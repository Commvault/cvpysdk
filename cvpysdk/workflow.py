#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing Workflow operations on Commcell via REST API.

WorkFlow: Class for handling all Workflows, and running a Workflow job

WorkFlow:
    __init__(commcell_object)       --  initialise instance of the WorkFlow class
    __repr__()                      --  returns all the workflows deployed in the commcell
    _get_workflows()                --  gets all the workflows deployed on the commcell
    has_workflow(workflow_name)     --  checks if the workflow exists with the given name or not

"""

from __future__ import absolute_import

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

        self._workflows = self._get_workflows()

    def __str__(self):
        """Representation string consisting of all workflows of the Commcell.

            Returns:
                str - string of all the workflows associated with the commcell
        """
        representation_string = '{:^5}\t{:^50}\t{:^60}\t{:^30}\n\n'.format(
            'S. No.', 'Workflow Name', 'Description', 'Client')

        for index, workflow in enumerate(self._workflows.items()):
            sub_str = '{:^5}\t{:50}\t{:60}\t{:^30}\n'.format(
                index + 1,
                workflow[0],
                workflow[1][0],
                workflow[1][1] if len(workflow[1]) > 1 else "  --  ")

            representation_string += sub_str

            if len(workflow[1]) > 1:
                workflow_inputs = workflow[1][2]
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
                    input_name, display_name, description, default_value, is_required = wf_input
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
                    workflow_name = str(workflow['entity']['workflowName'])
                    workflow_description = str(workflow['description'])

                    if 'deployments' in workflow:
                        workflow_client = str(workflow['deployments'][0]['client']['clientName'])

                        if 'entries' in workflow['deployments'][0]['inputForm']:
                            workflow_inputs = []
                            for a_input in workflow['deployments'][0]['inputForm']['entries']:
                                input_name = str(a_input['inputName'])

                                if 'displayName' in a_input:
                                    display_name = str(a_input['displayName'])
                                else:
                                    display_name = '  ----  '

                                if 'documentation' in a_input:
                                    documentation = str(a_input['documentation'])
                                else:
                                    documentation = '  ----  '

                                if 'defaultValue' in a_input:
                                    default_value = str(a_input['defaultValue'])
                                else:
                                    default_value = '  ----  '

                                if 'required' in a_input:
                                    required = a_input['required']
                                else:
                                    required = False

                                workflow_inputs.append(
                                    [
                                        input_name,
                                        display_name,
                                        documentation,
                                        default_value,
                                        required
                                    ]
                                )
                        else:
                            workflow_inputs = []

                        workflow_dict[workflow_name] = [workflow_description,
                                                        workflow_client,
                                                        workflow_inputs]
                    else:
                        workflow_dict[workflow_name] = [workflow_description]

                return workflow_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
