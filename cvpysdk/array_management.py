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
    add_atlas_array ()          --  Creates an Array for MongoDB Atlas

"""

from __future__ import unicode_literals
import base64
from typing import Any, Optional

from .job import Job
from .exception import SDKException

class ArrayManagement(object):
    """
    Manages array-related operations within the Commcell environment.

    This class provides a comprehensive interface for handling array management activities,
    including snapshot operations, mounting and unmounting volumes, deleting and reverting volumes,
    and reconciling array states. It also supports array lifecycle management such as adding,
    editing, and deleting arrays with detailed configuration options.

    Key Features:
        - Perform snapshot operations on volumes
        - Mount and unmount volumes with support for VSS protection
        - Force unmount and force delete operations for robust management
        - Delete and revert volumes to previous states
        - Reconcile array states and configurations
        - Add new arrays with vendor-specific configurations
        - Edit existing arrays with granular update levels
        - Delete arrays from the Commcell environment

    Args:
        commcell_object: The Commcell object used for array management operations.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize an ArrayManagement instance for Snap-related operations.

        Args:
            commcell_object: An instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> array_mgmt = ArrayManagement(commcell)
            >>> print("ArrayManagement instance created successfully")

        #ai-gen-doc
        """

        self._commcell_object = commcell_object
        self._SNAP_OPS = self._commcell_object._services['SNAP_OPERATIONS']
        self.storage_arrays = self._commcell_object._services['STORAGE_ARRAYS']
        self.atlas_array = self._commcell_object._services['ATLAS_ARRAYS']

    def _snap_operation(
        self,
        operation: int,
        volume_id: Optional[list] = None,
        client_name: Optional[str] = None,
        mountpath: Optional[str] = None,
        do_vssprotection: bool = True,
        control_host: Optional[int] = None,
        flags: Optional[int] = None,
        reconcile: bool = False,
        user_credentials: Optional[dict] = None,
        server_name: Optional[str] = None,
        instance_details: Optional[dict] = None,
        **kwargs
    ) -> object:
        """Perform a snapshot operation such as mount, unmount, delete, or revert on specified volumes.

        This common method handles various snapshot operations for array management, including mounting,
        unmounting, deleting, and reverting snapshots. Additional options allow for VSS protection,
        specifying control hosts, user credentials, and instance details.

        Args:
            operation: The snapshot operation to perform.
                0 - mount
                1 - unmount
                2 - delete
                3 - revert
            volume_id: List of volume IDs associated with the snapshot backup job.
            client_name: Name of the destination client for the operation.
            mountpath: Mount path to use for the snapshot operation.
            do_vssprotection: Whether to perform a VSS-protected snapshot mount. Defaults to True.
            control_host: Control host ID for the snapshot reconcile operation.
            flags: Integer flag to force certain operations.
                1 - force unmount
                2 - force delete
            reconcile: If True, uses reconcile JSON for the operation.
            user_credentials: Dictionary containing user credentials, e.g., {"userName": "vcentername"}.
            server_name: Name of the vCenter server for mount operations.
            instance_details: Dictionary with instance details such as apptypeId, instanceId, and instanceName.
            **kwargs: Additional keyword arguments, such as 'destclientid' for VSA operations.

        Returns:
            Job object representing the snapshot operation job.

        Example:
            >>> # Mount a snapshot with VSS protection
            >>> job = array_mgmt._snap_operation(
            ...     operation=0,
            ...     volume_id=[123, 456],
            ...     client_name="DestinationClient",
            ...     mountpath="/mnt/snap",
            ...     do_vssprotection=True,
            ...     user_credentials={"userName": "vcenteradmin"},
            ...     server_name="vcenter01",
            ...     instance_details={"apptypeId": 106, "instanceId": 7, "instanceName": "VMWare"}
            ... )
            >>> print(f"Snap operation job started: {job}")

        #ai-gen-doc
        """

        if client_name is None:
            client_id = 0
        else:
            client_id = int(self._commcell_object.clients.get(client_name).client_id)

        if flags is None:
            flags = 0

        if user_credentials is None:
            user_credentials = {}
            server_name = ""
            server_type = 0
            instance_details = {}
        else:
            server_type = 1

        if kwargs.get('destclientid'):
            destClientId = int(kwargs.get('destclientid'))
        else:
            destClientId = 0

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
                "volumes": [],
                "appId": instance_details,
                "destClientId": destClientId
            }
            for i in range(len(volume_id)):
                if i == 0:
                    request_json['volumes'].append({'doVSSProtection': int(do_vssprotection),
                                                    'destClientId': client_id,
                                                    'destPath': mountpath,
                                                    'serverType': server_type,
                                                    'flags': flags,
                                                    'serverName': server_name,
                                                    'userCredentials': user_credentials,
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

    def mount(
        self,
        volume_id: int,
        client_name: str,
        mountpath: str,
        do_vssprotection: bool = True,
        user_credentials: Optional[dict] = None,
        server_name: Optional[str] = None,
        instance_details: Optional[dict] = None,
        **kwargs: dict
    ) -> Any:
        """Mount a snapshot of the specified volume to a destination client.

        This method mounts a snapshot (snap) of the given volume ID to the specified client and mount path.
        It supports VSS protection, user credentials for vCenter, and additional instance or server details.
        Extra keyword arguments can be provided for specific scenarios, such as VSA destination client ID.

        Args:
            volume_id: The ID of the volume from the snap backup job to mount.
            client_name: The name of the destination client where the snapshot will be mounted.
            mountpath: The mount path on the destination client for the snap operation.
            do_vssprotection: Whether to perform a VSS-protected mount (default is True).
            user_credentials: Optional dictionary containing user credentials (e.g., {'userName': 'vcenter_user'}).
            server_name: Optional vCenter server name for the mount operation.
            instance_details: Optional dictionary with instance details (e.g., {'apptypeId': 1, 'InstanceId': 2, 'InstanceName': 'name'}).
            **kwargs: Additional keyword arguments, such as 'destclientid' for VSA operations.

        Returns:
            The result of the mount operation. The return type may vary depending on the implementation.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> result = array_mgmt.mount(
            ...     volume_id=12345,
            ...     client_name='DestinationClient',
            ...     mountpath='/mnt/snap',
            ...     do_vssprotection=True,
            ...     user_credentials={'userName': 'vcenter_user'},
            ...     server_name='vcenter01',
            ...     instance_details={'apptypeId': 1, 'InstanceId': 2, 'InstanceName': 'Instance01'},
            ...     destclientid='67890'
            ... )
            >>> print(result)
            # The result contains details of the mount operation.

        #ai-gen-doc
        """
        return self._snap_operation(0, volume_id,
                                    client_name,
                                    mountpath,
                                    do_vssprotection,
                                    user_credentials=user_credentials,
                                    server_name=server_name,
                                    instance_details=instance_details, **kwargs)

    def unmount(self, volume_id: int) -> object:
        """Unmount the snapshot associated with the specified volume ID.

        Args:
            volume_id: The unique integer identifier of the volume whose snapshot should be unmounted.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> array_mgmt.unmount(12345)
            >>> print("Snapshot for volume 12345 has been unmounted.")

        #ai-gen-doc
        """
        return self._snap_operation(1, volume_id)

    def force_unmount(self, volume_id: int) -> object:
        """Forcefully unmount the snapshot associated with the specified volume ID.

        Args:
            volume_id: The integer ID of the volume whose snapshot should be unmounted.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> array_mgmt.force_unmount(12345)
            >>> print("Snapshot for volume 12345 has been forcefully unmounted.")

        #ai-gen-doc
        """
        return self._snap_operation(1, volume_id, flags=1)

    def delete(self, volume_id: int) -> object:
        """Delete the snapshot associated with the specified volume ID.

        Args:
            volume_id: The unique identifier of the volume whose snapshot should be deleted.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> array_mgmt.delete(12345)
            >>> print("Snapshot for volume 12345 deleted successfully.")

        #ai-gen-doc
        """
        return self._snap_operation(2, volume_id)

    def force_delete(self, volume_id: int) -> object:
        """Forcefully delete the snapshot associated with the specified volume ID.

        Args:
            volume_id: The unique integer identifier of the volume whose snapshot should be deleted.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> array_mgmt.force_delete(12345)
            >>> print("Snapshot for volume 12345 deleted successfully.")

        #ai-gen-doc
        """
        return self._snap_operation(2, volume_id, flags=2)

    def revert(self, volume_id: int) -> object:
        """Revert the snapshot of the specified volume by its ID.

        Args:
            volume_id: The unique integer ID of the volume whose snapshot should be reverted.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> array_mgmt.revert(12345)
            >>> print("Snapshot for volume 12345 has been reverted.")

        #ai-gen-doc
        """
        return self._snap_operation(3, volume_id)

    def reconcile(self, control_host: int) -> object:
        """Run a Reconcile Snap operation for the specified control host ID.

        Args:
            control_host: The control host ID of the array for which to perform the reconcile operation.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> array_mgmt.reconcile(12345)
            >>> print("Reconcile Snap operation initiated for control host 12345")

        #ai-gen-doc
        """
        return self._snap_operation(7, control_host=control_host, reconcile=True)

    def add_array(self,
                  vendor_name: str,
                  array_name: str,
                  credential_vault_name: str,
                  vendor_id: int,
                  config_data: list,
                  control_host: str = None,
                  array_access_node: list = None,
                  is_ocum: bool = False) -> str:
        """Add a new array entry to the array management system.

        This method registers a new storage array with the specified configuration and credentials.
        It supports specifying vendor details, credential vault, configuration data, and optional
        control host and access nodes. For NetApp arrays, the `is_ocum` flag determines whether to
        use the primary file server or OCUM.

        Args:
            vendor_name: The name of the storage vendor (e.g., "NetApp", "Dell EMC").
            array_name: The name to assign to the array.
            credential_vault_name: The credential vault name associated with the array.
            vendor_id: The unique identifier for the vendor.
            config_data: List of configuration data (e.g., Snap configs) to be updated for the array.
            control_host: (Optional) The control host of the array.
            array_access_node: (Optional) List of MediaAgent names that serve as array access nodes.
            is_ocum: (Optional) For NetApp arrays, set to True to use OCUM instead of the primary file server.

        Returns:
            str: An error message if the operation fails, or an empty string if successful.

        Example:
            >>> error = array_mgmt.add_array(
            ...     vendor_name="NetApp",
            ...     array_name="ProdArray01",
            ...     credential_vault_name="NetAppVault",
            ...     vendor_id=101,
            ...     config_data=[{"snap_config": "value"}],
            ...     control_host="array01.company.com",
            ...     array_access_node=["MA1", "MA2"],
            ...     is_ocum=True
            ... )
            >>> if error:
            ...     print(f"Failed to add array: {error}")
            ... else:
            ...     print("Array added successfully")

        #ai-gen-doc
        """

        snap_configs = {}
        assocType = 0
        if config_data is not None:
            assocType = 3
            request_json_service = self.storage_arrays + '/Vendors/{0}'.format(vendor_id)
            flag, snap_configs = self._commcell_object._cvpysdk_object.make_request(
                'GET', request_json_service
            )
            snap_configs = snap_configs.json()
            for m_config, value in config_data.items():
                for config in snap_configs['configs']['configList']:
                    if int(config['masterConfigId']) == int(m_config):
                        config['value'] = str(value)

        else:
            snap_configs['configs'] = {}

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
            "assocType": assocType,
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
            "configs": snap_configs['configs'],
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
                    "userName": ""
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
                },
                "savedCredential": {
                    "credentialName": credential_vault_name
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
                if error_code in [1, 10]:
                    raise SDKException('StorageArray', '101')

                error_message = response.json().get('errorMessage', '')
                o_str = 'Error: "{0}"'.format(error_message)
                raise SDKException('StorageArray', '102', o_str)
            return error_message
        else:
            raise SDKException('StorageArray', '102')

    def delete_array(self, control_host_array: str) -> str:
        """Delete an array from the array management system.

        Args:
            control_host_array: The control host ID of the array to be deleted.

        Returns:
            A string containing the error message after execution. If the deletion is successful,
            the error message may be empty or indicate success.

        Example:
            >>> array_mgmt = ArrayManagement()
            >>> error_msg = array_mgmt.delete_array("CH12345")
            >>> if error_msg:
            ...     print(f"Failed to delete array: {error_msg}")
            ... else:
            ...     print("Array deleted successfully")

        #ai-gen-doc
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
                   control_host_id: int,
                   config_data: dict,
                   config_update_level: str,
                   level_id: int,
                   array_access_node: dict) -> None:
        """Update the Snap Configuration and Array access nodes for a specified array.

        This method allows you to modify the Snap configuration and manage array access nodes
        for a given array by specifying the control host, configuration data, update level,
        level ID, and access node operations.

        Args:
            control_host_id: The control host ID of the array.
            config_data: Dictionary containing master config IDs and their corresponding values.
            config_update_level: The update level for the Snap configuration.
                Valid values include "array", "subclient", "copy", "client".
            level_id: The ID of the level where the configuration should be added or updated.
            array_access_node: Dictionary of array access nodes with their operation modes.
                Example: {"snapautotest3": "add", "linuxautomation1": "add", "snapautofc1": "delete"}

        Example:
            >>> array_mgr = ArrayManagement()
            >>> config = {"masterConfigId1": "value1", "masterConfigId2": "value2"}
            >>> access_nodes = {"nodeA": "add", "nodeB": "delete"}
            >>> array_mgr.edit_array(
            ...     control_host_id=101,
            ...     config_data=config,
            ...     config_update_level="array",
            ...     level_id=5,
            ...     array_access_node=access_nodes
            ... )
            >>> print("Array configuration updated successfully")

        #ai-gen-doc
        """

        copy_level_id = app_level_id = client_level_id = 0

        if config_update_level == "array":
            config_update_level = 3
            request_json_service = self.storage_arrays + '/{0}'.format(control_host_id)

        elif config_update_level == "copy":
            config_update_level = 6
            copy_level_id = level_id
            request_json_service = self.storage_arrays + '/{0}?copyId={1}&assocType={2}'.format(
                control_host_id, copy_level_id, config_update_level)

        elif config_update_level == "subclient":
            config_update_level = 9
            app_level_id = level_id
            request_json_service = self.storage_arrays + '/{0}?appId={1}&assocType={2}'.format(
                control_host_id, app_level_id, config_update_level)

        elif config_update_level == "client":
            config_update_level = 8
            client_level_id = level_id
            request_json_service = self.storage_arrays + '/{0}?clientId={1}&assocType={2}'.format(
                control_host_id, client_level_id, config_update_level)

        else:
            config_update_level = 3
            request_json_service = self.storage_arrays + '/{0}'.format(control_host_id)

        flag, request_json = self._commcell_object._cvpysdk_object.make_request(
            'GET', request_json_service)

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
        del request_json['info']['region']

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

    def add_atlas_array(self, arraydict:dict) -> str:
        """Add a new array entry to the array management system.

        This method registers a new storage array with the specified configuration and credentials.
        It supports specifying vendor details, credential vault, configuration data, and optional
        control host and access nodes.

        Args:
            arraydict (dict): Dictionary containing array detils

        Returns:
            str: An error message if the operation fails, or an empty string if successful.

        Example:
            >>> error = array_mgmt.add_array(arraydict)
            >>> if error:
            ...     print(f"Failed to add array: {error}")
            ... else:
            ...     print("Array added successfully")

        #ai-gen-doc
        """
        # get List of existing arrays

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self.atlas_array
        )
        array_json = response.json()

        # check if any array exists with name MongoDB Atlas else create a new one

        if not (any(item["name"]=="MongoDB Atlas" for item in array_json["arrays"])):

            request_json = {
                              "snapConfigurations": [],
                              "general": {
                                "name": arraydict["array_name"],
                                "controlHost": arraydict["control_host"],
                                "snapVendor": "MongoDB Atlas",
                                "savedCredential": {
                                  "id":arraydict["credential_vault_id"],
                                  "name": arraydict["credential_vault_name"]
                                },
                                "description": "MongoDB Atlas Array"
                              },
                              "accessNodes": [
                                {
                                  "name": arraydict["array_access_node"],
                                  "id":arraydict["array_access_node_id"],
                                  "pruning": True
                                }
                              ]
                            }

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self.atlas_array, request_json
            )

            if response.json() and 'errorCode' in response.json():
                error_code = response.json()['errorCode']
                error_message = response.json()['errorMessage']

                if error_code != 0:
                    if error_code in [1, 10]:
                        raise SDKException('StorageArray', '101')

                    error_message = response.json().get('errorMessage', '')
                    o_str = 'Error: "{0}"'.format(error_message)
                    raise SDKException('StorageArray', '102', o_str)
                return error_message
            else:
                raise SDKException('StorageArray', '102')