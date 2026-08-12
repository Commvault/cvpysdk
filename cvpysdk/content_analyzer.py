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
    """
    Manages and represents all ContentAnalyzers within a CommCell environment.

    This class provides an interface for interacting with ContentAnalyzer clients,
    retrieving their properties, and managing their lifecycle within the CommCell.
    It supports operations such as fetching all available ContentAnalyzers, checking
    for the existence of specific clients, refreshing the analyzer list, and obtaining
    detailed properties for individual analyzers.

    Key Features:
        - Initialization with a CommCell object for context
        - Retrieve properties of a specific ContentAnalyzer client
        - Fetch all ContentAnalyzers present in the CommCell
        - Extract cloud information from collections
        - Refresh the list of ContentAnalyzers to reflect current state
        - Get a ContentAnalyzer client by name
        - Check if a specific ContentAnalyzer client exists
        - Internal response validation for API interactions

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a new instance of the ContentAnalyzers class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> content_analyzers = ContentAnalyzers(commcell)
            >>> print("ContentAnalyzers instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._content_analyzers = None
        self._api_get_content_analyzer_cloud = self._services['GET_CONTENT_ANALYZER_CLOUD']
        self.refresh()

    def _response_not_success(self, response: object) -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object, typically 
        returned from an API request using the `requests` Python package. If the response 
        status code is not 200, an exception is raised to indicate the request was not successful.

        Args:
            response: The response object received from an API request (e.g., a `requests.Response` instance).

        Example:
            >>> response = requests.get('https://api.example.com/data')
            >>> content_analyzers = ContentAnalyzers()
            >>> content_analyzers._response_not_success(response)
            # Raises an exception if the response status code is not 200

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_properties(self, caclient_name: str) -> dict:
        """Retrieve the properties of a specified content analyzer client.

        Args:
            caclient_name: The name of the content analyzer client whose properties are to be fetched.

        Returns:
            A dictionary containing the properties for the given content analyzer client name.

        Example:
            >>> analyzers = ContentAnalyzers()
            >>> properties = analyzers.get_properties("AnalyzerClient01")
            >>> print(properties)
            {'clientName': 'AnalyzerClient01', 'status': 'Active', ...}

        #ai-gen-doc
        """
        return self._content_analyzers[caclient_name.lower()]

    def _get_all_content_analyzers(self) -> dict:
        """Retrieve the list of all content analyzers associated with this Commcell.

        Returns:
            dict: A dictionary containing a list of content analyzer details. Each content analyzer is represented
            as a dictionary with keys such as "caUrl", "clientName", and "clientId".

            Example response structure:
                {
                    "contentAnalyzerList": [
                        {
                            "caUrl": "http://analyzer1.example.com",
                            "clientName": "AnalyzerClient1",
                            "clientId": 123
                        },
                        {
                            "caUrl": "http://analyzer2.example.com",
                            "clientName": "AnalyzerClient2",
                            "clientId": 456
                        }
                    ]
                }

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> analyzers = content_analyzers._get_all_content_analyzers()
            >>> for analyzer in analyzers.get("contentAnalyzerList", []):
            ...     print(f"Analyzer URL: {analyzer['caUrl']}, Client Name: {analyzer['clientName']}")
        #ai-gen-doc
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
    def _get_cloud_from_collections(collections: list) -> dict:
        """Extract all content analyzers and their details from a list of collections.

        This static method processes the provided list of collections and returns a dictionary
        where each key represents a content analyzer, and the corresponding value is a dictionary
        containing the details of that analyzer.

        Args:
            collections: List of collections to extract content analyzer information from.

        Returns:
            Dictionary mapping content analyzer identifiers to their detail dictionaries.

        Example:
            >>> collections = [
            ...     {'analyzer_id': 1, 'details': {'name': 'AnalyzerA', 'type': 'cloud'}},
            ...     {'analyzer_id': 2, 'details': {'name': 'AnalyzerB', 'type': 'cloud'}}
            ... ]
            >>> analyzers = ContentAnalyzers._get_cloud_from_collections(collections)
            >>> print(analyzers)
            {1: {'name': 'AnalyzerA', 'type': 'cloud'}, 2: {'name': 'AnalyzerB', 'type': 'cloud'}}

        #ai-gen-doc
        """
        _cacloud = {}
        for cacloud in collections['contentAnalyzerList']:
            cacloud_dict = {}
            cacloud_dict['caUrl'] = cacloud.get('caUrl', "")
            cacloud_dict['clientName'] = cacloud.get('clientName', "")
            cacloud_dict['clientId'] = cacloud.get('clientId', 0)
            _cacloud[cacloud['clientName'].lower()] = cacloud_dict
        return _cacloud

    def refresh(self) -> None:
        """Reload the content analyzers associated with the Commcell.

        This method refreshes the internal state of the ContentAnalyzers object, ensuring that 
        any changes to the content analyzers on the Commcell are reflected in this instance.

        Example:
            >>> analyzers = ContentAnalyzers(commcell_object)
            >>> analyzers.refresh()  # Updates the list of content analyzers from the Commcell
            >>> print("Content analyzers refreshed successfully")

        #ai-gen-doc
        """
        self._content_analyzers = self._get_all_content_analyzers()

    def get(self, client_name: str) -> 'ContentAnalyzer':
        """Retrieve a ContentAnalyzer object for the specified Content Analyzer (CA) client name.

        Args:
            client_name: The name of the Content Analyzer client for which to retrieve the ContentAnalyzer object.

        Returns:
            ContentAnalyzer: An instance of the ContentAnalyzer class corresponding to the given client name.

        Raises:
            SDKException: If the response is empty, the response is not successful, or if the client_name is not a string.

        Example:
            >>> analyzers = ContentAnalyzers()
            >>> ca = analyzers.get("CA_Client_01")
            >>> print(f"Retrieved ContentAnalyzer for: {ca.client_name}")

        #ai-gen-doc
        """
        if not isinstance(client_name, str):
            raise SDKException('ContentAnalyzer', '101')

        if self.has_client(client_name):
            return ContentAnalyzer(self._commcell_object, client_name)
        raise SDKException('ContentAnalyzer', '102', "Unable to get ContentAnalyzer class object")

    def has_client(self, client_name: str) -> bool:
        """Check if a content analyzer client exists in the Commcell by name.

        Args:
            client_name: The name of the content analyzer client to check.

        Returns:
            True if the content analyzer client exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the client_name argument is not a string.

        Example:
            >>> analyzers = ContentAnalyzers(commcell_object)
            >>> exists = analyzers.has_client("CA_Client01")
            >>> print(f"Client exists: {exists}")
            # Output: Client exists: True

        #ai-gen-doc
        """
        if not isinstance(client_name, str):
            raise SDKException('ContentAnalyzer', '101')

        return self._content_analyzers and client_name.lower() in map(str.lower, self._content_analyzers)


class ContentAnalyzer(object):
    """
    ContentAnalyzer provides an interface for managing and interacting with a single content analyzer client.

    This class allows users to initialize a content analyzer client, retrieve cloud-related properties,
    access client-specific identifiers and URLs, and refresh the client's state. It is designed to work
    with a commcell object and a specified client name, facilitating operations related to cloud content analysis.

    Key Features:
        - Initialization with commcell object and client name
        - Retrieval of cloud properties associated with the client
        - Access to client ID and cloud URL via properties
        - Ability to refresh and update the client's state

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, client_name: str) -> None:
        """Initialize a ContentAnalyzer object for a specific client.

        Args:
            commcell_object: An instance of the Commcell class representing the Commcell connection.
            client_name: The name of the content analyzer client.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> analyzer = ContentAnalyzer(commcell, 'AnalyzerClient01')
            >>> print("ContentAnalyzer object created for client:", analyzer)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._client_name = client_name
        self._cloud_url = None
        self._client_id = self._commcell_object.clients.get(client_name).client_id
        self.refresh()

    def _get_cloud_properties(self) -> None:
        """Retrieve properties for all content analyzer clients in the Commcell.

        This method gathers and updates the configuration properties for each content analyzer client 
        associated with the Commcell. It is typically used internally to ensure that the latest 
        cloud-related properties are available for further operations.

        Example:
            >>> analyzer = ContentAnalyzer()
            >>> analyzer._get_cloud_properties()
            >>> print("Cloud properties for all content analyzers have been refreshed.")

        #ai-gen-doc
        """
        content_analyzers_dict = self._commcell_object.content_analyzers.get_properties(self._client_name)
        self._cloud_url = content_analyzers_dict['caUrl']
        return content_analyzers_dict

    @property
    def client_id(self) -> int:
        """Get the client ID associated with the Content Analyzer.

        Returns:
            The integer value representing the Content Analyzer client ID.

        Example:
            >>> analyzer = ContentAnalyzer()
            >>> cid = analyzer.client_id
            >>> print(f"Content Analyzer client ID: {cid}")

        #ai-gen-doc
        """
        return int(self._client_id)

    @property
    def cloud_url(self) -> str:
        """Get the URL of the Content Analyzer client.

        Returns:
            The Content Analyzer client URL as a string.

        Example:
            >>> analyzer = ContentAnalyzer()
            >>> url = analyzer.cloud_url  # Use dot notation to access the property
            >>> print(f"Content Analyzer URL: {url}")

        #ai-gen-doc
        """
        return self._cloud_url

    def refresh(self) -> None:
        """Reload the content analyzer details associated with this Commcell.

        This method refreshes the internal state of the ContentAnalyzer object, ensuring that 
        any changes made to the content analyzer configuration on the Commcell are reflected 
        in this instance.

        Example:
            >>> analyzer = ContentAnalyzer(commcell_object)
            >>> analyzer.refresh()  # Updates the analyzer details from the Commcell
            >>> print("Content analyzer details refreshed.")
        #ai-gen-doc
        """
        self._get_cloud_properties()