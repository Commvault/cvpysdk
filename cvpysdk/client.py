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

    _get_dynamics_365_clients()           --  get all the Dynamics 365 clients in the commcell

    _get_salesforce_clients()             --  get all salesforce clients in the commcell

    _get_hidden_clients()                 --  gets all the hidden clients associated with the
    commcell

    _get_virtualization_clients()         --  gets all the virtualization clients associated with
    the commcell

    _get_virtualization_access_nodes()    --  gets all the virtualization access nodes associated with
    the commcell

    _get_client_dict()                    --  returns the client dict for client to be added to
    member server

    _member_servers()                     --  returns member clients to be associated with the
    Virtual Client

    _get_client_from_hostname()           --  returns the client name if associated with specified
    hostname if exists

    _get_hidden_client_from_hostname()    --  returns the client name if associated with specified
    hostname if exists

    _get_client_from_displayname()        --  get the client name for given display name

    _get_fl_parameters()                  --  Returns the fl parameters to be passed in the mongodb caching api call

    _get_sort_parameters()                --  Returns the sort parameters to be passed in the mongodb caching api call

    _get_fq_parameters()                  --  Returns the fq parameters based on the fq list passed

    get_clients_cache()                   --  Gets all the clients present in CommcellEntityCache DB.

    has_client(client_name)               --  checks if a client exists with the given name or not

    has_hidden_client(client_name)        --  checks if a hidden client exists with the given name

    _process_add_response()               -- to process the add client request using API call

    add_vmware_client()                   --  adds a new VMWare Virtualization Client to the
                                              Commcell

    add_kubernetes_client()               --  adds a new Kubernetes Virtualization Client to the
                                              Commcell

    add_nas_client()                      --  adds a new NAS Client

    add_share_point_client()              -- adds a new sharepoint pseudo client to the Commcell

    add_onedrive_for_business_client()              -- adds a new OneDrive for Business client to Commcell

    add_exchange_client()                 --  adds a new Exchange Virtual Client to the Commcell

    add_splunk_client()                   --  adds a new Splunk Client to the Commcell

    add_yugabyte_client()                 --  adds a new Yugabytedb Client to the Commcell

    add_couchbase_client()                --  adds a new Couchbase Client to the commcell

    add_case_client()                     --  adds a new Case Manger Client to the Commcell

    add_salesforce_client()               --  adds a new salesforce client

    add_azure_client()                    --  adds a new azure cloud client

    add_amazon_client()                    --  adds a new amazon cloud client

    add_google_client()                    --  adds a new google cloud client

    add_alicloud_client()                    --  adds a new alibaba cloud client

    add_nutanix_files_client()                  --  adds a new nutanix files client

    add_onedrive_client()                 --  adds a new onedrive client

    add_cassandra_client()                --  add cassandra client

    add_cockroachdb_client()              --  add cockroachdb client

    add_azure_cosmosdb_client()             --  add client for azure cosmosdb cloud account

    get(client_name)                      --  returns the Client class object of the input client
    name

    delete(client_name)                   --  deletes the client specified by the client name from
    the commcell

    filter_clients_return_displaynames()  --  filter clients based on criteria

    refresh()                             --  refresh the clients associated with the commcell

    add_azure_ad_client()                   --  add an Azure Active Directory client to the commcel

    add_googleworkspace_client()         --  adds a new google client


Clients Attributes
------------------

    **all_clients**             --  returns the dictionary consisting of all the clients that are
    associated with the commcell and their information such as id and hostname

    **all_clients_cache**       --  returns th dictionary consisting of all the clients and their
    info from CommcellEntityCache DB in Mongo

    **all_client_props**        --  returns complete GET api response

    **hidden_clients**          --  returns the dictionary consisting of only the hidden clients
    that are associated with the commcell and their information such as id and hostname

    **virtualization_clients**  --  returns the dictionary consisting of only the virtualization
    clients that are associated with the commcell and their information such as id and hostname

    **virtualization_access_nodes** --  returns the dictionary consisting of only the virtualization
    clients that are associated with the commcell and their information such as id and hostname

    **office365_clients**       --  Returns the dictionary consisting of all the office 365 clients that are
                                    associated with the commcell

    **dynamics365_clients**     --  Returns the dictionary consisting of all the Dynamics 365 clients
                                    that are associated with the commcell

    **salesforce_clients**      --  Returns the dictionary consisting of all the salesforce clients that are
                                    associated with the commcell

    **file_server_clients**     --  Returns the dictionary consisting of all the File Server clients
                                    that are associated with the commcell

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

    get_configured_additional_setting() --  To get configured additional settings from the client property

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

    enable_content_indexing()   --  Enables the v1 content indexing on the client

    disable_content_indexing()   --  Disables the v1 content indexing on the client

    check_eligibility_for_migration()  --   Checks whether client is Eligible for Migration or not

    change_company_for_client()        --   Migrates client to specified company

    disable_owner_privacy()                 --  Disables the privacy option for client

    enable_owner_privacy()                  --  Enables the privacy option for client

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

    **os_type**                     --  returns OSType Enum representing the client's OSType

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

    **is_mongodb_ready**            -- returns boolean value specifying whether mongoDB is working fine or not

    **set_encryption_prop**         --    Set encryption properties on a client

    **set_dedup_prop**              --     Set DDB properties

    **consumed_licenses**           --  returns dictionary of all the license details
    which is consumed by the client

    **cvd_port**                    -- returns cvd port of the client

    **vm_guid**                     -- returns guid of the vm client

    **company_name**                 -- returns company name for the client

    **is_privacy_enabled**          -- returns if client privacy is enabled

    **latitude**                    -- Returns the latitude from geo location of the client

    **longitude**                   -- Returns the longitude from geo location of the client

    **is_vm**                       -- Returns True if its a VM client

    **hyperv_id_of_vm**             -- Returns the Id of hyperV that the given VM is associated with

    **associated_client_group**     -- Returns the list of clientgroups that the client is associated to

    **company_id**                  -- Returns the company Id of the client

    **network_status**              --  Returns network status for the client

    **is_deleted_client**           --  Returns if the is deleted

    **is_infrastructure**           --  returns if the client is infrastructure

    **update_status**               --  returns the update status of the client
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
import time
import copy
import datetime
from base64 import b64encode

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
from .organization import Organizations
from .constants import AppIDAType, AppIDAName, OSType
from .constants import ResourcePoolAppType


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
        self._DYNAMICS365_CLIENTS = self._services['GET_DYNAMICS_365_CLIENTS']
        self._SALESFORCE_CLIENTS = self._services['GET_SALESFORCE_CLIENTS']
        self._ALL_CLIENTS = self._services['GET_ALL_CLIENTS_PLUS_HIDDEN']
        self._VIRTUALIZATION_CLIENTS = self._services['GET_VIRTUAL_CLIENTS']
        self._GET_VIRTUALIZATION_ACCESS_NODES = self._services['GET_VIRTUALIZATION_ACCESS_NODES']
        self._FS_CLIENTS = self._services['GET_FILE_SERVER_CLIENTS']
        self._ADD_EXCHANGE_CLIENT = self._ADD_SHAREPOINT_CLIENT = self._ADD_SALESFORCE_CLIENT = \
            self._ADD_GOOGLE_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_SPLUNK_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_COCKROACHDB_CLIENT = self._services['COCKROACHDB']
        self._ADD_CASSANDRA_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_YUGABYTE_CLIENT = self._services['CREATE_YUGABYTE_CLIENT']
        self._ADD_COUCHBASE_CLIENT = self._services['CREATE_COUCHBASE_CLIENT']
        self._ADD_NUTANIX_CLIENT = self._services['CREATE_NUTANIX_CLIENT']
        self._ADD_NAS_CLIENT = self._services['CREATE_NAS_CLIENT']
        self._ADD_ONEDRIVE_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._clients = None
        self._hidden_clients = None
        self._virtualization_clients = None
        self._virtualization_access_nodes = None
        self._office_365_clients = None
        self._dynamics365_clients = None
        self._salesforce_clients = None
        self._file_server_clients = None
        self._client_cache = None
        self._all_clients_props = None
        self.filter_query_count = 0
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
        return "Clients class instance for Commcell"

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

    def add_azure_ad_client(self,client_name,plan_name,application_Id,application_Secret,azure_directory_Id):
        """
        Function to add a new Azure AD Client
        Args:
            plan_name               (str)   --  plan name
            application_Id          (str)   --  application id of azure ad app
            application_Secret      (str)   --  application secret of azure ad app
            azure_directory_Id      (str)   --  directory id of azure ad app

        Raises:
            SDKException:

                if response is empty

                if response is not success
        """
        azure_ad_client=self._services['ADDAZURECLIENT']
        plan_id=None
        if self._commcell_object.plans.has_plan(plan_name):
            server_plan_object = self._commcell_object.plans.get(plan_name)
            plan_id=int(server_plan_object.plan_id)
        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        payload = {"name":client_name,
                   "serverPlan":{
                       "id":(plan_id),
                       "name":(plan_name)
                   },
                   "azureApp":{
                       "applicationId":(application_Id),
                       "applicationSecret":(application_Secret),
                       "azureDirectoryId":(azure_directory_Id)
                   }
                   }
        flag, response = self._cvpysdk_object.make_request(method='POST', url=azure_ad_client,payload=payload)

        if flag and response:
            azure_ad_response=response.json()
            if azure_ad_response.get("errorCode", None)==-1:
                raise SDKException('Client', '102', azure_ad_response.get("errorMessage"))
        elif not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException('Response', '102', self._update_response_(response.text))

    def _get_clients(self, full_response: bool = False):
        """Gets all the clients associated with the commcell

            Args:
                full_response(bool) --  flag to return complete response

            Returns:
                dict    -   consists of all clients in the commcell

                    {
                        "client1_name": {

                            "id": client1_id,

                            "hostname": client1_hostname,

                            "displayName": client1_displayname
                        },

                        "client2_name": {

                            "id": client2_id,

                            "hostname": client2_hostname.

                            "displayName": client2_displayname
                        }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        attempts = 0
        while attempts < 5:
            flag, response = self._cvpysdk_object.make_request('GET', self._CLIENTS)
            attempts += 1

            if flag:
                if response.json() and 'clientProperties' in response.json():
                    if full_response:
                        return response.json()
                    clients_dict = {}

                    for dictionary in response.json()['clientProperties']:
                        temp_name = dictionary['client']['clientEntity']['clientName'].lower()
                        temp_id = str(dictionary['client']['clientEntity']['clientId']).lower()
                        temp_hostname = dictionary['client']['clientEntity']['hostName'].lower()
                        temp_display_name = dictionary['client']['clientEntity']['displayName'].lower()
                        clients_dict[temp_name] = {
                            'id': temp_id,
                            'hostname': temp_hostname,
                            'displayName': temp_display_name
                        }

                    return clients_dict
                else:
                    return {} # logged in user might not have privileges on any client
            else:
                if attempts > 4:
                    raise SDKException('Response', '101', self._update_response_(response.text))
                time.sleep(5)

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

    def _get_dynamics_365_clients(self):
        """
            REST API call to get all Dynamics 365 clients in the commcell

                  Returns:
                      dict    -   For the Dynamics 365 clients in the Commcell
                      Format:
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
        flag, response = self._cvpysdk_object.make_request('GET', self._DYNAMICS365_CLIENTS)

        if flag:
            clients_dict = {}
            if response.json() and "o365Client" in response.json():
                for dictionary in response.json()['o365Client']:
                    client_name = dictionary['clientName'].lower()
                    client_id = str(dictionary['clientId']).lower()
                    clients_dict[client_name] = {
                        'id': client_id
                    }
            return clients_dict
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def dynamics365_clients(self):
        """Returns the dict of all Dynamics 365 clients in the commcell"""
        if self._dynamics365_clients is None:
            self._dynamics365_clients = self._get_dynamics_365_clients()
        return self._dynamics365_clients

    def _get_salesforce_clients(self):
        """
        REST API call to get all Salesforce clients in the commcell

        Returns:
            dict[str, dict]: Containing Salesforce clients and ids in the Commcell like

                {
                    "client1_displayName": {
                        "id": client1_id,
                        "clientName": "client1_name"
                    },
                    "client2_displayName": {
                        "id": client2_id,
                        "clientName": "client2_name"
                    }
                }
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._SALESFORCE_CLIENTS)

        if flag:
            if response.json() and 'orgs' in response.json():

                return {
                    self.all_clients[sf_subclient['clientName'].lower()]['displayName']: {
                        'id': sf_subclient['clientId'],
                        'clientName': sf_subclient['clientName']
                    }
                    for sf_subclient in map(lambda org: org['sfSubclient'], response.json()['orgs'])
                }
            return {}
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def salesforce_clients(self):
        """Returns the dict of all salesforce clients in the commcell"""
        if self._salesforce_clients is None:
            self._salesforce_clients = self._get_salesforce_clients()
        return self._salesforce_clients

    def _get_hidden_clients(self):
        """Gets all the clients associated with the commcell, including all VM's and hidden clients

            Returns:
                dict    -   consists of all clients (including hidden clients) in the commcell

                    {
                        "client1_name": {

                            "id": client1_id,

                            "hostname": client1_hostname,

                            "displayName": client1_displayname
                        },

                        "client2_name": {

                            "id": client2_id,

                            "hostname": client2_hostname,

                            "displayName": client1_displayname
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
                    temp_display_name = dictionary['client']['clientEntity']['displayName'].lower()
                    all_clients_dict[temp_name] = {
                        'id': temp_id,
                        'hostname': temp_hostname,
                        'displayName': temp_display_name
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
                return {} # logged in user might not have privileges on any client
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
                    virtualization_clients[pseudo_client['client']['displayName'].lower()] = {
                        'clientId': pseudo_client['client']['clientId'],
                        'clientName': pseudo_client['client']['clientName'],
                        'hostName': pseudo_client['client']['hostName']
                    }

                return virtualization_clients

            return {}
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_virtualization_access_nodes(self):
        """REST API call to get all virtualization access nodes in the commcell
            Returns:
                dict - consists of all access nodes in the commcell
                {
                     "display_name1": {
                            "id": client1_id,
                            "name": client1_name,
                            "hostname": client1_hostname
                    },
                     "display_name2": {
                            "id": client2_id,
                            "name": client2_name,
                            "hostname": client2_hostname
                     },
                }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._GET_VIRTUALIZATION_ACCESS_NODES)

        virtualization_access_nodes = {}
        if flag and response:
            if response.json() and 'clients' in response.json():
                for virtualization_access_node in response.json()['clients']:
                    client_id = virtualization_access_node.get('clientId')
                    client_name = virtualization_access_node.get('clientName').lower()
                    display_name = virtualization_access_node.get('displayName').lower()
                    host_name = virtualization_access_node.get('hostName').lower()
                    if client_name:
                        virtualization_access_nodes[display_name] = {
                            'id': client_id,
                            'name': client_name,
                            'hostName': host_name
                        }
            return virtualization_access_nodes
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_fileserver_clients(self):
        """REST API call to get all file server clients in the commcell

            Returns:
                dict    -   consists of all file server clients in the commcell

                    {
                        "client1_name": {

                            "id": client1_id,

                            "displayName": client1_displayname
                        },

                        "client2_name": {

                            "id": client2_id,

                            "displayName": client2_displayname
                        }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._FS_CLIENTS)

        fs_clients = {}
        if flag and response:
            if response.json() and 'fileServers' in response.json():
                for file_server in response.json()['fileServers']:
                    fs_clients[file_server['name']] = {
                        'id': file_server['id'],
                        'displayName': file_server['displayName']
                    }
            return fs_clients
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
            if isinstance(client, str):
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

    def _get_client_from_displayname(self, display_name):
        """get the client name for given display name
            Args:
                displayname    (str)   --  display name of the  client on this commcell

            Returns:
                str     -   name of the client associated with this display name

                None    -   None when no clients exists with this name
            Raises:
                Exception:
                    if multiple clients has same display name
        """
        display_name_occurence = 0
        client_name = None
        for client in self.all_clients:
            if self.all_clients[client]['displayName'] == display_name.lower():
                display_name_occurence += 1
                client_name = client
            if display_name_occurence > 1:
                raise SDKException('Client', '102', 'Multiple clients have the same display name')
        return client_name

    def _get_fl_parameters(self, fl: list = None) -> str:
        """
        Returns the fl parameters to be passed in the mongodb caching api call

        Args:
            fl    (list)  --   list of columns to be passed in API request

        Returns:
            fl_parameters(str) -- fl parameter string
        """
        self.valid_columns = {'clientName': 'clientProperties.client.clientEntity.clientName',
                              'clientId': 'clientProperties.client.clientEntity.clientId',
                              'hostName': 'clientProperties.client.clientEntity.hostName',
                              'displayName': 'clientProperties.client.clientEntity.displayName',
                              'clientGUID': 'clientProperties.client.clientEntity.clientGUID',
                              'companyName': 'clientProperties.client.clientEntity.entityInfo.companyName',
                              'idaList': 'client.idaList.idaEntity.appName',
                              'clientRoles': 'clientProperties.clientProps.clientRoles',
                              'isDeletedClient': 'clientProperties.clientProps.IsDeletedClient',
                              'version': 'clientProperties.client.versionInfo.version',
                              'OSName': 'client.osInfo.OsDisplayInfo.OSName',
                              'isInfrastructure': 'clientProperties.clientProps.isInfrastructure',
                              'updateStatus': 'client.versionInfo.UpdateStatus',
                              'networkStatus': 'clientProperties.clientProps.networkReadiness.status',
                              'tags': 'clientProperties.client.clientEntity.tags'
                              }
        default_columns = 'clientProperties.client.clientEntity.clientName'

        if fl:
            if all(col in self.valid_columns for col in fl):
                fl_parameters = f"&fl={default_columns},{','.join(self.valid_columns[column] for column in fl)}"
            else:
                raise SDKException('Client', '102', 'Invalid column name passed')
        else:
            fl_parameters = '&fl=clientProperties.client%2CclientProperties.clientProps%2Coverview'

        return fl_parameters

    def _get_sort_parameters(self, sort: list = None) -> str:
        """
        Returns the sort parameters to be passed in the mongodb caching api call

        Args:
            sort  (list)  --   contains the name of the column on which sorting will be performed and type of sort
                                valid sor type -- 1 for ascending and -1 for descending
                                e.g. sort = ['ColumnName','1']

        Returns:
            sort_parameters(str) -- sort parameter string
        """
        sort_type = str(sort[1])
        col = sort[0]
        if col in self.valid_columns.keys() and sort_type in ['1', '-1']:
            sort_parameter = '&sort=' + self.valid_columns[col] + ':' + sort_type
        else:
            raise SDKException('Client', '102', 'Invalid column name passed')
        return sort_parameter

    def _get_fq_parameters(self, fq: list = None) -> str:
        """
        Returns the fq parameters based on the fq list passed.

        Args:
            fq (list): Contains the columnName, condition, and value.
                       e.g. fq = [['displayName','contains', 'test'],['clientRoles','contains', 'Command Center']]

        Returns:
            str: fq parameter string.
        """
        conditions = {"contains", "notContains", "eq", "neq"}
        params = ["&fq=clientProperties.isServerClient:eq:true"]

        for column, condition, *value in (fq or []):
            if column not in self.valid_columns:
                raise SDKException("Client", "102", "Invalid column name passed")

            #  Handle networkStatus mapping
            if column == "networkStatus" and value:
                network_status_map = {
                    'Not available': 'UNKNOWN',
                    'No software installed': 'NOT_APPLICABLE',
                    'Offline': 'OFFLINE',
                    'Online': 'ONLINE'
                }
                value[0] = network_status_map.get(value[0], value[0])  # Convert back to enum key if needed

            # isDeletedClient is always passed as 'eq:true' or 'neq:true'
            if column == "isDeletedClient":
                condition = "neq" if value and value[0] is False else "eq"
                value = ["true"]

            if column == "tags" and condition == "contains":
                params.append(f"&tags={value[0]}")
            elif condition in conditions:
                params.append(f"&fq={self.valid_columns[column]}:{condition}:{value[0]}")
            elif condition == "isEmpty" and not value:
                params.append(f"&fq={self.valid_columns[column]}:in:null,")
            else:
                raise SDKException("Client", "102", "Invalid condition passed")

        return "".join(params)

    def get_clients_cache(self, hard: bool = False, **kwargs) -> dict:
        """
        Gets all the clients present in CommcellEntityCache DB.

        Args:
            hard  (bool)        --   Flag to perform hard refresh on clients cache.
            **kwargs (dict):
                fl (list)       --   List of columns to return in response (default: None).
                sort (list)     --   Contains the name of the column on which sorting will be performed and type of sort.
                                           Valid sort type: 1 for ascending and -1 for descending
                                           e.g. sort = ['connectName', '1'] (default: None).
                limit (list)    --   Contains the start and limit parameter value.
                                            Default ['0', '100'].
                search (str)    --   Contains the string to search in the commcell entity cache (default: None).
                fq (list)       --   Contains the columnName, condition and value.
                                            e.g. fq = [['displayName', 'contains', 'test'],
                                             ['clientRoles', 'contains', 'Command Center']] (default: None).
                enum (bool)     --   Flag to return enums in the response (default: True).

        Returns:
            dict: Dictionary of all the properties present in response.
        """
        # computing params
        fl_parameters = self._get_fl_parameters(kwargs.get('fl', None))
        fq_parameters = self._get_fq_parameters(kwargs.get('fq', None))
        limit = kwargs.get('limit', None)
        limit_parameters = f'start={limit[0]}&limit={limit[1]}' if limit else ''
        hard_refresh = '&hardRefresh=true' if hard else ''
        sort_parameters = self._get_sort_parameters(kwargs.get('sort', None)) if kwargs.get('sort', None) else ''

        # Search operation can only be performed on limited columns, so filtering out the columns on which search works
        searchable_columns= ["hostName","displayName","companyName","idaList","version","OSName"]
        search_parameter = (f'&search={",".join(self.valid_columns[col] for col in searchable_columns)}:contains:'
                            f'{kwargs.get("search", None)}') if kwargs.get('search', None) else ''

        params = [
            limit_parameters,
            sort_parameters,
            fl_parameters,
            hard_refresh,
            search_parameter,
            fq_parameters
        ]

        request_url = f"{self._CLIENTS}?" + "".join(params)
        flag, response = self._cvpysdk_object.make_request("GET", request_url,)

        if not flag:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        clients_cache = {}
        if response.json() and 'clientProperties' in response.json():
            self.filter_query_count = response.json().get('filterQueryCount',0)
            for client in response.json()['clientProperties']:
                temp_client = client.get('client', None)
                name = temp_client.get('clientEntity', None).get('clientName')
                client_config = {
                    'clientName':temp_client.get('clientEntity', None).get('clientName'),
                    'clientId': temp_client.get('clientEntity', {}).get('clientId'),
                    'hostName': temp_client.get('clientEntity', {}).get('hostName'),
                    'displayName': temp_client.get('clientEntity', {}).get('displayName'),
                    'clientGUID': temp_client.get('clientEntity', {}).get('clientGUID'),
                    'companyName': temp_client.get('clientEntity', {}).get('entityInfo', {}).get('companyName'),
                    'version': temp_client.get('versionInfo', {}).get('version',''),
                    'updateStatus': temp_client.get('versionInfo', {}).get('UpdateStatus'),
                    'idaList': [agent.get("idaEntity", {}).get('appName', None)
                                            for agent in temp_client.get('idaList', [])] or []
                }
                if 'osInfo' in temp_client:
                    client_config['OSName'] = temp_client.get('osInfo', {}).get('OsDisplayInfo', {}).get('OSName')
                if 'tags' in temp_client.get('clientEntity', {}):
                    client_config['tags'] = temp_client.get('clientEntity', {}).get('tags',[])
                if 'clientProps' in client:
                    temp_client_prop = client['clientProps']
                    status = temp_client_prop.get('networkReadiness', {}).get('status')
                    network_status_map = {
                        'UNKNOWN': 'Not available',
                        'NOT_APPLICABLE': 'No software installed',
                        'OFFLINE': 'Offline',
                        'ONLINE': 'Online'
                    }
                    client_config.update({
                        'isDeletedClient': temp_client_prop.get('IsDeletedClient', False),
                        'isInfrastructure': temp_client_prop.get('isInfrastructure'),
                        'networkStatus': network_status_map.get(status, status) if kwargs.get('enum', True) else status,
                        'clientRoles': [role.get('name') for role in temp_client_prop.get('clientRoles', [])]
                    })
                clients_cache[name] = client_config
            return clients_cache
        else:
            raise SDKException('Response', '102')

    @property
    def all_clients(self):
        """Returns the dictionary consisting of all the clients and their info.

            dict - consists of all clients in the commcell
                    {
                         "client1_name": {
                                "id": client1_id,
                                "hostname": client1_hostname,
                                "displayName": client1 display name
                        },
                         "client2_name": {
                                "id": client2_id,
                                "hostname": client2_hostname,
                                "displayName": client2 display name
                         },
                    }

        """
        return self._clients

    @property
    def all_clients_cache(self) -> dict:
        """returns th dictionary consisting of all the clients and their info from CommcellEntityCache DB in Mongo

            dict - consists of all clients in the CommcellEntityCache
                    {
                         "client1_name": {
                                "clientName": client1_unique_client_specifier
                                "id": client1_id,
                                "hostname": client1_hostname,
                                "displayName": client1 display name,
                                "clientGUID": client1 GUID,
                                "company": client1 company,
                                "version": client1 version,
                                "OsInfo": client1 os info,
                                "idaList": client1 ida list,
                                "tags": client1 tags,
                                "isDeletedClient": client1 status,
                                "isInfrastructure": client1 infrastructure flag,
                                "networkStatus": client1 network status,
                                "region": client1 region,
                                "roles": client1 roles
                        },
                         "client2_name": {
                                "clientName": client2_unique_client_specifier
                                "id": client2_id,
                                "hostname": client2_hostname,
                                "displayName": client2 display name,
                                "clientGUID": client2 GUID,
                                "company": client2 company,
                                "version": client2 version,
                                "OsInfo": client2 os info,
                                "idaList": client2 ida list,
                                "tags": client2 tags,
                                "isDeletedClient": client2 status,
                                "isInfrastructure": client2 infrastructure flag,
                                "networkStatus": client2 network status,
                                "region": client2 region,
                                "roles": client2 roles
                         },
                    }
        """
        if not self._client_cache:
            self._client_cache = self.get_clients_cache()
        return self._client_cache

    @property
    def all_clients_prop(self)->list[dict]:
        """
        Returns complete GET API response
        """
        self._all_clients_props = self._get_clients(full_response=True).get('clientProperties',[])
        return self._all_clients_props

    def create_pseudo_client(self, client_name, client_hostname=None, client_type="windows"):
        """ Creates a pseudo client

            Args:
                client_name     (str)   --  name of the client to be created

                client_hostname (str)   --  hostname of the client to be created
                    default:None

                client_type(str)     --  OS/Type of client to be created
                    default : "windows"

                    Available Values for client_type : "windows"
                                                       "unix"
                                                       "unix cluster"
                                                       "sap hana"

            Returns:
                client object for the created client.

            Raises:
                SDKException:
                    if client name type is incorrect

                    if response is empty

                    if failed to get client id from response

        """
        client_type_dict = {
            "windows": "WINDOWS",
            "unix": "UNIX",
            "unix cluster": 11,
            "sap hana": 16
        }
        if not isinstance(client_name, str):
            raise SDKException('Client', '101')

        os_id = client_type_dict[client_type.lower()]

        request_json = {
            'App_CreatePseudoClientRequest':
                {
                    "registerClient": "false",
                    "clientInfo": {
                        "clientType": os_id,
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

    @property
    def virtualization_access_nodes(self):
        """Returns the dictionary consisting of the virtualization access nodes

                dict - consists of all access nodes in the commcell
                {
                     "display_name1": {
                            "id": client1_id,
                            "name": client1_name,
                            "hostname": client1_hostname
                    },
                     "display_name2": {
                            "id": client2_id,
                            "name": client2_name,
                            "hostname": client2_hostname
                     },
                }
        """
        return self._virtualization_access_nodes

    @property
    def file_server_clients(self):
        """Returns the dictionary consisting of the file server clients and their info.

            dict - consists of all file server clients in the commcell
                    {
                        "client1_name": {

                            "id": client1_id,

                            "displayName": client1_displayname
                        },

                        "client2_name": {

                            "id": client2_id,

                            "displayName": client2_displayname
                        }
                    }
        """
        if self._file_server_clients is None:
            self._file_server_clients = self._get_fileserver_clients()
        return self._file_server_clients

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
        if not isinstance(client_name, str):
            raise SDKException('Client', '101')
        if self.all_clients and client_name.lower() in self.all_clients:
            return True
        elif self._get_client_from_hostname(client_name) is not None:
            return True
        elif self.hidden_clients and client_name.lower() in self.hidden_clients:
            return True
        elif self._get_hidden_client_from_hostname(client_name) is not None:
            return True
        elif self._get_client_from_displayname(client_name) is not None:
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
        if not isinstance(client_name, str):
            raise SDKException('Client', '101')

        return ((self.hidden_clients and client_name.lower() in self.hidden_clients) or
                self._get_hidden_client_from_hostname(client_name) is not None)

    def _process_add_response(self, request_json, endpoint=None):
        """Runs the Client Add API with the request JSON provided,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API
                endpoint        (str)   --  Endpoint for making request to (default is '/Client')

            Returns:
                (bool, str, str):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        if not endpoint:
            endpoint = self._ADD_CLIENT
        flag, response = self._cvpysdk_object.make_request('POST', endpoint, request_json)

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
            api_server_endpoint,
            service_account,
            service_token,
            encoded_service_token,
            access_nodes=None
    ):
        """Adds a new Kubernetes Cluster client to the Commcell.

            Args:
                client_name         (str)   --  name of the new Kubernetes Cluster client

                api_server_endpoint (str)   --  Kubernetes API Server endpoint of the cluster

                service_account     (str)   --  Name of the Service Account for authentication

                service_token       (str)   --  Token fetched from the Service Account

                encoded_service_token  (str)   -- Base64 encoded Service Account Token

                access_nodes        (list/str)  --  Virtual Server proxy clients as access nodes



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

        if type(access_nodes) is str:
            access_nodes = [access_nodes]

        if not access_nodes:
            access_nodes = []

        member_servers_list = []
        for server in access_nodes:
            if not self.has_client(server):
                raise SDKException('Client', '102', f'Access node {server} does not exist in CommCell')
            member_servers_list.append(
                {
                    "client": {
                        "clientName": server,
                        "_type_": 3
                    }
                }
            )

        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 20,
                        "k8s": {
                            "secretName": service_account,
                            "secretKey": service_token,
                            "secretKeyV2": encoded_service_token,
                            "secretType": "ServiceAccount",
                            "endpointurl": api_server_endpoint
                        },
                        "associatedClients": {},
                        "vmwareVendor": {
                            "vcenterHostName": api_server_endpoint
                        }
                    }
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        if member_servers_list:
            associated_clients = {
                'associatedClients': {
                    'memberServers': member_servers_list
                }
            }
            request_json['clientInfo']['virtualServerClientProperties']['virtualServerInstanceInfo'].update(associated_clients)

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
                    password,
                    listenPort = 10000
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
                "listenPort": listenPort,
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
                        "listenPort": listenPort,
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

    def add_hyperv_client(
            self,
            client_name,
            hyperv_hostname,
            hyperv_username,
            hyperv_password,
            clients
    ):
        """Adds a new Hyper-V Virtualization Client to the Commcell.
            Args:
                client_name        (str)   --  name of the new Hyper-V Virtual Client
                hyperv_hostname    (str)   --  hostname of the hyperv to connect to
                hyperv_username    (str)   --  login username for the hyperv
                hyperv_password    (str)   --  plain-text password for the hyperv
                clients            (list)  --  list cotaining client names / client objects,
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

        hyperv_password = b64encode(hyperv_password.encode()).decode()
        member_servers = self._member_servers(clients)

        request_json = {
            "clientInfo": {
                "clientType": 12,
                "virtualServerClientProperties": {
                    "virtualServerInstanceInfo": {
                        "vsInstanceType": 2,
                        "hyperV": {
                            "serverName": hyperv_hostname,
                            "credentials": {
                                "userName": hyperv_username,
                                "password": hyperv_password,
                            }
                        },
                        "associatedClients": {
                            "memberServers": member_servers
                        },
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

                azure_directory_id    (str)         --  azure directory id for sharepoint online

                cert_string           (str)         -- certificate string

                cert_password         (str)         -- certificate password

                cloud_region            (int)   --  stores the cloud region for the SharePoint client
                                                    - Default (Global Service) [1]
                                                    - Germany [2]
                                                    - China [3]
                                                    - U.S. Government GCC [4]
                                                    - U.S. Government GCC High [5]


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

        if index_server:
            if self.has_client(index_server):
                index_server_cloud = self.get(index_server)

                if index_server_cloud.agents.has_agent(AppIDAName.BIG_DATA_APPS.value):
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
            if isinstance(client, str):
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


        server_resource_pool_map = server_plan_object._properties.get('storageResourcePoolMap',[])
        if server_resource_pool_map:
            server_plan_resources= server_resource_pool_map[0].get('resources', None)
        else:
            server_plan_resources = None

        # use resource pool only if resource pool type is Office365 or Sharepoint
        is_resource_pool_enabled = False
        if server_plan_resources is not None:
            for resource in server_plan_resources:
                if resource.get('appType', 0) in (ResourcePoolAppType.O365.value, ResourcePoolAppType.SHAREPOINT.value):
                    is_resource_pool_enabled = True

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
        if 'cloud_region' in kwargs.keys():
            cloud_region = kwargs.get('cloud_region')
        else:
            cloud_region = 1
        global_administrator = kwargs.get('global_administrator')
        request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
            "spOffice365BackupSetProp"] = {
            "tenantUrlItem": tenant_url,
            "cloudRegion": cloud_region,
            "isModernAuthEnabled": kwargs.get('is_modern_auth_enabled', False),
            "infraStructurePoolEnabled": False,
             "office365Credentials": {
                    "userName": ""
                }
        }
        if global_administrator:
            azure_app_key_id = b64encode(kwargs.get('azure_app_key_id').encode()).decode()

            azure_app_dict = {
                "azureAppId": kwargs.get('azure_app_id'),
                "azureAppKeyValue": azure_app_key_id,
                "azureDirectoryId": kwargs.get('azure_directory_id')
            }

            if 'cert_string' in kwargs:
                # cert_string needs to be encoded twice
                cert_string = b64encode(kwargs.get('cert_string')).decode()
                cert_string = b64encode(cert_string.encode()).decode()

                cert_password = b64encode(kwargs.get('cert_password').encode()).decode()

                cert_dict = {
                    "certificate": {
                        "certBase64String": cert_string,
                        "certPassword": cert_password
                    }
                }
                azure_app_dict.update(cert_dict)



            global_administrator_password = b64encode(kwargs.get('global_administrator_password').encode()).decode()
            request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"]["azureAppList"] = {
                    "azureApps": [
                        azure_app_dict
                    ]
                }

            request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"]["serviceAccounts"] = {
                    "accounts": [
                        {
                            "serviceType": service_type["Sharepoint Global Administrator"],
                            "userAccount": {
                                "userName": global_administrator,
                                "password": global_administrator_password
                            }
                        }
                    ]
                }
        else:
            user_password = b64encode(kwargs.get('user_password').encode()).decode()
            request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"]["serviceAccounts"] = {
                    "accounts": [
                        {
                            "serviceType": service_type["Sharepoint Online"],
                            "userAccount": {
                                "password": user_password,
                                "userName": kwargs.get('user_username')
                            }
                        }
                    ]
                }
            if kwargs.get('is_modern_auth_enabled'):
                azure_app_key_id = b64encode(kwargs.get('azure_app_key_id').encode()).decode()

                azure_app_dict = {
                    "azureAppId": kwargs.get('azure_app_id'),
                    "azureAppKeyValue": azure_app_key_id,
                    "azureDirectoryId": kwargs.get('azure_directory_id')
                }

                if 'cert_string' in kwargs:
                    # cert_string needs to be encoded twice
                    cert_string = b64encode(kwargs.get('cert_string')).decode()
                    cert_string = b64encode(cert_string.encode()).decode()

                    cert_password = b64encode(kwargs.get('cert_password').encode()).decode()

                    cert_dict = {
                        "certificate": {
                            "certBase64String": cert_string,
                            "certPassword": cert_password
                        }
                    }
                    azure_app_dict.update(cert_dict)

                request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                    "spOffice365BackupSetProp"]["azureAppList"] = {
                    "azureApps": [
                        azure_app_dict
                    ]
                }
        if kwargs.get('azure_username'):
            azure_secret = b64encode(kwargs.get('azure_secret').encode()).decode()
            request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"]["serviceAccounts"]["accounts"].append(
                {
                    "serviceType": service_type["Sharepoint Azure Storage"],
                    "userAccount": {
                        "password": azure_secret,
                        "userName": kwargs.get('azure_username')
                    }
                }
            )
        if len(access_nodes_list) > 1:
            request_json["clientInfo"]["sharepointPseudoClientProperties"]["jobResultsDir"] = {
                "path": kwargs.get('shared_jr_directory').get('Path')
            }
            request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"]["serviceAccounts"]["accounts"].append(
                {
                    "serviceType": 3,
                    "userAccount": {
                        "userName": kwargs.get('shared_jr_directory').get('Username'),
                        "password": b64encode(kwargs.get('shared_jr_directory').get('Password').encode()).decode()
                    }
                })
        if is_resource_pool_enabled:
            request_json["clientInfo"]["useResourcePoolInfo"] = is_resource_pool_enabled

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

    def add_yugabyte_client(self,
                            instance_name,
                            db_host,
                            api_token,
                            universe_name,
                            config_name,
                            credential_name,
                            content,
                            plan_name,
                            data_access_nodes,
                            user_uuid,
                            universe_uuid,
                            config_uuid):

        """
        Adds new yugabyte client
        Args:
            instance_name            (str)   --  new yugabyte instance name

            db_host                  (str)   --  hostname of the yugabyteanywhere application

            api_token                (str)   --  apiToken of the yugabyteanywhere user

            universe_name            (str)   --  universe name to be backed up

            config_name              (str)   --  customer configuration name

            credential_name          (str)   --  credential name associated with customer config

            content                  (str)   --  content of the default subclient

            plan_name                (str)   -- name of the plan to be associated

            data_access_nodes        (str)   -- list of data access nodes to be used

            user_uuid                (str)   --  UUID of the yugabytedb user

            universe_uuid            (str)   --  UUID of the yugabytedb universe

            config_uuid              (str)   --  UUID of the yugabytedb user configuration

        Returns:
                client_object     (obj)   --  client object associated with the new yugabyte client

        Raises:
            SDKException:
                if failed to add the client

                if response is empty

                if response is not success
        """

        content_temp = []
        for path in content:
            content_temp.append({"path": path})

        access_nodes = []
        for node in data_access_nodes:
            access_nodes.append({"clientName": node})

        apitoken_temp = b64encode(api_token.encode()).decode()

        request_json = {
            "createPseudoClientRequest": {
                "clientInfo": {
                    "clientType": 29,
                    "plan": {
                        "planName": plan_name
                    },
                    "subclientInfo": {
                        "contentOperationType": 1,
                        "content": content_temp
                    },
                    "distributedClusterInstanceProperties": {
                        "clusterType": 19,
                        "opType": 2,
                        "instance": {
                            "instanceId": 0,
                            "instanceName": instance_name,
                            "clientName": instance_name,
                            "applicationId": 64
                        },
                        "clusterConfig": {
                            "yugabytedbConfig": {
                                "dbHost": db_host,
                                "apiToken": apitoken_temp,
                                "customer": {
                                    "name": "",
                                    "uuid": user_uuid
                                },
                                "universe": {
                                    "name": universe_name,
                                    "uuid": universe_uuid
                                },
                                "customerConfig": {
                                    "name": config_name,
                                    "uuid": config_uuid
                                }
                            },
                            "config": {
                                "staging": {
                                    "stagingType": 1,
                                    "stagingCredentials": {
                                        "credentialName": credential_name,
                                    }
                                }
                            }
                        },
                        "dataAccessNodes": {
                            "dataAccessNodes": access_nodes
                        }
                    }
                },
                "entity": {
                    "clientName": instance_name
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_YUGABYTE_CLIENT, request_json
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
                        return self.get(instance_name)

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

    def add_couchbase_client(self,
                             instance_name,
                             data_access_nodes,
                             user_name,
                             password,
                             port,
                             staging_type,
                             staging_path,
                             credential_name,
                             service_host,
                             plan_name,
                             ):
        """
        Adds new couchbase client
        Args:

                instance_name            (str)   --  new couchbase instance name

                data_access_nodes        (str)   -- list of data access nodes to be used

                user_name                (str)   --  couchbase admin username

                password                 (str)   --  couchbase admin password

                port                     (str)   --  couchbase db port

                staging_type             (str)   --  staging type : FileSystem or S3

                staging_path             (str)   --  staging path

                credential_name          (str)   --  name of the s3 credential

                service_host             (str)   --  aws service host

                plan_name                (str)   --  name of the plan to be associated



            Returns:
                    client_object     (obj)   --  client object associated with the new couchbase client

            Raises:
                SDKException:
                    if failed to add the client

                    if response is empty

                    if response is not success"""

        access_nodes = []
        for node in data_access_nodes:
            access_nodes.append({"clientName": node})
        pwd = b64encode(password.encode()).decode()

        port = int(port)

        if staging_type == "FileSystem":
            request_json = {
                "createPseudoClientRequest": {
                    "clientInfo": {
                        "clientType": 29,
                        "plan": {
                            "planName": plan_name
                        },
                        "distributedClusterInstanceProperties": {
                            "clusterType": 17,
                            "opType": 2,
                            "instance": {
                                "instanceId": 0,
                                "instanceName": instance_name,
                                "clientName": instance_name,
                                "applicationId": 64
                            },
                            "clusterConfig": {
                                "couchbaseConfig": {
                                    "port": port,
                                    "user": {
                                        "userName": user_name,
                                        "password": pwd
                                    },
                                    "staging": {
                                        "stagingType": 0,
                                        "stagingPath": staging_path
                                    }
                                }
                            },
                            "dataAccessNodes": {
                                "dataAccessNodes": access_nodes
                            }
                        }
                    },
                    "entity": {
                        "clientName": instance_name
                    }
                }
            }

        else:
            request_json = {
                "createPseudoClientRequest": {
                    "clientInfo": {
                        "clientType": 29,
                        "plan": {
                            "planName": plan_name
                        },
                        "distributedClusterInstanceProperties": {
                            "clusterType": 17,
                            "opType": 2,
                            "instance": {
                                "instanceId": 0,
                                "instanceName": instance_name,
                                "clientName": instance_name,
                                "applicationId": 64
                            },
                            "clusterConfig": {
                                "couchbaseConfig": {
                                    "port": port,
                                    "user": {
                                        "userName": user_name,
                                        "password": pwd
                                    },
                                    "staging": {
                                        "stagingType": 1,
                                        "stagingPath": staging_path,
                                        "serviceHost": service_host,
                                        "instanceType": 5,
                                        "cloudURL": "s3.amazonaws.com",
                                        "recordType": "AMAZON_S3",
                                        "stagingCredentials": {
                                            "credentialName": credential_name
                                        }
                                    }
                                }
                            },
                            "dataAccessNodes": {
                                "dataAccessNodes": access_nodes
                            }
                        }
                    },
                    "entity": {
                        "clientName": instance_name
                    }
                }
            }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_COUCHBASE_CLIENT, request_json
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
                        return self.get(instance_name)

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
            server_plan,
            recall_service_url,
            job_result_dir,
            exchange_servers,
            service_accounts,
            azure_app_key_secret,
            azure_tenant_name,
            azure_app_key_id,
            environment_type,
            backupset_type_to_create = 1,
            **kwargs):
        """Adds a new Exchange Mailbox Client to the Commcell.

            Args:
                client_name             (str)   --  name of the new Exchange Mailbox Client

                index_server            (str)   --  index server for virtual client

                clients_list            (list)  --  list containing client names / client objects,
                to associate with the Virtual Client

                server_plan          (str)   --  server_plan to associate with the client

                recall_service_url      (str)   --  recall service for client

                job_result_dir          (str)   --  job result directory path

                exchange_servers        (list)  --  list of exchange servers

                azure_app_key_secret    (str)   --  app secret for the Exchange online

                azure_tenant_name       (str)   --  tenant for exchange online

                azure_app_key_id        (str)   --  app key for exchange online

                environment_type        (int)   --  Exchange Environment Type for the Client.
                    Supported Value and corresponding types:
                        1   :   Exchange on- premise
                        2   :   Exchange Hybrid with on- premise Exchange Server
                        3   :   Exchange Hybrid with on- premise AD
                        4   :   Exchange Online

                backupset_type_to_create (int)  --  Backup set type to create
                    Supported Value and corresponding types:
                        1   :   user mailbox
                        2   :   journal mailbox
                        3   :   content store mailbox
                    Default Value: 1 (user mailbox)

                kwargs                  (dict)  --  Extra/ Additional Arguments
                    Accepted Values:
                        is_modern_auth_enabled  --
                            (bool)  --  Whether to create Exchange Online client with modern auth
                                        enabled
                            Default Value:
                                True
                            Applicable For:
                                Exchange Online Client


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
        server_plan_dict = {}

        if self.has_client(index_server):
            index_server_cloud = self.get(index_server)

            if index_server_cloud.agents.has_agent(AppIDAName.BIG_DATA_APPS.value):
                index_server_dict = {
                    "mediaAgentId": int(index_server_cloud.client_id),
                    "_type_": 11,
                    "mediaAgentName": index_server_cloud.client_name
                }

        if self._commcell_object.plans.has_plan(server_plan):
            server_plan_object = self._commcell_object.plans.get(server_plan)

            server_plan_dict = {
                "planId": int(server_plan_object.plan_id)
            }

        account_list = []
        member_servers = []

        for client in clients_list:
            if isinstance(client, str):
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


        server_plan_resources = server_plan_object._properties.get('storageResourcePoolMap')[0].get('resources')

        # use resource pool only if resource pool type is Office365 or Exchange
        is_resource_pool_enabled = False
        if server_plan_resources is not None:
            for resourse in server_plan_resources:
                if resourse.get('appType', 0) in (ResourcePoolAppType.O365.value, ResourcePoolAppType.EXCHANGE.value):
                    is_resource_pool_enabled = True

        request_json = {
            "clientInfo": {
                "clientType": 25,
                "plan": server_plan_dict,
                "exchangeOnePassClientProperties": {
                    "backupSetTypeToCreate" : backupset_type_to_create,
                    "recallService": recall_service_url,
                    "onePassProp": {
                        "environmentType": environment_type,
                        "servers": exchange_servers,
                        "accounts": {
                            "adminAccounts": account_list
                        }

                    },
                    "memberServers": {
                        "memberServers": member_servers
                    },
                    "indexServer": index_server_dict,
                    "jobResulsDir": {
                        "path": job_result_dir
                    }
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        if int(self._commcell_object.version.split(".")[1]) >= 23:
            azure_app_dict = {
                            "azureApps": [
                                {
                                    "azureDirectoryId": azure_tenant_name,
                                    "azureAppKeyValue": azure_app_key_secret,
                                    "azureAppId": azure_app_key_id,
                                    "appStatus": 1,
                                    "azureAppType": 1
                                }
                            ]
                        }
            request_json["clientInfo"]["exchangeOnePassClientProperties"]["onePassProp"][
                "azureAppList"] = azure_app_dict
        else:
            azure_app_dict = {
                            "azureAppKeySecret": azure_app_key_secret,
                            "azureTenantName": azure_tenant_name,
                            "azureAppKeyID": azure_app_key_id
                        }
            request_json["clientInfo"]["exchangeOnePassClientProperties"]["onePassProp"][
                "azureDetails"] = azure_app_dict

        if int(self._commcell_object.version.split(".")[1]) >= 25 and (environment_type == 4 or environment_type == 2) :
            request_json["clientInfo"]["clientType"] = 37 #37 - Office365 Client type. Exchange Online falls under O365 AppType
            request_json["clientInfo"]["exchangeOnePassClientProperties"]["onePassProp"][
                "isModernAuthEnabled"] = kwargs.get('is_modern_auth_enabled', True)
        if is_resource_pool_enabled:
            request_json["clientInfo"]["useResourcePoolInfo"] = is_resource_pool_enabled

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
            self,
            client_name,
            access_node,
            salesforce_options,
            db_options=None,
            **kwargs
    ):
        """Adds a new Salesforce Client to the Commcell.

            Args:
                client_name          (str)    --    salesforce pseudo client name
                access_node          (str)    --    access node name

                salesforce_options   (dict)   --    salesforce options
                                                    {
                                                        "login_url": 'salesforce login url',
                                                        "consumer_id": 'salesforce consumer key',
                                                        "consumer_secret": 'salesforce consumer secret',
                                                        "salesforce_user_name": 'salesforce login user',
                                                        "salesforce_user_password": 'salesforce user password',
                                                        "salesforce_user_token": 'salesforce user token',
                                                        "sandbox": True or False (default False)
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
        if self.has_client(client_name):
            raise SDKException('Client', '102', 'Client "{0}" already exists.'.format(client_name))
        if not salesforce_options.get("consumer_secret", None) or \
                not salesforce_options.get('salesforce_user_password', None):
            raise SDKException('Client', '102', 'Missing inputs. Check salesforce_options dictionary')
        if db_options is None:
            db_options = {'db_enabled': False}
        request_json = {
            "clientInfo": {
                "clientType": 15,
                "cloudClonnectorProperties": {
                    "instanceType": 3,
                    "instance": {
                        "instance": {
                            "clientName": client_name,
                            "instanceName": kwargs.get("instance_name", client_name),
                        },
                        "cloudAppsInstance": {
                            "instanceType": 3,
                            "salesforceInstance": {
                                "enableREST": True,
                                "endpoint": salesforce_options.get("login_url", "https://login.salesforce.com"),
                                "consumerId": salesforce_options.get("consumer_id"),
                                "consumerSecret": b64encode(
                                    salesforce_options.get("consumer_secret").encode()).decode(),
                                "defaultBackupsetProp": {
                                    "downloadCachePath": kwargs.get("download_cache_path", "/tmp"),
                                    "mutualAuthPath": kwargs.get("mutual_auth_path", ""),
                                    "token": b64encode(
                                        salesforce_options.get("salesforce_user_token", "").encode()).decode(),
                                    "userPassword": {
                                        "userName": salesforce_options.get("salesforce_user_name"),
                                        "password": b64encode(
                                            salesforce_options.get("salesforce_user_password").encode()).decode()
                                    }
                                }
                            },
                            "generalCloudProperties": {
                                "numberOfBackupStreams": kwargs.get("streams", 2),
                                "accessNodes": {
                                    "memberServers": [{
                                        "client": {
                                            "clientName": access_node,
                                            "_type_": 3
                                        }
                                    }]
                                },
                                "storageDevice": {
                                    "dataBackupStoragePolicy": {
                                        "storagePolicyName": kwargs.get("storage_policy", "")
                                    }
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
        if db_options.get("db_enabled", True):
            if not db_options.get('db_password', None):
                raise SDKException('Client', '102', 'Missing inputs. Check db_options dictionary')
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"] \
                ["salesforceInstance"]["defaultBackupsetProp"]["syncDatabase"] = {
                "dbPort": str(
                    db_options.get("db_port", 1433 if db_options.get("db_type", None) == "SQLSERVER" else 5432)),
                "dbEnabled": True,
                "dbName": db_options.get("db_name"),
                "dbType": db_options.get("db_type", "POSTGRESQL"),
                "dbHost": db_options.get("db_host_name"),
                "dbUserPassword": {
                    "userName": db_options.get("db_user_name"),
                    "password": b64encode(db_options.get("db_password").encode()).decode()
                }
            }
            if db_options.get('db_instance', None):
                request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"] \
                    ["salesforceInstance"]["defaultBackupsetProp"]["syncDatabase"]["db_instance"] = db_options[
                    "db_instance"]
        self._process_add_response(request_json, self._ADD_SALESFORCE_CLIENT)

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
                AccessKey and Secretkey authentication
                                            Example:
                                               amazon_options = {
                                                    "accessKey": amazon_options.get("accessKey"),
                                                    "secretkey": amazon_options.get("secretkey")
                                                }
                IAM authentication ( pass the key value pair "useIamRole":True )
                                            Example:
                                               amazon_options = {
                                                    "useIamRole": amazon_options.get("useIamRole"),
                                                }
                STS Role Authentication ( pass the Role arn Name in accessKey of amazon_options)
                                            Example:
                                               amazon_options = {
                                                    "accessKey": amazon_options.get("accessKey"),
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

        # IAM Authentication
        if "useIamRole" in amazon_options:
            amazon_options["accessKey"] = ''
            amazon_options["secretkey"] = ''
            amazon_options["useIamRole"] = True
        # Accesskey and secretkey authentication
        elif "secretkey" in amazon_options:
            amazon_options["useIamRole"] = False
        # STS Role ARN authentication
        else:
            amazon_options["secretkey"] = ''
            amazon_options["useIamRole"] = False

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

    def add_googleworkspace_client(self, plan_name, client_name, indexserver,
                                   service_account_details, credential_name,
                                   instance_type, **kwargs):
        """
                    Method to add new google cloud client
                    Args:
                        plan_name (str): Name of server plan
                        client_name (str): The name to be assigned to the client.
                        indexserver (str): The index server address used for the client.
                        credential_name (str): Credential Name that created in Credential Vault.
                        instance_type (int): Type of Google client
                        service_account_details (dict): A dictionary containing service account details
                                                        required for authentication and authorization.
                                                           Example:
                                                           "ServiceAccountDetails": {
                                                                   "accounts": [
                                                                     {
                                                                       "serviceType": "ExampleAgentServiceType",
                                                                       "AdminSmtpAddress": "example@google.com"
                                                                     }
                                                                   ]
                                                           }
                        **kwargs (dict) : Additional parameters.
                                            client_group_name (str) : Access Node Group Name.
                                            access_node (str) : Access Node name.
                                            jr_path (str): Job Results Dir path. Mandatory if client_group_name is provided.
                                            no_of_streams(int): Number of streams to create a client.
                                          Note:
                                            Either client_group_name or access_node should be provided.
                                            If both are given client_group_name will be treated as default.
                    Returns:
                        object  -   instance of the Client class for this new client
                    Raises:
                        SDKException:
                            if client_group_name is given None

        """
        is_client_group = True if kwargs.get('client_group_name') else False
        proxy_node = kwargs.get('client_group_name') if is_client_group else kwargs.get('access_node')
        if proxy_node is None:
            raise SDKException(
                'Client',
                '102',
                "Either client_group_name or access_node should be provided.")
        account_dict = service_account_details["accounts"]
        for account in account_dict:
            if account['serviceType'] == "SYSTEM_ACCOUNT":
                account["userAccount"]["password"] = b64encode(
                    account["userAccount"]["password"].encode()).decode()
                account["userAccount"]["confirmPassword"] = b64encode(
                    account["userAccount"]["confirmPassword"].encode()).decode()

        request_payload = {
            "clientInfo": {
                "clientType": 37,
                "plan": {
                    "planName": plan_name
                },
                "cloudClonnectorProperties": {
                    "instanceType": instance_type,
                    "instance": {
                        "instance": {
                            "clientName": client_name,
                            "instanceName": f"{client_name}_Instance001"
                        },
                        "cloudAppsInstance": {
                            "instanceType": instance_type,
                            "generalCloudProperties": {
                                "memberServers": [
                                    {
                                        "client": {
                                            "clientGroupName" if is_client_group else "clientName": proxy_node
                                        }
                                    }
                                ],
                                "indexServer": {
                                    "clientName": indexserver
                                },
                                "numberOfBackupStreams": kwargs.get('no_of_streams', 10),
                                "jobResultsDir": {
                                    "path": kwargs.get('jr_path') if is_client_group else ""
                                }
                            },
                            "v2CloudAppsInstance": {
                                "cloudRegion": "DEFAULT",
                                "serviceAccounts": service_account_details,
                                "connectionCredential": {
                                    "credentialName": credential_name
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

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_GOOGLE_CLIENT, request_payload
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

    def add_teams_client(self, client_name, server_plan, azure_app_id, azure_directory_id,
                     azure_app_key_id, **kwargs):
        """
            Adds Teams client

            Args:
                client_name (str) : Client Name
                server_plan (str) : Server Plan's Name
                azure_app_id (str) : Azure app ID
                azure_directory_id (str) : Azure directory ID
                azure_app_key_id (str) : Azure App key ID

                **kwargs (dict) : Additional parameters
                    index_server (str) : Index Server's Name
                    access_nodes_list (list[str/object]) : List of names/objects of access node clients
                    number_of_backup_streams (int) : Number of backup streams to be associated (default: 10)
                    user_name (str) : User name for shared job results
                    user_password (str) : User password for shared job results
                    shared_jr_directory (str) : Shared Job results directory path
                    cloud_region(int) : Cloud region for the client which determines the gcc or gcc high configuration

            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if server plan  donot exists with the given name

                    if data type of the input(s) is not valid

                    if access node do not exists with the given name

                    if failed to add the client

                    if response is empty

                    if response is not success
        """

        if self.has_client(client_name):
            raise SDKException('Client', '102', f'Client "{client_name}" already exists.')

        # Get server plan details
        server_plan_object = self._commcell_object.plans.get(server_plan)
        server_plan_id = int(server_plan_object.plan_id)
        server_plan_resources = server_plan_object._properties.get('storageResourcePoolMap')[0].get('resources')

        access_nodes_list = kwargs.get('access_nodes_list')
        index_server = kwargs.get('index_server')

        # use resource pool only if resource pool type is Office365 or OneDrive
        is_resource_pool_enabled = False
        if server_plan_resources is not None:
            for resourse in server_plan_resources:
                if resourse.get('appType', 0) in (1, 5):  # ResourcePoolAppType.O365 or ResourcePoolAppType.OneDrive
                    is_resource_pool_enabled = True

        number_of_backup_streams = kwargs.get('number_of_backup_streams', 10)
        user_name = kwargs.get('user_name')
        user_password = kwargs.get('user_password')
        shared_jr_directory = kwargs.get('shared_jr_directory')
        cloud_region = kwargs.get('cloud_region', 1)

        # If server plan is not resource pool enabled and infrastructure details are not provided, raise Exception
        if not is_resource_pool_enabled and (access_nodes_list is None or index_server is None):
            error_string = 'For a non resource-pool server plan, access nodes and index server details are necessary'
            raise SDKException('Client', '102', error_string)

        # If data type of the input(s) is not valid, raise Exception
        if ((access_nodes_list and not isinstance(access_nodes_list, list)) or
                (index_server and not isinstance(index_server, str)) or
                (number_of_backup_streams and not isinstance(number_of_backup_streams, int)) or
                (user_name and not isinstance(user_name, str)) or
                (user_password and not isinstance(user_password, str)) or
                (shared_jr_directory and not isinstance(shared_jr_directory, str))):
            raise SDKException('Client', '101')

        # For multiple access nodes, make sure service account details are provided
        if (access_nodes_list and len(access_nodes_list) > 1 and
                (user_name is None or user_password is None or shared_jr_directory is None)):
            error_string = 'For creating a multi-access node client service account details are necessary'
            raise SDKException('Client', '102', error_string)

        # Get index server details
        index_server_id = None
        if index_server:
            index_server_object = self.get(index_server)
            index_server_id = int(index_server_object.client_id)

        # For each access node create client object
        member_servers = []

        if access_nodes_list:
            for client in access_nodes_list:
                if isinstance(client, str):
                    client = client.strip().lower()

                    if self.has_client(client):
                        client_dict = {
                            "client": {
                                "clientName": client,
                                "clientId": int(self.all_clients.get(client).get('id')),
                                "_type_": 3
                            }
                        }
                        member_servers.append(client_dict)
                    else:
                        raise SDKException('Client', '102', f'Client {client} does not exitst')

                elif isinstance(client, Client):
                    if self.has_client(client):
                        client_dict = {
                            "client": {
                                "clientName": client.client_name,
                                "clientId": int(client.client_id),
                                "_type_": 3
                            }
                        }
                        member_servers.append(client_dict)
                    else:
                        raise SDKException('Client', '102', f'Client {client} does not exitst')

                else:
                    raise SDKException('Client', '101')

        azure_app_key_value = b64encode(azure_app_key_id.encode()).decode()

        request_json = {
            "clientInfo": {
                "clientType": 37,
                "useResourcePoolInfo": is_resource_pool_enabled,
                "plan": {
                    "planId": server_plan_id
                },
                "cloudClonnectorProperties": {
                    "instanceType": 36,
                    "instance": {
                        "instance": {
                            "clientName": client_name
                        },
                        "cloudAppsInstance": {
                            "instanceType": 36,
                            "serviceAccounts": {},
                            "v2CloudAppsInstance": {
                                "advanceSettings": {
                                        "channelChatOpMode": 1,
                                        "isPersonalChatOperationsEnabled": False
                                    },
                                "cloudRegion": cloud_region,
                                "callbackUrl": "",
                                "createAdditionalSubclients": False,
                                "infraStructurePoolEnabled": False,
                                "isAutoDiscoveryEnabled": False,
                                "isEnterprise": True,
                                "isModernAuthEnabled": False,
                                "manageContentAutomatically": False,
                                "numberofAdditionalSubclients": 0,
                                "serviceAccounts": {
                                    "accounts": [
                                    ]
                                },
                                "tenantInfo": {
                                    "azureTenantID": azure_directory_id
                                },
                                "azureAppList": {
                                    "azureApps": [
                                        {
                                            "appStatus": 1,
                                            "azureAppType": 2,
                                            "azureDirectoryId": azure_directory_id,
                                            "azureAppDisplayName": azure_app_id,
                                            "azureAppKeyValue": azure_app_key_value,
                                            "azureAppId": azure_app_id
                                        }
                                    ]
                                }
                            },
                            "generalCloudProperties": {
                                "numberOfBackupStreams": number_of_backup_streams,
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

        if not is_resource_pool_enabled:
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "generalCloudProperties"]["indexServer"] = {
                "clientId": index_server_id
            }
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "generalCloudProperties"]["memberServers"] = member_servers

        if access_nodes_list and len(access_nodes_list) > 1:
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "generalCloudProperties"]["jobResultsDir"]["path"] = shared_jr_directory

        if user_name:
            user_password = b64encode(user_password.encode()).decode()
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "oneDriveInstance"][
                "serviceAccounts"] = {
                "accounts": [
                    {
                        "serviceType": 3,
                        "userAccount": {
                            "userName": user_name,
                            "password": user_password
                        }
                    }
                ]
            }

        self._process_add_response(request_json, self._ADD_ONEDRIVE_CLIENT)


    def add_onedrive_for_business_client(
            self,
            client_name,
            server_plan,
            azure_app_id,
            azure_directory_id,
            azure_app_key_id,
            **kwargs):

        """
            Adds OneDrive for Business (v2) client

            Args:
                client_name (str) : Client Name
                server_plan (str) : Server Plan's Name
                azure_app_id (str) : Azure app ID
                azure_directory_id (str) : Azure directory ID
                azure_app_key_id (str) : Azure App key ID

                **kwargs (dict) : Additional parameters
                    index_server (str) : Index Server's Name
                    access_nodes_list (list[str/object]) : List of names/objects of access node clients
                    number_of_backup_streams (int) : Number of backup streams to be associated (default: 10)
                    user_name (str) : User name for shared job results
                    user_password (str) : User password for shared job results
                    shared_jr_directory (str) : Shared Job results directory path
                    cloud_region(int) : Cloud region for the client which determines the gcc or gcc high configuration

            Returns:
                object  -   instance of the Client class for this new client

            Raises:
                SDKException:
                    if client with given name already exists

                    if server plan  donot exists with the given name

                    if data type of the input(s) is not valid

                    if access node do not exists with the given name

                    if failed to add the client

                    if response is empty

                    if response is not success
        """

        # If client with given name already exists, raise Exception
        if self.has_client(client_name):
            raise SDKException('Client', '102', f'Client "{client_name}" already exists.')

        # Get server plan details
        server_plan_object = self._commcell_object.plans.get(server_plan)
        server_plan_id = int(server_plan_object.plan_id)
        server_plan_resources = server_plan_object._properties.get('storageResourcePoolMap')[0].get('resources')

        access_nodes_list = kwargs.get('access_nodes_list')
        index_server = kwargs.get('index_server')

        # use resource pool only if resource pool type is Office365 or OneDrive
        is_resource_pool_enabled = False
        if server_plan_resources is not None:
            for resourse in server_plan_resources:
                if resourse.get('appType', 0) in (1, 5):  # ResourcePoolAppType.O365 or ResourcePoolAppType.OneDrive
                    is_resource_pool_enabled = True

        number_of_backup_streams = kwargs.get('number_of_backup_streams', 10)
        user_name = kwargs.get('user_name')
        user_password = kwargs.get('user_password')
        shared_jr_directory = kwargs.get('shared_jr_directory')
        cloud_region = kwargs.get('cloud_region', 1)

        # If server plan is not resource pool enabled and infrastructure details are not provided, raise Exception
        if not is_resource_pool_enabled and (access_nodes_list is None or index_server is None):
            error_string = 'For a non resource-pool server plan, access nodes and index server details are necessary'
            raise SDKException('Client', '102', error_string)

        # If data type of the input(s) is not valid, raise Exception
        if ((access_nodes_list and not isinstance(access_nodes_list, list)) or
                (index_server and not isinstance(index_server, str)) or
                (number_of_backup_streams and not isinstance(number_of_backup_streams, int)) or
                (user_name and not isinstance(user_name, str)) or
                (user_password and not isinstance(user_password, str)) or
                (shared_jr_directory and not isinstance(shared_jr_directory, str))):
            raise SDKException('Client', '101')

        # For multiple access nodes, make sure service account details are provided
        if (access_nodes_list and len(access_nodes_list) > 1 and
                (user_name is None or user_password is None or shared_jr_directory is None)):
            error_string = 'For creating a multi-access node client service account details are necessary'
            raise SDKException('Client', '102', error_string)

        # Get index server details
        index_server_id = None
        if index_server:
            index_server_object = self.get(index_server)
            index_server_id = int(index_server_object.client_id)

        # For each access node create client object
        member_servers = []

        if access_nodes_list:
            for client in access_nodes_list:
                if isinstance(client, str):
                    client = client.strip().lower()

                    if self.has_client(client):
                        client_dict = {
                            "client": {
                                "clientName": client,
                                "clientId": int(self.all_clients.get(client).get('id')),
                                "_type_": 3
                            }
                        }
                        member_servers.append(client_dict)
                    else:
                        raise SDKException('Client', '102', f'Client {client} does not exitst')

                elif isinstance(client, Client):
                    if self.has_client(client):
                        client_dict = {
                            "client": {
                                "clientName": client.client_name,
                                "clientId": int(client.client_id),
                                "_type_": 3
                            }
                        }
                        member_servers.append(client_dict)
                    else:
                        raise SDKException('Client', '102', f'Client {client} does not exitst')

                else:
                    raise SDKException('Client', '101')

        azure_app_key_value = b64encode(azure_app_key_id.encode()).decode()

        request_json = {
            "clientInfo": {
                "clientType": 37,
                "useResourcePoolInfo": is_resource_pool_enabled,
                "plan": {
                    "planId": server_plan_id
                },
                "cloudClonnectorProperties": {
                    "instanceType": 7,
                    "instance": {
                        "instance": {
                            "clientName": client_name
                        },
                        "cloudAppsInstance": {
                            "instanceType": 7,
                            "serviceAccounts": {},
                            "oneDriveInstance": {
                                "manageContentAutomatically": False,
                                "isAutoDiscoveryEnabled": False,
                                "cloudRegion": cloud_region,
                                "azureAppList": {
                                    "azureApps": [
                                        {
                                            "azureDirectoryId": azure_directory_id,
                                            "azureAppDisplayName": azure_app_id,
                                            "azureAppKeyValue": azure_app_key_value,
                                            "azureAppId": azure_app_id
                                        }
                                    ]
                                }
                            },
                            "generalCloudProperties": {
                                "numberOfBackupStreams": number_of_backup_streams,
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

        if not is_resource_pool_enabled:
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "generalCloudProperties"]["indexServer"] = {
                "clientId": index_server_id
            }
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "generalCloudProperties"]["memberServers"] = member_servers

        if access_nodes_list and len(access_nodes_list) > 1:
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "generalCloudProperties"]["jobResultsDir"]["path"] = shared_jr_directory

        if user_name:
            user_password = b64encode(user_password.encode()).decode()
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "oneDriveInstance"][
                "serviceAccounts"] = {
                "accounts": [
                    {
                        "serviceType": 3,
                        "userAccount": {
                            "userName": user_name,
                            "password": user_password
                        }
                    }
                ]
            }

        self._process_add_response(request_json, self._ADD_ONEDRIVE_CLIENT)

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
                        if isinstance(access_node, str):
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

    def add_cassandra_client(self,
                             new_client_name,
                             gatewaynode,
                             cql_port,
                             cql_username,
                             cql_password,
                             jmx_port,
                             config_file_path,
                             plan_name):
        """
        Adds new cassandra client after clientname and plan validation

        Args:
            new_client_name       (str)   --  new cassandra client name

            gatewaynode           (str)   --  gateway node

            cql_port              (int)   --  cql port

            jmx_port              (int)   --  jmx port

            cql_username          (str)   --  cql username

            cql_password          (str)   --  cql password

            plan_name             (str)   --  plan name

        Returns:
                client_object     (obj)   --  client object associated with the new cassandra client

        Raises:
            SDKException:
                if plan name is not valid

                if failed to add the client

                if response is empty

                if response is not success
        """
        if self._commcell_object.plans.has_plan(plan_name):
            plan_object = self._commcell_object.plans.get(plan_name)
            plan_id = int(plan_object.plan_id)
            plan_type = int(plan_object.plan_type)
            plan_subtype = int(plan_object.subtype)
        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        cql_password = b64encode(cql_password.encode()).decode()
        jmx_port_int = int(jmx_port)
        cql_port_int = int(cql_port)

        request_json = {
            "clientInfo": {
                "clientType": 29,
                "plan": {
                    "planName": plan_name
                },
                "distributedClusterInstanceProperties": {
                    "clusterType": 9,
                    "opType": 2,
                    "instance": {
                        "instanceId": 0,
                        "instanceName": new_client_name,
                        "clientName": new_client_name,
                        "applicationId": 64
                    },
                    "clusterConfig": {
                        "cassandraConfig": {
                            "gateway": {
                                "node": {
                                    "clientNode": {
                                        "clientName": gatewaynode
                                    },
                                    "jmxConnection": {
                                        "port": jmx_port_int
                                    }
                                },
                                "gatewayCQLPort": cql_port_int,
                                "gatewayCQLUser": {
                                    "userName": cql_username,
                                    "password": cql_password,
                                    "confirmPassword": cql_password
                                }
                            },
                            "configFilePath": config_file_path
                        }
                    }
                }
            },
            "entity": {
                "clientName": new_client_name
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_CASSANDRA_CLIENT, payload=request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json(
                        )['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(
                            error_string)

                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(new_client_name)

                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(
                        error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def add_cockroachdb_client(self,
                               new_client_name,
                               s3_credential_name,
                               cockroachdb_host,
                               cockroachdb_port,
                               db_username,
                               db_password,
                               sslcert,
                               sslkey,
                               sslrootcert,
                               s3_service_host,
                               s3_staging_path,
                               accessnodes,
                               plan_name):
        """
        Adds new cockroachdb client after clientname and plan validation

        Args:
            new_client_name       (str)   --  new cockroachdb client name

            s3_credential_name    (str)   --  AWS S3 credential name

            cockroachdb_host      (str)   --  cockroachdb host machine name or ip

            cockroachdb_port      (int)   --  cockroachdb port number

            db_username           (str)   --  database user name

            db_password           (str)   --  database password

            sslcert                (str)  --  ssl cert path

            sslkey                 (str)  --  ssl key path

            sslrootcert           (str)   --  ssl root cert path

            s3_service_host       (str)   --  s3 service host

            s3_staging_path       (str)   --  s3 staging path

            accessnodes           (list)  --  list of access nodes

            plan_name             (str)   --  plan assocated with the new client

        Returns:
                client_object     (obj)   --  client object associated with the new cockroachdb client

        Raises:
            SDKException:
                if plan name is not valid

                if failed to add the client

                if response is empty

                if response is not success
        """
        if self._commcell_object.plans.has_plan(plan_name):
            plan_object = self._commcell_object.plans.get(plan_name)
            plan_id = int(plan_object.plan_id)
            plan_type = int(plan_object.plan_type)
            plan_subtype = int(plan_object.subtype)
        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        access_nodes = []
        for node in accessnodes:
            client_object = self._commcell_object.clients.get(node)
            client_id = int(client_object.client_id)
            access_node = {
                "hostName": "",
                "clientId": client_id,
                "clientName": client_object.client_name,
                "displayName": client_object.display_name,
                "selected": True
            }
            access_nodes.append(access_node)

        db_password = b64encode(db_password.encode()).decode()
        cockroachdb_port = int(cockroachdb_port)

        request_json = {
            "createPseudoClientRequest": {
                "clientInfo": {
                    "clientType": 29,
                    "distributedClusterInstanceProperties": {
                        "clusterConfig": {
                            "cockroachdbConfig": {
                                "dbCredentials": {
                                    "credentialId": 0,
                                    "credentialName": ""
                                },
                                "dbHost": cockroachdb_host,
                                "port": cockroachdb_port,
                                "sslCert": sslcert,
                                "sslKey": sslkey,
                                "sslRootCert": sslrootcert,
                                "staging": {
                                    "cloudURL": "s3.amazonaws.com",
                                    "instanceType": 5,
                                    "recordType": 102,
                                    "serviceHost": s3_service_host,
                                    "stagingCredentials": {
                                        "credentialName": s3_credential_name
                                    },
                                    "stagingPath": s3_staging_path,
                                    "stagingType": 1
                                },
                                "user": {
                                    "password": db_password,
                                    "userName": db_username
                                }
                            }
                        },
                        "clusterType": 18,
                        "dataAccessNodes": {
                            "dataAccessNodes": access_nodes
                        },
                        "instance": {
                            "applicationId": 64,
                            "clientName": new_client_name,
                            "instanceId": 0,
                            "instanceName": new_client_name
                        },
                        "opType": 2
                    },
                    "plan": {
                        "planName": plan_name,
                    },
                    "subclientInfo": {
                        "content": [
                            {
                                "path": "/"
                            }
                        ],
                        "contentOperationType": 1,
                        "fsSubClientProp": {
                            "useGlobalFilters": "USE_CELL_LEVEL_POLICY"
                        },
                        "useLocalContent": True
                    }
                },
                "entity": {
                    "clientName": new_client_name
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_COCKROACHDB_CLIENT, payload=request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json(
                        )['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(
                            error_string)

                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(new_client_name)

                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(
                        error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def add_azure_cosmosdb_client(
            self,
            client_name,
            access_nodes,
            credential_name,
            azure_options):
        """
            Method to add new azure cosmos db client

            Args:

                client_name     (str)   -- new azure cosmosdb client name

                access_nodes    (str)   -- list of access node name

                credential_name (str)   -- credential name

                azure_options   (dict)  -- dictionary for Azure details:
                                            Example:
                                               azure_options = {
                                                    "subscription_id": 'subscription id',
                                                    "tenant_id": 'tenant id',
                                                    "application_id": 'application id',
                                                    "password": 'application secret',
                                                    "credential_id": credential_id
                                                }

            Returns:
                object  -   instance of the Client class for this new client

            Raises:

                SDKException:
                    if None value in azure options

                    if pseudo client with same name already exists

                    if failed to add the client

                    if response is empty

                    if response is not success

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

        memberservers = []
        for node in access_nodes:
            client_object = self._commcell_object.clients.get(node)
            client_object._get_client_properties()
            client_id = int(client_object.client_id)
            clienttype = int(client_object._client_type_id)
            access_node = {
                "client": {
                    "_type_": clienttype,
                    "clientId": client_id,
                    "clientName": client_object.client_name,
                    "groupLabel": "Access nodes",
                    "selected": True
                }
            }
            memberservers.append(access_node)

        request_json = {
            "clientInfo": {
                "clientType": 12,
                "idaInfo": {
                },
                "virtualServerClientProperties": {
                    "allowEmptyMemberServers": False,
                    "appTypes": [
                        {
                            "applicationId": 106
                        },
                        {
                            "applicationId": 134
                        }
                    ],
                    "virtualServerInstanceInfo": {
                        "associatedClients": {
                            "memberServers": memberservers
                        },
                        "azureResourceManager": {
                            "credentials": {
                                "userName": ""
                            },
                            "serverName": client_name,
                            "subscriptionId": azure_options.get("subscription_id", ""),
                            "tenantId": "",
                            "useManagedIdentity": False
                        },
                        "cloudAppInstanceInfoList": [
                        ],
                        "skipCredentialValidation": False,
                        "virtualServerCredentialinfo": {
                            "credentialId": azure_options.get("credential_id", 0),
                            "credentialName": credential_name,
                            "description": "",
                            "recordType": 4,
                            "selected": True
                        },
                        "vmwareVendor": {
                            "vcenterHostName": ""
                        },
                        "vsInstanceType": 7
                    }
                }
            },
            "entity": {
                "clientName": client_name
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GET_ALL_CLIENTS'], payload=request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json(
                        )['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(
                            error_string)

                        raise SDKException('Client', '102', o_str)
                    else:
                        # initialize the clients again
                        # so the client object has all the clients
                        self.refresh()
                        return self.get(client_name)

                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(
                        error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def get(self, name):
        """Returns a client object if client name or host name or ID or display name matches the client attribute

            We check if specified name matches any of the existing client names else
            compare specified name with host names of existing clients else if name matches with the ID

            Args:
                name (str/int)  --  name / hostname / ID of the client / display name

            Returns:
                object - instance of the Client class for the given client name

            Raises:
                SDKException:
                    if type of the client name argument is not string or Int

                    if no client exists with the given name
        """
        if isinstance(name, str):
            name = name.lower()
            client_name = None
            client_id = None
            client_from_hostname_or_displayname = None
            if self.has_client(name):
                client_from_hostname_or_displayname = self._get_client_from_hostname(name)
                if self.has_hidden_client(name) and not client_from_hostname_or_displayname \
                                                and name not in self.all_clients:
                    client_from_hostname_or_displayname = self._get_hidden_client_from_hostname(name)
                if client_from_hostname_or_displayname is None:
                    client_from_hostname_or_displayname = self._get_client_from_displayname(name)
                if name is None and client_name is None and client_from_hostname_or_displayname is None:
                    raise SDKException(
                        'Client', '102', 'No client exists with given name/hostname: {0}'.format(name)
                    )
            client_name = name if client_from_hostname_or_displayname is None else client_from_hostname_or_displayname

            if client_name in self.all_clients:
                client_id = self.all_clients[client_name]['id']
            elif client_name in self.hidden_clients:
                client_id = self.hidden_clients[client_name]['id']

            if client_id is None:
                raise SDKException('Client', '102', f'No client exists with the given name/hostname: {client_name}')

            return Client(self._commcell_object, client_name, client_id)

        elif isinstance(name, int):
            name = str(name)
            client_name = [client_name for client_name in self.all_clients
                           if name in self.all_clients[client_name].values()]

            if client_name:
                return self.get(client_name[0])
            raise SDKException('Client', '102', 'No client exists with the given ID: {0}'.format(name))

        raise SDKException('Client', '101')

    def delete(self, client_name, forceDelete= True):
        """Deletes the client from the commcell.

            Args:
                client_name (str)  --  name of the client to remove from  commcell

                forceDelete (bool) --  Force delete client if True
            Raises:
                SDKException:
                    if type of the client name argument is not string

                    if failed to delete client

                    if response is empty

                    if response is not success

                    if no client exists with the given name

        """
        if not isinstance(client_name, str):
            raise SDKException('Client', '101')
        else:
            client_name = client_name.lower()

            if self.has_client(client_name):
                if client_name in self.all_clients:
                    client_id = self.all_clients[client_name]['id']
                else:
                    client_id = self.hidden_clients[client_name]['id']
                client_delete_service = self._services['CLIENT'] % (client_id)
                if forceDelete == True:
                    client_delete_service = self._services['CLIENTFORCEDELETE'] % (client_id)

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

    def refresh(self, **kwargs):
        """
        Refresh the clients associated with the Commcell.

            Args:
                **kwargs (dict):
                    mongodb (bool)  -- Flag to fetch client groups cache from MongoDB (default: False).
                    hard (bool)     -- Flag to hard refresh MongoDB cache for this entity (default: False).
        """
        self._clients = self._get_clients()
        self._hidden_clients = self._get_hidden_clients()
        self._virtualization_clients = self._get_virtualization_clients()
        self._virtualization_access_nodes = self._get_virtualization_access_nodes()
        self._office_365_clients = None
        self._file_server_clients = None
        self._salesforce_clients = None

        mongodb = kwargs.get('mongodb', False)
        hard = kwargs.get('hard', False)
        if mongodb:
            self._client_cache = self.get_clients_cache(hard=hard)


class Client(object):
    """Class for performing client operations for a specific client."""

    def __new__(cls, commcell_object, client_name, client_id=None, username=None, password=None):
        """Decides and creates which client object needs to be created
            Args:
                commcell_object (object)     --  instance of the Commcell class

                client_name     (str)        --  name of the client

                client_id       (str)        --  id of the client
                    default: None

            Returns:
                object - instance of the Client class
                """
        from .clients.vmclient import VMClient
        from .clients.onedrive_client import OneDriveClient
        _client = commcell_object._services['CLIENT'] % (client_id)
        flag, response = commcell_object._cvpysdk_object.make_request('GET', _client)
        if flag:
            if response.json() and 'clientProperties' in response.json():
                if response.json().get('clientProperties', {})[0].get('vmStatusInfo', {}).get('vsaSubClientEntity',
                                                                                              {}).get(
                        'applicationId') == 106:
                    return object.__new__(VMClient)

                elif (len(response.json().get('clientProperties', {})[0].get('client', {}).get('idaList', [])) > 0 and
                        response.json().get('clientProperties', {})[0].get('client', {}).get('idaList', [])[0]
                        .get('idaEntity', {}).get('applicationId') == AppIDAType.CLOUD_APP.value):
                    return object.__new__(OneDriveClient)

        return object.__new__(cls)

    def __init__(self, commcell_object, client_name, client_id=None, username=None, password=None):
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

        self._username = username
        self._password = password

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
        self._block_level_cache_dir = None
        self._log_directory = None
        self._license_info = None
        self._cvd_port = None
        self._job_start_time = None
        self._timezone = None
        self._is_privacy_enabled = None
        self._is_command_center = None
        self._is_web_server = None

        self._readiness = None
        self._vm_guid = None
        self._company_name = None
        self._is_vm = None
        self._vm_hyperv_id = None
        self._client_latitude = None
        self._client_longitude = None
        self._associated_client_groups = None
        self._company_id = None
        self._is_deleted_client = None
        self._is_infrastructure = None
        self._network_status = None
        self._update_status = None
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

                self._vm_guid = self._properties.get('vmStatusInfo', {}).get('strGUID')

                client_props = self._properties['clientProps']

                self._is_data_recovery_enabled = client_props[
                    'activityControl']['EnableDataRecovery']

                self._is_data_management_enabled = client_props[
                    'activityControl']['EnableDataManagement']

                self._is_ci_enabled = client_props['activityControl']['EnableOnlineContentIndex']

                self._is_privacy_enabled = client_props.get("clientSecurity", {}).get("enableDataSecurity")

                self._is_command_center = True if list(filter(lambda x: x.get("packageId") == 1135,
                                                              client_props.get("infrastructureMachineDetails",
                                                                               []))) else False
                self._is_web_server = True if list(filter(lambda x: x.get("packageId") == 252,
                                                          client_props.get("infrastructureMachineDetails",
                                                                           []))) else False

                if 'companyName' in self._properties['client'].get('clientEntity', {}).get('entityInfo', {}):
                    self._company_name = self._properties['client']['clientEntity']['entityInfo']['companyName']

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

                if 'BlockLevelCacheDir' in client_props:
                    self._block_level_cache_dir = client_props['BlockLevelCacheDir']

                if 'clientRegionInfo' in client_props:
                    self._client_latitude = client_props.get('clientRegionInfo', {}).get('geoLocation', {}). \
                        get('latitude')
                    self._client_longitude = client_props.get('clientRegionInfo', {}).get('geoLocation', {}). \
                        get('longitude')

                if 'vmStatusInfo' in self._properties:
                    self._is_vm = True
                    self._vm_hyperv_id = self._properties.get('vmStatusInfo', {}).get('pseudoClient', {}).get(
                        'clientId')
                else:
                    self._is_vm = False

                if 'clientGroups' in self._properties:
                    self._associated_client_groups = self._properties.get('clientGroups', {})

                if 'company' in client_props:
                    self._company_id = client_props.get('company', {}).get('shortName', {}).get('id')

                if 'IsDeletedClient' in client_props:
                    self._is_deleted_client = client_props.get('IsDeletedClient')

                if 'networkReadiness' in client_props:
                    self._network_status = client_props.get('networkReadiness', {}).get('status')

                if 'isInfrastructure' in client_props:
                    self._is_infrastructure= client_props.get('isInfrastructure')

                if 'UpdateStatus' in self._properties.get('client', {}).get('versionInfo'):
                    self._update_status = self._properties.get('client', {}).get('versionInfo', {}).get('UpdateStatus')

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
            command = 'cat'
            script_arguments = str(os.path.join(self.install_directory + '/', 'galaxy_vm'))

            __, output, error = self.execute_command(command, script_arguments)

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

            windows_command = operations_dict[operation]['windows_command']
            if service_name == 'ALL' and 'grp' not in windows_command:
                windows_command = windows_command + 'grp'

            command = '"{0}" -consoleMode -{1} {2}'.format(
                '\\'.join([self.install_directory, 'Base', 'GxAdmin.exe']),
                windows_command,
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
                command = '{0} -instance {1} {2} {3}'.format(
                    commvault,
                    self.instance,
                    f"-service {service_name}" if service_name != 'ALL' else "",
                    operations_dict[operation]['unix_command'])

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
        success_alerts = [f"cluster group [{request_json['association']['entity'][0]['clientName'].lower()}] "
                          f"configuration was saved on commserve successfully."]
        success = False

        if flag:
            if response.json():
                if 'response' in response.json():
                    if response.json()['response'][0].get('errorCode', 0):
                        error_message = response.json()['response'][0].get('errorMessage')
                        if not error_message:
                            error_message = response.json()['response'][0].get('errorString', '')
                        for success_alert in success_alerts:
                            if success_alert in error_message.lower():
                                success = True
                        if not success:
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
        request_json['clientProperties']['clientProps'].pop("CVS3BucketName")
        self._process_update_request(request_json)

    @property
    def properties(self):
        """Returns the client properties"""
        return copy.deepcopy(self._properties)

    @property
    def latitude(self):
        """Returns the client latitude from clientRegionInfo GeoLocation"""
        return self._client_latitude

    @property
    def longitude(self):
        """Returns the client Longitude from clientRegionInfo GeoLocation"""
        return self._client_longitude

    @property
    def is_vm(self):
        """Returns True if the given client is a VM else False"""
        return self._is_vm

    @property
    def hyperv_id_of_vm(self):
        """Returns the Hypervisor ID associated to a VM client"""
        return self._vm_hyperv_id

    @property
    def associated_client_groups(self):
        """Returns the list of client groups to which the given client is assocaited with"""
        return self._associated_client_groups

    @property
    def company_id(self):
        """Returns the client's Company ID"""
        return self._company_id

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
        update_description = {
          "client": {
            "clientDescription": description
          }
        }
        self.update_properties(update_description)

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
    def os_type(self):
        """Treats the os type as a read-only attribute."""
        os_type = OSType.WINDOWS if OSType.WINDOWS.name.lower() in self.os_info.lower() else OSType.UNIX
        return os_type

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
    def is_privacy_enabled(self):
        """Returns if client privacy is enabled"""
        return self._is_privacy_enabled

    @property
    def is_deleted_client(self) -> bool:
        """
        Returns if the is deleted

        Returns:
            bool  --  True if deleted else false
        """
        return self._is_deleted_client

    @property
    def is_infrastructure(self) -> bool:
        """
        returns if the client is infrastructure

        Returns:
            bool  --  True if infrastructure client else false
        """
        return self._is_infrastructure

    @property
    def update_status(self) -> int:
        """
        returns the update status of the client

        Returns:
            int -- update status flag of the client
        """
        return self._update_status

    @property
    def is_command_center(self):
        """Returns if a client has command center package installed"""
        return self._is_command_center

    @property
    def is_web_server(self):
        """Returns if a client has web server package installed"""
        return self._is_web_server

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
    def block_level_cache_dir(self):
        """Returns the Block level cache directory"""
        return self._block_level_cache_dir

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

    @property
    def network_status(self) -> int:
        """
        Returns network status for the client

        Returns:
            int  --  network status flag
        """
        return self._network_status

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

    def execute_script(self, script_type, script, script_arguments=None, wait_for_completion=True, username=None, password=None):
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

                username                (str)   --  username to execute the script

                    default: None

                password                (str)   --  password of the username to execute the script

                    default: None


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
        if not (isinstance(script_type, str) and (isinstance(script, str))):
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

        if username and password:
            user_impersonation = f'<userImpersonation userName="{username}" password="{password}"/>' if username and password else ""
        elif self._username and self._password is not None:
            user_impersonation = f'<userImpersonation userName="{self._username}" password="{self._password}"/>'
        else:
            user_impersonation = ""

        xml_execute_script = """
        <App_ExecuteCommandReq arguments="{0}" scriptType="{1}" waitForProcessCompletion="{5}">
            {6}
            <client clientId="{2}" clientName="{3}"/>
            "{4}"
        </App_ExecuteCommandReq>
        """.format(
            script_arguments,
            script_types[script_type.lower()],
            self.client_id,
            self.client_name,
            script_lines,
            1 if wait_for_completion else 0,
            user_impersonation
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

    def execute_command(self, command, script_arguments=None, wait_for_completion=True, username=None, password=None):
        """Executes a command on this client.

            Args:
                command                 (str)   --  command in string to be executed on the client

                script_arguments        (str)   --  arguments to the script

                    default: None

                wait_for_completion     (bool)  --  boolean specifying whether to wait for the
                script execution to finish or not

                    default: True

                username                (str)   --  username to execute the command

                    default: None

                password                (str)   --  password of the username to execute the command

                    default: None

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
        if not isinstance(command, str):
            raise SDKException('Client', '101')


        script_arguments = '' if script_arguments is None else script_arguments
        execute_command_payload = {
            "App_ExecuteCommandReq": {
                "arguments": f"{script_arguments}",
                "command": f"{command}",
                "waitForProcessCompletion": f"{1 if wait_for_completion else 0}",
                "processinginstructioninfo": {
                    "formatFlags": {
                        "continueOnError": "1",
                        "elementBased": "1",
                        "filterUnInitializedFields": "0",
                        "formatted": "0",
                        "ignoreUnknownTags": "1",
                        "skipIdToNameConversion": "0",
                        "skipNameToIdConversion": "0"
                    }
                },
                "client": {
                    "clientId": f"{self.client_id}",
                    "clientName": f"{self.client_name}"
                }
            }
        }

        if username and password:
            execute_command_payload["App_ExecuteCommandReq"]["userImpersonation"] = {
                "userName": f"{username}",
                "password": f"{password}"
            }
        elif self._username and self._password is not None:
            execute_command_payload["App_ExecuteCommandReq"]["userImpersonation"] = {
                "userName": f"{self._username}",
                "password": f"{self._password}"
            }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], execute_command_payload
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

    @property
    def is_mongodb_ready(self):
        """
        Checks the status mongoDB

            Returns:
                True : if the MongoDB is working fine
                False : if there is any error in mongoDB

            Raises:
                SDKException:
                    if response is not success
        """
        return self.readiness_details.is_mongodb_ready()

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

                    default:    None

                    Example:    GxVssProv(Instance001)

            Returns:
                None    -   if the service was restarted successfully

            Raises:
                SDKException:
                    if failed to restart the service

        """
        return self._service_operations(service_name, 'RESTART')

    def restart_services(self, wait_for_service_restart=True, timeout=10, implicit_wait=5):
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

                implicit_wait               (int)   -- Time (in seconds) to wait before the readiness is checked.

                    default: 5


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
            time.sleep(implicit_wait)

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

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['GET_NETWORK_SUMMARY'].replace('%s', self.client_id))
        if flag:
            if "No Network Config found" in response.text or "No Network Configuration Found" in response.text:
                return ""
            return response.text
        raise SDKException('Response', '101', self._update_response_(response.text))

    def change_exchange_job_results_directory(
            self, new_directory_path, username=None, password=None):
        """
            Change the Job Result Directory of an Exchange Online Client

            Arguments:
                new_directory_path    (str)   -- The new JR directory
                    Example:
                        C:\\JR
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
        if self.client_type not in [25, 37, 15]:
            raise SDKException(
                'Client', '109',
                ' Method is application for O365 Client only')

        if new_directory_path.startswith(r'\\') and (
                username is None or password is None):
            raise SDKException(
                'Client', '101',
                'For a network share path, pass the credentials also')

        prop_dict = {
            "clientId": int(self.client_id),
            "jobResultDirectory": new_directory_path
        }
        if self.client_type == 25:
            prop_dict["appType"] = 137
        elif self.client_type == 37:
            prop_dict["appType"] = 78
        else:
            prop_dict["appType"] = 134
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

    def change_o365_client_job_results_directory(
            self, new_directory_path, username=None, password=None):
        """
                Change the Job Result Directory of a O365 Client

                Arguments:
                    new_directory_path   (str)   -- The new JR directory
                        Example:
                            C:\\JR
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
        self.change_exchange_job_results_directory(new_directory_path, username, password)

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
                if not (isinstance(key, str) and isinstance(key_len, str)):
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
                           max_cache_db=None,
                           high_latency_optimization=None,
                           variable_content_alignment=None
                           ):
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

                enableClientSideCache: To set usage of Client Side Cache
                                Values - None(Default) - DoNot Modify the property value
                                         True/False - Enable/Disable Cache respectively
                    maxCacheDB: Size of Cache DB if enabled. Default Value: None (use default size)
                                Valid values are:
                                    1024
                                    2048
                                    4096
                                    8192
                                    16384
                                    32768
                                    65536
                                    131072
                    variable_content_alignment: to increase the effectiveness of deduplication on the client computer.
                                                Variable content alignment reduces the amount of data stored during a
                                                backup operation.
                               Values - None(Default) - DoNotModify the property value
                                        True/False - Enable/Disable optimization respectively

                    high_latency_optimization: To set Optimization for High latency Networks
                                Values - None(Default) - DoNotModify the property value
                                         True/False - Enable/Disable optimization respectively
        """
        if not (isinstance(prop_name, str) and isinstance(prop_value, str)):
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
                if high_latency_optimization is not None:
                    dedupe_props['deDuplicationProperties'][
                        'enableHighLatencyOptimization'] = high_latency_optimization

                if variable_content_alignment is not None:
                    dedupe_props['deDuplicationProperties'][
                        'enableVariableContentAlignment'] = variable_content_alignment

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

    def get_configured_additional_settings(self) -> list:
        """Method to get configured additional settings name"""
        url = self._services['GET_ADDITIIONAL_SETTINGS'] % self.client_id
        flag, response = self._cvpysdk_object.make_request('GET', url)
        if flag:
            if response.json():
                response = response.json()

                if response.get('errorMsg'):
                    error_message = response.json()['errorMsg']
                    o_str = 'Failed to fetch additional settings.\nError: "{0}"'.format(error_message)
                    raise SDKException('Client', '102', o_str)

                return response.get('regKeys', [])

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

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

    @property
    def vm_guid(self):
        """Returns guid of the vm client"""

        return self._vm_guid

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

    def uninstall_software(self, force_uninstall=True,software_list=[]):
        """
        Performs readiness check on the client

            Args:
                force_uninstall (bool): Uninstalls packages forcibly. Defaults to True.
                software_list (list): The client_composition will contain the list of components need to be uninstalled.

            Usage:
                client_obj.uninstall_software(force_uninstall=False,software_list=["Index Store","File System"])

            Returns:
                The job object of the uninstall software job

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        uninstall = Uninstall(self._commcell_object)
        client_composition = []
        if software_list:
            componentInfo = self.__get_componentInfo(software_list)
            client_composition = [{"activateClient": True, "packageDeliveryOption": 0,
                                "components": {
                                    "componentInfo": componentInfo}
                                }]

        return uninstall.uninstall_software(self.client_name, force_uninstall=force_uninstall,
                                            client_composition=client_composition)

    def __get_componentInfo(self, software_list):
        """get the component info for the installed software

        Args:
            software_list (list): list of software to uninstall

        Returns:
            list: list of componetInfo for the software list.
            [
                {
                    "osType": "Windows",
                    "ComponentName": "High Availability Computing"
                }
            ]
        """
        componentInfo = []
        os_type = "Windows" if "Windows" in self._os_info else "Unix"
        for software in software_list:
            componentInfo.append(
                {
                    "osType": os_type,
                    "ComponentName": software
                }
            )
        return componentInfo

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
        Returns a dictionary with the count of AnomalousServers, AnomalousJobs, InfrastructureServers
        for all the service commcells

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
                main_keys = ['CountOfAnomalousInfrastructureServers', 'CountOfAnomalousServers',
                             'CountOfAnomalousJobs']
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

    def get_mount_volumes(self, volume_names=None):
        """"Gets mount volumes information for client
            Args:
                volume_names (list): List of volume names to be fetched (optional)
            Returns:
                volume_guids (list) : Returns list volume dictionaries
            eg: [{
                  "volumeTypeFlags": 1,
                  "freeSize": 63669854208,
                  "size": 106779639808,
                  "guid": "8459b015-4c07-4312-8440-a64cb426203c",
                  "accessPathList": ["C:"]
                }]
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._services['BROWSE_MOUNT_POINTS']
                                                           % self.client_id)
        if flag:
            if response.json() and 'mountPathInfo' in response.json():
                volumes = response.json()['mountPathInfo']
                volume_guids = []
                if volume_names:
                    for volume_name in volume_names:
                        for volume in volumes:
                            if volume_name in volume['accessPathList']:
                                volume_guids.append(volume)
                                break
                        else:
                            raise SDKException('Client', '102', f'No volume found for path {volume_name}')
                    return volume_guids
                else:
                    return volumes
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_content_indexing(self):
        """Enables the v1 content indexing on the client"""
        update_properties = self.properties
        update_properties['client']['EnableContentIndexing'] = 'true'
        self.update_properties(update_properties)

    def disable_content_indexing(self):
        """Disables the v1 content indexing on the client"""
        update_properties = self.properties
        update_properties['client']['EnableContentIndexing'] = 'false'
        self.update_properties(update_properties)

    def enable_owner_privacy(self):
        """Enables the privacy option for client"""

        if self.is_privacy_enabled:
            return

        self.set_privacy(True)

    @property
    def company_name(self):
        """Returns Company Name to which client belongs to, Returns Empty String, If client belongs to Commcell"""
        return self._company_name

    def check_eligibility_for_migration(self, destination_company_name):
        """Checks whether Client is Eligible for migration
        Args:
            destination_company_name (str)  --  Destination company name to which client is to be migrated

        Returns:
            eligibility_status (bool)   --  True, If Clients are eligible for migration else False

        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        company_id = (int(Organizations(self._commcell_object).get(
            destination_company_name).organization_id)) if destination_company_name.lower() != 'commcell' else 0
        request_json = {
            "entities": [
                {
                    "clientName": self._client_name,
                    "clientId": int(self.client_id),
                    "_type_": 3
                }
            ]
        }
        req_url = self._services['CHECK_ELIGIBILITY_MIGRATION'] % company_id
        flag, response = self._cvpysdk_object.make_request('PUT', req_url, request_json)

        if flag:
            if response.json():
                if 'error' in response.json() and response.json()['error']['errorCode'] != 0:
                    raise SDKException('Organization', '110',
                                       'Error: {0}'.format(response.json()['error']['errorMessage']))
                return True if 'applicableClients' in response.json() else False
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_owner_privacy(self):
        """Enables the privacy option for client"""
        if not self.is_privacy_enabled:
            return

        self.set_privacy(False)

    def set_privacy(self, value):
        """
        Internal function to enable/disable privacy for client

        Args:
            value(bool): True/False to enable/disable the privacy

        Raises:
            SDKException:

                if setting privacy for client fails

                if response is empty

                if response is not success
        """
        url = self._services['DISABLE_CLIENT_PRIVACY'] % self.client_id
        if value:
            url = self._services['ENABLE_CLIENT_PRIVACY'] % self.client_id

        flag, response = self._cvpysdk_object.make_request(
            'POST', url
        )

        if flag:
            if response and response.json():
                error_string = response.json().get('errorString')
                error_code = response.json().get('errorCode')
                if error_code:
                    raise SDKException('Client', '102', error_string)
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def change_dynamics365_client_job_results_directory(
            self, new_directory_path: str, username: str = str(), password: str = str()):
        """
            Change the Job Result Directory of a Dynamics 365 Client

            Arguments:
                new_directory_path   (str)   -- The new JR directory
                    Example:
                        \\vm1.example-active-directory.com\\TestFolder1\\JobResults

                username    (str)   --
                    username of the machine, if new JobResults directory is a shared/ UNC path.

                password    (str)   --
                    Password of the machine, if new JobResults directory is a shared/ UNC path.

            Raises
                SDKException   (object)
                    Error in moving the job results directory

        """
        self.change_o365_client_job_results_directory(new_directory_path, username, password)

    def change_company_for_client(self, destination_company_name):
        """
        Changes Company for Client

        Args:
            destination_company_name (str)  --  Destination company name to which client is to be migrated

        Raises:
            SDKException:
                If Client is not eligible for migration

                if response is empty

                if response is not success
        """
        if not self.check_eligibility_for_migration(destination_company_name):
            raise SDKException('Client', 102, f'Client [{self.client_name}] is Not Eligible For Migration')

        company_id = (int(Organizations(self._commcell_object).get(
            destination_company_name).organization_id)) if destination_company_name.lower() != 'commcell' else 0
        request_json = {
            "entities": [
                {
                    "clientName": self._client_name,
                    "clientId": int(self.client_id),
                    "_type_": 3
                }
            ]
        }
        req_url = self._services['MIGRATE_CLIENTS'] % company_id
        flag, response = self._cvpysdk_object.make_request('PUT', req_url, request_json)

        if flag:
            if response.json():
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    raise SDKException('Organization', '110', 'Error: {0}'.format(response.json()['errorMessage']))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def read_log_file(self, file_name: str, complete_file: bool = False) -> list:
        """
        Reads the log file from the client

        Args:
            file_name (str)     --  Name of the log file to be read
            complete_file (bool) --  True if the complete file needs to be read, False otherwise

        Returns:
            list    --  List of lines in the log file
        """
        url_params = f"?LogFileName={file_name}&completeFile={str(complete_file).lower()}"
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['CLIENT_LOGS'] % self.client_id + url_params
        )
        if flag:
            if response.json():
                return response.json().get('logs', [])
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
        self._response = None

    def __fetch_readiness_details(
            self,
            network=True,
            resource=False,
            disabled_clients=False,
            cs_cc_network_check=False,
            application_check=False,
            additional_resources=False,
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

                application_check (bool) - Performs Application Readiness check.
                                             Default: False

                additional_resources (bool) - Include Additional Resources.
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
                cs_cc_network_check,
                application_check,
                additional_resources)
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

    def is_ready(self, network=True, resource=False, disabled_clients=False, cs_cc_network_check=False,
                 application_check=False, additional_resources=False):
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

                application_check (bool) - Performs Application Readiness check.
                                             Default: False

                additional_resources (bool) - Include Additional Resources.
                                         Default: False

        Returns:

            (bool)  - True if ready else False

        """
        self.__fetch_readiness_details(network, resource, disabled_clients, cs_cc_network_check,
                                        application_check, additional_resources)
        return self._status == "Ready."

    def is_mongodb_ready(self):
        """
        mongodb_readiness (bool) - performs mongoDB check readiness by calling mongodb readiness API

        Returns:
            (bool) - True if ready else False
        """
        flag, response = self.__commcell._cvpysdk_object.make_request(
            "GET",self.__commcell._services["MONGODB_CHECK_READINESS"])
        if flag:
            self._response = response.json()
            if response.json():
                if not (self._response.get('response', [])[0].get('errorString', '') and
                        self._response.get('response', [])[0].get('errorCode', None)):
                    return True
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self.__commcell._update_response_(response.text))

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

    def get_mongodb_failure_reason(self):
        """Retrieve mongoDB readiness failure details"""
        if not self._response:
            self.is_mongodb_ready()
        return self._response
