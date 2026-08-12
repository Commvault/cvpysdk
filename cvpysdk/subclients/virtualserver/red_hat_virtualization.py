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

"""File for operating on a Virtual Server VMWare Subclient.

VMWareVirtualServerSubclient is the only  class defined in this file.

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


class RhevVirtualServerSubclient(VirtualServerSubclient):
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

        super(RhevVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = ["none"]

        self._disk_option = {
            'Original': 0,
            'Thick Lazy Zero': 1,
            'Thin': 2,
            'Thick Eager Zero': 3
        }

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            proxy_client=None,
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

                proxy_client          (str)  --  proxy client to be used for restore
                                                        default: proxy added in subclient

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

        disk_option_value = self._disk_option[disk_option]

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        if proxy_client is not None:
            restore_option['client'] = proxy_client

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
            copy_precedence=copy_precedence
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        ovf_disk = {
            "name": restore_option["vm_to_restore"][0]+".ovf",
            "Datastore": ""
        }
        # Add the new disk object to the existing disks list
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
            'diskLevelVMRestoreOption']['advancedRestoreOptions'][0]['disks'].append(ovf_disk)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            restored_vm_name=None,
            destination_client=None,
            cluster=None,
            storage=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            proxy_client=None,
            **kwargs
    ):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore            (str)    --  VM that is to be restored

                restored_vm_name         (str)    --  new name of vm. If nothing is passed,
                                                      'delete' is appended to the original vm name

                destination_client   (str) --  name of the RHEV client where the VM
                                                      should be restored.

                cluster           (str)    --  destination cluster host. Restores to the source
                                                      VM cluster if this value is not specified

                storage         (str)   --  datastore where the restored VM should be
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

                proxy_client      (str)    --  destination proxy client

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

        # check mandatory input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, str):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client'] = proxy_client

        if restored_vm_name:
            if not(isinstance(vm_to_restore, str) or
                   isinstance(restored_vm_name, str)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_vm_name

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=destination_client,
            datastore=storage,
            esx_host=cluster,
            cluster=cluster,
            esx_server='',
            unconditional_overwrite=overwrite,
            power_on=power_on,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            disk_option=self._disk_option[disk_option],
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            source_item=[]
        )
        request_json = self._prepare_fullvm_restore_json(restore_option)
        ovf_disk = {
            "name": restore_option["vm_to_restore"][0]+".ovf",
            "Datastore": restore_option["datastore"]
        }
        # Add the new disk object to the existing disks list
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
            'diskLevelVMRestoreOption']['advancedRestoreOptions'][0]['disks'].append(ovf_disk)
        return self._process_restore_response(request_json)
