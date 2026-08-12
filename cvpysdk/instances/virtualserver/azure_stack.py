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

"""File for operating on a Virtual Server Azure Stack Instance.

AzureStackInstance is the only class defined in this file.

AzureStackInstance:         Derived class from VirtualServer
                            Base class, representing a Azure Stack
                            instance, and to perform operations on that
                            instance

    __init__(self, agent,_name,iid)   	 -- initialize object of azure Stack
                                            Instance object associated with the
                                            VirtualServer Instance

    _get_instance_properties()           -- VirtualServer Instance class method
                                            overwritten to get azure Stack
                                            Specific instance properties as well

    _get_instance_properties_json()		 -- get the all instance related
                                            properties of this subclient.

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class AzureStackInstance(VirtualServerInstance):
    """
    Represents an Azure Stack instance for the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to an Azure Stack
    instance within the context of virtual server management. It provides mechanisms
    to initialize the instance, retrieve its properties, and access key Azure Stack
    identifiers such as server host name, subscription ID, and application ID.

    Key Features:
        - Initialization with agent, name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access to Azure Stack-specific properties:
            - server_host_name
            - subscriptionid
            - applicationid

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', name: str, iid: str) -> None:
        """Initialize the AzureStackInstance object for a given Virtual Server instance.

        Args:
            agent: The agent class instance associated with this Azure Stack instance.
            name: The name of the Azure Stack instance.
            iid: The unique identifier (ID) for the instance.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> instance = AzureStackInstance(agent, 'MyAzureStackInstance', '101')
            >>> print(instance)
            <AzureStackInstance: MyAzureStackInstance (ID: 101)>

        #ai-gen-doc
        """
        self._subscriptionid = None
        self._applicationid = None
        self._server_name = []
        self._vendor_id = 403
        super(AzureStackInstance, self).__init__(agent, name, iid)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this AzureStackInstance.

        This method fetches the latest properties for the current AzureStackInstance object
        from the backend service and updates the instance accordingly.

        Raises:
            SDKException: If the response is not empty or the response indicates failure.

        #ai-gen-doc
        """

        super(AzureStackInstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._subscriptionid = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']

            self._applicationid = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['userName']

        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"][
                "associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient.

        Returns:
            dict: A dictionary containing all properties associated with the current instance.

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
        """Get the server host name associated with the Azure Stack instance.

        Returns:
            The server host name as a string.

        Example:
            >>> instance = AzureStackInstance()
            >>> host_name = instance.server_host_name  # Use dot notation for property access
            >>> print(f"Server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def subscriptionid(self) -> str:
        """Get the subscription ID of the Azure Stack instance.

        Returns:
            The subscription ID associated with this Azure Stack instance as a string.

        Example:
            >>> instance = AzureStackInstance()
            >>> sub_id = instance.subscriptionid  # Use dot notation for property access
            >>> print(f"Subscription ID: {sub_id}")
        #ai-gen-doc
        """
        return self._subscriptionid

    @property
    def applicationid(self) -> str:
        """Get the application ID associated with this Azure Stack instance.

        Returns:
            The application ID (as a string) for the current Azure Stack instance.

        Example:
            >>> instance = AzureStackInstance()
            >>> app_id = instance.applicationid  # Access the application ID property
            >>> print(f"Application ID: {app_id}")

        #ai-gen-doc
        """
        return self._applicationid
