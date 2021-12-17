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


"""File for operating on a Virtual Server Azure Subclient.

AzureSubclient is the only class defined in this file.

AzureSubclient: Derived class from VirtualServerSubClient  Base class, representing a
                           Azure Subclient, and to perform operations on that Subclient

AzureSubclient:

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                     to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()              --  restores the VM specified by the
                                                    user to the same location
"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class AzureSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    Azure  virtual server subclient,and to perform operations on that subclient."""

    def full_vm_restore_out_of_place(self,
                                     vm_to_restore=None,
                                     cloud_service=None,
                                     storage_account=None,
                                     proxy_client=None,
                                     restore_new_name=None,
                                     overwrite=False,
                                     power_on=False,
                                     copy_precedence=0,
                                     restore_option=None,
                                     **kwargs):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            at the specified destination location.

            Args:
                cloud_service         (str)        --  provide the cloud service

                storage_account     (str)          --  provide the storage account

                vm_to_restore         (list)       --  provide the VM name to restore

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
            esx_host=cloud_service,
            datastore=storage_account,
            client_name=proxy_client,
            out_place=True,
            restore_new_name=restore_new_name
        )

        # set attr for all the option in restore xml from user inputs

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 copy_precedence=0,
                                 **kwargs):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore         (list)       --  provide the VM name to restore

                overwrite
                        default:true   (bool)      --  overwrite the existing VM

                power_on                (bool)      --  power on the  restored VM
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
            copy_preceedence=copy_precedence,
            volume_level_restore=1,
            out_place=False
        )
        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
    