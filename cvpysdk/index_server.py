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

"""File for performing index server related operations on the commcell

IndexServers, IndexServer and _Roles are 3 classes defined in this file

IndexServers:   Class for representing all the index servers associated with the commcell

IndexServer:    Class for a instance of a single index server of the commcell

_Roles:         Class for storing all the cloud role details

"IndexServerOSType" is the enum class used to represent os type of IS

IndexServers
============

    __init__()                          --  initialize object of IndexServers class associated with
                                            the commcell

    __str()                             --  returns all the index servers of the commcell

    __repr__()                          --  returns the string to represent the instance

    __len__()                           --  returns the number of index servers associated

    _get_index_servers()                --  gets all the index server associated with the commcell

    _response_not_success()             --  raise exception when response is not 200

    _get_all_roles()                    --  creates an instance of _Roles class

    has()                               --  returns whether the index server is present or not

    get()                               --  returns a IndexServer object for given cloud name

    create()                            --  creates a index server within the commcell

    delete()                            --  deletes a index server associated with commcell

    update_roles_data()                 --  fetches the cloud roles data from commcell

    get_properties()                    --  returns a dict of data of index server for the given
                                            cloud name

    refresh()                           --  refresh the index servers associated with commcell

    prune_orphan_datasources()          --  Deletes all the orphan datasources

IndexServers Attributes
-----------------------

    **all_index_servers**               --  returns the dictionary consisting of all the index
                                            servers associated with the commcell and there details

    **roles_data**                      --  returns the list of cloud roles details


IndexServer
===========

    __init()__                          --  initializes the object with the specified commcell
                                            object, index server name and the cloud id

    __repr__()                          --  returns the index server's name, the instance is
    associated with

    _get_cloud_id()                     --  gets the cloud id

    _get_properties()                   --  gets all the properties of the index server

    refresh()                           --  refresh all the properties of client

    update_roles_data()                 --  fetches the cloud roles data from commcell

    modify()                            --  to modify the index server node details

    change_plan()                       --  changes the plan of a given index server

    update_role()                       --  to update the roles assigned to cloud

    delete_docs_from_core()             --  Deletes the docs from the given core name on index server depending
                                            on the select dict passed

    hard_commit                         --  do hard commit on specified index server solr core

    get_health_indicators()             --  get health indicators for index server node by client name

    get_all_cores                       --  gets all the cores in index server

    _create_solr_query()                --  Create solr search query based on inputs provided

    execute_solr_query()                --  Creates solr url based on input and executes it on solr on given core

    get_index_node()                    --  returns an Index server node object for given node name

    get_os_info()                       --  returns the OS type for the Index server

    get_plan_info()                     --  Returns the plan information of the index server

    __form_field_query()                --  returns the query with the key and value passed

IndexServer Attributes
----------------------

    **properties**                      --  returns the properties of this index server

    **roles_data**                      --  returns all the available cloud roles data

    **host_name**                       --  returns the host name for the index server

    **internal_cloud_name**             --  returns the internal cloud name

    **client_name**                     --  returns the client name for index server

    **server_url**                      --  returns the content indexing server url

    **type**                            --  returns the type of the index server

    **base_port**                       --  returns the base port of this index server

    **client_id**                       --  returns the client id for this index server

    **roles**                           --  returns the array of roles installed
                                            with the index server within the commcell

    **cloud_id**                        --  returns the cloud id of the index server

    **server_type**                     --  returns the server type of the index server

    **engine_name**                     --  returns the engine name that is index server name

    **index_server_client_id**          --  returns the index server client id

    **role_display_name**               --  display name of roles

    **is_cloud**                        --  returns boolean True if the Index server is cloud else returns False

    **node_count**                      --  returns the number of Index server nodes

    **os_info**                         --  returns the OS type for the Index server

    **plan_name**                       --  Returns the plan name associated with index server

    **fs_collection**                   --  Returns the multinode collection name of File System Index


IndexNode
=========

    __init__()                          --  initializes the class with commcell object
                                            Index server cloud id and Node client name

    refresh()                           --  refreshes the attributes

    modify()                            --  to modify the index server node details

IndexNode Attributes
--------------------

    **node_name**                       --  returns Index server node client name

    **node_id**                         --  returns Index server node client id

    **solr_port**                       --  returns port number Solr is running on the\
                                            Index server node

    **solr_url**                        --  returns Solr URL for Index server node

    **roles**                           --  returns the array of roles installed
                                            with the index server within the commcell

    **index_location**                  --  returns Index directory for the Index server Node

    **jvm_memory**                      --  returns Solr JVM memory for the Index server Node

_Roles
======

    __init__()                          --  initializes the class with commcell object

    refresh()                           --  refreshes the attributes

    _get_all_roles()                    --  fetches the cloud roles data from commcell

    get_role_id()                       --  returns role id for given role name

    update_roles_data()                 --  fetches the cloud roles data from commcell

_Roles Attributes
-----------------

    **roles_data**                      --  returns the list of details of all cloud roles
    """
import json

import enum
import http.client as httplib
from copy import deepcopy

from .exception import SDKException
from .datacube.constants import IndexServerConstants

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
if TYPE_CHECKING:
    import requests
    from cvpysdk.commcell import Commcell


class IndexServers(object):
    """
    Manages all index servers associated with a CommCell environment.

    This class provides a comprehensive interface for interacting with index servers,
    including retrieving, creating, updating, and deleting index server configurations.
    It also supports role management, property retrieval, and maintenance operations
    such as pruning orphaned data sources.

    Key Features:
        - Retrieve and list all index servers and their roles
        - Access index server and role data via properties
        - Create new index servers with specified configurations
        - Delete existing index servers by cloud name
        - Check for the existence of an index server
        - Get properties of a specific index server
        - Update roles data for index servers
        - Refresh the index server information from the CommCell
        - Prune orphaned data sources associated with index servers
        - Utility methods for string representation and length

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize an IndexServers object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> index_servers = IndexServers(commcell)
            >>> print("IndexServers object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._all_index_servers = None
        self._roles_obj = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all index servers in the Commcell.

        The returned string lists all index servers along with their associated roles.

        Returns:
            A string containing details of all index servers and their roles in the Commcell.

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'IS Name')
        index = 1
        for index_server in self._all_index_servers:
            representation_string += '{:^5}\t{:^20}\n'.format(
                index, index_server['engineName'])
            index += 1
        return representation_string

    def __repr__(self) -> str:
        """Return the string representation of the IndexServers instance.

        This method provides a developer-friendly string that represents the current
        IndexServers object, useful for debugging and logging purposes.

        Returns:
            A string representation of the IndexServers instance.

        #ai-gen-doc
        """
        return "IndexServers class instance for Commcell"

    def __len__(self) -> int:
        """Get the number of index servers associated with the Commcell.

        Returns:
            The total count of index servers managed by this IndexServers instance.

        #ai-gen-doc
        """
        return len(self._all_index_servers)

    def _response_not_success(self, response: 'requests.Response') -> None:
        """Raise an exception if the HTTP response is not successful (status code 200).

        This helper method checks the provided response object and raises an SDKException
        if the response does not indicate a successful HTTP request.

        Args:
            response: The response object to check for success.

        Raises:
            SDKException: If the response status code is not 200 (OK).

        #ai-gen-doc
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(response.text)
        )

    def _get_index_servers(self) -> None:
        """Retrieve all index servers available on the Commcell.

        Returns:
            None

        Raises:
            SDKException: If the retrieval of the index server list fails or the response is not successful.

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['GET_ALL_INDEX_SERVERS'])
        if flag:
            if response.json() and 'listOfCIServer' in response.json():
                for item in response.json()['listOfCIServer']:
                    if item['cloudID'] in self._all_index_servers:
                        # Add only unique roles to list
                        if 'version' in item and item['version'] not in self._all_index_servers[item['cloudID']]['version']:
                            self._all_index_servers[item['cloudID']]['version'].append(item['version'])
                        # check whether we have populated node details earlier. if not, add it to
                        # exisitng respective fields
                        if item['clientName'] not in self._all_index_servers[item['cloudID']]['clientName']:

                            self._all_index_servers[item['cloudID']]['clientId'].append(item['clientId'])
                            self._all_index_servers[item['cloudID']]['clientName'].append(item['clientName'])
                            self._all_index_servers[item['cloudID']]['hostName'].append(item['hostName'])
                            self._all_index_servers[item['cloudID']]['cIServerURL'].append(item['cIServerURL'])
                            self._all_index_servers[item['cloudID']]['basePort'].append(item['basePort'])

                    else:
                        item['version'] = [item.get('version', '')]
                        item['clientId'] = [item['clientId']]
                        item['clientName'] = [item['clientName']]
                        item['hostName'] = [item['hostName']]
                        item['cIServerURL'] = [item['cIServerURL']]
                        item['basePort'] = [item['basePort']]
                        self._all_index_servers[item['cloudID']] = item
            else:
                self._all_index_servers = {}
        else:
            self._response_not_success(response)

    def _get_all_roles(self) -> None:
        """Create and return an instance of the _Roles class for the IndexServer.

        This method initializes the _Roles class and associates it with the IndexServer instance.

        Returns:
            None

        #ai-gen-doc
        """
        self._roles_obj = _Roles(self._commcell_object)

    @property
    def all_index_servers(self) -> dict:
        """Get details of all index servers associated with the Commcell.

        Returns:
            dict: A dictionary containing details of all index servers, where each key is a cloud ID
            and the value is a dictionary of properties for that index server.

            Example structure:
                {
                    "cloud_id_1": {
                        "engineName": "IndexServer1",
                        "internalCloudName": "InternalName1",
                        ...
                    },
                    "cloud_id_2": {
                        "engineName": "IndexServer2",
                        "cloudID": "cloud_id_2",
                        ...
                    }
                }

        #ai-gen-doc
        """
        return self._all_index_servers

    @property
    def roles_data(self) -> List[Dict[str, Any]]:
        """Get details of all cloud roles associated with the IndexServers.

        Returns:
            List of dictionaries, each containing information about a cloud role.

        #ai-gen-doc
        """
        return self._roles_obj.roles_data

    def refresh(self) -> None:
        """Reload the properties and state of the IndexServers class.

        This method refreshes the internal data of the IndexServers instance, ensuring that 
        any changes made externally are reflected in the current object.

        #ai-gen-doc
        """
        self._all_index_servers = {}
        self._get_index_servers()
        if not self._roles_obj:
            self._get_all_roles()

    def update_roles_data(self) -> None:
        """Synchronize all cloud role details with the Commcell.

        This method updates the internal data to reflect the latest cloud roles 
        information from the Commcell, ensuring that any changes or new roles 
        are accurately represented.

        #ai-gen-doc
        """
        self._roles_obj.update_roles_data()

    def get_properties(self, cloud_name: str) -> dict:
        """Retrieve all details of an index server by its cloud name.

        Args:
            cloud_name: The cloud name of the index server whose properties are to be fetched.

        Returns:
            A dictionary containing details of the specified index server.

        #ai-gen-doc
        """
        for index_server in self._all_index_servers:
            if self._all_index_servers[index_server]['engineName'] == cloud_name:
                return self._all_index_servers[index_server]
        raise SDKException('IndexServers', '102')

    def has(self, cloud_name: str) -> bool:
        """Check if an index server with the specified name exists in the Commcell.

        Args:
            cloud_name: The engine name of the index server to check.

        Returns:
            True if an index server with the given name is associated with the Commcell, otherwise False.

        Raises:
            SDKException: If the data type of the input is not valid.

        #ai-gen-doc
        """
        if isinstance(cloud_name, str):
            for index_server in self._all_index_servers:
                if self._all_index_servers[index_server]["engineName"].lower() == cloud_name.lower():
                    return True
            return False
        raise SDKException('IndexServers', '101')

    def get(self, cloud_data: Union[int, str]) -> 'IndexServer':
        """Retrieve an IndexServer object by cloud name or cloud ID.

        Args:
            cloud_data: The cloud name (str) or cloud ID (int) of the index server to retrieve.

        Returns:
            IndexServer: An instance representing the index server identified by the provided cloud name or ID.

        Raises:
            SDKException: If the index server is not found or if the input data type is invalid.

        #ai-gen-doc
        """
        if isinstance(cloud_data, int):
            if cloud_data in self._all_index_servers:
                return IndexServer(
                    self._commcell_object,
                    self._all_index_servers[cloud_data]['engineName'],
                    cloud_data)
            SDKException('IndexServers', '102')
        elif isinstance(cloud_data, str):
            name = cloud_data.lower()
            for itter in self._all_index_servers:
                if self._all_index_servers[itter]['engineName'].lower(
                ) == name:
                    return IndexServer(
                        self._commcell_object,
                        self._all_index_servers[itter]['engineName'],
                        self._all_index_servers[itter]['cloudID'])
            raise SDKException('IndexServers', '102')
        raise SDKException('IndexServers', '101')

    def create(
        self,
        index_server_name: str,
        index_server_node_names: list,
        index_directory: list,
        index_server_roles: list,
        index_pool_name: str = None,
        is_cloud: bool = False,
        cloud_param: list = None
    ) -> None:
        """Create a new index server within the Commcell environment.

        This method provisions an index server with the specified configuration, including node clients,
        index directories, assigned roles, and optional cloud or custom parameters.

        Args:
            index_server_name: Name to assign to the new index server.
            index_server_node_names: List of client names to be used as index server nodes.
            index_directory: List of index directory paths for the index server nodes. 
                - If a single path is provided, it is used for all nodes.
                - If multiple paths are provided, each path is assigned to the corresponding node.
            index_server_roles: List of role names to assign to the index server.
            index_pool_name: (Optional) Name of the index pool to use for a cloud index server.
            is_cloud: If True, creates a cloud mode index server.
            cloud_param: (Optional) List of custom parameters to include in the index server meta info.
                Each parameter should be a dictionary with "name" and "value" keys.

        Raises:
            SDKException: If any input parameter is invalid, or if the server response is unsuccessful or empty.

        Example:
            >>> index_servers = IndexServers(commcell_object)
            >>> index_servers.create(
            ...     index_server_name="MyIndexServer",
            ...     index_server_node_names=["node1", "node2"],
            ...     index_directory=["/index/path1", "/index/path2"],
            ...     index_server_roles=["Search", "Analytics"],
            ...     index_pool_name="MyIndexPool",
            ...     is_cloud=True,
            ...     cloud_param=[{"name": "customParam", "value": "customValue"}]
            ... )
            >>> print("Index server created successfully.")

        #ai-gen-doc
        """
        if not (isinstance(index_server_roles, list) and isinstance(index_server_node_names, list)
                and isinstance(index_server_name, str)):
            raise SDKException('IndexServers', '101')
        if isinstance(index_directory, str):
            index_directory = index_directory.split(",")
        node_count = len(index_server_node_names)
        index_directories_count = len(index_directory)
        if index_directories_count != 1 and index_directories_count != node_count:
            raise SDKException('IndexServers', '101')
        cloud_meta_infos = {
            'REPLICATION': '1',
            'LANGUAGE': '0'
        }
        node_meta_infos = {
            'PORTNO': IndexServerConstants.DEFAULT_SOLR_PORT,
            'JVMMAXMEMORY': IndexServerConstants.DEFAULT_JVM_MAX_MEMORY
        }
        role_meta_infos = {}
        req_json = deepcopy(IndexServerConstants.REQUEST_JSON)
        req_json['cloudInfoEntity'] = {
            'cloudName': index_server_name,
            'cloudDisplayName': index_server_name
        }
        if is_cloud:
            index_pool_obj = self._commcell_object.index_pools[index_pool_name]
            req_json['type'] = 5
            req_json['solrCloudInfo']['cloudPoolInfo'] = {
                'cloudId': int(index_pool_obj['pool_id'])
            }
            cloud_meta_infos['INDEXLOCATION'] = index_directory[0]
        for node_name_index in range(len(index_server_node_names)):
            node_name = index_server_node_names[node_name_index]
            location_index = node_name_index - (node_name_index//index_directories_count)
            node_obj = self._commcell_object.clients[node_name]
            node_data = {
                "opType": IndexServerConstants.OPERATION_ADD,
                "nodeClientEntity": {
                    "hostName": node_obj['hostname'],
                    "clientId": int(node_obj['id']),
                    "clientName": node_name
                },
                'nodeMetaInfos': [{
                    "name": "INDEXLOCATION",
                    "value": index_directory[location_index]
                }]
            }
            for node_info in node_meta_infos:
                node_data['nodeMetaInfos'].append({
                    'name': node_info,
                    'value': str(node_meta_infos[node_info])
                })
            req_json['cloudNodes'].append(node_data)
        for role in index_server_roles:
            role_id = self._roles_obj.get_role_id(role)
            if not role_id:
                raise SDKException('IndexServers', '103')
            role_data = {
                "roleId": role_id,
                "roleName": role,
                "operationType": IndexServerConstants.OPERATION_ADD,
                'roleMetaInfos': []
            }
            for role_info in role_meta_infos:
                role_data['roleMetaInfos'].append({
                    'name': role_info,
                    'value': role_meta_infos[role_info]
                })
            req_json['solrCloudInfo']['roles'].append(role_data)
        if cloud_param:
            for param in cloud_param:
                if param['name'] in cloud_meta_infos:
                    del cloud_meta_infos[param['name']]
                req_json['cloudMetaInfos'].append(param)
        for cloud_info in cloud_meta_infos:
            req_json['cloudMetaInfos'].append({
                'name': cloud_info,
                'value': cloud_meta_infos[cloud_info]
            })
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CLOUD_CREATE'], req_json)
        if flag:
            if response.json():
                error_code = response.json()['genericResp']['errorCode']
                error_string = response.json()['genericResp']['errorMessage']
                if error_code == 0:
                    self.refresh()
                    self._commcell_object.clients.refresh()
                    self._commcell_object.datacube.refresh_engine()
                else:
                    o_str = 'Failed to create Index Server. Error: "{0}"'.format(
                        error_string)
                    raise SDKException('IndexServers', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            self._response_not_success(response)

    def delete(self, cloud_name: str) -> None:
        """Delete or remove an index server from the Commcell.

        Args:
            cloud_name: The name of the index server (cloud) to be removed from the Commcell.

        Raises:
            SDKException: If the input data type is invalid, the response is unsuccessful, or the response is empty.

        #ai-gen-doc
        """
        if not isinstance(cloud_name, str):
            raise SDKException('IndexServers', '101')
        cloud_id = self.get(cloud_name).cloud_id
        req_json = deepcopy(IndexServerConstants.REQUEST_JSON)
        req_json["opType"] = IndexServerConstants.OPERATION_DELETE
        req_json['cloudInfoEntity']['cloudId'] = cloud_id
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CLOUD_DELETE'], req_json
        )
        if flag:
            if response.json() and 'genericResp' in response.json() \
                    and 'errorCode' not in response.json()['genericResp']:
                self.refresh()
                self._commcell_object.clients.refresh()
                self._commcell_object.datacube.refresh_engine()
                return
            if response.json() and 'genericResp' in response.json():
                raise SDKException(
                    'Response', '102', response.json()['genericResp'].get(
                        'errorMessage', ''))
            raise SDKException('Response', '102')
        self._response_not_success(response)

    def prune_orphan_datasources(self) -> None:
        """Delete all orphan datasources associated with the IndexServers.

        This method removes datasources that are no longer associated with any active index server.
        It is useful for cleaning up unused or stale datasources to maintain optimal system performance.

        Raises:
            SDKException: If the operation fails, if the response is empty, or if the response indicates failure.

        #ai-gen-doc
        """
        prune_datasource = self._services['PRUNE_DATASOURCE']
        request_json = IndexServerConstants.PRUNE_REQUEST_JSON
        flag, response = self._cvpysdk_object.make_request(
            'POST', prune_datasource, request_json)
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException('IndexServers', '104', 'Failed to prune orphan datasources')
                return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101', self._update_response_(response.text))


class IndexServerOSType(enum.Enum):
    """
    Enumeration for Index Server Operating System Types.

    This enum class defines the possible operating system types that an Index Server can run on.
    It is intended to provide a clear and type-safe way to specify or check the OS type in code
    that interacts with Index Servers.

    Key Features:
        - Enumerates supported Index Server OS types
        - Ensures type safety and code clarity when handling OS types
        - Useful for configuration, validation, and conditional logic based on OS

    #ai-gen-doc
    """
    WINDOWS = "Windows"
    UNIX = "Unix"
    MIXED = "Mixed"


class IndexServer(object):
    """
    Class for managing and performing operations on a specific index server.

    The IndexServer class provides a comprehensive interface for interacting with
    and managing an index server within a cloud or on-premises environment. It supports
    operations such as modifying index server configurations, managing roles and nodes,
    executing Solr queries, handling document deletion and commits, and retrieving
    various server and client properties.

    Key Features:
        - Initialization and representation of index server objects
        - Retrieval and refresh of index server properties and health indicators
        - Management of roles, nodes, and index locations
        - Plan management, including changing and retrieving plan information
        - Execution of Solr queries and creation of Solr query parameters
        - Document management within Solr cores, including deletion and hard commits
        - Access to detailed server, client, and cloud properties via properties
        - Retrieval of OS information and index node details
        - Support for both cloud and non-cloud index server types

    #ai-gen-doc
    """

    def __init__(self, commcell_obj: 'Commcell', name: str, cloud_id: int = None) -> None:
        """Initialize an IndexServer class instance.

        Args:
            commcell_obj: Instance of the Commcell class representing the connected Commcell.
            name: Name of the index server.
            cloud_id: Optional cloud ID associated with the index server. Defaults to None.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> index_server = IndexServer(commcell, 'MyIndexServer')
            >>> # With cloud_id specified
            >>> index_server_with_cloud = IndexServer(commcell, 'CloudIndexServer', cloud_id=123)

        #ai-gen-doc
        """
        self._engine_name = name
        self._commcell_obj = commcell_obj
        self._cvpysdk_object = self._commcell_obj._cvpysdk_object
        self._services = self._commcell_obj._services
        if cloud_id:
            self._cloud_id = cloud_id
        else:
            self._cloud_id = self._get_cloud_id()
        self._properties = None
        self._roles_obj = None
        self.plan_info = None
        self.os_type = None
        self.refresh()

    def __repr__(self) -> str:
        """Return the string representation of the IndexServer instance.

        This method provides a developer-friendly string that represents the current
        IndexServer object, which can be useful for debugging and logging purposes.

        Returns:
            A string representation of the IndexServer instance.

        #ai-gen-doc
        """
        return 'IndexServer class instance for index server: "{0}"'.format(
            self._engine_name)

    def _get_cloud_id(self) -> int:
        """Retrieve the cloud ID associated with the index server.

        Returns:
            The cloud ID as an integer for the current index server instance.

        #ai-gen-doc
        """
        return self._commcell_obj.index_servers.get(self._engine_name).cloud_id

    def _get_properties(self) -> None:
        """Retrieve the properties of the index server.

        Returns:
            A dictionary containing the properties and configuration details of the index server.

        #ai-gen-doc
        """
        self._properties = self._commcell_obj.index_servers.get_properties(
            self._engine_name)

    def refresh(self) -> None:
        """Reload the properties of the index server to ensure the latest configuration is available.

        This method refreshes the internal state of the IndexServer object, updating its properties 
        from the underlying data source. Use this method if you suspect the index server's properties 
        have changed, and you want to ensure you are working with the most current information.

        #ai-gen-doc
        """
        self._commcell_obj.index_servers.refresh()
        self._get_properties()
        if self.os_type is None:
            self.os_type = self.get_os_info()
        if not self._roles_obj:
            self._roles_obj = _Roles(self._commcell_obj)
        if self.plan_info is None:
            self.plan_info = self.get_plan_info()

    def update_roles_data(self) -> None:
        """Synchronize the cloud roles data with the Commcell.

        This method updates the roles data for the IndexServer by fetching the latest
        information from the Commcell. Use this method to ensure that the IndexServer
        has the most current cloud roles configuration.

        #ai-gen-doc
        """
        self._roles_obj.update_roles_data()

    def modify(self, index_location: str, node_name: str, node_params: List[Dict]) -> None:
        """Modify the properties of an index server.

        Updates the configuration of the index server by specifying a new data directory,
        node name, and a set of parameters to be applied to the node.

        Args:
            index_location: The file system path to the index server's data directory.
            node_name: The name of the index server node to modify.
            node_params: A list of dictionary containing the parameters to update
                with "name" and "value" keys, for example:
                [
                    {
                        "name": "property_name",
                        "value": "property_value"
                    }
                ]

        Raises:
            SDKException: If the response from the server is unsuccessful or empty.

        Example:
            >>> index_server = IndexServer()
            >>> params = [
            ...     {"name": "maxConnections", "value": 100},
            ...     {"name": "enableLogging", "value": True}
            ... ]
            >>> index_server.modify("/data/index", "NodeA", params)
            >>> print("Index server properties updated successfully.")

        #ai-gen-doc
        """
        json_req = deepcopy(IndexServerConstants.REQUEST_JSON)
        json_req['opType'] = IndexServerConstants.OPERATION_EDIT
        json_req['cloudNodes'] = [{
            "opType": IndexServerConstants.OPERATION_EDIT,
            "nodeClientEntity": {
                "clientId": int(self._commcell_obj.clients.get(node_name).client_id)
            },
            "nodeMetaInfos": [
                {
                    "name": "INDEXLOCATION",
                    "value": index_location
                }
            ]
        }]
        json_req['cloudInfoEntity']['cloudId'] = self.cloud_id
        for param in node_params:
            json_req['cloudNodes'][0]['nodeMetaInfos'].append(param)
        flag, response = self._cvpysdk_object.make_request(
            "POST", self._services['CLOUD_MODIFY'], json_req)
        if flag:
            if response.json():
                if 'cloudId' in response.json():
                    self.refresh()
                    return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101')

    def change_plan(self, plan_name: str) -> None:
        """Modify the plan associated with the index server.

        Changes the plan used by the index server to the specified plan name.

        Args:
            plan_name: The name of the plan to assign to the index server.

        Raises:
            SDKException: If the response is not successful, the response is empty,
                or if a plan with the given name does not exist.

        #ai-gen-doc
        """
        if not self._commcell_obj.plans.has_plan(plan_name):
            raise SDKException(
                'Plan', '102', f"Plan with name [{plan_name}] doesn't exist")
        request_json = {
            "opType": IndexServerConstants.OPERATION_EDIT,
            "type": 1,
            "planInfo": {
                "planId": int(self._commcell_obj.plans.get(plan_name).plan_id)
            },
            "cloudInfoEntity": {
                "cloudId": self.cloud_id
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            "POST", self._services['CLOUD_MODIFY'], request_json)
        if flag:
            if response.json():
                if 'cloudId' in response.json():
                    self.refresh()
                    return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101')

    def update_role(self, props: Optional[List[Dict[str, Any]]] = None) -> None:
        """Update the roles assigned to the Index Server.

        This method allows you to add or remove roles for the Index Server by providing
        a list of dictionaries specifying the role name and the operation type.

        Args:
            props: Optional list of dictionaries, each containing:
                - "roleName": The name of the role to add or remove (str).
                - "operationType": The operation type (int), where
                    1 indicates adding a role,
                    2 indicates removing a role.

                Example:
                    [
                        {"roleName": "Search", "operationType": 1},
                        {"roleName": "Analytics", "operationType": 2}
                    ]

        Raises:
            SDKException: If the response from the server is empty or not successful.

        Example:
            >>> index_server = IndexServer()
            >>> roles_to_update = [
            ...     {"roleName": "Search", "operationType": 1},
            ...     {"roleName": "Analytics", "operationType": 2}
            ... ]
            >>> index_server.update_role(roles_to_update)
            >>> print("Roles updated successfully.")

        #ai-gen-doc
        """
        json_req = {"cloudId": self.cloud_id, "roles": []}
        if props:
            for prop in props:
                role_id = self._roles_obj.get_role_id(prop['roleName'])
                if not role_id:
                    raise SDKException('IndexServers', '103')
                prop['roleId'] = role_id
                json_req['roles'].append(prop)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CLOUD_ROLE_UPDATE'], json_req
        )
        if flag:
            if response.json() and 'errorCode' in response.json():
                if response.json()['errorCode'] == 0:
                    self.refresh()
                    return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101')

    def delete_docs_from_core(self, core_name: str, select_dict: Optional[dict] = None) -> None:
        """Delete documents from the specified Solr core on the index server.

        This method removes documents from the given Solr core based on the provided selection criteria.
        If no selection dictionary is provided, all documents in the core will be deleted.

        Args:
            core_name: The name of the Solr core from which documents should be deleted.
            select_dict: Optional dictionary specifying the query to select documents for deletion.
                If not provided, the default query "*:*" will be used to delete all documents.

        Raises:
            SDKException: If the input data is invalid, if the index server is a cloud server (not implemented),
                if the response is empty, or if the response indicates failure.

        Example:
            >>> index_server = IndexServer()
            >>> # Delete all documents from the 'my_core' Solr core
            >>> index_server.delete_docs_from_core('my_core')
            >>> # Delete documents matching a specific query
            >>> query = {'query': 'field:value'}
            >>> index_server.delete_docs_from_core('my_core', select_dict=query)

        #ai-gen-doc
        """
        if not isinstance(core_name, str):
            raise SDKException('IndexServers', '101')
        if self.is_cloud:
            raise SDKException('IndexServers', '104', "Not implemented for solr cloud")
        json_req = {"delete": {"query": self._create_solr_query(select_dict).replace("q=", "").replace("&wt=json", "")}}
        baseurl = f"{self.server_url[0]}/solr/{core_name}/update?commitWithin=1000&overwrite=true&wt=json"
        flag, response = self._cvpysdk_object.make_request("POST", baseurl, json_req)
        if flag and response.json():
            if 'error' in response.json():
                raise SDKException('IndexServers', '104', f' Failed with error message - '
                                                          f'{response.json().get("error").get("msg")}')
            if 'responseHeader' in response.json():
                commitstatus = str(response.json().get("responseHeader").get("status"))
                if int(commitstatus) != 0:
                    raise SDKException('IndexServers', '104',
                                       f"Deleting docs from the core returned bad status - {commitstatus}")
                return
        raise SDKException('IndexServers', '111')

    def hard_commit(self, core_name: str) -> None:
        """Perform a hard commit operation for the specified Solr core on the index server.

        This method triggers a hard commit, ensuring that all recent changes to the given Solr core 
        are flushed and made durable on the index server.

        Args:
            core_name: The name of the Solr core to commit.

        Raises:
            SDKException: If the input data is invalid, if the index server is a cloud instance 
                (not implemented), if the response is empty, or if the response indicates failure.

        #ai-gen-doc
        """
        if not isinstance(core_name, str):
            raise SDKException('IndexServers', '101')
        if self.is_cloud:
            raise SDKException('IndexServers', '104', "Not implemented for solr cloud")
        baseurl = f"{self.server_url[0]}/solr/{core_name}/update?commit=true"
        flag, response = self._cvpysdk_object.make_request("GET", baseurl)
        if flag and response.json():
            if 'error' in response.json():
                raise SDKException('IndexServers', '104', "Hard commit returned error")
            if 'responseHeader' in response.json():
                commitstatus = str(response.json()['responseHeader']['status'])
                if int(commitstatus) != 0:
                    raise SDKException('IndexServers', '104', "Hard commit returned bad status")
                return
        raise SDKException('IndexServers', '104', "Something went wrong with hard commit")

    def get_health_indicators(self, client_name: Optional[str] = None) -> str:
        """Retrieve health indicators for an index server node by client name.

        Args:
            client_name: Optional; the name of the client node for which health indicators are requested.
                If not provided, the method may return health indicators for all nodes or raise an exception
                depending on the index server configuration.

        Returns:
            A JSON string containing the health indicators for the specified index server node.

        Raises:
            SDKException: If input data is invalid, if client name is required but not provided,
                if the response is unsuccessful, or if the response is empty.

        #ai-gen-doc
        """
        server_url = self.server_url[0]
        response = None
        if self.is_cloud or len(self.client_name) > 1:
            if client_name is None:
                raise SDKException('IndexServers', '104', 'Client name param missing for solr cloud')
            if client_name not in self.client_name:
                raise SDKException('IndexServers', '104', 'client name not found in this index server cloud')
            server_url = self.server_url[self.client_name.index(client_name)]
        baseurl = f"{server_url}/solr/rest/admin/healthsummary"
        headers = {
            'Accept': 'application/xml'
        }
        flag, response = self._cvpysdk_object.make_request("GET", headers=headers, url=baseurl)
        if flag:
            return response
        raise SDKException('IndexServers', '104', "Could not get health summary for [{}]".format(client_name))

    def get_all_cores(self, client_name: Optional[str] = None) -> (List, str):
        """Retrieve all core names and their details from the index server.

        Args:
            client_name: Optional; the name of the client node. This parameter is required for Solr cloud mode or
            multi-node Index Server configurations.

        Returns:
            A list of core names if only core names are requested, or a dictionary containing details about each core.

        Raises:
            SDKException: If the input data is invalid, if the client name is not provided for an index server cloud,
            if the response is unsuccessful, or if the response is empty.

        Example:
            >>> index_server = IndexServer()
            >>> core_list = index_server.get_all_cores()
            >>> print(core_list)
            >>> # For Solr cloud or multi-node Index Server:
            >>> core_details = index_server.get_all_cores(client_name="node01")
            >>> print(core_details)

        #ai-gen-doc
        """
        server_url = self.server_url[0]
        if self.is_cloud or len(self.client_name) > 1:
            if client_name is None:
                raise SDKException('IndexServers', '104', 'Client name param missing for solr cloud')
            if client_name not in self.client_name:
                raise SDKException('IndexServers', '104', 'client name not found in this index server cloud')
            server_url = self.server_url[self.client_name.index(client_name)]
        core_names = []
        baseurl = f"{server_url}/solr/admin/cores"
        flag, response = self._cvpysdk_object.make_request("GET", baseurl)
        if flag and response.json():
            if 'error' in response.json():
                raise SDKException('IndexServers', '104', "Unable to get core names from index server")
            if 'status' in response.json():
                for core in response.json()['status']:
                    core_names.append(core)
                return core_names, response.json()['status']
        raise SDKException('IndexServers', '104', "Something went wrong while getting core names")

    def _create_solr_query(
        self,
        select_dict: Optional[Dict[str, Any]] = None,
        attr_list: Optional[set] = None,
        op_params: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a Solr query URL based on the provided parameters.

        This method constructs a Solr query URL using the specified search criteria, 
        result columns, and additional operational parameters.

        Args:
            select_dict: Optional dictionary containing search criteria and their values.
                This acts as the 'q' field in the Solr query.
            attr_list: Optional set of column names to be returned in the results.
                This acts as the 'fl' (field list) in the Solr query.
            op_params: Optional dictionary of additional parameters and their values for the Solr query,
                such as 'start' and 'rows'.

        Returns:
            A string representing the constructed Solr query URL based on the provided parameters.

        Raises:
            SDKException: If the Solr query URL could not be formed due to invalid parameters or internal errors.

        Example:
            >>> select_criteria = {'name': 'John Doe', 'age': 30}
            >>> columns = {'name', 'email', 'age'}
            >>> options = {'start': 0, 'rows': 10}
            >>> solr_url = index_server._create_solr_query(select_criteria, columns, options)
            >>> print(solr_url)
            # Output: (example) '/solr/select?q=name:John+Doe+AND+age:30&fl=name,email,age&start=0&rows=10'

        #ai-gen-doc
        """
        try:
            search_query = f'q='
            simple_search = 0
            if select_dict:
                for key, value in select_dict.items():
                    if isinstance(key, tuple):
                        if isinstance(value, list):
                            search_query += f'({key[0]}:{str(value[0])}'
                            for val in value[1:]:
                                search_query += f' OR {key[0]}:{str(val)}'
                        else:
                            search_query += f'({key[0]}:{value}'
                        for key_val in key[1:]:
                            if isinstance(value, list):
                                search_query += f' OR {key_val}:{str(value[0])}'
                                for val in value[1:]:
                                    search_query += f' OR {key_val}:{str(val)}'
                            else:
                                search_query += f' OR {key_val}:{value}'
                        search_query += ') AND '
                    elif isinstance(value, list):
                        search_query += f'({key}:{str(value[0])}'
                        for val in value[1:]:
                            search_query += f' OR {key}:{str(val)}'
                        search_query += ") AND "
                    elif key == "keyword":
                        search_query += "(" + value + ")"
                        simple_search = 1
                        break
                    else:
                        search_query = search_query + f'{key}:{str(value)} AND '
                if simple_search == 0:
                    search_query = search_query[:-5]
            else:
                search_query += "*:*"

            field_query = ""
            if attr_list:
                field_query = "&fl="
                for item in attr_list:
                    field_query += f'{str(item)},'
                field_query = field_query[:-1]
            if attr_list and 'content' in attr_list:
                field_query = f"{field_query}&exclude=false"

            ex_query = ""
            if not op_params:
                op_params = {'wt': "json"}
            else:
                op_params['wt'] = "json"
            for key, values in op_params.items():
                if isinstance(values, list):
                    for value in values:
                        ex_query += self.__form_field_query(key, value)
                else:
                    ex_query += self.__form_field_query(key, values)
            final_url = f'{search_query}{field_query}{ex_query}'
            return final_url
        except Exception as excp:
            raise SDKException('IndexServers', '104', f"Something went wrong while creating solr query - {excp}")

    def execute_solr_query(
        self,
        core_name: str,
        solr_client: Optional[str] = None,
        select_dict: Optional[dict] = None,
        attr_list: Optional[set] = None,
        op_params: Optional[dict] = None
    ) -> dict:
        """Execute a Solr query on the specified core or collection.

        This method constructs a Solr query URL based on the provided parameters and executes it
        on the given core or collection in the Index Server. It allows for flexible search criteria,
        attribute selection, and additional Solr query parameters.

        Args:
            core_name: The name of the Solr core or collection to query.
            solr_client: Optional; the Index Server client name to execute the Solr query. If not provided,
                the first available client on the index server is used.
            select_dict: Optional; a dictionary specifying search criteria and values. This acts as the 'q'
                field in the Solr query. Supports various formats:
                    - General filter: {"jid": 1024, "datatype": 2, "clid": 2}
                    - Keyword search: {'keyword': 'SearchKeyword'}
                    - Multiple values for a field: {'cvowner': ['xxx', 'yyy']}
                    - Single value for multiple fields: {('cvowner', 'cvreaddisp'): 'xxx'}
            attr_list: Optional; a set of column names to be returned in the results. Acts as the 'fl'
                (field list) in the Solr query.
                    Example: {'msgclass', 'ccsmtp', 'fmsmtp', 'folder'}
            op_params: Optional; a dictionary of additional Solr query parameters (excluding 'wt', which is always 'json').
                Example: {"rows": 0}

        Returns:
            dict: The content of the Solr response as a dictionary.

        Raises:
            SDKException: If the request cannot be sent or if the response indicates failure.

        Example:
            >>> # Execute a Solr query to fetch messages with a specific job ID
            >>> response = index_server.execute_solr_query(
            ...     core_name='mailbox_core',
            ...     select_dict={'jid': 1024},
            ...     attr_list={'msgclass', 'folder'},
            ...     op_params={'rows': 10}
            ... )
            >>> print(response)
            {'response': {'numFound': 1, 'docs': [{'msgclass': 'IPM.Note', 'folder': 'Inbox'}]}}

        #ai-gen-doc
        """
        solr_url = f"solr/{core_name}/select?{self._create_solr_query(select_dict, attr_list, op_params)}"
        if solr_client is None:
            solr_url = f"{self.server_url[0]}/{solr_url}"
        else:
            if solr_client not in self.client_name:
                raise SDKException('IndexServers', '104', 'client name not found in this index server')
            server_url = self.server_url[self.client_name.index(solr_client)]
            solr_url = f"{server_url}/{solr_url}"
        flag, response = self._cvpysdk_object.make_request("GET", solr_url)
        if flag and response.json():
            return response.json()
        elif response.status_code == httplib.FORBIDDEN:
            cmd = f"(Invoke-WebRequest -UseBasicParsing -uri \"{solr_url}\").content"
            client_obj = None
            if solr_client:
                client_obj = self._commcell_obj.clients.get(solr_client)
            else:
                # if no client is passed, then take first client in index server cloud
                client_obj = self._commcell_obj.clients.get(self.client_name[0])
            exit_code, output, error_message = client_obj.execute_script(script_type="PowerShell",
                                                                         script=cmd)
            if exit_code != 0:
                raise SDKException(
                    'IndexServers',
                    '104',
                    f"Something went wrong while querying solr - {exit_code}")
            elif error_message:
                raise SDKException(
                    'IndexServers',
                    '104',
                    f"Something went wrong while querying solr - {error_message}")
            try:
                return json.loads(output.strip())
            except Exception:
                raise SDKException('IndexServers', '104', f"Something went wrong while querying solr - {output}")
        raise SDKException('IndexServers', '104', "Something went wrong while querying solr")

    def get_index_node(self, node_name: str) -> 'IndexNode':
        """Retrieve the IndexNode object for the specified index server node name.

        Args:
            node_name: The name of the index server node to retrieve.

        Returns:
            IndexNode: An object representing the specified index server node.

        Raises:
            SDKException: If a node with the given name is not found.

        #ai-gen-doc
        """
        node_name = node_name.lower()
        if node_name in self.client_name:
            return IndexNode(self._commcell_obj, self.engine_name, node_name)
        raise SDKException("IndexServers", '104', 'Index server node not found')

    def get_plan_info(self) -> dict:
        """Retrieve the plan information associated with the index server.

        Returns:
            dict: A dictionary containing details about the plan configured for the index server.

        Example:
            >>> index_server = IndexServer()
            >>> plan_info = index_server.get_plan_info()
            >>> print(plan_info)
            >>> # Output will be a dictionary with plan details such as plan name, ID, and configuration

        #ai-gen-doc
        """
        client = self._commcell_obj.clients.get(self.engine_name)
        instance_props = client.properties.get("pseudoClientInfo", {}).get("distributedClusterInstanceProperties", {})
        plan_details = instance_props.get("clusterConfig", {}).get("cloudInfo", {}).get("planInfo", {})
        return plan_details

    def get_os_info(self) -> str:
        """Retrieve the operating system type for the Index server.

        Returns:
            The OS type of the Index server as a string (e.g., 'Windows', 'Linux').

        #ai-gen-doc
        """

        nodes_name = self.client_name
        nodes = [self._commcell_obj.clients.get(node) for node in nodes_name]
        nodes_os_info = [node.os_info for node in nodes]
        if IndexServerOSType.WINDOWS.value.lower() in nodes_os_info[0].lower():
            for node in nodes_os_info[1:]:
                if IndexServerOSType.UNIX.value.lower() in node.lower():
                    return IndexServerOSType.MIXED.value
            return IndexServerOSType.WINDOWS.value
        else:
            for node in nodes_os_info[1:]:
                if IndexServerOSType.WINDOWS.value.lower() in node.lower():
                    return IndexServerOSType.MIXED.value
            return IndexServerOSType.UNIX.value

    @staticmethod
    def __form_field_query(key: str, value: str) -> str:
        """Construct a Solr query string using the specified key and value.

        Args:
            key: The field name to use in the query.
            value: The value to match for the specified field.

        Returns:
            A string representing the Solr query to be executed.

        #ai-gen-doc
        """
        query = None
        if value is None:
            query = f'&{key}'
        else:
            query = f'&{key}={str(value)}'
        return query

    @property
    def plan_name(self) -> str:
        """Get the name of the plan associated with the index server.

        Returns:
            The name of the plan as a string.

        #ai-gen-doc
        """
        return self.plan_info.get("planName")

    @property
    def os_info(self) -> str:
        """Get the operating system type for the Index server.

        Returns:
            The OS type of the Index server as a string (e.g., 'Windows', 'Linux').

        #ai-gen-doc
        """
        return self.os_type

    @property
    def is_cloud(self) -> bool:
        """Check if the Index Server is a cloud-based server.

        Returns:
            True if the Index Server is a cloud server, False otherwise.

        #ai-gen-doc
        """
        return self.server_type == 5

    @property
    def nodes_count(self) -> int:
        """Get the number of Index Server nodes configured.

        Returns:
            The count of Index Server nodes as an integer.

        #ai-gen-doc
        """
        return len(self.client_id)

    @property
    def roles_data(self) -> dict:
        """Get the cloud roles data associated with the IndexServer.

        Returns:
            dict: A dictionary containing information about the cloud roles configured for the IndexServer.

        #ai-gen-doc
        """
        return self._roles_obj.roles_data

    @property
    def properties(self) -> dict:
        """Get the properties of the index server.

        Returns:
            dict: A dictionary containing the properties and configuration details of the index server.

        #ai-gen-doc
        """
        return self._properties

    @property
    def host_name(self) -> List[str]:
        """Get the list of host names for all index server nodes.

        Returns:
            List of strings representing the host names of all nodes in the index server.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.HOST_NAME]

    @property
    def cloud_name(self) -> str:
        """Get the internal cloud name of the index server.

        Returns:
            The internal cloud name as a string.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.CLOUD_NAME]

    @property
    def client_name(self) -> List[str]:
        """Get the list of client names for all index server nodes.

        Returns:
            List of strings representing the client names of all index server nodes.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.CLIENT_NAME]

    @property
    def server_url(self) -> list:
        """Get the list of Solr URLs for all index server nodes.

        Returns:
            list: A list containing the Solr URLs (as strings) for each index server node.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.CI_SERVER_URL]

    @property
    def type(self) -> str:
        """Get the type of the index server.

        Returns:
            The type of the index server as a string.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.TYPE]

    @property
    def base_port(self) -> list:
        """Get the list of base ports for all index server nodes.

        Returns:
            list: A list containing the base port numbers (as integers) for each index server node.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.BASE_PORT]

    @property
    def client_id(self) -> List[int]:
        """Get the list of client IDs for all index server nodes.

        Returns:
            List of integers representing the client IDs of all index server nodes.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.CLIENT_ID]

    @property
    def roles(self) -> List[str]:
        """Get the list of roles assigned to the index server.

        Returns:
            List of strings representing the roles associated with the index server.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.ROLES]

    @property
    def role_display_name(self) -> list:
        """Get the display name of the roles assigned to the index server.

        Returns:
            The display name of the roles configured for this index server as a string.

        #ai-gen-doc
        """
        role_disp_name = []
        for role_version in self.roles:
            for role in self.roles_data:
                if role_version == role['roleVersion']:
                    role_disp_name.append(role['roleName'])
                    break
        return role_disp_name

    @property
    def cloud_id(self) -> int:
        """Get the cloud ID associated with the index server.

        Returns:
            int: The unique cloud ID of the index server.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.CLOUD_ID]

    @property
    def server_type(self) -> str:
        """Get the server type of the index server.

        Returns:
            The server type as a string.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.SERVER_TYPE]

    @property
    def engine_name(self) -> str:
        """Get the engine name of the index server.

        Returns:
            The engine name as a string.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.ENGINE_NAME]

    @property
    def index_server_client_id(self) -> int:
        """Get the client ID of the index server.

        Returns:
            int: The unique client ID associated with this index server.

        #ai-gen-doc
        """
        return self._properties[IndexServerConstants.INDEX_SERVER_CLIENT_ID]

    @property
    def fs_collection(self) -> str:
        """Get the multinode collection name for the File System Index.

        Returns:
            The multinode collection name as a string, representing the File System index.

        #ai-gen-doc
        """
        return f'fsindex_{"".join(letter for letter in self.cloud_name if letter.isalnum())}_multinode'


class IndexNode(object):
    """
    Represents an Index server node within a CommCell environment.

    This class encapsulates the properties and operations associated with an Index server node,
    providing access to node-specific information and configuration management. It allows users
    to retrieve and update node attributes such as node name, node ID, Solr port, Solr URL, roles,
    index location, and JVM memory allocation. The class also supports refreshing the node's state
    to ensure up-to-date information.

    Key Features:
        - Initialize an IndexNode with CommCell object, index server name, and node name
        - Refresh node information to reflect current state
        - Access node properties: name, ID, Solr port, Solr URL, roles, index location, JVM memory
        - Update Solr port and JVM memory settings

    #ai-gen-doc
    """

    def __init__(self, commcell_obj: 'Commcell', index_server_name: str, node_name: str) -> None:
        """Initialize an IndexNode instance representing a node in an index server.

        Args:
            commcell_obj: The Commcell object representing the connection to the Commcell environment.
            index_server_name: The name of the index server as a string.
            node_name: The client name of the index server node.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> index_node = IndexNode(commcell, 'IndexServer01', 'NodeClient01')
            >>> print(f"IndexNode created for server: {index_node}")

        #ai-gen-doc
        """
        self.commcell = commcell_obj
        self.index_server_name = index_server_name
        self.data_index = 0
        self.index_server = None
        self.index_node_name = node_name.lower()
        self.index_node_client = None
        self.index_client_properties = None
        self.refresh()

    def refresh(self) -> None:
        """Reload the properties of the index node to ensure the latest information is available.

        This method refreshes the internal state of the IndexNode object, updating its properties
        from the underlying data source. Use this method if you suspect the index node's properties
        have changed and want to ensure you are working with the most current data.

        #ai-gen-doc
        """
        self.commcell.index_servers.refresh()
        self.index_server = self.commcell.index_servers.get(self.index_server_name)
        self.data_index = self.index_server.client_name.index(self.index_node_name)
        self.commcell.clients.refresh()
        self.index_node_client = self.commcell.clients.get(self.index_node_name)
        # TODO: Rewrite Index server API logic to access client properties
        self.index_client_properties = (self.index_node_client.properties.get('pseudoClientInfo', {}).
                                        get('indexServerProperties', {}))

    @property
    def node_name(self) -> str:
        """Get the client name of the Index Server node.

        Returns:
            The client name of the Index Server node as a string.

        #ai-gen-doc
        """
        return self.index_server.client_name[self.data_index]

    @property
    def node_id(self) -> int:
        """Get the client ID of the Index Server node.

        Returns:
            The client ID of the Index Server node as an integer.

        #ai-gen-doc
        """
        return self.index_server.client_id[self.data_index]

    @property
    def solr_port(self) -> int:
        """Get the port number on which Solr is running on the Index server node.

        Returns:
            The port number as an integer.

        #ai-gen-doc
        """
        return self.index_server.base_port[self.data_index]

    @property
    def solr_url(self) -> str:
        """Get the Solr URL for the Index server node.

        Returns:
            The Solr URL as a string associated with this IndexNode instance.

        #ai-gen-doc
        """
        return self.index_server.server_url[self.data_index]

    @property
    def roles(self) -> list:
        """Get the list of roles installed with the index server in the Commcell.

        Returns:
            list: An array containing the roles installed on the index server.

        #ai-gen-doc
        """
        return self.index_server.role_display_name

    @property
    def index_location(self) -> Union[str, None]:
        """Get the index directory path for the Index server node.

        Returns:
            The file system path to the index directory used by this Index server node.

        #ai-gen-doc
        """
        node_meta_infos = self.index_client_properties['nodeMetaInfos']
        for info in node_meta_infos:
            if info['name'] == 'INDEXLOCATION':
                return info['value']

    @property
    def jvm_memory(self) -> Union[str, None]:
        """Get the Solr JVM memory allocated for the Index server node.

        Returns:
            The amount of JVM memory (in megabytes) configured for the Index server node.

        #ai-gen-doc
        """
        node_meta_infos = self.index_client_properties['nodeMetaInfos']
        for info in node_meta_infos:
            if info['name'] == 'JVMMAXMEMORY':
                return info['value']

    @solr_port.setter
    def solr_port(self, port_no: str) -> None:
        """Set the Solr port number for this index node.

        Args:
            port_no: The Solr port number to assign to the node, as a string.

        #ai-gen-doc
        """
        solr_port_param = deepcopy(IndexServerConstants.SOLR_PORT_META_INFO)
        solr_port_param['value'] = str(port_no)
        cloud_param = [solr_port_param]
        self.index_server.modify(self.index_location, self.index_node_name, cloud_param)
        self.refresh()

    @jvm_memory.setter
    def jvm_memory(self, memory: str) -> None:
        """Set the Solr JVM memory allocation for this index node.

        Args:
            memory: The amount of JVM memory to allocate, specified as a string (e.g., '4g', '1024m').

        #ai-gen-doc
        """
        solr_jvm_param = deepcopy(IndexServerConstants.SOLR_JVM_META_INFO)
        solr_jvm_param['value'] = str(memory)
        solr_port_param = deepcopy(IndexServerConstants.SOLR_PORT_META_INFO)
        solr_port_param['value'] = str(self.solr_port)
        cloud_param = [solr_jvm_param, solr_port_param]
        self.index_server.modify(self.index_location, self.index_node_name, cloud_param)
        self.refresh()


class _Roles(object):
    """
    Class for managing and operating on cloud roles data.

    This class provides a set of methods and properties to interact with, retrieve,
    and update cloud roles information within a CommCell environment. It allows for
    refreshing the roles data, retrieving all available roles, obtaining role IDs by
    name, and updating the internal roles data cache. The `roles_data` property
    provides access to the current roles' data.

    Key Features:
        - Initialization with a CommCell object for context
        - Refreshing roles data to ensure up-to-date information
        - Retrieving all available roles
        - Fetching role IDs by role name
        - Updating roles data from the source
        - Accessing roles data via a property

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize the _Roles class with a Commcell connection object.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> roles = _Roles(commcell)
            >>> print("Roles object initialized successfully")
        #ai-gen-doc
        """
        self.commcell_object = commcell_object
        self._roles_data = None
        self.refresh()

    def refresh(self) -> None:
        """Reload the role data associated with this _Roles instance.

        This method refreshes the internal data, ensuring that any changes to roles
        are reflected in the current object. Use this method to update the role information
        after making changes externally.

        #ai-gen-doc
        """
        self._get_all_roles()

    def _get_all_roles(self) -> List[Dict[str, Any]]:
        """Retrieve all cloud role details available on the Commcell.

        Returns:
            A list of dictionaries, each containing details of a cloud role.

        Raises:
            SDKException: If the response from the Commcell is empty or not successful.

        #ai-gen-doc
        """
        flag, response = self.commcell_object._cvpysdk_object.make_request(
            "GET", self.commcell_object._services['GET_ALL_ROLES']
        )
        if flag:
            if response.json():
                if 'rolesInfo' in response.json():
                    self._roles_data = response.json()['rolesInfo']
                    return self._roles_data
            raise SDKException('Response', '102')
        raise SDKException('Response', '101')

    def get_role_id(self, role_name: str) -> Optional[int]:
        """Retrieve the ID of a cloud role by its name.

        Args:
            role_name: The name of the cloud role for which the ID is required.

        Returns:
            The integer ID of the role if the role name exists in the roles data; otherwise, None.

        #ai-gen-doc
        """
        for role_data in self._roles_data:
            if role_data['roleName'] == role_name:
                return role_data['roleId']
        return None

    def update_roles_data(self) -> None:
        """Update and synchronize the cloud role data with the Commcell database.

        This method refreshes the internal role data to ensure it matches the current state 
        of the Commcell database. Use this method to reload role information after changes 
        have been made in the Commcell environment.

        #ai-gen-doc
        """
        self._get_all_roles()

    @property
    def roles_data(self) -> List[Dict[str, Any]]:
        """Get the details of each cloud role as a list of dictionaries.

        Returns:
            List[Dict[str, Any]]: A list where each dictionary contains details about a cloud role.

        #ai-gen-doc
        """
        return self._roles_data
