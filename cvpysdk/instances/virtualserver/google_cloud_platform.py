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

"""File for operating on a Virtual Server Amazon Instance.

GoogleCloudInstance is the only class defined in this file.

GoogleCloudInstance: Derived class from VirtualServer  Base class, representing a
                    Google Cloud Platform instance, and to perform operations on that instance

GoogleCloudInstance:
    __init__(agent_object,instance_name,instance_id)    --  initialize object of Google Cloud
                                                            Platform Instance object associated
                                                            with the VirtualServer Instance

"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class GoogleCloudInstance(VirtualServerInstance):
    """
    Represents a Google Cloud virtual server instance within a virtual server management framework.

    This class provides mechanisms to initialize and manage Google Cloud instances, retrieve their
    properties, and access key server information such as server name and host name. It is designed
    to integrate with an agent and supports property-based access to important instance attributes.

    Key Features:
        - Initialization of Google Cloud instance objects with agent, name, and instance ID
        - Retrieval of instance properties in both standard and JSON formats
        - Property accessors for server name and server host name
        - Inherits from VirtualServerInstance for extended virtual server management capabilities

    #ai-gen-doc
    """
    def __init__(self, agent: 'Agent', name: str, iid: str) -> None:
        """Initialize a GoogleCloudInstance object with the specified agent, name, and instance ID.

        Args:
            agent: The agent object associated with this Google Cloud instance.
            name: The name of the Google Cloud instance.
            iid: The unique instance ID for the Google Cloud instance.

        Example:
            >>> agent = Agent()
            >>> instance = GoogleCloudInstance(agent, "my-instance", "instance-12345")

        #ai-gen-doc
        """
        self._vendor_id = 16
        self._server_name = []
        super(GoogleCloudInstance, self).__init__(agent, name, iid)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Google Cloud instance.

        This method fetches the latest properties for the instance from the backend service
        and updates the internal state accordingly. It ensures that the instance properties
        are current and accurate.

        Raises:
            SDKException: If the response is not empty or the response indicates failure.

        #ai-gen-doc
        """

        super(GoogleCloudInstance, self)._get_instance_properties()
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
            dict: A dictionary containing all properties associated with this Google Cloud instance subclient.

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
    def server_name(self) -> list:
        """Get the domain name associated with the Google Cloud instance from the vendor JSON.

        Returns:
            The domain name as a list.

        Example:
            >>> instance = GoogleCloudInstance()
            >>> domain = instance.server_name
            >>> print(f"Google Cloud domain: {domain}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def server_host_name(self) -> list:
        """Get the domain name (server host name) from the Google Cloud vendor JSON.

        Returns:
            The domain name (server host name) as a list.

        Example:
            >>> instance = GoogleCloudInstance()
            >>> host_name = instance.server_host_name  # Use dot notation for property access
            >>> print(f"Google Cloud server host name: {host_name}")

        #ai-gen-doc
        """
        return self._server_name