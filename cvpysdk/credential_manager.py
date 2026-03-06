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

    refresh()                   --  refreshes the list of credentials on this commcell

    delete()                    --  deletes the credential record on this commcell

    get_security_associations() --  Returns the security association dictionary for a given user or user group

    add_database_creds()        --  Creates database credential on this commcell for a given DATABASE type

    add_db2_database_creds      --  Creates DB2 credential on this commcell

    add_postgres_database_creds --  Creates PostgreSQL credential on this commcell

    add_informix_database_creds --  Creates Informix credential on this commcell

    add_mysql_database_creds    --  Creates MySQL credential on this commcell

    add_oracle_database_creds   --  Creates Oracle credential on this commcell

    add_sybase_database_creds   --  Creates Sybase credential on this commcell
    add_oracle_catalog_creds    --  Creates Oracle Recovery Catalog credential on this commcell

    add_azure_cloud_creds()     --  Creates azure access key based credential on this commcell

    add_azure_app_registration_creds()  --  Creates credential for azure using azure application
	                                id and application secret key

    add_aws_s3_creds()          --  Creates aws s3 credential

    add_aws_creds()  -- Creates AWS credentials on this commcell based on the credential type

    add_bigdata_creds()         --  Creates bigdata credential on this commcell for a given database type

    add_atlas_creds()           --  Creates Credential for MongoDB Atlas

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

    refresh()                   --  refreshes the properties of credential account

    _get_credential_properties()--  returns the properties of credential account

    _update_credential_props()  -- Updates credential account properties

    update_azure_app_credential() -- Update the Azure application registration credential with new values.

"""
import json
from base64 import b64encode
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from .commcell import Commcell
from .security.usergroup import UserGroups
from .exception import SDKException
from .constants import Credential_Type


class Credentials(object):
    """
    Manages and maintains all configured credentials within a Commcell environment.

    The Credentials class provides a comprehensive interface for handling various types of credentials,
    including database, cloud, storage array, and big data credentials. It allows for secure storage,
    retrieval, addition, deletion, and management of credentials, ensuring streamlined access control
    and security association management for different services and resources in the Commcell.

    Key Features:
        - Retrieve all configured credentials via the `all_credentials` property
        - Check for the existence of a specific credential
        - Get details of a credential by name
        - Add new credentials for various record types and services (databases, storage arrays, cloud providers, big data)
        - Refresh the credentials list to sync with the latest configuration
        - Delete credentials by name
        - Manage security associations for credential owners
        - Specialized methods for adding credentials for:
            - Storage arrays
            - Multiple database types (DB2, Postgres, Informix, MySQL, Oracle, Oracle Catalog)
            - Azure cloud and app registrations
            - AWS S3 and AWS general credentials
            - Big data platforms

    This class is intended to be used as a central credential management utility within the Commcell,
    providing secure and efficient operations for credential lifecycle management.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize the Credentials object for a given Commcell instance.

        Args:
            commcell_object: Instance of the Commcell class representing the connected Commcell.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> credentials = Credentials(commcell)
            >>> # The credentials object is now initialized and ready for use

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._credentials = self._get_credentials()
        self.record_type = {
            'windows': 1,
            'linux': 2
        }

    def __str__(self) -> str:
        """Return a formatted string representation of all credentials configured on the Commcell.

        The output lists each credential with its serial number in a tabular format.

        Returns:
            A string containing all credentials configured on the Commcell, formatted for display.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> print(str(credentials))
            >>> # Output:
            >>> # S. No.        Credentials
            >>> #
            >>> #   1           admin
            >>> #   2           backup_user
            >>> #   3           restore_user

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Credentials')

        for index, credentials in enumerate(self._credentials):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, credentials)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return a string representation of the Credentials class instance.

        This method provides a human-readable description of the Credentials object,
        typically used for debugging and logging purposes.

        Returns:
            String describing the Credentials class instance.

        Example:
            >>> creds = Credentials(...)
            >>> print(repr(creds))
            Credentials class instance for Commcell

        #ai-gen-doc
        """
        return "Credentials class instance for Commcell"

    def _get_credentials(self) -> Dict[str, int]:
        """Retrieve the credentials configured on this Commcell.

        This method fetches all credentials from the Commcell and returns a dictionary
        mapping credential names (in lowercase) to their corresponding credential IDs.

        Returns:
            Dictionary where keys are credential names (str) and values are credential IDs (int).

        Raises:
            Exception: If the response from the Commcell is not successful.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> creds_dict = credentials._get_credentials()
            >>> print(creds_dict)
            >>> # Output: {'admin': 101, 'backupuser': 102}

        #ai-gen-doc
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
    def all_credentials(self) -> Dict[str, int]:
        """Get all credentials present in the Commcell.

        Returns:
            List of dictionaries, each containing details of a credential.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> all_creds = credentials.all_credentials  # Use dot notation for property access
            >>> print(f"Total credentials found: {len(all_creds)}")
            >>> # Access details of the first credential
            >>> if all_creds:
            >>>     print(f"First credential details: {all_creds}")

        #ai-gen-doc
        """
        return self._credentials

    def has_credential(self, credential_name: str) -> bool:
        """Check if a credential with the specified name exists on this Commcell.

        Args:
            credential_name: The name of the credential to check for existence.

        Returns:
            True if the specified credential is present on the Commcell, False otherwise.

        Raises:
            SDKException: If the data type of the input is invalid.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> exists = credentials.has_credential("BackupAdmin")
            >>> print(f"Credential exists: {exists}")
            >>> # Output: Credential exists: True or False

        #ai-gen-doc
        """
        if not isinstance(credential_name, str):
            raise SDKException('Credentials', '101')

        return self._credentials and credential_name.lower() in self._credentials

    def get(self, credential_name: str) -> 'Credential':
        """Retrieve the Credential object for the specified credential name.

        Args:
            credential_name: Name of the credential for which the object should be returned.

        Returns:
            Credential: The Credential object corresponding to the given name.

        Raises:
            SDKException: If a credential with the specified name does not exist.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> credential = credentials.get("MyCredential")
            >>> print(f"Credential object: {credential}")
            >>> # The returned Credential object can be used for further operations

        #ai-gen-doc
        """
        if not self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} doesn't exists on this commcell.".format(
                    credential_name)
            )

        return Credential(self._commcell_object, credential_name, self._credentials[
            credential_name.lower()])

    def add(self, record_type: str, credential_name: str, user_name: str, user_password: str,
            description: Optional[str] = None) -> None:
        """Create a new credential account on the Commcell.

        Args:
            record_type: Type of credential record to be created (e.g., "windows" or "linux").
            credential_name: Name to assign to the credential account.
            user_name: Username to associate with this credential account.
            user_password: Password for the user.
            description: Optional description for the credential account.

        Raises:
            SDKException: If the credential account already exists, if input formats are invalid,
                or if the Commcell response is unsuccessful.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> credentials.add(
            ...     record_type="windows",
            ...     credential_name="BackupAdmin",
            ...     user_name="adminuser",
            ...     user_password="securepassword123",
            ...     description="Credential for backup operations"
            ... )
            >>> # The credential account 'BackupAdmin' is now created on the Commcell.

        #ai-gen-doc
        """

        if not (isinstance(credential_name, str) and isinstance(user_name, str)):
            raise SDKException('User', '101')

        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} already exists on this commcell.".format(
                    credential_name)
            )
        password = b64encode(user_password.encode()).decode()

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

    def refresh(self) -> None:
        """Reload the list of credential records from the Commcell.

        This method updates the internal credential cache to ensure that
        the latest credential records are available for use.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> credentials.refresh()  # Refreshes the credential records
            >>> print("Credential records updated successfully")

        #ai-gen-doc
        """
        self._credentials = self._get_credentials()

    def delete(self, credential_name: str) -> None:
        """Delete the credential object for the specified credential name.

        Removes the credential associated with the given name from the Commcell.
        If the credential does not exist or the deletion fails, an SDKException is raised.

        Args:
            credential_name: Name of the credential to be deleted.

        Raises:
            SDKException: If the credential does not exist, the response is empty, or the deletion is unsuccessful.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> credentials.delete("MyCredential")
            >>> print("Credential deleted successfully")
            # If the credential does not exist, an SDKException will be raised.

        #ai-gen-doc
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

    def get_security_associations(self, owner: str, is_user: bool = False) -> Dict[str, Any]:
        """Retrieve the security association dictionary for a specified user or user group.

        Args:
            owner: The name of the user or user group for which to retrieve security associations.
            is_user: Set to True if the owner is a user; set to False if the owner is a user group.

        Returns:
            Dictionary containing the security association details for the specified user or user group.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> # For a user
            >>> user_assoc = credentials.get_security_associations('john.doe', is_user=True)
            >>> print(user_assoc)
            >>> # For a user group
            >>> group_assoc = credentials.get_security_associations('BackupAdmins', is_user=False)
            >>> print(group_assoc)

        #ai-gen-doc
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

    def add_storage_array_creds(self, credential_name: str, username: str, password: str,
                                description: Optional[str] = None) -> 'Credential':
        """Create a new storage array credential on the Commcell.

        Args:
            credential_name: Name to assign to the credential account.
            username: Username for the storage array credential.
            password: Password for the credential account.
            description: Optional description for the credential.

        Returns:
            Credential: An instance representing the newly created storage array credential.

        Raises:
            SDKException: If a credential with the given name already exists on the Commcell,
                or if the response from the server is not successful.

        Example:
            >>> creds = Credentials(commcell_object)
            >>> new_cred = creds.add_storage_array_creds(
            ...     credential_name="ArrayBackupUser",
            ...     username="backupuser",
            ...     password="securepassword123",
            ...     description="Credential for array backups"
            ... )
            >>> print(f"Created credential: {new_cred}")

        #ai-gen-doc
        """
        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} already exists on this commcell.".format(
                    credential_name)
            )
        encoded_password = b64encode(password.encode()).decode()
        create_credential = {
            "accountType": "STORAGE_ARRAY_ACCOUNT",
            "name": credential_name,
            "userAccount": username,
            "password": encoded_password,
            "description": description
        }

        request = self._services['ADD_CREDENTIALS']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential
        )
        if flag:
            if response.json():
                id = response.json()['id']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
        return Credential(self._commcell_object, credential_name, id)

    def add_database_creds(
            self,
            database_type: str,
            credential_name: str,
            username: str,
            password: str,
            description: Optional[str] = None,
            service_name: Optional[str] = None
    ) -> 'Credential':
        """Create a new database credential on the Commcell for the specified database type.

        Args:
            database_type: Type of database credential to be created.
                Accepted values: "MYSQL", "INFORMIX", "POSTGRESQL", "DB2", "ORACLE", "ORACLE_CATALOG_ACCOUNT",
                 "SQL_SERVER_ACCOUNT","SYBASE".
            credential_name: Name to assign to the credential account.
            username: Database username for authentication.
            password: Database password for authentication.
            description: Optional description of the credential.
            service_name: Optional service name for Oracle databases.

        Returns:
            Credential: An instance representing the newly created database credential.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials(commcell_object)
            >>> db_cred = creds.add_database_creds(
            ...     database_type="MYSQL",
            ...     credential_name="MySQLAdmin",
            ...     username="admin",
            ...     password="securepass",
            ...     description="MySQL admin credentials"
            ... )
            >>> print(f"Created credential: {db_cred}")

        #ai-gen-doc
        """
        if database_type not in ["MYSQL", "INFORMIX", "POSTGRESQL", "DB2", "ORACLE", "ORACLE_CATALOG_ACCOUNT",
                                 "SQL_SERVER_ACCOUNT","SYBASE"]:
            raise SDKException(
                'Credential', '102', "Invalid database Type provided."
            )
        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} already exists on this commcell.".format(
                    credential_name)
            )
        password = b64encode(password.encode()).decode()
        create_credential = {
            "accountType": "DATABASE_ACCOUNT",
            "databaseCredentialType": database_type,
            "name": credential_name,
            "username": username,
            "password": password,
            "description": description
        }

        if database_type in ["ORACLE", "ORACLE_CATALOG_ACCOUNT"]:
            create_credential["serviceName"] = service_name

        request = self._services['ADD_CREDENTIALS']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential
        )
        if flag:
            if response.json():
                id = response.json()['id']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
        return Credential(self._commcell_object, credential_name, id)

    def add_db2_database_creds(self, credential_name: str, username: str, password: str,
                               description: Optional[str] = None) -> None:
        """Create a DB2 database credential on the Commcell.

        Args:
            credential_name: Name to assign to the credential account.
            username: Username for the DB2 credential.
            password: Password for the DB2 credential.
            description: Optional description for the credential.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials()
            >>> creds.add_db2_database_creds(
            ...     credential_name="db2_admin",
            ...     username="admin_user",
            ...     password="secure_password",
            ...     description="DB2 admin credentials"
            ... )
            >>> print("DB2 credential added successfully")

        #ai-gen-doc
        """
        self.add_database_creds("DB2", credential_name, username, password, description)

    def add_postgres_database_creds(self, credential_name: str, username: str, password: str,
                                    description: Optional[str] = None) -> None:
        """Create a PostgreSQL credential on the Commcell.

        Args:
            credential_name: Name to assign to the credential account.
            username: PostgreSQL username for authentication.
            password: PostgreSQL password for authentication.
            description: Optional description of the credential.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials()
            >>> creds.add_postgres_database_creds(
            ...     credential_name="pg_admin",
            ...     username="admin",
            ...     password="securepass123",
            ...     description="PostgreSQL admin credentials"
            ... )
            >>> print("PostgreSQL credential added successfully")
        #ai-gen-doc
        """
        self.add_database_creds("POSTGRESQL", credential_name, username, password, description)

    def add_informix_database_creds(self, credential_name: str, username: str, password: str,
                                    description: Optional[str] = None) -> None:
        """Create an Informix database credential on the Commcell.

        Args:
            credential_name: Name to assign to the credential account.
            username: Informix username and domain name (e.g., "domain\\username").
            password: Password for the Informix account.
            description: Optional description for the credential.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials()
            >>> creds.add_informix_database_creds(
            ...     credential_name="InformixAdmin",
            ...     username="domain\\informixuser",
            ...     password="securepassword",
            ...     description="Informix admin credentials for reporting"
            ... )
            >>> print("Informix credential added successfully")
        #ai-gen-doc
        """
        self.add_database_creds("INFORMIX", credential_name, username, password, description)

    def add_mysql_database_creds(self, credential_name: str, username: str, password: str,
                                 description: Optional[str] = None) -> None:
        """Create a MySQL credential on the Commcell.

        Args:
            credential_name: Name to assign to the MySQL credential account.
            username: MySQL username for authentication.
            password: MySQL password for authentication.
            description: Optional description for the credential account.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials(commcell_object)
            >>> creds.add_mysql_database_creds(
            ...     credential_name="MySQLAdmin",
            ...     username="admin",
            ...     password="securepassword",
            ...     description="Credential for MySQL backups"
            ... )
            >>> print("MySQL credential added successfully")

        #ai-gen-doc
        """
        self.add_database_creds("MYSQL", credential_name, username, password, description)

    def add_oracle_database_creds(self, credential_name: str, username: str, password: str, service_name: str,
                                  description: Optional[str] = None):
        """Create Oracle database credentials on the Commcell.

        Args:
            credential_name: Name to assign to the Oracle credential account.
            username: Oracle database username.
            password: Oracle database password.
            service_name: Service name of the Oracle database.
            description: Optional description for the credential.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials()
            >>> creds.add_oracle_database_creds(
            ...     credential_name="OracleProdCreds",
            ...     username="dbadmin",
            ...     password="securepass123",
            ...     service_name="ORCLPROD",
            ...     description="Production Oracle DB credentials"
            ... )
            >>> print("Oracle credentials added successfully")

        #ai-gen-doc
        """
        return self.add_database_creds("ORACLE", credential_name, username, password, description, service_name)

    def add_oracle_catalog_creds(self, credential_name: str, username: str, password: str, service_name: str,
                                 description: Optional[str] = None):
        """Create Oracle Recovery Catalog credentials on the Commcell.

        This method adds a new Oracle Recovery Catalog credential account, which can be used for database operations requiring authentication.

        Args:
            credential_name: Name to assign to the credential account.
            username: Oracle database username.
            password: Oracle database password.
            service_name: Service name of the Oracle database.
            description: Optional description for the credential account.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials(commcell_object)
            >>> creds.add_oracle_catalog_creds(
            ...     credential_name="OracleCatalogUser",
            ...     username="oracle_user",
            ...     password="secure_password",
            ...     service_name="ORCLDB",
            ...     description="Recovery catalog credentials for Oracle DB"
            ... )
        #ai-gen-doc
        """
        return self.add_database_creds("ORACLE_CATALOG_ACCOUNT", credential_name, username, password, description,
                                       service_name)
    def add_sybase_database_creds(self, credential_name, username, password, description=None):
        """Create Sybase database credentials on the Commcell.

        Args:
            credential_name: Name to assign to the Sybase credential account.
            username: Sybase database username.
            password: Sybase database password.
            description: Optional description for the credential.

        Raises:
            SDKException: If the credential account already exists on the Commcell or if the response is not successful.

        Example:
            >>> creds = Credentials()
            >>> creds.add_sybase_database_creds(
            ...     credential_name="SybaseProdCreds",
            ...     username="dbadmin",
            ...     password="securepass123",
            ...     description="Production Sybase DB credentials"
            ... )
            >>> print("Sybase credentials added successfully")

        #ai-gen-doc
        """
        return self.add_database_creds("SYBASE", credential_name, username, password, description)


    def add_azure_cloud_creds(self, credential_name: str, account_name: str, access_key_id: str, **kwargs: Any) -> None:
        """Create an Azure access key-based credential on this Commcell.

        This method adds a new credential for an Azure storage account using the provided access key.
        Additional supported arguments can be passed via kwargs, such as a description.

        Args:
            credential_name: Name to assign to the credential account.
            account_name: Name of the Azure storage account.
            access_key_id: Access key for the Azure storage account.
            **kwargs: Additional key-value pairs for supported arguments.
                Supported argument values:
                    description (str): Description of the credentials.

        Raises:
            SDKException: If argument types are incorrect, the credential account already exists,
                string formats are improper, or the response is not successful.

        Example:
            >>> creds = Credentials(commcell_object)
            >>> creds.add_azure_cloud_creds(
            ...     credential_name="AzureBlobCred",
            ...     account_name="myazurestorage",
            ...     access_key_id="my-access-key",
            ...     description="Credential for Azure Blob Storage"
            ... )
            >>> # The Azure credential is now added to the Commcell

        #ai-gen-doc
        """
        description = kwargs.get("description", "")

        if not (isinstance(access_key_id, str) and isinstance(account_name, str)
                and isinstance(credential_name, str)):
            raise SDKException("Credential", "101")

        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} already exists on this commcell.".format(
                    credential_name)
            )

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

    def add_azure_app_registration_creds(
            self,
            credential_name: str,
            tenant_id: str,
            application_id: str,
            application_secret: str,
            description: str = "",
            **kwargs: Any
    ) -> None:
        """Create Azure application registration credentials on the Commcell.

        This method adds a credential account using Azure application ID and secret key.
        Optionally, certificate-based authentication can be configured for SharePoint by
        providing certificate path and password via keyword arguments.

        Args:
            credential_name: Name to assign to the credential account.
            tenant_id: Azure tenant ID as a string.
            application_id: Azure application ID as a string.
            application_secret: Azure application secret key as a string.
            description: Optional description for the credentials.
            **kwargs: Additional parameters for certificate-based authentication.
                cert_path: Certificate path for SharePoint authentication.
                cert_password: Certificate password for SharePoint authentication.

        Raises:
            SDKException: If argument types are incorrect, credential account already exists,
                or the response from Commcell is unsuccessful.

        Example:
            >>> credentials = Credentials(commcell_object)
            >>> credentials.add_azure_app_registration_creds(
            ...     credential_name="AzureAppCreds",
            ...     tenant_id="your-tenant-id",
            ...     application_id="your-app-id",
            ...     application_secret="your-app-secret",
            ...     description="Azure app registration for backup"
            ... )
            >>> # For certificate-based authentication:
            >>> credentials.add_azure_app_registration_creds(
            ...     credential_name="AzureCertCreds",
            ...     tenant_id="your-tenant-id",
            ...     application_id="your-app-id",
            ...     application_secret="your-app-secret",
            ...     cert_path=b"certificate-bytes",
            ...     cert_password="cert-password"
            ... )
        #ai-gen-doc
        """
        if not (
                isinstance(
                    application_id,
                    str) and isinstance(
            tenant_id,
            str) and isinstance(
            credential_name,
            str) and isinstance(
            application_secret,
            str)):
            raise SDKException("Credential", "101")

        if self.has_credential(credential_name):
            raise SDKException(
                'Credential',
                '102',
                "Credential {0} already exists on this commcell.".format(credential_name))

        password = b64encode(application_secret.encode()).decode()

        create_credential_account = {
            "credentialRecordInfo": [
                {
                    "additionalInformation": {
                        "azureCredInfo": {
                            "applicationId": application_id,
                            "endpoints": {
                                "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                                "resourceManagerEndpoint": "https://management.azure.com/",
                                "storageEndpoint": "blob.core.windows.net"},
                            "environment": "AzureCloud",
                            "tenantId": tenant_id}
                    },
                    "createAs": {},
                    "credentialRecord": {
                        "credentialName": credential_name},
                    "description": description,
                    "record": {
                        "userName": application_id,
                        "password": password},
                    "recordType": "AZUREACCOUNT",
                    "securityAssociations": {
                        "associations": [],
                        "associationsOperationType": 1}}]}

        if kwargs.get("cert_path", None) and kwargs.get("cert_password", None):
            cert_string = b64encode(kwargs.get("cert_path")).decode()
            cert_string = b64encode(cert_string.encode()).decode()

            cert_password = b64encode(kwargs.get("cert_password").encode()).decode()

            azure_cred_info = {
                "authType": "AZURE_OAUTH_SHARED_SECRET_CERTIFICATE",
                "applicationId": application_id,
                "certificateP12": cert_string,
                "certPassword": cert_password,
                "tenantId": tenant_id,
                "environment": "AzureCloud",
                "endpoints": {
                    "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                    "resourceManagerEndpoint": "https://management.azure.com/",
                    "storageEndpoint": "blob.core.windows.net"
                }
            }
            create_credential_account["credentialRecordInfo"][0]["additionalInformation"][
                "azureCredInfo"] = azure_cred_info
            create_credential_account["credentialRecordInfo"][0]["recordType"] = "AZUREACCOUNT_SECRET_CERTIFICATE"

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
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def add_k8s_credentials(self, api_endpoint, ca_certificate, description, name, service_account, service_token):
        """Creates k8s credential on this commcell
            Args:

                api_endpoint (str)   --  API endpoint of the k8s cluster

                ca_certificate  (str)     --  CA certificate of the k8s cluster

                description (str)       --  description of the credential

                name (str)       --  name to be given to credential account

                service_account (str)       --  service account name

                service_token (str)       --  service account token

            Raises:
                SDKException:
                    if credential account is already present on the commcell

                    if response is not successful
        """
        if self.has_credential(name):
            raise SDKException(
                'Credential', '102', "Credential {0} already exists on this commcell.".format(
                    name)
            )
        encoded_token = b64encode(service_token.encode()).decode()
        create_credential = {
            "accountType": "KUBERNETES_SERVICE_ACCOUNT",
            "name": name,
            "description": description,
            "apiEndpoint": api_endpoint,
            "caCertificate": ca_certificate,
            "serviceAccount": service_account,
            "serviceToken": encoded_token
        }

        request = self._services['ADD_CREDENTIALS']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential
        )
        if flag:
            if response.json():
                id = response.json()['id']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
        return Credential(self._commcell_object, name, id)

    def add_aws_s3_creds(
            self,
            credential_name: str,
            access_key_id: str,
            secret_access_key: str,
            description: Optional[str] = None
    ) -> None:
        """Create an AWS S3 access key-based credential on this Commcell.

        This method adds a new credential account for AWS S3 access, using the provided access key ID and secret access key.
        The credential can be used for operations requiring authenticated access to AWS S3 buckets.

        Args:
            credential_name: Name to assign to the credential account.
            access_key_id: AWS S3 access key ID.
            secret_access_key: AWS S3 secret access key.
            description: Optional description for the credential account.

        Raises:
            SDKException: If argument types are incorrect.
            SDKException: If a credential account with the given name already exists on the Commcell.
            SDKException: If the response from the Commcell is not successful.

        Example:
            >>> creds = Credentials(commcell_object)
            >>> creds.add_aws_s3_creds(
            ...     credential_name="MyS3Credential",
            ...     access_key_id="AKIAIOSFODNN7EXAMPLE",
            ...     secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            ...     description="AWS S3 credential for backup operations"
            ... )
            >>> print("AWS S3 credential added successfully.")

        #ai-gen-doc
        """

        if not (
                isinstance(
                    access_key_id,
                    str) and isinstance(
            secret_access_key,
            str) and isinstance(
            credential_name,
            str)):
            raise SDKException("Credential", "101")

        if self.has_credential(credential_name):
            raise SDKException(
                'Credential',
                '102',
                "Credential {0} already exists on this commcell.".format(credential_name))

        password = b64encode(secret_access_key.encode()).decode()
        create_credential_account = {
            "credentialRecordInfo": [
                {
                    "createAs": {
                    },
                    "credentialRecord": {
                        "credentialName": credential_name
                    },
                    "description": description,
                    "record": {
                        "userName": access_key_id,
                        "password": password
                    },
                    "recordType": "AMAZON_S3",
                    "securityAssociations": {
                        "associations": [
                        ],
                        "associationsOperationType": 1
                    }
                }
            ]
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['CREDENTIAL'], payload=create_credential_account)
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
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def add_aws_creds(self, credential_name: str, creds_type: str, **kwargs: Any) -> None:
        """Create AWS credentials on the Commcell based on the specified credential type.

        This method adds a new AWS credential account to the Commcell. The required parameters
        depend on the credential type specified.

        Args:
            credential_name: Name to assign to the credential account.
            creds_type: Type of AWS credential to create. Supported values:
                - 'AWS_ACCESS_KEY': Requires 'access_key' and 'secret' in kwargs. 'description' is optional.
                - 'AWS_STS_IAM_ROLE': Requires 'role_arn' in kwargs. 'external_id' and 'description' are optional.
            **kwargs: Additional parameters required for the specific credential type.

        Raises:
            SDKException: If arguments are invalid, the credential already exists, or the response is unsuccessful.

        Example:
            >>> # Add AWS Access Key credentials
            >>> creds = Credentials()
            >>> creds.add_aws_creds(
            ...     credential_name="MyAWSAccessKey",
            ...     creds_type="AWS_ACCESS_KEY",
            ...     access_key="AKIA...",
            ...     secret="mySecretKey",
            ...     description="Backup AWS S3 credentials"
            ... )
            >>>
            >>> # Add AWS STS IAM Role credentials
            >>> creds.add_aws_creds(
            ...     credential_name="MyIAMRole",
            ...     creds_type="AWS_STS_IAM_ROLE",
            ...     role_arn="arn:aws:iam::123456789012:role/MyRole",
            ...     external_id="optional-external-id",
            ...     description="IAM role for cross-account access"
            ... )
        #ai-gen-doc
        """
        if not isinstance(credential_name, str) or not isinstance(creds_type, str):
            raise SDKException("Credential", "101", "Invalid argument types provided.")

        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', f"Credential {credential_name} already exists on this commcell."
            )

        if creds_type == 'AWS_ACCESS_KEY':
            access_key = kwargs.get('access_key')
            secret = kwargs.get('secret')
            description = kwargs.get('description', "")
            if not access_key or not secret or not (isinstance(access_key, str) and isinstance(secret, str)):
                raise SDKException("Credential", "102", "Invalid AWS access key or secret.")
            encoded_secret = b64encode(secret.encode('utf-8')).decode('utf-8')
            create_credential_account = {
                "accountType": "CLOUD_ACCOUNT",
                "vendorType": "AMAZON",
                "authType": "AMAZON_S3",
                "name": credential_name,
                "accessKeyId": access_key,
                "secretAccessKey": encoded_secret,
                "description": description
            }

        elif creds_type == 'AWS_STS_IAM_ROLE':
            role_arn = kwargs.get('role_arn')
            external_id = kwargs.get('external_id', "")
            description = kwargs.get('description', "")
            if not role_arn or not isinstance(role_arn, str):
                raise SDKException("Credential", "102", "Invalid IAM role ARN.")
            create_credential_account = {
                "accountType": "CLOUD_ACCOUNT",
                "vendorType": "AMAZON",
                "authType": "AMAZON_STS_IAM_ROLE",
                "name": credential_name,
                "externalId": external_id,
                "roleArn": role_arn,
                "description": description,
                "password": ""
            }

        else:
            raise SDKException("Credential", "102", f"Unsupported credential type: {creds_type}")

        request = self._services['ADD_CREDENTIALS']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential_account
        )

        if flag:
            if response.json():
                response_json = response.json().get('error', {})
                error_code = response_json.get('errorCode', 0)
                error_message = response_json.get('errorMessage', '')
                if error_code != 0:
                    raise SDKException('Response', '102', error_message)
            else:
                raise SDKException('Response', '102', "Empty response received.")
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def add_bigdata_creds(self, database_type: str, credential_name: str, username: str, password: str,
                          description: Optional[str] = None, **kwargs: Any) -> 'Credential':
        """Create a big data credential for a specified database type on this Commcell.

        This method adds a credential for supported big data database types such as Cassandra, CockroachDB, or MongoDB.
        Additional parameters may be required for certain database types and can be provided via kwargs.

        Args:
            database_type: Type of database credential to be created.
                Accepted values: "CASSANDRA_ACCOUNT", "CASSANDRA_JMX_ACCOUNT", "CASSANDRA_TRUSTSTORE_ACCOUNT",
                "CASSANDRA_KEYSTORE_ACCOUNT", "COCKROACHDB_ACCOUNT", "MONGODB_ACCOUNT", "MONGODB_SSL_OPTIONS",
                "COUCHBASE_ACCOUNT","YUGABYTE_ACCOUNT".
            credential_name: Name to assign to the credential account.
            username: Username for the credential.
            password: Password for the credential.
            description: Optional description of the credential.
            **kwargs: Additional parameters required for specific credential types (e.g., sslClientCertFile, sslCAFile, sslPEMKeyFile).

        Returns:
            Credential: An instance representing the newly created credential.

        Raises:
            SDKException: If the credential account already exists or if the response is not successful.

        Example:
            >>> # Create a Cassandra credential
            >>> cred = credentials.add_bigdata_creds(
            ...     database_type="CASSANDRA_ACCOUNT",
            ...     credential_name="CassandraCred01",
            ...     username="cassandra_user",
            ...     password="secure_password",
            ...     description="Cassandra DB credential"
            ... )
            >>> print(f"Credential created: {cred}")

            >>> # Create a CockroachDB credential with SSL options
            >>> cred = credentials.add_bigdata_creds(
            ...     database_type="COCKROACHDB_ACCOUNT",
            ...     credential_name="CockroachCred01",
            ...     username="roach_user",
            ...     password="secure_password",
            ...     description="CockroachDB credential",
            ...     sslClientCertFile="/path/client.crt",
            ...     sslCAFile="/path/ca.crt",
            ...     sslPEMKeyFile="/path/client.key"
            ... )
            >>> print(f"Credential created: {cred}")

        #ai-gen-doc
        """
        valid_types = {
            "CASSANDRA_ACCOUNT", "CASSANDRA_JMX_ACCOUNT", "CASSANDRA_TRUSTSTORE_ACCOUNT",
            "CASSANDRA_KEYSTORE_ACCOUNT", "COCKROACHDB_ACCOUNT", "MONGODB_ACCOUNT", "MONGODB_SSL_OPTIONS",
            "COUCHBASE_ACCOUNT", "YUGABYTE_ACCOUNT"
        }

        if database_type not in valid_types:
            raise SDKException(
                'Credential', '102', "Invalid database Type provided."
            )
        if self.has_credential(credential_name):
            raise SDKException(
                'Credential', '102', "Credential {0} already exists on this commcell.".format(
                    credential_name)
            )
        password = b64encode(password.encode()).decode()

        if database_type == "COCKROACHDB_ACCOUNT":
            sslClientCertFile = kwargs.get('sslClientCertFile', "")
            sslCAFile = kwargs.get('sslCAFile', "")
            sslPEMKeyFile = kwargs.get('sslPEMKeyFile', "")
            create_credential = {
                "accountType": "BIG_DATA_APPS_ACCOUNT",
                "databaseCredentialType": database_type,
                "name": credential_name,
                "sslClientCertFile": sslClientCertFile,
                "sslCAFile": sslCAFile,
                "sslPEMKeyFile": sslPEMKeyFile,
                "password": password,
                "description": description
            }
        elif database_type == "MONGODB_ACCOUNT":
            create_credential = {
                "name": credential_name,
                "description": "Credential manager created by MongoDB Automation",
                "accountType": "BIG_DATA_APPS_ACCOUNT",
                "databaseCredentialType": database_type,
                "userName": username,
                "password": password
            }
        elif database_type == "MONGODB_SSL_OPTIONS":
            sslClientCertFile = kwargs.get('sslClientCertFile', "")
            sslCAFile = kwargs.get('sslCAFile', "")
            sslPEMKeyFile = kwargs.get('sslPEMKeyFile', "")
            create_credential = {
                "accountType": "BIG_DATA_APPS_ACCOUNT",
                "databaseCredentialType": database_type,
                "name": credential_name,
                "sslCAFile": sslCAFile,
                "sslPEMKeyFile": sslPEMKeyFile,
                "username": username,
                "password": password,
                "description": description
            }
        elif database_type == "COUCHBASE_ACCOUNT":
            create_credential = {
                "accountType": "BIG_DATA_APPS_ACCOUNT",
                "databaseCredentialType": database_type,
                "name": credential_name,
                "userName": username,
                "password": password,
                "description": description
            }
        elif database_type == "YUGABYTE_ACCOUNT":
            create_credential = {
                "accountType": "BIG_DATA_APPS_ACCOUNT",
                "databaseCredentialType": database_type,
                "name": credential_name,
                "password": password,
                "description": description
            }
        else:
            # CASSANDRA credential integrated.
            # Integration of other Big Data credentials pending.
            create_credential = {
                "accountType": "BIG_DATA_APPS_ACCOUNT",
                "databaseCredentialType": database_type,
                "name": credential_name,
                "username": username,
                "password": password,
                "description": description
            }

        request = self._services['ADD_CREDENTIALS']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential
        )
        if flag:
            if response.json():
                id = response.json()['id']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
        return Credential(self._commcell_object, credential_name, id)

    def add_atlas_creds(self, credential_name: str, **kwargs: Any) -> None:

        """Create Atlas  credentials on the Commcell
        This method adds a new MongoDB Atlas credential  to the Commcell

        Args:
            credential_name: Name to assign to the credential account.
            **kwargs: Additional parameters required for the specific credential type.
        Raises:
            SDKException: If arguments are invalid, the credential already exists, or the response is unsuccessful.
        Example:
            >>> # Add AWS Access Key credentials
            >>> creds = Credentials()
            >>> creds.add_atlas_creds(
            ...     credential_name="MyAccessKey",
            ...     access_key="AKIA...",
            ...     secret="mySecretKey",
            ...     description="Atlas credentials"
            ... )
        #ai-gen-doc
        """
        access_key = kwargs.get('access_key')
        secret = kwargs.get('secret')
        description = kwargs.get('description', "")
        encoded_secret = b64encode(secret.encode('utf-8')).decode('utf-8')
        if not secret or not isinstance(secret, str):
            raise SDKException("Credential", "102", "Invalid or missing secret key.")

        create_credential = {
            "accountType": "CLOUD_ACCOUNT",
            "vendorType": "MONGODB_ATLAS_ACCESS_KEY",
            "name": credential_name,
            "accessKeyId": access_key,
            "secretAccessKey": encoded_secret,
            "description": description
        }

        request = self._services['ADD_CREDENTIALS']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', request, create_credential
        )

        if flag:
            if response.json():
                response_json = response.json().get('error', {})
                error_code = response_json.get('errorCode', 0)
                error_message = response_json.get('errorMessage', '')
                if error_code != 0:
                    raise SDKException('Response', '102', error_message)
            else:
                raise SDKException('Response', '102', "Empty response received.")
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()


class Credential(object):
    """
    Class for representing and managing a Credential record within a Commcell environment.

    This class encapsulates the properties and operations associated with a specific credential,
    including its identification, description, security properties, user information, and record type.
    It provides methods for retrieving, updating, and refreshing credential details, as well as
    managing security and user credentials.

    Key Features:
        - Initialize credential objects with name and ID
        - Retrieve credential properties such as name, ID, description, security properties, user name, and record type
        - Update credential security settings and user credentials
        - Refresh credential information from the Commcell
        - Internal methods for fetching and updating credential properties

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', credential_name: str, credential_id: Optional[str] = None) -> None:
        """Initialize a Credential object for the specified credential.

        Args:
            commcell_object: Instance of the Commcell class representing the Commcell connection.
            credential_name: Name of the credential as a string.
            credential_id: Optional credential ID as a string. If not provided, the ID will be determined automatically.

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> credential = Credential(commcell, "MyCredential")
            >>> # To specify a credential ID explicitly
            >>> credential = Credential(commcell, "MyCredential", credential_id="12345")

        #ai-gen-doc
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
        self._credential_properties = None
        self._credential_security_assoc = []
        self._record_type = None
        self._credential_password = ""
        self._record_types = {
            'WINDOWSACCOUNT': 'Windows',
            'LINUXACCOUNT': 'Linux'
        }
        self._get_credential_properties()

    def __repr__(self) -> str:
        """Return a string representation of the Credential instance.

        Returns:
            A string describing the Credential object, including its credential name.

        Example:
            >>> credential = Credential(...)
            >>> print(repr(credential))
            Credential class instance for Credential: "MyCredential"
        #ai-gen-doc
        """
        representation_string = 'Credential class instance for Credential: "{0}"'
        return representation_string.format(self.credential_name)

    def _get_credential_id(self, name: str) -> str:
        """Retrieve the credential ID associated with the specified credential name.

        Args:
            name: The credential account name as a string.

        Returns:
            The credential ID corresponding to the provided name.

        Example:
            >>> credential = Credential(commcell_object)
            >>> credential_id = credential._get_credential_id("MyAccount")
            >>> print(f"Credential ID: {credential_id}")

        #ai-gen-doc
        """
        creds = Credentials(self._commcell_object)
        return creds.get(credential_name=name)._credential_id

    @property
    def credential_name(self) -> str:
        """Get the name of the credential record.

        Returns:
            The credential name as a string.

        Example:
            >>> credential = Credential(...)
            >>> name = credential.credential_name  # Use dot notation for property access
            >>> print(f"Credential name: {name}")

        #ai-gen-doc
        """
        return self._credential_name

    @credential_name.setter
    def credential_name(self, val: str) -> None:
        """Set the name of the credential record.

        Args:
            val: The new name to assign to the credential record as a string.

        Example:
            >>> credential = Credential(...)
            >>> credential.credential_name = "MyDatabaseCredential"  # Use assignment for property setter
            >>> # The credential name is now updated to "MyDatabaseCredential"

        #ai-gen-doc
        """
        props_dict = {
            "credentialRecord": {
                "credentialId": self._credential_id,
                "credentialName": val
            }
        }
        self._update_credential_props(properties_dict=props_dict)

    @property
    def credential_id(self) -> int:
        """Get the unique identifier for this Commcell credential record.

        Returns:
            The credential ID as an integer.

        Example:
            >>> credential = Credential(...)
            >>> cred_id = credential.credential_id  # Use dot notation for property access
            >>> print(f"Credential ID: {cred_id}")
        #ai-gen-doc
        """
        return self._credential_id

    @property
    def credential_description(self) -> Optional[str]:
        """Get the description of this Commcell credential record.

        Returns:
            The credential description as a string, or None if not set.

        Example:
            >>> credential = Credential(...)
            >>> description = credential.credential_description  # Use dot notation for property access
            >>> print(f"Credential description: {description}")
        #ai-gen-doc
        """
        return self._credential_properties.get('description')

    @credential_description.setter
    def credential_description(self, value: str) -> None:
        """Set the description for this Commcell Credential record.

        Args:
            value: The description to assign to the credential as a string.

        Example:
            >>> credential = Credential(...)
            >>> credential.credential_description = "Service account for backup operations"
            >>> # The credential description is now updated

        #ai-gen-doc
        """
        props_dict = {
            "description": value
        }
        self._update_credential_props(props_dict)

    @property
    def credential_security_properties(self) -> Any:
        """Get the security association properties for this Credential.

        Returns:
            The security association details associated with the Credential. The type may vary depending on implementation.

        Example:
            >>> credential = Credential(...)
            >>> security_props = credential.credential_security_properties  # Use dot notation for property access
            >>> print(f"Security properties: {security_props}")
            >>> # The returned value contains security association information for the credential

        #ai-gen-doc
        """
        return self._credential_security_assoc

    def update_securtiy(self, name: str, is_user: bool = True) -> Any:
        """Update the security association for this Commcell Credential record.

        This method updates the security association for the credential, associating it with either a user or a user group.

        Args:
            name: The name of the user or user group to associate with the credential.
            is_user: Set to True to associate with a user, or False to associate with a user group.

        Returns:
            The result of the credential property update operation.

        Example:
            >>> credential = Credential(...)
            >>> # Associate with a user
            >>> result = credential.update_securtiy("john.doe", is_user=True)
            >>> print(result)
            >>> # Associate with a user group
            >>> result = credential.update_securtiy("BackupAdmins", is_user=False)
            >>> print(result)
        #ai-gen-doc
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
    def credential_user_name(self) -> str:
        """Get the user name associated with this Commcell credential record.

        Returns:
            The credential user name as a string.

        Example:
            >>> credential = Credential(...)
            >>> user_name = credential.credential_user_name  # Use dot notation for property access
            >>> print(f"Credential user name: {user_name}")
        #ai-gen-doc
        """
        return self._credential_user_name

    def update_user_credential(self, uname: str, upassword: str) -> None:
        """Update the credential with a new user name and password.

        Args:
            uname: The new user name as a string.
            upassword: The new password for the user as a string.

        Example:
            >>> credential = Credential()
            >>> credential.update_user_credential('new_user', 'secure_password123')
            >>> # The credential is now updated with the new user name and password

        #ai-gen-doc
        """
        creds_dict = {
            "record": {
                "userName": uname,
                "password": b64encode(upassword.encode()).decode()
            }
        }
        self._update_credential_props(properties_dict=creds_dict)

    @property
    def credential_record_type(self) -> str:
        """Get the credential record type name for this Commcell credential.

        Returns:
            The name of the credential record type as a string.

        Example:
            >>> credential = Credential(...)
            >>> record_type = credential.credential_record_type  # Use dot notation for property access
            >>> print(f"Credential record type: {record_type}")

        #ai-gen-doc
        """
        return self._record_types[self._record_type]

    def refresh(self) -> None:
        """Reload the properties of the Credential object.

        This method updates the Credential instance with the latest property values,
        ensuring that any changes made externally are reflected in the object.

        Example:
            >>> credential = Credential(...)
            >>> credential.refresh()  # Refreshes credential properties from the source
            >>> print("Credential properties updated successfully")
        #ai-gen-doc
        """
        self._get_credential_properties()

    def _get_credential_properties(self) -> None:
        """Retrieve and update the properties of this Credential record from the Commcell.

        This method fetches the credential details from the Commcell server and updates
        the internal properties of the Credential object, such as credential ID, name,
        user name, record type, and associated security information.

        Raises:
            SDKException: If the response from the Commcell server is invalid or if the
                request fails.

        Example:
            >>> credential = Credential(commcell_object, credential_name)
            >>> credential._get_credential_properties()
            >>> print(f"Credential ID: {credential._credential_id}")
            >>> print(f"Credential Name: {credential._credential_name}")
            >>> print(f"User Name: {credential._credential_user_name}")
            >>> print(f"Record Type: {credential._record_type}")
            >>> print(f"Security Associations: {credential._credential_security_assoc}")
        #ai-gen-doc
        """
        property_request = self._services['V5_CREDENTIAL'] % (
            self._credential_id)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', property_request
        )

        if flag:
            if response.json():
                self._credential_properties = response.json()
                self._credential_id = self._credential_properties.get('id')
                self._credential_name = self._credential_properties.get('name')
                self._credential_user_name = self._credential_properties.get('userAccount')
                self._record_type = self._credential_properties.get('accountType')
                security = self._credential_properties.get('security', {})
                associations = security.get('associations', [])
                for association in associations:
                    if 'user' in association:
                        self._credential_security_assoc.append({
                            'user': association['user']['name']
                        })
                    elif 'userGroup' in association:
                        self._credential_security_assoc.append({
                            'userGroup': association['userGroup']['name']
                        })
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _update_credential_props(self, properties_dict: Dict[str, Any]) -> None:
        """Update the properties of this credential using the provided dictionary.

        Args:
            properties_dict: Dictionary containing credential properties to update.
                Example:
                    {
                        "description": "My description",
                        "record": {
                            "userName": "admin",
                            "password": "secret"
                        },
                        "credentialRecord": {
                            "credentialName": "MyCredential"
                        },
                        "securityAssociations": {...}
                    }

        Raises:
            SDKException: If the credential does not exist, the response is empty, or the update is unsuccessful.

        Example:
            >>> properties = {
            ...     "description": "Updated credential description",
            ...     "record": {
            ...         "userName": "new_user",
            ...         "password": "new_password"
            ...     },
            ...     "credentialRecord": {
            ...         "credentialName": "UpdatedCredential"
            ...     }
            ... }
            >>> credential = Credential(...)
            >>> credential._update_credential_props(properties)
            >>> print("Credential properties updated successfully")
        #ai-gen-doc
        """
        if "record" in properties_dict:
            self._credential_user_name = properties_dict['record']['userName']
            self._credential_password = properties_dict.get('record', {}).get('password', {})

        if "credentialRecord" in properties_dict:
            self._credential_name = properties_dict['credentialRecord']['credentialName']

        request_json = {
            "credentialRecordInfo": [{
                "recordType": self._record_type,
                "credentialRecord": {
                    "credentialId": self._credential_id,
                    "credentialName": self._credential_name
                },
                "record": {
                    "userName": self._credential_user_name
                }
            }]
        }
        if "securityAssociations" in properties_dict:
            request_json['credentialRecordInfo'][0].update(securityAssociations=properties_dict['securityAssociations'])

        request = self._services['CREDENTIAL']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', request, request_json
        )

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def update_azure_app_credential(self, app_secret, credential_name=None, app_id=None, tenant_id=None, description=None):
        """Update the Azure application registration credential with new values.

        This method updates the Azure application registration credential properties such as application secret, application ID, tenant ID, and description.

        Args:
            app_secret: The new application secret key as a string.
            app_id: The new Azure application ID as a string (optional).
            tenant_id: The new Azure tenant ID as a string (optional).
            description: The new description for the credential (optional).

        Raises:
            SDKException: If the update operation fails or if the response is unsuccessful.

        Example:
            >>> credential = Credential(...)
            >>> credential.update_azure_app_credential(
            ...     app_secret="new_app_secret",
            ...     app_id="new_app_id",
            ...     tenant_id="new_tenant_id",
            ...     description="Updated Azure app registration credential"
            ... )
            >>> print("Azure application registration credential updated successfully")
        #ai-gen-doc
        """
        encoded_app_secret = b64encode(app_secret.encode()).decode()
        request_json = {
                          "accountType": "CLOUD_ACCOUNT",
                          "vendorType": "MICROSOFT_AZURE_TYPE",
                          "authType": "AZUREACCOUNT",
                          "name": self._credential_name,
                          "applicationId": app_id if app_id else self._credential_properties.get('applicationId'),
                          "tenantId": tenant_id if tenant_id else self._credential_properties.get('tenantId'),
                          "applicationSecret": encoded_app_secret,
                          "description": description if description else self._credential_properties.get('description'),
                          "environment": "AzureCloud",
                          "id": self.credential_id,
                          "newName": credential_name if credential_name else self._credential_name,
                          "endpoints": {
                            "activeDirectory": "https://login.microsoftonline.com/",
                            "storage": "blob.core.windows.net",
                            "resourceManager": "https://management.azure.com/"
                          }
                        }
        request = self._services['V5_CREDENTIAL'] % (self._credential_id)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', request, request_json
        )

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
