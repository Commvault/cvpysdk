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
    """Class to maintain all the Exchange subclient related constants."""

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
    """Enum to specify job option keys"""
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

class JobOptionValues(Enum):
    """Enum to specify job option values"""
    SKIP = "Skip"
    DISABLED = "Disabled"
    ENABLED = "Enabled"
    RECOVER_STUBS = "Recover stubs"
    STUB_REPORTING = "Stub reporting"
    UPDATE_RECALL_LINK = "Update recall link"
    EXCHANGE = "Exchange"
    ORIGINAL_LOCATION = "Original Location"

class JobOptionIntegers(Enum):
    """Enum to specify job option integers"""
    EXCHANGE_RESTORE_CHOICE = 1
    EXCHANGE_RESTORE_DRIVE = 1
    RECOVER_STUBS = 0
    STUB_REPORTING = 1
    UPDATE_RECALL_LINK = 2


