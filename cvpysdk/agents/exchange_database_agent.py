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

"""Module for doing operations on an Exchange Database Agent.

This module has operations that are applicable at the Agent level for Exchange Database.

ExchangeDatabaseAgent:
    __init__()      --  initialize object of Agent with the specified agent name
    and id, and associated to the specified client

    backup()        --  runs backup for all subclients present in the Agent

    browse()        --  browse the backed up content of the agent

    find()          --  searches the backed up content in the agent for the given file / folder

    refresh()       --  refresh the properties of the object


Attributes
----------

    **subclients**  --  returns the instance of the Subclients class, listing the subclients
    associated to the Agent


"""

from __future__ import unicode_literals

from typing import Any, Optional, List, Tuple, Dict

from ..agent import Agent
from ..subclient import Subclients

class ExchangeDatabaseAgent(Agent):
    """
    Specialized agent class for managing Exchange Database operations.

    This class extends the Agent base class to provide functionality specific
    to Exchange Database management, including backup, browsing, searching,
    and refreshing database information. It is initialized with client-specific
    details and maintains access to subclients for granular control.

    Key Features:
        - Initialization with client object, agent name, and agent ID
        - Property access to subclients for database management
        - Backup operations for Exchange databases
        - Browsing of database contents
        - Search functionality within the database
        - Refreshing of agent and database state

    #ai-gen-doc
    """

    def __init__(self, client_object: Any, agent_name: str, agent_id: Optional[str] = None) -> None:
        """Initialize an ExchangeDatabaseAgent instance for a specific client and agent.

        Args:
            client_object: Instance of the Client class representing the target client.
            agent_name: Name of the agent (e.g., "File System", "Virtual Server").
            agent_id: Optional string specifying the agent's unique identifier.

        Example:
            >>> client = Client(...)
            >>> agent = ExchangeDatabaseAgent(client, "Exchange Database", agent_id="12345")
            >>> # The agent object is now initialized and ready for further operations

        #ai-gen-doc
        """
        super(ExchangeDatabaseAgent, self).__init__(client_object, agent_name, agent_id)

        if self.instances.has_instance('defaultInstance'):
            self._instance_object = self.instances.get('defaultInstance')
        else:
            self._instance_object = self.instances.get(
                sorted(self.instances.all_instances)[0]
            )

        if self._instance_object.backupsets.has_backupset('defaultBackupSet'):
            self._backupset_object = self._instance_object.backupsets.get('defaultBackupSet')
        else:
            self._backupset_object = self._instance_object.backupsets.get(
                sorted(self._instance_object.backupsets.all_backupsets)[0]
            )

        self._subclients = None

    @property
    def subclients(self) -> 'Subclients':
        """Get the Subclients instance for the Exchange Database Agent.

        This property provides access to the Subclients object, which represents
        the list of subclients installed or configured on the client for the selected agent.

        Returns:
            Subclients: An instance for managing and accessing subclient information.

        Example:
            >>> agent = ExchangeDatabaseAgent(...)
            >>> subclients = agent.subclients  # Use dot notation for property access
            >>> print(f"Total subclients: {len(subclients)}")
            >>> # The returned Subclients object can be used to manage subclients

        #ai-gen-doc
        """
        if self._subclients is None:
            self._subclients = Subclients(self)

        return self._subclients

    def backup(self) -> List[Any]:
        """Run backup jobs for all subclients in the Exchange Database Agent.

        This method initiates an incremental backup for each subclient associated with the agent.
        If a subclient has not previously had a backup job run, a full backup will be performed instead.

        Returns:
            List of job objects representing the backup jobs started for each subclient.

        Example:
            >>> agent = ExchangeDatabaseAgent(...)
            >>> jobs = agent.backup()
            >>> print(f"Started {len(jobs)} backup jobs")
            >>> # Each item in 'jobs' is a job object for a subclient backup

        #ai-gen-doc
        """
        return self._backupset_object.backup()

    def browse(self, *args: Any, **kwargs: Any) -> Tuple[List[str], Dict[str, Any]]:
        """Browse the content of the Exchange Database Agent.

        This method allows you to retrieve file and folder paths, along with associated metadata,
        from the Exchange Database Agent using flexible browse options. Options can be provided
        either as a dictionary or as keyword arguments.

        Args:
            *args: Optional positional arguments, typically a dictionary of browse options.
                Example:
                    >>> agent.browse({
                    ...     'path': 'c:\\hello',
                    ...     'show_deleted': True,
                    ...     'from_time': '2014-04-20 12:00:00',
                    ...     'to_time': '2016-04-21 12:00:00'
                    ... })

            **kwargs: Optional keyword arguments for browse options.
                Example:
                    >>> agent.browse(
                    ...     path='c:\\hello',
                    ...     show_deleted=True,
                    ...     from_time='2014-04-20 12:00:00',
                    ...     to_time='2016-04-21 12:00:00'
                    ... )

        Returns:
            A tuple containing:
                - List of file and folder paths from the browse response.
                - Dictionary with all paths and additional metadata retrieved from the browse operation.

        Example:
            >>> # Using a dictionary of options
            >>> paths, metadata = agent.browse({
            ...     'path': 'c:\\hello',
            ...     'show_deleted': True
            ... })
            >>> print(paths)
            >>> print(metadata)

            >>> # Using keyword arguments
            >>> paths, metadata = agent.browse(path='c:\\hello', show_deleted=True)
            >>> print(paths)
            >>> print(metadata)

        Refer to the default browse options for all supported parameters:
        https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        #ai-gen-doc
        """
        return self._instance_object.browse(*args, **kwargs)

    def find(self, *args: Any, **kwargs: Any) -> Tuple[List[str], Dict[str, Any]]:
        """Search for files or folders in the backed-up content of the Exchange Database agent.

        This method allows you to search for files and folders using various filters and options.
        You can provide search criteria either as a dictionary of browse options or as keyword arguments.

        Args:
            *args: Optional positional arguments, typically a dictionary of browse options.
                Example:
                    >>> agent.find({
                    ...     'file_name': '*.txt',
                    ...     'show_deleted': True,
                    ...     'from_time': '2014-04-20 12:00:00',
                    ...     'to_time': '2016-04-31 12:00:00'
                    ... })

            **kwargs: Optional keyword arguments for browse options.
                Example:
                    >>> agent.find(
                    ...     file_name='*.txt',
                    ...     show_deleted=True,
                    ...     from_time='2014-04-20 12:00:00',
                    ...     to_time='2016-04-31 12:00:00'
                    ... )

        Returns:
            Tuple containing:
                - List of file and folder paths matching the search criteria.
                - Dictionary with additional metadata for each path retrieved from the browse operation.

        Example:
            >>> # Search for all .txt files, including deleted ones, within a date range
            >>> file_list, metadata = agent.find(
            ...     file_name='*.txt',
            ...     show_deleted=True,
            ...     from_time='2014-04-20 12:00:00',
            ...     to_time='2016-04-31 12:00:00'
            ... )
            >>> print(f"Found files: {file_list}")
            >>> print(f"Metadata: {metadata}")

        Refer to the default browse options documentation for all supported filters:
        https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        Additional supported options include:
            - file_name (str): Find files by name pattern.
            - file_size_gt (int): Find files larger than the specified size.
            - file_size_lt (int): Find files smaller than the specified size.
            - file_size_et (int): Find files equal to the specified size.

        #ai-gen-doc
        """
        return self._instance_object.find(*args, **kwargs)

    def refresh(self) -> None:
        """Reload the properties of the ExchangeDatabaseAgent.

        This method refreshes the agent's state and clears cached subclient information,
        ensuring that subsequent accesses retrieve the latest data.

        Example:
            >>> agent = ExchangeDatabaseAgent(...)
            >>> agent.refresh()  # Refresh agent properties and subclient cache
            >>> print("Agent properties refreshed successfully")

        #ai-gen-doc
        """
        super(ExchangeDatabaseAgent, self).refresh()

        self._subclients = None
