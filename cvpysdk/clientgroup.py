#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing client group operations.

ClientGroups and ClientGroup are the classes defined in this file.

ClientGroups: Class for representing all the client groups associated with a commcell

ClientGroup:  Class for representing a single Client Group of the commcell

ClientGroups:
    __init__(commcell_object)  -- initialise instance of the ClientGroups associated with
                                    the specified commcell

    __repr__()                 -- return all the clientgroup associated with the specified commcell

    _get_clientgroups()        -- gets all the clientgroups associated with the commcell specified

    _valid_clients()           -- returns the list of all the valid clients,
                                    from the list of clients provided

    has_clientgroup()          -- checks if a client group exists with the given name or not

    add(clientgroup_name)      -- adds a new client group to the commcell

    get(clientgroup_name)      -- returns the instance of the ClientGroup class,
                                    for the the input client group name

    delete(clientgroup_name)   -- deletes the client group from the commcell


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

    _process_request_()            -- processes the response received for the CG properties request

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

"""

from __future__ import absolute_import

import time

from .exception import SDKException


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
        self._CLIENTGROUPS = self._commcell_object._services.CLIENTGROUPS
        self._clientgroups = self._get_clientgroups()

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
            self._commcell_object._headers['Host']
        )

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
                    temp_name = str(client_group['name']).lower()
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
            if isinstance(client, str):
                client = client.strip().lower()

                if self._commcell_object.clients.has_client(client):
                    clients.append(client)

        return clients

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
        if not isinstance(clientgroup_name, str):
            raise SDKException('ClientGroup', '101')

        return self._clientgroups and str(clientgroup_name).lower() in self._clientgroups

    def add(self,
            clientgroup_name,
            clients=[],
            clientgroup_description="",
            enable_backup=True,
            enable_restore=True,
            enable_data_aging=True):
        """Adds a new Client Group to the Commcell.

            Args:
                clientgroup_name        (str)        --  name of the new client group to add

                clients                 (str/list)   --  ',' separated string of client names,
                                                             or a list of clients,
                                                             to be added under client group
                    default: []

                clientgroup_description (str)        --  description of the client group
                    default: ""

                enable_backup           (bool)       --  enable or disable backup
                    default: True

                enable_restore          (bool)       --  enable or disable restore
                    default: True

                enable_data_aging       (bool)       --  enable or disable data aging
                    default: True

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
        if not (isinstance(clientgroup_name, str) and isinstance(clientgroup_description, str)):
            raise SDKException('ClientGroup', '101')

        if not self.has_clientgroup(clientgroup_name):
            if isinstance(clients, list):
                clients = self._valid_clients(clients)
            elif isinstance(clients, str):
                clients = self._valid_clients(clients.split(','))
            else:
                raise SDKException('ClientGroup', '101')

            clients_list = []

            for client in clients:
                clients_list.append({'clientName': client})

            request_json = {
                "clientGroupOperationType": 1,
                "clientGroupDetail": {
                    "description": clientgroup_description,
                    "clientGroupActivityControl": {
                        "activityControlOptions": [
                            {
                                "activityType": 1,
                                "enableAfterADelay": False,
                                "enableActivityType": enable_backup
                            }, {
                                "activityType": 16,
                                "enableAfterADelay": False,
                                "enableActivityType": enable_data_aging
                            }, {
                                "activityType": 2,
                                "enableAfterADelay": False,
                                "enableActivityType": enable_restore
                            }
                        ]
                    },
                    "clientGroup": {
                        "clientGroupName": clientgroup_name
                    },
                    "associatedClients": clients_list
                }
            }

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
                        self._clientgroups = self._get_clientgroups()
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
        if not isinstance(clientgroup_name, str):
            raise SDKException('ClientGroup', '101')
        else:
            clientgroup_name = str(clientgroup_name).lower()

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

        if not isinstance(clientgroup_name, str):
            raise SDKException('ClientGroup', '101')
        else:
            clientgroup_name = str(clientgroup_name).lower()

            if self.has_clientgroup(clientgroup_name):
                clientgroup_id = self._clientgroups[clientgroup_name]

                delete_clientgroup_service = self._commcell_object._services.CLIENTGROUP

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'DELETE', delete_clientgroup_service % clientgroup_id
                )

                if flag:
                    if response.json():
                        if 'errorCode' in response.json():
                            error_code = str(response.json()['errorCode'])
                            error_message = str(response.json()['errorMessage'])

                            if error_code == '0':
                                # initialize the clientgroups again
                                # so the clientgroups object has all the client groups
                                self._clientgroups = self._get_clientgroups()
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

        self._clientgroup_name = str(clientgroup_name).lower()

        if clientgroup_id:
            # Use the client group id provided in the arguments
            self._clientgroup_id = str(clientgroup_id)
        else:
            # Get the id associated with this client group
            self._clientgroup_id = self._get_clientgroup_id()

        self._CLIENTGROUP = self._commcell_object._services.CLIENTGROUP % (self.clientgroup_id)

        self._initialize_clientgroup_properties()

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

        if 'clientGroupName' in clientgroup_props['clientGroup']:
            self._clientgroup_name = str(clientgroup_props['clientGroup']['clientGroupName'])
        else:
            raise SDKException(
                'ClientGroup', '102', 'Client Group name is not specified in the respone'
            )

        self._description = None

        if 'description' in clientgroup_props:
            self._description = str(clientgroup_props['description'])

        self._associated_clients = []

        if 'associatedClients' in clientgroup_props:
            for client in clientgroup_props['associatedClients']:
                self._associated_clients.append(str(client['clientName']))

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

    def _request_json_(self, option, enable=True, enable_time=None):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                option (str)  --  string option for which to run the API for
                    e.g.; Backup / Restore / Data Aging

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
                    "newName": self.clientgroup_name
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
                            "TimeZoneName": "(UTC) Coordinated Universal Time",
                            "timeValue": enable_time
                        }
                    }]
                },
                "clientGroup": {
                    "newName": self.clientgroup_name
                }
            }
        }

        if enable_time:
            return request_json2
        else:
            return request_json1

    def _process_request_(self, request_json):
        """Runs the Clientgroup update API to enable/disable backup, restore or data aging flags

            Args:
                request_json    (dict)  -- request json sent as payload

            Returns:
                (str, str):
                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENTGROUP, request_json
        )

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']
                else:
                    error_message = ""

                return (error_code, error_message)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
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

        self._initialize_clientgroup_properties()

        if flag:
            if response.json():

                error_message = str(response.json()['errorMessage'])
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
        if isinstance(clients, str) or isinstance(clients, list):
            clientgroups_object = ClientGroups(self._commcell_object)

            if isinstance(clients, list):
                validated_clients_list = clientgroups_object._valid_clients(clients)
            elif isinstance(clients, str):
                validated_clients_list = clientgroups_object._valid_clients(clients.split(','))

            if operation_type in ['ADD', 'OVERWRITE']:
                for client in validated_clients_list:
                    if client in self._associated_clients:
                        validated_clients_list.remove(client)

            if not validated_clients_list:
                raise SDKException('ClientGroup', '102', 'No valid clients were found')

            output = self._update(
                clientgroup_name=self.clientgroup_name,
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
        if self._associated_clients == []:
            return 'No clients are associated to this client group'

        o_str = 'Associated Clients:\n'
        for client in self._associated_clients:
            o_str += '\t' + client + '\n'

        return str(o_str.strip())

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

    def enable_backup(self):
        """Enable Backup for this ClientGroup.

            Raises:
                SDKException:
                    if failed to enable backup
        """
        request_json = self._request_json_('Backup')

        error_code, error_message = self._process_request_(request_json)

        if error_code == '0':
            self._is_backup_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Backup'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_backup_at_time(self, enable_time):
        """Disables Backup if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

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

        request_json = self._request_json_('Backup', False, enable_time)

        error_code, error_message = self._process_request_(request_json)

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

        error_code, error_message = self._process_request_(request_json)

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

        error_code, error_message = self._process_request_(request_json)

        if error_code == '0':
            self._is_restore_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Restore'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_restore_at_time(self, enable_time):
        """Disables restore if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

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

        request_json = self._request_json_('Restore', False, enable_time)

        error_code, error_message = self._process_request_(request_json)

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

        error_code, error_message = self._process_request_(request_json)

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

        error_code, error_message = self._process_request_(request_json)

        if error_code == '0':
            self._is_data_aging_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Data Aging\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Data Aging'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_data_aging_at_time(self, enable_time):
        """Disables Data Aging if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

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

        request_json = self._request_json_('Data Aging', False, enable_time)

        error_code, error_message = self._process_request_(request_json)

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

        error_code, error_message = self._process_request_(request_json)

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
        if isinstance(value, str):
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
        if isinstance(value, str):
            output = self._update(
                clientgroup_name=self.clientgroup_name,
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
                clients                 (str/list)   --  ',' separated string of client names,
                                                             or a list of clients,
                                                             to be added under client group

                overwrite               (bool)       --  if set to true will remove old clients,
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
                clients                 (str/list)   --  ',' separated string of client names,
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
            clientgroup_name=self.clientgroup_name,
            clientgroup_description=self.description,
            associated_clients=self._associated_clients,
            operation_type="CLEAR"
        )

        if output[0]:
            return
        else:
            o_str = 'Failed to remove clients from the ClientGroup\nError: "{0}"'
            raise SDKException('ClientGroup', '102', o_str.format(output[2]))
