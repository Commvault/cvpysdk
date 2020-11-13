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

"""Main file for performing client group operations.

ClientGroups and ClientGroup are the classes defined in this file.

ClientGroups: Class for representing all the client groups associated with a commcell

ClientGroup:  Class for representing a single Client Group of the commcell

ClientGroups:
    __init__(commcell_object)  -- initialise instance of the ClientGroups associated with
    the specified commcell

    __str__()                  -- returns all the client groups associated with the Commcell

    __repr__()                 -- returns the string for the instance of the ClientGroups class

    __len__()                  -- returns the number of client groups associated with the Commcell

    __getitem__()              -- returns the name of the client group for the given client group
    Id or the details for the given client group name

    _get_clientgroups()        -- gets all the clientgroups associated with the commcell specified

    _valid_clients()           -- returns the list of all the valid clients,
    from the list of clients provided

    all_clientgroups()         -- returns the dict of all the clientgroups on the commcell

    has_clientgroup()          -- checks if a client group exists with the given name or not

    create_smart_rule()        -- Create rules required for smart client group creation
    based on input parameters

    merge_smart_rules()        -- Merge multiple rules into (SCG) rule to create smart client group

    _create_scope_dict()       -- Creates Scope Dictionary needed for Smart Client group association

    add(clientgroup_name)      -- adds a new client group to the commcell

    get(clientgroup_name)      -- returns the instance of the ClientGroup class,
    for the the input client group name

    delete(clientgroup_name)   -- deletes the client group from the commcell

    refresh()                  -- refresh the client groups associated with the commcell


ClientGroup:
    __init__(commcell_object,
             clientgroup_name,
             clientgroup_id=None)  -- initialise object of ClientGroup class with the specified
    client group name and id

    __repr__()                     -- return the client group name, the instance is associated with

    _get_clientgroup_id()          -- method to get the clientgroup id, if not specified

    _get_clientgroup_properties()  -- get the properties of this clientgroup

    _initialize_clientgroup_properties() --  initializes the properties of this ClientGroup

    _request_json_()               -- returns the appropriate JSON to pass for enabling/disabling
    an activity

    _process_update_request()      -- processes the clientgroup update API call

    _update()                      -- updates the client group properties

    _add_or_remove_clients()       -- adds/removes clients to/from a ClientGroup

    enable_backup_at_time()        -- enables backup for the client group at the time specified

    enable_backup()                -- enables the backup flag

    disable_backup()               -- disables the backup flag

    enable_restore_at_time()       -- enables restore for the client group at the time specified

    enable_restore()               -- enables the restore flag

    disable_restore()              -- disables the restore flag

    enable_data_aging_at_time()    -- enables data aging for the client group at the time specified

    enable_data_aging()            -- enables the data aging flag

    disable_data_aging()           -- disables the data aging flag

    add_clients()                  -- adds the valid clients to client group

    remove_clients()               -- removes the valid clients from client group

    remove_all_clients()           -- removes all the associated clients from client group

    network()                      -- returns Network class object

    push_network_config()          -- performs a push network configuration on client group

    refresh()                      -- refresh the properties of the client group

    push_servicepack_and_hotfixes() -- triggers installation of service pack and hotfixes

    repair_software()               -- triggers Repair software on the client group

    update_properties()             -- to update the client group properties

    add_additional_setting()        -- adds registry key to client group property

    is_auto_discover_enabled()      -- gets the autodiscover option for the Organization

    enable_auto_discover()          -- enables  autodiscover option at client group level

    disable_auto_discover()         -- disables  autodiscover option at client group level

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import time
import copy

from past.builtins import basestring

from .exception import SDKException
from .network import Network
from .network_throttle import NetworkThrottle
from .deployment.install import Install


class ClientGroups(object):
    """Class for representing all the clientgroups associated with a Commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the ClientGroups class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the ClientGroups class
        """
        self._commcell_object = commcell_object
        self._CLIENTGROUPS = self._commcell_object._services['CLIENTGROUPS']

        self._clientgroups = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all clientgroups of the Commcell.

            Returns:
                str - string of all the clientgroups for a commcell
        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'ClientGroup')

        for index, clientgroup_name in enumerate(self._clientgroups):
            sub_str = '{:^5}\t{:50}\n'.format(index + 1, clientgroup_name)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the ClientGroups class.

            Returns:
                str - string of all the client groups associated with the commcell
        """
        return "ClientGroups class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the client groups associated to the Commcell."""
        return len(self.all_clientgroups)

    def __getitem__(self, value):
        """Returns the name of the client group for the given client group ID or
            the details of the client group for given client group Name.

            Args:
                value   (str / int)     --  Name or ID of the client group

            Returns:
                str     -   name of the client group, if the client group id was given

                dict    -   dict of details of the client group, if client group name was given

            Raises:
                IndexError:
                    no client group exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_clientgroups:
            return self.all_clientgroups[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_clientgroups.items())
                )[0][0]
            except IndexError:
                raise IndexError('No client group exists with the given Name / Id')

    def _get_clientgroups(self):
        """Gets all the clientgroups associated with the commcell

            Returns:
                dict - consists of all clientgroups of the commcell
                    {
                         "clientgroup1_name": clientgroup1_id,
                         "clientgroup2_name": clientgroup2_id,
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._CLIENTGROUPS
        )

        if flag:
            if response.json() and 'groups' in response.json():
                client_groups = response.json()['groups']
                clientgroups_dict = {}

                for client_group in client_groups:
                    temp_name = client_group['name'].lower()
                    temp_id = str(client_group['Id']).lower()
                    clientgroups_dict[temp_name] = temp_id

                return clientgroups_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _valid_clients(self, clients_list):
        """Returns only the valid clients specified in the input clients list

            Args:
                clients_list (list)    --  list of the clients to add to the client group

            Returns:
                list - list consisting of the names of all valid clients in the input clients list

            Raises:
                SDKException:
                    if type of clients list argument is not list
        """
        if not isinstance(clients_list, list):
            raise SDKException('ClientGroup', '101')

        clients = []

        for client in clients_list:
            if isinstance(client, basestring):
                client = client.strip().lower()

                if self._commcell_object.clients.has_client(client):
                    clients.append(client)

        return clients

    @property
    def all_clientgroups(self):
        """Returns dict of all the clientgroups associated with this commcell

            dict - consists of all clientgroups of the commcell
                    {
                         "clientgroup1_name": clientgroup1_id,
                         "clientgroup2_name": clientgroup2_id,
                    }
        """
        return self._clientgroups

    def has_clientgroup(self, clientgroup_name):
        """Checks if a client group exists in the commcell with the input client group name.

            Args:
                clientgroup_name (str)  --  name of the client group

            Returns:
                bool - boolean output whether the client group exists in the commcell or not

            Raises:
                SDKException:
                    if type of the client group name argument is not string
        """
        if not isinstance(clientgroup_name, basestring):
            raise SDKException('ClientGroup', '101')

        return self._clientgroups and clientgroup_name.lower() in self._clientgroups

    def create_smart_rule(self,
                          filter_rule='OS Type',
                          filter_condition='equal to',
                          filter_value='Windows',
                          value='1'):
        """Create/Prepare rules required for smart client group creation based on input parameters

            Args:
                filter_rule (str)      --  Rule selection to match specific criterion

                filter_condition (str) --  Filter value between selections in rule

                filter_value(str)     --   Value of rule criterion

                value(str)            --   value required to create rule

            Returns:
                    dict    -   consists of single rule based on inputs
                {
                    "rule": {
                        "filterID": 100,
                        "secValue": 'Windows',
                        "propID": 8,
                        "propType": 4,
                        "value": '1'
                    }
                }
        """

        filter_dict = {
            'equal to': 100,
            'not equal': 101,
            'any in selection': 108,
            'not in selection': 109,
            'is true': 1,
            'is false': 2,
            'contains': 10,
            }
        prop_id_dict = {
            'Name': 1,
            'Client': 2,
            'Agents Installed': 3,
            'Associated Client Group': 4,
            'Timezone': 5,
            'Hostname': 6,
            'Client Version': 7,
            'OS Type': 8,
            'Package Installed': 9,
            'Client offline (days)': 10,
            'User as client owner': 11,
            'Local user group as client owner': 12,
            'External group as client owner': 13,
            'Associated library name': 14,
            'OS Version': 15,
            'Product Version': 16,
            'Client Version Same as CS Version': 17,
            'Days since client created': 18,
            'Days since last backup': 19,
            'SnapBackup clients': 20,
            'Clients with attached storages': 21,
            'Case manager hold clients': 22,
            'MediaAgents for clients in group': 23,
            'Client acts as proxy': 24,
            'Backup activity enabled': 25,
            'Restore activity enabled': 26,
            'Client online (days)': 27,
            'Inactive AD user as client owner': 28,
            'Client excluded from SLA report': 29,
            'Client uses storage policy': 30,
            'Client is not ready': 31,
            'Associated Storage Policy': 32,
            'MediaAgent has Lucene Index Roles': 33,
            'Client associated with plan': 34,
            'Client by Schedule Interval': 35,
            'Client needs Updates': 36,
            'Subclient Name': 37,
            'CommCell Psuedo Client': 38,
            'Client Description': 39,
            'Clients discovered using VSA Subclient': 40,
            'Clients with no Archive Data': 41,
            'User Client Provider Associations': 42,
            'User Group Client Provider Associations': 43,
            'Company Client Provider Associations': 44,
            'Clients Meet SLA': 45,
            'Index Servers': 46,
            'Clients with OnePass enabled': 49,
            'Clients by Role': 50,
            'Clients by Permission': 51,
            'User description contains': 52,
            'User Group description contains': 53,
            'Content Analyzer Cloud': 54,
            'Company Installed Client Associations': 55,
            'Client Online in Last 30 Days': 56,
            'Clients With Subclients Having Associated Storage Policy': 60,
            'Clients With Improperly Deconfigured Subclients': 61,
            'Strikes count': 62,
            'Clients With Backup Schedule': 63,
            'Clients With Long Running Jobs': 64,
            'Clients With Synthetic Full Backup N Days': 67,
            'MediaAgents for clients in group list': 70,
            'Associated Client Group List': 71,
            'Timezone List': 72,
            'MediaAgent has Lucene Index Role List': 73,
            'Associated Storage Policy List': 74,
            'Timezone Region List': 75,
            'Clients With Encryption': 80,
            'Client CIDR Address Range': 81,
            'HAC Cluster': 85,
            }
        ptype_dict = {
            'Name': 2,
            'Client': 4,
            'Agents Installed': 6,
            'Associated Client Group': 4,
            'Timezone': 4,
            'Hostname': 2,
            'Client Version': 4,
            'OS Type': 4,
            'Package Installed': 6,
            'Client offline (days)': 3,
            'User as client owner': 2,
            'Local user group as client owner': 2,
            'External group as client owner': 2,
            'Associated library name': 2,
            'OS Version': 2,
            'Product Version': 2,
            'Client Version Same as CS Version': 1,
            'Days since client created': 3,
            'Days since last backup': 3,
            'SnapBackup clients': 1,
            'Clients with attached storages': 1,
            'Case manager hold clients': 1,
            'MediaAgents for clients in group': 2,
            'Client acts as proxy': 1,
            'Backup activity enabled': 1,
            'Restore activity enabled': 1,
            'Client online (days)': 3,
            'Inactive AD user as client owner': 1,
            'Client excluded from SLA report': 1,
            'Client uses storage policy': 2,
            'Client is not ready': 1,
            'Associated Storage Policy': 4,
            'MediaAgent has Lucene Index Roles': 4,
            'Client associated with plan': 2,
            'Client by Schedule Interval': 4,
            'Client needs Updates': 1,
            'Subclient Name': 2,
            'CommCell Psuedo Client': 1,
            'Client Description': 2,
            'Clients discovered using VSA Subclient': 6,
            'Clients with no Archive Data': 1,
            'User Client Provider Associations': 2,
            'User Group Client Provider Associations': 2,
            'Company Client Provider Associations': 4,
            'Clients Meet SLA': 4,
            'Index Servers': 1,
            'Clients with OnePass enabled': 1,
            'Clients by Role': 4,
            'Clients by Permission': 4,
            'User description contains': 2,
            'User Group description contains': 2,
            'Content Analyzer Cloud': 1,
            'Company Installed Client Associations': 4,
            'Client Online in Last 30 Days': 1,
            'Clients With Subclients Having Associated Storage Policy': 1,
            'Clients With Improperly Deconfigured Subclients': 1,
            'Strikes count': 3,
            'Clients With Backup Schedule': 1,
            'Clients With Long Running Jobs': 3,
            'Clients With Synthetic Full Backup N Days': 3,
            'MediaAgents for clients in group list': 7,
            'Associated Client Group List': 7,
            'Timezone List': 7,
            'MediaAgent has Lucene Index Role List': 7,
            'Associated Storage Policy List': 7,
            'Timezone Region List': 7,
            'Clients With Encryption': 1,
            'Client CIDR Address Range': 10,
            'HAC Cluster': 1,
            }

        rule_mk = {
            "rule": {
                "filterID": filter_dict[filter_condition],
                "secValue": filter_value,
                "propID": prop_id_dict[filter_rule],
                "propType": ptype_dict[filter_rule],
                "value": value
            }
            }

        return rule_mk

    def merge_smart_rules(self, rule_list, op_value='all', scg_op='all'):
        """Merge multiple rules into (SCG) rule to create smart client group.

            Args:
                rule_list (list)  --  List of smart rules to be added in rule group

                op_value (str)--     condition to apply between smart rules
                ex: all, any,not any

                scg_op (str)--       condition to apply between smart rule groups (@group level)

            Returns:
               scg_rule (dict)    -   Rule group to create smart client group

        """

        op_dict = {
            'all': 0,
            'any': 1,
            'not any': 2
        }
        scg_rule = {
            "op": op_dict[scg_op],
            "rules": [
            ]
        }
        rules_dict = {
            "rule": {
                "op": op_dict[op_value],
                "rules": [
                ]
            }
        }

        for each_rule in rule_list:
            rules_dict["rule"]["rules"].append(each_rule)

        scg_rule["rules"].append(rules_dict)
        return scg_rule

    def _create_scope_dict(self, client_scope, value=None):
        """Creates required dictionary for given client scope

            Args:
                value (string)  --  Value to be selected for the client scope dropdown
                client_scope (string) -- Value of the client scope

            Accepted Values (client_scope) --
                Clients in this Commcell
                Clients of Companies
                Clients of User
                Clients of User Groups

            Returns:
                dictionary - Client Scope data required for the smart client group

            NOTE : Value is not required for client scope = "Clients in this Commcell"
            For this, value is automatically set to the Commserve Name
        """
        scgscope = {
            "entity": {}
        }
        if client_scope.lower() == 'clients in this commcell':
            scgscope["entity"] = {
                "commCellName": self._commcell_object.commserv_name,
                "_type_": 1
            }
        elif client_scope.lower() == 'clients of companies' and value is not None:
            scgscope["entity"] = {
                "providerDomainName": value,
                "_type_": 61
            }
        elif client_scope.lower() == 'clients of user' and value is not None:
            scgscope["entity"] = {
                "userName": value,
                "_type_": 13
            }
        elif client_scope.lower() == 'clients of user group' and value is not None:
            scgscope["entity"] = {
                "userGroupName": value,
                "_type_": 15
            }
        return scgscope

    def add(self, clientgroup_name, clients=[], **kwargs):
        """Adds a new Client Group to the Commcell.

            Args:
                clientgroup_name        (str)        --  name of the new client group to add

                clients                 (str/list)   --  ',' separated string of client names,
                                                             or a list of clients,
                                                             to be added under client group
                                                            default: []

                ** kwargs               (dict)       -- Key value pairs for supported arguments

                Supported:

                    clientgroup_description (str)        --  description of the client group
                                                                default: ""

                    enable_backup           (bool)       --  enable or disable backup
                                                                default: True

                    enable_restore          (bool)       --  enable or disable restore
                                                                default: True

                    enable_data_aging       (bool)       --  enable or disable data aging
                                                                default: True
                    scg_rule                (dict)       --  scg_rule required to create smart
                                                                client group

                    client_scope            (str)        --  Client scope for the Smart Client Group

                    client_scope_value      (str)        --  Client scope value for a particular scope

            Returns:
                object - instance of the ClientGroup class created by this method

            Raises:
                SDKException:
                    if type of client group name and description is not of type string

                    if clients argument is not of type list / string

                    if response is empty

                    if response is not success

                    if client group already exists with the given name
        """
        if not (isinstance(clientgroup_name, basestring) and
                isinstance(kwargs.get('clientgroup_description', ''), basestring)):
            raise SDKException('ClientGroup', '101')

        if not self.has_clientgroup(clientgroup_name):
            if isinstance(clients, list):
                clients = self._valid_clients(clients)
            elif isinstance(clients, basestring):
                clients = self._valid_clients(clients.split(','))
            else:
                raise SDKException('ClientGroup', '101')

            clients_list = []

            for client in clients:
                clients_list.append({'clientName': client})

            smart_client_group = bool(kwargs.get('scg_rule'))
            if kwargs.get('scg_rule') is None:
                kwargs['scg_rule'] = {}

            request_json = {
                "clientGroupOperationType": 1,
                "clientGroupDetail": {
                    "description": kwargs.get('clientgroup_description', ''),
                    "isSmartClientGroup": smart_client_group,
                    "scgRule": kwargs.get('scg_rule'),
                    "clientGroup": {
                        "clientGroupName": clientgroup_name
                    },
                    "associatedClients": clients_list
                }
            }

            scg_scope = None
            if kwargs.get("client_scope") is not None:
                # Check if value is there or not
                if kwargs.get("client_scope").lower() == "clients in this commcell":
                    scg_scope = [self._create_scope_dict(kwargs.get("client_scope"))]
                else:
                    if kwargs.get("client_scope_value") is not None:
                        scg_scope = [self._create_scope_dict(kwargs.get("client_scope"), kwargs.get("client_scope_value"))]
                    else:
                        raise SDKException('ClientGroup', '102',
                                           "Client Scope {0} requires a value".format(kwargs.get("client_scope")))

            if scg_scope is not None:
                request_json["clientGroupDetail"]["scgScope"] = scg_scope

            if kwargs.get("enable_backup") or kwargs.get("enable_data_aging") or kwargs.get("enable_restore"):
                client_group_activity_control = {
                        "activityControlOptions": [
                            {
                                "activityType": 1,
                                "enableAfterADelay": False,
                                "enableActivityType": kwargs.get('enable_backup', True)
                            }, {
                                "activityType": 16,
                                "enableAfterADelay": False,
                                "enableActivityType": kwargs.get('enable_data_aging', True)
                            }, {
                                "activityType": 2,
                                "enableAfterADelay": False,
                                "enableActivityType": kwargs.get('enable_restore', True)
                            }
                        ]
                    }
                request_json["clientGroupDetail"]["clientGroupActivityControl"] = client_group_activity_control

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._CLIENTGROUPS, request_json
            )

            if flag:
                if response.json():
                    error_message = None

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to create new ClientGroup\nError:"{0}"'.format(
                            error_message
                        )
                        raise SDKException('ClientGroup', '102', o_str)
                    elif 'clientGroupDetail' in response.json():
                        self.refresh()
                        clientgroup_id = response.json()['clientGroupDetail'][
                            'clientGroup']['clientGroupId']

                        return ClientGroup(
                            self._commcell_object, clientgroup_name, clientgroup_id
                        )
                    else:
                        o_str = 'Failed to create new ClientGroup'
                        raise SDKException('ClientGroup', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'ClientGroup', '102', 'Client Group "{0}" already exists.'.format(clientgroup_name)
            )

    def get(self, clientgroup_name):
        """Returns a client group object of the specified client group name.

            Args:
                clientgroup_name (str)  --  name of the client group

            Returns:
                object - instance of the ClientGroup class for the given clientgroup name

            Raises:
                SDKException:
                    if type of the client group name argument is not string

                    if no client group exists with the given name
        """
        if not isinstance(clientgroup_name, basestring):
            raise SDKException('ClientGroup', '101')
        else:
            clientgroup_name = clientgroup_name.lower()

            if self.has_clientgroup(clientgroup_name):
                return ClientGroup(
                    self._commcell_object, clientgroup_name, self._clientgroups[clientgroup_name]
                )

            raise SDKException(
                'ClientGroup',
                '102',
                'No ClientGroup exists with name: {0}'.format(clientgroup_name)
            )

    def delete(self, clientgroup_name):
        """Deletes the clientgroup from the commcell.

            Args:
                clientgroup_name (str)  --  name of the clientgroup

            Raises:
                SDKException:
                    if type of the clientgroup name argument is not string

                    if response is empty

                    if failed to delete the client group

                    if no clientgroup exists with the given name
        """

        if not isinstance(clientgroup_name, basestring):
            raise SDKException('ClientGroup', '101')
        else:
            clientgroup_name = clientgroup_name.lower()

            if self.has_clientgroup(clientgroup_name):
                clientgroup_id = self._clientgroups[clientgroup_name]

                delete_clientgroup_service = self._commcell_object._services['CLIENTGROUP']

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'DELETE', delete_clientgroup_service % clientgroup_id
                )

                if flag:
                    if response.json():
                        if 'errorCode' in response.json():
                            error_code = str(response.json()['errorCode'])
                            error_message = response.json()['errorMessage']

                            if error_code == '0':
                                # initialize the clientgroups again
                                # so the clientgroups object has all the client groups
                                self.refresh()
                            else:
                                o_str = 'Failed to delete ClientGroup\nError: "{0}"'.format(
                                    error_message
                                )
                                raise SDKException('ClientGroup', '102', o_str)
                        else:
                            raise SDKException('Response', '102')
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'ClientGroup',
                    '102',
                    'No ClientGroup exists with name: "{0}"'.format(clientgroup_name)
                )

    def refresh(self):
        """Refresh the client groups associated with the Commcell."""
        self._clientgroups = self._get_clientgroups()


class ClientGroup(object):
    """Class for performing operations for a specific ClientGroup."""

    def __init__(self, commcell_object, clientgroup_name, clientgroup_id=None):
        """Initialise the ClientGroup class instance.

            Args:
                commcell_object     (object)   --  instance of the Commcell class

                clientgroup_name    (str)      --  name of the clientgroup

                clientgroup_id      (str)      --  id of the clientgroup
                    default: None

            Returns:
                object - instance of the ClientGroup class
        """
        self._commcell_object = commcell_object

        self._clientgroup_name = clientgroup_name.lower()

        if clientgroup_id:
            # Use the client group id provided in the arguments
            self._clientgroup_id = str(clientgroup_id)
        else:
            # Get the id associated with this client group
            self._clientgroup_id = self._get_clientgroup_id()

        self._CLIENTGROUP = self._commcell_object._services['CLIENTGROUP'] % (self.clientgroup_id)

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._properties = None
        self._description = None
        self._is_backup_enabled = None
        self._is_restore_enabled = None
        self._is_data_aging_enabled = None

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string containing the details of this ClientGroup
        """
        representation_string = 'ClientGroup class instance for ClientGroup: "{0}"'
        return representation_string.format(self.clientgroup_name)

    def _get_clientgroup_id(self):
        """Gets the clientgroup id associated with this clientgroup.

            Returns:
                str - id associated with this clientgroup
        """
        clientgroups = ClientGroups(self._commcell_object)
        return clientgroups.get(self.clientgroup_name).clientgroup_id

    def _get_clientgroup_properties(self):
        """Gets the clientgroup properties of this clientgroup.

            Returns:
                dict - dictionary consisting of the properties of this clientgroup

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._CLIENTGROUP
        )

        if flag:
            if response.json() and 'clientGroupDetail' in response.json():
                return response.json()['clientGroupDetail']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_clientgroup_properties(self):
        """Initializes the common properties for the clientgroup."""
        clientgroup_props = self._get_clientgroup_properties()
        self._properties = clientgroup_props

        if 'clientGroupName' in clientgroup_props['clientGroup']:
            self._clientgroup_name = clientgroup_props['clientGroup']['clientGroupName'].lower()
        else:
            raise SDKException(
                'ClientGroup', '102', 'Client Group name is not specified in the response'
            )

        self._description = None

        if 'description' in clientgroup_props:
            self._description = clientgroup_props['description']

        self._associated_clients = []

        if 'associatedClients' in clientgroup_props:
            for client in clientgroup_props['associatedClients']:
                self._associated_clients.append(client['clientName'])

        self._is_backup_enabled = False
        self._is_restore_enabled = False
        self._is_data_aging_enabled = False

        if 'clientGroupActivityControl' in clientgroup_props:
            cg_activity_control = clientgroup_props['clientGroupActivityControl']

            if 'activityControlOptions' in cg_activity_control:
                for control_options in cg_activity_control['activityControlOptions']:
                    if control_options['activityType'] == 1:
                        self._is_backup_enabled = control_options['enableActivityType']
                    elif control_options['activityType'] == 2:
                        self._is_restore_enabled = control_options['enableActivityType']
                    elif control_options['activityType'] == 16:
                        self._is_data_aging_enabled = control_options['enableActivityType']

    def _request_json_(self, option, enable=True, enable_time=None, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                option (str)  --  string option for which to run the API for
                    e.g.; Backup / Restore / Data Aging

                **kwargs (dict)  -- dict of keyword arguments as follows

                    timezone    (str)   -- timezone to be used of the operation

                        **Note** make use of TIMEZONES dict in constants.py to pass timezone

                        **Note** In case of linux CommServer provide time in GMT timezone

            Returns:
                dict - JSON request to pass to the API
        """
        options_dict = {
            "Backup": 1,
            "Restore": 2,
            "Data Aging": 16
        }

        request_json1 = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "clientGroupActivityControl": {
                    "activityControlOptions": [{
                        "activityType": options_dict[option],
                        "enableAfterADelay": False,
                        "enableActivityType": enable
                    }]
                },
                "clientGroup": {
                    "newName": self.name
                }
            }
        }

        request_json2 = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "clientGroupActivityControl": {
                    "activityControlOptions": [{
                        "activityType": options_dict[option],
                        "enableAfterADelay": True,
                        "enableActivityType": False,
                        "dateTime": {
                            "TimeZoneName": kwargs.get("timezone", self._commcell_object.default_timezone),
                            "timeValue": enable_time
                        }
                    }]
                },
                "clientGroup": {
                    "newName": self.name
                }
            }
        }

        if enable_time:
            return request_json2
        else:
            return request_json1

    def _process_update_request(self, request_json):
        """Runs the Clientgroup update API

            Args:
                request_json    (dict)  -- request json sent as payload

            Returns:
                (str, str):
                    str  -  error code received in the response

                    str  -  error message received in the response

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLIENTGROUP, request_json
        )

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']
                else:
                    error_message = ""

                self.refresh()
                return error_code, error_message
            raise SDKException('Response', '102')
        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _update(
            self,
            clientgroup_name,
            clientgroup_description,
            associated_clients=None,
            operation_type="NONE"):
        """Update the clientgroup properties of this clientgroup.

            Args:
                clientgroup_name        (str)       --  new name of the clientgroup

                clientgroup_description (str)       --  description for the clientgroup

                associated_clients      (str/list)  --  ',' separated string of client names,
                                                            or a list of clients,
                                                            to be added/removed under client group
                    default: None

                operation_type          (str)       --  associated clients operation type
                        Valid values: NONE, OVERWRITE, ADD, DELETE, CLEAR
                    default: NONE

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        clients_list = []

        associated_clients_op_types = {
            "NONE": 0,
            "OVERWRITE": 1,
            "ADD": 2,
            "DELETE": 3,
            "CLEAR": 4
        }

        for client in associated_clients:
            clients_list.append({'clientName': client})

        request_json = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "description": clientgroup_description,
                "clientGroup": {
                    "newName": clientgroup_name
                },
                "associatedClientsOperationType": associated_clients_op_types[operation_type],
                "associatedClients": clients_list
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENTGROUP, request_json
        )

        self.refresh()

        if flag:
            if response.json():

                error_message = response.json()['errorMessage']
                error_code = str(response.json()['errorCode'])

                if error_code == '0':
                    return (True, "0", "")
                else:
                    return (False, error_code, error_message)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _add_or_remove_clients(self, clients, operation_type):
        """Adds/Removes clients to/from the ClientGroup.

        Args:
                clients         (str/list)   --  ',' separated string of client names,
                                                     or a list of clients,
                                                     to be added under client group

                operation_type  (bool)       --  type of operation to run for the request
                    ADD / OVERWRITE / DELETE

            Raises:
                SDKException:
                    if clients is not of type string / list

                    if no valid clients are found

                    if failed to add clients to ClientGroup

                                    OR

                    if failed to remove clients from the ClientGroup
        """
        if isinstance(clients, (basestring, list)):
            clientgroups_object = ClientGroups(self._commcell_object)

            if isinstance(clients, list):
                validated_clients_list = clientgroups_object._valid_clients(clients)
            elif isinstance(clients, basestring):
                validated_clients_list = clientgroups_object._valid_clients(clients.split(','))

            if operation_type in ['ADD', 'OVERWRITE']:
                for client in validated_clients_list:
                    if client in self._associated_clients:
                        validated_clients_list.remove(client)

            if not validated_clients_list:
                raise SDKException('ClientGroup', '102', 'No valid clients were found')

            output = self._update(
                clientgroup_name=self.name,
                clientgroup_description=self.description,
                associated_clients=validated_clients_list,
                operation_type=operation_type
            )

            exception_message_dict = {
                'ADD': 'Failed to add clients to the ClientGroup\nError: "{0}"',
                'OVERWRITE': 'Failed to add clients to the ClientGroup\nError: "{0}"',
                'DELETE': 'Failed to remove clients from the ClientGroup\nError: "{0}"'
            }

            if output[0]:
                return
            else:
                o_str = exception_message_dict[operation_type]
                raise SDKException('ClientGroup', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'ClientGroup', '102', 'Client\'s name should be a list or string value'
            )

    @property
    def properties(self):
        """Returns the client group properties"""
        return copy.deepcopy(self._properties)

    @property
    def name(self):
        """Returns the client group display name"""
        return self._properties['clientGroup']['clientGroupName']

    @property
    def clientgroup_id(self):
        """Treats the clientgroup id as a read-only attribute."""
        return self._clientgroup_id

    @property
    def clientgroup_name(self):
        """Treats the clientgroup name as a read-only attribute."""
        return self._clientgroup_name

    @property
    def description(self):
        """Treats the clientgroup description as a read-only attribute."""
        return self._description

    @property
    def associated_clients(self):
        """Treats the clients associated to the ClientGroup as a read-only attribute."""
        return self._associated_clients

    @property
    def is_backup_enabled(self):
        """Treats the clientgroup backup attribute as a property of the ClientGroup class."""
        return self._is_backup_enabled

    @property
    def is_restore_enabled(self):
        """Treats the clientgroup restore attribute as a propetry of the ClientGroup class."""
        return self._is_restore_enabled

    @property
    def is_data_aging_enabled(self):
        """Treats the clientgroup data aging attribute as a property of the ClientGroup class."""
        return self._is_data_aging_enabled

    @property
    def network(self):
        """Returns the object of Network class."""
        if self._networkprop is None:
            self._networkprop = Network(self)

        return self._networkprop

    @property
    def network_throttle(self):
        """Returns the object of NetworkThrottle class"""
        if self._network_throttle is None:
            self._network_throttle = NetworkThrottle(self)

        return self._network_throttle

    @property
    def client_group_filter(self):
        """Returns the client group filters"""
        client_group_filters = {}

        os_type_map = {
            1: 'windows_filters',
            2: 'unix_filters'
        }

        for filters_root in self._properties['globalFiltersInfo']['globalFiltersInfoList']:
            client_group_filters[os_type_map[filters_root['operatingSystemType']]] = filters_root.get(
                'globalFilters', {}).get('filters', [])

        return client_group_filters

    @property
    def is_auto_discover_enabled(self):
        """Returns boolen for clientgroup autodiscover attribute whether property is enabled or not."""
        return self._properties.get('enableAutoDiscovery', False)

    @client_group_filter.setter
    def client_group_filter(self, filters):
        """""Sets the specified server group filters"""
        request_json = {}
        request_json['clientGroupDetail'] = self._properties
        filters_root = request_json['clientGroupDetail']['globalFiltersInfo']['globalFiltersInfoList']

        for var in filters_root:
            if var['operatingSystemType'] == 1:
                var['globalFilters'] = {
                    'filters': filters.get('windows_filters', var['globalFilters'].get(
                        'filters', []))
                }
            if var['operatingSystemType'] == 2:
                var['globalFilters'] = {
                    'filters': filters.get('unix_filters', var['globalFilters'].get(
                        'filters', []))
                }
            var['globalFilters']['opType'] = 1
        request_json['clientGroupOperationType'] = 2

        self._process_update_request(request_json)
        self.refresh()

    def enable_backup(self):
        """Enable Backup for this ClientGroup.

            Raises:
                SDKException:
                    if failed to enable backup
        """
        request_json = self._request_json_('Backup')

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_backup_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Backup'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_backup_at_time(self, enable_time, **kwargs):
        """Disables Backup if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

                **kwargs (dict)  -- dict of keyword arguments as follows

                    timezone    (str)   -- timezone to be used of the operation

                        **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable backup
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('ClientGroup', '103')
        except ValueError:
            raise SDKException('ClientGroup', '104')

        request_json = self._request_json_('Backup', False, enable_time, **kwargs)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            return
        else:
            if error_message:
                o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Backup'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_backup(self):
        """Disables Backup for this ClientGroup.

            Raises:
                SDKException:
                    if failed to disable backup
        """
        request_json = self._request_json_('Backup', False)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_backup_enabled = False
            return
        else:
            if error_message:
                o_str = 'Failed to disable Backup\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to diable Backup'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_restore(self):
        """Enable Restore for this ClientGroup.

            Raises:
                SDKException:
                    if failed to enable restore
        """
        request_json = self._request_json_('Restore')

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_restore_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Restore'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_restore_at_time(self, enable_time, **kwargs):
        """Disables restore if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

                **kwargs (dict)  -- dict of keyword arguments as follows

                    timezone    (str)   -- timezone to be used of the operation

                        **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable Restore
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('ClientGroup', '103')
        except ValueError:
            raise SDKException('ClientGroup', '104')

        request_json = self._request_json_('Restore', False, enable_time, **kwargs)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            return
        else:
            if error_message:
                o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Restore'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_restore(self):
        """Disables Restore for this ClientGroup.

            Raises:
                SDKException:
                    if failed to disable restore
        """
        request_json = self._request_json_('Restore', False)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_restore_enabled = False
            return
        else:
            if error_message:
                o_str = 'Failed to disable Restore\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to disable Restore'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_data_aging(self):
        """Enable Data Aging for this ClientGroup.

            Raises:
                SDKException:
                    if failed to enable data aging
        """
        request_json = self._request_json_('Data Aging')

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_data_aging_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Data Aging\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Data Aging'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_data_aging_at_time(self, enable_time, **kwargs):
        """Disables Data Aging if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

                **kwargs (dict)  -- dict of keyword arguments as follows

                    timezone    (str)   -- timezone to be used of the operation

                        **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable Data Aging
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('ClientGroup', '103')
        except ValueError:
            raise SDKException('ClientGroup', '104')

        request_json = self._request_json_('Data Aging', False, enable_time, **kwargs)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            return
        else:
            if error_message:
                o_str = 'Failed to enable Data Aging\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Data Aging'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_data_aging(self):
        """Disables Data Aging for this ClientGroup.

            Raises:
                SDKException:
                    if failed to disable data aging
        """
        request_json = self._request_json_('Data Aging', False)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_data_aging_enabled = False
            return
        else:
            if error_message:
                o_str = 'Failed to disable Data Aging\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to disable Data Aging'

            raise SDKException('ClientGroup', '102', o_str)

    @clientgroup_name.setter
    def clientgroup_name(self, value):
        """Sets the name of the clientgroup as the value provided as input."""
        if isinstance(value, basestring):
            output = self._update(
                clientgroup_name=value,
                clientgroup_description=self.description,
                associated_clients=self._associated_clients
            )

            if output[0]:
                return
            else:
                o_str = 'Failed to update the ClientGroup name\nError: "{0}"'
                raise SDKException('ClientGroup', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'ClientGroup', '102', 'Clientgroup name should be a string value'
            )

    @description.setter
    def description(self, value):
        """Sets the description of the clientgroup as the value provided in input."""
        if isinstance(value, basestring):
            output = self._update(
                clientgroup_name=self.name,
                clientgroup_description=value,
                associated_clients=self._associated_clients
            )

            if output[0]:
                return
            else:
                o_str = 'Failed to update the ClientGroup description\nError: "{0}"'
                raise SDKException('ClientGroup', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'ClientGroup', '102', 'Clientgroup description should be a string value'
            )

    def add_clients(self, clients, overwrite=False):
        """Adds clients to the ClientGroup.

        Args:
                clients     (str/list)  --  ',' separated string of client names,
                                                or a list of clients,
                                                to be added under client group

                overwrite   (bool)      --  if set to true will remove old clients,
                                                and add new clients
                    default: False

            Raises:
                SDKException:
                    if clients is not of type string / list

                    if no valid clients are found

                    if failed to add clients to client group
        """
        if overwrite is True:
            return self._add_or_remove_clients(clients, 'OVERWRITE')
        else:
            return self._add_or_remove_clients(clients, 'ADD')

    def remove_clients(self, clients):
        """Deletes clients from the ClientGroup.

            Args:
                clients     (str/list)  --  ',' separated string of client names,
                                                or a list of clients,
                                                to be removed from the client group

            Raises:
                SDKException:
                    if clients is not of type string / list

                    if no valid clients are found

                    if failed to remove clients from client group
        """
        return self._add_or_remove_clients(clients, 'DELETE')

    def remove_all_clients(self):
        """Clears the associated clients from client group

            Raises:
                SDKException:
                    if failed to remove all clients from client group
        """
        output = self._update(
            clientgroup_name=self.name,
            clientgroup_description=self.description,
            associated_clients=self._associated_clients,
            operation_type="CLEAR"
        )

        if output[0]:
            return
        else:
            o_str = 'Failed to remove clients from the ClientGroup\nError: "{0}"'
            raise SDKException('ClientGroup', '102', o_str.format(output[2]))

    def push_network_config(self):
        """Performs a push network configuration on the client group

                Raises:
                SDKException:
                    if input data is invalid

                    if response is empty

                    if response is not success
        """

        xml_execute_command = """
                        <App_PushFirewallConfigurationRequest>
                        <entity clientGroupName="{0}"/>
                        </App_PushFirewallConfigurationRequest>
            """.format(self.clientgroup_name)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], xml_execute_command
        )

        if flag:
            if response.json():
                error_code = -1
                error_message = ""
                if 'entityResponse' in response.json():
                    error_code = response.json()['entityResponse'][0]['errorCode']

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']

                elif 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']

                    if 'errorCode' in response.json():
                        error_code = response.json()['errorCode']

                if error_code != 0:
                    raise SDKException('ClientGroup', '102', error_message)

            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def push_servicepack_and_hotfix(
            self,
            reboot_client=False,
            run_db_maintenance=True):
        """triggers installation of service pack and hotfixes

        Args:
            reboot_client (bool)            -- boolean to specify whether to reboot the client
            or not

                default: False

            run_db_maintenance (bool)      -- boolean to specify whether to run db
            maintenance not

                default: True

        Returns:
            object - instance of the Job class for this download job

        Raises:
                SDKException:
                    if Download job failed

                    if response is empty

                    if response is not success

                    if another download job is already running

        **NOTE:** push_serivcepack_and_hotfixes cannot be used for revision upgrades

        """
        install = Install(self._commcell_object)
        return install.push_servicepack_and_hotfix(
            client_computer_groups=[self.name],
            reboot_client=reboot_client,
            run_db_maintenance=run_db_maintenance)

    def repair_software(
            self,
            username=None,
            password=None,
            reboot_client=False):
        """triggers Repair software on the client group

        Args:
             username    (str)               -- username of the machine to re-install features on

                default : None

            password    (str)               -- base64 encoded password

                default : None

            reboot_client (bool)            -- boolean to specify whether to reboot the
                                                client_group or not

                default: False

        Returns:
            object - instance of the Job class for this download job

        Raises:
                SDKException:
                if install job failed

                if response is empty

                if response is not success

        """
        install = Install(self._commcell_object)
        return install.repair_software(
            client_group=self.name,
            username=username,
            password=password,
            reboot_client=reboot_client
        )

    def update_properties(self, properties_dict):
        """Updates the client group properties

            Args:
                properties_dict (dict)  --  client group property dict which is to be updated

            Returns:
                None

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected

        **Note** self.properties can be used to get a deep copy of all the properties, modify the properties which you
        need to change and use the update_properties method to set the properties

        """
        request_json = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "clientGroup": {
                    "clientGroupName": self.name
                }
            }
        }

        request_json['clientGroupDetail'].update(properties_dict)
        error_code, error_message = self._process_update_request(request_json)

        if error_code != '0':
            raise SDKException(
                'ClientGroup', '102', 'Failed to update client group property\nError: "{0}"'.format(error_message)
            )

    def add_additional_setting(
            self,
            category=None,
            key_name=None,
            data_type=None,
            value=None,
            comment=None,
            enabled=1):
        """Adds registry key to the client group property

            Args:
                category        (str)           -- Category of registry key

                key_name        (str)           -- Name of the registry key

                data_type       (str)           -- Data type of registry key

                    Accepted Values: BOOLEAN, INTEGER, STRING, MULTISTRING, ENCRYPTED

                value           (str)           -- Value of registry key

                comment         (str)           -- Comment to be added for the additional setting

                enabled         (int)           -- To enable the additional setting
                                                    default: 1

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected"""

        properties_dict = {
            "registryKeys": [{"deleted": 0,
                              "hidden": False,
                              "relativepath": category,
                              "keyName": key_name,
                              "isInheritedFromClientGroup": False,
                              "comment": comment,
                              "type": data_type,
                              "value": value,
                              "enabled": enabled}]
        }

        self.update_properties(properties_dict)

    def enable_auto_discover(self):
        """Enables autodiscover at ClientGroup level..

            Raises:
                SDKException:
                    if failed to enable_auto_discover
        """
        request_json = {
            "clientGroupOperationType": 2,
            'clientGroupDetail': {
                    'enableAutoDiscovery': True,
                    "clientGroup": {
                            "clientGroupName": self.clientgroup_name
            }
        }
        }
        error_code, error_message = self._process_update_request(request_json)
        if error_code != '0':
            if error_message:
                o_str = 'Failed to enable autodiscover \nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable autodiscover'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_auto_discover(self):
        """Disables autodiscover at ClientGroup level..

            Raises:
                SDKException:
                    if failed to disable_auto_discover
        """
        request_json = {
            "clientGroupOperationType": 2,
            'clientGroupDetail': {
                    'enableAutoDiscovery': False,
                    "clientGroup": {
                            "clientGroupName": self.clientgroup_name
            }
        }
        }
        error_code, error_message = self._process_update_request(request_json)
        if error_code != '0':
            if error_message:
                o_str = 'Failed to Disable autodiscover \nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to Disable autodiscover'

            raise SDKException('ClientGroup', '102', o_str)

    def refresh(self):
        """Refresh the properties of the ClientGroup."""
        self._initialize_clientgroup_properties()
        self._networkprop = Network(self)
        self._network_throttle = None
