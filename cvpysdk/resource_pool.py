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

"""Main file for performing resource pool related operations on CS

ResourcePools , ResourcePool and ResourcePoolTypes are the classes defined in this file

ResourcePools:

        __init__()                          --  initialise object of the ResourcePools class

        _response_not_success()             --  parses through the exception response, and raises SDKException

        _get_resource_pools()               --  returns resource pools details from CS

        has()                               --  Checks whether given resource pool exists in cs or not

        get()                               -- returns ResourcePool object for given name

        delete()                            --  deletes the resource pool from CS

        create()                            --  creates resource pool in CS

        get_resource_pools_by_solution()    --  returns resource pools filtered by solution name

        get_resource_pools_by_region()      --  returns resource pools filtered by region name

        get_cleanroom_resource_pools()      --  returns all Cleanroom resource pools

        refresh()                           --  Refreshes resource pools associated with cs

ResourcePool:

        __init__()                          --  initialise object of the ResourcePool class

        _response_not_success()             --  parses through the exception response, and raises SDKException

        _get_pool_details()                 --  returns resource pool details from cs

        refresh()                           --  refreshes resource pool details

ResourcePool Attributes:
----------------------------------

    **resource_pool_id**        --  returns Resource pool id

    **resource_pool_type**      --  returns ResourcePoolTypes enum

    **resource_pool_solution**  --  returns list of solutions associated with the resource pool

    **resource_pool_region**    --  returns region name for the resource pool

"""

from .exception import SDKException

import enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import requests
    from cvpysdk.commcell import Commcell


class ResourcePoolTypes(enum.Enum):
    """
    Enumeration class representing different types of resource pools.

    This enum is used to define and categorize various resource pool types
    within the application, providing a clear and type-safe way to reference
    specific pool categories throughout the codebase.

    Key Features:
        - Defines distinct resource pool types as enumeration members
        - Ensures type safety and clarity when working with resource pools
        - Facilitates consistent usage of resource pool identifiers

    #ai-gen-doc
    """
    GENERIC = 0
    O365 = 1
    SALESFORCE = 2
    EXCHANGE = 3
    SHAREPOINT = 4
    ONEDRIVE = 5
    TEAMS = 6
    DYNAMICS_365 = 7
    VSA = 8
    FILESYSTEM = 9
    KUBERNETES = 10
    AZURE_AD = 11
    CLOUD_LAPTOP = 12
    FILE_STORAGE_OPTIMIZATION = 13
    DATA_GOVERNANCE = 14
    E_DISCOVERY = 15
    CLOUD_DB = 16
    OBJECT_STORAGE = 17
    GMAIL = 18
    GOOGLE_DRIVE = 19
    GOOGLE_WORKSPACE = 20
    SERVICENOW = 21
    THREATINDICATOR = 22
    DEVOPS = 23
    RISK_ANALYSIS = 24
    THREATSCAN = 25
    GOOGLE_CLOUD_PLATFORM = 50001


class ResourcePoolSolutions(enum.Enum):
    """
    Enumeration class representing different solutions associated with resource pools.

    This enum is used to define and categorize various solutions that resource pools may be associated with,
    providing a clear and type-safe way to reference specific solution categories throughout the codebase.

    Key Features:
        - Defines distinct solution categories as enumeration members
        - Ensures type safety and clarity when working with resource pool solutions
        - Facilitates consistent usage of solution identifiers in relation to resource pools

    #ai-gen-doc
    """
    CLEANROOM = 25


class ResourcePools:
    """
    Class to manage and represent all resource pools within a system.

    This class provides a comprehensive interface for interacting with resource pools,
    including creation, deletion, retrieval, existence checks, and refreshing the pool list.
    It also includes internal mechanisms for handling responses and fetching resource pool data.

    Key Features:
        - Initialize with a Commcell object for context
        - Create new resource pools with specified names and types
        - Delete existing resource pools by name
        - Retrieve resource pool details by name
        - Check for the existence of a resource pool
        - Refresh the list of resource pools to reflect current state
        - Internal handling of unsuccessful responses
        - Internal retrieval of all resource pools

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a new instance of the ResourcePools class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> resource_pools = ResourcePools(commcell)
            >>> print("ResourcePools instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._API_GET_ALL_RESOURCE_POOLS = self._services['GET_RESOURCE_POOLS']
        self._API_DELETE_RESOURCE_POOL = self._services['DELETE_RESOURCE_POOL']
        self._API_CREATE_RESOURCE_POOL = self._services['CREATE_RESOURCE_POOL']
        self._pools = {}
        self.refresh()

    def _response_not_success(self, response: 'requests.Response') -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object, typically
        obtained from the `requests` Python package, and raises an exception if the status
        code indicates a failure.

        Args:
            response: The response object returned from an API request.

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_resource_pools(self) -> dict:
        """Retrieve resource pool details from the CommServe (CS).

        Returns:
            dict: A dictionary containing details of all resource pools.

        Raises:
            SDKException: If the resource pool details could not be retrieved.

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_GET_ALL_RESOURCE_POOLS)
        output = {}
        if flag:
            if response.json() and 'resourcePools' in response.json():
                _resourcepools = response.json()['resourcePools']
                for _pool in _resourcepools:
                    if 'name' in _pool:
                        output.update({_pool['name'].lower(): _pool})
            elif bool(response.json()):
                raise SDKException('ResourcePools', '103')
            return output
        self._response_not_success(response)

    def create(self, name: str, resource_type: 'ResourcePoolTypes', access_nodes: list, is_client_group: bool = True) -> 'ResourcePool':
        """Create a new resource pool in the CommServe.

        Args:
            name: The name of the resource pool to create.
            resource_type: The type of resource pool (appType 25 for Cleanroom).
            access_nodes: List of client group names or client names to associate with the resource pool.
            is_client_group: Flag to determine if access_nodes contains client groups (True) or clients (False).
                            Default is True for client groups.

        Returns:
            ResourcePool: An instance representing the newly created resource pool.

        Raises:
            SDKException: If the resource pool creation fails or if a resource pool with the given name already exists.

        Example:
            >>> # Create with client groups
            >>> pool = resource_pools.create(
            ...     name="CleanroomPool",
            ...     resource_type=ResourcePoolTypes(25),
            ...     access_nodes=["AdminHyperVAWS"],
            ...     is_client_group=True
            ... )
            
            >>> # Create with clients
            >>> pool = resource_pools.create(
            ...     name="CleanroomPool",
            ...     resource_type=ResourcePoolTypes(25),
            ...     access_nodes=["lego"],
            ...     is_client_group=False
            ... )

        #ai-gen-doc
        """
        if resource_type.value != ResourcePoolTypes.THREATSCAN.value:
            raise SDKException('ResourcePools', '102', 'Resource pool creation is only supported for appType ThreatScan (25)')
        if not access_nodes:
            raise SDKException('ResourcePools', '102', 'Access nodes list cannot be empty')
        if self.has(name=name):
            raise SDKException('ResourcePools', '107')
        
        client_groups = []
        clients = []
        
        # Build client groups or clients based on flag
        if is_client_group:
            for node_name in access_nodes:
                client_group = self._commcell_object.client_groups.get(node_name)
                client_groups.append({
                    "clientGroupId": int(client_group.clientgroup_id),
                    "clientGroupName": node_name
                })
        else:
            for client_name in access_nodes:
                client = self._commcell_object.clients.get(client_name)
                clients.append({
                    "clientId": int(client.client_id),
                    "clientName": client_name
                })
        
        _request_json = {
            "resourcePool": {
                "appType": resource_type.value,
                "dataAccessNodes": [],
                "extendedProp": {
                    "exchangeOnePassClientProperties": {}},
                "resourcePool": {
                    "resourcePoolId": 0,
                    "resourcePoolName": name},
                "exchangeServerProps": {
                    "jobResultsDirCredentials": {
                        "userName": ""},
                    "jobResultsDirPath": ""},
                "roleId": None,
                "indexServerMembers": [],
                "accessNodes": {
                    "clientGroups": client_groups,
                    "clients": clients}}}
        
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_CREATE_RESOURCE_POOL, _request_json)
        if flag:
            if response.json() and 'error' in response.json():
                _error = response.json()['error']
                if _error.get('errorCode', 0) != 0:
                    raise SDKException('ResourcePools', '102', f'Resource pool creation failed with {_error}')
                self.refresh()
                return self.get(name=name)
            raise SDKException('ResourcePools', '108')
        self._response_not_success(response)

    def delete(self, name: str) -> None:
        """Delete a resource pool from the CommServe (CS) by name.

        Args:
            name: The name of the resource pool to delete.

        Raises:
            SDKException: If the resource pool cannot be found or deletion fails.

        #ai-gen-doc
        """
        if not self.has(name=name):
            raise SDKException('ResourcePools', '104')
        api = self._API_DELETE_RESOURCE_POOL % (self._pools[name.lower()]['id'])
        flag, response = self._cvpysdk_object.make_request('DELETE', api)
        if flag:
            if response.json() and 'error' in response.json():
                _error = response.json()['error']
                if _error.get('errorCode', 0) != 0:
                    raise SDKException('ResourcePools', '102', f'Resource pool deletion failed with {_error}')
                self.refresh()
                return
            raise SDKException('ResourcePools', '106')
        self._response_not_success(response)

    def get(self, name: str) -> 'ResourcePool':
        """Retrieve a ResourcePool object by its name.

        Args:
            name: The name of the resource pool to retrieve.

        Returns:
            ResourcePool: An instance of the ResourcePool class corresponding to the specified name.

        Raises:
            SDKException: If a resource pool with the given name cannot be found.

        #ai-gen-doc
        """
        if not self.has(name):
            raise SDKException('ResourcePools', '104')
        return ResourcePool(commcell_object=self._commcell_object, name=name, pool_id=self._pools[name.lower()]['id'])

    def has(self, name: str) -> bool:
        """Check if a resource pool with the specified name exists in the CommServe.

        Args:
            name: The name of the resource pool to check.

        Returns:
            True if the resource pool exists in the CommServe; False otherwise.

        #ai-gen-doc
        """
        if name.lower() in self._pools:
            return True
        return False

    def get_resource_pools_by_solution(self, solution_id: int) -> dict:
        """Return resource pools filtered by solution ID.

        This method checks each pool's ``solutions`` list and matches against the
        integer ``solutionId`` field. Pools that do not include the ``solutions`` key
        (or have an empty solutions list) are skipped.

        Args:
            solution_id (int): The solution ID to filter by, e.g. ``25`` for Cleanroom.

        Returns:
            dict: Mapping of resource pool name to its details dictionary for all pools
            whose ``solutions`` list contains the given ``solution_id``. Returns an
            empty dict if no pools match.

        Example:
            >>> cleanroom_pools = resource_pools.get_resource_pools_by_solution(25)
            >>> for name, details in cleanroom_pools.items():
            ...     region = details.get("regionInfo", {}).get("regionEntity", {}).get("regionName", "")
            ...     print(f"{name}: {region}")

        #ai-gen-doc
        """
        resource_pools = {}
        for pool_name, pool_details in self._pools.items():
            if solution_id == ResourcePoolTypes.THREATINDICATOR.value:
                 if pool_details.get('solutionType') == "THREAT_INDICATORS":
                    resource_pools[pool_name] = pool_details
            else:
                for sol in pool_details.get('solutions', []):
                    if sol.get('id') == solution_id:
                        resource_pools[pool_name] = pool_details
                        break
        return resource_pools

    def get_resource_pools_by_region(self, region_name: str) -> dict:
        """Return resource pools filtered by region name.

        This method matches pools based on the region name present at
        ``regionInfo.regionEntity.regionName`` in each pool's details. Matching is
        case-insensitive.

        Args:
            region_name (str): Region name to filter by (case-insensitive), e.g. ``"eastus2"``.

        Returns:
            dict: Mapping of resource pool name to its details dictionary for all matching pools.
                  Returns an empty dict if no pools match the given region or if a pool does not
                  contain region information.

        Example:
            >>> eastus2_pools = resource_pools.get_resource_pools_by_region("eastus2")
            >>> for name, details in eastus2_pools.items():
            ...     pool_id = details.get("resourcePool", {}).get("resourcePoolId")
            ...     print(f"{name}: {pool_id}")

        #ai-gen-doc
        """
        resource_pools = {}
        for pool_name, pool_details in self._pools.items():
            if pool_details.get('region', {}).get('name', '').lower() == region_name.lower():
                resource_pools[pool_name] = pool_details
        return resource_pools

    def get_cleanroom_resource_pools(self) -> dict:
        """Return all resource pools configured for the Cleanroom solution.

        This is a convenience wrapper over :meth:`get_resource_pools_by_solution`
        that filters pools where the ``solutions`` list contains the Cleanroom
        solution ID (``ResourcePoolSolutions.CLEANROOM.value``).

        Returns:
            dict: Mapping of resource pool name to its details dictionary for all Cleanroom pools.
                  Returns an empty dict if no Cleanroom resource pools are found.

        Example:
            >>> cleanroom_pools = resource_pools.get_cleanroom_resource_pools()
            >>> for name, details in cleanroom_pools.items():
            ...     print(name)

        #ai-gen-doc
        """
        return self.get_resource_pools_by_solution(ResourcePoolSolutions.CLEANROOM.value)

    def refresh(self) -> None:
        """Reload the resource pools associated with the CommServe (CS).

        This method refreshes the internal state of the ResourcePools object, ensuring that
        any changes to resource pools on the CommServe are reflected in the current instance.

        #ai-gen-doc
        """
        self._pools = {}
        self._pools = self._get_resource_pools()


class ResourcePool:
    """
    Represents a resource pool within a system, providing management and access to pool details.

    This class encapsulates the properties and operations related to a resource pool, including
    initialization with specific identifiers, retrieval and refreshing of pool details, and
    access to pool-specific properties such as ID and type. It also includes internal mechanisms
    for handling unsuccessful responses from operations.

    Key Features:
        - Initialize a resource pool with a commcell object, name, and pool ID
        - Retrieve and refresh resource pool details
        - Handle unsuccessful responses from operations
        - Access resource pool ID and type via properties

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', name: str, pool_id: int) -> None:
        """Initialize a new instance of the ResourcePool class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            name: The name of the resource pool.
            pool_id: The unique identifier for the resource pool.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> resource_pool = ResourcePool(commcell, 'MainPool', 12345)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._resource_pool_name = name
        self._resource_pool_id = pool_id
        self._resource_details = None
        self._API_GET_POOL_DETAILS = self._services['GET_RESOURCE_POOL_DETAILS']
        self.refresh()

    def _response_not_success(self, response: 'requests.Response') -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object,
        typically obtained from the `requests` Python package, and raises an
        exception if the response indicates a failure (i.e., status code is not 200).

        Args:
            response: The response object returned from an API request.

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_pool_details(self) -> dict:
        """Retrieve the details of the resource pool from the CommServe.

        Returns:
            dict: A dictionary containing the resource pool details.

        Raises:
            SDKException: If the details for the resource pool could not be retrieved.

        #ai-gen-doc
        """
        api = self._API_GET_POOL_DETAILS % (self._resource_pool_id)
        flag, response = self._cvpysdk_object.make_request('GET', api)
        if flag:
            if response.json() and 'resourcePool' in response.json():
                return response.json()['resourcePool']
            raise SDKException('ResourcePools', '105')
        self._response_not_success(response)

    def refresh(self) -> None:
        """Reload the details of the resource pool.

        This method updates the internal state of the ResourcePool instance to reflect
        the latest information from the underlying data source or system.

        #ai-gen-doc
        """
        self._resource_details = None
        self._resource_details = self._get_pool_details()

    @property
    def resource_pool_id(self) -> int:
        """Get the unique identifier (ID) for this resource pool.

        Returns:
            The resource pool ID as an integer.

        #ai-gen-doc
        """
        return int(self._resource_details['resourcePool'].get('resourcePoolId'))

    @property
    def resource_pool_type(self) -> 'ResourcePoolTypes':
        """Get the pool type enum for this resource pool.

        Returns:
            ResourcePoolTypes: The enum value representing the type of this resource pool.

        #ai-gen-doc
        """
        return ResourcePoolTypes(int(self._resource_details['appType']))

    @property
    def resource_pool_solution(self) -> list:
        """Return the solutions configured for this resource pool.

        The API returns solutions as a list of dictionaries under the ``solutions`` key,
        with keys like ``solutionId`` and ``solutionName``.

        Returns:
            list: List of solution dictionaries (e.g., ``{'solutionId': int, 'solutionName': str}``).
                  Returns an empty list if the resource pool has no solutions configured.

        Example:
            >>> pool = commcell.resource_pools.get('Cleanroom Access Nodes - eastus2')
            >>> for sol in pool.resource_pool_solution:
            ...     print(f"{sol.get('solutionName')} ({sol.get('solutionId')})")

        #ai-gen-doc
        """
        return self._resource_details.get('solutions', [])

    @property
    def resource_pool_region(self) -> str:
        """Return the region name for this resource pool.

        The API provides region information under ``regionInfo.regionEntity.regionName``.

        Returns:
            str: Region name (for example, ``'eastus2'``). Returns an empty string if not present.

        Example:
            >>> pool = commcell.resource_pools.get('Cleanroom Access Nodes - eastus2')
            >>> print(pool.resource_pool_region)

        #ai-gen-doc
        """
        return self._resource_details.get('regionInfo', {}).get('regionEntity', {}).get('regionName', '')

    @property
    def resource_pool_client_groups(self) -> list:
        """Return the access-node client groups associated with this resource pool.

        The API returns client groups under ``accessNodes.clientGroups`` as a list of dictionaries,
        typically containing ``clientGroupId`` and ``clientGroupName``.

        Returns:
            list: List of client-group dictionaries (e.g., ``{'clientGroupId': int, 'clientGroupName': str}``).
                  Returns an empty list if none are configured.

        Example:
            >>> pool = commcell.resource_pools.get('Cleanroom Access Nodes - eastus2')
            >>> for cg in pool.resource_pool_client_groups:
            ...     print(f"{cg.get('clientGroupName')} ({cg.get('clientGroupId')})")

        #ai-gen-doc
        """
        return self._resource_details.get('accessNodes', {}).get('clientGroups', [])