# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

    revert()                    --  Method for revert operation

    reconcile()                 --  Method for recon operation

    add_array()                 --  Method to add array

    delete_array()              --  Method to delete array
"""

from __future__ import unicode_literals

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
                        reconcile=False):
        """ Common Method for Snap Operations

            Args :

                operation    (int)        -- snap Operation value

                volume_id    (int)        -- volume id of the snap backup job

                client_name  (str)        -- name of the destination client, default: None

                MountPath    (str)        -- MountPath for Snap operation, default: None

                do_vssprotection  (int)   -- Performs VSS protected snapshot mount

                control_host (int)        -- Control host for the Snap recon operation,
                defaullt: None

                reconcile    (bool)       -- Uses Reconcile json if true

            Return :

                object : Job object of Snap Operation job
        """

        if client_name is None:
            client_id = 0
        else:
            client_id = int(self._commcell_object.clients.get(client_name).client_id)

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
                                                    'flags':0,
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

    def delete(self, volume_id):
        """ Deletes Snap of the given volume id

            Args:

                volume_id    (int)        -- volume id of the snap backup job
        """
        return self._snap_operation(2, volume_id)

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
                  array_controller=None,
                  is_ocum=False):
        """This method will help in adding array entry in the array management
            Args :
                    vendor_name         (str)               -- vendor name

                    array_name          (str)               -- name of the array

                    username            (str)               -- username of the array

                    password            (str)               -- password to access array

                    control_host        (str)               -- control host of the array

                    array_controller    (str)               -- Array Controller MediaAgent Name

                    is_ocum             (bool)              -- used for netapp to specify whether
                                                               to use Primary file server or OCUM

            Return :

                errorMessage   (string) :  Error message
        """

        client_id = int(self._commcell_object.clients.get(array_controller).client_id)
        request_json = {
            "clientId": 0,
            "flags": 0,
            "assocType": 0,
            "copyId": 0,
            "appId": 0,
            "selectedMAs":[
                {
                    "arrayControllerId":0,
                    "mediaAgent":{
                        "name": array_controller,
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
            ],
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

            if error_code != 0:
                if error_code == 1:
                    raise SDKException('StorageArray', '101')

                error_message = response.json().get('errorMessage', '')
                o_str = 'Failed to add array\nError: "{0}"'.format(error_message)
                raise SDKException('StorageArray', '102', o_str)
        else:
            raise SDKException('StorageArray', '102')

    def delete_array(self, control_host_array):

        """This method Deletes an array from the array management
            Args :
                    control_host_array  (str)               -- array id of the snap array
            Return :

                errorMessage   (string) :  Error message"""

        storagearrays_delete_service = self.storage_arrays + '/{0}'.format(control_host_array)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'DELETE', storagearrays_delete_service
        )

        if response.json() and 'errorCode' in response.json():
            error_code = response.json()['errorCode']

            if error_code != 0:
                raise SDKException('StorageArray', '103')
            else:
                error_message = response.json()['errorMessage']
