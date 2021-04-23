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

"""Main file for performing operations on entity manager app under Activate.

'Tags' , 'TagSet', 'Tag', 'EntityManagerTypes' , `ActivateEntities`, and `ActivateEntity` are 6 classes defined in this file.

ActivateEntities:   Class for representing all the regex entities in the commcell.

ActivateEntity:     Class for representing a single regex entity in the commcell.

EntityManagerTypes: Class to represent different entity types in entity manager

Tags:   Class to represent TagSets in the commcell

TagSet: Class to represent single Tagset entity in the commcell

Tag:  Class to represent tag inside a TagSet

Tags:

    __init__()                          --  initialise object of the Tags class

     _response_not_success()            --  parses through the exception response, and raises SDKException

    refresh()                           --  refresh the TagSet associated with the commcell

    _get_tag_sets_from_collections()    --  gets all the TagSet details from collection response

    _get_all_tag_sets()                 --  Returns dict consisting all TagSets associated with commcell

    get_properties()                    --  Returns the properties for the given TagSet name

    has_tag_set()                       --  Checks whether tagset with given name exists in commcell or not

    add()                               --  Creates new TagSet in the commcell

    delete()                            --  Deletes the Tagset in the commcell

    get()                               --  Returns the TagSet object for given tagset name


TagSet:

     __init__()                         --  initialize an object of TagSet Class with the given tagset
                                                name and id

     _response_not_success()            --  parses through the exception response, and raises SDKException

    refresh()                           --  refresh the properties of the TagSet

    modify()                            --  Modifies the tagset in the commcell

    share()                             --  Shares tagset with user or group in the commcell

    add_tag()                           --  Creates new tag inside this tagset container in commcell

    get()                               --  Returns the Tag class object for given tag name

    has_tag()                           --  checks whether given tag exists in tagset or not

    get_tag_id()                        --  Returns the tag id for given tag name

    _get_tag_set_id()                   --  Gets tag set container id for the given Tagset name

    _get_tag_set_properties()           --  Gets all the details of associated Tagset

TagSet Attributes
-----------------

    **guid**            --  returns container GUID of this tagset

    **full_name**       --  returns the full name of tagset container

    **comment**         --  returns the comment for this tagset

    **owner**           --  returns the owner user name for this tagset

    **tags**            --  returns the tags present in this tagset

    **tag_set_id**      --  returns the tagset id

Tag:

    __init__()                  --  Initialise object of the Tag class

    _response_not_success()     --  parses through the exception response, and raises SDKException

    _get_tag_id()               --  Returns the tag id of the given tag name

    _get_tag_properties()       --  Returns the properties of Tag

    refresh()                   --  refresh the tag details

    modify()                    --  modifies the name of the tag

Tag Attributes
-----------------

    **guid**            --  returns tag GUID of this tag

    **full_name**       --  returns the full name of this tag

    **tag_id**          --  returns the id of the tag


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

    **entity_type**       --  returns the type of entity (1- NER 2-RER 3-Derived 4-Classifier)

    **entity_xml**        --  returns the entity xml associated with this entity

"""
import copy
from enum import Enum

from past.builtins import basestring


from ..exception import SDKException
from .constants import ActivateEntityConstants
from .constants import TagConstants


class EntityManagerTypes(Enum):
    """Class to represent different entity types in entity manager"""
    ENTITIES = "Entities"
    CLASSIFIERS = "Classifiers"
    TAGS = "Tags"


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
        self._entity_xml = None
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

        regex_entity_dict = self._commcell_object.activate.entity_manager().get_properties(self._entity_name)
        self._display_name = regex_entity_dict['displayName']
        self._category_name = regex_entity_dict['categoryName']
        self._entity_id = regex_entity_dict['entityId']
        self._is_enabled = regex_entity_dict['enabled']
        self._entity_key = regex_entity_dict['entityKey']
        self._entity_type = regex_entity_dict['entityType']
        self._entity_xml = regex_entity_dict['entityXML']
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

    @property
    def entity_xml(self):
        """Returns the entity xml attribute."""
        return self._entity_xml

    def refresh(self):
        """Refresh the regex entity details for associated object"""
        self._get_entity_properties()


class Tags(object):
    """Class for representing all the Tagsets in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the Tags class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the Tags class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._tag_set_entities = None
        self._api_get_all_tag_sets = self._services['GET_TAGS']
        self._api_add_tag_set = self._services['ADD_CONTAINER']
        self._api_delete_tag_set = self._services['DELETE_CONTAINER']
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    @staticmethod
    def _get_tag_sets_from_collections(collections):
        """Extracts all the tagsets, and their details from the list of collections given,
            and returns the dictionary of all tagsets

            Args:
                collections     (list)  --  list of all tagsets

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single tagset

        """
        _tag_set_entity = {}
        for tagset in collections['listOftagSetList']:
            tagset = tagset['tagSetsAndItems']
            container = tagset[0]['container']
            owner_info = tagset[0]['container']['ownerInfo']
            tagset_dict = {}
            tagset_dict['containerName'] = container.get('containerName', "")
            tagset_dict['containerFullName'] = container.get('containerFullName', "")
            tagset_dict['containerId'] = container.get('containerId', "")
            tagset_dict['containerGuid'] = container.get('containerGuid', "")
            tagset_dict['comment'] = container.get('comment', "")
            tagset_dict['owneruserName'] = owner_info.get('userName', "")
            tagset_dict['owneruserGuid'] = owner_info.get('userGuid', "")
            tagset_dict['owneraliasName'] = owner_info.get('aliasName', "")
            container_tags = []
            tag_ids = []
            tag_dict = {}
            # process tags only if it is present
            if 'tags' in tagset[0]:
                tags = tagset[0]['tags']
                for tag in tags:
                    tag_dict[tag['name'].lower()] = tag
                    container_tags.append(tag['name'].lower())
                    tag_ids.append(tag['tagId'])
            tagset_dict['tags'] = container_tags
            tagset_dict['tagsIds'] = tag_ids
            tagset_dict['tagsDetails'] = tag_dict
            _tag_set_entity[tagset_dict['containerName'].lower()] = tagset_dict
        return _tag_set_entity

    def _get_all_tag_sets(self):
        """Gets the list of all tagsets associated with this commcell.

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single tagset entity

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._api_get_all_tag_sets
        )

        if flag:
            if response.json() and 'listOftagSetList' in response.json():
                return self._get_tag_sets_from_collections(response.json())
            raise SDKException('Tags', '103')
        self._response_not_success(response)

    def get(self, tag_set_name):
        """Returns a TagSet object for the given Tagset name.

            Args:
                tag_set_name (str)  --  name of the TagSet

            Returns:

                obj                 -- Object of TagSet class

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

                    if tag_set_name is not of type string


        """
        if not isinstance(tag_set_name, basestring):
            raise SDKException('Tags', '101')

        if self.has_tag_set(tag_set_name):
            tag_set_id = self._tag_set_entities[tag_set_name]['containerId']
            return TagSet(self._commcell_object, tag_set_name=tag_set_name, tag_set_id=tag_set_id)
        raise SDKException('Tags', '102', "Unable to get TagSet class object")

    def has_tag_set(self, tag_set_name):
        """Checks if a tagset exists in the commcell with the input name or not

            Args:
                tag_set_name (str)  --  name of the TagSet

            Returns:
                bool - boolean output whether the TagSet exists in the commcell or not

            Raises:
                SDKException:
                    if type of the TagSet name argument is not string

        """
        if not isinstance(tag_set_name, basestring):
            raise SDKException('Tags', '101')
        return self._tag_set_entities and tag_set_name.lower() in map(str.lower, self._tag_set_entities)

    def get_properties(self, tag_set_name):
        """Returns a properties of the specified TagSet name.

            Args:
                tag_set_name (str)  --  name of the TagSet

            Returns:
                dict -  properties for the given TagSet name


                Example : {
                              "containerName": "cvpysdk1",
                              "containerFullName": "cvpysdk1",
                              "containerId": 65931,
                              "containerGuid": "6B870271-543A-4B76-955D-CDEB3807D68E",
                              "comment": "Created from CvPySDK",
                              "owneruserName": "xxx",
                              "owneruserGuid": "C31C1194-AA5C-47C3-B5B0-9087EF429B6B",
                              "owneraliasName": "xx",
                              "tags": [
                                "p10"
                              ],
                              "tagsIds": [
                                15865
                              ],
                              "tagsDetails": {
                                "p10": {
                                  "tagOwnerType": 1,
                                  "tagId": 15865,
                                  "name": "p10",
                                  "flags": 0,
                                  "fullName": "cvpysdk1\\p10",
                                  "description": "",
                                  "id": "C9E229D0-B895-4653-9DA7-C9C6BD999121",
                                  "attribute": {}
                                }
                              }
                            }


        """
        return self._tag_set_entities[tag_set_name.lower()]

    def delete(self, tag_set_name):
        """Deletes the specified tagset from the commcell

                Args:

                    tag_set_name    (str)       --  Name of the Tagset

                Returns:

                    None

                Raises:

                    SDKException:

                                if response is empty

                                if response is not success

                                if unable to delete TagSet entity in commcell

                                if input data type is not valid
        """
        if not isinstance(tag_set_name, basestring):
            raise SDKException('Tags', '101')
        request_json = copy.deepcopy(TagConstants.TAG_SET_DELETE_REQUEST_JSON)
        request_json['containers'][0]['containerId'] = self._tag_set_entities[tag_set_name.lower()]['containerId']
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._api_delete_tag_set, request_json
        )
        if flag:
            if response.json() and 'errorCode' in response.json():
                if int(response.json()['errorCode']) != 0:
                    raise SDKException('Tags', '102', response.json()['errorMessage'])
            self.refresh()
            return
        self._response_not_success(response)

    def add(self, tag_set_name, comment="Created from CvPySDK"):
        """Adds the specified TagSet name in the commcell

                    Args:
                        tag_set_name (str)     --  name of the TagSet

                        comment (str)         --  Comment for this TagSet

                    Returns:

                        object      --  Object of TagSet class

                    Raises:
                        SDKException:

                                if response is empty

                                if response is not success

                                if unable to add TagSet entity in commcell

                                if input data type is not valid
                """
        if not isinstance(tag_set_name, basestring) or not isinstance(comment, basestring):
            raise SDKException('Tags', '101')
        request_json = copy.deepcopy(TagConstants.TAG_SET_ADD_REQUEST_JSON)
        request_json['container']['containerName'] = tag_set_name
        request_json['container']['comment'] = comment
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._api_add_tag_set, request_json
        )
        if flag:
            if response.json():
                if 'errList' in response.json():
                    raise SDKException('Tags', '102', response.json()['errList'][0]['errLogMessage'])
                elif 'container' in response.json():
                    self.refresh()
                    return TagSet(commcell_object=self._commcell_object, tag_set_name=tag_set_name)
            raise SDKException('Tags', '104')
        self._response_not_success(response)

    def refresh(self):
        """Refresh the TagSet entities associated with the commcell."""
        self._tag_set_entities = self._get_all_tag_sets()


class TagSet(object):
    """Class for performing operations on a TagSet"""

    def __init__(self, commcell_object, tag_set_name, tag_set_id=None):
        """Initialize an object of the TagSet class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                tag_set_name     (str)          --  name of the TagSet

                tag_set_id       (str)          --  Container id of the TagSet
                                                        default: None

            Returns:
                object  -   instance of the Tagset class
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._services = commcell_object._services
        self._cvpysdk_obj = self._commcell_object._cvpysdk_object
        self._tag_set_name = tag_set_name
        self._tag_set_id = None
        self._tag_set_props = None
        if tag_set_id is None:
            self._tag_set_id = self._get_tag_set_id(tag_set_name)
        else:
            self._tag_set_id = tag_set_id
        self._container_guid = None
        self._owner = None
        self._full_name = None
        self._comment = None
        self._tags = None
        self._tag_ids = None
        self._api_modify_tag_set = self._services['ADD_CONTAINER']
        self._api_add_tag = self._services['GET_TAGS']
        self._api_security = self._services['SECURITY_ASSOCIATION']
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def has_tag(self, tag_name):
        """Returns whether tag exists with given name or not in tagset

                    Args:
                        tag_name (str)      --  name of the Tag

                    Returns:

                        bool    --  True if it exists or else false

                    Raises:
                        SDKException:

                            if tag_name is not of type string


        """
        if not isinstance(tag_name, basestring):
            raise SDKException('Tags', '101')
        if tag_name.lower() in self.tags:
            return True
        return False

    def get(self, tag_name):
        """Returns a Tag object for the given Tag name.

            Args:
                tag_name (str)      --  name of the Tag

            Returns:

                obj                 -- Object of Tag class

            Raises:
                SDKException:

                    if unable to create Tag object

                    if tag_name is not of type string


        """
        if not isinstance(tag_name, basestring):
            raise SDKException('Tags', '101')
        if self.has_tag(tag_name):
            return Tag(self._commcell_object, tag_set_name=self._tag_set_name, tag_name=tag_name)
        raise SDKException('Tags', '102', "Unable to get Tag class object")

    def get_tag_id(self, tag_name):
        """Returns the tag id for the given tag name

                Args:

                    tag_name        (str)       --  Name of the tag

                Returns:

                    int     --  Tag id

                Raises:

                    SDKExeption:

                        if input tag name is not found in this tagset

        """
        if tag_name.lower() not in self.tags:
            raise SDKException('Tags', '106')
        index = self.tags.index(tag_name.lower())
        return self._tag_ids[index]

    def add_tag(self, tag_name):
        """Adds the specified tag name in the tagset container in commcell

                           Args:
                               tag_name (str)     --  name of the Tag

                           Returns:

                               object      --  Object of Tag class

                           Raises:
                               SDKException:

                                       if response is empty

                                       if response is not success

                                       if unable to add Tag inside Tagset in commcell

                                       if input data type is not valid
                       """
        if not isinstance(tag_name, basestring):
            raise SDKException('Tags', '101')
        request_json = copy.deepcopy(TagConstants.TAG_ADD_REQUEST_JSON)
        request_json['container']['containerId'] = self._tag_set_id
        request_json['tags'][0]['name'] = tag_name
        flag, response = self._cvpysdk_obj.make_request(
            'POST', self._api_add_tag, request_json
        )
        if flag:
            if response.json():
                if 'errList' in response.json():
                    raise SDKException('Tags', '102', response.json()['errList'][0]['errLogMessage'])
                elif 'tag' in response.json():
                    self.refresh()
                    return Tag(commcell_object=self._commcell_object, tag_set_name=self._tag_set_name,
                               tag_name=tag_name)
            raise SDKException('Tags', '104')
        self._response_not_success(response)

    def share(self, user_or_group_name, allow_edit_permission=False, is_user=True, ops_type=1):
        """Shares tagset with given user or group in commcell

                Args:

                    user_or_group_name      (str)       --  Name of user or group

                    is_user                 (bool)      --  Denotes whether this is user or group name
                                                                default : True(User)

                    allow_edit_permission   (bool)      --  whether to give edit permission or not to user or group

                    ops_type                (int)       --  Operation type

                                                            Default : 1 (Add)

                                                            Supported : 1 (Add)
                                                                        2 (Modify)
                                                                        3 (Delete)

                Returns:

                    None

                Raises:

                    SDKException:

                            if unable to update security associations

                            if response is empty or not success
        """
        if not isinstance(user_or_group_name, basestring):
            raise SDKException('Tags', '101')
        request_json = copy.deepcopy(TagConstants.TAG_SET_SHARE_REQUEST_JSON)
        external_user = False
        if '\\' not in user_or_group_name:
            user_or_group_name = f"\\{user_or_group_name}"
        else:
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
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['externalGroupName'] = user_or_group_name
        else:
            grp_obj = self._commcell_object.user_groups.get(user_or_group_name)
            grp_id = grp_obj.user_group_id
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userGroupId'] = int(grp_id)
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = "15"
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userGroupName'] = user_or_group_name

        request_json['entityAssociated']['entity'][0]['tagId'] = self._tag_set_id
        request_json['securityAssociations']['associationsOperationType'] = ops_type

        if allow_edit_permission:
            request_json['securityAssociations']['associations'][0]['properties']['permissions'].append(
                TagConstants.ADD_PERMISSION)
        flag, response = self._cvpysdk_obj.make_request(
            'POST', self._api_security, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                response_json = response.json()['response'][0]
                error_code = response_json['errorCode']
                if error_code != 0:
                    error_message = response_json['errorString']
                    raise SDKException(
                        'Tags',
                        '102', error_message)
            else:
                raise SDKException('Tags', '107')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def modify(self, new_name=None, comment="Modified from CvPySDK"):
        """Modifies the specified tagset in the commcell

                Args:

                    new_name        (str)       --  New name for Tagset

                    comment         (str)       --  New comment which needs to be added for Tagset

                Returns:

                    None

                Raises:

                    SDKException:

                                if response is empty

                                if response is not success

                                if unable to modify TagSet entity in commcell

                                if input is not a valid data type of string

        """
        if not isinstance(new_name, basestring) or not isinstance(comment, basestring):
            raise SDKException('Tags', '101')
        request_json = copy.deepcopy(TagConstants.TAG_SET_MODIFY_REQUEST_JSON)
        request_json['container']['containerName'] = new_name
        request_json['container']['comment'] = comment
        request_json['container']['containerId'] = self._tag_set_id
        flag, response = self._cvpysdk_obj.make_request(
            'POST', self._api_modify_tag_set, request_json
        )
        if flag:
            if response.json():
                if 'errList' in response.json():
                    raise SDKException('Tags', '102', response.json()['errList'][0]['errLogMessage'])
                elif 'container' in response.json():
                    self._tag_set_name = new_name
                    self.refresh()
                    return
            raise SDKException('Tags', '105')
        self._response_not_success(response)

    def refresh(self):
        """Refresh the TagSet details for associated object"""
        self._tag_set_props = self._get_tag_set_properties()

    def _get_tag_set_properties(self):
        """ Get TagSet properties for this associated object
                Args:

                    None

                Returns:

                    dict    --  Containing tagset properties

        """
        tags = self._commcell_object.activate.entity_manager(
            EntityManagerTypes.TAGS)
        # call refresh before fetching properties
        tags.refresh()
        tag_set_dict = tags.get_properties(self._tag_set_name)
        self._full_name = tag_set_dict['containerFullName']
        self._owner = tag_set_dict['owneruserName']
        self._comment = tag_set_dict['comment']
        self._container_guid = tag_set_dict['containerGuid']
        self._tags = tag_set_dict['tags']
        self._tag_ids = tag_set_dict['tagsIds']
        return tag_set_dict

    def _get_tag_set_id(self, tag_set_name):
        """ Get TagSet container id for given tag set name
                Args:

                    tag_set_name (str)  -- Name of the TagSet

                Returns:

                    int                --  TagSet container Id

        """

        return self._commcell_object.activate.entity_manager(
            entity_type=EntityManagerTypes.TAGS).get(tag_set_name).tag_set_id

    @property
    def guid(self):
        """Returns the container guid of this Tagset"""
        return self._container_guid

    @property
    def full_name(self):
        """Returns the full name of this Tagset"""
        return self._full_name

    @property
    def comment(self):
        """Returns the comment provided for this Tagset"""
        return self._comment

    @property
    def owner(self):
        """Returns the owner username for this Tagset"""
        return self._owner

    @property
    def tags(self):
        """Returns the tags present in this tagset"""
        return self._tags

    @property
    def tag_set_id(self):
        """returns the container id for this tagset"""
        return self._tag_set_id


class Tag(object):
    """Class for performing operations on a single Tag"""

    def __init__(self, commcell_object, tag_set_name, tag_name, tag_id=None):
        """Initialize an object of the Tag class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                tag_set_name     (str)          --  name of the TagSet

                tag_name         (str)          --  Name of tag inside TagSet container

                tag_id       (str)              --  id for tag
                                                        default: None

            Returns:
                object  -   instance of the Tag class
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._services = commcell_object._services
        self._cvpysdk_obj = self._commcell_object._cvpysdk_object
        self._tag_name = tag_name
        self._tag_set_name = tag_set_name
        self._tag_id = None
        self._tag_props = None
        self._api_modify_tag = self._services['GET_TAGS']
        if tag_id is None:
            self._tag_id = self._get_tag_id(tag_set_name, tag_name)
        else:
            self._tag_id = tag_id
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_tag_id(self, tag_set_name, tag_name):
        """ Get Tag id for given tag name
                Args:

                    tag_set_name    (str)   --  Name of the TagSet

                    tag_name        (str)   --  Name of the Tag

                Returns:

                    int                --  Tag id

        """
        tags = self._commcell_object.activate.entity_manager(
            entity_type=EntityManagerTypes.TAGS)
        # we need this refresh so that tags gets refreshed after adding new tag inside tagset
        tags.refresh()
        tag_set = tags.get(tag_set_name)
        return tag_set.get_tag_id(tag_name=tag_name)

    def _get_tag_properties(self):
        """ Get Tag properties for this associated tag object
                Args:

                    None

                Returns:

                    dict    --  containing tag properties

                        Example : {
                                      "tagOwnerType": 1,
                                      "tagId": 15865,
                                      "name": "p10",
                                      "flags": 0,
                                      "fullName": "cvpysdk1\\p10",
                                      "description": "",
                                      "id": "C9E229D0-B895-4653-9DA7-C9C6BD999121",
                                      "attribute": {}
                                    }

        """

        tags = self._commcell_object.activate.entity_manager(
            entity_type=EntityManagerTypes.TAGS)
        # we need this refresh so that tags gets refreshed after adding new tag inside tagset
        tags.refresh()
        tag_set_dict = tags.get_properties(self._tag_set_name)
        tag_dict = tag_set_dict['tagsDetails'][self._tag_name]
        return tag_dict

    def modify(self, new_name):
        """Modifies the tag name in the tagset

                Args:

                    new_name        (str)       --  New name for Tag

                Returns:

                    None

                Raises:

                    SDKException:

                                if response is empty

                                if response is not success

                                if unable to modify Tag name

                                if input data type is not valid

        """
        if not isinstance(new_name, basestring):
            raise SDKException('Tags', '101')
        tags = self._commcell_object.activate.entity_manager(
            entity_type=EntityManagerTypes.TAGS)
        tag_set = tags.get(self._tag_set_name)
        request_json = copy.deepcopy(TagConstants.TAG_MODIFY_REQUEST_JSON)
        request_json['container']['containerId'] = tag_set.tag_set_id
        request_json['tags'][0]['tagId'] = self._tag_id
        request_json['tags'][0]['name'] = new_name
        flag, response = self._cvpysdk_obj.make_request(
            'PUT', self._api_modify_tag, request_json
        )
        if flag:
            if response.json():
                if 'errList' in response.json():
                    raise SDKException('Tags', '102', response.json()['errList'][0]['errLogMessage'])
                elif 'tag' in response.json():
                    self._tag_name = new_name
                    self.refresh()
                    return
            raise SDKException('Tags', '105')
        self._response_not_success(response)

    def refresh(self):
        """Refresh the TagSet details for associated object"""
        self._tag_props = self._get_tag_properties()

    @property
    def full_name(self):
        """Returns the full name of the tag inside tagset"""
        return self._tag_props['fullName']

    @property
    def guid(self):
        """Returns the tag guid value"""
        return self._tag_props['id']

    @property
    def tag_id(self):
        """Returns the id of the tag"""
        return self._tag_id
