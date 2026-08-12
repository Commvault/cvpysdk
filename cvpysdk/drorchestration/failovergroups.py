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
Main file for getting failover group related information

FailoverGroups and FailoverGroup are 2 classes defined in this file.

FailoverGroups:     Class for getting information of all failover groups in the commcell

FailoverGroup:      Class for a failover group that gives us all the live sync pairs associated to in,
                    with addition to the clients/hypervisors associated


FailoverGroups:
    FailoverGroupSourceTypes                    --  Enum to represent all type of sources for failover groups
    FailoverGroupTypes                          --  Enum to represent all types of failover groups
    DRReplicationTypes                          --  Enum to represent all live sync types
    __init__(commcell_object)                   --  Initialize the object of failovergroups class for commcell

    __str__()                                   --  Returns the list of all failover groups

    __repr__()                                  --  Returns the string for the instance of the FailoverGroups class

    has_failover_group(failover_group_name)     --  Checks if failover group exists with the given name

    get(failover_group_name)                    --  Returns the FailoverGroup class object of the given name

    refresh()                                   --  Refresh all failover groups created on the commcell

    #### internal methods ###
    _get_failover_groups()                      --  Internal call to get information of all failover groups in commcell

    ##### properties ######
    failover_groups                             --  Returns the dictionary of all failover groups and their info


FailoverGroup:
    __init__(commcell_object,
            failover_group_name)                --  Initialize object of FailoverGroup with the given name

    __repr__()                                  --  Returns the name of the failover group for the object

    __str__()                                   --  Returns the name of the all VM pairs for the failover group

    refresh()                                   --  Refresh the failover group properties

    ##### internal methods #####
    _get_failover_group_dict()                  --  Gets the failover group information from FailoverGroups class

    _get_failover_group_properties()            --  Get the failover group properties

    ##### properties #####
    failover_group_id                           --  The ID of the failover group

    failover_group_name                         --  The name of the failover group

    replication_type                            --  The DRReplicationTypes key for replication of failover group

    group_type                                  --  The FailoverGroupTypes for operation of failover group

    source_type                                 --  The FailoverGroupSourceTypes of source of failover group

    is_client_group                             --  Whether the VM pairs are part of a client group or not

    replication_pairs                           --  The ReplicationPairs class for failover group

    vm_pair_ids                                 --  The ID of the replication pairs

    vm_pairs                                    --  Returns the live sync pair objects for each VM pair of the group
                                                        as a mapping of source VM name and VM pair object

    replication_groups                          --  The names of all replication groups associated
                                                    to the failover group

    source_client                               --  The client object of the source client

    source_agent                                --  The agent object of the source client

    source_instance                             --  The instance object of the source client

    destination_client                          --  The client object of the destination client

    destination_agent                           --  The agent object of the destination client

    destination_instance                        --  The instance object of the destination instance

    is_approval_required                        --  Whether the approval is set in failover group or not

    user_for_approval                           --  Returns the name of the user set in failover group
                                                        for approval

"""
from enum import Enum
from ..exception import SDKException
from .replication_pairs import ReplicationPairs


class FailoverGroups:
    """Class for getting all the failover groups in commcell."""

    class FailoverGroupSourceTypes(Enum):
        BACKUP = 0
        REPLICATION = 1
        TEMPLATES = 2

    class FailoverGroupTypes(Enum):
        """ Enum to map Failover Group Types to integers"""
        LIVE_MOUNT = 1
        LIVE_SYNC = 2
        RESTORE = 4
        LIVE_RECOVERY = 8
        FAILOVER = 16
        VIRTUAL_LAB = 32
        ORACLE_EBS_APP = 64
        GENERIC_ENTERPRISE_APP = 128
        TEST_FAILOVER = 256

    class DRReplicationTypes(Enum):
        """ Enum to map replication types to replication groups/failover groups"""
        LIVE_SYNC = 0
        LIVE_SYNC_DIRECT = 1
        LIVE_SYNC_IO = 2
        SNAP_ARRAY = 3

    def __init__(self, commcell_object):
        """Initialize object of the Failover groups
            Args:
                commcell_object (Commcell)  --  instance of the Commcell class
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services

        self._failover_groups = None

        self.refresh()

    def __str__(self):
        """Representation string consisting of all failover groups in a formatted output
            Returns:
                str - string of all the failover groups
        """
        representation_string = (f'{"S. No.":^5}\t'
                                 f'{"Failover Group Id":^20}\t'
                                 f'{"Failover Group":^20}\n\n')

        for index, failover_group in enumerate(self._failover_groups):
            sub_str = (f'{index + 1:^5}\t'
                       f'{self._failover_groups[failover_group]:20}\t'
                       f'{failover_group:20}\n')
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the FailoverGroups class."""
        return f"Failover Groups for Commserv: '{self._commcell_object.commserv_name}'"

    def has_failover_group(self, failover_group_name):
        """Checks if failover group exists or not

            Args:
                failover_group_name (str)  --  name of the failover group

            Returns:
                bool - boolean output whether failover group exists or not

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(failover_group_name, str):
            raise SDKException('FailoverGroup', '101')

        return self.failover_groups and failover_group_name.lower() in self.failover_groups

    def get(self, failover_group_name):
        """Returns a failover group object of the specified failover group name.

            Args:
                failover_group_name (str)  --  name of the failover group

            Returns:
                object - instance of the FailoverGroup class for the given failover group name

            Raises:
                SDKException:
                    if proper inputs are not provided
                    If Failover group doesnt exists with given name
        """
        if not isinstance(failover_group_name, str):
            raise SDKException('FailoverGroup', '101')
        failover_group_name = failover_group_name.lower()
        if not self.has_failover_group(failover_group_name):
            raise SDKException('FailoverGroup', '103')
        return FailoverGroup(self._commcell_object, failover_group_name)

    @property
    def failover_groups(self):
        """ return all failover groups
        Args:

        Returns: (dict) All the failover groups in the commcell
                eg:
                {
                     "failover_group_name1": {id: '1', 'type': VSA_PERIODIC, 'operation_type': FAILOVER},
                     "failover_group_name2": {id: '2', 'type': VSA_CONTINUOUS, 'operation_type': FAILOVER}
                }
        Raises:
        """
        return self._failover_groups

    def _get_failover_groups(self):
        """REST API call for all the failover groups in the commcell.
            Args:

            Returns:
                dict - consists of all failover groups
                    {
                        "failover_group_name1": {
                            'id': '1',
                            'type': LIVE_SYNC,
                            'operation_type': FAILOVER,
                            'source_type': REPLICATION
                        },
                        "failover_group_name2": {
                            'id': '2',
                            'type': SNAP_ARRAY,
                            'operation_type': TEST_FAILOVER
                            'source_type': REPLICATION
                        }
                    }

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        failover_groups = {}

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._services['FAILOVER_GROUPS'])
        if flag:
            if 'vApp' in response.json():
                for failover_group in response.json().get('vApp', []):
                    failover_group_id = str(failover_group.get('vAppEntity', {}).get('vAppId'))
                    failover_group_name = failover_group.get('vAppEntity', {}).get('vAppName', '').lower()
                    operation_type = self.FailoverGroupTypes(int(failover_group.get('operationType', 16)))
                    replication_type = self.DRReplicationTypes(int(failover_group.get('replicationType', 0)))
                    source_type = self.FailoverGroupSourceTypes(int(failover_group.get('source', 1)))
                    failover_groups[failover_group_name] = {
                        'id': failover_group_id,
                        'operation_type': operation_type,
                        'type': replication_type,
                        'source_type': source_type
                    }
                return failover_groups
            raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self):
        """ Refresh the failover groups created in the commcell.
        Args:

        Returns:

        Raises:

        """
        self._failover_groups = self._get_failover_groups()


class FailoverGroup:
    """ Class for representing a failover group """

    def __init__(self, commcell_object, failover_group_name):
        """Initialise the FailoverGroup object for the given group name
            Args:
                commcell_object (Commcell)      --  instance of the Commcell class
                failover_group_name (str)       --  name of the failover group
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._failover_group_properties = None

        self._failover_group_name = failover_group_name.lower()
        self._failover_group_dict = self._get_failover_group_dict()

        self._source_client = None
        self._destination_client = None
        self._destination_agent = None
        self._source_instance = None
        self._destination_instance = None

        self._replication_pairs = None

        self.refresh()

    def __repr__(self):
        """String representation of the instance of the failover group"""
        return f'FailoverGroup class instance for {self._failover_group_name}'

    def __str__(self):
        """Strings showing all VM pairs of the failover group in a formatted output
            Returns:
                str - string of all VM pairs
        """
        representation_string = f'{"Pair Id":^5}\t{"Source VM":^20}\t{"Destination VM":^20}\n\n'

        for source_vm in self.vm_pairs:
            sub_str = (f'{self.vm_pairs[source_vm].vm_pair_id:^5}\t'
                       f'{source_vm:20}\t'
                       f'{self.vm_pairs[source_vm].destination_vm:20}'
                       f'\n')
            representation_string += sub_str

        return representation_string.strip()

    def _get_failover_group_dict(self):
        """Get the failover group's basic information from FailoverGroups object for Commcell"""
        fgs_obj = FailoverGroups(self._commcell_object)
        return fgs_obj.failover_groups.get(self._failover_group_name)

    def _get_failover_group_properties(self):
        """ Gets failover group properties
            Args:

            Returns: Gets the failover group properties dict

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._services['GET_FAILOVER_GROUP'] % str(self.failover_group_id))
        if flag:
            if 'vApp' in response.json():
                return response.json().get('vApp', [{}])[0]
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self):
        """ Refresh the failover group properties """
        self._failover_group_properties = self._get_failover_group_properties()
        self.replication_pairs.refresh()

    @property
    def failover_group_id(self):
        """Returns: (str) The ID of the failover group"""
        return self._failover_group_dict.get('id')

    @property
    def failover_group_name(self):
        """Returns: (str) The name of the failover group"""
        return self._failover_group_name

    @property
    def replication_type(self):
        """Returns: (DRReplicationTypes) The type of replication"""
        return self._failover_group_dict.get('type')

    @property
    def group_type(self):
        """Returns: (FailoverGroupTypes) The type of failover group"""
        return self._failover_group_dict.get('operation_type')

    @property
    def source_type(self):
        """Returns: (FailoverGroupSourceTypes) The type of failover group's source"""
        return self._failover_group_dict.get('source_type')

    @property
    def is_client_group(self):
        """Returns: (bool) Whether this failover group has a client group or not"""
        return self._failover_group_properties.get('isClientGroup')

    @property
    def replication_pairs(self):
        """
        Returns: (ReplicationPairs) Returns the ReplicationPairs object that belongs to this failover group
        Note: Implemented only for live sync failover groups
        """
        if not self._replication_pairs:
            if self.replication_type == FailoverGroups.DRReplicationTypes.LIVE_SYNC:
                self._replication_pairs = ReplicationPairs(self._commcell_object,
                                                           failover_group_id=self.failover_group_id)
        return self._replication_pairs

    @property
    def vm_pair_ids(self):
        """Returns: (List[str]) Returns the VM pair IDs that belong to this failover group"""
        return list(self.replication_pairs.replication_pairs)

    @property
    def vm_pairs(self):
        """
        Returns: (dict) The list of all live sync VM pairs
            eg:
                {
                    <source_vm1>: <Replication_pair_obj1>,
                    <source_vm2>: <Replication_pair_obj2>
                }
        """
        replication_pair_objects = {}
        for replication_pair_id, replication_pair_dict in self.replication_pairs.replication_pairs.items():
            source_vm_name = replication_pair_dict.get('source_vm')
            replication_pair_object = self.replication_pairs.get(replication_id=replication_pair_id)
            replication_pair_objects[source_vm_name] = replication_pair_object
        return replication_pair_objects

    @property
    def replication_groups(self):
        """Returns: (list) The list of all replication group names"""
        group_names = {vm_pair.replication_group_name for vm_pair in self.vm_pairs.values()}
        return list(group_names)

    @property
    def source_client(self):
        """Returns: (Client) The client object for the failover group's source hypervisor"""
        if not self._source_client:
            client_name = self._failover_group_properties.get('selectedEntities', [{}])[0].get('entityName', '')
            self._source_client = self._commcell_object.clients.get(client_name)
        return self._source_client

    @property
    def source_agent(self):
        """Returns: (Agent) The agent object for the source hypervisor"""
        return self.source_instance._agent_object

    @property
    def source_instance(self):
        """Returns: (Instance) The instance object for the source hypervisor"""
        if not self._source_instance:
            instance_id = self._failover_group_properties.get('selectedEntities', [{}])[0].get('instanceId', '')
            for agent_name in self.source_client.agents.all_agents:
                agent_object = self.source_client.agents.get(agent_name)
                for instance_name, inst_id in agent_object.instances.all_instances.items():
                    if inst_id == str(instance_id):
                        self._source_instance = agent_object.instances.get(instance_name)
                        return self._source_instance

        return self._source_instance

    @property
    def destination_client(self):
        """Returns: (Client) The client object for the failover group's destination hypervisor"""
        return self.destination_agent._client_object

    @property
    def destination_agent(self):
        """Returns: (Agent) The agent object for the destination hypervisor"""
        return self.destination_instance._agent_object

    @property
    def destination_instance(self):
        """Returns: (Instance) The instance object for the destination hypervisor"""
        if not self._destination_client:
            vm_pair = list(self.vm_pairs.values())[0]
            self._destination_instance = (vm_pair._subclient_object
                                          ._backupset_object._instance_object)
        return self._destination_instance

    @property
    def is_approval_required(self):
        """Returns bool:
            true : if approval set in failover group
            false: if approval not set in failover group
        """
        return self._failover_group_properties.get('approvalRequired')

    @property
    def user_for_approval(self):
        """Returns: user name set in failover group"""
        user_name = (self._failover_group_properties.get('usersForApproval', [{}])[0]
                     .get('userEntity', {}).get('userName', ''))
        return user_name
