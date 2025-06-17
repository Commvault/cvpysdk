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

"""Main file for performing schedule policy related operations on the commcell.

This file has all the classes related to Schedule Policy operations.

SchedulePolicies: Class for representing all the Schedule Policies associated to the commcell.

SchedulePolicy: Class for representing Schedule Policy

SchedulePolicies:
    __init__(commcell_object)    --  initialize the SchedulePolicies instance for the commcell

    __str__()                    --  returns all the schedule policies associated with the commcell

    __repr__()                   --  returns a string for instance of the SchedulePolicies class

    _get_policies()              --  gets all the schedule policies of the commcell

    all_schedule_policies()      --  returns the dict of all the schedule policies on commcell

    has_policy(policy_name)      --  checks if a schedule policy exists with the given name

    subtasks_json()              --  gets the subtask in schedule policy JSON

    schedule_json()              --  forms the schedule policy subtask with patterns and options for a schedule

    add()                        --  Adds a schedule policy

    get()                        --  Returns a schedule policy object of the specified schedule policy name

    delete()                     --  deletes the specified schedule policy name

    refresh()                    --  refresh the schedule policies associated with the commcell

    _process_schedule_policy_response -- processes the response received schedule policy creation request

SchedulePolicy:

     __init__(commcell_object)      --  Initialise the Schedule Policy class instance

     _get_schedule_policy_id        --   Gets a schedule policy ID

    policy_type                     --   Gets the policy type of the schedule policy

    _get_schedule_policy_properties -- Gets the properties of this Schedule Policy

    update_associations             --  Updates the schedule policy associations

    all_schedules                   -- returns all the schedules associated to the schedule policy

    _update_pattern                 -- Updates the schedule pattern for the provided schedule id

    get_option                      -- gets the schedule options for the provided option

    _update_option                  -- Updates the option for the provided schedule id

    get_schedule                    -- returns the subtask dict for the provided schedule id or name

    add_schedule                    -- Adds a new schedule to the schedule policy

    modify_schedule                 -- Modifies the schedule with the given schedule json inputs for the given schedule
                                       id or name

    delete_schedule                 -- Deletes the schedule from the schedule policy

    update_app_groups               -- Update the appgroups for the provided schedule policy

    _modify_schedule_policy_properties -- Modifies the task properties of the schedule policy

    _process_schedule_policy_update_response -- processes the response received post update request

    refresh                         -- Refresh the properties of the Schedule Policy

    enable                          -- Enables a schedule policy

    disable                         -- Disables a schedule policy



"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ..exception import SDKException
from .schedule_options import ScheduleOptions
from ..schedules import SchedulePattern

class OperationType:
    """Operation Type for schedule policy associations and appGroups"""
    INCLUDE = 'include'
    EXCLUDE = 'exclude',
    DELETE = 'deleted'

class SchedulePolicies:
    """Class for getting all the schedule policies associated with the commcell."""

    policy_to_subtask_map = {

        'Data Protection': [2, 2], #[subtaskType, OperationType]
        'Auxiliary Copy': [1, 4003]
    }

    policy_types = {
        "Data Protection": 0,
        "Auxiliary Copy": 1,
        "Primary Storage Reports": 2,
        "Backup Copy": 3,
        "SRM Data Collection": 4,
        "Subclient Filter for BackupJob Report": 5,
        "Offline Content Indexing": 6,
        "Install Updates": 7,
        "Network Throttle": 8,
    }

    def __init__(self, commcell_object):
        """Initialize object of the SchedulePolicies class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the SchedulePolicies class
        """
        self._commcell_object = commcell_object
        self._POLICY = self._commcell_object._services['SCHEDULE_POLICY']
        self._CREATE_POLICY = self._commcell_object._services['CREATE_UPDATE_SCHEDULE_POLICY']
        self._policies = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all schedule policies of the commcell.

            Returns:
                str - string of all the schedule policies associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Schedule Policy')

        for index, policy in enumerate(self._policies):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, policy)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the SchedulePolicies class."""
        return "SchedulePolicies class instance for Commcell"

    def _get_policies(self):
        """Gets all the schedule policies associated to the commcell specified by commcell object.

            Returns:
                dict - consists of all schedule policies of the commcell
                    {
                         "schedule_policy1_name": schedule_policy1_id,
                         "schedule_policy2_name": schedule_policy2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._POLICY)

        if flag:
            if response and response.json():
                if response.json() and 'taskDetail' in response.json():
                    policies = response.json()['taskDetail']
                    policies_dict = {}

                    for policy in policies:
                        temp_name = policy['task']['taskName'].lower()
                        temp_id = str(policy['task']['taskId']).lower()
                        policies_dict[temp_name] = temp_id

                    return policies_dict
                else:
                    raise SDKException('Response', '102')
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_schedule_policies(self):
        """Returns the schedule policies on this commcell

            dict - consists of all schedule policies of the commcell
                    {
                         "schedule_policy1_name": schedule_policy1_id,
                         "schedule_policy2_name": schedule_policy2_id
                    }
        """
        return self._policies

    def has_policy(self, policy_name):
        """Checks if a schedule policy exists in the commcell with the input schedule policy name.

            Args:
                policy_name (str)  --  name of the schedule policy

            Returns:
                bool - boolean output whether the schedule policy exists in the commcell or not

            Raises:
                SDKException:
                    if type of the schedule policy name argument is not string
        """
        if not isinstance(policy_name, str):
            raise SDKException('Storage', '101')

        return self._policies and policy_name.lower() in self._policies

    @staticmethod
    def subtasks_json(policy_type):
        """
        gets the subtask in schedule policy JSON
        Args:
            policy_type (str) -- Type of the schedule policy from 'policy_types' dict

        Returns:
            returns schedule policy Subtask
        """

        _backup_subtask = {
            "subTaskType": SchedulePolicies.policy_to_subtask_map[policy_type][0],
            "operationType": SchedulePolicies.policy_to_subtask_map[policy_type][1]
        }

        return _backup_subtask

    @staticmethod
    def schedule_json(policy_type, schedule_dict):
        """
            Returns the schedule json for the given schedule options and pattern

        Args:
            policy_type (str) -- Type of the schedule policy from 'policy_types' dict
            schedule_dict (dict) -- with the below format, check add() module for more documentation on the below dict

                                            {
                                                pattern : {},
                                                options: {}
                                            }

        Returns:
            Returns the schedule json for the given schedule options and pattern

        """
        schedule_options = ScheduleOptions(ScheduleOptions.policy_to_options_map[policy_type]
                                           ).options_json(schedule_dict.get('options', None))
        sub_task = SchedulePolicies.subtasks_json(policy_type)
        sub_task['subTaskName'] = schedule_dict.get('name', '')
        sub_task = {
            "subTaskOperation": 1,
            "subTask": sub_task,
            "options": schedule_options
        }

        freq_type = schedule_dict.get('pattern', {}).get('freq_type', 'daily')

        try:
            schedule_dict["pattern"]["freq_type"] = freq_type
        except KeyError:
            schedule_dict["pattern"] = {"freq_type": freq_type}

        task_json = SchedulePattern().create_schedule({'taskInfo':
                                                           {'subTasks': [sub_task]
                                                            }
                                                       }, schedule_dict.get('pattern'))
        return task_json.get('taskInfo').get('subTasks')[0]


    def add(self, name, policy_type, associations, schedules, agent_type=None):
        """

        Adds a schedule policy

        Args:
            name (str) -- Name of the Schedule Policy
            policy_type (str) -- Type of the schedule policy from 'policy_types' dict
            associations (str) -- List of schedule associations
            [
            {
                "clientName": "scheduleclient1"
            },
            {
                "clientGroupName": "scheduleclient2"
            }
            ]

            schedules (List) -- schedules to be associated to the schedule policy

            [
                {
                    pattern : {}, -- Please refer SchedulePattern.create_schedule in schedules.py for the types of
                                     pattern to be sent

                                     eg: {
                                            "freq_type": 'daily',
                                            "active_start_time": time_in_%H/%S (str),
                                            "repeat_days": days_to_repeat (int)
                                         }

                    options: {} -- Please refer ScheduleOptions.py classes for respective schedule options

                                    eg:  {
                                        "maxNumberOfStreams": 0,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": True,
                                        "totalJobsToProcess": 1000,
                                        "allCopies": True,
                                        "mediaAgent": {
                                            "mediaAgentName": "<ANY MEDIAAGENT>"
                                        }
                                    }
                }
            ]



            agent_type (List) -- Agent Types to be associated to the schedule policy

                      eg:    [
                                {
                                    "appGroupName": "Protected Files"
                                },
                                {
                                    "appGroupName": "Archived Files"
                                }
                            ]

        sample:

                    apptype = [{'appGroupName': 'DB2'}]
                    associations = [{'clientName': 'testclient'}]
                    schedule = [
                        {
                            'name': 'trying',
                            'pattern': {
                                            'freq_type': 'Daily'
                                        }
                        }
                    ]
                    commcellobj.schedule_policies.add('testsch1', 'Data Protection', associations, schedule, apptype)

        Returns: schedule policy object on successful completion

        Raises:

            SDKExceptions on wrong input types and failure to create schedule policy

        """

        if not isinstance(schedules, list):
            raise SDKException('Schedules', '102', 'schedules should be a list')

        sub_tasks = []
        for schedule in schedules:
            sub_tasks.append(self.schedule_json(policy_type, schedule))


        schedule_policy = {
            "taskInfo":
                {
                    "associations": associations,
                    "task":
                        {
                            "description": "", "taskType": 4, "initiatedFrom": 2,
                            "policyType": self.policy_types[policy_type],
                            "taskName": name,
                            "securityAssociations": {},
                            "taskSecurity": {},
                            "alert": {"alertName": ""},
                            "taskFlags": {"isEdgeDrive": False, "disabled": False}
                        },
                    "appGroup":
                        {
                            "appGroups": agent_type if agent_type else [],
                        },
                    "subTasks": sub_tasks

                }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_POLICY, schedule_policy
        )
        output = self._process_schedule_policy_response(flag, response)
        self.refresh()

        if output[0]:
            return self.get(name)

        o_str = 'Failed to update properties of Schedule\nError: "{0}"'
        raise SDKException('Schedules', '102', o_str.format(output[2]))

    def get(self, schedule_policy_name, schedule_policy_id=None):
        """Returns a schedule policy object of the specified schedule policy name.

            Args:
                schedule_policy_name (str)  --  name of the Schedule Policy
                schedule_policy_id (int) -- id of the schedule Policy

            Sample: sch_pol_obj = commcellobj.schedule_policies.get('testschp')

            Returns:
                object - instance of the schedule policy class for the given schedule name

            Raises:
                SDKException:
                    if type of the schedule policy name argument is not string

                    if no schedule policy exists with the given name
        """

        if schedule_policy_name and not isinstance(schedule_policy_name, str):
            raise SDKException('Schedules', '102')

        if schedule_policy_id and not isinstance(schedule_policy_id, int):
            raise SDKException('Schedules', '102')

        schedule_policy_name = schedule_policy_name.lower()
        schedule_policy_id = self.all_schedule_policies.get(schedule_policy_name)
        if self.has_policy(schedule_policy_name):
            return SchedulePolicy(
                self._commcell_object, schedule_policy_name, schedule_policy_id
            )

        raise SDKException(
            'Schedules',
            '102',
            'No Schedule Policy exists with name: {0}'.format(schedule_policy_name))

    def delete(self, schedule_policy_name):
        """deletes the specified schedule policy name.

                    Args:
                        schedule_policy_name (str)  --  name of the Schedule Policy

                    Sample:  commcellobj.schedule_policies.delete('testschp')

                    Raises:
                        SDKException:
                            if type of the schedule policy name argument is not string
                            if no schedule policy exists with the given name
        """

        if schedule_policy_name and not isinstance(schedule_policy_name, str):
            raise SDKException('Schedules', '102')

        schedule_policy_name = schedule_policy_name.lower()
        schedule_policy_id = self.all_schedule_policies.get(schedule_policy_name)

        if schedule_policy_id:
            request_json = {
                "TMMsg_TaskOperationReq":
                    {
                        "opType": 3,
                        "taskEntities":
                            [
                                {
                                    "_type_": 69,
                                    "taskId": schedule_policy_id
                                }
                            ]
                    }
            }

            modify_schedule = self._commcell_object._services['EXECUTE_QCOMMAND']

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', modify_schedule, request_json)

            if flag:
                if response.json():
                    if 'errorCode' in response.json():
                        if response.json()['errorCode'] == 0:
                            self.refresh()
                        else:
                            raise SDKException(
                                'Schedules', '102', response.json()['errorMessage'])
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(
                    response.text)
                exception_message = 'Failed to delete schedule policy\nError: "{0}"'.format(
                    response_string)

                raise SDKException('Schedules', '102', exception_message)
        else:
            raise SDKException(
                'Schedules', '102', 'No schedule policy exists for: {0}'.format(
                    schedule_policy_id)
            )

    def refresh(self):
        """Refresh the Schedule Policies associated with the Commcell."""
        self._policies = self._get_policies()

    def _process_schedule_policy_response(self, flag, response):
        """
        processes the response received post create request
        Args:
        flag: (bool) -- True or false based on response
        response: (dict) response from modify request
        Returns:
            flag: (Bool) -- based on success and failure
            error_code: (int) -- error_code from response
            error_message: (str) -- error_message from the response if any
        """

        if flag:
            if response.json():
                if "taskId" in response.json():
                    task_id = str(response.json()["taskId"])

                    if task_id:
                        return True, "0", ""

                elif "errorCode" in response.json():
                    error_code = str(response.json()['errorCode'])
                    error_message = response.json()['errorMessage']

                    if error_code == "0":
                        return True, "0", ""

                    if error_message:
                        return False, error_code, error_message
                    else:
                        return False, error_code, ""
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

class SchedulePolicy:
    """Class for performing operations for a specific Schedule."""

    def __init__(self, commcell_obj, schedule_policy_name, schedule_policy_id=None):

        """Initialise the Schedule Policy class instance.

            Args:
                class_object (object)     --  instance of Class Object

                schedule_policy_name      (str)     --  name of the Schedule

                schedule_policy_id        (int)     --   task ids of the Schedule



            Returns:
                object - instance of the Schedule Policy class
        """

        self._commcell_object = commcell_obj

        self.schedule_policy_name = schedule_policy_name

        if schedule_policy_id:
            self.schedule_policy_id = schedule_policy_id
        else:
            self.schedule_policy_id = self._get_schedule_policy_id()


        self._SCHEDULE_POLICY = self._commcell_object._services['GET_SCHEDULE_POLICY'] % (
            self.schedule_policy_id)
        self._MODIFY_SCHEDULE_POLICY = self._commcell_object._services['CREATE_UPDATE_SCHEDULE_POLICY']

        self._associations = []
        self._subtasks = []
        self._app_groups = []
        self._task_json = {}
        self._task_name = None
        self._all_schedules = []
        self.refresh()

    def _get_schedule_policy_id(self):
        """
        Gets a schedule ID of the schedule policy
        Returns (int) -- schedule policy ID
        """
        schedule_policies = SchedulePolicies(self._commcell_object)
        return schedule_policies.get(self.schedule_policy_name).schedule_policy_id

    @property
    def policy_type(self):
        """
        Get the policy Type of the schedule policy

        Sample:  sch_pol_obj.policy_type

        Returns (str) -- Type of the schedule policy from 'policy_types' dict

        """
        return (
                list(
                SchedulePolicies.policy_types.keys())[
                list(
                    SchedulePolicies.policy_types.values()).index(self._task_json['policyType'])])


    def _get_schedule_policy_properties(self):
        """Gets the properties of this Schedule Policy.

            Returns:
                dict - dictionary consisting of the properties of this Schedule Policy

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._SCHEDULE_POLICY)

        if flag:
            if response.json() and 'taskInfo' in response.json():
                _task_info = response.json()['taskInfo']

                if 'associations' in _task_info:
                    self._associations = _task_info['associations']

                if 'task' in _task_info:
                    self._task_json = _task_info['task']

                self._app_groups = _task_info['appGroup'].get('appGroups')

                self._subtasks = _task_info['subTasks']

                for subtask in self._subtasks:
                    self._all_schedules.append({
                                                "schedule_name" : subtask["subTask"].get("subTaskName", ''),
                                                "schedule_id": subtask["subTask"]["subTaskId"]
                                                })


            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def update_associations(self, associations, operation_type):
        """
        Updates the schedule policy associations
        Args:
            associations (str) -- List of schedule associations
            [
            {
                "clientName": "scheduleclient1"
            },
            {
                "clientGroupName": "scheduleclient2"
            }
            ]
            operation_type (OperationType) -- Please check OperationType class present in this file

        Sample:
            associations = [{'clientName': 'client2'}]
            sch_pol_obj.update_associations(associations, OperationType.DELETE)

        """

        for app_group in associations:
            app_group["flags"] = {
                                    operation_type: True
                                 }
        self._associations = associations
        self._modify_schedule_policy_properties()

    @property
    def all_schedules(self):
        """
        Gets all the schedules of the schedule policy

        Sample:  sch_pol_obj.all_schedules

        Returns (dict) -- schedules in the below format

            {
                    "schedule_name" : (str),
                    "schedule_id": (int)
            }

        """
        return self._all_schedules


    def _update_pattern(self, schedule_id, pattern_dict):

        """

        Updates the schedule pattern for the provided schedule id (internal function)

        Args:
            schedule_id (int) -- id of the schedule
            pattern_dict (dict) -- Please refer SchedulePattern.create_schedule in schedules.py for the types of
                                     pattern to be sent

                                     eg: {
                                            "freq_type": 'daily',
                                            "active_start_time": time_in_%H/%S (str),
                                            "repeat_days": days_to_repeat (int)
                                         }


        """

        existing_pattern = {}

        for subtask in self._subtasks:
            if subtask["subTask"]["subTaskId"] == schedule_id:

                if 'pattern' in subtask:
                    existing_pattern = subtask['pattern']

                if 'options' in subtask:
                    _options = subtask['options']
                    if 'commonOpts' in _options:
                        if 'automaticSchedulePattern' in _options["commonOpts"]:
                            existing_pattern = _options[
                                "commonOpts"]['automaticSchedulePattern']

                    if 'backupOpts' in _options:
                        if 'dataOpt' in _options['backupOpts']:
                            if isinstance(existing_pattern, dict):
                                _data_opt = _options['backupOpts']['dataOpt']
                                existing_pattern.update(_data_opt)
                break


        task_json = SchedulePattern(existing_pattern).create_schedule({'taskInfo':
                                                                           {'subTasks': self._subtasks
                                                                            }
                                                                       }, pattern_dict, schedule_id)

        self._subtasks = task_json.get('taskInfo').get('subTasks')

    @staticmethod
    def get_option(option_dict, option):
        """
        gets the schedule options for the provided option
        Args:
            option_dict: the complete options dict
            option: option for which the dict has to be fetched

        Returns (dict) -- Option dict for the provided option

        """
        if isinstance(option_dict, dict) and option in option_dict:
            return option_dict[option]
        elif not isinstance(option_dict, dict):
            return None
        else:
            for value in option_dict.values():
                result = SchedulePolicy.get_option(value, option)
                if result is not None:
                    return result

    def _update_option(self, schedule_id, options):
        """
        Updates the option for the provided schedule id (internal)

        Args:
             schedule_id (int) -- id of the schedule
            options (dict) -- Please refer ScheduleOptions.py classes for respective schedule options

                                    eg:  {
                                        "maxNumberOfStreams": 0,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": True,
                                        "totalJobsToProcess": 1000,
                                        "allCopies": True,
                                        "mediaAgent": {
                                            "mediaAgentName": "<ANY MEDIAAGENT>"
                                        }
                                    }

        """

        option_allowed = ScheduleOptions.policy_to_options_map[self.policy_type]
        for subtask in self._subtasks:
            if subtask["subTask"]["subTaskId"] == schedule_id:
                if 'options' in subtask:
                    existing_options = self.get_option(subtask['options'], option_allowed)
                    if not existing_options:
                        raise SDKException('Schedules', '104')

                    subtask['options'] = ScheduleOptions(option_allowed, existing_options).options_json(options)
                    self._subtasks[self._subtasks.index(subtask)] = subtask
                    break

    def get_schedule(self, schedule_id=None, schedule_name=None):
        """
        returns the subtask dict for the provided schedule id or name
        Args:
            schedule_id (int) -- id of the schedule
            schedule_name (str) -- name of the schedule

        Sample:  sch_pol_obj.get_schedule(schedule_id=10)

        Returns (dict) -- subtask dict

        """
        if not schedule_name and not schedule_id:
            raise SDKException(
                'Schedules',
                '102',
                'Either Schedule Name or Schedule Id is needed')

        if schedule_name and not isinstance(schedule_name, str):
            raise SDKException('Schedules', '102')

        if schedule_id and not isinstance(schedule_id, int):
            raise SDKException('Schedules', '102')

        if schedule_name:
            search_dict = ("subTaskName", schedule_name)
        else:
            search_dict = ("subTaskId", schedule_id)

        for sub_task in self._subtasks:
            if search_dict in sub_task["subTask"].items():
                return sub_task

    def add_schedule(self, schedule_dict):
        """
        Adds a new schedule to the schedule policy
        Args:
            schedule_dict (dict) -- {
                    pattern : {}, -- Please refer SchedulePattern.create_schedule in schedules.py for the types of
                                     pattern to be sent

                                     eg: {
                                            "freq_type": 'daily',
                                            "active_start_time": time_in_%H/%S (str),
                                            "repeat_days": days_to_repeat (int)
                                         }

                    options: {} -- Please refer ScheduleOptions.py classes for respective schedule options

                                    eg:  {
                                        "maxNumberOfStreams": 0,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": True,
                                        "totalJobsToProcess": 1000,
                                        "allCopies": True,
                                        "mediaAgent": {
                                            "mediaAgentName": "<ANY MEDIAAGENT>"
                                        }
                                    }
                }

        Sample:

                sch_pol_obj.add_schedule({'pattern':{'freq_type': 'monthly'}})

        """
        sub_task = SchedulePolicies.schedule_json(self.policy_type, schedule_dict)
        sub_task["subTaskOperation"] = 2
        self._subtasks.append(sub_task)
        self._modify_schedule_policy_properties()

    def modify_schedule(self, schedule_json, schedule_id=None, schedule_name=None):
        """
        Modifies the schedule with the given schedule json inputs for the given schedule id or name
        Args:
            schedule_dict (dict) -- {
                    pattern : {}, -- Please refer SchedulePattern.create_schedule in schedules.py for the types of
                                     pattern to be sent

                                     eg: {
                                            "freq_type": 'daily',
                                            "active_start_time": time_in_%H/%S (str),
                                            "repeat_days": days_to_repeat (int)
                                         }

                    options: {} -- Please refer ScheduleOptions.py classes for respective schedule options

                                    eg:  {
                                        "maxNumberOfStreams": 0,
                                        "useMaximumStreams": True,
                                        "useScallableResourceManagement": True,
                                        "totalJobsToProcess": 1000,
                                        "allCopies": True,
                                        "mediaAgent": {
                                            "mediaAgentName": "<ANY MEDIAAGENT>"
                                        }
                                    }
                }
            schedule_id (int) -- id of the schedule
            schedule_name (str) -- name of the schedule

        Sample:
                Change Pattern:
                    sch_pol_obj.change_schedule({'pattern':{'freq_type': 'monthly'}}, schedule_id=77)

                Change Options:
                    sch_pol_obj.change_schedule({'options':{'maxNumberOfStreams': 10}}, schedule_id=77)

        """
        sub_task = self.get_schedule(schedule_id, schedule_name)
        if not sub_task:
            raise SDKException('Schedules', '105')
        if 'pattern' in schedule_json:
            self._update_pattern(sub_task["subTask"]["subTaskId"], schedule_json.get('pattern'))
        if 'options' in schedule_json:
            self._update_option(sub_task["subTask"]["subTaskId"], schedule_json.get('options'))
        self._modify_schedule_policy_properties()

    def delete_schedule(self, schedule_id=None, schedule_name=None):
        """
        Deletes the schedule from the schedule policy
        Args:
            schedule_id (int) -- id of the schedule
            schedule_name (str) -- name of the schedule

        Sample:
            sch_pol_obj.delete_schedule(schedule_name='testsch')

        """
        sub_task = self.get_schedule(schedule_id, schedule_name)
        if not sub_task:
            raise SDKException('Schedules', '105')
        sub_task["subTaskOperation"] = 3
        self._subtasks[self._subtasks.index(sub_task)] = sub_task
        self._modify_schedule_policy_properties()

    def update_app_groups(self, app_groups, operation_type):
        """
        Update the appgroups for the provided schedule policy
        Args:
            app_groups(List) -- Agent Types to be associated to the schedule policy

                      eg:    [
                                {
                                    "appGroupName": "Protected Files"
                                },
                                {
                                    "appGroupName": "Archived Files"
                                }
                            ]
            operation_type (OperationType) -- Please check OperationType class present in this file

        Sample:

            apptype = [{'appGroupName': 'DB2'}]
            sch_pol_obj.update_app_groups(apptype, OperationType.INCLUDE)

        """
        for app_group in app_groups:
            app_group["flags"] = {
                operation_type: True
            }
        self._app_groups = app_groups
        self._modify_schedule_policy_properties()

    def _modify_schedule_policy_properties(self):
        """
         Modifies the task properties of the schedule policy
        Exception:
            if modification of the schedule policy failed

        """
        request_json = {
            'taskInfo':
                {
                    'taskOperation': 1,
                    'associations': self._associations,
                    'task': self._task_json,
                    "appGroup":
                        {
                            "appGroups": self._app_groups if self._app_groups else [],
                        },
                    'subTasks': self._subtasks
                }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._MODIFY_SCHEDULE_POLICY, request_json
        )
        output = self._process_schedule_policy_update_response(flag, response)
        self.refresh()

        if output[0]:
            return

        o_str = 'Failed to update properties of Schedule Policy\nError: "{0}"'
        raise SDKException('Schedules', '102', o_str.format(output[2]))

    def enable(self):
        """Enable a schedule policy.

                    Raises:
                        SDKException:
                            if failed to enable schedule policy

                            if response is empty

                            if response is not success
                """
        enable_request = self._commcell_object._services['ENABLE_SCHEDULE']
        request_text = "taskId={0}".format(self.schedule_policy_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', enable_request, request_text)

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if error_code == "0":
                    return
                else:
                    error_message = 'Failed to enable Schedule Policy'

                    if 'errorMessage' in response.json():
                        error_message = "{0}\nError: {1}".format(error_message, response.json()['errorMessage'])

                    raise SDKException('Schedules', '102', error_message)

            else:
                raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def disable(self):
        """Disable a Schedule Policy.

            Raises:
                SDKException:
                    if failed to disable Schedule Policy

                    if response is empty

                    if response is not success
        """
        disable_request = self._commcell_object._services['DISABLE_SCHEDULE']

        request_text = "taskId={0}".format(self.schedule_policy_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', disable_request, request_text)

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if error_code == "0":
                    return
                else:
                    error_message = 'Failed to disable Schedule Policy'

                    if 'errorMessage' in response.json():
                        error_message = "{0}\nError: {1}".format(error_message, response.json()['errorMessage'])

                    raise SDKException('Schedules', '102', error_message)

            else:
                raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def _process_schedule_policy_update_response(self, flag, response):
        """
        processes the response received post update request
        Args:
        flag: (bool) -- True or false based on response
        response: (dict) response from modify request
        Returns:
            flag: (Bool) -- based on success and failure
            error_code: (int) -- error_code from response
            error_message: (str) -- error_message from the response if any
        """
        task_id = None
        if flag:
            if response.json():
                if "taskId" in response.json():
                    task_id = str(response.json()["taskId"])

                    if task_id:
                        return True, "0", ""

                elif "errorCode" in response.json():
                    error_code = str(response.json()['errorCode'])
                    error_message = response.json()['errorMessage']

                    if error_code == "0":
                        return True, "0", ""

                    if error_message:
                        return False, error_code, error_message
                    else:
                        return False, error_code, ""
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the Schedule Policy."""
        self._get_schedule_policy_properties()
