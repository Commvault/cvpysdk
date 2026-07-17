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

"""File for operating on a ServiceNow Subclient.

ServiceNowSubclient is the only class defined in this file.

ServiceNowSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                      ServiceNow Cloud Apps subclient, and to perform operations on that subclient.

ServiceNowSubclient:

    _get_subclient_properties()         --  Gets the properties of the ServiceNow subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the ServiceNow subclient

    content                             --  Gets/sets content as plain ServiceNow table name strings

    _set_content()                      --  Converts table name strings to XML dicts and persists

    _build_content_item()               --  Wraps a table name in CloudDBEntity XML format

    _build_content_xml()                --  Builds a single CloudDBEntity XML with all tables as children

    _parse_table_name()                 --  Extracts a table name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore ServiceNow data from the specified backup

"""
import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class ServiceNowSubclient(CloudAppsSubclient):
    """
    Represents a ServiceNow Cloud Apps subclient for managing backup and restore operations.

    This class extends the CloudAppsSubclient base class and provides specialized methods
    for interacting with ServiceNow subclients.

    Content format (user-facing):
        Content is represented as a List[str] of plain ServiceNow table names,
        e.g. ["incident", "change_request", "cmdb_ci"]. The SDK handles all XML wrapping
        (CloudDBEntity format) required by the underlying API internally.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(table_name: str) -> dict:
        """Wrap a plain ServiceNow table name in the CloudDBEntity XML format expected by the API.

        Args:
            table_name: Plain ServiceNow table name, e.g. "incident".

        Returns:
            dict: A content path dict {"path": "<CloudDBEntity>...</CloudDBEntity>"}.

        #ai-gen-doc
        """
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{table_name}</name>'
            f'<path>/{table_name}</path>'
            f'<displayName>{table_name}</displayName>'
            f'<isContainer>true</isContainer>'
            f'</children></CloudDBEntity>'
        )
        return {"path": xml}

    @staticmethod
    def _build_content_xml(table_names: List[str]) -> str:
        """Build a single CloudDBEntity XML string with all table names as children.

        Combines multiple table names into one "<CloudDBEntity>" element with a
        "<children>" block per table, which is the format expected by the ServiceNow
        instance creation API.

        Args:
            table_names: List of plain ServiceNow table name strings.

        Returns:
            str: A single XML string, e.g.::

                <CloudDBEntity>
                  <children><name>incident</name>...</children>
                  <children><name>change_request</name>...</children>
                </CloudDBEntity>

        #ai-gen-doc
        """
        children = ''.join(
            f'<children>'
            f'<name>{t}</name>'
            f'<path>/{t}</path>'
            f'<displayName>{t}</displayName>'
            f'<isContainer>true</isContainer>'
            f'</children>'
            for t in table_names
        )
        return f'<CloudDBEntity>{children}</CloudDBEntity>'

    @staticmethod
    def _parse_table_name(path_dict: dict) -> Optional[str]:
        """Extract the plain table name from a CloudDBEntity XML path dict.

        Args:
            path_dict: A content item dict returned by the API, containing
                       the CloudDBEntity XML string under the "path" key.

        Returns:
            The table name string, or None if the XML cannot be parsed.

        #ai-gen-doc
        """
        match = re.search(r'<name>([^<]+)</name>', path_dict.get('path', ''))
        return match.group(1) if match else None

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the ServiceNow subclient.

        Fetches and stores configuration details including the content list
        from the subclient properties response.

        #ai-gen-doc
        """
        super(ServiceNowSubclient, self)._get_subclient_properties()
        self._servicenow_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the ServiceNow subclient.

        Returns:
            dict: A dictionary containing all properties of the ServiceNow subclient
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
                "content": self._servicenow_content
            }
        }
        return subclient_json

    def _set_content(self, table_names: Optional[List[str]] = None) -> None:
        """Convert plain table names to CloudDBEntity XML dicts and persist via API.

        Args:
            table_names: List of plain ServiceNow table name strings.
                         Pass None or an empty list to clear content (backup all tables).

        #ai-gen-doc
        """
        self._servicenow_content = [
            self._build_content_item(name) for name in (table_names or [])
        ]
        self._set_subclient_properties("content", self._servicenow_content)

    @property
    def content(self) -> List[str]:
        """Get the ServiceNow table names configured as content for this subclient.

        Returns:
            list: A list of plain table name strings, e.g. ``["incident", "change_request"]``.

        #ai-gen-doc
        """
        names = [self._parse_table_name(item) for item in self._servicenow_content]
        return [n for n in names if n is not None]

    @content.setter
    def content(self, table_names: List[str]) -> None:
        """Set the ServiceNow tables to back up for this subclient.

        Args:
            table_names: List of plain ServiceNow table name strings.
                         Pass an empty list to revert to all-tables mode.

        #ai-gen-doc
        """
        self._set_content(table_names)

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
        """Restore data from backup via in-place restore.

        If *paths* is None, the restore covers the entire ServiceNow instance
        (i.e., all configured tables). When specific table names are needed,
        pass them as ``["/incident", "/change_request"]``.

        Args:
            paths: Optional list of ServiceNow table paths to restore.
                   If None, paths are derived from the subclient content, or
                   the full instance is restored when content is empty (all tables).
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        #ai-gen-doc
        """
        if paths is None:
            table_names = self.content
            if table_names:
                paths = [f'/{name}' for name in table_names]
            else:
                # Empty content means all tables — restore with root path
                paths = ['/']

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
