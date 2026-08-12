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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class FusionComputeInstance(VirtualServerInstance):
    """
    Represents a Fusion Compute instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to a Fusion Compute
    instance, providing mechanisms to initialize the instance, retrieve its properties,
    and access key server-related information. It is designed to interact with the
    underlying agent and manage instance-specific data.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties in both standard and JSON formats
        - Access to server host name and server name via properties
        - Access to the associated username via a protected property

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a FusionComputeInstance object for the specified Virtual Server instance.

        Args:
            agent: An instance of the Agent class representing the associated agent.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, a default or auto-generated ID may be used.

        Example:
            >>> agent = Agent(client_object, "Virtual Server")
            >>> instance = FusionComputeInstance(agent, "MyInstance", "12345")

        #ai-gen-doc
        """

        self._vendor_id = 14
        self._server_name = []
        self._vmwarvendor = None
        self._server_host_name = []
        super(FusionComputeInstance, self).__init__(agent, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this FusionCompute instance.

        This method fetches the latest properties for the FusionCompute instance and updates
        the internal state accordingly. It should be called to ensure the instance properties
        are current.

        Raises:
            SDKException: If the response is not empty or the response indicates a failure.

        #ai-gen-doc
        """

        super(FusionComputeInstance, self)._get_instance_properties()
        if "vmwareVendor" in self._virtualserverinstance:
            self._vmwarvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']

            self._server_name.append(self._instance['clientName'])

            self._server_host_name.append(self._vmwarvendor["domainName"])

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all properties associated with this FusionCompute instance.

        #ai-gen-doc
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
    def server_host_name(self) -> list:
        """Get the FusionCompute VRM server host name associated with the PseudoClient.

        Returns:
            The host name of the FusionCompute VRM server as a string.

        Example:
            >>> instance = FusionComputeInstance()
            >>> vrm_host = instance.server_host_name
            >>> print(f"VRM Host Name: {vrm_host}")
        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def server_name(self) -> list:
        """Get the server name (domain name) from the FusionCompute vendor JSON.

        Returns:
            The domain name as a list.

        Example:
            >>> instance = FusionComputeInstance()
            >>> domain = instance.server_name
            >>> print(f"FusionCompute domain name: {domain}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def _user_name(self) -> str:
        """Get the username from the VMware vendor JSON configuration.

        Returns:
            The username as a string extracted from the VMware vendor JSON.

        Example:
            >>> instance = FusionComputeInstance()
            >>> username = instance._user_name
            >>> print(f"VMware username: {username}")

        #ai-gen-doc
        """
        return self._vmwarvendor.get("userName", "")
