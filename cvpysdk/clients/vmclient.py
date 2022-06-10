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
from ..job import Job
from ..exception import SDKException
from ..client import Client


class VMClient(Client):
    """ Class for representing client of a vm client."""

    def __init__(self, commcell_object, client_name, client_id=None):
        """Initialise the VM Client class instance.

            Args:
                commcell_object (object)     --  instance of the Commcell class

                client_name     (str)        --  name of the client

                client_id       (str)        --  id of the client
                                                default: None

            Returns:
                object - instance of the VM Client class
        """
        super(VMClient, self).__init__(commcell_object, client_name, client_id)

    def _return_parent_subclient(self):
        """
        Returns the parent subclient if the client is VSA client and is backed up else returns None

        Returns:
            _parent_subclient           (object)   :        Subclient object

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

    def _child_job_subclient_details(self, parent_job_id):
        """
        Returns the  child subclient details

        Args:
            parent_job_id           (string):       job id of the parent

        Returns:
            _child_job_obj          (dict):         Child subclient details:
                                    eg: {
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

    def full_vm_restore_in_place(self, **kwargs):
        """Restores in place  FULL Virtual machine for the client

        Args:
            **kwargs                         : Arbitrary keyword arguments Properties as of
                                                full_vm_restore_in_place
            eg:
                            overwrite             (bool)        --  overwrite the existing VM

                            power_on              (bool)        --  power on the  restored VM

                            copy_precedence       (int)         --  copy precedence value

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

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

    def full_vm_restore_out_of_place(self, **kwargs):
        """Restores out of place FULL Virtual machine for the client

        Args:
            **kwargs                         : Arbitrary keyword arguments Properties as of
                                                full_vm_restore_out_of_place
            ex:
                        restored_vm_name         (str)    --  new name of vm. If nothing is passed,
                                                                'del' is appended to the original vm name

                        vcenter_client    (str)    --  name of the vcenter client where the VM
                                                              should be restored.

                        esx_host          (str)    --  destination esx host. Restores to the source
                                                              VM esx if this value is not specified

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

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
