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

"""File for operating on a Virtual Server Hyper-V Instance.

HyperVInstance is the only class defined in this file.

HyperVInstance: Derived class from VirtualServer  Base class, representing a
                           Hyper-V instance, and to perform operations on that instance

HyperVInstance:

    __init__(agent_object,instance_name,instance_id)    --  initialize object of hyper-v Instance
                                                                object associated with the
                                                                        VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Hyper-V Specific
                                                                         instance properties as well

    _set_instance_properties()                          --  Hyper-V Instance class method  to
                                                        set Hyper-V Specific instance properties


"""


from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class HyperVInstance(VirtualServerInstance):
    """
    Represents a Hyper-V instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to a Hyper-V
    virtual server instance, providing mechanisms to initialize the instance,
    retrieve its properties, and access key server information.

    Key Features:
        - Initialization with agent, instance name, and instance ID
        - Retrieval of instance properties and their JSON representation
        - Access to server name and server host name via properties

    #ai-gen-doc
    """

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a HyperVInstance object for the specified Virtual Server instance.

        Args:
            agent: An instance of the Agent class representing the associated agent.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, a default may be used.

        Example:
            >>> agent = Agent(client_object, 'VirtualServer')
            >>> hyperv_instance = HyperVInstance(agent, 'HyperV_Instance1', '12345')
            >>> print(f"Instance created: {hyperv_instance}")

        #ai-gen-doc
        """
        super(HyperVInstance, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 2

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this HyperV instance.

        This method fetches the current properties for the HyperV instance and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response is not empty or the response indicates failure.

        #ai-gen-doc
        """

        super(HyperVInstance, self)._get_instance_properties()
        self._server_name = []

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
            "instanceProperties":{
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
    def server_name(self) -> list:
        """Get the domain name of the Hyper-V server from the instance configuration.

        Returns:
            The domain name of the Hyper-V server as a list.

        Example:
            >>> instance = HyperVInstance(agent_object, instance_name)
            >>> domain = instance.server_name
            >>> print(f"Hyper-V server domain: {domain}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def server_host_name(self) -> list:
        """Get the server host name associated with the HyperV instance.

        This property retrieves the domain name or host name from the vendor-specific configuration
        for the HyperV instance.

        Returns:
            The server host name as a list.

        Example:
            >>> instance = HyperVInstance()
            >>> host_name = instance.server_host_name
            >>> print(f"HyperV server host: {host_name}")

        #ai-gen-doc
        """
        return self._server_name
