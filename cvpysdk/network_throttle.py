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

from .exception import SDKException


class NetworkThrottle(object):
    """Class for performing network throttle related operations on a client or client group"""

    def __init__(self, class_object):
        """Initialize the NetworkThrottle class object

            Args:
                class_object (object)  --  instance of the client/client group class

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

    def _get_throttle_properties(self):
        """Get all the existing network throttle properties on a client/client group
        and retain each of them


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
    def enable_network_throttle(self):
        """Gets the value for enable network throttling

        """
        return self._enable_network_throttling

    @enable_network_throttle.setter
    def enable_network_throttle(self, val):
        """sets the value for enable network throttling

            Args:
                val (boolean) --  value for enable network throttling

        """

        self._enable_network_throttling = val
        self._config_network_throttle()

    @property
    def share_bandwidth(self):
        """Gets the value for share bandwidth

        """
        return self._share_bandwidth

    @share_bandwidth.setter
    def share_bandwidth(self, val):
        """Sets the value for share bandwidth

            Args:
                val (boolean) --  value for share bandwidth

        """

        self._share_bandwidth = val
        self.enable_network_throttle = True

    @property
    def remote_clients(self):
        """Gets the associated client towards which throttling is configured

        """
        clients = []

        for client in self._remote_clients:
            clients.append(client['clientName'])
        return clients

    @remote_clients.setter
    def remote_clients(self, clients):
        """Sets the remote clients towards which throttling will be configured

            Args:
                clients (list) --   list of clients

        """

        for client in clients:
            client_dict = {
                "clientName": client
            }
            self._remote_clients.append(client_dict)

        self.enable_network_throttle = True

    @property
    def remote_client_groups(self):
        """Gets the associated client groups towards which throttling is configured

        """
        client_groups = []

        for client_group in self._remote_client_groups:
            client_groups.append(client_group['clientGroupName'])
        return client_groups

    @remote_client_groups.setter
    def remote_client_groups(self, client_groups):
        """Sets the remote client groups towards which throttling will be configured

            Args:
                client_groups (list) -- list of client groups

        """

        for client_group in client_groups:
            client_group_dict = {
                "clientGroupName": client_group
            }
            self._remote_client_groups.append(client_group_dict)

        self.enable_network_throttle = True

    @property
    def throttle_schedules(self):
        """Gets the throttle rules set on a client or client group

        """
        return self._throttle_schedules

    @throttle_schedules.setter
    def throttle_schedules(self, throttle_rules):
        """Sets different throttle schedules on a client/client group

            Args:
                throttle_rules (list of dict) --  list of throttle rules

            Supported keys:

                "sendRate"
                "sendEnabled"
                "receiveEnabled"
                "recvRate"
                "days"
                "isAbsolute"
                "startTime"
                "endTime"
                "sendRatePercent"
                "recvRatePercent"


            Example:
             [
                {
                    "sendRate": 1024,
                    "sendEnabled": true,
                    "receiveEnabled": true,
                    "recvRate": 1024,
                    "days": '1010101',
                    "isAbsolute": true,
                    "startTime": 0,
                    "endTime": 0,
                    "sendRatePercent": 40,
                    "recvRatePercent": 40
                },

                {
                    "sendRate": 1024,
                    "sendEnabled": True,
                    "receiveEnabled": True,
                    "recvRate": 1024,
                    "days": '1111111',
                    "isAbsolute": False

                }
            ]

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

    def _config_network_throttle(self):
        """Sets network throttle properties on the client/client group


                    Raises:
                        SDKException:
                            if  request was not successful

                            if  invalid input was provided in the request

                            if empty response was received

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
