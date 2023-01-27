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

"""Main file for performing operations on content analyzers, and a single content analyzer client in the commcell.

`ContentAnalyzers`, and `ContentAnalyzer` are 2 classes defined in this file.

ContentAnalyzers:    Class for representing all the Content analyzers in the commcell.

ContentAnalyzer:     Class for representing a single content analyzer client in the commcell.


ContentAnalyzers:

    __init__(commcell_object)           --  initialise object of the ContentAnalyzers class

     _response_not_success()            --  parses through the exception response, and raises SDKException

    refresh()                           --  refresh the content analyzers associated with the commcell

    get()                               --  Returns an instance of ContentAnalyzer class for the given CA client name

    get_properties()                    --  Returns the properties for the given content analyzer client name

    _get_all_contentanalyzers()         --  Returns dict consisting all content analyzers associated with commcell

    _get_cloud_from_collections()       --  gets all the content analyzer details from collection response

    has_client()                        --  Checks whether given CA client exists in commcell or not


ContentAnalyzer:

    __init__()                          --  initialize an object of ContentAnalyzer Class with the given CACloud
                                                name and client id associated to the commcell

    refresh()                           --  refresh the properties of the CA client

    _get_cloud_properties()             --  Gets all the details of associated content analyzer client


ContentAnalyzer Attributes
-----------------

    **client_id**    --  returns the client id of the content analyzer client

    **cloud_url**    --  returns the url of the content analyzer

"""
from .exception import SDKException


class ContentAnalyzers(object):
    """Class for representing all the ContentAnalyzers in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the ContentAnalyzers class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the ContentAnalyzers class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._content_analyzers = None
        self._api_get_content_analyzer_cloud = self._services['GET_CONTENT_ANALYZER_CLOUD']
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_properties(self, caclient_name):
        """Returns a properties of the specified content analyzer client name.

            Args:
                caclient_name (str)  --  name of the content analyzer client

            Returns:
                dict -  properties for the given content analyzer client name


        """
        return self._content_analyzers[caclient_name.lower()]

    def _get_all_content_analyzers(self):
        """Gets the list of all content analyzers associated with this commcell.

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single content analyzer

                    {
                        "contentAnalyzerList": [
                                {
                                    "caUrl": "",
                                     "clientName": "",
                                     "clientId": 0
                                },
                                {
                                      "caUrl": "",
                                      "clientName": "",
                                      "clientId": 0
                                }
                        ]
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._api_get_content_analyzer_cloud
        )
        if flag:
            if response.json() and 'contentAnalyzerList' in response.json():
                return self._get_cloud_from_collections(response.json())
            raise SDKException('ContentAnalyzer', '103')
        self._response_not_success(response)

    @staticmethod
    def _get_cloud_from_collections(collections):
        """Extracts all the content analyzers, and their details from the list of collections given,
            and returns the dictionary of all content analyzers.

            Args:
                collections     (list)  --  list of all collections

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single content analyzer

        """
        _cacloud = {}
        for cacloud in collections['contentAnalyzerList']:
            cacloud_dict = {}
            cacloud_dict['caUrl'] = cacloud.get('caUrl', "")
            cacloud_dict['clientName'] = cacloud.get('clientName', "")
            cacloud_dict['clientId'] = cacloud.get('clientId', 0)
            _cacloud[cacloud['clientName'].lower()] = cacloud_dict
        return _cacloud

    def refresh(self):
        """Refresh the content analyzers associated with the commcell."""
        self._content_analyzers = self._get_all_content_analyzers()

    def get(self, client_name):
        """Returns a ContentAnalyzer object for the given CA client name.

            Args:
                client_name (str)    --  name of the Content analyzer client

            Returns:

                obj                 -- Object of ContentAnalyzer class

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

                    if cacloud_name is not of type string


        """
        if not isinstance(client_name, str):
            raise SDKException('ContentAnalyzer', '101')

        if self.has_client(client_name):
            return ContentAnalyzer(self._commcell_object, client_name)
        raise SDKException('ContentAnalyzer', '102', "Unable to get ContentAnalyzer class object")

    def has_client(self, client_name):
        """Checks if a content analyzer client exists in the commcell with the input name.

            Args:
                client_name (str)    --  name of the content analyzer client

            Returns:
                bool - boolean output whether the CA client exists in the commcell or not

            Raises:
                SDKException:
                    if type of the CA client name argument is not string

        """
        if not isinstance(client_name, str):
            raise SDKException('ContentAnalyzer', '101')

        return self._content_analyzers and client_name.lower() in map(str.lower, self._content_analyzers)


class ContentAnalyzer(object):
    """Class for performing operations on a single content analyzer client"""

    def __init__(self, commcell_object, client_name):
        """Initialize an object of the ContentAnalyzer class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                client_name     (str)           --  name of the content analyzer client

            Returns:
                object  -   instance of the ContentAnalyzer class
        """
        self._commcell_object = commcell_object
        self._client_name = client_name
        self._cloud_url = None
        self._client_id = self._commcell_object.clients.get(client_name).client_id
        self.refresh()

    def _get_cloud_properties(self):
        """ Get properties for all content analyzers client in the commcell
                Args:

                    None

                Returns:

                    None

        """
        content_analyzers_dict = self._commcell_object.content_analyzers.get_properties(self._client_name)
        self._cloud_url = content_analyzers_dict['caUrl']
        return content_analyzers_dict

    @property
    def client_id(self):
        """Returns the value of the Content analyzer client id attribute."""
        return int(self._client_id)

    @property
    def cloud_url(self):
        """Returns the value of the Content analyzer client url attribute."""
        return self._cloud_url

    def refresh(self):
        """Refresh the content analyzer details associated with this commcell"""
        self._get_cloud_properties()
