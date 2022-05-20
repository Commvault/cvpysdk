# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright 2020 Commvault Systems, Inc.
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

"""Helper file to maintain all the constants used in the SDK

TIMEZONES               --  Dict which maintains the list of all timezones

HypervisorType          --  Enum which maintains the list of all the hypervisors supported by SDK

AppIDAType              --  Enum which maintains the list of all the IDA type values

InstanceBackupType      --  Enum for backup type for instance

SQLDefines              --  Class which maintains the defines list for SQL Server

AdvancedJobDetailType   --  Enum to maintain advanced job details info type

VSALiveSyncStatus       --  Enum to maintain status of the VSA Live sync

VSAFailOverStatus       --  Enum to maintain Failover status of the VSA Live sync

ApplicationGroup        --  Enum to maintain Application Group Types.
"""

from enum import Enum, auto


TIMEZONES = {
    "Olson TZID": "Windows Timezone ID",
    "Pacific/Apia": "Samoa Standard Time",
    "Pacific/Midway": "Hawaiian Standard Time",
    "Pacific/Niue": "Samoa Standard Time",
    "Pacific/Pago_Pago": "Samoa Standard Time",
    "America/Adak": "Hawaiian Standard Time",
    "Pacific/Fakaofo": "Hawaiian Standard Time",
    "Pacific/Honolulu": "Hawaiian Standard Time",
    "Pacific/Johnston": "Hawaiian Standard Time",
    "Pacific/Rarotonga": "Hawaiian Standard Time",
    "Pacific/Tahiti": "Hawaiian Standard Time",
    "Pacific/Marquesas": "Hawaiian Standard Time",
    "America/Anchorage": "Alaskan Standard Time",
    "America/Juneau": "Alaskan Standard Time",
    "America/Nome": "Alaskan Standard Time",
    "America/Yakutat": "Alaskan Standard Time",
    "Pacific/Gambier": "Alaskan Standard Time",
    "America/Dawson": "Pacific Standard Time",
    "America/Los_Angeles": "Pacific Standard Time",
    "America/Santa_Isabel": "Pacific Standard Time (Mexico)",
    "America/Tijuana": "Pacific Standard Time (Mexico)",
    "America/Vancouver": "Pacific Standard Time",
    "America/Whitehorse": "Pacific Standard Time",
    "Pacific/Pitcairn": "Pacific Standard Time",
    "America/Boise": "Mountain Standard Time",
    "America/Cambridge_Bay": "Mountain Standard Time",
    "America/Chihuahua": "Mountain Standard Time (Mexico)",
    "America/Dawson_Creek": "Mountain Standard Time",
    "America/Denver": "Mountain Standard Time",
    "America/Edmonton": "Mountain Standard Time",
    "America/Hermosillo": "Mountain Standard Time",
    "America/Inuvik": "Mountain Standard Time",
    "America/Mazatlan": "Mountain Standard Time",
    "America/Ojinaga": "US Mountain Standard Time",
    "America/Phoenix": "US Mountain Standard Time",
    "America/Shiprock": "Mountain Standard Time",
    "America/Yellowknife": "Mountain Standard Time",
    "America/Belize": "Central America Standard Time",
    "America/Cancun": "Central Standard Time (Mexico)",
    "America/Chicago": "Central Standard Time",
    "America/Costa_Rica": "Central America Standard Time",
    "America/El_Salvador": "Central America Standard Time",
    "America/Guatemala": "Central America Standard Time",
    "America/Indiana/Knox": "Central Standard Time",
    "America/Indiana/Tell_City": "Central Standard Time",
    "America/Managua": "Central Standard Time",
    "America/Matamoros": "Central Standard Time",
    "America/Menominee": "Central Standard Time",
    "America/Merida": "Central Standard Time",
    "America/Mexico_City": "Central Standard Time (Mexico)",
    "America/Monterrey": "Central Standard Time (Mexico)",
    "America/North_Dakota/Center": "Central Standard Time",
    "America/North_Dakota/New_Salem": "Central Standard Time",
    "America/Rainy_River": "Central Standard Time",
    "America/Rankin_Inlet": "Central Standard Time",
    "America/Regina": "Central Standard Time",
    "America/Swift_Current": "Central Standard Time",
    "America/Tegucigalpa": "Central Standard Time",
    "America/Winnipeg": "Central Standard Time",
    "Pacific/Easter": "Central America Standard Time",
    "Pacific/Galapagos": "Central America Standard Time",
    "America/Atikokan": "Eastern Standard Time",
    "America/Bogota": "SA Pacific Standard Time",
    "America/Cayman": "Eastern Standard Time",
    "America/Detroit": "Eastern Standard Time",
    "America/Grand_Turk": "Eastern Standard Time",
    "America/Guayaquil": "Eastern Standard Time",
    "America/Havana": "SA Pacific Standard Time",
    "America/Indiana/Indianapolis": "US Eastern Standard Time",
    "America/Indiana/Marengo": "US Eastern Standard Time",
    "America/Indiana/Petersburg": "US Eastern Standard Time",
    "America/Indiana/Vevay": "US Eastern Standard Time",
    "America/Indiana/Vincennes": "US Eastern Standard Time",
    "America/Indiana/Winamac": "US Eastern Standard Time",
    "America/Iqaluit": "Eastern Standard Time",
    "America/Jamaica": "Eastern Standard Time",
    "America/Kentucky/Louisville": "Eastern Standard Time",
    "America/Kentucky/Monticello": "Eastern Standard Time",
    "America/Lima": "SA Pacific Standard Time",
    "America/Montreal": "Eastern Standard Time",
    "America/Nassau": "Eastern Standard Time",
    "America/New_York": "Eastern Standard Time",
    "America/Nipigon": "Eastern Standard Time",
    "America/Panama": "SA Pacific Standard Time",
    "America/Pangnirtung": "Eastern Standard Time",
    "America/Port-au-Prince": "Eastern Standard Time",
    "America/Resolute": "Eastern Standard Time",
    "America/Thunder_Bay": "Eastern Standard Time",
    "America/Toronto": "Eastern Standard Time",
    "America/Caracas": "Venezuela Standard Time",
    "America/Anguilla": "Pacific SA Standard Time",
    "America/Antigua": "Atlantic Standard Time",
    "America/Aruba": "Atlantic Standard Time",
    "America/Asuncion": "Paraguay Standard Time",
    "America/Barbados": "Pacific SA Standard Time",
    "America/Blanc-Sablon": "Atlantic Standard Time",
    "America/Boa_Vista": "Atlantic Standard Time",
    "America/Campo_Grande": "Atlantic Standard Time",
    "America/Cuiaba": "Central Brazilian Standard Time",
    "America/Curacao": "Central Brazilian Standard Time",
    "America/Dominica": "Pacific SA Standard Time",
    "America/Eirunepe": "Atlantic Standard Time",
    "America/Glace_Bay": "Atlantic Standard Time",
    "America/Goose_Bay": "Atlantic Standard Time",
    "America/Grenada": "Atlantic Standard Time",
    "America/Guadeloupe": "Atlantic Standard Time",
    "America/Guyana": "Atlantic Standard Time",
    "America/Halifax": "Atlantic Standard Time",
    "America/La_Paz": "SA Western Standard Time",
    "America/Manaus": "SA Western Standard Time",
    "America/Marigot": "Atlantic Standard Time",
    "America/Martinique": "Atlantic Standard Time",
    "America/Moncton": "Atlantic Standard Time",
    "America/Montserrat": "Atlantic Standard Time",
    "America/Port_of_Spain": "Atlantic Standard Time",
    "America/Porto_Velho": "Central Brazilian Standard Time",
    "America/Puerto_Rico": "Central Brazilian Standard Time",
    "America/Rio_Branco": "Central Brazilian Standard Time",
    "America/Santiago": "Pacific SA Standard Time",
    "America/Santo_Domingo": "Atlantic Standard Time",
    "America/St_Barthelemy": "Atlantic Standard Time",
    "America/St_Kitts": "Atlantic Standard Time",
    "America/St_Lucia": "Atlantic Standard Time",
    "America/St_Thomas": "Atlantic Standard Time",
    "America/St_Vincent": "Atlantic Standard Time",
    "America/Thule": "Atlantic Standard Time",
    "America/Tortola": "Atlantic Standard Time",
    "Antarctica/Palmer": "Atlantic Standard Time",
    "Atlantic/Bermuda": "Atlantic Standard Time",
    "America/St_Johns": "Newfoundland Standard Time",
    "America/Araguaina": "E. South America Standard Time",
    "America/Argentina/Buenos_Aires": "Argentina Standard Time",
    "America/Argentina/Catamarca": "Argentina Standard Time",
    "America/Argentina/Cordoba": "Argentina Standard Time",
    "America/Argentina/Jujuy": "Argentina Standard Time",
    "America/Argentina/La_Rioja": "Argentina Standard Time",
    "America/Argentina/Mendoza": "Argentina Standard Time",
    "America/Argentina/Rio_Gallegos": "Argentina Standard Time",
    "America/Argentina/Salta": "Argentina Standard Time",
    "America/Argentina/San_Juan": "Argentina Standard Time",
    "America/Argentina/San_Luis": "Argentina Standard Time",
    "America/Argentina/Tucuman": "Argentina Standard Time",
    "America/Argentina/Ushuaia": "Argentina Standard Time",
    "America/Bahia": "E. South America Standard Time",
    "America/Belem": "E. South America Standard Time",
    "America/Cayenne": "SA Eastern Standard Time",
    "America/Fortaleza": "SA Eastern Standard Time",
    "America/Godthab": "Greenland Standard Time",
    "America/Maceio": "E. South America Standard Time",
    "America/Miquelon": "E. South America Standard Time",
    "America/Montevideo": "Montevideo Standard Time",
    "America/Paramaribo": "SA Eastern Standard Time",
    "America/Recife": "SA Eastern Standard Time",
    "America/Santarem": "E. South America Standard Time",
    "America/Sao_Paulo": "E. South America Standard Time",
    "Antarctica/Rothera": "Argentina Standard Time",
    "Atlantic/Stanley": "Argentina Standard Time",
    "America/Noronha": "Mid-Atlantic Standard Time",
    "Atlantic/South_Georgia": "Mid-Atlantic Standard Time",
    "America/Scoresbysund": "Azores Standard Time",
    "Atlantic/Azores": "Azores Standard Time",
    "Atlantic/Cape_Verde": "Cape Verde Standard Time",
    "Africa/Abidjan": "GMT Standard Time",
    "Africa/Accra": "GMT Standard Time",
    "Africa/Bamako": "GMT Standard Time",
    "Africa/Banjul": "GMT Standard Time",
    "Africa/Bissau": "GMT Standard Time",
    "Africa/Casablanca": "Morocco Standard Time",
    "Africa/Conakry": "GMT Standard Time",
    "Africa/Dakar": "GMT Standard Time",
    "Africa/El_Aaiun": "GMT Standard Time",
    "Africa/Freetown": "GMT Standard Time",
    "Africa/Lome": "GMT Standard Time",
    "Africa/Monrovia": "GMT Standard Time",
    "Africa/Nouakchott": "GMT Standard Time",
    "Africa/Ouagadougou": "GMT Standard Time",
    "Africa/Sao_Tome": "GMT Standard Time",
    "America/Danmarkshavn": "GMT Standard Time",
    "Antarctica/Vostok": "GMT Standard Time",
    "Atlantic/Canary": "GMT Standard Time",
    "Atlantic/Faroe": "GMT Standard Time",
    "Atlantic/Madeira": "GMT Standard Time",
    "Atlantic/Reykjavik": "Greenwich Standard Time",
    "Atlantic/St_Helena": "Greenwich Standard Time",
    "Europe/Dublin": "GMT Standard Time",
    "Europe/Guernsey": "GMT Standard Time",
    "Europe/Isle_of_Man": "GMT Standard Time",
    "Europe/Jersey": "GMT Standard Time",
    "Europe/Lisbon": "GMT Standard Time",
    "Europe/London": "GMT Standard Time",
    "GMT": "GMT Standard Time",
    "UTC": "UTC",
    "Africa/Algiers": "W. Central Africa Standard Time",
    "Africa/Bangui": "W. Central Africa Standard Time",
    "Africa/Brazzaville": "W. Central Africa Standard Time",
    "Africa/Ceuta": "W. Central Africa Standard Time",
    "Africa/Douala": "W. Central Africa Standard Time",
    "Africa/Kinshasa": "W. Central Africa Standard Time",
    "Africa/Lagos": "W. Central Africa Standard Time",
    "Africa/Libreville": "W. Central Africa Standard Time",
    "Africa/Luanda": "W. Central Africa Standard Time",
    "Africa/Malabo": "W. Central Africa Standard Time",
    "Africa/Ndjamena": "W. Central Africa Standard Time",
    "Africa/Niamey": "W. Central Africa Standard Time",
    "Africa/Porto-Novo": "W. Central Africa Standard Time",
    "Africa/Tunis": "W. Central Africa Standard Time",
    "Africa/Windhoek": "Namibia Standard Time",
    "Arctic/Longyearbyen": "W. Europe Standard Time",
    "Europe/Amsterdam": "W. Europe Standard Time",
    "Europe/Andorra": "W. Europe Standard Time",
    "Europe/Belgrade": "Central Europe Standard Time",
    "Europe/Berlin": "W. Europe Standard Time",
    "Europe/Bratislava": "Central Europe Standard Time",
    "Europe/Brussels": "Romance Standard Time",
    "Europe/Budapest": "Central Europe Standard Time",
    "Europe/Copenhagen": "Romance Standard Time",
    "Europe/Gibraltar": "W. Europe Standard Time",
    "Europe/Ljubljana": "Central Europe Standard Time",
    "Europe/Luxembourg": "W. Europe Standard Time",
    "Europe/Madrid": "Romance Standard Time",
    "Europe/Malta": "W. Europe Standard Time",
    "Europe/Monaco": "W. Europe Standard Time",
    "Europe/Oslo": "W. Europe Standard Time",
    "Europe/Paris": "Romance Standard Time",
    "Europe/Podgorica": "W. Europe Standard Time",
    "Europe/Prague": "Central Europe Standard Time",
    "Europe/Rome": "W. Europe Standard Time",
    "Europe/San_Marino": "W. Europe Standard Time",
    "Europe/Sarajevo": "Central Europe Standard Time",
    "Europe/Skopje": "Central Europe Standard Time",
    "Europe/Stockholm": "W. Europe Standard Time",
    "Europe/Tirane": "W. Europe Standard Time",
    "Europe/Vaduz": "W. Europe Standard Time",
    "Europe/Vatican": "W. Europe Standard Time",
    "Europe/Vienna": "W. Europe Standard Time",
    "Europe/Warsaw": "Central Europe Standard Time",
    "Europe/Zagreb": "Central Europe Standard Time",
    "Europe/Zurich": "W. Europe Standard Time",
    "Africa/Blantyre": "South Africa Standard Time",
    "Africa/Bujumbura": "South Africa Standard Time",
    "Africa/Cairo": "Egypt Standard Time",
    "Africa/Gaborone": "South Africa Standard Time",
    "Africa/Harare": "South Africa Standard Time",
    "Africa/Johannesburg": "South Africa Standard Time",
    "Africa/Kigali": "South Africa Standard Time",
    "Africa/Lubumbashi": "South Africa Standard Time",
    "Africa/Lusaka": "South Africa Standard Time",
    "Africa/Maputo": "South Africa Standard Time",
    "Africa/Maseru": "South Africa Standard Time",
    "Africa/Mbabane": "South Africa Standard Time",
    "Africa/Tripoli": "Middle East Standard Time",
    "Asia/Amman": "Jordan Standard Time",
    "Asia/Beirut": "Middle East Standard Time",
    "Asia/Damascus": "Syria Standard Time",
    "Asia/Gaza": "Middle East Standard Time",
    "Asia/Jerusalem": "Israel Standard Time",
    "Asia/Nicosia": "GTB Standard Time",
    "Europe/Athens": "GTB Standard Time",
    "Europe/Bucharest": "GTB Standard Time",
    "Europe/Chisinau": "E. Europe Standard Time",
    "Europe/Helsinki": "FLE Standard Time",
    "Europe/Istanbul": "Turkey Standard Time",
    "Europe/Kiev": "E. Europe Standard Time",
    "Europe/Mariehamn": "E. Europe Standard Time",
    "Europe/Riga": "FLE Standard Time",
    "Europe/Simferopol": "E. Europe Standard Time",
    "Europe/Sofia": "FLE Standard Time",
    "Europe/Tallinn": "FLE Standard Time",
    "Europe/Uzhgorod": "E. Europe Standard Time",
    "Europe/Vilnius": "FLE Standard Time",
    "Europe/Zaporozhye": "E. Europe Standard Time",
    "Africa/Addis_Ababa": "E. Africa Standard Time",
    "Africa/Asmara": "E. Africa Standard Time",
    "Africa/Dar_es_Salaam": "E. Africa Standard Time",
    "Africa/Djibouti": "E. Africa Standard Time",
    "Africa/Juba": "E. Africa Standard Time",
    "Africa/Kampala": "E. Africa Standard Time",
    "Africa/Khartoum": "E. Africa Standard Time",
    "Africa/Mogadishu": "E. Africa Standard Time",
    "Africa/Nairobi": "E. Africa Standard Time",
    "Antarctica/Syowa": "Kaliningrad Standard Time",
    "Asia/Aden": "Kaliningrad Standard Time",
    "Asia/Baghdad": "Arabic Standard Time",
    "Asia/Bahrain": "Arabic Standard Time",
    "Asia/Kuwait": "Arab Standard Time",
    "Asia/Qatar": "Arab Standard Time",
    "Asia/Riyadh": "Arab Standard Time",
    "Europe/Kaliningrad": "Kaliningrad Standard Time",
    "Europe/Minsk": "Kaliningrad Standard Time",
    "Indian/Antananarivo": "Arab Standard Time",
    "Indian/Comoro": "Arab Standard Time",
    "Indian/Mayotte": "Arab Standard Time",
    "Asia/Tehran": "Iran Standard Time",
    "Asia/Baku": "Caucasus Standard Time",
    "Asia/Dubai": "Arabian Standard Time",
    "Asia/Muscat": "Arabian Standard Time",
    "Asia/Tbilisi": "Georgian Standard Time",
    "Asia/Yerevan": "Caucasus Standard Time",
    "Europe/Moscow": "Russian Standard Time",
    "Europe/Samara": "Russian Standard Time",
    "Europe/Volgograd": "Russian Standard Time",
    "Indian/Mahe": "Mauritius Standard Time",
    "Indian/Mauritius": "Mauritius Standard Time",
    "Indian/Reunion": "Mauritius Standard Time",
    "Asia/Kabul": "Afghanistan Standard Time",
    "Asia/Aqtau": "West Asia Standard Time",
    "Asia/Aqtobe": "West Asia Standard Time",
    "Asia/Ashgabat": "West Asia Standard Time",
    "Asia/Dushanbe": "West Asia Standard Time",
    "Asia/Karachi": "Pakistan Standard Time",
    "Asia/Oral": "West Asia Standard Time",
    "Asia/Samarkand": "West Asia Standard Time",
    "Asia/Tashkent": "West Asia Standard Time",
    "Indian/Kerguelen": "West Asia Standard Time",
    "Indian/Maldives": "West Asia Standard Time",
    "Asia/Colombo": "Sri Lanka Standard Time",
    "Asia/Kolkata": "India Standard Time",
    "Asia/Kathmandu": "Nepal Standard Time",
    "Antarctica/Mawson": "Central Asia Standard Time",
    "Asia/Almaty": "Central Asia Standard Time",
    "Asia/Bishkek": "Central Asia Standard Time",
    "Asia/Dhaka": "Bangladesh Standard Time",
    "Asia/Qyzylorda": "Central Asia Standard Time",
    "Asia/Thimphu": "Central Asia Standard Time",
    "Asia/Yekaterinburg": "Ekaterinburg Standard Time",
    "Indian/Chagos": "Central Asia Standard Time",
    "Asia/Rangoon": "Myanmar Standard Time",
    "Indian/Cocos": "Myanmar Standard Time",
    "Antarctica/Davis": "SE Asia Standard Time",
    "Asia/Bangkok": "SE Asia Standard Time",
    "Asia/Ho_Chi_Minh": "SE Asia Standard Time",
    "Asia/Hovd": "N. Central Asia Standard Time",
    "Asia/Jakarta": "SE Asia Standard Time",
    "Asia/Novokuznetsk": "N. Central Asia Standard Time",
    "Asia/Novosibirsk": "N. Central Asia Standard Time",
    "Asia/Omsk": "N. Central Asia Standard Time",
    "Asia/Phnom_Penh": "SE Asia Standard Time",
    "Asia/Pontianak": "SE Asia Standard Time",
    "Asia/Vientiane": "SE Asia Standard Time",
    "Indian/Christmas": "SE Asia Standard Time",
    "Antarctica/Casey": "W. Australia Standard Time",
    "Asia/Brunei": "North Asia Standard Time",
    "Asia/Choibalsan": "China Standard Time",
    "Asia/Chongqing": "China Standard Time",
    "Asia/Harbin": "China Standard Time",
    "Asia/Hong_Kong": "China Standard Time",
    "Asia/Kashgar": "North Asia Standard Time",
    "Asia/Krasnoyarsk": "North Asia Standard Time",
    "Asia/Kuala_Lumpur": "Singapore Standard Time",
    "Asia/Kuching": "North Asia Standard Time",
    "Asia/Macau": "North Asia Standard Time",
    "Asia/Makassar": "North Asia Standard Time",
    "Asia/Manila": "North Asia Standard Time",
    "Asia/Shanghai": "China Standard Time",
    "Asia/Singapore": "Singapore Standard Time",
    "Asia/Taipei": "Taipei Standard Time",
    "Asia/Ulaanbaatar": "Ulaanbaatar Standard Time",
    "Asia/Urumqi": "China Standard Time",
    "Australia/Perth": "W. Australia Standard Time",
    "Australia/Eucla": "W. Australia Standard Time",
    "Asia/Dili": "North Asia East Standard Time",
    "Asia/Irkutsk": "North Asia East Standard Time",
    "Asia/Jayapura": "North Asia East Standard Time",
    "Asia/Pyongyang": "Korea Standard Time",
    "Asia/Seoul": "Korea Standard Time",
    "Asia/Tokyo": "Tokyo Standard Time",
    "Pacific/Palau": "North Asia East Standard Time",
    "Australia/Adelaide": "Cen. Australia Standard Time",
    "Australia/Broken_Hill": "AUS Central Standard Time",
    "Australia/Darwin": "AUS Central Standard Time",
    "Antarctica/DumontDUrville": "E. Australia Standard Time",
    "Asia/Yakutsk": "Yakutsk Standard Time",
    "Australia/Brisbane": "E. Australia Standard Time",
    "Australia/Currie": "Tasmania Standard Time",
    "Australia/Hobart": "Tasmania Standard Time",
    "Australia/Lindeman": "E. Australia Standard Time",
    "Australia/Melbourne": "AUS Eastern Standard Time",
    "Australia/Sydney": "AUS Eastern Standard Time",
    "Pacific/Guam": "West Pacific Standard Time",
    "Pacific/Port_Moresby": "West Pacific Standard Time",
    "Pacific/Saipan": "West Pacific Standard Time",
    "Pacific/Truk": "West Pacific Standard Time",
    "Australia/Lord_Howe": "E. Australia Standard Time",
    "Asia/Sakhalin": "Vladivostok Standard Time",
    "Asia/Vladivostok": "Vladivostok Standard Time",
    "Pacific/Efate": "Central Pacific Standard Time",
    "Pacific/Guadalcanal": "Central Pacific Standard Time",
    "Pacific/Kosrae": "Central Pacific Standard Time",
    "Pacific/Noumea": "Central Pacific Standard Time",
    "Pacific/Ponape": "Central Pacific Standard Time",
    "Pacific/Norfolk": "Central Pacific Standard Time",
    "Antarctica/McMurdo": "UTC+12",
    "Antarctica/South_Pole": "UTC+12",
    "Asia/Anadyr": "Magadan Standard Time",
    "Asia/Kamchatka": "Magadan Standard Time",
    "Asia/Magadan": "Magadan Standard Time",
    "Pacific/Auckland": "New Zealand Standard Time",
    "Pacific/Fiji": "Fiji Standard Time",
    "Pacific/Funafuti": "Fiji Standard Time",
    "Pacific/Kwajalein": "Fiji Standard Time",
    "Pacific/Majuro": "Fiji Standard Time",
    "Pacific/Nauru": "Fiji Standard Time",
    "Pacific/Tarawa": "Fiji Standard Time",
    "Pacific/Wake": "Fiji Standard Time",
    "Pacific/Wallis": "Fiji Standard Time",
    "Pacific/Chatham": "Tonga Standard Time",
    "Pacific/Enderbury": "Tonga Standard Time",
    "Pacific/Tongatapu": "Tonga Standard Time",
    "Pacific/Kiritimati": "Tonga Standard Time"
}


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
    AMAZON_AWS = "Amazon Web Services"
    VCLOUD = "vCloud Director"
    Nutanix = "Nutanix AHV"
    ORACLE_CLOUD_INFRASTRUCTURE = "Oracle Cloud Infrastructure"
    OPENSHIFT = "Red Hat OpenShift"


class AppIDAType(Enum):
    """Class to maintain all the app ida constants"""
    WINDOWS_FILE_SYSTEM = 33
    LINUX_FILE_SYSTEM = 29
    CLOUD_APP = 134


class AppIDAName(Enum):
    """Class to maintain the app IDA names"""
    FILE_SYSTEM = 'File System'

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
    Selector = 47


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


class VSAFailOverStatus(Enum):
    """Class to maintain Failover status of the VSA Live sync"""
    NONE = 0
    FAILOVER_COMPLETE = 1
    FAILOVER_RUNNING = 2
    FAILOVER_PAUSED = 3
    FAILOVER_FAILED = 4
    FAILBACK_COMPLETE = 5
    FAILBACK_RUNNING = 6
    FAILBACK_PAUSED = 7
    FAILBACK_FAILED = 8
    FAILBACK_PARTIAL = 9
    FAILOVER_PARTIAL = 10


class ApplicationGroup(Enum):
    """Class to maintain application group types."""

    WINDOWS = 'APPGRP_WindowsFileSystemIDA'
    UNIX = auto()
    IBMi = auto()
    OPENVMS = auto()
    CLOUDAPPS = auto()
    MSSQLSERVER = auto()
    SHAREPOINTSERVER = auto()
