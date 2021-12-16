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

InventoryConstants              -       Maintains constants for Inventory Manager apps

"""
import copy
from enum import Enum


class InventoryConstants:
    """Class to maintain constants for inventory manager"""

    CRAWL_JOB_FAILED_STATE = [5, 6, 7, 8, 9, 10, 11, 12]

    CRAWL_JOB_COMPLETE_STATE = 4

    CRAWL_JOB_COMPLETE_ERROR_STATE = 13

    INVENTORY_ADD_REQUEST_JSON = {
        "inventoryName": "",
        "assets": [],
        "analyticsEngineCloud": {
            "cloudId": 0,
            "cloudDisplayName": ""
        }
    }

    ASSET_ADD_REQUEST_JSON = {
        "name": "",
        "type": 0
    }

    ASSET_PROPERTY_JSON = {
        "propertyValues": {
            "nameValues": [

            ]
        }
    }
    ASSET_PROPERTY_NAME_VALUE_PAIR_JSON = {
        "name": "",
        "value": ""
    }

    FIELD_PROPERTY_NAME = 'name'
    FIELD_PROPERTY_DNSHOST = 'dNSHostName'
    FIELD_PROPERTY_OS = 'operatingSystem'
    FIELD_PROPERTY_IP = 'ipAddresses'
    FIELD_PROPERTY_COUNTRYCODE = 'countryCode'
    FIELD_PROPERTY_CO = 'co'
    FIELD_PROPERTY_DOMAIN = 'domainName'

    KWARGS_NAME = 'name'
    KWARGS_IP = 'ip'
    KWARGS_OS = 'os'
    KWARGS_DOMAIN = 'domain'
    KWARGS_FQDN = 'fqdn'
    KWARGS_COUNTRY_NAME = 'country_name'
    KWARGS_COUNTRY_CODE = 'country_code'

    FIELD_PROPS_MAPPING = {
        FIELD_PROPERTY_NAME: KWARGS_NAME,
        FIELD_PROPERTY_IP: KWARGS_IP,
        FIELD_PROPERTY_OS: KWARGS_OS,
        FIELD_PROPERTY_DOMAIN: KWARGS_DOMAIN,
        FIELD_PROPERTY_DNSHOST: KWARGS_FQDN,
        FIELD_PROPERTY_CO: KWARGS_COUNTRY_NAME,
        FIELD_PROPERTY_COUNTRYCODE: KWARGS_COUNTRY_CODE
    }

    ASSET_FILE_SERVER_PROPERTY = [
        FIELD_PROPERTY_NAME,
        FIELD_PROPERTY_DNSHOST,
        FIELD_PROPERTY_OS,
        FIELD_PROPERTY_IP,
        FIELD_PROPERTY_COUNTRYCODE,
        FIELD_PROPERTY_CO,
        FIELD_PROPERTY_DOMAIN]

    ASSET_ADD_TO_INVENTORY_JSON = {
        "inventoryId": 0,
        "assets": []
    }

    ASSET_DELETE_FROM_INVENTORY_JSON = {
        "inventoryId": 0,
        "assets": []
    }

    VIEW_CATEGORY_PERMISSION = {
        "permissionId": 31,
        "permissionName": "View",
        "_type_": 122
    }
    EDIT_CATEGORY_PERMISSION = {
        "permissionId": 2,
        "permissionName": "Agent Management",
        "_type_": 122
    }

    INVENTORY_SHARE_REQUEST_JSON = {
        "entityAssociated": {
            "entity": [
                {
                    "_type_": 132,
                    "seaDataSourceId": 0
                }
            ]
        },
        "securityAssociations": {
            "associationsOperationType": 1,
            "associations": [
                {
                    "userOrGroup": [
                        {
                            "userId": 0,
                            "_type_": 0,
                            "userName": ""
                        }
                    ],
                    "properties": {
                        "categoryPermission": {
                            "categoriesPermissionOperationType": 1,
                            "categoriesPermissionList": [
                                VIEW_CATEGORY_PERMISSION
                            ]
                        }
                    }
                }
            ]
        }
    }

    class AssetType(Enum):
        NAME_SERVER = 61
        FILE_SERVER = 132


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
