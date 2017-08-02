#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Instance.

VirualServerInstance is the only class defined in this file.

VirtualServerInstance: Derived class from Instance Base class, representing a
                            virtual server instance, and to perform operations on that instance

VirtualServerInstance:
    _get_instance_properties()  --  Instance class method overwritten to add virtual server
                                        instance properties as well

"""

from __future__ import unicode_literals

from ..instance import Instance


class VirtualServerInstance(Instance):
    """Class for representing an Instance of the Virtual Server agent."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        super(VirtualServerInstance, self)._get_instance_properties()

        self._vs_instance_type = None
        self._v_center_name = None
        self._v_center_username = None
        self._associated_clients = None

        if 'virtualServerInstance' in self._properties:
            virtual_server_instance = self._properties['virtualServerInstance']
            self._vs_instance_type = virtual_server_instance['vsInstanceType']

            if 'vmwareVendor' in virtual_server_instance:
                v_center = virtual_server_instance['vmwareVendor']['virtualCenter']

                self._v_center_name = v_center['domainName']
                self._v_center_username = v_center['userName']

            if 'associatedClients' in virtual_server_instance:
                associated_clients = virtual_server_instance['associatedClients']

                self._associated_clients = {
                    'Clients': [],
                    'ClientGroups': []
                }

                for member in associated_clients['memberServers']:
                    client = member['client']

                    if 'clientName' in client:
                        temp_dict = {
                            'client_name': client['clientName'],
                            'client_id': str(client['clientId'])
                        }
                        self._associated_clients['Clients'].append(temp_dict)
                    elif 'clientGroupName' in client:
                        temp_dict = {
                            'client_group_name': client['clientGroupName'],
                            'client_group_id': str(client['clientGroupId'])
                        }
                        self._associated_clients['ClientGroups'].append(temp_dict)
                    else:
                        continue

    @property
    def vs_instance_type(self):
        """Treats the vs instance type as a read-only attribute."""
        return self._vs_instance_type

    @property
    def v_center_name(self):
        """Treats the v-center name as a read-only attribute."""
        return self._v_center_name

    @property
    def v_center_username(self):
        """Treats the v-center user name as a read-only attribute."""
        return self._v_center_username

    @property
    def associated_clients(self):
        """Treats the clients associated to this instance as a read-only attribute."""
        return self._associated_clients
