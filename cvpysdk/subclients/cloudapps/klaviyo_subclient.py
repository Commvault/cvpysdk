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

"""File for operating on a Klaviyo Subclient.

KlaviyoSubclient is the only class defined in this file.

KlaviyoSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                   Klaviyo Cloud Apps subclient, and to perform operations on that subclient

KlaviyoSubclient:

    _get_subclient_properties()         --  Gets the properties of the Klaviyo subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the Klaviyo subclient

    content                             --  Gets/sets content as plain content name strings

    _set_content()                      --  Converts content name strings to XML dicts and persists

    _build_content_item()               --  Wraps a content name in CloudDBEntity XML format

    _parse_content_name()               --  Extracts a content name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore Klaviyo data from the specified backup

"""
import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class KlaviyoSubclient(CloudAppsSubclient):
    """
    Represents a Klaviyo Cloud Apps subclient for managing backup and restore operations.

    This class extends the CloudAppsSubclient base class and provides specialized methods
    for interacting with Klaviyo subclients.

    Key Features:
        - Retrieve subclient properties and their JSON representations
        - Set and manage subclient content using plain content name strings
        - Property-based access and modification of subclient content
        - Browse data within the subclient
        - Restore data to the original location with customizable options

    Content format (user-facing):
        Content is represented as a List[str] of plain content names (profiles, lists, etc.),
        e.g. ["profiles", "lists"]. The SDK handles all XML wrapping (CloudDBEntity format)
        required by the underlying API internally.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(content_name: str) -> dict:
        """Wrap a plain content name in the CloudDBEntity XML format expected by the API.

        Args:
            content_name: Plain Klaviyo content name, e.g. "profiles".

        Returns:
            dict: A content path dict {"path": "<CloudDBEntity>...</CloudDBEntity>"}.

        #ai-gen-doc
        """
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{content_name}</name>'
            f'<path>/{content_name}</path>'
            f'<displayName>{content_name}</displayName>'
            f'<type>1</type>'
            f'<workloadObjectType>1</workloadObjectType>'
            f'</children></CloudDBEntity>'
        )
        return {"path": xml}

    @staticmethod
    def _build_content_xml(content_names: List[str]) -> str:
        """Build a single CloudDBEntity XML string with all content names as children.

        Combines multiple content names into one "<CloudDBEntity>" element
        with a "<children>" block per content item, which is the format expected
        by the Klaviyo instance creation API.

        Args:
            content_names: List of plain Klaviyo content name strings.

        Returns:
            str: A single XML string, e.g.::

                <CloudDBEntity>
                  <children><name>profiles</name>...</children>
                  <children><name>lists</name>...</children>
                </CloudDBEntity>

        #ai-gen-doc
        """
        children = ''.join(
            f'<children>'
            f'<name>{name}</name>'
            f'<path>/{name}</path>'
            f'<displayName>{name}</displayName>'
            f'<type>1</type>'
            f'<workloadObjectType>1</workloadObjectType>'
            f'</children>'
            for name in content_names
        )
        return f'<CloudDBEntity>{children}</CloudDBEntity>'

    @staticmethod
    def _parse_content_name(path_dict: dict) -> Optional[str]:
        """Extract the plain content name from a CloudDBEntity XML path dict.

        Args:
            path_dict: A content item dict returned by the API, containing
                       the CloudDBEntity XML string under the "path" key.

        Returns:
            The content name string, or None if the XML cannot be parsed.

        #ai-gen-doc
        """
        match = re.search(r'<name>([^<]+)</name>', path_dict.get('path', ''))
        return match.group(1) if match else None

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the Klaviyo subclient.

        Fetches and stores configuration details including the content list
        from the subclient properties response. The raw API content (XML path
        dicts) is stored internally; the public "content" property exposes
        plain content name strings.

        Example:
            >>> subclient._get_subclient_properties()

        #ai-gen-doc
        """
        super(KlaviyoSubclient, self)._get_subclient_properties()
        self._klaviyo_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the Klaviyo subclient.

        Returns:
            dict: A dictionary containing all properties of the Klaviyo subclient
            suitable for a POST to the subclient update endpoint.

        Example:
            >>> properties = subclient._get_subclient_properties_json()

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
                "content": self._klaviyo_content
            }
        }
        return subclient_json

    def _set_content(self, content_names: Optional[List[str]] = None) -> None:
        """Convert plain content names to CloudDBEntity XML dicts and persist via API.

        Args:
            content_names: List of plain Klaviyo content name strings.
                           Pass None or an empty list to clear content.

        Example:
            >>> subclient._set_content(["profiles", "lists"])

        #ai-gen-doc
        """
        self._klaviyo_content = [
            self._build_content_item(name) for name in (content_names or [])
        ]
        self._set_subclient_properties("content", self._klaviyo_content)

    @property
    def content(self) -> List[str]:
        """Get the Klaviyo content names configured for this subclient.

        Returns:
            list: A list of plain content name strings, e.g. ``["profiles", "lists"]``.
            Items that cannot be parsed from the stored XML are omitted.

        Example:
            >>> print(subclient.content)
            ['profiles', 'lists']

        #ai-gen-doc
        """
        names = [self._parse_content_name(item) for item in self._klaviyo_content]
        return [n for n in names if n is not None]

    @content.setter
    def content(self, content_names: List[str]) -> None:
        """Set the content items to back up for this Klaviyo subclient.

        Args:
            content_names: A non-empty list of plain Klaviyo content name strings.
                The SDK wraps these into the CloudDBEntity XML format required
                by the API automatically.

        Raises:
            SDKException: If content_names is not a non-empty list of strings.

        Example:
            >>> subclient.content = ["profiles", "lists"]

        #ai-gen-doc
        """
        if isinstance(content_names, list) and content_names and all(isinstance(n, str) for n in content_names):
            self._set_content(content_names=content_names)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient content should be a non-empty list of content name strings'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this Klaviyo subclient's instance backups.

        Delegates to the parent instance's browse method.

        Args:
            *args: Optional positional arguments passed to the instance browse method.
            **kwargs: Optional keyword arguments passed to the instance browse method.

        Returns:
            dict: Browse results from the instance.

        Example:
            >>> result = subclient.browse()

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
        """Restore Klaviyo data from the specified backup.

        Submits an in-place restore job for the specified paths to restore Klaviyo
        content from a backup to the original location.

        If `paths` is not provided, the restore paths are automatically derived from
        the subclient's configured content (content names).

        Args:
            paths: List of paths to restore (e.g. ["/profiles"] or ["/lists"]).
                   If None, paths are derived from the subclient's content.
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to `restore_in_place`.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails, parameters are invalid, or
                          no paths can be resolved.

        Example:
            >>> job = subclient.restore(paths=["/profiles"], overwrite=True)

        #ai-gen-doc
        """
        if paths is None:
            content_names = self.content
            if not content_names:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in subclient; cannot derive restore paths'
                )
            paths = [f'/{name}' for name in content_names]

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
