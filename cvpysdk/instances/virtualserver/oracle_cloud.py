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

"""File for operating on a Virtual Server Oracle Cloud Instance.

OracleCloudInstance is the only class defined in this file.

OracleCloudInstance: Derived class from VirtualServer  Base class, representing a
                           Oracle Cloud instance, and to perform operations on that instance

OracleCloudInstance:

    __init__(agent_object,instance_name,instance_id)    --  initialize object of Oracle Cloud
                                                            Instance object associated with the
                                                            VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Oracle Cloud
                                                            Specific instance properties as well

    _set_instance_properties()                          --  Oracle Cloud Instance class method
                                                            to set Oracle Cloud
                                                            Specific instance properties


"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class OracleCloudInstance(VirtualServerInstance):
    """
    Represents an Oracle Cloud instance managed by the Virtual Server agent.

    This class provides an interface for handling Oracle Cloud virtual server instances,
    allowing for retrieval and management of instance properties and metadata. It includes
    methods for initializing the instance with specific agent and identification details,
    as well as internal methods for accessing instance properties in both object and JSON formats.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access to server host name, server name, and instance username via properties

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize an OracleCloudInstance object for the specified Virtual Server instance.

        Args:
            agent: The agent object associated with this Oracle Cloud instance.
            instance_name: The name of the Oracle Cloud instance.
            instance_id: The unique identifier for the instance. If not provided, it will be determined automatically.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> instance = OracleCloudInstance(agent, 'MyOracleInstance', '101')
            >>> print(f"Instance created: {instance}")

        #ai-gen-doc
        """
        self._vendor_id = 13
        self._server_name = []
        self._server_host_name = None
        self._username = None
        super(OracleCloudInstance, self).__init__(agent, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the current Oracle Cloud instance.

        This method fetches the latest properties for the instance and updates the internal state.
        It raises an SDK Exception if the response is not empty or if the response indicates failure.

        Raises:
            SDK Exception: If the response is not empty or not successful.

        #ai-gen-doc
        """

        super(OracleCloudInstance, self)._get_instance_properties()
        if "vmwareVendor" in self._virtualserverinstance:
            self._server_host_name = [self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']]

            self._username = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['userName']

        for _each_client in self._asscociatedclients['memberServers']:
            client = _each_client['client']
            if 'clientName' in client.keys():
                self._server_name.append(str(client['clientName']))

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this Oracle Cloud instance.

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
                    "vmwareVendor": self._virtualserverinstance['vmwareVendor'],
                    "xenServer": {}
                    }
            }
        }
        return instance_json

    @property
    def server_host_name(self) -> list:
        """Get the Oracle Cloud server endpoint hostname.

        Returns:
            The hostname of the Oracle Cloud server as a list.

        Example:
            >>> instance = OracleCloudInstance()
            >>> endpoint = instance.server_host_name  # Use dot notation for property access
            >>> print(f"Oracle Cloud endpoint: {endpoint}")

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def server_name(self) -> list:
        """Get the server name associated with this Oracle Cloud instance.

        Returns:
            The server name as a list.

        Example:
            >>> instance = OracleCloudInstance()
            >>> name = instance.server_name  # Use dot notation for property access
            >>> print(f"Server name: {name}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def instance_username(self) -> str:
        """Get the username associated with the Oracle Cloud instance endpoint.

        Returns:
            The username of the Oracle Cloud endpoint as a string.

        Example:
            >>> instance = OracleCloudInstance()
            >>> username = instance.instance_username  # Use dot notation for property access
            >>> print(f"Instance username: {username}")

        #ai-gen-doc
        """
        return self._username
