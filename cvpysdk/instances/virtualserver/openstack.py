# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server VMware Instance.

OpenStackinstance is the only class defined in this file.

OpenStackInstance:     Derived class from VirtualServer  Base class, representing a
                        Openstack instance, and to perform operations on that instance


OpenStackInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of vmware Instance object
                                                associated with the VirtualServer Instance


    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get openstack specific instance properties

    _get_instance_properties_json()     --  get the all instance(vmware)
                                                related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance


class OpenStackInstance(VirtualServerInstance):
    """Class for representing VMWare instance of the Virtual Server agent."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                agent_object    (object)    --  instance of the Agent class

                instance_name   (str)       --  instance name

                instance_id     (int)       --  instance id

        """
        self._vendor_id = 12
        self._server_name = []
        self._server_host_name = []
        super(OpenStackInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(OpenStackInstance, self)._get_instance_properties()

        if 'virtualServerInstance' in self._properties:
            self._server_host_name = [self._properties["virtualServerInstance"] \
                                                ["vmwareVendor"]["virtualCenter"]["domainName"]]
            self._server_name.append(self._instance['clientName'])

            _member_servers = self._properties["virtualServerInstance"] \
                                                ["associatedClients"]["memberServers"]

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
        """getter for the domain name in the vmware vendor json"""
        return self._server_host_name

    @property
    def _user_name(self):
        """getter for the username from the vmware vendor json"""
        return self._vmwarvendor["userName"]

    @property
    def server_name(self):
        """getter for the domain name in the vmware vendor json"""
        return self._server_name
