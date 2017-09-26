#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for operating on a Virtual Server Hyper-V Instance.

HyperVInstance is the only class defined in this file.

HyperVInstance:     Derived class from VirtualServerInstance Base class, representing a
                        Hyper-V instance, and to perform operations on that instance.

HyperVInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)            --  initialize object of hyper-v instance object associated with
                                        the VirtualServer Instance

    _get_instance_properties()  --  VirtualServer Instance class method overwritten to get Hyper-V
                                        specific instance properties

    _set_instance_properties()  --  Hyper-V Instance class method to set Hyper-V
                                        specific instance properties

"""

from ..vsinstance import VirtualServerInstance


class HyperVInstance(VirtualServerInstance):
    """Class for representing an Hyper-V Instance of the Virtual Server agent."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                agent_object        --      instance of the Agent class

                instance_name       --      name of the instance

                instance_id         --      id of the instance

            Returns:
                object  -   instance of the HyperVInstance class

        """
        super(HyperVInstance, self).__init__(agent_object, instance_name, instance_id)
        self._vendor_id(2)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(HyperVInstance, self)._get_instance_properties()

        self._server_name = []
        self._get_instance_common_properties()

        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"][
                "associatedClients"]["memberServers"]

            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))

    def set_instance_properties(self):
        """sets the Instance Property for this instance

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        self._default_FBRUnix_MediaAgent(self._properties_dict)
        self._vcPassword(self._properties_dict)
        self._docker(self._properties_dict)
        self._open_stack(self._properties_dict)
        self._azure(self._properties_dict)
        self._oracle_cloud(self._properties_dict)
        self._azure_Resource_Manager(self._properties_dict)

        request_json = self._prepare_instance_json()

        return self._update_instance_properties_request(request_json)
