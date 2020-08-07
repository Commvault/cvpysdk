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

"""File for operating on a Virtual Server FusionCompute Subclient.

XenSubclient is the only class defined in this file.

XenSubclient: Derived class from VirtualServerSubClient  Base class,
                            representing a FusionCompute Subclient, and
                            to perform operations on that Subclient

XenSubclient:

    __init__(,backupset_object, subclient_name, subclient_id)--  initialize object of FusionCompute
                                                                             subclient object
                                                                                 associated with
                                                                        the VirtualServer subclient

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                     to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()              --  restores the VM specified by the
                                                    user to the same location
"""
from past.builtins import basestring
from cvpysdk.exception import SDKException
from ..vssubclient import VirtualServerSubclient


class Xen(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a Fusion Compute virtual server subclient,
       and can perform restore operations on only that subclient.

    """
    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        super(Xen, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = ["none"]

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            overwrite=True,
            power_on=True,
            proxy_client=None,
            copy_precedence=0):
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


                proxy_client          (basestring)  --  proxy client to be used for restore
                                                        default: proxy added in subclient

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
        restore_option = {}

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            volume_level_restore=1,
            client_name=proxy_client,
            in_place=True
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            destination_client=None,
            proxy_client=None,
            new_name=None,
            xen_server=None,
            storage=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore     (list)  --  provide the VM name to restore
                                              default: None

                destination_client    (basestring) -- name of the Pseudo client
                                                  where the VM should be
                                                    restored.

                new_name          (basestring) -- new name to be given to the
                                                    restored VM

                xen_server          (basestring) -- destination cluster or  host
                                                    restores to the source VM
                                                    esx if this value is not
                                                    specified

                storage         (basestring) -- datastore where the
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

                proxy_client     (basestring)  --  proxy client to be used for restore
                                                        default: proxy added in subclient


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

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        if new_name:
            if not(isinstance(vm_to_restore, basestring) or
                   isinstance(new_name, basestring)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = new_name

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            client_name=proxy_client,
            vcenter_client=destination_client,
            esx_host=xen_server,
            datastore=storage,
            in_place=False,
            restore_new_name=new_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
