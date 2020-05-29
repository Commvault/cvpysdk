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

    update_role()                       --  to update the roles assigned to cloud

    hard_commit                         --  do hard commit on specified index server solr core

    get_all_cores                       --  gets all the cores in index server


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

from copy import deepcopy
from past.builtins import basestring
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
        return "IndexServers class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

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
                        if item['version'] not in self._all_index_servers[item['cloudID']]['version']:
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
                        item['version'] = [item['version']]
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
        if isinstance(cloud_name, basestring):
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
        elif isinstance(cloud_data, basestring):
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
                    index_directory                 (str)   --  index location for the index server
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
                and isinstance(index_server_name, basestring)):
            raise SDKException('IndexServers', '101')
        cloud_meta_infos = {
            'INDEXLOCATION': index_directory,
            'REPLICATION': '1',
            'LANGUAGE': '0'
        }
        node_meta_infos = {
            'PORTNO': '20000',
            'JVMMAXMEMORY': '8191'
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
            role_meta_infos['ISCLOUDMODE'] = '3'
            node_meta_infos['WEBSERVER'] = 'true'
        for node_name in index_server_node_names:
            node_obj = self._commcell_object.clients[node_name]
            node_data = {
                "opType": IndexServerConstants.OPERATION_ADD,
                "nodeClientEntity": {
                    "hostName": node_obj['hostname'],
                    "clientId": int(node_obj['id']),
                    "clientName": node_name
                },
                'nodeMetaInfos': []
            }
            for node_info in node_meta_infos:
                node_data['nodeMetaInfos'].append({
                    'name': node_info,
                    'value': node_meta_infos[node_info]
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
        if not isinstance(cloud_name, basestring):
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


class IndexServer(object):
    """Class for performing index server operations for a specific index server"""

    def __init__(self, commcell_obj, name, cloud_id=None):
        """Initialise the IndexServer class instance.

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
        self._get_properties()
        if not self._roles_obj:
            self._roles_obj = _Roles(self._commcell_obj)

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
        if not isinstance(core_name, basestring):
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

    def get_all_cores(self, client_name=None):
        """gets all cores & core details from index server

                Args:
                    client_name     (str)       --  name of the client node
                        ***Applicable only for solr cloud mode***

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
        if self.is_cloud:
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

    @property
    def is_cloud(self):
        return self.server_type == 5

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
        """Returns the host name of index server"""
        return self._properties[IndexServerConstants.HOST_NAME]

    @property
    def cloud_name(self):
        """Returns the internal cloud name of index server"""
        return self._properties[IndexServerConstants.CLOUD_NAME]

    @property
    def client_name(self):
        """Returns the client name of index server"""
        return self._properties[IndexServerConstants.CLIENT_NAME]

    @property
    def server_url(self):
        """Returns the content indexing url of index server"""
        return self._properties[IndexServerConstants.CI_SERVER_URL]

    @property
    def type(self):
        """Returns the type of index server"""
        return self._properties[IndexServerConstants.TYPE]

    @property
    def base_port(self):
        """Returns the base port of index server"""
        return self._properties[IndexServerConstants.BASE_PORT]

    @property
    def client_id(self):
        """Returns the client id of index server"""
        return self._properties[IndexServerConstants.CLIENT_ID]

    @property
    def roles(self):
        """Returns the roles of index server"""
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
