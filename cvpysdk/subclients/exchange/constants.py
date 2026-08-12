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

"""Helper file to maintain all the constants for MS Exchange subclient.

ExchangeConstants  -   Maintains constants for MS Exchange subclient.
"""
from enum import Enum

class ExchangeConstants:
    """
    Container for Exchange subclient-related constants.

    This class serves as a centralized location for storing and accessing
    constant values used throughout Exchange subclient operations. It is
    designed to improve maintainability and consistency by grouping all
    relevant constants in one place.

    Key Features:
        - Centralized management of Exchange subclient constants
        - Improves code readability and maintainability
        - Facilitates easy updates to constant values

    #ai-gen-doc
    """

    SEAARCH_PROCESSING_INFO = {
        "resultOffset": 0,
        "pageSize": 100,
        "queryParams": None,
        "sortParams": [
            {
                "sortDirection": 0, "sortField": "FROM_DISPLAY"
            }
        ]
    }

    ADVANCED_SEARCH_GROUP = {
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
                        },
                        {
                            "field": "IS_VISIBLE",
                            "intraFieldOp": 0,
                            "fieldValues": {
                                "values": [
                                    "true"
                                ]
                            }
                        }
                    ]
                }
            }
        ],
        "fileFilter": [],
        "emailFilter": [
            {
                "interGroupOP": 2,
                "filter": {
                    "interFilterOP": 2,
                    "filters": [
                        {
                            "field": "IS_VISIBLE",
                            "intraFieldOp": 0,
                            "fieldValues": {
                                "values": [
                                    "true"
                                ]
                            }
                        },
                        {
                            "field": "EXCH_VALID_AFID",
                            "intraFieldOp": 0,
                            "fieldValues": {
                                "values": [
                                    "true"
                                ]
                            }
                        },
                        {
                            "field": "DATA_TYPE",
                            "intraFieldOp": 0,
                            "fieldValues": {
                                "values": [
                                    "2"
                                ]
                            }
                        }

                    ]
                }
            }
        ],
        "galaxyFilter": [
            {
                "appIdList": None
            }
        ]
    }

    FIND_MAILBOX_REQUEST_DATA = {
        "mode": 4,
        "advSearchGrp": ADVANCED_SEARCH_GROUP,
        "searchProcessingInfo": SEAARCH_PROCESSING_INFO,
        "facetRequests": {
            "facetRequest": None
        }
    }

    FIND_MBX_QUERY_DEFAULT_PARAMS = {
        "RESPONSE_FIELD_LIST": "COMMCELLNO,AFILEID,AFILEOFFSET,BACKUPTIME,SIZEINKB,MODIFIEDTIME,"
                               "CONTENTID,LINKS,EMAIL_SUBJECT,FROM_DISPLAY,TO_DISPLAY,FOLDER,"
                               "EMAIL_IMPORTANCE,CUSTODIAN,OWNER,CVSTUB,DATA_TYPE,PARENT_GUID,"
                               "CISTATE,EMAIL_ATTACHMENTS,HAS_ATTACHMENT,EMAIL_MODIFIED_TIME,"
                               "IS_VISIBLE,EXCH_MIGRATED,EXCH_MBX_PROPERTY_TYPE,SRC_APP_GUID,"
                               "ExtractAttempt_i",
        "SHOW_EMAILS_ONLY": "true", "SUPPORT_SOLR_ONLY": "true", "ENABLE_FOLDERBROWSE": "off",
        "ENABLE_MIXEDVIEWSEARCH": "true"}

    FIND_MBX_DEFAULT_FACET = {"MODIFIEDTIME", "SIZEINKB", "FOLDER_PATH"}

    SEARCH_IN_RESTORE_PAYLOAD = {
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
                                    "values": ["1"]
                                }
                            },
                            {
                                "field": "IS_VISIBLE",
                                "intraFieldOp": 0,
                                "fieldValues": {
                                    "values": ["true"]
                                }
                            }
                        ]
                    }
                }
            ],
            "fileFilter": [],
            "emailFilter": [
                {
                    "interGroupOP": 2,
                    "filter": {
                        "interFilterOP": 2,
                        "filters": [
                            {
                                "field": "IS_VISIBLE",
                                "intraFieldOp": 0,
                                "fieldValues": {
                                    "values": ["true"]
                                }
                            },
                            {
                                "field": "EXCH_VALID_AFID",
                                "intraFieldOp": 0,
                                "fieldValues": {
                                    "values": ["true"]
                                }
                            },
                            {
                                "field": "DATA_TYPE",
                                "intraFieldOp": 0,
                                "fieldValues": {
                                    "values": ["2"]
                                }
                            }
                        ]
                    }
                }
            ],
            "galaxyFilter": [
                {
                    "appIdList": []
                }
            ],
            "cvSearchKeyword": {
                "isExactWordsOptionSelected": False,
                "keyword": ""
            }
        },
        "searchProcessingInfo": {
            "resultOffset": 0,
            "pageSize": 15,
            "queryParams": [
                {
                    "param": "RESPONSE_FIELD_LIST",
                    "value": "COMMCELLNO,AFILEID,AFILEOFFSET,BACKUPTIME,SIZEINKB,MODIFIEDTIME,CONTENTID,LINKS,EMAIL_SUBJECT,FROM_DISPLAY,TO_DISPLAY,FOLDER,EMAIL_IMPORTANCE,CUSTODIAN,OWNER,CVSTUB,DATA_TYPE,PARENT_GUID,CISTATE,EMAIL_ATTACHMENTS,HAS_ATTACHMENT,EMAIL_MODIFIED_TIME,IS_VISIBLE,EXCH_MIGRATED,EXCH_MBX_PROPERTY_TYPE,SRC_APP_GUID,ExtractAttempt_i"
                },
                {
                    "param": "DO_NOT_AUDIT",
                    "value": "false"
                },
                {
                    "param": "ENABLE_HIGHLIGHTING",
                    "value": "false"
                },
                {
                    "param": "SHOW_EMAILS_ONLY",
                    "value": "true"
                },
                {
                    "param": "ENABLE_DEFAULTFACETS",
                    "value": "false"
                },
                {
                    "param": "SUPPORT_SOLR_ONLY",
                    "value": "true"
                },
                {
                    "param": "ENABLE_FOLDERBROWSE",
                    "value": "off"
                },
                {
                    "param": "ENABLE_MIXEDVIEWSEARCH",
                    "value": "true"
                },
                {
                    "param": "ENABLE_NAVIGATION",
                    "value": "on"
                }
            ],
            "sortParams": [
                {
                    "sortDirection": 0,
                    "sortField": "EMAIL_SUBJECT"
                }
            ]
        },
        "facetRequests": {
            "facetRequest": [
                {"name": "MODIFIEDTIME"},
                {"name": "SIZEINKB"},
                {"name": "CUSTODIAN"},
                {"name": "HAS_ATTACHMENT"},
                {"name": "FOLDER_PATH"}
            ]
        }
    }

class JobOptionKeys(Enum):
    """
    Enumeration for specifying job option keys.

    This Enum class is used to define a set of constant keys that represent
    various job options within a system or application. It provides a
    type-safe way to refer to specific job configuration options, improving
    code readability and reducing the risk of errors due to string literals.

    Key Features:
        - Defines constant keys for job options
        - Ensures type safety and consistency in job configuration
        - Enhances code clarity and maintainability

    #ai-gen-doc
    """
    RESTORE_DESTINATION = "Restore destination"
    DESTINATION = "Destination"
    IF_MESSAGE_EXISTS = "If the message exists"
    INCLUDE_DELETED_ITEMS = "Include deleted items"
    MATCH_DESTINATION_USER = "Match destination user based on the email address"
    STUB_REHYDRATION = "Stub rehydration"
    STUB_REHYDRATION_OPTION = "Stub rehydration option"
    MAILBOX_LEVEL_REPORTING = "Mailbox level reporting"
    EMAIL_LEVEL_REPORTING = "Email level reporting"
    OLD_RECALL_LINK = "Old recall link"
    NEW_RECALL_LINK = "New recall link"
    EXCHANGE_RESTORE_CHOICE = "exchangeRestoreChoice"
    EXCHANGE_RESTORE_DRIVE = "exchangeRestoreDrive"
    IS_JOURNAL_REPORT = "isJournalReport"
    PST_FILE_PATH = "pstFilePath"
    TARGET_MAILBOX = "stubRehydration"
    STUB_REHYDRATION_SMALL = "stubRehydration"
    EXCH_STUB_REHYDRATION = "exchangeStubRehydrate"
    EXCH_STUB_REHYDRATION_OPTION = "exchangeStubRehydrationOption"

class JobOptionValues(Enum):
    """
    Enumeration for specifying job option values.

    This class defines a set of constant values representing different
    options that can be used to configure or control job-related behavior
    within an application. It inherits from Python's Enum, ensuring type
    safety and clarity when working with predefined job options.

    Key Features:
        - Provides a clear and type-safe way to represent job option values
        - Facilitates configuration and control of job-related settings
        - Inherits all standard Enum capabilities

    #ai-gen-doc
    """
    SKIP = "Skip"
    DISABLED = "Disabled"
    ENABLED = "Enabled"
    RECOVER_STUBS = "Recover stubs"
    STUB_REPORTING = "Stub reporting"
    UPDATE_RECALL_LINK = "Update recall link"
    EXCHANGE = "Exchange"
    ORIGINAL_LOCATION = "Original Location"

class JobOptionIntegers(Enum):
    """
    Enumeration for specifying job option integer values.

    This enum class is used to define a set of named integer constants
    that represent various job options within an application or system.
    It provides a type-safe way to work with predefined integer options,
    improving code readability and maintainability.

    Key Features:
        - Defines named integer constants for job options
        - Ensures type safety and clarity when handling job option values
        - Facilitates consistent usage of job option integers across the codebase

    #ai-gen-doc
    """
    EXCHANGE_RESTORE_CHOICE = 1
    EXCHANGE_RESTORE_DRIVE = 1
    RECOVER_STUBS = 0
    STUB_REPORTING = 1
    UPDATE_RECALL_LINK = 2