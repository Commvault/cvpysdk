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
ReplicationPairs: Class for a group of replication pairs from the replication monitor

ReplicationPairs Methods:
--------------------------
__init__(commcell_object, **kwargs)     -- Initializes the Replication pairs class with Commcell object and filters
__str__()                               -- Returns the list of all replication pairs as a string
__repr__()                              -- Return the string representation for Replication pairs class
refresh()                               -- Refreshes the list of Replication pairs
_get_replication_pairs()                -- Internal method to fetch replication pairs information from CommServ
**replication_pairs**                   -- Returns the dictionary of replication pair IDs with their information
get(replication_id)                     -- Returns the ReplicationPair class associated to replication ID


ReplicationPair: Class for monitoring a replication pair which exists on periodic monitor

ReplicationPair Attributes:
--------------------------

**vm_pair_id**          -- Returns the live sync VM pair ID

**vm_pair_name**        -- Returns the live sync VM pair name

**replication_guid**    -- Returns the replication guid of the live sync pair

**source_vm**           -- Returns the name of the source virtual machine

**destination_vm**      -- Returns the name of the destination virtual machine

**destination_client**  -- Returns the destination client of the Live sync VM pair

**destination_proxy**   -- Returns the destination proxy of the Live sync VM pair

**destination_instance**-- Returns the destination instance of the Live sync VM pair

**status**              -- Returns the status of the live sync pair

**last_synced_backup_job** -- Returns the last synced backup job ID

**latest_replication_job** -- Returns the latest replication job ID

**last_replication_job**   -- Returns the last replication job ID

**reverse_replication_schedule_id -- Returns the ID of the reverse replication schedule
"""
from ..exception import SDKException
from ..subclients.virtualserver.livesync.vsa_live_sync import LiveSyncVMPair


class ReplicationPairs:
    """Class for a group of replication pairs from the replication monitor"""

    def __init__(self, commcell_object, **kwargs):
        """
        Constructor method for replication monitor with filtering on the basis of kwargs
        Args:
            commcell_object (Commcell): CVPySDK commcell object
            kwargs (dict): The arguments passed for filtering replication pairs
                application_id: The application ID for the replication pairs. eg: 106 for VSA
                instance_id: The instance ID for the source instance associated
                subclient_id: The ID of VM group to find associated pairs for
                schedule_id: The ID of the replication schedule that replication pairs are part of
                failover_group_id: The ID of the failover group that is used for DROrchestration
        """
        self._commcell_object = commcell_object
        self._cypysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services

        self._filter_args = kwargs

        self._REPLICATION_PAIRS = self._services['GET_REPLICATION_PAIRS']
        if self._filter_args.get('application_id'):
            self._REPLICATION_PAIRS += f'applicationId={self._filter_args.get("application_id")}&'
        if self._filter_args.get('instance_id'):
            self._REPLICATION_PAIRS += f'instanceId={self._filter_args.get("instance_id")}&'
        if self._filter_args.get('subclient_id'):
            self._REPLICATION_PAIRS += f'subclientId={self._filter_args.get("subclient_id")}&'
        if self._filter_args.get('schedule_id'):
            self._REPLICATION_PAIRS += f'taskId={self._filter_args.get("schedule_id")}&'
        if self._filter_args.get('failover_group_id'):
            self._REPLICATION_PAIRS += f'vAppId={self._filter_args.get("failover_group_id")}&'

        self._replication_pairs = {}

        self.refresh()

    def __str__(self):
        """
        Representation string consisting of all Replication VM pairs.
        Returns: (str) table of all replication pairs
        """
        representation_string = ('{:^5}\t{:^20}\t{:^25}\t{:^25}\n\n'
                                 .format('S. No.', 'Replication ID', 'Source Name', 'Destination Name'))

        for index, replication_pair in enumerate(self.replication_pairs):
            replication_pair_dict = self.replication_pairs[replication_pair]
            sub_str = ('{:^5}\t{:^20}\t{:^25}\t{:^25}\n\n'
                       .format(index + 1,
                               replication_pair,
                               replication_pair_dict.get('source_vm'),
                               replication_pair_dict.get('destination_vm')
                               ))
            representation_string += sub_str
        return representation_string.strip()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = f'ReplicationPairs class instance for Filters: "{self._filter_args}"'
        return representation_string

    def refresh(self):
        """Re-populate the replication monitor information"""
        self._get_replication_pairs()

    def _get_replication_pairs(self):
        """
        Gets the list of replication pairs associated to the filters
        Returns: (dict) Dictionary of all replication pairs for the filters
                {
                    "id1": {
                        "source_vm": "sourceVM1",
                        "destination_vm": "sourceVM1DRVM"
                    },
                    "id2": {
                        "source_vm": "sourceVM2",
                        "destination_vm": "sourceVM2DR"
                    }
                }
        Raises:
            SDKException:
                if response is empty
                if response is not success
        """
        flag, response = self._cypysdk_object.make_request('GET', self._REPLICATION_PAIRS)

        if flag:
            if response.json() and 'siteInfo' in response.json():
                replication_pairs = {}
                for site_info in response.json().get('siteInfo', []):
                    replication_pairs[str(site_info.get('replicationId', 0))] = {
                        'source_vm': site_info.get('sourceName', '').lower(),
                        'destination_vm': site_info.get('destinationName', '').lower()
                    }
                return replication_pairs

            raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    @property
    def replication_pairs(self):
        """
        Returns: (dict) Returns the dictionary of all the replication pairs and their info
                {
                    "id1": {
                        "source_vm": "sourceVM1",
                        "destination_vm": "sourceVM1DRVM"
                    },
                    "id2": {
                        "source_vm": "sourceVM2",
                        "destination_vm": "sourceVM2DR"
                    }
                }
        """
        return self._replication_pairs

    def get(self, replication_id: str or int):
        """
        Returns the ReplicationPair object associated to the pair ID
        Args:
            replication_id (str or int)    : The ID of the replication pair
        """
        if replication_id in self.replication_pairs:
            return ReplicationPair(self._commcell_object, str(replication_id))
        raise Exception('ReplicationPairs', '103')


class ReplicationPair(LiveSyncVMPair):
    """Class for replication pair in the replication monitor"""

    def __init__(self, commcell_object, replication_pair_id: int or str):
        """New constructor method which uses pair ID instead of Live sync objects
        Args:
            commcell_object (Commcell): CVPySDK commcell object
            replication_pair_id (int or str): The pair id of the live sync pair
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._vm_pair_id = str(replication_pair_id)

        self._VM_PAIR = self._services['GET_REPLICATION_PAIR'] % (
            self._vm_pair_id
        )

        self._properties = {}
        self._replication_guid = None
        self._status = None
        self._failover_status = None
        self._source_vm = None
        self._destination_vm = None
        self._destination_client = None
        self._destination_proxy = None
        self._destination_instance = None
        self._last_backup_job = None
        self._latest_replication_job = None

        self._subclient_object = None
        self._subclient_name = None
        self._agent_object = None
        self.live_sync_pair = None

        self.refresh()

        self._populate_live_sync()

    def __repr__(self):
        """String representation of the instance of this class."""
        return f'ReplicationPair class instance for Replication ID: "{self._vm_pair_id}"'

    def __str__(self):
        """String representation of the instance of replication pair"""
        if self._source_vm and self._destination_vm:
            return f'Replication pair: {self._source_vm} -> {self._destination_vm}'
        return f'Replication pair ID: {self._vm_pair_id}'

    def _populate_live_sync(self):
        """ Method used to populate live sync classes"""
        subclient_dict = self._properties.get('parentSubclient', {})
        subtask_dict = self._properties.get('subTask', {})

        client_name = subclient_dict.get('clientName')
        agent_name = self._properties.get('entity', {}).get('appName')
        self._subclient_id = str(subclient_dict.get('subclientId', ''))

        client_object = self._commcell_object.clients.get(client_name)
        self._agent_object = client_object.agents.get(agent_name)

        instance_name = [name for name, instance_id in
                         self._agent_object.instances.all_instances.items()
                         if instance_id == str(subclient_dict.get('instanceId', ''))][0]
        instance_object = self._agent_object.instances.get(instance_name)
        subclient = [(name, subclient_info.get('backupset')) for name, subclient_info in
                     instance_object.subclients.all_subclients.items()
                     if subclient_info.get('id') == self._subclient_id][0]

        backupset_object = instance_object.backupsets.get(subclient[-1])
        self._subclient_object = backupset_object.subclients.get(subclient[0].split('\\')[-1])
        self._subclient_name = self._subclient_object.name

        live_sync = [live_sync_name for live_sync_name, live_sync_dict in
                     self._subclient_object.live_sync.live_sync_pairs.items()
                     if live_sync_dict.get('id') == str(subtask_dict.get('taskId', ''))][0]

        self.live_sync_pair = self._subclient_object.live_sync.get(live_sync)
        self._vm_pair_name = self._source_vm
