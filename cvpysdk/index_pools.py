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

"""File for performing index pool related operations on the commcell

IndexPools and IndexPool are 2 classes defined in this file

IndexPools:   Class for representing all the index pools associated with the commcell

IndexPool:    Class for a instance of a single index pool of the commcell


IndexPools
============

    __init__()                          --  initialize object of IndexPools class associated with
    the commcell

    __str()                             --  returns all the Index pools of the commcell

    __repr__()                          --  returns the string to represent the instance

    __getitem__()                       --  returns the details of index pool for given pool name

    _get_all_index_pools()              --  gets detail of all index pools using REST API call

    _response_not_success()             --  raise exception when response is not 200

    get()                               --  return an IndexPool object for given pool name

    has_pool()                          --  returns whether the index pool is present or not in
    the commcell

    add()                            --  creates a new Index pool to the commcell

    delete()                            --  deletes the index pool associated to commcell

    refresh()                           --  refresh the index pools details associated with commcell

IndexPools Attributes
-----------------------

    **all_index_pools**                 --  returns the dictionary consisting of all the index
    pools associated with the commcell and there details


IndexPool
=========

    __init__()                          --  initialize object of IndexPool class

    __repr__()                          --  returns the string to represent the instance

    _response_not_success()             --  raise exception when response is not 200

    modify_node()                       --  modify/add a node to the index pool

    node_info()                         --  returns a dict consisting details of node present in the pool

    refresh()                           --  refresh the index pool details associated with commcell

IndexPool Attributes
----------------------

    **pool_id**                         --  returns the pseudo client id for index pool cloud

    **cloud_id**                        --  returns the cloud id for index pool

    **node_names**                      --  returns a list of names of all the nodes present in pool

    **hac_cluster**                     --  returns the hac cluster name

    **pool_name**                       --  returns the client name for index pool

"""

from copy import deepcopy
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from .exception import SDKException
from .datacube.constants import IndexServerConstants
if TYPE_CHECKING:
    from .commcell import Commcell
    
class IndexPools(object):
    """
    Represents and manages all Index pools associated with a CommCell.

    The IndexPools class provides an interface to interact with, manage, and manipulate
    index pools within a CommCell environment. It allows users to retrieve, add, delete,
    and check the existence of index pools, as well as refresh and access all available
    index pools. The class supports dictionary-like access to individual pools and
    provides string representations for easy inspection.

    Key Features:
        - Retrieve all index pools associated with the CommCell
        - Access individual index pools by name or key
        - Add new index pools with specified nodes and HAC name
        - Delete existing index pools by name
        - Check for the existence of a specific index pool
        - Refresh the list of index pools to reflect current state
        - Access all index pools via a property
        - Handle unsuccessful responses from operations
        - Provides string and representation methods for easy display

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize an IndexPools object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> index_pools = IndexPools(commcell)
            >>> print("IndexPools object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._all_index_pools = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all index pools associated with the Commcell.

        This method provides a human-readable summary of all index pools managed by the Commcell,
        which can be useful for logging, debugging, or display purposes.

        Returns:
            A string listing all index pools associated with the Commcell.

        Example:
            >>> index_pools = IndexPools(commcell_object)
            >>> print(str(index_pools))
            IndexPool1, IndexPool2, IndexPool3
        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Index pool Name')
        index = 1
        for pool_name in self.all_index_pools:
            representation_string += '{:^5}\t{:^20}\n'.format(
                index, pool_name)
            index += 1
        return representation_string

    def __repr__(self) -> str:
        """Return the string representation of the IndexPools instance.

        This method provides a developer-friendly string that represents the current
        IndexPools object, which can be useful for debugging and logging purposes.

        Returns:
            A string representation of the IndexPools instance.

        Example:
            >>> index_pools = IndexPools(commcell_object)
            >>> print(repr(index_pools))
            <IndexPools object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        return "IndexPools class instance for Commcell"

    def __getitem__(self, value: str) -> dict:
        """Retrieve the details of an index pool by its name.

        Args:
            value: The name of the index pool to retrieve.

        Returns:
            A dictionary containing the details of the specified index pool.

        Raises:
            KeyError: If the specified index pool name does not exist.

        Example:
            >>> index_pools = IndexPools()
            >>> pool_details = index_pools["DefaultIndexPool"]
            >>> print(pool_details)
            {'name': 'DefaultIndexPool', 'status': 'Active', ...}

        #ai-gen-doc
        """
        value = value.lower()
        if value in self.all_index_pools:
            return {"pool_name": value, "pool_id": self.all_index_pools[value]}
        raise SDKException('IndexPools', '102')

    def _get_all_index_pools(self) -> None:
        """Retrieve details of all index pools present in the Commcell.

        Raises:
            SDKException: If the response from the Commcell is unsuccessful or empty.

        Example:
            >>> index_pools = index_pools_obj._get_all_index_pools()
            >>> for pool in index_pools:
            ...     print(f"Index Pool Name: {pool.get('name')}, ID: {pool.get('id')}")
        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._services['GET_ALL_CLIENTS'])
        if flag:
            if response.json() and 'clientProperties' in response.json():
                for dictionary in response.json()['clientProperties']:
                    if dictionary['clientProps']['clusterType'] == 14:
                        temp_name = dictionary['client']['clientEntity']['clientName'].lower()
                        temp_id = int(dictionary['client']['clientEntity']['clientId'])
                        self._all_index_pools[temp_name] = temp_id
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _response_not_success(self, response: object) -> None:
        """Raise an exception if the HTTP response is not successful (status code 200).

        Args:
            response: The response object to check for success.

        Raises:
            SDKException: If the response status code indicates failure.

        Example:
            >>> index_pools = IndexPools()
            >>> response = some_http_request()
            >>> index_pools._response_not_success(response)
            >>> # If the response is not successful, an SDKException will be raised

        #ai-gen-doc
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def refresh(self) -> None:
        """Reload the properties and state of the IndexPools class.

        This method refreshes the internal data of the IndexPools instance, ensuring that 
        any changes made externally are reflected in the current object.

        Example:
            >>> index_pools = IndexPools()
            >>> index_pools.refresh()
            >>> print("IndexPools properties refreshed successfully")

        #ai-gen-doc
        """
        self._commcell_object.clients.refresh()
        self._all_index_pools = {}
        self._get_all_index_pools()

    @property
    def all_index_pools(self) -> Dict[str, int]:
        """Get a dictionary containing details of all index pools.

        Returns:
            Dict[str, int]: A dictionary where each key is the name of an index pool and the value is its corresponding pool ID.

        Example:
            >>> index_pools = IndexPools(commcell_object)
            >>> pools = index_pools.all_index_pools
            >>> print(pools)
            {'DefaultPool': 1, 'ArchivePool': 2}

        #ai-gen-doc
        """
        return self._all_index_pools

    def get(self, pool_name: str) -> 'IndexPool':
        """Retrieve the IndexPool object for the specified pool name.

        Args:
            pool_name: The name or ID of the index pool as a string. This should match an existing index pool in the Commcell.

        Returns:
            IndexPool: An instance of the IndexPool class corresponding to the given pool name.

        Raises:
            SDKException: If the input data type is invalid or if the specified index pool is not found.

        Example:
            >>> index_pools = IndexPools(commcell_object)
            >>> pool = index_pools.get("DefaultIndexPool")
            >>> print(f"Retrieved index pool: {pool}")
            >>> # The returned IndexPool object can be used for further operations

        #ai-gen-doc
        """
        if isinstance(pool_name, int):
            for index_pool_name in self.all_index_pools:
                if self.all_index_pools[index_pool_name] == pool_name:
                    return IndexPool(self._commcell_object, index_pool_name)
        elif isinstance(pool_name, str):
            if pool_name.lower() in self.all_index_pools:
                return IndexPool(self._commcell_object, pool_name.lower())
        else:
            raise SDKException('IndexPools', '101')
        raise SDKException('IndexPools', '102')

    def has_pool(self, pool_name: str) -> bool:
        """Check if an index pool with the specified name exists in the Commcell.

        Args:
            pool_name: The name of the index pool to check.

        Returns:
            True if an index pool with the given name exists, otherwise False.

        Example:
            >>> index_pools = IndexPools(commcell_object)
            >>> exists = index_pools.has_pool("DefaultIndexPool")
            >>> print(f"Pool exists: {exists}")
            # Output: Pool exists: True

        #ai-gen-doc
        """
        return pool_name.lower() in self.all_index_pools

    def add(self, pool_name: str, node_names: List[str], hac_name: str) -> 'IndexPool':
        """Create a new Index pool within the Commcell.

        This method creates an Index pool with the specified name, node names, and HAC cluster name.
        It returns an IndexPool object representing the newly created pool.

        Args:
            pool_name: The name to assign to the new index pool.
            node_names: List of node names (as strings) to include in the index pool.
            hac_name: The name of the HAC cluster to associate with the pool.

        Returns:
            IndexPool: An object representing the created index pool.

        Raises:
            SDKException: If the input data types are invalid, the response is unsuccessful, or the response is empty.

        Example:
            >>> index_pools = IndexPools(commcell_object)
            >>> pool = index_pools.add("MyIndexPool", ["NodeA", "NodeB"], "HACCluster1")
            >>> print(f"Created index pool: {pool}")
            >>> # The returned IndexPool object can be used for further pool management

        #ai-gen-doc
        """
        if not (isinstance(pool_name, str) and isinstance(node_names, list)
                and isinstance(hac_name, str)):
            raise SDKException('IndexPools', '101')
        req_json = deepcopy(IndexServerConstants.REQUEST_JSON)
        del req_json['solrCloudInfo']
        del req_json['cloudMetaInfos']
        req_json['type'] = 9
        req_json['cloudInfoEntity'] = {
            "cloudName": pool_name,
            "cloudDisplayName": pool_name
        }
        req_json['solrCloudPoolInfo'] = {
            'zookerEntity': {
                "_type_": 28,
                "clientGroupId": int(self._commcell_object.hac_clusters.get(hac_name).cluster_id),
                "clientGroupName": hac_name,
                "flags": {
                    "include": False
                }
            }
        }
        for node_name in node_names:
            node_obj = self._commcell_object.clients.get(node_name)
            node_data = {
                "opType": IndexServerConstants.OPERATION_ADD,
                "nodeClientEntity": {
                    "hostName": node_obj.client_hostname,
                    "clientId": int(node_obj.client_id),
                    "clientName": node_obj.client_name,
                    "_type_": 3
                },
                "nodeMetaInfos": [
                    {
                        "name": "ISENABLED",
                        "value": "false"
                    },
                    {
                        "name": "JVMMAXMEMORY",
                        "value": "8191"
                    },
                    {
                        "name": "PORTNO",
                        "value": "20000"
                    },
                    {
                        "name": "URL",
                        "value": ""
                    },
                    {
                        "name": "INDEXLOCATION",
                        "value": "NA"
                    }
                ]
            }
            req_json['cloudNodes'].append(node_data)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CLOUD_CREATE'], req_json
        )
        if flag:
            if response.json() and 'genericResp' in response.json():
                if response.json()['genericResp'] == {} and \
                        'cloudId' in response.json():
                    self.refresh()
                    return IndexPool(self._commcell_object, pool_name)
                o_str = 'Failed to create index pool. Error: "{0}"'.format(
                    response.json()['genericResp'])
                raise SDKException('Response', '102', o_str)
            raise SDKException('Response', '102')
        self._response_not_success(response)

    def delete(self, pool_name: str) -> None:
        """Delete an existing index pool cloud from the Commcell.

        Removes the specified index pool cloud by its name. If the pool does not exist or the operation fails,
        an exception is raised.

        Args:
            pool_name: The name of the index pool cloud to delete.

        Raises:
            SDKException: If the input data type is invalid, the response is unsuccessful, or the response is empty.

        Example:
            >>> index_pools = IndexPools(commcell_object)
            >>> index_pools.delete("MyIndexPool")
            >>> print("Index pool deleted successfully.")

        #ai-gen-doc
        """
        if not isinstance(pool_name, str):
            raise SDKException('IndexPools', '101')
        client = self.get(pool_name)
        cloud_id = client.cloud_id
        req_json = IndexServerConstants.REQUEST_JSON.copy()
        req_json["opType"] = IndexServerConstants.OPERATION_DELETE
        req_json['cloudInfoEntity']['cloudId'] = cloud_id
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CLOUD_DELETE'], req_json
        )
        if flag:
            if response.json() and 'genericResp' in response.json() \
                    and 'errorCode' not in response.json()['genericResp']:
                self.refresh()
                return
            if response.json() and 'genericResp' in response.json():
                raise SDKException(
                    'Response', '102', response.json()['genericResp'].get(
                        'errorMessage', ''))
            raise SDKException('Response', '102')
        self._response_not_success(response)


class IndexPool(object):
    """
    Class for managing and performing operations on a specific index pool.

    The IndexPool class provides an interface to interact with and manage index pools,
    including retrieving node information, modifying node configurations, and refreshing
    the pool state. It exposes several properties for accessing pool metadata and
    supports operations for handling nodes within the pool.

    Key Features:
        - Initialize with commcell object, pool name, and pool ID
        - Retrieve and display pool representation
        - Check response status for pool operations
        - Refresh the index pool state to reflect latest changes
        - Retrieve information about specific nodes in the pool
        - Modify node configurations and perform node operations
        - Access pool metadata such as pool ID, cloud ID, pool name, node names, and HAC cluster

    #ai-gen-doc
    """

    def __init__(self, commcell_obj: 'Commcell', pool_name: str, pool_id: str = None) -> None:
        """Initialize an IndexPool class instance.

        Args:
            commcell_obj: Instance of the Commcell class representing the Commcell connection.
            pool_name: Name of the index pool to manage.
            pool_id: Optional index pool client ID. If not provided, it will be determined automatically.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> index_pool = IndexPool(commcell, 'DefaultIndexPool')
            >>> # The IndexPool instance is now ready for use

        #ai-gen-doc
        """
        self.commcell = commcell_obj
        self._pool_name = pool_name
        self._pool_id = pool_id
        self.pool_client = None
        self.pool_properties = None
        self.pool_nodes = None
        self.refresh()

    def __repr__(self) -> str:
        """Return the string representation of the IndexPool instance.

        This method provides a developer-friendly string that represents the current
        IndexPool object, typically including key identifying information.

        Returns:
            A string representation of the IndexPool instance.

        Example:
            >>> pool = IndexPool()
            >>> print(repr(pool))
            <IndexPool object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        return "IndexPool class instance for Commcell"

    def _response_not_success(self, response: object) -> None:
        """Raise an exception if the HTTP response indicates failure (not status 200).

        This helper method should be called after making an HTTP request to check if the response
        was successful. If the response does not indicate success (status code 200), an SDKException
        is raised to signal the failure.

        Args:
            response: The HTTP response object to check.

        Raises:
            SDKException: If the response status code is not 200 (OK).

        Example:
            >>> pool = IndexPool()
            >>> response = pool._make_request()
            >>> pool._response_not_success(response)
            # If the response is not successful, an exception will be raised.

        #ai-gen-doc
        """
        raise SDKException(
            'Response',
            '101',
            self.commcell._update_response_(
                response.text))

    def refresh(self) -> None:
        """Reload the properties of the IndexPool instance.

        This method updates the IndexPool object's properties to reflect the latest state 
        from the underlying data source. Use this method to ensure that the IndexPool 
        instance has up-to-date information.

        Example:
            >>> index_pool = IndexPool()
            >>> index_pool.refresh()
            >>> print("IndexPool properties refreshed successfully")

        #ai-gen-doc
        """
        self.commcell.clients.refresh()
        if not self.commcell.clients.has_client(self.pool_name):
            raise SDKException('IndexPools', '102')
        self.pool_client = self.commcell.clients.get(self.pool_name)
        self._pool_id = self.pool_client.client_id
        self.pool_properties = self.pool_client.\
            properties['pseudoClientInfo']['distributedClusterInstanceProperties']['clusterConfig']['cloudInfo']
        self.pool_nodes = self.pool_properties['cloudNodes']

    def node_info(self, node_name: str) -> dict:
        """Retrieve information for a specific index pool node.

        Args:
            node_name: The name of the index pool node to retrieve information for.

        Returns:
            A dictionary containing details of the specified index pool node.

        Raises:
            SDKException: If the specified index pool node is not found.

        Example:
            >>> index_pool = IndexPool()
            >>> node_details = index_pool.node_info("NodeA")
            >>> print(node_details)
            {'nodeName': 'NodeA', 'status': 'Active', 'ip': '192.168.1.10'}

        #ai-gen-doc
        """
        for node_info in self.pool_nodes:
            if node_info['nodeClientEntity']['clientName'].lower() == node_name.lower():
                return node_info
        raise SDKException('IndexPools', '103')

    def modify_node(self, node_name: str, operation_type: int = IndexServerConstants.OPERATION_EDIT, node_params: Optional[List[Dict[str, Any]]] = None) -> None:
        """Modify the details of an index pool node.

        This method allows you to add, remove, or edit a node in the index pool by specifying the node name,
        the type of operation, and optional node parameters.

        Args:
            node_name: The name of the index pool node to modify.
            operation_type: The type of operation to perform:
                1 - Add a new node
                2 - Remove an existing node
                3 - Edit an existing node (default)
            node_params: Optional list of dictionaries containing properties for the index pool node.
                Each dictionary should have the following structure:
                    {
                        "name": <property_name>,
                        "value": <property_value>
                    }

        Raises:
            SDKException: If the response is not successful or is empty.

        Example:
            >>> # Add a new node to the index pool
            >>> node_properties = [
            ...     {"name": "ip_address", "value": "192.168.1.10"},
            ...     {"name": "port", "value": 8400}
            ... ]
            >>> index_pool.modify_node("NodeA", operation_type=1, node_params=node_properties)
            >>>
            >>> # Edit an existing node's properties
            >>> updated_properties = [
            ...     {"name": "ip_address", "value": "192.168.1.20"}
            ... ]
            >>> index_pool.modify_node("NodeA", operation_type=3, node_params=updated_properties)
            >>>
            >>> # Remove a node from the index pool
            >>> index_pool.modify_node("NodeA", operation_type=2)

        #ai-gen-doc
        """
        req_json = {
            'cloudId': self.cloud_id,
            'type': 9,
            'nodes': [{
                'status': 1,
                'opType': operation_type,
                'nodeClientEntity': {
                    'clientId': int(self.commcell.clients[node_name]['id']),
                    'clientName': node_name
                },
                'nodeMetaInfos': []
            }]
        }
        if node_params:
            req_json['nodes'][0]['nodeMetaInfos'] = node_params
        flag, response = self.commcell._cvpysdk_object.make_request(
            'POST', self.commcell._services['CLOUD_NODE_UPDATE'],
            req_json
        )
        if flag:
            if response.json() is not None:
                if 'errorCode' not in response.json():
                    self.refresh()
                    return
        self._response_not_success(response)

    @property
    def pool_id(self) -> str:
        """Get the client ID of the index pool.

        Returns:
            str: The unique client ID associated with the index pool.

        Example:
            >>> index_pool = IndexPool()
            >>> pool_id = index_pool.pool_id  # Use dot notation for property access
            >>> print(f"Index pool client ID: {pool_id}")

        #ai-gen-doc
        """
        return self._pool_id

    @property
    def cloud_id(self) -> int:
        """Get the cloud ID associated with the index pool.

        Returns:
            The cloud ID of the index pool as an integer.

        Example:
            >>> index_pool = IndexPool()
            >>> cloud_id = index_pool.cloud_id  # Use dot notation for property access
            >>> print(f"Index pool cloud ID: {cloud_id}")

        #ai-gen-doc
        """
        return self.pool_properties['cloudInfoEntity']['cloudId']

    @property
    def pool_name(self) -> str:
        """Get the name of the index pool.

        Returns:
            The name of the index pool as a string.

        Example:
            >>> index_pool = IndexPool()
            >>> name = index_pool.pool_name  # Use dot notation for property access
            >>> print(f"Index pool name: {name}")

        #ai-gen-doc
        """
        return self._pool_name

    @property
    def node_names(self) -> list:
        """Get the list of index pool node names.

        Returns:
            list: A list containing the names of all nodes in the index pool.

        Example:
            >>> index_pool = IndexPool()
            >>> names = index_pool.node_names
            >>> print(f"Index pool nodes: {names}")

        #ai-gen-doc
        """
        result = []
        for node_info in self.pool_nodes:
            result.append(node_info['nodeClientEntity']['clientName'])
        return result

    @property
    def hac_cluster(self) -> str:
        """Get the HAC (High Availability Cluster) name assigned to the index pool.

        Returns:
            The name of the HAC cluster associated with this index pool as a string.

        Example:
            >>> index_pool = IndexPool()
            >>> cluster_name = index_pool.hac_cluster  # Access the HAC cluster name property
            >>> print(f"HAC Cluster Name: {cluster_name}")

        #ai-gen-doc
        """
        return self.pool_properties['solrCloudPoolInfo']['zookerEntity']['clientGroupName']