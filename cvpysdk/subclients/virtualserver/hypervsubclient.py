#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for operating on a Virtual Server Hyper-V Subclient.

HyperVSubclient is the only class defined in this file.

HyperVSubclient:    Derived class from VirtualServerSubClient Base class, representing a
                        Hyper-V Subclient, and to perform operations on that Subclient

HyperVSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)       --  initialize instance of the hyper-v subclient class associated with
                                    the VirtualServer subclient given with the subclient name & id

    disk_restore()          --  runs Disk Restore on Hyper-V Subclient

"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException
from ...client import Client


class HyperVSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
        Hyper-V  virtual server subclient,and to perform operations on that subclient.
    """

    def disk_restore(
            self,
            vm_name=None,
            destination_client=None,
            destination_path=None,
            overwrite=False,
            disk_name=None,
            convert_to=None):
        """Restores the disk specified in the input paths list to the same location.

            Args:
                vm_name             (str)   --  VM from which disk is to be restored

                destination_client  (str)   --  Destination client to whihc disk is to be restored

                client              (str)   --  name of the client to restore disk

                destinationpath     (str)   --  path where the disk needs to be restored

                disk_name           (str)   --  name of the disk which has to be restored

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
                isinstance(vm_name, (str, list))):
            raise SDKException('Subclient', '101')

        _disk_restore_option["unconditional_overwrite"] = overwrite
        self._restore_commonOptions_json(_disk_restore_option)

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._instance_object.co_ordinator

        if isinstance(destination_client, Client):
            client = destination_client
        elif isinstance(destination_client, str):
            client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        _disk_restore_option["client_name"] = client.client_name
        self._restore_destination_json(_disk_restore_option)

        # if conversion option is given
        if convert_to is not None:
            _disk_extn = self._get_disk_Extension(disk_name)
            if isinstance(_disk_extn, list):
                raise SDKException('Subclient', '101')
            else:
                destination_vendor, destination_disktype = self._get_conversion_disk_Type(
                    _disk_extn, convert_to
                )
                _disk_restore_option["destination_vendor"] = destination_vendor
                _disk_restore_option["destination_disktype"] = destination_disktype
        else:
            destination_vendor = self._backupset_object._instance_object._vendorid
            _disk_restore_option["destination_vendor"] = destination_vendor
            _disk_restore_option["destination_disktype"] = 4

        self._restore_volumeRstOption_json(_disk_restore_option)

        # if disk list is given
        disk_list, _ = self.disk_level_browse("\\" + _vm_ids[vm_name])

        if disk_name is not None:
            if disk_name in disk_list:
                disk_list = list(disk_list)
            else:
                raise SDKException('Subclient', '111')

        # set Source item List
        _src_item_list = []
        for each_disk in disk_list:
            _src_item_list.append("\\\\" + _vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        _disk_restore_option["source_item"] = _src_item_list
        self._restore_fileoption_json(_disk_restore_option)

        # set the rest setter
        self._impersonation_json(_disk_restore_option)
        self._restore_browse_option_json(_disk_restore_option)
        self._restore_virtualServerRstOption_json(_disk_restore_option)
        self._restore_diskLevelVMRestoreOption_json(_disk_restore_option)

        request_json = self._prepare_disk_restore_json()

        return self._process_restore_response(request_json)
