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

"""File for performing hac cluster related operations on the commcell

HACClusters and HACCluster are 2 classes defined in this file

HACClusters:   Class for representing all the hac clusters associated with the commcell

HACCluster:    Class for a instance of a single hac cluster of the commcell


HACClusters
============

    __init__()                          --  initialize object of HAC clusters class associated with
    the commcell

    __str()                             --  returns all the HAC clusters of the commcell

    __repr__()                          --  returns the string to represent the instance

    __get_item()                        --  returns the details of HAC cluster for given cloud name

    _get_all_clusters()                 --  gets detail of all hac cluster associated to commcell

    _response_not_success()             --  raise exception when response is not 200

    get()                               --  return an HACCluster object for given cluster name

    has_cluster()                       --  returns whether the hac cluster is present or not in
    the commcell

    add()                            --  creates a new hac cluster to the commcell

    delete()                            --  deletes the hac cluster associated to commcell

    refresh()                           --  refresh the hac clusters details associated with commcell

HACClusters Attributes
-----------------------

    **all_hac_clusters**                 --  returns the dictionary consisting of all the hac clusters
    associated with the commcell and there details

HACCluster
============

    __init__()                          --  initialize object of IndexPool class

    __repr__()                          --  returns the string to represent the instance

    _response_not_success()             --  raise exception when response is not 200

    modify_node()                       --  methods to modify the HAC cluster node properties

    node_info()                         --  returns a dict consisting details of node present in the cluster

    refresh()                           --  refresh the index pool details associated with commcell

HACCluster Attributes
-----------------------

    **cluster_id**                      --  returns the cluster id for HAC cluster

    **cluster_name**                    --  returns the HAC cluster name

    **cloud_id**                        --  returns HAC cluster cloud id

    **node_names**                      --  returns a list of names of all HAC cluster nodes

"""

from copy import deepcopy

from .exception import SDKException
from .datacube.constants import IndexServerConstants

from typing import List, Optional, Union, TYPE_CHECKING
if TYPE_CHECKING:
    import requests
    from cvpysdk.commcell import Commcell


class HACClusters(object):
    """
    Represents and manages all High Availability Cluster (HAC) entities associated with a CommCell.

    This class provides an interface to interact with HAC clusters, allowing users to retrieve,
    add, delete, and refresh cluster information. It supports dictionary-like access to clusters,
    and offers utility methods for checking cluster existence and obtaining detailed cluster data.

    Key Features:
        - Retrieve all HAC clusters associated with the CommCell
        - Access clusters using dictionary-style indexing
        - Check for the existence of a specific cluster by name
        - Get detailed information about a specific cluster
        - Add new HAC clusters with specified cloud and node names
        - Delete existing HAC clusters by cloud name
        - Refresh the internal list of clusters to reflect current state
        - Access all HAC clusters via a property
        - String and representation methods for easy inspection

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize an instance of the HACClusters class.

        Args:
            commcell_object: An instance of the Commcell class representing the Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> hac_clusters = HACClusters(commcell)
            >>> print("HACClusters object created:", hac_clusters)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._hac_group = None
        self._all_hac_clusters = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all HAC Clusters associated with the Commcell.

        This method provides a human-readable summary of all HAC Clusters managed by the Commcell,
        typically listing their names or key details in a single string.

        Returns:
            A string containing information about all HAC Clusters associated with the Commcell.

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'HAC Name')
        index = 1
        for hac_name in self.all_hac_clusters:
            representation_string += '{:^5}\t{:^20}\n'.format(
                index, hac_name)
            index += 1
        return representation_string

    def __repr__(self) -> str:
        """Return a string representation of the HACClusters instance.

        This method provides a developer-friendly string that identifies the HACClusters object,
        which is useful for debugging and logging purposes.

        Returns:
            A string representing the HACClusters instance.

        #ai-gen-doc
        """
        return "HACClusters class instance for Commcell"

    def __getitem__(self, value: str) -> dict:
        """Retrieve the details of a HAC cluster by its name.

        Args:
            value: The name of the HAC cluster to look up.

        Returns:
            A dictionary containing the details of the specified HAC cluster.

        Raises:
            KeyError: If the HAC cluster with the given name is not found.

        #ai-gen-doc
        """
        value = value.lower()
        if value.lower() in self.all_hac_clusters:
            return {"name": value.lower, "id": self.all_hac_clusters[value]}
        raise SDKException('HACClusters', '102')

    def _response_not_success(self, response: 'requests.Response') -> None:
        """Raise an exception if the response status is not successful (HTTP 200).

        Args:
            response: The response object to check for a successful status.

        Raises:
            SDKException: If the response does not indicate a successful (200 OK) status.

        #ai-gen-doc
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(response.text))

    def _get_all_clusters(self) -> None:
        """Retrieve details of all HAC clusters associated with the Commcell.

        Returns:
            None

        #ai-gen-doc
        """
        if self._commcell_object.client_groups.has_clientgroup("HAC Cluster"):
            if self._hac_group is None:
                self._hac_group = self._commcell_object.client_groups.get("HAC Cluster")
            self._hac_group.refresh()
            for client_name in self._hac_group.associated_clients:
                client_obj = HACCluster(
                    self._commcell_object, client_name
                )
                self._all_hac_clusters[client_name.lower()] = int(client_obj.cloud_id)

    def has_cluster(self, hac_name: str) -> bool:
        """Check if a HAC cluster with the specified name exists.

        Args:
            hac_name: The name of the HAC cluster to check.

        Returns:
            True if the HAC cluster with the given name is associated with the Commcell, otherwise False.

        Raises:
            SDKException: If the data type of the input is not valid.

        #ai-gen-doc
        """
        if not isinstance(hac_name, str):
            raise SDKException('HACClusters', '101')
        return hac_name.lower() in self._all_hac_clusters

    def get(self, hac_name: Union[str, int]) -> 'HACCluster':
        """Retrieve an instance of the HACCluster class for the specified cluster name or ID.

        Args:
            hac_name: The name (str) or ID (int) of the HAC cluster to retrieve.

        Returns:
            HACCluster: An instance representing the specified HAC cluster.

        Raises:
            SDKException: If the input data type is invalid or the HAC cluster is not found.

        Example:
            >>> clusters = HACClusters()
            >>> hac_cluster = clusters.get('ClusterA')
            >>> print(f"Retrieved HAC cluster: {hac_cluster}")
            >>> # You can also use the cluster ID
            >>> hac_cluster_by_id = clusters.get(101)
            >>> print(f"Retrieved HAC cluster by ID: {hac_cluster_by_id}")

        #ai-gen-doc
        """
        if isinstance(hac_name, str):
            if hac_name.lower() in self.all_hac_clusters:
                return HACCluster(self._commcell_object, hac_name.lower())
        elif isinstance(hac_name, int):
            for cluster_name in self.all_hac_clusters:
                if int(self._all_hac_clusters[cluster_name]) == int(hac_name):
                    return HACCluster(self._commcell_object, cluster_name)
        else:
            raise SDKException('HACClusters', '101')
        raise SDKException("HACClusters", "102")

    def refresh(self) -> None:
        """Reload the properties and state information for the HACClusters class.

        This method refreshes the internal data of the HACClusters instance, ensuring that 
        any changes in the underlying cluster configuration or status are reflected in the object.

        #ai-gen-doc
        """
        self._commcell_object.clients.refresh()
        self._commcell_object.client_groups.refresh()
        self._all_hac_clusters = {}
        self._hac_group = None
        self._get_all_clusters()

    def add(self, cloud_name: str, cloud_node_names: List[str]) -> 'HACCluster':
        """Create a new HAC cluster with the specified cloud name and node names.

        Args:
            cloud_name: The name to assign to the HAC cluster cloud.
            cloud_node_names: List of node names (strings) to be added to the cluster.

        Returns:
            HACCluster: An instance representing the newly created HAC cluster.

        Raises:
            SDKException: If the input data types are invalid, the response is unsuccessful, or the response is empty.

        Example:
            >>> hac_clusters = HACClusters()
            >>> cluster = hac_clusters.add("MyCloudCluster", ["node1", "node2", "node3"])
            >>> print(f"Created HAC cluster: {cluster}")
            >>> # The returned HACCluster object can be used for further cluster management

        #ai-gen-doc
        """
        if not (isinstance(cloud_name, str) and isinstance(cloud_node_names, list)):
            raise SDKException('HACClusters', '101')
        cloud_node_names = sorted(cloud_node_names)
        node_meta_infos = {
            'zkDataPort': '8091',
            'zkElectionPort': '8097',
            'zkListenerPort': '8090',
            'zkServerId': None,
            'zkDataDir': None
        }
        req_json = deepcopy(IndexServerConstants.REQUEST_JSON)
        del req_json['solrCloudInfo']
        del req_json['cloudMetaInfos']
        req_json['type'] = 6
        req_json['cloudInfoEntity'] = {
            "_type_": 169,
            "cloudName": cloud_name,
            "cloudDisplayName": cloud_name
        }
        server_id = 1
        for node_name in cloud_node_names:
            node_obj = self._commcell_object.clients.get(node_name)
            node_data = {
                "opType": IndexServerConstants.OPERATION_ADD,
                "status": 0,
                "nodeClientEntity": {
                    "_type_": 3,
                    "hostName": node_obj.client_hostname,
                    "clientName": node_name,
                    "clientId": int(node_obj.client_id)
                },
                "nodeMetaInfos": []
            }
            node_meta_infos['zkServerId'] = str(server_id)
            node_meta_infos['zkDataDir'] = node_obj.install_directory + "\\iDataAgent\\JobResults\\ZKData"
            for node_info in node_meta_infos:
                node_data['nodeMetaInfos'].append({
                    'name': node_info,
                    'value': node_meta_infos[node_info]
                })
            req_json['cloudNodes'].append(node_data)
            server_id += 1
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CLOUD_CREATE'], req_json
        )
        if flag:
            if response.json() and 'genericResp' in response.json():
                if response.json()['genericResp'] == {} and \
                        'cloudId' in response.json():
                    self.refresh()
                    return HACCluster(self._commcell_object, cloud_name)
                else:
                    o_str = 'Failed to create HAC Cluster. Error: "{0}"'.format(
                        response.json()['genericResp'])
                    raise SDKException('Response', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            self._response_not_success(response)

    def delete(self, cloud_name: str) -> None:
        """Delete an existing HAC cluster by its cloud name.

        Args:
            cloud_name: The name of the HAC cluster cloud to be deleted.

        Raises:
            SDKException: If the input data type is invalid, the response is not successful, or the response is empty.

        Example:
            >>> hac_clusters = HACClusters()
            >>> hac_clusters.delete("MyHACCluster")
            >>> print("HAC cluster deleted successfully.")

        #ai-gen-doc
        """
        if not isinstance(cloud_name, str):
            raise SDKException('HACCluster', '101')
        cloud_id = self.all_hac_clusters[cloud_name.lower()]
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

    @property
    def all_hac_clusters(self) -> dict:
        """Get the details of all HAC clusters associated with the Commcell.

        Returns:
            dict: A dict containing details of each HAC cluster associated with the Commcell.

        #ai-gen-doc
        """
        return self._all_hac_clusters


class HACCluster(object):
    """
    Class for managing and performing operations on a specific HAC (High Availability Cluster).

    This class provides an interface to interact with a HAC cluster, allowing users to retrieve
    cluster and node information, modify node configurations, and refresh cluster state. It exposes
    properties for accessing cluster identifiers and node names, and includes internal mechanisms
    for handling response validation.

    Key Features:
        - Initialization with commcell object, cluster name, and cluster ID
        - Retrieve and modify node information and configuration
        - Refresh cluster state to reflect latest changes
        - Access cluster and node properties (cloud_id, node_names, cluster_id, cluster_name)
        - Internal response validation for cluster operations

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', cluster_name: str, cluster_id: int = None) -> None:
        """Initialize a HACCluster object representing a specific HAC cluster.

        Args:
            commcell_object: An instance of the Commcell class used to interact with the Commcell environment.
            cluster_name: The name of the HAC cluster cloud.
            cluster_id: The unique identifier for the HAC cluster cloud. If not provided, it defaults to None.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> hac_cluster = HACCluster(commcell, 'MyHACCluster', cluster_id=123)
            >>> # The hac_cluster object can now be used to manage the specified HAC cluster

        #ai-gen-doc
        """
        self.commcell = commcell_object
        self._cluster_name = cluster_name
        self._cluster_id = cluster_id
        self._cluster_properties = None
        self.cluster_client_obj = None
        self.cluster_nodes = None
        self.refresh()

    def __repr__(self) -> str:
        """Return a string representation of the HACCluster instance.

        This method provides a developer-friendly string that identifies the HACCluster object,
        typically including its class name and key attributes for debugging purposes.

        Returns:
            A string representing the HACCluster instance.

        #ai-gen-doc
        """
        return "HACCluster class instance for Commcell"

    def _response_not_success(self, response: 'requests.Response') -> None:
        """Raise an exception if the HTTP response status is not 200 (OK).

        This helper method checks the provided response object and raises an SDKException
        if the response indicates a failure (i.e., status code is not 200).

        Args:
            response: The HTTP response object to validate.

        Raises:
            SDKException: If the response status code is not 200 (OK).

        #ai-gen-doc
        """
        raise SDKException(
            'Response',
            '101',
            self.commcell._update_response_(response.text)
        )

    def refresh(self) -> None:
        """Reload the properties of the HAC cluster to ensure the latest information is available.

        This method updates the internal state of the HACCluster object by fetching the most recent
        properties from the underlying data source or system.

        #ai-gen-doc
        """
        self.commcell.clients.refresh()
        if not self.commcell.clients.has_client(self._cluster_name):
            raise SDKException('HACClusters', '102')
        self.cluster_client_obj = self.commcell.clients.get(self._cluster_name)
        self._cluster_id = self.cluster_client_obj.client_id
        self._cluster_properties = self.cluster_client_obj.\
            properties['pseudoClientInfo']['distributedClusterInstanceProperties']['clusterConfig']['cloudInfo']
        self.cluster_nodes = self._cluster_properties['cloudNodes']

    def modify_node(
        self,
        node_name: str,
        listener_port: Optional[Union[int, str]] = None,
        data_port: Optional[Union[int, str]] = None,
        election_port: Optional[Union[int, str]] = None,
        data_dir: Optional[str] = None
    ) -> None:
        """Modify the properties of a node in the HAC cluster.

        This method updates the specified properties for a given node in the HAC cluster,
        such as listener port, data port, election port, and the ZooKeeper data directory.

        Args:
            node_name: The client name of the node to modify.
            listener_port: The new zkListenerPort address for the node (e.g., 8090 or '8090'). Optional.
            data_port: The new zkDataPort address for the node (e.g., 8091 or '8091'). Optional.
            election_port: The new zkElectionPort address for the node (e.g., 8097 or '8097'). Optional.
            data_dir: The new ZooKeeper data directory for the node. Optional.

        Raises:
            SDKException: If the HAC zKeeper node is not found or the response is not successful.

        Example:
            >>> hac_cluster = HACCluster()
            >>> hac_cluster.modify_node(
            ...     node_name='NodeA',
            ...     listener_port=8090,
            ...     data_port='8091',
            ...     election_port=8097,
            ...     data_dir='/var/lib/zookeeper'
            ... )
            >>> print("Node properties updated successfully.")

        #ai-gen-doc
        """
        node_info = self.node_info(node_name)
        port_infos = {}
        node_meta_info = node_info['nodeMetaInfos']
        for meta_info in node_meta_info:
            port_infos[meta_info['name']] = meta_info['value']
        if listener_port:
            port_infos['ZKLISTENERPORT'] = str(listener_port)
        if election_port:
            port_infos['ZKELECTIONPORT'] = str(election_port)
        if data_port:
            port_infos['ZKDATAPORT'] = str(data_port)
        if data_dir:
            port_infos['ZKDATADIR'] = str(data_dir)
        req_json = {
            'cloudId': self.cloud_id,
            'nodes': [{
                'status': 1,
                'opType': IndexServerConstants.OPERATION_EDIT,
                'nodeClientEntity': {
                    'clientId': int(self.commcell.clients[node_name]['id']),
                    'hostName': self.commcell.clients[node_name]['hostname'],
                    'clientName': node_name
                },
                'nodeMetaInfos': [
                    {
                        "name": "zkListenerPort",
                        "value": port_infos['ZKLISTENERPORT']
                    },
                    {
                        "name": "zkDataPort",
                        "value": port_infos['ZKDATAPORT']
                    },
                    {
                        "name": "zkElectionPort",
                        "value": port_infos['ZKELECTIONPORT']
                    },
                    {
                        "name": "zkDataDir",
                        "value": port_infos['ZKDATADIR']
                    }]
            }]
        }
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

    def node_info(self, node_name: str) -> dict:
        """Retrieve information for a specific HAC cluster node.

        Args:
            node_name: The name of the HAC cluster node to query.

        Returns:
            A dictionary containing details about the specified HAC cluster node.

        Raises:
            SDKException: If the specified HAC zKeeper node is not found.

        #ai-gen-doc
        """
        for node_info in self.cluster_nodes:
            if node_info['nodeClientEntity']['clientName'].lower() == node_name.lower():
                return node_info
        raise SDKException('HACCluster', '103')

    @property
    def cloud_id(self) -> str:
        """Get the cloud ID associated with the HAC cluster.

        Returns:
            int: The unique cloud ID for this HAC cluster.

        #ai-gen-doc
        """
        return self._cluster_properties['cloudInfoEntity']['cloudId']

    @property
    def node_names(self) -> list:
        """Get the list of node names in the HAC cluster.

        Returns:
            list: A list containing the names of all nodes in the HAC cluster.

        #ai-gen-doc
        """
        result = []
        for node_info in self.cluster_nodes:
            result.append(node_info['nodeClientEntity']['clientName'])
        return result

    @property
    def cluster_id(self) -> int:
        """Get the HAC cluster pseudo client ID.

        Returns:
            The unique integer ID representing the HAC cluster pseudo client.

        #ai-gen-doc
        """
        return self._cluster_id

    @property
    def cluster_name(self) -> str:
        """Get the name of the HAC cluster cloud.

        Returns:
            The name of the HAC cluster as a string.

        #ai-gen-doc
        """
        return self._cluster_name
