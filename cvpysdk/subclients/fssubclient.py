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

    find_all_versions()                  --  returns the dict containing list of all the backuped up
                                                versions of specified file

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

    def _set_content(self, content=None, filter_content=None):
        """Sets the subclient content / filter content

            Args:
                content         (list)      --  list of subclient content

                filter_content  (list)      --  list of filter content
        """
        if content is None:
            content = self.content

        if filter_content is None:
            filter_content = self.filter_content

        update_content = []
        for path in content:
            file_system_dict = {
                "path": path
            }
            update_content.append(file_system_dict)

        for path in filter_content:
            filter_dict = {
                "excludePath": path
            }
            update_content.append(filter_dict)

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
            File System Subclient.

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

            example: ['*book*', 'file**']

            Raises:
                SDKException:
                    if failed to update filter content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if isinstance(value, list) and value != []:
            self._set_content(filter_content=value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient filter content should be a list value and not empty'
            )

    def find_all_versions(self, *args, **kwargs):
        """Searches the content of a Subclient.

            Args:
                Dictionary of browse options:
                    Example:
                        find_all_versions({
                            'path': 'c:\\hello',
                            'show_deleted': True,
                            'from_time': '2014-04-20 12:00:00',
                            'to_time': '2016-04-31 12:00:00'
                        })

                    (OR)

                Keyword argument of browse options:
                    Example:
                        find_all_versions(
                            path='c:\\hello.txt',
                            show_deleted=True,
                            to_time='2016-04-31 12:00:00'
                        )

                Refer self._default_browse_options for all the supported options

        Returns:
            dict    -   dictionary of the specified file with list of all the file versions and
                            additional metadata retrieved from browse
        """
        if len(args) > 0 and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'all_versions'

        return self._backupset_object._do_browse(options)
