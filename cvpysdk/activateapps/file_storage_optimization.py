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

"""Main file for performing operations on file storage optimization(FSO) app under Activate.

'FsoTypes', 'FsoServers' , 'FsoServer', 'FsoServerGroups', 'FsoServerGroup' are 5 classes defined in this file

FsoTypes:  Class to represent different FSO types(Server/ServerGroup/Project)

FsoServers: Class to represent all FSO servers in the commcell

FsoServer:  Class to represent single FSO server in the commcell

FsoServerGroups:  Class to represent all FSO server groups in the commcell

FsoServerGroup:   Class to represent single FSO server group in the commcell

FsoServers:

    __init__()                          --  initialise object of the FsoServers class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_all_fso_servers()             --  gets all the fso servers from the commcell

     refresh()                          --  refresh the FSO Servers associated with the commcell

     has_server()                       --  checks whether given server name exists in FSO or not

     add_file_server()                  --  adds file server to the FSO

     get()                              --  returns the FsoServer object for given server name

FsoServer:

    __init__()                          --  initialise object of the FsoServer class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_server_properties()           --  gets FSO server details from the commcell

     _get_schedule_object()             --  returns the schedule object for associated schedule

     refresh()                          --  refresh the FSO Server details

     start_collection()                 --  starts collection job on all data sources in this server

     share()                            --  shares server with given user name or group name

     search()                           --  returns the search response containing document details

     add_schedule()                     --  creates schedule for this fso server

     delete_schedule()                  --  deletes schedule for this fso server

FsoServer Attributes
---------------------

    **server_id**           --  returns the client id of the server

    **server_details**      --  returns the server details

    **data_sources**        --  returns the EdiscoveryDataSources object

    **data_sources_name**   --  returns the list of data sources display name associated with this server

    **total_data_sources**  --  returns the total number of data sources associated with this server

    **total_doc_count**     --  returns the total document count from all data sources associated with this server

    **schedule**            --  returns the schedule object for associated schedule with this server

FsoServerGroups:

    __init__()                          --  initialise object of the FsoServerGroups class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_all_fso_server_groups()       --  gets all the fso server groups from the commcell

     refresh()                          --  refresh the FSO Server groups associated with the commcell

     has()                              --  checks whether given server group name exists in FSO or not

     get()                              --  returns object of FsoServerGroup class

     add_server_group()                 --  adds server group to FSO

FsoServerGroup:

    __init__()                          --  initialise object of the FsoServerGroup class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_server_group_properties()     --  gets FSO server group details from the commcell

     refresh()                          --  refresh the FSO Server group details

     has_server()                       --  returns whether server name exists as part of server group or not

     get()                              --  returns the object of FsoServer class

     start_collection()                 --  starts collection job on all servers associated with this server group

     search()                           --  returns the search response containing document details

FsoServerGroup Attributes:
---------------------------

    **server_group_id**     --  returns the server group id

    **server_group_props**  --  returns the properties of server group

    **server_list**         --  returns the list of servers associated with this server group

    **total_documents**     --  returns the total crawled document count for this server group

"""
import copy
import time
from enum import Enum

from ..schedules import Schedules

from ..activateapps.constants import EdiscoveryConstants

from ..activateapps.ediscovery_utils import EdiscoveryClients, EdiscoveryClientOperations, EdiscoveryDataSources

from ..exception import SDKException


class FsoTypes(Enum):
    """Class to represent different FSO types(Server/ServerGroup/Project)"""
    SERVERS = 0
    SERVER_GROUPS = 1
    PROJECTS = 2


class FsoServers():
    """Class for representing all FSO servers in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the FsoServers class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the FsoServers class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._fso_servers = None
        self._ediscovery_clients_obj = EdiscoveryClients(self._commcell_object, self)
        self._ediscovery_ds_obj = EdiscoveryDataSources(self._commcell_object, self)
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get(self, server_name):
        """returns the FsoServer object for given server name

                Args:

                    server_name         (str)       --  Name of the server

                Returns:

                    obj --  Instance of FsoServer Class

                Raises:

                    SDKException:

                            if failed to find server in FSO App

                            if input is not valid

        """
        if not isinstance(server_name, str):
            raise SDKException('FileStorageOptimization', '101')
        if not self.has_server(server_name):
            raise SDKException('FileStorageOptimization', '103')
        server_id = self._fso_servers[server_name.lower()]['clientEntity']['clientId']
        return FsoServer(commcell_object=self._commcell_object, server_name=server_name, server_id=server_id)

    def _get_all_fso_servers(self):
        """Returns all the FSO servers found in the commcell

                Args:

                    None

                Returns:

                    dict        --  Containing FSO server details

                Raises;

                    SDKException:

                            if failed to get FSO servers details

                            if response is empty

                            if response is not success
        """
        return self._ediscovery_clients_obj.get_ediscovery_clients()

    def refresh(self):
        """Refresh the FSO Servers associated with the commcell."""
        self._fso_servers = self._get_all_fso_servers()

    def add_file_server(self, server_name, data_source_name, inventory_name, plan_name,
                        source_type=EdiscoveryConstants.SourceType.BACKUP, **kwargs):
        """Adds file system FSO server

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

                    access_node         (str)       --  server name which needs to be used as access node
                                                            in case if server to be added is not a commvault client

                    country_name        (str)       --  country name where server is located (default : USA)

                    country_code        (str)       --  Country code (ISO 3166 2-letter code)

                    credential_name     (name)       --  Credential name for unc crawl path access

                    enable_monitoring   (str)       --  specifies whether to enable file monitoring or not for this


                Returns:

                    obj     --  Instance of FSOServer class

                Raises:

                      SDKException:

                            if plan/inventory/index server doesn't exists

                            if failed to add FSO server data source
        """
        self._ediscovery_ds_obj.add_fs_data_source(
            server_name=server_name,
            data_source_name=data_source_name,
            inventory_name=inventory_name,
            plan_name=plan_name,
            source_type=source_type,
            **kwargs)
        is_commvault_client = self._commcell_object.clients.has_client(server_name)
        server_id = 0
        if not is_commvault_client:
            all_clients = self._commcell_object.clients.all_clients
            for client_name, client_details in all_clients.items():
                if client_name.lower().startswith(f"{data_source_name.lower()}_"):
                    server_id = client_details['id']
                    break
        else:
            server_id = self._commcell_object.clients.get(server_name).client_id
        return FsoServer(commcell_object=self._commcell_object, server_name=server_name,
                         server_id=server_id)

    def has_server(self, server_name):
        """Checks if a server exists in the commcell with the input name for FSO or not

            Args:
                server_name (str)  --  name of the server

            Returns:
                bool - boolean output whether the FSO Server exists in the commcell or not

            Raises:
                SDKException:
                    if type of the server name argument is not string

        """
        if not isinstance(server_name, str):
            raise SDKException('FileStorageOptimization', '101')
        return self._fso_servers and server_name.lower() in self._fso_servers


class FsoServer():
    """Class to represent single FSO Server in the commcell"""

    def __init__(self, commcell_object, server_name, server_id=None):
        """Initializes an instance of the FsoServer class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                server_name         (str)       --  Name of the server

                server_id           (int)       --  server client id

            Returns:
                object  -   instance of the FsoServer class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._server_name = server_name
        self._server_id = None
        self._server_props = None
        self._schedule_obj = None
        self._CREATE_POLICY = self._services['CREATE_UPDATE_SCHEDULE_POLICY']
        if server_id:
            self._server_id = server_id
        else:
            self._server_id = self._commcell_object.activate.file_storage_optimization().get(server_name).server_id
        self._ediscovery_client_ops = EdiscoveryClientOperations(self._commcell_object, self)
        self._ediscovery_data_srcs_obj = EdiscoveryDataSources(self._commcell_object, self)
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def start_collection(self):
        """Starts collection job on all data sources associated with this server

                Args:

                    None

                Return:

                    list    --  List of jobid's

                Raises:

                    SDKException:

                            if failed to start collection job

        """
        request_json = copy.deepcopy(EdiscoveryConstants.START_CRAWL_SERVER_REQUEST_JSON)
        request_json['taskInfo']['associations'][0]['clientId'] = self._server_id
        request_json['taskInfo']['task'][
            'taskName'] = f"Cvpysdk_FSO_server_Crawl_{self._server_name}_{int(time.time())}"
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_POLICY, request_json
        )
        output = []
        if flag:
            if response.json() and 'jobIds' in response.json():
                for node in response.json()['jobIds']:
                    output.append(node)
                return output
            raise SDKException('FileStorageOptimization', '105')
        self._response_not_success(response)

    def _get_schedule_object(self):
        """returns the schedule object for associated schedule for this fso server

            Args:
                None

            Returns:

                obj --  Instance of Schedule class

                None -- if no schedule exists

            Raises:

                SDKException:

                        if failed to find schedule details associated with this server
        """
        scd_obj = Schedules(self)
        if scd_obj.has_schedule():
            return scd_obj.get()
        return None

    def _get_server_properties(self):
        """gets FSO server details from the commcell

                Args:

                    None

                Returns:

                    dict    --  Containing FSO Server details

                Raises:

                     Raises;

                        SDKException:

                            if failed to get server details

        """
        self._ediscovery_data_srcs_obj.refresh()  # do refresh before fetching so that doc count comes up fine
        return self._ediscovery_data_srcs_obj.ediscovery_client_props

    def search(self, criteria=None, attr_list=None, params=None):
        """do searches on data source and returns document details

            Args:

                criteria        (str)      --  containing criteria for query
                                                    (Default : None - returns all docs)

                                                    Example :

                                                        Size:[10 TO 1024]
                                                        FileName:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                params          (dict)     --  Any other params which needs to be passed
                                                   Example : { "start" : "0" }

            Returns:

                int,list(dict),dict    --  Containing document count, document details & facet details(if any)

            Raises:

                SDKException:

                        if failed to perform search

        """
        return self._ediscovery_client_ops.search(criteria=criteria, attr_list=attr_list, params=params)

    def add_schedule(self, schedule_name, pattern_json):
        """Creates the schedule and associate it with server

                        Args:

                            schedule_name       (str)       --  Schedule name

                            pattern_json        (dict)      --  Schedule pattern dict
                                                                (Refer to Create_schedule_pattern in schedule.py)

                        Raises:

                              SDKException:

                                    if input is not valid

                                    if failed to create schedule

        """
        self._ediscovery_client_ops.schedule(schedule_name=schedule_name, pattern_json=pattern_json)
        self.refresh()

    def delete_schedule(self):
        """Deletes the schedule associated with server

                        Args:

                            None

                        Raises:

                              SDKException:

                                    if failed to Delete schedule

        """
        if not self._schedule_obj:
            raise SDKException('FileStorageOptimization', '102', "No schedule is associated to this FSO Server")
        Schedules(self).delete()
        self.refresh()

    def share(self, user_or_group_name, allow_edit_permission=False, is_user=True, ops_type=1):
        """Shares Fso server with given user or user group in commcell

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
        return self._ediscovery_client_ops.share(
            user_or_group_name=user_or_group_name,
            allow_edit_permission=allow_edit_permission,
            is_user=is_user,
            ops_type=ops_type)

    def refresh(self):
        """Refresh the FSO Server details"""
        self._server_props = self._get_server_properties()
        self._schedule_obj = self._get_schedule_object()

    @property
    def schedule(self):
        """returns the schedule object for associated schedule

                Returns:

                    obj     --  Instance of Schedule Class if schedule exists

                    None    --  If no schedule exists

        """
        return self._schedule_obj

    @property
    def server_id(self):
        """returns the server id

            Returns:

                int --  Server id

        """
        return self._server_id

    @property
    def server_details(self):
        """returns the server details

            Returns:

                dict --  Server details

        """
        return self._server_props

    @property
    def data_sources_name(self):
        """returns the associated data sources to this FSO server

            Returns:

                list --  names of data sources

        """
        return self._ediscovery_data_srcs_obj.data_sources

    @property
    def data_sources(self):
        """returns the EdiscoveryDataSources object associated to this server

            Returns:

                obj --  Instance of EdiscoveryDataSources Object

        """
        return self._ediscovery_data_srcs_obj

    @property
    def total_data_sources(self):
        """returns the total number of data sources associated with this server

            Returns:

                int --  total number of data sources

        """
        return len(self._ediscovery_data_srcs_obj.data_sources)

    @property
    def total_doc_count(self):
        """returns the total document count of all data sources for this server

            Returns:

                int --  Total crawled document count

        """
        return self._ediscovery_data_srcs_obj.total_documents


class FsoServerGroups():
    """Class for representing all FSO server groups in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the FsoServerGroups class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the FsoServerGroups class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._fso_server_groups = None
        self._ediscovery_clients_obj = EdiscoveryClients(self._commcell_object, self)
        self._ediscovery_ds_obj = EdiscoveryDataSources(self._commcell_object, self)
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_all_fso_server_groups(self):
        """Returns all the FSO server groups found in the commcell

                Args:

                    None

                Returns:

                    dict        --  Containing FSO server group details

                Raises;

                    SDKException:

                            if failed to get FSO server group details

                            if response is empty

                            if response is not success
        """
        return self._ediscovery_clients_obj.get_ediscovery_clients()

    def refresh(self):
        """Refresh the FSO Server groups associated with the commcell."""
        self._fso_server_groups = self._get_all_fso_server_groups()

    def add_server_group(self, server_group_name, inventory_name, plan_name, **kwargs):
        """adds server group to FSO

                Args:

                    server_group_name       (str)       --      Server group name

                    inventory_name          (str)       --  Inventory name which needs to be associated

                    plan_name               (str)       --  Plan name which needs to be associated with this data source

                 Kwargs Arguments:

                    country_name        (str)       --  country name where server is located (default: USA)

                    country_code        (str)       --  Country code (ISO 3166 2-letter code)

                Returns:

                    obj     --  Instance of FSOServerGroup class

                Raises:

                      SDKException:

                            if plan/inventory/index server doesn't exists

                            if failed to add FSO server group

        """
        self._ediscovery_ds_obj.add_fs_data_source(
            server_name=server_group_name,
            data_source_name=server_group_name,
            inventory_name=inventory_name,
            plan_name=plan_name,
            **kwargs)
        return FsoServerGroup(
            self._commcell_object,
            server_group_name,
            server_id=self._commcell_object.client_groups.get(server_group_name).clientgroup_id)

    def has(self, server_group_name):
        """Checks if a server group exists in the commcell with the input name for FSO or not

            Args:
                server_group_name (str)  --  name of the server group

            Returns:
                bool - boolean output whether the FSO Server group exists in the commcell or not

            Raises:
                SDKException:
                    if type of the server group name argument is not string

        """
        if not isinstance(server_group_name, str):
            raise SDKException('FileStorageOptimization', '101')
        return self._fso_server_groups and server_group_name.lower() in self._fso_server_groups

    def get(self, server_grp_name):
        """returns the FsoServerGroup object for given server group name

                Args:

                    server_grp_name         (str)       --  Name of the server group

                Returns:

                    obj --  Instance of FsoServerGroup Class

                Raises:

                    SDKException:

                            if failed to find server group in FSO App

                            if input is not valid

        """
        if not isinstance(server_grp_name, str):
            raise SDKException('FileStorageOptimization', '101')
        if not self.has(server_grp_name):
            raise SDKException('FileStorageOptimization', '106')
        server_id = self._fso_server_groups[server_grp_name.lower()]['clientEntity']['clientId']
        return FsoServerGroup(
            commcell_object=self._commcell_object,
            server_group_name=server_grp_name,
            server_id=server_id)


class FsoServerGroup():
    """Class to represent single FSO Server group in the commcell"""

    def __init__(self, commcell_object, server_group_name, server_id=None):
        """Initializes an instance of the FsoServerGroup class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the FsoServerGroup class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._server_group_name = server_group_name
        self._server_id = None
        self._server_grp_props = None
        self._server_names = []
        self._total_doc = 0
        self._CREATE_POLICY = self._services['CREATE_UPDATE_SCHEDULE_POLICY']
        if server_id:
            self._server_id = server_id
        else:
            self._server_id = self._commcell_object.activate.file_storage_optimization(
                FsoTypes.SERVER_GROUPS).get(server_group_name).server_group_id
        self._ediscovery_clients_obj = EdiscoveryClients(self._commcell_object, self)
        self._ediscovery_client_ops = EdiscoveryClientOperations(self._commcell_object, self)
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_server_group_properties(self):
        """gets FSO server group details from the commcell

                Args:

                    None

                Returns:

                    dict    --  Containing FSO Server group details

                Raises:

                     Raises;

                        SDKException:

                            if failed to get server group details

        """
        client_resp = self._ediscovery_clients_obj.get_ediscovery_clients()
        grp_resp = self._ediscovery_clients_obj.get_ediscovery_client_group_details()
        if 'nodeList' in grp_resp:
            grp_resp = grp_resp['nodeList'][0]
            if 'childs' in grp_resp and 'customProperties' in grp_resp['childs'][0]:
                name_value_dict = grp_resp['childs'][0]['customProperties']['nameValues']
                for prop in name_value_dict:
                    prop_name = prop.get('name')
                    if prop_name == EdiscoveryConstants.FIELD_DOCUMENT_COUNT:
                        self._total_doc = int(prop.get('value'))
                        break
        self._server_names = []
        for key, value in client_resp.items():
            self._server_names.append(key)
        return client_resp

    def has_server(self, server_name):
        """Checks if a server exists in the FSO Server group with the input name or not

            Args:
                server_name (str)  --  name of the server

            Returns:
                bool - boolean output whether the FSO Server exists in the server group or not

            Raises:
                SDKException:
                    if type of the server name argument is not string

        """
        if not isinstance(server_name, str):
            raise SDKException('FileStorageOptimization', '101')
        return self._server_grp_props and server_name.lower() in self._server_grp_props

    def start_collection(self):
        """Starts collection job on all servers associated with this server group

                Args:

                    None

                Return:

                    list    --  List of jobid's

                Raises:

                    SDKException:

                            if failed to start collection job

        """
        request_json = copy.deepcopy(EdiscoveryConstants.START_CRAWL_SERVER_REQUEST_JSON)
        # delete clientid key and add client group level key and entity type
        del request_json['taskInfo']['associations'][0]['clientId']
        request_json['taskInfo']['associations'][0]['clientGroupId'] = self._server_id
        request_json['taskInfo']['associations'][0]['_type_'] = 28  # server group level job collection
        request_json['taskInfo']['task'][
            'taskName'] = f"Cvpysdk_FSO_server_Crawl_{self._server_group_name}_{int(time.time())}"
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_POLICY, request_json
        )
        output = []
        if flag:
            if response.json() and 'jobIds' in response.json():
                for node in response.json()['jobIds']:
                    output.append(node)
                return output
            raise SDKException('FileStorageOptimization', '107')
        self._response_not_success(response)

    def search(self, criteria=None, attr_list=None, params=None):
        """do searches on client group data and returns document details

            Args:

                criteria        (str)      --  containing criteria for query
                                                    (Default : None - returns all docs)

                                                    Example :

                                                        Size:[10 TO 1024]
                                                        FileName:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                params          (dict)     --  Any other params which needs to be passed
                                                   Example : { "start" : "0" }

            Returns:

                int,list(dict),dict    --  Containing document count, document details & facet details(if any)

            Raises:

                SDKException:

                        if failed to perform search

        """
        return self._ediscovery_client_ops.search(criteria=criteria, attr_list=attr_list, params=params)

    def get(self, server_name):
        """returns the FsoServer object for given server name

                Args:

                    server_name         (str)       --  Name of the server

                Returns:

                    obj --  Instance of FsoServer Class

                Raises:

                    SDKException:

                            if failed to find server in FSO server group

                            if input is not valid

        """
        if not isinstance(server_name, str):
            raise SDKException('FileStorageOptimization', '101')
        if not self.has_server(server_name):
            raise SDKException('FileStorageOptimization', '103')
        server_id = self._server_grp_props[server_name.lower()]['clientEntity']['clientId']
        return FsoServer(commcell_object=self._commcell_object, server_name=server_name, server_id=server_id)

    def refresh(self):
        """Refresh the FSO Server group details"""
        self._server_grp_props = self._get_server_group_properties()

    @property
    def server_group_id(self):
        """returns the client group id

            Returns:

                int --  Server group id

        """
        return self._server_id

    @property
    def server_group_props(self):
        """returns the server group properties

            Returns:

                dict --  Server group details

        """
        return self._server_grp_props

    @property
    def server_list(self):
        """returns the list of server which is part of this server group

            Returns:

                list --  Server names

        """
        return self._server_names

    @property
    def total_documents(self):
        """returns the total documents count for this server group

            Returns:

                int --  Total document count for this server group

        """
        return self._total_doc
