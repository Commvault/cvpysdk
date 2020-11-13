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

"""Main file for performing agent specific operations.

Agents and Agent are 2 classes defined in this file.

Agents:     Class for representing all the agents associated with a specific client

Agent:      Class for a single agent selected for a client, and to perform operations on that agent


Agents:
    __init__(client_object)     --  initialize object of Agents class associated with
    the specified client

    __str__()                   --  returns all the agents associated with the client

    __repr__()                  --  returns the string for the instance of the Agents class

    __len__()                   -- returns the number of agents licensed for the selected Client

    __getitem__()               -- returns the name of the agent for the given agent Id or the
    details for the given agent name

    _get_agents()               --  gets all the agents associated with the client specified

    all_agents()                --  returns the dict of all the agents installed on client

    has_agent(agent_name)       --  checks if an agent exists with the given name

    get(agent_name)             --  returns the Agent class object of the input agent name

    refresh()                   --  refresh the agents installed on the client

    _process_add_response()     --  processes add agent request response

    add_database_agent()        --  adds database agent


Agent:
    __init__(client_object,
             agent_name,
             agent_id=None)     --   initialize object of Agent with the specified agent name
    and id, and associated to the specified client

    __repr__()                  --   return the agent name, the instance is associated with

    _get_agent_id()             --   method to get the agent id

    _get_agent_properties()     --   get the properties of this agent

    _process_update_request()   --  to process the request using API call

    update_properties()         --  to update the agent properties

    enable_backup()             --   enables the backup for the agent

    enable_backup_at_time()     --   enables the backup for the agent at the input time specified

    disble_backup()             --   disbles the backup for the agent

    enable_restore()            --   enables the restore for the agent

    enable_restore_at_time()    --   enables the restore for the agent at the input time specified

    disble_restore()            --   disbles the restore for the agent

    is_backup_enabled()         --   returns boolean specifying whether backup is enabled or not

    is_restore_enabled()        --   returns boolean specifying whether restore is enabled or not

    refresh()                   --   refresh the object properties

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import string
import time
import copy

from past.builtins import basestring

from .instance import Instances
from .backupset import Backupsets
from .schedules import Schedules
from .exception import SDKException


class Agents(object):
    """Class for getting all the agents associated with a client."""

    def __init__(self, client_object):
        """Initialize object of the Agents class.

            Args:
                client_object (object)  --  instance of the Client class

            Returns:
                object - instance of the Agents class
        """
        self._client_object = client_object
        self._commcell_object = self._client_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._AGENTS = self._services['GET_ALL_AGENTS'] % (self._client_object.client_id)

        self._agents = None
        self.refresh()

        from .agents.exchange_database_agent import ExchangeDatabaseAgent

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        self._agents_dict = {
            'exchange database': ExchangeDatabaseAgent
        }

    def __str__(self):
        """Representation string consisting of all agents of the client.

            Returns:
                str     -   string of all the agents of a client

        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\n\n'.format('S. No.', 'Agent', 'Client')

        for index, agent in enumerate(self._agents):
            sub_str = '{:^5}\t{:20}\t{:20}\n'.format(
                index + 1,
                agent,
                self._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Agents class."""
        return "Agents class instance for Client: '{0}'".format(self._client_object.client_name)

    def __len__(self):
        """Returns the number of the Agents licensed for the selected Client."""
        return len(self.all_agents)

    def __getitem__(self, value):
        """Returns the name of the agent for the given agent ID or
            the details of the agent for given agent Name.

            Args:
                value   (str / int)     --  Name or ID of the agent

            Returns:
                str     -   name of the agent, if the agent id was given

                dict    -   dict of details of the agent, if agent name was given

            Raises:
                IndexError:
                    no agent exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_agents:
            return self.all_agents[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_agents.items()))[0][0]
            except IndexError:
                raise IndexError('No agent exists with the given Name / Id')

    def _get_agents(self):
        """Gets all the agents associated to the client specified with this client object.

            Returns:
                dict - consists of all agents in the client
                    {
                         "agent1_name": agent1_id,
                         "agent2_name": agent2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._AGENTS)

        if flag:
            if response.json() and 'agentProperties' in response.json():

                agent_dict = {}

                for dictionary in response.json()['agentProperties']:
                    temp_name = dictionary['idaEntity']['appName'].lower()
                    temp_id = str(dictionary['idaEntity']['applicationId']).lower()
                    agent_dict[temp_name] = temp_id

                return agent_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_agents(self):
        """Returns dict of all the agents installed on client.

            dict    -   consists of all agents in the client

                {
                    "agent1_name": agent1_id,

                    "agent2_name": agent2_id
                }

        """
        return self._agents

    def has_agent(self, agent_name):
        """Checks if an agent is installed for the client with the input agent name.

            Args:
                agent_name (str)  --  name of the agent

            Returns:
                bool - boolean output whether the agent is installed for the client or not

            Raises:
                SDKException:
                    if type of the agent name argument is not string
        """
        if not isinstance(agent_name, basestring):
            raise SDKException('Agent', '101')

        return self._agents and agent_name.lower() in self._agents

    def get(self, agent_name):
        """Returns a agent object of the specified client.

            Args:
                agent_name (str)  --  name of the agent

            Returns:
                object - instance of the Agent class for the given agent name

            Raises:
                SDKException:
                    if type of the agent name argument is not string

                    if no agent exists with the given name
        """
        if not isinstance(agent_name, basestring):
            raise SDKException('Agent', '101')
        else:
            agent_name = agent_name.lower()

            if self.has_agent(agent_name):
                updated_agent_name = agent_name
                if "file system" in agent_name:
                    updated_agent_name = "file system"
                return self._agents_dict.get(agent_name, Agent)(
                    self._client_object, updated_agent_name, self._agents[agent_name]
                )

            raise SDKException('Agent', '102', 'No agent exists with name: {0}'.format(agent_name))

    def refresh(self):
        """Refresh the agents installed on the Client."""
        self._agents = self._get_agents()

    def _process_add_response(self, request_json):
        """Runs the Agent Add API with the request JSON provided,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                (bool, basestring, basestring):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._services['AGENT'], request_json)
        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response'][0]['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response'][0]['errorString']
                        o_str = 'Failed to create agent\nError: "{0}"'.format(error_string)
                        raise SDKException('Agent', '102', o_str)
                    else:
                        # initialize the agetns again
                        # so the agent object has all the agents
                        agent_name = request_json['association']['entity'][0]['appName']
                        self.refresh()
                        return self.get(agent_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create agent\nError: "{0}"'.format(error_string)
                    raise SDKException('Agent', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_database_agent(self, agent_name, access_node, **kwargs):
        """Adds database agent to cloud client
            Args:
                agent_name      (str)   --  agent name
                access_node     (str)   --  access node name
                **kwargs        (dict)  --  dict of keyword arguments as follows
                                            install_dir     (str)   --  database client install directory
                                            version         (str)   --  database version
            Returns:
                object - instance of the Agent class

            Raises:
                SDKException:
                  if agent with given name already exists

                    if failed to add the agent

                    if response is empty

                    if response is not success
        """

        if self.has_agent(agent_name):
            raise SDKException(
                'Agent', '102', 'Agent "{0}" already exists.'.format(
                    agent_name)
            )

        request_json = {
            "createAgent": True,
            "association": {
                "entity": [
                    {
                        "clientName": self._client_object.client_name,
                        "appName": agent_name
                    }
                ]
            },
            "agentProperties": {
                "AgentProperties": {
                    "createIndexOnFail": False,
                    "createIndexOnFull": False,
                    "installDate": 0,
                    "userDescription": "",
                    "runTrueUpJobAfterDaysForOnePass": 0,
                    "maxSimultaneousStubRecoveries": 0,
                    "agentVersion": "",
                    "isTrueUpOptionEnabledForOnePass": False
                },
                "cloudDbConfig": {
                    "enabled": True,
                    "dbProxyClientList": [
                        {
                            "dbSoftwareConfigList": [
                                {
                                    "installDir": kwargs.get("install_dir", ""),
                                    "version": kwargs.get("version", "10.0")
                                }
                            ],
                            "client": {
                                "clientName": access_node
                            }
                        }
                    ]
                },
                "idaEntity": {
                    "clientName": self._client_object.client_name,
                    "appName": agent_name
                }
            }
        }
        self._process_add_response(request_json)


class Agent(object):
    """Class for performing agent operations of an agent for a specific client."""

    def __init__(self, client_object, agent_name, agent_id=None):
        """Initialize the instance of the Agent class.

            Args:
                client_object   (object)    --  instance of the Client class

                agent_name      (str)       --  name of the agent

                    (File System, Virtual Server, etc.)

                agent_id        (str)       --  id of the agent

                    default: None

            Returns:
                object  -   instance of the Agent class

        """
        self._client_object = client_object
        self._commcell_object = self._client_object._commcell_object
        self._agent_name = agent_name.lower()

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._AGENT = self._services['AGENT']

        if agent_id:
            # Use the agent id mentioned in the arguments
            self._agent_id = str(agent_id)
        else:
            # Get the agent id if agent id is not provided
            self._agent_id = self._get_agent_id()

        self.GET_AGENT = self._services['GET_AGENT'] % (self._client_object.client_id, self._agent_id)

        self._agent_properties = None

        self._instances = None
        self._backupsets = None
        self._schedules = None

        self.refresh()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = '"{0}" Agent instance for Client: "{1}"'

        return representation_string.format(
            string.capwords(self.agent_name), self._client_object.client_name
        )

    def _get_agent_id(self):
        """Gets the agent id associated with this agent.

            Returns:
                str - id associated with this agent
        """
        agents = Agents(self._client_object)
        return agents.get(self.agent_name).agent_id

    def _get_agent_properties(self):
        """Gets the agent properties of this agent.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self.GET_AGENT)

        if flag:
            if response.json() and 'agentProperties' in response.json():
                self._agent_properties = response.json()['agentProperties'][0]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _request_json_(self, option, enable=True, enable_time=None):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                option  (str)   --  string option for which to run the API for

                    e.g.; Backup / Restore

            Returns:
                dict    -   JSON request to pass to the API

        """
        options_dict = {
            "Backup": 1,
            "Restore": 2
        }

        request_json1 = {
            "association": {
                "entity": [{
                    "clientName": self._client_object.client_name,
                    "appName": self.agent_name
                }]
            },
            "agentProperties": {
                "idaActivityControl": {
                    "activityControlOptions": [{
                        "activityType": options_dict[option],
                        "enableAfterADelay": False,
                        "enableActivityType": enable
                    }]
                }
            }
        }

        request_json2 = {
            "association": {
                "entity": [{
                    "clientName": self._client_object.client_name,
                    "appName": self.agent_name
                }]
            },
            "agentProperties": {
                "idaActivityControl": {
                    "activityControlOptions": [{
                        "activityType": options_dict[option],
                        "enableAfterADelay": True,
                        "enableActivityType": False,
                        "dateTime": {
                            "TimeZoneName": self._commcell_object.default_timezone,
                            "timeValue": enable_time
                        }
                    }]
                }
            }
        }

        if enable_time:
            return request_json2
        else:
            return request_json1

    def _process_update_request(self, request_json):
        """Runs the Agent update API

            Args:
                request_json    (dict)  -- request json sent as payload

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self.GET_AGENT, request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    if response.json()['response'][0].get('errorCode', 0):
                        error_message = response.json()['errorMessage']
                        raise SDKException(
                            'Agent', '102', 'Failed to update Agent properties\nError: "{0}"'.format(error_message))
                    self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def update_properties(self, properties_dict):
        """Updates the agent properties

            Args:
                properties_dict (dict)  --  agent property dict which is to be updated

            Returns:
                None

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected

        **Note** self.properties can be used to get a deep copy of all the properties, modify the properties which you
        need to change and use the update_properties method to set the properties

        """
        request_json = {
            "agentProperties":
                {
                    "AgentProperties": {},
                    "idaEntity": {
                        "appName": self.agent_name,
                        "clientName": self._client_object.client_name,
                        "commCellName": self._commcell_object.commserv_name
                    },
                }
        }

        request_json['agentProperties'].update(properties_dict)

        self._process_update_request(request_json)

    @property
    def properties(self):
        """Returns the agent properties"""
        return copy.deepcopy(self._agent_properties)

    @property
    def name(self):
        """Returns the Agent display name """
        return self._agent_properties['idaEntity']['appName']

    @property
    def description(self):
        """Returns the description of the Agent"""
        return self._agent_properties.get('AgentProperties', {}).get('userDescription')

    @description.setter
    def description(self, description):
        """Sets the description for the agent

        Args:
            description (str)   -- Description to be set for the agent

        """
        update_properties = self.properties
        update_properties['AgentProperties']['userDescription'] = description
        self.update_properties(update_properties)

    @property
    def agent_id(self):
        """Returns the id of the Agent."""
        return self._agent_id

    @property
    def agent_name(self):
        """Returns the name of the Agent."""
        return self._agent_name

    @property
    def is_backup_enabled(self):
        """Returns boolean specifying whether backup is enabled for this agent or not."""
        for activitytype in self._agent_properties['idaActivityControl']['activityControlOptions']:
            if activitytype['activityType'] == 1:
                return activitytype['enableActivityType']

        return False

    @property
    def is_restore_enabled(self):
        """Returns boolean specifying whether restore is enabled for this agent or not."""
        for activitytype in self._agent_properties['idaActivityControl']['activityControlOptions']:
            if activitytype['activityType'] == 2:
                return activitytype['enableActivityType']

        return False

    @property
    def instances(self):
        """Returns the instance of the Instances class representing the list of Instances
        installed / configured on the Client for the selected Agent.
        """
        if self._instances is None:
            self._instances = Instances(self)

        return self._instances

    @property
    def backupsets(self):
        """Returns the instance of the Backupsets class representing the list of Backupsets
        installed / configured on the Client for the selected Agent.
        """
        if self._backupsets is None:
            self._backupsets = Backupsets(self)

        return self._backupsets

    @property
    def schedules(self):
        """Returns the instance of the Schedules class representing the list of Schedules
        installed / configured on the Client for the selected Agent.
        """
        if self._schedules is None:
            self._schedules = Schedules(self)

        return self._schedules

    def enable_backup(self):
        """Enable Backup for this Agent.

            Raises:
                SDKException:
                    if failed to enable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Backup')

        flag, response = self._cvpysdk_object.make_request('POST', self._AGENT, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']

                    o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
                    raise SDKException('Agent', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_backup_at_time(self, enable_time):
        """Disables Backup if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

                **Note** In case of linux CommServer provide time in GMT timezone

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable backup

                    if response is empty

                    if response is not success
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('Agent', '103')
        except ValueError:
            raise SDKException('Agent', '104')

        request_json = self._request_json_('Backup', False, enable_time)

        flag, response = self._cvpysdk_object.make_request('POST', self._AGENT, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']

                    o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
                    raise SDKException('Agent', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def disable_backup(self):
        """Disables Backup for this Agent.

            Raises:
                SDKException:
                    if failed to disable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Backup', False)

        flag, response = self._cvpysdk_object.make_request('POST', self._AGENT, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']

                    o_str = 'Failed to disable Backup\nError: "{0}"'.format(error_message)
                    raise SDKException('Agent', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_restore(self):
        """Enable Restore for this Agent.

            Raises:
                SDKException:
                    if failed to enable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Restore')

        flag, response = self._cvpysdk_object.make_request('POST', self._AGENT, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']

                    o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
                    raise SDKException('Agent', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def enable_restore_at_time(self, enable_time):
        """Disables Restore if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the restore at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable restore

                    if response is empty

                    if response is not success
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('Agent', '103')
        except ValueError:
            raise SDKException('Agent', '104')

        request_json = self._request_json_('Restore', False, enable_time)

        flag, response = self._cvpysdk_object.make_request('POST', self._AGENT, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']

                    o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
                    raise SDKException('Agent', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def disable_restore(self):
        """Disables Restore for this Agent.

            Raises:
                SDKException:
                    if failed to disable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Restore', False)

        flag, response = self._cvpysdk_object.make_request('POST', self._AGENT, request_json)

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    return
                elif 'errorString' in response.json()['response'][0]:
                    error_message = response.json()['response'][0]['errorString']
                    o_str = 'Failed to disable Backup\nError: "{0}"'.format(error_message)
                    raise SDKException('Agent', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def refresh(self):
        """Refresh the properties of the Agent."""
        self._get_agent_properties()

        self._instances = None
        self._backupsets = None
        self._schedules = None
