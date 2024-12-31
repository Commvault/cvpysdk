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
from ...exception import SDKException
from ..cainstance import CloudAppsInstance
from ...constants import AppIDAType
from base64 import b64encode


class GoogleInstance(CloudAppsInstance):
    """Class for representing an Instance of the GMail/Gdrive instance type."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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
    def ca_instance_type(self):
        """Returns the CloudApps instance type"""
        if self._ca_instance_type == 1:
            return 'GMAIL'
        elif self._ca_instance_type == 2:
            return 'GDRIVE'
        elif self._ca_instance_type == 7:
            return 'ONEDRIVE'
        return self._ca_instance_type

    @property
    def manage_content_automatically(self):
        """Returns the CloudApps Manage Content Automatically property"""
        return self._manage_content_automatically

    @property
    def auto_discovery_status(self):
        """Treats the Auto discovery property as a read-only attribute."""
        return self._auto_discovery_enabled

    @property
    def auto_discovery_mode(self):
        """Returns the Auto discovery mode property"""
        return self._auto_discovery_mode

    @property
    def app_email_id(self):
        """Returns the service account mail id"""
        return self._app_email_id

    @property
    def google_admin_id(self):
        """Returns the Google admin mail id"""
        return self._google_admin_id

    @property
    def key_file_path(self):
        """Returns the service account key file path"""
        return self._service_account_key_file

    @property
    def google_client_id(self):
        """Returns the service account client id"""
        return self._app_client_id

    @property
    def onedrive_client_id(self):
        """Returns the OneDrive app client id"""
        return self._client_id

    @property
    def onedrive_tenant(self):
        """Returns the OneDrive tenant id"""
        return self._tenant

    @property
    def proxy_client(self):
        """Returns the proxy client name to this instance"""
        return self._proxy_client

    def _prepare_advsearchgrp(self, source_item_list, subclient_id):
        """
                    Utility function to prepare advsearchgrp json for restore job for OneDrive for business clients

                    Args:
                        source_item_list (list)         --  list of user GUID to process in restore

                        subclient_id                    --  subclient id of the client

                    Returns:
                        advsearchgrp (dict) - advsearchgrp json for restore job
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

    def _prepare_findquery(self, source_item_list, subclient_id):
        """
            Utility function to prepare findquery json for restore job for OneDrive for bussiness clients

            Args:
                source_item_list (list)         --  list of user GUID to process in restore

                subclient_id                    --  subclient id of the client

            Returns:
                findquery (dict) - findquery json for restore job
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
                  "advSearchGrp": self._prepare_advsearchgrp(source_item_list,subclient_id),
                  "mode": "WebConsole"
                }

        return findquery

    def _prepare_restore_json_v2(self, source_item_list, **kwargs):

        """ Utility function to prepare user level restore json for OneDrive for bussiness clients

            Args:
                source_item_list (list)         --  list of user GUID to process in restore

            Kwargs:

                out_of_place (bool)             --  If True, out of place restore will be performed

                disk_restore (bool)             --  If True, restore to disk will be performed

                destination_path (str)          --  destination path for oop and disk restores

                destination_client              -- destination client for disk restore

                overwrite (bool)                --  If True, files will be overwritten in destination if already exists

                restore_as_copy (bool)          --  If True, files will be restored as copy if already exists

                skip_file_permissions (bool)    --  If True, file permissions will be restored

            Returns:
                request_json (dict) - request json for restore job

            Raises:
                SDKException:
                    if destination client with given name does not exist

                    if type of parameter is invalid

        """

        out_of_place = kwargs.get('out_of_place', False)
        disk_restore = kwargs.get('disk_restore', False)
        destination_path = kwargs.get('destination_path', False)
        destination_client = kwargs.get('destination_client')
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', False)



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

        restore_options["browseOption"] = {
            "commCellId": self._commcell_object.commcell_id,
            "showDeletedItems": False
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
                "restoreToGoogle": False if disk_restore else True,
                "gmailRestoreItemType": 0
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
        cloudAppsRestoreOptions['googleRestoreOptions']['findQuery'] = self._prepare_findquery(source_item_list, subclient_id)

        destination_option = "Destination"
        destination_value = "Original location"
        if out_of_place:
            destination_option = "Destination user"
            destination_value = source_item_list[0]
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
                    "itemType": "User" if self._ca_instance_type=="GDrive" else "Mailbox"
                  }
                ],
                "jobOptionItems": [
                  {
                    "option": "Restore destination",
                    "value": "Google Drive" if self._ca_instance_type=="GDrive" else "Gmail"
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
                    "value": "Disabled"
                  }
                ]
              }
            ]
          }

        joboptionitems = options['commonOpts']['jobMetadata'][0]['jobOptionItems']

        if out_of_place:
            joboptionitems.append({"option": "Destination client","value": destination_client })
        if disk_restore:
            joboptionitems.append({"option": "Destination path", "value": destination_path})

        return request_json

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            to_disk=False):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                                                           the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                                                           files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_disk             (bool)       --  If True, restore to disk will be performed

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
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

    def enable_auto_discovery(self, mode='REGEX'):
        """Enables auto discovery on instance.

           Args:

                mode    (str)   -- Auto Discovery mode

                Valid Values:

                    REGEX
                    GROUP

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

    def _get_instance_properties_json(self):
        """Returns the instance properties json."""

        return {'instanceProperties': self._properties}

    def modify_index_server(self, modified_index_server):
        """
            Method to modify the index server

            Arguments:
                modified_index_server        (str)--     new index server name
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

    def modify_accessnodes(self,modified_accessnodes_list,modified_user_name,modified_user_password):
        """
                   Method to modify accessnodes

                   Arguments:
                       modified_accessnodes_list     (list)  --     list of new accessnodes
                       modified_user_name            (str)   --     new user account name
                       modified_user_password        (str)   --     new user account password
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