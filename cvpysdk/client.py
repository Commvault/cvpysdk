# -*- coding: utf-8 -*-
# pylint: disable=R1705, R0205

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

    add_vmware_client()                   --  adds a new VMWare Virtualization Client to the
    Commcell

    add_exchange_client()                 --  adds a new Exchange Virtual Client to the Commcell

    add_case_client()                     --  adds a new Case Manger Client to the Commcell

    get(client_name)                      --  returns the Client class object of the input client
    name

    delete(client_name)                   --  deletes the client specified by the client name from
    the commcell

    refresh()                             --  refresh the clients associated with the commcell

Clients Attributes
------------------

    **all_clients**             --  returns the dictioanry consisting of all the clients that are
    associated with the commcell and their information such as id and hostname

    **hidden_clients**          --  returns the dictioanry consisting of only the hidden clients
    that are associated with the commcell and their information such as id and hostname

    **virtualization_clients**  --  returns the dictioanry consisting of only the virtualization
    clients that are associated with the commcell and their information such as id and hostname


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

    refresh()                    --  refresh the properties of the client

    add_additional_setting()     --  adds registry key to the client property

    delete_additional_setting()  --  deletes registry key from the client property

    release_license()            --  releases a license from a client

    reconfigure_client()         --  reapplies license to the client

    push_servicepack_and_hotfixes() -- triggers installation of service pack and hotfixes

    get_dag_member_servers()     --  Gets the member servers of an Exchange DAG client.

    create_pseudo_client()       --  Creates a pseudo client

    set_job_start_time()         -- sets the job start time at client level


Client Attributes
-----------------

    **available_security_roles**    --  returns the security roles available for the selected
    client

    **client_id**                   --  returns the id of the client

    **client_name**                 --  returns the name of the client

    **client_hostname**             --  returns the host name of the client

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

from base64 import b64encode
from past.builtins import basestring

import requests

from .agent import Agents
from .schedules import Schedules
from .exception import SDKException
from .deployment.install import Install

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
        self._ALL_CLIENTS = self._services['GET_ALL_CLIENTS_PLUS_HIDDEN']
        self._VIRTUALIZATION_CLIENTS = self._services['GET_VIRTUAL_CLIENTS']
        self._ADD_EXCHANGE_CLIENT = self._services['ADD_EXCHANGE']

        self._clients = None
        self._hidden_clients = None
        self._virtualization_clients = None

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
        value = str(value)

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
                    virtualization_clients[pseudo_client['client']['clientName']] = {
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

    def create_pseudo_client(self, client_name):
        """ Creates a pseudo client

            Args:
                client_name (str)    --  client name

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
                "clientInfo":{
                    "clientType":0,
                    "openVMSProperties":{
                        "cvdPort":0
                    },
                    "ibmiInstallOptions":{}
                },
                "entity":{
                    "hostName":client_name,
                    "clientName":client_name,
                    "clientId":0,
                    "_type_":3
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

        return ((self.all_clients and client_name.lower() in self.all_clients) or
                self._get_client_from_hostname(client_name) is not None)

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

    def get(self, name):
        """Returns a client object if client name or host name matches specified name
            We check if specified name matches any of the existing client names else
            compare specified name with host names of existing clients

            Args:
                name (str)  --  name / hostname of the client

            Returns:
                object - instance of the Client class for the given client name

            Raises:
                SDKException:
                    if type of the client name argument is not string

                    if no client exists with the given name
        """
        if not isinstance(name, basestring):
            raise SDKException('Client', '101')
        else:
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
                    if response.json() and 'response' in response.json():
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
                        r'ServicePack:([\d]*)',
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

    def _request_json(self, option, enable=True, enable_time=None, job_start_time=None):
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

        if job_start_time is not None:
            request_json1['clientProperties']['jobStartTime'] = job_start_time

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
            if self.instance:
                command = 'commvault -instance {0} {1}'.format(
                    self.instance, operations_dict[operation]['unix_command']
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

    @property
    def name(self):
        """Returns the Client name"""
        return self._properties['client']['clientEntity']['clientName']

    @property
    def display_name(self):
        """Returns the Client display name"""
        return self._properties['client']['displayName']

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

        request_json = self._request_json('Backup', False, enable_time)

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

        request_json = self._request_json('Restore', False, enable_time)

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

        request_json = self._request_json('Data Aging', False, enable_time)

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
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['CHECK_READINESS'] % self.client_id
        )

        if flag:
            if response.json():
                return 'isClientReady' in response.json() and response.json()['isClientReady'] == 1
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

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

            while True:
                try:
                    if self.is_ready:
                        break

                    if time.time() - start_time > timeout * 60:
                        raise SDKException('Client', '107')
                except requests.ConnectionError:
                    continue

                time.sleep(5)

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
            if enc_setting is "ON_CLIENT":
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
        request_json = self._request_json(job_start_time=job_start_time_value)

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

    @property
    def job_start_time(self):
        """Returns the job start time"""

        return self._job_start_time

