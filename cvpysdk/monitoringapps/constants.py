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
    """
    Class for maintaining constants related to threat scanning and analysis.

    This class serves as a centralized repository for constants used in threat
    detection, scanning, and analysis processes. It is intended to provide
    consistent and reusable values across different components of a threat
    management system.

    Key Features:
        - Centralized management of threat-related constants
        - Facilitates consistency in threat scan and analysis operations

    #ai-gen-doc
    """
    FIELD_INFECTED_COUNT = 'infectedFilesCount'
    FIELD_FINGERPRINT_COUNT = 'fingerPrintFilesCount'
    FIELD_DATASOURCE_ID = 'dataSourceId'


class FileTypeConstants:
    """
    Class to maintain constants related to file type anomalies.

    This class serves as a centralized location for storing constant values
    that represent various file type anomalies. It is intended to be used
    throughout the codebase wherever file type anomaly constants are required,
    promoting consistency and maintainability.

    Key Features:
        - Centralized management of file type anomaly constants
        - Improves code readability and maintainability
        - Facilitates easy updates to anomaly-related constants

    #ai-gen-doc
    """
    FIELD_DELETE_COUNT = 'deleteCount'
    FIELD_RENAME_COUNT = 'renameCount'
    FIELD_CREATE_COUNT = 'createCount'
    FIELD_MODIFIED_COUNT = 'modCount'


class RequestConstants:
    """
    Class to maintain constants related to request JSON structures for threat indicator operations.

    This class serves as a centralized location for storing and managing constants that define
    the structure and keys used in JSON requests pertaining to threat indicator-related processes.
    It is intended to promote consistency and reusability across the codebase when handling
    threat indicator requests.

    Key Features:
        - Centralized management of request JSON constants
        - Ensures consistency in threat indicator operations
        - Facilitates maintainability and readability

    #ai-gen-doc
    """
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