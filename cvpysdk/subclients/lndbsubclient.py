#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# import sys
# sys.path.append("..")
"""

File for operating on a Notes Database Subclient.

LNDbSubclient is the only class defined in this file.

LNDbSubclient: Derived class from Subclient Base class.
            Represents a notes database subclient, and performs operations on that subclient

LNDbSubclient:

    _get_subclient_properties()          --  gets subclient related properties of
                                                    Notes Database subclient.

    _get_subclient_properties_json()     --  gets all the subclient related properties of
                                                    Notes Database subclient.

    content()                            --  update the content of the subclient


"""
from __future__ import absolute_import
from __future__ import unicode_literals
from ..subclient import Subclient


class LNDbSubclient(Subclient):
    """Derived class from Subclient Base class, representing a LNDB subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of LN DB subclient."""
        super(LNDbSubclient, self)._get_subclient_properties()
        # print(self._subclient_properties)
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']
        if 'proxyClient' in self._subclient_properties:
            self._proxyClient = self._subclient_properties['proxyClient']
        if 'subClientEntity' in self._subclient_properties:
            self._subClientEntity = self._subclient_properties['subClientEntity']
        if 'commonProperties' in self._subclient_properties:
            self._commonProperties = self._subclient_properties['commonProperties']

    def _get_subclient_properties_json(self):
        """Get the all subclient related properties of this subclient.
           Returns:
                dict - all subclient properties put inside a dict
        """

        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                }
        }
        return subclient_json

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        return self._content

    # # @content.setter
    # def content(self, subclient_content):
    #     """
    #
    #     Creates the list of content JSON to pass to the API to add/update content of a
    #         LNDB Subclient.
    #
    #         Args:
    #             subclient_content (list)  --  list of the content to add to the subclient
    #
    #         Returns:
    #             list - list of the appropriate JSON for an agent to send to the POST Subclient API
    #
    #     """
    #     content = []
    #
    #     try:
    #         for database in subclient_content:
    #             print(database)
    #             print(type(database))
    #             # temp_content_dict = {
    #             #     "lotusNotesDBContent": {
    #             #             "dbiid1"        : database['dbiid1'],
    #             #             "dbiid2"        : database['dbiid2'],
    #             #             "dbiid3"        : database['dbiid3'],
    #             #             "dbiid4"        : database['dbiid4'],
    #             #             "relativePath"  : database['relativePath'],
    #             #             "databaseTitle" : database['databaseTitle'],
    #             #         }
    #             # }
    #             content.append(database)
    #     except KeyError as err:
    #         raise SDKException('Subclient', '102', '{} not given in content'.format(err))
    #
    #     self._set_subclient_properties("_content", content)
