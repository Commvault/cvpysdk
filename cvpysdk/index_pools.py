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
from .exception import SDKException
from .datacube.constants import IndexServerConstants


class IndexPools(object):
    """Class for representing all the Index pools associated with the commcell"""

    def __init__(self, commcell_object):
        """Initialize object of the IndexPools class

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of IndexPools class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._all_index_pools = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all Index pools of the commcell.

                Returns:
                    str - string of all the index pools associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Index pool Name')
        index = 1
        for pool_name in self.all_index_pools:
            representation_string += '{:^5}\t{:^20}\n'.format(
                index, pool_name)
            index += 1
        return representation_string

    def __repr__(self):
        """Representation string for the instance of the IndexPools class."""
        return "IndexPools class instance for Commcell"

    def __getitem__(self, value):
        """Returns the details of index pool for given index pool name

            Args:
                value   (str)       --  name of index pool

            Returns:
                dict    -   details of the index pool

            Raises:
                Index pool not found
        """
        value = value.lower()
        if value in self.all_index_pools:
            return {"pool_name": value, "pool_id": self.all_index_pools[value]}
        raise SDKException('IndexPools', '102')

    def _get_all_index_pools(self):
        """Method to get details of all the index pools present in commcell

            Raises:
                SDKException:
                    Response was not success

                    Response was empty
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

    def refresh(self):
        """Refreshes the properties of IndexPools class"""
        self._commcell_object.clients.refresh()
        self._all_index_pools = {}
        self._get_all_index_pools()

    @property
    def all_index_pools(self):
        """Returns a dict consisting details of all index pools

            Returns:
                dict    -   dictionary consisting details for all index pools
                Sample:
                    {
                        <pool_name_1> : <pool_id_1>,
                        <pool_name_2> : <pool_id_2>
                    }
        """
        return self._all_index_pools

    def get(self, pool_name):
        """Returns the IndexPool class object with given pool_name

        Args:
            pool_name       (int/str)       --  Index pool name present in commcell

        Returns:
            object  -   instance of IndexPool class

        Raises:
            SDKExecption:
                Data type of the input(s) is not valid

                Index pool not found
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

    def has_pool(self, pool_name):
        """Returns whether a index pool is present in the commcell or not

        Args:
            pool_name       (str)       --  Index pool name

        Returns:
            bool    -   True if index pool with given pool_name is present else False
        """
        return pool_name.lower() in self.all_index_pools

    def add(self, pool_name, node_names, hac_name):
        """Creates a new Index pool within the commcell

        Args:
            pool_name       (str)   --  Name for the index pool
            node_names      (list)  --  List of strings of all the index pool node names
            hac_name        (str)   --  Name of the HAC cluster to be used while creating pool

        Raises:
            SDKExecption:
                Data type of the input(s) is not valid.

                Response was not success.

                Response was empty.

        Returns:
            object  -   Returns a object of class IndexPool

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

    def delete(self, pool_name):
        """Deletes an existing index pool cloud from commcell

        Args:
            pool_name       (str)   --  Index pool cloud name

        Returns:
            None

        Raises:
              SDKExecption:
                  Data type of the input(s) is not valid.

                  Response was not success.

                  Response was empty.
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
    """Class for performing index pool operations on a specific index pool"""

    def __init__(self, commcell_obj, pool_name, pool_id=None):
        """Initializes the IndexPool class instance

        Args:
            commcell_obj        (object)    --  Instance of class Commcell
            pool_name           (str)       --  Index pool name
            pool_id             (int)       --  Index pool client id
                default:
                    None

        Returns:
            object  -   instance of the IndexPool class

        """
        self.commcell = commcell_obj
        self._pool_name = pool_name
        self._pool_id = pool_id
        self.pool_client = None
        self.pool_properties = None
        self.pool_nodes = None
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of the IndexPool class."""
        return "IndexPool class instance for Commcell"

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
        """Refreshes properties of IndexPool class"""
        self.commcell.clients.refresh()
        if not self.commcell.clients.has_client(self.pool_name):
            raise SDKException('IndexPools', '102')
        self.pool_client = self.commcell.clients.get(self.pool_name)
        self._pool_id = self.pool_client.client_id
        self.pool_properties = self.pool_client.\
            properties['pseudoClientInfo']['distributedClusterInstanceProperties']['clusterConfig']['cloudInfo']
        self.pool_nodes = self.pool_properties['cloudNodes']

    def node_info(self, node_name):
        """Returns the index pool node information

            Args:
                node_name       (str)       --  index pool node name

            Returns:
                dict    -   dictionary consisting details of index pool node

            Raises:
                SDKException:
                    Index pool node not found

        """
        for node_info in self.pool_nodes:
            if node_info['nodeClientEntity']['clientName'].lower() == node_name.lower():
                return node_info
        raise SDKException('IndexPools', '103')

    def modify_node(self, node_name,
                    operation_type=IndexServerConstants.OPERATION_EDIT,
                    node_params=None):
        """Method to modify the pool node details

        Args:
            node_name           (str)   --  index pool node name
            operation_type      (int)   --  operation type (1, 2, 3)
                                            1 - Adds a new node
                                            2 - Removes existing node
                                            3 - Edits the existing node (default)
            node_params         (list)  --  list of all the properties for the index pool node
                                            for example:
                                                [{
                                                    "name": <property_name>,
                                                    "value": <property_value>
                                                },
                                                ]
        Raises:
            SDKException:
                Response was not success.
                Response was empty.

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
    def pool_id(self):
        """Returns the index pool client id"""
        return self._pool_id

    @property
    def cloud_id(self):
        """Returns the index pool cloud id"""
        return self.pool_properties['cloudInfoEntity']['cloudId']

    @property
    def pool_name(self):
        """Returns index pool name"""
        return self._pool_name

    @property
    def node_names(self):
        """Returns a list of index pool node names"""
        result = []
        for node_info in self.pool_nodes:
            result.append(node_info['nodeClientEntity']['clientName'])
        return result

    @property
    def hac_cluster(self):
        """Returns the hac cluster name assigned to the index pool"""
        return self.pool_properties['solrCloudPoolInfo']['zookerEntity']['clientGroupName']
