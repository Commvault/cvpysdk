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

"""File for operating on a Virtual Server VMInstance Subclient.

VMInstanceSubclient is the only class defined in this file.

VMInstanceSubclient:   Derived class from Subclient Base
                                class,representing a VMInstance Subclien

VMInstanceSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of vminstance subclient class,
                                    associated with the VirtualServer subclient

    backup()                    --  run a backup job for the subclient
"""

from ..subclient import Subclient
from ..exception import SDKException
import copy


class VMInstanceSubclient(Subclient):
    """
    Derived class from Subclient Base class.
    This represents a VMInstance virtual server subclient
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Initialize the Instance object for the given Virtual Server instance.

           Args:
               backupset_object    (object)  --  instance of the Backupset class

               subclient_name   (str)        --  subclient name

               subclient_id     (int)           --  subclient id

        """
        super(VMInstanceSubclient, self).__init__(backupset_object, subclient_name, subclient_id)

        self._client_vm_status = copy.deepcopy(self._client_object.properties['vmStatusInfo'])
        self._parent_client = None
        self._parent_instance = None
        self._parent_agent = None
        self._parent_backupset = None
        self._parent_subclient = None
        self._vm_guid = None
        self.filter_types = {
            '1': 'Datastore',
            '2': 'Virtual Disk Name/Pattern',
            '3': 'Virtual Device Node',
            '4': 'Container',
            '5': 'Disk Label',
            '6': 'Disk Type',
            '9': 'Disk Tag Name/Value',
            '10': 'Repository'
        }

    @property
    def parent_client(self):
        """Returns parent client object
        Returns:
            object          -   Parent client object"""
        if not self._parent_client:
            _parent_client = self._client_vm_status.get('vsaSubClientEntity', {}).get('clientName')
            if _parent_client:
                self._parent_client = self._commcell_object.clients.get(_parent_client)
        return self._parent_client

    @property
    def parent_agent(self):
        """Returns parent agent object
        Returns:
            object          -   Parent agent object"""
        if self.parent_client and not self._parent_agent:
            _parent_agent = self._client_vm_status.get('vsaSubClientEntity', {}).get('appName')
            if _parent_agent:
                self._parent_agent = self.parent_client.agents.get(_parent_agent)
        return self._parent_agent

    @property
    def parent_instance(self):
        """Returns parent instance object
        Returns:
            object          -   Parent instance object"""
        if self.parent_agent and not self._parent_instance:
            _parent_instance = self._client_vm_status.get('vsaSubClientEntity', {}).get('instanceName')
            if _parent_instance:
                self._parent_instance = self.parent_agent.instances.get(_parent_instance)
        return self._parent_instance

    @property
    def parent_backupset(self):
        """Returns parent backupset object
        Returns:
            object          -   Parent backupset object"""
        if self.parent_instance and not self._parent_backupset:
            _parent_backupset = self._client_vm_status.get('vsaSubClientEntity', {}).get('backupsetName')
            if _parent_backupset:
                self._parent_backupset = self.parent_instance.backupsets.get(_parent_backupset)
        return self._parent_backupset

    @property
    def parent_subclient(self):
        """Returns parent subclient object
        Returns:
            object          -   Parent subclient object"""
        if self.parent_backupset and not self._parent_subclient:
            _parent_subclient = self._client_vm_status.get('vsaSubClientEntity', {}).get('subclientName')
            if _parent_subclient:
                self._parent_subclient = self.parent_backupset.subclients.get(_parent_subclient)
        return self._parent_subclient

    @property
    def vm_guid(self):
        """Returns vm guid
        Returns:
            str          -   vm guid of the client"""
        if not self._vm_guid:
            self._vm_guid = self._client_vm_status.get('strGUID')
        return self._vm_guid

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               schedule_pattern=None):
        """Runs a backup job for the vm subclient of the level specified.

            Args:
                backup_level            (str)   --  level of backup the user wish to run
                                                    Full / Incremental / Differential /
                                                    Synthetic_full

                incremental_backup      (bool)  --  run incremental backup
                                                    only applicable in case of Synthetic_full backup

                incremental_level       (str)   --  run incremental backup before/after synthetic full
                                                    BEFORE_SYNTH / AFTER_SYNTH
                                                    only applicable in case of Synthetic_full backup

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

            Returns:
                object - instance of the Job class for this backup job if its an immediate Job

                         instance of the Schedule class for the backup job if its a scheduled Job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        backup_level = backup_level.lower()
        if backup_level not in ['full', 'incremental',
                                'differential', 'synthetic_full']:
            raise SDKException('Subclient', '103')

        if schedule_pattern or len(self._instance_object.backupsets) > 1:
            advanced_options = {'vsaBackupOptions': {}}
            advanced_options['vsaBackupOptions']['selectiveVMInfo'] = [{'vmGuid': self.vm_guid}]
            if self.parent_subclient:
                request_json = self.parent_subclient._backup_json(
                    backup_level=backup_level,
                    incremental_backup=incremental_backup,
                    incremental_level=incremental_level,
                    schedule_pattern=schedule_pattern,
                    advanced_options=advanced_options
                )
                backup_service = self._commcell_object._services['CREATE_TASK']

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'POST', backup_service, request_json
                )
            else:
                raise SDKException('Subclient', 102, 'Not able to get Parent Subclient')
        else:
            vm_backup_service = self._commcell_object._services['VM_BACKUP'] % (self.vm_guid, backup_level)
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', vm_backup_service
            )
        return self._process_backup_response(flag, response)

    def _get_subclient_properties(self):
        """Gets the subclient related properties of Virtual server subclient"""

        self._vmDiskFilter = None
        super(VMInstanceSubclient, self)._get_subclient_properties()

        if 'vmDiskFilter' in self._subclient_properties:
            self._vmDiskFilter = self._subclient_properties['vmDiskFilter']
        if 'vmBackupInfo' in self._subclient_properties:
            self._vmBackupInfo = self._subclient_properties['vmBackupInfo']
        if 'vsaSubclientProp' in self._subclient_properties:
            self._vsaSubclientProp = self._subclient_properties['vsaSubclientProp']

    @property
    def quiesce_file_system(self):
        """
            Gets the quiesce value set for the vsa subclient

        Returns:
            (Boolean)    True/False
        """
        quiesce_file_system = r'quiesceGuestFileSystemAndApplications'
        return self._vsaSubclientProp.get(quiesce_file_system)

    @property
    def vm_diskfilter(self):
        """Gets the appropriate Diskfilter from the VM instance subclient relevant to the user.

            Returns:
                list - list of Diskfilter associated with the subclient

        """
        vm_diskfilter = []
        if self._vmDiskFilter is not None:
            subclient_diskfilter = self._vmDiskFilter

            if 'filters' in subclient_diskfilter:
                filters = subclient_diskfilter['filters']

                for child in filters:
                    filter_type_id = str(child['filterType'])
                    filter_type = self.filter_types[str(child['filterType'])]
                    vm_id = child['vmGuid'] if 'vmGuid' in child else None
                    filter_name = child['filter']
                    value = child['value']
                    vm_name = child['vmName']

                    temp_dict = {
                        'filter': filter_name,
                        'filterType': filter_type,
                        'vmGuid': vm_id,
                        'filterTypeId': filter_type_id,
                        'value': value,
                        'vmName': vm_name
                    }

                    vm_diskfilter.append(temp_dict)
        else:
            vm_diskfilter = self._vmDiskFilter

        if len(vm_diskfilter) == 0:
            vm_diskfilter = None
        return vm_diskfilter
