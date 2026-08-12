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

"""File for operating on a Virtual Server Azure Resource Manager Instance.

AzureResoureceManagerInstance is the only class defined in this file.

AzureResoureceManagerInstance: Derived class from VirtualServer
                            Base class, representing a Azure Resource Manager
                            instance, and to perform operations on that
                            instance

    __init__(self, agent,_name,iid)   	 -- 	initialize object of azure RM
                                            Instance object associated with the
                                            VirtualServer Instance

    _get_instance_properties()     --  VirtualServer Instance class method
                                        overwritten to get azure RM
                                        Specific instance properties as well

    _get_instance_properties_json()			--  get the all instance related
                                                        properties of this subclient.

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...agent import Agent


class AzureRMInstance(VirtualServerInstance):
    """
    Represents an Azure Resource Manager (ARM) instance associated with a VirtualServerInstance.

    This class provides functionality to manage and interact with Azure Resource Manager instances,
    including retrieving instance and application properties, updating Azure credentials, and accessing
    server-related information. It is designed to be initialized with agent information, instance name,
    and instance ID, and extends the capabilities of the VirtualServerInstance base class.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access to application-specific properties
        - Update and management of Azure credentials, including support for managed identities
        - Properties to access server name and server host name

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', name: str, iid: str) -> None:
        """Initialize an AzureRMInstance object for the specified Virtual Server instance.

        Args:
            agent: Instance of the Agent class representing the associated agent.
            name: The name of the virtual server instance.
            iid: The unique identifier (ID) of the virtual server instance.

        Example:
            >>> agent = Agent(client_object, "VirtualServer")
            >>> instance = AzureRMInstance(agent, "MyAzureInstance", '101')
            >>> print(f"Instance created: {instance}")

        #ai-gen-doc
        """

        super(VirtualServerInstance, self).__init__(agent, name, iid)
        self._vendor_id = 7
        self._subscription_id = None

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this AzureRMInstance.

        This method fetches the latest properties for the current AzureRMInstance object
        from the backend service and updates the instance accordingly.

        Raises:
            SDKException: If the response is not empty or the response indicates failure.

        #ai-gen-doc
        """

        super(AzureRMInstance, self)._get_instance_properties()
        self._server_name = []
        if 'virtualServerInstance' in self._properties:
            if self._properties["virtualServerInstance"]["associatedClients"].get("memberServers"):
                _member_servers = self._properties["virtualServerInstance"] \
                    ["associatedClients"]["memberServers"]
            else:
                _member_servers = []
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

    def _get_application_properties(self) -> None:
        """Retrieve the properties of the current AzureRMInstance.

        This method fetches and returns the application properties associated with this instance.
        If the response is empty or unsuccessful, an SDK Exception is raised.

        Returns:
            dict: A dictionary containing the application properties for this instance.

        Raises:
            SDKException: If the response is empty or the request is not successful.

        #ai-gen-doc
        """
        super(AzureRMInstance, self)._get_application_properties()
        if 'azureResourceManager' in self._application_properties:
            self._subscription_id = self._application_properties['azureResourceManager']['subscriptionId']

    def _update_azure_credentials(self, credential_id: int, credential_name: str = None,
                                  usemanaged_identity: bool = False) -> None:
        """Update the Azure credentials for the hypervisor instance.

        This method updates the credentials used by the Azure hypervisor, allowing you to specify a new credential ID,
        an optional credential name, and whether to use a managed identity.

        Args:
            credential_id: The ID of the credential to update in the hypervisor.
            credential_name: Optional name of the credential to update in the hypervisor.
            usemanaged_identity: If True, configures the hypervisor to use a managed identity instead of explicit credentials.

        #ai-gen-doc
        """

        self._get_application_properties()

        self._credential_json = {
            "hypervisorType": self._vendor_id,
            "skipCredentialValidation": False,
            "credentials": {
                "id": credential_id,
                "name": credential_name
            },
            "subscriptionId": self._subscription_id,
            "useManagedIdentity": usemanaged_identity
        }

        super(AzureRMInstance, self)._update_hypervisor_credentials(self._credential_json)

    @property
    def server_name(self) -> list:
        """Get the server (domain) name from the Hyper-V JSON configuration.

        Returns:
            The domain name as a string extracted from the Hyper-V JSON.

        Example:
            >>> instance = AzureRMInstance()
            >>> domain = instance.server_name
            >>> print(f"Server domain name: {domain}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def server_host_name(self) -> list:
        """Get the domain name (server host name) from the VMware vendor JSON.

        Returns:
            The server host name as a string.

        Example:
            >>> instance = AzureRMInstance()
            >>> host_name = instance.server_host_name
            >>> print(f"Server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_name
