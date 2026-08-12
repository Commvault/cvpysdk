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


"""
File for operating on a Virtual Server Morpheus Subclient.

MorpheusSubclient is the only class defined in this file.

MorpheusSubclient: Derived class from VirtualServerSubclient Base class, representing a
                           Morpheus Subclient, and to perform operations on that Subclient

MorpheusSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of morpheus subclient class,
                                    associated with the VirtualServer subclient

    full_vm_restore_in_place()  --  restores the VM specified by the user to
                                    the same location

    full_vm_restore_out_of_place() -- restores the VM specified to the provided
                                      Morpheus psuedoclient
"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class MorpheusSubclient(VirtualServerSubclient):
    """
    Derived class from VirtualServerSubclient Base class, representing a
    Morpheus virtual server subclient, and to perform operations on that subclient.
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Initialize the instance of MorpheusSubclient class.

        Args:
            backupset_object (object)  --  instance of the backupset class
            subclient_name   (str)     --  name of the subclient
            subclient_id     (str)     --  id of the subclient (optional)
        """

        super(MorpheusSubclient, self).__init__(backupset_object, subclient_name, subclient_id)
        self.diskExtension = ["ide", "scsi", "sata", "virtio", "qcow2", "none"]

    def full_vm_restore_in_place(self, vm_to_restore,destination_client, proxy_client, overwrite,power_on, copy_precedence):
        """
        Restores the full Virtual Machine specified in the input list to the specified client, at the specified
        destination location.

        Args:
            vm_to_restore    (list)  --  list of VMs to restore
            proxy_client     (str)   --  proxy client to be used for restore
            overwrite        (bool)  --  overwrite the existing VM (default: True)
            power_on         (bool)  --  power on the restored VM (default: True)
            copy_precedence  (int)   --  copy precedence value (optional)

        Returns:
            object - instance of the Job class for this restore job
        """
        restore_option = {}

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client_name'] = proxy_client

        if vm_to_restore and not isinstance(vm_to_restore, list):
            vm_to_restore = [vm_to_restore]

        self._set_restore_inputs(
            restore_option,
            in_place=True,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            destination_client=destination_client,
            unconditional_overwrite = overwrite,
            power_on = power_on,
            copy_precedence=copy_precedence,
            volume_level_restore = 1
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(self, vm_to_restore, destination_client, proxy_client, overwrite, power_on,
                                     copy_precedence, esx_host, datastore, cluster, datacenter):
        """
        Restores the full Virtual Machine specified in the input list to the specified client, at the specified
        destination location.

        Args:
            vm_to_restore    (list)  --  list of VMs to restore
            proxy_client     (str)   --  proxy client to be used for restore
            datastore        (str)   --  datastore where the VM should be restored
            esx_host         (str)   --  host where the VM should be restored
            cluster          (str)   --  cluster where the vm should be restored
            datacenter       (str)   --  cloud where the vm should be restored
            overwrite        (bool)  --  overwrite the existing VM (default: True)
            power_on         (bool)  --  power on the restored VM (default: True)
            copy_precedence  (int)   --  copy precedence value (optional)

        Returns:
            object - instance of the Job class for this restore job
        """
        restore_option = {}

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client_name'] = proxy_client

        if vm_to_restore and not isinstance(vm_to_restore, list):
            vm_to_restore = [vm_to_restore]

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            destination_client=destination_client,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            esx_host=esx_host,
            datastore=datastore,
            cluster=cluster,
            datacenter=datacenter,
            volume_level_restore=1
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
