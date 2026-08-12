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

AmazonInstance is the only class defined in this file.

AmazonInstance: Derived class from VirtualServer  Base class, representing a
                           Amazon instance, and to perform operations on that instance

AmazonInstance:
    __init__(agent_object,instance_name,instance_id)    --  initialize object of amazon Instance
                                                            object associated with the
                                                            VirtualServer Instance

"""

from ...exception import SDKException
from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class AmazonInstance(VirtualServerInstance):
    """
    Represents an Amazon virtual server instance within a cloud management framework.

    This class extends the VirtualServerInstance to provide specialized handling
    for Amazon-based virtual server instances. It manages instance properties,
    initialization, and provides access to server-specific information such as
    server name and host name.

    Key Features:
        - Initialization of Amazon instance with agent, name, and instance ID
        - Retrieval of instance properties in both object and JSON formats
        - Access to server name and host name via properties
        - Initialization of tenant-specific instance properties

    #ai-gen-doc
    """
    def __init__(self, agent: 'Agent', name: str, iid: str) -> None:
        """Initialize an AmazonInstance object with the specified agent, name, and instance ID.

        Args:
            agent: The agent object associated with this Amazon instance.
            name: The name of the Amazon instance.
            iid: The unique instance ID for the Amazon instance.

        Example:
            >>> agent = Agent()  # Replace with actual agent object
            >>> instance = AmazonInstance(agent, "MyInstance", "i-1234567890abcdef0")
            >>> print(instance)

        #ai-gen-doc
        """
        self._vendor_id = 4
        self._server_name = []
        super(AmazonInstance, self).__init__(agent, name, iid)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this AmazonInstance object.

        This method fetches the latest properties for the current AmazonInstance from the backend
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response is not empty or if the response indicates a failure.

        #ai-gen-doc
        """

        super(AmazonInstance, self)._get_instance_properties()
        self._server_name = []
        self._initialize_tenant_instance_properties()
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
                    "vmwareVendor": self._virtualserverinstance['vmwareVendor']
                }
            }
        }

        return instance_json

    @property
    def server_name(self) -> list:
        """Get the domain name of the server from the AWS vendor JSON.

        Returns:
            The domain names of the server as a list.

        Example:
            >>> amazon_instance = AmazonInstance()
            >>> domain = amazon_instance.server_name  # Access the server name property
            >>> print(f"Server domain name: {domain}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def server_host_name(self) -> list:
        """Get the domain name (server host name) from the AWS vendor JSON.

        Returns:
            The domain name or server host name as a string.

        Example:
            >>> amazon_instance = AmazonInstance()
            >>> host_name = amazon_instance.server_host_name  # Use dot notation for property access

        #ai-gen-doc
        """
        return self._server_name

    def _initialize_tenant_instance_properties(self) -> None:
        """Initialize tenant-specific instance properties for the AmazonInstance client.

        This method sets up the necessary properties if the current client is identified as a tenant.

        #ai-gen-doc
        """
        if 'virtualServerInstance' in self._properties.keys():
            if 'enableAdminAccount' in self._properties['virtualServerInstance']['amazonInstanceInfo']:
                if self._properties['virtualServerInstance']['amazonInstanceInfo']['enableAdminAccount']:
                    admin_ins_id = self._properties['virtualServerInstance']['amazonInstanceInfo']['adminInstanceId']
                    _instance = self._services['INSTANCE'] % (admin_ins_id)
                    flag, response = self._cvpysdk_object.make_request('GET', _instance)
                    if flag:
                        if response.json() and "instanceProperties" in response.json():
                            self._admin_properties = response.json()["instanceProperties"][0]
                            if 'virtualServerInstance' in self._admin_properties:
                                self._asscociatedclients = None
                                self._properties['virtualServerInstance']['associatedClients'] =\
                                    self._admin_properties['virtualServerInstance']['associatedClients']
                                self._virtualserverinstance = self._properties["virtualServerInstance"]
                                self._vsinstancetype = self._virtualserverinstance['vsInstanceType']
                                self._asscociatedclients = self._virtualserverinstance['associatedClients']
                        else:
                            raise SDKException('Response', '102')
                    else:
                        raise SDKException('Response', '101', self._update_response_(response.text))
