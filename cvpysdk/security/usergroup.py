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

"""Main file for performing user group operations.

UserGroups and UserGroup are the classes defined in this file.

UserGroups: Class for representing all the user groups associated with a commcell

UserGroup:  Class for representing a single User Group of the commcell

UserGroups:
    __init__(commcell_object)       --  Initialise instance of the UserGroups
                                        associated with the specified commcell

    __str__()                       --  Returns all the user groups associated with
                                        the commcell

    __repr__()                      --  Returns the string for the instance of the
                                        UserGroups class

    _get_usergroups()               --  Gets all the usergroups associated with the
                                        commcell specified

    has_user_group()                --  Checks if a user group exists with the given
                                        name or not

    get(user_group_name)            --  Returns the instance of the UserGroup class,
                                        for the the input user group name

    add()                           --  Adds local/external user group on this
                                        commserver

    delete(user_group_name)         --  Deletes the user group from the commcell

    refresh()                       --  Refresh the user groups associated with the
                                        commcell

    all_user_groups()               --  Returns all the usergroups present in the commcell


UserGroup:
    __init__(commcell_object,
             usergroup_name,
             usergroup_id=None)     --  initialise instance of the UserGroup for the
                                        commcell

    __repr__()                      --  return the usergroup name, the instance is
                                        associated with

    _get_usergroup_id()             --  method to get the usergroup id, if not
                                        specified in __init__

    _get_usergroup_properties()     --  get the properties of this usergroup

    _has_usergroup()                --  checks list of users present on the commcell

    refresh()                       --  refresh the properties of the user group

    status()                        --  sets status for users (enable or disable)

    update_security_associations()  --  updates 3-way security associations on usergroup

    update_usergroup_members()      --  DELETE, OVERWRITE users with this usergroup

    _send_request()                 --  forms complete joson request for usergroup

    _update_usergroup_props()       --  Updates the properties of this usergroup

    users()                         --  returns users who are members of this usergroup

    usergroups()                    --  returns external usergroups who are members of this
                                        usergroup

    user_group_id()                 --  returns group id of this user group

    user_group_name()               --  returns user group name of this group

    description()                   --  returns the description set for this user group

    email()                         --  returns the email of this user group

    associations()                  --  Returns security associations present on the usergroup

    is_tfa_enabled()                --  Returns status of tfa

    enable_tfa()                    --  Enables tfa for this user group

    disable_tfa()                   --  Disables tfa for this user group

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from past.builtins import basestring
from .security_association import SecurityAssociation

from ..exception import SDKException


class UserGroups(object):
    """Class for getting all the usergroups associated with a commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the UserGroups class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the UserGroups class

        """
        self._commcell_object = commcell_object
        self._user_group = self._commcell_object._services['USERGROUPS']

        self._user_groups = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all usergroups of the Commcell.

            Returns:
                str - string of all the usergroups for a commcell
        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'User Group')

        for index, user_group in enumerate(self._user_groups):
            sub_str = '{:^5}\t{:30}\n'.format(index + 1, user_group)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the UserGroups class."""
        return "UserGroups class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_user_groups(self):
        """Gets all the user groups associated with the commcell

            Returns:
                dict - consists of all user group in the commcell
                    {
                         "user_group1_name": user_group1_id,
                         "user_group2_name": user_group2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._user_group
        )

        if flag:
            if response.json() and 'userGroups' in response.json():
                response_value = response.json()['userGroups']
                user_groups_dict = {}

                for temp in response_value:
                    temp_name = temp['userGroupEntity']['userGroupName'].lower()
                    temp_id = str(temp['userGroupEntity']['userGroupId']).lower()
                    user_groups_dict[temp_name] = temp_id

                return user_groups_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_user_group(self, user_group_name):
        """Checks if a user group exists in the commcell with the input user group name.

            Args:
                user_group_name (str)  --  name of the user group

            Returns:
                bool - boolean output whether the user group exists in the commcell
                       or not

            Raises:
                SDKException:
                    if type of the user group name argument is not string
        """
        if not isinstance(user_group_name, basestring):
            raise SDKException('UserGroup', '101')

        return self._user_groups and user_group_name.lower() in self._user_groups

    def get(self, user_group_name):
        """Returns a user group object of the specified user group name.

            Args:
                user_group_name (str)  --  name of the user group

            Returns:
                object - instance of the UserGroup class for the given user group name

            Raises:
                SDKException:
                    if type of the user group name argument is not string

                    if no user group exists with the given name
        """
        if not isinstance(user_group_name, basestring):
            raise SDKException('UserGroup', '101')
        else:
            user_group_name = user_group_name.lower()

            if self.has_user_group(user_group_name):
                return UserGroup(self._commcell_object, user_group_name, self._user_groups[
                    user_group_name])

            raise SDKException(
                'UserGroup', '102', 'No user group exists with name: {0}'.format(
                    user_group_name)
            )

    def add(self,
            usergroup_name,
            domain=None,
            users_list=None,
            entity_dictionary=None,
            external_usergroup=None,
            local_usergroup=None):
        """Adds local/external user group on this commcell based domain parameter provided

            Args:
                usergroup_name (str)        --  name of the user group

                domain  (str)               --  name of the domain to which user group
                                                belongs to

                users_list	(list)			--  list which contains users who will be
                                                members of this group

                entity_dictionary(dict)     --  combination of entity_type, entity
                                                names and role
                e.g.: security_dict={
                                'assoc1':
                                    {
                                        'entity_type':['entity_name'],
                                        'entity_type':['entity_name', 'entity_name'],
                                        'role': ['role1']
                                    },
                                'assoc2':
                                    {
                                        'mediaAgentName': ['networktestcs', 'standbycs'],
                                        'clientName': ['Linux1'],
                                        'role': ['New1']
                                        }
                                    }
                entity_type         --      key for the entity present in dictionary
                                            on which user will have access
                entity_name         --      Value of the key
                role                --      key for role name you specify
                e.g:   e.g.: {"clientName":"Linux1"}
                Entity Types are:   clientName, mediaAgentName, libraryName, userName,
                                    userGroupName, storagePolicyName, clientGroupName,
                                    schedulePolicyName, locationName, providerDomainName,
                                    alertName, workflowName, policyName, roleName

                entity_name = "Linux1", "ClientMachine1"

                external_usergroup(list)    --  list of domain user group which could
                                                be added as members to this group

                local_usergroup (list)      --  list of commcell usergroup which could
                                                be added as members to this group

            Returns:
                (object)    -   UserGroup class instance for the specified user group name

            Raises:
                SDKException:

                    if usergroup with specified name already exists

                    if failed to add usergroup to commcell
        """
        if domain:
            group_name = "{0}\\{1}".format(domain, usergroup_name)
        else:
            group_name = usergroup_name

        if self.has_user_group(group_name):
            raise SDKException(
                'User', '102', "UserGroup {0} already exists on this commcell.".format
                (group_name))

        local_usergroup_json = []
        if local_usergroup:
            local_usergroup_json = [{"userGroupName": local_group}
                                    for local_group in local_usergroup]

        security_json = {}
        if entity_dictionary:
            security_request = SecurityAssociation._security_association_json(
                entity_dictionary=entity_dictionary)
            security_json = {
                "associationsOperationType": "ADD",
                "associations": security_request
            }
        user_json = []
        if users_list:
            user_json = [{"userName": uname} for uname in users_list]

        external_usergroup_json = []
        if external_usergroup:
            external_usergroup_json = [{"userGroupName": external_group}
                                       for external_group in external_usergroup]

        usergrop_request = {
            "groups": [
                {
                    "userGroupEntity": {
                        "userGroupName": group_name
                    },
                    "securityAssociations": security_json,
                    "users": user_json,
                    "localUserGroups": local_usergroup_json,
                    "associatedExternalUserGroups": external_usergroup_json
                }
            ]
        }

        usergroup_req = self._commcell_object._services['USERGROUPS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', usergroup_req, usergrop_request
        )
        if flag:
            if response.json():
                if 'response' in response.json():
                    response_json = response.json()['response'][0]
                    error_code = response_json['errorCode']
                    error_message = response_json['errorString']
                    if not error_code == 0:
                        raise SDKException('Response', '101', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
        return self.get(group_name)

    def delete(self, user_group, new_user=None, new_usergroup=None):
        """Deletes the specified user from the existing commcell users

            Args:
                user_group          (str)   --  name of the usergroup which has to be deleted

                new_user            (str)   --  name of the target user, whom the ownership
                                                of entities should be transferred

                new_usergroup       (str)   --  name of the user group, whom the ownership
                                                of entities should be transferred

            Note: either user or usergroup  should be provided for ownership
                transfer not both.

            Raises:
                SDKException:

                    if usergroup doesn't exist

                    if new user and new usergroup any of these is passed and these doesn't
                    exist on commcell

                    if both user and usergroup is passed for ownership transfer

                    if both user and usergroup is not passed for ownership transfer

                    if response is not success

        """
        if not self.has_user_group(user_group):
            raise SDKException(
                'UserGroup', '102', "UserGroup {0} doesn't exists on this commcell.".format(
                    user_group)
            )
        if new_user and new_usergroup:
            raise SDKException(
                'User', '102', "{0} and {1} both can not be set as owner!! "
                               "please send either new_user or new_usergroup".format(new_user,
                                                                                     new_usergroup))
        else:
            if new_user:
                if not self._commcell_object.users.has_user(new_user):
                    raise SDKException(
                        'User', '102', "User {0} doesn't exists on this commcell.".format(
                            new_user)
                    )
                new_user_id = self._commcell_object.users._users[new_user.lower()]
                new_group_id = 0
            else:
                if new_usergroup:
                    if not self.has_user_group(new_usergroup):
                        raise SDKException(
                            'UserGroup', '102', "UserGroup {0} doesn't exists "
                                                "on this commcell.".format(new_usergroup)
                        )
                else:
                    raise SDKException(
                        'User', '102',
                        "Ownership transfer is mondatory!! Please provide new owner information"
                    )
                new_group_id = self._commcell_object.user_groups.get(new_usergroup).user_group_id
                new_user_id = 0

        delete_usergroup = self._commcell_object._services['DELETE_USERGROUP'] % (
            self._user_groups[user_group.lower()], new_user_id, new_group_id)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'DELETE', delete_usergroup
        )
        if flag:
            if response.json():
                if 'response' in response.json():
                    response_json = response.json()['response'][0]
                    error_code = response_json['errorCode']
                    error_message = response_json['errorString']
                    if not error_code == 0:
                        raise SDKException('Response', '101', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self._user_groups = self._get_user_groups()

    def refresh(self):
        """Refresh the user groups associated with the Commcell."""
        self._user_groups = self._get_user_groups()

    @property
    def all_user_groups(self):
        """Returns dict of all the user groups associated with this commcell

        dict - consists of all user group in the commcell
                 {
                   "user_group1_name": user_group1_id,
                   "user_group2_name": user_group2_id
                  }

        """
        return self._user_groups


class UserGroup(object):
    """Class for performing operations for a specific User Group."""

    def __init__(self, commcell_object, user_group_name, user_group_id=None):
        """Initialise the UserGroup class instance.

            Args:
                commcell_object     (object)  --  instance of the Commcell class

                user_group_name     (str)     --  name of the user group

                user_group_id       (str)     --  id of the user group
                    default: None

            Returns:
                object - instance of the UserGroup class
        """
        self._commcell_object = commcell_object
        self._user_group_name = user_group_name.lower()

        if user_group_id:
            self._user_group_id = str(user_group_id)
        else:
            self._user_group_id = self._get_usergroup_id()

        self._usergroup = self._commcell_object._services['USERGROUP'] % (self.user_group_id)

        self._description = None
        self._properties = None
        self._email = None
        self._users = []
        self._usergroups = []
        self._usergroup_status = None
        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'User Group instance for UserGroup: "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self.user_group_name, self._commcell_object.commserv_name
        )

    def _get_usergroup_id(self):
        """Gets the user group id associated with this user group.

            Returns:
                str - id associated with this user group
        """
        user_groups = UserGroups(self._commcell_object)
        return user_groups.get(self.user_group_name).user_group_id

    def _get_usergroup_properties(self):
        """Gets the user group properties of this user group.

            Returns:
                dict - dictionary consisting of the properties of this user group

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._usergroup)

        if flag:
            if response.json() and 'userGroups' in response.json():
                self._properties = response.json()['userGroups'][0]

                if 'description' in self._properties:
                    self._description = self._properties['description']

                if 'enabled' in self._properties:
                    self._usergroup_status = self._properties['enabled']

                if 'email' in self._properties:
                    self._email = self._properties['email']

                security_properties = self._properties.get('securityAssociations', {}).get(
                    'associations', {})
                self._security_associations = SecurityAssociation.fetch_security_association(
                    security_dict=security_properties)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _has_usergroup(self, usergroup_list):
        """checks whether these users are present on this commcell

            Args:
            usergroup_list (list)   --   list of local_usergroup or external user group

            Raises:
                SDKException:
                    if user is not found on this commcell
        """
        if usergroup_list is not None:
            for usergroup in usergroup_list:
                if not self._commcell_object.user_groups.has_user_group(usergroup):
                    raise SDKException(
                        'UserGroup', '102', "UserGroup {0} doesn'texists on this commcell.".format(
                            usergroup))

    @property
    def name(self):
        """Returns the UserGroup display name"""
        return self._properties['userGroupEntity']['userGroupName']

    @property
    def user_group_id(self):
        """Treats the usergroup id as a read-only attribute."""
        return self._user_group_id

    @property
    def user_group_name(self):
        """Treats the usergroup name as a read-only attribute."""
        return self._user_group_name

    @property
    def description(self):
        """Treats the usergroup description as a read-only attribute."""
        return self._description

    @property
    def email(self):
        """Treats the usergroup email as a read-only attribute."""
        return self._email

    def refresh(self):
        """Refresh the properties of the UserGroup."""
        self._get_usergroup_properties()

    @property
    def status(self):
        """Returns the status of user group on this commcell"""
        return self._usergroup_status

    @status.setter
    def status(self, value):
        """Sets the status for this commcell user group"""

        request_json = {
            "groups": [{
                "enabled": value
            }]
        }
        self._update_usergroup_props(request_json)

    @property
    def users(self):
        """Returns the list of associated users with this usergroup"""
        users = []
        if 'users' in self._properties:
            for user in self._properties['users']:
                users.append(user['userName'])

        return users

    @property
    def usergroups(self):
        """Returns the list of associated external usergroups with this usergroup"""
        user_groups = []
        if 'externalUserGroups' in self._properties:
            for user_group in self._properties['externalUserGroups']:
                user_groups.append(user_group['externalGroupName'])

        return user_groups

    @property
    def associations(self):
        """Returns security associations present on th usergroup"""
        return self._security_associations

    @property
    def is_tfa_enabled(self):
        """Returns two factor authentication status (True/False)"""
        return self._properties.get('enableTwoFactorAuthentication') == 1

    def enable_tfa(self):
        """
        enables two factor authentication on this group

            Note: tfa will not get enabled for this user group if global tfa is disabled

        Returns:
             None
        """
        request_json = {
            "groups": [{
                "enableTwoFactorAuthentication": 1
            }]
        }
        self._update_usergroup_props(request_json)

    def disable_tfa(self):
        """
        disables two factor authentication for this group

        Returns:
            None
        """
        request_json = {
            "groups": [{
                "enableTwoFactorAuthentication": 0
            }]
        }
        self._update_usergroup_props(request_json)

    def update_security_associations(self, entity_dictionary, request_type):
        """handles three way associations (role-usergroup-entities)

            Args:
                entity_dictionary   (dict)      --  combination of entity_type, entity names
                                                    and role
                e.g.: security_dict={
                                'assoc1':
                                    {
                                        'entity_type':['entity_name'],
                                        'entity_type':['entity_name', 'entity_name'],
                                        'role': ['role1']
                                    },
                                'assoc2':
                                    {
                                        'mediaAgentName': ['networktestcs', 'standbycs'],
                                        'clientName': ['Linux1'],
                                        'role': ['New1']
                                        }
                                    }

                entity_type         --      key for the entity present in dictionary
                                            on which user will have access

                entity_name         --      Value of the key

                role                --      key for role name you specify

                e.g.: {"clientName":"Linux1"}
                Entity Types are:   clientName, mediaAgentName, libraryName, userName,
                                    userGroupName, storagePolicyName, clientGroupName,
                                    schedulePolicyName, locationName, providerDomainName,
                                    alertName, workflowName, policyName, roleName

                entity_name:        client name for entity_type 'clientName'
                                    Media agent name for entitytype 'mediaAgentName'
                                    similar for other entity_types

                request_type        --      decides whether to UPDATE, DELETE or
                                            OVERWRITE user security association.

            Raises:
                SDKException:

                    if failed update user properties

        """
        security_request = {}
        if entity_dictionary:
            security_request = SecurityAssociation._security_association_json(entity_dictionary)

        self._send_request(request_type, association_blob=security_request)

    def update_usergroup_members(
            self,
            request_type,
            users_list=None,
            external_usergroups=None,
            local_usergroups=None):
        """updates users and usergroups to local usergroup members tab
            Args:
                request_type (str)              --      decides whether to UPDATE, DELETE or
                                                        OVERWRITE user security association

                users_list  (list)              --      comlete list of local users and
                                                        externalusers
                e.g : users_list = [r'Red\\RedUser2', r'Red\\RedUser12', r'mirje-pc\\A',
                                    r'mirje-pc\\B', r'John', r'Prasad', r'Mahesh']
                where:
                RedUser2, RedUser12 are belongs to AD 'Red'
                A, B are belongs to AD 'mirje-pc'
                John, Prasad, Mahesh are local users

                external_usergroups (list)      --      complete list of external usergroup only

                e.g : external_usergroups_list = ['Red\\RedGroup2', 'mirje-pc\\XYZ']
                where:
                RedGroup2 is external user group present in AD 'Red'
                XYZ is external user group present in AD 'mirje-pc'

                local_usergroups (list) --  complete list of local user groups
                                            (Not required when updating external
                                            usergroup properties)
                e.g : local_usergroups=['usergroup1', 'usegrouop2']


            Raises:
                SDKException:

                    if failed update local usergroup properties
        """
        if users_list is not None:
            for user in users_list:
                if not self._commcell_object.users.has_user(user):
                    raise SDKException(
                        'User', '102', "User {0} doesn't exists on this commcell.".format(user))
            userlist_json = [{"userName": xuser} for xuser in users_list]
        else:
            userlist_json = []

        if external_usergroups is not None:
            self._has_usergroup(external_usergroups)
            usergroup_json = [{"userGroupName": name} for name in external_usergroups]
        else:
            usergroup_json = []

        if local_usergroups is not None:
            self._has_usergroup(local_usergroups)
            local_groups_json = [{"userGroupName": user_name} for user_name in local_usergroups]
        else:
            local_groups_json = []

        self._send_request(request_type=request_type, users_blob=userlist_json,
                           external_group_blob=usergroup_json, local_group_blob=local_groups_json)

    def _send_request(self, request_type, association_blob=None, users_blob=None,
                      external_group_blob=None, local_group_blob=None):
        """forms complete json request for user groups

            Args:
                request_type        (str)   --  decides whether to UPDATE, DELETE or
                                                OVERWRITE user security association

                association_blob    (dict)  --  security association blob generated from
                                                static method _security_association_json
                                                present in SecurityAssociation

                users_blob          (dict)  --  comlete json blob of local users and
                                                externalusers

                external_group_blob (dict)  --  complete json blob of external
                                                usergroup only

                local_group_blob    (list)  --  complete json blob of local
                                                usergroup only

            Raises:
                SDKException:

                    if failed update local usergroup properties

                    if response received is empty

                    if response is not success
        """
        update_usergroup_request = {
            "NONE": 0,
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3,
        }
        if local_group_blob is None:
            local_group_blob = []

        if association_blob:
            security_association_request = {
                "associationsOperationType": update_usergroup_request[request_type.upper()],
                "associations": association_blob
            }
        else:
            security_association_request = {}

        if users_blob is None:
            users_blob = []

        group_json = {
            "localUserGroupsOperationType": update_usergroup_request[request_type.upper()],
            "usersOperationType": update_usergroup_request[request_type.upper()],
            "externalUserGroupsOperationType": update_usergroup_request[request_type.upper()],
            "securityAssociations": security_association_request,
            "localUserGroups": local_group_blob,
            "users": users_blob
        }
        if external_group_blob is not None:
            group_json.update({"associatedExternalUserGroups": external_group_blob})

        request_json = {
            "groups": [group_json]
        }

        self._update_usergroup_props(request_json)

    def _update_usergroup_props(self, properties_dict):
        """Updates the properties of this usergroup

            Args:
                properties_dict (dict)  --  user property dict which is to be updated

            Raises:
                SDKException:
                    if failed update usergroup properties

                    if response is not success
        """
        usergroup_request = self._commcell_object._services['USERGROUP'] % (self._user_group_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', usergroup_request, properties_dict
        )
        if flag:
            if response.json():
                if 'response' in response.json():
                    response_json = response.json()['response'][0]
                    error_code = response_json['errorCode']
                    error_message = response_json['errorString']
                    if not error_code == 0:
                        raise SDKException('Response', '101', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
