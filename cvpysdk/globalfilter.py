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

"""Main file for managing global filters for this commcell

GlobalFilters and GlobalFilter are the only classes defined in this file

GlobalFilters: Class for managing global filters for this commcell

GlobalFilter: Class to represent one agent specific global filter

GlobalFilters:
    __init__()                      --  initializes global filter class object

    __repr__()                      --  returns the string for the instance of the GlobalFilter
                                            class

    get()                           --  returns the GlobalFilter object for specified filter name


GlobalFilter:
    __init__()                      --  initializes global filter object

    __repr__()                      --  returns string representing this class

    _get_global_filters()           --  gets the global filters associated with commcell
                                            for specified filter

    _initialize_global_filters()    --  initializes GlobalFilter class objects

    _update()                       --  updates the global filters list on commcell

    content()                       --  returns the list of filters associated with this agent

    add()                           --  adds the specified filter to global list

    overwrite()                     --  overwrites existing global list with specified

    delete_all()                    --  removes all the filters from global filters list

    refresh()                       --  refresh the properties of the global filter

"""

from .exception import SDKException


class GlobalFilters(object):
    """
    Class for managing global filters within a CommCell environment.

    This class provides an interface to interact with and manage global filters
    associated with a specific CommCell object. It allows users to retrieve
    filter details by name and offers a convenient representation for debugging
    and logging purposes.

    Key Features:
        - Initialization with a CommCell object for context-specific filter management
        - Retrieval of global filter details by filter name
        - String representation for easy inspection of the filter manager

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a GlobalFilters object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> global_filters = GlobalFilters(commcell)
            >>> print("GlobalFilters object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._global_filter_dict = {
            "WINDOWS": 'windowsGlobalFilters',
            "UNIX": 'unixGlobalFilters',
            "NAS":  'nasGlobalFilters'
        }

    def __repr__(self) -> str:
        """Return the string representation of the GlobalFilters instance.

        This method provides a developer-friendly string that represents the current
        GlobalFilters object, useful for debugging and logging purposes.

        Example:
            >>> filters = GlobalFilters()
            >>> print(repr(filters))
            <GlobalFilters object at 0x7f8c2b1e2d30>

        #ai-gen-doc
        """
        o_str = "GlobalFilter class instance for CommServ '{0}'".format(
            self._commcell_object.commserv_name
        )
        return o_str

    def get(self, filter_name: str) -> 'GlobalFilter':
        """Retrieve the global filter agent object for the specified filter name.

        Args:
            filter_name: The name of the global filter for which the object is to be created.
                Accepted values include: "WINDOWS", "UNIX", or "NAS".

        Returns:
            GlobalFilter: The global filter object corresponding to the specified filter name.

        Raises:
            SDKException: If the input data type is invalid or if the specified global filter does not exist.

        Example:
            >>> global_filters = GlobalFilters()
            >>> windows_filter = global_filters.get("WINDOWS")
            >>> print(f"Retrieved filter: {windows_filter}")

        #ai-gen-doc
        """
        if not isinstance(filter_name, str):
            raise SDKException('GlobalFilter', '101')

        if filter_name.upper() not in self._global_filter_dict:
            raise SDKException(
                'GlobalFilter', '102', 'Invalid Global Filter name {0}'.format(filter_name)
            )

        return GlobalFilter(
            self._commcell_object,
            filter_name.upper(),
            self._global_filter_dict[filter_name.upper()]
        )


class GlobalFilter(object):
    """
    Represents a global filter for a particular agent within a CommCell environment.

    This class provides an interface to manage global filters, including adding, overwriting,
    deleting, and refreshing filter configurations. It interacts with the CommCell object to
    retrieve and update filter information, ensuring that agent-level filtering is consistent
    and up-to-date.

    Key Features:
        - Initialization with CommCell object, filter name, and filter key
        - Retrieval and initialization of global filters
        - Addition of new filters to the global filter set
        - Overwriting existing filters with new configurations
        - Deletion of all filters from the global filter set
        - Refreshing filter data to synchronize with the latest state
        - Access to filter content via a property
        - String representation for debugging and logging purposes

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, filter_name: str, filter_key: str) -> None:
        """Initialize a GlobalFilter object.

        Args:
            commcell_object: The Commcell object representing the connection to the Commcell environment.
            filter_name: The name of the global filter to be managed.
            filter_key: The unique key identifying the global filter.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> global_filter = GlobalFilter(commcell, 'ExcludeTempFiles', 'filter_123')
            >>> print(f"Global filter '{global_filter}' initialized successfully")

        #ai-gen-doc
        """
        self._filter_name = filter_name
        self._filter_key = filter_key
        self._commcell_object = commcell_object
        self._GLOBAL_FILTER = self._commcell_object._services['GLOBAL_FILTER']
        self._content = []

        self.refresh()

    def __repr__(self) -> str:
        """Return a string representation of the GlobalFilter instance.

        This method provides a developer-friendly string that can be used to 
        identify the GlobalFilter object during debugging or logging.

        Returns:
            A string representation of the GlobalFilter instance.

        Example:
            >>> gf = GlobalFilter()
            >>> print(repr(gf))
            <GlobalFilter object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """
        return "Global Filter object for: {0}".format(self._filter_name)

    def _get_global_filters(self) -> dict:
        """Retrieve the global filters associated with this Commcell.

        Returns:
            dict: A dictionary containing the global filters configured for the Commcell.

        Example:
            >>> filters = global_filter._get_global_filters()
            >>> print(filters)
            >>> # Output will be a dictionary of global filter settings

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._GLOBAL_FILTER
        )

        if flag:
            if response.json():
                return response.json()
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_global_filters(self) -> None:
        """Initialize the global filters for the GlobalFilter instance.

        This method sets up the necessary global filters used by the GlobalFilter object.
        It should be called internally to ensure that all required filters are properly configured.

        Example:
            >>> gf = GlobalFilter()
            >>> gf._initialize_global_filters()  # Typically used internally, not called directly by users

        #ai-gen-doc
        """
        global_filters = self._get_global_filters()

        self._content = []

        if self._filter_key in global_filters:
            self._content = global_filters[self._filter_key]

    def _update(self, op_type: str, filters_list: list) -> None:
        """Update the global filters list on this Commcell.

        This method updates the global filters by performing the specified operation type
        (such as 'ADD', 'OVERWRITE', or 'DELETE') on the provided list of filters.

        Args:
            op_type: The operation type to be performed. Accepted values are 'ADD', 'OVERWRITE', or 'DELETE'.
            filters_list: The list of filters to be associated with the global filter configuration.

        Raises:
            SDKException: If the update operation fails, if the response received is empty, or if the response indicates failure.

        Example:
            >>> global_filter = GlobalFilter()
            >>> filters = ['*.tmp', '*.log']
            >>> global_filter._update('ADD', filters)
            >>> print("Global filters updated successfully.")

        #ai-gen-doc
        """
        op_dict = {
            "ADD": 1,
            "OVERWRITE": 1,
            "DELETE": 3
        }

        request_json = {
            self._filter_key: {
                "opType": op_dict[op_type],
                "filters": filters_list
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._GLOBAL_FILTER, request_json
        )

        self.refresh()

        if flag:
            if response.json() and 'error' in response.json():
                if 'errorCode' in response.json()['error']:
                    error_code = int(response.json()['error']['errorCode'])

                    if error_code != 0:
                        raise SDKException(
                            'GlobalFilter', '102', 'Failed to update global filters'
                        )
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def content(self) -> str:
        """Get the content of the global filter as a read-only property.

        Returns:
            The filter content as a string.

        Example:
            >>> global_filter = GlobalFilter()
            >>> filter_content = global_filter.content  # Access the filter content
            >>> print(filter_content)

        #ai-gen-doc
        """
        return self._content

    def add(self, filters_list: list) -> None:
        """Add a list of filters to the agent's global filters list.

        Args:
            filters_list: A list of filters to be added to this agent's global filter configuration.

        Raises:
            SDKException: If the input data type is invalid, if updating the global filter content fails,
                if the response received is empty, or if the response is not successful.

        Example:
            >>> global_filter = GlobalFilter()
            >>> filters = ['*.tmp', '/var/log', '*.bak']
            >>> global_filter.add(filters)
            >>> print("Filters added successfully.")

        #ai-gen-doc
        """
        if not isinstance(filters_list, list):
            raise SDKException('GlobalFilter', '101')

        self._update("ADD", filters_list + self.content)

    def overwrite(self, filters_list: list) -> None:
        """Overwrite the existing global filters list with a new list of filters.

        Replaces the current set of global filters with the provided list. This operation 
        will remove all existing filters and set the filters list to the new values.

        Args:
            filters_list: A list of filters to replace the existing global filters.

        Raises:
            SDKException: 
                If the input data type is invalid.
                If the update of global filter content fails.
                If the response received is empty.
                If the response indicates failure.

        Example:
            >>> global_filter = GlobalFilter()
            >>> new_filters = ['*.tmp', '*.log', '/var/cache']
            >>> global_filter.overwrite(new_filters)
            >>> print("Global filters have been overwritten successfully.")

        #ai-gen-doc
        """
        if not isinstance(filters_list, list):
            raise SDKException('GlobalFilter', '101')

        self._update("OVERWRITE", filters_list)

    def delete_all(self) -> None:
        """Delete all filters from the agent filters list.

        This method removes every filter currently present in the agent's global filter list.

        Raises:
            SDKException: If the global filter content update fails, if the response is empty, or if the response indicates failure.

        Example:
            >>> global_filter = GlobalFilter()
            >>> global_filter.delete_all()
            >>> print("All filters have been deleted from the agent filters list.")

        #ai-gen-doc
        """
        self._update("OVERWRITE", [""])

    def refresh(self) -> None:
        """Reload the properties of the GlobalFilter object.

        This method updates the GlobalFilter instance with the latest information,
        ensuring that any changes made externally are reflected in the current object.

        Example:
            >>> global_filter = GlobalFilter()
            >>> global_filter.refresh()
            >>> print("GlobalFilter properties refreshed successfully")

        #ai-gen-doc
        """
        self._initialize_global_filters()
