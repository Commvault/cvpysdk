# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
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

from enum import Enum
from past.builtins import basestring
from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException
from .vmwaresubclient import VMWareVirtualServerSubclient



class HyperVVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    Hyper-V  virtual server subclient,and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """

        super(HyperVVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = [".vhd", ".avhd", ".avhdx", ".vhdx"]

    class disk_pattern(Enum):
        """
        stores the disk pattern of all hypervisors
        """
        name = "name"
        datastore = "DestinationPath"
        new_name = "new_name"


    def _get_guest_os(self, os_name):
        """
        stores all the XML tag for OS
        """

        _os_name_dict ={
            "2012" : "windows8Server64Guest"
        }

        for os in _os_name_dict.keys():
            if os in os_name:
                return _os_name_dict[os]

        raise SDKException('Subclient', '102', "Input parameter specified is incorrect" )

    def disk_restore(self,
                     vm_name,
                     destination_path,
                     proxy_client=None,
                     disk_name=None,
                     copy_precedence=0,
                     convert_to=None):
        """Restores the disk specified in the input paths list to the same location

            Args:
                vm_name             (str)   -- VM from which disk is to be restored

                proxy_client  (str)   -- Destination client to whihc disk is to be restored

                client              (str)   --  name of the client to restore disk

                destinationpath     (str)   --path where the disk needs to be restored

                copy_precedence    (int)   -- SP copy precedence from which browse
                                                    has to be performed

                disk_Name           (str)   -- name of the disk which has to be restored

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
                (isinstance(vm_name, basestring) or (isinstance(vm_name, list)))):
            raise SDKException('Subclient', '101')


        if proxy_client is None:
            _disk_restore_option[
                "client"] = self._backupset_object._instance_object.co_ordinator
        else:
            _disk_restore_option["client"] = proxy_client

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
            _disk_restore_option["destination_disktype"] = 0

        _disk_restore_option["volume_level_restore"] = 4


        # set Source item List
        _src_item_list = []
        for each_disk in disk_list:
            _src_item_list.append(
                "\\" + _vm_ids[vm_name] + "\\" + each_disk.split("\\")[-1])

        self._set_restore_inputs(
            _disk_restore_option,
            in_place=False,
            copy_precedence=copy_precedence,
            destination_path=destination_path,
            paths=_src_item_list
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
                                     restored_vm_name=None,
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
            destination_client      (str)  - Hyperv Host Client Name where VM needs to be restored

            destination_vendor      (int)    - vendor id of the Hypervisor
            destination_disktype    (str)   - type of disk needs to be restored like VHDX,VHD,VMDK
            source_item              (str)   - GUID of VM from which disk needs to be restored
                                            eg:\\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA
            copy_precedence_applicable (str) - True if needs copy_precedence to be honoured
                                                                                        else False
            copy_precedence           (int) - the copy id from which browse and
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

        # restore options
        if restore_option is None:
            restore_option = {}

        if vm_to_restore and not isinstance(vm_to_restore, basestring):
            raise SDKException('Subclient', '101')

        if not restored_vm_name and isinstance(vm_to_restore, basestring):
            restored_vm_name = "Delete" + vm_to_restore

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True

        if restored_vm_name:
            if not (isinstance(vm_to_restore, basestring) or
                        isinstance(restored_vm_name, basestring)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_vm_name

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        # check mandatory input parameters are correct
        if bool(restore_option):
            if not (isinstance(destination_path, basestring) and
                    isinstance(overwrite, bool) and
                    isinstance(power_on, bool) and
                    isinstance(add_to_failover, bool)):
                raise SDKException('Subclient', '101')

        # set attr for all the option in restore xml from user inputs
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
            in_place=False
        )

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

        restore_option = {}
        # check mandatory input parameters are correct
        if not (isinstance(overwrite, bool) and
                isinstance(power_on, bool) and
                isinstance(add_to_failover, bool)):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True


        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            add_to_failover=add_to_failover,
            in_place=True
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_conversion_vmware(
            self,
            vcenter_client,
            destination_os_name,
            vm_to_restore=None,
            esx_host=None,
            datastore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            transport_mode='Auto',
            proxy_client=None,
            destination_network = None
            ):
        """
        This converts the Hyperv VM to VMware
        Args:
                vm_to_restore          (dict)  --  dict containing the VM name(s) to restore as
                                                   keys and the new VM name(s) as their values.
                                                   Input empty string for default VM name for
                                                   restored VM.
                                                    default: {}

                vcenter_client    (basestring) -- name of the vcenter client
                                                  where the VM should be
                                                    restored.

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
                                                  Options for input are: 'Original',
                                                  'Thick Lazy Zero', 'Thin', 'Thick Eager Zero'
                                                  default: Original

                transport_mode    (basestring) -- transport mode to be used for
                                                  the restore.
                                                  Options for input are: 'Auto', 'SAN', 'Hot Add',
                                                  'NBD', 'NBD SSL'
                                                  default: Auto

                proxy_client      (basestring) -- destination proxy client

                destination_network (basestring)-- destiantion network to which VM has to be connected

                destiantion_os      (base string)- os of source VM




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
        if not (isinstance(vcenter_client, basestring) and
                isinstance(destination_network, basestring)):
            raise SDKException('Subclient', '101')

        #getting all dummy objects for new client

        subclient = self._set_vm_conversion_defaults(vcenter_client, restore_option)
        instance = subclient._backupset_object._instance_object
        disk_option_value = subclient._disk_option[disk_option]
        transport_mode_value = subclient._transport_mode[transport_mode]
        esx_server = instance.server_host_name[0]

        #setting restore vms
        vm_list = None
        if vm_to_restore:
            vm_list = list(vm_to_restore.keys())


        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=vcenter_client,
            datastore=datastore,
            esx_host=esx_host,
            esx_server=esx_server,
            unconditional_overwrite=overwrite,
            client_name=proxy_client,
            power_on=power_on,
            vm_to_restore=self._set_vm_to_restore(vm_list),
            disk_option=disk_option_value,
            transport_mode=transport_mode_value,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            destination_instance=instance.instance_name,
            backupset_client_name=instance._agent_object._client_object.client_name,
            destination_network=destination_network,
            destination_os_name=self._get_guest_os(destination_os_name)
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_conversion_azurerm(
            self,
            azure_client,
            vm_to_restore=None,
            resource_group=None,
            storage_account=True,
            proxy_client=None,
            overwrite=True,
            power_on=True,
            instance_size=None,
            public_ip=False,
            restore_as_managed=False,
            copy_precedence=0,
            restore_option=None):
        """
                This converts the Hyperv VM to AzureRM
                Args:
                        vm_to_restore          (dict):     dict containing the VM name(s) to restore as
                                                           keys and the new VM name(s) as their values.
                                                           Input empty string for default VM name for
                                                           restored VM.
                                                           default: {}

                        azure_client    (basestring):      name of the AzureRM client
                                                           where the VM should be
                                                           restored.

                        resource_group   (basestring):      destination Resource group
                                                            in the AzureRM

                        storage_account  (basestring):    storage account where the
                                                          restored VM should be located
                                                          in AzureRM

                        overwrite              (bool):    overwrite the existing VM
                                                          default: True

                        power_on               (bool):    power on the  restored VM
                                                          default: True

                        instance_size    (basestring):    Instance Size of restored VM

                        public_ip              (bool):    If True, creates the Public IP of
                                                          restored VM

                        restore_as_managed     (bool):    If True, restore as Managed VM in Azure

                        copy_precedence         (int):    copy precedence value
                                                          default: 0

                        proxy_client      (basestring):   destination proxy client

                    Returns:
                        object - instance of the Job class for this restore job

                    Raises:
                        SDKException:
                            if inputs are not of correct type as per definition

                            if failed to initialize job

                            if response is empty

                            if response is not success

        """
        if restore_option is None:
            restore_option = {}

        # check mandatory input parameters are correct
        if not (isinstance(azure_client, basestring)):
            raise SDKException('Subclient', '101')

        subclient = self._set_vm_conversion_defaults(azure_client, restore_option)
        instance = subclient._backupset_object._instance_object
        if proxy_client is None:
            proxy_client = instance.server_host_name[0]

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=azure_client,
            datastore=storage_account,
            esx_host=resource_group,
            unconditional_overwrite=overwrite,
            client_name=proxy_client,
            power_on=power_on,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            copy_precedence=copy_precedence,
            createPublicIP=public_ip,
            restoreAsManagedVM=restore_as_managed,
            instanceSize=instance_size,
            volume_level_restore=1,
            destination_instance=instance.instance_name,
            backupset_client_name=instance._agent_object._client_object.client_name
        )


        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
