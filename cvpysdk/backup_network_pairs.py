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

"""Class to perform all the Backup Network Pairs operations on commcell

BackupNetworkPairs is the only class defined in this file.

BackupNetworkPairs: Helper class to perform Backup Network Pairs operations.

BackupNetworkPairs:

    __init__()                          --  initializes BackupNetworkPairs class object.

    __repr__()                          --  returns the string to represent the instance
                                            of the BackupNetworkPairs class

    get_backup_interface_for_client()   --  returns list of interfaces on a client

    add_backup_interface_pairs ()       --  sets backup interface pairs on a client/client group

    delete__backup_interface_pairs()    --  deletes backup interface pairs on a client/client group

    _modify_backup_interface_pairs()    -- modifies backup interface pairs on a client/client group

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from .exception import SDKException


class BackupNetworkPairs(object):
    """
    Manages backup network pairs operations within a CommCell environment.

    This class provides an interface for handling backup network pairs, allowing
    users to retrieve, add, delete, and modify backup interface pairs associated
    with clients in the CommCell system. It is designed to facilitate network
    configuration and management for backup operations.

    Key Features:
        - Retrieve backup interface pairs for a specific client
        - Add new backup interface pairs
        - Delete existing backup interface pairs
        - Modify backup interface pairs with specified operations
        - Integration with CommCell object for seamless operations
        - Provides a string representation for easy inspection

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a BackupNetworkPairs object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> backup_network_pairs = BackupNetworkPairs(commcell)
            >>> print("BackupNetworkPairs object created successfully")

        #ai-gen-doc
        """

        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._backup_network_pairs = None
        self._backup_network_pair = self._services['BACKUP_NETWORK_PAIR']
        self._update_response_ = self._commcell_object._update_response_
        self.operation_type = ['ADD', 'DELETE']

    def __repr__(self) -> str:
        """Return the string representation of the BackupNetworkPairs instance.

        This method provides a developer-friendly string that represents the current
        BackupNetworkPairs object, useful for debugging and logging purposes.

        Returns:
            A string representation of the BackupNetworkPairs instance.

        Example:
            >>> backup_pairs = BackupNetworkPairs()
            >>> print(repr(backup_pairs))
            <BackupNetworkPairs object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """

        return "BackupNetworkPairs class instance for Commcell"

    def get_backup_interface_for_client(self, client_name: str) -> list:
        """Retrieve the list of backup network interfaces configured for a specific client.

        Args:
            client_name: The name of the client for which to fetch backup network interfaces.

        Returns:
            A list of dictionaries, each containing the source and destination interfaces set for the specified client.

        Raises:
            SDKException: If a response is not received from the server.

        Example:
            >>> backup_network_pairs = BackupNetworkPairs()
            >>> interfaces = backup_network_pairs.get_backup_interface_for_client("ClientA")
            >>> print(interfaces)
            [{'source': '192.168.1.10', 'destination': '10.0.0.5'}, ...]

        #ai-gen-doc
        """

        client_id = self._commcell_object.clients.all_clients.get(client_name).get('id')

        self._backup_network_pairs = self._services['BACKUP_NETWORK_PAIRS'] % client_id

        flag, response = self._cvpysdk_object.make_request('GET', self._backup_network_pairs)

        if flag:
            if response.json() and 'ArchPipeLineList' in response.json():
                interface = response.json()['ArchPipeLineList']

            else:
                interface = {}
            return interface

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add_backup_interface_pairs(self, interface_pairs: list[tuple[dict, dict]]) -> None:
        """Add backup interface pairs for clients or client groups.

        This method allows you to specify pairs of source and destination interfaces for backup operations.
        Each pair should be a tuple containing two dictionaries: the first for the source (with 'srcip' and either 'client' or 'clientgroup'),
        and the second for the destination (with 'destip' and either 'client' or 'clientgroup').

        The 0th index of each tuple must be the source with key 'srcip', and the 1st index must be the destination with key 'destip'.
        Entities should be specified using the 'client' or 'clientgroup' key.

        Args:
            interface_pairs: A list of tuples, where each tuple contains two dictionaries representing the source and destination interface.
                Example:
                    [
                        ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                         {'client': 'SP9client', 'destip': '172.19.0.0'}),
                        ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                         {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
                        ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'},
                         {'clientgroup': 'G3', 'destip': '172.19.0.*'})
                    ]

        Raises:
            SDKException: If the input is not correct or if a response is not received.

        Example:
            >>> pairs = [
            ...     ({'client': 'featuretest', 'srcip': '172.19.96.123'}, {'client': 'SP9client', 'destip': '172.19.0.0'}),
            ...     ({'client': 'featuretest', 'srcip': '172.19.96.123'}, {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
            ...     ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'}, {'clientgroup': 'G3', 'destip': '172.19.0.*'})
            ... ]
            >>> backup_network_pairs.add_backup_interface_pairs(pairs)
            >>> print("Backup interface pairs added successfully.")

        #ai-gen-doc
        """

        if not isinstance(interface_pairs, list):
            raise SDKException('BackupNetworkPairs', '101',
                               'Interface Pairs should be a list of tuples '
                               'containing dictionary of source and destination')

        self._modify_backup_interface_pairs(interface_pairs, self.operation_type[0])

    def delete_backup_interface_pairs(self, interface_pairs: list[tuple[dict, dict]]) -> None:
        """Delete backup interface pairs for specified clients or client groups.

        This method removes the specified backup interface pairs from the configuration.
        Each pair should be a tuple of two dictionaries: the first representing the source
        (with keys like 'client' or 'clientgroup' and 'srcip'), and the second representing
        the destination (with keys like 'client', 'clientgroup', and 'destip').

        Args:
            interface_pairs: A list of tuples, where each tuple contains two dictionaries:
                - The first dictionary specifies the source entity and its source IP.
                - The second dictionary specifies the destination entity and its destination IP.
                Example:
                    [
                        ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                         {'client': 'SP9client', 'destip': '172.19.0.0'}),
                        ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                         {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
                        ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'},
                         {'clientgroup': 'G3', 'destip': '172.19.0.*'})
                    ]
                Note:
                    - The first element of each tuple must be the source (with 'srcip').
                    - The second element must be the destination (with 'destip').
                    - Entities should be specified using either 'client' or 'clientgroup' keys.

        Raises:
            SDKException: If the input is not correct or if a response is not received.

        Example:
            >>> pairs = [
            ...     ({'client': 'featuretest', 'srcip': '172.19.96.123'},
            ...      {'client': 'SP9client', 'destip': '172.19.0.0'}),
            ...     ({'client': 'featuretest', 'srcip': '172.19.96.123'},
            ...      {'clientgroup': 'G1', 'destip': 'No Default Interface'})
            ... ]
            >>> backup_network_pairs.delete_backup_interface_pairs(pairs)
            >>> print("Backup interface pairs deleted successfully.")

        #ai-gen-doc
        """

        if not isinstance(interface_pairs, list):
            raise SDKException('BackupNetworkPairs', '101',
                               'Interface Pairs should be a list of tuples '
                               'containing dictionary of source and destination')

        self._modify_backup_interface_pairs(interface_pairs, self.operation_type[1])

    def _modify_backup_interface_pairs(self, interface_pairs: list[tuple[dict[str, str], dict[str, str]]], operation_type: str) -> None:
        """Set, update, or delete backup interface pairs between clients or client groups.

        This method configures backup interface pairs, specifying the source and destination
        network interfaces for data transfer between clients or client groups. Each pair is
        represented as a tuple of two dictionaries: the first for the source (with 'srcip'),
        and the second for the destination (with 'destip'). Entities can be specified using
        either the 'client' or 'clientgroup' key.

        Args:
            interface_pairs: A list of tuples, each containing two dictionaries. The first
                dictionary represents the source (must include 'srcip' and either 'client'
                or 'clientgroup'), and the second represents the destination (must include
                'destip' and either 'client' or 'clientgroup').
                Example:
                    [
                        ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                         {'client': 'SP9client', 'destip': '172.19.0.0'}),
                        ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                         {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
                        ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'},
                         {'clientgroup': 'G3', 'destip': '172.19.0.*'})
                    ]
                Note: The 0th index should be the source with key 'srcip', and the 1st index
                should be the destination with key 'destip'. Entities should be specified
                using 'client' or 'clientgroup'.
            operation_type: The type of operation to perform. Must be one of 'add', 'update', or 'delete'.

        Raises:
            SDKException: If the input is not correct or if a response is not received.

        Example:
            >>> pairs = [
            ...     ({'client': 'featuretest', 'srcip': '172.19.96.123'},
            ...      {'client': 'SP9client', 'destip': '172.19.0.0'}),
            ...     ({'client': 'featuretest', 'srcip': '172.19.96.123'},
            ...      {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
            ...     ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'},
            ...      {'clientgroup': 'G3', 'destip': '172.19.0.*'})
            ... ]
            >>> backup_network_pairs._modify_backup_interface_pairs(pairs, 'add')
            >>> # This will add the specified backup interface pairs

        #ai-gen-doc
        """

        archpipeline_list = []

        for interface_pair in interface_pairs:
            interface_pair_dict = {
                "destGroupId": int(self._commcell_object.client_groups.all_clientgroups.get(
                    interface_pair[1].get('clientgroup', '').lower(), 0)),
                "srcGroupId": int(self._commcell_object.client_groups.all_clientgroups.get(
                    interface_pair[0].get('clientgroup', '').lower(), 0)),
                "isActive": 1,
                "client2": {
                    "name": interface_pair[1]['destip'],
                    "id": int(self._commcell_object.clients.all_clients.get(
                        interface_pair[1].get('client', '').lower(), {}).get('id', 0))
                },
                "client1": {
                    "name": interface_pair[0]['srcip'],
                    "id": int(self._commcell_object.clients.all_clients.get(
                        interface_pair[0].get('client', '').lower(), {}).get('id', 0))
                }
            }

            archpipeline_list.append(interface_pair_dict)

        request_json = {
            "operationType": operation_type,
            "ArchPipeLineList": archpipeline_list
        }

        flag, response = self._cvpysdk_object.make_request('POST',
                                                           self._backup_network_pair,
                                                           request_json)

        if flag:
            if response.json():
                if response.json()['errorCode'] != 0:
                    raise SDKException('BackupNetworkPairs', '101',
                                       "Failed to set network pairs")

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)