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

"""
from __future__ import unicode_literals
from ..backupset import Backupset
from ..exception import SDKException
from ..schedules import Schedule


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
                    return Schedule(self._commcell_object, schedule_id=response.json()['taskId'])

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
