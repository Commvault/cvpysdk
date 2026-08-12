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

"""Main file for performing handler operations on a datasource.

Handlers and Handler are 2 classes defined in this file.

Handlers: Class for representing all the Handlers associated with the datasource

Handler: Class for a single Handler of the datasource

Handlers:

    __init__()                  --  initialize object of Handlers class associated with commcell

    __str__()                   --  returns all the handlers associated with the commcell

    __repr__()                  --  returns the string representing instance of the Handlers class

    _get_handlers()             --  gets all the handlers associated with the commcell

    has_handler()               --  checks if a handler exists with the given name or not

    get_properties()            --  gets the properties of the given handler

    add()                       --  adds a new handler to the datasource

    refresh()                   --  refresh the handlers associated with the datasource

    get()                       -- gets the object for the given handler name

    delete()                    -- deletes the given handler name

Handler:

    __init__()                  -- Initialize object for Handler

    get_handler_data()          -- Execute the handler

    share()                     -- Share the handler with user or usergroup

"""


from __future__ import absolute_import
from __future__ import unicode_literals

from ..exception import SDKException


class Handlers(object):
    """
    Manages all handlers associated with a datasource.

    The Handlers class provides a comprehensive interface for managing, accessing,
    and manipulating handlers linked to a datasource object. It supports operations
    such as adding, deleting, retrieving, and refreshing handlers, as well as
    querying handler properties and existence.

    Key Features:
        - Initialization with a datasource object
        - String and representation methods for easy inspection
        - Internal retrieval of all handlers
        - Check for the existence of a handler by name
        - Retrieve properties of a specific handler
        - Get a handler by name
        - Delete a handler by name
        - Add a new handler with customizable parameters (search, filter, facet, rows, response type, sorting)
        - Refresh the handler list to reflect current datasource state

    #ai-gen-doc
    """

    def __init__(self, datasource_object: object) -> None:
        """Initialize a new instance of the Handlers class.

        Args:
            datasource_object: An instance of the datastore class to be used by the Handlers.

        Example:
            >>> datastore = Datastore()
            >>> handlers = Handlers(datastore)
            >>> print(f"Handlers object created: {handlers}")

        #ai-gen-doc
        """

        self._datasource_object = datasource_object
        self.commcell_obj = self._datasource_object._commcell_object
        self._create_handler = self.commcell_obj._services['CREATE_HANDLER']
        self._get_handler = self.commcell_obj._services['GET_HANDLERS'] % (
            self._datasource_object.datasource_id
        )

        self._handlers = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all handlers associated with the datasource.

        This method provides a human-readable summary of all handlers managed by the Handlers object.

        Returns:
            A string listing all handlers associated with the datasource.

        Example:
            >>> handlers = Handlers()
            >>> print(str(handlers))
            Handler1, Handler2, Handler3
            >>> # The output will display all handlers as a comma-separated string

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Handler')
        for index, handler in enumerate(self._handlers):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, handler)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return a string representation of the Handlers instance.

        This method provides a developer-friendly string that represents the current
        Handlers object, useful for debugging and logging purposes.

        Returns:
            A string representation of the Handlers instance.

        Example:
            >>> handlers = Handlers()
            >>> print(repr(handlers))
            <Handlers object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """
        return "Handlers class instance for Datasource: '{0}'".format(
            self._datasource_object.datasource_name
        )

    def _get_handlers(self) -> dict:
        """Retrieve all handlers associated with the datasource.

        Returns:
            dict: A dictionary containing all handlers in the datasource, where each key is a handler name
            and the value is a dictionary of that handler's properties.
            Example format:
                {
                    "handler1_name": { ... handler1 properties ... },
                    "handler2_name": { ... handler2 properties ... }
                }

        Raises:
            SDKException: If the response is empty or if the response indicates failure.

        Example:
            >>> handlers = handlers_obj._get_handlers()
            >>> print(f"Available handlers: {list(handlers.keys())}")
            >>> # Access properties of a specific handler
            >>> if 'handler1_name' in handlers:
            >>>     print(handlers['handler1_name'])

        #ai-gen-doc
        """

        flag, response = self._datasource_object._commcell_object._cvpysdk_object.make_request(
            'GET', self._get_handler)
        if flag:
            if response.json() and 'handlerInfos' in response.json():
                handlers_dict = {}
                for dictionary in response.json()['handlerInfos']:
                    temp_name = dictionary['handlerName']
                    handlers_dict[temp_name] = dictionary
                return handlers_dict
            raise SDKException('Response', '102')
        response_string = self._datasource_object._commcell_object._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def has_handler(self, handler_name: str) -> bool:
        """Check if a handler with the specified name exists in the datasource.

        Args:
            handler_name: The name of the handler to check for existence.

        Returns:
            True if the handler exists in the datasource; False otherwise.

        Raises:
            SDKException: If the handler_name argument is not a string.

        Example:
            >>> handlers = Handlers()
            >>> exists = handlers.has_handler("MyHandler")
            >>> print(f"Handler exists: {exists}")
            # Output: Handler exists: True

        #ai-gen-doc
        """
        if not isinstance(handler_name, str):
            raise SDKException('Datacube', '101')

        return self._handlers and handler_name.lower() in map(str.lower, self._handlers)

    def get_properties(self, handler_name: str) -> dict:
        """Retrieve the properties of a specified handler by name.

        Args:
            handler_name: The name of the handler whose properties are to be retrieved.

        Returns:
            A dictionary containing the properties for the given handler name.

        Example:
            >>> handlers = Handlers()
            >>> props = handlers.get_properties("FileHandler")
            >>> print(props)
            {'type': 'file', 'path': '/var/log/app.log', 'level': 'INFO'}

        #ai-gen-doc
        """
        return self._handlers[handler_name]

    def get(self, handler_name: str) -> 'Handler':
        """Retrieve a handler object by its name.

        Args:
            handler_name: The name of the handler to retrieve.

        Returns:
            Handler: An instance of the Handler class corresponding to the specified name.

        Example:
            >>> handlers = Handlers()
            >>> my_handler = handlers.get('backup_handler')
            >>> print(f"Handler type: {type(my_handler)}")
            >>> # Use the returned Handler object for further operations

        #ai-gen-doc
        """
        if not isinstance(handler_name, str):
            raise SDKException('Datacube', '101')

        if self.has_handler(handler_name):
            handler_id = self.get_properties(handler_name)['handlerId']
            return Handler(self._datasource_object, handler_name, handler_id)
        raise SDKException('Datacube', '102', "Unable to get handler class object")

    def delete(self, handler_name: str) -> None:
        """Delete the handler associated with this handler object.

        Args:
            handler_name: The name of the handler to be deleted.

        Raises:
            SDKExpception: If the response is empty or if the deletion is not successful.

        Example:
            >>> handlers = Handlers()
            >>> handlers.delete("my_handler")
            >>> print("Handler deleted successfully")

        #ai-gen-doc
        """
        handler_id = self.get(handler_name).handler_id
        self._delete_handler = self.commcell_obj._services['DELETE_HANDLER'] % (
            handler_id)

        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'POST', self._delete_handler)

        if flag:
            if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                error_message = response.json()['errLogMessage']
                o_str = 'Failed to Delete handler on datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Datacube', '102', o_str)
            elif 'errorCode' in response.json() and response.json()['errorCode'] == 0:
                return
            else:
                raise SDKException('Datacube', '102', "Empty Response with no errorCode")
        raise SDKException('Response', '101', response.text)

    def add(self,
            handler_name: str,
            search_query: list,
            filter_query: list = None,
            facet_field: list = None,
            facet_query: list = None,
            rows: int = 10,
            response_type: str = "json",
            sort_column: list = []) -> None:
        """Add a new handler to the Commcell datastore.

        This method registers a new handler with the specified configuration, including search and filter queries,
        faceting options, result formatting, and sorting preferences.

        Args:
            handler_name: Name of the handler to add to the datastore.
            search_query: List of keywords on which the search is performed.
            filter_query: Optional list of conditional queries to apply when retrieving data.
            facet_field: Optional list of fields to be faceted.
            facet_query: Optional list of conditional queries for which the facet count should be retrieved.
            rows: Number of rows (results) to retrieve. Default is 10.
            response_type: Format in which search results are retrieved. Supported types: "json" (default), "csv", "xml".
            sort_column: List of column names to sort the results by.

        Raises:
            SDKException: If the handler name is not a string, if the handler could not be added,
                if the response is empty or unsuccessful, or if no handler exists with the given name.

        Example:
            >>> handlers = Handlers()
            >>> handlers.add(
            ...     handler_name="my_handler",
            ...     search_query=["backup", "restore"],
            ...     filter_query=["client:Server01"],
            ...     facet_field=["status"],
            ...     facet_query=["status:completed"],
            ...     rows=20,
            ...     response_type="json",
            ...     sort_column=["date"]
            ... )
            >>> print("Handler 'my_handler' added successfully.")

        #ai-gen-doc
        """
        request_json = {
            "dataSourceId": self._datasource_object.datasource_id,
            "handlerName": handler_name,
            "handlerInfo": {
                "defaultParams": {
                    "q": search_query,
                    "fq": filter_query,
                    "sort": sort_column,
                    "facet": [
                        "true" if facet_field or facet_query else "false"
                    ],
                    "facet.field": facet_field,
                    "facet.query": facet_query,
                    "rows": [rows],
                    "wt": [response_type]
                },
                "appendParams": {},
                "rawDefaultParams": [],
                "rawAppendParams": [],
                "rawInvariantParams": [],
                "alwaysDecode": "true"
            }
        }

        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'POST', self._create_handler, request_json
        )
        if flag:
            if response.json():
                if 'error' in response.json() and (response.json()['error'] == 'None' or response.json()['error'] is None):
                    self.refresh()  # reload new list.
                    return
                elif 'error' in response.json():
                    error_code = response.json()['error'].get('errorCode',0)
                    if error_code == 0:
                        self.refresh()  # reload new list.
                        return
                    error_message = response.json()['error']['errLogMessage']
                    o_str = 'Failed to create handler\nError: "{0}"'.format(error_message)
                    raise SDKException('Response', '102', o_str)
                self.refresh()  # reload new list.
                return
            raise SDKException('Response', '102')
        response_string = self.commcell_obj._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Reload the handlers associated with the Datasource.

        This method refreshes the internal state of the handlers, ensuring that any changes 
        to the underlying Datasource are reflected in the handler objects.

        Example:
            >>> handlers = Handlers()
            >>> handlers.refresh()  # Reloads the handlers to reflect current Datasource state
            >>> print("Handlers refreshed successfully")

        #ai-gen-doc
        """
        self._handlers = self._get_handlers()


class Handler(object):
    """
    Handler class for managing and operating on individual handler instances.

    This class provides functionality to initialize handler objects with specific
    data sources, names, and IDs. It offers methods to retrieve handler data based
    on filters, access handler IDs, and share handler resources with specified
    permissions and user details.

    Key Features:
        - Initialization with datasource, handler name, and handler ID
        - Property access for handler ID
        - Retrieval of handler data using filters
        - Internal method for obtaining handler ID by name
        - Sharing handler resources with customizable permissions and user information

    #ai-gen-doc
    """

    def __init__(self, datasource_object: object, handler_name: str, handler_id: int = None) -> None:
        """Initialize a Handler object for managing data sources.

        Args:
            datasource_object: Instance of the Datacube class representing the data source.
            handler_name: Name to assign to the Handler.
            handler_id: Optional integer ID for the Handler. If not provided, defaults to None.

        Example:
            >>> datacube = Datacube()
            >>> handler = Handler(datacube, "MyHandler")
            >>> # Optionally specify a handler ID
            >>> handler_with_id = Handler(datacube, "MyHandler", handler_id=101)

        #ai-gen-doc
        """
        self._datasource_object = datasource_object
        self._handler_name = handler_name
        if handler_id is None:
            self._handler_id = self._get_handler_id(handler_name)
        else:
            self._handler_id = handler_id
        self.commcell_obj = self._datasource_object._commcell_object
        self._share_handler = self.commcell_obj._services['SHARE_HANDLER']

    @property
    def handler_id(self) -> int:
        """Get the unique identifier for this handler.

        Returns:
            int: The handler's unique ID.

        Example:
            >>> handler = Handler()
            >>> handler_id = handler.handler_id  # Access the handler's ID using the property
            >>> print(f"Handler ID: {handler_id}")

        #ai-gen-doc
        """
        return self._handler_id

    def _get_handler_id(self, handler_name: str) -> int:
        """Retrieve the handler ID for a given handler name.

        Args:
            handler_name: The name of the handler for which the ID is required.

        Returns:
            The integer ID corresponding to the specified handler name.

        Raises:
            SDKExpception: If the response is empty or the response indicates failure.

        Example:
            >>> handler = Handler()
            >>> handler_id = handler._get_handler_id("MyHandler")
            >>> print(f"Handler ID: {handler_id}")

        #ai-gen-doc
        """

        handlers = self.commcell_obj.Datacube.datasources.ds_handlers
        return handlers.get_properties(handler_name=handler_name)['handlerId']

    def get_handler_data(self, handler_filter: str = "") -> dict:
        """Execute the handler to fetch data with an optional filter.

        Args:
            handler_filter: Optional string filter to apply during handler execution. 
                If not provided, all handler data will be fetched.

        Returns:
            dict: Dictionary containing the values fetched from the handler execution.

        Raises:
            SDKExpception: 
                If the response is empty, not successful, or if there is an error fetching handler data.

        Example:
            >>> handler = Handler()
            >>> data = handler.get_handler_data("status=active")
            >>> print(data)
            {'result': 'success', 'data': [...]}

        #ai-gen-doc
        """

        if not isinstance(handler_filter, str):
            raise SDKException('Datacube', '101')
        self._execute_handler = self.commcell_obj._services['EXECUTE_HANDLER'] % (
            self.handler_id, self._handler_name, handler_filter
        )
        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'GET', self._execute_handler)
        if flag:
            if response.json() and 'response' in response.json():
                return response.json()['response']
            if 'error' in response.json():
                error_message = response.json()['error']['errLogMessage']
                o_str = 'Failed to execute handler on datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Datacube', '102', o_str)
            raise SDKException('Datacube', '102', "No response object in Json")
        raise SDKException('Response', '101', response.text)

    def share(self, permission_list: list, operation_type: int, user_id: int, user_name: str, user_type: int) -> None:
        """Share the handler with a specified user or user group.

        This method assigns or removes permissions for a user or user group on the handler,
        based on the provided operation type and permission list.

        Args:
            permission_list: List of permissions to assign or remove.
            operation_type: Operation type (2 for add, 3 for delete).
            user_id: The unique identifier of the user or user group to share with.
            user_name: The name of the user or user group to share with.
            user_type: The type of user (e.g., 13 for User).

        Raises:
            SDKExpception: If the response is empty, not successful, or if sharing the handler fails.

        Example:
            >>> handler = Handler()
            >>> permissions = [1, 2, 3]  # Example permission IDs
            >>> handler.share(permissions, 2, 101, "jdoe", 13)
            >>> print("Handler shared successfully with user jdoe")
        #ai-gen-doc
        """

        category_permission_list = []
        for permission in permission_list:
            category_permission_list.append({'permissionId': permission, '_type_': 122})
        request_json = {
            "entityAssociated": {
                "entity": [
                    {
                        "entityType": 157,
                        "_type_": 150,
                        "entityId": self.handler_id
                    }
                ]
            },
            "securityAssociations": {
                "processHiddenPermission": 1,
                "associationsOperationType": operation_type,
                "associations": [
                    {
                        "userOrGroup": [
                            {
                                "userId": user_id,
                                "_type_": user_type,
                                "userName": user_name
                            }
                        ],
                        "properties": {
                            "categoryPermission": {
                                "categoriesPermissionList": category_permission_list
                            }
                        }
                    }
                ]
            }
        }
        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'POST', self._share_handler, request_json)
        if flag:
            if 'response' in response.json():
                resp = response.json()['response']
                resp = resp[0]
                if resp.get('errorCode') != 0:
                    error_message = resp['errorString']
                    o_str = 'Failed to share handler on datasource\nError: "{0}"'.format(error_message)
                    raise SDKException('Datacube', '102', o_str)
                return response.json()['response']
            raise SDKException('Datacube', '102', "Empty Response")
        raise SDKException('Response', '101', response.text)
