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

"""File for operating on a Virtual Server Nutanix AHV prism central Subclient.

nutanixprismcentralsubclient is the only class defined in this file.

nutanixprismcentralsubclient: Derived class from VirtualServerSubClient Base class,
representing a nutanix AHV prism central Subclient, and to perform operations on
that Subclient

nutanixprismcentralsubclient:

    full_vm_restore_out_of_place() -- restores the VM specified in
                                      to the specified client, at the
                                      specified destination location
"""

from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class nutanixprismcentralsubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class, representing a
    Nutanix Prism Central virtual server subclient and performing operations
    on that subclient.
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the instance object for the given Virtual Server subclient.

        Args:
            backupset_object: Instance of the backupset class.
            subclient_name (str): Name of the subclient.
            subclient_id (int, optional): ID of the subclient.
        """
        self.diskExtension = ["none"]
        super(nutanixprismcentralsubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore: list[str] | None = None,
            container: str | None = None,
            proxy_client: str | None = None,
            restore_new_name: str | None = None,
            overwrite: bool = True,
            power_on: bool = True,
            copy_precedence: int = 0,
            restore_option: dict | None = None,
            vcenter_client: str | None = None,
            cluster: str | None = None,
            esx_server: str | None = None,
            **kwargs
            ):
        """Perform a full VM restore to a new location (out-of-place restore).

            Args:
                vm_to_restore (list[str]): List of VM names to restore.
        
                container (str): Storage container or datastore where the VM
                    should be restored.
        
                proxy_client (str): Proxy client used to perform the restore operation.
        
                restore_new_name (str): New name for the restored VM.
        
                overwrite (bool): Whether to overwrite an existing VM with the
                    same name at the destination.
                    Default: True
        
                power_on (bool): Whether to power on the VM after restore
                    completes.
                    Default: True
        
                copy_precedence (int): Copy precedence to use for restore.
                    Default: 0
        
                restore_option (dict): Dictionary containing advanced restore
                    options and configurations.
        
                vcenter_client (str): Name of the vCenter client where the VM
                    should be restored.
        
                cluster (str): Destination cluster where the VM should be restored.
        
                esx_server (str): Destination ESX host where the VM should be restored.
        
                **kwargs: Reserved for additional restore configuration options.
                    Example:
                        v2_details (dict): Details required for v2 subclient restore.
                        See:
                        clients.vmclient.VMClient._child_job_subclient_details
        
            Example:
                >>> job = helper.full_vm_restore_out_of_place(
                ...     vm_to_restore=["TestVM"],
                ...     container="datastore1",
                ...     proxy_client="proxy1",
                ...     restore_new_name="TestVM_Restore",
                ...     power_on=True
                ... )
                >>> print(job.job_id)
        
            Returns:
                Job: Instance of the Job class representing the restore job.
        
            Raises:
                SDKException: If restore initialization fails, response is empty,
                or the restore operation fails.
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
            esx_server=esx_server,
            vcenter_client=vcenter_client,
            datastore=container,
            client_name=proxy_client,
            in_place=False,
            restore_new_name=restore_new_name,
            cluster=cluster
        )

        # set attr for all the option in restore xml from user inputs

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)