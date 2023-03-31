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

    #. Get the Id for the given Storage Pool


StoragePools
============

    __init__(commcell_object)   --  initializes object of the StoragePools class associated
    with the commcell

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

    add_azure_storage_pool()    --  Adds new storage pool with provided name to the commcell

    delete()                    --  deletes the specified storage pool

    refresh()                   --  refresh the list of storage pools associated with the commcell


Attributes
----------

    **all_storage_pools**   --  returns dict of all the storage pools on commcell


StoragePool
===========

__init__(commcell_object,
            storage_pool_name,
            storage_pool_id)    --  initialize the instance of StoragePool class for specific
                                    storage pool of commcell
__repr__()                      --  returns a string representation of the
                                StoragePool instance
 _get_storage_pool_properties()        --  returns the properties of this storage pool

refresh()		                        --	Refresh the properties of the StoragePool

StoragePool instance attributes
================================

**storage_policy_name**         --  returns the name of the StoragePool as seen on GUI

**storage_policy_id**           --  returns the storage pool id


# TODO: check with MM API team to get the response in JSON


"""
import copy

import xmltodict

from .exception import SDKException

# from .job import Job

from .storage import DiskLibrary
from .storage import MediaAgent
from .security.security_association import SecurityAssociation
from .constants import StoragePoolConstants


class StoragePools:
    """Class for doing operations on Storage Pools, like get storage poo ID."""

    def __init__(self, commcell_object):
        """Initializes instance of the StoragePools class to perform operations on a storage pool.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the StoragePools class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._add_storage_pool_api = self._services['ADD_STORAGE_POOL']

        self._storage_pools_api = self._services['STORAGE_POOL']
        self._storage_pools = None

        self.refresh()

    def __str__(self):
        """Representation string consisting of all storage pools present in the Commcell.

            Returns:
                str     -   string of all the storage pools associated with the commcell

        """
        representation_string = '{:^5}\t{:^40}\n\n'.format('S. No.', 'Storage Pool')

        for index, storage_pool in enumerate(self._storage_pools):
            sub_str = '{:^5}\t{:40}\n'.format(index + 1, storage_pool)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Returns the string representation of an instance of this class."""
        return "StoragePools class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the storage pools added to the Commcell."""
        return len(self.all_storage_pools)

    def __getitem__(self, value):
        """Returns the name of the storage pool for the given storage pool ID or
            the details of the storage pool for given storage pool Name.

            Args:
                value   (str / int)     --  Name or ID of the storage pool

            Returns:
                str     -   name of the storage pool, if the storage pool id was given

                dict    -   dict of details of the storage pool, if storage pool name was given

            Raises:
                IndexError:
                    no storage pool exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_storage_pools:
            return self.all_storage_pools[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_storage_pools.items()))[0][0]
            except IndexError:
                raise IndexError('No storage pool exists with the given Name / Id')

    def _get_storage_pools(self):
        """Gets all the storage pools associated with the Commcell environment.

            Returns:
                dict    -   consists of all storage pools added to the commcell

                    {
                        "storage_pool1_name": storage_pool1_id,

                        "storage_pool2_name": storage_pool2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    @property
    def all_storage_pools(self):
        """Returns dict of all the storage pools on this commcell

            dict    -   consists of all storage pools added to the commcell

                {

                    "storage_pool1_name": storage_pool1_id,

                    "storage_pool2_name": storage_pool2_id
                }

        """
        return self._storage_pools

    def has_storage_pool(self, name):
        """Checks if a storage pool exists in the Commcell with the input storage pool name.

            Args:
                name    (str)   --  name of the storage pool

            Returns:
                bool    -   boolean output whether the storage pool exists in the commcell or not

        """
        return self._storage_pools and name.lower() in self._storage_pools

    def get(self, name):
        """Returns the id of the storage pool for the given storage pool name.

            Args:
                name    (str)   --  name of the storage pool to get the id of

            Returns:
                str     -   id of the storage pool for the given storage pool name

            Raises:
                SDKException:
                    if no storage pool exists with the given name

        """
        name = name.lower()

        if self.has_storage_pool(name):
            return StoragePool(self._commcell_object, name, storage_pool_id=self._storage_pools[name])
        else:
            raise SDKException('StoragePool', '103')

    def hyperscale_create_storage_pool(self, storage_pool_name, media_agents):
        """
            Create new storage pool for hyperscale
            Args:
                storage_pool_name (string) -- Name of the storage pools to create
                
                media_agents      (List)   -- List of 3 media agents with name's(str)
                                                or instance of media agent's(object)
                                                
                Example: ["ma1","ma2","ma3"]

            Return:
                 flag, response -- response returned by the REST API call
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

    def add(self, storage_pool_name, mountpath, media_agent, ddb_ma, dedup_path):
        """
        Adds a new storage pool to commcell

        Args:
            storage_pool_name   (str)       --  name of new storage pool to add

            mountpath           (str)       --  mount path for the storage pool

            media_agent         (str/object)--  name or instance of media agent

            ddb_ma              (str/object)--  name or instance of dedupe media agent

            dedup_path          (str)       --  path where the DDB should be stored

        Returns:
            StoragePool object if creation is successful

        Raises:
            Exception if creation is unsuccessful
        """
        # from urllib.parse import urlencode

        if ((dedup_path is not None and not isinstance(dedup_path, str)) or
                not (isinstance(storage_pool_name, str) or not isinstance(mountpath, str))):
            raise SDKException('Storage', '101')

        # if isinstance(library, DiskLibrary):
        #     disk_library = library
        # elif isinstance(library, str):
        #     disk_library = DiskLibrary(self._commcell_object, library)
        # else:
        #     raise SDKException('Storage', '104')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, str):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        else:
            raise SDKException('Storage', '103')

        if isinstance(ddb_ma, MediaAgent):
            ddb_ma = ddb_ma
        elif isinstance(ddb_ma, str):
            ddb_ma = MediaAgent(self._commcell_object, ddb_ma)
        else:
            raise SDKException('Storage', '103')

        request_json = {
            "storagePolicyName": storage_pool_name,
            "type": 1,
            "copyName": "Primary",
            "numberOfCopies": 1,
            "storage": [
                {
                    "path": mountpath,
                    "mediaAgent": {
                        "mediaAgentId": int(media_agent.media_agent_id),
                        "mediaAgentName": media_agent.media_agent_name
                    },
                    "credentials": {}
                }
            ],
            "storagePolicyCopyInfo": {
                "copyType": 1,
                "isFromGui": True,
                "active": 1,
                "isDefault": 1,
                "dedupeFlags": {
                    "enableDASHFull": 1,
                    "hostGlobalDedupStore": 1,
                    "enableDeduplication": 1
                },
                "storagePolicyFlags": {
                    "blockLevelDedup": 1,
                    "enableGlobalDeduplication": 1
                },
                "DDBPartitionInfo": {
                    "maInfoList": [
                        {
                            "mediaAgent": {
                                "mediaAgentId": int(ddb_ma.media_agent_id),
                                "mediaAgentName": ddb_ma.media_agent_name
                            },
                            "subStoreList": [
                                {
                                    "accessPath": {
                                        "path": dedup_path
                                    }
                                }
                            ]
                        }
                    ]
                },
                "library": {
                    "libraryName": mountpath,
                },
                "mediaAgent": {
                    "mediaAgentId": int(media_agent.media_agent_id),
                    "mediaAgentName": media_agent.media_agent_name
                }
            }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._add_storage_pool_api, request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if int(error_code) != 0:
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create storage policy\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
        return self.get(storage_pool_name)

    def add_azure_storage_pool(self, storage_pool_name, container_name, media_agents, dedup_paths, **kwargs):
        """ Adds new storage pool with provided name to the commcell
                 Args:
                     storage_pool_name (str)     --  name of the storage pool to be created

                     container_name (str)        --  container name to be used with storage pool

                     media_agents (list)         --  list of media agent names to be used for storage pool

                     dedup_paths (list)          --  list of paths for storing deduplication data

                     **kwargs (dict)             --  dict of keyword arguments as follows
                         username        (str)   --  azure storage credential username
                         password        (str)   --  azure storage credential password
                         credential_name (str)   --  Credential name to be used

                 Returns:
                     Azure storage policy object

                 Raises:
                     SDKException:
                         If invalid type arguments are passed
                         If Storage Pool with given name already exist
                         Response was not success.
                         Response was empty.

        """
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")
        credential_name = kwargs.get("credential_name", "")
        if not (isinstance(storage_pool_name, str) and isinstance(container_name, str)
                and isinstance(media_agents, list) and isinstance(dedup_paths, list)
                and isinstance(username, str) and isinstance(password, str)
                and isinstance(credential_name, str)):
            raise SDKException('StoragePool', '101')
        storage_pools = self._commcell_object.storage_pools
        if storage_pools.has_storage_pool(storage_pool_name):
            raise SDKException('StoragePool', '103')
        request_json = copy.deepcopy(StoragePoolConstants.AZURE_STORAGE_REQ_JSON)
        request_json["storagePolicyName"] = storage_pool_name
        storage_policy_info = request_json["storagePolicyCopyInfo"]
        storage_ma = self._commcell_object.media_agents.get(media_agents[0])
        storage_policy_info["library"]["libraryName"] = container_name
        storage_policy_info["mediaAgent"]["mediaAgentId"] = int(storage_ma.media_agent_id)
        storage_policy_info["mediaAgent"]["mediaAgentName"] = storage_ma.media_agent_name
        ddb_info = []
        for (ma, ddb_path) in zip(media_agents, dedup_paths):
            ma_ddb = copy.deepcopy(StoragePoolConstants.MA_INFO_LIST)
            ma_info = self._commcell_object.media_agents.get(ma)
            ma_ddb["mediaAgent"]["mediaAgentId"] = int(ma_info.media_agent_id)
            ma_ddb["mediaAgent"]["mediaAgentName"] = ma_info.media_agent_name
            ma_ddb["subStoreList"][0]["accessPath"]["path"] = ddb_path
            ddb_info.append(ma_ddb)
        storage_policy_info["DDBPartitionInfo"]["maInfoList"] = ddb_info
        storage_info = request_json["storage"][0]
        storage_info["path"] = container_name
        storage_info["mediaAgent"]["mediaAgentId"] = int(storage_ma.media_agent_id)
        storage_info["mediaAgent"]["mediaAgentName"] = storage_ma.media_agent_name
        storage_info["credentials"]["userName"] = username
        storage_info["credentials"]["password"] = password
        credential = self._commcell_object.credentials.get(credential_name)
        storage_info["savedCredential"]["credentialId"] = credential.credential_id
        storage_info["savedCredential"]["credentialName"] = credential.credential_name
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._add_storage_pool_api, request_json
        )

        if flag:
            if response.json():
                error_code = response.json().get('error', {}).get('errorCode', 0)
                if int(error_code) != 0:
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create storage policy\nError: "{0}"'

                    raise SDKException('StoragePool', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()
        return self.get(request_json["storagePolicyName"])

    def delete(self, storage_pool_name):
        """deletes the specified storage pool.

            Args:
                storage_pool_name (str)  --  name of the storage pool to delete

            Raises:
                SDKException:
                    if type of the storage pool name is not string

                    if failed to delete storage pool

                    if no storage pool exists with the given name

                    if response is empty

                    if response is not success

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

    def refresh(self):
        """Refresh the list of storage pools associated to the Commcell."""
        self._storage_pools = self._get_storage_pools()


class StoragePool(object):
    """Class for individual storage pools"""

    def __init__(self, commcell_object, storage_pool_name, storage_pool_id=None):
        """
        Intitalise the Storage Pool classs instance

        Args:
            commcell_object     (object)        --instance of the Commcell class

            storage_pool_name   (string)    -- Name of the storage pool

            storage_pool_id     (int)       -- Storage pool id
        Returns:
            object - Instance of the StoragePool class

        """
        self._storage_pool_name = storage_pool_name.lower()
        self._commcell_object = commcell_object
        self._storage_pool_properties = None
        self._storage_pool_id = None
        if storage_pool_id:
            self._storage_pool_id = str(storage_pool_id)
        else:
            self._storage_pool_id = self._commcell_object.storage_pools.get(self._storage_pool_name).storage_pool_id

        self._STORAGE_POOL = self._commcell_object._services['GET_STORAGE_POOL'] % (self.storage_pool_id)
        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class"""
        representation_string = "Storage Pool class Instance for {0}".format(self._storage_pool_name)
        return representation_string

    def _get_storage_pool_properties(self):
        """
        Gets StoragePool properties

            Raises:
                SDKException:
                    if repsonse is empty

                    if response is not success

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

    @property
    def storage_pool_name(self):
        """Treats the storage_policy_name as a read only attribute"""
        return self._storage_pool_name

    @property
    def storage_pool_id(self):
        """Treats id as a read only attribute"""
        return self._storage_pool_id

    @property
    def storage_pool_properties(self):
        """Treats the storage_pool_properties as a read only attribute"""
        return self._storage_pool_properties

    @property
    def global_policy_name(self):
        """Returns the global policy corresponding to the storage pool"""
        return self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["StoragePolicyCopy"]["storagePolicyName"]

    def hyperscale_add_nodes(self, media_agents):
        """
        Add 3 new nodes to an existing storage pool

        args:
            media_agents      (List)   -- List of 3 media agents with name's(str)
                                            or instance of media agent's(object)
                                            
            Example: ["ma1","ma2","ma3"]

        Raises:
                SDKException:
                    if add nodes to an existing storage pool fails
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

    def hyperscale_reconfigure_storage_pool(self, storage_pool_name):
        """
        Reconfigures storage pool, for any failure during creation and expansion

        args:
          storage_pool_name (string) -- Name of the storage pools to reconfigure
        Raises:
                SDKException:
                    if reconfigure fails
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

    def hyperscale_replace_disk(self, disk_id, media_agent, storage_pool_name):
        """
              Replace disk action, over a media agent which is part of storage pool
               args:
                    disk_id (int) --> disk id for the disk to replace
                    media_agent (string/object) --> media agent name/ object
                    storage_pool_name (string) --> Name of the storage pools for replacemnet of disk
               Raises:
                       SDKException:
                           if replace fails
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

    def refresh(self):
        """Refreshes propery of the class object"""
        self._get_storage_pool_properties()

    def update_security_associations(self, associations_list, isUser=True, request_type=None, externalGroup=False):
        """
        Adds the security association on the storage pool object

        Args:
            associations_list   (list)  --  list of users to be associated
                Example:
                    associations_list = [
                        {
                            'user_name': user1,
                            'role_name': role1
                        },
                        {
                            'user_name': user2,
                            'role_name': role2
                        }
                    ]

            isUser (bool)           --    True or False. set isUser = False, If associations_list made up of user groups
            request_type (str)      --    eg : 'OVERWRITE' or 'UPDATE' or 'DELETE', Default will be OVERWRITE operation
            externalGroup (bool)    --    True or False, set externalGroup = True. If Security associations is being done on External User Groups

        Raises:
            SDKException:
                if association is not of List type
        """
        if not isinstance(associations_list, list):
            raise SDKException('StoragePool', '101')

        SecurityAssociation(self._commcell_object, self)._add_security_association(associations_list,
                                                                                   user=isUser,
                                                                                   request_type=request_type,
                                                                                   externalGroup=externalGroup)
