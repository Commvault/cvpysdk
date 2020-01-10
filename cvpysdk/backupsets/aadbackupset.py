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
"""

from __future__ import unicode_literals

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
        if "adv_attributes" in options:
            request_json = self.azuread_browse_double_query_adv(options, request_json)
        else:
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
        _, result = self._azuread_browse_basic(options)
        if len(result) == 1 and result[0]['objType'] == 1:
            newid = result[0]['commonData']['id']
            options['filters'] = [(_[0], newid, _[2]) for _ in options['filters']]
            name, metainfo = self.azuread_browse_obj_meta(result[0])
            azure_meta['root'] = metainfo
            options['meta'] = azure_meta
            result = self.browse(**options)
        else:
            for _ in result:
                name, metainfo = self.azuread_browse_obj_meta(_)
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
            "user" : "users",
            "group" : "groups",
            "reg_app" : "applications",
            "ent_app" : "servicePrincipals"}

        azure_meta = options['meta']
        newid = azure_meta[azure_meta_mapper[options['folder']]]['id']

        options['filters'] = [(_[0], newid, _[2]) for _ in options['filters']]
        if "search" in options:
            options['filters'] = [[_, ("30", options['search'], None)] for _ in options['filters']]
        del(options['folder'])
        count, results = self._azuread_browse_basic(options)
        result = []
        for _ in results:
            _, metainfo = self.azuread_browse_obj_meta(_)
            result.append(metainfo)
        if 'adv_attributes' in options:
            count, result = self._adv_attributes(options, count, results)
        return count, result

    def _adv_attributes(self, options, count, results):
        """ get advanced attribute in objects
            Args:
                options    (dict)    browse option from impoort
                count     (int)    return count from browse
                result    (list)    objects list from browse
            Return:
                count     (int)    return count from browse
                result    (list)    objects list from browse
            Raise:
                None
        """
        for _ in results:
            _, obj_ = self.azuread_browse_obj_meta(_)
            rev_azuread_index_meta_mapper = {2 : "USER",
                                             5 : "APPLICATION",
                                             3 : "GROUP",
                                             6 : "SERVICE_PRINCIPAL"}
            options['filters'] = [[("130", obj_['id'], "9"),
                                   ("125", rev_azuread_index_meta_mapper[obj_['type']],
                                    None)],
                                  [("130", obj_['id'], "9"),
                                   ("125", rev_azuread_index_meta_mapper[obj_['type']],
                                    None)]]
            count, results = self._azuread_browse_basic(options)
            result = []
            for _ in results:
                _, metainfo = self.azuread_browse_obj_meta(_)
                result.append(metainfo)
        return count, result

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

        if "folder" in options:
            count, browse_result = self._azuread_browse_folder(options)
        else:
            browse_result = azure_meta
            count = 0
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
                    if not result_set:
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
#        rev_azuread_index_meta_mapper = dict((v,k) for k,v in AZUREAD_INDEX_META_MAPPER.items())
        azuread_index_meta_mapper = {5 : "application",
                                     3 : "group",
                                     6 : "servicePrincipal",
                                     2 : "user"}
        if metainfo['type'] in azuread_index_meta_mapper:
            metainfo["adv_attribute"] = obj_["{}Data".\
                                             format(azuread_index_meta_mapper[metainfo['type']])]
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
        if options['filters']:
            request_json['queries'] = []
            for ind_, filter_ in enumerate(options['filters']):
                if ind_ > 0:
                    queries = {
                        "type": ind_,
                        "queryId": str(ind_),
                        }
                    request_json['queries'].append(queries)
                    request_json['queries'][ind_]['agprParam'] = {'aggrType': 4,
                                                                  'field' : 0}
                else:
                    queries = {
                        "type": ind_,
                        "queryId": str(ind_),
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
                        }
                    request_json['queries'].append(queries)
                request_json['queries'][ind_]['whereClause'] = []
                if len(filter_) == 2:
                    for _ in filter_:
                        filter_dict = {
                            'connector': 0,
                            'criteria': {
                                'field': _[0],
                                'values': [_[1]]}}
                        request_json['queries'][ind_]['whereClause'].append(filter_dict)
                else:
                    filter_dict = {
                        'connector': 0,
                        'criteria': {
                            'field': filter_[0],
                            'values': [filter_[1]],
                            "dataOperator" : int(filter_[2])}}
                    request_json['queries'][ind_]['whereClause'].append(filter_dict)
        return request_json


    def azuread_browse_double_query_adv(self, options, request_json):
        """ get advanced attribute for obeject
            Args:
                options    (dict)    browse option from impoort
                request_json    (json)    request json file from basic request class
            Return:
                request_json    (json)    request json with addittional options
            Raise:
                None
        """
        if options['filters']:
            request_json['queries'] = []
            for ind_, filter_ in enumerate(options['filters']):
                if ind_ > 0:
                    queries = {
                        "type": ind_,
                        "queryId": str(ind_),
                        }
                    request_json['queries'].append(queries)
                    request_json['queries'][ind_]['agprParam'] = {'aggrType': 4,
                                                                  'field' : 0}
                else:
                    queries = {
                        "type": ind_,
                        "queryId": str(ind_),
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
                        }
                    request_json['queries'].append(queries)
                request_json['queries'][ind_]['whereClause'] = []

                if len(filter_) == 2:
                    for _ in filter_:
                        if _[2] is not None:
                            filter_dict = {
                                'connector': 0,
                                'criteria': {
                                    'field': _[0],
                                    'values': [_[1]],
                                    "dataOperator" : int(_[2])}}
                        else:
                            filter_dict = {
                                'criteria': {
                                    'field': _[0],
                                    'values': [_[1]]}}
                        request_json['queries'][ind_]['whereClause'].append(filter_dict)
        request_json['options']['fetchFileProperties'] = True
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
