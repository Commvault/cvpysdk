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
    along with the user name of the connected user

    __enter__()                 --  returns the current instance, using the "with" context manager

    __exit__()                  --  logs out the user associated with the current instance

    _update_response_()         --  returns only the relevant response for the response received
    from the server

    _remove_attribs_()          --  removes all the attributs associated with the commcell
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

    download_software()         --  triggers the Download Software job with the given options

    sync_remote_cache()         --  syncs remote cache

    get_remote_cache()     		--  returns the instance of the RemoteCache class

    push_servicepack_and_hotfixes() --  triggers installation of service pack and hotfixes

    install_software()              --  triggers the install Software job with the given options

    enable_auth_code()              --  executes the request on the server to enable Auth Code
    for installation on the commcell

    enable_shared_laptop()          --   Executes the request on the server to enable Shared Laptop on commcell

    disable_shared_laptop()         --  Executes the request on the server to disable Shared Laptop on commcell

    execute_qcommand()              --  executes the ExecuteQCommand API on the commcell

    add_associations_to_saml_app()  --  Adds the given user under associations of the SAML app

    _get_registered_service_commcells() -- gets the list of registered service commcells

    register_commcell()             -- registers a commcell

    sync_service_commcell()         --  Sync a service commcell

    unregister_commcell()           -- unregisters a commcell

    is_commcell_registered()       -- checks if the commcell is registered

    _get_redirect_rules_service_commcell()    -- gets the redirect rules of service commcell

    get_eligible_service_commcells()             -- gets the eligible service commcells to redirect

    get_default_plan()                  -- Get the default plans associed with the commcell

    get_security_associations()         -- Get the security associations associated with the commcell

    get_password_encryption_config()    -- Get the Password encryption configuration for the commcell

    get_email_settings()                -- Get the SMTP settings for the commcell

    get_commcell_properties()           -- Get the general, privacy and other properties of commcell

    get_commcell_organization_properties()     -- Get the organization properties of commcell

    add_service_commcell_associations()    -- adds an association for an entity on a service commcell

    enable_tfa()                           --   Enables two factor authentication on this commcell

    disable_tfa()                          --  Disables two factor authentication on this commcell

    _get_commserv_metadata()               -- Returns back the commserv metadata on this commcell

    enable_privacy()                    --  Enables users to enable data privacy on commcell

    disable_privacy()                   --  Enables users to disable data privacy on commcell

    switch_to_company()         --  Login to company as an operator, just like using switcher on Command Center

    reset_company()             --  Switch back to Commcell
    
    allow_users_to_enable_passkey()     --      Enable or Disable passkey authorization for company administrators and client owners

Commcell instance Attributes
============================

    **commserv_guid**           --  returns the `CommServ` GUID, class instance is initalized for

    **commserv_hostname**       --  returns the hostname of the `CommServ`, class instance is
    initalized for

    **commserv_name**           --  returns the `CommServ` name, class instance is initalized for

    **commserv_timezone**       --  returns the time zone of the `CommServ`,
    class instance is initalized for

    **commserv_timezone_name**  --  returns the name of the `CommServ` time zone,
    class instance is initalized for

    **commserv_version**        --  returns the ContentStore version installed on the `CommServ`,
    class instance is initalized for

    **version**                 --  returns the complete version info of the commserv

    **commcell_id**             --  returns the `CommCell` ID

    **commser_metadata**        -- returns the commserv metadata of the commserv

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

    **activate**                --  returns the instance of the `Activate` class,
    to interact with activate apps on the Commcell

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

    **backup_network_pairs**    --  returns the instance of 'BackupNetworkPairs' class to
    perform backup network pairs operations on the commcell class

    **recovery_targets**        -- Returns the instance of RecoverTargets class

    **reports**                 --  Return the instance of Report class

    **job_management**          --  Returns an instance of the JobManagement class.

    **hac_clusters**            --  Returns an instance of the HAC Clusters class

    **index_pools**             --  Returns an instance of the IndexPools class

    **deduplications_engines    --  Returnes the instance of the DeduplicationEngines class
    to interact wtih deduplication enines available on the commcell

    **two_factor_authentication**   --  Returns an instance of the TwoFactorAuthentication class.

    **is_tfa_enabled**              --  Returns the status of tfa on this commcell.

    **tfa_enabled_user_groups**     -- Returns user group names on which tfa is enabled.
    only for user group inclusion tfa.

    **is_linux_commserv**           -- boolean specifying if CommServer is installed on linux cs.

    **default_timezone**            -- Default timezone used by all the operations performed via cvpysdk.

    **metallic**                 -- Returns the instance of CVMetallic class

    **key_management_servers**      -- Returns the instance of `KeyManagementServers` class
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import getpass
import socket

from base64 import b64encode
from past.builtins import basestring

from requests.exceptions import SSLError
from requests.exceptions import Timeout

# ConnectionError is a built-in exception, do not override it
from requests.exceptions import ConnectionError as RequestsConnectionError

from .activate import Activate
from .services import get_services
from .cvpysdk import CVPySDK
from .client import Clients
from .alert import Alerts
from .storage import MediaAgents
from .storage import DiskLibraries
from .storage import TapeLibraries
from .security.usergroup import UserGroups, UserGroup
from .domains import Domains, Domain
from .workflow import WorkFlows
from .exception import SDKException
from .clientgroup import ClientGroups
from .globalfilter import GlobalFilters
from .datacube.datacube import Datacube
from .content_analyzer import ContentAnalyzers
from .plan import Plans
from .job import JobController
from .security.user import Users, User
from .security.role import Roles
from .security.two_factor_authentication import TwoFactorAuthentication
from .credential_manager import Credentials
from .download_center import DownloadCenter
from .organization import Organizations, Organization
from .storage_pool import StoragePools
from .monitoring import MonitoringPolicies
from .policy import Policies
from .schedules import SchedulePattern
from .schedules import Schedules
from .activitycontrol import ActivityControl
from .eventviewer import Events
from .array_management import ArrayManagement
from .disasterrecovery import DisasterRecovery
from .operation_window import OperationWindow
from .identity_management import IdentityManagementApps
from .system import System
from .commcell_migration import CommCellMigration
from .deployment.download import Download
from .deployment.cache_config import CommServeCache
from .deployment.cache_config import RemoteCache
from .deployment.install import Install
from .name_change import NameChange
from .backup_network_pairs import BackupNetworkPairs
from .reports import report
from .recovery_targets import RecoveryTargets
from .drorchestration.replication_groups import ReplicationGroups
from .drorchestration.blr_pairs import BLRPairs
from .job import JobManagement
from .index_server import IndexServers
from .hac_clusters import HACClusters
from .index_pools import IndexPools
from .deduplication_engines import DeduplicationEngines
from .metallic import Metallic
from .key_management_server import KeyManagementServers

USER_LOGGED_OUT_MESSAGE = 'User Logged Out. Please initialize the Commcell object again.'
USER_DOES_NOT_HAVE_PERMISSION = "User does not have permission on commcell properties"
"""str:     Message to be returned to the user, when trying the get the value of an attribute
of the Commcell class, after the user was logged out.

"""


class Commcell(object):
    """Class for establishing a session to the Commcell via Commvault REST API."""

    def __init__(
            self,
            webconsole_hostname,
            commcell_username=None,
            commcell_password=None,
            authtoken=None,
            force_https=False,
            certificate_path=None,
            is_service_commcell=None):
        """Initialize the Commcell object with the values required for doing the API operations.

            Commcell Username and Password can be None, if QSDK / SAML token is being given
            as the input by the user.

            If both the Commcell Password and the Authtoken are None,
            then the user will be prompted to enter the password via command line.


            Args:
                webconsole_hostname     (str)   --  webconsole host Name / IP address

                    e.g.:

                        -   webclient.company.com

                        -   xxx.xxx.xxx.xxx


                commcell_username       (str)   --  username for log in to the commcell console

                    default: None


                commcell_password       (str)   --  plain-text password for log in to the console

                    default: None


                authtoken               (str)   --  QSDK / SAML token for log in to the console

                    default: None

            **Note** : If SAML token is to be used to login to service commcell please set is_service_commcell=True


                force_https             (bool)  --  boolean flag to specify whether to force the
                connection to the commcell only via HTTPS

                if the flag is set to **False**, SDK first tries to connect to the commcell via
                HTTPS, but if that fails, it tries to connect via HTTP

                if flag is set to **True**, it'll only try via HTTPS, and exit if it fails

                    default: False


                certificate_path        (str)   --  path of the CA_BUNDLE or directory with
                certificates of trusted CAs (including trusted self-signed certificates)

                    default: None

            **Note** If certificate path is provided, force_https is set to True

                is_service_commcell     (bool) --  True if login into service (child commcell)
                                                   False if it is a normal login

                    default: None

            **Note** In case of Multicommcell Login, if we wanted to login into child commcell (Service commcell)
                        set is_service_commcell to True

            Returns:
                object  -   instance of this class

            Raises:
                SDKException:
                    if the web service is down or not reachable

                    if no token is received upon log in

        """
        web_service = [
            r'https://{0}/webconsole/api/'.format(webconsole_hostname)
        ]

        if certificate_path:
            force_https = True

        if force_https is False:
            web_service.append(r'http://{0}/webconsole/api/'.format(webconsole_hostname))

        self._user = commcell_username

        self._password = None

        self._headers = {
            'Host': webconsole_hostname,
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authtoken': None
        }

        self._device_id = socket.getfqdn()
        self._is_service_commcell = is_service_commcell

        self._cvpysdk_object = CVPySDK(self, certificate_path)

        # Checks if the service is running or not
        for service in web_service:
            self._web_service = service
            try:
                if self._cvpysdk_object._is_valid_service():
                    break
            except (RequestsConnectionError, SSLError, Timeout):
                if force_https:
                    raise
        else:
            raise SDKException('Commcell', '101')

        # Initialize all the services with this commcell service
        self._services = get_services(self._web_service)

        validity_err = None
        self._is_saml_login = False

        if isinstance(commcell_password, dict):
            authtoken = commcell_password['Authtoken']

        if authtoken and not is_service_commcell:
            if authtoken.startswith('QSDK ') or authtoken.startswith('SAML '):
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
        self._is_linux_commserv = None
        self._commserv_metadata = None

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
        self._content_analyzers = None
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
        self._registered_commcells = None
        self._redirect_rules_service = None
        self._backup_network_pairs = None
        self._reports = None
        self._replication_groups = None
        self._recovery_targets = None
        self._blr_pairs = None
        self._job_management = None
        self._index_servers = None
        self._hac_clusters = None
        self._index_pools = None
        self._deduplication_engines = None
        self._redirect_cc_idp = None
        self._tfa = None
        self._metallic = None
        self._kms = None
        self._privacy = None
        self._commcell_properties = None
        self.refresh()

        del self._password

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string about the details of the Commcell class instance

        """
        representation_string = 'Commcell class instance of Commcell: "{0}", for User: "{1}"'
        return representation_string.format(self.commserv_name, self._user)

    def __enter__(self):
        """Returns the current instance.

            Returns:
                object  -   the initialized instance referred by self

        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Logs out the user associated with the current instance."""
        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def _update_response_(self, input_string):
        """Returns only the relevant response from the response received from the server.

            Args:
                input_string    (str)   --  input string to retrieve the relevant response from

            Returns:
                str     -   final response to be used

        """
        if '<title>' in input_string and '</title>' in input_string:
            response_string = input_string.split("<title>")[1]
            response_string = response_string.split("</title>")[0]
            return response_string

        return input_string

    def _remove_attribs_(self):
        """Removes all the attributes associated with the instance of this class."""
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
        del self._plans
        del self._job_controller
        del self._users
        del self._download_center
        del self._organizations
        del self._storage_pools
        del self._recovery_targets
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
        del self._backup_network_pairs
        del self._job_management
        del self._index_servers
        del self._hac_clusters
        del self._index_pools
        del self._deduplication_engines
        del self._is_service_commcell
        del self._master_saml_token
        del self._tfa
        del self._metallic
        del self._kms
        del self

    def _get_commserv_details(self):
        """Gets the details of the CommServ, the Commcell class instance is initialized for,
            and updates the class instance attributes.

            Returns:
                None

            Raises:
                SDKException:
                    if failed to get commserv details

                    if response received is empty

                    if response is not success

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

                except KeyError as error:
                    raise SDKException('Commcell', '103', 'Key does not exist: {0}'.format(error))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _qoperation_execute(self, request_xml):
        """Makes a qoperation execute rest api call

            Args:
                request_xml     (str)   --  request xml that is to be passed

            Returns:
                dict    -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.ok:
                try:
                    return response.json()
                except ValueError:
                    return {'output': response}
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def qoperation_execute(self, request_xml):
        """Wrapper for def _qoperation_execute(self, request_xml)

            Args:
                request_xml     (str)   --  request xml that is to be passed

            Returns:
                dict    -   JSON response received from the server.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        return self._qoperation_execute(request_xml)

    @staticmethod
    def _convert_days_to_epoch(days):
        """
        convert the days to epoch time stamp
        Args:
            days: Number of days to convert

        Returns:
            from_time : days - now  . start time in unix format
            to_time   : now . end time in unix format
        """
        import datetime
        import time
        now = datetime.datetime.now()
        then = now - datetime.timedelta(days=days)
        start_dt = int(time.mktime(then.timetuple()))
        end_dt = int(time.mktime(now.timetuple()))
        return start_dt, end_dt

    @property
    def commcell_id(self):
        """Returns the ID of the CommCell."""
        return self._id

    def _qoperation_execscript(self, arguments):
        """Makes a qoperation execute qscript with specified arguements

            Args:
                arguments     (str)   --  arguements that is to be passed

            Returns:
                dict    -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def get_gxglobalparam_value(self):
        """Makes a rest api call to get values from GXGlobalParam

            Returns:
                dict    -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['GET_GLOBAL_PARAM']
        )

        if flag:
            if response.ok:
                try:
                    return response.json()
                except ValueError:
                    return {'output': response}
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_gxglobalparam_value(self, request_json):
        """ Updates GXGlobalParam table (Commcell level configuration parameters)

            Args:
                request_json (dict)   --  request json that is to be passed

                    Sample: {
                                "name": "",
                                "value": ""
                            }
                OR
                request_json (list)   --  list of Global Param settings
                    Sample: [
                                {
                                    "name": "",
                                    "value": ""
                                },
                                ...
                            ]

            Returns:
                dict                --   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        if  isinstance(request_json, list):
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
            'POST', self._services['GLOBAL_PARAM'], request_json
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def verify_owner_assignment_config(self):

        """ Verifies that the ownership assignments settings are configured and set properly

        Returns:
                dict    -   json response received from the server

        Raises:
            SDKException:
                if response is empty

                if response is not success

                if ownership assignment is not correct

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
    def commserv_guid(self):
        """Returns the GUID of the CommServ."""
        return self._commserv_guid

    @property
    def commserv_hostname(self):
        """Returns the hostname of the CommServ."""
        return self._commserv_hostname

    @property
    def commserv_name(self):
        """Returns the name of the CommServ."""
        return self._commserv_name

    @property
    def commserv_timezone(self):
        """Returns the time zone of the CommServ."""
        return self._commserv_timezone

    @property
    def commserv_timezone_name(self):
        """Returns the name of the time zone of the CommServ."""
        return self._commserv_timezone_name

    @property
    def commserv_version(self):
        """Returns the version installed on the CommServ.

            Example: 19

        """
        return self._commserv_version

    @property
    def version(self):
        """Returns the complete version info of the commserv

            Example: 11.19.1

        """
        return self._version_info

    @property
    def webconsole_hostname(self):
        """Returns the value of the host name of the webconsole used to connect to the Commcell."""
        return self._headers['Host']

    @property
    def auth_token(self):
        """Returns the Authtoken for the current session to the Commcell."""
        return self._headers['Authtoken']

    @property
    def commcell_username(self):
        """Returns the logged in user name"""
        return self._user

    @property
    def device_id(self):
        """Returns the value of the Device ID attribute."""
        try:
            return self._device_id
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def name_change(self):
        """Returns an instance of Namechange class"""
        return NameChange(self)

    @property
    def clients(self):
        """Returns the instance of the Clients class."""
        try:
            if self._clients is None:
                self._clients = Clients(self)

            return self._clients
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_cache(self):
        """Returns the instance of the CommServeCache  class."""
        try:
            if self._commserv_cache is None:
                self._commserv_cache = CommServeCache(self)

            return self._commserv_cache
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def index_servers(self):
        """Returns the instance of the Index Servers class."""
        try:
            if self._index_servers is None:
                self._index_servers = IndexServers(self)

            return self._index_servers
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def hac_clusters(self):
        """Returns the instance of the HAC Clusters class."""
        try:
            if self._hac_clusters is None:
                self._hac_clusters = HACClusters(self)

            return self._hac_clusters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def index_pools(self):
        """Returns the instance of the HAC Clusters class."""
        try:
            if self._index_pools is None:
                self._index_pools = IndexPools(self)

            return self._index_pools
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def media_agents(self):
        """Returns the instance of the MediaAgents class."""
        try:
            if self._media_agents is None:
                self._media_agents = MediaAgents(self)

            return self._media_agents
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def workflows(self):
        """Returns the instance of the Workflows class."""
        try:
            if self._workflows is None:
                self._workflows = WorkFlows(self)

            return self._workflows
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def alerts(self):
        """Returns the instance of the Alerts class."""
        try:
            if self._alerts is None:
                self._alerts = Alerts(self)

            return self._alerts
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disk_libraries(self):
        """Returns the instance of the DiskLibraries class."""
        try:
            if self._disk_libraries is None:
                self._disk_libraries = DiskLibraries(self)

            return self._disk_libraries
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def tape_libraries(self):
        """Returns the instance of the TapeLibraries class"""
        if self._tape_libraries is None:
            self._tape_libraries = TapeLibraries(self)
        return self._tape_libraries

    @property
    def storage_policies(self):
        """Returns the instance of the StoragePolicies class."""
        return self.policies.storage_policies

    @property
    def schedule_policies(self):
        """Returns the instance of the SchedulePolicies class."""
        return self.policies.schedule_policies

    @property
    def schedules(self):
        """Returns the instance of the Schedules class."""
        try:
            if self._schedules is None:
                self._schedules = Schedules(self)

            return self._schedules
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def policies(self):
        """Returns the instance of the Policies class."""
        try:
            if self._policies is None:
                self._policies = Policies(self)

            return self._policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def deduplication_engines(self):
        """Returns the instance of the Deduplicationengines class."""
        try:
            if self._deduplication_engines is None:
                self._deduplication_engines = DeduplicationEngines(self)
            return self._deduplication_engines
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def user_groups(self):
        """Returns the instance of the UserGroups class."""
        try:
            if self._user_groups is None:
                self._user_groups = UserGroups(self)

            return self._user_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def domains(self):
        """Returns the instance of the UserGroups class."""
        try:
            if self._domains is None:
                self._domains = Domains(self)

            return self._domains
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def client_groups(self):
        """Returns the instance of the ClientGroups class."""
        try:
            if self._client_groups is None:
                self._client_groups = ClientGroups(self)

            return self._client_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def global_filters(self):
        """Returns the instance of the GlobalFilters class."""
        try:
            if self._global_filters is None:
                self._global_filters = GlobalFilters(self)

            return self._global_filters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def datacube(self):
        """Returns the instance of the Datacube class."""
        try:
            if self._datacube is None:
                self._datacube = Datacube(self)

            return self._datacube
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def content_analyzers(self):
        """Returns the instance of the ContentAnalyzers class."""
        try:
            if self._content_analyzers is None:
                self._content_analyzers = ContentAnalyzers(self)

            return self._content_analyzers
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def activate(self):
        """Returns the instance of the ContentAnalyzers class."""
        try:
            if self._activate is None:
                self._activate = Activate(self)

            return self._activate
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def plans(self):
        """Returns the instance of the Plans class."""
        try:
            if self._plans is None:
                self._plans = Plans(self)

            return self._plans
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def job_controller(self):
        """Returns the instance of the Jobs class."""
        try:
            if self._job_controller is None:
                self._job_controller = JobController(self)

            return self._job_controller
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def users(self):
        """Returns the instance of the Users class."""
        try:
            if self._users is None:
                self._users = Users(self)

            return self._users
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def roles(self):
        """Returns the instance of the Roles class."""
        try:
            if self._roles is None:
                self._roles = Roles(self)

            return self._roles
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def credentials(self):
        """Returns the instance of the Credentials class."""
        try:
            if self._credentials is None:
                self._credentials = Credentials(self)

            return self._credentials
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def download_center(self):
        """Returns the instance of the DownloadCenter class."""
        try:
            if self._download_center is None:
                self._download_center = DownloadCenter(self)

            return self._download_center
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def organizations(self):
        """Returns the instance of the Organizations class."""
        try:
            if self._organizations is None:
                self._organizations = Organizations(self)

            return self._organizations
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def storage_pools(self):
        """Returns the instance of the StoragePools class."""
        try:
            if self._storage_pools is None:
                self._storage_pools = StoragePools(self)

            return self._storage_pools
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def monitoring_policies(self):
        """Returns the instance of the MonitoringPolicies class."""
        try:
            if self._monitoring_policies is None:
                self._monitoring_policies = MonitoringPolicies(self)

            return self._monitoring_policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def operation_window(self):
        """Returns the instance of the OperationWindow class."""
        try:
            if self._operation_window is None:
                self._operation_window = OperationWindow(self)
            return self._operation_window
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def activity_control(self):
        """Returns the instance of the ActivityControl class."""
        try:
            if self._activity_control is None:
                self._activity_control = ActivityControl(self)

            return self._activity_control
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def event_viewer(self):
        """Returns the instance of the Event Viewer class."""
        try:
            if self._events is None:
                self._events = Events(self)

            return self._events
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def array_management(self):
        """Returns the instance of the ArrayManagement class."""
        try:
            if self._array_management is None:
                self._array_management = ArrayManagement(self)

            return self._array_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disasterrecovery(self):
        """Returns the instance of the DisasterRecovery class."""
        try:
            if self._disaster_recovery is None:
                self._disaster_recovery = DisasterRecovery(self)

            return self._disaster_recovery
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def identity_management(self):
        """Returns the instance of the IdentityManagementApps class."""
        try:
            if self._identity_management is None:
                self._identity_management = IdentityManagementApps(self)

            return self._identity_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def system(self):
        """Returns the instance of the System class."""
        try:
            if self._system is None:
                self._system = System(self)

            return self._system
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_client(self):
        """Returns the instance of the Client class for the CommServ client."""
        if self._commserv_client is None:
            self._commserv_client = self.clients.get(self._commserv_name)

        return self._commserv_client

    @property
    def commcell_migration(self):
        """Returns the instance of the CommcellMigration class"""
        try:
            if self._commcell_migration is None:
                self._commcell_migration = CommCellMigration(self)

            return self._commcell_migration
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def registered_routing_commcells(self):
        """Returns the dictionary consisting of all registered commcells and
        their info

        dict - consists of all registered routing commcells
            {
                "commcell_name1:{
                    details related to commcell_name1
                },
                "commcell_name2:{
                    details related to commcell_name2
                }
            }
        """
        if self._registered_commcells is None:
            self._registered_commcells = self._get_registered_service_commcells()
        return self._registered_commcells

    @property
    def redirect_rules_of_service(self):
        """Returns the list of redirect rules from service commcell

        list - consists of redirect rules of service commcell
            ['abc.com','commvault-nj']
        """
        if self._redirect_rules_service is None:
            self._redirect_rules_service = self._get_redirect_rules_service_commcell()
        return self._redirect_rules_service

    @property
    def replication_groups(self):
        """Returns the instance of ReplicationGroups class"""
        try:
            if self._replication_groups is None:
                self._replication_groups = ReplicationGroups(self)
            return self._replication_groups

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def recovery_targets(self):
        """Returns the instance of RecoverTargets class"""
        try:
            if self._recovery_targets is None:
                self._recovery_targets = RecoveryTargets(self)

            return self._recovery_targets

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def blr_pairs(self):
        """Returns the instance of BLRPairs class"""
        try:
            if self._blr_pairs is None:
                self._blr_pairs = BLRPairs(self)

            return self._blr_pairs

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def backup_network_pairs(self):
        """Returns the instance of BackupNetworkPairs class"""
        try:
            if self._backup_network_pairs is None:
                self._backup_network_pairs = BackupNetworkPairs(self)

            return self._backup_network_pairs

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def reports(self):
        """Returns the instance of the Report class"""
        try:
            if self._reports is None:
                self._reports = report.Report(self)
            return self._reports
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def job_management(self):
        """Returns the instance of the JobManagement class."""
        try:
            if not self._job_management:
                self._job_management = JobManagement(self)
            return self._job_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commcells_for_user(self):
        """returns the list of accessible commcells to logged in user

        list - contains the list of accessible commcells
            ['cc1','cc2']
        """
        if self._redirect_cc_idp is None:
            self._redirect_cc_idp = self._commcells_for_user()
        return self._redirect_cc_idp

    @property
    def commserv_metadata(self):
        """Returns the metadata of the commserv."""
        if self._commserv_metadata is None:
            self._commserv_metadata = self._get_commserv_metadata()
        return self._commserv_metadata

    @property
    def metallic(self):
        """Returns the instance of the Metallic class."""
        try:
            if self._metallic is None:
                self._metallic = Metallic(self)

            return self._metallic
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def is_privacy_enabled(self):
        """Method to return if the privacy is enabled at commcell level or not"""
        if self._commcell_properties is None:
            self.get_commcell_properties()

        self._privacy = self._commcell_properties.get('enablePrivacy')

        return self._privacy

    @property
    def key_management_servers(self):
        """Returns the instance of the KeyManagementServers class."""
        try:
            if self._kms is None:
                self._kms = KeyManagementServers(self)

            return self._kms
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def logout(self):
        """Logs out the user associated with the current instance."""
        if self._headers['Authtoken'] is None:
            return 'User already logged out.'

        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def request(self, request_type, request_url, request_body=None):
        """Runs the request of the type specified on the request URL, with the body passed
            in the arguments.

            Args:
                request_type    (str)   --  type of HTTP request to run on the Commcell

                    e.g.;

                        - POST

                        - GET

                        - PUT

                        - DELETE

                request_url     (str)   --  API name to run the request on with params, if any

                    e.g.;

                        - Backupset

                        - Agent

                        - Client

                        - Client/{clientId}

                        - ...

                        etc.

                request_body    (dict)  --  JSON request body to pass along with the request

                    default: None

            Returns:
                object  -   the response received from the server

        """
        request_url = self._web_service + request_url

        _, response = self._cvpysdk_object.make_request(
            request_type.upper(), request_url, request_body
        )

        return response

    def send_mail(self, receivers, subject, body=None, copy_sender=False, is_html_content=True):
        """Sends a mail to the specified email address from the email asscoiated to this user

            Args:
                receivers       (list)  --  list of email addresses to whom the email is to
                be sent

                subject         (str)   --  subject of the email that is to be sent to the user

                body            (str)   --  email body that is to be included in the email

                copy_sender     (bool)  --  copies the sender in the html report that is sent

                is_html_content (bool)  --  determines if the email body has html content

                    True    -   the email body has html content

                    False   -   the email content is plain text

            Raises:
                SDKException:
                    if failed to send an email to specified user

                    if response is empty

                    if response is not success

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

        response_json = self._qoperation_execute(send_email_request)

        if response_json.get('errorCode', 0) != 0:
            raise SDKException(
                'Commcell',
                '104',
                'Error: "{}"'.format(response_json['errorMessage'])
            )

    def refresh(self):
        """Refresh the properties of the Commcell."""
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
        self._content_analyzers = None
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
        self._get_commserv_details()
        self._registered_commcells = None
        self._redirect_rules_service = None
        self._index_servers = None
        self._hac_clusters = None
        self._index_pools = None
        self._deduplication_engines = None
        self._tfa = None

    def get_remote_cache(self, client_name):
        """Returns the instance of the RemoteCache  class."""
        try:
            self._remote_cache = RemoteCache(self, client_name)
            return self._remote_cache

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def run_data_aging(
            self,
            copy_name=None,
            storage_policy_name=None,
            is_granular=False,
            include_all=True,
            include_all_clients=False,
            select_copies=False,
            prune_selected_copies=False,
            schedule_pattern=None):
        """
        Runs the Data Aging from Commcell,SP and copy level


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

    def get_saml_token(self, validity=30):
        """Returns the SAML token for the currently logged-in user.

            Args:
                validity    (int)   --  validity of the SAML token, **in minutes**

                    default: 30

            Returns:
                str     -   SAML token string received from the server

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

                    raise SDKException(
                        'Commcell',
                        '106',
                        'Error Code: {0}\nError Message: {1}'.format(error_code, error_message)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_additional_setting(self, category, key_name, data_type, value):
        """Adds registry key to the commserve property.

            Args:
                category    (str)   --  Category of registry key

                key_name    (str)   --  Name of the registry key

                data_type   (str)   --  Data type of registry key

                    Accepted Values:
                        - BOOLEAN
                        - INTEGER
                        - STRING
                        - MULTISTRING
                        - ENCRYPTED

                value   (str)   --  Value of registry key

            Returns:
                None

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected

        """
        self.commserv_client.add_additional_setting(category, key_name, data_type, value)

    def delete_additional_setting(self, category, key_name):
        """Deletes registry key from the commserve property.

            Args:
                category    (str)   --  Category of registry key

                key_name    (str)   --  Name of the registry key

            Returns:
                None

            Raises:
                SDKException:
                    if failed to delete

                    if response is empty

                    if response code is not as expected

        """
        self.commserv_client.delete_additional_setting(category, key_name)

    def protected_vms(self, days, limit=100):
        """
        Returns all the protected VMs for the particular client for passed days
        Args:
            days: Protected VMs for days
                ex: if value is 30 , returns VM protected in past 30 days

            limit: Number of Protected VMs
                ex: if value is 50, returns 50 protected vms are returned
                    if value is 0, all the protected vms are returned
                    default value is 100

        Returns:
                vm_dict -  all properties of VM protected for passed days

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

    def sync_remote_cache(self, client_list=None):
        """Syncs remote cache

            Args:

                client_list (list) --  list of client names.
                Default is None. By default all remote cache clients are synced

            Returns:
                object - instance of the Job class for sync job

            Raises:
                SDKException:
                    if sync job failed

                    if response is empty

                    if response is not success

                    if another sync job is running with the given client

        """
        download = Download(self)
        return download.sync_remote_cache(
            client_list=client_list)

    def download_software(self,
                          options=None,
                          os_list=None,
                          service_pack=None,
                          cu_number=0,
                          sync_cache=True,
                          schedule_pattern=None):
        """Downloads the os packages on the commcell

            Args:

                options      (enum)            --  Download option to download software

                os_list      (list of enum)    --  list of windows/unix packages to be downloaded

                service_pack (int)             --  service pack to be downloaded

                cu_number (int)                --  maintenance release number

                sync_cache (bool)              --  True if download and sync
                                                   False only download

            Returns:
                object - instance of the Job class for this download job

            Raises:
                SDKException:
                    if Download job failed

                    if response is empty

                    if response is not success

                    if another download job is running

            Usage:

            -   if download_software is not given any parameters it takes default value of latest
                service pack for options and downloads WINDOWS_64 package

                >>> commcell_obj.download_software()

            -   DownloadOptions and DownloadPackages enum is used for providing input to the
                download software method, it can be imported by

                >>> from cvpysdk.deployment.deploymentconstants import DownloadOptions
                    from cvpysdk.deployment.deploymentconstants import DownloadPackages

            -   sample method calls for different options, for latest service pack

                >>> commcell_obj.download_software(
                        options=DownloadOptions.LATEST_SERVICEPACK.value,
                        os_list=[DownloadPackages.WINDOWS_64.value]
                        )

            -   For Latest hotfixes for the installed service pack

                >>> commcell_obj.download_software(
                        options='DownloadOptions.LATEST_HOTFIXES.value',
                        os_list=[DownloadPackages.WINDOWS_64.value,
                                DownloadPackages.UNIX_LINUX64.value]
                        )

            -   For service pack and hotfixes

                >>> commcell_obj.download_software(
                        options='DownloadOptions.SERVICEPACK_AND_HOTFIXES.value',
                        os_list=[DownloadPackages.UNIX_MAC.value],
                        service_pack=13
                        )

                    **NOTE:** service_pack parameter must be specified for third option

        """
        download = Download(self)
        return download.download_software(
            options=options,
            os_list=os_list,
            service_pack=service_pack,
            cu_number=cu_number,
            sync_cache=sync_cache,
            schedule_pattern=schedule_pattern
        )

    def push_servicepack_and_hotfix(
            self,
            client_computers=None,
            client_computer_groups=None,
            all_client_computers=False,
            all_client_computer_groups=False,
            reboot_client=False,
            run_db_maintenance=True,
            maintenance_release_only=False):
        """triggers installation of service pack and hotfixes

        Args:
            client_computers    (list)      -- Client machines to install service pack on

            client_computer_groups (list)   -- Client groups to install service pack on

            all_client_computers (bool)     -- boolean to specify whether to install on all client
            computers or not

                default: False

            all_client _computer_groups (bool) -- boolean to specify whether to install on all
            client computer groups or not

                default: False

            reboot_client (bool)            -- boolean to specify whether to reboot the client
            or not

                default: False

            run_db_maintenance (bool)      -- boolean to specify whether to run db
            maintenance not

                default: True

            maintenance_release_only (bool) -- for clients of feature releases lesser than CS, this option
            maintenance release of that client FR, if present in cache

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
        install = Install(self)
        return install.push_servicepack_and_hotfix(
            client_computers=client_computers,
            client_computer_groups=client_computer_groups,
            all_client_computers=all_client_computers,
            all_client_computer_groups=all_client_computer_groups,
            reboot_client=reboot_client,
            run_db_maintenance=run_db_maintenance,
            maintenance_release_only=maintenance_release_only
        )

    def install_software(
            self,
            client_computers=None,
            windows_features=None,
            unix_features=None,
            username=None,
            password=None,
            install_path=None,
            log_file_loc=None,
            client_group_name=None,
            storage_policy_name=None,
            sw_cache_client=None,
            **kwargs):
        """
        Installs the selected features in the selected clients
        Args:

            client_computers    (list)      -- list of hostnames/IP address to install the
            features on

                default : None

            windows_features (list of enum) -- list of windows features to be installed

                default : None

            unix_features (list of enum)    -- list of unix features to be installed

                default : None

            username    (str)               -- username of the machine to install features on

                default : None

            password    (str)               -- base64 encoded password

                default : None

            install_path (str)              -- Install to a specified path on the client

                 default : None

            log_file_loc (str)              -- Install to a specified log path on the client

                 default : None

            client_group_name (list)        -- List of client groups for the client

                 default : None

            storage_policy_name (str)       -- Storage policy for the default subclient

                 default : None

            sw_cache_client (str)           -- Remote Cache Client Name/ Over-riding Software Cache

                default : None (Use CS Cache by default)

            **kwargs: (dict) -- Key value pairs for supporting conditional initializations
            Supported -
            install_flags (dict)            -- dictionary of install flag values

                default : None

            Ex : install_flags = {"preferredIPfamily":2, "install32Base":True}

            db2_logs_location (dict) - dictionary of db2 logs location

                default : None
                
            Ex: db2_logs_location = {
                                    "db2ArchivePath": "/opt/Archive/",
                                    "db2RetrievePath": "/opt/Retrieve/",
                                    "db2AuditErrorPath": "/opt/Audit/"
                            }

        Returns:
                object - instance of the Job class for this install_software job

        Raises:
            SDKException:
                if install job failed

                if response is empty

                if response is not success

        Usage:

            -   UnixDownloadFeatures and WindowsDownloadFeatures enum is used for providing
                input to the install_software method, it can be imported by

                >>> from cvpysdk.deployment.deploymentconstants import UnixDownloadFeatures
                    from cvpysdk.deployment.deploymentconstants import WindowsDownloadFeatures

            -   sample method call

                >>> commcell_obj.install_software(
                                client_computers=[win_machine1, win_machine2],
                                windows_features=[WindowsDownloadFeatures.FILE_SYSTEM.value],
                                unix_features=None,
                                username='username',
                                password='password',
                                install_path='/opt/commvault',
                                log_file_loc='/var/log',
                                client_group_name=[My_Servers],
                                storage_policy_name='My_Storage_Policy',
                                sw_cache_client="remote_cache_client_name"
                                install_flags={"preferredIPFamily":2})

                    **NOTE:** Either Unix or Windows clients_computers should be chosen and
                    not both

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

    def enable_auth_code(self):
        """Executes the request on the server to enable Auth Code for installation on commcell

            Args:
                None

            Returns:
                str     -   auth code generated from the server

            Raises:
                SDKException:
                    if failed to enable auth code generation

                    if response is empty

                    if response is not success

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

    def enable_shared_laptop(self):
        """Executes the request on the server to enable Shared Laptop on commcell

            Args:
                None

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty
                    if failed to enable shared laptop
                    if response is not success
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

    def disable_shared_laptop(self):
        """Executes the request on the server to disable Shared Laptop on commcell

            Args:
                None

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty
                    if failed to disable shared laptop
                    if response is not success

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

    def enable_privacy(self):
        """Enables users to enable data privacy on commcell"""
        if self.is_privacy_enabled is True:
            return

        self.set_privacy(True)

    def disable_privacy(self):
        """Enables users to disable data privacy on commcell"""
        if self.is_privacy_enabled is False:
            return

        self.set_privacy(False)

    def set_privacy(self, value):
        """
        Method to enable/disble privacy
            Args:
                value (bool): True/False to enable/disable privacy

        Raises:
                SDKException:
                    if response is empty
                    if failed to disable privacy
                    if response is not success
        """
        url = self._services['PRIVACY_DISABLE']
        if value:
            url = self._services['PRIVACY_ENABLE']

        flag, response = self._cvpysdk_object.make_request(
            'PUT', url
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

    def get_commcell_properties(self):
        """ Get Commcell properties

        Returns: (dict)
            "hostName": String,
            "enableSharedLaptopUsage": Boolean,
            "enableTwoFactorAuthentication": Boolean,
            "networkErrorRetryCount": Number,
            "useUPNForEmail": Boolean,
            "flags": Number,
            "description": String,
            "networkErrorRetryFreq": Number,
            "autoClientOwnerAssignmentType": Number,
            "networkErrorRetryFlag": Boolean,
            "allowUsersToEnablePasskey": Boolean,
            "autoClientOwnerAssignmentValue": String,
            "enablePrivacy": Boolean,
            "twoFactorAuthenticationInfo": {
                "mode": Number
            }
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

    def get_commcell_organization_properties(self):
        """
            Get organization properties for the commcell
        return:
            dict of organization properties of commcell
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

    def get_email_settings(self):
        """
            Get Email Server (SMTP) setup for commcell
        return: (dict) Email server settings for commcell
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

    def get_password_encryption_config(self):
        """ Get the password encryption config for commcell
        returns: (dict)
            "keyFilePath": String,
            "keyProviderName": String,
            "isKeyMovedToFile": Boolean
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

    def get_security_associations(self):
        """ Get the security associations for commcell
            Returns: (dict)
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

    def get_default_plan(self):
        """Executes the request on the server to get Default Plan at commcell level.
           This is independent of the organization, as id is 0.
           returns: (list of dictionaries)
                 [
                 { "subtype": 'File system plan', "plan": { "planName": "Gold plan", "planId": 2 } }
                ]
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

    def set_default_plan(self, plan_name):
        """Executes the request on the server to set Default Plan at commcell level.
            This is independent of the organization, as id is 0.

            Args:
                plan_name (str)    - Plan name

            Returns:
                None

            Raises:
                SDKException:
                    if failed to set Default plan

                    if response is empty

                    if response is not success

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

    def execute_qcommand(self, command, input_xml=None):
        """Executes the ExecuteQCommand API on the commcell.

            Args:
                command     (str)   --  qcommand to be executed

                input_xml   (str)   --  xml body (if applicable)

                    default:    None

            Returns:
                object  -   requests.Response object

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def add_associations_to_saml_app(self, saml_app_name, saml_app_key, props, user_to_be_added):
        """adds the given  user under associations tab of the saml app
            Args:
                saml_app_name   (str)   : SAML app name to add associations for

                saml_app_key    (str)   :app key of the SAML app

                props   (str)   :properties to be included in the XML request

                user_to_be_added    (str)   : user to be associated with

            Raises:
                SDKException:
                    if input data is invalid

                    if response is empty

                    if response is not success
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

    def _get_registered_service_commcells(self):
        """Gets the registered routing commcells

            Returns:
                dict - consists of all registered routing commcells
                    {
                        "commcell_name1": {
                            related information of commcell1
                        },
                        "commcell_name2:: {
                            related information of commcell2
                        }
                    }
            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['GET_REGISTERED_ROUTER_COMMCELLS']
        )

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

    def _get_redirect_rules_service_commcell(self):
        """gets the redirect rules from service commcell

        Returns:
            list - consisting of all redirect rules associated with service commcell

                ['abc.com', 'abc', 'commvault-nj']
        Raises:
            SDKException:
                if response is empty

                if response is not success
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['GET_USERSPACE_SERVICE']
        )

        if flag:
            if response.json() and 'redirectRules' in response.json():
                redirect_rules_list = []
                redirect_rules_list = response.json()['redirectRules']['domains'] + \
                    response.json()['redirectRules']['rules']
                return redirect_rules_list
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def is_commcell_registered(self, commcell_name):
        """checks if a commcell is registered in the commcell
                    with the provided name
            Args:
                commcell_name (str) -- name of the commcell

            Returns:
                bool - boolean output whether the commcell is registered or not

            Raises:
                SDKException:
                    if type of the commcell_name is not string
        """
        if not isinstance(commcell_name, basestring):
            raise SDKException('CommcellRegistration', '104')

        return self.registered_routing_commcells and commcell_name.lower() in self.registered_routing_commcells

    def register_commcell(
            self,
            commcell_name,
            registered_for_routing=False,
            admin_username=None,
            admin_password=None,
            register_for_idp=None):
        """Registers a commcell

        Args:

            commcell_name   (str)           -- name of the commcell

            registered_for_routing (bool)   -- True - if we want to register for Routing
                                               False - if we dont want to register for Routing

            admin_username   (str)          -- username of the user who has administrative
                                                rights on a commcell

            admin_password  (str)           -- password of the user specified

            register_for_idp (bool)         -- True - if we want to register for Identity provider
                                                False - if we dont want to register for Identity provider

        Raises:

            SDKException:

                if the registration fails
                if response is empty
                if there is no response

        """
        commcell_name = commcell_name.lower()
        registered_for_routing = 1 if registered_for_routing else 0
        register_for_idp = 1 if register_for_idp else 0

        xml_to_execute = """
        <EVGui_CN2CellRegReq>
            <commcell isRegisteredForRouting="{0}" adminPwd="{1}" adminUsr="{2}" interfaceName="{3}" ccClientName="{3}"
            isGlobalIDPCommcell="{4}">
                <commCell commCellName="{3}" />
            </commcell>
        </EVGui_CN2CellRegReq>
        """.format(
            registered_for_routing,
            admin_password,
            admin_username,
            commcell_name,
            register_for_idp
        )

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['REGISTRATION'], xml_to_execute
        )

        if flag:
            if response.json():
                error_code = response.json()['resultCode']

                if error_code != 0:
                    error_string = response.json()['resultMessage']
                    if error_code == 1013:
                        raise SDKException('CommcellRegistration', '105')

                    elif error_code == 1007:
                        raise SDKException('CommcellRegistration', '106')

                    elif error_code == 1010:
                        raise SDKException('CommcellRegistration', '107', '{0}'.format(error_string))

                    else:
                        raise SDKException(
                            'CommcellRegistration', '101', 'Registration Failed\n Error: "{0}"'.format(
                                error_string
                            )
                    )
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def service_commcell_sync(self, service_commcell):
        """ Sync a service commcell

        Args:

        service_commcell    (object)    : Service commcell object

        Raises:

            if sync fails
            if the response is empty
            if there is no response

        """
        if not isinstance(service_commcell, Commcell):
            raise SDKException('CommcellRegistration', '104')

        guid = service_commcell.commserv_guid
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['SYNC_SERVICE_COMMCELL'] % guid
        )

        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code != 0:
                    error_string = response.json()['errorMessage']
                    raise SDKException(
                        'CommcellRegistration',
                        '102',
                        'Sync operation failed\n Error: "{0}"'.format(
                            error_string
                        )
                    )
                self.refresh()

                service_commcell.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def unregister_commcell(self, commcell_name):
        """Unregisters a commcell

        Args:

            commcell_name       (str) - Name of the service commcell that has to be unregistered

        Raises:

            if Unregistration fails
            if the response is empty
            if there is no response

        """
        if not isinstance(commcell_name, basestring):
            raise SDKException('CommcellRegistration', '104')
        else:
            commcell_name = commcell_name.lower()
            if self.is_commcell_registered(commcell_name):
                xml_to_execute = """
                <EVGui_CN2RemoveCellRegReq>
                    <commcell ccClientId="{0}" ccClientName="{1}" interfaceName="{2}">
                        <commCell _type_="{3}" commCellId="{4}" csGUID="{5}"/>
                    </commcell>
                </EVGui_CN2RemoveCellRegReq>
                """.format(
                    self._registered_commcells[commcell_name]['ccClientId'],
                    self._registered_commcells[commcell_name]['ccClientName'],
                    self._registered_commcells[commcell_name]['interfaceName'],
                    self._registered_commcells[commcell_name]['commCell']['_type_'],
                    self._registered_commcells[commcell_name]['commCell']['commCellId'],
                    self._registered_commcells[commcell_name]['commCell']['csGUID']
                )

                flag, response = self._cvpysdk_object.make_request(
                    'POST', self._services['UNREGISTRATION'], xml_to_execute
                )

                if flag:
                    if response.json():
                        error_code = response.json()['resultCode']

                        if error_code != 0:
                            error_string = response.json()['resultMessage']
                            raise SDKException(
                                'CommcellRegistration',
                                '103',
                                'UnRegistration Failed\n Error: "{0}"'.format(
                                    error_string
                                )
                            )
                        self.refresh()
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)

    def get_eligible_service_commcells(self, login_name_or_email=None):
        """Gets the redirect service commcells based on login_name or email provided

        Args:

            login_name_or_email      (str)   -- Login name or email of the user

                default: current logged in user

        Raises:

            if the response is empty
            if there is no response

        Returns:

            list_of_service_commcells   (list)  -- list of service commcells

        """
        if not login_name_or_email:
            login_name_or_email = self.commcell_username

        login_name_or_email = login_name_or_email.lower()
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['POLL_REQUEST_ROUTER'] %
            login_name_or_email
        )
        if flag:
            if response.json() and 'AvailableRedirects' in response.json():
                service_commcell_list = []
                for ser_comm in response.json()['AvailableRedirects']:
                    if ser_comm.get('isLocalCommcell', False):
                        continue
                    service_commcell_list.append(ser_comm['commcellName'])
                return service_commcell_list
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _commcells_for_user(self):
        """returns the list of accessible commcells to logged in user

        Returns:
            list - consists list of accessible commcells

                ['S1', 'S2']
        Raises:
            SDKException:
                if response is empty

                if response is not success
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['MULTI_COMMCELL_DROP_DOWN']
        )

        if flag:
            if response.json() and 'AvailableRedirects' in response.json():
                redirect_cc_list = []
                for ser_comm in response.json()['AvailableRedirects']:
                    if ser_comm.get('commcellName', False):
                        continue
                    redirect_cc_list.append(ser_comm['commcellName'])
                if 'cloudServices' in response.json():
                    redirect_cc_list.append(response.json()['cloudServices'][0]['commcellName'])
                return redirect_cc_list
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _service_commcells_association(self):
        """returns the associated entities to a service commcell

        Returns:

                        dict of associated entities to a service commcell

        Raises:

            SDKException:
                if response is empty

                if response is not success
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['SERVICE_COMMCELL_ASSOC']
        )

        if flag:
            if response.json() and 'associations' in response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add_service_commcell_associations(self, entity_name, service_commcell):
        """adds an association for an entity on a service commcell

        Args:

            entity_name  (object)     -- entity_name can be object of User,UserGroup,Domain and Organization Class

            service_commcell (str)    --  name of the service commcell to which above entities can be associated

        Raises:
            SDKException:
                if response is empty

                if add association fails

                if response is not success
        """

        if not isinstance(service_commcell, basestring):
            raise SDKException('User', '101')

        request_json = {
            "userOrGroup": {
            },
            "entity": {
                "entityType": 194,
                "entityName": self.registered_routing_commcells[service_commcell]['commCell']['commCellName'],
                "_type_": 150,
                "entityId": self.registered_routing_commcells[service_commcell]['commCell']['commCellId'],
                "flags": {
                    "includeAll": False
                }
            },
            "properties": {
                "role": {
                    "_type_": 120,
                    "roleId": 3,
                    "roleName": "View"
                }
            }
        }

        if isinstance(entity_name, User):
            request_json['userOrGroup']['userId'] = int(entity_name.user_id)
            request_json['userOrGroup']['userName'] = entity_name.user_name
            request_json['userOrGroup']['_type_'] = 13

        if isinstance(entity_name, UserGroup):
            request_json['userOrGroup']['userGroupId'] = int(entity_name.user_group_id)
            request_json['userOrGroup']['userGroupName'] = entity_name.user_group_name
            request_json['userOrGroup']['_type_'] = 15

        if isinstance(entity_name, Organization):
            request_json['providerType'] = 5
            request_json['userOrGroup']['providerId'] = int(entity_name.organization_id)
            request_json['userOrGroup']['providerDomainName'] = entity_name.organization_name
            request_json['userOrGroup']['_type_'] = 61

        if isinstance(entity_name, Domain):
            request_json['providerType'] = 2
            request_json['userOrGroup']['providerId'] = int(entity_name.domain_id)
            request_json['userOrGroup']['providerDomainName'] = entity_name.domain_name
            request_json['userOrGroup']['_type_'] = 61

        res_json = self._service_commcells_association()
        res_json['associations'].append(request_json)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['SERVICE_COMMCELL_ASSOC'], res_json
        )

        if flag:
            if response.json():
                error_code = response.json().get('response', [{}])[0].get('errorCode', -1)

                if error_code != 0:
                    error_string = response.json().get('response', [{}])[0].get('errorString')
                    raise SDKException(
                        'CommcellRegistration',
                        '102',
                        'Service Commcell Association Failed\n Error: "{0}"'.format(
                            error_string
                        )
                    )
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def is_service_commcell(self):
        """Returns the is_service_commcell property."""

        return self._is_service_commcell

    @property
    def master_saml_token(self):
        """Returns the saml token of master commcell."""

        return self._master_saml_token

    @property
    def two_factor_authentication(self):
        """Returns the instance of the TwoFactorAuthentication class"""
        try:
            if self._tfa is None:
                self._tfa = TwoFactorAuthentication(self)
            return self._tfa
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def is_tfa_enabled(self):
        """
        Returns the status of two factor authentication for this commcell

            bool    --  status of tfa.
        """
        return self.two_factor_authentication.is_tfa_enabled

    @property
    def tfa_enabled_user_groups(self):
        """
        Returns the list of user group names for which two factor authentication is enabled.
         only for user group inclusion tfa.
            eg:-
            [
                {
                "userGroupId": 1,
                "userGroupName": "dummy"
                }
            ]
        """
        return self.two_factor_authentication.tfa_enabled_user_groups

    @property
    def is_linux_commserv(self):
        """Returns true if CommServer is installed on the linux machine

            Returns None if unable to determine the CommServ OS type

			**Note** To determine CommServ OS type logged in user
				should have access on CommServ client
		"""
        if self._is_linux_commserv is None and self.clients.has_client(self._commserv_name):
            self._is_linux_commserv = 'unix' in self.commserv_client.os_info.lower()
        return self._is_linux_commserv

    @property
    def default_timezone(self):
        """Returns the default timezone used for all the operations performed via cvpysdk"""
        return 'UTC' if self.is_linux_commserv else '(UTC) Coordinated Universal Time'

    def enable_tfa(self, user_groups=None):
        """
        Enables two factor authentication option on this commcell.

        Args:
            user_groups     (list)  --  user group names for which tfa needs to be enabled.

        Returns:
            None
        """
        self.two_factor_authentication.enable_tfa(user_groups=user_groups)

    def disable_tfa(self):
        """
        Disables two factor authentication on this commcell.

        Returns:
            None
        """
        self.two_factor_authentication.disable_tfa()

    def _get_commserv_metadata(self):
        """loads  the metadata of the CommServ, the Commcell class instance is initialized for,
            and updates the class instance attributes.

            Returns:
                commserv_metadata (dict) : returns a dict containing commserv_redirect_url and commserv_certificate

            Raises:
                SDKException:
                    if failed to get commserv details


                    if response is not success

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

    def switch_to_company(self, company_name):
        """Switching to Company as Operator"""
        if self.organizations.has_organization(company_name):
            self._headers['operatorCompanyId'] = str(self.organizations.get(company_name).organization_id)
        else:
            raise SDKException('Organization', 103)

    def reset_company(self):
        """Resets company to Commcell"""
        if 'operatorCompanyId' in self._headers:
            self._headers.pop('operatorCompanyId')
            
    def allow_users_to_enable_passkey(self, flag):
        """Enable or Disable passkey authorization for company administrators and client owners
        
        Args:
            flag (boolean)  --  Enable or Disable Passkey Authorization
            
        Raises:
            SDKException:
                if response is empty
                if response is not success
                if failed to enable or disable passkey
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