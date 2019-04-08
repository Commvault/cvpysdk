# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Helper file to maintain all the constants used in the SDK

HypervisorType          --  Enum which maintains the list of all the hypervisors supported by SDK

AppIDAType              --  Enum which maintains the list of all the IDA type values

InstanceBackupType      --  Enum for backup type for instance

SQLDefines              --  Class which maintains the defines list for SQL Server

AdvancedJobDetailType   --  Enum to maintain advanced job details info type

VSALiveSyncStatus       --  Enum to maintain status of the VSA Live sync

"""

from enum import Enum


class HypervisorType(Enum):
    """Class to maintain all the hypervisor related constants."""
    VIRTUAL_CENTER = "VMware"
    MS_VIRTUAL_SERVER = "Hyper-V"
    AZURE = "Azure"
    AZURE_V2 = "Azure Resource Manager"
    FUSION_COMPUTE = "FusionCompute"
    ORACLE_VM = "OracleVM"
    ALIBABA_CLOUD = "Alibaba Cloud"
    ORACLE_CLOUD = "Oracle Cloud"
    OPENSTACK = "OpenStack"
    GOOGLE_CLOUD = "Google Cloud Platform"
    Azure_Stack = "Azure Stack"
    Rhev = "Red Hat Virtualization"
    AMAZON_AWS = "Amazon"
    VCLOUD = "vCloud Director"
    Nutanix = "Nutanix AHV"
    ORACLE_CLOUD_INFRASTRUCTURE = "Oracle Cloud Infrastructure"


class AppIDAType(Enum):
    """Class to maintain all the app ida constants"""
    WINDOWS_FILE_SYSTEM = 33
    LINUX_FILE_SYSTEM = 29


class VSAObjects(Enum):
    """Mapping for VSA Objects."""
    SERVER = 1
    RESOURCE_POOL = 2
    VAPP = 3
    DATACENTER = 4
    FOLDER = 5
    CLUSTER = 6
    DATASTORE = 7
    DATASTORE_CLUSTER = 8
    VM = 9
    VMName = 10
    VMGuestOS = 11
    VMGuestHostName = 12
    ClusterSharedVolumes = 13
    LocalDisk = 14
    ClusterDisk = 15
    UnprotectedVMs = 16
    ROOT = 17
    FileServer = 18
    SMBShare = 19
    TypesFolder = 20
    VMFolder = 21
    ServerFolder = 22
    TemplateFolder = 23
    StorageRepositoryFolder = 24
    VAppFolder = 25
    DatacenterFolder = 26
    ClusterFolder = 27
    VMPowerState = 28
    VMNotes = 29
    VMCustomAttribute = 30
    Network = 31
    User = 32
    VMTemplate = 33
    Tag = 34
    TagCategory = 35
    Subclient = 36
    ClientGroup = 37
    ProtectionDomain = 38
    ConsistencyGroup = 39
    InstanceSize = 40
    Organization = 41


class InstanceBackupType(Enum):
    """Class to maintain type of instance backup"""
    FULL = 'full'
    INCREMENTAL = 'incremental'
    CUMULATIVE = 'incremental'      # cumulative backups pull incremental backup JSON


class SQLDefines:
    """Class to maintain SQL Defines"""

    # sql restore types
    DATABASE_RESTORE = 'DATABASE_RESTORE'
    STEP_RESTORE = 'STEP_RESTORE'
    RECOVER_ONLY = 'RECOVER_ONLY'

    # sql recovery types
    STATE_RECOVER = 'STATE_RECOVER'
    STATE_NORECOVER = 'STATE_NORECOVER'
    STATE_STANDBY = 'STATE_STANDBY'


class SharepointDefines:
    """Class to maintiain Sharepoint Defines"""

    # sharepoint strings
    CONTENT_WEBAPP = '\\MB\\Farm\\Microsoft SharePoint Foundation Web Application\\{0}'
    CONTENT_DB = '\\MB\\Farm\\Microsoft SharePoint Foundation Web Application\\{0}\\{1}'


class AdvancedJobDetailType(Enum):
    """Class to maintain advanced job details info type
    """

    RETENTION_INFO = 1
    REFERNCE_COPY_INFO = 2
    DASH_COPY_INFO = 4
    ADMIN_DATA_INFO = 8
    BKUP_INFO = 16


class VSALiveSyncStatus(Enum):
    """Class to maintain status of the VSA Live sync"""
    NEVER_HAS_BEEN_SYNCED = 0
    IN_SYNC = 1
    NEEDS_SYNC = 2
    SYNC_IN_PROGRESS = 3
    SYNC_PAUSED = 4
    SYNC_FAILED = 5
    SYNC_DISABLED = 6
    SYNC_ENABLED = 7
    VALIDATION_FAILED = 8
    SYNC_QUEUED = 9
    REVERT_FAILED = 10
    SYNC_STARTING = 11
