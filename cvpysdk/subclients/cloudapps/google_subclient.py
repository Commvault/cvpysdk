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

    add_user                            --  adds user to the subclient

"""

from __future__ import unicode_literals

from ...exception import SDKException

from ..casubclient import CloudAppsSubclient


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

            if temp_account['contentType'] == 134:
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
                            "contentType": 134,
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
        flag,response = self._cvpysdk_object.make_request('POST', add_user, request_json)

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