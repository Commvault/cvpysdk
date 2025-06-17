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

"""Main file for performing deduplication engine related operations on the commcell.

This file has all the classes related to deduplication engine operations.

DeduplicationEnigines:  Class for representing all the deduplication engines associated to the commcell.

DeduplicationEninge:    Class for representing a single deduplication engine associated to the commcell.

Store:  Class for representing a single deduplication store associated to the deduplication engine.

SubStore:   Class for representing a single substore associated to the deduplication store.

DeduplicationEngines:
    __init__(commcell_object)   - Initialise the DeduplicationEngines class instance


    __repr__()                  - Representation string consisting of deduplication engines.

    __str__()                   - Representation string for the instance of the DeduplicationEngines class.

    _get_engines()              - returns all engines properties on commcell

    get()                       - returns list of all engines

    has_engine()                - checkes if a engine exisits for storage policy and copy name

    refresh()                   - refreshes all engine properties

DeduplicationEngine:
    __init__(commcell_object, storage_policy_name, copy_name)   - Initialise the DeduplicationEngine class instance

    __repr__()                  - Representation string consisting of deduplication engine.

    __str__()                   - Representation string for the instance of the DeduplicationEngine class.

    _initialize_policy_and_copy_id()    - Gets deduplication engine properties

    _get_engine_properties()    - initializes deduplication engine properties

    _initialize_stores()        - initializes all the stores presnet in deduplication engine

    refresh()                   - refreshes all the deduplication engine properties

    all_stores()                - Checks if a deduplication store exists in a engine with provided storeid id.

    has_store()                 - returns list of all stores present in deduplication engines

    get()                       - Returns store class object for sssthe store id on deduplication engine

Store:
    __init__(commcell_object, storage_policy_name, copy_name, store_id)   - Initialise the Store class instance

    __repr__()                  - Representation string consisting of deduplication store.

    __str__()                   - Representation string for the instance of the Store class.

    _initialize_store_properties()  - initializes store properties

    _get_substores()            - gets all substores in a store along with properties

    _initialize_substores()     - initializes all substore properties

    refresh()                   - refreshes store properties

    has_substore()              - checks if a substore exists in a store

    get()                      - gets a substore class object for provided substore id

    seal_deduplication_database() - Seals the deduplication database

    recover_deduplication_database()    - starts DDB Reconstruction job for store

    run_space_reclaimation()    - starts DDB space reclaimation job for store

    run_ddb_verification()      - starts DDB verification job for store

    config_only_move_partition()    - performs config-only ddb move operation on specified substore

    move_partition()            - performs normal ddb move operation on specified substore
    
    add_partition()     -       Adding a partition to this store

Attributes
----------
    **all_substores**       -- returns list of all substores present on a deduplication store

    **store_flags**         -- returns the deduplication flags on store

    **store_name**          -- returns the store display name

    **store_id**            -- return the store id

    **version**             -- returns deduplication store version

    **status**              -- returns the store display name

    **storage_policy_name** -- returns storage policy name associated with store

    **copy_name**           -- returns copy name associated with store

    **copy_id**             -- returns copy id the store is associated to

    **enable_store_pruning**            -- returns whether purning is enabled or disabled on store

    **enable_store_pruning.setter**     -- sets store purning value to true or false

    **enable_garbage_collection**       -- returns garbage collection property value for store

    **enable_garbage_collection.setter** -- sets garbage collection property value for store

    **enable_journal_pruning**           --  Returns the value of journal pruning property

    **enable_journal_pruning.setter**    --  Sets the value of journal pruning property


Substore:
    __init__(commcell_object, storage_policy_name, copy_name,
            store_id, substore-id)   - Initialise the SubStore class instance

    __repr__()                  - Representation string consisting of substore.

    __str__()                   - Representation string for the instance of the SubStore class.

    _initialize_substore_properties()   - initialize substore properties of a store

    refresh()                   - refreshes substore properties

    mark_for_recovery()         - marks a substore for recovery
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from enum import Enum

from .exception import SDKException
from .job import Job
from .storage import MediaAgent


class StoreFlags(Enum):
    IDX_SIDBSTORE_FLAGS_PRUNING_ENABLED = 536870912
    IDX_SIDBSTORE_FLAGS_DDB_NEEDS_AUTO_RESYNC = 33554432
    IDX_SIDBSTORE_FLAGS_DDB_UNDER_MAINTENANCE = 16777216


class DeduplicationEngines(object):
    """Class for getting all the deduplication engines associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the DeduplicationEngines class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the StoragePolicies class
        """
        self._commcell_object = commcell_object

        self._engines = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all deduplication engines of the commcell.

            Returns:
                str - string of all the deduplication associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Deduplication engine')
        for index, engine in enumerate(self._engines):
            sub_str = '{:^5}\t{}/{}\n'.format(index + 1, engine[0], engine[1])
            representation_string += sub_str
        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the DeduplicationEngines class."""
        return "DeduplicationEngines class instance for Commcell"

    def _get_engines(self):
        """
        gets all the deduplication engines associated with the commcell

        Return:
            dict - consists of all the engines in the commcell

        Raises:
            SDKException:
                if response is not success
        """
        request_json = {
            "EVGui_DDBEnginesReq": {
                "filterOptions": {
                    "propertyLevel": 1
                },
                "storagepolicy": {
                    "storagePolicyId": 0
                },
                "spCopy": {
                    "copyId": 0,
                    "storagePolicyId": 0
                },
                "store": {
                    "type": 115
                },
                "flags": 0
            }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_json
        )
        if flag:
            if response and response.json() and 'engines' in response.json():
                engines = response.json()['engines']

                if engines == []:
                    return {}

                engines_dict = {}

                for engine in engines:
                    temp_sp_name = engine['sp']['name'].lower()
                    temp_sp_id = str(engine['sp']['id']).lower()
                    temp_copy_name = engine['copy']['name'].lower()
                    temp_copy_id = str(engine['copy']['id']).lower()
                    engines_dict[(temp_sp_name, temp_copy_name)] = [temp_sp_id, temp_copy_id]
                return engines_dict
            return {}
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    @property
    def all_engines(self):
        """returns list all the deduplication engines with storage polic and copy name"""
        return list(self._engines.keys())

    def refresh(self):
        """refreshes all the deduplication engines and their properties"""
        self._engines = self._get_engines()

    def has_engine(self, storage_policy_name, copy_name):
        """Checks if a deduplication engine exists in the commcell with the input storage policy and copy name.

            Args:
                storage_policy_name (str)  --  name of the storage policy

                copy_name (str)  --  name of the storage policy copy

            Returns:
                bool - boolean output whether the deduplication engine exists in the commcell or not

            Raises:
                SDKException:
                    if type of the storage policy and copy name arguments are not string
        """
        
        self.refresh()
        
        if not isinstance(storage_policy_name, str) and not isinstance(copy_name, str):
            raise SDKException('Storage', '101')
        return self._engines and (storage_policy_name.lower(), copy_name.lower()) in self._engines

    def get(self, storage_policy_name, copy_name):
        """
        Returns eng class object for the engine on deduplication engines

        Args:
            storage_policy_name (str) - name of the storage policy

            copy_name (str) - name of the deduplication enabled copy

        Return:
             object - instance of engine class for a given storage policy and copy name

        Raises:
            SDKException:
                if type of arguments are not string

                if no engine exists with given storage policy and copy name
        """
        if not isinstance(storage_policy_name, str) and not isinstance(copy_name, str):
            raise SDKException('Storage', '101')

        storage_policy_name = storage_policy_name.lower()
        copy_name = copy_name.lower()

        if self.has_engine(storage_policy_name, copy_name):
            return DeduplicationEngine(
                self._commcell_object, storage_policy_name, copy_name
            )
        raise SDKException(
            'Storage', '102', f'No dedupe engine exists with name: {storage_policy_name}/{copy_name}'
        )


class DeduplicationEngine(object):
    """Class to get all stores associated for deduplication engine"""

    def __init__(self, commcell_object, storage_policy_name, copy_name, storage_policy_id=None, copy_id=None):
        """Initialise the DeduplicationEngine class instance.

        Args:
            commcell_object (object)    - instance of class Commcell

            storage_policy_name (str)   - storage policy name on commcell

            copy_name (str)             - copy name under storage policy

            storage_policy_id (int)     - storage policy id for commcell

            copy_id (int)               - copy id under storage policy
        """
        self._storage_policy_name = storage_policy_name.lower()
        self._copy_name = copy_name.lower()
        self._commcell_object = commcell_object
        self._engine_properties = {}
        self._stores = {}
        if not storage_policy_id and not copy_id:
            self._initialize_policy_and_copy_id()
        else:
            if not isinstance(storage_policy_id, int) and not isinstance(copy_id, int):
                raise SDKException('Storage', '101')
            self._storage_policy_id = storage_policy_id
            self._copy_id = copy_id
        self.refresh()

    def __str__(self):
        """Representation string consisting of deduplication engine.

            Returns:
                str - string of all the stores associated with the deduplication engine
        """
        representation_string = '{:^5}\t{:^20}\t{}\n\n'.format('Store ID.', 'Store', 'Sealed Status')

        for store_id in self._stores:
            status = 'sealed' if self._stores[store_id]['sealedTime'] else 'active'
            sub_str = '{:^5}\t{:20}\t{}\n'.format(store_id, self._stores[store_id]['storeName'], status)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the DeduplicationEngine class."""
        return "DeduplicationEngine class instance for Engine: '{0}/{1}'".format(
            self._storage_policy_name, self._copy_name
        )

    def _initialize_policy_and_copy_id(self):
        """initializes the variables for storage policy and copy id"""
        deduplication_engines = DeduplicationEngines(self._commcell_object)
        policy_and_copy_id = deduplication_engines._engines[(self._storage_policy_name, self._copy_name)]
        self._storage_policy_id = policy_and_copy_id[0]
        self._copy_id = policy_and_copy_id[1]

    def _get_engine_properties(self):
        """
        Gets deduplication engine properties

        Return:
             dict - engine properties for each store on deduplication engine

        Raises:
            SDKException:
                    if response is empty

                    if response is not success
        """
        request_json = {
            "EVGui_DDBEnginesReq": {
                "filterOptions": {
                    "propertyLevel": 20
                },
                "storagepolicy": {
                    "storagePolicyId": self.storage_policy_id
                },
                "spCopy": {
                    "copyId": self.copy_id,
                    "storagePolicyId": self.storage_policy_id
                },
                "store": {
                    "type": 115
                },
                "flags": 0
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_json
        )
        if flag:
            if response and response.json():
                return response.json()
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _initialize_engine_properties(self):
        """initializes deduplication engine properties"""
        self._engine_properties = self._get_engine_properties()
        self._initialize_stores()

    def _initialize_stores(self):
        """initializes all the stores presnet in deduplication engine"""
        for store in self._engine_properties.get('engines'):
            temp_sp_name = store['sp']['name'].lower()
            temp_copy_name = store['copy']['name'].lower()
            if (temp_sp_name, temp_copy_name) == (self._storage_policy_name, self._copy_name):
                self._stores[store['storeId']] = store

    def refresh(self):
        """refreshes all the deduplication engine properties"""
        self._initialize_engine_properties()

    @property
    def all_stores(self):
        """returns list of all stores present in deduplication engines"""
        stores = []
        for store_id in self._stores:
            status = 'sealed' if self._stores[store_id]['sealedTime'] else 'active'
            stores.append([store_id, self._stores[store_id]['storeName'], status])
        return stores

    @property
    def storage_policy_id(self):
        """returns storage policy id associated to engine"""
        return self._storage_policy_id

    @property
    def copy_id(self):
        """returns copy id associated to engine"""
        return self._copy_id

    def has_store(self, store_id):
        """Checks if a deduplication store exists in a engine with provided storeid id.
        Args:
            store_id (int) - deduplication store id to check existance

        Returns:
            bool - boolean output whether the deduplication store exists in the engine or not

        Raises:
            SDKException:
                if type of the store id argument is not int
        """
        if not isinstance(store_id, int):
            raise SDKException('Storage', '101')
        return self._stores and store_id in self._stores

    def get(self, store_id):
        """
        Returns store class object for the store id on deduplication engine

        Args:
            store_id (int) - id of the store on deduplication engine

        Return:
            object - instance of Store class for a given store id

        Raises:
            if type of store id argument is not integer

            if no store exists with given store id
        """
        if not isinstance(store_id, int):
            raise SDKException('Storage', '101')

        if self.has_store(store_id):
            return Store(self._commcell_object, self._storage_policy_name, self._copy_name, store_id)
        raise SDKException(
            'Storage', '102', f'No store exists with id: {store_id}'
        )


class Store(object):
    """Class for performing deduplication store level operations for deduplication engine"""

    def __init__(self, commcell_object, storage_policy_name, copy_name, store_id):
        """Initialise the Store class instance.

        Args:
            commcell_object (object)    - commcell class instance

            storage_policy_name (str)   - storage policy name in commcell

            copy_name (str)             - copy name under storage policy

            store_id (int)              - deduplication store id in commcell
        """
        self._storage_policy_name = storage_policy_name.lower()
        self._copy_name = copy_name.lower()
        self._store_id = store_id
        self._commcell_object = commcell_object
        self._substores = {}
        self._store_properties = {}
        self._extended_flags = None
        self._dedupe_flags = None
        self._store_flags = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of deduplication store.

            Returns:
                str - string of all the substores associated with the deduplication store
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('SubStore ID.', 'SubStoreList')

        for substore_id in self._substores:
            sub_str = '{:^5}\t[{}]{}\n'.format(substore_id, self._substores[substore_id]['MediaAgent']['name'],
                                               self._substores[substore_id]['Path'])
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Store class."""
        return "Store class instance for Deduplication Store ID: '{0}'".format(self._store_id)

    def _initialize_store_properties(self):
        """initializes the deduplication store proerties"""
        deduplication_engine = DeduplicationEngine(self._commcell_object, self._storage_policy_name, self._copy_name)
        self._store_properties = deduplication_engine._stores[self._store_id]
        self._extended_flags = self._store_properties['storeExtendedFlags']
        self._dedupe_flags = self._store_properties['dedupeFlags']
        self._store_flags = self._store_properties['storeFlags']
        self._initialize_substores()

    def _get_substores(self):
        """
        Gets properties of all the substores in a deduplication store

        Return:
             dict - store properties and substore list for each substore on deduplication store

        Raises:
            SDKException:
                    if response is empty

                    if response is not success
        """
        request_json = {
            "EVGui_SubStoreListReq": {
                "commcellId": 2,
                "storeId": self.store_id
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_json
        )
        if flag:
            if response.json():
                return response.json()
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _initialize_substores(self):
        """initialisez all the substores present in a deduplication store"""
        substre_raw = self._get_substores()
        for substore in substre_raw.get('subStoreList'):
            self._substores[substore['subStoreId']] = substore

    def refresh(self):
        """refreshes all the deduplication store properties"""
        self._initialize_store_properties()

    def add_partition(self, path, media_agent):
        """Adding a partition to this store

        Args:

            path (str)   - path of the new deduplication database

            media_agent (str)  - MediaAgent name of the new deduplication database

        """
        payload = None

        if not isinstance(path, str):
            raise SDKException("Storage","101")

        if not isinstance(media_agent, str) and not isinstance(media_agent, MediaAgent):
            raise SDKException("Storage", "101")

        if isinstance(media_agent, str):
            media_agent = MediaAgent(self._commcell_object, media_agent)

        payload = """
        <EVGui_ParallelDedupConfigReq commCellId="2" copyId="{0}" operation="15">
        <SIDBStore SIDBStoreId="{1}"/>
        <dedupconfigItem commCellId="0">
        <maInfoList><clientInfo id="{2}" name="{3}"/>
        <subStoreList><accessPath path="{4}"/>
        </subStoreList></maInfoList></dedupconfigItem>
        </EVGui_ParallelDedupConfigReq>
        """.format(self.copy_id, self._store_id, media_agent.media_agent_id, media_agent.media_agent_name, path)

        self._commcell_object._qoperation_execute(payload)
        
    @property
    def all_substores(self):
        """returns list of all substores present on a deduplication store"""
        substores = []
        for substore_id in self._substores:
            substores.append([substore_id, self._substores[substore_id]['Path'],
                              self._substores[substore_id]['MediaAgent']['name']])
        return substores

    def has_substore(self, substore_id):
        """Checks if a substore exists in a deduplication store with provided substore id.
        Args:
            substore_id (int) - substore id to check existance

        Returns:
            bool - boolean output whether the substore exists in the store or not

        Raises:
            SDKException:
                if type of the store id argument is not int
        """
        if not isinstance(substore_id, int):
            raise SDKException('Storage', '101')
        return self._substores and substore_id in self._substores

    def get(self, substore_id):
        """
        Returns substore class object for the substore id on deduplication store

        Args:
            substore_id (int) - id of the substore on deduplication store

        Return:
             object - instance of subStore class for a given substore id

        Raises:
            if type of substore id argument is not integer

            if no substore exists with given substore id
        """
        if not isinstance(substore_id, int):
            raise SDKException('Storage', '101')

        if self.has_substore(substore_id):
            return SubStore(self._commcell_object, self._storage_policy_name, self._copy_name, self._store_id,
                            substore_id)
        raise SDKException(
            'Storage', '102', f'No substore exists with id: {substore_id}'
        )

    @property
    def store_flags(self):
        """returns the deduplication flags on store"""
        self.refresh()
        return self._store_flags

    @property
    def store_name(self):
        """returns the store display name"""
        return self._store_properties.get('storeName')

    @property
    def store_id(self):
        """return the store id"""
        return self._store_id

    @property
    def version(self):
        """returns deduplication store version"""
        return self._store_properties.get('ddbVersion')

    @property
    def status(self):
        """returns the store display name"""
        return self._store_properties.get('status')

    @property
    def storage_policy_name(self):
        """returns storage policy name associated with store"""
        return self._storage_policy_name

    @property
    def copy_name(self):
        """returns copy name associated with store"""
        return self._copy_name

    @property
    def copy_id(self):
        """returns copy id the store is associated to"""
        return self._store_properties.get('copy').get('id')

    @property
    def enable_garbage_collection(self):
        """returns garbage collection property value for store"""
        if (self._extended_flags & 4) == 0:
            return False
        return True

    @property
    def enable_store_pruning(self):
        """returns if purning is enabled or disabled on store"""
        return self._store_flags & StoreFlags.IDX_SIDBSTORE_FLAGS_PRUNING_ENABLED.value != 0

    @enable_store_pruning.setter
    def enable_store_pruning(self, value):
        """sets store purning value to true or false
        Args:
              value (bool) -- value to enable or disable store pruning
        """
        if not value:
            new_value = self._store_flags & ~StoreFlags.IDX_SIDBSTORE_FLAGS_PRUNING_ENABLED.value
        else:
            new_value = self._store_flags | StoreFlags.IDX_SIDBSTORE_FLAGS_PRUNING_ENABLED.value

        request_json = {
            "EVGui_ParallelDedupConfigReq": {
                "processinginstructioninfo": "",
                "SIDBStore": {
                    "SIDBStoreId": self.store_id,
                    "SIDBStoreName": self.store_name,
                    "extendedFlags": self._extended_flags,
                    "flags": new_value,
                    "minObjSizeKB": 50,
                    "oldestEligibleObjArchiveTime": -1
                },
                "appTypeGroupId": 0,
                "commCellId": 2,
                "copyId": self.copy_id,
                "operation": 3
            }
        }
        output = self._commcell_object.qoperation_execute(request_json)
        if output['error']['errorString'] != '':
            raise SDKException('Storage', '102', output['error']['errorString'])

        self.refresh()

    @enable_garbage_collection.setter
    def enable_garbage_collection(self, value):
        """sets enable garbage collection with true or false
        Args:
              value (bool) -- value to enable or disable garbage collection
        """
        if self.version == -1:
            if not value:
                new_value = self._extended_flags & ~4
            else:
                new_value = self._extended_flags | 4

            request_json = {
                "EVGui_ParallelDedupConfigReq": {
                    "processinginstructioninfo": "",
                    "SIDBStore": {
                        "SIDBStoreId": self.store_id,
                        "SIDBStoreName": self.store_name,
                        "extendedFlags": new_value,
                        "flags": self._store_flags,
                        "minObjSizeKB": 50,
                        "oldestEligibleObjArchiveTime": -1
                    },
                    "appTypeGroupId": 0,
                    "commCellId": 2,
                    "copyId": self.copy_id,
                    "operation": 3
                }
            }
            self._commcell_object.qoperation_execute(request_json)
        self.refresh()

    @property
    def enable_journal_pruning(self):
        """returns journal pruning property value for store"""
        if (self._extended_flags & 8) == 0:
            return False
        return True

    @enable_journal_pruning.setter
    def enable_journal_pruning(self, value):
        """sets enable journal pruning with true or false
        Args:
              value (bool) -- value to enable journal pruning
        """
        if not self._extended_flags & 8 and value or self.version == -1:

            if value:
                new_value = self._extended_flags | 8
            else:
                new_value = self._extended_flags & ~8

            request_json = {
                "EVGui_ParallelDedupConfigReq": {
                    "processinginstructioninfo": "",
                    "SIDBStore": {
                        "SIDBStoreId": self.store_id,
                        "SIDBStoreName": self.store_name,
                        "extendedFlags": new_value,
                        "flags": self._store_flags,
                        "minObjSizeKB": 50,
                        "oldestEligibleObjArchiveTime": -1
                    },
                    "appTypeGroupId": 0,
                    "commCellId": 2,
                    "copyId": self.copy_id,
                    "operation": 3
                }
            }
            self._commcell_object.qoperation_execute(request_json)
            self.refresh()
        elif self._extended_flags & 8 and value:
            raise SDKException("Response", '500', "Journal pruning is already enabled.")
        else:
            raise SDKException("Response", '500', "Journal pruning once enabled cannot be disabled.")

    def seal_deduplication_database(self):
        """ Seals the deduplication database """

        request_json = {
                        "App_SealSIDBStoreReq":{
                                "SidbStoreId": self.store_id
                            }
                        }
        self._commcell_object._qoperation_execute(request_json)

    def recover_deduplication_database(self, full_reconstruction=False, scalable_resources=True):
        """
        refresh store properties and start reconstruction job if at least one substore is marked for recovery

        Args:
            full_reconstruction (bool)  - to reconstruct without using previous backup (True/False)
                                        Default: False

            scalable_resources (bool)    - to run reconstruction using scalable resources
                                        Default: True

        Returns:
             object - instance of Job class for DDB Reconstruction job

        Raises:
             SDKException:
                if DDB Reconstruction job failed

                if response if empty

                if response in not success
        """
        self.refresh()
        substore_list = ""
        for substore in self.all_substores:
            if self._substores.get(substore[0]).get('status') == 1:
                substore_list += f"<SubStoreIdList val='{substore[0]}' />"

        if not substore_list:
            o_str = 'No substore is eligible for recon.'
            raise SDKException('Storage', '102', o_str)

        request_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <TMMsg_CreateTaskReq>
                  <processinginstructioninfo/>
                  <taskInfo>
                    <task>
                      <taskFlags>
                        <disabled>false</disabled>
                      </taskFlags>
                      <policyType>DATA_PROTECTION</policyType>
                      <taskType>IMMEDIATE</taskType>
                      <initiatedFrom>COMMANDLINE</initiatedFrom>
                    </task>
                    <associations>
                      <copyName>{self.copy_name}</copyName>
                      <storagePolicyName>{self.storage_policy_name}</storagePolicyName>
                    </associations>
                    <subTasks>
                      <subTask>
                        <subTaskType>ADMIN</subTaskType>
                        <operationType>DEDUPDBSYNC</operationType>
                      </subTask>
                      <options>
                        <adminOpts>
                          <dedupDBSyncOption>
                            <SIDBStoreId>{self.store_id}</SIDBStoreId>
                            {substore_list}
                          </dedupDBSyncOption>
                          <reconstructDedupDBOption>
                            <noOfStreams>0</noOfStreams>
                            <allowMaximum>true</allowMaximum>
                            <flags>{int(full_reconstruction)}</flags>
                            <mediaAgents>
                              <mediaAgentName></mediaAgentName>
                            </mediaAgents>
                            <useScallableResourceManagement>{str(scalable_resources).lower()}</useScallableResourceManagement>
                          </reconstructDedupDBOption>
                        </adminOpts>
                      </options>
                      <subTaskOperation>OVERWRITE</subTaskOperation>
                    </subTasks>
                  </taskInfo>
                </TMMsg_CreateTaskReq>"""
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_xml
        )
        if flag:
            if response and response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'DDB recon job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                raise SDKException('Storage', '112')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def run_space_reclaimation(self, level=3, clean_orphan_data=False, use_scalable_resource=True, num_streams="max",
                               defragmentation=True):
        """
        runs DDB Space reclaimation job with provided level

        Args:
            level (int) - criteria for space reclaimation level (1, 2, 3, 4)
                        Default: 3

            clean_orphan_data (bool) - run space reclaimation with OCL or not (True/False)
                        Default: False

            use_scalable_resource (bool)    - Use Scalable Resource Allocation while running DDB Space Reclamation Job
                        Default: True

            num_streams (str)   -- Number of streams with which job will run.

            defragmentation(bool) - run space reclamation with Defragmentation or not (True/False)
                        Default : True
        Returns:
             object - instance of Job class for DDB Verification job

        Raises:
             SDKException:
                if invalid level is provided

                if DDB space reclaimation job failed

                if response if empty

                if response in not success
        """
        if not (isinstance(level, int)) and level not in range(1, 4):
            raise SDKException('Storage', '101')

        if not isinstance(use_scalable_resource, bool):
            raise SDKException('Storage', '101')

        if not isinstance(defragmentation, bool):
            raise SDKException('Storage', '101')

        use_max_streams = "true"
        max_num_of_streams = 0
        if str(num_streams) != "max":
            max_num_of_streams = int(num_streams)
            use_max_streams = "false"

        level_map = {
            1: 80,
            2: 60,
            3: 40,
            4: 20
        }
        clean_orphan_data = str(clean_orphan_data).lower()
        request_json = {
            "TMMsg_CreateTaskReq": {
                "taskInfo": {
                    "task": {
                        "taskFlags": {
                            "disabled": "false"
                        },
                        "policyType": "DATA_PROTECTION",
                        "taskType": "IMMEDIATE",
                        "initiatedFrom": "COMMANDLINE"
                    },
                    "associations": {
                        "copyName": self.copy_name,
                        "storagePolicyName": self.storage_policy_name,
                        "sidbStoreName": self.store_name
                    },
                    "subTasks": {
                        "subTask": {
                            "subTaskType": "ADMIN",
                            "operationType": "ARCHIVE_CHECK"
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "useMaximumStreams": use_max_streams,
                                        "maxNumberOfStreams": max_num_of_streams,
                                        "allCopies": "true",
                                        "mediaAgent": {
                                            "mediaAgentName": ""
                                        },
                                        "useScallableResourceManagement": f"{use_scalable_resource}"
                                    }
                                }
                            },
                            "adminOpts": {
                                "archiveCheckOption": {
                                    "ddbVerificationLevel": "DDB_DEFRAGMENTATION",
                                    "backupLevel": "FULL",
                                    "defragmentationPercentage": level_map.get(level),
                                    "ocl": clean_orphan_data,
                                    "runDefrag": defragmentation
                                }
                            }
                        },
                        "subTaskOperation": "OVERWRITE"
                    }
                }
            }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_json
        )
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'DDB space reclaimation job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                raise SDKException('Storage', '113')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def run_ddb_verification(self, incremental_verification=True, quick_verification=True,
                             use_scalable_resource=True, max_streams=0, total_jobs_to_process=1000):
        """
        runs deduplication data verification(dv2) job with verification type and dv2 option

        Args:
            incremental_verification (bool) - DV2 job type, incremental or Full (True/False)
                                            Default: True (Incremental)

            quick_verification (bool)       - DV2 job option, Quick or Complete (True/False)
                                            Default: True (quick verification)

            use_scalable_resource (bool)    - Use Scalable Resource Allocation while running DDB Verification Job
                                            Default: True

            max_streams (int)               - DV2 job option, maximum number of streams to use.
                                              By default, job uses max streams.

            total_jobs_to_process    (int)  - Batch size for number of backup jobs to be picked for verification simultaneously
                                              Default: 1000 jobs per batch

        Returns:
             object - instance of Job class for DDB Verification job

        Raises:
             SDKException:
                if DDB Verification job failed

                if response if empty

                if response in not success
        """

        verification_type = 'INCREMENTAL'
        if not incremental_verification:
            verification_type = 'FULL'

        verification_option = 'QUICK_DDB_VERIFICATION'
        if not quick_verification:
            verification_option = 'DDB_AND_DATA_VERIFICATION'

        use_max_streams = True
        if max_streams != 0:
            use_max_streams = False

        if not isinstance(use_scalable_resource, bool):
            raise SDKException('Storage', '101')

        request_json = {
            "TMMsg_CreateTaskReq": {
                "taskInfo": {
                    "task": {
                        "taskFlags": {
                            "disabled": "false"
                        },
                        "policyType": "DATA_PROTECTION",
                        "taskType": "IMMEDIATE",
                        "initiatedFrom": "COMMANDLINE"
                    },
                    "associations": {
                        "copyName": self.copy_name,
                        "storagePolicyName": self.storage_policy_name,
                        "sidbStoreName": self.store_name
                    },
                    "subTasks": {
                        "subTask": {
                            "subTaskType": "ADMIN",
                            "operationType": "ARCHIVE_CHECK"
                        },
                        "options": {
                            "backupOpts": {
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "useMaximumStreams": f"{use_max_streams}",
                                        "maxNumberOfStreams": f"{max_streams}",
                                        "totalJobsToProcess": total_jobs_to_process,
                                        "allCopies": "true",
                                        "mediaAgent": {
                                            "mediaAgentName": ""
                                        },
                                        "useScallableResourceManagement": f"{use_scalable_resource}"
                                    }
                                }
                            },
                            "adminOpts": {
                                "archiveCheckOption": {
                                    "ddbVerificationLevel": verification_option,
                                    "backupLevel": verification_type
                                }
                            }
                        },
                        "subTaskOperation": "OVERWRITE"
                    }
                }
            }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_json
        )
        if flag:
            if response and response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'DDB verification job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                raise SDKException('Storage', '108')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def config_only_move_partition(self, substoreid, dest_path, dest_ma_name):
        """
        runs config-only ddb move operation on specified substore

        Args:
            substoreid - (int) - substore Id for partition to be moved

            dest_path - (str) - full path for partition destination directory

            dest_ma_name - (str) - destination media agent name

        Returns:
             boolean - returns true or false value depending on success of config only
        """
        dest_ma = self._commcell_object.media_agents.get(dest_ma_name)
        dest_ma_id = int(dest_ma.media_agent_id)
        substore = self.get(substoreid)

        request_json = {
            "MediaManager_CanDDBMoveRunReq": {
                "intReserveFiled1": 0,
                "sourceMaId": substore.media_agent_id,
                "flags": 1,
                "targetPath": dest_path,
                "stringReserveField1": "",
                "storeId": self.store_id,
                "subStoreId": substoreid,
                "targetMAId": dest_ma_id,
                "sourcePath": substore.path
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_json
        )

        if flag:
            if response and response.json():
                if "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'DDB move job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                else:
                    return flag
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def move_partition(self, substoreid, dest_path, dest_ma_name):
        """
        runs normal ddb move operation on specified substore

        Args:
            substoreid - (int) - substore Id for partition to be moved

            dest_path - (str) - full path for partition destination directory

            dest_ma_name - (str) - destination media agent name

        Returns:
             object - instance of Job class for DDB Move job

        Raises:
             SDKException:
                if DDB Move job failed

                if response if empty

                if response in not success
        """
        dest_ma = self._commcell_object.media_agents.get(dest_ma_name)
        dest_ma_id = int(dest_ma.media_agent_id)
        substore = self.get(substoreid)

        request_json = {
            "TMMsg_CreateTaskReq": {
                "taskInfo": {
                    "associations": [
                        {
                            "sidbStoreId": self.store_id,
                            "_type_": 18,
                            "appName": ""
                        }
                    ],
                    "task": {
                        "ownerId": 1,
                        "taskType": 1,
                        "ownerName": "admin",
                        "sequenceNumber": 0,
                        "initiatedFrom": 1,
                        "policyType": 0,
                        "taskId": 0,
                        "taskFlags": {
                            "disabled": False
                        }
                    },
                    "subTasks": [
                        {
                            "subTaskOperation": 1,
                            "subTask": {
                                "subTaskType": 1,
                                "operationType": 5013
                            },
                            "options": {
                                "adminOpts": {
                                    "contentIndexingOption": {
                                        "subClientBasedAnalytics": False
                                    },
                                    "libraryOption": {
                                        "operation": 20,
                                        "ddbMoveOption": {
                                            "flags": 2,
                                            "subStoreList": [
                                                {
                                                    "srcPath": substore.path,
                                                    "storeId": self.store_id,
                                                    "changeOnlyDB": False,
                                                    "destPath": dest_path,
                                                    "subStoreId": substoreid,
                                                    "destMediaAgent": {
                                                        "name": dest_ma_name,
                                                        "id": dest_ma_id
                                                    },
                                                    "srcMediaAgent": {
                                                        "name": substore.media_agent,
                                                        "id": substore.media_agent_id
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                },
                                "restoreOptions": {
                                    "virtualServerRstOption": {
                                        "isBlockLevelReplication": False
                                    },
                                    "commonOptions": {
                                        "syncRestore": False
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_json
        )

        if flag:
            if response and response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'DDB move job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Storage', '102', o_str)
                raise SDKException('Storage', '108')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)


class SubStore(object):
    """Class to performing substore level operations for Deduplication engine"""

    def __init__(self, commcell_object, storage_policy_name, copy_name, store_id, substore_id):
        """Initialise the SubStore class instance.

        Args:
            commcell_object (object)    - commcell class instance

            storage_policy_name (str)   - storage policy name in commcell

            copy_name (str)             - copy name under storage policy

            store_id (int)              - deduplication store id in commcell

            substore_id (int)           - substore id under deduplication store
        """
        self._commcell_object = commcell_object
        self._storage_policy_name = storage_policy_name
        self._copy_name = copy_name
        self._store_id = store_id
        self._substore_id = substore_id
        self._substore_properties = {}
        self._path = None
        self._media_agent = None
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of the SubStore class."""
        return "SubStore class instance for Deduplication Substore ID: '{0}'".format(
            self._substore_id
        )

    def _initialize_substore_properties(self):
        """Initialize substore properties for the substore on a deduplication store"""
        store = Store(self._commcell_object, self._storage_policy_name, self._copy_name, self._store_id)
        self._substore_properties = store._substores[self._substore_id]
        self._path = self._substore_properties['Path']
        self._media_agent = self._substore_properties['MediaAgent']['name']
        self._media_agent_id = self._substore_properties['MediaAgent']['id']

    def refresh(self):
        """refresh the properties of a substore"""
        self._initialize_substore_properties()

    def mark_for_recovery(self):
        """mark a substore for recovery and refresh substore properties"""
        request_json = {
            "EVGui_IdxSIDBSubStoreOpReq": {
                "info": {
                    "mediaAgent": {
                        "name": self.media_agent
                    },
                    "SIDBStoreId": self.store_id,
                    "SubStoreId": self.substore_id,
                    "opType": 1,
                    "path": self.path
                }
            }
        }
        self._commcell_object.qoperation_execute(request_json)
        self.refresh()

    @property
    def media_agent(self):
        """returns media agent for the substore"""
        return self._media_agent

    @property
    def media_agent_id(self):
        """returns media agent id for the substore"""
        return self._media_agent_id

    @property
    def path(self):
        """returns path for the substore"""
        return self._path

    @property
    def store_id(self):
        """returns store id for the substore"""
        return self._store_id

    @property
    def substore_id(self):
        """returns substore id"""
        return self._substore_id
