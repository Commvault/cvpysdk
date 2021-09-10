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

"""Helper file to maintain all the constants for Activate Apps

ActivateEntityConstants         -       Maintains constants for Regex custom entity

TagConstants                    -       Maintains constants for Tags

ClassifierConstants             -       Maintains constants for Classifiers

TrainingStatus                  -       Enum class for classifier training status

TargetApps                      -       Enum class for Activate App types

PlanConstants                   -       Maintains constants for Plan operations

"""
import copy
from enum import Enum

class PlanConstants:
    """Class to maintain constants related to DC plan activate operations"""

    INDEXING_ONLY_METADATA = 1
    INDEXING_METADATA_AND_CONTENT = 2

    DEFAULT_INCLUDE_DOC_TYPES = "*.doc,*.docx,*.xls,*.xlsx,*.ppt,*.pptx,*.msg,*.txt,*.rtf,*.eml,*.pdf,*.htm,*.html,*.csv,*.log,*.ods,*.odt,*.odg,*.odp,*.dot,*.pages,*.xmind"
    DEFAULT_EXCLUDE_LIST = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "C:\\Windows"]

    DEFAULT_MIN_DOC_SIZE = 0
    DEFAULT_MAX_DOC_SIZE = 50

    PLAN_UPDATE_REQUEST_JSON = {
        7: {
            "ciPolicyInfo": {
                "ciPolicy": {
                    "policyType": 5,
                    "flags": 536870912,
                    "agentType": {
                        "appTypeId": 0,
                        "entityInfo": {},
                        "flags": {}
                    },
                    "detail": {
                        "ciPolicy": {}
                    }
                }
            },
            "eePolicyInfo": {
                "eePolicy": {
                    "policyType": 3,
                    "flags": 536870920,
                    "agentType": {
                        "appTypeId": 0,
                        "entityInfo": {},
                        "flags": {}
                    },
                    "detail": {
                        "eePolicy": {}
                    }
                }
            },
            "summary": {
                "plan": {
                    "planId": 0
                }
            }
        }
    }

    PLAN_SCHEDULE_REQUEST_JSON = {
        7: {
            "summary": {
                "plan": {
                    "planId": 0
                }
            },
            "schedule": {
                "associations": [
                    {
                        "_type_": 158,
                        "entityId": 0
                    }
                ],
                "task": {
                    "taskType": 4,
                    "taskName": "",
                    "taskFlags": {
                        "isEdiscovery": True
                    }
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskName": "",
                            "subTaskType": 1,
                            "operationType": 5025
                        },
                        "pattern": {},
                        "options": {
                            "backupOpts": {
                                "backupLevel": 2,
                                "mediaOpt": {
                                    "auxcopyJobOption": {
                                        "maxNumberOfStreams": 1,
                                        "allCopies": True,
                                        "useMaximumStreams": True
                                    }
                                }
                            },
                            "adminOpts": {
                                "contentIndexingOption": {
                                    "fileAnalytics": False,
                                    "idaType": 1,
                                    "operationType": 2
                                }
                            }
                        }
                    }
                ]
            }
        }
    }
    PLAN_SHARE_REQUEST_JSON = {
        "entityAssociated": {
            "entity": [
                {
                    "entityType": 158,
                    "_type_": 150,
                    "entityId": 0
                }
            ]
        },
        "securityAssociations": {
            "associationsOperationType": 1,
            "associations": [
                {
                    "userOrGroup": [
                        {

                        }
                    ],
                    "properties": {
                        "role": {
                            "_type_": 120,
                            "roleId": 0,
                            "roleName": ""
                        }
                    }
                }
            ]
        }
    }


class TargetApps(Enum):
    """Class to maintain supported apps types in Activate"""
    SDG = 2
    FSO = 1
    CASE_MGR = 4
    FS = 8
    
class TrainingStatus(Enum):
    """Class to maintain training status for classifier"""
    NOT_APPLICABLE = 0
    CREATED = 1
    RUNNING = 2
    FAILED = 3
    COMPLETED = 4
    CANCELLED = 5
    NOT_USABLE = 6


class ClassifierConstants:
    """Class to maintain all the Classsifier related constants"""
    CREATE_REQUEST_JSON = {
        "description": "",
        "enabled": True,
        "entityName": "",
        "entityType": 4,
        "entityKey": "",
        "entityXML": {
            "classifierDetails": {
                "datasetStorageType": 1,
                "trainingStatus": 6,
                "trainDatasetURI": "http://localhost:22000/solr",
                "datasetType": "docs",
                "CAUsedInTraining": {
                    "caUrl": "",
                    "clientId": 0,
                    "cloudName": "",
                    "cloudId": 0
                }
            }
        }
    }


class ActivateEntityConstants:
    """Class to maintain all the Activate entity related constants"""

    REQUEST_JSON = {
        "regularExpression": "",
        "flags": 0,
        "enabled": True,
        "entityName": "",
        "entityXML": {
            "keywords": "",
            "isSystemDefinedEntity": False
        }
    }


class TagConstants:
    """class to maintain all the Tags related constants"""

    TAG_SET_ADD_REQUEST_JSON = {
        "entityType": 9504,
        "operationType": 1,
        "fromSite": 4,
        "container": {
            "containerType": 9504,
            "containerName": "",
            "comment": ""
        }
    }

    TAG_SET_MODIFY_REQUEST_JSON = copy.deepcopy(TAG_SET_ADD_REQUEST_JSON)
    TAG_SET_MODIFY_REQUEST_JSON['operationType'] = 3

    TAG_SET_DELETE_REQUEST_JSON = {
        "entityType": 9504,
        "containers": [
            {
                "containerType": 9504,
                "containerId": 0
            }
        ]
    }

    TAG_ADD_REQUEST_JSON = {
        "container": {
            "containerId": 0
        },
        "tags": [
            {
                "name": ""
            }
        ]
    }

    TAG_MODIFY_REQUEST_JSON = copy.deepcopy(TAG_ADD_REQUEST_JSON)
    TAG_MODIFY_REQUEST_JSON['tags'][0]['tagId'] = 0

    VIEW_PERMISSION = {
        "permissionId": 31,
        "_type_": 122,
        "permissionName": "View"
    }
    ADD_PERMISSION = {
        "permissionId": 34,
        "_type_": 122,
        "permissionName": "Add/Append"
    }

    TAG_SET_SHARE_REQUEST_JSON = {
        "entityAssociated": {
            "entity": [
                {
                    "tagId": 0,
                    "_type_": 9504
                }
            ]
        },
        "securityAssociations": {
            "associationsOperationType": 1,
            "associations": [
                {
                    "userOrGroup": [
                        {

                        }
                    ],
                    "properties": {
                        "permissions": [
                            VIEW_PERMISSION
                        ]
                    }
                }

            ]
        }
    }
