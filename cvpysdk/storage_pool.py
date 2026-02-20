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

"""File for doing operations on an Storage Pools.

This module has classes defined for doing operations for Storage Pools:

StoragePools, StoragePoolType, StorageType, WORMLockType and StoragePool are the classes defined in this file.

StoragePools: Class for representing all the StoragePools in the commcell

StoragePoolType : Class for representing storage pool types like deduplication, secondary copy, non-dedupe, scale out

StorageType : Class for representing storage types like disk, cloud, tape of a storage pool

WORMLockType : Class for representing different WORM lock types flag values of a WORM enable storage pool

StoragePool: Class for representing a single StoragePool of the commcell


StoragePools
============

    __init__(commcell_object)   --  initializes object of the StoragePools class associated with the commcell

    __str__()                   --  returns all the storage pools associated with the commcell

    __repr__()                  --  returns the string representation of an instance of this class

    __len__()                   --  returns the number of storage pools added to the Commcell

    __getitem__()               --  returns the name of the storage pool for the given storage
    pool Id or the details for the given storage pool name

    _get_storage_pools()        --  returns all storage pools added to the commcell

    has_storage_pool()          --  checks whether the storage pool  with given name exists or not

    get()                       --  returns StoragePool object of the storage pool for the
                                    specified input name

    add()                       --  Adds a storage pool, according to given input and returns
                                    StoragePool object

    delete()                    --  deletes the specified storage pool

    refresh()                   --  refresh the list of storage pools associated with the commcell

    add_air_gap_protect()       --  Adds a new air gap protect storage pool to commcell

    add_data_domain_boost_storage() -- Adds a new Data Domain Boost storage pool to commcell

    add_hpe_catalyst_storage()  --  Adds a new HPE Catalyst StoreOnce storage pool to commcell

Attributes
----------

    **all_storage_pools**   --  returns dict of all the storage pools on commcell


StoragePool
===========

    __init__()                  --  initialize the instance of StoragePool class for specific storage pool of commcell

    __repr__()                  --  returns a string representation of the StoragePool instance

     _get_storage_pool_properties() --  returns the properties of this storage pool

    refresh()                   --	Refresh the properties of the StoragePool

    get_copy()                  --  Returns the StoragePolicyCopy object of Storage Pool copy

    enable_compliance_lock()    --  Enables compliance lock on Storage Pool Copy

    enable_worm_storage_lock()  --  Enables WORM storage lock on storage pool

    hyperscale_add_nodes()      --  Add 3 new nodes to an existing storage pool

    enable_retention_lock()     --  Enables retention lock on Storage Pool Copy 

    add_media_agent()           --  Adds a media agent to the storage pool

    remove_media_agent()        --  Removes a media agent from the storage pool

StoragePool instance attributes
================================

    **storage_pool_name**           --  returns the name of the storage pool

    **storage_pool_id**             --  returns the storage pool id

    **storage_pool_properties**     --  returns the properties of the storage pool

    **global_policy_name**          --  returns the global policy corresponding to the storage pool

    **copy_name**                   --  returns the copy name of the storage pool

    **copy_id**                     --  returns the copy id of the storage pool

    **storage_pool_type**           --  returns the storage pool type

    **storage_type**                --  returns the storage type of the storage pool

    **storage_vendor**              --  returns the storage vendor id of the storage pool

    **media_agents**                --  returns the list of media agents associated with the storage pool

    **storage_media_agents**        --  returns the list of storage media agents associated with the storage pool

    **ddb_media_agents**            --  returns the list of deduplication media agents associated with the storage pool

    **media_agents_with_roles**     --  returns the list of media agents with their roles associated with the storage pool

    **store_id**                   --  returns the list of store IDs associated with the storage pool

    **library_id**                 --  returns the library ID associated with the storage pool

    **library_name**               --  returns the library name associated with the storage pool    

    **is_worm_storage_lock_enabled**--  returns whether WORM storage lock is enabled

    **is_object_level_worm_lock_enabled** --  returns whether object level WORM lock is enabled

    **is_bucket_level_worm_lock_enabled** --  returns whether bucket level WORM lock is enabled

    **is_compliance_lock_enabled**  --  returns whether compliance lock is enabled

# TODO: check with MM API team to get the response in JSON

"""
import copy
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

import xmltodict
from enum import Enum
from base64 import b64encode
from enum import IntEnum, IntFlag

if TYPE_CHECKING:
    from .commcell import Commcell

from .exception import SDKException
from .policies.storage_policies import StoragePolicyCopy

from .storage import MediaAgent
from .security.security_association import SecurityAssociation
from .constants import StoragePoolConstants

class StorageType(IntEnum):
    """
    Enumeration class to represent different storage types.

    This class inherits from IntEnum and is used to define and manage
    various storage type constants in a type-safe manner. It enables
    clear and readable code when working with different storage options,
    such as file systems, databases, or cloud storage.

    Key Features:
        - Type-safe enumeration of storage types
        - Improved code readability and maintainability
        - Facilitates storage type comparisons and assignments

    #ai-gen-doc
    """
    DISK = 1,
    CLOUD = 2,
    HYPERSCALE = 3,
    TAPE = 4

class StoragePools:
    """
    Manages operations related to Storage Pools within a CommCell environment.

    The StoragePools class provides a comprehensive interface for interacting with storage pools,
    including creation, deletion, retrieval, and management of various storage pool types such as
    hyperscale, air gap protected, and data domain boost storage pools. It supports querying storage
    pools by name, ID, or company, and offers utility methods for refreshing and listing all available
    storage pools.

    Key Features:
        - Initialize with a CommCell object for context
        - Retrieve storage pool information by name, ID, or company
        - List all storage pools via property access
        - Check for existence of a storage pool by name
        - Create hyperscale storage pools with specified media agents
        - Add air gap protected storage pools with detailed configuration
        - Retrieve air gap protection details for a company
        - Add Data Domain Boost storage pools with credentials and configuration
        - Add generic storage pools with mount paths and deduplication settings
        - Delete storage pools by name
        - Refresh the storage pool list to reflect current state
        - Supports Python container protocols (__len__, __getitem__, __str__, __repr__)

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a StoragePools instance for managing storage pool operations.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> storage_pools = StoragePools(commcell)
            >>> print("StoragePools instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._add_storage_pool_api = self._services['ADD_STORAGE_POOL']

        self._storage_pools_api = self._services['STORAGE_POOL']

        self._metallic_storage_api = self._services['GET_METALLIC_STORAGE_DETAILS']
        self.__get_agp_storage_api = self._services['GET_AGP_STORAGE']
        self._storage_pools = None

        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all storage pools present in the Commcell.

        This method provides a human-readable summary of all storage pools managed by the StoragePools object.

        Returns:
            A string listing all storage pools associated with the Commcell.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> print(str(storage_pools))
            Storage Pool 1, Storage Pool 2, Storage Pool 3

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^40}\n\n'.format('S. No.', 'Storage Pool')

        for index, storage_pool in enumerate(self._storage_pools):
            sub_str = '{:^5}\t{:40}\n'.format(index + 1, storage_pool)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the StoragePools instance.

        This method provides a developer-friendly string that represents the current
        StoragePools object, which can be useful for debugging and logging purposes.

        Returns:
            A string representation of the StoragePools instance.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> print(repr(storage_pools))
            <StoragePools object at 0x7f8c2b1e2d30>

        #ai-gen-doc
        """
        return "StoragePools class instance for Commcell"

    def __len__(self) -> int:
        """Return the number of storage pools added to the Commcell.

        This method allows you to use the built-in `len()` function to determine 
        how many storage pools are currently managed by this StoragePools instance.

        Returns:
            The total number of storage pools as an integer.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> count = len(storage_pools)
            >>> print(f"Number of storage pools: {count}")
        #ai-gen-doc
        """
        return len(self.all_storage_pools)

    def __getitem__(self, value: Union[str, int]) -> Union[str, dict]:
        """Retrieve storage pool information by name or ID.

        If a storage pool ID (int) is provided, returns the name of the storage pool.
        If a storage pool name (str) is provided, returns a dictionary with details of the storage pool.

        Args:
            value: The name (str) or ID (int) of the storage pool to retrieve.

        Returns:
            str: The name of the storage pool if an ID was provided.
            dict: A dictionary containing details of the storage pool if a name was provided.

        Raises:
            IndexError: If no storage pool exists with the given name or ID.

        Example:
            >>> pools = StoragePools()
            >>> # Get storage pool details by name
            >>> details = pools['PrimaryPool']
            >>> print(details)
            {'id': 101, 'name': 'PrimaryPool', 'size': '10TB'}
            >>> # Get storage pool name by ID
            >>> name = pools[101]
            >>> print(name)
            'PrimaryPool'

        #ai-gen-doc
        """
        value = str(value)

        if value in self.all_storage_pools:
            return self.all_storage_pools[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_storage_pools.items()))[0][0]
            except IndexError:
                raise IndexError('No storage pool exists with the given Name / Id')

    def _get_storage_pools(self) -> Dict[str, int]:
        """Retrieve all storage pools associated with the Commcell environment.

        Returns:
            Dict[str, int]: A dictionary mapping storage pool names to their corresponding IDs.
            Example:
                {
                    "storage_pool1_name": 123,
                    "storage_pool2_name": 456
                }

        Raises:
            SDKException: If the response from the Commcell is empty or not successful.

        Example:
            >>> storage_pools = storage_pools_obj._get_storage_pools()
            >>> print(storage_pools)
            {'PrimaryPool': 101, 'ArchivePool': 102}
            >>> # Access a specific storage pool ID
            >>> pool_id = storage_pools.get('PrimaryPool')
            >>> print(f"PrimaryPool ID: {pool_id}")

        #ai-gen-doc
        """
        headers = self._commcell_object._headers.copy()
        headers['Accept'] = 'application/xml'

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._storage_pools_api, headers=headers
        )

        if flag:
            storage_pools = {}

            response = xmltodict.parse(response.text)['Api_GetStoragePoolListResp']

            if response is None or response.get('storagePoolList') is None:
                storage_pool_list = []
            else:
                storage_pool_list = response['storagePoolList']

            if not isinstance(storage_pool_list, list):
                storage_pool_list = [storage_pool_list]

            if response:
                for pool in storage_pool_list:
                    name = pool['storagePoolEntity']['@storagePoolName'].lower()
                    storage_pool_id = pool['storagePoolEntity']['@storagePoolId']

                    storage_pools[name] = storage_pool_id

                return storage_pools
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
    
    def get_storage_pools_for_a_company(self, company_id: int, storage_type: 'StorageType' = None) -> dict:
        """Retrieve all storage pools associated with a specific company in the Commcell environment.

        Args:
            company_id: The unique identifier of the company for which the associated storage pools are to be fetched.
            storage_type: Optional; a StorageType object to filter storage pools by type.

        Returns:
            A dictionary mapping storage pool names to their corresponding IDs. For example:
                {
                    "storage_pool1_name": storage_pool1_id,
                    "storage_pool2_name": storage_pool2_id
                }

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> pools = storage_pools.get_storage_pools_for_a_company(company_id=123)
            >>> print(pools)
            {'PrimaryPool': 101, 'ArchivePool': 102}

            >>> # With storage type filter
            >>> pools = storage_pools.get_storage_pools_for_a_company(123, storage_type=my_storage_type)
            >>> print(pools)
            {'PrimaryPool': 101}

        #ai-gen-doc
        """
        headers = self._commcell_object._headers.copy()
        headers['Accept'] = 'application/json'
        headers['onlygetcompanyownedentities'] = '1'
        headers['operatorcompanyid'] = f'{company_id}'

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._storage_pools_api, headers=headers
        )

        if flag:
            storage_pools = {}
            response = response.json()
            if response is None or response.get('storagePoolList') is None:
                storage_pool_list = []
            else:
                storage_pool_list = response['storagePoolList']
            if not isinstance(storage_pool_list, list):
                storage_pool_list = [storage_pool_list]
            if response:
                for pool in storage_pool_list:
                    if storage_type and pool['storageType'] != storage_type:
                        continue
                    # skip agp pools for cloud storage type
                    if storage_type == StorageType.CLOUD and 401 <= pool['libraryVendorType'] <= 499:
                        continue
                    name = pool['storagePoolEntity']['storagePoolName']
                    storage_pool_id = pool['storagePoolEntity']['storagePoolId']

                    storage_pools[name] = storage_pool_id

            return storage_pools
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_storage_pools(self) -> Dict[str, int]:
        """Get a dictionary of all storage pools available on this Commcell.

        Returns:
            Dict[str, int]: A dictionary mapping storage pool names to their corresponding IDs.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> pools_dict = storage_pools.all_storage_pools
            >>> print(pools_dict)
            {'PrimaryPool': 101, 'ArchivePool': 102}

        #ai-gen-doc
        """
        return self._storage_pools

    def has_storage_pool(self, name: str) -> bool:
        """Check if a storage pool with the specified name exists in the Commcell.

        Args:
            name: The name of the storage pool to check.

        Returns:
            True if the storage pool exists in the Commcell, False otherwise.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> exists = storage_pools.has_storage_pool("PrimaryPool")
            >>> print(f"Storage pool exists: {exists}")
            >>> # Output: Storage pool exists: True (if the pool exists)

        #ai-gen-doc
        """
        return self._storage_pools and name.lower() in self._storage_pools

    def get(self, name: str) -> 'StoragePool':
        """Retrieve the ID of a storage pool by its name.

        Args:
            name: The name of the storage pool whose ID is to be retrieved.

        Returns:
            StoragePool class instance for the given storage pool name.

        Raises:
            SDKException: If no storage pool exists with the given name.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> pool_id = storage_pools.get("PrimaryPool")
            >>> print(f"Storage pool ID: {pool_id}")

        #ai-gen-doc
        """
        self.refresh()
        name = name.lower()

        if self.has_storage_pool(name):
            return StoragePool(self._commcell_object, name, storage_pool_id=self._storage_pools[name])
        else:
            raise SDKException('StoragePool', '103')

    def hyperscale_create_storage_pool(self, storage_pool_name: str, media_agents: list) -> 'StoragePool':
        """Create a new storage pool for HyperScale environments.

        Args:
            storage_pool_name: The name of the storage pool to create.
            media_agents: A list of 3 media agents, specified either by their names (str) or as media agent objects.

                Example:
                    ["ma1", "ma2", "ma3"]

        Returns:
            StoragePool: The created StoragePool object if creation is successful.

        Example:
            >>> storage_pools = StoragePools()
            >>> flag, response = storage_pools.hyperscale_create_storage_pool("HS_Pool1", ["ma1", "ma2", "ma3"])
            >>> if flag:
            ...     print("Storage pool created successfully.")
            ... else:
            ...     print("Failed to create storage pool:", response)

        #ai-gen-doc
        """

        if not isinstance(media_agents, list):
            raise SDKException('Storage', '101')
        if not isinstance(storage_pool_name, str):
            raise SDKException('Storage', '101')

        mediagent_obj = []
        for media_agent in media_agents:
            if isinstance(media_agent, MediaAgent):
                mediagent_obj.append(media_agent)
            elif isinstance(media_agent, str):
                mediagent_obj.append(self._commcell_object.media_agents.get(media_agent))
            else:
                raise SDKException('Storage', '103')
        if len(mediagent_obj) <= 2:
            raise SDKException('Storage', '102', "minimum 3 media agents are required")

        request_xml = """<App_CreateStoragePolicyReq storagePolicyName="{0}" copyName="{0}_Primary" type="1"
                                     numberOfCopies="1">
                                    <storagePolicyCopyInfo>
                                        <storagePolicyFlags scaleOutStoragePolicy="1"/>
                                    </storagePolicyCopyInfo>
                                    <storage>
                                        <mediaAgent mediaAgentId="{4}" mediaAgentName="{1}" displayName="{1}"/>
                                    </storage>
                                    <storage>
                                        <mediaAgent mediaAgentId="{5}" mediaAgentName="{2}" displayName="{2}"/>
                                    </storage>
                                    <storage>
                                        <mediaAgent mediaAgentId="{6}" mediaAgentName="{3}" displayName="{3}"/>
                                    </storage>
                                    <scaleoutConfiguration configurationType="1"/>
                                </App_CreateStoragePolicyReq>
                                """.format(storage_pool_name, mediagent_obj[0].media_agent_name,
                                           mediagent_obj[1].media_agent_name, mediagent_obj[2].media_agent_name,
                                           mediagent_obj[0].media_agent_id, mediagent_obj[1].media_agent_id,
                                           mediagent_obj[2].media_agent_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._add_storage_pool_api, request_xml
        )
        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if int(error_code) != 0:
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create storage pool\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
        return self.get(storage_pool_name)

    def add_air_gap_protect(
        self,
        storage_pool_name: str,
        media_agent: Union[str, object],
        storage_type: str,
        storage_class: str,
        region_name: str,
        ddb_ma: Optional[Union[List[Union[str, object]], str, object]] = None,
        dedup_path: Optional[Union[List[str], str]] = None
    ) -> 'StoragePool':
        """Add a new air gap protect storage pool to the Commcell.

        This method creates a storage pool with air gap protection using the specified parameters.
        The storage pool can be configured with a media agent, cloud vendor type, storage class, region,
        and optional deduplication media agent and deduplication path.

        Args:
            storage_pool_name: Name of the new storage pool to add.
            media_agent: Name (str) or instance (object) of the media agent.
            storage_type: Name of the cloud vendor (e.g., "Microsoft Azure storage").
            storage_class: Storage class (e.g., "Hot", "Cool").
            region_name: Name of the geographical region for storage.
            ddb_ma: Optional; list of names or instances, or a single name or instance of deduplication media agent.
            dedup_path: Optional; list of paths or a single path where the DDB should be stored.

        Returns:
            StoragePool: The created StoragePool object if creation is successful.

        Raises:
            SDKException: If invalid parameters are provided.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> pool = storage_pools.add_air_gap_protect(
            ...     storage_pool_name="AirGapPool1",
            ...     media_agent="MediaAgent01",
            ...     storage_type="Microsoft Azure storage",
            ...     storage_class="Hot",
            ...     region_name="East US",
            ...     ddb_ma=["DedupeMA01", "DedupeMA02"],
            ...     dedup_path=["/data/ddb1", "/data/ddb2"]
            ... )
            >>> print(f"Created storage pool: {pool}")

        #ai-gen-doc
        """
        license_type_dict = StoragePoolConstants.AIR_GAP_PROTECT_STORAGE_TYPES
        error_message = ""

        # to support backward compatibility
        if storage_class.upper() == "HOT":
            storage_class="FREQUENT ACCESS"
        elif storage_class.upper() == "COOL":
            storage_class="INFREQUENT ACCESS"

        if storage_type.upper() in license_type_dict:
            available_storage_classes = license_type_dict[storage_type.upper()]
            if storage_class.upper() in available_storage_classes:
                vendor_id = available_storage_classes[storage_class.upper()]["vendorId"]
                display_vendor_id = available_storage_classes[storage_class.upper()]["displayVendorId"]
            else:
                error_message += f"Invalid storage class provided. Valid storage class {list(available_storage_classes.keys())}"
        else:
            error_message += f"  Invalid storage type provided. {list(license_type_dict.keys())}"

        if error_message:
            raise SDKException('Storage', '101', error_message)

        region = None
        available_regions = []

        #  API call to fetch the region name - sourced directly from the vendor
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._metallic_storage_api)
        if flag:
            if response.json():
                if "storageInformation" in response.json():
                    for storage_info in response.json()["storageInformation"]:
                        if (int(storage_info["vendorId"]) == int(vendor_id)) and (int(storage_info["displayVendorId"]) == int(display_vendor_id)):
                            for region_dict in storage_info["region"]:
                                available_regions.append(region_dict["displayName"])
                                if region_dict["displayName"] == region_name:
                                    region = region_dict["regionName"]
                                    break

                        if region:
                            break

                    if region is None:
                        if not available_regions:
                            raise SDKException('Storage', '101',
                                               f"Active license is required to configure {storage_type} - {storage_class} Air Gap Protect storage")
                        else:
                            raise SDKException('Storage', '101',
                                               f"Invalid region: {region_name} ,\nValid regions: {available_regions}")
                else:
                    raise SDKException('Storage', '101', "Unexpected response returned while fetching Air Gap Protect storage details")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        # cloud server type for air gap protect is 400
        cloud_server_type = 400

        return self.add(storage_pool_name=storage_pool_name, mountpath=None, media_agent=media_agent, ddb_ma=ddb_ma,
                        dedup_path=dedup_path, cloud_server_type=cloud_server_type, region=region, vendor_id=vendor_id,
                        display_vendor_id=display_vendor_id)
        
    def get_air_gap_protect(self, company_id: int = None) -> dict:
        """Retrieve a dictionary of air gap protect storage pools in the Commcell.

        If a company ID is provided, only storage pools associated with that company are returned.
        If no company ID is specified, all air gap protect storage pools in the Commcell are returned.

        Args:
            company_id: Optional; The ID of the company to filter storage pools by. If None, returns all air gap protect storage pools.

        Returns:
            A dictionary mapping storage pool names to their corresponding IDs.
            Example:
                {
                    "storage_pool1_name": 123,
                    "storage_pool2_name": 456
                }

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> air_gap_pools = storage_pools.get_air_gap_protect()
            >>> print(air_gap_pools)
            {'SecurePoolA': 101, 'SecurePoolB': 102}

            >>> # To get air gap protect storage pools for a specific company
            >>> company_pools = storage_pools.get_air_gap_protect(company_id=5)
            >>> print(company_pools)
            {'CompanyPoolX': 201}

        #ai-gen-doc
        """
        headers = self._commcell_object._headers.copy()
        headers['Accept'] = 'application/json'
        if company_id:
            headers['onlygetcompanyownedentities'] = '1'
            headers['operatorcompanyid'] = f'{company_id}'

        flag, response = self._cvpysdk_object.make_request(
            'GET', self.__get_agp_storage_api, headers=headers
        )

        if flag:
            storage_pools = {}
            response = response.json()
            if response is None or response.get('cloudStorage') is None:
                storage_pool_list = []
            else:
                storage_pool_list = response['cloudStorage']
            if not isinstance(storage_pool_list, list):
                storage_pool_list = [storage_pool_list]
            if response:
                for pool in storage_pool_list:
                    name = pool['name']
                    storage_pool_id = pool['id']

                    storage_pools[name] = storage_pool_id

            return storage_pools
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
    
    def add_hpe_catalyst_storage(self, storage_pool_name, storeonce_host, media_agent, username, password, store):
        """Adds a new HPE Catalyst storage pool to commcell

        Args:
            storage_pool_name (str) -- name of the new storage pool to add

            storeonce_host (str) -- hostname or IP address of the StoreOnce server

            media_agent (str/object) -- name or instance of media agent

            username (str) -- username to access the StoreOnce server

            password (str) -- password to access the StoreOnce server

            store (str) -- name of the store on the StoreOnce server

        Returns:
            StoragePool object if creation is successful
        
        Raises:
            SDKException if creation is unsuccessful
        """
        username = storeonce_host+"//"+username
        return self.add(storage_pool_name=storage_pool_name, mountpath=store, media_agent=media_agent, cloud_server_type=59, username=username, password=password, library_name=store, region_id = 0)
        
    def add_data_domain_boost_storage(
        self,
        type: str,
        storage_pool_name: str,
        media_agent: Union[str, object],
        data_domain_host: str,
        storage_unit: str,
        credential_name: str,
        ddb_ma: Optional[Union[List[Union[str, object]], str, object]] = None
    ) -> 'StoragePool':
        """Add a new Data Domain Boost storage pool to the Commcell.

        This method creates a Data Domain Boost storage pool, allowing integration with a Data Domain server
        for optimized backup and deduplication. The storage pool can be configured as either an 'access' or 'client' type.

        Args:
            type: String representing the type of Data Domain Boost storage pool to add ('access' or 'client').
            storage_pool_name: Name of the new storage pool to be created.
            media_agent: Name or instance of the Media Agent to associate with the storage pool.
            data_domain_host: Hostname or IP address of the Data Domain server.
            storage_unit: Name of the storage unit on the Data Domain server.
            credential_name: Name of the saved credential used to access the Data Domain server.
            ddb_ma: (Optional) Name, instance, or list of names/instances of deduplication Media Agents.

        Returns:
            StoragePool: The StoragePool object representing the newly created storage pool.

        Raises:
            SDKException: If the storage pool creation is unsuccessful.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> pool = storage_pools.add_data_domain_boost_storage(
            ...     type=1,
            ...     storage_pool_name="DD_Boost_Pool",
            ...     media_agent="MediaAgent01",
            ...     data_domain_host="dd.example.com",
            ...     storage_unit="Backup_Unit",
            ...     credential_name="DD_Credential",
            ...     ddb_ma="DedupeMA01"
            ... )
            >>> print(f"Created storage pool: {pool}")

        #ai-gen-doc
        """
        dedup_path = None
        if type == 'access':
            cloud_server_type = 300
            dedup_path = ''
        elif type == 'client':
            cloud_server_type = 58
            if ddb_ma is not None:
                raise SDKException('Storage', '101', 'DDB media agents are not supported for client type storage pool')
        else:
            raise SDKException('Storage', '101', 'Invalid type provided. Valid types are "access" or "client".')
        username = data_domain_host+"//__CVCRED__"
        return self.add(storage_pool_name=storage_pool_name, mountpath=storage_unit, media_agent=media_agent,ddb_ma =ddb_ma, dedup_path= dedup_path, cloud_server_type = cloud_server_type, credential_name=credential_name, username=username, library_name=storage_unit)

    def add(
        self,
        storage_pool_name: str,
        mountpath: str,
        media_agent: Union[str, object],
        ddb_ma: Optional[Union[List[Union[str, object]], str, object]] = None,
        dedup_path: Optional[Union[str, List[str]]] = None,
        **kwargs: Any
    ) -> 'StoragePool':
        """Add a new storage pool to the Commcell environment.

        This method creates a new storage pool with the specified parameters, including mount path, media agent, 
        deduplication media agent, and deduplication path. Additional configuration options can be provided via keyword arguments.

        Args:
            storage_pool_name: Name of the new storage pool to add.
            mountpath: Mount path for the storage pool.
            media_agent: Name or instance of the media agent to associate with the storage pool.
            ddb_ma: (Optional) Name, instance, or list of names/instances of the deduplication media agent(s).
            dedup_path: (Optional) Path or list of paths where the DDB (Deduplication Database) should be stored.
            **kwargs: Additional optional parameters for storage pool creation, such as:
                - username (str): Username to access the mount path.
                - password (str): Password to access the mount path.
                - credential_name (str): Credential manager name.
                - cloud_server_type (int): Cloud vendor server type. Please refer to mediaagentconstants.CLOUD_SERVER_TYPES to fetch the required ID.
                - region (str): Geographical region for storage.
                - vendor_id (int): Cloud vendor ID (e.g., 3 for Azure).
                - display_vendor_id (int): Storage class ID for the vendor (e.g., 401 for Azure Hot).
                - region_id (int): Cloud hypervisor-specific region ID.
                - tape_storage (bool): Whether the library is a tape library.

        Returns:
            StoragePool: The created StoragePool object if creation is successful.

        Raises:
            Exception: If the storage pool creation is unsuccessful.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> pool = storage_pools.add(
            ...     storage_pool_name="NewPool",
            ...     mountpath="/mnt/storage",
            ...     media_agent="MediaAgent01",
            ...     ddb_ma="DedupeMA01",
            ...     dedup_path="/mnt/ddb",
            ...     username="user",
            ...     password="pass"
            ... )
            >>> print(f"Storage pool created: {pool}")

        #ai-gen-doc
        """
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        credential_name = kwargs.get('credential_name', None)
        cloud_server_type = kwargs.get('cloud_server_type', None)
        library_name = kwargs.get('library_name', None)
        tape_storage = False

        region = kwargs.get('region', None)
        vendor_id = kwargs.get('vendor_id', None)
        display_vendor_id = kwargs.get('display_vendor_id', None)
        region_id = kwargs.get('region_id', None)

        if library_name and (cloud_server_type is None or cloud_server_type not in (300, 58, 59)):
            library_object = self._commcell_object.disk_libraries.get(library_name)
            library_type = library_object.library_properties.get('libraryType', None)
            tape_storage = True if library_type == 1 else tape_storage


        if ((ddb_ma is not None and not (isinstance(dedup_path, str) or isinstance(dedup_path, list))) or
                not (isinstance(storage_pool_name, str) or not isinstance(mountpath, str))):
            raise SDKException('Storage', '101')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, str):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        else:
            raise SDKException('Storage', '103')

        if (isinstance(ddb_ma, str) or isinstance(ddb_ma, MediaAgent)) and isinstance(dedup_path, str):
            ddb_ma = [ddb_ma]
            dedup_path = [dedup_path]

        if isinstance(ddb_ma, list) and isinstance(dedup_path, list):
            if len(ddb_ma) != len(dedup_path):
                raise SDKException('Storage', '101')

        if library_name is not None and mountpath != '' and (cloud_server_type is None or cloud_server_type not in (300, 58, 59)):
            raise SDKException('Storage', '101')

        if ddb_ma is not None and (len(ddb_ma) > 6 or len(dedup_path) > 6):
            raise SDKException('Storage', '110')

        if ddb_ma is not None:
            for i in range(len(ddb_ma)):
                if isinstance(ddb_ma[i], MediaAgent):
                    ddb_ma[i] = ddb_ma[i]
                elif isinstance(ddb_ma[i], str):
                    ddb_ma[i] = MediaAgent(self._commcell_object, ddb_ma[i])
                else:
                    raise SDKException('Storage', '103')

        request_json = {
            "storagePolicyName": storage_pool_name,
            "type": "CVA_REGULAR_SP",
            "copyName": "Primary",
            "numberOfCopies": 1,
            "storage": [
                {
                    "path": mountpath,
                    "mediaAgent": {
                        "mediaAgentId": int(media_agent.media_agent_id),
                        "mediaAgentName": media_agent.media_agent_name
                    }
                }
            ],
            "storagePolicyCopyInfo": {
                "copyType": "SYNCHRONOUS",
                "isFromGui": True,
                "active": "SET_TRUE",
                "isDefault": "SET_TRUE",
                "numberOfStreamsToCombine": 1,
                "retentionRules": {
                    "retentionFlags": {
                        "enableDataAging": "SET_TRUE"
                    },
                    "retainBackupDataForDays": -1,
                    "retainBackupDataForCycles": -1,
                    "retainArchiverDataForDays": -1
                },
                "library": {
                    "libraryId": 0,
                },
                "mediaAgent": {
                    "mediaAgentId": int(media_agent.media_agent_id),
                    "mediaAgentName": media_agent.media_agent_name
                }
            }
        }

        if cloud_server_type and int(cloud_server_type) > 0:
            request_json["storage"][0]["deviceType"] = cloud_server_type

        if region_id is not None:
            request_json["storage"][0]["metallicStorageInfo"] = {
                "region": [
                    {
                        "regionId": region_id
                    }
                ],
                "storageClass": [
                    "CONTAINER_DEFAULT"
                ],
                "replication": [
                    "NONE"
                ]
            }
            if cloud_server_type != 59: # not for HPE Catalyst
                request_json["region"] = {"regionId": region_id}

        if username is not None:
            request_json["storage"][0]["credentials"] = {"userName": username}

        if password is not None:
            request_json["storage"][0]["credentials"]["password"] = b64encode(password.encode()).decode()

        if credential_name is not None:
            request_json["storage"][0]["savedCredential"] = {"credentialName": credential_name}

        if library_name is not None and (cloud_server_type is None or cloud_server_type not in (300, 58, 59)):
            request_json["storage"] = []
            request_json["storagePolicyCopyInfo"]["library"]["libraryName"] = library_name

        if ddb_ma is not None or dedup_path is not None:
            maInfoList = []
            for ma, path in zip(ddb_ma, dedup_path):
                maInfoList.append({
                    "mediaAgent": {
                        "mediaAgentId": int(ma.media_agent_id),
                        "mediaAgentName": ma.media_agent_name
                    },
                    "subStoreList": [
                        {
                            "accessPath": {
                                "path": path
                            },
                            "diskFreeThresholdMB": 5120,
                            "diskFreeWarningThreshholdMB": 10240
                        }]
                })

            request_json["storagePolicyCopyInfo"].update({
                "storagePolicyFlags": {
                    "blockLevelDedup": "SET_TRUE",
                    "enableGlobalDeduplication": "SET_TRUE"
                },
                "dedupeFlags": {
                    "enableDeduplication": "SET_TRUE",
                    "enableDASHFull": "SET_TRUE",
                    "hostGlobalDedupStore": "SET_TRUE"
                },
                "DDBPartitionInfo": {
                    "maInfoList": maInfoList
                }
            })
        elif tape_storage:
            request_json["storagePolicyCopyInfo"].update({
                "storagePolicyFlags": {
                    "globalAuxCopyPolicy": "SET_TRUE"
                },
                "copyFlags": {
                    "preserveEncryptionModeAsInSource": "SET_TRUE"
                },
                "extendedFlags": {
                    "globalAuxCopyPolicy": "SET_TRUE"
                }
            })
        else:
            request_json["storagePolicyCopyInfo"].update({
                "storagePolicyFlags": {
                    "globalStoragePolicy": "SET_TRUE"
                },
                "copyFlags": {
                    "preserveEncryptionModeAsInSource": "SET_TRUE"
                },
                "extendedFlags": {
                    "globalStoragePolicy": "SET_TRUE"
                }
            })

        # air gap protect storage
        if cloud_server_type == 400:
            del request_json["storage"][0]["path"]
            request_json["storage"][0]["savedCredential"] = {"credentialId": 0}

            metallic_Storage = {
                "region": [
                    {
                        "regionName": region
                    }
                ],
                "displayVendorId": display_vendor_id,
                "vendorId": vendor_id
            }
            request_json["storage"][0]["metallicStorageInfo"] = metallic_Storage
        
        if cloud_server_type == 59: # HPE Catalyst
            request_json["storage"][0]["savedCredential"] = {"credentialId": 0}

        
        #data domain boost storage (300, 58) and HPE Catalyst (59)
        if cloud_server_type in (300, 58, 59):
            request_json["storagePolicyCopyInfo"]["library"]["libraryName"] = library_name
            request_json["clientGroup"] = {"clientGroupId": 0}

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._add_storage_pool_api, request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if int(error_code) != 0:
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create storage pool\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
        self._commcell_object.disk_libraries.refresh()
        return self.get(storage_pool_name)

    def delete(self, storage_pool_name: str) -> None:
        """Delete the specified storage pool by name.

        Args:
            storage_pool_name: The name of the storage pool to delete.

        Raises:
            SDKException: If the storage pool name is not a string, if the deletion fails,
                if no storage pool exists with the given name, if the response is empty,
                or if the response indicates failure.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> storage_pools.delete("PrimaryPool")
            >>> print("Storage pool 'PrimaryPool' deleted successfully.")

        #ai-gen-doc
        """

        if not isinstance(storage_pool_name, str):
            raise SDKException('Storage', '101')
        else:
            storage_pool_name = storage_pool_name.lower()

            if self.has_storage_pool(storage_pool_name):
                storage_pool_id = self._storage_pools[storage_pool_name]

                delete_storage_pool = self._services['DELETE_STORAGE_POOL'] % (storage_pool_id)

                flag, response = self._cvpysdk_object.make_request('DELETE', delete_storage_pool)

                if flag:
                    error_code = response.json()['error']['errorCode']
                    if int(error_code) != 0:
                        error_message = response.json()['error']['errorMessage']
                        o_str = f'Failed to delete storage pools {storage_pool_name}'
                        o_str += '\nError: "{0}"'.format(error_message)
                        raise SDKException('Storage', '102', o_str)
                    else:
                        # initialize the storage pool again
                        # so the storage pool object has all the storage pools
                        self.refresh()
                        # as part of storage pool we might delete library so initialize the libraries again
                        self._commcell_object.disk_libraries.refresh()
                else:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'Storage',
                    '102',
                    'No storage pool exists with name: {0}'.format(storage_pool_name)
                )
    def refresh(self) -> None:
        """Reload the list of storage pools associated with the Commcell.

        This method clears any cached storage pool data, ensuring that subsequent accesses
        retrieve the most up-to-date information from the Commcell.

        Example:
            >>> storage_pools = StoragePools(commcell_object)
            >>> storage_pools.refresh()  # Refresh the storage pool list
            >>> print("Storage pools refreshed successfully")

        #ai-gen-doc
        """
        self._storage_pools = self._get_storage_pools()

class StoragePoolType(IntEnum):
    """
    Enumeration class representing different types of storage pools.

    This class extends IntEnum to provide a set of named constants for
    identifying various storage pool types in a type-safe manner. It is
    typically used to categorize and manage storage resources within
    applications or systems that require explicit pool type identification.

    Key Features:
        - Type-safe enumeration of storage pool types
        - Facilitates clear and maintainable code for storage management
        - Integrates seamlessly with integer-based logic and comparisons

    #ai-gen-doc
    """
    DEDUPLICATION = 1,
    SECONDARY_COPY = 2,
    NON_DEDUPLICATION = 3,
    SCALE_OUT = 4

class ManageMediaAgentActionType(Enum):
    """
    Enumeration class to represent different actions for managing media agents in a storage pool.

    This class inherits from Enum and is used to define and manage various media agent actions
    in a type-safe manner. It enables clear and readable code when working with different media
    agent operations, such as adding, removing, or updating media agents.

    Key Features:
        - Type-safe enumeration of media agent actions
        - Improved code readability and maintainability
        - Facilitates media agent action comparisons and assignments

    #ai-gen-doc
    """
    ADD_DDB = "ADD_DDB_ROLE"
    ADD_STORAGE = "ADD_STORAGE_ROLE"
    ADD_DDB_STORAGE = "ADD_DDB_STORAGE_ROLE"
    REMOVE_DDB = "REMOVE_DDB_ROLE"
    REMOVE_STORAGE = "REMOVE_STORAGE_ROLE"
    REMOVE_DDB_STORAGE = "REMOVE_DDB_STORAGE_ROLE"

class WORMLockType(IntFlag):
    """
    IntFlag class representing various WORM (Write Once Read Many) lock types.

    This class is designed to define and manage different flag values associated
    with WORM lock types, enabling bitwise operations for combining and checking
    lock states. It is typically used in scenarios where immutable data storage
    and access control are required.

    Key Features:
        - Represents WORM lock types as integer flags
        - Supports bitwise operations for flag combination and checking
        - Facilitates clear and type-safe management of lock states

    #ai-gen-doc
    """
    COPY = 1,  # copy level software WORM (compliance lock)
    STORAGE = 2,  # storage level hardware WORM
    OBJECT = 4,  # object level storage WORM
    BUCKET = 8  # bucket level storage WORM


class StoragePool(object):
    """
    Represents an individual storage pool within a CommCell environment.

    This class provides comprehensive management and configuration capabilities for storage pools,
    including property retrieval, copy management, WORM and compliance lock features, and
    hyperscale storage operations. It exposes various properties to access storage pool details
    such as name, ID, type, vendor, and lock statuses. Additionally, it offers methods to manage
    storage pool copies, enable security features, refresh properties, and update security associations.

    Key Features:
        - Access storage pool properties (name, ID, type, vendor, lock statuses)
        - Retrieve and manage storage pool copies
        - Enable compliance and WORM storage locks with configurable retention
        - Hyperscale storage operations: add nodes, reconfigure pools, replace disks
        - Refresh storage pool information
        - Update security associations for users and external groups

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', storage_pool_name: str, storage_pool_id: int = None) -> None:
        """Initialize a StoragePool instance.

        Args:
            commcell_object: An instance of the Commcell class representing the connected Commcell.
            storage_pool_name: The name of the storage pool to manage.
            storage_pool_id: Optional; the unique identifier of the storage pool. If not provided, it may be determined automatically.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> storage_pool = StoragePool(commcell, 'PrimaryPool')
            >>> # Optionally, specify the storage pool ID
            >>> storage_pool_with_id = StoragePool(commcell, 'PrimaryPool', storage_pool_id=101)

        #ai-gen-doc
        """
        self._storage_pool_name = storage_pool_name.lower()
        self._commcell_object = commcell_object
        self._storage_pool_properties = None
        self._storage_pool_id = None
        self._copy_id = None
        self._copy_name = None

        if storage_pool_id:
            self._storage_pool_id = str(storage_pool_id)
        else:
            self._storage_pool_id = self._commcell_object.storage_pools.get(self._storage_pool_name).storage_pool_id

        self._STORAGE_POOL = self._commcell_object._services['GET_STORAGE_POOL'] % (self.storage_pool_id)
        self.refresh()

        self._copy_id = self._storage_pool_properties.get("storagePoolDetails", {}).get("copyInfo", {}).get(
            "StoragePolicyCopy", {}).get("copyId")
        self._copy_name = self._storage_pool_properties.get("storagePoolDetails", {}).get("copyInfo", {}).get(
            "StoragePolicyCopy", {}).get("copyName")

    def __repr__(self) -> str:
        """Return a string representation of the StoragePool instance.

        This method provides a developer-friendly string that can be used to 
        identify the StoragePool object, typically including key identifying information.

        Returns:
            A string representation of the StoragePool instance.

        Example:
            >>> pool = StoragePool(...)
            >>> print(repr(pool))
            <StoragePool object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        representation_string = "Storage Pool class Instance for {0}".format(self._storage_pool_name)
        return representation_string

    def _get_storage_pool_properties(self) -> None:
        """Retrieve the properties of the StoragePool.

        This method fetches and returns the properties associated with the current StoragePool instance.

        Raises:
            SDKException: If the response is empty or the response indicates failure.

        Example:
            >>> storage_pool = StoragePool(commcell_object, pool_id)
            >>> properties = storage_pool._get_storage_pool_properties()
            >>> print(properties)
            >>> # Access specific property values
            >>> pool_name = properties.get('name')
            >>> print(f"Storage pool name: {pool_name}")

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._STORAGE_POOL)

        if flag:
            if response.json():
                self._storage_pool_properties = response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
    
    def _get_ddb_media_agents(self) -> list:
        """Retrieve the list of DDB media agents associated with the storage pool.

        This method fetches and returns a list of DDB media agents configured for the current StoragePool instance.

        Returns:
            list: A list of DDB media agents.

        #ai-gen-doc
        """
        ddb_media_agents = []
        try:
            ma_info_list = self._storage_pool_properties["storagePoolDetails"]["mediaAgents"]
            for ma_info in ma_info_list:
                if ma_info.get('bDDBMA'):
                    ddb_media_agents.append(ma_info['mediaAgent']['mediaAgentName'])
        except KeyError:
            pass
        return ddb_media_agents

    def _get_storage_media_agents(self) -> list:
        """Retrieve the list of storage media agents associated with the storage pool.

        This method fetches and returns a list of storage media agents configured for the current StoragePool instance.

        Returns:
            list: A list of storage media agents.

        #ai-gen-doc
        """
        storage_media_agents = []
        try:
            ma_info_list = self._storage_pool_properties["storagePoolDetails"]["mediaAgents"]
            for ma_info in ma_info_list:
                if ma_info.get('bStorageMA'):
                    storage_media_agents.append(ma_info['mediaAgent']['mediaAgentName'])
        except KeyError:
            pass
        return storage_media_agents
    

    @property
    def storage_pool_name(self) -> str:
        """Get the name of the storage pool as a read-only property.

        Returns:
            The name of the storage pool as a string.

        Example:
            >>> storage_pool = StoragePool()
            >>> name = storage_pool.storage_pool_name  # Access the storage pool name property
            >>> print(f"Storage pool name: {name}")

        #ai-gen-doc
        """
        return self._storage_pool_name

    @property
    def storage_pool_id(self) -> str:
        """Get the unique identifier of the storage pool as a read-only property.

        Returns:
            int: The unique ID of the storage pool.

        Example:
            >>> storage_pool = StoragePool()
            >>> pool_id = storage_pool.storage_pool_id  # Access the storage pool ID
            >>> print(f"Storage Pool ID: {pool_id}")

        #ai-gen-doc
        """
        return self._storage_pool_id

    @property
    def storage_pool_properties(self) -> dict:
        """Get the properties of the storage pool as a read-only attribute.

        Returns:
            dict: A dictionary containing the properties of the storage pool.

        Example:
            >>> storage_pool = StoragePool(commcell_object, 'MyStoragePool')
            >>> properties = storage_pool.storage_pool_properties
            >>> print(properties)
            {'poolName': 'MyStoragePool', 'totalCapacity': 100000, ...}

        #ai-gen-doc
        """
        return self._storage_pool_properties

    @property
    def global_policy_name(self) -> str:
        """Get the name of the global policy associated with this storage pool.

        Returns:
            The name of the global policy as a string.

        Example:
            >>> storage_pool = StoragePool()
            >>> policy_name = storage_pool.global_policy_name  # Use dot notation for property access
            >>> print(f"Global policy name: {policy_name}")

        #ai-gen-doc
        """
        return self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["StoragePolicyCopy"]["storagePolicyName"]

    @property
    def copy_name(self) -> str:
        """Get the name of the storage pool copy as a read-only attribute.

        Returns:
            The name of the storage pool copy as a string.

        Example:
            >>> storage_pool = StoragePool()
            >>> name = storage_pool.copy_name  # Access the copy name property
            >>> print(f"Copy name: {name}")

        #ai-gen-doc
        """
        return self._copy_name

    @property
    def copy_id(self) -> int:
        """Get the copy ID associated with this StoragePool instance.

        This property provides read-only access to the copy ID, which uniquely identifies 
        the storage pool copy within the system.

        Returns:
            The copy ID as an integer.

        Example:
            >>> storage_pool = StoragePool()
            >>> copy_id = storage_pool.copy_id  # Access the copy ID using dot notation
            >>> print(f"Storage pool copy ID: {copy_id}")

        #ai-gen-doc
        """
        return self._copy_id

    @property
    def storage_pool_type(self) -> int:
        """Get the type of the storage pool as a read-only attribute.

        Returns:
            The storage pool type as an integer.

        Example:
            >>> pool = StoragePool()
            >>> pool_type = pool.storage_pool_type  # Access the storage pool type property
            >>> print(f"Storage pool type: {pool_type}")

        #ai-gen-doc
        """
        return self._storage_pool_properties["storagePoolDetails"]["storagePoolType"]

    @property
    def storage_type(self) -> int:
        """Get the storage type of the storage pool as a read-only attribute.

        Returns:
            The storage type of the storage pool as an integer.

        Example:
            >>> pool = StoragePool()
            >>> stype = pool.storage_type  # Access the storage type property
            >>> print(f"Storage type: {stype}")

        #ai-gen-doc
        """
        return self._storage_pool_properties["storagePoolDetails"]["storageType"]

    @property
    def storage_vendor(self) -> int:
        """Get the storage vendor or cloud storage provider associated with this storage pool.

        This property provides the name of the library vendor or cloud storage provider as a read-only attribute.

        Returns:
            The id of the storage vendor or cloud storage provider as an integer.

        Example:
            >>> storage_pool = StoragePool()
            >>> vendor = storage_pool.storage_vendor
            >>> print(f"Storage vendor: {vendor}")

        #ai-gen-doc
        """
        return self._storage_pool_properties["storagePoolDetails"]["libraryVendorId"]

    @property
    def ddb_media_agents(self) -> list:
        """Get the list of deduplication media agents associated with this storage pool.

        This property provides a read-only list of deduplication media agents configured for the storage pool.

        Returns:
            list: A list of deduplication media agents."""
        return self._get_ddb_media_agents()

    @property
    def storage_media_agents(self) -> list:
        """Get the list of storage media agents associated with this storage pool.

        This property provides a read-only list of storage media agents configured for the storage pool.

        Returns:
            list: A list of storage media agents."""
        return self._get_storage_media_agents()

    @property
    def media_agents(self) -> list:
        """Get the list of all media agents associated with this storage pool.

        This property provides a read-only list of all media agents configured for the storage pool.

        Returns:
            list: A list of all media agents associated with the storage pool.

        Example:
            >>> storage_pool = StoragePool()
            >>> all_media_agents = storage_pool.media_agents  # Access the media agents property
            >>> print(f"All media agents: {all_media_agents}")

        #ai-gen-doc
        """
        return list(set(self._get_storage_media_agents() + self._get_ddb_media_agents()))

    @property
    def media_agents_with_roles(self) -> dict:
        """Get the dictionary of media agents associated with this storage pool, categorized by their roles.

        This property provides a read-only dictionary of media agents configured for the storage pool,
        categorized into 'storage' and 'DDB' roles.

        Returns:
            dict: A dictionary with two keys: 'storage' and 'DDB', each containing a list of corresponding media agents.

        Example:
            >>> storage_pool = StoragePool()
            >>> media_agents_dict = storage_pool.media_agents_with_roles  # Access the media agents with roles property
            >>> print(media_agents_dict)
            {
                'storage': ['StorageMA1', 'StorageMA2'],
                'DDB': ['DDBMA1', 'DDBMA2']
            }

        #ai-gen-doc
        """
        return {
                "storage": self._get_storage_media_agents(),
                "DDB": self._get_ddb_media_agents()
            }

    @property
    def store_id(self) -> list:
        """Get the list of store IDs associated with this storage pool.

        This property provides a read-only list of store IDs configured for the storage pool.

        Returns:
            list: A list of store IDs associated with the storage pool.

        Example:
            >>> storage_pool = StoragePool()
            >>> store_ids = storage_pool.store_id  # Access the store ID property
            >>> print(f"Store IDs: {store_ids}")

        #ai-gen-doc
        """
        store_ids = []
        DDB_details_list = self._storage_pool_properties.get("storagePoolDetails", {}).get("dedupDBDetailsList", [])
        for store in DDB_details_list:
            store_ids.append(store.get("storeId"))
        return store_ids

    @property
    def library_id(self) -> int:
        """Get the library ID associated with this storage pool.

        This property provides a read-only integer value representing the library ID configured for the storage pool.

        Returns:
            int: The library ID associated with the storage pool.
        Example:
            >>> storage_pool = StoragePool()
            >>> library_id = storage_pool.library_id  # Access the library ID property
            >>> print(f"Library ID: {library_id}")"""
        
        library_list = self._storage_pool_properties.get("storagePoolDetails", {}).get("libraryList")
        if library_list:
            return library_list[0].get("library", {}).get("libraryId")

    @property
    def library_name(self) -> str:
        """Get the library name associated with this storage pool.

        This property provides a read-only string value representing the library name configured for the storage pool.

        Returns:
            str: The library name associated with the storage pool.

        Example:
            >>> storage_pool = StoragePool()
            >>> library_name = storage_pool.library_name  # Access the library name property
            >>> print(f"Library name: {library_name}")
        """
        library_list = self._storage_pool_properties.get("storagePoolDetails", {}).get("libraryList")
        if library_list:
            return library_list[0].get("library", {}).get("libraryName")

    @property
    def is_worm_storage_lock_enabled(self) -> bool:
        """Indicate whether WORM (Write Once Read Many) storage lock is enabled for this storage pool.

        Returns:
            bool: True if WORM storage lock is enabled, False otherwise.

        Example:
            >>> storage_pool = StoragePool()
            >>> if storage_pool.is_worm_storage_lock_enabled:
            ...     print("WORM storage lock is enabled.")
            ... else:
            ...     print("WORM storage lock is not enabled.")

        #ai-gen-doc
        """
        return self._storage_pool_properties["storagePoolDetails"]["isWormStorage"]

    @property
    def is_object_level_worm_lock_enabled(self) -> bool:
        """Indicate whether object-level WORM (Write Once Read Many) lock is enabled for the storage pool.

        This property provides a read-only boolean value that specifies if object-level WORM lock is active.

        Returns:
            True if object-level WORM lock is enabled; False otherwise.

        Example:
            >>> storage_pool = StoragePool()
            >>> if storage_pool.is_object_level_worm_lock_enabled:
            ...     print("Object-level WORM lock is enabled.")
            ... else:
            ...     print("Object-level WORM lock is not enabled.")

        #ai-gen-doc
        """
        worm_flag = int(self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["wormStorageFlag"])
        return worm_flag & WORMLockType.OBJECT == WORMLockType.OBJECT

    @property
    def is_bucket_level_worm_lock_enabled(self) -> bool:
        """Indicate whether bucket-level WORM (Write Once Read Many) lock is enabled for the storage pool.

        This property provides a read-only boolean value that specifies if the bucket-level WORM lock feature 
        is currently enabled on the storage pool.

        Returns:
            True if bucket-level WORM lock is enabled; False otherwise.

        Example:
            >>> storage_pool = StoragePool()
            >>> if storage_pool.is_bucket_level_worm_lock_enabled:
            ...     print("Bucket-level WORM lock is enabled.")
            ... else:
            ...     print("Bucket-level WORM lock is not enabled.")

        #ai-gen-doc
        """
        worm_flag = int(self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["wormStorageFlag"])
        return worm_flag & WORMLockType.BUCKET == WORMLockType.BUCKET

    @property
    def is_compliance_lock_enabled(self) -> bool:
        """Indicate whether compliance lock is enabled for the storage pool.

        Returns:
            bool: True if compliance lock is enabled, False otherwise.

        Example:
            >>> storage_pool = StoragePool()
            >>> if storage_pool.is_compliance_lock_enabled:
            ...     print("Compliance lock is enabled.")
            ... else:
            ...     print("Compliance lock is not enabled.")

        #ai-gen-doc
        """
        return self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["copyFlags"]["wormCopy"] == 1

    def get_copy(self) -> 'StoragePolicyCopy':
        """Retrieve the StoragePolicyCopy object associated with this Storage Pool.

        Returns:
            StoragePolicyCopy: The copy object representing the storage policy copy for this storage pool.

        Example:
            >>> storage_pool = StoragePool()
            >>> copy = storage_pool.get_copy()
            >>> print(f"Copy name: {copy.name}")
            >>> # The returned StoragePolicyCopy object can be used for further copy-specific operations

        #ai-gen-doc
        """
        return StoragePolicyCopy(self._commcell_object, self.storage_pool_name, self.copy_name)

    def enable_compliance_lock(self) -> None:
        """Enable compliance lock on the storage pool copy.

        This method activates the compliance lock feature for the storage pool copy, 
        ensuring that data within the pool is protected from deletion or modification 
        according to compliance requirements.

        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.enable_compliance_lock()
            >>> print("Compliance lock enabled on the storage pool copy.")

        #ai-gen-doc
        """
        self.get_copy().enable_compliance_lock()
        self.refresh()

    def enable_worm_storage_lock(self, retain_days: int) -> None:
        """Enable WORM (Write Once Read Many) storage lock on the storage pool.

        This method activates the WORM lock feature for the storage pool, ensuring that data written 
        to the pool cannot be modified or deleted for the specified retention period.

        Args:
            retain_days: The number of days to retain data in WORM (immutable) state.

        Raises:
            SDKException: If the operation fails or the response is empty.

        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.enable_worm_storage_lock(retain_days=30)
            >>> print("WORM storage lock enabled for 30 days retention.")

        #ai-gen-doc
        """

        request_json = {
            "storagePolicyCopyInfo": {
                "copyFlags": {
                    "wormCopy": 1
                },
                "retentionRules": {
                    "retainBackupDataForDays": retain_days
                }
            },
            "isWormStorage": True,
            "forceCopyToFollowPoolRetention": True
        }

        _STORAGE_POOL_COPY = self._commcell_object._services['STORAGE_POLICY_COPY'] % (
            self._storage_pool_id, str(self.copy_id))
        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', _STORAGE_POOL_COPY, request_json)

        if flag:
            if response.json():
                response = response.json()
                if "error" in response and response.get("error", {}).get("errorCode") != 0:
                    error_message = response.get("error", {}).get("errorMessage")
                    raise SDKException('Response', '102', error_message)
                else:
                    self.refresh()
            else:
                raise SDKException('Response', '101')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
    
    def enable_retention_lock(self, retention_lock_days: int) -> None:
        """Enable retention lock on the storage pool copy.

        This method activates the retention lock feature for the storage pool copy, 
        ensuring that data within the pool is retained for the specified number of days.

        Args:
            retention_lock_days: The number of days to retain data in the storage pool copy.
        Raises:
            SDKException: If the operation fails or the response is empty.
        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.enable_retention_lock(retention_days=60)
            >>> print("Retention lock enabled on the storage pool copy for 60 days.")
        """
        _RETENTION_LOCK = self._commcell_object._services['ENABLE_RETENTION_LOCK'] % (
            self._storage_pool_id, str(self.copy_id))
        request_json = {
            "retentionDays": retention_lock_days
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', _RETENTION_LOCK, request_json)
        if flag:
            if response.json():
                response = response.json()
                if "errorCode" in response and response.get("errorCode") != 0:
                    error_message = response.get("errorMessage")
                    raise SDKException('Storage', '102', error_message)
            else:
                raise SDKException('Response', '101')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
        
        if not int(self.storage_pool_properties['storagePoolDetails']['copyInfo']['dataRetentionLockDays']) == retention_lock_days:
            raise SDKException('Storage', '102', 'Failed to set retention lock on storage pool copy.')

    def hyperscale_add_nodes(self, media_agents: list) -> None:
        """Add three new nodes to an existing storage pool using the specified media agents.

        Args:
            media_agents: A list of three media agents, each specified either by name (str) or as a media agent object.
                Example:
                    ["ma1", "ma2", "ma3"]

        Raises:
            SDKException: If adding nodes to the existing storage pool fails.

        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.hyperscale_add_nodes(["ma1", "ma2", "ma3"])
            >>> # Alternatively, you can pass media agent objects if available

        #ai-gen-doc
        """
        if not isinstance(media_agents, list):
            raise SDKException('Storage', '101')

        mediagent_obj = []
        for media_agent in media_agents:
            if isinstance(media_agent, MediaAgent):
                mediagent_obj.append(media_agent)
            elif isinstance(media_agent, str):
                mediagent_obj.append(self._commcell_object.media_agents.get(media_agent))
            else:
                raise SDKException('Storage', '103')

        if len(mediagent_obj) <= 2:
            raise SDKException('Storage', '102', "Minimum 3 MediaAgents required")

        request_json = {
            "scaleoutOperationType": 2,
            "StoragePolicy": {
                "storagePolicyName": "{0}".format(self.storage_pool_name),
            },
            "storage": [
                {
                    "mediaAgent": {
                        "displayName": "{0}".format(mediagent_obj[0].media_agent_id),
                        "mediaAgentName": "{0}".format(mediagent_obj[0].media_agent_name)
                    }
                },
                {
                    "mediaAgent": {
                        "displayName": "{0}".format(mediagent_obj[1].media_agent_id),
                        "mediaAgentName": "{0}".format(mediagent_obj[1].media_agent_name)
                    }
                },
                {
                    "mediaAgent": {
                        "displayName": "{0}".format(mediagent_obj[2].media_agent_id),
                        "mediaAgentName": "{0}".format(mediagent_obj[2].media_agent_name)
                    }
                }
            ],
            "scaleoutConfiguration": {
                "configurationType": 1
            }
        }

        self._edit_storage_pool_api = self._commcell_object._services[
            'EDIT_STORAGE_POOL']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._edit_storage_pool_api, request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if int(error_code) != 0:
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to add nodes to storage pool\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def hyperscale_reconfigure_storage_pool(self, storage_pool_name: str) -> None:
        """Reconfigure a HyperScale storage pool after a failure during creation or expansion.

        This method attempts to reconfigure the specified storage pool, which can be useful if
        the pool encountered issues during its initial creation or a recent expansion.

        Args:
            storage_pool_name: The name of the HyperScale storage pool to reconfigure.

        Raises:
            SDKException: If the reconfiguration process fails.

        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.hyperscale_reconfigure_storage_pool("HS_Pool_01")
            >>> print("Reconfiguration initiated for HS_Pool_01")

        #ai-gen-doc
        """
        if not isinstance(storage_pool_name, str):
            raise SDKException('Storage', '101')

        request_json = {

            "scaleoutOperationType": 4,
            "StoragePolicy":
                {
                    "storagePolicyName": "{0}".format(storage_pool_name),
                    "storagePolicyId": int("{0}".format(self.storage_pool_id))

                }
        }

        self._edit_storage_pool_api = self._commcell_object._services[
            'EDIT_STORAGE_POOL']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._edit_storage_pool_api, request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if int(error_code) != 0:
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to reconfigure storage pool\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def hyperscale_replace_disk(self, disk_id: int, media_agent: Union[str, object], storage_pool_name: str) -> None:
        """Replace a disk on a specified media agent within a storage pool in a HyperScale environment.

        This method initiates the replacement of a disk identified by its disk ID on the given media agent,
        which must be part of the specified storage pool.

        Args:
            disk_id: The unique identifier (ID) of the disk to be replaced.
            media_agent: The media agent name or object where the disk replacement will occur.
            storage_pool_name: The name of the storage pool containing the disk to be replaced.

        Raises:
            SDKException: If the disk replacement operation fails.

        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.hyperscale_replace_disk(
            ...     disk_id=101,
            ...     media_agent="MediaAgent01",
            ...     storage_pool_name="HS_StoragePool"
            ... )
            >>> print("Disk replacement initiated successfully.")

        #ai-gen-doc
        """
        if isinstance(disk_id, str):
            disk_id = int(disk_id)
        elif not isinstance(disk_id, int):
            raise SDKException('Storage', '101')

        media_agent_obj = None
        if isinstance(media_agent, str):
            media_agent_obj = self._commcell_object.media_agents.get(media_agent)
        elif isinstance(media_agent, MediaAgent):
            media_agent_obj = media_agent
        else:
            raise SDKException('Storage', '103')

        if not isinstance(storage_pool_name, str):
            raise SDKException('Storage', '101')

        request_json = {

            "driveId": int("{0}".format(disk_id)),
            "operationType": 1,
            "mediaAgent": {
                "_type_": 11,
                "mediaAgentId": int("{0}".format(media_agent_obj.media_agent_id)),
                "mediaAgentName": "{0}".format(media_agent_obj.media_agent_name)
            },
            "scaleoutStoragePool": {
                "_type_": 160,
                "storagePoolId": int("{0}".format(self.storage_pool_id)),
                "storagePoolName": "{0}".format(self.storage_pool_name)
            }
        }

        self._replace_disk_storage_pool_api = self._commcell_object._services[
            'REPLACE_DISK_STORAGE_POOL']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._replace_disk_storage_pool_api, request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if int(error_code) != 0:
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to replace disk\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
    
    def add_media_agent(self, media_agent, storage = True, ddb = False) -> None:
        """Add a media agent to the storage pool.

        This method associates a media agent with the storage pool, allowing it to be used for storage operations.
        You can specify whether to add the media agent as a storage media agent, a DDB media agent, or both.

        Args:
            media_agent: The name or MediaAgent object of the media agent to be added.
            storage: Set to True to add as a storage media agent. Default is True.
            ddb: Set to True to add as a DDB media agent. Default is False.
        
        Raises:
            SDKException: If the media agent is already associated with the storage pool in the specified role(s).
        
        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.add_media_agent("MediaAgent01", storage=True, ddb=False)
            >>> log.info("Media agent added to storage pool.")
        """

        if isinstance(media_agent, str):
            media_agent_obj = self._commcell_object.media_agents.get(media_agent)
        elif isinstance(media_agent, MediaAgent):
            media_agent_obj = media_agent
        else:
            raise SDKException('Storage', '101')
        if not (storage or ddb):
            raise SDKException('StoragePool', '104', 'At least one of storage or ddb must be True')

        if storage and media_agent_obj.media_agent_name in self._get_storage_media_agents():
            raise SDKException('StoragePool', '104', 'Media Agent already a storage media agent for this pool')
        if ddb and media_agent_obj.media_agent_name in self._get_ddb_media_agents():
            raise SDKException('StoragePool', '104', 'Media Agent already a DDB media agent for this pool')
        
        action = ManageMediaAgentActionType.ADD_STORAGE.value if storage and not ddb else \
                 ManageMediaAgentActionType.ADD_DDB.value if ddb and not storage else \
                 ManageMediaAgentActionType.ADD_DDB_STORAGE.value
        self._manage_media_agents_for_pool_api = self._commcell_object._services['MANAGE_MEDIA_AGENTS_FOR_POOL'] % (self.storage_pool_id)

        request_json = {
            "mediaAgent": {
                "id": int(media_agent_obj.media_agent_id)
            },
            "action": action
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._manage_media_agents_for_pool_api, request_json)
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)

                if int(error_code) != 0:
                    error_message = response.json().get('errorMessage', 'Unknown error occurred')
                    o_str = 'Failed to add media agent to storage pool\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()
    
    def remove_media_agent(self, media_agent : Union[str, MediaAgent], storage : bool = True, ddb : bool = True) -> None:
        """Remove a media agent from the storage pool.

        This method disassociates a media agent from the storage pool, preventing it from being used for storage operations.
        You can specify whether to remove the media agent as a storage media agent, a DDB media agent, or both.

        Args:
            media_agent: The name or MediaAgent object of the media agent to be removed.
            storage: Set to True to remove as a storage media agent. Default is True.
            ddb: Set to True to remove as a DDB media agent. Default is True.
            
        Raises:
            SDKException: If the media agent is not associated with the storage pool in the specified role(s).

        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.remove_media_agent("MediaAgent01", storage=True, ddb=False)
            >>> log.info("Media agent removed from storage pool.")
        """
        if isinstance(media_agent, str):
            media_agent_obj = self._commcell_object.media_agents.get(media_agent)
        elif isinstance(media_agent, MediaAgent):
            media_agent_obj = media_agent
        else:
            raise SDKException('Storage', '101')
        if not (storage or ddb):
            raise SDKException('StoragePool', '104', 'At least one of storage or ddb must be True')

        if storage and media_agent_obj.media_agent_name not in self._get_storage_media_agents():
            raise SDKException('StoragePool', '104', 'Media Agent is not a storage media agent for this pool')
        if ddb and media_agent_obj.media_agent_name not in self._get_ddb_media_agents():
            raise SDKException('StoragePool', '104', 'Media Agent is not a DDB media agent for this pool')
        
        action = ManageMediaAgentActionType.REMOVE_STORAGE.value if storage and not ddb else \
                 ManageMediaAgentActionType.REMOVE_DDB.value if ddb and not storage else \
                 ManageMediaAgentActionType.REMOVE_DDB_STORAGE.value
        self._manage_media_agents_for_pool_api = self._commcell_object._services['MANAGE_MEDIA_AGENTS_FOR_POOL'] % (self.storage_pool_id)
        request_json = {
            "mediaAgent": {
                "id": int(media_agent_obj.media_agent_id)
            },
            "action": action
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._manage_media_agents_for_pool_api, request_json
        )
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)

                if int(error_code) != 0:
                    error_message = response.json().get('errorMessage', 'Unknown error occurred')
                    o_str = 'Failed to remove media agent from storage pool\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def refresh(self) -> None:
        """Reload the properties of the StoragePool object to reflect the latest state.

        This method updates the internal state of the StoragePool instance, ensuring that 
        any changes made externally are reflected in the object's properties.

        Example:
            >>> storage_pool = StoragePool()
            >>> storage_pool.refresh()
            >>> print("Storage pool properties refreshed.")

        #ai-gen-doc
        """
        self._get_storage_pool_properties()

    def update_security_associations(
        self,
        associations_list: List[Dict[str, Any]],
        isUser: bool = True,
        request_type: str = None,
        externalGroup: bool = False
    ) -> None:
        """Add or update security associations on the storage pool object.

        This method associates users or user groups with specific roles on the storage pool.
        You can specify whether the associations are for users or user groups, the type of request
        (such as 'OVERWRITE', 'UPDATE', or 'DELETE'), and whether the associations are for external groups.

        Args:
            associations_list: A list of dictionaries specifying users or user groups and their roles.
                Example:
                    associations_list = [
                        {
                            'user_name': 'user1',
                            'role_name': 'role1'
                        },
                        {
                            'user_name': 'user2',
                            'role_name': 'role2'
                        }
                    ]
            isUser: Set to True if associating users, or False if associating user groups. Default is True.
            request_type: The type of association request. Can be 'OVERWRITE', 'UPDATE', or 'DELETE'.
                If not specified, defaults to 'OVERWRITE'.
            externalGroup: Set to True if associating external user groups. Default is False.

        Raises:
            SDKException: If associations_list is not a list.

        Example:
            >>> associations = [
            ...     {'user_name': 'alice', 'role_name': 'StorageAdmin'},
            ...     {'user_name': 'bob', 'role_name': 'Viewer'}
            ... ]
            >>> storage_pool.update_security_associations(associations, isUser=True, request_type='UPDATE')
            >>> # To associate user groups instead of users:
            >>> group_associations = [
            ...     {'user_group_name': 'BackupOperators', 'role_name': 'Operator'}
            ... ]
            >>> storage_pool.update_security_associations(group_associations, isUser=False)
            >>> # To associate external user groups:
            >>> ext_group_associations = [
            ...     {'user_group_name': 'ExternalGroup1', 'role_name': 'ExternalRole'}
            ... ]
            >>> storage_pool.update_security_associations(ext_group_associations, isUser=False, externalGroup=True)

        #ai-gen-doc
        """
        if not isinstance(associations_list, list):
            raise SDKException('StoragePool', '101')

        SecurityAssociation(self._commcell_object, self)._add_security_association(associations_list,
                                                                                   user=isUser,
                                                                                   request_type=request_type,
                                                                                   externalGroup=externalGroup)