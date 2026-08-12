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

"""File for operating on a Virtual Server Azure Instance.

AzureInstance is the only class defined in this file.

AzureInstance: Derived class from VirtualServer  Base class, representing a
                           Azure instance, and to perform operations on that instance

AzureInstance:

        _init_(self, agent, name, iid)      -- initialize object of azure Instance
                                        object associated with the VirtualServer Instance

        _get_instance_properties()          --  VirtualServer Instance class method
                                            overwritten to get Azure classic
                                            Specific instance properties as well


"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class AzureInstance(VirtualServerInstance):
    """
    Represents an Azure virtual server instance within the virtualization management framework.

    This class provides mechanisms to interact with and manage Azure-based virtual server instances.
    It allows for initialization with agent and instance details, retrieval of instance properties,
    and access to server-specific information such as server name and host name.

    Key Features:
        - Initialization with agent, name, and instance ID
        - Retrieval of instance properties in both standard and JSON formats
        - Access to server name and server host name via properties

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', name: str, iid: str) -> None:
        """Initialize an AzureInstance object for the specified Virtual Server instance.

        Args:
            agent: An instance of the Agent class representing the associated agent.
            name: The name of the virtual server instance.
            iid: The unique identifier (ID) of the virtual server instance.

        Example:
            >>> agent = Agent(client_object, "Virtual Server")
            >>> azure_instance = AzureInstance(agent, "AzureVMInstance", '101')

        #ai-gen-doc
        """

        super(AzureInstance, self).__init__(agent, name, iid)
        self._vendor_id = 5

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Azure instance.

        This method fetches the latest properties for the Azure instance and updates the instance's internal state.
        It raises an SDK Exception if the response is not empty or if the response indicates a failure.

        Raises:
            SDK Exception: If the response is not empty or if the response is not successful.

        #ai-gen-doc
        """

        super(AzureInstance, self)._get_instance_properties()
        self._server_name = []

        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                                                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this Azure subclient.

        Returns:
            dict: A dictionary containing all properties associated with this instance.

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
                    "vmwareVendor": {}
                    }
                       }
               }
        return instance_json

    @property
    def server_name(self) -> list:
        """Get the server (domain) name from the Hyper-V JSON configuration.

        Returns:
            The domain name as a string extracted from the Hyper-V JSON.

        Example:
            >>> azure_instance = AzureInstance()
            >>> domain = azure_instance.server_name
            >>> print(f"Domain name: {domain}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def server_host_name(self) -> list:
        """Get the domain name (server host name) from the VMware vendor JSON.

        Returns:
            The server host name as a string.

        Example:
            >>> azure_instance = AzureInstance()
            >>> host_name = azure_instance.server_host_name
            >>> print(f"Server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_name
