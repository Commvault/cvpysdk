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

"""File for operating on an Azure Redis Subclient.

AzureRedisSubclient is the only class defined in this file.

AzureRedisSubclient:  Derived class from CloudAppsSubclient Base class, representing an
                      Azure Redis Cloud Apps subclient, and to perform operations on
                      that subclient.

AzureRedisSubclient:

    _get_subclient_properties()         --  Gets the properties of the Azure Redis subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the Azure Redis subclient

    content                             --  Gets/sets content as plain resource group path strings

    _set_content()                      --  Converts resource group path strings to CloudDBEntity XML dicts
                                          and persists

    _build_content_item()               --  Wraps a resource group path in CloudDBEntity XML format

    _parse_resource_group_name()        --  Extracts a resource group name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore Azure Redis data from the specified backup

"""
import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class AzureRedisSubclient(CloudAppsSubclient):
    """
    Represents an Azure Redis Cloud Apps subclient for backup and restore operations.

    Content format (user-facing):
        Content is represented as a List[str] of plain resource group names,
        e.g. ["resource-group-1", "resource-group-2"]. The SDK handles all XML wrapping
        (CloudDBEntity format) required by the underlying API internally.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(resource_group: str) -> dict:
        """Wrap a plain resource group name in the CloudDBEntity XML format expected by the API.

        Args:
            resource_group: Plain Azure resource group name, e.g. "ymidha-redis".

        Returns:
            dict: A content path dict {"path": "<CloudDBEntity>...</CloudDBEntity>"}.

        #ai-gen-doc
        """
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{resource_group}</name>'
            f'<path>/{resource_group}</path>'
            f'<displayName>{resource_group}</displayName>'
            f'<type>1</type>'
            f'<workloadObjectType>1</workloadObjectType>'
            f'<isContainer>true</isContainer>'
            f'</children></CloudDBEntity>'
        )
        return {"path": xml}

    @staticmethod
    def _parse_resource_group_name(path_dict: dict) -> Optional[str]:
        """Extract the plain resource group name from a CloudDBEntity XML path dict.

        Args:
            path_dict: A content item dict returned by the API, containing
                       the CloudDBEntity XML string under the "path" key.

        Returns:
            The resource group name string, or None if the XML cannot be parsed.

        #ai-gen-doc
        """
        xml = path_dict.get("path", "")
        match = re.search(r'<name>(.*?)</name>', xml)
        if match:
            return match.group(1)
        return None

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the AzureRedis subclient.

        #ai-gen-doc
        """
        super(AzureRedisSubclient, self)._get_subclient_properties()
        self._azure_redis_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the AzureRedis subclient.

        Returns:
            dict: A dictionary containing all properties of the AzureRedis subclient.

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
                "content": self._azure_redis_content
            }
        }
        return subclient_json


    @property
    def content(self) -> List[str]:
        """Get the subclient content as a list of plain resource group names.

        Returns:
            List of resource group name strings (e.g. ["resource-group-1", "resource-group-2"]).

        #ai-gen-doc
        """
        return [
            self._parse_resource_group_name(item)
            for item in self._azure_redis_content
            if self._parse_resource_group_name(item) is not None
        ]

    @content.setter
    def content(self, value: List[str]) -> None:
        """Set the subclient content from a list of plain resource group names.

        Wraps each resource group name in the CloudDBEntity XML format required by the API,
        then persists the wrapped content to the CommCell.

        Args:
            value: List of plain resource group name strings (e.g. ["resource-group-1"]).

        Raises:
            SDKException: If setting content fails.

        #ai-gen-doc
        """
        if not isinstance(value, list):
            raise SDKException('Subclient', '101', 'Content must be a list of resource group names')

        wrapped_content = [self._build_content_item(rg) for rg in value]
        self._set_content(wrapped_content)

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this subclient's instance backups.

        Delegates to the parent instance's browse method.

        Args:
            *args: Optional positional arguments passed to the instance browse method.
            **kwargs: Optional keyword arguments passed to the instance browse method.

        Returns:
            dict: Browse results from the instance.

        #ai-gen-doc
        """
        return self._backupset_object._instance_object.browse(*args, **kwargs)

    def restore(
            self,
            paths: Optional[List[str]] = None,
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs: Any
    ) -> Job:
        """Restore Azure Redis data from the specified backup.

        Args:
            paths: List of resource group paths to restore (e.g. ["/resource-group-1"]).
                   Paths should start with '/' if not already prefixed.
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to the parent restore method.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = subclient.restore(paths=["/resource-group-1"], overwrite=True)

        #ai-gen-doc
        """
        if paths is None:
            resource_groups = self.content
            if not resource_groups:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in subclient; cannot derive restore paths'
                )
            paths = [f'/{name}' for name in resource_groups]

        return super(AzureRedisSubclient, self).restore(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
