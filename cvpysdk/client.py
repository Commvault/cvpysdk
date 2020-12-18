# -*- coding: utf-8 -*-
# pylint: disable=R1705, R0205

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

"""File for performing client related operations on the Commcell.

Clients and Client are 2 classes defined in this file.

Clients:    Class for representing all the clients associated with the commcell

Client:     Class for a single client of the commcell


Clients
=======

    __init__(commcell_object)             --  initialize object of Clients class associated with
    the commcell

    __str__()                             --  returns all the clients associated with the commcell

    __repr__()                            --  returns the string to represent the instance of the
    Clients class

    __len__()                             --  returns the number of clients associated with the
    Commcell

    __getitem__()                         --  returns the name of the client at the given index
    or the details for the given client name

    _get_clients()                        --  gets all the clients associated with the commcell

    _get_office_365_clients()             --  get all office365 clients in the commcell

    _get_hidden_clients()                 --  gets all the hidden clients associated with the
    commcell

    _get_virtualization_clients()         --  gets all the virtualization clients associated with
    the commcell

    _get_client_dict()                    --  returns the client dict for client to be added to
    member server

    _member_servers()                     --  returns member clients to be associated with the
    Virtual Client

    _get_client_from_hostname()           --  returns the client name if associated with specified
    hostname if exists

    _get_hidden_client_from_hostname()    --  returns the client name if associated with specified
    hostname if exists

    has_client(client_name)               --  checks if a client exists with the given name or not

    has_hidden_client(client_name)        --  checks if a hidden client exists with the given name

    _process_add_response()               -- to process the add client request using API call

    add_vmware_client()                   --  adds a new VMWare Virtualization Client to the
                                              Commcell

    add_kubernetes_client()               --  adds a new Kubernetes Virtualization Client to the
                                              Commcell

    add_nas_client()                      --  adds a new NAS Client

    add_share_point_client()              -- adds a new sharepoint pseudo client to the Commcell

    add_exchange_client()                 --  adds a new Exchange Virtual Client to the Commcell

    add_splunk_client()                   --  adds a new Splunk Client to the Commcell

    add_case_client()                     --  adds a new Case Manger Client to the Commcell

    add_salesforce_client()               --  adds a new salesforce client

    add_azure_client()                    --  adds a new azure cloud client

    add_amazon_client()                    --  adds a new amazon cloud client

    add_google_client()                    --  adds a new google cloud client

    add_alicloud_client()                    --  adds a new alibaba cloud client

    add_nutanix_files_client()                  --  adds a new nutanix files client

    add_onedrive_client()                 --  adds a new onedrive client

    get(client_name)                      --  returns the Client class object of the input client
    name

    delete(client_name)                   --  deletes the client specified by the client name from
    the commcell

    filter_clients_return_displaynames()  --  filter clients based on criteria

    refresh()                             --  refresh the clients associated with the commcell

Clients Attributes
------------------

    **all_clients**             --  returns the dictioanry consisting of all the clients that are
    associated with the commcell and their information such as id and hostname

    **hidden_clients**          --  returns the dictioanry consisting of only the hidden clients
    that are associated with the commcell and their information such as id and hostname

    **virtualization_clients**  --  returns the dictioanry consisting of only the virtualization
    clients that are associated with the commcell and their information such as id and hostname

    **office365_clients** -- returns the dictioanry consisting of all the office 365 clients that are
    associated with the commcell


Client
======

    __init__()                   --  initialize object of Class with the specified client name
    and id, and associated to the commcell

    __repr__()                   --  return the client name and id, the instance is associated with

    _get_client_id()             --  method to get the client id, if not specified in __init__

    _get_client_properties()     --  get the properties of this client

    _get_instance_of_client()    --  get the instance associated with the client

    _get_log_directory()         --  get the log directory path on the client

    _service_operations()        --  perform services related operations on a client

                START / STOP / RESTART

    _make_request()              --  makes the upload request to the server

    _process_update_request()    --  to process the request using API call

    update_properties()          --  to update the client properties

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

    upload_file()                --  uploads the specified file on controller to the client machine

    upload_folder()              --  uploads the specified folder on controller to client machine

    start_service()              --  starts the service with the given name on the client

    stop_service()               --  stops the service with the given name on the client

    restart_service()            --  restarts the service with the given name on the client

    restart_services()           --  executes the command on the client to restart the services

    push_network_config()        --  performs a push network configuration on the client

    add_user_association()       --  adds the user associations on this client

    add_client_owner()           --  adds users to owner list of this client

    refresh()                    --  refresh the properties of the client

    add_additional_setting()     --  adds registry key to the client property

    delete_additional_setting()  --  deletes registry key from the client property

    release_license()            --  releases a license from a client

    retire()                     --  perform retire operation on the client

    reconfigure_client()         --  reapplies license to the client

    push_servicepack_and_hotfixes() -- triggers installation of service pack and hotfixes

    repair_software()            -- triggers Repair software on the client machine

    get_dag_member_servers()     --  Gets the member servers of an Exchange DAG client.

    create_pseudo_client()       --  Creates a pseudo client

    register_decoupled_client()  --  registers decoupled client

    set_job_start_time()         -- sets the job start time at client level

    uninstall_software()         -- Uninstalls all the packages of the client

    get_network_summary()        -- Gets the network summary of the client

    change_exchange_job_results_directory()
                                --  Move the Job Results Directory for an
                                    Exchange Online Environment

    get_environment_details()   --  Gets environment tile details present in dashboard page

    get_needs_attention_details()   -- Gets needs attention tile details from dashboard page


Client Attributes
-----------------

    **available_security_roles**    --  returns the security roles available for the selected
    client

    **properties**                  --  returns the properties of the client

    **display_name**                --  returns the display name of the client

    **description**                 --  returns the description of the client

    **client_id**                   --  returns the id of the client

    **client_name**                 --  returns the name of the client

    **client_hostname**             --  returns the host name of the client

    **timezone**                    --  returns the timezone of the client

    **os_info**                     --  returns string consisting of OS information of the client

    **is_data_recovery_enabled**    --  boolean specifying whether data recovery is enabled for the
    client or not

    **is_data_management_enabled**  --  boolean specifying whether data management is enabled for
    the client or not

    **is_ci_enabled**               --  boolean specifying whether content indexing is enabled for
    the client or not

    **is_backup_enabled**           --  boolean specifying whether backup activity is enabled for
    the client or not

    **is_restore_enabled**          --  boolean specifying whether restore activity is enabled for
    the client or not

    **is_data_aging_enabled**       --  boolean specifying whether data aging is enabled for the
    client or not

    **is_intelli_snap_enabled**     --  boolean specifying whether intelli snap is enabled for the
    client or not

    **install_directory**           --  returns the path where the client is installed at

    **version**                     --  returns the version of the product installed on the client

    **service_pack**                --  returns the service pack installed on the client

    **job_results_directory**       --  returns the path of the job results directory on the client

    **instance**                    --  returns the Instance of the client

    **log_directory**               --  returns the path of the log directory on the client

    **agents**                      --  returns the instance of the Agents class representing
    the list of agents installed on the Client

    **schedules**                   --  returns the instance of the Schedules class representing
    the list of schedules configured for the Client

    **users**                       --  returns the instance of the Users class representing the
    list of users with access to the Client

    **network**                     --  returns object of the Network class corresponding to the
    selected client

    **is_ready**                    --  returns boolean value specifying whether services on the
    client are running or not, and whether the CommServ is able to communicate with the client


    **set_encryption_prop**         --    Set encryption properties on a client

    **set_dedup_prop**              --     Set DDB properties

    **consumed_licenses**           --  returns dictionary of all the license details
    which is consumed by the client

    **cvd_port**                    -- returns cvd port of the client

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
import time
import copy

from base64 import b64encode
from past.builtins import basestring

import requests

from .job import Job
from .agent import Agents
from .schedules import Schedules
from .exception import SDKException
from .deployment.install import Install
from .deployment.uninstall import Uninstall

from .network import Network
from .network_throttle import NetworkThrottle

from .security.user import Users

from .name_change import NameChange


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

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        # TODO: check with API team for additional property to remove multiple API calls
        # and use a single API call to get all types of clients, and to be able to distinguish
        # them
        self._CLIENTS = self._ADD_CLIENT = self._services['GET_ALL_CLIENTS']
        self._OFFICE_365_CLIENTS = self._services['GET_OFFICE_365_ENTITIES']
        self._ALL_CLIENTS = self._services['GET_ALL_CLIENTS_PLUS_HIDDEN']
        self._VIRTUALIZATION_CLIENTS = self._services['GET_VIRTUAL_CLIENTS']
        self._ADD_EXCHANGE_CLIENT = self._ADD_SHAREPOINT_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_SPLUNK_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_NUTANIX_CLIENT = self._services['CREATE_NUTANIX_CLIENT']
        self._ADD_NAS_CLIENT = self._services['CREATE_NAS_CLIENT']
        self._ADD_ONEDRIVE_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._clients = None
        self._hidden_clients = None
        self._virtualization_clients = None
        self._office_365_clients = None

        self.refresh()

    def __str__(self):
        """Representation string consisting of all clients of the commcell.

            Returns:
                str - string of all the clients associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Client')

        for index, client in enumerate(self.all_clients):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, client)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Clients class."""
        return "Clients class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the clients associated to the Commcell."""
        return len(self.all_clients)

    def __getitem__(self, value):
        """Returns the name of the client for the given client ID or
            the details of the client for given client Name.

            Args:
                value   (str / int)     --  Name or ID of the client

            Returns:
                str     -   name of the client, if the client id was given

                dict    -   dict of details of the client, if client name was given

            Raises:
                IndexError:
                    no client exists with the given Name / Id

        """
        value = str(value).lower()

        if value in self.all_clients:
            return self.all_clients[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_clients.items()))[0][0]
            except IndexError:
                raise IndexError('No client exists with the given Name / Id')

    def _get_clients(self):
        """Gets all the clients associated with the commcell

            Returns:
                dict    -   consists of all clients in the commcell

                    {
                        "client1_name": {

                            "id": client1_id,

                            "hostname": client1_hostname
                        },

                        "client2_name": {

                            "id": client2_id,

                            "hostname": client2_hostname
                        }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._CLIENTS)

        if flag:
            if response.json() and 'clientProperties' in response.json():
                clients_dict = {}

                for dictionary in response.json()['clientProperties']:
                    temp_name = dictionary['client']['clientEntity']['clientName'].lower()
                    temp_id = str(dictionary['client']['clientEntity']['clientId']).lower()
                    temp_hostname = dictionary['client']['clientEntity']['hostName'].lower()
                    clients_dict[temp_name] = {
                        'id': temp_id,
                        'hostname': temp_hostname
                    }

                return clients_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_office_365_clients(self):
        """REST API call to get all office365 clients in the commcell

                  Returns:
                      dict    -   consists of all office 365 clients in the commcell
                          {
                              "client1_name": {

                                  "id": client1_id

                              },

                              "client2_name": {

                                  "id": client2_id
                              }
                          }

                  Raises:
                      SDKException:
                          if response is empty

                          if response is not success

              """
        flag, response = self._cvpysdk_object.make_request('GET', self._OFFICE_365_CLIENTS)

        if flag:
            if response.json() and "o365Client" in response.json():
                clients_dict = {}

                for dictionary in response.json()['o365Client']:
                    temp_name = dictionary['clientName'].lower()
                    temp_id = str(dictionary['clientId']).lower()
                    clients_dict[temp_name] = {
                        'id': temp_id
                    }

                return clients_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def office_365_clients(self):
        """Returns the dict of all office 365 clients in the commcell"""
        if self._office_365_clients is None:
            self._office_365_clients = self._get_office_365_clients()
        return self._office_365_clients

    def _get_hidden_clients(self):
        """Gets all the clients associated with the commcell, including all VM's and hidden clients

            Returns:
                dict    -   consists of all clients (including hidden clients) in the commcell

                    {
                        "client1_name": {

                            "id": client1_id,

                            "hostname": client1_hostname
                        },

                        "client2_name": {

                            "id": client2_id,

                            "hostname": client2_hostname
                        }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._ALL_CLIENTS)

        if flag:
            if response.json() and 'clientProperties' in response.json():
                all_clients_dict = {}
                hidden_clients_dict = {}

                for dictionary in response.json()['clientProperties']:
                    temp_name = dictionary['client']['clientEntity']['clientName'].lower()
                    temp_id = str(dictionary['client']['clientEntity']['clientId']).lower()
                    temp_hostname = dictionary['client']['clientEntity']['hostName'].lower()
                    all_clients_dict[temp_name] = {
                        'id': temp_id,
                        'hostname': temp_hostname
                    }

                # hidden clients = all clients - true clients
                hidden_clients_dict = {
                    client: all_clients_dict.get(
                        client, client in all_clients_dict or self.all_clients[client]
                    )
                    for client in set(all_clients_dict) - set(self.all_clients)
                }
                return hidden_clients_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_virtualization_clients(self):
        """REST API call to get all virtualization clients in the commcell

            Returns:
                dict    -   consists of all virtualization clients in the commcell

                    {
                        "client1_name": {

                            "id": client1_id,

                            "hostname": client1_hostname
                        },

                        "client2_name": {

                            "id": client2_id,

                            "hostname": client2_hostname
                        }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._VIRTUALIZATION_CLIENTS)

        if flag:
            if response.json() and 'VSPseudoClientsList' in response.json():
                pseudo_clients = response.json()['VSPseudoClientsList']
                virtualization_clients = {}

                for pseudo_client in pseudo_clients:
                    virtualization_clients[pseudo_client['client']['clientName'].lower()] = {
                        'clientId': pseudo_client['client']['clientId'],
                        'hostName': pseudo_client['client']['hostName']
                    }

                return virtualization_clients

            return {}
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @staticmethod
    def _get_client_dict(client_object):
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

    def _get_client_from_hostname(self, hostname):
        """Checks if a client is associated with the given hostname.

            Args:
                hostname    (str)   --  host name of the client on this commcell

            Returns:
                str     -   name of the client associated with this hostname

                None    -   if no client has the same hostname as the given input

        """
        # verify there is no client in the Commcell with the same name as the given hostname
        # for multi-instance clients
        if self.all_clients and hostname not in self.all_clients:
            for client in self.all_clients:
                if hostname.lower() == self.all_clients[client]['hostname']:
                    return client

    def _get_hidden_client_from_hostname(self, hostname):
        """Checks if hidden client associated given hostname exists and returns the hidden client
            name

            Args:
                hostname    (str)   --  host name of the client on this commcell

            Returns:
                str     -   name of the client associated with this hostname

                None    -   if no client has the same hostname as the given input

        """
        # verify there is no client in the Commcell with the same name as the given hostname
        # for multi-instance clients
        if self.hidden_clients and hostname not in self.hidden_clients:
            for hidden_client in self.hidden_clients:
                if hostname.lower() == self.hidden_clients[hidden_client]['hostname']:
                    return hidden_client

    @property
    def all_clients(self):
        """Returns the dictionary consisting of all the clients and their info.

            dict - consists of all clients in the commcell
                    {
                         "client1_name": {
                                "id": client1_id,
                                "hostname": client1_hostname
                        },
                         "client2_name": {
                                "id": client2_id,
                                "hostname": client2_hostname
                         },
                    }

        """
        return self._clients

    def create_pseudo_client(self, client_name, client_hostname=None):
        """ Creates a pseudo client

            Args:
                client_name 	(str)   --  name of the client to be created

				client_hostname (str) 	-- 	hostname of the client to be created
					default:None

            Returns:
                client object for the created client.

            Raises:
                SDKException:
                    if client name type is incorrect

                    if response is empty

                    if failed to get client id from response

        """
        if not isinstance(client_name, str):
            raise SDKException('Client', '101')

        request_json = {
            'App_CreatePseudoClientRequest':
                {
                    "registerClient": "false",
                    "clientInfo": {
                        "clientType": 0,
                        "openVMSProperties": {
                            "cvdPort": 0
                        },
                        "ibmiInstallOptions": {}
                    },
                    "entity": {
                        "hostName": client_hostname if client_hostname else client_name,
                        "clientName": client_name,
                        "clientId": 0,
                        "_type_": 3
                    }
                }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_json
        )

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']
                error_string = response.json()['response'].get('errorString', '')
                if error_code == 0:
                    self.refresh()
                    return self.get(client_name)
                else:
                    o_str = 'Failed to create pseudo client. Error: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def register_decoupled_client(self, client_name, client_host_name, port_number=8400):
        """ registers decoupled client

            Args:
                client_name (str)    --  client name

                client_host_name (str)  -- client host name

                port_number (int)   -- port number of the decoupled client

            Returns:
                client object for the registered client.

            Raises:
                SDKException:
                    if client name type is incorrect

                    if response is empty

                    if failed to get client id from response

        """
        request_json = {
            "App_RegisterClientRequest":
                {
                    "getConfigurationFromClient": True,
                    "configFileName": "",
                    "cvdPort": port_number,
                    "client": {
                        "hostName": client_host_name,
                        "clientName": client_name,
                        "newName": ""
                    }
                }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']
                if error_code == 0:
                    self.refresh()
                    return self.get(client_name)
                else:
                    if response.json()['errorMessage']:
                        o_str = 'Failed to register client. Error: "{0}"'.format(response.json()['errorMessage'])
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def hidden_clients(self):
        """Returns the dictionary consisting of the hidden clients and their info.

            dict - consists of all clients in the commcell
                    {
                         "client1_name": {
                                "id": client1_id,
                                "hostname": client1_hostname
                        },
                         "client2_name": {
                                "id": client2_id,
                                "hostname": client2_hostname
                         },
                    }

        """
        return self._hidden_clients

    @property
    def virtualization_clients(self):
        """Returns the dictionary consisting of the virtualization clients and their info.

            dict - consists of all clients in the commcell
                    {
                         "client1_name": {
                                "id": client1_id,
                                "hostname": client1_hostname
                        },
                         "client2_name": {
                                "id": client2_id,
                                "hostname": client2_hostname
                         },
                    }

        """
        return self._virtualization_clients

    def has_client(self, client_name):
        """Checks if a client exists in the commcell with the given client name / hostname.

            Args:
                client_name     (str)   --  name / hostname of the client

            Returns:
                bool    -   boolean output whether the client exists in the commcell or not

            Raises:
                SDKException:
                    if type of the client name argument is not string

        """
        if not isinstance(client_name, basestring):
            raise SDKException('Client', '101')
        if self.all_clients and client_name.lower() in self.all_clients:
            return True
        elif self._get_client_from_hostname(client_name) is not None:
            return True
        elif self.hidden_clients and client_name.lower() in self.hidden_clients:
            return True
        elif self._get_hidden_client_from_hostname(client_name) is not None:
            return True
        return False

    def has_hidden_client(self, client_name):
        """Checks if a client exists in the commcell with the input client name as a hidden client.

            Args:
                client_name (str)  --  name of the client

            Returns:
                bool - boolean output whether the client exists in the commcell or not as a hidden
                client

            Raises:
                SDKException:
                    if type of the client name argument is not string
        """
        if not isinstance(client_name, basestring):
            raise SDKException('Client', '101')

        return ((self.hidden_clients and client_name.lower() in self.hidden_clients) or
                self._get_hidden_client_from_hostname(client_name) is not None)

    def _process_add_response(self, request_json):
        """Runs the Client Add API with the request JSON provided,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                (bool, basestring, basestring):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._ADD_CLIENT, request_json)

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        client_name = response.json(
                        )['response']['entity']['clientName']
                        self.refresh()
                        return self.get(client_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_kubernetes_client(
            self,
            client_name,
            master_node,
            secret_name,
            secret_key,
            vsaclient,
            vsaclient_id
    ):
        """Adds a new Kubernetes Virtualization Client to the Commcell.

            Args:
                client_name         (str)   --  name of the new Kubernetes Virtual Client

                master_node         (str)   --  Kubernetes kubectl node

                secret_name         (str)   --  Kubernetes Secret name

                secret_key          (str)   --  Kubernetes Secret Key

                vsaclient           (str)   --  Virtual Server proxy client

                vsaclient_id        (int)   --  Virtual Server Client id


            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if failed to add the client

                    if response is empty

                    if response is not success

        """
        host_name = "https://{0}:6443".format(master_node)
        if self.has_client(client_name):
            raise SDKException('Client', '102', 'Client "{0}" already exists.'.format(client_name))

        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 20,
                        "k8s": {
                            "secretName": secret_name,
                            "secretKey": secret_key,
                            "secretType": "ServiceAccount",
                            "endpointurl": host_name
                        },
                        "associatedClients": {
                            "memberServers": [
                                {
                                    "client": {
                                        "clientName": vsaclient,
                                        "clientId": vsaclient_id,
                                        "_type_": 3
                                    }
                                }
                            ]
                        },
                        "vmwareVendor": {
                            "vcenterHostName": host_name
                        }
                    }
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._ADD_CLIENT, request_json)

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']
                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                        raise SDKException('Client', '102', o_str)
                    else:
                        self.refresh()
                        return self.get(client_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_nas_client(self,
                    ndmp_server_clientname,
                    ndmp_server_hostname,
                    username,
                    password
                    ):

        """
        Adds new NAS client with NDMP and NetworkShare iDA

        Args:
            ndmp_server_clientname    (str)   --  new NAS client name

            ndmp_server_hostname      (str)   --  HostName for new NAS client

            username                (str)   --  NDMP user name

            password                (str)   --  NDMP password

        Returns:
                client_object     (obj)   --  client object associated with the new NAS client

        Raises:
            SDKException:
                if failed to add the client

                if response is empty

                if response is not success
        """
        password = b64encode(password.encode()).decode()
        request_json = {
            "nasTurboFSCreateReq": {
                "turboNASproperties": {
                    "osType": 3
                }
            },
            "detectNDMPSrvReq": {
                "listenPort": 10000,
                "ndmpServerDetails": {
                    "ndmpServerHostName": ndmp_server_hostname,
                    "ndmpServerClientName": ndmp_server_clientname,
                    "ndmpCredentials": {
                        "userName": username,
                        "password": password
                    }
                },
                "detectMediaAgent": {
                    "mediaAgentId": 0,
                    "mediaAgentName": ""
                }
            },
            "createPseudoClientReq": {
                "clientInfo": {
                    "clientType": 2,
                    "nasClientProperties": {
                        "listenPort": 10000,
                        "ndmpServerDetails": {
                            "ndmpServerHostName": ndmp_server_hostname,
                            "ndmpServerClientName": ndmp_server_clientname,
                            "ndmpCredentials": {
                                "userName": username,
                                "password": password
                            }
                        },
                        "detectMediaAgent": {
                            "mediaAgentId": 0,
                            "mediaAgentName": ""
                        }
                    }
                },
                "entity": {
                    "hostName": ndmp_server_hostname,
                    "clientName": ndmp_server_clientname,
                    "clientId": 0
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
           'POST', self._ADD_NAS_CLIENT, request_json
        )

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = response.json()['errorCode']

                    if error_code != 0:
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_message)

                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(ndmp_server_clientname)

                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

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

        flag, response = self._cvpysdk_object.make_request('POST', self._ADD_CLIENT, request_json)

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(client_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_share_point_client(
            self,
            client_name,
            server_plan,
            service_type,
            index_server,
            access_nodes_list,
            **kwargs):
        """Adds a new Office 365 Share Point Pseudo Client to the Commcell.

            Args:
                client_name                 (str)   --  name of the new Sharepoint Pseudo Client

                server_plan                 (str)   --  server_plan to associate with the client

                service_type                (dict)  --  service type of Sharepoint
                                                         "ServiceType": {
                                                                    "Sharepoint Global Administrator": 4
                                                         }

                index_server                (str)   --  index server for virtual client

                access_nodes_list           (list)  --  list containing client names / client objects

            Kwargs :

                tenant_url                  (str)   --  url of sharepoint tenant

                user_username                (str)   --  username of sharepoint user

                user_password               (str)   -- password of sharepoint user

                azure_username              (str)   --  username of azure app

                azure_secret                (str)   --  secret key of azure app

                global_administrator        (str)   --  username of global administrator

                global_administrator_password (str)  -- password of global administrator

                azure_app_id            (str)       --  azure app id for sharepoint online

                azure_app_key_id        (str)       --  app key for sharepoint online

                azure_directory_id    (str)   --  azure directory id for sharepoint online


            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if index_server is not found

                    if server_plan is not found

                    if failed to add the client

                    if response is empty

                    if response is not success

        """
        if self.has_client(client_name):
            raise SDKException('Client', '102', 'Client "{0}" already exists.'.format(client_name))

        index_server_dict = {}

        if self.has_client(index_server):
            index_server_cloud = self.get(index_server)

            if index_server_cloud.agents.has_agent('big data apps'):
                index_server_dict = {
                    "mediaAgentId": int(index_server_cloud.client_id),
                    "_type_": 11,
                    "mediaAgentName": index_server_cloud.client_name
                }
        else:
            raise SDKException('IndexServers', '102')

        if self._commcell_object.plans.has_plan(server_plan):
            server_plan_object = self._commcell_object.plans.get(server_plan)
            server_plan_dict = {
                "planId": int(server_plan_object.plan_id),
                "planType": int(server_plan_object.plan_type)
            }
        else:
            raise SDKException('Storage', '102')

        member_servers = []

        for client in access_nodes_list:
            if isinstance(client, basestring):
                client = client.strip().lower()

                if self.has_client(client):
                    client_dict = {
                        "client": {
                            "clientName": client,
                            "clientId": int(self.all_clients[client]['id']),
                            "_type_": 3
                        }
                    }
                    member_servers.append(client_dict)

            elif isinstance(client, Client):
                client_dict = {
                    "client": {
                        "clientName": client.client_name,
                        "clientId": int(client.client_id),
                        "_type_": 3
                    }
                }
                member_servers.append(client_dict)

        request_json = {
            "clientInfo": {
                "clientType": 37,
                "lookupPlanInfo": False,
                "sharepointPseudoClientProperties": {
                    "sharePointVersion": 23,
                    "sharepointBackupSet": {

                    },
                    "indexServer": index_server_dict,
                    "jobResultsDir": {},
                    "primaryMemberServer": {
                        "sharePointVersion": 23
                    },
                    "spMemberServers": {
                        "memberServers": member_servers
                    }
                },
                "plan": server_plan_dict
            },
            "entity": {
                "clientName": client_name
            }

        }
        tenant_url = kwargs.get('tenant_url')
        global_administrator = kwargs.get('global_administrator')
        if tenant_url:
            azure_secret = b64encode(kwargs.get('azure_secret').encode()).decode()
            user_password = b64encode(kwargs.get('user_password').encode()).decode()

            request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"] = {
                    "tenantUrlItem": tenant_url,
                    "cloudRegion": 1,
                    "infraStructurePoolEnabled": False,
                    "serviceAccounts": {
                        "accounts": [
                            {
                                "serviceType": service_type["Sharepoint Online"],
                                "userAccount": {
                                    "password": user_password,
                                    "userName": kwargs.get('user_username')
                                }
                            },
                            {
                                "serviceType": service_type["Sharepoint Azure Storage"],
                                "userAccount": {
                                    "password": azure_secret,
                                    "userName": kwargs.get('azure_username')
                                }
                            }
                        ]
                    },
                    "office365Credentials": {
                        "userName": ""
                    },
                    "azureAppList": {
                        "azureApps": [
                            {
                                "azureDirectoryId": "",
                                "azureAppId": ""
                            }
                        ]
                    }
                }
        elif global_administrator:
            azure_app_key_id = b64encode(kwargs.get('azure_app_key_id').encode()).decode()
            global_administrator_password = b64encode(kwargs.get('global_administrator_password').encode()).decode()

            request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"] = {
                    "cloudRegion": 1,
                    "infraStructurePoolEnabled": False,
                    "serviceAccounts": {
                        "accounts": [
                            {
                                "serviceType": service_type["Sharepoint Global Administrator"],
                                "userAccount": {
                                    "userName": global_administrator,
                                    "password": global_administrator_password
                                }
                            }
                        ]
                    },
                    "office365Credentials": {},
                    "azureAppList": {
                        "azureApps": [
                            {
                                "azureAppId": kwargs.get('azure_app_id'),
                                "azureAppKeyValue": azure_app_key_id,
                                "azureDirectoryId": kwargs.get('azure_directory_id')
                            }
                        ]
                    }
                }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_SHAREPOINT_CLIENT, request_json
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

                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(client_name)

                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)

                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_splunk_client(self,
                          new_client_name,
                          password,
                          master_uri,
                          master_node,
                          user_name,
                          plan):

        """
        Adds new splunk client after clientname and plan validation

        Args:
            new_client_name       (str)   --  new splunk client name

            password              (str)   --  splunk instance password

            master_uri            (str)   --  URI for the master node

            master_node           (str)   --  master node name

            user_name             (str)   --  splunk instance username

            plan                  (str)   --  plan assocated with the new client

        Returns:
                client_object     (obj)   --  client object associated with the new splunk client

        Raises:
            SDKException:
                if failed to add the client

                if response is empty

                if response is not success
        """
        if self._commcell_object.plans.has_plan(plan):
            plan_object = self._commcell_object.plans.get(plan)
            plan_id = int(plan_object.plan_id)
            plan_type = int(plan_object.plan_type)
            plan_subtype = int(plan_object.subtype)

        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        if self._commcell_object.clients.has_client(master_node):
            client_id = int(self._commcell_object.clients.all_clients[master_node.lower()]['id'])

        else:
            raise SDKException('Client', '102', 'Provide Valid Master Client')

        request_json = {
            "clientInfo": {
                "clientType": 29,
                "distributedClusterInstanceProperties": {
                    "clusterType": 16,
                    "opType": 2,
                    "instance": {
                        "clientName": new_client_name,
                        "instanceName": new_client_name,
                        "instanceId": 0,
                        "applicationId": 64
                    },
                    "clusterConfig": {
                        "splunkConfig": {
                            "url": master_uri,
                            "primaryNode": {
                                "entity": {
                                    "clientId": client_id,
                                    "clientName": master_node
                                }
                            },
                            "splunkUser": {
                                "password": password,
                                "userName": user_name
                            }
                        }
                    }
                },
                "plan": {
                    "planSubtype": plan_subtype,
                    "planType": plan_type,
                    "planName": plan,
                    "planId": plan_id
                }
            },
            "entity": {
                "clientName": new_client_name
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_SPLUNK_CLIENT, request_json
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
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(new_client_name)

                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_exchange_client(
            self,
            client_name,
            index_server,
            clients_list,
            storage_policy,
            recall_service_url,
            job_result_dir,
            exchange_servers,
            service_accounts,
            azure_app_key_secret,
            azure_tenant_name,
            azure_app_key_id,
            environment_type):
        """Adds a new Exchange Mailbox Client to the Commcell.

            Args:
                client_name             (str)   --  name of the new Exchange Mailbox Client

                index_server            (str)   --  index server for virtual cleint

                clients_list            (list)  --  list cotaining client names / client objects,
                to associate with the Virtual Client

                storage_policy          (str)   --  storage policy to associate with the client

                recall_service_url      (str)   --  recall service for client

                job_result_dir          (str)   --  job reult directory path

                exchange_servers        (list)  --  list of exchange servers

                azure_app_key_secret    (str)   --  app secret for the Exchange online

                azure_tenant_name       (str)   --  tenant for exchange online

                azure_app_key_id        (str)   --  app key for exchange online

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

        if not isinstance(exchange_servers, list):
            raise SDKException('Client', '101')

        index_server_dict = {}
        storage_policy_dict = {}

        if self.has_client(index_server):
            index_server_cloud = self.get(index_server)

            if index_server_cloud.agents.has_agent('big data apps'):
                index_server_dict = {
                    "mediaAgentId": int(index_server_cloud.client_id),
                    "_type_": 11,
                    "mediaAgentName": index_server_cloud.client_name
                }

        if self._commcell_object.storage_policies.has_policy(storage_policy):
            storage_policy_object = self._commcell_object.storage_policies.get(storage_policy)

            storage_policy_dict = {
                "storagePolicyName": storage_policy_object.storage_policy_name,
                "storagePolicyId": int(storage_policy_object.storage_policy_id)
            }

        account_list = []
        member_servers = []

        for client in clients_list:
            if isinstance(client, basestring):
                client = client.strip().lower()

                if self.has_client(client):
                    temp_client = self.get(client)
                    client_dict = self._get_client_dict(temp_client)
                    member_servers.append(client_dict)
                    del temp_client

            elif isinstance(client, Client):
                client_dict = self._get_client_dict(client)
                member_servers.append(client_dict)

        for account in service_accounts:
            account_dict = {}
            account_dict['serviceType'] = account['ServiceType']

            user_account_dict = {}

            if account['ServiceType'] == 2:
                account_dict['exchangeAdminSmtpAddress'] = account['Username']
                user_account_dict['userName'] = ""
            else:
                user_account_dict['userName'] = account['Username']
            user_account_dict['password'] = b64encode(account['Password'].encode()).decode()
            user_account_dict['confirmPassword'] = b64encode(account['Password'].encode()).decode()
            account_dict['userAccount'] = user_account_dict

            account_list.append(account_dict)

        azure_app_key_secret = b64encode(azure_app_key_secret.encode()).decode()

        request_json = {
            "clientInfo": {
                "clientType": 25,
                "exchangeOnePassClientProperties": {
                    "recallService": recall_service_url,
                    "onePassProp": {
                        "environmentType": environment_type,
                        "azureDetails": {
                            "azureAppKeySecret": azure_app_key_secret,
                            "azureTenantName": azure_tenant_name,
                            "azureAppKeyID": azure_app_key_id
                        },
                        "servers": exchange_servers,
                        "accounts": {
                            "adminAccounts": account_list
                        }

                    },
                    "memberServers": {
                        "memberServers": member_servers
                    },
                    "indexServer": index_server_dict,
                    "dataArchiveGroup": storage_policy_dict,
                    "jobResulsDir": {
                        "path": job_result_dir
                    }
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_EXCHANGE_CLIENT, request_json
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
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()

                        return self.get(client_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_case_client(
            self,
            client_name,
            server_plan,
            dc_plan,
            hold_type):
        """Adds a new Exchange Mailbox Client to the Commcell.

            Args:
                client_name             (str)   --  name of the new Case Client

                server_plan             (str)   --  Server plan to assocaite to case

                dc_plan                (str)    --  DC plan to assocaite to case

                hold_type              (int)    --  Type of client (values: 1, 2, 3)

            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if failed to add the client

                    if response is empty

                    if response is not success

        """

        plans_list = []
        dc_plan_dict = {}
        if self._commcell_object.plans.has_plan(dc_plan):
            dc_plan_object = self._commcell_object.plans.get(dc_plan)
            dc_plan_dict = {
                "planId": int(dc_plan_object.plan_id),
                "planType": int(dc_plan_object.plan_type)
            }
            plans_list.append(dc_plan_dict)
        if self._commcell_object.plans.has_plan(server_plan):
            server_plan_object = self._commcell_object.plans.get(server_plan)
            server_plan_dict = {
                "planId": int(server_plan_object.plan_id),
                "planType": int(server_plan_object.plan_type)
            }
            plans_list.append(server_plan_dict)

        request_json = {
            "clientInfo": {
                "clientType": 36,
                "edgeDrivePseudoClientProperties": {
                    "eDiscoveryInfo": {
                        "custodians": ""
                    }
                },
                "plan": dc_plan_dict,
                "exchangeOnePassClientProperties": {
                    "backupSetTypeToCreate": hold_type
                },
                "caseManagerPseudoClientProperties": {
                    "eDiscoveryInfo": {
                        "eDiscoverySubType": 1,
                        "additionalPlans": plans_list,
                        "appTypeIds": [
                            137
                        ]
                    }
                }
            },
            "entity": {
                "clientName": client_name,
                "_type_": 3
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_EXCHANGE_CLIENT, request_json
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
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()

                        return self.get(client_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_salesforce_client(
            self, client_name, access_node,
            salesforce_options,
            db_options=None, **kwargs):
        """Adds a new Salesforce Client to the Commcell.

            Args:
                client_name          (str)    --    salesforce pseudo client name
                access_node          (str)    --    access node name

                salesforce_options   (dict)   --    salesforce options
                                                    {
                                                        "login_url": 'salesforce login url',
                                                        "consume_id": 'salesforce consumer key',
                                                        "consumer_secret": 'salesforce consumer secret',
                                                        "salesforce_user_name": 'salesforce login user',
                                                        "salesforce_user_password": 'salesforce user password',
                                                        "salesforce_user_token": 'salesforce user token'
                                                    }

                db_options           (dict)   --    database options to configure sync db
                                                    {
                                                        "db_enabled": 'True or False',
                                                        "db_type": 'SQLSERVER or POSTGRESQL',
                                                        "db_host_name": 'database hostname',
                                                        "db_instance": 'database instance name',
                                                        "db_name": 'database name',
                                                        "db_port": 'port of the database',
                                                        "db_user_name": 'database user name',
                                                        "db_user_password": 'database user password'
                                                    }

                **kwargs             (dict)   --    dict of keyword arguments as follows

                                                    instance_name           (str)   -- name of the salesforce instance
                                                    download_cache_path     (str)   -- download cache path
                                                    mutual_auth_path        (str)   -- mutual auth certificate path
                                                    storage_policy          (str)   -- storage policy
                                                    streams                 (int)   -- number of streams



            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if failed to add the client

                    if response is empty

                    if response is not success
        """

        if db_options is None:
            db_options = {'db_enabled': False}
        if self.has_client(client_name):
            raise SDKException('Client', '102', 'Client "{0}" already exists.'.format(client_name))

        salesforce_password = b64encode(salesforce_options.get('salesforce_user_password').encode()).decode()
        salesforce_consumer_secret = b64encode(
            salesforce_options.get('consumer_secret', '3951207263309722430').encode()).decode()
        salesforce_token = b64encode(salesforce_options.get('salesforce_user_token', '').encode()).decode()
        db_user_password = ""
        if db_options.get('db_enabled', False):
            db_user_password = b64encode(db_options.get('db_user_password', '').encode()).decode()

        request_json = {
            "clientInfo": {
                "clientType": 15,
                "cloudClonnectorProperties": {
                    "instanceType": 3,
                    "instance": {
                        "instance": {
                            "clientName": client_name,
                            "instanceName": kwargs.get('instance_name', 'ORG1'),
                        },
                        "cloudAppsInstance": {
                            "instanceType": 3,
                            "salesforceInstance": {
                                "enableREST": True,
                                "endpoint": salesforce_options.get('login_url', "https://login.salesforce.com"),
                                "consumerId": salesforce_options.get('consumer_id',
                                                                     '3MVG9Nc1qcZ7BbZ0Ep18pfQsltTkZtbcMG9GMQzsVHGS8268yaOqmZ1lEEakAs8Xley85RBH1xKR1.eoUu1Z4'),
                                "consumerSecret": salesforce_consumer_secret,
                                "defaultBackupsetProp": {
                                    "downloadCachePath": kwargs.get('download_cache_path', '/tmp'),
                                    "mutualAuthPath": kwargs.get('mutual_auth_path', ''),
                                    "token": salesforce_token,
                                    "userPassword": {
                                        "userName": salesforce_options.get('salesforce_user_name'),
                                        "password": salesforce_password,
                                    },
                                    "syncDatabase": {
                                        "dbEnabled": db_options.get('db_enabled', False),
                                        "dbPort": db_options.get('db_port', '1433'),
                                        "dbInstance": db_options.get('db_instance', ''),
                                        "dbName": db_options.get('db_name', kwargs.get('instance_name', 'ORG1')),
                                        "dbType": db_options.get('db_type', "SQLSERVER"),
                                        "dbHost": db_options.get('db_host_name', ''),
                                        "dbUserPassword": {
                                            "userName": db_options.get('db_user_name', ''),
                                            "password": db_user_password,

                                        },
                                    },
                                },
                            },
                            "generalCloudProperties": {
                                "numberOfBackupStreams": kwargs.get('streams', 2),
                                "proxyServers": [
                                    {
                                        "clientName": access_node
                                    }
                                ],
                                "storageDevice": {
                                    "dataBackupStoragePolicy": {
                                        "storagePolicyName": kwargs.get('storage_policy', '')
                                    },
                                },
                            },
                        },
                    },
                },
            },

            "entity": {
                "clientName": client_name
            }
        }
        self._process_add_response(request_json)

    def add_azure_client(self, client_name, access_node, azure_options):
        """
            Method to add new azure cloud client
            Args:
                client_name     (str)   -- azure client name
                access_node     (str)   -- cloud access node name
                azure_options   (dict)  -- dictionary for Azure details:
                                            Example:
                                               azure_options = {
                                                    "subscription_id": 'subscription id',
                                                    "tenant_id": 'tenant id',
                                                    "application_id": 'application id',
                                                    "password": 'application password',
                                                }
            Returns:
                object  -   instance of the Client class for this new client
            Raises:
                SDKException:
                    if None value in azure options

                    if pseudo client with same name already exists

        """

        if None in azure_options.values():
            raise SDKException(
                'Client',
                '102',
                "One of the azure parameters is none so cannot proceed with pseudo client creation")

        if self.has_client(client_name):
            raise SDKException(
                'Client', '102', 'Client "{0}" already exists.'.format(
                    client_name)
            )

        # encodes the plain text password using base64 encoding
        password = b64encode(azure_options.get("password").encode()).decode()
        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 7,
                        "azureResourceManager": {
                            "tenantId": azure_options.get("tenant_id"),
                            "serverName": client_name,
                            "subscriptionId": azure_options.get("subscription_id"),
                            "credentials": {
                                "password": password,
                                "userName": azure_options.get("application_id")
                            }
                        },
                        "associatedClients": {
                            "memberServers": [
                                {
                                    "client": {
                                        "clientName": access_node
                                    }
                                }
                            ]
                        },
                        "vmwareVendor": {
                            "vcenterHostName": client_name
                        }
                    },
                    "appTypes": [
                        {
                            "appName": "Virtual Server"
                        }
                    ]
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        self._process_add_response(request_json)

    def add_amazon_client(self, client_name, access_node, amazon_options):
        """
            Method to add new amazon cloud client
            Args:
                client_name     (str)   -- amazon client name
                access_node     (str)   -- cloud access node name
                amazon_options   (dict)  -- dictionary for Amazon details:
                                            Example:
                                               amazon_options = {
                                                    "accessKey": amazon_options.get("accessKey"),
                                                    "secretkey": amazon_options.get("secretkey")
                                                }
            Returns:
                object  -   instance of the Client class for this new client
            Raises:
                SDKException:
                    if None value in amazon options

                    if pseudo client with same name already exists

        """

        if None in amazon_options.values():
            raise SDKException(
                'Client',
                '102',
                "One of the amazon parameters is none so cannot proceed with pseudo client creation")

        if self.has_client(client_name):
            raise SDKException(
                'Client', '102', 'Client "{0}" already exists.'.format(
                    client_name)
            )

        # encodes the plain text password using base64 encoding
        secretkey = b64encode(amazon_options.get("secretkey").encode()).decode()
        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 4,
                        "amazonInstanceInfo": {
                            "accessKey": amazon_options.get("accessKey"),
                            "secretkey": secretkey,
                            "regionEndPoints": amazon_options.get("regionEndPoints", "default"),
                            "useIamRole": False,
                            "enableAdminAccount": False
                        },
                        "associatedClients": {
                            "memberServers": [
                                {
                                    "client": {
                                        "clientName": access_node
                                    }
                                }
                            ]
                        },
                        "vmwareVendor": {
                            "vcenterHostName": "default"
                        }
                    },
                    "appTypes": [
                        {
                            "appName": "Virtual Server"
                        }
                    ]
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        self._process_add_response(request_json)

    def add_google_client(self, client_name, access_node, google_options):
        """
            Method to add new google cloud client
            Args:
                client_name     (str)   -- google client name
                access_node     (str)   -- cloud access node name
                google_options   (dict)  -- dictionary for google details:
                                            Example:
                                               google_options = {
                                                    "serviceAccountId": google_options.get("serviceAccountId"),
                                                    "userName": google_options.get("userName"),
                                                    "password": google_options.get("password")
                                                }
            Returns:
                object  -   instance of the Client class for this new client
            Raises:
                SDKException:
                    if None value in google options

                    if pseudo client with same name already exists

        """

        if None in google_options.values():
            raise SDKException(
                'Client',
                '102',
                "One of the google parameters is none so cannot proceed with pseudo client creation")

        if self.has_client(client_name):
            raise SDKException(
                'Client', '102', 'Client "{0}" already exists.'.format(
                    client_name)
            )

        # encodes the plain text password using base64 encoding
        password = b64encode(google_options.get("password").encode()).decode()
        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 16,
                        "googleCloud": {
                            "credentials":{
                                "userName": google_options.get("userName"),
                                "password": password},
                            "serviceAccountId": google_options.get("serviceAccountId"),
                            "serverName": client_name
                        },
                        "associatedClients": {
                            "memberServers": [
                                {
                                    "client": {
                                        "clientName": access_node
                                    }
                                }
                            ]
                        },
                    },
                    "appTypes": [
                        {
                            "appName": "Virtual Server"
                        }
                    ]
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        self._process_add_response(request_json)

    def add_alicloud_client(self, client_name, access_node, alicloud_options):
        """
            Method to add new alicloud cloud client
            Args:
                client_name     (str)   -- alicloud client name
                access_node     (str)   -- cloud access node name
                alicloud_options   (dict)  -- dictionary for alicloud details:
                                            Example:
                                               alicloud_options = {
                                                    "accessKey": alicloud_options.get("accessKey"),
                                                    "secretkey": alicloud_options.get("secretkey")
                                                }
            Returns:
                object  -   instance of the Client class for this new client
            Raises:
                SDKException:
                    if None value in alicloud options

                    if pseudo client with same name already exists

        """

        if None in alicloud_options.values():
            raise SDKException(
                'Client',
                '102',
                "One of the alicloud parameters is none so cannot proceed with pseudo client creation")

        if self.has_client(client_name):
            raise SDKException(
                'Client', '102', 'Client "{0}" already exists.'.format(
                    client_name)
            )

        # encodes the plain text password using base64 encoding
        secretkey = b64encode(alicloud_options.get("secretkey").encode()).decode()
        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 18,
                        "aliBabaCloud": {
                            "accessKey": alicloud_options.get("accessKey"),
                            "secretkey": secretkey
                        },
                        "associatedClients": {
                            "memberServers": [
                                {
                                    "client": {
                                        "clientName": access_node
                                    }
                                }
                            ]
                        },
                        "vmwareVendor": {
                            "vcenterHostName": client_name
                        }
                    },
                    "appTypes": [
                        {
                            "appName": "Virtual Server"
                        }
                    ]
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        self._process_add_response(request_json)

    def add_onedrive_client(self,
                            client_name,
                            instance_name,
                            server_plan,
                            connection_details,
                            access_node=None,
                            auto_discovery=False
                            ):

        """Adds a new OneDrive Client to the Commcell.

            Args:
                client_name             (str)   --  name of the new Exchange Mailbox Client

                server_plan            (str)   --  name of the server plan to be associated
                                                   with the client

                connection_details   (dict)  -- dictionary for Azure App details:
                                            Example:
                                               connection_details = {
                                                    "azure_directory_id": 'azure directory id',
                                                    "application_id": 'application id',
                                                    "application_key_value": 'application key value',
                                                }

                access_node          (str)   --  name of the access node

                auto_discovery      (bool)   --  Enable/Disable (True/False)

            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if server plan  donot exists with the given name

                    if access node  donot exists with the given name

                    if failed to add the client

                    if response is empty

                    if response is not success

                """

        if self.has_client(client_name):
            raise SDKException('Client', '102', 'Client "{0}" already exists.'.format(client_name))

        if self._commcell_object.plans.has_plan(server_plan):
            server_plan_object = self._commcell_object.plans.get(server_plan)
            server_plan_id = int(server_plan_object.plan_id)
        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        application_key_value = b64encode(connection_details.get("application_key_value").encode()).decode()

        request_json = {
            "clientInfo": {
                "clientType": 15,
                "lookupPlanInfo": False,
                "plan": {
                    "planId": server_plan_id
                },
                "cloudClonnectorProperties": {
                    "instanceType": 7,
                    "instance": {
                        "instance": {
                            "clientName": client_name,
                            "instanceName": instance_name
                        },
                        "cloudAppsInstance": {
                            "instanceType": 7,
                            "oneDriveInstance": {
                                "manageContentAutomatically": False,
                                "createAdditionalSubclients": False,
                                "numberofAdditionalSubclients": 0,
                                "cloudRegion": 1,
                                "clientSecret": application_key_value,
                                "callbackUrl": "",
                                "tenant": connection_details.get("azure_directory_id"),
                                "clientId": connection_details.get("application_id"),
                                "isAutoDiscoveryEnabled": auto_discovery,
                                "isEnterprise": True,
                                "serviceAccounts": {},
                                "azureAppList": {}
                            },
                            "generalCloudProperties": {
                                "numberOfBackupStreams": 10,
                                "jobResultsDir": {
                                    "path": ""
                                }
                            }
                        }
                    }
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        end_point = self._services['STORAGE_POLICY_INFRASTRUCTUREPOOL'] % (server_plan_id)
        flag, response = self._cvpysdk_object.make_request('GET', end_point)

        cloud_props = request_json.get('clientInfo').get('cloudClonnectorProperties').get('instance').get(
            'cloudAppsInstance')

        if flag:
            if response and response.json():
                onedrive_prop = cloud_props.get('oneDriveInstance')
                if 'isConfigured' in response.json():
                    if response.json()['isConfigured']:
                        onedrive_prop['infraStructurePoolEnabled'] = True
                    else:
                        onedrive_prop['infraStructurePoolEnabled'] = False
                        if isinstance(access_node, basestring):
                            proxy_servers = []
                            access_node = access_node.strip().lower()
                            if self.has_client(access_node):
                                access_node_dict = {
                                    "hostName": self.all_clients[access_node]['hostname'],
                                    "clientId": int(self.all_clients[access_node]['id']),
                                    "clientName": access_node,
                                    "displayName": access_node,
                                    "_type_": 3
                                }
                                proxy_servers.append(access_node_dict)
                                general_cloud_props = cloud_props['generalCloudProperties']
                                general_cloud_props["proxyServers"] = proxy_servers
                            else:
                                raise SDKException('Client', '101', 'Provide Valid Access Node')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_ONEDRIVE_CLIENT, request_json)

        if flag:
            if response and response.json():
                if 'response' in response.json():
                    error_code = response.json().get('response').get('errorCode')
                    if error_code != 0:
                        error_string = response.json().get('response').get('errorString')
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(client_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json().get('errorMessage')
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_nutanix_files_client(self, client_name, array_name, cifs_option=True, nfs_option=True):
        """
            Method to add new Nutanix Files client

            Args:
                client_name     (str)   --  Nutanix files client name
                array_name      (str)   --  FQDN of the Nutanix array(File Server)
                                            to be associated with client
                cifs_option     (bool)  --  option for adding Windows File System agent in
                                            the created client i.e for adding CIFS agent
                nfs_option      (bool)  --  option for adding Linux File System agent in
                                            the created client  i.e for adding NFS agent

            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if nfs_option and cifs_option both are false

                    if pseudo client with same name already exists
        """

        if self.has_client(client_name):
            raise SDKException(
                'Client', '102', 'Client "{0}" already exists.'.format(
                    client_name)
            )
        if (nfs_option == cifs_option == False):
            raise SDKException(
                'Client',
                '102',
                "nfs_option and cifs_option both cannot be false")

        request_json = {
                        "createPseudoClientRequest": {
                            "clientInfo": {
                                "fileServerInfo": {
                                    "arrayName": array_name,
                                    "arrayId": 0
                                    },
                                "clientAppType":2,
                                "clientType": 18,
                                },
                            "entity": {
                                "clientName": client_name
                                }
                            }
                        }

        if(nfs_option != cifs_option):
            additional_json = {}
            if(nfs_option):
                additional_json['osType'] = 'CLIENT_PLATFORM_OSTYPE_UNIX'
            else:
                additional_json['osType'] = 'CLIENT_PLATFORM_OSTYPE_WINDOWS'
            request_json["createPseudoClientRequest"]['clientInfo']['nonNDMPClientProperties'] = additional_json

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_NUTANIX_CLIENT, request_json)

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()

                        return self.get(client_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get(self, name):
        """Returns a client object if client name or host name or ID matches the client attribute
            We check if specified name matches any of the existing client names else
            compare specified name with host names of existing clients else if name matches with the ID

            Args:
                name (str/int)  --  name / hostname / ID of the client

            Returns:
                object - instance of the Client class for the given client name

            Raises:
                SDKException:
                    if type of the client name argument is not string or Int

                    if no client exists with the given name
        """
        if isinstance(name, basestring):
            name = name.lower()
            client_name = None
            client_id = None

            if self.has_client(name):
                client_from_hostname = self._get_client_from_hostname(name)
            elif self.has_hidden_client(name):
                client_from_hostname = self._get_hidden_client_from_hostname(name)
            else:
                raise SDKException(
                    'Client', '102', 'No client exists with given name/hostname: {0}'.format(name)
                )

            client_name = name if client_from_hostname is None else client_from_hostname

            try:
                client_id = self.all_clients[client_name]['id']
            except KeyError:
                client_id = self.hidden_clients[client_name]['id']

            return Client(self._commcell_object, client_name, client_id)

        elif isinstance(name, int):
            name = str(name)
            client_name = [client_name for client_name in self.all_clients
                           if name in self.all_clients[client_name].values()]

            if client_name:
                return self.get(client_name[0])
            raise SDKException('Client', '102', 'No client exists with the given ID: {0}'.format(name))

        raise SDKException('Client', '101')

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
                client_id = self.all_clients[client_name]['id']
                client_delete_service = self._services['CLIENT'] % (client_id)
                client_delete_service += "?forceDelete=1"

                flag, response = self._cvpysdk_object.make_request('DELETE', client_delete_service)

                error_code = warning_code = 0

                if flag:
                    if response.json():
                        o_str = 'Failed to delete client'
                        if 'response' in response.json():
                            if response.json()['response'][0]['errorCode'] == 0:
                                # initialize the clients again
                                # so the client object has all the clients
                                self.refresh()
                            else:
                                error_message = response.json()['response'][0]['errorString']
                                o_str += '\nError: "{0}"'.format(error_message)
                                raise SDKException('Client', '102', o_str)
                        else:
                            if 'errorCode' in response.json():
                                error_code = response.json()['errorCode']

                            if 'warningCode' in response.json():
                                warning_code = response.json()['warningCode']

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
                    raise SDKException('Response', '101', self._update_response_(response.text))
            else:
                raise SDKException(
                    'Client', '102', 'No client exists with name: {0}'.format(client_name)
                )

    def refresh(self):
        """Refresh the clients associated with the Commcell."""
        self._clients = self._get_clients()
        self._hidden_clients = self._get_hidden_clients()
        self._virtualization_clients = self._get_virtualization_clients()
        self._office_365_clients = None


class Client(object):
    """Class for performing client operations for a specific client."""

    def __init__(self, commcell_object, client_name, client_id=None):
        """Initialise the Client class instance.

            Args:
                commcell_object (object)     --  instance of the Commcell class

                client_name     (str)        --  name of the client

                client_id       (str)        --  id of the client
                    default: None

            Returns:
                object - instance of the Client class
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._client_name = client_name.lower()

        if client_id:
            self._client_id = str(client_id)
        else:
            self._client_id = self._get_client_id()

        _client_type = {
            'Client': 0,
            'Hidden Client': 1
        }

        if self._commcell_object.clients.has_client(client_name):
            self._client_type_id = _client_type['Client']
        else:
            self._client_type_id = _client_type['Hidden Client']

        self._CLIENT = self._services['CLIENT'] % (self.client_id)

        self._instance = None

        self._agents = None
        self._schedules = None
        self._users = None
        self._network = None
        self._network_throttle = None
        self._association_object = None

        self._properties = None

        self._os_info = None
        self._install_directory = None
        self._version = None
        self._service_pack = None
        self._client_owners = None
        self._is_backup_enabled = None
        self._is_ci_enabled = None
        self._is_data_aging_enabled = None
        self._is_data_management_enabled = None
        self._is_data_recovery_enabled = None
        self._is_intelli_snap_enabled = None
        self._is_restore_enabled = None
        self._client_hostname = None
        self._job_results_directory = None
        self._log_directory = None
        self._license_info = None
        self._cvd_port = None
        self._job_start_time = None
        self._timezone = None

        self._readiness = None

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Client class instance for Client: "{0}"'
        return representation_string.format(self.client_name)

    def _get_client_id(self):
        """Gets the client id associated with this client.

            Returns:
                str - id associated with this client
        """
        return self._commcell_object.clients.get(self.client_name).client_id

    def _get_client_properties(self):
        """Gets the client properties of this client.

            Returns:
                dict - dictionary consisting of the properties of this client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._CLIENT)

        if flag:
            if response.json() and 'clientProperties' in response.json():
                self._properties = response.json()['clientProperties'][0]

                os_info = self._properties['client']['osInfo']
                processor_type = os_info['OsDisplayInfo']['ProcessorType']
                os_name = os_info['OsDisplayInfo']['OSName']
                self._cvd_port = self._properties['client']['cvdPort']
                self._os_info = '{0} {1} {2}  --  {3}'.format(
                    processor_type,
                    os_info['Type'],
                    os_info['SubType'],
                    os_name
                )

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

                self._timezone = self._properties['client']['TimeZone']['TimeZoneName']

                self._is_intelli_snap_enabled = bool(client_props['EnableSnapBackups'])

                if 'installDirectory' in self._properties['client']:
                    self._install_directory = self._properties['client']['installDirectory']

                if 'jobResulsDir' in self._properties['client']:
                    self._job_results_directory = self._properties['client'][
                        'jobResulsDir']['path']

                if 'GalaxyRelease' in self._properties['client']['versionInfo']:
                    self._version = self._properties['client'][
                        'versionInfo']['GalaxyRelease']['ReleaseString']

                if 'version' in self._properties['client']['versionInfo']:
                    service_pack = re.findall(
                        r'[ServicePack|FeatureRelease]:([\d]*)',
                        self._properties['client']['versionInfo']['version']
                    )

                    if service_pack:
                        self._service_pack = service_pack[0]

                if 'clientSecurity' in client_props:
                    self._client_owners = client_props['clientSecurity'].get('clientOwners')

                if 'jobStartTime' in client_props:
                    self._job_start_time = client_props['jobStartTime']

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _request_json(self, option, enable=True, enable_time=None, job_start_time=None, **kwargs):
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
                                "TimeZoneName": kwargs.get("timezone", self._commcell_object.default_timezone),
                                "timeValue": enable_time
                            }
                        }]
                    }
                }
            }
        }

        if enable_time:
            return request_json2

        if job_start_time is not None:
            request_json1['clientProperties']['clientProps']['jobStartTime'] = job_start_time

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

    def _make_request(self,
                      upload_url,
                      file_contents,
                      headers,
                      request_id=None,
                      chunk_offset=None):
        """Makes the request to the server to upload the specified file contents on the
            client machine

            Args:
                upload_url      (str)   --  request url on which the request is to be done

                file_contents   (str)   --  data from the file which is to be copied

                headers         (str)   --  request headers for this api

                request_id      (int)   --  request id received from the first upload request.
                                                request id is used to uniquely identify
                                                chunks of data
                    default: None

                chunk_offset    (int)   --  number of bytes written till previous upload request.
                                                chunk_offset is used to specify from where to
                                                write data on specified file
                    default: None

            Returns:
                (int, int)  -   request id and chunk_offset returned from the response

            Raises:
                SDKException:
                    if failed to upload the file

                    if response is empty

                    if response is not success
        """
        if request_id is not None:
            upload_url += '&requestId={0}'.format(request_id)

        flag, response = self._cvpysdk_object.make_request(
            'POST', upload_url, file_contents, headers=headers
        )

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json()['errorCode'])

                    if error_code != 0:
                        error_string = response.json()['errorString']
                        raise SDKException(
                            'Client', '102', 'Failed to upload file with error: {0}'.format(
                                error_string
                            )
                        )

                if 'requestId' in response.json():
                    request_id = response.json()['requestId']

                if 'chunkOffset' in response.json():
                    chunk_offset = response.json()['chunkOffset']

                return request_id, chunk_offset

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_instance_of_client(self):
        """Gets the instance associated with this client.

            Returns:
                str     -   instance on which the client is installed

                    e.g.;   Instance001

            Raises:
                SDKException:
                    if failed to get the value of instance

                    if operation is not supported for the client OS

        """
        if 'windows' in self.os_info.lower():
            command = 'powershell.exe Get-Content "{0}"'.format(
                os.path.join(self.install_directory, 'Base', 'QinetixVM').replace(" ", "' '")
            )

            exit_code, output, __ = self.execute_command(command)

            if exit_code == 0:
                return output.strip()
            else:
                raise SDKException('Client', '106', 'Error: {0}'.format(output))

        elif 'unix' in self.os_info.lower():
            command = 'cat {0}'.format(os.path.join(self.install_directory + '/', 'galaxy_vm'))

            __, output, error = self.execute_command(command)

            if error:
                raise SDKException('Client', '106', 'Error: {0}'.format(error))
            else:
                temp = re.findall('GALAXY_INST="(.+?)";', output)

                if temp:
                    return temp[0]
                else:
                    raise SDKException('Client', '106')

        else:
            raise SDKException('Client', '109')

    def _get_log_directory(self):
        """Gets the path of the log directory on the client.

            Returns:
                str     -   path of the log directory on the client

                    e.g.;

                        -   ..\\\\ContentStore\\\\Log Files

                        -   ../commvault/Log_Files

            Raises:
                SDKException:
                    if failed to get the value of log directory path

                    if operation is not supported for the client OS

        """
        if 'windows' in self.os_info.lower():
            key = r'HKLM:\SOFTWARE\CommVault Systems\Galaxy\{0}\EventManager'.format(self.instance)

            exit_code, output, __ = self.execute_script(
                'PowerShell',
                '(Get-ItemProperty -Path {0}).dEVLOGDIR'.format(key.replace(" ", "' '"))
            )

            if exit_code == 0:
                return output.strip()
            else:
                raise SDKException('Client', '108', 'Error: {0}'.format(output.strip()))

        elif 'unix' in self.os_info.lower():
            script = r"""
            FILE=/etc/CommVaultRegistry/Galaxy/%s/EventManager/.properties
            KEY=dEVLOGDIR

            get_registry_value()
            {
                cat $1 | while read line
                do
                    key=`echo $line | cut -d' ' -f1`
                    if [ "$key" = "$2" ]; then
                        echo $line | awk '{print $2}'
                        break
                    fi
                done
            }

            echo `get_registry_value $FILE $KEY`
            """ % self.instance

            __, output, error = self.execute_script('UnixShell', script)

            if error:
                raise SDKException('Client', '106', 'Error: {0}'.format(error.strip()))
            else:
                return output.strip()

        else:
            raise SDKException('Client', '109')

    def _service_operations(self, service_name=None, operation=None):
        """Executes the command on the client machine to start / stop / restart a
            Commvault service, or ALL services.

            Args:
                service_name        (str)   --  name of the service to be operated on

                    default:    None

                operation           (str)   --  name of the operation to be done

                    Valid Values are:

                        -   START

                        -   STOP

                        -   RESTART

                        -   RESTART_SVC_GRP     **Only available for Windows Clients**

                    default:    None

                    for None as the input, we will run **RESTART_SVC_GRP** operation

            Returns:
                None    -   if the operation was performed successfully

        """
        operations_dict = {
            'START': {
                'windows_command': 'startsvc',
                'unix_command': 'start',
                'exception_message': 'Failed to start "{0}" service.\n Error: "{1}"'
            },
            'STOP': {
                'windows_command': 'stopsvc',
                'unix_command': 'stop',
                'exception_message': 'Failed to stop "{0}" service.\n Error: "{1}"'
            },
            'RESTART': {
                'windows_command': 'restartsvc',
                'unix_command': 'restart',
                'exception_message': 'Failed to restart "{0}" service.\n Error: "{1}"'
            },
            'RESTART_SVC_GRP': {
                'windows_command': 'restartsvcgrp',
                'unix_command': 'restart',
                'exception_message': 'Failed to restart "{0}" services.\n Error: "{1}"'
            }
        }

        operation = operation.upper() if operation else 'RESTART_SVC_GRP'

        if operation not in operations_dict:
            raise SDKException('Client', '109')

        if not service_name:
            service_name = 'ALL'

        if 'windows' in self.os_info.lower():
            command = '"{0}" -consoleMode -{1} {2}'.format(
                '\\'.join([self.install_directory, 'Base', 'GxAdmin.exe']),
                operations_dict[operation]['windows_command'],
                service_name
            )

            __, output, __ = self.execute_command(command, wait_for_completion=False)

            if output:
                raise SDKException(
                    'Client',
                    '102',
                    operations_dict[operation]['exception_message'].format(service_name, output)
                )
        elif 'unix' in self.os_info.lower():
            commvault = r'/usr/bin/commvault'
            if 'darwin' in self.os_info.lower():
                commvault = r'/usr/local/bin/commvault'

            if self.instance:
                command = '{0} -instance {1} {2}'.format(
                    commvault, self.instance, operations_dict[operation]['unix_command']
                )

                __, __, error = self.execute_command(command, wait_for_completion=False)

                if error:
                    raise SDKException(
                        'Client', '102', 'Failed to {0} services.\nError: {1}'.format(
                            operations_dict[operation]['unix_command'],
                            error
                        )
                    )
            else:
                raise SDKException('Client', '109')
        else:
            raise SDKException('Client', '109')

    def _process_update_request(self, request_json):
        """Runs the Client update API

            Args:
                request_json    (dict)  -- request json sent as payload

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )
        if flag:
            if response.json():
                if 'response' in response.json():
                    if response.json()['response'][0].get('errorCode', 0):
                        error_message = response.json()['response'][0].get('errorMessage')
                        if not error_message:
                            error_message = response.json()['response'][0].get('errorString', '')

                        o_str = 'Failed to set property\nError: "{0}"'.format(error_message)
                        raise SDKException('Client', '102', o_str)
                    self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def update_properties(self, properties_dict):
        """Updates the client properties

            Args:
                properties_dict (dict)  --  client property dict which is to be updated

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
            "clientProperties": {},
            "association": {
                "entity": [
                    {
                        "clientName": self.client_name
                    }
                ]
            }
        }

        request_json['clientProperties'].update(properties_dict)
        self._process_update_request(request_json)

    @property
    def properties(self):
        """Returns the client properties"""
        return copy.deepcopy(self._properties)

    @property
    def name(self):
        """Returns the Client name"""
        return self._properties['client']['clientEntity']['clientName']

    @property
    def display_name(self):
        """Returns the Client display name"""
        return self._properties['client']['displayName']

    @display_name.setter
    def display_name(self, display_name):
        """setter to set the display name of the client

        Args:
            display_name    (str)   -- Display name to be set for the client

        """
        update_properties = self.properties
        update_properties['client']['displayName'] = display_name
        self.update_properties(update_properties)

    @property
    def description(self):
        """Returns the Client description"""
        return self._properties.get('client', {}).get('clientDescription')

    @description.setter
    def description(self, description):
        """setter to set the display name of the client

        Args:
            description    (str)   -- description to be set for the client

        """
        update_properties = self.properties
        update_properties['client']['clientDescription'] = description
        self.update_properties(update_properties)

    @property
    def timezone(self):
        """Returns the timezone of the client"""
        return self._timezone

    @timezone.setter
    def timezone(self, timezone=None):
        """Setter to set the timezone of the client

        Args:
            timezone    (str)   -- timezone to be set for the client

        **Note** make use of TIMEZONES dict in constants.py to set timezone

        """
        update_properties = self.properties
        update_properties['client']['TimeZone']['TimeZoneName'] = timezone
        update_properties['client']['timezoneSetByUser'] = True
        self.update_properties(update_properties)

    @property
    def commcell_name(self):
        """Returns the Client's commcell name"""
        return self._properties['client']['clientEntity']['commCellName']

    @property
    def name_change(self):
        """Returns an instance of Namechange class"""
        return NameChange(self)

    @property
    def _security_association(self):
        """Returns the security association object"""
        if self._association_object is None:
            from .security.security_association import SecurityAssociation
            self._association_object = SecurityAssociation(self._commcell_object, self)

        return self._association_object

    @property
    def available_security_roles(self):
        """Returns the list of available security roles"""
        return self._security_association.__str__()

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

    @property
    def owners(self):
        """Treats the client owners as a read-only attribute."""
        return self._client_owners

    @property
    def job_results_directory(self):
        """Treats the job_results_directory pack as a read-only attribute."""
        return self._job_results_directory

    @property
    def instance(self):
        """Returns the value of the instance the client is installed on."""
        if self._instance is None:
            try:
                self._instance = self._get_instance_of_client()
            except SDKException:
                # pass silently if failed to get the value of instance
                pass

        return self._instance

    @property
    def log_directory(self):
        """Returns the path of the log directory on the client."""
        if self._log_directory is None:
            try:
                self._log_directory = self._get_log_directory()
            except SDKException:
                # pass silently if failed to get the value of the log directory
                pass

        return self._log_directory

    @property
    def agents(self):
        """Returns the instance of the Agents class representing the list of Agents
        installed / configured on the Client.
        """
        if self._agents is None:
            self._agents = Agents(self)

        return self._agents

    @property
    def schedules(self):
        """Returns the instance of the Schedules class representing the Schedules
        configured on the Client.
        """
        if self._schedules is None:
            self._schedules = Schedules(self)

        return self._schedules

    @property
    def users(self):
        """Returns the instance of the Users class representing the list of Users
        with permissions set on the Client.
        """
        if self._users is None:
            self._users = Users(self._commcell_object)

        return self._users

    @property
    def network(self):
        """Returns the object of Network class"""
        if self._network is None:
            self._network = Network(self)

        return self._network

    @property
    def network_throttle(self):
        """Returns the object of NetworkThrottle class"""
        if self._network_throttle is None:
            self._network_throttle = NetworkThrottle(self)

        return self._network_throttle

    @property
    def is_cluster(self):
        """Returns True if the client is of cluster type"""
        return 'clusterGroupAssociation' in self._properties['clusterClientProperties']

    def enable_backup(self):
        """Enable Backup for this Client.

            Raises:
                SDKException:
                    if failed to enable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json('Backup')

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_backup_at_time(self, enable_time, **kwargs):
        """Disables Backup if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  Time to enable the backup at, in 24 Hour format
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

        request_json = self._request_json('Backup', False, enable_time, **kwargs)

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def disable_backup(self):
        """Disables Backup for this Client.

            Raises:
                SDKException:
                    if failed to disable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json('Backup', False)

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_restore(self):
        """Enable Restore for this Client.

            Raises:
                SDKException:
                    if failed to enable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json('Restore')

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_restore_at_time(self, enable_time, **kwargs):
        """Disables Restore if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  Time to enable the restore at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

                **kwargs (dict)  -- dict of keyword arguments as follows

                    timezone    (str)   -- timezone to be used of the operation

                        **Note** make use of TIMEZONES dict in constants.py to pass timezone

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

        request_json = self._request_json('Restore', False, enable_time, **kwargs)

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def disable_restore(self):
        """Disables Restore for this Client.

            Raises:
                SDKException:
                    if failed to disable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json('Restore', False)

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_data_aging(self):
        """Enable Data Aging for this Client.

            Raises:
                SDKException:
                    if failed to enable data aging

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json('Data Aging')

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_data_aging_at_time(self, enable_time, **kwargs):
        """Disables Data Aging if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  Time to enable the data aging at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

                **kwargs (dict)  -- dict of keyword arguments as follows

                    timezone    (str)   -- timezone to be used of the operation

                        **Note** make use of TIMEZONES dict in constants.py to pass timezone

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

        request_json = self._request_json('Data Aging', False, enable_time, **kwargs)

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def disable_data_aging(self):
        """Disables Data Aging for this Client.

            Raises:
                SDKException:
                    if failed to disable data aging

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json('Data Aging', False)

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

    def execute_script(self, script_type, script, script_arguments=None, wait_for_completion=True):
        """Executes the given script of the script type on this client.

            **Only scripts of text format are supported**, i.e., the scripts should not have
            any binary/bytes content

            Args:
                script_type             (str)   --  type of script to be executed on the client

                    Script Types Supported:

                        JAVA

                        Python

                        PowerShell

                        WindowsBatch

                        UnixShell

                script                  (str)   --  path of the script to be executed on the client

                script_arguments        (str)   --  arguments to the script

                    default: None

                wait_for_completion     (bool)  --  boolean specifying whether to wait for the
                script execution to finish or not

                    default: True

            Returns:
                    (int, str, str)

                int     -   exit code returned from executing the script on the client

                    default: -1     (exit code not returned in the response)

                str     -   output returned from executing the script on the client

                    default: ''     (output not returned in the response)

                str     -   error returned from executing the script on the client

                    default: ''     (error not returned in the response)

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

        import html

        if os.path.isfile(script):
            with open(script, 'r') as temp_file:
                script = html.escape(temp_file.read())
        else:
            script = html.escape(script)

        script_lines = ""
        script_lines_template = '<scriptLines val="{0}"/>'

        for line in script.split('\n'):
            script_lines += script_lines_template.format(line)

        script_arguments = '' if script_arguments is None else script_arguments
        script_arguments = html.escape(script_arguments)

        xml_execute_script = """
        <App_ExecuteCommandReq arguments="{0}" scriptType="{1}" waitForProcessCompletion="{5}">
            <client clientId="{2}" clientName="{3}"/>
            "{4}"
        </App_ExecuteCommandReq>
        """.format(
            script_arguments,
            script_types[script_type.lower()],
            self.client_id,
            self.client_name,
            script_lines,
            1 if wait_for_completion else 0
        )

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], xml_execute_script
        )

        if flag:
            if response.json():
                exit_code = -1
                output = ''
                error_message = ''

                if 'processExitCode' in response.json():
                    exit_code = response.json()['processExitCode']

                if 'commandLineOutput' in response.json():
                    output = response.json()['commandLineOutput']

                if 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']

                return exit_code, output, error_message
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def execute_command(self, command, script_arguments=None, wait_for_completion=True):
        """Executes a command on this client.

            Args:
                command                 (str)   --  command in string to be executed on the client

                script_arguments        (str)   --  arguments to the script

                    default: None

                wait_for_completion     (bool)  --  boolean specifying whether to wait for the
                script execution to finish or not

                    default: True

            Returns:
                    (int, str, str)

                int     -   exit code returned from executing the command on the client

                    default: -1     (exit code not returned in the response)

                str     -   output returned from executing the command on the client

                    default: ''     (output not returned in the response)

                str     -   error returned from executing the command on the client

                    default: ''     (error not returned in the response)

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

        script_arguments = '' if script_arguments is None else script_arguments
        script_arguments = html.escape(script_arguments)

        xml_execute_command = """
        <App_ExecuteCommandReq arguments="{0}" command="{1}" waitForProcessCompletion="{4}">
            <processinginstructioninfo>
                <formatFlags continueOnError="1" elementBased="1" filterUnInitializedFields="0" formatted="0" ignoreUnknownTags="1" skipIdToNameConversion="0" skipNameToIdConversion="0"/>
            </processinginstructioninfo>
            <client clientId="{2}" clientName="{3}"/>
        </App_ExecuteCommandReq>
        """.format(
            script_arguments,
            command,
            self.client_id,
            self.client_name,
            1 if wait_for_completion else 0
        )

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], xml_execute_command
        )

        if flag:
            if response.json():
                exit_code = -1
                output = ''
                error_message = ''

                if 'processExitCode' in response.json():
                    exit_code = response.json()['processExitCode']

                if 'commandLineOutput' in response.json():
                    output = response.json()['commandLineOutput']

                if 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']

                return exit_code, output, error_message
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

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

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

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

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

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
            raise SDKException('Response', '101', self._update_response_(response.text))

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
        return self.readiness_details.is_ready()

    def upload_file(self, source_file_path, destination_folder):
        """Upload the specified source file to destination path on the client machine

            Args:
                source_file_path    (str)   --  path on the controller machine

                destination_folder  (str)   --  path on the client machine where the files
                                                    are to be copied

            Raises:
                SDKException:
                    if failed to upload the file

                    if response is empty

                    if response is not success

        """
        chunk_size = 1024 ** 2 * 2
        request_id = None
        chunk_offset = None

        file_name = os.path.split(source_file_path)[-1]

        file_size = os.path.getsize(source_file_path)
        headers = {
            'Authtoken': self._commcell_object._headers['Authtoken'],
            'Accept': 'application/json',
            'FileName': b64encode(file_name.encode('utf-8')),
            'FileSize': str(file_size),
            'ParentFolderPath': b64encode(destination_folder.encode('utf-8'))
        }

        file_stream = open(source_file_path, 'rb')

        if file_size <= chunk_size:
            upload_url = self._services['UPLOAD_FULL_FILE'] % (self.client_id)
            self._make_request(upload_url, file_stream.read(), headers)
        else:
            upload_url = self._services['UPLOAD_CHUNKED_FILE'] % (self.client_id)
            while file_size > chunk_size:
                file_size = file_size - chunk_size
                headers['FileEOF'] = str(0)
                request_id, chunk_offset = self._make_request(
                    upload_url, file_stream.read(chunk_size), headers, request_id, chunk_offset
                )

            headers['FileEOF'] = str(1)
            self._make_request(
                upload_url, file_stream.read(file_size), headers, request_id, chunk_offset
            )

    def upload_folder(self, source_dir, destination_dir):
        """Uploads the specified source dir to destination path on the client machine

            Args:
                source_dir          (str)   --  path on the controller machine

                destination_dir     (str)   --  path on the client machine where the files
                                                    are to be copied

            Raises:
                SDKException:
                    if failed to upload the file

                    if response is empty

                    if response is not success
        """

        def _create_destination_path(base_path, *args):
            """Returns the path obtained by joining the items in argument

                The final path to be generated is done based on the operating system path
            """
            if 'windows' in self.os_info.lower():
                delimiter = "\\"
            else:
                delimiter = "/"

            if args:
                for argv in args:
                    base_path = "{0}{1}{2}".format(base_path, delimiter, argv)

            return base_path

        source_list = os.listdir(source_dir)

        destination_dir = _create_destination_path(destination_dir, os.path.split(source_dir)[-1])

        for item in source_list:
            item = os.path.join(source_dir, item)
            if os.path.isfile(item):
                self.upload_file(item, destination_dir)
            else:
                self.upload_folder(item, destination_dir)

    def start_service(self, service_name=None):
        """Executes the command on the client machine to start the Commvault service(s).

            Args:
                service_name    (str)   --  name of the service to be started

                    service name is required only for Windows Clients, as for UNIX clients, the
                    operation is executed on all services

                    default:    None

                    Example:    GxVssProv(Instance001)

            Returns:
                None    -   if the service was started successfully

            Raises:
                SDKException:
                    if failed to start the service

        """
        return self._service_operations(service_name, 'START')

    def stop_service(self, service_name=None):
        """Executes the command on the client machine to stop the Commvault service(s).

            Args:
                service_name    (str)   --  name of the service to be stopped

                    service name is required only for Windows Clients, as for UNIX clients, the
                    operation is executed on all services

                    default:    None

                    Example:    GxVssProv(Instance001)

            Returns:
                None    -   if the service was stopped successfully

            Raises:
                SDKException:
                    if failed to stop the service

        """
        return self._service_operations(service_name, 'STOP')

    def restart_service(self, service_name=None):
        """Executes the command on the client machine to restart the Commvault service(s).

            Args:
                service_name    (str)   --  name of the service to be restarted

                    service name is required only for Windows Clients, as for UNIX clients, the
                    operation is executed on all services

                    default:    None

                    Example:    GxVssProv(Instance001)

            Returns:
                None    -   if the service was restarted successfully

            Raises:
                SDKException:
                    if failed to restart the service

        """
        return self._service_operations(service_name, 'RESTART')

    def restart_services(self, wait_for_service_restart=True, timeout=10):
        """Executes the command on the client machine to restart **ALL** services.

            Args:
                wait_for_service_restart    (bool)  --  boolean to specify whether to wait for the
                services to restart, or just execute the command and exit

                    if set to True, the method will wait till the services of the client are up

                    otherwise, the method will trigger a service restart, and exit

                    default: True

                timeout                     (int)   --  timeout **(in minutes)** to wait for the
                services to restart

                    if the services are not restarted by the timeout value, the method will exit
                    out with Exception

                    default: 10

            Returns:
                None    -   if the services were restarted sucessfully

            Raises:
                SDKException:
                    if failed to restart the services before the timeout value

        """
        self._service_operations('ALL', 'RESTART_SVC_GRP')

        if wait_for_service_restart:
            start_time = time.time()
            timeout = timeout * 60

            while time.time() - start_time < timeout:
                try:
                    if self.is_ready:
                        return
                except Exception:
                    continue

                time.sleep(5)

            raise SDKException('Client', '107')

    def get_network_summary(self):
        """Gets the network summary for the client

        Returns:
             str    -   Network Summary

        Raises:
            SDKException:
                    if response is not successful

        """

        flag, response = self._cvpysdk_object.make_request('GET', self._services['GET_NETWORK_SUMMARY'].replace('%s',
                                                                                                                self.client_id))
        if flag:
            if "No Network Config found" in response.text:
                return ""
            return response.text
        raise SDKException('Response', '101', self._update_response_(response.text))

    def change_exchange_job_results_directory(
            self, new_directory_path, username=None, password=None):
        """
                Change the Job Result Directory of an Exchange Online Client

                Arguments:
                    new_directory   (str)   -- The new JR directory
                        Example:
                            C:\ JR
                            or
                            <UNC-PATH>


                    username    (str)   --
                        username of the machine, if new JobResults directory is a shared/ UNC path.

                    password    (str)   --
                        Password of the machine, if new JobResults directory is a shared/ UNC path.

                Raises
                    SDKException   (object)
                        Error in moving the job results directory
        """
        if self.client_type != 25:
            raise SDKException(
                'Client', '109',
                ' Method is application for an Exchange Mailbox Client only')

        if new_directory_path.startswith(r'\\') and (
                username is None or password is None):
            raise SDKException(
                'Client', '101',
                'For a network share path, pass the credentials also')

        prop_dict = {
            "clientId": int(self.client_id),
            "appType": 137,
            "jobResultDirectory": new_directory_path
        }
        if username is not None:
            import base64
            password = base64.b64encode(password.encode()).decode()
            prop_dict["directoryAdmin"] = {
                "serviceType": 3,
                "userAccount": {
                    "userName": username,
                    "password": password
                }
            }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['OFFICE365_MOVE_JOB_RESULT_DIRECTORY'], prop_dict
        )
        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Failed to move the job results directory' \
                            '\nError: "{0}"'.format(error_message)
                    raise SDKException(
                        'Response', '101',
                        'Unable to move the job result directory' + o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                'Unable to move the job result directory')

    def push_network_config(self):
        """Performs a push network configuration on the client

                Raises:
                SDKException:
                    if input data is invalid

                    if response is empty

                    if response is not success
        """

        xml_execute_command = """
        <App_PushFirewallConfigurationRequest>
            <entity clientName="{0}"/>
        </App_PushFirewallConfigurationRequest>
        """.format(self.client_name)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], xml_execute_command
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
                    raise SDKException('Client', '102', error_message)

            else:
                raise SDKException('Response', '102')

        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_user_associations(self, associations_list):
        """Adds the users to the owners list of this client

        Args:
            associations_list   (list)  --  list of owners to be associated with this client
                Example:
                    associations_list = [
                        {
                            'user_name': user1,
                            'role_name': role1
                        },
                        {
                            'user_name': user2,
                            'role_name': role2
                        }
                    ]

            Note: You can get available roles list using self.available_security_roles

        """
        if not isinstance(associations_list, list):
            raise SDKException('Client', '101')

        self._security_association._add_security_association(associations_list, user=True)

    def add_client_owner(self, owner_list):
        """Adds the users to the owners list of this client
            Args:
                owner_list   (list)  --  list of owners to be associated with this client

             Raises:
                SDKException:
                    if input data is invalid
        """
        if not isinstance(owner_list, list):
            raise SDKException('Client', '101')
        properties_dict = self.properties
        owners, current_owners = list(), list()
        if 'owners' in properties_dict.get('clientProps', {}).get('securityAssociations', {}).get(
                'ownerAssociations', {}):
            owners = properties_dict['clientProps']['securityAssociations'][
                'ownerAssociations']['owners']
            current_owners = (o['userName'].lower() for o in owners)
        for owner in owner_list:
            if owner.lower() not in self.users.all_users:
                raise Exception("User %s is not part of commcell" % str(owner))
            if owner.lower() not in current_owners:
                owners.append({"userId": self.users.all_users[owner.lower()],
                               "userName": owner.lower()})
        if 'securityAssociations' in properties_dict['clientProps']:
            if 'ownerAssociations' in properties_dict['clientProps']['securityAssociations']:
                properties_dict['clientProps']['securityAssociations']['ownerAssociations'] = {
                    "ownersOperationType": 1, "owners": owners}
            else:
                properties_dict['clientProps']['securityAssociations'] = {'ownerAssociations': {
                    "ownersOperationType": 1, "owners": owners}}
        else:
            properties_dict['clientProps'] = {'securityAssociations': {'ownerAssociations': {
                "ownersOperationType": 1, "owners": owners}}}
        self.update_properties(properties_dict)

    def filter_clients_return_displaynames(self, filter_by="OS", **kwargs):
        """Gets all the clients associated with the commcell with properties

        Args:
            filter_by   (str)         --  filters clients based on criteria

                                            Accepted values:

                                            1. OS

            **kwargs    (str)         --  accepted optional arguments:

                                            os_type    (str)  - accepted values Windows, Unix, NAS

                                            url_params (dict) - dict of url parameters and values

                                                                Example:

                                                               {"Hiddenclients":"true"}

        Returns:

            list    -   list of clients of given os_type

        Raises:

            SDKException:

                if response is empty

                if response is not success

        """

        client_list = []
        param_string = ""

        if "url_params" in kwargs:
            for url_param, param_val in kwargs['url_params'].items():
                param_string += f"{url_param}={param_val}&"

        if "os_type" in kwargs:
            os_filter = kwargs['os_type']

        # To get the complete properties in the response
        self._commcell_object._headers["mode"] = "EdgeMode"

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['FILTER_CLIENTS'] % param_string)

        self._commcell_object._headers.pop("mode")

        if flag:
            if response.json() and 'clientProperties' in response.json():
                properties = response.json()['clientProperties']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

        if filter_by.lower() == 'os':
            for dictionary in properties:
                temp_name = dictionary['client']['clientEntity']['displayName']

                if 'idaList' in dictionary['client']:
                    ida_list = dictionary['client']['idaList']
                    for ida in ida_list:
                        os_type = ida['idaEntity']['appName']
                        if os_filter.lower() in os_type.lower():
                            client_list.append(temp_name)

        return client_list

    def refresh(self):
        """Refreshes the properties of the Client."""
        self._get_client_properties()

        if self._client_type_id == 0:
            self._agents = None
            self._schedules = None
            self._users = None
            self._network = None

    def set_encryption_property(self,
                                enc_setting="USE_SPSETTINGS",
                                key=None,
                                key_len=None):
        """updates encryption properties on client

        Args:

            enc_setting (str)   --  sets encryption level on client
                                    (USE_SPSETTINGS / OFF/ ON_CLIENT)
            default : USE_SPSETTINGS

            key         (str)   --  cipher type

            key_len     (str)   --  cipher key length

            to enable encryption    : client_object.set_encryption_property("ON_CLIENT", "TwoFish", "256")
            to disable encryption   : client_object.set_encryption_property("OFF")

        """
        client_props = self._properties['clientProps']
        if enc_setting is not None:
            client_props['encryptionSettings'] = enc_setting
            if enc_setting == "ON_CLIENT":
                if not (isinstance(key, basestring) and isinstance(key_len, basestring)):
                    raise SDKException('Client', '101')
                client_props['CipherType'] = key
                client_props['EncryptKeyLength'] = int(key_len)
        else:
            raise SDKException('Response', '102')

        request_json = self._update_client_props_json(client_props)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json)

        self._get_client_properties()

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json()['errorCode'])
                    if error_code != 0:
                        if 'errorMessage' in response.json():
                            error_message = "Failed to update client {0}.\nError: {1}".format(
                                self.client_name, response.json()['errorMessage']
                            )
                        else:
                            error_message = "Failed to update {0} client".format(
                                self.client_name
                            )

                        raise SDKException('Client', '102', error_message)
                elif 'response' in response.json():
                    error_code = int(response.json()['response'][0]['errorCode'])

                    if error_code != 0:
                        error_message = "Failed to update the client"
                        raise SDKException('Client', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def set_dedup_property(self,
                           prop_name,
                           prop_value,
                           client_side_cache=None,
                           max_cache_db=None):
        """
            Set DDB propeties

          :param prop_name:    property name
        :param prop_value:   property value
        :return:

        prop_name and prop_value:
            clientSideDeduplication values:
                USE_SPSETTINGS, to use storage policy settings
                ON_CLIENT, to enable client side deduplication
                OFF, to disable client side deduplication

                enableClientSideCache: True/False
                maxCacheDB: Valid values are:
                                1024
                                2048
                                4096
                                8192
                                16384
                                32768
                                65536
                                131072

        """
        if not (isinstance(prop_name, basestring) and isinstance(prop_value, basestring)):
            raise SDKException('Client', '101')

        if prop_name == "clientSideDeduplication" and prop_value == "ON_CLIENT":
            if client_side_cache is True and max_cache_db is not None:
                dedupe_props = {
                    'deDuplicationProperties': {
                        'clientSideDeduplication': prop_value,
                        'enableClientSideDiskCache': client_side_cache,
                        'maxCacheDb': max_cache_db
                    }
                }

            else:
                dedupe_props = {
                    'deDuplicationProperties': {
                        'clientSideDeduplication': prop_value,
                        'enableClientSideDiskCache': client_side_cache
                    }
                }

        else:
            dedupe_props = {
                'deDuplicationProperties': {
                    'clientSideDeduplication': prop_value
                }
            }

        request_json = self._update_client_props_json(dedupe_props)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json)

        self._get_client_properties()

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    error_code = int(response.json()['errorCode'])
                    if error_code != 0:
                        if 'errorMessage' in response.json():
                            error_message = "Failed to update client {0}.\nError: {1}".format(
                                self.client_name, response.json()['errorMessage']
                            )
                        else:
                            error_message = "Failed to update {0} client".format(
                                self.client_name
                            )

                        raise SDKException('Client', '102', error_message)
                elif 'response' in response.json():
                    error_code = int(response.json()['response'][0]['errorCode'])

                    if error_code != 0:
                        error_message = "Failed to update the client"
                        raise SDKException('Client', '102', error_message)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_additional_setting(self, category, key_name, data_type, value):
        """Adds registry key to the client property

            Args:
                category        (str)            --  Category of registry key

                key_name        (str)            --  Name of the registry key

                data_type       (str)            --  Data type of registry key

                    Accepted Values: BOOLEAN, INTEGER, STRING, MULTISTRING, ENCRYPTED

                value           (str)            --  Value of registry key

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected"""

        properties_dict = {
            "registryKeys": [{"deleted": 0,
                              "relativepath": category,
                              "keyName": key_name,
                              "isInheritedFromClientGroup": False,
                              "type": data_type,
                              "value": value,
                              "enabled": 1}]
        }
        request_json = self._update_client_props_json(properties_dict)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )
        if flag:
            if response.json():
                if 'response' in response.json():
                    if response.json()['response'][0].get('errorCode', 0):
                        error_message = response.json()['response'][0]['errorMessage']
                        o_str = 'Failed to add registry key\nError: "{0}"'.format(
                            error_message)
                        raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def delete_additional_setting(self, category, key_name):
        """Deletes registry key from the client property

        Args:
            category        (str)  --  Category of registry key

            key_name        (str)  --  Name of the registry key

        Raises:
            SDKException:
                if failed to delete

                if response is empty

                if response code is not as expected"""

        properties_dict = {
            "registryKeys": [{"deleted": 1,
                              "relativepath": category,
                              "keyName": key_name}]
        }
        request_json = self._update_client_props_json(properties_dict)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLIENT, request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    if response.json()['response'][0].get('errorCode', 0):
                        error_message = response.json()['response'][0]['errorMessage']
                        o_str = 'Failed to delete registry key\nError: "{0}"'.format(
                            error_message)
                        raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def release_license(self, license_name=None):
        """Releases a license from a client

        Args:

            license_name    (str)  --  Name of the license to be released.

                Releases all the licenses in the client if no value is passed.

                self.consumed_licenses() method will provide all the available

                license details along with license_name.

                default: None

        Raises:
            SDKException:
                if failed to release license

                if response is empty

                if response code is not as expected

        """
        license_type_id = 0
        app_type_id = 0
        platform_type = 1

        if license_name is not None:
            if self.consumed_licenses.get(license_name):
                license_type_id = self.consumed_licenses[license_name].get('licenseType')
                app_type_id = self.consumed_licenses[license_name].get('appType')
                platform_type = self.consumed_licenses[license_name].get('platformType')
            else:
                raise Exception(
                    "Provided license name is not configured in the client")
        request_json = {
            "licensesInfo": [{
                "platformType": platform_type,
                "license": {
                    "licenseType": license_type_id,
                    "appType": app_type_id,
                    "licenseName": license_name
                }
            }],
            "clientEntity": {
                "clientId": int(self.client_id)
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['RELEASE_LICENSE'], request_json
        )

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    if response.json()['errorCode'] != 0:
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to release license.\nError: "{0}"'.format(
                            error_message)
                        raise SDKException('Client', '102', o_str)
                    self._license_info = None
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def retire(self):
        """Uninstalls the CommVault Software on the client, releases the license and deletes the client.

        Returns:
            Job - job object of the uninstall job

        Raises:

            SDKException:

                if failed to retire client

                if response is empty

                if response code is not as expected
        """
        request_json = {
            "client": {
                "clientId": int(self.client_id),
                "clientName": self.client_name
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._services['RETIRE'] % self.client_id, request_json
        )

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']
                error_string = response.json()['response'].get('errorString', '')

                if error_code == 0:
                    if 'jobId' in response.json():
                        return Job(self._commcell_object, (response.json()['jobId']))
                else:
                    o_str = 'Failed to Retire Client. Error: "{0}"'.format(error_string)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def reconfigure_client(self):
        """Reapplies license to the client

            Raises:
                SDKException:
                    if failed to reconfigure client

                    if response is empty

                    if response code is not as expected

        """
        request_json = {
            "clientInfo": {
                "clientId": int(self.client_id)
            },
            "platformTypes": [1]
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['RECONFIGURE_LICENSE'], request_json
        )

        if flag:
            if response.json():
                if 'errorCode' in response.json():
                    if response.json()['errorCode'] != 0:
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to re-apply license.\nError: "{0}"'.format(
                            error_message)
                        raise SDKException('Client', '102', o_str)
                    self._license_info = None
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

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
            client_computers=[self.client_name],
            reboot_client=reboot_client,
            run_db_maintenance=run_db_maintenance
        )

    def repair_software(
            self,
            username=None,
            password=None,
            reboot_client=False):
        """triggers Repair software on the client machine

        Args:
             username    (str)               -- username of the machine to re-install features on

                default : None

            password    (str)               -- base64 encoded password

                default : None

            reboot_client (bool)            -- boolean to specify whether to reboot the client
            or not

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
            client=self.client_name,
            username=username,
            password=password,
            reboot_client=reboot_client
        )

    def get_dag_member_servers(self):
        """Gets the member servers for an Exchange DAG client.

            Returns:
                list - list consisting of the member servers

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        member_servers = []
        url = self._services['GET_DAG_MEMBER_SERVERS'] % self.client_id
        flag, response = self._cvpysdk_object.make_request('GET', url)
        if flag:
            if response.json():
                response = response.json()

                if response.get('errorCode', 0) != 0:
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to fetch details.\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)

                for member in response['dagSetup']['dagMemberServers']:
                    member_servers.append(member['serverName'])

                return member_servers

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    @property
    def consumed_licenses(self):
        """returns dictionary of all the license details which is consumed by the client

            Returns:
                dict - consisting of all licenses consumed by the client
                    {
                         "license_name_1": {
                            "licenseType": license_type_id,

                            "appType": app_type_id,

                            "licenseName": license_name,

                            "platformType": platform_type_id

                        },

                        "license_name_2": {

                            "licenseType": license_type_id,

                            "appType": app_type_id,

                            "licenseName": license_name,

                            "platformType": platform_type_id

                        }

                    }

            Raises:
                SDKException:
                    if failed to get the licenses

                    if response is empty

                    if response code is not as expected

        """
        if self._license_info is None:
            flag, response = self._cvpysdk_object.make_request(
                'GET', self._services['LIST_LICENSES'] % self.client_id
            )
            if flag:
                if response.json():
                    if 'errorCode' in response.json():
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to fetch license details.\nError: "{0}"'.format(
                            error_message)
                        raise SDKException('Client', '102', o_str)
                    licenses_dict = {}
                    for license_details in response.json().get('licensesInfo', []):
                        if license_details.get('license'):
                            licenses_dict[license_details['license'].get(
                                'licenseName', "")] = license_details['license']
                            licenses_dict[license_details['license'].get(
                                'licenseName', "")]['platformType'] = license_details.get(
                                'platformType')
                    self._license_info = licenses_dict
                else:
                    self._license_info = {}
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return self._license_info

    @property
    def cvd_port(self):
        """Returns CVD port of the client"""

        return self._cvd_port

    @property
    def client_guid(self):
        """Returns client GUID"""

        return self._properties.get('client', {}).get('clientEntity', {}).get('clientGUID', {})

    @property
    def client_type(self):
        """Returns client Type"""

        return self._properties.get('pseudoClientInfo', {}).get('clientType', "")

    def set_job_start_time(self, job_start_time_value):
        """Sets the jobstarttime for this Client.

            Raises:
                SDKException:
                    if failed to set the job start time

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json(option='Backup', job_start_time=job_start_time_value)

        flag, response = self._cvpysdk_object.make_request('POST', self._CLIENT, request_json)

        self._get_client_properties()

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorMessage']

                    o_str = 'Failed to set the jobstarttime \nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def uninstall_software(self, force_uninstall=True):
        """
        Performs readiness check on the client

            Args:
                force_uninstall (bool): Uninstalls packages forcibly. Defaults to True.


            Returns:
                The job object of the uninstall software job

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        uninstall = Uninstall(self._commcell_object)

        return uninstall.uninstall_software(self.client_name, force_uninstall=force_uninstall)

    @property
    def job_start_time(self):
        """Returns the job start time"""

        return self._job_start_time

    @property
    def readiness_details(self):
        """ returns instance of readiness"""
        if self._readiness is None:
            self._readiness = _Readiness(self._commcell_object, self.client_id)
        return self._readiness

    def get_environment_details(self):
        """
        Returns a dictionary with the count of fileservers, VM, Laptop for all the service commcells
        
         example output:
            {
            'fileServerCount': {'commcell_name': count},
            'laptopCount': {'commcell_name': count},
            'vmCount': {'commcell_name': count}
            }
        """
        self._headers = {
            'Accept': 'application/json',
            'CVContext': 'Comet',
            'Authtoken': self._commcell_object._headers['Authtoken']
        }
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['DASHBOARD_ENVIRONMENT_TILE'], headers=self._headers
        )
        if flag:
            if response.json() and 'cometClientCount' in response.json():
                main_keys = ['fileServerCount', 'laptopCount', 'vmCount']
                environment_tile_dict = {}
                for key in main_keys:
                    tile = {}
                    for tile_info in response.json()['cometClientCount']:
                        tile[tile_info['commcell']['commCellName']] = tile_info[key]
                    environment_tile_dict[key] = tile
                return environment_tile_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_needs_attention_details(self):
        """
        Returns a dictionary with the count of AnomalousServers, AnomalousJobs, InfrastructureServers for all the service commcells
        
        example output:
            {
            'CountOfAnomalousInfrastructureServers': {'commcell_name': count},
            'CountOfAnomalousServers': {'commcell_name': count},
            'CountOfAnomalousJobs': {'commcell_name': count}
            }
        """
        self._headers = {
            'Accept': 'application/json',
            'CVContext': 'Comet',
            'Authtoken': self._commcell_object._headers['Authtoken']
        }
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['DASHBOARD_NEEDS_ATTENTION_TILE'], headers=self._headers
        )
        if flag:
            if response.json() and 'commcellEntityRespList' in response.json():
                needs_attention_tile_dict = {}
                main_keys = ['CountOfAnomalousInfrastructureServers', 'CountOfAnomalousServers', 'CountOfAnomalousJobs']
                for key in main_keys:
                    tile = {}
                    for tile_info in response.json()['commcellEntityRespList']:
                        tile[tile_info['commcell']['commCellName']] = tile_info[key]
                    needs_attention_tile_dict[key] = tile
                return needs_attention_tile_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

class _Readiness:
    """ Class for checking the connection details of a client """

    def __init__(self, commcell, client_id):
        self.__commcell = commcell
        self.__client_id = client_id
        self._reason = None
        self._detail = None
        self._status = None
        self._dict = None

    def __fetch_readiness_details(
            self,
            network=True,
            resource=False,
            disabled_clients=False,
            cs_cc_network_check=False
    ):
        """
        Performs readiness check on the client

            Args:
                network (bool)  - Performs Network Readiness Check.
                                    Default: True

                resource (bool) - Performs Resource Readiness Check.
                                    Default: False

                disabled_clients (bool) - Includes backup activity disabled clients.
                                            Default: False

                cs_cc_network_check (bool)  - Performs network readiness check between CS and client alone.
                                                Default: False

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self.__commcell._cvpysdk_object.make_request(
            'GET',
            self.__commcell._services['CHECK_READINESS'] % (
                self.__client_id,
                network,
                resource,
                disabled_clients,
                cs_cc_network_check)
        )

        if flag:
            if response.json():
                self._dict = response.json()
                self.__check_reason()
                self.__check_status()
                self.__check_details()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self.__commcell._update_response_(response.text))

    def is_ready(self, network=True, resource=False, disabled_clients=False, cs_cc_network_check=False):
        """Performs readiness check on the client

        Args:
                network (bool)  - Performs Network Readiness Check.
                                    Default: True

                resource (bool) - Performs Resource Readiness Check.
                                    Default: False

                disabled_clients (bool) - Includes backup activity disabled clients.
                                            Default: False

                cs_cc_network_check (bool)  - Performs network readiness check between CS and client alone.
                                                Default: False

        Returns:

            (bool)  - True if ready else False

        """
        self.__fetch_readiness_details(network, resource, disabled_clients, cs_cc_network_check)
        return self._status == "Ready."

    def __check_reason(self):
        try:
            self._reason = self._dict['summary'][0]['reason']
        except KeyError:
            pass

    def __check_status(self):
        try:
            self._status = self._dict['summary'][0]['status']
        except KeyError:
            pass

    def __check_details(self):
        try:
            self._detail = self._dict['detail']
        except KeyError:
            pass

    def get_failure_reason(self):
        """ Retrieve client readiness failure reason"""
        if not self._dict:
            self.__fetch_readiness_details()
        return self._reason

    @property
    def status(self):
        """ Retrieve client readiness status """
        if not self._dict:
            self.__fetch_readiness_details()
        return self._status

    def get_detail(self):
        """ Retrieve client readiness details """
        if not self._dict:
            self.__fetch_readiness_details()
        return self._detail
