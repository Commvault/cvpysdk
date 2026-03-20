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

    add_lustre_client()                     -- adds a new lustre client
    
    add_onedrive_client()                 --  adds a new onedrive client

    add_cassandra_client()                --  add cassandra client

    add_cockroachdb_client()              --  add cockroachdb client
    
    add_mongodb_client()              		--  add mongodb client

    add_azure_cosmosdb_client()             --  add client for azure cosmosdb cloud account

    add_mongodb_atlas_client()              --  add client for MongoDB Atlas cloud account

    get(client_name)                      --  returns the Client class object of the input client
    name

    delete(client_name)                   --  deletes the client specified by the client name from
    the commcell

    retire(client_name)                     --  retires the client specified by the client name from
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

    _set_patch_options()         --  set the patch options for the client

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

    set_windows_os_updates()     -- Sets Windows OS updates for the client

    set_microsoft_sql_server_updates()  -- Sets Microsoft SQL Server updates for the client

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

    add_http_proxy()                    --  Adds HTTP proxy for the client

    remove_http_proxy()                 --  Removes HTTP proxy for the client

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

import copy
import datetime
import os
import re
import time
from base64 import b64encode
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import requests

if TYPE_CHECKING:
    from .commcell import Commcell

from .additional_settings import AdditionalSettings
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

from .security.security_association import SecurityAssociation

class Clients(object):
    """
    Manages and represents all clients associated with a CommCell environment.

    The Clients class provides a comprehensive interface for interacting with various types of clients
    within a CommCell, including management, retrieval, addition, deletion, and property access. It supports
    a wide range of client types such as Azure AD, Office 365, Dynamics 365, Salesforce, virtualization platforms,
    file servers, laptops, cloud services, and specialized database clients.

    This class enables users to:
        - Retrieve and enumerate clients using indexing, length, and string representations
        - Add new clients for multiple platforms and services (e.g., Azure, AWS, Google, Salesforce, VMware, Hyper-V, NAS, Splunk, Yugabyte, Couchbase, Exchange, Cassandra, CockroachDB, CosmosDB, Nutanix, SharePoint, Teams, OneDrive, AliCloud)
        - Access categorized client lists via properties (e.g., office_365_clients, dynamics365_clients, salesforce_clients, virtualization_clients, file_server_clients, laptop_clients, hidden_clients, virtual_machines)
        - Manage client cache and refresh client information
        - Check for existence of clients and hidden clients
        - Create pseudo clients and register decoupled clients
        - Delete or retire clients from the CommCell
        - Retrieve clients by name, hostname, or display name
        - Access and process client details and parameters for advanced operations

    Key Features:
        - Comprehensive client management for CommCell environments
        - Support for adding clients across cloud, virtualization, and database platforms
        - Categorized access to specialized client types
        - Client existence checks and retrieval by various identifiers
        - Client cache management and refresh capabilities
        - Pseudo client creation and decoupled client registration
        - Deletion and retirement of clients
        - Advanced internal methods for processing and organizing client data

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a Clients object with the provided Commcell instance.

        Args:
            commcell_object: Instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> clients = Clients(commcell)
            >>> # The Clients object is now ready to manage and query client entities

        #ai-gen-doc
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
        self._LAPTOP_CLIENTS = self._services['GET_LAPTOP_CLIENTS']
        self._VIRTUAL_MACHINES = self._services['GET_VIRTUAL_MACHINES']
        self._ADD_EXCHANGE_CLIENT = self._ADD_SHAREPOINT_CLIENT = self._ADD_SALESFORCE_CLIENT = \
            self._ADD_GOOGLE_CLIENT = self._ADD_OKTA_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_SPLUNK_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_COCKROACHDB_CLIENT = self._services['COCKROACHDB']
        self._ADD_CASSANDRA_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_YUGABYTE_CLIENT = self._services['CREATE_YUGABYTE_CLIENT']
        self._ADD_COUCHBASE_CLIENT = self._services['CREATE_COUCHBASE_CLIENT']
        self._ADD_NUTANIX_CLIENT = self._services['CREATE_NUTANIX_CLIENT']
        self._ADD_NAS_CLIENT = self._services['CREATE_NAS_CLIENT']
        self._ADD_ONEDRIVE_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_MONGODB_CLIENT = self._services['CREATE_PSEUDO_CLIENT']
        self._ADD_LUSTRE_CLIENT = self._services['CREATE_LUSTRE_CLIENT']
        self._clients = None
        self._hidden_clients = None
        self._virtualization_clients = None
        self._virtualization_access_nodes = None
        self._office_365_clients = None
        self._dynamics365_clients = None
        self._salesforce_clients = None
        self._file_server_clients = None
        self._laptop_clients = None
        self._virtual_machines = None
        self._client_cache = None
        self._all_clients_props = None
        self._infra_clients = None
        self.filter_query_count = 0
        self.refresh()

    def __str__(self) -> str:
        """Return a formatted string representation of all clients associated with the Commcell.

        The output lists each client with its serial number in a tabular format.

        Returns:
            A string containing the serial number and name of each client.

        Example:
            >>> clients = Clients(commcell_object)
            >>> print(str(clients))
            S. No.    	Client

            1        	ClientA
            2        	ClientB
            3        	ClientC
            # The output displays all clients in a formatted table

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Client')

        for index, client in enumerate(self.all_clients):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, client)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return a string representation of the Clients class instance.

        This method provides a human-readable description of the Clients object,
        typically used for debugging and logging purposes.

        Returns:
            A string indicating that this is a Clients class instance for Commcell.

        Example:
            >>> clients = Clients(commcell_object)
            >>> print(repr(clients))
            Clients class instance for Commcell

        #ai-gen-doc
        """
        return "Clients class instance for Commcell"

    def __len__(self) -> int:
        """Get the number of clients associated with the Commcell.

        Returns:
            The total count of clients as an integer.

        Example:
            >>> clients = Clients(commcell_object)
            >>> num_clients = len(clients)
            >>> print(f"Total clients: {num_clients}")
        #ai-gen-doc
        """
        return len(self.all_clients)

    def __getitem__(self, value: Union[str, int]) -> Union[str, Dict[str, Any]]:
        """Retrieve client information by name or ID.

        If a client name is provided, returns the details dictionary for that client.
        If a client ID is provided, returns the name of the corresponding client.

        Args:
            value: The name (str) or ID (int or str) of the client to retrieve.

        Returns:
            If a client name is provided, returns a dictionary containing client details.
            If a client ID is provided, returns the name of the client as a string.

        Raises:
            IndexError: If no client exists with the given name or ID.

        Example:
            >>> clients = Clients(...)
            >>> # Get client details by name
            >>> details = clients['ClientA']
            >>> print(details)
            >>> # Get client name by ID
            >>> name = clients[12345]
            >>> print(f"Client name: {name}")

        #ai-gen-doc
        """
        value = str(value).lower()

        if value in self.all_clients:
            return self.all_clients[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_clients.items()))[0][0]
            except IndexError:
                raise IndexError('No client exists with the given Name / Id')

    def add_azure_ad_client(self, client_name: str, plan_name: str, application_Id: str, application_Secret: str, azure_directory_Id: str):
        """Add a new Azure Active Directory (AD) client to the Commcell.

        This method registers a new Azure AD client using the provided application credentials and associates it with the specified server plan.

        Args:
            client_name: Name to assign to the new Azure AD client.
            plan_name: Name of the server plan to associate with the client.
            application_Id: Application ID of the Azure AD app.
            application_Secret: Application secret of the Azure AD app.
            azure_directory_Id: Directory ID of the Azure AD app.

        Raises:
            SDKException: If the plan name is invalid, the response is empty, or the request is unsuccessful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> clients.add_azure_ad_client(
            ...     client_name="FinanceADClient",
            ...     plan_name="AzureServerPlan",
            ...     application_Id="12345678-90ab-cdef-1234-567890abcdef",
            ...     application_Secret="superSecretValue",
            ...     azure_directory_Id="abcdef12-3456-7890-abcd-ef1234567890"
            ... )
            >>> print("Azure AD client added successfully.")

        #ai-gen-doc
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

    def _get_clients(self, full_response: bool = False) -> Dict[str, Dict[str, str]]:
        """Retrieve all clients associated with the Commcell.

        Args:
            full_response: If True, returns the complete response from the Commcell API.
                If False, returns a simplified dictionary of client details.

        Returns:
            Dictionary containing client information, where each key is the client name and
            the value is a dictionary with 'id', 'hostname', and 'displayName' for that client.
            If no clients are available, returns an empty dictionary.

        Raises:
            SDKException: If the response from the Commcell API is empty or unsuccessful.

        Example:
            >>> clients_obj = Clients(commcell_object)
            >>> clients = clients_obj._get_clients()
            >>> print(clients)
            >>> # Output:
            >>> # {
            >>> #     "client1_name": {
            >>> #         "id": "client1_id",
            >>> #         "hostname": "client1_hostname",
            >>> #         "displayName": "client1_displayname"
            >>> #     },
            >>> #     "client2_name": {
            >>> #         "id": "client2_id",
            >>> #         "hostname": "client2_hostname",
            >>> #         "displayName": "client2_displayname"
            >>> #     }
            >>> # }
            >>> # To get the full API response:
            >>> full_response = clients_obj._get_clients(full_response=True)
            >>> print(full_response)
        #ai-gen-doc
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

    def _get_office_365_clients(self) -> Dict[str, Dict[str, str]]:
        """Retrieve all Office 365 clients in the Commcell via REST API.

        This method makes a REST API call to fetch all Office 365 clients configured in the Commcell.
        The returned dictionary maps each client name (in lowercase) to its corresponding client ID.

        Returns:
            Dictionary where keys are Office 365 client names (str) and values are dictionaries containing the client ID.
            Example:
                {
                    "client1_name": {"id": "client1_id"},
                    "client2_name": {"id": "client2_id"}
                }

        Raises:
            SDKException: If the response is empty or unsuccessful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> o365_clients = clients._get_office_365_clients()
            >>> print(o365_clients)
            >>> # Output: {'client1_name': {'id': 'client1_id'}, ...}

        #ai-gen-doc
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
    def office_365_clients(self) -> Dict[str, Any]:
        """Get a dictionary of all Office 365 clients in the Commcell.

        Returns:
            Dictionary mapping client names to their respective details.

        Example:
            >>> clients = Clients(commcell_object)
            >>> o365_clients = clients.office_365_clients  # Use dot notation for property access
            >>> print(f"Total Office 365 clients: {len(o365_clients)}")
            >>> # Access details for a specific client
            >>> if 'ClientA' in o365_clients:
            >>>     print(f"ClientA details: {o365_clients['ClientA']}")

        #ai-gen-doc
        """
        if self._office_365_clients is None:
            self._office_365_clients = self._get_office_365_clients()
        return self._office_365_clients

    def _get_dynamics_365_clients(self) -> Dict[str, Dict[str, str]]:
        """Retrieve all Dynamics 365 clients in the Commcell via REST API.

        This method makes a REST API call to fetch all Dynamics 365 clients configured in the Commcell.
        The returned dictionary maps each client name to its corresponding client ID.

        Returns:
            Dictionary where keys are Dynamics 365 client names (as lowercase strings), and values are
            dictionaries containing the client ID under the 'id' key.

            Example format:
                {
                    "client1_name": {"id": "client1_id"},
                    "client2_name": {"id": "client2_id"}
                }

        Raises:
            SDKException: If the API response is empty or indicates a failure.

        Example:
            >>> clients = Clients(commcell_object)
            >>> dynamics_clients = clients._get_dynamics_365_clients()
            >>> print(dynamics_clients)
            >>> # Output: {'client1_name': {'id': 'client1_id'}, 'client2_name': {'id': 'client2_id'}}

        #ai-gen-doc
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
    def dynamics365_clients(self) -> Dict[str, Any]:
        """Get a dictionary of all Dynamics 365 clients in the Commcell.

        Returns:
            Dictionary mapping client names to their respective details for Dynamics 365 clients.

        Example:
            >>> clients = Clients(commcell_object)
            >>> d365_clients = clients.dynamics365_clients  # Use dot notation for property access
            >>> print(f"Total Dynamics 365 clients: {len(d365_clients)}")
            >>> # Access details for a specific client
            >>> if 'ClientA' in d365_clients:
            >>>     print(f"ClientA details: {d365_clients['ClientA']}")
        #ai-gen-doc
        """
        if self._dynamics365_clients is None:
            self._dynamics365_clients = self._get_dynamics_365_clients()
        return self._dynamics365_clients

    def _get_salesforce_clients(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all Salesforce clients in the Commcell via REST API.

        This method makes a REST API call to fetch all Salesforce clients configured in the Commcell.
        The returned dictionary maps each client's display name to its corresponding ID and client name.

        Returns:
            Dictionary where each key is a Salesforce client's display name, and the value is another
            dictionary containing the client's ID and name. Example format:

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

        Raises:
            SDKException: If the REST API call fails or returns an error response.

        Example:
            >>> clients = Clients(commcell_object)
            >>> salesforce_clients = clients._get_salesforce_clients()
            >>> for display_name, details in salesforce_clients.items():
            ...     print(f"Salesforce Client: {display_name}, ID: {details['id']}, Name: {details['clientName']}")
        #ai-gen-doc
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
    def salesforce_clients(self) -> Dict[str, Any]:
        """Get a dictionary of all Salesforce clients configured in the Commcell.

        Returns:
            Dictionary mapping Salesforce client names to their details.

        Example:
            >>> clients = Clients(commcell_object)
            >>> sf_clients = clients.salesforce_clients  # Use dot notation for property access
            >>> print(f"Total Salesforce clients: {len(sf_clients)}")
            >>> # Access details of a specific client
            >>> if 'SalesforceClient01' in sf_clients:
            >>>     details = sf_clients['SalesforceClient01']
            >>>     print(f"Details for SalesforceClient01: {details}")

        #ai-gen-doc
        """
        if self._salesforce_clients is None:
            self._salesforce_clients = self._get_salesforce_clients()
        return self._salesforce_clients

    def _get_hidden_clients(self) -> Dict[str, Dict[str, str]]:
        """Retrieve all hidden clients associated with the Commcell, including VMs and clients not visible in the main client list.

        This method returns a dictionary of hidden clients, where each key is the client name and the value is a dictionary containing the client's ID, hostname, and display name. Hidden clients are those present in the Commcell but not listed in the main client collection.

        Returns:
            Dictionary mapping hidden client names to their details:
                {
                    "client1_name": {
                        "id": "client1_id",
                        "hostname": "client1_hostname",
                        "displayName": "client1_displayname"
                    },
                    "client2_name": {
                        "id": "client2_id",
                        "hostname": "client2_hostname",
                        "displayName": "client2_displayname"
                    }
                }

        Raises:
            SDKException: If the response from the Commcell is empty or unsuccessful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> hidden_clients = clients._get_hidden_clients()
            >>> print(f"Found {len(hidden_clients)} hidden clients")
            >>> for name, details in hidden_clients.items():
            ...     print(f"Client: {name}, ID: {details['id']}, Hostname: {details['hostname']}")
        #ai-gen-doc
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

    def _get_virtualization_clients(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all virtualization clients in the Commcell via REST API.

        This method makes a REST API call to fetch all virtualization clients configured in the Commcell.
        The returned dictionary maps each client name (in lowercase) to its details, including client ID,
        client name, and host name.

        Returns:
            Dictionary where each key is a virtualization client name (str), and the value is a dictionary
            containing 'clientId', 'clientName', and 'hostName' for that client.

        Raises:
            SDKException: If the API response is empty or indicates a failure.

        Example:
            >>> clients = Clients(commcell_object)
            >>> virtualization_clients = clients._get_virtualization_clients()
            >>> for name, details in virtualization_clients.items():
            ...     print(f"Client: {name}, ID: {details['clientId']}, Host: {details['hostName']}")
        #ai-gen-doc
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

    def _get_virtualization_access_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all virtualization access nodes in the Commcell via REST API.

        This method performs a REST API call to obtain details of all virtualization access nodes
        configured in the Commcell. The returned dictionary maps each access node's display name
        to its corresponding details, including client ID, client name, and host name.

        Returns:
            Dictionary where each key is the display name of an access node, and the value is
            another dictionary containing:
                - 'id': The client ID of the access node.
                - 'name': The client name of the access node.
                - 'hostName': The host name of the access node.

        Raises:
            SDKException: If the API response is empty or unsuccessful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> access_nodes = clients._get_virtualization_access_nodes()
            >>> for display_name, node_info in access_nodes.items():
            ...     print(f"Access Node: {display_name}")
            ...     print(f"  ID: {node_info['id']}")
            ...     print(f"  Name: {node_info['name']}")
            ...     print(f"  Hostname: {node_info['hostName']}")

        #ai-gen-doc
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

    def _get_fileserver_clients(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all file server clients in the Commcell via REST API.

        This method makes a REST API call to fetch all file server clients configured in the Commcell.
        The returned dictionary maps each client name to its details, including client ID and display name.

        Returns:
            Dictionary where each key is a file server client name, and the value is a dictionary with:
                - 'id': The unique identifier of the client.
                - 'displayName': The display name of the client.

        Raises:
            SDKException: If the API response is empty or indicates a failure.

        Example:
            >>> clients = Clients(commcell_object)
            >>> fs_clients = clients._get_fileserver_clients()
            >>> for name, details in fs_clients.items():
            ...     print(f"Client: {name}, ID: {details['id']}, Display Name: {details['displayName']}")
        #ai-gen-doc
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

    def _get_laptop_clients(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all laptop clients in the Commcell via REST API.

        This method makes a REST API call to fetch all laptop clients registered in the Commcell.
        The returned dictionary maps each client name to its details, including client ID and display name.

        Returns:
            Dictionary where each key is a laptop client name and the value is a dictionary containing:
                - 'id': The unique identifier of the client.
                - 'displayName': The display name of the client.

        Raises:
            SDKException: If the API response is empty or unsuccessful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> laptop_clients = clients._get_laptop_clients()
            >>> for name, info in laptop_clients.items():
            ...     print(f"Client: {name}, ID: {info['id']}, Display Name: {info['displayName']}")
        #ai-gen-doc
        """
        request_url = f'{self._LAPTOP_CLIENTS}?fl=clientsFileSystem'
        flag, response = self._cvpysdk_object.make_request('GET', request_url)

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        if not response:
            raise SDKException('Response','102')

        devices = {}
        if 'clientsFileSystem' in response.json():
            for device in response.json()['clientsFileSystem']:
                client_info = device.get('client', {})
                client_name = client_info.get('clientName')
                plan = device.get('plan', {})
                plan_name = plan.get('planName', None)
                is_cloud_laptop = device.get('isCloudLaptop', False)
                if not client_name:
                    continue  # Skip clients without a name

                devices[client_name] = {
                    'id': client_info.get('clientId'),
                    'displayName': client_name,
                    'planName': plan_name,
                    'isCloudLaptop': is_cloud_laptop
                }
        return devices

    def _get_virtual_machines(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all virtual machine clients in the Commcell via REST API.

        This method makes a REST API call to fetch details of all virtual machine clients
        managed by the Commcell. The returned dictionary maps each VM's unique name to
        its details, including hypervisor, vendor, and display name. Duplicate VM names
        are handled by appending a numeric suffix.

        Returns:
            Dictionary where each key is a VM name and the value is a dictionary with VM details:
                {
                    "vm1_name": {
                        "hypervisor": str,
                        "vendor": str,
                        "displayName": str
                    },
                    "vm2_name": {
                        "hypervisor": str,
                        "vendor": str,
                        "displayName": str
                    }
                }

        Raises:
            SDKException: If the REST API response is empty or unsuccessful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> vm_clients = clients._get_virtual_machines()
            >>> for vm_name, vm_info in vm_clients.items():
            ...     print(f"VM: {vm_name}, Hypervisor: {vm_info['hypervisor']}, Vendor: {vm_info['vendor']}")
        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._VIRTUAL_MACHINES)

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        if not response:
            raise SDKException('Response','102')

        vms = {}
        if 'virtualMachines' in response.json():
            name_count = {} # to handle duplicate names

            for vm in response.json().get('virtualMachines', []):
                original_name = vm.get('name')

                if not original_name:
                    continue  # Skip VMs without a name
                # Check and update name for duplicates
                if original_name in name_count:
                    name_count[original_name] += 1
                    unique_name = f"{original_name}_{name_count[original_name]}"
                else:
                    name_count[original_name] = 0
                    unique_name = original_name

                vms[unique_name] = {
                    'hypervisor': vm.get('hypervisor', {}).get('name'),
                    'vendor': vm.get('vendor'),
                    'displayName': vm.get('displayName')
                }
        return vms

    @staticmethod
    def _get_client_dict(client_object: 'Client') -> Dict[str, Any]:
        """Generate a dictionary representation for a Client object to associate with a Virtual Client.

        Args:
            client_object: Instance of the Client class whose details are to be included.

        Returns:
            Dictionary containing client information formatted for Virtual Client association.

        Example:
            >>> client = Client(...)
            >>> client_dict = Clients._get_client_dict(client)
            >>> print(client_dict)
            {'client': {'clientName': client.client_name, 'clientId': int(client.client_id), '_type_': 3}}

        #ai-gen-doc
        """
        client_dict = {
            "client": {
                "clientName": client_object.client_name,
                "clientId": int(client_object.client_id),
                "_type_": 3
            }
        }

        return client_dict

    def _member_servers(self, clients_list: List[Union[str, 'Client']]) -> List[Dict[str, Any]]:
        """Get the member servers to be associated with the Virtual Client.

        Args:
            clients_list: List of client names (as strings) or Client objects to associate with the virtual client.

        Returns:
            List of dictionaries, each representing a member server eligible for association with the Virtual Client.

        Raises:
            SDKException: If the clients_list argument is not a list.

        Example:
            >>> clients = Clients(commcell_object)
            >>> member_servers = clients._member_servers(['client1', 'client2'])
            >>> print(f"Eligible member servers: {member_servers}")
            >>> # You can also pass Client objects in the list
            >>> client_obj = clients.get('client3')
            >>> member_servers = clients._member_servers(['client1', client_obj])
            >>> print(f"Member servers: {member_servers}")

        #ai-gen-doc
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

    def _get_client_from_hostname(self, hostname: str) -> Optional[str]:
        """Check if a client is associated with the specified hostname.

        Args:
            hostname: Host name of the client to search for in the Commcell.

        Returns:
            The name of the client associated with the given hostname if found, otherwise None.

        Example:
            >>> clients = Clients(commcell_object)
            >>> client_name = clients._get_client_from_hostname('server01.domain.com')
            >>> if client_name:
            >>>     print(f"Client found: {client_name}")
            >>> else:
            >>>     print("No client associated with the given hostname.")

        #ai-gen-doc
        """
        # verify there is no client in the Commcell with the same name as the given hostname
        # for multi-instance clients
        if self.all_clients and hostname not in self.all_clients:
            for client in self.all_clients:
                if hostname.lower() == self.all_clients[client]['hostname']:
                    return client

    def _get_hidden_client_from_hostname(self, hostname: str) -> Optional[str]:
        """Check if a hidden client associated with the given hostname exists and return its name.

        This method searches for a hidden client whose hostname matches the provided value.
        If a match is found, the hidden client's name is returned; otherwise, None is returned.

        Args:
            hostname: Host name of the client to search for in hidden clients.

        Returns:
            The name of the hidden client associated with the given hostname, or None if no match is found.

        Example:
            >>> clients = Clients(commcell_object)
            >>> hidden_client_name = clients._get_hidden_client_from_hostname('server01.domain.com')
            >>> if hidden_client_name:
            ...     print(f"Hidden client found: {hidden_client_name}")
            ... else:
            ...     print("No hidden client found for the given hostname.")

        #ai-gen-doc
        """
        # verify there is no client in the Commcell with the same name as the given hostname
        # for multi-instance clients
        if self.hidden_clients and hostname not in self.hidden_clients:
            for hidden_client in self.hidden_clients:
                if hostname.lower() == self.hidden_clients[hidden_client]['hostname']:
                    return hidden_client

    def _get_client_from_displayname(self, display_name: str) -> Optional[str]:
        """Retrieve the client name associated with the given display name.

        Args:
            display_name: The display name of the client on this Commcell.

        Returns:
            The name of the client associated with the specified display name as a string.
            Returns None if no client exists with the given display name.

        Raises:
            Exception: If multiple clients have the same display name.

        Example:
            >>> clients = Clients(commcell_object)
            >>> client_name = clients._get_client_from_displayname("WebServer01")
            >>> if client_name:
            ...     print(f"Client name found: {client_name}")
            ... else:
            ...     print("No client found with the specified display name")
        #ai-gen-doc
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

    def _get_fl_parameters(self, fl: Optional[List[str]] = None) -> str:
        """Generate the 'fl' parameter string for MongoDB caching API calls.

        This method constructs the 'fl' query parameter used to specify which client columns
        should be included in the API response. If no columns are provided, a default set is used.

        Args:
            fl: Optional list of column names to include in the API request. Each column name
                must be one of the valid columns supported by the API.

        Returns:
            A string representing the 'fl' parameter to be appended to the API request URL.

        Raises:
            SDKException: If any column name in the provided list is invalid.

        Example:
            >>> clients = Clients()
            >>> fl_param = clients._get_fl_parameters(['clientName', 'hostName'])
            >>> print(fl_param)
            &fl=clientProperties.client.clientEntity.clientName,clientProperties.client.clientEntity.clientName,clientProperties.client.clientEntity.hostName

            >>> # Using default columns
            >>> fl_param = clients._get_fl_parameters()
            >>> print(fl_param)
            &fl=clientProperties.client%2CclientProperties.clientProps%2Coverview

        #ai-gen-doc
        """
        self.valid_columns = {'clientName': 'clientProperties.client.clientEntity.clientName',
                              'clientId': 'clientProperties.client.clientEntity.clientId',
                              'hostName': 'clientProperties.client.clientEntity.hostName',
                              'displayName': 'clientProperties.client.clientEntity.displayName',
                              'clientGUID': 'clientProperties.client.clientEntity.clientGUID',
                              'companyName': 'clientProperties.client.clientEntity.entityInfo.companyName',
                              'idaList': 'client.idaList.idaEntity.appName',
                              'clientRoles': 'clientProperties.clientProps.clientRoles.name',
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

    def _get_sort_parameters(self, sort: Optional[List[str]] = None) -> str:
        """Generate the sort parameter string for MongoDB caching API calls.

        Args:
            sort: A list containing the column name and sort type.
                - The first element is the column name to sort by.
                - The second element is the sort type: '1' for ascending, '-1' for descending.
                Example: ['ColumnName', '1']

        Returns:
            A string representing the sort parameter to be used in the API call.

        Raises:
            SDKException: If an invalid column name or sort type is provided.

        Example:
            >>> clients = Clients(...)
            >>> sort_param = clients._get_sort_parameters(['ClientName', '1'])
            >>> print(sort_param)
            &sort=clientName:1

        #ai-gen-doc
        """
        sort_type = str(sort[1])
        col = sort[0]
        if col in self.valid_columns.keys() and sort_type in ['1', '-1']:
            sort_parameter = '&sort=' + self.valid_columns[col] + ':' + sort_type
        else:
            raise SDKException('Client', '102', 'Invalid column name passed')
        return sort_parameter

    def _get_fq_parameters(self, fq: Optional[List[List[Any]]] = None) -> str:
        """Generate the filter query (fq) parameter string based on the provided filter criteria.

        Args:
            fq: Optional list of filter criteria, where each item is a list containing
                [columnName, condition, value]. For example:
                [['displayName', 'contains', 'test'], ['clientRoles', 'contains', 'Command Center']]
                - columnName: Name of the client property to filter (e.g., 'displayName', 'clientRoles').
                - condition: Filter condition ('contains', 'notContains', 'eq', 'neq', 'isEmpty').
                - value: Value to match for the filter (may be omitted for 'isEmpty').

        Returns:
            A string representing the constructed fq parameter for use in API queries.

        Raises:
            SDKException: If an invalid column name or condition is provided.

        Example:
            >>> fq_filters = [
            ...     ['displayName', 'contains', 'test'],
            ...     ['clientRoles', 'contains', 'Command Center'],
            ...     ['networkStatus', 'eq', 'Online'],
            ...     ['isDeletedClient', 'eq', True]
            ... ]
            >>> fq_param_str = clients._get_fq_parameters(fq_filters)
            >>> print(fq_param_str)
            # Output: &fq=clientProperties.isServerClient:eq:true&fq=displayName:contains:test&fq=clientRoles:contains:Command Center&fq=networkStatus:eq:ONLINE&fq=isDeletedClient:eq:true

        #ai-gen-doc
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

    def get_clients_cache(self, hard: bool = False, **kwargs: Any) -> Dict[str, Dict[str, Any]]:
        """Retrieve all clients present in the CommcellEntityCache database.

        This method fetches client details from the CommcellEntityCache DB, with options to filter, sort, limit,
        and search the results. It supports both soft and hard refreshes of the client cache.

        Args:
            hard: If True, performs a hard refresh on the clients cache.
            **kwargs: Optional parameters to customize the response:
                fl (list): List of columns to include in the response (default: None).
                sort (list): List specifying the column to sort by and sort order (1 for ascending, -1 for descending).
                    Example: ['connectName', 1]
                limit (list): List containing start and limit values for pagination. Example: ['0', '100']
                search (str): String to search within supported columns.
                fq (list): List of filter queries, each as [columnName, condition, value].
                    Example: [['displayName', 'contains', 'test']]
                enum (bool): If True, returns enums in the response (default: True).

        Returns:
            Dictionary mapping client names to their respective property dictionaries.

        Example:
            >>> clients = Clients(commcell_object)
            >>> cache = clients.get_clients_cache(hard=True, fl=['clientName', 'hostName'], limit=['0', '50'], search='Server')
            >>> print(f"Found {len(cache)} clients in cache")
            >>> for name, props in cache.items():
            >>>     print(f"Client: {name}, Host: {props.get('hostName')}")
        #ai-gen-doc
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
    def all_clients(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary containing all clients and their associated information.

        Returns:
            Dictionary mapping client names to their details, including ID, hostname, and display name.
            Example structure:
                {
                    "client1_name": {
                        "id": client1_id,
                        "hostname": client1_hostname,
                        "displayName": client1_display_name
                    },
                    "client2_name": {
                        "id": client2_id,
                        "hostname": client2_hostname,
                        "displayName": client2_display_name
                    },
                    ...
                }

        Example:
            >>> clients = Clients(commcell_object)
            >>> all_clients_info = clients.all_clients  # Use dot notation for property
            >>> print(f"Total clients: {len(all_clients_info)}")
            >>> # Access details for a specific client
            >>> if "client1_name" in all_clients_info:
            >>>     client_details = all_clients_info["client1_name"]
            >>>     print(f"Client ID: {client_details['id']}")
            >>>     print(f"Hostname: {client_details['hostname']}")
            >>>     print(f"Display Name: {client_details['displayName']}")

        #ai-gen-doc
        """
        return self._clients

    @property
    def all_clients_cache(self) -> Dict[str, Dict[str, Any]]:
        """Get a cached dictionary of all clients and their details from the CommcellEntityCache database.

        This property returns a dictionary where each key is a client name, and the value is another dictionary
        containing detailed information about that client, such as ID, hostname, display name, GUID, company,
        version, OS info, IDA list, tags, deletion status, infrastructure flag, network status, region, and roles.

        Returns:
            Dictionary mapping client names to their respective information dictionaries.

        Example:
            >>> clients = Clients(commcell_object)
            >>> client_cache = clients.all_clients_cache  # Use dot notation for property access
            >>> print(f"Total clients cached: {len(client_cache)}")
            >>> # Access details for a specific client
            >>> if "client1_name" in client_cache:
            >>>     details = client_cache["client1_name"]
            >>>     print(f"Client ID: {details['id']}, Hostname: {details['hostname']}")
        #ai-gen-doc
        """
        if not self._client_cache:
            self._client_cache = self.get_clients_cache()
        return self._client_cache

    @property
    def all_clients_prop(self) -> List[Dict[str, Any]]:
        """Get the complete GET API response containing all client properties.

        Returns:
            List of dictionaries, each representing the properties of a client as returned by the API.

        Example:
            >>> clients = Clients(commcell_object)
            >>> all_props = clients.all_clients_prop  # Use dot notation for property access
            >>> print(f"Total clients found: {len(all_props)}")
            >>> # Access properties of the first client
            >>> if all_props:
            >>>     first_client = all_props[0]
            >>>     print(f"First client properties: {first_client}")

        #ai-gen-doc
        """
        self._all_clients_props = self._get_clients(full_response=True).get('clientProperties',[])
        return self._all_clients_props

    def create_pseudo_client(self, client_name: str, client_hostname: Optional[str] = None, client_type: str = "windows") -> 'Client':
        """Create a pseudo client with the specified name, hostname, and type.

        This method creates a pseudo client in the Commcell environment. The client type can be one of:
        "windows", "unix", "unix cluster", or "sap hana". If no hostname is provided, the client name is used as the hostname.

        Args:
            client_name: Name of the client to be created.
            client_hostname: Optional hostname for the client. If not provided, defaults to client_name.
            client_type: OS/type of the client to be created. Available values are:
                - "windows"
                - "unix"
                - "unix cluster"
                - "sap hana"
                Default is "windows".

        Returns:
            Client object representing the newly created pseudo client.

        Raises:
            SDKException: If the client name type is incorrect, if the response is empty,
                or if the client creation fails due to an error in the response.

        Example:
            >>> clients = Clients(commcell_object)
            >>> pseudo_client = clients.create_pseudo_client(
            ...     client_name="TestPseudoClient",
            ...     client_hostname="test-host",
            ...     client_type="unix"
            ... )
            >>> print(f"Pseudo client created: {pseudo_client}")

        #ai-gen-doc
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

    def register_decoupled_client(self, client_name: str, client_host_name: str, port_number: int = 8400):
        """Register a decoupled client with the specified host name and port.

        Args:
            client_name: Name of the client to register.
            client_host_name: Host name of the decoupled client.
            port_number: Port number used by the decoupled client (default is 8400).

        Returns:
            The client object for the registered client.

        Raises:
            SDKException: If the client name type is incorrect, the response is empty, or the client ID cannot be retrieved from the response.

        Example:
            >>> clients = Clients(commcell_object)
            >>> client_obj = clients.register_decoupled_client(
            ...     client_name="WebServer01",
            ...     client_host_name="webserver01.domain.com",
            ...     port_number=8500
            ... )
            >>> print(f"Registered client: {client_obj}")
            >>> # The returned client object can be used for further client operations

        #ai-gen-doc
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
    def hidden_clients(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of hidden clients and their associated information.

        Returns:
            Dictionary mapping hidden client names to their details, including client ID and hostname.
            Example structure:
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

        Example:
            >>> clients = Clients(commcell_object)
            >>> hidden = clients.hidden_clients  # Use dot notation for property access
            >>> print(f"Number of hidden clients: {len(hidden)}")
            >>> for name, info in hidden.items():
            ...     print(f"Client: {name}, ID: {info['id']}, Hostname: {info['hostname']}")

        #ai-gen-doc
        """
        return self._hidden_clients

    @property
    def virtualization_clients(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of virtualization clients and their details.

        Returns:
            Dictionary mapping virtualization client names to their information, including client ID and hostname.
            Example structure:
                {
                    "client1_name": {
                        "id": client1_id,
                        "hostname": client1_hostname
                    },
                    "client2_name": {
                        "id": client2_id,
                        "hostname": client2_hostname
                    },
                    ...
                }

        Example:
            >>> clients = Clients(commcell_object)
            >>> v_clients = clients.virtualization_clients  # Use dot notation for property access
            >>> print(f"Total virtualization clients: {len(v_clients)}")
            >>> for name, info in v_clients.items():
            ...     print(f"Client: {name}, ID: {info['id']}, Hostname: {info['hostname']}")

        #ai-gen-doc
        """
        return self._virtualization_clients

    @property
    def virtualization_access_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Get the dictionary of virtualization access nodes available in the Commcell.

        Each key in the dictionary is the display name of an access node, and its value is a dictionary
        containing the node's ID, name, and hostname.

        Returns:
            Dictionary mapping display names to access node details. Each value contains:
                - id: Unique identifier of the access node.
                - name: Name of the access node.
                - hostname: Hostname of the access node.

        Example:
            >>> clients = Clients(commcell_object)
            >>> access_nodes = clients.virtualization_access_nodes  # Use dot notation for property
            >>> for display_name, node_info in access_nodes.items():
            ...     print(f"Access Node: {display_name}")
            ...     print(f"  ID: {node_info['id']}")
            ...     print(f"  Name: {node_info['name']}")
            ...     print(f"  Hostname: {node_info['hostname']}")

        #ai-gen-doc
        """
        return self._virtualization_access_nodes

    @property
    def file_server_clients(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all file server clients and their details in the Commcell.

        Returns:
            Dictionary mapping client names to their information, including client ID and display name.
            Example structure:
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

        Example:
            >>> clients = Clients(commcell_object)
            >>> file_servers = clients.file_server_clients  # Use dot notation for property access
            >>> print(f"Total file server clients: {len(file_servers)}")
            >>> for name, info in file_servers.items():
            ...     print(f"Client: {name}, ID: {info['id']}, Display Name: {info['displayName']}")

        #ai-gen-doc
        """
        if self._file_server_clients is None:
            self._file_server_clients = self._get_fileserver_clients()
        return self._file_server_clients

    @property
    def laptop_clients(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all laptop clients and their information in the Commcell.

        Returns:
            Dictionary mapping laptop client names to their details, including client ID and display name.
            Example structure:
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

        Example:
            >>> clients = Clients(commcell_object)
            >>> laptop_info = clients.laptop_clients  # Use dot notation for property access
            >>> print(f"Total laptop clients: {len(laptop_info)}")
            >>> for name, info in laptop_info.items():
            >>>     print(f"Client: {name}, ID: {info['id']}, Display Name: {info['displayName']}")
        #ai-gen-doc
        """
        if not self._laptop_clients:
            self._laptop_clients = self._get_laptop_clients()
        return self._laptop_clients

    @property
    def virtual_machines(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all virtual machine clients and their details in the Commcell.

        Returns:
            Dictionary mapping virtual machine client names to their information, including hypervisor, vendor, and display name.
            Example structure:
                {
                    "vm1_name": {
                        "hypervisor": "hypervisor1",
                        "vendor": "vendor_name",
                        "displayName": "vm1_displayname"
                    },
                    "client2_name": {
                        "hypervisor": "hypervisor2",
                        "vendor": "vendor_name",
                        "displayName": "vm2_displayname"
                    }
                }

        Example:
            >>> clients = Clients(commcell_object)
            >>> vm_clients = clients.virtual_machines  # Use dot notation for property access
            >>> print(f"Total VM clients: {len(vm_clients)}")
            >>> for vm_name, vm_info in vm_clients.items():
            >>>     print(f"VM: {vm_name}, Hypervisor: {vm_info['hypervisor']}, Vendor: {vm_info['vendor']}")
        #ai-gen-doc
        """
        if not self._virtual_machines:
            self._virtual_machines = self._get_virtual_machines()
        return self._virtual_machines

    def has_client(self, client_name: str) -> bool:
        """Check if a client exists in the Commcell by name or hostname.

        Args:
            client_name: Name or hostname of the client to check.

        Returns:
            True if the client exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the client_name argument is not a string.

        Example:
            >>> clients = Clients(commcell_object)
            >>> exists = clients.has_client("Server01")
            >>> print(f"Client exists: {exists}")
            >>> # Output: Client exists: True or False

        #ai-gen-doc
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

    def has_hidden_client(self, client_name: str) -> bool:
        """Check if a client exists in the Commcell as a hidden client.

        Args:
            client_name: Name of the client to check, provided as a string.

        Returns:
            True if the client exists as a hidden client in the Commcell, False otherwise.

        Raises:
            SDKException: If the client_name argument is not a string.

        Example:
            >>> clients = Clients(commcell_object)
            >>> is_hidden = clients.has_hidden_client("Server01")
            >>> print(f"Is 'Server01' a hidden client? {is_hidden}")
        #ai-gen-doc
        """
        if not isinstance(client_name, str):
            raise SDKException('Client', '101')

        return ((self.hidden_clients and client_name.lower() in self.hidden_clients) or
                self._get_hidden_client_from_hostname(client_name) is not None)

    def _process_add_response(self, request_json: Dict[str, Any], endpoint: Optional[str] = None):
        """Run the Client Add API with the provided request JSON and parse the response.

        This method sends a POST request to the specified endpoint to add a client,
        then processes the response to determine success or failure. If the client
        is successfully created, the method refreshes the client list and returns
        the newly created client object. If the response indicates an error or is
        empty, an SDKException is raised.

        Args:
            request_json: Dictionary containing the JSON request payload for the API.
            endpoint: Optional string specifying the API endpoint to use. Defaults to '/Client'.

        Returns:
            The newly created client object if the operation is successful.

        Raises:
            SDKException: If the response is empty, indicates failure, or contains an error.

        Example:
            >>> request_json = {
            ...     "clientInfo": {
            ...         "clientName": "NewClient",
            ...         "clientType": 1
            ...     }
            ... }
            >>> clients = Clients(commcell_object)
            >>> new_client = clients._process_add_response(request_json)
            >>> print(f"Created client: {new_client}")

        #ai-gen-doc
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
            client_name: str,
            api_server_endpoint: str,
            credential_id: int,
            credential_name: str,
            access_nodes: Optional[Union[List[str], str]] = None
    ) -> 'Client':
        """Adds a new Kubernetes Cluster client to the Commcell.

            This method creates a Kubernetes client in the Commcell using the provided API server endpoint,
            service account credentials, and optional access nodes (proxy clients). If a client with the
            specified name already exists, an exception is raised.
            Args:
                client_name         (str)   --  name of the new Kubernetes Cluster client

                api_server_endpoint (str)   --  Kubernetes API Server endpoint of the cluster

                credential_id       (int)   --  ID of the credential to be associated with this client

                credential_name (str)   --  Name of the credential to be associated with this client

                access_nodes        (list/str)  --  Virtual Server proxy clients as access nodes



        Returns:
            Client: Instance of the Client class representing the newly created Kubernetes client.

        Raises:
            SDKException: If a client with the given name already exists, if access nodes do not exist,
                if the client creation fails, or if the response from the server is empty or unsuccessful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> k8s_client = clients.add_kubernetes_client(
            ...     client_name="K8sCluster01",
            ...     api_server_endpoint="https://k8s.example.com:6443",
            ...     service_account="my-service-account",
            ...     service_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
            ...     encoded_service_token="ZXlKaGJHY2lPaUpJVXpJMU5pSjkuZXlK...",
            ...     access_nodes=["Proxy01", "Proxy02"]
            ... )
            >>> print(f"Created Kubernetes client: {k8s_client}")
        #ai-gen-doc
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
                        "virtualServerCredentialinfo":{
                            "credentialId": credential_id,
                            "credentialName": credential_name
                        },
                        "k8s": {
                            "secretType": "ServiceAccount",
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
                       ndmp_server_clientname: str,
                       ndmp_server_hostname: str,
                       username: str,
                       password: str,
                       listenPort: int = 10000
                       ):
        """Add a new NAS client with NDMP and NetworkShare iDA support.

        This method creates a NAS client using the provided NDMP server details and credentials.
        The client will be configured to use the specified listening port for NDMP communication.

        Args:
            ndmp_server_clientname: Name of the new NAS client to be created.
            ndmp_server_hostname: Hostname of the NDMP server for the NAS client.
            username: NDMP username for authentication.
            password: NDMP password for authentication.
            listenPort: Port number for NDMP server to listen on (default is 10000).

        Returns:
            The client object associated with the newly created NAS client.

        Raises:
            SDKException: If the client creation fails, the response is empty, or the response indicates an error.

        Example:
            >>> clients = Clients(commcell_object)
            >>> nas_client = clients.add_nas_client(
            ...     ndmp_server_clientname="NAS_Server01",
            ...     ndmp_server_hostname="nas01.example.com",
            ...     username="ndmpuser",
            ...     password="ndmppass",
            ...     listenPort=12000
            ... )
            >>> print(f"Created NAS client: {nas_client}")

        #ai-gen-doc
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
            client_name: str,
            vcenter_hostname: str,
            vcenter_username: str,
            vcenter_password: str,
            clients: list
        ):
        """Add a new VMware Virtualization Client to the Commcell.

        This method creates a VMware Virtual Client and associates it with the specified member clients.
        The vCenter credentials are used to connect and configure the virtualization client.

        Args:
            client_name: Name of the new VMware Virtual Client.
            vcenter_hostname: Hostname of the vCenter server to connect to.
            vcenter_username: Username for vCenter authentication.
            vcenter_password: Plain-text password for vCenter authentication.
            clients: List containing client names or client objects to associate with the Virtual Client.

        Returns:
            Instance of the Client class representing the newly created VMware Virtual Client.

        Raises:
            SDKException: If a client with the given name already exists, if the client creation fails,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> clients_list = ['ClientA', 'ClientB']
            >>> new_vmware_client = clients_obj.add_vmware_client(
            ...     client_name='VMwareClient01',
            ...     vcenter_hostname='vcenter.example.com',
            ...     vcenter_username='administrator',
            ...     vcenter_password='password123',
            ...     clients=clients_list
            ... )
            >>> print(f"Created VMware client: {new_vmware_client}")
        #ai-gen-doc
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
            client_name: str,
            hyperv_hostname: str,
            hyperv_username: str,
            hyperv_password: str,
            clients: list
    ) -> 'Client':
        """Add a new Hyper-V Virtualization Client to the Commcell.

        This method creates a Hyper-V Virtualization Client and associates the specified member clients
        with it. The Hyper-V credentials are encoded before being sent to the Commcell server.

        Args:
            client_name: Name of the new Hyper-V Virtual Client.
            hyperv_hostname: Hostname of the Hyper-V server to connect to.
            hyperv_username: Login username for the Hyper-V server.
            hyperv_password: Plain-text password for the Hyper-V server.
            clients: List containing client names or client objects to associate with the Virtual Client.

        Returns:
            Client: Instance of the Client class representing the newly created Hyper-V Virtualization Client.

        Raises:
            SDKException: If a client with the given name already exists, if the client creation fails,
                or if the response from the server is empty or unsuccessful.

        Example:
            >>> clients_list = ['ClientA', 'ClientB']
            >>> new_client = clients_mgr.add_hyperv_client(
            ...     client_name='HyperV01',
            ...     hyperv_hostname='hyperv01.domain.com',
            ...     hyperv_username='admin',
            ...     hyperv_password='password123',
            ...     clients=clients_list
            ... )
            >>> print(f"Created Hyper-V client: {new_client}")

        #ai-gen-doc
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

    def add_okta_client(
            self,
            client_name: str,
            server_plan: str,
            index_server: str,
            access_nodes_list: List[Any]=[],
            **kwargs: Any
    ) -> 'Client':
        """Add a new Okta Pseudo Client to the Commcell.

        This method creates a okta pseudo client, associating it with the specified server plan,
        index server, and access nodes. Additional configuration can be provided via keyword arguments for authentication,
        okta app integration and certificate details.

        Args:
            client_name: Name of the new SharePoint pseudo client.
            server_plan: Name of the server plan to associate with the client.
            index_server: Name of the index server for the virtual client.
            access_nodes_list: List of client names (str) or Client objects to be added as access nodes.
            **kwargs: Additional configuration options, such as:
                - organization_url (str): URL of the Okta organization.
                - app_id (str): application ID for Okta.
                - cloud_region (int): Cloud region for the Okta client (default is 1).
                - shared_jr_directory (dict): Shared job results directory configuration.
                - credential_name(str): Credential name for Okta credential
        Returns:
            Client: Instance of the Client class representing the newly created Okta pseudo client.

        Raises:
            SDKException: If the client with the given name already exists, index server or server plan is not found,
                failed to add the client, or if the response is empty or unsuccessful.

        Example:
            >>> service_type = {
            ...     "Okta Global Administrator": 4,
            ...     "Okta Online": 2,
            ...     "Okta Azure Storage": 3
            ... }
            >>> access_nodes = ["client1", "client2"]
            >>> client = clients.add_okta_client(
            ...     client_name="OktaPseudo01",
            ...     server_plan="O365Plan",
            ...     service_type=service_type,
            ...     index_server="IndexServer01",
            ...     access_nodes_list=access_nodes,
            ...     tenant_url="https://tenant.okta.com",
            ...     user_username="user@domain.com",
            ...     user_password="password",
            ...     cloud_region=1
            ... )
            >>> print(f"Created Okta client: {client.client_name}")
        #ai-gen-doc
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
                raise SDKException('IndexServers', '102', f"Index server {index_server} not found")

        if self._commcell_object.plans.has_plan(server_plan):
            server_plan_object = self._commcell_object.plans.get(server_plan)
            server_plan_dict = {
                "planId": int(server_plan_object.plan_id),
                "planType": int(server_plan_object.plan_type)
            }
        else:
            raise SDKException('Storage', '102', f"Server Plan {server_plan} not found")

        member_servers = []
        proxy_servers = []
        number_of_backup_streams = kwargs.get('number_of_backup_streams', 10)

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

        server_resource_pool_map = server_plan_object._properties.get('storageResourcePoolMap', [])
        if server_resource_pool_map:
            server_plan_resources = server_resource_pool_map[0].get('resources', None)
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
                "clientType": 51,
                "lookupPlanInfo": False,
                "cloudClonnectorProperties": {
                    "instance": {
                        "cloudAppsInstance": {
                            "generalCloudProperties": {
                                "indexServer": index_server_dict,
                                "numberOfBackupStreams": number_of_backup_streams,
                                "jobResultsDir": {},
                                "memberServers": member_servers,
                                "proxyServers": proxy_servers
                            },
                            "instanceType": 59,
                            "oktaInstance": {
                                "blobPath": {},
                                "infraStructurePoolEnabled": False,
                                "isAutoDiscoveryEnabled": False,
                                "oktaAppList": {
                                    "oktaApps": []
                                },
                                "oktaOrganisationUrl": ""
                            }
                        },
                        "instance": {
                            "applicationId": 0,
                            "clientId": 0,
                            "clientName": client_name,
                            "instanceId": 0,
                            "instanceName": f"{client_name}_Instance001"
                        }
                    },
                    "instanceType": 59
                },
                "environmentType": 0,
                "plan": server_plan_dict,
                "resourcePoolAppType": -1,
                "setKeyForMultiTenantApp": False,
                "useResourcePoolInfo": False
            },
            "entity": {
                "clientName": client_name
            },
            "metaInfo": None
        }

        credential_name = kwargs.get("credential_name", "")
        if credential_name:
            credential_properties = self._commcell_object.credentials.get(credential_name)
            credential_id = credential_properties.credential_id
            okta_app_dict = {
                "isCVCreated": True,
                "oktaAppType": 1,
                "credentialEntity": {
                    "credentialId": credential_id,
                    "credentialName": kwargs.get("credential_name")
                }
            }

            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"][
                "cloudAppsInstance"]["oktaInstance"]["oktaAppList"]["oktaApps"].append(okta_app_dict)

        if len(access_nodes_list) > 1:
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"][
                "cloudAppsInstance"]["generalCloudProperties"]["jobResultsDir"] = {
                "path": kwargs.get('shared_jr_directory').get('Path')
            }

        if is_resource_pool_enabled:
            request_json["clientInfo"]["useResourcePoolInfo"] = is_resource_pool_enabled

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_OKTA_CLIENT, request_json
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
                    raise SDKException('Response', '102', 'Response/Error message not found')
            else:
                raise SDKException('Response', '102', 'Response is not json serializable')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_share_point_client(
            self,
            client_name: str,
            server_plan: str,
            service_type: Dict[str, int],
            index_server: str,
            access_nodes_list: List[Any],
            **kwargs: Any
        ) -> 'Client':
        """Add a new Office 365 SharePoint Pseudo Client to the Commcell.

        This method creates a SharePoint pseudo client for Office 365, associating it with the specified server plan,
        index server, and access nodes. Additional configuration can be provided via keyword arguments for authentication,
        Azure app integration, certificate details, and cloud region selection.

        Args:
            client_name: Name of the new SharePoint pseudo client.
            server_plan: Name of the server plan to associate with the client.
            service_type: Dictionary mapping SharePoint service types to their integer values.
            index_server: Name of the index server for the virtual client.
            access_nodes_list: List of client names (str) or Client objects to be added as access nodes.
            **kwargs: Additional configuration options, such as:
                - tenant_url (str): URL of the SharePoint tenant.
                - user_username (str): Username for SharePoint user authentication.
                - user_password (str): Password for SharePoint user authentication.
                - azure_username (str): Username for Azure app authentication.
                - azure_secret (str): Secret key for Azure app authentication.
                - global_administrator (str): Username of the global administrator.
                - global_administrator_password (str): Password for the global administrator.
                - azure_app_id (str): Azure app ID for SharePoint Online.
                - azure_app_key_id (str): App key for SharePoint Online.
                - azure_directory_id (str): Azure directory ID for SharePoint Online.
                - cert_string (str): Certificate string for authentication.
                - cert_password (str): Certificate password.
                - cloud_region (int): Cloud region for the SharePoint client (default is 1).
                - shared_jr_directory (dict): Shared job results directory configuration.
                - is_modern_auth_enabled (bool): Enable modern authentication (default is False).
                - credential_name(str):  Credential
        Returns:
            Client: Instance of the Client class representing the newly created SharePoint pseudo client.

        Raises:
            SDKException: If the client with the given name already exists, index server or server plan is not found,
                failed to add the client, or if the response is empty or unsuccessful.

        Example:
            >>> service_type = {
            ...     "Sharepoint Global Administrator": 4,
            ...     "Sharepoint Online": 2,
            ...     "Sharepoint Azure Storage": 3
            ... }
            >>> access_nodes = ["client1", "client2"]
            >>> client = clients.add_share_point_client(
            ...     client_name="SharePointPseudo01",
            ...     server_plan="O365Plan",
            ...     service_type=service_type,
            ...     index_server="IndexServer01",
            ...     access_nodes_list=access_nodes,
            ...     tenant_url="https://tenant.sharepoint.com",
            ...     user_username="user@domain.com",
            ...     user_password="password",
            ...     cloud_region=1
            ... )
            >>> print(f"Created SharePoint client: {client.client_name}")
        #ai-gen-doc
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

        server_resource_pool_map = server_plan_object._properties.get('storageResourcePoolMap', [])
        if server_resource_pool_map:
            server_plan_resources = server_resource_pool_map[0].get('resources', None)
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

                if kwargs.get("credential_name", None):
                    credential_properties = self._commcell_object.credentials.get(kwargs.get("credential_name"))
                    credential_id = credential_properties.credential_id
                    azure_app_dict = {
                        "appStatus": 1,
                        "azureAppType": 1,
                        "certificate": {},
                        "credentialEntity": {
                            "credentialId": credential_id,
                            "credentialName": kwargs.get("credential_name")
                        }
                    }

                    tenant_info_dict = {
                        "azureTenantID": kwargs.get('azure_directory_id')
                    }
                    request_json["clientInfo"]["sharepointPseudoClientProperties"]["sharepointBackupSet"][
                        "spOffice365BackupSetProp"]["tenantInfo"] = tenant_info_dict

                else:
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
                          new_client_name: str,
                          master_uri: str,
                          master_node: str,
                          plan: str,
                          **kwargs: Any):
        """Add a new Splunk client to the Commcell environment after validating the client name and plan.

        Args:
            new_client_name: Name of the new Splunk client to be added.
            master_uri: URI for the Splunk master node.
            master_node: Name of the master node client.
            plan: Name of the plan to associate with the new client.
            **kwargs: Additional keyword arguments for authentication:
                password (str): Password for the Splunk instance (if not using credential_name).
                user_name (str): Username for the Splunk instance (if not using credential_name).
                credential_name (str): Name of the credential associated with the Splunk instance.

        Returns:
            The client object associated with the newly created Splunk client.

        Raises:
            SDKException: If the plan or master client is invalid, or if the client creation fails.

        Example:
            >>> clients = Clients(commcell_object)
            >>> # Using username and password
            >>> splunk_client = clients.add_splunk_client(
            ...     new_client_name="SplunkNode01",
            ...     master_uri="https://splunk-master:8089",
            ...     master_node="MasterNode",
            ...     plan="SplunkPlan",
            ...     user_name="admin",
            ...     password="splunk_password"
            ... )
            >>> print(f"Created Splunk client: {splunk_client}")

            >>> # Using credential name
            >>> splunk_client = clients.add_splunk_client(
            ...     new_client_name="SplunkNode02",
            ...     master_uri="https://splunk-master:8089",
            ...     master_node="MasterNode",
            ...     plan="SplunkPlan",
            ...     credential_name="SplunkCredential"
            ... )
            >>> print(f"Created Splunk client with credential: {splunk_client}")

        #ai-gen-doc
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

        if 'credential_name' not in kwargs:
            request_json["clientInfo"]["distributedClusterInstanceProperties"]["clusterConfig"]["splunkConfig"][
                "splunkUser"] = {
                "password": kwargs.get('password'),
                "userName": kwargs.get('user_name')
            }
        else:
            cred_name=kwargs.get('credential_name')
            self.credential = self._commcell_object.credentials.get(cred_name)
            request_json["clientInfo"]["distributedClusterInstanceProperties"]["clusterConfig"]["splunkConfig"][
                "splunkUserCredInfo"] = {
                "credentialId": self.credential.credential_id,
                "credentialName": cred_name
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
                            instance_name: str,
                            db_host: str,
                            yugabyte_credname: str,
                            universe_name: str,
                            config_name: str,
                            credential_name: str,
                            content: List[str],
                            plan_name: str,
                            data_access_nodes: List[str],
                            user_uuid: str,
                            universe_uuid: str,
                            config_uuid: str):
        """Add a new Yugabyte client to the Commcell environment.

        This method creates a new Yugabyte client using the provided configuration details,
        including instance information, database host, API token, universe details, customer
        configuration, credentials, content paths, plan association, and data access nodes.

        Args:

            instance_name: Name for the new Yugabyte instance.
            db_host: Hostname of the YugabyteAnywhere application.
            yugabyte_credname: yugabyte credential name.
            universe_name: Name of the Yugabyte universe to be backed up.
            config_name: Customer configuration name.
            credential_name: Credential name associated with the customer configuration.
            content: List of content paths for the default subclient.
            plan_name: Name of the plan to associate with the client.
            data_access_nodes: List of data access node client names.
            user_uuid: UUID of the YugabyteDB user.
            universe_uuid: UUID of the YugabyteDB universe.
            config_uuid: UUID of the YugabyteDB user configuration.

        Returns:
            The client object associated with the newly created Yugabyte client.

        Raises:
            SDKException: If the client creation fails, the response is empty, or the response indicates an error.

        Example:
            >>> content_paths = ["/data/yugabyte/table1", "/data/yugabyte/table2"]
            >>> access_nodes = ["node1", "node2"]
            >>> client_obj = clients.add_yugabyte_client(
            ...     instance_name="YB_Instance01",
            ...     db_host="yugabyte.example.com",
            ...     yugabyte_credname="ybcredname",
            ...     universe_name="TestUniverse",
            ...     config_name="CustomerConfig01",
            ...     credential_name="YB_Credential",
            ...     content=content_paths,
            ...     plan_name="YB_BackupPlan",
            ...     data_access_nodes=access_nodes,
            ...     user_uuid="user-uuid-123",
            ...     universe_uuid="universe-uuid-456",
            ...     config_uuid="config-uuid-789"
            ... )
            >>> print(f"Created Yugabyte client: {client_obj}")

        #ai-gen-doc
        """

        content_temp = []
        for path in content:
            content_temp.append({"path": path})

        access_nodes = []
        for node in data_access_nodes:
            access_nodes.append({"clientName": node})

        yugabyte_credential = self._commcell_object.credentials.get(yugabyte_credname)
        yugabyte_cred_id = yugabyte_credential.credential_id

        s3_credential = self._commcell_object.credentials.get(credential_name)
        s3_cred_id = s3_credential.credential_id

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
                                "yugaByteCredInfo": {
                                    "credentialId": yugabyte_cred_id,
                                    "credentialName": yugabyte_credname
                                },
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
                                        "credentialId": s3_cred_id
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
                             instance_name: str,
                             data_access_nodes: List[str],
                             couchbase_credname: str,
                             port: Union[str, int],
                             staging_type: str,
                             staging_path: str,
                             credential_name: str,
                             service_host: str,
                             plan_name: str,
                             db_host: str
                             ):
        """Add a new Couchbase client to the Commcell environment.

        This method creates a Couchbase pseudo-client with the specified configuration,
        including data access nodes, credentials, staging type, and associated plan.
        Supports both FileSystem and S3 staging types.

        Args:
            instance_name: Name for the new Couchbase instance.
            data_access_nodes: List of client names to be used as data access nodes.
            couchbase_credname: Couchbase credential name.
            port: Couchbase database port (as string or integer).
            staging_type: Staging type, either "FileSystem" or "S3".
            staging_path: Path for staging data (filesystem path or S3 bucket path).
            credential_name: Name of the S3 credential (required for S3 staging).
            service_host: AWS service host (required for S3 staging).
            plan_name: Name of the plan to associate with the client.
            db_host: Couchbase database host.

        Returns:
            Object representing the newly created Couchbase client.

        Raises:
            SDKException: If the client creation fails, the response is empty, or the response indicates an error.


        Example:
            >>> clients = Clients(commcell_object)
            >>> couchbase_client = clients.add_couchbase_client(
            ...     instance_name="CB_Instance01",
            ...     data_access_nodes=["node1", "node2"],
            ...     user_name="admin",
            ...     password="securepass",
            ...     port=8091,
            ...     staging_type="FileSystem",
            ...     staging_path="/mnt/couchbase_staging",
            ...     credential_name="",
            ...     service_host="",
            ...     plan_name="CouchbasePlan"
            ... )
            >>> print(f"Created Couchbase client: {couchbase_client}")

        #ai-gen-doc
        """

        access_nodes = []
        for node in data_access_nodes:
            access_nodes.append({"clientName": node})

        port = int(port)

        couchbase_credential = self._commcell_object.credentials.get(couchbase_credname)
        couchbase_cred_id = couchbase_credential.credential_id

        s3_credential = self._commcell_object.credentials.get(credential_name)
        s3_cred_id = s3_credential.credential_id

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
                                    "dbHost": db_host,
                                    "couchBaseCMCredInfo": {
                                        "credentialId": couchbase_cred_id,
                                        "credentialName": couchbase_credname
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
                                    "dbHost": db_host,
                                    "couchBaseCMCredInfo": {
                                        "credentialId": couchbase_cred_id,
                                        "credentialName": couchbase_credname
                                    },
                                    "staging": {
                                        "stagingType": 1,
                                        "stagingPath": staging_path,
                                        "serviceHost": service_host,
                                        "instanceType": 5,
                                        "cloudURL": "s3.amazonaws.com",
                                        "recordType": "AMAZON_S3",
                                        "stagingCredentials": {
                                            "credentialName": credential_name,
                                            "credentialId": s3_cred_id
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
            client_name: str,
            index_server: str,
            clients_list: List[Any],
            server_plan: str,
            recall_service_url: str,
            job_result_dir: str,
            exchange_servers: List[Any],
            service_accounts: List[Dict[str, Any]],
            azure_app_key_secret: str = "",
            azure_tenant_name: str = "",
            azure_app_key_id: str = "",
            environment_type: int = 0,
            backupset_type_to_create: int = 1,
            **kwargs: Any
        ) -> Any:
        """Add a new Exchange Mailbox Client to the Commcell.

        This method creates a new Exchange Mailbox Client with the specified configuration,
        including associated member servers, service accounts, Exchange servers, and Azure credentials.
        It supports both on-premise and Exchange Online environments.

        Args:
            client_name: Name of the new Exchange Mailbox Client.
            index_server: Index server for the virtual client.
            clients_list: List of client names (str) or client objects to associate with the virtual client.
            server_plan: Server plan to associate with the client.
            recall_service_url: Recall service URL for the client.
            job_result_dir: Directory path for job results.
            exchange_servers: List of Exchange server names or objects.
            service_accounts: List of dictionaries containing service account details. Each dictionary should include:
                - 'ServiceType': int
                - 'Username': str
                - 'Password': str
            azure_app_key_secret: App secret for Exchange Online.
            azure_tenant_name: Azure tenant name for Exchange Online.
            azure_app_key_id: App key ID for Exchange Online.
            environment_type: Exchange environment type.
                Supported values:
                    1: Exchange on-premise
                    2: Exchange Hybrid with on-premise Exchange Server
                    3: Exchange Hybrid with on-premise AD
                    4: Exchange Online
            backupset_type_to_create: Backup set type to create.
                Supported values:
                    1: User mailbox (default)
                    2: Journal mailbox
                    3: Content store mailbox
            **kwargs: Additional optional arguments.
                - is_modern_auth_enabled (bool): Whether to enable modern authentication for Exchange Online. Default is True.
                - credential_name (str): Credential name for Azure authentication.

        Returns:
            Instance of the Client class representing the newly created Exchange Mailbox Client.

        Raises:
            SDKException: If a client with the given name already exists, if the client creation fails,
                or if the response from the server is invalid.

        Example:
            >>> clients = Clients(commcell_object)
            >>> service_accounts = [
            ...     {'ServiceType': 1, 'Username': 'admin@domain.com', 'Password': 'password123'},
            ...     {'ServiceType': 2, 'Username': 'admin2@domain.com', 'Password': 'password456'}
            ... ]
            >>> exchange_servers = ['EXCH01', 'EXCH02']
            >>> new_client = clients.add_exchange_client(
            ...     client_name='ExchangeClient01',
            ...     index_server='IndexServer01',
            ...     clients_list=['ClientA', 'ClientB'],
            ...     server_plan='ExchangePlan',
            ...     recall_service_url='https://recall.service.url',
            ...     job_result_dir='/var/results',
            ...     exchange_servers=exchange_servers,
            ...     service_accounts=service_accounts,
            ...     azure_app_key_secret='app_secret',
            ...     azure_tenant_name='tenant_name',
            ...     azure_app_key_id='app_key_id',
            ...     environment_type=4,
            ...     backupset_type_to_create=1,
            ...     is_modern_auth_enabled=True
            ... )
            >>> print(f"Created Exchange client: {new_client}")
        #ai-gen-doc
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
                    "backupSetTypeToCreate": backupset_type_to_create,
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
        if kwargs.get("credential_name", None):
            credential_properties = self._commcell_object.credentials.get(kwargs.get("credential_name"))
            credential_id = credential_properties.credential_id
            azure_app_dict = {
                "azureApps": [
                    {
                        "appStatus": 1,
                        "azureAppType": 1,
                        "credentialEntity": {
                            "credentialId": credential_id,
                            "credentialName": kwargs.get("credential_name")
                        }
                    }
                ]
            }
            request_json["clientInfo"]["exchangeOnePassClientProperties"]["onePassProp"][
                "azureAppList"] = azure_app_dict
        elif int(self._commcell_object.version.split(".")[1]) >= 23:
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

        if int(self._commcell_object.version.split(".")[1]) >= 25 and (environment_type == 4 or environment_type == 2):
            request_json["clientInfo"][
                "clientType"] = 37  # 37 - Office365 Client type. Exchange Online falls under O365 AppType
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
            client_name: str,
            server_plan: str,
            dc_plan: str,
            hold_type: int
        ) -> 'Client':
        """Add a new Exchange Mailbox Case Client to the Commcell.

        This method creates a new Case Client with the specified name, associates it with the provided
        server and DC plans, and sets the client type according to the hold_type value.

        Args:
            client_name: Name of the new Case Client to be created.
            server_plan: Name of the server plan to associate with the case client.
            dc_plan: Name of the DC plan to associate with the case client.
            hold_type: Type of client (valid values: 1, 2, or 3).

        Returns:
            Client: An instance of the Client class representing the newly created case client.

        Raises:
            SDKException: If a client with the given name already exists, if the client creation fails,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> clients = Clients(commcell_object)
            >>> new_client = clients.add_case_client(
            ...     client_name="LegalCase01",
            ...     server_plan="ServerPlanA",
            ...     dc_plan="DCPlanB",
            ...     hold_type=1
            ... )
            >>> print(f"Created case client: {new_client}")
            >>> # The returned Client object can be used for further client operations

        #ai-gen-doc
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
            client_name: str,
            access_node: str,
            salesforce_options: Dict[str, Any],
            db_options: Optional[Dict[str, Any]] = None,
            **kwargs: Any
        ):
        """Add a new Salesforce Client to the Commcell environment.

        This method creates a Salesforce pseudo client with the specified configuration,
        including Salesforce connection options, access node, and optional database settings
        for sync operations. Additional keyword arguments allow customization of instance name,
        cache paths, storage policy, and backup streams.

        Args:
            client_name: Name of the Salesforce pseudo client to be created.
            access_node: Name of the access node for the client.
            salesforce_options: Dictionary containing Salesforce connection options, such as:
                - login_url: Salesforce login URL.
                - consumer_id: Salesforce consumer key.
                - consumer_secret: Salesforce consumer secret.
                - salesforce_user_name: Salesforce login user.
                - salesforce_user_password: Salesforce user password.
                - salesforce_user_token: Salesforce user token.
                - sandbox: Boolean indicating sandbox environment (default False).
            db_options: Optional dictionary for database sync configuration, such as:
                - db_enabled: Boolean to enable database sync.
                - db_type: 'SQLSERVER' or 'POSTGRESQL'.
                - db_host_name: Database hostname.
                - db_instance: Database instance name.
                - db_name: Database name.
                - db_port: Database port.
                - db_user_name: Database user name.
                - db_user_password: Database user password.
            **kwargs: Additional keyword arguments for client customization:
                - instance_name: Name of the Salesforce instance.
                - download_cache_path: Path for download cache.
                - mutual_auth_path: Path to mutual auth certificate.
                - storage_policy: Storage policy name.
                - streams: Number of backup streams.

        Returns:
            Client: Instance of the Client class representing the newly added Salesforce client.

        Raises:
            SDKException: If a client with the given name already exists, if required inputs are missing,
                or if the client addition fails due to an unsuccessful response.

        Example:
            >>> salesforce_options = {
            ...     "login_url": "https://login.salesforce.com",
            ...     "consumer_id": "your_consumer_key",
            ...     "consumer_secret": "your_consumer_secret",
            ...     "salesforce_user_name": "user@example.com",
            ...     "salesforce_user_password": "password123",
            ...     "salesforce_user_token": "user_token",
            ...     "sandbox": False
            ... }
            >>> db_options = {
            ...     "db_enabled": True,
            ...     "db_type": "SQLSERVER",
            ...     "db_host_name": "db.example.com",
            ...     "db_instance": "instance1",
            ...     "db_name": "sfdb",
            ...     "db_port": 1433,
            ...     "db_user_name": "dbuser",
            ...     "db_user_password": "dbpass"
            ... }
            >>> client = clients.add_salesforce_client(
            ...     client_name="SalesforceClient01",
            ...     access_node="AccessNode01",
            ...     salesforce_options=salesforce_options,
            ...     db_options=db_options,
            ...     instance_name="SF_Instance",
            ...     download_cache_path="/tmp/sf_cache",
            ...     storage_policy="SalesforcePolicy",
            ...     streams=4
            ... )
            >>> print(f"Salesforce client created: {client}")

        #ai-gen-doc
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

    def add_azure_client(self, client_name: str, access_node: str, azure_options: Dict[str, str]):
        """Add a new Azure cloud client to the Commcell environment.

        This method creates a pseudo client for Azure cloud by providing the required subscription, tenant,
        application, and password details. The client will be associated with the specified access node.

        Args:
            client_name: Name of the Azure cloud client to be created.
            access_node: Name of the cloud access node to associate with the client.
            azure_options: Dictionary containing Azure configuration details. Must include:
                - "subscription_id": Azure subscription ID as a string.
                - "tenant_id": Azure tenant ID as a string.
                - "application_id": Azure application ID as a string.
                - "password": Azure application password as a string.

        Returns:
            Instance of the Client class representing the newly created Azure client.

        Raises:
            SDKException: If any value in azure_options is None.
            SDKException: If a client with the same name already exists.

        Example:
            >>> azure_options = {
            ...     "subscription_id": "your-subscription-id",
            ...     "tenant_id": "your-tenant-id",
            ...     "application_id": "your-application-id",
            ...     "password": "your-application-password"
            ... }
            >>> clients = Clients(commcell_object)
            >>> new_client = clients.add_azure_client("AzureClient01", "AccessNode01", azure_options)
            >>> print(f"Created Azure client: {new_client}")

        #ai-gen-doc
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

    def add_amazon_client(self, client_name: str, access_node: str, amazon_options: Dict[str, Any]):
        """Add a new Amazon cloud client to the Commcell environment.

        This method creates a new Amazon cloud client using the provided authentication details.
        The `amazon_options` dictionary should contain the necessary credentials or IAM role information
        for authenticating with Amazon Web Services.

        Args:
            client_name: Name of the Amazon cloud client to be created.
            access_node: Name of the cloud access node to associate with the client.
            amazon_options: Dictionary containing Amazon authentication details. Supported authentication methods:
                - AccessKey and SecretKey authentication:
                    Example:
                        amazon_options = {
                            "accessKey": "your-access-key",
                            "secretkey": "your-secret-key"
                        }
                - IAM Role authentication (set "useIamRole" to True):
                    Example:
                        amazon_options = {
                            "useIamRole": True
                        }
                - STS Role ARN authentication (provide Role ARN in "accessKey"):
                    Example:
                        amazon_options = {
                            "accessKey": "arn:aws:iam::123456789012:role/YourRole"
                        }

        Returns:
            Instance of the Client class representing the newly created Amazon cloud client.

        Raises:
            SDKException: If any value in amazon_options is None, or if a client with the same name already exists.

        Example:
            >>> amazon_options = {
            ...     "accessKey": "AKIA...",
            ...     "secretkey": "abcd1234..."
            ... }
            >>> clients = Clients(commcell_object)
            >>> new_client = clients.add_amazon_client("AmazonClient01", "AccessNode01", amazon_options)
            >>> print(f"Created Amazon client: {new_client}")

        #ai-gen-doc
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

    def add_google_client(self, client_name: str, access_node: str, google_options: Dict[str, Any]) -> 'Client':
        """Add a new Google Cloud client to the Commcell environment.

        This method creates a pseudo client for Google Cloud using the provided credentials and access node.
        The google_options dictionary must contain valid values for 'serviceAccountId', 'userName', and 'password'.

        Args:
            client_name: Name of the Google Cloud client to be created.
            access_node: Name of the cloud access node to associate with the client.
            google_options: Dictionary containing Google Cloud credentials and details.
                Required keys:
                    - serviceAccountId: Service account ID for Google Cloud.
                    - userName: Username for authentication.
                    - password: Password for authentication.

        Returns:
            Client: Instance of the Client class representing the newly created Google Cloud client.

        Raises:
            SDKException: If any value in google_options is None.
            SDKException: If a pseudo client with the same name already exists.

        Example:
            >>> google_options = {
            ...     "serviceAccountId": "my-service-account-id",
            ...     "userName": "admin@domain.com",
            ...     "password": "securepassword"
            ... }
            >>> clients = Clients(commcell_object)
            >>> new_client = clients.add_google_client("GoogleClient01", "AccessNode01", google_options)
            >>> print(f"Created Google Cloud client: {new_client}")

        #ai-gen-doc
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

    def add_googleworkspace_client(
        self,
        plan_name: str,
        client_name: str,
        indexserver: str,
        service_account_details: Dict[str, Any],
        credential_name: str,
        instance_type: int,
        **kwargs: Any
    ):
        """Add a new Google Workspace client to the Commcell environment.

        This method creates a new Google Workspace client using the provided plan, credentials,
        and service account details. You must specify either `client_group_name` or `access_node`
        in the keyword arguments. If both are provided, `client_group_name` is used by default.

        Args:
            plan_name: Name of the server plan to associate with the client.
            client_name: The name to assign to the new Google Workspace client.
            indexserver: The index server address for the client.
            service_account_details: Dictionary containing service account details required for authentication and authorization.
                Example:
                    {
                        "accounts": [
                            {
                                "serviceType": "ExampleAgentServiceType",
                                "AdminSmtpAddress": "example@google.com"
                            }
                        ]
                    }
            credential_name: Name of the credential created in Credential Vault.
            instance_type: Integer representing the type of Google client.
            **kwargs: Additional parameters for client creation.
                - client_group_name (str): Access Node Group Name.
                - access_node (str): Access Node name.
                - jr_path (str): Job Results Directory path (mandatory if client_group_name is provided).
                - no_of_streams (int): Number of backup streams to create for the client.

        Returns:
            Client: Instance of the Client class representing the newly created Google Workspace client.

        Raises:
            SDKException: If neither `client_group_name` nor `access_node` is provided, or if client creation fails.

        Example:
            >>> service_account_details = {
            ...     "accounts": [
            ...         {
            ...             "serviceType": "SYSTEM_ACCOUNT",
            ...             "AdminSmtpAddress": "admin@google.com",
            ...             "userAccount": {
            ...                 "password": "my_password",
            ...                 "confirmPassword": "my_password"
            ...             }
            ...         }
            ...     ]
            ... }
            >>> client = clients.add_googleworkspace_client(
            ...     plan_name="GooglePlan",
            ...     client_name="GoogleClient01",
            ...     indexserver="IndexServer01",
            ...     service_account_details=service_account_details,
            ...     credential_name="GoogleCred",
            ...     instance_type=1,
            ...     client_group_name="AccessNodeGroup01",
            ...     jr_path="/job/results/dir",
            ...     no_of_streams=5
            ... )
            >>> print(f"Created Google Workspace client: {client}")

        #ai-gen-doc
        """
        is_client_group = True if kwargs.get('client_group_name') else False
        proxy_node = kwargs.get('client_group_name') if is_client_group else kwargs.get('access_node')
        if proxy_node is None:
            raise SDKException(
                'Client',
                '102',
                "Either client_group_name or access_node should be provided.")

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

    def add_alicloud_client(self, client_name: str, access_node: str, alicloud_options: Dict[str, str]):
        """Add a new Alibaba Cloud (Alicloud) client to the Commcell.

        This method creates a pseudo client for Alibaba Cloud using the provided credentials and access node.
        The `alicloud_options` dictionary must contain valid "accessKey" and "secretkey" values.

        Args:
            client_name: Name of the new Alicloud client as a string.
            access_node: Name of the cloud access node as a string.
            alicloud_options: Dictionary containing Alicloud credentials. Must include:
                - "accessKey": The access key for Alicloud authentication.
                - "secretkey": The secret key for Alicloud authentication.

        Returns:
            Instance of the Client class representing the newly added Alicloud client.

        Raises:
            SDKException: If any value in `alicloud_options` is None, or if a client with the same name already exists.

        Example:
            >>> alicloud_options = {
            ...     "accessKey": "your-access-key",
            ...     "secretkey": "your-secret-key"
            ... }
            >>> clients = Clients(commcell_object)
            >>> new_client = clients.add_alicloud_client("AlicloudClient01", "AccessNode01", alicloud_options)
            >>> print(f"Added new Alicloud client: {new_client}")

        #ai-gen-doc
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

    def add_teams_client(
        self,
        client_name: str,
        server_plan: str,
        azure_app_id: str,
        azure_directory_id: str,
        azure_app_key_id: str,
        **kwargs: Any
    ):
        """Add a new Teams client to the Commcell environment.

        This method creates a Teams client using the provided Azure and server plan details.
        Additional infrastructure and configuration options can be specified via keyword arguments.

        Args:
            client_name: Name of the Teams client to be added.
            server_plan: Name of the server plan to associate with the client.
            azure_app_id: Azure application ID for authentication.
            azure_directory_id: Azure directory (tenant) ID.
            azure_app_key_id: Azure application key ID.
            **kwargs: Optional keyword arguments for advanced configuration:
                - index_server (str): Name of the index server client.
                - access_nodes_list (List[Union[str, 'Client']]): List of access node client names or Client objects.
                - number_of_backup_streams (int): Number of backup streams to associate (default: 10).
                - user_name (str): Username for shared job results (required for multi-access node clients).
                - user_password (str): Password for shared job results (required for multi-access node clients).
                - shared_jr_directory (str): Path to shared job results directory (required for multi-access node clients).
                - cloud_region (int): Cloud region identifier (default: 1).
                - credential_name (str): Name of the credential to use.

        Returns:
            Instance of the Client class representing the newly added Teams client.

        Raises:
            SDKException: If the client already exists, the server plan does not exist,
                invalid input types are provided, access node does not exist,
                required infrastructure details are missing, or if the client addition fails.

        Example:
            >>> clients = Clients(commcell_object)
            >>> teams_client = clients.add_teams_client(
            ...     client_name="TeamsClient01",
            ...     server_plan="TeamsServerPlan",
            ...     azure_app_id="your-azure-app-id",
            ...     azure_directory_id="your-azure-directory-id",
            ...     azure_app_key_id="your-azure-app-key-id",
            ...     index_server="IndexServer01",
            ...     access_nodes_list=["AccessNode01", "AccessNode02"],
            ...     user_name="serviceuser",
            ...     user_password="password123",
            ...     shared_jr_directory="/shared/results",
            ...     cloud_region=1
            ... )
            >>> print(f"Teams client added: {teams_client.client_name}")
        #ai-gen-doc
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

        if kwargs.get("credential_name", None):
            credential_properties = self._commcell_object.credentials.get(kwargs.get("credential_name"))
            credential_id = credential_properties.credential_id
            azure_app_dict = {
                "azureApps": [
                    {
                        "appStatus": 1,
                        "azureAppType": 2,
                        "credentialEntity": {
                            "credentialId": credential_id,
                            "credentialName": kwargs.get("credential_name")
                        }
                    }
                ]
            }
            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "v2CloudAppsInstance"][
                "azureAppList"] = azure_app_dict

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
            client_name: str,
            server_plan: str,
            azure_app_id: str,
            azure_directory_id: str,
            azure_app_key_id: str,
            **kwargs: Any
        ):
        """Add a OneDrive for Business (v2) client to the Commcell environment.

        This method provisions a new OneDrive for Business client using the specified Azure application credentials
        and associates it with a server plan. Additional infrastructure details such as access nodes, index server,
        backup streams, and service account information can be provided via keyword arguments.

        Args:
            client_name: Name of the client to be created.
            server_plan: Name of the server plan to associate with the client.
            azure_app_id: Azure application ID for authentication.
            azure_directory_id: Azure directory (tenant) ID.
            azure_app_key_id: Azure application key ID (will be base64 encoded).
            **kwargs: Additional optional parameters:
                index_server (str): Name of the index server client.
                access_nodes_list (List[Union[str, 'Client']]): List of access node client names or Client objects.
                number_of_backup_streams (int): Number of backup streams to associate (default: 10).
                user_name (str): Service account username for shared job results.
                user_password (str): Service account password for shared job results.
                shared_jr_directory (str): Path to the shared job results directory.
                cloud_region (int): Cloud region identifier (default: 1).
                credential_name(str):  Credential
        Returns:
            Instance of the Client class representing the newly created OneDrive for Business client.

        Raises:
            SDKException: If the client already exists, server plan is invalid, access node is missing,
                input data types are incorrect, required infrastructure details are missing, or client creation fails.

        Example:
            >>> # Add a OneDrive for Business client with a single access node
            >>> client = clients.add_onedrive_for_business_client(
            ...     client_name="OneDriveClient01",
            ...     server_plan="O365ServerPlan",
            ...     azure_app_id="your-azure-app-id",
            ...     azure_directory_id="your-azure-directory-id",
            ...     azure_app_key_id="your-azure-app-key-id",
            ...     index_server="IndexServer01",
            ...     access_nodes_list=["AccessNode01"]
            ... )
            >>> print(f"Created OneDrive client: {client.client_name}")

            >>> # Add a client with multiple access nodes and service account details
            >>> client = clients.add_onedrive_for_business_client(
            ...     client_name="OneDriveClient02",
            ...     server_plan="O365ServerPlan",
            ...     azure_app_id="your-azure-app-id",
            ...     azure_directory_id="your-azure-directory-id",
            ...     azure_app_key_id="your-azure-app-key-id",
            ...     index_server="IndexServer01",
            ...     access_nodes_list=["AccessNode01", "AccessNode02"],
            ...     user_name="serviceuser",
            ...     user_password="servicepassword",
            ...     shared_jr_directory="/shared/job/results"
            ... )
            >>> print(f"Created OneDrive client with multiple access nodes: {client.client_name}")

        #ai-gen-doc
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

        if kwargs.get("credential_name", None):
            credential_properties = self._commcell_object.credentials.get(kwargs.get("credential_name"))
            credential_id = credential_properties.credential_id
            azure_app_dict = {
                "azureApps": [
                    {
                        "appStatus": 1,
                        "azureAppType": 1,
                        "credentialEntity": {
                            "credentialId": credential_id,
                            "credentialName": kwargs.get("credential_name")
                        }
                    }
                ]
            }

            request_json["clientInfo"]["cloudClonnectorProperties"]["instance"]["cloudAppsInstance"][
                "oneDriveInstance"]["azureAppList"] = azure_app_dict

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
                            client_name: str,
                            instance_name: str,
                            server_plan: str,
                            connection_details: Dict[str, str],
                            access_node: Optional[str] = None,
                            auto_discovery: bool = False
                            ):
        """Add a new OneDrive Client to the Commcell environment.

        This method creates a new OneDrive client using the provided Azure application details,
        associates it with the specified server plan, and optionally configures an access node
        and auto-discovery settings.

        Args:
            client_name: Name of the new OneDrive client to be created.
            instance_name: Name of the instance for the OneDrive client.
            server_plan: Name of the server plan to associate with the client.
            connection_details: Dictionary containing Azure application details. Example:
                {
                    "azure_directory_id": "your-azure-directory-id",
                    "application_id": "your-application-id",
                    "application_key_value": "your-application-key-value"
                }
            access_node: Optional; name of the access node to use for proxy operations.
            auto_discovery: Optional; set to True to enable auto-discovery of OneDrive accounts.

        Returns:
            Instance of the Client class representing the newly created OneDrive client.

        Raises:
            SDKException: If the client name already exists, the server plan is invalid,
                the access node is invalid, the client creation fails, or the response is empty or unsuccessful.

        Example:
            >>> connection_details = {
            ...     "azure_directory_id": "your-azure-directory-id",
            ...     "application_id": "your-application-id",
            ...     "application_key_value": "your-application-key-value"
            ... }
            >>> clients = Clients(commcell_object)
            >>> new_client = clients.add_onedrive_client(
            ...     client_name="OneDriveClient01",
            ...     instance_name="OneDriveInstance01",
            ...     server_plan="OneDriveServerPlan",
            ...     connection_details=connection_details,
            ...     access_node="AccessNode01",
            ...     auto_discovery=True
            ... )
            >>> print(f"Created OneDrive client: {new_client}")

        #ai-gen-doc
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

    def add_nutanix_files_client(self, client_name: str, array_name: str, cifs_option: bool = True, nfs_option: bool = True):
        """Add a new Nutanix Files client to the Commcell.

        This method creates a Nutanix Files pseudo client associated with the specified array name.
        You can optionally enable Windows (CIFS) and/or Linux (NFS) File System agents for the client.

        Args:
            client_name: Name of the Nutanix Files client to be created.
            array_name: FQDN of the Nutanix array (File Server) to associate with the client.
            cifs_option: If True, adds the Windows File System (CIFS) agent to the client.
            nfs_option: If True, adds the Linux File System (NFS) agent to the client.

        Returns:
            Instance of the Client class representing the newly created Nutanix Files client.

        Raises:
            SDKException: If both nfs_option and cifs_option are False.
            SDKException: If a pseudo client with the same name already exists.
            SDKException: If the Commcell response indicates a failure.

        Example:
            >>> clients = Clients(commcell_object)
            >>> nutanix_client = clients.add_nutanix_files_client(
            ...     client_name="NutanixFiles01",
            ...     array_name="nutanix-array.domain.com",
            ...     cifs_option=True,
            ...     nfs_option=False
            ... )
            >>> print(f"Created Nutanix Files client: {nutanix_client}")
        #ai-gen-doc
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

    def add_lustre_client(
        self,
        client_name: str,
        data_access_nodes: List[str],
        plan_name: str,
        content: List[str],
        isAzureManagedLustre: bool = False
    ):
        """Add a new Lustre client to the Commcell environment.

        This method creates a Lustre distributed file system client with the specified configuration,
        including data access nodes, plan association, and content paths. It supports both standard
        Lustre and Azure Managed Lustre configurations.

        Args:
            client_name (str): Name for the new Lustre client to be created.
            
            data_access_nodes (List[str]): List of client names to be used as data access nodes 
                for the Lustre client. These nodes handle data transfer operations.
            
            plan_name (str): Name of the backup plan to associate with the client. The plan must 
                exist in the Commcell.
            
            content (List[str]): List of file system paths to be included in the backup content.
                Example: ["/lustre/data", "/lustre/home"]
            
            isAzureManagedLustre (bool, optional): If True, configures the client as an Azure 
                Managed Lustre client. Default is False.

        Returns:
            Client: Instance of the Client class representing the newly created Lustre client.

        Raises:
            SDKException: If the plan name is invalid or not found in the Commcell
            SDKException: If the client creation fails

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> 
            >>> # Initialize Commcell connection
            >>> commcell = Commcell('commserv.example.com', 'admin', 'password')
            >>> 
            >>> # Create a standard Lustre client
            >>> lustre_client = commcell.clients.add_lustre_client(
            ...     client_name="LustreFS01",
            ...     data_access_nodes=["AccessNode01", "AccessNode02"],
            ...     plan_name="LustreBackupPlan",
            ...     content=["/lustre/data", "/lustre/projects"]
            ... )
            >>> print(f"Created Lustre client: {lustre_client.client_name}")
            >>> 
            >>> # Create an Azure Managed Lustre client
            >>> azure_lustre = commcell.clients.add_lustre_client(
            ...     client_name="AzureLustreFS",
            ...     data_access_nodes=["AzureNode01"],
            ...     plan_name="AzureLustrePlan",
            ...     content=["/mnt/lustre"],
            ...     isAzureManagedLustre=True
            ... )
            >>> print(f"Created Azure Managed Lustre client: {azure_lustre.client_name}")

        Note:
            - Data access nodes must exist in the Commcell before creating the client
            - Content paths should be valid Lustre mount points
            - For Azure Managed Lustre, ensure Azure-specific configurations are in place
            - The method refreshes the clients list after successful creation
            - Uses client type 29 (Distributed Cluster) with cluster type 13 (Lustre)
            - Application ID 64 is used for Distributed Apps
        """

        content_temp = []
        for path in content:
            content_temp.append({"path": path})

        access_nodes = []
        for node in data_access_nodes:
            access_nodes.append({"clientName": node})

        if self._commcell_object.plans.has_plan(plan_name):
            plan_object = self._commcell_object.plans.get(plan_name)
            plan_id = int(plan_object.plan_id)
        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        request_json = {
            "createPseudoClientRequest": {
                "clientInfo": {
                    "clientType": 29,
                    "plan": {
                        "planName": plan_name,
                        "planId": plan_id
                    },
                    "distributedClusterInstanceProperties": {
                        "clusterType": 13,
                        "opType": 2,
                        "instance": {
                            "instanceId": 0,
                            "instanceName": client_name,
                            "clientName": client_name,
                            "applicationId": 64
                        },
                        "clusterConfig": {
                            "uxfsConfig": {}
                        },
                        "dataAccessNodes" : {
                            "dataAccessNodes" : access_nodes
                        }
                    },
                    "subclientInfo": {
                        "useLocalContent": True,
                        "contentOperationType": 1,
                        "fsSubClientProp": {},
                        "dfsSubclientProp": {
                            "useGPFSSnapshot": False
                        },
                        "content": content_temp
                    }
                },
                "entity": {
                    "clientName": client_name
                }
            }
        }

        if isAzureManagedLustre:
            request_json["createPseudoClientRequest"]["clientInfo"]["cloudFileShareWorkloadType"] = 6028
        
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_LUSTRE_CLIENT, payload=request_json
        )

        if flag and response:
            response_json = response.json()
            if 'response' in response_json:
                # errorCode is nested inside 'response' key
                error_code = response_json.get('response', {}).get('errorCode', 0)

                if error_code != 0:
                    error_string = response_json.get('response', {}).get('errorMessage', 'Unknown error')
                    o_str = 'Failed to create client\nError: "{0}"'.format(
                        error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    # initialize the clients again
                    # so the client object has all the clients
                    self.refresh()
                    return self.get(client_name)

            elif 'errorMessage' in response_json:
                error_string = response_json.get('errorMessage')
                o_str = 'Failed to create client\nError: "{0}"'.format(
                    error_string)

                raise SDKException('Client', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))
        
    def add_cassandra_client(
        self,
        new_client_name: str,
        gatewaynode: str,
        cql_port: int,
        config_file_path: str,
        plan_name: str,
        cql_username: Optional[str] = None,
        cql_password: Optional[str] = None,
        jmx_port: int = 7199,
        cql_credential_id: Optional[str] = None,
        jmx_credential_id: Optional[str] = None,
        keystore_credential_id: Optional[str] = None,
        truststore_credential_id: Optional[str] = None
    ):
        """Add a new Cassandra client to the Commcell environment.

        This method creates and registers a new Cassandra client using the provided configuration details,
        credentials, and plan. It supports both direct username/password authentication and credential IDs
        for secure access.

        Args:
            new_client_name: Name of the new Cassandra client to be created.
            gatewaynode: Hostname of the gateway node for Cassandra communication.
            cql_port: Port number for CQL connections.
            config_file_path: Path to the Cassandra configuration file.
            plan_name: Name of the plan to associate with the client.
            cql_username: Optional CQL username for authentication.
            cql_password: Optional CQL password for authentication.
            jmx_port: Port number for JMX connections (default: 7199).
            cql_credential_id: Optional credential ID for CQL authentication.
            jmx_credential_id: Optional credential ID for JMX authentication.
            keystore_credential_id: Optional credential ID for the keystore.
            truststore_credential_id: Optional credential ID for the truststore.

        Returns:
            The client object associated with the newly created Cassandra client.

        Raises:
            SDKException: If the plan is invalid, required credentials are missing, or client creation fails.

        Example:
            >>> clients = Clients(commcell_object)
            >>> cassandra_client = clients.add_cassandra_client(
            ...     new_client_name="CassandraNode01",
            ...     gatewaynode="gateway01.domain.com",
            ...     cql_port=9042,
            ...     config_file_path="/etc/cassandra/cassandra.yaml",
            ...     plan_name="CassandraBackupPlan",
            ...     cql_username="admin",
            ...     cql_password="securepassword"
            ... )
            >>> print(f"Created Cassandra client: {cassandra_client}")

        #ai-gen-doc
        """
        if self._commcell_object.plans.has_plan(plan_name):
            plan_object = self._commcell_object.plans.get(plan_name)
            plan_id = int(plan_object.plan_id)
            plan_type = int(plan_object.plan_type)
            plan_subtype = int(plan_object.subtype)
        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        if cql_username:
            cql_password = b64encode(cql_password.encode()).decode()
            jmx_port_int = int(jmx_port)
        cql_port_int = int(cql_port)
        cql_cred_id = int(cql_credential_id) if cql_credential_id else 0
        jmx_cred_id = int(jmx_credential_id) if jmx_credential_id else 0
        keystore_cred_id = int(keystore_credential_id) if keystore_credential_id else 0
        truststore_cred_id = int(truststore_credential_id) if truststore_credential_id else 0

        # Build base request

        gateway_node = {
            "clientNode": {"clientName": gatewaynode},
            "jmxConnection": {}
        }

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
                                "node": gateway_node,
                                "gatewayCQLPort": cql_port_int,
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

        # Add credentials

        cassandra_config = request_json["clientInfo"]["distributedClusterInstanceProperties"]["clusterConfig"]["cassandraConfig"]
        gateway = cassandra_config["gateway"]

        if cql_username:
            gateway["node"]["jmxConnection"]["port"] = jmx_port_int
            gateway["gatewayCQLUser"] = {
                "userName": cql_username,
                "password": cql_password,
                "confirmPassword": cql_password
            }
        else:
            if cql_cred_id:
                gateway["cqlCMCredInfo"] = {"credentialId": cql_cred_id}
            if jmx_cred_id:
                gateway["node"]["jmxConnection"]["jmxCMCredInfo"] = {"credentialId": jmx_cred_id}
            if keystore_cred_id:
                ssl_config = {
                    "useSSL": True,
                    "keyStoreCMCredInfo": {"credentialId": keystore_cred_id}
                }
                if truststore_cred_id:
                    ssl_config["trustStoreCMCredInfo"] = {"credentialId": truststore_cred_id}
                gateway.setdefault("node", {}).setdefault("authConfig", {})["sslConfig"] = ssl_config


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

    def add_cockroachdb_client(
        self,
        new_client_name: str,
        cockroachdb_host: str,
        cockroachdb_port: int,
        s3_service_host: str,
        s3_staging_path: str,
        accessnodes: List[str],
        plan_name: str,
        s3_credential_name: Optional[str] = None,
        db_username: Optional[str] = None,
        db_password: Optional[str] = None,
        sslcert: Optional[str] = None,
        sslkey: Optional[str] = None,
        sslrootcert: Optional[str] = None,
        s3_credential_id: Optional[str] = None,
        db_credential_id: Optional[str] = None,
        ssl_credential_id: Optional[str] = None
    ) -> Any:
        """Add a new CockroachDB client to the Commcell environment.

        This method provisions a CockroachDB pseudo client with the specified configuration,
        including database connection details, S3 staging information, access nodes, plan association,
        and optional credential and SSL settings.

        Args:
            new_client_name: Name for the new CockroachDB client.
            cockroachdb_host: Hostname or IP address of the CockroachDB server.
            cockroachdb_port: Port number for CockroachDB access.
            s3_service_host: Hostname of the S3 service for staging.
            s3_staging_path: Path on the S3 service for staging data.
            accessnodes: List of client names to be used as access nodes.
            plan_name: Name of the plan to associate with the new client.
            s3_credential_name: Optional AWS S3 credential name.
            db_username: Optional database username for authentication.
            db_password: Optional database password for authentication.
            sslcert: Optional path to the SSL certificate file.
            sslkey: Optional path to the SSL key file.
            sslrootcert: Optional path to the SSL root certificate file.
            s3_credential_id: Optional AWS S3 credential ID.
            db_credential_id: Optional database authentication credential ID.
            ssl_credential_id: Optional CockroachDB SSL credential ID.

        Returns:
            The client object associated with the newly created CockroachDB client.

        Raises:
            SDKException: If the plan is invalid, required credentials are missing, or client creation fails.

        Example:
            >>> access_nodes = ['node1', 'node2']
            >>> client_obj = clients.add_cockroachdb_client(
            ...     new_client_name='CockroachDB01',
            ...     cockroachdb_host='db.example.com',
            ...     cockroachdb_port=26257,
            ...     s3_service_host='s3.example.com',
            ...     s3_staging_path='/staging/path',
            ...     accessnodes=access_nodes,
            ...     plan_name='CockroachDBPlan',
            ...     db_username='admin',
            ...     db_password='securepassword',
            ...     sslcert='/path/to/cert.pem',
            ...     sslkey='/path/to/key.pem',
            ...     sslrootcert='/path/to/rootcert.pem'
            ... )
            >>> print(f"Created CockroachDB client: {client_obj}")

        #ai-gen-doc
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

        if db_username:
            db_password = b64encode(db_password.encode()).decode()

        cockroachdb_port = int(cockroachdb_port)
        s3_cred_id = int(s3_credential_id) if s3_credential_id else 0
        db_cred_id = int(db_credential_id) if db_credential_id else 0
        ssl_cred_id = int(ssl_credential_id) if ssl_credential_id else 0

        # Build base request

        cockroach_config = {
            "dbCredentials": {"credentialId": 0},
            "dbHost": cockroachdb_host,
            "port": cockroachdb_port,
            "staging": {
                "cloudURL": "s3.amazonaws.com",
                "instanceType": 5,
                "recordType": 102,
                "serviceHost": s3_service_host,
                "stagingPath": s3_staging_path,
                "stagingType": 1,
                "stagingCredentials": {}
            },
            "user": {"password": ""}
        }

        #Handle DB Credentials
        if db_username:
            cockroach_config["dbCredentials"]["credentialName"] = ""
            cockroach_config["user"]["userName"] = db_username
            cockroach_config["user"]["password"] = db_password
        elif db_cred_id:
            cockroach_config["dbCredentials"]["credentialId"] = db_cred_id
        else:
            raise SDKException('database', '102', 'Provide valid DB user name or db credential id')

        #Handle SSL
        if sslrootcert:
            cockroach_config["sslRootCert"] = sslrootcert
            cockroach_config["sslKey"] = sslkey
            cockroach_config["sslCert"] = sslcert
        elif ssl_cred_id:
            cockroach_config["sslCredentials"] = {"credentialId": ssl_cred_id}

        #Handle S3 credential
        if s3_credential_name:
            cockroach_config["staging"]["stagingCredentials"] = {
                "credentialName": s3_credential_name
            }
        elif s3_cred_id:
            cockroach_config["staging"]["stagingCredentials"] = {
                "credentialId": s3_cred_id
            }
        else:
            cockroach_config["staging"] = {
                    "cloudURL": "s3.amazonaws.com",
                    "instanceType": 5,
                    "recordType": 14,
                    "serviceHost": s3_service_host,
                    "stagingPath": s3_staging_path,
                    "stagingType": 1
                }

        # Final request JSON
        request_json = {
            "createPseudoClientRequest": {
                "clientInfo": {
                    "clientType": 29,
                    "distributedClusterInstanceProperties": {
                        "clusterConfig": {
                            "cockroachdbConfig": cockroach_config
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

    def add_mongodb_client(self,
                           new_client_name,
                           master_node,
                           master_hostname,
                           port,
                           os_user,
                           bin_path,
                           plan,
                           db_user = '',
                           db_password ='',
                           db_credential_id = None,
                           ssl_credential_id = None):

        """
                Adds new mongodb  client after client name and plan validation

                Args:
                    new_client_name     (str)   --  New pseudo client name
                    master_node         (str)   --  Master node name
                    master_hostname     (str)   --  Master Node's Host name
                    port                (int)   --  Mongodb Port on master node
                    os_user             (str)   --  MongoDB OS user used for impersonation
                    bin_path            (str)   --  Bin path for mongodb installation
                    plan                (str)   --  Plan associated with the new client
                    db_user             (str)   --  Db user if Authentication is Enabled on Cluster
                    db_password         (str)   --  Db Password  corresponding to db_user


                Returns:
                    client_object       (obj)   --  Client object associated with the new MongoDB client


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
        db_credential_id = int(db_credential_id)
        ssl_credential_id = int(ssl_credential_id)
        if self._commcell_object.clients.has_client(master_node):
            master_client_id = int(self._commcell_object.clients.all_clients[master_node.lower()]['id'])
        else:
            raise SDKException('Client', '102', 'Provide Valid Master Client')
        company_id = 0
        if (company_id == 0 ):
            company_name = "Commcell"
        else:
            company_name = ""
        request_json= {
            "clientInfo": {
                "clientType": "DISTRIBUTED_IDA",
                "distributedClusterInstanceProperties": {
                    "instance": {
                        "instanceId": 0,
                        "instanceName": new_client_name,
                        "applicationId": 64,
                        "clientName": new_client_name
                    },
                    "opType": 2,
                    "clusterType": "MONGODB",
                    "clusterConfig": {
                        "mdbConfig": {
                        "sslCMCredInfo": {
                            "credentialId": ssl_credential_id
                        },
                        "authCMCredInfo": {
                            "credentialId": db_credential_id
                        },
                            "masterNode": {
                                "client": {
                                    "clientId": master_client_id,
                                    "clientName": master_node
                                },
                                "hostName": master_hostname,
                                "portNumber": port,
                                "osUser": os_user,
                                "binPath": bin_path
                            }
                        }
                    }
                },
                "plan": {
                    "planId": plan_id,
                    "planName": plan,
                    "planType": plan_type,
                    "planSubtype": plan_subtype,
                    "entityInfo": {
                        "companyId": company_id,
                        "companyName": company_name,
                        "multiCommcellId": 0
                    }
                }
            },
            "entity": {
                "clientName": new_client_name
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._ADD_MONGODB_CLIENT, request_json)

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


    def add_azure_cosmosdb_client(
            self,
            client_name: str,
            access_nodes: List[str],
            credential_name: str,
            azure_options: Dict[str, Any]
        ) -> 'Client':
        """Add a new Azure Cosmos DB client to the Commcell environment.

        This method creates a pseudo client for Azure Cosmos DB using the provided client name,
        access nodes, credentials, and Azure-specific options. It validates the input parameters,
        encodes sensitive information, and sends a request to the Commcell server to create the client.

        Args:
            client_name: Name for the new Azure Cosmos DB client.
            access_nodes: List of access node names to associate with the client.
            credential_name: Name of the credential to use for authentication.
            azure_options: Dictionary containing Azure details. Example:
                {
                    "subscription_id": "your-subscription-id",
                    "tenant_id": "your-tenant-id",
                    "application_id": "your-application-id",
                    "password": "your-application-secret",
                    "credential_id": 12345
                }

        Returns:
            Client: Instance of the Client class representing the newly created Azure Cosmos DB client.

        Raises:
            SDKException: If any required Azure option is None, if a client with the same name already exists,
                if the client creation fails, or if the response from the server is invalid.

        Example:
            >>> azure_options = {
            ...     "subscription_id": "sub-id",
            ...     "tenant_id": "tenant-id",
            ...     "application_id": "app-id",
            ...     "password": "secret",
            ...     "credential_id": 12345
            ... }
            >>> access_nodes = ["AccessNode1", "AccessNode2"]
            >>> client = clients.add_azure_cosmosdb_client(
            ...     client_name="CosmosDBClient01",
            ...     access_nodes=access_nodes,
            ...     credential_name="AzureCreds",
            ...     azure_options=azure_options
            ... )
            >>> print(f"Created Cosmos DB client: {client}")

        #ai-gen-doc
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
        cloudAppInstanceInfo = {}
        emptyMemberServers = False

        if any(access_nodes):
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

        if azure_options.get("useHosted"):
            emptyMemberServers = True
            memberservers = []
            cloudAppInstanceInfo = {
                "generalCloudProperties": {
                    "regionEndPoints": azure_options.get("region")
                }
            }
        request_json = {
            "clientInfo": {
                "clientType": 12,
                "idaInfo": {
                },
                "virtualServerClientProperties": {
                    "allowEmptyMemberServers": emptyMemberServers,
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
                        "cloudAppInstanceInfoList": [cloudAppInstanceInfo
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

    def add_mongodb_atlas_client(self,client_name: str ,
                                 access_nodes: str,
                                 credential_name: str,
                                 description: str):
        """
        adds a new cloud account for mongodb atlas

        Args :

        client_name         :   str         # cloud Account Name
        access_nodes        :   List[str]   # Access Node to be associated with cloud account
        credential_name     :   str         # credentail to be associated with cloud account .
        description         :   str         # description for cloud account

        """
        request_json={
            "clientInfo": {
                "clientType": 15,
                "cloudClonnectorProperties": {
                    "instanceType": 40,
                    "instance": {
                        "cloudAppsInstance": {
                            "instanceType": 40,
                            "generalCloudProperties": {
                                "credentials": {
                                    "credentialId": 0,
                                    "credentialName": credential_name,
                                    "recordType": 23,
                                    "description": description,
                                    "selected": True
                                },
                                "accessNodes": {
                                    "memberServers": [
                                        {
                                            "client": {
                                                "clientId": 0,
                                                "clientName": access_nodes[0],
                                                "_type_": 3,
                                                "isClientGroup": False,
                                                "displayLabel": access_nodes[0],
                                                "typeLabel": "Access nodes",
                                                "selected": True
                                            }
                                        }
                                    ]
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

    def get(self, name: Union[str, int]) -> 'Client':
        """Retrieve a Client object by name, hostname, ID, or display name.

        This method searches for a client using the provided identifier, which can be a client name,
        host name, display name, or numeric ID. If a matching client is found, an instance of the
        Client class is returned.

        Args:
            name: The client identifier, which can be a string (name, hostname, display name)
                  or an integer (client ID).

        Returns:
            Client: Instance of the Client class corresponding to the specified identifier.

        Raises:
            SDKException: If the type of the name argument is not str or int.
            SDKException: If no client exists with the given name, hostname, display name, or ID.

        Example:
            >>> clients = Clients(commcell_object)
            >>> client_obj = clients.get('Server01')  # Search by client name
            >>> client_obj = clients.get('server01.domain.com')  # Search by hostname
            >>> client_obj = clients.get(12345)  # Search by client ID
            >>> print(f"Client found: {client_obj}")

        #ai-gen-doc
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

    def delete(self, client_name: str, forceDelete: bool = True):
        """Delete a client from the Commcell.

        Removes the specified client from the Commcell environment. If `forceDelete` is True,
        the client will be forcefully deleted, bypassing certain checks.

        Args:
            client_name: Name of the client to remove from the Commcell.
            forceDelete: If True, forcefully deletes the client. Defaults to True.

        Raises:
            SDKException:
                - If the type of `client_name` is not string.
                - If the client does not exist.
                - If the deletion fails due to an unsuccessful response.
                - If the response is empty or not successful.

        Example:
            >>> clients = Clients(commcell_object)
            >>> clients.delete("Server01")
            >>> # To force delete a client
            >>> clients.delete("Server02", forceDelete=True)

        #ai-gen-doc
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

    def retire(self, client_name: str) -> 'Job':
        """Retire the specified client from the Commcell environment.

        This method initiates the client retirement process, which uninstalls the client and removes it from active management.
        If successful, it returns a Job object representing the uninstall job.

        Args:
            client_name: The name of the client to retire (case-insensitive).

        Returns:
            Job: Job object representing the uninstall job for the retired client.

        Raises:
            SDKException: If the client retirement fails, the response is empty, or the response code is not as expected.

        Example:
            >>> clients = Clients(commcell_object)
            >>> job = clients.retire("Server01")
            >>> print(f"Retirement job started with Job ID: {job.job_id}")
            >>> # The returned Job object can be used to monitor the uninstall progress

        #ai-gen-doc
        """
        client_name = client_name.lower()
        if self.has_client(client_name):
            if client_name in self.all_clients:
                client_id = self.all_clients[client_name]['id']
            else:
                client_id = self.hidden_clients[client_name]['id']

            request_json = {
                "client": {
                    "clientId": int(client_id),
                    "clientName": client_name
                }
            }
            flag, response = self._cvpysdk_object.make_request(
                'DELETE', self._services['RETIRE'] % client_id, request_json
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
        else:
            raise SDKException(
                'Client', '102', 'No client exists with name: {0}'.format(client_name)
            )

    def refresh(self, **kwargs: Any) -> None:
        """Refresh the clients associated with the Commcell.

        This method reloads all client-related data, including hidden clients, virtualization clients,
        access nodes, and specialized client types. Optionally, it can refresh the client groups cache
        from MongoDB, with an option for a hard refresh.

        Args:
            **kwargs: Optional keyword arguments to control refresh behavior.
                mongodb (bool): If True, fetch client groups cache from MongoDB (default: False).
                hard (bool): If True, perform a hard refresh of the MongoDB cache for this entity (default: False).

        Example:
            >>> clients = Clients(commcell_object)
            >>> clients.refresh()  # Standard refresh of all client data
            >>> clients.refresh(mongodb=True)  # Refresh client groups cache from MongoDB
            >>> clients.refresh(mongodb=True, hard=True)  # Hard refresh of MongoDB cache

        #ai-gen-doc
        """
        self._clients = self._get_clients()
        self._hidden_clients = self._get_hidden_clients()
        self._virtualization_clients = self._get_virtualization_clients()
        self._virtualization_access_nodes = self._get_virtualization_access_nodes()
        self._office_365_clients = None
        self._file_server_clients = None
        self._salesforce_clients = None
        self._laptop_clients = None
        self._virtual_machines = None

        mongodb = kwargs.get('mongodb', False)
        hard = kwargs.get('hard', False)
        if mongodb:
            self._client_cache = self.get_clients_cache(hard=hard)

    def _get_infrastructure_clients(self) -> Dict[str, Dict[str, str]]:
        """Retrieve all infrastructure clients in the Commcell.
        
        This method scans through all clients in the Commcell cache and identifies those marked
        as infrastructure clients. Infrastructure clients are typically CommServ, WebConsole,
        WebServer, and other core Commvault infrastructure components.
        
        Returns:
            dict: Dictionary with infrastructure client names (lowercase) as keys and their details as values.
                  Each value contains client information including ID, hostname, and infrastructure flag.
        
        Example:
            >>> clients = Clients(commcell_object)
            >>> infra_clients = clients._get_infrastructure_clients()
            >>> for client_name, client_info in infra_clients.items():
            ...     print(f"Infrastructure client: {client_name}, ID: {client_info['id']}")
        
        #ai-gen-doc
        """
        all_clients = self.all_clients_cache
        infrastructure_clients = {}
        for client_name, client_info in all_clients.items():
            if client_info.get('isInfrastructure', False):              
                infrastructure_clients[client_name] = client_info
        
        return infrastructure_clients
    
    @property
    def infrastructure_clients(self) -> Dict[str, Dict[str, str]]:
        """Returns a dictionary containing information of all infrastructure clients in the Commcell.
        
        This property provides access to all infrastructure clients such as CommServ, WebConsole,
        WebServer, and other core Commvault components. The data is cached after the first access
        for improved performance.
        
        Returns:
            dict: Dictionary with infrastructure client names (lowercase) as keys and their details as values.
                  Each value contains client information including:
                  - 'id': Client ID
                  - 'hostName': Hostname of the client
                  - 'isInfrastructure': Boolean flag (always True for this property)
                  - Additional client metadata
        
        Example:
            >>> clients = Clients(commcell_object)
            >>> infra_clients = clients.infrastructure_clients
            >>> print(f"Total infrastructure clients: {len(infra_clients)}")
        
        #ai-gen-doc
        """
        if not self._infra_clients:
            self._infra_clients = self._get_infrastructure_clients()
        return self._infra_clients

class Client(object):
    """
    Comprehensive class for managing and performing operations on a specific client within a CommCell environment.

    The Client class provides a rich interface for interacting with client entities, enabling configuration,
    management, monitoring, and operational control. It supports a wide range of functionalities including
    property management, backup and restore operations, service control, network configuration, user and owner
    associations, software management, and advanced settings.

    Key Features:
        - Client property access and updates via properties and update methods
        - Backup, restore, data aging, IntelliSnap, and content indexing enable/disable operations
        - Service management: start, stop, restart individual or all services
        - Network configuration, throttling, and status monitoring
        - File and folder upload capabilities to the client
        - Execution of scripts and commands on the client with authentication support
        - Management of client owners, user associations, and client groups
        - Software operations: push service packs/hotfixes, repair, uninstall, reconfigure, retire
        - License management and release
        - Advanced settings: encryption, deduplication, additional settings management
        - Privacy and security role management
        - Environment, readiness, and needs attention details retrieval
        - Log file reading and job results directory management
        - Support for virtual machine clients and cluster configurations
        - Company and migration operations for client entities

    This class is designed to be instantiated with CommCell context and client credentials, providing
    both high-level and granular control over client operations and configurations.

    #ai-gen-doc
    """

    def __new__(cls, commcell_object: 'Commcell', client_name: str, client_id: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None) -> object:
        """Create and return the appropriate client object based on client properties.

        This method determines the type of client (e.g., VMClient, OneDriveClient, or generic Client)
        to instantiate based on the provided Commcell object and client details.

        Args:
            commcell_object: Instance of the Commcell class representing the Commcell connection.
            client_name: Name of the client as a string.
            client_id: Optional client ID as a string. Defaults to None.
            username: Optional username for authentication. Defaults to None.
            password: Optional password for authentication. Defaults to None.

        Returns:
            An instance of the appropriate client class (VMClient, OneDriveClient, or Client).

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> client = Client(commcell, "Client01", client_id="12345")
            >>> print(type(client))
            >>> # The returned object may be a VMClient, OneDriveClient, or Client depending on client properties

        #ai-gen-doc
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

    def __init__(self, commcell_object: 'Commcell', client_name: str, client_id: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """Initialize a Client instance for managing backup and restore operations.

        Args:
            commcell_object: Instance of the Commcell class representing the Commcell connection.
            client_name: Name of the client as a string.
            client_id: Optional client ID as a string. If not provided, it will be determined automatically.
            username: Optional username for client authentication.
            password: Optional password for client authentication.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> client = Client(commcell, "Server01")
            >>> print(f"Initialized client: {client}")

        #ai-gen-doc
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
        self._SECURITY_ASSOCIATION = self._services['SECURITY_ASSOCIATION']

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
        self._additional_settings = None
        self.refresh()

    def __repr__(self) -> str:
        """Return a string representation of the Client instance.

        This method provides a human-readable description of the Client object,
        including the client name for easier identification during debugging or logging.

        Returns:
            A string describing the Client instance and its associated client name.

        Example:
            >>> client = Client(...)
            >>> print(repr(client))
            Client class instance for Client: "MyClient"
        #ai-gen-doc
        """
        representation_string = 'Client class instance for Client: "{0}"'
        return representation_string.format(self.client_name)

    def _get_client_id(self) -> str:
        """Retrieve the client ID associated with this Client instance.

        Returns:
            The unique client ID as a string.

        Example:
            >>> client = Client(commcell_object, client_name)
            >>> client_id = client._get_client_id()
            >>> print(f"Client ID: {client_id}")

        #ai-gen-doc
        """
        return self._commcell_object.clients.get(self.client_name).client_id

    def _get_client_properties(self) -> Dict[str, Any]:
        """Retrieve and update the properties of this client from the Commcell.

        This method fetches the client properties from the Commcell server and updates
        the internal state of the Client object with the latest configuration, activity,
        and infrastructure details.

        Returns:
            Dictionary containing the properties of this client, such as OS information,
            activity controls, infrastructure details, and other metadata.

        Raises:
            SDKException: If the response from the Commcell server is empty or indicates failure.

        Example:
            >>> client = Client(commcell_object, client_name)
            >>> properties = client._get_client_properties()
            >>> print(properties)
            >>> # Access specific property values
            >>> os_info = properties['client']['osInfo']
            >>> print(f"Client OS: {os_info}")

        #ai-gen-doc
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

    def _request_json(
        self,
        option: str,
        enable: bool = True,
        enable_time: Optional[int] = None,
        job_start_time: Optional[int] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Construct the JSON request payload for client activity control operations.

        This method generates the appropriate JSON structure to be sent to the API based on the selected option
        (e.g., Backup, Restore, Data Aging) and additional parameters. It supports enabling/disabling activities
        immediately or after a specified delay, and allows customization of timezone and job start time.

        Args:
            option: The activity option for which to generate the API request (e.g., "Backup", "Restore", "Data Aging").
            enable: Whether to enable the specified activity type immediately. Defaults to True.
            enable_time: Optional epoch time (int) to enable the activity after a delay. If provided, the request will include a delayed enable configuration.
            job_start_time: Optional epoch time (int) specifying when the job should start. If provided, it is added to the request.
            **kwargs: Additional keyword arguments. Supported keys:
                - timezone (str): Timezone name to use for the operation. If not provided, defaults to the Commcell's default timezone.

        Returns:
            Dictionary representing the JSON request payload to be sent to the API.

        Example:
            >>> # Enable backup activity immediately
            >>> payload = client._request_json("Backup", enable=True)
            >>> print(payload)
            >>>
            >>> # Schedule restore activity to enable after a delay in a specific timezone
            >>> payload = client._request_json(
            ...     "Restore",
            ...     enable=False,
            ...     enable_time=1680307200,
            ...     timezone="GMT"
            ... )
            >>> print(payload)
            >>>
            >>> # Set job start time for data aging activity
            >>> payload = client._request_json(
            ...     "Data Aging",
            ...     job_start_time=1680310800
            ... )
            >>> print(payload)

        #ai-gen-doc
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

    def _update_client_props_json(self, properties_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Construct the JSON request for updating client properties via the API.

        Args:
            properties_dict: Dictionary containing client properties to update.
                Example:
                    {
                        "EnableSnapBackups": True
                    }

        Returns:
            Dictionary representing the client properties update request in the required API format.

        Example:
            >>> client = Client(...)
            >>> update_dict = {"EnableSnapBackups": True}
            >>> request_json = client._update_client_props_json(update_dict)
            >>> print(request_json)
            # Output will be a JSON-ready dictionary for the API request

        #ai-gen-doc
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
                      upload_url: str,
                      file_contents: str,
                      headers: str,
                      request_id: Optional[int] = None,
                      chunk_offset: Optional[int] = None) -> Tuple[int, int]:
        """Send a request to upload file contents to the client machine.

        This method uploads the specified file data to the server using the provided URL and headers.
        It supports chunked uploads by accepting a request ID and chunk offset, which are used to
        uniquely identify and position data chunks.

        Args:
            upload_url: The request URL to which the file contents will be uploaded.
            file_contents: The data from the file to be copied, as a string.
            headers: Request headers for the API call.
            request_id: Optional request ID from a previous upload, used to identify data chunks.
            chunk_offset: Optional number of bytes written in previous upload requests, used to specify
                the starting position for writing data.

        Returns:
            A tuple containing:
                - request_id (int): The request ID returned from the server response.
                - chunk_offset (int): The chunk offset returned from the server response.

        Raises:
            SDKException: If the upload fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(...)
            >>> upload_url = "http://server/upload"
            >>> file_contents = "file data here"
            >>> headers = "Authorization: Bearer <token>"
            >>> request_id, chunk_offset = client._make_request(upload_url, file_contents, headers)
            >>> print(f"Upload successful. Request ID: {request_id}, Chunk Offset: {chunk_offset}")

        #ai-gen-doc
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

    def _get_instance_of_client(self) -> str:
        """Retrieve the instance name associated with this client.

        This method determines the instance on which the client is installed, based on the client's operating system.
        For Windows clients, it reads the instance information from the QinetixVM file.
        For Unix clients, it extracts the instance name from the galaxy_vm file.

        Returns:
            The name of the instance as a string (e.g., "Instance001").

        Raises:
            SDKException: If the instance value cannot be retrieved or if the operation is not supported for the client OS.

        Example:
            >>> client = Client(...)
            >>> instance_name = client._get_instance_of_client()
            >>> print(f"Client is installed on instance: {instance_name}")

        #ai-gen-doc
        """
        if 'windows' in self.os_info.lower():
            command = 'powershell.exe Get-Content "{0}"'.format(
                os.path.join(self.install_directory.replace(' ', '` '), 'Base', 'QinetixVM')
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

    def _get_log_directory(self) -> str:
        """Retrieve the path of the log directory on the client.

        This method determines the log directory path based on the client's operating system.
        For Windows clients, it queries the registry for the log directory location.
        For Unix clients, it reads the appropriate properties file to obtain the path.

        Returns:
            The path to the log directory on the client as a string.
            Example values:
                - "..\\ContentStore\\Log Files" (Windows)
                - "../commvault/Log_Files" (Unix)

        Raises:
            SDKException: If unable to retrieve the log directory path or if the operation
                is not supported for the client's operating system.

        Example:
            >>> client = Client(...)
            >>> log_dir = client._get_log_directory()
            >>> print(f"Client log directory: {log_dir}")
            >>> # Use the returned path for log file operations

        #ai-gen-doc
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

    def _service_operations(self, service_name: Optional[str] = None, operation: Optional[str] = None) -> None:
        """Execute a command on the client machine to start, stop, or restart a Commvault service or all services.

        This method performs the specified operation (START, STOP, RESTART, or RESTART_SVC_GRP) on a given service
        or all services on the client. If no operation is provided, it defaults to RESTART_SVC_GRP. The method
        automatically determines the appropriate command based on the client's operating system.

        Args:
            service_name: Name of the service to operate on. If None, operates on all services.
            operation: Operation to perform. Valid values are 'START', 'STOP', 'RESTART', and 'RESTART_SVC_GRP'.
                If None, defaults to 'RESTART_SVC_GRP'.

        Raises:
            SDKException: If an invalid operation is specified, the client OS is unsupported, or the command fails.

        Example:
            >>> client = Client(...)
            >>> # Restart all services on the client
            >>> client._service_operations()
            >>> # Start a specific service
            >>> client._service_operations(service_name="GxEvMgrS", operation="START")
            >>> # Stop all services
            >>> client._service_operations(operation="STOP")
        #ai-gen-doc
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

    def _set_patch_options(self, option_type: int, enable: bool = True) -> None:
        """Set patch management options for this Client.

        This method enables or disables patch management options (e.g., Windows OS updates).

        Args:
            option_type: The type of patch option to set (e.g., 2 for Windows OS updates).
            enable: True to enable the patch option, False to disable. Default: True.

        Raises:
            SDKException: If the request fails or the response indicates an error.

        Example:
            >>> client = Client(...)
            >>> # Enable Windows OS updates
            >>> client._set_patch_options(option_type=2, enable=True)
            >>> # Enable Microsoft SQL Server updates
            >>> client._set_patch_options(option_type=1, enable=True)
        #ai-gen-doc
        """
        request_json = {
            "clientID": int(self.client_id),
            "optionType": option_type,
            "value": enable
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._services['SET_PATCH_OPTIONS'], request_json)

        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException(
                        'Response', '101',
                        self._commcell_object._update_response_(response.text)
                    )
                return
            raise SDKException('Response', '102')
        raise SDKException(
            'Response', '101', self._commcell_object._update_response_(response.text))

    def _process_update_request(self, request_json: Dict[str, Any]) -> None:
        """Run the Client update API with the provided request payload.

        This method sends a client update request to the Commcell server using the specified
        request JSON payload. It validates the response and raises an SDKException if the update
        fails or if the response is empty.

        Args:
            request_json: Dictionary containing the request payload for the client update API.

        Raises:
            SDKException: If the response is empty or the update operation is not successful.

        Example:
            >>> client = Client(commcell_object, client_name)
            >>> update_payload = {
            ...     "association": {
            ...         "entity": [
            ...             {"clientName": "MyClient"}
            ...         ]
            ...     },
            ...     "properties": {
            ...         # Additional update properties
            ...     }
            ... }
            >>> client._process_update_request(update_payload)
            >>> # If the update fails, an SDKException will be raised

        #ai-gen-doc
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

    def update_properties(self, properties_dict: Dict[str, Any]) -> None:
        """Update the properties of the client.

        This method updates the client configuration using the provided properties dictionary.
        To modify client properties, obtain a deep copy of the current properties using `self.properties`,
        make the necessary changes, and then pass the updated dictionary to this method.

        Args:
            properties_dict: Dictionary containing the client properties to be updated.

        Raises:
            SDKException: If the update fails, the response is empty, or the response code is not as expected.

        Example:
            >>> client = Client(...)
            >>> props = client.properties.copy()  # Get a deep copy of current properties
            >>> props['clientProps']['clientName'] = "NewClientName"
            >>> client.update_properties(props)
            >>> print("Client properties updated successfully")

        #ai-gen-doc
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
        if "CVS3BucketName" in request_json.get("clientProperties", {}).get("clientProps", {}) \
                and request_json.get("clientProperties", {}).get("clientProps", {}).get("CVS3BucketName") == "":
            request_json['clientProperties']['clientProps'].pop("CVS3BucketName")

        self._process_update_request(request_json)

    @property
    def properties(self) -> Dict[str, Any]:
        """Get a copy of the client properties.

        Returns:
            Dictionary containing all properties associated with the client.

        Example:
            >>> client = Client(...)
            >>> props = client.properties  # Use dot notation for properties
            >>> print(f"Client properties: {props}")
            >>> # The returned dictionary contains key-value pairs for client configuration

        #ai-gen-doc
        """
        return copy.deepcopy(self._properties)

    @property
    def latitude(self) -> float:
        """Get the latitude of the client from the clientRegionInfo GeoLocation.

        Returns:
            The latitude value as a float.

        Example:
            >>> client = Client(...)
            >>> lat = client.latitude  # Use dot notation for property access
            >>> print(f"Client latitude: {lat}")

        #ai-gen-doc
        """
        return self._client_latitude

    @property
    def longitude(self) -> float:
        """Get the longitude value of the client from the clientRegionInfo GeoLocation.

        Returns:
            The longitude of the client as a float.

        Example:
            >>> client = Client(...)
            >>> longitude = client.longitude  # Use dot notation for property access
            >>> print(f"Client longitude: {longitude}")

        #ai-gen-doc
        """
        return self._client_longitude

    @property
    def is_vm(self) -> bool:
        """Indicate whether the client is a virtual machine (VM).

        Returns:
            True if the client is a VM, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_vm:
            ...     print("This client is a virtual machine.")
            ... else:
            ...     print("This client is a physical machine.")

        #ai-gen-doc
        """
        return self._is_vm

    @property
    def hyperv_id_of_vm(self) -> str:
        """Get the Hypervisor ID associated with this VM client.

        Returns:
            The Hypervisor ID as a string.

        Example:
            >>> client = Client(...)
            >>> hypervisor_id = client.hyperv_id_of_vm  # Use dot notation for property access
            >>> print(f"VM Hypervisor ID: {hypervisor_id}")

        #ai-gen-doc
        """
        return self._vm_hyperv_id

    @property
    def associated_client_groups(self) -> List[str]:
        """Get the list of client groups associated with this client.

        Returns:
            List of client group names as strings to which the client is associated.

        Example:
            >>> client = Client(...)
            >>> groups = client.associated_client_groups  # Use dot notation for property access
            >>> print(f"Client is part of groups: {groups}")
            >>> # The returned list contains the names of all associated client groups

        #ai-gen-doc
        """
        return self._associated_client_groups

    @property
    def company_id(self) -> int:
        """Get the company ID associated with this client.

        Returns:
            The company ID as an integer.

        Example:
            >>> client = Client(...)
            >>> company_id = client.company_id  # Use dot notation for property access
            >>> print(f"Client's company ID: {company_id}")

        #ai-gen-doc
        """
        return self._company_id

    @property
    def name(self) -> str:
        """Get the name of the client.

        Returns:
            The client name as a string.

        Example:
            >>> client = Client(...)
            >>> client_name = client.name  # Use dot notation for properties
            >>> print(f"Client name: {client_name}")

        #ai-gen-doc
        """
        return self._properties['client']['clientEntity']['clientName']

    @property
    def display_name(self) -> str:
        """Get the display name of the client.

        Returns:
            The display name of the client as a string.

        Example:
            >>> client = Client(...)
            >>> name = client.display_name  # Use dot notation for property access
            >>> print(f"Client display name: {name}")

        #ai-gen-doc
        """
        return self._properties['client']['displayName']

    @display_name.setter
    def display_name(self, display_name: str) -> None:
        """Set the display name for the client.

        Args:
            display_name: The new display name to assign to the client.

        Example:
            >>> client = Client(...)
            >>> client.display_name = "ProductionServer01"  # Use assignment for property setters
            >>> # The client's display name is now updated to "ProductionServer01"
        #ai-gen-doc
        """
        update_properties = self.properties
        update_properties['client']['displayName'] = display_name
        self.update_properties(update_properties)

    @property
    def description(self) -> Optional[str]:
        """Get the description of the client.

        Returns:
            The client description as a string, or None if not set.

        Example:
            >>> client = Client(...)
            >>> desc = client.description  # Use dot notation for property access
            >>> print(f"Client description: {desc}")

        #ai-gen-doc
        """
        return self._properties.get('client', {}).get('clientDescription')

    @description.setter
    def description(self, description: str) -> None:
        """Set the display name (description) for the client.

        Args:
            description: The description string to assign to the client.

        Example:
            >>> client = Client(...)
            >>> client.description = "Production Database Server"  # Use assignment for property setter
            >>> # The client's display name is now updated

        #ai-gen-doc
        """
        update_description = {
            "client": {
                "clientDescription": description
            }
        }
        self.update_properties(update_description)

    @property
    def timezone(self) -> str:
        """Get the timezone setting of the client.

        Returns:
            The timezone of the client as a string.

        Example:
            >>> client = Client(...)
            >>> tz = client.timezone  # Use dot notation for property access
            >>> print(f"Client timezone: {tz}")

        #ai-gen-doc
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone: Optional[str] = None) -> None:
        """Set the timezone for the client.

        Args:
            timezone: The timezone name to assign to the client as a string.
                Refer to the TIMEZONES dictionary in constants.py for valid timezone values.

        Example:
            >>> client = Client(...)
            >>> client.timezone = "Asia/Kolkata"  # Set the client's timezone
            >>> # Ensure the timezone string matches a key in the TIMEZONES dict

        #ai-gen-doc
        """
        update_properties = self.properties
        update_properties['client']['TimeZone']['TimeZoneName'] = timezone
        update_properties['client']['timezoneSetByUser'] = True
        self.update_properties(update_properties)

    @property
    def commcell_name(self) -> str:
        """Get the name of the Commcell associated with this Client.

        Returns:
            The Commcell name as a string.

        Example:
            >>> client = Client(...)
            >>> name = client.commcell_name  # Use dot notation for property access
            >>> print(f"Commcell name: {name}")
        #ai-gen-doc
        """
        return self._properties['client']['clientEntity']['commCellName']

    @property
    def name_change(self) -> 'NameChange':
        """Get the NameChange instance associated with this Client.

        Returns:
            NameChange: An object for managing client name changes.

        Example:
            >>> client = Client(...)
            >>> name_change_obj = client.name_change  # Use dot notation for property access
            >>> print(f"NameChange object: {name_change_obj}")
            >>> # The returned NameChange object can be used to perform name change operations

        #ai-gen-doc
        """
        return NameChange(self)

    @property
    def _security_association(self) -> 'SecurityAssociation':
        """Get the SecurityAssociation object associated with this Client.

        Returns:
            SecurityAssociation: An object for managing security associations of the client.

        Example:
            >>> client = Client(commcell_object, "ClientName")
            >>> security_assoc = client._security_association  # Use dot notation for property access
            >>> print(f"Security association object: {security_assoc}")
            >>> # The returned SecurityAssociation object can be used for security operations

        #ai-gen-doc
        """
        if self._association_object is None:
            from .security.security_association import SecurityAssociation
            self._association_object = SecurityAssociation(self._commcell_object, self)

        return self._association_object

    @property
    def available_security_roles(self) -> str:
        """Get the list of available security roles for the client as a string.

        Returns:
            A string representation of the client's available security roles.

        Example:
            >>> client = Client(...)
            >>> roles = client.available_security_roles  # Use dot notation for properties
            >>> print(f"Available security roles: {roles}")
            >>> # The returned string lists all roles associated with the client

        #ai-gen-doc
        """
        return self._security_association.__str__()

    @property
    def client_id(self) -> str:
        """Get the unique identifier for this client as a read-only property.

        Returns:
            The client ID as a string.

        Example:
            >>> client = Client(...)
            >>> print(client.client_id)  # Access the client ID using dot notation
            >>> # The client_id property is read-only and cannot be modified directly

        #ai-gen-doc
        """
        return self._client_id

    @property
    def client_name(self) -> str:
        """Get the name of the client as a read-only property.

        Returns:
            The client name as a string.

        Example:
            >>> client = Client(...)
            >>> name = client.client_name  # Access the client name property
            >>> print(f"Client name: {name}")
        #ai-gen-doc
        """
        return self._client_name

    @property
    def client_hostname(self) -> str:
        """Get the host name of the client as a read-only property.

        Returns:
            The client host name as a string.

        Example:
            >>> client = Client(...)
            >>> hostname = client.client_hostname  # Access via property
            >>> print(f"Client host name: {hostname}")
        #ai-gen-doc
        """
        return self._client_hostname

    @property
    def os_info(self) -> str:
        """Get the operating system information for the client as a read-only property.

        Returns:
            Dictionary containing details about the client's operating system, such as name, version, and architecture.

        Example:
            >>> client = Client(...)
            >>> os_details = client.os_info  # Access as a property
            >>> print(f"OS Name: {os_details}")
        #ai-gen-doc
        """
        return self._os_info

    @property
    def os_type(self) -> 'OSType':
        """Get the operating system type of the client as a read-only property.

        Returns:
            OSType: The operating system type, such as OSType.WINDOWS or OSType.UNIX.

        Example:
            >>> client = Client(...)
            >>> os_type = client.os_type  # Use dot notation for property access
            >>> print(f"Client OS type: {os_type.name}")
            >>> # The returned OSType object can be used for OS-specific logic

        #ai-gen-doc
        """
        os_type = OSType.WINDOWS if OSType.WINDOWS.name.lower() in self.os_info.lower() else OSType.UNIX
        return os_type

    @property
    def is_data_recovery_enabled(self) -> bool:
        """Indicate whether data recovery is enabled for this client.

        Returns:
            True if data recovery is enabled; False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_data_recovery_enabled:
            ...     print("Data recovery is enabled for this client.")
            ... else:
            ...     print("Data recovery is not enabled for this client.")

        #ai-gen-doc
        """
        return self._is_data_recovery_enabled

    @property
    def is_data_management_enabled(self) -> bool:
        """Indicate whether data management is enabled for this client.

        Returns:
            True if data management is enabled; False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_data_management_enabled:
            ...     print("Data management is enabled for this client.")
            ... else:
            ...     print("Data management is not enabled.")

        #ai-gen-doc
        """
        return self._is_data_management_enabled

    @property
    def is_ci_enabled(self) -> bool:
        """Indicate whether online content indexing is enabled for the client.

        Returns:
            True if online content indexing is enabled; False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_ci_enabled:
            ...     print("Online content indexing is enabled for this client.")
            ... else:
            ...     print("Online content indexing is not enabled.")

        #ai-gen-doc
        """
        return self._is_ci_enabled

    @property
    def is_backup_enabled(self) -> bool:
        """Indicate whether backup is enabled for this client.

        Returns:
            True if backup is enabled for the client, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_backup_enabled:
            ...     print("Backup is enabled for this client.")
            ... else:
            ...     print("Backup is disabled for this client.")

        #ai-gen-doc
        """
        return self._is_backup_enabled

    @property
    def is_restore_enabled(self) -> bool:
        """Indicate whether restore operations are enabled for this client.

        Returns:
            True if restore operations are enabled; False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_restore_enabled:
            ...     print("Restore is enabled for this client.")
            ... else:
            ...     print("Restore is disabled for this client.")

        #ai-gen-doc
        """
        return self._is_restore_enabled

    @property
    def is_data_aging_enabled(self) -> bool:
        """Indicate whether data aging is enabled for this client.

        Returns:
            True if data aging is enabled; False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_data_aging_enabled:
            ...     print("Data aging is enabled for this client.")
            ... else:
            ...     print("Data aging is not enabled for this client.")

        #ai-gen-doc
        """
        return self._is_data_aging_enabled

    @property
    def is_intelli_snap_enabled(self) -> bool:
        """Indicate whether IntelliSnap is enabled for this client.

        Returns:
            True if IntelliSnap is enabled for the client, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_intelli_snap_enabled:
            ...     print("IntelliSnap is enabled for this client.")
            ... else:
            ...     print("IntelliSnap is not enabled.")

        #ai-gen-doc
        """
        return self._is_intelli_snap_enabled

    @property
    def is_privacy_enabled(self) -> bool:
        """Indicate whether privacy is enabled for this client.

        Returns:
            True if client privacy is enabled, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_privacy_enabled:
            ...     print("Privacy is enabled for this client.")
            ... else:
            ...     print("Privacy is not enabled for this client.")

        #ai-gen-doc
        """
        return self._is_privacy_enabled

    @property
    def is_deleted_client(self) -> bool:
        """Indicate whether the client has been deleted.

        Returns:
            True if the client is deleted, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_deleted_client:
            ...     print("Client has been deleted.")
            ... else:
            ...     print("Client is active.")

        #ai-gen-doc
        """
        return self._is_deleted_client

    @property
    def is_infrastructure(self) -> bool:
        """Indicate whether this client is classified as an infrastructure client.

        Returns:
            True if the client is an infrastructure client, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_infrastructure:
            ...     print("This is an infrastructure client.")
            ... else:
            ...     print("This is a regular client.")

        #ai-gen-doc
        """
        return self._is_infrastructure

    @property
    def update_status(self) -> int:
        """Get the update status flag of the client.

        Returns:
            Integer value representing the update status of the client.

        Example:
            >>> client = Client(...)
            >>> status = client.update_status  # Use dot notation for property access
            >>> print(f"Client update status: {status}")
            >>> # The returned status can be used to determine if updates are pending or completed

        #ai-gen-doc
        """
        return self._update_status

    @property
    def is_command_center(self) -> bool:
        """Indicate whether the client has the Command Center package installed.

        Returns:
            True if the Command Center package is installed on the client, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_command_center:
            ...     print("Command Center package is installed.")
            ... else:
            ...     print("Command Center package is not installed.")

        #ai-gen-doc
        """
        return self._is_command_center

    @property
    def is_web_server(self) -> bool:
        """Check if the client has the web server package installed.

        Returns:
            True if the web server package is installed on the client, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_web_server:
            ...     print("Web server package is installed.")
            ... else:
            ...     print("Web server package is not installed.")

        #ai-gen-doc
        """
        return self._is_web_server

    @property
    def install_directory(self) -> str:
        """Get the installation directory of the client as a read-only property.

        Returns:
            The path to the installation directory as a string.

        Example:
            >>> client = Client(...)
            >>> install_path = client.install_directory  # Use dot notation for property access
            >>> print(f"Client is installed at: {install_path}")
        #ai-gen-doc
        """
        return self._install_directory

    @property
    def version(self) -> str:
        """Get the version of the client as a read-only property.

        Returns:
            The version string representing the client's software version.

        Example:
            >>> client = Client(...)
            >>> print(client.version)  # Access the version property
            >>> # Output: '11.28.20' (example version string)
        #ai-gen-doc
        """
        return self._version

    @property
    def service_pack(self) -> str:
        """Get the service pack version installed on the client.

        This property provides read-only access to the service pack information for the client.

        Returns:
            The service pack version as a string.

        Example:
            >>> client = Client(...)
            >>> sp_version = client.service_pack  # Use dot notation for property access
            >>> print(f"Service Pack: {sp_version}")

        #ai-gen-doc
        """
        return self._service_pack

    @property
    def owners(self) -> List[str]:
        """Get the list of owners associated with this client as a read-only property.

        Returns:
            List of owner names as strings.

        Example:
            >>> client = Client(...)
            >>> owner_list = client.owners  # Use dot notation for property access
            >>> print(f"Client owners: {owner_list}")
            >>> # The returned list contains all owners assigned to the client

        #ai-gen-doc
        """
        return self._client_owners

    @property
    def job_results_directory(self) -> str:
        """Get the job results directory for the client as a read-only property.

        Returns:
            The path to the job results directory as a string.

        Example:
            >>> client = Client(...)
            >>> results_dir = client.job_results_directory  # Use dot notation for properties
            >>> print(f"Job results directory: {results_dir}")
            >>> # The returned string can be used to access job result files

        #ai-gen-doc
        """
        return self._job_results_directory

    @property
    def block_level_cache_dir(self) -> str:
        """Get the block-level cache directory path for the client.

        Returns:
            The path to the block-level cache directory as a string.

        Example:
            >>> client = Client(...)
            >>> cache_dir = client.block_level_cache_dir  # Use dot notation for property access
            >>> print(f"Block-level cache directory: {cache_dir}")

        #ai-gen-doc
        """
        return self._block_level_cache_dir

    @property
    def instance(self) -> Any:
        """Get the instance information for the client.

        This property retrieves the value of the instance on which the client is installed.
        If the instance information is not already cached, it attempts to fetch it.

        Returns:
            The instance object or value associated with the client. The type may vary depending on implementation.

        Example:
            >>> client = Client(...)
            >>> instance_info = client.instance  # Use dot notation for property access
            >>> print(f"Client instance: {instance_info}")

        #ai-gen-doc
        """
        if self._instance is None:
            try:
                self._instance = self._get_instance_of_client()
            except SDKException:
                # pass silently if failed to get the value of instance
                pass

        return self._instance

    @property
    def log_directory(self) -> Optional[str]:
        """Get the path of the log directory on the client.

        Returns:
            The log directory path as a string, or None if unavailable.

        Example:
            >>> client = Client(...)
            >>> log_dir = client.log_directory  # Use dot notation for property access
            >>> print(f"Client log directory: {log_dir}")
            >>> # The returned value may be None if the log directory cannot be determined

        #ai-gen-doc
        """
        if self._log_directory is None:
            try:
                self._log_directory = self._get_log_directory()
            except SDKException:
                # pass silently if failed to get the value of the log directory
                pass

        return self._log_directory

    @property
    def agents(self) -> 'Agents':
        """Get the Agents instance representing all agents installed or configured on this Client.

        Returns:
            Agents: An object for managing and accessing agent details for the client.

        Example:
            >>> client = Client(...)
            >>> agents = client.agents  # Use dot notation for property access
            >>> print(f"Total agents installed: {len(agents)}")
            >>> # The returned Agents object can be used to list, add, or manage agents

        #ai-gen-doc
        """
        if self._agents is None:
            self._agents = Agents(self)

        return self._agents

    @property
    def schedules(self) -> 'Schedules':
        """Get the Schedules instance configured for this Client.

        Returns:
            Schedules: An object representing all schedules associated with the client.

        Example:
            >>> client = Client(...)
            >>> schedules = client.schedules  # Access schedules property
            >>> print(f"Schedules object: {schedules}")
            >>> # The returned Schedules object can be used to manage client schedules

        #ai-gen-doc
        """
        if self._schedules is None:
            self._schedules = Schedules(self)

        return self._schedules

    @property
    def users(self) -> 'Users':
        """Get the Users instance representing users with permissions on this Client.

        Returns:
            Users: An object for managing and accessing users assigned to the client.

        Example:
            >>> client = Client(commcell_object, client_name)
            >>> users = client.users  # Use dot notation for property access
            >>> print(f"Total users with permissions: {len(users)}")
            >>> # The returned Users object can be used to manage user permissions

        #ai-gen-doc
        """
        if self._users is None:
            self._users = Users(self._commcell_object)

        return self._users

    @property
    def network(self) -> 'Network':
        """Get the Network object associated with this Client.

        Returns:
            Network: An instance for managing network-related operations of the client.

        Example:
            >>> client = Client(...)
            >>> network_obj = client.network  # Use dot notation for property access
            >>> print(f"Network object: {network_obj}")
            >>> # The returned Network object can be used for network configuration and management

        #ai-gen-doc
        """
        if self._network is None:
            self._network = Network(self)

        return self._network

    @property
    def network_throttle(self) -> 'NetworkThrottle':
        """Get the NetworkThrottle object associated with this Client.

        Returns:
            NetworkThrottle: An instance for managing network throttling settings for the client.

        Example:
            >>> client = Client(...)
            >>> throttle = client.network_throttle  # Use dot notation for property access
            >>> print(f"Network throttle object: {throttle}")
            >>> # The returned NetworkThrottle object can be used to configure bandwidth limits

        #ai-gen-doc
        """
        if self._network_throttle is None:
            self._network_throttle = NetworkThrottle(self)

        return self._network_throttle

    @property
    def is_cluster(self) -> bool:
        """Check if the client is of cluster type.

        Returns:
            True if the client is identified as a cluster type, False otherwise.

        Example:
            >>> client = Client(...)
            >>> if client.is_cluster:
            ...     print("This client is a cluster type.")
            ... else:
            ...     print("This client is not a cluster type.")

        #ai-gen-doc
        """
        return 'clusterGroupAssociation' in self._properties['clusterClientProperties']

    @property
    def network_status(self) -> int:
        """Get the network status flag for the client.

        Returns:
            Integer value representing the client's network status. The meaning of the flag depends on the implementation.

        Example:
            >>> client = Client(...)
            >>> status = client.network_status  # Use dot notation for property access
            >>> print(f"Client network status: {status}")

        #ai-gen-doc
        """
        return self._network_status

    def enable_backup(self) -> None:
        """Enable backup operations for this client.

        This method sends a request to enable backup for the current client instance.
        If the operation fails, an SDKException is raised with details about the failure.

        Raises:
            SDKException: If enabling backup fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(...)
            >>> client.enable_backup()
            >>> print("Backup enabled successfully for the client.")
            # If an error occurs, SDKException will be raised with the error details.

        #ai-gen-doc
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

    def enable_backup_at_time(self, enable_time: str, **kwargs: Any) -> None:
        """Disable backup if currently enabled, and schedule backup to be enabled at the specified time.

        Args:
            enable_time: Time to enable the backup, in 24-hour format "YYYY-MM-DD HH:mm:ss".
            **kwargs: Additional keyword arguments for backup configuration.

        Raises:
            SDKException: If the specified time is in the past, not in the correct format,
                if enabling backup fails, or if the response is empty or unsuccessful.

        Example:
            >>> client = Client(...)
            >>> # Schedule backup to be enabled at 2024-07-01 23:00:00
            >>> client.enable_backup_at_time("2024-07-01 23:00:00")
            >>> # You can also pass additional options as keyword arguments
            >>> client.enable_backup_at_time("2024-07-01 23:00:00", force=True)
        #ai-gen-doc
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

    def disable_backup(self) -> None:
        """Disable backup operations for this client.

        This method sends a request to disable backup for the current client instance.
        If the operation fails, or if the response is empty or unsuccessful, an SDKException is raised.

        Raises:
            SDKException: If the backup could not be disabled, if the response is empty, or if the response indicates failure.

        Example:
            >>> client = Client(...)
            >>> client.disable_backup()
            >>> print("Backup disabled successfully for the client.")
            >>> # If the operation fails, an SDKException will be raised.

        #ai-gen-doc
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

    def enable_restore(self) -> None:
        """Enable restore functionality for this client.

        This method sends a request to enable restore operations for the client.
        If the operation fails, an SDKException is raised with details about the failure.

        Raises:
            SDKException: If enabling restore fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(...)
            >>> client.enable_restore()
            >>> print("Restore enabled successfully for the client.")
            # If an error occurs, SDKException will be raised with details.

        #ai-gen-doc
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

    def enable_restore_at_time(self, enable_time: str, **kwargs: Any) -> None:
        """Enable restore functionality at a specified future time.

        This method disables restore if it is currently enabled, and schedules it to be enabled
        at the provided time. The time must be specified in 24-hour format (YYYY-MM-DD HH:mm:ss).
        Additional keyword arguments, such as timezone, can be provided to customize the operation.

        Args:
            enable_time: The time to enable restore, in 24-hour format (YYYY-MM-DD HH:mm:ss).
            **kwargs: Additional keyword arguments for the operation.
                timezone: The timezone to use for scheduling the restore. Refer to the TIMEZONES dict in constants.py.

        Raises:
            SDKException: If the provided time is in the past, not in the correct format,
                if enabling restore fails, or if the response is empty or unsuccessful.

        Example:
            >>> client = Client(...)
            >>> # Enable restore at 2024-07-01 22:30:00 in UTC timezone
            >>> client.enable_restore_at_time("2024-07-01 22:30:00", timezone="UTC")
            >>> print("Restore scheduled successfully.")

        #ai-gen-doc
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

    def disable_restore(self) -> None:
        """Disable restore operations for this client.

        This method sends a request to the Commcell to disable restore functionality for the current client.
        If the operation fails, an SDKException is raised with details about the error.

        Raises:
            SDKException: If the request to disable restore fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(commcell_object, client_name)
            >>> client.disable_restore()
            >>> print("Restore operations have been disabled for the client.")

        #ai-gen-doc
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

    def enable_data_aging(self) -> None:
        """Enable Data Aging for this client.

        This method sends a request to enable Data Aging on the client. Data Aging allows the removal of aged data according to retention policies.

        Raises:
            SDKException: If enabling data aging fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(commcell_object, "ClientName")
            >>> client.enable_data_aging()
            >>> print("Data Aging enabled successfully for the client.")
        #ai-gen-doc
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

    def enable_data_aging_at_time(self, enable_time: str, **kwargs: Any) -> None:
        """Enable Data Aging at a specified future time.

        This method disables Data Aging if it is currently enabled, and then schedules
        Data Aging to be enabled at the provided time. The time must be specified in
        24-hour format: 'YYYY-MM-DD HH:mm:ss'. Optional keyword arguments such as
        'timezone' can be provided to specify the timezone for the operation.

        Args:
            enable_time: The time to enable Data Aging, in 'YYYY-MM-DD HH:mm:ss' format.
            **kwargs: Additional keyword arguments for the operation.
                timezone: (str) Timezone to use for scheduling. Refer to the TIMEZONES dict in constants.py.

        Raises:
            SDKException: If the provided time is in the past, not in the correct format,
                if enabling Data Aging fails, or if the response is empty or unsuccessful.

        Example:
            >>> client = Client(...)
            >>> # Enable Data Aging at 11:30 PM on June 30, 2024, in UTC timezone
            >>> client.enable_data_aging_at_time('2024-06-30 23:30:00', timezone='UTC')
            >>> print("Data Aging scheduled successfully")
        #ai-gen-doc
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

    def disable_data_aging(self) -> None:
        """Disable Data Aging for this Client.

        This method sends a request to disable data aging for the client.
        If the operation fails, an SDKException is raised with details about the failure.

        Raises:
            SDKException: If the request to disable data aging fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(...)
            >>> client.disable_data_aging()
            >>> print("Data Aging has been disabled for the client.")
        #ai-gen-doc
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

    def execute_script(
        self,
        script_type: str,
        script: str,
        script_arguments: Optional[str] = None,
        wait_for_completion: bool = True,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Tuple[int, str, str]:
        """Execute a text-based script of the specified type on this client.

        Only scripts in text format are supported; binary or byte content is not allowed.
        The method executes the given script (either as a file path or direct script content)
        on the client, optionally with arguments and user impersonation.

        Args:
            script_type: Type of script to execute. Supported values are:
                - "JAVA"
                - "Python"
                - "PowerShell"
                - "WindowsBatch"
                - "UnixShell"
            script: Path to the script file or the script content as a string.
            script_arguments: Optional arguments to pass to the script.
            wait_for_completion: Whether to wait for the script execution to finish before returning.
            username: Optional username for user impersonation during script execution.
            password: Optional password for the impersonation user.

        Returns:
            A tuple containing:
                int: Exit code returned from executing the script on the client (-1 if not returned).
                str: Output from the script execution ('' if not returned).
                str: Error message from the script execution ('' if not returned).

        Raises:
            SDKException: If script type or script argument is not a string,
                if script type is invalid, or if the response is empty or unsuccessful.

        Example:
            >>> client = Client(...)
            >>> exit_code, output, error = client.execute_script(
            ...     script_type="Python",
            ...     script="/path/to/script.py",
            ...     script_arguments="--option value",
            ...     wait_for_completion=True
            ... )
            >>> print(f"Exit code: {exit_code}")
            >>> print(f"Output: {output}")
            >>> print(f"Error: {error}")

        #ai-gen-doc
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

    def execute_command(
        self,
        command: str,
        script_arguments: Optional[str] = None,
        wait_for_completion: bool = True,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Tuple[int, str, str]:
        """Execute a command on the client system.

        This method sends a command to be executed on the client, optionally with script arguments and user impersonation.
        It can wait for the command to complete and returns the exit code, output, and error message from the execution.

        Args:
            command: The command string to be executed on the client.
            script_arguments: Optional arguments to pass to the script or command.
            wait_for_completion: Whether to wait for the command execution to finish before returning.
            username: Optional username for user impersonation during command execution.
            password: Optional password for the impersonated user.

        Returns:
            A tuple containing:
                int: Exit code returned from executing the command on the client (default: -1 if not returned).
                str: Output returned from executing the command (default: '' if not returned).
                str: Error message returned from executing the command (default: '' if not returned).

        Raises:
            SDKException: If the command argument is not a string, if the response is empty, or if the response indicates failure.

        Example:
            >>> client = Client(...)
            >>> exit_code, output, error = client.execute_command(
            ...     command="ls -l /tmp",
            ...     script_arguments=None,
            ...     wait_for_completion=True
            ... )
            >>> print(f"Exit code: {exit_code}")
            >>> print(f"Output: {output}")
            >>> print(f"Error: {error}")

        #ai-gen-doc
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

    def enable_intelli_snap(self) -> None:
        """Enable Intelli Snap backups for this Client.

        This method updates the client properties to enable Intelli Snap functionality.
        It sends a request to the Commcell server and refreshes the client properties upon success.

        Raises:
            SDKException: If enabling Intelli Snap fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(commcell_object, client_name)
            >>> client.enable_intelli_snap()
            >>> print("Intelli Snap has been enabled for the client.")
        #ai-gen-doc
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

    def disable_intelli_snap(self) -> None:
        """Disable Intelli Snap backups for this client.

        This method updates the client properties to disable Intelli Snap functionality.
        If the operation fails or the response is invalid, an SDKException is raised.

        Raises:
            SDKException: If disabling Intelli Snap fails, the response is empty, or the response indicates an error.

        Example:
            >>> client = Client(...)
            >>> client.disable_intelli_snap()
            >>> print("Intelli Snap has been disabled for the client.")
        #ai-gen-doc
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

    def set_windows_os_updates(self, enable: bool = True) -> None:
        """Set Windows os updates for this client.

        This method sends a request to set Windows os updates for the current client instance.
        If the operation fails, an SDKException is raised with details about the failure.

        Args:
            enable: True to enable the option, False to disable. Default: True.

        Raises:
            SDKException: If setting Windows os updates fails, the response is empty, or the response indicates an
                          error.

        Example:
            >>> client = Client(...)
            >>> client.set_windows_os_updates()
            >>> print("windows os updates enabled successfully for the client.")
            # If an error occurs, SDKException will be raised with the error details.

        #ai-gen-doc
        """
        self._set_patch_options(option_type=2, enable=enable)

    def set_microsoft_sql_server_updates(self, enable: bool = True) -> None:
        """Set Microsoft SQL Server updates for this client.

        This method sends a request to set Microsoft SQL server updates for the current client instance.
        If the operation fails, an SDKException is raised with details about the failure.

        Args:
            enable: True to enable the option, False to disable. Default: True.

        Raises:
            SDKException: If setting Microsoft SQL server updates fails, the response is empty, or the response
                          indicates an error.

        Example:
            >>> client = Client(...)
            >>> client.set_microsoft_sql_server_updates()
            >>> print("Microsoft SQL Server updates enabled successfully for the client.")
            # If an error occurs, SDKException will be raised with the error details.

        #ai-gen-doc
        """
        self._set_patch_options(option_type=1, enable=enable)

    @property
    def is_ready(self) -> bool:
        """Check if CommServ is able to communicate with the client.

        Returns:
            True if the CommServ (CS) can successfully connect to the client.
            False if communication between the CS and the client fails.

        Raises:
            SDKException: If the response from the readiness check is empty or not successful.

        Example:
            >>> client = Client(...)
            >>> if client.is_ready:
            ...     print("Client is reachable from CommServ.")
            ... else:
            ...     print("Communication with client failed.")

        #ai-gen-doc
        """
        return self.readiness_details.is_ready()

    @property
    def is_mongodb_ready(self) -> bool:
        """Check if MongoDB is operational for this client.

        Returns:
            True if MongoDB is working correctly; False if there is an error.

        Raises:
            SDKException: If the response from the readiness check is not successful.

        Example:
            >>> client = Client(...)
            >>> if client.is_mongodb_ready:
            ...     print("MongoDB is ready for operations.")
            ... else:
            ...     print("MongoDB is not ready. Please check the configuration.")

        #ai-gen-doc
        """
        return self.readiness_details.is_mongodb_ready()

    def upload_file(self, source_file_path: str, destination_folder: str) -> None:
        """Upload a source file from the controller machine to a destination folder on the client machine.

        This method transfers the specified file to the client, either as a single upload or in chunks,
        depending on the file size.

        Args:
            source_file_path: Path to the source file on the controller machine.
            destination_folder: Path to the destination folder on the client machine where the file will be copied.

        Raises:
            SDKException: If the file upload fails, the response is empty, or the response indicates failure.

        Example:
            >>> client = Client(...)
            >>> client.upload_file('/home/user/data.txt', 'C:\\Data\\Uploads')
            >>> print("File uploaded successfully to the client machine.")

        #ai-gen-doc
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

    def upload_folder(self, source_dir: str, destination_dir: str):
        """Upload a folder from the controller machine to the specified destination on the client machine.

        This method recursively uploads all files and subfolders from the given source directory
        to the destination directory on the client machine. The destination path is constructed
        based on the client's operating system.

        Args:
            source_dir: Path to the source directory on the controller machine.
            destination_dir: Path on the client machine where the folder and its contents will be copied.

        Raises:
            SDKException: If the upload fails, the response is empty, or the response indicates failure.

        Example:
            >>> client = Client(...)
            >>> client.upload_folder('/home/user/data', 'C:\\Backup\\Data')
            >>> # The contents of '/home/user/data' will be uploaded to 'C:\\Backup\\Data' on the client

        #ai-gen-doc
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

    def start_service(self, service_name: Optional[str] = None) -> None:
        """Start a Commvault service on the client machine.

        Executes the command to start the specified Commvault service. If no service name is provided,
        the default service(s) will be started.

        Args:
            service_name: Optional name of the service to start (e.g., "GxVssProv(Instance001)"). If None, starts default services.

        Raises:
            SDKException: If the service fails to start.

        Example:
            >>> client = Client(...)
            >>> client.start_service("GxVssProv(Instance001)")
            >>> # To start default services
            >>> client.start_service()
        #ai-gen-doc
        """
        return self._service_operations(service_name, 'START')

    def stop_service(self, service_name: Optional[str] = None) -> None:
        """Stop a Commvault service on the client machine.

        Executes a command to stop the specified Commvault service. If no service name is provided,
        all relevant services may be stopped depending on the client configuration.

        Args:
            service_name: Optional; the name of the service to stop (e.g., "GxVssProv(Instance001)"). If None, stops default services.

        Raises:
            SDKException: If the service fails to stop.

        Example:
            >>> client = Client(...)
            >>> client.stop_service("GxVssProv(Instance001)")
            >>> # To stop all default services
            >>> client.stop_service()
        #ai-gen-doc
        """
        return self._service_operations(service_name, 'STOP')

    def restart_service(self, service_name: Optional[str] = None) -> None:
        """Restart a Commvault service on the client machine.

        Executes the command to restart the specified Commvault service. If no service name is provided,
        the default service(s) will be restarted.

        Args:
            service_name: Optional; name of the service to be restarted (e.g., "GxVssProv(Instance001)").
                If None, restarts the default service(s).

        Raises:
            SDKException: If the service fails to restart.

        Example:
            >>> client = Client(...)
            >>> client.restart_service("GxVssProv(Instance001)")
            >>> # To restart the default service(s)
            >>> client.restart_service()
        #ai-gen-doc
        """
        return self._service_operations(service_name, 'RESTART')

    def restart_services(self, wait_for_service_restart: bool = True, timeout: int = 10, implicit_wait: int = 5) -> None:
        """Restart all services on the client machine.

        This method executes a command to restart all services on the client. Optionally, it can wait until
        the services are fully restarted, or simply trigger the restart and exit immediately.

        Args:
            wait_for_service_restart: If True, waits until all client services are restarted before returning.
                If False, triggers the restart and exits without waiting.
            timeout: Maximum time in minutes to wait for services to restart. If services are not restarted
                within this period, an SDKException is raised.
            implicit_wait: Time in seconds to wait before checking if the services are ready after restart.

        Raises:
            SDKException: If the services fail to restart within the specified timeout.

        Example:
            >>> client = Client(...)
            >>> # Restart all services and wait for completion (default behavior)
            >>> client.restart_services()
            >>>
            >>> # Restart services and exit immediately without waiting
            >>> client.restart_services(wait_for_service_restart=False)
            >>>
            >>> # Restart services with custom timeout and implicit wait
            >>> client.restart_services(timeout=15, implicit_wait=10)

        #ai-gen-doc
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

    def get_network_summary(self) -> str:
        """Retrieve the network summary information for the client.

        This method sends a request to the Commcell to obtain the network configuration summary
        for the current client. If no network configuration is found, an empty string is returned.

        Returns:
            The network summary as a string. Returns an empty string if no network configuration is found.

        Raises:
            SDKException: If the response from the Commcell is not successful.

        Example:
            >>> client = Client(commcell_object, client_id)
            >>> summary = client.get_network_summary()
            >>> print(f"Network Summary: {summary}")
            >>> # If no network configuration exists, summary will be an empty string

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['GET_NETWORK_SUMMARY'].replace('%s', self.client_id))
        if flag:
            if "No Network Config found" in response.text or "No Network Configuration Found" in response.text:
                return ""
            return response.text
        raise SDKException('Response', '101', self._update_response_(response.text))

    def change_exchange_job_results_directory(
            self, new_directory_path: str, username: Optional[str] = None, password: Optional[str] = None
        ) -> None:
        """Change the Job Result Directory for an Exchange Online Client.

        This method updates the job results directory for the Exchange Online client.
        If the new directory is a network share (UNC path), valid credentials must be provided.

        Args:
            new_directory_path: The new job results directory path. Can be a local path (e.g., "C:\\JR") or a UNC path (e.g., "\\\\server\\share").
            username: Optional. Username for accessing the network share, required if new_directory_path is a UNC path.
            password: Optional. Password for accessing the network share, required if new_directory_path is a UNC path.

        Raises:
            SDKException: If the operation fails due to invalid client type, missing credentials for UNC path, or errors during the directory move.

        Example:
            >>> client = Client(...)
            >>> # Change to a local directory
            >>> client.change_exchange_job_results_directory("C:\\JR")
            >>> # Change to a network share with credentials
            >>> client.change_exchange_job_results_directory(
            ...     "\\\\server\\share", username="admin", password="password123"
            ... )
        #ai-gen-doc
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
            self, new_directory_path: str, username: Optional[str] = None, password: Optional[str] = None
        ) -> None:
        """Change the Job Result Directory for an Office 365 Client.

        This method updates the location where job results are stored for the O365 client.
        If the new directory is a shared or UNC path, provide the appropriate username and password
        for authentication.

        Args:
            new_directory_path: The new job results directory path. Can be a local path (e.g., "C:\\JR") or a UNC path (e.g., "\\\\server\\share").
            username: Optional username for accessing the new directory if it is a shared or UNC path.
            password: Optional password for accessing the new directory if it is a shared or UNC path.

        Raises:
            SDKException: If there is an error moving the job results directory.

        Example:
            >>> client = Client(...)
            >>> client.change_o365_client_job_results_directory("C:\\JR")
            >>> # For UNC path with credentials
            >>> client.change_o365_client_job_results_directory(
            ...     "\\\\server\\share", username="admin", password="password123"
            ... )
        #ai-gen-doc
        """
        self.change_exchange_job_results_directory(new_directory_path, username, password)

    def push_network_config(self) -> None:
        """Push the network configuration to the client.

        This method sends a network configuration update request to the client using the Commcell services.
        It performs a push operation for firewall configuration and validates the response for success.

        Raises:
            SDKException: If input data is invalid, the response is empty, or the response indicates failure.

        Example:
            >>> client = Client(commcell_object, "Client01")
            >>> client.push_network_config()
            >>> print("Network configuration pushed successfully")
            # If an error occurs, SDKException will be raised.

        #ai-gen-doc
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

    def add_user_associations(self, associations_list: List[Dict[str, str]]) -> None:
        """Add user associations to the owners list of this client.

        This method associates a list of users with specific roles as owners of the client.
        Each association should be a dictionary containing 'user_name' and 'role_name' keys.

        Args:
            associations_list: List of dictionaries, each specifying a user and their role to be associated with the client.
                Example:
                    associations_list = [
                        {
                            'user_name': 'user1',
                            'role_name': 'role1'
                        },
                        {
                            'user_name': 'user2',
                            'role_name': 'role2'
                        }
                    ]

        Note:
            You can retrieve available roles using the `available_security_roles` property of the Client object.

        Example:
            >>> associations = [
            ...     {'user_name': 'alice', 'role_name': 'BackupAdmin'},
            ...     {'user_name': 'bob', 'role_name': 'Operator'}
            ... ]
            >>> client = Client(...)
            >>> client.add_user_associations(associations)
            >>> print("User associations added successfully")

        #ai-gen-doc
        """
        if not isinstance(associations_list, list):
            raise SDKException('Client', '101')

        self._security_association._add_security_association(associations_list, user=True)

    def add_client_owner(self, owner_list: List[str]) -> None:
        """Add users to the owners list of this client.

        This method associates the specified users as owners of the client.
        Each user in the list must exist in the Commcell. If a user is not found,
        an exception is raised. The method updates the client's properties to reflect
        the new owner associations.

        Args:
            owner_list: List of user names (as strings) to be added as owners of the client.

        Raises:
            SDKException: If the input data is invalid (e.g., owner_list is not a list).
            Exception: If any user in owner_list does not exist in the Commcell.

        Example:
            >>> client = Client(...)
            >>> client.add_client_owner(['alice', 'bob'])
            >>> # 'alice' and 'bob' are now owners of the client

        #ai-gen-doc
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

        owner_dict = {"entityAssociated": {
                        "entity": [
                          {
                            "_type_": 3,
                            "clientId": int(self.client_id)
                          }
                        ]
                      }
                    }
        owner_dict["securityAssociations"] = properties_dict['clientProps']['securityAssociations']
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._SECURITY_ASSOCIATION, owner_dict
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    if response.json()['response'][0].get('errorCode', 0):
                        error_message = response.json()['response'][0].get('errorMessage')
                        if not error_message:
                            error_message = response.json()['response'][0].get('errorString', '')

                        if not error_message:
                            error_message = response.json()['response'][0].get('warningMessage', '')

                        if not error_message:
                            o_str = 'Failed to add owner\nError: "{0}"'.format(error_message)
                            raise SDKException('Client', '102', o_str)
                    self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            error_message = self._update_response_(response.text)
            if response.json():
                error_message = response.json().get('errorMessage', '')
            raise SDKException('Response', '101', error_message)

    def filter_clients_return_displaynames(self, filter_by: str = "OS", **kwargs: Any) -> List[str]:
        """Retrieve display names of clients filtered by operating system or other criteria.

        This method fetches all clients associated with the Commcell and returns their display names
        based on the specified filter criteria. The primary filter supported is by operating system (OS),
        with optional arguments to further refine the results.

        Args:
            filter_by: Criteria to filter clients. Accepted value is "OS".
            **kwargs: Optional arguments to customize filtering:
                os_type (str): Operating system type to filter clients (e.g., "Windows", "Unix", "NAS").
                url_params (dict): Dictionary of additional URL parameters for the request.
                    Example: {"Hiddenclients": "true"}

        Returns:
            List of client display names matching the specified filter criteria.

        Raises:
            SDKException: If the response is empty or unsuccessful.

        Example:
            >>> # Filter clients by Windows OS
            >>> client_mgr = Client(commcell_object)
            >>> windows_clients = client_mgr.filter_clients_return_displaynames(
            ...     filter_by="OS", os_type="Windows"
            ... )
            >>> print(f"Windows clients: {windows_clients}")

            >>> # Filter clients with additional URL parameters
            >>> hidden_clients = client_mgr.filter_clients_return_displaynames(
            ...     filter_by="OS", os_type="Unix", url_params={"Hiddenclients": "true"}
            ... )
            >>> print(f"Hidden Unix clients: {hidden_clients}")

        #ai-gen-doc
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

    def refresh(self) -> None:
        """Reload the properties and cached data for this Client instance.

        This method refreshes the client's properties and clears any cached settings, agents, schedules, users, and network information if applicable. Use this to ensure the Client object reflects the latest state from the Commcell.

        Example:
            >>> client = Client(commcell_object, "Server01")
            >>> client.refresh()  # Updates client properties and clears cached data
            >>> print("Client properties refreshed successfully")

        #ai-gen-doc
        """
        self._get_client_properties()
        self._additional_settings = None
        if self._client_type_id == 0:
            self._agents = None
            self._schedules = None
            self._users = None
            self._network = None

    def set_encryption_property(self,
                               enc_setting: str = "USE_SPSETTINGS",
                               key: Optional[str] = None,
                               key_len: Optional[str] = None) -> None:
        """Update the encryption properties for the client.

        This method configures the encryption settings on the client, allowing you to enable or disable encryption,
        and specify the cipher type and key length when enabling client-side encryption.

        Args:
            enc_setting: Sets the encryption level on the client. Valid values are "USE_SPSETTINGS", "OFF", or "ON_CLIENT".
                - "USE_SPSETTINGS": Use storage policy settings (default).
                - "OFF": Disable encryption on the client.
                - "ON_CLIENT": Enable client-side encryption (requires `key` and `key_len`).
            key: Cipher type to use when enabling client-side encryption (e.g., "TwoFish"). Required if `enc_setting` is "ON_CLIENT".
            key_len: Cipher key length as a string (e.g., "256"). Required if `enc_setting` is "ON_CLIENT".

        Raises:
            SDKException: If invalid parameters are provided or if the encryption property update fails.

        Example:
            >>> # Enable client-side encryption with TwoFish cipher and 256-bit key
            >>> client_object.set_encryption_property("ON_CLIENT", "TwoFish", "256")
            >>>
            >>> # Disable encryption on the client
            >>> client_object.set_encryption_property("OFF")
            >>>
            >>> # Use storage policy encryption settings (default)
            >>> client_object.set_encryption_property()

        #ai-gen-doc
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
                           prop_name: str,
                           prop_value: str,
                           client_side_cache: Optional[bool] = None,
                           max_cache_db: Optional[int] = None,
                           high_latency_optimization: Optional[bool] = None,
                           variable_content_alignment: Optional[bool] = None
                           ) -> None:
        """Set deduplication (DDB) properties for the client.

        This method configures deduplication settings such as client-side deduplication, disk cache usage,
        cache database size, high latency optimization, and variable content alignment for the client.

        Args:
            prop_name: Name of the deduplication property to set. Common values:
                - "clientSideDeduplication"
            prop_value: Value for the deduplication property. For "clientSideDeduplication", valid values are:
                - "USE_SPSETTINGS": Use storage policy settings
                - "ON_CLIENT": Enable client-side deduplication
                - "OFF": Disable client-side deduplication
            client_side_cache: Whether to enable client-side disk cache. If None, property is not modified.
            max_cache_db: Size of the cache database in MB. Valid values include:
                1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072. If None, uses default size.
            high_latency_optimization: Enable optimization for high latency networks. If None, property is not modified.
            variable_content_alignment: Enable variable content alignment for improved deduplication. If None, property is not modified.

        Raises:
            SDKException: If invalid property names/values are provided, or if the update fails.

        Example:
            >>> client = Client(...)
            >>> # Enable client-side deduplication with disk cache and 8192MB cache DB
            >>> client.set_dedup_property(
            ...     prop_name="clientSideDeduplication",
            ...     prop_value="ON_CLIENT",
            ...     client_side_cache=True,
            ...     max_cache_db=8192,
            ...     high_latency_optimization=True,
            ...     variable_content_alignment=True
            ... )
            >>> # Disable client-side deduplication
            >>> client.set_dedup_property(
            ...     prop_name="clientSideDeduplication",
            ...     prop_value="OFF"
            ... )

        #ai-gen-doc
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

    def add_additional_setting(self, category: str, key_name: str, data_type: str, value: str) -> None:
        """Add a registry key to the client property.

        This method adds an additional registry key to the client configuration, allowing customization
        of client behavior through registry settings.

        Args:
            category: Category of the registry key (e.g., "Network", "Security").
            key_name: Name of the registry key to add.
            data_type: Data type of the registry key. Accepted values are:
                "BOOLEAN", "INTEGER", "STRING", "MULTISTRING", "ENCRYPTED".
            value: Value to assign to the registry key.

        Raises:
            SDKException: If the registry key could not be added, if the response is empty,
                or if the response code is not as expected.

        Example:
            >>> client = Client(...)
            >>> client.add_additional_setting(
            ...     category="Network",
            ...     key_name="EnableIPv6",
            ...     data_type="BOOLEAN",
            ...     value="True"
            ... )
            >>> print("Registry key added successfully")
        #ai-gen-doc
        """

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

    def delete_additional_setting(self, category: str, key_name: str) -> None:
        """Delete a registry key from the client's additional settings.

        Removes the specified registry key under the given category from the client properties.
        Raises an SDKException if the deletion fails, the response is empty, or the response code is not as expected.

        Args:
            category: Category of the registry key to delete (as a string).
            key_name: Name of the registry key to delete (as a string).

        Raises:
            SDKException: If the deletion fails, the response is empty, or the response code is not as expected.

        Example:
            >>> client = Client(...)
            >>> client.delete_additional_setting('Network', 'ProxyServer')
            >>> print("Registry key deleted successfully")
        #ai-gen-doc
        """

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

    def get_configured_additional_settings(self) -> List[str]:
        """Retrieve the names of configured additional settings for the client.

        This method fetches the list of additional registry keys (settings) that have been configured
        for the client. If the request fails or an error is returned, an SDKException is raised.

        Returns:
            List of strings representing the names of configured additional settings.

        Raises:
            SDKException: If the request fails or the response contains an error message.

        Example:
            >>> client = Client(...)
            >>> settings = client.get_configured_additional_settings()
            >>> print(f"Configured additional settings: {settings}")
            >>> # Each item in 'settings' is the name of an additional registry key

        #ai-gen-doc
        """
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

    def release_license(self, license_name: Optional[str] = None) -> None:
        """Release a license from the client.

        If a specific license name is provided, releases that license from the client.
        If no license name is given, releases all licenses associated with the client except mediaagent license.

        Args:
            license_name: Name of the license to be released. If None, all licenses will be released.

        Raises:
            SDKException: If the license release fails, the response is empty, or the response code is not as expected.

        Example:
            >>> client = Client(...)
            >>> # Release a specific license
            >>> client.release_license('FileSystemAgent')
            >>> # Release all licenses from the client
            >>> client.release_license()
        #ai-gen-doc
        """
        license_type_id = 0
        app_type_id = 0
        platform_type = 1
        is_client_level_operation = True
        
        if license_name is not None:
            if self.consumed_licenses.get(license_name):
                license_type_id = self.consumed_licenses[license_name].get('licenseType')
                app_type_id = self.consumed_licenses[license_name].get('appType')
                platform_type = self.consumed_licenses[license_name].get('platformType')
                is_client_level_operation = False
            else:
                raise Exception(
                    "Provided license name is not configured in the client")
        request_json = {
            "isClientLevelOperation": is_client_level_operation,
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

    def retire(self) -> 'Job':
        """Uninstall the CommVault Software from the client, release its license, and delete the client.

        This method initiates the client retirement process, which includes uninstalling the software,
        releasing the associated license, and removing the client from the Commcell. Upon successful
        completion, it returns a Job object representing the uninstall job.

        Returns:
            Job: Job object corresponding to the uninstall operation.

        Raises:
            SDKException: If the client retirement fails, the response is empty, or the response code is not as expected.

        Example:
            >>> client = Client(...)
            >>> uninstall_job = client.retire()
            >>> print(f"Uninstall job started with Job ID: {uninstall_job.job_id}")
            >>> # The returned Job object can be used to monitor the uninstall progress

        #ai-gen-doc
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

    def reconfigure_client(self) -> None:
        """Reapply the license to the client.

        This method sends a request to the Commcell to reconfigure the license for the client.
        It updates the license information upon successful completion.

        Raises:
            SDKException: If the client reconfiguration fails, the response is empty, or the response code is not as expected.

        Example:
            >>> client = Client(...)
            >>> client.reconfigure_client()
            >>> print("License reapplied successfully")
            >>> # If an error occurs, SDKException will be raised

        #ai-gen-doc
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
            reboot_client: bool = False,
            run_db_maintenance: bool = True
        ) -> 'Job':
        """Trigger installation of service pack and hotfixes on the client.

        This method initiates the download and installation of service packs and hotfixes
        for the client. You can specify whether the client should be rebooted after installation
        and whether database maintenance should be performed.

        Note:
            This method cannot be used for revision upgrades.

        Args:
            reboot_client: Whether to reboot the client after installation. Default is False.
            run_db_maintenance: Whether to run database maintenance during installation. Default is True.

        Returns:
            Job: Instance of the Job class representing the download and installation job.

        Raises:
            SDKException: If the download job fails, the response is empty, the response is not successful,
                or another download job is already running.

        Example:
            >>> client = Client(...)
            >>> job = client.push_servicepack_and_hotfix(reboot_client=True, run_db_maintenance=False)
            >>> print(f"Service pack and hotfix job started: {job}")
        #ai-gen-doc
        """
        install = Install(self._commcell_object)
        return install.push_servicepack_and_hotfix(
            client_computers=[self.client_name],
            reboot_client=reboot_client,
            run_db_maintenance=run_db_maintenance
        )

    def repair_software(
            self,
            username: Optional[str] = None,
            password: Optional[str] = None,
            reboot_client: bool = False
        ):
        """Trigger a repair of the software on the client machine.

        This method initiates a repair operation for the client software, optionally using provided credentials
        and specifying whether the client machine should be rebooted after the repair.

        Args:
            username: Optional username for the machine to re-install features on. If None, uses default credentials.
            password: Optional base64-encoded password for authentication. If None, uses default credentials.
            reboot_client: Boolean flag indicating whether to reboot the client machine after repair. Defaults to False.

        Returns:
            Instance of the Job class representing the repair job.

        Raises:
            SDKException: If the install job fails, the response is empty, or the response indicates failure.

        Example:
            >>> client = Client(commcell_object, "Client01")
            >>> job = client.repair_software(username="admin", password="cGFzc3dvcmQ=", reboot_client=True)
            >>> print(f"Repair job started: {job}")
            >>> # The returned Job object can be used to monitor the repair progress

        #ai-gen-doc
        """
        install = Install(self._commcell_object)
        return install.repair_software(
            client=self.client_name,
            username=username,
            password=password,
            reboot_client=reboot_client
        )

    def get_dag_member_servers(self) -> List[str]:
        """Retrieve the member servers for an Exchange DAG client.

        This method fetches the list of server names that are part of the Exchange Database Availability Group (DAG)
        associated with this client. It communicates with the Commcell to obtain the DAG member server details.

        Returns:
            List of server names (as strings) that are members of the Exchange DAG.

        Raises:
            SDKException: If the response from the Commcell is empty or unsuccessful.

        Example:
            >>> client = Client(...)
            >>> dag_members = client.get_dag_member_servers()
            >>> print(f"DAG member servers: {dag_members}")
            >>> # The returned list contains the names of all servers in the DAG

        #ai-gen-doc
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
    def consumed_licenses(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all license details consumed by the client.

        Returns:
            Dictionary mapping license names to their details. Each entry contains:
                - licenseType: The license type ID.
                - appType: The application type ID.
                - licenseName: The name of the license.
                - platformType: The platform type ID.

        Raises:
            SDKException: If the license details cannot be retrieved, the response is empty, or the response code is unexpected.

        Example:
            >>> client = Client(...)
            >>> licenses = client.consumed_licenses  # Use dot notation for property access
            >>> for name, details in licenses.items():
            ...     print(f"License: {name}, Type: {details['licenseType']}, Platform: {details['platformType']}")
            >>> # The returned dictionary contains all licenses consumed by the client

        #ai-gen-doc
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
    def cvd_port(self) -> int:
        """Get the CVD (Commvault Daemon) port number configured for the client.

        Returns:
            The CVD port number as an integer.

        Example:
            >>> client = Client(...)
            >>> port = client.cvd_port  # Use dot notation for property access
            >>> print(f"CVD port: {port}")
            >>> # The returned port can be used for network configuration or diagnostics

        #ai-gen-doc
        """

        return self._cvd_port

    @property
    def client_guid(self) -> str:
        """Get the globally unique identifier (GUID) of the client.

        Returns:
            The client GUID as a string.

        Example:
            >>> client = Client(...)
            >>> guid = client.client_guid  # Use dot notation for property access
            >>> print(f"Client GUID: {guid}")
            >>> # The GUID uniquely identifies the client in the Commcell environment

        #ai-gen-doc
        """

        return self._properties.get('client', {}).get('clientEntity', {}).get('clientGUID', {})

    @property
    def client_type(self) -> str:
        """Get the type of the client as a string.

        Returns:
            The client type, such as 'Virtual', 'Physical', or other supported types.

        Example:
            >>> client = Client(...)
            >>> client_type = client.client_type  # Use dot notation for property access
            >>> print(f"Client type: {client_type}")
            >>> # Output might be: "Virtual" or "Physical"

        #ai-gen-doc
        """

        return self._properties.get('pseudoClientInfo', {}).get('clientType', "")

    @property
    def vm_guid(self) -> str:
        """Get the GUID of the VM client.

        Returns:
            The globally unique identifier (GUID) of the VM client as a string.

        Example:
            >>> client = Client(...)
            >>> guid = client.vm_guid  # Use dot notation for property access
            >>> print(f"VM GUID: {guid}")

        #ai-gen-doc
        """

        return self._vm_guid

    def set_job_start_time(self, job_start_time_value: int) -> None:
        """Set the job start time for this Client.

        This method updates the job start time property for the client. The value should be provided
        as an integer representing the desired start time (typically in seconds since epoch or as required by the API).

        Args:
            job_start_time_value: The job start time value to set for the client.

        Raises:
            SDKException: If the job start time could not be set, if the response is empty, or if the response indicates failure.

        Example:
            >>> client = Client(...)
            >>> client.set_job_start_time(1622548800)  # Set job start time to a specific timestamp
            >>> print("Job start time updated successfully")

        #ai-gen-doc
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

    def uninstall_software(self, force_uninstall: bool = True, software_list: Optional[List[str]] = None):
        """Uninstall specified software components from the client.

        This method initiates an uninstall job for the given client, optionally forcing the uninstall
        and specifying which software components to remove.

        Args:
            force_uninstall: If True, forcibly uninstalls the specified packages. Defaults to True.
            software_list: Optional list of component names to uninstall from the client. If not provided,
                no components will be specified for removal.

        Returns:
            The job object representing the uninstall software job.

        Raises:
            SDKException: If the uninstall response is empty or unsuccessful.

        Example:
            >>> client_obj.uninstall_software(force_uninstall=False, software_list=["Index Store", "File System"])
            >>> # The returned job object can be used to monitor uninstall progress

        #ai-gen-doc
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

    def __get_componentInfo(self, software_list: List[str]) -> List[Dict[str, str]]:
        """Retrieve component information for the specified installed software.

        Args:
            software_list: List of software names to retrieve component information for.

        Returns:
            A list of dictionaries containing component information for each software item.
            Each dictionary includes:
                - "osType": The operating system type ("Windows" or "Unix").
                - "ComponentName": The name of the software component.

        Example:
            >>> client = Client(...)
            >>> software_list = ["High Availability Computing", "File System Agent"]
            >>> component_info = client.__get_componentInfo(software_list)
            >>> print(component_info)
            [
                {"osType": "Windows", "ComponentName": "High Availability Computing"},
                {"osType": "Windows", "ComponentName": "File System Agent"}
            ]
        #ai-gen-doc
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
    def job_start_time(self) -> str:
        """Get the start time of the job associated with this client.

        Returns:
            The job start time as a string, typically in a standard date-time format.

        Example:
            >>> client = Client(...)
            >>> start_time = client.job_start_time  # Use dot notation for property access
            >>> print(f"Job started at: {start_time}")

        #ai-gen-doc
        """

        return self._job_start_time

    @property
    def readiness_details(self) -> '_Readiness':
        """Get the readiness details for this client.

        Returns:
            _Readiness: An instance representing the readiness status and details of the client.

        Example:
            >>> client = Client(commcell_object, client_id)
            >>> readiness = client.readiness_details  # Use dot notation for property access
            >>> print(f"Client readiness: {readiness}")
            >>> # The returned _Readiness object can be used to check client status

        #ai-gen-doc
        """
        if self._readiness is None:
            self._readiness = _Readiness(self._commcell_object, self.client_id)
        return self._readiness

    def get_environment_details(self) -> Dict[str, Dict[str, int]]:
        """Retrieve environment details for all service Commcells.

        This method returns a dictionary containing the count of file servers, virtual machines (VMs),
        and laptops for each service Commcell. The result is organized by environment type, with each
        type mapping to a dictionary of Commcell names and their respective counts.

        Returns:
            Dictionary with keys 'fileServerCount', 'laptopCount', and 'vmCount', each mapping to a
            dictionary of Commcell names and their counts.

        Raises:
            SDKException: If the response from the server is invalid or cannot be processed.

        Example:
            >>> client = Client(...)
            >>> env_details = client.get_environment_details()
            >>> print(env_details)
            >>> # Example output:
            >>> # {
            >>> #     'fileServerCount': {'CommcellA': 5, 'CommcellB': 3},
            >>> #     'laptopCount': {'CommcellA': 10, 'CommcellB': 7},
            >>> #     'vmCount': {'CommcellA': 2, 'CommcellB': 4}
            >>> # }
        #ai-gen-doc
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

    def get_needs_attention_details(self) -> Dict[str, Dict[str, int]]:
        """Retrieve counts of anomalous servers, jobs, and infrastructure servers for all service Commcells.

        This method returns a dictionary containing the count of anomalous infrastructure servers,
        anomalous servers, and anomalous jobs for each Commcell in the environment.

        Returns:
            Dictionary mapping anomaly types to per-Commcell counts. The keys are:
                - 'CountOfAnomalousInfrastructureServers'
                - 'CountOfAnomalousServers'
                - 'CountOfAnomalousJobs'
            Each value is a dictionary mapping Commcell names to their respective counts.

        Example:
            >>> client = Client(...)
            >>> needs_attention = client.get_needs_attention_details()
            >>> print(needs_attention)
            >>> # Output:
            >>> # {
            >>> #   'CountOfAnomalousInfrastructureServers': {'CommcellA': 2, 'CommcellB': 0},
            >>> #   'CountOfAnomalousServers': {'CommcellA': 1, 'CommcellB': 3},
            >>> #   'CountOfAnomalousJobs': {'CommcellA': 0, 'CommcellB': 5}
            >>> # }

        Raises:
            SDKException: If the response from the server is invalid or the request fails.

        #ai-gen-doc
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

    def get_mount_volumes(self, volume_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Retrieve mount volumes information for the client.

        Args:
            volume_names: Optional list of volume names (as strings) to filter the returned volumes.
                If provided, only volumes matching these names will be returned. If None, all mount volumes are returned.

        Returns:
            List of dictionaries containing mount volume details. Each dictionary includes keys such as:
                - "volumeTypeFlags": int
                - "freeSize": int
                - "size": int
                - "guid": str
                - "accessPathList": List[str]

        Raises:
            SDKException: If the response is invalid or if a specified volume name is not found.

        Example:
            >>> client = Client(...)
            >>> # Get all mount volumes for the client
            >>> all_volumes = client.get_mount_volumes()
            >>> print(f"Total volumes: {len(all_volumes)}")
            >>> # Get specific volumes by name
            >>> selected_volumes = client.get_mount_volumes(['C:', 'D:'])
            >>> for vol in selected_volumes:
            ...     print(f"Volume GUID: {vol['guid']}, Paths: {vol['accessPathList']}")

        #ai-gen-doc
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

    def enable_content_indexing(self) -> None:
        """Enable v1 content indexing for the client.

        This method updates the client's properties to activate v1 content indexing,
        allowing enhanced search and retrieval capabilities for client data.

        Example:
            >>> client = Client(...)
            >>> client.enable_content_indexing()
            >>> print("Content indexing enabled for the client.")

        #ai-gen-doc
        """
        update_properties = self.properties
        update_properties['client']['EnableContentIndexing'] = 'true'
        self.update_properties(update_properties)

    def disable_content_indexing(self) -> None:
        """Disable v1 content indexing for this client.

        This method updates the client properties to turn off v1 content indexing,
        ensuring that content indexing is no longer performed on this client.

        Example:
            >>> client = Client(...)
            >>> client.disable_content_indexing()
            >>> print("Content indexing disabled for client.")
        #ai-gen-doc
        """
        update_properties = self.properties
        update_properties['client']['EnableContentIndexing'] = 'false'
        self.update_properties(update_properties)

    def enable_owner_privacy(self) -> None:
        """Enable the privacy option for the client.

        This method activates owner privacy for the client, ensuring that sensitive information
        is protected according to privacy settings. If privacy is already enabled, no action is taken.

        Example:
            >>> client = Client(...)
            >>> client.enable_owner_privacy()
            >>> # Owner privacy is now enabled for the client

        #ai-gen-doc
        """

        if self.is_privacy_enabled:
            return

        self.set_privacy(True)

    @property
    def company_name(self) -> str:
        """Get the company name to which the client belongs.

        Returns:
            The company name as a string. Returns an empty string if the client belongs to the Commcell.

        Example:
            >>> client = Client(...)
            >>> company = client.company_name  # Use dot notation for property access
            >>> print(f"Client belongs to company: {company if company else 'Commcell'}")
        #ai-gen-doc
        """
        return self._company_name

    def check_eligibility_for_migration(self, destination_company_name: str) -> bool:
        """Check if the client is eligible for migration to the specified destination company.

        This method verifies whether the current client can be migrated to the given destination company.
        It returns True if the client is eligible for migration, otherwise returns False.

        Args:
            destination_company_name: The name of the destination company to which the client is to be migrated.

        Returns:
            True if the client is eligible for migration; False otherwise.

        Raises:
            SDKException: If the response from the server is empty or not successful.

        Example:
            >>> client = Client(...)
            >>> is_eligible = client.check_eligibility_for_migration("AcmeCorp")
            >>> print(f"Migration eligibility: {is_eligible}")
            >>> # Returns True if eligible, False otherwise

        #ai-gen-doc
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

    def disable_owner_privacy(self) -> None:
        """Disable the owner privacy option for the client.

        This method turns off the privacy setting for the client if it is currently enabled.

        Example:
            >>> client = Client(...)
            >>> client.disable_owner_privacy()
            >>> print("Owner privacy disabled for the client.")
        #ai-gen-doc
        """
        if not self.is_privacy_enabled:
            return

        self.set_privacy(False)

    def set_privacy(self, value: bool) -> None:
        """Enable or disable privacy settings for the client.

        This method updates the privacy status of the client by sending a request to the Commcell server.
        If the operation fails or the response is invalid, an SDKException is raised.

        Args:
            value: Set to True to enable privacy, or False to disable privacy for the client.

        Raises:
            SDKException: If setting privacy for the client fails, the response is empty, or the response indicates failure.

        Example:
            >>> client = Client(...)
            >>> client.set_privacy(True)   # Enable privacy for the client
            >>> client.set_privacy(False)  # Disable privacy for the client

        #ai-gen-doc
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

    def change_company_for_client(self, destination_company_name: str) -> None:
        """Change the company association for this client.

        Migrates the client to the specified destination company. This operation will validate
        migration eligibility and perform the migration if allowed. If the migration fails or
        the client is not eligible, an SDKException is raised.

        Args:
            destination_company_name: The name of the destination company to which the client should be migrated.

        Raises:
            SDKException: If the client is not eligible for migration, if the response is empty,
                or if the migration request is unsuccessful.

        Example:
            >>> client = Client(...)
            >>> client.change_company_for_client("NewCompany")
            >>> print("Client migration successful.")
            # If the client is not eligible or migration fails, an SDKException will be raised.

        #ai-gen-doc
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
        """Read the specified log file from the client.

        Args:
            file_name: Name of the log file to be read.
            complete_file: If True, reads the entire log file; if False, reads a partial log.

        Returns:
            List of lines from the log file as strings.

        Raises:
            SDKException: If the log file cannot be read or the response is invalid.

        Example:
            >>> client = Client(...)
            >>> log_lines = client.read_log_file('Backup.log', complete_file=True)
            >>> for line in log_lines:
            ...     print(line)
        #ai-gen-doc
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

    def add_http_proxy(self, use_client_os_proxy_settings=False, proxy_server="", proxy_port=0,
                       use_authentication=False, use_with_network_topology=False,
                       proxy_credential_name=None, proxy_credential_id=None, proxy_bypass_list="") -> None:
        """Add an HTTP proxy configuration to the client

        Args:
            use_client_os_proxy_settings (bool): Use the client OS proxy settings.

            proxy_server (str): The proxy server address.

            proxy_port (int): The proxy server port.

            use_authentication (bool): Use authentication for the proxy.

            use_with_network_topology (bool): Use the proxy with network topology.

            proxy_credential_name (str): The name of the proxy credential.

            proxy_credential_id (int): The ID of the proxy credential.

            proxy_bypass_list (str): Comma-separated list of addresses to bypass the proxy.

        """

        proxy_type = "GLOBAL" if use_client_os_proxy_settings else "EXPLICIT"

        if proxy_type == "EXPLICIT":
            if not proxy_server or not isinstance(proxy_server, str):
                raise SDKException( 'Client', 102,
                    "proxy_server is required and must be a non-empty string when using EXPLICIT proxy."
                )
            if not isinstance(proxy_port, int) or not (1 <= proxy_port <= 65535):
                raise SDKException( 'Client', 102,
                    "proxy_port must be an integer between 1 and 65535 when using EXPLICIT proxy."
                )

        request_json = {
            "entity": {
                "clientId": int(self.client_id)
            },
            "httpProxy": {
                "server": proxy_server,
                "port": proxy_port,
                "useForNetworkRoutes": use_with_network_topology,
                "proxyBypassList": proxy_bypass_list,
                "configureHTTPProxy": True,
                "useAuthentication": use_authentication,
                "proxyType": proxy_type
            }
        }

        if proxy_credential_id and proxy_credential_name:
            request_json["httpProxy"]["credentials"] = {
                "credentialId": proxy_credential_id,
                "credentialName": proxy_credential_name
            }
        else:
            request_json["httpProxy"]["selectedCredential"] = None


        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['HTTP_PROXY'], request_json
        )

        if flag:
            if response.json():
                error_code = -1
                error_message ="Failed to add HTTP proxy configuration to the client group."
                if 'errorCode' in response.json():
                        error_code = response.json()['errorCode']
                if error_code != 0:
                    raise SDKException('Client', '102', error_message)

            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def remove_http_proxy(self) -> None:
        """Remove the HTTP proxy configuration from the client."""

        request_json = {
            "entity": {
                "clientId": int(self.client_id)
            },
            "httpProxy": {
                "configureHTTPProxy": False
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['HTTP_PROXY'], request_json
        )

        if flag:
            if response.json():
                error_code = -1
                error_message ="Failed to remove HTTP proxy configuration from the client."
                if 'errorCode' in response.json():
                    error_code = response.json()['errorCode']
                if error_code != 0:
                    raise SDKException('Client', '102', error_message)

            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def additional_settings(self) -> 'AdditionalSettings':
        """Get the AdditionalSettings instance associated with this Client.

        Returns:
            AdditionalSettings: An object for managing advanced or custom settings for the client.

        Example:
            >>> client = Client(...)
            >>> settings = client.additional_settings  # Access via property
            >>> print(f"Additional settings object: {settings}")
            >>> # The returned AdditionalSettings object can be used to configure client-specific options

        #ai-gen-doc
        """
        if self._additional_settings is None:
            self._additional_settings = AdditionalSettings(self)
        return self._additional_settings

    def send_logs(self, email_ids: Optional[List[str]], **kwargs) -> bool:
        """Send logs for this client to specified email addresses.

        This method creates a send logs task for the current client and sends the logs to the
        provided list of email addresses. It waits for the log sending task to complete and
        returns True if successful.

        Args:
            email_ids: list of email addresses to which the client logs should be sent.
            **kwargs: Additional keyword arguments for the operation.
                email_subject: (str) Subject line for the email containing the logs.

        Returns:
            True if the logs were sent successfully.

        Raises:
            SDKException: If the log sending operation fails or the response contains an error.

        Example:
            >>> client = Client(commcell_object, "Client01")
            >>> success = client.send_logs(['admin@example.com', 'support@example.com'])
            >>> print(f"Logs sent successfully: {success}")
            >>> # Send logs with job results included
            >>> client.send_logs(['admin@example.com'], include_job_results=True)

        #ai-gen-doc
        """
        if isinstance(email_ids, str):
            email_ids = [email_ids]

        email_subject = kwargs.get('email_subject',
                                   f"{self._commcell_object.commserv_name} : Logs for Client '{self.client_name}'")

        request_json = {
            "taskInfo": {
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 1,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 5010
                        },
                        "options": {
                            "adminOpts": {
                                "sendLogFilesOption": {
                                    "actionLogsEndJobId": 0,
                                    "emailSelected": True,
                                    "jobid": 0,
                                    "tsDatabase": False,
                                    "galaxyLogs": False,
                                    "getLatestUpdates": False,
                                    "actionLogsStartJobId": 0,
                                    "computersSelected": True,
                                    "csDatabase": False,
                                    "otherDatabases": False,
                                    "crashDump": False,
                                    "isNetworkPath": False,
                                    "saveToFolderSelected": False,
                                    "notifyMe": True,
                                    "includeJobResults": False,
                                    "doNotIncludeLogs": True,
                                    "machineInformation": False,
                                    "scrubLogFiles": False,
                                    "emailSubject": email_subject,
                                    "osLogs": False,
                                    "allUsersProfile": False,
                                    "splitFileSizeMB": 512,
                                    "actionLogs": False,
                                    "includeIndex": False,
                                    "databaseLogs": True,
                                    "includeDCDB": False,
                                    "collectHyperScale": False,
                                    "logFragments": False,
                                    "uploadLogsSelected": True,
                                    "useDefaultUploadOption": True,
                                    "enableChunking": True,
                                    "collectRFC": False,
                                    "collectUserAppLogs": False,
                                    "impersonateUser": {
                                        "useImpersonation": False
                                    },
                                    "clients": [
                                        {
                                            "clientId": int(self.client_id),
                                            "clientName": self.client_name
                                        }
                                    ],
                                    "recipientTo": {
                                        "emailids": email_ids,
                                        "users": [],
                                        "userGroups": []
                                    },
                                    "sendLogsOnJobCompletion": False,
                                    "emailDescription": f"Client logs for {self.client_name}"
                                }
                            }
                        }
                    }
                ]
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CREATE_TASK'], request_json
        )

        if flag:
            if response.json():
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    error_message = response.json().get('errorMessage', 'nil')
                    raise SDKException(
                        'Client', '102', 'Sending logs failed\nError: "{0}"'.format(error_message)
                    )
                else:
                    # Wait for the send logs job to complete
                    from .job import Job
                    send_logs_job = Job(self._commcell_object, response.json()['jobIds'][0])
                    try:
                        send_logs_job.wait_for_completion()
                    except Exception:
                        pass
                return True
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

class _Readiness:
    """
    Class for assessing and reporting the readiness status of a client connection.

    This class provides mechanisms to check various aspects of client readiness,
    including network connectivity, resource availability, application status, and
    MongoDB-specific readiness. It encapsulates detailed checks and exposes methods
    to retrieve readiness status, failure reasons, and diagnostic details.

    Key Features:
        - Initialization with commcell and client ID for context
        - Comprehensive readiness checks across network, resources, and applications
        - MongoDB-specific readiness verification and failure diagnostics
        - Retrieval of failure reasons and detailed status information
        - Property access to current readiness status
        - Internal methods for detailed status, reason, and detail checks

    #ai-gen-doc
    """

    def __init__(self, commcell: 'Commcell', client_id: str) -> None:
        """Initialize the _Readiness object with Commcell and client ID.

        Args:
            commcell: Instance of the Commcell class representing the backup environment.
            client_id: Unique identifier for the client as a string.

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> readiness = _Readiness(commcell, "client_123")
            >>> # The _Readiness object is now initialized for the specified client

        #ai-gen-doc
        """
        self.__commcell = commcell
        self.__client_id = client_id
        self._reason = None
        self._detail = None
        self._status = None
        self._dict = None
        self._mongodb_dict = None

    def __fetch_readiness_details(
            self,
            network: bool = True,
            resource: bool = False,
            disabled_clients: bool = False,
            cs_cc_network_check: bool = False,
            application_check: bool = False,
            additional_resources: bool = False,
            application_readiness_option: bool = False
        ):
        """Perform readiness checks on the client with configurable options.

        Args:
            network: If True, performs a network readiness check. Default is True.
            resource: If True, performs a resource readiness check. Default is False.
            disabled_clients: If True, includes clients with backup activity disabled. Default is False.
            cs_cc_network_check: If True, performs network readiness check between CommServe and client only. Default is False.
            application_check: If True, performs application readiness check. Default is False.
            additional_resources: If True, includes additional resources in the readiness check. Default is False.
            application_readiness_option: If True, includes application readiness option in the check. Default is False.

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> readiness = _Readiness(commcell_object, client_id)
            >>> readiness.__fetch_readiness_details(
            ...     network=True,
            ...     resource=True,
            ...     disabled_clients=False,
            ...     cs_cc_network_check=True,
            ...     application_check=True,
            ...     additional_resources=True
            ... )
            >>> # The readiness details will be updated in the readiness object

        #ai-gen-doc
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
                additional_resources,
                int(application_readiness_option))
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

    def is_ready(
            self,
            network: bool = True,
            resource: bool = False,
            disabled_clients: bool = False,
            cs_cc_network_check: bool = False,
            application_check: bool = False,
            additional_resources: bool = False,
            application_readiness_option = False
    ) -> bool:
        """Perform a readiness check on the client with configurable options.

        Args:
            network: If True, performs a network readiness check. Default is True.
            resource: If True, performs a resource readiness check. Default is False.
            disabled_clients: If True, includes clients with backup activity disabled. Default is False.
            cs_cc_network_check: If True, performs a network readiness check between CommServe (CS) and client only. Default is False.
            application_check: If True, performs an application readiness check. Default is False.
            additional_resources: If True, includes additional resources in the readiness check. Default is False.
            application_readiness_option: If True, includes application readiness option in the check. Default is False.

        Returns:
            True if the client is ready based on the selected checks, otherwise False.

        Example:
            >>> readiness = _Readiness()
            >>> # Perform a full readiness check including network and resource
            >>> is_client_ready = readiness.is_ready(network=True, resource=True)
            >>> print(f"Client readiness: {'Ready' if is_client_ready else 'Not Ready'}")
            >>> # Check readiness including disabled clients and application check
            >>> is_ready = readiness.is_ready(disabled_clients=True, application_check=True)
            >>> print(f"Readiness with disabled clients and application check: {is_ready}")

        #ai-gen-doc
        """
        self.__fetch_readiness_details(network, resource, disabled_clients, cs_cc_network_check,
                                       application_check, additional_resources, application_readiness_option)
        return self._status == "Ready."

    def is_mongodb_ready(self) -> bool:
        """Check if the MongoDB service is ready by calling the readiness API.

        This method performs a readiness check for the MongoDB service by sending a request to the
        MongoDB readiness API endpoint. It returns True if the service is ready, otherwise raises
        an SDKException if the check fails or the response is invalid.

        Returns:
            True if MongoDB is ready; False otherwise.

        Raises:
            SDKException: If the API response indicates an error or is invalid.

        Example:
            >>> readiness = _Readiness(commcell_object)
            >>> if readiness.is_mongodb_ready():
            ...     print("MongoDB is ready for operations.")
            ... else:
            ...     print("MongoDB is not ready.")
        #ai-gen-doc
        """
        self.__fetch_readiness_details(application_readiness_option=True)
        for entityName in self._dict.get('summary',[]):
            if entityName.get('entity', {}).get('entityName', "") == 'MongoDB':
                self._mongodb_dict = entityName
                status = entityName.get('status', "")
                return status.strip() == "Ready."
        return False

    def __check_reason(self) -> None:
        """Extract and set the reason for readiness from the internal summary dictionary.

        This method attempts to retrieve the 'reason' field from the first element of the 'summary' list
        within the internal dictionary. If the required keys are missing, the method silently ignores the error.

        Example:
            >>> readiness = _Readiness()
            >>> readiness._dict = {'summary': [{'reason': 'All systems operational'}]}
            >>> readiness.__check_reason()
            >>> print(readiness._reason)
            All systems operational

        #ai-gen-doc
        """
        try:
            self._reason = self._dict['summary'][0]['reason']
        except KeyError:
            pass

    def __check_status(self) -> None:
        """Check and update the readiness status from the internal summary dictionary.

        This method attempts to extract the 'status' value from the first element of the 'summary' list
        within the internal dictionary and updates the object's status attribute. If the required keys
        are missing, the status remains unchanged.

        Example:
            >>> readiness = _Readiness()
            >>> readiness._dict = {'summary': [{'status': 'Ready'}]}
            >>> readiness.__check_status()
            >>> # The _status attribute is now updated to 'Ready'

        #ai-gen-doc
        """
        try:
            self._status = self._dict['summary'][0]['status']
        except KeyError:
            pass

    def __check_details(self) -> None:
        """Check and update the '_detail' attribute from the internal dictionary.

        This method attempts to retrieve the 'detail' key from the internal '_dict' attribute
        and assigns its value to the '_detail' attribute. If the 'detail' key is not present,
        the method silently ignores the missing key.

        Example:
            >>> readiness = _Readiness()
            >>> readiness._dict = {'detail': 'System is ready'}
            >>> readiness.__check_details()
            >>> print(readiness._detail)
            System is ready

        #ai-gen-doc
        """
        try:
            self._detail = self._dict['detail']
        except KeyError:
            pass

    def get_failure_reason(self) -> str:
        """Retrieve the failure reason for client readiness.

        Returns:
            The failure reason as a string, describing why the client is not ready.

        Example:
            >>> readiness = _Readiness()
            >>> reason = readiness.get_failure_reason()
            >>> print(f"Failure reason: {reason}")

        #ai-gen-doc
        """
        if not self._dict:
            self.__fetch_readiness_details()
        return self._reason

    @property
    def status(self) -> str:
        """Get the client readiness status.

        Returns:
            The readiness status of the client as a string.

        Example:
            >>> readiness = _Readiness(...)
            >>> current_status = readiness.status  # Use dot notation for property access
            >>> print(f"Client readiness status: {current_status}")

        #ai-gen-doc
        """
        if not self._dict:
            self.__fetch_readiness_details()
        return self._status

    def get_detail(self) -> Dict[str, Any]:
        """Retrieve detailed readiness information for the client.

        Returns:
            Dictionary containing client readiness details.

        Example:
            >>> readiness = _Readiness()
            >>> details = readiness.get_detail()
            >>> print(details)
            >>> # The details dictionary contains readiness status and related information

        #ai-gen-doc
        """
        if not self._dict:
            self.__fetch_readiness_details()
        return self._detail

    def get_mongodb_failure_reason(self) -> Any:
        """Retrieve the failure reason for MongoDB readiness.

        This method returns details about why MongoDB is not ready, if applicable.
        If the readiness status has not been checked, it will trigger a readiness check before returning the failure details.

        Returns:
            Failure details for MongoDB readiness. The type and structure of the response may vary depending on the implementation.

        Example:
            >>> readiness = _Readiness()
            >>> failure_reason = readiness.get_mongodb_failure_reason()
            >>> print(f"MongoDB failure reason: {failure_reason}")

        #ai-gen-doc
        """
        if not self._mongodb_dict:
            self.is_mongodb_ready()
        return self._mongodb_dict.get('reason', "")
