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

import http.client as httplib
from copy import deepcopy
import enum
from .exception import SDKException
from .datacube.constants import IndexServerConstants


class IndexServers(object):
    """Class for representing all the index servers associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the IndexServers class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the IndexServers class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._all_index_servers = None
        self._roles_obj = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all index servers of the commcell.

                Returns:
                    str - string of all the index servers with different roles associated
                    with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'IS Name')
        index = 1
        for index_server in self._all_index_servers:
            representation_string += '{:^5}\t{:^20}\n'.format(
                index, index_server['engineName'])
            index += 1
        return representation_string

    def __repr__(self):
        """Representation string for the instance of the IndexServers class."""
        return "IndexServers class instance for Commcell"

    def __len__(self):
        """Returns the number of the index servers associated with the commcell"""
        return len(self._all_index_servers)

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

                Raises:
                    SDKException:
                        Response was not success
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def _get_index_servers(self):
        """Method to retrieve all the index server available on commcell.

            Raises:
                SDKException:
                    Failed to get the list of analytics engines

                    Response was not success
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

    def _get_all_roles(self):
        """Creates an instance of _Roles class and adds it to the IndexServer class"""
        self._roles_obj = _Roles(self._commcell_object)

    @property
    def all_index_servers(self):
        """Returns the details of all the index server for associated commcell.

                Returns:
                    dict - dictionary consisting details of all the index servers
                    associated with commcell
                    Sample - {
                                <cloud_id_1>   :
                                    {
                                        "engineName" : <property_value>,
                                        "internalCloudName" : <property_value>,
                                        ...
                                    },
                                <cloud_id_2>   :
                                    {
                                        "engineName" : <property_value>,
                                        "cloudID" : <property_value>,
                                        ...
                                    }
                            }
        """
        return self._all_index_servers

    @property
    def roles_data(self):
        """Returns the details of all the cloud roles data

                Returns:
                    list - list of dictionary containing details of the cloud roles
        """
        return self._roles_obj.roles_data

    def refresh(self):
        """Refresh the properties of IndexServers class"""
        self._all_index_servers = {}
        self._get_index_servers()
        if not self._roles_obj:
            self._get_all_roles()

    def update_roles_data(self):
        """Synchronises all the cloud roles details with the commcell"""
        self._roles_obj.update_roles_data()

    def get_properties(self, cloud_name):
        """Returns all details of a index server with the cloud name

                Args:
                    cloud_name     (str)       --  cloud name of index server

                Returns:
                    dict        -   dict consisting details of the index server
        """
        for index_server in self._all_index_servers:
            if self._all_index_servers[index_server]['engineName'] == cloud_name:
                return self._all_index_servers[index_server]
        raise SDKException('IndexServers', '102')

    def has(self, cloud_name):
        """Returns True if the index server with given name is present in commcell.

                Args:
                    cloud_name     (str)       --  the engine name of index server

                Returns:
                    boolean     -   True if index server with given name as is_name
                    is associated with the commcell else returns False

                Raises:
                    SDKExecption:
                        Data type of the input(s) is not valid
        """
        if isinstance(cloud_name, str):
            for index_server in self._all_index_servers:
                if self._all_index_servers[index_server]["engineName"].lower() == cloud_name.lower():
                    return True
            return False
        raise SDKException('IndexServers', '101')

    def get(self, cloud_data):
        """Returns IndexServer object if a index server is found.

                Args:
                    cloud_data        (int/str)       --    cloud name or
                                                            cloud ID of index server

                Returns:
                    object            (IndexServer)   --  Instance on index server with
                    the engine name or cloud id as item

                Raises:
                    SDKException:
                        Index Server not found.

                        Data type of the input(s) is not valid.
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
            index_server_name,
            index_server_node_names,
            index_directory,
            index_server_roles,
            index_pool_name=None,
            is_cloud=False,
            cloud_param=None):
        """Creates an index server within the commcell

                Args:
                    index_server_node_names         (list)  --  client names for index server node
                    index_server_name               (str)   --  name for the index server
                    index_directory                 (list)  --  list of index locations for the index server
                                                                nodes respectively
                                                    For example:
                                                            [<path_1>] - same index location for all the nodes
                                                            [<path_1>, <path_2>, <path_3>] - different index
                                                    location for index server with 3 nodes
                    index_server_roles              (list)  --  list of role names to be assigned
                    index_pool_name                 (str)   --  name for the index pool to used by cloud index server
                    cloud_param                     (list)  --  list of custom parameters to be parsed
                                                    into the json for index server meta info
                                                    [
                                                        {
                                                            "name": <name>,
                                                            "value": <value>
                                                        }
                                                    ]
                    is_cloud            (bool)  --  if true then creates a cloud mode index server

                Raises:
                    SDKException:
                        Data type of the input(s) is not valid.

                        Response was not success.

                        Response was empty.
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

    def delete(self, cloud_name):
        """Deletes / removes an index server from the commcell

                Args:
                    cloud_name      (str)   --  cloud name of index server
                    to be removed from the commcell

                Raises:
                    SDKException:
                        Data type of the input(s) is not valid.

                        Response was not success.

                        Response was empty.
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

    def prune_orphan_datasources(self):
        """Deletes all the orphan datasources
            Raises:
                SDKException:
                    if failed to prune the orphan datasources

                    If response is empty

                    if response is not success
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
    """Enum class for Index Server OS Type"""
    WINDOWS = "Windows"
    UNIX = "Unix"
    MIXED = "Mixed"


class IndexServer(object):
    """Class for performing index server operations for a specific index server"""

    def __init__(self, commcell_obj, name, cloud_id=None):
        """Initialize the IndexServer class instance.

            Args:
                commcell_obj    (object)        --  instance of the Commcell class

                name            (str)           --  name of the index server

                cloud_id        (int)           --  cloud id of the index server
                    default: None

            Returns:
                object - instance of the IndexServer class
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

    def __repr__(self):
        """String representation of the instance of this class."""
        return 'IndexServer class instance for index server: "{0}"'.format(
            self._engine_name)

    def _get_cloud_id(self):
        """Get the cloud id for the index server

                Returns:
                    int - cloud id for the index server
        """
        return self._commcell_obj.index_servers.get(self._engine_name).cloud_id

    def _get_properties(self):
        """Get the properties of the index server"""
        self._properties = self._commcell_obj.index_servers.get_properties(
            self._engine_name)

    def refresh(self):
        """Refresh the index server properties"""
        self._commcell_obj.index_servers.refresh()
        self._get_properties()
        if self.os_type is None:
            self.os_type = self.get_os_info()
        if not self._roles_obj:
            self._roles_obj = _Roles(self._commcell_obj)
        if self.plan_info is None:
            self.plan_info = self.get_plan_info()

    def update_roles_data(self):
        """Synchronize the cloud roles data with the commcell"""
        self._roles_obj.update_roles_data()

    def modify(self, index_location, node_name, node_params):
        """Modifies the properties of an index server

            Args:
                index_location      (str)       --  index server data directory
                node_name           (str)       --  index server node name
                node_params         (dict)      --  parameters to be passed
                                                    [
                                                        {
                                                            "name" : <property_name>,
                                                            "value" : <property_value>
                                                        }
                                                    ]
            Raises:
                SDKException:
                    Response was not success.
                    Response was empty.
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

    def change_plan(self, plan_name):
        """Modifies the plan used by an index server

            Args:
                plan_name      (str)       --  Name of the plan to be used for the index server
            Raises:
                SDKException:
                    Response was not success.
                    Response was empty.
                    if plan with given name doesn't exist
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

    def update_role(self, props=None):
        """Updates a role of an Index Server

            Args:
                props               (list)  --  array of dictionaries
                consisting details of the roles such as role name
                and operation type.
                                            [{
                                                "roleName": <name>          (str)
                                                "operationType": 1 or 2     (int)
                                                    1 for adding a role
                                                    2 for removing a role
                                            }]

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def delete_docs_from_core(self, core_name, select_dict = None):
        """Deletes the docs from the given core name on index server depending on the select dict passed

                Args:

                        core_name               (str)  --  name of the solr core
                        select_dict             (dict) --  dict with query to delete specific documents
                                                    default query - "*:*" (Deletes all the docs)

                    Returns:
                        None

                    Raises:
                        SDKException:

                            if input data is not valid

                            if index server is cloud, not implemented error

                            if response is empty

                            if response is not success
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

    def hard_commit(self, core_name):
        """do hard commit for the given core name on index server

                    Args:

                        core_name               (str)  --  name of the solr core

                    Returns:
                        None

                    Raises:
                        SDKException:

                            if input data is not valid

                            if index server is cloud, not implemented error

                            if response is empty

                            if response is not success
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

    
    def get_health_indicators(self, client_name=None):
        """Get health indicators for index server node by client name

                Args:
                    client_name     (str)       --  name of the client node

                Returns:
                    (response(str)) -- str json object

                Raises:

                    SDKException:
                        if input data is not valid
                        if client name is not passed for index server cloud
                        if response is not success
                        if response is empty

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

    def get_all_cores(self, client_name=None):
        """gets all cores & core details from index server

                Args:
                    client_name     (str)       --  name of the client node
                        ***Applicable only for solr cloud mode or multi node Index Server***

                Returns:
                    (list,dict)     -- list containing core names
                                    -- dict containing details about cores

                Raises:

                    SDKException:

                        if input data is not valid

                        if client name is not passed for index server cloud

                        if response is not success

                        if response is empty

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

    def _create_solr_query(self, select_dict=None, attr_list=None, op_params=None):
        """Method to create the solr query based on the params
            Args:
                select_dict     (dictionary)     --  Dictionary containing search criteria and value
                                                     Acts as 'q' field in solr query

                attr_list       (set)            --  Column names to be returned in results.
                                                     Acts as 'fl' in solr query

                op_params       (dictionary)     --  Other params and values for solr query
                                                        (Ex: start, rows)

            Returns:
                The solr url based on params

            Raises:
                SDKException:

                        if failed to form solr query
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
            core_name,
            solr_client=None,
            select_dict=None,
            attr_list=None,
            op_params=None):
        """Creates solr url based on input and executes it on solr on given core/collection
            Args:

                core_name               (str)           --  Core name/collection name where we want to query

                solr_client             (str)           --  Index Server client name to execute solr query
                                                                Default : None (picks first client on index server)

                select_dict             (dictionary)    --  Dictionary containing search criteria and
                                                            value. Acts as 'q' field in solr query

                        Example :

                            1. General Criteria to filter results              -   {"jid": 1024, "datatype": 2,clid: 2}
                            2. Keyword Searches on solr                        -   {'keyword': 'SearchKeyword'}
                            3. For multiple value searches on single field     -   {'cvowner': ['xxx','yyy']}
                            4. For single value searches on multiple fields    -   {('cvowner','cvreaddisp') : 'xxx'}

                attr_list               (set)           --  Column names to be returned in results.
                                                                Acts as 'fl' in solr query

                        Example (For Exchange Mailbox IDA, below fields are there in solr) :
                                    {
                                     'msgclass',
                                     'ccsmtp',
                                     'fmsmtp',
                                     'folder'
                                   }

                op_params               (dictionary)    --  Other params and values for solr query. Do not
                                                            mention 'wt' param as it is always json

                                                            Example : {"rows": 0}

            Returns:
                content of the response

            Raises:
                SDKException:

                        if unable to send request

                        if response is not success
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

    def get_index_node(self, node_name):
        """Returns an Index server node object for given node name
            Args:
                node_name           (str)   --  Index server node name

            Returns:
                IndexNode class object

            Raises:
                SDKException:

                        if node not found for the given node name

        """
        node_name = node_name.lower()
        if node_name in self.client_name:
            return IndexNode(self._commcell_obj, self.engine_name, node_name)
        raise SDKException("IndexServers", '104', 'Index server node not found')

    def get_plan_info(self):
        """Gets the plan information of the index server
            Returns:
                dict - containing the plan information
        """
        client = self._commcell_obj.clients.get(self.engine_name)
        instance_props = client.properties.get("pseudoClientInfo", {}).get("distributedClusterInstanceProperties", {})
        plan_details = instance_props.get("clusterConfig",{}).get("cloudInfo", {}).get("planInfo", {})
        return plan_details

    def get_os_info(self):
        """Returns the OS type for the Index server"""

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

    def __form_field_query(self, key, value):
        """
        Returns the query with the key and value passed
        Args:
                key(str)    -- key for forming the query
                value(str)  -- value for forming the query
            Returns:
                query to be executed against solr
        """
        query = None
        if value is None:
            query = f'&{key}'
        else:
            query = f'&{key}={str(value)}'
        return query

    @property
    def plan_name(self):
        """Returns the plan name associated with index server
            Returns:
                str - name of the plan
        """
        return self.plan_info.get("planName")

    @property
    def os_info(self):
        """Returns the OS type for the Index server"""
        return self.os_type

    @property
    def is_cloud(self):
        """Returns true if the Index server is cloud and false if not"""
        return self.server_type == 5

    @property
    def nodes_count(self):
        """Returns the count of Index server nodes"""
        return len(self.client_id)

    @property
    def roles_data(self):
        """Returns the cloud roles data"""
        return self._roles_obj.roles_data

    @property
    def properties(self):
        """Returns the index server properties"""
        return self._properties

    @property
    def host_name(self):
        """Returns a list of host names of all index server nodes"""
        return self._properties[IndexServerConstants.HOST_NAME]

    @property
    def cloud_name(self):
        """Returns the internal cloud name of index server"""
        return self._properties[IndexServerConstants.CLOUD_NAME]

    @property
    def client_name(self):
        """Returns a list of client names of all index server nodes"""
        return self._properties[IndexServerConstants.CLIENT_NAME]

    @property
    def server_url(self):
        """Returns a list of Solr url of all index server nodes"""
        return self._properties[IndexServerConstants.CI_SERVER_URL]

    @property
    def type(self):
        """Returns the type of index server"""
        return self._properties[IndexServerConstants.TYPE]

    @property
    def base_port(self):
        """Returns a list of base ports of all index server nodes"""
        return self._properties[IndexServerConstants.BASE_PORT]

    @property
    def client_id(self):
        """Returns a list client ids of all index server nodes"""
        return self._properties[IndexServerConstants.CLIENT_ID]

    @property
    def roles(self):
        """Returns a list of roles of index server"""
        return self._properties[IndexServerConstants.ROLES]

    @property
    def role_display_name(self):
        """Returns the roles display name of index server"""
        role_disp_name = []
        for role_version in self.roles:
            for role in self.roles_data:
                if role_version == role['roleVersion']:
                    role_disp_name.append(role['roleName'])
                    break
        return role_disp_name

    @property
    def cloud_id(self):
        """Returns the cloud id of index server"""
        return self._properties[IndexServerConstants.CLOUD_ID]

    @property
    def server_type(self):
        """Returns the server type of index server"""
        return self._properties[IndexServerConstants.SERVER_TYPE]

    @property
    def engine_name(self):
        """Returns the engine name of index server"""
        return self._properties[IndexServerConstants.ENGINE_NAME]

    @property
    def index_server_client_id(self):
        """Returns the index server client id of index server"""
        return self._properties[IndexServerConstants.INDEX_SERVER_CLIENT_ID]

    @property
    def fs_collection(self):
        """Returns the multinode collection name of File System Index

            Returns:

                str --  File System index multinode collection name

        """
        return f'fsindex_{"".join(letter for letter in self.cloud_name if letter.isalnum())}_multinode'


class IndexNode(object):
    """Class for Index server node object"""

    def __init__(self, commcell_obj, index_server_name, node_name):
        """Initialize the IndexNode class

            Args:
                commcell_obj        (object)    --  commcell object
                index_server_name   (int)       --  Index server name
                node_name           (str)       --  Index server node client name

        """
        self.commcell = commcell_obj
        self.index_server_name = index_server_name
        self.data_index = 0
        self.index_server = None
        self.index_node_name = node_name.lower()
        self.index_node_client = None
        self.index_client_properties = None
        self.refresh()

    def refresh(self):
        """Refresh the index node properties"""
        self.commcell.index_servers.refresh()
        self.index_server = self.commcell.index_servers.get(self.index_server_name)
        self.data_index = self.index_server.client_name.index(self.index_node_name)
        self.commcell.clients.refresh()
        self.index_node_client = self.commcell.clients.get(self.index_node_name)
        # TODO: Rewrite Index server API logic to access client properties
        self.index_client_properties = (self.index_node_client.properties.get('pseudoClientInfo', {}).
                                        get('indexServerProperties', {}))

    @property
    def node_name(self):
        """Returns Index server node client name"""
        return self.index_server.client_name[self.data_index]

    @property
    def node_id(self):
        """Returns Index server node client id"""
        return self.index_server.client_id[self.data_index]

    @property
    def solr_port(self):
        """Returns port number Solr is running on the Index server node"""
        return self.index_server.base_port[self.data_index]

    @property
    def solr_url(self):
        """Returns Solr URL for Index server node"""
        return self.index_server.server_url[self.data_index]

    @property
    def roles(self):
        """Returns the array of roles installed with the index server within the commcell"""
        return self.index_server.role_display_name

    @property
    def index_location(self):
        """Returns Index directory for the Index server Node"""
        node_meta_infos = self.index_client_properties['nodeMetaInfos']
        for info in node_meta_infos:
            if info['name'] == 'INDEXLOCATION':
                return info['value']
        return None

    @property
    def jvm_memory(self):
        """Returns Solr JVM memory for the Index server Node"""
        node_meta_infos = self.index_client_properties['nodeMetaInfos']
        for info in node_meta_infos:
            if info['name'] == 'JVMMAXMEMORY':
                return info['value']
        return None

    @solr_port.setter
    def solr_port(self, port_no):
        """Setter to set the Solr port number for the node

            Args:
                port_no     (str)   --  Solr port number to be set for node

        """
        solr_port_param = deepcopy(IndexServerConstants.SOLR_PORT_META_INFO)
        solr_port_param['value'] = str(port_no)
        cloud_param = [solr_port_param]
        self.index_server.modify(self.index_location, self.index_node_name, cloud_param)
        self.refresh()

    @jvm_memory.setter
    def jvm_memory(self, memory):
        """Setter to set the Solr JVM memory for the node

                    Args:
                        memory      (str)   --  Solr JVM memory to be set for the node

        """
        solr_jvm_param = deepcopy(IndexServerConstants.SOLR_JVM_META_INFO)
        solr_jvm_param['value'] = str(memory)
        solr_port_param = deepcopy(IndexServerConstants.SOLR_PORT_META_INFO)
        solr_port_param['value'] = str(self.solr_port)
        cloud_param = [solr_jvm_param, solr_port_param]
        self.index_server.modify(self.index_location, self.index_node_name, cloud_param)
        self.refresh()


class _Roles(object):
    """Class for cloud roles data operations"""

    def __init__(self, commcell_object):
        """Initializes _Roles class with commcell object

            Args:
                commcell_object (object)    --  instance of Commcell class

            Returns:
                object  -   instance of _Roles class
        """
        self.commcell_object = commcell_object
        self._roles_data = None
        self.refresh()

    def refresh(self):
        """Refreshes the class data"""
        self._get_all_roles()

    def _get_all_roles(self):
        """Method to get all cloud roles details available on the commcell.

            Raises:
                SDKException:
                    Response was empty.

                    Response was not success.
        """
        flag, response = self.commcell_object._cvpysdk_object.make_request(
            "GET", self.commcell_object._services['GET_ALL_ROLES']
        )
        if flag:
            if response.json():
                if 'rolesInfo' in response.json():
                    self._roles_data = response.json()['rolesInfo']
                    return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101')

    def get_role_id(self, role_name):
        """Method to get a cloud role id with given name

            Args:
                role_name       (str)   --  cloud role name of which role id has to be returned

            Returns:
                role_id         (int)   --  if role name is found in roles data then returns the id
                                            else returns None

        """
        for role_data in self._roles_data:
            if role_data['roleName'] == role_name:
                return role_data['roleId']
        return None

    def update_roles_data(self):
        """Synchronize the cloud role data with the commcell database"""
        self._get_all_roles()

    @property
    def roles_data(self):
        """Returns the list of dictionary of details of each cloud role"""
        return self._roles_data
