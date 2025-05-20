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

"""Main file for managing users on this commcell

Users and User are only the two classes defined in this commcell

Users:
    __init__()                          --  initializes the users class object

    __str__()                           --  returns all the users associated with the
                                            commcell

    __repr__()                          --  returns the string for the instance of the
                                            Users class

    _get_users()                        --  gets all the users on this commcell

    _get_fl_parameters()                --  Returns the fl parameters to be passed in the mongodb caching api call

    _get_sort_parameters()              --  Returns the sort parameters to be passed in the mongodb caching api call

    _get_fq_parameters()                --  Returns the fq parameters based on the fq list passed

    get_users_cache()                   --  Gets all the users present in CommcellEntityCache DB.

    all_users_cache()                   --  Returns dict of all the users and their info present in CommcellEntityCache
                                            in mongoDB

    _process_add_or_delete_response()   --  process the add or delete users response

    add()                               --  adds local/external user to commcell

    has_user()                          --  checks if user with specified user exists
                                            on this commcell

    get()                               --  returns the user class object for the
                                            specified user name

    delete()                            --  deletes the user on this commcell

    refresh()                           --  refreshes the list of users on this
                                            commcell

    all_users()                         --  Returns all the users present in the commcell

    _get_users_on_service_commcell()    -- gets the users from service commcell

    all_users_prop()                    --  Returns complete GET API response

User
    __init__()                          --  initiaizes the user class object

    __repr__()                          --  returns the string for the instance of the
                                            User class

    _get_user_id()                      --  returns the user id associated with this
                                            user

    _get_user_properties()              --  gets all the properties associated with
                                            this user

    _update_user_props()                --  updates the properties associated with
                                            this user

    _update_usergroup_request()         --  makes the request to update usergroups
                                            associated with this user

    user_name()                         --  returns the name of this user

    user_id()                           --  returns the id of this user

    description()                       --  returns the description of this user

    email()                             --  returns the email of this user

    upn()                               --  Returns user principal name of the user

    number_of_laptops()                 --  Returns number of devices for the user

    associated_usergroups()             --  returns the usergroups associated with
                                            this user

    associated_external_usergroups()    -- returns the external usergroups associated with this user

    add_usergroups()                    --  associates the usergroups with this user

    remove_usergroups()                 --  disassociated the usergroups with this user

    overwrite_usergroups()              --  reassociates the usergroups with this user

    refresh()                           --  refreshes the properties of this user

    update_security_associations()      --  updates 3-way security associations on user

    request_OTP()                       --  fetches OTP for user

    user_security_associations()        --  returns sorted roles and custom roles present on the
                                            different entities.

    status()                            --  returns the status of user

    update_user_password()              --  Updates new passwords of user

    user_guid()                         --  returns user GUID

    age_password_days()                 --  returns age password days for user

    user_company_name()                 -- returns company name if user is a company user else returns empty str

    get_account_lock_info()             -- returns account lock information

    unlock()                            --  Unlocks user account

    reset_tenant_password()             --  resets password of a tenant admin using token received in email
"""

from base64 import b64encode
from .security_association import SecurityAssociation
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
        self._users = None
        self._users_cache = None
        self._users_on_service = None
        self._all_users_prop = None
        self.filter_query_count = 0
        self.refresh()

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
            self._commcell_object.commserv_name
        )

    def _get_users(self, full_response: bool = False):
        """Returns the list of users configured on this commcell

            Args:
                full_response(bool) --  flag to return complete response

            Returns:
                dict of all the users on this commcell
                    {
                        'user_name_1': user_id_1
                    }

        """
        get_all_user_service = self._commcell_object._services['USERS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', get_all_user_service
        )

        if flag:
            if response.json() and 'users' in response.json():
                if full_response:
                    return response.json()
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

    def _get_fl_parameters(self, fl: list = None) -> str:
        """
        Returns the fl parameters to be passed in the mongodb caching api call

        Args:
            fl    (list)  --   list of columns to be passed in API request

        Returns:
            fl_parameters(str) -- fl parameter string
        """
        self.valid_columns = {
            'userName': 'users.userEntity.userName',
            'userId': 'users.userEntity.userId',
            'email': 'users.email',
            'fullName': 'users.fullName',
            'description': 'users.description',
            'UPN': 'users.UPN',
            'enableUser': 'users.enableUser',
            'isAccountLocked': 'users.isAccountLocked',
            'numDevices': 'users.numDevices',
            'company': 'users.userEntity.entityInfo.companyName',
            'lastLogIntime': 'users.lastLogIntime',
            'commcell': 'users.userEntity.entityInfo.multiCommcellName'
        }
        default_columns = 'users.userEntity'

        if fl:
            if all(col in self.valid_columns for col in fl):
                fl_parameters = f"&fl={default_columns},{','.join(self.valid_columns[column] for column in fl)}"
            else:
                raise SDKException('User', '102', 'Invalid column name passed')
        else:
            fl_parameters = f"&fl={default_columns},{','.join(column for column in self.valid_columns.values())}"

        return fl_parameters

    def _get_sort_parameters(self, sort: list = None) -> str:
        """
        Returns the sort parameters to be passed in the mongodb caching api call

        Args:
            sort  (list)  --   contains the name of the column on which sorting will be performed and type of sort
                                valid sor type -- 1 for ascending and -1 for descending
                                e.g. sort = ['connectName','1']

        Returns:
            sort_parameters(str) -- sort parameter string
        """
        sort_type = str(sort[1])
        col = sort[0]
        if col in self.valid_columns.keys() and sort_type in ['1', '-1']:
            sort_parameter = '&sort=' + self.valid_columns[col] + ':' + sort_type
        else:
            raise SDKException('User', '102', 'Invalid column name passed')
        return sort_parameter

    def _get_fq_parameters(self, fq: list = None) -> str:
        """
        Returns the fq parameters based on the fq list passed
        Args:
             fq     (list) --   contains the columnName, condition and value
                    e.g. fq = [['UserName','contains', 'test'],['email','contains', 'test']]

        Returns:
            fq_parameters(str) -- fq parameter string
        """
        conditions = {"contains", "notContain", "eq", "neq", "gt", "lt"}
        params = []

        for column, condition, *value in fq or []:
            if column not in self.valid_columns:
                raise SDKException('User', '102', 'Invalid column name passed')

            if condition in conditions:
                params.append(f"&fq={self.valid_columns[column]}:{condition.lower()}:{value[0]}")
            elif condition == "isEmpty" and not value:
                params.append(f"&fq={self.valid_columns[column]}:in:null,")
            elif condition.lower() == "between" and value and "-" in value[0]:
                start, end = value[0].split("-", 1)
                params.append(f"&fq={self.valid_columns[column]}:gteq:{start}")
                params.append(f"&fq={self.valid_columns[column]}:lteq:{end}")
            else:
                raise SDKException('User', '102', 'Invalid condition passed')

        return "".join(params)

    def get_users_cache(self, hard: bool = False, **kwargs) -> dict:
        """
        Gets all the users present in CommcellEntityCache DB.

        Args:
            hard  (bool)        --   Flag to perform hard refresh on users cache.
            **kwargs (dict):
                fl (list)       --   List of columns to return in response (default: None).
                sort (list)     --   Contains the name of the column on which sorting will be performed and type of sort.
                                        Valid sort type: 1 for ascending and -1 for descending
                                        e.g. sort = ['columnName', '1'] (default: None).
                limit (list)    --   Contains the start and limit parameter value.
                                        Default ['0', '100'].
                search (str)    --   Contains the string to search in the commcell entity cache (default: None).
                fq (list)       --   Contains the columnName, condition and value.
                                        e.g. fq = [['UserName', 'contains', 'test'],
                                         ['email', 'contains', 'test']] (default: None).

        Returns:
            dict: Dictionary of all the properties present in response.
        """
        # computing params
        fl_parameters = self._get_fl_parameters(kwargs.get('fl', None))
        fq_parameters = self._get_fq_parameters(kwargs.get('fq', None))
        limit = kwargs.get('limit', None)
        limit_parameters = f'start={limit[0]}&limit={limit[1]}' if limit else ''
        hard_refresh = '&hardRefresh=true' if hard else ''
        sort_parameters = self._get_sort_parameters(kwargs.get('sort', None)) if kwargs.get('sort', None) else ''

        # Search operation can only be performed on limited columns, so filtering out the columns on which search works
        searchable_columns = ["userName","email","fullName","company","description"]
        search_parameter = (f'&search={",".join(self.valid_columns[col] for col in searchable_columns)}:contains:'
                            f'{kwargs.get("search", None)}') if kwargs.get('search', None) else ''

        params = [
            limit_parameters,
            sort_parameters,
            fl_parameters,
            hard_refresh,
            search_parameter,
            fq_parameters
        ]

        request_url = f"{self._commcell_object._services['USERS']}?" + "".join(params)
        flag, response = self._commcell_object._cvpysdk_object.make_request("GET", request_url)

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        users_cache = {}
        if response.json() and 'users' in response.json():
            self.filter_query_count = response.json().get('filterQueryCount',0)
            for user in response.json()['users']:
                name = user.get('userEntity', {}).get('userName')
                users_config = {
                    'userName': name,
                    'userId': user.get('userEntity', {}).get('userId'),
                    'email': user.get('email'),
                    'fullName': user.get('fullName'),
                    'description': user.get('description',''),
                    'UPN': user.get('UPN'),
                    'enableUser': user.get('enableUser'),
                    'isAccountLocked': user.get('isAccountLocked'),
                    'numDevices': user.get('numDevices'),
                    'company': user.get('userEntity', {}).get('entityInfo', {}).get('companyName'),
                    'lastLogIntime': user.get('lastLogIntime')
                }
                if self._commcell_object.is_global_scope():
                    users_config['commcell'] = user.get('userEntity', {}).get('entityInfo', {}).get('multiCommcellName')

                    # Handle duplicate names for different commcells
                    unique_name = name
                    i = 1
                    while unique_name in users_cache:
                        existing_user = users_cache[unique_name]
                        if existing_user.get('commcell') != users_config.get('commcell'):
                            unique_name = f"{name}__{i}"
                            i += 1
                        else:
                            break
                    users_cache[unique_name] = users_config
                else:
                    users_cache[name] = users_config

            return users_cache
        else:
            raise SDKException('Response', '102')

    @property
    def all_users_cache(self) -> dict:
        """Returns dict of all the users and their info present in CommcellEntityCache in mongoDB

            dict - consists of all users of the in the CommcellEntityCache
                    {
                         "user1_name": {
                                'id': user1_id ,
                                'email': user1_email,
                                'fullName': user1_fullName,
                                'description': user1_description,
                                'UPN': user1_UPN,
                                'enabled': user1_enabled_user_flag,
                                'locked': user1_is_user_locked_flag,
                                'numberOfLaptops': user1_number_of_devices,
                                'company': user1_company
                                },
                         "user2_name": {
                                'id': user2_id ,
                                'email': user2_email,
                                'fullName': user2_fullName,
                                'description': user2_description,
                                'UPN': user2_UPN,
                                'enabled': user2_enabled_user_flag,
                                'locked': user2_is_user_locked_flag,
                                'numberOfLaptops': user2_number_of_devices,
                                'company': user2_company
                                }
                    }
        """
        if not self._users_cache:
            self._users_cache = self.get_users_cache()
        return self._users_cache

    def _process_add_or_delete_response(self, flag, response):
        """Processes the flag and response received from the server during add delete request

            Args:
                request_object  (object)  --  request objects specifying the details
                                              to request

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
                    if 'errorString' in response_json:
                        error_message = response_json['errorString']
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

    def _add_user(self, create_user_request):
        """Makes the add user request on the server

            Args:
                create_user_request     (dict)  --  request json to create an user

            Raises:
                SDKException:
                    if failed to add user
        """
        add_user = self._commcell_object._services['USERS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', add_user, create_user_request
        )
        error_code, error_message = self._process_add_or_delete_response(flag, response)

        if not error_message:
            error_message = 'Failed to add user. Please check logs for further details.'

        if error_code != 0:
            raise SDKException('User', '102', error_message)

        self._users = self._get_users()

        return response.json()

    def add(self,
            user_name,
            email,
            full_name=None,
            domain=None,
            password=None,
            system_generated_password=False,
            local_usergroups=None,
            entity_dictionary=None):
        """Adds a local/external user to this commcell

            Args:
                user_name                     (str)     --  name of the user to be
                                                            created

                full_name                     (str)     --  full name of the user to be
                                                            created

                email                         (str)     --  email of the user to be
                                                            created

                domain                        (str)     --  Needed in case you are adding
                                                            external user

                password                      (str)     --  password of the user to be
                                                            created
                    default: None

                local_usergroups              (list)     --  user can be member of
                                                            these user groups
                                                            Ex:1. ["master"],
                                                               2. ["group1", "group2"]

                system_generated_password     (bool)    --  if set to true system
                                                            defined password will be used
                                                            default: False

                entity_dictionary   --      combination of entity_type, entity names
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

                 role               --      key for role name you specify

                e.g.: {"clientName":"Linux1"}
                entity_type:    clientName, mediaAgentName, libraryName, userName,
                                userGroupName, storagePolicyName, clientGroupName,
                                schedulePolicyName, locationName, providerDomainName,
                                alertName, workflowName, policyName, roleName

                entity_name:    client name for entity_type 'clientName'
                                Media agent name for entitytype 'mediaAgentName'
                                similar for other entity_typees

            Raises:
                SDKException:
                    if data type of input is invalid

                    if user with specified name already exists

                    if password or system_generated_password are not set

                    if failed to add user to commcell
        """
        if domain:
            username = "{0}\\{1}".format(domain, user_name)
            password = ""
            system_generated_password = False
        else:
            username = user_name
            if not password:
                system_generated_password = True

        if not (isinstance(username, str) and
                isinstance(email, str)):
            raise SDKException('User', '101')

        if self.has_user(username):
            raise SDKException('User', '103', 'User: {0}'.format(username))

        if password is not None:
            password = b64encode(password.encode()).decode()
        else:
            password = ''

        if local_usergroups:
            groups_json = [{"userGroupName": lname} for lname in local_usergroups]
        else:
            groups_json = [{}]

        security_json = {}
        if entity_dictionary:
            security_request = SecurityAssociation._security_association_json(
                entity_dictionary=entity_dictionary)
            security_json = {
                "associationsOperationType": "ADD",
                "associations": security_request
                }

        create_user_request = {
            "users": [{
                "password": password,
                "email": email,
                "fullName": full_name,
                "systemGeneratePassword": system_generated_password,
                "userEntity": {
                    "userName": username
                },
                "securityAssociations": security_json,
                "associatedUserGroups": groups_json
            }]
        }
        response_json = self._add_user(create_user_request)


        created_user_username = response_json.get("response", [{}])[0].get("entity", {}).get("userName")

        return self.get(created_user_username)

    def has_user(self, user_name):
        """Checks if any user with specified name exists on this commcell

            Args:
                user_name         (str)     --     name of the user which has to be
                                                   checked if exists

            Raises:
                SDKException:
                    if data type of input is invalid
        """
        if not isinstance(user_name, str):
            raise SDKException('User', '101')

        return self._users and user_name.lower() in self._users

    def get(self, user_name):
        """Returns the user object for the specified user name

            Args:
                user_name  (str)  --  name of the user for which the object has to be
                                      created

            Raises:
                SDKException:
                    if user doesn't exist with specified name
        """
        if not self.has_user(user_name):
            raise SDKException(
                'User', '102', "User {0} doesn't exists on this commcell.".format(
                    user_name)
            )

        return User(self._commcell_object, user_name, self._users[user_name.lower()])

    def delete(self, user_name, new_user=None, new_usergroup=None):
        """Deletes the specified user from the existing commcell users

            Args:
                user_name       (str)   --  name of the user which has to be deleted

                new_user        (str)   --  name of the target user, whom the ownership
                                            of entities should be transferred

                new_usergroup   (str)   --  name of the user group, whom the ownership
                                            of entities should be transferred

                Note: either user or usergroup  should be provided for ownership
                transfer not both.

            Raises:
                SDKException:
                    if user doesn't exist

                    if new user and new usergroup any of these is passed and these doesn't
                    exist on commcell

                    if both user and usergroup is passed for ownership transfer

                    if both user and usergroup is not passed for ownership transfer

                    if response is not success

        """
        if not self.has_user(user_name):
            raise SDKException(
                'User', '102', "User {0} doesn't exists on this commcell.".format(
                    user_name)
            )
        if new_user and new_usergroup:
            raise SDKException(
                'User', '102', "{0} and {1} both can not be set as owner!! "
                "please send either new_user or new_usergroup".format(new_user, new_usergroup)
            )
        else:
            if new_user:
                if not self.has_user(new_user):
                    raise SDKException(
                        'User', '102', "User {0} doesn't exists on this commcell.".format(
                            new_user)
                    )
                new_user_id = self._users[new_user.lower()]
                new_group_id = 0
            else:
                if new_usergroup:
                    if not self._commcell_object.user_groups.has_user_group(new_usergroup):
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

        delete_user = self._commcell_object._services['DELETE_USER'] %(
            self._users[user_name.lower()], new_user_id, new_group_id)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'DELETE', delete_user
        )
        error_code, error_message = self._process_add_or_delete_response(flag, response)
        if not error_message:
            error_message = 'Failed to delete user. Please check logs for further details.'
        if error_code != 0:
            raise SDKException('User', '102', error_message)
        self._users = self._get_users()

    def _get_users_on_service_commcell(self):
        """gets the userspace from service commcell

        Returns:
            list  - consisting of all users assciated with service commcell

                    ['user1', 'user2']
        Raises:
            SDKException:
                if response is empty

                if response is not success
        """

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services['GET_USERSPACE_SERVICE']
        )

        if flag:
            if response.json() and 'users' in response.json():
                users_space_dict = {}
                for user in response.json()['users']:
                    users_space_dict[user['userEntity']['userName']] = user
                return users_space_dict
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def service_commcell_users_space(self):
        """Returns the user space from service commcell

        list - consists of users space from service commcell
            ['user1','user2']
        """
        if self._users_on_service is None:
            self._users_on_service = self._get_users_on_service_commcell()
        return self._users_on_service

    def refresh(self, **kwargs):
        """
        Refresh the list of users on this commcell.

            Args:
                **kwargs (dict):
                    mongodb (bool)  -- Flag to fetch users cache from MongoDB (default: False).
                    hard (bool)     -- Flag to hard refresh MongoDB cache for this entity (default: False).
        """
        mongodb = kwargs.get('mongodb', False)
        hard = kwargs.get('hard', False)

        self._users = self._get_users()
        self._users_on_service = None
        if mongodb:
            self._users_cache = self.get_users_cache(hard=hard)

    @property
    def all_users(self):
        """Returns the dict of all the users on the commcell

        dict of all the users on commcell
                   {
                      'user_name_1': user_id_1
                   }
        """
        return self._users

    @property
    def all_users_prop(self)->list[dict]:
        """
        Returns complete GET API response
        """
        self._all_users_prop = self._get_users(full_response=True).get('users', [])
        return self._all_users_prop


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

        self._user = self._commcell_object._services['USER'] % (self._user_id)
        self._user_status = None
        self._email = None
        self._description = None
        self._associated_external_usergroups = None
        self._associated_usergroups = None
        self._properties = None
        self._tfa_status = None
        self._upn = None
        self._num_devices = None
        self._get_user_properties()
        self._get_tfa_status()

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
            'GET', self._user
        )

        if flag:
            if response.json() and 'users' in response.json():
                self._properties = response.json()['users'][0]
                self._security_properties = self._properties.get('securityAssociations', {}).get(
                    'associations', {})
                self._security_associations = SecurityAssociation.fetch_security_association(
                    security_dict=self._security_properties)
                if 'enableUser' in self._properties:
                    self._user_status = self._properties['enableUser']

                if 'email' in self._properties:
                    self._email = self._properties['email']

                if 'description' in self._properties:
                    self._description = self._properties['description']

                if 'associatedUserGroups' in self._properties:
                    self._associated_usergroups = self._properties['associatedUserGroups']

                if 'associatedExternalUserGroups' in self._properties:
                    self._associated_external_usergroups = self._properties['associatedExternalUserGroups']

                if 'UPN' in self._properties:
                    self._upn = self._properties.get('UPN')

                if 'numDevices' in self._properties:
                    self._num_devices = self._properties.get('numDevices')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _update_user_props(self, properties_dict, **kwargs):
        """Updates the properties of this user

            Args:
                properties_dict (dict)  --  user property dict which is to be updated
                    e.g.: {
                            "description": "My description"
                        }
                ** kwargs(dict)         --  Key value pairs for supported arguments
                Supported arguments values:
                    new_username (str)  -- New login name for the user
            Returns:
                User Properties update dict
            Raises:
                SDKException:
                    If invalid type arguments are passed
                    Response was not success.
                    Response was empty.
        """
        request_json = {
            "users": [{
                "userEntity": {
                    "userName": self.user_name
                }
            }]
        }
        new_username = kwargs.get("new_username", None)
        if new_username is not None:
            if not isinstance(new_username, str):
                raise SDKException("USER", "101")
            request_json["users"][0]["userEntity"]["userName"] = new_username
        request_json['users'][0].update(properties_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._user, request_json
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

    def _update_usergroup_request(self, request_type, usergroups_list=None):
        """Updates the usergroups this user is associated to

            Args:
                usergroups_list     (list)     --     list of usergroups to be updated

                request_type         (str)     --     type of request to be done

            Raises:
                SDKException:

                    if failed to update usergroups

                    if usergroup is not list

                    if usergroup doesn't exixt on this commcell

        """
        update_usergroup_request = {
            "NONE": 0,
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3,
        }

        if not isinstance(usergroups_list, list):
            raise SDKException('USER', '101')

        for usergroup in usergroups_list:
            if not self._commcell_object.user_groups.has_user_group(usergroup):
                raise SDKException(
                    'UserGroup', '102', "UserGroup {0} doesn't "
                    "exists on this commcell".format(usergroup)
                )

        associated_usergroups = []
        if usergroups_list:
            for usergroup in usergroups_list:
                temp = {
                    "userGroupName": usergroup
                }
                associated_usergroups.append(temp)

        update_usergroup_dict = {
            "associatedUserGroupsOperationType": update_usergroup_request[
                request_type.upper()],
            "associatedUserGroups": associated_usergroups
        }

        self._update_user_props(update_usergroup_dict)

    @property
    def name(self):
        """Returns the User display name"""
        return self._properties['userEntity']['userName']

    @property
    def full_name(self):
        """Returns the full name of this commcell user"""
        return self._properties.get('fullName','')

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
        return self._description

    @property
    def email(self):
        """Returns the email associated with this commcell user"""
        return self._email

    @property
    def upn(self) -> str:
        """
        Returns user principal name of the user

        Returns:
            str -- upn of the user
        """
        return self._upn

    @property
    def number_of_laptops(self) -> int:
        """
        Returns number of devices for the user

        Returns:
            int --  number of devices
        """
        return self._num_devices

    @user_name.setter
    def user_name(self, value):
        """Sets the new username for this commcell user"""
        self._update_user_props("", new_username=value)

    @email.setter
    def email(self, value):
        """""Sets the description for this commcell user"""
        props_dict = {
            "email": value
        }
        self._update_user_props(props_dict)

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
        usergroups = []
        if self._associated_usergroups is not None:
            for usergroup in self._associated_usergroups:
                usergroups.append(usergroup['userGroupName'])
        return usergroups

    @property
    def associated_external_usergroups(self):
        """Returns the list of associated external usergroups"""
        usergroups = []
        if self._associated_external_usergroups is not None:
            for usergroup in self._associated_external_usergroups:
                usergroups.append(usergroup['externalGroupName'])
        return usergroups

    @property
    def user_security_associations(self):
        """Returns security associations from properties of the User."""
        return self._security_associations

    @property
    def status(self):
        """Returns the status of this commcell user"""
        return self._user_status

    @status.setter
    def status(self, value):
        """Sets the status for this commcell user"""
        request_json = {
            "users":[{
                "enableUser": value
            }]
        }
        usergroup_request = self._commcell_object._services['USER']%(self._user_id)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', usergroup_request, request_json
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

    @property
    def user_guid(self):
        """
        returns user guid
        """
        return self._properties.get('userEntity', {}).get('userGUID')

    @property
    def age_password_days(self):
        """
        returns age password days
        """
        return self._properties.get('agePasswordDays')

    @property
    def user_company_name(self):
        """
        returns user associated company name
        """
        return self._properties.get('companyName', '').lower()

    @age_password_days.setter
    def age_password_days(self, days):
        """
        sets the age password days

        Args:
            days    (int) -- number of days password needs to be required
        """
        if isinstance(days, int):
            props_dict = {
                "agePasswordDays": days
            }
            self._update_user_props(props_dict)
        else:
            raise SDKException('User', '101')

    def update_user_password(self, new_password, logged_in_user_password):
        """updates new passwords of user

            Args:
                new_password            (str)   --  new password for user

                logged_in_user_password (str)   --  password of logged-in user(User who is changing
                                                    the password) for validation.
        """
        password = b64encode(new_password.encode()).decode()
        validation_password = b64encode(logged_in_user_password.encode()).decode()
        props_dict = {
            "password": password,
            "validationParameters":{
                "password": validation_password,
                "passwordOperationType": 2
            }
        }
        self._update_user_props(props_dict)

    def add_usergroups(self, usergroups_list):
        """UPDATE the specified usergroups to this commcell user

            Args:
                usergroups_list     (list)  --     list of usergroups to be added
        """
        self._update_usergroup_request('UPDATE', usergroups_list)

    def remove_usergroups(self, usergroups_list):
        """DELETE the specified usergroups to this commcell user

            Args:
                usergroups_list     (list)  --     list of usergroups to be deleted
        """
        self._update_usergroup_request('DELETE', usergroups_list)

    def overwrite_usergroups(self, usergroups_list):
        """OVERWRITE the specified usergroups to this commcell user

            Args:
                usergroups_list     (list)  --     list of usergroups to be overwritten

        """
        self._update_usergroup_request('OVERWRITE', usergroups_list)

    def refresh(self):
        """Refresh the properties of the User."""
        self._get_user_properties()
        self._get_tfa_status()

    def update_security_associations(self, entity_dictionary, request_type):
        """handles three way associations (role-user-entities)

            Args:
                entity_dictionary   --      combination of entity_type, entity names
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

                request_type        --      decides whether to ADD, DELETE or
                                            OVERWRITE user security association.

            Raises:
                SDKException:

                    if response is not success
        """
        update_user_request = {
            "NONE": 0,
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3,
        }

        sec_request = {}
        if entity_dictionary:
            sec_request = SecurityAssociation._security_association_json(
                entity_dictionary=entity_dictionary)

        request_json = {
            "securityAssociations":{
                "associationsOperationType":update_user_request[request_type.upper()],
                "associations":sec_request
                }
        }
        self._update_user_props(request_json)

    def request_otp(self):
        """fetches OTP for user
        Returns:
            OTP generated for user
        Raises:
                Exception:
                    if response is not successful
        """

        if self._commcell_object.users.has_user(self.user_name):
            get_otp = self._commcell_object._services['OTP'] % (self.user_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', get_otp
        )
        if flag:
            if response.json():
                if 'value' in response.json():
                    return response.json()['value']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_tfa_status(self):
        """
        Gets the status of two factor authentication for this user
        """
        url = self._commcell_object._services['TFA_STATUS_OF_USER'] % self._user_name
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', url=url
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                if response.json().get('errorCode') != 0:
                    raise SDKException('User',
                                       '102',
                                       "Failed to get two factor authentication "
                                       "status. error={0}".format(response.json().get('errorMessage')))
            if response.json() and 'twoFactorInfo' in response.json():
                info = response.json().get('twoFactorInfo')
                self._tfa_status = info.get('isTwoFactorAuthenticationEnabled', False)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def is_tfa_enabled(self):
        """
        Returns the status of two factor authentication for this user

        bool    --  tfa status
        """
        return self._tfa_status

    @property
    def get_account_lock_info(self):
        """
        Returns user account lock status
        dict     --  account lock info
        example:
            {
                "isAccountLocked" : True,
                "lockStartTime" : 1646640752,
                "lockEndTime" : 1646727152
            }
        """
        lock_info = dict()
        lock_info['isAccountLocked'] = self._properties.get('isAccountLocked', False)
        lock_info['lockStartTime'] = self._properties.get('lockStartTime', 0)
        lock_info['lockEndTime'] = self._properties.get('lockEndTime', 0)
        return lock_info

    def unlock(self):
        """
        Unlocks user account.
        Returns:
            status      (str)   --      unlock operation status
                Example:-
                "Unlock successful for user account"
                "Logged in user cannot unlock their own account"
                "Unlock failed for user account"
                "User account is not locked"
                "Logged in user does not have rights to unlock this user account"
            statusCode
        Raises:
            SDKException:
                if response is empty
                if response is not success
        """
        payload = {"lockedAccounts": [{"user": {"userName": self._user_name, "userId": self._user_id}}]}
        service = self._commcell_object._services['UNLOCK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', service, payload
        )
        if flag:
            if response and response.json() and 'lockedAccounts' in response.json():
                return response.json().get('lockedAccounts')[0].get('status'), response.json().get('lockedAccounts')[0].get('statusCode')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def reset_tenant_password(self, token: str, password: str):
        """
        Method to reset the password of a tenant admin using a token received in an email.

        Args:
            token (str): The token received in the reset password email.
            password (str): The new password to set for the tenant admin.

        Returns:
            bool: True if the password reset is successful.

        Raises:
            SDKException: If there's an error with the response or the password reset fails.
                - 'User', '102' if there's an error code or error string in the response.
                - 'Response', '102' if the response is empty or has an invalid JSON format.
                - 'Response', '101' if the HTTP request fails.
        """
        headers = self._commcell_object._headers.copy()
        del headers['Authtoken']
        headers['Reset-Password-token'] = token
        payload = (f'<App_UpdateUserPropertiesRequest><processinginstructioninfo><formatFlags skipIdToNameConversion='
                   f'"1"/></processinginstructioninfo><users removeOtherActiveSessions="1" password = "{password}">'
                   f'<userEntity userId="{str(self.user_id)}" /><validationParameters passwordOperationType="1" '
                   f'password="{password}"/></users></App_UpdateUserPropertiesRequest>')
        service = self._commcell_object._services['RESET_TENANT_PASSWORD']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', service, payload, headers=headers
        )
        if flag:
            if response and response.json():
                response_data = response.json()
                error_code = response_data['response'][0].get('errorCode', -1)
                error_string = response_data['response'][0].get('errorString', '')

                # Check if there's an error
                if error_code != 0 or error_string:
                    raise SDKException('User', '102', f'Error Code:'
                                                      f'{error_code}, Error String: {error_string}')
                return True
            else:
                raise SDKException('Response', '102', 'Empty response or invalid JSON format.')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def create_access_token(self,
                            token_name,
                            token_type=None,
                            renewable_until_time=None,
                            token_expiry_time=None,
                            api_endpoints=None):
        """
        Creates v4 Access token for the given User
        Args:
            token_name   (str)   -- User friendly name for the Access token

            token_type   (int)   -- Scope for the Access token
                Expected values: 0: All Scope(Default)
                                 1: Microsoft SCIM
                                 2: All Scope
                                 3: Custom
                                 4: 1-Touch

            renewable_until_time (int) -- Unix time stamp for renewable until time applicable
            for Scopes ["All Scope", "custom"]. It will be ignored for other scopes.

            token_expiry_time (int) -- Unix time stamp for Token expiry time
            applicable for Scopes ["Microsoft SCIM", "1-Touch"]. It will be ignored for other scopes.

            api_endpoints (list) -- List of Commvault REST API to be considered in the custom scope
                Example-> ["/client", "/v4/servergroup"]

        Returns:
            dict - Containing Access token details
            Example response:
            For Microsoft SCIM and 1-Touch:
                {'accessTokenId': <token_ID>, 'tokenName': 'sample_token_name', 'accessToken': '<Access token>',
                 'userId': <logged-in-user-ID>, 'tokenExpiryTimestamp': Expiry time stamp}
            For All scope and custom scope:
                {'accessTokenId': <token_ID>, 'renewableUntilTimestamp': <renewable until time stamp>,
                'tokenName': 'sample_token_name', 'accessToken': '<Access token>', 'userId': 1,
                'refreshTokenExpiryTimestamp': <refresh token expiry time>,
                'tokenExpiryTimestamp': <token expiry time>, 'refreshToken': '<refresh token>'}
        """
        payload = {
                "tokenName": token_name
        }
        if token_type:
            payload["tokenType"] = token_type

        if renewable_until_time:
            payload["renewableUntilTimestamp"] = renewable_until_time

        if token_expiry_time:
            payload["tokenExpiryTimestamp"] = token_expiry_time

        if api_endpoints:
            payload["apiEndpoints"] = api_endpoints

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CREATE_ACCESS_TOKEN'], payload
        )
        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']
                if error_code != 0:
                    error_string = response.json()['error'].get('errorMessage')
                    raise SDKException('User', '104', error_string)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()["tokenInfo"]

    def edit_access_token(self,
                          access_token_id,
                          token_name=None,
                          token_type=None,
                          renewable_until_time=None,
                          token_expiry_time=None,
                          api_endpoints=None):
        """
        update v4 Access token for the given token ID
        Args:
            access_token_id (int) -- Access token ID received in the create request

            token_name   (str)   -- User friendly name for the Access token

            token_type   (int)   -- Scope for the Access token
                Expected values: 0: All Scope(Default)
                                 1: Microsoft SCIM
                                 2: All Scope
                                 3: Custom
                                 4: 1-Touch

            renewable_until_time (int) -- Unix time stamp for renewable until time applicable
            for Scopes ["All Scope", "custom"]. It will be ignored for other scopes.

            token_expiry_time (int) -- Unix time stamp for Token expiry time
            applicable for Scopes ["Microsoft SCIM", "1-Touch"]. It will be ignored for other scopes.

            api_endpoints (list) -- List of Commvault REST API to be considered in the custom scope
                Example-> ["/client", "/v4/servergroup"]

        Returns:
            dict - Containing updated Access token details
        """

        if not any([token_name, renewable_until_time, token_expiry_time, api_endpoints]):
            if token_type is None:
                raise SDKException('User', '105', "At least one input is required for update token operation")

        payload = {}
        if token_name:
            payload["tokenName"] = token_name

        if token_type:
            payload["tokenType"] = token_type

        if renewable_until_time:
            payload["renewableUntilTimestamp"] = renewable_until_time

        if token_expiry_time:
            payload["tokenExpiryTimestamp"] = token_expiry_time

        if api_endpoints:
            payload["apiEndpoints"] = api_endpoints

        update_token_api_url = self._commcell_object._services['UPDATE_ACCESS_TOKEN'] % access_token_id
        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', update_token_api_url, payload)
        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']
                if error_code != 0:
                    error_string = response.json()['error'].get('errorMessage')
                    raise SDKException('User', '106', error_string)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()["tokenInfo"]

    def delete_access_token(self, access_token_id):
        """
        delete v4 Access token for the given token ID
        Args:
            access_token_id (int) -- Access token ID received in the create request

        Returns:
            dict - Containing error message and error code.
        """
        revoke_token_api_url = self._commcell_object._services['REVOKE_ACCESS_TOKEN'] % access_token_id
        flag, response = self._commcell_object._cvpysdk_object.make_request('DELETE', revoke_token_api_url)
        if flag:
            if response.json():
                error_code = response.json()['errorCode']
                if error_code != 0:
                    error_string = response.json().get('errorMessage')
                    raise SDKException('User', '107', error_string)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()

    def get_access_tokens(self):
        """
        get v4 Access token for the current user
        Args:
        Returns:
            dict - Containing List of all Access tokens available for the current user.
        """
        get_tokens_api_url = self._commcell_object._services['GET_ACCESS_TOKENS'] % self.user_id
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', get_tokens_api_url)
        if flag:
            if response.json():
                error_code = response.json().get('errorCode')
                if error_code and error_code != 0:
                    error_string = response.json().get('errorMessage')
                    raise SDKException('User', '108', error_string)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()

    def renew_access_token(self, access_token, refresh_token):
        """
        Renew Access token
        Args:
            access_token    (str)  -- Access token received in create request
            refresh_token   (str)  -- refresh token received in create request
        Returns:
            dict - Containing details of renewed Access token.
        """
        renew_token_api_url = self._commcell_object._services['RENEW_TOKEN']
        payload = {
            "accessToken" : access_token,
            "refreshToken" : refresh_token
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', renew_token_api_url, payload)
        if flag:
            if response.json():
                error_code = response.json().get('errorCode')
                if error_code and error_code != 0:
                    error_string = response.json().get('errorMessage')
                    raise SDKException('User', '109', error_string)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()


