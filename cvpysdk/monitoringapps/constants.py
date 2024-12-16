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

"""Helper file to maintain all the constants for threat indicators

ThreatConstants         --  class to maintains constants for Threat scan and threat analysis

FileTypeConstants       --  class to maintain constants for file type anomalies

RequestConstants        --  class to maintain request json for threat indicators related operations

"""


class ThreatConstants:
    """class to maintains constants for Threat scan and threat analysis"""
    FIELD_INFECTED_COUNT = 'infectedFilesCount'
    FIELD_FINGERPRINT_COUNT = 'fingerPrintFilesCount'
    FIELD_DATASOURCE_ID = 'dataSourceId'


class FileTypeConstants:
    """class to maintain constants for file type anomalies"""
    FIELD_DELETE_COUNT = 'deleteCount'
    FIELD_RENAME_COUNT = 'renameCount'
    FIELD_CREATE_COUNT = 'createCount'
    FIELD_MODIFIED_COUNT = 'modCount'


class RequestConstants:
    """class to maintain request json for threat indicator related operations"""
    CLEAR_ANOMALY_JSON = {"clients": [{"_type_": "CLIENT_ENTITY",
                                       "clientId": 0,
                                       "displayName": "",
                                       "dataSourceId": 0,
                                       "selected": True}],
                          "anomalyTypes": []}

    RUN_SCAN_JSON = {"client": {
        "clientId": 0},
        "timeRange": {"fromTime": 0, "toTime": 0},
        "threatAnalysisFlags": 0,
        "indexServer": {"clientId": 0},
        "backupDetails": [{"copyId": 0, "storagePoolId": 0}]}
