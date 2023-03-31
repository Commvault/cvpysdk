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

"""Main file for managing credentials records on this commcell

Credentials and Credential are only the two classes defined in this commcell

Credentials:
    __init__()                  --  initializes the Credentials class object

    __str__()                   --  returns all the Credentials associated
                                    with the commcell

    __repr__()                  --  returns the string for the instance of the Credentials class

    _get_credentials()          --  Returns the list of Credentials configured on this commcell

    all_credentials()           --  Returns all the Credentials present in the commcell

    has_credential()            --  Checks if any Credentials with specified name exists on
                                    this commcell

    get()                       --  Returns the Credential object for the specified Credential name

    add()                       --  creates the credential record on this commcell

    owner_json()                --  returns json blob for setting user or usergroup as creator

    refresh()                   --  refreshes the list of credentials on this commcell

    delete()                    --  deletes the credential record on this commcell

    get_security_associations() --  Returns the security association dictionary for a given user or user group

    add_azure_cloud_creds()     --  Creates azure access key based credential on this commcell


Credential:
    __init__()                  --  initiaizes the credential class object

    __repr__()                  --  returns the string for the instance of the
                                    credential class

    _get_credential_id()        --  Gets the Credential id associated with this Credential

    credential_name             --  Returns the name of the credential record

    credential_id               --  Returns the id of the credential record

    credential_description      --  Returns the description set of credential record

    credential_user_name        --  Returns the user name set in the credential record

    update_user_credential      --  Sets the value for credential user name and password with
                                    the parameters provided

    credential_owner            --  Returns the creator of credential account

    update_credential_owner()   --  Updates creator of credential account.

    refresh()                   --  refreshes the properties of credential account

    _get_credential_properties()--  returns the properties of credential account

    _update_credential_props()  -- Updates credential account properties


"""

from base64 import b64encode
from .security.usergroup import UserGroups
from .exception import SDKException
from .constants import Credential_Type


class Credentials(object):
    """Class for maintaining all the configured credential on this commcell"""

    def __init__(self, commcell_object):
        """Initializes the credentials class object for this commcell

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Clients class
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._credentials = self._get_credentials()
        self.record_type = {
            'windows': 1,
            'Linux': 2
        }

    def __str__(self):
        """Representation string consisting of all Credentials of the commcell.

            Returns:
                str - string of all the Credentials configured on the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Credentials')

        for index, credentials in enumerate(self._credentials):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, credentials)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Credentials class."""
        return "Credentials class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_credentials(self):
        """Returns the Credentials configured on this commcell

        Raises:
            Exception if response is not success
        """
        get_all_credential_service = self._services['ALL_CREDENTIALS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', get_all_credential_service
        )

        if flag:
            credentials_dict = {}
            if response.json() and 'credentialRecordInfo' in response.json():

                for credential in response.json()['credentialRecordInfo']:
                    temp_id = credential['credentialRecord']['credentialId']
                    temp_name = credential['credentialRecord']['credentialName'].lower()
                    credentials_dict[temp_name] = temp_id

            return credentials_dict
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_credentials(self):
        """"Returns all the Credentials present in the commcell"""
        return self._credentials

    def has_credential(self, credential_name):
        """Checks if any Credentials with specified name exists on this commcell

            Args:
                credential_name         (str)     --    name of the Credential which has to be
                                                        checked if exists

            Retruns:
                Bool- True if specified Credential is present on the commcell else false

            Raises:
                SDKException:
                    if data type of input is invalid
        """
        if not isinstance(credential_name, str):
            raise SDKException('Credentials', '101')

        return self._credentials and credential_name.lower() in self._credentials

    def get(self, credential_name):
        """Returns the Credential object for the specified Credential name

            Args:
                credential_name  (str)    --  name of the Credential for which the object has to
                                              be created
            Raises:
                SDKException:
                    if Credential doesn't exist with specified name
        """
        if not self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} doesn't exists on this commcell.".format(
                    credential_name)
            )

        return Credential(self._commcell_object, credential_name, self._credentials[
            credential_name.lower()])

    def add(self, record_type, credential_name, user_name, user_password, owner, isuser=1, description=None):
        """Creates credential account on this commcell

            Args:
                record_type     (str)   -- type of credential record to be created (windows\linux)

                credential_name (str)   --  name to be given to credential account

                user_name       (str)   --  name of the user to be associated to this credential
                                            account

                user_password   (str)   --  password for user

                owner           (str)   --  owner who can manage the credential account

                isuser          (bool)  --  Decider, whener owner is user or usergroup
                                            isuser=1 for user, isuser=0 for usergroup

                description     (str)   --  description for credential account

            Raises:
                SDKException:
                    if credential account is already present on the commcell

                    if string format are not proper

                    if response is not successful

        """

        if not (isinstance(credential_name, str) and isinstance(user_name, str)):
            raise SDKException('User', '101')

        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "User {0} already exists on this commcell.".format(
                    credential_name)
            )
        password = b64encode(user_password.encode()).decode()

        creator = self.owner_json(owner=owner, isuser_flag=isuser)

        record = {
            "userName": user_name,
            "password": password
        }
        create_credential_account = {
            "credentialRecordInfo": [{
                "recordType": self.record_type[record_type.lower()],
                "description": description,
                "credentialRecord": {
                    "credentialName": credential_name
                },
                "record": record,
                "createAs": creator['createAs']
            }]
        }

        request = self._services['CREDENTIAL']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential_account
        )
        if flag:
            if response.json():
                response_json = response.json()['error']
                error_code = response_json['errorCode']
                error_message = response_json['errorMessage']
                if not error_code == 0:
                    raise SDKException('Response', '101', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    @staticmethod
    def owner_json(owner, isuser_flag):
        """returns json blob for setting owners
        Args:
            owner       (Str)   --  user or User Group Name

            isuser_flag (Str)   --  decider whether owner is user or usergroup
        """
        if isuser_flag == 1:
            creator = {
                "createAs": {
                    "user": {
                        "user": {
                            "userName": owner
                        }
                    }
                }
            }
        else:
            creator = {
                "createAs": {
                    "userGroup": {
                        "userGroupName": owner
                    }
                }
            }
        return creator

    def refresh(self):
        """Refresh the list of credential records on this commcell."""
        self._credentials = self._get_credentials()

    def delete(self, credential_name):
        """Deletes the credential object for specified credential name

            Args:
                credential_name (str) --  name of the credential for which the object has to be
                                          deleted

            Raises:
                SDKException:
                    if credential doesn't exist

                    if response is empty

                    if response is not success

        """
        if not self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "credential {0} doesn't exists on this commcell.".format(
                    credential_name)
            )

        delete_credential = self._services['DELETE_RECORD']

        request_json = {
            "credentialRecordInfo": [{
                "credentialRecord": {
                    "credentialName": credential_name
                }
            }]
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', delete_credential, request_json
        )
        if flag:
            if response.json():
                response_json = response.json()['error']
                error_code = response_json['errorCode']
                error_message = response_json['errorMessage']
                if not error_code == 0:
                    raise SDKException('Response', '101', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def get_security_associations(self, owner, is_user=False):
        """
        Returns the security association dictionary for a given user or user group
        Args:
            owner(str)          -   Owner of the user or user group
            is_user(bool)       -   True if the owner is a user
                                    False if the owner is a user group

        Returns:
            dict containing the security association
        """
        if is_user is True:
            userOrGroupInfo = {
                "entityTypeName": "USER_ENTITY",
                "userGroupName": owner,
                "userGroupId": int(self._commcell_object.users.get(owner).user_id)
            }
        else:
            userOrGroupInfo = {
                "entityTypeName": "USERGROUP_ENTITY",
                "userGroupName": owner,
                "userGroupId": int(self._commcell_object.user_groups.get(owner).user_group_id)
            }
        security_association = {
            "associationsOperationType": 1,
            "associations": [
                {
                    "userOrGroup": [
                        userOrGroupInfo
                    ],
                    "properties": {
                        "isCreatorAssociation": False,
                        "permissions": [
                            {
                                "permissionId": 218,
                                "_type_": 122,
                                "permissionName": "User Credential"
                            }
                        ]
                    }
                }
            ]
        }
        return security_association

    def add_azure_cloud_creds(self, credential_name, account_name, access_key_id, **kwargs):
        """Creates azure access key based credential on this commcell

            Args:

                credential_name (str)   --  name to be given to credential account

                account_name  (str)     --  name of the azure storage account

                access_key_id   (str)   --  access key for azure storage

                ** kwargs(dict)         --  Key value pairs for supported arguments

                Supported argument values:
                    owner(str)                  -   owner of the credentials
                    is_user(bool)               -   Represents whether owner passed is a user or user group
                                                    is_user=1 for user, is_user=0 for usergroup
                    description(str)            -   description of the credentials

            Raises:
                SDKException:
                    if arguments type is incorrect

                    if credential account is already present on the commcell

                    if string format are not proper

                    if response is not successful

        """
        owner = kwargs.get("owner", "")
        is_user = kwargs.get("is_user", True)
        description = kwargs.get("description", "")

        if not (isinstance(access_key_id, str) and isinstance(owner, str)
                and isinstance(is_user, bool) and isinstance(account_name, str)
                and isinstance(description, str) and isinstance(credential_name, str)):
            raise SDKException("Credential", "101")

        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} already exists on this commcell.".format(
                    credential_name)
            )

        creator = self.owner_json(owner=owner, isuser_flag=is_user)
        password = b64encode(access_key_id.encode()).decode()
        additional_information = {
            "azureCredInfo": {
                "authType": "AZURE_OAUTH_SHARED_SECRET",
                "endpoints": {
                    "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                    "storageEndpoint": "blob.core.windows.net",
                    "resourceManagerEndpoint": "https://management.azure.com/"
                }
            }
        }
        create_credential_account = {
            "credentialRecordInfo": [
                {
                    "credentialRecord": {
                        "credentialName": credential_name
                    },
                    "securityAssociations": self.get_security_associations(owner, is_user),
                    "createAs": creator["createAs"],
                    "record": {
                        "userName": account_name,
                        "password": password
                    },
                    "recordType": "MICROSOFT_AZURE",
                    "additionalInformation": additional_information,
                    "description": description
                }
            ]
        }

        request = self._services['CREDENTIAL']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential_account
        )
        if flag:
            if response.json():
                response_json = response.json()['error']
                error_code = response_json['errorCode']
                error_message = response_json['errorMessage']
                if not error_code == 0:
                    raise SDKException('Response', '101', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()


class Credential(object):
    """"Class for representing a particular Credential record on this commcell"""

    def __init__(self, commcell_object, credential_name, credential_id=None):
        """Initialize the Credential class object for specified Credential

            Args:
                commcell_object         (object)    --  instance of the Commcell class

                credential_name         (str)       --  name of the Credential

                credential_id           (str)       --  id of the credential
                    default: None

        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._credential_name = credential_name.lower()

        if credential_id is None:
            self._credential_id = self._get_credential_id(self._credential_name)
        else:
            self._credential_id = credential_id

        self._credential_description = None
        self._credential_user_name = None
        self._credential_owner_json = None
        self._credential_owner = None
        self._credential_properties = None
        self._credential_security_assoc = []
        self._record_type = None
        self._credential_password = ""
        self._record_types = {
            1: 'Windows',
            2: 'Linux'
        }
        self._get_credential_properties()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Credential class instance for Credential: "{0}"'
        return representation_string.format(self.credential_name)

    def _get_credential_id(self, name):
        """Gets the Credential id associated with this Credential.

            Args:
                name    (str)   --  credential account name

            Returns:
                str - id associated with this Credential
        """
        creds = Credentials(self._commcell_object)
        return creds.get(credential_name=name)._credential_id

    @property
    def credential_name(self):
        """Returns the name of the credential record"""
        return self._credential_name

    @credential_name.setter
    def credential_name(self, val):
        """Sets the value for credential record with the parameter provided

        """
        props_dict = {
            "credentialRecord": {
                "credentialId": self._credential_id,
                "credentialName": val
            }
        }
        self._update_credential_props(properties_dict=props_dict)

    @property
    def credential_id(self):
        """Returns the Credential id of this commcell Credential record"""
        return self._credential_id

    @property
    def credential_description(self):
        """Returns the Credential_desccription of this commcell Credential reord"""
        return self._credential_properties.get('description')

    @credential_description.setter
    def credential_description(self, value):
        """Sets the description for this commcell Credential record"""
        props_dict = {
            "description": value
        }
        self._update_credential_props(props_dict)

    @property
    def credential_security_properties(self):
        """Returns the Credential's security association"""
        return self._credential_security_assoc

    def update_securtiy(self, name, is_user=True):
        """Updates the security association for this commcell Credential record

        Args:
            name    (str)   -- User or UserGroupName
            is_user (bool)  -- Set False for UserGroup

        """

        props_dict = {
            "securityAssociations": {
                "associationsOperationType": 1,
                "associations": [{
                    "userOrGroup": [{
                        "_type_": 13 if is_user else 15,
                        "userName" if is_user else "userGroupName": name
                    }],
                    "properties": {
                        "isCreatorAssociation": False,
                        "permissions": [{
                            "permissionId": 218,
                            "_type_": 122,
                            "permissionName": "User Credential"
                        }]
                    }
                }],
                "ownerAssociations": {}
            }
        }

        return self._update_credential_props(props_dict)

    @property
    def credential_user_name(self):
        """Returns the Credential name of this commcell Credential record"""
        return self._credential_user_name

    def update_user_credential(self, uname, upassword):
        """Sets the value for credential user name and password with the parameters provided
            Args:
                uname   (str)   --  new user name

                upassword(str)  --  new password for user

        """
        creds_dict = {
            "record": {
                "userName": uname,
                "password": b64encode(upassword.encode()).decode()
            }
        }
        self._update_credential_props(properties_dict=creds_dict)

    @property
    def credential_owner(self):
        """Returns the Credential name of this commcell Credential"""
        return self._credential_owner

    @property
    def credential_record_type(self):
        """Returns the Credential name of this commcell Credential record"""
        return self._record_types[self._record_type]

    def update_credential_owner(self, val, isuser):
        """Sets the value for credential record owner with the parameter provided
            Args:
                val     (str)   --  name of user or usergroup

                isuser  (bool)  --  value decides whether owner is user or usergroup
                                    1 for user and 0 for usergroup
        """
        creator = Credentials.owner_json(owner=val, isuser_flag=isuser)
        self._update_credential_props(properties_dict=creator)

    def refresh(self):
        """Refresh the properties of the Credentials."""
        self._get_credential_properties()

    def _get_credential_properties(self):
        """Gets the properties of this Credential record"""
        property_request = self._services['ONE_CREDENTIAL'] % (
            self._credential_name)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', property_request
        )

        if flag:
            if response.json() and 'credentialRecordInfo' in response.json():
                json_resp = response.json()
                self._credential_properties = response.json()['credentialRecordInfo'][0]

                self._credential_id = self._credential_properties['credentialRecord'].get(
                    'credentialId')
                self._credential_name = self._credential_properties['credentialRecord'].get(
                    'credentialName')
                self._credential_user_name = self._credential_properties['record']['userName']
                self._record_type = self._credential_properties['recordType']
                self._credential_owner_json = self._credential_properties.get('createAs', {})
                if self._record_type != Credential_Type.MICROSOFT_AZURE.value: # Azure Storage Credentials
                    if "userGroup" in self._credential_owner_json:
                        cred_id = self._credential_owner_json.get('userGroup', {}).get('userGroupId')
                        urs = UserGroups(self._commcell_object)
                        all_groups = urs.all_user_groups
                        for group_name, group_id in all_groups.items():
                            if group_id == str(cred_id):
                                self._credential_owner = group_name
                    else:
                        self._credential_owner = self._credential_owner_json.get('user', {}).get(
                            'user').get('userName')
                        self._credential_owner_json = self._credential_owner_json.get('user')
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _update_credential_props(self, properties_dict):
        """Updates the properties of this credential

            Args:
                properties_dict (dict)  --  credential property dict which is to be updated
                    e.g.: {
                            "description": "My description"
                        }

            Returns:
                credential Properties update dict

            Raises:
                SDKException:
                    if credential doesn't exist

                    if response is empty

                    if response is not success
        """
        if "record" in properties_dict:
            self._credential_user_name = properties_dict['record']['userName']
            self._credential_password = properties_dict.get('record', {}).get('password', {})

        if "credentialRecord" in properties_dict:
            self._credential_name = properties_dict['credentialRecord']['credentialName']

        if "createAs" in properties_dict:
            owner_json = properties_dict['createAs']
        else:
            owner_json = self._credential_owner_json

        if "securityAssociations" in properties_dict:
            self._credential_security_assoc = properties_dict['securityAssociations']

        request_json = {
            "credentialRecordInfo": [{
                "recordType": self._record_type,
                "credentialRecord": {
                    "credentialId": self._credential_id,
                    "credentialName": self._credential_name
                },
                "record": {
                    "userName": self._credential_user_name
                },
                "createAs": owner_json
                }]
            }

        if self._credential_security_assoc:
            request_json['credentialRecordInfo'][0].update(securityAssociations=self._credential_security_assoc)

        request = self._services['CREDENTIAL']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', request, request_json
        )

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
