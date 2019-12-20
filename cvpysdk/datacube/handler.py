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
        self.commcell_obj = self._datasource_object._commcell_object
        self._create_handler = self.commcell_obj._services['CREATE_HANDLER']
        self._get_handler = self.commcell_obj._services['GET_HANDLERS'] % (
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

    def get_properties(self, handler_name):
        """Returns a handler object of the specified handler name.

            Args:
                handler_name (str)  --  name of the handler

            Returns:
                dict -  properties for the given handler name


        """
        return self._handlers[handler_name]

    def get(self, handler_name):
        """Returns a handler object of the specified handler name.

            Args:
                handler_name (str)  --  name of the handler

            Returns:

                obj                 -- Object of Handler class


        """
        if not isinstance(handler_name, basestring):
            raise SDKException('Datacube', '101')

        if self.has_handler(handler_name):
            handler_id = self.get_properties(handler_name)['handlerId']
            return Handler(self._datasource_object, handler_name, handler_id)
        raise SDKException('Datacube', '102', "Unable to get handler class object")

    def delete(self, handler_name):
        """ deletes the handler associated with this handler object
                Args:

                    handler_name (str)     -- Name of the handler which needs to be deleted

                Returns:

                    None

                Raises:

                    SDKExpception:

                        if response is empty

                        if response is not success
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

        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'POST', self._create_handler, request_json
        )
        if flag:
            if response.json() and 'error' in response.json():
                if(response.json()['error'] == 'None' or response.json()['error'] is None):
                    self.refresh()  # reload new list.
                    return
                error_code = response.json()['error']['errorCode']
                if error_code == 0:
                    self.refresh()  # reload new list.
                    return
                error_message = response.json()['error']['errLogMessage']
                o_str = 'Failed to create handler\nError: "{0}"'.format(error_message)
                raise SDKException('Response', '102', o_str)
            raise SDKException('Response', '102')
        response_string = self.commcell_obj._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the handlers associated with the Datasource."""
        self._handlers = self._get_handlers()


class Handler(object):
    """Class for performing operations on a single Handler"""

    def __init__(self, datasource_object, handler_name, handler_id=None):
        """Initialize an object of the Handler class.

            Args:
                datasource_object     (object)    --  instance of the Datacube class

                handler_name          (str)       --  name of the Handler

                handler_id            (int)       --  Id of the Handler. Default = None

            Returns:

                object  -   instance of the Handler class
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
    def handler_id(self):
        """Returns the value of the handler id attribute."""
        return self._handler_id

    def _get_handler_id(self, handler_name):
        """ Get handler id for given handler name
                Args:

                    handler_name (str) -- Name of the Handler

                Returns:

                    int                -- Handler id

                Raises:

                    SDKExpception:

                        if response is empty

                        if response is not success

                """

        handlers = self.commcell_obj.Datacube.datasources.ds_handlers
        return handlers.get_properties(handler_name=handler_name)['handlerId']

    def get_handler_data(self, handler_filter=""):
        """ Executes handler for fetching data
                Args:

                     handler_filter    (str)  -- Filter which needs to applied for handler execution

                Returns:

                    dict        --  Dictionary of values fetched from handler execution

                Raises:
                    SDKExpception:

                        if response is empty

                        if response is not success

                        if error in fetching handler data
        """

        if not isinstance(handler_filter, basestring):
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

    def share(self, permission_list, operation_type, user_id, user_name, user_type):
        """ Share handler with user/usergroup
                Args:
                    permission_list (list)      -- List of permission

                    operation_type  (int)       -- Operation type (2-add / 3- delete)

                    user_id         (int)       -- User id of share user

                    user_name       (str)       -- Share user name

                    user_type       (int)       -- Share user type (Ex : 13- User)

                Returns:

                    None

                Raises:

                     SDKExpception:

                        if response is empty

                        if response is not success

                        if failed to share handler with User/Usergroup
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
