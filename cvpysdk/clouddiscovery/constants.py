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

"""Constants and Enums for Cloud Discovery module."""

from enum import Enum, IntEnum


class AssetProvider(IntEnum):
    """Enumeration for different asset providers."""

    NONE = 0
    AZURE = 1
    AWS = 2
    GCP = 3
    M365 = 4
    LOCAL = 5
    COMMVAULT = 6


class WorkloadType(IntEnum):
    """Enumeration for different workload types."""

    NONE = 0
    COMPUTE = 1
    STORAGE = 2
    DATABASE = 3
    SECURITY = 4
    APPLICATION = 5
    EFS = 7


class AssetType(IntEnum):
    """Enumeration for different asset types across cloud providers."""

    NONE = 0

    # Azure Assets
    AZURE_VIRTUAL_MACHINE = 1
    AZURE_VM_SCALE_SET = 2
    AZURE_KUBERNETES_SERVICE = 3
    AZURE_STORAGE_ACCOUNT = 4
    AZURE_BLOB_STORAGE = 5
    AZURE_FILE_STORAGE = 6
    AZURE_QUEUE_STORAGE = 7
    AZURE_TABLE_STORAGE = 8
    AZURE_COSMOS_DB_ACCOUNT = 9
    AZURE_COSMOS_DB_SQL_ACCOUNT = 10
    AZURE_COSMOS_DB_MONGODB_RU_ACCOUNT = 11
    AZURE_COSMOS_DB_CASSANDRA_RU_ACCOUNT = 12
    AZURE_COSMOS_DB_GREMLIN_ACCOUNT = 13
    AZURE_COSMOS_DB_TABLE_ACCOUNT = 14
    AZURE_SQL_DATABASE = 15
    AZURE_POSTGRESQL_SERVER = 16
    AZURE_MYSQL_SERVER = 17
    AZURE_MYSQL_SERVER_FLEXIBLE = 18
    AZURE_POSTGRESQL_SERVER_FLEXIBLE = 19
    AZURE_DATA_LAKE_STORAGE = 37

    # Amazon AWS Assets
    AMAZON_EC2_VIRTUAL_MACHINE = 20
    AMAZON_S3_STORAGE = 21
    AMAZON_RDS = 22
    AMAZON_DYNAMO_DB = 23
    AMAZON_DOCUMENT_DB = 24
    AMAZON_ELASTIC_KUBERNETES_SERVICE = 29
    AMAZON_FSX_FILE_SYSTEM = 30
    AMAZON_RDS_MARIA_DB = 38
    AMAZON_RDS_MYSQL_DB = 39
    AMAZON_RDS_SQL_SERVER_DB = 40
    AMAZON_RDS_POSTGRESQL_DB = 41
    AMAZON_AURORA_MYSQL_DB = 42
    AMAZON_AURORA_POSTGRESQL_DB = 43
    AMAZON_REDSHIFT = 44
    AMAZON_RDS_ORACLE_DB = 45
    AMAZON_RDS_DB2_DB = 46
    AMAZON_ELASTIC_FILE_SYSTEM = 47

    # Microsoft 365 Assets
    M365_ONEDRIVE_APP = 25
    M365_EXCHANGE_APP = 26
    M365_TEAMS_APP = 27
    M365_SHAREPOINT_APP = 28

    # Google Cloud Platform Assets
    GOOGLE_CLOUD_VIRTUAL_MACHINE = 31
    GOOGLE_CLOUD_SQL_DATABASE = 32
    GOOGLE_CLOUD_BIG_QUERY_DATABASE = 33
    GOOGLE_CLOUD_ALLOY_DB_DATABASE = 34
    GOOGLE_CLOUD_FILE_STORAGE = 35
    GOOGLE_CLOUD_CLOUD_SPANNER = 36
    GOOGLE_CLOUD_MYSQL_DATABASE = 48
    GOOGLE_CLOUD_SQL_SERVER_DATABASE = 49
    GOOGLE_CLOUD_POSTGRESQL_DATABASE = 50


class AssetCVProtectionStatus(IntEnum):
    """Enumeration for Commvault protection status of assets."""

    NONE = 0
    NOT_AVAILABLE = 1
    NOT_PROTECTED = 2
    PROTECTION_CONFIGURED = 3
    PROTECTED = 4
    PROTECTION_FAILED = 5
    PROTECTION_CONFIGURED_COMMVAULT = 6


class AssetCVProtectedBY(IntEnum):
    """Enumeration for Commvault protection status of assets."""

    AZURE_MANAGED = 1
    AWS_MANAGED = 2
    COMMVAULT_PROTECTED = 6


class AzureConfigType(IntEnum):
    """Enumeration for different Azure configuration types."""

    EXPRESS = 0
    CUSTOM = 1


# Constants for Discovery payload
QUERY = "*:*"
RESPONSE_FORMAT = "json"
START = 0
ROWS = 100
ITEM_STATE = "ItemState:1"
ASSET_SUB_TYPE = ("AssetSubType:0 OR AssetSubType:38 OR AssetSubType:39 OR AssetSubType:40 OR AssetSubType:41 OR"
                  " AssetSubType:42 OR AssetSubType:43")
FILTER_QUERY = "Provider:1"
FACET_JSON = {
    "CredentialName": {
        "field": "CredentialName",
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms",
        "facet": {
            "Provider": {
                "field": "Provider",
                "mincount": 1,
                "limit": 50,
                "sort": {"count": "desc"},
                "type": "terms"
            }
        }
    },
    "WorkloadType": {
        "field": "WorkloadType",
        "mincount": 1,
        "limit": 50,
        "sort": {"count": "desc"},
        "type": "terms",
        "facet": {
            "Total_Size": {
                "type": "query",
                "domain": {"excludeTags": ["tag_group_Total"]},
                "minCount": 1,
                "q": "AssetSize:[* TO *]",
                "facet": {"Sum_Size": "sum(AssetSize)"}
            }
        }
    },
    "AssetType": {
        "field": "AssetType",
        "mincount": 1,
        "limit": 50,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "ProtectionStatus": {
        "field": "ProtectionStatus",
        "mincount": 1,
        "limit": 50,
        "sort": {"count": "desc"},
        "type": "terms",
        "facet": {
            "ProtectedBy": {
                "field": "ProtectedBy",
                "mincount": 1,
                "limit": 50,
                "sort": {"count": "desc"},
                "type": "terms"
            }
        }
    },
    "AssetRegion": {
        "field": "AssetRegion",
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "SubscriptionName": {
        "field": "SubscriptionName",
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "AssetGroup": {
        "field": "AssetGroup",
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "EntityTags": {
        "field": "EntityTags",
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "Total_Size": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_Total"]},
        "minCount": 1,
        "q": "AssetSize:[* TO *]",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "ProtectionStatusSize_Protected": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_ProtectionStatusSize"]},
        "minCount": 1,
        "q": "ProtectionStatus:4 AND ProtectedBy:6",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "ProtectionStatusSize_Managed": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_ProtectionStatusSize"]},
        "minCount": 1,
        "q": "ProtectionStatus:4 AND !ProtectedBy:6",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "ProtectionStatusSize_NotProtected": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_ProtectionStatusSize"]},
        "minCount": 1,
        "q": "(ProtectionStatus:2 OR ProtectionStatus:5 OR ProtectionStatus:1)",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    }
}

# Payloads

AWS_EXPRESS_CONNECTION_PAYLOAD = {
    "cloudType": "aws",
    "connectionType": None,
    "cloudSpecificConfiguration": {
        "aws": {
            "regions": "default",
            "iamRoleAccountId": None
        }
    }
}

AZURE_EXPRESS_CONNECTION_PAYLOAD = {
    "name": None,
    "startDiscoveryJob": False,
    "cloudType": "azure",
    "credentials": {"credentialId": None},
    "cloudSpecificConfiguration": {
        "azure": {

            "environment": "AzureCloud",
            "discoverAllSubscription": False,
        }
    }
}


# Constants for AWS Cloud Connection

AWS_CLOUD_CONNECTION_CRED = "cloud-connection-%s-credential"
AWS_CONNECTION_TYPE_ORG = "OrganizationLevel"
AWS_CONNECTION_TYPE_SINGLE = "CloudAccountLevel"
AZURE_CUSTOM = "azure_custom"
AZURE_EXPRESS = "azure_express"
AZURE = "azure"
AWS = "aws"
