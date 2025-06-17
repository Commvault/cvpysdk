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

"""Main file for performing Monitoring related operations on the commcell.

This file has all the classes related to Monitoring operations.

MonitoringPolicies:      Class for representing all the monitoring policies
                            configured in the commcell.

MonitoringPolicy:        Class for representing a single monitoring policy
                            configured in the commcell.

MonitoringPolicies:

    __init__(commcell_object)       --  initialize the MonitoringPolicies class
                                            instance for the commcell

    __str__()                       --  returns all the monitoring policies
                                            associated with the commcell

    __repr__()                      --  returns the string for the instance
                                            of the MonitoringPolicy class

    _get_monitoring_policies()      --  gets all the monitoring policies
                                            of the commcell

    has_monitoring_policy()         --  checks if a monitoring policy exists
                                            with the given name or not

    _get_analytics_servers()        --  returns all the analytics servers
                                            associated with the commcell

    has_analytics_server()          --  checks if a analytics server exists
                                            with the given name or not

    _get_templates()                --  returns all the templates
                                            associated with the commcell

    has_template()                  --  checks if a template exists
                                            with the given name or not

    get()                           --  Returns  a MonitoringPolicy object
                                        of the specified monitoring policy name

    add()                           --  adds a new monitoring policy to the commcell

    delete()                        --  deletes a monitoring policy

    refresh()                       -- refreshes the MonitoringPolicies/Templates
                                            and Analytics Servers
                                            associated to the commcell

Attributes
==========

    **all_analytics_servers**       -- returns the dictionary consisting of
    all the analytics servers that are associated with the commcell and their
    information such as cloudid and analyticsserver name

    **all_templates**               -- returns the dictionary consisting of
    all the templates that are associated with the commcell and their
    information such as templateid and templatename

    **all_monitoring_policies       -- returns the dictionary consisting of
    all the monitoring policies that are associated with the commcell and
    their information such as monitoringpolicyid and name


MonitoringPolicy:

    __init__(commcell_object,
             monitoring_policy_name,
             monitoring_policy_id)            --  initializes the instance of
                                                    MonitoringPolicy class
                                                    for a specific MonitoringPolicy
                                                    of the commcell

    __repr__()                                --  returns a string representation
                                                    of the MonitoringPolicy instance

    _get_monitoring_policy_id()            --  gets the id of the MonitoringPolicy
                                                    instance from the commcell

    run()                                     --  starts a Monitoring Policy job
                                                    and returns a job object

Attributes
==========

    **monitoring_policy_name**          -- returns the monitoringpolicy name

    **monitoring_policy_id**            -- returnd the id of monitoringpolicy
"""

from .exception import SDKException
from .job import Job


class MonitoringPolicies(object):
    """Class for representing all the Monitoring Policies
        configured in the commcell."""

    def __init__(self, commcell_object):
        """Intializes object of the MonitoringPolicies class.

            Args:
                commcell_object (object) -instance of the commcell class

            Returns:
                object - instance of the MonitoringPolicies class
        """

        self._commcell_object = commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._MONITORING_POLICIES = self._services['GET_ALL_MONITORING_POLICIES']
        self._ANALYTICS_SERVERS = self._services['GET_ALL_ANALYTICS_SERVERS']
        self._TEMPLATES = self._services['GET_ALL_TEMPLATES']
        self._MONITORING_POLICIES_OPERATIONS = self._services[
            'CREATE_DELETE_EDIT_OPERATIONS'
        ]
        self._monitoring_policies = None
        self._analytics_servers = None
        self._templates = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all MonitoringPolicies of the commcell.

            Returns:
                str - string of all the monitoring policies
                    associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S.No.',
                                                           'Monitoring Policy')

        for index, monitoring_policy in enumerate(self.all_monitoring_policies):
            sub_str = '{:^5}\t{:^20}\n\n'.format(index + 1, monitoring_policy)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the MonitoringPolicies class."""
        return "MonitoringPolicies class instance for Commcell"

    def _get_monitoring_policies(self):
        """Gets all the Monitoring Policies associated to the commcell
            specified by commcell object.

                Returns:
                    dict - consists of all monitoring policies of the commcell
                        {
                             "monitoring_policy_name1":monitoring_policy_id1,
                             "monitoring_policy_name2":monitoring_policy_id2
                        }
                Raises:
                    SDKException:
                        if response is empty

                        if response is not success
        """
        request = {
                "flag": 2, "appType": 1
            }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._MONITORING_POLICIES, request)

        if flag:
            if response.json() and 'monitoringPolicies' in response.json():
                monitoring_policies_dict = {}

                for dictionary in response.json()['monitoringPolicies']:
                    temp_name = dictionary['monitoringPolicyName'].lower()
                    temp_id = int(dictionary['monitoringPolicyid'])
                    monitoring_policies_dict[temp_name] = temp_id

                return monitoring_policies_dict

            return {}
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_analytics_servers(self):
        """Returns the dictionary consisting of all the analytics servers
            and their info.

            dict - consists of all analytics servers in the commcell
                {
                    "analytics_server_1":cloud_id1,
                    "analytics_server_2":cloud_id2
                }
        """
        return self._analytics_servers

    @property
    def all_templates(self):
        """Returns the dictionary consisting of all the templates
            and their info.

            dict - consists of all templates in the commcell
                {
                     "template_name1":{
                         "id":template_id1,
                         "type":template_type
                    },
                    "template_name2":{
                        "id":template_id2,
                        "type":template_type
                    }
                }
        """
        return self._templates

    @property
    def all_monitoring_policies(self):
        """Returns the dictionary consisting of all the
            monitoringpolicies and their info.

            dict - consists of all the monitoringpolicies
                    in the commcell
                {
                    "monitoring_policy_name1":monitoring_policy_id1,
                    "monitoring_policy_name2":monitoring_policy_id2
                }
        """
        return self._monitoring_policies

    def has_monitoring_policy(self, monitoring_policy_name):
        """checks if a moniotoring policy exists in the commcell
                with the provided name

            Args:
                monitoring_policy_name (str) -- name of the monitoring policy

            Returns:
                bool - boolean output whether the monitoring policy
                    exists in the commcell or not

            Raises:
                SDKException:
                    if type of the monitoring_policy_name is not string
        """

        if not isinstance(monitoring_policy_name, str):
            raise SDKException('Monitoring', '101')

        return self.all_monitoring_policies and monitoring_policy_name.lower() in \
            self.all_monitoring_policies

    def _get_analytics_servers(self):
        """Gets all the analytics servers associated to the commcell
                specified by commcell object.

            Returns:
                dict - consists of all analytics servers of the commcell
                    {
                         "analytics_server_1":cloud_id1
                         "analytics_server_2":cloud_id2
                    }
            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._ANALYTICS_SERVERS
        )

        if flag:
            if response.json() and 'listOfCIServer' in response.json():
                analytics_servers_dict = {}

                for dictionary in response.json()['listOfCIServer']:
                    temp_name = dictionary['internalCloudName'].lower()
                    temp_id = int(dictionary['cloudID'])
                    analytics_servers_dict[temp_name] = temp_id

                return analytics_servers_dict

            return {}
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_analytics_server(self, analytics_server_name):
        """Checks if a analytics server exists in the commcell
            with the input analytics server name

            Args:
                analytics_server_name (str) -- name of the analytics server

            Returns:
                bool - boolean output whether the analytics server
                    exists in the commcell or not

            Raises:
                SDKException:
                    if type of the analytics server name is not string

        """

        if not isinstance(analytics_server_name, str):
            raise SDKException('Monitoring', '101')

        return self.all_analytics_servers and analytics_server_name.lower() in \
            self.all_analytics_servers

    def _get_templates(self):
        """Gets all the templates associated to the commcell
            specified by commcell object.

                Returns:
                    dict- consists of all templates of the commcell
                        {
                             "template_name1": {
                                 "id":template_id1,
                                 "type":template_type
                            },
                            "template_name2": {
                                "id":template_id2,
                                "type":template_type
                            }
                        }
                Raises:
                    SDKException:
                        if response is empty

                        if response is not success
        """

        xml_request = """<GetListofTemplatesByTemplateId templateId=""
        includeTemplateXML="" appType="" flag=""></GetListofTemplatesByTemplateId>"""

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._TEMPLATES, xml_request
        )

        if flag:
            if response.json() and 'LMTemplates' in response.json():
                templates_dict = {}

                for dictionary in response.json()['LMTemplates']:
                    temp_name = dictionary['LMTemplateEntity']['templateName'].lower()
                    temp_id = int(dictionary['LMTemplateEntity']['templateId'])
                    temp_type = int(dictionary['templateForMonitoringType'])
                    templates_dict[temp_name] = {
                        'id' : temp_id,
                        'type' : temp_type
                    }

                return templates_dict

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_template(self, template_name):
        """Checks if a template exists in the commcell with the input template name.

            Args:
                template_name(str) -- name of the template

            Returns:
                bool- boolean output whether the template exists
                    in the commcell or not

            Raises:
                SDKException:
                    if type of the library name argument is not string
        """
        if not isinstance(template_name, str):
            raise SDKException('Monitoring', '101')

        return self.all_templates and template_name.lower() in self.all_templates

    def get(self, monitoring_policy_name):
        """Returns  a MonitoringPolicy object of the specified monitoring policy name.

            Args:
                monitoring_policy_name (str) - name of the monitoring policy

            Returns:
                object - instance of the MonitoringPolicy class
                    for the given policy name

            Raises:
                SDKException:
                    if type of the monitoring policy name argument is not string

                    if no monitoring policy exists with the given name
        """
        if not isinstance(monitoring_policy_name, str):
            raise SDKException('Monitoring', '101')

        monitoring_policy_name = monitoring_policy_name.lower()

        if not self.has_monitoring_policy(monitoring_policy_name):
            raise SDKException(
                'Monitoring',
                '102',
                'No policy exists with name :{0}'.format(monitoring_policy_name))

        return MonitoringPolicy(
            self._commcell_object,
            monitoring_policy_name,
            self.all_monitoring_policies[monitoring_policy_name]
        )

    def add(self,
            monitoring_policy_name,
            template_name,
            analytics_server_name,
            client_name,
            content=None,
            win_flag=False,
            policy_type=0,
            **kwargs):
        """Adds a new Monitoring Policy to the Commcell.

            Args:
                monitoring_policy_name (str) -- name of the new monitoring
                                                    policy to add

                template_name (str)          -- name of the template
                                                    that has to be used

                analytics_server_name (str)  -- name of the Analytics Server
                                                    with LM role

                client_name (str)            -- client from which data
                                                    has to be picked

                content (str)                     -- content to be used for
                                                    running the policy

                win_flag (bool)                    -- For executing Text based
                                                    WindowsEvents Policy

                policy_type (int)                -- type of policy to be created 0 - index server 1 - event raiser

                kwargs                          -- continuousMode - true/false, conditionsXML - criteria for policy

            Raises:
                SDKException:
                    if template doesn't exists

                    if Analytics Server doesn't exists

                    if Client doesn't exists

                    if creation of Monitoring Policy fails

                    if response is empty

                    if response is not success
        """
        template_name = template_name.lower()
        client_name = client_name.lower()
        template_dict = {}
        cloud_id = 0
        if analytics_server_name is None:
            analytics_server_name = ''

        if template_name == "ondemand":
            template_id = 1
            template_type = 4
        elif win_flag:
            template_id = 2
            template_type = 0
        else:
            if self.has_template(template_name):
                # template_dict = self.all_templates
                template_id = int(self.all_templates[template_name]['id'])
                template_type = int(self.all_templates[template_name]['type'])
            else:
                err_msg = 'Template "{0}" doesn\'t exist'.format(template_name)
                raise SDKException('Monitoring', '102', err_msg)

        if content is None:
            content = ""

        if policy_type==0:
            analytics_server_name = analytics_server_name.lower()
            if self.has_analytics_server(analytics_server_name):
                cloud_id = self.all_analytics_servers[analytics_server_name]
            else:
                err_msg = 'Analytics Server "{0}" doesn\'t exist'.format(
                    analytics_server_name
                )
                raise SDKException('Monitoring', '102', err_msg)

        client_dict = {}
        if self._commcell_object.clients.has_client(client_name):
            client_dict = self._commcell_object.clients.all_clients
            client_id = int(client_dict[client_name]['id'])
        else:
            err_msg = 'Client "{0}" doesn\'t exist'.format(client_name)
            raise SDKException('Monitoring', '102', err_msg)

        request = {
            "op": 1,
            "policy": {
                "monitoringPolicyName": monitoring_policy_name,
                "monitoringPolicyid": 0,
                "content": content,
                "continuousMode": kwargs.get('continuousMode',False),
                "indexAllLines": False if kwargs.get('conditionsXML') else True,
                "associations": [{
                    "clientName": client_name,
                    "clientId": client_id,
                    "_type_": 3
                }],
                "monitoringTypes": [
                    template_type
                ],
                "LMTemplates": [{
                    "templateName": template_name,
                    "templateId": template_id
                }],
                "criteria": [
                    {
                        "conditionsXML": kwargs.get('conditionsXML',''),
                        "templateId": template_id
                    }
                ],
                "dataCapturingOptions": {
                    "cloudId": cloud_id,
                    "ageCIDataAfterDays": 15,
                    "cloudName": analytics_server_name,
                    "doNotMonitorOldData": False,
                    "enableContentIndexing": True,
                    "asFtp": False,
                    "dataCapturingType": policy_type,
                    "captureEntireFile": False
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._MONITORING_POLICIES_OPERATIONS, request)

        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code != 0:
                    error_string = response.json()['errorMessage']
                    raise SDKException(
                        'Monitoring',
                        '102',
                        'Failed to create MonitoringPolicy\nError: "{0}"'.format(
                            error_string
                        )
                    )
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return self.get(monitoring_policy_name)

    def delete(self, monitoring_policy_name):
        """Deletes the monitoring policy from the commcell.

            Args:
                monitoring_policy_name(str) -- name of the monitoring policy to delete

            Raises:
                SDKException:
                    if type of the monitoring policy name argument is not string

                    if failed to delete monitoring policy

                    if response is empty

                    if response is not succcess
        """
        if not isinstance(monitoring_policy_name, str):
            raise SDKException('Monitoring', '101')
        else:
            monitoring_policy_name = monitoring_policy_name.lower()

            if self.has_monitoring_policy(monitoring_policy_name):
                request = {
                    "op": 3,
                    "policy": {
                        "monitoringPolicyName": monitoring_policy_name,
                        "monitoringTypes": [0]
                    }
                }
                flag, response = self._cvpysdk_object.make_request(
                    'POST', self._MONITORING_POLICIES_OPERATIONS, request)

                self.refresh()

                if flag:
                    if response.json():
                        error_code = response.json()['errorCode']

                        if error_code != 0:
                            error_string = response.json()['errorMessage']
                            raise SDKException(
                                'Monitoring', '102'
                                'Failed to delete MonitoringPolicy\nError: "{0}"'
                                .format(
                                    error_string
                                )
                            )

                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._update_response_(
                        response.text
                    )
                    raise SDKException('Response', '101', response_string)
            else:
                err_msg = 'MonitoringPolicy "{0}" doesn\'t exist'.format(
                    monitoring_policy_name
                )
                raise SDKException('Monitoring', '102', err_msg)

    def refresh(self):
        """Refreshes the monitoring policies/analytics servers
            and templates associated with the commcell"""

        self._monitoring_policies = self._get_monitoring_policies()
        self._analytics_servers = self._get_analytics_servers()
        self._templates = self._get_templates()


class MonitoringPolicy(object):
    """"Class for performing monitoring policy operations
            for a specific monitoring policy"""

    def __init__(self, commcell_object, monitoring_policy_name,
                 monitoring_policy_id=None):
        """Initialise the Monitoring Policy class instance."""

        self._monitoring_policy_name = monitoring_policy_name.lower()
        self._commcell_object = commcell_object
        self._update_response_ = self._commcell_object._update_response_

        if monitoring_policy_id:
            self._monitoring_policy_id = str(monitoring_policy_id)
        else:
            self._monitoring_policy_id = self._get_monitoring_policy_id()

        self._RUN_MONITORING_POLICY = self._commcell_object._services[
            'RUN_MONITORING_POLICY'] % (self._monitoring_policy_id)

    def __repr__(self):
        """String representation of the instance of this class"""
        representation_string = 'Monitoring Policy class instance ' \
                                'for Monitoring Policy: "{0}"'
        return representation_string.format(self.monitoring_policy_name)

    def _get_monitoring_policy_id(self):
        """Gets the monitoring policy id associated with the monitoring policy."""
        monitoring_policies = MonitoringPolicies(self._commcell_object)
        return monitoring_policies.get(self.monitoring_policy_name).\
            monitoring_policy_id

    @property
    def monitoring_policy_name(self):
        """Treats the monitoring policy name as read only attribute."""
        return self._monitoring_policy_name

    @property
    def monitoring_policy_id(self):
        """Treats the monitoring policy id as read only attribute."""
        return self._monitoring_policy_id

    def run(self):
        """Runs the Monitoring Policy job"""

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._RUN_MONITORING_POLICY)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    o_str = 'Intializing Monitoring Policy Job failed\nError: "{0}"'\
                        .format(response.json()['errorMessage'])
                    raise SDKException('Monitoring', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
