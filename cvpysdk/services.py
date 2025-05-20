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
    'CREATE_RC': '{0}V4/SoftwareCache',
    'DOWNLOAD_SOFTWARE': '{0}V4/DownloadSoftware',
    'UPGRADE_SOFTWARE': '{0}V4/UpgradeSoftware',

    'TFA': '{0}Commcell/Properties/TwoFactorAuth',
    'TFA_ENABLE': '{0}Commcell/Properties/TwoFactorAuth/Action/Enable',
    'TFA_DISABLE': '{0}Commcell/Properties/TwoFactorAuth/Action/Disable',
    'PRIVACY_ENABLE': '{0}Commcell/Properties/Privacy/Action/Enable',
    'PRIVACY_DISABLE': '{0}Commcell/Properties/Privacy/Action/Disable',
    'ACCOUNT_lOCK_SETTINGS': '{0}Commcell/Properties/AccountLockSettings',
    'ORG_TFA': '{0}Organization/%s/TwoFactorAuth',
    'ORG_TFA_ENABLE': '{0}Organization/%s/TwoFactorAuth/Action/Enable',
    'ORG_TFA_DISABLE': '{0}Organization/%s/TwoFactorAuth/Action/Disable',
    'TFA_STATUS_OF_USER': '{0}Security/TwoFactorAuth/Status?username=%s',

    'GET_ALL_CLIENTS': '{0}Client',
    'GET_VIRTUAL_CLIENTS': '{0}Client?PseudoClientType=VSPseudo',
    'GET_VIRTUALIZATION_ACCESS_NODES': '{0}VSAClientAndClientGroupList',
    'GET_FILE_SERVER_CLIENTS': '{0}/v4/FileServers',
    'CLIENTFORCEDELETE': '{0}Client/%s?forceDelete=1',
    'CLIENT': '{0}Client/%s',
    'CLIENT_LOGS': '{0}Client/%s/Logs/Read',
    'GET_ADDITIIONAL_SETTINGS': '{0}Client/%s/AdditionalSettings',
    'FILTER_CLIENTS': '{0}Client?%s',
    'GET_ALL_CLIENTS_PLUS_HIDDEN': '{0}Client?hiddenclients=true',
    'GET_ALL_PSEUDO_CLIENTS': '{0}Client?PseudoClientType',
    'CHECK_READINESS': '{0}Client/%s/CheckReadiness?network=%s&resourceCapacity=%s'
                       '&NeedXmlResp=true&includeDisabledClients=%s&CSCCNetworkCheck=%s'
                       '&applicationCheck=%s&additionalResources=%s',
    'RUN_TRUEUP': '{0}Office365/TrueUp',
    'READ_TRUEUP_RESULTS_CLIENT': '{0}Job/Office365/Results?subclientId=%s&clientId=%s&appTypeId=134&options=4',
    'READ_TRUEUP_RESULTS_USER': '{0}Job/Office365/Results?subclientId=%s&clientId=%s&options=3&appTypeId=134&userGUID=%s',
    'MONGODB_CHECK_READINESS': '{0}/clients/mongodb/status',
    'CLIENT_BROWSE_FS': '{0}/client/%s/browsefs',
    'GET_ALL_AGENTS': '{0}Agent?clientId=%s',
    'AGENT': '{0}Agent',
    'GET_AGENT': '{0}Agent?clientId=%s&applicationId=%s&propertyLevel=30',

    'GET_ALL_BACKUPSETS': '{0}Backupset?clientId=%s&propertyLevel=10',
    'BACKUPSET': '{0}Backupset/%s',
    'ADD_BACKUPSET': '{0}Backupset',

    'GET_ALL_INSTANCES': '{0}Instance?clientId=%s',
    'INSTANCE': '{0}Instance/%s',
    'APPLICATION_INSTANCE': '{0}Application/%s',
    'APPLICATION': '{0}Application',
    'INSTANCE_CREDENTIALS': '{0}v4/Hypervisor/%s/Credentials',

    'GET_ALL_SUBCLIENTS': '{0}Subclient?clientId=%s&applicationId=%s&propertyLevel=20',
    'ADD_SUBCLIENT': '{0}Subclient',
    'SUBCLIENT': '{0}Subclient/%s',
    'SUBCLIENT_BACKUP': '{0}Subclient/%s/action/backup?backupLevel=%s',
    'VM_BACKUP': '{0}v2/vsa/vm/%s/backup?backupLevel=%s',
    'PREVIEW': '{0}Subclient/Content/Preview',

    'GET_JOBS': '{0}Job?clientId=%s&jobFilter=%s',
    'JOB': '{0}Job/%s',
    'JOB_DETAILS': '{0}JobDetails',
    'JOB_TASK_DETAILS': '{0}Job/%s/TaskDetails',
    'SUSPEND_JOB': '{0}Job/%s/action/pause',
    'RESUME_JOB': '{0}Job/%s/action/resume',
    'KILL_JOB': '{0}Job/%s/action/kill',
    'RESUBMIT_JOB': '{0}Job/%s/action/Resubmit',
    'ALL_JOBS': '{0}Jobs',
    'JOB_EVENTS': '{0}Events?jobId=%s',
    'JOB_MANAGEMENT_SETTINGS': '{0}CommServ/JobManagementSetting',

    'ENABLE_SHARED_LAPTOP': '{0}Commcell/Properties/SharedLaptopUsage/Action/Enable',
    'DISABLE_SHARED_LAPTOP': '{0}Commcell/Properties/SharedLaptopUsage/Action/Disable',

    'GET_MEDIA_AGENTS': '{0}V2/MediaAgents',
    'LIBRARY': '{0}Library',
    'GET_LIBRARY_PROPERTIES': '{0}Library/%s',
    'DETECT_TAPE_LIBRARY': '{0}Library?Action=detect',
    'CONFIGURE_TAPE_LIBRARY': '{0}Library?Action=configureTape',
    'EDIT_CLOUD_CONTROLLER': '{0}V4/Storage/Cloud/0/Bucket/%s/AccessPath/%s',
    'GET_AGP_STORAGE': '{0}V4/Storage/Cloud?additionalProperties=true&storageSubType=4',

    'GET_MOVE_MOUNTPATH_DETAILS': '{0}MountPath/%s/Move',
    'MOVE_MOUNTPATH': '{0}MountPath/Move',

    'LOCK_MM_CONFIGURATION': '{0}LockMMConfiguration',

    'STORAGE_POLICY': '{0}StoragePolicy',
    'GET_STORAGE_POLICY': '{0}StoragePolicy/%s',
    'DELETE_STORAGE_POLICY': '{0}V2/StoragePolicy',
    'UPDATE_STORAGE_POLCY': '{0}V2/StoragePolicy/%s',
    'GET_STORAGE_POLICY_ADVANCED': '{0}v2/StoragePolicy/%s?propertyLevel=10',
    'CREATE_STORAGE_POLICY_COPY': '{0}StoragePolicy?Action=createCopy',
    'DELETE_STORAGE_POLICY_COPY': '{0}StoragePolicy?Action=deleteCopy',
    'SCHEDULE_POLICY': '{0}SchedulePolicy',
    'CREATE_UPDATE_SCHEDULE_POLICY': '{0}Task',
    'GET_SCHEDULE_POLICY': '{0}SchedulePolicy/%s',
    'MEDIA_AGENT': '{0}MediaAgent/%s',
    'CLOUD_MEDIA_AGENT': '{0}MediaAgent/%s/CloudVMPowerManagement',
    'STORAGE_POLICY_COPY': '{0}V2/StoragePolicy/%s/Copy/%s',
    'DISABLE_STORAGE_POLICY_COMPLIANCE_LOCK': '{0}V4/StoragePolicy/%s/Copy/%s/ComplianceLock/Disable',
    'STORAGE_POLICY_INFRASTRUCTUREPOOL': '{0}/StoragePolicy/Infrastructurepool?planId=%s',
    'RECOVERY_ENABLERS': '{0}MediaAgent/RecoveryEnabler?osType=CLIENT_PLATFORM_OSTYPE_UNIX ',
    'GET_ALL_ALERTS': '{0}AlertRule',
    'ALERT': '{0}AlertRule/%s',
    'ALERT_TEST': '{0}AlertRule/%s/Test',
    'CREATE_BLR_PAIR': '{0}Replications/Groups',
    'DELETE_BLR_PAIR': '{0}Replications/Monitors/continuous/%s',
    'GET_BLR_PAIRS': '{0}Replications/Monitors/continuous',
    'GET_BLR_PAIR': '{0}Replications/Monitors/continuous?replicationPairId=%s',
    'GET_BLR_PAIR_STATS': '{0}Replications/Statistics/%s',
    'GRANULAR_BLR_POINTS': '{0}Replications/Monitors/continuous/VmScale?destProxyClientId=%s&subclientId=%s&vmUuid=%s',
    'BLR_BOOT_DETAILS': '{0}/Replications/Monitors/continuous/Boot?replicationPairId=%s&bootType=%s&latest=true',
    'BROWSE_MOUNT_POINTS': '{0}/Client/%s/Action/BrowseMountPoints',

    'GET_VM_BROWSE': '{0}/VMBrowse?inventoryPath=%%5CFOLDER%%3AApplications%%3AApplications&PseudoClientId=%s',

    'GET_K8S_NS_BROWSE': '{0}/VMBrowse?inventoryPath=%%5CFOLDER%%3AApplications%%3AApplications&PseudoClientId=%s&vendor=KUBERNETES',
    'GET_K8S_VOLUME_BROWSE': '{0}/VMBrowse?inventoryPath=%%5CFOLDER%%3AVolumes%%3AVolumes%%5CFOLDER%%3A%s%%3A%s&PseudoClientId=%s&vendor=KUBERNETES',
    'GET_K8S_APP_BROWSE': '{0}/VMBrowse?inventoryPath=%%5CFOLDER%%3AApplications%%3AApplications%%5CFOLDER%%3A%s%%3A%s&PseudoClientId=%s&vendor=KUBERNETES',
    'GET_K8S_LABEL_BROWSE': '{0}/VMBrowse?inventoryPath=%%5CFOLDER%%3ALabels%%3ALabels%%5CFOLDER%%3A%s%%3A%s&PseudoClientId=%s&vendor=KUBERNETES',

    'MODIFY_ALERT': '{0}AlertRule/%s/Action/Modify',
    'GET_ALL_CONSOLE_ALERTS': '{0}Alert?pageNo=%s&pageCount=%s',
    'GET_CONSOLE_ALERT': '{0}Alert/%s',
    'ENABLE_ALERT_NOTIFICATION': '{0}AlertRule/%s/notificationType/%s/Action/Enable',
    'DISABLE_ALERT_NOTIFICATION': '{0}AlertRule/%s/notificationType/%s/Action/Disable',
    'ENABLE_ALERT': '{0}AlertRule/%s/Action/Enable',
    'DISABLE_ALERT': '{0}AlertRule/%s/Action/Disable',
    'EMAIL_SERVER': '{0}EmailServer',

    'INVENTORY_SCHEDULES': '{0}Schedules?seaDataSourceId=%s&appType=132',
    'CLIENT_SCHEDULES': '{0}Schedules?clientId=%s',
    'AGENT_SCHEDULES': '{0}Schedules?clientId=%s&apptypeId=%s',
    'BACKUPSET_SCHEDULES': '{0}Schedules?clientId=%s&apptypeId=%s&backupsetId=%s',
    'INSTANCE_SCHEDULES':  '{0}Schedules?clientId=%s&apptypeId=%s&instanceId=%s',
    'SUBCLIENT_SCHEDULES': ('{0}Schedules?clientId=%s&apptypeId=%s&'
                            'backupsetId=%s&subclientId=%s'),
    'WORKFLOW_SCHEDULES': '{0}Schedules?workflowId=%s',
    'REPORT_SCHEDULES': '{0}/ScheduleReports',
    'OPTYPE_SCHEDULES': '{0}/Schedules?operationType=%s',
    'COMMCELL_SCHEDULES': '{0}/Schedules',
    'SCHEDULE': '{0}Schedules/%s',
    'ENABLE_SCHEDULE': '{0}Schedules/task/Action/Enable',
    'DISABLE_SCHEDULE': '{0}Schedules/task/Action/Disable',

    'LIVE_SYNC': '{0}Task',
    'LIVE_SYNC_DETAILS': '{0}/Task/%s/Details',

    'CLIENTGROUPS': '{0}ClientGroup',
    'CLIENTGROUP': '{0}ClientGroup/%s',
    'SERVERGROUPS_V4': '{0}V4/ServerGroup',

    'USERGROUPS': '{0}UserGroup?includeSystemCreated=%s',
    'USERGROUP': '{0}UserGroup/%s',
    'USERGROUP_V4': '{0}V4/UserGroup/%s',
    'DELETE_USERGROUP': '{0}UserGroup/%s?newUserId=%s&newUserGroupId=%s',
    'COMPANY_USERGROUP': '{0}UserGroup?parentProvider/providerId=%s',

    'BROWSE': '{0}DoBrowse',
    'RESTORE': '{0}CreateTask',
    'DELETE': '{0}DeleteDocuments',
    'DATABASES': '{0}databases',
    'DB_INSTANCES': '{0}databases/instances',
    'DB_CLONES': '{0}databases/clones',
    'SQL_CLONES': '{0}sql/clones',
    'SQL_DATABASE': '{0}sql/databases?instance=%s&databaseName=%s',
    'SQL_DATABASES': '{0}sql/databases?databaseName=%s',
    'SQL_DATABASE_LIST': '{0}sql/databases?instance=%s',
    'SQL_DATABASE_DETAILS': '{0}sql/instance/%s/database/%s',
    'SQL_AG_GROUPS': '{0}v2/sql/availabilityGroups/client/%s/instance/%s',
    'SQL_AG_GROUP_REPLICAS': '{0}v2/sql/availabilityGroupReplicas/client/%s/instance/%s/availabilityGroup/%s',

    'GET_WORKFLOWS': '{0}Workflow',
    'DEPLOY_WORKFLOW': '{0}Workflow/%s/action/deploy',
    'EXECUTE_WORKFLOW_API': '{0}Workflow/%s/action/execute',
    'EXECUTE_WORKFLOW': '{0}wapi/%s',
    'EXECUTE_INTERACTIVE_WORKFLOW': '{0}workflowrequest',
    'GET_WORKFLOW': '{0}Workflow/%s',
    'GET_WORKFLOW_DEFINITION': '{0}Workflow/%s/definition',
    'GET_INTERACTIONS': '{0}WorkflowInteractions',
    'GET_INTERACTION': '{0}Workflow/Interaction/%s',
    'EDIT_WORKFLOW_CONFIG': '{0}/cr/apps/configform/%s',
    'APPROVE_WORKFLOW': '{0}workflow_editor/configuration/%s/approve',

    'INSTANCE_BROWSE': '{0}Client/%s/%s/Instance/%s/Browse',
    'CLOUD_DATABASE_BROWSE': '{0}BrowseRDSBackups',

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

    'DO_COMPLIANCE_SEARCH': '{0}doWebSearch',
    'GET_EXPORT_SETS': '{0}GetContainers',
    'GET_EXPORTS': '{0}getContainerItems',
    'ADD_EXPORT_SET': '{0}PerformContainerOperation',
    'DELETE_EXPORT_SET': '{0}Containers/Action/Delete',
    'EXPORT_ITEM_TO_SET': '{0}Download',
    'DOWNLOAD_EXPORT_ITEMS': '{0}DownloadFile',
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
    'PRUNE_DATASOURCE': '{0}indexing/uns/deletecollection',
    'CREATE_DATASOURCE': '{0}dcube/createDataSource',
    'DATACUBE_IMPORT_DATA': '{0}dcube/post/%s/%s',
    'START_JOB_DATASOURCE': '{0}dcube/startjob/%s',
    'GET_STATUS_DATASOURCE': '{0}dcube/GetStatus/%s',
    'EXECUTE_HANDLER': '{0}dcube/handler/%s/%s?%s',
    'DELETE_HANDLER': '{0}dcube/deletehandler/%s',
    'SHARE_HANDLER': '{0}dcube/share/handler',
    'SHARE_DATASOURCE': '{0}dcube/share/datasource',
    'GET_CONTENT_ANALYZER_CLOUD': '{0}getContentAnalyzerClient',
    'ACTIVATE_ENTITIES': '{0}dcube/entity',
    'ACTIVATE_ENTITY': '{0}dcube/entity/%s',
    'ACTIVATE_ENTITY_CONTAINER': '{0}EntityExtractionRules?getDisabled=true',
    'GET_TAGS': '{0}EDiscovery/Tags',
    'GET_ENTITY_TAGS': '{0}V4/Tags/AssociatedEntities',
    'CREATE_ENTITY_TAGS': '{0}EDiscovery/Tags',
    'DELETE_ENTITY_TAGS': '{0}V4/EntityTags/%s',
    'ADD_CONTAINER': '{0}PerformContainerOperation',
    'DELETE_CONTAINER': '{0}Containers/Action/Delete',
    'CA_UPLOAD_FILE': '{0}ContentAnalyzer/%s/action/uploadFile',
    'GET_CLASSIFIERS': '{0}dcube/classifiers?getDisabled=True',
    'START_TRAINING': '{0}ContentAnalyzer/%s/%s/ml/action/train',
    'CANCEL_TRAINING': '{0}ContentAnalyzer/%s/%s/training/cancel',

    'V4_ACTIVATE_DS_PERMISSION': '{0}V4/Activate/SEA_DATASOURCE_ENTITY/%s/Permissions',
    'V4_INVENTORY_CRAWL': '{0}V4/InventoryManager/Inventory/%s/Crawl',
    'EDISCOVERY_INVENTORIES': '{0}V4/InventoryManager/Inventory',
    'EDISCOVERY_INVENTORY': '{0}V4/InventoryManager/Inventory/%s',
    'EDISCOVERY_ASSETS': '{0}V4/InventoryManager/Inventory/%s/Assets',
    'EDISCOVERY_ASSET': '{0}V4/InventoryManager/Inventory/%s/Assets/%s',
    'EDISCOVERY_ASSET_JOBS': '{0}V4/InventoryManager/Inventory/%s/Assets/%s/jobs',
    'EDISCOVERY_CRAWL': '{0}EDiscoveryClients/Clients/%s/Jobs?datasourceId=%s&type=%s&operation=%s',
    'EDISCOVERY_JOBS_HISTORY': '{0}EDiscoveryClients/Clients/%s/Jobs/History?type=%s&datasourceId=%s',
    'EDISCOVERY_JOB_STATUS': '{0}EDiscoveryClients/Clients/%s/Jobs/Status?type=%s&datasourceId=%s',
    'EDISCOVERY_GET_DEFAULT_HANDLER': '{0}dcube/getdefaulthandler/%s',
    'EDISCOVERY_V2_GET_CLIENTS': '{0}V2/EDiscoveryClients/Clients?datasourceType=%s&clientGroup=%s&limit=%s&offset=%s&sortBy=%s&sortDir=%s',
    'EDISCOVERY_V2_GET_CLIENT_DETAILS': '{0}V2/EDiscoveryClients/Clients/%s?includeDocCount=%s&limit=%s&offset=%s&sortBy=%s&sortDir=%s&datasourceType=%s',
    'EDISCOVERY_V2_GET_CLIENT_GROUP_DETAILS': '{0}V2/EDiscoveryClients/ClientGroups/%s?includeDocCount=%s',
    'EDISCOVERY_SECURITY_ASSOCIATION': '{0}EDiscoveryClients/Security?appType=%s',
    'EDISCOVERY_DATA_SOURCES': '{0}V2/EDiscoveryClients/Datasources?datasourceId=%s&type=%s',
    'EDISCOVERY_DATA_SOURCE_DELETE': '{0}EDiscoveryClients/Datasources?datasourceId=%s&clientId=%s',
    'EDISCOVERY_DYNAMIC_FEDERATED': '{0}dcube/dynamicfederated/%s/%s/default',
    'EDISCOVERY_EXPORT': '{0}dcube/export/%s',
    'EDISCOVERY_EXPORT_STATUS': '{0}dcube/export/%s/status?token=%s',
    'EDISCOVERY_CREATE_DATA_SOURCE': '{0}EDiscoveryClients/Datasources',
    'EDISCOVERY_REVIEW_ACTIONS_WITH_REQUEST': '{0}EDiscoveryClients/Datasources/Actions/Requests',
    'EDISCOVERY_REVIEW_ACTIONS': '{0}V2/EDiscoveryClients/Datasources/Actions',
    'EDISCOVERY_CLIENTS': '{0}EDiscoveryClients?eDiscoverySubtype=%s',
    'EDISCOVERY_CLIENT_DETAILS': '{0}EDiscoveryClients/%s',
    'EDISCOVERY_DATA_SOURCE_STATS': '{0}EDiscoveryClients/Datasources?id=%s&type=%s&start=0&count=1000',
    'EDISCOVERY_CREATE_CLIENT': '{0}EDiscoveryClients/Clients',
    'EDISCOVERY_DELETE_CLIENT': '{0}EDiscoveryClients/Clients/%s',
    'EDISCOVERY_REQUESTS': '{0}V4/RequestManager/Request',
    'EDISCOVERY_REQUEST_DETAILS': '{0}V4/RequestManager/Request/%s',
    'EDISCOVERY_REQUEST_CONFIGURE': '{0}V4/RequestManager/Request/%s/Configure',
    'EDISCOVERY_REQUEST_PROJECTS': '{0}V4/RequestManager/Request/%s/Projects',
    'EDISCOVERY_REQUEST_FEDERATED': '{0}dcube/federated/%s/%s',
    'EDISCOVERY_REQUEST_DOCUMENT_MARKER': '{0}EDiscoveryClients/Tasks/%s/Documents',
    'EDISCOVERY_CONFIGURE_TASK': '{0}EDiscoveryClient/ConfigureTask',
    'EDICOVERY_TASK_WORKFLOW': '{0}EDiscoveryClients/Tasks/%s/Workflows',
    'GET_RESOURCE_POOLS': '{0}V4/ResourcePool',
    'GET_RESOURCE_POOL_DETAILS': '{0}ResourcePool/%s',
    'DELETE_RESOURCE_POOL': '{0}ResourcePool/%s',
    'CREATE_RESOURCE_POOL': '{0}ResourcePool',

    'GLOBAL_FILTER': '{0}GlobalFilter',
    'RESTORE_OPTIONS': '{0}Restore/GetDestinationsToRestore?clientId=0&appId=%s&flag=8',

    'UPLOAD_FULL_FILE': '{0}Client/%s/file/action/upload?uploadType=fullFile',
    'UPLOAD_CHUNKED_FILE': '{0}Client/%s/file/action/upload?uploadType=chunkedFile',
    'PLANS': '{0}V2/Plan',
    'PLAN': '{0}V2/Plan/%s',
    'PLAN_SUMMARY': '{0}v4/Plan/Summary?%s',
    'DELETE_PLAN': '{0}V2/Plan/%s?confirmDelete=True',
    'ADD_USERS_TO_PLAN': '{0}V2/Plan/%s/Users',
    'GET_PLAN_TEMPLATE': '{0}V2/Plan/template?type=%s&subType=%s',
    'ELIGIBLE_PLANS': '{0}V2/Plan/Eligible?%s',
    'ASSOCIATED_ENTITIES': '{0}V2/Plan/%s/AssociatedEntities',
    'GET_PLANS': '{0}V2/Plan?type=%s&subType=%s',
    'APPLICABLE_SOLNS_ENABLE': '{0}V4/ServerPlan/%s/ApplicableSolutions/Restrict/Enable',
    'APPLICABLE_SOLNS_DISABLE': '{0}V4/ServerPlan/%s/ApplicableSolutions/Restrict/Disable',
    'PLAN_SUPPORTED_SOLUTIONS': '{0}V4/Solutions?filter=PLAN_SUPPORTED_SOLUTIONS',
    'V4_SERVER_PLAN': '{0}V4/ServerPlan/%s',
    'V4_SERVER_PLANS': '{0}V4/ServerPlan',
    'V4_GLOBAL_SERVER_PLANS': '{0}/V4/Global/ServerPlan',
    'V4_SERVER_PLAN_BACKUP_DESTINATION': '{0}V4/ServerPlan/%s/BackupDestination',
    'V4_SERVER_PLAN_COPY': '{0}V4/ServerPlan/%s/BackupDestination/%s',
    'V4_DC_PLANS': '{0}V4/DCPlan',
    'V4_DC_PLAN': '{0}V4/DCPlan/%s',
    'V5_SERVER_PLAN_COPY': '{0}V5/ServerPlan/%s/BackupDestination/%s',
    'SERVER_PLAN_REGIONS': '{0}V4/ServerPlan/%s/storageRegion/%s?isRegionIdList=true',
    'SERVER_PLAN_RPO': '{0}V4/ServerPlan/%s/RPO',

    'DOMAIN_CONTROLER': '{0}CommCell/DomainController',
    'DELETE_DOMAIN_CONTROLER': '{0}CommCell/DomainController/%s',
    'DOMAIN_PROPERTIES': '{0}CommCell/DomainController?domainId=%s',

    'DRBACKUP': '{0}/CommServ/DRBackup',
    'DRBACKUP_REGIONS': '{0}/V4/DRBackup/Regions',
    'DISASTER_RECOVERY_PROPERTIES': '{0}/Commcell/DRBackup/Properties',
    'DISASTER_RECOVERY_OPTIONS': '{0}/Commcell/DRBackup/Options',
    'CVDRBACKUP_STATUS': '{0}/cvdrbackup/status?commcellid=%s',
    'CVDRBACKUP_INFO': '{0}/cvdrbackup/info',
    'CVDRBACKUP_DOWNLOAD': '{0}/cvdrbackup/download',
    'CVDRBACKUP_REQUEST': '{0}/cvdrbackup/requests',
    'CVDRBACKUP_REQUEST_HISTORY': '{0}/cr/reportsplusengine/datasets/%s/data/?parameter.duration=%s',

    'ORACLE_INSTANCE_BROWSE': '{0}Instance/DBBrowse/%s',

    'METRICS': '{0}CommServ/MetricsReporting',
    'GET_METRICS': '{0}CommServ/MetricsReporting?isPrivateCloud=%s',
    'LOCAL_METRICS': '{0}CommServ/MetricsReporting?isLocalMetrics=%s',

    'INTERNET_PROXY': '{0}/Commcell/InternetOptions/Proxy',

    'PASSWORD_ENCRYPTION_CONFIG': '{0}/Commcell/PasswordEncryptionConfig',

    'VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy',
    'ALL_VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy?showResourceGroupPolicy=true&deep=false&hiddenpolicies=true',
    'GET_VM_ALLOCATION_POLICY': '{0}VMAllocationPolicy/%s',
    'PROTECTED_VMS': "{0}VM?propertyLevel=AllProperties&status=1&fromTime=%s&toTime=%s&Limit=%s",
    'CONTINUOUS_REPLICATION_MONITOR': "{0}Replications/Monitors/continuous",
    'USERS': '{0}User',
    'V4_USERS': '{0}v4/user?additionalProperties=true',
    'USER': '{0}User/%s?Level=50',
    'DELETE_USER': '{0}User/%s?newUserId=%s&newUserGroupId=%s',
    'OTP': '{0}User/%s/preferences/OTP',

    'UNLOCK': '{0}User/Unlock',

    'ROLES': '{0}Role',
    'ROLE': '{0}Role/%s',

    'ALL_CREDENTIALS': '{0}/CommCell/Credentials?propertyLevel=30',
    'ONE_CREDENTIAL': '{0}/CommCell/Credentials/%s?propertyLevel=30',
    'CREDENTIAL':   '{0}/Commcell/Credentials',
    'DELETE_RECORD': '{0}/Commcell/Credentials/action/delete',

    'ADD_CREDENTIALS': '{0}V4/Credential',

    'GET_SECURITY_ROLES': '{0}Security/Roles',
    'SECURITY_ASSOCIATION': '{0}Security',
    'ENTITY_SECURITY_ASSOCIATION': '{0}Security/%s/%s',
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
    'ORGANIZATION_ASSOCIATION': '{0}company/%s/company-association',
    'ENABLE_PRIVACY_COMPANY_DATA': '{0}V2/Organization/%s/Privacy/Action/Lock',
    'DISABLE_PRIVACY_COMPANY_DATA': '{0}V2/Organization/%s/Privacy/Action/Unlock',
    'ORGANIZATION_THEME': '{0}V2/Organization/%s/Customization',
    'GET_ORGANIZATION_THEME': '{0}Organization/%s/Customization',
    'EXTEND_ORGANIZATION': '{0}ThirdParty/App/Company/Extend',
    'ORGANIZATION_TAGS': '{0}Tags',
    'GET_ORGANIZATION_TAGS': '{0}Tags/PROVIDER_ENTITY/%s',
    'COMPANY_PASSKEY': '{0}Company/%s/Passkey',
    'COMPANY_AUTH_RESTORE': '{0}Company/%s/AuthRestore',
    'EDIT_COMPANY_DETAILS': '{0}v4/company/%s',
    'CHECK_ELIGIBILITY_MIGRATION': '{0}Company/%s/migration-entities',
    'COMPANY_ENTITIES': '{0}Company/%s/AssociatedEntities',
    'MIGRATE_CLIENTS': '{0}Company/%s/company-association',
    'COMPANY_OPERATORS': '{0}V4/Company/Operator',
    "ORGANIZATION_ADDITIONAL_SETTINGS": '{0}v4/workload/AdditionalSettings',

    'STORAGE_POOL': '{0}StoragePool',
    'GET_STORAGE_POOL': '{0}StoragePool/%s',
    'ADD_STORAGE_POOL': '{0}StoragePool?Action=create',
    'DELETE_STORAGE_POOL': '{0}StoragePool/%s',
    'EDIT_STORAGE_POOL': '{0}StoragePool?Action=edit',
    'REPLACE_DISK_STORAGE_POOL': '{0}StoragePool?action=diskOperation',
    'GET_METALLIC_STORAGE_DETAILS': '{0}metallic/storage',

    'KEY_MANAGEMENT_SERVER_ADD_GET': '{0}CommCell/KeyManagementServers',
    'KEY_MANAGEMENT_SERVER_DELETE': '{0}CommCell/KeyManagementServers/%s',

    'GET_ALL_MONITORING_POLICIES': '{0}logmonitoring/monitoringpolicy',
    'GET_ALL_ANALYTICS_SERVERS': '{0}AnalyticsServers',
    'GET_ALL_TEMPLATES': '{0}logmonitoring/search/getListOfTemplate',
    'CREATE_DELETE_EDIT_OPERATIONS': '{0}logmonitoring/policy/operations',
    'GET_MONITORING_POLICY_PROP': '{0}logmonitoring/Policy/%s',
    'RUN_MONITORING_POLICY': '{0}logmonitoring/Policy/%s/Action/Run',

    'LICENSE': '{0}CommcellRegistrationInformation',

    'REPLICATION_GROUPS': '{0}ReplicationGroups',
    'DELETE_REPLICATION_GROUPS': '{0}ReplicationGroups/Action/Delete',
    'REPLICATION_GROUP_DETAILS': '{0}Vsa/ReplicationGroup/%s',

    'DR_GROUPS': '{0}DRGroups',
    'GET_DR_GROUP': '{0}DRGroups/%s',
    'DR_GROUP_MACHINES': '{0}DRGroups/ClientList?source=1&entityType=3&entityId=%s',
    'DR_GROUP_JOB_STATS': '{0}DRGroups/JobStats?jobId=%s&drGroupId=%s&replicationId=%s&clientId=0',
    'DR_JOB_STATS': '{0}DRGroups/JobStats?jobId=%s',

    'FAILOVER_GROUPS': '{0}FailoverGroups',
    'GET_FAILOVER_GROUP': '{0}FailoverGroups/%s',
    'FAILOVER_GROUP_MACHINES': '{0}FailoverGroups/ClientList?source=1&entityType=3&entityId=%s',
    'FAILOVER_GROUP_JOB_STATS': '{0}DR/JobStats?jobId=%s&failoverGroupId=%s&replicationId=%s&clientId=0',
    'DRORCHESTRATION_JOB_STATS': '{0}DR/JobStats?jobId=%s',

    'REVERSE_REPLICATION_TASK': '{0}Replications/Monitors/streaming/Operation',
    'REPLICATION_MONITOR': '{0}Replications/Monitors/streaming?subclientId=0',
    'RPSTORE': '{0}Replications/RPStore',

    'CREATE_PSEUDO_CLIENT': '{0}pseudoClient',
    'CREATE_YUGABYTE_CLIENT': '{0}Client/YugabyteDB',
    'CREATE_COUCHBASE_CLIENT': '{0}Client/Couchbase',
    'CREATE_NAS_CLIENT': '{0}NASClient',
    'GET_OFFICE_365_ENTITIES': '{0}Office365/entities',
    'GET_DYNAMICS_365_CLIENTS': '{0}Office365/entities?agentType=5',
    'GET_SALESFORCE_CLIENTS': '{0}Salesforce/Organization',
    'OFFICE365_OVERVIEW_STATS': '{0}Office365/overview/%s?mode=0',
    'OFFICE365_POPULATE_INDEX_STATS': '{0}Office365/PopulateIdxStats',
    'CLOUD_DISCOVERY': '{0}Instance/%s/CloudDiscovery?clientId=%s&appType=%s',
    'GOOGLE_DISCOVERY_OVERVIEW': '{0}Office365/overview/%s?mode=2',
    'SET_USER_POLICY_ASSOCIATION': '{0}Office365/CloudApps/SetUserPolicyAssociation',
    'CUSTOM_CATEGORY': '{0}Office365/SubClient/%s/CustomCategory',
    'CUSTOM_CATEGORIES': '{0}Office365/SubClient/%s/CustomCategories',
    'INSTANCE_PROPERTIES': '{0}instance/%s',
    'USER_POLICY_ASSOCIATION': '{0}Office365/CloudApps/UserPolicyAssociation',
    'UPDATE_USER_POLICY_ASSOCIATION': '{0}Office365/CloudApps/UpdateUserPolicyAssociation',
    'GDRIVE_UPDATE_USERS': '{0}GoogleWorkspace/GDrive/UpdateUsers',
    'GMAIL_UPDATE_USERS': '{0}GoogleWorkspace/GMail/UpdateUsers',
    'GDRIVE_GET_USERS': '{0}GoogleWorkspace/GDrive/GetUsers',
    'GMAIL_GET_USERS': '{0}GoogleWorkspace/GMail/GetUsers',
    'OFFICE365_MOVE_JOB_RESULT_DIRECTORY': '{0}Office365/MoveJobResultsDirectory',
    'OFFICE365_PROCESS_INDEX_RETENTION_RULES': '{0}Office365/ProcessIdxRetentionRules',
    'OFFICE365_POPULATE_INDEX_STATS': '{0}Office365/PopulateIdxStats',
    'OFFICE365_OVERVIEW_STATS': '{0}Office365/overview/%s?mode=0',
    'ADD_EXCHANGE': '{0}pseudoClient',
    'CREATE_CONFIGURATION_POLICIES': '{0}ConfigurationPolicies',
    'GET_CONFIGURATION_POLICIES': '{0}ConfigurationPolicies?policyType=email',
    'GET_CONFIGURATION_POLICIES_FS': '{0}ConfigurationPolicies?policyType=filesytem',
    'GET_CONFIGURATION_POLICY': '{0}ConfigurationPolicies/%s',
    'DELETE_CONFIGURATION_POLICY': '{0}ConfigurationPolicies/%s',
    'EMAIL_DISCOVERY': '{0}Backupset/%s/mailboxDiscover?discoveryType=%s&pageSize=-1',
    'EMAIL_DISCOVERY_WITHOUT_REFRESH': '{0}Backupset/%s/mailboxDiscover?discoveryType=%s&refreshMailboxDb=false&pageSize=-1',
    'GET_EMAIL_POLICY_ASSOCIATIONS': '{0}Subclient/%s/EmailPolicyAssociation?discoveryType=%s',
    'SET_EMAIL_POLICY_ASSOCIATIONS': '{0}/Subclient/EmailPolicyAssociation',
    'DELETE_DOCUMENTS': '{0}/DeleteDocuments',

    'CREATE_NUTANIX_CLIENT': '{0}Client/Nutanix',

    'GET_EVENTS': '{0}Events',
    'GET_EVENT': '{0}Events/%s',

    'GET_ACTIVITY_CONTROL': '{0}V4/CommCell/ActivityControl',
    'SET_ACTIVITY_CONTROL': '{0}CommCell/ActivityControl/%s/Action/%s',
    'SET_COMMCELL_PROPERTIES': '{0}Commcell/properties',

    'OPERATION_WINDOW': '{0}OperationWindow',
    'LIST_OPERATION_WINDOW': '{0}/OperationWindow/OpWindowList?clientId=%s',

    'RELEASE_LICENSE': '{0}Client/License/Release',
    'RECONFIGURE_LICENSE': '{0}Client/License/Reconfigure',
    'LIST_LICENSES': '{0}Client/%s/License',
    'APPLY_LICENSE': '{0}License',
    'CAPACITY_LICENSE': '{0}cr/reportsplusengine/datasets/d7faef75-cf66-40a2-98ce-a2d0cc2a144b:feabb5ca-b6b7-4572-b0cb-39352c7e1b67/data',
    'OI_LICENSE': '{0}cr/reportsplusengine/datasets/d7faef75-cf66-40a2-98ce-a2d0cc2a144b:cd38c52a-e099-4252-d36f-3e2c54540f6f/data',
    'VIRTUALIZATION_LICENSE': '{0}cr/reportsplusengine/datasets/d7faef75-cf66-40a2-98ce-a2d0cc2a144b:0aac5b36-10a4-4970-838a-c41fa2365583/data',
    'USER_LICENSE': '{0}cr/reportsplusengine/datasets/d7faef75-cf66-40a2-98ce-a2d0cc2a144b:44cd7de8-ecb2-4ec8-8b2b-162491172eef/data',
    'ACTIVATE_LICENSE': '{0}cr/reportsplusengine/datasets/d7faef75-cf66-40a2-98ce-a2d0cc2a144b:f7c6b473-f99d-44b4-ff5e-466b55656500/data',
    'METALLIC_LICENSE': '{0}cr/reportsplusengine/datasets/d7faef75-cf66-40a2-98ce-a2d0cc2a144b:cc2e77ec-9315-4446-cd7e-44ef80a8860e/data',
    'OTHER_LICENSE': '{0}cr/reportsplusengine/datasets/d7faef75-cf66-40a2-98ce-a2d0cc2a144b:2654b01f-9bb0-481e-b273-4b4fddc585b1/data',
    'GET_CLOUDAPPS_USERS': '{0}Instance/%s/CloudDiscovery?clientId=%s&eDiscoverType=%s',
    'GET_CLOUDAPPS_ONEDRIVE_USERS': '{0}Instance/%s/CloudDiscovery?clientId=%s&eDiscoverType=%s&subclientId=%s',
    'ENABLE_CLIENT_PRIVACY': '{0}/V3/Client/%s/Lock',
    'DISABLE_CLIENT_PRIVACY': '{0}/V3/Client/%s/Unlock',

    'IDENTITY_APPS': '{0}ThirdParty/App',

    'SET_GLOBAL_PARAM': '{0}/setGlobalParam',
    'GET_GLOBAL_PARAM': '{0}/CommServ/GlobalParams',

    'SNAP_OPERATIONS': '{0}/Snaps/Operations',
    'STORAGE_ARRAYS': '{0}/StorageArrays',

    'GET_NETWORK_SUMMARY': '{0}/FirewallSummary/%s',
    'NETWORK_TOPOLOGIES': '{0}FirewallTopology',
    'NETWORK_TOPOLOGY': '{0}FirewallTopology/%s',
    'PUSH_TOPOLOGY': '{0}FirewallTopology/%s/Push',

    'ADVANCED_JOB_DETAIL_TYPE': '{0}Job/%s/AdvancedDetails?infoType=%s',

    'CERTIFICATES': '{0}CommServ/Certificates',

    # only for Exchange DAG
    'GET_DAG_MEMBER_SERVERS': '{0}Exchange/DAG/%s/PseudoClientInfo',
    'GET_RECOVERY_POINTS': '{0}Exchange/DAG/%s/RecoveryPoints?instanceId=%s&backupSetId=%s&subClientId=%s&appId=%s',

    'CASEDEFINITION': '{0}EDiscoveryClients/CaseDefinitions',

    'REGISTRATION': '{0}/RegFrgnCell',
    'UNREGISTRATION': '{0}/UnRegisterCommCell',
    'SERVICE_REGISTER': '{0}/ServiceCommcells/Register',
    'SERVICE_PROPS': '{0}/ServiceCommcell/Properties',
    'GET_REGISTERED_COMMCELLS': '{0}/CommCell/registered',
    'GET_REGISTERED_ROUTER_COMMCELLS': '{0}/ServiceCommcells',
    'GET_USERSPACE_SERVICE': '{0}/ServiceCommcell/UserSpace',
    'POLL_USER_SERVICE': '{0}/ServiceCommcell/IsUserPresent?userName=%s',
    'POLL_MAIL_SERVICE': '{0}/ServiceCommcell/IsUserPresent?email=%s',
    'POLL_REQUEST_ROUTER': '{0}/CommcellRedirect/RedirectListforUser?user=%s&getDistinctSAMLAppType=true',
    'MULTI_COMMCELL_SWITCHER': '{0}/CommcellRedirect/MultiCommcell',
    'MULTI_COMMCELL_DROP_DOWN': '{0}/MultiCommcellsForUser',
    'SERVICE_COMMCELL_ASSOC': '{0}/Security/MultiCommcell',
    'SYNC_SERVICE_COMMCELL': '{0}/RouterCommcell/SyncUserSpace?commcellGUID=%s',

    'DASHBOARD_ENVIRONMENT_TILE': '{0}clients/count?type=fileserver,vm,laptop',
    'DASHBOARD_NEEDS_ATTENTION_TILE': '{0}CommServ/Anomaly/Entity/Count?anomalousEntityType=14',

    'GET_ALL_LIVE_SYNC_PAIRS': '{0}Replications/Monitors/streaming?subclientId=%s',
    'GET_ALL_LIVE_SYNC_VM_PAIRS': '{0}Replications/Monitors/streaming?subclientId=%s&taskId=%s',
    'GET_LIVE_SYNC_VM_PAIR': '{0}Replications/Monitors/streaming?subclientId=%s&replicationPairId=%s',
    'GET_REPLICATION_PAIR': '{0}Replications/Monitors/streaming?replicationPairId=%s',
    'GET_REPLICATION_PAIRS': '{0}Replications/Monitors/streaming?',

    'BACKUP_NETWORK_PAIRS': '{0}CommServ/DataInterfacePairs?ClientId=%s',
    'BACKUP_NETWORK_PAIR': '{0}CommServ/DataInterfacePairs',

    'GET_ALL_RECOVERY_TARGETS': '{0}V4/RecoveryTargets',
    'GET_RECOVERY_TARGET': '{0}V4/RecoveryTarget/%s',

    'RETIRE': '{0}Client/%s/Retire',
    'GET_REMOTE_CACHE_CLIENTS': '{0}RemoteCacheClients',

    'DATASOURCE_ACTIONS': '{0}EDiscoveryClients/Datasources/Actions',
    'CLOUD_CREATE': '{0}cloud/create',
    'CLOUD_MODIFY': '{0}cloud/modify',
    'CLOUD_DELETE': '{0}cloud/delete',
    'CLOUD_ROLE_UPDATE': '{0}cloud/role/update',
    'CLOUD_NODE_UPDATE': '{0}cloud/node/update',
    'GET_ALL_INDEX_SERVERS': '{0}dcube/getAnalyticsEngine?retrieveall=true',
    'GET_ALL_ROLES': '{0}IndexingGateway/GetAnalyticsRolesInfo',
    'GET_THREAT_INDICATORS': '{0}/Client/Anomaly',
    'GET_ALL_CLIENT_ANOMALIES': '{0}/Client/AnomalyRecord?filter=%s&clients=%s',
    'CLEAR_ANOMALIES': '{0}/Client/PruneAnomalyRecord',
    'RUN_ANOMALY_SCAN': '{0}/EDiscoveryClients/OnDemandAnalytics',
    'ANOMALY_CLIENTS_COUNT':'{0}/clients/count?type=fileserver,vm,laptop',
    'MONITORED_VM_COUNT':'{0}/Client/Anomaly/MonitoredVMCount',
    'GET_SWAGGER': '{0}swagger/V3/swagger.json',

    'COMMCELL_METADATA': '{0}Commcell/MetaData',
    'METALLIC_LINKING': '{0}CloudService/Subscription',
    'CV_METALLIC_LINKING': '{0}/CloudService/Subscription/Details',
    'METALLIC_COMPLETED_SETUPS': '{0}CloudService/CompletedSetups',
    'USER_MAPPINGS': '{0}GetUserMappings',
    'METALLIC_REGISTERED': '{0}CloudServices/Registered',
    'METALLIC_UNLINK': '{0}CloudService/Unsubscribe',

    'ADD_OR_GET_SAML': '{0}/v4/SAML',
    'EDIT_SAML': '{0}/v4/SAML/%s',
    'GET_SAML_PROP': '{0}/ThirdParty/SAML/App?isOpenAPISpec=true',

    'REGIONS': '{0}/v4/Regions',
    'REGION': '{0}/v4/Regions/%s',
    'EDIT_REGION': '{0}/entity/%s/%s/region',
    'GET_REGION': '{0}/entity/%s/%s/region?entityRegionType=%s',
    'CALCULATE_REGION': '{0}/entity/%s/%s/region?calculate=True&entityRegionType=%s',

    'GET_OEM_ID': '{0}/GetOemId',

    'DO_WEB_SEARCH': '{0}/Search',


    'GET_SLA': '{0}GetSLAConfiguration',
    'WORKLOAD_REGION': '{0}entity/COMMCELL/%s/region?entityRegionType=WORKLOAD',

    'GET_USER_SUGGESTIONS': '{0}getADUserSuggestions',
    'DOMAIN_SSO': '{0}V4/LDAP/%s',

    'LAUNCH_O365_LICENSING': '{0}Office365/License',

    'VM_GROUP': '{0}V4/VmGroup/%s',

    'VSA_HIDDEN_SUBCLIENT': '{0}GetId?clientname=%s&agent=Virtual Server&backupset=%s&subclient=Do Not Backup',

    'ALL_RECOVERY_GROUPS': '{0}RecoveryGroups',
    'RECOVERY_GROUP': '{0}RecoveryGroup/%s?getEntityDetails=true',
    'RECOVERY_GROUP_RECOVER': '{0}RecoveryGroup/%s/Recover',
    'CLEANUP_RECOVERY_GROUP': '{0}RecoveryGroup/CleanupRecovery',


    'ADCOMPAREID': '{0}/ActiveDirectory/Subclient/%s/Comparison',

    'ADCOMPARESTATUSCHECK': '{0}/ActiveDirectory/Comparison/%s',
    'ADCOMPAREVIEWRESULTS': '{0}/ActiveDirectory/Compare',

    'LIST_BACKUP_JOBS': '{0}Jobs/Calendar?dateListResponse=false&agedJobs=false&subclientId=&instanceId=&backupsetId=%s'
                        '&clientId=%s&jobTypeList=Backup,SYNTHFULL&fromStartTime=%s&toStartTime=%s&applicationIdList'
                        '=&statusList=%s&clientIdList=%s&isArchiverClient=false&lastBackup=false',

    'VIEW_PROPERTIES': '{0}/Recall?at=%s&si=%s&op=%s&appId=%s&ec=%s',




    'COMMSERVE_RECOVERY': '{0}cvdrbackup/csrecovery',
    'GET_BACKUPSET_INFO': '{0}cvdrbackup/info?csGuid=%s',
    'GET_COMMSERVE_RECOVERY_LICENSE_DETAILS': '{0}cvdrbackup/csrecovery/quota?csGuid=%s',
    'GET_COMMSERVE_RECOVERY_RETENTION_DETAILS': '{0}cvdrbackup/cleanup/lock?csGuid=%s',
    'ADDASHBOARD': '{0}/ActiveDirectory/Overview',
    'ADDAZURECLIENT': '{0}/v4/ActiveDirectory/AzureAD',
    'ADCLIENTS': '{0}/ActiveDirectory/Clients?apptypeId=0',
    'ADAPPS': '{0}/v4/ActiveDirectory/Apps',

    'ENABLE_DATA_AGING': '{0}/V5/ServerPlan/%s/BackupDestination/%s',


    'LICENSE_COLLECTION': '{0}Office365/License',

    'NAVIGATION_SETTINGS': '{0}/NavigationSettings',

    'COCKROACHDB': '{0}/Client/CockroachDB',

    'ALL_RPStores': '{0}Library?libraryType=RPSTORE',

    'RESET_TENANT_PASSWORD': '{0}/user/Password/Forgot',

    'GET_DOC_PREVIEW': '{0}/GetDocPreviewWithFields',

    'GET_VARIOUS_PREVIEW':  '{0}/GetVariousPreview',

    'GET_PREVIEW': '{0}/GetPreview',

    'CREATE_ACCESS_TOKEN': '{0}/V4/AccessToken',

    'UPDATE_ACCESS_TOKEN': '{0}/V4/AccessToken/%s',

    'REVOKE_ACCESS_TOKEN': '{0}/V4/AccessToken/%s',

    'GET_ACCESS_TOKENS': '{0}/V4/AccessToken/?userId=%s',

    'RENEW_TOKEN': '{0}/V4/AccessToken/Renew'
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
