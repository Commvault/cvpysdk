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

"""File for operating on a OneDrive Subclient.

OneDriveSubclient is the only class defined in this file.

OneDriveSubclient:    Derived class from CloudAppsSubclient Base class, representing a
OneDrive subclient, and to perform operations on that subclient

OneDriveSubclient:

    content()                                                           --  gets the content of the subclient

    groups()                                                            --  gets the groups associated with the subclient

    restore_out_of_place()                                              --  runs out-of-place restore for the subclient

    discover()                                                          --  runs user discovery on subclient

    add_AD_group()                                                      --  adds AD group to the subclient

    add_user()                                                          --  adds user to the subclient

    add_users_onedrive_for_business_client()                            --  Adds user to OneDrive for Business Client

    search_for_user()                                                   --  Searches for a specific user's details from
                                                                            discovered list

    disk_restore_onedrive_for_business_client()                         --  Runs disk restore of selected users for
                                                                            OneDrive for Business Client

    out_of_place_restore_onedrive_for_business_client()                 --  Runs out-of-place restore of selected users
                                                                            for OneDrive for Business Client

    in_place_restore_onedrive_syntex()          --  Runs in-place restore of selected users for Syntex OneDrive for Business Client

    in_place_restore_onedrive_for_business_client()               --  Runs in-place restore of selected users for OneDrive for Business Client

    _get_user_guids()                                                   --  Retrieve GUIDs for users specified

    _task_json_for_onedrive_backup()                                    --  Json for onedrive backup for selected users

    _association_users_json()                                           --  user association

    point_in_time_in_place_restore_onedrive_for_business_client()       -- Runs PIT in-place restore of selected users

    point_in_time_out_of_place_restore_onedrive_for_business_client()   -- Runs PIT out of place restore of selected users

    run_user_level_backup_onedrive_for_business_client()                --  Runs the backup for the users in users list

    _get_user_details()                                                 --   gets user details from discovery

    _get_group_details()                                                --   gets group details from discovery

    browse_for_content()                                                --  Returns the Onedrive client content i.e.
                                                                            users/group information that is discovered
                                                                            in auto discovery phase

    _set_properties_to_update_site_association()                        --   Updates the association properties of user

    update_users_association_properties()                               --   Updates the association properties of user

    manage_custom_category()                                            --   Adds or Edits Custom category in the office 365 app

    update_custom_categories_association_properties()                   --  Updates the association properties of custom category

    refresh_retention_stats()                                           --  refresh the retention stats for the client

    refresh_client_level_stats()                                        --  refresh the client level stats for the client

    get_client_level_stats()                                            --  Returns the client level stats for the client

"""

from __future__ import unicode_literals

import datetime

from ...exception import SDKException
import time
from ..casubclient import CloudAppsSubclient
from ...constants import AppIDAType
from .onedrive_constants import OneDriveConstants as constants
import re

class OneDriveSubclient(CloudAppsSubclient):
    """Derived class from CloudAppsSubclient Base class, representing a OneDrive subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.."""
        super(OneDriveSubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

        content = []
        group_list = []

        for account in self._content:
            temp_account = account["cloudconnectorContent"]["includeAccounts"]

            if temp_account['contentType'] == AppIDAType.CLOUD_APP.value:
                content_dict = {
                    'SMTPAddress': temp_account["contentName"].split(";")[0],
                    'display_name': temp_account["contentValue"]
                }

                content.append(content_dict)
            if temp_account['contentType'] == 135:
                group_list.append(temp_account["contentName"])
        self._ca_content = content
        self._ca_groups = group_list

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """

        return {'subClientProperties': self._subclient_properties}

    def _association_users_json(self, users_list):
        """
            Args:
                users_list (list) : list of SMTP addresses of users
            Returns:
                users_json(list): Required details of users to backup
        """
        users_json = []
        for user_smtp in users_list:
            user_details=self._get_user_details(user_smtp)
            user_info={
                      "user": {
                        "userGUID": user_details[0].get('user', {}).get('userGUID')
                      }
            }
            users_json.append(user_info)
        return users_json

    def _task_json_for_onedrive_backup(self, users_list, custom_groups_list=[]):
        """
        Json for onedrive backup for selected users

        Args:
                users_list (list) : list of SMTP addresses of users
                custom_groups_list (list) : list of custom category groups
        """
        groups, _ = self.browse_for_content(discovery_type=31)
        associated_users_json = self._association_users_json(users_list)

        associated_custom_groups_json = []
        if len(custom_groups_list) != 0:
            for group in custom_groups_list:
                group_info = {
                    "id": groups[group].get('id', None),
                    "name": group
                }
                associated_custom_groups_json.append(group_info)

        advanced_options_dict = {
            'cloudAppOptions': {
                'userAccounts': associated_users_json,
                'userGroups': associated_custom_groups_json
            }
        }

        selected_items=[]
        for user_smtp in users_list:
            details=self._get_user_details(user_smtp)
            item={
                "itemName": details[0].get('displayName'),
                "itemType": "User"
            }
            selected_items.append(item)

        for group in custom_groups_list:
            item={
                "itemName": group,
                "itemtype": "Custom category"
            }
            selected_items.append(item)

        common_options_dict={
            "jobMetadata": [
                {
                    "selectedItems": selected_items,
                    "jobOptionItems": [
                        {
                            "option": "Total running time",
                            "value": "Disabled"
                        }
                    ]
                }
            ]
        }

        task_json = self._backup_json(backup_level='INCREMENTAL',incremental_backup=False,incremental_level='BEFORE_SYNTH',advanced_options=advanced_options_dict,common_backup_options=common_options_dict)
        return task_json

    @property
    def content(self):
        """Returns the subclient content dict"""
        return self._ca_content

    @property
    def groups(self):
        """Returns the list of groups assigned to the subclient if any.
        Groups are assigned only if auto discovery is enabled for groups.

            Returns:

                list - list of groups associated with the subclient

        """
        return self._ca_groups

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Cloud Apps Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient
                                              contains the account info for each user in list.

                                              example temp_content_dict={
                                                "cloudconnectorContent": {
                                                  "includeAccounts": {
                                                    "contentValue": Automation User,
                                                    "contentType": 134,
                                                    "contentName": automation_user@automationtenant.com
                                                     }
                                                  }
                                              }

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        try:
            for account in subclient_content:
                temp_content_dict = {
                    "cloudconnectorContent": {
                        "includeAccounts": {
                            "contentValue": account['display_name'],
                            "contentType": AppIDAType.CLOUD_APP.value,
                            "contentName": account['SMTPAddress']
                        }
                    }
                }

                content.append(temp_content_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        self._set_subclient_properties("_content", content)

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
        self._instance_object._restore_association = self._subClientEntity

        return self._instance_object.restore_out_of_place(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            to_disk=to_disk
        )

    def discover(self, discover_type='USERS'):
        """This method discovers the users/groups on OneDrive

                Args:

                    discover_type (str)  --  Type of discovery

                        Valid Values are

                        -   USERS
                        -   GROUPS

                        Default: USERS

                Returns:

                    List (list)  --  List of users on GSuite account

                Raises:
                    SDKException:
                        if response is empty

                        if response is not success


        """

        if discover_type.upper() == 'USERS':
            disc_type = 10
        elif discover_type.upper() == 'GROUPS':
            disc_type = 5
        _get_users = self._services['GET_CLOUDAPPS_USERS'] % (self._instance_object.instance_id,
                                                              self._client_object.client_id,
                                                              disc_type)

        flag, response = self._cvpysdk_object.make_request('GET', _get_users)
        if flag:
            if response.json() and "scDiscoveryContent" in response.json():
                self._discover_properties = response.json()[
                    "scDiscoveryContent"][0]

                if "contentInfo" in self._discover_properties:
                    self._contentInfo = self._discover_properties["contentInfo"]
                return self._contentInfo
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def set_auto_discovery(self, value):
        """Sets the auto discovery value for subclient.
        You can either set a RegEx value or a user group,
        depending on the auto discovery type selected at instance level.

            Args:

                value   (list)  --  List of RegEx or user groups

        """

        if not isinstance(value, list):
            raise SDKException('Subclient', '116')

        if not self._instance_object.auto_discovery_status:
            raise SDKException('Subclient', '117')

        subclient_prop = self._subclient_properties['cloudAppsSubClientProp'].copy()
        if self._instance_object.auto_discovery_mode == 0:
            # RegEx based auto discovery is enabled on instance

            subclient_prop['oneDriveSubclient']['regularExp'] = value
            self._set_subclient_properties("_subclient_properties['cloudAppsSubClientProp']", subclient_prop)
        else:
            # User group based auto discovery is enabled on instance
            grp_list = []
            groups = self.discover(discover_type='GROUPS')
            for item in value:
                for group in groups:
                    if group['contentName'].lower() == item.lower():
                        grp_list.append({
                            "cloudconnectorContent": {
                                "includeAccounts": group
                            }
                        })
            self._content.extend(grp_list)
            self._set_subclient_properties("_subclient_properties['content']", self._content)
        self.refresh()

    def run_subclient_discovery(self):
        """
            This method launches AutoDiscovery on the subclient
        """

        discover_type = 15
        discover_users = self._services['GET_CLOUDAPPS_ONEDRIVE_USERS'] % (self._instance_object.instance_id,
                                                                           self._client_object.client_id,
                                                                           discover_type,
                                                                           self.subclient_id)
        flag, response = self._cvpysdk_object.make_request('GET', discover_users)
        if response.status_code != 200 and response.status_code != 500:
            raise SDKException('Response', '101')

    def add_AD_group(self, value):
        """Adds the user group to the subclient if auto discovery type selected
            AD group at instance level.
                Args:
                    value   (list)  --  List of user groups
        """
        grp_list = []
        groups = self.discover(discover_type='GROUPS')
        for item in value:
            for group in groups:
                if group['contentName'].lower() == item.lower():
                    grp_list.append(group)

        contentinfo = []

        for grp in grp_list:
            info = {
                "contentValue": grp['contentValue'],
                "contentType": grp['contentType'],
                "contentName": grp['contentName']
            }
            contentinfo.append(info)

        request_json = {
            "App_DiscoveryContent": {
                "scDiscoveryContent": [
                    {
                        "scEntity": {
                            "subclientId": self.subclient_id
                        },
                        "contentInfo": contentinfo
                    }
                ]
            }
        }
        add_ADgroup = self._services['EXECUTE_QCOMMAND']
        flag, response = self._cvpysdk_object.make_request('POST', add_ADgroup, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    raise SDKException('Response', '101')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_user(self, user_name):
        """This method adds one drive user to the subclient
                Args:
                    user_name   (str)  --  Onedrive user name
        """
        users = self.discover(discover_type='USERS')

        for user in users:
            if user['contentName'].lower() == user_name.lower():
                user_dict = user
                break

        request_json = {
            "App_DiscoveryContent": {
                "scDiscoveryContent": [
                    {
                        "scEntity": {
                            "subclientId": self.subclient_id
                        },
                        "contentInfo": [
                            {
                                "contentValue": user_dict['contentValue'],
                                "contentType": user_dict['contentType'],
                                "contentName": user_dict['contentName']
                            }
                        ]
                    }
                ]
            }
        }

        add_user = self._services['EXECUTE_QCOMMAND']
        flag, response = self._cvpysdk_object.make_request('POST', add_user, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = 'Failed to user to the subclient\nError: "{0}"'
                    raise SDKException('Subclient', '102', output_string.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_subclient_users(self):
        """Method to get the users in the subclient

            Returns:
                List of Users in subclient
        """
        users = []
        result = self.content
        for user in result:
            users.append(user['SMTPAddress'])
        return users

    @property
    def get_subclient_users(self):
        """Returns the users in subclient"""
        return self._get_subclient_users()

    def add_ad_group_onedrive_for_business_client(self,value,plan_name):
        """ Adds given OneDrive group to v2 client

            Args:

                value (string) : Group name

                plan_name (str) : O365 plan name to associate with users

            Raises:

                SDKException:

                    if response is not success

                    if response is returned with errors
        """
        # Get o365plan
        plan_name = plan_name.strip()
        o365_plan_object = self._commcell_object.plans.get(plan_name)
        o365_plan_id = int(o365_plan_object.plan_id)

        # Get client id
        client_id = int(self._client_object.client_id)

        groups = []
        group_response = self.search_for_group(group_id=value)
        display_name = group_response[0].get('name')
        group_id = group_response[0].get('id')

        groups.append({
            "name": display_name,
            "id": group_id
        })

        request_json = {
            "LaunchAutoDiscovery": True,
            "cloudAppAssociation": {
                "accountStatus": 0,
                "subclientEntity": {
                    "subclientId": int(self.subclient_id),
                    "clientId": client_id,
                    "applicationId": AppIDAType.CLOUD_APP.value
                },
                "cloudAppDiscoverinfo": {
                    "discoverByType": 2,
                    "groups": groups
                },
                "plan": {
                    "planId": o365_plan_id
                }
            }
        }

        user_associations = self._services['UPDATE_USER_POLICY_ASSOCIATION']
        flag, response = self._cvpysdk_object.make_request('POST', user_associations, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to add group\nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_users_onedrive_for_business_client(self, users, plan_name):
        """ Adds given OneDrive users to v2 client

            Args:

                users (list) : List of user's SMTP address

                plan_name (str) : O365 plan name to associate with users

            Raises:

                SDKException:

                    if response is not success

                    if response is returned with errors
        """

        if not (isinstance(users, list) and isinstance(plan_name, str)):
            raise SDKException('Subclient', '101')

        # Get o365plan
        plan_name = plan_name.strip()
        o365_plan_object = self._commcell_object.plans.get(plan_name)
        o365_plan_id = int(o365_plan_object.plan_id)

        # Get client ID
        client_id = int(self._client_object.client_id)

        user_accounts = []

        for user_id in users:
            # Get user details
            user_response = self.search_for_user(user_id)
            display_name = user_response[0].get('displayName')
            user_guid = user_response[0].get('user').get('userGUID')
            is_auto_discovered_user = user_response[0].get('isAutoDiscoveredUser')
            is_super_admin = user_response[0].get('isSuperAdmin')

            user_accounts.append({
                "displayName": display_name,
                "isSuperAdmin": is_super_admin,
                "smtpAddress": user_id,
                "isAutoDiscoveredUser": is_auto_discovered_user,
                "associated": False,
                "commonFlags": 0,
                "user": {
                    "userGUID": user_guid
                }
            })

        request_json = {
            "LaunchAutoDiscovery": False,
            "cloudAppAssociation": {
                "accountStatus": 0,
                "subclientEntity": {
                    "subclientId": int(self.subclient_id),
                    "clientId": client_id,
                    "applicationId": AppIDAType.CLOUD_APP.value
                },
                "cloudAppDiscoverinfo": {
                    "discoverByType": 1,
                    "userAccounts": user_accounts
                },
                "plan": {
                    "planId": o365_plan_id
                }
            }
        }

        user_associations = self._services['UPDATE_USER_POLICY_ASSOCIATION']
        flag, response = self._cvpysdk_object.make_request('POST', user_associations, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to add user\nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def verify_discovery_onedrive_for_business_client(self):
        """ Verifies that discovery is complete

            Returns:

                discovery_stats (tuple):

                    discovery_status (bool): True if users are discovered else returns False

                    total_records (int):     Number of users fetched, returns -1 if discovery is not complete

            Raises:

                 SDKException:

                        if response is not success

                        if response received does not contain pagining info
        """

        browse_content = (self._services['CLOUD_DISCOVERY'] % (self._instance_object.instance_id,
                                                               self._client_object.client_id,
                                                               AppIDAType.CLOUD_APP.value))

        # determines the number of accounts to return in response
        page_size = 1
        discover_query = f'{browse_content}&pageSize={page_size}'

        flag, response = self._cvpysdk_object.make_request('GET', discover_query)

        if flag:
            no_of_records = -1
            if response and response.json():
                if 'pagingInfo' in response.json():
                    no_of_records = response.json().get('pagingInfo', {}).get('totalRecords', -1)
                    if no_of_records > 0:
                        return True, no_of_records
            return False, no_of_records
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def search_for_user(self, user_id):
        """ Searches for a specific user's details from discovered list

            Args:
                user_id (str) : user's SMTP address

            Returns:

                user_accounts (list): user details' list fetched from discovered content
                              eg: [
                                      {
                                        'displayName': '',
                                        'smtpAddress': '',
                                        'isSuperAdmin': False,
                                        'isAutoDiscoveredUser': False,
                                        'commonFlags': 0,
                                        'user': {
                                            '_type_': 13,
                                             'userGUID': 'UserGuid'
                                             }
                                       }
                                  ]

            Raises:

                SDKException:

                    if discovery is not complete

                    if invalid SMTP address is passed

                    if response is empty

                    if response is not success
        """
        browse_content = (self._services['CLOUD_DISCOVERY'] % (self._instance_object.instance_id,
                                                               self._client_object.client_id,
                                                               AppIDAType.CLOUD_APP.value))


        search_query = f'{browse_content}&search={user_id}'

        flag, response = self._cvpysdk_object.make_request('GET', search_query)

        if flag:
            if response and response.json():
                if 'userAccounts' in response.json():
                    user_accounts = response.json().get('userAccounts', [])
                    if len(user_accounts) == 0:
                        error_string = 'Either discovery is not complete or user is not available in discovered data'
                        raise SDKException('Subclient', '102', error_string)
                    return user_accounts
                else:
                    raise SDKException('Response', '102', 'Check if the user provided is valid')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def search_for_group(self, group_id):
        """ Searches for a specific group details from discovered list

            Args:
                group_id (str) : group name

            Returns:

                groups (list): group details' list fetched from discovered content
                              eg: [
                                      {
                                         "name": "g1",
                                         "id": "df1f794a-ceee-4e91-b644-6f34a0416917"
                                       }
                                  ]

            Raises:

                SDKException:

                    if discovery is not complete

                    if invalid SMTP address is passed

                    if response is empty

                    if response is not success
        """
        browse_content = (self._services['GET_CLOUDAPPS_USERS'] % (self._instance_object.instance_id,
                                                              self._client_object.client_id,
                                                              5))

        search_query = f'{browse_content}&search={group_id}'

        flag, response = self._cvpysdk_object.make_request('GET', search_query)

        if flag:
            if response and response.json():
                if 'groups' in response.json():
                    groups = response.json().get('groups', [])
                    if len(groups) == 0:
                        error_string = 'Either discovery is not complete or group is not available in discovered data'
                        raise SDKException('Subclient', '102', error_string)
                    return groups
                else:
                    raise SDKException('Response', '102', 'Check if the group provided is valid')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def disk_restore_onedrive_for_business_client(self, users, destination_client, destination_path, skip_file_permissions=False):
        """ Runs an out-of-place restore job for specified users on OneDrive for business client
            By default restore skips the files already present in destination

            Args:
                users (list) : list of SMTP addresses of users
                destination_client (str) : client where the users need to be restored
                destination_path (str) : Destination folder location
                skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)

            Returns:
                object - instance of the Job class for this restore job
        """
        self._instance_object._restore_association = self._subClientEntity
        source_user_list = self._get_user_guids(users)
        kwargs = {
            'disk_restore': True,
            'destination_path': destination_path,
            'destination_client': destination_client,
            'skip_file_permissions': skip_file_permissions
        }
        restore_json = self._instance_object._prepare_restore_json_onedrive_for_business_client(source_user_list, **kwargs)
        return self._process_restore_response(restore_json)

    def out_of_place_restore_onedrive_for_business_client(self, users, destination_path, **kwargs):
        """ Runs an out-of-place restore job for specified users on OneDrive for business client
            By default restore skips the files already present in destination

            Args:
                users (list) : list of SMTP addresses of users
                destination_path (str) : SMTP address of destination user
                **kwargs (dict) : Additional parameters
                    overwrite (bool) : unconditional overwrite files during restore (default: False)
                    restore_as_copy (bool) : restore files as copy during restore (default: False)
                    skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if overwrite and restore as copy file options are both selected
        """
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', True)
        include_deleted_items = kwargs.get('include_deleted_items',False)

        if overwrite and restore_as_copy:
            raise SDKException('Subclient', '102', 'Either select overwrite or restore as copy for file options')

        self._instance_object._restore_association = self._subClientEntity
        source_user_list = self._get_user_guids(users)
        kwargs = {
            'out_of_place': True,
            'destination_path': destination_path,
            'overwrite': overwrite,
            'restore_as_copy': restore_as_copy,
            'skip_file_permissions': skip_file_permissions,
            'include_deleted_items': include_deleted_items
        }
        restore_json = self._instance_object._prepare_restore_json_onedrive_for_business_client(source_user_list, **kwargs)

        return self._process_restore_response(restore_json)

    def in_place_restore_onedrive_syntex(self, users):
        """ Runs an in-place restore job for specified users on Syntex OneDrive for business client

            Args:
                users (list) :  List of SMTP addresses of users

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if restore job failed

                    if response is empty

                    if response is not success
        """

        user_details = {}
        for user in users:
            user_details[user] = self.search_for_user(user)

        self._instance_object._restore_association = self._subClientEntity

        syntex_restore_items = []
        for key, value in user_details.items():
            syntex_restore_items.append({
                "displayName": value[0]["displayName"],
                "email": value[0]["smtpAddress"],
                "guid": value[0]["user"]["userGUID"],
                "rawId": value[0]["user"]["userGUID"],
                "restoreType": 1
            })

        source_user_list = self._get_user_guids(users)
        restore_json = self._instance_object._prepare_restore_json_onedrive_for_business_client(source_user_list)

        # Get the current time in UTC
        current_time = datetime.datetime.now(datetime.timezone.utc)
        current_timestamp = int(current_time.timestamp())
        current_iso_format = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"][
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
            "useFastRestorePoint": True
        }

        return self._process_restore_response(restore_json)

    def in_place_restore_onedrive_for_business_client(self, users, **kwargs):
        """ Runs an in-place restore job for specified users on OneDrive for business client
            By default restore skips the files already present in destination

            Args:
                users (list) :  List of SMTP addresses of users
                **kwargs (dict) : Additional parameters
                    overwrite (bool) : unconditional overwrite files during restore (default: False)
                    restore_as_copy (bool) : restore files as copy during restore (default: False)
                    skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if overwrite and restore as copy file options are both selected
        """
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', True)
        include_deleted_items = kwargs.get('include_deleted_items',False)
        if overwrite and restore_as_copy:
            raise SDKException('Subclient', '102', 'Either select overwrite or restore as copy for file options')

        self._instance_object._restore_association = self._subClientEntity
        source_user_list = self._get_user_guids(users)
        kwargs = {
            'overwrite': overwrite,
            'restore_as_copy': restore_as_copy,
            'skip_file_permissions': skip_file_permissions,
            'include_deleted_items': include_deleted_items
        }

        restore_json = self._instance_object._prepare_restore_json_onedrive_for_business_client(source_user_list, **kwargs)
        return self._process_restore_response(restore_json)



    def _get_user_guids(self, users):
        """ Retrieve GUIDs for users specified

            Args:
                user (list) : List of SMTP addresses of users

            Returns:
                user_guid_list (list) : list of GUIDs of specified users

            Raises:
                SDKException:
                    if user details couldn't be found in discovered data
        """
        user_guid_list = []
        for user_id in users:
            user = self.search_for_user(user_id)
            if len(user) != 0 and user[0].get('user', {}).get('userGUID') is not None:
                user_guid_list.append(user[0].get('user').get('userGUID'))
            else:
                raise SDKException('Subclient', '102', 'User details not found in discovered data')
        return user_guid_list

    def process_index_retention_rules(self, index_app_type_id, index_server_client_name):
        """
         Makes API call to process index retention rules

         Args:

            index_app_type_id           (int)   --   index app type id

            index_server_client_name    (str)   --  client name of index server

         Raises:

                SDKException:

                    if index server not found

                    if response is empty

                    if response is not success
        """
        if self._commcell_object.clients.has_client(index_server_client_name):
            index_server_client_id = int(self._commcell_object.clients[index_server_client_name.lower()]['id'])
            request_json = {
                "appType": index_app_type_id,
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
            raise SDKException('IndexServers', '102')

    def point_in_time_in_place_restore_onedrive_for_business_client(self, users, end_time, **kwargs):
        """ Runs an in-place point in time restore job for specified users on OneDrive for business client
            By default restore skips the files already present in destination

            Args:
                users (list) :  List of SMTP addresses of users
                end_time (int) : Backup job end time
                **kwargs (dict) : Additional parameters
                    overwrite (bool) : unconditional overwrite files during restore (default: False)
                    restore_as_copy (bool) : restore files as copy during restore (default: False)
                    skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)
            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if overwrite and restore as copy file options are both selected
        """

        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', False)

        if overwrite and restore_as_copy:
            raise SDKException('Subclient', '102', 'Either select overwrite or restore as copy for file options')

        self._instance_object._restore_association = self._subClientEntity
        source_user_list = self._get_user_guids(users)
        kwargs = {
            'overwrite': overwrite,
            'restore_as_copy': restore_as_copy,
            'skip_file_permissions': skip_file_permissions
        }

        restore_json = self._instance_object._prepare_restore_json_onedrive_for_business_client(source_user_list, **kwargs)

        adv_search_bkp_time_dict={
                "field": "BACKUPTIME",
                "fieldValues": {
                    "values": [
                        "0",
                        str(end_time)
                    ]
                },
                "intraFieldOp": "FTOr"
            }


        add_to_time=restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]
        add_to_time["timeRange"]={"toTime":end_time}
        add_backup_time=restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"]["googleRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0]["filter"]["filters"]
        add_backup_time.append(adv_search_bkp_time_dict)

        return self._instance_object._process_restore_response(restore_json)

    def point_in_time_out_of_place_restore_onedrive_for_business_client(self, users, end_time, destination_path, **kwargs):
        """ Runs an out-of-place point in time restore job for specified users on OneDrive for business client
            By default restore skips the files already present in destination

            Args:
                users (list) : list of SMTP addresses of users
                end_time (int) : Backup job end time
                destination_path (str) : SMTP address of destination user
                **kwargs (dict) : Additional parameters
                    overwrite (bool) : unconditional overwrite files during restore (default: False)
                    restore_as_copy (bool) : restore files as copy during restore (default: False)
                    skip_file_permissions (bool) : If True, restore of file permissions are skipped (default: False)

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if overwrite and restore as copy file options are both selected
        """
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', False)

        if overwrite and restore_as_copy:
            raise SDKException('Subclient', '102', 'Either select overwrite or restore as copy for file options')

        self._instance_object._restore_association = self._subClientEntity
        source_user_list = self._get_user_guids(users)
        kwargs = {
            'out_of_place': True,
            'destination_path': destination_path,
            'overwrite': overwrite,
            'restore_as_copy': restore_as_copy,
            'skip_file_permissions': skip_file_permissions
        }
        restore_json = self._instance_object._prepare_restore_json_onedrive_for_business_client(source_user_list, **kwargs)

        adv_search_bkp_time_dict = {
            "field": "BACKUPTIME",
            "fieldValues": {
                "values": [
                    "0",
                    str(end_time)
                ]
            },
            "intraFieldOp": "FTOr"
        }

        add_to_time=restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]
        add_to_time["timeRange"]={"toTime":end_time}
        add_backup_time=restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"]["googleRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0]["filter"]["filters"]
        add_backup_time.append(adv_search_bkp_time_dict)

        return self._process_restore_response(restore_json)

    def run_user_level_backup_onedrive_for_business_client(self,users_list, custom_groups_list=[]):
        """
        Runs the backup for the users in users list/ custom categories list
        Args:
                users_list (list) : list of SMTP addresses of users
                custom_groups_list (lis) : list of custom categories

        Returns:
                object - instance of the Job class for this backup job
 
        Raises:
            SDKException:
                if response is empty
 
                if response is not success

        """
        task_json = self._task_json_for_onedrive_backup(users_list, custom_groups_list)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)

    def _get_user_details(self,user):
        """
        gets user details from discovery
        Args:
                user (str) : SMTP address of user

        Returns:
                user_details  (dict) : User's details fetched from discovery
 
        Raises:
            SDKException:
                if response is empty
        """
        user_details=self.search_for_user(user)
        if len(user_details)!=0:
            return user_details
        else:
            raise SDKException('Subclient', '102', 'User details not found in discovered data')

    def _get_group_details(self,group):
        """
        gets group details from discovery
        Args:
                group (str) : SMTP address of group
        """
        group_details=self.search_for_group(group)
        if len(group_details)!=0:
            return group_details
        else:
            raise SDKException('Subclient', '102', 'Group details not found in discovered data')

    def browse_for_content(self, discovery_type, include_deleted=False):
        """Returns the Onedrive client content i.e. users/ group information that is discovered in auto discovery phase

                Args:

                    discovery_type  (int)   --  type of discovery for content
                                                For all Associated users = 1
                                                For all Associated groups = 2
                                                For all Custom category groups = 31

                    include_deleted  (bool)  -- If True, deleted items will also be included

                Returns:

                    user_dict     (dict)    --  dictionary of users properties

                    no_of_records   (int)   --  no of records

                Raises:

                    SDKException:

                        if response is empty

                        if response is not success

                        if the method is called by Onedrive On-Premise Instance

        """
        if not self._backupset_object._instance_object.ca_instance_type.lower() == constants.ONEDRIVE_INSTANCE.lower():
            raise SDKException('Subclient', '102', 'Method not supported for Onedrive On-Premise Instance')

        self._USER_POLICY_ASSOCIATION = self._services['USER_POLICY_ASSOCIATION']
        request_json = {
            "discoverByType": discovery_type,
            "bIncludeDeleted": include_deleted,
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
                no_of_records = 0
                if 'associations' in response.json():
                    no_of_records = response.json().get('associations', [{}])[0].get('pagingInfo', {}). \
                        get('totalRecords', -1)
                elif 'pagingInfo' in response.json():
                    no_of_records = response.json().get('pagingInfo', {}).get('totalRecords', -1)
                    if no_of_records <= 0:
                        return {}, no_of_records
                associations = response.json().get('associations', [{}])
                user_dict = {}
                if discovery_type == 2 or discovery_type == 31:
                    if associations:
                        for group in associations:
                            group_name = group.get("groups", {}).get("name", "")
                            user_dict[group_name] = {
                                'accountStatus': group.get("accountStatus"),
                                'discoverByType': group.get("discoverByType"),
                                'planName': group.get("plan", {}).get("planName", ""),
                                'id': group.get("groups", {}).get("id", ""),
                                'categoryNumber': group.get("groups", {}).get("categoryNumber", None)
                            }
                else:
                    if associations:
                        for user in associations:
                            user_url = user.get("userAccountInfo", {}).get("smtpAddress", "")
                            user_account_info = user.get("userAccountInfo", {})
                            user_dict[user_url] = {
                                'userAccountInfo': user_account_info,
                                'accountStatus': user.get("accountStatus"),
                                'discoverByType': user.get("discoverByType"),
                                'planName': user.get("plan", {}).get("planName", ""),
                                'lastBackupTime': user.get("userAccountInfo", {}).get("lastBackupJobRanTime", {}).get(
                                    "time", None)
                            }
                return user_dict, no_of_records
            return {}, 0
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_properties_to_update_site_association(self, operation):
        """Updates the association properties of user

            Args:

               operation (int)                  --  type of operation to be performed
                                                     Example: 1 - Associate
                                                              2 - Enable
                                                              3 - Disable
                                                              4 - Remove

            Raises:

            SDKException:

                if the method is called by Onedrive On-Premise Instance

        """
        if not self._backupset_object._instance_object.ca_instance_type.lower() == constants.ONEDRIVE_INSTANCE.lower():
            raise SDKException('Subclient', '102', 'Method not supported for Onedrive On-Premise Instance')

        properties_dict = {}
        if operation == 1:
            properties_dict["accountStatus"] = 0
        elif operation == 2:
            properties_dict["accountStatus"] = 0
        elif operation == 3:
            properties_dict["accountStatus"] = 2
        elif operation == 4:
            properties_dict["accountStatus"] = 1
        return properties_dict


    def update_users_association_properties(self, operation, **kwargs):
        """Updates the association properties of user

                Args:
                    operation (int)         --  type of operation to be performed
                                                 Example: 1 - Associate
                                                          2 - Enable
                                                          3 - Disable
                                                          4 - Remove

                    Additional arguments (kwargs):
                    user_accounts_list (list)   --  list of user accounts
                                                    It has all information of users

                    groups_list (list)      --  list of groups
                                                It has all information of groups

                    plan_id (int)           --  id of Office 365 plan

                Raises:

                    SDKException:

                        if response is empty

                        if response is not success

                        if the method is called by Onedrive On-Premise Instance

        """
        plan_id = kwargs.get('plan_id', None)
        user_accounts_list = kwargs.get('user_accounts_list', None)
        groups_list = kwargs.get('groups_list', None)

        if not self._backupset_object._instance_object.ca_instance_type.lower() == constants.ONEDRIVE_INSTANCE.lower():
            raise SDKException('Subclient', '102', 'Method not supported for Onedrive On-Premise Instance')

        properties_dict = self._set_properties_to_update_site_association(operation)
        self._ASSOCIATE_CONTENT = self._services['UPDATE_USER_POLICY_ASSOCIATION']
        if user_accounts_list:
            request_json = {
                "cloudAppAssociation": {
                    "subclientEntity": {
                        "subclientId": int(self.subclient_id)
                    },
                    "cloudAppDiscoverinfo": {
                        "discoverByType": 1,
                        "userAccounts": user_accounts_list
                    }
                }
            }
        if groups_list:
            request_json = {
                "LaunchAutoDiscovery": True,
                "cloudAppAssociation": {
                    "subclientEntity": {
                        "subclientId": int(self.subclient_id)
                    },
                    "cloudAppDiscoverinfo": {
                        "discoverByType": 2,
                        "groups": groups_list
                    }
                }
            }
        if properties_dict.get('accountStatus', None) is not None:
            request_json['cloudAppAssociation']['accountStatus'] = properties_dict['accountStatus']
        if plan_id:
            request_json['cloudAppAssociation']['plan'] = {
                "planId": int(plan_id)
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
            raise SDKException('Response', '102', self._update_response_(response.text))

    def manage_custom_category(self, custom_dict, action, plan=None):
        """
        Adds or Edits Custom category in the office 365 app.

        Args:
            custom_dict (dict)  --  dictionary of custom category name and rule details.
                Example:
                    {
                    "name":"Display name contains custom"
                    "rules":
                        [
                            {
                            "CCRuleName":"User Display Name",
                            "CCRuleOperator":"Contains",
                            "CCRuleMask":"od_test_user"
                            }
                        ]
                    }
            action (str)     --  Action to perform. Either 'add' or 'edit'.
            plan (str)       --  Name of plan to be selected for adding category.
                                //Default: None. Required for adding category.

        Raises:
            SDKException:
                if response is not success
                if response is returned with errors
        """

        def get_field_number(field_name):
            """ Gets the indexed number for each type of field"""
            numbers = {
                "User Display Name": 1,
                "User SMTP Address": 2,
                "User Geo Location": 3,
                "License": 4
            }
            return numbers.get(field_name, None)

        def get_field_type(field_name):
            """ Returns the mapped field_type of given field_name """
            types = {
                "User Display Name": 5,
                "User SMTP Address": 5,
                "User Geo Location": 1,
                "License": 1
            }
            return types.get(field_name, None)

        def get_field_operator(cc_rule_operator):
            """ Gets the corresponding number assigned to each operator """
            operators = {
                "Contains": 0,
                "Regular Expression": 1,
                "Starts With": 3,
                "Ends With": 4,
                "Equals": 1000,
                "Not Equal": 1001
            }
            return operators.get(cc_rule_operator, None)

        def get_cc_rule_type(field_type):
            """  Gets the type of field in English words """
            if field_type == 1:
                return "Generic"
            elif field_type == 5:
                return "String"
            else:
                return "Unknown"

        def get_mask(cc_rule_mask, cc_rule_name):
            """ Gets the masked name of Custom category rule """
            if cc_rule_name != "User Geo Location":
                if cc_rule_name == "License":
                    if cc_rule_mask != "Active":
                        return "ActiveRevoked"
                return cc_rule_mask
            else:
                # Extract mask from the brackets in CCRuleMask
                match = re.search(r'\((.*?)\)', cc_rule_mask)
                if match:
                    return match.group(1)
                else:
                    return None

        # Get o365 plan object and ID
        if action == 'add':
            plan_name = plan.strip()
            o365_plan_object = self._commcell_object.plans.get(plan_name)
            o365_plan_id = int(o365_plan_object.plan_id)
        else:
            # Fetch plan details for the given category in case of edit
            groups, _ = self.browse_for_content(discovery_type=31)
            plan_name = groups[custom_dict['name']].get('planName', "")
            o365_plan_object = self._commcell_object.plans.get(plan_name)
            o365_plan_id = int(o365_plan_object.plan_id)
            categoryNumber = groups[custom_dict['name']].get('categoryNumber', None)

        # Get Instance, client, Subclient Ids
        instance_id = int(self._instance_object.instance_id)
        client_id = int(self._client_object.client_id)
        subclient_id = int(self.subclient_id)

        conditions = []
        for entry in custom_dict["rules"]:
            self.custom_counter += 1
            condition = {
                "uniqueId": f"CC_{self.custom_counter}",
                "fieldSource": "OD_KnownFields",
                "fieldName": entry["CCRuleName"],
                "fieldNumber": get_field_number(entry["CCRuleName"]),
                "fieldType": get_field_type(entry["CCRuleName"]),
                "fieldOperator": get_field_operator(entry["CCRuleOperator"]),
                "mask": get_mask(entry["CCRuleMask"], entry["CCRuleName"]),
                "CCRuleName": entry["CCRuleName"],
                "CCRuleOperator": entry["CCRuleOperator"],
                "CCRuleType": get_cc_rule_type(get_field_type(entry["CCRuleName"])),
                "CCRuleMask": entry["CCRuleMask"]
            }
            conditions.append(condition)

        req_json = {
            "subclientEntity": {
                "subclientId": subclient_id
            },
            "planEntity": {
                "planId": o365_plan_id,
                "planName": plan_name if action == 'edit' else ""
            },
            "status": 0,
            "categoryName": custom_dict['name'],
            "categoryQuery": {
                "conditions": conditions
            },
            "office365V2AutoDiscover": {
                "launchAutoDiscover": True,
                "appType": 134,
                "clientId": client_id,
                "instanceId": instance_id,
                "instanceType": 7
            }
        }

        if action == 'add':
            url = self._services['CUSTOM_CATEGORY'] % subclient_id
            flag, response = self._cvpysdk_object.make_request('POST', url, req_json)
        elif action == 'edit':
            url = self._services['CUSTOM_CATEGORY'] % subclient_id + "/" + str(categoryNumber)
            flag, response = self._cvpysdk_object.make_request('PUT', url, req_json)
        else:
            raise SDKException('Subclient', '102', "Invalid action. Must be either 'add' or 'edit'.")

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to {action} group\nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))


    def update_custom_categories_association_properties(self, category_name, operation):
        """
        Updates the association properties of custom category

                Args:
                    category_name (str)     --  Display name of custom category
                    operation (int)         --  type of operation to be performed
                                                 Example:
                                                          0 - Enable
                                                          1 - Remove
                                                          2 - Disable

                Raises:

                    SDKException:

                        if response is empty

                        if response is not success

                        if the method is called by Onedrive On-Premise Instance

        """

        if not self._backupset_object._instance_object.ca_instance_type.lower() == constants.ONEDRIVE_INSTANCE.lower():
            raise SDKException('Subclient', '102', 'Method not supported for Onedrive On-Premise Instance')

        # Get Instance, client, Subclient Ids
        instance_id = int(self._instance_object.instance_id)
        client_id = int(self._client_object.client_id)
        client_name = self._client_object.client_name
        subclient_id = int(self.subclient_id)
        url = self._services['CUSTOM_CATEGORIES'] % subclient_id

        # Get the category number
        groups, numberOfGroups = self.browse_for_content(discovery_type=31)
        category_number = groups[category_name].get('categoryNumber', None)

        if not category_number:
            raise SDKException('Subclient', '102', 'Please ensure the category name given is valid')

        request_json = {
            "updateCategoryNumbers": [category_number],
            "subclientEntity": {
                "subclientId": subclient_id,
                "clientName": client_name
            },
            "office365V2AutoDiscover": {
                "launchAutoDiscover": True,
                "appType": 134,
                "clientId": client_id,
                "instanceId": instance_id
            },
            "status": operation
        }

        flag, response = self._cvpysdk_object.make_request(
            'PUT', url, request_json
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to add group\nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def refresh_retention_stats(self, subclient_id):
        """
        refresh the retention stats for the client

        Args:
            subclient_id(int)             : subclient id of the client
        """
        request_json = {
            "appType": constants.ONEDRIVE_INDEX_APPTYPE_ID,
            "subclientId": int(subclient_id)
        }
        refresh_retention = self._services['OFFICE365_PROCESS_INDEX_RETENTION_RULES']
        flag, response = self._cvpysdk_object.make_request('POST', refresh_retention, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to refresh retention stats \nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
                else:
                    self.log.info("refresh retention stats successful")
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def refresh_client_level_stats(self,subclient_id):
        """
        refresh the client level stats for the client

        Args:
            subclient_id(int)             : subclient id of the client

        """
        request_json = {
            "appType": constants.ONEDRIVE_INDEX_APPTYPE_ID,
            "oneDriveIdxStatsReq":
                [{
                    "subclientId": int(subclient_id), "type": 0}]
        }
        refresh_backup_stats = self._services['OFFICE365_POPULATE_INDEX_STATS']
        flag, response = self._cvpysdk_object.make_request('POST', refresh_backup_stats, request_json)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to refresh client level stats \nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
                else:
                    self.log.info("refresh client level stats successful")
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_client_level_stats(self,backupset_id):
        """
        Returns the client level stats for the client

        Args:
            backupset_id(int)             : backupset id of the client

        Retruns:

            response(json)                : returns the client level stats as a json response
        """
        get_backup_stats = self._services['OFFICE365_OVERVIEW_STATS'] % backupset_id
        flag, response = self._cvpysdk_object.make_request('GET', get_backup_stats)

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to get client level stats \nError: {error_message}'
                    raise SDKException('Subclient', '102', output_string)
                else:
                    self.log.info("get client level stats successful")
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

        return response.json()




