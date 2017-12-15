# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Service URLs for REST API operations.

SERVICES_DICT:  A python dictionary for holding all the API services endpoints.

get_services(web_service):  updates the SERVICES_DICT with the WebConsole API URL

"""

from __future__ import absolute_import
from __future__ import unicode_literals


SERVICES_DICT_TEMPLATE = {
    'LOGIN': '{0}Login',
    'LOGOUT': '{0}Logout',
    'RENEW_LOGIN_TOKEN': '{0}RenewLoginToken',
    'COMMSERV': '{0}CommServ',

    'GET_ALL_CLIENTS': '{0}Client',
    'GET_VIRTUAL_CLIENTS': '{0}Client?PseudoClientType=VSPseudo',
    'CLIENT': '{0}Client/%s',

    'GET_ALL_AGENTS': '{0}Agent?clientId=%s',
    'AGENT': '{0}Agent',
    'GET_AGENT': '{0}Agent?clientId=%s&applicationId=%s',

    'GET_ALL_BACKUPSETS': '{0}Backupset?clientId=%s',
    'BACKUPSET': '{0}Backupset/%s',
    'ADD_BACKUPSET': '{0}Backupset',

    'GET_ALL_INSTANCES': '{0}Instance?clientId=%s',
    'INSTANCE': '{0}Instance/%s',

    'GET_ALL_SUBCLIENTS': '{0}Subclient?clientId=%s',
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

    'GET_MEDIA_AGENTS': '{0}MediaAgent',
    'LIBRARY': '{0}Library',

    'STORAGE_POLICY': '{0}StoragePolicy',
    'GET_STORAGE_POLICY': '{0}StoragePolicy/%s',
    'CREATE_STORAGE_POLICY_COPY': '{0}StoragePolicy?Action=createCopy',
    'DELETE_STORAGE_POLICY_COPY': '{0}StoragePolicy?Action=deleteCopy',
    'SCHEDULE_POLICY': '{0}SchedulePolicy',
    'MEDIA_AGENT': '{0}MediaAgent/%s',

    'GET_ALL_ALERTS': '{0}AlertRule',
    'ALERT': '{0}AlertRule/%s',
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
    'SCHEDULE': '{0}Schedules/%s',
    'ENABLE_SCHEDULE': '{0}Schedules/task/Action/Enable',
    'DISABLE_SCHEDULE': '{0}Schedules/task/Action/Disable',

    'CLIENTGROUPS': '{0}ClientGroup',
    'CLIENTGROUP': '{0}ClientGroup/%s',

    'USERGROUPS': '{0}UserGroup',
    'USERGROUP': '{0}UserGroup/%s',

    'BROWSE': '{0}DoBrowse',
    'RESTORE': '{0}CreateTask',

    'GET_WORKFLOWS': '{0}Workflow',
    'DEPLOY_WORKFLOW': '{0}Workflow/%s/action/deploy',
    'EXECUTE_WORKFLOW': '{0}wapi/%s',
    'GET_WORKFLOW': '{0}Workflow/%s',

    'INSTANCE_BROWSE': '{0}Client/%s/%s/Instance/%s/Browse',

    'SQL_RESTORE_OPTIONS': '{0}SQL/RestoreOptions',

    'EXECUTE_QCOMMAND': '{0}Qcommand/qoperation execute',

    'SOFTWARESTORE_DOWNLOADITEM': '{0}DownloadFile',
    'SOFTWARESTORE_PKGINFO': '{0}SoftwareStore/getPackagePublishInfo?packageName=%s',
    'SOFTWARESTORE_GETPKGID': '{0}SoftwareStoreItem',

    'CREATE_TASK': '{0}CreateTask',
    'ADD_SYBASE_INSTANCE': '{0}Instance',

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

    'DOMAIN_CONTROLER': '{0}CommCell/DomainController',
    'DELETE_DOMAIN_CONTROLER': '{0}CommCell/DomainController/%s',

    'ORACLE_INSTANCE_BROWSE': '{0}Instance/DBBrowse/%s',

    'METRICS': '{0}CommServ/MetricsReporting',
    'GET_METRICS': '{0}CommServ/MetricsReporting?isPrivateCloud=%s',

    'INTERNET_PROXY': '{0}/Commcell/InternetOptions/Proxy',

    'VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy',
    'GET_VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy/%s',

    'USERS': '{0}User',
    'USER': '{0}User/%s',

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
