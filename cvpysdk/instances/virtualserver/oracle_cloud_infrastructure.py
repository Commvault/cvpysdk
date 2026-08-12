# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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


class OracleCloudInfrastructureInstance(VirtualServerInstance):
    """
    Represents an Oracle Cloud Infrastructure (OCI) instance managed by the Virtual Server agent.

    This class provides an interface for handling VMWare instances within the Oracle Cloud Infrastructure
    environment. It enables retrieval and management of instance properties, including server host name,
    username, and server name, and supports access to instance configuration details in both object and
    JSON formats.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Retrieval of instance properties and configuration details
        - Access to instance properties in JSON format
        - Properties for server host name, username, and server name

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize an OracleCloudInfrastructureInstance object for a Virtual Server instance.

        Args:
            agent_object: Instance of the Agent class associated with this Oracle Cloud Infrastructure instance.
            instance_name: The name of the Virtual Server instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, it can be set later.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> oci_instance = OracleCloudInfrastructureInstance(agent, 'MyOCIInstance', '12345')
            >>> print(f"Instance name: {oci_instance.instance_name}")

        #ai-gen-doc
        """
        self._vendor_id = 1
        self._vmwarvendor = None
        self._server_name = []
        self._server_host_name = []
        super(OracleCloudInfrastructureInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Oracle Cloud Infrastructure instance.

        This method fetches the latest properties for the instance and updates the internal state.
        It should be called to ensure the instance properties are current.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        #ai-gen-doc
        """
        super(OracleCloudInfrastructureInstance, self)._get_instance_properties()
        print (self._properties)
        if "vmwareVendor" in self._virtualserverinstance:
            self._vmwarvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']
            self._instance_guid = self._instance['instanceGUID']
            self._instance_id = self._instance['instanceId']
            self._server_name.append(self._instance['clientName'])

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all properties associated with this Oracle Cloud Infrastructure instance subclient.

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
            The server host name as a list.

        Example:
            >>> instance = OracleCloudInfrastructureInstance()
            >>> host_name = instance.server_host_name
            >>> print(f"Server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def _user_name(self) -> str:
        """Get the username from the VMware vendor JSON configuration.

        Returns:
            The username as a string extracted from the VMware vendor JSON.

        Example:
            >>> instance = OracleCloudInfrastructureInstance()
            >>> username = instance._user_name
            >>> print(f"Username: {username}")

        #ai-gen-doc
        """
        return self._vmwarvendor["userName"]

    @property
    def server_name(self) -> list:
        """Get the domain name associated with the Oracle Cloud Infrastructure instance.

        This property retrieves the server (domain) name as specified in the VMware vendor JSON configuration.

        Returns:
            The domain name as a list.

        Example:
            >>> oci_instance = OracleCloudInfrastructureInstance()
            >>> domain = oci_instance.server_name  # Access the server name property
            >>> print(f"Domain name: {domain}")

        #ai-gen-doc
        """
        return self._server_name