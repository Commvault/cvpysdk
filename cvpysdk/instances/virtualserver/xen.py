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

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class Xen(VirtualServerInstance):
    """
    Represents a Xen Server instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to a Xen Server
    instance, providing mechanisms to retrieve and manage instance properties,
    as well as access and modify server host and server names. It is designed to
    integrate with the broader Virtual Server agent framework.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access and modification of the server host name via property
        - Access to the server name via property

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize the Xen Instance object for a given Virtual Server instance.

        Args:
            agent: An instance of the Agent class representing the associated agent.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, a default may be used.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> xen_instance = Xen(agent, 'XenInstance01', '12345')
            >>> # The Xen instance is now initialized and ready for further operations

        #ai-gen-doc
        """
        super(Xen, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 3
        self._server_name = None
        self._server_host_name = None

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the current Xen instance.

        This method fetches the latest properties for the Xen instance and updates the internal state accordingly.

        Raises:
            SDKException: If the response is not empty or the response indicates failure.

        #ai-gen-doc
        """

        super(Xen, self)._get_instance_properties()
        self._server_name = self._instance.get('clientName', '')

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient as a dictionary.

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
    def server_host_name(self) -> str:
        """Get the host name of the Xen server.

        Returns:
            The host name of the Xen server as a string.

        Example:
            >>> xen = Xen()
            >>> host_name = xen.server_host_name  # Access the server host name property
            >>> print(f"Xen server host name: {host_name}")

        #ai-gen-doc
        """
        # This property will be set during TC execution. 
        return self._server_host_name

    @server_host_name.setter
    def server_host_name(self, value: str) -> None:
        """Set the Xen server host name.

        Args:
            value: The host name to assign to the Xen server.

        Example:
            >>> xen = Xen()
            >>> xen.server_host_name = "xen-server-01.example.com"  # Use assignment for property setter
            >>> # The Xen server host name is now set to "xen-server-01.example.com"

        #ai-gen-doc
        """
        self._server_host_name = value

    @property
    def server_name(self) -> str:
        """Get the name of the Xen server associated with this instance.

        Returns:
            The server name as a string.

        Example:
            >>> xen = Xen()
            >>> name = xen.server_name  # Use dot notation to access the property
            >>> print(f"Xen server name: {name}")

        #ai-gen-doc
        """
        return self._server_name
