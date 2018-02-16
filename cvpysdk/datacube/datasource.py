# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on Datasources, and a single Datasource in the Datacube.

`Datasources`, and `Datasource` are 2 classes defined in this file.

Datasources:    Class for representing all the Datasources in the Datacube.

Datasource:     Class for representing a single Datasource in the Datacube.


Datasources:

    __init__(datacube_object)           --  initialise object of the Datasources class

    __str__()                           --  prints all the datasources

    __repr__()                          --  returns the string representation of this instance

    _get_datasources_from_collections() --  gets all the datasources from a list of collections

    _get_all_datasources()              --  gets the collections, and all datasources in it

    has_datasource()                    --  checks if a datasource exists with the given name

    get(datasource_name)                --  returns an instance of the Datasource class,
                                                for the input datasource name

    add(datasource_name,
        analytics_engine,
        datasource_type)                --  adds new datasource to the datacube

    delete(datasource_name)             --  deletes the give datasource to the datacube

    refresh()                           --  refresh the datasources associated with the datacube


Datasource:

    __init__(
        datacube_object,
        datasource_name,
        datasource_id=None)             --  initialize an object of Class with the given datasource
                                                name and id, and associated to the datacube

    __repr__()                          --  return the datasource name, the instance is
                                                associated with

    _get_datasource_id()                --  method to get the data source id, if not specified
                                                in __init__

    _get_datasource_properties()        --  get the properties of this data source

    get_crawl_history()                 --  get the crawl history of the data source.

    get_datasource_schema()             --  returns information about the schema of a data source

    update_datasource_schema(schema)    --  updates the schema for the given data source

    import_data(data)                   --  imports/pumps given data into data source.

    delete_content()                    --  deletes the contents of the data source.

    refresh()                           --  refresh the properties of the datasource

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

from .handler import Handlers
from .sedstype import SEDS_TYPE_DICT

from ..exception import SDKException


class Datasources(object):
    """Class for representing all the Datasources in the Datacube."""

    def __init__(self, datacube_object):
        """Initializes an instance of the Datasources class.

            Args:
                datacube_object     (object)    --  instance of the Datacube class

            Returns:
                object  -   instance of the Datasources class

        """
        self._datacube_object = datacube_object

        self._ALL_DATASOURCES = self._datacube_object._commcell_object._services[
            'GET_ALL_DATASOURCES']

        self._CREATE_DATASOURCE = self._datacube_object._commcell_object._services[
            'CREATE_DATASOURCE']

        self._datasources = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all datasources in datacube.

            Returns:
                str - string of all the datasources associated with the datacube

        """
        representation_string = '{:^5}\t{:30}\n\n'.format(
            'ID', 'Data Source Name')
        for datasource in self._datasources.values():
            sub_str = '{:^5}\t{:30}\n'.format(
                datasource['data_source_id'], datasource['data_source_name']
            )
            representation_string += sub_str

        return representation_string

    def __repr__(self):
        """Representation string for the instance of the Datasources class."""
        return "Datasources class instance for Commcell: '{0}'".format(
            self._datacube_object._commcell_object.commserv_name
        )

    @staticmethod
    def _get_datasources_from_collections(collections):
        """Extracts all the datasources, and their details from the list of collections given,
            and returns the dictionary of all datasources.

            Args:
                collections     (list)  --  list of all collections

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single datasource

                    {
                        'data_source_1_name': {

                            'data_source_id': 21,

                            'data_source_name': '',

                            'description': '',

                            'data_source_type': '',

                            'total_count': 1234,

                            'state': 1
                        },

                        'data_source_2_name': {},

                        'data_source_3_name': {}
                        ...
                    }

        """
        _datasources = {}

        for collection in collections:
            for datasource in collection['datasources']:
                datasource_dict = {}

                datasource_dict['data_source_id'] = datasource['datasourceId']
                datasource_dict['data_source_name'] = datasource['datasourceName']
                datasource_dict['description'] = datasource['description']
                datasource_dict['data_source_type'] = SEDS_TYPE_DICT[datasource['datasourceType']]
                datasource_dict['total_count'] = datasource['status']['totalcount']
                datasource_dict['state'] = datasource['status']['state']

                _datasources[datasource['datasourceName']] = datasource_dict

        return _datasources

    def _get_all_datasources(self):
        """Gets the list of all datasources associated with this Datacube instance.

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single datasource

                    {
                        'data_source_1_name': {

                            'data_source_id': 21,

                            'data_source_name': '',

                            'description': '',

                            'data_source_type': '',

                            'total_count': 1234,

                            'state': 1
                        },

                        'data_source_2_name': {},

                        'data_source_3_name': {}
                        ...
                    }

        """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'GET', self._ALL_DATASOURCES
        )

        if flag:
            if response.json() and 'collections' in response.json():
                collections = response.json()['collections']
                return self._get_datasources_from_collections(collections)
            else:
                raise SDKException('Datacube', '104')
        else:
            self._datacube_object._response_not_success(response)

    def has_datasource(self, datasource_name):
        """Checks if a datasource exists in the Datacube with the input datasource name.

            Args:
                datasource_name     (str)   --  name of the datasource

            Returns:
                bool    -   boolean output whether the datasource exists in the datacube or not

            Raises:
                SDKException:
                    if type of the datasource name argument is not string

        """
        if not isinstance(datasource_name, basestring):
            raise SDKException('Datacube', '101')

        return self._datasources and datasource_name.lower() in self._datasources

    def get(self, datasource_name):
        """Returns a datasource object of the specified datasource name.

            Args:
                datasource_name     (str)   --  name of the datasource

            Returns:
                object  -   instance of the Datasource class for the given datasource name

            Raises:
                SDKException:
                    if type of the datasource name argument is not string

                    if no datasource exists with the given name

        """
        if not isinstance(datasource_name, basestring):
            raise SDKException('Datacube', '101')

        datasource_name = datasource_name.lower()

        if self.has_datasource(datasource_name):
            datasource = self._datasources[datasource_name]

            return Datasource(
                self._datacube_object, datasource_name, datasource['data_source_id']
            )

        raise SDKException(
            'Datacube', '102', 'No datasource exists with the name: {0}'.format(
                datasource_name)
        )

    def add(self, datasource_name, analytics_engine, datasource_type):
        """Deletes the handler from the commcell.

            Args:
                datasource_name (str)   --  name of the datasource to add to the datacube

                analytics_engine (str)  --  name of the analytics engine to be associated with this
                                                datacube.

                datasource_type (list)  --  type of datasource to add

                                            Valid values are:
                                            1: Database
                                            2: Web site
                                            3: CSV
                                            4: File system
                                            5: NAS
                                            6: Eloqua
                                            8: Salesforce
                                            9: LDAP
                                            10: Federated Search
                                            11: Open data source
                                            12: HTTP
            Raises:
                SDKException:
                    if type of the datasource name argument is not string

                    if type of the analytics_engine  argument is not string

                    if type of the datasource_type  argument is not string

                    if failed to delete handler

                    if response is empty

                    if response is not success

        """

        if not isinstance(datasource_name, basestring):
            raise SDKException('Datacube', '101')

        if not isinstance(analytics_engine, basestring):
            raise SDKException('Datacube', '101')

        if not isinstance(datasource_type, basestring):
            raise SDKException('Datacube', '101')

        engine_index = (
            self._datacube_object.analytics_engines.index(engine)
            for engine in self._datacube_object.analytics_engines
            if engine["clientName"] == analytics_engine
        ).next()

        request_json = {
            "collectionReq": {
                "collectionName": datasource_name,
                "ciserver": {
                    "cloudID": self._datacube_object.analytics_engines[engine_index]["cloudID"]
                }
            },
            "dataSource": {
                "description": "",
                "datasourceType": datasource_type,
                "attribute": 0,
                "datasourceName": datasource_name
            }
        }

        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_DATASOURCE, request_json
        )
        if flag and response.json():
            if 'error' in response.json():
                error_code = response.json()['error']['errorCode']
                if error_code == 0:
                    return
                else:
                    error_message = response.json()['error']['errLogMessage']
                    o_str = 'Failed to create datasource\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Response', '102', o_str)
            elif 'collections' in response.json():
                return
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._datacube_object._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()  # reload new list.

    def delete(self, datasource_name):
        """Deletes specified datasource from data cube .

            Args:
                datasource_name     (str)   --  name of the datasource

            Raises:
                SDKException:
                    if type of the datasource name argument is not string

                    if no datasource exists with the given name

        """

        if not isinstance(datasource_name, basestring):
            raise SDKException('Datacube', '101')

        if not self.has_datasource(datasource_name):
            raise SDKException(
                'Datacube', '102', 'No datasource exists with the name: {0}'.format(
                    datasource_name)
            )

        self._DELETE_DATASOURCE = self._datacube_object._commcell_object._services[
            'DELETE_DATASOURCE'] % (self.get(datasource_name).datasource_id)

        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._DELETE_DATASOURCE, {}
        )
        if flag:
            # on success empty {} json is returned
            self.refresh()
        else:
            response_string = self._datacube_object._commcell_object._update_response_(
                response.text
            )
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the datasources associated with the Datacube."""
        self._datasources = self._get_all_datasources()


class Datasource(object):
    """Class for performing operations on a single datasource"""

    def __init__(self, datacube_object, datasource_name, datasource_id=None):
        """Initialize an object of the Datasource class.

            Args:
                datacube_object     (object)    --  instance of the Datacube class

                datasource_name     (str)       --  name of the datasource

                datasource_id       (str)       --  id of the datasource
                    default: None

            Returns:
                object  -   instance of the Datasource class
        """
        self._datacube_object = datacube_object
        self._datasource_name = datasource_name.lower()
        self._commcell_object = self._datacube_object._commcell_object

        if datasource_id is not None:
            self._datasource_id = str(datasource_id)
        else:
            self._datasource_id = self._get_datasource_id()

        self._DATASOURCE = self._datacube_object._commcell_object._services['GET_DATASOURCE'] % (
            self._datasource_id
        )
        self._CRAWL_HISTORY = self._datacube_object._commcell_object._services['GET_CRAWL_HISTORY'] % (
            self._datasource_id)

        self._GET_DATASOURCE_SCHEMA = self._datacube_object._commcell_object._services[
            'GET_DATASOURCE_SCHEMA'] % (self.datasource_id)

        self._DELETE_DATASOURCE_CONTENTS = self._datacube_object._commcell_object._services[
            'DELETE_DATASOURCE_CONTENTS'] % (self.datasource_id)

        self._DATACUBE_IMPORT_DATA = self._datacube_object._commcell_object._services[
            'DATACUBE_IMPORT_DATA'] % ("json", self.datasource_id)

        self._UPDATE_DATASOURCE_SCHEMA = self._datacube_object._commcell_object._services[
            'UPDATE_DATASOURCE_SCHEMA']

        self.handlers = None
        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Datasource class instance for Commcell: "{0}"'

        return representation_string.format(
            self._datacube_object._commcell_object.commserv_name
        )

    def _get_datasource_id(self):
        """Gets the datasource id associated with this datasource.

            Returns:
                str     -   id associated with this datasource

        """
        datasources = Datasources(self._datacube_object)
        return datasources.get(self.datasource_name).datasource_id

    def _get_datasource_properties(self):
        """Gets the properties of this datasource.

            Returns:
                dict - dictionary consisting of the properties of this datasource

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        # TODO: Populate self.properties in this method
        pass

    def get_crawl_history(self, last_crawl_history=False):
        """Gets the Crawling  history for this datasource.

            Args:
                last_crawl_history (bool)    -- if set to True , returns
                the status of and information about the most recent crawling
                operation for a data source in Data Cube

            Returns:
                list - list consisting of key value pair for history details of this datasource

                 [
                    {
                        "numFailed": ,
                        "totalcount": ,
                        "endUTCTime": ,
                        "numAccessDenied": ,
                        "numAdded": ,
                        "startUTCTime": ,
                        "state":
                    }
                ]

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'GET', self._CRAWL_HISTORY
        )

        if flag:
            if response.json():
                return response.json()["status"]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._datacube_object._commcell_object._update_response_(
                response.text
            )
            raise SDKException('Response', '101', response_string)

    @property
    def datasource_id(self):
        """Returns the value of the data source id attribute."""
        return self._datasource_id

    @property
    def datasource_name(self):
        """Returns the value of the data source name attribute."""
        return self._datasource_name

    def get_datasource_schema(self):
        """returns information about the schema of a data source.

            Returns:
                dict - dict consisting of all schema fields of this datasource grouped
                under dynSchemaFields and schemaFields

                {
                "uniqueKey": "contentid",
                "schemaFields": [{properties of field},list of fields]
               "dynSchemaFields":[{properties of field},list of fields]

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'GET', self._GET_DATASOURCE_SCHEMA
        )

        if flag:
            if response.json():
                return response.json()["collections"][0]["schema"]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._datacube_object._commcell_object._update_response_(
                response.text
            )
            raise SDKException('Response', '101', response_string)

    def update_datasource_schema(self, schema):
        """updates the schema of a data source.

            Args:
                schema (list)   -- list of  properties of schemas represented as key value pair.
                [{
                                    "fieldName": "",
                                    "indexed": "",
                                    "autocomplete": "",
                                    "type": "",
                                    "searchDefault": "",
                                    "multiValued": ""
                                }]
                Valid values for type are as follows:
                    [string, int, float, long, double, date, longstring]
                indexed, autocomplete, searchDefault, multiValued takes 0/1

            Raises:
                SDKException:
                    if response is empty

                    if type of the schema argument is not list

                    if response is not success

        """
        if not isinstance(schema, list):
            raise SDKException('Datacube', '101')

        for element in schema:
            if not isinstance(element, dict):
                raise SDKException('Datacube', '101')

        request_json = {
            "datasourceId": self.datasource_id,
            "schema": {
                "schemaFields": schema
            }
        }

        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._UPDATE_DATASOURCE_SCHEMA, request_json
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json()['errorCode']
                if error_code == 0:
                    return
                else:
                    error_message = response.json()['errLogMessage']
                    o_str = 'Failed to update schema\nError: "{0}"'.format(error_message)
                    raise SDKException('Response', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def import_data(self, data):
        """imports/pumps given data into data source.

            Args:
                data (list)   -- data to be indexed and pumped into  solr.list of key value pairs.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._DATACUBE_IMPORT_DATA, data
        )
        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json()['errorCode']

                if error_code == 0:
                    return
                else:
                    error_message = response.json()['errLogMessage']
                    o_str = 'Failed to import data\nError: "{0}"'.format(error_message)
                    raise SDKException('Response', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._commcell_object._update_response_(
                response.text
            )
            raise SDKException('Response', '101', response_string)

    def delete_content(self):
        """deletes the content of a data source from Data Cube.
           The data source itself is not deleted using this API.

            Raises:
                SDKException:

                    if response is empty

                    if response is not success

        """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._DELETE_DATASOURCE_CONTENTS
        )

        if flag:
            return
        else:
            response_string = self._commcell_object._commcell_object._update_response_(
                response.text
            )
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the Datasource."""
        self._properties = self._get_datasource_properties()
        self.handlers = Handlers(self)
