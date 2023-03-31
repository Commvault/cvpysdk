# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Comm-vault Systems, Inc.
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

"""Main file for common operations for the Office 365 Apps Subclient

O365AppsSubclient:
    Derived class from CloudAppsSubclient Base class, for common sub-client functionalities
    pertaining to the Office 365 Apps

O365AppsSubclient Attributes:
==============================

    _prepare_web_search_browse_json()       --          Prepare the JSON for the web search based browse
    _process_web_search_response()          --          Process the response received from the do web search browse
    do_web_search()                         --          Perform a search of the backed up contents
    process_index_retention()               --          Run the retention thread for Office 365 Apps on the INdex Server
"""

import time

from .casubclient import CloudAppsSubclient
from cvpysdk.exception import SDKException


class O365AppsSubclient(CloudAppsSubclient):
    """
        Parent class representing the Office 365 Apps based sub-clients.
        Supported agents:
            Dynamics 365 CRM, SharePoint online, OneDrive for Business and MS Teams
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Sub client object for the given O365Apps Subclient.

            Args:
                backupset_object    (object)    --  instance of the backup-set class

                subclient_name      (str)       --  subclient name

                subclient_id        (int)       --  subclient id

        """
        super(O365AppsSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._client_object = self._instance_object._agent_object._client_object
        self._associated_tables: dict = dict()
        self._associated_environments: dict = dict()
        self._discovered_environments: dict = dict()
        self._discovered_tables: dict = dict()
        self._instance_type: int = 35
        self._app_id: int = 134
        # App ID for cloud apps
        self._O365Apps_SET_USER_POLICY_ASSOCIATION = self._commcell_object._services['SET_USER_POLICY_ASSOCIATION']
        self._O365APPS_BROWSE = self._commcell_object._services['DO_WEB_SEARCH']

    def _process_web_search_response(self, flag, response) -> dict:
        """
            Method to process the response from the web search operation

            Arguments:
                flag        (bool)  --  boolean, whether the response was success or not

                response    (dict)  --  JSON response received for the request from the Server
            Returns:
                dict - Dictionary of all the paths with additional metadata retrieved from browse
        """
        if flag:
            response_json = response.json()

            _search_result = response_json.get("searchResult")
            return _search_result.get("resultItem")

        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _prepare_web_search_browse_json(self, browse_options: dict) -> dict:
        """
            Prepare the request JSON for the webSearch browse

            Arguments:
                browse_options      dict:   Dictionary of browse options

        """
        request_json = {
            "mode": 4,

            "advSearchGrp": {
                "commonFilter": [
                    {
                        "filter": {
                            "interFilterOP": 2,
                            "filters": browse_options.get("common_filters", list())
                        }
                    }
                ],
                "fileFilter": [
                    {
                        "filter": {
                            "interFilterOP": 2,
                            "filters": browse_options.get("file_filter", list())
                        }
                    }
                ],
                "galaxyFilter": [
                    {
                        "appIdList": [
                            int(self.subclient_id)
                        ]
                    }
                ]
            },
            "searchProcessingInfo": {
                "resultOffset": browse_options.get("offset", 0),
                "pageSize": browse_options.get("page_size", 10000),
                "queryParams": browse_options.get("query_params", list()),
                "sortParams": browse_options.get("sort_param", list())
            }
        }

        if browse_options.get('to_time', 0) != 0:
            _point_in_time_browse_args = {
                "field": "BACKUPTIME",
                "fieldValues": {
                    "values": [
                        "0",
                        str(browse_options.get("to_time"))
                    ]
                }
            }
            request_json['advSearchGrp']['fileFilter'][0]['filter']['filters'].append(_point_in_time_browse_args)

        return request_json

    def do_web_search(self, **kwargs) -> dict:
        """
            Method to perform a web search using the /Search endpoint.
            Default browse endpoint for new O365 agents.

            Arguments:
                kwargs:     Dictionary of arguments to be used for the browse
        """
        _browse_options = kwargs
        _retry = kwargs.get("retry", 10)

        _browse_req = self._prepare_web_search_browse_json(browse_options=_browse_options)
        flag, response = self._cvpysdk_object.make_request('POST', self._O365APPS_BROWSE, _browse_req)

        attempt = 1
        while attempt <= _retry:
            if response.json() == {}:
                time.sleep(120)
                flag, response = self._cvpysdk_object.make_request('POST', self._WEB_SEARCH, _browse_req)
            else:
                break
            attempt += 1
        return self._process_web_search_response(flag, response)

    def process_index_retention(self, index_server_client_id):
        """
            Run the retention thread for Dynamics 365/ Office 365 Apps sub-client

         Args:
                index_server_client_id (int)  --  client id of index server

        Raises:

                SDKException:

                    if response is empty

                    if response is not success
        """

        request_json = {
            "appType": int(self._instance_object.idx_app_type),  # 200127
            "indexServerClientId": index_server_client_id
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['OFFICE365_PROCESS_INDEX_RETENTION_RULES'], request_json
        )
        if flag:
            if response.json():
                if "resp" in response.json():
                    error_code = response.json()['resp']['errorCode']
                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to process index retention request\nError: "{0}"'.format(error_string)
                        raise SDKException('Subclient', '102', o_str)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to process index retention request\nError: "{0}"'.format(error_string)
                    raise SDKException('Subclient', '102', o_str)
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))