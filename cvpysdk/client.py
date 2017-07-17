#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing client operations.

Clients and Client are 2 classes defined in this file.

Clients: Class for representing all the clients associated with the commcell

Client: Class for a single client of the commcell


Clients:
    __init__(commcell_object) --  initialise object of Clients class associated with the commcell

    __str__()                 --  returns all the clients associated with the commcell

    __repr__()                --  returns the string to represent the instance of the Clients class

    _get_clients()            --  gets all the clients associated with the commcell

    _get_client_dict()        --  returns the client dict for client to be added to member server

    _member_servers()         --  returns member clients to be associated with the Virtual Client

    has_client(client_name)   --  checks if a client exists with the given name or not

    add_vmware_client()       --  adds a new VMWare Virtualization Client to the Commcell

    get(client_name)          --  returns the Client class object of the input client name

    delete(client_name)       --  deletes the client specified by the client name from the commcell


Client:
    __init__(commcell_object,
             client_name,
             client_id=None)     --  initialise object of Class with the specified client name
                                         and id, and associated to the commcell

    __repr__()                   --  return the client name and id, the instance is associated with

    _get_client_id()             --  method to get the client id, if not specified in __init__

    _get_client_properties()     --  get the properties of this client

    enable_backup()              --  enables the backup for the client

    enable_backup_at_time()      --  enables the backup for the client at the input time specified

    disable_backup()             --  disables the backup for the client

    enable_restore()             --  enables the restore for the client

    enable_restore_at_time()     --  enables the restore for the client at the input time specified

    disable_restore()            --  disables the restore for the client

    enable_data_aging()          --  enables the data aging for the client

    enable_data_aging_at_time()  --  enables the data aging for the client at input time specified

    disable_data_aging()         --  disables the data aging for the client

    execute_script()             --  executes given script on the client

    execute_command()            --  executes a command on the client

    enable_intelli_snap()        --  enables intelli snap for the client

    disable_intelli_snap()       --  disables intelli snap for the client

    is_ready                     --  checks if CommServ is able to communicate to client

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import time

from past.builtins import basestring
from base64 import b64encode

from .agent import Agents
from .schedules import Schedules
from .exception import SDKException


class Clients(object):
    """Class for representing all the clients associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Clients class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Clients class
        """
        self._commcell_object = commcell_object
        self._CLIENTS = self._commcell_object._services['GET_ALL_CLIENTS']
        self._ADD_CLIENT = self._commcell_object._services['GET_ALL_CLIENTS']
        self._clients = self._get_clients()

    def __str__(self):
        """Representation string consisting of all clients of the commcell.

            Returns:
                str - string of all the clients associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Client')

        for index, client in enumerate(self._clients):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, client)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Clients class."""
        return "Clients class instance for Commcell: '{0}'".format(
            self._commcell_object._headers['Host']
        )

    def _get_clients(self):
        """Gets all the clients associated with the commcell

            Returns:
                dict - consists of all clients in the commcell
                    {
                         "client1_name": client1_id,
                         "client2_name": client2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._CLIENTS)

        if flag:
            if response.json() and 'clientProperties' in response.json():
                clients_dict = {}

                for dictionary in response.json()['clientProperties']:
                    temp_name = dictionary['client']['clientEntity']['clientName'].lower()
                    temp_id = str(dictionary['client']['clientEntity']['clientId']).lower()
                    clients_dict[temp_name] = temp_id

                return clients_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_client_dict(self, client_object):
        """Returns the client dict for the client object to be appended to member server.

            Args:
                client_object   (object)    --  instance of the Client class

            Returns:
                dict    -   dictionary for a single client to be associated with the Virtual Client
        """
        client_dict = {
            "client": {
                "clientName": client_object.client_name,
                "clientId": int(client_object.client_id),
                "_type_": 3
            }
        }

        return client_dict

    def _member_servers(self, clients_list):
        """Returns the member clients to be associated with the Virtual Client.

            Args:
                clients_list (list)    --  list of the clients to associated to the virtual client

            Returns:
                list - list consisting of all member servers to be associated to the Virtual Client

            Raises:
                SDKException:
                    if type of clients list argument is not list
        """
        if not isinstance(clients_list, list):
            raise SDKException('Client', '101')

        member_servers = []

        for client in clients_list:
            if isinstance(client, basestring):
                client = client.strip().lower()

                if self.has_client(client):
                    temp_client = self.get(client)

                    if temp_client.agents.has_agent('virtual server'):
                        client_dict = self._get_client_dict(temp_client)
                        member_servers.append(client_dict)

                    del temp_client
            elif isinstance(client, Client):
                if client.agents.has_agent('virtual server'):
                    client_dict = self._get_client_dict(client)
                    member_servers.append(client_dict)

        return member_servers

    def has_client(self, client_name):
        """Checks if a client exists in the commcell with the input client name.

            Args:
                client_name (str)  --  name of the client

            Returns:
                bool - boolean output whether the client exists in the commcell or not

            Raises:
                SDKException:
                    if type of the client name argument is not string
        """
        if not isinstance(client_name, basestring):
            raise SDKException('Client', '101')

        return self._clients and client_name.lower() in self._clients

    def add_vmware_client(
            self,
            client_name,
            vcenter_hostname,
            vcenter_username,
            vcenter_password,
            clients):
        """Adds a new VMWare Virtualization Client to the Commcell.

            Args:
                client_name         (str)   --  name of the new VMWare Virtual Client
                vcenter_hostname    (str)   --  hostname of the vcenter to connect to
                vcenter_username    (str)   --  login username for the vcenter
                vcenter_password    (str)   --  plain-text password for the vcenter
                clients             (list)  --  list cotaining client names / client objects,
                                                    to associate with the Virtual Client

            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if failed to add the client

                    if response is empty

                    if response is not success
        """
        if self.has_client(client_name):
            raise SDKException('Client', '102', 'Client "{0}" already exists.'.format(client_name))

        vcenter_password = b64encode(vcenter_password.encode()).decode()
        member_servers = self._member_servers(clients)

        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 1,
                        "associatedClients": {
                            "memberServers": member_servers
                        },
                        "vmwareVendor": {
                            "vcenterHostName": vcenter_hostname,
                            "virtualCenter": {
                                "userName": vcenter_username,
                                "password": vcenter_password
                            }
                        }
                    }
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._ADD_CLIENT, request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                        raise SDKException('Client', '102', o_str)
                    else:
                        client_id = response.json()['response']['entity']['clientId']

                        # initialize the clients again
                        # so the client object has all the clients
                        self._clients = self._get_clients()
                        return Client(self._commcell_object, client_name, client_id)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, client_name):
        """Returns a client object of the specified client name.

            Args:
                client_name (str)  --  name of the client

            Returns:
                object - instance of the Client class for the given client name

            Raises:
                SDKException:
                    if type of the client name argument is not string

                    if no client exists with the given name
        """
        if not isinstance(client_name, basestring):
            raise SDKException('Client', '101')
        else:
            client_name = client_name.lower()

            if self.has_client(client_name):
                return Client(self._commcell_object, client_name, self._clients[client_name])

            raise SDKException(
                'Client', '102', 'No client exists with name: {0}'.format(client_name)
            )

    def delete(self, client_name):
        """Deletes the client from the commcell.

            Args:
                client_name (str)  --  name of the client to remove from the commcell

            Raises:
                SDKException:
                    if type of the client name argument is not string

                    if failed to delete client

                    if response is empty

                    if response is not success

                    if no client exists with the given name
        """
        if not isinstance(client_name, basestring):
            raise SDKException('Client', '101')
        else:
            client_name = client_name.lower()

            if self.has_client(client_name):
                client_id = self._clients[client_name]
                client_delete_service = self._commcell_object._services['CLIENT'] % (client_id)
                client_delete_service += "?forceDelete=1"

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'DELETE', client_delete_service
                )

                error_code = warning_code = 0

                if flag:
                    if response.json() and 'response' in response.json():
                        if 'response' in response.json():
                            if response.json()['response'][0]['errorCode'] == 0:
                                # initialize the clients again
                                # so the client object has all the clients
                                self._clients = self._get_clients()
                        else:
                            if 'errorCode' in response.json():
                                error_code = response.json()['errorCode']

                            if 'warningCode' in response.json():
                                warning_code = response.json()['warningCode']

                            o_str = 'Failed to delete client'

                            if error_code != 0:
                                error_message = response.json()['errorMessage']
                                if error_message:
                                    o_str += '\nError: "{0}"'.format(error_message)
                            elif warning_code != 0:
                                warning_message = response.json()['warningMessage']
                                if warning_message:
                                    o_str += '\nWarning: "{0}"'.format(warning_message)

                            raise SDKException('Client', '102', o_str)
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'Client', '102', 'No client exists with name: {0}'.format(client_name)
                )


class Client(object):
    """Class for performing client operations for a specific client."""

    def __init__(self, commcell_object, client_name, client_id=None):
        """Initialise the Client class instance.

            Args:
                commcell_object (object)  --  instance of the Commcell class

                client_name     (str)     --  name of the client

                client_id       (str)     --  id of the client
                    default: None

            Returns:
                object - instance of the Client class
        """
        self._commcell_object = commcell_object
        self._client_name = client_name.lower()

        if client_id:
            self._client_id = str(client_id)
        else:
            self._client_id = self._get_client_id()

        self._CLIENT = self._commcell_object._services['CLIENT'] % (self.client_id)
        self._get_client_properties()

        self.agents = Agents(self)
        self.schedules = Schedules(self)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Client class instance for Client: "{0}"'
        return representation_string.format(self.client_name)

    def _get_client_id(self):
        """Gets the client id associated with this client.

            Returns:
                str - id associated with this client
        """
        clients = Clients(self._commcell_object)
        return clients.get(self.client_name).client_id

    def _get_client_properties(self):
        """Gets the client properties of this client.

            Returns:
                dict - dictionary consisting of the properties of this client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._CLIENT)

        if flag:
            if response.json() and 'clientProperties' in response.json():
                self._properties = response.json()['clientProperties'][0]

                os_info = self._properties['client']['osInfo']
                processor_type = os_info['OsDisplayInfo']['ProcessorType']
                os_name = os_info['OsDisplayInfo']['OSName']

                self._os_info = '{0} {1} {2}  --  {3}'.format(
                    processor_type,
                    os_info['Type'],
                    os_info['SubType'],
                    os_name
                )

                self._install_directory = None
                self._version = None
                self._service_pack = None

                client_props = self._properties['clientProps']

                self._is_data_recovery_enabled = client_props[
                    'activityControl']['EnableDataRecovery']

                self._is_data_management_enabled = client_props[
                    'activityControl']['EnableDataManagement']

                self._is_ci_enabled = client_props['activityControl']['EnableOnlineContentIndex']

                activities = client_props["clientActivityControl"]["activityControlOptions"]

                for activity in activities:
                    if activity["activityType"] == 1:
                        self._is_backup_enabled = activity["enableActivityType"]
                    elif activity["activityType"] == 2:
                        self._is_restore_enabled = activity["enableActivityType"]
                    elif activity["activityType"] == 16:
                        self._is_data_aging_enabled = activity["enableActivityType"]

                self._client_hostname = self._properties['client']['clientEntity']['hostName']

                self._is_intelli_snap_enabled = bool(client_props['EnableSnapBackups'])

                if 'installDirectory' in self._properties['client']:
                    self._install_directory = self._properties['client']['installDirectory']

                if 'GalaxyRelease' in self._properties['client']['versionInfo']:
                    self._version = self._properties['client'][
                        'versionInfo']['GalaxyRelease']['ReleaseString']

                if 'version' in self._properties['client']['versionInfo']:
                    patch_info = self._properties['client']['versionInfo']['version']

                    self._service_pack = patch_info.split(',')[0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
            "association": {
                "entity": [{
                    "clientName": self.client_name
                }]
            },
            "clientProperties": {
                "clientProps": {
                    "clientActivityControl": {
                        "activityControlOptions": [{
                            "activityType": options_dict[option],
                            "enableAfterADelay": False,
                            "enableActivityType": enable
                        }]
                    }
                }
            }
        }

        request_json2 = {
            "association": {
                "entity": [{
                    "clientName": self.client_name
                }]
            },
            "clientProperties": {
                "clientProps": {
                    "clientActivityControl": {
                        "activityControlOptions": [{
                            "activityType": options_dict[option],
                            "enableAfterADelay": True,
                            "enableActivityType": False,
                            "dateTime": {
                                "TimeZoneName": "(UTC) Coordinated Universal Time",
                                "timeValue": enable_time
                            }
                        }]
                    }
                }
            }
        }

        if enable_time:
            return request_json2
        else:
            return request_json1

    def _update_client_props_json(self, properties_dict):
        """Returns the update client properties JSON request to pass to the API as per
            the property mentioned by the user.

            Args:
                properties_dict (dict)  --  client property dict which is to be updated
                    e.g.: {
                            "EnableSnapBackups": True
                          }

            Returns:
                Client Properties update dict
        """
        request_json = {
            "clientProperties": {
                "clientProps": {}
            },
            "association": {
                "entity": [
                    {
                        "clientName": self.client_name
                    }
                ]
            }
        }

        request_json['clientProperties']['clientProps'].update(properties_dict)

        return request_json

    @property
    def client_id(self):
        """Treats the client id as a read-only attribute."""
        return self._client_id

    @property
    def client_name(self):
        """Treats the client name as a read-only attribute."""
        return self._client_name

    @property
    def client_hostname(self):
        """Treats the client host name as a read-only attribute."""
        return self._client_hostname

    @property
    def os_info(self):
        """Treats the os information as a read-only attribute."""
        return self._os_info

    @property
    def is_data_recovery_enabled(self):
        """Treats the is data recovery enabled as a read-only attribute."""
        return self._is_data_recovery_enabled

    @property
    def is_data_management_enabled(self):
        """Treats the is data management enabled as a read-only attribute."""
        return self._is_data_management_enabled

    @property
    def is_ci_enabled(self):
        """Treats the is online content index enabled as a read-only attribute."""
        return self._is_ci_enabled

    @property
    def is_backup_enabled(self):
        """Treats the is backup enabled as a read-only attribute."""
        return self._is_backup_enabled

    @property
    def is_restore_enabled(self):
        """Treats the is restore enabled as a read-only attribute."""
        return self._is_restore_enabled

    @property
    def is_data_aging_enabled(self):
        """Treats the is data aging enabled as a read-only attribute."""
        return self._is_data_aging_enabled

    @property
    def is_intelli_snap_enabled(self):
        """Treats the is intelli snap enabled as a read-only attribute."""
        return self._is_intelli_snap_enabled

    @property
    def install_directory(self):
        """Treats the install directory as a read-only attribute."""
        return self._install_directory

    @property
    def version(self):
        """Treats the version as a read-only attribute."""
        return self._version

    @property
    def service_pack(self):
        """Treats the service pack as a read-only attribute."""
        return self._service_pack

    def enable_backup(self):
        """Enable Backup for this Client.

            Raises:
                SDKException:
                    if failed to enable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Backup')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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

                    if response is empty

                    if response is not success
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('Client', '103')
        except ValueError:
            raise SDKException('Client', '104')

        request_json = self._request_json_('Backup', False, enable_time)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_backup(self):
        """Disables Backup for this Client.

            Raises:
                SDKException:
                    if failed to disable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Backup', False)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to disable Backup\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_restore(self):
        """Enable Restore for this Client.

            Raises:
                SDKException:
                    if failed to enable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Restore')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_restore_at_time(self, enable_time):
        """Disables Restore if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the restore at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable restore

                    if response is empty

                    if response is not success
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('Client', '103')
        except ValueError:
            raise SDKException('Client', '104')

        request_json = self._request_json_('Restore', False, enable_time)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_restore(self):
        """Disables Restore for this Client.

            Raises:
                SDKException:
                    if failed to disable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Restore', False)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to disable Restore\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_data_aging(self):
        """Enable Data Aging for this Client.

            Raises:
                SDKException:
                    if failed to enable data aging

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Data Aging')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to enable Data Aging\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_data_aging_at_time(self, enable_time):
        """Disables Data Aging if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the data aging at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable data aging

                    if response is empty

                    if response is not success
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('Client', '103')
        except ValueError:
            raise SDKException('Client', '104')

        request_json = self._request_json_('Data Aging', False, enable_time)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to enable Data Aging\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_data_aging(self):
        """Disables Data Aging for this Client.

            Raises:
                SDKException:
                    if failed to disable data aging

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Data Aging', False)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to disable Data Aging\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def execute_script(self, script_type, script):
        """Executes the given script of the script type on this client.

            Args:
                script_type     (str)   --  type of script to be executed on the client
                    JAVA / Python / PowerShell / WindowsBatch / UnixShell

                script          (str)   --  path of the script to be executed on the client

            Raises:
                SDKException:
                    if script type argument is not of type string

                    if script argument is not of type string

                    if script type is not valid

                    if response is empty

                    if response is not success
        """
        if not (isinstance(script_type, basestring) and (isinstance(script, basestring))):
            raise SDKException('Client', '101')

        script_types = {
            'java': 0,
            'python': 1,
            'powershell': 2,
            'windowsbatch': 3,
            'unixshell': 4
        }

        if script_type.lower() not in script_types:
            raise SDKException('Client', '105')

        if os.path.isfile(script):
            with open(script, 'r') as temp_file:
                script_file = temp_file.read()
        else:
            raise SDKException('Client', '105')

        import html
        script = html.escape(script_file)
        script_lines = ""
        script_lines_template = '<scriptLines val="{0}"/>'

        for line in script.split('\n'):
            script_lines += script_lines_template.format(line)

        xml_execute_script = """
        <App_ExecuteCommandReq arguments="" scriptType="{0}" waitForProcessCompletion="1">
            <client clientId="{1}" clientName="{2}"/>
            "{3}"
        </App_ExecuteCommandReq>
        """.format(
            script_types[script_type.lower()],
            self.client_id,
            self.client_name,
            script_lines
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], xml_execute_script
        )

        if flag:
            if response.json():
                exit_code = None
                output = None

                if 'commandLineOutput' in response.json():
                    output = response.json()['commandLineOutput']

                if 'processExitCode' in response.json():
                    exit_code = response.json()['processExitCode']

                return exit_code, output
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def execute_command(self, command):
        """Executes a command on this client.

            Args:
                command     (str)   --  command in string to be executed on the client

            Raises:
                SDKException:
                    if command argument is not of type string

                    if response is empty

                    if response is not success
        """
        if not isinstance(command, basestring):
            raise SDKException('Client', '101')

        import html
        command = html.escape(command)

        xml_execute_command = """
        <App_ExecuteCommandReq arguments="" command="{0}" waitForProcessCompletion="1">
            <processinginstructioninfo>
                <formatFlags continueOnError="1" elementBased="1" filterUnInitializedFields="0" formatted="0" ignoreUnknownTags="1" skipIdToNameConversion="0" skipNameToIdConversion="0"/>
            </processinginstructioninfo>
            <client clientId="{1}" clientName="{2}"/>
        </App_ExecuteCommandReq>
        """.format(command, self.client_id, self.client_name)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], xml_execute_command
        )

        if flag:
            if response.json():
                exit_code = None
                output = None

                if 'commandLineOutput' in response.json():
                    output = response.json()['commandLineOutput']

                if 'processExitCode' in response.json():
                    exit_code = response.json()['processExitCode']

                return exit_code, output
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_intelli_snap(self):
        """Enables Intelli Snap for this Client.

            Raises:
                SDKException:
                    if failed to enable intelli snap

                    if response is empty

                    if response is not success
        """
        enable_intelli_snap_dict = {
            "EnableSnapBackups": True
        }

        request_json = self._update_client_props_json(enable_intelli_snap_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to enable Inetlli Snap\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_intelli_snap(self):
        """Disables Intelli Snap for this Client.

            Raises:
                SDKException:
                    if failed to disable intelli snap

                    if response is empty

                    if response is not success
        """
        disable_intelli_snap_dict = {
            "EnableSnapBackups": False
        }

        request_json = self._update_client_props_json(disable_intelli_snap_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to disable Inetlli Snap\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def is_ready(self):
        """Checks if CommServ is able to communicate to the client.

            Returns:
                True    -   if the CS is able to connect to the client

                False   -   if communication fails b/w the CS and the client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        request_xml = """
        <EVGui_CheckReadinessReq >
            <entity clientName="{0}" />
        </EVGui_CheckReadinessReq>
        """.format(self.client_name)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json():
                if int(response.json()['isClientReady']) == 0:
                    return False
                return True
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
