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

"""File for operating on an AWS Bedrock Subclient.

AwsBedrockSubclient is the only class defined in this file.

AwsBedrockSubclient: Derived class from CloudAppsSubclient Base class, representing an
AWS Bedrock Cloud Apps subclient, and to perform operations on that subclient.

AwsBedrockSubclient:

    _get_subclient_properties()         --  Gets the properties of the AWS Bedrock subclient

    _get_subclient_properties_json()    --  Gets the properties JSON of the AWS Bedrock subclient

    content                             --  Gets/sets content as plain content-path strings

    _set_content()                      --  Converts path strings to XML dicts and persists

    _build_content_item()               --  Wraps a path in CloudDBEntity XML format

    _parse_content_name()               --  Extracts a path/name from a CloudDBEntity XML dict

    browse()                            --  Browse and return content of this subclient's backups

    restore()                           --  Restore AWS Bedrock data from the specified backup

"""

import re
from typing import Any, List, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job


class AwsBedrockSubclient(CloudAppsSubclient):
    """Represents an AWS Bedrock Cloud Apps subclient.

    Content format (user-facing):
        Content is represented as a List[str] of plain workload paths or names,
        e.g. ["/us-east-1/Agents/Agent - sample"]. The SDK handles XML wrapping.

    #ai-gen-doc
    """

    @staticmethod
    def _build_content_item(content_path: str) -> dict:
        """Wrap a plain AWS Bedrock content path in CloudDBEntity XML format.

        Args:
            content_path: Plain path string, for example "/us-east-1/Agents/Agent - sample".

        Returns:
            dict: A content path dict {"path": "<CloudDBEntity>...</CloudDBEntity>"}.

        #ai-gen-doc
        """
        normalized = content_path if content_path.startswith('/') else f'/{content_path}'
        leaf_name = normalized.split('/')[-1]
        xml = (
            f'<CloudDBEntity><children>'
            f'<name>{leaf_name}</name>'
            f'<path>{normalized}</path>'
            f'<displayName>{leaf_name}</displayName>'
            f'<isContainer>false</isContainer>'
            f'</children></CloudDBEntity>'
        )
        return {'path': xml}

    @staticmethod
    def _parse_content_name(path_dict: Any) -> Optional[str]:
        """Extract a plain content path from an API content item.

        Args:
            path_dict: API content item. May be a dict with "path" or a raw XML string.

        Returns:
            str: Extracted path when available, otherwise None.

        #ai-gen-doc
        """
        if isinstance(path_dict, str):
            match = re.search(r'<path>([^<]+)</path>', path_dict)
            return match.group(1) if match else None

        if isinstance(path_dict, dict):
            raw_path = path_dict.get('path', '')
            if isinstance(raw_path, str) and raw_path.strip().startswith('<CloudDBEntity>'):
                match = re.search(r'<path>([^<]+)</path>', raw_path)
                return match.group(1) if match else None
            if isinstance(raw_path, str):
                return raw_path

        return None

    def _get_subclient_properties(self) -> None:
        """Retrieve the properties specific to the AWS Bedrock subclient.

        #ai-gen-doc
        """
        super(AwsBedrockSubclient, self)._get_subclient_properties()
        self._aws_bedrock_content = self._subclient_properties.get('content', [])

    def _get_subclient_properties_json(self) -> dict:
        """Build the properties JSON payload for updating the AWS Bedrock subclient.

        Returns:
            dict: A dictionary containing all properties of the AWS Bedrock subclient.

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
                'content': self._aws_bedrock_content
            }
        }

    def _set_content(self, items: Optional[List[str]] = None) -> None:
        """Convert plain path strings to CloudDBEntity XML dicts and persist via API.

        Args:
            items: List of plain AWS Bedrock content path strings.

        #ai-gen-doc
        """
        self._aws_bedrock_content = [
            self._build_content_item(item) for item in (items or [])
        ]
        self._set_subclient_properties('content', self._aws_bedrock_content)

    @property
    def content(self) -> List[str]:
        """Get the list of content paths configured for this subclient.

        Returns:
            List[str]: Plain content path strings.

        #ai-gen-doc
        """
        parsed = [self._parse_content_name(item) for item in self._aws_bedrock_content]
        return [item for item in parsed if item is not None]

    @content.setter
    def content(self, items: List[str]) -> None:
        """Set the list of content paths to back up.

        Args:
            items: Non-empty list of content path strings.

        Raises:
            SDKException: If items is not a non-empty list of strings.

        #ai-gen-doc
        """
        if isinstance(items, list) and items and all(isinstance(item, str) for item in items):
            self._set_content(items=items)
        elif isinstance(items, list) and not items:
            self._set_content(items=items)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient content should be a list of content path strings'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this AWS Bedrock subclient's instance backups.

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
        """Restore AWS Bedrock data from the specified backup.

        Args:
            paths: List of paths to restore. If None, derived from subclient content.
            overwrite: Whether to overwrite existing data. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0.
            **kwargs: Additional keyword arguments forwarded to restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If no paths are available for restore.

        #ai-gen-doc
        """
        if paths is None:
            paths = self.content
            if not paths:
                raise SDKException(
                    'Subclient', '102',
                    'No content found in subclient; cannot derive restore paths'
                )

        return self._backupset_object._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
