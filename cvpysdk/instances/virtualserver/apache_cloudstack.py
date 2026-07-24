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

"""Module for operating on a Virtual Server Apache CloudStack instance."""

from ..vsinstance import VirtualServerInstance

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from ...agent import Agent


class ApacheCloudStackInstance(VirtualServerInstance):
    """Represents an Apache CloudStack instance of the Virtual Server agent."""

    def __init__(self, agent: 'Agent', instance_name: str, instance_id: str = None) -> None:
        """Initialize an ApacheCloudStackInstance object."""
        super(ApacheCloudStackInstance, self).__init__(agent, instance_name, instance_id)

        member_servers = self._virtualserverinstance.get('associatedClients', {}).get('memberServers', [])
        primary_client = member_servers[0].get('client', {}) if member_servers else {}

        client_name = primary_client.get('clientName')
        host_name = primary_client.get('hostName')

        # Keep vendor aligned with instance type when explicit cloudstack vendor JSON is unavailable.
        self._vendor_id = self._virtualserverinstance.get('vsInstanceType', 1800)
        self._server_name = [client_name] if isinstance(client_name, str) and client_name else []
        self._server_host_name = [host_name] if isinstance(host_name, str) and host_name else []

        if "vmwareVendor" in self._virtualserverinstance:
            self._client_host_name = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Apache CloudStack instance."""
        super(ApacheCloudStackInstance, self)._get_instance_properties()

    def _get_instance_properties_json(self) -> dict:
        """Construct the JSON representation of this instance properties."""
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
    def server_host_name(self) -> List[str]:
        """Get the host name(s) of the associated Apache CloudStack server."""
        return self._server_host_name

    @server_host_name.setter
    def server_host_name(self, value: list) -> None:
        """Set the host name(s) of the associated Apache CloudStack server."""
        self._server_host_name = value

    @property
    def server_name(self) -> List[str]:
        """Get the name(s) of the associated Apache CloudStack server."""
        return self._server_name

    @property
    def client_host_name(self) -> str:
        """Get the cloudstack console associated with this instance.

        Returns:
            The name of the cloudstack console as a string.

        """
        return self._client_host_name
