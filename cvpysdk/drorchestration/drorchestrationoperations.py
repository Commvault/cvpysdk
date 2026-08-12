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

"""Main file for performing DR Orchestration specific operations.


DROrchestrationOperations:  Class for representing all the DR orchestration operations from failover groups
                            or replication monitor


DROrchestrationOperations:
    __init__(commcell_object)                       -- Initialise object of DROrchestrationOperations

    __repr__()                                      -- Return the DROrchestrationOperations

    testboot()                                      -- Call testboot operation

    planned_failover()                              -- Call Planned failvoer operation

    unplanned_failover()                            -- Call Unplanned Failover operation

    failback()                                      -- Call failback operation

    undo_failover()                                 -- Call UndoFailover operation

    revert_failover()                               -- Call RevertFailover operation

    point_in_time_failover()                        -- Call PointInTimeFailover operation

    reverse_replication()                           -- Schedule and call ReverseReplication operation

    schedule_reverse_replication()                  -- Schedule ReverseReplication

    force_reverse_replication()                     -- Call ReverseReplication operation

    validate_dr_orchestration_job(jobId)            -- Validate DR orchestration job Id

    get_snapshot_list(guid)                         -- Retrieves snapshot lists from the specified guid


    ##### internal methods #####
    _construct_dr_orchestration_operation_json()    -- Construct dr orchestration operation json

    _construct_reverse_replication_json()           -- Construct reverse replication json

    _call_dr_orchestration_task
    (dr_orchestration_json)                         -- Call DR orchestration task

    _call_reverse_replication_task
    (dr_orchestration_json)                         -- Call reverse replication

    _get_dr_orchestration_job_stats
    (jobId, replicationId)                          -- Gets DR orchetration job phase types and states


    ##### properties #####
    _json_task()                                    -- Returns task json

    _json_dr_orchestration_subtasks()               -- Returns DR orchestration subtasks json

    _json_dr_orchestration()                        -- Returns DR orchestration json

    _dr_group_id()                                  -- Returns DR group Id

    dr_orchestration_options()                      -- DR orchestration options

    dr_orchestration_job_phase()                    -- DR orchestration job phase type


"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ..exception import SDKException

from .dr_orchestration_job_phase import DRJobPhaseToText, DRJobPhases


class DROrchestrationOperations(object):
    """Class for invoking DROrchestration operations in the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the DROrchestrationOperations.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the DROrchestrationOperations class
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services

        ####### init REST API URLS #########
        self._CREATE_TASK = self._commcell_object._services['CREATE_TASK']
        self._REVERSE_REPLICATION_TASK = self._commcell_object._services[
            'REVERSE_REPLICATION_TASK']

        #### init variables ######
        self._dr_orchestration_option = None
        self._dr_orchestration_job_phase = None
        self._dr_group_Id = 0

    def __repr__(self):
        """String representation of the instance of this class."""
        return 'DROrchestrationOperations instance for Commcell'

    @property
    def dr_orchestration_job_phase(self):
        """
        Args:

        Returns: DR orchestration job phase dict

        Raises:
        """
        if not self._dr_orchestration_job_phase:
            _dr_orchestration_job_phase = DRJobPhases

            self._dr_orchestration_job_phase = _dr_orchestration_job_phase
        return self._dr_orchestration_job_phase

    @property
    def dr_orchestration_options(self):
        """Getter dr orchestration options json"""
        return self._dr_orchestration_option

    @dr_orchestration_options.setter
    def dr_orchestration_options(self, value):
        """Setter dr orchestration options json"""
        self._dr_orchestration_option = value

    @property
    def dr_group_id(self):
        """Getter DR group Id"""
        return int(self.dr_orchestration_options.get("failoverGroupId", 0))

    @property
    def _json_task(self):
        """Getter for the task information in JSON"""

        _taks_option_json = {
            "ownerId": 1,
            "taskType": 1,
            "ownerName": "admin",
            "sequenceNumber": 0,
            "initiatedFrom": 2,
            "taskFlags": {
                "disabled": False
            }
        }

        return _taks_option_json

    @property
    def _json_dr_orchestration_subtasks(self):
        """Getter for the subtask in DR orchestraion JSON . It is read only attribute"""

        _backup_subtask = {
            "subTaskType": 1,
            "operationType": 4046
        }

        return _backup_subtask

    @property
    def _json_dr_orchestration(self):
        """Getter for the DRorchestration task in failover group JSON . It is read only attribute"""

        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        initiatedFrom = self.dr_orchestration_options.get(
            "initiatedfromMonitor", False)

        _dr_orchestration_json = {
            "operationType": int(self.dr_orchestration_options.get("DROrchestrationType")),
            "initiatedfromMonitor": initiatedFrom,
            "advancedOptions": {
                "skipDisableNetworkAdapter": self.dr_orchestration_options.get("skipDisableNetworkAdapter", False)
            }
        }

        # if initiated from monitor set To True
        if initiatedFrom:

            _dr_orchestration_json.update({
                    "replicationInfo": {
                        "replicationId": self.dr_orchestration_options.get("replicationIds", [0])
                    }
            })

        else:
            _dr_orchestration_json.update({
                "vApp": {
                    "vAppId": int(self.dr_orchestration_options.get("failoverGroupId")),
                    "vAppName": self.dr_orchestration_options.get("failoverGroupName")
                }
            })

        return _dr_orchestration_json

    def testboot(self):
        """Performs testboot failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the Testboot job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "7"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def planned_failover(self):
        """Performs Planned failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the Planned Failover job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "1"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def unplanned_failover(self):
        """Performs UnPlanned failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the Unplanned Failover job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "3"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def failback(self):
        """Performs Failback operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "2"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def undo_failover(self):
        """Performs Undo Failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "6"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def reverse_replication(self):
        """Schedules and calls Reverse Replication

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the reverse replication job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        self.schedule_reverse_replication()
        return self.force_reverse_replication()

    def schedule_reverse_replication(self):
        """Schedules Reverse Replication.

            Args:

            Returns:
                (TaskId) - TaskId of the scheduling reverse replication job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "9"
        dr_orchestration_json = self._json_dr_orchestration

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_reverse_replication_task(dr_orchestration_json)

    def force_reverse_replication(self):
        """Performs one reverse replication operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the reverse replication job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "9"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        # We need to have this option in the request because "powerOnVM" is True by default.
        # If it is not set, both src and dst VMs will be booted up.
        dr_orchestration_json["taskInfo"]["subTasks"][0]["options"][
            "adminOpts"]["drOrchestrationOption"]["advancedOptions"].update(
                {"powerOnVM": False})

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def revert_failover(self):
        """Performs Revert Failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "4"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def point_in_time_failover(self, timestamp, replication_id):
        """Performs Point in time Failover operation.

            Args:

            Returns:
                (JobId, TaskId) - JobId and taskId of the failback job triggered

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(self.dr_orchestration_options, dict):
            raise SDKException('DROrchestrationOperations', '101')

        self.dr_orchestration_options["DROrchestrationType"] = "8"
        dr_orchestration_json = self._construct_dr_orchestration_operation_json()

        if not dr_orchestration_json:
            raise SDKException('DROrchestrationOperations', '101')

        dr_orchestration_json["taskInfo"]["subTasks"][0]["options"][
            "adminOpts"]["drOrchestrationOption"]["replicationInfo"][
                "configOption"] = [
                    {"pointInTime": int(timestamp),
                     "replicationId": int(replication_id)}]

        return self._call_dr_orchestration_task(dr_orchestration_json)

    def validate_dr_orchestration_job(self, jobId):
        """ Validates DR orchestration job of jobId
            Args:
                JobId: Job Id of the DR orchestration job

            Returns:
                bool - boolean that represents whether the DR orchestration job finished successfully or not

            Raises:
                SDKException:
                    if proper inputs are not provided
                    If failover phase failed at any stage
        """

        if not isinstance(jobId, str):
            raise SDKException('DROrchestrationOperations', '101')

        _replicationIds = self.dr_orchestration_options.get(
            "replicationIds", [])
        if not _replicationIds:
            raise SDKException('DROrchestrationOperations', '101')

        # iterate over replication Ids
        for replicationId in iter(_replicationIds):

            dr_orchestration_job_stats_json = self._get_dr_orchestration_job_stats(
                str(jobId), str(replicationId))

            if dr_orchestration_job_stats_json and isinstance(
                    dr_orchestration_job_stats_json, dict):

                if "phase" in dr_orchestration_job_stats_json:

                    for phase in dr_orchestration_job_stats_json["phase"]:

                        phase_type = DRJobPhaseToText(self.dr_orchestration_job_phase(phase["phase"])).value
                        phase_state = phase["status"]

                        if phase_state == 1:
                            o_str = 'Failed to complete phase: [' + str(
                                phase_type) + '] status: [' + str(phase_state) + ']'
                            raise SDKException(
                                'DROrchestrationOperations', '102', o_str)

                else:

                    o_str = 'Failed to finish any phases in DR orchestration Job {0} \n'.format(
                        jobId)
                    raise SDKException(
                        'DROrchestrationOperations', '102', o_str)

        return True

    def get_snapshot_list(self, guid: str, instance_id: int, timestamp_filter: bool = True):
        """ Gets snapshot list

            Args:
                guid (str): GUID of the spcified VM

                timestamp_filter (bool): whether to only return snapshots with timestamps

            Returns:
                list of dict: list of snapshot information
        """
        vm_browse_req = "{0}VMBrowse/{1}?instanceId={2}&snapshots=true".format(
            self._commcell_object._web_service, guid, instance_id)
        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='GET', url=vm_browse_req)

        # only fetches snapshot info from the response
        if flag:
            if response.json():
                snapshots = response.json()["scList"][0]["snapshots"]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

        if timestamp_filter:
            # we only need snapshots with timestamps
            snapshots = list(
                filter(lambda s: "__GX_Recovery_Point_" in s["name"], snapshots))

            # adds integer timestamps to the list
            for s in snapshots:
                timestamp = s["name"].split("_")[-1]
                s["timestamp"] = int(timestamp)

        return snapshots


#################### private functions #####################

    def _get_dr_orchestration_operation_string(self, orchestration_type):
        """Getter for dr orchestration operation type"""

        _orchestration_string = ""
        if orchestration_type == 1:
            _orchestration_string = "Planned Failover"

        elif orchestration_type == 2:
            _orchestration_string = "Failback"

        elif orchestration_type == 3:
            _orchestration_string = "UnPlanned Failover"

        elif orchestration_type == 4:
            _orchestration_string = "Revert Failover"

        elif orchestration_type == 6:
            _orchestration_string = "Undo Failover"

        elif orchestration_type == 7:
            _orchestration_string = "TestBoot"

        elif orchestration_type == 8:
            _orchestration_string = "Point in Time Failover"

        elif orchestration_type == 9:
            _orchestration_string = "Reverse Replication"

        return _orchestration_string

    def _construct_dr_orchestration_operation_json(self):
        """
            Constructs DR orchestration operation json to invoke DR orchestration operation in the commcell

            Args:

            Returns: DR orchestration json dict

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        dr_orchestration_json = {
            "taskInfo": {
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": self._json_dr_orchestration_subtasks,
                        "options": {
                            "adminOpts": {
                                "drOrchestrationOption": self._json_dr_orchestration
                            }
                        }
                    }
                ]
            }
        }

        return dr_orchestration_json

    def _construct_reverse_replication_json(self):
        """
            Constructs reverse replication json to invoke reverse replication task in the commcell

            Args:

            Returns: Reverse replication task dict

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        dr_orchestration_json = {

            "drOrchestrationOption": self._json_dr_orchestration

        }

        return dr_orchestration_json

    def _call_dr_orchestration_task(self, dr_orchestration_json):
        """
            Invokes DR orchestration operation task

            Args: dr orchestration json

                    taskInfo':  {
                    'task':  {
                        'taskFlags':  {
                            'disabled':  0
                        },
                         'taskType':  1,
                         'ownerId':  1,
                         'initiatedFrom':  2,
                         'sequenceNumber':  0,
                         'ownerName':  'admin'
                    },
                     'subTasks':  {
                        'subTask':  {
                            'subTaskType':  1,
                             'operationType':  4046
                        },
                         'options':  {
                            'adminOpts':  {
                                'drOrchestrationOption':  {
                                    'replicationInfo':  {
                                        'replicationId':  [
                                            {
                                                'val':  3
                                            },
                                             {
                                                'val':  4
                                            }
                                        ]
                                    },
                                     'vApp':  {
                                        'vAppId':  26,
                                         'vAppName':  'fg1-automation1x21'
                                    },
                                     'advancedOptions':  {
                                        'skipDisableNetworkAdapter':  0
                                    },
                                     'operationType':  7,
                                     'initiatedfromMonitor':  0
                                }
                            }
                        },
                         'subTaskOperation':  1
                    }
                }
            }


            Returns:
                (JobId, TaskId) - JobId and taskId of the DR orchestration job triggered

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        if not isinstance(dr_orchestration_json, dict):
            raise SDKException('DROrchestrationOperations', '101')

        # passing the built json to start failover
        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='POST', url=self._CREATE_TASK, payload=dr_orchestration_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to start {0} job \nError: "{1}"'.format(
                        self._get_dr_orchestration_operation_string(self.dr_orchestration_options.get("DROrchestrationType")), error_message)

                    raise SDKException(
                        'DROrchestrationOperations', '102', o_str)
                else:
                    # return object of corresponding Virtual Machine Policy
                    # here
                    task_id = response.json()['taskId']
                    job_id = response.json()['jobIds'][0]
                    return (job_id, task_id)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _call_reverse_replication_task(self, dr_orchestration_json):
        """
            Create reverse replication task

            Args: DR orchestration json

                drOrchestrationOption':  {
                    'replicationInfo':  {
                        'replicationId':  [
                            {
                                'val':  3
                            },
                             {
                                'val':  4
                            }
                        ]
                    },

                     'advancedOptions':  {
                        'skipDisableNetworkAdapter':  0
                    },
                     'operationType':  9,
                     'initiatedfromMonitor':  1
            }


            Returns:
                (TaskId) - taskId of the created reverse replication schedule

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """

        if not isinstance(dr_orchestration_json, dict):
            raise SDKException('DROrchestrationOperations', '101')

        # passing the built json to start DR orchestration
        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='PUT', url=self._REVERSE_REPLICATION_TASK, payload=dr_orchestration_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to start {0} job \nError: "{1}"'.format(
                        self._get_dr_orchestration_operation_string(self.dr_orchestration_options.get("DROrchestrationType")), error_message)

                    raise SDKException(
                        'DROrchestrationOperations', '102', o_str)
                else:
                    # return object of corresponding Virtual Machine Policy
                    # here
                    task_id = response.json()['taskId']
                    return (task_id)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _get_dr_orchestration_job_stats(self, jobId, replicationId):
        """ Gets DR orchestration job stats json
            Args:
                JobId: Job Id of the DR orchestration job
                replicationId: replication Id of the DR orchestration

            Returns:
                dict - DR orchestration job phases
                {
                            "jobId": 4240,
                            "replicationId": 7,
                            "phase": [
                                {
                                    "phase": 15,
                                    "status": 0,
                                    "startTime": {
                                        "_type_": 55,
                                        "time": 1516293332
                                    },
                                    "endTime": {
                                        "_type_": 55,
                                        "time": 1516293335
                                    },
                                    "entity": {
                                        "clientName": "failovervm1"
                                    }
                                },
                                {
                                    "phase": 17,
                                    "status": 0,
                                    "startTime": {
                                        "_type_": 55,
                                        "time": 1516293335
                                    },
                                    "endTime": {
                                        "_type_": 55,
                                        "time": 1516293340
                                    },
                                    "entity": {
                                        "clientName": "failovervm1"
                                    }
                                },
                                {
                                    "phase": 20,
                                    "status": 0,
                                    "startTime": {
                                        "_type_": 55,
                                        "time": 1516293340
                                    },
                                    "endTime": {
                                        "_type_": 55,
                                        "time": 1516293345
                                    },
                                    "entity": {
                                        "clientName": "failovervm1"
                                    }
                                }
            }

            Raises:
                SDKException:
                    if proper inputs are not provided
                    If DR orchestration phase failed at any stage
        """

        if not isinstance(jobId, str) and not isinstance(
                replicationId, str):
            raise SDKException('DROrchestrationOperations', '101')

        _DR_JOB_STATS = self._services['FAILOVER_GROUP_JOB_STATS'] % (jobId, self.dr_group_id, replicationId)

        # passing the built json to get DR orchestration job phases
        (flag, response) = self._commcell_object._cvpysdk_object.make_request(
            method='GET', url=_DR_JOB_STATS)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to validate DR orchestration job {0} \nError: "{1}"'.format(jobId,
                                                                                                error_message)

                    raise SDKException(
                        'DROrchestrationOperations', '102', o_str)
                else:

                    if 'job' in response.json():

                        # return DR orchestration job phases
                        return (response.json()["job"][0])

                    else:
                        raise SDKException(
                            'DROrchestrationOperations', '102', 'Failed to start DR orchestration job')

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)
