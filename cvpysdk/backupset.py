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

"""Main file for performing backup set operations.

Backupsets and Backupset are 2 classes defined in this file.

Backupsets: Class for representing all the backup sets associated with a specific agent

Backupset:  Class for a single backup set selected for an agent,
and to perform operations on that backup set


Backupsets:
===========
    __init__(class_object)          -- initialise object of Backupsets class associated with
    the specified agent/instance

    __str__()                       -- returns all the backupsets associated with the agent

    __repr__()                      -- returns the string for the instance of the Backupsets class

    __len__()                       -- returns the number of backupsets associated with the Agent

    __getitem__()                   -- returns the name of the backupset for the given backupset Id
    or the details for the given backupset name

    _get_backupsets()               -- gets all the backupsets associated with the agent specified

    default_backup_set()            -- returns the name of the default backup set

    all_backupsets()                -- returns the dict of all the backupsets for the Agent /
    Instance of the selected Client

    has_backupset(backupset_name)   -- checks if a backupset exists with the given name or not

    _process_add_response()         -- to process the add backupset request using API call

    add(backupset_name)             -- adds a new backupset to the agent of the specified client
    
    add_archiveset(archiveset_name)   -- adds a new archiveset to the agent of the specified client

    add_v1_sharepoint_client()      -- Adds a new Office 365 V1 Share Point Pseudo Client to the Commcell.

    add_salesforce_backupset()      -- adds a new salesforce backupset

    get(backupset_name)             -- returns the Backupset class object
    of the input backup set name

    delete(backupset_name)          -- removes the backupset from the agent of the specified client

    refresh()                       -- refresh the backupsets associated with the agent


Backupset:
==========
    __init__()                      -- initialise object of Backupset with the specified backupset
    name and id, and associated to the specified instance

    __getattr__()                   -- provides access to restore helper methods

    __repr__()                      -- return the backupset name, the instance is associated with

    _get_backupset_id()             -- method to get the backupset id, if not specified in __init__

    _get_backupset_properties()     -- get the properties of this backupset

    _run_backup()                   -- runs full backup for the specified subclient,
    and appends the job object to the return list

    _update()                       -- updates the properties of the backupset

    _get_epoch_time()               -- gets the Epoch time given the input time is in format

                                            %Y-%m-%d %H:%M:%S

    _set_defaults()                 -- recursively sets default values on a dictionary

    _prepare_browse_options()       -- prepares the options for the Browse/find operation

    _prepare_browse_json()          -- prepares the JSON object for the browse request

    _process_browse_response()      -- retrieves the items from browse response

    _process_update_request()       --  to process the request using API call

    _do_browse()                    -- performs a browse operation with the given options

    update_properties()             -- updates the backupset properties

    set_default_backupset()         -- sets the backupset as the default backup set for the agent,
    if not already default

    backup()                        -- runs full backup for all subclients
    associated with this backupset

    browse()                        -- browse the content of the backupset

    find()                          -- find content in the backupset

    list_media()                    -- List media required to browse and restore backed up data from the backupset

    refresh()                       -- refresh the properties of the backupset

    delete_data()                   -- deletes items from the backupset and makes then unavailable
    to browse and restore

    backed_up_files_count()         -- Returns the count of the total number of files present in the backed up data
                                       of all the subclients of the given backupset.

Backupset instance Attributes
-----------------------------

    **properties**                  -- returns the properties of backupset

    **name**                        -- returns the name of the backupset

    **guid**                        -- treats the backupset GUID as a property
    of the Backupset class

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy
import threading
import time
from base64 import b64encode
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from .exception import SDKException
from .schedules import Schedules
from .subclient import Subclients

if TYPE_CHECKING:
    from .client import Client
    from .plan import Plan

class Backupsets(object):
    """
    Manages and interacts with backupsets associated with a client.

    The Backupsets class provides a comprehensive interface for handling backupsets,
    including retrieval, addition, deletion, and management of various backupset types.
    It supports operations for different backupset categories such as archivesets,
    SharePoint clients, and Salesforce backupsets. The class also offers utility methods
    for refreshing backupset data, checking for the existence of specific backupsets,
    and accessing default and all backupsets via properties.

    Key Features:
        - Retrieve all backupsets associated with a client
        - Add new backupsets, archivesets, SharePoint, and Salesforce backupsets
        - Delete existing backupsets
        - Check for the existence of a backupset by name
        - Access all backupsets and the default backupset via properties
        - Refresh backupset information
        - Support for indexing, length, and string representation
        - Internal processing of backupset addition responses

    #ai-gen-doc
    """

    def __init__(self, class_object: object) -> None:
        """Initialize an instance of the Backupsets class.

        Args:
            class_object: An instance of the Agent or Instance class required to initialize Backupsets.

        Raises:
            SDKException: If class_object is not an instance of the Agent or Instance class.

        Example:
            >>> agent = Agent(commcell_object, "File System")
            >>> backupsets = Backupsets(agent)
            >>> print(type(backupsets))
            <class 'Backupsets'>
        #ai-gen-doc
        """
        from .agent import Agent
        from .instance import Instance

        self._instance_object = None

        if isinstance(class_object, Agent):
            self._agent_object = class_object
        elif isinstance(class_object, Instance):
            self._instance_object = class_object
            self._agent_object = class_object._agent_object
        else:
            raise SDKException('Backupset', '103')

        self._client_object = self._agent_object._client_object

        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._BACKUPSETS = self._services['GET_ALL_BACKUPSETS'] % (self._client_object.client_id)
        if self._agent_object:
            self._BACKUPSETS += '&applicationId=' + self._agent_object.agent_id

        if self._instance_object:
            self._BACKUPSETS += '&instanceId=' + str(self._instance_object.instance_id)

        if self._agent_object.agent_name in ['cloud apps', 'sql server', 'sap hana']:
            self._BACKUPSETS += '&excludeHidden=0'

        self._backupsets = None
        self._default_backup_set = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all backupsets for the agent of a client.

        This method provides a human-readable summary listing all backupsets associated 
        with the agent of a client.

        Returns:
            A string containing the names or details of all backupsets for the agent.

        Example:
            >>> backupsets = Backupsets(commcell_object, agent_name, client_name)
            >>> print(str(backupsets))
            >>> # Output: "Backupset1, Backupset2, Backupset3"

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Backupset', 'Instance', 'Agent', 'Client'
        )

        for index, backupset in enumerate(self._backupsets):
            sub_str = '{:^5}\t{:20}\t{:20}\t{:20}\t{:20}\n'.format(
                index + 1,
                backupset.split('\\')[-1],
                self._backupsets[backupset]['instance'],
                self._agent_object.agent_name,
                self._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the Backupsets instance.

        This method provides a developer-friendly string that represents the Backupsets object,
        typically used for debugging and logging purposes.

        Returns:
            A string representation of the Backupsets instance.

        Example:
            >>> backupsets = Backupsets(commcell_object)
            >>> print(repr(backupsets))
            <Backupsets object at 0x7f8c2b1e2d30>
        #ai-gen-doc
        """
        return "Backupsets class instance for Agent: '{0}'".format(self._agent_object.agent_name)

    def __len__(self) -> int:
        """Get the number of backupsets associated with the selected Agent.

        Returns:
            The total count of backupsets as an integer.

        Example:
            >>> backupsets = Backupsets(agent_object)
            >>> count = len(backupsets)
            >>> print(f"Number of backupsets: {count}")

        #ai-gen-doc
        """
        return len(self.all_backupsets)

    def __getitem__(self, value: 'Union[str, int]') -> 'Union[str, dict]':
        """Retrieve backupset information by name or ID.

        If a backupset ID (int) is provided, returns the name of the corresponding backupset.
        If a backupset name (str) is provided, returns a dictionary containing the details of the backupset.

        Args:
            value: The name (str) or ID (int) of the backupset to retrieve.

        Returns:
            str: The name of the backupset if an ID was provided.
            dict: The details of the backupset if a name was provided.

        Raises:
            IndexError: If no backupset exists with the given name or ID.

        Example:
            >>> backupsets = Backupsets()
            >>> # Retrieve backupset details by name
            >>> details = backupsets['DailyBackup']
            >>> print(details)
            {'backupsetId': 123, 'name': 'DailyBackup', ...}

            >>> # Retrieve backupset name by ID
            >>> name = backupsets[123]
            >>> print(name)
            'DailyBackup'

        #ai-gen-doc
        """
        value = str(value)

        if value in self.all_backupsets:
            return self.all_backupsets[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_backupsets.items())
                )[0][0]
            except IndexError:
                raise IndexError('No backupset exists with the given Name / Id')

    def _get_backupsets(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve all backupsets associated with the specified agent.

        Returns:
            Dictionary mapping backupset names to their details. Each entry contains:
                - 'id': The unique identifier of the backupset.
                - 'instance': The instance associated with the backupset.

            Example structure:
                {
                    "backupset1_name": {
                        "id": backupset1_id,
                        "instance": instance
                    },
                    "backupset2_name": {
                        "id": backupset2_id,
                        "instance": instance
                    }
                }

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> backupsets = Backupsets(agent_object)
            >>> all_backupsets = backupsets._get_backupsets()
            >>> for name, details in all_backupsets.items():
            ...     print(f"Backupset: {name}, ID: {details['id']}, Instance: {details['instance']}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._BACKUPSETS)

        if flag:
            if response.json() and 'backupsetProperties' in response.json():
                return_dict = {}

                for dictionary in response.json()['backupsetProperties']:
                    agent = dictionary['backupSetEntity']['appName'].lower()
                    instance = dictionary['backupSetEntity']['instanceName'].lower()

                    if self._instance_object is not None:
                        if (self._instance_object.instance_name in instance and
                                self._agent_object.agent_name in agent):
                            temp_name = dictionary['backupSetEntity']['backupsetName'].lower()
                            temp_id = str(dictionary['backupSetEntity']['backupsetId']).lower()
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "instance": instance
                            }

                            if dictionary['commonBackupSet'].get('isDefaultBackupSet'):
                                self._default_backup_set = temp_name

                    elif self._agent_object.agent_name in agent:
                        temp_name = dictionary['backupSetEntity']['backupsetName'].lower()
                        temp_id = str(dictionary['backupSetEntity']['backupsetId']).lower()

                        if len(self._agent_object.instances.all_instances) > 1:
                            return_dict["{0}\\{1}".format(instance, temp_name)] = {
                                "id": temp_id,
                                "instance": instance
                            }

                            if dictionary['commonBackupSet'].get('isDefaultBackupSet'):
                                self._default_backup_set = "{0}\\{1}".format(instance, temp_name)
                        else:
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "instance": instance
                            }

                            if dictionary['commonBackupSet'].get('isDefaultBackupSet'):
                                self._default_backup_set = temp_name

                return return_dict
            else:
                return {}
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_backupsets(self) -> Dict[str, Dict[str, Any]]:
        """Get a dictionary of all backupsets for the Agent or Instance of the selected Client.

        The returned dictionary maps backupset names to their details, including the backupset ID and instance information.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary where each key is a backupset name, and the value is a dictionary with keys:
                - 'id': The unique identifier of the backupset.
                - 'instance': The instance associated with the backupset.

        Example:
            >>> backupsets = Backupsets(client_object)
            >>> all_sets = backupsets.all_backupsets  # Use dot notation for property access
            >>> for name, details in all_sets.items():
            ...     print(f"Backupset: {name}, ID: {details['id']}, Instance: {details['instance']}")

        #ai-gen-doc
        """
        return self._backupsets

    def has_backupset(self, backupset_name: str) -> bool:
        """Check if a backupset with the specified name exists for the agent.

        Args:
            backupset_name: The name of the backupset to check for existence.

        Returns:
            True if the backupset exists for the agent, False otherwise.

        Raises:
            SDKException: If the type of the backupset_name argument is not a string.

        Example:
            >>> backupsets = Backupsets(agent_object)
            >>> exists = backupsets.has_backupset("DailyBackup")
            >>> print(f"Backupset exists: {exists}")
            # Output: Backupset exists: True

        #ai-gen-doc
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '101')

        return self._backupsets and backupset_name.lower() in self._backupsets

    def _process_add_response(self, backupset_name: str, request_json: dict) -> tuple:
        """Execute the Backupset Add API with the provided request JSON and parse the response.

        This method sends a request to add a backupset using the specified name and request JSON,
        then processes the API response to determine success or failure, along with any error codes
        and messages.

        Args:
            backupset_name: The name of the backupset to be added.
            request_json: The JSON payload to be sent in the API request.

        Returns:
            A tuple containing:
                bool: True if the operation was successful, False otherwise.
                str: The error code returned by the API, if any.
                str: The error message returned by the API, if any.

        Raises:
            SDKException: If the API response is empty or indicates a failure.

        Example:
            >>> backupsets = Backupsets()
            >>> result = backupsets._process_add_response("MyBackupset", {"backupsetProperties": {...}})
            >>> success, error_code, error_message = result
            >>> if success:
            ...     print("Backupset added successfully.")
            ... else:
            ...     print(f"Failed to add backupset: {error_code} - {error_message}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._services['ADD_BACKUPSET'], request_json)

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response'][0]['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response'][0]['errorString']
                        o_str = 'Failed to create backupset\nError: "{0}"'.format(error_string)
                        raise SDKException('Backupset', '102', o_str)
                    else:
                        # initialize the backupsets again
                        # so the backupset object has all the backupsets
                        self.refresh()
                        return self.get(backupset_name)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create backuspet\nError: "{0}"'.format(error_string)
                    raise SDKException('Backupset', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add(self, backupset_name: str, on_demand_backupset: bool = False, **kwargs: dict) -> 'Backupset':
        """Add a new backup set to the agent.

        Args:
            backupset_name: The name of the new backup set to add.
            on_demand_backupset: If True, creates an on-demand backup set; otherwise, creates a standard backup set. Defaults to False.
            **kwargs: Optional keyword arguments to further configure the backup set:
                - storage_policy (str): Name of the storage policy to associate with the backup set.
                - plan_name (str): Name of the plan to associate with the backup set.
                - is_nas_turbo_backupset (bool): Set to True for NAS-based clients.

        Returns:
            Backupset: An instance of the Backupset class representing the newly created backup set.

        Raises:
            SDKException: If the backup set name is not a string, if creation fails, if the response is empty or unsuccessful, or if a backup set with the same name already exists.

        Example:
            >>> backupsets = Backupsets(agent_object)
            >>> new_backupset = backupsets.add(
            ...     backupset_name="WeeklyBackup",
            ...     storage_policy="DefaultPolicy",
            ...     plan_name="GoldPlan"
            ... )
            >>> print(f"Created backup set: {new_backupset}")

        #ai-gen-doc
        """
        if not (isinstance(backupset_name, str) and isinstance(on_demand_backupset, bool)):
            raise SDKException('Backupset', '101')

        if self.has_backupset(backupset_name):
            raise SDKException(
                'Backupset', '102', 'Backupset "{0}" already exists.'.format(backupset_name)
            )

        if self._instance_object is None:
            if self._agent_object.instances.has_instance('DefaultInstanceName'):
                self._instance_object = self._agent_object.instances.get('DefaultInstanceName')
            else:
                self._instance_object = self._agent_object.instances.get(
                    sorted(self._agent_object.instances.all_instances)[0]
                )

        request_json = {
            "association": {
                "entity": [{
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": backupset_name
                }]
            },
            "backupSetInfo": {
                "commonBackupSet": {
                    "onDemandBackupset": on_demand_backupset
                }
            }
        }

        if kwargs.get('is_nas_turbo_type'):
            request_json["backupSetInfo"]["commonBackupSet"]["isNasTurboBackupSet"] = kwargs.get('is_nas_turbo_type',
                                                                                                 False)

        agent_settings = {
            'db2': """
request_json['backupSetInfo'].update({
    'db2BackupSet': {
        'dB2DefaultIndexSP': {
            'storagePolicyName': kwargs.get('storage_policy', '')
        }
    }
})
            """
        }

        exec(agent_settings.get(self._agent_object.agent_name, ''))

        if kwargs.get('plan_name'):
            plan_entity_dict = {
                "planName": kwargs.get('plan_name')
            }
            request_json['backupSetInfo']['planEntity'] = plan_entity_dict

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ADD_BACKUPSET'], request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    response_value = response.json()['response'][0]
                    error_code = str(response_value['errorCode'])
                    error_message = None

                    if 'errorString' in response_value:
                        error_message = response_value['errorString']

                    if error_message:
                        o_str = 'Failed to create new backupset\nError: "{0}"'.format(
                            error_message
                        )
                        raise SDKException('Backupset', '102', o_str)
                    else:
                        if error_code == '0':
                            # initialize the backupsets again
                            # so the backupsets object has all the backupsets
                            self.refresh()

                            return self.get(backupset_name)

                        else:
                            o_str = ('Failed to create new backupset with error code: "{0}"\n'
                                     'Please check the documentation for '
                                     'more details on the error').format(error_code)

                            raise SDKException('Backupset', '102', o_str)
                else:
                    error_code = response.json()['errorCode']
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to create new backupset\nError: "{0}"'.format(
                        error_message
                    )
                    raise SDKException('Backupset', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_archiveset(self, archiveset_name: str, is_nas_turbo_backupset: bool = False) -> 'Backupset':
        """Add a new archiveset to the agent.

        An archiveset is a specialized backupset primarily used for archiving-only items. 
        This method creates a new archiveset with the specified name. For NAS-based clients, 
        set `is_nas_turbo_backupset` to True.

        Args:
            archiveset_name: The name of the new archiveset to add.
            is_nas_turbo_backupset: Set to True if the archiveset is for a NAS-based client. Defaults to False.

        Returns:
            Backupset: An instance of the Backupset class representing the newly created archiveset.

        Raises:
            SDKException: If the archiveset name is not a string, if creation fails, 
                if the response is empty or unsuccessful, or if an archiveset with the same name already exists.

        Example:
            >>> backupsets = Backupsets(agent_object)
            >>> new_archiveset = backupsets.add_archiveset("ArchiveSet2024")
            >>> print(f"Created archiveset: {new_archiveset}")
            >>> # For NAS-based client
            >>> nas_archiveset = backupsets.add_archiveset("NAS_Archive", is_nas_turbo_backupset=True)

        #ai-gen-doc
        """
        if not (isinstance(archiveset_name, str)):
            raise SDKException('Backupset', '101')
        else:
            archiveset_name = archiveset_name.lower()

        if self.has_backupset(archiveset_name):
            raise SDKException('archiveset_name', '102', 'Archiveset "{0}" already exists.'.format(archiveset_name))

        if self._agent_object.agent_id not in ['29', '33']:
            raise SDKException('Backupset', '101', "Archiveset is not applicable to this application type.")



        request_json = {
            "backupSetInfo": {
                "useContentFromPlan": False,
                "planEntity": {},
                "commonBackupSet": {
                    "isNasTurboBackupSet": is_nas_turbo_backupset,
                    "isArchivingEnabled": True,
                    "isDefaultBackupSet": False
                },
                "backupSetEntity": {
                    "_type_": 6,
                    "clientId": int(self._client_object.client_id),
                    "backupsetName": archiveset_name,
                    "applicationId": int(self._agent_object.agent_id)
                },
                "subClientList": [
                    {
                        "contentOperationType": 1,
                        "fsSubClientProp": {
                            "useGlobalFilters": 2,
                            "forcedArchiving": True,
                            "diskCleanupRules": {
                                "enableArchivingWithRules": True,
                                "diskCleanupFileTypes": {}
                            }
                        },
                        "content": [
                            {
                                "path": ""
                            }
                        ]
                    }
                ]
            }
        }
        
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['ADD_BACKUPSET'], request_json
        )

        if flag:
            if response.json():
                if 'response' in response.json():
                    response_value = response.json()['response'][0]
                    error_code = str(response_value['errorCode'])
                    error_message = None

                    if 'errorString' in response_value:
                        error_message = response_value['errorString']

                    if error_message:
                        o_str = 'Failed to create new Archiveset\nError: "{0}"'.format(
                            error_message
                        )
                        raise SDKException('Archiveset', '102', o_str)
                    else:
                        if error_code == '0':
                            # initialize the backupsets again
                            # so the backupsets object has all the backupsets
                            self.refresh()
                            return self.get(archiveset_name)
                        
                        else:
                            o_str = ('Failed to create new Archiveset with error code: "{0}"\n'
                                     'Please check the documentation for '
                                     'more details on the error').format(error_code)

                            raise SDKException('Backupset', '102', o_str)
                else:
                    error_code = response.json()['errorCode']
                    error_message = response.json()['errorMessage']
                    o_str = 'Failed to create new Archiveset\nError: "{0}"'.format(
                        error_message
                    )
                    raise SDKException('Backupset', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_v1_sharepoint_client(
            self,
            backupset_name: str,
            server_plan: str,
            client_name: str,
            **kwargs: str
        ) -> None:
        """Add a new Office 365 V1 SharePoint Pseudo Client to the Commcell.

        This method creates a SharePoint V1 pseudo client, which is represented as a backupset,
        and associates it with the specified server plan and access node. Additional configuration
        parameters for Azure and SharePoint Online can be provided as keyword arguments.

        Args:
            backupset_name: Name of the new SharePoint Pseudo Client (backupset).
            server_plan: Name of the server plan to associate with the client.
            client_name: Name of the access node for which the pseudo client will be created.

        Keyword Args:
            tenant_url: URL of the SharePoint tenant.
            azure_username: Username of the Azure app.
            azure_secret: Secret key of the Azure app.
            user_username: Username of the SharePoint admin.
            user_password: Password of the SharePoint admin.
            azure_app_id: Azure app ID for SharePoint Online.
            azure_app_key_id: App key for SharePoint Online.
            azure_directory_id: Azure directory ID for SharePoint Online.

        Returns:
            Client: An instance of the Client class representing the newly created SharePoint pseudo client.

        Raises:
            SDKException: If a client with the given name already exists,
                if the index server or server plan is not found,
                if the client creation fails,
                or if the response is empty or unsuccessful.

        Example:
            >>> backupsets = Backupsets(commcell_object)
            >>> client = backupsets.add_v1_sharepoint_client(
            ...     backupset_name="SharePointBackupset",
            ...     server_plan="SharePointPlan",
            ...     client_name="AccessNode01",
            ...     tenant_url="https://tenant.sharepoint.com",
            ...     azure_username="azureuser@domain.com",
            ...     azure_secret="secretkey",
            ...     user_username="spadmin@domain.com",
            ...     user_password="adminpassword",
            ...     azure_app_id="app-id-123",
            ...     azure_app_key_id="app-key-456",
            ...     azure_directory_id="directory-id-789"
            ... )
            >>> print(f"Created SharePoint client: {client}")

        #ai-gen-doc
        """
        if self.has_backupset(backupset_name):
            raise SDKException(
                'Backupset', '102', 'Backupset "{0}" already exists.'.format(backupset_name))
        if self._commcell_object.plans.has_plan(server_plan):
            server_plan_object = self._commcell_object.plans.get(server_plan)
            server_plan_dict = {
                "planId": int(server_plan_object.plan_id)
            }
        else:
            raise SDKException('Backupset', '102')
        backup_set = {
            "_type_": 6,
            "applicationId": 78,
            "backupsetName": backupset_name,
            "clientId": int(self._client_object.client_id)
        }
        request_json = {
            "backupSetInfo": {
                "planEntity": server_plan_dict,
                "backupSetEntity": backup_set,
                "sharepointBackupSet": {
                    "sharepointBackupSetType": 4
                }
            }
        }
        tenant_url = kwargs.get('tenant_url')
        user_username = kwargs.get('user_username')
        is_modern_auth_enabled = kwargs.get('is_modern_auth_enabled',False)
        azure_secret = b64encode(kwargs.get('azure_secret').encode()).decode()
        azure_app_key_id = b64encode(kwargs.get('azure_app_key_id').encode()).decode()
        user_password = b64encode(kwargs.get('user_password').encode()).decode()
        request_json["backupSetInfo"]["sharepointBackupSet"][
            "spOffice365BackupSetProp"] = {
            "azureUserAccount": kwargs.get('azure_username'),
            "azureAccountKey": azure_secret,
            "tenantUrlItem": tenant_url,
            "isModernAuthEnabled": is_modern_auth_enabled,
            "office365Credentials": {
                "userName": user_username,
                "password": user_password
            },
        }
        if is_modern_auth_enabled:
            request_json["backupSetInfo"]["sharepointBackupSet"][
                "spOffice365BackupSetProp"]["azureAppList"] = {
                "azureApps": [
                    {
                        "azureAppId": kwargs.get('azure_app_id'),
                        "azureAppKeyValue": azure_app_key_id,
                        "azureDirectoryId": kwargs.get('azure_directory_id')
                    }
                ]
            }

        self._process_add_response(backupset_name, request_json)

    def add_salesforce_backupset(
            self,
            salesforce_options: dict,
            db_options: dict = None,
            **kwargs: dict
        ) -> None:
        """Add a new Salesforce Backupset to the Commcell.

        This method creates a new Salesforce backupset using the provided Salesforce credentials and optional database configuration.
        Additional keyword arguments can be supplied to further customize the backupset creation.

        Args:
            salesforce_options: Dictionary containing Salesforce credentials and options. Example:
                {
                    "salesforce_user_name": "salesforce_user",
                    "salesforce_user_password": "password",
                    "salesforce_user_token": "user_token"
                }
            db_options: Optional dictionary for configuring the sync database. Example:
                {
                    "db_enabled": True,
                    "db_type": "SQLSERVER",
                    "db_host_name": "db.example.com",
                    "db_instance": "instance1",
                    "db_name": "salesforce_db",
                    "db_port": 1433,
                    "db_user_name": "db_user",
                    "db_user_password": "db_password"
                }
            **kwargs: Additional keyword arguments for backupset configuration, such as:
                - download_cache_path (str): Path for download cache.
                - mutual_auth_path (str): Path to mutual authentication certificate.
                - storage_policy (str): Name of the storage policy.
                - streams (int): Number of data streams.

        Returns:
            Backupset: An instance of the Backupset class representing the newly created Salesforce backupset.

        Raises:
            SDKException: If a backupset with the given name already exists, if the backupset creation fails,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> salesforce_opts = {
            ...     "salesforce_user_name": "user@company.com",
            ...     "salesforce_user_password": "mypassword",
            ...     "salesforce_user_token": "mytoken"
            ... }
            >>> db_opts = {
            ...     "db_enabled": True,
            ...     "db_type": "SQLSERVER",
            ...     "db_host_name": "dbhost",
            ...     "db_instance": "instance1",
            ...     "db_name": "sf_db",
            ...     "db_port": 1433,
            ...     "db_user_name": "dbuser",
            ...     "db_user_password": "dbpass"
            ... }
            >>> backupset = backupsets.add_salesforce_backupset(
            ...     salesforce_options=salesforce_opts,
            ...     db_options=db_opts,
            ...     storage_policy="SalesforcePolicy",
            ...     streams=4
            ... )
            >>> print(f"Created backupset: {backupset}")

        #ai-gen-doc
        """

        if db_options is None:
            db_options = {'db_enabled': False}
        if self.has_backupset(salesforce_options.get('salesforce_user_name')):
            raise SDKException('Backupset', '102',
                               'Backupset "{0}" already exists.'.format(salesforce_options.get('salesforce_user_name')))

        salesforce_password = b64encode(salesforce_options.get('salesforce_user_password').encode()).decode()
        salesforce_token = b64encode(salesforce_options.get('salesforce_user_token', '').encode()).decode()
        db_user_password = ""
        if db_options.get('db_enabled', False):
            db_user_password = b64encode(db_options.get('db_user_password').encode()).decode()

        request_json = {
            "backupSetInfo": {
                "backupSetEntity": {
                    "clientName": self._client_object.client_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": salesforce_options.get('salesforce_user_name'),
                    "appName": self._agent_object.agent_name
                },
                "cloudAppsBackupset": {
                    "instanceType": 3,
                    "salesforceBackupSet": {
                        "enableREST": True,
                        "downloadCachePath": kwargs.get('download_cache_path', '/tmp'),
                        "mutualAuthPath": kwargs.get('mutual_auth_path', ''),
                        "token": salesforce_token,
                        "userPassword": {
                            "userName": salesforce_options.get('salesforce_user_name'),
                            "password": salesforce_password,
                        },
                        "syncDatabase": {
                            "dbEnabled": db_options.get('db_enabled', False),
                            "dbPort": db_options.get('db_port', '1433'),
                            "dbInstance": db_options.get('db_instance', ''),
                            "dbName": db_options.get('db_name', self._instance_object.instance_name),
                            "dbType": db_options.get('db_type', "SQLSERVER"),
                            "dbHost": db_options.get('db_host_name', ''),
                            "dbUserPassword": {
                                "userName": db_options.get('db_user_name', ''),
                                "password": db_user_password,

                            },
                        },
                    },
                    "generalCloudProperties": {
                        "numberOfBackupStreams": kwargs.get('streams', 2),
                        "storageDevice": {
                            "dataBackupStoragePolicy": {
                                "storagePolicyName": kwargs.get('storage_policy', '')
                            },
                        },
                    },
                },
            },
        }

        self._process_add_response(salesforce_options.get('salesforce_user_name'), request_json)

    def get(self, backupset_name: str) -> 'Backupset':
        """Retrieve a Backupset object by its name.

        Args:
            backupset_name: The name of the backupset to retrieve.

        Returns:
            Backupset: An instance of the Backupset class corresponding to the specified name.

        Raises:
            SDKException: If the backupset_name is not a string, or if no backupset exists with the given name.

        Example:
            >>> backupsets = Backupsets(commcell_object, client_name, agent_name)
            >>> backupset = backupsets.get('DailyBackupSet')
            >>> print(f"Retrieved backupset: {backupset}")
            >>> # The returned Backupset object can be used for further backup operations

        #ai-gen-doc
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = backupset_name.lower()

            if self.has_backupset(backupset_name):
                if self._instance_object is None:
                    self._instance_object = self._agent_object.instances.get(
                        self._backupsets[backupset_name]['instance']
                    )
                return Backupset(
                    self._instance_object,
                    backupset_name,
                    self._backupsets[backupset_name]["id"]
                )

            raise SDKException(
                'Backupset', '102', 'No backupset exists with name: "{0}"'.format(backupset_name)
            )

    def delete(self, backupset_name: str) -> None:
        """Delete a backup set from the agent by its name.

        Args:
            backupset_name: The name of the backup set to be deleted.

        Raises:
            SDKException: If the backup set name is not a string, if the deletion fails,
                if the response is empty or not successful, or if no backup set exists with the given name.

        Example:
            >>> backupsets = Backupsets(agent_object)
            >>> backupsets.delete("DailyBackupSet")
            >>> print("Backup set deleted successfully.")

        #ai-gen-doc
        """
        if not isinstance(backupset_name, str):
            raise SDKException('Backupset', '101')
        else:
            backupset_name = backupset_name.lower()

        if self.has_backupset(backupset_name):
            delete_backupset_service = self._services['BACKUPSET'] % (
                self._backupsets[backupset_name]['id']
            )

            flag, response = self._cvpysdk_object.make_request('DELETE', delete_backupset_service)

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = response_value['errorString']

                        if error_message:
                            o_str = 'Failed to delete backupset\nError: "{0}"'
                            raise SDKException('Backupset', '102', o_str.format(error_message))
                        else:
                            if error_code == '0':
                                # initialize the backupsets again
                                # so the backupsets object has all the backupsets
                                self.refresh()
                            else:
                                o_str = ('Failed to delete backupset with error code: "{0}"\n'
                                         'Please check the documentation for '
                                         'more details on the error').format(error_code)
                                raise SDKException('Backupset', '102', o_str)
                    else:
                        error_code = response.json()['errorCode']
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to delete backupset\nError: "{0}"'.format(error_message)
                        raise SDKException('Backupset', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        else:
            raise SDKException(
                'Backupset', '102', 'No backupset exists with name: "{0}"'.format(backupset_name)
            )

    def refresh(self) -> None:
        """Reload the backupsets associated with the Agent or Instance.

        This method refreshes the internal cache of backupsets, ensuring that any changes 
        made on the Commcell are reflected in the current object. Use this method to 
        update the backupset information after adding, removing, or modifying backupsets.

        Example:
            >>> backupsets = Backupsets(agent_object)
            >>> backupsets.refresh()  # Refreshes the list of backupsets
            >>> print("Backupsets refreshed successfully")

        #ai-gen-doc
        """
        self._backupsets = self._get_backupsets()

    @property
    def default_backup_set(self) -> str:
        """Get the name of the default backup set for the selected Client and Agent.

        Returns:
            The name of the default backup set as a string.

        Example:
            >>> backupsets = Backupsets(client_object)
            >>> default_set = backupsets.default_backup_set  # Use dot notation for property access
            >>> print(f"Default backup set: {default_set}")

        #ai-gen-doc
        """
        return self._default_backup_set


class Backupset(object):
    """
    Class for managing and performing operations on a specific backupset.

    The Backupset class provides a comprehensive interface for handling backupset-related
    operations within a backup management system. It allows users to interact with backupsets,
    retrieve and update their properties, perform backup and browse operations, manage backupset
    configurations, and handle data deletion and media listing.

    Key Features:
        - Creation and initialization of backupset objects
        - Dynamic attribute access and representation
        - Retrieval of backupset ID and properties
        - Execution of backup operations for specified subclients
        - Processing and updating backupset properties and responses
        - Time conversion utilities for backupset operations
        - Setting default values and updating backupset configurations
        - Preparation and processing of browse options and responses
        - Browsing all versions and specific data within the backupset
        - Updating backupset properties via dictionary input
        - Access to backupset metadata via properties (name, ID, description, plan, GUID, etc.)
        - Setting backupset as default and managing on-demand backupsets
        - Performing backup, browse, find, and data deletion operations
        - Listing associated media and refreshing backupset state
        - Counting backed up files for specified paths

    This class is intended for use in environments where backupset management and data protection
    are critical, providing a robust set of methods for interacting with backupset entities.

    #ai-gen-doc
    """

    def __new__(cls, instance_object: object, backupset_name: str, backupset_id: str = None) -> 'Backupset':
        """Create and return a new Backupset instance.

        This method is responsible for creating a new instance of the Backupset class,
        associating it with the specified instance object, backupset name, and optional backupset ID.

        Args:
            instance_object: The instance object to which the backupset belongs.
            backupset_name: The name of the backupset to be created.
            backupset_id: Optional; the unique identifier for the backupset.

        Returns:
            Backupset: A new instance of the Backupset class.

        Example:
            >>> backupset = Backupset(instance_object, "DailyBackup", "12345")
            >>> print(f"Created backupset: {backupset}")

        #ai-gen-doc
        """
        from .backupsets.fsbackupset import FSBackupset
        from .backupsets.nasbackupset import NASBackupset
        from .backupsets.hanabackupset import HANABackupset
        from .backupsets.cabackupset import CloudAppsBackupset
        from .backupsets.postgresbackupset import PostgresBackupset
        from .backupsets.adbackupset import ADBackupset
        from .backupsets.db2backupset import DB2Backupset
        from .backupsets.vsbackupset import VSBackupset
        from .backupsets.aadbackupset import AzureAdBackupset
        from .backupsets.sharepointbackupset import SharepointBackupset

        _backupsets_dict = {
            'file system': FSBackupset,
            'nas': NASBackupset,        # SP11 or lower CS honors NAS as the Agent Name
            'ndmp': NASBackupset,       # SP12 and above honors NDMP as the Agent Name
            'sap hana': HANABackupset,
            'cloud apps': CloudAppsBackupset,
            'postgresql': PostgresBackupset,
            "active directory": ADBackupset,
            'db2': DB2Backupset,
            'virtual server': VSBackupset,
            "azure ad": AzureAdBackupset,
            'sharepoint server': SharepointBackupset
        }

        if instance_object._agent_object.agent_name in _backupsets_dict.keys():
            _class = _backupsets_dict.get(instance_object._agent_object.agent_name, cls)
            if _class.__new__ == cls.__new__:
                return object.__new__(_class)
            return _class.__new__(_class, instance_object, backupset_name, backupset_id)
        else:
            return object.__new__(cls)

    def __init__(self, instance_object: object, backupset_name: str, backupset_id: str = None) -> None:
        """Initialize a Backupset object.

        Args:
            instance_object: An instance of the Instance class to which this backupset belongs.
            backupset_name: The name of the backupset.
            backupset_id: The unique identifier for the backupset. If not provided, it will be determined automatically.

        Example:
            >>> instance = Instance(commcell_object, "FileSystem")
            >>> backupset = Backupset(instance, "defaultBackupSet")
            >>> print(f"Backupset created: {backupset}")

        #ai-gen-doc
        """
        self._instance_object = instance_object
        self._agent_object = self._instance_object._agent_object
        self._client_object = self._agent_object._client_object

        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        # self._restore_methods = ['_process_restore_response', '_filter_paths', '_restore_json']
        self._restore_methods = [
            '_process_restore_response',
            '_filter_paths',
            '_process_search_response',
            '_restore_json',
            '_impersonation_json',
            '_restore_browse_option_json',
            '_restore_common_options_json',
            '_restore_destination_json',
            '_restore_fileoption_json',
            '_json_restore_subtask'
        ]

        self._restore_options_json = [
            '_impersonation_json_',
            '_browse_restore_json',
            '_destination_restore_json',
            '_commonoption_restore_json',
            '_fileoption_restore_json',
        ]

        self._backupset_name = backupset_name.split('\\')[-1].lower()
        self._description = None

        if backupset_id:
            # Use the backupset id provided in the arguments
            self._backupset_id = str(backupset_id)
        else:
            # Get the id associated with this backupset
            self._backupset_id = self._get_backupset_id()

        self._BACKUPSET = self._services['BACKUPSET'] % (self.backupset_id)
        self._BROWSE = self._services['BROWSE']
        self._RESTORE = self._services['RESTORE']

        self._is_default = False
        self._is_on_demand_backupset = False
        self._properties = None
        self._backupset_association = {}
        self._plan_name = None
        self._plan_obj = None

        self.subclients = None
        self.schedules = None
        self._hidden_subclient = None
        self.refresh()

        self._default_browse_options = {
            'operation': 'browse',
            'show_deleted': False,
            'from_time': 0,  # value should either be the Epoch time or the Timestamp
            'to_time': 0,  # value should either be the Epoch time or the Timestamp
            'path': '\\',
            'copy_precedence': 0,
            'media_agent': '',
            'page_size': 100000,
            'skip_node': 0,
            'restore_index': True,
            'vm_disk_browse': False,
            'filters': [],
            'job_id': 0,
            'include_aged_data': False,
            'include_meta_data':False,
            'include_hidden': False,
            'include_running_jobs': False,
            'compute_folder_size': False,
            'vs_volume_browse': False,
            'browse_view_name': 'VOLUMEVIEW',
            'compare_backups_req': 0,
            'comparison_job_id': 0,

            '_subclient_id': 0,
            '_raw_response': False,
            '_custom_queries': False
        }

    def __getattr__(self, attribute: str) -> object:
        """Retrieve the value of a persistent attribute for the Backupset instance.

        This method is called when an attribute lookup does not find the attribute in the usual places.
        It allows access to persistent attributes that may not be explicitly defined in the class.

        Args:
            attribute: The name of the attribute to retrieve.

        Returns:
            The value of the requested persistent attribute.

        Example:
            >>> backupset = Backupset()
            >>> value = backupset.some_persistent_attribute
            >>> print(f"Attribute value: {value}")

        #ai-gen-doc
        """
        if attribute in self._restore_methods:
            return getattr(self._instance_object, attribute)
        elif attribute in self._restore_options_json:
            return getattr(self._instance_object, attribute)

        return super(Backupset, self).__getattribute__(attribute)

    def __repr__(self) -> str:
        """Return a string representation of the Backupset instance.

        This method provides a developer-friendly string that identifies the Backupset object,
        which can be useful for debugging and logging purposes.

        Returns:
            A string representing the Backupset instance.

        Example:
            >>> backupset = Backupset()
            >>> print(repr(backupset))
            <Backupset object at 0x7f8c2e4b2d30>
        #ai-gen-doc
        """
        representation_string = ('Backupset class instance for Backupset: "{0}" '
                                 'for Instance: "{1}" of Agent: "{2}"')
        return representation_string.format(
            self.backupset_name,
            self._instance_object.instance_name,
            self._agent_object.agent_name
        )

    def _get_backupset_id(self) -> str:
        """Retrieve the unique identifier (ID) associated with this backupset.

        Returns:
            The backupset ID as a string.

        Example:
            >>> backupset = Backupset()
            >>> backupset_id = backupset._get_backupset_id()
            >>> print(f"Backupset ID: {backupset_id}")

        #ai-gen-doc
        """
        backupsets = Backupsets(self._instance_object)
        return backupsets.get(self.backupset_name).backupset_id

    def _get_backupset_properties(self) -> None:
        """Retrieve and update the properties of this backupset from the Commcell.

        This method fetches the latest properties for the backupset and updates the internal state accordingly.

        Raises:
            SDKException: If the response from the Commcell is empty or indicates a failure.

        Example:
            >>> backupset = Backupset(commcell_object, client_name, instance_name, backupset_name)
            >>> backupset._get_backupset_properties()
            >>> # The backupset object now has updated properties

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._BACKUPSET)

        if flag:
            if response.json() and "backupsetProperties" in response.json():
                self._properties = response.json()["backupsetProperties"][0]

                backupset_name = self._properties["backupSetEntity"]["backupsetName"]
                self._backupset_name = backupset_name.lower()

                self._backupset_association = self._properties['backupSetEntity']

                self._is_default = bool(self._properties["commonBackupSet"]["isDefaultBackupSet"])

                if 'commonBackupSet' in self._properties:
                    if 'onDemandBackupset' in self._properties['commonBackupSet']:
                        self._is_on_demand_backupset = bool(
                            self._properties['commonBackupSet']['onDemandBackupset']
                        )

                if "userDescription" in self._properties["commonBackupSet"]:
                    self._description = self._properties["commonBackupSet"]["userDescription"]

                if "planName" in self._properties["planEntity"]:
                    self._plan_name = self._properties["planEntity"]["planName"]
                else:
                    self._plan_name = None
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _run_backup(self, subclient_name: str, return_list: list, **kwargs: dict) -> None:
        """Trigger a backup job for the specified subclient and append its Job object to the provided list.

        This method initiates a backup job for the given subclient if backup activity is enabled and a storage policy is set.
        The resulting Job object (or an SDKException instance if an error occurs) is appended to the `return_list`.
        Additional keyword arguments are passed to the subclient's `backup()` method, allowing customization of the backup operation.

        Args:
            subclient_name: The name of the subclient for which to trigger the backup.
            return_list: The list to which the resulting Job object or SDKException will be appended.
            **kwargs: Additional arguments to pass to the subclient's `backup()` method, such as:
                - backup_level (str): The type of backup to run (e.g., 'Full', 'Incremental').
                - advanced_options (dict): Advanced backup options to include in the request.

        Example:
            >>> jobs = []
            >>> backupset._run_backup('default', jobs, backup_level='Full')
            >>> for job in jobs:
            ...     print(job)
            >>> # jobs will contain Job objects for successful backups or SDKException instances for failures

        #ai-gen-doc
        """
        try:
            subclient = self.subclients.get(subclient_name)
            if subclient.is_backup_enabled and subclient.storage_policy is not None:
                job = subclient.backup(**kwargs)
                return_list.append(job)
                time.sleep(2)  # Staggering the next backup job to be started
        except SDKException as excp:
            return_list.append(excp)

    def _process_update_reponse(self, request_json: dict) -> tuple[bool, str, str]:
        """Execute the Backupset update API using the provided request JSON and parse the response.

        This method sends the given JSON request to the Backupset update API, processes the response,
        and returns a tuple containing the success status, error code, and error message.

        Args:
            request_json: Dictionary containing the JSON request payload for the Backupset update API.

        Returns:
            A tuple containing:
                bool: True if the update was successful, False otherwise.
                str: Error code received from the API response.
                str: Error message received from the API response.

        Raises:
            SDKException: If the API response is empty or indicates a failure.

        Example:
            >>> backupset = Backupset()
            >>> request_payload = {"backupsetName": "DailyBackup", "description": "Updated backupset"}
            >>> success, error_code, error_message = backupset._process_update_reponse(request_payload)
            >>> if success:
            ...     print("Backupset updated successfully.")
            ... else:
            ...     print(f"Update failed: {error_code} - {error_message}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._BACKUPSET, request_json)

        self._get_backupset_properties()

        if flag:
            if response.json() and "response" in response.json():
                error_code = str(response.json()["response"][0]["errorCode"])

                if error_code == "0":
                    return True, "0", ""
                else:
                    error_string = ""

                    if "errorString" in response.json()["response"][0]:
                        error_string = response.json()["response"][0]["errorString"]

                    if error_string:
                        return False, error_code, error_string
                    else:
                        return False, error_code, ""
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _update(self, backupset_name: str, backupset_description: str, default_backupset: bool) -> tuple[bool, str, str]:
        """Update the properties of the backupset.

        Args:
            backupset_name: The new name to assign to the backupset.
            backupset_description: The description to set for the backupset.
            default_backupset: Whether to set this backupset as the default.

        Returns:
            A tuple containing:
                bool: True if the update was successful, False otherwise.
                str: Error code received in the response, if any.
                str: Error message received, if any.

        Raises:
            SDKException: If the response is empty or indicates failure.

        Example:
            >>> result = backupset._update("NewBackupsetName", "Updated description", True)
            >>> success, error_code, error_message = result
            >>> if success:
            ...     print("Backupset updated successfully.")
            ... else:
            ...     print(f"Update failed: {error_code} - {error_message}")

        #ai-gen-doc
        """

        request_json = {
            "association": {
                "entity": [{
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": self.backupset_name
                }]
            },
            "backupsetProperties": {
                "commonBackupSet": {
                    "newBackupSetName": backupset_name,
                    "isDefaultBackupSet": default_backupset
                }
            }
        }

        if backupset_description is not None:
            request_json["backupsetProperties"]["commonBackupSet"][
                "userDescription"] = backupset_description

        return self._process_update_reponse(request_json)

    @staticmethod
    def _get_epoch_time(timestamp: Union[int, str]) -> int:
        """Convert a timestamp to its corresponding epoch time.

        The input can be either an epoch time (int) or a string timestamp in the format '%Y-%m-%d %H:%M:%S'.
        If a string is provided, it will be parsed and converted to epoch time.

        Args:
            timestamp: The timestamp to convert. Can be an integer representing epoch time,
                or a string in the format '%Y-%m-%d %H:%M:%S'.

        Returns:
            The epoch time as an integer.

        Raises:
            SDKException: If the input timestamp is not in the correct format.

        Example:
            >>> epoch = Backupset._get_epoch_time(1688123456)
            >>> print(epoch)
            1688123456
            >>> epoch = Backupset._get_epoch_time('2023-06-30 12:30:56')
            >>> print(epoch)
            1688123456

        #ai-gen-doc
        """
        if str(timestamp) == '0':
            return 0

        try:
            # return the timestamp value in int type
            return int(timestamp)
        except ValueError:
            # if not convertible to int, then convert the timestamp input to Epoch time
            try:
                return int(time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")))
            except Exception:
                raise SDKException('Subclient', '106')

    def _set_defaults(self, final_dict: dict, defaults_dict: dict) -> None:
        """Recursively set default values in a dictionary.

        Iterates over the `defaults_dict` and adds any missing keys and their default values 
        to the `final_dict`. If a value in `defaults_dict` is itself a dictionary, this method 
        will recursively set defaults for nested dictionaries as well.

        Args:
            final_dict: The dictionary to update with default values. This dictionary will be 
                modified in place and is typically used to generate the Browse/Find JSON.
            defaults_dict: The dictionary containing default key-value pairs to apply.

        Example:
            >>> final = {'a': 1}
            >>> defaults = {'a': 0, 'b': 2, 'c': {'d': 4}}
            >>> backupset._set_defaults(final, defaults)
            >>> print(final)
            {'a': 1, 'b': 2, 'c': {'d': 4}}

        #ai-gen-doc
        """
        for key in defaults_dict:
            if key not in final_dict:
                final_dict[key] = defaults_dict[key]

            if isinstance(defaults_dict[key], dict):
                self._set_defaults(final_dict[key], defaults_dict[key])

    def _prepare_browse_options(self, options: dict) -> dict:
        """Prepare and set default values for browse or find operation options.

        This method takes a dictionary of browse options and ensures that all required
        default options are set for a browse or find operation within the backupset.

        Args:
            options: A dictionary containing user-specified browse options.

        Returns:
            A dictionary with all necessary browse options, including defaults where not provided.

        Example:
            >>> browse_options = {"path": "/data", "show_deleted": True}
            >>> prepared_options = backupset._prepare_browse_options(browse_options)
            >>> print(prepared_options)
            {'path': '/data', 'show_deleted': True, 'other_default_option': 'value'}

        #ai-gen-doc
        """
        self._set_defaults(options, self._default_browse_options)
        return options

    def _prepare_browse_json(self, options: dict) -> dict:
        """Prepare the JSON object required for a browse request.

        Args:
            options: A dictionary containing browse options and parameters.

        Returns:
            A dictionary representing the JSON object to be used in the browse response.

        Example:
            >>> browse_options = {
            ...     "path": "/data",
            ...     "show_deleted": True,
            ...     "time_range": {"from": "2023-01-01", "to": "2023-01-31"}
            ... }
            >>> browse_json = backupset._prepare_browse_json(browse_options)
            >>> print(browse_json)
            {'path': '/data', 'show_deleted': True, 'time_range': {'from': '2023-01-01', 'to': '2023-01-31'}}

        #ai-gen-doc
        """
        operation_types = {
            'browse': 0,
            'find': 1,
            'all_versions': 2,
            'list_media': 3,
            'delete_data': 7
        }

        options['operation'] = options['operation'].lower()

        if options['operation'] not in operation_types:
            options['operation'] = 'find'

        # add the browse mode value here, if it is different for an agent
        # if agent is not added in the dict, default value 2 will be used
        browse_mode = {
            'virtual server': 4,
            'cloud apps': 3,
            'azure ad': 3
        }

        mode = 2
        paths = []

        if isinstance(options['path'], str):
            paths.append(options['path'])
        elif isinstance(options['path'], list):
            paths = options['path']
        else:
            paths = ['\\']

        if self._agent_object.agent_name in browse_mode:
            mode = browse_mode[self._agent_object.agent_name]

        request_json = {
            "opType": operation_types[options['operation']],
            "mode": {
                "mode": mode
            },
            "paths": [{"path": path} for path in paths],
            "options": {
                "showDeletedFiles": options.get('show_deleted', False),
                "restoreIndex": options['restore_index'],
                "vsDiskBrowse": options['vm_disk_browse'],
                "vsFileBrowse": options.get('vs_file_browse', False),
                "includeMetadata": options.get('include_meta_data', False),
                "hideUserHidden": options.get('hide_user_hidden', False)
            },
            "entity": {
                "clientName": self._client_object.client_name,
                "clientId": int(self._client_object.client_id),
                "applicationId": int(self._agent_object.agent_id),
                "instanceId": int(self._instance_object.instance_id),
                "backupsetId": int(self.backupset_id),
                "subclientId": int(options['_subclient_id'])
            },
            "timeRange": {
                "fromTime": self._get_epoch_time(options['from_time']),
                "toTime": self._get_epoch_time(options['to_time'])
            },
            "advOptions": {
                "copyPrecedence": int(options['copy_precedence'])
            },
            "ma": {
                "clientName": options['media_agent']
            },
            "queries": [{
                "type": 0,
                "queryId": "dataQuery",
                "dataParam": {
                    "sortParam": {
                        "ascending": False,
                        "sortBy": [0]
                    },
                    "paging": {
                        "pageSize": int(options['page_size']),
                        "skipNode": int(options['skip_node']),
                        "firstNode": 0
                    }
                }
            }]
        }

        if options['filters']:
            # [('FileName', '*.txt'), ('FileSize','GT','100')]
            request_json['queries'][0]['whereClause'] = []

            for browse_filter in options['filters']:
                if browse_filter[0] in ('FileName', 'FileSize'):
                    temp_dict = {
                        'connector': 0,
                        'criteria': {
                            'field': browse_filter[0],
                            'values': [browse_filter[1]]
                        }
                    }

                    if browse_filter[0] == 'FileSize':
                        temp_dict['criteria']['dataOperator'] = browse_filter[2]

                    request_json['queries'][0]['whereClause'].append(temp_dict)

        if options['job_id'] != 0:
            request_json['advOptions']['advConfig'] = {
                'browseAdvancedConfigBrowseByJob': {
                    'jobId': options['job_id']
                }
            }


        if options.get('threatAnalysisRequest',False):
            request_json['options']['showMaliciousFiles'] = True
            request_json['options']['includeMetadata'] = True
            request_json['advOptions']['stubAsData'] = True
            request_json['advOptions']['advConfig'] = {
                'threatAnalysisRequest': True
            }
            request_json['queries'] = [
        {
            "type": 0,
            "queryId": "threatsList",
            "dataParam":
            {
                "sortParam":
                {
                    "ascending": True,
                    "sortBy":
                    [
                        38,
                        0
                    ]
                },
                "paging":
                {
                    "firstNode": 0,
                    "pageSize": int(options['page_size']),
                    "skipNode": int(options['skip_node'])
                }
            },
            "isFacet": 1,
            "fileOrFolder": 0,
            "whereClause":
            [
                {
                    "connector": 0,
                    "criteria":
                    {
                        "field": 38,
                        "dataOperator": 9,
                        "values":
                        [
                            "file"
                        ]
                    }
                }
            ]
        },
        {
            "type": 1,
            "queryId": "threatsListCount",
            "aggrParam":
            {
                "field": 0,
                "aggrType": 4
            },
            "isFacet": 1,
            "fileOrFolder": 0,
            "whereClause":
            [
                {
                    "connector": 0,
                    "criteria":
                    {
                        "field": 38,
                        "dataOperator": 9,
                        "values":
                        [
                            "file"
                        ]
                    }
                }
            ]
        }
    ]

        if options['include_aged_data']:
            request_json['options']['includeAgedData'] = True

        if options['include_meta_data']:
            request_json['options']['includeMetadata'] = True

        if options['include_hidden']:
            request_json['options']['includeHidden'] = True

        if options['include_running_jobs']:
            request_json['options']['includeRunningJobs'] = True

        if options['compute_folder_size']:
            request_json['options']['computeFolderSizeForFilteredBrowse'] = True

        if options['vs_volume_browse']:
            request_json['mode']['mode'] = 3
            request_json['options']['vsVolumeBrowse'] = True
            request_json['advOptions']['browseViewName'] = options['browse_view_name']

        if options['operation'] == 'list_media':
            request_json['options']['doPrediction'] = True

        if options['_custom_queries']:
            request_json['queries'] = options['_custom_queries']

        if options.get('live_browse', False):
            request_json['options']['liveBrowse'] = True

        if options.get('compare_backups_req', 0) != 0:
            request_json['mode']['mode'] = 3
            request_json['advOptions']['advConfig'] = {
                'compareBackupsReqType': int(options.get('compare_backups_req'))
            }
            if options.get('comparison_job_id', 0) != 0:
                request_json['applicationInfo'] = {
                    'indexingInfo': {
                        'jobId': int(options.get('comparison_job_id'))
                    }
                }

        return request_json

    def _process_browse_all_versions_response(self, result_set: list[dict], options: dict) -> dict:
        """Process the browse response to retrieve all versions of specified items.

        This method extracts items and their version information from the browse response
        returned by the server, using the provided options to filter or modify the results.

        Args:
            result_set: A list of dictionaries representing the browse response obtained from the server.
            options: A dictionary of browse options, such as {"show_deleted": True}.

        Returns:
            A dictionary containing the specified file(s) with a list of all file versions and
            additional metadata retrieved from the browse operation.

        Raises:
            SDKException: If the browse/search operation fails, the response is empty, or the response indicates failure.

        Example:
            >>> result_set = [
            ...     {"name": "file1.txt", "version": 1, "metadata": {...}},
            ...     {"name": "file1.txt", "version": 2, "metadata": {...}}
            ... ]
            >>> options = {"show_deleted": True}
            >>> versions_info = backupset._process_browse_all_versions_response(result_set, options)
            >>> print(versions_info)
            {'file1.txt': [{'version': 1, ...}, {'version': 2, ...}]}

        #ai-gen-doc
        """
        path = None
        versions_list = []
        show_deleted = options.get('show_deleted', False)

        for result in result_set:
            name = result['displayName']
            path = result['path']

            if 'modificationTime' in result:
                mod_time = time.localtime(int(result['modificationTime']))
                mod_time = time.strftime('%d/%m/%Y %H:%M:%S', mod_time)
            else:
                mod_time = None
            
            if 'backupTime' in result['advancedData'] and int(result['advancedData']['backupTime']) > 0:
                bkp_time = time.localtime(int(result['advancedData']['backupTime']))
                bkp_time = time.strftime('%d/%m/%Y %H:%M:%S', bkp_time)
            else:
                bkp_time = None

            if 'file' in result['flags']:
                if result['flags']['file'] in (True, '1'):
                    file_or_folder = 'File'
                else:
                    file_or_folder = 'Folder'
            else:
                file_or_folder = 'Folder'

            if 'size' in result:
                size = result['size']
            else:
                size = None

            if 'version' in result:
                version = result['version']
            else:
                version = None

            if show_deleted and 'deleted' in result.get('flags'):
                deleted = True if result['flags'].get('deleted') in (True, '1') else False
            else:
                deleted = None
                    
            paths_dict = {
                'name': name,
                'version': version,
                'size': size,
                'modified_time': mod_time,
                'type': file_or_folder,
                'backup_time': bkp_time,
                'advanced_data': result['advancedData'],
                'deleted': deleted
            }

            versions_list.append(paths_dict)

        all_versions_dict = dict()
        all_versions_dict[path] = versions_list

        return all_versions_dict

    def _process_browse_response(self, flag: bool, response: dict, options: dict) -> tuple[list, dict]:
        """Process the browse response and extract file or folder paths and associated metadata.

        Args:
            flag: Indicates whether the response from the server was successful.
            response: The JSON response dictionary received from the server for the browse request.
            options: Dictionary containing browse options used in the request.

        Returns:
            A tuple containing:
                - A list of file or folder paths extracted from the browse response.
                - A dictionary mapping each path to its associated metadata retrieved from the browse.

        Raises:
            SDKException: If the browse/search operation fails, the response is empty, or the response indicates failure.

        Example:
            >>> paths, metadata = backupset._process_browse_response(True, browse_response, browse_options)
            >>> print("Paths:", paths)
            >>> print("Metadata for first path:", metadata.get(paths[0], {}))

        #ai-gen-doc
        """

        operation_types = {
            "browse": ('110', 'Failed to browse for subclient backup content\nError: "{0}"'),
            "find": ('111', 'Failed to Search\nError: "{0}"'),
            "all_versions": (
                '112', 'Failed to browse all version for specified content\nError: "{0}"'
            ),
            "delete_data": (
                '113', 'Failed to perform delete data operation for given content\nError: "{0}"'
            ),
            "list_media": (
                '113', 'Failed to perform list media operation for given content\nError: "{0}"'
            )
        }

        exception_code = operation_types[options['operation']][0]
        exception_message = operation_types[options['operation']][1]
        
        show_deleted = options.get('show_deleted', False)

        if flag:

            response_json = response.json()
            paths_dict = {}
            paths = []
            result_set = None
            browse_result = None

            # Send raw result as browse response for advanced use cases
            if options['_raw_response']:
                return [], response_json

            if response_json and 'browseResponses' in response_json:
                _browse_responses = response_json['browseResponses']
                for browse_response in _browse_responses:
                    if "browseResult" in browse_response:
                        browse_result = browse_response['browseResult']
                        if 'dataResultSet' in browse_result:
                            result_set = browse_result['dataResultSet']
                            break

                if not browse_result:
                    try:
                        message = response_json['browseResponses'][0]['messages'][0]
                        error_message = message['errorMessage']

                        o_str = exception_message
                        raise SDKException('Subclient', '102', o_str.format(error_message))
                    except KeyError:
                        return [], {}

                if not result_set:
                    raise SDKException('Subclient', exception_code)

                if not isinstance(result_set, list):
                    result_set = [result_set]

                if 'all_versions' in options['operation']:
                    return self._process_browse_all_versions_response(result_set, options)

                for result in result_set:
                    name = result.get('displayName')
                    snap_display_name = result.get('name')

                    if 'path' in result:
                        path = result['path']
                    else:
                        path = '\\'.join([options['path'], name])

                    if 'modificationTime' in result and int(result['modificationTime']) > 0:
                        mod_time = time.localtime(int(result['modificationTime']))
                        mod_time = time.strftime('%d/%m/%Y %H:%M:%S', mod_time)
                    else:
                        mod_time = None
                    
                    if 'backupTime' in result['advancedData'] and int(result['advancedData']['backupTime']) > 0:
                        bkp_time = time.localtime(int(result['advancedData']['backupTime']))
                        bkp_time = time.strftime('%d/%m/%Y %H:%M:%S', bkp_time)
                    else:
                        bkp_time = None

                    if 'file' in result['flags']:
                        if result['flags']['file'] in (True, '1'):
                            file_or_folder = 'File'
                        else:
                            file_or_folder = 'Folder'
                    else:
                        file_or_folder = 'Folder'

                    if 'size' in result:
                        size = result['size']
                    else:
                        size = None
                        
                    if show_deleted and 'deleted' in result.get('flags'):
                        deleted = True if result['flags'].get('deleted') in (True, '1') else False
                    else:
                        deleted = None

                    paths_dict[path] = {
                        'name': name,
                        'snap_display_name': snap_display_name,
                        'size': size,
                        'modified_time': mod_time,
                        'type': file_or_folder,
                        'backup_time': bkp_time,
                        'advanced_data': result['advancedData'],
                        'deleted': deleted
                    }

                    if "threatAnalysisRequest" in options and options["threatAnalysisRequest"] and 'flags' in result:
                        paths_dict[path]['threatAnalysisData'] = result["flags"]

                    paths.append(path)

                return paths, paths_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _do_browse(self, options: Optional[Dict[str, Any]] = None, retry: int = 10) -> Union[List[str], Dict[str, Any]]:
        """Perform a browse operation on the backupset with the specified options.

        This method initiates a browse request using the provided options and returns either a list of file/folder paths 
        or a dictionary containing paths with additional metadata, depending on the browse response.

        Args:
            options: Optional dictionary specifying browse options such as filters, path, or other parameters.
            retry: Number of times to retry the browse operation in case of failure. Default is 10.

        Returns:
            A list of file and folder paths if the browse response contains only paths.
            A dictionary mapping paths to their metadata if the browse response includes additional information.

        Example:
            >>> backupset = Backupset()
            >>> # Browse for all files in a specific folder
            >>> browse_options = {'path': '/home/user/documents'}
            >>> result = backupset._do_browse(browse_options)
            >>> if isinstance(result, list):
            >>>     print("File/Folder paths:", result)
            >>> elif isinstance(result, dict):
            >>>     for path, metadata in result.items():
            >>>         print(f"Path: {path}, Metadata: {metadata}")

        #ai-gen-doc
        """
        if options is None:
            options = {}

        options = self._prepare_browse_options(options)
        request_json = self._prepare_browse_json(options)

        flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)

        attempt = 1
        while attempt <= retry:
            if response.json() == {}:
                time.sleep(120)
                flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)
            else:
                break
            attempt += 1
        return self._process_browse_response(flag, response, options)

    def update_properties(self, properties_dict: dict) -> None:
        """Update the properties of the backupset.

        This method updates the backupset's properties using the provided dictionary.
        To modify properties safely, use `self.properties` to obtain a deep copy of the current properties,
        make the necessary changes, and then pass the updated dictionary to this method.

        Args:
            properties_dict: Dictionary containing the backupset properties to update.

        Raises:
            SDKException: If the update fails, the response is empty, or the response code is not as expected.

        Example:
            >>> backupset = Backupset()
            >>> props = backupset.properties  # Get a deep copy of current properties
            >>> props['backupType'] = 'Full'  # Modify the desired property
            >>> backupset.update_properties(props)  # Update the backupset with new properties

        #ai-gen-doc
        """
        request_json = {
            "backupsetProperties": {},
            "association": {
                "entity": [
                    {
                        "clientName": self._client_object.client_name,
                        "backupsetName": self.backupset_name,
                        "instanceName": self._instance_object.instance_name,
                        "appName": self._agent_object.agent_name
                    }
                ]
            }
        }

        request_json['backupsetProperties'].update(properties_dict)
        status, _, error_string = self._process_update_reponse(request_json)

        if not status:
            raise SDKException(
                'Backupset',
                '102',
                'Failed to update backupset property\nError: "{0}"'.format(error_string))

    @property
    def properties(self) -> dict:
        """Get the properties of the backupset.

        Returns:
            dict: A dictionary containing the properties and configuration details of the backupset.

        Example:
            >>> backupset = Backupset()
            >>> props = backupset.properties
            >>> print(props)
            >>> # Output will be a dictionary with backupset configuration details

        #ai-gen-doc
        """
        return copy.deepcopy(self._properties)

    @property
    def name(self) -> str:
        """Get the display name of the backupset.

        Returns:
            The display name of the backupset as a string.

        Example:
            >>> backupset = Backupset()
            >>> display_name = backupset.name  # Use dot notation for property access
            >>> print(f"Backupset name: {display_name}")

        #ai-gen-doc
        """
        return self._properties["backupSetEntity"]["backupsetName"]

    @property
    def backupset_id(self) -> str:
        """Get the unique identifier of the backupset as a read-only property.

        Returns:
            The backupset ID as a string.

        Example:
            >>> backupset = Backupset(commcell_object, client_name, instance_name, backupset_name)
            >>> backupset_id = backupset.backupset_id  # Access the backupset ID property
            >>> print(f"Backupset ID: {backupset_id}")

        #ai-gen-doc
        """
        return self._backupset_id

    @property
    def backupset_name(self) -> str:
        """Get the name of the backupset associated with this Backupset instance.

        Returns:
            The name of the backupset as a string.

        Example:
            >>> backupset = Backupset()
            >>> name = backupset.backupset_name  # Access the backupset name property
            >>> print(f"Backupset name: {name}")

        #ai-gen-doc
        """
        return self._backupset_name

    @property
    def description(self) -> str:
        """Get the description of the backupset.

        Returns:
            The description string associated with this backupset.

        Example:
            >>> backupset = Backupset(commcell_object, client_name, instance_name, backupset_name)
            >>> desc = backupset.description  # Access the description property
            >>> print(f"Backupset description: {desc}")

        #ai-gen-doc
        """
        return self._description

    @property
    def is_default_backupset(self) -> bool:
        """Indicate whether this backupset is the default backupset.

        Returns:
            True if this backupset is the default backupset, False otherwise.

        Example:
            >>> backupset = Backupset()
            >>> if backupset.is_default_backupset:
            ...     print("This is the default backupset.")
            ... else:
            ...     print("This is not the default backupset.")

        #ai-gen-doc
        """
        return self._is_default

    @property
    def is_on_demand_backupset(self) -> bool:
        """Indicate whether this backupset is an on-demand backupset.

        This property provides a read-only boolean value that specifies if the backupset
        is configured as an on-demand backupset.

        Returns:
            True if the backupset is on-demand; False otherwise.

        Example:
            >>> backupset = Backupset()
            >>> if backupset.is_on_demand_backupset:
            ...     print("This is an on-demand backupset.")
            ... else:
            ...     print("This is a regular backupset.")

        #ai-gen-doc
        """
        return self._is_on_demand_backupset

    @property
    def plan(self) -> 'Plan':
        """Get the plan associated with this Backupset as a property.

        Returns:
            Plan: The plan object linked to the current Backupset.

        Example:
            >>> backupset = Backupset(commcell_object, client_name, instance_name, backupset_name)
            >>> plan = backupset.plan  # Access the plan property
            >>> print(f"Plan name: {plan.name}")
            >>> # The returned Plan object can be used for further plan management

        #ai-gen-doc
        """
        if self._plan_obj is not None:
            return self._plan_obj
        elif self._plan_name is not None:
            self._plan_obj = self._commcell_object.plans.get(self._plan_name)
            return self._plan_obj
        else:
            return None

    @property
    def guid(self) -> str:
        """Get the GUID (Globally Unique Identifier) of the backupset.

        This property provides access to the unique identifier associated with the backupset instance.

        Returns:
            The backupset GUID as a string.

        Example:
            >>> backupset = Backupset(commcell_object, client_name, instance_name, backupset_name)
            >>> guid = backupset.guid  # Use dot notation to access the property
            >>> print(f"Backupset GUID: {guid}")

        #ai-gen-doc
        """
        if self._properties.get('backupSetEntity'):
            if self._properties['backupSetEntity'].get('backupsetGUID'):
                return self._properties['backupSetEntity']['backupsetGUID']
            raise SDKException('Backupset', '102', 'Backupset GUID not found')
        raise SDKException('Backupset', '102', 'Backupset entity not found')

    @backupset_name.setter
    def backupset_name(self, value: str) -> None:
        """Set the name of the backupset to the specified value.

        Args:
            value: The new name to assign to the backupset. Must be a string.

        Raises:
            SDKException: If the backupset name could not be updated, or if the provided value is not a string.

        Example:
            >>> backupset = Backupset()
            >>> backupset.backupset_name = "NewBackupsetName"  # Use assignment to set the backupset name
            >>> print("Backupset name updated successfully")

        #ai-gen-doc
        """
        if isinstance(value, str):
            output = self._update(
                backupset_name=value,
                backupset_description=self.description,
                default_backupset=self.is_default_backupset
            )

            if output[0]:
                return
            o_str = 'Failed to update the name of the backupset\nError: "{0}"'
            raise SDKException('Backupset', '102', o_str.format(output[2]))

        raise SDKException('Backupset', '102', 'Backupset name should be a string value')

    @description.setter
    def description(self, value: str) -> None:
        """Set the description of the backupset to the specified value.

        Args:
            value: The new description to assign to the backupset. Must be a string.

        Raises:
            SDKException: If the description update fails, if the input value is not a string,
                or if the description cannot be modified for this backupset.

        Example:
            >>> backupset = Backupset(commcell_object, client_name, instance_name, backupset_name)
            >>> backupset.description = "Monthly full backup for critical data"
            >>> # The backupset description is now updated to the provided string

        #ai-gen-doc
        """
        if self.description is not None:
            if isinstance(value, str):
                output = self._update(
                    backupset_name=self.backupset_name,
                    backupset_description=value,
                    default_backupset=self.is_default_backupset
                )

                if output[0]:
                    return

                o_str = 'Failed to update the description of the backupset\nError: "{0}"'
                raise SDKException('Backupset', '102', o_str.format(output[2]))

            raise SDKException(
                'Backupset', '102', 'Backupset description should be a string value'
            )

        raise SDKException('Backupset', '102', 'Description cannot be modified')

    @plan.setter
    def plan(self, value: 'Union[object, str, None]') -> None:
        """Associate or remove a plan from the backupset.

        This setter allows you to associate a plan with the backupset by providing either a Plan object,
        the name of the plan as a string, or remove the association by setting the value to None.

        Args:
            value: The plan to associate with the backupset. This can be:
                - A Plan object to associate with the backupset.
                - A string representing the name of the plan to associate.
                - None to remove any existing plan association.

        Raises:
            SDKException: If the specified plan does not exist, the association fails, or the plan is not eligible.

        Example:
            >>> backupset.plan = plan_obj  # Associate using a Plan object
            >>> backupset.plan = "GoldPlan"  # Associate using the plan name
            >>> backupset.plan = None  # Remove any plan association

        #ai-gen-doc
        """
        from .plan import Plan
        if isinstance(value, Plan):
            self._plan_obj = value
        elif isinstance(value, str):
            self._plan_obj = self._commcell_object.plans.get(value)
        elif value is None:
            self._plan_obj = None
        else:
            raise SDKException('Backupset', '102', 'Input value is not of supported type')

        plans_obj = self._commcell_object.plans
        entity_dict = {
            'clientId': int(self._client_object.client_id),
            'appId': int(self._agent_object.agent_id),
            'backupsetId': int(self.backupset_id)
        }
        if value is not None and self._plan_obj.plan_name in plans_obj.get_eligible_plans(entity_dict):
            request_json = {
                'backupsetProperties': {
                    'planEntity': {
                        'planSubtype': int(self._plan_obj.subtype),
                        '_type_': 158,
                        'planType': int(self._plan_obj.plan_type),
                        'planName': self._plan_obj.plan_name,
                        'planId': int(self._plan_obj.plan_id)
                    }
                }
            }

            response = self._process_update_reponse(
                request_json
            )

            if response[0]:
                return
            else:
                o_str = 'Failed to asspciate plan to the backupset\nError: "{0}"'
                raise SDKException('Backupset', '102', o_str.format(response[2]))
        elif value is None:
            request_json = {
                'backupsetProperties': {
                    'removePlanAssociation': True
                }
            }

            response = self._process_update_reponse(
                request_json
            )

            if response[0]:
                return
            else:
                o_str = 'Failed to dissociate plan from backupset\nError: "{0}"'
                raise SDKException('Backupset', '102', o_str.format(response[2]))
        else:
            raise SDKException(
                'Backupset',
                '102',
                'Plan not eligible to be associated with the backupset'
            )

    def set_default_backupset(self) -> None:
        """Set this backupset as the default backupset if it is not already set.

        This method updates the default backupset for the associated client/application
        to the backupset represented by this instance. If the operation fails, an
        SDKException is raised.

        Raises:
            SDKException: If the backupset could not be set as the default.

        Example:
            >>> backupset = Backupset(client_object, 'UserBackupset')
            >>> backupset.set_default_backupset()
            >>> print("Backupset is now set as default.")

        #ai-gen-doc
        """
        if self.is_default_backupset is False:
            output = self._update(
                backupset_name=self.backupset_name,
                backupset_description=self.description,
                default_backupset=True
            )

            if output[0]:
                return

            o_str = 'Failed to set this as the Default Backup Set\nError: "{0}"'
            raise SDKException('Backupset', '102', o_str.format(output[2]))

    def backup(self, **kwargs: dict) -> list:
        """Run backup jobs for all subclients in this backupset.

        This method initiates backup jobs for each subclient associated with the backupset.
        You can specify various backup options using keyword arguments, which are passed
        to each subclient's backup operation.

        Commonly used keyword arguments include:
            - backup_level (str): The level of backup to perform. Options are
              'Full', 'Incremental', 'Differential', or 'Synthetic_full'.
              Default is 'Incremental'.
            - advanced_options (dict): Advanced backup options to include in the request.
            - common_backup_options (dict): Advanced job options to include in the request.

        For a complete list of supported arguments, refer to the documentation for `subclient.backup()`.

        Returns:
            list: A list of job objects representing the backup jobs started for each subclient in the backupset.

        Example:
            >>> backupset = Backupset()
            >>> jobs = backupset.backup(backup_level='Full')
            >>> print(f"Started {len(jobs)} backup jobs for the backupset")
            >>> # Each item in 'jobs' is a job object for a subclient backup

        #ai-gen-doc
        """
        return_list = []
        thread_list = []

        if self.subclients.all_subclients:
            for subclient in self.subclients.all_subclients:
                thread = threading.Thread(
                    target=self._run_backup, args=(subclient, return_list), kwargs=kwargs
                )
                thread_list.append(thread)
                thread.start()

        for thread in thread_list:
            thread.join()

        return return_list

    def browse(self, *args: Any, **kwargs: Any) -> tuple[list, dict]:
        """Browse the content of the Backupset.

        This method allows you to browse files and folders within the backupset, 
        supporting both positional and keyword arguments for browse options.

        You can specify browse options either as a dictionary or as keyword arguments.
        Common options include:
            - path: The path to browse (e.g., 'c:\\hello')
            - show_deleted: Whether to include deleted items (bool)
            - from_time: Start time for the browse window (str, format 'YYYY-MM-DD HH:MM:SS')
            - to_time: End time for the browse window (str, format 'YYYY-MM-DD HH:MM:SS')

        For a full list of supported options, refer to the 
        `default_browse_options` documentation:
        https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        Returns:
            tuple[list, dict]: 
                - A list of file and folder paths from the browse response.
                - A dictionary containing all paths with additional metadata from the browse operation.

        Example:
            >>> # Using a dictionary of browse options
            >>> file_list, metadata = backupset.browse({
            ...     'path': 'c:\\hello',
            ...     'show_deleted': True,
            ...     'from_time': '2014-04-20 12:00:00',
            ...     'to_time': '2016-04-21 12:00:00'
            ... })
            >>> print(file_list)
            >>> print(metadata)
            >>>
            >>> # Using keyword arguments
            >>> file_list, metadata = backupset.browse(
            ...     path='c:\\hello',
            ...     show_deleted=True,
            ...     from_time='2014-04-20 12:00:00',
            ...     to_time='2016-04-21 12:00:00'
            ... )
            >>> print(file_list)
            >>> print(metadata)

        #ai-gen-doc
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'browse'

        return self._do_browse(options)

    def find(self, *args: Any, **kwargs: Any) -> tuple[list, dict]:
        """Search for files or folders in the backed up content of the backupset matching specified filters.

        This method allows you to search for files and folders within the backupset using various filter options.
        You can provide search criteria either as a single dictionary of options or as keyword arguments.

        Supported filter options include:
            - file_name (str): Pattern to match file names (e.g., '*.txt').
            - show_deleted (bool): Whether to include deleted files in the results.
            - from_time (str): Start time for the search range (format: 'YYYY-MM-DD HH:MM:SS').
            - to_time (str): End time for the search range (format: 'YYYY-MM-DD HH:MM:SS').
            - file_size_gt (int): Find files with size greater than the specified value (in bytes).
            - file_size_lt (int): Find files with size less than the specified value (in bytes).
            - file_size_et (int): Find files with size equal to the specified value (in bytes).

        For a complete list of supported options, refer to the
        `default_browse_options`_ documentation.

        Returns:
            tuple[list, dict]: 
                - A list of file and folder paths matching the search criteria.
                - A dictionary containing all matched paths with additional metadata from the browse operation.

        Example:
            >>> # Using a dictionary of options
            >>> results, metadata = backupset.find({
            ...     'file_name': '*.txt',
            ...     'show_deleted': True,
            ...     'from_time': '2022-01-01 00:00:00',
            ...     'to_time': '2022-12-31 23:59:59'
            ... })
            >>> print(f"Found {len(results)} .txt files")

            >>> # Using keyword arguments
            >>> results, metadata = backupset.find(
            ...     file_name='report_*.csv',
            ...     file_size_gt=1024,
            ...     show_deleted=False
            ... )
            >>> for path in results:
            ...     print(path)

        .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        #ai-gen-doc
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        if 'operation' not in options:
            options['operation'] = 'find'

        if 'path' not in options:
            options['path'] = '\\**\\*'

        if 'filters' not in options:
            options['filters'] = []

        if 'file_name' in options:
            options['filters'].append(('FileName', options['file_name']))

        if 'file_size_gt' in options:
            options['filters'].append(('FileSize', options['file_size_gt'], 'GTE'))

        if 'file_size_lt' in options:
            options['filters'].append(('FileSize', options['file_size_lt'], 'LTE'))

        if 'file_size_et' in options:
            options['filters'].append(('FileSize', options['file_size_et'], 'EQUALSBLAH'))

        return self._do_browse(options)

    def delete_data(self, paths: Union[str, List[str]]) -> None:
        """Delete specified items from the backupset index, making them unavailable for browsing and recovery.

        Args:
            paths: A single path as a string, or a list of paths, specifying the items to delete from the backupset.

        Raises:
            Exception: If the delete data request cannot be prepared, the response is invalid, or the request fails.

        Example:
            >>> backupset = Backupset()
            >>> # Delete a single file from the backupset
            >>> backupset.delete_data('/data/old_file.txt')
            >>> # Delete multiple directories from the backupset
            >>> backupset.delete_data(['/data/dir1', '/data/dir2'])
            >>> print("Delete request sent successfully.")

        #ai-gen-doc
        """

        options = {
            'operation': 'delete_data',
            'path': paths
        }

        files, _ = self._do_browse(options)

        # Delete operation does not return any result, hence consider the operation successful
        if files:
            raise SDKException('Backupset', '102', 'Delete data operation gave unexpected results')

    def list_media(self, *args: Any, **kwargs: Any) -> Union[List[Any], Dict[str, Any]]:
        """List media required to browse and restore backed up data from the backupset.

        This method retrieves the list of media required for browsing and restoring data from the backupset,
        based on the provided options. Options can be supplied either as a dictionary or as keyword arguments.

        Args:
            *args: Optional positional arguments. Typically, a single dictionary containing browse options.
            **kwargs: Optional keyword arguments specifying browse options directly.

        Supported options include (but are not limited to):
            - path (str): Path to the data to browse.
            - show_deleted (bool): Whether to include deleted items.
            - from_time (str): Start time for the browse operation (format: 'YYYY-MM-DD HH:MM:SS').
            - to_time (str): End time for the browse operation (format: 'YYYY-MM-DD HH:MM:SS').

        Note:
            Refer to the `_default_browse_options` attribute for all supported options.

        Returns:
            Union[List[Any], Dict[str, Any]]:
                - List of all media required for the given options.
                - Dictionary containing the total size of the media.

        Raises:
            SDKException: If the media listing fails or the response is not successful.

        Example:
            >>> # Using a dictionary of options
            >>> media_list, media_size = backupset.list_media({
            ...     'path': 'c:\\hello',
            ...     'show_deleted': True,
            ...     'from_time': '2020-04-20 12:00:00',
            ...     'to_time': '2021-04-19 12:00:00'
            ... })
            >>> print(f"Media required: {media_list}")
            >>> print(f"Total media size: {media_size}")

            >>> # Using keyword arguments
            >>> media_list, media_size = backupset.list_media(
            ...     path='c:\\hello',
            ...     show_deleted=True,
            ...     from_time='2020-04-20 12:00:00',
            ...     to_time='2021-04-19 12:00:00'
            ... )
            >>> print(f"Media required: {media_list}")
            >>> print(f"Total media size: {media_size}")

        #ai-gen-doc
        """

        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'list_media'
        options['_raw_response'] = True

        _, response = self._do_browse(options)

        if response and 'browseResponses' in response:
            responses = response['browseResponses']
            list_media_response = responses[0]

            prediction_data = list_media_response.get('predictionData', [])
            browse_result = list_media_response.get('browseResult', {})

            return prediction_data, browse_result
        else:
            raise SDKException('Backupset', '102', 'List media operation gave unexpected results')

    def refresh(self) -> None:
        """Reload the properties of the Backupset to reflect the latest state.

        This method refreshes the Backupset's properties, ensuring that any changes 
        made externally or in the Commcell are updated in the current object instance.

        Example:
            >>> backupset = Backupset(commcell_object, client_name, instance_name, backupset_name)
            >>> backupset.refresh()
            >>> print("Backupset properties refreshed successfully")

        #ai-gen-doc
        """
        self._get_backupset_properties()

        self.subclients = Subclients(self)
        self.schedules = Schedules(self)

    def backed_up_files_count(self, path: str = "\\**\\*") -> int:
        """Get the total number of files backed up in all subclients of this backupset for a given path.

        Args:
            path: The folder path to search for backed up files. Supports wildcards.
                Default is "\\**\\*", which searches all files in all folders.

        Returns:
            The number of files backed up in the specified path across all subclients.

        Raises:
            Exception: If the browse response is not proper or an error occurs during the count.

        Example:
            >>> backupset = Backupset()
            >>> count = backupset.backed_up_files_count()
            >>> print(f"Total backed up files: {count}")
            >>> # To count files in a specific folder:
            >>> count = backupset.backed_up_files_count('C:\\Users\\Documents\\*')
            >>> print(f"Files in Documents: {count}")

        #ai-gen-doc
        """
        options_dic = {"operation": "find", "opType": 1, "path": path,
                       "_custom_queries": [{"type": "AGGREGATE", "queryId": "2",
                                            "aggrParam": {"aggrType": "COUNT"}, "whereClause": [{
                                                "criteria": {
                                                    "field": "Flags",
                                                    "dataOperator": "IN",
                                                    "values": ["file"]
                                                }
                                            }]}], "_raw_response": True}

        browse_response = self._do_browse(options_dic)
        if not len(browse_response) > 1:
            raise SDKException('Backupset', '102', 'Browse response is not proper')
        browse_response = browse_response[1]
        if 'browseResponses' not in browse_response or len(browse_response['browseResponses']) == 0:
            raise SDKException('Backupset', '102', 'Browse response is missing browseResponses')
        browse_response = browse_response['browseResponses'][0]
        if 'browseResult' not in browse_response:
            raise SDKException('Backupset', '102', 'Browse response is missing browseResult')
        browse_result = browse_response['browseResult']
        if 'aggrResultSet' not in browse_result or len(browse_result['aggrResultSet']) == 0:
            raise SDKException('Backupset', '102', 'Browse response is missing aggrResultSet')
        return browse_result['aggrResultSet'][0].get('count', 0)