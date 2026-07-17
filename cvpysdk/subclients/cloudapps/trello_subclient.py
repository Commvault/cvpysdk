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

"""File for operating on a Trello Subclient.

TrelloSubclient is the only class defined in this file.

TrelloSubclient: Derived class from CloudAppsSubclient Base class, representing a
Trello Cloud Apps subclient, and to perform operations on that subclient.

"""
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class TrelloSubclient(CloudAppsSubclient):
    """Represents a Trello Cloud Apps subclient.

    Content format (user-facing):
        Content is represented as List[str] of plain Trello entity names.

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> None:
        """Retrieve Trello-specific subclient properties.

        #ai-gen-doc
        """
        super(TrelloSubclient, self)._get_subclient_properties()
        self._trello_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build Trello subclient properties JSON.

        Returns:
            dict: Payload for updating subclient properties.

        #ai-gen-doc
        """
        return {
            'subClientProperties': {
                'proxyClient': self._proxyClient,
                'subClientEntity': self._subClientEntity,
                'commonProperties': self._commonProperties,
                'cloudAppsSubClientProp': {
                    'instanceType': self._backupset_object._instance_object.ca_instance_type
                },
                'content': self._trello_content
            }
        }

    def _set_content(self, items: Optional[List[str]] = None) -> None:
        """Set Trello content and persist.

        Args:
            items: List of Trello entities to protect.

        #ai-gen-doc
        """
        self._trello_content = [{'path': item} for item in (items or [])]
        self._set_subclient_properties('content', self._trello_content)

    @property
    def content(self) -> List[str]:
        """Get configured Trello subclient content as plain strings.

        Returns:
            list[str]: Trello entity names/paths.

        #ai-gen-doc
        """
        values = []
        for item in self._trello_content:
            if isinstance(item, dict):
                values.append(item.get('path', ''))
            elif isinstance(item, str):
                values.append(item)
        return [value for value in values if value]

    @content.setter
    def content(self, items: List[str]) -> None:
        """Set Trello subclient content.

        Args:
            items: Non-empty list of Trello content names.

        Raises:
            SDKException: If items is not a non-empty list of strings.

        #ai-gen-doc
        """
        if isinstance(items, list) and items and all(isinstance(i, str) for i in items):
            self._set_content(items=items)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient content should be a non-empty list of Trello entity strings'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse content of this Trello subclient's instance backups.

        Returns:
            dict: Browse results.

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
        """Restore Trello data from backup.

        Args:
            paths: Items to restore. If omitted, derived from subclient content.
            overwrite: Whether to overwrite existing data. Defaults to True.
            copy_precedence: Copy precedence value. Defaults to 0.
            **kwargs: Additional restore options.

        Returns:
            Job: Submitted restore job.

        Raises:
            SDKException: If no restore paths can be resolved.

        #ai-gen-doc
        """
        if paths is None:
            current_content = self.content
            if not current_content:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in subclient; cannot derive restore paths'
                )
            paths = [c if c.startswith('/') else f'/{c}' for c in current_content]

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
