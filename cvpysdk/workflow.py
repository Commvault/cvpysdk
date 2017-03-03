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
    __init__(commcell_object)       --  initialise instance of the WorkFlow class

    __repr__()                      --  returns all the workflows deployed in the commcell

    _get_workflows()                --  gets all the workflows deployed on the commcell

    _read_inputs_()                 --  gets the values for a workflow input

    has_workflow(workflow_name)     --  checks if the workflow exists with the given name or not

    execute_workflow(workflow_name) --  executes a workflow and returns the job instance

"""

from __future__ import absolute_import

import xmltodict

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
        self._WORKFLOWS = self._commcell_object._services.GET_WORKFLOWS
        self._EXECUTE_WORKFLOW = self._commcell_object._services.EXECUTE_WORKFLOW

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
                    workflow_name = str(workflow['entity']['workflowName']).lower()
                    workflow_description = str(workflow['description'])

                    if 'deployments' in workflow:
                        workflow_client = str(workflow['deployments'][0]['client']['clientName'])

                        if 'entries' in workflow['deployments'][0]['inputForm']:
                            workflow_inputs = []

                            for a_input in workflow['deployments'][0]['inputForm']['entries']:
                                workflow_input = {}

                                input_name = str(a_input['inputName'])

                                if 'displayName' in a_input:
                                    display_name = str(a_input['displayName'])
                                else:
                                    display_name = None

                                if 'documentation' in a_input:
                                    documentation = str(a_input['documentation'])
                                else:
                                    documentation = None

                                if 'defaultValue' in a_input:
                                    default_value = str(a_input['defaultValue'])
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
                            'inputs': workflow_inputs
                        }
                    else:
                        workflow_dict[workflow_name] = {
                            'description': workflow_description
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
            value = input(prompt + '*' + '::  ')
        else:
            value = input(prompt + '::  ')

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
        if not isinstance(workflow_name, str):
            raise SDKException('Workflow', '101')

        return self._workflows and str(workflow_name).lower() in self._workflows

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
        if not isinstance(workflow_name, str):
            raise SDKException('Workflow', '101')

        workflow_name = str(workflow_name).lower()

        if self.has_workflow(workflow_name):
            workflow_vals = self._workflows[workflow_name]

            execute_workflow_json = {}
            inputs = {}

            if 'inputs' in workflow_vals:
                o_str = 'Workflow Name: \t\t"{0}"\n'.format(workflow_name)
                o_str += 'Workflow Description: \t"{0}"\n'.format(workflow_vals['description'])

                print(o_str)

                for a_input in workflow_vals['inputs']:
                    inputs[a_input['input_name']] = self._read_inputs_(a_input)

            if inputs:
                execute_workflow_json['inputs'] = inputs

            # Temporarily use XML here till the time API does not support JSON
            xml = xmltodict.unparse(execute_workflow_json)

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._EXECUTE_WORKFLOW % workflow_name, xml
            )

            if flag:
                if response.json():
                    if "jobId" in response.json():
                        return Job(self._commcell_object, response.json()['jobId'])
                    elif "errorCode" in response.json():
                        error_message = response.json()['errorMessage']

                        o_str = 'Executing Workflow failed\nError: "{0}"'.format(error_message)
                        raise SDKException('Workflow', '102', o_str)
                    else:
                        raise SDKException('Workflow', '102', 'Failed to execute the workflow')
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Workflow', '102', 'No workflow exists with name: {0}'.format(workflow_name)
            )
