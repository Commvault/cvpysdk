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

"""File for operating on a Virtual Server Amazon AWS Subclient.

AmazonVirtualServerSubclient is the only class defined in this file.

AmazonVirtualServerSubclient:   Derived class from VirtualServerSubClient Base
                                class,representing a AWS Subclient,
                                and to perform operations on that Subclient

AmazonVirtualServerSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of vmware subclient class,
                                    associated with the VirtualServer subclient

    full_vm_restore_in_place()  --  restores the VM specified by the user to
                                    the same location

    full_vm_restore_out_of_place() -- restores the VM specified to the provided
                                      Amazon AWS psuedoclient vcenter via
                                      vcenter_client

"""

from enum import Enum
from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class AmazonVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents an Amazon AWS virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        super(AmazonVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = ["none"]

    class disk_pattern(Enum):
        """
        stores the disk pattern of all hypervisors
        """
        name = "name"
        datastore = "availabilityZone"
        new_name = 'newName'
        aws_bucket = 'Datastore'

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            proxy_client=None,
            is_aws_proxy=True,
            amazon_bucket=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            **kwargs
    ):
        """Restores the FULL Virtual machine specified in the input list
            to the location same as the actual location of the VM in VCenter.

            Args:
                vm_to_restore         (list)        --  provide the VM name to restore
                                                        default: None

                proxy_client          (str)  --  proxy client to be used for restore
                                                        default: proxy added in subclient

                is_aws_proxy          (str)  --  boolean value whether proxy resides in AWS
                                                        or not
                                                        default: True

                amazon_bucket         (str)  --  Amazon bucket (required when non-AWS proxy
                                                        is used)

                overwrite             (bool)        --  overwrite the existing VM
                                                        default: True

                power_on              (bool)        --  power on the  restored VM
                                                        default: True

                copy_precedence       (int)         --  copy precedence value
                                                        default: 0

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_in_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        restore_option = {"v2_details": kwargs.get("v2_details", None)}

        # check input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        if proxy_client is not None:
            restore_option['client'] = proxy_client

        if not is_aws_proxy:
            if not amazon_bucket:
                raise SDKException('Subclient', 104)
            restore_option['datastore'] = amazon_bucket

        instance_dict = self._backupset_object._instance_object._properties['instance']

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            in_place=True,
            esx_server_name=instance_dict["clientName"],
            volume_level_restore=1,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            is_aws_proxy=is_aws_proxy,
            datacenter=None,
            securityGroups=None,
            keyPairList=None,
            resourcePoolPath=None,
            terminationProtected=None,
            optimizationEnabled=False,
            vmSize=None
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            vm_display_name=None,
            proxy_client=None,
            is_aws_proxy=True,
            amazon_bucket=None,
            availability_zone=None,
            amazon_options=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            **kwargs
    ):
        """Restores the FULL Virtual machine specified in the input list
            to the provided virtualization client along with the zone and instance type.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding zone and instance type.

            Args:
                vm_to_restore         (str)  --  provide the VM name to restore
                                                        default: None

                vm_display_name       (str)        --  provide the new display name for the
                                                        restored VM
                                                        default: None

                proxy_client          (str)  --  proxy client to be used for restore
                                                        default: proxy added in subclient

                is_aws_proxy          (str)  --  boolean value whether proxy resides in AWS
                                                        or not
                                                        default: True

                amazon_bucket         (str)  --  Amazon bucket (required when non-AWS proxy
                                                        is used)

                amazon_options        (dict)        --  dict containing configuration options for
                                                        restored VM. Permissible keys are below
                    availability_zone

                    ami

                    instance_type

                    iam_role

                    termination_protection

                overwrite             (bool)        --  overwrite the existing VM
                                                        default: True

                power_on              (bool)        --  power on the  restored VM
                                                        default: True

                copy_precedence       (int)         --  copy precedence value
                                                        default: 0
                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_out_of_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        restore_option = {"v2_details": kwargs.get("v2_details", None)}
        if not amazon_options:
            amazon_options = {}

        # check input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client_name'] = proxy_client

        if vm_display_name:
            if not (isinstance(vm_to_restore, str) or
                    isinstance(vm_display_name, str)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = vm_display_name

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        if not is_aws_proxy:
            if not amazon_bucket:
                raise SDKException('Subclient', 104)
            restore_option['datastore'] = amazon_bucket

        instance_dict = self._backupset_object._instance_object._properties['instance']

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            in_place=False,
            esx_server_name=instance_dict["clientName"],
            volume_level_restore=1,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            is_aws_proxy=is_aws_proxy,
            datacenter=None,
            resourcePoolPath=None,
            optimizationEnabled=False,
            availability_zone=availability_zone,
            esx_host=availability_zone,
            ami=amazon_options.get('ami', None),
            vmSize=amazon_options.get('instance_type', None),
            iamRole=amazon_options.get('iam_role', None),
            securityGroups=amazon_options.get('security_groups', None),
            keyPairList=amazon_options.get('keypair_list', None),
            terminationProtected=amazon_options.get('termination_protected', False),
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def attach_disk_restore(
            self,
            vm_to_restore,
            destination_vm,
            proxy_client=None,
            amazon_options=None,
            overwrite=True,
            copy_precedence=0,
            destination_vm_guid=None,
            disk_prefix=None,
            availability_zone=None,
            media_agent=None,
            disk_name=None
    ):
        """Restores the Attach Disk restore with  specified in the input list
            to the provided instance.

            Args:
                vm_to_restore         (str)  --  provide the source vm name

                destination_vm        (str)  --  provide the destination VM name to restore

                disk_prefix       (str)        --  provide the new display name for the
                                                    restored disk
                                                    default: None

                disk_name       (str)        --  provide the new display name for the source disk
                                                    default: None

                proxy_client          (str)  --  proxy client to be used for restore
                                                    default: proxy added in subclient

                destination_vm_guid     (str)  --  instance id of the vm
                                                            default:None

                media_agent             (str)  --  media agent to be used browse and restore

                amazon_options        (dict)        --  dict containing configuration options for
                                                        restored VM. Permissible keys are below
                    availability_zone

                    ami

                    instance_type

                overwrite             (bool)        --  overwrite the existing VM
                                                        default: True

                copy_precedence       (int)         --  copy precedence value
                                                        default: 0

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
        _attach_disk_restore_option = {}
        if not amazon_options:
            amazon_options = {}

        # check input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            _attach_disk_restore_option['copy_precedence_applicable'] = True

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            _attach_disk_restore_option['client'] = proxy_client

        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + vm_ids[vm_to_restore])
        if not disk_name:
            disk_name = []
            for each_disk_path in disk_list:
                disk_name.append(each_disk_path.split('\\')[-1])

        else:
            for each_disk in disk_name:
                each_disk_path = "\\" + str(vm_to_restore) + "\\" + each_disk
                if each_disk_path not in disk_list:
                    raise SDKException('Subclient', '111')

        src_item_list = []
        for each_disk in disk_name:
            src_item_list.append("\\" + vm_ids[vm_to_restore] + "\\" + each_disk.split("\\")[-1])
        _attach_disk_restore_option['paths'] = src_item_list
        if proxy_client is not None:
            _attach_disk_restore_option['client'] = proxy_client
        if not destination_vm:
            destination_vm = vm_to_restore
        instance_dict = self._backupset_object._instance_object._properties['instance']
        _attach_disk_restore_option = self.amazon_defaults(vm_to_restore, _attach_disk_restore_option)

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            _attach_disk_restore_option,
            vm_to_restore=vm_to_restore,
            esx_server_name=instance_dict["clientName"],
            volume_level_restore=6,
            unconditional_overwrite=overwrite,
            copy_precedence=copy_precedence,
            paths=src_item_list,
            datacenter=None,
            resourcePoolPath=None,
            availability_zone=availability_zone,
            esx_host=availability_zone,
            newName=destination_vm,
            newGUID=destination_vm_guid,
            disk_name_prefix=disk_prefix,
            ami=_attach_disk_restore_option.get('ami', None),
            vmSize=_attach_disk_restore_option.get('instance_type', None)
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
