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

"""File for operating on a Virtual Server Azure Local Subclient.

AzureLocalSubclient is the only class defined in this file.

AzureLocalSubclient: Derived class from VirtualServerSubClient Base class, representing an
                     Azure Local (Azure Stack HCI) Subclient, and to perform operations on that Subclient

AzureLocalSubclient:

    disk_restore()                        --  Perform Disk Restore on Azure Local Subclient

    full_vm_restore_out_of_place()        --  restores the VM specified to the specified client,
                                              at the specified destination location

    full_vm_restore_in_place()            --  restores the VM specified by the user to the same location
"""

from enum import Enum
from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class AzureLocalSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class, representing an
    Azure Local (Azure Stack HCI) virtual server subclient, and to perform operations on that subclient.
    
    Azure Local (formerly Azure Stack HCI) uses Hyper-V technology, so this class
    supports similar disk formats and restore operations as Hyper-V."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Azure Local Virtual Server instance.
        
        Args:
            backupset_object    (object)    --  instance of the backupset class
            subclient_name      (str)       --  subclient name
            subclient_id        (int)       --  subclient id
        """
        self.diskExtension = [".vhd", ".avhd", ".avhdx", ".vhdx"]
        super(AzureLocalSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    class disk_pattern(Enum):
        """Stores the disk pattern for Azure Local hypervisor."""
        name = "name"
        datastore = "DestinationPath"
        new_name = "new_name"

    def disk_restore(self,
                     vm_name,
                     destination_path,
                     proxy_client=None,
                     disk_name=None,
                     copy_precedence=0,
                     convert_to=None,
                     media_agent=None,
                     snap_proxy=None,
                     unconditional_overwrite=False):
        """Restores the disk specified in the input paths list to the same location.

        Args:
            vm_name                     (str)   --  VM from which disk is to be restored
            destination_path            (str)   --  path where the disk needs to be restored
            proxy_client                (str)   --  destination client to which disk is to be restored
            disk_name                   (str)   --  name of the disk which has to be restored
            copy_precedence             (int)   --  SP copy precedence from which browse has to be performed
            convert_to                  (str)   --  convert the disk to the specified format
                                                    default: None
            media_agent                 (str)   --  MA needs to use for disk browse
                                                    default: Storage policy MA
            snap_proxy                  (str)   --  proxy need to be used for disk restores from snap
                                                    default: proxy in instance or subclient
            unconditional_overwrite     (bool)  --  specifies whether to overwrite existing files 
                                                    unconditionally during restore
                                                    default: False

        Returns:
            object - instance of the Job class for this restore job

        Raises:
            SDKException:
                if destination_path is not str
                if vm_name is not str or list
                if failed to initialize job
                if response is empty
                if response is not success
        """
        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _disk_restore_option = {}

        # Check if inputs are correct
        if not (isinstance(destination_path, str) and isinstance(vm_name, (str, list))):
            raise SDKException('Subclient', '101')

        if proxy_client is None:
            _disk_restore_option["client"] = self._backupset_object._instance_object.co_ordinator
        else:
            _disk_restore_option["client"] = proxy_client

        # Get disk list
        disk_list, disk_info_dict = self.disk_level_browse("\\" + _vm_ids[vm_name])

        if disk_name is not None:
            if disk_name in disk_list:
                disk_list = [disk_name]
            else:
                raise SDKException('Subclient', '111')

        # Handle conversion option
        if convert_to is not None:
            _disk_extn = self._get_disk_extension(disk_list)
            if isinstance(_disk_extn, list):
                raise SDKException('Subclient', '101')
            _disk_restore_option["destination_vendor"], \
                _disk_restore_option["destination_disktype"] = \
                self._get_conversion_disk_type(_disk_extn, convert_to)
        else:
            _disk_restore_option["destination_vendor"] = \
                self._backupset_object._instance_object._vendor_id
            _disk_restore_option["destination_disktype"] = 0

        _disk_restore_option["volume_level_restore"] = 4

        # Set source item list
        _src_item_list = []
        for each_disk in disk_list:
            _src_item_list.append("\\" + _vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        self._set_restore_inputs(
            _disk_restore_option,
            in_place=False,
            copy_precedence=copy_precedence,
            destination_path=destination_path,
            paths=_src_item_list,
            media_agent=media_agent,
            snap_proxy=snap_proxy,
            unconditional_overwrite=unconditional_overwrite
        )

        request_json = self._prepare_disk_restore_json(_disk_restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(self,
                                     destination_client=None,
                                     proxy_client=None,
                                     destination_path=None,
                                     vm_to_restore=None,
                                     overwrite=False,
                                     power_on=False,
                                     copy_precedence=0,
                                     add_to_failover=False,
                                     network=None,
                                     restored_vm_name=None,
                                     restore_option=None,
                                     snap_proxy=None,
                                     media_agent=None,
                                     **kwargs):
        """Restores the FULL Virtual machine specified in the input list to the client,
        at the specified destination location.

        Args:
            destination_client      (str)       --  destination client name where VM needs to be restored
            proxy_client            (str)       --  proxy client to use for restore
            destination_path        (str)       --  full path of the restore location on client
            vm_to_restore           (list)      --  list of VM name(s) to restore
            overwrite               (bool)      --  overwrite the existing VM (default: False)
            power_on                (bool)      --  power on the restored VM (default: False)
            copy_precedence         (int)       --  copy precedence value (default: 0)
            add_to_failover         (bool)      --  Add the Restored VM to Failover Cluster (default: False)
            network                 (str)       --  Network interface card to be used
            restored_vm_name        (str)       --  new name for the restored VM
            restore_option          (dict)      --  complete dictionary with all advanced options
            snap_proxy              (str)       --  Snap proxy to be used for restore
            media_agent             (str)       --  Media Agent to be used for Browse
            **kwargs                            --  Arbitrary keyword arguments
                v2_details          (dict)      --  details for v2 subclient

        Returns:
            object - instance of the Job class for this restore job

        Raises:
            SDKException:
                if destination_path is not a string
                if failed to initialize job
                if response is empty
                if response is not success
        """
        # Restore options
        if restore_option is None:
            restore_option = {}
        restore_option["v2_details"] = kwargs.get("v2_details", None)

        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True

        if restored_vm_name:
            if not (isinstance(vm_to_restore, str) or isinstance(restored_vm_name, str)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_vm_name

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        # Check mandatory input parameters are correct
        if bool(restore_option):
            if not (isinstance(destination_path, str) and
                    isinstance(overwrite, bool) and
                    isinstance(power_on, bool) and
                    isinstance(add_to_failover, bool)):
                raise SDKException('Subclient', '101')

        # Set attributes for all the options in restore XML from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            vcenter_client=destination_client,
            client_name=proxy_client,
            esx_server=proxy_client,
            esx_host=proxy_client,
            add_to_failover=add_to_failover,
            datastore=destination_path,
            in_place=False,
            destination_network=network,
            snap_proxy=snap_proxy,
            media_agent=media_agent
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 copy_precedence=0,
                                 add_to_failover=False,
                                 snap_proxy=None,
                                 **kwargs):
        """Restores the FULL Virtual machine specified in the input list to the same location.

        Args:
            vm_to_restore           (list)      --  list of VM name(s) to restore
            overwrite               (bool)      --  overwrite the existing VM (default: True)
            power_on                (bool)      --  power on the restored VM (default: True)
            copy_precedence         (int)       --  copy precedence value (default: 0)
            add_to_failover         (bool)      --  Add the Restored VM to Failover Cluster (default: False)
            snap_proxy              (str)       --  proxy need to be used for disk restores from snap
                                                    (default: proxy in instance or subclient)
            **kwargs                            --  Arbitrary keyword arguments
                v2_details          (dict)      --  details for v2 subclient

        Returns:
            object - instance of the Job class for this restore job

        Raises:
            SDKException:
                if failed to initialize job
                if response is empty
                if response is not success
        """
        restore_option = {"v2_details": kwargs.get("v2_details", None)}

        # Check mandatory input parameters are correct
        if not (isinstance(overwrite, bool) and
                isinstance(power_on, bool) and
                isinstance(add_to_failover, bool)):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True

        if vm_to_restore and isinstance(vm_to_restore, str):
            vm_to_restore = [vm_to_restore]

        # Set attributes for all the options in restore XML from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            add_to_failover=add_to_failover,
            in_place=True,
            snap_proxy=snap_proxy
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        request_json["taskInfo"]["subTasks"][0][
            "options"]["restoreOptions"]["virtualServerRstOption"]["diskLevelVMRestoreOption"][
            "esxServerName"] = restore_option["esx_server"]
        return self._process_restore_response(request_json)
