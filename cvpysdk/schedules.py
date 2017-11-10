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
    
    delete(schedule_name)           -- deletes the given schedule

Schedule: Class for performing operations for a specific Schedule.

Schedule:
    __init__(class_object)                          --  initialise object of the Schedule class

    _get_schedule_id_dict                           -- Gets a schedule ID dict for the schedule

    _get_schedule_properties                        -- get all schedule properties

    _pattern_json(pattern_option_dict)              -- forms the pattern json based on the
                                                                                 dict provided

    _time_converter(_time_string, time_format)      -- converts utc to epoch and vice versa

    schedule_freq_type                              -- gets the schedule frequence type

    one_time                                        -- gets the one time schedule pattern dict

    one_time(pattern_dict)                          -- sets the one time schedule pattern

    daily                                           -- gets the daily schedule pattern

    daily(pattern_dict)                             -- sets the daily schedule pattern

    weekly                                          -- gets the weekly schedule pattern

    weekly(pattern_dict)                            -- sets the weekly schedule pattern

    monthly                                         -- gets the monthly schedule pattern

    active_start_date                               -- gets the start date of schedule pattern

    active_start_date(active_start_date)            -- sets the start date of schedule pattern

    active_start_time                               -- gets the start time of schedule pattern

    active_start_time(active_start_time)            -- sets the start time of schedule pattern

    enable()                                        -- enables the schedule

    disable()                                        -- disables the schedule

    _modify_task_properties                         -- modifies the schedule properties
                                                                            based on the setters

    _process_schedule_update_response               -- processes the response and
                                                                gives the error_code and message


"""

from __future__ import absolute_import
from __future__ import unicode_literals
from datetime import datetime
from past.builtins import basestring

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

        self.class_object = class_object

        self._commcell_object = class_object._commcell_object

        self._repr_str = ""

        if isinstance(class_object, Client):
            self._SCHEDULES = self._commcell_object._services['CLIENT_SCHEDULES'] % (
                class_object.client_id
            )
            self._repr_str = "Client: {0}".format(class_object.client_name)
        elif isinstance(class_object, Agent):
            self._SCHEDULES = self._commcell_object._services['AGENT_SCHEDULES'] % (
                class_object._client_object.client_id,
                class_object.agent_id
            )
            self._repr_str = "Agent: {0}".format(class_object.agent_name)
        elif isinstance(class_object, Backupset):
            self._SCHEDULES = self._commcell_object._services['BACKUPSET_SCHEDULES'] % (
                class_object._agent_object._client_object.client_id,
                class_object._agent_object.agent_id,
                class_object.backupset_id
            )
            self._repr_str = "Backupset: {0}".format(
                class_object.backupset_name)
        elif isinstance(class_object, Subclient):
            self._SCHEDULES = self._commcell_object._services['SUBCLIENT_SCHEDULES'] % (
                class_object._backupset_object._agent_object._client_object.client_id,
                class_object._backupset_object._agent_object.agent_id,
                class_object._backupset_object.backupset_id,
                class_object.subclient_id
            )
            self._repr_str = "Subclient: {0}".format(
                class_object.subclient_name)
        else:
            raise SDKException('Schedules', '101')

        self.schedules = self._get_schedules()

    def __str__(self):
        """Representation string consisting of all schedules of the commcell entity.

            Returns:
                str - string of all the schedules associated with the commcell entity
        """
        if self.schedules:
            representation_string = '{:^5}\t{:^20}\n\n'.format(
                'S. No.', 'Schedule')

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
                         "schedule1_name": {
                                'task_id': task_id,
                                'schedule_id': schedule_id,
                                'description': description
                            }

                         "schedule2_name": {
                                'task_id': task_id,
                                'schedule_id': schedule_id,
                                'description': description
                            }
                    }

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._SCHEDULES)

        if flag:
            if response.json() and 'taskDetail' in response.json():

                for schedule in response.json()['taskDetail']:
                    task_id = schedule['task']['taskId']
                    subtask_dict = {}
                    description = ''
                    if 'subTasks' in schedule:
                        for subtask in schedule['subTasks']:
                            schedule_id = subtask['subTask']['subTaskId']
                            if 'description' in subtask['subTask']:
                                description = subtask['pattern']['description'].lower(
                                )
                            if 'subTaskName' in subtask['subTask']:
                                subtask_name = subtask['subTask']['subTaskName'].lower(
                                )
                            elif description:
                                subtask_name = description
                            else:
                                subtask_name = str(schedule_id)

                            subtask_dict[subtask_name] = {
                                'task_id': task_id,
                                'schedule_id': schedule_id,
                                'description': description
                            }

                return subtask_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
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
        if not isinstance(schedule_name, basestring):
            raise SDKException('Schedules', '102')

        return self.schedules and schedule_name.lower() in self.schedules

    def get(self, schedule_name):
        """Returns a schedule object of the specified schedule name.

            Args:
                schedule_name (str)  --  name of the Schedule

            Returns:
                object - instance of the schedule class for the given schedule name

            Raises:
                SDKException:
                    if type of the schedule name argument is not string

                    if no schedule exists with the given name
        """
        if not isinstance(schedule_name, basestring):
            raise SDKException('Schedules', '102')
        else:
            schedule_name = schedule_name.lower()

            if self.has_schedule(schedule_name):
                return Schedule(
                    self.class_object, schedule_name,
                    self.schedules[schedule_name]['task_id']

                )

            raise SDKException(
                'Schedules', '102', 'No Schedule exists with name: {0}'.format(schedule_name))

    def delete(self, schedule_name):
        """deletes the specified schedule name.

                    Args:
                        schedule_name (str)  --  name of the Schedule

                    Raises:
                        SDKException:
                            if type of the schedule name argument is not string
                            if no schedule exists with the given name
        """
        if not isinstance(schedule_name, basestring):
            raise SDKException('Schedules', '102')
        else:
            schedule_name = schedule_name.lower()
            if self.has_schedule(schedule_name):
                request_json = {
                    "TMMsg_TaskOperationReq":
                        {
                            "opType": 3,
                            "taskEntities":
                                [
                                    {
                                        "_type_": 69,
                                        "taskId": self.schedules[schedule_name]['task_id']
                                    }
                                ]
                        }
                }

                modify_schedule = self._commcell_object._services['EXECUTE_QCOMMAND']

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'POST', modify_schedule, request_json
                )

                if flag:
                    if response.json():
                        if 'errorCode' in response.json():
                            if response.json()['errorCode'] == 0:
                                self.schedules = self._get_schedules()
                            else:
                                raise SDKException(
                                    'Schedules', '102', response.json()['errorMessage'])
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(
                        response.text)
                    exception_message = 'Failed to delete schedule\nError: "{0}"'.format(
                        response_string
                    )

                    raise SDKException('Schedules', '102', exception_message)
            else:
                raise SDKException(
                    'Schedules', '102', 'No schedule exists with name: {0}'.format(
                        schedule_name)
                )


class Schedule(object):
    """Class for performing operations for a specific Schedule."""

    def __init__(self, class_object, schedule_name, schedule_id=None):
        """Initialise the Schedule class instance.

            Args:
                class_object (object)  --  instance of the client/agent/backupset/subclient class

                schedule_name      (str)     --  name of the Schedule

                schedule_id        (int)     --   task ids of the Schedule



            Returns:
                object - instance of the Schedule class
        """
        self.class_object = class_object

        self._commcell_object = class_object._commcell_object
        self.schedule_name = schedule_name.lower()

        if schedule_id:
            self.schedule_id = schedule_id
        else:
            self.schedule_id = self._get_schedule_id()

        self._SCHEDULE = self._commcell_object._services['SCHEDULE'] % (
            self.schedule_id)
        self._MODIFYSCHEDULE = self._commcell_object._services['EXECUTE_QCOMMAND']

        self._week_of_month = {
            '1': 'First',
            '2': 'Second',
            '3': 'Third',
            '4': 'Fourth',
            '5': 'Last'
        }

        self._days_to_run = {
            1: 'sunday',
            2: 'monday',
            4: 'tuesday',
            8: 'wednesday',
            16: 'thursday',
            32: 'friday',
            64: 'saturday'
        }

        self._freq_type = {
            1: 'One_Time',
            2: 'On_Demand',
            4: 'Daily',
            8: 'Weekly',
            16: 'Monthly',
            32: 'Monthly_Relative',
            64: 'Yearly',
            128: 'Yearly_Relative',
        }

        self.task_operation_type = {
            1: 'ALL_BACKUP_JOBS',
            2: 'BACKUP',
            1001: ' RESTORE',
            2000: 'ADMIN',
            2001: 'WORK_FLOW',
            4002: 'DRBACKUP',
            4003: 'AUX_COPY',
            4004: 'REPORT',
            4018: 'DATA_AGING',
            4019: 'DOWNLOAD_UPDATES',
            4020: 'INSTALL_UPDATES'
        }

        self._new_pattern = {}
        self._criteria = {}
        self._pattern = {}
        self._task_options = {}
        self._associations_json = {}
        self._description = None
        self._alert_type = None

        self._get_schedule_properties()

    def _get_schedule_id(self):
        """
        Gets a schedule ID dict for the schedule
        :return:
            int - schedule ID

        """
        schedules = Schedules(self.class_object)
        return schedules.get(self.schedule_name).schedule_id

    def _get_schedule_properties(self):
        """Gets the properties of this Schedule.

            Returns:
                dict - dictionary consisting of the properties of this Schedule

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object.\
            _cvpysdk_object.make_request('GET', self._SCHEDULE)

        if flag:
            if response.json() and 'taskInfo' in response.json():
                _task_info = response.json()['taskInfo']

                if 'associations' in _task_info:
                    self._associations_json = _task_info['associations']

                if 'task' in _task_info:
                    self._task_json = _task_info['task']

                for subtask in _task_info['subTasks']:
                    self._sub_task_json = subtask['subTask']
                    if 'operationType' in subtask['subTask']:
                        self.operation_type = subtask['subTask']['operationType']
                    else:
                        continue

                    if 'pattern' in subtask:
                        self._pattern = subtask['pattern']
                    else:
                        continue

                    if 'options' in subtask:
                        self._task_options = subtask['options']

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _pattern_json(self, pattern_option_dict):
        """
        forms a pattern json and set the class variable
        :param pattern_option_dict: dictionary with the parameters needed for
                                                            forming the corresponding pattern
                                        {'freq_type',
                                        'active_start_date',
                                        'active_start_time',
                                        'freq_recurrence_factor',
                                        'freq_interval'}
        """
        if ('freq_type' not in pattern_option_dict) or (
                pattern_option_dict['freq_type'] == self._pattern['freq_type']):
            for key, value in pattern_option_dict.items():
                if key == 'active_start_date':
                    self._pattern['active_start_date'] = self._time_converter(
                        pattern_option_dict['active_start_date'] + ' 12:00', '%m/%d/%Y %H:%M')
                elif key == 'active_start_time':
                    self._pattern['active_start_time'] = self._time_converter(
                        '1/1/1970 ' + pattern_option_dict['active_start_time'], '%m/%d/%Y %H:%M')
                else:
                    self._pattern[pattern_option_dict[key]] = value

        else:
            if pattern_option_dict['freq_type']=='One_Time':
                default_start_time = str(datetime.utcnow().strftime('%H:%M'))

            else:
                default_start_time = '09:00'

            self._new_pattern = {
                'freq_type': pattern_option_dict['freq_type'],
                'active_start_date': self._time_converter(
                    pattern_option_dict.get('active_start_date', str(
                        datetime.utcnow().strftime('%m/%d/%Y'))) + ' 00:00',
                    '%m/%d/%Y %H:%M'),
                'active_start_time': self._time_converter(
                    '1/1/1970 ' +
                    pattern_option_dict.get('active_start_time', default_start_time),
                    '%m/%d/%Y %H:%M'),
                'freq_recurrence_factor': pattern_option_dict.get('freq_recurrence_factor', 0),
                'freq_interval': pattern_option_dict.get('freq_interval', 0)
            }

    @staticmethod
    def _time_converter(_time, time_format, utc_to_epoch=True):
        """
        converts a time string to epoch time based on the time format provided
        param :
            _time: UTC time (str) or EPOCH time (int)
            time_format      : format of the time you need process (str)

        Exception:
            if time format is wrong

        """
        try:
            if utc_to_epoch:
                date_time = datetime.strptime(_time, time_format)
                return int((date_time - datetime.utcfromtimestamp(0)).total_seconds())
            else:
                utc_time = datetime.utcfromtimestamp(_time)
                return utc_time.strftime(time_format)

        except ValueError:
            raise SDKException('Schedules', '102',
                               "Incorrect data format, should be {0}".format(time_format))

    @property
    def schedule_freq_type(self):
        """
        get the schedule frequency type
        :return: returns the schedule frequency type (str)
        """
        return self._freq_type[self._pattern['freq_type']]

    @property
    def one_time(self):
        """
        gets the one time schedule pattern
        :return: return a dict with the schedule pattern
                {
                     "active_start_date": date_in_%m/%d/%y (str),
                     "active_start_time": time_in_%h:%m (str)
                }

                False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'One_Time':
            return {
                'active_start_date': self._time_converter(
                    self._pattern['active_start_date'],
                    '%m/%d/%Y', False),
                'active_start_time': self._time_converter(
                    self._pattern['active_start_time'],
                    '%H:%M', False)
            }
        else:
            return False

    @one_time.setter
    def one_time(self, pattern_dict):
        """
        sets the pattern type as one time with the parameters provided
        :param pattern_dict: (dict) with the schedule pattern
                {
                                 "active_start_date": date_in_%m/%d/%y (str),
                                 "active_start_time": time_in_%h:%m (str)
                }
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 1
        self._pattern_json(pattern_dict)
        self._modify_task_properties()

    @property
    def daily(self):
        """
            gets the daily schedule
            :return: return a dict with the schedule pattern
                    {
                                     "active_start_time": time_in_%H/%S (str),
                                     "repeat_days": days_to_repeat (int)
                    }
            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Daily':
            return {'active_start_time':
                    self._time_converter(self._pattern['active_start_time'],
                                         '%H:%M', False),
                    'repeat_days': self._pattern['freq_recurrence_factor']
                   }
        else:
            return False

    @daily.setter
    def daily(self, pattern_dict):
        """
                sets the pattern type as daily with the parameters provided
                :param pattern_dict: (dict) with the schedule pattern
                  {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_days": days_to_repeat (int)
                  }
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}

        pattern_dict['freq_type'] = 4
        pattern_dict['freq_recurrence_factor'] = pattern_dict.get(
            'repeat_days', 1)
        self._pattern_json(pattern_dict)
        self._modify_task_properties()

    @property
    def weekly(self):
        """
        gets the weekly schedule
        :return: return a dict with the schedule pattern
                {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_weeks": weeks_to_repeat (int)
                         "weekdays": list of weekdays ['Monday','Tuesday']
                }
        False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Weekly':
            _freq = self._pattern['freq_interval']
            return {'active_start_time':
                    self._time_converter(self._pattern['active_start_time'],
                                         '%H:%M', False),
                    'repeat_weeks': self._pattern['freq_recurrence_factor'],
                    'weekdays': [
                        self._days_to_run[x]
                        for x in list(self._days_to_run.keys()) if _freq & x > 0]}
        else:
            return False

    @weekly.setter
    def weekly(self, pattern_dict):
        """
        sets the pattern type as weekly with the parameters provided
        :param pattern_dict: (dict) with the schedule pattern
                        {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_weeks": weeks_to_repeat (int)
                         "weekdays": list of weekdays ['Monday','Tuesday']
                        }
        """
        try:
            if isinstance(pattern_dict, bool):
                pattern_dict = {}
            pattern_dict['freq_type'] = 8
            # encoding
            if 'weekdays' in pattern_dict:
                _freq_interval_list = pattern_dict['weekdays']
            else:
                o_str = 'Weekdays need to be specified'
                raise SDKException('Schedules', '102', o_str)
            _freq_interval = 0
            for weekday in _freq_interval_list:
                _freq_interval += (list(self._days_to_run.keys())
                                   [list(self._days_to_run.values()).index(weekday.lower())])
            pattern_dict['freq_interval'] = _freq_interval
            pattern_dict['freq_recurrence_factor'] = pattern_dict.get(
                'repeat_weeks', 1)

            self._pattern_json(pattern_dict)
            self._modify_task_properties()

        except ValueError:
            raise SDKException('Schedules', '102',
                               "Incorrect weekday specified")



    @property
    def monthly(self):
        """
        gets the monthly schedule
                :return: return a dict with the schedule pattern
                        {
                                 "active_start_time": time_in_%H/%S (str),
                                 "repeat_months": weeks_to_repeat (int)
                                 "onDay": Day to run schedule (int)
                        }
                False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Monthly':
            return {'active_start_time':
                    self._time_converter(self._pattern['active_start_time'],
                                         '%H:%M', False),
                    'repeat_months': self._pattern['freq_recurrence_factor'],
                    'onDay': self._pattern['freq_interval']
                   }
        else:
            return False

    @monthly.setter
    def monthly(self, pattern_dict):
        """
        sets the pattern type as monthly with the parameters provided
        :param pattern_dict: (dict) with the schedule pattern
                        {
                                 "active_start_time": time_in_%H/%S (str),
                                 "repeat_months": weeks_to_repeat (int)
                                 "onDay": Day to run schedule (int)
                        }
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_recurrence_factor'] = pattern_dict.get(
            'repeat_months', 1)
        pattern_dict['freq_interval'] = pattern_dict.get('onDay', 10)
        pattern_dict['freq_type'] = 16
        self._pattern_json(pattern_dict)
        self._modify_task_properties()

    @property
    def active_start_date(self):
        """
        gets the start date of the schedule
        :return: date in %m/%d/%Y (str)
        """
        return self._time_converter(self._pattern['active_start_date'],
                                    '%m/%d/%Y', False)

    @active_start_date.setter
    def active_start_date(self, active_start_date):
        """
        sets the start date of the schedule
        :param active_start_date: date in %m/%d/%Y (str)
        :return:
        """
        self._pattern_json({'active_start_date': active_start_date})
        self._modify_task_properties()

    @property
    def active_start_time(self):
        """
                gets the start time of the schedule
                :return: time in %H/%S (str)
        """
        return self._time_converter(self._pattern['active_start_time'],
                                    '%H:%M', False)

    @active_start_time.setter
    def active_start_time(self, active_start_time):
        """
        sets the start time of the schedule
        :param active_start_time: time in %H/%S (str)
        :return:
        """
        self._pattern_json({'active_start_time': active_start_time})
        self._modify_task_properties()

    def _modify_task_properties(self):
        """
        modifies the task properties of the schedule
        Exception:
            if time format is wrong
        """
        request_json = {
            'TMMsg_ModifyTaskReq':
                {
                    'taskInfo':
                        {
                            'associations': self._associations_json,
                            'task': self._task_json,
                            'subTasks':
                            [
                                {
                                    'subTask': self._sub_task_json,
                                    'pattern': self._pattern
                                    if not self._new_pattern
                                    else self._new_pattern,
                                    'options': self._task_options

                                }
                            ]
                        }
                }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._MODIFYSCHEDULE, request_json
        )
        output = self._process_schedule_update_response(flag, response)

        if output[0]:
            return
        else:
            o_str = 'Failed to update properties of Schedule\nError: "{0}"'
            raise SDKException('Schedules', '102', o_str.format(output[2]))

    def enable(self):
        """Enable a schedule.

                    Raises:
                        SDKException:
                            if failed to enable schedule

                            if response is empty

                            if response is not success
                """
        enable_request = self._commcell_object._services['ENABLE_SCHEDULE']
        request_text = "taskId={0}".format(self.schedule_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', enable_request, request_text)

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if error_code == "0":
                    return
                else:
                    error_message = ""

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']

                    if error_message:
                        raise SDKException(
                            'Schedules', '102', 'Failed to enable Schedule\nError: "{0}"'.format(
                                error_message
                            )
                        )
                    else:
                        raise SDKException(
                            'Schedules', '102', "Failed to enable Schedule")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def disable(self):
        """Disable a Schedule.

            Raises:
                SDKException:
                    if failed to disable Schedule

                    if response is empty

                    if response is not success
        """
        disable_request = self._commcell_object._services['DISABLE_SCHEDULE']

        request_text = "taskId={0}".format(self.schedule_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', disable_request, request_text)

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if error_code == "0":
                    return
                else:
                    error_message = ""

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']

                    if error_message:
                        raise SDKException(
                            'Schedules', '102', 'Failed to disable Schedule\nError: "{0}"'.format(
                                error_message
                            )
                        )
                    else:
                        raise SDKException(
                            'Schedules', '102', "Failed to disable Schedule")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _process_schedule_update_response(self, flag, response):
        """
        processes the response received post update request
        :param flag: True or false based on response (bool)
        :param response: response from modify request (dict)
        :return:
            flag: Bool based on success and failure
            error_code: error_code from response (int)
            error_message: error_message from the response if any (str)
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
