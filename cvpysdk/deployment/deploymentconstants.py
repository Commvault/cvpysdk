# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File that contains list of constants used by Deployment package
"""

from enum import Enum


class DownloadOptions(Enum):
    """
    Enum with list of all options available under Download software
    """
    LATEST_SERVICEPACK = "latest service pack"
    LATEST_HOTFIXES = "latest hotfixes for the installed service pack"
    SERVICEPACK_AND_HOTFIXES = "service pack and hotfixes"


class DownloadPackages(Enum):
    """
    List of supported OS groups.
    """
    WINDOWS_32 = "Windows(32)"
    WINDOWS_64 = "Windows(X64)"
    UNIX_AIX = "Aix PPC"
    UNIX_AIX32 = "Aix-PPC-32"
    UNIX_MAC = "macOS"
    UNIX_FREEBSD86 = "Freebsd X86"
    UNIX_FREEBSD64 = "Freebsd X86_64"
    UNIX_HP = "HP IA64"
    UNIX_LINUX86 = "Linux X86"
    UNIX_LINUX64 = "Linux X86_64"
    UNIX_S390 = "Linux-S390"
    UNIX_S390_31 = "Linux-S390-31"
    UNIX_PPC64 = "Linux-PPC-64"
    UNIX_SOLARIS86 = "Solaris X86"
    UNIX_SOLARIS64 = "Solaris X86_64"
    UNIX_SOLARIS_SPARC = "Solaris SPARC"
    UNIX_SOLARIS_SPARC86 = "Solaris-SPARC-X86"
    UNIX_LINUX64LE = "Linux PPC64le"


class UnixDownloadFeatures(Enum):
    """
    list of Unix features supported
    """
    CASSANDRA = 1211
    CLOUD_APPS = 1140
    DOMINO_DATABASE = 1051
    FILE_SYSTEM = 1101
    FILE_SYSTEM_FOR_IBMI = 1137
    FILE_SYSTEM_FOR_OPEN_VMS = 1138
    MEDIA_AGENT = 1301
    ORACLE = 1204
    POSTGRESQL = 1209
    SAPHANA = 1210
    SQLSERVER = 1212
    VIRTUAL_SERVER = 1136
    TEST_AUTOMATION = 1153
    PYTHON_SDK = 1154


class WindowsDownloadFeatures(Enum):
    """
    list of Windows features supported
    """
    ACTIVE_DIRECTORY = 703
    CLOUD_APPS = 730
    DOMINO_DATABASE = 201
    EXCHANGE = 151
    FILE_SYSTEM = 702
    MEDIA_AGENT = 51
    SHAREPOINT = 101
    ORACLE = 352
    POSTGRESQL = 362
    SQLSERVER = 353
    VIRTUAL_SERVER = 713
    VSS_PROVIDER = 453
    WEB_CONSOLE = 726
    TEST_AUTOMATION = 719
    PYTHON_SDK = 754

