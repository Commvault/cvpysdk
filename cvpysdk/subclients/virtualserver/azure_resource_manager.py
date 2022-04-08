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

"""File for operating on a Virtual Server AzureRM Subclient.

AzureRMSubclient is the only class defined in this file.

AzureRMSubclient: Derived class from VirtualServerSubClient  Base class, representing a
                           AzureRM Subclient, and to perform operations on that Subclient

AzureRMSubclient:

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                     to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()              --  restores the VM specified by the
                                                    user to the same location
    
    full_vm_conversion_azurestack()         -- converts azure vm to azurestack
    
    full_vm_conversion_amazon()             -- converts azure vm to amazon
     
    full_vm_conversion_hyperv()             -- converts azure vm to hyperv
    
    full_vm_conversion_vmware()             -- converts azure vm to vmware
"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException
from past.builtins import basestring


class AzureRMSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    AzureRM  virtual server subclient,and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        self.diskExtension = [".vhd", "none"]
        super(AzureRMSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def full_vm_restore_out_of_place(self,
                                     vm_to_restore=None,
                                     resource_group=None,
                                     storage_account=None,
                                     datacenter=None,
                                     proxy_client=None,
                                     restore_new_name=None,
                                     overwrite=True,
                                     power_on=True,
                                     instance_size=None,
                                     public_ip=False,
                                     restore_as_managed=False,
                                     copy_precedence=0,
                                     disk_type=None,
                                     restore_option=None,
                                     **kwargs):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            at the specified destination location.

            Args:

                vm_to_restore         (list)       --  provide the VM name to restore

                resource_group        (str)        -- provide the resource group to restore

                storage_account       (str)        -- provide the storage account to restore

                proxy_client          (str)        -- provide the proxy client to restore

                restore_new_name      (str)        -- provide the new restore name

                instance_size         (str)        -- provide the instance size of the restore VM

                createPublicIP
                        default:True   (bool)      --  creates the Public IP of the new VM

                restoreAsManagedVM
                        default:False   (bool)      --  new VM will be restored as unmanaged VM


                overwrite
                        default:False   (bool)      --  overwrite the existing VM

                poweron
                        default:False   (bool)      --  power on the  restored VM


                restore_option      (dict)     --  complete dictionary with all advanced optio
                    default: {}

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_out_of_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

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
        restore_option["v2_details"] = kwargs.get("v2_details", None)

        # check input parameters are correct
        if bool(restore_option):
            if not (isinstance(overwrite, bool) and
                    isinstance(power_on, bool)):
                raise SDKException('Subclient', '101')

        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            esx_host=resource_group,
            datastore=storage_account,
            datacenter=datacenter,
            client_name=proxy_client,
            in_place=False,
            createPublicIP=public_ip,
            restoreAsManagedVM=restore_as_managed,
            disk_type=disk_type,
            instanceSize=instance_size,
            restore_new_name=restore_new_name
        )

        # set attr for all the option in restore xml from user inputs

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 public_ip=False,
                                 restore_as_managed=False,
                                 copy_precedence=0,
                                 **kwargs):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore         (list)       --  provide the VM name to restore

                createPublicIP
                        default:True   (bool)      --  creates the Public IP of the new VM

                restoreAsManagedVM
                        default:False   (bool)      --  new VM will be restored as unmanaged VM

                overwrite
                        default:true   (bool)      --  overwrite the existing VM

                poweron
                        default:true   (bool)      --  power on the  restored VM

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_in_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        restore_option = {"v2_details": kwargs.get("v2_details", None)}
        # check mandatory input parameters are correct
        if not (isinstance(overwrite, bool) and
                isinstance(power_on, bool)):
            raise SDKException('Subclient', '101')
        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            createPublicIP=public_ip,
            restoreAsManagedVM=restore_as_managed,
            in_place=True
        )
        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_conversion_azurestack(
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
                This converts the AzureRM to Azurestack
                Args:
                        vm_to_restore          (list):     provide the VM names to restore

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
        if not isinstance(azure_client, basestring):
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

    def full_vm_conversion_amazon(
            self,
            amazon_client,
            guest_options=None,
            vm_to_restore=None,
            proxy_client=None,
            is_aws_proxy=True,
            amazon_bucket=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0):
        """
                This converts the AzureRM to Amazon
                Args:
                        vm_to_restore          (list):     provide the VM names to restore

                        amazon_client    (basestring):     name of the Amazon client
                                                           where the VM should be
                                                           restored.

                        overwrite              (bool):     overwrite the existing VM
                                                           default: True

                        power_on               (bool):     power on the  restored VM
                                                           default: True

                        copy_precedence         (int):     copy precedence value
                                                           default: 0

                        proxy_client      (basestring):    destination proxy client

                        is_aws_proxy      (basestring):     boolean value whether
                                                            proxy resides in AWS
                                                            or not
                                                            default: True

                        amazon_bucket    (basestring) :     Amazon bucket (required
                                                            when non-AWS proxy
                                                            is used)

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
        if not isinstance(amazon_client, basestring):
            raise SDKException('Subclient', '101')

        subclient = self._set_vm_conversion_defaults(amazon_client, restore_option)
        dest_vm = subclient.content[0]["display_name"]
        amazon_options = subclient.amazon_defaults(dest_vm, restore_option)

        instance = subclient._backupset_object._instance_object
        instance_dict = instance._properties['instance']
        if proxy_client is None:
            proxy_client = instance.server_host_name[0]

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        if not is_aws_proxy:
            if not amazon_bucket:
                raise SDKException('Subclient', 104)
            restore_option['datastore'] = amazon_bucket
        if guest_options is None:
            guest_options = {}


        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            in_place=False,
            esx_server_name=instance_dict["clientName"],
            esx_server=proxy_client,
            volume_level_restore=1,
            client_name=proxy_client,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            is_aws_proxy=is_aws_proxy,
            destComputerName=guest_options.get('name', None),
            destComputerUserName=guest_options.get('user_name', None),
            instanceAdminPassword=guest_options.get('password', None),
            datacenter=amazon_options.get('datacenter', None),
            resourcePoolPath=amazon_options.get('resourcePoolPath', None),
            optimizationEnabled=False,
            datastore=restore_option.get('datastore', None),
            availability_zone=amazon_options.get('esx_host', None),
            esx_host=amazon_options.get('esx_host', None),
            ami=amazon_options.get('ami', None),
            vmSize=amazon_options.get('instance_type', None),
            iamRole=amazon_options.get('iam_role', None),
            securityGroups=amazon_options.get('security_groups', None),
            keyPairList=amazon_options.get('keypair_list', None),
            terminationProtected=amazon_options.get('termination_protected', False)
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

                    hyperv_client(basestring):  name of the hyper-V client
                                                    where the VM should restored.

                    vm_to_restore(dict):    dict containing the VM name(s) to restore as
                                                keys and the new VM name(s) as their values.
                                                Input empty string for default VM name for
                                                restored VM.
                                                default: {}

                    DestinationPath   (basestring): DestinationPath
                                                        in the Hyper-V client

                    proxy_client(basestring):   destination proxy client

                    overwrite   (bool):    overwrite the existing VM
                                                default: True

                    power_on  (bool):    power on the  restored VM
                                            default: True

                    copy_precedence   (int):    copy precedence value
                                                    default: 0

                    Destination_network   (basestring):      Destination network
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
        if not isinstance(hyperv_client, basestring):
            raise SDKException('Subclient', '101')

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
            volume_level_restore=0,
            destination_instance=instance.instance_name,
            backupset_client_name=instance._agent_object._client_object.client_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        disk_options = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption']
        for disk_info in disk_options['advancedRestoreOptions'][0]['disks']:
            disk_info['newName'] = ''
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['volumeRstOption']['volumeLevelRestoreType'] = 1

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
            destination_network=None
    ):
        """
        This converts the azure VM to VMware
        Args:
                vcenter_client    (basestring) -- name of the vcenter client
                                                  where the VM should be
                                                    restored.

                destination_os_name      (base string)- os of source VM

                vm_to_restore          (dict)  --  dict containing the VM name(s) to restore as
                                                   keys and the new VM name(s) as their values.
                                                   Input empty string for default VM name for
                                                   restored VM.
                                                    default: {}

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

                destination_network (basestring)-- destiantion network
                                                    to which VM has to be connected

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
            destination_os_name=destination_os_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        disk_options = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption']['diskLevelVMRestoreOption']
        for disk_info in disk_options['advancedRestoreOptions'][0]['disks']:
            disk_info['newName'] = ''

        return self._process_restore_response(request_json)