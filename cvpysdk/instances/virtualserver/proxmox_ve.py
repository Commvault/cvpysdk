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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class ProxmoxVEInstance(VirtualServerInstance):
    """
    Represents a Proxmox VE instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to a Proxmox VE
    virtual server instance. It provides mechanisms to initialize the instance with
    relevant identifiers, retrieve instance properties in both standard and JSON formats,
    and manage server host and server name attributes.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties
        - Retrieval of instance properties in JSON format
        - Access and modification of server host name via property
        - Access to server name via property

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a ProxmoxVEInstance object for the specified Virtual Server instance.

        Args:
            agent: An instance of the Agent class representing the associated agent.
            instance_name: The name of the Proxmox VE instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, a default or auto-generated ID may be used.

        Example:
            >>> agent = Agent(client_object, "Virtual Server")
            >>> proxmox_instance = ProxmoxVEInstance(agent, "Proxmox_Instance_01", "12345")
            >>> # The ProxmoxVEInstance object is now initialized and ready for use

        #ai-gen-doc
        """
        super(ProxmoxVEInstance, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 23 
        self._server_name = [self._virtualserverinstance['associatedClients']['memberServers'][0]['client'].get('clientName')]
        self._server_host_name = [self._virtualserverinstance['vmwareVendor']['virtualCenter']['domainName']]

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Proxmox VE instance.

        This method fetches the current properties of the Proxmox VE instance and updates
        the internal state accordingly. It raises an exception if the response is empty
        or if the response indicates a failure.

        Raises:
            SDKException: If the response is empty or the request is unsuccessful.

        #ai-gen-doc
        """

        super(ProxmoxVEInstance, self)._get_instance_properties()

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient.

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
                    "associatedClients": self._virtualserverinstance['associatedClients']
                }
            }
        }
        return instance_json

    @property
    def server_host_name(self) -> list:
        """Get the host name of the Proxmox VE server associated with this instance.

        Returns:
            The server host name as a string.

        Example:
            >>> proxmox_instance = ProxmoxVEInstance()
            >>> host_name = proxmox_instance.server_host_name
            >>> print(f"Proxmox server host: {host_name}")

        #ai-gen-doc
        """
        return self._server_host_name

    @server_host_name.setter
    def server_host_name(self, value: str) -> None:
        """Set the server host name for the ProxmoxVEInstance.

        Args:
            value: The new host name to assign to the server.

        Example:
            >>> instance = ProxmoxVEInstance()
            >>> instance.server_host_name = "proxmox01.example.com"  # Use assignment for property setter
            >>> # The server host name is now set to "proxmox01.example.com"

        #ai-gen-doc
        """
        self._server_host_name = value

    @property
    def server_name(self) -> list:
        """Get the name of the Proxmox VE server associated with this instance.

        Returns:
            The server name as a list.

        Example:
            >>> instance = ProxmoxVEInstance()
            >>> name = instance.server_name  # Access the server name property
            >>> print(f"Proxmox VE server name: {name}")

        #ai-gen-doc
        """
        return self._server_name
