# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for managing users on this commcell

Users and User are only the two classes defined in this commcell

Users
    __init__()                          --  initializes the users class object

    __str__()                           --  returns all the users associated with the commcell

    __repr__()                          --  returns the string for the instance of the Users class

    _get_users()                        --  gets all the users on this commcell

    _process_add_or_delete_response()   --  process the add or delete users response

    add_local_user()                    --  adds the local user on this commcell

    has_user()                          --  checks if user with specified user exists
                                                on this commcell

    get()                               --  returns the user class object for the
                                                specified user name

    delete()                            --  deletes the user on this commcell

    refresh()                           --  refreshes the list of users on this commcell

User
    __init__()                          --  initiaizes the user class object

    __repr__()                          --  returns the string for the instance of the User class

    _get_user_id()                      --  returns the user id associated with this user

    _get_user_properties()              --  gets all the properties associated with this user

    _update_user_props()                --  updates the properties associated with this user

    _update_usergroup_request()         --  makes the request to update usergroups associated
                                                with this user

    user_name()                         --  returns the name of this user

    user_id()                           --  returns the id of this user

    description()                       --  returns the description of this user

    associated_usergroups()             --  returns the usergroups associated with this user

    add_usergroups()                    --  associates the usergroups with this user

    remove_usergroups()                 --  disassociated the usergroups with this user

    overwrite_usergroups()              --  reassociates the usergroups with new list of usergroups
                                                on this user

    refresh()                           --  refreshes the properties of this user

"""

from base64 import b64encode
from past.builtins import basestring

from ..exception import SDKException


class Users(object):
    """Class for maintaining all the configured users on this commcell"""

    def __init__(self, commcell_object):
        """Initializes the users class object for this commcell

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Clients class
        """
        self._commcell_object = commcell_object
        self._users = self._get_users()

    def __str__(self):
        """Representation string consisting of all users of the commcell.

            Returns:
                str - string of all the users configured on the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Users')

        for index, user in enumerate(self._users):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, user)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Users class."""
        return "Users class instance for Commcell: '{0}'".format(
            self._commcell_object._headers['Host']
        )

    def _get_users(self):
        """Returns the list of users configured on this commcell"""
        GET_ALL_USERS_SERVICE = self._commcell_object._services['USERS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', GET_ALL_USERS_SERVICE
        )

        if flag:
            if response.json() and 'users' in response.json():
                users_dict = {}

                for user in response.json()['users']:
                    temp_name = user['userEntity']['userName'].lower()
                    temp_id = user['userEntity']['userId']
                    users_dict[temp_name] = temp_id

                return users_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _process_add_or_delete_response(self, flag, response):
        """Processes the flag and response received from the server during add / delete request

        Args:
            request_object  (object)  --  request objects specifying the details to request

        Raises:
            SDKException:
                if response is empty

                if reponse is not success
        """
        if flag:
            if response.json():
                error_code = -1
                error_message = ''
                if 'response' in response.json():
                    response_json = response.json()['response'][0]
                    error_code = response_json['errorCode']

                elif 'errorCode' in response.json():
                    error_code = response.json()['errorCode']
                    if 'errorMessage' in response:
                        error_message = response['errorMessage']

                return error_code, error_message

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add_local_user(self,
                       user_name,
                       full_name,
                       email,
                       password=None,
                       system_generated_password=False):
        """Adds a local user to this commcell

            Args:
                user_name                     (str)     --  name of the user to be created

                full_name                     (str)     --  full name of the user to be created

                email                         (str)     --  email of the user to be created

                password                      (str)     --  password of the user to be created
                    default: None

                system_generated_password     (bool)    --  if set to true system defined
                                                                password will be used
                    default: False

            Raises:
                SDKException:
                    if data type of input is invalid

                    if user with specified name already exists

                    if password or system_generated_password are not set

                    if failed to add user to commcell
        """
        if not (isinstance(user_name, basestring) and
                isinstance(full_name, basestring) and
                isinstance(email, basestring)):
            raise SDKException('User', '101')

        if self.has_user(user_name):
            raise SDKException(
                'User', '102', "User {0} already exists on this commcell.".format(user_name)
            )

        if password is None and system_generated_password is False:
            raise SDKException(
                'User',
                '102',
                'Both password and system_generated_password are not set.'
                'Please specify password or mark system_generated_password as true')

        if password is not None:
            password = b64encode(password.encode()).decode()
        else:
            password = ''

        create_local_user_request = {
            "users": [{
                "password": password,
                "email": email,
                "fullName": full_name,
                "systemGeneratePassword": system_generated_password,
                "userEntity": {
                    "userName": user_name
                }
            }]
        }

        ADD_USER = self._commcell_object._services['USERS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', ADD_USER, create_local_user_request
        )

        error_code, error_message = self._process_add_or_delete_response(flag, response)

        if not error_message:
            error_message = 'Failed to add user. Please check logs for further details.'

        if error_code != 0:
            raise SDKException('User', '102', error_message)

        self._users = self._get_users()

        return self.get(user_name)

    def has_user(self, user_name):
        """Checks if any user with specified name exists on this commcell

        Args:
            user_name         (str)     --     name of the user which has to be checked if exists

        Raises:
            SDKException:
                if data type of input is invalid
        """
        if not isinstance(user_name, basestring):
            raise SDKException('User', '101')

        return self._users and user_name.lower() in self._users

    def get(self, user_name):
        """Returns the user object for the specified user name

        Args:
            user_name  (str)  --  name of the user for which the object has to be created

        Raises:
            SDKException:
                if user doesn't exist with specified name
        """
        if not self.has_user(user_name):
            raise SDKException(
                'User', '102', "User {0} doesn't exists on this commcell.".format(user_name)
            )

        return User(self._commcell_object, user_name, self._users[user_name.lower()])

    def delete(self, user_name):
        """Deletes the specified user from the existing commcell users

        Args:
            user_name     (str)     --     name of the user which has to be deleted

        Raises:
            SDKException:
                if user doesn't exist

                if response is empty

                if response is not success

        """
        if not self.has_user(user_name):
            raise SDKException(
                'User', '102', "User {0} doesn't exists on this commcell.".format(user_name)
            )

        DELETE_USER = self._commcell_object._services['USER'] % (self._users[user_name.lower()])

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'DELETE', DELETE_USER
        )

        error_code, error_message = self._process_add_or_delete_response(flag, response)

        if not error_message:
            error_message = 'Failed to delete user. Please check logs for further details.'

        if error_code != 0:
            raise SDKException('User', '102', error_message)

        self._users = self._get_users()

    def refresh(self):
        """Refresh the list of Users on this commcell."""
        self._users = self._get_users()


class User(object):
    """Class for representing a particular user configured on this commcell"""

    def __init__(self, commcell_object, user_name, user_id=None):
        """Initialize the User class object for specified user

            Args:
                commcell_object (object)  --  instance of the Commcell class

                user_name         (str)     --  name of the user

                user_id           (str)     --  id of the user
                    default: None

        """
        self._commcell_object = commcell_object
        self._user_name = user_name.lower()

        if user_id is None:
            self._user_id = self._get_user_id(self._user_name)
        else:
            self._user_id = user_id

        self._USER = self._commcell_object._services['USER'] % (self._user_id)

        self._get_user_properties()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'User class instance for User: "{0}"'
        return representation_string.format(self.user_name)

    def _get_user_id(self, user_name):
        """Gets the user id associated with this user

            Args:
                user_name         (str)     --     name of the user whose

            Returns:
                int     -     id associated to the specified user
        """
        users = Users(self._commcell_object)
        return users.get(user_name).user_id

    def _get_user_properties(self):
        """Gets the properties of this user"""
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._USER
        )

        if flag:
            if response.json() and 'users' in response.json():
                self._properties = response.json()['users'][0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _update_user_props(self, properties_dict):
        """Updates the properties of this user

            Args:
                properties_dict (dict)  --  user property dict which is to be updated
                    e.g.: {
                            "description": "My description"
                        }

            Returns:
                Client Properties update dict
        """
        request_json = {
            "users": [{
                "userEntity": {
                    "userName": self.user_name
                }
            }]
        }

        request_json['users'][0].update(properties_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._USER, request_json
        )

        if flag:
            if response.json():
                error_code = -1
                error_message = ''
                if 'response' in response.json():
                    response_json = response.json()['response'][0]
                    error_code = response_json['errorCode']

                elif 'errorCode' in response.json():
                    error_code = response.json()['errorCode']
                    if 'errorMessage' in response:
                        error_message = response['errorMessage']

                return error_code, error_message

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _update_usergroup_request(self, request_type, usergroups_list=[]):
        """Updates the usergroups this user is associated to

        Args:
            usergroups_list     (list)     --     list of usergroups to be updated

            request_type         (str)     --     type of request to be done
        """
        update_usergroup_request = {
            "NONE": 0,
            "OVERWRITE": 1,
            "ADD": 2,
            "DELETE": 3,
            "CLEAR": 4
        }

        associated_usergroups = []

        for usergroup in usergroups_list:
            temp = {
                "userGroupName": usergroup
            }
            associated_usergroups.append(temp)

        update_usergroup_dict = {
            "associatedUserGroupsOperationType": update_usergroup_request[request_type.upper()],
            "associatedUserGroups": associated_usergroups
        }

        self._update_user_props(update_usergroup_dict)

    @property
    def user_name(self):
        """Returns the user name of this commcell user"""
        return self._user_name

    @property
    def user_id(self):
        """Returns the user id of this commcell user"""
        return self._user_id

    @property
    def description(self):
        """Returns the description associated with this commcell user"""
        return self._properties['description']

    @description.setter
    def description(self, value):
        """Sets the description for this commcell user"""
        props_dict = {
            "description": value
        }
        self._update_user_props(props_dict)

    @property
    def associated_usergroups(self):
        """Returns the list of associated usergroups"""
        associated_usergroups = []

        if 'associatedUserGroups' not in self._properties:
            return

        for user_group in self._properties['associatedUserGroups']:
            associated_usergroups.append(user_group['userGroupName'])

        return associated_usergroups

    def add_usergroups(self, usergroups_list):
        """Adds the specified usergroups to this commcell user

        Args:
            usergroups_list     (list)     --     list of usergroups to be added

        Raises:
            SDKException:
                if data type of input is invalid

                if failed to add usergroups
        """
        if not isinstance(usergroups_list, list):
            raise SDKException('USER', '101')

        self._update_usergroup_request('ADD', usergroups_list)

    def remove_usergroups(self, usergroups_list):
        """Removes the specified usergroups to this commcell user

        Args:
            usergroups_list     (list)     --     list of usergroups to be deleted

        Raises:
            SDKException:
                if data type of input is invalid

                if failed to delete usergroups
        """
        if not isinstance(usergroups_list, list):
            raise SDKException('USER', '101')

        self._update_usergroup_request('DELETE', usergroups_list)

    def overwrite_usergroups(self, usergroups_list):
        """Overwrites the specified usergroups to this commcell user

        Args:
            usergroups_list     (list)     --     list of usergroups to be overwritten

        Raises:
            SDKException:
                if data type of input is invalid

                if failed to overwrite usergroups
        """
        if not isinstance(usergroups_list, list):
            raise SDKException('USER', '101')

        self._update_usergroup_request('OVERWRITE', usergroups_list)

    def refresh(self):
        """Refresh the properties of the User."""
        self._get_user_properties()