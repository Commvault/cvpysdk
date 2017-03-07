#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Subclient.

VirualServerSubclient is the only class defined in this file.

VirtualServerSubclient: Derived class from Subclient Base class, representing a
                            virtual server subclient, and to perform operations on that subclient

VirtualServerSubclient:
    _get_subclient_content_()   --  gets the content of a virtual server subclient

    _set_subclient_content_()   --  sets the content of a virtual server subclient

"""

from ..exception import SDKException
from ..subclient import Subclient


class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self, subclient_properties):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of subclient

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        content_types = {
            '1': 'Host',
            '2': 'Resource Pool',
            '4': 'Datacenter',
            '9': 'Virtual Machine',
            '16': 'All unprotected VMs',
            '17': 'Root'
        }

        if 'vmContent' in self._subclient_properties:
            subclient_content = subclient_properties['vmContent']

            if 'children' in subclient_content:
                children = subclient_content['children']

                for child in children:
                    path = str(child['path']) if 'path' in child else None
                    display_name = str(child['displayName'])
                    content_type = content_types[str(child['type'])]

                    temp_dict = {
                        'path': path,
                        'display_name': display_name,
                        'type': content_type
                    }

                    content.append(temp_dict)

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Virtual Server Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        content_types = {
            'Host': '1',
            'Root': '17',
            'Datacenter': '4',
            'Resource Pool': '2',
            'Virtual Machine': '9',
            'All unprotected VMs': '16'
        }

        try:
            for temp_dict in subclient_content:
                virtual_server_dict = {
                    'allOrAnyChildren': True,
                    'equalsOrNotEquals': True,
                    'displayName': temp_dict['display_name'],
                    'path': temp_dict['path'],
                    'type': content_types[temp_dict['type']]
                }

                content.append(virtual_server_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        vs_subclient_content = {
            "children": content
        }

        return vs_subclient_content

    @property
    def restore_in_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
                self.__class__.__name__,
                'restore_in_place'
            )
        )

    @property
    def restore_out_of_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
                self.__class__.__name__,
                'restore_out_of_place'
            )
        )
