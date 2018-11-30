# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing network topology operations.

NetworkTopologies and NetworkTopology are 2 classes defined in this file.

NetworkTopologies: Class for representing all the network topologies in
the commcell

NetworkTopology: class for a single topology in commcell


NetworkTopologies:
    __init__(class_object)              --  initialize object of NetworkTopologies
                                            class associated with the commcell

    __repr__()                          --  returns the string to represent the instance
                                            of the NetworkTopologies class

    all_network_topologies()            -- returns dict of all the network topologies
                                            in the commcell

    __len__()                           --  returns the number of topologies associated
                                            with the Commcell

    add(topology_name)                  -- adds a new network topology to the commcell

    get(topology_name)                  --  returns the NetworkTopology class object of
                                            the input topology name

    delete(topology_name)               --  deletes the specified network topology
                                            from the commcell

    refresh()                           -- refresh the network topologies associated
                                            with the commcell


NetworkTopology:

   __init__(commcell_object,
             network_topology_name,
             network_topology_id=None)      -- initialize object of NetworkTopology class
                                               with the specified network topology name and id

    __repr__()                              -- return the network topology name, the instance
                                                is associated with

    _get_network_topology_id()              -- method to get the network topology id if
                                               not specified

    _initialize_network_topology_properties()-- initializes the properties of this network
                                                topology

    update()                                -- update properties of existing network topology

    network_topology_name()                 -- updates new name for network topology

    description()                           -- updates description for network topology

    network_topology_type()                 -- updates network topology type

    firewall_groups()                       -- updates client groups associated with the topology

    push_network_config()                   -- performs a push network configuration on
                                               network topology

    refresh()                               -- refresh the properties of  network topology

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from past.builtins import basestring
from .exception import SDKException


class NetworkTopologies(object):
    """Class for getting all the network topologies associated with client groups in commcell."""

    def __init__(self, commcell_object):
        """Initialize the NetworkTopologies object.

            Args:
                commcell_object    (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the NetworkTopologies class

        """

        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._NETWORK_TOPOLOGIES = self._services['NETWORK_TOPOLOGIES']
        self._network_topologies = None
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of NetworkTopologies class."""

        return "NetworkTopologies class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_network_topologies(self):
        """Gets all the network topologies associated with the commcell

            Returns:
                dict - consists of all network topologies of the commcell
                    {
                         "network_topology_name1": network_topology_id1,
                         "network_topology_name2": network_topology_id2
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        flag, response = self._cvpysdk_object.make_request('GET', self._NETWORK_TOPOLOGIES)
        network_topologies_dict = {}
        if flag:
            if response.json():
                if 'error' in response.json() and response.json()['error']['errorCode'] == 0:
                    if 'firewallTopologies' in response.json():
                        network_topologies = response.json()['firewallTopologies']

                        for network_topology in network_topologies:
                            temp_name = network_topology['topologyEntity']['topologyName'].lower()
                            temp_id = network_topology['topologyEntity']['topologyId']
                            network_topologies_dict[temp_name] = temp_id

                        return network_topologies_dict

                    else:
                        return network_topologies_dict

                else:
                    raise SDKException('NetworkTopology', '102', 'Custom error message')

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_network_topologies(self):
        """Returns dict of all the network topologies associated with the commcell

            dict - consists of all network topologies of the commcell
                    {
                         "network_topology_name": network_topology_id,

                         "network_topology_name": network_topology_id
                    }
        """

        return self._network_topologies

    def __len__(self):
        """Returns the number of network topologies associated to the Commcell."""

        return len(self.all_network_topologies)

    def has_network_topology(self, network_topology_name):
        """Checks if a network topology exists in the commcell with the input network topology name.

            Args:
                network_topology_name (str)  --  name of network topology

            Returns:
                bool - boolean output whether the network topology exists in the commcell or not

            Raises:
                SDKException:
                    if type of the network topology name argument is not string
        """

        if not isinstance(network_topology_name, basestring):
            raise SDKException('NetworkTopology', '101')

        return (self._network_topologies and
                network_topology_name.lower() in self._network_topologies)

    def add(self, network_topology_name, client_groups=None, **kwargs):
        """Adds a new Network Topology to the Commcell.

            Args:
                network_topology_name        (str)        --  name of the new network
                                                              topology to add

                client_groups               (list of dict) -- client group names and
                                                              client group types

                [{'group_type':2, 'group_name': "test1", 'is_mnemonic': False },
                {'group_type':1, 'group_name': "test2", 'is_mnemonic': False },
                {'group_type':3, 'group_name': "test3", 'is_mnemonic': False }]

                ** kwargs               (dict)       -- Key value pairs for supported
                                                        arguments

                Supported argument values:

                use_wildcardproxy   (boolean)  --   option to use wildcard proxy for proxy type
                                                 topology
                                                 Default value: False

                is_smart_topology   (boolean)  --   specified as true for smart topology
                                                 Default value: False

                topology_type        (int)     --   to specify type of network topology

                topology_description (str)     --   to specify topology description

                display_type         (int)     --   to specify display type for firewall extended
                                                 properties
                                                 Default value: 0

                Possible input values:

                topology_type :
                1 --- for proxy topology
                2 --- for one-way topology
                3 --- for two-way topology

                display_type:
                0 --- servers
                1 --- laptops

                group_type for client_groups:
                2: first client group in GUI screen
                1: second client group in GUI screen
                3: third client group in GUI screen

                is_mnemonic for client_groups:
                True: if the specified group is a mnemonic
                False: if the specified group is a client group


            Returns:
                object - instance of the NetworkTopology class created by this method

            Raises:
                SDKException:
                    if topology creation fails

                    if topology with same name already exists

                    if client group specified is already a part of some topology

        """
        if not isinstance(network_topology_name, basestring):
            raise SDKException('NetworkTopology', '101')

        if not isinstance(client_groups, list):
            raise SDKException('NetworkTopology', '102',
                               'Client Groups should be a list of dict containing group '
                               'name and group type')

        firewall_groups_list = []

        display_type = kwargs.get('display_type', 0)

        if display_type == 1:
            d_type = "<App_TopologyExtendedProperties displayType=\"1\" />"
        else:
            d_type = "<App_TopologyExtendedProperties displayType=\"0\" />"

        for client_group in client_groups:
            firewall_groups_dict = {
                "fwGroupType": client_group.get('group_type'),
                "isMnemonic": client_group.get('is_mnemonic', False),
                "clientGroup": {
                    "clientGroupName": client_group.get('group_name')
                    }
                }

            firewall_groups_list.append(firewall_groups_dict)

        if not self.has_network_topology(network_topology_name):

            request_json = {
                "firewallTopology": {
                    "useWildcardProxy": kwargs.get('use_wildcard', False),
                    "extendedProperties": d_type,
                    "topologyType": kwargs.get('topology_type', 2),
                    "description": kwargs.get('topology_description', ''),
                    "isSmartTopology": kwargs.get('is_smart_topology', False),

                    "firewallGroups": firewall_groups_list,
                    "topologyEntity": {
                        "topologyName": network_topology_name

                        }
                    }
                }

            flag, response = self._cvpysdk_object.make_request('POST',
                                                               self._NETWORK_TOPOLOGIES,
                                                               request_json)

            if flag:
                if response.json():

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']
                        raise SDKException('NetworkTopology', '102',
                                           'Failed to create new Network Topology\nError:"{0}"'
                                           .format(error_message))

                    elif 'topology' in response.json():
                        self.refresh()

                        return self.get(network_topology_name)

                    else:
                        raise SDKException('NetworkTopology', '102',
                                           'Failed to create new Network Topology')
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException('NetworkTopology', '102',
                               'Network Topology "{0}" already exists.'.
                               format(network_topology_name))

    def get(self, network_topology_name):
        """Returns the network topology object of the specified network topology name.

            Args:
                network_topology_name (str)  --  name of the network topology

            Returns:
                object - instance of the NetworkTopology class for the given network topology name

            Raises:
                SDKException:
                    if type of the network topology name argument is not string

                    if no network topology exists with the given name

        """
        if not isinstance(network_topology_name, basestring):
            raise SDKException('NetworkTopology', '101')
        else:
            network_topology_name = network_topology_name.lower()

            if self.has_network_topology(network_topology_name):
                return NetworkTopology(
                    self._commcell_object, network_topology_name,
                    self._network_topologies[network_topology_name])

            raise SDKException('NetworkTopology', '102',
                               'No Network Topology exists with name: {0}'.
                               format(network_topology_name))

    def delete(self, network_topology_name):
        """Deletes the Network Topology from the commcell.

            Args:
                network_topology_name (str)  --  name of the network topology

            Raises:
                SDKException:
                    if type of the network topology name argument is not string

                    if failed to delete the network topology

                    if no network topology exists with the given name
        """

        if not isinstance(network_topology_name, basestring):
            raise SDKException('NetworkTopology', '101')
        else:
            network_topology_name = network_topology_name.lower()

            if self.has_network_topology(network_topology_name):
                network_topology_id = self._network_topologies[network_topology_name]

                delete_network_topology_service = self._services['NETWORK_TOPOLOGY']

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'DELETE', delete_network_topology_service % network_topology_id
                )

                if flag:
                    if response.json():
                        if 'errorCode' in response.json():
                            error_code = str(response.json()['errorCode'])
                            error_message = response.json()['errorMessage']

                            if error_code == '0':
                                self.refresh()
                            else:
                                raise SDKException('NetworkTopology', '102',
                                                   'Failed to delete topology\nError: "{0}"'.
                                                   format(error_message))
                        else:
                            raise SDKException('Response', '102')
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'NetworkTopology',
                    '102',
                    'No Network Topology exists with name: "{0}"'.format(network_topology_name)
                )

    def refresh(self):
        """Refresh the network topologies associated with the Commcell."""

        self._network_topologies = self._get_network_topologies()


class NetworkTopology(object):
    """Class for performing operations for a specific network topology."""

    def __init__(self, commcell_object, network_topology_name, network_topology_id=None):
        """Initialize the NetworkTopology class instance.

            Args:
                commcell_object     (object)        --  instance of the Commcell class

                network_topology_name    (str)      --  name of the network topology

                network_topology_id   (str)         --  id of the network topology
                    default: None

            Returns:
                object - instance of the NetworkTopology class

        """

        self._commcell_object = commcell_object

        self._network_topology_name = network_topology_name.lower()

        self._properties = None

        self._description = None

        self._extended_properties = None

        self._network_topology_type = None

        self._firewall_groups = []

        if network_topology_id:

            self._network_topology_id = str(network_topology_id)

        else:

            self._network_topology_id = self._get_network_topology_id()

        self._NETWORKTOPOLOGY = (self._commcell_object._services['NETWORK_TOPOLOGY'] %
                                 self.network_topology_id)

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string containing the details of this NetworkTopology

        """

        representation_string = 'NetworkTopology class instance for NetworkTopology: "{0}"'

        return representation_string.format(self.network_topology_name)

    def _get_network_topology_id(self):
        """Gets the network topology id associated with network topology.

            Returns:
                str - id associated with network topology

        """

        network_topologies = NetworkTopologies(self._commcell_object)

        return network_topologies.get(self.network_topology_name).network_topology_id

    def _initialize_network_topology_properties(self):
        """Gets the network topology properties of network topology and
        initializes the common properties for the network topology

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

                    if topology name is not specified in the response

                    if topology type is missing in the response

        """

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._NETWORKTOPOLOGY
        )

        if flag:
            if response.json() and 'topologyInfo' in response.json():
                network_topology_props = response.json()['topologyInfo']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self._properties = network_topology_props

        if 'topologyName' in network_topology_props['topologyEntity']:
            self._network_topology_name = network_topology_props['topologyEntity']['topologyName']
        else:
            raise SDKException(
                'NetworkTopology', '102', 'Network Topology name is not specified in the respone'
            )

        self._description = network_topology_props.get('description')

        self._extended_properties = network_topology_props.get('extendedProperties')

        if 'topologyType' in network_topology_props:
            self._network_topology_type = network_topology_props['topologyType']
        else:
            raise SDKException(
                'NetworkTopology', '102', 'Network Topology type is not specified in the response'
            )

        self._firewall_groups = network_topology_props.get('firewallGroups')

    def update(self, firewall_groups=None, **kwargs):
        """Update the network topology properties of network topology.

            Args:

                firewall_groups(list of dict)  --   client group names and client
                                                    group types

                [{'group_type':2, 'group_name': "test1", 'is_mnemonic': False },
                {'group_type':1, 'group_name': "test2", 'is_mnemonic': False },
                {'group_type':3, 'group_name': "test3", 'is_mnemonic': False }]

                **kwargs             (dict)  -- Key value pairs for supported arguments

                Supported arguments:

                network_topology_name   (str)       --  new name of the network topology

                description             (str)       --  description for the network topology

                topology_type           (int)       -- network topology type

                wildcard_proxy          (boolean)   -- option to use wildcard proxy for
                                                     proxy type topology

                is_smart_topology       (boolean)   -- specified as true for smart topology

                Possible input values:

                topology_type :
                1 --- for proxy topology
                2 --- for one-way topology
                3 --- for two-way topology

                group_type for client_groups:
                2: first client group in GUI screen
                1: second client group in GUI screen
                3: third client group in GUI screen

                is_mnemonic for client_groups:
                True: if the specified group is a mnemonic
                False: if the specified group is a client group

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        firewall_groups_list = []

        if firewall_groups is None:
            firewall_groups_list = self.firewall_groups

        else:
            for client_group in firewall_groups:
                firewall_groups_dict = {
                    "fwGroupType": client_group.get('group_type'),
                    "isMnemonic": client_group.get('is_mnemonic', False),
                    "clientGroup": {
                        "clientGroupName": client_group.get('group_name')
                        }
                    }

                firewall_groups_list.append(firewall_groups_dict)

        network_topology_name = kwargs.get('network_topology_name', self.network_topology_name)

        description = kwargs.get('description', self.description)

        topology_type = kwargs.get('topology_type', self.network_topology_type)

        wildcard_proxy = kwargs.get('wildcard_proxy', False)

        is_smart_topology = kwargs.get('is_smart_topology', False)

        extended_properties = self.extended_properties

        request_json = {
            "firewallTopology": {
                "useWildcardProxy": wildcard_proxy,
                "extendedProperties": extended_properties,
                "topologyType": topology_type,
                "description": description,
                "isSmartTopology": is_smart_topology,
                "firewallGroups": firewall_groups_list,
                "topologyEntity": {
                    "topologyName": network_topology_name
                    }
                }
            }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._NETWORKTOPOLOGY, request_json
        )

        if flag:
            if response.json():

                error_message = response.json()['errorMessage']
                error_code = str(response.json()['errorCode'])

                if error_code != '0':
                    raise SDKException('NetworkTopology', '102', error_message)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    @property
    def network_topology_id(self):
        """Treats the network topology id as a read-only attribute."""

        return self._network_topology_id

    @property
    def network_topology_name(self):
        """Treats the network topology name as a read-only attribute."""

        return self._network_topology_name

    @network_topology_name.setter
    def network_topology_name(self, val):
        """Sets the value for network topology name

            args:

                val(string)  --  new name for network topology

        """

        self.update(**{'network_topology_name': val})

    @property
    def description(self):
        """Treats the network topology description as a read-only attribute."""

        return self._description

    @description.setter
    def description(self, val):
        """Sets the description for network topology

            args:

                val(string)  --  network topology description

        """
        self.update(**{'description': val})

    @property
    def network_topology_type(self):
        """Treats the network topology type as read-only attribute"""

        return self._network_topology_type

    @network_topology_type.setter
    def network_topology_type(self, val):
        """Sets the value for network topology type

            args:

                val(int)  --  network topology type

                topology_type :
                1 --- for proxy topology
                2 --- for one-way topology
                3 --- for two-way topology

        """
        self.update(**{'topology_type': val})

    @property
    def extended_properties(self):
        """Treats the extended properties as read-only attribute"""

        return self._extended_properties

    @property
    def firewall_groups(self):
        """Treats the associated client groups as read only attribute"""

        return self._firewall_groups

    @firewall_groups.setter
    def firewall_groups(self, val):
        """Sets the value for associated client groups

            Args:

                val(list of dict)  --   client group names and client group types

                [{'group_type':2, 'group_name': "test1", 'is_mnemonic': False },
                {'group_type':1, 'group_name': "test2", 'is_mnemonic': False },
                {'group_type':3, 'group_name': "test3", 'is_mnemonic': False }]

                group_type for client_groups:
                2: first client group in GUI screen
                1: second client group in GUI screen
                3: third client group in GUI screen

                is_mnemonic for client_groups:
                True: if the specified group is a mnemonic
                False: if the specified group is a client group

            Raises:
                SDKException:
                    if input value is not a list

        """
        if not isinstance(val, list):
            raise SDKException('NetworkTopology', '102',
                               'Client Groups should be a list of dict containing '
                               'group name and group type')

        self.update(val)

    def push_network_config(self):
        """Performs a push network configuration on network topology

            Raises:
                SDKException:

                    if failed to push configuration on network topology

                    if response is not success

        """

        push_network_topology_service = self._commcell_object._services['PUSH_TOPOLOGY']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', push_network_topology_service % self._network_topology_id)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = str(response.json()['error']['errorCode'])
                    error_message = response.json()['error']['errorString']

                    if error_code != '0':
                        raise SDKException('NetworkTopology', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of Network Topology"""

        self._initialize_network_topology_properties()
