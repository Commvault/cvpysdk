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

"""File for operating on a GMail/GDrive/OneDrive Subclient.

GoogleSubclient is the only class defined in this file.

GoogleSubclient:    Derived class from CloudAppsSubclient Base class, representing a
GMail/GDrive/OneDrive subclient, and to perform operations on that subclient

GoogleSubclient:

    _get_subclient_properties()         --  gets the properties of Google Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of Google Subclient

    content()                           --  gets the content of the subclient

    groups()                            --  gets the groups associated with the subclient

    restore_out_of_place()              --  runs out-of-place restore for the subclient

    discover()                          --  runs user discovery on subclient

    add_AD_group()                      --  adds AD group to the subclient

    add_user()                          --  adds user to the subclient

    add_users()                      --  Adds user to OneDrive for Business Client

    add_shared_drives()              --  Adds given SharedDrives to client

    search_for_user()                   --  Searches for a specific user's details from discovered list

    disk_restore()                   --  Runs disk restore of selected users for OneDrive for Business Client

    out_of_place_restore()           --  Runs out-of-place restore of selected users for OneDrive for Business Client

    in_place_restore()               --  Runs in-place restore of selected users for OneDrive for Business Client

    _get_user_guids()                   --  Retrieve GUIDs for users specified

    process_index_retention_rules()     --  Makes API call to process index retention rules

    verify_user_discovery()          --  Makes API call to get discovered users of Google client

    verify_shareddrive_discovery()   --  Makes API call to get discovered shared drives of GDrive client.

    run_user_level_backup()             --  Runs Users level backup for google client

    run_client_level_backup()           --  Runs client level backup for Google Client
    
    browse_content()                    --  Fetches discovered content based on discovery type
    
    verify_groups_discovery()           --  Verifies that groups discovery is complete
    
    search_for_shareddrive()            --  Searches for a specific shared drive details from discovered list

    _association_users_json()           --  Constructs json for associated users to backup

    _task_json_for_google_backup()      --  Constructs json for google backup for selected users

"""

from __future__ import unicode_literals
from ...exception import SDKException
import time
from ..casubclient import CloudAppsSubclient
from ...constants import AppIDAType

class GoogleSubclient(CloudAppsSubclient):
    """Derived class from CloudAppsSubclient Base class, representing a GMail/GDrive/OneDrive subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.."""
        super(GoogleSubclient, self)._get_subclient_properties()
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

    @property
    def content(self):
        """Returns the subclient content dict"""
        return self._ca_content

    @property
    def groups(self):
        """Returns the list of groups assigned to the subclient if any.
        Groups can be azure AD group or Google groups.
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
        """This method discovers the users/groups on Google GSuite Account/OneDrive

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

            if subclient_prop['instanceType'] == 7:
                subclient_prop['oneDriveSubclient']['regularExp'] = value
            else:
                subclient_prop['GoogleSubclient']['regularExp'] = value
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

    def add_users(self, users, plan_name):
        """ Adds given OneDrive users to v2 client

            Args:

                users (list) : List of user's SMTP address

                plan_name (str) : Google Workspace plan name to associate with users

            Raises:

                SDKException:

                    if response is not success

                    if response is returned with errors
        """

        if not (isinstance(users, list) and isinstance(plan_name, str)):
            raise SDKException('Subclient', '101')

        # Get GoogleWorkspace plan
        plan_name = plan_name.strip()
        google_plan_object = self._commcell_object.plans.get(plan_name)
        google_plan_id = int(google_plan_object.plan_id)

        # Get client ID
        client_id = int(self._client_object.client_id)

        user_accounts = []

        for user_id in users:
            user_accounts.append(self.search_for_user(user_id))

        request_json = {
            "LaunchAutoDiscovery": False,
            "cloudAppAssociation": {
                "accountStatus": 0,
                "subclientEntity": {
                    "subclientId": int(self.subclient_id),
                    "clientId": client_id,
                    "instanceId": int(self._instance_object.instance_id),
                    "applicationId": AppIDAType.CLOUD_APP.value
                },
                "cloudAppDiscoverinfo": {
                    # GDrive : 24 | GMail : 22
                    "discoverByType": 22 if self._instance_object.ca_instance_type == 'GMAIL' else 24,
                    "userAccounts": user_accounts
                },
                "plan": {
                    "planId": google_plan_id
                }
            }
        }

        user_associations = self._services[
            'GMAIL_UPDATE_USERS'] if self._instance_object.ca_instance_type == 'GMAIL' else self._services[
            'GDRIVE_UPDATE_USERS']
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

    def add_shared_drives(self, shared_drives, plan_name):
        """ Adds given SharedDrives to client

            Args:

                shared_drives (list) : List of SharedDrives

                plan_name (str) : Google Workspace plan name to associate with users

            Raises:

                SDKException:

                    if response is not success

                    if response is returned with errors
        """

        if not (isinstance(shared_drives, list) and isinstance(plan_name, str)):
            raise SDKException('Subclient', '101')

        # Get GoogleWorkspace plan
        plan_name = plan_name.strip()
        google_plan_object = self._commcell_object.plans.get(plan_name)
        google_plan_id = int(google_plan_object.plan_id)

        # Get client ID
        client_id = int(self._client_object.client_id)

        drives = []

        for drive in shared_drives:
            response = self.search_for_shareddrive(drive)
            response['user'] = {}
            response['displayName'] = response['folderTitle']
            response['user']['userGUID'] = response['folderId']
            response['isAutoDiscoveredUser'] = False
            drives.append(response)

        request_json = {
            "LaunchAutoDiscovery": False,
            "cloudAppAssociation": {
                "accountStatus": 0,
                "subclientEntity": {
                    "subclientId": int(self.subclient_id),
                    "clientId": client_id,
                    "instanceId": int(self._instance_object.instance_id),
                    "applicationId": AppIDAType.CLOUD_APP.value
                },
                "cloudAppDiscoverinfo": {
                    "discoverByType": 32,
                    "userAccounts": drives
                },
                "plan": {
                    "planId": google_plan_id
                }
            }
        }

        user_associations = self._services['GDRIVE_UPDATE_USERS']
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

    def browse_content(self, discovery_type):
        """ Fetches discovered content based on discovery type
            Args:
                discovery_type: Type of content to be discovered.
                    discovery_type=8 - Users
                    discovery_type=25 - Shared Drives
                    discovery_type=5 - Groups

            Returns:
                    records (list):  content fetched, [] if no content fetched

            Raises:

                 SDKException:

                        if response is not success
        """
        # Wait for sometime unitl disco discovery completes before checking actual content.
        attempt = 0
        while attempt < 5:
            flag, response = self._cvpysdk_object.make_request('GET', (
                        self._services['GOOGLE_DISCOVERY_OVERVIEW'] % (self._backupset_object.backupset_id)))
            if response.json()['office365ClientOverview']['summary']['discoverState']['discoveryProgress'] == 100:
                break
            attempt += 1
            time.sleep(10)

        browse_content = (self._services['CLOUD_DISCOVERY'] % (self._instance_object.instance_id,
                                                               self._client_object.client_id,
                                                               AppIDAType.CLOUD_APP.value))

        # determines the number of accounts to return in response
        page_size = 500
        offset = 0

        records = []
        while True:
            discover_query = f'{browse_content}&pageSize={page_size}&offset={offset}&eDiscoverType={discovery_type}'
            flag, response = self._cvpysdk_object.make_request('GET', discover_query)
            offset += 1
            if flag:
                if response and response.json():
                    if discovery_type==8:
                        if 'userAccounts' in response.json():
                            curr_records = response.json().get('userAccounts', [])
                            records.extend(curr_records)
                            if len(curr_records) < page_size:
                                break
                    elif discovery_type==25:
                        if 'folders' in response.json():
                            curr_records = response.json().get('folders', [])
                            records.extend(curr_records)
                            if len(curr_records) < page_size:
                                break
                    elif discovery_type == 5:
                        if 'groups' in response.json():
                            curr_groups = response.json().get('groups', [])
                            records.extend(curr_groups)
                            if len(curr_groups) < page_size:
                                break
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return records

    def verify_groups_discovery(self):
        """ Verifies that groups discovery is complete

            Returns:

                discovery_stats (tuple):

                    discovery_status (bool): True if users are discovered else returns False

                    user_accounts (int):     List of users fetched, returns [] if discovery is not complete

            Raises:

                 SDKException:

                        if response is not success

                        if response received does not contain pagining info
        """
        browse_content = (self._services['CLOUD_DISCOVERY'] % (self._instance_object.instance_id,
                                                               self._client_object.client_id,
                                                               AppIDAType.CLOUD_APP.value))

        # determines the number of accounts to return in response
        page_size = 500
        offset = 0

        groups = []
        while True:
            discover_query = f'{browse_content}&pageSize={page_size}&offset={offset}&eDiscoverType=5'
            flag, response = self._cvpysdk_object.make_request('GET', discover_query)
            offset += 1

            if flag:
                if response and response.json():
                    if 'groups' in response.json():
                        curr_groups = response.json().get('groups', [])
                        groups.extend(curr_groups)
                        if len(curr_groups) < page_size:
                            break
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return groups

    def verify_shareddrive_discovery(self):
        """ Verifies all shared drives discovery completed.

                    Returns:

                        discovery_stats (tuple):

                            discovery_status (bool): True if users are discovered else returns False

                            user_accounts (int):     List of shared drives fetched, returns [] if discovery is not complete

                    Raises:

                         SDKException:

                                if response is not success

                                if response received does not contain pagining info
                """

        browse_content = (self._services['CLOUD_DISCOVERY'] % (self._instance_object.instance_id,
                                                               self._client_object.client_id,
                                                               AppIDAType.CLOUD_APP.value))

        # determines the number of accounts to return in response
        page_size = 500
        discover_query = f'{browse_content}&pageSize={page_size}&eDiscoverType=25' # for shared drive discovery

        flag, response = self._cvpysdk_object.make_request('GET', discover_query)

        if flag:
            no_of_records = -1
            if response and response.json():
                if 'pagingInfo' in response.json():
                    no_of_records = response.json().get('pagingInfo', {}).get('totalRecords', -1)
                    if no_of_records > 0:
                        shared_drives = response.json().get('folders', [])
                        return True, shared_drives
            return False, []
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _association_users_json(self, users_list):
        """
            Args:
                users_list (list) : list of SMTP addresses of users
            Returns:
                users_json(list): Required details of users to backup
        """
        users_json = []
        for user_smtp in users_list:
            user_details = self.search_for_user(user_smtp)
            user_info = {
                "user": {
                    "userGUID": user_details.get('user', {}).get('userGUID')
                }
            }
            users_json.append(user_info)
        return users_json

    def _task_json_for_google_backup(self, is_mailbox, users_list=None):
        """
        Json for google backup for selected users

        Args:
                is_mailbox (boolean) : used to determine Gmail or GDrive
                users_list (list) : list of SMTP addresses of users
        Returns:
                task_json(dict): Task request used as backup payload
        """

        selected_items = []
        advanced_options_dict = None
        if users_list is not None:
            associated_users_json = self._association_users_json(users_list)
            advanced_options_dict = {
                'cloudAppOptions': {
                    'userAccounts': associated_users_json
                }
            }

            for user_smtp in users_list:
                details = self.search_for_user(user_smtp)
                item = {
                    "itemName": details.get('displayName'),
                    "itemType": "Mailbox" if is_mailbox else "User"
                }
                selected_items.append(item)
        else:
            item = {
                "itemName": "All mailboxes" if is_mailbox else "All users",
                "itemType": "All mailboxes" if is_mailbox else "All users"
            }
            selected_items.append(item)

        common_options_dict = {
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
        task_json = self._backup_json(backup_level='INCREMENTAL', incremental_backup=False,
                                      incremental_level='BEFORE_SYNTH', advanced_options=advanced_options_dict,
                                      common_backup_options=common_options_dict)
        return task_json

    def run_user_level_backup(self, users_list, is_mailbox):
        """
        Runs the backup for the users in users list
        Args:
                users_list (list) : list of SMTP addresses of users

                is_mailbox (boolean) : flag to determine GMail Mailbox or not

        Returns:
                object - instance of the Job class for this backup job

        Raises:
            SDKException:
                if response is empty

                if response is not success

        """
        task_json = self._task_json_for_google_backup(is_mailbox, users_list=users_list)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)

    def run_client_level_backup(self, is_mailbox):
        """
                Runs the backup for the client
                Args:
                        is_mailbox (boolean) : flag to determine GMail Mailbox or not

                Returns:
                        object - instance of the Job class for this backup job

                Raises:
                    SDKException:
                        if response is empty

                        if response is not success

                """
        task_json = self._task_json_for_google_backup(is_mailbox)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)

    def search_for_user(self, user_id):
        """ Searches for a specific user's details from discovered list

            Args:
                user_id (str) : user's SMTP address

            Returns:

                user (list): user details' list fetched from discovered content
                              eg: {
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
                    for user in user_accounts:
                        if user['smtpAddress'] == user_id:
                            return user
                    else:
                        error_string = 'User is not available in discovered data'
                        raise SDKException('Subclient', '102', error_string)
                else:
                    raise SDKException('Response', '102', 'Check if the user provided is valid')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def search_for_shareddrive(self, drive):
        """ Searches for a specific shared drive details from discovered list

            Args:
                drive (str) : Shared Drive iD

            Returns:

                drive (list): shared drive details' list fetched from discovered content
                              eg: {
                                        'folderTitle': '',
                                        'folderId':'',
                                        'user': {
                                             'userGUID': 'UserGuid'
                                        }
                                 }

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

        search_query = f'{browse_content}&search={drive}&eDiscoverType=25'

        flag, response = self._cvpysdk_object.make_request('GET', search_query)

        if flag:
            if response and response.json():
                if 'folders' in response.json():
                    folders = response.json().get('folders', [])
                    if len(folders) == 0:
                        error_string = 'Either discovery is not complete or Shared Drive is not available in discovered data'
                        raise SDKException('Subclient', '102', error_string)
                    for folder in folders:
                        if folder['folderTitle'] == drive:
                            return folder
                    else:
                        error_string = 'Shared Drive is not available in discovered data'
                        raise SDKException('Subclient', '102', error_string)
                else:
                    raise SDKException('Response', '102', 'Check if the Shared Drive provided is valid')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def disk_restore(self, users, destination_client, destination_path, skip_file_permissions=False):
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
        restore_json = self._instance_object._prepare_restore_json_v2(source_user_list, **kwargs)
        return self._process_restore_response(restore_json)

    def out_of_place_restore(self, users, destination_path, **kwargs):
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
        restore_json = self._instance_object._prepare_restore_json_v2(source_user_list, **kwargs)
        return self._process_restore_response(restore_json)

    def in_place_restore(self, users, **kwargs):
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
        restore_json = self._instance_object._prepare_restore_json_v2(source_user_list, **kwargs)
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
            try:
                user = self.search_for_user(user_id)
                if len(user) != 0 and user.get('user', {}).get('userGUID') is not None:
                    user_guid_list.append(user.get('user').get('userGUID'))
                else:
                    raise SDKException('Subclient', '102', 'User details not found in discovered data')
            except SDKException:
                user = self.search_for_shareddrive(user_id)
                if len(user) != 0 and user.get('folderId') is not None:
                    user_guid_list.append(user.get('folderId'))
                else:
                    raise SDKException('Subclient', '102', 'User details not found in discovered data')
        return  user_guid_list

    def process_index_retention_rules(self,index_app_type_id,index_server_client_name):
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
