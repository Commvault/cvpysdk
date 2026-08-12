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

"""Main file for performing operations related to Datacube APIs.

The class `Datacube` is defined here in this file,
that will directly interact with all the Datacube APIs.


Datacube:

    __init__(commcell_object)   --  initialise object of the Datacube class

    __repr__()                  --  returns the string representation of an instance of this class

    _response_not_success()     --  parses through the exception response, and raises SDKException

    _get_analytics_engines()    --  returns the list of all Content Indexing (CI) Servers

    datasources()               --  returns an instance of the Datasources class

    get_jdbc_drivers()          --  gets the list all jdbc_drivers associated with the datacube.

    refresh()                   --  refresh the datasources associated with the Datacube Engine

    refresh_engine()            --  refresh the index server associated with datacube

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from typing import Any

from .datasource import Datasources

from ..exception import SDKException

USER_LOGGED_OUT_MESSAGE = 'User Logged Out. Please initialize the Commcell object again.'
"""str:     Message to be returned to the user, when trying the get the value of an attribute
of the Commcell class, after the user was logged out.

"""


class Datacube(object):
    """
    Represents a datacube instance running on the Commcell platform.

    This class provides an interface for interacting with datacube resources,
    including analytics engines and data sources. It allows users to retrieve
    information about available analytics engines, access data sources, manage
    JDBC drivers for analytics engines, and refresh datacube metadata and engine
    information.

    Key Features:
        - Initialization with a Commcell object for context
        - Access to analytics engines and data sources via properties
        - Retrieval of JDBC drivers for specific analytics engines
        - Refreshing datacube metadata and engine information
        - Internal handling of unsuccessful responses

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a Datacube instance with the specified Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> datacube = Datacube(commcell)
            >>> print("Datacube instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._ANALYTICS_ENGINES = self._services['GET_ALL_INDEX_SERVERS']
        self._ALL_DATASOURCES = self._services['GET_ALL_DATASOURCES']
        self._GET_JDBC_DRIVERS = None

        self._analytics_engines = self._get_analytics_engines()
        self._datasources = None

    def __repr__(self) -> str:
        """Return a string representation of the Datacube instance.

        This method provides a human-readable string that describes the current Datacube object,
        which is useful for debugging and logging purposes.

        Returns:
            A string containing details about the Datacube instance.

        Example:
            >>> datacube = Datacube()
            >>> print(repr(datacube))
            <Datacube object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        o_str = "Datacube class instance for CommServ '{0}'".format(
            self._commcell_object.commserv_name
        )

        return o_str

    def _response_not_success(self, response: object) -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object,
        typically obtained from the `requests` Python package, and raises an
        exception if the response indicates a failure (i.e., status code is not 200).

        Args:
            response: The response object returned from an API request.

        Example:
            >>> response = requests.get('https://api.example.com/data')
            >>> datacube = Datacube()
            >>> datacube._response_not_success(response)
            # Raises an exception if response.status_code is not 200

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_analytics_engines(self) -> list:
        """Retrieve the list of all analytics engines associated with the datacube.

        Returns:
            list: A list containing details of all analytics engines linked to this datacube.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> engines = datacube._get_analytics_engines()
            >>> print(f"Number of analytics engines: {len(engines)}")
            >>> # Each item in the list contains details about an analytics engine

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._ANALYTICS_ENGINES)

        if flag:
            if 'listOfCIServer' in response.json():
                return response.json()['listOfCIServer']
            return []
        self._response_not_success(response)

    @property
    def analytics_engines(self) -> list:
        """Get the value of the analytics engines attributes for this Datacube instance.

        Returns:
            The analytics engines attributes associated with the Datacube. The exact type depends on the implementation.

        Example:
            >>> datacube = Datacube()
            >>> engines = datacube.analytics_engines  # Access the analytics engines property
            >>> print(f"Analytics engines: {engines}")

        #ai-gen-doc
        """
        return self._analytics_engines

    @property
    def datasources(self) -> 'Datasources':
        """Get the Datasources instance associated with this Datacube object.

        Returns:
            Datasources: An instance for managing data sources within the Datacube.

        Example:
            >>> datacube = Datacube(commcell_object)
            >>> ds = datacube.datasources  # Access the datasources property
            >>> print(f"Datasources object: {ds}")
            >>> # The returned Datasources object can be used to manage data sources

        #ai-gen-doc
        """
        try:
            if self._datasources is None:
                self._datasources = Datasources(self)

            return self._datasources
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def get_jdbc_drivers(self, analytics_engine: str) -> list:
        """Retrieve the list of all JDBC drivers associated with the specified analytics engine in the datacube.

        Args:
            analytics_engine: The client name of the analytics engine for which to fetch JDBC drivers.

        Returns:
            A list containing the names or details of all JDBC drivers available in the datacube for the given analytics engine.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        Example:
            >>> datacube = Datacube()
            >>> drivers = datacube.get_jdbc_drivers('analytics_engine_01')
            >>> print(f"Available JDBC drivers: {drivers}")

        #ai-gen-doc
        """
        if not isinstance(analytics_engine, str):
            raise SDKException('Datacube', '101')

        engine_index = (
            self.analytics_engines.index(engine)
            for engine in self.analytics_engines
            if engine["clientName"] == analytics_engine
        ).next()

        self._GET_JDBC_DRIVERS = self._services['GET_JDBC_DRIVERS'] % (
            self.analytics_engines[engine_index]["cloudID"]
        )

        flag, response = self._cvpysdk_object.make_request('GET', self._GET_JDBC_DRIVERS)

        if flag:
            if response.json() and 'drivers' in response.json():
                return response.json()['drivers']
            else:
                raise SDKException('Datacube', '103')
        else:
            self._response_not_success(response)

    def refresh(self) -> None:
        """Reload the datasources associated with the Datacube Engine.

        This method refreshes the internal state of the Datacube object, ensuring that
        any changes to the underlying datasources are reflected in the Datacube Engine.

        Example:
            >>> datacube = Datacube()
            >>> datacube.refresh()
            >>> print("Datasources refreshed successfully")

        #ai-gen-doc
        """
        self._datasources = None

    def refresh_engine(self) -> None:
        """Refresh the Index server associated with the Datacube.

        This method reloads or updates the Index server connection or configuration
        for the current Datacube instance, ensuring that the latest state is reflected.

        Example:
            >>> datacube = Datacube()
            >>> datacube.refresh_engine()
            >>> print("Index server refreshed successfully")

        #ai-gen-doc
        """
        self._analytics_engines = self._get_analytics_engines()
