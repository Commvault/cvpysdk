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

""" File for associating Workload and Backup destination regions for various entites
class: Regions. Region

Regions:
========
    _get_regions()                  --  Gets all the regions created in commcell
    refresh()                       --  Refresh the list of Regions associated to commcell
    has_region()                    --  Checks if region with given name exists
    get()                           --  returns Region class object for the specified input name
    set_region()                    --  Associate a region to an entity
    get_region()                    --  Gets the Region associated to an Entity
    calculate_region()              --  Calculates the Region to be associated to an Entity
    add()                           --  Method to add a region
    delete()                        --  Method to delete regions

Attributes:

    ***all_regions***               --  returns dict of details about region such as id

Region:
=======
    _get_region_id()                --  Returns the region id
    _get_region_properties()        --  Gets the properties of this region
    refresh()                       --  Refresh the properties of the regions

Attributes:
    ***region_id***                 --  Id of the given Region
    ***region_name***               --  Name of the given region
    ***region_type***               --  type of the given region
    ***locations***                 --  locations of the given region
    ***associated_servers_count***  --  associated servers count of the given region
    ***associated_servers***        --  associated servers of the given region
    ***associated_plans_count***    --  associated plans count of the given region
    ***associated_plans***          --  associated plan of the given region

"""
from typing import TYPE_CHECKING
from .exception import SDKException

if TYPE_CHECKING:
    from .commcell import Commcell


class Regions:
    """
    Class for representing all the Regions created in the commcell.

    Attributes:
        _commcell_object (Commcell): Instance of the Commcell class.
        _cvpysdk_object (CVPySDK): Instance of the CVPySDK class.
        _update_response_ (method): Method to update the response.
        _regions_api (str): API endpoint for regions.
        _EDIT_REGION (str): API endpoint for editing a region.
        _GET_REGION (str): API endpoint for getting a region.
        _CALCULATE_REGION (str): API endpoint for calculating a region.
        _regions (dict): Dictionary of regions.

    Usage:
        regions = Regions(commcell_object)
    """
    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialises the object of Regions class."""
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._update_response_ = commcell_object._update_response_
        self._regions_api = self._commcell_object._services['REGIONS']
        self._EDIT_REGION = self._commcell_object._services['EDIT_REGION']
        self._GET_REGION = self._commcell_object._services['GET_REGION']
        self._CALCULATE_REGION = self._commcell_object._services['CALCULATE_REGION']
        self._regions = None
        self.refresh()

    def _get_regions(self) -> dict:
        """
        Gets all the regions created in commcell.

        Returns:
            dict: Dictionary of regions with region name as key and region id as value.

        Raises:
            SDKException:
                - If response is not success.
                - If response json is empty.
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._regions_api)
        if flag:
            regions = {}
            if response.json() and 'regions' in response.json():

                name_count = {}

                for region in response.json()['regions']:
                    temp_name = region['name'].lower()
                    temp_company = region.get('company', {}).get('name', '').lower()

                    if temp_name in name_count:
                        name_count[temp_name].add(temp_company)
                    else:
                        name_count[temp_name] = {temp_company}

                for region in response.json()['regions']:
                    temp_name = region['name'].lower()
                    temp_id = region['id']
                    temp_company = region.get('company', {}).get('name', '').lower()

                    if len(name_count[temp_name]) > 1:
                        unique_key = f"{temp_name}_({temp_company})"
                    else:
                        unique_key = temp_name
                    regions[unique_key] = temp_id

                return regions

            raise SDKException('Response', '102')

        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Refresh the list of Regions associated to commcell."""
        self._regions = self._get_regions()

    def has_region(self, name: str) -> bool:
        """Checks if the given Region exists in the Commcell.

        Args:
            name (str): name of the Region

        Returns:
            bool: boolean output whether the Region exists in the commcell or not

        Raises:
            SDKException:
                if type of the Region name argument is not string

        Usage:
            regions.has_region('region_name')
        """
        if not isinstance(name, str):
            raise SDKException('Region', '103')

        return self._regions and (name.lower() in self._regions)

    def get(self, name: str) -> 'Region':
        """
        Returns the instance of Region class for the given Region name.

        Args:
            name (str): name of the Region

        Returns:
            object: Instance of Region class for the given Region name

        Raises:
            SDKException:
                - If the Region name argument is not a string
                - If No Region found in commcell with the given region name

        Usage:
            region = regions.get('region_name')
        """
        if not isinstance(name, str):
            raise SDKException('Region', '102', "Invalid input received")

        if not self.has_region(name):
            raise SDKException('Region', '102', f"Region {name.lower()} not present in commcell")

        return Region(self._commcell_object, name, self._regions[name.lower()])

    def set_region(self, entity_type: str, entity_id: int, entity_region_type: str, region_id: int) -> None:
        """
        Associate a region to an entity.

        Args:
            entity_type         (str): Type of the entity
                                        (eg:    COMMCELL,
                                                COMPANY,
                                                CLIENT,
                                                CLIENT_GROUP,
                                                MEDIAAGENT,
                                                STORAGE_POOL, etc
                                        )
            entity_id           (int): unique id of the entity
            entity_region_type  (str): Type of the region
                                        (WORKLOAD or BACKUP)
            region_id           (int): ID of the region from app_regions

        Raises:
            SDKException:
                - If the API returns an error.

        Usage:
            regions.set_region('CLIENT', 123, 'WORKLOAD', 456)
        """
        if isinstance(region_id,str):
            region_id = int(region_id)
        request = {
            "entityRegionType": entity_region_type,
            "region":
                {
                    "id": region_id
                }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._EDIT_REGION % (entity_type, entity_id), request
        )

        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code != 0:
                    if error_code == 50000:
                        raise SDKException('Regions', '101')
                    elif error_code == 547:
                        raise SDKException('Regions', '102', 'Invalid regionID provided in request')
                    else:
                        error_string = response.json()['errorMessage']
                        raise SDKException('Regions', '102', '{0}'.format(error_string))

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_region(self, entity_type: str, entity_id: int, entity_region_type: str) -> int:
        """
        Gets the Region associated to an Entity.

        Args:
            entity_type         (str): Type of the entity
                                        (eg:    COMMCELL,
                                                COMPANY,
                                                CLIENT,
                                                CLIENT_GROUP,
                                                MEDIAAGENT,
                                                STORAGE_POOL, etc
                                        )
            entity_id           (int): unique id of the entity
            entity_region_type  (str): Type of the region
                                        (WORKLOAD or BACKUP)

        Returns:
            int: The region ID associated with the entity. Returns 0 if no region is associated.

        Raises:
            SDKException:
                - If the API returns an error.

        Usage:
            region_id = regions.get_region('CLIENT', 123, 'WORKLOAD')
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._GET_REGION % (entity_type, entity_id, entity_region_type)
        )

        if flag:
            if response.json():
                try:
                    if response.json()['errorCode']:
                        error_string = response.json()['errorMessage']
                        raise SDKException('Regions', '102', '{0}'.format(error_string))

                except:
                    if response.json().get('regionId'):
                        return response.json().get('regionId')
                    return 0

            else:
                return None
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def calculate_region(self, entity_type: str, entity_id: int, entity_region_type: str) -> int:
        """
        Calculates the Region to be associated to an Entity.

        Args:
            entity_type         (str): Type of the entity
                                        (eg:    COMMCELL,
                                                COMPANY,
                                                CLIENT,
                                                CLIENT_GROUP,
                                                MEDIAAGENT,
                                                STORAGE_POOL, etc
                                        )
            entity_id           (int): unique id of the entity
            entity_region_type  (str): Type of the region
                                        (WORKLOAD or BACKUP)

        Returns:
            int: The calculated region ID.

        Raises:
            SDKException:
                - If the API returns an error.

        Usage:
            region_id = regions.calculate_region('CLIENT', 123, 'WORKLOAD')
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._CALCULATE_REGION % (entity_type, entity_id, entity_region_type)
        )

        if flag:
            if response.json():
                try:
                    if response.json()['errorCode']:
                        error_string = response.json()['errorMessage']
                        raise SDKException('Regions', '102', '{0}'.format(error_string))

                except:
                    return response.json()['regionId']

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add(self, region_name: str, region_type: str, locations: list) -> 'Region':
        """
        Method to add a region.

        Args:
            region_name (str): name of the region
            region_type (str): type of region
            locations   (list): list of dictionaries containing details of a location
                                e.g. locations = [{"city":"city1",
                                                    "state":"stateOfCity1",
                                                    "country":"countryOfCity1",
                                                    "latitude":"latitudeOfCity1",
                                                    "longitude":"longitudeOfCity1"},
                                                    {"city":"city2",
                                                    "state":"stateOfCity2",
                                                    "country":"countryOfCity2",
                                                    "latitude":"latitudeOfCity2",
                                                    "longitude":"longitudeOfCity2"}]

        Returns:
            object: instance of the region class created by this method

        Raises:
            SDKException:
                - if input parameters are incorrect
                - if Plan already exists
                - if invalid region type is passed

        Usage:
            locations = [{"city":"city1", "state":"stateOfCity1", "country":"countryOfCity1", "latitude":"latitudeOfCity1", "longitude":"longitudeOfCity1"}]
            region = regions.add('region_name', 'USER_CREATED', locations)
        """
        valid_region_types = ['USER_CREATED', 'OCI', 'AWS', 'AZURE', 'GCP']

        if not (isinstance(region_name, str) and isinstance(region_type, str) and isinstance(locations, list)):
            raise SDKException('Region', '101')

        elif self.has_region(region_name):
            raise SDKException('Region', '102', 'Region "{0}" already exists'.format(region_name))

        elif region_type.upper() not in valid_region_types:
            raise SDKException('Region', '102', 'Invalid region type')

        request_json = {
            "name": region_name,
            "type": region_type,
            "locations": locations
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._regions_api, request_json)

        if flag:
            if response.json():
                response_value = response.json()
                error_message = response_value.get('errorMessage')
                error_code = response_value.get('errorCode', 0)

                if error_code != 0:
                    raise SDKException('Region', '102', f'Failed to create new Region\nError: "{error_message}"')

                region_name = response_value['name']

                self.refresh()

                return self.get(region_name)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def delete(self, region_name: str) -> None:
        """
        Method to delete regions.

        Args:
            region_name (str): name of the region

        Raises:
            SDKException:
                - if type of the Region name argument is not string
                - if no region exists with the given name
                - if response is empty
                - if failed to delete the region

        Usage:
            regions.delete('region_name')
        """
        if not isinstance(region_name, str):
            raise SDKException('Region', '101')

        else:
            region_name = region_name.lower()

            if not self.has_region(region_name):
                raise SDKException('Region', '102', 'No Region exists with name: "{0}"'.format(region_name))

            region_id = self._regions[region_name]
            delete_region_service = self._commcell_object._services['REGION']%(region_id)
            flag, response = self._cvpysdk_object.make_request('DELETE', delete_region_service)

            if not flag:
                response_string = self._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
            if not response.json():
                raise SDKException('Response', '102' 'Empty response received from server.')
            response_json = response.json()
            error_code = str(response_json.get('errorCode'))
            error_message = response_json.get('errorMessage')

            if error_code == '0':
                self.refresh()
            else:
                raise SDKException('Region', '102', f'Failed to delete region. Error: {error_message}')

    @property
    def all_regions(self) -> dict:
        """Returns dict consisting of all regions details such as id."""
        return self._regions

class Region:
    """ Class for performing operations on a given Region

    Attributes:
        _commcell_object (object): Instance of the Commcell class.
        _region_name (str): Name of the region.
        _cvpysdk_object (object): Instance of the cvpysdk class.
        _update_response_ (method): Method to update the response.
        _region_id (str): ID of the region.
        _region_api (str): API endpoint for the region.
        _region_type (str): Type of the region.
        _locations (list): List of locations associated with the region.
        _associated_servers_count (int): Count of servers associated with the region.
        _associated_servers (list): List of servers associated with the region.
        _associated_plans_count (int): Count of plans associated with the region.
        _associated_plans (list): List of plans associated with the region.
        _region_properties (dict): Properties of the region.

    Usage:
        region = Region(commcell_object, 'Region1')
    """
    def __init__(self, commcell_object: 'Commcell', region_name: str, region_id: int = None) -> None:
        """ Initialise the Region class instance.
            Args:
                commcell_object     (object)    --  instance of the Commcell class

                region_name         (str)       --  name of the region

                region_id           (int)       --  ID of the REgion
                                                    Default : None

            Returns:
                object  -   instance of the Region class
        """
        self._commcell_object = commcell_object
        self._region_name = region_name
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._update_response_ = commcell_object._update_response_

        self._region_name = region_name

        if region_id:
            self._region_id = str(region_id)
        else:
            self._region_id = self._get_region_id()

        self._region_api = self._commcell_object._services['REGION'] % (self._region_id)
        self._region_type = None
        self._locations = []
        self._associated_servers_count = None
        self._associated_servers = []
        self._associated_plans_count = None
        self._associated_plans = []
        self.refresh()
        self._region_properties = None

    def _get_region_id(self) -> str:
        """ Returns the ID of the Region

        Returns:
            str: ID of the region
        """
        regions = Regions(self._commcell_object)
        return regions.get(self._region_name).region_id

    def _get_region_properties(self) -> None:
        """Gets the properties of this region"""
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._region_api)

        if flag:
            if response.json():
                properties = response.json()
                self._region_id = properties.get('id')
                self._region_name = properties.get('name')
                self._region_type = properties.get('regionType')
                if 'locations' in properties:
                    self._locations = properties.get('locations')
                if 'associatedServers' in properties:
                    self._associated_servers_count = properties.get('associatedServers', {}).get('serversCount')
                    if 'servers' in properties.get('associatedServers'):
                        self._associated_servers = properties.get('associatedServers', {}).get('servers')
                if 'associatedRegionBasedPlans' in properties:
                    self._associated_plans_count = properties.get('associatedRegionBasedPlans', {}).get('plansCount')
                    if 'plans' in properties.get('associatedRegionBasedPlans'):
                        for plan in properties.get('associatedRegionBasedPlans', {}).get('plans'):
                            self._associated_plans.append(plan.get('plan'))
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def region_id(self) -> int:
        """
        Get Region ID

        Returns:
            int -- region ID
        """
        return self._region_id

    @property
    def region_name(self) -> str:
        """
        Get Region name

        Returns:
            str -- name of the region
        """
        return self._region_name

    @property
    def region_type(self) -> str:
        """
        Get Region type

        Returns:
            str -- type of the region
        """
        return self._region_type

    @property
    def locations(self) -> list:
        """
        Get locations

        Returns:
            list -- locations added in the region
        """
        return self._locations

    @property
    def associated_servers_count(self) -> int:
        """
         Get associated servers count

        Returns:
            int -- count of servers associated with the region
         """
        return self._associated_servers_count

    @property
    def associated_servers(self) -> list:
        """
         Get associated servers

        Returns:
            list -- list of servers associated with the region
         """
        return self._associated_servers

    @property
    def associated_plans_count(self) -> int:
        """
        Get associated plans count

        Returns:
            int -- count of plans associated with the region
        """
        return self._associated_plans_count

    @property
    def associated_plans(self) -> list:
        """
        Get associated plans

        Returns:
            list -- list of plans associated with the region
        """
        return self._associated_plans

    def refresh(self) -> None:
        """Refresh the properties of the regions."""
        self._get_region_properties() # Refresh the region properties
