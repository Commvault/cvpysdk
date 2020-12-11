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
    set_workflow_configuration()        -- Set workflow configuration

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

from past.builtins import basestring
from past.builtins import raw_input

from .job import Job
from .exception import SDKException


class WorkFlows(object):
    """Class for representing all workflows associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize the WorkFlow class instance for performing workflow related
            operations.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the WorkFlow class

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

    def __str__(self):
        """Representation string consisting of all workflows of the Commcell.

            Returns:
                str     -   string of all the workflows associated with the commcell

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

    def __repr__(self):
        """Representation string for the instance of the WorkFlow class."""
        return "WorkFlow class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the workflows associated to the Commcell."""
        return len(self.all_workflows)

    def __getitem__(self, value):
        """Returns the name of the workflow for the given workflow ID or
            the details of the workflow for given workflow Name.

            Args:
                value   (str / int)     --  Name or ID of the workflow

            Returns:
                str     -   name of the workflow, if the workflow id was given

                dict    -   dict of details of the workflow, if workflow name was given

            Raises:
                IndexError:
                    no workflow exists with the given Name / Id

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

    def _get_workflows(self):
        """Gets all the workflows associated to the commcell.

            Returns:
                dict    -   consists of all workflows in the commcell

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def _get_activities(self):
        """Gets all the workflow activities associated to the commcell.

            Returns:
                dict    -   consists of all activities in the commcell

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def has_workflow(self, workflow_name):
        """Checks if a workflow exists in the commcell with the input workflow name.

            Args:
                workflow_name   (str)   --  name of the workflow

            Returns:
                bool    -   boolean output whether the workflow exists in the
                            commcell or not

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

        """
        if not isinstance(workflow_name, basestring):
            raise SDKException('Workflow', '101')

        return self._workflows and workflow_name.lower() in self._workflows

    def has_activity(self, activity_name):
        """Checks if a workflow activity exists in the commcell with the input
            activity name.

            Args:
                activity_name   (str)   --  name of the activity

            Returns:
                bool    -   boolean output whether the workflow activity exists
                            in the commcell or not

            Raises:
                SDKException:
                    if type of the workflow activity name argument is not string

        """
        if not isinstance(activity_name, basestring):
            raise SDKException('Workflow', '101')

        return self._activities and activity_name.lower() in self._activities

    def import_workflow(self, workflow_xml):
        """Imports a workflow to the Commcell.

            Args:
                workflow_xml    (str)   --  path of the workflow xml file / XML contents

                    checks whether the given value is a local file, and reads its contents

                    otherwise, uses the value given as the body for the POST request

            Returns:
                None

            Raises:
                SDKException:
                    if type of the workflow xml argument is not string

                    if workflow xml is not a valid xml / a valid file path

                    if HTTP Status Code is not SUCCESS / importing workflow failed

        """
        if not isinstance(workflow_xml, basestring):
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

    def import_activity(self, activity_xml):
        """Imports a workflow activity to the Commcell.

            Args:
                activity_xml    (str)   --  path of the workflow activity xml
                                            file / XMl contents.

                    Checks whether the given value is a local file, and reads its

                    contents otherwise, uses the value given as the body for the

                    POST request

            Returns:
                None

            Raises:
                SDKException:
                    if type of the workflow activity xml argument is not string

                    if workflow activity xml is not a valid xml / a valid file path

                    if HTTP Status Code is not SUCCESS / importing workflow failed

        """
        if not isinstance(activity_xml, basestring):
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
            workflow_name,
            download_location,
            cloud_username,
            cloud_password):
        """Downloads workflow from Software Store.

            Args:
                workflow_name       (str)   --  name of the workflow to download

                download_location   (str)   --  location to download the workflow at

                cloud_username      (str)   --  username for the cloud account

                cloud_password      (str)   --  password for the above username

            Returns:
                str     -   full path of the workflow XML

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if HTTP Status Code is not SUCCESS / download workflow failed

        """
        if not isinstance(workflow_name, basestring):
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

        if response.json():
            if "packageId" in response.json():
                package_id = response.json()["packageId"]
            else:
                raise SDKException(
                    'Workflow', '102', response.json()['errorDetail']['errorMessage']
                )
        else:
            raise SDKException('Response', '102')

        download_xml = """
        <DM2ContentIndexing_OpenFileReq>
            <fileParams id="3" name="Package"/>
            <fileParams id="2" name="{0}"/>
            <fileParams id="9" name="1"/>
        </DM2ContentIndexing_OpenFileReq>
        """.format(package_id)

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

                with open(download_path, "w") as file_pointer:
                    file_pointer.write(file_content)

                return download_path

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, workflow_name):
        """Returns a workflow object if workflow name matches specified name
            We check if specified name matches any of the existing workflow names.

            Args:
                workflow_name (str)  --  name of the workflow

            Returns:
                object - instance of the Workflow class for the given workflow name

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if no workflow exists with the given name
        """
        if not isinstance(workflow_name, basestring):
            raise SDKException('Workflow', '101')
        else:
            workflow_name = workflow_name.lower()

        workflow_id = self._workflows[workflow_name].get('id')

        if self.has_workflow(workflow_name):
            return WorkFlow(self._commcell_object, workflow_name, workflow_id)
        else:
            raise SDKException(
                'Workflow',
                '102',
                'No workflow exists with name: {0}'.format(workflow_name)
            )

    def delete_workflow(self, workflow_name):
        """Deletes a workflow from the Commcell.

            Args:
                workflow_name   (str)   --  name of the workflow to remove

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if HTTP Status Code is not SUCCESS / importing workflow failed

        """
        if not isinstance(workflow_name, basestring):
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

    def refresh(self):
        """Refresh the list of workflows deployed on the Commcell."""
        self._workflows = self._get_workflows()

    def refresh_activities(self):
        """Refresh the list of workflow activities deployed on the Commcell."""
        self._activities = self._get_activities()

    def get_interaction_properties(self, interaction_id):
        """Returns a workflow interaction properties to the user

            Args:
                interaction_id (int)  --  Workflow interaction id

            Returns:
                dictionary - Workflow interaction id properties

            Raises:
                SDKException:
                    - if response is empty

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._INTERACTION % interaction_id)

        if flag:
            if response.json() and 'request' in response.json():
                return response.json()['request']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def submit_interaction(self, interaction, input_xml, action):
        """ Submits a given interaction with specified action

            Args:
                interaction (dict)    --  Interaction dictionary
                e.g:
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

                input_xml (str)       --  Input XML string for completing the interaction.
                                            e.g : This is very specific to the user input interaction.
                                                    Construct the input XML based on workflow being executed and send
                                                    to this module.

                action   (str)        --  Interaction action
                                            This is very specific to workflow being executed and the expected options
                                                for the given interaction

            Raises:
                Exception:
                    Failed to submit workflow interaction request
        """
        if not isinstance(input_xml, basestring) or not isinstance(interaction, dict) or not isinstance(action, str):
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

    def all_interactions(self):
        """ Returns all interactive interactions for workflows on commcell
            Args:
                None

            Raises:
                SDKException:

                    if response is empty

                    if there are no interactions

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
    def all_workflows(self):
        """Returns the dictionary consisting of all the workflows and their info."""
        return self._workflows

    @property
    def all_activities(self):
        """Treats the activities as a read-only attribute."""
        return self._activities


class WorkFlow(object):
    """Class for representing a workflow on a commcell."""

    def __init__(self, commcell_object, workflow_name, workflow_id=None):
        """Initialize the WorkFlow class instance for performing workflow related operations.

            Args:
                commcell_object      (object)   --  instance of the Commcell class

                workflow_name        (str)      --  Name of the workflow

                workflow_id          (str)      --  id of the workflow
                    default: None

            Returns:
                object  -   instance of the WorkFlow class

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
        self.refresh()

    def _get_workflow_id(self):
        """Gets the workflow id associated with this Workflow.

            Returns:
                str - id associated with this workflow
        """
        return self._commcell_object.workflows.get(self._workflow_name).workflow_id

    def _read_inputs(self, input_dict):
        """Gets the values from the user for a workflow input.

            If user provides empty value, then default value is returned for the
            workflow input, if it is specified.

            Else, prompts the user again for the input.

            Args:
                input_dict (dict)   --  dictionary containing the values for a
                workflow input

                    {
                        'input_name',

                        'display_name',

                        'documentation',

                        'default_value',

                        'is_required'
                    }

            Returns:
                str     -   value entered by the user for the workflow input

        """
        if input_dict['display_name'] in [None, '']:
            prompt = input_dict['input_name']
        else:
            prompt = input_dict['display_name']

        if input_dict['is_required']:
            value = raw_input(prompt + '*' + '::  ')
        else:
            value = raw_input(prompt + '::  ')

        if value:
            return value
        elif input_dict['default_value']:
            return input_dict['default_value']
        else:
            return self._read_inputs(input_dict)

    def _set_workflow_properties(self, attrname, attrval, disabled='0'):
        """Set Workflow Properties

            Args:
                attrname    (str)    : Attribute Name
                                            e.g:    flags,
                                                    description

                attrval     (str)    : Attribute value
                                                    0, 1, 2, 19
                                                    "This is workflow description"

                disabled    (str)   : Set to 1 to disable a workflow
                                        default is '0'

            Raises:
                SDKException:

                    if HTTP Status Code is not SUCCESS / Setting workflow properties failed
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

    def _get_workflow_properties(self):
        """Gets the workflow properties

            Returns:
                dict - dictionary consisting of the properties of workflow

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._GET_WORKFLOW)

        if flag:
            if response.json() and 'container' in response.json():
                self._properties = response.json()['container']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_workflow_definition(self):
        """Get the workflow definition from the workflow properties

        Returns:
                definition  (str)   - workflow attribute of workflow property response

            Raises:
                SDKException:
                    if response is not success
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

    def set_workflow_configuration(self, config_xml):
        """Set Workflow configuration

            Args:
                config_xml    (xml)    : Configuration inputs for the workflow's properties->configuration tab

            Raises:
                SDKException:

                    if HTTP Status Code is not SUCCESS / Setting workflow set_workflow_configuration failed
        """
        config_xml = "<configuration>{0}</configuration>".format(config_xml)
        from xml.sax.saxutils import escape
        escaped_xml = escape(config_xml)

        request_xml = """<Workflow_SetConfigurationSettings configSettings="{0}">
            <workflow workflowId="{1}" workflowName="{2}"/>
        </Workflow_SetConfigurationSettings> """.format(escaped_xml, self._workflow_id, self._workflow_name)

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

    def enable(self):
        """ Enable Worklfow

            Raises:
                SDKException:

                    if HTTP Status Code is not SUCCESS / Enabling workflow fails
        """
        self._set_workflow_properties('flags', '0', disabled='0')

    def disable(self):
        """ Disable Worklfow

            Raises:
                SDKException:

                    if HTTP Status Code is not SUCCESS / Disabling workflow fails
        """
        self._set_workflow_properties('flags', '1', disabled='1')

    def deploy_workflow(self, workflow_engine=None, workflow_xml=None):
        """Deploys a workflow on the Commcell.

            Args:
                workflow_engine     (str)   --  name of the client to deploy the workflow on

                    default: None

                workflow_xml    (str)   --  path of the workflow xml file / XMl contents

                        checks whether the given value is a local file, and reads its contents

                        otherwise, uses the value given as the body for the POST request

                    default: None

            Returns:
                None

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if workflow xml argument is given and is not of type string

                    if no workflow exists with the given name

                    if workflow xml is given and is not a valid xml / a valid file path

                    if failed to deploy workflow

                    if response is empty

                    if response is not success

        """

        workflow_name = self._workflow_name.lower()

        if not ((workflow_engine is not None and isinstance(workflow_engine, basestring)) or
                (workflow_xml is not None and isinstance(workflow_xml, basestring))):
            raise SDKException('Workflow', '101')

        if not self._commcell_object.workflows.has_workflow(workflow_name):
            raise SDKException('Workflow', '104')

        workflow_deploy_service = self._DEPLOY_WORKFLOW % self._workflows[workflow_name]['id']

        if workflow_xml is None:
            workflow_xml = {
                "Workflow_DeployWorkflow": {}
            }

            if workflow_engine is not None:
                workflow_xml = {
                    "Workflow_DeployWorkflow": {
                        "client": {
                            "clientName": workflow_engine
                        }
                    }
                }
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

    def execute_workflow(self, workflow_inputs=None, hidden=False):
        """Executes the workflow with the workflow name given as input, and returns its job id.

            Args:

                workflow_inputs     (dict)  --  dictionary consisting of inputs for the workflow

                    if inputs are not given, user will be prompted for inputs on the command line

                    default: None

                    inputs dict format:

                        {
                            'input1_name': 'input1_value',

                            'input2_name': 'input2_value'
                        }

                    e.g.:

                        for executing the Demo_CheckReadiness workflow, inputs dict would be:

                            {
                                "ClientGroupName": "client_group_value"
                            }

                hidden (bool) -- Is the workflow hidden ? True/False

            Returns:
                **tuple**   -   (`dict`, `str` **/** `dict` **/** `object`)

                    **dict**    -   returns the outputs dictionary received in the
                    response of the API

                    **str / dict / object**

                        str     -   when workflow is executed in API mode

                            when no job id was returned / job ID or error code is 0

                        dict    -   complete response received from the server

                            when the response did not had any expected values

                        object  -   instance of the Job class for this workflow job

                            object of the Job class is mainly returned when the Workflow being
                            executed has User Sessions, OR the workflow is executed in JOB mode

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if failed to execute workflow

                    if response is empty

                    if response is not success

                    if no workflow exists with the given name

        """
        workflow_name = self._workflow_name.lower()

        if not hidden and workflow_name not in self._workflows:
            raise SDKException('Workflow', '104')

        execute_workflow_json = {}

        if workflow_inputs is None:
            workflow_vals = self._workflows[workflow_name]
            if 'inputs' in workflow_vals:
                o_str = 'Workflow Name: \t\t"{0}"\n'.format(workflow_name)
                o_str += 'Workflow Description: \t"{0}"\n'.format(workflow_vals.get('description', ''))

                print(o_str)

                for a_input in workflow_vals['inputs']:
                    execute_workflow_json[a_input['input_name']] = self._read_inputs(a_input)
        else:
            execute_workflow_json = workflow_inputs

        import urllib.parse
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._EXECUTE_WORKFLOW % urllib.parse.quote(workflow_name), execute_workflow_json)

        if flag:
            if response.json():
                output = response.json().get("outputs", {})

                if "jobId" in response.json():
                    if response.json()["jobId"] == 0:
                        return output, 'Workflow Execution Finished Successfully'
                    else:
                        return output, Job(self._commcell_object, response.json()['jobId'])
                elif "errorCode" in response.json():
                    if response.json()['errorCode'] == 0:
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

    def export_workflow(self, export_location=None):
        """Exports the workflow to the directory location specified by the user.

            Args:
                export_location     (str)   --  Directory where the workflow would be exported

                    default: None

            Returns:
                str     -   absolute path of the exported workflow xml file

            Raises:
                SDKException:
                    if export_location does not exist

                    if no workflow exists with the given name

                    if response is empty

                    if response is not success

                    if failed to write to export file

        """
        workflow_name = self._workflow_name

        if not self._commcell_object.workflows.has_workflow(workflow_name):
            raise SDKException('Workflow', '104')

        if export_location is None:
            export_location = os.getcwd()
        else:
            if not isinstance(export_location, basestring):
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

    def clone_workflow(self, clone_workflow_name):
        """Clones the workflow

        Args:
            clone_workflow_name (str)   : name for the new workflow(clone)

        Raises:
            SDKException:
                if response is not status

                If cloning workflow operation fails
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

    def schedule_workflow(self, schedule_pattern, workflow_inputs=None):
        """ Creates a schedule for a workflow

             Args:
                  schedule_pattern(dict)    -- Please refer SchedulePattern.create_schedule in
                                            schedules.py for the types of pattern to be sent

                                     eg: {
                                            "schedule_name: 'schedule1',
                                            "freq_type": 'daily',
                                            "active_start_time": time_in_%H/%S (str),
                                            "repeat_days": days_to_repeat (int)
                                         }

                  workflow_inputs(dict) --  dictionary consisting of inputs for the workflow

                    if inputs are not given, user will be prompted for inputs on the command line

                    default: None

                    inputs dict format:

                    {
                            'input1_name': 'input1_value',

                            'input2_name': 'input2_value'
                    }

                    e.g.:

                    for executing the Demo_CheckReadiness workflow, inputs dict would be:

                    {
                    "ClientGroupName": "client_group_value"
                    }

             Returns:
                     Object : An instance of the Schedule class for the schedule created
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

    def _process_workflow_schedule_response(self, flag, response):
        """
        processes the response received post create schedule request
        Args:
        flag: (bool) -- True or false based on response
        response: (dict) response from modify request
        Returns:
            flag: (Bool) -- based on success and failure
            error_code: (int) -- error_code from response
            error_message: (str) -- error_message from the response if any
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

    def refresh(self):
        """Refreshes the properties of the workflow."""
        self._get_workflow_properties()

    @property
    def workflow_name(self):
        """Treats the workflow name as a read-only attribute."""
        return self._workflow_name

    @property
    def workflow_id(self):
        """Treats the workflow id as a read-only attribute."""
        return self._workflow_id

    @property
    def version(self):
        """Treats the workflow version as a property of the Workflow class."""
        return self._properties['version']

    @property
    def revision(self):
        """Treats the workflow revision as a property of the Workflow class."""
        return self._properties['revision']

    @property
    def flags(self):
        """Treats the workflow flags as a property of the Workflow class."""
        return self._properties['flags']

    @property
    def description(self):
        """Treats the workflow description as a property of the Workflow class."""
        return self._description

    @description.setter
    def description(self, value):
        """Sets the description of the workflow

            Raises:
                SDKException:
                    if failed to update description of workflow

                    if the type of value input is not string
        """
        if isinstance(value, basestring):
            self._set_workflow_properties("description", value)
        else:
            raise SDKException(
                'Workflow', '102', 'Failed to set workflow description'
            )
