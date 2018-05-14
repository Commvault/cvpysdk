# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing network related operations on a client/client group

Network:

    __init__(class_object)            --    initialize object of the Network class

    _get_network_properties()         --    returns all the existing network properties on a client/client group

    configure_network_settings        --    get the value  for configureFirewallSettings

    configure_network_settings(val)   --    set the value  for configureFirewallSettings

    trivial_config                    --    get the value for isTrivialConfig

    trivial_config(val)               --    set the value for isTrivialConfig

    roaming_client                    --    get the value for isRoamingClient

    roaming_client(val)               --    set the value for isRoamingClient

    tunnel_connection_port            --    get the tunnel connection port on the client/client group

    tunnel_connection_port(val)       --    set the tunnel connection port on the client/client group

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

    incoming_connections              --    get the list of incoming connections on the client/client group

    set_incoming_connections(incoming_connections) --  sets the incoming connections on the client/client group with the list of values provided

    additional_ports                  --    get the list of additional ports on the client/client group

    set_additional_ports(ports,tunnelPort)   --  sets the range of additional ports on the client/client group provided as list and tunnel port

    outgoing_routes                   --    get the list of outgoing routes on the client/client group

    set_outgoing_routes(outgoing_routes) -- sets the outgoing routes on the client/client group with the list of values provided

    tppm_settings                     --    get the list of tppm settings on the client

    set_tppm_settings(tppm_settings)  --    set the tppm on the client with the list of values provided

    _advanced_network_config()       --    set advanced network configuration on the client/client group


"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .exception import SDKException


class Network(object):
    """Class for performing network related operations on a client or client group"""

    def __init__(self, class_object):
        """Initialize the Network class object

            Args:
                class_object (object)  --  instance of the client/client group class



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

    def _get_network_properties(self):
        """Get all the existing network properties on a client/client group and retain each of them


        """
        if self.flag == "CLIENT":
            network_prop = self._client_object._properties['clientProps']

        elif self.flag == "CLIENTGROUP":
            network_prop = self._clientgroup_object._properties

        if 'firewallConfiguration' in network_prop:
            self._config_network_settings = network_prop['firewallConfiguration']['configureFirewallSettings']

            self._is_trivial_config = network_prop['firewallConfiguration']['isTrivialConfig']

            if 'portRange' in network_prop['firewallConfiguration']:
                self._port_range = network_prop['firewallConfiguration']['portRange']

            if 'proxyEntities' in network_prop['firewallConfiguration']:
                self._proxy_entities = network_prop['firewallConfiguration']['proxyEntities']

            if 'firewallOutGoingRoutes' in network_prop['firewallConfiguration']:
                self._network_outgoing_routes = network_prop['firewallConfiguration']['firewallOutGoingRoutes']

            if 'restrictionTo' in network_prop['firewallConfiguration']:
                self._restriction_to = network_prop['firewallConfiguration']['restrictionTo']

            if 'firewallOptions' in network_prop['firewallConfiguration']:
                self._network_options = network_prop['firewallConfiguration']['firewallOptions']

            if 'isRoamingClient' in network_prop['firewallConfiguration']:
                self._is_roaming_client = network_prop['firewallConfiguration']['firewallOptions']['isRoamingClient']

            self._tunnel_connection_port = network_prop['firewallConfiguration']['firewallOptions'][
                'tunnelconnectionPort']

            self._force_ssl = network_prop['firewallConfiguration']['firewallOptions']['foreceSSL']

            self._tunnel_init_seconds = network_prop['firewallConfiguration']['firewallOptions']['tunnelInitSeconds']

            self._lockdown = network_prop['firewallConfiguration']['firewallOptions']['lockdown']

            self._bind_open_ports_only = network_prop['firewallConfiguration']['firewallOptions']['bindOpenPortsOnly']

            self._is_dmz = network_prop['firewallConfiguration']['firewallOptions']['isDMZ']

            self._keep_alive_seconds = network_prop['firewallConfiguration']['firewallOptions']['keepAliveSeconds']

            if 'tppm' in self._network_options:
                self._tppm_settings = network_prop['firewallConfiguration']['firewallOptions']['tppm']

    @property
    def configure_network_settings(self):
        """Gets the value for configure firewall settings

        :return:
            boolean - configureFirewallSettings
        """
        return self._config_network_settings

    @configure_network_settings.setter
    def configure_network_settings(self, val):
        """Sets the value for configureFirewallSettings with the parameter provided


        """
        self._config_network_settings = val
        self._advanced_network_config()

    @property
    def trivial_config(self):
        """Gets the value for isTrivialConfig

        :return:
            boolean - isTrivialConfig
        """
        return self._is_trivial_config

    @trivial_config.setter
    def trivial_config(self, val):
        """Sets the value for isTrivialConfig with the parameter provided


        """
        self._is_trivial_config = val
        self.enable_network_settings = True

    @property
    def roaming_client(self):
        """Gets the value for isRoamingClient

        :return:
            boolen - isRoamingClient
        """
        return self._is_roaming_client

    @roaming_client.setter
    def roaming_client(self, val):
        """Sets the value for isRoamingClient with the parameter provided

        """
        self._is_roaming_client = val
        self.configure_network_settings = True

    @property
    def tunnel_connection_port(self):
        """Gets the value for tunnel port on the client/client group

        :return:
            int - tunnelConnectionPort
        """
        return self._tunnel_connection_port

    @tunnel_connection_port.setter
    def tunnel_connection_port(self, val):
        """Sets the value for tunnelConnectionPort with the parameter provided

        """
        self._tunnel_connection_port = val
        self.configure_network_settings = True

    @property
    def force_ssl(self):
        """Gets the value for forceSSL

        :return:
            boolean - forceSSL
        """
        return self._force_ssl

    @force_ssl.setter
    def force_ssl(self, val):
        """Sets the value for forceSSL with the parameter provided


        """
        self._force_ssl = val
        self.configure_network_settings = True

    @property
    def tunnel_init_seconds(self):
        """Gets the tunnel init seconds

        :return:
            int - tunnelInitSeconds
        """
        return self._tunnel_init_seconds

    @tunnel_init_seconds.setter
    def tunnel_init_seconds(self, val):
        """Sets the tunnelInitSeconds with the parameter provided


        """
        self._tunnel_init_seconds = val
        self.configure_network_settings = True

    @property
    def lockdown(self):
        """Gets the value for lockdown

        :return:
            boolean - lockdown
        """
        return self._lockdown

    @lockdown.setter
    def lockdown(self, val):
        """Sets the lockdown with the parameter provided


        """
        self._lockdown = val
        self.configure_network_settings = True

    @property
    def bind_open_ports(self):
        """Gets the value for bindOpenports only

        :return:
            boolean - bindOpenPortsOnly
        """
        return self._bind_open_ports_only

    @bind_open_ports.setter
    def bind_open_ports(self, val):
        """Sets bindopenportsonly with the parameter provided


        """
        self._bind_open_ports_only = val
        self.configure_network_settings = True

    @property
    def proxy(self):
        """Gets the value for isDMZ

        :return:
            boolean - isDMZ
        """
        return self._is_dmz

    @proxy.setter
    def proxy(self, val):
        """Sets the value for isDMZ with the parameter provided


        """
        self._is_dmz = val
        self.configure_network_settings = True

    @property
    def keep_alive_seconds(self):
        """Gets the value set for keep alive

        :return:
            int - keepAliveSeconds
        """
        return self._keep_alive_seconds

    @keep_alive_seconds.setter
    def keep_alive_seconds(self, val):
        """Sets the value for keep alive seconds with the parameter provided

        """
        self._keep_alive_seconds = val
        self.configure_network_settings = True

    @property
    def incoming_connections(self):
        """Gets all the incoming connections on a client

        :return:
            list - incoming connections
        """

        for incoming_connection in self._restriction_to:
            if incoming_connection['state'] in self._incoming_connection_type.keys():
                incoming_connection['state'] = self._incoming_connection_type[incoming_connection['state']]

        return self._restriction_to

    def set_incoming_connections(self, incoming_connections):
        """Sets the incoming connections on a client/client group with the list of values provided

         Args:
                incoming_connections(list)  -- list of incoming connections should be a list of dict containing
                incoming connection type, entity name and entity type.
                [{'state':val,'entity':val,'isClient':val}]

            Example:
            [
                {
                'state': 'RESTRICTED',
                'entity': 'centOS',
                'isClient' : True
                },

                {
                'state': 'BLOCKED',
                'entity':  'Edge Clients',
                'isClient' : False
                }
            ]

        Raises:
                SDKException:
                    if the required key is missing in the input value passed

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
    def additional_ports(self):
        """Gets the additional ports

        :return:
            list - ports
        """
        return self._port_range

    def set_additional_ports(self, ports, tunnelPort=8403):
        """Sets additional incoming ports and tunnel port with the values provided as parameter

            Args:
                tunnelPort (int) -- value to be set for tunnel port
                ports(list)  -- list of ports should be a list of dict containing start port and end port
                [{'startPort':val,'endPort':val}]

            Example:
            [
                {
                'startPort': 1024,
                'endPort': 1030
                },
                {
                'startPort': 2000,
                'endPort':4000
                }
            ]

            Raises:
                SDKException:
                    if the required key is missing in the input value passed
        """
        try:
            self._tunnel_connection_port = tunnelPort
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
    def outgoing_routes(self):
        """Gets the list of all outgoing routes

            :return:
                list - outgoing routes

        """

        for outgoing_route in self._network_outgoing_routes:
            if outgoing_route['fireWallOutGoingRouteOptions'][
                'connectionProtocol'] in self._firewall_outgoing_connection_protocol.keys():
                outgoing_route['fireWallOutGoingRouteOptions']['connectionProtocol'] = \
                    self._firewall_outgoing_connection_protocol[
                        outgoing_route['fireWallOutGoingRouteOptions']['connectionProtocol']]
            if outgoing_route['fireWallOutGoingRouteOptions']['routeType'] in self._firewall_outgoing_route_type.keys():
                outgoing_route['fireWallOutGoingRouteOptions']['routeType'] = self._firewall_outgoing_route_type[
                    outgoing_route['fireWallOutGoingRouteOptions']['routeType']]

        return self._network_outgoing_routes

    def set_outgoing_routes(self, outgoing_routes):
        """Sets outgoing routes on the client with the list of values provided as parameter

            Args:
                outgoing_routes(list)  -- list of outgoing routes should be a list of dict containing
                route type, entity name, entity type, streams, gateway host, gateway port and remote proxy based on
                route type.

                For routeType: DIRECT
                [{'routeType':'DIRECT', 'remoteEntity':val ,'streams':val, 'isClient':val, 'forceAllDataTraffic': True}]

                For routeType: VIA_GATEWAY
                [{'routeType':'VIA_GATEWAY', 'remoteEntity':val, 'streams':val, 'gatewayPort':val, 'gatewayHost': val,
                'isClient':val, 'forceAllDataTraffic': False}]

                For routeType: VIA_PROXY
                [{'routeType':'VIA_PROXY', 'remoteEntity':val, 'remoteProxy':val, 'isClient':val}]

            Example:
            [
                {
                'routeType': 'DIRECT',
                'remoteEntity':'Testcs' ,
                'streams': 1,
                'isClient': True,
                'forceAllDataTraffic' : True
                },
                {
                'routeType': 'VIA_GATEWAY',
                'remoteEntity': 'centOS',
                'streams': 2,
                'gatewayPort': 443,
                'gatewayHost': '1.2.3.4',
                'isClient': True,
                'forceAllDataTraffic' :False
                },
                {
                'routeType': 'VIA_PROXY',
                'remoteEntity': 'Laptop Clients',
                'remoteProxy': 'TemplateRHEL65_4',
                'isClient': False
                }
            ]

            Raises:
                SDKException:
                    if routeType is invalid in the input value passed

                    if the required key is missing in the input value passed

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

                elif outgoing_route['routeType'] == self._firewall_outgoing_route_type[1]:
                    gatewayport = outgoing_route['gatewayPort']
                    gatewayhostname = outgoing_route['gatewayHost']
                    remote_proxy = {}
                    nstreams = outgoing_route['streams']
                    force_all_data_traffic = outgoing_route['forceAllDataTraffic']

                elif outgoing_route['routeType'] == self._firewall_outgoing_route_type[2]:
                    gatewayport = 0
                    gatewayhostname = ""
                    nstreams = 1
                    force_all_data_traffic = False
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
                        "connectionProtocol": 2,
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
    def tppm_settings(self):
        """Gets the list of tppm settings on a client

        :return:
            list - tppm settings
        """

        for tppm_setting in self._tppm_settings:
            if tppm_setting['tppmType'] in self._tppm_type.keys():
                tppm_setting['tppmType'] = self._tppm_type[tppm_setting['tppmType']]

        return self._tppm_settings

    def set_tppm_settings(self, tppm_settings):
        """Sets tppm on the client with the list of values provided as parameter


            Note:  This is supported only on client level

            Args:
                tppm_settings(list)  -- list of tppm settings should be a list of dict containing
                tppm type, port number and proxy entity
                [{'tppmType':val, 'portNumber':val, 'proxyEntity':val}]

                Valid values for tppmType:
                1. WEB_SERVER_FOR_IIS_SERVER
                2. COMMSERVE
                3. REPORTS
                4. CUSTOM_REPORT_ENGINE

            Example:
            [
                {
                'tppmType': 'WEB_SERVER_FOR_IIS_SERVER',
                'portNumber':9999,
                'proxyEntity' : 'shezavm3'
                },

                {
                'tppmType': 'REPORTS',
                'portNumber':8888,
                'proxyEntity' : 'shezavm11'
                }
            ]

            Raises:
                SDKException:
                    if tppmType is invalid in the input value passed

                    if the required key is missing in the input value passed

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

    def _advanced_network_config(self):

        """Sets network properties on the client/client group with all the network properties


            Raises:
                SDKException:
                    if  request was not successful

                    if  invalid input was provided in the request

                    if empty response was received

        """

        if self.flag == "CLIENT":
            if self._config_network_settings == False:
                update_networkconfig_dict = {
                    "firewallConfiguration":
                        {
                            "configureFirewallSettings": self._config_network_settings
                        }
                }


            else:
                update_networkconfig_dict ={
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
                                "extendedProperties": "<App_FirewallExtendedProperties configureAutomatically=\"0\" defaultOutgoingProtocol=\"0\"/>",
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
            flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._client_object._CLIENT,
                                                                            request_json)

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

            if self._config_network_settings == False:
                request_json = {
                "clientGroupOperationType": 2,
                "clientGroupDetail": {
                "clientGroup": {
                    "clientGroupName": self._clientgroup_object._clientgroup_name
                },
                "firewallConfiguration":
                    {
                        "configureFirewallSettings": self._config_network_settings,

                    }

            }}

            else:
                request_json = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "clientGroup": {
                    "clientGroupName": self._clientgroup_object._clientgroup_name
                },
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
                            "extendedProperties": "<App_FirewallExtendedProperties configureAutomatically=\"0\" defaultOutgoingProtocol=\"0\"/>",
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
                        raise SDKException('ClientGroup', '102', 'Client group properties were not updated')

                else:
                    self._get_network_properties()
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                self._get_network_properties()
                raise SDKException('Response', '101', response_string)
