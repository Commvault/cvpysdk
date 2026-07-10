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

"""File for operating on a HubSpot Subclient.

HubSpotSubclient is the only class defined in this file.

HubSpotSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                   HubSpot Cloud Apps subclient, and to perform operations on that subclient

HubSpotSubclient:

    _get_subclient_properties()         --  Gets the properties of the HubSpot subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the HubSpot subclient

    content                             --  Gets/sets content as plain HubSpot module name strings

    _set_content()                      --  Converts module name strings to XML dicts and persists

    _build_content_item()               --  Wraps a module name in CloudDBEntity XML format

    _build_content_xml()                --  Builds a single CloudDBEntity XML with all modules as children

    _parse_module_name()                --  Extracts a module name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore HubSpot data from the specified backup

"""
import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class HubSpotSubclient(CloudAppsSubclient):
    """
    Represents a HubSpot Cloud Apps subclient for managing backup and restore operations.

    This class extends the CloudAppsSubclient base class and provides specialized methods
    for interacting with HubSpot subclients.

    Content format (user-facing):
        Content is represented as a List[str] of plain HubSpot module names,
        e.g. ["CRM", "Marketing", "Sales"]. The SDK handles all XML wrapping
        (CloudDBEntity format) required by the underlying API internally.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(module_name: str) -> dict:
        """Wrap a plain HubSpot module name in the CloudDBEntity XML format expected by the API.

        Args:
            module_name: Plain HubSpot module name, e.g. "CRM".

        Returns:
            dict: A content path dict {"path": "<CloudDBEntity>...</CloudDBEntity>"}.

        #ai-gen-doc
        """
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{module_name}</name>'
            f'<path>/{module_name}</path>'
            f'<displayName>{module_name}</displayName>'
            f'<isContainer>true</isContainer>'
            f'</children></CloudDBEntity>'
        )
        return {"path": xml}

    @staticmethod
    def _build_content_xml(module_names: List[str]) -> str:
        """Build a single CloudDBEntity XML string with all module names as children.

        Combines multiple module names into one "<CloudDBEntity>" element with a
        "<children>" block per module, which is the format expected by the HubSpot
        instance creation API.

        Args:
            module_names: List of plain HubSpot module name strings.

        Returns:
            str: A single XML string, e.g.::

                <CloudDBEntity>
                  <children><name>CRM</name>...</children>
                  <children><name>Marketing</name>...</children>
                </CloudDBEntity>

        #ai-gen-doc
        """
        children = ''.join(
            f'<children>'
            f'<name>{m}</name>'
            f'<path>/{m}</path>'
            f'<displayName>{m}</displayName>'
            f'<isContainer>true</isContainer>'
            f'</children>'
            for m in module_names
        )
        return f'<CloudDBEntity>{children}</CloudDBEntity>'

    @staticmethod
    def _parse_module_name(path_dict: dict) -> Optional[str]:
        """Extract the plain module name from a CloudDBEntity XML path dict.

        Args:
            path_dict: A content item dict returned by the API, containing
                       the CloudDBEntity XML string under the "path" key.

        Returns:
            The module name string, or None if the XML cannot be parsed.

        #ai-gen-doc
        """
        match = re.search(r'<name>([^<]+)</name>', path_dict.get('path', ''))
        return match.group(1) if match else None

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the HubSpot subclient.

        Fetches and stores configuration details including the content list
        from the subclient properties response.

        #ai-gen-doc
        """
        super(HubSpotSubclient, self)._get_subclient_properties()
        self._hubspot_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the HubSpot subclient.

        Returns:
            dict: A dictionary containing all properties of the HubSpot subclient
            suitable for a POST to the subclient update endpoint.

        #ai-gen-doc
        """
        subclient_json = {
            "subClientProperties": {
                "subClientEntity": self._subClientEntity,
                "commonProperties": self._commonProperties,
                "cloudAppsSubClientProp": {
                    "instanceType": self._backupset_object._instance_object.ca_instance_type
                },
                "content": self._hubspot_content
            }
        }
        return subclient_json

    def _set_content(self, module_names: Optional[List[str]] = None) -> None:
        """Convert plain module names to CloudDBEntity XML dicts and persist via API.

        Args:
            module_names: List of plain HubSpot module name strings.
                          Pass None or an empty list to clear content.

        #ai-gen-doc
        """
        self._hubspot_content = [
            self._build_content_item(name) for name in (module_names or [])
        ]
        self._set_subclient_properties("content", self._hubspot_content)

    @property
    def content(self) -> List[str]:
        """Get the HubSpot module names configured as content for this subclient.

        Returns:
            list: A list of plain module name strings, e.g. ``["CRM", "Marketing"]``.

        #ai-gen-doc
        """
        names = [self._parse_module_name(item) for item in self._hubspot_content]
        return [n for n in names if n is not None]

    @content.setter
    def content(self, module_names: List[str]) -> None:
        """Set the HubSpot modules to back up for this subclient.

        Args:
            module_names: A non-empty list of plain HubSpot module name strings.

        Raises:
            SDKException: If module_names is not a non-empty list of strings.

        #ai-gen-doc
        """
        if isinstance(module_names, list) and module_names and all(isinstance(n, str) for n in module_names):
            self._set_content(module_names=module_names)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient content should be a non-empty list of HubSpot module name strings'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this HubSpot subclient's instance backups.

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
        """Restore HubSpot data from the specified backup.

        Submits an in-place restore job for the specified paths.

        If `paths` is not provided, the restore paths are automatically derived from
        the subclient's configured content (module names).

        Args:
            paths: List of paths to restore (e.g. ["/CRM", "/Marketing"]).
                   If None, paths are derived from the subclient's content.
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to `restore_in_place`.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or no paths can be resolved.

        #ai-gen-doc
        """
        if paths is None:
            module_names = self.content
            if not module_names:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in subclient; cannot derive restore paths'
                )
            paths = [f'/{name}' for name in module_names]

        # Set the subclient entity on the instance so the restore request
        # includes the subclientId — required by JobManager to locate backup data.
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
