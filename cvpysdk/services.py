#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
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
    'COMMSERV': '{0}CommServ',

    'GET_ALL_CLIENTS': '{0}Client',
    'GET_VIRTUAL_CLIENTS': '{0}Client?PseudoClientType=VSPseudo',
    'CLIENT': '{0}Client/%s',

    'GET_ALL_AGENTS': '{0}Agent?clientId=%s',
    'AGENT': '{0}Agent',

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

    'CLIENTGROUPS': '{0}ClientGroup',
    'CLIENTGROUP': '{0}ClientGroup/%s',

    'USERGROUPS': '{0}UserGroup',
    'USERGROUP': '{0}UserGroup/%s',

    'BROWSE': '{0}DoBrowse',
    'RESTORE': '{0}CreateTask',

    'GET_WORKFLOWS': '{0}Workflow',
    'DEPLOY_WORKFLOW': '{0}Workflow/%s/action/deploy',
    'EXECUTE_WORKFLOW': '{0}wapi/%s',

    'INSTANCE_BROWSE': '{0}Client/%s/%s/Instance/%s/Browse',

    'SQL_RESTORE_OPTIONS': '{0}SQL/RestoreOptions',

    'EXECUTE_QCOMMAND': '{0}Qcommand/qoperation execute',

    'SOFTWARESTORE_DOWNLOADITEM': '{0}DownloadFile',
    'SOFTWARESTORE_PKGINFO': '{0}SoftwareStore/getPackagePublishInfo?packageName=%s',
    'SOFTWARESTORE_GETPKGID': '{0}SoftwareStoreItem',

    'CREATE_TASK': '{0}CreateTask'
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
