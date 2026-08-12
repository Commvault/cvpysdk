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

"""File for operating on a Google Instance.

GoogleInstance is the only class defined in this file.

GoogleInstance: Derived class from CloudAppsInstance Base class, representing a
Google (GMail/GDrive) and OneDrive instance,
and to perform operations on that instance

GoogleInstance:

    _prepare_restore_json_v2()  --  Utility function to prepare user level restore json for
                                    OneDrive for bussiness clients

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
    instance properties as well

    restore_out_of_place()      --  runs out-of-place restore for the instance

    modify_index_server()       --  Method to modify the index server

    modify_accessnodes()        --  Method to modify accessnodes

"""

from __future__ import unicode_literals
from base64 import b64encode
from typing import Any, Dict, List

from ...constants import AppIDAType
from ...exception import SDKException
from ..cainstance import CloudAppsInstance
from ...job import Job

class GoogleInstance(CloudAppsInstance):
    """
    Represents an instance of a GMail/GDrive cloud application.

    This class provides comprehensive management and configuration capabilities
    for Google cloud application instances, including GMail and GDrive. It
    exposes properties for accessing instance-specific details such as email IDs,
    admin credentials, client IDs, and key file paths. The class also supports
    advanced operations such as auto-discovery management, content automation,
    index server modification, access node configuration, and data restoration.

    Key Features:
        - Retrieve and manage instance properties and configuration as JSON
        - Access instance details via properties (email ID, admin ID, client IDs, key file path, etc.)
        - Manage auto-discovery status and modes
        - Enable or modify automatic content management
        - Prepare advanced search and find queries for data operations
        - Prepare restore operations and JSON payloads
        - Restore data out-of-place with flexible options (ACL, overwrite, time range, disk)
        - Modify index server and access nodes for the instance
        - Proxy client management for network operations

    #ai-gen-doc
    """

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this GoogleInstance.

        This method fetches the latest properties for the current instance from the backend
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response from the backend is empty or indicates a failure.

        Example:
            >>> instance = GoogleInstance()
            >>> instance._get_instance_properties()
            >>> # The instance properties are now refreshed

        #ai-gen-doc
        """
        super(GoogleInstance, self)._get_instance_properties()
        # Common properties for Google and OneDrive
        self._ca_instance_type = None
        self._manage_content_automatically = None
        self._auto_discovery_enabled = None
        self._auto_discovery_mode = None
        self._proxy_client = None

        # Google instance related properties
        self._app_email_id = None
        self._google_admin_id = None
        self._service_account_key_file = None
        self._app_client_id = None

        # OneDrive instance related properties
        self._client_id = None
        self._tenant = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'gInstance' in cloud_apps_instance:
                ginstance = cloud_apps_instance['gInstance']

                self._manage_content_automatically = ginstance['manageContentAutomatically']
                self._auto_discovery_enabled = ginstance['isAutoDiscoveryEnabled']
                self._auto_discovery_mode = ginstance['autoDiscoveryMode']
                self._app_email_id = ginstance['appEmailId']
                self._google_admin_id = ginstance['emailId']
                self._service_account_key_file = ginstance['appKey']
                self._app_client_id = ginstance['appClientId']

            if 'oneDriveInstance' in cloud_apps_instance:
                onedrive_instance = cloud_apps_instance['oneDriveInstance']

                self._manage_content_automatically = onedrive_instance['manageContentAutomatically']
                self._auto_discovery_enabled = onedrive_instance['isAutoDiscoveryEnabled']
                self._auto_discovery_mode = onedrive_instance['autoDiscoveryMode']
                if 'clientId' in onedrive_instance:
                    self._client_id = onedrive_instance.get('clientId')
                    self._tenant = onedrive_instance.get('tenant')
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
        """Get the CloudApps instance type for this GoogleInstance.

        Returns:
            The instance type as a string, representing the CloudApps configuration.

        Example:
            >>> google_instance = GoogleInstance()
            >>> instance_type = google_instance.ca_instance_type  # Use dot notation for property
            >>> print(f"CloudApps instance type: {instance_type}")

        #ai-gen-doc
        """
        if self._ca_instance_type == 1:
            return 'GMAIL'
        elif self._ca_instance_type == 2:
            return 'GDRIVE'
        elif self._ca_instance_type == 7:
            return 'ONEDRIVE'
        return self._ca_instance_type

    @property
    def manage_content_automatically(self) -> bool:
        """Get the status of the 'Manage Content Automatically' property for the CloudApps instance.

        Returns:
            bool: True if content is managed automatically, False otherwise.

        Example:
            >>> google_instance = GoogleInstance()
            >>> is_auto = google_instance.manage_content_automatically
            >>> print(f"Manage Content Automatically: {is_auto}")

        #ai-gen-doc
        """
        return self._manage_content_automatically

    @property
    def auto_discovery_status(self) -> bool:
        """Get the current status of the Auto Discovery property for the GoogleInstance.

        Returns:
            bool: True if Auto Discovery is enabled, False otherwise.

        Example:
            >>> google_instance = GoogleInstance()
            >>> status = google_instance.auto_discovery_status
            >>> print(f"Auto Discovery Enabled: {status}")

        #ai-gen-doc
        """
        return self._auto_discovery_enabled

    @property
    def auto_discovery_mode(self) -> bool:
        """Get the auto discovery mode status for the GoogleInstance.

        Returns:
            bool: True if auto discovery mode is enabled, False otherwise.

        Example:
            >>> instance = GoogleInstance()
            >>> is_enabled = instance.auto_discovery_mode
            >>> print(f"Auto discovery mode enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._auto_discovery_mode

    @property
    def app_email_id(self) -> str:
        """Get the service account email ID associated with this Google instance.

        Returns:
            The service account email address as a string.

        Example:
            >>> google_instance = GoogleInstance()
            >>> email_id = google_instance.app_email_id
            >>> print(f"Service account email: {email_id}")

        #ai-gen-doc
        """
        return self._app_email_id

    @property
    def google_admin_id(self) -> str:
        """Get the Google admin email ID associated with this GoogleInstance.

        Returns:
            The Google admin email ID as a string.

        Example:
            >>> instance = GoogleInstance()
            >>> admin_email = instance.google_admin_id  # Use dot notation for property access
            >>> print(f"Google admin email: {admin_email}")

        #ai-gen-doc
        """
        return self._google_admin_id

    @property
    def key_file_path(self) -> str:
        """Get the file path to the Google service account key.

        Returns:
            The full path to the service account key file as a string.

        Example:
            >>> instance = GoogleInstance()
            >>> key_path = instance.key_file_path  # Use dot notation for property access
            >>> print(f"Service account key file is located at: {key_path}")

        #ai-gen-doc
        """
        return self._service_account_key_file

    @property
    def google_client_id(self) -> str:
        """Get the service account client ID associated with this Google instance.

        Returns:
            The client ID string for the service account.

        Example:
            >>> google_instance = GoogleInstance()
            >>> client_id = google_instance.google_client_id  # Access the property
            >>> print(f"Service account client ID: {client_id}")

        #ai-gen-doc
        """
        return self._app_client_id

    @property
    def onedrive_client_id(self) -> str:
        """Get the OneDrive application client ID associated with this GoogleInstance.

        Returns:
            The client ID string used for OneDrive app authentication.

        Example:
            >>> google_instance = GoogleInstance()
            >>> client_id = google_instance.onedrive_client_id
            >>> print(f"OneDrive Client ID: {client_id}")

        #ai-gen-doc
        """
        return self._client_id

    @property
    def onedrive_tenant(self) -> str:
        """Get the OneDrive tenant ID associated with this GoogleInstance.

        Returns:
            The OneDrive tenant ID as a string.

        Example:
            >>> instance = GoogleInstance()
            >>> tenant_id = instance.onedrive_tenant
            >>> print(f"OneDrive Tenant ID: {tenant_id}")

        #ai-gen-doc
        """
        return self._tenant

    @property
    def proxy_client(self) -> str:
        """Get the proxy client name associated with this GoogleInstance.

        Returns:
            The name of the proxy client as a string.

        Example:
            >>> instance = GoogleInstance()
            >>> proxy_name = instance.proxy_client  # Use dot notation for property access
            >>> print(f"Proxy client name: {proxy_name}")

        #ai-gen-doc
        """
        return self._proxy_client

    def _prepare_advsearchgrp(self, source_item_list: List[str], subclient_id: int) -> Dict[str, Any]:
        """Prepare the advsearchgrp JSON structure for a restore job for OneDrive for Business clients.

        This utility function generates the required advsearchgrp dictionary for initiating a restore job,
        using the provided list of user GUIDs and the subclient ID.

        Args:
            source_item_list: List of user GUIDs to process in the restore operation.
            subclient_id: The subclient ID associated with the client.

        Returns:
            Dictionary representing the advsearchgrp JSON structure for the restore job.

        Example:
            >>> user_guids = ['guid1', 'guid2', 'guid3']
            >>> subclient_id = 12345
            >>> advsearchgrp_json = google_instance._prepare_advsearchgrp(user_guids, subclient_id)
            >>> print(advsearchgrp_json)
            >>> # Use the returned advsearchgrp_json in a restore job request

        #ai-gen-doc
        """
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
                                    "values": source_item_list
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

    def _prepare_findquery(self, source_item_list: list, subclient_id: int) -> dict:
        """Prepare the findquery JSON payload for a restore job for OneDrive for Business clients.

        This utility function constructs the findquery JSON required to initiate a restore job,
        using the provided list of user GUIDs and the subclient ID.

        Args:
            source_item_list: List of user GUIDs to be processed in the restore operation.
            subclient_id: The subclient ID associated with the client.

        Returns:
            A dictionary representing the findquery JSON for the restore job.

        Example:
            >>> user_guids = ['guid1', 'guid2']
            >>> subclient_id = 123
            >>> findquery = google_instance._prepare_findquery(user_guids, subclient_id)
            >>> print(findquery)
            {'subclientId': 123, 'userGuids': ['guid1', 'guid2']}
        #ai-gen-doc
        """

        findquery = {
            "searchProcessingInfo": {
                "pageSize": 15,
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
                    }
                ]
            },
            "advSearchGrp": self._prepare_advsearchgrp(source_item_list, subclient_id),
            "mode": "WebConsole"
        }

        return findquery

    def _prepare_restore_json(self, source_item_list: list, **kwargs: dict) -> dict:
        """Prepare the user-level restore JSON for OneDrive for Business clients.

        This utility function constructs the request JSON required to initiate a restore job for OneDrive for Business users.
        It supports both in-place and out-of-place restores, as well as disk restores, and allows for various customization
        options via keyword arguments.

        Args:
            source_item_list: List of user GUIDs to process in the restore operation.

        Keyword Args:
            out_of_place (bool): If True, performs an out-of-place restore.
            accountInfo (dict): Required for out-of-place restore. Example:
                {
                    "userDisplayName": "",
                    "userGUID": "",
                    "userSMTP": ""
                }
            disk_restore (bool): If True, performs a restore to disk.
            destination_client (str): Name of the destination client for disk restore.
            overwrite (bool): If True, existing files at the destination will be overwritten.
            restore_as_copy (bool): If True, files will be restored as a copy if they already exist.
            skip_file_permissions (bool): If True, file permissions will be restored.
            destination_type (str): Destination type for out-of-place restore.
            destination_path (str): Destination account for out-of-place restore.
            include_deleted_items (bool): If True, deleted items are included in the restore.
            destination_label (str): Label specifying where the restore should be performed in the mailbox.

        Returns:
            dict: The request JSON for the restore job.

        Raises:
            SDKException: If the destination client with the given name does not exist, or if any parameter type is invalid.

        Example:
            >>> user_guids = ["guid1", "guid2"]
            >>> restore_json = google_instance._prepare_restore_json(
            ...     user_guids,
            ...     out_of_place=True,
            ...     accountInfo={
            ...         "userDisplayName": "John Doe",
            ...         "userGUID": "guid1",
            ...         "userSMTP": "john.doe@example.com"
            ...     },
            ...     overwrite=True,
            ...     include_deleted_items=True
            ... )
            >>> print(restore_json)
            # The returned dictionary can be used to submit a restore job.

        #ai-gen-doc
        """

        out_of_place = kwargs.get('out_of_place', False)
        disk_restore = kwargs.get('disk_restore', False)
        destination_client = kwargs.get('destination_client')
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', False)
        include_deleted_items = kwargs.get('include_deleted_items', False)
        destination_label = kwargs.get('destination_label', "")

        if destination_client:
            if self._commcell_object.clients.all_clients.get(destination_client):
                destination_client_object = self._commcell_object.clients.all_clients.get(destination_client)
                destination_client_id = int(destination_client_object.get('id'))
            else:
                raise SDKException('Client', '102', 'Client "{0}" does not exist.'.format(destination_client))

        if ((destination_client and not isinstance(destination_client, str) or
             kwargs.get('destination_path') and not isinstance(kwargs.get('destination_path'), str)) or not
        (isinstance(source_item_list, list) and
         isinstance(skip_file_permissions, bool) and
         isinstance(disk_restore, bool) and
         isinstance(out_of_place, bool) and
         isinstance(overwrite, bool) and
         isinstance(restore_as_copy, bool) and
         isinstance(include_deleted_items, bool))):
            raise SDKException('Instance', '101')

        request_json = self._restore_json(client=self._agent_object._client_object)

        subtasks = request_json['taskInfo']['subTasks'][0]
        options = subtasks['options']
        restore_options = options['restoreOptions']

        restore_options["browseOption"] = {
            "commCellId": self._commcell_object.commcell_id,
            "showDeletedItems": include_deleted_items
        }

        restore_options['commonOptions'] = {
            "overwriteFiles": False,
            "skip": True,
            "unconditionalOverwrite": False
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

        if kwargs.get("destination_path"):
            destination['destPath'] = [kwargs.get('destination_path')]

        restore_options['fileOption']['sourceItem'] = source_item_list

        restore_options['cloudAppsRestoreOptions'] = {
            "instanceType": self._ca_instance_type,
            "googleRestoreOptions": {
                "skipPermissionsRestore": False if disk_restore else skip_file_permissions,
                "restoreToDifferentAccount": True if out_of_place else False,
                "restoreAsCopy": False if disk_restore else restore_as_copy,
                "filelevelRestore": False,
                "strDestUserAccount": kwargs.get("destination_path") if out_of_place else '',
                "overWriteItems": False if disk_restore else overwrite,
                "restoreToGoogle": False if disk_restore else True,
                "gmailRestoreItemType": 0,
                "destInfo": {
                    "destinationType": 0 if kwargs.get("destination_type") == 'USER' else 1,
                    "userDisplayName": kwargs.get('accountInfo', {}).get('userDisplayName', ''),
                    "userGUID": kwargs.get('accountInfo', {}).get('userGUID', ''),
                    "folderPath": destination_label,
                    "folderId": destination_label
                }
            }
        }

        del subtasks['subTaskOperation']
        del restore_options['fileOption']
        del restore_options['impersonation']
        del restore_options['volumeRstOption']
        del restore_options['sharePointRstOption']
        del restore_options['virtualServerRstOption']

        associations = request_json['taskInfo']['associations'][0]
        subclient_id = associations['subclientId']

        cloudAppsRestoreOptions = restore_options['cloudAppsRestoreOptions']
        cloudAppsRestoreOptions['googleRestoreOptions']['findQuery'] = self._prepare_findquery(source_item_list,
                                                                                               subclient_id)
        cloudAppsRestoreOptions['googleRestoreOptions']['destInfo']['userSMTP'] = kwargs.get('accountInfo', {}).get(
            'userSMTP', '')
        cloudAppsRestoreOptions['googleRestoreOptions']['destInfo']['subclientId'] = subclient_id

        destination_option = "Destination"
        destination_value = "Original location"
        if out_of_place:
            destination_option = f"Destination {'user' if kwargs.get('destination_type') == 'USER' else 'shared drive'}"
            destination_value = kwargs.get("destination_path")
        if disk_restore:
            destination_option = "Destination server"
            destination_value = destination_client

        options["commonOpts"] = {
            "notifyUserOnJobCompletion": False,
            "jobMetadata": [
                {
                    "selectedItems": [
                        {
                            "itemName": source_item_list[0],
                            "itemType": "Mailbox" if self.ca_instance_type == "GMAIL" else "User"
                        }
                    ],
                    "jobOptionItems": [
                        {
                            "option": "Restore destination",
                            "value": "Gmail" if self.ca_instance_type == "GMAIL" else "Google Drive"
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
                            "value": "Skip"
                        },
                        {
                            "option": "Skip file permissions",
                            "value": "Enabled"
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

        if self.ca_instance_type == "GMAIL":
            joboptionitems.extend([{"option": "Restore mail","value": "Enabled"},{"option": "Restore contacts","value": "Enabled"},{"option": "Restore calendars","value": "Enabled"}])
            cloudAppsRestoreOptions['googleRestoreOptions']['gmailOperations']={"isMailSelected": True,"isContactsSelected": True,"isCalendarSelected": True}

        if include_deleted_items:
            for filter in cloudAppsRestoreOptions['googleRestoreOptions']['findQuery']['advSearchGrp']['commonFilter'][0]['filter']['filters']:
                if filter['field']=='CISTATE':
                    filter['fieldValues']['values'].extend(['3333', '3334', '3335'])

        if out_of_place:
            joboptionitems.append({"option": "Destination client", "value": destination_client})
        if disk_restore:
            joboptionitems.append({"option": "Destination path", "value": kwargs.get("destination_path")})

        return request_json

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
        """Restore specified files or folders to a different client and destination path.

        This method restores the files and folders listed in `paths` to the specified `destination_path`
        on the given `client`. The restore can be customized to overwrite existing files, restore data
        and ACLs, specify copy precedence, filter by time range, and optionally restore to disk.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: The full path on the destination client where data will be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional copy precedence value for the storage policy copy. Default is None.
            from_time: Optional lower bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_disk: If True, perform a restore to disk operation. Default is False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize.

        Example:
            >>> # Restore files to a different client and path
            >>> job = google_instance.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location',
            ...     paths=['/data/file1.txt', '/data/folder2'],
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
                "restoreToGoogle": restore_to_google,
                "gmailRestoreItemType": 0
            }
        }
        return self._process_restore_response(request_json)

    def enable_auto_discovery(self, mode: str = 'REGEX') -> None:
        """Enable auto discovery on the GoogleInstance.

        This method enables automatic discovery of resources for the instance using the specified mode.

        Args:
            mode: The auto discovery mode to use. Valid values are:
                - 'REGEX': Use regular expressions for discovery.
                - 'GROUP': Use group-based discovery.
                Default is 'REGEX'.

        Example:
            >>> instance = GoogleInstance()
            >>> instance.enable_auto_discovery()  # Enables with default 'REGEX' mode
            >>> instance.enable_auto_discovery(mode='GROUP')  # Enables with 'GROUP' mode

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
            dict: A dictionary containing the properties of the GoogleInstance in JSON format.

        Example:
            >>> instance = GoogleInstance()
            >>> properties_json = instance._get_instance_properties_json()
            >>> print(properties_json)
            >>> # Output will be a dictionary with instance configuration details

        #ai-gen-doc
        """

        return {'instanceProperties': self._properties}

    def modify_index_server(self, modified_index_server: str) -> None:
        """Modify the index server associated with this GoogleInstance.

        Args:
            modified_index_server: The name of the new index server to assign.

        Example:
            >>> google_instance = GoogleInstance()
            >>> google_instance.modify_index_server("NewIndexServer01")
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
        """Modify the access nodes for the GoogleInstance.

        This method updates the list of access nodes and the associated user credentials
        for the GoogleInstance. Use this to change which nodes have access and update
        authentication details.

        Args:
            modified_accessnodes_list: List of new access nodes to be assigned.
            modified_user_name: The new user account name for access nodes.
            modified_user_password: The new user account password for access nodes.

        Example:
            >>> instance = GoogleInstance()
            >>> new_nodes = ['accessnode1', 'accessnode2']
            >>> instance.modify_accessnodes(new_nodes, 'new_user', 'new_password')
            >>> print("Access nodes and credentials updated successfully.")

        #ai-gen-doc
        """
        member_servers = []
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