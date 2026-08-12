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

"""Helper file to maintain all the constants for Google subclient.
"""

GMAIL_INDEX_APP_TYPE=200136

GDRIVE_INDEX_APP_TYPE=200137

GMAIL_DISCOVERY_TYPE=22

GDRIVE_DISCOVERY_TYPE=24

BROWSE_FIELD_FILTER_PAYLOAD = {
                "field": "",
                "fieldValues": {
                  "values": []
                }
              }

GMAIL_BROWSE_FIELD_RESPONSE_FIELD_PARAMS = ("COMMCELLNO,AFILEID,AFILEOFFSET,BACKUPTIME,SIZEINKB,MODIFIEDTIME,CONTENTID,LINKS,"
                                      "EMAIL_SUBJECT,FROM_DISPLAY,TO_DISPLAY,FOLDER,EMAIL_IMPORTANCE,CUSTODIAN,OWNER,"
                                      "DATA_TYPE,PARENT_GUID,CISTATE,EMAIL_ATTACHMENTS,HAS_ATTACHMENT,EMAIL_MODIFIED_TIME,"
                                      "IS_VISIBLE,CV_OBJECT_GUID,EMAIL_SMTPTO,EMAIL_SMTPFROM,GMAILV2_LABEL_ID")

GDRIVE_BROWSE_FIELD_RESPONSE_FIELD_PARAMS = ("FAST_URL,BACKUPTIME,SIZEINKB,MODIFIEDTIME,CONTENTID,CV_TURBO_GUID,AFILEID,"
                                             "AFILEOFFSET,COMMCELLNO,FILE_NAME,EXT_NAME,FILE_FOLDER,CVSTUB,DATA_TYPE,"
                                             "CISTATE,DATE_DELETED,CV_OBJECT_GUID,PARENT_GUID,CUSTODIAN,OWNER,"
                                             "GOOGLEDRIVE_SOURCE_TYPE,GOOGLEDRIVE_NODE_TYPE,ObjectType")

WEB_SEARCH_PAYLOAD = {
    "mode": 4,
    "advSearchGrp": {
      "emailFilter": [
        {
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
                "field": "DATA_TYPE",
                "intraFieldOp": 0,
                "fieldValues": {
                  "values": []
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
      ]
    },
    "searchProcessingInfo": {
      "resultOffset": 0,
      "pageSize": 0,
      "queryParams": [
        {
          "param": "ENABLE_MIXEDVIEW",
          "value": "true"
        },
        {
          "param": "RESPONSE_FIELD_LIST"
        }
      ]
    }
  }

GDRIVE_FOLDER_DOCUMENT_TYPE = 1
GMAIL_FOLDER_DOCUMENT_TYPE = 4
GMAIL_MAIL_DOCUMENT_TYPE = 2

GDRIVE_WEB_SEARCH_PAYLOAD = {
    "mode": 4,
    "advSearchGrp": {
        "commonFilter": [
            {
                "filter": {
                    "interFilterOP": 2,
                    "filters": [
                        {
                            "field": "CISTATE",
                            "fieldValues": {
                                "values": [
                                    "1"
                                ]
                            },
                            "intraFieldOp": 0
                        },
                        {
                            "field": "IS_VISIBLE",
                            "fieldValues": {
                                "values": [
                                    "true"
                                ]
                            },
                            "intraFieldOp": 0
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
                    "filters": []
                }
            }
        ],
        "emailFilter": [],
        "galaxyFilter": [
            {
                "appIdList": []
            }
        ]
    },
    "searchProcessingInfo": {
        "resultOffset": 0,
        "pageSize": 15,
        "queryParams": [{
            "param": "ENABLE_MIXEDVIEW",
            "value": "true"
        },
            {
                "param": "ENABLE_NAVIGATION",
                "value": "on"
            },
            {
                "param": "RESPONSE_FIELD_LIST",
                "value": "FAST_URL,BACKUPTIME,SIZEINKB,MODIFIEDTIME,CONTENTID,CV_TURBO_GUID,AFILEID,AFILEOFFSET,COMMCELLNO,FILE_NAME,EXT_NAME,FILE_FOLDER,CVSTUB,DATA_TYPE,CISTATE,DATE_DELETED,CV_OBJECT_GUID,PARENT_GUID,CUSTODIAN,OWNER,GOOGLEDRIVE_SOURCE_TYPE,GOOGLEDRIVE_NODE_TYPE,ObjectType"
            }]
    },
    "facetRequests": {
        "facetRequest": []
    }
}
