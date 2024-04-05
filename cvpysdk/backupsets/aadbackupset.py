# -*- coding: utf-8 -*-
# pylint: disable=R1705, R0205

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
"""File for operating on an AD agent Backupset.

adbackupset is the only class defined in this file.

Function:
    azuread_browse_double_query     create browse options for objects in folder

    azuread_browse_double_query_adv    create browse options for objects attrbute

    azuread_browse_options_builder    build browse options for azure ad browse
Class:

    AzureADBackupset:  Derived class from Backuset Base class, representing a
                            Azure AD agent backupset, and to perform operations on that backupset

        _azuread_browse_basic : Do basic browse with option

        _azuread_browse_meta  : Get Azure ad folder meta information

        _azuread_browse_folder : Get Azure objects based on the folder type

        _adv_attributes : Get Azure AD object attribute

        browse() : Overwrite default browse operation

        _process_browse_repsonse : process the browse result

        azuread_get_metadata : create azure ad object meta data information

        __prepare_search_json : Prepare search json for search api request

        get_search_response : Get search response from search api

        view_attributes_url_builder : Build view attribute url

        get_view_attribute_response : Get view attribute response from view attribute url

"""


from __future__ import unicode_literals
import base64
from ..backupset import Backupset
from ..exception import SDKException


class AzureAdBackupset(Backupset):
    """ Azure AD agent backupset class """

    def _azuread_browse_basic(self, options):
        """ do basic browse activity with options
            Args:
                options    (dict)    browse option from impoort
                                adv_attributes    get object advanced attribute
            Return:
                count     (int)    return count from browse
                result    (list)    objects list from browse
            Raise:
                101    If browse return Nothing
        """
        options = self._prepare_browse_options(options)

        request_json = self._prepare_browse_json(options)
        request_json = self.azuread_browse_double_query(options, request_json)
        flag, response = self._cvpysdk_object.make_request("POST",
                                                           self._BROWSE,
                                                           request_json)
        if flag:
            count, result = self._process_browse_response(flag, response, options)
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))
        return count, result

    def _azuread_browse_meta(self, options):
        """ get basic browse related meta data
            Args:
                options    (dict)    browse option from impoort
            Return:
                azure_meta    (dict)    azure ad meta data from browse result
            Raise:
                None
        """
        if "meta" in options:
            azure_meta = options['meta']
        else:
            azure_meta = {}
        count, result = self._azuread_browse_basic(options)
        if len(result) == 1 and result[0]['objType'] == 1:
            newid = result[0]['commonData']['id']
            options['filters'] = [(_[0], newid, _[2]) for _ in options['filters']]
            name, metainfo = self.azuread_browse_obj_meta(result[0])
            azure_meta['root'] = metainfo
            options['meta'] = azure_meta
            self._azuread_browse_meta(options)
        else:
            for r_ in result:
                if r_['objType'] == 100:
                    options['filters'] = [("76", r_['commonData']['id'], "9"),
                                        ("125", "FOLDER")]
                    count_, metainfo_ = self._azuread_browse_basic(options)
                    for i_ in metainfo_:
                        name, metainfo = self.azuread_browse_obj_meta(i_)
                        azure_meta[name] = metainfo
                else:
                    name, metainfo = self.azuread_browse_obj_meta(r_)
                    azure_meta[name] = metainfo
        return azure_meta

    def _azuread_browse_folder(self, options):
        """ browse folder content
            Args:
                options    (dict)    browse option from impoort
            Return:
                count     (int)    return count from browse
                result    (list)    objects list from browse
            Raise:
                None
        """
        azure_meta_mapper = {
            "user" : { "displayname" : "Users", "browsetype" : 2, "browsestring" : "USER"},
            "group" : { "displayname" : "Groups", "browsetype" : 3, "browsestring": "GROUP"},
            "reg_app" : {"displayname" : "App registrations", "browsetype" : 5, "browsestring" : "APPLICATION"},
            "ent_app" : { "displayname" : "Enterprise applications","browsetype": 6, "browsestring" : "SERVICE_PRINCIPAL"},
            "ca_policy" : { "displayname" : "Policies","browsetype": 11, "browsestring" : "CONDITIONAL_ACCESS_POLICY"},
            "ca_name_location" : { "displayname" : "Named locations","browsetype": 12, "browsestring" : "NAMED_LOCATION"} ,
            "ca_auth_context" : { "displayname" : "Authentication context","browsetype": 13, "browsestring" : "AUTHENTICATION_CONTEXT"},
            "ca_auth_strength" : { "displayname" : "Authentication strengths","browsetype": 14, "browsestring" : "AUTHENTICATION_STRENGTH"},
            "role" : { "displayname" : "Roles","browsetype": 15, "browsestring" : "DIRECTORY_ROLE_DEFINITIONS"},
            "admin_unit" : { "displayname" : "Admin units","browsetype": 16, "browsestring" : "ADMINISTRATIVE_UNIT"}}
        azure_meta = options['meta']
        newid = azure_meta[azure_meta_mapper[options['folder']]['displayname']]['id']
        options['filters'] = [("76", newid, "9"),
                              ("125", azure_meta_mapper[options['folder']]['browsestring'])]
        if "search" in options:
            if isinstance(options['search'], dict):
                search_dict = options['search']
                if "obj_id" in search_dict:
                    options['filters'].append(("130", search_dict['obj_id']))
                if "source" in search_dict:
                    if search_dict['source'] == "AzureAD":
                        options['filters'].append(("128", "0"))
                    elif search_dict['source'] == "WinAD":
                        options['filters'].append(("128", "1"))
            else:
                options['filters'].append(("30", options['search']))

        del(options['folder'])
        del(options['meta'])
        del(options['path'])
        count, results = self._azuread_browse_basic(options)
        results = self._process_result_format(results)
        return count, results

    def browse(self, *args, **kwargs):
        """Browses the content of the Backupset.
            Args:
                args    list    args passed for browse
                kwargs    dict    dict passed for browse
            Return:
                count     (int)    return count from browse
                browse_result    (list)    objects list from browse
            Raise:
                None
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs
        options = self.azuread_browse_options_builder(options)
        azure_meta = self._azuread_browse_meta(options)
        options['meta'] = azure_meta
        count, browse_result = self._azuread_browse_folder(options)

        return count, browse_result

    def _process_browse_response(self, flag, response, options):
        """Retrieves the items from browse response.
            Args:
                flag    (bool)  --  boolean, whether the response was success or not
                response (dict)  --  JSON response received for the request from the Server
                options  (dict)  --  The browse options dictionary
            Returns:
                list - List of only the file / folder paths from the browse response
                dict - Dictionary of all the paths with additional metadata retrieved from browse
            Raises:
                SDKException:
                    if failed to browse/search for content
                    if response is empty
                    if response is not success
        """
        metadatas = []
        if flag:
            if response.json():
                response_json = response.json()
                if response_json and 'browseResponses' in response_json:
                    _browse_responses = response_json['browseResponses']
                    for browse_response in _browse_responses:
                        if "browseResult" in browse_response:
                            browse_result = browse_response['browseResult']
                            browseresulttcount = browse_result['totalItemsFound']
                            if 'dataResultSet' in browse_result:
                                result_set = browse_result['dataResultSet']
                    if not result_set and result_set != []:
                        raise SDKException('Backupset', '102',
                                           "Failed to browse for subclient backup content")
                    else:
                        for result in result_set:
                            metadata = self.azuread_get_metadata(result)
                            metadatas.append(metadata['azureADDataV2'])
            else:
                raise SDKException("Backupset", "102", "response is not valid")
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))
        return browseresulttcount, metadatas

    def _process_result_format(self, results):
        """
        process the browse result to original data format
        Args:
            results     (list)  search results list
        return
            results     (list)  search results list
        """
        for _ in results:
            _['azureid'] =  _['commonData']['id'].replace("x","-")
        return results
    def azuread_get_metadata(self, result):
        """ Get azure ad meta data for browse result
            Args:
                result    (list)    objects list from browse
            Return:
                metadata    (dict)    azure ad browse meta data
            Raise:
                110    can't find meta data
        """
        metadata = {}
        if "advancedData" in result:
            if "browseMetaData" in result['advancedData']:
                metadata = result['advancedData']['browseMetaData']
                if "azureADDataV2" in metadata:
                    metadata['azureADDataV2']['guid'] = result['advancedData']['objectGuid']
                else:
                    raise SDKException('Backupset', '110',
                                       "Azure AD meta data is not found")
        return metadata

    def azuread_browse_obj_meta(self, obj_):
        """ get azure ad obj meta info
            Args:
                obj_    (obj)    azuare ad object
            Return:
                name    (str)    azure ad display name
                metainfo     (dict)    azure ad browse meta data
            Raise:
                None
        """
        name = obj_['commonData']['displayName']
        metainfo = {}
        metainfo['id'] = obj_['commonData']['id']
        metainfo['azureid'] = metainfo['id'].replace("x", "-")
        metainfo['name'] = name
        metainfo['guid'] = obj_['guid']
        metainfo['type'] = obj_['objType']
        return name, metainfo

    def azuread_browse_double_query(self, options, request_json):
        """ create request json for azure ad based on double query
            Args:
                options    (dict)    browse option from impoort
                request_json    (json)    request json file from basic request class
            Return:
                request_json    (json)    request json with addittional options
            Raise:
                None
        """
        request_json['queries'] = [{
                        "type": "0",
                        "queryId": "0",
                        "whereClause" :[],
                        "dataParam": {
                            "sortParam": {
                                "ascending": True,
                                "sortBy": [126]
                            },
                            "paging": {
                                "pageSize": int(options['page_size']),
                                "skipNode": int(options['skip_node']),
                                "firstNode": 0
                            }
                        }
                    },
                    {   "type": "1",
                        "queryId": "1",
                        "whereClause": [],
                        "aggrParam"  : {'aggrType': 4,
                                        'field': 0}}]

        if options['filters']:
            for filter_ in options['filters']:
                filter_dict = {
                    'connector': 0,
                    'criteria': {
                        'field': filter_[0],
                        'values': [filter_[1]]}}
                if len(filter_) == 3:
                    filter_dict['criteria']['dataOperator'] = int(filter_[2])
                if filter_[0] == "125":
                    del (filter_dict['connector'])
                request_json['queries'][0]['whereClause'].append(filter_dict)
                request_json['queries'][1]['whereClause'].append(filter_dict)

        del(request_json['paths'])
        return request_json

    def azuread_browse_options_builder(self, options):
        """ build browse options
            Args:
                options    (dict)    browse option from impoort
            Return:
                options    (list)    create formated options based on import
            Raise:
                None
        """
        if "filters" not in options:
            options['filters'] = [("76", "00000000000000000000000000000001", "9"),
                                  ("76", "00000000000000000000000000000001", "9")]
        if "operation" not in options:
            options['operation'] = "browse"
            options['page_size'] = 20
            options['skip_node'] = 0
        return options

    def __prepare_search_json(self, options):
        """
        performs view_properties (Cvpysdk Api call)
        Args:
            options     (dict)      example {"to_time":(epoch) ,
                                            "subclient_id":(string/optional),
                                            "attribute": "attribute to perform search "}
            Return:     (dict)      view properties
        """
        options["subclient_id"] = self.subclients.get("default").subclient_id

        request_json = {
            "mode": 4,
            "advSearchGrp": {
                "commonFilter": [
                    {
                        "filter": {
                            "interFilterOP": 2,
                            "filters": [
                                {
                                    "field": "CISTATE",
                                    "intraFieldOp": 0,
                                    "fieldValues": {
                                        "values": [
                                            "1"
                                        ]
                                    }
                                },
                                {
                                    "field": "IS_VISIBLE",
                                    "intraFieldOp": 0,
                                    "fieldValues": {
                                        "values": [
                                            "true"
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ],
                "fileFilter": [
                    {
                        "interGroupOP": 2,
                        "filter": {
                            "interFilterOP": 2,
                            "filters": [
                                {
                                    "field": "BACKUPTIME",
                                    "intraFieldOp": 0,
                                    "fieldValues": {
                                        "values": [
                                            "0",
                                            str(options["to_time"])
                                        ]
                                    }
                                },
                                {
                                    "field": "DATA_TYPE",
                                    "intraFieldOp": 0,
                                    "fieldValues": {
                                        "values": [
                                            "1"
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ],
                "emailFilter": [],
                "galaxyFilter": [
                    {
                        "appIdList": [
                            int(options["subclient_id"])
                        ]
                    }
                ],
                "cvSearchKeyword": {
                    "isExactWordsOptionSelected": False,
                    "keyword": str(options["attribute"]) + "*"
                }
            },
            "searchProcessingInfo": {
                "resultOffset": 0,
                "pageSize": 15,
                "queryParams": [
                    {
                        "param": "ENABLE_MIXEDVIEW",
                        "value": "true"
                    },
                    {
                        "param": "ENABLE_NAVIGATION",
                        "value": "on"
                    },
                    {
                        "param": "ENABLE_DEFAULTFACETS",
                        "value": "false"
                    },
                    {
                        "param": "RESPONSE_FIELD_LIST",
                        "value": "CONTENTID,CV_TURBO_GUID,PARENT_GUID,AFILEID,AFILEOFFSET,"
                                 "COMMCELLNO,MODIFIEDTIME,SIZEINKB,DATA_TYPE,AD_DISPLAYNAME,"
                                 "AD_ID,AD_OBJECT_TYPE,BACKUPTIME,AD_FLAGS,CISTATE,DATE_DELETED,"
                                 "AD_MAIL,AD_MAILNICKNAME,AD_PROXY_ADDRESSES,AD_BUSINESS_PHONES,"
                                 "AD_CITY,AD_COUNTRY,AD_DELETED_TIME,AD_POSTALCODE,AD_STATE,"
                                 "AD_STREET_ADDRESS,AD_LAST_DIR_SYNC_TIME,"
                                 "AD_COUNTRY_LETTER_CODE,AD_DIR_SYNC_ENABLED,AD_MKT_NOTIFY_MAILS,"
                                 "AD_TENANT_OBJECT_TYPE,AD_PREFER_LANG,AD_SEC_NOTIFY_MAILS,"
                                 "AD_SEC_NOTIFY_PHONES,AD_TECH_NOTIFY_MAILS,AD_TELEPHONE_NR,"
                                 "AD_CREATED_TIME,AD_DESCRIPTION,AD_GROUP_TYPES,AD_MAIL_ENABLED,"
                                 "AD_VISIBILITY,AD_SOURCE_TYPE,AD_AZURE_APP_ID,AD_HOME_PAGE_URL,"
                                 "AD_TAGS,AD_AZURE_APP_DISPLAY_NAME,AD_APP_OWNER_ORGID,"
                                 "AD_REPLY_URLS,AD_PUBLISHER_NAME,AD_SERVICE_PRINCIPAL_NAMES"
                    },
                    {
                        "param": "DO_NOT_AUDIT",
                        "value": "true"
                    },
                    {
                        "param": "COLLAPSE_FIELD",
                        "value": "AD_ID"
                    },
                    {
                        "param": "COLLAPSE_SORT",
                        "value": "BACKUPTIME DESC"
                    }
                ],
                "sortParams": [
                    {
                        "sortDirection": 0,
                        "sortField": "AD_DISPLAYNAME"
                    }
                ]
            },
            "facetRequests": {
                "facetRequest": [
                    {
                        "name": "AD_OBJECT_TYPE"
                    }
                ]
            }
        }

        return request_json

    def get_search_response(self, job_time, attribute):
        """
            Searches for jobs based on the specified parameters.

            This method performs a search operation for jobs using the
            given job time, display name and application ID.
            Args:
                job_time    (str)   The job ends time.
                attribute   (str)  Attribute to search for.
            Return:
                The response contains the search results.
            Raises:
                SDKException: If there is a bad request
                or no object found with the specified display name.
        """

        uri = self._services["DO_WEB_SEARCH"]
        options = {"to_time": job_time, "attribute": attribute}
        request_json = self.__prepare_search_json(options)
        flag, response = self._cvpysdk_object.make_request('POST', uri, request_json)
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))
        response = response.json()
        if response["proccessingInfo"]["totalHits"] == 0:
            raise SDKException('Backupset', '107', "no result found with specified attribute")
        return response

    def view_attributes_url_builder(self,
                                    job_time,
                                    display_name):
        """
        Builds a URL for viewing attributes based on the specified parameters.

        This method constructs a URL for viewing attributes of an
        object identified by the given job time and display name.
        Args:
            job_time    (str)   The job time.
            display_name    (str)   The display name of the object.
        Return:
            The URL for viewing attributes.
        """

        subclient_id = self.subclients.get("default").subclient_id

        try:
            search_response = self.get_search_response(job_time=job_time, attribute=display_name)
            afile_id = search_response["searchResult"]["resultItem"][0]["aFileId"]
            afile_offset = search_response["searchResult"]["resultItem"][0]["aFileOffset"]
            commcell_no = search_response["searchResult"]["resultItem"][0]["commcellNo"]

            op = "dGVtcC5qc29u"  # any filename.json for view properties call
            # encoding string to base64
            stub_info = str('2:' + str(commcell_no) + ':0:' +
                            str(afile_id) + ':' + str(afile_offset))
            stub_info = stub_info.encode("ascii")
            stub_info = base64.b64encode(stub_info)
            stub_info = stub_info.decode("ascii")

            url = self._services['VIEW_PROPERTIES'] % (str(self._agent_object.agent_id),
                                                       stub_info,
                                                       op,
                                                       str(subclient_id),
                                                       '1')
            return url
        except SDKException as e:
            raise SDKException('Backupset', '107',
                               f"No result found with specified attribute {e.exception_message}")

    def get_view_attribute_response(self,
                                    job_time,
                                    display_name):
        """
        Retrieves view attributes based on the specified parameters.

        This method retrieves the view attributes of an
        object identified by the given job time and display name.
        Args:
            job_time    (int)   The job time.
            display_name    (string)    The display name of the object.
        Return:
            (dict)  The JSON response contains the view attributes.
        Raises:
            SDKException: If there is an error while retrieving the view attributes.
        """
        try:
            url = self.view_attributes_url_builder(display_name=display_name,
                                                   job_time=job_time)

            flag, response = self._cvpysdk_object.make_request('GET', url)
            if not flag:
                raise SDKException('Response', '101', "Response was not success")
            if not response:
                raise SDKException('Response', '102', "Response received is empty")
            return response.json()
        except Exception as e:
            raise SDKException('Backupset', '107', f"No result found {e.exception_message}")
