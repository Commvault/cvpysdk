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

"""File for operating on a Mailchimp subclient."""

import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class MailchimpSubclient(CloudAppsSubclient):
    """Represents a Mailchimp Cloud Apps subclient."""

    CONTENT_TYPES = {
        'Templates': 49,
        'Audiences': 100,
        'Campaigns': 47,
        'LandingPages': 102,
        'Assets': 101,
        'Automations': 103,
        'ECommerce': 104,
        'CustomerJourneys': 105,
    }
    DEFAULT_CONTENT = (
        'Templates',
        'Audiences',
        'Campaigns',
        'LandingPages',
        'Assets',
        'Automations',
        'ECommerce',
    )

    @classmethod
    def _normalize_content(cls, content_names: Optional[List[str]]) -> List[str]:
        """Validate Mailchimp category names and return unique values."""
        if content_names is None or content_names == []:
            return list(cls.DEFAULT_CONTENT)
        if not isinstance(content_names, list) or not all(
                isinstance(content_name, str) for content_name in content_names
        ):
            raise SDKException(
                'Subclient', '101',
                'Mailchimp content should be a list of category name strings'
            )

        unknown = [name for name in content_names if name not in cls.CONTENT_TYPES]
        if unknown:
            raise SDKException(
                'Subclient', '102',
                'Unsupported Mailchimp content categories: {0}'.format(', '.join(unknown))
            )
        return list(dict.fromkeys(content_names))

    @classmethod
    def _build_content_item(cls, content_name: str) -> dict:
        """Build one Mailchimp content item in CloudDBEntity XML format."""
        content_type = cls.CONTENT_TYPES[content_name]
        xml = (
            '<CloudDBEntity><children>'
            '<name>{0}</name><path>/{0}</path><displayName>{0}</displayName>'
            '<type>{1}</type><workloadObjectType>{1}</workloadObjectType>'
            '<isContainer>false</isContainer></children></CloudDBEntity>'
        ).format(content_name, content_type)
        return {'path': xml}

    @classmethod
    def _build_content_xml(cls, content_names: Optional[List[str]] = None) -> str:
        """Build the Mailchimp content XML used by instance creation."""
        children = ''.join(
            cls._build_content_item(content_name)['path'][len('<CloudDBEntity>'):-len('</CloudDBEntity>')]
            for content_name in cls._normalize_content(content_names)
        )
        return '<CloudDBEntity>{0}</CloudDBEntity>'.format(children)

    @staticmethod
    def _parse_content_name(path_dict: dict) -> Optional[str]:
        """Extract a Mailchimp category name from a CloudDBEntity item."""
        match = re.search(r'<name>([^<]+)</name>', path_dict.get('path', ''))
        return match.group(1) if match else None

    def _get_subclient_properties(self) -> None:
        """Retrieve Mailchimp-specific subclient properties."""
        super(MailchimpSubclient, self)._get_subclient_properties()
        self._mailchimp_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the Mailchimp subclient update payload."""
        return {
            'subClientProperties': {
                'proxyClient': self._proxyClient,
                'subClientEntity': self._subClientEntity,
                'commonProperties': self._commonProperties,
                'cloudAppsSubClientProp': {
                    'instanceType': self._backupset_object._instance_object.ca_instance_type
                },
                'content': self._mailchimp_content
            }
        }

    def _set_content(self, content_names: Optional[List[str]] = None) -> None:
        """Convert Mailchimp category names to XML items and persist them."""
        self._mailchimp_content = [
            self._build_content_item(name) for name in self._normalize_content(content_names)
        ]
        self._set_subclient_properties('content', self._mailchimp_content)

    @property
    def content(self) -> List[str]:
        """Get configured Mailchimp content category names."""
        names = [self._parse_content_name(item) for item in self._mailchimp_content]
        return [name for name in names if name is not None]

    @content.setter
    def content(self, content_names: List[str]) -> None:
        """Set Mailchimp content category names."""
        if isinstance(content_names, list) and content_names:
            self._set_content(content_names)
            return
        raise SDKException(
            'Subclient', '102',
            'Subclient content should be a non-empty list of Mailchimp category strings'
        )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse content in this Mailchimp subclient's backups."""
        return self._backupset_object._instance_object.browse(*args, **kwargs)

    def restore(
            self,
            paths: Optional[List[str]] = None,
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs: Any
    ) -> Job:
        """Restore Mailchimp data from the specified backup."""
        if paths is None:
            content_names = self.content
            paths = [('/' + name) for name in content_names] if content_names else ['/']

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )