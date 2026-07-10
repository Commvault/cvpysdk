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

"""File for operating on a GCP Memorystore Subclient.

GcpMemorystoreSubclient is the only class defined in this file.

GcpMemorystoreSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                           GCP Memorystore Cloud Apps subclient, and to perform operations on
                           that subclient.

GcpMemorystoreSubclient:

    _get_subclient_properties()         --  Gets the properties of the GCP Memorystore subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the GCP Memorystore subclient

    content                             --  Gets/sets content as plain region path strings

    _set_content()                      --  Converts region path strings to CloudDBEntity XML dicts
                                          and persists

    _build_content_item()               --  Wraps a region path in CloudDBEntity XML format

    _parse_region_name()                --  Extracts a region name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore GCP Memorystore data from the specified backup

"""
import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class GcpMemorystoreSubclient(CloudAppsSubclient):
    """
    Represents a GCP Memorystore Cloud Apps subclient for backup and restore operations.

    Content format (user-facing):
        Content is represented as a List[str] of plain region names,
        e.g. ["us-central1", "us-east1"]. The SDK handles all XML wrapping
        (CloudDBEntity format) required by the underlying API internally.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(region_name: str) -> dict:
        """Wrap a plain region name in the CloudDBEntity XML format expected by the API.

        Args:
            region_name: Plain GCP region name, e.g. "us-central1".

        Returns:
            dict: A content path dict {"path": "<CloudDBEntity>...</CloudDBEntity>"}.

        #ai-gen-doc
        """
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{region_name}</name>'
            f'<path>/{region_name}</path>'
            f'<displayName>{region_name}</displayName>'
            f'<isContainer>true</isContainer>'
            f'</children></CloudDBEntity>'
        )
        return {"path": xml}

    @staticmethod
    def _parse_region_name(path_dict: dict) -> Optional[str]:
        """Extract the plain region name from a CloudDBEntity XML path dict.

        Args:
            path_dict: A content item dict returned by the API, containing
                       the CloudDBEntity XML string under the "path" key.

        Returns:
            The region name string, or None if the XML cannot be parsed.

        #ai-gen-doc
        """
        match = re.search(r'<name>([^<]+)</name>', path_dict.get('path', ''))
        return match.group(1) if match else None

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the GCP Memorystore subclient.

        #ai-gen-doc
        """
        super(GcpMemorystoreSubclient, self)._get_subclient_properties()
        self._gcp_memorystore_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the GCP Memorystore subclient.

        Returns:
            dict: A dictionary containing all properties of the GCP Memorystore subclient
            suitable for a POST to the subclient update endpoint.

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
                "content": self._gcp_memorystore_content
            }
        }
        return subclient_json

    def _set_content(self, region_names: Optional[List[str]] = None) -> None:
        """Convert plain region names to CloudDBEntity XML dicts and persist via API.

        Args:
            region_names: List of plain GCP region name strings.
                          Pass None or an empty list to clear content.

        #ai-gen-doc
        """
        self._gcp_memorystore_content = [
            self._build_content_item(name) for name in (region_names or [])
        ]
        self._set_subclient_properties("content", self._gcp_memorystore_content)

    @property
    def content(self) -> List[str]:
        """Get the GCP region names configured as content for this subclient.

        Returns:
            list: A list of plain region name strings, e.g. ``["us-central1"]``.
            Items that cannot be parsed from the stored XML are omitted.

        #ai-gen-doc
        """
        names = [self._parse_region_name(item) for item in self._gcp_memorystore_content]
        return [n for n in names if n is not None]

    @content.setter
    def content(self, region_names: List[str]) -> None:
        """Set the GCP regions to back up for this GCP Memorystore subclient.

        Args:
            region_names: A non-empty list of plain GCP region name strings.
                The SDK wraps these into the CloudDBEntity XML format required
                by the API automatically.

        Raises:
            SDKException: If region_names is not a non-empty list of strings.

        #ai-gen-doc
        """
        if isinstance(region_names, list) and region_names and all(isinstance(n, str) for n in region_names):
            self._set_content(region_names=region_names)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient content should be a non-empty list of GCP region name strings'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this GCP Memorystore subclient's instance backups.

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
        """Restore GCP Memorystore data from the specified backup.

        Args:
            paths: List of region paths to restore (e.g. ["/us-central1"]).
                   If None, paths are derived from the subclient's configured content.
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If no content is found and no paths provided.
        """
        if paths is None:
            region_names = self.content
            if not region_names:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in subclient; cannot derive restore paths'
                )
            paths = [f'/{name}' for name in region_names]

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
