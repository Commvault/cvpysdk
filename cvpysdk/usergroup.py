#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing user group operations.

UserGroups and UserGroup are the classes defined in this file.

UserGroups: Class for representing all the user groups associated with a commcell

UserGroup:  Class for representing a single User Group of the commcell

UserGroups:
    __init__(commcell_object)  -- initialise instance of the UserGroups associated with
                                    the specified commcell
    __repr__()                 -- return all the usergroups associated with the specified commcell
    _get_usergroups()          -- gets all the usergroups associated with the commcell specified
    get(usergroup_name)        -- returns the instance of the UserGroup class,
                                    for the the input user group name

UserGroup:
    __init__(commcell_object,
             usergroup_name,
             usergroup_id=None)  -- initialise object of UserGroup class with the specified
                                     usergroup name and id
    __repr__()                   -- return the usergroup name, the instance is associated with
    _get_usergroup_id()          -- method to get the usergroup id, if not specified in __init__
    _get_usergroup_properties()  -- get the properties of this usergroup

"""

from exception import SDKException


class UserGroups(object):
    """Class for getting all the usergroups associated with a commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the UserGroups class.

            Args:
                commcell_object (object) - instance of the Commcell class

            Returns:
                object - instance of the UserGroups class
        """
        self._commcell_object = commcell_object
        self._USER_GROUPS = self._commcell_object._services.GET_ALL_USERGROUPS
        self._user_groups = self._get_user_groups()

    def __repr__(self):
        """Representation string for the instance of the UserGroups class.

            Returns:
                str - string of all the user groups associated with the commcell
        """
        representation_string = ""

        for user_group_name, _ in self._user_groups.items():
            sub_str = 'User Group "{0}" of Commcell: "{1}"\n'
            sub_str.format(user_group_name, self._commcell_object._headers['Host'])
            representation_string += sub_str

        return representation_string.strip()

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET',
                                                                            self._USER_GROUPS)

        if flag:
            if response.json():
                user_groups_dict = {}

                if 'userGroups' in response.json():
                    response_value = response.json()['userGroups']

                    for temp in response_value:
                        temp_name = str(temp['userGroupEntity']['userGroupName']).lower()
                        temp_id = str(temp['userGroupEntity']['userGroupId']).lower()
                        user_groups_dict[temp_name] = temp_id

                return user_groups_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def get(self, user_group_name):
        """Returns a user group object of the specified user group name.

            Args:
                user_group_name (str) - name of the user group

            Returns:
                object - instance of the UserGroup class for the given user group name

            Raises:
                SDKException:
                    if type of the user group name argument is not string
                    if no user group exists with the given name
        """
        if not isinstance(user_group_name, str):
            raise SDKException('UserGroup', '103')
        else:
            user_group_name = str(user_group_name).lower()
            all_usergroups = self._user_groups

            if all_usergroups and user_group_name in all_usergroups:
                return UserGroup(self._commcell_object,
                                 user_group_name,
                                 all_usergroups[user_group_name])

            raise SDKException('UserGroup',
                               '104',
                               'No user group exists with name: {0}'.format(user_group_name))


class UserGroup(object):
    """Class for performing operations for a specific User Group."""

    def __init__(self, commcell_object, user_group_name, user_group_id=None):
        """Initialise the UserGroup class instance.

            Args:
                commcell_object (object) - instance of the Commcell class
                user_group_name (str) - name of the user group
                user_group_id (str) - id of the user group
                    default: None

            Returns:
                object - instance of the UserGroup class
        """
        self._commcell_object = commcell_object
        self._user_group_name = str(user_group_name).lower()

        if user_group_id:
            self._user_group_id = str(user_group_id)
        else:
            self._user_group_id = self._get_usergroup_id()

        self._USERGROUP = self._commcell_object._services.USERGROUP % (self.usergroup_id)
        self.properties = self._get_usergroup_properties()

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string containing the details of this user group
        """
        representation_string = 'User Group instance for UserGroup: "{0}", of Commcell: "{1}"'

        return representation_string.format(self.user_group_name,
                                            self._commcell_object._headers['Host'])

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
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    @property
    def user_group_id(self):
        """Treats the usergroup id as a read-only attribute."""
        return self._usergroup_id

    @property
    def user_group_name(self):
        """Treats the usergroup name as a read-only attribute."""
        return self._user_group_name
