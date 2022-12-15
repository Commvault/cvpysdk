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

AssociatedEntityRegion: Class for representing all Region associations with entites

AssociatedEntityRegion
======================

    __init__()                  --  initialize instance of the AssociatedEntityRegion class

    set_region()                --  Associates a region to an entity

    get_region()                --  Get teh region associated to an entity

    calculate_region()          --  Calculates the Region to be associated to an Entity

"""
from .exception import SDKException

class AssociatedEntityRegion:
    """ Class for associating Regions to all entities"""

    def __init__(self, commcell_object):
        """ Initialize object of the Regions class """
        self._commcell_object = commcell_object
        self._EDIT_REGION = self._commcell_object._services['EDIT_REGION']
        self._GET_REGION = self._commcell_object._services['GET_REGION']
        self._CALCULATE_REGION = self._commcell_object._services['CALCULATE_REGION']

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
                    return response.json()['regionId']

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