# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

from past.builtins import basestring

from .exception import SDKException


class GlobalFilters(object):
    """Class for managing global filters for this commcell"""

    def __init__(self, commcell_object):
        """Initializes global filter object

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the GlobalFilter class
        """
        self._commcell_object = commcell_object

        self._global_filter_dict = {
            "WINDOWS": 'windowsGlobalFilters',
            "UNIX": 'unixGlobalFilters',
            "NAS":  'nasGlobalFilters'
        }

    def __repr__(self):
        """Representation string for the instance of the GlobalFilter class."""
        o_str = "GlobalFilter class instance for CommServ '{0}'".format(
            self._commcell_object.commserv_name
        )
        return o_str

    def get(self, filter_name):
        """Returns the global filter agent object for specified filter name

            Args:
                filter_name     (str)   -- Global filter name for which the object is to be created
                    Accepted values: WINDOWS/ UNIX/ NAS

            Returns:
                object - GlobalFilter object for specified global filter

            Raises:
                SDKException:
                    if data type of input is invalid

                    if specified global filter doesn't exist
        """
        if not isinstance(filter_name, basestring):
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
    """Class to represent any one particular agent global filter"""

    def __init__(self, commcell_object, filter_name, filter_key):
        """Initializes global filter object

            Args:
                commcell_object     (object)    -- commcell object

                agent_key           (str)       --  agent key that shall be used in requests
        """
        self._filter_name = filter_name
        self._filter_key = filter_key
        self._commcell_object = commcell_object
        self._GLOBAL_FILTER = self._commcell_object._services['GLOBAL_FILTER']
        self._content = []

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        return "Global Filter object for: {0}".format(self._filter_name)

    def _get_global_filters(self):
        """Returns the global filters associated with this commcell"""
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

    def _initialize_global_filters(self):
        """Initializes global filters"""
        global_filters = self._get_global_filters()

        self._content = []

        if self._filter_key in global_filters:
            self._content = global_filters[self._filter_key]

    def _update(self, op_type, filters_list):
        """Updates the global filters list on tise commcell

            Args:
                op_type         (dict)  --  operation type to be performed
                        Accepted values: ADD/ OVERWRITE/ DELETE

                filters_list    (list)  --  list of filters to be associated

            Raises:
                SDKException:
                    if failed to update global filter content

                    if response received is empty

                    if response is not success
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
    def content(self):
        """Treats filter content as read-only property"""
        return self._content

    def add(self, filters_list):
        """Adds the filters list to the specified agent global filters list

            Args:
                filters_list    (list)  --  list of filters to be added to this agent

            Raises:
                SDKException:
                    if data type of input is invalid

                    if failed to update global filter content

                    if response received is empty

                    if response is not success
        """
        if not isinstance(filters_list, list):
            raise SDKException('GlobalFilter', '101')

        self._update("ADD", filters_list + self.content)

    def overwrite(self, filters_list):
        """Overwrites the existing filters list with given filter list

            Args:
                filters_list    (list)  --  list of filters to be replaced with existing

            Raises:
                SDKException:
                    if data type of input is invalid

                    if failed to update global filter content

                    if response received is empty

                    if response is not success
        """
        if not isinstance(filters_list, list):
            raise SDKException('GlobalFilter', '101')

        self._update("OVERWRITE", filters_list)

    def delete_all(self):
        """Deletes all the filters from given agent filters list

            Raises:
                SDKException:
                    if failed to update global filter content

                    if response received is empty

                    if response is not success
        """
        self._update("DELETE", [])

    def refresh(self):
        """Refresh the properties of the GlobalFilter."""
        self._initialize_global_filters()
