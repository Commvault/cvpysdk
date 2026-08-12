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

"""File for operating on a Google Cloud Spanner Subclient.

GoogleSpannerSubclient is the only class defined in this file.

GoogleSpannerSubclient:    Derived class from CloudAppsSubclient Base class, representing a
Google Cloud Spanner subclient, and to perform operations on that subclient

GoogleSpannerSubclient:

    _get_subclient_properties()         --  gets the properties of Google Subclient

    content()                           --  sets the content of the subclient

    discover()                          --  runs database discovery on subclient

GoogleSpannerSubclient Attributes:

    content           --  Returns the subclient content list

"""

from ...exception import SDKException
from ..casubclient import CloudAppsSubclient


class GoogleSpannerSubclient(CloudAppsSubclient):
    """
    Represents a subclient for Google Cloud Spanner within the CloudApps framework.

    This class extends the CloudAppsSubclient base class to provide specialized
    operations and management for Google Cloud Spanner subclients. It includes
    methods for retrieving subclient properties and managing subclient content.

    Key Features:
        - Retrieve subclient properties specific to Google Cloud Spanner
        - Access and manage subclient content via a property interface
        - Inherits core functionality from CloudAppsSubclient

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> None:
        """Retrieve and update the properties specific to the Google Cloud Spanner subclient.

        This method fetches the configuration and metadata related to the current Google Cloud Spanner subclient
        and updates the internal state of the object accordingly.

        Example:
            >>> subclient = GoogleSpannerSubclient()
            >>> subclient._get_subclient_properties()
            >>> # The subclient's properties are now refreshed with the latest values

        #ai-gen-doc
        """
        super(GoogleSpannerSubclient, self)._get_subclient_properties()
        if 'backupObject' in self._subclient_properties['cloudAppsSubClientProp']['cloudSpannerSubclient']:
            self._content = \
                self._subclient_properties['cloudAppsSubClientProp']['cloudSpannerSubclient']['backupObject']

        self._spanner_content = []
        for database in self._content:
            self._spanner_content.append(database['dbName'])

    @property
    def content(self) -> list:
        """Get the list of content items associated with the Google Spanner subclient.

        Returns:
            list: A list containing the content items configured for this subclient.

        Example:
            >>> subclient = GoogleSpannerSubclient()
            >>> content_list = subclient.content
            >>> print(f"Subclient content: {content_list}")
            >>> # The returned list contains the content items for the subclient

        #ai-gen-doc
        """
        return self._spanner_content

    @content.setter
    def content(self, subclient_content: list) -> None:
        """Set the content for the Google Spanner Subclient.

        Args:
            subclient_content: A list specifying the content to add to the subclient.

        Example:
            >>> spanner_subclient = GoogleSpannerSubclient()
            >>> spanner_subclient.content = ['database1', 'database2']
            >>> # The subclient content is now set to the specified databases

        #ai-gen-doc
        """
        content = []

        for database in subclient_content:
            temp_content_dict = {
                "cloudAppsSubClientProp": {
                    "cloudSpannerSubclient": {
                        "backupObject": {
                            "dbName": database
                        }
                    }
                }
            }

            content.append(temp_content_dict)
        self._set_subclient_properties("_content", content)
