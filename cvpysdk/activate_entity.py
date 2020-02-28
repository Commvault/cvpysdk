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

"""Main file for performing operations on Activate regex Entities, and a single Activate regex Entity in the commcell.

`ActivateEntities`, and `ActivateEntity` are 2 classes defined in this file.

ActivateEntities:   Class for representing all the regex entities in the commcell.

ActivateEntity:     Class for representing a single regex entity in the commcell.


ActivateEntities:

    __init__(commcell_object)           --  initialise object of the ActivateEntities class

     _response_not_success()            --  parses through the exception response, and raises SDKException

    refresh()                           --  refresh the regex entities associated with the commcell

    get()                               --  Returns an instance of ActivateEntity class for the given regex entity name

    get_entity_ids()                    --  Returns an list of entity ids for the given regex entity name list

    get_entity_keys()                   --  Returns an list of entity keys for the given regex entity name list

    get_properties()                    --  Returns the properties for the given regex entity name

    _get_all_activate_entities()        --  Returns dict consisting all regex entities associated with commcell

    _get_regex_entity_from_collections()--  gets all the regex entity details from collection response

    has_entity()                        --  Checks whether given regex entity exists in commcell or not

    add()                               --  adds the regex entity in the commcell

    delete()                            --  deletes the regex entity in the commcell for given entity name

ActivateEntity:

    __init__(
        commcell_object,
        entity_name,
        entity_id=None)             --  initialize an object of ActivateEntity Class with the given regex entity
                                                name and id

     _response_not_success()            --  parses through the exception response, and raises SDKException

    refresh()                           --  refresh the properties of the regex entity

    _get_entity_id()                    --  Gets entity id for the given regex entity name

    _get_entity_properties()            --  Gets all the details of associated regex entity

    modify()                            --  Modifies the entity properties for the associated regex entity


ActivateEntity Attributes
-----------------

    **entity_id**         --  returns the id of the regex entity

    **entity_key**        --  returns the key of the regex entity

    **category_name**     --  returns the category name of the regex entity

    **is_enabled**        --  returns the enabled flag of the regex entity

    **display_name**      --  returns the display name of the regex entity

    **entity_type**       --  returns the type of entity (1- NER 2-RER 3-Derived)

"""

from past.builtins import basestring
from .exception import SDKException
from .datacube.constants import ActivateEntityConstants


class ActivateEntities(object):
    """Class for representing all the regex entities in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the ActivateEntities class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the ActivateEntities class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._regex_entities = None
        self._api_get_all_regex_entities = self._services['ACTIVATE_ENTITIES']
        self._api_create_regex_entity = self._api_get_all_regex_entities
        self._api_delete_regex_entity = self._services['ACTIVATE_ENTITY']
        self.refresh()

    def add(self, entity_name, entity_regex, entity_keywords, entity_flag, is_derived=False, parent_entity=None):
        """Adds the specified regex entity name in the commcell

                    Args:
                        entity_name (str)      --  name of the regex entity

                        entity_regex (str)     --  Regex for the entity

                        entity_keywords (str)  --  Keywords for the entity

                        entity_flag (int)      --  Sensitivity flag value for entity
                                                        5-Highly sensitive
                                                        3-Moderate sensitive
                                                        1-Low sensitive

                        is_derived (bool)      --  represents whether it is derived entity or not

                        parent_entity(int)     -- entity id of the parent entity in case of derived entity

                    Returns:
                        None

                    Raises:
                        SDKException:

                                if response is empty

                                if response is not success

                                if unable to add regex entity in commcell

                                if entity_flag is not in proper allowed values [1,3,5]

                                if input data type is not valid
                """
        if not isinstance(entity_name, basestring) or not isinstance(entity_regex, basestring) \
                or not isinstance(entity_keywords, basestring):
            raise SDKException('ActivateEntity', '101')
        if entity_flag not in [1, 3, 5]:
            raise SDKException('ActivateEntity', '102', 'Unsupported entity flag value')
        request_json = ActivateEntityConstants.REQUEST_JSON
        request_json['regularExpression'] = "{\"entity_key\":\"" + \
            entity_name + "\",\"entity_regex\":\"" + entity_regex + "\"}"
        request_json['flags'] = entity_flag
        request_json['entityName'] = entity_name
        request_json['entityXML']['keywords'] = entity_keywords
        if is_derived:
            request_json['regularExpression'] = "{\"entity_key\":\"" + entity_name + "\"}"
            request_json['entityType'] = 3
            if isinstance(parent_entity, int):
                request_json['parentEntityId'] = parent_entity
            elif isinstance(parent_entity, basestring):
                request_json['parentEntityId'] = self._regex_entities[parent_entity]['entityId']
            else:
                raise SDKException('ActivateEntity', '102', 'Unsupported parent entity id type provided')

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._api_create_regex_entity, request_json
        )

        if flag:
            if response.json() and 'entityDetails' in response.json() and 'err' not in response.json():
                self.refresh()
                return
            raise SDKException('ActivateEntity', '104')
        self._response_not_success(response)

    def delete(self, entity_name):
        """deletes the specified regex entity name in the commcell

                    Args:
                        entity_name (str)      --  name of the regex entity

                    Returns:
                        None

                    Raises:
                        SDKException:

                                if response is empty

                                if response is not success

                                if unable to delete regex entity in commcell

                                if unable to find entity name in the commcell

                                if data type of entity_name is invalid


                """
        if not isinstance(entity_name, basestring):
            raise SDKException('ActivateEntity', '101')
        if entity_name not in self._regex_entities:
            raise SDKException('ActivateEntity', '102', 'Unable to find given regex entity name in the commcell')

        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._api_delete_regex_entity % self._regex_entities[entity_name]['entityId']
        )

        if flag:
            if response.json() and 'errorCode' in response.json() and response.json()['errorCode'] == 0:
                self.refresh()
                return
            raise SDKException('ActivateEntity', '105')
        self._response_not_success(response)

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_properties(self, entity_name):
        """Returns a properties of the specified regex entity name.

            Args:
                entity_name (str)  --  name of the regex entity

            Returns:
                dict -  properties for the given regex entity name


        """
        return self._regex_entities[entity_name]

    def _get_all_activate_entities(self):
        """Gets the list of all regex entities associated with this commcell.

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single regex entity

                    {
                        "entityDetails": [
                            {
                                "displayName": "US Social Security number",
                                "flags": 5,
                                "description": "",
                                "categoryName": "US",
                                "enabled": true,
                                "entityName": "SSN",
                                "attribute": 3,
                                "entityType": 2,
                                "entityKey": "ssn",
                                "entityId": 1111,
                                "entityXML": {
                                    "keywords": "Social Security,Social Security#,Soc Sec,SSN,SSNS,SSN#,SS#,SSID",
                                    "entityKey": "ssn",
                                    "isSystemDefinedEntity": true,
                                    "inheritBaseWords": false
                                }
                            },
                            {
                                "displayName": "Person Name",
                                "flags": 1,
                                "description": "Name of a person.",
                                "categoryName": "Generic",
                                "enabled": true,
                                "entityName": "Person",
                                "attribute": 3,
                                "entityType": 1,
                                "entityKey": "person",
                                "entityId": 1112,
                                "entityXML": {
                                    "keywords": "",
                                    "entityKey": "person",
                                    "inheritBaseWords": false
                                }
                            }
                            ]
                            }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._api_get_all_regex_entities
        )

        if flag:
            if response.json() and 'entityDetails' in response.json():
                return self._get_regex_entity_from_collections(response.json())
            raise SDKException('ActivateEntity', '103')
        self._response_not_success(response)

    @staticmethod
    def _get_regex_entity_from_collections(collections):
        """Extracts all the regex entities, and their details from the list of collections given,
            and returns the dictionary of all regex entities

            Args:
                collections     (list)  --  list of all collections

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single regex entity

        """
        _regex_entity = {}
        for regex_entity in collections['entityDetails']:
            regex_entity_dict = {}
            regex_entity_dict['displayName'] = regex_entity.get('displayName', "")
            regex_entity_dict['entityKey'] = regex_entity.get('entityKey', "")
            regex_entity_dict['categoryName'] = regex_entity.get('categoryName', "")
            regex_entity_dict['entityXML'] = regex_entity.get('entityXML', "")
            regex_entity_dict['entityId'] = regex_entity.get('entityId', 0)
            regex_entity_dict['flags'] = regex_entity.get('flags', 0)
            regex_entity_dict['entityType'] = regex_entity.get('entityType', 0)
            regex_entity_dict['enabled'] = regex_entity.get('enabled', False)
            _regex_entity[regex_entity['entityName']] = regex_entity_dict
        return _regex_entity

    def refresh(self):
        """Refresh the activate regex entities associated with the commcell."""
        self._regex_entities = self._get_all_activate_entities()

    def get(self, entity_name):
        """Returns a ActivateEntity object for the given regex entity name.

            Args:
                entity_name (str)  --  name of the regex entity

            Returns:

                obj                 -- Object of ActivateEntity class

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

                    if entity_name is not of type string


        """
        if not isinstance(entity_name, basestring):
            raise SDKException('ActivateEntity', '101')

        if self.has_entity(entity_name):
            entity_id = self._regex_entities[entity_name]['entityId']
            return ActivateEntity(self._commcell_object, entity_name, entity_id)
        raise SDKException('ActivateEntity', '102', "Unable to get ActivateEntity class object")

    def get_entity_ids(self, entity_name):
        """Returns a list of entity id for the given regex entity name list.

            Args:
                entity_name (list)  --  names of the regex entity

            Returns:

                list                -- entity id's for the given entity names


        """
        if not isinstance(entity_name, list):
            raise SDKException('ActivateEntity', '101')
        entity_ids = []
        for regex_entity in entity_name:
            if regex_entity in self._regex_entities:
                entity_ids.append(self._regex_entities[regex_entity]['entityId'])
            else:
                raise SDKException(
                    'ActivateEntity', '102', f"Unable to find entity id for given entity name :{regex_entity}")
        return entity_ids

    def get_entity_keys(self, entity_name):
        """Returns a list of entity keys for the given regex entity name list.

            Args:
                entity_name (list)  --  names of the regex entity

            Returns:

                list                -- entity keys for the given entity names


        """
        if not isinstance(entity_name, list):
            raise SDKException('ActivateEntity', '101')
        entity_keys = []
        for regex_entity in entity_name:
            if regex_entity in self._regex_entities:
                entity_keys.append(self._regex_entities[regex_entity]['entityKey'])
            else:
                raise SDKException(
                    'ActivateEntity', '102', f"Unable to find entity keys for given entity name :{regex_entity}")
        return entity_keys

    def has_entity(self, entity_name):
        """Checks if a regex entity exists in the commcell with the input name.

            Args:
                entity_name (str)  --  name of the regex entity

            Returns:
                bool - boolean output whether the regex entity exists in the commcell or not

            Raises:
                SDKException:
                    if type of the regex entity name argument is not string

        """
        if not isinstance(entity_name, basestring):
            raise SDKException('ActivateEntity', '101')

        return self._regex_entities and entity_name.lower() in map(str.lower, self._regex_entities)


class ActivateEntity(object):
    """Class for performing operations on a single regex entity"""

    def __init__(self, commcell_object, entity_name, entity_id=None):
        """Initialize an object of the ActivateEntity class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                entity_name     (str)           --  name of the regex entity

                entity_id       (str)           --  id of the regex entity
                    default: None

            Returns:
                object  -   instance of the ActivateEntity class
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._services = commcell_object._services
        self._cvpysdk_obj = self._commcell_object._cvpysdk_object
        self._entity_name = entity_name
        self._entity_id = None
        self._display_name = None
        self._entity_type = None
        self._is_enabled = None
        self._entity_key = None
        self._category_name = None
        if entity_id is None:
            self._entity_id = self._get_entity_id(entity_name)
        else:
            self._entity_id = entity_id
        self.refresh()
        self._api_modify_regex_entity = self._services['ACTIVATE_ENTITY']

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def modify(self, entity_regex, entity_keywords, entity_flag, is_derived=False, parent_entity=None):
        """Modifies the specified regex entity details

                    Args:

                        entity_regex (str)     --  Regex for the entity

                        entity_keywords (str)  --  Keywords for the entity

                        entity_flag (int)      --  Sensitivity flag value for entity
                                                        5-Highly sensitive
                                                        3-Moderate sensitive
                                                        1-Low sensitive

                        is_derived (bool)      --  represents whether it is derived entity or not

                        parent_entity(int)     -- entity id of the parent entity in case of derived entity

                    Returns:
                        None

                    Raises:
                        SDKException:

                                if response is empty

                                if response is not success

                                if unable to modify regex entity in commcell

                                if input entity_keywords & entity_regex is not string

                                if entity_flag value is not in allowed values[1,3,5]


                """
        if not isinstance(entity_regex, basestring) \
                or not isinstance(entity_keywords, basestring):
            raise SDKException('ActivateEntity', '101')
        if entity_flag not in [1, 3, 5]:
            raise SDKException('ActivateEntity', '102', 'Unsupported entity flag value')
        request_json = ActivateEntityConstants.REQUEST_JSON
        request_json['regularExpression'] = "{\"entity_key\":\"" + \
            self._entity_name + "\",\"entity_regex\":\"" + entity_regex + "\"}"
        request_json['flags'] = entity_flag
        request_json['entityName'] = self._entity_name
        request_json['entityXML']['keywords'] = entity_keywords
        if is_derived:
            request_json['regularExpression'] = "{\"entity_key\":\"" + self._entity_name + "\"}"
            request_json['entityType'] = 3
            if isinstance(parent_entity, int):
                request_json['parentEntityId'] = parent_entity
            elif isinstance(parent_entity, basestring):
                request_json['parentEntityId'] = ActivateEntities.get(
                    self._commcell_object, entity_name=parent_entity).entity_id
            else:
                raise SDKException('ActivateEntity', '102', 'Unsupported parent entity id type provided')

        flag, response = self._cvpysdk_obj.make_request(
            'PUT', (self._api_modify_regex_entity % self.entity_id), request_json
        )

        if flag:
            if response.json() and 'entityDetails' in response.json() and 'err' not in response.json():
                return
            raise SDKException('ActivateEntity', '106')
        self._response_not_success(response)

    def _get_entity_id(self, entity_name):
        """ Get regex entity id for given entity name
                Args:

                    entity_name (str)  -- Name of the regex entity

                Returns:

                    int                -- id of the regex entity

        """

        return self._commcell_object.activate_entity.get(entity_name).entity_id

    def _get_entity_properties(self):
        """ Get regex entity properties for given entity name
                Args:

                    None

                Returns:

                    None

        """

        regex_entity_dict = self._commcell_object.activate_entity.get_properties(self._entity_name)
        self._display_name = regex_entity_dict['displayName']
        self._category_name = regex_entity_dict['categoryName']
        self._entity_id = regex_entity_dict['entityId']
        self._is_enabled = regex_entity_dict['enabled']
        self._entity_key = regex_entity_dict['entityKey']
        self._entity_type = regex_entity_dict['entityType']
        return regex_entity_dict

    @property
    def entity_id(self):
        """Returns the value of the regex entity id attribute."""
        return self._entity_id

    @property
    def entity_type(self):
        """Returns the entity type attribute."""
        return self._entity_type

    @property
    def category_name(self):
        """Returns the entity category name attribute."""
        return self._category_name

    @property
    def display_name(self):
        """Returns the entity display name attribute."""
        return self._display_name

    @property
    def is_enabled(self):
        """Returns the entity isenabled attribute."""
        return self._is_enabled

    @property
    def entity_key(self):
        """Returns the entity key attribute."""
        return self._entity_key

    def refresh(self):
        """Refresh the regex entity details for associated object"""
        self._get_entity_properties()
