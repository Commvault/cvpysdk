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
    """Derived class from CloudAppsSubclient Base class, representing a Google Cloud Spanner subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient related properties of Google Cloud Spanner subclient.."""
        super(GoogleSpannerSubclient, self)._get_subclient_properties()
        if 'backupObject' in self._subclient_properties['cloudAppsSubClientProp']['cloudSpannerSubclient']:
            self._content = \
                self._subclient_properties['cloudAppsSubClientProp']['cloudSpannerSubclient']['backupObject']

        self._spanner_content = []
        for database in self._content:
                self._spanner_content.append(database['dbName'])

    @property
    def content(self):
        """
        Returns the subclient content list

            Returns:
                    list - list of subclient content
        """
        return self._spanner_content

    @content.setter
    def content(self, subclient_content):
        """Sets content to the Google Spanner Subclient

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

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
