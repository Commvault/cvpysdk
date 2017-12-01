#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ?2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Hyper-V Subclient.

HyperVVirtualServerSubclient is the only class defined in this file.

HyperVVirtualServerSubclient: Derived class from VirtualServerSubClient  Base class, representing a
                           Hyper-V Subclient, and to perform operations on that Subclient

HypervSubclient:

    __init__(,backupset_object, subclient_name, subclient_id)    --  initialize object of hyper-v
                                                                             subclient object
                                                                                 associated with
                                                                        the VirtualServer subclient

    disk_restore()                                               -- Perform Disk Restore on
                                                                        Hyper-V Subclient

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                     to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()              --  restores the VM specified by the
                                                    user to the same location
"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException
from past.builtins import basestring


class HyperVVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    Hyper-V  virtual server subclient,and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                            backupset class, subclient name, subclient id

                """
        super(HyperVVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def disk_restore(self,
                     vm_name=None,
                     destination_client=None,
                     destination_path=None,
                     overwrite=False,
                     copy_preceedence=0,
                     disk_name=None,
                     convert_to=None):
        """Restores the disk specified in the input paths list to the same location

            Args:
                vm_name             (str)   -- VM from which disk is to be restored

                destination_client  (str)   -- Destination client to whihc disk is to be restored

                client              (str)   --  name of the client to restore disk

                destinationpath     (str)   --path where the disk needs to be restored

                copy_preceedence    (int)   -- SP copy precedence from which browse
                                                    has to be performed

                disk_Name           (str)   -- name of the disk which has to be restored

                overwrite           (bool)  --  unconditional overwrite files during restore
                    default: True

                convert_to          (str)   --  to convert the disk to the specified format
                    default: None


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if destinationpath is not str

                    if client is not str or object

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _disk_restore_option = {}

        # check if inputs are correct
        if not (isinstance(destination_path, basestring) and
                isinstance(overwrite, bool)and
                (isinstance(vm_name, basestring) or (isinstance(vm_name, list)))):
            raise SDKException('Subclient', '101')

        _disk_restore_option["unconditional_overwrite"] = overwrite

        client = self._set_default_client(destination_client)
        _disk_restore_option["destination_client_name"] = client.client_name
        _disk_restore_option["destination_path"] = destination_path

        # if disk list is given
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + _vm_ids[vm_name])

        if disk_name is not None:
            if disk_name in disk_list:
                disk_list = list(disk_name)
            else:
                raise SDKException('Subclient', '111')

        # if conversion option is given
        if convert_to is not None:
            _disk_extn = self._get_disk_extension(disk_list)
            if isinstance(_disk_extn, list):
                raise SDKException('Subclient', '101')
            else:
                _disk_restore_option["destination_vendor"], \
                    _disk_restore_option["destination_disktype"] = \
                    self._get_conversion_disk_type(_disk_extn, convert_to)

        else:
            _disk_restore_option["destination_vendor"] = \
                self._backupset_object._instance_object._vendor_id
            _disk_restore_option["destination_disktype"] = 4


        # set Source item List
        _src_item_list = []
        for each_disk in disk_list:
            _src_item_list.append(
                "\\" + _vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        _disk_restore_option["source_item"] = _src_item_list
        # _disk_restore_option["browse_filters"] = constants.browse_filters()

        request_json = self._prepare_disk_restore_json(_disk_restore_option)

        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(self,
                                     destination_client=None,
                                     destination_path=None,
                                     vm_to_restore=None,
                                     overwrite=False,
                                     power_on=False,
                                     copy_precedence=0,
                                     add_to_failover=False,
                                     restore_new_name=None,
                                     restore_option=None):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            at the specified destination location.

            Args:
                client                (str/object) --  either the name of the client or
                                                           the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                vm_to_restore         (list)       --  provide the VM name to restore

                overwrite
                        default:False   (bool)      --  overwrite the existing VM

                poweron
                        default:False   (bool)      --  power on the  restored VM

                add_to_failover
                        default:False   (bool)      --  Add the Restored VM to Failover Cluster


                restore_option      (dict)     --  complete dictionary with all advanced optio
                    default: {}

        value:
            preserve_level           (int)    -  set the preserve level in restore
            unconditional_overwrite  (bool)  - unconditionally overwrite the disk
                                                in the restore path

            destination_path         (str)   - path where the disk needs to be restored
            client_name              (str)  - client where the disk needs to be restored

            destination_vendor      (int)    - vendor id of the Hypervisor
            destination_disktype    (str)   - type of disk needs to be restored like VHDX,VHD,VMDK
            source_item              (str)   - GUID of VM from which disk needs to be restored
                                            eg:\\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA
            copy_precedence_applicable (str) - True if needs copy_preceedence to be honoured
                                                                                        else False
            copy_preceedence           (int) - the copy id from which browse and
                                                            restore needs to be performed

            power_on                   (bool) - power on the VM after restore
            add_to_failover            (bool)- Register the VM to Failover Cluster
            datastore                  (str) - Datastore where the VM needs to be restored

            disks   (list of dict)     (list) - list with dict for each disk in VM
                                            eg: [{
                                                    name:"disk1.vmdk"
                                                    datastore:"local"
                                                }
                                                {
                                                    name:"disk2.vmdk"
                                                    datastore:"local1"
                                                }
                                            ]
            guid                        (str)- GUID of the VM needs to be restored
            new_name                    (str)- New name for the VM to be restored
            esx_host                    (str)- esx_host or client name where it need to be restored
            name                        (str)- name of the VM to be restored

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if destination_path is not a string

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        self._advanced_restore_option_list = []
        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        browse_result = self.vm_files_browse()

        # restore options
        if restore_option is None:
            restore_option = {}

        # check input parameters are correct
        if bool(restore_option):
            if not (isinstance(destination_path, basestring) and
                    isinstance(overwrite, bool) and
                    isinstance(power_on, bool) and
                    isinstance(add_to_failover, bool)):
                raise SDKException('Subclient', '101')

        client = self._set_default_client(destination_client)
        restore_option["destination_client_name"] = client.client_name
        restore_option["copy_precedence"] = copy_precedence

        restore_option['vm_to_restore'] = self._set_vm_to_restore(vm_to_restore, restore_option)

        # set attr for all the option in restore xml from user inputs
        self._set_advanced_attributes(restore_option, unconditional_overwrite=overwrite,
                                      power_on=power_on, add_to_failover=add_to_failover,
                                      destination_path=destination_path)

        # set advanced restore options
        restore_option['volume_level_restore'] = 1
        restore_option['source_item'] = []
        for _each_vm_to_restore in restore_option['vm_to_restore']:

            # vs metadata from browse result
            vm_disks = []
            _metadata = browse_result[1][('\\' + _each_vm_to_restore)]
            vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]

            # populate restore source item
            restore_option['source_item'].append(
                "\\" + _vm_ids[_each_vm_to_restore])

            # populate restore disk
            disk_list, disk_info_dict = self.disk_level_browse(
                "\\" + _vm_ids[_each_vm_to_restore])

            for each_disk in disk_list:
                disk_dict = {
                    "name": each_disk.split("\\")[-1],
                    "DestinationPath": restore_option['destination_path']
                }

                vm_disks.append(disk_dict)

            if vm_disks == []:
                raise SDKException('Subclient', 104)

            # populate VM Specific values
            self._set_vm_attributes(restore_option, disks=vm_disks,
                                    guid=_vm_ids[_each_vm_to_restore],
                                    new_name=restore_option.get(
                                        "restore_new_name", (
                                            "Delete" + _each_vm_to_restore)),
                                    esx_host=vs_metadata['esxHost'],
                                    name=_each_vm_to_restore)

            self._json_restore_advancedRestoreOptions(restore_option)
            self._advanced_restore_option(
                self._advanced_option_restore_json)

        request_json = self._prepare_fullvm_restore_json(restore_option)

        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 copy_precedence=0,
                                 add_to_failover=False):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore         (list)       --  provide the VM name to restore

                overwrite
                        default:true   (bool)      --  overwrite the existing VM

                poweron
                        default:true   (bool)      --  power on the  restored VM

                add_to_failover
                        default:False   (bool)      --  Add the Restored VM to Failover Cluster

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        self._advanced_restore_option_list = []
        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        restore_option = {}

        # check input parameters are correct
        if bool(restore_option):
            if not (isinstance(overwrite, bool) and
                    isinstance(power_on, bool) and
                    isinstance(add_to_failover, bool)):
                raise SDKException('Subclient', '101')

        restore_option['vm_to_restore'] = self._set_vm_to_restore(vm_to_restore)
        browse_result = self.vm_files_browse()

        # set attr for all the option in restore xml from user inputs
        self._set_advanced_attributes(restore_option, unconditional_overwrite=overwrite,
                                      power_on=power_on, add_to_failover=add_to_failover)

        # set advanced restore options
        restore_option['volume_level_restore'] = 1
        restore_option['source_item'] = []
        for _each_vm_to_restore in restore_option['vm_to_restore']:

            # vs metadata from browse result
            vm_disks = []
            _metadata = browse_result[1][('\\' + _each_vm_to_restore)]
            vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]

            # populate restore source item
            restore_option['source_item'].append(
                "\\" + _vm_ids[_each_vm_to_restore])

            # populate restore disk
            disk_list, disk_info_dict = self.disk_level_browse(
                "\\\\" + _vm_ids[_each_vm_to_restore])
            for disk, data in disk_info_dict.items():
                destination_path = data["advanced_data"]["browseMetaData"][
                    "virtualServerMetaData"]['datastore']

                disk_dict = {
                    "name": disk.split('\\')[-1],
                    "DestinationPath": destination_path
                }

                vm_disks.append(disk_dict)

            if vm_disks == []:
                raise SDKException('Subclient', 104)

            # populate VM Specific values
            self._set_vm_attributes(restore_option, disks=vm_disks,
                                    guid=_vm_ids[_each_vm_to_restore],
                                    new_name=_each_vm_to_restore, esx_host=vs_metadata['esxHost'],
                                    name=_each_vm_to_restore, destination_path=destination_path,
                                    destination_client_name=vs_metadata['esxHost'])

            self._json_restore_advancedRestoreOptions(restore_option)
            self._advanced_restore_option(
                self._advanced_option_restore_json)

        request_json = self._prepare_fullvm_restore_json(restore_option)

        return self._process_restore_response(request_json)
