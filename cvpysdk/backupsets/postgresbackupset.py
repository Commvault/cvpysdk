# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

"""File for operating on a Postgres Server Backupset

PostgresBackupset is the only class defined in this file.

PostgresBackupset: Derived class from Backupset Base class, representing a Postgres
server backupset, and to perform operations on that backupset

PostgresBackupset:
==================

    run_live_sync()                      --  runs live sync replication operation

    configure_live_sync()                --  runs the Task API with the request JSON provided
    to create live sync configuration, and returns the contents after parsing the response

    restore_postgres_server()            --  method to restore the Postgres server

"""
from __future__ import unicode_literals
from ..backupset import Backupset
from ..exception import SDKException
from ..schedules import Schedule, Schedules
from typing import Any, Optional, List, Dict

class PostgresBackupset(Backupset):
    """
    Represents a PostgreSQL backup set, extending the Backupset base class.

    This class provides specialized operations for managing PostgreSQL backup sets,
    including configuration and execution of live sync operations, as well as
    comprehensive restore capabilities for PostgreSQL servers.

    Key Features:
        - Initialization of PostgreSQL backup set instances
        - Configuration of live sync operations using JSON requests
        - Execution of live sync to synchronize data between source and destination clients/instances
        - Restoration of PostgreSQL servers with support for various options such as:
            - Database selection
            - Time-based restores
            - Cloning environments and options
            - Media agent specification
            - Table-level and volume-level restores
            - Stream management
            - Redirection and restore-to-disk capabilities
            - Staging and destination path configuration
            - Revert operations

    This class is intended for use in environments requiring advanced backup and restore
    management for PostgreSQL databases, providing flexibility and control over backupset operations.

    #ai-gen-doc
    """

    def __init__(self, instance_object: Any, backupset_name: str, backupset_id: Optional[str] = None) -> None:
        """Initialize a PostgresBackupset instance.

        Args:
            instance_object: The instance object associated with the backupset.
            backupset_name: Name of the backupset as a string.
            backupset_id: Optional ID of the backupset as a string.

        Example:
            >>> instance = Instance(...)
            >>> backupset = PostgresBackupset(instance, "DailyBackup", backupset_id="12345")
            >>> print(f"Backupset created: {backupset}")

        #ai-gen-doc
        """
        super(PostgresBackupset, self).__init__(
            instance_object, backupset_name, backupset_id)
        self._LIVE_SYNC = self._commcell_object._services['LIVE_SYNC']

    def configure_live_sync(self, request_json: Dict[str, Any]) -> 'Schedule':
        """Configure live sync for the Postgres backupset using the provided request JSON.

        This method sends a POST request to the Task API to create a live sync configuration.
        Upon successful creation, it returns an instance of the Schedule class corresponding
        to the created task.

        Args:
            request_json: Dictionary containing the JSON request payload for the API.

        Returns:
            Schedule: Instance representing the created live sync schedule.

        Raises:
            SDKException: If live sync configuration fails, the response is empty, or the response indicates failure.

        Example:
            >>> request_json = {
            ...     "taskInfo": {
            ...         "task": {"taskType": 1, "initiatedFrom": 2},
            ...         "subTasks": [{"subTask": {"subTaskType": 2, "operationType": 402}}]
            ...     }
            ... }
            >>> backupset = PostgresBackupset(...)
            >>> schedule = backupset.configure_live_sync(request_json)
            >>> print(f"Live sync schedule created: {schedule}")
        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._LIVE_SYNC, request_json)

        if flag:
            if response.json():
                if "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    error_message = 'Live Sync configuration failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Backupset', '102', error_message)
                else:
                    raise SDKException('Backupset', '102', 'Failed to create schedule')
            else:
                raise SDKException('Backupset', '102')
        else:
            raise SDKException('Backupset', '101', self._update_response_(response.text))

    def run_live_sync(
            self,
            dest_client_name: str,
            dest_instance_name: str,
            baseline_job: Any
        ) -> 'Schedule':
        """Run a live sync replication operation for a PostgreSQL backupset.

        This method initiates a live sync replication from the current backupset to a specified
        destination client and instance, using a baseline backup job as the reference.

        Args:
            dest_client_name: Name of the destination client where files will be restored.
            dest_instance_name: Name of the destination PostgreSQL instance on the destination client.
            baseline_job: Baseline backup job object containing job details.

        Returns:
            Schedule: An instance of the Schedule class representing the configured live sync operation.

        Example:
            >>> baseline_job = BackupJob(...)  # Initialize with appropriate parameters
            >>> backupset = PostgresBackupset(...)
            >>> schedule = backupset.run_live_sync(
            ...     dest_client_name="dbserver02",
            ...     dest_instance_name="PostgresInstance2",
            ...     baseline_job=baseline_job
            ... )
            >>> print(f"Live sync scheduled: {schedule}")

        #ai-gen-doc
        """
        instance_object = self._instance_object
        instance_object._restore_association = self._properties["backupSetEntity"]
        request_json = instance_object._restore_json(
            paths=["/data"],
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            backupset_name="fsbasedbackupset",
            backupset_flag=True,
            no_image=True,
            overwrite=True,
            baseline_jobid=int(baseline_job.job_id),
            baseline_ref_time=int(baseline_job.summary['jobStartTime']))

        request_json['taskInfo']['subTasks'][0]['options']['backupOpts'] = {
            'backupLevel': 2,
            'vsaBackupOptions': {}
            }
        request_json['taskInfo']['task']['taskType'] = 2
        request_json['taskInfo']['subTasks'][0]['subTask']['operationType'] = 1007
        request_json['taskInfo']['subTasks'][0]['subTask']['subTaskName'] = "automation"
        request_json['taskInfo']['subTasks'][0]['pattern'] = {
            "freq_type": 4096,
            "timeZone": {
                "TimeZoneName": "(UTC) Coordinated Universal Time"
                }
            }

        return self.configure_live_sync(request_json)

    def restore_postgres_server(
            self,
            database_list: Optional[List[str]] = None,
            dest_client_name: Optional[str] = None,
            dest_instance_name: Optional[str] = None,
            copy_precedence: Optional[int] = None,
            from_time: Optional[str] = None,
            to_time: Optional[str] = None,
            clone_env: bool = False,
            clone_options: Optional[Dict[str, Any]] = None,
            media_agent: Optional[str] = None,
            table_level_restore: bool = False,
            staging_path: Optional[str] = None,
            no_of_streams: Optional[int] = None,
            volume_level_restore: bool = False,
            redirect_enabled: bool = False,
            redirect_path: Optional[str] = None,
            restore_to_disk: bool = False,
            restore_to_disk_job: Optional[List[int]] = None,
            destination_path: Optional[str] = None,
            revert: bool = False
        ) -> Any:
        """Restore the Postgres server with various restore options.

        This method initiates a restore operation for the Postgres server, supporting advanced options
        such as cloning, table-level restore, volume-level restore, redirect restore, and restore to disk.

        Args:
            database_list: Optional list of database names to restore. If None and backupset is file system based, defaults to ['/data'].
            dest_client_name: Optional destination client name for the restore. If None, uses the instance's client name.
            dest_instance_name: Optional destination instance name for the restore. If None, uses the instance's name.
            copy_precedence: Optional copy precedence associated with storage.
            from_time: Optional string specifying the start time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional string specifying the end time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            clone_env: Boolean indicating whether to clone the database environment.
            clone_options: Optional dictionary of clone restore options. Example:
                {
                    "stagingLocaion": "/gk_snap",
                    "forceCleanup": True,
                    "port": "5595",
                    "libDirectory": "/opt/PostgreSQL/9.6/lib",
                    "isInstanceSelected": True,
                    "reservationPeriodS": 3600,
                    "user": "postgres",
                    "binaryDirectory": "/opt/PostgreSQL/9.6/bin"
                }
            media_agent: Optional media agent name to use for restore.
            table_level_restore: Boolean indicating if the restore operation is table-level.
            staging_path: Optional staging path location for table-level restore.
            no_of_streams: Optional number of streams to use for volume-level restore.
            volume_level_restore: Boolean flag for volume-level restore.
            redirect_enabled: Boolean indicating if redirect restore is enabled.
            redirect_path: Optional path for redirect restore.
            restore_to_disk: Boolean flag to restore to disk.
            restore_to_disk_job: Optional list of backup job IDs to restore to disk.
            destination_path: Optional destination path for restore.
            revert: Boolean indicating whether to perform a hardware revert during restore.

        Returns:
            Job object containing restore details.

        Example:
            >>> backupset = PostgresBackupset(...)
            >>> job = backupset.restore_postgres_server(
            ...     database_list=['db1', 'db2'],
            ...     dest_client_name='DestinationClient',
            ...     dest_instance_name='DestinationInstance',
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-01-31 23:59:59',
            ...     clone_env=True,
            ...     clone_options={
            ...         "stagingLocaion": "/gk_snap",
            ...         "forceCleanup": True,
            ...         "port": "5595",
            ...         "libDirectory": "/opt/PostgreSQL/9.6/lib",
            ...         "isInstanceSelected": True,
            ...         "reservationPeriodS": 3600,
            ...         "user": "postgres",
            ...         "binaryDirectory": "/opt/PostgreSQL/9.6/bin"
            ...     },
            ...     media_agent='MediaAgent01',
            ...     table_level_restore=False,
            ...     volume_level_restore=True,
            ...     no_of_streams=4,
            ...     restore_to_disk=False,
            ...     destination_path='/restore/location'
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        instance_object = self._instance_object
        if dest_client_name is None:
            dest_client_name = instance_object._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = instance_object.instance_name

        backupset_name = self.backupset_name

        if backupset_name.lower() == "fsbasedbackupset":
            backupset_flag = True
            if database_list is None:
                database_list = ["/data"]
        else:
            backupset_flag = False

        instance_object._restore_association = self._properties['backupSetEntity']
        return instance_object.restore_in_place(
            database_list,
            dest_client_name,
            dest_instance_name,
            backupset_name,
            backupset_flag,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            clone_env=clone_env,
            clone_options=clone_options,
            media_agent=media_agent,
            table_level_restore=table_level_restore,
            staging_path=staging_path,
            no_of_streams=no_of_streams,
            volume_level_restore=volume_level_restore,
            redirect_enabled=redirect_enabled,
            redirect_path=redirect_path,
            restore_to_disk=restore_to_disk,
            restore_to_disk_job=restore_to_disk_job,
            destination_path=destination_path,
            revert=revert)
