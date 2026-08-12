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

"""Main file for performing network related operations on a client/client group

Network:

    __init__(class_object)            --    initialize object of the Network class

    _get_network_properties()         --    returns all the existing network properties on a
                                            client/client group

    configure_network_settings        --    get the value  for configureFirewallSettings

    configure_network_settings(val)   --    set the value  for configureFirewallSettings

    trivial_config                    --    get the value for isTrivialConfig

    trivial_config(val)               --    set the value for isTrivialConfig

    roaming_client                    --    get the value for isRoamingClient

    roaming_client(val)               --    set the value for isRoamingClient

    tunnel_connection_port            --    get the tunnel connection port on the
                                            client/client group

    tunnel_connection_port(val)       --    set the tunnel connection port on the
                                            client/client group

    force_ssl                         --    get the value for foreceSSL

    force_ssl(val)                    --    set the value for foreceSSL

    tunnel_init_seconds               --    get the value for tunnelInitSeconds

    tunnel_init_seconds(val)          --    set the value for tunnelInitSeconds

    lockdown                          --    get the value for lockdown

    lockdown(val)                     --    set the value for lockdown

    bind_open_ports                   --    get the value for bindOpenPortsOnly

    bind_open_ports(val)              --    set the value for bindOpenPortsOnly

    proxy                             --    get the value for isDMZ

    proxy(val)                        --    set the value for isDMZ

    keep_alive_seconds                --    get the value for keepAliveSeconds

    keep_alive_seconds(val)           --    set the value for keepAliveSeconds

    incoming_connections              --    get the list of incoming connections on the
                                            client/client group

    set_incoming_connections()        --    sets the incoming connections on the client/client
                                            group with the list of values provided

    additional_ports                  --    get the list of additional ports on the
                                            client/client group

    set_additional_ports()            --    sets the range of additional ports on the client/client
                                            group provided as list and tunnel port

    outgoing_routes                   --    get the list of outgoing routes on the
                                            client/client group

    set_outgoing_routes()             --    sets the outgoing routes on the client/client group
                                            with the list of values provided

    tppm_settings                     --    get the list of tppm settings on the client

    set_tppm_settings(tppm_settings)  --    set the tppm on the client with the list of
                                            values provided

    _advanced_network_config()        --    set advanced network configuration on the
                                            client/client group


"""

from __future__ import absolute_import
from __future__ import unicode_literals

from typing import Any, Dict

from .exception import SDKException

class Network(object):
    """
    Class for performing network related operations on a client or client group.

    This class provides a comprehensive interface for managing and configuring
    network settings for individual clients or groups of clients. It exposes
    various properties and methods to control network behavior, security, and
    connectivity options.

    Key Features:
        - Retrieve network properties and advanced configuration details
        - Configure network settings such as SSL enforcement, lockdown mode, and proxy usage
        - Manage tunnel connection parameters including port and initialization timing
        - Set trivial and roaming client configurations
        - Bind open ports and manage additional ports for network communication
        - Control incoming connections and outgoing routes
        - Adjust keep-alive intervals for network sessions
        - Apply TPPM (Third-Party Policy Management) settings
        - Flexible property-based interface for dynamic network configuration

    #ai-gen-doc
    """

    def __init__(self, class_object: object) -> None:
        """Initialize a Network class object with a client or client group instance.

        Args:
            class_object: An instance of the client or client group class to associate with the Network object.

        Example:
            >>> client = Client('client_name')
            >>> network = Network(client)
            >>> # The Network object is now initialized with the specified client

        #ai-gen-doc
        """
        from .client import Client
        from .clientgroup import ClientGroup

        self._class_object = class_object
        self._commcell_object = self._class_object._commcell_object
        self.flag = ""
        if isinstance(class_object, Client):
            self._client_object = class_object
            self.flag = "CLIENT"

        elif isinstance(class_object, ClientGroup):
            self._clientgroup_object = class_object
            self.flag = "CLIENTGROUP"

        self._config_network_settings = None
        self._is_trivial_config = False
        self._proxy_entities = []
        self._port_range = []
        self._network_outgoing_routes = []
        self._restriction_to = []
        self._tppm_settings = []
        self._is_roaming_client = False
        self._tunnel_connection_port = 8403
        self._force_ssl = False
        self._tunnel_init_seconds = 30
        self._lockdown = False
        self._bind_open_ports_only = False
        self._is_dmz = False
        self._keep_alive_seconds = 300
        self.enable_network_settings = None

        self._incoming_connection_type = {
            0: 'RESTRICTED',
            1: 'BLOCKED'
        }

        self._firewall_outgoing_route_type = {
            0: 'DIRECT',
            1: 'VIA_GATEWAY',
            2: 'VIA_PROXY'
        }

        self._firewall_outgoing_connection_protocol = {
            0: 'HTTP',
            1: 'HTTPS',
            2: 'HTTPS_AuthOnly',
            3: 'RAW_PROTOCOL'
        }

        self._tppm_type = {
            2: 'WEB_SERVER_FOR_IIS_SERVER',
            3: 'COMMSERVE',
            5: 'REPORTS',
            6: 'CUSTOM_REPORT_ENGINE'
        }

        self._get_network_properties()

    def _get_network_properties(self) -> Dict[str, Any]:
        """Retrieve all existing network properties for a client or client group.

        This method gathers and returns the network properties associated with the current client or client group,
        allowing you to inspect or process network configuration details.

        Returns:
            A dictionary containing the network properties, where keys are property names and values are their corresponding settings.

        Example:
            >>> network = Network()
            >>> properties = network._get_network_properties()
            >>> print(properties)
            {'ip_address': '192.168.1.10', 'subnet': '255.255.255.0', ...}

        #ai-gen-doc
        """
        if self.flag == "CLIENT":
            network_prop = self._client_object._properties['clientProps']

        elif self.flag == "CLIENTGROUP":
            network_prop = self._clientgroup_object._properties

        if 'firewallConfiguration' in network_prop:
            self._config_network_settings = (network_prop['firewallConfiguration'][
                'configureFirewallSettings'])

            self._is_trivial_config = network_prop['firewallConfiguration']['isTrivialConfig']

            if 'portRange' in network_prop['firewallConfiguration']:
                self._port_range = network_prop['firewallConfiguration']['portRange']

            if 'proxyEntities' in network_prop['firewallConfiguration']:
                self._proxy_entities = network_prop['firewallConfiguration']['proxyEntities']

            if 'firewallOutGoingRoutes' in network_prop['firewallConfiguration']:
                self._network_outgoing_routes = (network_prop['firewallConfiguration'][
                    'firewallOutGoingRoutes'])

            if 'restrictionTo' in network_prop['firewallConfiguration']:
                self._restriction_to = network_prop['firewallConfiguration']['restrictionTo']

            if 'firewallOptions' in network_prop['firewallConfiguration']:
                self._network_options = network_prop['firewallConfiguration']['firewallOptions']

            if 'isRoamingClient' in network_prop['firewallConfiguration']:
                self._is_roaming_client = (network_prop['firewallConfiguration'][
                    'firewallOptions']['isRoamingClient'])

            self._tunnel_connection_port = network_prop['firewallConfiguration']['firewallOptions'][
                'tunnelconnectionPort']

            self._force_ssl = network_prop['firewallConfiguration']['firewallOptions']['foreceSSL']

            self._tunnel_init_seconds = (network_prop['firewallConfiguration'][
                'firewallOptions']['tunnelInitSeconds'])

            self._lockdown = network_prop['firewallConfiguration']['firewallOptions']['lockdown']

            self._bind_open_ports_only = (network_prop['firewallConfiguration'][
                'firewallOptions']['bindOpenPortsOnly'])

            self._is_dmz = network_prop['firewallConfiguration']['firewallOptions']['isDMZ']

            self._keep_alive_seconds = (network_prop['firewallConfiguration'][
                'firewallOptions']['keepAliveSeconds'])

            if 'tppm' in self._network_options:
                self._tppm_settings = (network_prop['firewallConfiguration'][
                    'firewallOptions']['tppm'])

    @property
    def configure_network_settings(self) -> bool:
        """Get the current value indicating whether firewall settings are configured.

        Returns:
            bool: True if firewall settings are configured, False otherwise.

        Example:
            >>> network = Network()
            >>> is_configured = network.configure_network_settings
            >>> print(f"Firewall settings configured: {is_configured}")

        #ai-gen-doc
        """
        return self._config_network_settings

    @configure_network_settings.setter
    def configure_network_settings(self, val: bool) -> None:
        """Set the value for configuring firewall settings on the network.

        Args:
            val: Boolean value indicating whether to enable (True) or disable (False) firewall settings.

        Example:
            >>> network = Network()
            >>> network.configure_network_settings = True  # Enable firewall settings
            >>> network.configure_network_settings = False  # Disable firewall settings

        #ai-gen-doc
        """
        self._config_network_settings = val
        self._advanced_network_config()

    @property
    def trivial_config(self) -> bool:
        """Get the value indicating whether the network configuration is trivial.

        Returns:
            bool: True if the network configuration is considered trivial, False otherwise.

        Example:
            >>> network = Network()
            >>> is_trivial = network.trivial_config  # Use dot notation for property access
            >>> print(f"Is network configuration trivial? {is_trivial}")

        #ai-gen-doc
        """
        return self._is_trivial_config

    @trivial_config.setter
    def trivial_config(self, val: bool) -> None:
        """Set the value for the isTrivialConfig property.

        Args:
            val: Boolean value to set for isTrivialConfig.

        Example:
            >>> network = Network()
            >>> network.trivial_config = True  # Enable trivial configuration
            >>> network.trivial_config = False  # Disable trivial configuration

        #ai-gen-doc
        """
        self._is_trivial_config = val
        self.enable_network_settings = True

    @property
    def roaming_client(self) -> bool:
        """Get the roaming client status for the network.

        Returns:
            bool: True if the network is configured as a roaming client, False otherwise.

        Example:
            >>> network = Network()
            >>> is_roaming = network.roaming_client
            >>> print(f"Roaming client enabled: {is_roaming}")

        #ai-gen-doc
        """
        return self._is_roaming_client

    @roaming_client.setter
    def roaming_client(self, val: bool) -> None:
        """Set the roaming client status for the network.

        Args:
            val: A boolean value indicating whether the client should be set as a roaming client (True) or not (False).

        Example:
            >>> network = Network()
            >>> network.roaming_client = True  # Enable roaming client
            >>> network.roaming_client = False  # Disable roaming client

        #ai-gen-doc
        """
        self._is_roaming_client = val
        self.configure_network_settings = True

    @property
    def tunnel_connection_port(self) -> int:
        """Get the tunnel connection port value for the client or client group.

        Returns:
            The tunnel connection port as an integer.

        Example:
            >>> network = Network()
            >>> port = network.tunnel_connection_port
            >>> print(f"Tunnel connection port: {port}")

        #ai-gen-doc
        """
        return self._tunnel_connection_port

    @tunnel_connection_port.setter
    def tunnel_connection_port(self, val: int) -> None:
        """Set the value for the tunnel connection port.

        Args:
            val: The port number to be used for the tunnel connection.

        Example:
            >>> network = Network()
            >>> network.tunnel_connection_port = 8080  # Set the tunnel connection port to 8080

        #ai-gen-doc
        """
        self._tunnel_connection_port = val
        self.configure_network_settings = True

    @property
    def force_ssl(self) -> bool:
        """Get the current value of the forceSSL setting for the network.

        Returns:
            bool: True if SSL is enforced for network communication, False otherwise.

        Example:
            >>> network = Network()
            >>> is_ssl_forced = network.force_ssl
            >>> print(f"SSL enforced: {is_ssl_forced}")

        #ai-gen-doc
        """
        return self._force_ssl

    @force_ssl.setter
    def force_ssl(self, val: bool) -> None:
        """Set the forceSSL property for the network.

        Args:
            val: Boolean value indicating whether to force SSL (True) or not (False).

        Example:
            >>> network = Network()
            >>> network.force_ssl = True  # Enable SSL enforcement
            >>> network.force_ssl = False  # Disable SSL enforcement

        #ai-gen-doc
        """
        self._force_ssl = val
        self.configure_network_settings = True

    @property
    def tunnel_init_seconds(self) -> int:
        """Get the number of seconds used for tunnel initialization.

        Returns:
            The tunnel initialization time in seconds as an integer.

        Example:
            >>> network = Network()
            >>> init_time = network.tunnel_init_seconds
            >>> print(f"Tunnel initialization time: {init_time} seconds")

        #ai-gen-doc
        """
        return self._tunnel_init_seconds

    @tunnel_init_seconds.setter
    def tunnel_init_seconds(self, val: int) -> None:
        """Set the tunnel initialization timeout in seconds.

        Args:
            val: The number of seconds to set for tunnel initialization.

        Example:
            >>> network = Network()
            >>> network.tunnel_init_seconds = 30  # Set tunnel initialization to 30 seconds

        #ai-gen-doc
        """
        self._tunnel_init_seconds = val
        self.configure_network_settings = True

    @property
    def lockdown(self) -> bool:
        """Get the current lockdown status of the network.

        Returns:
            True if the network is in lockdown mode, False otherwise.

        Example:
            >>> network = Network()
            >>> is_locked_down = network.lockdown  # Use dot notation for property access
            >>> print(f"Network lockdown status: {is_locked_down}")
            >>> # Output: Network lockdown status: True or False

        #ai-gen-doc
        """
        return self._lockdown

    @lockdown.setter
    def lockdown(self, val: bool) -> None:
        """Set the network lockdown state.

        Args:
            val: A boolean value indicating whether to enable (True) or disable (False) network lockdown.

        Example:
            >>> network = Network()
            >>> network.lockdown = True  # Enable network lockdown
            >>> network.lockdown = False  # Disable network lockdown

        #ai-gen-doc
        """
        self._lockdown = val
        self.configure_network_settings = True

    @property
    def bind_open_ports(self) -> bool:
        """Get the value indicating whether only open ports are bound.

        Returns:
            bool: True if only open ports are bound; False otherwise.

        Example:
            >>> network = Network()
            >>> is_bind_open = network.bind_open_ports
            >>> print(f"Bind only open ports: {is_bind_open}")

        #ai-gen-doc
        """
        return self._bind_open_ports_only

    @bind_open_ports.setter
    def bind_open_ports(self, val: bool) -> None:
        """Set the 'bindopenportsonly' property to control whether only open ports are bound.

        Args:
            val: A boolean value indicating whether to bind only open ports (True) or not (False).

        Example:
            >>> network = Network()
            >>> network.bind_open_ports = True  # Enable binding only to open ports
            >>> network.bind_open_ports = False  # Disable the restriction

        #ai-gen-doc
        """
        self._bind_open_ports_only = val
        self.configure_network_settings = True

    @property
    def proxy(self) -> bool:
        """Get the value indicating whether the network is configured as a DMZ proxy.

        Returns:
            bool: True if the network is a DMZ proxy, False otherwise.

        Example:
            >>> network = Network()
            >>> is_dmz = network.proxy  # Use dot notation for property access
            >>> print(f"Is DMZ proxy: {is_dmz}")

        #ai-gen-doc
        """
        return self._is_dmz

    @proxy.setter
    def proxy(self, val: bool) -> None:
        """Set the value for the isDMZ property using the provided parameter.

        Args:
            val: Boolean value to set the isDMZ property. Set to True if the network is a DMZ proxy, otherwise False.

        Example:
            >>> network = Network()
            >>> network.proxy = True  # Sets the network as a DMZ proxy
            >>> network.proxy = False  # Unsets the DMZ proxy status

        #ai-gen-doc
        """
        self._is_dmz = val
        self.configure_network_settings = True

    @property
    def keep_alive_seconds(self) -> int:
        """Get the configured keep-alive interval in seconds for the network.

        Returns:
            The keep-alive interval in seconds as an integer.

        Example:
            >>> network = Network()
            >>> interval = network.keep_alive_seconds
            >>> print(f"Keep-alive interval: {interval} seconds")

        #ai-gen-doc
        """
        return self._keep_alive_seconds

    @keep_alive_seconds.setter
    def keep_alive_seconds(self, val: int) -> None:
        """Set the keep-alive interval in seconds for the network connection.

        Args:
            val: The number of seconds to use for the keep-alive interval.

        Example:
            >>> network = Network()
            >>> network.keep_alive_seconds = 120  # Set keep-alive to 120 seconds

        #ai-gen-doc
        """
        self._keep_alive_seconds = val
        self.configure_network_settings = True

    @property
    def incoming_connections(self) -> list:
        """Retrieve all incoming network connections on the client.

        Returns:
            list: A list containing information about each incoming connection.

        Example:
            >>> network = Network()
            >>> connections = network.incoming_connections
            >>> print(f"Number of incoming connections: {len(connections)}")
            >>> # Each item in 'connections' represents an incoming connection

        #ai-gen-doc
        """

        for incoming_connection in self._restriction_to:
            if incoming_connection['state'] in self._incoming_connection_type.keys():
                incoming_connection['state'] = (self._incoming_connection_type[
                    incoming_connection['state']])

        return self._restriction_to

    def set_incoming_connections(self, incoming_connections: list[dict]) -> None:
        """Set the incoming connections for a client or client group.

        This method configures the allowed incoming connection states for specified entities,
        such as clients or client groups, using a list of dictionaries. Each dictionary should
        specify the connection state, the entity name, and whether the entity is a client.

        Args:
            incoming_connections: A list of dictionaries, each containing:
                - 'state' (str): The connection state, e.g., 'RESTRICTED' or 'BLOCKED'.
                - 'entity' (str): The name of the client or client group.
                - 'isClient' (bool): True if the entity is a client, False if it is a client group.

        Raises:
            SDKException: If a required key is missing in any of the input dictionaries.

        Example:
            >>> network = Network()
            >>> incoming = [
            ...     {'state': 'RESTRICTED', 'entity': 'centOS', 'isClient': True},
            ...     {'state': 'BLOCKED', 'entity': 'Edge Clients', 'isClient': False}
            ... ]
            >>> network.set_incoming_connections(incoming)
            >>> print("Incoming connections updated successfully.")

        #ai-gen-doc
        """
        try:

            for incoming_connection in incoming_connections:

                if incoming_connection['isClient']:
                    restriction_to_dict = {
                        "state": incoming_connection['state'],
                        "entity": {
                            "clientName": incoming_connection['entity']
                        }
                    }

                else:
                    restriction_to_dict = {
                        "state": incoming_connection['state'],
                        "entity": {
                            "clientGroupName": incoming_connection['entity']
                        }
                    }

                self._restriction_to.append(restriction_to_dict)
            self.configure_network_settings = True

        except KeyError as err:
            raise SDKException('Client', '102', '{} not given in content'.format(err))

    @property
    def additional_ports(self) -> list:
        """Get the list of additional network ports configured for this Network.

        Returns:
            list: A list of additional port numbers.

        Example:
            >>> network = Network()
            >>> ports = network.additional_ports
            >>> print(f"Additional ports: {ports}")

        #ai-gen-doc
        """
        return self._port_range

    def set_additional_ports(self, ports: list[dict], tunnel_port: int = 8403) -> None:
        """Set additional incoming ports and the tunnel port for the network.

        This method configures additional incoming port ranges and sets the tunnel port
        to the specified value. The `ports` parameter should be a list of dictionaries,
        each containing 'startPort' and 'endPort' keys to define port ranges.

        Args:
            ports: A list of dictionaries specifying port ranges. Each dictionary must have
                'startPort' and 'endPort' integer keys.
                Example:
                    [
                        {'startPort': 1024, 'endPort': 1030},
                        {'startPort': 2000, 'endPort': 4000}
                    ]
            tunnel_port: The tunnel port to set (default is 8403).

        Raises:
            SDKException: If any required key is missing in the input dictionaries.

        Example:
            >>> network = Network()
            >>> port_ranges = [
            ...     {'startPort': 1024, 'endPort': 1030},
            ...     {'startPort': 2000, 'endPort': 4000}
            ... ]
            >>> network.set_additional_ports(port_ranges, tunnel_port=8500)
            >>> # The network is now configured with the specified port ranges and tunnel port

        #ai-gen-doc
        """
        try:
            self._tunnel_connection_port = tunnel_port
            for port in ports:
                additional_port_dict = {
                    "startPort": port['startPort'],
                    "endPort": port['endPort']
                }

                self._port_range.append(additional_port_dict)

            self.configure_network_settings = True

        except KeyError as err:
            raise SDKException('Client', '102', '{} not given in content'.format(err))

    @property
    def outgoing_routes(self) -> list:
        """Retrieve the list of all outgoing network routes.

        Returns:
            list: A list containing all outgoing routes configured for the network.

        Example:
            >>> network = Network()
            >>> routes = network.outgoing_routes
            >>> print(f"Outgoing routes: {routes}")

        #ai-gen-doc
        """

        for outgoing_route in self._network_outgoing_routes:
            if (outgoing_route['fireWallOutGoingRouteOptions']['connectionProtocol']
                    in self._firewall_outgoing_connection_protocol.keys()):
                (outgoing_route['fireWallOutGoingRouteOptions'][
                    'connectionProtocol']) = (self._firewall_outgoing_connection_protocol[
                    outgoing_route['fireWallOutGoingRouteOptions']['connectionProtocol']])
            if (outgoing_route['fireWallOutGoingRouteOptions']['routeType']
                    in self._firewall_outgoing_route_type.keys()):
                outgoing_route['fireWallOutGoingRouteOptions']['routeType'] = (self._firewall_outgoing_route_type[
                    outgoing_route['fireWallOutGoingRouteOptions']['routeType']])

        return self._network_outgoing_routes

    def set_outgoing_routes(self, outgoing_routes: list[dict]) -> None:
        """Set outgoing routes on the client using the provided list of route definitions.

        Each outgoing route should be specified as a dictionary with required keys depending on the route type.
        Supported route types are 'DIRECT', 'VIA_GATEWAY', and 'VIA_PROXY'. The structure of each dictionary
        varies based on the route type, as described below.

        Args:
            outgoing_routes: A list of dictionaries, each representing an outgoing route configuration.
                - For routeType 'DIRECT':
                    {
                        'routeType': 'DIRECT',
                        'remoteEntity': <str>,
                        'streams': <int>,
                        'isClient': <bool>,
                        'forceAllDataTraffic': <bool>,
                        'connectionProtocol': <int>  # 0: HTTP, 1: HTTPS, 2: HTTPS_AuthOnly, 3: RAW_PROTOCOL
                    }
                - For routeType 'VIA_GATEWAY':
                    {
                        'routeType': 'VIA_GATEWAY',
                        'remoteEntity': <str>,
                        'streams': <int>,
                        'gatewayPort': <int>,
                        'gatewayHost': <str>,
                        'isClient': <bool>,
                        'forceAllDataTraffic': <bool>,
                        'connectionProtocol': <int>
                    }
                - For routeType 'VIA_PROXY':
                    {
                        'routeType': 'VIA_PROXY',
                        'remoteEntity': <str>,
                        'remoteProxy': <str>,
                        'isClient': <bool>
                    }

        Raises:
            SDKException: If an invalid routeType is provided or if required keys are missing in any route dictionary.

        Example:
            >>> routes = [
            ...     {
            ...         'routeType': 'DIRECT',
            ...         'remoteEntity': 'Testcs',
            ...         'streams': 1,
            ...         'isClient': True,
            ...         'forceAllDataTraffic': True,
            ...         'connectionProtocol': 0
            ...     },
            ...     {
            ...         'routeType': 'VIA_GATEWAY',
            ...         'remoteEntity': 'centOS',
            ...         'streams': 2,
            ...         'gatewayPort': 443,
            ...         'gatewayHost': '1.2.3.4',
            ...         'isClient': True,
            ...         'forceAllDataTraffic': False,
            ...         'connectionProtocol': 1
            ...     },
            ...     {
            ...         'routeType': 'VIA_PROXY',
            ...         'remoteEntity': 'Laptop Clients',
            ...         'remoteProxy': 'TemplateRHEL65_4',
            ...         'isClient': False
            ...     }
            ... ]
            >>> network = Network()
            >>> network.set_outgoing_routes(routes)
            >>> print("Outgoing routes set successfully.")

        #ai-gen-doc
        """

        try:

            for outgoing_route in outgoing_routes:
                if outgoing_route['isClient']:
                    remote_entity_dict = {
                        "clientName": outgoing_route['remoteEntity']

                    }

                else:
                    remote_entity_dict = {

                        "clientGroupName": outgoing_route['remoteEntity']
                    }

                if outgoing_route['routeType'] == self._firewall_outgoing_route_type[0]:
                    gatewayport = 0
                    gatewayhostname = ""
                    remote_proxy = {}
                    nstreams = outgoing_route['streams']
                    force_all_data_traffic = outgoing_route['forceAllDataTraffic']
                    connection_protocol = outgoing_route.get('connectionProtocol', 2)

                elif outgoing_route['routeType'] == self._firewall_outgoing_route_type[1]:
                    gatewayport = outgoing_route['gatewayPort']
                    gatewayhostname = outgoing_route['gatewayHost']
                    remote_proxy = {}
                    nstreams = outgoing_route['streams']
                    force_all_data_traffic = outgoing_route['forceAllDataTraffic']
                    connection_protocol = outgoing_route.get('connectionProtocol', 2)

                elif outgoing_route['routeType'] == self._firewall_outgoing_route_type[2]:
                    gatewayport = 0
                    gatewayhostname = ""
                    nstreams = 1
                    force_all_data_traffic = False
                    connection_protocol = 2
                    remote_proxy = {
                        "clientName": outgoing_route['remoteProxy'],

                        "clientGroupName": "",
                        "_type_": 3
                    }

                else:
                    raise SDKException('Client', '101')

                outgoing_routes_dict = {
                    "fireWallOutGoingRouteOptions": {
                        "numberOfStreams": nstreams,
                        "connectionProtocol": connection_protocol,
                        "gatewayTunnelPort": gatewayport,
                        "forceAllBackupRestoreDataTraffic": force_all_data_traffic,
                        "gatewayHostname": gatewayhostname,
                        "routeType": outgoing_route['routeType'],
                        "remoteProxy": remote_proxy
                    },
                    "remoteEntity": remote_entity_dict
                }

                self._network_outgoing_routes.append(outgoing_routes_dict)
            self.configure_network_settings = True

        except KeyError as err:
            raise SDKException('Client', '102', '{} not given in content'.format(err))

    @property
    def tppm_settings(self) -> list:
        """Retrieve the list of TPPM (Third Party Patch Management) settings configured on the client.

        Returns:
            list: A list containing the TPPM settings for the client.

        Example:
            >>> network = Network()
            >>> settings = network.tppm_settings
            >>> print(f"TPPM settings: {settings}")

        #ai-gen-doc
        """

        for tppm_setting in self._tppm_settings:
            if tppm_setting['tppmType'] in self._tppm_type.keys():
                tppm_setting['tppmType'] = self._tppm_type[tppm_setting['tppmType']]

        return self._tppm_settings

    def set_tppm_settings(self, tppm_settings: list[dict]) -> None:
        """Set TPPM (Third Party Proxy Management) settings on the client.

        This method configures TPPM settings for the client using the provided list of settings.
        Each setting should be a dictionary containing the TPPM type, port number, and proxy entity.

        Note:
            This operation is supported only at the client level.

        Args:
            tppm_settings: A list of dictionaries, each specifying a TPPM configuration.
                Each dictionary must contain the following keys:
                    - 'tppmType': The type of TPPM. Valid values are:
                        1. 'WEB_SERVER_FOR_IIS_SERVER'
                        2. 'COMMSERVE'
                        3. 'REPORTS'
                        4. 'CUSTOM_REPORT_ENGINE'
                    - 'portNumber': The port number to use (int).
                    - 'proxyEntity': The proxy entity name (str).

                Example:
                    [
                        {
                            'tppmType': 'WEB_SERVER_FOR_IIS_SERVER',
                            'portNumber': 9999,
                            'proxyEntity': 'shezavm3'
                        },
                        {
                            'tppmType': 'REPORTS',
                            'portNumber': 8888,
                            'proxyEntity': 'shezavm11'
                        }
                    ]

        Raises:
            SDKException: If an invalid 'tppmType' is provided or if any required key is missing in a setting.

        Example:
            >>> tppm_settings = [
            ...     {'tppmType': 'COMMSERVE', 'portNumber': 8080, 'proxyEntity': 'proxy1'},
            ...     {'tppmType': 'REPORTS', 'portNumber': 9090, 'proxyEntity': 'proxy2'}
            ... ]
            >>> network = Network()
            >>> network.set_tppm_settings(tppm_settings)
            >>> print("TPPM settings applied successfully.")

        #ai-gen-doc
        """

        try:

            if self.flag == "CLIENT":
                for tppm_setting in tppm_settings:

                    if tppm_setting['tppmType'] in self._tppm_type.values():
                        tppm_dict = {
                            "enable": True,
                            "tppmType": tppm_setting['tppmType'],
                            "proxyInformation": {
                                "portNumber": tppm_setting['portNumber'],
                                "proxyEntity": {
                                    "clientName": tppm_setting['proxyEntity'],
                                    "_type_": 3
                                }
                            }
                        }
                        self._tppm_settings.append(tppm_dict)

                    else:
                        raise SDKException('Client', '101')

            self.configure_network_settings = True

        except KeyError as err:
            raise SDKException('Client', '102', '{} not given in content'.format(err))

    def _advanced_network_config(self) -> None:
        """Configure advanced network properties for the client or client group.

        This method sets all relevant network properties on the associated client or client group.
        It is typically used to apply advanced network configurations as required.

        Raises:
            SDKException: If the request was not successful, if invalid input was provided,
                or if an empty response was received.

        Example:
            >>> network = Network()
            >>> network._advanced_network_config()
            >>> print("Advanced network configuration applied successfully.")

        #ai-gen-doc
        """

        if self.flag == "CLIENT":
            if not self._config_network_settings:
                update_networkconfig_dict = {
                    "firewallConfiguration":
                        {
                            "configureFirewallSettings": self._config_network_settings
                        }
                }

            else:
                update_networkconfig_dict = {
                    "firewallConfiguration":
                        {
                            "configureFirewallSettings": self._config_network_settings,
                            "isTrivialConfig": False,
                            "portRange": self._port_range,
                            "proxyEntities": self._proxy_entities,
                            "firewallOutGoingRoutes": self._network_outgoing_routes,
                            "restrictionTo": self._restriction_to,
                            "firewallOptions": {
                                "isRoamingClient": self._is_roaming_client,
                                "extendedProperties": "<App_FirewallExtendedProperties "
                                                      "configureAutomatically=\"0\" "
                                                      "defaultOutgoingProtocol=\"0\"/>",
                                "tunnelconnectionPort": self._tunnel_connection_port,
                                "foreceSSL": self._force_ssl,
                                "tunnelInitSeconds": self._tunnel_init_seconds,
                                "lockdown": self._lockdown,
                                "bindOpenPortsOnly": self._bind_open_ports_only,
                                "isDMZ": self._is_dmz,
                                "keepAliveSeconds": self._keep_alive_seconds,
                                "tppm": self._tppm_settings
                            }
                        }
                }

            request_json = self._client_object._update_client_props_json(update_networkconfig_dict)
            flag, response = (self._commcell_object._cvpysdk_object.make_request(
                'POST', self._client_object._CLIENT, request_json))

            if flag:
                if response.json() and 'response' in response.json():
                    error_code = response.json()['response'][0]['errorCode']

                    if error_code == 0:
                        self._client_object._get_client_properties()

                    elif 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']
                        self._get_network_properties()
                        raise SDKException('Client', '102', error_message)

                else:
                    self._get_network_properties()
                    raise SDKException('Response', '102')

            else:
                response_string = self._commcell_object._update_response_(response.text)
                self._get_network_properties()
                raise SDKException('Response', '101', response_string)

        elif self.flag == "CLIENTGROUP":

            if not self._config_network_settings:
                request_json = {
                    "clientGroupOperationType": 2,
                    "clientGroupDetail": {
                        "clientGroup": {
                            "clientGroupName": self._clientgroup_object._clientgroup_name
                        },
                        "firewallConfiguration": {
                            "configureFirewallSettings": self._config_network_settings,

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
                        "firewallConfiguration": {
                            "configureFirewallSettings": self._config_network_settings,
                            "isTrivialConfig": False,
                            "portRange": self._port_range,
                            "proxyEntities": self._proxy_entities,
                            "firewallOutGoingRoutes": self._network_outgoing_routes,
                            "restrictionTo": self._restriction_to,
                            "firewallOptions": {
                                "isRoamingClient": self._is_roaming_client,
                                "extendedProperties": "<App_FirewallExtendedProperties "
                                                      "configureAutomatically=\"0\" "
                                                      "defaultOutgoingProtocol=\"0\"/>",
                                "tunnelconnectionPort": self._tunnel_connection_port,
                                "foreceSSL": self._force_ssl,
                                "tunnelInitSeconds": self._tunnel_init_seconds,
                                "lockdown": self._lockdown,
                                "bindOpenPortsOnly": self._bind_open_ports_only,
                                "isDMZ": self._is_dmz,
                                "keepAliveSeconds": self._keep_alive_seconds,
                            }
                        }

                    }}

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._clientgroup_object._CLIENTGROUP, request_json)

            if flag:
                if response.json():
                    error_code = str(response.json()['errorCode'])

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']
                    else:
                        error_message = ""

                    if error_code == '0':
                        self._clientgroup_object._get_clientgroup_properties()

                    else:
                        self._get_network_properties()
                        raise SDKException('ClientGroup', '102',
                                           'Client group properties were not updated')

                else:
                    self._get_network_properties()
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                self._get_network_properties()
                raise SDKException('Response', '101', response_string)
