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

"""Main file for performing operations on Sensitive data governance(SDG) app under Activate.

'Projects' & 'Project' are 2 classes defined in this file

Projects:   Class to represent all SDG projects in the commcell

Project:    Class to represent single SDG project in the commcell

Projects:

    __init__()                          --  initialise object of the Projects class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_all_projects()                --  gets all the Projects from the SDG

     refresh()                          --  refresh the projects associated with the SDG

     has_project()                      --  checks whether given project name exists in SDG or not

     get()                              --  returns the Project class object for given project name

     add()                              --  adds project to the SDG

     delete()                           --  deletes project from the SDG

Project:

     __init__()                         --  initialise object of the Project class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_project_details()             --  returns the project properties

     _get_schedule_object()             --  returns the schedule object for associated project schedule

     refresh()                          --  refresh the project details

     add_fs_data_source()               --  adds file system data source to project

     delete_schedule()                  --  deletes schedule for this project

     add_schedule()                     --  creates schedule for this project

     share()                            --  shares project with given user name or group name

     search()                           --  returns the search response containing document details from project


Project Attributes
--------------------

    **project_id**              --  returns the id of the project

    **project_details**         --  returns the project properties

    **data_sources_name**       --  returns the list of data sources associated with this project

    **data_sources**            --  returns the EdiscoveryDataSources object for this project

    **total_data_sources**      --  returns total no of data sources associated with this project

    **project_name**            --  returns the name of the project

    **schedule**                --  returns the schedule object for associated project schedule

    **sensitive_files_count**   --  returns the total sensitive files count

"""

from ..schedules import Schedules

from ..activateapps.constants import EdiscoveryConstants

from ..activateapps.ediscovery_utils import EdiscoveryClients, EdiscoveryClientOperations, EdiscoveryDataSources

from ..exception import SDKException


class Projects():
    """Class for representing all SDG Projects in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the Projects class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the Projects class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._sdg_projects = None
        self._ediscovery_clients_obj = EdiscoveryClients(self._commcell_object, self)
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_all_sdg_projects(self):
        """Returns all the SDG Projects found in the commcell

                Args:

                    None

                Returns:

                    dict        --  Containing SDG Project details

                Raises;

                    SDKException:

                            if failed to get SDG Project details

                            if response is empty

                            if response is not success
        """
        return self._ediscovery_clients_obj.get_ediscovery_projects()

    def refresh(self):
        """Refresh the SDG Projects associated with the commcell."""
        self._sdg_projects = self._get_all_sdg_projects()

    def delete(self, project_name):
        """Deletes project from SDG

                Args:

                    project_name        (str)       --  Name of the project

                Returns:

                    None

                Raises:

                    SDKException:

                            if input is not valid

                            if failed to delete project

                            if response is empty or not success
        """
        if not self.has_project(project_name):
            raise SDKException('SensitiveDataGovernance', '102', "Project doesn't exists in SDG")
        project_id = self._sdg_projects[project_name.lower()]['clientId']
        self._ediscovery_clients_obj.delete(client_id=project_id)
        self.refresh()

    def add(self, project_name, inventory_name, plan_name):
        """Adds project to the SDG

                Args:

                    project_name        (str)       --  Name of the project

                    inventory_name      (str)       --  Name of inventory

                    plan_name           (str)       --  Plan name to associate with this project

                Returns:

                    obj --  Instance of Project class

                Raises:

                    SDKException:

                            if input is not valid

                            if failed to create project

                            if response is empty or not success
        """
        client_id = self._ediscovery_clients_obj.add(
            client_name=project_name,
            inventory_name=inventory_name,
            plan_name=plan_name)
        if client_id == 0:
            raise SDKException('SensitiveDataGovernance', '102', 'Failed to add project to SDG')
        self.refresh()
        return Project(commcell_object=self._commcell_object, project_name=project_name, project_id=client_id)

    def has_project(self, project_name):
        """Checks if a project exists in the commcell with the input name for SDG or not

            Args:
                project_name (str)  --  name of the project

            Returns:
                bool - boolean output whether the SDG Project exists in the commcell or not

            Raises:
                SDKException:
                    if type of the project name argument is not string

        """
        if not isinstance(project_name, str):
            raise SDKException('SensitiveDataGovernance', '101')
        return self._sdg_projects and project_name.lower() in self._sdg_projects

    def get(self, project_name):
        """returns the Project object for given project name

                Args:

                    project_name         (str)       --  Name of the project

                Returns:

                    obj --  Instance of Project Class

                Raises:

                    SDKException:

                            if failed to find Project in SDG

                            if input is not valid

        """
        if not isinstance(project_name, str):
            raise SDKException('SensitiveDataGovernance', '101')
        if not self.has_project(project_name):
            raise SDKException('SensitiveDataGovernance', '103')
        project_id = self._sdg_projects[project_name.lower()]['eDiscoveryClient']['clientId']
        return Project(commcell_object=self._commcell_object, project_name=project_name, project_id=project_id)


class Project():
    """Class to represent single SDG Project in the commcell"""

    def __init__(self, commcell_object, project_name, project_id=None):
        """Initializes an instance of the Project class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                project_name        (str)       --  name of the project

                project_id          (int)       --  project's pseudoclient id

            Returns:
                object  -   instance of the Project class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._project_name = project_name
        self._project_id = None
        self._project_props = None
        self._schedule_obj = None
        if project_id:
            self._project_id = project_id
        else:
            self._project_id = self._commcell_object.activate.sensitive_data_governance().get(project_name).project_id
        self._ediscovery_data_srcs_obj = EdiscoveryDataSources(self._commcell_object, self)
        self._ediscovery_client_ops = EdiscoveryClientOperations(self._commcell_object, self)
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_project_details(self):
        """gets SDG Project details from the commcell

                Args:

                    None

                Returns:

                    dict    --  Containing project details

                Raises:

                     Raises;

                        SDKException:

                            if failed to get project details

        """
        return self._ediscovery_data_srcs_obj.ediscovery_client_props

    def _get_schedule_object(self):
        """returns the schedule object for associated project schedule

            Args:
                None

            Returns:

                obj --  Instance of Schedule class

                None -- if no schedule exists

            Raises:

                SDKException:

                        if failed to find schedule details associated with this project
        """
        scd_obj = Schedules(self)
        if scd_obj.has_schedule():
            return scd_obj.get()
        return None

    def refresh(self):
        """Refresh the SDG project details"""
        self._project_props = self._get_project_details()
        self._schedule_obj = self._get_schedule_object()

    def add_schedule(self, schedule_name, pattern_json):
        """Creates the schedule and associate it with project

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
        """Deletes the schedule associated with project

                        Args:

                            None

                        Raises:

                              SDKException:

                                    if failed to Delete schedule

        """
        if not self._schedule_obj:
            raise SDKException('SensitiveDataGovernance', '102', "No schedule is associated to this SDG Project")
        Schedules(self).delete()
        self.refresh()

    def search(self, criteria=None, attr_list=None, params=None):
        """do searches on entire project and returns document details

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

    def share(self, user_or_group_name, allow_edit_permission=False, is_user=True, ops_type=1):
        """Shares project with given user or user group in commcell

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

    def add_fs_data_source(self, server_name, data_source_name,
                           source_type=EdiscoveryConstants.SourceType.BACKUP, **kwargs):
        """Adds file system data source to project

                Args:

                    server_name         (str)       --  Server name which needs to be added

                    data_source_name    (str)       --  Name for data source

                    source_type         (enum)      --  Source type for crawl (Live source or Backedup)
                                                                Refer EdiscoveryConstants.SourceType

                Kwargs Arguments:

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

                Raises:

                      SDKException:

                            if plan/inventory/index server doesn't exists

                            if failed to add FS data source
        """
        inventory_name = self.project_details['inventoryDataSource']['seaDataSourceName']
        plan_name = self.project_details['plan']['planName']
        return self._ediscovery_data_srcs_obj.add_fs_data_source(
            server_name=server_name,
            data_source_name=data_source_name,
            inventory_name=inventory_name,
            plan_name=plan_name,
            source_type=source_type,
            **kwargs)

    @property
    def project_id(self):
        """returns the project psuedoclient id

                Returns:

                    int --  Pseudoclient id associated with this project

        """
        return self._project_id

    @property
    def project_name(self):
        """returns the project name

                Returns:

                    str --  project name

        """
        return self._project_name

    @property
    def project_details(self):
        """returns the project properties

            Returns:

                dict    --  Containing project properties

        """
        return self._project_props

    @property
    def data_sources_name(self):
        """returns the associated data sources to this project

            Returns:

                list --  names of data sources

        """
        return self._ediscovery_data_srcs_obj.data_sources

    @property
    def total_data_sources(self):
        """returns the total number of data sources associated with this project

            Returns:

                int --  total number of data sources

        """
        return len(self._ediscovery_data_srcs_obj.data_sources)

    @property
    def data_sources(self):
        """returns the EdiscoveryDataSources object associated to this project

            Returns:

                obj --  Instance of EdiscoveryDataSources Object

        """
        return self._ediscovery_data_srcs_obj

    @property
    def schedule(self):
        """returns the schedule object for associated schedule

                Returns:

                    obj     --  Instance of Schedule Class if schedule exists

                    None    --  If no schedule exists

        """
        return self._schedule_obj

    @property
    def sensitive_files_count(self):
        """returns the total sensitive files count on this project

            Returns:

                int --  Sensitive files count

        """
        count, _, _ = self.search(criteria=EdiscoveryConstants.CRITERIA_EXTRACTED_DOCS,
                                  params={"rows":"0"})
        return count
