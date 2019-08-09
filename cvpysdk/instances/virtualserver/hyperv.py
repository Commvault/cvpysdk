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

"""File for operating on a Virtual Server Hyper-V Instance.

HyperVInstance is the only class defined in this file.

HyperVInstance: Derived class from VirtualServer  Base class, representing a
                           Hypeer-V instance, and to perform operations on that instance

HyperVInstance:

    __init__(agent_object,instance_name,instance_id)    --  initialize object of hyper-v Instance
                                                                object associated with the
                                                                        VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Hyper-V Specific
                                                                         instance properties as well

    _set_instance_properties()                          --  Hyper-V Instance class method  to
                                                        set Hyper-V Specific instance properties


"""


from ..vsinstance import VirtualServerInstance

class HyperVInstance(VirtualServerInstance):
    """Class for representing an Hyper-V of the Virtual Server agent."""

    def __init__(self, agent, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (agent_object,instance_name,instance_id)  --  instance of the
                                                                                Agent class,
                                                                                instance name,
                                                                                instance id

        """
        super(HyperVInstance, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 2



    def  _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(HyperVInstance, self)._get_instance_properties()
        self._server_name = []

        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                                                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))


    def _get_instance_properties_json(self):
        """get the all instance related properties of this subclient.

          Returns:
               dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties":{
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
    def server_name(self):
        """getter for the domain name in the Hyper-V json"""
        return self._server_name

    @property
    def server_host_name(self):
        """getter for the domain name in the vmware vendor json"""
        return self._server_name


