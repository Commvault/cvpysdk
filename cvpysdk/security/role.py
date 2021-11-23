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

"""Main file for managing roles on this commcell

Roles and Role are only the two classes defined in this commcell

Roles
    __init__()              --  initializes the Roles class object

    __str__()               --  returns all the Roles associated
                                with the commcell

    __repr__()              --  returns the string for the
                                instance of the Roles class

    _get_roles()            --  gets all the roles on this commcell

    has_role()              --  checks if role with specified role exists
                                on this commcell

    add()                   --  craetes the role on this commcell

    get()                   --  returns the role class object for the
                                specified role name

    delete()                --  deletes the role on this commcell

    refresh()               --  refreshes the list of roles on this commcell

Role
    __init__()              --  initiaizes the role class object

    __repr__()              --  returns the string for the instance of the
                                role class

    _get_role_id()          --  returns the role id associated with this role

    _get_role_properties()  --  gets all the properties associated with this role

    role_name()             --  returns the name of this role

    role_id()               --  returns the id of this role

    company_name()          --  returns the company name of this role

    role_description()      --  returns the description of this role

    status()                --  returns the status of this role

    refresh()               --  refreshes the properties of this role

    _update_role_props()    --  Updates properties of existing roles

    associate_user()        --  sharing role to user with valid permissions who can
                                manage this role.

    associate_usergroup()   --  sharing role to user group with valid permissions who
                                can manage this role

    modify_capability()     --  modifying permissions of the role

"""

from past.builtins import basestring
from ..exception import SDKException

class Roles(object):
    """Class for maintaining all the configured role on this commcell"""

    def __init__(self, commcell_object):
        """Initializes the roles class object for this commcell

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Clients class
        """
        self._commcell_object = commcell_object
        self._roles = self._get_roles()

    def __str__(self):
        """Representation string consisting of all roles of the commcell.

            Returns:
                str - string of all the roles configured on the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Roles')

        for index, role in enumerate(self._roles):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, role)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Roles class."""
        return "Roles class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_roles(self):
        """Returns the list of roles configured on this commcell"""
        get_all_roles_service = self._commcell_object._services['ROLES']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', get_all_roles_service
        )

        if flag:
            if response.json() and 'roleProperties' in response.json():
                roles_dict = {}

                for role in response.json()['roleProperties']:
                    temp_id = role['role']['roleId']
                    temp_name = role['role']['roleName'].lower()
                    roles_dict[temp_name] = temp_id

                return roles_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_role(self, role_name):
        """Checks if any role with specified name exists on this commcell

            Args:
                role_name         (str)     --      name of the role which has to be
                                                    checked if exists

            Retruns:
                Bool- True if specified role is presnt on th ecommcell else false

            Raises:
                SDKException:
                    if data type of input is invalid
        """
        if not isinstance(role_name, basestring):
            raise SDKException('Role', '101')

        return self._roles and role_name.lower() in self._roles

    def add(self, rolename, permission_list="", categoryname_list=""):
        """creates new role

             Args:
                 role Name          --  Name of the role to be created
                 category Name list --  role will be created with all the permissions
                                    associated with this category
                    e.g.: category Name=Client :role will have all permisisons from
                                        this category.
                    e.g.: category Name=Client Group :role will have all permissions
                                        from this category
                    e.g.: category Name=commcell :role will have all permissions from
                                        this category
                 permission_list (array)  --  permission array which is to be updated
                     e.g.: permisison_list=["View", "Agent Management", "Browse"]
             Returns:
                 Role Properties update dict
                             Raises:
            SDKException:
                    if data type of input is invalid

                    if role already exists on the commcell

         """
        if permission_list == "" and categoryname_list == "":
            raise SDKException('Role', '102', "empty role can not be created!!  "
                                              "either permission_list or categoryname_list "
                                              "should have some value! ")
        if not isinstance(rolename, basestring):
            raise SDKException('Role', '101')
        if self.has_role(rolename):
            raise SDKException('Role', '102',
                               "Role {0} already exists on this commcell.".format(rolename))

        if permission_list:
            arr = [{"permissionName": permission} for permission in permission_list]
        else:
            arr = []
        if categoryname_list:
            for catname in categoryname_list:
                cat_blob = {"categoryName":catname}
                arr.append(cat_blob)

        request_json = {
            "roles": [{
                "role": {
                    "roleName": rolename
                },
                "categoryPermission": {
                    "categoriesPermissionOperationType": "ADD",
                    "categoriesPermissionList": arr
                }
            }]
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['ROLES'], request_json
        )
        if flag:
            if response.json():
                error_code = -1
                error_message = ''
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
        return self.get(rolename)

    def get(self, role_name):
        """Returns the role object for the specified role name

            Args:
                role_name  (str)    --  name of the role for which the object has to
                                        be created

            Raises:
                SDKException:
                    if role doesn't exist with specified name
        """
        if not self.has_role(role_name):
            raise SDKException(
                'Role', '102', "Role {0} doesn't exists on this commcell.".format(role_name)
            )

        return Role(self._commcell_object, role_name, self._roles[role_name.lower()])

    def delete(self, role_name):
        """Deletes the role object for specified role name

            Args:
                role_name (str) --  name of the role for which the object has to be
                                    deleted

            Raises:
                SDKException:
                    if role doesn't exist

                    if response is empty

                    if response is not success

        """
        if not self.has_role(role_name):
            raise SDKException(
                'Role', '102', "Role {0} doesn't exists on this commcell.".format(role_name)
            )

        delete_role = self._commcell_object._services['ROLE'] % (self._roles[role_name.lower()])

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'DELETE', delete_role
        )

        if flag:
            if response.json():
                error_code = -1
                error_message = ''
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

    def refresh(self):
        """Refresh the list of Roles on this commcell."""
        self._roles = self._get_roles()

    @property
    def all_roles(self):
        """"Returns all the roles present in the commcell"""
        return self._get_roles()

class Role(object):
    """"Class for representing a particular role configured on this commcell"""

    def __init__(self, commcell_object, role_name, role_id=None):
        """Initialize the Role class object for specified role

            Args:
                commcell_object (object)  --  instance of the Commcell class

                role_name         (str)     --  name of the role

                role_id           (str)     --  id of the role
                    default: None

        """
        self._commcell_object = commcell_object
        self._role_name = role_name.lower()

        if role_id is None:
            self._role_id = self._get_role_id(self._role_name)
        else:
            self._role_id = role_id

        self._request_role = self._commcell_object._services['ROLE'] % (self._role_id)
        self._role_description = ''
        self._role_status = True
        self._security_associations = {}
        self._role_permissions = {}
        self._company_name = ''
        self._get_role_properties()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Role class instance for Role: "{0}"'
        return representation_string.format(self.role_name)

    def _get_role_id(self, role_name):
        """Gets the role id associated with this role.

            Returns:
                str - id associated with this role
        """
        roles = Roles(self._commcell_object)
        return roles.get(role_name).role_id

    def _get_role_properties(self):
        """Gets the properties of this role"""
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._request_role
        )

        if flag:
            if response.json() and 'roleProperties' in response.json():
                role_properties = response.json()['roleProperties'][0]

                self._role_description = role_properties.get('description')
                self._role_id = role_properties['role'].get('roleId')
                self._role_name = role_properties['role'].get('roleName')
                self._role_status = role_properties['role']['flags'].get('disabled')
                if 'entityInfo' in role_properties['role']: self._company_name = role_properties['role']['entityInfo'].get('companyName')
                category_list = []
                permission_list = []

                if 'categoryPermission' in role_properties:
                    for associations in role_properties['categoryPermission'].get(
                            'categoriesPermissionList', []):
                        if 'permissionName' in associations:
                            permission_list.append(associations['permissionName'])
                        else:
                            category_list.append(associations['categoryName'])

                self._role_permissions = {
                    'permission_list': permission_list,
                    'category_list': category_list
                }
                if 'securityAssociations' in role_properties:
                    for association in role_properties['securityAssociations'].get(
                            'associations', []):
                        user_or_group = association['userOrGroup'][0]
                        if 'userName' in user_or_group:
                            name = user_or_group['userName']
                        elif 'userGroupName' in user_or_group:
                            name = user_or_group['userGroupName']
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

    def _update_role_props(self, properties_dict, name_val=None):
        """Updates the properties of this role

            Args:
                properties_dict (dict)  --  role property dict which is to be updated
                    e.g.: {
                            "description": "My description"
                        }

            Returns:
                role Properties update dict

            Raises:
                SDKException:
                    if role doesn't exist

                    if response is empty

                    if response is not success
        """
        if name_val:
            request_json = {
                "roles": [{
                    "role": {
                        "roleName": name_val
                    }
                }]
            }
        else:
            request_json = {
                "roles": [{
                    "role": {
                        "roleName": self.role_name
                    }
                }]
            }

        if "description" in properties_dict:
            request_json['roles'][0].update(properties_dict)
        else:
            request_json['roles'][0]['role'].update(properties_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._request_role, request_json
        )
        if flag:
            if response.json():
                error_code = -1
                error_message = ''
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

    def associate_user(self, rolename, username):
        """Updates the user who can manage this role with the permission provided

            Args:
                role Name   --  Role given to user on this role object
                user Name   --  user name who can manage this role

            Raises:
                SDKException:
                    if role Name doesn't exist

                    if user Name doesn't exist

                    if response is not success
        """
        if not isinstance(username, basestring):
            raise SDKException('Role', '101')
        if not self._commcell_object.roles.has_role(rolename):
            raise SDKException(
                'Role', '102', "Role {0} doesn't exists on this commcell.".format(rolename)
            )
        if not self._commcell_object.users.has_user(username):
            raise SDKException(
                'User', '102', "User {0} doesn't exists on this commcell.".format(username)
            )

        request_json = {
            "roles":[{
                "securityAssociations":{
                    "associationsOperationType":2,
                    "associations":[
                        {
                            "userOrGroup":[
                                {
                                    "userName":username
                                }
                            ],
                            "properties":{
                                "role":{
                                    "roleName":rolename
                                }
                            }
                        }
                    ]
                }
            }]
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._request_role, request_json
        )
        if flag:
            if response.json():
                error_code = -1
                error_message = ''
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

    def associate_usergroup(self, rolename, usergroupname):
        """Updates the usergroup who can manage this role with the permission provided

            Args:
                role Name        --  Role given to user on this role object
                user Group Name   --  user name who can manage this role

            Raises:
                SDKException:
                    if role Name doesn't exist

                    if user Group Name doesn't exist

                    if response is not success
        """
        if not isinstance(usergroupname, basestring):
            raise SDKException('Role', '101')
        if not self._commcell_object.roles.has_role(rolename):
            raise SDKException(
                'User', '102', "Role {0} doesn't exists on this commcell.".format(rolename)
            )
        if not self._commcell_object.user_groups.has_user_group(usergroupname):
            raise SDKException(
                'UserGroup', '102', "UserGroup {0} doesn't exists on this commcell.".format(
                    usergroupname)
            )

        request_json = {
            "roles":[{
                "securityAssociations":{
                    "associationsOperationType":2,
                    "associations":[
                        {
                            "userOrGroup":[
                                {
                                    "userGroupName":usergroupname
                                }
                            ],
                            "properties":{
                                "role":{
                                    "roleName":rolename
                                }
                            }
                        }
                    ]
                }
            }]
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._request_role, request_json
        )

        if flag:
            if response.json():
                error_code = -1
                error_message = ''
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

    def modify_capability(self, request_type, permission_list="", categoryname_list=""):
        """Updates role capabilities

             Args:
                 request_type(str)      --  type of request to be done
                                            ADD, OVERWRITE, DELETE
                 category Name list     --  role will be created with all the
                                            permissions associated with this category
                    e.g.: category Name=Client :role will have all permisisons from
                                        this category.
                    e.g.: category Name=Client Group :role will have all permissions
                                        from this category
                    e.g.: category Name=commcell :role will have all permissions from
                                        this category
                 permission_list(list)  --  permission array which is to be updated
                     e.g.: permisison_list=["View", "Agent Management", "Browse"]
             Returns:
                 Role Properties update dict
                             Raises:
            SDKException:
                    if data type of input is invalid

                    if role already exists on the commcell

         """

        update_role_request = {
            "NONE": 0,
            "OVERWRITE": 1,
            "UPDATE": 2,
            "ADD":2,
            "DELETE": 3
        }
        if(permission_list == "" and categoryname_list == ""):
            raise SDKException('Role', '102', "Capabilties can not be modified!!  "
                                              "either permission_list or categoryname_list "
                                              "should have some value! ")
        capability_arr = []
        if permission_list:
            capability_arr = [{"permissionName": permission} for permission in permission_list]
        if categoryname_list:
            for catname in categoryname_list:
                cat_blob = {"categoryName":catname}
                capability_arr.append(cat_blob)

        request_json = {
            "roles": [{
                "role": {
                    "roleName": self.role_name
                },
                "categoryPermission": {
                    "categoriesPermissionOperationType" : update_role_request[request_type.upper()],
                    "categoriesPermissionList": capability_arr
                }
            }]
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._request_role, request_json
        )
        if flag:
            if response.json():
                error_code = -1
                error_message = ''
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

    @property
    def role_name(self):
        """Returns the role name of this commcell role"""
        return self._role_name

    @role_name.setter
    def role_name(self, val):
        """Sets the value for role_name with the parameter provided

        """
        self._update_role_props(properties_dict={}, name_val=val)


    @property
    def role_id(self):
        """Returns the role id of this commcell role"""
        return self._role_id

    @property
    def role_description(self):
        """Returns the role_desccription of this commcell role"""
        return self._role_description

    @property
    def company_name(self):
        """
        Returns:
            str  -  company name to which user group belongs to.
            str  -  empty string, if usergroup belongs to Commcell
        """
        return self._company_name

    @role_description.setter
    def role_description(self, value):
        """Sets the description for this commcell role"""
        props_dict = {
            "description": value
        }
        self._update_role_props(props_dict)

    @property
    def status(self):
        """Returns the role_status of this commcell role"""
        return self._role_status

    @status.setter
    def status(self, value):
        """Sets the description for this commcell role"""
        props_dict = {
            "flags": {
                "disabled": not value
            }
        }
        self._update_role_props(props_dict)

    @property
    def permissions(self):
        """Returns the permissions that are associated with role"""
        return self._role_permissions

    def refresh(self):
        """Refresh the properties of the Roles."""
        self._get_role_properties()
