# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing user group operations.

UserGroups and UserGroup are the classes defined in this file.

UserGroups: Class for representing all the user groups associated with a commcell

UserGroup:  Class for representing a single User Group of the commcell

UserGroups:
    __init__(commcell_object)  --  initialise instance of the UserGroups associated with
                                       the specified commcell

    __str__()                  --  returns all the user groups associated with the commcell

    __repr__()                 --  returns the string for the instance of the UserGroups class

    _get_usergroups()          --  gets all the usergroups associated with the commcell specified

    has_user_group()           --  checks if a user group exists with the given name or not

    get(user_group_name)       --  returns the instance of the UserGroup class,
                                       for the the input user group name

    delete(user_group_name)    --  deletes the user group from the commcell

    refresh()                  --  refresh the user groups associated with the commcell


UserGroup:
    __init__(commcell_object,
             usergroup_name,
             usergroup_id=None)  -- initialise instance of the UserGroup for the commcell

    __repr__()                   -- return the usergroup name, the instance is associated with

    _get_usergroup_id()          -- method to get the usergroup id, if not specified in __init__

    _get_usergroup_properties()  -- get the properties of this usergroup

    refresh()                    -- refresh the properties of the user group

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

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
        self._USERGROUPS = self._commcell_object._services['USERGROUPS']

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
            self._commcell_object._headers['Host']
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
            'GET', self._USERGROUPS
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
                bool - boolean output whether the user group exists in the commcell or not

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
                return UserGroup(
                    self._commcell_object,
                    user_group_name,
                    self._user_groups[user_group_name]
                )

            raise SDKException(
                'UserGroup', '102', 'No user group exists with name: {0}'.format(user_group_name)
            )

    def delete(self, user_group_name):
        """Deletes the usergroup from the commcell.

            Args:
                user_group_name (str)  --  name of the usergroup to remove from the commcell

            Raises:
                SDKException:
                    if type of the usergroup name argument is not string

                    if failed to delete usergroup

                    if response is empty

                    if response is not success

                    if no usergroup exists with the given name
        """

        if not isinstance(user_group_name, basestring):
            raise SDKException('UserGroup', '101')
        else:
            user_group_name = user_group_name.lower()

            if self.has_user_group(user_group_name):
                usergroup_id = self._user_groups[user_group_name]

                delete_usergroup = self._commcell_object._services['USERGROUP'] % (usergroup_id)

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'DELETE', delete_usergroup
                )

                if flag:
                    if response.json() and 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = response_value['errorString']

                        if error_message:
                            o_str = 'Failed to delete user group\nError: "{0}"'
                            raise SDKException(
                                'UserGroup', '102', o_str.format(error_message)
                            )
                        else:
                            if error_code == '0':
                                # initialize the usergroup again
                                # so the usergroups object has all the usergroups
                                self.refresh()
                            else:
                                o_str = ('Failed to delete usergroup with error code: "{0}"'
                                         '\nPlease check the documentation for '
                                         'more details on the error')
                                raise SDKException(
                                    'UserGroup', '102', o_str.format(error_code)
                                )
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'UserGroup',
                    '102',
                    'No usergroup exists with name: {0}'.format(user_group_name)
                )

    def refresh(self):
        """Refresh the user groups associated with the Commcell."""
        self._user_groups = self._get_user_groups()


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

        self._USERGROUP = self._commcell_object._services['USERGROUP'] % (self.user_group_id)

        self._description = None
        self._email = None
        self._users = []
        self._security_associations = {}

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'User Group instance for UserGroup: "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self.user_group_name, self._commcell_object._headers['Host']
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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._USERGROUP)

        if flag:
            if response.json() and 'userGroups' in response.json():
                usergroup_properties = response.json()['userGroups'][0]

                if 'description' in usergroup_properties:
                    self._description = usergroup_properties['description']

                if 'email' in usergroup_properties:
                    self._email = usergroup_properties['email']

                if 'users' in usergroup_properties:
                    for user in usergroup_properties['users']:
                        self._users.append(user['userName'])

                if 'securityAssociations' in usergroup_properties:
                    if 'associations' in usergroup_properties['securityAssociations']:
                        associations = usergroup_properties['securityAssociations']['associations']

                        for association in associations:
                            entity = association['entities']['entity'][0]

                            if 'commCellName' in entity:
                                name = entity['commCellName']
                            elif 'userGroupName' in entity:
                                name = entity['userGroupName']
                            else:
                                return

                            properties = association['properties']

                            if name not in self._security_associations:
                                self._security_associations[name] = {
                                    'permissions': set([]),
                                    'roles': set([])
                                }

                            permission = None
                            role = None

                            if 'categoryPermission' in properties:
                                permissions = properties['categoryPermission']
                                permission_list = permissions['categoriesPermissionList'][0]
                                permission = permission_list['permissionName']
                            elif 'permissions' in properties:
                                permission = properties['permissions'][0]['permissionName']
                            elif 'role' in properties:
                                role = properties['role']['roleName']

                            if permission is not None:
                                self._security_associations[name]['permissions'].add(
                                    permission
                                )

                            if role is not None:
                                self._security_associations[name]['roles'].add(role)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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

    @property
    def users(self):
        """Treats the usergroup users as a read-only attribute."""
        return self._users

    @property
    def associations(self):
        """Treats the usergroup security associations as a read-only attribute."""
        return self._security_associations

    def refresh(self):
        """Refresh the properties of the UserGroup."""
        self._get_usergroup_properties()
