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

"""File for operating on a SAP IQ Subclient.

SapIqSubclient is the only class defined in this file.

SapIqSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                 SAP IQ Cloud Apps subclient, and to perform operations on that subclient

SapIqSubclient:

    _get_subclient_properties()         --  Gets the properties of the SAP IQ subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the SAP IQ subclient

    content                             --  Gets/sets content as plain database name strings

    _set_content()                      --  Converts database names to content dicts and persists

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore SAP IQ data from the specified backup

"""
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class SapIqSubclient(CloudAppsSubclient):
    """
    Represents a SAP IQ Cloud Apps subclient for managing backup and restore operations.

    Content format (user-facing):
        Content is represented as a List[str] of plain SAP IQ database names,
        e.g. ["my_iq_db"]. The API stores each item as ``{"path": "<database name>"}``
        without any XML wrapping.

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the SAP IQ subclient.

        Example:
            >>> subclient._get_subclient_properties()

        #ai-gen-doc
        """
        super(SapIqSubclient, self)._get_subclient_properties()
        self._sap_iq_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the SAP IQ subclient.

        Returns:
            dict: A dictionary containing all properties of the SAP IQ subclient.

        Example:
            >>> properties = subclient._get_subclient_properties_json()

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
                "content": self._sap_iq_content
            }
        }

    def _set_content(self, db_names: Optional[List[str]] = None) -> None:
        """Convert plain database names to content dicts and persist via API.

        Args:
            db_names: List of plain SAP IQ database name strings.
                      Pass None or an empty list to clear content.

        Example:
            >>> subclient._set_content(["my_iq_db"])

        #ai-gen-doc
        """
        self._sap_iq_content = [{"path": name} for name in (db_names or [])]
        self._set_subclient_properties("content", self._sap_iq_content)

    @property
    def content(self) -> List[str]:
        """Get the SAP IQ database names configured as content for this subclient.

        Returns:
            list: A list of plain database name strings.

        Example:
            >>> subclient.content
            ['my_iq_db']

        #ai-gen-doc
        """
        return [item.get('path') for item in self._sap_iq_content if item.get('path')]

    @content.setter
    def content(self, db_names: List[str]) -> None:
        """Set the SAP IQ databases to back up for this subclient.

        Args:
            db_names: A non-empty list of plain SAP IQ database name strings.

        Raises:
            SDKException: If db_names is not a non-empty list of strings.

        Example:
            >>> subclient.content = ["my_iq_db"]

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
        """Browse the content of this SAP IQ subclient's instance backups.

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
        """Restore SAP IQ data from the specified backup.

        If ``paths`` is not provided, restore paths are derived from the subclient's
        configured content as ``/<database name>``.

        Args:
            paths: List of paths to restore (e.g. ["/my_iq_db"]).
                   If None, paths are derived from the subclient's content.
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to ``restore_in_place``.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore fails or no paths can be resolved.

        Example:
            >>> job = subclient.restore(overwrite=True)

        #ai-gen-doc
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
