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

"""File for performing Workflow related operations on Commcell.

WorkFlows and WorkFlow are the two classes defined in this file.

WorkFlows:   Class for representing all the workflows associated with the commcell

Workflow:    Class for a single workflow of the commcell

WorkFlows:

    __init__(commcell_object)           --  initialize instance of the WorkFlow class

    __str__()                           --  returns all the workflows associated with the commcell

    __repr__()                          --  returns all the workflows deployed in the commcell

    __len__()                           --  returns the number of workflows associated with the Commcell

    __getitem__()                       --  returns the name of the workflow for the given WF ID
                                                or the details for the given workflow name

    _get_workflows()                    --  gets all the workflows deployed on the commcell

    _get_activities()                   --  gets all the workflow activities deployed
                                                on the commcell

    has_workflow(workflow_name)         --  checks if the workflow exists with given name or not

    has_activity(activity_name)         --  checks if the workflow activity exists with given name
                                                or not

    import_workflow(workflow_xml)       --  imports a workflow to the Commcell

    import_activity(activity_xml)       --  imports a workflow activity to the Commcell

    download_workflow_from_store()      --  downloads given workflow from the cloud.commvault.com

    get()                               --  returns the instance of a specific workflow on commcell

    delete_workflow()                   --  deletes a workflow from the commcell

    refresh()                           --  refresh the workflows added to the Commcell

    refresh_activities()                --  refresh the workflow activities added to the commcell

    get_interaction_properties()        --  Returns a workflow interaction properties to the user

    submit_initeraction()               --  Submits a given interaction with specified action

    all_interactions()                  --  Returns all interactive interactions for workflows on commcell

    @Property
    all_workflows                       --  returns all workflows on Commcell

    all_activities                      --  returns all activities on Commcell


Workflow:

    @Private Modules
    _read_inputs()                      --  gets the values for a workflow input

    _get_workflow_id()                  --  Get Workflow id

    _read_inputs()                      --  Gets the values from the user for a workflow input.

    _set_workflow_properties()          --  Sets Workflow properties

    _get_workflow_properties()          --  Get workflow properties

    _get_workflow_definition()          --  Get workflow definition properties

    @Class Modules
    set_workflow_configuration()        --  Set workflow configuration

    approve_workflow()                  --  Approves the workflow change requested by different user

    get_authorizations()                --  Get authorizations/approvals for the workflow

    enable()                            --  Enables the workflow

    disable()                           --  Disables the workflow

    deploy_workflow()                   --  Deploys a workflow to the Commcell

    execute_workflow()                  --  Executes a workflow and returns the job instance

    export_workflow()                   --  Exports a workflow and returns the workflow xml path

    clone_workflow()                    --  Clones the workflow

    schedule_workflow()                 --  Creates a schedule for the workflow

    _process_workflow_schedule_response -- processes the response received schedule creation request

    refresh()                           --  Refreshes the workflow properties

    @Property
    workflow_name                       -- Returns workflow name

    workflow_id                         -- Returns workflow id

    workflow_description                -- Returns workflow description

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from base64 import b64decode
from xml.parsers.expat import ExpatError

import os
import xmltodict

from .job import Job
from .exception import SDKException
from .schedules import Schedule
from typing import Any, Dict, List, Optional, Union

class WorkFlows(object):
    """
    Manages all workflows and activities associated with a Commcell.

    The WorkFlows class provides a comprehensive interface for interacting with workflows and activities
    within a Commcell environment. It allows users to query, import, download, delete, and refresh workflows
    and activities, as well as manage interactions and retrieve their properties.

    Key Features:
        - Retrieve and list all workflows and activities
        - Check existence of specific workflows and activities
        - Import workflows and activities from XML definitions
        - Download workflows from the workflow store with authentication
        - Access workflow and activity details using indexing and property access
        - Delete workflows by name
        - Refresh workflow and activity lists to reflect latest changes
        - Manage and submit interactions, and retrieve their properties
        - Provides string representation, length, and item access for workflows

    Attributes:
        all_workflows (property): Returns all available workflows.
        all_activities (property): Returns all available activities.

    Usage:
        Instantiate with a Commcell object to manage workflows and activities for that Commcell.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a WorkFlows instance for managing workflow-related operations.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> workflows = WorkFlows(commcell)
            >>> print("WorkFlows instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._WORKFLOWS = self._services['GET_WORKFLOWS']
        self._INTERACTIONS = self._services['GET_INTERACTIONS']
        self._INTERACTION = self._services['GET_INTERACTION']

        self._workflows = None
        self._activities = None

        self.refresh()
        self.refresh_activities()

    def __str__(self) -> str:
        """Return a string representation of all workflows associated with the Commcell.

        This method provides a human-readable summary of all workflows managed by the WorkFlows object.

        Returns:
            A string listing all workflows associated with the Commcell.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> print(str(workflows))
            >>> # Output will display a summary of all workflows in the Commcell

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^50}\t{:^60}\t{:^30}\n\n'.format(
            'S. No.', 'Workflow Name', 'Description', 'Client'
        )

        for index, workflow in enumerate(self._workflows):
            workflow_vals = self._workflows[workflow]
            workflow_desciption = workflow_vals.get('description', '')

            if 'client' in workflow_vals:
                workflow_client = workflow_vals['client']
            else:
                workflow_client = "  --  "

            sub_str = '{:^5}\t{:50}\t{:60}\t{:^30}\n'.format(
                index + 1,
                workflow,
                workflow_desciption,
                workflow_client
            )

            representation_string += sub_str

            if 'inputs' in workflow_vals and workflow_vals['inputs'] != []:
                workflow_inputs = workflow_vals['inputs']

                sub_str = '\n\t\tWorkFlow Inputs:\n\n'

                sub_str += '\t\t{:^5}\t{:^35}\t{:^35}\t{:^70}\t{:^20}\t{:^20}\n\n'.format(
                    'S. No.',
                    'Input Name',
                    'Display Name',
                    'Description',
                    'Default Value',
                    'Is Required'
                )

                for index1, wf_input in enumerate(workflow_inputs):
                    input_name = wf_input['input_name']
                    is_required = wf_input['is_required']

                    if wf_input['display_name'] is None:
                        display_name = '  ----  '
                    else:
                        display_name = wf_input['display_name']

                    if wf_input['documentation'] is None:
                        description = '  ----  '
                    else:
                        description = wf_input['documentation']

                    if wf_input['default_value'] is None:
                        default_value = '  ----  '
                    else:
                        default_value = wf_input['default_value']

                    sub_str += '\t\t{:^5}\t{:35}\t{:35}\t{:70}\t{:20}\t{:^20}\n'.format(
                        index1 + 1,
                        input_name,
                        display_name,
                        description,
                        default_value,
                        str(bool(is_required))
                    )

                    sub_str += '\n'

                representation_string += sub_str

            representation_string += "\n\n"

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the WorkFlows instance.

        This method provides a developer-friendly string that represents the current
        WorkFlows object, useful for debugging and logging purposes.

        Returns:
            A string representation of the WorkFlows instance.

        Example:
            >>> workflows = WorkFlows()
            >>> print(repr(workflows))
            <WorkFlows object at 0x7f8b2c3e2d30>
        #ai-gen-doc
        """
        return "WorkFlow class instance for Commcell"

    def __len__(self) -> int:
        """Return the number of workflows associated with the Commcell.

        Returns:
            The total count of workflows managed by this WorkFlows instance.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> num_workflows = len(workflows)
            >>> print(f"Total workflows: {num_workflows}")

        #ai-gen-doc
        """
        return len(self.all_workflows)

    def __getitem__(self, value: 'Union[str, int]') -> 'Union[str, dict]':
        """Retrieve workflow information by name or ID.

        If a workflow ID (int) is provided, returns the name of the workflow.
        If a workflow name (str) is provided, returns a dictionary with workflow details.

        Args:
            value: The name (str) or ID (int) of the workflow to retrieve.

        Returns:
            str: The name of the workflow if an ID is provided.
            dict: A dictionary containing workflow details if a name is provided.

        Raises:
            IndexError: If no workflow exists with the given name or ID.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> # Get workflow name by ID
            >>> name = workflows[101]
            >>> print(f"Workflow name: {name}")
            >>>
            >>> # Get workflow details by name
            >>> details = workflows['MyWorkflow']
            >>> print(f"Workflow details: {details}")

        #ai-gen-doc
        """
        value = str(value)

        if value in self.all_workflows:
            return self.all_workflows[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_workflows.items())
                )[0][0]
            except IndexError:
                raise IndexError('No workflow exists with the given Name / Id')

    def _get_workflows(self) -> dict:
        """Retrieve all workflows associated with the Commcell.

        Returns:
            dict: A dictionary containing all workflows present in the Commcell.

        Raises:
            SDKException: If the response from the Commcell is empty or not successful.

        Example:
            >>> workflows = workflows_obj._get_workflows()
            >>> print(f"Total workflows found: {len(workflows)}")
            >>> # Access workflow details by iterating over the dictionary
            >>> for workflow_name, workflow_info in workflows.items():
            ...     print(f"Workflow: {workflow_name}, Info: {workflow_info}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._WORKFLOWS)

        if flag:
            if response.json() and 'container' in response.json():
                workflow_dict = {}

                for workflow in response.json()['container']:
                    workflow_name = workflow['entity']['workflowName'].lower()
                    workflow_id = str(workflow['entity']['workflowId'])
                    workflow_description = workflow.get('description', '')

                    if 'deployments' in workflow:
                        workflow_client = workflow['deployments'][0]['client']['clientName']

                        if 'entries' in workflow['deployments'][0]['inputForm']:
                            workflow_inputs = []

                            for a_input in workflow['deployments'][0]['inputForm']['entries']:
                                workflow_input = {}

                                workflow_input['input_name'] = a_input.get('inputName')
                                workflow_input['display_name'] = a_input.get('displayName')
                                workflow_input['documentation'] = a_input.get('documentation')
                                workflow_input['default_value'] = a_input.get('defaultValue')
                                workflow_input['is_required'] = a_input.get('required', False)

                                workflow_inputs.append(workflow_input)
                        else:
                            workflow_inputs = []

                        workflow_dict[workflow_name] = {
                            'description': workflow_description,
                            'client': workflow_client,
                            'id': workflow_id,
                            'inputs': workflow_inputs
                        }
                    else:
                        workflow_dict[workflow_name] = {
                            'description': workflow_description,
                            'id': workflow_id,
                        }

                return workflow_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_activities(self) -> dict:
        """Retrieve all workflow activities associated with the Commcell.

        Returns:
            dict: A dictionary containing all activities present in the Commcell.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> activities = workflows._get_activities()
            >>> print(f"Number of activities: {len(activities)}")
            >>> # Access activity details by key
            >>> for activity_name, activity_info in activities.items():
            ...     print(f"Activity: {activity_name}, Info: {activity_info}")

        #ai-gen-doc
        """

        request_xml = "<Workflow_GetActivitiesRequest/>"

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json() and 'activities' in response.json():
                activities_dict = {}

                for activity in response.json()['activities']:
                    name = activity['activity']['activityName'].lower()
                    activity_id = str(activity['activity']['schemaId'])
                    description = activity.get('description')
                    activities_dict[name] = {
                        'description': description,
                        'id': activity_id,
                    }

                return activities_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def has_workflow(self, workflow_name: str) -> bool:
        """Check if a workflow with the specified name exists in the Commcell.

        Args:
            workflow_name: The name of the workflow to check for existence.

        Returns:
            True if the workflow exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the workflow_name argument is not a string.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> exists = workflows.has_workflow("DailyBackup")
            >>> print(f"Workflow exists: {exists}")
            # Output: Workflow exists: True

        #ai-gen-doc
        """
        if not isinstance(workflow_name, str):
            raise SDKException('Workflow', '101')

        return self._workflows and workflow_name.lower() in self._workflows

    def has_activity(self, activity_name: str) -> bool:
        """Check if a workflow activity with the specified name exists in the Commcell.

        Args:
            activity_name: The name of the workflow activity to check.

        Returns:
            True if the workflow activity exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the activity_name argument is not a string.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> exists = workflows.has_activity("DataBackup")
            >>> print(f"Activity exists: {exists}")
            # Output: Activity exists: True

        #ai-gen-doc
        """
        if not isinstance(activity_name, str):
            raise SDKException('Workflow', '101')

        return self._activities and activity_name.lower() in self._activities

    def import_workflow(self, workflow_xml: str) -> None:
        """Import a workflow into the Commcell from an XML file or XML string.

        This method imports a workflow definition to the Commcell. The input can be either:
          - The path to a local XML file containing the workflow definition, or
          - A string containing the XML contents of the workflow.

        If a valid file path is provided, the file is read and its contents are used for import.
        Otherwise, the provided string is used directly as the workflow XML.

        Args:
            workflow_xml: Path to the workflow XML file or the XML content as a string.

        Raises:
            SDKException: If the input is not a string, if the XML is invalid or the file path is incorrect,
                or if the workflow import fails due to an HTTP error.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> # Import from a file path
            >>> workflows.import_workflow('/path/to/workflow.xml')
            >>> # Import from XML string
            >>> xml_content = '<WorkflowDefinition>...</WorkflowDefinition>'
            >>> workflows.import_workflow(xml_content)

        #ai-gen-doc
        """
        # Added a check for bytes input and decoding it using UTF-8, previously failing the str check
        # making it compatible if the user passes bytes object using ET.tostring() method
        if isinstance(workflow_xml, bytes):
            try:
                workflow_xml = workflow_xml.decode('utf-8')
            except UnicodeDecodeError:
                raise SDKException('Workflow', '101', 'workflow_xml must be UTF-8 encoded bytes')
        elif not isinstance(workflow_xml, str):
            raise SDKException('Workflow', '101')

        if os.path.isfile(workflow_xml):
            with open(workflow_xml, 'r', encoding='utf-8') as file_object:
                workflow_xml = file_object.read()
        else:
            try:
                __ = xmltodict.parse(workflow_xml)
            except ExpatError:
                raise SDKException('Workflow', '103')

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._WORKFLOWS, workflow_xml
        )

        self.refresh()

        if flag is False:
            response_string = self._update_response_(response.text)
            raise SDKException(
                'Workflow',
                '102',
                'Importing Workflow failed. {0}'.format(response_string)
            )

    def import_activity(self, activity_xml: str) -> None:
        """Import a workflow activity into the Commcell.

        This method imports a workflow activity by accepting either the path to a local XML file 
        or the XML content as a string. If a valid file path is provided, the file is read and 
        its contents are used; otherwise, the provided string is treated as the XML content.

        Args:
            activity_xml: The path to the workflow activity XML file or the XML content as a string.

        Raises:
            SDKException: 
                - If the activity_xml argument is not a string.
                - If the provided XML is invalid or the file path does not exist.
                - If the HTTP request to import the workflow activity fails.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> # Import from a file path
            >>> workflows.import_activity('/path/to/activity.xml')
            >>> # Import from XML content string
            >>> xml_content = '<Activity>...</Activity>'
            >>> workflows.import_activity(xml_content)

        #ai-gen-doc
        """
        if not isinstance(activity_xml, str):
            raise SDKException('Workflow', '101')

        if os.path.isfile(activity_xml):
            with open(activity_xml, 'r', encoding='utf-8') as file_object:
                activity_xml = file_object.read()
        else:
            try:
                __ = xmltodict.parse(activity_xml)
            except ExpatError:
                raise SDKException('Workflow', '103')

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._WORKFLOWS, activity_xml
        )

        self.refresh_activities()

        if flag is False:
            response_string = self._update_response_(response.text)
            raise SDKException(
                'Workflow',
                '102',
                'Importing Workflow activity failed. {0}'.format(response_string)
            )

    def download_workflow_from_store(
            self,
            workflow_name: str,
            download_location: str,
            cloud_username: str,
            cloud_password: str
        ) -> str:
        """Download a workflow from the Software Store to a specified location.

        This method retrieves the specified workflow from the Software Store using the provided
        cloud account credentials and saves it to the given download location.

        Args:
            workflow_name: The name of the workflow to download from the Software Store.
            download_location: The local directory path where the workflow XML should be saved.
            cloud_username: The username for the cloud account used to access the Software Store.
            cloud_password: The password for the specified cloud account.

        Returns:
            The full file path to the downloaded workflow XML.

        Raises:
            SDKException: If the workflow name is not a string, or if the download fails due to
                an unsuccessful HTTP status code.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> xml_path = workflows.download_workflow_from_store(
            ...     workflow_name="MyWorkflow",
            ...     download_location="/tmp/workflows",
            ...     cloud_username="user@example.com",
            ...     cloud_password="<example_password_here>"
            ... )
            >>> print(f"Workflow downloaded to: {xml_path}")

        #ai-gen-doc
        """
        if not isinstance(workflow_name, str):
            raise SDKException('Workflow', '101')

        from .commcell import Commcell

        cloud_commcell = Commcell('cloud.commvault.com', cloud_username, cloud_password)
        cvpysdk_object = cloud_commcell._cvpysdk_object
        services = cloud_commcell._services

        flag, response = cvpysdk_object.make_request(
            'GET', services['SOFTWARESTORE_PKGINFO'] % (workflow_name)
        )

        if flag is False:
            raise SDKException(
                'Workflow',
                '102',
                'Getting Pacakge id for workflow failed. {0}'.format(response.text)
            )

        if not response.json():
            raise SDKException('Response', '102')

        if "packageId" not in response.json():
            raise SDKException(
                'Workflow', '102', response.json()['errorDetail']['errorMessage']
            )
        package_id = response.json()["packageId"]
        platform_id = 1
        if "platforms" in response.json():
            platforms = response.json()["platforms"]
            if isinstance(platforms, list) and platforms:
                platform_id = platforms[0]["id"]

        download_xml = """
        <DM2ContentIndexing_OpenFileReq>
            <fileParams id="3" name="Package"/>
            <fileParams id="2" name="{0}"/>
            <fileParams id="9" name="{1}"/>
        </DM2ContentIndexing_OpenFileReq>
        """.format(package_id, platform_id)

        flag, response = cvpysdk_object.make_request(
            'POST', services['SOFTWARESTORE_DOWNLOADITEM'], download_xml
        )

        if flag:
            if response.json():
                file_content = response.json()["fileContent"]["data"]
                file_content = b64decode(file_content).decode('utf-8')

                if not os.path.exists(download_location):
                    try:
                        os.makedirs(download_location)
                    except FileExistsError:
                        pass

                download_path = os.path.join(download_location, workflow_name + ".xml")

                with open(download_path, "w", encoding="utf-8") as file_pointer:
                    file_pointer.write(file_content)

                return download_path

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, workflow_name: str, **kwargs: dict) -> 'Workflow':
        """Retrieve a Workflow object by its name.

        Searches for a workflow with the specified name and returns an instance of the Workflow class
        if a match is found. Optional keyword arguments can be provided to customize the retrieval.

        Args:
            workflow_name: The name of the workflow to retrieve.
            **kwargs: Optional keyword arguments.
                - get_properties (bool): If True, fetches workflow properties.

        Returns:
            Workflow: An instance of the Workflow class corresponding to the given workflow name.

        Raises:
            SDKException: If the workflow_name is not a string or if no workflow exists with the given name.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> workflow = workflows.get('DailyBackup', get_properties=True)
            >>> print(f"Workflow name: {workflow.name}")

        #ai-gen-doc
        """
        if not isinstance(workflow_name, str):
            raise SDKException('Workflow', '101')
        else:
            workflow_name = workflow_name.lower()

        workflow_id = self._workflows[workflow_name].get('id')
        if self.has_workflow(workflow_name):
            return WorkFlow(self._commcell_object, workflow_name, workflow_id,
                            get_properties = kwargs.get('get_properties',True))
        else:
            raise SDKException(
                'Workflow',
                '102',
                'No workflow exists with name: {0}'.format(workflow_name)
            )

    def delete_workflow(self, workflow_name: str) -> None:
        """Delete a workflow from the Commcell.

        Removes the specified workflow by name from the Commcell environment.

        Args:
            workflow_name: The name of the workflow to remove.

        Raises:
            SDKException: If the workflow name is not a string, or if the deletion fails due to an unsuccessful HTTP response.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> workflows.delete_workflow("DailyBackupWorkflow")
            >>> print("Workflow deleted successfully.")

        #ai-gen-doc
        """
        if not isinstance(workflow_name, str):
            raise SDKException('Workflow', '101')

        workflow_xml = """
            <Workflow_DeleteWorkflow>
                <workflow workflowName="{0}"/>
            </Workflow_DeleteWorkflow>
        """.format(workflow_name)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._WORKFLOWS, workflow_xml
        )

        self.refresh()

        if flag is False:
            response_string = self._update_response_(response.text)
            raise SDKException(
                'Workflow', '102', 'Deleting Workflow failed. {0}'.format(response_string)
            )

    def refresh(self) -> None:
        """Reload the list of workflows deployed on the Commcell.

        This method updates the internal cache of workflows, ensuring that any changes 
        (such as new deployments or deletions) are reflected in subsequent operations.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> workflows.refresh()  # Refresh the list of deployed workflows
            >>> print("Workflow list refreshed successfully")

        #ai-gen-doc
        """
        self._workflows = self._get_workflows()

    def refresh_activities(self) -> None:
        """Reload the list of workflow activities deployed on the Commcell.

        This method refreshes the internal cache of workflow activities, ensuring that 
        any new, updated, or removed activities on the Commcell are reflected in the 
        WorkFlows object.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> workflows.refresh_activities()  # Refresh the list of workflow activities
            >>> print("Workflow activities refreshed successfully")

        #ai-gen-doc
        """
        self._activities = self._get_activities()

    def get_interaction_properties(self, interaction_id: int, workflow_job_id: int = None) -> dict:
        """Retrieve the properties of a specific workflow interaction.

        Args:
            interaction_id: The unique identifier for the workflow interaction.
            workflow_job_id: Optional; the workflow job ID associated with the interaction.

        Returns:
            dict: A dictionary containing the properties of the specified workflow interaction.

        Raises:
            SDKException: If the response is empty or the interaction cannot be found.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> properties = workflows.get_interaction_properties(12345)
            >>> print(properties)
            >>> # To specify a workflow job ID:
            >>> properties = workflows.get_interaction_properties(12345, workflow_job_id=67890)
            >>> print(properties)

        #ai-gen-doc
        """
        if not interaction_id:
            if not workflow_job_id:
                raise SDKException('Workflow', '102', "Please provide either interaction id or workflow job id")
            all_interactions = self.all_interactions()
            for interaction in all_interactions:
                if int(interaction['jobId']) == workflow_job_id:
                    interaction_id = interaction['interactionId']
                    break
            if not interaction_id:
                raise SDKException('Workflow', '102', "Failed to find workflow job")
        flag, response = self._cvpysdk_object.make_request('GET', self._INTERACTION % interaction_id)

        if flag:
            if response.json() and 'request' in response.json():
                return response.json()['request']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def submit_interaction(self, interaction: dict, input_xml: str, action: str) -> None:
        """Submit a workflow interaction with the specified action and input XML.

        This method submits a given workflow interaction using the provided interaction dictionary,
        input XML string, and action. The interaction dictionary should contain all necessary
        details about the workflow interaction, while the input XML and action are specific to
        the workflow being executed.

        Args:
            interaction: A dictionary containing details of the workflow interaction.
                Example:
                    {
                        "interactionId": 3871,
                        "created": 1547524940,
                        "subject": "Delete Backupset [  ->  ->  ] requested by [ 11111_Automation_45_651 ]",
                        "activityName": "Get Authorization",
                        "flags": 1,
                        "description": "",
                        "sessionId": "a38b32dc-f505-45c5-9d61-3eaee226b50c",
                        "processStepId": 648993,
                        "jobId": 2804488,
                        "status": 0,
                        "workflow": {
                            "workflowName": "GetAndProcessAuthorization",
                            "workflowId": 2095
                        },
                        "commCell": {
                            "commCellName": "WIN-K2DCEJR56MG",
                            "commCellId": 2
                        },
                        "client": {
                            "clientId": 2,
                            "clientName": "WIN-K2DCEJR56MG"
                        },
                        "user": {
                            "userName": "11111_Automation_01-14-2019_23_01_45_651",
                            "userId": 1418
                        }
                    }
            input_xml: The input XML string required to complete the interaction. This should be
                constructed based on the workflow being executed and the expected user input.
            action: The action to perform for the interaction. This is specific to the workflow
                and the available options for the given interaction.

        Raises:
            Exception: If the workflow interaction request fails to submit.

        Example:
            >>> interaction_dict = {
            ...     "interactionId": 3871,
            ...     "created": 1547524940,
            ...     "subject": "Delete Backupset [  ->  ->  ] requested by [ 11111_Automation_45_651 ]",
            ...     "activityName": "Get Authorization",
            ...     "flags": 1,
            ...     "description": "",
            ...     "sessionId": "a38b32dc-f505-45c5-9d61-3eaee226b50c",
            ...     "processStepId": 648993,
            ...     "jobId": 2804488,
            ...     "status": 0,
            ...     "workflow": {
            ...         "workflowName": "GetAndProcessAuthorization",
            ...         "workflowId": 2095
            ...     },
            ...     "commCell": {
            ...         "commCellName": "WIN-K2DCEJR56MG",
            ...         "commCellId": 2
            ...     },
            ...     "client": {
            ...         "clientId": 2,
            ...         "clientName": "WIN-K2DCEJR56MG"
            ...     },
            ...     "user": {
            ...         "userName": "11111_Automation_01-14-2019_23_01_45_651",
            ...         "userId": 1418
            ...     }
            ... }
            >>> input_xml = "<InputXML>...</InputXML>"
            >>> action = "Approve"
            >>> workflows.submit_interaction(interaction_dict, input_xml, action)
            >>> print("Interaction submitted successfully.")

        #ai-gen-doc
        """
        if not isinstance(input_xml, str) or not isinstance(interaction, dict) or not isinstance(action, str):
            raise SDKException('Workflow', '101')

        from xml.sax.saxutils import escape
        escaped_xml = escape(input_xml)
        commserve_name = self._commcell_object.commserv_name

        request_xml = """
            <Workflow_SetWebFormInteractionRequest action="{0}" flags="1" inputXml="{1}" interactionId="{2}"
                jobId="{3}" okClicked="0" processStepId="{4}" sessionId="">
                <commCell commCellName="{5}"/>
                <client clientName="{6}"/>
            </Workflow_SetWebFormInteractionRequest>""".format(
                action, escaped_xml, str(interaction['interactionId']), str(interaction['jobId']),
                str(interaction['processStepId']), commserve_name, commserve_name
            )
        response = self._commcell_object._qoperation_execute(request_xml)

        if response.get('errorCode', 1) != 0:
            o_str = 'Error: ' + response.get('errorMessage', '')
            raise SDKException('Workflow', '102', 'Failed to submit workflow interaction request. Error: '+o_str)

    def all_interactions(self) -> List[Dict[str, Any]]:
        """Retrieve all interactive interactions for workflows on the Commcell.

        Returns:
            A list of dictionaries, each representing an interactive workflow interaction.

        Raises:
            SDKException: If the response is empty or if there are no interactions available.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> interactions = workflows.all_interactions()
            >>> print(f"Total interactions found: {len(interactions)}")
            >>> # Access details of the first interaction
            >>> if interactions:
            >>>     first_interaction = interactions[0]
            >>>     print(f"First interaction details: {first_interaction}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._INTERACTIONS)

        if flag:
            if response.json() and 'request' in response.json():
                return response.json()['request']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_workflows(self) -> Dict[str, Any]:
        """Get a dictionary containing all workflows and their associated information.

        Returns:
            Dict[str, Any]: A dictionary where each key is a workflow name and the value contains workflow details.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> all_wf = workflows.all_workflows  # Access the property to get all workflows
            >>> print(f"Total workflows: {len(all_wf)}")
            >>> # Access details of a specific workflow
            >>> if 'MyWorkflow' in all_wf:
            ...     print(all_wf['MyWorkflow'])

        #ai-gen-doc
        """
        return self._workflows

    @property
    def all_activities(self) -> List[dict]:
        """Get a read-only list of all activities associated with the workflows.

        Returns:
            List[dict]: A list of dictionaries, each representing an activity.

        Example:
            >>> workflows = WorkFlows(commcell_object)
            >>> activities = workflows.all_activities
            >>> print(f"Total activities: {len(activities)}")
            >>> # Access details of the first activity
            >>> if activities:
            ...     print(activities[0])

        #ai-gen-doc
        """
        return self._activities


class WorkFlow(object):
    """
    Represents and manages a workflow within a Commcell environment.

    The WorkFlow class provides a comprehensive interface for creating, configuring,
    deploying, executing, and managing workflows on a Commcell. It supports workflow
    property management, authorization handling, scheduling, cloning, exporting, and
    state control (enable/disable). The class also exposes workflow metadata through
    properties such as name, ID, version, revision, flags, and description.

    Key Features:
        - Initialization with Commcell object, workflow name, and workflow ID
        - Retrieval and management of workflow properties and definitions
        - Reading and setting workflow inputs and attributes
        - Configuration of workflow using XML
        - Workflow approval and authorization management
        - Enable and disable workflow operations
        - Deployment and execution of workflows with customizable inputs
        - Exporting and cloning workflows
        - Scheduling workflows with specified patterns and inputs
        - Refreshing workflow state and properties
        - Access to workflow metadata via properties (name, ID, version, revision, flags, description)

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, workflow_name: str, workflow_id: str = None, **kwargs: dict) -> None:
        """Initialize a WorkFlow instance for performing workflow-related operations.

        Args:
            commcell_object: Instance of the Commcell class representing the connected Commcell.
            workflow_name: Name of the workflow to manage.
            workflow_id: Optional ID of the workflow. If not provided, the workflow will be identified by name.
            **kwargs: Optional keyword arguments for additional configuration.
                - get_properties (bool): If True, fetches workflow properties during initialization.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> workflow = WorkFlow(commcell, 'MyWorkflow')
            >>> # To fetch properties during initialization
            >>> workflow = WorkFlow(commcell, 'MyWorkflow', get_properties=True)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._workflow_name = workflow_name.lower()
        self._workflow_id = str(workflow_id) if workflow_id else self._get_workflow_id()

        self._DEPLOY_WORKFLOW = self._services['DEPLOY_WORKFLOW']
        self._EXECUTE_WORKFLOW = self._services['EXECUTE_WORKFLOW']
        self._GET_WORKFLOW = self._services['GET_WORKFLOW'] % (self._workflow_id)
        self._GET_WORKFLOW_DEFINITION = self._services['GET_WORKFLOW_DEFINITION']
        self._CREATE_SCHEDULE = self._services['CREATE_UPDATE_SCHEDULE_POLICY']
        self._MODIFY_SCHEDULE = self._services['EXECUTE_QCOMMAND']

        self._workflows = self._commcell_object.workflows.all_workflows
        self._activities = self._commcell_object.workflows.all_activities

        self._properties = None
        self._description = None
        if kwargs.get('get_properties',True):
            self.refresh()

    def _get_workflow_id(self) -> str:
        """Retrieve the workflow ID associated with this Workflow instance.

        Returns:
            The unique identifier (ID) of the workflow as a string.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow_id = workflow._get_workflow_id()
            >>> print(f"Workflow ID: {workflow_id}")

        #ai-gen-doc
        """
        return self._commcell_object.workflows.get(self._workflow_name).workflow_id

    def _read_inputs(self, input_dict: dict) -> str:
        """Prompt the user to provide a value for a workflow input.

        If the user provides an empty value and a default value is specified in the input dictionary,
        the default value is returned. Otherwise, the user is prompted again until a valid input is provided.

        Args:
            input_dict: A dictionary containing details for the workflow input. Expected keys include:
                - 'input_name': The internal name of the input.
                - 'display_name': The name to display to the user.
                - 'documentation': Description or help text for the input.
                - 'default_value': The default value to use if the user provides no input.
                - 'is_required': Boolean indicating if the input is mandatory.

        Returns:
            The value entered by the user for the workflow input as a string.

        Example:
            >>> input_details = {
            ...     'input_name': 'username',
            ...     'display_name': 'User Name',
            ...     'documentation': 'Enter your login username.',
            ...     'default_value': 'admin',
            ...     'is_required': True
            ... }
            >>> value = workflow._read_inputs(input_details)
            >>> print(f"User input: {value}")

        #ai-gen-doc
        """
        if input_dict['display_name'] in [None, '']:
            prompt = input_dict['input_name']
        else:
            prompt = input_dict['display_name']

        if input_dict['is_required']:
            value = input(prompt + '*' + '::  ')
        else:
            value = input(prompt + '::  ')

        if value:
            return value
        elif input_dict['default_value']:
            return input_dict['default_value']
        else:
            return self._read_inputs(input_dict)

    def _set_workflow_properties(self, attrname: str, attrval: str, disabled: str = '0') -> None:
        """Set properties for the workflow.

        This method updates a specified property of the workflow, such as flags or description.
        The 'disabled' parameter can be set to '1' to disable the workflow.

        Args:
            attrname: The name of the workflow attribute to set (e.g., "flags", "description").
            attrval: The value to assign to the specified attribute (e.g., "0", "1", "2", "19", or a description string).
            disabled: Set to '1' to disable the workflow, or '0' (default) to keep it enabled.

        Raises:
            SDKException: If the HTTP status code is not successful or if setting workflow properties fails.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow._set_workflow_properties('description', 'This is a workflow description')
            >>> workflow._set_workflow_properties('flags', '1', disabled='1')
            >>> # The workflow's description is updated, and it is disabled

        #ai-gen-doc
        """
        request_xml = {
            "Workflow_SetWorkflowProperties":
            {
                attrname: attrval,
                "disabled": disabled,
                "workflow": {
                    "workflowName": self._workflow_name,
                    "workflowId": self._workflow_id
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                if response.json()['errorCode'] != 0:
                    raise SDKException('Workflow', '105')
                else:
                    self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_workflow_properties(self) -> dict:
        """Retrieve the properties of the workflow.

        Returns:
            dict: A dictionary containing key-value pairs representing the workflow's properties.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> workflow = WorkFlow()
            >>> properties = workflow._get_workflow_properties()
            >>> print(properties)
            >>> # Output: {'name': 'BackupWorkflow', 'status': 'Active', ...}

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._GET_WORKFLOW)

        if flag:
            if response.json() and 'container' in response.json():
                self._properties = response.json()['container']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_workflow_definition(self) -> str:
        """Retrieve the workflow definition from the workflow properties.

        Returns:
            The workflow definition as a string, extracted from the workflow property response.

        Raises:
            SDKException: If the response is not successful.

        Example:
            >>> workflow = WorkFlow()
            >>> definition = workflow._get_workflow_definition()
            >>> print(definition)
            # Output: XML or JSON string representing the workflow definition

        #ai-gen-doc
        """
        workflow = self._workflow_name

        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._GET_WORKFLOW_DEFINITION % (
                self._workflow_id
            )
        )
        if flag:
            if not response.json():
                    raise SDKException('Response', '102', 'Failed to clone workflow')
            return response.json()
        else:
            raise SDKException('Response', '101', response.text)

    def set_workflow_configuration(self, config_xml: str) -> None:
        """Set the configuration for the workflow using the provided XML input.

        This method updates the workflow's configuration tab with the specified XML configuration.

        Args:
            config_xml: A string containing the XML configuration for the workflow's properties->configuration tab.

        Raises:
            SDKException: If the HTTP status code is not successful or if setting the workflow configuration fails.

        Example:
            >>> workflow = WorkFlow()
            >>> xml_config = "<configuration><property name='Timeout' value='30'/></configuration>"
            >>> workflow.set_workflow_configuration(xml_config)
            >>> print("Workflow configuration updated successfully.")

        #ai-gen-doc
        """
        config_xml = "<configuration>{0}</configuration>".format(config_xml)
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EDIT_WORKFLOW_CONFIG'] % self.workflow_id, config_xml
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_message = response.json().get('errorMessage', 'No error message in response')
                if response.json()['errorCode'] != 0:
                    raise SDKException('Workflow', '105', error_message)
                else:
                    self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def approve_workflow(self, auth_id: Optional[int] = None) -> None:
        """Approve a pending change to this workflow initiated by another admin user.

        If an authorization ID is provided, approves the specific workflow change associated with that ID.
        If no auth_id is given, the latest pending authorization will be approved.

        Args:
            auth_id: Optional; The authorization ID to approve. If not specified, the latest pending authorization is approved.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow.approve_workflow()  # Approves the latest pending workflow change
            >>> workflow.approve_workflow(auth_id=12345)  # Approves the workflow change with auth ID 12345

        #ai-gen-doc
        """
        if not auth_id:
            auth_dicts = self.get_authorizations()
            if not auth_dicts:
                raise SDKException('Workflow', '102', 'No approvals found for this workflow')
            auth_id = sorted(auth_dicts, key=lambda x: x.get("createdTime"))[-1].get('authId')

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['APPROVE_WORKFLOW'] % auth_id
        )

        if flag:
            if response.json() and 'errorCode' in response.json():
                error_message = response.json().get('errorMessage', 'No error message in response')
                if response.json()['errorCode'] != 0:
                    raise SDKException('Workflow', '105', error_message)
                else:
                    self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_authorizations(self) -> list[dict]:
        """Retrieve the list of authorizations (approvals) associated with this workflow.

        Returns:
            list[dict]: A list of dictionaries, each containing details about an authorization for the workflow.

        Example:
            >>> workflow = WorkFlow()
            >>> authorizations = workflow.get_authorizations()
            >>> print(f"Number of authorizations: {len(authorizations)}")
            >>> if authorizations:
            ...     print(f"First authorization details: {authorizations[0]}")

        #ai-gen-doc
        """
        self._get_workflow_properties()
        return self._properties.get('authorizations', [])

    def enable(self) -> None:
        """Enable the workflow.

        This method activates the workflow, making it available for execution. If the operation fails
        due to an unsuccessful HTTP status code or other issues, an SDKException is raised.

        Raises:
            SDKException: If the HTTP status code is not successful or enabling the workflow fails.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow.enable()
            >>> print("Workflow enabled successfully.")

        #ai-gen-doc
        """
        self._set_workflow_properties('flags', '0', disabled='0')

    def disable(self) -> None:
        """Disable the workflow associated with this WorkFlow instance.

        This method attempts to disable the workflow. If the operation fails or the HTTP status code 
        is not successful, an SDKException is raised.

        Raises:
            SDKException: If the HTTP status code is not successful or disabling the workflow fails.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow.disable()
            >>> print("Workflow disabled successfully")
            # If disabling fails, an SDKException will be raised.

        #ai-gen-doc
        """
        self._set_workflow_properties('flags', '1', disabled='1')

    def deploy_workflow(self, workflow_engine: Optional[str] = None, workflow_xml: Optional[str] = None) -> None:
        """Deploy a workflow on the Commcell.

        This method deploys a workflow to the specified workflow engine (client) using either the path to a workflow XML file or the XML content itself. If a file path is provided for `workflow_xml`, the file is read and its contents are used. If a string of XML content is provided, it is used directly.

        Args:
            workflow_engine: The name of the client (workflow engine) on which to deploy the workflow. If None, the default workflow engine is used.
            workflow_xml: The path to the workflow XML file or the XML content as a string. If a valid file path is provided, the file is read; otherwise, the value is treated as XML content.

        Raises:
            SDKException: If the workflow engine or workflow XML arguments are not strings, if the workflow does not exist, if the XML is invalid or the file path is incorrect, or if deployment fails for any reason.

        Example:
            >>> workflow = WorkFlow(commcell_object)
            >>> workflow.deploy_workflow(workflow_engine="client01", workflow_xml="/path/to/workflow.xml")
            >>> # Alternatively, deploy using XML content directly
            >>> xml_content = "<Workflow>...</Workflow>"
            >>> workflow.deploy_workflow(workflow_engine="client01", workflow_xml=xml_content)

        #ai-gen-doc
        """

        workflow_name = self._workflow_name.lower()

        if not ((workflow_engine is not None and isinstance(workflow_engine, str)) or
                (workflow_xml is not None and isinstance(workflow_xml, str))):
            raise SDKException('Workflow', '101')

        if not self._commcell_object.workflows.has_workflow(workflow_name):
            raise SDKException('Workflow', '104')

        workflow_deploy_service = self._DEPLOY_WORKFLOW % self._workflows[workflow_name]['id']

        if workflow_xml is None:
            workflow_xml = {
                "Workflow_DeployWorkflow": {}
            }

            if workflow_engine is not None:
                workflow_deploy_service='%s?clientName=%s'%(workflow_deploy_service,workflow_engine)

        elif os.path.isfile(workflow_xml):
            with open(workflow_xml, 'r', encoding='utf-8') as file_object:
                workflow_xml = file_object.read()
        else:
            try:
                __ = xmltodict.parse(workflow_xml)
            except ExpatError:
                raise SDKException('Workflow', '103')

        flag, response = self._cvpysdk_object.make_request(
            'POST', workflow_deploy_service, workflow_xml
        )

        self._commcell_object.workflows.refresh()

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if error_code != "0":
                    error_message = response.json()['errorMessage']

                    raise SDKException(
                        'Workflow',
                        '102',
                        'Failed to deploy workflow\nError: "{0}"'.format(error_message)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def execute_workflow(self, workflow_inputs: Optional[Dict[str, Any]] = None, hidden: bool = False) -> tuple:
        """Execute the workflow with the specified inputs and return its job information.

        This method runs the workflow associated with this WorkFlow instance, using the provided
        input parameters. If no inputs are given, the user may be prompted for required values.
        The method returns a tuple containing the workflow outputs and job information.

        Args:
            workflow_inputs: Optional dictionary of input parameters for the workflow.
                If not provided, the user will be prompted for required inputs.
                Example:
                    {
                        "ClientGroupName": "client_group_value"
                    }
            hidden: Boolean indicating whether the workflow is hidden.

        Returns:
            tuple:
                - dict: Outputs dictionary received in the API response.
                - Union[str, dict, object]: Job information, which can be:
                    - str: When executed in API mode and no job ID is returned.
                    - dict: Complete server response if expected values are missing.
                    - object: Instance of the Job class if the workflow runs in job mode or has user sessions.

        Raises:
            SDKException: If the workflow name is not a string, execution fails, response is empty or unsuccessful,
                or if no workflow exists with the given name.

        Example:
            >>> workflow = WorkFlow()
            >>> outputs, job_info = workflow.execute_workflow(
            ...     workflow_inputs={"ClientGroupName": "MyClientGroup"},
            ...     hidden=False
            ... )
            >>> print("Workflow outputs:", outputs)
            >>> print("Job info:", job_info)
            #ai-gen-doc
        """
        workflow_name = self._workflow_name.lower()

        if not hidden and workflow_name not in self._workflows:
            raise SDKException('Workflow', '104')

        execute_workflow_json = {}

        if workflow_inputs is None:
            workflow_vals = self._workflows[workflow_name]
            if 'inputs' in workflow_vals:
                for a_input in workflow_vals['inputs']:
                    execute_workflow_json[a_input['input_name']] = self._read_inputs(a_input)
        else:
            execute_workflow_json = workflow_inputs

        import urllib.parse
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._EXECUTE_WORKFLOW % urllib.parse.quote(workflow_name), execute_workflow_json)

        if flag:
            if response.json():
                output = response.json()

                if "jobId" in response.json():
                    if response.json()["jobId"] == 0:
                        return output, 'Workflow Execution Finished Successfully'
                    else:
                        return output, Job(self._commcell_object, response.json()['jobId'])
                elif "errorCode" in response.json():
                    if int(response.json()['errorCode']) == 0:
                        return output, 'Workflow Execution Finished Successfully'
                    else:
                        error_message = response.json()['errorMessage']
                        o_str = 'Executing Workflow failed\nError: "{0}"'.format(error_message)

                        raise SDKException('Workflow', '102', o_str)
                else:
                    return output, response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def export_workflow(self, export_location: str = None) -> str:
        """Export the workflow to a specified directory location.

        This method exports the current workflow to the given directory. The exported file will be in XML format.
        If no export location is provided, a default directory will be used.

        Args:
            export_location: The directory path where the workflow XML file will be exported. If None, a default location is used.

        Returns:
            The absolute path to the exported workflow XML file.

        Raises:
            SDKException: If the export location does not exist, if no workflow exists with the given name,
                if the response is empty or unsuccessful, or if writing to the export file fails.

        Example:
            >>> workflow = WorkFlow()
            >>> exported_path = workflow.export_workflow('/tmp/exported_workflows')
            >>> print(f"Workflow exported to: {exported_path}")

        #ai-gen-doc
        """
        workflow_name = self._workflow_name

        if not self._commcell_object.workflows.has_workflow(workflow_name):
            raise SDKException('Workflow', '104')

        if export_location is None:
            export_location = os.getcwd()
        else:
            if not isinstance(export_location, str):
                raise SDKException('Workflow', '101')

            if not os.path.exists(export_location):
                os.makedirs(export_location)

        request_xml = """
            <Workflow_GetWorkflowRequest exportOnly="1">
                <workflow workflowName="{0}"/>
            </Workflow_GetWorkflowRequest>
        """.format(workflow_name)

        workflow_xml = os.path.join(export_location, workflow_name + '.xml')

        headers = self._commcell_object._headers.copy()
        headers['Accept'] = 'application/xml'

        flag, response = self._cvpysdk_object.make_request(
            'POST',
            self._commcell_object._services['EXECUTE_QCOMMAND'],
            request_xml,
            headers=headers
        )

        if flag and xmltodict.parse(response.text).get('Workflow_WorkflowDefinition'):
            try:
                with open(workflow_xml, 'w') as export_file:
                    export_file.write(response.text)
                return workflow_xml
            except Exception as excp:
                raise SDKException(
                    'Workflow',
                    '102',
                    'Failed to write workflow definition: "{0}" to file.\nError: "{1}"'.format(
                        workflow_xml, excp
                    )
                )
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def clone_workflow(self, clone_workflow_name: str) -> None:
        """Clone the current workflow with a new name.

        This method creates a duplicate of the existing workflow, assigning it the specified name.
        The cloned workflow will have the same configuration and steps as the original.

        Args:
            clone_workflow_name: The name to assign to the new cloned workflow.

        Raises:
            SDKException: If the cloning operation fails or the response is not successful.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow.clone_workflow("MyClonedWorkflow")
            >>> print("Workflow cloned successfully.")

        #ai-gen-doc
        """
        workflow_definition = self._get_workflow_definition()
        workflow_definition['name'] = clone_workflow_name
        workflow_definition['uniqueGuid'] = ''

        flag, response = self._cvpysdk_object.make_request(
            'PUT',
            self._services['GET_WORKFLOWS'],
            workflow_definition,
        )

        if flag and response.json():
            if not response.json()['workflow']['workflowId']:
                raise SDKException('Workflow', '102', 'Failed to clone the workflow')
        else:
            raise SDKException('Response', '101', response.text)

    def schedule_workflow(self, schedule_pattern: dict, workflow_inputs: dict = None) -> 'Schedule':
        """Create a schedule for the workflow with the specified pattern and optional inputs.

        Args:
            schedule_pattern: Dictionary defining the schedule pattern. Refer to SchedulePattern.create_schedule 
                in schedules.py for supported pattern types. Example:
                    {
                        "schedule_name": "schedule1",
                        "freq_type": "daily",
                        "active_start_time": "14:00",
                        "repeat_days": 2
                    }
            workflow_inputs: Optional dictionary of workflow input parameters. If not provided, 
                the user will be prompted for inputs at runtime. Example:
                    {
                        "ClientGroupName": "client_group_value"
                    }

        Returns:
            Schedule: An instance of the Schedule class representing the created schedule.

        Example:
            >>> schedule_pattern = {
            ...     "schedule_name": "NightlyBackup",
            ...     "freq_type": "daily",
            ...     "active_start_time": "23:00",
            ...     "repeat_days": 1
            ... }
            >>> workflow_inputs = {
            ...     "ClientGroupName": "ProductionServers"
            ... }
            >>> schedule = workflow.schedule_workflow(schedule_pattern, workflow_inputs)
            >>> print(f"Schedule created: {schedule}")

        #ai-gen-doc
        """
        from cvpysdk.schedules import SchedulePattern
        if workflow_inputs is not None:
            xml = str(xmltodict.unparse(input_dict={"inputs": workflow_inputs}).split('\n')[1])
        task_req = {
            "processinginstructioninfo": {},
            "taskInfo": {
                "associations": [
                    {
                        "workflowName": self._workflow_name
                    }
                ],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 2001
                        },
                        "options": {
                            "workflowJobOptions": xml if workflow_inputs else "",
                            "adminOpts": {
                                "contentIndexingOption": {
                                    "subClientBasedAnalytics": False
                                }
                            }
                        }
                    }
                ]
                }
        }
        request_json = SchedulePattern().create_schedule(task_req, schedule_pattern)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_SCHEDULE, request_json)
        output = self._process_workflow_schedule_response(flag, response)
        if output[0]:
            self._commcell_object.schedules.refresh()
            return self._commcell_object.schedules.get(task_id=response.json()["taskId"])
        o_str = 'Failed to create Schedule\nError: "{0}"'
        raise SDKException('Schedules', '102', o_str.format(output[2]))

    def _process_workflow_schedule_response(self, flag: bool, response: dict) -> tuple:
        """Process the response received after a workflow schedule creation request.

        Args:
            flag: Indicates whether the initial request was successful (True) or not (False).
            response: Dictionary containing the response data from the schedule modification request.

        Returns:
            tuple: A tuple containing:
                - flag (bool): True if the operation was successful, False otherwise.
                - error_code (int): The error code from the response, if any.
                - error_message (str): The error message from the response, if any.

        Example:
            >>> result = workflow._process_workflow_schedule_response(True, {"errorCode": 0, "errorMessage": ""})
            >>> print(result)
            (True, 0, "")
            >>> # result[0] is the success flag, result[1] is the error code, result[2] is the error message

        #ai-gen-doc
        """

        if flag:
            if response.json():
                if "taskId" in response.json():
                    task_id = str(response.json()["taskId"])

                    if task_id:
                        return True, "0", ""

                elif "errorCode" in response.json():
                    error_code = str(response.json()['errorCode'])
                    error_message = response.json()['errorMessage']

                    if error_code == "0":
                        return True, "0", ""

                    if error_message:
                        return False, error_code, error_message
                    else:
                        return False, error_code, ""
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Reload the properties of the workflow to ensure the latest information is available.

        This method updates the workflow's internal state by fetching the most recent properties.
        Use this method if you suspect the workflow's properties have changed and want to synchronize
        the object with the current state.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow.refresh()
            >>> print("Workflow properties refreshed successfully")

        #ai-gen-doc
        """
        self._get_workflow_properties()

    @property
    def workflow_name(self) -> str:
        """Get the name of the workflow as a read-only property.

        Returns:
            The name of the workflow as a string.

        Example:
            >>> workflow = WorkFlow()
            >>> name = workflow.workflow_name  # Access the workflow name property
            >>> print(f"Workflow name: {name}")

        #ai-gen-doc
        """
        return self._workflow_name

    @property
    def workflow_id(self) -> str:
        """Get the unique identifier (ID) of the workflow as a read-only property.

        Returns:
            int: The workflow's unique identifier.

        Example:
            >>> workflow = WorkFlow()
            >>> wf_id = workflow.workflow_id  # Access the workflow ID as a property
            >>> print(f"Workflow ID: {wf_id}")

        #ai-gen-doc
        """
        return self._workflow_id

    @property
    def version(self) -> str:
        """Get the version of the workflow.

        Returns:
            The version string representing the current workflow version.

        Example:
            >>> workflow = WorkFlow()
            >>> current_version = workflow.version  # Access the version property
            >>> print(f"Workflow version: {current_version}")

        #ai-gen-doc
        """
        return self._properties['version']

    @property
    def revision(self) -> int:
        """Get the current revision number of the workflow.

        Returns:
            The revision number of the workflow as an integer.

        Example:
            >>> workflow = WorkFlow()
            >>> current_revision = workflow.revision  # Access the revision property
            >>> print(f"Workflow revision: {current_revision}")

        #ai-gen-doc
        """
        return self._properties['revision']

    @property
    def flags(self) -> dict:
        """Get the workflow flags as a property of the Workflow class.

        Returns:
            dict: A dictionary containing the flags associated with the workflow.

        Example:
            >>> workflow = WorkFlow()
            >>> flags = workflow.flags  # Access workflow flags as a property
            >>> print(flags)
            {'is_active': True, 'priority': 'high'}

        #ai-gen-doc
        """
        return self._properties['flags']

    @property
    def description(self) -> str:
        """Get the description of the workflow.

        Returns:
            The description of the workflow as a string.

        Example:
            >>> workflow = WorkFlow()
            >>> desc = workflow.description  # Access the workflow description property
            >>> print(f"Workflow description: {desc}")

        #ai-gen-doc
        """
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set the description of the workflow.

        Updates the workflow's description to the specified string value.

        Args:
            value: The new description to assign to the workflow. Must be a string.

        Raises:
            SDKException: If the description update fails or if the input value is not a string.

        Example:
            >>> workflow = WorkFlow()
            >>> workflow.description = "This workflow automates daily backups."
            >>> # The workflow's description is now updated

        #ai-gen-doc
        """
        if isinstance(value, str):
            self._set_workflow_properties("description", value)
        else:
            raise SDKException(
                'Workflow', '102', 'Failed to set workflow description'
            )