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

"""File for operating on an Okta Subclient.

OktaSubclient is the only class defined in this file.

OktaSubclient:  Derived class from CloudAppsSubclient Base class, representing
                an Okta subclient, and to perform operations on that subclient.

OktaSubclient:

    do_web_search()                     --  Perform a web search on backed-up Okta data

    _prepare_web_search_json()          --  Build the DO_WEB_SEARCH request payload

    _process_web_search_response()      --  Process the response from the web search operation

"""

from __future__ import unicode_literals

from ..casubclient import CloudAppsSubclient
from cvpysdk.exception import SDKException


class OktaSubclient(CloudAppsSubclient):
    """Class for representing a subclient of the Okta agent."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Subclient object for the given Okta Subclient.

        Args:
            backupset_object    (object)    --  instance of the backup-set class

            subclient_name      (str)       --  subclient name

            subclient_id        (int)       --  subclient id

        """
        super(OktaSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self._WEB_SEARCH = self._commcell_object._services['DO_WEB_SEARCH']

    def _prepare_web_search_json(self, search_options: dict) -> dict:
        """Build the request JSON for the DO_WEB_SEARCH API.

        Args:
            search_options  (dict)  --  Dictionary of search options:
                parent_guid     (str)   --  PARENT_GUID to filter by (optional)
                page_size       (int)   --  Number of results per page (default 50000)
                offset          (int)   --  Result offset for pagination (default 0)
                query_params    (list)  --  List of query parameter dicts (optional)
                sort_params     (list)  --  List of sort parameter dicts (optional)

        Returns:
            dict    --  The request JSON for the search API
        """
        common_filters = [
            {
                "field": "CISTATE",
                "intraFieldOp": 0,
                "fieldValues": {"values": ["1"]}
            },
            {
                "field": "IS_VISIBLE",
                "intraFieldOp": 0,
                "fieldValues": {"values": ["true"]}
            }
        ]

        file_filter = []
        parent_guid = search_options.get("parent_guid", "")
        if parent_guid:
            file_filter = [
                {
                    "interGroupOP": 2,
                    "filter": {
                        "interFilterOP": 2,
                        "filters": [
                            {
                                "field": "PARENT_GUID",
                                "intraFieldOp": 0,
                                "fieldValues": {"values": [parent_guid]}
                            }
                        ]
                    }
                }
            ]

        request_json = {
            "mode": 4,
            "advSearchGrp": {
                "commonFilter": [
                    {
                        "filter": {
                            "interFilterOP": 2,
                            "filters": common_filters
                        }
                    }
                ],
                "fileFilter": file_filter,
                "emailFilter": [],
                "galaxyFilter": [
                    {"appIdList": [int(self.subclient_id)]}
                ]
            },
            "searchProcessingInfo": {
                "resultOffset": search_options.get("offset", 0),
                "pageSize": search_options.get("page_size", 50000),
                "queryParams": search_options.get("query_params", []),
                "sortParams": search_options.get("sort_params", [])
            }
        }

        return request_json

    def _process_web_search_response(self, flag, response) -> dict:
        """Process the response from the web search operation.

        Args:
            flag        (bool)  --  whether the response was success or not
            response    (object)--  response received from the server

        Returns:
            dict    --  The response JSON dictionary

        Raises:
            SDKException:   If the request was not successful
        """
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))
        return response.json()

    def do_web_search(self, **kwargs) -> dict:
        """Perform a web search on backed-up Okta data using the /Search endpoint.

        Args:
            **kwargs:   Search options passed to _prepare_web_search_json():
                parent_guid     (str)   --  PARENT_GUID to filter by
                page_size       (int)   --  Number of results per page
                offset          (int)   --  Result offset for pagination
                query_params    (list)  --  List of query parameter dicts
                sort_params     (list)  --  List of sort parameter dicts

        Returns:
            dict    --  The response JSON from the search API

        Raises:
            SDKException:   If the request fails
        """
        request_json = self._prepare_web_search_json(kwargs)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._WEB_SEARCH, request_json)
        return self._process_web_search_response(flag, response)