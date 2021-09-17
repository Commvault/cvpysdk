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

KeyManagementServers        --   Class for representing all the KMS in the commcell.

KeyManagementServer         --   Class for representing a single KMS in the commcell.


KeyManagementServers:
=================

    __init__()              --      initializes KeyManagementServers class object

    _get_kms_dict()         --      fetches the dictionary of all Key Management Servers

    get()                   --      gets a specific Key Management Server object

    get_all_kms()           --      gets the dictionary of all Key Management Servers

    refresh()               --      refreshes the dictionary of Key Management Servers

    delete()                --      deletes a Key Management Server

    has_kms()               --      checks if the Key Management Server exists or not

    add_aws_kms()           --      configures AWS Key Management Server


KeyManagementServers Attributes
==========================

    **_kms_dict**           --    a name-indexed dictionary of KeyManagementServer objects

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

class KeyManagementServers(object):
    """Class for representing all the KMS in the commcell."""

    def __init__(self, commcell):
        """Initializes KeyManagementServers class object

            Args:
                commcell    (object)    --  instance of commcell

        """
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

        self.refresh()
    
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
    
    def add_aws_kms(self, kms_name, aws_access_key, aws_secret_key, aws_region_name=None):
        """Configure AWS Key Management Server
        
            Args:
                kms_name        (string) -- name of the Key Management Server
                
                aws_access_key  (string) -- AWS access key
                
                aws_secret_key  (string) -- AWS secret key, base64 encoded

                aws_region_name (string) -- AWS region 
                                            defaults to "Asia Pacific (Mumbai)"

            Raises SDKException:
                If inputs are wrong data type

                If API response is not successful

                If the API response JSON is empty

                If error code on API response JSON is not 0
        """
        KeyManagementServers._validate_input(kms_name, str)
        KeyManagementServers._validate_input(aws_access_key, str)
        KeyManagementServers._validate_input(aws_secret_key, str)

        if aws_region_name is None:
            aws_region_name = "Asia Pacific (Mumbai)"

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
        return "KeyManagementServers class instance for Commcell: '{0}'".format(
            self._commcell.commserv_name
        )

class KeyManagementServer(object):
    """Class for representing a single KMS in the commcell."""

    _TYPE = {
        1: "KEY_PROVIDER_COMMVAULT",
        2: "KEY_PROVIDER_KMIP",
        3: "KEY_PROVIDER_AWS_KMS",
        4: "KEY_PROVIDER_AZURE_KEY_VAULT",
        5: "KEY_PROVIDER_SAFENET",
        6: "KEY_PROVIDER_PASSPHRASE",
    }

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

        if type_id not in self._TYPE:
            raise SDKException("KeyManagementServer", 104)
        
        return self._TYPE[type_id]
    
    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'KeyServerManagement class instance for: "{0}"'
        return representation_string.format(self.name)
