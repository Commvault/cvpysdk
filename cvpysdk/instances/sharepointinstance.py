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
                        "MB\\https://cvdevtenant.sharepoint.com/sites/TestSite\\/\\Shared Documents\\TestFolder",
                        "MB\\https://cvdevtenant.sharepoint.com/sites/TestSite\\/\\Lists\\TestList",
                        ]
        Returns:

            rest_json  (dict)  --  dictionary with parameters set required for a restore job

        """
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
