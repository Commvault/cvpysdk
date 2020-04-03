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

"""" Main file for performing the software cache configuration related operations

CommserveCache   --  Class for performing operations on the CS cache
RemoteCache      --  Class for performing operations on the remote cache

CommServeCache
==============

    __init__(commcell_object)             --  initialize commcell_object of CommServeCache class
    associated with the commcell

    get_cs_cache_path()                   --  returns CS cache path

    delete_cache()                        --  deletes CS cache

    commit_cache()                        --  commits CS cache

RemoteCache
==============

    __init__(commcell, client_object)     --  initialize commcell and client_object of RemoteCache class
    associated with the client

    get_remote_cache_path()               --  returns remote cache path

    configure_remote_cache()              --  Configures client as remote cache

    configure_packages_to_sync()          --  Configures packages to sync for the remote cache
"""
from ..exception import SDKException
from .deploymentconstants import UnixDownloadFeatures
from .deploymentconstants import WindowsDownloadFeatures
from .deploymentconstants import OSNameIDMapping


class CommServeCache(object):
    """"class for downloading software packages"""

    def __init__(self, commcell_object):
        """Initialize commcell_object of the Download class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the CommServeCache class

        """

        self.commcell_object = commcell_object

    def get_cs_cache_path(self):
        """
        Returns CS cache path

        Returns:
            cs_cache_path (str) -- returns cs cache path

        Raises:
            SDKException:
            - Failed to execute the api

            - Response is incorrect/empty
        """
        response = self.commcell_object.get_gxglobalparam_value()
        if response['error']['errorCode'] != 0:
            error_message = "Failed with error: [{0}]".format(
                response['error']['errorMessage']
            )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(response['error']['errorCode'], error_message)
            )
        try:
            return response['commserveSoftwareCache']['storePatchlocation']
        except Exception:
            raise SDKException('Response', '102')

    def delete_cache(self):
        """
        Delete CS cache

        Raises:
            SDKException:
            - Failed to execute the api

            - Response is incorrect
        """

        request_xml = """<EVGui_SetUpdateAgentInfoReq>
            <uaInfo deletePackageCache="1" deleteUpdateCache="1" swAgentOpType="1"
            uaOpCode="0" uaPackageCacheStatus="0"
             uaUpdateCacheStatus="0" >
            <uaName id="2" name=""/>
            <client _type_="3"/>
            </uaInfo>
            </EVGui_SetUpdateAgentInfoReq>
            """

        response = self.commcell_object.qoperation_execute(request_xml)

        if response.get('errorCode') != 0:
            error_message = "Failed with error: [{0}]".format(
                response.get('errorMessage')
            )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(response.get('errorCode'), error_message)
            )

    def commit_cache(self):
        """
        Commits CS cache

        Raises:
            SDKException:
            - Failed to execute the api

            - Response is incorrect
        """

        request_xml = """<EVGui_SetUpdateAgentInfoReq>
            <uaInfo defaultShareName="" deletePackageCache="0" deleteUpdateCache="0" swAgentOpType="4"
            uaPackageCacheStatus="0" uaUpdateCacheStatus="0">
            <uaName id="2" name=""/>
            <client _type_="3"/>
            </uaInfo>
            <uaList/>
            </EVGui_SetUpdateAgentInfoReq>
            """

        response = self.commcell_object.qoperation_execute(request_xml)

        if response.get('errorCode') != 0:
            error_message = "Failed with error: [{0}]".format(
                response.get('errorMessage')
            )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(response.get('errorCode'), error_message)
            )


class RemoteCache(object):
    """"class for downloading software packages"""

    def __init__(self, commcell, client_name):
        """Initialize commcell_object of the Download class.

            Args:
                commcell (object)     --  commcell object
                client_name           --  client name

            Returns:
                object - instance of the RemoteCache class

        """
        self.commcell = commcell
        self.client_object = self.commcell.clients.get(client_name)

    def get_remote_cache_path(self):
        """
        Returns remote cache path

        Returns:
            remote_cache_path (str) - remote cache path of the client

        Raises:
            SDKException:
            - Failed to execute the api

            - Response is incorrect/empty

        """
        request_xml = '<EVGui_GetUpdateAgentInfoReq />'
        response = self.commcell.qoperation_execute(request_xml)
        if response:
            try:
                for clients in response["qualifiedClients"]:
                    if clients['clientName']['name'] == self.client_object.client_name:
                        remote_cache_path = clients["cachePath"]
                        break
                return remote_cache_path
            except Exception:
                raise SDKException('Response', '101')
        else:
            raise SDKException('Response', '102')

    def configure_remotecache(self, cache_path):
        """
        Configures client as remote cache

        Args:
              cache_path (str)  - Remote cache path

        Raises:
            SDKException:
            - Failed to execute the api

            - Response is incorrect
        """

        request_xml = """
             <EVGui_SetUpdateAgentInfoReq>
             <uaInfo uaCachePath="%s" uaOpCode="5">
             <uaName id="%s" name="%s"/>
             <client _type_="3"/>
             </uaInfo>
             <uaList/>
             </EVGui_SetUpdateAgentInfoReq>
             """ % (cache_path, self.client_object.client_id, self.client_object.client_name)

        response = self.commcell.qoperation_execute(request_xml)
        if response.get('errorCode') != 0:
            error_message = "Failed with error: [{0}]".format(
                response.get('errorMessage')
            )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(response.get('errorCode'), error_message)
            )

    def configure_packages_to_sync(self, win_os=None, win_package_list=None, unix_os=None,
                                   unix_package_list=None):
        """
        Configures packages to sync for the remote cache

        Args:
            win_os 		(list)	 	-- list of windows oses to sync
            win_package_list  (list)-- list of windows packages to sync
            unix_os (list) 		  	-- list of unix oses to sync
            unix_package_list (list)-- list of unix packages to sync

        Raises:
            SDKException:
            - Failed to execute the api

            - Response is incorrect

            - Incorrect input

        Usage:
            commcell_obj.configure_packages_to_sync()

            win_os = ["WINDOWS_32", "WINDOWS_64"]
            unix_os = ["UNIX_LINUX64", "UNIX_AIX"]
            win_package_list = ["FILE_SYSTEM", "MEDIA_AGENT"]
            unix_package_list = ["FILE_SYSTEM", "MEDIA_AGENT"]

            OS_Name_ID_Mapping, WindowsDownloadFeatures and UnixDownloadFeatures enum is used for
            providing input to the configure_packages_to_sync method, it can be imported by

                >>> from cvpysdk.deployment.deploymentconstants import UnixDownloadFeatures
                    from cvpysdk.deployment.deploymentconstants import OS_Name_ID_Mapping
                    from cvpysdk.deployment.deploymentconstants import WindowsDownloadFeatures

        """
        win_os_id = [eval(f"OSNameIDMapping.{each}.value") for each in win_os]
        unix_os_id = [eval(f"OSNameIDMapping.{each}.value") for each in unix_os]
        win_packages = [eval(f"WindowsDownloadFeatures.{packages}.value") for packages in win_package_list]
        unix_packages = [eval(f"UnixDownloadFeatures.{packages}.value") for packages in unix_package_list]

        if not win_os_id and not unix_os_id:
            qscript = f'''-sn QS_GranularConfigRemoteCache -si '{self.client_object.client_name}' -si SyncAll'''
        elif not unix_os_id:
            qscript = (f'''-sn QS_GranularConfigRemoteCache -si '{self.client_object.client_name}' -si SyncCustom '''
                       f'''-si {",".join(map(str, win_os_id))} -si {",".join(map(str, win_packages))}''')
        elif not win_os_id:
            qscript = (f'''-sn QS_GranularConfigRemoteCache -si '{self.client_object.client_name}' -si SyncCustom '''
                       f'''-si {",".join(map(str, unix_os_id))} -si {",".join(map(str, unix_packages))}''')
        else:
            qscript = (f'''-sn QS_GranularConfigRemoteCache -si '{self.client_object.client_name}' -si SyncCustom '''
                       f'''-si {",".join(map(str, win_os_id))} -si {",".join(map(str, win_packages))} '''
                       f'''-si {",".join(map(str, unix_os_id))} -si {",".join(map(str, unix_packages))}''')

        response = self.commcell._qoperation_execscript(qscript)
        if response.get('CVGui_GenericResp'):
            if response['CVGui_GenericResp']['@errorCode'] != 0:
                error_message = "Failed with error: [{0}]".format(
                    response['CVGui_GenericResp']['@errorMessage']
                )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(
                    response['CVGui_GenericResp']['@errorCode'],
                    error_message))
