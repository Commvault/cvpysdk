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

"""File for operating on a Virtual Server Googlecloud Subclient.

GooglecloudVirtualServerSubclient is the only class defined in this file.

GooglecloudVirtualServerSubclient: Derived class from VirtualServerSubClient  Base class,
                                   representing a FusionCompute Subclient, and
                                   to perform operations on that Subclient

GooglecloudVirtualServerSubclient:

    __init__(,backupset_object, subclient_name, subclient_id)--  initialize object of googlecloud
                                                                             subclient object
                                                                                 associated with
                                                                        the VirtualServer subclient

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                     to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()              --  restores the VM specified by the
                                                    user to the same location
"""

from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class GooglecloudVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a Google cloud virtual server subclient,
       and can perform restore operations on only that subclient.

    """
    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        super(GooglecloudVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = ["none"]

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            overwrite=True,
            power_on=True,
            proxy_client=None,
            copy_precedence=0,
            **kwargs):
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

                copy_precedence     (int)      --  copy precedence value
                                                   default: 0

                proxy_client          (basestring)  --  proxy client to be used for restore
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
            proxy_client=None,
            new_name=None,
            zone=None,
            machine_type=None,
            overwrite=True,
            power_on=True,
            public_ip=False,
            copy_precedence=0,
            project_id=None,
            restore_option=None,
            **kwargs):

        """Restores the FULL Virtual machine specified  in the input  list to the client,
            at the specified destination location.


            Args:
                vm_to_restore     (list):       provide the VM name to restore
                                                default: None

                proxy_client     (str):         proxy client to be used for restore
                                                default: proxy added in subclient

                new_name         (str):         new name to be given to the
                                                restored VM

                overwrite         (bool):        overwrite the existing VM
                                                 default: True

                power_on          (bool):        power on the  restored VM
                                                  default: True

                copy_precedence   (int)        -- copy precedence value
                                                  default: 0

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_out_of_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details
                    destination_network (string)     -- Name of the destination network
                    networks_nic        (string)     -- Link for the destination network
                    subnetwork_nic      (string)    -- Link for the destination subnetwork

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
        extra_options = ['destination_network', 'networks_nic', 'subnetwork_nic']
        for key in extra_options:
            if key in kwargs:
                restore_option[key] = kwargs[key]
            else:
                restore_option[key] = None

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        if new_name:
            restore_option['restore_new_name'] = new_name

        if bool(restore_option):
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
            client_name=proxy_client,
            esx_host=zone,
            vm_size=machine_type,
            datacenter=zone,
            in_place=False,
            createPublicIP=public_ip,
            project_id=project_id,
            restore_new_name=new_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
