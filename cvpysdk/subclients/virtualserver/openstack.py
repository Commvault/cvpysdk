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

"""File for operating on a Virtual Server OpenStack Subclient.

OpenStackVirtualServerSubclient is the only class defined in this file.

OpenStackVirtualServerSubclient:   Derived class from VirtualServerSubClient Base
                                class,representing a OpenStack Subclient,
                                and to perform operations on that Subclient

OpenStackVirtualServerSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of openstack subclient class,
                                    associated with the VirtualServer subclient

    full_vm_restore_in_place()  --  restores the VM specified by the user to
                                    the same location

    full_vm_restore_out_of_place() -- restores the VM specified to the provided
                                      Openstack project or tenant


"""

from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException
from past.builtins import basestring


class OpenStackVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a OpenStack virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """

        super(OpenStackVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = ["none"]

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            restored_vm_name=None,
            vcenter_client=None,
            destination_client=None,
            esx_host=None,
            esx_server=None,
            datastore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            proxy_client=None,
            source_ip=None,
            destination_ip=None,
            datacenter = None,
            cluster = None):
            # vm_to_restore=None,
            # overwrite=True,
            # power_on=True,
            # destination_client=None,
            # copy_precedence=0,
            # esx_host = None,
            # esx_server = None,
            # proxy_client=None):
        """Restores the FULL Virtual machine specified in the input list
            to the location same as the actual location of the VM in VCenter.

            Args:
                vm_to_restore         (list)        --  provide the VM name to restore
                                                        default: None

                overwrite             (bool)        --  overwrite the existing VM
                                                        default: True

                power_on              (bool)        --  power on the  restored VM
                                                        default: True

                copy_precedence       (int)         --  copy precedence value
                                                        default: 0

                proxy_client          (basestring)  --  proxy client to be used for restore
                                                        default: proxy added in subclient

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        restore_option = {}

        # check input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, basestring):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        if proxy_client is not None:
            restore_option['client'] = proxy_client

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
                restore_option,
                in_place=True,
                vcenter_client=destination_client,
                datastore=datastore,
                esx_host=esx_host,
                esx_server=esx_server,
                unconditional_overwrite=overwrite,
                power_on=power_on,
                vm_to_restore=self._set_vm_to_restore(vm_to_restore),
                copy_precedence=copy_precedence,
                volume_level_restore=1,
                source_item=[],
                source_ip=source_ip,
                destination_ip=destination_ip,
                data_center = datacenter,
                cluster = cluster
    )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            restored_vm_name=None,
            vcenter_client=None,
            destination_client=None,
            esx_host=None,
            esx_server=None,
            datastore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            proxy_client=None,
            source_ip=None,
            destination_ip=None,
            datacenter = None,
            cluster = None,
            securityGroups = None
    ):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore            (str)    --  VM that is to be restored

                restored_vm_name         (str)    --  new name of vm. If nothing is passed,
                                                      'delete' is appended to the original vm name

                vcenter_client    (basestring)    --  name of the vcenter client where the VM
                                                      should be restored.

                esx_host          (basestring)    --  destination esx host. Restores to the source
                                                      VM esx if this value is not specified

                datastore         (basestring)    --  datastore where the restored VM should be
                                                      located. Restores to the source VM datastore
                                                      if this value is not specified

                overwrite               (bool)    --  overwrite the existing VM
                                                      default: True

                power_on                (bool)    --  power on the  restored VM
                                                      default: True

                copy_precedence          (int)    --  copy precedence value
                                                      default: 0

                proxy_client      (basestring)    --  destination proxy client

                source_ip           (basestring)    --  IP of the source VM

                destination_ip      (basestring)    --  IP of the destination VM



            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        restore_option = {}

        # check mandatory input parameters are correct
        for vm in vm_to_restore:
            if vm and not isinstance(vm, basestring):
                raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client'] = proxy_client

        if restored_vm_name:
            if not(isinstance(vm_to_restore, basestring) or
                   isinstance(restored_vm_name, basestring)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_vm_name


        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=destination_client,
            datastore=datastore,
            esx_host=esx_host,
            esx_server=esx_server,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            source_item=[],
            source_ip=source_ip,
            destination_ip=destination_ip,
            datacenter = datacenter,
            cluster = cluster,
            securityGroups = securityGroups
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def disk_restore(self,
                     vm_name,
                     destination_path,
                     disk_name=None,
                     proxy_client=None,
                     copy_precedence=0,
                     convert_to=None,
                     media_agent=None,
                     snap_proxy=None):
        """Restores the disk specified in the input paths list to the same location

            Args:
                vm_name             (basestring)    --  Name of the VM added in subclient content
                                                        whose  disk is selected for restore

                destination_path        (basestring)    --  Staging (destination) path to restore the
                                                        disk.

                disk_name                 (list)    --  name of the disk which has to be restored
                                                        (cinder volumes will be restores - enter full
                                                        name of the disk)
                                                        default: None

                proxy_client        (basestring)    --  Destination proxy client to be used
                                                        default: None

                copy_precedence            (int)    --  SP copy precedence from which browse has to
                                                         be performed

                convert_to          (basestring)    --  disk format for the restored disk
                                                        (applicable only when the vmdk disk is
                                                        selected for restore). Allowed values are
                                                        "VHDX" or "VHD"
                                                        default: None
                media_agent         (str)   -- MA needs to use for disk browse
                    default :Storage policy MA

                snap_proxy          (str)   -- proxy need to be used for disk
                                                    restores from snap
                    default :proxy in instance or subclient
            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not passed in proper expected format

                    if response is empty

                    if response is not success
        """

        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _disk_restore_option = {}

        disk_extn = '.vmdk'
        if not disk_name:
            disk_name = []
        else:
            disk_extn = self._get_disk_extension(disk_name)

        # check if inputs are correct
        if not (isinstance(vm_name, basestring) and
                isinstance(destination_path, basestring) and
                isinstance(disk_name, list) and
                disk_extn == '.vmdk'):
            raise SDKException('Subclient', '101')

        # if convert_to is not None:
        #     convert_to = convert_to.lower()
        #     if convert_to not in ['vhdx', 'vhd']:
        #         raise SDKException('Subclient', '101')

        if copy_precedence:
            _disk_restore_option['copy_precedence_applicable'] = True

        # fetching all disks from the vm
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + vm_ids[vm_name])

        if not disk_name:   # if disk names are not provided, restore all vmdk disks
            for each_disk_path in disk_list:
                disk_name.append(each_disk_path.split('\\')[-1])

        else:   # else, check if the given VM has a disk with the list of disks in disk_name.
            for each_disk in disk_name:
                each_disk_path = "\\" + str(vm_name) + "\\" + each_disk
                if each_disk_path not in disk_list:
                    raise SDKException('Subclient', '111')

        # if conversion option is given
        if convert_to is not None:
            dest_disk_dict = {
                'VHD_DYNAMIC': 13,
                'VHDX_DYNAMIC': 21
            }
            vol_restore, dest_disk = self._get_conversion_disk_Type('vmdk', convert_to)
            _disk_restore_option["destination_disktype"] = dest_disk_dict[dest_disk]
            _disk_restore_option["volume_level_restore"] = 4
        else:
            _disk_restore_option["volume_level_restore"] = 3

        _disk_restore_option["destination_vendor"] = \
            self._backupset_object._instance_object._vendor_id

        if proxy_client is not None:
            _disk_restore_option['client'] = proxy_client
        else:
            _disk_restore_option['client'] = self._backupset_object._instance_object.co_ordinator

        # set Source item List
        src_item_list = []
        for each_disk in disk_name:
            src_item_list.append("\\" + vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        _disk_restore_option['paths'] = src_item_list

        self._set_restore_inputs(
            _disk_restore_option,
            in_place=False,
            copy_precedence=copy_precedence,
            destination_path=destination_path,
            paths=src_item_list
        )

        request_json = self._prepare_disk_restore_json(_disk_restore_option)
        return self._process_restore_response(request_json)

    def attach_disk_restore(self,
                            vm_name,
                            vcenter,
                            esx=None,
                            datastore=None,
                            proxy_client=None,
                            copy_precedence=0,
                            media_agent=None,
                            snap_proxy=None,
                            disk_name=None,
                            destinationVM = None,
                            destinationVMGUID = None,
                            datacenter = None,
                            cluster = None):
        """Attaches the Disks to the provided vm

            Args:
                vm_name             (basestring)    --  Name of the VM added in subclient content
                                                        whose  disk is selected for restore

                vcenter             (dict)          --  Dictinoary of vcenter, username and creds

                esx                 (basestring)    --  Esx host where the vm resides

                datastore               (string)    --  Datastore where disks will be restoed to
                                                        default: None

                proxy_client        (basestring)    --  Destination proxy client to be used
                                                        default: None

                copy_precedence            (int)    --  SP copy precedence from which browse has to
                                                         be performed

                media_agent                 (str)   -- MA needs to use for disk browse
                    default :Storage policy MA

                snap_proxy                   (str)   -- proxy need to be used for disk
                                                    restores from snap
                    default :proxy in instance or subclient

                disk_name                    (str)  --  Prefix of the disk name to be attached
                                                        defaul: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not passed in proper expected format

                    if response is empty

                    if response is not success
        """
        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _attach_disk_restore_option = {}
        disk_name = []

        # check if inputs are correct
        if not (isinstance(vm_name, basestring) and
                isinstance(disk_name, list)):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            _attach_disk_restore_option['copy_precedence_applicable'] = True

        # fetching all disks from the vm
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + vm_ids[vm_name])

        if not disk_name:  # if disk names are not provided, restore all vmdk disks
            for each_disk_path in disk_list:
                disk_name.append(each_disk_path.split('\\')[-1])

        else:  # else, check if the given VM has a disk with the list of disks in disk_name.
            for each_disk in disk_name:
                each_disk_path = "\\" + str(vm_name) + "\\" + each_disk
                if each_disk_path not in disk_list:
                    raise SDKException('Subclient', '111')

        if proxy_client is not None:
            _attach_disk_restore_option['client'] = proxy_client
        else:
            _attach_disk_restore_option['client'] = self._backupset_object._instance_object.co_ordinator

        # set Source item List
        src_item_list = []
        for each_disk in disk_name:
            src_item_list.append("\\" + vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        _attach_disk_restore_option['paths'] = src_item_list
        _attach_disk_restore_option['newName'] = destinationVM
        _attach_disk_restore_option['newGUID'] = destinationVMGUID
        _attach_disk_restore_option['datacenter'] = datacenter
        _attach_disk_restore_option['cluster'] = cluster

        self._set_restore_inputs(
            _attach_disk_restore_option,
            in_place=False,
            copy_precedence=copy_precedence,
            vm_to_restore=vm_name,
            esxHost=vcenter['vcenter'],
            userName=vcenter['user'],
            password=vcenter['password'],
            esx=esx,
            paths=src_item_list,
            datastore=datastore,
            volume_level_restore=6,
        )

        request_json = self._prepare_attach_disk_restore_json(_attach_disk_restore_option)
        return self._process_restore_response(request_json)
