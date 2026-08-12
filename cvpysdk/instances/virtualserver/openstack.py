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

OpenStackinstance is the only class defined in this file.

OpenStackInstance:     Derived class from VirtualServer  Base class, representing a
                        Openstack instance, and to perform operations on that instance


OpenStackInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of vmware Instance object
                                                associated with the VirtualServer Instance


    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get openstack specific instance properties

    _get_instance_properties_json()     --  get the all instance(vmware)
                                                related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class OpenStackInstance(VirtualServerInstance):
    """
    Represents an OpenStack instance managed by the Virtual Server agent.

    This class provides an interface for handling OpenStack virtual server instances,
    allowing retrieval and management of instance properties and metadata. It includes
    methods for initializing the instance with specific parameters, accessing instance
    properties in both object and JSON formats, and retrieving key attributes such as
    server host name, username, and server name.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Retrieval of instance properties as objects and JSON
        - Access to server host name, username, and server name via properties

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize an OpenStackInstance object for the specified Virtual Server instance.

        Args:
            agent_object: Instance of the Agent class associated with this OpenStack instance.
            instance_name: The name of the OpenStack instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, it can be set later.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> openstack_instance = OpenStackInstance(agent, 'MyOpenStackInstance', '101')
            >>> # The OpenStackInstance object is now initialized and ready for use

        #ai-gen-doc
        """
        self._vendor_id = 12
        self._server_name = []
        self._server_host_name = []
        super(OpenStackInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this OpenStack instance.

        This method fetches the latest properties for the current OpenStack instance
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        #ai-gen-doc
        """
        super(OpenStackInstance, self)._get_instance_properties()

        if 'virtualServerInstance' in self._properties:
            self._server_host_name = [self._properties["virtualServerInstance"] \
                                                ["vmwareVendor"]["virtualCenter"]["domainName"]]
            self._server_name.append(self._instance['clientName'])

            _member_servers = self._properties["virtualServerInstance"] \
                                                ["associatedClients"]["memberServers"]

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all properties related to this OpenStack instance subclient.

        Returns:
            dict: A dictionary containing all instance properties for the subclient.

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
        """Get the server host name (domain name) from the OpenStack vendor JSON.

        Returns:
            The domain name as a string extracted from the OpenStack vendor JSON.

        Example:
            >>> instance = OpenStackInstance()
            >>> host_name = instance.server_host_name  # Use dot notation for property access

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def server_name(self) -> list:
        """Get the server name associated with the OpenStack instance.

        This property retrieves the domain name as specified in the VMware vendor JSON configuration.

        Returns:
            The server (domain) name as a list.

        Example:
            >>> instance = OpenStackInstance()
            >>> name = instance.server_name
            >>> print(f"OpenStack server name: {name}")

        #ai-gen-doc
        """
        return self._server_name
