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

"""Main file for performing replication group specific operations.

ReplicationGroups and ReplicationGroup are 2 classes defined in this file.

ReplicationGroups:     Class for representing all the replication groups associated
                        with a specific client

ReplicationGroup:      Class for a single replication group selected for a client,
                        and to perform operations on that replication group


ReplicationGroups:
    ReplicationGroupType                        --  Enum to denote all possible types of replication groups
    __init__(commcell_object)                   --  Initialise object of ReplicationGroups class

    __str__()                                   --  Returns all the replication groups

    __repr__()                                  --  Returns the string for the instance of the
                                                    ReplicationGroups class

    has_replication_group(
            replication_group_name)             --  Checks if replication group exists with the given name

    get(replication_group_name)                 --  Returns the ReplicationGroup class object of the input
                                                    replication name

    delete(replication_group_name)              --  Delete replication group with replication group name

    refresh()                                   --  Refresh all replication groups created on the commcell

    #### internal methods ###
    _get_replication_groups()                   --  REST API call to get all replication groups
                                                    in the commcell

    ##### properties ######
    replication_groups()                        --  Returns all replication groups in the commcell


ReplicationGroup:
    __init__(commcell_object,
            replication_group_name)                 -- Initialise object of ReplicationGroup with the
                                                        specified replication group name

    __repr__()                                      -- return the ReplicationGroup name

    refresh()                                       -- Refresh the object properties

    ##### internal methods #####
    _get_replication_group_dict()                   -- Method to get replication group dictionary

    _get_replication_group_properties()             -- Get the replication group properties

    ##### properties #####
    group_name()                                    -- Returns the replication group name
    group_id()                                      -- Returns the replication group ID
    task_id()                                       -- Returns the ID of the task associated to replication group
    replication_type()                              -- Returns the enum constant of the ReplicationGroupType
    zeal_group()                                    -- Returns a boolean to denote whether group is Zeal
                                                        or backup-based

    restore_options()                               -- Returns a hypervisor specific set of restore options

    is_dvdf_enabled()                               -- Returns whether 'Deploy VM during failover' enabled
    is_warm_sync_enabled()                          -- Returns whether 'Warm site recovery' is enabled

    source_client()                                 -- Returns a client object of the source hypervisor
    destination_client()                            -- Returns a client object of the destination hypervisor

    source_agent()                                  -- Returns an agent object of the source client
    destination_agent()                             -- Returns an agent object of the destination client

    source_instance()                               -- Returns an instance object of the source agent
    destination_instance()                          -- Returns an instance object of the destination agent

    subclient()                                     -- Returns the subclient object of the VM group associated
                                                        with the replication group

    live_sync_pairs()                               -- Returns the list of source VM names that are already present in
                                                        replication monitor
    vm_pairs()                                      -- Returns a dictionary of source VM names
                                                        and LiveSyncVMPairs object mapping

    is_enabled()                                    -- Returns a boolean to tell whether replication group
                                                        is enabled or disabled
    group_frequency()                               -- Returns the group frequency in minutes

    copy_precedence_applicable                      -- Returns a boolean whether the copy precedence is applicable or
                                                        not

    copy_for_replication()                          -- Returns the copy precedence ID used for replication

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from enum import Enum

from cvpysdk.drorchestration.blr_pairs import BLRPairs
from past.builtins import basestring
from ..exception import SDKException


class ReplicationGroups:
    """Class for getting all the replication groups in commcell."""

    class ReplicationGroupType(Enum):
        """ Enum to map Replication Group Types to integers"""
        VSA_PERIODIC = 1
        VSA_CONTINUOUS = 2
        FILE_SYSTEM = 3
        ORACLE = 4
        SQL_SERVER = 5
        SAP_HANA = 6

    def __init__(self, commcell_object):
        """Initialize object of the Replication groups
            Args:
                commcell_object (Commcell)  --  instance of the Commcell class
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services

        self._replication_groups = None

        self.refresh()

    def __str__(self):
        """Representation string consisting of all replication groups in a formatted output
            Returns:
                str - string of all the replication groups
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Replication Group Id', 'Replication Group')

        for index, replication_group in enumerate(self._replication_groups):
            sub_str = '{:^5}\t{:20}\t{:20}\n'.format(
                index + 1,
                self._replication_groups[replication_group],
                replication_group
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the ReplicationGroups class."""
        return "Replication Groups for Commserv: '{0}'".format(
            self._commcell_object.commserv_name)

    def has_replication_group(self, replication_group_name):
        """Checks if replication group exists or not

            Args:
                replication_group_name (str)  --  name of the replication group

            Returns:
                bool - boolean output whether replication group exists or not

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(replication_group_name, basestring):
            raise SDKException('ReplicationGroup', '101')

        return self.replication_groups and replication_group_name.lower() in self.replication_groups

    def get(self, replication_group_name):
        """Returns a replication group object of the specified replication group name.

            Args:
                replication_group_name (str)  --  name of the replication group

            Returns:
                object - instance of the ReplicationGroup class for the given replication group name

            Raises:
                SDKException:
                    if proper inputs are not provided
                    If Replication group doesnt exists with given name
        """
        if not isinstance(replication_group_name, basestring):
            raise SDKException('ReplicationGroup', '101')
        replication_group_name = replication_group_name.lower()
        if self.has_replication_group(replication_group_name):
            return ReplicationGroup(
                self._commcell_object, replication_group_name)

        raise SDKException(
            'ReplicationGroup',
            '102',
            "Replication group doesn't exist with name: {0}".format(replication_group_name))

    def delete(self, replication_group_name):
        """ Deletes the specified replication group name.

            Args:
                replication_group_name (str)  --  name of the replication group

            Returns:


            Raises:
                SDKException:
                    if proper inputs are not provided
                    if response is empty
                    if response is not success
        """

        if not isinstance(replication_group_name, basestring):
            raise SDKException('ReplicationGroup', '101')

        replication_group_name = replication_group_name.lower()
        if self.has_replication_group(replication_group_name):

            replication_group_dict = self.replication_groups.get(
                replication_group_name.lower(), {})

            if replication_group_dict:
                if replication_group_dict.get('zealGroup'):
                    payload = {
                        "repGrpIds": [int(replication_group_dict.get('id'))],
                        "taskIds": [],
                    }
                else:
                    payload = {
                        "repGrpIds": [],
                        "taskIds": [replication_group_dict.get('id')],
                    }

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    method='POST',
                    url=self._services['DELETE_REPLICATION_GROUPS'],
                    payload=payload
                )

                if flag:
                    if response.json() and 'deleteGroupsResponse' in response.json():
                        if (response.json().get('deleteGroupsResponse', [{}])[0]
                                .get('response').get('errorMessage')):
                            error_message = (response.json().get('deleteGroupsResponse', {})
                                             .get('response', {}).get('errorMessage'))
                            o_str = ('Failed to delete replication group: {0} \nError: "{1}"'
                                     .format(replication_group_name, error_message))

                            raise SDKException('ReplicationGroup', '102', o_str)
                        self.refresh()

                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(
                        response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException('ReplicationGroup', '101', 'Replication group information is empty')
        else:
            raise SDKException(
                'ReplicationGroup', '102', 'No replication group exists with name: "{0}"'.format(
                    replication_group_name)
            )

    @property
    def replication_groups(self):
        """ return all replication groups
        Args:

        Returns: All the replication groups in the commcell

        Raises:
        """
        return self._replication_groups

    def _get_replication_groups(self):
        """REST API call for all the replication groups in the commcell.
            Args:

            Returns:
                dict - consists of all replication groups
                    {
                         "replication_group_name1": {id: '1', 'type': VSA_PERIODIC, 'zealGroup': true},
                         "replication_group_name2": {id: '2', 'type': VSA_CONTINUOUS, 'zealGroup': false}
                    }

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._services['REPLICATION_GROUPS'])

        if flag:
            if response.json() and 'replicationGroups' in response.json():

                replication_groups = {}

                for group_dict in response.json()['replicationGroups']:
                    group_type = (self.ReplicationGroupType(group_dict.get('type'))
                                  if group_dict.get('type') else None)
                    if group_dict.get('replicationGroup', {}).get('replicationGroupId'):
                        group_name = group_dict.get('replicationGroup', {}).get('replicationGroupName', '')
                        group_id = str(group_dict.get('replicationGroup', {}).get('replicationGroupId', 0))
                        zeal_group = True
                    else:
                        subtask_dict = group_dict.get('taskDetail', {}).get('subTasks')[0]
                        group_name = subtask_dict.get('subTask', {}).get('subTaskName', '')
                        group_id = str(group_dict.get('taskDetail', {}).get('task', {}).get('taskId', 0))
                        zeal_group = False
                    replication_groups[group_name.lower()] = {
                        'id': group_id,
                        'type': group_type,
                        'zealGroup': zeal_group,
                    }
                return replication_groups
            raise SDKException('Response', 102)

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self):
        """ Refresh the replication groups created in the commcell.
        Args:

        Returns:

        Raises:

        """
        self._replication_groups = self._get_replication_groups()


class ReplicationGroup:
    """Class for all Replication groups related SDK"""

    def __init__(self, commcell_object, replication_group_name):
        """Initialise the ReplicationGroup object for the given group name
            Args:
                commcell_object (Commcell)      --  instance of the Commcell class
                replication_group_name (str)    --  name of the replication group
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._replication_group_properties = None

        self._group_name = replication_group_name.lower()
        self._group_dict = self._get_replication_group_dict()

        self._source_client = None
        self._destination_client = None
        self._source_agent = None
        self._destination_agent = None
        self._source_instance = None
        self._destination_instance = None

        self._subclient = None
        self._vm_pairs = None

        self.refresh()

    def __repr__(self):
        """String representation of the instance of the replication group"""
        representation_string = f'ReplicationGroup class instance for ' \
                                f'{"Zeal" if self.zeal_group else "Backup based"}' \
                                f' replication group: "{self.group_name}"'
        return representation_string.format(self.group_name)

    def __str__(self):
        """Strings showing all VM pairs of the replication group in a formatted output
            Returns:
                str - string of all VM pairs
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\n\n'.format('Pair Id', 'Source VM', 'Destination VM')

        for source_vm in self.vm_pairs:
            sub_str = '{:^5}\t{:20}\t{:20}\n'.format(
                self.vm_pairs[source_vm].vm_pair_id,
                source_vm,
                self.vm_pairs[source_vm].destination_vm
            )
            representation_string += sub_str

        return representation_string.strip()

    def _get_replication_group_dict(self):
        """ Gets replication group dict from the ReplicationGroups class
            Returns: (list) The list of replication groups dictionary objects
        """
        rgs_obj = ReplicationGroups(self._commcell_object)
        return rgs_obj.replication_groups.get(self._group_name)

    def _get_replication_group_properties(self):
        """ Gets replication group properties
            Args:

            Returns: Gets the replication group properties dict

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        if self.zeal_group:
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'GET', self._services['REPLICATION_GROUP_DETAILS'] % self.group_id)
        else:
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'GET', self._services['LIVE_SYNC_DETAILS'] % self.group_id)

        if flag:
            if response.json().get('replicationInfo', {}).get('replicationTargets', {}).get('taskInfo'):
                return response.json().get('replicationInfo', {}).get('replicationTargets', {}).get('taskInfo')[0]
            if response.json().get('taskInfo'):
                return response.json().get('taskInfo')
            if self.replication_type == ReplicationGroups.ReplicationGroupType.VSA_CONTINUOUS:
                return response.json().get('replicationGroupDetails', {}).get('taskDetail')
            raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self):
        """ Refresh the replication group properties """
        self._replication_group_properties = self._get_replication_group_properties()
        self._vm_pairs = None

    @property
    def group_name(self):
        """Returns: (str) Returns the name of the replication group"""
        return self._group_name

    @property
    def group_id(self):
        """Returns: (str) Returns the ID of the replication group (Zeal)/subtask(classic)"""
        return str(self._group_dict.get('id'))

    @property
    def task_id(self):
        """Returns: (str) Returns the ID of the task associated to the replication group"""
        return str(self._replication_group_properties.get('task', {}).get('taskId'))

    @property
    def replication_type(self):
        """
        Returns: (enum) Returns the type of the replication group.
        """
        return self._group_dict.get('type')

    @property
    def zeal_group(self):
        """Returns: (bool) True, if zeal replication group, false otherwise"""
        return self._group_dict.get('zealGroup', False)

    @property
    def restore_options(self):
        """
        Returns: (dict) The dictionary of restore options of the replication group
            The dictionary structure depends on the vendor
        """
        return (self._replication_group_properties.get('subTasks', [{}])[0]
                .get('options', {}).get('restoreOptions', {}))

    @property
    def is_dvdf_enabled(self):
        """Returns: (bool) Whether deploy VM during failover is enabled or not"""
        return (self.restore_options.get('virtualServerRstOption', {})
                .get('diskLevelVMRestoreOption', {}).get('deployVmWhenFailover', False))

    @property
    def is_warm_sync_enabled(self):
        """Returns: (bool) Whether Warm sync is enabled or not"""
        return (self.restore_options.get('virtualServerRstOption', {})
                .get('diskLevelVMRestoreOption', {}).get('createVmsDuringFailover', False))

    @property
    def source_client(self):
        """Returns:  the client object of the source hypervisor"""
        if not self._source_client:
            client_name = self._replication_group_properties.get('associations', [{}])[0].get('clientName')
            self._source_client = self._commcell_object.clients.get(client_name)
        return self._source_client

    @property
    def destination_client(self):
        """Returns: (str) the client object for the destination hypervisor"""
        if not self._destination_client:
            client_name = (self.restore_options.get('virtualServerRstOption', {})
                           .get('vCenterInstance', {}).get('clientName'))
            self._destination_client = self._commcell_object.clients.get(client_name)
        return self._destination_client

    @property
    def source_agent(self):
        """Returns: the agent object of the source hypervisor"""
        if not self._source_agent:
            agent_name = self._replication_group_properties.get('associations', [{}])[0].get('appName')
            self._source_agent = self.source_client.agents.get(agent_name)
        return self._source_agent

    @property
    def destination_agent(self):
        """Returns: the agent object of the destination hypervisor"""
        if not self._destination_agent:
            agent_name = self._replication_group_properties.get('associations', [{}])[0].get('appName')
            self._destination_agent = self.destination_client.agents.get(agent_name)
        return self._destination_agent

    @property
    def source_instance(self):
        """Returns: (str) The source hypervisor's instance name"""
        if not self._source_instance:
            instance_name = self._replication_group_properties.get('associations', [{}])[0].get('instanceName')
            self._source_instance = self.source_agent.instances.get(instance_name)
        return self._source_instance

    @property
    def destination_instance(self):
        """Returns: (str) The destination hypervisor's instance name"""
        if not self._destination_instance:
            instance_name = (self.restore_options.get('virtualServerRstOption', {})
                             .get('vCenterInstance', {}).get('instanceName'))
            
            # TODO : Depends on DR Layer changes : Workaround used
            instance_name = 'Amazon Web Services' if instance_name == 'Amazon' else instance_name
            
            self._destination_instance = self.destination_agent.instances.get(instance_name)
        return self._destination_instance

    @property
    def subclient(self):
        """Returns: the subclient object of the replication group"""
        if not self._subclient:
            backupset_name = self._replication_group_properties.get('associations', [{}])[0].get('backupsetName')
            backupset = self.source_instance.backupsets.get(backupset_name)
            subclient_name = self._replication_group_properties.get('associations', [{}])[0].get('subclientName')
            self._subclient = backupset.subclients.get(subclient_name)
        return self._subclient

    @property
    def live_sync_pairs(self):
        """
        Returns: A list of all source VM names for which live sync pair exists for a periodic replication group
            eg: ["vm1", "vm2"]
        """
        _live_sync_pairs = []
        if self.replication_type == ReplicationGroups.ReplicationGroupType.VSA_PERIODIC:
            live_sync_name = self.group_name.replace('_ReplicationPlan__ReplicationGroup', '')
            live_sync = self.subclient.live_sync.get(live_sync_name)
            _live_sync_pairs = list(live_sync.vm_pairs)
        elif self.replication_type == ReplicationGroups.ReplicationGroupType.VSA_CONTINUOUS:
            blr_pairs = BLRPairs(self._commcell_object, self.group_name)
            _live_sync_pairs = list(blr_pairs.blr_pairs)
        else:
            raise SDKException('ReplicationGroup', '101', 'Implemented only for replication groups'
                                                          ' of virtual server periodic')
        return _live_sync_pairs

    @property
    def vm_pairs(self):
        """Returns: A dictionary of livesyncVM pairs/BLR pairs object
            eg: {"src_vm1": LiveSyncVMPair, "src_vm2": LiveSyncVMPair}
        """
        if not self._vm_pairs:
            if self.replication_type == ReplicationGroups.ReplicationGroupType.VSA_PERIODIC:
                live_sync_name = self.group_name.replace('_ReplicationPlan__ReplicationGroup', '')
                live_sync = self.subclient.live_sync.get(live_sync_name)
                self._vm_pairs = {source_vm: live_sync.get(source_vm)
                                  for source_vm in live_sync.vm_pairs}
            elif self.replication_type == ReplicationGroups.ReplicationGroupType.VSA_CONTINUOUS:
                blr_pairs = BLRPairs(self._commcell_object, self.group_name)
                self._vm_pairs = {pair_dict.get('sourceName'):
                                  blr_pairs.get(pair_dict.get('sourceName'), pair_dict.get('destinationName'))
                                  for pair_dict in blr_pairs.blr_pairs.values()}
            else:
                raise SDKException('ReplicationGroup', '101', 'Implemented only for replication groups'
                                                              ' of virtual server periodic')
        return self._vm_pairs

    @property
    def is_enabled(self):
        """Returns: (bool) Returns True if state of the replication group 'Enabled' else False"""
        return not self._replication_group_properties.get('task', {}).get('taskFlags', {}).get('disabled', False)

    @property
    def group_frequency(self):
        """Returns: (int) The frequency in minutes at which the group is synced (only applicable for Zeal groups)"""
        return self._replication_group_properties.get('pattern', {}).get('freq_interval', 0)

    @property
    def copy_precedence_applicable(self):
        """Returns: (bool) Whether the copy precedence is applicable or not"""
        return (self.restore_options.get('browseOption', {}).get('mediaOption', {})
                .get('copyPrecedence', {}).get('copyPrecedenceApplicable', False))

    @property
    def copy_for_replication(self):
        """Returns: (int) The ID of the copy used for the replication"""
        # Copy for replication is only applicable is group has copy precedence enabled
        return (self.restore_options.get('browseOption', {}).get('mediaOption', {})
                .get('copyPrecedence', {}).get('copyPrecedence'))

    @property
    def recovery_target(self):
        """Returns: (str) The recovery target used for the replication"""
        return (self.restore_options.get('virtualServerRstOption', {}).get('allocationPolicy', {})
                .get('vmAllocPolicyName'))
