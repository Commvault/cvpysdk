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

"""" Main file for performing the Uniinstall operations

Download
========

    __init__(commcell_object)        --  initialize commcell_object of Uninstall class
    associated with the commcell

    uninstall_software                 --  Uninstalls all the packages of the selected client.

"""

from ..job import Job
from ..exception import SDKException
from typing import List, Dict, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..commcell import Commcell

UNINSTALL_SELECTED_PACKAGES = 6
class Uninstall(object):
    """class for Uninstalling software packages

    Attributes:
        _commcell_object (Commcell): Instance of the Commcell class.
        _services (dict): Available Commcell services.
        _cvpysdk_object (CVPySDK): Instance of the CVPySDK class.
    Usage:
        # Initialize the Uninstall class
        uninstall_obj = Uninstall(commcell_object)
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize object of the Uninstall class.

        Args:
            commcell_object (object): instance of the Commcell class

        Returns:
            Uninstall: instance of the Uninstall class

        """

        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._cvpysdk_object = commcell_object._cvpysdk_object

    def uninstall_software(self, client_name: str, force_uninstall: bool=True, client_composition: List[Dict]=None) -> Job:
        """
        Performs readiness check on the client

        Args:
            client_name     (str): The client_name whose packages are to be uninstalled.
            force_uninstall (bool): Uninstalls packages forcibly. Defaults to True.
            client_composition (list): The client_coposition will contain the list of components need to be uninstalled.

        Returns:
            Job: An instance of the Job class representing the uninstall job.

        Raises:
            SDKException:
                if response is empty

                if response is not success

        Usage:
            uninstall.uninstall_software(client_name="freezaclient")

            uninstall.uninstall_software(client_name="freezaclient", force_uninstall=False)

            uninstall.uninstall_software(client_name="freezaclient", force_uninstall=False, client_composition=[{
                                     "activateClient": True,
                                     "packageDeliveryOption": 0,
                                     "components": {
                                         "componentInfo": [
                                             {
                                                 "osType": "Windows",
                                                 "ComponentName": "High Availability Computing"
                                             },
                                             {
                                                 "osType": "Windows",
                                                 "ComponentName": "Index Store"
                                             },
                                             {
                                                 "osType": "Windows",
                                                 "ComponentName": "Index Gateway"
                                             }
                                         ]
                                     }
                                 }
                             ])
        """
        if not isinstance(client_name, str):
            raise SDKException('Uninstall', '101')
        optype = 7 # default value to remove all the packages
        if client_composition:
            optype = UNINSTALL_SELECTED_PACKAGES
        request_json = {
            "taskInfo": {
                "associations": [
                    {
                        "clientName": client_name
                    }
                ],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4027
                        },
                        "options": {
                            "adminOpts": {
                                "clientInstallOption": {
                                    "forceUninstall": force_uninstall,
                                    "installOSType": 0,
                                    "discoveryType": 0,
                                    "installerOption": {
                                        "requestType": 0,
                                        "Operationtype": optype,
                                        "CommServeHostName": self._commcell_object.commserv_name,
                                        "RemoteClient": False,
                                        "User": {
                                            "userName": "admin"
                                        },
                                        "clientComposition":client_composition
                                    },
                                    "clientDetails": [
                                        {
                                            "clientEntity": {
                                                "clientName": client_name
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._services['CREATE_TASK'], request_json)

        if flag:
            if response.json():
                if 'jobIds' in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                else:
                    o_str = 'Failed to submit uninstall job.'
                    raise SDKException('Uninstall', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
