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
    _get_subclient_content_()   --  gets the content of a file system subclient

    _set_subclient_content_()   --  sets the content of a file system subclient

"""

from ..subclient import Subclient


class FileSystemSubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self, subclient_properties):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of subclient

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        if 'content' in self._subclient_properties:
            subclient_content = subclient_properties['content']

            for path in subclient_content:
                content.append(str(path["path"]))

        return content

    def _set_subclient_content_(self, subclient_content):
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

        return content
