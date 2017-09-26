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

HyperVInstance:

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
from ...client import Client


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
        if not (isinstance(destination_path, str) and
                isinstance(overwrite, bool)and
                (isinstance(vm_name, str) or (isinstance(vm_name, list)))):
            raise SDKException('Subclient', '101')

        _disk_restore_option["unconditional_overwrite"] = overwrite
        self._restore_commonOptions_json(_disk_restore_option)

        client = self._set_default_client(destination_client)
        _disk_restore_option["client_name"] = client.client_name
        self._restore_destination_json(_disk_restore_option)

        # if conversion option is given
        if not convert_to is None:
            _disk_extn = self._get_disk_extension(disk_name)
            if isinstance(_disk_extn, list):
                raise SDKException('Subclient', '101')
            else:
                _disk_restore_option["destination_vendor"], \
                    _disk_restore_option["destination_disktype"] = \
                    self._get_conversion_disk_type(_disk_extn, convert_to)

        else:
            _disk_restore_option["destination_vendor"] = \
                self._backupset_object._instance_object._vendorid
            _disk_restore_option["destination_disktype"] = 4

        self._json_restore_volumeRstOption(_disk_restore_option)

        # if disk list is given
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + _vm_ids[vm_name])

        if not disk_name is None:
            if disk_name in disk_list:
                disk_list = list(disk_list)
            else:
                raise SDKException('Subclient', '111')

        # set Source item List
        _src_item_list = []
        for each_disk in disk_list:
            _src_item_list.append(
                "\\\\" + _vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        _disk_restore_option["source_item"] = _src_item_list
        self._restore_fileoption_json(_disk_restore_option)

        # set the rest setter
        self._impersonation_json(_disk_restore_option)
        self._restore_browse_option_json(_disk_restore_option)
        self._json_restore_virtualServerRstOption(_disk_restore_option)
        self._json_restore_diskLevelVMRestoreOption(_disk_restore_option)

        request_json = self._prepare_disk_restore_json()

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

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if destination_path is not a string

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict_from_browse()

        # restore options
        if restore_option is None:
            restore_option = {}

        # check input parameters are correct
        if bool(restore_option):
            if not (isinstance(destination_path, str) and
                    isinstance(overwrite, bool) and
                    isinstance(power_on, bool) and
                    isinstance(add_to_failover, bool)):
                raise SDKException('Subclient', '101')

        client = self._set_default_client(destination_client)
        restore_option["client_name"] = client.client_name

        restore_option['vm_to_restore'] = self._set_vm_to_restore(vm_to_restore,restore_option)

        # set attr for all the option in restore xml from user inputs
        self._set_advanced_attribute(restore_option,unconditional_overwrite= overwrite,\
                                        power_on = power_on,add_to_failover = add_to_failover, \
                                        destination_path = destination_path)

        # set common parameters
        self._restore_commonOptions_json(restore_option)
        self._impersonation_json(restore_option)
        self._json_restore_volumeRstOption(restore_option)
        self._restore_commonOptions_json(restore_option)
        self._restore_browse_option_json(restore_option)
        self._restore_destination_json(restore_option)
        self._json_restore_diskLevelVMRestoreOption(restore_option)
        self._json_restore_virtualServerRstOption(restore_option)

        # set advanced restore options
        vm_disks = []
        restore_option['source_item'] = []
        for _each_vm_to_restore in restore_option['vm_to_restore']:

            # populate restore source item
            restore_option['source_item'].append(
                _vm_ids[_each_vm_to_restore])

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
            self._set_vm_attribute(restore_option,disks = vm_disks,guid = _vm_ids[_each_vm_to_restore], \
                                   restore_new_name = restore_option.get("restore_new_name",\
                                  ("Delete" + _each_vm_to_restore)),esxHost = vs_metadata['esxHost'], \
                                   name = _each_vm_to_restore)
            

            self._json_restore_advancedRestoreOptions(restore_option)
            self._advanced_restore_option(
                self._advanced_option_restore_json)

        self._restore_fileoption_json(restore_option)

        request_json = self._prepare_fullvm_restore_json()

        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=False,
                                 power_on=False,
                                 copy_precedence=0,
                                 add_to_failover=False):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore         (list)       --  provide the VM name to restore

                overwrite
                        default:False   (bool)      --  overwrite the existing VM

                poweron
                        default:False   (bool)      --  power on the  restored VM

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
        self._set_advanced_attributes(restore_option,unconditional_overwrite= overwrite,\
                                        power_on = power_on,add_to_failover = add_to_failover)
        
       
        # set common parameters
        self._restore_commonOptions_json(restore_option)
        self._impersonation_json(restore_option)
        self._json_restore_volumeRstOption(restore_option)
        self._restore_commonOptions_json(restore_option)
        self._restore_browse_option_json(restore_option)
        self._restore_destination_json(restore_option)
        self._json_restore_diskLevelVMRestoreOption(restore_option)
        self._json_restore_virtualServerRstOption(restore_option)

        # set advanced restore options
        vm_disks = []
        restore_option['source_item'] = []
        for _each_vm_to_restore in restore_option['vm_to_restore']:

            # vs metadata from browse result
            _metadata =  browse_result[1][str('\\' + _each_vm_to_restore)]
            vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]

            # populate restore source item
            restore_option['source_item'].append(
                _vm_ids[_each_vm_to_restore])

            # populate restore disk
            disk_list, disk_info_dict = self.disk_level_browse(
                "\\\\" + _vm_ids[_each_vm_to_restore])
            for disk, data in disk_info_dict.items():
                disk_dict = {
                    "name": disk.split('\\')[-1],
                    "DestinationPath": data["advanced_data"]["browseMetaData"]
                                                ["virtualServerMetaData"]['datastore']
                }

                vm_disks.append(disk_dict)

            if vm_disks == []:
                raise SDKException('Subclient', 104)

            # populate VM Specific values
            self._set_vm_attributes(restore_option,disks = vm_disks,guid = _vm_ids[_each_vm_to_restore], \
                                   restore_new_name = _each_vm_to_restore,esxHost = vs_metadata['esxHost'], \
                                   name = _each_vm_to_restore)

            self._json_restore_advancedRestoreOptions(restore_option)
            self._advanced_restore_option(
                self._advanced_option_restore_json)

        self._restore_fileoption_json(restore_option)

        request_json = self._prepare_fullvm_restore_json()

        return self._process_restore_response(request_json)
