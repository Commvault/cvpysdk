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
    COMMSERVE = 1020
    CASSANDRA = 1211
    CLOUD_APPS = 1140
    DOMINO_DATABASE = 1051
    FILE_SYSTEM = 1101
    FILE_SYSTEM_CORE = 1002
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
    CONTENT_ANALYZER = 1108
    DB2_AGENT = 1207
    INFORMIX = 1201
    SYBASE = 1202


class WindowsDownloadFeatures(Enum):
    """
    list of Windows features supported
    """
    COMMSERVE = 20
    ACTIVE_DIRECTORY = 703
    CLOUD_APPS = 730
    DOMINO_DATABASE = 201
    EXCHANGE = 151
    FILE_SYSTEM = 702
    FILE_SYSTEM_CORE = 1
    MEDIA_AGENT = 51
    SHAREPOINT = 101
    ORACLE = 352
    POSTGRESQL = 362
    SQLSERVER = 353
    VIRTUAL_SERVER = 713
    VSS_PROVIDER = 453
    VSS_HARDWARE_PROVIDER = 455
    WEB_CONSOLE = 726
    TEST_AUTOMATION = 719
    PYTHON_SDK = 754
    COMMSERVE_LITE = 25
    CONTENT_ANALYZER = 729
    INDEX_STORE = 55
    INDEX_GATEWAY = 263
    CONTENT_EXTRACTOR = 259
    DB2_AGENT = 351
    INFORMIX = 360
    SYBASE = 1202
    WEB_SERVER = 252


class OSNameIDMapping(Enum):
    """
    Class for os name to id mapping
    """
    WINDOWS_32 = 1
    WINDOWS_64 = 3
    UNIX_AIX = 14
    UNIX_AIX32 = 28
    UNIX_FREEBSD86 = 25
    UNIX_FREEBSD64 = 26
    UNIX_HP = 20
    UNIX_LINUX86 = 15
    UNIX_LINUX64 = 16
    UNIX_S390 = 18
    UNIX_S390_31 = 29
    UNIX_PPC64 = 17
    UNIX_SOLARIS86 = 31
    UNIX_SOLARIS64 = 23
    UNIX_SOLARIS_SPARC = 22
    UNIX_SOLARIS_SPARC86 = 30
    UNIX_LINUX64LE = 32

class InstallUpdateOptions(Enum):
    """
    Enum with list of all options available under Upgrade software
    """
    UPDATE_INSTALL_CV = 1
    UPDATE_INSTALL_SQL = 2
    UPDATE_INSTALL_WINOS = 4
    UPDATE_INSTALL_FREL_OS_UPDATES = 8
    UPDATE_INSTALL_HYPERSCALE_OS_UPDATES = 16
    UPDATE_INSTALL_HSX_STORAGE_UPDATES = 32
    UPDATE_INSTALL_HSX_STORAGE_UPDATES_DISRUPTIVE_MODE = 64
