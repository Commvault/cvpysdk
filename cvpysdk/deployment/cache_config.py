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

    get_request_xml()                     --  returns request xml for cache and remote cache related operations

    get_cs_cache_path()                   --  returns CS cache path

    delete_cache()                        --  deletes CS cache

    commit_cache()                        --  commits CS cache

    get_remote_cache_clients()            --  fetches the list of Remote Cache configured for a particular Admin/Tenant

RemoteCache
==============

    __init__(commcell, client_object)     --  initialize commcell and client_object of RemoteCache class
    associated with the client

    get_remote_cache_path()               --  returns remote cache path, if exists, else None

    configure_remote_cache()              --  Configures client as remote cache

    configure_packages_to_sync()          --  Configures packages to sync for the remote cache

    assoc_entity_to_remote_cache()        --  Associates entity to the Remote Cache

    delete_remote_cache_contents()        --  deletes remote cache contents

    get_remote_cache_details()            --  gets all details of specific remote cache

    get_qualified_servers_for_remote_cache() -- get the list of clients which can be configured as Remote Cache

    update_cache_path()                   --  updates the cache path of Remote Cache

    enable_rc()                           --  enables the remote cache

    disable_rc()                          --  disables the remote cache

    update_associations()                 --  updates the clients/client group associations to a remote cache

    delete_remote_cache()                 --  deleted the remote cache

    get_all_remote_cache()                --  get the list of all remote caches
"""
from xml.etree import ElementTree as ET
from ..exception import SDKException
from .deploymentconstants import UnixDownloadFeatures
from .deploymentconstants import WindowsDownloadFeatures
from .deploymentconstants import OSNameIDMapping
from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..commcell import Commcell

class CommServeCache(object):
    """class for downloading software packages

    Description:
        This class is used to perform operations on the CommServe cache.

    Attributes:
        commcell_object (object): Instance of the Commcell class.
        request_xml (str): XML request for cache and remote cache related operations.
        _cvpysdk_object (object): Instance of the CVPySDK class.
        _services (dict): Dictionary of CommCell services.

    Usage:
        >>> cs_cache = CommServeCache(commcell_object)
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize commcell_object of the Download class.

        Args:
            commcell_object (object): Instance of the Commcell class.

        Returns:
            CommServeCache: Instance of the CommServeCache class.

        Usage:
            >>> cs_cache = CommServeCache(commcell_object)
        """

        self.commcell_object = commcell_object
        self.request_xml = CommServeCache.get_request_xml()
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services

    @staticmethod
    def get_request_xml() -> str:
        """Returns request xml for cache and remote cache related operations

        Returns:
            str: The XML request string.

        Usage:
            >>> CommServeCache.get_request_xml()
        """
        return """<EVGui_SetUpdateAgentInfoReq>
                <uaInfo deletePackageCache="" deleteUpdateCache="" swAgentOpType=""
                uaOpCode="0" uaPackageCacheStatus="0"
                 uaUpdateCacheStatus="0" >
                <uaName id="2" name=""/>
                <client _type_="3"/>
                </uaInfo>
                </EVGui_SetUpdateAgentInfoReq>
                """

    def get_cs_cache_path(self) -> str:
        """Returns CS cache path

        Returns:
            str: The CS cache path.

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect/empty.

        Usage:
            >>> cs_cache.get_cs_cache_path()
        """
        try:
            response = self.commcell_object.get_gxglobalparam_value()
        except Exception:
            try:
                response = self.commcell_object.get_gxglobalparam_value('Patch Directory')
            except Exception:
                raise SDKException('Response', '101', 'Failed to execute api for get_cs_cache_path')
            if response == '':
                raise SDKException('Response', '102')
            return response
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

    def delete_cache(self) -> None:
        """Delete CS cache

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect.

        Usage:
            >>> cs_cache.delete_cache()
        """
        root = ET.fromstring(self.request_xml)
        uaInfo = root.find(".//uaInfo")
        uaInfo.set('deletePackageCache', "1")
        uaInfo.set("deleteUpdateCache", "1")
        uaInfo.set("swAgentOpType", "1")

        response = self.commcell_object.qoperation_execute(ET.tostring(root))
        if response.get('errorCode') != 0:
            error_message = "Failed with error: [{0}]".format(
                response.get('errorMessage')
            )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(response.get('errorCode'), error_message)
            )

    def commit_cache(self) -> None:
        """Commits CS cache

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect.

        Usage:
            >>> cs_cache.commit_cache()
        """

        root = ET.fromstring(self.request_xml)
        uaInfo = root.find(".//uaInfo")
        uaInfo.set('deletePackageCache', "0")
        uaInfo.set("deleteUpdateCache", "0")
        uaInfo.set("swAgentOpType", "4")

        response = self.commcell_object.qoperation_execute(ET.tostring(root))
        if response.get('errorCode') != 0:
            error_message = "Failed with error: [{0}]".format(
                response.get('errorMessage')
            )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(response.get('errorCode'), error_message)
            )

    def get_remote_cache_clients(self) -> List[str]:
        """Fetches the List of Remote Cache configured for a particular Admin/Tenant

        Returns:
            List[str]: List of Remote Cache configured.

        Raises:
            SDKException:
                - Response is incorrect.
                - Failed to execute the API.

        Usage:
            >>> cs_cache.get_remote_cache_clients()
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._services['GET_REMOTE_CACHE_CLIENTS'])

        if flag:
            rc_client_names = []
            if response.ok:
                xml_tree = ET.fromstring(response.text)
                if xml_tree.findall(".//client"):
                    # Find all 'client' elements
                    client_elements = xml_tree.findall('.//client')
                    # Extract the client names
                    rc_client_names = [client.get('clientName') for client in client_elements]
                    rc_client_names.remove(self.commcell_object.commserv_name)
                return rc_client_names
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')


class RemoteCache(object):
    """class for downloading software packages

    Description:
        This class is used to perform operations on a remote cache client.

    Attributes:
        commcell (object): Instance of the Commcell class.
        client_object (object): Instance of the Client class.
        request_xml (str): XML request for cache and remote cache related operations.
        _cvpysdk_object (object): Instance of the CVPySDK class.
        _services (dict): Dictionary of CommCell services.

    Usage:
        >>> remote_cache = RemoteCache(commcell_object, 'client1')
    """

    def __init__(self, commcell: 'Commcell', client_name: str) -> None:
        """Initialize commcell_object of the Download class.

        Args:
            commcell (object): Commcell object.
            client_name (str): Client name.

        Returns:
            RemoteCache: Instance of the RemoteCache class.

        Usage:
            >>> remote_cache = RemoteCache(commcell_object, 'client1')
        """
        self.commcell = commcell
        self.client_object = self.commcell.clients.get(client_name)
        self.request_xml = CommServeCache.get_request_xml()
        self._cvpysdk_object = commcell._cvpysdk_object
        self._services = commcell._services

    def get_remote_cache_path(self) -> Optional[str]:
        """Returns remote cache path, if exists, else None

        Returns:
            Optional[str]: Remote cache path of the client if exists, otherwise None.

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect/empty.

        Usage:
            >>> remote_cache.get_remote_cache_path()
        """
        request_xml = '<EVGui_GetUpdateAgentInfoReq />'
        response = self.commcell.qoperation_execute(request_xml)
        if response:
            try:
                for clients in response["uaInfo"]:
                    if clients['client']['clientName'] == self.client_object.client_name:
                        return clients["uaCachePath"]
                return None
            except Exception:
                raise SDKException('Response', '101')
        else:
            raise SDKException('Response', '102')

    def configure_remotecache(self, cache_path: str, cs_version: Optional[int] = None) -> None:
        """Configures client as remote cache

        Args:
            cache_path (str): Remote cache path.
            cs_version (int, optional): CS SP version. Defaults to None.
                        (This parameter should be passed if tennat admin is configuring RC)

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect.

        Usage:
            >>> remote_cache.configure_remotecache(cache_path='/opt/remote_cache')
        """
        if cs_version is None:
            cs_version = self.commcell.commserv_version

        # using API to configure RC from SP34
        if cs_version >= 34:
            request_json = {
                "cacheDirectory": cache_path,
                "associations": [],
                "cache": {
                    "name": self.client_object.client_name,
                    "id": int(self.client_object.client_id)
                }
            }

            flag, response = self._cvpysdk_object.make_request(
                'POST', self._services['SOFTWARE_CACHE'], request_json
            )

            if flag:
                if response.json():
                    errorCode = response.json()['errorCode']
                    if errorCode != 0:
                        raise SDKException(
                            'Response',
                            '101',
                            'Error Code: "{0}"'.format(errorCode)
                        )
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101')

        # using qscript to configure machine as RC before SP34
        else:
            root = ET.fromstring(self.request_xml)
            uaInfo = root.find(".//uaInfo")
            uaInfo.set('uaCachePath', cache_path)
            uaInfo.set('uaOpCode', "5")
            uaInfo.attrib.pop("uaPackageCacheStatus")
            uaInfo.attrib.pop('uaUpdateCacheStatus')
            root.find("./uaInfo/uaName").set("id", self.client_object.client_id)
            root.find("./uaInfo/uaName").set("name", self.client_object.client_name)
            response = self.commcell.qoperation_execute(ET.tostring(root))
            if response.get('errorCode') != 0:
                error_message = "Failed with error: [{0}]".format(
                    response.get('errorMessage')
                )
                raise SDKException(
                    'Response',
                    '101',
                    'Error Code:"{0}"\nError Message: "{1}"'.format(response.get('errorCode'), error_message)
                )

    def configure_packages_to_sync(self, win_os: Optional[List[str]] = None, win_package_list: Optional[List[str]] = None, unix_os: Optional[List[str]] = None,
                                   unix_package_list: Optional[List[str]] = None) -> None:
        """Configures packages to sync for the remote cache

        Args:
            win_os (Optional[List[str]]): List of Windows OSes to sync. Defaults to None.
            win_package_list (Optional[List[str]]): List of Windows packages to sync. Defaults to None.
            unix_os (Optional[List[str]]): List of Unix OSes to sync. Defaults to None.
            unix_package_list (Optional[List[str]]): List of Unix packages to sync. Defaults to None.

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect.
                - Incorrect input.

        Usage:
            >>> remote_cache.configure_packages_to_sync()
            >>>
            >>> win_os = ["WINDOWS_32", "WINDOWS_64"]
            >>> unix_os = ["UNIX_LINUX64", "UNIX_AIX"]
            >>> win_package_list = ["FILE_SYSTEM", "MEDIA_AGENT"]
            >>> unix_package_list = ["FILE_SYSTEM", "MEDIA_AGENT"]
            >>>
            >>> remote_cache.configure_packages_to_sync(win_os=win_os, win_package_list=win_package_list, unix_os=unix_os, unix_package_list=unix_package_list)
            >>>
            >>> # OS_Name_ID_Mapping, WindowsDownloadFeatures and UnixDownloadFeatures enum is used for
            >>> # providing input to the configure_packages_to_sync method, it can be imported by
            >>> # from cvpysdk.deployment.deploymentconstants import UnixDownloadFeatures
            >>> # from cvpysdk.deployment.deploymentconstants import OS_Name_ID_Mapping
            >>> # from cvpysdk.deployment.deploymentconstants import WindowsDownloadFeatures
        """
        if win_os:
            win_os_id = [eval(f"OSNameIDMapping.{each}.value") for each in win_os]
            win_packages = [eval(f"WindowsDownloadFeatures.{packages}.value") for packages in win_package_list]
        if unix_os:
            unix_os_id = [eval(f"OSNameIDMapping.{each}.value") for each in unix_os]
            unix_packages = [eval(f"UnixDownloadFeatures.{packages}.value") for packages in unix_package_list]

        if not win_os and not unix_os:
            qscript = f'''-sn QS_GranularConfigRemoteCache -si '{self.client_object.client_name}' -si SyncAll'''
        elif not unix_os:
            qscript = (f'''-sn QS_GranularConfigRemoteCache -si '{self.client_object.client_name}' -si SyncCustom '''
                       f'''-si {",".join(map(str, win_os_id))} -si {",".join(map(str, win_packages))}''')
        elif not win_os:
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

    def delete_remote_cache_contents(self) -> None:
        """Delete remote cache contents

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect.

        Usage:
            >>> remote_cache.delete_remote_cache_contents()
        """
        root = ET.fromstring(self.request_xml)
        uaInfo = root.find(".//uaInfo")
        uaInfo.set('deletePackageCache', "1")
        uaInfo.set("deleteUpdateCache", "1")
        uaInfo.set("swAgentOpType", "1")
        root.find("./uaInfo/uaName").set("id", self.client_object.client_id)
        root.find("./uaInfo/uaName").set("name", self.client_object.client_name)

        response = self.commcell.qoperation_execute(ET.tostring(root))
        if response.get('errorCode') != 0:
            error_message = "Failed with error: [{0}]".format(
                response.get('errorMessage')
            )
            raise SDKException(
                'Response',
                '101',
                'Error Code:"{0}"\nError Message: "{1}"'.format(response.get('errorCode'), error_message)
            )

    def assoc_entity_to_remote_cache(self, client_name: Optional[str] = None, client_group_name: Optional[str] = None) -> None:
        """Points/Associates entity to the Remote Cache Client

        Args:
            client_name (Optional[str]): The client which has to be pointed to Remote Cache. Defaults to None.
            client_group_name (Optional[str]): The client_group which has to be pointed to Remote Cache. Defaults to None.

        Raises:
            SDKException:
                - Failed to execute the API.
                - Response is incorrect.

        Usage:
            >>> remote_cache.assoc_entity_to_remote_cache(client_name='client1')
            >>> remote_cache.assoc_entity_to_remote_cache(client_group_name='client_group1')
        """

        if client_name is None and client_group_name is None:
            raise Exception("No clients or client groups to associate; Please provide a valid name")

        if client_name and client_name in self.commcell.clients.all_clients:
            entity_obj = self.commcell.clients.get(client_name)
            entity_id = entity_obj.client_id
            entity_name = entity_obj.client_name
            entity_type = "0"

        elif client_group_name in self.commcell.client_groups.all_clientgroups:
            entity_obj = self.commcell.client_groups.get(client_group_name)
            entity_id = entity_obj.clientgroup_id
            entity_name = entity_obj.clientgroup_name
            entity_type = "1"

        else:
            raise Exception("{0} does not exist".format(client_name if client_name else client_group_name))

        request_json = {
                "EVGui_SetUpdateAgentInfoReq" :{
                "uaInfo": {
                    "uaCachePath": self.get_remote_cache_path(),
                    "uaOpCode": "5",
                    "uaName": {
                        "id": self.client_object.client_id,
                        "name": self.client_object.client_name
                    }
                },
                "uaList": {
                    "addedList": {
                        "id": entity_id,
                        "name": entity_name,
                        "type": entity_type
                    }
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_json
        )

        if flag:
            if response.ok:
                if response.json():
                    if response.json().get('errorCode') != 0:
                        error_code = response.json().get('errorCode')
                        error_message = "Failed with error: [{0}]".format(
                            response.json().get('errorMessage')
                        )
                        raise SDKException(
                            'Response',
                            '101',
                            'Error Code:"{0}"\nError Message: "{1}"'.format(error_code, error_message)
                        )
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def get_remote_cache_details(self) -> Dict[str, Any]:
        """Retrieve details of the remote software cache.

        The returned dictionary contains the following keys:
            - cacheDirectory: Path to the cache directory.
            - enabled: Boolean indicating if the cache is enabled.
            - associations: List of associated entities.
            - cacheContents: Information about the contents of the cache.
            - status: Current status of the remote cache.

        Returns:
            Dictionary containing remote cache details for the client.

        Raises:
            SDKException: If the response from the server is invalid or the request fails.

        Example:
            >>> remote_cache = RemoteCache(...)
            >>> cache_details = remote_cache.get_remote_cache_details()
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['SOFTWARE_CACHE']+f"/{self.client_object.client_id}"
        )

        if flag:
            if response.json():
                return response.json()['softwareCacheDetailList'][0]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def get_qualified_servers_for_remote_cache(self) -> List[Dict[str, Any]]:
        """Retrieve all machines qualified to be configured as remote cache servers.

        Returns:
            List of dictionaries containing details for each qualified remote cache server.

        Raises:
            SDKException: If the response from the server is invalid or the request fails.

        Example:
            >>> remote_cache = RemoteCache(...)
            >>> qualified_servers = remote_cache.get_qualified_servers_for_remote_cache()
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['QUALIFIED_SERVERS_SW']
        )

        if flag:
            if response.json():
                return response.json()['softwareCacheDetailList']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def update_cache_path(self, path: str) -> None:
        """Update the cache directory path for the remote cache.

        This method sets a new cache directory path for the remote cache associated with the client.
        If the update fails or the response contains a non-zero error code, an SDKException is raised.

        Args:
            path: The new cache directory path as a string.

        Raises:
            SDKException: If the update operation fails or the response contains a non-zero error code.

        Example:
            >>> remote_cache = RemoteCache(...)
            >>> remote_cache.update_cache_path("/mnt/remote/cache")
            # If the operation fails, SDKException will be raised.
        """
        request_json = {}
        request_json['cacheDirectory'] = path

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['SOFTWARE_CACHE'] + f"/{self.client_object.client_id}", request_json
        )

        if flag:
            if response.json():
                errorCode = response.json()['errorCode']
                if errorCode != 0:
                    raise SDKException(
                        'Response',
                        '101',
                        'Error Code: "{0}"'.format(errorCode)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def enable_rc(self) -> None:
        """Enable the remote cache.

        This method sends a request to enable the remote cache.
        If the operation fails or the response contains a non-zero error code,
        an SDKException is raised.

        Raises:
            SDKException: If the request fails or the response contains a non-zero error code.

        Example:
            >>> remote_cache = RemoteCache(...)
            >>> remote_cache.enable_rc()
            # If an error occurs, SDKException will be raised
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['SOFTWARE_CACHE'] + f"/{self.client_object.client_id}", {'enabled' : True}
        )

        if flag:
            if response.json():
                errorCode = response.json()['errorCode']
                if errorCode != 0:
                    raise SDKException(
                        'Response',
                        '101',
                        'Error Code: "{0}"'.format(errorCode)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def disable_rc(self) -> None:
        """Disable the remote cache.

        This method sends a request to disable the remote cache on the client.
        If the operation fails or the response contains a non-zero error code,
        an SDKException is raised.

        Raises:
            SDKException: If the request fails or the response contains a non-zero error code.

        Example:
            >>> remote_cache = RemoteCache(...)
            >>> remote_cache.disable_rc()
            # If an error occurs, SDKException will be raised
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['SOFTWARE_CACHE'] + f"/{self.client_object.client_id}", {'enabled': False}
        )

        if flag:
            if response.json():
                errorCode = response.json()['errorCode']
                if errorCode != 0:
                    raise SDKException(
                        'Response',
                        '101',
                        'Error Code: "{0}"'.format(errorCode)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def update_associations(self, associations: List[Dict[str, Any]]) -> None:
        """Update the remote cache associations with specified clients or client groups.

        Args:
            associations: A list of dictionaries, each representing a client or client group association.
                Each dictionary should contain:
                    - name (str): Name of the client or client group.
                    - id (int): ID of the client or client group.
                    - type (int): 1 for client group, 0 for client.
                    - opType (str): "ADD" to add association, "DELETE" to remove association.

        Raises:
            SDKException: If updating remote cache details fails due to an error response.

        Example:
            >>> associations = [
            ...     {"name": "ClientA", "id": 101, "type": 0, "opType": "ADD"},
            ... ]
            >>> remote_cache = RemoteCache(...)
            >>> remote_cache.update_associations(associations)

        """

        request_json = {}
        request_json['associations'] = associations

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['SOFTWARE_CACHE'] + f"/{self.client_object.client_id}", request_json
        )

        if flag:
            if response.json():
                errorCode = response.json()['errorCode']
                if errorCode != 0:
                    raise SDKException(
                        'Response',
                        '101',
                        'Error Code: "{0}"'.format(errorCode)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def delete_remote_cache(self) -> None:
        """Delete the remote cache.

        This method sends a DELETE request to delete the remote cache.
        If the operation fails or the response contains a non-zero error code, an SDKException is raised.

        Raises:
            SDKException: If the remote cache deletion fails or the response contains a non-zero error code.

        Example:
            >>> remote_cache = RemoteCache(...)
            >>> remote_cache.delete_remote_cache()
            # If an error occurs, SDKException will be raised.

        """
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._services['SOFTWARE_CACHE']+f"/{self.client_object.client_id}"
        )

        if flag:
            if response.json():
                errorCode = response.json()['errorCode']
                if errorCode != 0:
                    raise SDKException(
                        'Response',
                        '101',
                        'Error Code: "{0}"'.format(errorCode)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def get_all_remote_cache(self) -> List[Dict[str, Any]]:
        """Retrieve all remote cache names and their details.

        This method fetches the list of remote software caches configured in the Commcell.
        The returned value is either a list of cache detail dictionaries or an empty list
        if no caches are found.

        Returns:
            A list of dictionaries containing remote cache details, or an empty list if no caches exist.

        Raises:
            SDKException: If the response from the Commcell is invalid or an error occurs.

        Example:
            >>> remote_cache = RemoteCache(...)
            >>> caches = remote_cache.get_all_remote_cache()
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['SOFTWARE_CACHE']
        )

        if flag:
            if response.json():
                return response.json()['softwareCacheDetailList']
            elif response.status_code == 200:
                return []
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')