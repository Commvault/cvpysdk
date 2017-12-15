# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing handler operations on a datasource.

Handlers and Handler are 2 classes defined in this file.

Handlers: Class for representing all the Handlers associated with the datasource

Handler: Class for a single Handler of the datasource


Handlers:

    __init__(commcell_object)   --  initialize object of Handlers class associated with commcell

    __str__()                   --  returns all the handlers associated with the commcell

    __repr__()                  --  returns the string representing instance of the Handlers class

    _get_handlers()             --  gets all the handlers associated with the commcell

    has_handler(handler_name)   --  checks if a handler exists with the given name or not

    get(handler_name)           --  gets the properties of the given handler

    add()                       --  adds a new handler to the datasource

    refresh()                   --  refresh the handlers associated with the datasource

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

from ..exception import SDKException


class Handlers(object):
    """Class for representing all the handlers associated with the datasource."""

    def __init__(self, datasource_object):
        """Initialize object of the Handlers class.

            Args:
                _datasource_object (object)  --  instance of the datastore class

            Returns:
                object - instance of the Handlers class

        """
        self._datasource_object = datasource_object
        self._CREATE_HANDLER = self._datasource_object._commcell_object._services['CREATE_HANDLER']
        self._GET_HANDLERS = self._datasource_object._commcell_object._services['GET_HANDLERS'] % (
            self._datasource_object.datasource_id
        )

        self._handlers = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all handlers of the datasource.

            Returns:
                str - string of all the handlers associated with the datasource

        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Handler')

        for index, handler in enumerate(self._handlers):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, handler)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Handlers class."""
        return "Handlers class instance for Datasource: '{0}'".format(
            self._datasource_object.datasource_name
        )

    def _get_handlers(self):
        """Gets all the handlers associated with the datasource

            Returns:
                dict - consists of all handlers in the datasource
                    {
                         "handler1_name": dict of handler1 properties,
                         "handler2_name": dict of handler2 properties
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._datasource_object._commcell_object._cvpysdk_object.make_request(
            'GET', self._GET_HANDLERS)

        if flag:
            if response.json() and 'handlerInfos' in response.json():
                handlers_dict = {}

                for dictionary in response.json()['handlerInfos']:
                    temp_name = dictionary['handlerName']
                    handlers_dict[temp_name] = dictionary

                return handlers_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._datasource_object._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def has_handler(self, handler_name):
        """Checks if a handler exists in the datasource with the input handler name.

            Args:
                handler_name (str)  --  name of the handler

            Returns:
                bool - boolean output whether the handler exists in the commcell or not

            Raises:
                SDKException:
                    if type of the handler name argument is not string

        """
        if not isinstance(handler_name, basestring):
            raise SDKException('Datacube', '101')

        return self._handlers and handler_name.lower() in map(str.lower, self._handlers)

    def get(self, handler_name):
        """Returns a handler object of the specified handler name.

            Args:
                handler_name (str)  --  name of the handler

            Returns:
                dict -  properties for the given handler name


        """
        return self._handlers[handler_name]

    def _delete(self, handler_name):
        """Deletes the handler from the commcell.

            Args:
                handler_name (str)  --  name of the handler to remove from the commcell

            Raises:
                SDKException:
                    if type of the handler name argument is not string

                    if failed to delete handler

                    if response is empty

                    if response is not success

                    if no handler exists with the given name

        """
        pass  # place holder when delete handler REST API is implemented.

    def add(self,
            handler_name,
            search_query,
            filter_query=None,
            facet_field=None,
            facet_query=None,
            rows=10,
            response_type="json",
            sort_column=[]):
        """Adds a new handler to the commcell.

            Args:
                handler_name    (str)   --  name of the handler to add to the datastore

                search_query    (list)  --  list of keywords on which the search is performed.

                filter_query    (list)  --  list of conditional queries which needs to be performed
                                                when the data is retrieved

                facet_field     (list)  --  list of fields to be faceted.

                facet_query     (list)  --  list of conditional queries for which the facet count
                                                should be retrieved

                rows            (int)   --  list of keywords on which the search is performed.

                response_type   (str)   --  format in which search results are retrieved.
                    default: json

                    Supported Types:
                        json

                        csv

                        xml


                sort_column     (list)  --  list of column name to be sorted


            Raises:
                SDKException:
                    if type of the handler name argument is not string

                    if failed to delete handler

                    if response is empty

                    if response is not success

                    if no handler exists with the given name

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

        flag, response = self._datasource_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_HANDLER, request_json
        )
        if flag:
            if response.json() and 'error' in response.json():
                error_code = response.json()['error']['errorCode']

                if error_code == 0:
                    return
                else:
                    error_message = response.json()['error']['errLogMessage']
                    o_str = 'Failed to create handler\nError: "{0}"'.format(error_message)
                    raise SDKException('Response', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._datasource_object._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()  # reload new list.

    def refresh(self):
        """Refresh the handlers associated with the Datasource."""
        self._handlers = self._get_handlers()
