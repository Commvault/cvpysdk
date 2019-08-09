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

from ..agent import Agent
from ..subclient import Subclients


class ExchangeDatabaseAgent(Agent):
    """Derived class from the Agent Base class,
        to perform operations specific to an Exchange Database Agent."""

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
    def subclients(self):
        """Returns the instance of the Subclients class representing the list of Subclients
        installed / configured on the Client for the selected Agent.
        """
        if self._subclients is None:
            self._subclients = Subclients(self)

        return self._subclients

    def backup(self):
        """Runs Incremental backup job for all subclients belonging to the Exchange Database Agent.

            Runs Full Backup job for a subclient, if no job had been ran earlier for it.

            Returns:
                list    -   list consisting of the job objects for the backup jobs started for
                the subclients in the agent

        """
        return self._backupset_object.backup()

    def browse(self, *args, **kwargs):
        """Browses the content of the Exchange Database Agent.

            Args:
                Dictionary of browse options:
                    Example:

                        browse({
                            'path': 'c:\\\\hello',

                            'show_deleted': True,

                            'from_time': '2014-04-20 12:00:00',

                            'to_time': '2016-04-21 12:00:00'
                        })

            Kwargs:
                Keyword argument of browse options:
                    Example:

                        browse(
                            path='c:\\hello',

                            show_deleted=True,

                            from_time='2014-04-20 12:00:00',

                            to_time='2016-04-21 12:00:00'
                        )

            Returns:
                (list, dict)
                    list    -   List of only the file, folder paths from the browse response

                    dict    -   Dictionary of all the paths with additional metadata retrieved
                    from browse operation


            Refer `default_browse_options`_ for all the supported options.

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        return self._instance_object.browse(*args, **kwargs)

    def find(self, *args, **kwargs):
        """Searches a file/folder in the backed up content of the agent,
            and returns all the files matching the filters given.

            Args:
                Dictionary of browse options:
                    Example:

                        find({
                            'file_name': '*.txt',

                            'show_deleted': True,

                            'from_time': '2014-04-20 12:00:00',

                            'to_time': '2016-04-31 12:00:00'
                        })

            Kwargs:
                Keyword argument of browse options:
                    Example:

                        find(
                            file_name='*.txt',

                            show_deleted=True,

                            'from_time': '2014-04-20 12:00:00',

                            to_time='2016-04-31 12:00:00'
                        )

            Returns:
                (list, dict)
                    list    -   List of only the file, folder paths from the browse response

                    dict    -   Dictionary of all the paths with additional metadata retrieved
                    from browse operation


            Refer `default_browse_options`_ for all the supported options.

            Additional options supported:
                file_name       (str)   --  Find files with name

                file_size_gt    (int)   --  Find files with size greater than size

                file_size_lt    (int)   --  Find files with size lesser than size

                file_size_et    (int)   --  Find files with size equal to size

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        return self._instance_object.find(*args, **kwargs)

    def refresh(self):
        """Refresh the properties of the Agent."""
        super(ExchangeDatabaseAgent, self).refresh()

        self._subclients = None
