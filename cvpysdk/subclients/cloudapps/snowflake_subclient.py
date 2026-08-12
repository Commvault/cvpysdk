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

"""File for operating on a Snowflake Subclient.

SnowflakeSubclient is the only class defined in this file.

SnowflakeSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                     Snowflake Cloud Apps subclient, and to perform operations on that subclient

SnowflakeSubclient:

    _get_subclient_properties()         --  Gets the properties of the Snowflake subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the Snowflake subclient

    content                             --  Gets/sets content as plain database name strings

    _set_content()                      --  Converts DB name strings to XML dicts and persists

    _build_content_item()               --  Wraps a DB name in CloudDBEntity XML format

    _parse_db_name()                    --  Extracts a DB name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore Snowflake data from the specified backup

"""
import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class SnowflakeSubclient(CloudAppsSubclient):
    """
    Represents a Snowflake Cloud Apps subclient for managing backup and restore operations.

    This class extends the CloudAppsSubclient base class and provides specialized methods
    for interacting with Snowflake subclients.

    Key Features:
        - Retrieve subclient properties and their JSON representations
        - Set and manage subclient content using plain database name strings
        - Property-based access and modification of subclient content
        - Browse data within the subclient
        - Restore data to the original location with customizable options

    Content format (user-facing):
        Content is represented as a List[str] of plain database names,
        e.g. ["MY_DB", "ANOTHER_DB"]. The SDK handles all XML wrapping
        (CloudDBEntity format) required by the underlying API internally.
    """

    @staticmethod
    def _build_content_item(db_name: str) -> dict:
        """Wrap a plain database name in the CloudDBEntity XML format expected by the API.

        Args:
            db_name: Plain Snowflake database name, e.g. "MY_DB".

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
    def _build_content_xml(db_names: List[str]) -> str:
        """Build a single CloudDBEntity XML string with all DB names as children.

        Combines multiple database names into one "<CloudDBEntity>" element
        with a "<children>" block per database, which is the format expected
        by the Snowflake instance creation API.

        Args:
            db_names: List of plain Snowflake database name strings.

        Returns:
            str: A single XML string, e.g.::

                <CloudDBEntity>
                  <children><name>DB1</name>...</children>
                  <children><name>DB2</name>...</children>
                </CloudDBEntity>

        #ai-gen-doc
        """
        children = ''.join(
            f'<children>'
            f'<name>{db}</name>'
            f'<path>/{db}</path>'
            f'<displayName>{db}</displayName>'
            f'<type>1</type>'
            f'<workloadObjectType>1</workloadObjectType>'
            f'</children>'
            for db in db_names
        )
        return f'<CloudDBEntity>{children}</CloudDBEntity>'

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
        """Retrieve the properties specific to the Snowflake subclient.

        Fetches and stores configuration details including the content list
        from the subclient properties response. The raw API content (XML path
        dicts) is stored internally; the public "content" property exposes
        plain database name strings.

        Example:
            >>> subclient._get_subclient_properties()

        #ai-gen-doc
        """
        super(SnowflakeSubclient, self)._get_subclient_properties()
        self._snowflake_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the Snowflake subclient.

        Returns:
            dict: A dictionary containing all properties of the Snowflake subclient
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
                "content": self._snowflake_content
            }
        }
        return subclient_json

    def _set_content(self, db_names: Optional[List[str]] = None) -> None:
        """Convert plain database names to CloudDBEntity XML dicts and persist via API.

        Args:
            db_names: List of plain Snowflake database name strings.
                      Pass None or an empty list to clear content.

        Example:
            >>> subclient._set_content(["MY_DB", "ANOTHER_DB"])

        #ai-gen-doc
        """
        self._snowflake_content = [
            self._build_content_item(name) for name in (db_names or [])
        ]
        self._set_subclient_properties("content", self._snowflake_content)

    @property
    def content(self) -> List[str]:
        """Get the Snowflake database names configured as content for this subclient.

        Returns:
            list: A list of plain database name strings, e.g. ``["MY_DB", "ANOTHER_DB"]``.
            Items that cannot be parsed from the stored XML are omitted.

        Example:
            >>> print(subclient.content)
            ['TC_00001_AUTODB_10']

        #ai-gen-doc
        """
        names = [self._parse_db_name(item) for item in self._snowflake_content]
        return [n for n in names if n is not None]

    @content.setter
    def content(self, db_names: List[str]) -> None:
        """Set the databases to back up for this Snowflake subclient.

        Args:
            db_names: A non-empty list of plain Snowflake database name strings.
                The SDK wraps these into the CloudDBEntity XML format required
                by the API automatically.

        Raises:
            SDKException: If db_names is not a non-empty list of strings.

        Example:
            >>> subclient.content = ["MY_DB", "ANOTHER_DB"]

        #ai-gen-doc
        """
        if isinstance(db_names, list) and db_names and all(isinstance(n, str) for n in db_names):
            self._set_content(db_names=db_names)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient content should be a non-empty list of database name strings'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this Snowflake subclient's instance backups.

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
        """Restore Snowflake data from the specified backup.

        Submits an in-place restore job for the specified paths to restore Snowflake
        database content from a backup to the original location.

        If `paths` is not provided, the restore paths are automatically derived from
        the subclient's configured content (database names).

        Args:
            paths: List of paths to restore (e.g. ["/MY_DB"] or ["/MY_DB/MY_SCHEMA"]).
                   If None, paths are derived from the subclient's content.
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to `restore_in_place`.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails, parameters are invalid, or
                          no paths can be resolved.
        """
        if paths is None:
            db_names = self.content
            if not db_names:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in subclient; cannot derive restore paths'
                )
            paths = [f'/{name}' for name in db_names]

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
