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
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .exception import SDKException

if TYPE_CHECKING:
    from .clientgroup import ClientGroup
    from .commcell import Commcell

class NetworkTopologies(object):
    """
    Manages network topologies associated with client groups in a CommCell environment.

    This class provides a comprehensive interface for retrieving, managing, and manipulating
    network topologies linked to client groups. It allows users to query, add, delete, and
    verify network topologies, as well as manage firewall groups and smart topology groups.

    Key Features:
        - Retrieve all network topologies associated with client groups
        - Access all network topologies via a property
        - Check for the existence of a specific network topology
        - Verify smart topology groups with mnemonic counts
        - Create firewall groups lists for specified client groups
        - Add new network topologies and associate them with client groups
        - Get details of a specific network topology
        - Delete existing network topologies
        - Refresh the network topology data
        - Obtain the number of network topologies
        - String representation for easy inspection

    Args:
        commcell_object: The CommCell object used for network topology operations.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a NetworkTopologies object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> network_topologies = NetworkTopologies(commcell)
            >>> print(type(network_topologies))
            <class 'NetworkTopologies'>

        #ai-gen-doc
        """

        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._NETWORK_TOPOLOGIES = self._services['NETWORK_TOPOLOGIES']
        self._network_topologies = None
        self.refresh()

    def __repr__(self) -> str:
        """Return the string representation of the NetworkTopologies instance.

        This method provides a developer-friendly string that identifies the NetworkTopologies object,
        which can be useful for debugging and logging purposes.

        Returns:
            A string representation of the NetworkTopologies instance.

        Example:
            >>> topologies = NetworkTopologies()
            >>> print(repr(topologies))
            <NetworkTopologies object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """

        return "NetworkTopologies class instance for Commcell"

    def _get_network_topologies(self) -> dict:
        """Retrieve all network topologies associated with the Commcell.

        Returns:
            dict: A dictionary mapping network topology names to their corresponding IDs.
                Example:
                    {
                        "network_topology_name1": network_topology_id1,
                        "network_topology_name2": network_topology_id2
                    }

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> topologies = network_topologies._get_network_topologies()
            >>> print(topologies)
            {'DMZ_Topology': 101, 'Internal_Topology': 102}

        #ai-gen-doc
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
    def all_network_topologies(self) -> Dict[str, int]:
        """Get a dictionary of all network topologies associated with the Commcell.

        Returns:
            Dict[str, int]: A dictionary mapping network topology names to their corresponding IDs.

        Example:
            >>> topologies = network_topologies.all_network_topologies
            >>> print(topologies)
            {'DMZ_Topology': 101, 'Internal_Network': 102}
            >>> # Access a specific topology ID by name
            >>> dmz_id = topologies.get('DMZ_Topology')
            >>> print(f"DMZ Topology ID: {dmz_id}")

        #ai-gen-doc
        """

        return self._network_topologies

    def __len__(self) -> int:
        """Return the number of network topologies associated with the Commcell.

        Returns:
            The total count of network topologies managed by this object.

        Example:
            >>> topologies = NetworkTopologies(commcell_object)
            >>> count = len(topologies)
            >>> print(f"Number of network topologies: {count}")
        #ai-gen-doc
        """

        return len(self.all_network_topologies)

    def has_network_topology(self, network_topology_name: str) -> bool:
        """Check if a network topology with the specified name exists in the Commcell.

        Args:
            network_topology_name: The name of the network topology to check.

        Returns:
            True if the network topology exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the network_topology_name argument is not a string.

        Example:
            >>> topologies = NetworkTopologies(commcell_object)
            >>> exists = topologies.has_network_topology("Production_Network")
            >>> print(f"Network topology exists: {exists}")
            # Output: Network topology exists: True

        #ai-gen-doc
        """

        if not isinstance(network_topology_name, str):
            raise SDKException('NetworkTopology', '101')

        return (self._network_topologies and
                network_topology_name.lower() in self._network_topologies)

    @staticmethod
    def verify_smart_topology_groups(is_smartTopology: bool, count_mnemonic: int) -> None:
        """Verify client groups when creating a smart topology.

        This helper function checks the validity of client group configurations 
        during the creation of a smart topology. It ensures that the provided 
        parameters for smart topology and mnemonic group count are appropriate.

        Args:
            is_smartTopology: Indicates whether the topology being created is a smart topology.
            count_mnemonic: The number of mnemonic groups specified for the topology.

        Raises:
            SDKException: If the client group configuration is invalid for a smart topology.

        Example:
            >>> NetworkTopologies.verify_smart_topology_groups(True, 3)
            >>> # If the configuration is invalid, an SDKException will be raised

        #ai-gen-doc
        """

        if is_smartTopology:
            if count_mnemonic == 0:
                raise SDKException('NetworkTopology', '102',
                                   ' One client group should be mnemonic in a smart topology'
                                   )
            elif count_mnemonic > 1:
                raise SDKException('NetworkTopology', '102',
                                   'There cannot be more than one mnemonic group in a topology')
        elif count_mnemonic != 0:
            raise SDKException('NetworkTopology', '102',
                               ' Mnemonic group cannot be present in Non-smart toplogy'
                               )

    @staticmethod
    def create_firewall_groups_list(client_groups: list[dict]) -> tuple[list[dict], int]:
        """Create a list of firewall groups and count the number of mnemonic groups.

        This helper function processes a list of client group dictionaries, each containing
        information about group type, group name, and whether the group is mnemonic. It returns
        a tuple with the processed firewall groups list and the count of mnemonic groups.

        Args:
            client_groups: A list of dictionaries, where each dictionary represents a client group
                with keys:
                    - 'group_type' (int): The type of the group.
                    - 'group_name' (str): The name of the group.
                    - 'is_mnemonic' (bool): Whether the group is mnemonic.

                Example:
                    [
                        {'group_type': 2, 'group_name': "test1", 'is_mnemonic': False},
                        {'group_type': 1, 'group_name': "test2", 'is_mnemonic': False},
                        {'group_type': 3, 'group_name': "test3", 'is_mnemonic': False}
                    ]

        Returns:
            A tuple containing:
                - firewall_groups_list (list of dict): The processed list of firewall group dictionaries.
                - mnemonic_groups_count (int): The number of mnemonic groups in the input list.

        Example:
            >>> client_groups = [
            ...     {'group_type': 2, 'group_name': "test1", 'is_mnemonic': False},
            ...     {'group_type': 1, 'group_name': "test2", 'is_mnemonic': True},
            ...     {'group_type': 3, 'group_name': "test3", 'is_mnemonic': False}
            ... ]
            >>> firewall_groups, mnemonic_count = NetworkTopologies.create_firewall_groups_list(client_groups)
            >>> print(firewall_groups)
            >>> print(f"Number of mnemonic groups: {mnemonic_count}")

        #ai-gen-doc
        """
        count_mnemonic = 0
        firewall_groups_list = []

        mnemonic_grp_set = {'My CommServe Computer and MediaAgents', 'My CommServe Computer',
                            'My MediaAgents'}

        for client_group in client_groups:
            is_mnemonic = client_group.get('is_mnemonic', False)
            if is_mnemonic:
                if client_group.get('group_name') not in mnemonic_grp_set:
                    raise SDKException('NetworkTopology', '102',
                                       'Client group {0} is not a mnemonic group'.format(client_group.get('group_name'))
                                       )
                if client_group.get('group_type') in {3, 4}:
                    raise SDKException('NetworkTopology', '102',
                                       'Proxy Client group {0} cannot be a mnemonic group'.format(
                                           client_group.get('group_name'))
                                       )
                count_mnemonic += 1
            firewall_groups_dict = {
                "fwGroupType": client_group.get('group_type'),
                "isMnemonic": client_group.get('is_mnemonic', False),
                "clientGroup": {
                    "clientGroupName": client_group.get('group_name')
                }
            }
            firewall_groups_list.append(firewall_groups_dict)

        return (firewall_groups_list, count_mnemonic)

    def add(self, network_topology_name: str, client_groups: Optional[List[Dict[str, Any]]] = None, **kwargs: Any) -> 'NetworkTopology':
        """Add a new Network Topology to the Commcell.

        This method creates a new network topology with the specified name and client groups.
        Additional configuration options can be provided as keyword arguments.

        Args:
            network_topology_name: The name of the new network topology to add.
            client_groups: Optional list of dictionaries specifying client group details.
                Each dictionary should contain:
                    - group_type (int): Type of the group (1: Infrastructure, 2: Servers, 3: Server Gateways, 4: DMZ Gateways)
                    - group_name (str): Name of the client group
                    - is_mnemonic (bool): True if the group is a mnemonic, False if it is a client group

                Example for Gateway topology:
                    [
                        {'group_type': 2, 'group_name': "test1", 'is_mnemonic': False},
                        {'group_type': 1, 'group_name': "test2", 'is_mnemonic': False},
                        {'group_type': 3, 'group_name': "test3", 'is_mnemonic': False}
                    ]

                Example for Cascading topology:
                    [
                        {'group_type': 2, 'group_name': "test1", 'is_mnemonic': False},
                        {'group_type': 1, 'group_name': "test2", 'is_mnemonic': False},
                        {'group_type': 3, 'group_name': "test3", 'is_mnemonic': False},
                        {'group_type': 4, 'group_name': "test33", 'is_mnemonic': False}
                    ]
            **kwargs: Additional keyword arguments for topology configuration. Supported keys include:
                - use_wildcard (bool): Use wildcard proxy for proxy type topology (default: False)
                - is_smart_topology (bool): Set to True for smart topology if a mnemonic group is present (default: False)
                - topology_type (int): Type of network topology (1: Gateway, 2: One-way, 3: Two-way, 4: Cascading, etc.)
                - topology_description (str): Description of the topology
                - display_type (int): Display type for firewall extended properties (0: servers, 1: laptops; default: 0)
                - encrypt_traffic (int): Whether to encrypt traffic (default: 0)
                - number_of_streams (int): Number of streams (default: 1)
                - region_id (int): Region ID (default: 0)
                - connection_protocol (int): Protocols to use (default: 2)

        Returns:
            NetworkTopology: An instance of the created NetworkTopology.

        Raises:
            SDKException: If topology creation fails, if a topology with the same name already exists,
                or if a specified client group is already part of another topology.

        Example:
            >>> client_groups = [
            ...     {'group_type': 2, 'group_name': "ServersGroup", 'is_mnemonic': False},
            ...     {'group_type': 1, 'group_name': "InfraGroup", 'is_mnemonic': False},
            ...     {'group_type': 3, 'group_name': "GatewayGroup", 'is_mnemonic': False}
            ... ]
            >>> topology = network_topologies.add(
            ...     network_topology_name="MyGatewayTopology",
            ...     client_groups=client_groups,
            ...     topology_type=1,
            ...     topology_description="Main gateway topology",
            ...     encrypt_traffic=1
            ... )
            >>> print(f"Created topology: {topology}")

        #ai-gen-doc
        """

        if not isinstance(network_topology_name, str):
            raise SDKException('NetworkTopology', '101')

        if not isinstance(client_groups, list):
            raise SDKException('NetworkTopology', '102',
                               'Client Groups should be a list of dict containing group '
                               'name and group type')

        firewall_groups_list = []
        count_mnemonic = 0

        display_type = kwargs.get('display_type', 0)

        extended_properties = f'''<App_TopologyExtendedProperties displayType=\"{kwargs.get('display_type', 0)}\" encryptTraffic=\"{kwargs.get('encrypt_traffic', 0)}\"
        numberOfStreams =\"{kwargs.get('number_of_streams', 1)}\" regionId=\"{kwargs.get('region_id', 0)}\" connectionProtocol=\"{kwargs.get('connection_protocol', 2)}\" />'''

        firewall_groups_list, count_mnemonic = self.create_firewall_groups_list(client_groups)

        is_smartTopology = kwargs.get('is_smart_topology', False)

        self.verify_smart_topology_groups(is_smartTopology, count_mnemonic)

        if not self.has_network_topology(network_topology_name):

            request_json = {
                "firewallTopology": {
                    "useWildcardProxy": kwargs.get('use_wildcard', False),
                    "extendedProperties": extended_properties,
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

    def get(self, network_topology_name: str) -> 'NetworkTopology':
        """Retrieve the network topology object for the specified network topology name.

        Args:
            network_topology_name: The name of the network topology to retrieve.

        Returns:
            NetworkTopology: An instance of the NetworkTopology class corresponding to the given name.

        Raises:
            SDKException: If the network_topology_name is not a string, or if no network topology exists with the given name.

        Example:
            >>> topologies = NetworkTopologies(commcell_object)
            >>> topology = topologies.get("Production_Network")
            >>> print(f"Retrieved topology: {topology}")

        #ai-gen-doc
        """
        if not isinstance(network_topology_name, str):
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

    def delete(self, network_topology_name: str) -> None:
        """Delete a network topology from the Commcell.

        Removes the specified network topology by name. If the topology does not exist,
        or if deletion fails, an SDKException is raised.

        Args:
            network_topology_name: The name of the network topology to delete.

        Raises:
            SDKException: If the network topology name is not a string,
                if deletion fails, or if no topology exists with the given name.

        Example:
            >>> topologies = NetworkTopologies(commcell_object)
            >>> topologies.delete("OfficeNetwork")
            >>> print("Network topology 'OfficeNetwork' deleted successfully.")

        #ai-gen-doc
        """

        if not isinstance(network_topology_name, str):
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

    def refresh(self) -> None:
        """Reload the network topologies associated with the Commcell.

        This method clears any cached network topology data, ensuring that subsequent accesses
        retrieve the most up-to-date information from the Commcell.

        Example:
            >>> network_topologies = NetworkTopologies(commcell_object)
            >>> network_topologies.refresh()  # Refreshes the network topology cache
            >>> print("Network topologies refreshed successfully")

        #ai-gen-doc
        """

        self._network_topologies = self._get_network_topologies()


class NetworkTopology(object):
    """
    Class for managing and performing operations on a specific network topology.

    This class provides an interface to interact with network topology objects, allowing
    users to retrieve and update topology properties, manage firewall groups, and push
    network configurations. It supports property accessors for key attributes such as
    topology ID, name, type, description, extended properties, firewall groups, and wildcard proxy.
    The class also includes methods for refreshing topology data and updating firewall group settings.

    Key Features:
        - Initialization with commcell object, topology name, and ID
        - Property accessors for topology ID, name, type, description, extended properties, firewall groups, and wildcard proxy
        - Update firewall groups associated with the topology
        - Push network configuration changes
        - Refresh topology properties from the source
        - Internal methods for topology ID retrieval and property initialization
        - String representation for easy identification

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', network_topology_name: str, network_topology_id: str = None) -> None:
        """Initialize a new instance of the NetworkTopology class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            network_topology_name: The name of the network topology to manage.
            network_topology_id: Optional; the unique identifier of the network topology. If not provided, it will be determined automatically.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> topology = NetworkTopology(commcell, 'Corporate_Network')
            >>> # Optionally, provide a topology ID
            >>> topology_with_id = NetworkTopology(commcell, 'Corporate_Network', '12345')

        #ai-gen-doc
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

    def __repr__(self) -> str:
        """Return a string representation of the NetworkTopology instance.

        This method provides a human-readable string that describes the current
        NetworkTopology object, which can be useful for debugging or logging.

        Returns:
            A string containing details about this NetworkTopology instance.

        Example:
            >>> topology = NetworkTopology()
            >>> print(repr(topology))
            <NetworkTopology: ...>

        #ai-gen-doc
        """

        representation_string = 'NetworkTopology class instance for NetworkTopology: "{0}"'

        return representation_string.format(self.network_topology_name)

    def _get_network_topology_id(self) -> str:
        """Retrieve the unique identifier associated with the network topology.

        Returns:
            The network topology ID as a string.

        Example:
            >>> topology = NetworkTopology()
            >>> topology_id = topology._get_network_topology_id()
            >>> print(f"Network Topology ID: {topology_id}")

        #ai-gen-doc
        """

        network_topologies = NetworkTopologies(self._commcell_object)

        return network_topologies.get(self.network_topology_name).network_topology_id

    def _initialize_network_topology_properties(self) -> None:
        """Retrieve and initialize the network topology properties for this NetworkTopology instance.

        This method fetches the network topology details and sets up the common properties
        required for further operations. It ensures that essential information such as topology
        name and type are present in the response.

        Raises:
            SDKException: If the response is empty, unsuccessful, missing the topology name,
                or missing the topology type.

        Example:
            >>> topology = NetworkTopology()
            >>> topology._initialize_network_topology_properties()
            >>> # The topology properties are now initialized and ready for use

        #ai-gen-doc
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

    def update(self, firewall_groups: Optional[list[dict]] = None, **kwargs: Any) -> None:
        """Update the network topology properties for this network topology.

        This method allows you to modify various properties of the network topology, such as client group associations,
        topology name, description, type, and advanced options like encryption and protocol settings.

        Args:
            firewall_groups: Optional list of dictionaries specifying client group details. Each dictionary should contain:
                - group_type (int): The type of client group (1, 2, or 3).
                - group_name (str): The name of the client group.
                - is_mnemonic (bool): True if the group is a mnemonic, False if it is a client group.
                Example:
                    [
                        {'group_type': 2, 'group_name': "test1", 'is_mnemonic': False},
                        {'group_type': 1, 'group_name': "test2", 'is_mnemonic': False},
                        {'group_type': 3, 'group_name': "test3", 'is_mnemonic': False}
                    ]
            **kwargs: Additional keyword arguments for supported network topology properties:
                - network_topology_name (str): New name for the network topology.
                - description (str): Description for the network topology.
                - topology_type (int): Type of topology (1: proxy, 2: one-way, 3: two-way).
                - wildcard_proxy (bool): Whether to use wildcard proxy for proxy type topology.
                - is_smart_topology (bool): Set to True for smart topology.
                - encrypt_traffic (int): Specify whether to encrypt traffic (default: 0).
                - number_of_streams (int): Number of streams (default: 1).
                - region_id (int): Region ID (default: 0).
                - connection_protocol (int): Protocols to use (default: 2).

        Raises:
            SDKException: If the response is empty or the update operation is not successful.

        Example:
            >>> topology = NetworkTopology()
            >>> firewall_groups = [
            ...     {'group_type': 2, 'group_name': "GroupA", 'is_mnemonic': False},
            ...     {'group_type': 1, 'group_name': "GroupB", 'is_mnemonic': True}
            ... ]
            >>> topology.update(
            ...     firewall_groups=firewall_groups,
            ...     network_topology_name="NewTopologyName",
            ...     description="Updated topology for new region",
            ...     topology_type=2,
            ...     encrypt_traffic=1,
            ...     number_of_streams=4
            ... )
            >>> print("Network topology updated successfully.")

        #ai-gen-doc
        """

        firewall_groups_list = []
        count_mnemonic = 0
        if firewall_groups is None:
            firewall_groups_list = self.firewall_groups

        else:
            firewall_groups_list, count_mnemonic = NetworkTopologies.create_firewall_groups_list(firewall_groups)

        network_topology_name = kwargs.get('network_topology_name', self.network_topology_name)

        description = kwargs.get('description', self.description)

        topology_type = kwargs.get('topology_type', self.network_topology_type)

        wildcard_proxy = kwargs.get('wildcard_proxy', False)

        is_smart_topology = kwargs.get('is_smart_topology', False)

        NetworkTopologies.verify_smart_topology_groups(is_smart_topology, count_mnemonic)

        extended_properties = self.extended_properties
        properties = ['display_type', 'encrypt_traffic', 'number_of_streams', 'region_id', 'connection_protocol']
        for prop in properties:
            if prop in kwargs:
                temp = prop.split('_')
                for i in range(1, len(temp)):
                    temp[i] = temp[i][0].upper() + temp[i][1:]
                camel_case_prop = ''.join(temp)

                idx = extended_properties.find(camel_case_prop) + len(camel_case_prop) + len("\"=")
                temp = list(extended_properties)
                temp[idx] = str(kwargs.get(prop))
                extended_properties = ''.join(temp)

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
    def network_topology_id(self) -> str:
        """Get the unique identifier for the network topology.

        This property provides read-only access to the network topology's unique ID.

        Returns:
            The network topology ID as a string.

        Example:
            >>> topology = NetworkTopology()
            >>> topology_id = topology.network_topology_id  # Access the property
            >>> print(f"Network Topology ID: {topology_id}")

        #ai-gen-doc
        """

        return self._network_topology_id

    @property
    def network_topology_name(self) -> str:
        """Get the name of the network topology as a read-only property.

        Returns:
            The name of the network topology as a string.

        Example:
            >>> topology = NetworkTopology()
            >>> name = topology.network_topology_name  # Access the property
            >>> print(f"Network topology name: {name}")

        #ai-gen-doc
        """

        return self._network_topology_name

    @network_topology_name.setter
    def network_topology_name(self, val: str) -> None:
        """Set the name of the network topology.

        Args:
            val: The new name to assign to the network topology.

        Example:
            >>> topology = NetworkTopology()
            >>> topology.network_topology_name = "CorporateNetwork"  # Use assignment for property setter
            >>> # The network topology name is now set to "CorporateNetwork"
        #ai-gen-doc
        """

        self.update(**{'network_topology_name': val})

    @property
    def description(self) -> str:
        """Get the description of the network topology as a read-only property.

        Returns:
            The description string of the network topology.

        Example:
            >>> topology = NetworkTopology()
            >>> desc = topology.description  # Access the description property
            >>> print(f"Topology description: {desc}")

        #ai-gen-doc
        """

        return self._description

    @description.setter
    def description(self, val: str) -> None:
        """Set the description for the network topology.

        Args:
            val: The description text to assign to the network topology.

        Example:
            >>> topology = NetworkTopology()
            >>> topology.description = "Corporate WAN topology for Q2 2024"
            >>> # The description is now set for the network topology

        #ai-gen-doc
        """
        self.update(**{'description': val})

    @property
    def network_topology_type(self) -> int:
        """Get the network topology type as a read-only attribute.

        Returns:
            The type of the network topology as an integer.

        Example:
            >>> topology = NetworkTopology()
            >>> topology_type = topology.network_topology_type  # Access as a property
            >>> print(f"Network topology type: {topology_type}")

        #ai-gen-doc
        """

        return self._network_topology_type

    @network_topology_type.setter
    def network_topology_type(self, val: int) -> None:
        """Set the network topology type for the NetworkTopology instance.

        Args:
            val: An integer representing the network topology type.
                - 1: Proxy topology
                - 2: One-way topology
                - 3: Two-way topology

        Example:
            >>> topology = NetworkTopology()
            >>> topology.network_topology_type = 2  # Set to one-way topology
            >>> # The network topology type is now set to one-way

        #ai-gen-doc
        """
        self.update(**{'topology_type': val})

    @property
    def extended_properties(self) -> dict:
        """Get the extended properties of the network topology as a read-only attribute.

        Returns:
            dict: A dictionary containing the extended properties associated with the network topology.

        Example:
            >>> topology = NetworkTopology()
            >>> properties = topology.extended_properties
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2'}

        #ai-gen-doc
        """

        return self._extended_properties

    @property
    def firewall_groups(self) -> List['ClientGroup']:
        """Get the list of firewall client groups associated with the network topology as a read-only attribute.

        Returns:
            List of ClientGroup objects representing the firewall groups linked to this network topology.

        Example:
            >>> topology = NetworkTopology()
            >>> groups = topology.firewall_groups  # Access as a property
            >>> for group in groups:
            ...     print(f"Firewall group: {group.name}")
        #ai-gen-doc
        """

        return self._firewall_groups

    @firewall_groups.setter
    def firewall_groups(self, val: list[dict]) -> None:
        """Set the associated client groups for the network topology firewall.

        Args:
            val: A list of dictionaries, each specifying a client group and its type. 
                Each dictionary should have the following keys:
                    - 'group_type' (int): The type of the client group.
                        2: first client group in GUI screen
                        1: second client group in GUI screen
                        3: third client group in GUI screen
                    - 'group_name' (str): The name of the client group.
                    - 'is_mnemonic' (bool): 
                        True if the group is a mnemonic, 
                        False if it is a client group.

                Example input:
                    [
                        {'group_type': 2, 'group_name': "test1", 'is_mnemonic': False},
                        {'group_type': 1, 'group_name': "test2", 'is_mnemonic': False},
                        {'group_type': 3, 'group_name': "test3", 'is_mnemonic': False}
                    ]

        Raises:
            SDKException: If the input value is not a list.

        Example:
            >>> topology = NetworkTopology()
            >>> topology.firewall_groups = [
            ...     {'group_type': 2, 'group_name': "test1", 'is_mnemonic': False},
            ...     {'group_type': 1, 'group_name': "test2", 'is_mnemonic': False},
            ...     {'group_type': 3, 'group_name': "test3", 'is_mnemonic': False}
            ... ]
            >>> # The firewall groups are now set for the topology

        #ai-gen-doc
        """
        if not isinstance(val, list):
            raise SDKException('NetworkTopology', '102',
                               'Client Groups should be a list of dict containing '
                               'group name and group type')

        self.update(val)

    @property
    def wildcard_proxy(self) -> bool:
        """Indicate whether the wildcard proxy option is enabled for the network topology.

        This property provides read-only access to the status of the wildcard proxy setting.

        Returns:
            bool: True if the wildcard proxy option is enabled, False otherwise.

        Example:
            >>> topology = NetworkTopology()
            >>> if topology.wildcard_proxy:
            ...     print("Wildcard proxy is enabled.")
            >>> else:
            ...     print("Wildcard proxy is disabled.")

        #ai-gen-doc
        """

        return self._properties.get('useWildcardProxy', False)

    def push_network_config(self) -> None:
        """Push the network configuration to the network topology.

        This method initiates a push operation to apply the current network configuration
        to the network topology. It is typically used to synchronize or update the network
        settings across the managed environment.

        Raises:
            SDKException: If the push operation fails or if the response indicates an unsuccessful attempt.

        Example:
            >>> topology = NetworkTopology()
            >>> topology.push_network_config()
            >>> print("Network configuration pushed successfully.")

        #ai-gen-doc
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

    def refresh(self) -> None:
        """Reload the properties and state of the NetworkTopology object.

        This method updates the NetworkTopology instance to reflect the latest network configuration
        and topology information. Use this method to ensure that the object contains current data
        after changes have been made to the network.

        Example:
            >>> topology = NetworkTopology()
            >>> topology.refresh()  # Refreshes the network topology properties
            >>> print("Network topology updated successfully")

        #ai-gen-doc
        """

        self._initialize_network_topology_properties()