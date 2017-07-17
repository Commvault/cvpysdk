#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing Workflow operations on Commcell.

WorkFlow: Class for handling all Workflows, and running a Workflow job

WorkFlow:
    __init__(commcell_object)           --  initialise instance of the WorkFlow class

    __repr__()                          --  returns all the workflows deployed in the commcell

    _get_workflows()                    --  gets all the workflows deployed on the commcell

    _read_inputs_()                     --  gets the values for a workflow input

    has_workflow(workflow_name)         --  checks if the workflow exists with given name or not

    import_workflow(workflow_xml)       --  imports a workflow to the Commcell

    deploy_workflow()                   --  deploys a workflow to the Commcell

    execute_workflow(workflow_name)     --  executes a workflow and returns the job instance

    delete_workflow(workflow_name)      --  deletes a workflow from the commcell

    _download_workflow(workflow_name)   --  downloads given workflow from the cloud.commvault.com

"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from base64 import b64decode

from past.builtins import basestring
from past.builtins import raw_input

from .job import Job
from .exception import SDKException


class WorkFlow(object):
    """Class for representing all workflows of a commcell."""

    def __init__(self, commcell_object):
        """Initialize the WorkFlow class instance for performing workflow related operations.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the WorkFlow class
        """
        self._commcell_object = commcell_object
        self._WORKFLOWS = self._commcell_object._services['GET_WORKFLOWS']
        self._DEPLOY_WORKFLOW = self._commcell_object._services['DEPLOY_WORKFLOW']
        self._EXECUTE_WORKFLOW = self._commcell_object._services['EXECUTE_WORKFLOW']

        self._workflows = self._get_workflows()

    def __str__(self):
        """Representation string consisting of all workflows of the Commcell.

            Returns:
                str - string of all the workflows associated with the commcell
        """
        representation_string = '{:^5}\t{:^50}\t{:^60}\t{:^30}\n\n'.format(
            'S. No.', 'Workflow Name', 'Description', 'Client'
        )

        for index, workflow in enumerate(self._workflows):
            workflow_vals = self._workflows[workflow]
            workflow_desciption = workflow_vals['description']

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

                for index, wf_input in enumerate(workflow_inputs):
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
                        index + 1,
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
            self._commcell_object._headers['Host']
        )

    def _get_workflows(self):
        """Gets all the workflows associated to the commcell.

            Returns:
                dict - consists of all workflows in the commcell

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._WORKFLOWS)

        if flag:
            if response.json() and 'container' in response.json():
                workflow_dict = {}

                for workflow in response.json()['container']:
                    workflow_name = workflow['entity']['workflowName'].lower()
                    workflow_id = str(workflow['entity']['workflowId'])
                    workflow_description = workflow['description']

                    if 'deployments' in workflow:
                        workflow_client = workflow['deployments'][0]['client']['clientName']

                        if 'entries' in workflow['deployments'][0]['inputForm']:
                            workflow_inputs = []

                            for a_input in workflow['deployments'][0]['inputForm']['entries']:
                                workflow_input = {}

                                input_name = a_input['inputName']

                                if 'displayName' in a_input:
                                    display_name = a_input['displayName']
                                else:
                                    display_name = None

                                if 'documentation' in a_input:
                                    documentation = a_input['documentation']
                                else:
                                    documentation = None

                                if 'defaultValue' in a_input:
                                    default_value = a_input['defaultValue']
                                else:
                                    default_value = None

                                if 'required' in a_input:
                                    required = a_input['required']
                                else:
                                    required = False

                                workflow_input['input_name'] = input_name
                                workflow_input['display_name'] = display_name
                                workflow_input['documentation'] = documentation
                                workflow_input['default_value'] = default_value
                                workflow_input['is_required'] = required

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _read_inputs_(self, input_dict):
        """Gets the values from the user for a workflow input.
            If user provieds empty value, then default value is returned for the workflow input,
                if it is specified.
            Else, prompts the user again for the input.

            Args:
                input_dict (dict)   --  dictionary containing the values for a workflow input
                    {'input_name', 'display_name', 'documentation', 'default_value', 'is_required'}

            Returns:
                str - value entered by the user for the workflow input
        """
        if input_dict['display_name'] is not None:
            prompt = input_dict['display_name']
        else:
            prompt = input_dict['input_name']

        if input_dict['is_required']:
            value = raw_input(prompt + '*' + '::  ')
        else:
            value = raw_input(prompt + '::  ')

        if value:
            return value
        elif input_dict['default_value']:
            return input_dict['default_value']
        else:
            return self._read_inputs_(input_dict)

    def has_workflow(self, workflow_name):
        """Checks if a workflow exists in the commcell with the input workflow name.

            Args:
                workflow_name (str)  --  name of the workflow

            Returns:
                bool - boolean output whether the workflow exists in the commcell or not

            Raises:
                SDKException:
                    if type of the workflow name argument is not string
        """
        if not isinstance(workflow_name, basestring):
            raise SDKException('Workflow', '101')

        return self._workflows and workflow_name.lower() in self._workflows

    def import_workflow(self, workflow_xml):
        """Imports a workflow to the Commcell.

            Args:
                workflow_xml    (str)   --  path of the workflow xml file

            Raises:
                SDKException:
                    if type of the workflow xml argument is not string

                    if workflow xml is not a valid file

                    if HTTP Status Code is not SUCCESS / importing workflow failed
        """
        if not isinstance(workflow_xml, basestring):
            raise SDKException('Workflow', '101')

        if os.path.isfile(workflow_xml):
            with open(workflow_xml, 'r') as file_object:
                workflow_xml = file_object.read()
        else:
            raise SDKException('Workflow', '103')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._WORKFLOWS, workflow_xml
        )

        self._workflows = self._get_workflows()

        if flag is False:
            raise SDKException(
                'Workflow', '102', 'Importing Workflow failed. {0}'.format(response.json())
            )

    def deploy_workflow(self, workflow_name, workflow_engine=None, workflow_xml=None):
        """Deploys a workflow on the Commcell.

            Args:
                workflow_name       (str)   --  name of the workflow

                workflow_engine     (str)   --  name of the client to deploy the workflow on
                    default: None

                workflow_xml        (str)   --  path of the workflow xml file
                    default: None

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if workflow xml argument is given and is not of type string

                    if no workflow exists with the given name

                    if workflow xml is given and is not a valid file

                    if failed to deploy workflow

                    if response is empty

                    if response is not success
        """
        if not (isinstance(workflow_name, basestring) or
                (workflow_engine is not None and isinstance(workflow_engine, basestring)) or
                (workflow_xml is not None and isinstance(workflow_xml, basestring))):
            raise SDKException('Workflow', '101')

        workflow_name = workflow_name.lower()

        if not self.has_workflow(workflow_name):
            raise SDKException(
                'Workflow', '102', 'No workflow exists with name: {0}'.format(workflow_name)
            )

        workflow_deploy_service = self._DEPLOY_WORKFLOW % self._workflows[workflow_name]['id']

        if workflow_xml is None:
            workflow_xml = {
                "Workflow_DeployWorkflow": {}
            }

            if workflow_engine is not None:
                workflow_xml['Workflow_DeployWorkflow']['client']['clientName'] = workflow_engine
        elif os.path.isfile(workflow_xml):
            with open(workflow_xml, 'r') as file_object:
                workflow_xml = file_object.read()
        else:
            raise SDKException('Workflow', '103')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', workflow_deploy_service, workflow_xml
        )

        self._workflows = self._get_workflows()

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def execute_workflow(self, workflow_name):
        """Executes the workflow with the workflow name given as input, and returns its job id.

            Args:
                workflow_name (str)  --  name of the workflow

            Returns:
                object - instance of the Job class for this workflow job

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if failed to execute workflow

                    if response is empty

                    if response is not success

                    if no workflow exists with the given name
        """
        if not isinstance(workflow_name, basestring):
            raise SDKException('Workflow', '101')

        workflow_name = workflow_name.lower()

        if self.has_workflow(workflow_name):
            workflow_vals = self._workflows[workflow_name]

            execute_workflow_json = {}

            if 'inputs' in workflow_vals:
                o_str = 'Workflow Name: \t\t"{0}"\n'.format(workflow_name)
                o_str += 'Workflow Description: \t"{0}"\n'.format(workflow_vals['description'])

                print(o_str)

                for a_input in workflow_vals['inputs']:
                    execute_workflow_json[a_input['input_name']] = self._read_inputs_(a_input)

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._EXECUTE_WORKFLOW % workflow_name, execute_workflow_json
            )

            if flag:
                if response.json():
                    if "jobId" in response.json():
                        if response.json()["jobId"] == 0:
                            return 'Workflow Execution Finished Successfully'
                        else:
                            return Job(self._commcell_object, response.json()['jobId'])
                    elif "errorCode" in response.json():
                        if response.json()['errorCode'] == 0:
                            return 'Workflow Execution Finished Successfully'
                        else:
                            error_message = response.json()['errorMessage']
                            o_str = 'Executing Workflow failed\nError: "{0}"'.format(error_message)
                            raise SDKException('Workflow', '102', o_str)
                    else:
                        return response.json()
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Workflow', '102', 'No workflow exists with name: {0}'.format(workflow_name)
            )

    def delete_workflow(self, workflow_name):
        """Deletes a workflow from the Commcell.

            Args:
                workflow_name    (str)   --  name of the workflow to remove

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

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._WORKFLOWS, workflow_xml
        )

        self._workflows = self._get_workflows()

        if flag is False:
            raise SDKException(
                'Workflow', '102', 'Deleting Workflow failed. {0}'.format(response.json())
            )

    def _download_workflow(self, workflow_name, download_location, cloud_username, cloud_password):
        """Downloads workflow from Software Store.

            Args:
                workflow_name       (str)   --  name of the workflow to download

                download_location   (str)   --  location to download the workflow at

                cloud_username      (str)   --  username for the cloud account

                cloud_password      (str)   --  password for the above username

            Raises:
                SDKException:
                    if type of the workflow name argument is not string

                    if HTTP Status Code is not SUCCESS / download workflow failed
        """
        if not isinstance(workflow_name, basestring):
            raise SDKException('Workflow', '101')

        from .commcell import Commcell

        cloud_commcell = Commcell('cloud.commvault.com', cloud_username, cloud_password)
        flag, response = cloud_commcell._cvpysdk_object.make_request(
            'GET', cloud_commcell._services['SOFTWARESTORE_PKGINFO'] % (workflow_name)
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

        flag, response = cloud_commcell._cvpysdk_object.make_request(
            'POST', cloud_commcell._services['SOFTWARESTORE_DOWNLOADITEM'], download_xml
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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
