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

"""File for operating on a Miro Subclient.

MiroSubclient is the only class defined in this file.

MiroSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                Miro Cloud Apps subclient, and to perform operations on that subclient

MiroSubclient:

    _get_subclient_properties()         --  Gets the properties of the Miro subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the Miro subclient

    content                             --  Gets/sets content as plain board name strings

    _set_content()                      --  Converts board items to CloudDBEntity XML dicts
                                            and persists via API

    _build_content_item()               --  Wraps a board item in CloudDBEntity XML format

    _build_content_xml()                --  Builds a CloudDBEntity XML string from board items

    _parse_board_name()                 --  Extracts a board display name from a
                                            CloudDBEntity XML path dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore Miro data from the specified backup

"""

import re
from typing import Any, Dict, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class MiroSubclient(CloudAppsSubclient):
    """
    Represents a Miro Cloud Apps subclient for managing backup and restore operations.

    This class extends the CloudAppsSubclient base class and provides specialised
    methods for interacting with Miro subclients.

    Content format (user-facing):
        Content is represented as ``List[str]`` of plain board display names
        (e.g. ``["MyBoard", "AnotherBoard"]``).  The SDK handles all CloudDBEntity
        XML wrapping required by the underlying API internally.

        Note: Because Miro board paths include an encoded board ID
        (``/BoardName__cvbid12<encodedId>``), the full path must be supplied
        when calling ``_build_content_item()`` directly.  The ``content`` property
        returns only the human-readable board names.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(board_name: str, encoded_path: str) -> dict:
        """
        Wrap a board name and its encoded path in the CloudDBEntity XML format.

        The ``path`` field uses the encoded path from the MachineBrowse response
        (e.g. ``/BoardName__cvbid12uXjVHO0_AJU=``).

        Args:
            board_name (str): Human-readable board display name.
            encoded_path (str): Encoded board path returned by the MachineBrowse API,
                                including the leading ``/`` separator.

        Returns:
            dict: A content path dict ``{"path": "<CloudDBEntity>...</CloudDBEntity>"}``.

        Example:
            >>> item = MiroSubclient._build_content_item(
            ...     "MyBoard", "/MyBoard__cvbid12uXjVHO0_AJU="
            ... )

        #ai-gen-doc
        """
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{board_name}</name>'
            f'<path>{encoded_path}</path>'
            f'<displayName>{board_name}</displayName>'
            f'<isContainer>false</isContainer>'
            f'</children></CloudDBEntity>'
        )
        return {"path": xml}

    @staticmethod
    def _build_content_xml(board_items: List[Dict[str, str]]) -> str:
        """
        Build a single CloudDBEntity XML string with all board items as children.

        Used internally by ``add_miro_instance()`` to construct the ``content``
        array for the instance-creation POST request.

        Args:
            board_items (List[Dict[str, str]]): List of dicts, each with keys:
                - ``'name'``: Human-readable board display name.
                - ``'path'``: Encoded board path (e.g. ``/BoardName__cvbid12<id>``).

        Returns:
            str: A single CloudDBEntity XML string containing one ``<children>``
                 block per board item.

        Example:
            >>> xml = MiroSubclient._build_content_xml([
            ...     {"name": "MyBoard", "path": "/MyBoard__cvbid12uXjVHO0_AJU="}
            ... ])

        #ai-gen-doc
        """
        children = ''.join(
            f'<children>'
            f'<name>{item["name"]}</name>'
            f'<path>{item["path"]}</path>'
            f'<displayName>{item["name"]}</displayName>'
            f'<isContainer>false</isContainer>'
            f'</children>'
            for item in board_items
        )
        return f'<CloudDBEntity>{children}</CloudDBEntity>'

    @staticmethod
    def _parse_board_name(path_dict: dict) -> Optional[str]:
        """
        Extract the plain board display name from a CloudDBEntity XML path dict.

        Args:
            path_dict (dict): A content item dict returned by the API, containing
                              the CloudDBEntity XML string under the ``"path"`` key.

        Returns:
            Optional[str]: The board display name, or ``None`` if the XML cannot
                           be parsed.

        #ai-gen-doc
        """
        match = re.search(r'<displayName>([^<]+)</displayName>', path_dict.get('path', ''))
        return match.group(1) if match else None

    def _get_subclient_properties(self) -> None:
        """
        Retrieve the properties specific to the Miro subclient.

        Fetches and stores configuration details including the content list
        from the subclient properties response.

        Example:
            >>> subclient._get_subclient_properties()

        #ai-gen-doc
        """
        super(MiroSubclient, self)._get_subclient_properties()
        self._miro_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """
        Build the properties JSON payload for updating the Miro subclient.

        Returns:
            dict: Properties dictionary suitable for a POST to the subclient
                  update endpoint.

        Example:
            >>> props = subclient._get_subclient_properties_json()

        #ai-gen-doc
        """
        return {
            "subClientProperties": {
                "proxyClient": self._proxyClient,
                "subClientEntity": self._subClientEntity,
                "commonProperties": self._commonProperties,
                "cloudAppsSubClientProp": {
                    "instanceType": self._backupset_object._instance_object.ca_instance_type
                },
                "content": self._miro_content,
            }
        }

    def _set_content(self, board_items: Optional[List[Dict[str, str]]] = None) -> None:
        """
        Convert board items to CloudDBEntity XML dicts and persist via API.

        Args:
            board_items (Optional[List[Dict[str, str]]]): List of dicts with
                ``'name'`` and ``'path'`` keys.  Pass ``None`` or an empty list
                to clear content.

        Example:
            >>> subclient._set_content([
            ...     {"name": "MyBoard", "path": "/MyBoard__cvbid12uXjVHO0_AJU="}
            ... ])

        #ai-gen-doc
        """
        self._miro_content = [
            self._build_content_item(item["name"], item["path"])
            for item in (board_items or [])
        ]
        self._set_subclient_properties("content", self._miro_content)

    @property
    def content(self) -> List[str]:
        """
        Get the Miro board names configured as content for this subclient.

        Returns:
            List[str]: Plain board display name strings.

        Example:
            >>> print(subclient.content)
            ['TC_00001_MiroBoard']

        #ai-gen-doc
        """
        names = [self._parse_board_name(item) for item in self._miro_content]
        return [n for n in names if n is not None]

    @content.setter
    def content(self, board_items: List[Dict[str, str]]) -> None:
        """
        Set the Miro boards to back up for this subclient.

        Args:
            board_items (List[Dict[str, str]]): A non-empty list of dicts, each
                containing ``'name'`` (board display name) and ``'path'``
                (encoded board path, e.g. ``/BoardName__cvbid12<id>``).

        Raises:
            SDKException: If ``board_items`` is not a non-empty list of dicts
                          or if any dict is missing required keys.

        Example:
            >>> subclient.content = [
            ...     {"name": "MyBoard", "path": "/MyBoard__cvbid12uXjVHO0_AJU="}
            ... ]

        #ai-gen-doc
        """
        if (
            isinstance(board_items, list)
            and board_items
            and all(
                isinstance(i, dict) and 'name' in i and 'path' in i
                for i in board_items
            )
        ):
            self._set_content(board_items=board_items)
        else:
            raise SDKException(
                'Subclient', '102',
                'Miro subclient content must be a non-empty list of dicts '
                'with "name" and "path" keys'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """
        Browse the content of this Miro subclient's instance backups.

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
        **kwargs: Any,
    ) -> Job:
        """
        Restore Miro boards from the specified backup.

        Submits an in-place restore job for the specified paths.  If ``paths`` is
        not provided, paths are derived automatically from the subclient's content.

        Args:
            paths (Optional[List[str]]): List of board paths to restore
                (e.g. ``["/BoardName__cvbid12uXjVHO0_AJU="]``).  If ``None``,
                paths are derived from the subclient's stored content items.
            overwrite (bool): Whether to overwrite existing data. Defaults to True.
            copy_precedence (int): Copy precedence to use. Defaults to 0 (latest).
            **kwargs: Additional keyword arguments forwarded to ``restore_in_place``.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If no content is found when ``paths`` is ``None``, or
                          if the restore operation fails.

        Example:
            >>> job = subclient.restore()

        #ai-gen-doc
        """
        if paths is None:
            # Derive restore paths from stored CloudDBEntity XML path values
            derived = []
            for item in self._miro_content:
                path_match = re.search(r'<path>([^<]+)</path>', item.get('path', ''))
                if path_match:
                    derived.append(path_match.group(1))
            if not derived:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in Miro subclient; cannot derive restore paths'
                )
            paths = derived

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs,
        )
