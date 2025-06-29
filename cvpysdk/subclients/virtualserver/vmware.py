﻿# -*- coding: utf-8 -*-

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

from cvpysdk.storage import RPStore
from cvpysdk.subclients.vssubclient import VirtualServerSubclient
from cvpysdk.virtualmachinepolicies import VirtualMachinePolicy
from ...exception import SDKException


class VMWareVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a VMWare virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """

        super(VMWareVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = [".vmdk"]

        self._disk_option = {
            'Original': 0,
            'Thick Lazy Zero': 1,
            'Thin': 2,
            'Thick Eager Zero': 3
        }

        self._transport_mode = {
            'Auto': 0,
            'SAN': 1,
            'Hot Add': 2,
            'NBD': 5,
            'NBD SSL': 4
        }

    def add_revert_option(self, request_json, revert):
        """
        Add revert in restore json

        Args:

            request_json            (dict)  :       restore dict

            revert                  (bool)  :       revert option

        Returns:
            request_json            (dict)  :       restore dict

        """
        if revert:
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['revert'] = True
        return request_json

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            transport_mode='Auto',
            proxy_client=None,
            to_time=0,
            **kwargs):
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

                disk_option           (str)  --  disk provisioning for the restored vm
                                                        Options for input are: 'Original',
                                                        'Thick Lazy Zero', 'Thin',
                                                        'Thick Eager Zero'
                                                        default: Original

                transport_mode        (str)  --  transport mode to be used for
                                                        the restore.
                                                        Options for input are: 'Auto', 'SAN',
                                                        ''Hot Add', NBD', 'NBD SSL'
                                                        default: Auto

                proxy_client          (str)  --  proxy client to be used for restore
                                                        default: proxy added in subclient

                to_time                 (int)       -- End time to select the job for restore
                                                        default: None

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_in_place
                    eg:
                    media_agent         (str)   -- media agent

                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

                    revert              (bool)      --  Revert option


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        restore_option = {"media_agent": kwargs.get("media_agent", None), "v2_details": kwargs.get("v2_details", None),
                          "revert": kwargs.get("revert", False)}

        # check input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        disk_option_value = self._disk_option[disk_option]
        transport_mode_value = self._transport_mode[transport_mode]

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        if proxy_client is not None:
            restore_option['client_name'] = proxy_client

        if vm_to_restore and not isinstance(vm_to_restore, list):
            vm_to_restore = [vm_to_restore]
        restore_option_copy = restore_option.copy()

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            in_place=True,
            esx_server_name="",
            volume_level_restore=1,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            disk_option=disk_option_value,
            transport_mode=transport_mode_value,
            copy_precedence=copy_precedence,
            to_time=to_time
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        request_json = self.add_revert_option(request_json, restore_option.get('revert', False))
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            restored_vm_name=None,
            vcenter_client=None,
            esx_host=None,
            datastore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            transport_mode='Auto',
            proxy_client=None,
            to_time=0,
            run_security_scan=False,
            **kwargs
    ):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore            (str)    --  VM that is to be restored

                restored_vm_name         (str)    --  new name of vm. If nothing is passed,
                                                      'del' is appended to the original vm name

                vcenter_client    (str)    --  name of the vcenter client where the VM
                                                      should be restored.

                esx_host          (str)    --  destination esx host. Restores to the source
                                                      VM esx if this value is not specified

                datastore         (str)    --  datastore where the restored VM should be
                                                      located. Restores to the source VM datastore
                                                      if this value is not specified

                overwrite               (bool)    --  overwrite the existing VM
                                                      default: True

                power_on                (bool)    --  power on the  restored VM
                                                      default: True

                copy_precedence          (int)    --  copy precedence value
                                                      default: 0

                disk_option       (str)    --  disk provisioning for the  restored vm
                                                      Options for input are: 'Original',
                                                      'Thick Lazy Zero', 'Thin', 'Thick Eager Zero'
                                                      default: 'Original'

                transport_mode    (str)    --  transport mode to be used for the restore.
                                                      Options for input are: 'Auto', 'SAN',
                                                      'Hot Add', 'NBD', 'NBD SSL'
                                                      default: Auto

                proxy_client      (str)    --  destination proxy client

                to_time             (Int)         --  End time to select the job for restore
                                                    default: None

                run_security_scan   (bool)  --  run security scan or not                                  

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_out_of_place
                    eg:
                    source_ip           (str)    --  IP of the source VM

                    destination_ip      (str)    --  IP of the destination VM

                    destComputerName  (str)    --  Hostname of the restored vm

                    source_subnet  (str)    --  subnet of the source vm

                    source_gateway  (str)    --  gateway of the source vm

                    destination_subnet  (str)    --  subnet of the restored vm

                    destination_gateway  (str)    --  gateway of the restored vm

                    media_agent         (str)   --  media agent for restore

                    restore_option      (dict)     --  complete dictionary with all advanced options
                        default: {}

                    v2_details          (dict)       -- details for v2 jobs
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

                    revert              (bool)      --  Revert option

                    volume_level_restore (bool)     -- Restore option type for LR: Default is None

                    redirectWritesToDatastore (str) -- Datastore name to redirect writes for LR restore: Default " "

                    delayMigrationMinutes   (Int)  -- Migrations delay in minutes: Default '0'

                    vmTags              (list)  --  List of tags to be added to the restored VM

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
        extra_options = ['source_ip', 'destination_ip', 'network', 'destComputerName',
                         'source_subnet', 'source_gateway', 'destination_subnet',
                         'destination_gateway', 'folder_path', 'media_agent', 'v2_details', 'revert',
                         'volume_level_restore', 'redirectWritesToDatastore', 'delayMigrationMinutes', 'vmTags']

        for key in extra_options:
            if key in kwargs:
                restore_option[key] = kwargs[key]
            else:
                restore_option[key] = None
        # check mandatory input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client_name'] = proxy_client

        if restored_vm_name:
            if not (isinstance(vm_to_restore, str) or
                    isinstance(restored_vm_name, str)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_vm_name

        if vm_to_restore and not isinstance(vm_to_restore, list):
            vm_to_restore = [vm_to_restore]

        restore_option_copy = restore_option.copy()

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=vcenter_client,
            datastore=datastore,
            esx_host=esx_host,
            esx_server=None,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            run_security_scan=run_security_scan,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            disk_option=self._disk_option[disk_option],
            transport_mode=self._transport_mode[transport_mode],
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            source_item=[],
            to_time=to_time
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        request_json = self.add_revert_option(request_json, restore_option.get('revert', False))
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
                vm_name             (str)    --  Name of the VM added in subclient content
                                                        whose  disk is selected for restore

                destination_path        (str)    --  Staging (destination) path to restore the
                                                        disk.

                disk_name                 (list)    --  name of the disk which has to be restored
                                                        (only vmdk files permitted - enter full
                                                        name of the disk)
                                                        default: None

                proxy_client        (str)    --  Destination proxy client to be used
                                                        default: None

                copy_precedence            (int)    --  SP copy precedence from which browse has to
                                                         be performed

                convert_to          (str)    --  disk format for the restored disk
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
        if not (isinstance(vm_name, str) and
                isinstance(destination_path, str) and
                isinstance(disk_name, list) and
                disk_extn == '.vmdk'):
            raise SDKException('Subclient', '101')

        if convert_to is not None:
            convert_to = convert_to.lower()
            if convert_to not in ['vhdx', 'vhd']:
                raise SDKException('Subclient', '101')

        if copy_precedence:
            _disk_restore_option['copy_precedence_applicable'] = True

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
                            disk_name=None):

        """Attaches the Disks to the provided vm

            Args:
                vm_name             (str)    --  Name of the VM added in subclient content
                                                        whose  disk is selected for restore

                vcenter             (dict)          --  Dictinoary of vcenter, username and creds

                esx                 (str)    --  Esx host where the vm resides

                datastore               (string)    --  Datastore where disks will be restoed to
                                                        default: None

                proxy_client        (str)    --  Destination proxy client to be used
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

        disk_extn = '.vmdk'
        if not disk_name:
            disk_name = []
        else:
            disk_extn = self._get_disk_extension(disk_name)

        # check if inputs are correct
        if not (isinstance(vm_name, str) and
                isinstance(disk_name, list) and
                disk_extn == '.vmdk'):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            _attach_disk_restore_option['copy_precedence_applicable'] = True

        # fetching all disks from the vm
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + vm_ids[vm_name])

        if not disk_name:  # if disk names are not provided, restore all vmdk disks
            for each_disk_path in disk_list:
                disk_name.append(disk_info_dict[each_disk_path]['snap_display_name'])

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

        self._set_restore_inputs(
            _attach_disk_restore_option,
            in_place=True,
            copy_precedence=copy_precedence,
            vm_to_restore=vm_name,
            esxHost=vcenter['vcenter'],
            userName=vcenter['user'],
            password=vcenter['password'],
            esx=esx,
            paths=src_item_list,
            datastore=datastore,
            volume_level_restore=6
        )

        request_json = self._prepare_attach_disk_restore_json(_attach_disk_restore_option)
        return self._process_restore_response(request_json)

    def full_vm_conversion_azurerm(
            self,
            azure_client,
            vm_to_restore=None,
            resource_group=None,
            storage_account=None,
            datacenter=None,
            proxy_client=None,
            overwrite=True,
            power_on=True,
            instance_size=None,
            public_ip=False,
            restore_as_managed=False,
            copy_precedence=0,
            disk_type=None,
            restore_option=None,
            networkDisplayName=None,
            networkrsg=None,
            destsubid=None,
            subnetId=None):
        """
                This converts the Hyperv VM to AzureRM
                Args:
                        vm_to_restore          (dict):     dict containing the VM name(s) to restore as
                                                           keys and the new VM name(s) as their values.
                                                           Input empty string for default VM name for
                                                           restored VM.
                                                           default: {}

                        azure_client    (str):      name of the AzureRM client
                                                           where the VM should be
                                                           restored.

                        resource_group   (str):      destination Resource group
                                                            in the AzureRM

                        storage_account  (str):    storage account where the
                                                          restored VM should be located
                                                          in AzureRM

                        overwrite              (bool):    overwrite the existing VM
                                                          default: True

                        power_on               (bool):    power on the  restored VM
                                                          default: True

                        instance_size    (str):    Instance Size of restored VM

                        public_ip              (bool):    If True, creates the Public IP of
                                                          restored VM

                        restore_as_managed     (bool):    If True, restore as Managed VM in Azure

                        copy_precedence         (int):    copy precedence value
                                                          default: 0

                        proxy_client      (str):   destination proxy client

                        networkDisplayName(str):   destination network display name

                        networkrsg        (str):   destination network display name's security group

                        destsubid         (str):   destination subscription id

                        subnetId          (str):   destination subet id



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

        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if not isinstance(vm_to_restore, list):
            vm_to_restore = [vm_to_restore]
        # check mandatory input parameters are correct
        if not isinstance(azure_client, str):
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
            datacenter=datacenter,
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
            backupset_client_name=instance._agent_object._client_object.client_name,
            networkDisplayName=networkDisplayName,
            networkrsg=networkrsg,
            destsubid=destsubid,
            subnetId=subnetId
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)


    def full_vm_conversion_hyperv(
            self,
            hyperv_client,
            vm_to_restore=None,
            DestinationPath=None,
            proxy_client=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            destination_network=None):
        """
                This converts the AzureRM to Hyper-v VM
                Args:

                    hyperv_client(str):  name of the hyper-V client
                                                    where the VM should restored.

                    vm_to_restore(dict):    dict containing the VM name(s) to restore as
                                                keys and the new VM name(s) as their values.
                                                Input empty string for default VM name for
                                                restored VM.
                                                default: {}

                    DestinationPath   (str): DestinationPath
                                                        in the Hyper-V client

                    proxy_client(str):   destination proxy client

                    overwrite   (bool):    overwrite the existing VM
                                                default: True

                    power_on  (bool):    power on the  restored VM
                                            default: True

                    copy_precedence   (int):    copy precedence value
                                                    default: 0

                    Destination_network   (str):      Destination network
                                                            in the Hyper-V client

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
        if not isinstance(hyperv_client, str):
            raise SDKException('Subclient', '101')

        if not isinstance(vm_to_restore, list):
            vm_to_restore = [vm_to_restore]

        subclient = self._set_vm_conversion_defaults(hyperv_client, restore_option)
        instance = subclient._backupset_object._instance_object
        if proxy_client is None:
            proxy_client = instance.server_host_name[0]

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=hyperv_client,
            unconditional_overwrite=overwrite,
            client_name=proxy_client,
            DestinationPath=DestinationPath,
            power_on=power_on,
            vm_to_restore=vm_to_restore,
            copy_precedence=copy_precedence,
            datastore=DestinationPath,
            name=vm_to_restore,
            destination_network=destination_network,
            volume_level_restore=1,
            destination_instance=instance.instance_name,
            backupset_client_name=instance._agent_object._client_object.client_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        disk_options = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption']
        for disk_info in disk_options['advancedRestoreOptions'][0]['disks']:
            disk_info['newName'] = ''
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['volumeRstOption']['volumeLevelRestoreType'] = 1

        return self._process_restore_response(request_json)

    def create_blr_replication_pair(self, *, target, vms, plan_name, rpstore=None, granular_options=None):
        """

        Args:
            target  (VirtualMachinePolicy): an instance of  VirtualMachinePolicy which is the target

            vms     (List)                : List of VMs to be replicated

            plan_name (str)               : Name of the plan

            rpstore (str)                 : Name of the RPStore.
                default : None. If name of the RPStore is given, granular mode is chosen else Live mode

            granular_options(dict)        : Dict which contains granular recovery options

                Example:
                    {
                        "ccrpInterval": 300,
                        "acrpInterval": 0,
                        "maxRpInterval": 21600,
                        "rpMergeDelay": 172800,
                        "rpRetention": 604800,
                        "maxRpStoreOfflineTime": 0,
                        "useOffPeakSchedule": 0,
                    }
        """

        try:
            assert isinstance(target, VirtualMachinePolicy) is True
        except AssertionError:
            raise TypeError("Expected an instance of VirtualMachinePolicy")
        if rpstore and granular_options:
            try:
                assert granular_options["rpRetention"] > granular_options["rpMergeDelay"]
                assert granular_options["rpRetention"] > granular_options["maxRpInterval"]
            except AssertionError:
                ValueError("rpRetention value must be greater than rpMergeDelay and maxRpInterval")

        restore_option = dict()
        restore_option.update(granular_options)
        for vm in vms:
            self._set_restore_inputs(
                restore_option,
                paths=[],
                in_place=False,
                target_id=target.vm_policy_id,
                target_name=target.vm_policy_name,
                vcenter_client=target.properties()["destinationHyperV"]["clientName"],
                datastore=target.properties()["dataStores"][0]["dataStoreName"],
                esx_host=target.properties()["esxServers"][0]["esxServerName"],
                vm_to_restore=[vm],
                volume_level_restore=1,
                block_level=True,
                new_name=target.properties()["vmNameEditString"],
                prefix=bool(target.properties()["vmNameEditType"] == 1),
                plan_name=plan_name,
                source_network=target.properties()["networkList"][0]["sourceNetwork"],
                destination_network=target.properties()["networkList"][0]["destinationNetwork"]

            )
            if isinstance(rpstore, RPStore):
                restore_option["recovery_type"] = 4
                restore_option["rpstore_name"] = rpstore.rpstore_name
                restore_option["rpstore_id"] = rpstore.rpstore_id

            response = self._commcell_object.execute_qcommand("qoperation execute",
                                                              self._prepare_blr_xml(restore_option))
            if response.json() != {'errorMessage': '', 'errorCode': 0}:
                raise SDKException("Subclient", 102, response.json()["errorMessage"])

    def full_vm_conversion_googlecloud(
            self,
            google_cloud_client,
            vm_to_restore=None,
            esx_host=None,
            vmSize=None,
            nics=None,
            datacenter=None,
            projectId=None,
            overwrite=True,
            power_on=True,
            proxy_client=None,
            vcenter_client=None,
            esx_server=None,
            copy_precedence=0,
            restore_option=None):

        """
                        This converts the VMware to Google Cloud
                        Args:
                                vm_to_restore          (list):     provide the VM names to restore

                                google_cloud_client    (str):      name of the Google Cloud client
                                                                   where the VM should be
                                                                   restored.

                                esx_host               (str): Zone of the restored VM in Google Cloud

                                vmSize                 (str): vmSize of the restoed VM

                                overwrite              (bool):    overwrite the existing VM
                                                                  default: True

                                power_on               (bool):    power on the  restored VM
                                                                  default: True

                                vcenter_client    (str)    --  name of the vcenter client where the VM
                                                      should be restored.

                                copy_precedence         (int):    copy precedence value
                                                                  default: 0

                                proxy_client      (str):   destination proxy client

                                esx_server        (str):    Name of the destination virtualization Client

                                nics              (str):   Network Configurations of the VM

                                datacenter        (str):   Project ID of the restored VM

                                projectId         (str):   project ID where the new VM has to be created

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
        if not isinstance(google_cloud_client, str):
            raise SDKException('Subclient', '101')

        subclient = self._set_vm_conversion_defaults(google_cloud_client, restore_option)
        instance = subclient._backupset_object._instance_object
        if proxy_client is None:
            proxy_client = instance.server_host_name[0]

        if vm_to_restore is None:
            vm_to_restore = self._set_vm_to_restore(vm_to_restore)

        self._set_restore_inputs(
            restore_option,
            vm_to_restore=vm_to_restore,
            esx_host=esx_host,
            esx_server=esx_server,
            vcenter_client=vcenter_client,
            vmSize=vmSize,
            nics=nics,
            datacenter=datacenter,
            createPublicIP=False,
            projectId=projectId,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            volume_level_restore=1,
            client_name=proxy_client,
            in_place=False,
            copy_precedence=copy_precedence
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
            'diskLevelVMRestoreOption']['advancedRestoreOptions'][0]['projectId'] = projectId
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
            'diskLevelVMRestoreOption']['advancedRestoreOptions'][0]['newName'] = vm_to_restore[0].lower().replace("_",
                                                                                                                   "")
        disk_new_names = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
            'diskLevelVMRestoreOption']['advancedRestoreOptions'][0]['disks']
        for each in range(0, len(disk_new_names)):
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
                'diskLevelVMRestoreOption']['advancedRestoreOptions'][0]['disks'][each]['newName'] = ""
        return self._process_restore_response(request_json)
