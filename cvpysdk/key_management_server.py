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

from .exception import SDKException
from abc import ABC


class KeyManagementServerConstants(ABC):

    def __init__(self):
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
            "KMIP_CERTIFICATE": 99
        }

class KeyManagementServers(KeyManagementServerConstants):
    """Class for representing all the KMS in the commcell."""

    def __init__(self, commcell):
        """Initializes KeyManagementServers class object

            Args:
                commcell    (object)    --  instance of commcell

        """
        KeyManagementServerConstants.__init__(self)
        self._commcell = commcell

        self._cvpysdk_object = commcell._cvpysdk_object
        self._services = commcell._services

        self._KMS_ADD_GET = self._services['KEY_MANAGEMENT_SERVER_ADD_GET']
        self._KMS_DELETE = self._services['KEY_MANAGEMENT_SERVER_DELETE']
        self._kms_dict = None
        self.refresh()

    def _get_kms_dict(self):
        """Fetches the name-indexed dictionary of all Key Management Servers

            Returns:
                the name-indexed dictionary of Key Management Server info
                {
                    name1: {
                       name: name1, 
                       id: id1,
                       type_id: type_id1,
                    },
                    ...
                }

            Raises SDKException:
                    If failed to fetch the list
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
    
    def _validate_input(input_value, input_type, exception_id=101):
        """Raises SDKException if input_value doesn't match input_type
        
            Args:
                input_value     (any)   --  The value to check

                input_type      (type)  --  The type to check against.
                                            For int type, the input can be int-convertible

                exception_id    (int)   --  The exception id to throw
                                            defaults to 101

            Raises SDKException:
                If type mismatch was found
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
    
    def get(self, kms_name):
        """Gets a specific Key Management Server object
        
            Args:
                kms_name    (str)       -- The Key Management Server to get

            Returns:
                kms         (object)    --  The KeyManagementServer object
            
            Raises SDKException:
                If kms_name is not str

                If Key Management Server not found
        """      
        if not self.has_kms(kms_name):
            raise SDKException("KeyManagementServer", 102)
        
        kms_info = self._kms_dict[kms_name.lower()]
        kms_obj = KeyManagementServer(self._commcell, kms_info['name'], kms_info['id'], kms_info['type_id'])
        return kms_obj


    def get_all_kms(self):
        """Gets the name-indexed dictionary of all Key Management Servers

            Returns:
                the name-indexed dictionary of Key Management Server info
                {
                    name1: {
                       name: name1, 
                       id: id1,
                       type_id: type_id1,
                    },
                    ...
                }
                
        """
        return self._kms_dict

    def refresh(self):
        """Refreshes the dictionary of Key Management Servers"""
        self._kms_dict = self._get_kms_dict()

    def delete(self, kms_name):
        """Deletes a Key Management Server

            Args:
                kms_name (string) -- name of the Key Management Server

            Raises SDKException:
                    If API response code is not successfull

                    If response JSON is empty

                    If errorCode is not part of the response JSON
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

        
    
    def has_kms(self, kms_name):
        """Check if the Key Management Server exist or not

            Args:
                kms_name    (str)   -- name of the Key Management Server

            Returns:
                result      (bool)  -- whether Key Management Server exists or not
            
            Raises SDKException:
                If kms_name is not string
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


    def _add_aws_kms_with_iam(self, kms_details):
        """Configure AWS Key Management Server with IMA based authentication

            :arg
                kms_details ( dictionary ) - Dictionary with AWS KMS details
            :return:
                Object of KeyManagementServer class for the newly created KMS.
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

    def _add_azure_key_vault_key_auth(self, kms_details):
        """Configure Azure Key Management Server with AD-app key based authentication

            :arg
                kms_details ( dictionary ) - Dictionary with AWS KMS details
            :return:
                Object of KeyManagementServer class for the newly created KMS.
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
        
    
    def _add_azure_key_vault_certificate_auth(self, kms_details):
        """Configure Azure Key Management Server with AD-app certificate based authentication

            :arg
                kms_details ( dictionary ) - Dictionary with AWS KMS details
            :return:
                Object of KeyManagementServer class for the newly created KMS.
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



    def add(self, kms_details):
        """
        Method to add Key Management Server

        Args:
                kms_details    (dictionary)   -- dictionary with KMS details

        input dictionary for creating AWS KMS without access node ( key based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AWS_KMS",
                "KMS_NAME": "KMS1" ,
                "AWS_ACCESS_KEY":"",
                "AWS_SECRET_KEY": "",
                "AWS_REGION_NAME": "Asia Pacific (Mumbai)",  -- Optional Value. Default is "Asia Pacific (Mumbai)"
                "KEY_PROVIDER_AUTH_TYPE": "AWS_KEYS"
            }

        input dictionary for creating AWS KMS with access node ( key based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AWS_KMS",
                "AWS_REGION_NAME": "US East (Ohio)",    -- Optional Value. Default is "Asia Pacific (Mumbai)"
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "",
                "KEY_PROVIDER_AUTH_TYPE": "",
                "AWS_ACCESS_KEY": "",
                "AWS_SECRET_KEY": ""     -- Base64 encoded
            }
            
        input dictionary for creating AWS KMS with access node ( key based authentication ) and by enabling Bring Your Own Key.
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AWS_KMS",
                "AWS_REGION_NAME": "US East (Ohio)",    -- Optional Value. Default is "Asia Pacific (Mumbai)"
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "",
                "KEY_PROVIDER_AUTH_TYPE": "AWS_KEYS",
                "AWS_ACCESS_KEY": "",
                "AWS_SECRET_KEY": "",     -- Base64 encoded
                "BringYourOwnKey": True,
                "KEYS": []
            }

        input dictionary for creating AWS KMS with access node ( credential template file based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AWS_KMS",
                "AWS_REGION_NAME": "US East (Ohio)",    -- Optional Value. Default is "Asia Pacific (Mumbai)"
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "AWS_KMS_NAME",
                "KEY_PROVIDER_AUTH_TYPE": "AWS_CREDENTIALS_FILE",
                "AWS_CREDENTIALS_FILE_PROFILE_NAME": ""
            }

        input dictionary for creating AWS KMS with access Node ( IAM based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AWS_KMS",
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "",
                "KEY_PROVIDER_AUTH_TYPE": "AWS_IAM"
            }
            
        

        input dictionary for creating Azure KMS with access Node ( certificate based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "",
                "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_CERTIFICATE",
                "AZURE_KEY_VAULT_KEY_LENGTH":2048,     -- Optional Value. Default is 3072
                "AZURE_KEY_VAULT_NAME":"",
                "AZURE_TENANT_ID":"",
                "AZURE_APP_ID":"",
                "AZURE_CERTIFICATE_PATH":"",
                "AZURE_CERTIFICATE_THUMBPRINT":"",
                "AZURE_CERTIFICATE_PASSWORD": "",    -- Base64 encoded
            }

        input dictionary for creating Azure KMS with access Node ( IAM managed identity based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "",
                "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_IAM",
                "AZURE_KEY_VAULT_NAME":"",
            }

        input dictionary for creating Azure KMS without access Node ( certificate based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                "KMS_NAME": "",
                "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_CERTIFICATE",
                "AZURE_KEY_VAULT_NAME":"",
                "AZURE_TENANT_ID": "",
                "AZURE_APP_ID": "",
                "AZURE_CERTIFICATE_PATH": "",
                "AZURE_CERTIFICATE_THUMBPRINT": "",
                "AZURE_CERTIFICATE_PASSWORD": "",    -- Base64 encoded
            }
            
        input dictionary for creating KMIP KMS with access Node ( certificate based authentication )
            kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_KMIP",
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "",
                "KEY_PROVIDER_AUTH_TYPE": "KMIP_CERTIFICATE",
                "KMIP_CERTIFICATE_PATH": "",
                "KMIP_CERTIFICATE_KEY_PATH": "",
                "KMIP_CA_CERTIFICATE_PATH": "",
                "KMIP_CERTIFICATE_PASS": "", -- Base64 encoded
                "KMIP_HOST": "",
                "KMIP_PORT": "",
                "KMIP_ENC_KEY_LENGTH":256           -- Optional Value. Default is 256
            }

        input dictionary for Azure KMS with access Node ( certificate based authentication ) with Bring Your Own Key enabled
            self.kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "MyKMS",
                "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_CERTIFICATE",
                "AZURE_KEY_VAULT_KEY_LENGTH": 2072,
                "AZURE_KEY_VAULT_NAME": "",
                "AZURE_TENANT_ID": "",
                "AZURE_APP_ID": "",
                "AZURE_CERTIFICATE_PATH": "",
                "AZURE_CERTIFICATE_THUMBPRINT": "",
                "AZURE_CERTIFICATE_PASSWORD": "",    -- Base64 encoded
                "BringYourOwnKey": True,
                "KEYS": ["KeyID1/KeyVersion1", "KeyID2/KeyVersion2", "KeyID3/KeyVersion3"]
            }
            
        input dictionary for Azure KMS with access Node ( AD APp based authentication ) with Bring Your Own Key enabled
            self.kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                "ACCESS_NODE_NAME": "",
                "KMS_NAME": "MyKMS",
                "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_KEY",
                "AZURE_KEY_VAULT_KEY_LENGTH": 2072,
                "AZURE_KEY_VAULT_NAME": "",
                "AZURE_TENANT_ID": "",
                "AZURE_APP_ID": "",
                "AZURE_APP_SECRET": "", -- Base64 encoded
                "BringYourOwnKey": True,
                "KEYS": ["KeyID1/KeyVersion1", "KeyID2/KeyVersion2", "KeyID3/KeyVersion3"]
            }
        
        input dictionary for Azure KMS without access Node ( AD APp based authentication ) with Bring Your Own Key enabled
            self.kms_details = {
                "KEY_PROVIDER_TYPE": "KEY_PROVIDER_AZURE_KEY_VAULT",
                "KMS_NAME": "MyKMS",
                "KEY_PROVIDER_AUTH_TYPE": "AZURE_KEY_VAULT_KEY",
                "AZURE_KEY_VAULT_KEY_LENGTH": 2072,
                "AZURE_KEY_VAULT_NAME": "",
                "AZURE_TENANT_ID": "",
                "AZURE_APP_ID": "",
                "AZURE_APP_SECRET": "", -- Base64 encoded
                "BringYourOwnKey": True,
                "KEYS": ["KeyID1/KeyVersion1", "KeyID2/KeyVersion2", "KeyID3/KeyVersion3"]
            }
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
            
        return self.get(kms_details['KMS_NAME'])


    def _add_kmip_certificate(self, kms_details):
        """
        Configure KMIP Key Management Server with certificate based authentication

        Args:
            kms_name    (dictionary): dictionary with KMIP KMS details
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


    def _add_azure_key_vault_iam_auth(self, kms_details):
        """Configure Azure Key Management Server with IAM based authentication

            :arg
                kms_details ( dictionary ) - Dictionary with AWS KMS details
            :return:
                Object of KeyManagementServer class for the newly created KMS.
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


    def add_aws_kms(self, kms_name, aws_access_key, aws_secret_key, aws_region_name=None, kms_details = None):
        """Configure AWS Key Management Server

            Args:
                kms_name        (string) -- name of the Key Management Server

                aws_access_key  (string) -- AWS access key

                aws_secret_key  (string) -- AWS secret key, base64 encoded

                aws_region_name (string) -- AWS region
                                            defaults to "Asia Pacific (Mumbai)"

                kms_details ( dictionary ) - Dictionary with AWS KMS details

            Raises SDKException:
                If inputs are wrong data type

                If API response is not successful

                If the API response JSON is empty

                If error code on API response JSON is not 0
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
        

    def _kms_api_call(self, payload):
        """ Calling KMS API

        :param
        kms_details ( JSON ) - prefilled JSON payload for KMS API

        :exception
        Raises SDKException:
                    If API response code is not successful

                    If response JSON is empty

                    If errorCode is not part of the response JSON

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
        
    def __str__(self):
        """Representation string consisting of all KMS of the commcell.

            Returns:
                str - string of all the KMS associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'KMS')

        for index, client in enumerate(self._kms_dict):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, client)
            representation_string += sub_str

        return representation_string.strip()
    
    def __repr__(self):
        """Representation string for the instance of the KeyManagementServers class.
        
        Returns:
                str - string representation of this class
        """
        return "KeyManagementServers class instance for Commcell"

class KeyManagementServer(object):
    """Class for representing a single KMS in the commcell."""

    def __init__(self, commcell, name, id, type_id):
        """Initializes the KeyManagementServer object

        Args:
                commcell    (object)    --  instance of commcell
                name        (str)       --  The name of Key Management Server
                id          (int)       --  The id of Key Management Server
                type_id     (int)       --  The type id of Key Management Server
        
        Raises SDKException:
            If input type is invalid for any param

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
    
    def _get_name_from_type(self, type_id):
        """Returns the type name for type id
        
            Args:
                type_id     (int)   --  The type id of the Key Management Server
            
            Returns:
                type_name   (str)   --  The type name of the Key Management Server
            
            Raises SDKException:
                If type_id is not int() convertible

                If Unknown type_id received

        """
        KeyManagementServers._validate_input(type_id, int, 103)
        type_id = int(type_id)

        if type_id not in self._KMS_TYPE:
            raise SDKException("KeyManagementServer", 104)
        
        return self._KMS_TYPE[type_id]
    
    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'KeyServerManagement class instance for: "{0}"'
        return representation_string.format(self.name)
