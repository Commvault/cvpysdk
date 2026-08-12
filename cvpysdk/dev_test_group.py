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
from typing import Optional

from .job import Job
from .schedules import Schedules
from .exception import SDKException

class Dev_Test_Group(object):
    """
    Class for managing Virtual Lab restore operations with the Commcell.

    This class provides an interface to perform and manage virtual lab restore operations
    within a Commcell environment. It allows users to generate and process restore tasks,
    handle virtual application properties, and access various JSON representations of tasks
    and subtasks related to the restore process.

    Key Features:
        - Initialization with a Commcell object for context
        - Generation of virtual lab restore JSON using virtual application properties
        - Access to JSON representations of restore tasks, virtual subtasks, and provision options
        - Internal processing of restore responses from JSON requests

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize an instance of the Dev_Test_Group class.

        Args:
            commcell_object: An instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> dev_test_group = Dev_Test_Group(commcell)
            >>> print(type(dev_test_group))
            <class 'Dev_Test_Group'>

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

    def dev_test_lab_json(self, vapp_prop: Optional[dict] = None) -> 'Job':
        """Run a Virtual Lab job for the Dev-Test-Group at the Commcell level.

        Args:
            vapp_prop: Optional dictionary containing properties such as 'vappName' and 'vappId'
                to include in the Virtual Lab job request.

        Returns:
            Job: An instance of the Job class representing the initiated Virtual Lab job.

        Example:
            >>> group = Dev_Test_Group(commcell)
            >>> job = group.dev_test_lab_json({'vappName': 'TestApp', 'vappId': 12345})
            >>> print(f"Virtual Lab job started with ID: {job.job_id}")

        #ai-gen-doc
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
    def _json_task(self) -> dict:
        """Get the task information for this Dev_Test_Group as a JSON dictionary.

        Returns:
            dict: A dictionary containing the task information in JSON format.

        Example:
            >>> group = Dev_Test_Group()
            >>> task_info = group._json_task
            >>> print(task_info)
            >>> # Output will be a dictionary with task details in JSON structure

        #ai-gen-doc
        """

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
    def _json_virtual_subtasks(self) -> dict:
        """Get the list of virtual subtasks from the restore JSON.

        This property provides read-only access to the subtasks defined in the restore JSON
        for the Dev_Test_Group. The returned list contains the details of each subtask.

        Returns:
            list: A list of virtual subtask dictionaries from the restore JSON.

        Example:
            >>> group = Dev_Test_Group()
            >>> subtasks = group._json_virtual_subtasks
            >>> print(f"Number of virtual subtasks: {len(subtasks)}")
            >>> # Access details of the first subtask
            >>> if subtasks:
            >>>     print(subtasks[0])

        #ai-gen-doc
        """

        _virtual_subtask = {
            "subTaskType": 1,
            "operationType": 4038
        }

        return _virtual_subtask

    @property
    def _json_provision_Option(self) -> dict:
        """Get the provision option subtask from the restore JSON.

        This property provides read-only access to the subtask information used in the restore JSON
        for the Dev_Test_Group. It is intended for internal use when constructing or inspecting
        restore operations.

        Returns:
            dict: The subtask dictionary from the restore JSON.

        Example:
            >>> group = Dev_Test_Group()
            >>> provision_option = group._json_provision_Option
            >>> print(provision_option)
            {'subtaskType': 'RESTORE', 'options': {...}}

        #ai-gen-doc
        """

        _provision_Option = {
            "powerOnVM": True,
            "useLinkedClone": False,
            "restoreAsManagedVM": False,
            "doLinkedCloneFromLocalTemplateCopy": False
        }

        return _provision_Option

    def _process_restore_response(self, request_json: dict) -> 'Job':
        """Execute the CreateTask API for Virtual Lab restore and process the response.

        This method sends the provided JSON request to the CreateTask API to initiate a Virtual Lab restore job.
        It parses the API response and returns an instance of the Job class representing the restore job.

        Args:
            request_json: Dictionary containing the JSON request payload for the CreateTask API.

        Returns:
            Job: An instance of the Job class representing the initiated restore job.

        Raises:
            SDKException: If the restore job fails, the response is empty, or the response indicates failure.

        Example:
            >>> request_payload = {...}  # Construct the appropriate request JSON
            >>> job = dev_test_group._process_restore_response(request_payload)
            >>> print(f"Restore job ID: {job.job_id}")

        #ai-gen-doc
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



