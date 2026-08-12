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
    """
    Container class for Teams subclient-related constants.

    This class is designed to centralize and manage all constant values
    used throughout the Teams subclient implementation. By storing constants
    in a dedicated class, it promotes maintainability, consistency, and
    ease of access across the codebase.

    Key Features:
        - Centralized storage for Teams subclient constants
        - Improves code readability and maintainability
        - Prevents duplication of constant values

    #ai-gen-doc
    """

    ADD_DISCOVER_TYPE = 12
    INDEX_APP_TYPE = 200128
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
            "visibility": 1

        },
        "lastBackupJobRanTime": {},
        "IdxCollectionTime": {},
        "user": None
    }

    BACKUP_USER_JSON = {
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

    DESTINATION_ONEDRIVE_INFO = {
        "userSMTP": None,
        "userGUID": None,
         "folder": "/"
    }

    USER_ONEDRIVE_RESTORE_JSON = {
      "taskInfo": {
        "associations": None,
        "task": {
            "taskType": 1,
            "initiatedFrom": 1
        },
        "subTasks": [
          {
            "subTask": {
              "subTaskType": 3,
              "operationType": 1001
            },
            "options": {
              "commonOpts": {
                "notifyUserOnJobCompletion": False,
                "jobMetadata": [
                  {
                    "selectedItems": [],
                    "jobOptionItems": []
                  }
                ]
              },
              "restoreOptions": {
                "browseOption": {
                  "commCellId": 2
                },
                "destination": {
                  "inPlace": False,
                  "destClient": {},
                  "destPath": None,
                  "destAppId": 134
                },
                "commonOptions": {
                  "unconditionalOverwrite": False,
                  "overwriteFiles": False,
                  "skip": True
                },
                "cloudAppsRestoreOptions": {
                  "instanceType": 36,
                  "msTeamsRestoreOptions": {
                    "restoreToTeams": False,
                    "restoreToOneDrive": True,
                    "destLocation": None,
                    "overWriteItems": False,
                    "restoreUsingFindQuery": False,
                    "findQuery": {
                      "mode": 4,
                      "advSearchGrp": {
                        "commonFilter": [
                          {
                            "filter": {
                              "interFilterOP": 2,
                              "filters": [
                                {
                                  "field": "CISTATE",
                                  "intraFieldOp": 0,
                                  "fieldValues": {
                                    "values": [
                                      "1"
                                    ]
                                  }
                                }
                              ]
                            }
                          }
                        ],
                        "fileFilter": [
                          {
                            "interGroupOP": 2,
                            "filter": {
                              "interFilterOP": 2,
                              "filters": [
                                  {
                                      "field": "CV_OBJECT_GUID",
                                      "intraFieldOp": 0,
                                      "fieldValues": {
                                          "values": [
                                              ""
                                          ]
                                      }
                                  }
                              ]
                            }
                          }
                        ],
                        "emailFilter": [],
                        "galaxyFilter": [
                          {
                            "appIdList": None
                          }
                        ]
                      },
                      "searchProcessingInfo": {
                        "resultOffset": 0,
                        "pageSize": 15,
                        "queryParams": [
                          {
                            "param": "ENABLE_MIXEDVIEW",
                            "value": "true"
                          },
                          {
                            "param": "RESPONSE_FIELD_LIST",
                            "value": "DATA_TYPE,CONTENTID,CV_OBJECT_GUID"
                                     ",PARENT_GUID,CV_TURBO_GUID,AFILEID"
                                     ",AFILEOFFSET,COMMCELLNO,MODIFIEDTIME"
                                     ",SIZEINKB,BACKUPTIME,CISTATE,DATE_DELETED"
                                     ",TEAMS_ITEM_ID,TEAMS_ITEM_NAME,TEAMS_NAME"
                                     ",TEAMS_SMTP,TEAMS_ITEM_TYPE,TEAMS_CHANNEL_TYPE"
                                     ",TEAMS_TAB_TYPE,TEAMS_GROUP_VISIBILITY"
                                     ",TEAMS_GUID,TEAMS_CONV_ITEM_TYPE,TEAMS_CONV_MESSAGE_TYPE"
                                     ",TEAMS_CONV_SUBJECT,TEAMS_CONV_IMPORTANCE,TEAMS_CONV_SENDER_TYPE"
                                     ",TEAMS_CONV_SENDER_NAME,TEAMS_CONV_HAS_REPLIES,CI_URL,TEAMS_DRIVE_FOLDER_TYPE"
                          }
                        ],
                        "sortParams": [
                          {
                            "sortDirection": 0,
                            "sortField": "TEAMS_NAME"
                          }
                        ]
                      }
                    },
                    "selectedItemsToRestore": None,
                    "destinationOneDriveInfo": None,
                    "restorePostsAsHtml": True
                  }
                }
              }
            }
          }
        ]
      }
    }