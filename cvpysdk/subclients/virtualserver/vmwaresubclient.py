#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server VMWare Subclient.

VMWareVirtualServerSubclient is the only class defined in this file.

VMWareVirtualServerSubclient:   Derived class from VirtualServerSubClient Base class,
                                    representing a VMware Subclient,
                                    and to perform operations on that Subclient

VMWareVirtualServerSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of vmware subclient class,
                                        associated with the VirtualServer subclient

    full_vm_restore_in_place()  --  restores the VM specified by the user to the same location

"""

from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class VMWareVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class,
        represents a VMWare virtual server subclient,
        and to perform operations on that subclient.

    """

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            add_to_failover=False):
        """Restores the FULL Virtual machine specified in the input list
            to the location same as the actual location of the VM in VCenter.

            Args:
                vm_to_restore       (list)  --  provide the VM name to restore
                    default: None

                overwrite           (bool)  --  overwrite the existing VM
                    default: True

                power_on            (bool)  --  power on the  restored VM
                    default: True

                copy_precedence     (int)   --  copy precedence value
                    default: 0

                add_to_failover     (bool)  --  add the Restored VM to Failover Cluster
                    default: False

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        __, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        restore_option = {}

        # check input parameters are correct
        if bool(restore_option):
            if not (isinstance(overwrite, bool) and
                    isinstance(power_on, bool) and
                    isinstance(add_to_failover, bool) and
                    isinstance(copy_precedence, int)):
                raise SDKException('Subclient', '101')

        restore_option['vm_to_restore'] = self._set_vm_to_restore(vm_to_restore)
        browse_result = self.vm_files_browse()

        # set attr for all the option in restore xml from user inputs
        self._set_advanced_attributes(
            restore_option,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            add_to_failover=add_to_failover
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
            __, disk_info_dict = self.disk_level_browse("\\\\" + vm_ids[_each_vm_to_restore])

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
            #added these to vssubclient.py - need to validate with official
            #self._json_vcenter_instance(restore_option)
            #self._json_restore_diskLevelVMRestoreOption(restore_option)

        request_json = self._prepare_fullvm_restore_json(restore_option)

        return self._process_restore_response(request_json)
