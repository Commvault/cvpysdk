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

"""File for operating on a Virtual Server OracleVM Instance.

OracleVMInstance is the only class defined in this file.

OracleVMInstance:     Derived class from VirtualServer  Base class, representing a
                        OracleVM instance, and to perform operations on that instance


OracleVMInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of oraclevm Instance object
                                                associated with the VirtualServer Instance


    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get oraclevm specific instance properties

    _get_instance_properties_json()     --  get the all instance(oraclevm)
                                                related properties of this subclient

"""


from ..vsinstance import VirtualServerInstance

class OracleVMInstance(VirtualServerInstance):

    """Class for representing VMWare instance of the Virtual Server agent."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                agent_object    (object)    --  instance of the Agent class

                instance_name   (str)       --  instance name

                instance_id     (int)       --  instance id

        """
        self._vendor_id = 10
        self._vmwarvendor = None
        self._server_name = []
        self._server_host_name = []
        super(OracleVMInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(OracleVMInstance, self)._get_instance_properties()

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
        """getter for the domain name in the OracleVM vendor json"""
        return ["vmcontrol.commvault.com"]


    @property
    def server_name(self):
        """return the Oracle client associated with the PseudoClient"""
        # TODO will change with Praveen Form(rsn)
        return ["vmcontrol.commvault.com"]
