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

from ..exception import SDKException
from ..instance import Instance


class SharepointInstance(Instance):
    """
    Represents a SharePoint instance and provides operations for managing and restoring SharePoint data.

    This class is designed to handle various restore operations on a SharePoint instance, including
    generating and processing JSON configurations for restore options, destinations, and browsing.
    It encapsulates the logic required to prepare and manage restore-related data structures for
    SharePoint environments.

    Key Features:
        - Generate and process JSON for restore browse options
        - Handle common restore options in JSON format
        - Manage restore destination configurations as JSON
        - Provide comprehensive restore JSON data for SharePoint
        - Support legacy and versioned restore JSON formats

    #ai-gen-doc
    """

    def _restore_browse_option_json(self, value: dict) -> None:
        """Set the browse options for restore operations in JSON format.

        Args:
            value: A dictionary containing the browse options to be used during restore.

        #ai-gen-doc
        """

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

    def _restore_common_options_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing the common options to be set in the restore JSON.

        #ai-gen-doc
        """
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

    def _restore_destination_json(self, value: dict) -> None:
        """Set the destination restore option in the restore JSON configuration.

        Args:
            value: A dictionary containing the destination restore options to be set in the restore JSON.

        #ai-gen-doc
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._destination_restore_json = {
            "inPlace": value.get("in_place", True),
            "destClient": {
                "clientName": value.get("client_name", ""),
                "clientId": value.get("client_id", -1)
            }
        }

    def _restore_json(self, **kwargs) -> dict:
        """Create the JSON dictionary required for a SharePoint restore job.

        This method constructs the parameters needed to initiate a restore job for SharePoint sites or webs.
        The primary input is a list of paths specifying the SharePoint sites, webs, or lists to be restored.

        Keyword Args:
            paths (list of str): List of SharePoint site or web paths to restore.
                Example:
                    [
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Shared Documents\\TestFolder",
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Lists\\TestList",
                    ]
            Additional keyword arguments may be provided as needed for restore customization.

        Returns:
            dict: A dictionary containing the parameters required for a SharePoint restore job.

        Example:
            >>> instance = SharepointInstance()
            >>> restore_json = instance._restore_json(
            ...     paths=[
            ...         "MB\\https://tenant.sharepoint.com/sites/SiteA\\/\\Shared Documents\\Folder1",
            ...         "MB\\https://tenant.sharepoint.com/sites/SiteA\\/\\Lists\\List1"
            ...     ]
            ... )
            >>> print(restore_json)
            # The output will be a dictionary with restore job parameters.

        #ai-gen-doc
        """
        if kwargs.get("v1", False):
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

    def _restore_v1_json(self, **kwargs) -> dict:
        """Create the JSON payload required for a restore job for a v1 SharePoint client.

        This method constructs a dictionary containing the parameters necessary to initiate
        a restore job for SharePoint v1 clients. The primary input is a list of site or web
        paths to be restored, provided via the 'paths' keyword argument.

        Keyword Args:
            paths (list of str): List of SharePoint site or web paths to restore.
                Example:
                    [
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Shared Documents\\TestFolder",
                        "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\/\\Lists\\TestList",
                    ]

        Returns:
            dict: A dictionary containing the parameters required for the restore job.

        Example:
            >>> instance = SharepointInstance()
            >>> restore_json = instance._restore_v1_json(
            ...     paths=[
            ...         "MB\\https://tenant.sharepoint.com/sites/SiteA\\/\\Shared Documents\\Folder1",
            ...         "MB\\https://tenant.sharepoint.com/sites/SiteA\\/\\Lists\\List1"
            ...     ]
            ... )
            >>> print(restore_json)
            # The returned dictionary can be used to submit a restore job request.

        #ai-gen-doc
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
            if not restore_option.get("paths"):
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
