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

"""File for operating on a Virtual Server Fusion Compute Instance.

FusionComputeInstance is the only class defined in this file.

FusionComputeInstance: Derived class from VirtualServer  Base class, representing a
                           Fusion Compute instance, and to perform operations on that instance

HyperVInstance:

    __init__(agent_object,instance_name,instance_id)    -- initialize object of FusionCompute
                                                                Instance object associated with the
                                                                        VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Fusion Compute
                                                            Specific instance properties as well

    _set_instance_properties()                          --  Fusion Compute Instance class method
                                                                to set Fusion Compute
                                                                Specific instance properties


"""

from ..vsinstance import VirtualServerInstance


class FusionComputeInstance(VirtualServerInstance):
    """Class for representing a Fusion Compute of the Virtual Server agent."""

    def __init__(self, agent, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (agent_object,instance_name,instance_id)  --  instance of the
                                                                                Agent class,
                                                                                instance name,
                                                                                instance id

        """

        self._vendor_id = 14
        self._server_name = []
        self._vmwarvendor = None
        self._server_host_name = []
        super(FusionComputeInstance, self).__init__(agent, instance_name, instance_id)

    def _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(FusionComputeInstance, self)._get_instance_properties()
        if "vmwareVendor" in self._virtualserverinstance:
            self._vmwarvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']

            self._server_name.append(self._instance['clientName'])

            self._server_host_name.append(self._vmwarvendor["domainName"])

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
        """return the Fusion compute VRM  associated with the PseudoClient"""
        return self._server_host_name

    @property
    def server_name(self):
        """getter for the domain name in the vmware vendor json"""
        return self._server_name

    @property
    def _user_name(self):
        """getter for the username from the vmware vendor json"""
        return self._vmwarvendor.get("userName", "")
