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
Module for operating on a Virtual Server Morpheus Server Instance.

This module defines the MorpheusInstance class, which is a subclass of
VirtualServerInstance. It provides functionality specific to managing
Morpheus virtual server instances within the Commvault framework.

Classes:
    MorpheusInstance -- Represents a Morpheus virtual server instance and
                         provides methods to get and set instance properties.
"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from ...agent import Agent


class MorpheusInstance(VirtualServerInstance):
    """
    Represents a Morpheus instance of the Virtual Server agent.

    This class extends the VirtualServerInstance base class to provide
    specialized functionality for managing Morpheus server instances.
    It encapsulates properties and methods for handling instance-specific
    details such as server name, host name, and vendor identification.

    Key Features:
        - Initialization of Morpheus instance with agent, name, and ID
        - Retrieval of instance properties and properties in JSON format
        - Access and modification of server host name via property methods
        - Access to server name via property
        - Maintains vendor ID specific to Morpheus (fixed as 27)
        - Stores associated client name and host name information

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a MorpheusInstance object.

        Args:
            agent: Instance of the Agent class associated with this Morpheus instance.
            instance_name: The name of the Morpheus instance.
            instance_id: Optional integer ID of the instance. If not provided, defaults to None.

        Attributes Set:
            _vendor_id: Vendor ID specific to Morpheus.
            _server_name: Name of the associated client.
            _server_host_name: Host name of the associated client.

        Example:
            >>> agent = Agent()
            >>> morpheus_instance = MorpheusInstance(agent, "TestInstance", '101')

        #ai-gen-doc
        """
        super(MorpheusInstance, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 27
        self._server_name = [
            self._virtualserverinstance['associatedClients']['memberServers'][0]['client'].get('clientName')
        ]
        self._server_host_name = [
            self._virtualserverinstance['associatedClients']['memberServers'][0]['client'].get('hostName')
        ]

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the Morpheus instance.

        This method overrides the base class implementation to fetch and store
        Morpheus-specific instance properties. It is typically used internally
        to ensure the instance has the latest configuration and metadata.

        Raises:
            SDKException: If the response from the server is not empty or not successful.

        Example:
            >>> instance = MorpheusInstance()
            >>> instance._get_instance_properties()

        #ai-gen-doc
        """
        super(MorpheusInstance, self)._get_instance_properties()

    def _get_instance_properties_json(self) -> dict:
        """Construct the JSON representation of the instance properties.

        Returns:
            dict: A dictionary containing all relevant properties of the Morpheus instance.

        Example:
            >>> instance = MorpheusInstance()
            >>> properties_json = instance._get_instance_properties_json()
            >>> print(properties_json)
            {'property1': 'value1', 'property2': 'value2', ...}

        #ai-gen-doc
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
    def server_host_name(self) -> List[str]:
        """Get the host name(s) of the associated Morpheus server.

        Returns:
            List[str]: A list containing the host names of the Morpheus server associated with this instance.

        Example:
            >>> instance = MorpheusInstance()
            >>> host_names = instance.server_host_name
            >>> print(host_names)
            ['morpheus-server1.example.com', 'morpheus-server2.example.com']

        #ai-gen-doc
        """
        return self._server_host_name

    @server_host_name.setter
    def server_host_name(self, value: list) -> None:
        """Set the host name(s) of the Morpheus server.

        Args:
            value: A list of host names to assign to the Morpheus server.

        Example:
            >>> instance = MorpheusInstance()
            >>> instance.server_host_name = ["server1.example.com", "server2.example.com"]
            >>> # The server_host_name property is now set to the provided list of host names

        #ai-gen-doc
        """
        self._server_host_name = value

    @property
    def server_name(self) -> List[str]:
        """Get the name(s) of the associated Morpheus server(s).

        Returns:
            List[str]: A list containing the names of the Morpheus servers associated with this instance.

        Example:
            >>> instance = MorpheusInstance()
            >>> names = instance.server_name  # Use dot notation for property access
            >>> print(f"Associated server names: {names}")
            >>> # Output might be: ['morpheus-server-01', 'morpheus-server-02']

        #ai-gen-doc
        """
        return self._server_name
