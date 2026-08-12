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
VMClient class is defined in this file.

VMClient:     Class for a single vm client of the commcell

VMClient
=======

_return_parent_subclient()              --  Returns the parent subclient where the vm has been backed up

_child_job_subclient_details()          --  returns the subclient details of the child job

full_vm_restore_in_place()              --  Performs in place full vm restore and return job object

full_vm_restore_out_of_place()          --  Performs out of place full vm restore and return job object
"""

import copy
from typing import Any, Dict, Optional
from cvpysdk.commcell import Commcell
from ..job import Job
from ..exception import SDKException
from ..client import Client

class VMClient(Client):
    """
    Represents a client for managing virtual machine (VM) operations within a CommCell environment.

    This class provides an interface for interacting with VM clients, enabling operations such as
    retrieving subclient details, handling parent-child job relationships, and performing full VM
    restore operations both in-place and out-of-place.

    Key Features:
        - Initialization with CommCell object, client name, and client ID
        - Retrieval of parent subclient information
        - Access to child job subclient details based on parent job ID
        - Full VM restore operations in-place
        - Full VM restore operations out-of-place

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', client_name: str, client_id: Optional[str] = None) -> None:
        """Initialize a VMClient instance with Commcell connection and client details.

        Args:
            commcell_object: Instance of the Commcell class for SDK operations.
            client_name: Name of the VM client as a string.
            client_id: Optional client ID as a string. If not provided, defaults to None.

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> vm_client = VMClient(commcell, "VMClient01", client_id="12345")
            >>> # The VMClient object is now initialized and ready for use

        #ai-gen-doc
        """
        super(VMClient, self).__init__(commcell_object, client_name, client_id)

    def _return_parent_subclient(self) -> Optional[Any]:
        """Retrieve the parent subclient for a VSA client if it is backed up.

        This method checks if the current VM client is a VSA client and has backup information.
        If so, it returns the corresponding parent Subclient object; otherwise, it returns None.

        Returns:
            The parent Subclient object if available, or None if the client is not backed up.

        Example:
            >>> vm_client = VMClient(...)
            >>> parent_subclient = vm_client._return_parent_subclient()
            >>> if parent_subclient:
            ...     print("Parent subclient found:", parent_subclient)
            ... else:
            ...     print("No parent subclient available for this VM client.")

        #ai-gen-doc
        """
        _subclient_entity = copy.deepcopy(self.properties.get('vmStatusInfo', {}).get('vsaSubClientEntity'))
        if _subclient_entity:
            _parent_client = self._commcell_object.clients.get(_subclient_entity.get('clientName'))
            _parent_agent = _parent_client.agents.get(_subclient_entity.get('appName'))
            _parent_instance = _parent_agent.instances.get(_subclient_entity.get('instanceName'))
            _parent_backupset = _parent_instance.backupsets.get(_subclient_entity.get('backupsetName'))
            _parent_subclient = _parent_backupset.subclients.get(_subclient_entity.get('subclientName'))
            return _parent_subclient
        else:
            return None

    def _child_job_subclient_details(self, parent_job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the subclient details for a child job associated with the given parent job ID.

        Args:
            parent_job_id: The job ID of the parent job as a string.

        Returns:
            Dictionary containing child subclient details if found, otherwise None.
            Example structure:
                {
                    'clientName': 'vm_client1',
                    'instanceName': 'VMInstance',
                    'displayName': 'vm_client1',
                    'backupsetId': 12,
                    'instanceId': 2,
                    'subclientId': 123,
                    'clientId': 1234,
                    'appName': 'Virtual Server',
                    'backupsetName': 'defaultBackupSet',
                    'applicationId': 106,
                    'subclientName': 'default'
                }

        Example:
            >>> vm_client = VMClient(...)
            >>> subclient_details = vm_client._child_job_subclient_details('123456')
            >>> if subclient_details:
            ...     print(f"Subclient Name: {subclient_details['subclientName']}")
            ... else:
            ...     print("No child subclient details found for the given parent job ID.")

        #ai-gen-doc
        """
        _parent_job_obj = Job(self._commcell_object, parent_job_id)
        _child_jobs = _parent_job_obj.get_child_jobs()
        if _child_jobs:
            _child_job = None
            for _job in _child_jobs:
                if self.vm_guid == _job['GUID']:
                    _child_job = _job['jobID']
                    break
            if not _child_job:
                return None
            _child_job_obj = Job(self._commcell_object, _child_job)
            return _child_job_obj.details.get('jobDetail', {}).get('generalInfo', {}).get('subclient')
        else:
            return None

    def full_vm_restore_in_place(self, **kwargs: Any):
        """Perform an in-place full restore of the virtual machine for this client.

        This method initiates a full VM restore in place, using the provided keyword arguments to customize the restore operation.
        Common options include overwriting the existing VM, powering on the restored VM, and specifying copy precedence.

        Args:
            **kwargs: Arbitrary keyword arguments to control restore behavior.
                Supported options include:
                    overwrite (bool): Whether to overwrite the existing VM.
                    power_on (bool): Whether to power on the restored VM after completion.
                    copy_precedence (int): Copy precedence value for the restore.

        Returns:
            Job: Instance of the Job class representing the restore job, or None if the VM GUID is not available.

        Raises:
            SDKException: If input types are incorrect, job initialization fails, response is empty, or restore is unsuccessful.

        Example:
            >>> client = VMClient(...)
            >>> job = client.full_vm_restore_in_place(overwrite=True, power_on=True, copy_precedence=2)
            >>> if job:
            ...     print(f"Restore job started: {job}")
            ... else:
            ...     print("Restore could not be initiated for this VM client.")

        #ai-gen-doc
        """
        if self.vm_guid:
            _sub_client_obj = self._return_parent_subclient()
            kwargs.pop('vm_to_restore', None)
            if self.properties.get('clientProps', {}).get('isIndexingV2VSA'):
                _child_details = self._child_job_subclient_details(self.properties['vmStatusInfo']['vmBackupJob'])
                vm_restore_job = _sub_client_obj.full_vm_restore_in_place(vm_to_restore=self.name,
                                                                          v2_details=_child_details,
                                                                          **kwargs)
            else:
                vm_restore_job = _sub_client_obj.full_vm_restore_in_place(vm_to_restore=self.name,
                                                                          **kwargs)
            return vm_restore_job
        else:
            return None

    def full_vm_restore_out_of_place(self, **kwargs: Any):
        """Perform an out-of-place full restore of the virtual machine for this client.

        This method initiates a full VM restore to a different location or configuration, allowing you to specify
        properties such as the restored VM name, target vCenter client, and destination ESX host.

        Keyword Args:
            restored_vm_name (str): New name for the restored VM. If not provided, 'del' is appended to the original VM name.
            vcenter_client (str): Name of the vCenter client where the VM should be restored.
            esx_host (str): Destination ESX host. If not specified, restores to the source VM's ESX host.
            Additional keyword arguments may be supported depending on restore requirements.

        Returns:
            Job: Instance of the Job class representing the restore job, or None if the VM GUID is not available.

        Raises:
            SDKException: If input types are incorrect, job initialization fails, response is empty, or response is not successful.

        Example:
            >>> vm_client = VMClient(...)
            >>> job = vm_client.full_vm_restore_out_of_place(
            ...     restored_vm_name="RestoredVM01",
            ...     vcenter_client="vCenterProd",
            ...     esx_host="esxhost01"
            ... )
            >>> if job:
            ...     print(f"Restore job started: {job}")
            >>> else:
            ...     print("Restore could not be initiated for this VM client.")

        #ai-gen-doc
        """
        if self.vm_guid:
            _sub_client_obj = self._return_parent_subclient()
            kwargs.pop('vm_to_restore', None)
            if self.properties.get('clientProps', {}).get('isIndexingV2VSA'):
                _child_details = self._child_job_subclient_details(self.properties['vmStatusInfo']['vmBackupJob'])
                vm_restore_job = _sub_client_obj.full_vm_restore_out_of_place(vm_to_restore=self.name,
                                                                              v2_details=_child_details,
                                                                              **kwargs)
            else:
                vm_restore_job = _sub_client_obj.full_vm_restore_out_of_place(vm_to_restore=self.name,
                                                                              **kwargs)
            return vm_restore_job
        else:
            return None
