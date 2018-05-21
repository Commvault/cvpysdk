# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Amazon S3 Subclient.

S3Subclient is the only class defined in this file.

S3Subclient:    Derived class from CloudAppsSubclient Base class, representing a
                        Amazon S3 subclient, and to perform operations on that subclient

S3Subclient:

    _get_subclient_properties()         --  gets the properties of Amazon S3 Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of Amazon S3 Subclient

    content()                           --  gets the content of the subclient

    _set_content()                      --  sets the content of the subclient


"""

from __future__ import unicode_literals
from past.builtins import basestring
from ...exception import SDKException
from ..casubclient import CloudAppsSubclient


class S3Subclient(CloudAppsSubclient):
    """Derived class from Subclient Base class, representing a Amazon s3 subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of Amazon S3 subclient.."""
        super(S3Subclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']
        if 's3SubClientProp' in self._subclient_properties:
            self._s3SubClientProp = self._subclient_properties['s3SubClientProp']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "cloudAppsSubClientProp": {
                        "instanceType": 5
                    },
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    def _set_content(self,
                     content=None):
        """Sets the subclient content

            Args:
                content         	(list)      --  list of subclient content
        """
        if content is None:
            content = self.content

        update_content = []
        for path in content:
            s3_dict = {
                "path": path
            }
            update_content.append(s3_dict)

        self._set_subclient_properties("_content", update_content)

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        for path in self._content:
            if 'path' in path:
                content.append(path["path"])

        return content

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Amazon S3 Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )
