# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Azure Local (Azure Stack HCI) Instance.

AzureLocal is the only class defined in this file.

AzureLocal: Derived class from VirtualServer Base class, representing an
            Azure Local (Azure Stack HCI) instance, and to perform operations on that instance

AzureLocal:

    __init__(agent_object, instance_name, instance_id)  --  initialize object of Azure Local Instance
                                                            object associated with the
                                                            VirtualServer Instance

    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Azure Local Specific
                                                            instance properties as well

    _get_instance_properties_json()                     --  get the all instance(Azure Local)
                                                            related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class AzureLocal(VirtualServerInstance):
    """
    Represents an Azure Local (Azure Stack HCI) instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to an Azure Local
    virtual server instance, providing mechanisms to retrieve and manage
    instance properties and metadata.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access to server name and server host name via properties

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize an AzureLocal instance object for the specified Virtual Server instance.

        Args:
            agent: An instance of the Agent class representing the associated agent.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> azure_local_instance = AzureLocal(agent, 'azure local', '79377')
            >>> # The AzureLocal object is now initialized and ready for use

        #ai-gen-doc
        """
        self._vendor_id = 25
        self._server_name = []
        self._server_host_name = []
        super(AzureLocal, self).__init__(agent, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Azure Local instance.

        This method fetches the current configuration and properties for the Azure Local instance
        and updates the internal state accordingly.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        #ai-gen-doc
        """
        super(AzureLocal, self)._get_instance_properties()
        
        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                                                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))

            if "vmwareVendor" in self._properties["virtualServerInstance"]:
                vendor_info = self._properties["virtualServerInstance"]['vmwareVendor']
                if 'virtualCenter' in vendor_info:
                    self._server_host_name.append(vendor_info['virtualCenter'].get('domainName', ''))

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all properties associated with this Azure Local instance.

        #ai-gen-doc
        """
        instance_json = {
            "instanceProperties": {
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "virtualServerInstance": {
                    "vsInstanceType": self._virtualserverinstance['vsInstanceType'],
                    "associatedClients": self._virtualserverinstance['associatedClients']
                }
            }
        }
        return instance_json

    @property
    def server_name(self) -> list:
        """Get the server name(s) associated with this Azure Local instance.

        Returns:
            The server name(s) as a list.

        Example:
            >>> instance = AzureLocal(agent, 'azure local')
            >>> names = instance.server_name
            >>> print(f"Azure Local server names: {names}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def server_host_name(self) -> list:
        """Get the server host name(s) from the Azure Local instance configuration.

        Returns:
            The server host name(s) as a list.

        Example:
            >>> instance = AzureLocal(agent, 'azure local')
            >>> host_names = instance.server_host_name
            >>> print(f"Azure Local server hosts: {host_names}")

        #ai-gen-doc
        """
        return self._server_host_name
