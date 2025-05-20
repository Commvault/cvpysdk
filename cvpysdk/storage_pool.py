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

StoragePools, StoragePoolType, StorageType, WORMLockType and StoragePool are the classes defined in this file.

StoragePools: Class for representing all the StoragePools in the commcell

StoragePoolType : Class for representing storage pool types like deduplication, secondary copy, non-dedupe, scale out

StorageType : Class for representing storage types like disk, cloud, tape of a storage pool

WORMLockType : Class for representing different WORM lock types flag values of a WORM enable storage pool

StoragePool: Class for representing a single StoragePool of the commcell


StoragePools
============

    __init__(commcell_object)   --  initializes object of the StoragePools class associated with the commcell

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

    add_air_gap_protect()       --  Adds a new air gap protect storage pool to commcell

Attributes
----------

    **all_storage_pools**   --  returns dict of all the storage pools on commcell


StoragePool
===========

    __init__()                  --  initialize the instance of StoragePool class for specific storage pool of commcell

    __repr__()                  --  returns a string representation of the StoragePool instance

     _get_storage_pool_properties() --  returns the properties of this storage pool

    refresh()                   --	Refresh the properties of the StoragePool

    get_copy()                  --  Returns the StoragePolicyCopy object of Storage Pool copy

    enable_compliance_lock()    --  Enables compliance lock on Storage Pool Copy

    enable_worm_storage_lock()  --  Enables WORM storage lock on storage pool

    hyperscale_add_nodes()      --  Add 3 new nodes to an existing storage pool

StoragePool instance attributes
================================

    **storage_pool_name**           --  returns the name of the storage pool

    **storage_pool_id**             --  returns the storage pool id

    **storage_pool_properties**     --  returns the properties of the storage pool

    **global_policy_name**          --  returns the global policy corresponding to the storage pool

    **copy_name**                   --  returns the copy name of the storage pool

    **copy_id**                     --  returns the copy id of the storage pool

    **storage_pool_type**           --  returns the storage pool type

    **storage_type**                --  returns the storage type of the storage pool

    **storage_vendor**              --  returns the storage vendor id of the storage pool

    **is_worm_storage_lock_enabled**--  returns whether WORM storage lock is enabled

    **is_object_level_worm_lock_enabled** --  returns whether object level WORM lock is enabled

    **is_bucket_level_worm_lock_enabled** --  returns whether bucket level WORM lock is enabled

    **is_compliance_lock_enabled**  --  returns whether compliance lock is enabled

# TODO: check with MM API team to get the response in JSON

"""
import copy

import xmltodict
from base64 import b64encode
from enum import IntFlag, IntEnum

from .exception import SDKException

from .storage import MediaAgent
from .security.security_association import SecurityAssociation
from .constants import StoragePoolConstants
from .policies.storage_policies import StoragePolicyCopy

class StorageType(IntEnum):
    """Class IntEnum to represent different storage types"""
    DISK = 1,
    CLOUD = 2,
    HYPERSCALE = 3,
    TAPE = 4

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

        self._metallic_storage_api = self._services['GET_METALLIC_STORAGE_DETAILS']
        self.__get_agp_storage_api = self._services['GET_AGP_STORAGE']
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
    
    def get_storage_pools_for_a_company(self, company_id, storage_type: StorageType = None):
        """Gets all the storage pools associated with the Commcell environment.

            Args:
                company_id - id of the company for which the associated storge pools are to be fetched

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
        headers['Accept'] = 'application/json'
        headers['onlygetcompanyownedentities'] = '1'
        headers['operatorcompanyid'] = f'{company_id}'

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._storage_pools_api, headers=headers
        )

        if flag:
            storage_pools = {}
            response = response.json()
            if response is None or response.get('storagePoolList') is None:
                storage_pool_list = []
            else:
                storage_pool_list = response['storagePoolList']
            if not isinstance(storage_pool_list, list):
                storage_pool_list = [storage_pool_list]
            if response:
                for pool in storage_pool_list:
                    if storage_type and pool['storageType'] != storage_type:
                        continue
                    # skip agp pools for cloud storage type
                    if storage_type == StorageType.CLOUD and 401 <= pool['libraryVendorType'] <= 499:
                        continue
                    name = pool['storagePoolEntity']['storagePoolName']
                    storage_pool_id = pool['storagePoolEntity']['storagePoolId']

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
        self.refresh()
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

    def add_air_gap_protect(self, storage_pool_name, media_agent, storage_type, storage_class, region_name,
                            ddb_ma=None, dedup_path=None):
        """
            Adds a new air gap protect storage pool to commcell

                Args:
                    storage_pool_name   (str)       --  name of new storage pool to add

                    media_agent         (str/object)--  name or instance of media agent

                    storage_type        (str)        -- name of the cloud vendor (str, eg - "Microsoft Azure storage") (same as UI)

                    storage_class       (str)        -- storage class (str, eg - "Hot","Cool") (same as UI)

                    region_name (str)      --  name of the geographical region for storage (same as UI)

                    ddb_ma              (list<str/object>/str/object)   --  list of (name of name or instance)
                                                                            or name or instance of dedupe media agent

                    dedup_path          (list<str>/str)       --  list of paths or path where the DDB should be stored

                Returns:
                    StoragePool object if creation is successful

                Raises:
                    SDKException, if invalid parameters provided

        """
        license_type_dict = StoragePoolConstants.AIR_GAP_PROTECT_STORAGE_TYPES
        error_message = ""
        if storage_type.upper() in license_type_dict:
            available_storage_classes = license_type_dict[storage_type.upper()]
            if storage_class.upper() in available_storage_classes:
                vendor_id = available_storage_classes[storage_class.upper()]["vendorId"]
                display_vendor_id = available_storage_classes[storage_class.upper()]["displayVendorId"]
            else:
                error_message += f"Invalid storage class provided. Valid storage class {list(available_storage_classes.keys())}"
        else:
            error_message += f"  Invalid storage type provided. {list(license_type_dict.keys())}"

        if error_message:
            raise SDKException('Storage', '101', error_message)

        region = None
        available_regions = []

        #  API call to fetch the region name - sourced directly from the vendor
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._metallic_storage_api)
        if flag:
            if response.json():
                if "storageInformation" in response.json():
                    for storage_info in response.json()["storageInformation"]:
                        if (int(storage_info["vendorId"]) == int(vendor_id)) and (int(storage_info["displayVendorId"]) == int(display_vendor_id)):
                            for region_dict in storage_info["region"]:
                                available_regions.append(region_dict["displayName"])
                                if region_dict["displayName"] == region_name:
                                    region = region_dict["regionName"]
                                    break

                        if region:
                            break

                    if region is None:
                        if not available_regions:
                            raise SDKException('Storage', '101',
                                               f"Active license is required to configure {storage_type} - {storage_class} Air Gap Protect storage")
                        else:
                            raise SDKException('Storage', '101',
                                               f"Invalid region: {region_name} ,\nValid regions: {available_regions}")
                else:
                    raise SDKException('Storage', '101', "Unexpected response returned while fetching Air Gap Protect storage details")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        # cloud server type for air gap protect is 400
        cloud_server_type = 400

        return self.add(storage_pool_name=storage_pool_name, mountpath=None, media_agent=media_agent, ddb_ma=ddb_ma,
                        dedup_path=dedup_path, cloud_server_type=cloud_server_type, region=region, vendor_id=vendor_id,
                        display_vendor_id=display_vendor_id)
        
    def get_air_gap_protect(self, company_id = None):
        """
        Returns the list of air gap protect storage pools in the commcell.
        
        Args:
            company_id (int) -- id of the company to get the air gap protect storage pools for
                                (optional, default is None which returns all air gap protect storage pools)
        
        Returns:
            dict - dictionary of air gap protect storage pools with name as key and id as value
                
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
        headers['Accept'] = 'application/json'
        if company_id:
            headers['onlygetcompanyownedentities'] = '1'
            headers['operatorcompanyid'] = f'{company_id}'

        flag, response = self._cvpysdk_object.make_request(
            'GET', self.__get_agp_storage_api, headers=headers
        )

        if flag:
            storage_pools = {}
            response = response.json()
            if response is None or response.get('cloudStorage') is None:
                storage_pool_list = []
            else:
                storage_pool_list = response['cloudStorage']
            if not isinstance(storage_pool_list, list):
                storage_pool_list = [storage_pool_list]
            if response:
                for pool in storage_pool_list:
                    name = pool['name']
                    storage_pool_id = pool['id']

                    storage_pools[name] = storage_pool_id

            return storage_pools
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add(self, storage_pool_name, mountpath, media_agent, ddb_ma=None, dedup_path=None, **kwargs):
        """
        Adds a new storage pool to commcell

        Args:
            storage_pool_name   (str)       --  name of new storage pool to add

            mountpath           (str)       --  mount path for the storage pool

            media_agent         (str/object)--  name or instance of media agent

            ddb_ma              (list<str/object>/str/object)   --  list of (name of name or instance)
                                                                        or name or instance of dedupe media agent

            dedup_path          (list<str>/str)       --  list of paths or path where the DDB should be stored

            **kwargs:
                username        (str)       --  username to access the mountpath

                password        (str)       --  password to access the mountpath

                credential_name (str)       --  name of the credential as in credential manager

                cloud_server_type (int)     --  cloud server type of the cloud vendor (required)

                region (str)                --  name of geographical region for storage (required for air gap protect)

                vendor_id (int)             -- id for the cloud_vendor (eg - 3 for azure) (required for air gap protect pool)

                display_vendor_id (int)     -- storage Class id for that vendor (eg - 401 for azure hot) (required for air gap protect pool)

                region_id        (int)      --  Cloud Hypervisor specific region ID

                tape_storage (boolean)      -- if library passed is tape library. 

        Returns:
            StoragePool object if creation is successful

        Raises:
            Exception if creation is unsuccessful
        """
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        credential_name = kwargs.get('credential_name', None)
        cloud_server_type = kwargs.get('cloud_server_type', None)
        library_name = kwargs.get('library_name', None)
        tape_storage = False

        region = kwargs.get('region', None)
        vendor_id = kwargs.get('vendor_id', None)
        display_vendor_id = kwargs.get('display_vendor_id', None)
        region_id = kwargs.get('region_id', None)

        if library_name:
            library_object = self._commcell_object.disk_libraries.get(library_name)
            library_type = library_object.library_properties.get('libraryType', None)
            tape_storage = True if library_type == 1 else tape_storage


        if ((ddb_ma is not None and not (isinstance(dedup_path, str) or isinstance(dedup_path, list))) or
                not (isinstance(storage_pool_name, str) or not isinstance(mountpath, str))):
            raise SDKException('Storage', '101')

        if isinstance(media_agent, MediaAgent):
            media_agent = media_agent
        elif isinstance(media_agent, str):
            media_agent = MediaAgent(self._commcell_object, media_agent)
        else:
            raise SDKException('Storage', '103')

        if (isinstance(ddb_ma, str) or isinstance(ddb_ma, MediaAgent)) and isinstance(dedup_path, str):
            ddb_ma = [ddb_ma]
            dedup_path = [dedup_path]

        if isinstance(ddb_ma, list) and isinstance(dedup_path, list):
            if len(ddb_ma) != len(dedup_path):
                raise SDKException('Storage', '101')

        if library_name is not None and mountpath != '':
            raise SDKException('Storage', '101')

        if ddb_ma is not None and (len(ddb_ma) > 6 or len(dedup_path) > 6):
            raise SDKException('Storage', '110')

        if ddb_ma is not None:
            for i in range(len(ddb_ma)):
                if isinstance(ddb_ma[i], MediaAgent):
                    ddb_ma[i] = ddb_ma[i]
                elif isinstance(ddb_ma[i], str):
                    ddb_ma[i] = MediaAgent(self._commcell_object, ddb_ma[i])
                else:
                    raise SDKException('Storage', '103')

        request_json = {
            "storagePolicyName": storage_pool_name,
            "type": "CVA_REGULAR_SP",
            "copyName": "Primary",
            "numberOfCopies": 1,
            "storage": [
                {
                    "path": mountpath,
                    "mediaAgent": {
                        "mediaAgentId": int(media_agent.media_agent_id),
                        "mediaAgentName": media_agent.media_agent_name
                    }
                }
            ],
            "storagePolicyCopyInfo": {
                "copyType": "SYNCHRONOUS",
                "isFromGui": True,
                "active": "SET_TRUE",
                "isDefault": "SET_TRUE",
                "numberOfStreamsToCombine": 1,
                "retentionRules": {
                    "retentionFlags": {
                        "enableDataAging": "SET_TRUE"
                    },
                    "retainBackupDataForDays": -1,
                    "retainBackupDataForCycles": -1,
                    "retainArchiverDataForDays": -1
                },
                "library": {
                    "libraryId": 0,
                },
                "mediaAgent": {
                    "mediaAgentId": int(media_agent.media_agent_id),
                    "mediaAgentName": media_agent.media_agent_name
                }
            }
        }

        if cloud_server_type and int(cloud_server_type) > 0:
            request_json["storage"][0]["deviceType"] = cloud_server_type

        if region_id is not None:
            request_json["storage"][0]["metallicStorageInfo"] = {
                "region": [
                    {
                        "regionId": region_id
                    }
                ],
                "storageClass": [
                    "CONTAINER_DEFAULT"
                ],
                "replication": [
                    "NONE"
                ]
            }
            request_json["region"] = {"regionId": region_id}

        if username is not None:
            request_json["storage"][0]["credentials"] = {"userName": username}

        if password is not None:
            request_json["storage"][0]["credentials"]["password"] = b64encode(password.encode()).decode()

        if credential_name is not None:
            request_json["storage"][0]["savedCredential"] = {"credentialName": credential_name}

        if library_name is not None:
            request_json["storage"] = []
            request_json["storagePolicyCopyInfo"]["library"]["libraryName"] = library_name

        if ddb_ma is not None or dedup_path is not None:
            maInfoList = []
            for ma, path in zip(ddb_ma, dedup_path):
                maInfoList.append({
                    "mediaAgent": {
                        "mediaAgentId": int(ma.media_agent_id),
                        "mediaAgentName": ma.media_agent_name
                    },
                    "subStoreList": [
                        {
                            "accessPath": {
                                "path": path
                            },
                            "diskFreeThresholdMB": 5120,
                            "diskFreeWarningThreshholdMB": 10240
                        }]
                })

            request_json["storagePolicyCopyInfo"].update({
                "storagePolicyFlags": {
                    "blockLevelDedup": "SET_TRUE",
                    "enableGlobalDeduplication": "SET_TRUE"
                },
                "dedupeFlags": {
                    "enableDeduplication": "SET_TRUE",
                    "enableDASHFull": "SET_TRUE",
                    "hostGlobalDedupStore": "SET_TRUE"
                },
                "DDBPartitionInfo": {
                    "maInfoList": maInfoList
                }
            })
        elif tape_storage:
            request_json["storagePolicyCopyInfo"].update({
                "storagePolicyFlags": {
                    "globalAuxCopyPolicy": "SET_TRUE"
                },
                "copyFlags": {
                    "preserveEncryptionModeAsInSource": "SET_TRUE"
                },
                "extendedFlags": {
                    "globalAuxCopyPolicy": "SET_TRUE"
                }
            })
        else:
            request_json["storagePolicyCopyInfo"].update({
                "storagePolicyFlags": {
                    "globalStoragePolicy": "SET_TRUE"
                },
                "copyFlags": {
                    "preserveEncryptionModeAsInSource": "SET_TRUE"
                },
                "extendedFlags": {
                    "globalStoragePolicy": "SET_TRUE"
                }
            })

        # air gap protect storage
        if cloud_server_type == 400:
            del request_json["storage"][0]["path"]
            request_json["storage"][0]["savedCredential"] = {"credentialId": 0}

            metallic_Storage = {
                "region": [
                    {
                        "regionName": region
                    }
                ],
                "displayVendorId": display_vendor_id,
                "vendorId": vendor_id
            }
            request_json["storage"][0]["metallicStorageInfo"] = metallic_Storage

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._add_storage_pool_api, request_json
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
        self._commcell_object.disk_libraries.refresh()
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

class StoragePoolType(IntEnum):
    """Class IntEnum to represent different storage pool types"""
    DEDUPLICATION = 1,
    SECONDARY_COPY = 2,
    NON_DEDUPLICATION = 3,
    SCALE_OUT = 4


class WORMLockType(IntFlag):
    """Class IntFlag to represent different WORM lock types flag values"""
    COPY = 1,  # copy level software WORM (compliance lock)
    STORAGE = 2,  # storage level hardware WORM
    OBJECT = 4,  # object level storage WORM
    BUCKET = 8  # bucket level storage WORM


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
        self._copy_id = None
        self._copy_name = None

        if storage_pool_id:
            self._storage_pool_id = str(storage_pool_id)
        else:
            self._storage_pool_id = self._commcell_object.storage_pools.get(self._storage_pool_name).storage_pool_id

        self._STORAGE_POOL = self._commcell_object._services['GET_STORAGE_POOL'] % (self.storage_pool_id)
        self.refresh()

        self._copy_id = self._storage_pool_properties.get("storagePoolDetails", {}).get("copyInfo", {}).get(
            "StoragePolicyCopy", {}).get("copyId")
        self._copy_name = self._storage_pool_properties.get("storagePoolDetails", {}).get("copyInfo", {}).get(
            "StoragePolicyCopy", {}).get("copyName")

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

    @property
    def copy_name(self):
        """Treats copy name as a read only attribute"""
        return self._copy_name

    @property
    def copy_id(self):
        """Treats copy ID as a read only attribute"""
        return self._copy_id

    @property
    def storage_pool_type(self):
        """Treats storage type as a read only attribute"""
        return self._storage_pool_properties["storagePoolDetails"]["storagePoolType"]

    @property
    def storage_type(self):
        """Treats storage type as a read only attribute"""
        return self._storage_pool_properties["storagePoolDetails"]["storageType"]

    @property
    def storage_vendor(self):
        """Treats library vendor like cloud storage provider as a read only attribute"""
        return self._storage_pool_properties["storagePoolDetails"]["libraryVendorId"]

    @property
    def is_worm_storage_lock_enabled(self):
        """Treats is worm enabled as a read only attribute"""
        return self._storage_pool_properties["storagePoolDetails"]["isWormStorage"]

    @property
    def is_object_level_worm_lock_enabled(self):
        """Treats is object WORM enabled as a read only attribute"""
        worm_flag = int(self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["wormStorageFlag"])
        return worm_flag & WORMLockType.OBJECT == WORMLockType.OBJECT

    @property
    def is_bucket_level_worm_lock_enabled(self):
        """Treats is bucket WORM enabled as a read only attribute"""
        worm_flag = int(self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["wormStorageFlag"])
        return worm_flag & WORMLockType.BUCKET == WORMLockType.BUCKET

    @property
    def is_compliance_lock_enabled(self):
        """Treats is compliance lock enabled as a read only attribute"""
        return self._storage_pool_properties["storagePoolDetails"]["copyInfo"]["copyFlags"]["wormCopy"] == 1

    def get_copy(self):
        """ Returns the StoragePolicyCopy object of Storage Pool copy"""
        return StoragePolicyCopy(self._commcell_object, self.storage_pool_name, self.copy_name)

    def enable_compliance_lock(self):
        """ Enables compliance lock on Storage Pool Copy """
        self.get_copy().enable_compliance_lock()
        self.refresh()

    def enable_worm_storage_lock(self, retain_days):
        """
        Enable storage WORM lock on storage pool

        Args:
            retain_days    (int)   -- number of days of retention on WORM copy.

        Raises:
            SDKException:
                if response is not success.

                if reponse is empty.
        """

        request_json = {
            "storagePolicyCopyInfo": {
                "copyFlags": {
                    "wormCopy": 1
                },
                "retentionRules": {
                    "retainBackupDataForDays": retain_days
                }
            },
            "isWormStorage": True,
            "forceCopyToFollowPoolRetention": True
        }

        _STORAGE_POOL_COPY = self._commcell_object._services['STORAGE_POLICY_COPY'] % (
            self._storage_pool_id, str(self.copy_id))
        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', _STORAGE_POOL_COPY, request_json)

        if flag:
            if response.json():
                response = response.json()
                if "error" in response and response.get("error", {}).get("errorCode") != 0:
                    error_message = response.get("error", {}).get("errorMessage")
                    raise SDKException('Response', '102', error_message)
                else:
                    self.refresh()
            else:
                raise SDKException('Response', '101')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
