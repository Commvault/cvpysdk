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

"""Main file for performing virtual lab restore operations on the Commcell.

Dev_Test_Group : Class for representing all the Virtual Lab creation associated
                    with the Commcell.

Dev_Test_Group:
    __init__(commcell_object)               --  initialize the VirtualMachinePolicies instance for
                                                    the Commcell
"""
import json
from .job import Job

class Dev_Test_Group(object):

    """ Class for Virtual Lab restore opreation with the Commcell"""

    def __init__(self, commcell_object):
        """Initialize object of the VirtualMachinePolicies class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Dev_Test_Group class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

    def dev_test_lab_json(self, vapp_prop=None):
        """
        Runs Virtual Lab job for the Dev-Test-Group at Commcell Level.

        vapp_prop (dict) -- options like vappName and vappId to be include while making
                            the request

        Returns:
                object - instance of the Job class for the Virtual Lab job

        """

        request_json = {
            "taskInfo": {
                "associations": [vapp_prop],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": self._json_virtual_subtasks,
                        "options": {
                            "adminOpts": {
                                "vmProvisioningOption": {
                                    "invokeWorkflowperJob": True,
                                    "operationType": 23,
                                    "workflow": {
                                        "workflowName": "CreateLab"
                                    },
                                    "virtualMachineOption": [self._json_provision_Option],
                                    "vAppEntity": vapp_prop
                                }
                            }
                        }
                    }
                ]
            }
        }

        return self._process_restore_response(request_json)

    @property
    def _json_task(self):
        """getter for the task information in JSON"""

        _taks_option_json = {
            "initiatedFrom": 1,
            "taskType": 1,
            "policyType": 0,
            "taskFlags": {
                "disabled": False
            }
        }

        return _taks_option_json

    @property
    def _json_virtual_subtasks(self):
        """getter for the subtask in restore JSON . It is read only attribute"""

        _virtual_subtask = {
            "subTaskType": 1,
            "operationType": 4038
        }

        return _virtual_subtask

    @property
    def _json_provision_Option(self):
        """getter for the subtask in restore JSON . It is read only attribute"""

        _provision_Option = {
            "powerOnVM": True,
            "useLinkedClone": False,
            "restoreAsManagedVM": False,
            "doLinkedCloneFromLocalTemplateCopy": False
        }

        return _provision_Option

    def _process_restore_response(self, request_json):
        """Runs the CreateTask API with the request JSON provided for Virtual Lab,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if restore job failed

                    if response is empty

                    if response is not success
        """
        self._RESTORE = self._services['RESTORE']
        flag, response = self._cvpysdk_object.make_request('POST', self._RESTORE, request_json)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Virtual Machine Management job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run Virtual Machine Management job')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))



