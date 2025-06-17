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

    get_datasource_properties()         --  get the properties of this data source

    get_crawl_history()                 --  get the crawl history of the data source.

    get_datasource_schema()             --  returns information about the schema of a data source

    update_datasource_schema(schema)    --  updates the schema for the given data source

    import_data(data)                   --  imports/pumps given data into data source.

    delete_content()                    --  deletes the contents of the data source.

    refresh()                           --  refresh the properties of the datasource

    start_job()                          --  Starts crawl job for the datasource

    get_status()                         --  Gets the status of the datasource

    share()                              -- Share the datasource with user or usergroup

    delete_datasource()                  -- deletes the datasource associated with this

DataSource Attributes
----------------------

    **computed_core_name**              --  Data source core name in index server

    **datasource_id**                   --  data source id

    **datasource_name**                 --  name of the data source

    **data_source_type**                --  data source type value

    **properties**						--	returns the properties of the data source

    **index_server_cloud_id**           --  index server cloudid associated to this data source

"""

from __future__ import absolute_import
from __future__ import unicode_literals

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
        self.commcell_obj = self._datacube_object._commcell_object
        self._all_datasources = self.commcell_obj._services[
            'GET_ALL_DATASOURCES']

        self._create_datasource = self.commcell_obj._services[
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
        return "Datasources class instance for Commcell"

    def get_datasource_properties(self, data_source_name):
        """Returns the properties of datasources.

            Args:

                data_source_name    (str)       -- Name of the data source

            Returns:
                dict - dictionary consisting of the properties of  datasources

        """
        return self._datasources[data_source_name]

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
            core_name = None
            cloud_id = None
            if 'computedCoreName' in collection:
                core_name = collection['computedCoreName']
            if 'cloudId' in collection:
                cloud_id = collection['cloudId']
            for datasource in collection['datasources']:
                datasource_dict = {}
                if core_name:
                    datasource_dict['computedCoreName'] = core_name
                if cloud_id:
                    datasource_dict['cloudId'] = cloud_id
                datasource_dict['data_source_id'] = datasource['datasourceId']
                datasource_dict['data_source_name'] = datasource['datasourceName']
                datasource_dict['data_source_type'] = SEDS_TYPE_DICT[
                    datasource['datasourceType']]
                if 'coreId' in datasource:
                    datasource_dict['coreId'] = datasource['coreId']
                if 'description' in datasource:
                    datasource_dict['description'] = datasource['description']
                if 'status' in datasource:
                    datasource_dict['total_count'] = datasource['status']['totalcount']
                    if 'state' in datasource['status']:
                        datasource_dict['state']= datasource['status']['state']
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
        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'GET', self._all_datasources
        )

        if flag:
            if response.json() and 'collections' in response.json():
                collections = response.json()['collections']
                return self._get_datasources_from_collections(collections)
            elif 'error' in response.json():
                raise SDKException('Datacube', '104')
            else:
                response = {}
                return response
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
        if not isinstance(datasource_name, str):
            raise SDKException('Datacube', '101')

        return self._datasources and datasource_name in self._datasources

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
        if not isinstance(datasource_name, str):
            raise SDKException('Datacube', '101')

        if self.has_datasource(datasource_name):
            datasource = self._datasources[datasource_name]

            return Datasource(
                self._datacube_object, datasource_name, datasource['data_source_id']
            )

        raise SDKException(
            'Datacube', '102', 'No datasource exists with the name: {0}'.format(
                datasource_name)
        )

    def add(self, datasource_name, analytics_engine, datasource_type, input_param):
        """Add a datasource.

            Args:
                datasource_name (str)   --  name of the datasource to add to the datacube

                analytics_engine (str)  --  name of the analytics engine or index server node to be associated with this
                                                datacube.

                datasource_type (str)  --  type of datasource to add

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
                input_param(list)      -- properties for datasource
            Raises:
                SDKException:
                    if type of the datasource name argument is not string

                    if type of the analytics_engine  argument is not string

                    if type of the datasource_type  argument is not string

                    if failed to add datasource

                    if response is empty

                    if response is not success

        """

        if not isinstance(datasource_name, str):
            raise SDKException('Datacube', '101')

        if not isinstance(analytics_engine, str):
            raise SDKException('Datacube', '101')

        if not isinstance(datasource_type, str):
            raise SDKException('Datacube', '101')

        engine_index = None
        for engine in self._datacube_object.analytics_engines:
            if engine["clientName"] == analytics_engine or engine['engineName'] == analytics_engine:
                engine_index = self._datacube_object.analytics_engines.index(engine)

        if engine_index is None:
            raise Exception("Unable to find Index server for client")

        request_json = {
            "collectionReq": {
                "collectionName": datasource_name,
                "ciserver": {
                    "cloudID": self._datacube_object.analytics_engines[engine_index][
                        "cloudID"]
                }
            },
            "dataSource": {
                "description": "",
                "datasourceType": datasource_type,
                "attribute": 0,
                "datasourceName": datasource_name

            }
        }
        if input_param is not None:
            request_json['dataSource']['properties'] = input_param

        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'POST', self._create_datasource, request_json
        )
        if flag and response.json():
            if 'error' in response.json():
                error_code = response.json()['error']['errorCode']
                if error_code == 0:
                    self.refresh()  # reload new list.
                    return

                error_message = response.json()['error']['errLogMessage']
                o_str = 'Failed to create datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Response', '102', o_str)
            elif 'collections' in response.json():
                self.refresh()  # reload new list.
                return
            else:
                raise SDKException('Response', '102')
        response_string = self.commcell_obj._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def delete(self, datasource_name):
        """Deletes specified datasource from data cube .

            Args:
                datasource_name     (str)   --  name of the datasource

            Raises:
                SDKException:
                    if type of the datasource name argument is not string

                    if no datasource exists with the given name

        """

        if not isinstance(datasource_name, str):
            raise SDKException('Datacube', '101')

        if not self.has_datasource(datasource_name):
            raise SDKException(
                'Datacube', '102', 'No datasource exists with the name: {0}'.format(
                    datasource_name)
            )

        self._delete_datasource = self.commcell_obj._services[
            'DELETE_DATASOURCE'] % (self.get(datasource_name).datasource_id)

        flag, response = self.commcell_obj._cvpysdk_object.make_request(
            'POST', self._delete_datasource)
        if flag:
            if 'errLogMessage' in response.json():
                error_message = response.json()['errLogMessage']
                o_str = 'Failed to delete datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Datacube', '102', o_str)
            else:
                return True
        else:
            raise SDKException('Response', '101', response.text)

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
        self._datasource_name = datasource_name
        self._commcell_object = self._datacube_object._commcell_object

        if datasource_id is not None:
            self._datasource_id = str(datasource_id)
        else:
            self._datasource_id = self._get_datasource_id()

        self._DATASOURCE = self._datacube_object._commcell_object._services['GET_DATASOURCE'] % (
            self._datasource_id
        )
        self._crawl_history = self._datacube_object._commcell_object._services['GET_CRAWL_HISTORY'] % (
            self._datasource_id)

        self._get_datasource_schema = self._datacube_object._commcell_object._services[
            'GET_DATASOURCE_SCHEMA'] % (self.datasource_id)

        self._delete_datasource_contents = self._datacube_object._commcell_object._services[
            'DELETE_DATASOURCE_CONTENTS'] % (self.datasource_id)

        self._datacube_import_data = self._datacube_object._commcell_object._services[
            'DATACUBE_IMPORT_DATA'] % ("json", self.datasource_id)

        self._update_datasource_schema = self._datacube_object._commcell_object._services[
            'UPDATE_DATASOURCE_SCHEMA']

        self._start_job_datasource = self._datacube_object._commcell_object._services[
            'START_JOB_DATASOURCE']

        self._get_status_datasource = self._datacube_object._commcell_object._services[
            'GET_STATUS_DATASOURCE']

        self._delete_datasource = self._datacube_object._commcell_object._services[
            'DELETE_DATASOURCE']

        self._share_datasource = self._datacube_object._commcell_object._services['SHARE_DATASOURCE']

        self.handlers = None
        self._handlers_obj = None
        self._computed_core_name = None
        self._cloud_id = None
        self._data_source_type = None
        self._properties = None
        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        return 'Datasource class instance for Commcell'

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
        data_source_dict = self._commcell_object.datacube.datasources.get_datasource_properties(self.datasource_name)
        if 'computedCoreName' in data_source_dict:
            self._computed_core_name = data_source_dict['computedCoreName']
        if 'cloudId' in data_source_dict:
            self._cloud_id = data_source_dict['cloudId']
        self._data_source_type = data_source_dict['data_source_type']
        return data_source_dict

    def start_job(self):
        """Starts the crawl job for the datasource

                Returns:
                    Str  -   Job id of crawl job

                Raises:
                    Exception:
                        failed to start job

        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._start_job_datasource % (self._datasource_id))

        if flag:
            if 'error' in response.json():
                error_message = response.json()['error']['errLogMessage']
                o_str = 'Failed to start job on datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Datacube', '102', o_str)
            elif response.json() and 'status' in response.json():
                return response.json()['status']['jobId']
            else:
                raise SDKException('Datacube', '102', "Status object not found in response")
        raise SDKException('Response', '101', response.text)

    def delete_datasource(self):
        """deletes the datasource

                    Returns:
                        true  -   if success

                    Raises:
                        Exception:
                            Error message for failed ops

                """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._delete_datasource % (self._datasource_id))

        if flag:
            if 'errLogMessage' in response.json():
                error_message = response.json()['errLogMessage']
                o_str = 'Failed to delete datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Datacube', '102', o_str)
            else:
                return True
        raise SDKException('Response', '101', response.text)

    def get_status(self):
        """Gets status of the datasource.

                Returns:
                    dict - containing all status information of datasource

                Raises:
                    Exception:
                            Failure to find datasource details

        """

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._get_status_datasource % (self._datasource_id))

        if flag:
            if 'error' in response.json():
                error_message = response.json()['error']['errLogMessage']
                o_str = 'Failed to Get status on datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Datacube', '102', o_str)
            elif response.json() and 'status' in response.json():
                return response.json()
            else:
                raise SDKException('Datacube', '102', "Status object not found in response")
        raise SDKException('Response', '101', response.text)

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
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._crawl_history
        )

        if flag:
            if response.json():
                return response.json()["status"]
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(
            response.text
        )
        raise SDKException('Response', '101', response_string)

    @property
    def datasource_id(self):
        """Returns the value of the data source id attribute."""
        return self._datasource_id

    @property
    def properties(self):
        """Returns all the data source properties"""
        return self._properties

    @property
    def datasource_name(self):
        """Returns the value of the data source name attribute."""
        return self._datasource_name

    @property
    def computed_core_name(self):
        """Returns the value of the computedcorename attribute."""
        return self._computed_core_name

    @property
    def index_server_cloud_id(self):
        """Returns the value of the cloud id attribute."""
        return self._cloud_id

    @property
    def data_source_type(self):
        """Returns the value of the data source type attribute."""
        return self._data_source_type

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
            'GET', self._get_datasource_schema
        )

        if flag:
            if response.json():
                return response.json()["collections"][0]["schema"]
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(
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
            "datasourceId": int(self.datasource_id),
            "schema": {
                "schemaFields": schema
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._update_datasource_schema, request_json
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json()['errorCode']
                if error_code == 0:
                    return
                error_message = response.json()['errLogMessage']
                o_str = 'Failed to update schema\nError: "{0}"'.format(error_message)
                raise SDKException('Response', '102', o_str)
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(
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
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._datacube_import_data, data
        )
        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json()['errorCode']
                if error_code == 0:
                    return
                error_message = response.json()['errLogMessage']
                o_str = 'Failed to import data\nError: "{0}"'.format(error_message)
                raise SDKException('Response', '102', o_str)
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(
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
            'POST', self._delete_datasource_contents
        )

        if flag:
            if response.json() and 'error' in response.json():
                error_message = response.json()['error']['errLogMessage']
                o_str = 'Failed to do soft delete on datasource\nError: "{0}"'.format(error_message)
                raise SDKException('Datacube', '102', o_str)
            return
        raise SDKException('Response', '101', response.text)

    def refresh(self):
        """Refresh the properties of the Datasource."""
        self._properties = self._get_datasource_properties()
        self.handlers = Handlers(self)

    @property
    def ds_handlers(self):
        """Returns the instance of the Handlers class."""
        try:
            if self._handlers_obj is None:
                self._handlers_obj = Handlers(self)
            return self._handlers_obj
        except BaseException:
            raise SDKException('Datacube', '102', "Failed to init Handlers")

    def share(self, permission_list, operation_type, user_id, user_name, user_type):
        """ Share datasource with user/usergroup
                Args:
                    permission_list (list)-- List of permission

                    operation_type (int)  -- Operation type (2-add / 3- delete)

                    user_id (int)         -- User id of share user

                    user_name (str)       -- Share user name

                    user_type (int)       -- Share user type (Ex : 13- User)

                Returns:
                    None

                Raises:
                    SDKExpception:

                        if response is empty

                        if response is not success

                        if failed to share the datasource with User/userGroup
        """
        category_permission_list = []
        for permission in permission_list:
            category_permission_list.append({'permissionId': permission, '_type_': 122})
        request_json = {
            "entityAssociated": {
                "entity": [
                    {
                        "_type_": 132,
                        "seaDataSourceId": int(self.datasource_id)
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
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'POST', self._share_datasource, request_json)

        if flag:
            if 'response' in response.json():
                resp = response.json()['response']
                resp = resp[0]
                if resp.get('errorCode') is not None and resp.get('errorCode') != 0:
                    error_message = resp['errorString']
                    o_str = 'Failed to share handler on datasource\nError: "{0}"'.format(error_message)
                    raise SDKException('Datacube', '102', o_str)
                elif resp.get('errorCode') is None:
                    raise SDKException('Datacube', '102', "No errorCode mentioned in response")
                return
        raise SDKException('Response', '101', response.text)
