# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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


class PostgresBackupset(Backupset):
    """Derived class from Backupset Base class, representing a postgres backupset,
        and to perform operations on that backupset."""

    def __init__(self, instance_object, backupset_name, backupset_id=None):
        """
        Constructor for the class

        Args:
            instance_object   (obj)     -- instance object

            backupset_name    (str)     -- name of the backupset

            backupset_id      (str)     -- id of the backupset

        """
        super(PostgresBackupset, self).__init__(
            instance_object, backupset_name, backupset_id)
        self._LIVE_SYNC = self._commcell_object._services['LIVE_SYNC']

    def configure_live_sync(self, request_json):
        """Runs the Task API with the request JSON provided to create live sync configuration,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                object - instance of the Schedule class

            Raises:
                SDKException:
                    if live sync configuration fails

                    if response is empty

                    if response is not success
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
            dest_client_name,
            dest_instance_name,
            baseline_job):
        """runs live sync replication operation

            Args:

                dest_client_name        (str)   --  destination client name where files are to be
                restored

                dest_instance_name      (str)   --  destination postgres instance name of
                destination client

                baseline_job            (obj)   --  baseline backup job object

            Returns:
                object - instance of the Schedule class

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
            database_list=None,
            dest_client_name=None,
            dest_instance_name=None,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            clone_env=False,
            clone_options=None,
            media_agent=None,
            table_level_restore=False,
            staging_path=None,
            no_of_streams=None,
            volume_level_restore=False,
            redirect_enabled=False,
            redirect_path=None,
            restore_to_disk=False,
            restore_to_disk_job=None,
            destination_path=None):
        """
        Method to restore the Postgres server

            Args:

                database_list               (List) -- List of databases

                dest_client_name            (str)  -- Destination Client name

                dest_instance_name          (str)  -- Destination Instance name

                copy_precedence             (int)  -- Copy precedence associted with storage

                from_time               (str)   --  time to retore the contents after
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time                 (str)   --  time to retore the contents before
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                clone_env                   (bool)  --  boolean to specify whether the database
                should be cloned or not

                    default: False

                clone_options               (dict)  --  clone restore options passed in a dict

                    default: None

                    Accepted format: {
                                        "stagingLocaion": "/gk_snap",
                                        "forceCleanup": True,
                                        "port": "5595",
                                        "libDirectory": "/opt/PostgreSQL/9.6/lib",
                                        "isInstanceSelected": True,
                                        "reservationPeriodS": 3600,
                                        "user": "postgres",
                                        "binaryDirectory": "/opt/PostgreSQL/9.6/bin"

                                     }

                media_agent             (str)   --  media agent name

                    default: None

                table_level_restore     (bool)  --  boolean to specify if the restore operation
                is table level

                    default: False

                staging_path            (str)   --  staging path location for table level restore

                    default: None

                no_of_streams           (int)   --  number of streams to be used by
                volume level restore

                    default: None

                volume_level_restore    (bool)  --  volume level restore flag

                    default: False

                redirect_enabled         (bool)  --  boolean to specify if redirect restore is
                enabled

                    default: False

                redirect_path           (str)   --  Path specified in advanced restore options
                in order to perform redirect restore

                    default: None

                restore_to_disk         (bool)  --  restore to disk flag

                    default: False

                restore_to_disk_job     (list)   --  list of backup job ids to restore to disk

                    default: None

                destination_path        (str)   --  destination path for restore

                    default: None

            Returns:
                object -- Job containing restore details

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
            destination_path=destination_path)
