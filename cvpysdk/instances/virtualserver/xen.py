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

"""File for operating on a Virtual Server Xen Server Instance.

XenServer Instance is the only class defined in this file.

XenInstance: Derived class from VirtualServer  Base class, representing a
                           Xen Server instance, and to perform operations on that instance

XenInstance:

    __init__(agent_object,instance_name,instance_id)    -- initialize object of FusionCompute
                                                            Instance object associated with the
                                                            VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Xen Server specific
                                                            instance properties as well

    _set_instance_properties()                          --  Xen Server Instance class method
                                                            to set Xen Specific instance properties


"""

from ..vsinstance import VirtualServerInstance


class Xen(VirtualServerInstance):
    """Class for representing an Xen Server instance of the Virtual Server agent."""

    def __init__(self, agent, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (agent_object,instance_name,instance_id)  --  instance of the
                                                                            Agent class,
                                                                            instance name,
                                                                            instance id

        """
        super(Xen, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 3
        self._server_name = None
        self._server_host_name = None

    def _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(Xen, self)._get_instance_properties()
        self._server_name = self._instance.get('clientName', '')

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
                    "vmwareVendor": {}
                }
            }
        }
        return instance_json

    @property
    def server_host_name(self):
        """Getter for server_host_name property"""
        # This property will be set during TC execution. 
        return self._server_host_name

    @server_host_name.setter
    def server_host_name(self, value):
        """Setter for server_host_name property"""
        self._server_host_name = value

    @property
    def server_name(self):
        """Getter for the server_name property"""
        return self._server_name
