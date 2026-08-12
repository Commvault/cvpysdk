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

"""Utilities class for Activate application : Compliance Search

ComplianceSearchUtils:  Class for compliance search related operations support

ExportSets: Class for representing all the export sets associated with the commcell

ExportSet:  Class for an instance of a single Export set of the commcell

Export: Class for an instance of a single Export of the commcell


ComplianceSearchUtils
============

    __init__()                          --  Initializes the Compliance search utility class

    _response_not_success()             --  Helper method to raise exception when response is not 200 (ok)

    do_compliance_search()              --  Method to run a compliance search with the search text provided


ExportSets
============

    __init__()                          --  Initializes the ExportSets class

    _response_not_success()             --  Helper method to raise exception when response is not 200 (ok)

    _get_export_sets()                  --  Method to call the API and fetch all the export sets
                                            from the commcell environment

    refresh()                           --  Method to refresh all the properties of the class ExportSets

    add()                               --  Method to create an export set to the commcell environment

    has()                               --  Method to check if the export set exists or not

    get()                               --  Method to get the export set

    delete()                            --  Method to delete the export set

ExportSet
============

    __init__()                          --  Initializes the ExportSet class

    _response_not_success()             --  Helper method to raise exception when response is not 200 (ok)

    refresh()                           --  Method to refresh all the properties of the class ExportSet

    _get_all_exports()                  --  Method to fetch all the exports for the export set

    share()                             --  Method to share the export set with the user or user group

    has()                               --  Method to check if the export exists or not

    get()                               --   Method to get the export

    delete()                            --  Method to delete the export

    export_items_to_set()               --  Method to export items/documents to the export set

    select()                            --  Static Method to randomly pick user input
                                            amount of items from the search result items

ExportSet Attributes
-----------------------

    **properties**                      --  return all the properties of the export set

    **export_set_full_name**            --  return the export set full name

    **export_set_name**                 --  return the export set name

    **export_set_comment**              --  return the export set comment

    **export_set_id**                   --  return the export set ID

    **export_set_guid**                 --  return the export set GUID

    **export_set_owner_info**           --  return the export set owner info


Export
============

    __init__()                          --  Initializes the Export class

    _response_not_success()             --  Helper method to raise exception when response is not 200 (ok)

    refresh()                           --  Method to refresh all the properties of the class Export

    download_export()                   --  Method to download the exported items to a zip file

"""
import copy
import base64
import os.path
import random
import requests

from cvpysdk.exception import SDKException
from cvpysdk.activateapps.constants import ComplianceConstants


class ComplianceSearchUtils():
    """Class for compliance search related operations support"""

    def __init__(self, commcell):
        """Initializes the Compliance search utility class"""
        self._commcell = commcell
        self._index_servers = commcell.index_servers
        self._cvpysdk_object = commcell._cvpysdk_object
        self._services = commcell._services
        self._update_response_ = commcell._update_response_
        self._users = commcell.users
        self._export_sets = ExportSets(commcell)
        self._do_search_api = self._services["DO_COMPLIANCE_SEARCH"]

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

            Raises:
                SDKException:
                    Response was not success
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def do_compliance_search(self, search_text, index_server_name=None,
                             page_size=50, app_type=ComplianceConstants.AppTypes.FILE_SYSTEM):
        """Method to run a compliance search with the search text provided

            Args:
                search_text         (str)   -   Search text to be searched on the Compliance search
                index_server_name   (str)   -   Index server name on which the search has to be executed
                page_size           (int)   -   Search result page size value (To Fetch all HITS - 0)
                                                Default: 50
                app_type            (str)   -   ComplianceConstants.AppTypes Enum values
                                                Default: FILE_SYSTEM

            Returns:
                (list)  -   List of all the search result items with the metadata and SOLR fields
                Example :
                    [ {
                        "FileName": <name>,
                        "SizeKB": <size>...,
                        <name>: <key>
                    },
                    {
                        "FileName": <name>,
                        "SizeKB": <size>...,
                        <name>: <key>
                    }... ]

            Raises:
                    SDKException:
                        Response was not success

        """
        self._index_servers.refresh()
        search_request = copy.deepcopy(ComplianceConstants.COMPLIANCE_SEARCH_JSON)
        if index_server_name:
            if not self._index_servers.has(index_server_name):
                raise SDKException('IndexServers', '102')
            search_request["listOfCIServer"][0]["cloudID"] = self._index_servers.get(index_server_name).cloud_id
        else:
            del search_request["listOfCIServer"]
        search_request["advSearchGrp"]["cvSearchKeyword"]["keyword"] = search_text
        search_request["userInformation"]["userGuid"] = self._users.get(self._commcell.commcell_username).user_guid
        if app_type in ComplianceConstants.FILE_TYPES:
            search_request["advSearchGrp"]["galaxyFilter"][0]["applicationType"] = ComplianceConstants.FILE_TYPE
            search_request["advSearchGrp"][ComplianceConstants.FILE_FILTERS_KEY] = ComplianceConstants.FILE_FILTERS
            search_request["advSearchGrp"][ComplianceConstants.COMMON_FILTER] = ComplianceConstants.COMMON_FILTERS
            custom_facet = copy.deepcopy(ComplianceConstants.FILE_FACET)
            if app_type != ComplianceConstants.AppTypes.FILE_SYSTEM:
                custom_facet = copy.deepcopy(ComplianceConstants.CUSTOM_FACET)
                custom_facet[0]["name"] = ComplianceConstants.CUSTOM_FACETS_NAME[app_type]
                if app_type == ComplianceConstants.AppTypes.TEAMS:
                    search_request["searchProcessingInfo"]["queryParams"].append(
                        {
                            "param": "RESPONSE_FIELD_LIST",
                            "value": ComplianceConstants.RESPONSE_FIELD_LIST
                        },
                    )
                if app_type == ComplianceConstants.AppTypes.SHAREPOINT:
                    search_request["searchProcessingInfo"]["queryParams"].append(
                        {
                            "param": "RESPONSE_FIELD_LIST",
                            "value": ComplianceConstants.RESPONSE_FIELD_LIST_SHAREPOINT
                        },
                    )
                custom_facet[1]["stringParameter"][0]["name"] = ComplianceConstants.CUSTOM_FACETS[app_type]
            search_request["facetRequests"][ComplianceConstants.FACET_KEY] = custom_facet
        elif app_type in ComplianceConstants.EMAIL_TYPES:
            search_request["advSearchGrp"]["galaxyFilter"][0]["applicationType"] = ComplianceConstants.EMAIL_TYPE
            search_request["advSearchGrp"][ComplianceConstants.EMAIL_FILTERS_KEY] = {
                "usermailbox": app_type == ComplianceConstants.AppTypes.EXCHANGE,
                "journalmailbox": app_type == ComplianceConstants.AppTypes.EXCHANGE_JOURNAL,
                "smtpmailbox": app_type == ComplianceConstants.AppTypes.EXCHANGE_JOURNAL
            }
        else:
            raise SDKException('ComplianceSearch', '107')
        if page_size == 0:
            flag, response = self._cvpysdk_object.make_request('POST', self._do_search_api, payload=search_request)
            if flag and response.json() and "totalHits" in response.json().get("proccessingInfo"):
                page_size = max(response.json()["proccessingInfo"]["totalHits"], 50)
        search_request["searchProcessingInfo"]["pageSize"] = page_size
        flag, response = self._cvpysdk_object.make_request('POST', self._do_search_api, payload=search_request)
        if flag:
            if response.json():
                if "searchResult" in response.json():
                    if "resultItem" in response.json()["searchResult"]:
                        return response.json()["searchResult"]["resultItem"]
                return []
            raise SDKException('Response', '102')
        else:
            self._response_not_success(response)


class ExportSets():
    """Class for representing all the export sets associated with the commcell"""

    def __init__(self, commcell):
        """Initializes the ExportSets class"""
        self._commcell = commcell
        self._cvpysdk_object = None
        self._services = None
        self._update_response_ = None
        self._user_guid = None
        self._add_export_set_api = None
        self._add_export_set_json_req = None
        self._get_export_sets_api = None
        self._get_export_sets_json_req = None
        self._delete_export_set_api = None
        self._delete_export_set_json_req = None
        self._all_export_set = None
        self.refresh()

    def _get_export_sets(self):
        """Method to call the API and fetch all the export sets from the commcell environment"""
        flag, response = self._cvpysdk_object.make_request(
            method="POST", url=self._get_export_sets_api, payload=self._get_export_sets_json_req)
        if flag:
            if response.json() and "containers" in response.json():
                containers = response.json()['containers']
                for container in containers:
                    self._all_export_set.update(
                        {container["containerName"]: container})
        else:
            self._response_not_success(response)

    def refresh(self):
        """Method to refresh all the properties of the class ExportSets"""
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_
        self._user_guid = self._commcell.users.get(self._commcell.commcell_username).user_guid
        self._all_export_set = {}
        self._get_export_sets_api = self._services['GET_EXPORT_SETS']
        self._get_export_sets_json_req = \
            {
                "getContainerOptions": 0,
                "entityType": 9503,
                "userGuid": self._user_guid,
                "attribute": {
                    "all": True
                }
            }
        self._add_export_set_api = self._services['ADD_EXPORT_SET']
        self._add_export_set_json_req = \
            {
                "entityType": 9503,
                "operationType": 1,
                "userGuid": self._user_guid,
                "fromSite": 2,
                "container": {
                    "containerType": 9503,
                    "containerName": None,
                    "containerOwnerType": 1,
                    "comment": "Export set created from CvPySDK"
                }
            }
        self._delete_export_set_api = self._services['DELETE_EXPORT_SET']
        self._delete_export_set_json_req = \
            {
                "entityType": 9503,
                "containers": None
            }
        self._get_export_sets()

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

            Raises:
                SDKException:
                    Response was not success
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def add(self, export_set_name, comment=None):
        """Method to create an export set to the commcell environment

            Args:
                export_set_name     (str)   -   Export set name for the newly created export set
                comment             (str)   -   Export set description fot the newly created export set

            Returns:
                ExportSet instance for the newly created export set

        """
        if not self.has(export_set_name):
            add_export_set_json_req = copy.deepcopy(self._add_export_set_json_req)
            add_export_set_json_req['container']['containerName'] = export_set_name
            if comment:
                add_export_set_json_req['container']['comment'] = comment
            flag, response = self._cvpysdk_object.make_request(
                method="POST", url=self._add_export_set_api, payload=add_export_set_json_req)
            if flag:
                if response.json() and "container" in response.json():
                    self.refresh()
                    return self.get(export_set_name=export_set_name)
                raise SDKException('Response', '102')
            else:
                self._response_not_success(response)

    def has(self, export_set_name):
        """Method to check if the export set exists or not

            Args:
                export_set_name (str)   -   Export set name to be checked

            Returns:
                Returns True if export set exists in the environment or False otherwise

        """
        return export_set_name in self._all_export_set

    def get(self, export_set_name):
        """Method to get the export set

            Args:
                export_set_name (str)   -   Export set name to get

            Returns:
                ExportSet instance for the export set with the given name if found else raises Exception

        """

        if self.has(export_set_name):
            return ExportSet(self._commcell, self._all_export_set[export_set_name])
        raise SDKException('ComplianceSearch', '106')

    def delete(self, export_set_name):
        """Method to delete the export set

            Args:
                export_set_name (str)   -   Export set name to be deleted

            Returns:
                Returns True if delete successfully else raises error

            Raises:
                SDKException:
                    Response was not success

        """
        if not self.has(export_set_name):
            raise SDKException("ComplianceSearch", "105")
        delete_json = copy.deepcopy(self._delete_export_set_json_req)
        delete_json['containers'] = [self._all_export_set[export_set_name]]
        flag, response = self._cvpysdk_object.make_request("POST", self._delete_export_set_api, delete_json)
        if flag:
            if response.json() and "errList" in response.json() and len(response.json()["errList"]) == 0:
                self.refresh()
                return True
        self._response_not_success(response)


class ExportSet():
    """Class for an instance of a single Export set of the commcell"""

    def __init__(self, commcell, export_set_properties):
        """Initializes the ExportSet class"""
        self._commcell = commcell
        self._export_set_properties = export_set_properties
        self._cvpysdk_object = None
        self._services = None
        self._update_response_ = None
        self._user_guid = None
        self._get_exports_api = None
        self._get_export_json_req = None
        self._export_items_api = None
        self._export_items_json_req = None
        self._share_export_set_api = None
        self._exports_list = None
        self._all_exports = None
        self._delete_export_api = None
        self._delete_export_json_req = None
        self.refresh()

    def refresh(self):
        """Method to refresh the properties of the class ExportSet"""
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_
        self._user_guid = self._commcell.users.get(self._commcell.commcell_username).user_guid
        self._get_exports_api = self._services['GET_EXPORTS']
        self._share_export_set_api = self._services['SECURITY_ASSOCIATION']
        self._get_export_json_req = \
            {
                "containerOpReq": {
                    "entityType": 9503,
                    "operationType": 1,
                    "userGuid": self._user_guid,
                    "fromSite": 0,
                    "container": self._export_set_properties
                },
                "filter": {},
                "pagingData": {
                    "startIndex": 0,
                    "fetchEmails": True,
                    "pageSize": 50,
                    "fetchFiles": True,
                    "orderByClause": "CreateTime desc"
                }
            }
        self._export_items_api = self._services['EXPORT_ITEM_TO_SET']
        self._export_items_json_req = \
            {
                "complianceData": {
                    "mode": 2,
                    "restoreType": 2,
                    "downLoadDesc": None,
                    "destContainer": None,
                    "originatingContainer": {
                        "containerOwnerType": 1
                    },
                    "options": {
                        "zipEML": True,
                        "retentionInDays": 30}
                },
                "onlineData": {
                    "downloadStatus": 0
                },
                "listOfItems": {
                    "resultItem": None
                }
            }
        self._delete_export_api = self._services['GET_EXPORTS']
        self._delete_export_json_req = \
            {
                "operationType": 2,
                "container": None,
                "downloadItems": {
                    "items": None
                },
                "tagModifyRequest": {
                    "operationType": 2
                }
            }
        self._all_exports = {}
        self._get_all_exports()

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

        Raises:
            SDKException:
                Response was not success

        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def _get_all_exports(self):
        """Method to fetch all the exports for the export set"""
        flag, response = self._cvpysdk_object.make_request(
            method="POST", url=self._get_exports_api, payload=self._get_export_json_req)
        if flag:
            if (response.json() and "totalHits" in response.json()
                    and int(response.json()['totalHits']) != 0):
                items = response.json()['downloadItems']['items']
                for item in items:
                    self._all_exports.update(
                        {item["description"]: item})
            else:
                self._all_exports = {}
        else:
            self._response_not_success(response)

    def share(self, user_or_user_group_name=None, permissions=None, mode=2):
        """Method to share the export set with the user or user group provided

            Args:
                user_or_user_group_name (str)       -   User or user group with which export set has to be shared
                permissions             (list/str)  -   List or comma separated permissions that need
                                                        to be set to the user/ user group
                mode                    (int)       -   to add (2), remove (3) or overwrite (1) the permissions
                                                        Default : Add (2)

            Returns:
                Returns True if share worked fine else raises an Exception

        """
        if isinstance(permissions, str):
            permissions = permissions.split(",")
        share_json = copy.deepcopy(ComplianceConstants.EXPORT_SET_SHARE_REQUEST_JSON)
        unshare = False
        user_details = {}
        if user_or_user_group_name is None:
            unshare = True
        elif self._commcell.users.has_user(user_or_user_group_name):
            user_details = {
                "userId": int(self._commcell.users.get(user_or_user_group_name).user_id),
                "userName": user_or_user_group_name,
                "_type_": 13
            }
        elif self._commcell.user_groups.has_user_group(user_or_user_group_name):
            user_details = {
                "groupId": int(self._commcell.user_groups.get(user_or_user_group_name).user_group_id),
                "userGroupName": user_or_user_group_name,
                "_type_": 15
            }
        else:
            raise SDKException('ComplianceSearch', '101')
        if unshare:
            share_json['securityAssociations']['associations'] = []
            share_json['securityAssociations']['associationsOperationType'] = 1
        else:
            share_json['securityAssociations']['associationsOperationType'] = mode
            share_json['securityAssociations']['associations'][0]['userOrGroup'] = [user_details]
            if permissions is None:
                share_json['securityAssociations']['associations'][0]['properties']['permissions'] = []
                permissions = [["View", "Download"], list(ComplianceConstants.PERMISSIONS.keys())][mode//3]
            if mode == 3:
                share_json['securityAssociations']['associations'][0]['properties']['permissions'] = []
            for permission in permissions:
                try:
                    share_json['securityAssociations']['associations'][0]['properties']['permissions'].append(
                        ComplianceConstants.PERMISSIONS[permission]
                    )
                except KeyError:
                    raise SDKException('ComplianceSearch', '102')
        share_json['entityAssociated']['entity'][0]['downloadSetId'] = self.export_set_id
        flag, response = self._cvpysdk_object.make_request("POST", self._share_export_set_api, share_json)
        if flag:
            if response.json() and "response" in response.json():
                if response.json()['response'][0]['errorCode'] == 0:
                    self.refresh()
                    return True
        self._response_not_success(response)

    def has(self, export_name):
        """Method to check if the export exists or not

            Args:
                export_name (str)   -   Export name to be checked

            Returns:
                Returns True if export exists in the environment or False otherwise

        """
        return export_name in self._all_exports

    def get(self, export_name):
        """Method to get the export

            Args:
                export_name (str)   -   Export name to get

            Returns:
                Export class instance for the export with the given name if found else returns None

        """
        if self.has(export_name):
            return Export(self._commcell, self._all_exports[export_name])
        raise SDKException('ComplianceSearch', '103')

    def delete(self, export_name):
        """Method to delete the export

            Args:
                export_name (str)   -   Export name to be deleted

            Returns:
                Returns True if delete successfully else raises error

            Raises:
                SDKException:
                    Response was not success

        """
        if not self.has(export_name):
            raise SDKException("ComplianceSearch", "103")
        delete_json = copy.deepcopy(self._delete_export_json_req)
        delete_json["downloadItems"]["items"] = [self._all_exports[export_name]]
        delete_json["container"] = self.properties
        flag, response = self._cvpysdk_object.make_request("POST", self._delete_export_api, delete_json)
        if flag:
            if response.json() and "errList" in response.json() and len(response.json()["errList"]) != 0:
                if response.json()["errList"][0]["errorCode"] != 0:
                    raise SDKException("ComplianceSearch", "104",
                                       response.json()["errList"][0].get("errLogMessage"))
            return True
        self._response_not_success(response)

    def export_items_to_set(self, export_name, export_items, export_type=ComplianceConstants.ExportTypes.CAB):
        """Method to export items/documents to the export set

            Args:
                export_name     (str)   -   Export name for the exported items
                export_items    (list)  -   List of search result items which needs to be export
                export_type     (str)   -   ComplianceConstants.ExportTypes Enum values
                                            Default: CAB

            Returns:
                Returns the restore job ID for the export operation

            Raises:
                SDKException:
                    Response was not success

        """
        if export_type not in ComplianceConstants.RESTORE_TYPE:
            raise SDKException('ComplianceSearch', '108')
        export_items_json_req = copy.deepcopy(self._export_items_json_req)
        export_items_json_req['complianceData']['restoreType'] = ComplianceConstants.RESTORE_TYPE[export_type]
        export_items_json_req['complianceData']['downLoadDesc'] = export_name
        export_items_json_req['complianceData']['destContainer'] = self.properties
        export_items_json_req['listOfItems']['resultItem'] = export_items
        flag, response = self._cvpysdk_object.make_request(
            method="POST", url=self._export_items_api, payload=export_items_json_req)
        if flag:
            if response.json() and "downloadId" in response.json() and "jobId" in response.json():
                self.refresh()
                return response.json()['jobId']
            raise SDKException('Response', '102')
        else:
            self._response_not_success(response)

    @staticmethod
    def select(result_items, no_of_files=0, export_all=False):
        """Static Method to randomly pick user input amount of items from the search result items

            Args:
                result_items    (list)      -   List of all the search result items
                no_of_files     (int)       -   Number of items to be selected
                export_all      (bool)      -   if all the items needs to be selected or not

            Returns:
                List of randomly selected (no_of_files) items from the (result_items)

        """
        if export_all or len(result_items) < no_of_files:
            return result_items
        return list(random.sample(result_items, no_of_files))

    @property
    def properties(self):
        """Method to return all the properties of the export set

            Returns:
                Dict of the properties of the export set as received from the API (rawdata)

        """
        return self._export_set_properties

    @property
    def export_set_full_name(self):
        """Method to return the export set full name

            Returns:
                (str) export set full name

        """
        return self._export_set_properties['containerFullName']

    @property
    def export_set_name(self):
        """Method to return the export set name

            Returns:
                (str) export set name

        """
        return self._export_set_properties['containerName']

    @property
    def export_set_comment(self):
        """Method to return the export set comment

            Returns:
                (str) export set comment

        """
        return self._export_set_properties['comment']

    @property
    def export_set_id(self):
        """Method to return the export set ID

            Returns:
                (int) export set ID

        """
        return self._export_set_properties['containerId']

    @property
    def export_set_guid(self):
        """Method to return the export set Guid

            Returns:
                (str) export set Guid

        """
        return self._export_set_properties['containerGuid']

    @property
    def export_set_owner_info(self):
        """Method to return the export set Owner info

            Returns:
                (str) export set Owner info

        """
        return self._export_set_properties['ownerInfo']


class Export():
    """Class for an instance of a single Export of the export set"""

    def __init__(self, commcell, export_properties):
        """Initializes the Export class instance"""
        self._commcell = commcell
        self._export_set_properties = export_properties
        self._cvpysdk_object = None
        self._services = None
        self._update_response_ = None
        self._user_guid = None
        self._download_file_api = None
        self._download_via_stream = None
        self._download_file_json_req = None
        self.refresh()

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

        Raises:
            SDKException:
                Response was not success

        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def refresh(self):
        """Method to refresh the properties of the class Export"""
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_
        self._user_guid = self._commcell.users.get(self._commcell.commcell_username).user_guid
        self._download_file_api = self._services['DOWNLOAD_EXPORT_ITEMS']
        self._download_via_stream = self._services['DOWNLOAD_VIA_STREAM']
        self._download_file_json_req = \
            {
                "appTypeId": 200,
                "responseFileName": self._export_set_properties['description'],
                "fileParams": [
                    {
                        "name": self._export_set_properties['downLoadID'],
                        "id": 2
                    },
                    {
                        "name": "zip",
                        "id": 3
                    }
                ]
            }

    def download_export(self, download_folder):
        """Method to download the exported items to a zip file

            Args:
                download_folder     (str)   -   Path of the folder in which exported items zip file should be saved

            Returns:
                (str) path of the downloaded zip file

            Raises:
                SDKException:
                    Response was not success

        """
        flag, response = self._cvpysdk_object.make_request(
            method="POST", url=self._download_file_api, payload=self._download_file_json_req
        )

        if not flag or not response.json() or not response.json().get("fileContent"):
            self._response_not_success(response)

        file_content = response.json().get("fileContent", {})
        download_file = os.path.join(download_folder, file_content.get("fileName", ""))
        req_id = file_content.get("requestId")

        if not download_file or not req_id:
            raise SDKException('ComplianceSearch', '110')

        # Handle response with 'cloudUrl' or 'data'
        if 'cloudUrl' in response.json() or 'data' in file_content:
            if 'cloudUrl' in response.json():
                url = response.json().get('cloudUrl')
                cloud_file = requests.get(url)
                if cloud_file.status_code == 200:
                    file_data = cloud_file.content
                else:
                    raise SDKException('ComplianceSearch', '109')
            else:
                file_data = base64.b64decode(file_content['data'])
            with open(download_file, "wb") as f:
                f.write(file_data)
            return download_file
        else:
            # Handle download via stream API
            self._download_file_json_req.update({
                "requestId": req_id,
                "userInformation": {
                    "userGuid": self._user_guid,
                    "userName": self._commcell.commcell_username,
                }
            })

            flag, response = self._cvpysdk_object.make_request(
                method="POST", url=self._download_via_stream, payload=self._download_file_json_req, stream=True
            )

            if flag:
                try:
                    with open(download_file, "wb") as f:
                        for content in response.iter_content():
                            f.write(content)
                except Exception:
                    raise SDKException('Response', '102')
                return download_file
            else:
                self._response_not_success(response)
