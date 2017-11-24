#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server VMWare Subclient.

VMWareVirtualServerSubclient is the only class defined in this file.

VMWareVirtualServerSubclient:   Derived class from VirtualServerSubClient Base
                                class,representing a VMware Subclient,
                                and to perform operations on that Subclient

VMWareVirtualServerSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of vmware subclient class,
                                    associated with the VirtualServer subclient

    full_vm_restore_in_place()  --  restores the VM specified by the user to
                                    the same location

    full_vm_restore_out_of_place() -- restores the VM specified to the provided
                                      VMware psuedoclient vcenter via
                                      vcenter_client

"""

from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException
from past.builtins import basestring


class VMWareVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a VMWare virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            destination_client=None):
        """Restores the FULL Virtual machine specified in the input list
            to the location same as the actual location of the VM in VCenter.

            Args:
                vm_to_restore       (list)     --  provide the VM name to
                                                   restore
                                                   default: None

                overwrite           (bool)     --  overwrite the existing VM
                                                   default: True

                power_on            (bool)     --  power on the  restored VM
                                                   default: True

                copy_precedence     (int)      --  copy precedence value
                                                   default: 0

                destination_client (basestring)  -- proxy client to be used for
                                                    restore
                                                    default: proxy added in
                                                    subclient

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        restore_option = {}

        # check input parameters are correct
        if bool(restore_option):
            if not isinstance(vm_to_restore, basestring):
                raise SDKException('Subclient', '101')

        restore_option['vm_to_restore'] = self._set_vm_to_restore(vm_to_restore)
        browse_result = self.vm_files_browse()

        # set attr for all the option in restore xml from user inputs
        self._set_advanced_attributes(
            restore_option,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_preecedence=copy_precedence
        )

        restore_option['volume_level_restore'] = 1
        restore_option['source_item'] = []

        # set esx info
        if self._backupset_object._instance_object.server_host_name[0]:
            restore_option['esx_server'] = \
                self._backupset_object._instance_object.server_host_name[0]
        else:
            restore_option['esx_server'] = ""

        for _each_vm_to_restore in restore_option['vm_to_restore']:
            vm_disks = []

            # vs metadata from browse result
            _metadata = browse_result[1][('\\' + _each_vm_to_restore)]
            vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]

            # populate restore source item
            restore_option['source_item'].append("\\" + vm_ids[_each_vm_to_restore])

            # populate restore disk
            disk_list, disk_info_dict = self.disk_level_browse(
                "\\\\" + vm_ids[_each_vm_to_restore])

            datastore = ""

            for disk, data in disk_info_dict.items():
                datastore = data["advanced_data"]["browseMetaData"][
                    "virtualServerMetaData"]['datastore']

                disk_dict = {
                    "name": disk.split('\\')[-1],
                    "Datastore": datastore
                }

                vm_disks.append(disk_dict)

            if not vm_disks:
                raise SDKException('Subclient', 104)

            # prepare nics info json
            nics_list = self._json_nics_advancedRestoreOptions(_each_vm_to_restore)

            # populate vcenter details
            instance_dict = self._backupset_object._instance_object._properties['instance']

            if instance_dict:
                restore_option['client_name'] = instance_dict['clientName']
                restore_option['instanceName'] = instance_dict['instanceName']
                restore_option['appName'] = instance_dict['appName']

            # populating destination client, it assumes the proxy controller added
            # in instance properties if not specified
            if destination_client is not None:
                restore_option['destination_client_name'] = destination_client
            else:
                restore_option['destination_client_name'] = \
                    self._set_default_client(destination_client).client_name

            # populate VM Specific values
            self._set_vm_attributes(
                restore_option,
                disks=vm_disks,
                nics=nics_list,
                guid=vm_ids[_each_vm_to_restore],
                new_name=_each_vm_to_restore,
                esx_host=vs_metadata['esxHost'],
                name=_each_vm_to_restore,
                datastore=datastore
            )

            self._json_restore_advancedRestoreOptions(restore_option)
            self._advanced_restore_option(self._advanced_option_restore_json)

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            vcenter_client=None,
            new_name=None,
            esx_host=None,
            datastore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option=0,
            transport_mode=0,
            destination_client=None):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore     (list)  --  provide the VM name to restore
                                              default: None

                vcenter_client    (basestring) -- name of the vcenter client
                                                  where the VM should be
                                                    restored.

                new_name          (basestring) -- new name to be given to the
                                                    restored VM

                esx_host          (basestring) -- destination esx host
                                                    restores to the source VM
                                                    esx if this value is not
                                                    specified

                datastore         (basestring) -- datastore where the
                                                  restored VM should be located
                                                  restores to the source VM
                                                  datastore if this value is
                                                  not specified

                overwrite         (bool)       -- overwrite the existing VM
                                                  default: True

                power_on          (bool)       -- power on the  restored VM
                                                  default: True

                copy_precedence   (int)        -- copy precedence value
                                                  default: 0

                disk_option       (basestring) -- disk provisioning for the
                                                  restored vm
                                                  default: 0 which is equivalent
                                                  to Original

                transport_mode    (basestring) -- transport mode to be used for
                                                  the restore.
                                                  default: 0 representing
                                                  the auto mode.

                destination_client (basestring)-- proxy client



            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        restore_option = {}

        # check mandatory input parameters are correct
        if bool(restore_option):
            if not isinstance(vm_to_restore, basestring):
                raise SDKException('Subclient', '101')

        restore_option['vm_to_restore'] = self._set_vm_to_restore(vm_to_restore)
        restore_option['disk_option'] = disk_option
        restore_option['transport_mode'] = transport_mode
        restore_option['copy_preceedence'] = copy_precedence

        # set attr for all the option in restore xml from user inputs
        self._set_advanced_attributes(
            restore_option,
            unconditional_overwrite=overwrite,
            power_on=power_on
        )

        restore_option['volume_level_restore'] = 1
        restore_option['source_item'] = []

        # set esx info
        if self._backupset_object._instance_object.server_host_name[0]:
            restore_option['esx_server'] = \
                self._backupset_object._instance_object.server_host_name[0]
        else:
            restore_option['esx_server'] = ""

        for _each_vm_to_restore in restore_option['vm_to_restore']:

            # Set the new name for the restored VM.
            # If new_name is not given, it restores the VM with same name
            # with suffix Delete.

            if new_name is not None:
                restore_option['new_name'] = new_name

            else:
                restore_option['new_name'] = "Delete" + _each_vm_to_restore

            browse_result = self.vm_files_browse()

            # setting disks for restore
            vm_disks = []

            # vs metadata from browse result
            _metadata = browse_result[1][('\\' + _each_vm_to_restore)]
            vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]

            # populate restore source item
            restore_option['source_item'].append("\\" + vm_ids[_each_vm_to_restore])

            # populate restore disk
            disk_list, disk_info_dict = self.disk_level_browse(
                "\\\\" + vm_ids[_each_vm_to_restore])

            for disk, data in disk_info_dict.items():

                if datastore is not None:
                    restore_datastore = datastore
                else:
                    restore_datastore = data["advanced_data"]["browseMetaData"][
                        "virtualServerMetaData"]["datastore"]

                disk_dict = {
                    "name": disk.split('\\')[-1],
                    "Datastore": restore_datastore
                }

                vm_disks.append(disk_dict)

            if not vm_disks:
                raise SDKException('Subclient', 104)

            # prepare nics info json
            nics_list = self._json_nics_advancedRestoreOptions(_each_vm_to_restore)

            # populate vcenter details
            instance_dict = self._backupset_object._instance_object._properties['instance']

            restore_option['client_name'] = ""
            if instance_dict:
                if vcenter_client is not None:

                    restore_option['client_name'] = vcenter_client
                else:
                    restore_option['client_name'] = instance_dict['clientName']

                restore_option['instanceName'] = instance_dict['instanceName']
                restore_option['appName'] = instance_dict['appName']

            # populating destination client, it assumes the proxy controller added
            # in instance properties if not specified
            if destination_client is not None:
                restore_option['destination_client_name'] = destination_client
            else:
                restore_option['destination_client_name'] = self._set_default_client(
                    destination_client).client_name

            if esx_host is not None:
                restore_esx_host = esx_host
            else:
                restore_esx_host = vs_metadata['esxHost']

            # populate VM Specific values
            self._set_vm_attributes(
                restore_option,
                disks=vm_disks,
                nics=nics_list,
                guid=vm_ids[_each_vm_to_restore],
                esx_host=restore_esx_host,
                name=_each_vm_to_restore,
                datastore=restore_datastore
            )

            self._json_restore_advancedRestoreOptions(restore_option)
            self._advanced_restore_option(self._advanced_option_restore_json)

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def disk_restore(self,
                     vm_name=None,
                     destination_client=None,
                     staging_path=None,
                     copy_precedence=0,
                     disk_name=None,
                     convert_to=None):
        """Restores the disk specified in the input paths list to the same location

            Args:
                vm_name             (basestring)   -- Name of the VM added in
                                                      subclient content whose
                                                      disk is selected for
                                                      restore

                destination_client  (basestring)   -- Destination client where
                                                      the disk should be restored

                staging_path        (basestring)   -- Staging path to restore
                                                      the disk.

                copy_precedence     (int)          -- SP copy precedence from
                                                      which browse has to be
                                                      performed

                disk_name           (basestring)   -- name of the disk which
                                                      has to be restored

                convert_to          (basestring)   -- disk format for the
                                                      restored disk(applicable
                                                      only when the vmdk disk
                                                      is selected for restore)
                                                      default: None
            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not passed in proper expected format

                    if response is empty

                    if response is not success
        """

        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        disk_restore_option = {}

        # check if inputs are correct
        if not (isinstance(staging_path, basestring) and
                isinstance(vm_name, basestring)):
            raise SDKException('Subclient', '101')

        disk_restore_option['copy_preecedence'] = copy_precedence

        if destination_client is not None:
            disk_restore_option["destination_client_name"] = destination_client
        else:
            disk_restore_option["destination_client_name"] = self._set_default_client(
                destination_client).client_name

        disk_restore_option["destination_path"] = staging_path

        # fetching all disks from the vm
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + vm_ids[vm_name])

        # check if the given VM has a disk with the given disk_name
        # else it raised exception
        if disk_name is not None:
            disk_path = "\\" + str(vm_name) + "\\" + disk_name
            if disk_path in disk_list:
                disks = []
                disks.append(disk_name)
                disk_list = disks
            else:
                raise SDKException('Subclient', '111')

        # if conversion option is given
        if convert_to is not None and disk_name is not None:
            disk_extn = self._get_disk_extension(disk_list)
            if not isinstance(disk_extn, list):
                raise SDKException('Subclient', '101')
            else:
                if "vmdk" in disk_extn:
                    disk_restore_option["destination_vendor"], \
                        disk_restore_option["destination_disktype"] = \
                        self._get_conversion_disk_type(disk_extn, convert_to)

        else:
            disk_restore_option["destination_vendor"] = \
                self._backupset_object._instance_object._vendor_id
            disk_restore_option["destination_disktype"] = 4

        instance_dict = self._backupset_object._instance_object._properties['instance']

        disk_restore_option['client_name'] = ""
        if instance_dict:
            disk_restore_option['client_name'] = instance_dict['clientName']
            disk_restore_option['instanceName'] = instance_dict['instanceName']
        # set Source item List
        src_item_list = []
        for each_disk in disk_list:
            src_item_list.append(
                "\\" + vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        disk_restore_option["source_item"] = src_item_list

        request_json = self._prepare_disk_restore_json(disk_restore_option)
        return self._process_restore_response(request_json)
