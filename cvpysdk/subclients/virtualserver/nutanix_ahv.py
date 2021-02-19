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

"""File for operating on a Virtual Server Nutanix AHV Subclient.

nutanixsubclient is the only class defined in this file.

nutanixsubclient: Derived class from VirtualServerSubClient  Base class, representing a
                           nutanix AHV Subclient, and to perform operations on that Subclient

nutanixsubclient:

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                        to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()                      --  restores the VM specified by the
                                                        user to the same location
"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class nutanixsubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    nutanix  virtual server subclient,and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        self.diskExtension = ["none"]
        super(nutanixsubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def full_vm_restore_out_of_place(self,
                                     vm_to_restore=None,
                                     host=None,
                                     container=None,
                                     proxy_client=None,
                                     restore_new_name=None,
                                     overwrite=True,
                                     power_on=True,
                                     copy_precedence=0,
                                     restore_option=None):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
                    at the specified destination location.

                    Args:

                        vm_to_restore         (list)       --  provide the VM name to restore

                        host                  (str)        -- ESX host for Vm to restore

                        container             (str)        -- provide the storage account to restore

                        proxy_client          (str)        -- provide the proxy client to restore

                        restore_new_name      (str)        -- provide the new restore name
                        overwrite
                                default:False (bool)       --  overwrite the existing VM

                        poweron
                                default:False (bool)       --  power on the  restored VM


                        restore_option        (dict)       --  complete dictionary with
                                                               all advanced option
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
        # restore options
        if restore_option is None:
            restore_option = {}

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
            esx_host=host,
            datastore=container,
            client_name=proxy_client,
            in_place=False,
            restore_new_name=restore_new_name
        )

        # set attr for all the option in restore xml from user inputs

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 copy_precedence=0):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore          (list)      --  provide the VM name to restore

                overwrite
                        default:true   (bool)      --  overwrite the existing VM

                poweron
                        default:true   (bool)      --  power on the  restored VM

                copy_precedence        (int)       -- storage policy copy precedence
                                                      from which browse has to be performed


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
            destination_network=None
        ):
        """
        Conversion from AHV VM to VMware
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
        disk_options = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
            'diskLevelVMRestoreOption']
        for disk_info in disk_options['advancedRestoreOptions'][0]['disks']:
            disk_info['newName'] = ''

        return self._process_restore_response(request_json)
