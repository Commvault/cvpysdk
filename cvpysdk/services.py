# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Service URLs for REST API operations.

SERVICES_DICT:
    A python dictionary for holding all the API services endpoints.

|

get_services(web_service):
    updates the SERVICES_DICT with the WebConsole API URL


To add a new REST API End-point to the SDK, user needs to add a key to the SERVICES_DICT_TEMPLATE
dictionary, for their usage, and the value will be in the format:

    "{0}{{ENDPOINT}}"

{0} will be replaced by the webconsole URL

"""

from __future__ import absolute_import
from __future__ import unicode_literals


SERVICES_DICT_TEMPLATE = {
    'LOGIN': '{0}Login',
    'LOGOUT': '{0}Logout',
    'RENEW_LOGIN_TOKEN': '{0}RenewLoginToken',
    'COMMSERV': '{0}CommServ',
    'GET_SAML_TOKEN': '{0}Commcell/SamlToken?validityInMins=%s',
    'WHO_AM_I': '{0}WhoAmI',

    'GET_ALL_CLIENTS': '{0}Client',
    'GET_VIRTUAL_CLIENTS': '{0}Client?PseudoClientType=VSPseudo',
    'CLIENT': '{0}Client/%s',
    'GET_ALL_CLIENTS_PLUS_HIDDEN': '{0}Client?hiddenclients=true',
    'GET_ALL_PSEUDO_CLIENTS': '{0}Client?PseudoClientType',
    'CHECK_READINESS': '{0}Client/%s/CheckReadiness?network=true&resourceCapacity=false',

    'GET_ALL_AGENTS': '{0}Agent?clientId=%s',
    'AGENT': '{0}Agent',
    'GET_AGENT': '{0}Agent?clientId=%s&applicationId=%s',

    'GET_ALL_BACKUPSETS': '{0}Backupset?clientId=%s&propertyLevel=10',
    'BACKUPSET': '{0}Backupset/%s',
    'ADD_BACKUPSET': '{0}Backupset',

    'GET_ALL_INSTANCES': '{0}Instance?clientId=%s',
    'INSTANCE': '{0}Instance/%s',

    'GET_ALL_SUBCLIENTS': '{0}Subclient?clientId=%s&propertyLevel=20',
    'ADD_SUBCLIENT': '{0}Subclient',
    'SUBCLIENT': '{0}Subclient/%s',
    'SUBCLIENT_BACKUP': '{0}Subclient/%s/action/backup?backupLevel=%s',

    'GET_JOBS': '{0}Job?clientId=%s&jobFilter=%s',
    'JOB': '{0}Job/%s',
    'JOB_DETAILS': '{0}JobDetails',
    'SUSPEND_JOB': '{0}Job/%s/action/pause',
    'RESUME_JOB': '{0}Job/%s/action/resume',
    'KILL_JOB': '{0}Job/%s/action/kill',
    'ALL_JOBS': '{0}Jobs',

    'GET_MEDIA_AGENTS': '{0}V2/MediaAgents',
    'LIBRARY': '{0}Library',
    'GET_LIBRARY_PROPERTIES': '{0}Library/%s',

    'STORAGE_POLICY': '{0}StoragePolicy',
    'GET_STORAGE_POLICY': '{0}StoragePolicy/%s',
    'CREATE_STORAGE_POLICY_COPY': '{0}StoragePolicy?Action=createCopy',
    'DELETE_STORAGE_POLICY_COPY': '{0}StoragePolicy?Action=deleteCopy',
    'SCHEDULE_POLICY': '{0}SchedulePolicy',
    'CREATE_UPDATE_SCHEDULE_POLICY': '{0}Task',
    'GET_SCHEDULE_POLICY': '{0}SchedulePolicy/%s',
    'MEDIA_AGENT': '{0}MediaAgent/%s',
    'STORAGE_POLICY_COPY': '{0}V2/StoragePolicy/%s/Copy/%s',

    'GET_ALL_ALERTS': '{0}AlertRule',
    'ALERT': '{0}AlertRule/%s',
    'MODIFY_ALERT': '{0}AlertRule/%s/Action/Modify',
    'GET_ALL_CONSOLE_ALERTS': '{0}Alert?pageNo=%s&pageCount=%s',
    'ENABLE_ALERT_NOTIFICATION': '{0}AlertRule/%s/notificationType/%s/Action/Enable',
    'DISABLE_ALERT_NOTIFICATION': '{0}AlertRule/%s/notificationType/%s/Action/Disable',
    'ENABLE_ALERT': '{0}AlertRule/%s/Action/Enable',
    'DISABLE_ALERT': '{0}AlertRule/%s/Action/Disable',

    'CLIENT_SCHEDULES': '{0}Schedules?clientId=%s',
    'AGENT_SCHEDULES': '{0}Schedules?clientId=%s&apptypeId=%s',
    'BACKUPSET_SCHEDULES': '{0}Schedules?clientId=%s&apptypeId=%s&backupsetId=%s',
    'SUBCLIENT_SCHEDULES': ('{0}Schedules?clientId=%s&apptypeId=%s&'
                            'backupsetId=%s&subclientId=%s'),
    'REPORT_SCHEDULES': '{0}/ScheduleReports',
    'OPTYPE_SCHEDULES': '{0}/Schedules?operationType=%s',
    'COMMCELL_SCHEDULES': '{0}/Schedules',
    'SCHEDULE': '{0}Schedules/%s',
    'ENABLE_SCHEDULE': '{0}Schedules/task/Action/Enable',
    'DISABLE_SCHEDULE': '{0}Schedules/task/Action/Disable',

    'LIVE_SYNC': '{0}Task',

    'CLIENTGROUPS': '{0}ClientGroup',
    'CLIENTGROUP': '{0}ClientGroup/%s',

    'USERGROUPS': '{0}UserGroup?includeSystemCreated=true',
    'USERGROUP': '{0}UserGroup/%s',
    'DELETE_USERGROUP': '{0}UserGroup/%s?newUserId=%s&newUserGroupId=%s',

    'BROWSE': '{0}DoBrowse',
    'RESTORE': '{0}CreateTask',

    'GET_WORKFLOWS': '{0}Workflow',
    'DEPLOY_WORKFLOW': '{0}Workflow/%s/action/deploy',
    'EXECUTE_WORKFLOW': '{0}wapi/%s',
    'GET_WORKFLOW': '{0}Workflow/%s',
    'GET_INTERACTIONS': '{0}WorkflowInteractions',
    'GET_INTERACTION': '{0}Workflow/Interaction/%s',

    'INSTANCE_BROWSE': '{0}Client/%s/%s/Instance/%s/Browse',

    'SQL_RESTORE_OPTIONS': '{0}SQL/RestoreOptions',

    'EXECUTE_QCOMMAND': '{0}Qcommand/qoperation execute',
    'EXECUTE_QSCRIPT': '{0}Qcommand/qoperation execscript %s',
    'QCOMMAND': '{0}QCommand',
    'EXEC_QCOMMAND': '{0}ExecuteQCommand',

    'SOFTWARESTORE_DOWNLOADITEM': '{0}DownloadFile',
    'SOFTWARESTORE_PKGINFO': '{0}SoftwareStore/getPackagePublishInfo?packageName=%s',
    'SOFTWARESTORE_GETPKGID': '{0}SoftwareStoreItem',

    'CREATE_TASK': '{0}CreateTask',
    'ADD_INSTANCE': '{0}Instance',
    'MASKING_POLICY': '{0}MaskingPolicy',


    'GET_ANALYTICS_ENGINES': '{0}dcube/getAnalyticsEngine',
    'GET_ALL_DATASOURCES': '{0}dcube/GetDataSources?summary=1',
    'GET_DATASOURCE': '{0}dcube/getDataSource/%s',
    'GET_ALL_HANDLERS': '{0}dcube/getAllHandlers?dsId=%s',
    'GET_HANDLER': '{0}dcube/getHandler/?dsId=%s&handlerId=%s',
    'GET_CRAWL_HISTORY': '{0}dcube/GetHistory/%s',
    'GET_HANDLERS': '{0}dcube/gethandler?datasourceId=%s',
    'CREATE_HANDLER': '{0}dcube/savehandler',
    'GET_DATASOURCE_SCHEMA': '{0}dcube/getDSSchema/%s',
    'UPDATE_DATASOURCE_SCHEMA': '{0}dcube/updateschema',
    'GET_JDBC_DRIVERS': '{0}dcube/GetJDBCDrivers/%s',
    'DELETE_DATASOURCE_CONTENTS': '{0}dcube/deletedata/%s?softdelete=true',
    'DELETE_DATASOURCE': '{0}dcube/deleteDataSource/%s',
    'CREATE_DATASOURCE': '{0}dcube/createDataSource',
    'DATACUBE_IMPORT_DATA': '{0}dcube/post/%s/%s',

    'GLOBAL_FILTER': '{0}GlobalFilter',
    'RESTORE_OPTIONS': '{0}Restore/GetDestinationsToRestore?clientId=0&appId=%s&flag=8',

    'UPLOAD_FULL_FILE': '{0}Client/%s/file/action/upload?uploadType=fullFile',
    'UPLOAD_CHUNKED_FILE': '{0}Client/%s/file/action/upload?uploadType=chunkedFile',

    'PLANS': '{0}V2/Plan',
    'PLAN': '{0}V2/Plan/%s',
    'DELETE_PLAN': '{0}V2/Plan/%s?confirmDelete=True',
    'ADD_USERS_TO_PLAN': '{0}V2/Plan/%s/Users',
    'GET_PLAN_TEMPLATE': '{0}V2/Plan/template?type=%s&subType=%s',
    'ELIGIBLE_PLANS': '{0}V2/Plan/Eligible?%s',

    'DOMAIN_CONTROLER': '{0}CommCell/DomainController',
    'DELETE_DOMAIN_CONTROLER': '{0}CommCell/DomainController/%s',
    'DRBACKUP': '{0}/CommServ/DRBackup',
    'ORACLE_INSTANCE_BROWSE': '{0}Instance/DBBrowse/%s',

    'METRICS': '{0}CommServ/MetricsReporting',
    'GET_METRICS': '{0}CommServ/MetricsReporting?isPrivateCloud=%s',

    'INTERNET_PROXY': '{0}/Commcell/InternetOptions/Proxy',

    'VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy',
    'ALL_VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy?hiddenpolicies=true',
    'GET_VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy/%s',
    'PROTECTED_VMS': "{0}VM?propertyLevel=AllProperties&status=1&fromTime=%s&toTime=%s",

    'USERS': '{0}User',
    'USER': '{0}User/%s?Level=50',
    'DELETE_USER': '{0}User/%s?newUserId=%s&newUserGroupId=%s',
    'OTP': '{0}User/%s/preferences/OTP',

    'ROLES': '{0}Role',
    'ROLE': '{0}Role/%s',

    'ALL_CREDENTIALS': '{0}/CommCell/Credentials?propertyLevel=30',
    'ONE_CREDENTIAL': '{0}/CommCell/Credentials/%s?propertyLevel=30',
    'CREDENTIAL':   '{0}/Commcell/Credentials',
    'DELETE_RECORD':'{0}/Commcell/Credentials/action/delete',

    'GET_SECURITY_ROLES': '{0}Security/Roles',
    'SECURITY_ASSOCIATION': '{0}Security',

    'GET_DATASTORE_BROWSE': '{0}VSBrowse/%s/%s?requestType=%s',

    'GET_DC_DATA': '{0}getDownloadCenterLookupData',
    'DC_ENTITY': '{0}saveDownloadCenterLookupEntities',
    'DC_SUB_CATEGORY': '{0}saveDownloadCenterSubCategory',
    'SEARCH_PACKAGES': '{0}searchPackages?release=11',
    'DOWNLOAD_PACKAGE': '{0}DownloadFile',
    'DOWNLOAD_VIA_STREAM': '{0}Stream/getDownloadCenterFileStream',
    'UPLOAD_PACKAGE': '{0}saveDownloadCenterPackage',
    'DELETE_PACKAGE': '{0}deleteDownloadCenterPackage?packageId=%s',

    'ORGANIZATIONS': '{0}Organization',
    'ORGANIZATION': '{0}Organization/%s',
    'UPDATE_ORGANIZATION': '{0}Organization?organizationId=%s',
    'GENERATE_AUTH_CODE': '{0}Organization/%s/Authtoken',
    'ACTIVATE_ORGANIZATION': '{0}Organization/%s/action/activate',
    'DEACTIVATE_ORGANIZATION': '{0}Organization/%s/action/deactivate',

    'STORAGE_POOL': '{0}StoragePool',
    'GET_STORAGE_POOL': '{0}StoragePool/%s',
    'ADD_STORAGE_POOL': '{0}StoragePool?Action=create',

    'GET_ALL_MONITORING_POLICIES': '{0}getLMCloudAndMonitoringPolicyList',
    'GET_ALL_ANALYTICS_SERVERS': '{0}AnalyticsServers',
    'GET_ALL_TEMPLATES': '{0}logmonitoring/search/getListOfTemplate',
    'CREATE_DELETE_EDIT_OPERATIONS': '{0}logmonitoring/policy/operations',
    'GET_MONITORING_POLICY_PROP': '{0}logmonitoring/Policy/%s',
    'RUN_MONITORING_POLICY': '{0}logmonitoring/Policy/%s/Action/Run',

    'LICENSE': '{0}CommcellRegistrationInformation',

    'DR_GROUPS': '{0}DRGroups',
    'GET_DR_GROUP': '{0}DRGroups/%s',
    'DR_GROUP_MACHINES': '{0}DRGroups/ClientList?source=1&entityType=3&entityId=%s',
    'DR_GROUP_JOB_STATS': '{0}DRGroups/JobStats?jobId=%s&drGroupId=%s&replicationId=%s&clientId=0',
    'REVERSE_REPLICATION_TASK': '{0}Replications/Monitors/streaming/Operation',
    'REPLICATION_MONITOR': '{0}Replications/Monitors/streaming?subclientId=0',

    'ADD_EXCHANGE': '{0}pseudoClient',
    'CREATE_CONFIGURATION_POLICIES': '{0}ConfigurationPolicies',
    'GET_CONFIGURATION_POLICIES': '{0}ConfigurationPolicies?policyType=email',
    'GET_CONFIGURATION_POLICY': '{0}ConfigurationPolicies/%s',
    'DELETE_CONFIGURATION_POLICY': '{0}ConfigurationPolicies/%s',
    'EMAIL_DISCOVERY': '{0}Backupset/%s/mailboxDiscover?discoveryType=%s',
    'GET_EMAIL_POLICY_ASSOCIATIONS': '{0}Subclient/%s/EmailPolicyAssociation?discoveryType=%s',
    'SET_EMAIL_POLICY_ASSOCIATIONS': '{0}/Subclient/EmailPolicyAssociation',

    'GET_EVENTS': '{0}Events',
    'GET_EVENT': '{0}Events/%s',

    'GET_ACTIVITY_CONTROL': '{0}CommCell/ActivityControl',
    'SET_ACTIVITY_CONTROL': '{0}CommCell/ActivityControl/%s/Action/%s',
    'SET_COMMCELL_PROPERTIES': '{0}Commcell/properties',

    'OPERATION_WINDOW': '{0}OperationWindow',
    'LIST_OPERATION_WINDOW': '{0}/OperationWindow/OpWindowList?clientId=%s',

    'RELEASE_LICENSE': '{0}Client/License/Release',
    'RECONFIGURE_LICENSE': '{0}Client/License/Reconfigure',
    'LIST_LICENSES': '{0}Client/%s/License',
    'GET_CLOUDAPPS_USERS': '{0}Instance/%s/CloudDiscovery?clientId=%s&discType=%s',

    'IDENTITY_APPS': '{0}ThirdParty/App',

    'GLOBAL_PARAM': '{0}/setGlobalParam',

    'SNAP_OPERATIONS': '{0}/Snaps/Operations',
    'STORAGE_ARRAYS': '{0}/StorageArrays',

    'NETWORK_TOPOLOGIES': '{0}FirewallTopology',
    'NETWORK_TOPOLOGY': '{0}FirewallTopology/%s',
    'PUSH_TOPOLOGY': '{0}FirewallTopology/%s/Push',

    'ADVANCED_JOB_DETAIL_TYPE': '{0}Job/%s/AdvancedDetails?infoType=%s',

    'CERTIFICATES': '{0}CommServ/Certificates',

    'GET_DAG_MEMBER_SERVERS': '{0}Exchange/DAG/%s/PseudoClientInfo',  # only for Exchange DAG

    'CASEDEFINITION': '{0}EDiscoveryClients/CaseDefinitions',

    'REGISTRATION': '{0}/RegFrgnCell',
    'UNREGISTRATION': '{0}/UnRegisterCommCell',
    'GET_REGISTERED_ROUTER_COMMCELLS': '{0}/CommCell/registered?getOnlyServiceCommcells=true',
    'GET_USERSPACE_SERVICE': '{0}/ServiceCommcell/UserSpace',
    'POLL_USER_SERVICE': '{0}/ServiceCommcell/IsUserPresent?userName=%s',
    'POLL_MAIL_SERVICE': '{0}/ServiceCommcell/IsUserPresent?email=%s',
    'POLL_REQUEST_ROUTER': '{0}/CommcellRedirect/RedirectListforUser?user=%s',

    'GET_ALL_LIVE_SYNC_PAIRS': '{0}Replications/Monitors/streaming?subclientId=%s',
    'GET_LIVE_SYNC_PAIR': '{0}Replications/Monitors/streaming?subclientId=%s&replicationPairId=%s'

}


def get_services(web_service):
    """Initializes the SERVICES DICT with the web service for APIs.

        Args:
            web_service     (str)   --  web service string for APIs

        Returns:
            dict    -   services dict consisting of all APIs

    """
    services_dict = SERVICES_DICT_TEMPLATE.copy()
    for service in services_dict:
        services_dict[service] = services_dict[service].format(web_service)

    return services_dict
