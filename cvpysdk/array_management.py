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

"""
File for performing IntelliSnap and Array Management operations on Commcell via REST API

ArrayManagement:   Class for handling all Array Management Operations

ArrayManagement:

    __init__()                  --  initialize instance of the ArrayManagement class

    _snap_operation()           --  Common Method for Snap Operations

    mount()                     --  Method for mount operation

    unmount()                   --  Method for unmount operation

    delete()                    --  Method for delete operation

    force_delete()              --  Method for force delete operation

    revert()                    --  Method for revert operation

    reconcile()                 --  Method for recon operation

    add_array()                 --  Method to add array

    delete_array()              --  Method to delete array

    edit_array()                --  Method to Update Snap Configuration and Array Access Node MA
                                    for the given Array
"""

from __future__ import unicode_literals
import json
from .job import Job
from .exception import SDKException


class ArrayManagement(object):
    """Class for representing all the array management activities with the commcell."""

    def __init__(self, commcell_object):
        """ Initialize the ArrayManagement class instance for performing Snap related operations

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the ArrayManagement class
        """

        self._commcell_object = commcell_object
        self._SNAP_OPS = self._commcell_object._services['SNAP_OPERATIONS']
        self.storage_arrays = self._commcell_object._services['STORAGE_ARRAYS']

    def _snap_operation(self,
                        operation,
                        volume_id=None,
                        client_name=None,
                        mountpath=None,
                        do_vssprotection=True,
                        control_host=None,
                        flags=None,
                        reconcile=False):
        """ Common Method for Snap Operations

            Args :

                operation    (int)        -- snap Operation value

                volume_id    (list)        -- volume id's of the snap backup job

                client_name  (str)        -- name of the destination client, default: None

                MountPath    (str)        -- MountPath for Snap operation, default: None

                do_vssprotection  (int)   -- Performs VSS protected snapshot mount

                control_host (int)        -- Control host for the Snap recon operation,
                defaullt: None

                flags        (int)       -- value to define when snap operation to be forced
                1 - to force unmount
                2 - to force delete

                reconcile    (bool)       -- Uses Reconcile json if true

            Return :

                object : Job object of Snap Operation job
        """

        if client_name is None:
            client_id = 0
        else:
            client_id = int(self._commcell_object.clients.get(client_name).client_id)

        if flags is None:
            flags = 0

        if reconcile:
            request_json = {
                "reserveField": 0,
                "doVSSProtection": 0,
                "serverName": "",
                "controlHostId": control_host,
                "CopyId": 0,
                "smArrayId": "",
                "destClientId": 0,
                "destPath": "",
                "serverType": 0,
                "operation": operation,
                "userCredentials": {},
                "scsiServer": {
                    "_type_": 3
                }
            }
        else:
            request_json = {
                "reserveField": 0,
                "serverType": 0,
                "operation": operation,
                "userCredentials": {},
                "volumes": []
            }
            for i in range(len(volume_id)):
                if i == 0:
                    request_json['volumes'].append({'doVSSProtection': int(do_vssprotection),
                                                    'destClientId': client_id,
                                                    'destPath': mountpath,
                                                    'serverType':0,
                                                    'flags': flags,
                                                    'serverName':"",
                                                    'userCredentials': {},
                                                    'volumeId':int(volume_id[i][0]),
                                                    'CommCellId': self._commcell_object.commcell_id})

                else:
                    request_json['volumes'].append({'volumeId':int(volume_id[i][0]),
                                                    'CommCellId': self._commcell_object.commcell_id})

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._SNAP_OPS, request_json)

        if flag:
            if response.json():
                if "jobId" in response.json():
                    return Job(self._commcell_object, response.json()['jobId'])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'job for Snap Operation failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Snap', '102', o_str)
        else:
            raise SDKException('Snap', '102')

    def mount(self, volume_id, client_name, mountpath, do_vssprotection=True):
        """ Mounts Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job

                client_name  (str)        -- name of the destination client, default: None

                MountPath    (str)        -- MountPath for Snap operation, default: None

                do_vssprotection (int)    -- Performs VSS protected mount
        """
        return self._snap_operation(0, volume_id, client_name, mountpath, do_vssprotection)

    def unmount(self, volume_id):
        """ UnMounts Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(1, volume_id)

    def force_unmount(self, volume_id):
        """ Force UnMounts Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(1, volume_id, flags=1)

    def delete(self, volume_id):
        """ Deletes Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(2, volume_id)

    def force_delete(self, volume_id):
        """ Deletes Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(2, volume_id, flags=2)

    def revert(self, volume_id):
        """ Reverts Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(3, volume_id)

    def reconcile(self, control_host):
        """ Runs Reconcile Snap of the given control host id

            Args:

                control_host    (int)        -- control host id of the array
        """
        return self._snap_operation(7, control_host=control_host, reconcile=True)

    def add_array(self,
                  vendor_name,
                  array_name,
                  username,
                  password,
                  control_host=None,
                  array_access_node=None,
                  is_ocum=False):
        """This method will help in adding array entry in the array management
            Args :
                    vendor_name         (str)               -- vendor name

                    array_name          (str)               -- name of the array

                    username            (str)               -- username of the array

                    password            (str)               -- password to access array

                    control_host        (str)               -- control host of the array

                    array_access_node   (list)              -- Array Access Node MediaAgent's Name list

                    is_ocum             (bool)              -- used for netapp to specify whether
                                                               to use Primary file server or OCUM

            Return :

                errorMessage   (string) :  Error message
        """

        selectedMAs = []
        if array_access_node is not None:
            for node in array_access_node:
                client_id = int(self._commcell_object.clients.get(node).client_id)
                node_dict = {
                    "arrayControllerId":0,
                    "mediaAgent":{
                        "name": node,
                        "id": client_id
                        },
                    "arrCtrlOptions":[
                        {
                            "isEnabled": True,
                            "arrCtrlOption":{
                                "name":"Pruning",
                                "id": 262144
                            }
                        }
                    ]
                }
                selectedMAs.append(node_dict)

        request_json = {
            "clientId": 0,
            "flags": 0,
            "assocType": 0,
            "copyId": 0,
            "appId": 0,
            "selectedMAs":selectedMAs,
            "hostDG": {
                "doNotMoveDevices": True,
                "isOverridden": False,
                "hostDGName": "",
                "useOnlySpouseDevices": False,
                "flags": 0,
                "deviceGroupOption": 0
            },
            "arrayDG": {
                "isOverridden": False,
                "arrayDGName": "",
                "flags": 0,
                "disableDG": False,
                "useDevicesFromThisDG": False
            },
            "configList": {},
            "array": {
                "name": "",
                "id": 0
            },
            "vendor": {
                "name": "",
                "id": 0
            },
            "info": {
                "passwordEdit": False,
                "offlineReason": "",
                "arrayType": 0,
                "flags": 0,
                "description": "",
                "ctrlHostName": control_host,
                "offlineCode": 0,
                "isEnabled": True,
                "arrayInfoType": 0,
                "uniqueIdentifier": "",
                "securityAssociations": {
                    "processHiddenPermission": 0
                },
                "userPswd": {
                    "userName": username,
                    "password": password,

                },
                "arraySecurity": {},
                "arrayName": {
                    "name": array_name,
                    "id": 0
                },
                "vendor": {
                    "name": vendor_name,
                    "id": 0
                },
                "client": {
                    "name": "",
                    "id": 0
                }
            }
        }
        array_type_dict1 = {
            "info": {
                "arrayType": 2
            }
        }
        array_type_dict2 = {
            "info": {
                "arrayType": 1
            }
        }
        array_type_dict3 = {
            "info": {
                "arrayType": 0
            }
        }
        if vendor_name == "NetApp":
            request_json["info"].update(array_type_dict1["info"]),

        if vendor_name == "NetApp" and is_ocum:
            request_json["info"].update(array_type_dict2["info"]),
        else:
            request_json["info"].update(array_type_dict3["info"]),

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self.storage_arrays, request_json
        )

        if response.json() and 'errorCode' in response.json():
            error_code = response.json()['errorCode']
            error_message = response.json()['errorMessage']

            if error_code != 0:
                if error_code == 1:
                    raise SDKException('StorageArray', '101')

                error_message = response.json().get('errorMessage', '')
                o_str = 'Error: "{0}"'.format(error_message)
                raise SDKException('StorageArray', '102', o_str)
            return error_message
        else:
            raise SDKException('StorageArray', '102')

    def delete_array(self, control_host_array):
        """This method Deletes an array from the array management
            Args :
                control_host_array      (str)        --   Control Host id of the array
            Return :
                errorMessage            (str)        --   Error message after the execution
        """

        storagearrays_delete_service = self.storage_arrays + '/{0}'.format(control_host_array)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'DELETE', storagearrays_delete_service
        )

        if response.json():
            error_code = response.json()['errorCode']
            error_message = response.json()['errorMessage']

            if error_code != 0:
                raise SDKException('StorageArray', '103', error_message)
            return error_message

    def edit_array(self,
                   control_host_id,
                   config_data,
                   config_update_level,
                   level_id,
                   array_access_node):
        """Method to Update Snap Configuration and Array access nodes for the given Array
        Args:
            control_host_id        (int)        -- Control Host Id of the Array

            Config_data            (dict)       -- Master config Id and the config value in dict format

            config_update_level    (str)        -- update level for the Snap config
            ex: "array", "subclient", "copy", "client"

            level_id               (int)        -- level Id where the config needs to be
                                                   added/updated

            array_access_node      (dict)       -- Array Access Node MA's in dict format with
                                                   operation mode
            default: None
            Ex: {"snapautotest3" : "add", "linuxautomation1" : "add", "snapautofc1" : "delete"}

        """

        copy_level_id = app_level_id = client_level_id = 0
        request_json_service = self.storage_arrays + '/{0}'.format(control_host_id)
        flag, request_json = self._commcell_object._cvpysdk_object.make_request(
            'GET', request_json_service
        )

        if config_update_level == "array":
            config_update_level = 3
        elif config_update_level == "copy":
            config_update_level = 6
            copy_level_id = level_id
        elif config_update_level == "subclient":
            config_update_level = 9
            app_level_id = level_id
        elif config_update_level == "client":
            config_update_level = 8
            client_level_id = level_id
        else:
            config_update_level = 3

        request_json = request_json.json()

        update_dict = {
            "add": False,
            "forceAdd": False,
            "assocType": config_update_level,
            "copyId": copy_level_id,
            "appId": app_level_id,
            "clientId": client_level_id
            }
        request_json.update(update_dict)

        if config_data is not None:
            for m_config, value in config_data.items():
                for config in request_json['configList']['configList']:
                    if config['masterConfigId'] == int(m_config):
                        if isinstance(value, dict):
                            for alias, mode in value.items():
                                if mode == "add":
                                    config_values_dict = {
                                        "name": str(alias),
                                        "id": 0
                                        }
                                    aliasPresent = False
                                    for alias_name in config['values']:
                                        if alias_name['name'] == alias:
                                            aliasPresent = True
                                    if not aliasPresent:
                                        config['values'].append(config_values_dict)
                                if mode != "add" and mode != "delete":
                                    for alias_name in config['values']:
                                        if alias_name['name'] == mode:
                                            alias_name['name'] = alias
                                if mode == "delete":
                                    for alias_name in range(len(config['values'])):
                                        if config['values'][alias_name]['name'] == alias:
                                            del config['values'][alias_name]
                                            break
                            if config_update_level != "array":
                                config['isOverridden'] = True

                        else:
                            config['value'] = str(value)
                            if config_update_level != "array":
                                config['isOverridden'] = True

        if array_access_node is not None:
            for access_node, mode in array_access_node.items():
                client_id = int(self._commcell_object.clients.get(access_node).client_id)
                if mode == "add":
                    if "selectedMAs" in request_json:
                        update_dict = {
                            "arrayControllerId": 0,
                            "mediaAgent": {
                                "name": access_node,
                                "id": client_id
                                },
                            "arrCtrlOptions": [
                                {
                                    "isEnabled": True,
                                    "arrCtrlOption": {
                                        "name": "Pruning",
                                        "id": 262144
                                        }
                                    }
                                ]
                            }
                        isNodePresent = False
                        for nodes in request_json['selectedMAs']:
                            if nodes['mediaAgent']['id'] == int(client_id):

                                isNodePresent = True
                        if not isNodePresent:
                            request_json['selectedMAs'].append(update_dict)

                    else:
                        update_dict = {
                            "selectedMAs": [
                                {
                                    "arrayControllerId": 0,
                                    "mediaAgent": {
                                        "name": access_node,
                                        "id": client_id
                                    },
                                    "arrCtrlOptions": [
                                        {
                                            "isEnabled": True,
                                            "arrCtrlOption": {
                                                "name": "Pruning",
                                                "id": 262144
                                            }
                                        }
                                    ]
                                }
                            ]}
                        request_json.update(update_dict)

                elif mode == "delete":
                    client_id = int(self._commcell_object.clients.get(access_node).client_id)
                    if "selectedMAs" in request_json:
                        for controller in range(len(request_json['selectedMAs'])):
                            if request_json['selectedMAs'][controller]['mediaAgent']['id'] == int(client_id):
                                del request_json['selectedMAs'][controller]
                                break

        request_json['configs'] = request_json.pop('configList')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self.storage_arrays, request_json
        )

        if response.json() and 'errorCode' in response.json():
            error_code = response.json()['errorCode']

            if error_code != 0:
                if error_code == 1:
                    raise SDKException('StorageArray', '101')

                error_message = response.json().get('errorMessage', '')
                o_str = 'Failed to update Snap Configs\nError: "{0}"'.format(error_message)
                raise SDKException('StorageArray', '103', o_str)
        else:
            raise SDKException('StorageArray', '103')
