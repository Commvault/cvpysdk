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

import xmltodict

from .exception import SDKException
from past.builtins import basestring
# from future.standard_library import install_aliases

# from .job import Job

from .storage import DiskLibrary
from .storage import MediaAgent


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

            if response is None:
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

    def refresh(self):
        """Refresh the list of storage pools associated to the Commcell."""
        self._storage_pools = self._get_storage_pools()

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

        if ((dedup_path is not None and not isinstance(dedup_path, basestring)) or
                not (isinstance(storage_pool_name, basestring) or not isinstance(mountpath, basestring))):
            raise SDKException('Storage', '101')

        # if isinstance(library, DiskLibrary):
        #     disk_library = library
        # elif isinstance(library, basestring):
        #     disk_library = DiskLibrary(self._commcell_object, library)
        # else:
        #     raise SDKException('Storage', '104')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, basestring):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        else:
            raise SDKException('Storage', '103')

        if isinstance(ddb_ma, MediaAgent):
            ddb_ma = ddb_ma
        elif isinstance(ddb_ma, basestring):
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

        if not isinstance(storage_pool_name, basestring):
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
                else:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'Storage',
                    '102',
                    'No storage pool exists with name: {0}'.format(storage_pool_name)
                )


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

    def refresh(self):
        """Refreshes propery of the class object"""
        self._get_storage_pool_properties()
