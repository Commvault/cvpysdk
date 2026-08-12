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

VMwareInstance is the only class defined in this file.

VMwareInstance:     Derived class from VirtualServer  Base class, representing a
                        VMware instance, and to perform operations on that instance


VMwareInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of vmware Instance object
                                                associated with the VirtualServer Instance


    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get vmware specific instance properties

    _get_instance_properties_json()     --  get the all instance(vmware)
                                                related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class VMwareInstance(VirtualServerInstance):
    """
    Represents a VMware instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to a VMware
    virtual server instance, providing mechanisms to retrieve and manage
    instance properties and metadata. It is designed to interface with the
    broader Virtual Server agent framework, allowing for seamless integration
    and management of VMware environments.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access to server host name, username, and server name via properties

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a VMwareInstance object for the specified Virtual Server instance.

        Args:
            agent_object: An instance of the Agent class representing the associated agent.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, it may be determined automatically.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> vmware_instance = VMwareInstance(agent, 'VM_Instance_01', '123')
            >>> # The VMwareInstance object is now initialized and ready for use

        #ai-gen-doc
        """
        self._vendor_id = 1
        self._vmwarvendor = None
        self._server_name = []
        self._server_host_name = []
        super(VMwareInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this VMware instance.

        This method fetches the current configuration and properties for the VMware instance
        and updates the internal state accordingly.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        #ai-gen-doc
        """
        super(VMwareInstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._vmwarvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']

            self._server_name.append(self._instance['clientName'])

            self._server_host_name.append(self._vmwarvendor["domainName"])

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all properties associated with this VMware instance.

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
        """Get the domain name (server host name) from the VMware vendor JSON.

        Returns:
            The domain name or server host name as a list.

        Example:
            >>> vmware_instance = VMwareInstance()
            >>> host_name = vmware_instance.server_host_name
            >>> print(f"VMware server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def _user_name(self) -> str:
        """Get the username from the VMware vendor JSON configuration.

        Returns:
            The username string extracted from the VMware vendor JSON.

        Example:
            >>> instance = VMwareInstance()
            >>> username = instance._user_name
            >>> print(f"VMware username: {username}")

        #ai-gen-doc
        """
        return self._vmwarvendor.get('userName') or self._credential.get('userName', '')

    @property
    def server_name(self) -> list:
        """Get the domain name from the VMware vendor JSON.

        Returns:
            The domain name associated with this VMware instance as a list.

        Example:
            >>> vmware_instance = VMwareInstance()
            >>> domain = vmware_instance.server_name
            >>> print(f"VMware domain name: {domain}")

        #ai-gen-doc
        """
        return self._server_name
