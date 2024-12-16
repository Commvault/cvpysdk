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

"""Main file for performing resource pool related operations on CS

ResourcePools , ResourcePool and ResourcePoolTypes are the classes defined in this file

ResourcePools:

        __init__()                          --  initialise object of the ResourcePools class

        _response_not_success()             --  parses through the exception response, and raises SDKException

        _get_resource_pools()               --  returns resource pools details from CS

        has()                               --  Checks whether given resource pool exists in cs or not

        get()                               -- returns ResourcePool object for given name

        delete()                            --  deletes the resource pool from CS

        create()                            --  creates resource pool in CS

        refresh()                           --  Refreshes resource pools associated with cs

ResourcePool:

        __init__()                          --  initialise object of the ResourcePool class

        _response_not_success()             --  parses through the exception response, and raises SDKException

        _get_pool_details()                 --  returns resource pool details from cs

        refresh()                           --  refreshes resource pool details

ResourcePool Attributes:
----------------------------------

    **resource_pool_id**        --  returns Resource pool id

    **resource_pool_type**      --  returns ResourcePoolTypes enum

"""

from .exception import SDKException

import enum


class ResourcePoolTypes(enum.Enum):
    """Enum class for different resource pool types"""
    GENERIC = 0
    O365 = 1
    SALESFORCE = 2
    EXCHANGE = 3
    SHAREPOINT = 4
    ONEDRIVE = 5
    TEAMS = 6
    DYNAMICS_365 = 7
    VSA = 8
    FILESYSTEM = 9
    KUBERNETES = 10
    AZURE_AD = 11
    CLOUD_LAPTOP = 12
    FILE_STORAGE_OPTIMIZATION = 13
    DATA_GOVERNANCE = 14
    E_DISCOVERY = 15
    CLOUD_DB = 16
    OBJECT_STORAGE = 17
    GMAIL = 18
    GOOGLE_DRIVE = 19
    GOOGLE_WORKSPACE = 20
    SERVICENOW = 21
    THREATSCAN = 22
    DEVOPS = 23
    RISK_ANALYSIS = 24
    GOOGLE_CLOUD_PLATFORM = 50001


class ResourcePools():
    """class to represent all pool in resource pool"""

    def __init__(self, commcell_object):
        """Initializes an instance of the ResourcePools class.

            Args:

                commcell_object     (object)    --  instance of the commcell class

            Returns:

                object  -   instance of the ResourcePools class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._API_GET_ALL_RESOURCE_POOLS = self._services['GET_RESOURCE_POOLS']
        self._API_DELETE_RESOURCE_POOL = self._services['DELETE_RESOURCE_POOL']
        self._API_CREATE_RESOURCE_POOL = self._services['CREATE_RESOURCE_POOL']
        self._pools = {}
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_resource_pools(self) -> dict:
        """returns resource pools details from CS

                Args:

                    None

                Returns:

                    dict       --  Resource pool details

                Raises:

                    SDKException:

                        if failed to get resource pool details

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_GET_ALL_RESOURCE_POOLS)
        output = {}
        if flag:
            if response.json() and 'resourcePools' in response.json():
                _resourcepools = response.json()['resourcePools']
                for _pool in _resourcepools:
                    if 'name' in _pool:
                        output.update({_pool['name'].lower(): _pool})
            elif bool(response.json()):
                raise SDKException('ResourcePools', '103')
            return output
        self._response_not_success(response)

    def create(self, name: str, resource_type, **kwargs):
        """creates resource pool in CS

            Args:

                name    (str)           --  Resource pool name

                resource_type   (enum)  --  ResourcePoolTypes enum

            kwargs options:

                for Threat Scan -

                    index_server    (str)   --  index server name

            Returns:

                obj --  Instance of ResourcePool class

            Raises:

                SDKException:

                    if failed to create resource pool

                    if resource pool already exists

        """
        if resource_type.value not in [ResourcePoolTypes.THREATSCAN.value]:
            raise SDKException('ResourcePools', '102', 'Resource pool creation is not supported for this resource type')
        if resource_type.value == ResourcePoolTypes.THREATSCAN.value and 'index_server' not in kwargs:
            raise SDKException('ResourcePools', '102', 'Index server name is missing in kwargs')
        if self.has(name=name):
            raise SDKException('ResourcePools', '107')
        _request_json = {
            "resourcePool": {
                "appType": resource_type.value,
                "dataAccessNodes": [],
                "extendedProp": {
                    "exchangeOnePassClientProperties": {}},
                "resourcePool": {
                    "resourcePoolId": 0,
                    "resourcePoolName": name},
                "exchangeServerProps": {
                    "jobResultsDirCredentials": {
                        "userName": ""},
                    "jobResultsDirPath": ""},
                "roleId": None,
                "indexServerMembers": [],
                "indexServer": {
                    "clientId": self._commcell_object.index_servers.get(
                        kwargs.get('index_server')).index_server_client_id if resource_type.value == ResourcePoolTypes.THREATSCAN.value else 0,
                    "clientName": kwargs.get('index_server') if resource_type.value == ResourcePoolTypes.THREATSCAN.value else '',
                    "displayName": kwargs.get('index_server') if resource_type.value == ResourcePoolTypes.THREATSCAN.value else '',
                    "selected": True},
                "accessNodes": {
                    "clientGroups": [],
                    "clients": []}}}
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_CREATE_RESOURCE_POOL, _request_json)
        if flag:
            if response.json() and 'error' in response.json():
                _error = response.json()['error']
                if _error.get('errorCode', 0) != 0:
                    raise SDKException('ResourcePools', '102', f'Resource pool creation failed with {_error}')
                self.refresh()
                return self.get(name=name)
            raise SDKException('ResourcePools', '108')
        self._response_not_success(response)

    def delete(self, name: str):
        """deletes the resource pool from CS

            Args:

                name   (str)       --   Resource pool name

            Returns:

                None

            Raises:

                SDKException:

                    if failed to delete resource pool

                    if failed to find resource pool
        """
        if not self.has(name=name):
            raise SDKException('ResourcePools', '104')
        api = self._API_DELETE_RESOURCE_POOL % (self._pools[name.lower()]['id'])
        flag, response = self._cvpysdk_object.make_request('DELETE', api)
        if flag:
            if response.json() and 'error' in response.json():
                _error = response.json()['error']
                if _error.get('errorCode', 0) != 0:
                    raise SDKException('ResourcePools', '102', f'Resource pool deletion failed with {_error}')
                self.refresh()
                return
            raise SDKException('ResourcePools', '106')
        self._response_not_success(response)

    def get(self, name: str):
        """returns ResourcePool object for given name

            Args:

                Name    (str)       -- Resource Pool name

            Returns:

                obj     -- Instance of ResourcePool class

            Raises:

                SDKException:

                    if failed to find resource pool with given name

        """
        if not self.has(name):
            raise SDKException('ResourcePools', '104')
        return ResourcePool(commcell_object=self._commcell_object, name=name, pool_id=self._pools[name.lower()]['id'])

    def has(self, name: str) -> bool:
        """Checks whether given resource pool exists in cs or not

            Args:

                name        (str)       -- Resource pool name

            Returns:

               bool    --  True if resource pool exists in cs
        """
        if name.lower() in self._pools:
            return True
        return False

    def refresh(self):
        """Refresh the resource pools associated with CS"""
        self._pools = {}
        self._pools = self._get_resource_pools()


class ResourcePool:

    def __init__(self, commcell_object, name, pool_id):
        """Initializes an instance of the ResourcePool class.

            Args:

                commcell_object     (object)    --  instance of the commcell class

                server_name         (str)       --  Name of the resurce pool

                pool_id             (str)       --  Resource pool id


            Returns:

                object  -   instance of the ResourcePool class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._resource_pool_name = name
        self._resource_pool_id = pool_id
        self._resource_details = None
        self._API_GET_POOL_DETAILS = self._services['GET_RESOURCE_POOL_DETAILS']
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_pool_details(self) -> dict:
        """returns resource pool details from CS

            Args:

                None

            Returns:

                dict        - Resource pool details

            Raises:

                SDKException:

                    if failed to get details for resource pool
        """
        api = self._API_GET_POOL_DETAILS % (self._resource_pool_id)
        flag, response = self._cvpysdk_object.make_request('GET', api)
        if flag:
            if response.json() and 'resourcePool' in response.json():
                return response.json()['resourcePool']
            raise SDKException('ResourcePools', '105')
        self._response_not_success(response)

    def refresh(self):
        """Refresh the resource pool details"""
        self._resource_details = None
        self._resource_details = self._get_pool_details()

    @property
    def resource_pool_id(self):
        """returns the pool id for this resource pool

            Returns:

                int --  resource pool id

        """
        return int(self._resource_details['resourcePool'].get('resourcePoolId'))

    @property
    def resource_pool_type(self):
        """returns the pool type enum for this resource pool

            Returns:

                enum --  ResourcePoolTypes

        """
        return ResourcePoolTypes(int(self._resource_details['appType']))
