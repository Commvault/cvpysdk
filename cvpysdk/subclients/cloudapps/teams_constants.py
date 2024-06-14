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

"""Helper file to maintain all the constants for MS Teams subclient.

TeamsConstants  -   Maintains constants for MS Teams subclient.

"""


class TeamsConstants:
    """Class to maintain all the Teams subclient related constants."""

    ADD_DISCOVER_TYPE = 12

    ADD_SUBCLIENT_ENTITY_JSON = {
        "instanceId": None,
        "subclientId": None,
        "clientId": None,
        "applicationId": None
    }

    ADD_USER_JSON = {
        "_type_": None,
        "userGUID": None
    }

    ADD_TEAM_JSON = {
        "displayName": None,
        "smtpAddress": None,
        "associated": False,
        "msTeamsInfo": {
            "visibility": 1,
            "teamsCreatedTime": None
        },
        "user": None
    }

    ADD_GROUP_JSON = {
        "associated": False,
        "name": None,
        "id": None
    }

    ADD_REQUEST_JSON = {
        "LaunchAutoDiscovery": False,
        "cloudAppAssociation": {
            "accountStatus": 0,
            "subclientEntity": None,
            "cloudAppDiscoverinfo": {
                "discoverByType": ADD_DISCOVER_TYPE,
                "userAccounts": []
            },
            "plan": {
                "planId": None
            }
        }
    }

    BACKUP_TEAM_JSON = {
        "aliasName": "",
        "displayName": None,
        "smtpAddress": None,
        "BackupSetId": 0,
        "isAutoDiscoveredUser": False,
        "accountSize": 0,
        "ParentWebGuid": "",
        "commonFlags": 0,
        "msTeamsInfo": {
            "visibility": 1,
            "teamsCreatedTime": None
        },
        "lastBackupJobRanTime": {},
        "IdxCollectionTime": {},
        "user": None
    }

    ASSOCIATIONS = {
        "subclientId": None,
        "applicationId": None,
        "clientName": None,
        "displayName": None,
        "backupsetId": None,
        "instanceId": None,
        "subclientGUID": None,
        "clientId": None,
        "clientGUID": None,
        "subclientName": None,
        "backupsetName": None,
        "instanceName": None,
        "_type_": None,
    }

    BACKUP_SUBTASK_JSON = {
        "subTask": {
            "subTaskType": 2,
            "operationType": 2
        },
        "options": {
            "backupOpts": {
                "backupLevel": 2,
                "cloudAppOptions": {"forceFullBackup": False, "userAccounts": []}
            },
            "commonOpts": {
                "notifyUserOnJobCompletion": False,
                "jobMetadata": [
                    {
                        "jobOptionItems": [
                            {
                                "value": "Disabled",
                                "option": "Convert job to full"
                            },
                            {
                                "value": "Disabled",
                                "option": "Total running time"
                            }
                        ],
                        "selectedItems": []
                    }
                ]
            }
        }
    }

    BACKUP_REQUEST_JSON = {
        "processinginstructioninfo": {
            "formatFlags": {"skipIdToNameConversion": True}
        },
        "taskInfo": {
            "associations": [],
            "task": {"taskType": 1},
            "subTasks": []
        }
    }

    RESTORE_TASK_JSON = {
        "initiatedFrom": 2,
        "taskType": 1,
        "policyType": 0
    }

    RESTORE_SUBTASK_JSON = {
        "subTaskType": 3,
        "operationType": 1001
    }

    CUSTOM_CATEGORY_JSON = {
        "subclientEntity": {
            "subclientId": None
        },
        "planEntity": {
            "planId": None,
            "planName": ""
        },
        "status": 0,
        "categoryName": None,
        "categoryQuery": {
            "conditions": []
        },
        "office365V2AutoDiscover": {
            "launchAutoDiscover": True,
            "appType": 134,
            "clientId": None,
            "instanceId": None,
            "instanceType": 36
        }
    }

    ClOUD_APP_EDISCOVER_TYPE = {
        "Teams": 8,
        "Users": 7,
        "Groups": 22
    }