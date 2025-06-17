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
    """Class for representing backup network pairs operations from commcell"""

    def __init__(self, commcell_object):
        """Initializes object of the BackupNetworkPairs class.

            Args:
               commcell_object (object) -instance of the commcell class

            Returns:
               object - instance of the BackupNetworkPairs class
        """

        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._backup_network_pairs = None
        self._backup_network_pair = self._services['BACKUP_NETWORK_PAIR']
        self._update_response_ = self._commcell_object._update_response_
        self.operation_type = ['ADD', 'DELETE']

    def __repr__(self):
        """Representation string for the instance of BackupNetworkPairs class"""

        return "BackupNetworkPairs class instance for Commcell"

    def get_backup_interface_for_client(self, client_name):
        """Returns interfaces set on a particular client

            Args:
                client_name (str)  --  name of client

            Returns:
                list - list of interfaces with source and destination

            Raises:
                SDKException:
                    if response is not received

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

    def add_backup_interface_pairs(self, interface_pairs):
        """Adds backup interface pairs on clients/client groups

            Args:
                interface_pairs (list)  --  list of tuples containing dict of source and destination

                Example:
                [({'client': 'featuretest', 'srcip': '172.19.96.123'},
                {'client': 'SP9client', 'destip': '172.19.0.0'}),
                ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
                ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'},
                {'clientgroup': 'G3', 'destip': '172.19.0.*'})]

                Note: 0th index should be source with key 'srcip' and 1st index
                should be destination with key 'destip'

                      entities should be passed with key client/clientgroup

            Raises:
                SDKException:
                    if input is not correct

                    if response is not received

        """

        if not isinstance(interface_pairs, list):
            raise SDKException('BackupNetworkPairs', '101',
                               'Interface Pairs should be a list of tuples '
                               'containing dictionary of source and destination')

        self._modify_backup_interface_pairs(interface_pairs, self.operation_type[0])

    def delete_backup_interface_pairs(self, interface_pairs):
        """Deletes backup interface pairs on clients/client groups

            Args:
                interface_pairs (list)  --  list of tuples containing dict of source and destination

                Example:
                [({'client': 'featuretest', 'srcip': '172.19.96.123'},
                {'client': 'SP9client', 'destip': '172.19.0.0'}),
                ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
                ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'},
                {'clientgroup': 'G3', 'destip': '172.19.0.*'})]

                Note: 0th index should be source with key 'srcip' and 1st index
                should be destination with key 'destip'

                      entities should be passed with key client/clientgroup

            Raises:
                SDKException:
                    if input is not correct

                    if response is not received

        """

        if not isinstance(interface_pairs, list):
            raise SDKException('BackupNetworkPairs', '101',
                               'Interface Pairs should be a list of tuples '
                               'containing dictionary of source and destination')

        self._modify_backup_interface_pairs(interface_pairs, self.operation_type[1])

    def _modify_backup_interface_pairs(self, interface_pairs, operation_type):
        """Sets a backup interface pair between clients/client-groups

            Args:
                operation_type  (str)  --  operation type--> add, update, delete

                interface_pairs (list)  --  list of tuples containing dict of source and destination
                                           source and destination can be a combination of
                                           client/client group

                Example:
                [({'client': 'featuretest', 'srcip': '172.19.96.123'},
                {'client': 'SP9client', 'destip': '172.19.0.0'}),
                ({'client': 'featuretest', 'srcip': '172.19.96.123'},
                {'clientgroup': 'G1', 'destip': 'No Default Interface'}),
                ({'clientgroup': 'G2', 'srcip': '172.19.0.0/16'},
                {'clientgroup': 'G3', 'destip': '172.19.0.*'})]

                Note: 0th index should be source with key 'srcip' and 1st index
                should be destination with key 'destip'

                       entities should be passed with key client/clientgroup

            Raises:
                SDKException:
                    if input is not correct

                    if response is not received

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
