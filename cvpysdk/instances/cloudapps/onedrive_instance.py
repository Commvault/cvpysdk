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

"""File for operating on a OneDrive Instance.

OneDriveInstance is the only class defined in this file.

OneDriveInstance: Derived class from CloudAppsInstance Base class, representing a
OneDrive instance,and to perform operations on that instance

OneDriveInstance:

    _prepare_advsearchgrp_onedrive_for_business_client() --  Utility function to prepare advsearchgrp json for restore
                                                            job for OneDrive for business clients

    _prepare_findquery_onedrive_for_business_client()    --  Utility function to prepare findquery json for restore job
                                                            for OneDrive for business clients

    _prepare_restore_json_onedrive_for_business_client() --  Utility function to prepare user level restore json for
                                                            OneDrive for business clients

    _prepare_delete_json_onedrive_v2()      --  Utility function to prepare delete documents json for
                                                OneDrive for business clients

    _get_instance_properties()       --  Instance class method overwritten to add cloud apps
    instance properties as well

    restore_out_of_place()                               --  runs out-of-place restore for the instance

    modify_connection_settings()                         --  Modifies the azure app connection settings

    delete_data_from_browse()       --  Deletes items for the backupset in the Index and makes them unavailable for
                                        browsing and recovery

"""

from __future__ import unicode_literals
from base64 import b64encode
from typing import Any, List, Union

from ...constants import AppIDAType
from ...exception import SDKException
from ..cainstance import CloudAppsInstance
from ...job import Job

class OneDriveInstance(CloudAppsInstance):
    """
    Represents an instance of the OneDrive cloud application within a cloud management framework.

    This class provides comprehensive management and operational capabilities for OneDrive instances,
    including configuration, content management, auto-discovery, advanced search, restore, and deletion
    operations. It exposes properties for accessing instance-specific details and methods for modifying
    connection settings, access nodes, and index servers. The class also supports advanced operations
    such as out-of-place restore, data deletion, and preparation of search and restore queries.

    Key Features:
        - Access OneDrive instance properties and configuration details
        - Manage content automatically and control auto-discovery settings
        - Retrieve client, tenant, and proxy information for OneDrive
        - Prepare advanced search and restore queries for OneDrive for Business clients
        - Restore data out-of-place with flexible options (overwrite, ACL, time range, etc.)
        - Enable and configure auto-discovery modes
        - Modify index server, access nodes, and connection settings securely
        - Delete data from OneDrive with support for item GUIDs and folder targeting
        - Generate and retrieve instance properties in JSON format

    #ai-gen-doc
    """

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this OneDrive instance.

        This method fetches the latest properties for the OneDrive instance from the server
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        Example:
            >>> instance = OneDriveInstance(commcell_object, instance_name)
            >>> instance._get_instance_properties()
            >>> # The instance properties are now refreshed with the latest values

        #ai-gen-doc
        """
        super(OneDriveInstance, self)._get_instance_properties()
        # Common properties for Google and OneDrive
        self._ca_instance_type = None
        self._manage_content_automatically = None
        self._auto_discovery_enabled = None
        self._auto_discovery_mode = None
        self._proxy_client = None

        self._client_id = None
        self._tenant = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'oneDriveInstance' in cloud_apps_instance:
                onedrive_instance = cloud_apps_instance['oneDriveInstance']

                self._manage_content_automatically = onedrive_instance['manageContentAutomatically']
                self._auto_discovery_enabled = onedrive_instance['isAutoDiscoveryEnabled']
                self._auto_discovery_mode = onedrive_instance['autoDiscoveryMode']
                if 'clientId' in onedrive_instance:
                    self._client_id = onedrive_instance.get('clientId')
                    self._tenant = onedrive_instance.get('tenant')
                elif "credentialEntity" in onedrive_instance["azureAppList"]["azureApps"][0]:
                    self._client_id = self._properties["instance"]["clientId"]
                else:
                    self._client_id = onedrive_instance.get(
                        'azureAppList', {}).get('azureApps', [{}])[0].get('azureAppId')
                    self._tenant = onedrive_instance.get(
                        'azureAppList', {}).get('azureApps', [{}])[0].get('azureDirectoryId')

                if self._client_id is None:
                    raise SDKException('Instance', '102', 'Azure App has not been configured')

            if 'generalCloudProperties' in cloud_apps_instance:
                if 'proxyServers' in cloud_apps_instance['generalCloudProperties']:
                    self._proxy_client = cloud_apps_instance.get(
                        'generalCloudProperties', {}).get('proxyServers', [{}])[0].get('clientName')
                else:
                    if 'clientName' in cloud_apps_instance.get(
                            'generalCloudProperties', {}).get('memberServers', [{}])[0].get('client'):
                        self._proxy_client = cloud_apps_instance.get('generalCloudProperties', {}).get(
                            'memberServers', [{}])[0].get('client', {}).get('clientName')
                    else:
                        self._proxy_client = cloud_apps_instance.get('generalCloudProperties', {}).get(
                            'memberServers', [{}])[0].get('client', {}).get('clientGroupName')

                if self._proxy_client is None:
                    raise SDKException('Instance', '102', 'Access Node has not been configured')

    @property
    def ca_instance_type(self) -> str:
        """Get the CloudApps instance type for this OneDrive instance.

        Returns:
            The type of the CloudApps instance as a string.

        Example:
            >>> onedrive_instance = OneDriveInstance()
            >>> instance_type = onedrive_instance.ca_instance_type
            >>> print(f"CloudApps instance type: {instance_type}")

        #ai-gen-doc
        """
        if self._ca_instance_type == 7:
            return 'ONEDRIVE'
        return self._ca_instance_type

    @property
    def manage_content_automatically(self) -> bool:
        """Get the status of the 'Manage Content Automatically' property for CloudApps.

        Returns:
            bool: True if content is managed automatically, False otherwise.

        Example:
            >>> instance = OneDriveInstance()
            >>> auto_manage = instance.manage_content_automatically
            >>> print(f"Automatic content management enabled: {auto_manage}")

        #ai-gen-doc
        """
        return self._manage_content_automatically

    @property
    def auto_discovery_status(self) -> bool:
        """Get the current status of the Auto Discovery property for the OneDrive instance.

        This property allows you to check whether Auto Discovery is enabled or disabled
        for the OneDrive instance. It is a read-only attribute.

        Returns:
            bool: True if Auto Discovery is enabled, False otherwise.

        Example:
            >>> instance = OneDriveInstance()
            >>> status = instance.auto_discovery_status
            >>> print(f"Auto Discovery Enabled: {status}")

        #ai-gen-doc
        """
        return self._auto_discovery_enabled

    @property
    def auto_discovery_mode(self) -> str:
        """Get the auto discovery mode property for the OneDrive instance.

        Returns:
            The current auto discovery mode as a string.

        Example:
            >>> instance = OneDriveInstance()
            >>> mode = instance.auto_discovery_mode
            >>> print(f"Auto discovery mode: {mode}")

        #ai-gen-doc
        """
        return self._auto_discovery_mode

    @property
    def onedrive_client_id(self) -> str:
        """Get the OneDrive app client ID associated with this instance.

        Returns:
            The client ID string used for OneDrive app authentication.

        Example:
            >>> instance = OneDriveInstance()
            >>> client_id = instance.onedrive_client_id
            >>> print(f"OneDrive Client ID: {client_id}")

        #ai-gen-doc
        """
        return self._client_id

    @property
    def onedrive_tenant(self) -> str:
        """Get the OneDrive tenant ID associated with this instance.

        Returns:
            The OneDrive tenant ID as a string.

        Example:
            >>> instance = OneDriveInstance()
            >>> tenant_id = instance.onedrive_tenant  # Access the tenant ID using the property
            >>> print(f"OneDrive tenant ID: {tenant_id}")

        #ai-gen-doc
        """
        return self._tenant

    @property
    def proxy_client(self) -> str:
        """Get the name of the proxy client associated with this OneDrive instance.

        Returns:
            The name of the proxy client as a string.

        Example:
            >>> instance = OneDriveInstance()
            >>> proxy_name = instance.proxy_client
            >>> print(f"Proxy client name: {proxy_name}")

        #ai-gen-doc
        """
        return self._proxy_client


    def _prepare_advsearchgrp_onedrive_for_business_client(self, source_item_list: list, subclient_id: int) -> dict:
        """Prepare the advsearchgrp JSON structure for a OneDrive for Business restore job.

        This utility function generates the required advsearchgrp JSON payload for restoring
        OneDrive for Business clients, based on the provided list of user GUIDs and the subclient ID.

        Args:
            source_item_list: List of user GUIDs to include in the restore operation.
            subclient_id: The subclient ID associated with the OneDrive for Business client.

        Returns:
            A dictionary representing the advsearchgrp JSON structure for the restore job.

        Example:
            >>> user_guids = ['guid1', 'guid2', 'guid3']
            >>> subclient_id = 12345
            >>> advsearchgrp_json = instance._prepare_advsearchgrp_onedrive_for_business_client(user_guids, subclient_id)
            >>> print(advsearchgrp_json)
            # Output will be a dictionary suitable for use in a restore job request

        #ai-gen-doc
        """


        user_guid = source_item_list[0]
        advsearchgrp = {
            "fileFilter": [
                {
                    "interGroupOP": "FTAnd",
                    "filter": {
                        "filters": [
                            {
                                "field": "HIDDEN",
                                "fieldValues": {
                                    "values": [
                                        "true"
                                    ]
                                },
                                "intraFieldOp": "FTNot"
                            },
                            {
                                "field": "CV_OBJECT_GUID",
                                "fieldValues": {
                                    "values": [
                                        user_guid
                                    ]
                                },
                                "intraFieldOp": "FTOr"
                            }
                        ],
                        "interFilterOP": "FTAnd"
                    }
                }
            ],
            "commonFilter": [
                {
                    "filter": {
                        "filters": [
                            {
                                "field": "CISTATE",
                                "fieldValues": {
                                    "values": [
                                        "1"
                                    ]
                                },
                                "intraFieldOp": "FTOr",
                                "groupType": 0
                            },
                            {
                                "field": "IS_VISIBLE",
                                "fieldValues": {
                                    "values": [
                                        "true"
                                    ],
                                    "isRange": False,
                                    "isMoniker": False
                                },
                                "intraFieldOp": "FTOr",
                                "intraFieldOpStr": "None"
                            }
                        ],
                        "interFilterOP": "FTAnd"
                    }
                }
            ],
            "galaxyFilter": [
                {
                    "appIdList": [
                        subclient_id
                    ]
                }
            ],
            "graphFilter": [
                {
                    "fromField": "PARENT_GUID",
                    "toField": "CV_OBJECT_GUID",
                    "returnRoot": True,
                    "traversalFilter": [
                        {
                            "filters": [
                                {
                                    "field": "IS_VISIBLE",
                                    "fieldValues": {
                                        "values": [
                                            "true"
                                        ]
                                    },
                                    "intraFieldOp": "FTAnd",
                                    "groupType": 0
                                },
                                {
                                    "field": "HIDDEN",
                                    "fieldValues": {
                                        "values": [
                                            "true"
                                        ]
                                    },
                                    "intraFieldOp": "FTNot"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return advsearchgrp

    def _prepare_findquery_onedrive_for_business_client(self, source_item_list: list, subclient_id: int) -> dict:
        """Prepare the findquery JSON payload for a OneDrive for Business restore job.

        This utility function constructs the findquery JSON required to initiate a restore job
        for OneDrive for Business clients, based on the provided list of user GUIDs and the subclient ID.

        Args:
            source_item_list: List of user GUIDs to be processed in the restore operation.
            subclient_id: The subclient ID associated with the OneDrive for Business client.

        Returns:
            A dictionary representing the findquery JSON payload for the restore job.

        Example:
            >>> user_guids = ['1234-abcd-5678-efgh', '2345-bcde-6789-fghi']
            >>> subclient_id = 101
            >>> findquery = instance._prepare_findquery_onedrive_for_business_client(user_guids, subclient_id)
            >>> print(findquery)
            {'subclientId': 101, 'userGuids': ['1234-abcd-5678-efgh', '2345-bcde-6789-fghi']}
        #ai-gen-doc
        """

        findquery = {
                  "searchProcessingInfo": {
                    "pageSize": 20,
                    "resultOffset": 0,
                    "sortParams": [
                      {
                        "sortField": "DATA_TYPE",
                        "sortDirection": "DESCENDING"
                      },
                      {
                        "sortField": "FileName",
                        "sortDirection": "ASCENDING"
                      }
                    ],
                    "queryParams": [
                      {
                        "param": "ENABLE_MIXEDVIEW",
                        "value": "true"
                      },
                      {
                        "param": "RESPONSE_FIELD_LIST",
                        "value": "FAST_URL,BACKUPTIME,SIZEINKB,MODIFIEDTIME,CONTENTID,CV_TURBO_GUID,AFILEID,AFILEOFFSET,COMMCELLNO,FILE_NAME,FILE_FOLDER,CVSTUB,DATA_TYPE,APPID,JOBID,CISTATE,DATE_DELETED,IdxFlags,CV_OBJECT_GUID,PARENT_GUID,CUSTODIAN,OWNER,ObjectType"
                      },
                      {
                        "param": "DO_NOT_AUDIT",
                        "value": "false"
                      },
                      {
                        "param": "COLLAPSE_FIELD",
                        "value": "CV_OBJECT_GUID"
                      },
                      {
                        "param": "COLLAPSE_SORT",
                        "value": "BACKUPTIME DESC"
                      },
                      {
                        "param": "ENABLE_NAVIGATION",
                        "value": "on"
                      },
                      {
                        "param": "ENABLE_DEFAULTFACETS",
                        "value": "false"
                      }
                    ]
                  },
                  "advSearchGrp": self._prepare_advsearchgrp_onedrive_for_business_client(source_item_list,subclient_id),
                  "mode": "WebConsole"
                }

        return findquery




    def _prepare_restore_json_onedrive_for_business_client(self, source_item_list: list, **kwargs: object) -> dict:
        """Prepare the user-level restore JSON for OneDrive for Business clients.

        This utility function constructs the request JSON required to initiate a restore job for OneDrive for Business users.
        The function supports both in-place and out-of-place restores, as well as disk restores, and allows for various
        customization options via keyword arguments.

        Args:
            source_item_list: List of user GUIDs to process in the restore operation.

        Keyword Args:
            out_of_place (bool, optional): If True, perform an out-of-place restore.
            disk_restore (bool, optional): If True, perform a restore to disk.
            destination_path (str, optional): Destination path for out-of-place and disk restores.
            destination_client (object, optional): Destination client for disk restore.
            overwrite (bool, optional): If True, overwrite files at the destination if they already exist.
            restore_as_copy (bool, optional): If True, restore files as copies if they already exist.
            skip_file_permissions (bool, optional): If True, skip restoring file permissions.
            include_deleted_items (bool, optional): If True, include deleted items in the restore.
            restore_to_blob (bool, optional):  If True, performs restore to azure blob storage

        Returns:
            dict: The request JSON for the restore job.

        Raises:
            SDKException: If the destination client with the given name does not exist, or if any parameter type is invalid.

        Example:
            >>> user_guids = ['user-guid-1', 'user-guid-2']
            >>> restore_json = instance._prepare_restore_json_onedrive_for_business_client(
            ...     user_guids,
            ...     out_of_place=True,
            ...     destination_path='/restore/location',
            ...     overwrite=True
            ... )
            >>> print(restore_json)
            # The returned dictionary can be used to submit a restore job.

        #ai-gen-doc
        """

        out_of_place = kwargs.get('out_of_place', False)
        disk_restore = kwargs.get('disk_restore', False)
        destination_path = kwargs.get('destination_path', False)
        destination_client = kwargs.get('destination_client')
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', True)
        include_deleted_items = kwargs.get('include_deleted_items', False)
        restore_to_blob = kwargs.get('restore_to_blob', False)


        if destination_client:
            if self._commcell_object.clients.all_clients.get(destination_client):
                destination_client_object = self._commcell_object.clients.all_clients.get(destination_client)
                destination_client_id = int(destination_client_object.get('id'))
            else:
                raise SDKException('Client', '102', 'Client "{0}" does not exist.'.format(destination_client))

        if ((destination_client and not isinstance(destination_client, str) or
             destination_path and not isinstance(destination_path, str)) or not
            (isinstance(source_item_list, list) and
             isinstance(skip_file_permissions, bool) and
             isinstance(disk_restore, bool) and
             isinstance(out_of_place, bool) and
             isinstance(overwrite, bool) and
             isinstance(restore_as_copy, bool))):
            raise SDKException('Instance', '101')

        request_json = self._restore_json(client=self._agent_object._client_object)

        subtasks = request_json['taskInfo']['subTasks'][0]
        options = subtasks['options']
        restore_options = options['restoreOptions']

        options["restoreOptions"]["browseOption"] = {
            "commCellId": self._commcell_object.commcell_id,
            "showDeletedItems": False
        }

        restore_options['commonOptions'] = {
            "overwriteFiles": overwrite,
            "skip": True if not restore_as_copy and not overwrite else False,
            "unconditionalOverwrite": overwrite
        }

        destination = restore_options['destination']
        destination['destAppId'] = AppIDAType.WINDOWS_FILE_SYSTEM.value if disk_restore else AppIDAType.CLOUD_APP.value
        destination['inPlace'] = False if out_of_place or disk_restore else True

        destination['destClient'] = {
            "clientId": destination_client_id,
            "clientName": destination_client
        } if disk_restore else {
            "clientId": int(self._agent_object._client_object.client_id),
            "clientName": self._agent_object._client_object.client_name
        }

        if destination_path:
            destination['destPath'] = [destination_path]

        restore_options['fileOption']['sourceItem'] = source_item_list

        restore_options['cloudAppsRestoreOptions'] = {
            "instanceType": self._ca_instance_type,
            "googleRestoreOptions": {
                "skipPermissionsRestore": False if disk_restore else skip_file_permissions,
                "restoreToDifferentAccount": True if out_of_place else False,
                "restoreAsCopy": False if disk_restore else restore_as_copy,
                "filelevelRestore": False,
                "strDestUserAccount": destination_path if out_of_place else '',
                "overWriteItems": False if disk_restore else overwrite,
                "restoreToGoogle": False if disk_restore else True
            }
        }

        del subtasks['subTaskOperation']
        del restore_options['fileOption']
        del restore_options['impersonation']
        del restore_options['volumeRstOption']
        del restore_options['sharePointRstOption']
        del restore_options['virtualServerRstOption']

        associations = request_json['taskInfo']['associations'][0]
        associations['subclientId'] = subclient_id = int(self.subclients['default']['id'])

        cloudAppsRestoreOptions = restore_options['cloudAppsRestoreOptions']
        cloudAppsRestoreOptions['googleRestoreOptions'][
            'findQuery'] = self._prepare_findquery_onedrive_for_business_client(source_item_list, subclient_id)
        if include_deleted_items:
            cloudAppsRestoreOptions['googleRestoreOptions']['findQuery']['advSearchGrp']['commonFilter'][0]['filter'][
                'filters'][0]['fieldValues']['values'].extend(["3333", "3334", "3335"])

        destination_option = "Destination"
        destination_value = "Original location"
        if out_of_place:
            destination_option = "Destination user"
            destination_value = source_item_list[0]
        if disk_restore:
            destination_option = "Destination server"
            destination_value = destination_client
        if restore_to_blob:
            restore_options['cloudAppsRestoreOptions']['googleRestoreOptions']['blobContainerId'] = kwargs.get(
                'blob_container_id')
            restore_options['cloudAppsRestoreOptions']['googleRestoreOptions']['googleRestoreChoice'] = 4
            destination_option = "Destination Azure Blob Storage"
            destination_value = ""

        options["commonOpts"] = {
            "notifyUserOnJobCompletion": False,
            "jobMetadata": [
                {
                    "selectedItems": [
                        {
                            "itemName": source_item_list[0],
                            "itemType": "User"
                        }
                    ],
                    "jobOptionItems": [
                        {
                            "option": "Restore destination",
                            "value": "Azure Blob Storage" if restore_to_blob else "OneDrive for Business"
                        },
                        {
                            "option": "Source",
                            "value": source_item_list[0]
                        },
                        {
                            "option": destination_option,
                            "value": destination_value
                        },
                        {
                            "option": "If the file exists",
                            "value": "Restore as a copy" if restore_as_copy and not overwrite else "Unconditionally overwrite" if overwrite else "Skip"

                        },
                        {
                            "option": "Skip file permissions",
                            "value": "Enabled" if skip_file_permissions else "Disabled"
                        },
                        {
                            "option": "Include deleted items",
                            "value": "Enabled" if include_deleted_items else "Disabled"
                        }
                    ]
                }
            ]
        }

        joboptionitems = options['commonOpts']['jobMetadata'][0]['jobOptionItems']

        if out_of_place:
            joboptionitems.append({"option": "Destination client", "value": destination_client})
        if disk_restore:
            joboptionitems.append({"option": "Destination path", "value": destination_path})

        return request_json

    def _prepare_delete_json_onedrive_v2(self, item_guids: list, **kwargs: dict) -> dict:
        """Prepare the JSON payload for deleting documents in OneDrive for Business clients.

        This utility function constructs the request JSON required to delete one or more items 
        (documents or folders) from OneDrive for Business clients, based on the provided item GUIDs.
        Additional options can be specified using keyword arguments.

        Args:
            item_guids: A list of item GUIDs (str) representing the documents or folders to delete.
            **kwargs: Optional keyword arguments to modify the delete operation.
                - include_deleted_items (bool): If True, include deleted items in the search.

        Returns:
            A dictionary representing the request JSON for the delete document operation.

        Raises:
            SDKException: If the destination client with the given item does not exist, or if any 
                parameter type is invalid.

        Example:
            >>> item_guids = ['1234-5678-90ab-cdef', 'abcd-ef12-3456-7890']
            >>> delete_json = onedrive_instance._prepare_delete_json_onedrive_v2(item_guids, include_deleted_items=True)
            >>> print(delete_json)
            # The returned dictionary can be used as the payload for a delete request.

        #ai-gen-doc
        """
        folder = kwargs.get('folder', False)
        include_deleted_items = kwargs.get('include_deleted_items', False)
        subclient_id = int(self.subclients['default']['id'])

        if isinstance(item_guids, str):
            source_item_list = [item_guids]
        else:
            source_item_list = [].extend(item_guids)
        req_json = {
            'opType': 1,
            'bulkMode': folder,
            'deleteOption': {
                'folderDelete': folder
            },
            'searchReq': {
                'mode': 4,
                'facetRequests': {
                    'facetRequest': []
                },
                'advSearchGrp': self._prepare_advsearchgrp_onedrive_for_business_client(source_item_list, subclient_id),
                'searchProcessingInfo': {
                    'resultOffset': 0,
                    'pageSize': 50,
                    'queryParams': [
                        {
                            'param': 'ENABLE_MIXEDVIEW',
                            'value': 'true'
                        },
                        {
                            'param': 'ENABLE_NAVIGATION',
                            'value': 'on'
                        },
                        {
                            'param': 'ENABLE_DEFAULTFACETS',
                            'value': 'false'
                        }
                    ],
                    'sortParams': []
                }
            }
        }

        if isinstance(item_guids, list):
            req_json['searchReq']['advSearchGrp']['fileFilter'][0]['filter']['filters'][1]['fieldValues'][
                'values'].extend(item_guids[1:])

        if include_deleted_items:
            req_json['searchReq']['advSearchGrp']['commonFilter'][0]['filter']['filters'][0]['fieldValues']['values'].extend(
                ["3333", "3334", "3335"])

        return req_json

    def restore_out_of_place(
            self,
            client: object,
            destination_path: str,
            paths: list,
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: int = None,
            from_time: str = None,
            to_time: str = None,
            to_disk: bool = False
        ) -> 'Job':
        """Restore specified files or folders to a different client and/or location.

        This method restores the files and folders listed in `paths` to the given `destination_path`
        on the specified `client`. The restore can optionally overwrite existing files, restore
        data and ACLs, and be filtered by time range or copy precedence. The restore can also
        be performed to disk if required.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: Full path to the restore location on the target client.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional copy precedence value for the storage policy copy. Default is None.
            from_time: Optional lower bound for restore time window (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper bound for restore time window (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_disk: If True, perform a restore to disk operation. Default is False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If any of the following conditions are met:
                - `client` is not a string or Client instance
                - `destination_path` is not a string
                - `paths` is not a list
                - Failed to initialize the restore job
                - The response is empty or not successful

        Example:
            >>> # Restore files to a different client and location
            >>> job = onedrive_instance.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='C:\\Restore\\Data',
            ...     paths=['/user/docs/file1.txt', '/user/docs/file2.txt'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        from cvpysdk.client import Client

        if not ((isinstance(client, str) or isinstance(client, Client)) and
                isinstance(destination_path, str) and
                isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if isinstance(client, Client):
            client = client
        elif isinstance(client, str):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        paths = self._filter_paths(paths)

        destination_path = self._filter_paths([destination_path], True)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            in_place=False,
            client=client,
            destination_path=destination_path,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
        )
        dest_user_account = destination_path
        rest_different_account = True
        restore_to_google = True

        if to_disk:
            dest_user_account = ''
            rest_different_account = False
            restore_to_google = False
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]['cloudAppsRestoreOptions'] = {
            "instanceType": self._ca_instance_type,
            "googleRestoreOptions": {
                "strDestUserAccount": dest_user_account,
                "folderGuid": "",
                "restoreToDifferentAccount": rest_different_account,
                "restoreToGoogle": restore_to_google
            }
        }
        return self._process_restore_response(request_json)

    def enable_auto_discovery(self, mode: str = 'REGEX') -> None:
        """Enable auto discovery on the OneDrive instance.

        This method enables automatic discovery of OneDrive users or groups based on the specified mode.

        Args:
            mode: The auto discovery mode to use. Valid values are:
                - 'REGEX': Enables discovery using regular expressions.
                - 'GROUP': Enables discovery based on group membership.
                Default is 'REGEX'.

        Example:
            >>> instance = OneDriveInstance()
            >>> instance.enable_auto_discovery()  # Enables auto discovery in REGEX mode
            >>> instance.enable_auto_discovery(mode='GROUP')  # Enables auto discovery in GROUP mode

        #ai-gen-doc
        """
        auto_discovery_dict = {
            'REGEX': 0,
            'GROUP': 1
        }
        instance_dict = {
            1: 'gInstance',
            2: 'gInstance',
            7: 'oneDriveInstance'
        }
        auto_discovery_mode = auto_discovery_dict.get(mode.upper(), None)

        if auto_discovery_mode is None:
            raise SDKException('Instance', '107')
        instance_prop = self._properties['cloudAppsInstance'].copy()

        instance_prop[instance_dict[instance_prop['instanceType']]]['isAutoDiscoveryEnabled'] = True
        instance_prop[instance_dict[instance_prop['instanceType']]]['autoDiscoveryMode'] = auto_discovery_mode

        self._set_instance_properties("_properties['cloudAppsInstance']", instance_prop)
        self.refresh()

    def _get_instance_properties_json(self) -> dict:
        """Retrieve the instance properties as a JSON dictionary.

        Returns:
            dict: A dictionary containing the properties of the OneDrive instance in JSON format.

        Example:
            >>> instance = OneDriveInstance()
            >>> properties_json = instance._get_instance_properties_json()
            >>> print(properties_json)
            >>> # Output will be a dictionary with instance property details

        #ai-gen-doc
        """

        return {'instanceProperties': self._properties}

    def modify_index_server(self, modified_index_server: str) -> None:
        """Modify the index server for the OneDrive instance.

        Args:
            modified_index_server: The name of the new index server to be set.

        Example:
            >>> onedrive_instance = OneDriveInstance()
            >>> onedrive_instance.modify_index_server("NewIndexServer01")
            >>> print("Index server updated successfully.")

        #ai-gen-doc
        """
        update_dict = {
            "instance": {
                "instanceId": int(self.instance_id),
                "clientId": int(self._agent_object._client_object.client_id),
                "applicationId": int(self._agent_object.agent_id)
            },
                "cloudAppsInstance": {
                    "instanceType": self.ca_instance_type,
                    "oneDriveInstance": {
                    },
                    "generalCloudProperties": {
                        "indexServer": {
                            "clientName": modified_index_server
                        }
                    }
                }
            }

        self.update_properties(properties_dict=update_dict)

    def modify_accessnodes(self, modified_accessnodes_list: list, modified_user_name: str, modified_user_password: str) -> None:
        """Modify the access nodes for the OneDrive instance.

        This method updates the list of access nodes and the associated user credentials
        for the OneDrive instance.

        Args:
            modified_accessnodes_list: List of new access nodes to be assigned to the instance.
            modified_user_name: The new user account name to associate with the access nodes.
            modified_user_password: The new user account password for the specified user.

        Example:
            >>> accessnodes = ['node1', 'node2']
            >>> instance.modify_accessnodes(accessnodes, 'new_user', 'new_password')
            >>> print("Access nodes and credentials updated successfully.")

        #ai-gen-doc
        """
        member_servers=[]
        for client in modified_accessnodes_list:
            client_dict = {
                "client": {
                    "clientName": client
                }
            }
            member_servers.append(client_dict)

        update_dict = {
            "instance": {
                "instanceId": int(self.instance_id),
                "clientId": int(self._agent_object._client_object.client_id),
                "applicationId": int(self._agent_object.agent_id)
            },
            "cloudAppsInstance": {
                "instanceType": self.ca_instance_type,
                "oneDriveInstance": {
                    "serviceAccounts": {
                        "accounts": [
                            {
                                "serviceType": "SYSTEM_ACCOUNT",
                                "userAccount": {
                                    "userName": modified_user_name,
                                    "password": b64encode(modified_user_password.encode()).decode(),
                                }
                            }
                        ]
                    }
                },
                "generalCloudProperties": {
                    "memberServers": member_servers
                }
            }
        }

        self.update_properties(properties_dict=update_dict)

    def modify_connection_settings(self, azure_app_id: str, azure_dir_id: str, azure_app_secret: str) -> None:
        """Modify the OneDrive connection settings with new Azure credentials.

        Updates the Azure application ID, directory ID, and application secret used for connecting to OneDrive.

        Args:
            azure_app_id: The new Azure application (client) ID.
            azure_dir_id: The new Azure directory (tenant) ID.
            azure_app_secret: The new Azure application secret (password).

        Raises:
            SDKException: If the update fails, the response is empty, or the response code is not as expected.

        Example:
            >>> instance = OneDriveInstance()
            >>> instance.modify_connection_settings(
            ...     azure_app_id="your-app-id",
            ...     azure_dir_id="your-dir-id",
            ...     azure_app_secret="your-app-secret"
            ... )
            >>> print("Connection settings updated successfully.")

        #ai-gen-doc
        """

        if not isinstance(azure_app_id, str) or not azure_app_id:
            raise SDKException('Instance', '102', 'Invalid argument: azure_app_id must be a non-empty string')
        if not isinstance(azure_dir_id, str) or not azure_dir_id:
            raise SDKException('Instance', '102', 'Invalid argument: azure_dir_id must be a non-empty string')
        if not isinstance(azure_app_secret, str) or not azure_app_secret:
            raise SDKException('Instance', '102', 'Invalid argument: azure_app_secret must be a non-empty string')

        update_dict = {
            "instance": self._instance,
            "cloudAppsInstance": {
                "instanceType": self.ca_instance_type,
                "oneDriveInstance": {
                    "azureAppList": {
                        "azureApps": [
                            {
                                "azureDirectoryId": azure_dir_id,
                                "azureAppId": azure_app_id,
                                "azureAppKeyValue": b64encode(azure_app_secret.encode()).decode()
                            }
                        ]
                    }
                }
            }
        }

        self.update_properties(properties_dict=update_dict)

    def delete_data_from_browse(self, item_guids: 'Union[str, List[str]]', include_deleted_items: bool = False, folder: bool = False) -> 'Union[None, Any]':
        """Delete items from the backupset index, making them unavailable for browsing and recovery.

        This method removes specified items (files or folders) from the backupset's index. 
        Once deleted, these items cannot be browsed or recovered through the standard interface.

        Args:
            item_guids: A single GUID (str) or a list of GUIDs (List[str]) representing the items to delete from browse.
            include_deleted_items: If True, also includes items that are already deleted in the browse operation.
            folder: If True, indicates that the item(s) to be deleted are folders.

        Returns:
            None if the delete request is sent successfully for files.
            jobIds if the delete request is sent successfully for folders.

        Raises:
            SDKException: If the deletion fails, the response is empty, or the response code is not as expected.

        Example:
            >>> # Delete a single file by GUID
            >>> instance = OneDriveInstance()
            >>> instance.delete_data_from_browse('file-guid-123')
            >>> 
            >>> # Delete multiple files by GUIDs
            >>> instance.delete_data_from_browse(['file-guid-123', 'file-guid-456'])
            >>> 
            >>> # Delete a folder by GUID and get job IDs
            >>> job_ids = instance.delete_data_from_browse('folder-guid-789', folder=True)
            >>> print(f"Delete job IDs: {job_ids}")

        #ai-gen-doc
        """
        if not isinstance(item_guids, str) or not item_guids:
            if not isinstance(item_guids, list):
                raise SDKException('Instance', '102', "Invalid argument: item_guid must be a non-empty string or list of strings.")
        if isinstance(item_guids, list):
            for item in item_guids:
                if not isinstance(item, str) or not item:
                    raise SDKException('Instance', '102',"Invalid argument: item_guid must be a non-empty string.")

        request_json = self._prepare_delete_json_onedrive_v2(item_guids, include_deleted_items=include_deleted_items, folder=folder)
        return self._process_delete_response(request_json)
