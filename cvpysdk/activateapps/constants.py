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

EdiscoveryConstants             -       Maintains constants for Ediscovery clients in activate

RequestConstants                -       Maintains constants for request manager in Activate

ComplianceConstants             -       Maintains constants for Compliance Search in Activate

"""
import copy
from enum import Enum


class RequestConstants:
    """class to maintain constants for request manager"""
    PROPERTY_REVIEW_CRIERIA = 'ReviewCriteria'
    PROPERTY_ENTITIES = 'Entities'
    PROPERTY_REQUEST_HANDLER_ID = 'RequestHandlerId'
    PROPERTY_REQUEST_HANDLER_NAME = 'RequestHandlerName'
    PROPERTY_REVIEW_SET_ID = 'ReviewSetId'
    SEARCH_QUERY_SELECTION_SET = {
        "entity_*",
        "count_entity_*",
        "Url",
        "contentid",
        "FileName",
        "Size",
        "data_source",
        "data_source_name",
        "entities_extracted",
        "RedactMode*",
        "CommentFor*",
        "ConsentFor*"}

    FACET_REVIEWED = '_ConsentFor_%s_b_Reviewed'
    FACET_NOT_REVIEWED = '_ConsentFor_%s_b_Not reviewed'
    FACET_ACCEPTED = '_ConsentFor_%s_b_Accepted'
    FACET_DECLINED = '_ConsentFor_%s_b_Declined'
    FACET_REDACTED = '_RedactMode_%s_b_Redacted'
    FACET_NOT_REDACTED = '_RedactMode_%s_b_Not redacted'
    FACET_COUNT = "count"
    REQUEST_FEDERATED_FACET_SEARCH_QUERY = {"searchParams": [{"key": "q",
                                                              "value": "*:*"},
                                                             {"key": "wt",
                                                              "value": "json"},
                                                             {"key": "rows",
                                                              "value": "0"},
                                                             {"key": "defType",
                                                              "value": "edismax"},
                                                             {"key": "facet",
                                                              "value": "true"},
                                                             {"key": "json.facet",
                                                              "value": "{\"_ConsentFor_<rsidparam>_b_Reviewed\":{\"type\":\"query\",\"domain\":{\"excludeTags\":[\"tag_group_ConsentFor_<rsidparam>_b\",\"tag_ConsentFor_<rsidparam>_b\",\"tag_exclude_ConsentFor_<rsidparam>_b\"]},\"numBuckets\":true,\"mincount\":1,\"q\":\"ConsentFor_<rsidparam>_b:*\",\"facet\":{}},\"_ConsentFor_<rsidparam>_b_Not reviewed\":{\"type\":\"query\",\"domain\":{\"excludeTags\":[\"tag_group_ConsentFor_<rsidparam>_b\",\"tag_ConsentFor_<rsidparam>_b\",\"tag_exclude_ConsentFor_<rsidparam>_b\"]},\"numBuckets\":true,\"mincount\":1,\"q\":\"contentid:* AND -(ConsentFor_<rsidparam>_b:*)\",\"facet\":{}},\"_ConsentFor_<rsidparam>_b_Accepted\":{\"type\":\"query\",\"domain\":{\"excludeTags\":[\"tag_group_ConsentFor_<rsidparam>_b\",\"tag_ConsentFor_<rsidparam>_b\",\"tag_exclude_ConsentFor_<rsidparam>_b\"]},\"numBuckets\":true,\"mincount\":1,\"q\":\"ConsentFor_<rsidparam>_b:true\",\"facet\":{}},\"_ConsentFor_<rsidparam>_b_Declined\":{\"type\":\"query\",\"domain\":{\"excludeTags\":[\"tag_group_ConsentFor_<rsidparam>_b\",\"tag_ConsentFor_<rsidparam>_b\",\"tag_exclude_ConsentFor_<rsidparam>_b\"]},\"numBuckets\":true,\"mincount\":1,\"q\":\"ConsentFor_<rsidparam>_b:false\",\"facet\":{}},\"_RedactMode_<rsidparam>_b_Redacted\":{\"type\":\"query\",\"domain\":{\"excludeTags\":[\"tag_group_RedactMode_<rsidparam>_b\",\"tag_RedactMode_<rsidparam>_b\",\"tag_exclude_RedactMode_<rsidparam>_b\"]},\"numBuckets\":true,\"mincount\":1,\"q\":\"RedactMode_<rsidparam>_b:true\",\"facet\":{}},\"_RedactMode_<rsidparam>_b_Not redacted\":{\"type\":\"query\",\"domain\":{\"excludeTags\":[\"tag_group_RedactMode_<rsidparam>_b\",\"tag_RedactMode_<rsidparam>_b\",\"tag_exclude_RedactMode_<rsidparam>_b\"]},\"numBuckets\":true,\"mincount\":1,\"q\":\"RedactMode_<rsidparam>_b:false\",\"facet\":{}},\"FileExtension\":{\"type\":\"terms\",\"domain\":{\"excludeTags\":[\"tag_FileExtension\",\"tag_exclude_FileExtension\"]},\"numBuckets\":true,\"mincount\":1,\"field\":\"FileExtension\",\"limit\":-1,\"facet\":{},\"sort\":{\"count\":\"desc\"}},\"ReadAccessUserName\":{\"type\":\"terms\",\"domain\":{\"excludeTags\":[\"tag_ReadAccessUserName\",\"tag_exclude_ReadAccessUserName\"]},\"numBuckets\":true,\"mincount\":1,\"field\":\"ReadAccessUserName\",\"limit\":-1,\"facet\":{},\"sort\":{\"count\":\"desc\"}},\"data_source_name\":{\"type\":\"terms\",\"domain\":{\"excludeTags\":[\"tag_data_source_name\",\"tag_exclude_data_source_name\"]},\"numBuckets\":true,\"mincount\":1,\"field\":\"data_source_name\",\"limit\":-1,\"facet\":{},\"sort\":{\"count\":\"desc\"}}}"},
                                                             {"key": "useDCubeReq",
                                                              "value": "true"}]}

    FIELD_DOC_COUNT = "TotalDocuments"
    FIELD_REVIEWED = "ReviewedDocuments"
    FIELD_NOT_REVIEWED = "Non-ReviewedDocuments"
    FIELD_ACCEPTED = 'AcceptedDocuments'
    FIELD_DECLINED = 'DeclinedDocuments'
    FIELD_REDACTED = 'RedactedDocuments'
    FIELD_NOT_REDACTED = 'Non-RedactedDocuments'

    class RequestStatus(Enum):
        """enum to specify different request status"""
        TaskCreated = 1
        TaskConfigured = 2
        ReviewInProgress = 3
        ReviewCompleted = 4
        ApproveCompleted = 5
        ExportCompleted = 6
        DeleteCompleted = 7
        TaskCompleted = 8
        ApprovalRequested = 9
        ActionInProgress = 10
        CompletedWithErrors = 11
        Failed = 12

    class RequestType(Enum):
        """enum to maintain different request type"""
        EXPORT = 'EXPORT'
        DELETE = 'DELETE'


class EdiscoveryConstants:
    """class to maintain constants for ediscovery clients"""

    class CrawlType(Enum):
        """Crawl type for SDG/FSO jobs"""
        LIVE = 1
        BACKUP = 2
        CONTENT_INDEXED = 3
        FILE_LEVEL_ANALYTICS = 4
        BACKUP_V2 = 5

    class SourceType(Enum):
        """Source type of data for FSO/SDG app"""
        SOURCE = 1
        BACKUP = 2

    class ReviewActions(Enum):
        """Review actions for documents on SDG/FSO app"""
        DELETE = 1
        MOVE = 4
        RETENTION = 10
        IGNORE = 11
        ARCHIVE = 90
        TAG = 98

    class RiskTypes(Enum):
        """Different risk types for documents on SDG/FSO app"""
        OPEN_ACCESS = 1
        OLD_FILES = 2
        FILE_MOVED = 3
        MULTI_USER_ACCESS = 4
        NO_RETENTION = 5
        IS_PROTECTED = 6

    FSO_SERVERS = "FsoServers"
    FSO_SERVER_GROUPS = "FsoServerGroups"

    SERVER_LEVEL_SCHEDULE_JSON = {
        "taskInfo": {
            "task": {
                "taskType": 4,
                "taskFlags": {
                    "isEdiscovery": True
                },
                "taskName": ""
            },
            "subTasks": [
                {
                    "subTask": {
                        "operationType": 5025,
                        "subTaskType": 1,
                        "subTaskName": ""
                    },
                    "pattern": {},
                    "options": {
                        "backupOpts": {
                            "backupLevel": 2,
                            "mediaOpt": {
                                "auxcopyJobOption": {
                                    "allCopies": True,
                                    "useMaximumStreams": True,
                                    "maxNumberOfStreams": 1
                                }
                            }
                        },
                        "adminOpts": {
                            "contentIndexingOption": {
                                "idaType": 1,
                                "operationType": 2,
                                "fileAnalytics": False
                            }
                        }
                    }
                }
            ],
            "associations": [
                {
                    "clientId": 0,
                    "_type_": 3
                }
            ]
        }
    }

    REVIEW_ACTION_FSO_SUPPORTED = [ReviewActions.DELETE.value, ReviewActions.MOVE.value, ReviewActions.ARCHIVE.value]

    REVIEW_ACTION_SDG_SUPPORTED = [
        ReviewActions.DELETE.value,
        ReviewActions.MOVE.value,
        ReviewActions.ARCHIVE.value,
        ReviewActions.RETENTION.value,
        ReviewActions.IGNORE.value]

    CREATE_CLIENT_REQ_JSON = {
        "clientInfo": {
            "clientType": 19,
            "edgeDrivePseudoClientProperties": {
                "systemDriveType": 6,
                "edgeDriveAssociations": {},
                "eDiscoveryInfo": {
                    "eDiscoverySubType": 2,
                    "inventoryDataSource": {
                        "seaDataSourceId": 0
                    }
                }
            },
            "plan": {
                "planId": 0
            }
        },
        "entity": {
            "clientName": "",
            "_type_": 3
        }
    }

    REVIEW_ACTION_DELETE_REQ_JSON = {
        "operation": ReviewActions.DELETE.value,
        "files": "",
        "deleteFromBackup": False,
        "options": ""}

    REVIEW_ACTION_MOVE_REQ_JSON = {"operation": ReviewActions.MOVE.value, "files": "", "options": ""}

    REVIEW_ACTION_SET_RETENTION_REQ_JSON = {
        "operation": ReviewActions.RETENTION.value,
        "remActionRequest": {
            "dataSourceId": 0,
            "handlerName": "default",
            "isBulkOperation": False,
            "searchRequest": ""},
        "setRetentionReq": {"numOfMonthsRemain": 0},
    }

    REVIEW_ACTION_IGNORE_FILES_REQ_JSON = {
        "operation": ReviewActions.IGNORE.value,
        "remActionRequest": {
            "dataSourceId": 0,
            "handlerName": "default",
            "isBulkOperation": False,
            "searchRequest": ""},
        "ignoreRisksReq": {"ignoreAllRisks": False},
    }

    REVIEW_ACTION_TAG_REQ_JSON = {
        "operation": ReviewActions.TAG.value,
        "remActionRequest": {
            "dataSourceId": 0,
            "isBulkOperation": False},
        "taggingRequest": {}}

    REVIEW_ACTION_BULK_SEARCH_REQ = "{\"searchParams\":" \
                                    "[{\"key\":\"q\",\"value\":\"*:*\"},{\"key\":\"wt\",\"value\":\"json\"}," \
                                    "{\"key\":\"rows\",\"value\":\"0\"},{\"key\":\"defType\",\"value\":\"edismax\"}," \
                                    "{\"key\":\"fq\",\"value\":\"IsFile:\\\"1\\\"\"}," \
                                    "{\"key\":\"fl\",\"value\":\"FileName\"},{\"key\":\"fl\",\"value\":\"OwnerName\"}," \
                                    "{\"key\":\"fl\",\"value\":\"OwnerLocation\"}," \
                                    "{\"key\":\"fl\",\"value\":\"CountryCode\"}," \
                                    "{\"key\":\"fl\",\"value\":\"FileExtension\"}," \
                                    "{\"key\":\"fl\",\"value\":\"operatingSystem\"}," \
                                    "{\"key\":\"fl\",\"value\":\"IsProtected\"}," \
                                    "{\"key\":\"fl\",\"value\":\"FileName_path\"},{\"key\":\"fl\",\"value\":\"Url\"}," \
                                    "{\"key\":\"fl\",\"value\":\"ClientId\"}," \
                                    "{\"key\":\"fl\",\"value\":\"DocumentType\"}," \
                                    "{\"key\":\"fl\",\"value\":\"contentid\"}," \
                                    "{\"key\":\"fl\",\"value\":\"AllowListUsername\"}," \
                                    "{\"key\":\"fl\",\"value\":\"AllowModifyUsername\"}," \
                                    "{\"key\":\"fl\",\"value\":\"AllowWriteUsername\"}," \
                                    "{\"key\":\"fl\",\"value\":\"AllowExecuteUsername\"}," \
                                    "{\"key\":\"fl\",\"value\":\"AllowFullControlUsername\"}," \
                                    "{\"key\":\"fl\",\"value\":\"ExpiryDate\"}," \
                                    "{\"key\":\"fl\",\"value\":\"CreatedTime\"}," \
                                    "{\"key\":\"fl\",\"value\":\"data_source\"}," \
                                    "{\"key\":\"fl\",\"value\":\"data_source_name\"}," \
                                    "{\"key\":\"fl\",\"value\":\"data_source_type\"}," \
                                    "{\"key\":\"fl\",\"value\":\"entities_extracted\"}," \
                                    "{\"key\":\"fl\",\"value\":\"ConsentFor_*\"}," \
                                    "{\"key\":\"fl\",\"value\":\"RedactFor_*\"}," \
                                    "{\"key\":\"fl\",\"value\":\"RedactMode_*\"}," \
                                    "{\"key\":\"fl\",\"value\":\"CommentFor_*\"}," \
                                    "{\"key\":\"fl\",\"value\":\"AppType\"}," \
                                    "{\"key\":\"fl\",\"value\":\"ApplicationId\"}," \
                                    "{\"key\":\"fl\",\"value\":\"CVTurboGUID\"}," \
                                    "{\"key\":\"fl\",\"value\":\"CommcellNumber\"}," \
                                    "{\"key\":\"fl\",\"value\":\"AchiveFileId\"}," \
                                    "{\"key\":\"fl\",\"value\":\"ArchiveFileOffset\"}," \
                                    "{\"key\":\"fl\",\"value\":\"Size\"}," \
                                    "{\"key\":\"fl\",\"value\":\"Risk_*\"}," \
                                    "{\"key\":\"fl\",\"value\":\"LastAccessedBy\"}," \
                                    "{\"key\":\"fl\",\"value\":\"LastModifiedBy\"}," \
                                    "{\"key\":\"fl\",\"value\":\"ModifiedTimeAsStr\"}," \
                                    "{\"key\":\"fl\",\"value\":\"entity_doc_tags\"}," \
                                    "{\"key\":\"fl\",\"value\":\"TagIds\"},{\"key\":\"fl\",\"value\":\"FileName\"}," \
                                    "{\"key\":\"fl\",\"value\":\"Url\"},{\"key\":\"fl\",\"value\":\"Size\"}," \
                                    "{\"key\":\"fl\",\"value\":\"OwnerName\"}," \
                                    "{\"key\":\"fl\",\"value\":\"entity_doc_tags\"}," \
                                    "{\"key\":\"start\",\"value\":\"0\"}]}"

    REVIEW_ACTION_SEARCH_FL_SET = {
        "FileName",
        "OwnerName",
        "OwnerLocation",
        "CountryCode",
        "FileExtension",
        "operatingSystem",
        "IsProtected",
        "FileName_path",
        "Url",
        "ClientId",
        "DocumentType",
        "contentid",
        "AllowListUsername",
        "AllowModifyUsername",
        "AllowWriteUsername",
        "AllowExecuteUsername",
        "AllowFullControlUsername",
        "ExpiryDate",
        "CreatedTime",
        "data_source",
        "data_source_name",
        "data_source_type",
        "entities_extracted",
        "ConsentFor_*",
        "RedactFor_*",
        "RedactMode_*",
        "CommentFor_*",
        "AppType",
        "ApplicationId",
        "CVTurboGUID",
        "CommcellNumber",
        "AchiveFileId",
        "ArchiveFileOffset",
        "Size",
        "Risk_*",
        "LastAccessedBy",
        "LastModifiedBy",
        "ModifiedTimeAsStr",
        "entity_doc_tags",
        "TagIds"}

    REVIEW_ACTION_IDA_SELECT_SET = {
        5: {'contentid', 'Url', 'ClientId', 'CreatedTime', 'FileName'}}

    FS_SERVER_HANDLER_NAME = 'GetFileServers'
    ADD_FS_REQ_JSON = {
        "datasourceId": 0,
        "indexServerClientId": 0,
        "followScheduleCrawl": False,
        "datasources": [
            {
                "datasourceName": "",
                "properties": [],
                "datasourceType": 5,
                "accessNodes": [
                    {
                        "clientId": 0,
                        "clientName": ""
                    }
                ]
            }
        ]
    }

    FS_DEFAULT_EXPORT_FIELDS = {'FileName', 'Url', 'Size', 'OwnerName', 'CreatedTime', 'AccessTime', 'ModifiedTime'}
    EXPORT_DOWNLOAD_REQ = {
        "appTypeId": 200,
        "responseFileName": "",
        "fileParams": [
            {
                "name": "",
                "id": 2
            },
            {
                "name": "zip",
                "id": 3
            },
            {
                "name": "Streamed",
                "id": 10
            }
        ]
    }

    DATA_SOURCE_TYPES = {
        0: 'NONE',
        1: 'jdbc',
        5: 'file',
        9: 'ldap',
        10: 'federated',
        11: 'blank',
        15: 'fla',
        16: 'edge',
        17: 'exchange',
        18: 'reviewset',
        22: 'nfs',
        24: 'systemdefault',
        26: 'onedrive',
        27: 'sharepoint',
        28: 'email',
        29: 'dbanalysis',
        30: 'cloudpaas',
        31: 'googledrive',
        32: 'gmail',
        34: 'onedriveindex',
        37: 'dynamic365'
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

    SHARE_REQUEST_JSON = {
        "entityAssociated": {
            "entity": [
                {
                    "_type_": 3,
                    "clientId": 0
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

    DS_FILE = 'file'
    DS_CLOUD_STORAGE = 'cloudstorage'
    FIELD_DATA_SOURCE_DISPLAY_NAME = 'datasourceDisplayName'
    FIELD_DISPLAY_NAME = 'displayName'
    FIELD_DATA_SOURCE_NAME = 'datasourceName'
    FIELD_DATA_SOURCE_ID_NON_SEA = 'datasourceId'
    FIELD_DOCUMENT_COUNT = 'documentCount'
    FIELD_DATA_SOURCE_TYPE = 'datasourceType'
    FIELD_DATA_SOURCE_ID = 'seaDataSourceId'
    FIELD_PLAN_ID = 'planId'
    FIELD_DC_PLAN_ID = 'dcplanid'
    FIELD_PSEDUCO_CLIENT_ID = 'pseudoclientid'
    FIELD_SUBCLIENT_ID = 'subclientid'
    FIELD_CRAWL_TYPE = 'crawltype'
    FIELD_DATA_SOURCE_NAME_SEA = 'seaDataSourceName'
    FIELD_CONTENT_ID = 'contentid'
    FIELD_IS_FILE = 'IsFile:1'
    DYNAMIC_FEDERATED_SEARCH_PARAMS = {"searchParams": []}

    CRITERIA_EXTRACTED_DOCS = "entities_extracted:*"

    TAGGING_ITEMS_REQUEST = {
        "entityType": "SEA_DATASOURCE_ENTITY",
        "entityIds": [],
        "handler": "default",
        "searchRequest": {},
        "opType": "ADD",
        "tags": [],
        "isAsync": True}
    TAGGING_ITEMS_REVIEW_REQUEST = {"operation": ReviewActions.TAG.value, "files": "",
                                    "options": "",
                                    "taggingInformation": {'opType': 'ADD', "tagIds": []}}

    START_CRAWL_SERVER_REQUEST_JSON = {
        "taskInfo": {
            "associations": [
                {
                    "clientId": 0,
                    "_type_": 3
                }
            ],
            "task": {
                "taskType": 1,
                "taskName": "",
                "taskFlags": {
                    "isEdiscovery": True
                }
            },
            "subTasks": [
                {
                    "subTask": {
                        "subTaskName": "CVPYSDK_FSO_IMMEDIATE",
                        "subTaskType": 1,
                        "operationType": 5025
                    },
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


class InventoryConstants:
    """Class to maintain constants for inventory manager"""

    CRAWL_JOB_FAILED_STATE = [5, 6, 7, 8, 9, 10, 11, 12]

    CRAWL_JOB_COMPLETE_STATE = 4

    CRAWL_JOB_COMPLETE_ERROR_STATE = 13

    INVENTORY_ADD_REQUEST_JSON = {
        "name": "",
        "identityServers": [],
        "indexServer": {
            "cloudId": 0,
            "displayName": ""
        }
    }

    FIELD_PROPERTY_NAME = 'name'
    FIELD_PROPERTY_DNSHOST = 'hostName'
    FIELD_PROPERTY_OS = 'operatingSystem'
    FIELD_PROPERTY_IP = 'ipAddress'
    FIELD_PROPERTY_COUNTRYCODE = 'countryCode'

    KWARGS_NAME = 'name'
    KWARGS_IP = 'ip'
    KWARGS_OS = 'os'
    KWARGS_FQDN = 'fqdn'
    KWARGS_COUNTRY_CODE = 'country_code'

    FIELD_PROPS_MAPPING = {
        FIELD_PROPERTY_NAME: KWARGS_NAME,
        FIELD_PROPERTY_IP: KWARGS_IP,
        FIELD_PROPERTY_OS: KWARGS_OS,
        FIELD_PROPERTY_DNSHOST: KWARGS_FQDN,
        FIELD_PROPERTY_COUNTRYCODE: KWARGS_COUNTRY_CODE
    }

    ASSET_FILE_SERVER_PROPERTY = [
        FIELD_PROPERTY_NAME,
        FIELD_PROPERTY_DNSHOST,
        FIELD_PROPERTY_OS,
        FIELD_PROPERTY_IP,
        FIELD_PROPERTY_COUNTRYCODE
    ]

    IDENTITY_SERVER_ASSET_ADD_TO_INVENTORY_JSON = {"identityServers": [], "startDataCollection": True}

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
        """Asset type for inventory"""
        IDENTITY_SERVER = 61
        FILE_SERVER = 132


class PlanConstants:
    """Class to maintain constants related to DC plan activate operations"""

    INDEXING_ONLY_METADATA = 1
    INDEXING_METADATA_AND_CONTENT = 2

    DEFAULT_INCLUDE_DOC_TYPES = "*.doc,*.docx,*.xls,*.xlsx,*.ppt,*.pptx,*.msg,*.txt,*.rtf,*.eml,*.pdf,*.htm,*.html," \
                                "*.csv,*.log,*.ods,*.odt,*.odg,*.odp,*.dot,*.pages,*.xmind"
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
        },
        6: {
            "ciPolicyInfo": {
                "ciPolicy": {
                    "policyType": 5,
                    "detail": {
                        "ciPolicy": {
                            "opType": 2,
                            "enableExactSearch": False,
                            "ciPolicyType": 5,
                            "filters": {
                                "fileFilters": {
                                    "includeDocTypes": "",
                                    "minDocSize": 0,
                                    "maxDocSize": 50
                                }
                            }
                        }
                    }
                }
            },
            "eePolicyInfo": {},
            "exchange": {},
            "office365Info": {
                "o365Exchange": {
                    "mbArchiving": {
                        "policyType": 1,
                        "agentType": {
                            "appTypeId": 137
                        },
                        "detail": {
                            "emailPolicy": {
                                "emailPolicyType": 1,
                                "archivePolicy": {
                                    "primaryMailbox": True,
                                    "contentIndexProps": {}
                                }
                            }
                        }
                    }
                },
                "o365CloudOffice": {
                    "caBackup": {
                        "policyType": 6,
                        "detail": {
                            "cloudAppPolicy": {
                                "cloudAppPolicyType": 1,
                                "backupPolicy": {
                                    "onedrivebackupPolicy": {},
                                    "spbackupPolicy": {},
                                    "teamsbackupPolicy": {}
                                }
                            }
                        }

                    }

                }

            },

            "summary": {
                "plan": {
                    "planName": "",
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


class ComplianceConstants:
    """Class to maintain all the Compliance search related constants"""

    SOLR_FIELD_FILE_NAME = "fileName"
    SOLR_FIELD_SIZE = "sizeKB"

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

    DOWNLOAD_PERMISSION = {
        "_type_": 122,
        "permissionId": 36,
        "permissionName": "Download"
    }

    DELETE_PERMISSION = {
        "permissionId": 35,
        "permissionName": "Delete",
        "_type_": 122
    }

    PERMISSION_ADD_NAME = "Add"
    PERMISSION_DELETE_NAME = "Delete"
    PERMISSION_DOWNLOAD_NAME = "Download"
    PERMISSION_VIEW_NAME = "View"

    PERMISSIONS = {
        PERMISSION_ADD_NAME: ADD_PERMISSION,
        PERMISSION_DELETE_NAME: DELETE_PERMISSION,
        PERMISSION_DOWNLOAD_NAME: DOWNLOAD_PERMISSION,
        PERMISSION_VIEW_NAME: VIEW_PERMISSION
    }

    EXPORT_SET_SHARE_REQUEST_JSON = {
        "entityAssociated": {
            "entity": [
                {
                    "entityType": 9503,
                    "downloadSetId": None,
                    "_type_": 9503}
            ]
        },
        "securityAssociations": {
            "associationsOperationType": 2,
            "associations": [
                {
                    "userOrGroup": None,
                    "properties": {
                        "permissions": [
                            VIEW_PERMISSION,
                            DOWNLOAD_PERMISSION
                        ]
                    }
                }
            ]
        }
    }

    class AppTypes(Enum):
        EXCHANGE = "EXCHANGE"
        EXCHANGE_JOURNAL = "EXCHANGE_JOURNAL"
        SHAREPOINT = "SHAREPOINT"
        ONEDRIVE = "ONEDRIVE"
        TEAMS = "TEAMS"
        FILE_SYSTEM = "FILE_SYSTEM"

    class ExportTypes(Enum):
        CAB = "CAB"
        PST = "PST"

    RESTORE_TYPE = {
        ExportTypes.PST: 1,
        ExportTypes.CAB: 2
    }

    FILE_TYPE = "File"
    EMAIL_TYPE = "Email"
    FILE_TYPES = [AppTypes.FILE_SYSTEM, AppTypes.SHAREPOINT, AppTypes.ONEDRIVE, AppTypes.TEAMS]
    EMAIL_TYPES = [AppTypes.EXCHANGE, AppTypes.EXCHANGE_JOURNAL]

    FILE_FILTERS_KEY = "fileFilter"
    FILE_FILTERS = [
        {
            "filter": {
                "interFilterOP": "FTAnd",
                "filters": [
                    {
                        "field": "CISTATE",
                        "intraFieldOp": "FTOr",
                        "fieldValues": {
                            "values": [
                                "0",
                                "1",
                                "12",
                                "13",
                                "14",
                                "15",
                                "1014",
                                "3333",
                                "3334",
                                "3335"
                            ]
                        }
                    }
                ]
            }
        }
    ]

    EMAIL_FILTERS_KEY = "emailView"

    ONEDRIVE_FACET = "200118"
    TEAMS_FACET = "200128"
    SHAREPOINT_FACET = "78"
    CUSTOM_FACETS = {
        AppTypes.ONEDRIVE: ONEDRIVE_FACET,
        AppTypes.TEAMS: TEAMS_FACET,
        AppTypes.SHAREPOINT: SHAREPOINT_FACET
    }

    CUSTOM_FACETS_NAME = {
        AppTypes.TEAMS: "TEAMS_NAME",
        AppTypes.SHAREPOINT: "CUSTODIAN",
        AppTypes.ONEDRIVE: "CUSTODIAN"
    }

    FACET_KEY = "facetRequest"
    FILE_FACET = [
        {
            "count": 4,
            "name": "CUSTODIAN"
        },
        {
            "count": 4,
            "name": "APPTYPE",
            "searchFieldName": "APPTYPE",
            "stringParameter": [
                {
                    "name": "33",
                    "custom": True
                },
                {
                    "name": "29",
                    "custom": True
                },
                {
                    "name": "63",
                    "custom": True
                },
                {
                    "name": "21",
                    "custom": True
                }
            ]
        }
    ]
    CUSTOM_FACET = [
        {
            "count": 4,
            "name": "CUSTODIAN"
        },
        {
            "count": 4,
            "name": "APPTYPE",
            "searchFieldName": "APPTYPE",
            "stringParameter": [
                {
                    "name": None,
                    "custom": True
                }
            ]
        }
    ]

    RESPONSE_FIELD_LIST = ("DATA_TYPE,CLIENTNAME,CONTENTID,CV_OBJECT_GUID,PARENT_GUID,CV_TURBO_GUID,"
                           "AFILEID,AFILEOFFSET,COMMCELLNO,MODIFIEDTIME,SIZEINKB,BACKUPTIME,CISTATE,DATE_DELETED,"
                           "TEAMS_ITEM_ID,TEAMS_ITEM_NAME,TEAMS_NAME,TEAMS_SMTP,TEAMS_ITEM_TYPE,TEAMS_CHANNEL_TYPE,"
                           "TEAMS_TAB_TYPE,TEAMS_GROUP_VISIBILITY,TEAMS_GUID,TEAMS_CONV_ITEM_TYPE,"
                           "TEAMS_CONV_MESSAGE_TYPE,TEAMS_CONV_SUBJECT,TEAMS_CONV_IMPORTANCE,TEAMS_CONV_SENDER_TYPE,"
                           "TEAMS_CONV_SENDER_NAME,TEAMS_CONV_HAS_REPLIES,CI_URL,TEAMS_DRIVE_FOLDER_TYPE,APPTYPE,APPID")

    COMPLIANCE_SEARCH_JSON = {
        "mode": 2,
        "facetRequests": {},
        "advSearchGrp": {
            "commonFilter": [
                {
                    "filter": {
                        "filters": [
                            {
                                "field": "CI_STATUS",
                                "intraFieldOp": 0,
                                "fieldValues": {
                                    "values": [
                                        "1",
                                        "3"
                                    ]
                                }
                            }
                        ]
                    }
                }
            ],
            "cvSearchKeyword": {
                "isExactWordsOptionSelected": False,
                "keyword": None
            },
            "galaxyFilter": [
                {
                    "applicationType": None
                }
            ]
        },
        "userInformation": {
            "userGuid": None
        },
        "listOfCIServer": [
            {
                "cloudID": None
            }
        ],
        "searchProcessingInfo": {
            "resultOffset": 0,
            "pageSize": 50,
            "queryParams": [
                {
                    "param": "ENABLE_NEW_COMPLIANCE_SEARCH",
                    "value": "true"
                }
            ]
        }
    }
