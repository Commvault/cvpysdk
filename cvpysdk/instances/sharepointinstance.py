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
"""
SharepointInstance is the only class defined in this file.

SharepointInstance  :  Derived class from Instance  Base class, representing a
                       Sharepoint Instance, and to perform operations on that instance

SharepointInstance:

     _restore_common_options_json()  -- setter for common options property in restore

     _restore_json() --  Method which creates json for a restore job

     _restore_v1_json() -- Method which creates json for v1 client for a restore job

"""

from cvpysdk.exception import SDKException
from ..instance import Instance



class SharepointInstance(Instance):
    """ Class  representing a sharepoint instance, and to perform operations on that instance
    """

    def _restore_browse_option_json(self, value):
        """setter for the Browse options for restore in Json"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        time_range_dict = {}
        if value.get('to_time'):
            time_range_dict['toTime'] = value.get('to_time')
        self._browse_restore_json = {
            "commCellId":  int(self._commcell_object.commcell_id),
            "showDeletedItems": value.get("showDeletedItems", False),
            "backupset": {
                "clientName": self._agent_object._client_object.client_name,
                "appName": self._agent_object.agent_name,
                "clientId": int(self._instance['clientId']),
                "backupsetId": int(self._restore_association['backupsetId'])
            },
            "timeRange": time_range_dict
        }

    def _restore_common_options_json(self, value):
        """setter for  the Common options of in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._commonoption_restore_json = {
            "allVersion": True,
            "offlineMiningRestore": False,
            "skip": not value.get("unconditional_overwrite", False),
            "restoreACLs": False,
            "erExSpdbPathRestore": True,
            "unconditionalOverwrite": value.get("unconditional_overwrite", False),
            "siteReplicationrestore": False,
            "append": False
        }

    def _restore_destination_json(self, value):
        """setter for  the destination restore option in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._destination_restore_json = {
            "inPlace": value.get("in_place", True),
            "destClient": {
                "clientName": value.get("client_name", ""),
                "clientId": value.get("client_id", -1)
            }
        }

    def _restore_json(self, **kwargs):
        """
        Creates json required for restore job

        Kwargs:

            paths   (list)  --  list of sites or webs to be restored
                Example : [
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Shared Documents\\TestFolder",
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Lists\\TestList",
                        ]
        Returns:

            rest_json  (dict)  --  dictionary with parameters set required for a restore job

        """
        if(kwargs.get("v1",False)):
            return self._restore_v1_json(**kwargs)
        rest_json = super(SharepointInstance, self)._restore_json(**kwargs)
        rest_json["taskInfo"]["task"]["initiatedFrom"] = 1
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["sharePointDocRstOption"] = {}
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]\
            ["sharePointRstOption"]= {
                "sharePointDocument": True,
                "spRestoreToDisk": {
                    "restoreToDiskPath": "",
                    "restoreToDisk": False
                }
            }
        rest_json["taskInfo"]["subTasks"][0]["options"]["commonOpts"] = {
            "notifyUserOnJobCompletion": False
        }
        return rest_json

    def _restore_v1_json(self, **kwargs):
        """
        Creates json required for restore job for v1 client

        Kwargs:

            paths   (list)  --  list of sites or webs to be restored
                Example : [
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Shared Documents\\TestFolder",
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Lists\\TestList",
                        ]
        Returns:

            rest_json  (dict)  --  dictionary with parameters set required for a restore job

        """
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        if self._restore_association is None:
            self._restore_association = self._instance

        if restore_option.get('copy_precedence') is None:
            restore_option['copy_precedence'] = 0

        if restore_option.get('overwrite') is not None:
            restore_option['unconditional_overwrite'] = restore_option['overwrite']

        if restore_option.get('live_browse'):
            restore_option['liveBrowse'] = True
        else:
            restore_option['liveBrowse'] = False

        # restore_option should use client key for destination client info
        client = restore_option.get("client", self._agent_object._client_object)

        if isinstance(client, str):
            client = self._commcell_object.clients.get(client)

        restore_option["client_name"] = client.client_name
        restore_option["client_id"] = int(client.client_id)

        # set time zone
        from_time = restore_option.get("from_time", None)
        to_time = restore_option.get("to_time", None)
        time_list = ['01/01/1970 00:00:00', '1/1/1970 00:00:00']

        if from_time and from_time not in time_list:
            restore_option["from_time"] = from_time

        if to_time and to_time not in time_list:
            restore_option["to_time"] = to_time

        self._restore_browse_option_json(restore_option)
        self._restore_common_options_json(restore_option)
        self._restore_destination_json(restore_option)
        self._restore_fileoption_json(restore_option)
        self._restore_common_opts_json(restore_option)

        if not restore_option.get('index_free_restore', False):
            if restore_option.get("paths") == []:
                raise SDKException('Subclient', '104')

        request_json = {
            "taskInfo": {
                "associations": [self._restore_association],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 1
                },
                "subTasks": [{
                    "subTask": {
                        "subTaskType": 3,
                        "operationType": 1001
                    },
                    "options": {
                        "restoreOptions": {
                            "sharePointDocRstOption": {
                                "isWorkflowAlertsRestoreOnly": False
                            },
                            "browseOption": self._browse_restore_json,
                            "commonOptions": self._commonoption_restore_json,
                            "destination": self._destination_restore_json,
                            "fileOption": self._fileoption_restore_json,
                            "sharePointRstOption": {
                                "sharePointDocument": True,
                                "spRestoreToDisk": {
                                    "restoreToDiskPath": "",
                                    "restoreToDisk": False
                                }
                            },
                        },
                        "commonOpts": self._commonopts_restore_json
                    }
                }]
            }
        }
        return request_json

