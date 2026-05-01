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

"""File for operating on a Pinecone Subclient.

PineConeSubclient is the only class defined in this file.

PineConeSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                    Pinecone vector database subclient, and to perform operations on that subclient

PineConeSubclient:

    _get_subclient_properties()         --  gets the properties of Pinecone Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of Pinecone Subclient

    content()                           --  gets the content of the subclient

    _set_content()                      --  sets the content of the subclient

    update_content_xml()                --  overwrites subclient content with a pre-built CloudDBEntity XML string

    browse()                            --  Browse and returns the content of this subclient's instance backups

    restore()                           --  Restores Pinecone data from the specified source and restore options

"""
from __future__ import unicode_literals
from typing import Any, Dict, Optional, List

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException


class PineConeSubclient(CloudAppsSubclient):
    """
    Represents a Pinecone vector database subclient for managing and operating on Pinecone resources.

    This class extends the CloudAppsSubclient base class and provides specialized methods
    for interacting with Pinecone vector database subclients. It enables users to retrieve and set
    subclient properties, manage subclient content, browse available data, and perform
    restore operations to specified destinations.

    Key Features:
        - Retrieve subclient properties and their JSON representations
        - Set and manage subclient content
        - Property-based access and modification of subclient content
        - Browse data within the subclient
        - Restore data to a specified destination with customizable options

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the Pinecone subclient.

        This method fetches and stores configuration details and settings
        related to the Pinecone subclient, including content information.

        Example:
            >>> subclient = PineConeSubclient(backupset_object, 'default')
            >>> subclient._get_subclient_properties()
            >>> # The subclient's properties are now loaded

        #ai-gen-doc
        """
        super(PineConeSubclient, self)._get_subclient_properties()

        # Initialize Pinecone-specific content
        if 'content' in self._subclient_properties:
            self._pinecone_content = self._subclient_properties.get('content', [])
        else:
            self._pinecone_content = []

    def _get_subclient_properties_json(self) -> dict:
        """Retrieve the properties JSON for the Pinecone Subclient.

        Returns:
            dict: A dictionary containing all properties of the Pinecone Subclient.

        Example:
            >>> subclient = PineConeSubclient(backupset_object, 'default')
            >>> properties = subclient._get_subclient_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary with subclient property details

        #ai-gen-doc
        """
        subclient_json = {
            "subClientProperties": {
                "proxyClient": self._proxyClient,
                "subClientEntity": self._subClientEntity,
                "commonProperties": self._commonProperties,
                "cloudAppsSubClientProp": {
                    "instanceType": self._backupset_object._instance_object.ca_instance_type
                },
                "content": self._pinecone_content
            }
        }

        # Add plan entity if storage policy is set
        if hasattr(self, 'storage_policy') and self.storage_policy:
            subclient_json["subClientProperties"]["planEntity"] = {
                "planName": self.storage_policy
            }

        return subclient_json

    def _set_content(self, content: Optional[List[str]] = None) -> None:
        """Set the subclient content for the PineConeSubclient.

        Args:
            content: Optional list of content paths/items for the subclient. 
                    If not provided, content will be set to an empty list.

        Example:
            >>> subclient = PineConeSubclient(backupset_object, 'default')
            >>> subclient._set_content(['/index1', '/index2'])
            >>> # The subclient content is now set to the specified paths

        #ai-gen-doc
        """
        if content is not None:
            self._pinecone_content = content
        else:
            self._pinecone_content = []

        self._set_subclient_properties("_pinecone_content", self._pinecone_content)

    @property
    def content(self) -> List[str]:
        """Get the Pinecone content associated with this subclient.

        Returns:
            list: A list of content paths/items configured for this subclient.

        Example:
            >>> subclient = PineConeSubclient(backupset_object, 'default')
            >>> content_info = subclient.content
            >>> print(f"Subclient content: {content_info}")
            >>> # Output: ['/index1', '/index2']

        #ai-gen-doc
        """
        return self._pinecone_content

    @content.setter
    def content(self, subclient_content: List[str]) -> None:
        """Set the content for the Pinecone Subclient.

        This method validates and sets the content list for the Pinecone subclient.
        The provided content should be a non-empty list of paths or items to back up.

        Args:
            subclient_content: A list containing the content items to add to the subclient.

        Raises:
            SDKException: If the subclient_content is not a list or if it is empty.

        Example:
            >>> subclient = PineConeSubclient(backupset_object, 'default')
            >>> new_content = ['/index1', '/index2']
            >>> subclient.content = new_content
            >>> # The subclient content is now updated with the provided paths

        #ai-gen-doc
        """
        if isinstance(subclient_content, list) and subclient_content:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a non-empty list'
            )

    def update_content_xml(self, cloud_db_entity_xml: str) -> None:
        """Overwrite subclient content using a pre-built CloudDBEntity XML string.

        Args:
            cloud_db_entity_xml (str): Fully formed CloudDBEntity XML to set as content.

        Raises:
            SDKException: If the API request fails.
        """
        payload = {
            "subClientProperties": {
                "contentOperationType": "OVERWRITE",
                "content": [{"path": cloud_db_entity_xml}],
                "cloudAppsSubClientProp": {
                    "instanceType": self._backupset_object._instance_object.ca_instance_type
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._SUBCLIENT, payload
        )

        if not flag:
            raise SDKException(
                'Subclient', '102',
                f'Failed to update subclient content: {response}'
            )
