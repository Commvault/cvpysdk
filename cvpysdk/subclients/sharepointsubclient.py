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

SharepointSubclient is the only class defined in this file.

SharepointSubclient: Derived class from Subclient Base class, representing a sharepoint subclient,
and to perform operations on that subclient

SharepointSubclient:

    _get_subclient_properties()         --  gets the subclient related properties of the Sharepoint subclient.

    _get_subclient_properties_json()    --  gets all the subclient related properties of the Sharepoint subclient.

    _process_restore_response           --  processes response received for the restore request.

    _restore_request_json               --  returns the JSON request to pass to the API as per the options.

    sharepoint_subclient_prop()         --  initializes additional properties of this subclient.

    content()                           --  sets the content of the subclient.

    restore()                           --  restores the databases specified in the input paths list.

    run_manual_discovery()              --  runs the manual disocvery for specified backupset

    browse_for_content()                --  returns the user association content

    associate_site_collections_and_webs()-- associates the specified site collections/webs

    restore_in_place()                  --  runs a in-place restore job on the specified Sharepoint pseudo client

"""

from __future__ import unicode_literals
from base64 import b64encode
from ..subclient import Subclient
from ..exception import SDKException
from ..constants import SQLDefines
from ..constants import SharepointDefines


class SharepointSubclient(Subclient):
    """Derived class from Subclient Base class, representing a Sharepoint subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient related properties of the Sharepoint subclient.

        """
        super(SharepointSubclient, self)._get_subclient_properties()

        self._sharepoint_subclient_prop = self._subclient_properties.get('sharepointsubclientprop', {})
        self._content = self._subclient_properties.get('content', {})

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
            request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
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
        request_json = self._restore_json(restore_option=_restore_option)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions'][
            'destination'] = self._out_of_place_destination_json
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
                        o_str = 'Failed to set category based content for association\nError: "{0}"'.format(error_string)
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
                            error_string = response.json()['response']['errorString']
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

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               collect_metadata=False,
               advanced_options=None):
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

        if advanced_options:
            request_json = self._backup_json(
                backup_level=backup_level,
                incremental_backup=incremental_backup,
                incremental_level=incremental_level,
                advanced_options=advanced_options
            )
            backup_service = self._commcell_object._services['CREATE_TASK']

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

            return self._process_backup_response(flag, response)

        else:
            return super(SharepointSubclient, self).backup(backup_level=backup_level,
                                                           incremental_backup=incremental_backup,
                                                           incremental_level=incremental_level,
                                                           collect_metadata=collect_metadata)

    def restore_in_place(self, **kwargs):
        """Runs a in-place restore job on the specified Sharepoint pseudo client
           This is used by Sharepoint V2 pseudo client

             Kwargs:

                 paths     (list)   --  list of sites or webs to be restored
                 Example: [
                    "MB\\https://cvdevtenant.sharepoint.com/sites/TestSite\Contents\Shared Documents",
                    "MB\\https://cvdevtenant.sharepoint.com/sites/TestSite\Contents\Test Automation List"
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
            request_json = self._prepare_out_of_place_restore_json(restore_option)
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

                destination_client              --  client where the lists/libraries needs to be restored

                destination_path                --  path where the lists/libraries needs to be restored

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
