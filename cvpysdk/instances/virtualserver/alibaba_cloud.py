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

"""File for operating on a Virtual Server Alibaba Cloud Instance.

AlibabaCloudInstance is the only class defined in this file.

AlibabaCloudInstance: Derived class from VirtualServer  Base class, representing a
                           Alibaba Cloud instance, and to perform operations on that instance

AlibabaCloudInstance:

    __init__(agent_object,instance_name,instance_id)    --  initialize object of Alibaba Cloud
                                                            Instance object associated with the
                                                            VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Alibaba Cloud
                                                            Specific instance properties as well

    _set_instance_properties()                          --  Alibaba Cloud Instance class method
                                                            to set Alibaba Cloud
                                                            Specific instance properties


"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class AlibabaCloudInstance(VirtualServerInstance):
    """
    Represents an Alibaba Cloud instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to an Alibaba Cloud
    virtual server instance. It provides mechanisms to initialize the instance with
    relevant identifiers, retrieve instance properties in both object and JSON formats,
    and access key attributes such as server host name, server name, and instance username.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties as objects and JSON
        - Access to server host name, server name, and instance username via properties

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize an AlibabaCloudInstance object for a specific Virtual Server instance.

        Args:
            agent: The agent object associated with this instance.
            instance_name: The name of the Alibaba Cloud virtual server instance.
            instance_id: The unique identifier for the instance. If not provided, it can be set later.

        Example:
            >>> agent = Agent(client_object, "Virtual Server")
            >>> instance = AlibabaCloudInstance(agent, "MyECSInstance", '12345')
            >>> print(f"Instance name: {instance.instance_name}")
            >>> # The instance is now initialized and ready for further operations

        #ai-gen-doc
        """
        self._vendor_id = 18
        self._server_name = []
        self._server_host_name = None
        self._username = None
        super(AlibabaCloudInstance, self).__init__(agent, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Alibaba Cloud instance.

        This method fetches the latest properties for the current instance from the Alibaba Cloud service
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response is not empty or if the response indicates a failure.

        Example:
            >>> instance = AlibabaCloudInstance()
            >>> instance._get_instance_properties()
            >>> # The instance properties are now updated with the latest values

        #ai-gen-doc
        """

        super(AlibabaCloudInstance, self)._get_instance_properties()
        if "vmwareVendor" in self._virtualserverinstance:
            self._server_host_name = [self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']]

            self._username = (
                self._virtualserverinstance
                .get('vmwareVendor', {})
                .get('virtualCenter', {})
                .get('userName', None)
            )

        for _each_client in self._asscociatedclients['memberServers']:
            client = _each_client['client']
            if 'clientName' in client.keys():
                self._server_name.append(str(client['clientName']))

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all properties associated with this Alibaba Cloud instance subclient.

        #ai-gen-doc
        """
        instance_json = {
            "instanceProperties":{
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
        """Get the hostname of the Alibaba Cloud server endpoint.

        Returns:
            The hostname of the Alibaba Cloud server as a list.

        Example:
            >>> instance = AlibabaCloudInstance()
            >>> endpoint = instance.server_host_name  # Use dot notation for property access

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def server_name(self) -> list:
        """Get the name of the server associated with this AlibabaCloudInstance.

        Returns:
            The list of server names

        Example:
            >>> instance = AlibabaCloudInstance()
            >>> name = instance.server_name  # Use dot notation for property access

        #ai-gen-doc
        """
        return self._server_name

    @property
    def instance_username(self) -> str:
        """Get the username associated with the Alibaba Cloud instance.

        Returns:
            The username of the Alibaba Cloud endpoint as a string.

        Example:
            >>> instance = AlibabaCloudInstance()
            >>> username = instance.instance_username
            >>> print(f"Instance username: {username}")

        #ai-gen-doc
        """
        return self._username
