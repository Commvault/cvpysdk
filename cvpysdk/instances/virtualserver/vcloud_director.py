#!/usr/bin/env python
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

"""File for operating on a Virtual Server Vcloud Instance.

vcloudInstance is the only class defined in this file.

vcloudInstance:     Derived class from VirtualServer  Base class, representing a
                        Vcloud instance, and to perform operations on that instance


vcloudInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of Vcloud Instance object
                                                associated with the VirtualServer Instance


    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get vcloud specific instance properties

    _get_instance_properties_json()     --  get the all instance(vcloud)
                                                related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class vcloudInstance(VirtualServerInstance):
    """
    Represents a VCloud instance within the Virtual Server agent framework.

    This class encapsulates the properties and behaviors specific to a VCloud
    instance, providing mechanisms to initialize the instance, retrieve its
    properties, and access key attributes such as server host name, username,
    and server name. It is designed to interact with the underlying Virtual
    Server agent infrastructure, enabling management and inspection of VCloud
    instance configurations.

    Key Features:
        - Initialization of VCloud instance with agent object, name, and ID
        - Retrieval of instance properties and their JSON representation
        - Access to server host name, username, and server name via properties

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a vCloud Instance object for the specified Virtual Server instance.

        Args:
            agent_object: An instance of the Agent class representing the associated agent.
            instance_name: The name of the vCloud instance.
            instance_id: Optional; the unique identifier for the vCloud instance. If not provided, it may be set later.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> vcloud_instance = vcloudInstance(agent, 'vCloud_Instance1', '101')
            >>> # The vcloud_instance object is now initialized and ready for further operations

        #ai-gen-doc
        """
        self._vendor_id = 103
        self._vmwarvendor = None
        self._server_name = []
        self._server_host_name = []
        self._vcloudvendor = {}
        super(vcloudInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this vCloud instance.

        This method fetches the latest properties for the vCloud instance and updates the instance's internal state.
        It should be called to ensure the instance has the most current configuration and status information.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        #ai-gen-doc
        """
        super(vcloudInstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._vcloudvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']

            self._server_name.append(self._instance['clientName'])

            self._server_host_name.append(self._vcloudvendor["domainName"])

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all properties associated with this vCloud instance subclient.

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
        """Get the domain name (server host name) from the Vcloud vendor JSON configuration.

        Returns:
            The domain name or server host name as a list.

        Example:
            >>> vcloud = vcloudInstance()
            >>> host_name = vcloud.server_host_name  # Access the property
            >>> print(f"Vcloud server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def _user_name(self) -> str:
        """Get the username from the Vcloud vendor JSON configuration.

        Returns:
            The username as a string extracted from the Vcloud vendor JSON.

        #ai-gen-doc
        """
        return self._vcloudvendor["userName"]

    @property
    def server_name(self) -> list:
        """Get the domain name (server name) from the Vcloud vendor JSON configuration.

        Returns:
            The domain name (server name) as a list.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> vcloud = vcloudInstance(agent, 'instance_name', 'instance_id')
            >>> vcloud._get_instance_properties()
            >>> domain = vcloud.server_name  # Access the server name property
            >>> print(f"Vcloud server domain: {domain}")

        #ai-gen-doc
        """
        return self._server_name
