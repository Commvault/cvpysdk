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

"""File for operating on a ClickHouse Subclient.

ClickHouseSubclient is the only class defined in this file.

ClickHouseSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                      ClickHouse Cloud Apps subclient, and to perform operations on that subclient

ClickHouseSubclient:

    _get_subclient_properties()         --  Gets the properties of the ClickHouse subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the ClickHouse subclient

    content                             --  Gets/sets content as plain database name strings

    _set_content()                      --  Converts DB name strings to XML dicts and persists

    _build_content_item()               --  Wraps a DB name in CloudDBEntity XML format

    _parse_db_name()                    --  Extracts a DB name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore ClickHouse data from the specified backup

"""
import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class ClickHouseSubclient(CloudAppsSubclient):
    """
    Represents a ClickHouse Cloud Apps subclient for managing backup and restore operations.

    Content format (user-facing):
        Content is represented as a List[str] of plain database names,
        e.g. ["my_db", "another_db"]. The SDK handles all XML wrapping
        (CloudDBEntity format) required by the underlying API internally.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(db_name: str) -> dict:
        """Wrap a plain database name in the CloudDBEntity XML format expected by the API.

        Args:
            db_name: Plain ClickHouse database name, e.g. "my_db".

        Returns:
            dict: A content path dict {"path": "<CloudDBEntity>...</CloudDBEntity>"}.

        #ai-gen-doc
        """
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{db_name}</name>'
            f'<path>/{db_name}</path>'
            f'<displayName>{db_name}</displayName>'
            f'<type>1</type>'
            f'<workloadObjectType>1</workloadObjectType>'
            f'</children></CloudDBEntity>'
        )
        return {"path": xml}

    @staticmethod
    def _build_content_xml(db_name: str) -> str:
        """Build a CloudDBEntity XML string for a single database.

        Args:
            db_name: Plain ClickHouse database name string.

        Returns:
            str: A CloudDBEntity XML string.

        #ai-gen-doc
        """
        return (
            f'<CloudDBEntity><children>'
            f'<name>{db_name}</name>'
            f'<path>/{db_name}</path>'
            f'<displayName>{db_name}</displayName>'
            f'<type>1</type>'
            f'<workloadObjectType>1</workloadObjectType>'
            f'</children></CloudDBEntity>'
        )

    @staticmethod
    def _parse_db_name(path_dict: dict) -> Optional[str]:
        """Extract the plain database name from a CloudDBEntity XML path dict.

        Args:
            path_dict: A content item dict returned by the API, containing
                       the CloudDBEntity XML string under the "path" key.

        Returns:
            The database name string, or None if the XML cannot be parsed.

        #ai-gen-doc
        """
        match = re.search(r'<name>([^<]+)</name>', path_dict.get('path', ''))
        return match.group(1) if match else None

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the ClickHouse subclient.

        #ai-gen-doc
        """
        super(ClickHouseSubclient, self)._get_subclient_properties()
        self._clickhouse_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the ClickHouse subclient.

        Returns:
            dict: A dictionary containing all properties of the ClickHouse subclient.

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
                "content": self._clickhouse_content
            }
        }
        return subclient_json

    def _set_content(self, db_names: Optional[List[str]] = None) -> None:
        """Convert plain database names to CloudDBEntity XML dicts and persist via API.

        Args:
            db_names: List of plain ClickHouse database name strings.
                      Pass None or an empty list to clear content.

        #ai-gen-doc
        """
        self._clickhouse_content = [
            self._build_content_item(name) for name in (db_names or [])
        ]
        self.update_properties(self._get_subclient_properties_json())

    @property
    def content(self) -> List[str]:
        """Get the list of backed-up database names.

        Returns:
            List of plain database name strings.

        #ai-gen-doc
        """
        return [
            self._parse_db_name(item)
            for item in self._clickhouse_content
            if self._parse_db_name(item) is not None
        ]

    @content.setter
    def content(self, db_names: List[str]) -> None:
        """Set the list of databases to back up.

        Args:
            db_names: List of plain ClickHouse database name strings.

        #ai-gen-doc
        """
        self._set_content(db_names)

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this ClickHouse subclient's backups.

        Returns:
            dict: A dictionary of browsed content.

        #ai-gen-doc
        """
        return super(ClickHouseSubclient, self).browse(*args, **kwargs)

    def restore(
            self,
            paths: Optional[List[str]] = None,
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ) -> "Job":
        """Restore ClickHouse data from the specified backup.

        Args:
            paths: List of database paths to restore.
                   Defaults to all content if None.
            overwrite: Whether to overwrite existing data. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0.
            **kwargs: Additional arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        #ai-gen-doc
        """
        if paths is None:
            paths = [f'/{db}' for db in self.content]
        return self._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
