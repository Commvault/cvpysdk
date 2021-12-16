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

"""Main file for performing operations on inventory manager app under Activate.

Inventories, Inventory, Assets & Asset are the four classes defined in this file

Inventories: class for representing all inventories in the commcell

Inventory: class for representing a single inventory in the commcell

Assets: class for representing all assets in an inventory

Asset: class to represent single asset in an inventory

Inventories:

            __init__()                          --  initialise object of the Inventories class

            _get_inventories()                  --  Gets all inventories in the commcell

             _response_not_success()            --  parses through the exception response, and raises SDKException

             refresh()                          --  refresh the Inventories from the commcell

             get_properties()                   --  returns the properties for given inventory name

             has_inventory()                    --  Checks if a given inventory name exists in the commcell or not

             get()                              --  returns the Inventory class object for given inventory name

             add()                              --  add inventory to the commcell

             delete()                           --  delete inventory from the commcell


Inventory:

            __init__()                          --  initialise object of the Inventory class

            _response_not_success()             --  parses through the exception response, and raises SDKException

            _get_inventory_properties()         --  Gets all the properties of this inventory

             _get_schedule_object()             --  returns the schedule class object associated to this inventory

            _get_data_source_handler_object()   --  returns the datasource and default handler object for this inventory

            refresh()                           --  refresh the properties of the inventory

            get_assets()                        --  returns the Assets class object for this inventory

            share()                             --  shares inventory with other user or user group

            start_collection()                  --  starts collection job on this inventory

            get_inventory_data()                --  returns data from inventory

Inventory Attributes
-----------------

    **properties**              --  returns properties of the inventory

    **index_server_name**       --  returns the index server name associated with this inventory

    **_index_server_cloud_id**  --  returns the index server cloudid associated with this inventory

    **inventory_name**          --  returns the inventory name

    **inventory_id**            --  returns the inventory id

    **security_associations**   --  returns the security associations blob of this inventory

    **schedule**                --  returns the schedule object associated with this inventory

    **data_source**             --  returns the DataSource object associated with this inventory

    **handler**                 --  returns the default handler object for this inventory

Assets:

        __init__()                          --  initialise object of the Assets class

        refresh()                           --  refresh the assets associated with inventory

        add()                               --  adds asset to the inventory

        get()                               --  returns the instance of Asset class based on given asset name

        has_asset()                         --  returns whether given asset exists or not in inventory

        delete()                            --  deletes the asset from the inventory

        _get_assets_properties()            --  returns the assets properties

         _response_not_success()            --  parses through the exception response, and raises SDKException

Assets Attributes:
----------------

    **assets**                  --  returns the assets details as json

Asset:

        __init__()                          --  initialise object of the Asset class

        _get_properties()                   --  returns the properties of the asset

        refresh()                           --  refresh the asset associated with inventory

        start_collection()                  --  starts collection job on this asset

        get_job_history()                   --  returns the job history details of this asset

        get_job_status()                    --  returns the job status details of this asset

        get_asset_prop()                    --  returns the asset property value for the given property name


Asset Attributes:
-----------------

        **asset_id**            --      returns the id of asset

        **asset_name**          --      returns the name of asset

        **asset_type**          --      returns the type of asset

        **crawl_start_time**    --      returns the last crawl start time of asset

        **asset_props**         --      returns the properties(name/value pair) of asset

        **asset_status**        --      returns the status of asset

        **inventory_id**        --      returns the inventory id of this asset


"""
import copy

from ..activateapps.ediscovery_utils import EdiscoveryClientOperations

from ..activateapps.constants import InventoryConstants
from ..schedules import Schedules
from ..exception import SDKException


class Inventories():
    """Class for representing all inventories in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the Inventories class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the Inventories class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._inventories = None
        self._API_INVENTORIES = self._services['EDISCOVERY_INVENTORIES']
        self._API_DELETE_INVENTORY = self._services['EDISCOVERY_INVENTORY']
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_inventories(self):
        """Gets all inventories from the commcell

            Args:

                None

            Return:

                list(dict)        --  list Containing inventory details dict

            Raises:

                SDKException:

                    if response is empty

                    if response is not success

        """
        output = {}
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_INVENTORIES
        )
        if flag:
            if response.json() and 'inventoryList' in response.json():
                inventories = response.json()['inventoryList']
                for inventory in inventories:
                    output[inventory['inventoryName'].lower()] = inventory
                return output
            raise SDKException('Inventory', '103')
        self._response_not_success(response)

    def add(self, inventory_name, index_server, name_server=None):
        """Adds inventory to the commcell with given inputs

                Args:

                    inventory_name              (str)       --  Name of the inventory

                    index_server                (str)       --  Index server name

                    name_server                 (list)      --  Name server assets which needs to be added to inventory

                Returns:

                    object  --  Instance of Inventory Class

                Raises:

                    SDKException:

                            if input data type is not valid

                            if failed to add inventory

                            if Index Server doesn't exists in commcell

        """
        if not isinstance(inventory_name, str) or not isinstance(index_server, str):
            raise SDKException('Inventory', '101')
        req_json = copy.deepcopy(InventoryConstants.INVENTORY_ADD_REQUEST_JSON)
        if name_server:
            asset_json = copy.deepcopy(InventoryConstants.ASSET_ADD_REQUEST_JSON)
            for server in name_server:
                asset_json['name'] = server
                req_json['assets'].append(asset_json)
        req_json['inventoryName'] = inventory_name
        if not self._commcell_object.index_servers.has(index_server):
            raise SDKException('Inventory', '102', "Given index server name not exists on this commcell")
        index_server_obj = self._commcell_object.index_servers.get(index_server)
        req_json['analyticsEngineCloud']['cloudId'] = index_server_obj.cloud_id
        req_json['analyticsEngineCloud']['cloudDisplayName'] = index_server_obj.cloud_name
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_INVENTORIES, req_json
        )
        if flag:
            if response.json() and 'errorResp' in response.json():
                err_resp = response.json()['errorResp']
                if 'errorCode' in err_resp and err_resp['errorCode'] != 0:
                    raise SDKException(
                        'Inventory',
                        '102',
                        f"Failed to create inventory with error [{err_resp['errorMessage']}]")
                elif 'inventoryList' in response.json():
                    inventory = response.json()['inventoryList'][0]
                    inventory_id = inventory['inventoryId']
                    self.refresh()
                    return Inventory(self._commcell_object, inventory_name, inventory_id)
                raise SDKException('Inventory', '102', f"Failed to create inventory with response - {response.json()}")
            raise SDKException('Inventory', '105')
        self._response_not_success(response)

    def delete(self, inventory_name):
        """Deletes the inventory from the commcell

                Args:

                    inventory_name      (str)       --  Inventory name to be deleted

                Returns:
                    None

                Raises:

                    SDKException:

                            if unable to find inventory

                            if failed to delete inventory

                            if input type is not valid

        """
        if not isinstance(inventory_name, str):
            raise SDKException('Inventory', '101')
        if not self.has_inventory(inventory_name):
            raise SDKException('Inventory', '106')
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._API_DELETE_INVENTORY % self._inventories[inventory_name.lower()]['inventoryId']
        )
        if flag:
            if response.json() and 'errorResp' in response.json():
                err_resp = response.json()['errorResp']
                if 'errorCode' in err_resp and err_resp['errorCode'] != 0:
                    raise SDKException(
                        'Inventory',
                        '102',
                        f"Failed to Delete inventory with error [{err_resp['errorMessage']}]")
                self.refresh()
            else:
                raise SDKException('Inventory', '107')
        else:
            self._response_not_success(response)

    def refresh(self):
        """Refresh the inventories associated with the commcell."""
        self._inventories = self._get_inventories()

    def get_properties(self, inventory_name):
        """Returns a properties of the specified Inventory

            Args:
                inventory_name (str)  --  name of the inventory

            Returns:
                dict -  properties for the given inventory name


        """
        return self._inventories[inventory_name.lower()]

    def has_inventory(self, inventory_name):
        """Checks if a inventory exists in the commcell with the input name.

            Args:
                inventory_name (str)  --  name of the inventory

            Returns:
                bool - boolean output to specify whether the inventory exists in the commcell or not

            Raises:
                SDKException:
                    if type of the inventory name argument is not string

        """
        if not isinstance(inventory_name, str):
            raise SDKException('Inventory', '101')

        return self._inventories and inventory_name.lower() in map(str.lower, self._inventories)

    def get(self, inventory_name):
        """Returns a Inventory object for the given inventory name.

            Args:
                inventory_name (str)  --  name of the inventory

            Returns:

                obj                 -- Object of Inventory class

            Raises:

                SDKException:

                    if inventory doesn't exists in commcell

                    if inventory_name is not of type string


        """
        if not isinstance(inventory_name, str):
            raise SDKException('Inventory', '101')

        if self.has_inventory(inventory_name):
            inventory_id = self._inventories[inventory_name.lower()]['inventoryId']
            return Inventory(self._commcell_object, inventory_name, inventory_id)
        raise SDKException('Inventory', '106')


class Inventory():
    """Class for performing operations on a single inventory"""

    def __init__(self, commcell_object, inventory_name, inventory_id=None):
        """Initialize an object of the Inventory class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                inventory_name     (str)        --  name of the Inventory

                inventory_id       (str)        --  id of Inventory
                    default: None

            Returns:
                object  -   instance of the Inventory class
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._services = commcell_object._services
        self._cvpysdk_obj = self._commcell_object._cvpysdk_object
        self._inventory_id = None
        self._inventory_name = inventory_name
        self._inventory_props = None
        self._index_server_name = None
        self._index_server_cloud_id = None
        self._security_associations = None
        self._schedule = None
        self._data_source = None
        self._handler = None
        self._API_GET_INVENTORY_DETAILS = self._services['EDISCOVERY_INVENTORY']
        self._API_SECURITY = self._services['SECURITY_ASSOCIATION']
        self._API_SECURITY_ENTITY = self._services['ENTITY_SECURITY_ASSOCIATION']
        self._API_GET_DEFAULT_HANDLER = self._services['EDISCOVERY_GET_DEFAULT_HANDLER']

        if not inventory_id:
            self._inventory_id = self._commcell_object.activate.inventory_manager().get(inventory_name).inventory_id
        else:
            self._inventory_id = inventory_id
        self.refresh()
        self._ediscovery_client_obj = EdiscoveryClientOperations(class_object=self, commcell_object=commcell_object)

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_inventory_properties(self):
        """ Get inventory properties from the commcell
                Args:

                    None

                Returns:

                    dict        --  Properties of inventory

        """
        flag, response = self._cvpysdk_obj.make_request(
            'GET', self._API_GET_INVENTORY_DETAILS % self._inventory_id
        )
        if flag:
            if response.json() and 'inventoryList' in response.json():
                inventory_props = response.json()['inventoryList'][0]
                self._index_server_name = inventory_props['analyticsEngineCloud']['cloudDisplayName']
                self._index_server_cloud_id = inventory_props['analyticsEngineCloud']['cloudId']
                self._inventory_name = inventory_props['inventoryName']
                self._security_associations = inventory_props['securityAssociation']['associations']
                return inventory_props
            raise SDKException('Inventory', '104')
        self._response_not_success(response)

    def refresh(self):
        """Refresh the inventory details for associated object"""
        self._inventory_props = self._get_inventory_properties()
        self._schedule = self._get_schedule_object()
        self._data_source, self._handler = self._get_data_source_handler_object()

    def get_assets(self):
        """Returns the Assets class instance for this inventory

                Args:

                    None

                Returns:

                    object      --  Instance of Assets class

        """
        return Assets(self._commcell_object, self.inventory_name, self.inventory_id)

    def start_collection(self):
        """Starts collection job on this inventory

                Args:

                    None

                Return:

                    None

                Raises:

                    SDKException:

                            if failed to start collection job

        """
        return self._ediscovery_client_obj.start_job()

    def share(self, user_or_group_name, allow_edit_permission=False, is_user=True, ops_type=1):
        """Shares inventory with given user or user group in commcell

                Args:

                    user_or_group_name      (str)       --  Name of user or group

                    is_user                 (bool)      --  Denotes whether this is user or group name
                                                                default : True(User)

                    allow_edit_permission   (bool)      --  whether to give edit permission or not to user or group

                    ops_type                (int)       --  Operation type

                                                            Default : 1 (Add)

                                                            Supported : 1 (Add)
                                                                        3 (Delete)

                Returns:

                    None

                Raises:

                    SDKException:

                            if unable to update security associations

                            if response is empty or not success
        """
        if not isinstance(user_or_group_name, str):
            raise SDKException('Inventory', '101')
        request_json = copy.deepcopy(InventoryConstants.INVENTORY_SHARE_REQUEST_JSON)
        external_user = False
        association_response = None
        if ops_type == 1 and len(self.security_associations) > 1:
            association_request_json = copy.deepcopy(InventoryConstants.INVENTORY_SHARE_REQUEST_JSON)
            del association_request_json['securityAssociations']
            association_request_json['entityAssociated']['entity'][0]['seaDataSourceId'] = int(self.inventory_id)
            # get security blob for this data source type entity - 132
            flag, response = self._cvpysdk_obj.make_request(
                'GET', self._API_SECURITY_ENTITY % (132, int(self.inventory_id)), association_request_json
            )
            if flag:
                if response.json() and 'securityAssociations' in response.json():
                    association_response = response.json(
                    )['securityAssociations'][0]['securityAssociations']['associations']
                else:
                    raise SDKException('Inventory', '102', 'Failed to get existing security associations')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

        if '\\' in user_or_group_name:
            external_user = True
        if is_user:
            user_obj = self._commcell_object.users.get(user_or_group_name)
            user_id = user_obj.user_id
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userId'] = int(user_id)
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = "13"
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userName'] = user_or_group_name
        elif external_user:
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['groupId'] = 0
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = "62"
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0][
                'externalGroupName'] = user_or_group_name
        else:
            grp_obj = self._commcell_object.user_groups.get(user_or_group_name)
            grp_id = grp_obj.user_group_id
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userGroupId'] = int(grp_id)
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = "15"
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0][
                'userGroupName'] = user_or_group_name

        request_json['entityAssociated']['entity'][0]['seaDataSourceId'] = self.inventory_id
        request_json['securityAssociations']['associationsOperationType'] = ops_type

        if allow_edit_permission:
            request_json['securityAssociations']['associations'][0]['properties']['categoryPermission']['categoriesPermissionList'].append(
                InventoryConstants.EDIT_CATEGORY_PERMISSION)

            # Associate existing associations to the request
        if ops_type == 1 and len(self.security_associations) > 1:
            request_json['securityAssociations']['associations'].extend(association_response)

        flag, response = self._cvpysdk_obj.make_request(
            'POST', self._API_SECURITY, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                response_json = response.json()['response'][0]
                error_code = response_json['errorCode']
                if error_code != 0:
                    error_message = response_json['errorString']
                    raise SDKException(
                        'Inventory',
                        '102', error_message)
                # update association list by refreshing inventory
                self.refresh()
            else:
                raise SDKException('Inventory', '111')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_data_source_handler_object(self):
        """returns the data source and handler object associated with this inventory

                Args:
                    None

                Returns:
                    obj,obj     --  Instance of DataSource object,Instance of Handler object

                Raises:

                    SDKException:

                            if failed to get datasource or handler details
        """
        flag, response = self._cvpysdk_obj.make_request(
            'GET', self._API_GET_DEFAULT_HANDLER % self.inventory_id)
        if flag:
            if response.json() and 'handlerInfos' in response.json():
                handler_list = response.json()['handlerInfos']
                if not isinstance(handler_list, list):
                    raise SDKException('Inventory', '102', "Failed to get Datasource/Handler details")
                handler_details = handler_list[0]
                ds_name = handler_details['dataSourceName']
                handler_name = handler_details['handlerName']
                ds_obj = self._commcell_object.datacube.datasources.get(ds_name)
                handler_obj = ds_obj.ds_handlers.get(handler_name)
                return ds_obj, handler_obj
            raise SDKException('Inventory', '102', 'Unknown response while fetching datasource details')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _get_schedule_object(self):
        """Returns the schedule class object of schedule associated to this inventory

                Args:

                    None

                Returns:

                    object      --  Instance of Schedule class

                Raises:

                    SDKException:

                            if failed to find schedule
        """
        return Schedules(self).get()

    def get_inventory_data(self, handler_filter=""):
        """ Executes handler for fetching data from inventory
                Args:

                     handler_filter    (str)  -- Filter which needs to applied for handler execution

                Returns:

                    dict        --  Dictionary of values fetched from handler execution

                Raises:

                    SDKExpception:

                        if error in fetching handler data

                        if input is not valid
        """
        if not isinstance(handler_filter, str):
            raise SDKException('Inventory', '101')
        if not self._handler:
            raise SDKException('Inventory', '102', 'No handler object initialised')
        return self._handler.get_handler_data(handler_filter=handler_filter)

    @property
    def properties(self):
        """Returns the properties of this inventory as dict"""
        return self._inventory_props

    @property
    def index_server_name(self):
        """Returns the index server name associated with this inventory"""
        return self._index_server_name

    @property
    def index_server_cloud_id(self):
        """Returns the index server id associated with this inventory"""
        return self._index_server_cloud_id

    @property
    def inventory_id(self):
        """Returns the inventory id associated with this inventory"""
        return self._inventory_id

    @property
    def inventory_name(self):
        """Returns the inventory name associated with this inventory"""
        return self._inventory_name

    @property
    def security_associations(self):
        """Returns the security blob associated with this inventory"""
        return self._security_associations

    @property
    def schedule(self):
        """Returns the schedule class object for schedule associated with this inventory"""
        return self._schedule

    @property
    def data_source(self):
        """Returns the DataSource class object for datasource associated with this inventory"""
        return self._data_source

    @property
    def handler(self):
        """Returns the Handler class object for default handler associated with this inventory"""
        return self._handler


class Assets():
    """Class to represent all assets in an inventory"""

    def __init__(self, commcell_object, inventory_name, inventory_id=None):
        """Initialize an object of the Assets class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                inventory_name     (str)        --  name of the Inventory

                inventory_id       (str)        --  id of Inventory
                    default: None

            Returns:
                object  -   instance of the Assets class
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._services = commcell_object._services
        self._cvpysdk_obj = self._commcell_object._cvpysdk_object
        self._inventory_id = None
        self._inventory_name = inventory_name
        if not inventory_id:
            self._inventory_id = self._commcell_object.activate.inventory_manager().get(inventory_name).inventory_id
        else:
            self._inventory_id = inventory_id
        self._assets = None
        self._API_INVENTORIES = self._services['EDISCOVERY_INVENTORIES']
        self._API_ASSETS = self._services['EDISCOVERY_ASSETS']
        self.refresh()

    def _get_assets_properties(self):
        """gets the assets properties from inventory

                    Args:
                        None

                    Returns:

                        dict    --  containing asset properties

        """
        inv_mgr = self._commcell_object.activate.inventory_manager()
        inv_obj = inv_mgr.get(self._inventory_name)
        inv_obj.refresh()
        assets = {}
        for asset in inv_obj.properties['assets']:
            name = asset['name'].lower()
            assets[name] = asset
        return assets

    def refresh(self):
        """Refresh the assets details associated with this inventory"""
        self._assets = self._get_assets_properties()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def has_asset(self, asset_name):
        """Checks whether given asset exists in inventory or not

                        Args:

                            asset_name      (str)       --  Name of the asset

                        Returns:

                            bool      --  true if asset exists else false
        """
        return self._assets and asset_name.lower() in self._assets

    def get(self, asset_name):
        """Returns the asset object

                Args:

                    asset_name      (str)       --  Name of the asset

                Returns:

                    object      -- Instance of Asset class

                Raises:

                    SDKException:

                            if input is not valid

                            if asset doesn't exists in inventory
        """
        if not isinstance(asset_name, str):
            raise SDKException('Inventory', '101')
        if not self.has_asset(asset_name):
            raise SDKException('Inventory', '109')
        return Asset(self._commcell_object, self._inventory_name, asset_name, self._inventory_id)

    def add(self, asset_name, asset_type=InventoryConstants.AssetType.NAME_SERVER, **kwargs):
        """Adds asset to the inventory

                Args:

                    asset_name          (str)       --  Name of the asset

                    asset_type          (Enum)      --  type of asset (Refer to InventoryConstants.AssetType class)

                    kwargs for FILE SERVER type Asset:

                            fqdn                --  File server FQDN

                            os                  --  File Server OS type

                            ip                  --  File server IP

                            country_code        --  Country code (ISO 3166 2-letter code)

                            country_name        --  Country name

                            domain              --  File Server Domain name(optional)

                Returns:

                    object  --  Instance of Asset class

                Raises:

                    SDKException:

                            if input is not valid

                            if failed to add asset to inventory

        """
        if not isinstance(asset_name, str) or not isinstance(asset_type, InventoryConstants.AssetType):
            raise SDKException('Inventory', '101')
        request_json = copy.deepcopy(InventoryConstants.ASSET_ADD_TO_INVENTORY_JSON)
        request_json['inventoryId'] = int(self._inventory_id)
        asset_json = copy.deepcopy(InventoryConstants.ASSET_ADD_REQUEST_JSON)
        asset_json['name'] = asset_name
        asset_json['type'] = asset_type.value
        property_json = copy.deepcopy(InventoryConstants.ASSET_PROPERTY_JSON)
        if asset_type.value == InventoryConstants.AssetType.FILE_SERVER.value:
            for prop in InventoryConstants.ASSET_FILE_SERVER_PROPERTY:
                prop_name = InventoryConstants.FIELD_PROPS_MAPPING[prop]
                default_value = ""
                if prop_name not in kwargs:
                    # if domain is not passed, then form domain from fqdn
                    if prop == InventoryConstants.FIELD_PROPERTY_DOMAIN:
                        default_value = kwargs.get(InventoryConstants.KWARGS_FQDN)
                        default_value = default_value.split(".", 1)[1]
                    # always use asset name as file server name
                    if prop == InventoryConstants.FIELD_PROPERTY_NAME:
                        default_value = asset_name
                prop_json = copy.deepcopy(InventoryConstants.ASSET_PROPERTY_NAME_VALUE_PAIR_JSON)
                prop_json['name'] = prop
                prop_json['value'] = kwargs.get(prop_name, default_value)
                property_json['propertyValues']['nameValues'].append(prop_json)
            asset_json.update(property_json)
        request_json['assets'].append(asset_json)
        flag, response = self._cvpysdk_obj.make_request(
            'PUT', self._API_INVENTORIES, request_json)
        if flag:
            if response.json() and 'errorResp' in response.json():
                err_resp = response.json()['errorResp']
                if 'errorCode' in err_resp and err_resp['errorCode'] != 0:
                    raise SDKException(
                        'Inventory',
                        '102',
                        f"Failed to add asset to inventory with error [{err_resp['errorMessage']}]")
                self.refresh()
                return Asset(self._commcell_object, self._inventory_name, asset_name, self._inventory_id)
            raise SDKException('Inventory', '108')
        self._response_not_success(response)

    def delete(self, asset_name):
        """Delete the asset from the inventory

                Args:

                    asset_name      (str)       --  Name of the asset

                Returns:

                    None

                Raises:

                    SDKException:

                            if input is not valid

                            if failed to delete the asset

                            if unable to find this asset in inventory
        """
        if not isinstance(asset_name, str):
            raise SDKException('Inventory', '101')
        if not self.has_asset(asset_name):
            raise SDKException('Inventory', '109')
        request_json = copy.deepcopy(InventoryConstants.ASSET_DELETE_FROM_INVENTORY_JSON)
        request_json['inventoryId'] = int(self._inventory_id)
        if 'assetId' in self._assets[asset_name.lower()]:
            request_json['assets'].append({'assetId': self._assets[asset_name.lower()]['assetId']})
        else:
            req = copy.deepcopy(InventoryConstants.ASSET_ADD_REQUEST_JSON)
            asset_obj = self.get(asset_name)
            asset_type = asset_obj.asset_type
            # for file server asset, asset name will not be display name in backend delete request. so fetch fqdn
            req['name'] = asset_obj.get_asset_prop(prop_name=InventoryConstants.FIELD_PROPERTY_DNSHOST)
            req['type'] = asset_type
            request_json['assets'].append(req)
        flag, response = self._cvpysdk_obj.make_request(
            'PUT', self._API_ASSETS % self._inventory_id, request_json)
        if flag:
            if response.json():
                err_resp = response.json()['errorResp']
                if 'errorCode' in err_resp and err_resp['errorCode'] != 0:
                    raise SDKException(
                        'Inventory',
                        '102',
                        f"Failed to delete asset from inventory with error [{err_resp['errorMessage']}]")
                self.refresh()
                return
            raise SDKException('Inventory', '110')
        self._response_not_success(response)

    @property
    def assets(self):
        """Returns the assets details associated with this inventory"""
        return self._assets


class Asset():
    """Class to represent single asset in an inventory"""

    def __init__(self, commcell_object, inventory_name, asset_name, inventory_id=None):
        """Initialize an object of the Asset class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                inventory_name     (str)        --  name of the Inventory

                asset_name          (str)       --  Name of the asset

                inventory_id       (str)        --  id of Inventory
                    default: None

            Returns:
                object  -   instance of the Asset class
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._services = commcell_object._services
        self._cvpysdk_obj = self._commcell_object._cvpysdk_object
        self._inventory_id = None
        self._inventory_name = inventory_name
        if not inventory_id:
            self._inventory_id = self._commcell_object.activate.inventory_manager().get(inventory_name).inventory_id
        else:
            self._inventory_id = inventory_id
        self._asset_name = asset_name
        self._asset_props = None
        self._asset_id = None
        self._crawl_start_time = None
        self._asset_type = None
        self._asset_status = None
        self._asset_name_values_props = None
        self.refresh()
        self._ediscovery_client_obj = EdiscoveryClientOperations(class_object=self, commcell_object=commcell_object)

    def _get_properties(self):
        """Returns the properties of this asset

                Args:

                    None

                Returns:

                    dict        -- Containing properties of asset

        """
        inv_mgr = self._commcell_object.activate.inventory_manager()
        inv_obj = inv_mgr.get(self._inventory_name)
        inv_obj.get_assets().refresh()
        for asset in inv_obj.properties['assets']:
            if asset['name'].lower() == self._asset_name.lower():
                # for file server, we will not have asset id & crawl times
                self._asset_id = asset.get('assetId', 0)
                self._crawl_start_time = asset.get('crawlStartTime', 0)
                self._asset_type = asset.get('type', 0)
                self._asset_status = asset['status']
                self._asset_name = asset['name']
                self._asset_name_values_props = asset['propertyValues']['nameValues']
                return asset
        return {}

    def refresh(self):
        """Refresh the asset details associated with this"""
        self._asset_props = self._get_properties()

    def get_job_history(self):
        """Returns the job history details of this asset

                Args:
                    None

                Returns:

                    list(dict)    --  containing job history details

                Raises:

                    SDKException:

                            if failed to get job history

                            if asset is not supported for this operation

        """
        if self.asset_type != InventoryConstants.AssetType.NAME_SERVER.value:
            raise SDKException('Inventory', '102', "Not supported other than Name Server asset type")
        return self._ediscovery_client_obj.get_job_history()

    def get_job_status(self):
        """Returns the job status details of this asset

                Args:
                    None

                Returns:

                    dict    --  containing job status details

                Raises:

                    SDKException:

                            if failed to get job status

                             if asset is not supported for this operation

        """
        if self.asset_type != InventoryConstants.AssetType.NAME_SERVER.value:
            raise SDKException('Inventory', '102', "Not supported other than Name Server asset type")
        return self._ediscovery_client_obj.get_job_status()

    def start_collection(self, wait_for_job=False, wait_time=60):
        """Starts collection job on this asset

                Args:

                    wait_for_job        (bool)      --  specifies whether to wait for job to complete or not

                    wait_time           (int)       --  time interval to wait for job completion in Mins
                                                            Default : 60Mins

                Return:

                    None

                Raises:

                    SDKException:

                            if failed to start collection job

                            if asset is not supported for this operation

        """
        if self.asset_type != InventoryConstants.AssetType.NAME_SERVER.value:
            raise SDKException('Inventory', '102', "Not supported other than Name Server asset type")
        return self._ediscovery_client_obj.start_job(wait_for_job=wait_for_job, wait_time=wait_time)

    def get_asset_prop(self, prop_name):
        """returns the property value for given property name for this asset

            Args:

                prop_name       (str)       --  Name of the property

            Returns:

                str     --  Value of the property


        """
        for prop in self._asset_name_values_props:
            name = prop['name']
            if name == prop_name:
                return prop['value']
        return ""

    @property
    def asset_id(self):
        """Returns the asset id with this asset"""
        return self._asset_id

    @property
    def asset_name(self):
        """Returns the asset name with this asset"""
        return self._asset_name

    @property
    def crawl_start_time(self):
        """Returns the crawl start time with this asset"""
        return self._crawl_start_time

    @property
    def asset_type(self):
        """Returns the asset type for this asset"""
        return self._asset_type

    @property
    def asset_status(self):
        """Returns the asset status for this asset"""
        return self._asset_status

    @property
    def asset_props(self):
        """Returns the property values for this asset"""
        return self._asset_name_values_props

    @property
    def inventory_id(self):
        """Returns the inventory id for this asset"""
        return self._inventory_id
