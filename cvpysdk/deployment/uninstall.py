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

from past.builtins import basestring

from ..job import Job
from ..exception import SDKException


class Uninstall(object):
    """"class for Uninstalling software packages"""

    def __init__(self, commcell_object):
        """Initialize object of the Uninstall class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Uninstall class

        """

        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._cvpysdk_object = commcell_object._cvpysdk_object

    def uninstall_software(self, client_name, force_uninstall=True):
        """
        Performs readiness check on the client

            Args:
                force_uninstall (bool): Uninstalls packages forcibly. Defaults to True.

                client_name     (str): The client_name whose packages are to be uninstalled.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        if not isinstance(client_name, basestring):
            raise SDKException('Uninstall', '101')

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
                                        "Operationtype": 7,
                                        "CommServeHostName": self._commcell_object.commserv_name,
                                        "RemoteClient": False,
                                        "User": {
                                            "userName": "admin"
                                        }
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
