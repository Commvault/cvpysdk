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

"""File for operating on a Virtual Server VMware Instance.

RhevInstance is the only class defined in this file.

RhevInstance:     Derived class from VirtualServer  Base class, representing a
                        VMware instance, and to perform operations on that instance


RhevInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of Rhev Instance object
                                                associated with the RhevInstance Instance


    _get_instance_properties()          --  Rhev Instance class method overwritten
                                                to get vmware specific instance properties

    _get_instance_properties_json()     --  get the all instance(rhev)
                                                related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class RhevInstance(VirtualServerInstance):
    """
    Represents a RHEV (Red Hat Enterprise Virtualization) instance within the Virtual Server agent framework.

    This class encapsulates the properties and behaviors specific to a RHEV virtual server instance,
    providing mechanisms to access and manage instance details, properties, and configuration data.
    It offers property accessors for key instance attributes and methods to retrieve instance properties
    in both object and JSON formats.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Retrieval of instance properties as objects and JSON
        - Access to server host name, username, and server name via properties

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a RhevInstance object for the specified Virtual Server instance.

        Args:
            agent_object: An instance of the Agent class associated with this virtual server.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, it may be determined automatically.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> rhev_instance = RhevInstance(agent, 'MyRhevInstance', '101')
            >>> # The RhevInstance object is now initialized and ready for use

        #ai-gen-doc
        """
        self._vendor_id = 501
        self._server_name = []
        self._server_host_name = []
        super(RhevInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this RhevInstance.

        This method fetches the current properties of the instance from the backend
        and updates the internal state accordingly.

        Raises:
            SDKException: If the response is empty or the response indicates failure.

        #ai-gen-doc
        """
        super(RhevInstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._vmwarvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']

            self._server_name.append(self._instance['clientName'])

            self._server_host_name.append(self._vmwarvendor["domainName"])

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
                    "vmwareVendor": self._virtualserverinstance['vmwareVendor']
                }
            }
        }

        return instance_json

    @property
    def server_host_name(self) -> list:
        """Get the domain name of the server from the VMware vendor JSON.

        Returns:
            The domain name of the server as a list.

        Example:
            >>> instance = RhevInstance()
            >>> domain_name = instance.server_host_name  # Use dot notation for property access
            >>> print(f"Server domain name: {domain_name}")

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def _user_name(self) -> str:
        """Get the username from the VMware vendor JSON configuration.

        Returns:
            The username as a string extracted from the vendor JSON.

        Example:
            >>> instance = RhevInstance()
            >>> username = instance._user_name  # Use dot notation for property access
            >>> print(f"Username: {username}")

        #ai-gen-doc
        """
        return self._vmwarvendor["userName"]

    @property
    def server_name(self) -> list:
        """Get the domain name associated with the RHEV instance from the VMware vendor JSON.

        Returns:
            The domain name as a list.

        Example:
            >>> instance = RhevInstance()
            >>> domain = instance.server_name  # Access the server name property
            >>> print(f"RHEV domain name: {domain}")

        #ai-gen-doc
        """
        return self._server_name
