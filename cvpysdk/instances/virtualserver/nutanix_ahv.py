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

"""File for operating on a Virtual Server Nutanix AHV Instance.

nutanixinstance is the only class defined in this file.

nutanixinstance:            Derived class from VirtualServer
                            Base class, representing a Nutanix AHV
                            instance, and to perform operations on that
                            instance

    __init__(self, agent,_name,iid)   	 --   initialize object of Nutanix AHV
                                              Instance object associated with the
                                              VirtualServer Instance

    _get_instance_properties()           --  VirtualServer Instance class method
                                             overwritten to get nutanix AHV
                                            Specific instance properties as well

    _get_instance_properties_json()		 --  get the all instance related
                                                properties of this subclient.

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class nutanixinstance(VirtualServerInstance):
    """
    Represents a Nutanix AHV instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to a Nutanix AHV
    virtual server instance, providing mechanisms to retrieve and manage instance
    properties, as well as access key configuration details such as server host name,
    Nutanix cluster, and associated username.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access to server host name, Nutanix cluster, and username via properties

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', name: str, iid: str) -> None:
        """Initialize a nutanixinstance object for the specified Virtual Server instance.

        Args:
            agent: The agent class instance associated with this Virtual Server instance.
            name: The name of the Virtual Server instance.
            iid: The unique identifier (ID) for the Virtual Server instance.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> instance = nutanixinstance(agent, 'Nutanix_Instance_01', '101')

        #ai-gen-doc
        """
        self._nutanix_cluster = None
        self._username = None
        self._server_name = []
        self._vendor_id = 601
        super(nutanixinstance, self).__init__(agent, name, iid)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Nutanix instance.

        This method fetches the current properties of the Nutanix instance and updates the internal state accordingly.
        It raises an SDK Exception if the response is not empty or if the response indicates a failure.

        Raises:
            SDK Exception: If the response is not empty or if the response is not successful.

        #ai-gen-doc
        """

        super(nutanixinstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._nutanix_cluster = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']

        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))

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
    def server_host_name(self) -> list:
        """Get the server host name associated with this Nutanix instance.

        Returns:
            The host name of the server as a string.

        Example:
            >>> instance = nutanixinstance()
            >>> host_name = instance.server_host_name  # Use dot notation for property access
            >>> print(f"Server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def nutanix_cluster(self) -> str:
        """Get the Nutanix cluster associated with this instance.

        Returns:
            The name of the Nutanix cluster as a string.

        Example:
            >>> instance = nutanixinstance()
            >>> cluster_name = instance.nutanix_cluster  # Access the Nutanix cluster property
            >>> print(f"Nutanix cluster: {cluster_name}")

        #ai-gen-doc
        """
        return self._nutanix_cluster

    @property
    def username(self) -> str:
        """Get the username associated with the Nutanix cluster instance.

        Returns:
            The username as a string.

        Example:
            >>> nutanix = nutanixinstance()
            >>> user = nutanix.username  # Access the username property
            >>> print(f"Nutanix cluster username: {user}")

        #ai-gen-doc
        """
        return self._username
