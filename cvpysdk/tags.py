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

"""File for performing tags related operations.


Tags: Class for representing all the tags created by the user which is logged in.


Tags:
    Methods:

        has_tag()   --  checks whether the tag with given name exists or not

        add()       --  creates a new tag to commcell

        get()       --  returns a tag object for given tag name

        delete()    --  deletes an entity tag from commcell

        refresh()   --  refreshes the tags list

    Properties:

        **all_tags  --  returns the dict containing all the tags and id

Tag:
    Properties:

        **tag_id    --  returns tag id

        **tag_name  --  returns tag name

"""
from typing import TYPE_CHECKING

from cvpysdk.exception import SDKException

if TYPE_CHECKING:
    from .commcell import Commcell

class Tags:
    """Class for doing operations related to entity tags from backend

    Attributes:
        _commcell_object (object): Instance of the Commcell class.
        _service (dict): Dictionary of service URLs.
        _cvpysdk_object (object): Instance of the CVPYSDK class.
        _get_tags_url (str): URL to get entity tags.
        _create_tags_url (str): URL to create entity tags.
        _tags (dict): Dictionary of tags.

    Usage:
        >>> tags = Tags(commcell_object)
    """

    DEFAULT_TAGSET_ID: int = -1

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Method to initialize tags class

            Args:
                commcell_object (Commcell)  -- instance of commcell class
            Returns:
                Tags (object)               -- instance of tags class
        """
        self._commcell_object = commcell_object
        self._service = commcell_object._services
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._get_tags_url = self._service['GET_ENTITY_TAGS']
        self._create_tags_url = self._service['CREATE_ENTITY_TAGS']
        self._tags: dict = None

        self.refresh()

    def _get_tags(self) -> dict:
        """Gets all the tags created by a user

            Returns:
                tags: name-id pair of tags associated to a user
                    Example:
                        {
                            "tag1": 1,
                            "tag2": 3,
                            "tag3": 4
                        }
            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._get_tags_url)

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        resp = response.json()
        if not resp:
            raise SDKException('Response', '102')

        self.DEFAULT_TAGSET_ID = resp['tagSetInfo']['id']

        tag_dict: dict = {}
        if 'tags' in resp:
            for tag in resp.get("tags", []):
                tag_dict[tag.get("name").lower()] = tag.get("id")
            return tag_dict

    @property
    def all_tags(self) -> dict:
        """Returns a dictionary containing tags and their ID associated to a user

            Returns:
                tags: name-id pair of tags associated to a user
                    Example:
                        {
                            "tag1": 1,
                            "tag2": 3,
                            "tag3": 4
                        }
        """

        return self._tags

    def has_tag(self, tag_name: str) -> bool:
        """Checks if a tag exist for the logged-in user

            Args:
                tag_name (str): name of the tag to search

            Returns:
                bool: return True if tag is found, else returns false

            Raises:
                SDKException:
                    if type of the tag name argument is not string

        """
        if not isinstance(tag_name, str):
            raise SDKException('EntityTags', '101')

        return self._tags and tag_name.lower() in self._tags

    def get(self, name: str) -> 'Tag':
        """Returns an instance of the Tag class for the given tag name.

            Args:
                name (str): name of the tag to get the instance of

            Returns:
                object: instance of the Tag class for the given tag name

            Raises:
                SDKException:
                    if type of the tag name argument is not string

                    if no tag exists with the given name

        """
        if self.has_tag(name):
            name = name.lower()
            return Tag(self._commcell_object, name, self._tags[name])

        raise SDKException('EntityTags', '105')

    def refresh(self) -> None:
        """Refresh the list of tags"""
        self._tags = self._get_tags()

    def add(self, tag_name: str) -> 'Tag':
        """Method to add an entity tag

            Args:
                tag_name (str): entity tag name

            Returns:
                object: instance of the Tag class, for the newly created entity tag

            Raises:
                SDKException:
                    if tag_name is not a string

                    if response is not success

                    if error occurs while creating tag

            Usage:
                >>> tags.add('mytag')
        """
        if not isinstance(tag_name, str):
            raise SDKException('EntityTags', '101')

        payload = {
            'container': {
                'containerId': self.DEFAULT_TAGSET_ID
                },
            'tags': [
                {
                    'name': f"{tag_name}"
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._service['CREATE_ENTITY_TAGS'], payload)

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        response_json = response.json()
        if 'errList' in response_json:
            err_message = response_json.get('errLogMessage')
            err_code = response_json.get('errorCode')

            if err_code or err_message:
                raise SDKException('EntityTags', '103', err_message)

        self.refresh()
        return self.get(tag_name)

    def delete(self, tag_name: str) -> None:
        """Deletes the entity tag

        Args:
            tag_name (str): entity tag name to delete

        Raises:
            SDKException:
                if no tag exists with the given name

                if response is not success

                if error occurs while deleting tag

        Usage:
            >>> tags.delete('mytag')
        """
        if not self.has_tag(tag_name):
            raise SDKException("EntityTags", '105')

        tag_name = tag_name.lower()
        tag_id = self._tags[tag_name]

        flag, response = self._cvpysdk_object.make_request('DELETE', self._service['DELETE_ENTITY_TAGS'] % tag_id)

        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        resp = response.json()
        err_code: int = 0
        err_message: str = ""
        if resp:
            err_code = resp.get('errorCode', 0)
            err_message = resp.get('errorMessage', "")

        if err_code or err_message:
            raise SDKException("EntityTags", '102', f"Error: {err_message}")

        self.refresh()


class Tag:
    """Class for performing actions related to tag

    Attributes:
        _commcell_object (object): Instance of the Commcell class.
        _cvpysdk_object (object): Instance of the CVPYSDK class.
        _services (dict): Dictionary of service URLs.
        _update_response_ (callable): Method to update the response.
        _tag_name (str): Name of the entity tag.
        _tag_id (str): ID of the entity tag.

    Usage:
        >>> tag = Tag(commcell_object, 'mytag', '123')
    """

    def __init__(self, commcell_object: 'Commcell', tag_name: str, tag_id: str = None) -> None:
        """Initialise the Tag class instance.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

                tag_name            (str)       --  name of the entity tag

                tag_id              (str)       --  id of the entity tag
                    default: None

            Returns:
                object  -   instance of the tag class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._tag_name = tag_name

        if tag_id:
            self._tag_id = str(tag_id)
        else:
            self._tag_id = self._get_tag_id()

    def _get_tag_id(self) -> str:
        """Gets tag id based on the tag name"""
        tags = Tags(self._commcell_object)
        return tags.get(self._tag_name).tag_id

    @property
    def tag_id(self) -> str:
        """Returns tag id"""
        return self._tag_id

    @property
    def tag_name(self) -> str:
        """Returns tag name"""
        return self._tag_name
