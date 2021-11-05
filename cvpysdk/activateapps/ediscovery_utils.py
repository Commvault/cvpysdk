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

"""Main file for performing operations on ediscovery clients & ediscovery data sources.

'EdiscoveryClients','EdiscoveryClientOperations' ,'EdiscoveryDataSources' , 'EdiscoveryDataSource' are the 4 classes defined in this file

EdiscoveryClients:  Class for getting ediscovery clients details for different apps in activate

EdiscoveryClientOperations : Class for performing operations on Ediscovery client

EdiscoveryDataSources:  Class to represent all datasources associated with ediscovery client

EdiscoveryDataSource:   Class to represent single data source associated with edisocvery client

EdiscoveryClients:

    __init__()                          --  initialise object of the EdiscoveryClients class

    _response_not_success()             --  parses through the exception response, and raises SDKException

    get_ediscovery_clients()            --  returns the ediscovery clients details

    get_ediscovery_client_group_details() -  returns the ediscovery client group details

EdiscoveryClientOperations:

    __init__()                          --  initialise object of the EdiscoveryClientOperations class

    _response_not_success()             --  parses through the exception response, and raises SDKException

    _get_associations()                 --  returns the associations blob for this client

    _do_stream_download()               --  does stream download of exported csv file to local machine

    form_search_params()                --  returns the search params dict for searching/exporting

    refresh()                           --  refresh the ediscovery client properties

    share()                             --  shares client with given user name or group name

    export()                            --  do export to CSV on data

    start_job()                         --  starts collection job on ediscovery client

    get_job_status()                    --  returns the job status of ediscovery client job

    get_job_history()                   --  returns the job history details of this ediscovery client

    wait_for_collection_job()           --  waits for collection job to finish

    wait_for_export()                   --  waits for export to csv operation to finish

    get_ediscovery_client_details()     --  returns the ediscovery client details

    search()                            --  returns the search response containing document details

    get_handler_id()                    --  returns the handler id for this Ediscovery client

    schedule()                          --  Creates or modifies the schedule associated with ediscovery client

EdiscoveryClientOperations Attributes:
--------------------------------------

    **associations**            --  returns the blob of associated entities for this client


EdiscoveryDataSources:

    __init__()                              --  initialise object of the EdiscoveryDataSources class

    _response_not_success()                 --  parses through the exception response, and raises SDKException

    _get_data_sources_details()             --  returns the data sources details associated with ediscovery client

    _get_data_source_names()                --  returns separate list of data source display names & data source names
                                                    associated with client

    _parse_client_response_for_data_source  --  returns list of values for field names for data sources
                                                                                from client response

    _get_data_source_properties()           --  parses client response and returns deta sources properties

    has_data_source()                       --  checks whether given data source exists in this client or not

    get()                                   --  returns the EdiscoveryDataSource class object for given data source name

    delete()                                --  deletes the given data source associated with client

    add_fs_data_source()                    --  adds file system data source

    refresh()                               --  refresh the data sources details associated with client

EdiscoveryDataSources Attributes:
----------------------------------

    **data_sources**            --  returns the list of data sources names associated with this client

    **ediscovery_client_props** --  returns the Ediscovery client properties response for associated client

    **total_documents**         --  returns the total documents count from all data sources

    **client_id**               --  returns associated client id for all these data sources

    **client_targetapp**        --  returns the source details of client (FSO/SDG)

EdiscoveryDataSource:

    __init__()                              --  initialise object of the EdiscoveryDataSource class

    _response_not_success()                 --  parses through the exception response, and raises SDKException

    _get_data_source_properties()           --  returns the properties of data source

    _get_property_value()                   --  returns the value for the property name

    _form_files_list()                      --  returns list of dict containing files details

    _form_request_options()                 --  returns the options for review request

    refresh()                               --  refresh the datasource properties

    get_job_history()                       --  returns the job history for this data source

    get_active_jobs()                       --  returns the active jobs for this data source

    search()                                --  returns the search response containing document details

    export()                                --  do export to CSV on data

    wait_for_export()                       --  waits for export to csv operation to finish

    tag_items()                             --  applies tag to the documents

    review_action()                         --  do review action for documents

EdiscoveryDataSource Attributes:
---------------------------------

    **crawl_type_name**         --  returns the crawl type enum name for this data source

    **crawl_type**              --  returns the crawl type for this data source

    **core_id**                 --  returns the data source core id attribute

    **computed_core_name**      --  returns the computed core name of this datasource

    **core_name**               --  returns the core name attribute of this data source

    **cloud_id**                --  returns the index server cloud id associated with this data source

    **data_source_props**       --  returns dict containing data source properties

    **data_source_id**          --  returns the id of data source

    **data_source_type**        --  returns the type of data source

    **data_source_name**        --  returns the name of data source

    **plan_id**                 --  returns the associated DC plan id

    **data_source_type_id**     --  returns the data source type id value

"""
import copy
import time
import json
import os

from ..activateapps.entity_manager import EntityManagerTypes

from ..activateapps.constants import InventoryConstants, EdiscoveryConstants, TargetApps
from ..exception import SDKException


class EdiscoveryClients():
    """Class for getting ediscovery clients details for different apps in activate"""

    def __init__(self, commcell_object, class_object):
        """Initializes an instance of the EdiscoveryClients class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                class_object        (object)    -- instance of FsoServers/FsoServerGroups/FsoServerGroup class

            Returns:
                object  -   instance of the EdiscoveryClients class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._class_obj = class_object
        self._ds_type = None
        self._client_group = None
        self._limit = None
        self._offset = None
        self._sort_by = None
        self._sort_dir = None
        self._client_group_filter = None
        self._include_doc = None
        self._API_GET_EDISCOVERY_CLIENTS = copy.deepcopy(self._services['EDISCOVERY_V2_GET_CLIENTS'])
        self._API_GET_EDISCOVERY_CLIENT_GROUPS = self._services['EDISCOVERY_V2_GET_CLIENT_GROUP_DETAILS']

        from .file_storage_optimization import FsoServers, FsoServerGroups, FsoServerGroup

        if isinstance(class_object, FsoServers):
            self._ds_type = 5
            self._client_group = 0
            self._limit = 0
            self._offset = 0
            self._sort_by = 1
            self._sort_dir = 0
        elif isinstance(class_object, FsoServerGroups):
            self._ds_type = 5
            self._client_group = 1
            self._limit = 0
            self._offset = 0
            self._sort_by = 1
            self._sort_dir = 0
        elif isinstance(class_object, FsoServerGroup):
            self._ds_type = 5
            self._client_group = 0
            self._client_group_filter = class_object.server_group_id
            self._limit = 0
            self._offset = 0
            self._sort_by = 1
            self._sort_dir = 0
            self._include_doc = 1
        else:
            raise SDKException('EdiscoveryClients', '102', 'Not a supported caller for this class')

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def get_ediscovery_client_group_details(self):
        """returns the ediscovery client group details for the app

                Args:

                    None

                Returns:

                    dict        -- Containing client group details

                Raises;

                    SDKException:

                            if failed to get client group details

                            if response is empty

                            if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_GET_EDISCOVERY_CLIENT_GROUPS %
            (self._client_group_filter, self._include_doc))
        if flag:
            if response.json() and 'nodeList' in response.json():
                return response.json()
            raise SDKException('EdiscoveryClients', '106')
        self._response_not_success(response)

    def get_ediscovery_clients(self):
        """returns the ediscovery clients details for the app

                Args:

                    None

                Returns:

                    dict        -- Containing client details

                Raises;

                    SDKException:

                            if failed to get client details

                            if response is empty

                            if response is not success

        """
        api = self._API_GET_EDISCOVERY_CLIENTS % (
            self._ds_type, self._client_group, self._limit, self._offset, self._sort_by, self._sort_dir)
        if self._client_group_filter:
            api = api + f"&clientGroupFilter={self._client_group_filter}"
        flag, response = self._cvpysdk_object.make_request('GET', api)
        output = {}
        if flag:
            if response.json() and 'nodeList' in response.json():
                for node in response.json()['nodeList']:
                    if 'clientEntity' in node:
                        output[node['clientEntity'].get('displayName', 'NA').lower()] = node
                return output
            raise SDKException('EdiscoveryClients', '106')
        self._response_not_success(response)


class EdiscoveryClientOperations():
    """Class for performing operations on ediscovery client."""

    def __init__(self, commcell_object, class_object):
        """Initializes an instance of the EdiscoveryClientOperations class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                class_object        (object)    -- instance of Inventory/Asset/FsoServer
                                                        /EdiscoveryDataSource/EdiscoveryDataSources/FsoServerGroup class

            Returns:
                object  -   instance of the EdiscoveryClientOperations class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._class_obj = class_object
        self._type = None
        self._operation = None
        self._client_id = None
        self._data_source_id = None
        self._ds_type_names = None
        self._include_doc_count = None
        self._limit = None
        self._offset = None
        self._sort_by = None
        self._sort_dir = None
        self._app_type = None
        self._associations = None
        self._search_entity_type = None
        self._search_entity_id = None
        self._client_entity_type = 3
        self._API_CRAWL = self._services['EDISCOVERY_CRAWL']
        self._API_JOBS_HISTORY = self._services['EDISCOVERY_JOBS_HISTORY']
        self._API_JOB_STATUS = self._services['EDISCOVERY_JOB_STATUS']
        self._API_CLIENT_DETAILS = self._services['EDISCOVERY_V2_GET_CLIENT_DETAILS']
        self._API_SECURITY_ENTITY = self._services['ENTITY_SECURITY_ASSOCIATION']
        self._API_SECURITY = self._services['EDISCOVERY_SECURITY_ASSOCIATION']
        self._API_SEARCH = self._services['EDISCOVERY_DYNAMIC_FEDERATED']
        self._API_GET_DEFAULT_HANDLER = self._services['EDISCOVERY_GET_DEFAULT_HANDLER']
        self._API_EXPORT = self._services['EDISCOVERY_EXPORT']
        self._API_EXPORT_STATUS = self._services['EDISCOVERY_EXPORT_STATUS']
        self._CREATE_POLICY = self._services['CREATE_UPDATE_SCHEDULE_POLICY']
        from .inventory_manager import Inventory, Asset
        from .file_storage_optimization import FsoServer, FsoServerGroup

        if isinstance(class_object, Inventory):
            self._type = 0  # Inventory
            self._operation = 0
            self._client_id = class_object.inventory_id
            self._data_source_id = 0
        elif isinstance(class_object, Asset):
            self._type = 0  # Inventory
            self._operation = 0
            self._client_id = class_object.inventory_id
            self._data_source_id = class_object.asset_id
        elif isinstance(class_object, FsoServer):
            self._client_id = class_object.server_id
            self._include_doc_count = 1
            self._limit = self._offset = 0
            self._sort_by = 2
            self._sort_dir = 0
            self._ds_type_names = f"{EdiscoveryConstants.DS_FILE},{EdiscoveryConstants.DS_CLOUD_STORAGE}"
            self._data_source_id = 0  # invoke on all data sources
            self._type = 1  # Client
            self._operation = 0
            self._app_type = 1
            self._search_entity_type = 3
            self._search_entity_id = self._client_id
        elif isinstance(class_object, EdiscoveryDatasource):
            self._search_entity_type = 132
            self._search_entity_id = class_object.data_source_id
            self._data_source_id = class_object.data_source_id
        elif isinstance(class_object, EdiscoveryDataSources):
            self._client_id = class_object.client_id
            self._include_doc_count = 1
            self._limit = self._offset = 0
            self._sort_by = 2
            self._sort_dir = 0
            if class_object.client_targetapp == TargetApps.FSO.value:
                # based on caller, set appropriate ds types supported for that
                self._ds_type_names = f"{EdiscoveryConstants.DS_FILE},{EdiscoveryConstants.DS_CLOUD_STORAGE}"
        elif isinstance(class_object, FsoServerGroup):
            self._search_entity_type = 28
            self._search_entity_id = class_object.server_group_id
        else:
            raise SDKException('EdiscoveryClients', '101')
        self.refresh()

    def refresh(self):
        """refresh ediscovery client properties"""
        self._associations = self._get_associations()

    def schedule(self, schedule_name, pattern_json, ops_type=2):
        """Creates or modifies the schedule associated with ediscovery client

                Args:

                    schedule_name       (str)       --  Schedule name

                    pattern_json        (dict)      --  Schedule pattern dict (Refer to Create_schedule_pattern in schedule.py)

                    ops_type            (int)       --  Operation type

                                                            Default : 2 (Add)

                                                            Supported : 2 (Add/Modify)

                Raises:

                      SDKException:

                            if input is not valid

                            if failed to create/modify schedule

        """
        if not isinstance(schedule_name, str) or not isinstance(pattern_json, dict):
            raise SDKException('EdiscoveryClients', '101')
        if ops_type not in [2]:
            raise SDKException('EdiscoveryClients', '102', "Schedule operation type provided is not supported")
        request_json = copy.deepcopy(EdiscoveryConstants.SERVER_LEVEL_SCHEDULE_JSON)
        request_json['taskInfo']['associations'][0]['clientId'] = int(self._client_id)
        request_json['taskInfo']['task'][
            'taskName'] = f"Cvpysdk created Schedule for Server id - {self._client_id}"
        request_json['taskInfo']['subTasks'][0]['subTask'][
            'subTaskName'] = schedule_name
        request_json['taskInfo']['subTasks'][0]['pattern'] = pattern_json
        request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['contentIndexingOption']['operationType'] = ops_type

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_POLICY, request_json
        )
        if flag:
            if response.json():
                if "taskId" in response.json():
                    task_id = str(response.json()["taskId"])
                    if task_id:
                        return

                elif "errorCode" in response.json():
                    error_code = str(response.json()['errorCode'])
                    error_message = response.json()['errorMessage']

                    if error_code == "0":
                        return
                    else:
                        raise SDKException(
                            'EdiscoveryClients',
                            '102',
                            f"Schedule operation failed on server - {error_code} - {error_message}")
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def form_search_params(self, criteria=None, attr_list=None, params=None, query="*:*", key="key"):
        """returns the search params dict based on input

            Args:

                criteria        (str)      --  containing criteria for query

                                                    Example :

                                                        Size:[10 TO 1024]
                                                        FileName:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                params          (dict)     --  Any other params which needs to be passed
                                                   Example : { "start" : "0" }

                query           (str)      --   query to be performed (acts as q param in query)
                                                    default:None (Means *:*)

                key             (str)      --   key name to be used in request (default:key)

            Returns:

                dict        --  Containing searchparams details

                Example : {
                              "searchParams": [
                                {
                                  "key": "wt",
                                  "value": "json"
                                },
                                {
                                  "key": "defType",
                                  "value": "edismax"
                                },
                                {
                                  "key": "q",
                                  "value": "*:*"
                                },
                                {
                                  "key": "fq",
                                  "value": "(contentid:949c3b53ce4dd72a82b8e67039eeddef)"
                                },
                                {
                                  "key": "fl",
                                  "value": "contentid,CreatedTime,Url,ClientId"
                                }
                              ]
                            }
        """
        search_params = copy.deepcopy(EdiscoveryConstants.DYNAMIC_FEDERATED_SEARCH_PARAMS)
        search_params['searchParams'].append(
            {key: "wt", "value": "json"})
        search_params['searchParams'].append(
            {key: "defType", "value": "edismax"})
        search_params['searchParams'].append({key: "q", "value": query})
        if criteria:
            fq_dict = {
                key: "fq",
                "value": criteria
            }
            search_params['searchParams'].append(fq_dict)
        if attr_list:
            fl_list = ','.join(attr_list)
            fl_dict = {
                key: "fl",
                "value": fl_list
            }
            search_params['searchParams'].append(fl_dict)
        if params:
            for dkey, value in params.items():
                custom_dict = {
                    key: str(dkey),
                    "value": str(value)
                }
                search_params['searchParams'].append(custom_dict)
        return search_params

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _do_stream_download(self, guid, file_name, download_location):
        """does stream download to file to local machine

                Args:

                    guid                (str)       --  Download GUID

                    download_location   (str)       --  path on local machine to download requested file

                    file_name           (str)       --  File name for download

                Returns:

                    Str     --  File path containing downloaded file

                Raise:

                    SDKException:

                        if failed to do stream download


        """
        request = copy.deepcopy(EdiscoveryConstants.EXPORT_DOWNLOAD_REQ)
        request['responseFileName'] = file_name
        for param in request['fileParams']:
            if param['id'] == 2:
                param['name'] = guid
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['DOWNLOAD_PACKAGE'], request
        )

        if flag:
            error_list = response.json().get('errList')
            file_content = response.json().get('fileContent', {})

            if error_list:
                raise SDKException('EdiscoveryClients', '102', 'Error: {0}'.format(error_list))

            file_name = file_content.get('fileName', file_name)
            request_id = file_content['requestId']

            # full path of the file on local machine to be downloaded
            download_path = os.path.join(download_location, file_name)

            # execute request to get the stream of content
            # using request id returned in the previous response
            request['requestId'] = request_id
            flag1, response1 = self._cvpysdk_object.make_request(
                'POST',
                self._services['DOWNLOAD_VIA_STREAM'],
                request,
                stream=True
            )

            # download chunks of 1MB each
            chunk_size = 1024 ** 2

            if flag1:
                with open(download_path, "wb") as file_pointer:
                    for content in response1.iter_content(chunk_size=chunk_size):
                        file_pointer.write(content)
            else:
                self._response_not_success(response1)
        else:
            self._response_not_success(response)

        return download_path

    def get_handler_id(self, handler_name="default"):
        """returns the id of given handler name

                Args:

                    handler_name            (str)       --  Handler name(Default: default)

                Returns:

                    int --  Handler id

                Raises:

                    SDKException:

                        if failed to find handler

                        if response is empty

        """
        if not isinstance(self._class_obj, EdiscoveryDatasource):
            return 0
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_GET_DEFAULT_HANDLER % self._data_source_id)
        if flag:
            if response.json() and 'handlerInfos' in response.json():
                handler_list = response.json()['handlerInfos']
                if not isinstance(handler_list, list):
                    raise SDKException('EdiscoveryClients', '102', "Failed to get Datasource/Handler details")
                for handler in handler_list:
                    if handler['handlerName'].lower() == handler_name.lower():
                        return handler['handlerId']
                else:
                    raise SDKException('EdiscoveryClients', '102', 'No Handler found with given name')
            raise SDKException('EdiscoveryClients', '102', 'Unknown response while fetching datasource details')
        self._response_not_success(response)

    def export(self, criteria=None, attr_list=None, params=None):
        """do export to CSV on data

            Args:

                criteria        (str)      --  containing criteria for query
                                                    (Default : None - Exports all docs)

                                                    Example :

                                                        1) Size filter --> Size:[10 TO 1024]
                                                        2) File name filter --> FileName_idx:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                params          (dict)     --  Any other params which needs to be passed
                                                   Example : { "start" : "0" }

            Returns:

                str     --  export operation token


            Raises:

                SDKException:

                        if failed to perform export

        """
        if criteria and not isinstance(criteria, str):
            raise SDKException('EdiscoveryClients', '101')
        search_params = self.form_search_params(criteria=criteria, attr_list=attr_list,
                                                params=params)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_EXPORT % self.get_handler_id(), search_params
        )
        if flag:
            if response.json():
                response = response.json()
                if 'errorCode' in response and response['errorCode'] != 0:
                    raise SDKException(
                        'EdiscoveryClients',
                        '102',
                        f"Export failed with error : {response.get('errLogMessage','')}")
                elif 'customMap' in response and 'name' in response['customMap']:
                    return response['customMap']['name']
                raise SDKException('EdiscoveryClients', '102', f"Failed to search with response - {response.json()}")
            raise SDKException('EdiscoveryClients', '113')
        self._response_not_success(response)

    def search(self, criteria=None, attr_list=None, params=None):
        """do searches on data source and returns document details

            Args:

                criteria        (str)      --  containing criteria for query
                                                    (Default : None - returns all docs)

                                                    Example :

                                                        1) Size filter --> Size:[10 TO 1024]
                                                        2) File name filter --> FileName_idx:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                params          (dict)     --  Any other params which needs to be passed
                                                   Example : { "start" : "0" }

            Returns:

                list(dict),dict    --  Containing document details & facet details(if any)


            Raises:

                SDKException:

                        if failed to perform search

        """
        if criteria and not isinstance(criteria, str):
            raise SDKException('EdiscoveryClients', '101')
        search_params = self.form_search_params(criteria=criteria, attr_list=attr_list,
                                                params=params)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_SEARCH % (self._search_entity_type, self._search_entity_id), search_params
        )
        if flag:
            if response.json():
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    raise SDKException(
                        'EdiscoveryClients',
                        '102',
                        f"Failed to perform search - {response.json().get('errLogMessage','')}")
                if 'response' in response.json() and 'docs' in response.json()['response']:
                    if 'facets' not in response.json():
                        return response.json()['response']['docs'], {}
                    return response.json()['response']['docs'], response.json()['facets']
                raise SDKException('EdiscoveryClients', '102', f"Failed to search with response - {response.json()}")
            raise SDKException('EdiscoveryClients', '112')
        self._response_not_success(response)

    def _get_associations(self):
        """returns the associations for this client

            Args:

                None

            Returns:

                Dict    --  Containing associations details

            Raises:

                SDKException:

                    if failed to find association details

        """
        # if called from EdiscoveryDatasource, then no association check needed as sharing is not possible at this level
        from ..activateapps.file_storage_optimization import FsoServerGroup
        if isinstance(self._class_obj, EdiscoveryDatasource) or isinstance(self._class_obj, FsoServerGroup):
            return {}
        association_request_json = copy.deepcopy(EdiscoveryConstants.SHARE_REQUEST_JSON)
        del association_request_json['securityAssociations']
        association_request_json['entityAssociated']['entity'][0]['clientId'] = int(self._client_id)
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_SECURITY_ENTITY %
            (self._client_entity_type, int(
                self._client_id)), association_request_json)
        if flag:
            if response.json() and 'securityAssociations' in response.json():
                security = response.json()['securityAssociations'][0]['securityAssociations']
                return security.get('associations', {})
            else:
                raise SDKException('EdiscoveryClients', '102', 'Failed to get existing security associations')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def share(self, user_or_group_name, allow_edit_permission=False, is_user=True, ops_type=1):
        """Shares ediscovery client with given user or user group in commcell

                Args:

                    user_or_group_name      (str)       --  Name of user or group

                    is_user                 (bool)      --  Denotes whether this is user or group name
                                                                default : True(User)

                    allow_edit_permission   (bool)      --  whether to give edit permission or not to user or group

                    ops_type                (int)       --  Operation type

                                                            Default : 1 (Add)

                                                            Supported : 1 (Add)
                                                                        3 (Delete)

                Returns:

                    None

                Raises:

                    SDKException:

                            if unable to update security associations

                            if response is empty or not success
        """
        if not isinstance(user_or_group_name, str):
            raise SDKException('EdiscoveryClients', '101')
        request_json = copy.deepcopy(EdiscoveryConstants.SHARE_REQUEST_JSON)
        external_user = False
        association_response = None
        if ops_type == 1:
            association_response = self._associations

        if '\\' in user_or_group_name:
            external_user = True
        if is_user:
            user_obj = self._commcell_object.users.get(user_or_group_name)
            user_id = user_obj.user_id
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userId'] = int(user_id)
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = "13"
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userName'] = user_or_group_name
        elif external_user:
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['groupId'] = 0
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = "62"
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0][
                'externalGroupName'] = user_or_group_name
        else:
            grp_obj = self._commcell_object.user_groups.get(user_or_group_name)
            grp_id = grp_obj.user_group_id
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userGroupId'] = int(grp_id)
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = "15"
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0][
                'userGroupName'] = user_or_group_name

        request_json['entityAssociated']['entity'][0]['clientId'] = self._client_id
        request_json['securityAssociations']['associationsOperationType'] = ops_type

        if allow_edit_permission:
            # we need to send separate association for each permission
            association_json = copy.deepcopy(request_json['securityAssociations']['associations'][0])
            # do copy, remove permission and add Edit
            del association_json['properties']['categoryPermission']['categoriesPermissionList'][0]
            association_json['properties']['categoryPermission']['categoriesPermissionList'].append(
                EdiscoveryConstants.EDIT_CATEGORY_PERMISSION)
            request_json['securityAssociations']['associations'].append(association_json)

            # Associate existing associations to the request
        if ops_type == 1:
            request_json['securityAssociations']['associations'].extend(association_response)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_SECURITY % self._app_type, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                response_json = response.json()['response']
                for node in response_json:
                    if 'errorCode' in node:
                        error_code = node['errorCode']
                        if error_code != 0:
                            error_message = node.get('warningMessage', "Something went wrong")
                            raise SDKException(
                                'EdiscoveryClients',
                                '102', error_message)
                self.refresh()
            else:
                raise SDKException('EdiscoveryClients', '109')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_ediscovery_client_details(self):
        """returns the ediscovery client details for this client

                Args:

                    None

                Returns:

                    dict        -- Containing client details

                Raises;

                    SDKException:

                            if failed to get client details

                            if response is empty

                            if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_CLIENT_DETAILS % (
            self._client_id, self._include_doc_count, self._limit, self._offset,
            self._sort_by, self._sort_dir, self._ds_type_names))
        if flag:
            if response.json() and 'nodeList' in response.json():
                return response.json()['nodeList'][0]
            raise SDKException('EdiscoveryClients', '106')
        self._response_not_success(response)

    def start_job(self, wait_for_job=False, wait_time=60):
        """Starts job on ediscovery client

            Args:

                    wait_for_job        (bool)       --  specifies whether to wait for job to complete or not

                    wait_time           (int)        --  time interval to wait for job completion in Mins
                                                            Default : 60Mins

             Return:

                    None

            Raises:

                    SDKException:

                            if failed to start collection job

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_CRAWL % (self._client_id, self._data_source_id, self._type, self._operation)
        )
        if flag:
            if response.json():
                response_json = response.json()
                if 'errorCode' in response_json:
                    error_code = response_json['errorCode']
                    if error_code != 0:
                        error_message = response_json['errorMessage']
                        raise SDKException(
                            'EdiscoveryClients',
                            '102', error_message)
                raise SDKException('EdiscoveryClients', '103')
            if not wait_for_job:
                return
            return self.wait_for_collection_job(wait_time=wait_time)
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def wait_for_export(self, token, wait_time=60, download=True, download_location=os.getcwd()):
        """Waits for Export to CSV to finish

                Args:

                    wait_time           (int)       --  time interval to wait for job completion in Mins
                                                            Default : 60Mins

                    token               (str)       --  Export to CSV token GUID

                    download_location   (str)       --  Path where to download exported csv file
                                                                Default: Current working dir

                Return:

                    str     -- Download GUID for exported CSV file if download=false
                               File path containing exported csv file if download=true

                Raises:

                    SDKException:

                            if Export status check fails

                            if timeout happens

        """
        timeout = time.time() + 60 * wait_time  # 1hr
        handler_id = self.get_handler_id()
        while True:
            if time.time() > timeout:
                raise SDKException('EdiscoveryClients', '102', "Export job Timeout")
            flag, response = self._cvpysdk_object.make_request(
                'GET', self._API_EXPORT_STATUS % (handler_id, token)
            )
            if flag:
                if response.json():
                    response = response.json()
                    if 'errorCode' in response and response['errorCode'] != 0:
                        raise SDKException(
                            'EdiscoveryClients',
                            '102',
                            f"Export status check failed with error : {response.get('errLogMessage', '')}")
                    elif 'customMap' in response and response['customMap'].get('name', '') == 'statusObject':
                        value_json = json.loads(response['customMap']['value'])
                        if 'response' in value_json and isinstance(
                                value_json['response'],
                                dict) and value_json['response'].get(
                                'status',
                                '') == 'finished':
                            if not download:
                                return value_json['response'].get('downloadGuid', '')
                            else:
                                return self._do_stream_download(guid=value_json['response'].get('downloadGuid', ''),
                                                                file_name=f"Cvpysdk_Activate_export_{time.time()}",
                                                                download_location=download_location)
                    else:
                        raise SDKException('EdiscoveryClients', '102',
                                           f"Failed to check export status with response - {response.json()}")
                else:
                    raise SDKException('EdiscoveryClients', '114')
            else:
                self._response_not_success(response)
            time.sleep(10)

    def wait_for_collection_job(self, wait_time=60):
        """Waits for collection job to finish

                Args:

                    wait_time           (int)       --  time interval to wait for job completion in Mins
                                                            Default : 60Mins

                Return:

                    None

                Raises:

                    SDKException:

                            if collection job fails

                            if timeout happens

        """
        timeout = time.time() + 60 * wait_time  # 1hr
        while True:
            if time.time() > timeout:
                raise SDKException('EdiscoveryClients', '102', "Collection job Timeout")
            status = self.get_job_status()
            if int(status['state']) == InventoryConstants.CRAWL_JOB_COMPLETE_STATE:  # Finished State
                return
            elif int(status['state']) == InventoryConstants.CRAWL_JOB_COMPLETE_ERROR_STATE:  # completed with error
                raise SDKException('EdiscoveryClients', '102', "Job status is marked as Completed with Error")
            # STOPPING,STOPPED,ABORTING, ABORTED,EXCEPTION,UNKNOWN,SYNCING,PENDING
            elif int(status['state']) in InventoryConstants.CRAWL_JOB_FAILED_STATE:
                raise SDKException('EdiscoveryClients', '102', "Job status is marked as Failed/Error/Pending")
            else:
                time.sleep(10)

    def get_job_history(self):
        """Returns the job history details of ediscovery client

                Args:
                    None

                Returns:

                    list(dict)    --  containing job history details

                Raises:

                    SDKException:

                            if failed to get job history

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_JOBS_HISTORY % (self._client_id, self._type, self._data_source_id)
        )
        if flag:
            if response.json() and 'status' in response.json():
                return response.json()['status']
            elif 'error' in response.json():
                error = response.json()['error']
                error_code = error['errorCode']
                if error_code != 0:
                    error_message = error['errLogMessage']
                    raise SDKException(
                        'EdiscoveryClients',
                        '102', error_message)
                raise SDKException('EdiscoveryClients', '102', "Something went wrong while fetching job history")
            else:
                raise SDKException('EdiscoveryClients', '104')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_job_status(self):
        """Returns the job status details of this asset

                Args:
                    None

                Returns:

                    dict    --  containing job status details

                Raises:

                    SDKException:

                            if failed to get job status

        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_JOB_STATUS % (self._client_id, self._type, self._data_source_id)
        )
        if flag:
            if response.json() and 'status' in response.json():
                return response.json()['status']
            elif 'error' in response.json():
                error = response.json()['error']
                error_code = error['errorCode']
                if error_code != 0:
                    error_message = error['errLogMessage']
                    raise SDKException(
                        'EdiscoveryClients',
                        '102', error_message)
                raise SDKException('EdiscoveryClients', '102', "Something went wrong while fetching job status")
            else:
                raise SDKException('EdiscoveryClients', '105')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def associations(self):
        """returns association blob for this client

            Returns:

                dict --  containing security association blob details

        """
        return self._associations


class EdiscoveryDataSources():
    """Class to represent all datasources associated with ediscovery client"""

    def __init__(self, commcell_object, class_object):
        """Initializes an instance of the EdiscoveryDataSources class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                class_object        (object)    -- instance of FsoServer/FsoServers/FsoServerGroups class

            Returns:
                object  -   instance of the EdiscoveryDataSources class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._class_obj = class_object
        self._ediscovery_client_ops = None
        self._client_id = None
        self._ediscovery_client_props = None
        self._data_source_display_names = None
        self._data_source_names = None
        self._data_sources = None
        self._app_source = None
        self._app_source_sub_type = None
        self._API_DELETE = self._services['EDISCOVERY_DATA_SOURCE_DELETE']
        self._API_CREATE_DATA_SOURCE = self._services['EDISCOVERY_CREATE_DATA_SOURCE']

        from .file_storage_optimization import FsoServer, FsoServers, FsoServerGroups

        if isinstance(class_object, FsoServer):
            self._client_id = class_object.server_id
            self._ediscovery_client_ops = EdiscoveryClientOperations(commcell_object, class_object)
            self._app_source = TargetApps.FSO
        elif isinstance(class_object, FsoServers):
            self._app_source = TargetApps.FSO
            self._app_source_sub_type = EdiscoveryConstants.FSO_SERVERS
        elif isinstance(class_object, FsoServerGroups):
            self._app_source = TargetApps.FSO
            self._app_source_sub_type = EdiscoveryConstants.FSO_SERVER_GROUPS
        else:
            raise SDKException('EdiscoveryClients', '101')

        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_data_source_properties(self, client_details):
        """Parses client response and returns data sources properties

                Args:

                    client_details      (dict)      --  containing EdiscoveryClient details response

                Returns:

                    list        --  containing data source details

                Raises:

                    SDKException:

                            if input is not valid


        """
        output = {}
        if not isinstance(client_details, dict):
            raise SDKException('EdiscoveryClients', '107')
        index = 0
        ds_name = self._parse_client_response_for_data_source(
            client_details, field_name=EdiscoveryConstants.FIELD_DATA_SOURCE_DISPLAY_NAME)
        ds_type = self._parse_client_response_for_data_source(
            client_details, field_name=EdiscoveryConstants.FIELD_DATA_SOURCE_TYPE)
        plan_id = self._parse_client_response_for_data_source(
            client_details, field_name=EdiscoveryConstants.FIELD_PLAN_ID, field_type="int")
        subclient_id = self._parse_client_response_for_data_source(
            client_details, field_name=EdiscoveryConstants.FIELD_SUBCLIENT_ID, field_type="int")
        crawl_type = self._parse_client_response_for_data_source(
            client_details, field_name=EdiscoveryConstants.FIELD_CRAWL_TYPE, field_type="int")
        for data_source in client_details['childs']:
            ds_id = 0
            if 'dsEntity' in data_source:
                ds_id = data_source['dsEntity'].get(EdiscoveryConstants.FIELD_DATA_SOURCE_ID, 0)
            ds_props = {
                EdiscoveryConstants.FIELD_DATA_SOURCE_DISPLAY_NAME: ds_name[index],
                EdiscoveryConstants.FIELD_DATA_SOURCE_TYPE: ds_type[index],
                EdiscoveryConstants.FIELD_PLAN_ID: plan_id[index],
                EdiscoveryConstants.FIELD_SUBCLIENT_ID: subclient_id[index],
                EdiscoveryConstants.FIELD_DATA_SOURCE_ID: ds_id,
                EdiscoveryConstants.FIELD_CRAWL_TYPE: crawl_type
            }
            output[ds_name[index].lower()] = ds_props
            index = index + 1
        return output

    def refresh(self):
        """Refresh the data sources associated with edisocvery client"""
        if not self._client_id:
            return
        self._ediscovery_client_props = self._get_data_sources_details()
        self._data_source_display_names, self._data_source_names = self._get_data_source_names(
            self._ediscovery_client_props)
        self._data_sources = self._get_data_source_properties(self._ediscovery_client_props)

    def add_fs_data_source(self, server_name, data_source_name, inventory_name, plan_name,
                           source_type=EdiscoveryConstants.SourceType.BACKUP, **kwargs):
        """Adds file system data source to server

                Args:

                    server_name         (str)       --  Server name which needs to be added

                    data_source_name    (str)       --  Name for data source

                    inventory_name      (str)       --  Inventory name which needs to be associated

                    plan_name           (str)       --  Plan name which needs to be associated with this data source

                    source_type         (enum)      --  Source type for crawl (Live source or Backedup)
                                                                Refer EdiscoveryConstants.SourceType

                Kwargs Arguments:

                    scan_type           (str)       --  Specifies scan type when source type is for backed up data
                                                                Supported values : quick | full

                    crawl_path          (list)      --  File path which needs to be crawl if source type is Live source

                    access_node         (str)       --  server name which needs to be used as access node in case
                                                                if server to be added is not a commvault client

                    country_name        (str)       --  country name where server is located (default: USA)

                    country_code        (str)       --  Country code (ISO 3166 2-letter code)

                    user_name           (str)       --  User name who has access to UNC path

                    password            (str)       --  base64 encoded password to access unc path

                    enable_monitoring   (str)       --  specifies whether to enable file monitoring or not for this

                Returns:

                    obj     --  Instance of EdiscoveryDataSource class

                    None    --  if it is called to create FSO server group

                Raises:

                      SDKException:

                            if plan/inventory/index server doesn't exists

                            if failed to add FSO server data source
        """
        is_commvault_client = False
        is_server_group = False
        if self._app_source_sub_type and self._app_source_sub_type == EdiscoveryConstants.FSO_SERVER_GROUPS:
            is_server_group = True
        if not self._commcell_object.activate.inventory_manager().has_inventory(inventory_name):
            raise SDKException('EdiscoveryClients', '102', 'Invalid inventory name')
        if not self._commcell_object.plans.has_plan(plan_name):
            raise SDKException('EdiscoveryClients', '102', 'Invalid plan name')
        plan_obj = self._commcell_object.plans.get(plan_name)
        if self._app_source.value not in plan_obj.content_indexing_props['targetApps']:
            raise SDKException('EdiscoveryClients', '102', 'Plan is not marked with targetapp as FSO')
        inv_obj = self._commcell_object.activate.inventory_manager().get(inventory_name)
        request_json = copy.deepcopy(EdiscoveryConstants.ADD_FS_REQ_JSON)
        request_json['datasourceId'] = inv_obj.inventory_id
        request_json['indexServerClientId'] = plan_obj.content_indexing_props['analyticsIndexServer'].get('clientId', 0)
        request_json['datasources'][0]['datasourceName'] = data_source_name
        # find out whether given server is commvault client or not to decide further
        inventory_resp = None
        scan_type = kwargs.get('scan_type', 'quick')
        if not is_server_group:
            is_commvault_client = self._commcell_object.clients.has_client(server_name)
            if not is_commvault_client:
                if ('access_node' not in kwargs or 'user_name' not in kwargs or 'password' not in kwargs):
                    raise SDKException('EdiscoveryClients', '102', "Access node information is missing")
                if not self._commcell_object.clients.has_client(kwargs.get("access_node")):
                    raise SDKException('EdiscoveryClients', '102', "Access node client is not present")
            inventory_resp = inv_obj.handler.get_handler_data(
                handler_filter=f"q=(name_idx:{server_name} AND objectClass:computer)&rows=1")
            if inventory_resp['numFound'] != 1:
                raise SDKException('EdiscoveryClients', '102', 'Multiple server with same name exists in inventory')
            inventory_resp = inventory_resp['docs'][0]
        # set common properties
        request_json['datasources'][0]['properties'].append({
            "propertyName": "enablemonitoring",
            "propertyValue": kwargs.get('enable_monitoring', "false").lower()
        })
        request_json['datasources'][0]['properties'].append({
            "propertyName": "countryCode",
            "propertyValue": kwargs.get('country_code', 'US')
        })
        request_json['datasources'][0]['properties'].append({
            "propertyName": "co",
            "propertyValue": kwargs.get('country_name', 'United States')
        })
        request_json['datasources'][0]['properties'].append({
            "propertyName": "contentid",
            "propertyValue": inventory_resp['contentid'] if not is_server_group else server_name
        })
        request_json['datasources'][0]['properties'].append({
            "propertyName": "clientdisplayname",
            "propertyValue": server_name
        })
        request_json['datasources'][0]['properties'].append({
            "propertyName": "dcplanid",
            "propertyValue": str(plan_obj.plan_id)
        })
        request_json['datasources'][0]['properties'].append({
            "propertyName": "name",
            "propertyValue": inventory_resp['name'] if not is_server_group else server_name
        })
        request_json['datasources'][0]['properties'].append({
            "propertyName": "operatingSystem",
            "propertyValue": inventory_resp['operatingSystem'] if not is_server_group else ""
        })
        if is_commvault_client:
            del request_json['datasources'][0]['accessNodes']
            request_json['datasources'][0]['properties'].append({
                "propertyName": "ClientId",
                "propertyValue": str(self._commcell_object.clients.get(server_name).client_id)
            })
            request_json['datasources'][0]['properties'].append({
                "propertyName": "ContentIndexingStatus",
                "propertyValue": str(inventory_resp['ContentIndexingStatus'])
            })
            request_json['datasources'][0]['properties'].append({
                "propertyName": "BackedupStatus",
                "propertyValue": str(inventory_resp['BackedupStatus'])
            })
        elif is_server_group:
            del request_json['datasources'][0]['accessNodes']
            del request_json['indexServerClientId']
            request_json['datasources'][0]['properties'].append({
                "propertyName": "ClientGroupId",
                "propertyValue": str(self._commcell_object.client_groups.get(server_name).clientgroup_id)
            })
            request_json['datasources'][0]['properties'].append({
                "propertyName": "ContentIndexingStatus",
                "propertyValue": str(0)
            })
            request_json['datasources'][0]['properties'].append({
                "propertyName": "BackedupStatus",
                "propertyValue": str(0)
            })

        # set crawl type and source type related params
        if source_type.value == EdiscoveryConstants.SourceType.BACKUP.value:
            if scan_type == 'quick':
                request_json['datasources'][0]['properties'].append({
                    "propertyName": "crawltype",
                    "propertyValue": str(EdiscoveryConstants.CrawlType.FILE_LEVEL_ANALYTICS.value)
                })
            else:
                request_json['datasources'][0]['properties'].append({
                    "propertyName": "crawltype",
                    "propertyValue": str(EdiscoveryConstants.CrawlType.BACKUP_V2.value)
                })
        else:
            if not is_commvault_client:
                request_json['datasources'][0]['properties'].append({
                    "propertyName": "username",
                    "propertyValue": kwargs.get('user_name', '')
                })
                request_json['datasources'][0]['properties'].append({
                    "propertyName": "password",
                    "propertyValue": kwargs.get('password', '')
                })
                request_json['datasources'][0]['properties'].append({
                    "propertyName": "domainName",
                    "propertyValue": inventory_resp['domainName']
                })
                request_json['datasources'][0]['properties'].append({
                    "propertyName": "dNSHostName",
                    "propertyValue": inventory_resp['dNSHostName']
                })
                request_json['datasources'][0]['accessNodes'][0]['clientId'] = int(
                    self._commcell_object.clients.get(kwargs.get('access_node')).client_id)
                request_json['datasources'][0]['accessNodes'][0]['clientName'] = kwargs.get('access_node')

            request_json['datasources'][0]['properties'].append({
                "propertyName": "includedirectoriespath",
                "propertyValue": ','.join(kwargs.get('crawl_path', []))
            })

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_CREATE_DATA_SOURCE, request_json)
        if flag:
            if response.json() and 'collections' in response.json():
                collection = response.json()['collections'][0]
                if 'datasources' in collection:
                    data_source = collection['datasources'][0]
                    # when add data source is called for new server then handle client id accordingly
                    if is_server_group:
                        # for server group, no need to refresh data sources details as we go via Server by server only
                        return
                    if not self._client_id:
                        if is_commvault_client:
                            self._client_id = inventory_resp['ClientId']
                        else:
                            self._commcell_object.clients.refresh()
                            all_clients = self._commcell_object.clients.all_clients
                            for client_name, client_details in all_clients.items():
                                if client_name.startswith(f"{data_source_name}_"):
                                    self._client_id = self._commcell_object.clients.get(client_name).client_id
                                    break
                        self._ediscovery_client_ops = EdiscoveryClientOperations(self._commcell_object, self)
                    self.refresh()
                    return EdiscoveryDatasource(
                        self._commcell_object,
                        data_source['datasourceId'],
                        EdiscoveryConstants.DATA_SOURCE_TYPES[5])
            if response.json() and 'error' in response.json():
                error = response.json()['error']
                if 'errorCode' in error and error['errorCode'] != 0:
                    raise SDKException(
                        'EdiscoveryClients',
                        '102',
                        f"Creation of data source failed with error - {error['errorCode']}")
            raise SDKException('EdiscoveryClients', '115')
        self._response_not_success(response)

    def delete(self, data_source_name):
        """Deletes the given data source from client

                        Args:

                            data_source_name        (str)       --  Datasource name

                        Returns:

                            None

                        Raises:

                            SDKException:

                                    if failed to find given data source in this client

                                    if failed to delete the data source

        """
        if not self.has_data_source(data_source_name):
            raise SDKException('EdiscoveryClients', '108')
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._API_DELETE % (self.get(data_source_name).data_source_id, self._client_id)
        )
        if flag:
            if response.json() and 'errorCode' in response.json():
                if response.json()['errorCode'] != 0:
                    raise SDKException(
                        'EdiscoveryClients',
                        '102',
                        f"Failed to Delete DataSource with error [{response.json().get('errorMessage','')}]")
                self.refresh()
            else:
                raise SDKException('EdiscoveryClients', '111')
        else:
            self._response_not_success(response)

    def has_data_source(self, data_source_name):
        """Checks whether given data source exists in this client or not

                Args:

                    data_source_name        (str)       --  Datasource name

                Returns:

                    bool    --  True if exists else false

                Raises:

                    SDKException:

                            if failed to find given data source in this client

        """
        if not isinstance(data_source_name, str):
            raise SDKException('EdiscoveryClients', '101')
        return self._data_source_display_names and data_source_name.lower() in self._data_source_display_names

    def get(self, data_source_name):
        """returns EdiscoveryDataSource class object for given data source name

                Args:

                    data_source_name        (str)       --  Datasource name

                Returns:

                    obj --  Instance of EdiscoveryDataSource class

                Raises:

                    SDKException:

                            if failed to find given data source in this client

                            if input is not valid

        """
        if not isinstance(data_source_name, str):
            raise SDKException('EdiscoveryClients', '101')
        if not self.has_data_source(data_source_name):
            raise SDKException('EdiscoveryClients', '108')
        ds_props = self._data_sources[data_source_name.lower()]
        return EdiscoveryDatasource(commcell_object=self._commcell_object,
                                    data_source_id=int(ds_props[EdiscoveryConstants.FIELD_DATA_SOURCE_ID]),
                                    data_source_type=ds_props[EdiscoveryConstants.FIELD_DATA_SOURCE_TYPE],
                                    app_type=self._app_source)

    def _parse_client_response_for_data_source(self, client_details, field_name, field_type="str"):
        """Parses client response and returns given property from data sources as list

                Args:

                    client_details      (dict)      --  containing EdiscoveryClient details response

                    field_name          (str)       --  Field name to be fetched

                    field_type          (str)       --  Field type to be converted (Default: str)

                Returns:

                    list        --  containing field values from all data sources in response

                Raises:

                    SDKException:

                            if input is not valid


        """
        output = []
        old_len = len(output)
        if not isinstance(client_details, dict):
            raise SDKException('EdiscoveryClients', '107')
        for data_source in client_details['childs']:
            if 'customProperties' in data_source:
                name_value_dict = data_source['customProperties']['nameValues']
                for prop in name_value_dict:
                    prop_name = prop.get('name')
                    if prop_name == field_name:
                        if field_type == "int":
                            output.append(int(prop.get('value', 0)))
                        else:
                            if field_name == EdiscoveryConstants.FIELD_DATA_SOURCE_DISPLAY_NAME:
                                output.append(prop.get('value', 'NA').lower())
                            else:
                                output.append(prop.get('value', 'NA'))
            new_len = len(output)
            if old_len == new_len:
                output.append('Not Found')
                new_len = new_len + 1
            old_len = new_len
        return output

    def _get_data_source_names(self, client_details):
        """returns the list of data source display name and data source name

                Args:

                    client_details      (dict)      --  containing EdiscoveryClient details response

                Returns:

                    list,list       --  Data source display name & Data Source name

                Raises:

                    SDKException:

                            if input is not valid

        """
        if not isinstance(client_details, dict):
            raise SDKException('EdiscoveryClients', '107')
        data_sources_name = self._parse_client_response_for_data_source(
            client_details, EdiscoveryConstants.FIELD_DATA_SOURCE_NAME)
        data_sources_display_name = self._parse_client_response_for_data_source(
            client_details, EdiscoveryConstants.FIELD_DATA_SOURCE_DISPLAY_NAME)
        return data_sources_display_name, data_sources_name

    def _get_data_sources_details(self):
        """returns the data sources details associated with ediscovery client

                Args:

                    None

                Return:

                    dict    --  containing data source details

                Raises:

                        SDKException:

                                if failed to get data source details

        """
        server_details = self._ediscovery_client_ops.get_ediscovery_client_details()
        return server_details

    @property
    def data_sources(self):
        """returns the list of data sources display nameassociated with this client

            Returns:

                list --  Name of data sources

        """
        return self._data_source_display_names

    @property
    def client_id(self):
        """returns the associated client id

            Returns:

                int --  client id

        """
        return self._client_id

    @property
    def client_targetapp(self):
        """returns the source client targetapp

            Returns:

                str --  Target app for this data sources

        """
        return self._app_source.value

    @property
    def ediscovery_client_props(self):
        """Returns the associated client properties

            Returns:

                dict --  containing client properties

        """
        return self._ediscovery_client_props

    @property
    def total_documents(self):
        """returns the total document counts of all data sources associated with this client

            Returns:

                int --  Total crawled documents from all of these data sources

        """
        return sum(
            self._parse_client_response_for_data_source(
                client_details=self.ediscovery_client_props,
                field_name=EdiscoveryConstants.FIELD_DOCUMENT_COUNT,
                field_type="int"))


class EdiscoveryDatasource():
    """Class to represent single datasource associated with ediscovery client"""

    def __init__(self, commcell_object, data_source_id, data_source_type, app_type=TargetApps.FSO):
        """Initializes an instance of the EdiscoveryDataSource class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                data_source_id      (int)       --  Data source id

                data_source_type    (int/str)   --  Data Source type (Example : 5 for file)
                                                        Refer to EdiscoveryConstants class in activateapps\constants.py

                app_type            (enum)      --  Specifies which app type these data sources belongs too
                                                        Default:FSO

            Returns:
                object  -   instance of the EdiscoveryDataSource class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._data_source_name = None
        self._data_source_id = None
        self._data_source_type = None
        self._data_source = None
        self._data_source_props = None
        self._client_id = None
        self._collection_client_id = None
        self._core_name = None
        self._computed_core_name = None
        self._cloud_id = None
        self._core_id = None
        self._crawl_type = None
        self._dc_plan_id = None
        self._data_source_entity_id = 132
        self._app_type = app_type
        self._API_DATA_SOURCE = self._services['EDISCOVERY_DATA_SOURCES']
        self._API_SEARCH = self._services['EDISCOVERY_DYNAMIC_FEDERATED']
        self._API_ACTIONS = self._services['EDISCOVERY_REVIEW_ACTIONS']
        self._API_ACTIONS_WITH_REQUEST = self._services['EDISCOVERY_REVIEW_ACTIONS_WITH_REQUEST']
        self._jobs = self._commcell_object.job_controller
        self._data_source_id = data_source_id
        if isinstance(data_source_type, int):
            self._data_source_type = EdiscoveryConstants.DATA_SOURCE_TYPES.get(data_source_type)
        else:
            self._data_source_type = data_source_type
        self.refresh()
        self._ediscovery_client_ops = EdiscoveryClientOperations(self._commcell_object, self)

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_data_source_properties(self):
        """returns the data source properties for this data source

            Args:

                None

            Returns:

                Dict    --  Containing data source details

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._API_DATA_SOURCE %
            (self._data_source_id, self._data_source_type))
        if flag:
            if response.json() and 'collections' in response.json():
                collection = response.json()['collections'][0]
                self._collection_client_id = collection.get('clientId')
                self._core_name = collection.get('coreName')
                self._computed_core_name = collection.get('computedCoreName')
                self._cloud_id = collection.get('cloudId')
                self._core_id = collection.get('coreId')
                ds_list = collection.get('datasources', [])
                if len(ds_list) == 1:
                    self._data_source_props = ds_list[0].get('properties', [])
                    # fetch crawl type from above properties fetched.
                    self._crawl_type = self._get_property_value(property_name=EdiscoveryConstants.FIELD_CRAWL_TYPE)
                    self._dc_plan_id = self._get_property_value(property_name=EdiscoveryConstants.FIELD_DC_PLAN_ID)
                    self._client_id = self._get_property_value(
                        property_name=EdiscoveryConstants.FIELD_PSEDUCO_CLIENT_ID)
                    self._data_source_name = ds_list[0].get('displayName', 'NA')
                return collection
            raise SDKException('EdiscoveryClients', '110')
        self._response_not_success(response)

    def _get_property_value(self, property_name):
        """Returns the property value for property name

            Args:

                property_name       (str)       --  Name of property

            Returns:
                str --  value of property

        """
        for prop in self.data_source_props:
            if 'propertyName' in prop:
                if prop['propertyName'].lower() == property_name.lower():
                    return prop['propertyValue']
        return ""

    def refresh(self):
        """refresh the data source properties"""
        self._data_source = self._get_data_source_properties()

    def tag_items(
            self,
            tags,
            document_ids=None,
            ops_type=1,
            create_review=False,
            reviewers=None,
            approvers=None,
            req_name=None):
        """Applies given tag to documents

            Args:

                tags            (list)      --  list of tags names which needs to be applied
                                                        Format : Tagset\\TagName
                                                        Example : DiscoveryEntity\\American

                document_ids    (list)      --  list of document content id's which needs to be tagged

                ops_type        (int)       --  Denotes operation type for tagging  (1-Add or 2-Delete)
                                                        Default : 1(Add)

                create_review   (bool)      --  Specifies whether to create review request for this tagging or not
                                                        Default:False

                reviewers       (list)      --  List of review users

                approvers       (list)      --  List of approver users

                req_name        (str)       --  Request name

            Returns:

                None if it is few items tagging or tagging with review request

                jobid (str) -- if it is bulk operation of tagging all items without review request

            Raises:

                SDKException:

                        if tag name doesn't exists in commcell

                        if failed to apply tag

                        if response is empty

                        if data source doesn't belongs to FSO app
        """
        if self._app_type.value != TargetApps.FSO.value:
            raise SDKException('EdiscoveryClients', '102', "Tagging is supported only for FSO app")
        if not isinstance(tags, list):
            raise SDKException('EdiscoveryClients', '101')
        query = ""
        request_json = None
        tag_guids = []
        api = self._API_ACTIONS
        if create_review:
            api = self._API_ACTIONS_WITH_REQUEST

        tag_mgr = self._commcell_object.activate.entity_manager(EntityManagerTypes.TAGS)
        for tag in tags:
            tag_split = tag.split("\\\\")
            if not tag_mgr.has_tag_set(tag_set_name=tag_split[0]):
                raise SDKException('EdiscoveryClients', '102', "Unable to find tagset in the commcell")
            tag_set_obj = tag_mgr.get(tag_split[0])
            if not tag_set_obj.has_tag(tag_split[1]):
                raise SDKException('EdiscoveryClients', '102', "Unable to find tag in the tagset")
            tag_obj = tag_set_obj.get(tag_split[1])
            if not create_review:
                tag_guids.append({"id": tag_obj.guid})
            else:
                tag_guids.append(tag_obj.guid)

        if not create_review:
            if document_ids:
                for doc in document_ids:
                    query = query + f"(contentid:{doc}) OR "
                last_char_index = query.rfind(" OR ")
                query = query[:last_char_index]
            else:
                query = "*:*"
            search_params = self._ediscovery_client_ops.form_search_params(
                query=query, key="name", params={"rows": "0"})
            tag_request = copy.deepcopy(EdiscoveryConstants.TAGGING_ITEMS_REQUEST)
            request_json = copy.deepcopy(EdiscoveryConstants.REVIEW_ACTION_TAG_REQ_JSON)
            if ops_type != 1:
                tag_request['opType'] = "DELETE"
            if not document_ids:  # bulk request
                tag_request['isAsync'] = True
            tag_request['entityIds'].append(self.data_source_id)
            tag_request['searchRequest'] = search_params
            tag_request['tags'] = tag_guids
            tag_request['dsType'] = self.data_source_type_id
            request_json['taggingRequest'] = tag_request
            request_json['remActionRequest']['dataSourceId'] = self.data_source_id
            if not document_ids:
                request_json['remActionRequest']['isBulkOperation'] = True

        else:
            request_json = copy.deepcopy(EdiscoveryConstants.TAGGING_ITEMS_REVIEW_REQUEST)
            if ops_type != 1:
                request_json['taggingInformation']['opType'] = "DELETE"
            request_json['files'] = json.dumps(self._form_files_list(
                document_ids=document_ids,
                attr_list=EdiscoveryConstants.REVIEW_ACTION_IDA_SELECT_SET[self.data_source_type_id]))
            request_json['taggingInformation']['tagIds'] = tag_guids
            request_json['options'] = str(
                self._form_request_options(
                    reviewers=reviewers,
                    approvers=approvers,
                    document_ids=document_ids,
                    req_name=req_name if req_name else f"{self.data_source_name}_tag_{int(time.time())}"))

        flag, response = self._cvpysdk_object.make_request(
            'POST', api, request_json
        )
        if flag:
            if response.json():
                response = response.json()
                if 'errorCode' in response and response['errorCode'] != 0:
                    raise SDKException(
                        'EdiscoveryClients',
                        '102',
                        f"Tagging failed with error : {response.get('errorMessage', '')}")
                else:
                    if not create_review:
                        # tagging without review. return the job id
                        return response['jobId']
                    return
            raise SDKException('EdiscoveryClients', '113')
        self._response_not_success(response)

    def get_job_history(self, limit=50, lookup_time=2160):
        """returns the job history details for this data source

            Args:

                limit       (int)           --  No of jobs to return (default: 50 rows)

                lookup_time (int)           --  list of jobs to be retrieved which are specified
                    hours older

                            default: 2160 hours (last 90 days)

        """
        return self._jobs.finished_jobs(lookup_time=lookup_time,
                                        limit=limit,
                                        entity={"dataSourceId": self.data_source_id})

    def get_active_jobs(self, limit=50, lookup_time=2160):
        """returns the active jobs details for this data source

            Args:

                limit       (int)           --  No of jobs to return (default: 50 rows)

                lookup_time (int)           --  list of jobs to be retrieved which are started within specified
                    hours older

                            default: 2160 hours (last 90 days)

        """
        return self._jobs.active_jobs(lookup_time=lookup_time,
                                      limit=limit,
                                      entity={"dataSourceId": self.data_source_id})

    def wait_for_export(self, token, wait_time=60):
        """Waits for Export to CSV to finish

                Args:

                    wait_time           (int)       --  time interval to wait for job completion in Mins
                                                            Default : 60Mins

                    token               (str)       --  Export to CSV token GUID

                Return:

                    str     -- Download GUID for exported CSV file

                Raises:

                    SDKException:

                            if Export job fails

                            if timeout happens

        """
        return self._ediscovery_client_ops.wait_for_export(token=token,
                                                           wait_time=wait_time)

    def export(self, criteria=None, attr_list=None, params=None):
        """do export to CSV on data

            Args:

                criteria        (str)      --  containing criteria for query
                                                    (Default : None - Exports all docs)

                                                    Example :

                                                        1) Size filter --> Size:[10 TO 1024]
                                                        2) File name filter --> FileName_idx:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                params          (dict)     --  Any other params which needs to be passed
                                                   Example : { "start" : "0" }

            Returns:

                str     --  export operation token


            Raises:

                SDKException:

                        if failed to perform export

        """
        if not attr_list:
            if self.data_source_type == EdiscoveryConstants.DATA_SOURCE_TYPES[5]:
                attr_list = EdiscoveryConstants.FS_DEFAULT_EXPORT_FIELDS
        return self._ediscovery_client_ops.export(criteria=criteria, attr_list=attr_list,
                                                  params=params)

    def search(self, criteria=None, attr_list=None, params=None):
        """do searches on data source and returns document details

            Args:

                criteria        (str)      --  containing criteria for query
                                                    (Default : None - returns all docs)

                                                    Example :

                                                        1) Size filter --> Size:[10 TO 1024]
                                                        2) File name filter --> FileName_idx:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                params          (dict)     --  Any other params which needs to be passed
                                                   Example : { "start" : "0" }

            Returns:

                list(dict),dict    --  Containing document details & facet details(if any)

            Raises:

                SDKException:

                        if failed to perform search

        """
        return self._ediscovery_client_ops.search(criteria=criteria, attr_list=attr_list,
                                                  params=params)

    def _form_request_options(self, req_name, reviewers, approvers, document_ids=None):
        """Returns the options for review request

            Args:

                req_name        (str)       --  Request Name

                reviewers       (list)      --  List of review users

                approvers       (list)      --  List of approver users

                document_ids    (list)      --  list of document id's
                                                    Default:None

            Returns:

                dict        --  Containing options

            Raises:

                SDKException:

                        if failed to get document details

                        if failed to find user details for reviewers/approvers
        """
        options = {
            "Name": req_name,
            "DatasetId": str(self.data_source_id),
            "DatasetType": "SEA_DATASOURCE_ENTITY",
            "DatasetName": self.data_source_name,
            "CreatedFrom": "FSO" if self._app_type.value == TargetApps.FSO.value else "SDG",
            "ClientId": str(self._client_id)
        }
        if document_ids:
            query = ""
            for doc in document_ids:
                query = query + f"(contentid:{doc}) OR "
            last_char_index = query.rfind(" OR ")
            query = query[:last_char_index]
            docs, facets = self.search(
                criteria=query, attr_list=EdiscoveryConstants.REVIEW_ACTION_IDA_SELECT_SET[self.data_source_type_id])
            if len(docs) != len(document_ids):
                raise SDKException(
                    'EdiscoveryClients',
                    '102',
                    "Unable to find document details from given list of document id")
            file_names = []
            for doc in docs:
                file_names.append(doc['FileName'])
            options['ReviewCriteria'] = json.dumps({
                "Files": file_names
            })
        else:
            options['ReviewCriteria'] = json.dumps({})
        # reviewer
        reviewers_list = []
        for user in reviewers:
            if not self._commcell_object.users.has_user((user)):
                raise SDKException('EdiscoveryClients', '102', f"Unable to find reviewer user : {user}")
            user_obj = self._commcell_object.users.get(user)
            reviewers_list.append({"id": user_obj.user_id,
                                   "name": user_obj.user_name
                                   })
        options['Reviewers'] = str(reviewers_list)

        # approvers
        approvers_list = []
        for user in approvers:
            if not self._commcell_object.users.has_user((user)):
                raise SDKException('EdiscoveryClients', '102', f"Unable to find approver user : {user}")
            user_obj = self._commcell_object.users.get(user)
            approvers_list.append({"id": user_obj.user_id,
                                   "name": user_obj.user_name
                                   })
        options['Approvers'] = str(approvers_list)
        return options

    def _form_files_list(self, document_ids, attr_list):
        """returns the list of dict containing files details

                Args:

                    document_ids        (list)      --  list of document id's

                    attr_list           (set)       --  Set of fields needed to be fetched for document id

                Returns:

                      list(dict)      --  Containing file details

                Raises:

                    SDKException:

                        if failed to get document details

        """
        query = ""
        files_list = []
        for doc in document_ids:
            query = query + f"(contentid:{doc}) OR "
        last_char_index = query.rfind(" OR ")
        query = query[:last_char_index]
        docs, facets = self.search(criteria=query, attr_list=attr_list)
        if len(docs) != len(document_ids):
            raise SDKException(
                'EdiscoveryClients',
                '102',
                "Unable to find document details from given list of document id")
        for doc in docs:
            doc_dict = {
                "file": doc['Url'],
                "dsid": str(
                    self.data_source_id),
                "contentid": doc['contentid'],
                "CreatedTime": doc['CreatedTime'],
                "ClientId": doc['ClientId'],
                "dstype": self.data_source_type_id}
            files_list.append(doc_dict)
        return files_list

    def review_action(self, action_type, reviewers, approvers, document_ids=None, req_name=None, **kwargs):
        """do review action on documents

                Args:

                    action_type         (enum)      --  Type of action to be taken
                                                        Refer to EdiscoveryConstants.ReviewActions

                    document_ids        (list)      --  list of document id's
                                                            Default:None (means all docs)

                    reviewers           (list)      --  List of review users

                    approvers           (list)      --  List of approver users

                    req_name            (str)       --  Request name

                kwargs arguments:

                    backup_delete       (bool)      --  Spcifies whether to delete document from backup or not

                    destination         (str)       --  Destination UNC path for move operation

                    user_name           (str)       --  Username to access share path

                    password            (str)       --  Password for user in base64 encoded

                Returns:

                    None for review actions on few files

                    job id for review actions on bulk files

                Raises:

                    SDKException:

                        if action type is not valid

                        if failed to do review action on documents

                        if document id's not found
        """
        if not isinstance(action_type, EdiscoveryConstants.ReviewActions):
            raise SDKException('EdiscoveryClients', '101')
        if self._app_type.value == TargetApps.FSO.value and \
                action_type.value not in EdiscoveryConstants.REVIEW_ACTION_FSO_SUPPORTED:
            raise SDKException('EdiscoveryClients', '102', f"{action_type.value} is not supported for FSO app")
        attr_list = None
        if self.data_source_type_id not in EdiscoveryConstants.REVIEW_ACTION_IDA_SELECT_SET:
            raise SDKException('EdiscoveryClients', '102', "Not supported data source for review action")
        attr_list = EdiscoveryConstants.REVIEW_ACTION_IDA_SELECT_SET[self.data_source_type_id]
        request_json = None
        if action_type.value == EdiscoveryConstants.ReviewActions.DELETE.value:
            request_json = copy.deepcopy(EdiscoveryConstants.REVIEW_ACTION_DELETE_REQ_JSON)
            request_json['deleteFromBackup'] = kwargs.get("backup_delete", False)
        elif action_type.value == EdiscoveryConstants.ReviewActions.MOVE.value:
            if 'destination' not in kwargs or 'user_name' not in kwargs or 'password' not in kwargs:
                raise SDKException('EdiscoveryClients', '102', "Required params missing for move operation")
            request_json = copy.deepcopy(EdiscoveryConstants.REVIEW_ACTION_MOVE_REQ_JSON)
            request_json['newDestination'] = kwargs.get("destination", '')
            request_json['username'] = kwargs.get("user_name", '')
            request_json['password'] = kwargs.get("password", '')
        if document_ids:
            request_json['files'] = json.dumps(self._form_files_list(document_ids=document_ids, attr_list=attr_list))
        else:
            # bulk operation request
            del request_json['files']
            request_json['isBulkOperation'] = True
            request_json['searchRequest'] = EdiscoveryConstants.REVIEW_ACTION_BULK_SEARCH_REQ
            request_json['handlerId'] = self._ediscovery_client_ops.get_handler_id()

        request_json['options'] = json.dumps(
            self._form_request_options(
                reviewers=reviewers,
                approvers=approvers,
                document_ids=document_ids,
                req_name=req_name if req_name else f"{self.data_source_name}_{action_type.name}_{int(time.time())}"))

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_ACTIONS_WITH_REQUEST, request_json
        )
        if flag:
            if response.json():
                response = response.json()
                if 'errorCode' in response and response['errorCode'] != 0:
                    raise SDKException(
                        'EdiscoveryClients',
                        '102',
                        f"Review action failed with error - {response.get('errorMsg')}")
                if not document_ids and 'jobId' in response:
                    return response['jobId']
                return
            raise SDKException('EdiscoveryClients', '116')
        self._response_not_success(response)

    @property
    def data_source_name(self):
        """returns the data source name

            Returns:

                str --  Name of data source

        """
        return self._data_source_name

    @property
    def data_source_type(self):
        """returns the data source type

            Returns:

                str --  Type of data source

        """
        return self._data_source_type

    @property
    def data_source_type_id(self):
        """returns the data source type id

            Returns:

                int --  data source type

        """
        position = list(EdiscoveryConstants.DATA_SOURCE_TYPES.values()).index(self.data_source_type)
        return list(EdiscoveryConstants.DATA_SOURCE_TYPES.keys())[position]

    @property
    def data_source_id(self):
        """returns the data source id

            Returns:

                int --  data source id

        """
        return self._data_source_id

    @property
    def data_source_props(self):
        """returns the data source properties

            Returns:

                dict --  data source properties

        """
        return self._data_source_props

    @property
    def cloud_id(self):
        """returns the index server cloudid associated with this data source

            Returns:

                int --  index server cloud id

        """
        return self._cloud_id

    @property
    def core_name(self):
        """returns the core name for this data source

            Returns:

                str --  core name for this data source

        """
        return self._core_name

    @property
    def computed_core_name(self):
        """returns the computed core name for this data source

            Returns:

                str --  Index server core name for this data source

        """
        return self._computed_core_name

    @property
    def core_id(self):
        """returns the core id for this data source

            Returns:

                int --  core id

        """
        return self._core_id

    @property
    def crawl_type_name(self):
        """returns the crawl type enum name for this data source

            Returns:

                str --  crawl type

        """
        return EdiscoveryConstants.CrawlType(int(self._crawl_type)).name

    @property
    def crawl_type(self):
        """returns the crawl type for this data source

            Returns:

                int --  crawl type

        """
        return self._crawl_type

    @property
    def plan_id(self):
        """returns the DC plan id associated

            Returns:

                int -- Data classification plan id

        """
        return self._dc_plan_id
