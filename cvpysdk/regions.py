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

Region:
=======
    _get_region_id()                --  Returns the region id

Attributes:
    ***region_id***                 --  Id of the given Region

"""
from .exception import SDKException


class Regions:
    """
    Class for representing all the Regions created in the commcell
    """
    def __init__(self, commcell_object):
        """Initialises the object of Regions class"""
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._regions_api = self._commcell_object._services['REGIONS']
        self._EDIT_REGION = self._commcell_object._services['EDIT_REGION']
        self._GET_REGION = self._commcell_object._services['GET_REGION']
        self._CALCULATE_REGION = self._commcell_object._services['CALCULATE_REGION']
        self._regions = {}
        self.refresh()

    def _get_regions(self):
        """Gets all the regions created in commcell"""
        flag, response = self._cvpysdk_object.make_request('GET', self._regions_api)
        if flag:
            if response.json() and 'regions' in response.json():
                for region in response.json()['regions']:
                    name = region['name']
                    id = region['id']
                    self._regions[name.lower()] = id

                return self._regions

            raise SDKException('Response', '102')

        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the list of Regions associated to commcell"""
        self._regions = self._get_regions()

    def has_region(self, name):
        """Checks if the given Region exists in the Commcell.

            Args:
                name    (str)   --  name of the Region

            Returns:
                bool    -   boolean output whether the Region exists in the commcell or not

            Raises:
                SDKException:
                    if type of the Region name argument is not string

        """
        if not isinstance(name, str):
            raise SDKException('Region', '103')

        return self._regions and (name.lower() in self._regions)

    def get(self, name):
        """
        Returns the instance of Region class for the given Region name
        Args:
            name    (str)   --  name of the Region

        Returns:
            object  -- Instance of Region class for the given Region name

        Raises:
            SDKException:
                - If the Region name argument is not a string

                - If No Region found in commcell with the given region name
        """
        if not isinstance(name, str):
            raise SDKException('Region', '102',"Invalid input received")

        name = name.lower()

        if self.has_region(name):
            return Region(self._commcell_object, name, self._regions[name])
        raise SDKException('Region', '103',"Region not present in commcell")

    def set_region(self, entity_type, entity_id, entity_region_type, region_id):
        """
        Associate a region to an entity
        Args:
            entity_type         (str)   :   Type of the entity
                                            (eg:    COMMCELL,
                                                    COMPANY,
                                                    CLIENT,
                                                    CLIENT_GROUP,
                                                    MEDIAAGENT,
                                                    STORAGE_POOL, etc
                                            )
            entity_id           (int)   :   unique id of the entity

            entity_region_type  (str)   :   Type of the region
                                            (WORKLOAD or BACKUP)

            region_id           (int)   :   ID of the region from app_regions
        """
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

    def get_region(self, entity_type, entity_id, entity_region_type):
        """
        Gets the Region associated to an Entity
        Args:
            entity_type         (str)   :   Type of the entity
                                            (eg:    COMMCELL,
                                                    COMPANY,


                                                    CLIENT,
                                                    CLIENT_GROUP,
                                                    MEDIAAGENT,
                                                    STORAGE_POOL, etc
                                            )
            entity_id           (int)   :   unique id of the entity

            entity_region_type  (str)   :   Type of the region
                                            (WORKLOAD or BACKUP)
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

    def calculate_region(self, entity_type, entity_id, entity_region_type):
        """
                Calculates the Region to be associated to an Entity
                Args:
                    entity_type         (str)   :   Type of the entity
                                                    (eg:    COMMCELL,
                                                            COMPANY,
                                                            CLIENT,
                                                            CLIENT_GROUP,
                                                            MEDIAAGENT,
                                                            STORAGE_POOL, etc
                                                    )
                    entity_id           (int)   :   unique id of the entity

                    entity_region_type  (str)   :   Type of the region
                                                    (WORKLOAD or BACKUP)
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



class Region:
    """ Class for performing operations on a given Region """
    def __init__(self, commcell_object, region_name, region_id=None):
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

    def _get_region_id(self):
        """ Returns the ID of the Region """
        regions = Regions(self._commcell_object)
        id = regions.get(self._region_name).region_id

    @property
    def region_id(self):
        """ Get Region ID """
        return self._region_id