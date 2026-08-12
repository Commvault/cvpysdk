# -*- coding: utf-8 -*-
# ————————————————————————–
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
# ————————————————————————–

"""File for operating on a Sharepoint Subclient

SharepointSuperSubclient: Derived class from Subclient Base class, containing common methods for both Sharepoint v1 and v2 subclients.

SharepointSuperSubclient:

    backup()                            --  Runs a backup job for the subclient of the level specified.

    _get_subclient_properties()         --  gets the subclient related properties of the Sharepoint subclient.

    _json_out_of_place_destination_option() -- setter for the SharePoint Online out of place restore
        option in restore json


SharepointSubclient: Derived class from SharepointSuperSubclient Base class, representing a sharepoint subclient,
and to perform operations on that subclient

SharepointSubclient:


    _get_subclient_properties_json()    --  gets all the subclient related properties of the Sharepoint subclient.

    _process_restore_response           --  processes response received for the restore request.

    _restore_request_json               --  returns the JSON request to pass to the API as per the options.

    sharepoint_subclient_prop()         --  initializes additional properties of this subclient.

    content()                           --  sets the content of the subclient.

    restore()                           --  restores the databases specified in the input paths list.

    add_azure_app()                     --  adds a single azure app to the sharepoint client

    delete_azure_app()                  --  deletes one/multiple azure app(s) from the sharepoint client

    run_manual_discovery()              --  runs the manual disocvery for specified backupset

    browse_for_content()                --  returns the user association content

    associate_site_collections_and_webs()-- associates the specified site collections/webs

    delete_data()                       --  delete backed up data from sharepoint clients

    restore_in_place()                  --  runs an in-place restore job on the specified Sharepoint pseudo client

    restore_in_place_syntex()           --  runs an in-place restore job on the specified Sharepoint Syntex pseudo client

    refresh_license_collection()        --  runs a license collection process

    preview_backedup_file()               --  gets the preview content for the file

SharepointV1Subclient: Derived class from SharepointSuperSubclient Base class, representing a sharepoint v1 subclient,
and to perform operations on that subclient

SharepointV1Subclient:

    discover_sharepoint_sites()         --  Checks whether SP content i.e, sites/webs are available

    _get_subclient_properties_json()    --  gets all the subclient related properties of the Sharepoint subclient.

    content()                           --  sets the content of the subclient.

    restore_in_place()                  --  runs a in-place restore job on the specified Sharepoint pseudo client


"""

from __future__ import unicode_literals

import datetime
from base64 import b64encode
from ..subclient import Subclient
from ..exception import SDKException
from ..constants import SQLDefines
from ..constants import SharepointDefines
from ..job import Job


class SharepointSuperSubclient(Subclient):

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               collect_metadata=False,
               advanced_options=None,
               common_backup_options=None):
        """Runs a backup job for the subclient of the level specified.
            Args:
                backup_level            (str)   --  level of backup the user wish to run
                                                    Full / Incremental
                incremental_backup      (bool)  --  run incremental backup
                                                    only applicable in case of Synthetic_full backup
                incremental_level       (str)   --  run incremental backup before/after synthetic full
                                                    BEFORE_SYNTH / AFTER_SYNTH
                                                    only applicable in case of Synthetic_full backup
                collect_metadata        (bool)  --  Collect Meta data for the backup
                advanced_options       (dict)  --  advanced backup options to be included while
                                                    making the request
            Returns:
                object - instance of the Job class for this backup job if its an immediate Job
                         instance of the Schedule class for the backup job if its a scheduled Job
            Raises:
                SDKException:
                    if backup level specified is not correct
                    if response is empty
                    if response is not success
        """
        backup_level = backup_level.lower()
        if backup_level not in ['full', 'incremental']:
            raise SDKException('Subclient', '103')
        if advanced_options or common_backup_options:
            request_json = self._backup_json(
                backup_level=backup_level,
                incremental_backup=incremental_backup,
                incremental_level=incremental_level,
                advanced_options=advanced_options,
                common_backup_options=common_backup_options
            )
            backup_service = self._commcell_object._services['CREATE_TASK']
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )
            return self._process_backup_response(flag, response)
        else:
            return super(SharepointSuperSubclient, self).backup(backup_level=backup_level,
                                                                incremental_backup=incremental_backup,
                                                                incremental_level=incremental_level,
                                                                collect_metadata=collect_metadata)

    def _json_out_of_place_destination_option(self, value):
        """setter for the SharePoint Online out of place restore
        option in restore json
            Args:
                value (dict)    --  restore option need to be included
            Returns:
                (dict)          --  generated exchange restore options JSON
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')
        self._out_of_place_destination_json = {
            "inPlace": False,
            "destPath": [value.get("destination_path")],
            "destClient": {
                "clientId": int(self._client_object.client_id),
                "clientName": self._client_object.client_name
            },
        }

    def _get_subclient_properties(self):
        """Gets the subclient related properties of the Sharepoint subclient.
        """
        super(SharepointSuperSubclient, self)._get_subclient_properties()
        self._sharepoint_subclient_prop = self._subclient_properties.get('sharepointsubclientprop', {})
        self._content = self._subclient_properties.get('content', {})


class SharepointSubclient(SharepointSuperSubclient):
    """Derived class from Subclient Base class, representing a Sharepoint subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "sharepointsubclientprop": self._sharepoint_subclient_prop,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def sharepoint_subclient_prop(self):
        """ getter for sql server subclient properties """
        return self._sharepoint_subclient_prop

    @sharepoint_subclient_prop.setter
    def sharepoint_subclient_prop(self, value):
        """

            Args:
                value (list)  --  list of the category and properties to update on the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        category, prop = value

        self._set_subclient_properties(category, prop)

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """

        subclient_content = self._content

        content_list = []

        for content in subclient_content:
            if 'spContentPath' in content:
                content_list.append(content["spContentPath"])

        return content_list

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add a new Sharepoint server Subclient
            with the content passed in subclient content.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

        """
        content = []

        for webapp in subclient_content:
            sp_server_dict = {
                "spContentPath": webapp
            }
            content.append(sp_server_dict)

        self._set_subclient_properties("_content", content)

    def restore(
            self,
            content_to_restore,
            database_client,
            spsetup_list,
            overwrite=True
    ):
        """Restores the Sharepoint content specified in the input paths list.

            Args:
                content_to_restore (list):  Content to restore.

                database_client (str): Name of Sharepoint SQL server back-end client.

                spsetup_list (dict): Dictionary of the Sharepoint setup configuration.

                overwrite (bool):  Unconditional overwrite files during restore.  Defaults to True.

                to_time (str):  Restore to time.  Defaults to None.


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if content_to_restore is not a list

                    if response is empty

                    if response is not success
        """
        if not self._backupset_object.is_sharepoint_online_instance:
            if not isinstance(content_to_restore, list):
                raise SDKException('Subclient', '101')

            self._backupset_object._instance_object._restore_association = self._subClientEntity

            request_json = self._sharepoint_restore_options_json(
                content_to_restore,
                database_client,
                spsetup_list,
                overwrite=overwrite
            )

            return self._process_restore_response(request_json)
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint Online Instance')

    def _sharepoint_restore_options_json(
            self,
            content,
            database_client,
            spsetup_list,
            destination_client=None,
            overwrite=None
    ):
        """Constructs JSON for Sharepoint restore options based on restore request
            and returns the constructed json.

            Args:
                content (list):  List of Sharepoint content to restore.

                database_client (str): Name of Sharepoint SQL server back-end client.

                spsetup_list (dict): Dictionary of the Sharepoint setup configuration.

                destination_client (str): Restore destination Sharepoint client.

                overwrite (bool):  Unconditional overwrite files during restore.  Defaults to True.

            Returns:
                dict: dictionary consisting of the Sharepoint Server options.
        """
        if not self._backupset_object.is_sharepoint_online_instance:
            client_name = self._client_object._client_name

            request_json = self._restore_json(
                client=client_name
            )

            if destination_client is None:
                destination_client = client_name

            common_options = {
                "allVersion": True,
                "erExSpdbPathRestore": True
            }
            destination = {
                "inPlace": True,  # TODO check if in-place/oop.. will do this when we implement oop testcase
                "destClient": {
                    "clientName": destination_client
                },
                "destinationInstance": {
                    "clientName": destination_client,
                    "instanceName": "defaultInstance",
                    "appName": self._agent_object.agent_name
                }
            }
            sql_restore_options = {
                "sqlRecoverType": SQLDefines.STATE_RECOVER,
                "dropConnectionsToDatabase": True,
                "overWrite": overwrite,
                "sqlRestoreType": SQLDefines.DATABASE_RESTORE
            }
            sharepoint_restore_option = {
                "configContentDatabase": True,
                "isSharePointRBS": False,
                "restoreSqlDBTO": False,
                "is90OrUpgradedClient": False,
                "restoreSqlDBtoLocation": "",
                "fetchSqlDatabases": True,
                "spRestoreToDisk": {
                    "restoreToDisk": False
                }
            }
            sharepoint_db_restore_option = {
                "restoreType": "SameConfiguration",
                "restoreDatabaseOption": "RESTORE_ALL",
                "rbsOptions": {
                    "sqlSource": {
                        "clientName": database_client
                    },
                    "sqlDestination": {
                        "destClient": {
                            "clientName": database_client
                        }
                    }
                }
            }

            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'] \
                ['browseOption']['backupset']["backupsetName"] = self._backupset_object._backupset_name
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["sqlServerRstOption"] = sql_restore_options
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["sharePointDBRestoreOption"] = sharepoint_db_restore_option
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["commonOptions"].update(common_options)
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["destination"].update(destination)
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["sharePointRstOption"].update(sharepoint_restore_option)

            content_json = {}
            source_items = []
            database_list = []
            for item in content:
                item = item.split("\\")[2]
                for sp_dict in spsetup_list:
                    if sp_dict["application_pool"].lower() == item.lower():
                        database_name = sp_dict["content_database"]
                        database_server = sp_dict["database_server"]
                        web_application = sp_dict["web_application"]
                        username = sp_dict["credentials"]["username"]
                        password = b64encode(sp_dict["credentials"]["password"].encode()).decode()

                        source_items.append(
                            SharepointDefines.CONTENT_WEBAPP.format(item)
                        )
                        source_items.append(
                            SharepointDefines.CONTENT_DB.format(item, database_name)
                        )

                        database_list.append(database_name)

                        content_json = {
                            "SharePointMetaData": [{
                                "newDirectoryName": "",
                                "newDatabaseServerName": database_server,
                                "sourceItem":
                                    SharepointDefines.CONTENT_DB.format(item, database_name),
                                "newDatabaseName": database_name,
                                "sharePointMetaDataType": "SPContentDatabase"
                            }, {
                                "sourceItem":
                                    SharepointDefines.CONTENT_WEBAPP.format(item),
                                "newWebApplicationURL": web_application,
                                "newWebApplicationName": item,
                                "sharePointMetaDataType": "SPWebApplication",
                                "credentials": {
                                    "userName": username,
                                    "password": password
                                }
                            }]
                        }
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["fileOption"]["sourceItem"] = source_items
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["sqlServerRstOption"]["database"] = database_list
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["sqlServerRstOption"]["restoreSource"] = database_list
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"] \
                ["sharePointDBRestoreOption"].update(content_json)

            return request_json
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint Online Instance')

    def _json_disk_restore_sharepoint_restore_option(self, value):
        """Setter for  the SharePoint Online Disk restore option
        in restore json

            Args:
                value   (dict)  --  restore option need to be included
                                    Example:
                                        {
                                            "disk_restore_type": 1,
                                            "destination_path": "C:\\TestRestore"
                                        }

                                        disk_restore_type - 1 (Restore as native files)
                                        disk_restore_type - 2 (Restore as original files)


            Returns:
                (dict)          --  generated sharepoint restore options JSON

        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._sharepoint_disk_option_restore_json = {
            "restoreToDiskType": value.get("disk_restore_type", 1),
            "restoreToDiskPath": value.get("destination_path", ""),
            "restoreToDisk": True
        }

    def _json_blob_restore_sharepoint_restore_option(self, value):
        """Setter for the SharePoint Online Blob restore option
        in restore json

            Args:
                value   (dict)  --  restore option need to be included
                                    Example:
                                        {
                                            "blob_container_id": 1,
                                        }

            Returns:
                (dict)          --  generated sharepoint restore options JSON

        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        if "blob_container_id" not in value:
            raise SDKException('Subclient', '101', 'blob_container_id is required')

        self._sharepoint_blob_option_restore_json = {
            "blobContainerCredId": value.get("blob_container_id"),
            "restoreToBlob": True
        }

    def _prepare_disk_restore_json(self, _disk_restore_option):
        """
        Prepare disk restore Json with all getters

        Args:
            _disk_restore_option - dictionary with all disk restore options

            value:

                paths (list)                    --  list of paths of lists/libraries to restore

                destination_client (str)        --  client where the lists/libraries needs to be restored

                destination_path (str)          --  path where the lists/libraries needs to be restored

                unconditional_overwrite (bool)  --  unconditional overwrite files during restore
                    default: True


        returns:
            request_json        -complete json for performing disk Restore options
        """

        if _disk_restore_option is None:
            _disk_restore_option = {}

        paths = self._filter_paths(_disk_restore_option.get('paths', []))
        self._json_disk_restore_sharepoint_restore_option(_disk_restore_option)
        _disk_restore_option['paths'] = paths

        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_disk_restore_option)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions']["sharePointRstOption"][
            "spRestoreToDisk"] = self._sharepoint_disk_option_restore_json

        return request_json

    def _prepare_blob_restore_json(self, _blob_restore_option: dict) -> dict:
        """
        Prepare blob restore Json with all getters

        Args:
            _blob_restore_option (dict) - All blob restore options

            value:

                destination_blob(str)           --  The Azure blob where data will get restored

                destination_client (str)        --  client where the lists/libraries needs to be restored

                unconditional_overwrite (bool)  --  unconditional overwrite files during restore
                    default: True


        returns:
            request_json        -complete json for performing disk Restore options
        """

        if _blob_restore_option is None:
            _blob_restore_option = {}

        self._json_blob_restore_sharepoint_restore_option(_blob_restore_option)

        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_blob_restore_option)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions']["sharePointRstOption"][
            "spRestoreToBlob"] = self._sharepoint_blob_option_restore_json

        return request_json

    def _prepare_out_of_place_restore_json(self, _restore_option, common_options: dict):
        """
        Prepare out of place retsore Json with all getters

        Args:
            _restore_option - dictionary with all out of place restore options

            value:

                paths (list)            --  list of paths of SharePoint list/libraries to restore

                destination_path (str)  --  path where the SharePoint Site where list/libraries needs to be restored

                overwrite (bool)        --  unconditional overwrite files during restore
                    default: True

            common_options      (dict)  -- common options for restore job payload

        returns:
            request_json        -  complete json for performing disk Restore options

        """

        if _restore_option is None:
            _restore_option = {}

        paths = self._filter_paths(_restore_option['paths'])
        self._json_out_of_place_destination_option(_restore_option)
        _restore_option['paths'] = paths

        # set the setters
        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_restore_option)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions'][
            'destination'] = self._out_of_place_destination_json

        if common_options:
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions'].update(common_options)
        return request_json

    def _set_properties_to_update_site_association(self, operation):
        """Updates the association properties of site

            Args:

               operation (int)                  --  type of operation to be performed
                                                     Example: 1 - Associate
                                                              2 - Enable
                                                              3 - Disable
                                                              4 - Remove

            Raises:

            SDKException:

                if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            properties_dict = {}
            if operation == 1:
                properties_dict["commonFlags"] = 0
                properties_dict["isAutoDiscoveredUser"] = False
                properties_dict["accountStatus"] = 0
            elif operation == 2:
                properties_dict["commonFlags"] = 4
                properties_dict["accountStatus"] = 0
            elif operation == 3:
                properties_dict["commonFlags"] = 4
                properties_dict["accountStatus"] = 2
            elif operation == 4:
                properties_dict["isAutoDiscoveredUser"] = True
            return properties_dict
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def add_azure_app(self, azure_app_id, azure_app_key_id, azure_directory_id, cert_string=None, cert_password=None):
        """
        Adds an azure app to the sharepoint client

        args:
            azure_app_id        (str)       --      Application id of the azure app
            azure_app_key_id    (str)       --      Client Secret of the azure app
            azure_directory_id  (str)       --      Azure directory/tenant ID
            cert_string         (str)       --      Certificate String
            cert_password       (str)       --      Certificate Password
        """
        properties_dict = self._backupset_object.properties
        azure_app_list = properties_dict["sharepointBackupSet"]["spOffice365BackupSetProp"].get("azureAppList", {}).get("azureApps", [])
        azure_app_key_id = b64encode(azure_app_key_id.encode()).decode()

        azure_app_dict = {
            "azureAppId": azure_app_id,
            "azureAppKeyValue": azure_app_key_id,
            "azureDirectoryId": azure_directory_id
        }

        if cert_string:
            # cert_string needs to be encoded twice
            cert_string = b64encode(cert_string).decode()
            cert_string = b64encode(cert_string.encode()).decode()

            cert_password = b64encode(cert_password.encode()).decode()

            cert_dict = {
                "certificate": {
                    "certBase64String": cert_string,
                    "certPassword": cert_password
                }
            }
            azure_app_dict.update(cert_dict)

        azure_app_list.append(azure_app_dict)

        properties_dict["sharepointBackupSet"]["spOffice365BackupSetProp"]["azureAppList"] = {
            "azureApps": azure_app_list
        }

        self._backupset_object.update_properties(properties_dict)

    def delete_azure_app(self, app_ids):
        """
        Deletes azure app from the sharepoint client

        args:
            app_ids         (str / list[str])   --      Azure App ID or list of Azure App IDs to delete.
        """
        if not isinstance(app_ids, list):
            app_ids = [app_ids]

        properties_dict = self._backupset_object.properties
        azure_app_list = properties_dict["sharepointBackupSet"]["spOffice365BackupSetProp"]["azureAppList"]["azureApps"]
        new_app_list = []

        for azure_app_dict in azure_app_list:
            if not azure_app_dict["azureAppId"] in app_ids:
                new_app_list.append(azure_app_dict)

        properties_dict["sharepointBackupSet"]["spOffice365BackupSetProp"]["azureAppList"]["azureApps"] = new_app_list

        self._backupset_object.update_properties(properties_dict)

    def run_manual_discovery(self):
        """Runs the manual discovery of backupset

            Raises:

                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success

                    if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            self._MANUAL_DISCOVERY = self._services['CLOUD_DISCOVERY'] % (
                self._instance_object.instance_id, self._client_object.client_id, self._agent_object.agent_id)
            flag, response = self._cvpysdk_object.make_request(
                'GET', self._MANUAL_DISCOVERY
            )
            if flag:
                if response.json():
                    if 'response' in response.json():
                        response = response.json().get('response', [])
                        if response:
                            error_code = response[0].get('errorCode', -1)
                            if error_code != 0:
                                error_string = response.json().get('response', {})
                                o_str = 'Failed to run manual discovery\nError: "{0}"'.format(error_string)
                                raise SDKException('Subclient', '102', o_str)
                    elif 'errorMessage' in response.json():
                        error_string = response.json().get('errorMessage', "")
                        o_str = 'Failed to run manual discovery\nError: "{0}"'.format(error_string)
                        raise SDKException('Subclient', '102', o_str)
                    else:
                        raise SDKException('Response', '102')
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def configure_group_for_backup(self, discovery_type, association_group_name, plan_id):
        """Configures group for backup

            Args:

                discovery_type  (int)       --  type of discovery for content
                                                All Web Sites - 9
                                                All Groups And Teams Sites - 10
                                                All Project Online Sites - 11

                association_group_name(str) --  type of association
                                                Example: All Web Sites, All Groups And Teams Sites,
                                                All Project Online Sites

                plan_id (int)               --  id of office 365 plan

            Raises:

                SDKException:

                    if response is empty

                    if response is not success

                    if the method is called by SharePoint On-Premise Instance

         """
        if self._backupset_object.is_sharepoint_online_instance:
            self._SET_USER_POLICY_ASSOCIATION = self._services['SET_USER_POLICY_ASSOCIATION']
            request_json = {
                "cloudAppAssociation": {
                    "accountStatus": 2,
                    "subclientEntity": {
                        "subclientId": int(self.subclient_id)
                    },
                    "cloudAppDiscoverinfo": {
                        "discoverByType": discovery_type,
                        "groups": [
                            {
                                "name": association_group_name
                            }
                        ]
                    },
                    "plan": {
                        "planId": plan_id
                    }
                }
            }
            flag, response = self._cvpysdk_object.make_request(
                'POST', self._SET_USER_POLICY_ASSOCIATION, request_json
            )
            if flag:
                if response.json():
                    if 'response' in response.json():
                        response = response.json().get('response', [])
                        if response:
                            error_code = response[0].get('errorCode', -1)
                            if error_code != 0:
                                error_string = response.json().get('response', {})
                                o_str = 'Failed to set \nError: "{0}"'.format(error_string)
                                raise SDKException('Subclient', '102', o_str)
                    elif 'errorMessage' in response.json():
                        error_string = response.json().get('errorMessage', "")
                        o_str = 'Failed to set category based content for association\nError: "{0}"'.format(
                            error_string)
                        raise SDKException('Subclient', '102', o_str)
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def update_auto_association_group_properties(self, discovery_type, association_group_name,
                                                 account_status=None, plan_id=None):
        """Associates the content for backup based on provided group

            Args:

                discovery_type  (int)       --  type of discovery for content
                                                All Web Sites - 9
                                                All Groups And Teams Sites - 10
                                                All Project Online Sites - 11

                association_group_name(str) --  type of association
                                                Example: All Web Sites, All Groups And Teams Sites,
                                                All Project Online Sites

                account_status  (int)       --  type of operation to be performed
                                                enable - 0
                                                remove - 1
                                                disable - 2

                plan_id (int)               --  id of office 365 plan

            Raises:

                SDKException:

                    if response is empty

                    if response is not success

                    if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            self._ASSOCIATE_CONTENT = self._services['UPDATE_USER_POLICY_ASSOCIATION']
            request_json = {
                "cloudAppAssociation": {
                    "subclientEntity": {
                        "subclientId": int(self.subclient_id)
                    },
                    "cloudAppDiscoverinfo": {
                        "discoverByType": discovery_type,
                        "groups": [
                            {
                                "name": association_group_name
                            }
                        ]
                    }
                }
            }
            if account_status is not None:
                request_json['cloudAppAssociation']['accountStatus'] = account_status
            if plan_id:
                request_json['cloudAppAssociation']['plan'] = {
                    "planId": plan_id
                }
            flag, response = self._cvpysdk_object.make_request(
                'POST', self._ASSOCIATE_CONTENT, request_json
            )
            if flag:
                if response.json():
                    if "resp" in response.json():
                        error_code = response.json()['resp']['errorCode']
                        if error_code != 0:
                            error_string = response.json()['response']['errorString']
                            o_str = 'Failed to enable group\nError: "{0}"'.format(error_string)
                            raise SDKException('Subclient', '102', o_str)
                    elif 'errorMessage' in response.json():
                        error_string = response.json()['errorMessage']
                        o_str = 'Failed to associate content\nError: "{0}"'.format(error_string)
                        raise SDKException('Subclient', '102', o_str)
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def browse_for_content(self, discovery_type):
        """Returns the SP content i.e. sites/web information that is discovered in auto discovery phase

                Args:

                    discovery_type  (int)   --  type of discovery for content
                                                For all Associated Web/Sites = 6
                                                For all Non-Associated Web/Sites = 7

                Returns:

                    site_dict     (dict)    --  dictionary of sites properties

                    no_of_records   (int)   --  no of records

                Raises:

                    SDKException:

                        if response is empty

                        if response is not success

                        if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            self._USER_POLICY_ASSOCIATION = self._services['USER_POLICY_ASSOCIATION']
            request_json = {
                "discoverByType": discovery_type,
                "bIncludeDeleted": False,
                "cloudAppAssociation": {
                    "subclientEntity": {
                        "subclientId": int(self.subclient_id)
                    }
                },
                "searchInfo": {
                    "isSearch": 0,
                    "searchKey": ""
                }
            }
            flag, response = self._cvpysdk_object.make_request(
                'POST', self._USER_POLICY_ASSOCIATION, request_json
            )
            if flag:
                if response and response.json():
                    no_of_records = None
                    if 'associations' in response.json():
                        no_of_records = response.json().get('associations', [])[0].get('pagingInfo', {}). \
                            get('totalRecords', -1)
                    elif 'pagingInfo' in response.json():
                        no_of_records = response.json().get('pagingInfo', {}).get('totalRecords', -1)
                        if no_of_records <= 0:
                            return {}, no_of_records
                    associations = response.json().get('associations', [])
                    site_dict = {}
                    if discovery_type == 8:
                        if associations:
                            for group in associations:
                                group_name = group.get("groups", {}).get("name", "")
                                site_dict[group_name] = {
                                    'accountStatus': group.get("accountStatus"),
                                    'discoverByType': group.get("discoverByType"),
                                    'planName': group.get("plan", {}).get("planName", "")
                                }
                    else:
                        if associations:
                            for site in associations:
                                site_url = site.get("userAccountInfo", {}).get("smtpAddress", "")
                                user_account_info = site.get("userAccountInfo", {})
                                site_dict[site_url] = {
                                    'userAccountInfo': user_account_info,
                                    'accountStatus': site.get("accountStatus"),
                                    'discoverByType': site.get("discoverByType"),
                                    'planName': site.get("plan", {}).get("planName", "")
                                }
                    return site_dict, no_of_records
                return {}, 0
            raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def update_sites_association_properties(self, site_user_accounts_list, operation, plan_id=None):
        """Updates the association properties of site

                Args:

                    site_user_accounts_list (list)   --  list of user accounts of all sites
                                                           It has all information of sites/webs

                    operation (int)                  --  type of operation to be performed
                                                         Example: 1 - Associate
                                                                  2 - Enable
                                                                  3 - Disable
                                                                  4 - Remove

                    plan_id (int)                    --  id of office 365 plan

                Raises:

                    SDKException:

                        if response is empty

                        if response is not success

                        if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            properties_dict = self._set_properties_to_update_site_association(operation)
            self._ASSOCIATE_CONTENT = self._services['UPDATE_USER_POLICY_ASSOCIATION']
            for user_account in site_user_accounts_list:
                item_type = user_account['itemType']
                if item_type == 2 and operation == 4:
                    user_account['commonFlags'] = 6
                elif item_type == 1 and operation == 4:
                    user_account['commonFlags'] = 10
                else:
                    user_account['commonFlags'] = properties_dict['commonFlags']
                if properties_dict.get('isAutoDiscoveredUser', None) is not None:
                    user_account['isAutoDiscoveredUser'] = properties_dict['isAutoDiscoveredUser']
            request_json = {
                "cloudAppAssociation": {
                    "subclientEntity": {
                        "subclientId": int(self.subclient_id)
                    },
                    "cloudAppDiscoverinfo": {
                        "discoverByType": 6,
                        "userAccounts": site_user_accounts_list
                    }
                }
            }
            if properties_dict.get('accountStatus', None) is not None:
                request_json['cloudAppAssociation']['accountStatus'] = properties_dict['accountStatus']
            if plan_id:
                request_json['cloudAppAssociation']['plan'] = {
                    "planId": plan_id
                }
            flag, response = self._cvpysdk_object.make_request(
                'POST', self._ASSOCIATE_CONTENT, request_json
            )
            if flag:
                if response.json():
                    if "resp" in response.json():
                        error_code = response.json()['resp']['errorCode']
                        if error_code != 0:
                            error_string = response.json().get('response', {}).get('errorString', str())
                            o_str = 'Failed to associate content\nError: "{0}"'.format(error_string)
                            raise SDKException('Subclient', '102', o_str)
                    elif 'errorMessage' in response.json():
                        error_string = response.json()['errorMessage']
                        o_str = 'Failed to associate content\nError: "{0}"'.format(error_string)
                        raise SDKException('Subclient', '102', o_str)
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def delete_data(self, guids=None, search_string=None, folder_delete=False, search_and_select_all=False):
        """
        Trigger a bulk delete job or normal delete for files/folders according to input given for SharePoint V2

        Args:
            guids (list)                    --  List of file/folder object GUIDs or web GUIDs of items we are deleting
            search_string (string)          --  Search string (needed for search and delete all)
            folder_delete (bool)            --  Bool value to confirm if a folder is being deleted or not
            search_and_select_all (bool)    --  Normal delete operation or search and delete all operation
        """
        ci_state_values = ["1"]
        bulk_mode = False
        if folder_delete or search_and_select_all:
            bulk_mode = True
        if search_and_select_all:
            file_filter = [{"interGroupOP": 2,
                            "filter": {"interFilterOP": 2, "filters": [
                                {"field": "HIDDEN", "intraFieldOp": 4, "fieldValues": {"values": ["true"]}}, {
                                    "field": "SPWebGUID",
                                    "intraFieldOp": 0,
                                    "fieldValues": {"values": guids}}]}},
                           {"interGroupOP": 2, "filter": {"interFilterOP": 0,
                                                          "filters": [{
                                                              "field": "FILE_NAME",
                                                              "intraFieldOp": 0,
                                                              "fieldValues": {
                                                                  "values": [search_string, search_string + "*"]}},
                                                              {
                                                                  "field": "SPTitle",
                                                                  "intraFieldOp": 0,
                                                                  "fieldValues": {"values": [search_string,
                                                                                             search_string + "*"]}}]}}]
        else:
            ci_state_values.extend(["3333", "3334", "3335"])
            file_filter = [{"interGroupOP": 2, "filter": {"interFilterOP": 2, "filters": [
                {
                    "field": "IS_VISIBLE",
                    "intraFieldOp": 0,
                    "fieldValues": {"values": ["true"]}},
                {
                    "field": "CV_OBJECT_GUID",
                    "intraFieldOp": 0,
                    "fieldValues": {"values": guids}}]}}]

        request_json = {"opType": 1, "bulkMode": bulk_mode, "deleteOption": {"folderDelete": bulk_mode},
                        "searchReq": {
                            "mode": 4, "advSearchGrp": {"commonFilter": [{"filter": {"interFilterOP": 2,
                                                                                     "filters": [
                                                                                         {"field": "CISTATE",
                                                                                          "intraFieldOp": 0,
                                                                                          "fieldValues": {
                                                                                              "values": ci_state_values}}]}}],
                                                        "fileFilter": file_filter,
                                                        "emailFilter": [],
                                                        "galaxyFilter": [{"appIdList": [int(self.subclient_id)]}],
                                                        "graphFilter": [
                                                            {
                                                                "toField": "CV_OBJECT_GUID", "fromField": "PARENT_GUID",
                                                                "returnRoot": True,
                                                                "traversalFilter": [{"filters": [
                                                                    {"field": "IS_VISIBLE", "intraFieldOp": 2,
                                                                     "fieldValues": {"values": ["true"]}},
                                                                    {"field": "HIDDEN", "intraFieldOp": 4,
                                                                     "fieldValues": {"values": ["true"]}}]}]
                                                            }]},
                            "searchProcessingInfo": {
                                "resultOffset": 0, "pageSize": 0,
                                "queryParams": [{"param": "ENABLE_MIXEDVIEW", "value": "true"}],
                                "sortParams": []
                            }
                        }
                        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['DELETE_DOCUMENTS'], request_json
        )
        return self._process_index_delete_response(flag, response)

    def restore_in_place(self, **kwargs):
        """Runs a in-place restore job on the specified Sharepoint pseudo client
           This is used by Sharepoint V2 pseudo client

             Kwargs:

                 paths     (list)   --  list of sites or webs to be restored
                 Example: [
                    "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\Contents\\Shared Documents",
                    "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\Contents\\Test Automation List"
                    ]

             Returns:

                Job object

            Raises:

                SDKException:

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            self._instance_object._restore_association = self._subClientEntity
            parameter_dict = self._restore_json(**kwargs)
            return self._process_restore_response(parameter_dict)
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def restore_in_place_syntex(self, **kwargs):
        """Runs an in-place restore job on the specified Syntex Sharepoint pseudo client

             Kwargs:

                 paths     (list)   --  list of sites or webs to be restored
                 Example: [
                    "MB\\<tenant-url>/sites/TestSite\Contents\Shared Documents",
                    "MB\\<tenant-url>/sites/TestSite\Contents\Test Automation List"
                    ]

                 fast_restore_point   (booL)  -- Whether to use fast restore point or not
                                                 default: False
             Returns:

                Job object

            Raises:

                SDKException:

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if the method is called by SharePoint On-Premise Instance

        """
        paths = kwargs.get('paths', [])
        fast_restore_point = kwargs.get('fast_restore_point', False)

        if self._backupset_object.is_sharepoint_online_instance:
            site_dict, _ = self.browse_for_content(discovery_type=7)
            site_details = {}
            for path in paths:
                site_details[path] = site_dict[path].get('userAccountInfo', {})
            self._instance_object._restore_association = self._subClientEntity
            parameter_dict = self._restore_json(**kwargs)

            syntex_restore_items = []

            for key, value in site_details.items():
                sharepoint_item = value["EVGui_SharePointItem"][0]
                syntex_restore_items.append({
                    "displayName": value["displayName"],
                    "email": value["smtpAddress"],
                    "guid": value["user"]["userGUID"],
                    "rawId": sharepoint_item['siteId']+";"+sharepoint_item['objectId']+";"+sharepoint_item['contentPath'],
                    "restoreType": 1
                })

            # Get the current time in UTC
            current_time = datetime.datetime.now(datetime.timezone.utc)
            current_timestamp = int(current_time.timestamp())
            current_iso_format = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            parameter_dict["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = {}
            parameter_dict["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"][
                "msSyntexRestoreOptions"] = {
                "msSyntexRestoreItems": {
                    "listMsSyntexRestoreItems": syntex_restore_items
                },
                "restoreDate": {
                    "time": current_timestamp,
                    "timeValue": current_iso_format
                },
                "restorePointId": "",
                "restoreType": 1,
                "useFastRestorePoint": fast_restore_point
            }

            return self._process_restore_response(parameter_dict)
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def out_of_place_restore(
            self,
            paths,
            destination_path,
            overwrite=True,
            common_options: dict = None):
        """Restores the SharePoint list/libraries specified in the input paths list to the different site

            Args:
                paths                   (list)  --  list of paths of SharePoint list/libraries to restore

                destination_path        (str)   --  path where the SharePoint Site where list/libraries needs to be restored

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                common_options          (dict)  -- add common options for restoring all versions
            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

                    if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            restore_option = {}
            if not paths:
                raise SDKException('Subclient', '104')
            restore_option['overwrite'] = overwrite
            restore_option['paths'] = paths
            restore_option['destination_path'] = destination_path
            restore_option['in_place'] = False
            request_json = self._prepare_out_of_place_restore_json(restore_option, common_options)
            return self._process_restore_response(request_json)
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def disk_restore(
            self,
            paths,
            destination_client,
            destination_path,
            disk_restore_type,
            overwrite=True,
            in_place=False):
        """Restores the sharepoint libraries/list specified in the input paths list to the same location.

           value:
                paths                   (list)  --  list of paths of lists/libraries to restore

                destination_client      (str)    --  client where the lists/libraries needs to be restored

                destination_path        (str)    --  path where the lists/libraries needs to be restored

                disk_restore_type               --  type of disk restore

                unconditional_overwrite (bool)  --  unconditional overwrite files during restore
                    default: True

                in_place               (bool)   --  in place restore set to false by default
                    default: False

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

                    if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            restore_option = {}
            if not paths:
                raise SDKException('Subclient', '104')
            restore_option['unconditional_overwrite'] = overwrite
            restore_option['paths'] = paths
            restore_option['client'] = destination_client
            restore_option['destination_path'] = destination_path
            restore_option['disk_restore_type'] = disk_restore_type
            restore_option['in_place'] = in_place
            request_json = self._prepare_disk_restore_json(restore_option)
            return self._process_restore_response(request_json)
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def blob_restore(
            self,
            paths: list[str],
            destination_client: str,
            destination_blob: str,
            overwrite: bool = True,
            in_place: bool = False) -> Job:
        """Restores the sharepoint libraries/list specified in the input paths list to the given Azure Blob.

           value:
                paths                   (list)  --  list of paths of lists/libraries to restore

                destination_client       (str)  --  client where the lists/libraries needs to be restored

                destination_blob         (str)  --  blob where the lists/libraries needs to be restored

                unconditional_overwrite (bool)  --  unconditional overwrite files during restore
                    default: True

                in_place               (bool)   --  in place restore set to false by default
                    default: False

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

                    if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            credential = self._commcell_object.credentials.get(destination_blob)
            if credential is None:
                raise SDKException('Subclient', '102', f'Credential "{destination_blob}" not found')
            restore_option = {
                'paths': paths,
                'unconditional_overwrite': overwrite,
                'client': destination_client,
                'in_place': in_place,
                'blob_container_id': credential.credential_id}
            request_json = self._prepare_blob_restore_json(restore_option)
            return self._process_restore_response(request_json)
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def process_index_retention_rules(self, index_server_client_id):
        """Makes API call to process index retention rules

         Args:
                index_server_client_id (int)  --  client id of index server

        Raises:

                SDKException:

                    if response is empty

                    if response is not success

                    if the method is called by SharePoint On-Premise Instance

        """
        if self._backupset_object.is_sharepoint_online_instance:
            request_json = {
                "appType": int(self._agent_object.agent_id),
                "subclientId": int(self.subclient_id),
                "indexServerClientId": index_server_client_id
            }
            flag, response = self._cvpysdk_object.make_request(
                'POST', self._services['OFFICE365_PROCESS_INDEX_RETENTION_RULES'], request_json
            )
            if flag:
                if response.json():
                    if "resp" in response.json():
                        error_code = response.json()['resp']['errorCode']
                        if error_code != 0:
                            error_string = response.json()['response']['errorString']
                            o_str = 'Failed to process index retention rules\nError: "{0}"'.format(error_string)
                            raise SDKException('Subclient', '102', o_str)
                    elif 'errorMessage' in response.json():
                        error_string = response.json()['errorMessage']
                        o_str = 'Failed to process index retention rules\nError: "{0}"'.format(error_string)
                        raise SDKException('Subclient', '102', o_str)
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException('Subclient', '102', 'Method not supported for SharePoint On-Premise Instance')

    def refresh_license_collection(self):

        """
        Method is used to update the License collection status

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        payload = {
            "subClient": {
                "clientId": int(self._client_object.client_id),
                "backupsetId": int(self._subClientEntity.get('backupsetId'))
            }
        }

        api_url = self._services['LICENSE_COLLECTION']
        flag, response = self._cvpysdk_object.make_request(method='POST',
                                                           url=api_url, payload=payload)
        if not flag:
            raise SDKException('Response', '101',
                               self._commcell_object._update_response_(response.text))
        if not response:
            raise SDKException('Response', '102',
                               self._commcell_object._update_response_(response.text))

    def preview_backedup_file(self, file_path):
        """Gets the preview content for the subclient.

            Returns:
                html   (str)   --  html content of the preview

            Raises:
                SDKException:
                    if file is not found

                    if response is empty

                    if response is not success
        """
        return self._get_preview(file_path)


class SharepointV1Subclient(SharepointSuperSubclient):
    """Derived class from Subclient Base class, representing a Sharepoint v1 subclient,
            and to perform operations on that subclient."""

    def discover_sharepoint_sites(self, paths):
        """Checks whether SP content i.e, sites/webs are available

                    Args:
                            paths (list)          --      list of paths of SharePoint sites to be checked

                """
        request_json = {
            "opType": 0,
            "session": {
                "sessionId": ""
            },
            "paths": [{"path": path} for path in paths],
            "entity": {
                "clientId": int(self._client_object.client_id),
                "applicationId": int(self._agent_object.agent_id),
                "instanceId": int(self._instance_object.instance_id),
                "backupsetId": int(self._backupset_object.backupset_id),
            },
            "advOptions": {
                "advConfig": {
                    "applicationMining": {
                        "isApplicationMiningReq": True,
                        "appType": int(self._agent_object._agent_id),
                        "agentVersion": 2013,
                        "browseReq": {
                            "spBrowseReq": {
                                "spBrowseType": 2,
                                "spBrowseLevel": 1
                            }
                        }
                    }
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)
        if flag:
            if response and response.json():
                response = response.json()
                if len(response['browseResponses'][0]['browseResult']['advConfig']['applicationMining']['browseResp'][
                           'spBrowseResp']['dataPathContents']) > 0:
                    return \
                        response['browseResponses'][0]['browseResult']['advConfig']['applicationMining']['browseResp'][
                            'spBrowseResp']['dataPathContents']
                else:
                    raise SDKException('Sites not found')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """

        return self._content

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add a new Sharepoint server Subclient
            with the content passed in subclient content.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

        """

        self._set_subclient_properties("_content", subclient_content)

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "subClientEntity": self._subClientEntity,
                    "sharepointsubclientprop": self._sharepoint_subclient_prop,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1,
                    "planEntity": self._planEntity,
                },
            "association": {
                "entity": [
                    {
                        "subclientId": int(self.subclient_id),
                        "applicationId": self._subClientEntity["applicationId"],
                        "backupsetId": int(self._backupset_object.backupset_id),
                        "instanceId": int(self._instance_object.instance_id),
                        "clientId": int(self._client_object.client_id),
                        "subclientName": self.subclient_name
                    }
                ]
            }
        }
        return subclient_json

    def restore_in_place(self, **kwargs):
        """Runs a in-place restore job on the specified Sharepoint pseudo client
           This is used by Sharepoint V2 pseudo client

             Kwargs:

                 paths     (list)   --  list of sites or webs to be restored
                 Example: [
                    "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\Contents\\Shared Documents",
                    "MB\\https://<tenant_name>.sharepoint.com/sites/TestSite\\Contents\\Test Automation List"
                    ]

             Returns:

                Job object

            Raises:

                SDKException:

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if the method is called by SharePoint On-Premise Instance

        """
        self._instance_object._restore_association = self._subClientEntity
        parameter_dict = self._restore_json(**kwargs, v1=True)
        return self._process_restore_response(parameter_dict)

    def out_of_place_restore(
            self,
            paths,
            destination_path,
            overwrite=True):
        """Restores the SharePoint list/libraries specified in the input paths list to the different site

            Args:
                paths                   (list)  --  list of paths of SharePoint list/libraries to restore

                destination_path        (str)   --  path where the SharePoint Site where list/libraries needs to be restored

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success


        """
        restore_option = {}
        if not paths:
            raise SDKException('Subclient', '104')
        restore_option['overwrite'] = overwrite
        restore_option['paths'] = paths
        restore_option['destination_path'] = destination_path
        restore_option['in_place'] = False
        request_json = self._prepare_out_of_place_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def _prepare_out_of_place_restore_json(self, _restore_option):
        """
        Prepare out of place retsore Json with all getters

        Args:
            _restore_option - dictionary with all out of place restore options

            value:

                paths (list)            --  list of paths of SharePoint list/libraries to restore

                destination_path (str)  --  path where the SharePoint Site where list/libraries needs to be restored

                overwrite (bool)        --  unconditional overwrite files during restore
                    default: True


        returns:
            request_json        -  complete json for performing disk Restore options

        """

        if _restore_option is None:
            _restore_option = {}

        paths = self._filter_paths(_restore_option['paths'])
        self._json_out_of_place_destination_option(_restore_option)
        _restore_option['paths'] = paths

        # set the setters
        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_restore_option, v1=True)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions'][
            'destination'] = self._out_of_place_destination_json
        return request_json
