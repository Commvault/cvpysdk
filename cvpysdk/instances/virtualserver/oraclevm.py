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

"""File for operating on a Virtual Server OracleVM Instance.

OracleVMInstance is the only class defined in this file.

OracleVMInstance:     Derived class from VirtualServer  Base class, representing a
                        OracleVM instance, and to perform operations on that instance


OracleVMInstance:

    __init__()                    --  initialize object of oraclevm Instance object
                                        associated with the VirtualServer Instance

    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get oraclevm specific instance properties

    _get_instance_properties_json()     --  get the all instance(oraclevm)
                                                related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class OracleVMInstance(VirtualServerInstance):
    """
    Represents an Oracle VM instance managed by the Virtual Server agent.

    This class provides an interface for handling Oracle VM instances within the
    Virtual Server environment. It allows for initialization with agent details,
    retrieval of instance properties, and access to key server information.

    Key Features:
        - Initialize Oracle VM instance with agent object, name, and ID
        - Retrieve instance properties and their JSON representation
        - Access server host name and server name via properties

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize an OracleVMInstance object for the specified Virtual Server instance.

        Args:
            agent_object: Instance of the Agent class associated with this Oracle VM instance.
            instance_name: The name of the Oracle VM instance.
            instance_id: Optional; the unique identifier for the Oracle VM instance. If not provided, it will be determined automatically.

        Example:
            >>> agent = Agent(client_object, 'Virtual Server')
            >>> ovm_instance = OracleVMInstance(agent, 'MyOracleVM', '101')
            >>> # The OracleVMInstance object is now initialized and ready for use

        #ai-gen-doc
        """
        self._vendor_id = 10
        self._vmwarvendor = None
        self._server_name = []
        self._server_host_name = []
        super(OracleVMInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this OracleVMInstance.

        This method fetches the latest properties for the OracleVMInstance from the backend
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response from the backend is empty or indicates a failure.

        #ai-gen-doc
        """
        super(OracleVMInstance, self)._get_instance_properties()
        if "vmwareVendor" in self._virtualserverinstance:
            self._vmwarvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']

            self._server_name.append(self._instance['clientName'])

            self._server_host_name.append(self._vmwarvendor["domainName"])

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this OracleVM subclient.

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
        """Get the domain name (server host name) from the OracleVM vendor JSON.

        Returns:
            The domain name or server host name as a list.

        Example:
            >>> instance = OracleVMInstance()
            >>> domain_name = instance.server_host_name
            >>> print(f"OracleVM domain name: {domain_name}")

        #ai-gen-doc
        """
        return self._server_host_name

    @property
    def server_name(self) -> list:
        """Get the name of the Oracle client associated with the PseudoClient.

        Returns:
            The name of the Oracle client as a list.

        Example:
            >>> instance = OracleVMInstance()
            >>> client_name = instance.server_name
            >>> print(f"Oracle client name: {client_name}")

        #ai-gen-doc
        """
        return self._server_name
