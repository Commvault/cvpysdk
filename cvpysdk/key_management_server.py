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

"""Main file for performing Key Management Server operations on commcell

This file has all the classes related to Key Management Server operations.

KeyManagementServerConstants --  Abstract class to define the key management server related  constancts

KeyManagementServers        --   Class for representing all the KMS in the commcell.

KeyManagementServer         --   Class for representing a single KMS in the commcell.


KeyManagementServerConstants Attributes
=======================================
    **_KMS_TYPE**           --    dictionary of key management server types
    **_KMS_AUTHENTICATION_TYPE** -- dictionary of key management server authentication
    

KeyManagementServers Attributes
==========================

    **_kms_dict**           --    a name-indexed dictionary of KeyManagementServer objects
    

KeyManagementServers:
=================

    __init__()              --      initializes KeyManagementServers class object

    _get_kms_dict()         --      fetches the dictionary of all Key Management Servers

    get()                   --      gets a specific Key Management Server object

    get_all_kms()           --      gets the dictionary of all Key Management Servers

    refresh()               --      refreshes the dictionary of Key Management Servers

    delete()                --      deletes a Key Management Server

    has_kms()               --      checks if the Key Management Server exists or not

    add_aws_kms()           --      configures AWS Key Management Server with key based authentication
    
    _add_aws_kms_with_cred_file() --  configures AWS KMS with credential file based authentication
    
    _add_aws_kms_with_iam() --      configures AWS KMS with IAM based authentication
    
    _add_azure_key_vault_certificate_auth() -- Configure Azure Key Management Server with AD-app certificate based authentication

    _add_azure_key_vault_iam_auth() -- Configure Azure Key Management Server with IAM managed identity based authentication
    
    _add_kmip_certificate()         --  Configure KMIP supported Key Management Server with certificate based authentication

    _add_passphrase_kms()           --  Configure Passphrase based Key Management Server
    
    _kms_api_call() --              call KMS API
    

KeyManagementServer:
=================

    __init__()              --      initializes KeyManagementServer class object

    _get_name_from_type()   --      returns the type name for type id
    
KeyManagementServer Attributes
==========================

    **name**                --    name of the Key Management Server
    **id**                  --    id of the Key Management Server
    **type_id**             --    type id of the Key Management Server
    **type_name**           --    type name of the Key Management Server

"""

import base64
from abc import ABC
from typing import Any, Dict, Optional

from .exception import SDKException

class KeyManagementServerConstants(ABC):
    """
    Abstract base class for key management server constants.

    This class serves as a foundation for defining and organizing constant values
    used in key management server implementations. It is intended to be subclassed
    by concrete classes that provide specific constant definitions relevant to
    key management operations.

    Key Features:
        - Abstract base class for key management server constants
        - Provides a structured approach for organizing constant values
        - Designed for extensibility in key management server implementations

    #ai-gen-doc
    """

    def __init__(self) -> None:
        """Initialize a new instance of the KeyManagementServerConstants class.

        This constructor sets up the constants required for key management server operations.

        Example:
            >>> kms_constants = KeyManagementServerConstants()
            >>> print(type(kms_constants))
            <class 'KeyManagementServerConstants'>
        #ai-gen-doc
        """
        self._KMS_TYPE = {
            1: "KEY_PROVIDER_COMMVAULT",
            2: "KEY_PROVIDER_KMIP",
            3: "KEY_PROVIDER_AWS_KMS",
            4: "KEY_PROVIDER_AZURE_KEY_VAULT",
            5: "KEY_PROVIDER_SAFENET",
            6: "KEY_PROVIDER_PASSPHRASE",
        }

        self._KMS_AUTHENTICATION_TYPE = {
            "AWS_KEYS": 0,
            "AWS_IAM": 1,
            "AWS_CREDENTIALS_FILE": 0,
            "AZURE_KEY_VAULT_CERTIFICATE": 1,
            "AZURE_KEY_VAULT_IAM": 3,
            "AZURE_KEY_VAULT_KEY": 2,
            "KMIP_CERTIFICATE": 99,
            "PASSPHRASE": 0
        }

class KeyManagementServers(KeyManagementServerConstants):
    """
    Represents and manages all Key Management Servers (KMS) within a Commcell environment.

    This class provides a comprehensive interface for interacting with various types of KMS,
    including AWS KMS, Azure Key Vault (with multiple authentication methods), and KMIP-based servers.
    It allows for adding, retrieving, validating, deleting, and refreshing KMS configurations,
    as well as checking for the existence of specific KMS instances.

    Key Features:
        - Retrieve and manage all KMS configurations in the Commcell
        - Add new KMS with support for AWS (via credentials or IAM), Azure Key Vault (key, certificate, or IAM auth), and KMIP certificate-based servers
        - Validate input parameters for KMS operations
        - Delete existing KMS by name
        - Check for the existence of a KMS by name
        - Refresh the internal KMS list to reflect current state
        - Internal utility methods for API calls and KMS dictionary management
        - String representation for easy inspection

    #ai-gen-doc
    """

    def __init__(self, commcell: object) -> None:
        """Initialize a KeyManagementServers class object.

        Args:
            commcell: An instance of the Commcell class representing the active Commcell connection.

        Example:

            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> kms = KeyManagementServers(commcell)
            >>> print("KeyManagementServers object created successfully")

        #ai-gen-doc
        """
        KeyManagementServerConstants.__init__(self)
        self._commcell = commcell

        self._cvpysdk_object = commcell._cvpysdk_object
        self._services = commcell._services

        self._KMS_ADD_GET = self._services['KEY_MANAGEMENT_SERVER_ADD_GET']
        self._KMS_DELETE = self._services['KEY_MANAGEMENT_SERVER_DELETE']
        self._kms_dict = None
        self.refresh()

    def _get_kms_dict(self) -> dict:
        """Retrieve a dictionary of all Key Management Servers indexed by their names.

        Returns:
            dict: A dictionary where each key is the name of a Key Management Server, and the value is 
            another dictionary containing the server's details such as 'name', 'id', and 'type_id'.
            Example structure:
                {
                    "kms_server1": {
                        "name": "kms_server1",
                        "id": 101,
                        "type_id": 1
                    },
                    "kms_server2": {
                        "name": "kms_server2",
                        "id": 102,
                        "type_id": 2
                    }
                }

        Raises:
            SDKException: If the list of Key Management Servers cannot be fetched.

        Example:
            >>> kms_mgr = KeyManagementServers()
            >>> kms_dict = kms_mgr._get_kms_dict()
            >>> for name, info in kms_dict.items():
            ...     print(f"KMS Name: {name}, ID: {info['id']}, Type ID: {info['type_id']}")

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._KMS_ADD_GET)

        if not flag:
            raise SDKException("Response", 101)

        if not response.json() or 'keyProviders' not in response.json():
            return {}

        key_providers = response.json()["keyProviders"]
        kms_dict = {}
        for key_provider in key_providers:
            type = key_provider.get("keyProviderType")
            
            provider = key_provider.get("provider")
            name = provider.get("keyProviderName", "").lower()
            id = provider.get("keyProviderId")
            
            kms_dict[name] = {
                "name": name,
                "id": id,
                "type_id": type,
            }

        return kms_dict
    
    def _validate_input(input_value: object, input_type: type, exception_id: int = 101) -> None:
        """Validate that the input value matches the specified type.

        Raises an SDKException if the input_value does not match the input_type.
        For the int type, input_value can be any value that is convertible to int.

        Args:
            input_value: The value to validate.
            input_type: The expected type to check against. For int, input_value can be int-convertible.
            exception_id: The exception ID to use if validation fails. Defaults to 101.

        Raises:
            SDKException: If input_value does not match input_type.

        Example:
            >>> KeyManagementServers._validate_input("123", int)
            >>> KeyManagementServers._validate_input(42, int)
            >>> # The following will raise SDKException:
            >>> KeyManagementServers._validate_input("abc", int)
        #ai-gen-doc
        """
        # if int, then try to convert and then check
        if input_type == int:
            try:
                input_value = int(input_value)
            except ValueError as e:
                pass
        
        if not isinstance(input_value, input_type):
            message = f"Received: {type(input_value)}. Expected: {input_type}"
            raise SDKException("KeyManagementServer", exception_id, message)
    
    def get(self, kms_name: str) -> 'KeyManagementServer':
        """Retrieve a specific Key Management Server object by name.

        Args:
            kms_name: The name of the Key Management Server to retrieve.

        Returns:
            KeyManagementServer: The object representing the specified Key Management Server.

        Raises:
            SDKException: If `kms_name` is not a string or if the specified Key Management Server is not found.

        Example:
            >>> kms_servers = KeyManagementServers()
            >>> kms = kms_servers.get("MyKMS")
            >>> print(f"Retrieved KMS: {kms}")

        #ai-gen-doc
        """
        if not self.has_kms(kms_name):
            raise SDKException("KeyManagementServer", 102)
        
        kms_info = self._kms_dict[kms_name.lower()]
        kms_obj = KeyManagementServer(self._commcell, kms_info['name'], kms_info['id'], kms_info['type_id'])
        return kms_obj


    def get_all_kms(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve a dictionary of all Key Management Servers (KMS) indexed by their names.

        Returns:
            A dictionary where each key is the name of a Key Management Server, and the value is another
            dictionary containing information about that server, such as its name, id, and type_id.

            Example structure:
                {
                    "kms_server1": {
                        "name": "kms_server1",
                        "id": 101,
                        "type_id": 1
                    },
                    "kms_server2": {
                        "name": "kms_server2",
                        "id": 102,
                        "type_id": 2
                    }
                }

        Example:
            >>> kms_mgr = KeyManagementServers()
            >>> all_kms = kms_mgr.get_all_kms()
            >>> print(f"Total KMS servers: {len(all_kms)}")
            >>> for name, info in all_kms.items():
            ...     print(f"KMS Name: {name}, ID: {info['id']}, Type ID: {info['type_id']}")

        #ai-gen-doc
        """
        return self._kms_dict

    def refresh(self) -> None:
        """Reload the dictionary of Key Management Servers.

        This method refreshes the internal cache of Key Management Servers, ensuring that 
        the latest information is retrieved and available for subsequent operations.

        Example:
            >>> kms = KeyManagementServers()
            >>> kms.refresh()
            >>> print("Key Management Servers have been refreshed.")

        #ai-gen-doc
        """
        self._kms_dict = self._get_kms_dict()

    def delete(self, kms_name: str) -> None:
        """Delete a Key Management Server by its name.

        This method removes the specified Key Management Server (KMS) from the system.

        Args:
            kms_name: The name of the Key Management Server to delete.

        Raises:
            SDKException: If the API response code is not successful, if the response JSON is empty,
                or if 'errorCode' is not present in the response JSON.

        Example:
            >>> kms_manager = KeyManagementServers()
            >>> kms_manager.delete("MyKMS")
            >>> print("Key Management Server deleted successfully.")

        #ai-gen-doc
        """
        if not self.has_kms(kms_name):
            raise SDKException('KeyManagementServer', 102)

        kms_id = self._kms_dict[kms_name.lower()]['id']

        kms_service = self._KMS_DELETE % (kms_id)
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', kms_service)

        if not flag:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException("Response", 101, response_string)

        if not response.json():
            raise SDKException("Response", 102)

        if "errorCode" not in response.json():
            raise SDKException(
                "Response", 101, f"Something went wrong while deleting {kms_name}")

        error_code = response.json()["errorCode"]
        if error_code != 0:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException("Response", 101, response_string)

        
    
    def has_kms(self, kms_name: str) -> bool:
        """Check if a Key Management Server (KMS) with the specified name exists.

        Args:
            kms_name: The name of the Key Management Server to check.

        Returns:
            True if the Key Management Server exists, False otherwise.

        Raises:
            SDKException: If `kms_name` is not a string.

        Example:
            >>> kms_manager = KeyManagementServers()
            >>> exists = kms_manager.has_kms("MyKMS")
            >>> print(f"KMS exists: {exists}")
            # Output: KMS exists: True

        #ai-gen-doc
        """
        KeyManagementServers._validate_input(kms_name, str)
        
        return kms_name.lower() in self._kms_dict
 

    def _add_aws_kms_with_cred_file(self, kms_details):
            """Configure AWS Key Management Server with credential file based authentication

                :arg
                    kms_details ( dictionary ) - Dictionary with AWS KMS details
                :return:
                    Object of KeyManagementServer class for the newly created KMS.
            """

            if "ACCESS_NODE_NAME" in kms_details:
                payload = {
                    "keyProvider": {

                        "provider": {
                            "keyProviderName": kms_details["KMS_NAME"]
                        },
                        "encryptionType": 3,
                        "keyProviderType": 3,

                        "properties": {
                            "accessNodes": [
                                {
                                    "accessNode": {
                                        "clientName": kms_details["ACCESS_NODE_NAME"]
                                    },
                                    "awsCredential": {
                                        "profile": kms_details["AWS_CREDENTIALS_FILE_PROFILE_NAME"],
                                        "amazonAuthenticationType": self._KMS_AUTHENTICATION_TYPE[kms_details["KEY_PROVIDER_AUTH_TYPE"]]
                                    }
                                }
                            ],
                            "bringYourOwnKey": 0,
                            "regionName": kms_details["AWS_REGION_NAME"]
                        }

                    }
                }

                self._kms_api_call(payload)


    def _add_aws_kms_with_iam(self, kms_details: dict) -> 'KeyManagementServer':
        """Configure an AWS Key Management Server (KMS) using IAM-based authentication.

        Args:
            kms_details: A dictionary containing the AWS KMS configuration details required for setup.

        Returns:
            KeyManagementServer: An instance representing the newly created AWS KMS.

        Example:
            >>> kms_details = {
            ...     "kms_name": "MyAWSKMS",
            ...     "region": "us-west-2",
            ...     "access_key": "AKIA...",
            ...     "secret_key": "abcd...",
            ...     "iam_role": "arn:aws:iam::123456789012:role/MyKMSRole"
            ... }
            >>> kms_server = key_mgmt_servers._add_aws_kms_with_iam(kms_details)
            >>> print(f"Created KMS: {kms_server}")

        #ai-gen-doc
        """

        if "ACCESS_NODE_NAME" in kms_details:

            payload= {
                        "keyProvider": {
	                    "provider": {
		                    "keyProviderName": kms_details["KMS_NAME"]
			            },
			        "encryptionType": 3,
			        "keyProviderType": 3,
			        "properties": {
				        "accessNodes": [
					        {
						        "accessNode": {
							        "clientName": kms_details["ACCESS_NODE_NAME"]
						        },
						        "awsCredential": {
							    "amazonAuthenticationType":1
						        }
					        }
				            ],
				            "bringYourOwnKey": 0,
				            "regionName": kms_details["AWS_REGION_NAME"]
			            }

		            }
                    }

            self._kms_api_call(payload)

    def _add_azure_key_vault_key_auth(self, kms_details: dict) -> 'KeyManagementServer':
        """Configure an Azure Key Management Server using AD-app key-based authentication.

        Args:
            kms_details: A dictionary containing the details required to configure the Azure Key Management Server.
                This should include authentication and connection parameters for the Azure Key Vault.

        Returns:
            KeyManagementServer: An object representing the newly created Azure Key Management Server.

        Example:
            >>> kms_details = {
            ...     "server_name": "my-azure-kms",
            ...     "client_id": "your-app-client-id",
            ...     "client_secret": "your-app-client-secret",
            ...     "tenant_id": "your-tenant-id",
            ...     "vault_url": "https://myvault.vault.azure.net/"
            ... }
            >>> kms_obj = key_mgmt_servers._add_azure_key_vault_key_auth(kms_details)
            >>> print(f"Created KMS: {kms_obj}")

        #ai-gen-doc
        """
        payload = None
        is_bring_your_own_key = 0
        keys = []
        
        if "AZURE_KEY_VAULT_KEY_LENGTH" not in kms_details:
            kms_details['AZURE_KEY_VAULT_KEY_LENGTH'] = 3072
        
        if "BringYourOwnKey" in kms_details:
            if kms_details["BringYourOwnKey"]:
                if "KEYS" not in kms_details:
                    raise SDKException('KeyManagementServer', 107)
                if type(kms_details['KEYS']) != list :
                    raise SDKException('Storage', 101)
                is_bring_your_own_key = 1
                for k in kms_details['KEYS']:
                    keys.append({"keyId": k})
                    
        if "ACCESS_NODE_NAME" in kms_details:
            payload= {
                        "keyProvider": {
                        "encryptionKeyLength": kms_details['AZURE_KEY_VAULT_KEY_LENGTH'],
                        "encryptionType": 1001,
                        "keyProviderType": 4,
                        "provider": {
                            "keyProviderName": kms_details['KMS_NAME']
                        },
                        "properties": {
                            "accessNodes": [
                            {
                                "accessNode": {
                                "clientName": kms_details['ACCESS_NODE_NAME']
                                },
                            "keyVaultCredential": {
                            "authType": self._KMS_AUTHENTICATION_TYPE[kms_details["KEY_PROVIDER_AUTH_TYPE"]],
                            "applicationId": kms_details['AZURE_APP_ID'],
                            "tenantId": kms_details['AZURE_TENANT_ID'],
                            "environment": "AzureCloud",
                            "endpoints": {
                                "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                                "keyVaultEndpoint": "vault.azure.net"
                            },
                        "certPassword": kms_details['AZURE_APP_SECRET'],
                        "overrideCredentials": True,
                        "resourceName": kms_details['AZURE_KEY_VAULT_NAME']
                        }
                        }
                        ],
                        "bringYourOwnKey": is_bring_your_own_key,
                         "keys": keys
                    }
                }
            }

            
        else:
            payload = {
                "keyProvider": {
                    "encryptionKeyLength": kms_details['AZURE_KEY_VAULT_KEY_LENGTH'],
                    "encryptionType": 1001,
                    "keyProviderType": 4,
                    "provider": {
                        "keyProviderName": kms_details['KMS_NAME']
                    },
                "properties": {
                    "keyVaultCredential": {
                    "authType": self._KMS_AUTHENTICATION_TYPE[kms_details["KEY_PROVIDER_AUTH_TYPE"]],
                    "applicationId": kms_details['AZURE_APP_ID'],
                    "tenantId": kms_details['AZURE_TENANT_ID'],
                    "resourceName": kms_details['AZURE_KEY_VAULT_NAME'],
                    "environment": "AzureCloud",
                    "endpoints": {
                    "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                    "keyVaultEndpoint": "vault.azure.net"
                    }
                    },
                "sslPassPhrase": kms_details['AZURE_APP_SECRET'],
                "bringYourOwnKey": is_bring_your_own_key,
                 "keys": keys
                }
                }
            }     

        self._kms_api_call(payload)
        
    
    def _add_azure_key_vault_certificate_auth(self, kms_details: dict) -> 'KeyManagementServer':
        """Configure an Azure Key Management Server using AD-app certificate-based authentication.

        Args:
            kms_details: Dictionary containing the details required to configure the Azure Key Vault 
                with certificate-based authentication. This should include parameters such as 
                client ID, tenant ID, certificate thumbprint, and other relevant Azure Key Vault settings.

        Returns:
            KeyManagementServer: An object representing the newly created Azure Key Management Server.

        Example:
            >>> kms_details = {
            ...     "client_id": "your-client-id",
            ...     "tenant_id": "your-tenant-id",
            ...     "certificate_thumbprint": "your-cert-thumbprint",
            ...     "vault_url": "https://your-keyvault.vault.azure.net/"
            ... }
            >>> kms_server = key_mgmt_servers._add_azure_key_vault_certificate_auth(kms_details)
            >>> print(f"Created KMS: {kms_server}")

        #ai-gen-doc
        """
        payload = None
        is_bring_your_own_key = 0
        keys = []

        if "AZURE_KEY_VAULT_KEY_LENGTH" not in kms_details:
            kms_details['AZURE_KEY_VAULT_KEY_LENGTH'] = 3072

        if "BringYourOwnKey" in kms_details:
            if kms_details["BringYourOwnKey"]:
                if "KEYS" not in kms_details:
                    raise SDKException('KeyManagementServer', 107)
                if type(kms_details['KEYS']) != list :
                    raise SDKException('Storage', 101)
                is_bring_your_own_key = 1
                for k in kms_details['KEYS']:
                    keys.append({"keyId": k})

        if "ACCESS_NODE_NAME" in kms_details:
            payload = {
                        "keyProvider": {
                            "provider": {
                            "keyProviderName": kms_details['KMS_NAME']
                            },
                            "encryptionKeyLength": kms_details['AZURE_KEY_VAULT_KEY_LENGTH'],
                            "encryptionType": 1001,
                            "keyProviderType": 4,
                            "properties": {
                                "accessNodes": [
                                {
                                    "keyVaultCredential": {
                                    "certificate": kms_details['AZURE_CERTIFICATE_PATH'],
                                    "resourceName": kms_details['AZURE_KEY_VAULT_NAME'],
                                    "environment": "AzureCloud",
                                    "certificateThumbprint": kms_details['AZURE_CERTIFICATE_THUMBPRINT'],
                                    "tenantId": kms_details['AZURE_TENANT_ID'],
                                    "authType": 1,
                                    "applicationId": kms_details['AZURE_APP_ID'],
                                    "endpoints": {
                                        "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                                        "keyVaultEndpoint": "vault.azure.net"
                                    },
                                    "certPassword": kms_details['AZURE_CERTIFICATE_PASSWORD']
                                    },
                                    "accessNode": {
                                        "clientName": kms_details['ACCESS_NODE_NAME']
                                    }
                                }
                                ],
                            "keyVaultCredential": {
                                "resourceName": kms_details['AZURE_KEY_VAULT_NAME']
                            },
                            "bringYourOwnKey": is_bring_your_own_key,
                            "keys": keys
                            }
                        }
                    }
        else:
            payload = {
                        "keyProvider": {
                            "provider": {
                            "keyProviderName": kms_details['KMS_NAME']
                            },
                            "encryptionKeyLength": kms_details['AZURE_KEY_VAULT_KEY_LENGTH'],
                            "encryptionType": 1001,
                            "keyProviderType": 4,
                            "properties": {
                                    "keyVaultCredential": {
                                    "certificate": kms_details['AZURE_CERTIFICATE_PATH'],
                                    "resourceName": kms_details['AZURE_KEY_VAULT_NAME'],
                                    "environment": "AzureCloud",
                                    "certificateThumbprint": kms_details['AZURE_CERTIFICATE_THUMBPRINT'],
                                    "tenantId": kms_details['AZURE_TENANT_ID'],
                                    "authType": 1,
                                    "applicationId":kms_details['AZURE_APP_ID'],
                                    "endpoints": {
                                        "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                                        "keyVaultEndpoint": "vault.azure.net"
                                    }
                                    },
                            "bringYourOwnKey": 0,
                            "sslPassPhrase": kms_details['AZURE_CERTIFICATE_PASSWORD']
                            }
                        }
                      }

        self._kms_api_call(payload)



    def add(self, kms_details: dict) -> None:
        """Add a new Key Management Server (KMS) configuration.

        This method registers a new Key Management Server (KMS) with the system using the provided
        configuration details. The `kms_details` dictionary must specify the KMS type, authentication
        method, and all required parameters for the chosen KMS provider (AWS, Azure, or KMIP).
        Optional parameters and advanced features such as "Bring Your Own Key" are also supported.

        The structure of `kms_details` varies depending on the KMS provider and authentication type.
        See the examples below for supported configurations.

        Args:
            kms_details: Dictionary containing the KMS configuration details. The required and optional
                keys depend on the KMS provider and authentication method. Example configurations:

                - AWS KMS (key-based authentication, no access node):
                    {
                        "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AWS_KMS",
                        "KMS_NAME": "KMS1",
                        "AWS_ACCESS_KEY": "",
                        "AWS_SECRET_KEY": "",
                        "AWS_REGION_NAME": "Asia Pacific (Mumbai)",  # Optional, default is "Asia Pacific (Mumbai)"
                        "KEY_PROVIDER_AUTH_TYPE": "AWS_KEYS"
                    }

                - Azure Key Vault (certificate-based authentication, with access node):
                    {
                        "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                        "ACCESS_NODE_NAME": "",
                        "KMS_NAME": "",
                        "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_CERTIFICATE",
                        "AZURE_KEY_VAULT_KEY_LENGTH": 2048,  # Optional, default is 3072
                        "AZURE_KEY_VAULT_NAME": "",
                        "AZURE_TENANT_ID": "",
                        "AZURE_APP_ID": "",
                        "AZURE_CERTIFICATE_PATH": "",
                        "AZURE_CERTIFICATE_THUMBPRINT": "",
                        "AZURE_CERTIFICATE_PASSWORD": ""  # Base64 encoded
                    }

                - KMIP KMS (certificate-based authentication):
                    {
                        "KEY_PROVIDER_TYPE": "KEY_PROVIDER_KMIP",
                        "ACCESS_NODE_NAME": "",
                        "KMS_NAME": "",
                        "KEY_PROVIDER_AUTH_TYPE": "KMIP_CERTIFICATE",
                        "KMIP_CERTIFICATE_PATH": "",
                        "KMIP_CERTIFICATE_KEY_PATH": "",
                        "KMIP_CA_CERTIFICATE_PATH": "",
                        "KMIP_CERTIFICATE_PASS": "",  # Base64 encoded
                        "KMIP_HOST": "",
                        "KMIP_PORT": "",
                        "KMIP_ENC_KEY_LENGTH": 256  # Optional, default is 256
                    }

                - Bring Your Own Key (BYOK) for Azure Key Vault:
                    {
                        "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                        "KMS_NAME": "MyKMS",
                        "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_KEY",
                        "AZURE_KEY_VAULT_KEY_LENGTH": 2072,
                        "AZURE_KEY_VAULT_NAME": "",
                        "AZURE_TENANT_ID": "",
                        "AZURE_APP_ID": "",
                        "AZURE_APP_SECRET": "",  # Base64 encoded
                        "BringYourOwnKey": True,
                        "KEYS": ["KeyID1/KeyVersion1", "KeyID2/KeyVersion2"]
                    }

        Example:
            >>> kms_mgr = KeyManagementServers()
            >>> kms_details = {
            ...     "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AWS_KMS",
            ...     "KMS_NAME": "MyAWSKMS",
            ...     "AWS_ACCESS_KEY": "AKIA...",
            ...     "AWS_SECRET_KEY": "secret",
            ...     "AWS_REGION_NAME": "US East (Ohio)",
            ...     "KEY_PROVIDER_AUTH_TYPE": "AWS_KEYS"
            ... }
            >>> kms_mgr.add(kms_details)
            >>> print("KMS added successfully.")

        #ai-gen-doc
        """
        
        KeyManagementServers._validate_input(kms_details, dict)

        if kms_details['KEY_PROVIDER_TYPE'] not in self._KMS_TYPE.values():
            raise SDKException("KeyManagementServer", 103)

        if kms_details['KEY_PROVIDER_AUTH_TYPE'] not in self._KMS_AUTHENTICATION_TYPE:
            raise SDKException("KeyManagementServer", 105)

        if "KMS_NAME" not in kms_details:
            raise SDKException("KeyManagementServer", 106)



        if kms_details['KEY_PROVIDER_TYPE'] == "KEY_PROVIDER_AWS_KMS":
            if "AWS_REGION_NAME" not in kms_details:
                kms_details["AWS_REGION_NAME"] = "Asia Pacific (Mumbai)"

            if kms_details['KEY_PROVIDER_AUTH_TYPE'] == "AWS_KEYS":
                self.add_aws_kms(kms_name=kms_details['KMS_NAME'], aws_access_key=kms_details['AWS_ACCESS_KEY'], aws_secret_key=kms_details['AWS_SECRET_KEY'],aws_region_name=kms_details["AWS_REGION_NAME"], kms_details = kms_details)

            elif kms_details['KEY_PROVIDER_AUTH_TYPE'] == "AWS_CREDENTIALS_FILE":
                self._add_aws_kms_with_cred_file(kms_details)

            elif kms_details['KEY_PROVIDER_AUTH_TYPE'] == "AWS_IAM":
                self._add_aws_kms_with_iam(kms_details)

        if kms_details['KEY_PROVIDER_TYPE'] == "KEY_PROVIDER_AZURE_KEY_VAULT":
            if kms_details['KEY_PROVIDER_AUTH_TYPE'] == "AZURE_KEY_VAULT_CERTIFICATE":
                self._add_azure_key_vault_certificate_auth(kms_details)

            elif kms_details['KEY_PROVIDER_AUTH_TYPE'] == "AZURE_KEY_VAULT_IAM":
                self._add_azure_key_vault_iam_auth(kms_details)
            
            elif kms_details['KEY_PROVIDER_AUTH_TYPE'] == "AZURE_KEY_VAULT_KEY":
                self._add_azure_key_vault_key_auth(kms_details)

        if kms_details['KEY_PROVIDER_TYPE'] == "KEY_PROVIDER_KMIP":
            self._add_kmip_certificate(kms_details)

        if kms_details['KEY_PROVIDER_TYPE'] == "KEY_PROVIDER_PASSPHRASE":
            self._add_passphrase_kms(kms_details)
            
        return self.get(kms_details['KMS_NAME'])


    def _add_kmip_certificate(self, kms_details: dict) -> None:
        """Configure a KMIP Key Management Server using certificate-based authentication.

        Args:
            kms_details: A dictionary containing the details required to configure the KMIP KMS,
                such as server address, port, certificate paths, and authentication parameters.

        Example:
            >>> kms_details = {
            ...     "server_name": "kmip-server01",
            ...     "port": 5696,
            ...     "certificate_path": "/path/to/cert.pem",
            ...     "private_key_path": "/path/to/key.pem"
            ... }
            >>> kms_manager = KeyManagementServers()
            >>> kms_manager._add_kmip_certificate(kms_details)
            >>> print("KMIP KMS configured with certificate authentication.")

        #ai-gen-doc
        """
        
        if "KMIP_ENC_KEY_LENGTH" not in kms_details:
            kms_details["KMIP_ENC_KEY_LENGTH"] = 256
            payload = None

        if "ACCESS_NODE_NAME" in kms_details:

                payload = {
                        "keyProvider": {
                        "encryptionKeyLength": kms_details["KMIP_ENC_KEY_LENGTH"],
                        "encryptionType": 3,
                        "keyProviderType": 2,
                        "provider": {
                            "keyProviderName": kms_details["KMS_NAME"]
                        },
                        "properties": {
                            "bringYourOwnKey": "0",
                            "host": kms_details["KMIP_HOST"],
                            "port": int(kms_details["KMIP_PORT"]),
                            "accessNodes": [
                                {
                                "accessNode": {
                                    "clientName": kms_details["ACCESS_NODE_NAME"]
                                },
                                "kmipCredential": {
                                    "caCertFilePath": kms_details["KMIP_CA_CERTIFICATE_PATH"],
                                    "certFilePath": kms_details["KMIP_CERTIFICATE_PATH"],
                                    "certPassword": kms_details["KMIP_CERTIFICATE_PASS"],
                                    "keyFilePath": kms_details["KMIP_CERTIFICATE_KEY_PATH"]
                                }
                                }
                            ]
                        }
                        }
                        }

        else:
                payload = {
                    "keyProvider": {
                        "provider": {
                            "keyProviderName": kms_details['KMS_NAME']
                        },
                        "encryptionKeyLength": kms_details['KMIP_ENC_KEY_LENGTH'],
                        "encryptionType": 3,
                        "keyProviderType": 2,
                        "properties": {
                            "caCertFilePath": kms_details['KMIP_CA_CERTIFICATE_PATH'],
                            "certFilePath": kms_details['KMIP_CERTIFICATE_PATH'],
                            "certPassword": kms_details['KMIP_CERTIFICATE_PASS'],
                            "keyFilePath": kms_details['KMIP_CERTIFICATE_KEY_PATH'],
                            "bringYourOwnKey": 0,
                            "host": kms_details['KMIP_HOST'],
                            "port": int(kms_details['KMIP_PORT'])
                        }
                    }
                }
                
        self._kms_api_call(payload)


    def _add_azure_key_vault_iam_auth(self, kms_details: Dict[str, Any]) -> 'KeyManagementServer':
        """Configure an Azure Key Management Server using IAM-based authentication.

        Args:
            kms_details: Dictionary containing the configuration details required for Azure Key Vault IAM authentication.

        Returns:
            KeyManagementServer: An object representing the newly created Azure Key Management Server.

        Example:
            >>> kms_details = {
            ...     "vault_name": "myKeyVault",
            ...     "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            ...     "client_id": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
            ...     "subscription_id": "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"
            ... }
            >>> kms_server = key_mgmt_servers._add_azure_key_vault_iam_auth(kms_details)
            >>> print(f"Created KMS: {kms_server}")

        #ai-gen-doc
        """

        if "AZURE_KEY_VAULT_KEY_LENGTH" not in kms_details:
            kms_details['AZURE_KEY_VAULT_KEY_LENGTH'] = 3072

        if "ACCESS_NODE_NAME" in kms_details:
            payload = {
                        "keyProvider": {
                            "provider": {
                                "keyProviderName": kms_details['KMS_NAME']
                            },
                            "encryptionKeyLength": kms_details['AZURE_KEY_VAULT_KEY_LENGTH'],
                            "encryptionType": 1001,
                            "keyProviderType": 4,
                            "properties": {
                                "accessNodes": [
                                {
                                    "keyVaultCredential": {
                                    "environment": "AzureCloud",
                                    "authType": self._KMS_AUTHENTICATION_TYPE[kms_details['KEY_PROVIDER_AUTH_TYPE']],
                                    "resourceName": kms_details['AZURE_KEY_VAULT_NAME'],
                                    "endpoints": {
                                        "activeDirectoryEndpoint": "https://login.microsoftonline.com/",
                                        "keyVaultEndpoint": "vault.azure.net"
                                        }
                                    },
                                    "accessNode": {
                                    "clientName": kms_details['ACCESS_NODE_NAME']
                                }
                                }
                                ],
                                "keyVaultCredential": {
                                    "resourceName": kms_details['AZURE_KEY_VAULT_NAME']
                                },
                                "bringYourOwnKey": 0
                                }
                            }
                        }

            self._kms_api_call(payload)


    def add_aws_kms(
        self,
        kms_name: str,
        aws_access_key: str,
        aws_secret_key: str,
        aws_region_name: Optional[str] = None,
        kms_details: Optional[dict] = None
    ) -> None:
        """Configure an AWS Key Management Server (KMS) for use with the system.

        This method registers a new AWS KMS by providing the required credentials and optional configuration details.

        Args:
            kms_name: The name to assign to the Key Management Server.
            aws_access_key: The AWS access key for authentication.
            aws_secret_key: The AWS secret key (base64 encoded) for authentication.
            aws_region_name: The AWS region name. If not specified, defaults to "Asia Pacific (Mumbai)".
            kms_details: Optional dictionary containing additional AWS KMS configuration details.

        Raises:
            SDKException: If any input is of the wrong data type, if the API response is unsuccessful,
                if the API response JSON is empty, or if the error code in the API response JSON is not 0.

        Example:
            >>> kms_mgr = KeyManagementServers()
            >>> kms_mgr.add_aws_kms(
            ...     kms_name="MyAWSKMS",
            ...     aws_access_key="AKIAIOSFODNN7EXAMPLE",
            ...     aws_secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            ...     aws_region_name="us-west-2",
            ...     kms_details={"description": "Production AWS KMS"}
            ... )
            >>> print("AWS KMS configured successfully")
        #ai-gen-doc
        """

        KeyManagementServers._validate_input(kms_name, str)

        payload = None
        is_bring_your_own_key = 0
        keys = []

        if "BringYourOwnKey" in kms_details:
            if kms_details.get("BringYourOwnKey"):
                if "KEYS" not in kms_details:
                    raise SDKException('KeyManagementServer', 107)
                if type(kms_details['KEYS']) != list :
                    raise SDKException('Storage', 101)
                is_bring_your_own_key = 1
                for k in kms_details['KEYS']:
                    keys.append({"keyId": k})

        if kms_details == None or "ACCESS_NODE_NAME" not in kms_details:

            if aws_region_name is None:
                aws_region_name = "Asia Pacific (Mumbai)"

            KeyManagementServers._validate_input(aws_access_key, str)
            KeyManagementServers._validate_input(aws_secret_key, str)
            KeyManagementServers._validate_input(aws_region_name, str)

            payload = {
                "keyProvider": {
                    "encryptionType": 3,
                    "keyProviderType": 3,
                    "provider": {
                        "keyProviderName": kms_name
                    },
                    "properties": {
                        "regionName": aws_region_name,
                        "userAccount": {
                            "userName": aws_access_key,
                            "password": aws_secret_key
                        }
                    }
                }
            }

        elif kms_details['KEY_PROVIDER_AUTH_TYPE'] == "AWS_KEYS" and kms_details['ACCESS_NODE_NAME'] != None:

            if "AWS_REGION_NAME" not in kms_details:
                kms_details['AWS_REGION_NAME'] = "Asia Pacific (Mumbai)"

            KeyManagementServers._validate_input(aws_access_key, str)
            KeyManagementServers._validate_input(aws_secret_key, str)
            KeyManagementServers._validate_input(aws_region_name, str)

            payload = {
		            "keyProvider": {
			            "properties": {
				            "accessNodes": [
					        {
						        "accessNode": {
							        "clientName": kms_details['ACCESS_NODE_NAME']
						        },
						        "awsCredential": {
							        "userAccount": {
								        "password": aws_secret_key,
								        "userName": aws_access_key
							        },
							    "amazonAuthenticationType": self._KMS_AUTHENTICATION_TYPE[kms_details['KEY_PROVIDER_AUTH_TYPE']]
						        }
					        }
				            ],
				            "bringYourOwnKey": str(is_bring_your_own_key),
                            "keys": keys,
				            "regionName": aws_region_name if aws_region_name!=None else kms_details['AWS_REGION_NAME']
			            },
			            "provider": {
				            "keyProviderName": kms_name
			            },
			            "encryptionType": 3,
			            "keyProviderType": "3"
		            }
                }

        self._kms_api_call(payload)
        

    def _add_passphrase_kms(self, kms_details: dict) -> None:
        """Configure a Passphrase-based Key Management Server.

        Args:
            kms_details: A dictionary containing the passphrase KMS configuration details.

                Required keys:
                    - KMS_NAME (str): Name of the Key Management Server.
                    - PASSPHRASE (str): Plain-text passphrase.
                    - PASSPHRASE_CLIENTS (list): List of dicts, each with:
                        - clientName (str): Client hostname/name.
                        - filePath (str): Path on the client where the passphrase file is stored.

                Optional keys:
                    - ENCRYPTION_KEY_LENGTH (int): Encryption key length in bits. Defaults to 256.

        Raises:
            SDKException: If required keys are missing or if the API call fails.

        Example:
            >>> kms_details = {
            ...     "KEY_PROVIDER_TYPE": "KEY_PROVIDER_PASSPHRASE",
            ...     "KEY_PROVIDER_AUTH_TYPE": "PASSPHRASE",
            ...     "KMS_NAME": "test",
            ...     "PASSPHRASE": "test123",
            ...     "ENCRYPTION_KEY_LENGTH": 256,
            ...     "PASSPHRASE_CLIENTS": [
            ...         {
            ...             "clientName": "commserve client name",
            ...             "filePath": "/usr/test1"
            ...         }
            ...     ]
            ... }
            >>> kms_mgr.add(kms_details)

        #ai-gen-doc
        """
        for required_key in ("KMS_NAME", "PASSPHRASE", "PASSPHRASE_CLIENTS"):
            if required_key not in kms_details:
                raise SDKException(
                    "KeyManagementServer", 101,
                    f"Missing required key '{required_key}' in kms_details for PASSPHRASE KMS."
                )

        enc_key_length = kms_details.get("ENCRYPTION_KEY_LENGTH", 256)
        passphrase_b64 = base64.b64encode(kms_details["PASSPHRASE"].encode("utf-8")).decode("utf-8")

        passphrase_client_list = []
        for client_entry in kms_details["PASSPHRASE_CLIENTS"]:
            passphrase_client_list.append(
                {
                    "client": {
                        "clientName": client_entry["clientName"]
                    },
                    "filePath": {
                        "path": client_entry["filePath"]
                    }
                }
            )

        payload = {
            "keyProvider": {
                "encryptionKeyLength": enc_key_length,
                "encryptionType": 3,
                "keyProviderType": 6,
                "properties": {
                    "passphrase": passphrase_b64,
                    "passphraseClient": passphrase_client_list
                },
                "provider": {
                    "keyProviderName": kms_details["KMS_NAME"]
                }
            },
            "useSaveLabel": True
        }

        self._kms_api_call(payload)

    def _kms_api_call(self, payload: dict) -> dict:
        """Call the Key Management Server (KMS) API with the specified payload.

        This method sends a prefilled JSON payload to the KMS API and returns the response as a dictionary.

        Args:
            payload: A dictionary representing the JSON payload to be sent to the KMS API.

        Returns:
            A dictionary containing the response from the KMS API.

        Raises:
            SDKException: If the API response code is not successful, if the response JSON is empty,
                or if 'errorCode' is not present in the response JSON.

        Example:
            >>> kms_servers = KeyManagementServers()
            >>> payload = {"operation": "getKey", "keyId": "12345"}
            >>> response = kms_servers._kms_api_call(payload)
            >>> print(response)
            {'key': 'abcdef123456', 'status': 'success'}

        #ai-gen-doc
        """
    
        KeyManagementServers._validate_input(payload, dict)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._KMS_ADD_GET, payload)

        if not flag:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException("Response", 101, response_string)

        if not response.json():
            raise SDKException("Response", 102)

        error_code = response.json().get("errorCode", -1)

        if error_code != 0:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException("Response", 101, response_string)
        
        self.refresh()
        
    def __str__(self) -> str:
        """Return a string representation of all Key Management Servers (KMS) associated with the Commcell.

        Returns:
            A string listing all KMS configured in the Commcell.

        Example:
            >>> kms_servers = KeyManagementServers(commcell_object)
            >>> print(str(kms_servers))
            >>> # Output will display a summary of all KMS associated with the Commcell

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'KMS')

        for index, client in enumerate(self._kms_dict):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, client)
            representation_string += sub_str

        return representation_string.strip()
    
    def __repr__(self) -> str:
        """Return the string representation of the KeyManagementServers instance.

        This method provides a developer-friendly string that represents the current
        KeyManagementServers object, useful for debugging and logging purposes.

        Returns:
            A string representation of the KeyManagementServers instance.

        Example:
            >>> kms = KeyManagementServers()
            >>> print(repr(kms))
            <KeyManagementServers object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        return "KeyManagementServers class instance for Commcell"

class KeyManagementServer(object):
    """
    Represents a single Key Management Server (KMS) within a CommCell environment.

    This class encapsulates the properties and behaviors associated with a KMS,
    including initialization with specific identifiers and types, and internal
    utilities for resolving KMS type names from type IDs. It is designed to be
    used as part of the CommCell's key management infrastructure.

    Key Features:
        - Initialization with CommCell context, KMS name, ID, and type ID
        - Internal method to retrieve KMS type name from a type ID
        - Provides a string representation for debugging and logging

    #ai-gen-doc
    """

    def __init__(self, commcell: object, name: str, id: int, type_id: int) -> None:
        """Initialize a KeyManagementServer object.

        Args:
            commcell: Instance of the Commcell class representing the connected Commcell environment.
            name: The name of the Key Management Server.
            id: The unique identifier for the Key Management Server.
            type_id: The type identifier for the Key Management Server.

        Raises:
            SDKException: If any parameter is of an invalid type.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> kms = KeyManagementServer(commcell, 'KMS-Server1', 101, 2)
            >>> print(f"Key Management Server '{kms.name}' initialized with ID {kms.id}")

        #ai-gen-doc
        """
        KeyManagementServerConstants.__init__(self)
        self._commcell = commcell
        self._cvpysdk_object = commcell._cvpysdk_object
        self._services = commcell._services

        KeyManagementServers._validate_input(name, str)
        self.name = name

        KeyManagementServers._validate_input(id, int)
        self.id = int(id)

        KeyManagementServers._validate_input(type_id, int, 103)
        self.type_id = int(type_id)

        self.type_name = self._get_name_from_type(type_id)
    
    def _get_name_from_type(self, type_id: int) -> str:
        """Get the type name corresponding to a given Key Management Server type ID.

        Args:
            type_id: The integer type ID of the Key Management Server.

        Returns:
            The type name as a string corresponding to the provided type ID.

        Raises:
            SDKException: If type_id cannot be converted to an integer or if an unknown type_id is provided.

        Example:
            >>> kms = KeyManagementServer()
            >>> type_name = kms._get_name_from_type(2)
            >>> print(f"Type name for ID 2: {type_name}")
            >>> # If an invalid type_id is provided, SDKException will be raised

        #ai-gen-doc
        """
        KeyManagementServers._validate_input(type_id, int, 103)
        type_id = int(type_id)

        if type_id not in self._KMS_TYPE:
            raise SDKException("KeyManagementServer", 104)
        
        return self._KMS_TYPE[type_id]
    
    def __repr__(self) -> str:
        """Return the string representation of the KeyManagementServer instance.

        This method provides a developer-friendly string that represents the current
        KeyManagementServer object, which can be useful for debugging and logging.

        Returns:
            A string representation of the KeyManagementServer instance.

        Example:
            >>> kms = KeyManagementServer()
            >>> print(repr(kms))
            <KeyManagementServer object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        representation_string = 'KeyServerManagement class instance for: "{0}"'
        return representation_string.format(self.name)