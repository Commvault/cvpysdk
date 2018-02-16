# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing agent specific operations.

Agents and Agent are 2 classes defined in this file.

Agents:     Class for representing all the agents associated with a specific client

Agent:      Class for a single agent selected for a client, and to perform operations on that agent


Agents:
    __init__(client_object)     --  initialise object of Agents class associated with
    the specified client

    __str__()                   --  returns all the agents associated with the client

    __repr__()                  --  returns the string for the instance of the Agents class

    _get_agents()               --  gets all the agents associated with the client specified

    all_agents()                --  returns the dict of all the agents installed on client

    has_agent(agent_name)       --  checks if an agent exists with the given name

    get(agent_name)             --  returns the Agent class object of the input agent name

    refresh()                   --  refresh the agents installed on the client


Agent:
    __init__(client_object,
             agent_name,
             agent_id=None)     --   initialise object of Agent with the specified agent name
    and id, and associated to the specified client

    __repr__()                  --   return the agent name, the instance is associated with

    _get_agent_id()             --   method to get the agent id

    _get_agent_properties()     --   get the properties of this agent

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

from past.builtins import basestring

from .backupset import Backupsets
from .instance import Instances
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

        self._AGENTS = self._commcell_object._services['GET_ALL_AGENTS'] % (
            self._client_object.client_id
        )

        self._agents = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all agents of the client.

            Returns:
                str - string of all the agents of a client
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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._AGENTS)

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_agents(self):
        """Returns dict of all the agents installed on client
        
            dict - consists of all agents in the client
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
                return Agent(self._client_object, agent_name, self._agents[agent_name])

            raise SDKException('Agent', '102', 'No agent exists with name: {0}'.format(agent_name))

    def refresh(self):
        """Refresh the agents installed on the Client."""
        self._agents = self._get_agents()


class Agent(object):
    """Class for performing agent operations of an agent for a specific client."""

    def __init__(self, client_object, agent_name, agent_id=None):
        """Initialise the agent object.

            Args:
                client_object (object)  --  instance of the Client class to which the agent belongs

                agent_name    (str)     --  name of the agent (File System, Virtual Server, etc.)

                agent_id      (str)     --  id of the associated agent
                    default: None

            Returns:
                object - instance of the Agent class
        """
        self._client_object = client_object
        self._commcell_object = self._client_object._commcell_object
        self._agent_name = agent_name.lower()

        self._AGENT = self._commcell_object._services['AGENT']

        if agent_id:
            # Use the agent id mentioned in the arguments
            self._agent_id = str(agent_id)
        else:
            # Get the agent id if agent id is not provided
            self._agent_id = self._get_agent_id()

        self.GET_AGENT = self._commcell_object._services['GET_AGENT'] % (
            self._client_object.client_id, agent_id
        )

        self._agent_properties = None
        self.instances = None
        self.backupsets = None
        self.schedules = None

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self.GET_AGENT)

        if flag:
            if response.json() and 'agentProperties' in response.json():
                self._agent_properties = response.json()['agentProperties'][0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _request_json_(self, option, enable=True, enable_time=None):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                option (str)  --  string option for which to run the API for
                    e.g.; Backup / Restore

            Returns:
                dict - JSON request to pass to the API
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
                            "TimeZoneName": "(UTC) Coordinated Universal Time",
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

    @property
    def agent_id(self):
        """Treats the agent id as a read-only attribute."""
        return self._agent_id

    @property
    def agent_name(self):
        """Treats the agent name as a read-only attribute."""
        return self._agent_name

    def enable_backup(self):
        """Enable Backup for this Agent.

            Raises:
                SDKException:
                    if failed to enable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Backup')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._AGENT, request_json
        )

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_backup_at_time(self, enable_time):
        """Disables Backup if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

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

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._AGENT, request_json
        )

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_backup(self):
        """Disables Backup for this Agent.

            Raises:
                SDKException:
                    if failed to disable backup

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Backup', False)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._AGENT, request_json
        )

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_restore(self):
        """Enable Restore for this Agent.

            Raises:
                SDKException:
                    if failed to enable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Restore')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._AGENT, request_json
        )

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._AGENT, request_json
        )

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_restore(self):
        """Disables Restore for this Agent.

            Raises:
                SDKException:
                    if failed to disable restore

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_('Restore', False)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._AGENT, request_json
        )

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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

    def refresh(self):
        """Refresh the properties of the Agent."""
        self._get_agent_properties()

        self.instances = Instances(self)
        self.backupsets = Backupsets(self)
        self.schedules = Schedules(self)
