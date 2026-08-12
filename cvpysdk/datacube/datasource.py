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
    """
    Manages and represents all Datasources within a Datacube environment.

    This class provides a comprehensive interface for handling datasources,
    including creation, retrieval, deletion, and property management. It is
    designed to interact with a Datacube object and supports operations for
    maintaining and querying the collection of datasources.

    Key Features:
        - Initialization with a Datacube object
        - String and representation methods for easy inspection
        - Retrieve properties of a specific datasource
        - Internal methods for extracting datasources from collections
        - Fetch all available datasources
        - Check existence of a datasource by name
        - Get a datasource by name
        - Add new datasources with analytics engine, type, and input parameters
        - Delete existing datasources
        - Refresh the datasource collection

    #ai-gen-doc
    """

    def __init__(self, datacube_object: object) -> None:
        """Initialize a new instance of the Datasources class.

        Args:
            datacube_object: An instance of the Datacube class to associate with this Datasources object.

        Example:
            >>> datacube = Datacube('server_name', 'username', 'password')
            >>> datasources = Datasources(datacube)
            >>> print("Datasources object created successfully")

        #ai-gen-doc
        """
        self._datacube_object = datacube_object
        self.commcell_obj = self._datacube_object._commcell_object
        self._all_datasources = self.commcell_obj._services[
            'GET_ALL_DATASOURCES']

        self._create_datasource = self.commcell_obj._services[
            'CREATE_DATASOURCE']

        self._datasources = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all datasources in the datacube.

        This method provides a human-readable summary of all datasources associated 
        with the datacube, typically listing their names or identifiers.

        Returns:
            A string containing the details of all datasources in the datacube.

        Example:
            >>> datasources = Datasources()
            >>> print(str(datasources))
            >>> # Output: "Datasource1, Datasource2, Datasource3"

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:30}\n\n'.format(
            'ID', 'Data Source Name')
        for datasource in self._datasources.values():
            sub_str = '{:^5}\t{:30}\n'.format(
                datasource['data_source_id'], datasource['data_source_name']
            )
            representation_string += sub_str

        return representation_string

    def __repr__(self) -> str:
        """Return the string representation of the Datasources instance.

        This method provides a developer-friendly string that represents the current
        Datasources object, useful for debugging and logging purposes.

        Returns:
            A string representation of the Datasources instance.

        Example:
            >>> datasources = Datasources()
            >>> print(repr(datasources))
            <Datasources object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        return "Datasources class instance for Commcell"

    def get_datasource_properties(self, data_source_name: str) -> dict:
        """Retrieve the properties of a specified data source.

        Args:
            data_source_name: The name of the data source whose properties are to be fetched.

        Returns:
            A dictionary containing the properties of the specified data source.

        Example:
            >>> datasources = Datasources()
            >>> properties = datasources.get_datasource_properties("OracleDB")
            >>> print(properties)
            {'name': 'OracleDB', 'type': 'Database', 'status': 'Active', ...}

        #ai-gen-doc
        """
        return self._datasources[data_source_name]

    @staticmethod
    def _get_datasources_from_collections(collections: list) -> dict:
        """Extract all datasources and their details from a list of collections.

        This method processes the provided list of collection objects and extracts
        information about each datasource contained within. The result is a dictionary
        where each key is a datasource name, and the value is a dictionary of its details.

        Args:
            collections: List of collection objects or dictionaries containing datasource information.

        Returns:
            Dictionary mapping datasource names to their details. Each value is a dictionary
            with keys such as 'data_source_id', 'data_source_name', 'description',
            'data_source_type', 'total_count', and 'state'.

            Example return structure:
                {
                    'data_source_1_name': {
                        'data_source_id': 21,
                        'data_source_name': 'data_source_1_name',
                        'description': 'Description of datasource 1',
                        'data_source_type': 'TypeA',
                        'total_count': 1234,
                        'state': 1
                    },
                    'data_source_2_name': {
                        ...
                    }
                }

        Example:
            >>> collections = [...]  # List of collection objects with datasource info
            >>> datasources = Datasources._get_datasources_from_collections(collections)
            >>> print(datasources.keys())
            dict_keys(['data_source_1_name', 'data_source_2_name'])
            >>> first_ds = datasources['data_source_1_name']
            >>> print(first_ds['description'])
            Description of datasource 1

        #ai-gen-doc
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

    def _get_all_datasources(self) -> dict:
        """Retrieve all datasources associated with this Datacube instance.

        Returns:
            dict: A dictionary where each key is a datasource name and the value is a dictionary
            containing details about that datasource, such as its ID, name, description, type,
            total count, and state.

            Example structure:
                {
                    'data_source_1_name': {
                        'data_source_id': 21,
                        'data_source_name': 'data_source_1_name',
                        'description': 'Sample description',
                        'data_source_type': 'TypeA',
                        'total_count': 1234,
                        'state': 1
                    },
                    'data_source_2_name': {
                        ...
                    }
                }

        Example:
            >>> datasources = Datasources()
            >>> all_sources = datasources._get_all_datasources()
            >>> for name, details in all_sources.items():
            ...     print(f"Datasource: {name}, ID: {details['data_source_id']}")
            >>> # This will print the name and ID of each datasource

        #ai-gen-doc
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

    def has_datasource(self, datasource_name: str) -> bool:
        """Check if a datasource with the specified name exists in the Datacube.

        Args:
            datasource_name: The name of the datasource to check for existence.

        Returns:
            True if the datasource exists in the Datacube, False otherwise.

        Raises:
            SDKException: If the type of the datasource_name argument is not a string.

        Example:
            >>> datasources = Datasources()
            >>> exists = datasources.has_datasource("SalesData")
            >>> print(f"Datasource exists: {exists}")
            # Output: Datasource exists: True

        #ai-gen-doc
        """
        if not isinstance(datasource_name, str):
            raise SDKException('Datacube', '101')

        return self._datasources and datasource_name in self._datasources

    def get(self, datasource_name: str) -> 'Datasource':
        """Retrieve a Datasource object by its name.

        Args:
            datasource_name: The name of the datasource to retrieve.

        Returns:
            Datasource: An instance of the Datasource class corresponding to the specified name.

        Raises:
            SDKException: If the datasource_name is not a string or if no datasource exists with the given name.

        Example:
            >>> datasources = Datasources(commcell_object)
            >>> ds = datasources.get("SalesDB")
            >>> print(f"Datasource name: {ds.name}")

        #ai-gen-doc
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

    def add(self, datasource_name: str, analytics_engine: str, datasource_type: str, input_param: list) -> None:
        """Add a new datasource to the datacube.

        This method registers a new datasource with the specified name, associates it with an analytics engine,
        and sets its type and properties.

        Args:
            datasource_name: The name of the datasource to add to the datacube.
            analytics_engine: The name of the analytics engine or index server node to associate with this datacube.
            datasource_type: The type of datasource to add. Valid values include:
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
            input_param: A list of properties for the datasource.

        Raises:
            SDKException: If any of the following conditions occur:
                - The type of the datasource_name argument is not string.
                - The type of the analytics_engine argument is not string.
                - The type of the datasource_type argument is not string.
                - Failed to add the datasource.
                - The response is empty.
                - The response is not successful.

        Example:
            >>> datasources = Datasources()
            >>> properties = [{"propertyName": "host", "propertyValue": "db.example.com"}]
            >>> datasources.add(
            ...     datasource_name="SalesDB",
            ...     analytics_engine="IndexServer1",
            ...     datasource_type="1",
            ...     input_param=properties
            ... )
            >>> print("Datasource 'SalesDB' added successfully.")

        #ai-gen-doc
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

    def delete(self, datasource_name: str) -> None:
        """Delete the specified datasource from the data cube.

        Args:
            datasource_name: The name of the datasource to be deleted.

        Raises:
            SDKException: If the datasource_name is not a string, or if no datasource exists with the given name.

        Example:
            >>> datasources = Datasources()
            >>> datasources.delete("SalesData")
            >>> print("Datasource 'SalesData' deleted successfully.")

        #ai-gen-doc
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

    def refresh(self) -> None:
        """Reload all datasource information associated with the Datacube.

        This method refreshes the internal state of the Datasources object, ensuring that
        any changes to the datasources in the Datacube are reflected in the current instance.

        Example:
            >>> datasources = Datasources(datacube_object)
            >>> datasources.refresh()  # Updates the datasources to reflect the latest state

        #ai-gen-doc
        """
        self._datasources = self._get_all_datasources()


class Datasource(object):
    """
    Class for managing and performing operations on a single datasource.

    This class provides a comprehensive interface for interacting with a datasource,
    including lifecycle management, schema operations, data import, content deletion,
    job initiation, status monitoring, and sharing capabilities. It exposes various
    properties for accessing datasource metadata and configuration details.

    Key Features:
        - Initialization with datacube object, datasource name, and ID
        - Access to datasource properties and identifiers
        - Start and monitor jobs related to the datasource
        - Delete datasource and its content
        - Retrieve and update datasource schema
        - Import data into the datasource
        - Refresh datasource state
        - Retrieve crawl history and status information
        - Share datasource with users, specifying permissions and operations
        - Access computed core name, index server cloud ID, and datasource type
        - Manage datasource handlers

    #ai-gen-doc
    """

    def __init__(self, datacube_object: object, datasource_name: str, datasource_id: str = None) -> None:
        """Initialize a Datasource object.

        Args:
            datacube_object: Instance of the Datacube class to which this datasource belongs.
            datasource_name: The name of the datasource.
            datasource_id: Optional; the unique identifier for the datasource. If not provided, it can be set later.

        Example:
            >>> datacube = Datacube()
            >>> datasource = Datasource(datacube, "SalesData")
            >>> # Optionally, provide a datasource ID
            >>> datasource_with_id = Datasource(datacube, "InventoryData", "ds_12345")

        #ai-gen-doc
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

    def __repr__(self) -> str:
        """Return a string representation of the Datasource instance.

        This method provides a developer-friendly string that can be used to 
        inspect the Datasource object, typically for debugging purposes.

        Returns:
            A string representing the Datasource instance.

        Example:
            >>> datasource = Datasource()
            >>> print(repr(datasource))
            <Datasource object at 0x7f8b1c2d3e80>

        #ai-gen-doc
        """
        return 'Datasource class instance for Commcell'

    def _get_datasource_id(self) -> str:
        """Retrieve the unique identifier associated with this datasource.

        Returns:
            The ID of the datasource as a string.

        Example:
            >>> datasource = Datasource()
            >>> datasource_id = datasource._get_datasource_id()
            >>> print(f"Datasource ID: {datasource_id}")

        #ai-gen-doc
        """
        datasources = Datasources(self._datacube_object)
        return datasources.get(self.datasource_name).datasource_id

    def _get_datasource_properties(self) -> dict:
        """Retrieve the properties of this datasource.

        Returns:
            dict: A dictionary containing the properties of the datasource.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> datasource = Datasource()
            >>> properties = datasource._get_datasource_properties()
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2'}

        #ai-gen-doc
        """
        data_source_dict = self._commcell_object.datacube.datasources.get_datasource_properties(self.datasource_name)
        if 'computedCoreName' in data_source_dict:
            self._computed_core_name = data_source_dict['computedCoreName']
        if 'cloudId' in data_source_dict:
            self._cloud_id = data_source_dict['cloudId']
        self._data_source_type = data_source_dict['data_source_type']
        return data_source_dict

    def start_job(self) -> str:
        """Start the crawl job for the datasource.

        Initiates a crawl job associated with this datasource and returns the job ID.

        Returns:
            str: The job ID of the started crawl job.

        Raises:
            Exception: If the job fails to start.

        Example:
            >>> datasource = Datasource()
            >>> job_id = datasource.start_job()
            >>> print(f"Crawl job started with ID: {job_id}")

        #ai-gen-doc
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

    def delete_datasource(self) -> bool:
        """Delete the datasource from the system.

        Returns:
            True if the datasource was successfully deleted.

        Raises:
            Exception: If the deletion operation fails, an exception is raised with an error message.

        Example:
            >>> datasource = Datasource()
            >>> success = datasource.delete_datasource()
            >>> print(f"Datasource deleted: {success}")

        #ai-gen-doc
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

    def get_status(self) -> dict:
        """Retrieve the current status information of the datasource.

        Returns:
            dict: A dictionary containing all status details of the datasource.

        Raises:
            Exception: If the datasource details cannot be found.

        Example:
            >>> datasource = Datasource()
            >>> status_info = datasource.get_status()
            >>> print(status_info)
            >>> # Output will be a dictionary with status information about the datasource

        #ai-gen-doc
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

    def get_crawl_history(self, last_crawl_history: bool = False) -> list:
        """Retrieve the crawling history for this datasource.

        Args:
            last_crawl_history: If True, returns only the status and information about the most recent crawling
                operation for this datasource in Data Cube. If False, returns the complete crawl history.

        Returns:
            list: A list of dictionaries, each containing key-value pairs with details about crawl history for this datasource.
            Each dictionary may include:
                - "numFailed": Number of failed items.
                - "totalcount": Total number of items processed.
                - "endUTCTime": End time of the crawl operation (UTC).
                - "numAccessDenied": Number of access denied errors.
                - "numAdded": Number of items added.
                - "startUTCTime": Start time of the crawl operation (UTC).
                - "state": State of the crawl operation.

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> datasource = Datasource()
            >>> history = datasource.get_crawl_history()
            >>> print(f"Total crawl operations: {len(history)}")
            >>> if history:
            ...     print(f"Most recent crawl state: {history[0]['state']}")

        #ai-gen-doc
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
    def datasource_id(self) -> int:
        """Get the unique identifier of the data source.

        Returns:
            int: The ID value associated with this data source.

        Example:
            >>> datasource = Datasource()
            >>> ds_id = datasource.datasource_id  # Use dot notation for property access
            >>> print(f"Datasource ID: {ds_id}")

        #ai-gen-doc
        """
        return self._datasource_id

    @property
    def properties(self) -> dict:
        """Get all properties associated with the data source.

        Returns:
            dict: A dictionary containing all properties of the data source.

        Example:
            >>> datasource = Datasource()
            >>> props = datasource.properties  # Access properties using dot notation
            >>> print(props)
            {'name': 'DataSource1', 'type': 'SQL', 'status': 'active'}

        #ai-gen-doc
        """
        return self._properties

    @property
    def datasource_name(self) -> str:
        """Get the name of the data source.

        Returns:
            The name of the data source as a string.

        Example:
            >>> ds = Datasource()
            >>> name = ds.datasource_name  # Use dot notation to access the property
            >>> print(f"Datasource name: {name}")

        #ai-gen-doc
        """
        return self._datasource_name

    @property
    def computed_core_name(self) -> str:
        """Get the value of the computed core name attribute for this datasource.

        Returns:
            The computed core name as a string.

        Example:
            >>> datasource = Datasource()
            >>> core_name = datasource.computed_core_name  # Access as a property
            >>> print(f"Computed core name: {core_name}")

        #ai-gen-doc
        """
        return self._computed_core_name

    @property
    def index_server_cloud_id(self) -> int:
        """Get the cloud ID associated with the index server for this datasource.

        Returns:
            int: The cloud ID value of the index server.

        Example:
            >>> datasource = Datasource()
            >>> cloud_id = datasource.index_server_cloud_id
            >>> print(f"Index server cloud ID: {cloud_id}")

        #ai-gen-doc
        """
        return self._cloud_id

    @property
    def data_source_type(self) -> str:
        """Get the type of the data source.

        Returns:
            The data source type as a string.

        Example:
            >>> ds = Datasource()
            >>> ds_type = ds.data_source_type  # Use dot notation for property access
            >>> print(f"Datasource type: {ds_type}")

        #ai-gen-doc
        """
        return self._data_source_type

    def get_datasource_schema(self) -> dict:
        """Retrieve information about the schema of the data source.

        Returns:
            dict: A dictionary containing all schema fields of this data source, grouped under
            'dynSchemaFields' and 'schemaFields'. The dictionary structure is as follows:

                {
                    "uniqueKey": "contentid",
                    "schemaFields": [ {field properties}, ... ],
                    "dynSchemaFields": [ {field properties}, ... ]
                }

            - 'uniqueKey': The primary key field for the data source.
            - 'schemaFields': List of dictionaries, each representing a static schema field.
            - 'dynSchemaFields': List of dictionaries, each representing a dynamic schema field.

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> datasource = Datasource()
            >>> schema_info = datasource.get_datasource_schema()
            >>> print(schema_info["uniqueKey"])
            >>> print("Number of static fields:", len(schema_info["schemaFields"]))
            >>> print("Number of dynamic fields:", len(schema_info["dynSchemaFields"]))

        #ai-gen-doc
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

    def update_datasource_schema(self, schema: list[dict[str, str]]) -> None:
        """Update the schema of the data source.

        This method updates the schema definition for the data source using the provided list of field property dictionaries.
        Each dictionary should represent a field and its properties, such as field name, type, and indexing options.

        Args:
            schema: A list of dictionaries, where each dictionary defines the properties of a schema field.
                Example field dictionary:
                    {
                        "fieldName": "username",
                        "indexed": "1",
                        "autocomplete": "0",
                        "type": "string",
                        "searchDefault": "1",
                        "multiValued": "0"
                    }
                Valid values for "type" are: "string", "int", "float", "long", "double", "date", "longstring".
                The values for "indexed", "autocomplete", "searchDefault", and "multiValued" should be "0" or "1" as strings.

        Raises:
            SDKException: If the response is empty, if the schema argument is not a list, or if the response indicates failure.

        Example:
            >>> schema = [
            ...     {
            ...         "fieldName": "email",
            ...         "indexed": "1",
            ...         "autocomplete": "1",
            ...         "type": "string",
            ...         "searchDefault": "0",
            ...         "multiValued": "0"
            ...     }
            ... ]
            >>> datasource.update_datasource_schema(schema)
            >>> print("Datasource schema updated successfully.")

        #ai-gen-doc
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

    def import_data(self, data: list) -> None:
        """Import or pump the given data into the data source for indexing.

        Args:
            data: A list of key-value pairs representing the data to be indexed and pumped into Solr.

        Raises:
            SDKException: If the response from the data source is empty or not successful.

        Example:
            >>> datasource = Datasource()
            >>> sample_data = [
            ...     {"id": 1, "name": "Document1"},
            ...     {"id": 2, "name": "Document2"}
            ... ]
            >>> datasource.import_data(sample_data)
            >>> print("Data imported successfully.")

        #ai-gen-doc
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

    def delete_content(self) -> None:
        """Delete the content of the data source from Data Cube.

        This method removes all content associated with the data source, but does not delete the data source itself.

        Raises:
            SDKException: If the response from the Data Cube API is empty or indicates a failure.

        Example:
            >>> datasource = Datasource()
            >>> datasource.delete_content()
            >>> print("Datasource content deleted successfully")
            # The data source object remains, but its content is removed.

        #ai-gen-doc
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

    def refresh(self) -> None:
        """Reload the properties of the Datasource object.

        This method updates the Datasource instance with the latest information from the underlying data source.
        Use this method to ensure that the object's properties reflect the current state.

        Example:
            >>> datasource = Datasource()
            >>> datasource.refresh()
            >>> print("Datasource properties refreshed successfully")

        #ai-gen-doc
        """
        self._properties = self._get_datasource_properties()
        self.handlers = Handlers(self)

    @property
    def ds_handlers(self) -> 'Handlers':
        """Get the Handlers instance associated with this Datasource.

        Returns:
            Handlers: An instance of the Handlers class for managing datasource handlers.

        Example:
            >>> datasource = Datasource()
            >>> handlers = datasource.ds_handlers  # Access the Handlers instance via property
            >>> print(f"Handlers object: {handlers}")

        #ai-gen-doc
        """
        try:
            if self._handlers_obj is None:
                self._handlers_obj = Handlers(self)
            return self._handlers_obj
        except BaseException:
            raise SDKException('Datacube', '102', "Failed to init Handlers")

    def share(self, permission_list: list, operation_type: int, user_id: int, user_name: str, user_type: int) -> None:
        """Share the datasource with a specified user or user group.

        This method assigns or removes permissions for a user or user group on the datasource,
        based on the provided operation type and permission list.

        Args:
            permission_list: List of permissions to assign or remove for the user/user group.
            operation_type: The type of operation to perform (2 for add, 3 for delete).
            user_id: The unique identifier of the user or user group to share with.
            user_name: The name of the user or user group to share with.
            user_type: The type of user (e.g., 13 for User).

        Raises:
            SDKException: If the response is empty, not successful, or if sharing the datasource fails.

        Example:
            >>> datasource = Datasource()
            >>> permissions = ['read', 'write']
            >>> datasource.share(permissions, 2, 101, 'jdoe', 13)
            >>> print("Datasource shared successfully with user jdoe.")

        #ai-gen-doc
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
