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

"""Main file for performing BLR pair specific operations.

BLRPairs and BLRPair are classes defined in this file.

BLRPairs:       Class for representing all the BLR pairs

        PairStatus:     Enum for all possible pair status

        EndPointTypes:  Enum for all allowed end points for BLR pairs

        PendingStatus:  Enum for all pending status codes

        RecoveryType:   Enum of all possible recovery point types

        DROperations:   Enum of DR Operations that can be applied on the BLR pair

BLRPair:        Class for a single BLR Pair


BLRPairs:
    __init__(commcell_object)                   --  Initialise object of BLRPairs class

    __repr__()                                  --  Returns the string for the instance of the
                                                    BLRPairs class

    blr_pairs()                                 --  Returns a dictionary of BLR pair names mapping with their IDs

    has_blr_pair(
            source_name, destination_name)      --  Checks if BLR pair exists with the given source and
                                                    destination client name

    create_fsblr_pair(source_client_id,         --  Creates FSBLR replication pair for given set of options
            destination_client_id,
            source_volumes,
            destination_volumes,
            recovery_type,
            **kwargs)

    get(source_name, destination_name)          --  Returns the BLRPair class object for the source and
                                                    destination client name

    delete(source_name, destination_name)       --  Delete BLR pair with the source and
                                                    destination client name

    refresh()                                   --  Refresh all BLR pairs created on the commcell

    get_rpstore_id(rpstore_name)                --  Get the RPStore ID for the given name

    get_rpstore_mountpath(rpstore_name)         --  Get the RPstore mounth path for the given name

    #### internal methods ###
    _update_data()                              -- REST API call to get all BLR pairs in the commcell

BLRPair:
    __init__(commcell_object, pair_name)    --  Initialise object of BLRPair class for pair name

    __repr__()                                  --  Returns the string for the instance of the
                                                    BLRPair class

    pair_properties                             --  Returns the properties of the pair

    pair_status                                 --  Returns the status of the pair

    source                                      --  Returns the dictionary for all source client properties

    destination                                 --  Returns the dictionary for all destination client properties

    lag_time                                    --  Returns the replication lag time in minutes

    replication_group_name                      -- (VSABLR) Returns the replication group name of the pair

    pending_status                              --  Returns the reason for replication lag

    pair_flag                                   --  Returns the integer for the pair's flag

    subclient_props                             --  Returns the properties of the subclient associated with the pair

    pair_recovery_type                          --  Returns the enum for recovery type of the pair

    pair_rpstore_intervals                      --  Returns the RPStore interval options set for the pair

    pair_volume_map                             --  (FSBLR) Returns the mapping of volumes for FSBLR pairs

    pair_latest_stats                           --  Returns the pair's latest data stats

    get_pair_stats()                            --  Returns the pair's data stats

    get_recovery_point_stores()                 --  Returns the RPstore points for the pair

    create_replica_copy()                       --  Creates a replica copy task and return the job/task ID

    refresh()                                   --  Refresh the BLR pair properties

    #### internal methods ###
    _get_pair_id()                              --  Returns the BLR pair ID from the BLR pairs dictionary

    _get_pair_properties()                      --  Returns the BLR pair properties
"""
import time

from cvpysdk.job import Job
from cvpysdk.schedules import Schedules

from ..exception import SDKException
from enum import Enum
import xmltodict


class BLRPairs:
    """Class for getting all BLR pairs in commcell."""

    class PairStatus(Enum):
        NOT_SYNCED = 0
        BACKING_UP = 1
        RESTORING = 2
        RESYNCING = 3
        REPLICATING = 4
        SUSPENDED = 5
        STOPPED = 6
        VERIFYING = 7
        PROBLEM = 8
        FAILED = 9
        STARTING = 10
        STOPPING = 11
        SUSPENDING = 12
        RESUMING = 13
        FAILING_OVER = 14
        FAILOVER_FAILED = 15
        FAILOVER_DONE = 16
        FAILING_BACK = 17
        FAILBACK_FAILED = 18
        SWITCHING_ROLES = 19
        SWITCH_ROLES_FAILED = 20

    class EndPointTypes(Enum):
        VIRTUALIZATION = 1
        FILESYSTEM = 2
        DATABASE = 3

    class AgentTypes(Enum):
        VIRTUALIZATION = 'Virtual Server'
        FILESYSTEM = 'File system'
        DATABASE = 'Database'

    class PendingStatus(Enum):
        NOLAG = 0

    class RecoveryType(Enum):
        LIVE = 1
        SNAPSHOT = 2
        GRANULAR = 3
        GRANULARV2 = 4

    class DROperations(Enum):
        TEST_BOOT = 1,
        VSA_FAIL_OVER = 2
        DELETE = 3
        PERMANENT_BOOT = 4
        TEST_BOOT_EXTEND = 5
        MANAGE_TEST_BOOT = 6
        TEST_FS_MOUNT = 7
        PERM_FS_MOUNT = 8
        TEST_FSMOUNT_EXTEND = 9
        MANAGE_TEST_MOUNT = 10
        VSA_FAIL_BACK = 11
        FS_FAIL_OVER = 12
        FS_FAIL_BACK = 13
        RESUME_VSA_FAILOVER = 14
        CANCEL_VSA_FAILOVER = 15
        RESUME_FS_FAILOVER = 16
        CANCEL_FS_FAILOVER = 17
        ABORT_VSA_FAILBACK = 18
        ABORT_FS_FAILBACK = 19

    def __init__(self, commcell_object, replication_group_name: str = ''):
        """Initialize object of the BLR Pairs
            Args:
                commcell_object (Commcell)  --  instance of the Commcell class
                replication_group_name (str)--  Name of the replication group (only for VSA BLR)
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services
        self._replication_group_name = replication_group_name.lower()
        self._replication_group_id = None
        if self._replication_group_name:
            self._replication_group_id = self._get_replication_group_id()

        self._LIST_BLR_PAIRS = self._services['GET_BLR_PAIRS']

        self._DELETE_BLR = self._services['DELETE_BLR_PAIR']
        self._QEXEC = self._services['EXEC_QCOMMAND']

        self._site_info = None
        self._summary = None
        self._rpstore_list = None

        self.refresh()

    def __repr__(self):
        """Representation string for the instance of the BLR Pairs class."""
        if not self._replication_group_name:
            return "BLR Pairs for Commserv: '{0}'".format(self._commcell_object.commserv_name)
        else:
            return "BLR Pairs for Replication group: '{0}'".format(self._replication_group_name)

    def _get_replication_group_id(self):
        """Returns the replication group ID
            Args:
            Returns:
                replication_group_id (str):  The ID of the associated replication group
            Raises:
        """
        if not self._replication_group_name:
            return ''
        return (self._commcell_object.replication_groups.replication_groups
                .get(self._replication_group_name, {}).get('id'))

    def _update_data(self):
        """REST API call for getting all the info for all pairs in the commcell.
            Args:
            Returns:
            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._LIST_BLR_PAIRS)
        if flag:
            if response.json():
                self._summary = response.json().get('summary', {})
                if self._replication_group_id:
                    self._site_info = [site_info for site_info in response.json().get('siteInfo', [])
                                       if str(site_info.get('replicationGroup', {}).get('replicationGroupId', 0))
                                       == self._replication_group_id]
                else:
                    self._site_info = response.json().get('siteInfo', [])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _update_rpstorelist(self):
        """REST API call for getting all the rp store in the commcell.
            Args:
            Returns:
            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        response = self._commcell_object.qoperation_execute('<EVGui_GetLibraryListWCReq libraryType="RPSTORE" />')

        if response and 'libraryList' in response:
            self._rpstore_list = response.get('libraryList', [])
        else:
            raise SDKException('Response', '102')

    @property
    def blr_pairs(self):
        """REST API call for getting all the BLR pairs in the commcell.
            Args:

            Returns:
                dict - consists of all BLR pairs
                    {
                         "blr_id_1": {
                             "sourceName": "vm1",
                             "destinationName": "DRvm1",
                             "subclientName": "BLR_vm1(<guid>)"
                         },
                         "blr_id_2": {
                             "sourceName": "vm1",
                             "destinationName": "DRvm1",
                             "subclientName": "BLRSC_vm1_DRvm1_E:"
                         },
                    }
        """
        pairs = {}
        for pair_row in self._site_info:
            pair_id = pair_row.get('id')
            if pair_id:
                pairs[str(pair_id)] = {
                    'sourceName': pair_row.get('sourceName', ''),
                    'destinationName': pair_row.get('destinationName', ''),
                    'subclientName': pair_row.get('entity', {}).get('subclientName', '')
                }
        return pairs

    def has_blr_pair(self, source_name, destination_name):
        """Checks if BLR pair exists or not
            Args:
                source_name (str): Name of the source client
                destination_name (str): Name of the destination client
            Returns:
                bool - boolean output whether BLR pair exists or not

            Raises:
                SDKException:
                    if proper inputs are not provided
        """
        if not isinstance(source_name, str) or not isinstance(destination_name, str):
            raise SDKException('BLRPairs', '101')
        source_name = source_name.lower()
        destination_name = destination_name.lower()
        for _, pair_row in self.blr_pairs.items():
            if (source_name == pair_row.get('sourceName', '').lower() and
                    destination_name == pair_row.get('destinationName', '').lower()):
                return True
        else:
            return False

    def create_fsblr_pair(self,
                          source_client_id,
                          destination_client_id,
                          source_volumes,
                          destination_volumes,
                          recovery_type,
                          **kwargs):
        """Creates a new FSBLR pair on the commcell with the specified options
            Args:
                source_client_id (str)      : The source client's ID
                destination_client_id (str) : The destination client's ID
                source_volumes (list)       : The list of all source volumes
                destination_volumes (list)  : The list of all destination volumes
                recovery_type (RecoveryType): The enum to specify what type of recovery pair is supposed to be
                **kwargs (dict)             : Only used for granular type FSBLR pairs
                    rpstore_id (str)        : The ID of the RPstore to be used
                    rpstore_name (str)      : The name of the RPStore
                    ccrp_interval (int)     : The number of minutes after which CCRP is taken
                    acrp_interval (int)     : The number of minutes after which ACRP is taken
                    max_rp_interval (int)   : The number of minutes after which RP store's retention is ended
                    rp_merge_delay (int)    : Merge recovery points older than time in minutes
                    rp_retention (int)      : The number of minutes for which RPstore is retained for
                    rpstore_switch_live(int): The time in minutes after which pair is switch to
                                                live if RPstore is offline
                    merge_only_off_peak(bool):Whether to merge RPstore only during off-peak time
        """
        blr_options = {
            'BlockReplication_BLRRecoveryOptions':
                {
                    '@recoveryType': recovery_type.value,
                    'granularV2': {
                        '@ccrpInterval': kwargs.get('ccrp_interval', 300),
                        '@acrpInterval': kwargs.get('acrp_interval', 0),
                        '@maxRpInterval': kwargs.get('max_rp_interval', 21600),
                        '@rpMergeDelay': kwargs.get('rp_merge_delay', 172800),
                        '@rpRetention': kwargs.get('rp_retention', 604800),
                        '@maxRpStoreOfflineTime': kwargs.get('rpstore_switch_live', 0),
                        '@useOffPeakSchedule': int(kwargs.get('merge_only_off_peak', False)),
                    }},
        }
        if kwargs.get('rpstore_id') and kwargs.get('rpstore_name'):
            granularv2 = blr_options['BlockReplication_BLRRecoveryOptions']['granularV2']
            granularv2['@rpStoreId'] = int(kwargs.get('rpstore_id', 0))
            granularv2['@rpStoreName'] = kwargs.get('rpstore_name')
            blr_options['BlockReplication_BLRRecoveryOptions']['granularV2'] = granularv2

        source_client = self._commcell_object.clients.get(int(source_client_id))
        destination_client = self._commcell_object.clients.get(int(destination_client_id))
        source_client_volumes = source_client.get_mount_volumes(source_volumes)
        destination_client_volumes = destination_client.get_mount_volumes(destination_volumes)

        request_json = {
            "destEndPointType": self.EndPointTypes.FILESYSTEM.value,
            "blrRecoveryOpts": xmltodict.unparse(blr_options, short_empty_elements=True).replace('\n', ''),
            "srcEndPointType": self.EndPointTypes.FILESYSTEM.value,
            "srcDestVolumeMap": [],
            "destEntity": {
                "client": {
                    "clientId": int(destination_client_id),
                    "clientName": destination_client.client_name,
                    "hasDrivesInPair": True,
                    "tabLevel": "level-0",
                    "checked": True,
                }
            },
            "sourceEntity": {
                "client": {
                    "clientId": int(source_client_id),
                    "clientName": source_client.client_name,
                    "hasDrivesInPair": True,
                    "tabLevel": "level-0",
                    "checked": True,
                }
            }
        }
        for source, destination in zip(source_client_volumes, destination_client_volumes):
            request_json['srcDestVolumeMap'].append({
                "sourceVolumeGUID": source['guid'],
                "sourceVolume": source['accessPathList'][0],
                "destVolumeGUID": destination['guid'],
                "destVolume": destination['accessPathList'][0],
                "sourceVolumeSize": source['size'],
                "disabled": "",
            })

        flag, response = (self._commcell_object._cvpysdk_object
                          .make_request('POST', self._services['CREATE_BLR_PAIR'], request_json))

        if flag:
            if response and response.json():
                if response.json().get('errorCode', 0) != 0:
                    response_string = self._commcell_object._update_response_(
                        response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def get(self, source_name, destination_name):
        """Get pair name on the basis of source and destination name and return pair object
        Args:
            source_name (str): Name of the source client
            destination_name (str): Name of the destination client
        Returns: BLRPair object for source and destination

        Raises:
            SDKException:
                if proper inputs are not provided
        """
        if not isinstance(source_name, str) or not isinstance(destination_name, str):
            raise SDKException('BLRPairs', '101')
        source_name = source_name.lower()
        destination_name = destination_name.lower()
        for _, pair_row in self.blr_pairs.items():
            if (source_name == pair_row.get('sourceName', '').lower() and
                    destination_name == pair_row.get('destinationName', '').lower()):
                return BLRPair(self._commcell_object, source_name, destination_name)
        else:
            raise SDKException('BLRPairs', '102',
                               'No BLR pair exists with source: "{0}" and destination: "{1}"'
                               .format(source_name, destination_name))

    def delete(self, source_name, destination_name):
        """ Deletes the blr pair with source and destination names
        Args:
            source_name (str): Name of the source client
            destination_name (str): Name of the destination client
        Returns: BLRPair object for source and destination

        Raises:
            SDKException:
                if proper inputs are not provided
                if response is empty
                if response is not success
        """
        if not isinstance(source_name, str) or not isinstance(destination_name, str):
            raise SDKException('BLRPairs', '101')
        source_name = source_name.lower()
        destination_name = destination_name.lower()
        if self.has_blr_pair(source_name, destination_name):
            for pair_id, pair_row in self.blr_pairs.items():
                if (source_name == pair_row.get('sourceName', '').lower() and
                        destination_name == pair_row.get('destinationName', '').lower()):
                    flag, response = self._commcell_object._cvpysdk_object.make_request(
                        method='DELETE', url=self._DELETE_BLR % pair_id)
                    if flag:
                        if 'error' in response.json():
                            error_message = response.json(
                            )['error']['errorMessage']
                            o_str = 'Failed to delete Source: {0} and Destination: {1} \nError: "{2}"' \
                                .format(source_name, destination_name, error_message)

                            raise SDKException('Response', '101', o_str)
                        else:
                            self.refresh()
                    else:
                        raise SDKException('Response', '102')
                    break
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('BLRPairs', '102',
                               'No BLR pair exists with source: "{0}" and destination: "{1}"'
                               .format(source_name, destination_name))

    def refresh(self):
        """ Refresh the BLR pairs created in the commcell.
        Args:

        Returns:

        Raises:

        """
        self._update_data()
        self._update_rpstorelist()

    def get_rpstore_id(self, rpstore_name):
        """Gets the RPStore ID for the given name
            Args:
                rpstore_name (str)  : The name of the RP store
        """

        for rpstore in self._rpstore_list:
            if rpstore.get('library', {}).get('libraryName') == rpstore_name and rpstore.get('MountPathList', ''):
                return str(rpstore.get('MountPathList')[0]
                           .get('rpStoreLibraryInfo', {}).get('rpStoreId', ''))
        else:
            raise SDKException('BLRPairs', '103', f'No RP Store found with name {rpstore_name}')

    def get_rpstore_mountpath(self, rpstore_name):
        """Gets the RPStore mount path for the given name
            Args:
                rpstore_name (str)  : The name of the RP store
        """

        for rpstore in self._rpstore_list:
            if rpstore.get('library', {}).get('libraryName') == rpstore_name:
                mount_path = str(rpstore.get('MountPathList', {})[0]['mountPathName'])
                return mount_path.split()[1].strip()
        else:
            raise SDKException('BLRPairs', '103', f'No RP Store found with name {rpstore_name}')


class BLRPair:
    class PairOperationsStatus(Enum):
        SUSPEND = BLRPairs.PairStatus.SUSPENDED
        START = BLRPairs.PairStatus.REPLICATING
        RESUME = BLRPairs.PairStatus.REPLICATING
        STOP = BLRPairs.PairStatus.STOPPED
        RESYNC = BLRPairs.PairStatus.RESYNCING

    def __init__(self, commcell_object, source_name, destination_name):
        """Initialise the ReplicationGroup object for the given group name
            Args:
                commcell_object (Commcell)      --  instance of the Commcell class
                source_name (str)               --  Name of the source of BLR pair
                destination_name (str)          --  Name of the destination of BLR pair
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services

        self._source_name = source_name.lower()
        self._destination_name = destination_name.lower()
        self._pair_id = self._get_pair_id()
        self._pair_properties = None
        self._source_instance = None
        self._destination_instance = None

        self._GET_PAIR = self._services['GET_BLR_PAIR']
        self._PAIR_STATS = self._services['GET_BLR_PAIR_STATS']
        self._GRANULAR_RP_STORES = self._services['GRANULAR_BLR_POINTS']
        self._BOOT_DETAILS = self._services['BLR_BOOT_DETAILS']

        self.refresh()

    def __repr__(self):
        """String representation of the instance of the BLR pair"""
        representation_string = 'BLR pair class instance for pair: "{0} -> {1}"'
        return representation_string.format(self._source_name, self._destination_name)

    def __str__(self):
        """String representation of the instance of BLR pair"""
        return f'BLR Pair: {self._source_name} -> {self._destination_name}'

    def _get_pair_id(self):
        """ Gets BLR pair Id from the BLRPairs class"""
        for pair_id, blr_pair in self._commcell_object.blr_pairs.blr_pairs.items():
            if (blr_pair.get('sourceName').lower() == self._source_name and
                    blr_pair.get('destinationName').lower() == self._destination_name):
                return pair_id
        raise SDKException('BLRPairs', '102')

    def _get_pair_properties(self):
        """ Gets BLR pair properties
            Args:

            Returns: Gets the BLR pair properties dictionary

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._GET_PAIR % self._pair_id)
        if flag:
            if response.json() and 'siteInfo' in response.json():
                self._pair_properties = response.json().get('siteInfo')[0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _perform_action(self, operation_type):
        """Performs an action on BLR pair
            Args:
                operation_type (PairOperations): An enum of pair operations of BLRPair class
            Returns:

            Raises:
            SDKException:
            if response is empty
            if response is not success
        """
        status_to_be_set = operation_type.value
        site_info = [self._pair_properties.copy()]
        site_info[0]['status'] = status_to_be_set.value
        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT',
                                                                            self._services['GET_BLR_PAIRS'],
                                                                            {'siteInfo': site_info})
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', -1)
                if error_code != 0:
                    raise SDKException('Response', '101')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def pair_properties(self):
        """Returns a dictionary of the pair properties"""
        return self._pair_properties

    @property
    def pair_status(self):
        """Returns the status of the pair according the to PairStatus enum"""
        self.refresh()
        return BLRPairs.PairStatus(self._pair_properties.get('status'))

    @property
    def source(self):
        """Returns: (dict) The properties of the source client
        eg: {
            name: 'clientName',
            client_id: 'client id'
            proxy_client_id: 'head proxy_id',
            guid: 'client guid',
            endpoint: 'endpoint enum'
        }
        """
        return {
            "name": self.pair_properties.get('sourceName'),
            "client_id": str(self.pair_properties.get('srcClientId')),
            "proxy_client_id": str(self.pair_properties.get('headClientId')),
            "guid": self.pair_properties.get('sourceGuid'),
            "endpoint": BLRPairs.EndPointTypes(self.pair_properties.get('srcEndPointType')),
        }

    @property
    def source_vm(self):
        """Returns (str): the source VM name"""
        return self.source.get('name')

    @property
    def destination(self):
        """Returns: (dict) The properties of the destination client
        eg: {
            name: 'clientName',
            proxy_client_id: 'tail proxy_id',
            guid: 'client guid',
            endpoint: 'endpoint enum'
        }
        """
        return {
            "name": self.pair_properties.get('destinationName'),
            "client_id": str(self.pair_properties.get('destClientId')),
            "proxy_client_id": str(self.pair_properties.get('tailClientId')),
            "guid": self.pair_properties.get('destinationGuid'),
            "endpoint": BLRPairs.EndPointTypes(self.pair_properties.get('destEndPointType')),
        }

    @property
    def destination_vm(self):
        """Returns (str): the destination VM name"""
        return self.destination.get('name')

    @property
    def lag_time(self):
        """Returns: (int) The replication lag for pair in minutes"""
        return self.pair_properties.get('lagTime')

    @property
    def replication_group_name(self):
        """Returns: (str) The name of the replication group"""
        return self.pair_properties.get('replicationGroup', {}).get('replicationGroupName')

    @property
    def pending_status(self):
        """Returns: (enum) The pair pending Status"""
        return BLRPairs.PendingStatus(self.pair_properties.get('pendingStatusCode'))

    @property
    def pair_flag(self):
        """Returns: (int) The pair's flag status"""
        return self.pair_properties.get('flags')

    @property
    def subclient_props(self):
        """Returns: (dict) The subclient associated with pair's properties
        eg: {
            "subclientName": "subclient name",
            "subclientId": subclient ID,
            "instanceId": instance ID,
            "backupsetId": backupset ID,
            "clientId": client ID
        }
        """
        return self.pair_properties.get('entity')

    @property
    def pair_recovery_type(self):
        """Returns: (enum) Returns whether the pair is granular or live"""
        return BLRPairs.RecoveryType(self.pair_properties.get('blrRecoveryOpts', {}).get('recoveryType'))

    @property
    def pair_rpstore_intervals(self):
        """Returns: (dict) A dictionary of intervals set for RPstores
        eg: {
            'ccrpInterval': 15,
            'maxRpStoreOfflineTime': 900,
            'useOffPeakSchedule': True,
            'acrpInterval': 3600,
            'rpMergeDelay': 43200,
            'maxRpInterval': 21600,
            'rpStoreId': 0,
            'rpRetention': 604800,
            'rpStoreName': 'N/A'
        }
        """
        return self.pair_properties.get('blrRecoveryOpts', {}).get('granularV2', {})

    @property
    def pair_volume_map(self):
        """Returns: (list) Returns a list of volume mappings for FSBLR
        eg: [{
            'sourceVolumeGUID': 'F961A090-90B3-403A-8629-10203C81517F',
            'destVolume': 'F:',
            'destVolumeGUID': '0A800478-57E2-42B2-80BA-F7BA1B2E0BE1',
            'sourceVolume': 'E:'
        }]
        """
        return self.pair_properties.get('srcDestVolumeMap', [])

    @property
    def pair_latest_stats(self):
        """Returns: (list) A list of dictionary of latest statistics for BLR pair
        eg: [{
            'repDataDeltaActual': 226051,
            'ioDelta': 303935,
            'repSetSize': 10522460160,
            'iopsDelta': 160,
            'sizeInRpStore': 0,
            'id': 14195,
            'repDataDeltaComp': 226051,
            'retention': 0,
            'timeStamp': {'time': 1622714743}
        }]
        """
        return self.pair_properties.get('statsList')

    def get_pair_stats(self):
        """Returns: (list) A list of dictionary of statistics for BLR pair
        eg: [{
            'repDataDeltaActual': 226051,
            'ioDelta': 303935,
            'repSetSize': 10522460160,
            'iopsDelta': 160,
            'sizeInRpStore': 0,
            'id': 14195,
            'repDataDeltaComp': 226051,
            'retention': 0,
            'timeStamp': {'time': 1622714743}
        }]
        """
        flag, response = (self._commcell_object._cvpysdk_object
                          .make_request('GET', self._PAIR_STATS % self._pair_id))
        if flag:
            if response.json() and 'statsList' in response.json():
                return response.json().get('statsList', [])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def get_recovery_point_stores(self):
        """Returns a list of all recovery point stores for the BLR pair
            Args:

            Returns: Gets the BLR rpstores list

            Raises:
            SDKException:
            if response is empty

            if response is not success
        """
        destination_client = self._commcell_object.clients.get(int(self.destination['client_id']))
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._GRANULAR_RP_STORES %
                                                                            (self.destination['proxy_client_id'],
                                                                             str(self.subclient_props['subclientId']),
                                                                             destination_client.client_guid))
        if flag:
            if response.json() and 'vmScale' in response.json():
                return response.json().get('vmScale', {}).get('restorePoints', [])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def get_test_failover_vms(self, boot_type: int = 1):
        """Returns the BLRTestFailovers object for all test failover VMs of the BLR pair
        Args:
            boot_type (int): Refer to BLRTestFailover.BLRBootType
        Returns:
            BLRTestFailovers object
        """
        boot_type = BLRTestFailovers.BLRBootType(boot_type)
        return BLRTestFailovers(self._commcell_object, self._pair_id, boot_type)

    def stop(self):
        """Stops the BLR Pair
            Args:

            Returns:

            Raises:
            SDKException:
            if response is empty
            if response is not success
        """
        self._perform_action(self.PairOperationsStatus.STOP)

    def start(self):
        """Starts the BLR Pair
            Args:

            Returns:

            Raises:
            SDKException:
            if response is empty
            if response is not success
        """
        self._perform_action(self.PairOperationsStatus.START)

    def resume(self):
        """Resumes the BLR Pair
            Args:

            Returns:

            Raises:
            SDKException:
            if response is empty
            if response is not success
        """
        self._perform_action(self.PairOperationsStatus.RESUME)

    def resync(self):
        """Resyncs the BLR pair
            Args:

            Returns:

            Raises:
            SDKException:
            if response is empty
            if response is not success
        """
        self._perform_action(self.PairOperationsStatus.RESYNC)

    def suspend(self):
        """Suspends the BLR Pair
            Args:

            Returns:

            Raises:
            SDKException:
            if response is empty
            if response is not success
        """
        self._perform_action(self.PairOperationsStatus.SUSPEND)

    def wait_for_pair_status(self, expected_status, timeout=30):
        """
        Waits for the BLR pair to reach the expected status
            Args:
                expected_status (enum or str): Enum of PairStatus or string value for pair status
                timeout (int)                : The amount of time in minutes to wait for pair to
                                                    reach status before exiting
            Returns:
                True, if the expected status is met
                False, if the expected status was not met in given time
        """
        if isinstance(expected_status, str):
            expected_status = BLRPairs.PairStatus(expected_status.upper())
        start_time = time.time()
        self.refresh()

        while not self.pair_status == expected_status:
            time.sleep(30)

            if time.time() - start_time > timeout * 60:
                break
        return self.pair_status == expected_status

    def create_replica_copy(self, destination_volumes, copy_volumes, timestamp=None):
        """Perform the DR operation for the BLR pair
            Args:
                destination_volumes (list)  : The destination volumes list
                copy_volumes (list)         : The copy volumes list
                timestamp (int)             : The timestamp of the RPstore, only for granular pairs
            Returns:

            Raises:
            SDKException:
            if response is empty
            if response is not success
        """
        restore_point = None
        if self.pair_recovery_type == BLRPairs.RecoveryType.GRANULARV2:
            if timestamp is not None:
                restore_point = [replica_point for replica_point in self.get_recovery_point_stores()
                                 if int(replica_point['timeStamp']) == timestamp][0]
            else:
                restore_point = self.get_recovery_point_stores()[-1]

        destination_client = self._commcell_object.clients.get(int(self.destination['client_id']))
        destination_volumes = destination_client.get_mount_volumes(destination_volumes)
        copy_volumes = destination_client.get_mount_volumes(copy_volumes)

        request_json = {
            "taskInfo": {
                "task": {
                    "ownerId": 1,
                    "taskType": 1,
                    "ownerName": "",
                    "initiatedFrom": 1,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4047
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "maxNumberOfStreams": 0,
                                        "allCopies": True,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": False
                                    }
                                }
                            },
                            "adminOpts": {
                                "blockOperation": {
                                    "operations": [
                                        {
                                            "appId": int(self.subclient_props['subclientId']),
                                            "opType": 8,
                                            "dstProxyClientId": int(self.destination['client_id']),
                                            "fsMountInfo": {
                                                "doLiveMount": True,
                                                "lifeTimeInSec": 7200,
                                                "blrPairId": int(self._pair_id),
                                                "mountPathPairs": [{
                                                    "mountPath": copy['accessPathList'][0],
                                                    "srcPath": destination['accessPathList'][0],
                                                    "srcGuid": destination['guid'],
                                                    "dstGuid": copy['guid']} for destination, copy in
                                                    zip(destination_volumes, copy_volumes)],
                                                "rp": {
                                                    "timeStamp": int(restore_point['timeStamp']),
                                                    "sequenceNumber": int(restore_point['sequenceNumber']),
                                                    "rpType": 1,
                                                    "appConsistent": False,
                                                    "dataChangedSize": int(restore_point['dataChangedSize'])
                                                } if restore_point is not None else None
                                            }
                                        }
                                    ]
                                }
                            },
                        }
                    }
                ]
            }
        }
        if restore_point is None:
            admin_opts = request_json['taskInfo']['subTasks'][0]['options']['adminOpts']
            del admin_opts['blockOperation']['operations'][0]['fsMountInfo']['rp']

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            self._services['RESTORE'],
                                                                            request_json)
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Job', '102', o_str)
                else:
                    raise SDKException('Job', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """ Refresh the BLR pair properties """
        self._get_pair_properties()


class BLRTestFailovers:
    """Class for getting all test failover VMs for BLR pair"""
    class BLRBootType(Enum):
        TESTBOOT = 1
        PERMANENT = 2

    class BootStatus(Enum):
        NONE = 0
        IN_PROGRESS = 1
        SUCCESS = 2
        FAILED = 3
        ABOUT_TO_EXPIRE = 4
        EXPIRED = 5
        USER_DELETED = 6
        DELETE_FAILED = 7
        PARTIAL_SUCCESS = 8

    def __init__(self, commcell_object, pair_id, boot_type: BLRBootType):
        """Method for making initial data members
            Args:
                commcell_object (Commcell)      --  instance of the Commcell class
                pair_id (str)                   --  Id of the BLR pair
                boot_type (BLRBootType)         --  The type of the boot for VMs
        """
        self._commcell_object = commcell_object
        self._services = commcell_object._services

        self._pair_id = pair_id
        self._boot_type = boot_type
        self._boot_vm_dict = None

        self._GET_BOOT_VMS = self._services['BLR_BOOT_DETAILS']

        self.refresh()

    def __repr__(self):
        """String representation of the instance of BLRTestFailovers"""
        representation_string = 'BLR Test failover VMs class instance for pair id: {0}'
        return representation_string.format(self._pair_id)

    def _get_test_failover_vms(self):
        """Gets the list of all test failover VMs
            Args:
            Returns: Gets the BLR test failover VMs list
            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._GET_BOOT_VMS % (self._pair_id, self._boot_type.value))
        if flag:
            if response.json() and 'siteInfo' in response.json():
                return response.json()['siteInfo']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the VMs list for BLR pair"""
        self._boot_vm_dict = {boot_dict.get('name'): boot_dict
                              for boot_dict in self._get_test_failover_vms()}

    @property
    def all_boot_vms(self):
        """Returns a list of all boot VMs"""
        return list(self._boot_vm_dict.keys())

    def get_boot_vm_details(self, vm_name):
        """Get the boot VM details for a given vm name
        Args:
            vm_name (str): The name of the VM to fetch details for
        Returns:
            dict:  {
                id (int)                : The ID of the test failover VM
                uuid (str)              : The UUID of the test failover VM
                name (str)              : The name of the test failover VM
                creation_time (int)     : The timestamp of VM creation
                vm_status (BootStatus)  : The status of the test failover VM
                status_message (str)    : The description of the VM status
            }
        Raises:
            BLRPair not found: If test boot VM name is not found
        """
        vm_dict = self._boot_vm_dict.get(vm_name)
        if not vm_dict:
            raise SDKException('BLRPairs', '102', f'BLR test boot VM with name {vm_name} not found')
        return {
            'id': vm_dict.get('id'),
            'uuid': vm_dict.get('uuid'),
            'name': vm_dict.get('name'),
            'creation_time': vm_dict.get('creationTime'),
            'vm_status': self.BootStatus(vm_dict.get('status')) if vm_dict.get('status') else None,
            'status_message': vm_dict.get('statusMessage'),
            'expiration_time': vm_dict.get('bestBefore')
        }
