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

"""Main file for performing network throttle related operations on a client/client group

NetworkThrottle:

    __init__(class_object)             --    initialize object of the NetworkThrottle class

    _get_throttle_properties()         --    returns all the existing network throttle properties
                                             on a client/client group

    enable_network_throttle()          --    enables network throttling option on the
                                             client/client group

    share_bandwidth()                  --    enables share bandwidth option on the
                                             client/client group

    remote_clients()                   --    adds the remote clients for throttling on a
                                             client/client group

    remote_client_groups()             --    adds the remote client group for throttling on a
                                             client/client group

    throttle_schedules()               --    adds the throttling schedules with different options
                                             provided

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from typing import Any, Dict, List

from .exception import SDKException

class NetworkThrottle(object):
    """
    Class for managing and configuring network throttling operations for clients and client groups.

    This class provides an interface to control network bandwidth usage by enabling or disabling
    network throttling, sharing bandwidth among clients, and managing remote clients and client groups.
    It also supports the configuration of throttle schedules and rules to optimize network performance.

    Key Features:
        - Initialization with a class object for context
        - Retrieval of throttle properties
        - Enable or disable network throttling via property
        - Share bandwidth among clients or groups
        - Manage remote clients and remote client groups
        - Configure and manage throttle schedules and rules
        - Internal configuration of network throttle settings

    #ai-gen-doc
    """

    def __init__(self, class_object: object) -> None:
        """Initialize a NetworkThrottle instance for managing network throttling settings.

        Args:
            class_object: An instance of the client or client group class to which network throttling will be applied.

        Example:
            >>> client = Client('client_name')
            >>> throttle = NetworkThrottle(client)
            >>> print("NetworkThrottle object initialized for client.")

        #ai-gen-doc
        """
        from .client import Client
        from .clientgroup import ClientGroup

        self._class_object = class_object
        self._commcell_object = self._class_object._commcell_object
        self.flag = ""
        self.is_client = None
        self.is_client_group = None

        if isinstance(class_object, Client):
            self._client_object = class_object
            self.is_client = True

        elif isinstance(class_object, ClientGroup):
            self._clientgroup_object = class_object
            self.is_client_group = True

        self._enable_network_throttling = None
        self._share_bandwidth = None
        self._throttle_schedules = []
        self._remote_client_groups = []
        self._remote_clients = []
        self._get_throttle_properties()

    def _get_throttle_properties(self) -> Dict[str, Any]:
        """Retrieve and store all existing network throttle properties for a client or client group.

        This method fetches the current network throttle settings associated with the client or client group
        and retains each property for further use or inspection.

        Returns:
            A dictionary containing the network throttle properties and their values.

        Example:
            >>> throttle = NetworkThrottle()
            >>> properties = throttle._get_throttle_properties()
            >>> print(properties)
            {'max_bandwidth': 100, 'throttle_type': 'client', ...}

        #ai-gen-doc
        """
        if self.is_client:
            throttle_prop = self._client_object._properties['clientProps']

        elif self.is_client_group:
            throttle_prop = self._clientgroup_object._properties

        if 'networkThrottle' in throttle_prop:
            self._enable_network_throttling = (throttle_prop['networkThrottle']['enableThrottle'])

            self._share_bandwidth = (throttle_prop.get(
                'networkThrottle').get('throttle', {}).get('shareBandwidth', True))

            self._throttle_schedules = (throttle_prop.get(
                'networkThrottle').get('throttle', {}).get('throttle', []))

            self._remote_client_groups = (throttle_prop.get('networkThrottle').get(
                'clientGroupList', []))

            self._remote_clients = (throttle_prop.get('networkThrottle').get('clientList', []))

    @property
    def enable_network_throttle(self) -> bool:
        """Get the current status of network throttling.

        Returns:
            bool: True if network throttling is enabled, False otherwise.

        Example:
            >>> throttle = NetworkThrottle()
            >>> is_enabled = throttle.enable_network_throttle
            >>> print(f"Network throttling enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._enable_network_throttling

    @enable_network_throttle.setter
    def enable_network_throttle(self, val: bool) -> None:
        """Set the value to enable or disable network throttling.

        Args:
            val: Boolean value indicating whether to enable (True) or disable (False) network throttling.

        Example:
            >>> throttle = NetworkThrottle()
            >>> throttle.enable_network_throttle = True  # Enable network throttling
            >>> throttle.enable_network_throttle = False  # Disable network throttling

        #ai-gen-doc
        """

        self._enable_network_throttling = val
        self._config_network_throttle()

    @property
    def share_bandwidth(self) -> int:
        """Get the configured value for shared network bandwidth.

        Returns:
            The amount of bandwidth (in Mbps) allocated for sharing across network operations.

        Example:
            >>> throttle = NetworkThrottle()
            >>> bandwidth = throttle.share_bandwidth
            >>> print(f"Shared bandwidth: {bandwidth} Mbps")

        #ai-gen-doc
        """
        return self._share_bandwidth

    @share_bandwidth.setter
    def share_bandwidth(self, val: bool) -> None:
        """Set the value for the share bandwidth property.

        Args:
            val: Boolean value indicating whether to enable (True) or disable (False) bandwidth sharing.

        Example:
            >>> throttle = NetworkThrottle()
            >>> throttle.share_bandwidth = True  # Enable bandwidth sharing
            >>> throttle.share_bandwidth = False  # Disable bandwidth sharing

        #ai-gen-doc
        """

        self._share_bandwidth = val
        self.enable_network_throttle = True

    @property
    def remote_clients(self) -> List[str]:
        """Get the list of remote clients for which network throttling is configured.

        Returns:
            List of client names (as strings) that have network throttling settings applied.

        Example:
            >>> throttle = NetworkThrottle()
            >>> clients = throttle.remote_clients
            >>> print(f"Throttling is configured for: {clients}")

        #ai-gen-doc
        """
        clients = []

        for client in self._remote_clients:
            clients.append(client['clientName'])
        return clients

    @remote_clients.setter
    def remote_clients(self, clients: list) -> None:
        """Set the list of remote clients for which network throttling will be configured.

        Args:
            clients: A list of client names (as strings) to apply throttling settings to.

        Example:
            >>> throttle = NetworkThrottle()
            >>> throttle.remote_clients = ['client1', 'client2', 'client3']
            >>> # The specified clients will now have throttling configured

        #ai-gen-doc
        """

        for client in clients:
            client_dict = {
                "clientName": client
            }
            self._remote_clients.append(client_dict)

        self.enable_network_throttle = True

    @property
    def remote_client_groups(self) -> List[str]:
        """Get the list of client groups associated with network throttling.

        Returns:
            List of client group names (as strings) for which throttling is configured.

        Example:
            >>> throttle = NetworkThrottle()
            >>> groups = throttle.remote_client_groups
            >>> print(f"Throttled client groups: {groups}")

        #ai-gen-doc
        """
        client_groups = []

        for client_group in self._remote_client_groups:
            client_groups.append(client_group['clientGroupName'])
        return client_groups

    @remote_client_groups.setter
    def remote_client_groups(self, client_groups: list) -> None:
        """Set the remote client groups for which network throttling will be configured.

        Args:
            client_groups: A list of client group names or identifiers to apply throttling settings to.

        Example:
            >>> throttle = NetworkThrottle()
            >>> throttle.remote_client_groups = ['GroupA', 'GroupB']
            >>> # Throttling will now be configured for the specified remote client groups

        #ai-gen-doc
        """

        for client_group in client_groups:
            client_group_dict = {
                "clientGroupName": client_group
            }
            self._remote_client_groups.append(client_group_dict)

        self.enable_network_throttle = True

    @property
    def throttle_schedules(self) -> list:
        """Retrieve the throttle rules configured for a client or client group.

        Returns:
            list: A list of throttle rule configurations currently set on the client or client group.

        Example:
            >>> network_throttle = NetworkThrottle()
            >>> schedules = network_throttle.throttle_schedules
            >>> print(f"Number of throttle schedules: {len(schedules)}")
            >>> for rule in schedules:
            ...     print(rule)

        #ai-gen-doc
        """
        return self._throttle_schedules

    @throttle_schedules.setter
    def throttle_schedules(self, throttle_rules: list[dict]) -> None:
        """Set throttle schedules for a client or client group.

        This setter allows you to define multiple network throttle rules, specifying bandwidth limits and schedules
        for sending and receiving data. Each rule is represented as a dictionary with supported keys such as
        "sendRate", "recvRate", "days", and others.

        Args:
            throttle_rules: A list of dictionaries, each representing a throttle rule. Supported keys in each
                dictionary include:
                    - "sendRate": (int) Maximum send rate in KBps.
                    - "sendEnabled": (bool) Whether sending is enabled.
                    - "receiveEnabled": (bool) Whether receiving is enabled.
                    - "recvRate": (int) Maximum receive rate in KBps.
                    - "days": (str) 7-character string representing days of the week (e.g., '1010101').
                    - "isAbsolute": (bool) Whether the rate is absolute.
                    - "startTime": (int) Start time in seconds from midnight.
                    - "endTime": (int) End time in seconds from midnight.
                    - "sendRatePercent": (int) Send rate as a percentage.
                    - "recvRatePercent": (int) Receive rate as a percentage.

        Example:
            >>> throttle_rules = [
            ...     {
            ...         "sendRate": 1024,
            ...         "sendEnabled": True,
            ...         "receiveEnabled": True,
            ...         "recvRate": 1024,
            ...         "days": '1010101',
            ...         "isAbsolute": True,
            ...         "startTime": 0,
            ...         "endTime": 0,
            ...         "sendRatePercent": 40,
            ...         "recvRatePercent": 40
            ...     },
            ...     {
            ...         "sendRate": 1024,
            ...         "sendEnabled": True,
            ...         "receiveEnabled": True,
            ...         "recvRate": 1024,
            ...         "days": '1111111',
            ...         "isAbsolute": False
            ...     }
            ... ]
            >>> network_throttle = NetworkThrottle()
            >>> network_throttle.throttle_schedules = throttle_rules  # Use assignment for property setter

        #ai-gen-doc
        """

        for throttle_rule in throttle_rules:
            days = int(throttle_rule.get('days', '1111111'), 2)
            throttle_rule_dict = {
                "sendRate": throttle_rule.get('sendRate', 1024),
                "sendEnabled": throttle_rule.get('sendEnabled', False),
                "receiveEnabled": throttle_rule.get('receiveEnabled', False),
                "recvRate": throttle_rule.get('recvRate', 1024),
                "days": days,
                "isAbsolute": throttle_rule.get('isAbsolute', True),
                "startTime": 0,
                "endTime": 0,
                "sendRatePercent": throttle_rule.get('sendRatePercent', 40),
                "recvRatePercent": throttle_rule.get('recvRatePercent', 40)
            }

            self._throttle_schedules.append(throttle_rule_dict)

        self.enable_network_throttle = True

    def _config_network_throttle(self) -> None:
        """Configure network throttle properties on the client or client group.

        This method applies the network throttle settings to the associated client or client group.
        It should be used to enforce bandwidth limitations or other network-related restrictions.

        Raises:
            SDKException: If the request was not successful, if invalid input was provided,
                or if an empty response was received.

        Example:
            >>> throttle = NetworkThrottle()
            >>> throttle._config_network_throttle()
            >>> print("Network throttle configuration applied successfully.")

        #ai-gen-doc
        """

        update_props_call = None
        request_url = None

        if self.is_client:
            update_props_call = self._client_object.refresh
            request_url = self._client_object._CLIENT
            if not self._enable_network_throttling:
                update_networkconfig_dict = {
                    "networkThrottle":
                        {
                            "enableThrottle": self._enable_network_throttling
                        }
                }

            else:
                update_networkconfig_dict = {
                    "networkThrottle": {
                        "enableThrottle": self._enable_network_throttling,
                        "throttle": {
                            "shareBandwidth": self._share_bandwidth,
                            "throttle": self._throttle_schedules
                        },
                        "clientGroupList":
                            self._remote_client_groups,

                        "clientList": self._remote_clients
                    }
                }

            request_json = self._client_object._update_client_props_json(update_networkconfig_dict)

        elif self.is_client_group:
            update_props_call = self._clientgroup_object.refresh
            request_url = self._clientgroup_object._CLIENTGROUP

            if not self._enable_network_throttling:
                request_json = {
                    "clientGroupOperationType": 2,
                    "clientGroupDetail": {
                        "clientGroup": {
                            "clientGroupName": self._clientgroup_object._clientgroup_name
                        },
                        "networkThrottle": {
                            "enableThrottle": self._enable_network_throttling,

                        }
                    }
                }

            else:
                request_json = {
                    "clientGroupOperationType": 2,
                    "clientGroupDetail": {
                        "clientGroup": {
                            "clientGroupName": self._clientgroup_object._clientgroup_name
                            },
                        "networkThrottle": {
                            "enableThrottle": self._enable_network_throttling,
                            "throttle": {
                                "shareBandwidth": self._share_bandwidth,
                                "throttle": self._throttle_schedules
                            },
                            "clientGroupList": self._remote_client_groups,

                            "clientList": self._remote_clients
                        }

                    }}

        flag, response = (self._commcell_object._cvpysdk_object.make_request(
            'POST', request_url, request_json))

        if flag:
            if response.json() and 'response' in response.json():
                self.error_code = response.json()['response'][0]['errorCode']

            elif response.json():
                self.error_code = str(response.json()['errorCode'])

                if self.error_code == 0 or self.error_code == '0':
                    update_props_call()

                elif 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']
                    update_props_call()
                    raise SDKException('Client', '102', error_message)

                elif self.error_code != '0' and self.is_client_group:
                    update_props_call()
                    raise SDKException('ClientGroup', '102',
                                       'Client group properties were not updated')

            else:
                update_props_call()
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            update_props_call()
            raise SDKException('Response', '101', response_string)
