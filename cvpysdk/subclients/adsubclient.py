# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
File for Ad agent sublcient replated operation

Class:
    ADSubclient :

        _get_subclient_properties()    --    Method to get subclinet properites

        _get_subclient_properties_json --    Method to generate subclinet properties in json format

        content                        --    Properties of AD objects in subclient

ADSubclient:
    content() -- method to get AD agent subclient content

Function:
"""

from __future__ import unicode_literals

from ..exception import SDKException
from ..subclient import Subclient


class ADSubclient(Subclient):
    """Class for AD agent related subclient """

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.
        """
        super()._get_subclient_properties()
        if 'impersonateUser' in self._subclient_properties:
            self._impersonateUser = self._subclient_properties['impersonateUser']
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.
           Returns:
                dict - all subclient properties put inside a dict
        """
        subclient_json = {
            "subClientProperties":
                {
                    "impersonateUser": self._impersonateUser,
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def content(self):
        """ Get AD agent subclient content"""
        contents = []
        if "content" in self._subclient_properties:
            subclient_content = self._subclient_properties['content']
        else:
            subclient_content = []
        if len(subclient_content) > 0:
            for entry in subclient_content:
                if len(entry['path'].split(',')) > 1:
                    contents.append(",".join(entry['path'].split(',')[1:]))
                else:
                    raise SDKException('Subclient', "101",
                                       "subclient content is not valid")
        else:
            raise SDKException('Subclient', '101',
                               "subclient content return empty result")

        return contents

    def cv_contents(self, contents, entrypoint=None):
        """Commvault subclient content convert to AD format
            Args:
                content    (list)    subclient content        
                entrypoint    (string)    ad object entry point
            Return:
                (list)    ad format content
            Exception:
                None
        """
        content_ad = []
        for content in contents:
            contententry = ",".join(list(reversed(content.split(","))))
            if entrypoint is not None:
                shortdn = contententry.split(",{0}".format(entrypoint))[0]
            else:
                shortdn = None
            content_ad.append((contententry, shortdn))
        return content_ad        