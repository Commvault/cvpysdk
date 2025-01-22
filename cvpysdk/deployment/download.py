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

"""" Main file for performing the download operation

Download
========

    __init__(commcell_object)             --  initialize commcell_object of Download class
    associated with the commcell

    download_software()                   --  downloads software packages in the commcell

    sync_remote_cache()                   --  syncs remote cache

"""

from ..job import Job
from ..exception import SDKException
from .deploymentconstants import DownloadOptions
from cvpysdk.schedules import Schedules, SchedulePattern


class Download(object):
    """"class for downloading software packages"""

    def __init__(self, commcell_object):
        """Initialize commcell_object of the Download class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Download class

        """

        self.commcell_object = commcell_object
        self._services = commcell_object._services
        self._cvpysdkcommcell_object = commcell_object._cvpysdk_object
        self.update_option = {}

    def download_software(
            self,
            options=None,
            os_list=None,
            service_pack=None,
            cu_number=0,
            sync_cache=True,
            sync_cache_list=None,
            schedule_pattern=None):
        """Downloads the os packages on the commcell

            Args:

                options      (enum)            --  Download option to download software

                os_list      (list of enum)    --  list of windows/unix packages to be downloaded

                service_pack (int)             --  service pack to be downloaded

                cu_number (int)                --  maintenance release number

                sync_cache (bool)              --  True if download and sync
                                                   False only download
                
                sync_cache_list (list)         --  list of names of remote caches to sync
                                                   use None to sync all caches

                schedule_pattern (dict)        --  pattern for schedule task
                                                   

            Returns:
                object - instance of the Job class for this download job

            Raises:
                SDKException:
                    if Download job failed

                    if response is empty

                    if response is not success

                    if another download job is running

            Usage:

            -   if download_software is not given any parameters it takes default value of latest
                service pack for options and downloads WINDOWS_64 package

                >>> commcell_obj.download_software()

            -   DownloadOptions and DownloadPackages enum is used for providing input to the
                download software method, it can be imported by

                >>> from cvpysdk.deployment.deploymentconstants import DownloadOptions
                    from cvpysdk.deployment.deploymentconstants import DownloadPackages

            -   sample method calls for different options, for latest service pack

                >>> commcell_obj.download_software(
                        options=DownloadOptions.lATEST_SERVICEPACK.value,
                        os_list=[DownloadPackages.WINDOWS_64.value]
                        )

            -   For Latest hotfixes for the installed service pack

                >>> commcell_obj.download_software(
                        options='DownloadOptions.LATEST_HOTFIXES.value',
                        os_list=[DownloadPackages.WINDOWS_64.value,
                                DownloadPackages.UNIX_LINUX64.value]
                        )

            -   For service pack and hotfixes

                >>> commcell_obj.download_software(
                        options='DownloadOptions.SERVICEPACK_AND_HOTFIXES.value',
                        os_list=[DownloadPackages.UNIX_MAC.value],
                        service_pack=13,
                        cu_number=42
                        )

                    **NOTE:** service_pack parameter must be specified for third option

        """

        # To set the default value if option is none
        version = self.commcell_object.commserv_version
        if options is None:
            options = 'latest service pack'

        if DownloadOptions.LATEST_SERVICEPACK.value == options:
            self.update_option = {
                'upgradeToLatestRelease': True,
                'latestFixesForCurrentRelease': False,
                "featureRelease": self.commcell_object.version,
                'SPName': 'latest',
                'IsSPName': False,
                'isSpDelayedDays': True,
                'isHotfixesDownload': False
            }
        elif DownloadOptions.LATEST_HOTFIXES.value == options:
            self.update_option = {
                'upgradeToLatestRelease': False,
                'latestFixesForCurrentRelease': True,
                'SPName': 'hotfix',
                'IsSPName': False,
                'isSpDelayedDays': True,
                'isHotfixesDownload': True
            }
        elif DownloadOptions.SERVICEPACK_AND_HOTFIXES.value == options:
            if service_pack is None:
                raise SDKException('Download', '102')
            self.update_option = {
                'upgradeToLatestRelease': False,
                'latestFixesForCurrentRelease': False,
                "featureRelease": "11." + str(service_pack) + "." + str(cu_number),
                'SPName': str(service_pack),
                'IsSPName': True,
                'isSpDelayedDays': False,
                'isHotfixesDownload': False
            }

        # to set the default value if os_list is none
        if os_list is None:
            os_list = ['WINDOWS_X64']

        client_groups = []
        if sync_cache and sync_cache_list:
            for cache in sync_cache_list:
                client_groups.append({"type": "CLIENT_ENTITY",
                                      "clientName": cache,
                                      "id": self.commcell_object.clients.get(cache).client_id
                                      }) if version >= 36 else client_groups.append({"clientName": cache})
        elif sync_cache and not sync_cache_list:
            if version < 36:
                client_groups = [{"_type_": 2}]
            else:
                flag_1, response_1 = self._cvpysdkcommcell_object.make_request('GET', self._services['CREATE_RC'])
                cache_list = []
                for obj in response_1.json()['softwareCacheDetailList']:
                    if obj['cache']['id'] != 2:
                        cache_list.append(obj['cache']['name'])
                for client in cache_list:
                    client_groups.append({"type": "CLIENT_ENTITY",
                                          "clientName": client,
                                          "id": int(self.commcell_object.clients.all_clients[client]['id'])})

        if version >= 36:
            win_os_list = []
            unix_os_list = []
            temp_win = ['WINDOWS_X64', 'WINDOWS_X32', 'WINDOWS_ARM64']

            for os in os_list:
                if os in temp_win:
                    win_os_list.append(os)
                else:
                    unix_os_list.append(os)
            request_json = {
                "downloadConfiguration": {
                    "upgradeToLatestRelease": self.update_option['upgradeToLatestRelease'],
                    "latestFixesForCurrentRelease": self.update_option['latestFixesForCurrentRelease'],
                    "windowsDownloadOptions": win_os_list,
                    "unixDownloadOptions": unix_os_list,
                },
                "notifyWhenJobCompletes": False,
                "entities": client_groups

            }
            if DownloadOptions.SERVICEPACK_AND_HOTFIXES.value == options:
                request_json["downloadConfiguration"]["featureRelease"] = self.update_option['featureRelease']
        else:
            request_json = {
                "taskInfo": {
                    "task": {
                        "taskType": 1,
                        "initiatedFrom": 2,
                        "policyType": 0,
                        "alert": {
                            "alertName": ""
                        },
                        "taskFlags": {
                            "isEdgeDrive": False,
                            "disabled": False
                        }
                    },
                    "subTasks": [
                        {
                            "subTaskOperation": 1,
                            "subTask": {
                                "subTaskType": 1,
                                "operationType": 4019
                            },
                            "options": {
                                "adminOpts": {
                                    "updateOption": {
                                        "syncUpdateCaches": sync_cache,
                                        "spName": self.update_option['SPName'],
                                        "CUNumber": cu_number,
                                        "isWindows": True,
                                        "majorOnly": False,
                                        "isSpName": self.update_option['IsSPName'],
                                        "copyUpdates": True,
                                        "isHotfixesDownload": self.update_option['isHotfixesDownload'],
                                        "isSpDelayedDays": self.update_option['isSpDelayedDays'],
                                        "copySoftwareAndUpdates": False,
                                        "isUnix": True,
                                        "unixDownloadPackages": {
                                            "linuxosX64": 'LINUX_X86_64' in os_list,
                                            "solarisosX64": 'SOLARIS_X86_64' in os_list,
                                            "solsparcos": 'Solaris-SPARC-X86' in os_list,
                                            "freeBSDos": 'FREEBSD_X86' in os_list,
                                            "linuxos": 'LINUX_X86' in os_list,
                                            "linuxosPPC64le": 'LINUX_PPC64LE' in os_list,
                                            "freeBSDosX64": 'FREEBSD_X86_64' in os_list,
                                            "solarisos": 'SOLARIS_SPARC' in os_list,
                                            "linuxs390os": 'Linux-S390-31' in os_list,
                                            "darwinos": 'MAC_OS' in os_list,
                                            "linuxosS390": 'Linux-S390' in os_list,
                                            "aixppcos": 'Aix-PPC-32' in os_list,
                                            "linuxosPPC64": 'LINUX_PPC64' in os_list,
                                            "aixos": 'AIX_PPC' in os_list,
                                            "hpos": 'HP_IA64' in os_list,
                                            "solos": 'Solaris X86' in os_list
                                        },
                                        "windowsDownloadPackages": {
                                            "windowsX64": 'WINDOWS_X64' in os_list,
                                            "windows32": 'WINDOWS_X32' in os_list
                                        },
                                        "clientAndClientGroups": client_groups,
                                        "downloadUpdatesJobOptions": {
                                            "downloadSoftware": True
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        method = 'PUT' if version >= 36 else 'POST'
        url = self._services['DOWNLOAD_SOFTWARE'] if version >= 36 else self._services['CREATE_TASK']

        flag, response = self._cvpysdkcommcell_object.make_request(
            method, url, request_json
        )

        if flag:
            if response.json():
                if "jobId" in response.json() or "jobIds" in response.json():
                    return Job(self.commcell_object, response.json()['jobId']) if version >= 36 \
                        else Job(self.commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedules(self.commcell_object).get(task_id=response.json()['taskId'])

                else:
                    raise SDKException('Download', '101')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def copy_software(self, media_loc, username=None, password=None, sync_cache=True, sync_cache_list=None, schedule_pattern=None):
        """copies media from the specified location on the commcell

                    Args:

                        media_loc      (str)           --  Media Location to be used for copy software

                        username       (str)           --  username to authenticate to external location

                        password       (str)           --  password to authenticate to external location

                        sync_cache (bool)              --  True if download and sync
                                                           False only download

                        sync_cache_list (list)         --  list of names of remote caches to sync
                                                            use None to sync all caches

                        schedule_pattern(dict)         --  pattern for schedule task


                    Returns:
                        object - instance of the Job class for this copy software job

                    Raises:
                        SDKException:
                            if Download job failed

                            if response is empty

                            if response is not success

                            if another download job is running
                    Usage:

                        -   if media_location directory is local to the machine - username and password is not needed

                            >>> commcell_obj.copy_software(media_loc = "C:\\Downloads\\Media")

                        -   if Media_location directory is remote- username and passsword(base 64 encoded) are needed
                            to authenticate the cache

                            >>> commcell_obj.copy_software(
                            media_loc = "\\\\subdomain.company.com\\Media",
                            username = "domainone\\userone",
                            password = "base64encoded password"
                            )
                """
        version = self.commcell_object.commserv_version
        client_auth = {}
        if username:
            if password is None:
                raise Exception(f"Password missing for remote location {media_loc}")
            client_auth = {
                "userName": username,
                "password": password
            }

        if version >= 36:
            client_groups = []
            if sync_cache:
                if sync_cache_list:
                    for cache in sync_cache_list:
                        client_groups.append({"type": "CLIENT_ENTITY",
                                              "clientName": cache,
                                              "id": self.commcell_object.clients.get(cache).client_id
                                              })
                else:
                    flag_1, response_1 = self._cvpysdkcommcell_object.make_request('GET', self._services['CREATE_RC'])
                    cache_list = []
                    for obj in response_1.json()['softwareCacheDetailList']:
                        if obj['cache']['id'] != 2:
                            cache_list.append(obj['cache']['name'])
                    for client in cache_list:
                        client_groups.append({"type": "CLIENT_ENTITY",
                                              "clientName": client,
                                              "id": int(self.commcell_object.clients.all_clients[client]['id'])})
            request_json = {
                "copyConfiguration": {
                    "downloadPath": media_loc
                },
                "notifyWhenJobCompletes": False,
                "entities": client_groups
            }
            if client_auth:
                request_json['copyConfiguration']['username'] = username
                request_json['copyConfiguration']['password'] = password
        else:
            request_json = {
                "taskInfo": {
                    "task": {
                        "taskType": 1,
                        "initiatedFrom": 2,
                        "policyType": 0,
                        "alert": {
                            "alertName": ""
                        },
                        "taskFlags": {
                            "isEdgeDrive": False,
                            "disabled": False
                        }
                    },
                    "subTasks": [
                        {
                            "subTaskOperation": 1,
                            "subTask": {
                                "subTaskType": 1,
                                "operationType": 4019
                            },
                            "options": {
                                "adminOpts": {
                                    "updateOption": {
                                        "syncUpdateCaches": sync_cache,
                                        "copyUpdates": True,
                                        "copySoftwareAndUpdates": True,
                                        "clientAndClientGroups": [
                                            {
                                                "_type_": 2
                                            }
                                        ],
                                        "downloadUpdatesJobOptions": {
                                            "downloadSoftware": True,
                                            "updateCachePath": media_loc,
                                            "clientAuth": client_auth
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        method = 'PUT' if version >= 36 else 'POST'
        url = self._services['DOWNLOAD_SOFTWARE'] if version >= 36 else self._services['CREATE_TASK']

        flag, response = self._cvpysdkcommcell_object.make_request(
            method, url, request_json
        )

        if flag:
            if response.json():
                if "jobId" in response.json() or "jobIds" in response.json():
                    return Job(self.commcell_object, response.json()['jobId']) if version >= 36 \
                        else Job(self.commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedules(self.commcell_object).get(task_id=response.json()['taskId'])

                else:
                    raise SDKException('Download', '101')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def sync_remote_cache(self, client_list=None):
        """Syncs remote cache

            Args:

                client_list  --  list of client names
                Default is None. By default all remote cache clients are synced

            Returns:
                object - instance of the Job class for sync job

            Raises:
                SDKException:
                    if sync job failed

                    if response is empty

                    if response is not success

                    if another sync job is running with the given client

        """

        clients = []
        if client_list is None:

            clients = [{
                "_type_": 2
            }]
        else:
            for each in client_list:
                clients.append({
                    "_type_": 3,
                    "clientName": each})

        request_json = {
            "taskInfo": {
                "task": {
                    "ownerId": 1,
                    "taskType": 1,
                    "ownerName": "admin",
                    "initiatedFrom": 1,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4019
                        },
                        "options": {
                            "adminOpts": {
                                "updateOption": {
                                    "syncUpdateCaches": True,
                                    "invokeLevel": 1,
                                    "isWindows": False,
                                    "majorOnly": False,
                                    "isSpName": False,
                                    "copyUpdates": True,
                                    "isHotfixesDownload": False,
                                    "isSpDelayedDays": True,
                                    "copySoftwareAndUpdates": False,
                                    "isUnix": False,
                                    "clientAndClientGroups": clients,
                                    "downloadUpdatesJobOptions": {
                                        "downloadSoftware": False
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }

        flag, response = self._cvpysdkcommcell_object.make_request(
            'POST', self._services['CREATE_TASK'], request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self.commcell_object, response.json()['jobIds'][0])

                else:
                    raise SDKException('Download', '101')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')
