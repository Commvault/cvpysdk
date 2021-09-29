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

"""Main file for performing operations on content analyzers, and a single content analyzer cloud in the commcell.

`ContentAnalyzers`, and `ContentAnalyzer` are 2 classes defined in this file.

ContentAnalyzers:    Class for representing all the Content analyzers in the commcell.

ContentAnalyzer:     Class for representing a single content analyzer cloud in the commcell.


ContentAnalyzers:

    __init__(commcell_object)           --  initialise object of the ContentAnalyzers class

     _response_not_success()            --  parses through the exception response, and raises SDKException

    refresh()                           --  refresh the content analyzers associated with the commcell

    get()                               --  Returns an instance of ContentAnalyzer class for the given CAcloud name

    get_properties()                    --  Returns the properties for the given content analyzer cloud name

    _get_all_contentanalyzers()         --  Returns dict consisting all content analyzers associated with commcell

    _get_cloud_from_collections()       --  gets all the content analyzer details from collection response

    has_cloud()                         --  Checks whether given CA cloud exists in commcell or not

    create()                            --  Creates the content analyzer cloud for the given client name

    delete()                            --  deletes the content analyzer cloud for the given cloud name

ContentAnalyzer:

    __init__(
        commcell_object,
        cloud_name,
        cloud_id=None)                  --  initialize an object of ContentAnalyzer Class with the given CACloud
                                                name and id associated to the commcell

    refresh()                           --  refresh the properties of the CAcloud

    _get_cloud_id()                     --  Gets content analyzer cloud id for the given CA cloud name

    _get_cloud_properties()             --  Gets all the details of associated content analyzer cloud


ContentAnalyzer Attributes
-----------------

    **cloud_id**    --  returns the cloudid of the content analyzer

    **cloud_url**   --  returns the url of the content analyzer

"""
from past.builtins import basestring
from .exception import SDKException
from .datacube.constants import ContentAnalyzerConstants


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

    def get_properties(self, cacloud_name):
        """Returns a properties of the specified content analyzer cloud name.

            Args:
                cacloud_name (str)  --  name of the content analyzer cloud

            Returns:
                dict -  properties for the given content analyzer cloud name


        """
        return self._content_analyzers[cacloud_name]

    def _get_all_content_analyzers(self):
        """Gets the list of all content analyzers associated with this commcell.

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single content analyzer

                    {
                        "contentAnalyzerList": [
                                {
                                    "caUrl": "http://client.company.com:22005",
                                     "cloudName": "V11lotusClientCloud",
                                     "cloudId": 1010
                                },
                                {
                                      "caUrl": "http://client.company.com:22001",
                                      "cloudName": "Imsolrcloud",
                                      "cloudId": 1026
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
            cacloud_dict['cloudName'] = cacloud.get('cloudName', "")
            cacloud_dict['cloudId'] = cacloud.get('cloudId', 0)
            cacloud_dict['clientId'] = cacloud.get('clientId', 0)
            _cacloud[cacloud['cloudName']] = cacloud_dict
        return _cacloud

    def refresh(self):
        """Refresh the content analyzers associated with the commcell."""
        self._content_analyzers = self._get_all_content_analyzers()

    def create(self, client_name, content_analyzer_name, temp_directory):
        """Creates an content analyzer cloud within the commcell

                Args:
                    client_name            (str)    --  Name of the client where content analyzer package is installed
                    content_analyzer_name  (str)    --  name for the content analyzer cloud
                    temp_directory        (str)     --  temp location for the content extractor
                    cloud_param           (list)    --  list of custom parameters to be parsed
                                                    into the json for content analyser meta info
                                                    [
                                                        {
                                                            "name": <name>,
                                                            "value": <value>
                                                        }
                                                    ]
                Returns:
                    None

                Raises:
                    SDKException:
                        Data type of the input(s) is not valid.

                        Response was not success.

                        Response was empty.
        """
        if not isinstance(client_name, basestring) or not isinstance(content_analyzer_name, basestring):
            raise SDKException('ContentAnalyzer', '101')
        client = self._commcell_object.clients.get(client_name)
        req_json = ContentAnalyzerConstants.REQUEST_JSON
        req_json['cloudNodes'] = [
            {
                "opType": ContentAnalyzerConstants.OPERATION_ADD,
                "nodeClientEntity": {
                    "hostName": client.client_hostname,
                    "clientId": int(client.client_id),
                    "clientName": client.client_name,
                    "_type_": 3
                },
                "nodeMetaInfos": [
                    {
                        "name": "PORTNO",
                        "value": "22000"
                    },
                    {
                        "name": "JVMMAXMEMORY",
                        "value": "4096"
                    },
                    {
                        "name": "INDEXLOCATION",
                        "value": temp_directory
                    }
                ]
            }
        ]
        req_json['cloudInfoEntity']['cloudName'] = content_analyzer_name
        req_json['cloudInfoEntity']['cloudDisplayName'] = content_analyzer_name
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['INDEX_SERVER_CREATION'], req_json)
        if flag:
            if response.json():
                error_code = response.json()['genericResp']['errorCode']
                error_string = response.json()['genericResp']['errorMessage']
                if error_code == 0:
                    self.refresh()
                else:
                    o_str = 'Failed to create content analyzer cloud. Error: "{0}"'.format(
                        error_string)
                    raise SDKException('ContentAnalyzer', '102', o_str)
            raise SDKException('Response', '102')
        self._response_not_success(response)

    def delete(self, cloud_name):
        """Deletes / removes an content analyzer from the commcell

                Args:
                    cloud_name      (str)   --  cloud name of content analyzer to be deleted from the commcell

                Raises:
                    SDKException:
                        Data type of the input(s) is not valid.

                        Response was not success.

                        Response was empty.
        """
        if cloud_name is None or not isinstance(cloud_name, basestring):
            raise SDKException('ContentAnalyzer', '101')

        cloud_id = self.get(cloud_name).cloud_id
        req_json = ContentAnalyzerConstants.REQUEST_JSON
        req_json["opType"] = ContentAnalyzerConstants.OPERATION_DELETE
        req_json['cloudInfoEntity']['cloudId'] = cloud_id

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['INDEX_SERVER_DELETION'], req_json
        )
        if flag:
            if response.json() and 'genericResp' in response.json(
            ) and 'errorCode' not in response.json()['genericResp']:
                self.refresh()
                return
            if response.json() and 'genericResp' in response.json():
                raise SDKException(
                    'Response', '102', response.json()['genericResp'].get(
                        'errorMessage', ''))
            raise SDKException('Response', '102')
        self._response_not_success(response)

    def get(self, cloud_name):
        """Returns a ContentAnalyzer object for the given CA cloud name.

            Args:
                cloud_name (str)    --  name of the Content analyzer cloud

            Returns:

                obj                 -- Object of ContentAnalyzer class

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

                    if cacloud_name is not of type string


        """
        if not isinstance(cloud_name, basestring):
            raise SDKException('ContentAnalyzer', '101')

        if self.has_cloud(cloud_name):
            cloud_id = self._content_analyzers[cloud_name]['cloudId']
            return ContentAnalyzer(self._commcell_object, cloud_name, cloud_id)
        raise SDKException('ContentAnalyzer', '102', "Unable to get ContentAnalyzer class object")

    def has_cloud(self, cloud_name):
        """Checks if a content analyzer cloud exists in the commcell with the input name.

            Args:
                cloud_name (str)    --  name of the content analyzer

            Returns:
                bool - boolean output whether the CA cloud exists in the commcell or not

            Raises:
                SDKException:
                    if type of the CA cloud name argument is not string

        """
        if not isinstance(cloud_name, basestring):
            raise SDKException('ContentAnalyzer', '101')

        return self._content_analyzers and cloud_name.lower() in map(str.lower, self._content_analyzers)


class ContentAnalyzer(object):
    """Class for performing operations on a single content analyzer cloud"""

    def __init__(self, commcell_object, cloud_name, cloud_id=None):
        """Initialize an object of the ContentAnalyzer class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                cloud_name     (str)            --  name of the content analyzer cloud

                cloud_id       (str)            --  id of the content analyzer cloud
                    default: None

            Returns:
                object  -   instance of the ContentAnalyzer class
        """
        self._commcell_object = commcell_object
        self._cloud_name = cloud_name
        self._cloud_url = None
        self._cloud_id = None
        self._client_id = None
        if cloud_id is None:
            self._cloud_id = self._get_cloud_id(cloud_name)
        else:
            self._cloud_id = cloud_id
        self.refresh()

    def _get_cloud_id(self, cloud_name):
        """ Get CA cloud id for given CA cloud name
                Args:

                    cloud_name (str)   -- Name of the content analyzer cloud

                Returns:

                    int                -- Content analyzer cloud id

        """

        return self._commcell_object.content_analyzers.get(cloud_name).cloud_id

    def _get_cloud_properties(self):
        """ Get CA cloud properties for all content analyzers cloud in the commcell
                Args:

                    None

                Returns:

                    None

        """
        content_analyzers_dict = self._commcell_object.content_analyzers.get_properties(self._cloud_name)
        self._cloud_url = content_analyzers_dict['caUrl']
        self._cloud_id = content_analyzers_dict['cloudId']
        self._client_id = content_analyzers_dict['clientId']
        return content_analyzers_dict

    @property
    def client_id(self):
        """Returns the value of the Content analyzer client id attribute."""
        return self._client_id

    @property
    def cloud_id(self):
        """Returns the value of the Content analyzer cloud id attribute."""
        return self._cloud_id

    @property
    def cloud_url(self):
        """Returns the value of the Content analyzer cloud url attribute."""
        return self._cloud_url

    def refresh(self):
        """Refresh the content analyzer details associated with this commcell"""
        self._get_cloud_properties()
