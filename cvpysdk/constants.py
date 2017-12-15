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

"""

from enum import Enum


class HypervisorType(Enum):
    """Class to maintain all the hypervisor related constants."""
    VIRTUAL_CENTER = "VMware"
    MS_VIRTUAL_SERVER = "Hyper-V"
    AZURE = "Azure"
    AZURE_V2 = "Azure Resource Manager"


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
    VM = 10
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
    CUMULATIVE = 'incremental'  # cumulative backups pull incremental backup JSON
