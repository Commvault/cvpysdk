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

    refresh_retention_stats()           --  Refreshes the retention stats for the client

    refresh_stats_status()              --  refresh the client level or user level stats for the client

    get_client_level_stats()            --  Returns the client level stats for the client

    get_user_level_stats()              --  Returns the user level stats

    browse_folders()                    --  Browse folders of the user in the browse

    browse_mails()                      --  Browse mails of the user in the browse

    browse_files()                      --  Browse files of the user in the browse
"""

from __future__ import unicode_literals
import copy
import time
from typing import Any, Dict, List, Optional

from ...exception import SDKException
from ...constants import AppIDAType
from ..casubclient import CloudAppsSubclient
from . import google_constants as constants

from cvpysdk.job import Job


class GoogleSubclient(CloudAppsSubclient):
    """
    Specialized subclient class for managing Google Workspace applications such as GMail, GDrive, and OneDrive.

    This class extends the CloudAppsSubclient base class to provide comprehensive management and data protection
    operations for Google-based subclients. It enables discovery, browsing, backup, restore, and user/group
    management functionalities tailored for Google Workspace environments.

    Key Features:
        - Retrieve and manage subclient properties and configuration
        - Discover content, users, groups, and shared drives within Google Workspace
        - Add and manage Active Directory groups, users, and shared drives
        - Perform user-level and client-level backup operations for mailboxes and drives
        - Browse content including folders, mails, and files with advanced filtering
        - Restore data in-place, out-of-place, and to disk with support for ACLs and permissions
        - Search for users and shared drives by identifiers
        - Manage retention rules and refresh retention statistics
        - Access and report on client-level and user-level statistics
        - Property accessors for subclient content and groups

    This class is intended for use in environments requiring granular control and automation of Google Workspace
    data management, backup, and recovery operations.

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> dict[str, Any]:
        """Retrieve the properties related to the File System subclient.

        This method fetches and returns a dictionary containing various configuration
        and status details specific to the File System subclient.

        Returns:
            Dictionary containing subclient properties and their values.

        Example:
            >>> subclient = GoogleSubclient()
            >>> properties = subclient._get_subclient_properties()
            >>> print(properties)
            >>> # Access specific property
            >>> backup_enabled = properties.get('backupEnabled')
            >>> print(f"Backup enabled: {backup_enabled}")

        #ai-gen-doc
        """
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

    def _get_subclient_properties_json(self) -> dict:
        """Retrieve all properties related to this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all subclient properties.

        Example:
            >>> subclient = GoogleSubclient()
            >>> properties = subclient._get_subclient_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary with subclient property details

        #ai-gen-doc
        """

        return {'subClientProperties': self._subclient_properties}

    @property
    def content(self) -> list[dict[str, Any]]:
        """Get the content dictionary associated with the Google subclient.

        Returns:
            list: A list of dictionaries representing the content configuration of the subclient.

        Example:
            >>> google_subclient = GoogleSubclient()
            >>> content_dict = google_subclient.content
            >>> print(content_dict)
            >>> # Use the content dictionary for further processing or inspection

        #ai-gen-doc
        """
        return self._ca_content

    @property
    def groups(self) -> list:
        """Get the list of groups assigned to the subclient, if any.

        The groups can be Azure AD groups or Google groups. Groups are assigned to the subclient
        only if auto discovery is enabled for groups.

        Returns:
            list: A list of groups associated with the subclient. The list may be empty if no groups are assigned.

        Example:
            >>> subclient = GoogleSubclient()
            >>> assigned_groups = subclient.groups
            >>> print(f"Groups assigned to subclient: {assigned_groups}")

        #ai-gen-doc
        """
        return self._ca_groups

    @content.setter
    def content(self, subclient_content: list) -> None:
        """Set the content for the Cloud Apps Subclient.

        This method prepares and assigns the list of content items to be included in the subclient.
        The content is formatted as a list of JSON objects suitable for use with the POST Subclient API.

        Args:
            subclient_content: A list containing the content items to add or update in the subclient.

        Example:
            >>> subclient = GoogleSubclient()
            >>> new_content = [
            ...     {"user": "user1@example.com"},
            ...     {"user": "user2@example.com"}
            ... ]
            >>> subclient.content = new_content  # Use assignment for property setter
            >>> print("Subclient content updated successfully")

        #ai-gen-doc
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

    def __do_submit_browse_request(self, req_payload: dict) -> dict:
        """Submit a browse request and return the response.

        Args:
            req_payload: A dictionary containing the payload for the browse request.

        Returns:
            A dictionary representing the response from the browse request.

        Example:
            >>> subclient = GoogleSubclient()
            >>> payload = {"path": "/documents", "options": {"recursive": True}}
            >>> response = subclient._GoogleSubclient__do_submit_browse_request(payload)
            >>> print(response)
            {'status': 'success', 'items': [...]}

        #ai-gen-doc
        """
        for params in req_payload["searchProcessingInfo"]["queryParams"]:
            if params["param"] == "RESPONSE_FIELD_LIST":
                values_in_response = constants.GMAIL_BROWSE_FIELD_RESPONSE_FIELD_PARAMS if (
                        self._instance_object.ca_instance_type == "GMAIL") \
                    else constants.GDRIVE_BROWSE_FIELD_RESPONSE_FIELD_PARAMS
                params.update({"value": values_in_response})
        _search_api = self._services["DO_WEB_SEARCH"]
        flag, response = self._cvpysdk_object.make_request("POST", _search_api, req_payload)
        if flag:
            try:
                resp_json = response.json()
            except ValueError:
                raise SDKException("Response", '102', 'Invalid or empty response JSON')
            if not resp_json:
                raise SDKException('Response', '102', 'Empty response json')
            if resp_json and 'errorCode' in resp_json:
                error_code = resp_json.get('errorCode')
                if error_code != 0:
                    error_message = resp_json.get('errorMessage')
                    raise SDKException('Subclient', '102', error_message)
            else:
                count = int(resp_json.get("proccessingInfo", {}).get("totalHits", 0))
                req_payload["searchProcessingInfo"]["pageSize"] = count
                flag, response = self._cvpysdk_object.make_request("POST", _search_api, req_payload)
                if flag:
                    try:
                        resp_json = response.json()
                    except ValueError:
                        raise SDKException("Response", '102', 'Invalid or empty response JSON')
                    if not resp_json:
                        raise SDKException('Response', '102', 'Empty response json')
                    if resp_json and 'errorCode' in resp_json:
                        error_code = resp_json.get('errorCode')
                        if error_code != 0:
                            error_message = resp_json.get('errorMessage')
                            raise SDKException('Subclient', '102', error_message)
                    else:
                        return count, resp_json
                else:
                    raise SDKException('Response', '102',
                                       self._update_response_(response.text))
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text))

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

        This method restores the files or folders listed in `paths` to the specified `destination_path`
        on the given `client`. The restore can be performed out-of-place, optionally overwriting existing
        files, restoring data and ACLs, and using additional restore options.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: Full path to the restore location on the target client.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional copy precedence value for the storage policy copy. Default is None.
            from_time: Optional lower time boundary for restore (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper time boundary for restore (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_disk: If True, perform a restore to disk operation. Default is False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize.

        Example:
            >>> subclient = GoogleSubclient()
            >>> job = subclient.restore_out_of_place(
            ...     client="TargetClient",
            ...     destination_path="/restore/location",
            ...     paths=["/data/file1.txt", "/data/folder2"],
            ...     overwrite=True,
            ...     restore_data_and_acl=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
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

    def discover(self, discover_type: str = 'USERS') -> list:
        """Discover users or groups on a Google GSuite Account or OneDrive.

        Args:
            discover_type: The type of entities to discover. Valid values are:
                - 'USERS': Discover users (default).
                - 'GROUPS': Discover groups.

        Returns:
            A list containing the discovered users or groups, depending on the specified discover_type.

        Raises:
            SDKException: If the response is empty or the discovery operation is not successful.

        Example:
            >>> subclient = GoogleSubclient()
            >>> users = subclient.discover()  # Discover users (default)
            >>> print(f"Discovered users: {users}")
            >>> groups = subclient.discover('GROUPS')  # Discover groups
            >>> print(f"Discovered groups: {groups}")

        #ai-gen-doc
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

    def set_auto_discovery(self, value: list) -> None:
        """Set the auto discovery value for the subclient.

        This method allows you to configure auto discovery for the subclient by specifying
        either a list of regular expressions (RegEx) or user groups, depending on the auto
        discovery type selected at the instance level.

        Args:
            value: A list containing either RegEx patterns or user group names to be used
                for auto discovery.

        Example:
            >>> subclient = GoogleSubclient()
            >>> # Set auto discovery using RegEx patterns
            >>> subclient.set_auto_discovery(['^user.*@domain.com$', '^admin.*@domain.com$'])
            >>>
            >>> # Set auto discovery using user groups
            >>> subclient.set_auto_discovery(['IT_Group', 'HR_Group'])

        #ai-gen-doc
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

    def run_subclient_discovery(self) -> None:
        """Launch AutoDiscovery on the subclient.

        This method initiates the AutoDiscovery process for the current subclient, allowing the system to automatically detect and configure new data sources or changes within the subclient's scope.

        Example:
            >>> google_subclient = GoogleSubclient()
            >>> google_subclient.run_subclient_discovery()
            >>> print("AutoDiscovery launched successfully for the subclient.")

        #ai-gen-doc
        """

        discover_type = 15
        discover_users = self._services['GET_CLOUDAPPS_ONEDRIVE_USERS'] % (self._instance_object.instance_id,
                                                                           self._client_object.client_id,
                                                                           discover_type,
                                                                           self.subclient_id)
        flag, response = self._cvpysdk_object.make_request('GET', discover_users)
        if response.status_code != 200 and response.status_code != 500:
            raise SDKException('Response', '101')

    def add_AD_group(self, value: list) -> None:
        """Add Active Directory (AD) user groups to the subclient when auto discovery type is set to AD group at the instance level.

        Args:
            value: List of user group names to be added to the subclient.

        Example:
            >>> subclient = GoogleSubclient()
            >>> ad_groups = ['Domain Admins', 'Backup Operators']
            >>> subclient.add_AD_group(ad_groups)
            >>> print("AD groups added to the subclient successfully")
        #ai-gen-doc
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

    def add_user(self, user_name: str) -> None:
        """Add a OneDrive user to the GoogleSubclient.

        Args:
            user_name: The OneDrive user name to be added to the subclient.

        Example:
            >>> subclient = GoogleSubclient()
            >>> subclient.add_user("john.doe@example.com")
            >>> print("User added successfully")

        #ai-gen-doc
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

    def _get_subclient_users(self) -> list:
        """Retrieve the list of users associated with this subclient.

        Returns:
            list: A list containing the users present in the subclient.

        Example:
            >>> users = google_subclient._get_subclient_users()
            >>> print(f"Users in subclient: {users}")

        #ai-gen-doc
        """
        users = []
        result = self.content
        for user in result:
            users.append(user['SMTPAddress'])
        return users

    @property
    def get_subclient_users(self) -> list:
        """Get the list of users associated with this subclient.

        Returns:
            list: A list containing the users assigned to the subclient.

        Example:
            >>> subclient = GoogleSubclient()
            >>> users = subclient.get_subclient_users
            >>> print(f"Users in subclient: {users}")

        #ai-gen-doc
        """
        return self._get_subclient_users()

    def add_users(self, users: List[str], plan_name: str) -> None:
        """Add specified OneDrive users to the v2 Google Workspace client.

        This method associates the provided list of users, identified by their SMTP addresses,
        with the specified Google Workspace plan.

        Args:
            users: List of user SMTP addresses to be added.
            plan_name: Name of the Google Workspace plan to associate with the users.

        Raises:
            SDKException: If the response is not successful or contains errors.

        Example:
            >>> users_to_add = ['user1@example.com', 'user2@example.com']
            >>> plan = 'Standard_Google_Plan'
            >>> google_subclient.add_users(users_to_add, plan)
            >>> print("Users added successfully to the plan.")

        #ai-gen-doc
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

    def add_shared_drives(self, shared_drives: list, plan_name: str) -> None:
        """Add the specified Shared Drives to the client and associate them with a Google Workspace plan.

        Args:
            shared_drives: A list of Shared Drive identifiers or names to be added to the client.
            plan_name: The name of the Google Workspace plan to associate with the added Shared Drives.

        Raises:
            SDKException: If the response from the server is not successful or contains errors.

        Example:
            >>> shared_drives = ['DriveA', 'DriveB']
            >>> plan = 'Workspace_Plan_1'
            >>> google_subclient.add_shared_drives(shared_drives, plan)
            >>> print("Shared Drives added successfully.")

        #ai-gen-doc
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

    def browse_content(self, discovery_type: int) -> list:
        """Fetch discovered Google Workspace content based on the specified discovery type.

        Args:
            discovery_type: The type of content to be discovered.
                - 8: Users
                - 25: Shared Drives
                - 5: Groups

        Returns:
            list: A list of discovered content records. Returns an empty list if no content is found.

        Raises:
            SDKException: If the response from the server is not successful.

        Example:
            >>> subclient = GoogleSubclient()
            >>> users = subclient.browse_content(8)
            >>> print(f"Discovered users: {users}")
            >>> shared_drives = subclient.browse_content(25)
            >>> print(f"Discovered shared drives: {shared_drives}")

        #ai-gen-doc
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
                    if discovery_type == 8:
                        if 'userAccounts' in response.json():
                            curr_records = response.json().get('userAccounts', [])
                            records.extend(curr_records)
                            if len(curr_records) < page_size:
                                break
                    elif discovery_type == 25:
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

    def verify_groups_discovery(self) -> tuple[bool, int]:
        """Verify whether the groups discovery process is complete.

        This method checks if the groups discovery operation has finished and returns the discovery status
        along with the number of user accounts discovered.

        Returns:
            tuple:
                A tuple containing:
                    - discovery_status (bool): True if users have been successfully discovered, False otherwise.
                    - user_accounts (int): The number of user accounts fetched. Returns 0 if discovery is not complete.

        Raises:
            SDKException: If the response is not successful or if the response does not contain paging information.

        Example:
            >>> subclient = GoogleSubclient()
            >>> status, user_count = subclient.verify_groups_discovery()
            >>> if status:
            ...     print(f"Discovery complete. Users discovered: {user_count}")
            ... else:
            ...     print("Discovery not complete.")

        #ai-gen-doc
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

    def verify_shareddrive_discovery(self) -> tuple[bool, int]:
        """Verify that the discovery of all shared drives has completed.

        This method checks whether the shared drives have been successfully discovered.
        It returns a tuple containing the discovery status and the number of shared drives found.

        Returns:
            tuple:
                A tuple containing:
                    - discovery_status (bool): True if all shared drives have been discovered, False otherwise.
                    - user_accounts (int): The number of shared drives fetched. Returns 0 if discovery is not complete.

        Raises:
            SDKException: If the response is not successful or if the response does not contain paging information.

        Example:
            >>> subclient = GoogleSubclient()
            >>> status, drive_count = subclient.verify_shareddrive_discovery()
            >>> if status:
            ...     print(f"Discovery complete. {drive_count} shared drives found.")
            ... else:
            ...     print("Discovery not complete.")

        #ai-gen-doc
        """

        browse_content = (self._services['CLOUD_DISCOVERY'] % (self._instance_object.instance_id,
                                                               self._client_object.client_id,
                                                               AppIDAType.CLOUD_APP.value))

        # determines the number of accounts to return in response
        page_size = 500
        discover_query = f'{browse_content}&pageSize={page_size}&eDiscoverType=25'  # for shared drive discovery

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

    def _association_users_json(self, users_list: List[str]) -> List[Dict[str, Any]]:
        """Generate a JSON-compatible list of user details for backup association.

        Args:
            users_list: List of SMTP addresses representing users to be backed up.

        Returns:
            List of dictionaries containing the required details of users for backup association.

        Example:
            >>> users = ['user1@example.com', 'user2@example.com']
            >>> users_json = google_subclient._association_users_json(users)
            >>> print(users_json)
            >>> # Output: [{'smtp_address': 'user1@example.com', ...}, {'smtp_address': 'user2@example.com', ...}]

        #ai-gen-doc
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

    def _task_json_for_google_backup(self, is_mailbox: bool, users_list: Optional[list] = None, **kwargs: dict) -> dict:
        """Generate the JSON payload for a Google backup task for selected users.

        Args:
            is_mailbox: Boolean flag to determine if the backup is for Gmail (True) or Google Drive (False).
            users_list: Optional list of SMTP addresses representing the users to include in the backup.
            **kwargs: Additional optional parameters for the backup task, such as:
                - full_backup (bool): Whether to perform a full backup.

        Returns:
            A dictionary representing the task request payload for the Google backup operation.

        Example:
            >>> subclient = GoogleSubclient()
            >>> payload = subclient._task_json_for_google_backup(
            ...     is_mailbox=True,
            ...     users_list=['user1@example.com', 'user2@example.com'],
            ...     full_backup=True
            ... )
            >>> print(payload)
            {'taskInfo': {...}, 'users': ['user1@example.com', 'user2@example.com'], 'fullBackup': True}

        #ai-gen-doc
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
                        },
                        {
                            "option": "Convert job to full",
                            "value": "Enabled" if kwargs.get('full_backup', False) else "Disabled"
                        }
                    ]
                }
            ]
        }
        task_json = self._backup_json(backup_level='INCREMENTAL', incremental_backup=False,
                                      incremental_level='BEFORE_SYNTH', advanced_options=advanced_options_dict,
                                      common_backup_options=common_options_dict)
        return task_json

    def run_user_level_backup(self, users_list: list, is_mailbox: bool, **kwargs: dict) -> 'Job':
        """Run a user-level backup for the specified users.

        Initiates a backup job for the provided list of user SMTP addresses. The backup can be performed
        for GMail mailboxes or other user data, depending on the value of `is_mailbox`. Additional options
        such as running a full backup can be specified via keyword arguments.

        Args:
            users_list: List of SMTP addresses (strings) representing the users to back up.
            is_mailbox: Boolean flag indicating whether to perform a GMail Mailbox backup.
            **kwargs: Optional keyword arguments for backup options.
                Example:
                    full_backup (bool): If True, performs a full backup instead of incremental.

        Returns:
            Job: An instance of the Job class representing the initiated backup job.

        Raises:
            SDKException: If the backup response is empty or not successful.

        Example:
            >>> users = ['user1@example.com', 'user2@example.com']
            >>> job = google_subclient.run_user_level_backup(users, is_mailbox=True, full_backup=True)
            >>> print(f"Backup job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        task_json = self._task_json_for_google_backup(is_mailbox, users_list=users_list, **kwargs)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)

    def run_client_level_backup(self, is_mailbox: bool, **kwargs: dict) -> 'Job':
        """Run a client-level backup for the GoogleSubclient.

        Args:
            is_mailbox: Flag indicating whether the backup is for a GMail Mailbox (True) or not (False).
            **kwargs: Optional keyword arguments for backup customization.
                Supported options include:
                    - full_backup (bool): If True, performs a full backup. If False or omitted, performs an incremental backup.

        Returns:
            Job: An instance of the Job class representing the initiated backup job.

        Raises:
            SDKException: If the backup response is empty or not successful.

        Example:
            >>> subclient = GoogleSubclient()
            >>> job = subclient.run_client_level_backup(is_mailbox=True, full_backup=True)
            >>> print(f"Backup job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        task_json = self._task_json_for_google_backup(is_mailbox, **kwargs)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)

    def search_for_user(self, user_id: str) -> dict:
        """Search for a specific user's details from the discovered content list.

        Args:
            user_id: The SMTP address of the user to search for.

        Returns:
            Dictionary containing the user's details fetched from the discovered content.
            Example structure:
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

        Raises:
            SDKException: If discovery is not complete, if an invalid SMTP address is passed,
                if the response is empty, or if the response is not successful.

        Example:
            >>> subclient = GoogleSubclient()
            >>> user_details = subclient.search_for_user('user@example.com')
            >>> print(user_details)
            >>> # Output will be a dictionary with user information as shown above

        #ai-gen-doc
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

    def search_for_shareddrive(self, drive: str) -> list:
        """Search for details of a specific shared drive from the discovered list.

        This method retrieves the details of a shared drive identified by its ID from the list of discovered shared drives.

        Args:
            drive: The ID of the shared drive to search for.

        Returns:
            A list containing the details of the shared drive, such as folder title, folder ID, and user information.
            Example structure:
                [
                    {
                        'folderTitle': '',
                        'folderId': '',
                        'user': {
                            'userGUID': 'UserGuid'
                        }
                    }
                ]

        Raises:
            SDKException: If discovery is not complete, if an invalid SMTP address is provided,
                if the response is empty, or if the response is not successful.

        Example:
            >>> subclient = GoogleSubclient()
            >>> shared_drive_details = subclient.search_for_shareddrive('0AExxxxxxxUk9PVA')
            >>> print(shared_drive_details)
            [
                {
                    'folderTitle': 'Project Drive',
                    'folderId': '0AExxxxxxxUk9PVA',
                    'user': {
                        'userGUID': 'UserGuid'
                    }
                }
            ]

        #ai-gen-doc
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

    def disk_restore(self, users: list, destination_client: str, destination_path: str,
                     skip_file_permissions: bool = False) -> 'Job':
        """Run an out-of-place disk restore job for specified users to a destination client.

        This method initiates a restore operation for the provided list of users, restoring their data
        to the specified destination client and path. By default, files already present in the destination
        are skipped. Optionally, file permissions can also be skipped during the restore.

        Args:
            users: List of SMTP addresses representing the users whose data will be restored.
            destination_client: The name of the client machine where the data should be restored.
            destination_path: The folder path on the destination client where the data will be restored.
            skip_file_permissions: If True, file permissions are not restored. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> users = ['user1@example.com', 'user2@example.com']
            >>> job = google_subclient.disk_restore(
            ...     users,
            ...     destination_client='DestinationClient01',
            ...     destination_path='/restore/location',
            ...     skip_file_permissions=True
            ... )
            >>> print(f"Restore job started with Job ID: {job.job_id}")

        #ai-gen-doc
        """
        self._instance_object._restore_association = self._subClientEntity
        source_user_list = self._get_user_guids(users)
        kwargs = {
            'disk_restore': True,
            'destination_path': destination_path,
            'destination_client': destination_client,
            'skip_file_permissions': skip_file_permissions
        }
        restore_json = self._instance_object._prepare_restore_json(source_user_list, **kwargs)
        return self._process_restore_response(restore_json)

    def out_of_place_restore(self, users: list, destination_path: str, **kwargs) -> 'Job':
        """Run an out-of-place restore job for specified users on a OneDrive for Business client.

        This method restores data for the given list of users to a specified destination user (SMTP address).
        By default, files already present in the destination are skipped. Additional restore options can be
        controlled via keyword arguments.

        Args:
            users: List of SMTP addresses representing the users whose data will be restored.
            destination_path: SMTP address of the destination user where data will be restored.
            **kwargs: Optional keyword arguments to customize the restore operation:
                - overwrite (bool): If True, unconditionally overwrite files during restore (default: False).
                - restore_as_copy (bool): If True, restore files as copies (default: False).
                - skip_file_permissions (bool): If True, skip restoring file permissions (default: False).
                - destination_type (str): Type of destination for out-of-place restore.
                - end_time (int): Job end time for point-in-time restore (default: None).
                - destination_label (str): Label where restore should be performed in the mailbox.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If both 'overwrite' and 'restore_as_copy' options are selected.

        Example:
            >>> users = ['user1@domain.com', 'user2@domain.com']
            >>> destination = 'destination_user@domain.com'
            >>> job = subclient.out_of_place_restore(
            ...     users,
            ...     destination,
            ...     overwrite=True,
            ...     skip_file_permissions=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', False)
        end_time = kwargs.get('end_time', None)
        destination_label = kwargs.get('destination_label', "")

        if overwrite and restore_as_copy:
            raise SDKException('Subclient', '102', 'Either select overwrite or restore as copy for file options')

        self._instance_object._restore_association = self._subClientEntity
        source_user_list = self._get_user_guids(users)
        accountInfo = {}
        destination_type = kwargs.get("destination_type")
        if destination_type == 'USER' or destination_type == 'MAILBOX':
            destination_user_info = self.search_for_user(destination_path)
            accountInfo['userDisplayName'] = destination_user_info.get('displayName', '')
            accountInfo['userGUID'] = destination_user_info.get('user').get('userGUID', '')
            accountInfo['userSMTP'] = destination_user_info.get('smtpAddress', '')
        else:
            destination_user_info = self.search_for_shareddrive(destination_path)
            accountInfo['userDisplayName'] = destination_user_info.get('folderTitle', '')
            accountInfo['userGUID'] = destination_user_info.get('folderId', '')

        kwargs = {
            'out_of_place': True,
            'overwrite': overwrite,
            'restore_as_copy': restore_as_copy,
            'skip_file_permissions': skip_file_permissions,
            'accountInfo': accountInfo,
            'destination_type': destination_type,
            'destination_path': destination_path,
            'destination_label': destination_label
        }
        restore_json = self._instance_object._prepare_restore_json(source_user_list, **kwargs)
        if end_time:
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

            add_to_time = restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]
            add_to_time["timeRange"] = {"toTime": end_time}
            add_backup_time = \
                restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"][
                    "googleRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0]["filter"]["filters"]
            add_backup_time.append(adv_search_bkp_time_dict)
        return self._process_restore_response(restore_json)

    def in_place_restore(self, users: list, **kwargs: dict) -> 'Job':
        """Run an in-place restore job for specified users on OneDrive for Business.

        This method initiates an in-place restore operation for the provided list of user SMTP addresses.
        By default, files already present at the destination are skipped during the restore process.
        Additional restore options can be specified using keyword arguments.

        Args:
            users: List of SMTP addresses (strings) representing the users whose data will be restored.
            **kwargs: Optional keyword arguments to customize the restore behavior:
                - overwrite (bool): If True, unconditionally overwrite files during restore (default: False).
                - restore_as_copy (bool): If True, restore files as copies instead of overwriting (default: False).
                - skip_file_permissions (bool): If True, skip restoring file permissions (default: False).
                - include_deleted_items (bool): If True, include deleted items in the restore (default: False).
                - end_time (int): Unix timestamp specifying the job end time for point-in-time restore (default: None).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If both 'overwrite' and 'restore_as_copy' options are set to True.

        Example:
            >>> users = ['user1@example.com', 'user2@example.com']
            >>> # Start an in-place restore with overwrite enabled
            >>> job = subclient.in_place_restore(users, overwrite=True)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        overwrite = kwargs.get('overwrite', False)
        restore_as_copy = kwargs.get('restore_as_copy', False)
        skip_file_permissions = kwargs.get('skip_file_permissions', False)
        include_deleted_items = kwargs.get('include_deleted_items', False)
        end_time = kwargs.get('end_time', None)

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
        restore_json = self._instance_object._prepare_restore_json(source_user_list, **kwargs)
        if end_time:
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

            add_to_time = restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]
            add_to_time["timeRange"] = {"toTime": end_time}
            add_backup_time = \
                restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"][
                    "googleRestoreOptions"]["findQuery"]["advSearchGrp"]["fileFilter"][0]["filter"]["filters"]
            add_backup_time.append(adv_search_bkp_time_dict)

        return self._process_restore_response(restore_json)

    def _get_user_guids(self, users: List[str]) -> List[str]:
        """Retrieve GUIDs for the specified users based on their SMTP addresses.

        Args:
            users: List of SMTP addresses representing the users whose GUIDs are to be retrieved.

        Returns:
            List of GUID strings corresponding to the specified users.

        Raises:
            SDKException: If user details could not be found in the discovered data.

        Example:
            >>> subclient = GoogleSubclient()
            >>> smtp_addresses = ['user1@example.com', 'user2@example.com']
            >>> guids = subclient._get_user_guids(smtp_addresses)
            >>> print(guids)
            ['guid-for-user1', 'guid-for-user2']

        #ai-gen-doc
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
        return user_guid_list

    def process_index_retention_rules(self, index_app_type_id: int, index_server_client_name: str) -> None:
        """Process index retention rules for a specified index server.

        This method makes an API call to process index retention rules for the given index application type ID
        and the specified index server client name.

        Args:
            index_app_type_id: The ID representing the index application type.
            index_server_client_name: The client name of the index server for which to process retention rules.

        Raises:
            SDKException: If the index server is not found, the response is empty, or the response indicates failure.

        Example:
            >>> subclient = GoogleSubclient()
            >>> subclient.process_index_retention_rules(101, "index_server_01")
            >>> print("Index retention rules processed successfully.")

        #ai-gen-doc
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

    def refresh_retention_stats(self) -> None:
        """Refresh the retention statistics for the Google subclient.

        This method updates the retention statistics, ensuring that the latest retention information
        is available for the client associated with this GoogleSubclient instance.

        Example:
            >>> subclient = GoogleSubclient()
            >>> subclient.refresh_retention_stats()
            >>> print("Retention stats refreshed successfully")

        #ai-gen-doc
        """
        request_json = {
            "appType": constants.GMAIL_INDEX_APP_TYPE if self._instance_object.ca_instance_type == 'GMAIL' else constants.GDRIVE_INDEX_APP_TYPE,
            "subclientId": int(self.subclient_id)
        }
        refresh_retention = self._services['OFFICE365_PROCESS_INDEX_RETENTION_RULES']
        flag, response = self._cvpysdk_object.make_request(
            'POST', refresh_retention, request_json)

        if flag:
            if response and response.text.strip():
                try:
                    resp_json = response.json()
                except ValueError:
                    raise SDKException('Response', '102', 'Invalid JSON in response')

                if 'errorCode' in resp_json:
                    error_code = resp_json.get('errorCode')
                    if error_code != 0:
                        error_message = resp_json.get('errorMessage', 'Unknown error')
                        raise SDKException('Subclient', '102', error_message)
            else:
                # Response is empty
                raise SDKException('Response', '102', 'Empty response from server')
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text if response else ''))

        # Return empty dict if response is empty
        return response.json() if response and response.text.strip() else {}

    def refresh_stats_status(self, user_level: bool) -> None:
        """Refresh the statistics status at the client or user level for the client.

        Args:
            user_level: If True, refreshes user-level statistics; if False, refreshes client-level statistics.

        Example:
            >>> subclient = GoogleSubclient()
            >>> subclient.refresh_stats_status(user_level=True)   # Refresh user-level stats
            >>> subclient.refresh_stats_status(user_level=False)  # Refresh client-level stats

        #ai-gen-doc
        """
        if self._instance_object.ca_instance_type == 'GMAIL':
            request_json = {
                "appType": constants.GMAIL_INDEX_APP_TYPE,
                "gmailIdxStatsReq":
                    [{
                        "subclientId": int(self.subclient_id), "type": 1 if user_level else 0}]
            }
        else:
            request_json = {
                "appType": constants.GDRIVE_INDEX_APP_TYPE,
                "googleDriveIdxStatsReq":
                    [{
                        "subclientId": int(self.subclient_id), "type": 1 if user_level else 0}]
            }
        refresh_backup_stats = self._services['OFFICE365_POPULATE_INDEX_STATS']
        flag, response = self._cvpysdk_object.make_request(
            'POST', refresh_backup_stats, request_json)

        if flag:
            if response and response.text.strip():
                try:
                    resp_json = response.json()
                except ValueError:
                    raise SDKException('Response', '102', 'Invalid JSON in response')

                if 'errorCode' in resp_json:
                    error_code = resp_json.get('errorCode')
                    if error_code != 0:
                        error_message = resp_json.get('errorMessage', 'Unknown error')
                        raise SDKException('Subclient', '102', error_message)
            else:
                # Response is empty
                raise SDKException('Response', '102', 'Empty response from server')
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text if response else ''))

    def get_client_level_stats(self) -> dict:
        """Retrieve client-level statistics for the current client.

        Returns:
            dict: A JSON-compatible dictionary containing client-level statistics.

        Example:
            >>> subclient = GoogleSubclient()
            >>> stats = subclient.get_client_level_stats()
            >>> print(stats)
            >>> # Output will be a dictionary with client statistics

        #ai-gen-doc
        """
        get_backup_stats = self._services['OFFICE365_OVERVIEW_STATS'] % self._backupset_object.backupset_id
        flag, response = self._cvpysdk_object.make_request(
            'GET', get_backup_stats)

        if flag:
            if response and response.text.strip():
                try:
                    resp_json = response.json()
                except ValueError:
                    raise SDKException('Response', '102', 'Invalid JSON in response')

                if 'errorCode' in resp_json:
                    error_code = resp_json.get('errorCode')
                    if error_code != 0:
                        error_message = resp_json.gt('errorMessage', 'Unknown error')
                        raise SDKException('Subclient', '102', error_message)
            else:
                # Response is empty
                raise SDKException('Response', '102', 'Empty response from server')
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text if response else ''))

        # Return empty dict if response is empty
        return response.json() if response and response.text.strip() else {}

    def get_user_level_stats(self) -> dict:
        """Retrieve user-level statistics for the Google subclient.

        Returns:
            dict: A dictionary containing entity-level statistics as returned by the API.

        Example:
            >>> subclient = GoogleSubclient()
            >>> stats = subclient.get_user_level_stats()
            >>> print(stats)
            >>> # Output will be a dictionary with user-level statistics

        #ai-gen-doc
        """
        request_json = {
            "bIncludeDeleted": False,
            "pagingInfo": {
                "pageNumber": 0,
                "pageSize": 100
            },
            "discoverByType": constants.GMAIL_DISCOVERY_TYPE if self._instance_object.ca_instance_type == 'GMAIL' else constants.GDRIVE_DISCOVERY_TYPE,
            "cloudAppAssociation": {
                "subclientEntity": {
                    "subclientId": int(self.subclient_id),
                    "applicationId": AppIDAType.CLOUD_APP.value
                }
            }
        }
        if self._instance_object.ca_instance_type == 'GMAIL':
            get_backup_stats = self._services['GMAIL_GET_USERS']
        else:
            get_backup_stats = self._services['GDRIVE_GET_USERS']
        flag, response = self._cvpysdk_object.make_request(
            'POST', get_backup_stats, request_json)

        if flag:
            if response and response.text.strip():
                try:
                    resp_json = response.json()
                except ValueError:
                    raise SDKException('Response', '102', 'Invalid JSON in response')

                if 'errorCode' in resp_json:
                    error_code = resp_json.get('errorCode')
                    if error_code != 0:
                        error_message = resp_json.get('errorMessage', 'Unknown error')
                        raise SDKException('Subclient', '102', error_message)
            else:
                # Response is empty
                raise SDKException('Response', '102', 'Empty response from server')
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text if response else ''))

        # Return empty dict if response is empty
        return response.json() if response and response.text.strip() else {}

    def browse_folders(self, folder_id: str) -> dict:
        """Browse and retrieve folders for a user based on the provided folder ID.

        This method allows you to browse folders associated with a user in Google Workspace environments,
        such as Gmail or Google Drive, by specifying the relevant folder ID. The folder ID can represent
        either the owner ID of the mailbox/user or a specific folder/label ID, depending on the agent type.

        Args:
            folder_id: The ID of the folder to browse. For Gmail agents, this can be the OwnerId (mailbox)
                or GMAIL_LABELV2_ID (specific folder). For Google Drive agents, this can be the OwnerId
                (user) or the Folder Id (specific folder).

        Returns:
            A dictionary containing the details of the browsed folders.

        Example:
            >>> subclient = GoogleSubclient()
            >>> folder_info = subclient.browse_folders('1234567890abcdef')
            >>> print(folder_info)
            >>> # Output will be a dictionary with folder details

        #ai-gen-doc
        """
        req_payload = copy.deepcopy(constants.WEB_SEARCH_PAYLOAD)
        filters = req_payload.get("advSearchGrp").get("emailFilter")[0].get("filter").get("filters")
        for filter in filters:
            if filter.get("field") == "DATA_TYPE":
                filter["fieldValues"]["values"] = [str(constants.GMAIL_FOLDER_DOCUMENT_TYPE)
                                                   if self._instance_object.ca_instance_type == 'GMAIL'
                                                   else str(constants.GDRIVE_FOLDER_DOCUMENT_TYPE)]
                break
        filter_field = constants.BROWSE_FIELD_FILTER_PAYLOAD
        filter_field["field"] = "PARENT_GUID"
        filter_field["fieldValues"]["values"] = [str(folder_id)]
        filters.append(filter_field)
        req_payload["advSearchGrp"]["emailFilter"][0]["filter"]["filters"] = filters
        req_payload["advSearchGrp"]["galaxyFilter"][0]["appIdList"] = [int(self.subclient_id)]
        return self.__do_submit_browse_request(req_payload=req_payload)

    def browse_mails(self, label_id: Optional[str] = None, client_level_browse: bool = False,
                     facet_filters: Optional[dict] = None) -> dict:
        """Browse emails for a user, optionally filtered by label, client level, or facet filters.

        Args:
            label_id: Optional; The ID of the folder (label) to browse within. If None, browses all folders.
            client_level_browse: If True, performs browsing at the client level rather than subclient level.
            facet_filters: Optional; A dictionary of additional filters to apply to the browse operation.

        Returns:
            A list containing all emails present inside the specified label (folder) or matching the given filters.

        Example:
            >>> # Browse all mails in a specific label
            >>> mails = google_subclient.browse_mails(label_id='INBOX')
            >>> print(f"Found {len(mails)} mails in INBOX")
            >>>
            >>> # Browse mails at client level with filters
            >>> filters = {'from': 'user@example.com'}
            >>> mails = google_subclient.browse_mails(client_level_browse=True, facet_filters=filters)
            >>> print(f"Filtered mails: {mails}")

        #ai-gen-doc
        """
        req_payload = copy.deepcopy(constants.WEB_SEARCH_PAYLOAD)
        filters = req_payload.get("advSearchGrp").get("emailFilter")[0].get("filter").get("filters")
        for filter in filters:
            if filter.get("field") == "DATA_TYPE":
                filter["fieldValues"]["values"] = [str(constants.GMAIL_MAIL_DOCUMENT_TYPE)]
                break
        if label_id:
            filter_field = constants.BROWSE_FIELD_FILTER_PAYLOAD
            filter_field["field"] = "GMAILV2_LABEL_ID"
            filter_field["fieldValues"]["values"] = [str(label_id)]
            filters.append(filter_field)
        elif facet_filters and client_level_browse:
            filters.append(facet_filters)
        else:
            raise SDKException("Subclient", "102", "Filters are needed to be supplied for client level browse")
        req_payload["advSearchGrp"]["emailFilter"][0]["filter"]["filters"] = filters
        req_payload["advSearchGrp"]["galaxyFilter"][0]["appIdList"].append(int(self.subclient_id))
        return self.__do_submit_browse_request(req_payload=req_payload)

    def browse_files(self, client_level_browse: bool = False, search_keyword: str = '*',
                     facet_filters: dict = None) -> dict:
        """Browse files for the user within the GoogleSubclient.

        This method allows you to browse and search for files associated with the user.
        You can perform a client-level browse, filter results using a search keyword,
        and apply additional facet filters.

        Args:
            client_level_browse: Set to True to perform a client-level browse. Defaults to False.
            search_keyword: The keyword to search for in the browse operation. Defaults to '*', which returns all files.
            facet_filters: Optional dictionary of filters to further refine the browse results.

        Returns:
            A dict containing all files present for the user that match the search criteria.

        Example:
            >>> subclient = GoogleSubclient()
            >>> files = subclient.browse_files(client_level_browse=True, search_keyword='report', facet_filters={'type': 'pdf'})
            >>> print(f"Found {len(files)} PDF reports")
            >>> # The returned list contains file details matching the criteria

        #ai-gen-doc
        """
        req_payload = copy.deepcopy(constants.GDRIVE_WEB_SEARCH_PAYLOAD)
        file_filters = [{
            "field": "FILE_NAME",
            "fieldValues": {
                "values": [
                    "",
                    search_keyword
                ]
            },
            "intraFieldOp": 0
        }]

        req_payload['advSearchGrp']['fileFilter'] = file_filters
        req_payload["advSearchGrp"]["galaxyFilter"][0]["appIdList"].append(int(self.subclient_id))

        if facet_filters:
            req_payload["facetRequests"]["facetRequest"] = facet_filters
        return self.__do_submit_browse_request(req_payload=req_payload)