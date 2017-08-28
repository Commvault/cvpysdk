#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a File System Subclient

FileSystemSubclient is the only class defined in this file.

FileSystemSubclient: Derived class from Subclient Base class, representing a file system subclient,
                        and to perform operations on that subclient

FileSystemSubclient:

    _get_subclient_properties()          --  initializes the subclient  related properties of
                                                 File System subclient

    _get_subclient_properties_json()     --  gets all the subclient  related properties of
                                                 File System subclient

    content()                            --  update the content of the subclient

    filter_content()                     --  update the filter of the subclient

"""

from __future__ import unicode_literals

from ..subclient import Subclient
from ..exception import SDKException


class FileSystemSubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient.
    """

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.

        """
        super(FileSystemSubclient, self)._get_subclient_properties()
        if 'impersonateUser' in self._subclient_properties:
            self._impersonateUser = self._subclient_properties['impersonateUser']
        if 'fsSubClientProp' in self._subclient_properties:
            self._fsSubClientProp = self._subclient_properties['fsSubClientProp']
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
                    "fsSubClientProp": self._fsSubClientProp,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

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
            File System Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []
        for path in subclient_content:
            file_system_dict = {
                "path": path
            }
            content.append(file_system_dict)

        self._set_subclient_properties("_content", content)

    @property
    def filter_content(self):
        """Treats the subclient filter content as a property of the Subclient class."""
        _filter_content = []

        for path in self._content:
            if 'excludePath' in path:
                _filter_content.append(path["excludePath"])

        return _filter_content

    @filter_content.setter
    def filter_content(self, value):
        """Sets the filter content of the subclient as the value provided as input.

            example: ['/vol/Test_Vol', '/vol/test/file*', '/vol/test2/file.txt']

            Raises:
                SDKException:
                    if failed to update filter content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if isinstance(value, list) and value != []:
            content = []

            for path in value:
                nas_dict = {
                    "excludePath": path
                }
                content.append(nas_dict)

            self._set_subclient_properties("_content", content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient filter content should be a list value and not empty'
            )
