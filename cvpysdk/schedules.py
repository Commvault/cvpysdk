#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing schedule related operations for client/agent/backupset/subclient.

Schedules: Initializes instance of all schedules for a commcell entity.

Schedules:
    __init__(class_object)          --  initialise object of the Schedules class

    __str__()                       --  string of all schedules associated with the commcell entity

    __repr__()                      --  returns the string for the instance of the Schedules class

    _get_schedules()                --  gets all the schedules associated with the commcell entity

    has_schedule(schedule_name)     --  checks if schedule exists for the comcell entity or not

"""

from __future__ import absolute_import

from .exception import SDKException


class Schedules(object):
    """Class for getting the schedules of a commcell entity."""

    def __init__(self, class_object):
        """Initialise the Schedules class instance.

            Args:
                class_object (object)  --  instance of the client/agent/backupset/subclient class

            Returns:
                object - instance of the Schedules class

            Raises:
                SDKException:
                    if class object does not belong to any of the Client or Agent or Backupset or
                        Subclient class
        """
        # imports inside the __init__ method definition to avoid cyclic imports
        from .client import Client
        from .agent import Agent
        from .backupset import Backupset
        from .subclient import Subclient

        self._commcell_object = class_object._commcell_object

        self._repr_str = ""

        if isinstance(class_object, Client):
            self._SCHEDULES = self._commcell_object._services.CLIENT_SCHEDULES % (
                class_object.client_id
            )
            self._repr_str = "Client: {0}".format(class_object.client_name)
        elif isinstance(class_object, Agent):
            self._SCHEDULES = self._commcell_object._services.AGENT_SCHEDULES % (
                class_object._client_object.client_id,
                class_object.agent_id
            )
            self._repr_str = "Agent: {0}".format(class_object.agent_name)
        elif isinstance(class_object, Backupset):
            self._SCHEDULES = self._commcell_object._services.BACKUPSET_SCHEDULES % (
                class_object._agent_object._client_object.client_id,
                class_object._agent_object.agent_id,
                class_object.backupset_id
            )
            self._repr_str = "Backupset: {0}".format(class_object.backupset_name)
        elif isinstance(class_object, Subclient):
            self._SCHEDULES = self._commcell_object._services.SUBCLIENT_SCHEDULES % (
                class_object._backupset_object._agent_object._client_object.client_id,
                class_object._backupset_object._agent_object.agent_id,
                class_object._backupset_object.backupset_id,
                class_object.subclient_id
            )
            self._repr_str = "Subclient: {0}".format(class_object.subclient_name)
        else:
            raise SDKException('Schedules', '101')

        self.schedules = self._get_schedules()

    def __str__(self):
        """Representation string consisting of all schedules of the commcell entity.

            Returns:
                str - string of all the schedules associated with the commcell entity
        """
        if self.schedules:
            representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Schedule')

            for index, schedule in enumerate(self.schedules):
                sub_str = '{:^5}\t{:20}\n'.format(index + 1, schedule)
                representation_string += sub_str
        else:
            representation_string = 'No Schedules are associated to this Commcell Entity'

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Schedules class."""
        return "Schedules class instance for {0}".format(self._repr_str)

    def _get_schedules(self):
        """Gets the schedules associated with the input commcell entity.
            Client / Agent / Backupset / Subclient

            Returns:
                dict - consists of all schedules for the commcell entity
                    {
                         "schedule1_name": [
                             schedule1_id, {
                                 "subtask1_name": subtask1_id,
                                 "subtask2_name": subtask2_id
                             }
                         ],
                         "schedule2_name": [
                             schedule2_id, {
                                 "subtask1_name": subtask1_id,
                                 "subtask2_name": subtask2_id
                             }
                         ]
                    }

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._SCHEDULES)

        if flag:
            if response.json() and 'taskDetail' in response.json():
                schedules_dict = {}

                for schedule in response.json()['taskDetail']:
                    if 'taskName' in schedule['task'] and schedule['task']['taskName']:
                        schedule_name = schedule['task']['taskName']
                    elif 'description' in schedule['task'] and schedule['task']['description']:
                        schedule_name = schedule['task']['description']
                    else:
                        continue

                    temp_name = str(schedule_name).lower()
                    temp_id = str(schedule['task']['taskId']).lower()

                    subtask_dict = {}

                    for subtask in schedule['subTasks']:
                        if 'subTaskName' in subtask['subTask']:
                            subtask_name = str(subtask['subTask']['subTaskName']).lower()
                        else:
                            continue

                        if 'subTaskId' in subtask['subTask']:
                            subtask_id = str(subtask['subTask']['subTaskId']).lower()
                        else:
                            continue

                        subtask_dict[subtask_name] = subtask_id

                    schedules_dict[temp_name] = [temp_id, subtask_dict]

                return schedules_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_schedule(self, schedule_name):
        """Checks if a schedule exists for the commcell entity with the input schedule name.

            Args:
                schedule_name (str)  --  name of the schedule

            Returns:
                bool - boolean output whether the schedule exists for the commcell entity or not

            Raises:
                SDKException:
                    if type of the schedule name argument is not string
        """
        if not isinstance(schedule_name, str):
            raise SDKException('Schedules', '102')

        return self.schedules and str(schedule_name).lower() in self.schedules
