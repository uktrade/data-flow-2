import base64
import time
import os
import json
import shlex
import uuid
from typing import Optional

import dagster._check as check
from dagster._core.events import EngineEventData
from dagster._core.instance import T_DagsterInstance
from dagster._core.launcher.base import (
    CheckRunHealthResult,
    LaunchRunContext,
    RunLauncher,
    WorkerStatus,
)
from dagster._grpc.types import ExecuteRunArgs
from dagster._core.storage.dagster_run import DagsterRun
from dagster._core.storage.tags import RUN_WORKER_ID_TAG
from dagster._serdes import ConfigurableClass
from dagster._serdes.config_class import ConfigurableClassData

import requests


def CFToken(login_base, username, password):
    expires_at = time.monotonic()
    token = None

    def _get():
        nonlocal token
        nonlocal expires_at

        if expires_at > time.monotonic():
            return token

        response = requests.post(
            f'{login_base}oauth/token',
            headers={
                'Authorization': 'Basic ' + base64.b64encode(b'cf:').decode('ascii')
            },
            data={
                'username': username,
                'password': password,
                'grant_type': 'password',
            },
        )
        response.raise_for_status()
        response_json = response.json()

        token = response_json['access_token']
        # 5 to avoid us thinking valid, but not CF
        expires_at = time.monotonic() + int(response_json['expires_in']) - 5

        return token

    return _get


def APIRequest(get_token, api_base):

    def _request(method, path, params=None, json=None):
        response = requests.request(
            method=method,
            url=f'{api_base}{path}',
            headers={'authorization': f'bearer {get_token()}'},
            params=params,
            json=json,
        )
        response.raise_for_status()
        return response.json()

    return _request


class CFLauncher(RunLauncher[T_DagsterInstance], ConfigurableClass):

    def __init__(
        self,
        inst_data: Optional[ConfigurableClassData] = None,
    ):
        self._inst_data = inst_data
        api_base = os.environ['CF_API_BASE']
        get_token = CFToken(
            os.environ['CF_LOGIN_BASE'],
            os.environ['CF_USERNAME'],
            os.environ['CF_PASSWORD'],
        )
        self.make_api_request = APIRequest(get_token, api_base)
        self.mapping = json.loads(os.environ['CF_LAUNCHER_CODE_LOCATION_TO_APP_MAPPING'])

    # The following methods seem to be ~needed for the configuration system

    @classmethod
    def config_type(cls):
        return {}

    @property
    def inst_data(self):
        return self._inst_data

    @classmethod
    def from_config_value(cls, inst_data, config_value):
        return cls(inst_data=inst_data, **config_value)

    # The following methods are the core methods that define a launcher

    def launch_run(self, context: LaunchRunContext) -> None:
        """Launch a run.

        This method should begin the execution of the specified run, and may emit engine events.
        Runs should be created in the instance (e.g., by calling
        ``DagsterInstance.create_run()``) *before* this method is called, and
        should be in the ``PipelineRunStatus.STARTING`` state. Typically, this method will
        not be invoked directly, but should be invoked through ``DagsterInstance.launch_run()``.

        Args:
            context (LaunchRunContext): information about the launch - every run launcher
            will need the PipelineRun, and some run launchers may need information from the
            IWorkspace from which the run was launched.
        """
        run = context.dagster_run

        # A lot of this is best guess
        external_job_origin = check.not_none(run.external_job_origin)
        code_location = context.workspace.get_code_location(
            external_job_origin.external_repository_origin.code_location_origin.location_name
        )

        job_origin = check.not_none(run.job_code_origin)
        command_args = ExecuteRunArgs(
            job_origin=job_origin,
            run_id=run.run_id,
            instance_ref=self._instance.get_ref(),
            set_exit_code_on_failure=True,
        ).get_command_args()

        print("Code location name", code_location.name)
        print("App name", self.mapping[code_location.name])

        # Get app guid by its name
        app_guid = self.make_api_request(
            method='GET',
            path='v3/apps',
            params={'names': self.mapping[code_location.name]},
        )['resources'][0]['guid']

        # Start a task in this app (or more specifically, the app's current droplet)
        task = self.make_api_request(
            method='POST',
            path=f'v3/apps/{app_guid}/tasks',
            json={
                "command": shlex.join(['./pipelines_platform/paas-wrapper.sh'] + command_args),
            }
        )

        # Save tags to be able to find the task later
        self._instance.add_run_tags(run.run_id, {
            "cf/task_guid": task['guid'],
            "cf/task_name": task['name'],
            RUN_WORKER_ID_TAG: str(uuid.uuid4().hex)[0:6],
        })

        # Report event
        self._instance.report_engine_event(
            message="Launching run as CloudFoundry task",
            dagster_run=run,
            engine_event_data=EngineEventData({
                "CF task GUID": task['guid'],
                "CF task name": task['name'],
            }),
            cls=self.__class__,
        )

    def terminate(self, run_id: str) -> bool:
        """Terminates a process.

        Returns False is the process was already terminated. Returns true if
        the process was alive and was successfully terminated
        """

        run = self._instance.get_run_by_id(run_id)
        if not run:
            return False

        task_guid = run.tags.get("cf/task_guid")
        if not task_guid:
            return False

        # Reasonable to report this before making the API request so there
        # is feedback to the user in case it's slow
        self._instance.report_run_canceling(run)

        task = self.make_api_request(
            method='GET',
            path=f'v3/tasks/{task_guid}',
        )
        if task['state'] in ('SUCCEEDED', 'FAILED'):
            self._instance.report_engine_event(
                message=f"CloudFoundry task already {task['state']}",
                dagster_run=run,
                engine_event_data=EngineEventData({
                    "CF task GUID": task['guid'],
                    "CF task name": task['name'],
                }),
                cls=self.__class__,
            )
            return False

        self._instance.report_engine_event(
            message="Cancelling CloudFoundry task",
            dagster_run=run,
            engine_event_data=EngineEventData({
                "CF task GUID": task['guid'],
                "CF task name": task['name'],
            }),
            cls=self.__class__,
        )

        self.make_api_request(
            method='GET',
            path=f'v3/tasks/{task_guid}/actions/cancel',
        )
        return True

    def dispose(self) -> None:
        """Do any resource cleanup that should happen when the DagsterInstance is
        cleaning itself up.
        """
        pass

    @property
    def supports_check_run_worker_health(self) -> bool:
        """Whether the run launcher supports check_run_worker_health."""
        return True

    def check_run_worker_health(self, run: DagsterRun) -> CheckRunHealthResult:
        run_worker_id = run.tags.get(RUN_WORKER_ID_TAG)

        task_guid = run.tags.get("cf/task_guid")
        if not task_guid:
            return CheckRunHealthResult(WorkerStatus.UNKNOWN, "", run_worker_id=run_worker_id)

        task = self.make_api_request(
            method='GET',
            path=f'v3/tasks/{task_guid}',
        )
        if task['state'] in ('PENDING', 'RUNNING'):
            return CheckRunHealthResult(WorkerStatus.RUNNING, "", run_worker_id=run_worker_id)
        if task['state'] == 'SUCCEEDED':
            return CheckRunHealthResult(WorkerStatus.SUCCESS, "", run_worker_id=run_worker_id)
        if task['state'] in ('CANCELING', 'FAILED'):
            message = task.get('result', {}).get('failure_reason', '')
            return CheckRunHealthResult(WorkerStatus.FAILED, message, run_worker_id=run_worker_id)

        return CheckRunHealthResult(WorkerStatus.SUCCESS, run_worker_id=run_worker_id)
