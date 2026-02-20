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
from typing import Dict, Any, Tuple, List

class AzureAdBackupset(Backupset):
    """
    Azure AD agent backupset class for managing and browsing Azure Active Directory backup data.

    This class provides specialized methods for interacting with Azure AD backupsets, enabling
    users to browse, query, and retrieve metadata and folder information from Azure AD backups.
    It supports building search and view attribute requests, processing browse responses, and
    formatting results for further analysis.

    Key Features:
        - Basic, meta, and folder-level browsing of Azure AD backup data
        - Metadata retrieval and object-level metadata browsing
        - Double query support for advanced browsing scenarios
        - Options builder for constructing browse requests
        - Preparation of search JSON for custom queries
        - Retrieval of search and view attribute responses based on job time and attributes
        - URL builder for view attributes
        - Processing and formatting of browse results

    #ai-gen-doc
    """

    def _azuread_browse_basic(self, options: Dict[str, Any]) -> Tuple[int, List[Any]]:
        """Perform a basic browse operation on Azure AD objects using the provided options.

        This method executes a browse activity with the specified options, returning the count of 
        objects found and a list of the resulting objects. Advanced attributes can be included in 
        the options to retrieve additional object details.

        Args:
            options: Dictionary containing browse options, such as filters and advanced attributes.

        Returns:
            A tuple containing:
                - count (int): The number of objects returned from the browse operation.
                - result (list): List of objects retrieved from Azure AD.

        Raises:
            SDKException: If the browse operation returns no results (error code 101).

        Example:
            >>> options = {
            ...     "object_type": "User",
            ...     "adv_attributes": ["displayName", "mail"]
            ... }
            >>> count, result = azuread_backupset._azuread_browse_basic(options)
            >>> print(f"Found {count} users")
            >>> for user in result:
            ...     print(user)
        #ai-gen-doc
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

    def _azuread_browse_meta(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve Azure AD browse metadata based on the provided options.

        This method processes the browse options to extract and organize metadata 
        from Azure Active Directory browse results. It updates the options dictionary 
        with relevant filters and metadata as needed.

        Args:
            options: Dictionary containing browse options and filters for Azure AD metadata retrieval.

        Returns:
            Dictionary containing Azure AD metadata extracted from the browse results.

        Example:
            >>> options = {
            ...     'filters': [('76', 'some_id', '9')],
            ...     # Additional browse options as needed
            ... }
            >>> azuread_backupset = AzureAdBackupset(...)
            >>> meta_data = azuread_backupset._azuread_browse_meta(options)
            >>> print(meta_data)
            {'root': {...}, 'User1': {...}, 'Group1': {...}}

        #ai-gen-doc
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

    def _azuread_browse_folder(self, options: Dict[str, Any]) -> Tuple[int, List[Any]]:
        """Browse the contents of a specified Azure AD folder.

        This method prepares browse filters based on the provided options and retrieves 
        the folder content from Azure AD. The results are processed and returned as a count 
        and a list of objects.

        Args:
            options: Dictionary containing browse options, including 'folder', 'meta', 'path', 
                and optional 'search' criteria.

        Returns:
            A tuple containing:
                - count: The number of objects found in the folder (int).
                - results: A list of objects representing the folder contents.

        Example:
            >>> options = {
            ...     'folder': 'user',
            ...     'meta': {'Users': {'id': '12345'}},
            ...     'path': '/Users',
            ...     'search': {'obj_id': 'abcde', 'source': 'AzureAD'}
            ... }
            >>> count, results = azure_ad_backupset._azuread_browse_folder(options)
            >>> print(f"Found {count} users")
            >>> for user in results:
            ...     print(user)

        #ai-gen-doc
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
            "admin_unit" : { "displayname" : "Admin units","browsetype": 16, "browsestring" : "ADMINISTRATIVE_UNIT"},
            "device_compliance_policy" : { "displayname" : "Device compliance policies","browsetype": 17, "browsestring" : "DEVICE_COMPLIANCE_POLICY"}}
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

    def browse(self, *args: Any, **kwargs: Any) -> Tuple[int, List[Any]]:
        """Browse the content of the Azure AD Backupset.

        This method allows you to retrieve objects and their count from the backupset by specifying browse options.
        Options can be provided either as a dictionary in the first positional argument or as keyword arguments.

        Args:
            *args: Optional positional arguments. The first argument can be a dictionary of browse options.
            **kwargs: Optional keyword arguments representing browse options.

        Returns:
            A tuple containing:
                - count (int): The number of objects found in the browse operation.
                - browse_result (list): A list of objects retrieved from the backupset.

        Example:
            >>> backupset = AzureAdBackupset(...)
            >>> # Browse using a dictionary of options
            >>> count, objects = backupset.browse({'folder': 'Users', 'recursive': True})
            >>> print(f"Found {count} objects in 'Users' folder")
            >>> 
            >>> # Browse using keyword arguments
            >>> count, objects = backupset.browse(folder='Groups', recursive=False)
            >>> print(f"Found {count} objects in 'Groups' folder")

        #ai-gen-doc
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

    def _process_browse_response(self, flag: bool, response: Any, options: dict) -> tuple:
        """Process the browse response and retrieve item metadata.

        This method parses the server's browse response to extract the total number of items found 
        and a list of metadata dictionaries for each item. It raises an SDKException if the response 
        is invalid or if browsing fails.

        Args:
            flag: Boolean indicating whether the response was successful.
            response: The server response object, expected to have a .json() method returning a dictionary.
            options: Dictionary containing browse options.

        Returns:
            A tuple containing:
                - The total number of items found (int).
                - A list of metadata dictionaries for each item (List[dict]).

        Raises:
            SDKException: If browsing fails, the response is empty, or the response indicates failure.

        Example:
            >>> flag = True
            >>> response = server.get_browse_response()
            >>> options = {'path': '/users'}
            >>> total_items, metadatas = backupset._process_browse_response(flag, response, options)
            >>> print(f"Total items found: {total_items}")
            >>> print(f"Metadata list: {metadatas}")

        #ai-gen-doc
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

    def _process_result_format(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert browse results to the original data format for Azure AD.

        This method updates each result dictionary by replacing all occurrences of "x" with "-" 
        in the 'id' field found under 'commonData', and stores the result in a new 'azureid' key.

        Args:
            results: List of dictionaries representing search results. Each dictionary should contain
                a 'commonData' key with an 'id' field.

        Returns:
            List of dictionaries with the added 'azureid' field reflecting the formatted ID.

        Example:
            >>> results = [
            ...     {'commonData': {'id': 'abcx123xdef'}, 'other': 'value'},
            ...     {'commonData': {'id': 'xyzx456xuvw'}, 'other': 'value2'}
            ... ]
            >>> backupset = AzureAdBackupset()
            >>> formatted_results = backupset._process_result_format(results)
            >>> print(formatted_results)
            [{'commonData': {'id': 'abcx123xdef'}, 'other': 'value', 'azureid': 'abc-123-def'},
             {'commonData': {'id': 'xyzx456xuvw'}, 'other': 'value2', 'azureid': 'xyz-456-uvw'}]

        #ai-gen-doc
        """
        for _ in results:
            _['azureid'] =  _['commonData']['id'].replace("x","-")
        return results
    def azuread_get_metadata(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve Azure AD metadata from the provided browse result.

        This method extracts Azure AD metadata from the given browse result dictionary.
        If the required metadata is not found, an SDKException with error code 110 is raised.

        Args:
            result: Dictionary containing the browse result data, typically including 'advancedData'.

        Returns:
            Dictionary containing Azure AD browse metadata.

        Raises:
            SDKException: If Azure AD metadata is not found in the result (error code 110).

        Example:
            >>> browse_result = {
            ...     "advancedData": {
            ...         "browseMetaData": {
            ...             "azureADDataV2": {}
            ...         },
            ...         "objectGuid": "1234-5678-90ab-cdef"
            ...     }
            ... }
            >>> backupset = AzureAdBackupset(...)
            >>> metadata = backupset.azuread_get_metadata(browse_result)
            >>> print(metadata)
            # The returned metadata dictionary contains Azure AD browse information.

        #ai-gen-doc
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

    def azuread_browse_obj_meta(self, obj_: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Extract Azure AD object metadata information.

        Args:
            obj_: Dictionary representing the Azure AD object. Must contain keys 'commonData', 'guid', and 'objType'.

        Returns:
            A tuple containing:
                - name: The display name of the Azure AD object as a string.
                - metainfo: Dictionary with metadata including 'id', 'azureid', 'name', 'guid', and 'type'.

        Example:
            >>> azuread_obj = {
            ...     'commonData': {'displayName': 'John Doe', 'id': 'x123'},
            ...     'guid': 'abcd-efgh-ijkl',
            ...     'objType': 'User'
            ... }
            >>> backupset = AzureAdBackupset()
            >>> name, meta = backupset.azuread_browse_obj_meta(azuread_obj)
            >>> print(f"Display Name: {name}")
            >>> print(f"Metadata: {meta}")

        #ai-gen-doc
        """
        name = obj_['commonData']['displayName']
        metainfo = {}
        metainfo['id'] = obj_['commonData']['id']
        metainfo['azureid'] = metainfo['id'].replace("x", "-")
        metainfo['name'] = name
        metainfo['guid'] = obj_['guid']
        metainfo['type'] = obj_['objType']
        return name, metainfo

    def azuread_browse_double_query(self, options: Dict[str, Any], request_json: Dict[str, Any]) -> Dict[str, Any]:
        """Create a request JSON for Azure AD double query browsing.

        This method constructs and modifies the request JSON to include double query parameters
        for Azure AD browsing, based on the provided options. It sets up query structures,
        applies filters, and removes unnecessary paths from the request.

        Args:
            options: Dictionary containing browse options such as 'page_size', 'skip_node', and 'filters'.
            request_json: Dictionary representing the base request JSON to be modified.

        Returns:
            The updated request JSON dictionary with double query parameters and applied filters.

        Example:
            >>> options = {
            ...     'page_size': 100,
            ...     'skip_node': 0,
            ...     'filters': [
            ...         ['123', 'value1'],
            ...         ['124', 'value2', 2]
            ...     ]
            ... }
            >>> request_json = {
            ...     'paths': ['/azuread/users'],
            ...     # other base request fields
            ... }
            >>> backupset = AzureAdBackupset()
            >>> updated_json = backupset.azuread_browse_double_query(options, request_json)
            >>> print(updated_json)
            # The returned dictionary can be used for Azure AD browse operations.

        #ai-gen-doc
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

    def azuread_browse_options_builder(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Build and format browse options for Azure AD backupset operations.

        This method ensures that the provided options dictionary contains all required
        keys for a browse operation. If certain keys are missing, default values are added.

        Args:
            options: Dictionary containing browse options. Missing keys such as 'filters',
                'operation', 'page_size', and 'skip_node' will be populated with defaults.

        Returns:
            Dictionary with all necessary browse options formatted for Azure AD operations.

        Example:
            >>> backupset = AzureAdBackupset()
            >>> browse_options = {'operation': 'browse'}
            >>> formatted_options = backupset.azuread_browse_options_builder(browse_options)
            >>> print(formatted_options)
            {'operation': 'browse', 'page_size': 20, 'skip_node': 0, 'filters': [('76', '00000000000000000000000000000001', '9'), ('76', '00000000000000000000000000000001', '9')]}
        #ai-gen-doc
        """
        if "filters" not in options:
            options['filters'] = [("76", "00000000000000000000000000000001", "9"),
                                  ("76", "00000000000000000000000000000001", "9")]
        if "operation" not in options:
            options['operation'] = "browse"
            options['page_size'] = 20
            options['skip_node'] = 0
        return options

    def __prepare_search_json(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the search JSON payload for the view_properties API call.

        This method constructs a search request JSON using the provided options, 
        which include search attributes, time filters, and subclient information. 
        The resulting JSON can be used to perform advanced search operations 
        against Azure AD backup data.

        Args:
            options: Dictionary containing search parameters. 
                Example:
                    {
                        "to_time": <epoch_time>,
                        "subclient_id": <string, optional>,
                        "attribute": <attribute to perform search>
                    }

        Returns:
            Dictionary representing the search request JSON for the API call.

        Example:
            >>> options = {
            ...     "to_time": 1712345678,
            ...     "attribute": "AD_DISPLAYNAME"
            ... }
            >>> backupset = AzureAdBackupset(...)
            >>> search_json = backupset.__prepare_search_json(options)
            >>> print(search_json)
            # The returned dictionary can be used in an API request to perform the search.

        #ai-gen-doc
        """
        options["subclient_id"] = self.subclients.all_subclients['default']['id']

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

    def get_search_response(self, job_time: str, attribute: str) -> Dict[str, Any]:
        """Search for jobs based on the specified job end time and attribute.

        This method performs a search operation for jobs using the provided job end time and attribute.
        It returns the search results as a dictionary containing job details.

        Args:
            job_time: The job end time as a string (e.g., "2024-06-01T12:00:00Z").
            attribute: The attribute to search for (e.g., display name, application ID).

        Returns:
            Dictionary containing the search results for jobs matching the criteria.

        Raises:
            SDKException: If the request is invalid or no jobs are found with the specified attribute.

        Example:
            >>> backupset = AzureAdBackupset(...)
            >>> results = backupset.get_search_response("2024-06-01T12:00:00Z", "displayName")
            >>> print(f"Total jobs found: {results['proccessingInfo']['totalHits']}")
            >>> # Access job details from the results dictionary

        #ai-gen-doc
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

    def view_attributes_url_builder(self, job_time: str, display_name: str) -> str:
        """Build a URL for viewing attributes of an object based on job time and display name.

        This method constructs a URL that allows users to view the attributes of an object
        identified by the specified job time and display name. The URL is generated using
        internal service endpoints and encoded parameters.

        Args:
            job_time: The job time as a string, representing when the job was executed.
            display_name: The display name of the object whose attributes are to be viewed.

        Returns:
            A string containing the URL for viewing the object's attributes.

        Example:
            >>> backupset = AzureAdBackupset(...)
            >>> url = backupset.view_attributes_url_builder('2024-06-01 12:00:00', 'UserAccount01')
            >>> print(f"View attributes URL: {url}")
            >>> # The returned URL can be used to access the object's attribute view in the web console

        #ai-gen-doc
        """

        subclient_id = self.subclients.all_subclients['default']['id']

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

    def get_view_attribute_response(self, job_time: int, display_name: str) -> Dict[str, Any]:
        """Retrieve view attributes for an object using job time and display name.

        This method fetches the view attributes of an object identified by the specified job time and display name.
        The response contains the attributes in JSON format.

        Args:
            job_time: The job time as an integer, representing when the job was executed.
            display_name: The display name of the object whose view attributes are to be retrieved.

        Returns:
            Dictionary containing the view attributes as returned by the API.

        Raises:
            SDKException: If there is an error while retrieving the view attributes.

        Example:
            >>> backupset = AzureAdBackupset(...)
            >>> attributes = backupset.get_view_attribute_response(1681234567, "AzureADUser01")
            >>> print(attributes)
            >>> # The returned dictionary contains the view attributes for the specified object

        #ai-gen-doc
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
