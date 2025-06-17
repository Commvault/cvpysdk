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


class HACClusters(object):
    """Class for representing all the HAC clusters associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the HACClusters class

            Args:
                commcell_object (object)    --  instance of class Commcell

            Returns:
                object  -   instance of class HACClusters
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._hac_group = None
        self._all_hac_clusters = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all HAC Clusters of the commcell.

                Returns:
                    str - string of all the HAC clusters associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'HAC Name')
        index = 1
        for hac_name in self.all_hac_clusters:
            representation_string += '{:^5}\t{:^20}\n'.format(
                index, hac_name)
            index += 1
        return representation_string

    def __repr__(self):
        """Representation string for the instance of the HACClusters class."""
        return "HACClusters class instance for Commcell"

    def __getitem__(self, value):
        """Returns the details of HAC cluster for given HAC name

            Args:
                value   (str)       --  name of HAC cluster

            Returns:
                dict    -   details of the HAC cluster

            Raises:
                HAC cluster not found
        """
        value = value.lower()
        if value.lower() in self.all_hac_clusters:
            return {"name": value.lower, "id": self.all_hac_clusters[value]}
        raise SDKException('HACClusters', '102')

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

            Args:
                response    (object)    -   response object

            Raises:
                SDKException:
                    Response was not success
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def _get_all_clusters(self):
        """Gets details of all HAC clusters associated to the commcell"""
        if self._commcell_object.client_groups.has_clientgroup("HAC Cluster"):
            if self._hac_group is None:
                self._hac_group = self._commcell_object.client_groups.get("HAC Cluster")
            self._hac_group.refresh()
            for client_name in self._hac_group.associated_clients:
                client_obj = HACCluster(
                    self._commcell_object, client_name
                )
                self._all_hac_clusters[client_name.lower()] = int(client_obj.cloud_id)

    def has_cluster(self, hac_name):
        """Returns whether the HAC cluster with given name is present or not

            Args:
                hac_name    (str)       --  hac cluster name

            Returns:
                boolean     -   True if hac cluster is associated with the commcell
                else returns False

            Raises:
                SDKException:
                    Data type of the input(s) is not valid
        """
        if not isinstance(hac_name, str):
            raise SDKException('HACClusters', '101')
        return hac_name.lower() in self._all_hac_clusters

    def get(self, hac_name):
        """Returns instance of HACCluster class is cluster is found

            Args:
                hac_name        (str/int)   --      hac cluster name or id

            Returns:
                object          (HACCluster)   --  Instance of a single hac cluster

            Raises:
                SDKException:
                    Data type of the input(s) is not valid

                    HAC Cluster not found
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

    def refresh(self):
        """Refreshes properties for HACClusters class"""
        self._commcell_object.clients.refresh()
        self._commcell_object.client_groups.refresh()
        self._all_hac_clusters = {}
        self._hac_group = None
        self._get_all_clusters()

    def add(self, cloud_name, cloud_node_names):
        """Creates a new HAC cluster

            Args:
                cloud_name      (str)       --  hac cluster cloud name
                cloud_node_names    (list)  --  string array of node names to be added to cluster

            Raises:
                SDKException:
                    Data type of the input(s) is not valid.

                    Response was not success.

                    Response was empty.

            Returns:
                Object  -   Instance of class HACCluster
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

    def delete(self, cloud_name):
        """Deletes an existing HAC cluster

        Args:
            cloud_name  (str)   --  HAC cluster cloud name to be deleted

        Raises:
            SDKException:
                Data type of the input(s) is not valid.

                Response was not success.

                Response was empty.
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
    def all_hac_clusters(self):
        """Returns the details of all HAC clusters associated with commcell"""
        return self._all_hac_clusters


class HACCluster(object):
    """Class to perform HAC cluster operations on a specific HAC cluster"""

    def __init__(self, commcell_object, cluster_name, cluster_id=None):
        """Initializes the HACCluster class object

            Args:
                commcell_object     (object)        --  Instance of commcell class
                cluster_name        (str)           --  HAC cluster cloud name
                cluster_id          (int)           --  HAC cluster cloud id
                    default: None

            Returns:
                object  -   instance of the HACCluster class
        """
        self.commcell = commcell_object
        self._cluster_name = cluster_name
        self._cluster_id = cluster_id
        self._cluster_properties = None
        self.cluster_client_obj = None
        self.cluster_nodes = None
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of the HACCluster class."""
        return "HACCluster class instance for Commcell"

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

                Raises:
                    SDKException:
                        Response was not success
        """
        raise SDKException(
            'Response',
            '101',
            self.commcell._update_response_(
                response.text))

    def refresh(self):
        """Refreshes properties of the HAC cluster"""
        self.commcell.clients.refresh()
        if not self.commcell.clients.has_client(self._cluster_name):
            raise SDKException('HACClusters', '102')
        self.cluster_client_obj = self.commcell.clients.get(self._cluster_name)
        self._cluster_id = self.cluster_client_obj.client_id
        self._cluster_properties = self.cluster_client_obj.\
            properties['pseudoClientInfo']['distributedClusterInstanceProperties']['clusterConfig']['cloudInfo']
        self.cluster_nodes = self._cluster_properties['cloudNodes']

    def modify_node(self, node_name, listener_port=None, data_port=None,
                    election_port=None, data_dir=None):
        """Methods to modify the hac cluster node properties

        Args:
            node_name       (str)       -   Client name for the node
            listener_port   (int/str)   -   zkListenerPort address to be updated
                default - None              Sample: '8090' or 8090
            data_port       (int/str)   -   zkDataPort address to be updated
                default - None              Sample: '8091' or 8091
            election_port   (int/str)   -   zkElectionPort address to be updated
                default - None              Sample: '8097' or 8097
            data_dir        (str)       -   zoo keeper data directory
                default - None

        Raises:
            SDKException:
                HAC zKeeper node not found

                Response was not success

        Returns:
            None

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

    def node_info(self, node_name):
        """Returns the hac cluster node information

        Args:
            node_name       (str)   -   HAC cluster node name

        Returns:
            dict        -   dictionary containing details of the hac node

        Raises:
            SDKException:
                HAC zKeeper node not found

        """
        for node_info in self.cluster_nodes:
            if node_info['nodeClientEntity']['clientName'].lower() == node_name.lower():
                return node_info
        raise SDKException('HACCluster', '103')

    @property
    def cloud_id(self):
        """Returns HAC cluster cloud id"""
        return self._cluster_properties['cloudInfoEntity']['cloudId']

    @property
    def node_names(self):
        """Returns a list of HAC cluster node names"""
        result = []
        for node_info in self.cluster_nodes:
            result.append(node_info['nodeClientEntity']['clientName'])
        return result

    @property
    def cluster_id(self):
        """Returns the HAC cluster pseudo client id"""
        return self._cluster_id

    @property
    def cluster_name(self):
        """Returns the HAC cluster cloud name"""
        return self._cluster_name
