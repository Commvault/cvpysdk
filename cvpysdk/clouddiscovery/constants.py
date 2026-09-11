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
    GOOGLE_CLOUD_BIG_TABLE_DATABASE = 53
    GOOGLE_CLOUD_FIRE_STORE_DATABASE = 54
    GOOGLE_CLOUD_MEMORY_STORE_DATABASE = 55
    GOOGLE_CLOUD_KUBERNETES_ENGINE = 56
    GOOGLE_CLOUD_MEMORY_STORE_REDIS_INSTANCE = 67
    GOOGLE_CLOUD_MEMORY_STORE_REDIS_CLUSTER = 68
    GOOGLE_CLOUD_MEMORY_STORE_VALKEY = 69
    GOOGLE_CLOUD_MEMORY_STORE_MEMCACHED = 70
    GOOGLE_CLOUD_FILESTORE_FILESHARE = 71


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
    GCP_MANAGED = 3
    COMMVAULT_PROTECTED = 6


# Maps AssetProvider int value to the corresponding ProtectedBy int value
# used to identify natively-managed assets for that provider.
PROVIDER_PROTECTED_BY_MAP: dict = {
    1: AssetCVProtectedBY.AZURE_MANAGED,   # AZURE
    2: AssetCVProtectedBY.AWS_MANAGED,     # AWS
    3: AssetCVProtectedBY.GCP_MANAGED,     # GCP
}


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
PROVIDER = "Provider:1"
ASSET_SUB_TYPE = ("AssetSubType:0 OR AssetSubType:38 OR AssetSubType:39 OR AssetSubType:40 OR AssetSubType:41 OR"
                  " AssetSubType:42 OR AssetSubType:43 OR AssetSubType:48 OR AssetSubType:49 OR AssetSubType:50")
FACET_JSON = {
    "CloudConnectionName": {
        "field": "CloudConnectionName",
        "domain": {"excludeTags": ["tag_CloudConnectionName"]},
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms",
        "facet": {
            "Provider": {
                "field": "Provider",
                "domain": {"excludeTags": ["tag_Provider"]},
                "mincount": 1,
                "sort": {"count": "desc"},
                "type": "terms"
            }
        }
    },
    "CredentialName": {
        "field": "CredentialName",
        "domain": {"excludeTags": ["tag_CredentialName"]},
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms",
        "facet": {
            "Provider": {
                "field": "Provider",
                "domain": {"excludeTags": ["tag_Provider"]},
                "mincount": 1,
                
                "sort": {"count": "desc"},
                "type": "terms"
            }
        }
    },
    "WorkloadType": {
        "field": "WorkloadType",
        "domain": {"excludeTags": ["tag_WorkloadType"]},
        "mincount": 1,
        
        "sort": {"count": "desc"},
        "type": "terms",
        "facet": {
            "Total_Size": {
                "type": "query",
                "domain": {"excludeTags": ["tag_group_Total", "tag_Total"]},
                "minCount": 1,
                "q": "AssetSize:[* TO *]",
                "facet": {"Sum_Size": "sum(AssetSize)"}
            }
        }
    },
    "AssetType": {
        "field": "AssetType",
        "domain": {"excludeTags": ["tag_AssetType"]},
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "ProtectionStatus": {
        "field": "ProtectionStatus",
        "domain": {"excludeTags": ["tag_ProtectionStatus"]},
        "mincount": 1,
        
        "sort": {"count": "desc"},
        "type": "terms",
        "facet": {
            "ProtectedBy": {
                "field": "ProtectedBy",
                "domain": {"excludeTags": ["tag_ProtectedBy"]},
                "mincount": 1,
                "sort": {"count": "desc"},
                "type": "terms"
            }
        }
    },
    "AssetRegion": {
        "field": "AssetRegion",
        "domain": {"excludeTags": ["tag_AssetRegion"]},
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "SubscriptionName": {
        "field": "SubscriptionName",
        "domain": {"excludeTags": ["tag_SubscriptionName"]},
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "AssetGroup": {
        "field": "AssetGroup",
        "domain": {"excludeTags": ["tag_AssetGroup"]},
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "EntityTags": {
        "field": "EntityTags",
        "domain": {"excludeTags": ["tag_EntityTags"]},
        "mincount": 1,
        "sort": {"count": "desc"},
        "type": "terms"
    },
    "Total_Size": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_Total", "tag_Total"]},
        "minCount": 1,
        "q": "AssetSize:[* TO *]",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "ProtectionStatusSize_Protected": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_ProtectionStatusSize", "tag_ProtectionStatusSize"]},
        "minCount": 1,
        "q": "ProtectionStatus:4 AND ProtectedBy:6",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "ProtectionStatusSize_Configured": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_ProtectionStatusSize", "tag_ProtectionStatusSize"]},
        "minCount": 1,
        "q": "ProtectionStatus:6 AND ProtectedBy:6",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "ProtectionStatusSize_Managed": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_ProtectionStatusSize", "tag_ProtectionStatusSize"]},
        "minCount": 1,
        "q": "(ProtectionStatus:6 OR ProtectionStatus:4) AND ProtectedBy:1",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "ProtectionStatusSize_NotProtected": {
        "type": "query",
        "domain": {"excludeTags": ["tag_group_ProtectionStatusSize", "tag_ProtectionStatusSize"]},
        "minCount": 1,
        "q": "(ProtectionStatus:2 OR ProtectionStatus:5 OR ProtectionStatus:1)",
        "facet": {"Sum_Size": "sum(AssetSize)"}
    },
    "KubernetesWorkload": {
        "type": "query",
        "q": "(AssetType:3 OR AssetType:29)",
        "facet": {"Total_Size": "sum(AssetSize)"}
    },
    "VMWorkloadWithoutKubernetes": {
        "type": "query",
        "q": "(WorkloadType:1 AND -(AssetType:3 OR AssetType:29))",
        "facet": {"Total_Size": "sum(AssetSize)"}
    },
}

# Payloads

# ASSET_SEARCH_PAYLOAD — template payload for POST Asset/Search that returns
# the overview facets (counts and byte sums) without fetching individual docs.
ASSET_SEARCH_PAYLOAD: dict = {
    "searchParams": [
        {"key": "q",     "value": QUERY},
        {"key": "wt",    "value": RESPONSE_FORMAT},
        {"key": "start", "value": str(START)},
        {"key": "rows",  "value": "0"},
        {"key": "fq",    "value": ITEM_STATE},
        {"key": "fq",    "value": ASSET_SUB_TYPE},
    ]
}

# ---------------------------------------------------------------------------
# API response key constants (wire format)
# ---------------------------------------------------------------------------
NATIVE_TOTAL: str = "native_total"
"""Key for the estimated native-cloud (Azure/AWS) monthly backup cost."""
CV_TOTAL: str = "cv_total"
"""Key for the estimated Commvault monthly backup cost."""
SAVINGS_AMOUNT: str = "savings_amount"
"""Key for the absolute monthly saving (native_total - cv_total)."""
SAVINGS_PERCENT: str = "savings_percent"
"""Key for the relative monthly saving as a percentage."""

# ---------------------------------------------------------------------------
# Facet key constants (matching FACET_JSON keys)
# ---------------------------------------------------------------------------
TOTAL_SIZE: str = "Total_Size"
PROTECTION_STATUS_SIZE_PROTECTED: str = "ProtectionStatusSize_Protected"
PROTECTION_STATUS_SIZE_MANAGED: str = "ProtectionStatusSize_Managed"
PROTECTION_STATUS_SIZE_NOT_PROTECTED: str = "ProtectionStatusSize_NotProtected"
PROTECTION_STATUS_SIZE_CONFIGURED: str = "ProtectionStatusSize_Configured"
PROTECTION_STATUS_COUNT_MAP: str = "_protection_status_count"
WORKLOAD_TYPE_MAP: str = "WorkloadType"
KUBERNETES_WORKLOAD: str = "KubernetesWorkload"
VM_WORKLOAD_WITHOUT_KUBERNETES: str = "VMWorkloadWithoutKubernetes"

# ---------------------------------------------------------------------------
# TCO API request payload template
# ---------------------------------------------------------------------------
ASSET_TCO_PAYLOAD: dict = {
    "provider": "AZURE",
    "discoveredSizes": [],
    "retentions": [
        {"scope": "PRIMARY", "days": 30},
    ],
    "annualGrowthRate": 10,
    "dailyChangeRates": [
        {"workloadType": "COMPUTE",    "rate": "MEDIUM"},
        {"workloadType": "DATABASE",   "rate": "MEDIUM"},
        {"workloadType": "STORAGE",    "rate": "MEDIUM"},
        {"workloadType": "KUBERNETES", "rate": "MEDIUM"},
    ],
}

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
GCP = "googleCloud"

# GCP Connection Payload Template
GCP_CONNECTION_PAYLOAD = {
    "name": None,
    "startDiscoveryJob": False,
    "cloudType": "googleCloud",
    "credentials": {"credentialId": None},
    "cloudSpecificConfiguration": {
        "googleCloud": {
            "projects": [],
            "discoverAllProjects": True
        }
    }
}

# GCP Validate Credential Payload Template
GCP_VALIDATE_CREDENTIAL_PAYLOAD = {
    "cloudType": "googleCloud",
    "credentials": {"credentialId": None},
    "cloudSpecificConfiguration": {
        "googleCloud": {
            "isCustomConfig": True
        }
    }
}
