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
"""Main file for performing operations on Commcell via REST API.

Commcell is the main class for the CVPySDK python package.

Commcell:   Initializes a connection to the commcell and is a wrapper for the entire commcell ops.

Commcell:
    __init__()                  --  initialize instance of the Commcell class

    __repr__()                  --  return the name of the commcell, user is connected to,
    along with the username of the connected user

    __enter__()                 --  returns the current instance, using the "with" context manager

    __exit__()                  --  logs out the user associated with the current instance

    _update_response_()         --  returns only the relevant response for the response received
    from the server

    _remove_attribs_()          --  removes all the attributes associated with the commcell
    object upon call to the logout method

    _get_commserv_details()     --  gets the details of the commserv, the Commcell class instance
    is initialized for

    _qoperation_execute()       --  runs the qoperation execute rest api on specified input xml

    _qoperation_execscript()    --  runs the qoperation execute qscript with specified arguements

    get_gxglobalparam_value()	--	makes a rest api call to get values from GXGlobalParam

    _set_gxglobalparam_value    --  updates GXGlobalParam(commcell level configuration parameters)

    verify_owner_assignment_config()    -- verifies that the ownership assignments settings are configured
    and set properly

    logout()                    --  logs out the user associated with the current instance

    request()                   --  runs an input HTTP request on the API specified,
    and returns its response

    send_mail()                 --  sends an email to the specified user

    refresh()                   --  refresh the properties associated with the Commcell
    class instance
    run_data_aging()            --  triggers data aging job from the commcell level

    get_saml_token()            --  returns the SAML token for the currently logged-in user

    add_additional_setting()    --  adds registry key to the commserve property

    delete_additional_setting() --  deletes registry key from the commserve property

    get_configured_additional_setting() --  To get configured additional settings from the commserve property

    download_software()         --  triggers the Download Software job with the given options

    copy_software()             --  triggers the Copy Software job with the given options

    sync_remote_cache()         --  syncs remote cache

    get_remote_cache()     		--  returns the instance of the RemoteCache class

    push_servicepack_and_hotfixes() --  triggers installation of service pack and hotfixes

    install_software()              --  triggers the install Software job with the given options

    remote_cache_clients()      --  fetches the list of Remote Cache configured for a particular Admin/Tenant

    enable_auth_code()              --  executes the request on the server to enable Auth Code
    for installation on the commcell

    disable_auth_code()             --  disables auth code requirement for installation on the commcell

    enable_shared_laptop()          --   Executes the request on the server to enable Shared Laptop on commcell

    disable_shared_laptop()         --  Executes the request on the server to disable Shared Laptop on commcell

    execute_qcommand()              --  executes the ExecuteQCommand API on the commcell

    add_associations_to_saml_app()  --  Adds the given user under associations of the SAML app

    register_commcell()             -- registers a commcell

    is_commcell_registered()       -- checks if the commcell is registered

    get_default_plan()                  -- Get the default plans associated with the commcell

    get_security_associations()         -- Get the security associations associated with the commcell

    get_password_encryption_config()    -- Get the Password encryption configuration for the commcell

    get_email_settings()                -- Get the SMTP settings for the commcell

    set_email_settings()                -- Set the SMTP settings for the commcell

    get_commcell_properties()           -- Get the general, privacy and other properties of commcell

    get_commcell_organization_properties()     -- Get the organization properties of commcell

    enable_tfa()                           --   Enables two-factor authentication on this commcell

    disable_tfa()                          --  Disables two-factor authentication on this commcell

    _get_commserv_metadata()               -- Returns back the commserv metadata on this commcell

    _get_commserv_oem_id()               -- Returns back the commserv OEM ID on this commcell

    enable_privacy()                    --  Enables users to enable data privacy on commcell

    disable_privacy()                   --  Enables users to disable data privacy on commcell

    switch_to_company()         --  Login to company as an operator, just like using switcher on Command Center

    reset_company()             --  Switch back to Commcell

    switch_to_global()          --  Adds comet fanout headers, like global mode in multi commcell command center

    is_global_scope()           --  Check if comet headers are active

    reset_to_local()            --  Removes comet headers, like switching back to local commcell

    allow_users_to_enable_passkey()     --      Enable or Disable passkey authorization for company administrators and client owners

    passkey()                       --  Updates Passkey properties of the commcell

    get_sla_configuration()         --  gets the sla configuration details at commcell level

    get_workload_region()           --  gets the current workload region

    set_workload_region()           --  sets the workload region at commcell level

    get_user_suggestions()          --  gets details of entities matching given term

    enable_limit_user_logon_attempts()  --  Enables limit user logon attempts feature.

    disable_limit_user_logon_attempts()   -- Disables limit user logon attempts feature.

    get_aws_backup_gateway_cft_url() -- Returns the CFT link to create and point AWS Backup gateway


Commcell instance Attributes
============================

    **commserv_guid**           --  returns the `CommServ` GUID, class instance is initialized for

    **commserv_hostname**       --  returns the hostname of the `CommServ`, class instance is
    initalized for

    **commserv_name**           --  returns the `CommServ` name, class instance is initialized for

    **commserv_timezone**       --  returns the time zone of the `CommServ`,
    class instance is initalized for

    **commserv_timezone_name**  --  returns the name of the `CommServ` time zone,
    class instance is initalized for

    **commserv_version**        --  returns the ContentStore version installed on the `CommServ`,
    class instance is initalized for

    **version**                 --  returns the complete version info of the commserv

    **release_name**            --  returns the release name of this commserv

    **commcell_id**             --  returns the `CommCell` ID

    **commserv_metadata**       -- returns the commserv metadata of the commserv

    **commserv_oem_id**         -- returns the commserv OEM ID of the commserv

    **webconsole_hostname**     --  returns the host name of the `webconsole`,
    class instance is connected to

    **auth_token**              --  returns the `Authtoken` for the current session to the commcell

    **commcell_username**       --  returns the associated `user` name for the current session
    to the commcell

    **device_id**               --  returns the id associated with the calling machine

    *name_change*               --  returns the name change object of the commcell

    **clients**                 --  returns the instance of the `Clients` class,
    to interact with the clients added on the Commcell

    **commserv_cache**          --  returns the instance of the `CommServeCache` class

    **media_agents**            --  returns the instance of the `MediaAgents` class,
    to interact with the media agents associated with the Commcell class instance

    **workflows**               --  returns the instance of the `WorkFlow` class,
    to interact with the workflows deployed on the Commcell

    **alerts**                  --  returns the instance of the `Alerts` class,
    to interact with the alerts available on the Commcell

    **disk_libraries**          --  returns the instance of the `DiskLibraries` class,
    to interact with the disk libraries added on the Commcell

    **tape_libraries**          --  returns the instance of the `TapeLibraries` class,
    to interact with the tape libraries added on the Commcell
    
    **storage_policies**        --  returns the instance of the `StoragePolicies` class,
    to interact with the storage policies available on the Commcell

    **schedule_policies**       --  returns the instance of the `SchedulePolicies` class,
    to interact with the schedule policies added to the Commcell

    **schedules**       --  returns the instance of the `Schedules` class,
    to interact with the schedules associated to the Commcell

    **user_groups**             --  returns the instance of the `UserGroups` class,
    to interact with the user groups added to the Commcell

    **domains**                 --  returns the instance of the `Domains` class,
    to interact with the domains added to the Commcell

    **client_groups**           --  returns the instance of the `ClientGroups` class,
    to interact with the client groups added to the Commcell

    **global_filters**          --  returns the instance of the `GlobalFilters` class,
    to interact with the global filters available on the Commcell

    **datacube**                --  returns the instance of the `Datacube` class,
    to interact with the datacube engine deployed on the Commcell

    **content_analyzers**       --  returns the instance of the `ContentAnalyzers` class,
    to interact with the CA cloud deployed on the Commcell

    **scale_targets**           --  returns the instance of the `ScaleTargets` class,
    to interact with scale targets configured on the Commcell

    **activate**                --  returns the instance of the `Activate` class,
    to interact with activate apps on the Commcell

    **threat_indicators**       --  returns the instance of Servers class, to interact with threat indicators on the commcell

    **export_sets**             --  returns the instance of the `ExportSets` class
    to interact with compliance search export sets on the Commcell

    **plans**                   --  returns the instance of the `Plans` class,
    to interact with the plans associated with the Commcell

    **job_controller**          --  returns the instance of the `JobController` class,
    to interact with all the jobs finished / running on the Commcell

    **users**                   --  returns the instance of the `Users` class,
    to interact with the users added to the Commcell

    **roles**                   --  returns the instance of the `Roles` class,
    to interact with the roles added to the Commcell

    **credentials**             --  returns the instance of the `Credentials` class,
    to interact with the credentials records added to the Commcell

    **download_center**         --  returns the instance of the `DownloadCenter` class,
    to interact with the download center repositories deployed on the Commcell WebConsole

    **organizations**           --  returns the instance of the `Organizations` class,
    to interact with the organizations/companies added on the Commcell

    **storage_pools**           --  returns the instance of the `StoragePools` class,
    to interact with the storage pools added to the Commcell Admin Console

    **monitoring_policies**     --  returns the instance of the `MonitoringPolicies` class,
    to interact with the MonitoringPolicies added to the Commcell

    **operation_window**        -- returns the instance of the 'OperationWindow' class,
    to interact with the opeartion windows of commcell

    **array_management**        --  returns the instance of the `ArrayManagement` class,
    to perform SNAP related operations on the Commcell

    **activity_control**        --  returns the instance of the `ActivityControl` class,
    to interact with the Activity Control on the Commcell

    **event_viewer**            --  returns the instance of the `Events` class,
    to interact with the Events associated on the Commcell

    **disasterrecovery**    -- returns the instance of the 'DisasterRecovery' class,
    to run disaster recovery backup , restore operations.

    **commserv_client**         --  returns the client object associated with the
    commserver

    **identity_management**     --  returns the instance of the 'IdentityManagementApps
    class to perform identity management operations on the commcell class

    **system**                  --  returns the instance of the 'System' class to perform
    system related operations on the commcell

    **commcell_migration**      --  returns the instance of the 'CommCellMigration' class,
    to interact with the Commcell Export & Import on the Commcell

    **grc**      --  returns the instance of the 'GlobalRepositoryCell' class,
    to interact with the registered commcells and setup/modify GRC schedules

    **service_commcells**       --  returns the instance of the `ServiceCommcells` class, to
    perform service commcell related operations

    **backup_network_pairs**    --  returns the instance of 'BackupNetworkPairs' class to
    perform backup network pairs operations on the commcell class

    **recovery_targets**        -- Returns the instance of RecoverTargets class

    **cleanroom_targets**       -- -- Returns the instance of CleanroomTargets class

    **reports**                 --  Return the instance of Report class

    **job_management**          --  Returns an instance of the JobManagement class.

    **hac_clusters**            --  Returns an instance of the HAC Clusters class

    **network_topologies**      --  Returns an instance of NetworkTopologies class

    **index_pools**             --  Returns an instance of the IndexPools class

    **deduplications_engines    --  Returns the instance of the DeduplicationEngines class
    to interact with deduplication engines available on the commcell

    **two_factor_authentication**   --  Returns an instance of the TwoFactorAuthentication class.

    **is_tfa_enabled**              --  Returns the status of tfa on this commcell.

    **tfa_enabled_user_groups**     -- Returns user group names on which tfa is enabled.
    only for user group inclusion tfa.

    **tags                          -- Returns the instance of entity tags class

    **is_linux_commserv**           -- boolean specifying if CommServer is installed on linux cs.

    **default_timezone**            -- Default timezone used by all the operations performed via cvpysdk.

    **metallic**                 -- Returns the instance of CVMetallic class

    **key_management_servers**      -- Returns the instance of `KeyManagementServers` class

    **is_passkey_enabled**          -- Returns True if Passkey is enabled on commcell

    **databases**                    -- Returns the list of databases on the commcell

    **database_instances**           -- Returns the list of database instances on the commcell

    **database_instant_clones**      -- Returns the list of database instant clone jobs active on the commcell

    **cost_assessment**             -- Returns the instance of the CostAssessment class

    **azure_discovery**          -- Returns the instance of the AzureDiscovery class

    **aws_discovery**            -- Returns the instance of the AWSDiscovery class

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import getpass
import socket
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

import requests
import xmltodict

from base64 import b64encode

from requests.exceptions import SSLError
from requests.exceptions import Timeout

# ConnectionError is a built-in exception, do not override it
from requests.exceptions import ConnectionError as RequestsConnectionError

from .activate import Activate
from .activateapps.compliance_utils import ExportSets
from .clouddiscovery.cloud_discovery import AzureDiscovery, AWSDiscovery
from .constants import UserRole
from .activateapps.tco import CostAssessment
from .services import get_services
from .cvpysdk import CVPySDK
from .client import Clients, Client
from .monitoringapps.threat_indicators import TAServers
from .alert import Alerts
from .snmp_configs import SNMPConfigurations
from .storage import MediaAgents
from .storage import DiskLibraries
from .storage import TapeLibraries
from .security.usergroup import UserGroups, UserGroup
from .domains import Domains, Domain
from .tags import Tags
from .workflow import WorkFlows
from .exception import SDKException
from .clientgroup import ClientGroups
from .globalfilter import GlobalFilters
from .datacube.datacube import Datacube
from .content_analyzer import ContentAnalyzers
from .scale_target import ScaleTargets
from .network_topology import NetworkTopologies
from .plan import Plans
from .job import JobController, Job
from .security.user import Users, User
from .security.role import Roles
from .security.two_factor_authentication import TwoFactorAuthentication
from .credential_manager import Credentials
from .download_center import DownloadCenter
from .resource_pool import ResourcePools
from .organization import Organizations, Organization
from .storage_pool import StoragePools
from .monitoring import MonitoringPolicies
from .policy import Policies
from .policies.storage_policies import StoragePolicies
from .policies.schedule_policies import SchedulePolicies
from .schedules import SchedulePattern
from .schedules import Schedules
from .activitycontrol import ActivityControl
from .eventviewer import Events
from .array_management import ArrayManagement
from .disasterrecovery import DisasterRecovery
from .operation_window import OperationWindow
from .identity_management import IdentityManagementApps
from .system import System
from .commcell_migration import CommCellMigration, GlobalRepositoryCell
from .deployment.download import Download
from .deployment.cache_config import CommServeCache
from .deployment.cache_config import RemoteCache
from .deployment.install import Install
from .name_change import NameChange
from .backup_network_pairs import BackupNetworkPairs
from .reports.report import Report
from .recovery_targets import RecoveryTargets
from .cleanroom.target import CleanroomTargets
from .cleanroom.recovery_groups import RecoveryGroups
from .drorchestration.replication_groups import ReplicationGroups
from .drorchestration.failovergroups import FailoverGroups
from .drorchestration.blr_pairs import BLRPairs
from .job import JobManagement
from .index_server import IndexServers
from .hac_clusters import HACClusters
from .index_pools import IndexPools
from .deduplication_engines import DeduplicationEngines
from .metallic import Metallic
from .key_management_server import KeyManagementServers
from .regions import Regions
from .service_commcells import ServiceCommcells
from urllib.parse import urlparse

USER_LOGGED_OUT_MESSAGE = 'User Logged Out. Please initialize the Commcell object again.'
USER_DOES_NOT_HAVE_PERMISSION = "User does not have permission on commcell properties"
"""str:     Message to be returned to the user, when trying the get the value of an attribute
of the Commcell class, after the user was logged out.

"""


class Commcell(object):
    """
    Class for establishing and managing a session to the Commcell via Commvault REST API.

    The Commcell class provides a comprehensive interface for interacting with a Commcell environment,
    enabling session management, resource access, configuration, and administrative operations through
    the Commvault REST API. It supports authentication, resource querying, configuration management,
    software deployment, user and role management, reporting, and advanced features such as privacy,
    multi-tenancy, disaster recovery, and global scope operations.

    Key Features:
        - Session management and authentication (including SAML, two-factor, passkey, privacy)
        - Resource access via properties for clients, media agents, storage policies, workflows, alerts, etc.
        - Administrative operations: user, role, group, domain, organization, and company management
        - Software management: download, copy, install, push service packs/hotfixes
        - Configuration management: global parameters, additional settings, email, navigation, SLA, workload region
        - Security and compliance: owner assignment verification, password encryption, security associations
        - Disaster recovery, replication, failover, and cleanroom recovery group management
        - Reporting and monitoring: job controller, reports, event viewer, monitoring policies
        - Advanced features: global scope switching, operator company management, cost assessment
        - Utility methods for sending mail, executing QCommands, and custom REST requests
        - Support for cache management, remote cache synchronization, and protected VM queries
        - Extensive property access for Commcell metadata, versioning, and system details

    This class is intended for use by administrators and integrators who need to automate, monitor,
    or manage Commcell environments programmatically.

    #ai-gen-doc
    """

    def __init__(
            self,
            webconsole_hostname: str,
            commcell_username: str = None,
            commcell_password: str = None,
            authtoken: str = None,
            force_https: bool = False,
            certificate_path: str = None,
            is_service_commcell: bool = None,
            verify_ssl: bool = True,
            **kwargs
        ) -> None:
        """Initialize a Commcell object for API operations.

        This constructor sets up a Commcell session using the provided connection and authentication details.
        You can authenticate using a username/password, a QSDK/SAML token, or interactively if neither is provided.
        Additional options allow for HTTPS enforcement, SSL certificate verification, and service commcell login.

        Args:
            webconsole_hostname: Hostname or IP address of the Commcell Web Console (e.g., 'webclient.company.com' or '192.168.1.100').
            commcell_username: Username for logging into the Commcell console. Optional if using a token.
            commcell_password: Plain-text password for the Commcell user. Optional if using a token.
            authtoken: QSDK or SAML token for authentication. If provided, username and password are not required.
            force_https: If True, only HTTPS connections are attempted; if False, will fall back to HTTP if HTTPS fails. Default is False.
            certificate_path: Path to a CA_BUNDLE file or directory with trusted CA certificates. If provided, force_https is set to True.
            is_service_commcell: Set to True to log in to a service (child) commcell, or False for a normal login. Default is None.
            verify_ssl: Whether to verify SSL certificates for requests to the Commcell. Default is True.
            **kwargs: Additional keyword arguments:
                - web_service_url (str): URL of the web service for API requests.
                - user_agent (str): User agent header for requests.
                - master_commcell ('Commcell'): Instance of the master Commcell object (for multi-Commcell scenarios).
                - master_hostname (str): Hostname of the master Commcell for authentication if master_commcell is not provided.
                - trace_parent (str): W3C Trace Context header string in the format:
                    '00-<trace-id>-<span-id>-<trace-flags>'.

        Raises:
            SDKException: If the web service is unreachable or no authentication token is received.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(
            ...     webconsole_hostname='webclient.company.com',
            ...     commcell_username='admin',
            ...     commcell_password='password',
            ...     verify_ssl=False
            ... )
            >>> print("Commcell session established successfully")
            >>> # For SAML/QSDK token authentication:
            >>> commcell = Commcell(
            ...     webconsole_hostname='webclient.company.com',
            ...     authtoken='your_saml_token'
            ... )
            >>> # For service commcell login:
            >>> commcell = Commcell(
            ...     webconsole_hostname='webclient.company.com',
            ...     commcell_username='admin',
            ...     commcell_password='password',
            ...     is_service_commcell=True
            ... )

        #ai-gen-doc
        """
        web_service_url = kwargs.get("web_service_url", None)
        web_service = []
        
        if certificate_path:
            force_https = True
            
        if not web_service_url:
            web_service = [
				r'https://{0}/commandcenter/api/'.format(webconsole_hostname)
			]

            if force_https is False:
                web_service.append(r'http://{0}/commandcenter/api/'.format(webconsole_hostname))
        else:
            web_service = []
            if web_service_url.startswith("https://") or web_service_url.startswith("http://"):
                web_service.append(r'{0}/'.format(web_service_url))
            else:
                web_service.append(r'https://{0}/'.format(web_service_url))
                if force_https is False:
                    web_service.append(r'http://{0}/'.format(web_service_url))

        self._user = commcell_username

        self._password = None

        self._user_agent = kwargs.get('user_agent')

        self._headers = {
            'Host': webconsole_hostname,
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authtoken': None
        }
        if self._user_agent:
            self._headers['User-Agent'] = self._user_agent
        
        if web_service_url:
            parsed_web_service_url = urlparse(web_service_url)
            self._headers['Host'] = f"{parsed_web_service_url.netloc}"

        self._device_id = socket.getfqdn()

        if idp_hostname := kwargs.get("master_hostname"):
            self._master_commcell = Commcell(
                idp_hostname, commcell_username, commcell_password, authtoken,
                force_https, certificate_path, False, verify_ssl
            )
        else:
            self._master_commcell = kwargs.get("master_commcell")

        if self._master_commcell:
            is_service_commcell = True
            authtoken = self._master_commcell.get_saml_token()

        self._is_service_commcell = is_service_commcell

        # Checks if the service is running or not
        for service in web_service:
            self._web_service = service
            try:
                trace_parent = kwargs.get('trace_parent')
                if service.startswith("http:"):
                    # if force_https is false and if verify_ssl is true, we still allow HTTP calls to be made.
                    # since verify_ssl is set, the calls for http is failing. Below change allow http calls to be made
                    verify_ssl = False
                    self._cvpysdk_object = CVPySDK(self, certificate_path, verify_ssl, trace_parent=trace_parent)
                else:
                    self._cvpysdk_object = CVPySDK(self, certificate_path, verify_ssl, trace_parent=trace_parent)
                if self._cvpysdk_object._is_valid_service():
                    break
            except (RequestsConnectionError, SSLError, Timeout):
                if force_https:
                    raise
        else:
            raise SDKException('Commcell', '101', f'[{webconsole_hostname}]')

        # Initialize all the services with this commcell service
        self._services = get_services(self._web_service)

        validity_err = None
        self._is_saml_login = False

        if isinstance(commcell_password, dict):
            authtoken = commcell_password['Authtoken']

        if authtoken and not is_service_commcell:
            if authtoken.startswith('QSDK ') or authtoken.startswith('SAML ') or authtoken.startswith('Bearer '):
                self._headers['Authtoken'] = authtoken
            else:
                self._headers['Authtoken'] = '{0}{1}'.format('QSDK ', authtoken)

            try:
                self._is_saml_login = True if authtoken.startswith('SAML ') else False
                self._user = self._cvpysdk_object.who_am_i()
            except SDKException as error:
                self._headers['Authtoken'] = None
                validity_err = error

        if not self._headers['Authtoken'] and commcell_username is not None:
            if commcell_password is None:
                commcell_password = getpass.getpass('Please enter the Commcell Password: ')

            self._password = b64encode(commcell_password.encode()).decode()
            # Login to the commcell with the credentials provided
            # and store the token in the headers
            self._headers['Authtoken'] = self._cvpysdk_object._login()

        if self.is_service_commcell and authtoken is not None and authtoken.startswith('SAML '):
            self._master_saml_token = authtoken
            self._headers['Authtoken'] = self._cvpysdk_object._login()
            self._user = self._cvpysdk_object.who_am_i()
        if not self._headers['Authtoken']:
            if isinstance(validity_err, Exception):
                raise validity_err

            raise SDKException('Commcell', '102')

        self._master_saml_token = None
        self._commserv_name = None
        self._commserv_hostname = None
        self._commserv_timezone = None
        self._commserv_timezone_name = None
        self._commserv_guid = None
        self._commserv_version = None
        self._version_info = None
        self._release_name = None
        self._is_linux_commserv = None
        self._commserv_metadata = None
        self._commserv_oem_id = None
        self._user_mappings = None
        self._user_role = None
        self._user_org = None

        self._id = None
        self._clients = None
        self._commserv_cache = None
        self._remote_cache = None
        self._media_agents = None
        self._workflows = None
        self._disaster_recovery = None
        self._alerts = None
        self._disk_libraries = None
        self._tape_libraries = None
        self._storage_policies = None
        self._schedule_policies = None
        self._schedules = None
        self._policies = None
        self._user_groups = None
        self._domains = None
        self._client_groups = None
        self._global_filters = None
        self._datacube = None
        self._activate = None
        self._export_sets = None
        self._content_analyzers = None
        self._scale_targets = None
        self._resource_pool = None
        self._plans = None
        self._job_controller = None
        self._users = None
        self._roles = None
        self._credentials = None
        self._download_center = None
        self._organizations = None
        self._storage_pools = None
        self._activity_control = None
        self._events = None
        self._monitoring_policies = None
        self._array_management = None
        self._operation_window = None
        self._commserv_client = None
        self._identity_management = None
        self._system = None
        self._commcell_migration = None
        self._grc = None
        self._registered_commcells = None
        self._backup_network_pairs = None
        self._reports = None
        self._replication_groups = None
        self._failover_groups = None
        self._recovery_targets = None
        self._recovery_groups = None
        self._cleanroom_targets = None
        self._threat_indicators = None
        self._blr_pairs = None
        self._job_management = None
        self._index_servers = None
        self._hac_clusters = None
        self._nw_topo = None
        self._index_pools = None
        self._deduplication_engines = None
        self._tfa = None
        self._metallic = None
        self._kms = None
        self._privacy = None
        self._commcell_properties = None
        self._regions = None
        self._snmp_configurations = None
        self._tags = None
        self._additional_settings = None
        self._service_commcells = None
        self._databases = None
        self._database_instances = None
        self._database_instant_clones = None
        self._cost_assessment = None
        self._azure_discovery = None
        self._aws_discovery = None
        self._commserv_details_loaded = False
        self._commserv_details_set = False
        self._job_logs_emails = []
        self.refresh()

        del self._password

    def __repr__(self) -> str:
        """Return a string representation of the Commcell instance.

        This method provides a human-readable string that describes the Commcell object,
        which can be useful for debugging or logging purposes.

        Returns:
            A string containing details about the Commcell class instance.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> print(repr(commcell))
            Commcell(hostname='hostname', user='username')

        #ai-gen-doc
        """
        rep =  (f'Commcell class instance '
                f'of Commcell: [{self.webconsole_hostname}] '
                f'for User: [{self.commcell_username}]')
        if self.is_global_scope():
            rep += ' in Global Scope'
        if self.operating_company:
            rep += f' operating on Company: [{self.operating_company}]'
        return rep

    def __enter__(self) -> 'Commcell':
        """Enter the runtime context related to this Commcell instance.

        This method enables the use of the Commcell object as a context manager,
        allowing resource management using the `with` statement.

        Returns:
            Commcell: The current Commcell instance.

        Example:
            >>> with Commcell('hostname', 'username', 'password') as cc:
            ...     print("Connected to Commcell:", cc)
            >>> # The Commcell connection is automatically managed within the context

        #ai-gen-doc
        """
        return self

    def __exit__(self, exception_type: type, exception_value: BaseException, traceback: object) -> None:
        """Handle cleanup when exiting a context, logging out the user associated with this Commcell instance.

        This method is called automatically when using the Commcell object as a context manager
        (i.e., within a `with` statement). It ensures that the user session is properly logged out
        when the context is exited, regardless of whether an exception occurred.

        Args:
            exception_type: The exception type, if an exception was raised, otherwise None.
            exception_value: The exception instance, if an exception was raised, otherwise None.
            traceback: The traceback object, if an exception was raised, otherwise None.

        Example:
            >>> with Commcell('hostname', 'username', 'password') as commcell:
            ...     # Perform operations with commcell
            ...     pass
            # Upon exiting the 'with' block, the user is automatically logged out

        #ai-gen-doc
        """
        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def _update_response_(self, input_string: str) -> str:
        """Extract and return the relevant portion of the server response.

        This method processes the input string received from the server and returns only the relevant
        part of the response that should be used for further operations.

        Args:
            input_string: The raw response string received from the server.

        Returns:
            The processed string containing only the relevant response data.

        Example:
            >>> response = commcell._update_response_("{'response': 'success', 'data': {...}}")
            >>> print(response)
            {'response': 'success', 'data': {...}}

        #ai-gen-doc
        """
        if '<title>' in input_string and '</title>' in input_string:
            response_string = input_string.split("<title>")[1]
            response_string = response_string.split("</title>")[0]
            return response_string

        return input_string

    def _remove_attribs_(self) -> None:
        """Remove all attributes associated with this Commcell instance.

        This method clears all attributes from the current Commcell object, effectively resetting its state.
        Use with caution, as this will remove all data and configuration stored in the instance.

        Example:
            >>> commcell = Commcell()
            >>> commcell._remove_attribs_()
            >>> # All attributes of commcell are now removed

        #ai-gen-doc
        """
        del self._clients
        del self._commserv_cache
        del self._remote_cache
        del self._media_agents
        del self._workflows
        del self._alerts
        del self._disk_libraries
        del self._tape_libraries
        del self._storage_policies
        del self._schedule_policies
        del self._schedules
        del self._user_groups
        del self._policies
        del self._domains
        del self._roles
        del self._credentials
        del self._client_groups
        del self._global_filters
        del self._datacube
        del self._activate
        del self._content_analyzers
        del self._resource_pool
        del self._plans
        del self._job_controller
        del self._users
        del self._download_center
        del self._organizations
        del self._storage_pools
        del self._recovery_targets
        del self._cleanroom_targets
        del self._threat_indicators
        del self._replication_groups
        del self._blr_pairs
        del self._activity_control
        del self._events
        del self._monitoring_policies
        del self._array_management
        del self._operation_window
        del self._commserv_client
        del self._identity_management
        del self._system
        del self._web_service
        del self._cvpysdk_object
        del self._device_id
        del self._services
        del self._disaster_recovery
        del self._commcell_migration
        del self._grc
        del self._backup_network_pairs
        del self._job_management
        del self._index_servers
        del self._hac_clusters
        del self._nw_topo
        del self._index_pools
        del self._deduplication_engines
        del self._is_service_commcell
        del self._master_saml_token
        del self._tfa
        del self._metallic
        del self._kms
        del self._tags
        del self

    def _set_commserv_details(self, commcell_info: object) -> None:
        """Set the CommServ details for this Commcell instance.

        This method updates the Commcell object with information from the provided
        commcell_info object, which typically contains configuration or connection
        details for the CommServ server.

        Args:
            commcell_info: An object containing CommServ information to be set on the Commcell instance.

        Example:
            >>> commcell_info = get_commcell_info_from_source()
            >>> commcell._set_commserv_details(commcell_info)
            >>> # The Commcell instance now has updated CommServ details

        #ai-gen-doc
        """
        self._commserv_guid = commcell_info.commserv_guid
        self._commserv_hostname = commcell_info.commserv_hostname
        self._commserv_name = commcell_info.commserv_name
        self._commserv_timezone = commcell_info.commserv_timezone
        self._commserv_timezone_name = commcell_info.commserv_timezone_name
        self._commserv_version = commcell_info.commserv_version
        self._version_info = commcell_info.version
        self._id = commcell_info.commserv_id
        self._release_name = commcell_info.release_name
        self._commserv_details_loaded = True
        self._commserv_details_set = True

    def _get_commserv_details(self) -> None:
        """Retrieve and update CommServ details for the current Commcell instance.

        This method fetches the details of the CommServ associated with the Commcell object
        and updates the relevant attributes of the class instance. It is typically called
        during initialization to ensure the Commcell object has up-to-date information about
        the connected CommServ.

        Raises:
            SDKException: If the CommServ details cannot be retrieved, if the response is empty,
                or if the response indicates a failure.

        Example:
            >>> commcell = Commcell('commserv_host', 'username', 'password')
            >>> commcell._get_commserv_details()
            >>> # The commcell instance now has updated CommServ details

        #ai-gen-doc
        """
        import re

        flag, response = self._cvpysdk_object.make_request('GET', self._services['COMMSERV'])

        if flag:
            if response.json():
                try:
                    self._commserv_guid = response.json()['commcell'].get('csGUID')
                    self._commserv_hostname = response.json()['hostName']
                    self._commserv_name = response.json()['commcell']['commCellName']
                    self._commserv_timezone_name = response.json()['csTimeZone']['TimeZoneName']
                    self._commserv_version = response.json()['currentSPVersion']
                    version_info = response.json().get('csVersionInfo')
                    self._id = response.json()['commcell']['commCellId']
                    self._release_name = response.json().get('releaseName')

                    try:
                        self._commserv_timezone = re.search(
                            r'\(.*', response.json()['timeZone']
                        ).group()
                    except:
                        # in case where timezone string might be missing strings like
                        # (UTC+5:30) substitute the prepending strings like 0:-300: with ''
                        self._commserv_timezone = re.sub(
                            r'^([+|-]*\d*:)*', '', response.json()['timeZone']
                        )

                    # set commcell version (E.g. 11.21.0)
                    version_replace_strings = {
                        '.0 SP': '.',
                        ' SP': '.',
                        ' HPK': '.',
                        '+': '',
                        '-': '',
                        'a': '.1',
                        'b': '.2'
                    }

                    for key, value in version_replace_strings.items():
                        version_info = version_info.replace(key, value)

                    self._version_info = version_info + '.0' * (3 - len(version_info.split('.')))
                    self._commserv_details_loaded = True

                except KeyError as error:
                    raise SDKException('Commcell', '103', 'Key does not exist: {0}'.format(error))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text) + 
                               ". You may need to provide View Commcell permission to the logged-in user. ")

    def _qoperation_execute(self, request_xml: str, return_xml: bool = False) -> dict:
        """Execute a qoperation REST API call with the provided XML request.

        This method sends a qoperation execute request to the Commcell server using the specified XML payload.
        The response can be returned either as a JSON dictionary (default) or as raw XML, depending on the
        value of `return_xml`.

        Args:
            request_xml: The XML string to be sent in the qoperation execute request.
            return_xml: If True, returns the response as an XML string instead of a JSON dictionary.

        Returns:
            dict: The JSON response received from the server if `return_xml` is False.
            If `return_xml` is True, the response will be returned as an XML string.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        Example:
            >>> xml_request = "<EVGui_GetAllClientsRequest/>"
            >>> response = commcell._qoperation_execute(xml_request)
            >>> print(response)
            >>> # To get the response as XML:
            >>> xml_response = commcell._qoperation_execute(xml_request, return_xml=True)
            >>> print(xml_response)

        #ai-gen-doc
        """
        accept_type_initial = self._headers['Accept']
        if return_xml:
            self._headers['Accept'] = 'application/xml'

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.ok:
                try:
                    if return_xml:
                        self._headers['Accept'] = accept_type_initial # reset initial accept type
                        return response.text
                    return response.json()
                except ValueError:
                    return {'output': response}
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def qoperation_execute(self, request_xml: str, **kwargs: dict) -> dict:
        """Execute a QOperation request on the Commcell server.

        This method sends the provided XML request to the Commcell server using the QOperation API.
        Optionally, you can specify `return_xml=True` in kwargs to receive the raw XML response
        instead of the default JSON response.

        Args:
            request_xml: The XML string representing the QOperation request to be executed.
            **kwargs: Optional keyword arguments.
                - return_xml (bool): If True, returns the response as XML instead of JSON.

        Returns:
            dict: The JSON response received from the server, unless `return_xml=True` is specified.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        Example:
            >>> xml_request = "<EVGui_GetAllClientsReq/>"
            >>> response = commcell_obj.qoperation_execute(xml_request)
            >>> print(response)
            >>> # To get the response as XML:
            >>> xml_response = commcell_obj.qoperation_execute(xml_request, return_xml=True)
            >>> print(xml_response)

        #ai-gen-doc
        """

        return self._qoperation_execute(request_xml, **kwargs)

    @staticmethod
    def _convert_days_to_epoch(days: int) -> tuple:
        """Convert a number of days to a tuple of epoch timestamps.

        This static method calculates the start and end times in Unix epoch format,
        where the start time is the current time minus the specified number of days,
        and the end time is the current time.

        Args:
            days: The number of days to subtract from the current time to determine the start time.

        Returns:
            A tuple (from_time, to_time):
                from_time: The epoch timestamp representing 'days' ago from now.
                to_time: The current epoch timestamp.

        Example:
            >>> from_time, to_time = Commcell._convert_days_to_epoch(7)
            >>> print(f"Start time (7 days ago): {from_time}")
            >>> print(f"End time (now): {to_time}")

        #ai-gen-doc
        """
        import datetime
        import time
        now = datetime.datetime.now()
        then = now - datetime.timedelta(days=days)
        start_dt = int(time.mktime(then.timetuple()))
        end_dt = int(time.mktime(now.timetuple()))
        return start_dt, end_dt

    @property
    def commcell_id(self) -> int:
        """Get the unique identifier (ID) of the CommCell.

        Returns:
            int: The CommCell's unique ID.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> cc_id = commcell.commcell_id  # Use dot notation for property access
            >>> print(f"CommCell ID: {cc_id}")

        #ai-gen-doc
        """
        if self._id is None:
            self._get_commserv_details()
        return self._id

    def _qoperation_execscript(self, arguments: str) -> dict:
        """Execute a qscript on the Commcell using qoperation with the specified arguments.

        Args:
            arguments: The arguments to be passed to the qscript as a string.

        Returns:
            dict: The JSON response received from the server after executing the script.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        Example:
            >>> response = commcell._qoperation_execscript("-script_name MyScript -param1 value1")
            >>> print(response)
            {'status': 'success', 'result': {...}}

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QSCRIPT'] % arguments)

        if flag:
            if response.ok:
                try:
                    return response.json()
                except ValueError:
                    return {'output': response.text}
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_gxglobalparam_value(self, parameters: Union[str, List[str]]) -> Union[Optional[str], List[Any]]:
        """Retrieve values from GXGlobalParam for the specified parameter(s).

        This method makes a REST API call to fetch the value(s) of one or more parameters from GXGlobalParam.
        If a single parameter name is provided as a string, the corresponding value is returned as a string (or None if not found).
        If a list of parameter names is provided, a list of values is returned.

        Args:
            parameters: The name of the parameter as a string, or a list of parameter names to retrieve values for.

        Returns:
            If `parameters` is a string:
                The value of the specified parameter as a string, or None if the parameter is not found.
            If `parameters` is a list:
                A list containing the values of the specified parameters.

        Raises:
            SDKException: If the response is empty or the API call is not successful.

        Example:
            >>> # Retrieve a single parameter value
            >>> value = commcell.get_gxglobalparam_value('MyParam')
            >>> print(f"Value for 'MyParam': {value}")

            >>> # Retrieve multiple parameter values
            >>> values = commcell.get_gxglobalparam_value(['Param1', 'Param2'])
            >>> print(f"Values: {values}")

        #ai-gen-doc
        """

        parameters_orig = parameters
        if isinstance(parameters, str):
            parameters = [parameters]

        if not isinstance(parameters, list):
            raise SDKException('Commcell', '107')

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GET_GLOBAL_PARAM'], {
                'globalParamsRequestList': parameters
            }
        )

        if flag:
            if response.json():
                param_results = response.json().get('globalParamsResultList')

                # If requested parameter is a string, then return the single value directly instead of the list response
                if isinstance(parameters_orig, str):
                    for param_result in param_results:
                        if param_result.get('name').lower() == parameters_orig.lower():
                            return param_result.get('value')

                    # Return None if the requested parameter is not found in the response
                    return None

                return param_results
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_gxglobalparam_value(self, request_json: 'Union[Dict[str, str], List[Dict[str, str]]]') -> dict:
        """Update the GXGlobalParam table with Commcell-level configuration parameters.

        This method updates configuration parameters at the Commcell level by sending the provided
        request JSON to the server. The input can be a single parameter dictionary or a list of such
        dictionaries for batch updates.

        Args:
            request_json: A dictionary representing a single global parameter setting, or a list of such
                dictionaries for multiple settings.
                Example (single parameter):
                    {
                        "name": "EnableFeatureX",
                        "value": "True"
                    }
                Example (multiple parameters):
                    [
                        {"name": "EnableFeatureX", "value": "True"},
                        {"name": "MaxBackupStreams", "value": "8"}
                    ]

        Returns:
            dict: The JSON response received from the server after updating the parameters.

        Raises:
            SDKException: If the server response is empty or indicates a failure.

        Example:
            >>> # Update a single global parameter
            >>> response = commcell._set_gxglobalparam_value({"name": "EnableFeatureX", "value": "True"})
            >>> print(response)
            >>> # Update multiple global parameters
            >>> params = [
            ...     {"name": "EnableFeatureX", "value": "True"},
            ...     {"name": "MaxBackupStreams", "value": "8"}
            ... ]
            >>> response = commcell._set_gxglobalparam_value(params)
            >>> print(response)

        #ai-gen-doc
        """
        if isinstance(request_json, list):
            global_params_list = request_json
            payload = {
                "App_SetGlobalParamsReq": {
                    "globalParams": global_params_list
                }
            }
            return self.qoperation_execute(payload)

        if not isinstance(request_json, dict):
            message = f"Received: {type(request_json)}. Expected: dict, list"
            raise SDKException('Commcell', 107, message)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['SET_GLOBAL_PARAM'], request_json
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def verify_owner_assignment_config(self) -> dict:
        """Verify that the ownership assignment settings are configured and set properly.

        This method checks the current ownership assignment configuration on the Commcell
        and ensures that all required settings are present and correctly set.

        Returns:
            dict: The JSON response received from the server containing the ownership assignment configuration details.

        Raises:
            SDKException: If the response is empty, not successful, or if the ownership assignment is not correct.

        Example:
            >>> commcell = Commcell()
            >>> config_status = commcell.verify_owner_assignment_config()
            >>> print(config_status)
            >>> # The output will be a dictionary with the configuration details

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            "GET", self._services["SET_COMMCELL_PROPERTIES"]
        )

        if flag:
            try:
                return response.json()
            except ValueError:
                return {'output': response}
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def commserv_guid(self) -> str:
        """Get the GUID (Globally Unique Identifier) of the CommServ.

        Returns:
            The GUID of the CommServ as a string.

        Example:
            >>> commcell = Commcell()
            >>> guid = commcell.commserv_guid  # Use dot notation for property access
            >>> print(f"CommServ GUID: {guid}")

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_guid

    @property
    def commserv_hostname(self) -> str:
        """Get the hostname of the CommServ server associated with this Commcell.

        Returns:
            The hostname of the CommServ as a string.

        Example:
            >>> commcell = Commcell()
            >>> hostname = commcell.commserv_hostname  # Use dot notation for property access
            >>> print(f"CommServ Hostname: {hostname}")

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_hostname

    @property
    def commserv_name(self) -> str:
        """Get the name of the CommServ associated with this Commcell.

        Returns:
            The name of the CommServ as a string.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> name = commcell.commserv_name  # Use dot notation for property access
            >>> print(f"CommServ name: {name}")

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_name

    @property
    def commserv_timezone(self) -> str:
        """Get the time zone setting of the CommServ.

        Returns:
            The time zone of the CommServ as a string.

        Example:
            >>> commcell = Commcell()
            >>> timezone = commcell.commserv_timezone  # Use dot notation for property access
            >>> print(f"CommServ time zone: {timezone}")

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_timezone

    @property
    def commserv_timezone_name(self) -> str:
        """Get the name of the time zone configured for the CommServ.

        Returns:
            The name of the CommServ's time zone as a string.

        Example:
            >>> commcell = Commcell()
            >>> timezone = commcell.commserv_timezone_name
            >>> print(f"CommServ time zone: {timezone}")

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_timezone_name

    @property
    def commserv_version(self) -> int:
        """Get the major version number installed on the CommServ.

        Returns:
            The major version of the CommServe installation as an integer.

        Example:
            >>> commcell = Commcell()
            >>> version = commcell.commserv_version  # Use dot notation for property
            >>> print(f"CommServe version: {version}")
            # Output might be: CommServe version: 19

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_version

    @property
    def version(self) -> str:
        """Get the complete version information of the CommServe.

        Returns:
            The full version string of the CommServe, such as "11.19.1".

        Example:
            >>> commcell = Commcell()
            >>> version_info = commcell.version
            >>> print(f"CommServe version: {version_info}")
            CommServe version: 11.19.1

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._version_info

    @property
    def release_name(self) -> str:
        """Get the complete release name of the CommServe.

        Returns:
            The release name of the CommServe as a string (e.g., "2024E").

        Example:
            >>> commcell = Commcell()
            >>> release = commcell.release_name
            >>> print(f"CommServe release: {release}")
            CommServe release: 2024E

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._release_name

    @property
    def webconsole_hostname(self) -> str:
        """Get the host name of the Web Console used to connect to the Commcell.

        Returns:
            The host name of the Web Console as a string.

        Example:
            >>> commcell = Commcell()
            >>> hostname = commcell.webconsole_hostname
            >>> print(f"Web Console Hostname: {hostname}")

        #ai-gen-doc
        """
        return self._headers['Host']

    @property
    def auth_token(self) -> str:
        """Get the authentication token for the current Commcell session.

        Returns:
            str: The authentication token (Authtoken) associated with the current session.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> token = commcell.auth_token  # Use dot notation for property access
            >>> print(f"Current session token: {token}")

        #ai-gen-doc
        """
        return self._headers['Authtoken']

    @property
    def commcell_username(self) -> str:
        """Get the username of the currently logged-in Commcell user.

        Returns:
            The username as a string.

        Example:
            >>> commcell = Commcell()
            >>> username = commcell.commcell_username  # Use dot notation for property access
            >>> print(f"Logged in as: {username}")
        #ai-gen-doc
        """
        return self._user

    @property
    def user_mappings(self) -> dict:
        """Get the user mappings for the currently logged-in user.

        Returns:
            dict: A dictionary containing user mapping information for the active session.

        Example:
            >>> commcell = Commcell()
            >>> mappings = commcell.user_mappings
            >>> print(mappings)
            {'userName': 'admin', 'role': 'Master', 'groups': ['Administrators', 'BackupOperators']}
        #ai-gen-doc
        """
        if self._user_mappings is None:
            self._user_mappings = self.wrap_request('GET', 'USER_MAPPINGS')
        return self._user_mappings

    @property
    def user_role(self) -> 'UserRole':
        """Get the user role enum for the currently logged-in user.

        Returns:
            UserRole: The role of the user currently authenticated in the Commcell session.
            This can be values such as UserRole.MSP_ADMIN, UserRole.MSP_USER, etc.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> role = commcell.user_role
            >>> print(f"Current user role: {role}")

        #ai-gen-doc
        """
        if self._user_role is None:
            self._user_role = UserRole(self.user_mappings.get('userRole', 5))
        return self._user_role

    @property
    def is_tenant(self) -> bool:
        """Check if the logged-in user is a company (tenant) user.

        Returns:
            True if the current user is a company (tenant) user, False otherwise.

        Example:
            >>> commcell = Commcell()
            >>> if commcell.is_tenant:
            ...     print("User is a tenant user")
            ... else:
            ...     print("User is not a tenant user")

        #ai-gen-doc
        """
        return self.user_role in [UserRole.TENANT_USER, UserRole.TENANT_ADMIN]

    @property
    def is_tenant_level(self) -> bool:
        """Check if the logged-in user is at the company (tenant) level.

        Returns:
            True if the current user session is authenticated at the company (tenant) level, False otherwise.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> if commcell.is_tenant_level:
            ...     print("User is at tenant level")
            ... else:
            ...     print("User is not at tenant level")

        #ai-gen-doc
        """
        return bool(self.is_tenant or self.operating_company)

    @property
    def user_org(self) -> Optional['Organization']:
        """Get the organization object that the currently logged-in user belongs to.

        Note:
            Update operations on the returned organization object may fail depending on the user's role and permissions.

        Returns:
            The Organization object associated with the current user, or None if the user does not belong to any organization.

        Example:
            >>> commcell = Commcell()
            >>> org = commcell.user_org
            >>> if org is not None:
            ...     print(f"User belongs to organization: {org.name}")
            >>> else:
            ...     print("User does not belong to any organization.")

        #ai-gen-doc
        """
        if 'providerId' not in self.user_mappings:
            return None
        if self._user_org is None:
            self._user_org = Organization(self, organization_id=self.user_mappings['providerId'])
            # need to directly use Organization class here, as /Organizations API may be restricted
            # but GET /Organization/{org_id} API response is always provided to all users
        return self._user_org

    @property
    def device_id(self) -> int:
        """Get the value of the Device ID attribute for this Commcell.

        Returns:
            The Device ID as an integer.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> device_id = commcell.device_id
            >>> print(f"Commcell Device ID: {device_id}")

        #ai-gen-doc
        """
        try:
            return self._device_id
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def name_change(self) -> 'NameChange':
        """Get the NameChange instance associated with this Commcell.

        Returns:
            NameChange: An instance of the NameChange class for managing name change operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> name_change_mgr = commcell.name_change  # Access the NameChange property
            >>> print(f"NameChange manager: {name_change_mgr}")

        #ai-gen-doc
        """
        return NameChange(self)

    @property
    def clients(self) -> 'Clients':
        """Get the Clients instance associated with this Commcell.

        Returns:
            Clients: An instance for managing clients within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> clients = commcell.clients  # Access the Clients property
            >>> print(f"Total clients: {len(clients)}")
            >>> # The returned Clients object can be used to manage client operations

        #ai-gen-doc
        """
        try:
            if self._clients is None:
                self._clients = Clients(self)

            return self._clients
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_cache(self) -> 'CommServeCache':
        """Get the CommServeCache instance associated with this Commcell.

        Returns:
            CommServeCache: An instance for managing CommServe cache operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> cache = commcell.commserv_cache  # Access the CommServeCache property
            >>> print(f"CommServeCache object: {cache}")
            >>> # The returned CommServeCache object can be used for cache management tasks

        #ai-gen-doc
        """
        try:
            if self._commserv_cache is None:
                self._commserv_cache = CommServeCache(self)

            return self._commserv_cache
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def index_servers(self) -> 'IndexServers':
        """Get the IndexServers instance associated with this Commcell.

        Returns:
            IndexServers: An instance for managing index servers in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> index_servers = commcell.index_servers  # Access the IndexServers property
            >>> print(f"IndexServers object: {index_servers}")
            >>> # The returned IndexServers object can be used for index server operations

        #ai-gen-doc
        """
        try:
            if self._index_servers is None:
                self._index_servers = IndexServers(self)

            return self._index_servers
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def hac_clusters(self) -> 'HACClusters':
        """Get the HACClusters instance associated with this Commcell.

        Returns:
            HACClusters: An instance for managing High Availability Clusters (HAC) within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> hac_clusters = commcell.hac_clusters  # Access the HACClusters property
            >>> print(f"HAC Clusters object: {hac_clusters}")
            >>> # The returned HACClusters object can be used for further HAC management

        #ai-gen-doc
        """
        try:
            if self._hac_clusters is None:
                self._hac_clusters = HACClusters(self)

            return self._hac_clusters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def network_topologies(self) -> 'NetworkTopologies':
        """Get the NetworkTopologies instance associated with this Commcell.

        Returns:
            NetworkTopologies: An instance for managing network topologies within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> net_topologies = commcell.network_topologies  # Access via property
            >>> print(f"Network topologies object: {net_topologies}")
            >>> # The returned NetworkTopologies object can be used for further network management

        #ai-gen-doc
        """
        try:
            if self._nw_topo is None:
                self._nw_topo = NetworkTopologies(self)

            return self._nw_topo
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def index_pools(self) -> 'IndexPools':
        """Get the IndexPools instance associated with this Commcell.

        Returns:
            IndexPools: An instance for managing index pools within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> index_pools = commcell.index_pools  # Access the IndexPools property
            >>> print(f"IndexPools object: {index_pools}")
            >>> # The returned IndexPools object can be used for index pool management

        #ai-gen-doc
        """
        try:
            if self._index_pools is None:
                self._index_pools = IndexPools(self)

            return self._index_pools
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def media_agents(self) -> 'MediaAgents':
        """Get the MediaAgents instance associated with this Commcell.

        Returns:
            MediaAgents: An instance for managing media agents in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> media_agents = commcell.media_agents  # Access the MediaAgents property
            >>> print(media_agents)
            >>> # The returned MediaAgents object can be used to manage media agents

        #ai-gen-doc
        """
        try:
            if self._media_agents is None:
                self._media_agents = MediaAgents(self)

            return self._media_agents
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def workflows(self) -> 'WorkFlows':
        """Get the WorkFlows instance associated with this Commcell.

        Returns:
            WorkFlows: An instance for managing and interacting with workflows on the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> workflows = commcell.workflows  # Access the workflows property
            >>> print(f"WorkFlows object: {workflows}")
            >>> # The returned WorkFlows object can be used to manage workflows

        #ai-gen-doc
        """
        try:
            if self._workflows is None:
                self._workflows = WorkFlows(self)

            return self._workflows
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def alerts(self) -> 'Alerts':
        """Get the Alerts instance associated with this Commcell.

        Returns:
            Alerts: An instance for managing and retrieving alert information from the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> alerts_obj = commcell.alerts  # Access the Alerts property
            >>> print(f"Alerts object: {alerts_obj}")
            >>> # The returned Alerts object can be used to manage alerts

        #ai-gen-doc
        """
        try:
            if self._alerts is None:
                self._alerts = Alerts(self)

            return self._alerts
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disk_libraries(self) -> 'DiskLibraries':
        """Get the DiskLibraries instance associated with this Commcell.

        Returns:
            DiskLibraries: An instance for managing disk libraries in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> disk_libs = commcell.disk_libraries  # Access the DiskLibraries property
            >>> print(disk_libs)
            >>> # The returned DiskLibraries object can be used to manage disk libraries

        #ai-gen-doc
        """
        try:
            if self._disk_libraries is None:
                self._disk_libraries = DiskLibraries(self)

            return self._disk_libraries
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def tape_libraries(self) -> 'TapeLibraries':
        """Get the TapeLibraries instance associated with this Commcell.

        Returns:
            TapeLibraries: An instance for managing tape libraries in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> tape_libs = commcell.tape_libraries  # Access the tape libraries property
            >>> print(f"Tape libraries object: {tape_libs}")
            >>> # The returned TapeLibraries object can be used for further tape library operations

        #ai-gen-doc
        """
        if self._tape_libraries is None:
            self._tape_libraries = TapeLibraries(self)
        return self._tape_libraries

    @property
    def storage_policies(self) -> 'StoragePolicies':
        """Get the StoragePolicies instance associated with this Commcell.

        Returns:
            StoragePolicies: An instance for managing storage policies within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> storage_policies = commcell.storage_policies  # Access via property
            >>> print(storage_policies)
            >>> # The returned StoragePolicies object can be used to manage storage policies

        #ai-gen-doc
        """
        return self.policies.storage_policies

    @property
    def schedule_policies(self) -> 'SchedulePolicies':
        """Get the SchedulePolicies instance associated with this Commcell.

        Returns:
            SchedulePolicies: An instance for managing schedule policies within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> sched_policies = commcell.schedule_policies  # Access via property
            >>> print(f"Schedule policies object: {sched_policies}")
            >>> # The returned SchedulePolicies object can be used for further schedule policy operations

        #ai-gen-doc
        """
        return self.policies.schedule_policies

    @property
    def schedules(self) -> 'Schedules':
        """Get the Schedules instance associated with this Commcell.

        Returns:
            Schedules: An instance for managing and retrieving schedule information.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> schedules = commcell.schedules  # Access the schedules property
            >>> print(f"Schedules object: {schedules}")
            >>> # The returned Schedules object can be used to manage schedules

        #ai-gen-doc
        """
        try:
            if self._schedules is None:
                self._schedules = Schedules(self)

            return self._schedules
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def policies(self) -> 'Policies':
        """Get the Policies instance associated with this Commcell.

        Returns:
            Policies: An instance for managing policies within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> policies = commcell.policies  # Access the policies property
            >>> print(f"Policies object: {policies}")
            >>> # The returned Policies object can be used for further policy management

        #ai-gen-doc
        """
        try:
            if self._policies is None:
                self._policies = Policies(self)

            return self._policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def deduplication_engines(self) -> 'DeduplicationEngines':
        """Get the DeduplicationEngines instance associated with this Commcell.

        Returns:
            DeduplicationEngines: An object for managing deduplication engines in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> dedupe_engines = commcell.deduplication_engines  # Access via property
            >>> print(f"Deduplication engines object: {dedupe_engines}")
            >>> # The returned DeduplicationEngines object can be used for further deduplication management

        #ai-gen-doc
        """
        try:
            if self._deduplication_engines is None:
                self._deduplication_engines = DeduplicationEngines(self)
            return self._deduplication_engines
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def user_groups(self) -> 'UserGroups':
        """Get the UserGroups instance associated with this Commcell.

        Returns:
            UserGroups: An instance for managing user groups within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> user_groups = commcell.user_groups  # Access the user groups property
            >>> print(user_groups)
            >>> # The returned UserGroups object can be used to manage user groups

        #ai-gen-doc
        """
        try:
            if self._user_groups is None:
                self._user_groups = UserGroups(self)

            return self._user_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def domains(self) -> 'Domains':
        """Get the Domains instance associated with this Commcell.

        Returns:
            Domains: An instance for managing Domains and domain-related operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> domains = commcell.domains  # Access the Domains property
            >>> print(f"Domains object: {user_groups}")
            >>> # The returned Domains object can be used for Domains management

        #ai-gen-doc
        """
        try:
            if self._domains is None:
                self._domains = Domains(self)

            return self._domains
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def client_groups(self) -> 'ClientGroups':
        """Get the ClientGroups instance associated with this Commcell.

        Returns:
            ClientGroups: An instance for managing client groups within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> client_groups = commcell.client_groups  # Access the client_groups property
            >>> print(f"ClientGroups object: {client_groups}")
            >>> # The returned ClientGroups object can be used to manage client groups

        #ai-gen-doc
        """
        try:
            if self._client_groups is None:
                self._client_groups = ClientGroups(self)

            return self._client_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def global_filters(self) -> 'GlobalFilters':
        """Get the GlobalFilters instance associated with this Commcell.

        Returns:
            GlobalFilters: An instance for managing global filters within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> filters = commcell.global_filters  # Access the global filters property
            >>> print(filters)
            >>> # The returned GlobalFilters object can be used to manage global filter settings

        #ai-gen-doc
        """
        try:
            if self._global_filters is None:
                self._global_filters = GlobalFilters(self)

            return self._global_filters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def datacube(self) -> 'Datacube':
        """Get the Datacube instance associated with this Commcell.

        Returns:
            Datacube: An instance of the Datacube class for managing data analytics and insights.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> datacube_instance = commcell.datacube  # Access the Datacube property
            >>> print(f"Datacube object: {datacube_instance}")
            >>> # The returned Datacube object can be used for further data analytics operations

        #ai-gen-doc
        """
        try:
            if self._datacube is None:
                self._datacube = Datacube(self)

            return self._datacube
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def content_analyzers(self) -> 'ContentAnalyzers':
        """Get the ContentAnalyzers instance associated with this Commcell.

        Returns:
            ContentAnalyzers: An instance for managing content analyzers in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> analyzers = commcell.content_analyzers  # Access the ContentAnalyzers property
            >>> print(analyzers)
            >>> # The returned ContentAnalyzers object can be used for further analyzer management

        #ai-gen-doc
        """
        try:
            if self._content_analyzers is None:
                self._content_analyzers = ContentAnalyzers(self)

            return self._content_analyzers
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def scale_targets(self) -> 'ScaleTargets':
        """Get the ScaleTargets instance associated with this Commcell.

        Returns:
            ScaleTargets: An instance for managing scale targets in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> scale_targets = commcell.scale_targets  # Access the ScaleTargets property
            >>> print(scale_targets)
            >>> # The returned ScaleTargets object can be used for scale target management

        #ai-gen-doc
        """
        try:
            if self._scale_targets is None:
                self._scale_targets = ScaleTargets(self)

            return self._scale_targets
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def resource_pool(self) -> 'ResourcePools':
        """Get the ResourcePools instance associated with this Commcell.

        Returns:
            ResourcePools: An instance for managing resource pools within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> resource_pools = commcell.resource_pool  # Access the resource pools property
            >>> print(resource_pools)
            >>> # The returned ResourcePools object can be used for further resource pool operations

        #ai-gen-doc
        """
        try:
            if self._resource_pool is None:
                self._resource_pool = ResourcePools(self)
            return self._resource_pool
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def activate(self) -> 'Activate':
        """Get the Activate instance associated with this Commcell.

        Returns:
            Activate: An instance for managing activate within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> activate = commcell.activate  # Access the Activate property
            >>> print(activate)
            >>> # The returned Activate object can be used for further activate operations

        #ai-gen-doc
        """
        try:
            if self._activate is None:
                self._activate = Activate(self)

            return self._activate
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def threat_indicators(self) -> 'TAServers':
        """Get the TAServers instance associated with threat indicators for this Commcell.

        Returns:
            TAServers: An instance of the TAServers class for managing threat indicators.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> threat_servers = commcell.threat_indicators  # Access the TAServers instance via property
            >>> print(threat_servers)
            >>> # Use the returned TAServers object to interact with threat indicators

        #ai-gen-doc
        """
        try:
            if self._threat_indicators is None:
                self._threat_indicators = TAServers(self)

            return self._threat_indicators

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def export_sets(self) -> 'ExportSets':
        """Get the ExportSets instance associated with this Commcell.

        Returns:
            ExportSets: An instance for managing export sets within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> export_sets = commcell.export_sets  # Access the ExportSets property
            >>> print(f"ExportSets object: {export_sets}")
            >>> # The returned ExportSets object can be used for export set operations

        #ai-gen-doc
        """
        try:
            if self._export_sets is None:
                self._export_sets = ExportSets(self)
            return self._export_sets
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def plans(self) -> 'Plans':
        """Get the Plans instance associated with this Commcell object.

        Returns:
            Plans: An instance for managing plans within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> plans_obj = commcell.plans  # Access the Plans property
            >>> print(f"Plans object: {plans_obj}")
            >>> # The returned Plans object can be used to manage plans

        #ai-gen-doc
        """
        try:
            if self._plans is None:
                self._plans = Plans(self)

            return self._plans
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def job_controller(self) -> 'JobController':
        """Get the JobController instance associated with this Commcell.

        Returns:
            JobController: An instance for managing and monitoring jobs on the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> jobs = commcell.job_controller  # Access the JobController object via property
            >>> print(f"JobController object: {jobs}")
            >>> # The returned JobController object can be used to interact with job operations

        #ai-gen-doc
        """
        try:
            if self._job_controller is None:
                self._job_controller = JobController(self)

            return self._job_controller
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def users(self) -> 'Users':
        """Get the Users instance associated with this Commcell.

        Returns:
            Users: An instance for managing users within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> users_obj = commcell.users  # Access the Users property
            >>> print(users_obj)
            >>> # The returned Users object can be used to manage user accounts

        #ai-gen-doc
        """
        try:
            if self._users is None:
                self._users = Users(self)

            return self._users
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def roles(self) -> 'Roles':
        """Get the Roles instance associated with this Commcell.

        Returns:
            Roles: An instance for managing user roles within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> roles_obj = commcell.roles  # Access the roles property
            >>> print(f"Roles object: {roles_obj}")
            >>> # The returned Roles object can be used to manage user roles

        #ai-gen-doc
        """
        try:
            if self._roles is None:
                self._roles = Roles(self)

            return self._roles
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def credentials(self) -> 'Credentials':
        """Get the Credentials instance associated with this Commcell.

        Returns:
            Credentials: An instance for managing user credentials within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> creds = commcell.credentials  # Access the credentials property
            >>> print(f"Credentials object: {creds}")
            >>> # The returned Credentials object can be used for credential management

        #ai-gen-doc
        """
        try:
            if self._credentials is None:
                self._credentials = Credentials(self)

            return self._credentials
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def download_center(self) -> 'DownloadCenter':
        """Get the DownloadCenter instance associated with this Commcell.

        Returns:
            DownloadCenter: An instance for managing downloads and updates within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> download_mgr = commcell.download_center  # Access the DownloadCenter property
            >>> print(f"Download center object: {download_mgr}")
            >>> # The returned DownloadCenter object can be used for managing downloads

        #ai-gen-doc
        """
        try:
            if self._download_center is None:
                self._download_center = DownloadCenter(self)

            return self._download_center
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def organizations(self) -> 'Organizations':
        """Get the Organizations instance associated with this Commcell.

        Returns:
            Organizations: An instance for managing organizations within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> orgs = commcell.organizations  # Access the organizations property
            >>> print(f"Organizations object: {orgs}")
            >>> # The returned Organizations object can be used for further organization management

        #ai-gen-doc
        """
        try:
            if self._organizations is None:
                self._organizations = Organizations(self)

            return self._organizations
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def tags(self) -> 'Tags':
        """Get the Tags instance associated with this Commcell.

        Returns:
            Tags: An instance for managing tags within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> tags_obj = commcell.tags  # Access the tags property
            >>> print(f"Tags object: {tags_obj}")
            >>> # The returned Tags object can be used to manage tags in the Commcell

        #ai-gen-doc
        """
        try:
            if self._tags is None:
                self._tags = Tags(self)

            return self._tags
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def storage_pools(self) -> 'StoragePools':
        """Get the StoragePools instance associated with this Commcell.

        Returns:
            StoragePools: An instance for managing storage pools in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> pools = commcell.storage_pools  # Access the storage pools property
            >>> print(f"Storage pools object: {pools}")
            >>> # The returned StoragePools object can be used for further storage pool operations

        #ai-gen-doc
        """
        try:
            if self._storage_pools is None:
                self._storage_pools = StoragePools(self)

            return self._storage_pools
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def monitoring_policies(self) -> 'MonitoringPolicies':
        """Get the MonitoringPolicies instance associated with this Commcell.

        Returns:
            MonitoringPolicies: An instance for managing monitoring policies.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> monitoring_policies = commcell.monitoring_policies  # Access via property
            >>> print(monitoring_policies)
            >>> # Use the returned MonitoringPolicies object for further operations

        #ai-gen-doc
        """
        try:
            if self._monitoring_policies is None:
                self._monitoring_policies = MonitoringPolicies(self)

            return self._monitoring_policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def operation_window(self) -> 'OperationWindow':
        """Get the OperationWindow instance associated with this Commcell.

        Returns:
            OperationWindow: An instance for managing operation windows on the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> op_window = commcell.operation_window  # Access the operation window property
            >>> print(f"Operation window object: {op_window}")
            >>> # The returned OperationWindow object can be used for further operations

        #ai-gen-doc
        """
        try:
            if self._operation_window is None:
                self._operation_window = OperationWindow(self)
            return self._operation_window
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def activity_control(self) -> 'ActivityControl':
        """Get the ActivityControl instance associated with this Commcell.

        Returns:
            ActivityControl: An instance for managing activity controls on the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> activity_ctrl = commcell.activity_control  # Access the property
            >>> print(f"ActivityControl object: {activity_ctrl}")
            >>> # The returned ActivityControl object can be used to manage activity controls

        #ai-gen-doc
        """
        try:
            if self._activity_control is None:
                self._activity_control = ActivityControl(self)

            return self._activity_control
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def event_viewer(self) -> 'Events':
        """Get the Events instance associated with this Commcell.

        Returns:
            Events: An instance for accessing and managing event logs and viewer operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> event_viewer = commcell.event_viewer  # Use dot notation for property access
            >>> print(f"Events object: {event_viewer}")
            >>> # The returned Events object can be used to interact with event logs

        #ai-gen-doc
        """
        try:
            if self._events is None:
                self._events = Events(self)

            return self._events
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def array_management(self) -> 'ArrayManagement':
        """Get the ArrayManagement instance associated with this Commcell.

        Returns:
            ArrayManagement: An instance for managing storage arrays within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> array_mgr = commcell.array_management  # Access the property
            >>> print(f"Array management object: {array_mgr}")
            >>> # Use the returned ArrayManagement object for array operations

        #ai-gen-doc
        """
        try:
            if self._array_management is None:
                self._array_management = ArrayManagement(self)

            return self._array_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disasterrecovery(self) -> 'DisasterRecovery':
        """Get the DisasterRecovery instance associated with this Commcell.

        Returns:
            DisasterRecovery: An instance for managing disaster recovery operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> dr = commcell.disasterrecovery  # Access the DisasterRecovery property
            >>> print(f"Disaster recovery object: {dr}")
            >>> # The returned DisasterRecovery object can be used for recovery operations

        #ai-gen-doc
        """
        try:
            if self._disaster_recovery is None:
                self._disaster_recovery = DisasterRecovery(self)

            return self._disaster_recovery
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def identity_management(self) -> 'IdentityManagementApps':
        """Get the IdentityManagementApps instance associated with this Commcell.

        Returns:
            IdentityManagementApps: An instance for managing identity management applications.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> idm_apps = commcell.identity_management  # Access the property
            >>> print(f"Identity management object: {idm_apps}")
            >>> # The returned IdentityManagementApps object can be used for identity-related operations

        #ai-gen-doc
        """
        try:
            if self._identity_management is None:
                self._identity_management = IdentityManagementApps(self)

            return self._identity_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def system(self) -> 'System':
        """Get the System instance associated with this Commcell.

        Returns:
            System: An instance of the System class for managing system-level operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> system_obj = commcell.system  # Access the System object via the property
            >>> print(f"System object: {system_obj}")

        #ai-gen-doc
        """
        try:
            if self._system is None:
                self._system = System(self)

            return self._system
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_client(self) -> 'Client':
        """Get the Client instance representing the CommServ client.

        Returns:
            Client: An instance of the Client class for the CommServ client.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> commserv_client = commcell.commserv_client  # Access CommServ client as a property
            >>> print(f"CommServ client name: {commserv_client.client_name}")

        #ai-gen-doc
        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()

        if self._commserv_client is None:
            self._commserv_client = self.clients.get(self.commcell_id)
        return self._commserv_client

    @property
    def commcell_migration(self) -> 'CommCellMigration':
        """Get the CommCellMigration instance associated with this Commcell.

        Returns:
            CommCellMigration: An instance for managing Commcell migration operations.

        Example:
            >>> commcell = Commcell(commcell_object)
            >>> migration = commcell.commcell_migration  # Access the migration property
            >>> print(f"Migration object: {migration}")
            >>> # Use the migration object for migration-related tasks

        #ai-gen-doc
        """
        try:
            if self._commcell_migration is None:
                self._commcell_migration = CommCellMigration(self)

            return self._commcell_migration
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def grc(self) -> 'GlobalRepositoryCell':
        """Get the GlobalRepositoryCell instance associated with this Commcell.

        Returns:
            GlobalRepositoryCell: An instance for managing global repository cell operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> grc_instance = commcell.grc  # Access the GlobalRepositoryCell property
            >>> print(f"GRC object: {grc_instance}")
            >>> # The returned GlobalRepositoryCell object can be used for further operations

        #ai-gen-doc
        """
        try:
            if self._grc is None:
                self._grc = GlobalRepositoryCell(self)

            return self._grc
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def registered_commcells(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all registered Commcells and their associated information.

        Returns:
            A dictionary where each key is the name of a registered Commcell, and the value is another
            dictionary containing details related to that Commcell.

            Example structure:
                {
                    "commcell_name1": {
                        # details related to commcell_name1
                    },
                    "commcell_name2": {
                        # details related to commcell_name2
                    }
                }

        Example:
            >>> commcell = Commcell()
            >>> reg_commcells = commcell.registered_commcells
            >>> print(f"Total registered Commcells: {len(reg_commcells)}")
            >>> for name, info in reg_commcells.items():
            ...     print(f"Commcell: {name}, Info: {info}")

        #ai-gen-doc
        """
        if self._registered_commcells is None:
            self._registered_commcells = self._get_registered_commcells()
        return self._registered_commcells

    @property
    def replication_groups(self) -> 'ReplicationGroups':
        """Get the ReplicationGroups instance associated with this Commcell.

        Returns:
            ReplicationGroups: An object for managing and accessing replication groups within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> rep_groups = commcell.replication_groups  # Use dot notation for property access
            >>> print(f"Replication groups object: {rep_groups}")
            >>> # The returned ReplicationGroups object can be used to manage replication groups

        #ai-gen-doc
        """
        try:
            if self._replication_groups is None:
                self._replication_groups = ReplicationGroups(self)
            return self._replication_groups

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def failover_groups(self) -> 'FailoverGroups':
        """Get the FailoverGroups instance associated with this Commcell.

        Returns:
            FailoverGroups: An instance for managing failover groups within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> failover_groups = commcell.failover_groups  # Access via property
            >>> print(f"FailoverGroups object: {failover_groups}")
            >>> # The returned FailoverGroups object can be used to manage failover groups

        #ai-gen-doc
        """
        try:
            if self._failover_groups is None:
                self._failover_groups = FailoverGroups(self)
            return self._failover_groups

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def recovery_targets(self) -> 'RecoveryTargets':
        """Get the RecoveryTargets instance associated with this Commcell.

        Returns:
            RecoveryTargets: An instance for managing recovery targets within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> targets = commcell.recovery_targets  # Access the recovery targets property
            >>> print(targets)
            >>> # Use the returned RecoveryTargets object for further recovery operations

        #ai-gen-doc
        """
        try:
            if self._recovery_targets is None:
                self._recovery_targets = RecoveryTargets(self)

            return self._recovery_targets

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def cleanroom_recovery_groups(self) -> 'RecoveryGroups':
        """Get the RecoveryGroups instance associated with this Commcell.

        Returns:
            RecoveryGroups: An instance for managing cleanroom recovery groups.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> recovery_groups = commcell.cleanroom_recovery_groups  # Access as a property
            >>> print(f"RecoveryGroups object: {recovery_groups}")
            >>> # Use the returned RecoveryGroups object for further operations

        #ai-gen-doc
        """
        try:
            if self._recovery_groups is None:
                self._recovery_groups = RecoveryGroups(self)

            return self._recovery_groups

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def cleanroom_targets(self) -> 'CleanroomTargets':
        """Get the CleanroomTargets instance associated with this Commcell.

        Returns:
            CleanroomTargets: An instance for managing cleanroom recovery targets.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> targets = commcell.cleanroom_targets  # Access the property
            >>> print(f"CleanroomTargets object: {targets}")

        #ai-gen-doc
        """
        try:
            if self._cleanroom_targets is None:
                self._cleanroom_targets = CleanroomTargets(self)

            return self._cleanroom_targets

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def blr_pairs(self) -> 'BLRPairs':
        """Get the BLRPairs instance associated with this Commcell.

        Returns:
            BLRPairs: An instance for managing BLR (Block Level Replication) pairs.

        Example:
            >>> commcell = Commcell()
            >>> blr_pairs_instance = commcell.blr_pairs  # Access the BLRPairs property
            >>> print(f"BLRPairs object: {blr_pairs_instance}")
            >>> # The returned BLRPairs object can be used for BLR pair management

        #ai-gen-doc
        """
        try:
            if self._blr_pairs is None:
                self._blr_pairs = BLRPairs(self)

            return self._blr_pairs

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def backup_network_pairs(self) -> 'BackupNetworkPairs':
        """Get the BackupNetworkPairs instance associated with this Commcell.

        Returns:
            BackupNetworkPairs: An instance for managing backup network pairs in the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> network_pairs = commcell.backup_network_pairs  # Access the property
            >>> print(f"Backup network pairs object: {network_pairs}")
            >>> # The returned BackupNetworkPairs object can be used for network pair management

        #ai-gen-doc
        """
        try:
            if self._backup_network_pairs is None:
                self._backup_network_pairs = BackupNetworkPairs(self)

            return self._backup_network_pairs

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def reports(self) -> 'Report':
        """Get the Report instance associated with this Commcell.

        Returns:
            Report: An instance of the Report class for generating and managing reports.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> report_obj = commcell.reports  # Access the reports property
            >>> print(f"Report object: {report_obj}")
            >>> # The returned Report object can be used to generate or retrieve reports

        #ai-gen-doc
        """
        try:
            if self._reports is None:
                self._reports = Report(self)
            return self._reports
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def job_management(self) -> 'JobManagement':
        """Get the JobManagement instance associated with this Commcell.

        Returns:
            JobManagement: An instance for managing and monitoring jobs on the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> job_mgmt = commcell.job_management  # Access the job management property
            >>> print(f"Job management object: {job_mgmt}")
            >>> # The returned JobManagement object can be used to manage jobs

        #ai-gen-doc
        """
        try:
            if not self._job_management:
                self._job_management = JobManagement(self)
            return self._job_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_metadata(self) -> dict:
        """Get the metadata information for the CommServe.

        Returns:
            dict: A dictionary containing metadata details of the CommServe.

        Example:
            >>> commcell = Commcell()
            >>> metadata = commcell.commserv_metadata  # Use dot notation for property access
            >>> print(metadata)
            >>> # Output might include keys such as 'version', 'hostname', etc.

        #ai-gen-doc
        """
        if self._commserv_metadata is None:
            self._commserv_metadata = self._get_commserv_metadata()
        return self._commserv_metadata

    @property
    def commserv_oem_id(self) -> int:
        """Get the OEM ID of the CommServe.

        Returns:
            int: The OEM (Original Equipment Manufacturer) ID associated with this CommServe instance.

        Example:
            >>> commcell = Commcell()
            >>> oem_id = commcell.commserv_oem_id
            >>> print(f"CommServe OEM ID: {oem_id}")

        #ai-gen-doc
        """
        try:
            if self._commserv_oem_id is None:
                self._commserv_oem_id = self._get_commserv_oem_id()

            return self._commserv_oem_id
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def metallic(self) -> 'Metallic':
        """Get the Metallic instance associated with this Commcell.

        Returns:
            Metallic: An instance of the Metallic class for managing Metallic-related operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> metallic_instance = commcell.metallic  # Access the Metallic property
            >>> print(metallic_instance)
            >>> # Use metallic_instance for further Metallic operations

        #ai-gen-doc
        """
        try:
            if self._metallic is None:
                self._metallic = Metallic(self)

            return self._metallic
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def is_privacy_enabled(self) -> bool:
        """Check if privacy is enabled at the Commcell level.

        Returns:
            True if privacy is enabled for the Commcell, False otherwise.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> if commcell.is_privacy_enabled:
            ...     print("Privacy is enabled on this Commcell.")
            ... else:
            ...     print("Privacy is not enabled on this Commcell.")

        #ai-gen-doc
        """
        if self._commcell_properties is None:
            self.get_commcell_properties()

        self._privacy = self._commcell_properties.get('enablePrivacy')

        return self._privacy

    @property
    def key_management_servers(self) -> 'KeyManagementServers':
        """Get the KeyManagementServers instance associated with this Commcell.

        Returns:
            KeyManagementServers: An instance for managing key management servers.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> kms = commcell.key_management_servers  # Access via property
            >>> print(f"Key management servers object: {kms}")
            >>> # The returned KeyManagementServers object can be used for further operations

        #ai-gen-doc
        """
        try:
            if self._kms is None:
                self._kms = KeyManagementServers(self)

            return self._kms
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def regions(self) -> 'Regions':
        """Get the Regions instance associated with this Commcell.

        Returns:
            Regions: An instance for managing regions within the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> regions_obj = commcell.regions  # Access the Regions property
            >>> print(f"Regions object: {regions_obj}")
            >>> # The returned Regions object can be used for region management tasks

        #ai-gen-doc
        """
        try:
            if self._regions is None:
                self._regions = Regions(self)

            return self._regions
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def snmp_configurations(self) -> 'SNMPConfigurations':
        """Get the SNMPConfigurations instance associated with this Commcell.

        Returns:
            SNMPConfigurations: An instance for managing SNMP configurations on the Commcell.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> snmp_configs = commcell.snmp_configurations  # Access SNMP configurations property
            >>> print(snmp_configs)
            >>> # The returned SNMPConfigurations object can be used to manage SNMP settings

        #ai-gen-doc
        """
        try:
            if self._snmp_configurations is None:
                self._snmp_configurations = SNMPConfigurations(self)
            return self._snmp_configurations
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def service_commcells(self) -> 'ServiceCommcells':
        """Get the ServiceCommcells instance associated with this Commcell.

        Returns:
            ServiceCommcells: An instance for managing service commcells.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> service_commcells = commcell.service_commcells  # Access via property
            >>> print(f"Service commcells object: {service_commcells}")
            >>> # The returned ServiceCommcells object can be used for further operations

        #ai-gen-doc
        """
        try:
            if self._service_commcells is None:
                self._service_commcells = ServiceCommcells(self)
            return self._service_commcells
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def logout(self) -> None:
        """Log out the user associated with the current Commcell instance.

        This method terminates the session for the user currently authenticated with this Commcell object.
        After calling this method, further operations requiring authentication will fail until a new login is performed.

        Example:
            >>> commcell = Commcell('server', 'username', 'password')
            >>> commcell.logout()
            >>> print("User has been logged out successfully.")

        #ai-gen-doc
        """
        if self._headers['Authtoken'] is None:
            return 'User already logged out.'

        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def request(self, request_type: str, request_url: str, request_body: Optional[dict] = None) -> 'requests.Response':
        """Send an HTTP request of the specified type to the Commcell API.

        This method allows you to perform HTTP operations (such as GET, POST, PUT, DELETE) 
        on the Commcell by specifying the request type, API endpoint, and an optional JSON body.

        Args:
            request_type: The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            request_url: The API endpoint or resource path to target (e.g., 'Client', 'Agent', 'Client/{clientId}').
            request_body: Optional dictionary representing the JSON body to include in the request.

        Returns:
            The response object received from the Commcell server. The exact type of the response 
            depends on the request and the API endpoint.

        Example:
            >>> commcell = Commcell()
            >>> # Send a GET request to retrieve all clients
            >>> response = commcell.request('GET', 'Client')
            >>> print(response)
            >>> 
            >>> # Send a POST request to create a new client
            >>> new_client_data = {'clientName': 'Server01', 'hostName': 'server01.example.com'}
            >>> response = commcell.request('POST', 'Client', request_body=new_client_data)
            >>> print(response)

        #ai-gen-doc
        """
        request_url = self._web_service + request_url

        _, response = self._cvpysdk_object.make_request(
            request_type.upper(), request_url, request_body
        )

        return response

    def wrap_request(
            self,
            method: str,
            service_key: str,
            fill_params: Optional[tuple] = None,
            req_kwargs: Optional[dict] = None,
            **wrap_kwargs
        ) -> Any:
        """Wrap a request to the Commcell in a standard format for most API calls.

        This method standardizes the process of making HTTP requests to the Commcell API, handling URL formatting,
        request parameters, and response processing. It supports flexible error handling, response validation,
        and custom callbacks for error scenarios.

        Args:
            method: The HTTP method to use for the request (e.g., 'GET', 'POST').
            service_key: The key to access the request URL from the services.py dictionary.
                         (You can give the endpoint URL also directly)
            fill_params: Optional tuple of parameters to fill in the service URL if it contains %s formatting.
            req_kwargs: Optional dictionary of keyword arguments to pass to the request. Example keys include:
                - 'payload': dict or str, the request payload.
                - 'attempts': int, number of retry attempts.
                - 'headers': dict, custom HTTP headers.
                - 'stream': bool, whether to stream the response.
                - 'files': dict, files to upload.
                - 'remove_processing_info': bool, whether to remove processing info from the response.

            wrap_kwargs:
                return_resp (bool): If True, returns the raw response object; otherwise, returns response.json(). Default is False.
                ignore_flag (bool): If True, ignores the flag in the response. Default is False.
                empty_check (bool): If True, checks if the response is empty and raises an exception if so. Default is True.
                error_check (bool): If True, handles errors in the response dict and raises an SDK exception. Default is False for 'GET', True for others.
                error_read (Callable): Function to extract error code and message from the response dict.
                error_callback (Callable): Function to handle non-zero error codes, typically raising an SDKException.
                sdk_exception (tuple): Tuple specifying the module and error code for the default error callback.

        Returns:
            The parsed JSON response from the Commcell API, or the raw response object if 'return_resp' is True.

        Example:
            >>> # Make a POST request to the 'CREATE_CLIENT' service with payload
            >>> response = commcell.wrap_request(
            ...     method='POST',
            ...     service_key='CREATE_CLIENT',
            ...     fill_params=('client_name',),
            ...     req_kwargs={'payload': {'client': 'client_name'}}
            ... )
            >>> print(response)
            >>> # To get the raw response object:
            >>> raw_resp = commcell.wrap_request(
            ...     method='GET',
            ...     service_key='GET_CLIENT',
            ...     fill_params=('client_name',),
            ...     return_resp=True
            ... )
            >>> print(raw_resp.status_code)

        #ai-gen-doc
        """
        req_kwargs = req_kwargs or {}
        exc_module, exc_code = wrap_kwargs.get('sdk_exception', ('Response', '101'))

        def default_error_read(resp_dict) -> tuple[int, str]:
            """Default error reading function"""
            error_node = resp_dict
            if 'error' in resp_dict:
                error_node = resp_dict['error']
            code = error_node.get('errorCode', error_node.get('resultCode', -1))
            msg = error_node.get('errorMessage',
                error_node.get('errorString',
                    error_node.get('resultMessage', f'No error message in response -> {resp_dict}')
                )
            )
            return code, msg

        def default_error_callback(error_code: int, error_msg: str):
            """Default error callback function"""
            raise SDKException(exc_module, exc_code, f'[{error_code}: {error_msg}]')

        ignore_flag = wrap_kwargs.get('ignore_flag', False)
        return_resp = wrap_kwargs.get('return_resp', False)
        empty_check = wrap_kwargs.get('empty_check', True)
        error_check = wrap_kwargs.get('error_check', method!='GET')
        error_read = wrap_kwargs.get('error_read', default_error_read)
        error_callback = wrap_kwargs.get('error_callback', default_error_callback)

        def error_handling(res):
            erc, erm = error_read(res.json())
            if erc != 0:
                error_callback(erc, erm)

        api_url = self._services.get(service_key, service_key)
        if fill_params:
            api_url = api_url % fill_params
        flag, response = self._cvpysdk_object.make_request(method, api_url, **req_kwargs)
        content_message = f'Received: {response.content}'

        if (not flag) and (not ignore_flag):
            try:
                error_handling(response)
            except Exception as e:
                if not isinstance(e, SDKException):
                    raise SDKException('Response', '101', content_message)
                raise

        if return_resp and not error_check:
            return response

        try:
            response.json()
        except:
            raise SDKException('Response', '103', content_message)

        if empty_check and not response.json():
            raise SDKException('Response', '102', content_message)

        if error_check:
            error_handling(response)

        return response if return_resp else response.json()

    @contextmanager
    def wrapped_request(self, method: str, service_key: str, fill_params: Optional[tuple] = None, **wrap_kwargs: dict) -> Any:
        """Context manager for handling API requests and responses.

        This context manager wraps the process of making an API request and handling its response,
        providing a convenient way to manage error handling and response parsing. It yields either
        the raw response object or the parsed JSON, depending on the 'return_resp' key in wrap_kwargs.

        Args:
            method: The HTTP method to use for the request (e.g., 'GET', 'POST').
            service_key: The key used to retrieve the request URL from the services dictionary.
            fill_params: Optional tuple of parameters to fill in the service URL if it contains formatting placeholders.
            **wrap_kwargs: Additional keyword arguments for request customization, such as:
                - req_kwargs (dict): Additional arguments to pass to the request method.
                - return_resp (bool): If True, yields the raw response object; otherwise, yields response.json().

        Yields:
            The response object or its JSON content, depending on the 'return_resp' flag in wrap_kwargs.

        Raises:
            SDKException: If an error occurs during the request or within the context block, an SDKException is raised
            with the response content or JSON for debugging.

        Example:
            >>> with commcell.wrapped_request('GET', 'GET_CLIENTS', fill_params=('client1',), return_resp=False) as resp_json:
            ...     print(resp_json)
            >>> # To get the raw response object:
            >>> with commcell.wrapped_request('POST', 'CREATE_POLICY', req_kwargs={'json': payload}, return_resp=True) as resp:
            ...     print(resp.status_code)

        #ai-gen-doc
        """
        resp = self.wrap_request(method, service_key, fill_params, **wrap_kwargs)
        try:
            yield resp
        except Exception as exp:
            debug_msg = resp if isinstance(resp, dict) else resp.content
            raise SDKException('Response', '104', f'Got response: {debug_msg}') from exp

    def send_mail(
        self,
        receivers: list,
        subject: str,
        body: str = None,
        copy_sender: bool = False,
        is_html_content: bool = True,
        **kwargs
    ) -> None:
        """Send an email to the specified recipients from the email address associated with this user.

        Args:
            receivers: List of email addresses to which the email will be sent.
            subject: Subject line of the email.
            body: Optional. The content of the email body. If not provided, the email will have an empty body.
            copy_sender: If True, the sender will be copied in the email. Defaults to False.
            is_html_content: If True, the email body is treated as HTML content. If False, the body is sent as plain text. Defaults to True.
            **kwargs: Additional keyword arguments, such as 'attachments' (list of file paths to attach to the email).

        Raises:
            SDKException: If the email fails to send, if the response is empty, or if the response indicates failure.

        Example:
            >>> commcell = Commcell()
            >>> commcell.send_mail(
            ...     receivers=['user1@example.com', 'user2@example.com'],
            ...     subject='Backup Report',
            ...     body='<h1>Backup Completed Successfully</h1>',
            ...     copy_sender=True,
            ...     is_html_content=True,
            ...     attachments=['/path/to/report.pdf']
            ... )
            >>> print("Email sent successfully.")

        #ai-gen-doc
        """
        if body is None:
            body = ''

        send_email_request = {
            "App_SendEmailReq": {
                "emailInfo": {
                    "subject": subject,
                    "body": body,
                    "copySender": copy_sender,
                    "isHTML": is_html_content,
                    "toEmail": [
                        {
                            "emailAddress": email
                        } for email in receivers
                    ]
                }
            }
        }
        if attachments := kwargs.get('attachments'):
            send_email_request['App_SendEmailReq']['emailInfo']['attachments'] = [
                {"attachmentPath": path} for path in attachments
            ]

        response_json = self._qoperation_execute(send_email_request)
        if response_json.get('errorCode', 0) != 0:
            raise SDKException(
                'Commcell',
                '104',
                'Error: "{}"'.format(response_json['errorMessage'])
            )

    def refresh(self) -> None:
        """Reload the properties and cached data of the Commcell object.

        This method refreshes the Commcell instance, ensuring that any changes 
        made on the Commcell server are reflected in the current object. 
        Use this method to update the Commcell's state after external modifications.

        Example:
            >>> commcell = Commcell('server', 'username', 'password')
            >>> commcell.refresh()  # Refreshes the Commcell properties
            >>> print("Commcell properties refreshed successfully")
        #ai-gen-doc
        """
        
        if not self._commserv_details_set:
            self._commserv_details_loaded = False
        self._clients = None
        self._commserv_cache = None
        self._remote_cache = None
        self._media_agents = None
        self._workflows = None
        self._alerts = None
        self._disk_libraries = None
        self._tape_libraries = None
        self._storage_policies = None
        self._schedule_policies = None
        self._schedules = None
        self._user_groups = None
        self._domains = None
        self._client_groups = None
        self._global_filters = None
        self._datacube = None
        self._activate = None
        self._threat_indicators = None
        self._content_analyzers = None
        self._scale_targets = None
        self._resource_pool = None
        self._plans = None
        self._job_controller = None
        self._users = None
        self._roles = None
        self._credentials = None
        self._download_center = None
        self._organizations = None
        self._policies = None
        self._storage_pools = None
        self._activity_control = None
        self._events = None
        self._monitoring_policies = None
        self._array_management = None
        self._disaster_recovery = None
        self._operation_window = None
        self._commserv_client = None
        self._identity_management = None
        self._commcell_migration = None
        self._grc = None
        self._registered_commcells = None
        self._index_servers = None
        self._hac_clusters = None
        self._nw_topo = None
        self._index_pools = None
        self._deduplication_engines = None
        self._tfa = None
        self._tags = None
        self._additional_settings = None
        self._snmp_configurations = None
        self._service_commcells = None
        self._user_mappings = None
        self._user_role = None
        self._user_org = None

    def get_remote_cache(self, client_name: str) -> 'RemoteCache':
        """Retrieve the RemoteCache instance for a specified client.

        Args:
            client_name: The name of the client for which to obtain the remote cache.

        Returns:
            RemoteCache: An instance of the RemoteCache class associated with the given client.

        Example:
            >>> commcell = Commcell()
            >>> remote_cache = commcell.get_remote_cache('Client01')
            >>> print(f"Remote cache object: {remote_cache}")

        #ai-gen-doc
        """
        try:
            self._remote_cache = RemoteCache(self, client_name)
            return self._remote_cache

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def run_data_aging(
            self,
            copy_name: str = None,
            storage_policy_name: str = None,
            is_granular: bool = False,
            include_all: bool = True,
            include_all_clients: bool = False,
            select_copies: bool = False,
            prune_selected_copies: bool = False,
            schedule_pattern: dict = None
        ) -> Union['Job', 'Schedules']:
        """Run the Data Aging operation at the Commcell, Storage Policy, or Copy level.

        This method initiates the Data Aging process, which removes aged data based on retention rules.
        The operation can be performed at different levels of granularity, including Commcell-wide,
        specific storage policies, or individual copies.

        Args:
            copy_name: Name of the copy to run data aging on. If None, applies to all copies or as specified.
            storage_policy_name: Name of the storage policy to target. If None, applies to all storage policies.
            is_granular: If True, enables granular selection for data aging.
            include_all: If True, includes all eligible items for data aging.
            include_all_clients: If True, includes all clients in the data aging operation.
            select_copies: If True, allows selection of specific copies for data aging.
            prune_selected_copies: If True, prunes only the selected copies.
            schedule_pattern: Optional dictionary specifying a schedule pattern for the data aging job.

        Example:
            >>> commcell = Commcell()
            >>> # Run data aging for all storage policies and copies
            >>> commcell.run_data_aging()
            >>>
            >>> # Run data aging for a specific storage policy and copy
            >>> commcell.run_data_aging(
            ...     storage_policy_name="DailyBackupPolicy",
            ...     copy_name="PrimaryCopy",
            ...     is_granular=True
            ... )

        #ai-gen-doc
        """
        if storage_policy_name is None:
            copy_name = ""
            storage_policy_name = ""

        if copy_name is None:
            copy_name = ""

        request_json = {
            "taskInfo": {
                "associations": [],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0,
                    "alert": {
                        "alertName": ""
                    },
                    "taskFlags": {
                        "isEdgeDrive": False,
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {

                            "subTaskType": 1,
                            "operationType": 4018
                        },

                        "options": {
                            "adminOpts": {
                                "dataAgingOption": {
                                    "selectCopies": select_copies,
                                    "includeAllClients": include_all_clients,
                                    "pruneSelectedCopies": prune_selected_copies,
                                    "isGranular": is_granular,
                                    "includeAll": include_all,
                                    "archiveGroupCopy": [
                                        {
                                            "copyName": copy_name,
                                            "storagePolicyName": storage_policy_name
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CREATE_TASK'], request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    from .job import Job
                    return Job(self, response.json()['jobIds'][0])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Error: "{0}"'.format(error_message)
                    raise SDKException('Commcell', '105', o_str)

                elif "taskId" in response.json():
                    return Schedules(self).get(task_id=response.json()['taskId'])

                else:
                    raise SDKException('Commcell', '105')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_saml_token(self, validity: int = 30) -> str:
        """Retrieve the SAML token for the currently logged-in user.

        Args:
            validity: The validity period of the SAML token in minutes. Defaults to 30 minutes.

        Returns:
            The SAML token string received from the server.

        Example:
            >>> commcell = Commcell()
            >>> saml_token = commcell.get_saml_token(validity=60)
            >>> print(f"SAML Token: {saml_token}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._services['GET_SAML_TOKEN'] % validity
        )

        if flag:
            if response.json():
                response = response.json()
                token = response.get('token')

                if token:
                    return token
                else:
                    error_message = response['errList'][0]['errLogMessage']
                    error_code = response['errList'][0]['errorCode']

                    if 'relogin required' in error_message.lower():
                        self._headers['Authtoken'] = self._cvpysdk_object._renew_login_token(5)
                        return self.get_saml_token(validity)

                    raise SDKException(
                        'Commcell',
                        '106',
                        'Error Code: {0}\nError Message: {1}'.format(error_code, error_message)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_additional_setting(self, category: str, key_name: str, data_type: str, value: str) -> None:
        """Add a registry key to the CommServe property.

        This method allows you to add a custom registry key under a specified category in the CommServe configuration.
        The key can be of various data types, such as BOOLEAN, INTEGER, STRING, MULTISTRING, or ENCRYPTED.

        Args:
            category: The category under which the registry key will be added.
            key_name: The name of the registry key to add.
            data_type: The data type of the registry key. Accepted values are:
                - "BOOLEAN"
                - "INTEGER"
                - "STRING"
                - "MULTISTRING"
                - "ENCRYPTED"
            value: The value to assign to the registry key.

        Raises:
            SDKException: If the key could not be added, if the response is empty, or if the response code is not as expected.

        Example:
            >>> commcell = Commcell('commserve_host', 'username', 'password')
            >>> commcell.add_additional_setting(
            ...     category='ClientProperties',
            ...     key_name='EnableCustomBackup',
            ...     data_type='BOOLEAN',
            ...     value='True'
            ... )
            >>> print("Registry key added successfully.")

        #ai-gen-doc
        """
        self.commserv_client.add_additional_setting(category, key_name, data_type, value)
        self._additional_settings = None

    def delete_additional_setting(self, category: str, key_name: str) -> None:
        """Delete a registry key from the CommServe property.

        This method removes a specified registry key under a given category from the CommServe's additional settings.

        Args:
            category: The category under which the registry key exists.
            key_name: The name of the registry key to be deleted.

        Raises:
            SDKException: If the deletion fails, the response is empty, or the response code is not as expected.

        Example:
            >>> commcell = Commcell()
            >>> commcell.delete_additional_setting('ClientProperties', 'EnableBackupCompression')
            >>> print("Registry key deleted successfully.")

        #ai-gen-doc
        """
        self.commserv_client.delete_additional_setting(category, key_name)
        self._additional_settings = None

    def get_configured_additional_setting(self) -> list:
        """Retrieve the names of all configured additional settings for the Commcell.

        Returns:
            list: A list containing the names of configured additional settings.

        Example:
            >>> commcell = Commcell()
            >>> settings = commcell.get_configured_additional_setting()
            >>> print(settings)
            ['Setting1', 'Setting2', 'Setting3']

        #ai-gen-doc
        """
        return self.commserv_client.get_configured_additional_settings()

    @property
    def additional_settings(self) -> dict:
        """Get the dictionary of additional settings configured on the Commcell.

        This property provides a dictionary where each key is the name of an additional setting,
        and the value is a tuple containing the relative path, key name, type, and value of the setting.

        Returns:
            dict: A dictionary mapping setting names to tuples of the form
                (relative_path, key_name, type, value).

        Example:
            >>> settings = commcell.additional_settings
            >>> for key, setting in settings.items():
            ...     print(f"Setting: {key}, Details: {setting}")
            # Example output:
            # Setting: keyName, Details: ('relativepath', 'keyName', 'type', 'value')
            # Setting: keyName1, Details: ('relativepath1', 'keyName1', 'type1', 'value1')

        #ai-gen-doc
        """
        if self._additional_settings is None:
            self._additional_settings = {
                cs_key.get('keyName'): cs_key for cs_key in self.get_configured_additional_setting()
            }
        return self._additional_settings

    def protected_vms(self, days: int, limit: int = 100) -> dict:
        """Retrieve all protected virtual machines (VMs) for the specified number of days.

        Args:
            days: The number of days to look back for protected VMs.
                For example, if days=30, returns VMs protected in the past 30 days.
            limit: The maximum number of protected VMs to return.
                If set to 0, all protected VMs are returned.
                Default is 100.

        Returns:
            dict: A dictionary containing properties of VMs protected within the specified time frame.

        Example:
            >>> commcell = Commcell()
            >>> vms = commcell.protected_vms(days=30, limit=50)
            >>> print(f"Number of protected VMs: {len(vms)}")
            >>> # Access VM properties
            >>> for vm_name, vm_info in vms.items():
            ...     print(f"VM: {vm_name}, Info: {vm_info}")

        #ai-gen-doc
        """

        from_time, to_time = self._convert_days_to_epoch(days)
        self._PROTECTED_VMS = self._services['PROTECTED_VMS'] % (from_time, to_time, limit)
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._PROTECTED_VMS
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def sync_remote_cache(self, client_list: Optional[List[str]] = None, schedule_pattern: Optional[Dict[str, Any]] = None) -> 'Job':
        """Synchronize the remote cache for specified clients.

        This method initiates a sync job for the remote cache on the provided list of clients.
        If no client list is specified, all remote cache clients will be synchronized.
        Optionally, a schedule pattern can be provided to schedule the sync job.

        Args:
            client_list: Optional list of client names to sync. If None, all remote cache clients are synced.
            schedule_pattern: Optional dictionary specifying the pattern to schedule the sync job.

        Returns:
            Job: An instance of the Job class representing the sync job.

        Raises:
            SDKException: If the sync job fails, the response is empty, the response is not successful,
                or another sync job is already running for the given client(s).

        Example:
            >>> commcell = Commcell()
            >>> # Sync all remote cache clients immediately
            >>> job = commcell.sync_remote_cache()
            >>> print(f"Sync job started with Job ID: {job.job_id}")
            >>>
            >>> # Sync specific clients with a schedule pattern
            >>> schedule = {"pattern": "Daily", "time": "02:00"}
            >>> job = commcell.sync_remote_cache(client_list=["ClientA", "ClientB"], schedule_pattern=schedule)
            >>> print(f"Scheduled sync job: {job}")

        #ai-gen-doc
        """
        download = Download(self)
        return download.sync_remote_cache(
            client_list=client_list, schedule_pattern=schedule_pattern)

    def download_software(
        self,
        options: object = None,
        os_list: Optional[list] = None,
        service_pack: Optional[int] = None,
        cu_number: int = 1,
        sync_cache: bool = True,
        sync_cache_list: Optional[list] = None,
        schedule_pattern: Optional[object] = None
    ) -> 'Job':
        """Download operating system software packages to the Commcell.

        This method initiates a download job for OS packages (such as Windows or Unix) on the Commcell.
        You can specify the type of download (e.g., latest service pack, hotfixes), the list of OS packages,
        the service pack number, maintenance release number, and whether to synchronize with remote caches.

        Args:
            options: Download option specifying what to download (e.g., latest service pack, hotfixes).
                Typically, this is a value from the DownloadOptions enum.
            os_list: List of OS package identifiers to download (e.g., [DownloadPackages.WINDOWS_64.value]).
            service_pack: The service pack number to download. Required for some download options.
            cu_number: Maintenance release (cumulative update) number. Defaults to 1.
            sync_cache: If True, download and synchronize with remote caches; if False, only download.
            sync_cache_list: List of remote cache names to synchronize. If None, all caches are synchronized.
            schedule_pattern: Optional schedule pattern object to schedule the download.

        Returns:
            Job: An instance of the Job class representing the download job.

        Raises:
            SDKException: If the download job fails, the response is empty, the response is not successful,
                or another download job is already running.

        Example:
            >>> # Download the latest service pack for Windows 64-bit
            >>> job = commcell_obj.download_software()
            >>> print(f"Download job started: {job}")

            >>> # Download specific packages using DownloadOptions and DownloadPackages enums
            >>> from cvpysdk.deployment.deploymentconstants import DownloadOptions, DownloadPackages
            >>> job = commcell_obj.download_software(
            ...     options=DownloadOptions.LATEST_SERVICEPACK.value,
            ...     os_list=[DownloadPackages.WINDOWS_64.value]
            ... )
            >>> print(f"Download job started: {job}")

            >>> # Download latest hotfixes for Windows and Linux
            >>> job = commcell_obj.download_software(
            ...     options=DownloadOptions.LATEST_HOTFIXES.value,
            ...     os_list=[DownloadPackages.WINDOWS_64.value, DownloadPackages.UNIX_LINUX64.value]
            ... )
            >>> print(f"Download job started: {job}")

            >>> # Download a specific service pack and hotfixes for Mac
            >>> job = commcell_obj.download_software(
            ...     options=DownloadOptions.SERVICEPACK_AND_HOTFIXES.value,
            ...     os_list=[DownloadPackages.UNIX_MAC.value],
            ...     service_pack=13
            ... )
            >>> print(f"Download job started: {job}")

        #ai-gen-doc
        """
        download = Download(self)
        return download.download_software(
            options=options,
            os_list=os_list,
            service_pack=service_pack,
            cu_number=cu_number,
            sync_cache=sync_cache,
            sync_cache_list=sync_cache_list,
            schedule_pattern=schedule_pattern
        )

    def copy_software(
        self,
        media_loc: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        sync_cache: bool = True,
        sync_cache_list: Optional[list] = None,
        schedule_pattern: Optional[dict] = None
    ) -> 'Job':
        """Copy software media from the specified location to the Commcell.

        This method initiates a copy software job, allowing you to copy media from a local or remote location
        to the Commcell. If the media location is remote, you must provide authentication credentials.
        Optionally, you can synchronize the cache and specify a schedule pattern for the operation.

        Args:
            media_loc: The path to the media location to be used for the copy software operation.
            username: Optional; Username to authenticate to the external (remote) location. Not required for local paths.
            password: Optional; Password (base64 encoded) to authenticate to the external (remote) location.
            sync_cache: If True, downloads and synchronizes the cache; if False, only downloads the media. Default is True.
            sync_cache_list: Optional; List of remote cache names to synchronize. If None, all caches are synchronized.
            schedule_pattern: Optional; Dictionary specifying the schedule pattern for the copy software job.

        Returns:
            Job: An instance of the Job class representing the copy software job.

        Raises:
            SDKException: If the download job fails, the response is empty, the response is not successful,
                or another download job is already running.

        Example:
            # Copy software from a local directory (no authentication required)
            >>> job = commcell_obj.copy_software(media_loc="C:\\Downloads\\Media")
            >>> print(f"Copy software job started: {job}")

            # Copy software from a remote directory with authentication
            >>> job = commcell_obj.copy_software(
            ...     media_loc="\\\\subdomain.company.com\\Media",
            ...     username="domainone\\userone",
            ...     password="base64encodedpassword"
            ... )
            >>> print(f"Copy software job started: {job}")

        #ai-gen-doc
        """
        download = Download(self)
        return download.copy_software(
            media_loc=media_loc,
            username=username,
            password=password,
            sync_cache=sync_cache,
            sync_cache_list=sync_cache_list,
            schedule_pattern=schedule_pattern
        )

    def push_servicepack_and_hotfix(
            self,
            client_computers: Optional[List[str]] = None,
            client_computer_groups: Optional[List[str]] = None,
            all_client_computers: bool = False,
            all_client_computer_groups: bool = False,
            reboot_client: bool = False,
            run_db_maintenance: bool = True,
            maintenance_release_only: bool = False,
            **kwargs: Any
        ) -> object:
        """Trigger the installation of service packs and hotfixes on specified clients or client groups.

        This method initiates the deployment of service packs and hotfixes to selected client computers
        or client computer groups. You can target specific clients/groups, all clients, or all groups.
        Additional options allow for client reboot, database maintenance, and scheduling.

        Args:
            client_computers: Optional list of client machine names to install the service pack on.
            client_computer_groups: Optional list of client group names to install the service pack on.
            all_client_computers: If True, install on all client computers in the Commcell. Default is False.
            all_client_computer_groups: If True, install on all client computer groups. Default is False.
            reboot_client: If True, reboot the client after installation. Default is False.
            run_db_maintenance: If True, run database maintenance after installation. Default is True.
            maintenance_release_only: If True, only the maintenance release of the client feature release
                (if present in cache) will be installed. Default is False.
            **kwargs: Additional keyword arguments for conditional initializations.
                Supported keys:
                    - schedule_pattern (dict): JSON request for scheduling the operation.

        Returns:
            object: An instance of the Job or Task class representing the download/installation job.

        Raises:
            SDKException: If the schedule is not a dictionary, if the download job fails,
                if the response is empty or not successful, or if another download job is already running.

        Note:
            This method cannot be used for revision upgrades.

        Example:
            >>> commcell = Commcell()
            >>> job = commcell.push_servicepack_and_hotfix(
            ...     client_computers=['client1', 'client2'],
            ...     reboot_client=True,
            ...     run_db_maintenance=False
            ... )
            >>> print(f"Job started: {job}")

            >>> # Schedule installation for all clients at a specific time
            >>> schedule = {
            ...     "pattern": {
            ...         "freq_type": 1,
            ...         "active_start_time": 1620000000
            ...     }
            ... }
            >>> job = commcell.push_servicepack_and_hotfix(
            ...     all_client_computers=True,
            ...     schedule_pattern=schedule
            ... )
            >>> print(f"Scheduled job: {job}")

        #ai-gen-doc
        """
        schedule_pattern = kwargs.get("schedule_pattern", None)
        if schedule_pattern:
            if not isinstance(schedule_pattern, dict):
                raise SDKException("Commcell", "101")
        install = Install(self)
        return install.push_servicepack_and_hotfix(
            client_computers=client_computers,
            client_computer_groups=client_computer_groups,
            all_client_computers=all_client_computers,
            all_client_computer_groups=all_client_computer_groups,
            reboot_client=reboot_client,
            run_db_maintenance=run_db_maintenance,
            maintenance_release_only=maintenance_release_only,
            **kwargs
        )

    def install_software(
            self,
            client_computers: Optional[list] = None,
            windows_features: Optional[list] = None,
            unix_features: Optional[list] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
            install_path: Optional[str] = None,
            log_file_loc: Optional[str] = None,
            client_group_name: Optional[list] = None,
            storage_policy_name: Optional[str] = None,
            sw_cache_client: Optional[str] = None,
            **kwargs: dict
        ) -> 'Job':
        """Install selected software features on specified client computers.

        This method deploys the specified Windows or Unix features to the provided list of client computers.
        Additional installation options such as credentials, install paths, client groups, storage policy,
        and software cache client can be specified. Extra keyword arguments allow for advanced configuration.

        Args:
            client_computers: List of hostnames or IP addresses of the clients to install features on.
                If None, no clients are specified.
            windows_features: List of Windows feature enums to install (use WindowsDownloadFeatures enum values).
                If None, no Windows features are installed.
            unix_features: List of Unix feature enums to install (use UnixDownloadFeatures enum values).
                If None, no Unix features are installed.
            username: Username for authenticating to the client machines. If None, default credentials are used.
            password: Base64-encoded password for the client machines. If None, default credentials are used.
            install_path: Path on the client where the software should be installed. If None, default path is used.
            log_file_loc: Path on the client where installation logs should be stored. If None, default location is used.
            client_group_name: List of client group names to which the client should be added. If None, no groups are specified.
            storage_policy_name: Name of the storage policy to associate with the default subclient. If None, no policy is set.
            sw_cache_client: Name of the remote cache client or software cache to use. If None, uses the default CS cache.
            **kwargs: Additional keyword arguments for advanced installation options, such as:
                - commserv_name (str): Name of the CommServe (if user lacks view permission).
                - install_flags (dict): Dictionary of install flag values (e.g., {"preferredIPFamily": 2}).
                - db2_logs_location (dict): Dictionary specifying DB2 logs locations.

        Returns:
            Job: An instance of the Job class representing the install_software job.

        Raises:
            SDKException: If the install job fails, the response is empty, or the response indicates failure.

        Example:
            >>> from cvpysdk.deployment.deploymentconstants import UnixDownloadFeatures, WindowsDownloadFeatures
            >>> job = commcell_obj.install_software(
            ...     client_computers=['win_machine1', 'win_machine2'],
            ...     windows_features=[WindowsDownloadFeatures.FILE_SYSTEM.value],
            ...     unix_features=None,
            ...     username='admin',
            ...     password='base64password',
            ...     install_path='/opt/commvault',
            ...     log_file_loc='/var/log',
            ...     client_group_name=['My_Servers'],
            ...     storage_policy_name='My_Storage_Policy',
            ...     sw_cache_client='remote_cache_client_name',
            ...     install_flags={"preferredIPFamily": 2}
            ... )
            >>> print(f"Install job started with ID: {job.job_id}")

        Note:
            - Only one of Windows or Unix client computers should be specified in a single call.
            - Use the appropriate enums for specifying features.

        #ai-gen-doc
        """
        install = Install(self)
        return install.install_software(
            client_computers=client_computers,
            windows_features=windows_features,
            unix_features=unix_features,
            username=username,
            password=password,
            install_path=install_path,
            log_file_loc=log_file_loc,
            client_group_name=client_group_name,
            storage_policy_name=storage_policy_name,
            sw_cache_client=sw_cache_client,
            **kwargs)

    @property
    def remote_cache_clients(self) -> list:
        """Retrieve the list of remote cache clients configured for the current Admin or Tenant.

        Returns:
            list: A list containing the names or identifiers of remote cache clients configured for this Commcell.

        Example:
            >>> commcell = Commcell()
            >>> remote_caches = commcell.remote_cache_clients
            >>> print(f"Remote cache clients: {remote_caches}")

        #ai-gen-doc
        """
        try:
            if self._commserv_cache is None:
                self._commserv_cache = CommServeCache(self)

            return self._commserv_cache.get_remote_cache_clients()

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def enable_auth_code(self) -> str:
        """Enable Auth Code generation for installation on the Commcell.

        Sends a request to the server to enable Auth Code, which is required for installation operations.
        Returns the generated Auth Code as a string.

        Returns:
            The Auth Code generated by the server.

        Raises:
            SDKException: If enabling Auth Code generation fails, the response is empty, or the response indicates failure.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> auth_code = commcell.enable_auth_code()
            >>> print(f"Generated Auth Code: {auth_code}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GENERATE_AUTH_CODE'] % 0
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Client', '102', 'Failed to set auth code, with error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()['organizationProperties']['authCode']

    def disable_auth_code(self) -> None:
        """Disable the authentication code requirement at the Commcell level.

        This method turns off the requirement for an authentication code when performing operations 
        on the Commcell. It is useful for environments where additional authentication is not needed.

        Raises:
            SDKException: If disabling the auth code fails, the response is empty, or the response indicates failure.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> commcell.disable_auth_code()
            >>> print("Auth code requirement disabled successfully.")

        #ai-gen-doc
        """
        request_json = {
            "organizationInfo": {
                "organization": {
                    "shortName": {
                        "id": 0
                    }
                },
                "organizationProperties": {
                    "enableAuthCodeGen": False
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ORGANIZATIONS'], request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Commcell', '108', 'Failed to disable authcode: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_shared_laptop(self) -> None:
        """Enable the Shared Laptop feature on the Commcell.

        This method sends a request to the server to enable the Shared Laptop functionality
        for the Commcell. It raises an exception if the operation fails or if the server
        response is invalid.

        Raises:
            SDKException: If the server response is empty, the request fails, or the response indicates failure.

        Example:
            >>> commcell = Commcell()
            >>> commcell.enable_shared_laptop()
            >>> print("Shared Laptop feature enabled successfully.")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ENABLE_SHARED_LAPTOP']
        )

        if flag:
            if response.json():
                response = response.json().get('response', [{}])[0]
                if not response:
                    raise SDKException('Response', '102')
                if response.get('errorCode', -1) != 0:
                    raise SDKException(
                        'Response', '101', 'Failed to enable shared laptop')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_shared_laptop(self) -> None:
        """Disable the Shared Laptop feature on the Commcell.

        This method sends a request to the server to disable the Shared Laptop functionality
        for the entire Commcell. It is typically used by administrators to restrict access
        to shared laptop features across all clients managed by the Commcell.

        Raises:
            SDKException: If the server response is empty, the request fails, or the response
                indicates an unsuccessful operation.

        Example:
            >>> commcell = Commcell('server_name', 'username', 'password')
            >>> commcell.disable_shared_laptop()
            >>> print("Shared Laptop feature has been disabled on the Commcell.")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['DISABLE_SHARED_LAPTOP']
        )

        if flag:
            if response.json():
                response = response.json().get('response', [{}])[0]
                if not response:
                    raise SDKException('Response', '102')
                if response.get('errorCode', -1) != 0:
                    raise SDKException(
                        'Response', '101', 'Failed to disable shared laptop')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_privacy(self, otp: str = None) -> None:
        """Enable data privacy on the Commcell.
        Args:
                otp (str): otp for two-factor authentication operation.

        This method activates data privacy features for the Commcell, enhancing the security of sensitive information.

        Example:
            >>> commcell = Commcell()
            >>> commcell.enable_privacy()
            >>> print("Data privacy has been enabled on the Commcell.")

        #ai-gen-doc
        """
        if self.is_privacy_enabled is True:
            return

        self.set_privacy(True, otp=otp)

    def disable_privacy(self, otp: str = None) -> None:
        """Disable data privacy on the Commcell.
        Args:
                otp (str): otp for two-factor authentication operation.

        This method allows users to turn off data privacy features for the Commcell instance.

        Example:
            >>> commcell = Commcell()
            >>> commcell.disable_privacy()
            >>> print("Data privacy has been disabled on the Commcell.")

        #ai-gen-doc
        """
        if self.is_privacy_enabled is False:
            return

        self.set_privacy(False, otp=otp)

    def set_privacy(self, value: bool, otp: str = None) -> None:
        """Enable or disable privacy settings for the Commcell.

        Args:
            value: Set to True to enable privacy, or False to disable privacy.
            otp (str): otp for two-factor authentication operation.

        Raises:
            SDKException: If the response is empty, if disabling privacy fails, or if the response indicates failure.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> commcell.set_privacy(True)   # Enable privacy
            >>> commcell.set_privacy(False)  # Disable privacy

        #ai-gen-doc
        """
        url = self._services['PRIVACY_DISABLE']
        if value:
            url = self._services['PRIVACY_ENABLE']
        headers = None
        if otp:
            headers = self._headers.copy()
            headers["otp"] = otp

        flag, response = self._cvpysdk_object.make_request(
            'PUT', url, headers=headers
        )

        if flag:
            if response and response.json():
                response = response.json().get('response', [{}])[0]
                if not response:
                    raise SDKException('Response', '102')
                if response.get('errorCode', -1) != 0:
                    error_string = response.json().get('errorString')
                    raise SDKException(
                        'Commcell', '108', error_string)
                self.get_commcell_properties()

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_commcell_properties(self) -> Dict[str, Any]:
        """Retrieve the properties of the Commcell.

        Returns:
            Dictionary containing Commcell properties such as host name, authentication settings,
            network error retry configurations, privacy settings, and more.

            Example keys in the returned dictionary:
                - "hostName": str
                - "enableSharedLaptopUsage": bool
                - "enableTwoFactorAuthentication": bool
                - "networkErrorRetryCount": int
                - "useUPNForEmail": bool
                - "flags": int
                - "description": str
                - "networkErrorRetryFreq": int
                - "autoClientOwnerAssignmentType": int
                - "networkErrorRetryFlag": bool
                - "allowUsersToEnablePasskey": bool
                - "autoClientOwnerAssignmentValue": str
                - "enablePrivacy": bool
                - "twoFactorAuthenticationInfo": dict (e.g., {"mode": int})

        Example:
            >>> commcell = Commcell()
            >>> properties = commcell.get_commcell_properties()
            >>> print(properties["hostName"])
            >>> print(properties.get("enableTwoFactorAuthentication", False))
            >>> # Access nested info
            >>> two_factor_info = properties.get("twoFactorAuthenticationInfo", {})
            >>> print(two_factor_info.get("mode"))

        #ai-gen-doc
        """
        url = self._services['SET_COMMCELL_PROPERTIES']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                self._commcell_properties = response.get("commCellInfo").get("generalInfo")
                return self._commcell_properties
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_commcell_organization_properties(self) -> Dict[str, Any]:
        """Retrieve the organization properties for the Commcell.

        Returns:
            A dictionary containing the organization properties of the Commcell.

        Example:
            >>> commcell = Commcell()
            >>> org_props = commcell.get_commcell_organization_properties()
            >>> print(org_props)
            >>> # Access specific organization property
            >>> org_name = org_props.get('organizationName')
            >>> print(f"Organization Name: {org_name}")

        #ai-gen-doc
        """
        url = self._services['ORGANIZATION'] % '0'
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                passkey_details = response.get('organizationInfo').get('organizationProperties')
                return passkey_details
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_email_settings(self) -> Dict[str, Any]:
        """Retrieve the Email Server (SMTP) settings configured for the Commcell.

        Returns:
            Dictionary containing the email server (SMTP) settings for the Commcell.

        Example:
            >>> commcell = Commcell()
            >>> email_settings = commcell.get_email_settings()
            >>> print(email_settings)
            >>> # Output might include keys like 'server', 'port', 'sender', etc.

        #ai-gen-doc
        """
        url = self._services['EMAIL_SERVER']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                return response
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def set_email_settings(self, smtp_server: str, sender_name: str, sender_email: str, **kwargs: Any) -> None:
        """Configure the Email Server (SMTP) settings for the Commcell.

        This method sets up the SMTP server details, sender information, and additional 
        email configuration options for notifications and alerts.

        Args:
            smtp_server: Hostname or IP address of the SMTP server.
            sender_name: Name to be used as the sender in outgoing emails.
            sender_email: Email address to be used as the sender.
            **kwargs: Optional key-value pairs for additional configuration:
                - enable_ssl (bool): Whether SSL is enabled for the email server (default: False).
                - start_tls (bool): Whether TLS is enabled for the email server (default: False).
                - smtp_port (int): Port number for the SMTP server (default: 25).
                - username (str): Username for SMTP authentication.
                - password (str): Password for SMTP authentication.

        Returns:
            None

        Raises:
            SDKException: If invalid argument types are provided, if the email server update fails,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> commcell = Commcell()
            >>> commcell.set_email_settings(
            ...     smtp_server="smtp.example.com",
            ...     sender_name="Backup Admin",
            ...     sender_email="admin@example.com",
            ...     enable_ssl=True,
            ...     smtp_port=465,
            ...     username="smtp_user",
            ...     password="smtp_pass"
            ... )
            >>> print("Email server settings updated successfully.")

        #ai-gen-doc
        """

        if not (isinstance(smtp_server, str) and isinstance(sender_email, str)
                and isinstance(sender_name, str)):
            raise SDKException("Commcell", "101")

        enable_ssl = kwargs.get("enable_ssl", False)
        start_tls = kwargs.get("start_tls", False)
        smtp_port = kwargs.get("smtp_port", 25)
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")

        if not (isinstance(enable_ssl, bool) and isinstance(smtp_port, int)
                and isinstance(username, str) and isinstance(password, str)):
            raise SDKException("Commcell", "101")

        request_json = {"smtpInfo":
                            {"enableSSL": enable_ssl,
                             "startTLS": start_tls,
                             "smtpServer": smtp_server,
                             "smtpPort": smtp_port,
                             "useAuthentication": False,
                             "maxMailServerSize": 0,
                             "userInfo": {
                                 "password": username,
                                 "userName": password
                             },
                             "senderInfo": {
                                 "senderName": sender_name,
                                 "senderAddress": sender_email
                             }
                             }
                        }
        url = self._services['EMAIL_SERVER']
        flag, response = self._cvpysdk_object.make_request(
            'POST', url, request_json
        )
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException('Response', '101', self._update_response_(response.text))
                return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_password_encryption_config(self) -> Dict[str, Any]:
        """Retrieve the password encryption configuration for the Commcell.

        Returns:
            Dictionary containing the password encryption configuration details:
                - "keyFilePath": Path to the encryption key file (str)
                - "keyProviderName": Name of the key provider (str)
                - "isKeyMovedToFile": Indicates if the key has been moved to a file (bool)

        Example:
            >>> commcell = Commcell()
            >>> config = commcell.get_password_encryption_config()
            >>> print(config["keyFilePath"])
            >>> print(config["keyProviderName"])
            >>> print(config["isKeyMovedToFile"])

        #ai-gen-doc
        """
        pass__enc_config = {}

        url = self._services['PASSWORD_ENCRYPTION_CONFIG']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                for key, value in response.items():
                    pass__enc_config.update({key: value})
                return pass__enc_config
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_security_associations(self) -> Dict[str, List[List[str]]]:
        """Retrieve the security associations configured for the Commcell.

        Returns:
            A dictionary mapping user names to lists of permission groups. Each permission group is represented as a list of permission strings.

            Example output:
                {
                    'master': [
                        ['Array Management'],
                        ['Create Role', 'Edit Role', 'Delete Role'],
                        ['Master']
                    ],
                    'User2': [
                        ['View']
                    ]
                }

        Example:
            >>> commcell = Commcell()
            >>> associations = commcell.get_security_associations()
            >>> print(associations)
            >>> # Access permissions for a specific user
            >>> master_permissions = associations.get('master', [])
            >>> print(f"Master user permissions: {master_permissions}")

        #ai-gen-doc
        """
        security_associations = {}
        value_list = {}
        url = self._services['SECURITY_ASSOCIATION'] + '/1/2'
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                security_list = response.get('securityAssociations')[0].get('securityAssociations').get('associations')
                for list_item in security_list:
                    name = list_item.get('userOrGroup')[0].get('userGroupName') or \
                        list_item.get('userOrGroup')[0].get('userName') or \
                        list_item.get('userOrGroup')[0].get('providerDomainName') + '\\' + \
                        list_item.get('userOrGroup')[0].get('externalGroupName')
                    value = []
                    if list_item.get('properties').get('role'):
                        value.append(list_item.get('properties').get('role').get('roleName'))
                    elif list_item.get('properties').get('categoryPermission'):
                        for sub_list_item in list_item.get('properties').get('categoryPermission').get(
                                'categoriesPermissionList'):
                            value.append(sub_list_item.get('permissionName'))
                    if name in value_list:
                        value_list[name].append(value)
                        value_list[name].sort()
                    else:
                        value_list[name] = [value]
                    security_associations.update({name: value_list[name]})
                return security_associations
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_default_plan(self) -> List[Dict[str, Any]]:
        """Retrieve the default backup plan at the Commcell level.

        This method executes a request to the server to obtain the default plan configuration 
        for the Commcell. The default plan is independent of any organization and uses an ID of 0.

        Returns:
            A list of dictionaries, each containing details about a default plan and its subtype.
            Example format:
                [
                    {
                        "subtype": "File system plan",
                        "plan": {
                            "planName": "Gold plan",
                            "planId": 2
                        }
                    }
                ]

        Example:
            >>> commcell = Commcell()
            >>> default_plans = commcell.get_default_plan()
            >>> for plan_info in default_plans:
            ...     print(f"Subtype: {plan_info['subtype']}, Plan Name: {plan_info['plan']['planName']}")
            >>> # Output:
            >>> # Subtype: File system plan, Plan Name: Gold plan

        #ai-gen-doc
        """
        default_plan_details = []
        plan_sub_type = {
            16777223: 'DLO plan',
            33554437: 'Server plan',
            33554439: 'Laptop plan',
            33579013: 'Database plan',
            67108869: 'Snap plan',
            50331655: 'File system plan',
            83886085: 'VSA system plan',
            83918853: 'VSA Replication plan',
            100859907: 'ExchangeUser plan',
            100794372: 'ExchangeJournal plan',
            117506053: 'DataClassification plan',
            1: 'Ediscovery plan'
        }
        url = self._services['ORGANIZATION'] % '0' + '/defaultplan'
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                plan_details = response.get('organizationInfo').get('organizationProperties')
                if "defaultPlans" in plan_details:
                    plan_list = plan_details.get('defaultPlans')
                    for default_plan in plan_list:
                        default_plan_details.append({"subtype": plan_sub_type.get(default_plan.get('subtype')),
                                                     "plan": {
                                                         "planName": default_plan.get('plan').get('planName'),
                                                         "planId": default_plan.get('plan').get('planId')}
                                                     })
                return default_plan_details
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def set_default_plan(self, plan_name: str) -> None:
        """Set the default plan for the Commcell at the global level.

        This method sends a request to the server to set the specified plan as the default plan 
        for the Commcell. The operation is independent of any organization, as the organization ID is set to 0.

        Args:
            plan_name: The name of the plan to set as the default.

        Raises:
            SDKException: If the request to set the default plan fails, the response is empty, 
                or the response indicates failure.

        Example:
            >>> commcell = Commcell()
            >>> commcell.set_default_plan("StandardBackupPlan")
            >>> print("Default plan set successfully.")

        #ai-gen-doc
        """

        request_json = {
            "organizationInfo": {
                "organization": {
                    "shortName": {
                        "id": 0
                    }
                },
                "organizationProperties": {
                    "defaultPlansOperationType": 1,
                    "defaultPlans": [
                        {
                            "plan": {
                                "planName": plan_name
                            }
                        }
                    ]
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ORGANIZATIONS'], request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Client', '102', 'Failed to set default plan, with error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def execute_qcommand(self, command: str, input_xml: Optional[str] = None) -> object:
        """Execute a QCommand on the Commcell using the ExecuteQCommand API.

        Deprecated:
            This method is deprecated and will be removed in a future version.
            Use `execute_qcommand_v2` instead.

        Args:
            command: The QCommand string to be executed on the Commcell.
            input_xml: Optional XML body to be sent with the command. Defaults to None.

        Returns:
            The response object from the requests library containing the result of the QCommand execution.

        Raises:
            SDKException: If the response is empty or indicates a failure.

        Example:
            >>> commcell = Commcell()
            >>> response = commcell.execute_qcommand('QCommandName', '<inputXML></inputXML>')
            >>> print(response.status_code)
            >>> print(response.text)

        #ai-gen-doc
        """
        from urllib.parse import (urlencode, quote)

        headers = self._headers.copy()
        headers['Content-type'] = 'application/x-www-form-urlencoded'

        payload = {
            'command': command
        }

        if input_xml:
            payload['inputRequestXML'] = input_xml

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXEC_QCOMMAND'], urlencode(payload, quote_via=quote), headers=headers
        )

        if flag:
            return response
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def execute_qcommand_v2(self, command: str, input_data: Union[str, dict, None] = None) -> object:
        """Execute a QCommand API request on the Commcell.

        This method sends a QCommand to the Commcell server, optionally including input data 
        in XML, JSON, or dictionary format. The response is returned as a requests.Response object.

        Args:
            command: The QCommand string to be executed on the Commcell.
            input_data: Optional XML, JSON, or dictionary body to include with the request.

        Returns:
            The response object from the requests library containing the result of the QCommand.

        Raises:
            SDKException: If the response is empty or indicates a failure.

        Example:
            >>> commcell = Commcell()
            >>> response = commcell.execute_qcommand_v2('QCommandName', {'param1': 'value1'})
            >>> print(response.status_code)
            >>> print(response.text)
            # The response object contains the server's reply to the QCommand.

        #ai-gen-doc
        """

        headers = self._headers.copy()
        dict_data = dict()

        if input_data and not isinstance(input_data, dict):
            try:
                dict_data = xmltodict.parse(input_data, attr_prefix='')
            except Exception as e:
                try:
                    import json
                    dict_data = json.loads(input_data)
                except Exception as e:
                    raise SDKException('Commcell', '107', 'Unable to parse the input data as either XML or JSON')

        flag, response = self._cvpysdk_object.make_request(
            'POST', f"{self._services['QCOMMAND']}/{command}", dict_data, headers=headers
        )

        if flag:
            return response
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_associations_to_saml_app(self, saml_app_name: str, saml_app_key: str, props: str, user_to_be_added: str) -> None:
        """Add a user association to the specified SAML application.

        This method adds the given user under the associations tab of the specified SAML app.
        The properties string is included in the XML request sent to the Commcell server.

        Args:
            saml_app_name: The name of the SAML application to add associations for.
            saml_app_key: The application key of the SAML app.
            props: Properties to be included in the XML request.
            user_to_be_added: The user to be associated with the SAML app.

        Raises:
            SDKException: If input data is invalid, the response is empty, or the response indicates failure.

        Example:
            >>> commcell = Commcell()
            >>> commcell.add_associations_to_saml_app(
            ...     saml_app_name="MySAMLApp",
            ...     saml_app_key="abc123",
            ...     props="<property name='role' value='admin'/>",
            ...     user_to_be_added="jdoe"
            ... )
            >>> print("User association added successfully.")

        #ai-gen-doc
        """

        xml_execute_command = """
            <App_SetClientThirdPartyAppPropReq opType="3">
            <clientThirdPartyApps appDescription="" appKey="{0}" appName="{1}" appType="2" flags="2" isCloudApp="0" isEnabled="1">
                {2}
                <UserMappings/>
                <assocTree _type_="13" userName="{3}"/>
            </clientThirdPartyApps>
        </App_SetClientThirdPartyAppPropReq>
        	"""\
            .format(str(saml_app_key), saml_app_name, props, user_to_be_added)
        self._qoperation_execute(xml_execute_command)

    def _get_registered_commcells(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all registered routing Commcell instances.

        This method fetches the registered Commcell objects associated with the current Commcell.
        Note: This is distinct from service Commcells. For service Commcells, use the `service_commcells` class.

        Returns:
            Dictionary mapping Commcell names to their respective information.
            Example structure:
                {
                    "commcell_name1": {
                        # related information for commcell1
                    },
                    "commcell_name2": {
                        # related information for commcell2
                    }
                }

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> commcell = Commcell()
            >>> registered_commcells = commcell._get_registered_commcells()
            >>> for name, info in registered_commcells.items():
            ...     print(f"Commcell: {name}, Info: {info}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._services['GET_REGISTERED_COMMCELLS'])
        if flag:
            if response.json() and 'commcellsList' in response.json():
                register_commcells_dict = {}

                for registered_commcell in response.json()['commcellsList']:
                    register_commcells_dict[registered_commcell['commCell']['commCellName']] = registered_commcell
                return register_commcells_dict
            else:
                return {}
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def register_commcell(self, commcell_name: str, admin_username: str, admin_password: str, **kwargs: Any) -> None:
        """Register a new Commcell with the specified administrative credentials.

        This method registers a Commcell using the provided Command Center hostname or URL,
        along with the credentials of a user who has administrative rights on the target Commcell.
        For service Commcell registration, use the `service_commcells.add` method instead.

        Args:
            commcell_name: The Command Center hostname or the complete Command Center URL of the Commcell to register.
            admin_username: Username of a user with administrative rights on the Commcell.
            admin_password: Password for the specified administrative user.
            **kwargs: Additional optional parameters for registration.

        Raises:
            SDKException: If the registration fails, the response is empty, or there is no response.

        Example:
            >>> commcell = Commcell()
            >>> commcell.register_commcell(
            ...     commcell_name="cc.example.com",
            ...     admin_username="admin",
            ...     admin_password="password123"
            ... )
            >>> print("Commcell registered successfully")
            # For service Commcell registration, use:
            >>> # commcell.service_commcells.add(...)

        #ai-gen-doc
        """
        commcell_url = commcell_name.lower()
        if 'http' not in commcell_name:
            commcell_url = f"https://{commcell_name}/commandcenter"

        payload = {
            "serviceCommcelWebconsoleUrl": commcell_url,
            "username": admin_username,
            "isIDPCommcell": False,
            "displayName": kwargs.get('commcell_displayname'),
            "userOrGroup": [],
            "password": b64encode(admin_password.encode()).decode()
        } | kwargs.get('custom_payload', {})

        self.wrap_request(
            'POST', 'REGISTRATION',
            req_kwargs={'payload': payload},
            sdk_exception=('CommcellRegistration', '101')
        )
        self._registered_commcells = None

    def get_redirect_list(self, login: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve the list of service Commcell redirects available for a user.

        This method returns a list of service Commcell redirects based on the provided login name or email.
        If no login is specified, it retrieves redirects for the current user.

        Args:
            login: Optional login name or email address of the user. If not provided, uses the current user's credentials.

        Returns:
            A list of dictionaries, each representing a service Commcell redirect available to the user.

        Raises:
            RuntimeError: If the response is empty or no response is received from the server.

        Example:
            >>> commcell = Commcell()
            >>> redirects = commcell.get_redirect_list('user@example.com')
            >>> print(f"Available redirects: {redirects}")
            >>> # Each item in 'redirects' is a dictionary with redirect details

        #ai-gen-doc
        """
        login = login or self.commcell_username
        login = login.lower()
        flag, response = self._cvpysdk_object.make_request('GET', self._services['REDIRECT_LIST'] % login)
        if flag:
            if response.json() and 'AvailableRedirects' in response.json():
                service_commcell_list = []
                for ser_comm in response.json()['AvailableRedirects']:
                    service_commcell_list.append(
                        urlparse(ser_comm['redirectUrl']).netloc
                    )
                return service_commcell_list
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def is_service_commcell(self) -> bool:
        """Indicate whether this Commcell instance is a service Commcell.

        Returns:
            True if the Commcell is configured as a service Commcell, False otherwise.

        Example:
            >>> commcell = Commcell()
            >>> if commcell.is_service_commcell:
            ...     print("This is a service Commcell.")
            ... else:
            ...     print("This is a regular Commcell.")

        #ai-gen-doc
        """
        return self._is_service_commcell

    @property
    def master_saml_token(self) -> str:
        """Get the SAML token for the master Commcell.

        Returns:
            str: The SAML token string associated with the master Commcell.

        Example:
            >>> commcell = Commcell()
            >>> token = commcell.master_saml_token  # Use dot notation for property access
            >>> print(f"Master SAML token: {token}")

        #ai-gen-doc
        """
        return self._master_saml_token

    @property
    def master_commcell(self) -> 'Commcell':
        """Get the master Commcell object associated with this Commcell instance.

        Returns:
            Commcell: The master Commcell object.

        Example:
            >>> commcell = Commcell()
            >>> master = commcell.master_commcell  # Use dot notation for property access
            >>> print(f"Master Commcell: {master}")
            >>> # The returned Commcell object can be used for further operations

        #ai-gen-doc
        """
        return self._master_commcell

    @property
    def two_factor_authentication(self) -> 'TwoFactorAuthentication':
        """Get the TwoFactorAuthentication instance associated with this Commcell.

        Returns:
            TwoFactorAuthentication: An object for managing two-factor authentication settings and operations.

        Example:
            >>> commcell = Commcell()
            >>> twofa = commcell.two_factor_authentication  # Access property via dot notation
            >>> print(f"Two-factor authentication object: {twofa}")
            >>> # Use the returned TwoFactorAuthentication object for further 2FA management

        #ai-gen-doc
        """
        try:
            if self._tfa is None:
                self._tfa = TwoFactorAuthentication(self)
            return self._tfa
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def is_tfa_enabled(self) -> bool:
        """Check if two-factor authentication (TFA) is enabled for this Commcell.

        Returns:
            True if TFA is enabled, False otherwise.

        Example:
            >>> commcell = Commcell()
            >>> if commcell.is_tfa_enabled:
            ...     print("Two-factor authentication is enabled.")
            ... else:
            ...     print("Two-factor authentication is not enabled.")

        #ai-gen-doc
        """
        return self.two_factor_authentication.is_tfa_enabled

    @property
    def tfa_enabled_user_groups(self) -> List[Dict[str, Any]]:
        """Get the list of user groups with two-factor authentication (TFA) enabled.

        This property returns a list of dictionaries, each containing the user group ID and name
        for groups where TFA is enabled via user group inclusion.

        Returns:
            List of dictionaries with user group details. Each dictionary contains:
                - "userGroupId": The unique ID of the user group (int).
                - "userGroupName": The name of the user group (str).

        Example:
            >>> commcell = Commcell()
            >>> tfa_groups = commcell.tfa_enabled_user_groups  # Use dot notation for property
            >>> print(tfa_groups)
            >>> # Output:
            >>> # [
            >>> #     {"userGroupId": 1, "userGroupName": "dummy"},
            >>> #     {"userGroupId": 2, "userGroupName": "admins"}
            >>> # ]

        #ai-gen-doc
        """
        return self.two_factor_authentication.tfa_enabled_user_groups

    @property
    def is_linux_commserv(self) -> Optional[bool]:
        """Check if the CommServer is installed on a Linux machine.

        Returns:
            True if the CommServer is installed on a Linux machine.
            False if the CommServer is not installed on Linux.
            None if unable to determine the CommServ OS type (e.g., due to insufficient permissions).

        Note:
            To determine the CommServ OS type, the logged-in user must have access to the CommServ client.

        Example:
            >>> commcell = Commcell()
            >>> is_linux = commcell.is_linux_commserv  # Use dot notation for property
            >>> if is_linux is True:
            ...     print("CommServer is running on Linux.")
            ... elif is_linux is False:
            ...     print("CommServer is not running on Linux.")
            ... else:
            ...     print("Unable to determine CommServer OS type.")

        #ai-gen-doc
        """
        try:
            if self._is_linux_commserv is None and self.clients.has_client(self.commserv_name):
                self._is_linux_commserv = 'unix' in self.commserv_client.os_info.lower()
        except SDKException:
            # If unable to determine the CommServ OS type, set it to Windows
            self._is_linux_commserv = False
        return self._is_linux_commserv

    @property
    def default_timezone(self) -> str:
        """Get the default timezone used for all operations performed via cvpysdk.

        Returns:
            The default timezone as a string.

        Example:
            >>> commcell = Commcell()
            >>> tz = commcell.default_timezone  # Use dot notation for property access
            >>> print(f"Default timezone: {tz}")
            >>> # The returned value is the timezone string used by the Commcell

        #ai-gen-doc
        """
        return 'UTC' if self.is_linux_commserv else '(UTC) Coordinated Universal Time'

    @property
    def is_passkey_enabled(self) -> bool:
        """Check if Passkey authentication is enabled on the Commcell.

        Returns:
            True if Passkey is enabled; False otherwise.

        Example:
            >>> commcell = Commcell()
            >>> if commcell.is_passkey_enabled:
            ...     print("Passkey authentication is enabled.")
            ... else:
            ...     print("Passkey authentication is not enabled.")

        #ai-gen-doc
        """
        org_prop = self.get_commcell_organization_properties()
        return True if org_prop.get('advancedPrivacySettings', {}).get('authType', 0) == 2 else False

    @property
    def databases(self) -> List[Dict[str, Any]]:
        """Get the list of databases associated with the Commcell.

        Returns:
            List of dictionaries, each containing details about a database associated with the Commcell.

        Example:
            >>> commcell = Commcell()
            >>> db_list = commcell.databases  # Use dot notation for property access
            >>> print(f"Total databases: {len(db_list)}")
            >>> if db_list:
            >>>     print(f"First database details: {db_list[0]}")

        #ai-gen-doc
        """
        if self._databases is None:
            flag, response = self._cvpysdk_object.make_request('GET', self._services['DATABASES'])
            if flag:
                if response.json():
                    response = response.json()
                    self._databases = [database['backupset']['backupsetName'] for database in response['dbInstance']]
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return self._databases

    @property
    def database_instances(self) -> List[str]:
        """Get the list of database instance names associated with the Commcell.

        Returns:
            List of strings, each representing the name of a database instance configured in the Commcell.

        Example:
            >>> commcell = Commcell()
            >>> db_instance_names = commcell.database_instances  # Use dot notation for property access
            >>> print(f"Total database instances: {len(db_instance_names)}")
            >>> # Access the name of the first database instance
            >>> if db_instance_names:
            ...     first_instance_name = db_instance_names[0]
            ...     print(f"First instance name: {first_instance_name}")

        #ai-gen-doc
        """
        if self._db_instances is None:
            flag, response = self._cvpysdk_object.make_request('GET', self._services['DB_INSTANCES'])
            if flag:
                if response.json():
                    response = response.json()
                    self._db_instances = [instance['instance']['instanceName'] for instance in response['dbInstance']]
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return self._db_instances

    @property
    def database_instant_clones(self) -> List[Dict[str, Any]]:
        """Get the list of active database instant clone jobs on the Commcell.

        Returns:
            List of dictionaries, each containing details of an active database instant clone job.

        Example:
            >>> commcell = Commcell()
            >>> instant_clones = commcell.database_instant_clones  # Use dot notation for property
            >>> print(f"Active instant clone jobs: {instant_clones}")
            >>> # Each item in the list is a dictionary with job details

        #ai-gen-doc
        """
        if self._db_instant_clones is None:
            flag, response = self._cvpysdk_object.make_request('GET', self._services['DB_INSTANT_CLONES'])
            if flag:
                if response.json():
                    response = response.json()
                    self._db_instant_clones = [clone['cloneJobId'] for clone in response['clones']]
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return self._db_instant_clones

    def get_aws_backup_gateway_cft_url(self, region_name: str = 'us-east-1', authentication: str = "IAM Role", platform: str = "linux") -> str:
        """Retrieve the AWS CloudFormation Template (CFT) URL to launch a Backup Gateway.

        Args:
            region_name: AWS region where the Backup Gateway should be launched (e.g., 'us-east-1').
            authentication: Type of IAM authentication to associate with the EC2 instance.
                Supported values:
                    - "IAM Role"
                    - "Access and Secret Key"
                    - "STS Assume Role"
            platform: Operating system of the Backup Gateway to be created (e.g., 'linux').

        Returns:
            The AWS CloudFormation URL as a string, which can be used to launch the Backup Gateway stack.

        Example:
            >>> commcell = Commcell()
            >>> cft_url = commcell.get_aws_backup_gateway_cft_url(
            ...     region_name="us-west-2",
            ...     authentication="IAM Role",
            ...     platform="linux"
            ... )
            >>> print(f"Launch Backup Gateway using CFT URL: {cft_url}")

        #ai-gen-doc
        """
        if "sts" in authentication.lower():
            authentication = 3
        elif "key" in authentication.lower():
            authentication = 2
        else:
            authentication = 1
        base_url = self._services['GET_AWS_CFT'] % (platform, region_name, authentication)
        flag, response = self._cvpysdk_object.make_request('GET', base_url)
        if flag:
            if response.json():
                return response.json().get("quickLinkUrl")
            else:
                raise SDKException('Response', '102', 'Failed to get CFT URL')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def job_logs_emails(self) -> List[str]:
        """Get the list of email servers associated with the Commcell for job log notifications.

        Returns:
            List of email server addresses as strings.

        Example:
            >>> commcell = Commcell()
            >>> email_servers = commcell.job_logs_emails  # Use dot notation for property access
            >>> print("Configured email servers:", email_servers)
            >>> # Output might be: ['smtp1.example.com', 'smtp2.example.com']

        #ai-gen-doc
        """
        return self._job_logs_emails

    @job_logs_emails.setter
    def job_logs_emails(self, email_servers: List[str]) -> None:
        """Set the list of email servers associated with the Commcell for job log notifications.

        Args:
            email_servers: A list of email server addresses (as strings) to be used for sending job log emails.

        Example:
            >>> commcell = Commcell()
            >>> commcell.job_logs_emails = ["smtp1.example.com", "smtp2.example.com"]
            >>> # The Commcell will now use these servers for job log email notifications

        #ai-gen-doc
        """
        if isinstance(email_servers, list):
            self._job_logs_emails = email_servers
        else:
            raise SDKException('Commcell', '101', 'Email servers should be a list')

    def enable_tfa(self, user_groups: Optional[List[str]] = None, usernameless: bool = False,
                   passwordless: bool = False, otp: str = None) -> None:
        """Enable two-factor authentication (TFA) on the Commcell.

        This method enables TFA for the Commcell, optionally restricting it to specific user groups.
        You can also allow usernameless and/or passwordless login as part of the TFA configuration.

        Args:
            user_groups: Optional list of user group names for which TFA should be enabled. If None, TFA is enabled for all applicable users.
            usernameless: If True, allows usernameless login as part of TFA.
            passwordless: If True, allows passwordless login as part of TFA.
            otp (str): otp for two-factor authentication operation.

        Example:
            >>> commcell = Commcell()
            >>> # Enable TFA for all users
            >>> commcell.enable_tfa()
            >>> # Enable TFA for specific user groups with usernameless login
            >>> commcell.enable_tfa(user_groups=['Admins', 'BackupOperators'], usernameless=True)
            >>> # Enable TFA with passwordless login for all users
            >>> commcell.enable_tfa(passwordless=True)

        #ai-gen-doc
        """
        self.two_factor_authentication.enable_tfa(
            user_groups=user_groups, usernameless=usernameless, passwordless=passwordless, otp=otp
        )

    def disable_tfa(self, otp: str = None) -> None:
        """Disable two-factor authentication (TFA) on this Commcell.
        Args:
            otp (str): otp for two-factor authentication operation.

        This method turns off TFA for the Commcell, allowing users to log in without requiring a second authentication factor.

        Example:
            >>> commcell = Commcell()
            >>> commcell.disable_tfa()
            >>> print("Two-factor authentication has been disabled.")

        #ai-gen-doc
        """
        self.two_factor_authentication.disable_tfa(otp=otp)

    def _get_commserv_metadata(self) -> Dict[str, Any]:
        """Load and retrieve metadata for the CommServ associated with this Commcell instance.

        This method fetches metadata such as the CommServ redirect URL and certificate,
        and updates the Commcell instance attributes accordingly.

        Returns:
            Dictionary containing CommServ metadata, including:
                - 'commserv_redirect_url': The URL for CommServ redirection.
                - 'commserv_certificate': The CommServ certificate string.

        Raises:
            SDKException: If unable to retrieve CommServ details or if the response is unsuccessful.

        Example:
            >>> commcell = Commcell()
            >>> metadata = commcell._get_commserv_metadata()
            >>> print(metadata['commserv_redirect_url'])
            >>> print(metadata['commserv_certificate'])

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request('GET', self._services['COMMCELL_METADATA'])

        if flag:
            if response.json():
                    commserv_metadata = {
                        'commserv_redirect_url': response.json()['redirectUrl'],
                        'commserv_certificate': response.json()['certificate']
                    }
                    return commserv_metadata
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_commserv_oem_id(self) -> int:
        """Retrieve the CommServe OEM ID for the current Commcell instance.

        This method loads and returns the OEM ID associated with the CommServe server.
        The OEM ID is typically used for identifying the specific OEM version of the CommServe.

        Returns:
            The CommServe OEM ID as an integer.

        Raises:
            SDKException: If unable to retrieve CommServe details or if the response is unsuccessful.

        Example:
            >>> commcell = Commcell()
            >>> oem_id = commcell._get_commserv_oem_id()
            >>> print(f"CommServe OEM ID: {oem_id}")

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request('GET', self._services['GET_OEM_ID'])

        if flag:
            if response.json():
                    return response.json()['id']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def operator_companies(self) -> Dict[str, int]:
        """Get a mapping of operator company names to their IDs for the current user.

        This property returns a dictionary where each key is the name of an operator company,
        and each value is the corresponding company ID. Only companies available for the
        currently logged-in user are included.

        Returns:
            Dict[str, int]: A dictionary mapping operator company names to their IDs.

        Example:
            >>> commcell = Commcell()
            >>> companies = commcell.operator_companies  # Use dot notation for properties
            >>> print(companies)
            {'CompanyA': 101, 'CompanyB': 102}
            >>> # You can access a specific company ID by name
            >>> company_id = companies.get('CompanyA')
            >>> print(f"CompanyA ID: {company_id}")

        #ai-gen-doc
        """
        return {
            opc['providerDomainName'].lower(): opc['providerId']
            for opc in self.user_mappings.get('operatorCompanies', [])
        }

    def switch_to_company(self, company_name: str) -> None:
        """Switch the current Commcell context to the specified company as an operator.

        This method allows you to operate within the context of a given company, 
        enabling company-specific operations and management.

        Args:
            company_name: The name of the company to switch to.

        Example:
            >>> commcell = Commcell()
            >>> commcell.switch_to_company("AcmeCorp")
            >>> print("Switched to company context: AcmeCorp")
            >>> # Subsequent operations will be performed as an operator for AcmeCorp

        #ai-gen-doc
        """
        if company_id := self.operator_companies.get(company_name.lower()):
            self._headers['operatorCompanyId'] = str(company_id)
            self._user_org = Organization(self, organization_id=company_id)
        else:
            self._user_mappings = None # refreshing once
            if not self.operator_companies.get(company_name.lower()):
                raise SDKException(
                    'Commcell', 108, f'Company {company_name} is not available/allowed '
                                     f'to operate on by this user {self.commcell_username}.'
                                     f'Choose from list: {list(self.operator_companies)}'
                )
            else:
                self.switch_to_company(company_name)

    @property
    def operating_company(self) -> Optional[str]:
        """Get the name of the currently operating company, if available.

        Returns:
            The name of the operating company as a string, or None if no company is currently operating.

        Example:
            >>> commcell = Commcell()
            >>> company_name = commcell.operating_company  # Use dot notation for property access
            >>> if company_name:
            ...     print(f"Operating company: {company_name}")
            ... else:
            ...     print("No operating company is currently set.")

        #ai-gen-doc
        """
        if operating_company_id := self._headers.get('operatorCompanyId'):
            for company_name, company_id in self.operator_companies.items():
                if str(company_id) == str(operating_company_id):
                    return company_name
            raise SDKException('Commcell', 108, f'Operating unknown company. id: {operating_company_id}')
        return None

    def reset_company(self) -> None:
        """Reset the company configuration to the default Commcell settings.

        This method restores the company settings to their original Commcell state.
        It is useful when you need to revert any changes made to the company configuration.

        Example:
            >>> commcell = Commcell()
            >>> commcell.reset_company()
            >>> print("Company configuration has been reset to Commcell defaults.")

        #ai-gen-doc
        """
        if 'operatorCompanyId' in self._headers:
            self._headers.pop('operatorCompanyId')
        self._user_org = None

    @contextmanager
    def as_operator_of(self, company_name: str):
        """Context manager for temporarily switching the Commcell session to operate as the specified company.

        This context manager allows you to perform operations as the operator of a given company.
        Upon exiting the context, the session automatically reverts to its previous state.

        Args:
            company_name: The name of the company to switch to as operator.

        Example:
            >>> with commcell.as_operator_of("AcmeCorp"):
            ...     # Perform actions as AcmeCorp operator
            ...     # All operations within this block are executed as the specified company
            >>> # After exiting the block, the session returns to its original operator level

        #ai-gen-doc
        """
        old_headers = self._headers.copy()
        self.switch_to_company(company_name)
        try:
            yield
        finally:
            self._user_org = None
            self._headers = old_headers

    def switch_to_global(self, target_commcell: Optional[str] = None, comet_header: bool = False) -> None:
        """Switch to the global scope in a multi-commcell configuration.

        This method updates the Commcell context to operate in the global scope, which is useful 
        in environments with multiple commcells. You can specify a target commcell name if a 
        specific header is required, or use the comet_header flag to indicate the use of 
        Comet-Commcells header.

        Args:
            target_commcell: Optional; the name of the target commcell if the '_cn' header is needed.
            comet_header: If True, uses the Comet-Commcells header instead of '_cn'.

        Example:
            >>> commcell = Commcell()
            >>> commcell.switch_to_global()  # Switches to global scope with default headers
            >>> commcell.switch_to_global(target_commcell="CommcellA")  # Uses '_cn' header for CommcellA
            >>> commcell.switch_to_global(comet_header=True)  # Uses Comet-Commcells header

        #ai-gen-doc
        """
        self._headers['Cvcontext'] = 'Comet'
        target_header = '_cn' if not comet_header else 'Comet-Commcells'
        if target_commcell:
            self._headers[target_header] = target_commcell

    def is_global_scope(self) -> bool:
        """Determine if global scope (comet headers) is currently active for API responses.

        Returns:
            True if comet headers are set and global scope is active; otherwise, False.

        Example:
            >>> commcell = Commcell()
            >>> if commcell.is_global_scope():
            ...     print("Global scope is active for API responses.")
            ... else:
            ...     print("Global scope is not active.")

        #ai-gen-doc
        """
        return self._headers.get('Cvcontext') == 'Comet'

    def reset_to_local(self) -> None:
        """Reset the Commcell object to local scope if currently in global scope.

        This method switches the Commcell context back to local, ensuring that 
        subsequent operations are performed within the local Commcell environment.

        Example:
            >>> commcell = Commcell()
            >>> commcell.reset_to_local()
            >>> print("Commcell is now operating in local scope")

        #ai-gen-doc
        """
        for header in ['Cvcontext', '_cn', 'Comet-Commcells']:
            if header in self._headers:
                del self._headers[header]

    @contextmanager
    def global_scope(self, target_commcell: Optional[str] = None, comet_header: bool = False) -> Any:
        """Context manager for temporarily switching the Commcell to Global scope.

        This context manager allows you to perform operations within the Global scope of the Commcell.
        Upon exiting the context, the scope is automatically reverted to its previous state.

        Args:
            target_commcell: Optional; the name of the target Commcell if the '_cn' header is required.
            comet_header: If True, uses the 'Comet-Commcells' header instead of '_cn'.

        Returns:
            A context manager object that manages the Global scope transition.

        Example:
            >>> with commcell.global_scope(target_commcell="CentralCommcell", comet_header=True):
            ...     # Perform operations in Global scope
            ...     print("Now operating in Global scope")
            >>> # After exiting the context, scope is reverted

        #ai-gen-doc
        """
        old_headers = self._headers.copy()
        self.switch_to_global(target_commcell, comet_header)
        try:
            yield
        finally:
            self._headers = old_headers

    @contextmanager
    def custom_headers(self, **headers: str) -> Any:
        """Context manager for temporarily setting custom HTTP headers.

        This context manager allows you to specify additional HTTP headers for requests made within its scope.
        The headers are passed as keyword arguments and are applied only for the duration of the context.

        Args:
            **headers: Arbitrary keyword arguments representing header names and their values.

        Returns:
            A context manager that applies the specified headers within its scope.

        Example:
            >>> with commcell.custom_headers(Authorization="Bearer token123", X-Custom="value"):
            ...     # All requests within this block will include the specified headers
            ...     response = commcell.get_data()
            >>> # After exiting the block, headers revert to their previous state

        #ai-gen-doc
        """
        old_headers = self._headers.copy()
        self._headers.update(headers)
        try:
            yield
        finally:
            self._headers = old_headers

    def passkey(self, current_password: str, action: str, new_password: Optional[str] = None) -> None:
        """Update the Passkey properties of the Commcell.

        This method allows you to enable, disable, change, authorize, or unauthorize the passkey for the Commcell.
        The current passkey must be provided for authentication. If the action is 'change passkey', a new password
        must also be provided.

        Args:
            current_password: The current passkey of the user required to perform the action.
            action: The action to perform. Valid values are 'enable', 'disable', 'change passkey', 'authorize', or 'unauthorize'.
            new_password: The new passkey to set when changing the existing passkey. Required if action is 'change passkey'.

        Raises:
            SDKException: If an invalid action is provided, if the request fails to update passkey properties,
                or if the new password is missing when changing the passkey.

        Example:
            >>> commcell = Commcell()
            >>> # Enable passkey
            >>> commcell.passkey('currentPass123', 'enable')
            >>> # Change passkey
            >>> commcell.passkey('currentPass123', 'change passkey', new_password='newPass456')
            >>> # Authorize passkey
            >>> commcell.passkey('currentPass123', 'authorize')
            >>> # Disable passkey
            >>> commcell.passkey('currentPass123', 'disable')
            >>> # Unauthorize passkey
            >>> commcell.passkey('currentPass123', 'unauthorize')

        #ai-gen-doc
        """

        current_password = b64encode(current_password.encode()).decode()
        commcell_organization_id = 0
        req_url = self._services['COMPANY_PASSKEY'] % commcell_organization_id

        if action.lower() == 'enable':
            req_json = {
            "newPasskey": current_password,
            "confirmPasskey": current_password,
            "passkeyOpType": "CREATE"
            }

        elif action.lower() == 'disable':
            req_json = {
                "currentPasskey": current_password,
                "confirmPasskey": current_password,
                "passkeyOpType": "DISABLE"
            }

        elif action.lower() == 'change passkey':
            if new_password:
                new_password = b64encode(new_password.encode()).decode()
                req_json = {
                    "currentPasskey": current_password,
                    "newPasskey": new_password,
                    "confirmPasskey": new_password,
                    "passkeyOpType": "EDIT"
                }
            else:
                raise SDKException('Commcell', 102, 'New password is missing in input')

        elif action.lower() in ['authorize', 'unauthorize']:
            req_json = {
                "passkey": current_password,
                "passkeySettings": {
                    "enableAuthorizeForRestore": action.lower() == 'authorize',
                    "passkeyExpirationInterval": {
                        "toTime": 1800
                    }
                }
            }
            req_url = self._services['COMPANY_AUTH_RESTORE'] % commcell_organization_id

        else:
            raise SDKException('Commcell', 102, 'Action is undefined, Invalid action passed as a parameter')

        flag, response = self._cvpysdk_object.make_request('POST', req_url, req_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Commcell', '110', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('Commcell', '110')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def allow_users_to_enable_passkey(self, flag: bool) -> None:
        """Enable or disable passkey authorization for company administrators and client owners.

        This method allows you to control whether company administrators and client owners
        can enable passkey authorization for enhanced security.

        Args:
            flag: Set to True to enable passkey authorization, or False to disable it.

        Raises:
            SDKException: If the response is empty, not successful, or if enabling/disabling passkey fails.

        Example:
            >>> commcell = Commcell()
            >>> commcell.allow_users_to_enable_passkey(True)  # Enable passkey authorization
            >>> commcell.allow_users_to_enable_passkey(False) # Disable passkey authorization

        #ai-gen-doc
        """
        request_json = {
            "commCellInfo": {
                "generalInfo": {
                    "allowUsersToEnablePasskey": flag
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request('PUT', self._services['SET_COMMCELL_PROPERTIES'], request_json)

        if flag:
            if response.json() and "response" in response.json():
                errorCode = response.json()['response'][0].get('errorCode')
                if errorCode != 0:
                    raise SDKException('Response', '101', 'Failed to enable passkey')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_sla_configuration(self) -> Dict[str, Any]:
        """Retrieve the Service Level Agreement (SLA) configuration for the Commcell.

        This method makes a REST API call to obtain the current SLA settings at the Commcell level.
        The returned dictionary contains details such as SLA days, exclusion reasons, system default usage,
        delay intervals, and inherited SLA information.

        Returns:
            Dictionary containing SLA configuration details. Example structure:
                {
                    'slaDays': 7,
                    'excludedReason': '',
                    'useSystemDefaultSLA': False,
                    'excludeFromSLA': False,
                    'delayInterval': 0,
                    'inheritedSLA': {
                        'slaDays': 0,
                        'entityType': 0,
                        'excludeFromSLA': False
                    }
                }

        Raises:
            SDKException: If the API response is empty or unsuccessful.

        Example:
            >>> commcell = Commcell()
            >>> sla_config = commcell.get_sla_configuration()
            >>> print(f"SLA Days: {sla_config['slaDays']}")
            >>> if sla_config['excludeFromSLA']:
            >>>     print("This Commcell is excluded from SLA calculations.")
            >>> inherited = sla_config.get('inheritedSLA', {})
            >>> print(f"Inherited SLA Days: {inherited.get('slaDays', 0)}")

        #ai-gen-doc
        """
        request_json = {"entities": [{"entity": {"commCellId": self.commcell_id, "_type_": 1}}]}
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GET_SLA'], payload=request_json
        )

        if flag:
            if response.ok and response.json():
                return response.json().get('entities', [{}])[0]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_workload_region(self) -> Optional[str]:
        """Retrieve the workload region configured at the Commcell level.

        Returns:
            The name of the workload region set for the Commcell, such as 'US - east'.
            Returns None if no region is set or the region name cannot be found.

        Example:
            >>> commcell = Commcell()
            >>> region = commcell.get_workload_region()
            >>> if region:
            >>>     print(f"Workload region: {region}")
            >>> else:
            >>>     print("No workload region is set for this Commcell.")

        #ai-gen-doc
        """
        region_id = self.regions.get_region('COMMCELL', self.commcell_id, 'WORKLOAD')
        for reg_name, reg_id in self.regions.all_regions.items():
            if reg_id == region_id:
                return reg_name

    def set_workload_region(self, region_name: Optional[str]) -> None:
        """Set the workload region for the Commcell.

        This method assigns a workload region at the Commcell level. 
        Passing None will remove any previously set region.

        Args:
            region_name: The name of the region to set. Use None to unset the region.

        Example:
            >>> commcell = Commcell()
            >>> commcell.set_workload_region("US-East")
            >>> # To remove the region setting:
            >>> commcell.set_workload_region(None)

        #ai-gen-doc
        """
        if region_name:
            if not self.regions.has_region(region_name):
                raise SDKException('Region', '102', 'Given region not found!')
            region_id = self.regions.all_regions[region_name]
        else:
            region_id = 0
        self.regions.set_region('COMMCELL', self.commcell_id, 'WORKLOAD', region_id)

    def get_user_suggestions(self, term: str, additional_params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Retrieve user suggestions for entities matching the specified term.

        This method makes an API call to fetch suggestions for entities whose names match the provided term.
        Additional parameters can be supplied to refine the search.

        Args:
            term: The entity name or search term to match suggestions against.
            additional_params: Optional dictionary of additional parameters to include in the API request.

        Returns:
            A list of dictionaries, each containing details of an entity that matches the given term.
            Example output:
                [
                    {
                        "displayName": "John Doe",
                        "groupId": 123,
                        "umEntityType": 1,
                        "umGuid": "abc-123",
                        "groupGuid": "def-456",
                        "company": {...},
                    },
                    {...},
                    {...},
                ]

        Raises:
            SDKException: If the API response is empty or not successful.

        Example:
            >>> commcell = Commcell()
            >>> suggestions = commcell.get_user_suggestions("admin")
            >>> for entity in suggestions:
            ...     print(entity["displayName"])
            >>> # Use additional parameters to filter results
            >>> params = {"companyId": 42}
            >>> filtered_suggestions = commcell.get_user_suggestions("user", additional_params=params)
            >>> print(filtered_suggestions)

        #ai-gen-doc
        """
        from urllib.parse import urlencode

        if additional_params is None:
            additional_params = {}

        url_params = {
            'namePattern': term,
            'getDomainUsers': True,
            'getCommcellUsers': True,
            'getCommCellGroups': True,
            'getDomainGroups': True,
            'searchOnDisplayName': True,
            'searchOnAliasName': True,
            'searchOnSmtp': 1,
            'ignoreSmtpRule': 1,
        }
        url_params.update(additional_params)
        url_params.update({k: str(v).lower() for k, v in url_params.items() if v in [True, False]})

        api_endpoint = self._services['GET_USER_SUGGESTIONS'] + '?' + urlencode(url_params)
        flag, response = self._cvpysdk_object.make_request('GET', api_endpoint)

        if flag:
            if response.json():
                return response.json().get('users')
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_limit_user_logon_attempts(
        self,
        failed_login_attempt_limit: int = 5,
        failed_login_attempts_within: int = 3600,
        account_lock_duration: int = 86400,
        lock_duration_increment_by: int = 3600,
        otp: str = None
    ) -> None:
        """Enable the feature to limit user logon attempts on the Commcell.

        This method configures the Commcell to restrict the number of failed logon attempts 
        allowed for users, and sets the duration for which accounts are locked after exceeding 
        the allowed attempts. The lock duration can be incremented after each consecutive lock.

        Args:
            failed_login_attempt_limit: The maximum number of failed logon attempts allowed before locking the account. Default is 5.
            failed_login_attempts_within: The time window (in seconds) within which failed attempts are counted. Default is 3600 seconds (1 hour).
            account_lock_duration: The duration (in seconds) for which a locked account remains inaccessible. Default is 86400 seconds (24 hours).
            lock_duration_increment_by: The increment (in seconds) added to the lock duration after each consecutive account lock. Default is 3600 seconds (1 hour).
            otp (str): otp for two-factor authentication operation.

        Raises:
            SDKException: If the response from the Commcell is empty, unsuccessful, or if enabling the feature fails.

        Example:
            >>> commcell = Commcell()
            >>> commcell.enable_limit_user_logon_attempts(
            ...     failed_login_attempt_limit=3,
            ...     failed_login_attempts_within=1800,
            ...     account_lock_duration=7200,
            ...     lock_duration_increment_by=1200,
            ...     otp="otp"
            ... )
            >>> print("User logon attempt limits enabled successfully.")

        #ai-gen-doc
        """
        req_json = {
            'failedLoginAttemptLimit': failed_login_attempt_limit,
            'failedLoginAttemptsWithin': failed_login_attempts_within,
            'accountLockDuration': account_lock_duration,
            'accountLockDurationIncrements': lock_duration_increment_by
        }
        
        headers = None
        if otp:
            headers = self._headers.copy()
            headers["otp"] = otp

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ACCOUNT_lOCK_SETTINGS'], req_json, headers=headers
        )
        if flag:
            if response and response.json():
                error_code = response.json().get('errorCode', -1)
                if error_code != 0:
                    error_string = response.json().get('errorMessage', '')
                    raise SDKException(
                        'Security',
                        '102',
                        'Failed to set account lock settings: "{0}"'.format(
                            error_string
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_limit_user_logon_attempts(self, otp: str = None) -> None:
        """Disable the feature that limits user logon attempts on the Commcell.

        This method turns off the restriction that limits the number of failed user logon attempts,
        allowing users to attempt logon without being blocked after multiple failures.

        Args:
            otp (str): otp for two-factor authentication operation.

        Raises:
            SDKException: If the response from the Commcell is empty, unsuccessful, or if disabling
                the limit user logon feature fails.

        Example:
            >>> commcell = Commcell()
            >>> commcell.disable_limit_user_logon_attempts(otp="otp")
            >>> print("User logon attempt limit has been disabled.")

        #ai-gen-doc
        """
        self.enable_limit_user_logon_attempts(failed_login_attempt_limit=-1,
                                              failed_login_attempts_within=-1,
                                              account_lock_duration=-1,
                                              lock_duration_increment_by=-1,
                                              otp=otp)

    def get_navigation_settings(self, org_id: int = 0) -> Dict[str, Dict[str, List[str]]]:
        """Retrieve the navigation preference list for all user roles in Command Center.

        This method makes a REST API call to obtain the navigation settings for each user role,
        including which navigation items are included or denied. The settings are returned as a
        dictionary mapping user roles to their respective navigation preferences.

        Args:
            org_id: The ID of the company (organization) to get the preference list for. Defaults to 0.

        Returns:
            A dictionary where each key is a user role (e.g., "msp_admin", "tenant_admin") and the value
            is another dictionary containing:
                - "include_navs": List of navigation items included for the role.
                - "denied_navs": List of navigation items denied for the role.

            Example return value:
                {
                    "msp_admin": {
                        "include_navs": ["gsuite", "replication", ...],
                        "denied_navs": []
                    },
                    "tenant_admin": {...},
                    "tenant_user": {...},
                    "msp_user": {...},
                    "restricted_user": {...}
                }

        Example:
            >>> commcell = Commcell()
            >>> nav_settings = commcell.get_navigation_settings(org_id=123)
            >>> print(nav_settings["msp_admin"]["include_navs"])
            >>> # Output: ['gsuite', 'replication', ...]

        #ai-gen-doc
        """
        user_roles = {0: 'msp_admin', 1: 'tenant_admin', 2: 'tenant_user', 3: 'msp_user', 4: 'restricted_user'}
        url = self._services['NAVIGATION_SETTINGS']
        settings_type = 'globalSettings'
        if org_id:
            url += f'?organizationId={org_id}'
            settings_type = 'companySettings'

        flag, response = self._cvpysdk_object.make_request('GET', url)
        if flag:
            if response.json():
                error_response = response.json().get('error', {})
                if error_response.get('errorCode', -1) != 0:
                    error_string = error_response.get('errorMessage', '')
                    raise SDKException('Commcell', '108', error_string)

                nav_settings = {}
                for user_nav in response.json().get('navSettings', {}).get(settings_type, []):
                    nav_settings[user_roles[user_nav.get('userRole')]] = {
                        "include_navs": user_nav.get('includeNavItems', '').split(','),
                        "denied_navs": user_nav.get('deniedNavItems', '').split(',')
                    }
                return nav_settings
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.content)
            raise SDKException('Response', '101', response_string)

    def set_navigation_settings(self, nav_settings: Dict[str, Dict[str, List[str]]], org_id: int = 0) -> None:
        """Set the navigation preference list for Command Center roles.

        This method makes a REST API call to update the navigation settings for different user roles
        in the Command Center. The settings specify which navigation items are included or denied
        for each role.

        Args:
            nav_settings: A dictionary mapping role names to their navigation preferences.
                Each role should have 'include_navs' and 'denied_navs' lists.
                Example:
                    {
                      "msp_admin": {
                        "include_navs": ["gsuite", "replication"],
                        "denied_navs": []
                      },
                      "tenant_admin": {
                        "include_navs": ["backup", "restore"],
                        "denied_navs": ["replication"]
                      },
                      "tenant_user": {...},
                      "msp_user": {...},
                      "restricted_user": {...}
                    }
            org_id: The ID of the company (organization) to set the preference list for. Defaults to 0.

        Example:
            >>> nav_settings = {
            ...     "msp_admin": {
            ...         "include_navs": ["gsuite", "replication"],
            ...         "denied_navs": []
            ...     },
            ...     "tenant_admin": {
            ...         "include_navs": ["backup", "restore"],
            ...         "denied_navs": ["replication"]
            ...     }
            ... }
            >>> commcell = Commcell()
            >>> commcell.set_navigation_settings(nav_settings, org_id=123)
            >>> print("Navigation settings updated successfully.")

        #ai-gen-doc
        """
        user_roles = {'msp_admin': 0, 'tenant_admin': 1, 'tenant_user': 2, 'msp_user': 3, 'restricted_user': 4}
        url = self._services['NAVIGATION_SETTINGS']
        settings_type = 'globalSettings'
        if org_id:
            url += f'?organizationId={org_id}'
            settings_type = 'companySettings'

        settings = []
        for role, nav_items in nav_settings.items():
            settings.append({"userRole": user_roles[role]})
            if "include_navs" in nav_items:
                settings[-1]["includeNavItems"] = ",".join(nav_items["include_navs"])
            if "denied_navs" in nav_items:
                settings[-1]["deniedNavItems"] = ",".join(nav_items["denied_navs"])

        request_json = {
            'navSettings': {
                settings_type: settings
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST', url, payload=request_json)
        if flag:
            if response.json():
                if response.json().get('errorCode', -1) != 0:
                    error_string = response.json().get('errorMessage', '')
                    raise SDKException('Commcell', '108', error_string)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.content)
            raise SDKException('Response', '101', response_string)

    @property
    def cost_assessment(self) -> 'CostAssessment':
        """Get the CostAssessment instance associated with this Commcell.

        Returns:
            CostAssessment: An object for managing and analyzing cost assessments within the Commcell.

        Example:
            >>> commcell = Commcell()
            >>> cost_assess = commcell.cost_assessment  # Access the property using dot notation
            >>> print(f"Cost assessment object: {cost_assess}")
            >>> # The returned CostAssessment object can be used for further cost analysis operations

        #ai-gen-doc
        """
        try:
            if self._cost_assessment is None:
                self._cost_assessment = CostAssessment(self)

            return self._cost_assessment
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def azure_discovery(self) -> 'AzureDiscovery':
        """Get the AzureDiscovery instance associated with this Commcell.

    Returns:
        AzureDiscovery: An object for discovering and analyzing discovered Azure resources within the Commcell.

    Example:
        >>> commcell = Commcell()
        >>> azure_discovery = commcell.azure_discovery  # Access the property using dot notation
        >>> print(f"Azure Discovery object: {azure_discovery}")

    """
        try:
            if self._azure_discovery is None:
                self._azure_discovery = AzureDiscovery(self)

            return self._azure_discovery
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def aws_discovery(self) -> 'AWSDiscovery':
        """Get the AWSDiscovery instance associated with this Commcell.

        Returns:
            AWSDiscovery: An object for discovering and analyzing discovered AWS resources within the Commcell.

        Example:
            >>> commcell = Commcell()
            >>> aws_discovery = commcell.aws_discovery  # Access the property using dot notation
            >>> print(f"AWS Discovery object: {aws_discovery}")

        """
        try:
            if self._aws_discovery is None:
                self._aws_discovery = AWSDiscovery(self)

            return self._aws_discovery
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def get_environment_tile_details(self, comet_flag: bool = False) -> dict[str, dict[str, int]]:
        """Retrieve environment tile details for the Commcell, including counts of file servers, VMs, laptops, and users.

        Args:
            comet_flag: If True, fetches details for each service Commcell individually. If False, returns aggregate counts for the current Commcell.

        Returns:
            A dictionary containing environment tile details:
                - If comet_flag is True: Returns a dictionary where each key is a Commcell name, and the value is another dictionary with counts for 'fileServerCount', 'laptopCount', 'vmCount', and 'usersCount'. Includes a 'totalCount' key for overall totals.
                - If comet_flag is False: Returns a dictionary with aggregate counts for 'fileServerCount', 'laptopCount', 'vmCount', and 'usersCount' for the current Commcell.

        Example:
            >>> # Get aggregate environment details for the current Commcell
            >>> details = commcell.get_environment_tile_details()
            >>> print(details)
            >>> # Output: {'fileServerCount': 56, 'laptopCount': 2, 'vmCount': 453, 'usersCount': 2415}

            >>> # Get environment details for each service Commcell
            >>> details = commcell.get_environment_tile_details(comet_flag=True)
            >>> print(details)
            >>> # Output: {'commcell1': {...}, 'commcell2': {...}, ..., 'totalCount': {...}}

        #ai-gen-doc
        """
        if comet_flag:
            self.switch_to_global()

        # Fetch environment tile counts - fileserver,vm,laptop
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['DASHBOARD_ENVIRONMENT_TILE']
        )
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        resp_json = response.json()
        if not resp_json:
            raise SDKException('Response', '102')

        # Fetch environment tile counts - users
        flag_1, response_1 = self._cvpysdk_object.make_request(
            'GET', self._services['DASHBOARD_ENVIRONMENT_TILE_USERS']
        )
        if not flag_1:
            raise SDKException('Response', '101', self._update_response_(response_1.text))

        resp_json_1 = response_1.json()
        if not resp_json_1:
            raise SDKException('Response', '102')

        environment_tile_dict = {}
        main_keys = ['fileServerCount', 'laptopCount', 'vmCount']

        if comet_flag:
            commcell_data = {}

            # Populate fileServerCount, laptopCount, vmCount
            for tile in resp_json.get('cometClientCount', []):
                commcell_name = tile.get('commcell',{}).get('commCellName','')
                if not commcell_name:
                    continue
                commcell_data.setdefault(commcell_name, {})
                for key in main_keys:
                    commcell_data[commcell_name][key] = tile.get(key, 0)

            # Populate usersCount
            for item in resp_json_1.get('commcellWiseAggregation', []):
                commcell_name = item.get('commcellName', '')
                if not commcell_name:
                    continue
                func_value = item.get('aggregation', [{}])[0].get('funcValue', 0)
                commcell_data.setdefault(commcell_name, {})
                commcell_data[commcell_name]['usersCount'] = int(func_value)

            # Add totalCount as a separate key
            commcell_data['totalCount'] = {
                key: resp_json.get('totalCount', {}).get(key, 0) if key != 'usersCount' else
                     int(resp_json_1.get('aggregation', [{}])[0].get('funcValue', 0))
                for key in ['fileServerCount', 'laptopCount', 'vmCount', 'usersCount']
            }

            environment_tile_dict = commcell_data
        else:
            for key in main_keys:
                environment_tile_dict[key] = resp_json.get(key, 0)

            environment_tile_dict['usersCount'] = int(
                resp_json_1.get('aggregation', [{}])[0].get('funcValue', 0)
            )
        if comet_flag:
            self.reset_to_local()
        return environment_tile_dict
    
    def get_logs_by_trace_id(self, trace_id: str) -> List[Dict[str, Any]]:
        """Retrieve logs associated with a specific trace ID.

        Args:
            trace_id: The trace ID for which to retrieve logs.

        Returns:
            A list of dictionaries, each representing a log entry associated with the given trace ID.

        Example:
            >>> commcell = Commcell()
            >>> logs = commcell.get_logs_by_trace_id("trace-id-12345")
            >>> for log in logs:
            ...     print(log)

        #ai-gen-doc
        """
        url = self._services['VIEW_LOGS_BY_TRACE_ID'] % trace_id
        flag, response = self._cvpysdk_object.make_request('GET', url)

        if flag:
            if response.json():
                return response.json().get('logs', [])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
