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

import copy
import string
import time
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from .constants import AppIDAName
from .instance import Instances
from .backupset import Backupsets
from .schedules import Schedules
from .exception import SDKException
if TYPE_CHECKING:
    from .client import Client

class Agents(object):
    """
    Manages and interacts with agents associated with a client.

    The Agents class provides a comprehensive interface for retrieving, managing,
    and interacting with agents linked to a specific client object. It supports
    agent enumeration, access, addition, and refresh operations, making it easy
    to handle agent-related tasks programmatically.

    Key Features:
        - Initialization with a client object for context
        - String and representation methods for readable output
        - Length and item access for agent collection-like behavior
        - Retrieval of all agents via the `all_agents` property
        - Check for existence of an agent by name
        - Get a specific agent by name
        - Refresh the agent list from the source
        - Add a new database agent with specified access node
        - Internal processing of agent addition responses

    #ai-gen-doc
    """

    def __init__(self, client_object: 'Client') -> None:
        """Initialize an Agents object for managing agents on a specific client.

        Args:
            client_object: Instance of the Client class representing the target client.

        Example:
            >>> client = Client(...)
            >>> agents = Agents(client)
            >>> # The Agents object can now be used to manage agents for the specified client

        #ai-gen-doc
        """
        self._client_object = client_object
        self._commcell_object = self._client_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._AGENTS = self._services['GET_ALL_AGENTS'] % (self._client_object.client_id)

        self._agents = None
        self.refresh()

    def __str__(self) -> str:
        """Return a formatted string representation of all agents associated with the client.

        The output includes a table listing the serial number, agent name, and client name for each agent.

        Returns:
            Formatted string listing all agents of the client.

        Example:
            >>> agents = Agents(client_object)
            >>> print(str(agents))
            >>> # Output:
            >>> # S. No.   Agent                Client
            >>> #
            >>> #   1      FileSystem           ClientA
            >>> #   2      SQLServer            ClientA

        #ai-gen-doc
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

    def __repr__(self) -> str:
        """Return a string representation of the Agents class instance.

        This method provides a human-readable description of the Agents object,
        including the associated client name.

        Returns:
            String representation of the Agents instance.

        Example:
            >>> agents = Agents(client_object)
            >>> print(repr(agents))
            Agents class instance for Client: 'Client01'

        #ai-gen-doc
        """
        return "Agents class instance for Client: '{0}'".format(self._client_object.client_name)

    def __len__(self) -> int:
        """Get the number of agents licensed for the selected client.

        Returns:
            The total count of licensed agents as an integer.

        Example:
            >>> agents = Agents(client_object)
            >>> num_agents = len(agents)
            >>> print(f"Licensed agents: {num_agents}")

        #ai-gen-doc
        """
        return len(self.all_agents)

    def __getitem__(self, value: Union[str, int]) -> Union[str, Dict[str, Any]]:
        """Retrieve agent information by agent ID or agent name.

        If an agent ID (as int or str) is provided, returns the name of the agent.
        If an agent name (as str) is provided, returns the details dictionary for that agent.

        Args:
            value: The agent's name (str) or ID (int or str).

        Returns:
            str: Name of the agent if the agent ID was provided.
            dict: Details of the agent if the agent name was provided.

        Raises:
            IndexError: If no agent exists with the given name or ID.

        Example:
            >>> agents = Agents()
            >>> # Get agent details by name
            >>> details = agents['FileSystem']
            >>> print(details)
            >>> # Get agent name by ID
            >>> name = agents[101]
            >>> print(f"Agent name for ID 101: {name}")

        #ai-gen-doc
        """
        value = str(value)

        if value in self.all_agents:
            return self.all_agents[value]
        else:
            try:
                return list(filter(lambda x: x[1] == value, self.all_agents.items()))[0][0]
            except IndexError:
                raise IndexError('No agent exists with the given Name / Id')

    def _get_agents(self) -> Dict[str, str]:
        """Retrieve all agents associated with the current client object.

        Returns:
            Dictionary mapping agent names (as lowercase strings) to their corresponding agent IDs.
            Example:
                {
                    "agent1_name": "agent1_id",
                    "agent2_name": "agent2_id"
                }

        Raises:
            SDKException: If the response is empty or unsuccessful.

        Example:
            >>> agents = client_obj._get_agents()
            >>> print(agents)
            >>> # Output: {'file_system': '1', 'sql_server': '2'}
            >>> # Each key is the agent name, and each value is the agent ID as a string.

        #ai-gen-doc
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
            elif self._client_object.vm_guid is not None and not self._client_object.properties.get('clientProps', {}).\
                    get('isIndexingV2VSA', False):
                return {}
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_agents(self) -> Dict[str, int]:
        """Get a dictionary of all agents installed on the client.

        Returns:
            Dictionary mapping agent names (str) to their corresponding agent IDs (int).

        Example:
            >>> agents = Agents(client_object)
            >>> agent_dict = agents.all_agents  # Use dot notation for property access
            >>> print(agent_dict)
            >>> # Output: {'FileSystem': 1, 'SQLServer': 2}
            >>> # You can access agent IDs by name:
            >>> fs_agent_id = agent_dict.get('FileSystem')
            >>> print(f"FileSystem agent ID: {fs_agent_id}")

        #ai-gen-doc
        """
        return self._agents

    def has_agent(self, agent_name: str) -> bool:
        """Check if a specific agent is installed for the client.

        Args:
            agent_name: Name of the agent to check, as a string.

        Returns:
            True if the agent is installed for the client, False otherwise.

        Raises:
            SDKException: If the agent_name argument is not a string.

        Example:
            >>> agents = Agents(client_object)
            >>> is_installed = agents.has_agent("File System")
            >>> print(f"File System agent installed: {is_installed}")
            >>> # Returns True if the agent is present, False otherwise

        #ai-gen-doc
        """
        if not isinstance(agent_name, str):
            raise SDKException('Agent', '101')

        return self._agents and agent_name.lower() in self._agents

    def get(self, agent_name: str) -> 'Agent':
        """Retrieve an Agent object for the specified agent name.

        Args:
            agent_name: Name of the agent as a string.

        Returns:
            Agent instance corresponding to the given agent name.

        Raises:
            SDKException: If the agent_name is not a string or if no agent exists with the given name.

        Example:
            >>> agents = Agents(client_object)
            >>> file_system_agent = agents.get('File System')
            >>> print(f"Retrieved agent: {file_system_agent}")
            >>> # The returned Agent object can be used for further agent operations

        #ai-gen-doc
        """
        if not isinstance(agent_name, str):
            raise SDKException('Agent', '101')
        else:
            agent_name = agent_name.lower()

            if self.has_agent(agent_name):
                return Agent(self._client_object, agent_name, self._agents[agent_name])

            raise SDKException('Agent', '102', 'No agent exists with name: {0}'.format(agent_name))

    def refresh(self) -> None:
        """Reload the list of agents installed on the client.

        This method updates the internal agent cache to reflect the current state
        of agents installed on the client. Use this method to ensure you are working
        with the latest agent information.

        Example:
            >>> agents = Agents(client_object)
            >>> agents.refresh()  # Refresh the agent list after installation or removal
            >>> print("Agent list refreshed successfully")

        #ai-gen-doc
        """
        self._agents = self._get_agents()

    def _process_add_response(self, request_json: Dict[str, Any]) -> Any:
        """Process the response from the Agent Add API using the provided request JSON.

        This method sends a POST request to the Agent Add API with the given JSON payload,
        parses the response, and returns the created agent object if successful. If the API
        response indicates an error or is empty, an SDKException is raised.

        Args:
            request_json: Dictionary containing the JSON request payload for the Agent Add API.

        Returns:
            The agent object corresponding to the newly created agent if the operation is successful.

        Raises:
            SDKException: If the API response is empty, indicates failure, or contains an error message.

        Example:
            >>> agents = Agents(commcell_object)
            >>> request_json = {
            ...     "association": {
            ...         "entity": [{"appName": "File System"}]
            ...     },
            ...     "properties": {...}
            ... }
            >>> new_agent = agents._process_add_response(request_json)
            >>> print(f"Agent created: {new_agent}")
        #ai-gen-doc
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

    def add_database_agent(self, agent_name: str, access_node: str, **kwargs: Any):
        """Add a database agent to the cloud client.

        This method creates and associates a new database agent with the specified cloud client,
        using the provided agent name and access node. Additional configuration options such as
        installation directory and database version can be specified via keyword arguments.

        Args:
            agent_name: Name of the database agent to add.
            access_node: Name of the access node client for the database agent.
            **kwargs: Optional keyword arguments for agent configuration:
                install_dir (str): Directory where the database client should be installed.
                version (str): Version of the database software (default is "10.0").

        Returns:
            Instance of the Agent class representing the newly added database agent.

        Raises:
            SDKException: If an agent with the given name already exists, if the agent addition fails,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> agents = Agents(client_object)
            >>> # Add a database agent with custom install directory and version
            >>> agent = agents.add_database_agent(
            ...     agent_name="SQLServer",
            ...     access_node="AccessNode01",
            ...     install_dir="/opt/dbclient",
            ...     version="12.0"
            ... )
            >>> print(f"Added agent: {agent}")

        #ai-gen-doc
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
    """
    Agent class for managing operations related to a specific client agent.

    This class provides a comprehensive interface for interacting with and managing
    agent entities associated with a client. It supports initialization, property
    management, backup and restore operations, and integration with Exchange On-Prem
    environments. The Agent class exposes various properties and methods to facilitate
    agent configuration, status monitoring, and operational control.

    Key Features:
        - Agent instantiation and representation
        - Retrieval of agent ID and properties
        - JSON-based request handling for agent operations
        - Processing and updating agent properties
        - Access to agent metadata (name, description, ID)
        - Backup and restore enable/disable operations (immediate or scheduled)
        - Support for Exchange On-Prem EWS integration
        - Access to related entities: instances, backupsets, schedules
        - Refreshing agent state and properties

    #ai-gen-doc
    """
    def __new__(cls, client_object: Any, agent_name: str, agent_id: Optional[int] = None):
        """Create a new instance of the Agent class or its specialized subclass.

        This method dynamically selects the appropriate agent subclass based on the provided
        agent_name. If a specialized agent class exists for the given agent_name, an instance
        of that class is created; otherwise, a generic Agent instance is returned.

        Args:
            client_object: The client object associated with the agent. Type may vary depending on context.
            agent_name: Name of the agent as a string (e.g., 'exchange database').
            agent_id: Optional identifier for the agent.

        Example:
            >>> client = Client(...)
            >>> agent = Agent(client, 'exchange database', agent_id=101)
            >>> print(type(agent))
            <class 'cvpysdk.agents.exchange_database_agent.ExchangeDatabaseAgent'>
            >>> # For unknown agent names, a generic Agent instance is returned
            >>> generic_agent = Agent(client, 'unknown_agent')
            >>> print(type(generic_agent))
            <class 'Agent'>

        #ai-gen-doc
        """
        from cvpysdk.agents.exchange_database_agent import ExchangeDatabaseAgent
        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        _agents_dict = {
            'exchange database': ExchangeDatabaseAgent
        }

        if agent_name in _agents_dict:
            _class = _agents_dict.get(agent_name, cls)
            if _class.__new__ == cls.__new__:
                return object.__new__(_class)
            return _class.__new__(_class, client_object, agent_name, agent_id)
        else:
            return object.__new__(cls)

    def __init__(self, client_object: 'Client', agent_name: str, agent_id: Optional[str] = None) -> None:
        """Initialize an Agent instance for the specified client and agent name.

        Args:
            client_object: Instance of the Client class representing the target client.
            agent_name: Name of the agent (e.g., "File System", "Virtual Server").
            agent_id: Optional string specifying the agent ID. If not provided, the agent ID will be determined automatically.

        Example:
            >>> client = Client(...)
            >>> agent = Agent(client, "File System")
            >>> # Optionally specify agent_id
            >>> agent_with_id = Agent(client, "Virtual Server", agent_id="12345")

        #ai-gen-doc
        """
        self._client_object = client_object
        self._commcell_object = self._client_object._commcell_object
        self._agent_name = (AppIDAName.FILE_SYSTEM.value.lower()
                            if AppIDAName.FILE_SYSTEM.value.lower() in agent_name.lower() else agent_name.lower())

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

    def __repr__(self) -> str:
        """Return a string representation of the Agent instance.

        The returned string includes the agent name (capitalized) and the associated client name.

        Returns:
            A formatted string describing the Agent instance and its client.

        Example:
            >>> agent = Agent(...)
            >>> print(repr(agent))
            "File System" Agent instance for Client: "Server01"

        #ai-gen-doc
        """
        representation_string = '"{0}" Agent instance for Client: "{1}"'

        return representation_string.format(
            string.capwords(self.agent_name), self._client_object.client_name
        )

    def _get_agent_id(self) -> str:
        """Retrieve the agent ID associated with this Agent instance.

        Returns:
            The unique agent ID as a string.

        Example:
            >>> agent = Agent(client_object, agent_name)
            >>> agent_id = agent._get_agent_id()
            >>> print(f"Agent ID: {agent_id}")

        #ai-gen-doc
        """
        agents = Agents(self._client_object)
        return agents.get(self.agent_name).agent_id

    def _get_agent_properties(self) -> None:
        """Retrieve and update the agent properties for this Agent instance.

        This method sends a GET request to fetch the agent properties from the Commcell server.
        The retrieved properties are stored in the internal `_agent_properties` attribute.

        Raises:
            SDKException: If the response is empty or unsuccessful.

        Example:
            >>> agent = Agent(commcell_object, agent_name)
            >>> agent._get_agent_properties()
            >>> # The agent's properties are now updated and accessible via agent._agent_properties

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self.GET_AGENT)

        if flag:
            if response.json() and 'agentProperties' in response.json():
                self._agent_properties = response.json()['agentProperties'][0]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _request_json_(self, option: str, enable: bool = True, enable_time: Optional[int] = None) -> Dict[str, Any]:
        """Generate the JSON request payload for the API based on the selected option.

        Args:
            option: The operation type for which to generate the API request (e.g., "Backup" or "Restore").
            enable: Whether to enable the activity type immediately. Defaults to True.
            enable_time: Optional epoch time (as an integer) to enable the activity type after a delay. If provided, the request will include delayed activation.

        Returns:
            Dictionary representing the JSON request to be sent to the API.

        Example:
            >>> agent = Agent(...)
            >>> # Immediate backup activity
            >>> backup_request = agent._request_json_("Backup", enable=True)
            >>> print(backup_request)
            >>> # Delayed restore activity
            >>> restore_request = agent._request_json_("Restore", enable=False, enable_time=1680307200)
            >>> print(restore_request)

        #ai-gen-doc
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

    def _process_update_request(self, request_json: Dict[str, Any]) -> None:
        """Run the Agent update API with the provided request payload.

        This method sends an update request for the Agent using the specified JSON payload.
        It validates the response and raises an SDKException if the update fails or if the response is empty.

        Args:
            request_json: Dictionary containing the request payload for the Agent update.

        Raises:
            SDKException: If the response is empty or the update operation is unsuccessful.

        Example:
            >>> agent = Agent(...)
            >>> update_payload = {"property": "value"}
            >>> agent._process_update_request(update_payload)
            >>> # If the update fails, an SDKException will be raised

        #ai-gen-doc
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

    def update_properties(self, properties_dict: Dict[str, Any]) -> None:
        """Update the agent properties with the specified values.

        This method updates the agent's configuration using the provided dictionary of properties.
        To modify agent properties, obtain a deep copy using `self.properties`, update the desired fields,
        and pass the modified dictionary to this method.

        Args:
            properties_dict: Dictionary containing agent property values to update.

        Raises:
            SDKException: If the update fails, the response is empty, or the response code is not as expected.

        Example:
            >>> agent = Agent(...)
            >>> props = agent.properties.copy()  # Get a deep copy of current properties
            >>> props['AgentProperties']['someProperty'] = 'newValue'
            >>> agent.update_properties(props)
            >>> print("Agent properties updated successfully")
        #ai-gen-doc
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
    def properties(self) -> Dict[str, Any]:
        """Get a copy of the agent's properties.

        Returns:
            Dictionary containing the agent's properties and configuration details.

        Example:
            >>> agent = Agent(...)
            >>> agent_props = agent.properties  # Use dot notation for properties
            >>> print(agent_props)
            >>> # The returned dictionary contains agent-specific settings

        #ai-gen-doc
        """
        return copy.deepcopy(self._agent_properties)

    @property
    def name(self) -> str:
        """Get the display name of the Agent.

        Returns:
            The Agent's display name as a string.

        Example:
            >>> agent = Agent(...)
            >>> display_name = agent.name  # Use dot notation for property access
            >>> print(f"Agent display name: {display_name}")

        #ai-gen-doc
        """
        return self._agent_properties['idaEntity']['appName']

    @property
    def description(self) -> Optional[str]:
        """Get the user-defined description of the Agent.

        Returns:
            The description of the Agent as a string, or None if not set.

        Example:
            >>> agent = Agent(...)
            >>> desc = agent.description  # Use dot notation for property access
            >>> print(f"Agent description: {desc}")

        #ai-gen-doc
        """
        return self._agent_properties.get('AgentProperties', {}).get('userDescription')

    @description.setter
    def description(self, description: str) -> None:
        """Set the description for the agent.

        Args:
            description: The description text to assign to the agent.

        Example:
            >>> agent = Agent(...)
            >>> agent.description = "This agent handles database backups."  # Use assignment for property setters
            >>> # The agent's description is now updated

        #ai-gen-doc
        """
        update_properties = self.properties
        update_properties['AgentProperties']['userDescription'] = description
        self.update_properties(update_properties)

    @property
    def agent_id(self) -> int:
        """Get the unique identifier of the Agent.

        Returns:
            The agent's ID as an integer.

        Example:
            >>> agent = Agent(...)
            >>> agent_id = agent.agent_id  # Use dot notation for property access
            >>> print(f"Agent ID: {agent_id}")
        #ai-gen-doc
        """
        return self._agent_id

    @property
    def agent_name(self) -> str:
        """Get the name of the Agent.

        Returns:
            The name of the Agent as a string.

        Example:
            >>> agent = Agent(...)
            >>> name = agent.agent_name  # Use dot notation for property access
            >>> print(f"Agent name: {name}")

        #ai-gen-doc
        """
        return self._agent_name

    @property
    def is_backup_enabled(self) -> bool:
        """Check if backup is enabled for this agent.

        Returns:
            True if backup is enabled for the agent, False otherwise.

        Example:
            >>> agent = Agent(...)
            >>> if agent.is_backup_enabled:
            ...     print("Backup is enabled for this agent.")
            ... else:
            ...     print("Backup is disabled for this agent.")

        #ai-gen-doc
        """
        for activitytype in self._agent_properties['idaActivityControl']['activityControlOptions']:
            if activitytype['activityType'] == 1:
                return activitytype['enableActivityType']

        return False

    @property
    def is_restore_enabled(self) -> bool:
        """Indicate whether restore operations are enabled for this agent.

        Returns:
            True if restore is enabled for the agent, False otherwise.

        Example:
            >>> agent = Agent(...)
            >>> if agent.is_restore_enabled:
            ...     print("Restore is enabled for this agent.")
            ... else:
            ...     print("Restore is disabled for this agent.")

        #ai-gen-doc
        """
        for activitytype in self._agent_properties['idaActivityControl']['activityControlOptions']:
            if activitytype['activityType'] == 2:
                return activitytype['enableActivityType']

        return False

    @property
    def instances(self) -> 'Instances':
        """Get the Instances object representing all instances configured for this Agent.

        Returns:
            Instances: An object for managing and accessing the list of instances installed or configured
            on the client for the selected Agent.

        Example:
            >>> agent = Agent(...)
            >>> instances = agent.instances  # Use dot notation for property access
            >>> print(f"Total instances: {len(instances)}")
            >>> # The returned Instances object can be used to manage individual instances

        #ai-gen-doc
        """
        if self._instances is None:
            self._instances = Instances(self)

        return self._instances

    @property
    def backupsets(self) -> 'Backupsets':
        """Get the Backupsets instance for the current Agent.

        This property provides access to the Backupsets object, which represents
        all backup sets installed or configured on the client for the selected agent.

        Returns:
            Backupsets: An instance for managing and accessing backup sets.

        Example:
            >>> agent = Agent(...)
            >>> backupsets = agent.backupsets  # Use dot notation for property access
            >>> print(f"Number of backup sets: {len(backupsets)}")
            >>> # The returned Backupsets object can be used to manage backup sets

        #ai-gen-doc
        """
        if self._backupsets is None:
            self._backupsets = Backupsets(self)

        return self._backupsets

    @property
    def schedules(self) -> 'Schedules':
        """Get the Schedules instance for the current Agent.

        This property provides access to the Schedules object, which represents all schedules
        installed or configured on the client for the selected agent.

        Returns:
            Schedules: An instance for managing and retrieving schedule information related to this agent.

        Example:
            >>> agent = Agent(...)
            >>> schedules = agent.schedules  # Use dot notation for property access
            >>> print(f"Schedules object: {schedules}")
            >>> # The returned Schedules object can be used to view or manage schedules

        #ai-gen-doc
        """
        if self._schedules is None:
            self._schedules = Schedules(self)

        return self._schedules

    def enable_backup(self) -> None:
        """Enable backup operations for this Agent.

        This method sends a request to enable backup for the current Agent instance.
        If the operation fails, or if the response is empty or unsuccessful, an SDKException is raised.

        Raises:
            SDKException: If enabling backup fails, the response is empty, or the response indicates an error.

        Example:
            >>> agent = Agent(...)
            >>> agent.enable_backup()
            >>> print("Backup enabled successfully for the agent.")
            # If an error occurs, SDKException will be raised.

        #ai-gen-doc
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

    def enable_backup_at_time(self, enable_time: str) -> None:
        """Schedule backup enablement at a specified UTC time.

        This method disables backup if it is currently enabled, and then schedules backup to be enabled
        at the provided UTC time. The time must be specified in 24-hour format as "YYYY-MM-DD HH:mm:ss".
        For Linux CommServer environments, provide the time in GMT timezone.

        Args:
            enable_time: UTC time to enable the backup, in "YYYY-MM-DD HH:mm:ss" format.

        Raises:
            SDKException: If the time value is less than the current time.
            SDKException: If the time value is not in the correct format.
            SDKException: If backup enablement fails.
            SDKException: If the response is empty or not successful.

        Example:
            >>> agent = Agent(...)
            >>> agent.enable_backup_at_time("2024-07-01 23:30:00")
            >>> print("Backup will be enabled at the specified time.")

        #ai-gen-doc
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

    def disable_backup(self) -> None:
        """Disable backup operations for this Agent.

        This method sends a request to disable backup for the current Agent instance.
        If the operation fails, or if the response is empty or unsuccessful, an SDKException is raised.

        Raises:
            SDKException: If the backup could not be disabled, the response is empty, or the response indicates failure.

        Example:
            >>> agent = Agent(...)
            >>> agent.disable_backup()
            >>> print("Backup disabled successfully for the agent.")
            # If the operation fails, an SDKException will be raised.

        #ai-gen-doc
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

    def enable_restore(self) -> None:
        """Enable restore functionality for this Agent.

        This method sends a request to enable restore operations for the current Agent instance.
        If the operation fails, an SDKException is raised with details about the failure.

        Raises:
            SDKException: If enabling restore fails, the response is empty, or the response indicates an error.

        Example:
            >>> agent = Agent(...)
            >>> agent.enable_restore()
            >>> print("Restore enabled successfully for the agent.")
            # If an error occurs, SDKException will be raised with the error details.

        #ai-gen-doc
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

    def enable_restore_at_time(self, enable_time: str) -> None:
        """Enable restore functionality at a specified UTC time.

        This method disables restore if it is not already disabled, and then schedules
        restore to be enabled at the provided UTC time in 24-hour format.

        Args:
            enable_time: UTC time to enable restore, in the format "YYYY-MM-DD HH:mm:ss".

        Raises:
            SDKException: If the provided time is earlier than the current time.
            SDKException: If the time format is incorrect.
            SDKException: If restore could not be enabled due to an error response.
            SDKException: If the response from the server is empty or unsuccessful.

        Example:
            >>> agent = Agent(...)
            >>> agent.enable_restore_at_time("2024-07-01 15:30:00")
            >>> # Restore will be enabled at the specified UTC time

        #ai-gen-doc
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

    def disable_restore(self) -> None:
        """Disable restore operations for this Agent.

        This method sends a request to the Commcell to disable restore functionality for the current Agent.
        If the operation fails, an SDKException is raised with details about the error.

        Raises:
            SDKException: If the request to disable restore fails, the response is empty, or the response indicates an error.

        Example:
            >>> agent = Agent(...)
            >>> agent.disable_restore()
            >>> print("Restore operations have been disabled for the agent.")
        #ai-gen-doc
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

    def enable_ews_support_for_exchange_on_prem(self, ews_service_url: str) -> None:
        """Enable EWS backup support for an Exchange on-premises client.

        This method configures the agent to use Exchange Web Services (EWS) for backup operations
        by setting the EWS connection URL and enabling EWS support. Only applicable for Exchange on-prem agents.

        Args:
            ews_service_url: The EWS connection URL for your Exchange server.

        Example:
            >>> agent = Agent(...)
            >>> agent.enable_ews_support_for_exchange_on_prem("https://exchange.example.com/EWS/Exchange.asmx")
            >>> print("EWS support enabled for Exchange on-prem client.")

        #ai-gen-doc
        """
        if int(self.agent_id) != 137:
            raise SDKException('Agent', '102', f'Invalid operation for {self.agent_name}')

        _agent_properties = self.properties
        _agent_properties["onePassProperties"]["onePassProp"]["ewsDetails"]["bUseEWS"] = True
        _agent_properties["onePassProperties"]["onePassProp"]["ewsDetails"]["ewsConnectionUrl"] = ews_service_url
        self.update_properties(_agent_properties)

    def refresh(self) -> None:
        """Reload the properties and cached data for the Agent object.

        This method refreshes the agent's properties and clears cached instances, backupsets,
        and schedules. Use this to ensure the Agent reflects the latest state from the Commcell.

        Example:
            >>> agent = Agent(commcell_object, client_name, agent_name)
            >>> agent.refresh()  # Updates agent properties and clears cached data
            >>> # Subsequent accesses will retrieve updated information

        #ai-gen-doc
        """
        self._get_agent_properties()

        self._instances = None
        self._backupsets = None
        self._schedules = None
