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

"""
File for operating on a Virtual Server Proxmox Server Instance.

ProxmoxVEInstance is the only class defined in this file.

ProxmoxVEInstance: Derived class from VirtualServer  Base class, representing a
                           Proxmox Server instance, and to perform operations on that instance

ProxmoxVEInstance:

    __init__(agent_object,instance_name,instance_id)    -- initialize object of FusionCompute
                                                            Instance object associated with the
                                                            VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Proxmox Server specific
                                                            instance properties as well

    _set_instance_properties()                          --  Proxmox VE Instance class method
                                                            to set Proxmox Specific instance properties

"""

from ..vsinstance import VirtualServerInstance


class ProxmoxVEInstance(VirtualServerInstance):
    """
    Class for representing an Proxmox VE instance of the Virtual Server agent.

    """

    def __init__(self, agent, instance_name, instance_id=None):
        """
        Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (agent_object,instance_name,instance_id)  --  instance of the
                                                                            Agent class,
                                                                            instance name,
                                                                            instance id

        """
        super(ProxmoxVEInstance, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 23 
        self._server_name = [self._virtualserverinstance['associatedClients']['memberServers'][0]['client'].get('clientName')]
        self._server_host_name = [self._virtualserverinstance['associatedClients']['memberServers'][0]['client'].get('hostName')]


    def _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(ProxmoxVEInstance, self)._get_instance_properties()

    def _get_instance_properties_json(self):
        """
        Get the all instance related properties of this subclient.

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
                    "associatedClients": self._virtualserverinstance['associatedClients']
                }
            }
        }
        return instance_json

    @property
    def server_host_name(self):
        """
        Getter for server_host_name property
        """
        return self._server_host_name

    @server_host_name.setter
    def server_host_name(self, value):
        """
        Setter for server_host_name property
        """
        self._server_host_name = value

    @property
    def server_name(self):
        """
        Getter for the server_name property
        """
        return self._server_name
