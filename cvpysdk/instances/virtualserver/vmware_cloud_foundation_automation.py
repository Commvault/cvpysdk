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

"""File for operating on a Virtual Server VMware Cloud Foundation Automation Instance.

VMwareCloudFoundationAutomationInstance is the only class defined in this file.

VMwareCloudFoundationAutomationInstance:     Derived class from VirtualServerBase,
                                           representing a VCF instance, and to perform
                                           operations on that instance.

VMwareCloudFoundationAutomationInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of VCF Instance object
                                                associated with the VirtualServer Instance

    _get_instance_properties()          --  VirtualServer Instance class method overwritten
                                                to get VCF specific instance properties

    _get_instance_properties_json()     --  get all instance (VCF) related properties
                                                as JSON
"""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...agent import Agent


class VMwareCloudFoundationAutomationInstance(VirtualServerInstance):
    """
    Represents a VMware Cloud Foundation Automation instance managed by the Virtual Server agent.

    This class encapsulates the properties and behaviors specific to a VCF virtual server
    instance, providing mechanisms to retrieve and manage instance properties and metadata.

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize a VMwareCloudFoundationAutomationInstance object.

        Args:
            agent_object: An instance of the Agent class representing the associated agent.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance.

        #ai-gen-doc
        """
        self._vendor_id = 105
        self._vmwarvendor = None
        self._server_name = []
        self._server_host_name = []
        super(VMwareCloudFoundationAutomationInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this VCF instance.

        #ai-gen-doc
        """
        super(VMwareCloudFoundationAutomationInstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._vmwarvendor = self._virtualserverinstance['vmwareVendor']['virtualCenter']
            self._server_name.append(self._instance['clientName'])
            self._server_host_name.append(self._vmwarvendor["domainName"])

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this VCF instance as a dictionary.

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
        """Get the server host name list from the VCF vendor JSON."""
        return self._server_host_name

    @property
    def _user_name(self) -> str:
        return self._vmwarvendor.get('userName') or self._credential.get('userName', '')

    @property
    def server_name(self) -> list:
        """Get the server name list from the VCF vendor JSON."""
        return self._server_name
