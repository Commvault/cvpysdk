#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Vcloud Instance.

vcloudInstance is the only class defined in this file.

vcloudInstance:     Derived class from VirtualServer  Base class, representing a
                        Vcloud instance, and to perform operations on that instance


vcloudInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of Vcloud Instance object
                                                associated with the VirtualServer Instance


    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get vcloud specific instance properties

    _get_instance_properties_json()     --  get the all instance(vcloud)
                                                related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance
from ...instance import Instance


class vcloudInstance(VirtualServerInstance):
    """Class for representing VCloud instance of the Virtual Server agent."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                agent_object    (object)    --  instance of the Agent class

                instance_name   (str)       --  instance name

                instance_id     (int)       --  instance id

        """
        self._vendor_id = 103
        self._vmwarvendor = None
        self._server_name = []
        self._server_host_name = []
        self._vcloudvendor = {}
        super(vcloudInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(vcloudInstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._vcloudvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']

            self._server_name.append(self._instance['clientName'])

            self._server_host_name.append(self._vcloudvendor["domainName"])

    def _get_instance_properties_json(self):
        """get the all instance related properties of this subclient.

           Returns:
                dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties": {
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "virtualServerInstance": {
                    "vsInstanceType": self._virtualserverinstance['vsInstanceType'],
                    "associatedClients": self._virtualserverinstance['associatedClients'],
                    "vmwareVendor": self._virtualserverinstance['vmwareVendor']
                }
            }
        }

        return instance_json

    @property
    def server_host_name(self):
        """getter for the domain name in the Vcloud vendor json"""
        return self._server_host_name

    @property
    def _user_name(self):
        """getter for the username from the Vcloud vendor json"""
        return self._vcloudvendor["userName"]

    @property
    def server_name(self):
        """getter for the domain name in the Vcloud vendor json"""
        return self._server_name
