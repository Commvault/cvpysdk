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

"""Helper file to maintain all the constants for index server and datacube

IndexServerConstants            -       Maintains constants for index server

ContentAnalyzerConstants        -       Maintains constants for Content Analyzer

"""


class IndexServerConstants:
    """Class to maintain all the index server related constants"""

    INDEX_SERVER_IDA_NAME = "Big Data Apps"
    INDEX_SERVER_INSTANCE_NAME = "dynamicIndexInstance"

    ROLE_DATA_ANALYTICS = "Data Analytics"
    ROLE_FILE_SYSTEM_INDEX = "FileSystem Index"
    ROLE_EXCHANGE_INDEX = "Exchange Index"
    ROLE_ONEDRIVE_INDEX = "OneDrive Index"
    ROLE_SYSTEM_DEFAULT = "System Default"

    ENGINE_NAME = "engineName"
    CLOUD_ID = "cloudID"
    ROLES = "version"
    HOST_NAME = "hostName"
    CLOUD_NAME = 'internalCloudName'
    CLIENT_NAME = 'clientName'
    CI_SERVER_URL = 'cIServerURL'
    TYPE = 'type'
    BASE_PORT = 'basePort'
    CLIENT_ID = 'clientId'
    SERVER_TYPE = 'serverType'
    INDEX_SERVER_CLIENT_ID = 'indexServerClientId'

    FSINDEX = 'fsindex_'
    MULTINODE = '_multinode'

    OPERATION_ADD = 1
    OPERATION_DELETE = 2
    OPERATION_EDIT = 3

    DEFAULT_JVM_MAX_MEMORY = '8191'
    DEFAULT_SOLR_PORT = '20000'

    SOLR_PORT_META_INFO = {
        "name": "PORTNO",
        "value": DEFAULT_SOLR_PORT
    }
    SOLR_JVM_META_INFO = {
        "name": "JVMMAXMEMORY",
        "value": DEFAULT_JVM_MAX_MEMORY
    }

    UPDATE_ADD_ROLE = {
        "roleName": "",
        "operationType": OPERATION_ADD}

    REQUEST_JSON = {
        "opType": OPERATION_ADD,
        "type": 1,
        "configureNodes": True,
        "solrCloudInfo": {
            "roles": []
        },
        "cloudNodes": [],
        "cloudInfoEntity": {},
        "cloudMetaInfos": []

    }

    PRUNE_REQUEST_JSON = {
        "forceDelete": False,
        "datasourceId": 0,
        "collectionProperty": {
            "nameValues": [
                {
                    "name": "PruneAllDataSources",
                    "value": "true"
                }
            ]
        }
    }


class ContentAnalyzerConstants:
    """Class to maintain all the content analyzer cloud related constants"""

    OPERATION_ADD = 1
    OPERATION_DELETE = 2
    OPERATION_EDIT = 3

    REQUEST_JSON = {
        "opType": OPERATION_ADD,
        "type": 2,
        "configureNodes": True,
        "cloudNodes": [],
        "cloudInfoEntity": {},
    }
