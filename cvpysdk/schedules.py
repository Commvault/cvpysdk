# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#class Schedules
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

"""Main file for performing schedule related operations for client/agent/backupset/subclient.

SchedulePattern: Class for creating the necessary pattern for a schedule creation/modification

SchedulePattern:
    __init__(class_object)                          --  initialise object of the SchedulePattern
                                                        class

    _time_converter(_time_string, time_format)      -- converts utc to epoch and vice versa

    _pattern_json(pattern_option_dict)              -- forms the pattern json based on the
                                                                                 dict provided
    _one_time(pattern_dict)                         -- sets the one time schedule pattern

    _daily(pattern_dict)                            -- sets the daily schedule pattern

    _weekly(pattern_dict)                           -- sets the weekly schedule pattern

    _monthly(pattern_dict)                          -- sets the monthly schedule pattern

    _monthly_relative(pattern_dict)                 -- set the monthly_relative schedule pattern

    _yearly(pattern_dict)                           -- sets the yearly schedule pattern

    _yearly_relative(pattern_dict)                  -- sets the yearly_relative schedule pattern

    _continuous(pattern_dict)                       -- sets the continuous schedule pattern

    _automatic(pattern_dict)                        -- sets the automatic schedule pattern

    _after_job_completes(pattern_dict)              -- sets the after job completes schedule pattern

    create_schedule_pattern(pattern_dict)           -- creates a schedule pattern for the user
                    given pattern

    create_schedule(task_req,pattern_dict)          -- creates a scheduling request from the
                                                                            pattern provided


Schedules: Initializes instance of all schedules for a commcell entity.

Schedules:
    __init__(class_object)          --  initialise object of the Schedules class

    __str__()                       --  string of all schedules associated with the commcell entity

    __repr__()                      --  returns the string for the instance of the Schedules class

    _get_sch_id_from_task_id()      --  gets the schedule id from the provided task id

    _get_schedule_id()              --  gets the schedule if with the provided inputs

    _get_schedules()                --  gets all the schedules associated with the commcell entity

    has_schedule(schedule_name)     --  checks if schedule exists for the comcell entity or not

    delete(schedule_name)           --  deletes the given schedule

    refresh()                       --  refresh the schedules associated with the commcell entity


Schedule: Class for performing operations for a specific Schedule.

Schedule:
    __init__(class_object)                          --  initialise object of the Schedule class

    _get_schedule_properties                        -- get all schedule properties

    is_disabled                                     -- Get the schedule status whether its disabled

    schedule_freq_type                              -- gets the schedule frequence type

    name                                            -- gets the name of the schedule

    name(new_name)                                  -- sets the name of the schedule

    one_time                                        -- gets the one time schedule pattern dict

    one_time(pattern_dict)                          -- sets the one time schedule pattern

    daily                                           -- gets the daily schedule pattern

    daily(pattern_dict)                             -- sets the daily schedule pattern

    weekly                                          -- gets the weekly schedule pattern

    weekly(pattern_dict)                            -- sets the weekly schedule pattern

    monthly                                         -- gets the monthly schedule pattern

    monthly(pattern_dict)                           -- gets the monthly schedule pattern

    monthly_relative                               -- gets the monthly_relative schedule pattern

    monthly_relative(pattern_dict)                 -- set the monthly_relative schedule pattern

    yearly                                         -- gets the yearly schedule pattern

    yearly(pattern_dict)                           -- sets the yearly schedule pattern

    yearly_relative                                -- gets the yearly_relative schedule pattern

    yearly_relative(pattern_dict)                  -- sets the yearly_relative schedule pattern

    continuous                                     -- gets the continuous schedule pattern

    continuous(pattern_dict)                       -- sets the continuous schedule pattern

    automatic                                      -- gets the automatic schedule pattern

    automatic(pattern_dict)                        -- sets the automatic schedule pattern

    active_start_date                               -- gets the start date of schedule pattern

    active_start_date(active_start_date)            -- sets the start date of schedule pattern

    active_start_time                               -- gets the start time of schedule pattern

    active_start_time(active_start_time)            -- sets the start time of schedule pattern

    enable()                                        -- enables the schedule

    disable()                                        -- disables the schedule

    run_now()                                       -- Triggers the schedule immediately

    _modify_task_properties                         -- modifies the schedule properties
                                                                            based on the setters

    _process_schedule_update_response               -- processes the response and
                                                                gives the error_code and message

    refresh()                                       -- refresh the properties of the schedule

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from typing import Optional, Dict, Union, List, Tuple, Any, TYPE_CHECKING
from datetime import datetime
import calendar
from .exception import SDKException

if TYPE_CHECKING:
    from .commcell import Commcell
    from .client import Client
    from .agent import Agent
    from .backupset import Backupset
    from .subclient import Subclient
    from .instance import Instance
    from .activateapps.inventory_manager import Inventory
    from .activateapps.file_storage_optimization import FsoServer
    from .activateapps.sensitive_data_governance import Project

class OperationType:
    """ Operation Types supported to get schedules of particular optype"""
    REPORTS = 'Reports'
    DATA_AGING = 'DATA_AGING'

class SchedulePattern:
    """Class for getting the schedule pattern

    Attributes:
        _days_to_run (dict): Mapping of integer values to day names for weekly schedules.
        _relative_weekday (dict): Mapping of integer values to relative weekday names for monthly relative schedules.
        _relative_day (dict): Mapping of integer values to relative day names for monthly relative schedules.
    Usage:
        pattern = SchedulePattern()
    """

    _days_to_run: Dict[int, str] = {
        2: 'monday',
        4: 'tuesday',
        8: 'wednesday',
        16: 'thursday',
        32: 'friday',
        64: 'saturday',
        1: 'sunday',
    }

    _relative_weekday: Dict[int, str] = {
        1: 'sunday',
        2: 'monday',
        3: 'tuesday',
        4: 'wednesday',
        5: 'thursday',
        6: 'friday',
        7: 'saturday',
        8: 'days',
        9: 'weekday',
        10: 'weekend_day'
    }

    _relative_day: Dict[int, str] = {
        1: 'first',
        2: 'second',
        3: 'third',
        4: 'fourth',
        5: 'last'
    }

    def __init__(self, schedule_pattern: Dict[str, Union[str, int, dict, list, None]] = None) -> None:
        """initialise object of the SchedulePattern class

        Args:
            schedule_pattern (dict, optional): Initial schedule pattern. Defaults to None.
        Usage:
            pattern = SchedulePattern({'freq_type': 'Daily'})
        """
        if not schedule_pattern:
            self._pattern: Dict[str, Union[str, int, dict, list, None]] = {'freq_type': 'Init'}
        else:
            self._pattern: Dict[str, Union[str, int, dict, list, None]] = schedule_pattern

    @staticmethod
    def _time_converter(_time: Union[str, int], time_format: str, utc_to_epoch: bool = True) -> int:
        """
        converts a time string to epoch time based on the time format provided
        Args:
            _time (str/int): UTC time or EPOCH time
            time_format (str): format of the time you need process

        Raises:
            SDKException: if time format is wrong

        Returns:
            int: Epoch time if utc_to_epoch is True, otherwise a formatted time string.

        Usage:
            epoch_time = SchedulePattern._time_converter("10/10/2024 10:00", "%m/%d/%Y %H:%M")
            formatted_time = SchedulePattern._time_converter(1665427200, "%m/%d/%Y %H:%M", utc_to_epoch=False)
        """
        try:

            if utc_to_epoch:
                date_time = datetime.strptime(_time, time_format)
                return int(
                    (date_time - datetime.utcfromtimestamp(0)).total_seconds())

            utc_time = datetime.utcfromtimestamp(_time)
            return utc_time.strftime(time_format)

        except ValueError:
            raise SDKException(
                'Schedules',
                '102',
                "Incorrect data format, should be {0}".format(time_format))

    def _pattern_json(self, pattern_option_dict: Dict[str, Union[str, int, dict, list, None]]) -> None:
        """
        forms a pattern json and set the class variable
        Args:
             pattern_option_dict (dict): dictionary with the parameters needed for
                                                            forming the corresponding pattern
                                            {'freq_type',
                                            'active_start_date',
                                            'active_start_time',
                                            'freq_recurrence_factor',
                                            'freq_interval'}
        Usage:
            pattern = SchedulePattern()
            pattern._pattern_json({'freq_type': 'Daily', 'active_start_date': '10/26/2023', 'active_start_time': '09:00'})
        """

        if ('freq_type' not in pattern_option_dict) or (
                pattern_option_dict['freq_type'] == self._pattern['freq_type']):
            for key, value in pattern_option_dict.items():
                if key in ('active_start_date', 'active_end_date'):
                    self._pattern[key] = self._time_converter(
                        pattern_option_dict[key] + ' 00:00', '%m/%d/%Y %H:%M')
                elif key in ('active_start_time', 'active_end_time'):
                    self._pattern[key] = self._time_converter(
                        '1/1/1970 ' + pattern_option_dict[key], '%m/%d/%Y %H:%M')
                else:
                    self._pattern[key] = value

        else:

            if pattern_option_dict['freq_type'] == 'One_Time':
                default_start_time = str(datetime.now().strftime('%H:%M'))

            else:
                default_start_time = '09:00'

            _active_start_date = pattern_option_dict.get(
                'active_start_date', str(datetime.now().strftime('%m/%d/%Y')))
            _active_start_time = pattern_option_dict.get(
                'active_start_time', default_start_time)

            self._pattern = {
                'freq_type': pattern_option_dict['freq_type'],
                'active_start_date': self._time_converter(
                    _active_start_date + ' 00:00',
                    '%m/%d/%Y %H:%M'),
                'active_start_time': self._time_converter(
                    '1/1/1970 ' + _active_start_time,
                    '%m/%d/%Y %H:%M'),
                'freq_recurrence_factor': pattern_option_dict.get(
                    'freq_recurrence_factor',
                    0),
                'freq_interval': pattern_option_dict.get(
                    'freq_interval',
                    0),
                'freq_relative_interval': pattern_option_dict.get(
                    'freq_relative_interval',
                    0),
                'timeZone': {
                    'TimeZoneName': pattern_option_dict.get(
                        'time_zone',
                        '')}}

            if "active_end_date" in pattern_option_dict:
                self._pattern["active_end_date"] = self._time_converter(
                    pattern_option_dict["active_end_date"] + ' 00:00', '%m/%d/%Y %H:%M')

        if "exception_dates" in pattern_option_dict:
            self._pattern["repeatPattern"] = [{"exception": True,
                                               "onDayNumber": self.exception_dates(
                                                   pattern_option_dict["exception_dates"])}
                                              ]

        if "end_after" in pattern_option_dict:
            self._pattern["active_end_occurence"] = pattern_option_dict["end_after"]

        if "repeat_every" in pattern_option_dict:
            self._pattern.update(self._repeat_pattern(pattern_option_dict))

    @staticmethod
    def _repeat_pattern(pattern_dict: Dict[str, str]) -> Dict[str, Union[int, None]]:
        """
        Forms repeat pattern json based on the pattern dict provided
        Args:
            pattern_dict (dict): Dictionary containing repeat_every and repeat_end parameters
                                    {
                                    "repeat_every": "08:00",
                                    "repeat_end": "23:00"
                                    }
        Returns:
                Dict with subdayinterval and endtime information to plug into the pattern json
        Usage:
            repeat_info = SchedulePattern._repeat_pattern({"repeat_every": "08:00", "repeat_end": "23:00"})
        """
        _repeat_time = datetime.strptime(
            pattern_dict.get(
                "repeat_every", "08:00"), "%H:%M")
        _freq_subday = (_repeat_time.hour * 3600 + _repeat_time.minute * 60)
        return {'freq_subday_interval': _freq_subday,
                'active_end_time': SchedulePattern._time_converter(
                    '1/1/1970 ' + pattern_dict["repeat_end"], '%m/%d/%Y %H:%M')
                }

    def _one_time(self, pattern_dict: Dict[str, str]) -> None:
        """
        sets the pattern type as one time with the parameters provided,
        send only required keys to change only those values
        Args:
             pattern_dict (dict): Dictonary with the schedule pattern
                {
                                 "active_start_date": date_in_%m/%d/%y (str),
                                 "active_start_time": time_in_%h:%m (str)
                }
        Usage:
            pattern = SchedulePattern()
            pattern._one_time({"active_start_date": "10/27/2023", "active_start_time": "10:00"})
        """
        pattern_dict['freq_type'] = 1
        self._pattern_json(pattern_dict)

    def _daily(self, pattern_dict: Dict[str, Union[str, int]]) -> None:
        """
                sets the pattern type as daily with the parameters provided
                send only required keys to change only those values
                Args:
                     pattern_dict (dict): Dictionary with the schedule pattern
                  {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_days": days_to_repeat (int)
                  }
        Usage:
            pattern = SchedulePattern()
            pattern._daily({"active_start_time": "09:00", "repeat_days": 2})
        """
        _repeat_days = 1
        if self._pattern['freq_type'] == 4:
            _repeat_days = self._pattern['freq_recurrence_factor']

        _freq_recurrence_factor = pattern_dict.get('repeat_days', _repeat_days)

        pattern_dict['freq_type'] = 4
        pattern_dict['freq_recurrence_factor'] = 1 if not isinstance(
            _freq_recurrence_factor, int) else _freq_recurrence_factor
        self._pattern_json(pattern_dict)

    def _weekly(self, pattern_dict: Dict[str, Union[str, int, List[str]]]) -> None:
        """
        sets the pattern type as weekly with the parameters provided
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                        {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_weeks": weeks_to_repeat (int)
                         "weekdays": list of weekdays ['Monday','Tuesday']
                        }
        Raises:
            SDKException: If incorrect weekday is specified or weekdays are not specified.
        Usage:
            pattern = SchedulePattern()
            pattern._weekly({"active_start_time": "10:00", "repeat_weeks": 1, "weekdays": ["Monday", "Tuesday"]})
        """
        try:
            _repeat_weeks = 1
            _freq_interval = 0
            if self._pattern['freq_type'] == 8:
                _repeat_weeks = self._pattern['freq_recurrence_factor']
                _freq_interval = self._pattern['freq_interval']

            pattern_dict['freq_type'] = 8
            # encoding
            if 'weekdays' in pattern_dict:
                _freq_interval_list = pattern_dict['weekdays']
                for weekday in _freq_interval_list:
                    _freq_interval += (
                        list(
                            self._days_to_run.keys())[
                            list(
                                self._days_to_run.values()).index(
                                weekday.lower())])
            elif _freq_interval == 0:
                o_str = 'Weekdays need to be specified'
                raise SDKException('Schedules', '102', o_str)

            _freq_recurrence_factor = pattern_dict.get(
                '_repeat_weeks', _repeat_weeks)

            pattern_dict['freq_interval'] = _freq_interval
            pattern_dict['freq_recurrence_factor'] = 1 if not isinstance(
                _freq_recurrence_factor, int) else _freq_recurrence_factor

            self._pattern_json(pattern_dict)

        except ValueError:
            raise SDKException('Schedules', '102',
                               "Incorrect weekday specified")

    def _monthly(self, pattern_dict: Dict[str, Union[str, int]]) -> None:
        """
        sets the pattern type as monthly with the parameters provided
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                        {
                                 "active_start_time": time_in_%H/%S (str),
                                 "repeat_months": months_to_repeat (int)
                                 "on_day": Day to run schedule (int)
                        }
        Usage:
            pattern = SchedulePattern()
            pattern._monthly({"active_start_time": "10:00", "repeat_months": 1, "on_day": 15})
        """
        _repeat_months = 1
        _on_day = 10
        if self._pattern['freq_type'] == 16:
            _repeat_months = self._pattern['freq_recurrence_factor']
            _on_day = self._pattern['freq_interval']

        _freq_recurrence_factor = pattern_dict.get(
            'repeat_months', _repeat_months)
        _freq_interval = pattern_dict.get('on_day', _on_day)

        pattern_dict['freq_recurrence_factor'] = 1 if not isinstance(
            _freq_recurrence_factor, int) else _freq_recurrence_factor
        pattern_dict['freq_interval'] = 1 if not isinstance(
            _freq_interval, int) else _freq_interval
        pattern_dict['freq_type'] = 16
        self._pattern_json(pattern_dict)

    def _monthly_relative(self, pattern_dict: Dict[str, str]) -> None:
        """
        sets the pattern type as monthly_relative with the parameters provided
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                        {
                                 "active_start_time": time_in_%H/%S (str),
                                 "relative_time": relative day of the schedule (str) 'first',
                                                                                        'second',..
                                 "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                                 "repeat_months": months_to_repeat
                        }
        Raises:
            SDKException: If there is a ValueError.
        Usage:
            pattern = SchedulePattern()
            pattern._monthly_relative({"active_start_time": "10:00", "relative_time": "first", "relative_weekday": "monday", "repeat_months": 1})
        """
        _freq_recurrence_factor = 1
        _freq_interval = 1
        _freq_relative_interval = 1

        try:

            if self._pattern['freq_type'] == 32:
                _freq_recurrence_factor = self._pattern['freq_recurrence_factor']
                _freq_interval = self._pattern['freq_interval']
                _freq_relative_interval = self._pattern['freq_relative_interval']

            if 'relative_time' in pattern_dict:
                _freq_relative_interval = (
                    list(
                        self._relative_day.keys())[
                        list(
                            self._relative_day.values()).index(
                            pattern_dict['relative_time'].lower())])

            if 'relative_weekday' in pattern_dict:
                _freq_interval = (
                    list(
                        self._relative_weekday.keys())[
                        list(
                            self._relative_weekday.values()).index(
                            pattern_dict['relative_weekday'].lower())])

            _freq_recurrence_factor = pattern_dict.get(
                'repeat_months', _freq_recurrence_factor)

            pattern_dict['freq_recurrence_factor'] = 1 if not isinstance(
                _freq_recurrence_factor, int) else _freq_recurrence_factor

            pattern_dict['freq_interval'] = _freq_interval
            pattern_dict['freq_relative_interval'] = _freq_relative_interval

            pattern_dict['freq_type'] = 32
            self._pattern_json(pattern_dict)

        except ValueError as v_error:
            raise SDKException('Schedules', '102',
                               str(v_error))

    def _yearly(self, pattern_dict: Dict[str, Union[str, int]]) -> None:
        """
        sets the pattern type as monthly with the parameters provided
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                        {
                                 "active_start_time": time_in_%H/%S (str),
                                 "on_month": month to run schedule (str) January, Febuary...
                                 "on_day": Day to run schedule (int)
                        }
        Raises:
            SDKException: If there is a ValueError.
        Usage:
            pattern = SchedulePattern()
            pattern._yearly({"active_start_time": "10:00", "on_month": "January", "on_day": 1})
        """
        try:

            _freq_recurrence_factor = 1
            _freq_interval = 10
            if self._pattern['freq_type'] == 64:
                _freq_recurrence_factor = self._pattern['freq_recurrence_factor']
                _freq_interval = self._pattern['freq_interval']

            if 'on_month' in pattern_dict:
                _freq_recurrence_factor = list(
                    calendar.month_name).index(
                    pattern_dict['on_month'].title())

            _freq_interval = pattern_dict.get('on_day', _freq_interval)

            pattern_dict['freq_recurrence_factor'] = _freq_recurrence_factor
            pattern_dict['freq_interval'] = 1 if not isinstance(
                _freq_interval, int) else _freq_interval
            pattern_dict['freq_type'] = 64
            self._pattern_json(pattern_dict)

        except ValueError as ve:
            raise SDKException('Schedules', '102',
                               str(ve))

    def _yearly_relative(self, pattern_dict: Dict[str, str]) -> None:
        """
        sets the pattern type as monthly_relative with the parameters provided
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                        {
                                 "active_start_time": time_in_%H/%S (str),
                                 "relative_time": relative day of the schedule (str) 'first',
                                                                                        'second',..
                                 "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                                 "on_month": month to run the schedule(str) January, February...
                        }
        Raises:
            SDKException: If there is a ValueError.
        Usage:
            pattern = SchedulePattern()
            pattern._yearly_relative({"active_start_time": "10:00", "relative_time": "first", "relative_weekday": "monday", "on_month": "January"})
        """
        _freq_recurrence_factor = 1
        _freq_interval = 1
        _freq_relative_interval = 1

        try:

            if self._pattern['freq_type'] == 128:
                _freq_recurrence_factor = self._pattern['freq_recurrence_factor']
                _freq_interval = self._pattern['freq_interval']
                _freq_relative_interval = self._pattern['freq_relative_interval']

            if 'relative_time' in pattern_dict:
                _freq_relative_interval = (
                    list(
                        self._relative_day.keys())[
                        list(
                            self._relative_day.values()).index(
                            pattern_dict['relative_time'].lower())])

            if 'relative_weekday' in pattern_dict:
                _freq_interval = (
                    list(
                        self._relative_weekday.keys())[
                        list(
                            self._relative_weekday.values()).index(
                            pattern_dict['relative_weekday'].lower())])

            if 'on_month' in pattern_dict:
                _freq_recurrence_factor = list(
                    calendar.month_name).index(
                    pattern_dict['on_month'].title())
            pattern_dict['freq_recurrence_factor'] = _freq_recurrence_factor
            pattern_dict['freq_interval'] = _freq_interval
            pattern_dict['freq_relative_interval'] = _freq_relative_interval

            pattern_dict['freq_type'] = 128
            self._pattern_json(pattern_dict)

        except ValueError as ve:
            raise SDKException('Schedules', '102',
                               str(ve))

    def _continuous(self, pattern_dict: Dict[str, Union[str, int]]) -> None:
        """
        sets the pattern type as one time with the parameters provided,
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                                 job_interval: interval between jobs in mins(int)
                }
        Usage:
            pattern = SchedulePattern()
            pattern._continuous({"job_interval": 60})
        """

        _freq_recurrence_factor = pattern_dict.get('job_interval', 30)
        pattern_dict['freq_interval'] = 30 if not isinstance(
            _freq_recurrence_factor, int) else _freq_recurrence_factor
        pattern_dict['freq_type'] = 4096
        self._pattern_json(pattern_dict)

    def _automatic(self, pattern_dict: dict) -> None:
        """sets the pattern type as one time with the parameters provided,
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                                {
                                    min_interval_hours: minimum hours between jobs(int)
                                    min_interval_minutes: minimum minutes between jobs(int)
                                    max_interval_hours: maximum hours between jobs(int)
                                    max_interval_minutes: maximum minutes between jobs(int)
                                    min_sync_interval_hours: minimum sync hours
                                                                                   between jobs(int)
                                    min_sync_interval_minutes: minimum sync minutes
                                                                                   between jobs(int)
                                    ignore_opwindow_past_maxinterval: (bool)
                                    wired_network_connection: (bool)
                                    min_network_bandwidth: (int) kbps
                                    specific_network: (dict){ip_address:(str),subnet:(int)}
                                    dont_use_metered_network: (bool)
                                    ac_power: (bool)
                                    stop_if_on_battery: (bool)
                                    stop_sleep_if_runningjob: (bool)
                                    cpu_utilization_below : (int)%
                                    cpu_utilization_above : (int)%
                                    disk_use_threshold: (int)%
                                    number_of_log_files: (int)
                                }

        Usage:
            pattern_dict = {
                "max_interval_hours": 72,
                "ignore_opwindow_past_maxinterval": False,
                "min_interval_minutes": 15,
                "max_interval_minutes": 0,
                "min_sync_interval_hours": 0,
                "min_interval_hours": 0,
                "min_sync_interval_minutes": 2,
                "stop_if_on_battery": False,
                "ac_power": False,
                "specific_network": {"ip_address": "0.0.0.0", "subnet": 24},
                "stop_sleep_if_runningjob": False,
                "cpu_utilization_below": 10,
                "dont_use_metered_network": False,
                "cpu_utilization_above": 10,
                "wired_network_connection": False,
                "min_network_bandwidth": 128,
                "sweep_start_time": 3600,
                "use_storage_space_ma": False,
                "disk_use_threshold": 80,
                "number_of_log_files": 50
            }
            SchedulePattern()._automatic(pattern_dict)
        """
        automatic_pattern = {
            "maxBackupInterval": pattern_dict.get("max_interval_hours",
                                                  self._pattern.get("maxBackupInterval", 72)),
            "ignoreOpWindowPastMaxInterval": pattern_dict.get("ignore_opwindow_past_maxinterval",
                                                              self._pattern.get(
                                                                  "ignoreOpWindowPastMaxInterval",
                                                                  False)),
            "minBackupIntervalMinutes": pattern_dict.get("min_interval_minutes",
                                                         self._pattern.get(
                                                             "minBackupIntervalMinutes", 15)),
            "maxBackupIntervalMinutes": pattern_dict.get("max_interval_minutes",
                                                         self._pattern.get(
                                                             "maxBackupIntervalMinutes", 0)),
            "minSyncInterval": pattern_dict.get("min_sync_interval_hours",
                                                self._pattern.get("minSyncInterval", 0)),
            "minBackupInterval": pattern_dict.get("min_interval_hours",
                                                  self._pattern.get("minBackupInterval", 0)),
            "minSyncIntervalMinutes": pattern_dict.get("min_sync_interval_minutes",
                                                       self._pattern.get("minSyncIntervalMinutes",
                                                                         2)),
            "stopIfOnBattery": {
                "enabled": pattern_dict.get("stop_if_on_battery",
                                            self._pattern.get("stopIfOnBattery",
                                                              {'enabled': False})['enabled'])
            },
            "acPower": {
                "enabled": pattern_dict.get("ac_power",
                                            self._pattern.get("acPower",
                                                              {'enabled': False})['enabled'])
            },
            "specfificNetwork": {
                "enabled": True if 'specific_network' in pattern_dict
                else (self._pattern.get("specfificNetwork",
                                        {'enabled': False})['enabled']),
                "ipAddress": {
                    "family": 32,
                    "address": pattern_dict.get('specific_network',
                                                {"ip_address": "0.0.0.0"})["ip_address"],
                    "subnet": pattern_dict.get('specific_network',
                                               {"subnet": 24})["subnet"],
                }

            },
            "stopSleepIfBackUp": {
                "enabled": pattern_dict.get("stop_sleep_if_runningjob",
                                            self._pattern.get("stopSleepIfBackUp",
                                                              {'enabled': False})['enabled'])

            },
            "emergencyBackup": {
                "emergencyBackupCommandName": "",
                "emergencyBackup": {
                    "enabled": False
                }
            },
            "cpuUtilization": {
                "enabled": True if 'cpu_utilization_below' in pattern_dict
                else (self._pattern.get("cpuUtilization",
                                        {'enabled': False})['enabled']),
                "threshold": pattern_dict.get("cpu_utilization_below",
                                              self._pattern.get("cpuUtilization",
                                                                {'threshold': 10})['threshold'])
            },
            "dontUseMeteredNetwork": {
                "enabled": pattern_dict.get("dont_use_metered_network",
                                            self._pattern.get("dontUseMeteredNetwork",
                                                              {'enabled': False})['enabled'])
            },
            "cpuUtilizationAbove": {
                "enabled": True if 'cpu_utilization_above' in pattern_dict
                else (self._pattern.get("cpuUtilizationAbove",
                                        {'enabled': False})['enabled']),
                "threshold": pattern_dict.get("cpu_utilization_above",
                                              self._pattern.get("cpuUtilizationAbove",
                                                                {'threshold': 10})['threshold'])
            },
            "wiredNetworkConnection": {
                "enabled": pattern_dict.get("wired_network_connection",
                                            self._pattern.get("wiredNetworkConnection",
                                                              {'enabled': False})['enabled'])
            },
            "minNetworkBandwidth": {
                "enabled": True if 'min_network_bandwidth' in pattern_dict
                else (self._pattern.get("minNetworkBandwidth",
                                        {'enabled': False})['enabled']),
                "threshold": pattern_dict.get("min_network_bandwidth",
                                              self._pattern.get("minNetworkBandwidth",
                                                                {'threshold': 128})['threshold'])
            },
            "sweepStartTime": pattern_dict.get("sweep_start_time",
                                               self._pattern.get("sweepStartTime", 3600)
                                               ),
            "useStorageSpaceFromMA": pattern_dict.get("use_storage_space_ma",
                                               self._pattern.get("useStorageSpaceFromMA", False)
                                               ),
            "diskUsedPercent": {
                "enabled": True if 'disk_use_threshold' in pattern_dict
                else (self._pattern.get("diskUsedPercent",
                                        {'enabled': False})['enabled']),
                "threshold": pattern_dict.get("disk_use_threshold",
                                              self._pattern.get("diskUsedPercent",
                                                                {'threshold': 80})['threshold'])
            },
            "logFileNum": {
                "enabled": True if 'number_of_log_files' in pattern_dict
                else (self._pattern.get("logFileNum",
                                        {'enabled': False})['enabled']),
                "threshold": pattern_dict.get("number_of_log_files",
                                              self._pattern.get("logFileNum",
                                                                {'threshold': 50})['threshold'])
            }
        }

        self._pattern = automatic_pattern


    def _after_job_completes(self, pattern_dict: dict) -> None:
        """sets the pattern type as after job completes with the parameters provided,
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                    "active_start_date": date_in_%m/%d/%y (str),
                    "active_start_time": time_in_%H/%S (str),
                    "repeat_days": days_to_repeat (int)
                }

        Usage:
            pattern_dict = {
                "active_start_date": "12/31/2024",
                "active_start_time": "23/59",
                "repeat_days": 7
            }
            SchedulePattern()._after_job_completes(pattern_dict)
        """
        pattern_dict['freq_type'] = 'After_Job_Completes'

        pattern_dict['freq_recurrence_factor'] = pattern_dict.get('repeat_days', 4096)

        self._pattern_json(pattern_dict)


    @staticmethod
    def exception_dates(day_list: list) -> int:
        """Provided a Scheduler version of exception as an on day number

        Args:
            day_list (list): List of exception dates [1,2,3]

        Returns:
            int: on_day number for the pattern json

        Usage:
            day_list = [1, 2, 3]
            on_day = SchedulePattern.exception_dates(day_list)
        """
        on_day = 0
        for value in day_list:
            on_day |= (1 << (value - 1))
        return on_day


    def create_schedule_pattern(self, pattern_dict: dict) -> dict:
        """calls the required type of schedule module and forms the pattern json

        Args:
            pattern_dict (dict): Dictionary containing schedule pattern details.
                freq_type is mandatory, all other fields specified below can be skipped and system
                defaults will be set. For reference on pattern_dict check create_schedule.

        Returns:
            dict: pattern which can be plugged into the create or modify task request to
            create or modify schedules

        Raises:
            SDKException: If 'freq_type' is not in pattern_dict or if freq_type specified is wrong.

        Usage:
            pattern_dict = {"freq_type": "one_time", "active_start_date": "12/31/2024", "active_start_time": "23:59"}
            pattern = SchedulePattern().create_schedule_pattern(pattern_dict)
        """

        if 'freq_type' not in pattern_dict:
            raise SDKException('Schedules', '102',
                               "Frequency type is required to create pattern")

        try:
            getattr(
                self,
                '_' +
                pattern_dict['freq_type'].lower())(pattern_dict)
            return self._pattern

        except AttributeError:
            raise SDKException('Schedules', '102',
                               "freq_type specified is wrong")


    def create_schedule(self, task_req: dict, pattern_dict: dict, schedule_id: str = None) -> dict:
        """returns a schedule task_req after including pattern

        Args:
            task_req (dict): task_req for immediate job operation to be converted to a schedule
            pattern_dict (dict): schedule pattern to be merged with the task request
                freq_type is mandatory, all other fields specified below can be skipped and system
                defaults will be set.

                with the same dict, pass
                time_zone: Time Zone Name(default is taken as COmmServe Time Zone)
                    Common Time Zones examples -- 'CommServe Time Zone', 'Client Time Zone', 'UTC'

                for one_time: {
                                     "freq_type": 'one_time',
                                     "active_start_date": date_in_%m/%d/%y (str),
                                     "active_start_time": time_in_%h:%m (str)
                            }

                for daily: {
                                 "freq_type": 'daily',
                                 "active_start_time": time_in_%H/%S (str),
                                 "repeat_days": days_to_repeat (int)
                          }

                for weekly: {
                                 "freq_type": 'weekly',
                                 "active_start_time": time_in_%H/%S (str),
                                 "repeat_weeks": weeks_to_repeat (int)
                                 "weekdays": list of weekdays ['Monday','Tuesday']
                                }

                for monthly: {
                                         "freq_type": 'monthly',
                                         "active_start_time": time_in_%H/%S (str),
                                         "repeat_months": weeks_to_repeat (int)
                                         "on_day": Day to run schedule (int)
                                }

                for monthly_relative:    {
                                         "active_start_time": time_in_%H/%S (str),
                                         "relative_time": relative day of the schedule (str) 'first',
                                                                                                'second',..
                                         "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                                         "repeat_months": months_to_repeat
                                        }

                for yearly: {
                                         "active_start_time": time_in_%H/%S (str),
                                         "on_month": month to run schedule (str) January, Febuary...
                                         "on_day": Day to run schedule (int)
                                }

                for yearly_relative: {
                                         "active_start_time": time_in_%H/%S (str),
                                         "relative_time": relative day of the schedule (str) 'first',
                                                                                                'second',..
                                         "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                                         "on_month": month to run the schedule(str) January, Febuary...
                                }

                for continuous: {
                                         job_interval: interval between jobs in mins(int)
                        }

                for automatic: {
                                             min_interval_hours: minimum hours between jobs(int)
                                             min_interval_minutes: minimum minutes between jobs(int)
                                             max_interval_hours: maximum hours between jobs(int)
                                             max_interval_minutes: maximum minutes between jobs(int)
                                             min_sync_interval_hours: minimum sync hours
                                                                                            between jobs(int)
                                             min_sync_interval_minutes: minimum sync minutes
                                                                                            between jobs(int)
                                             ignore_opwindow_past_maxinterval: (bool)
                                             wired_network_connection: (bool)
                                             min_network_bandwidth: (int) kbps
                                             specific_network: (dict){ip_address:(str),subnet:(int)}
                                             dont_use_metered_network: (bool)
                                             ac_power: (bool)
                                             stop_if_on_battery: (bool)
                                             stop_sleep_if_runningjob: (bool)
                                             cpu_utilization_below : (int)%
                                             cpu_utilization_above : (int)%
                                             disk_use_threshold: (int)%
                                             number_of_log_files: (int)
                                }

                for after_job_completes :   {
                                                "freq_type": 'after_job_completes',
                                                "active_start_date": date_in_%m/%d/%y (str),
                                                "active_start_time": time_in_%H/%S (str),
                                                "repeat_days": days_to_repeat (int)
                                            }

                Sample Usage inside the individual operation function:
                Add a schedule_pattern parameter to the function and include the below line before making
                the sdk make_request call

                if schedule_pattern:
                    request_json = SchedulePattern().create_schedule(task_req,schedule_pattern)

        Returns:
             dict: Schedule task request

        Usage:
            task_req = {"taskInfo": {"task": {"taskType": 1}, "subTasks": [{"subTask": {"subTaskId": "123"}}]}}
            pattern_dict = {"freq_type": "one_time", "active_start_date": "12/31/2024", "active_start_time": "23:59"}
            schedule_id = "123"
            updated_task_req = SchedulePattern().create_schedule(task_req, pattern_dict, schedule_id)
        """

        _automatic_pattern = {}

        if pattern_dict["freq_type"] == 'automatic':
            _pattern = {"freq_type": 1024}
            _automatic_pattern = self.create_schedule_pattern(pattern_dict)
        else:
            _pattern = self.create_schedule_pattern(pattern_dict)

        _task_info = task_req["taskInfo"]
        if _task_info.get("task"):
            _task_info["task"]["taskType"] = 2
        for subtask in _task_info['subTasks']:
            if schedule_id:
                if subtask["subTask"]['subTaskId'] != schedule_id:
                    continue
            else:
                subtask["subTask"]['subTaskName'] = pattern_dict.get(
                    'schedule_name', '')
            subtask["pattern"] = _pattern
            if pattern_dict["freq_type"] == 'automatic':
                if 'options' in subtask:
                    _task_options = subtask['options']
                    if 'commonOpts' in _task_options:
                        _task_options["commonOpts"]["automaticSchedulePattern"] = _automatic_pattern
                    else:
                        _task_options["commonOpts"] = \
                            {"automaticSchedulePattern": _automatic_pattern}

                    if 'run_synthetic_full' in pattern_dict:
                        synthetic_pattern = pattern_dict['run_synthetic_full']

                        if synthetic_pattern == 'every_x_days':
                            synthetic_interval = pattern_dict.get(
                                'days_between_synthetic_full', 30)
                        else:
                            synthetic_interval = 30

                        _data_opt = {
                            'autoCopy': True,
                            'daysBetweenSyntheticBackup': synthetic_interval,
                            'useAutomaticIntervalForSyntheticFull': (
                                    synthetic_pattern == 'extended_retention'),
                            'enableRunFullConsolidationBackup': (
                                    synthetic_pattern == 'space_reclaim')
                        }

                        if 'backupOpts' in _task_options:
                            if 'dataOpt' in _task_options["backupOpts"]:
                                _task_options['backupOpts']['dataOpt'].update(_data_opt)
                            else:
                                _task_options['backupOpts']['dataOpt'] = _data_opt
                        else:
                            _task_options['backupOpts'] = {
                                'dataOpt': _data_opt
                            }

                else:
                    subtask['options'] = {
                        'commonOpts': {
                            'automaticSchedulePattern': _automatic_pattern}}

        task_req["taskInfo"] = _task_info
        return task_req

class Schedules:
    """Class for getting the schedules of a commcell entity.

    Attributes:
        class_object (object): Instance of client/agent/backupset/subclient/CommCell class.
        schedules (dict): Dictionary of schedules associated with the commcell entity.

    Usage:
        # Initialize Schedules for a client
        schedules = Schedules(client_object)
    """

    def __init__(self, class_object: Union['Commcell', 'Client', 'Agent', 'Instance', 'Backupset', 'Subclient', 'Inventory', 'FsoServer', 'Project'], operation_type: str = None) -> None:
        """Initialise the Schedules class instance.

            Args:
                class_object (object): instance of Commcell/Client/Agent/Backupset/Subclient/Inventory/FsoServer/Project class
                operation_type (str, optional): required when commcell object is passed
                                        refer OperationType class for supported op types. Defaults to None.

            Raises:
                SDKException:
                    if class object does not belong to any of the Client or Agent or Backupset or
                        Subclient class
        """
        # imports inside the __init__ method definition to avoid cyclic imports
        from .commcell import Commcell
        from .client import Client
        from .agent import Agent
        from .backupset import Backupset
        from .subclient import Subclient
        from .instance import Instance
        from .activateapps.inventory_manager import Inventory
        from .activateapps.file_storage_optimization import FsoServer
        from .activateapps.sensitive_data_governance import Project

        self.class_object = class_object
        self._single_scheduled_entity = False
        self._task_flags = {}
        self._repr_str = ""

        if isinstance(class_object, Commcell):
            self._commcell_object = class_object
            if operation_type == OperationType.REPORTS:
                self._SCHEDULES = class_object._services['REPORT_SCHEDULES']
                self._repr_str = "Reports in Commcell: {0}".format(
                    class_object.commserv_name)
            elif operation_type == OperationType.DATA_AGING:
                self._SCHEDULES = class_object._services['OPTYPE_SCHEDULES'] % (
                    operation_type)
                self._repr_str = "Dataging in Commcell: {0}".format(
                    class_object.commserv_name)
            elif not operation_type:
                self._SCHEDULES = class_object._services['COMMCELL_SCHEDULES']
                self._repr_str = "Schedules in Commcell"
            else:
                raise SDKException('Schedules', '103')
        elif isinstance(class_object, FsoServer):
            self._SCHEDULES = class_object._commcell_object._services['CLIENT_SCHEDULES'] % (
                class_object.server_id)
            self._repr_str = "Fso Server: {0}".format(class_object.server_id)
            self._commcell_object = class_object._commcell_object
            self._single_scheduled_entity = True
            self._task_flags['isEdiscovery'] = True

        elif isinstance(class_object, Project):
            self._SCHEDULES = class_object._commcell_object._services['CLIENT_SCHEDULES'] % (
                class_object.project_id)
            self._repr_str = "SDG Project: {0}".format(class_object.project_id)
            self._commcell_object = class_object._commcell_object
            self._single_scheduled_entity = True
            self._task_flags['isEdiscovery'] = True

        elif isinstance(class_object, Inventory):
            self._SCHEDULES = class_object._commcell_object._services['INVENTORY_SCHEDULES'] % (
                class_object.inventory_id)
            self._repr_str = "Inventory: {0}".format(class_object.inventory_name)
            self._commcell_object = class_object._commcell_object
            # set below flag to denote inventory type entity will always have only one schedule associated to it
            self._single_scheduled_entity = True

        elif isinstance(class_object, Client):
            self._SCHEDULES = class_object._commcell_object._services['CLIENT_SCHEDULES'] % (
                class_object.client_id)
            self._repr_str = "Client: {0}".format(class_object.client_name)
            self._commcell_object = class_object._commcell_object

        elif isinstance(class_object, Agent):
            self._SCHEDULES = class_object._commcell_object._services['AGENT_SCHEDULES'] % (
                class_object._client_object.client_id, class_object.agent_id)
            self._repr_str = "Agent: {0}".format(class_object.agent_name)
            self._commcell_object = class_object._commcell_object

        elif isinstance(class_object, Instance):
            self._SCHEDULES = class_object._commcell_object._services['INSTANCE_SCHEDULES'] % (
                class_object._agent_object._client_object.client_id,
                class_object._agent_object.agent_id,
                class_object.instance_id
            )
            self._repr_str = "Instance: {0}".format(
                class_object.instance_name)
            self._commcell_object = class_object._commcell_object

        elif isinstance(class_object, Backupset):
            self._SCHEDULES = class_object._commcell_object._services['BACKUPSET_SCHEDULES'] % (
                class_object._agent_object._client_object.client_id,
                class_object._agent_object.agent_id,
                class_object.backupset_id
            )
            self._repr_str = "Backupset: {0}".format(
                class_object.backupset_name)
            self._commcell_object = class_object._commcell_object

        elif isinstance(class_object, Subclient):
            self._SCHEDULES = class_object._commcell_object._services['SUBCLIENT_SCHEDULES'] % (
                class_object._backupset_object._agent_object._client_object.client_id,
                class_object._backupset_object._agent_object.agent_id,
                class_object._backupset_object.backupset_id,
                class_object.subclient_id
            )
            self._repr_str = "Subclient: {0}".format(
                class_object.subclient_name)
            self._commcell_object = class_object._commcell_object
        else:
            raise SDKException('Schedules', '101')

        self.schedules = None
        self.refresh()

    def __str__(self) -> str:
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

    def __repr__(self) -> str:
        """Representation string for the instance of the Schedules class."""
        return "Schedules class instance for {0}".format(self._repr_str)

    def _get_schedules(self) -> dict:
        """Gets the schedules associated with the input commcell entity.
            Client / Agent / Backupset / Subclient

            Returns:
                dict: consists of all schedules for the commcell entity
                    {
                         "schedule_id": {
                                'task_id': task_id,
                                'schedule_name': schedule_name,
                                'description': description
                            }

                         "schedule_id": {
                                'task_id': task_id,
                                'schedule_name': schedule_name,
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
                subtask_dict = {}
                for schedule in response.json()['taskDetail']:
                    task_id = schedule['task']['taskId']
                    description = ''
                    task_flags = schedule['task'].get('taskFlags', 0)
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
                            # change schedule_id as key
                            subtask_dict[schedule_id] = {
                                'task_id': task_id,
                                'schedule_name': subtask_name,
                                'description': description,
                                'task_flags': task_flags
                            }

                return subtask_dict
            else:
                return {}
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _get_sch_id_from_task_id(self, task_id: int) -> int:
        """
        Gets the schedule id from the task id

        Args:
            task_id (int): task id of the schedule

        Returns:
            int: schedule id of the schedule

        Raises:
            SDKException: if schedule id not found for the corresponding task id
        """
        task_ids = [k for k, v in self.schedules.items() if v['task_id'] == task_id]
        if task_ids:
            return task_ids[0]
        else:
            raise SDKException('Schedules', '102', 'Schedule id not found for corresponding task id')

    def _get_schedule_id(self, schedule_name: str = None, schedule_id: int = None, task_id: int = None) -> int:
        """Gets the schedule id from the provided inputs.

            Args:
                schedule_name (str, optional): name of the schedule. Defaults to None.
                schedule_id (int, optional): id of the schedule. Defaults to None.
                task_id (int, optional): task id of the schedule. Defaults to None.

            Returns:
                int: schedule id of the schedule

            Raises:
                SDKException:
                    if neither schedule_name nor schedule_id is provided
                    if schedule_name is not a string
                    if schedule_id is not an integer
                    if task_id is not an integer
        """

        if self._single_scheduled_entity:
            # if flag set, then entity will have only one schedule associated to it so return first one from dict
            # if flag set along with task flags, then find schedule with that flags set and return that from dict
            for subtask_id, subtask_dict in self.schedules.items():
                if len(self._task_flags) == 0:
                    return subtask_id
                else:
                    task_flags = subtask_dict['task_flags']
                    match = True
                    for flag, value in self._task_flags.items():
                        if flag in task_flags:
                            if task_flags[flag] != value:
                                match = False
                        else:
                            match = False
                    if match:
                        return subtask_id
            return None

        if not task_id and not schedule_name and not schedule_id:
            raise SDKException(
                'Schedules',
                '102',
                'Either Schedule Name or Schedule Id is needed')

        if schedule_name and not isinstance(schedule_name, str):
            raise SDKException('Schedules', '102')

        if schedule_id and not isinstance(schedule_id, int):
            raise SDKException('Schedules', '102')

        if task_id and not isinstance(task_id, int):
            raise SDKException('Schedules', '102')

        if schedule_name:
            schedule_name = schedule_name.lower()
            for subtask_id, subtask_dict in self.schedules.items():
                if subtask_dict['schedule_name'] == schedule_name:
                    schedule_id = subtask_id

        elif task_id:
            schedule_id = self._get_sch_id_from_task_id(task_id)

        if self.schedules and schedule_id in self.schedules:
            return schedule_id

    def has_schedule(self, schedule_name: str = None, schedule_id: int = None, task_id: int = None) -> bool:
        """Checks if a schedule exists for the commcell entity with the input schedule name.

            Args:
                schedule_name (str, optional): name of the schedule. Defaults to None.
                schedule_id (int, optional): id of the schedule. Defaults to None.
                task_id (int, optional): task id of the schedule. Defaults to None.

            Returns:
                bool: boolean output whether the schedule exists for the commcell entity or not

            Raises:
                SDKException:
                    if type of the schedule name argument is not string
        """
        if self._get_schedule_id(schedule_name, schedule_id, task_id):
            return True
        return False

    def get(self, schedule_name: str = None, schedule_id: int = None, task_id: int = None) -> 'Schedule':
        """Returns a schedule object of the specified schedule name.

            Args:
                schedule_name (str, optional): name of the Schedule. Defaults to None.
                schedule_id (int, optional): id of the schedule. Defaults to None.
                task_id (int, optional): task id of the schedule. Defaults to None.

            Returns:
                object: instance of the schedule class for the given schedule name

            Raises:
                SDKException:
                    if type of the schedule name argument is not string

                    if no schedule exists with the given name

            Usage:
                # Get a schedule by name
                schedule = schedules.get(schedule_name='My Schedule')

                # Get a schedule by ID
                schedule = schedules.get(schedule_id=123)

                # Get a schedule by task ID
                schedule = schedules.get(task_id=456)
        """
        schedule_id = self._get_schedule_id(schedule_name, schedule_id, task_id)
        if schedule_id:
            return Schedule(self.class_object, schedule_id=schedule_id, task_id=self.schedules[schedule_id]['task_id'])

        raise SDKException('Schedules', '105')

    def delete(self, schedule_name: str = None, schedule_id: int = None, task_id: int = None) -> None:
        """deletes the specified schedule name.

                    Args:
                        schedule_name (str, optional): name of the Schedule. Defaults to None.
                        schedule_id (int, optional): id of the schedule. Defaults to None.
                        task_id (int, optional): task id of the schedule. Defaults to None.

                    Raises:
                        SDKException:
                            if type of the schedule name argument is not string
                            if no schedule exists with the given name

                    Usage:
                        # Delete a schedule by name
                        schedules.delete(schedule_name='My Schedule')

                        # Delete a schedule by ID
                        schedules.delete(schedule_id=123)

                        # Delete a schedule by task ID
                        schedules.delete(task_id=456)
        """

        schedule_id = self._get_schedule_id(schedule_name, schedule_id, task_id)
        if schedule_id:
            request_json = {
                "TMMsg_TaskOperationReq":
                    {
                        "opType": 3,
                        "subtaskEntity":
                            [
                                {
                                    "_type_": 68,
                                    "subtaskId": schedule_id
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
                exception_message = 'Failed to delete schedule\nError: "{0}"'.format(
                    response_string)

                raise SDKException('Schedules', '102', exception_message)
        else:
            raise SDKException('Schedules', '105')

    def refresh(self) -> None:
        """Refresh the Schedules associated with the Client / Agent / Backupset / Subclient.

        Usage:
            schedules.refresh()
        """
        self.schedules = self._get_schedules()

class Schedule:
    """Class for performing operations for a specific Schedule.

    Attributes:
        class_object (object): Instance of Class Object.
        _commcell_object (object): Instance of the Commcell class.
        schedule_name (str): Name of the Schedule.
        schedule_id (int): Task ID of the Schedule.
        task_id (int): Task ID of the Schedule.
        _SCHEDULE (str): API service endpoint for the schedule.
        _MODIFYSCHEDULE (str): API service endpoint for modifying the schedule.
        _freq_type (dict): Dictionary mapping frequency types to their string representations.
        _week_of_month (dict): Dictionary mapping week numbers to their string representations.
        task_operation_type (dict): Dictionary mapping task operation types to their string representations.
        _criteria (dict): Criteria for the schedule.
        _pattern (dict): Pattern for the schedule.
        _task_options (dict): Task options for the schedule.
        _associations_json (dict): Associations JSON for the schedule.
        _description (str): Description of the schedule.
        _alert_type (str): Alert type for the schedule.
        _sub_task_option (dict): Subtask options for the schedule.
        _automatic_pattern (dict): Automatic pattern for the schedule.
        virtualServerRstOptions (dict): Virtual server restore options for the schedule.
        _schedule_disabled (bool): Indicates if the schedule is disabled.

    Usage:
        >>> schedule = Schedule(commcell_object, schedule_name='MySchedule')
    """

    def __init__(
        self,
        class_object: Union['Commcell', 'Client', 'Agent', 'Instance', 'Backupset', 'Subclient', 'Inventory', 'FsoServer', 'Project'],
        schedule_name: Optional[str] = None,
        schedule_id: Optional[int] = None,
        task_id: Optional[int] = None,
    ) -> None:
        """Initialise the Schedule class instance.

        Args:
            class_object (object): Instance of Class Object.
            schedule_name (str, optional): Name of the Schedule. Defaults to None.
            schedule_id (int, optional): Task ID of the Schedule. Defaults to None.
            task_id (int, optional): Task ID of the Schedule. Defaults to None.

        Raises:
            SDKException:
                If neither schedule_name nor schedule_id is provided.

        Usage:
            >>> schedule = Schedule(commcell_object, schedule_name='MySchedule')
            >>> schedule = Schedule(commcell_object, schedule_id=123)
        """

        from .commcell import Commcell

        self.class_object = class_object

        if isinstance(class_object, Commcell):
            self._commcell_object = class_object
        else:
            self._commcell_object = class_object._commcell_object
        self.schedule_name = ''

        if not schedule_name and not schedule_id:
            raise SDKException(
                'Schedules',
                '102',
                'Either Schedule Name or Schedule Id is needed')

        if schedule_name:
            self.schedule_name = schedule_name.lower()

        if schedule_id:
            self.schedule_id = schedule_id
        else:
            self.schedule_id = self._get_schedule_id()

        if task_id:
            self.task_id = task_id
        else:
            self.task_id = self._get_task_id()

        self._SCHEDULE = self._commcell_object._services['SCHEDULE'] % (
            self.task_id)
        self._MODIFYSCHEDULE = self._commcell_object._services['EXECUTE_QCOMMAND']

        self._freq_type = {
            1: 'One_Time',
            2: 'On_Demand',
            4: 'Daily',
            8: 'Weekly',
            16: 'Monthly',
            32: 'Monthly_Relative',
            64: 'Yearly',
            128: 'Yearly_Relative',
            1024: 'Automatic',
            4096: 'Continuous'
        }

        self._week_of_month = {
            '1': 'First',
            '2': 'Second',
            '3': 'Third',
            '4': 'Fourth',
            '5': 'Last'
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

        self._criteria = {}
        self._pattern = {}
        self._task_options = {}
        self._associations_json = {}
        self._description = None
        self._alert_type = None
        self._sub_task_option = None
        self._automatic_pattern = {}
        self.virtualServerRstOptions = None
        self._schedule_disabled = None
        self.refresh()

    @property
    def subtask_id(self) -> int:
        """Property which returns subtask id of the schedule

        Returns:
            int: Subtask id
        """
        return self.schedule_id

    def _get_schedule_id(self) -> int:
        """Gets a schedule ID dict for the schedule

        Returns:
            int: schedule ID
        """
        schedules_obj = Schedules(self.class_object)
        return schedules_obj.get(self.schedule_name).schedule_id

    def _get_task_id(self) -> int:
        """Gets a schedule ID dict for the schedule

        Returns:
            int: schedule ID
        """
        schedules_obj = Schedules(self.class_object)
        return schedules_obj.schedules.get(self.schedule_id).get('task_id')

    def _get_schedule_properties(self) -> Dict:
        """Gets the properties of this Schedule.

        Returns:
            dict: dictionary consisting of the properties of this Schedule

        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._SCHEDULE)

        if flag:
            if response.json() and 'taskInfo' in response.json():
                _task_info = response.json()['taskInfo']

                if 'associations' in _task_info:
                    self._associations_json = _task_info['associations']

                if 'task' in _task_info:
                    self._task_json = _task_info['task']

                    # Get status of schedule enabled/disabled
                    self._schedule_disabled = self._task_json.get('taskFlags', {}).get('disabled')

                for subtask in _task_info['subTasks']:
                    self._sub_task_option = subtask['subTask']
                    if self._sub_task_option['subTaskId'] == self.schedule_id:
                        self.schedule_name = self._sub_task_option['subTaskName']
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
                            if 'restoreOptions' in self._task_options:
                                if 'virtualServerRstOption' in self._task_options['restoreOptions']:
                                    self.virtualServerRstOptions = self._task_options['restoreOptions'][
                                        'virtualServerRstOption']

                            if 'commonOpts' in self._task_options:
                                if 'automaticSchedulePattern' in self._task_options["commonOpts"]:
                                    self._automatic_pattern = self._task_options[
                                        "commonOpts"]['automaticSchedulePattern']

                            if 'backupOpts' in self._task_options:
                                if 'dataOpt' in self._task_options['backupOpts']:
                                    if isinstance(self._automatic_pattern, dict):
                                        _data_opt = self._task_options['backupOpts']['dataOpt']
                                        self._automatic_pattern.update(_data_opt)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def is_disabled(self) -> bool:
        """Get the schedule status

        Returns:
            bool: True if the schedule is disabled otherwise returns False
        """
        return self._schedule_disabled

    @property
    def schedule_freq_type(self) -> str:
        """get the schedule frequency type

        Returns:
            str: the schedule frequency type
        """
        return self._freq_type[self._pattern['freq_type']]

    @property
    def name(self) -> str:
        """gets the name of the schedule

        Returns:
            str: The schedule name
        """
        return self.schedule_name

    @name.setter
    def name(self, new_name: str) -> None:
        """sets the name of the schedule

        Args:
            new_name (str): New name for the schedule

        Usage:
            >>> schedule.name = "New Schedule Name"
        """
        self.schedule_name = new_name
        self._sub_task_option['subTaskName'] = new_name
        self._sub_task_option['subTask']['subtaskName'] = new_name
        self._modify_task_properties()

    @property
    def one_time(self) -> Dict:
        """gets the one time schedule pattern

        Returns:
            dict: The schedule pattern
                {
                     "active_start_date": date_in_%m/%d/%y (str),
                     "active_start_time": time_in_%h:%m (str)
                }

            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'One_Time':
            return {
                'active_start_date': SchedulePattern._time_converter(
                    self._pattern['active_start_date'],
                    '%m/%d/%Y', False),
                'active_start_time': SchedulePattern._time_converter(
                    self._pattern['active_start_time'],
                    '%H:%M', False)
            }

        return False

    @one_time.setter
    def one_time(self, pattern_dict: Dict) -> None:
        """sets the pattern type as one time with the parameters provided,
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictonary with the schedule pattern
                {
                                 "active_start_date": date_in_%m/%d/%y (str),
                                 "active_start_time": time_in_%h:%m (str)
                }

        Usage:
            >>> schedule.one_time = {"active_start_date": "12/31/2024", "active_start_time": "23:59"}
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'one_time'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def daily(self) -> Dict:
        """gets the daily schedule

        Returns:
            dict: The schedule pattern
                    {
                                     "active_start_time": time_in_%H/%S (str),
                                     "repeat_days": days_to_repeat (int)
                    }
            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Daily':
            return {'active_start_time': SchedulePattern._time_converter(
                self._pattern['active_start_time'], '%H:%M', False),
                'repeat_days': self._pattern['freq_recurrence_factor']
            }
        return False

    @daily.setter
    def daily(self, pattern_dict: Dict) -> None:
        """sets the pattern type as daily with the parameters provided
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                     "active_start_time": time_in_%H/%S (str),
                     "repeat_days": days_to_repeat (int)
                }

        Usage:
            >>> schedule.daily = {"active_start_time": "10:00", "repeat_days": 1}
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'daily'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def weekly(self) -> Dict:
        """gets the weekly schedule

        Returns:
            dict: The schedule pattern
                {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_weeks": weeks_to_repeat (int)
                         "weekdays": list of weekdays ['Monday','Tuesday']
                }
            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Weekly':
            _freq = self._pattern['freq_interval']
            return {
                'active_start_time': SchedulePattern._time_converter(
                    self._pattern['active_start_time'],
                    '%H:%M',
                    False),
                'repeat_weeks': self._pattern['freq_recurrence_factor'],
                'weekdays': [
                    SchedulePattern._days_to_run[x] for x in list(
                        SchedulePattern._days_to_run.keys()) if _freq & x > 0]}
        return False

    @weekly.setter
    def weekly(self, pattern_dict: Dict) -> None:
        """sets the pattern type as weekly with the parameters provided
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_weeks": weeks_to_repeat (int)
                         "weekdays": list of weekdays ['Monday','Tuesday']
                }

        Usage:
            >>> schedule.weekly = {"active_start_time": "09:00", "repeat_weeks": 2, "weekdays": ["Monday", "Wednesday"]}
        """

        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'weekly'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def monthly(self) -> Dict:
        """gets the monthly schedule

        Returns:
            dict: the schedule pattern
                {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_months": months_to_repeat (int)
                         "on_day": Day to run schedule (int)
                }
            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Monthly':
            return {
                'active_start_time': SchedulePattern._time_converter(
                    self._pattern['active_start_time'],
                    '%H:%M',
                    False),
                'repeat_months': self._pattern['freq_recurrence_factor'],
                'on_day': self._pattern['freq_interval']}
        return False

    @monthly.setter
    def monthly(self, pattern_dict: Dict) -> None:
        """sets the pattern type as monthly with the parameters provided
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                         "active_start_time": time_in_%H/%S (str),
                         "repeat_months": months_to_repeat (int)
                         "on_day": Day to run schedule (int)
                }

        Usage:
            >>> schedule.monthly = {"active_start_time": "11:00", "repeat_months": 1, "on_day": 15}
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'monthly'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def monthly_relative(self) -> Dict:
        """gets the monthly_relative schedule

        Returns:
            dict: The schedule pattern
                {
                     "active_start_time": time_in_%H/%S (str),
                     "relative_time": relative day of the schedule (str)'first','second',..
                     "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                     "repeat_months": months_to_repeat
                }
            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Monthly_Relative':
            return {
                'active_start_time': SchedulePattern._time_converter(
                    self._pattern['active_start_time'],
                    '%H:%M',
                    False),
                'relative_time': SchedulePattern._relative_day[
                    self._pattern['freq_relative_interval']],
                'relative_weekday': SchedulePattern._relative_weekday[
                    self._pattern['freq_interval']],
                'repeat_months': self._pattern['freq_recurrence_factor']}
        return False

    @monthly_relative.setter
    def monthly_relative(self, pattern_dict: Dict) -> None:
        """sets the pattern type as monthly_relative with the parameters provided
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                     "active_start_time": time_in_%H/%S (str),
                     "relative_time": relative day of the schedule (str) 'first',
                                                                            'second',..
                     "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                     "repeat_months": months_to_repeat
                }

        Usage:
            >>> schedule.monthly_relative = {"active_start_time": "14:00", "relative_time": "first", "relative_weekday": "monday", "repeat_months": 3}
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'monthly_relative'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def yearly(self) -> Dict:
        """gets the yearly schedule

        Returns:
            dict: The schedule pattern
                {
                         "active_start_time": time_in_%H/%S (str),
                         "on_month": month to run schedule (str) January, Febuary...
                         "on_day": Day to run schedule (int)
                }
            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Yearly':
            return {'active_start_time':
                    SchedulePattern._time_converter(self._pattern['active_start_time'],
                                                    '%H:%M', False),
                    'on_month': calendar.month_name[self._pattern['freq_recurrence_factor']],
                    'on_day': self._pattern['freq_interval']
                    }
        return False

    @yearly.setter
    def yearly(self, pattern_dict: Dict) -> None:
        """sets the pattern type as monthly with the parameters provided
        send only required keys to change only those values

        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                         "active_start_time": time_in_%H/%S (str),
                         "on_month": month to run schedule (str) January, Febuary...
                         "on_day": Day to run schedule (int)
                }

        Usage:
            >>> schedule.yearly = {"active_start_time": "16:00", "on_month": "January", "on_day": 1}
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'yearly'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def yearly_relative(self) -> Dict:
        """gets the yearly_relative schedule

        Returns:
            dict: The schedule pattern
                {
                     "active_start_time": time_in_%H/%S (str),
                     "relative_time": relative day of the schedule (str)'first','second',..
                     "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                     "on_month": month to run the schedule(str) January, Febuary...
                }
            False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Yearly_Relative':
            return {'active_start_time':
                    SchedulePattern._time_converter(self._pattern['active_start_time'],
                                                    '%H:%M', False),
                    'relative_time': SchedulePattern._relative_day
                    [self._pattern['freq_relative_interval']],
                    'relative_weekday': SchedulePattern._relative_weekday
                    [self._pattern['freq_interval']],
                    'on_month': calendar.month_name[self._pattern['freq_recurrence_factor']]
                    }
        return False

    @yearly_relative.setter
    def yearly_relative(self, pattern_dict: dict) -> None:
        """
        sets the pattern type as monthly_relative with the parameters provided
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                        {
                                 "active_start_time": time_in_%H/%S (str),
                                 "relative_time": relative day of the schedule (str) 'first',
                                                                                        'second',..
                                 "relative_weekday": Day to run schedule (str) 'sunday','monday'...
                                 "on_month": month to run the schedule(str) January, February...
                        }
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'yearly_relative'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def continuous(self) -> dict:
        """
        gets the continuous schedule
        Returns:
            (dict): The schedule pattern
                        {
                                 job_interval: interval between jobs in mins(int)
                }
                False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Continuous':
            return {
                'job_interval': self._pattern['freq_interval']
            }
        return False

    @continuous.setter
    def continuous(self, pattern_dict: dict) -> None:
        """
        sets the pattern type as one time with the parameters provided,
        send only required keys to change only those values
        Args:
            pattern_dict (dict): Dictionary with the schedule pattern
                {
                                 job_interval: interval between jobs in mins(int)
                }
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'continuous'
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def automatic(self) -> dict:
        """
        gets the automatic schedule
        Returns:
            (dict): The schedule pattern
                        {
                                 min_interval_hours: minimum hours between jobs(int)
                                 min_interval_minutes: minimum minutes between jobs(int)
                                 max_interval_hours: maximum hours between jobs(int)
                                 max_interval_minutes: maximum minutes between jobs(int)
                                 min_sync_interval_hours: minimum sync hours
                                                                        between jobs(int)
                                 min_sync_interval_minutes: minimum sync minutes
                                                                        between jobs(int)
                                 ignore_opwindow_past_maxinterval: (bool)
                                 wired_network_connection: (bool)
                                 min_network_bandwidth: (int) kbps
                                 specific_network: (dict){ip_address:(str),subnet:(int)}
                                 dont_use_metered_network: (bool)
                                 ac_power: (bool)
                                 stop_if_on_battery: (bool)
                                 stop_sleep_if_runningjob: (bool)
                                 cpu_utilization_below : (int)%
                                 cpu_utilization_above : (int)%
                                 run_synthetic_full : (str: every_x_days/extended_retention/
                                 space_reclaim)
                                 days_between_synthetic_full : (int)
                        }
                False: if schedule type is wrong
        """
        if self.schedule_freq_type == 'Automatic':
            pattern = {
                "min_interval_hours": self._automatic_pattern['minBackupInterval'],
                "min_interval_minutes": self._automatic_pattern['minBackupIntervalMinutes'],
                "max_interval_hours": self._automatic_pattern['maxBackupInterval'],
                "max_interval_minutes": self._automatic_pattern['maxBackupIntervalMinutes'],
                "min_sync_interval_hours": self._automatic_pattern['minSyncInterval'],
                "min_sync_interval_minutes": self._automatic_pattern['minSyncIntervalMinutes'],
                "ignore_opwindow_past_maxinterval": self._automatic_pattern['ignoreOpWindowPastMaxInterval'],
                "wired_network_connection": self._automatic_pattern.get('wiredNetworkConnection',
                                                                        {'enabled': False})['enabled'],
                "min_network_bandwidth": self._automatic_pattern.get('minNetworkBandwidth',
                                                                     {'enabled': False})['enabled'],
                "specific_network": self._automatic_pattern.get('specfificNetwork',
                                                                {'enabled': False})['enabled'],
                "dont_use_metered_network": self._automatic_pattern.get('dontUseMeteredNetwork',
                                                                        {'enabled': False})['enabled'],
                "ac_power": self._automatic_pattern.get('acPower',
                                                        {'enabled': False})['enabled'],
                "stop_if_on_battery": self._automatic_pattern.get('stopIfOnBattery',
                                                                  {'enabled': False})['enabled'],
                "stop_sleep_if_runningjob": self._automatic_pattern.get('stopSleepIfBackUp',
                                                                        {'enabled': False})['enabled'],
                "cpu_utilization_below": self._automatic_pattern.get('cpuUtilization',
                                                                     {'enabled': False})['enabled'],
                "cpu_utilization_above": self._automatic_pattern.get('cpuUtilizationAbove',
                                                                     {'enabled': False})['enabled'],
                "run_synthetic_full": 'every_x_days'
            }

            if ('useAutomaticIntervalForSyntheticFull' in self._automatic_pattern and
                    self._automatic_pattern['useAutomaticIntervalForSyntheticFull']):
                pattern['run_synthetic_full'] = 'extended_retention'

            if ('enableRunFullConsolidationBackup' in self._automatic_pattern and
                    self._automatic_pattern['enableRunFullConsolidationBackup']):
                pattern['run_synthetic_full'] = 'space_reclaim'

            if ('daysBetweenSyntheticBackup' in self._automatic_pattern and
                    self._automatic_pattern['daysBetweenSyntheticBackup']):
                pattern['days_between_synthetic_full'] = self._automatic_pattern[
                    'daysBetweenSyntheticBackup']

            return pattern
        return False

    @automatic.setter
    def automatic(self, pattern_dict: dict) -> None:
        """
        sets the pattern type as one time with the parameters provided,
                send only required keys to change only those values
                Args:
                     pattern_dict (dict): Dictionary with the schedule pattern
                        {
                             min_interval_hours: minimum hours between jobs(int)
                             min_interval_minutes: minimum minutes between jobs(int)
                             max_interval_hours: maximum hours between jobs(int)
                             max_interval_minutes: maximum minutes between jobs(int)
                             min_sync_interval_hours: minimum sync hours
                                                                    between jobs(int)
                             min_sync_interval_minutes: minimum sync minutes
                                                                    between jobs(int)
                             ignore_opwindow_past_maxinterval: (bool)
                             wired_network_connection: (bool)
                             min_network_bandwidth: (int) kbps
                             specific_network: (dict){ip_address:(str),subnet:(int)}
                             dont_use_metered_network: (bool)
                             ac_power: (bool)
                             stop_if_on_battery: (bool)
                             stop_sleep_if_runningjob: (bool)
                             cpu_utilization_below : (int)%
                             cpu_utilization_above : (int)%
                             run_synthetic_full : (str: every_x_days/extended_retention/
                             space_reclaim)
                             days_between_synthetic_full : (int)
                        }
        """
        if isinstance(pattern_dict, bool):
            pattern_dict = {}
        pattern_dict['freq_type'] = 'automatic'
        schedule_pattern = SchedulePattern(self._automatic_pattern)
        self._pattern = {"freq_type": 1024}
        if 'commonOpts' in self._task_options:
            self._task_options["commonOpts"]["automaticSchedulePattern"] = \
                schedule_pattern.create_schedule_pattern(pattern_dict)
        else:
            self._task_options["commonOpts"] = \
                {"automaticSchedulePattern": schedule_pattern.create_schedule_pattern(
                    pattern_dict)}

        if 'run_synthetic_full' in pattern_dict:
            synthetic_pattern = pattern_dict['run_synthetic_full']

            if synthetic_pattern == 'every_x_days':
                synthetic_interval = pattern_dict.get(
                    'days_between_synthetic_full', 30)
            else:
                synthetic_interval = 30

            _data_opt = {
                'autoCopy': True,
                'daysBetweenSyntheticBackup': synthetic_interval,
                'useAutomaticIntervalForSyntheticFull': (
                        synthetic_pattern == 'extended_retention'),
                'enableRunFullConsolidationBackup': (
                        synthetic_pattern == 'space_reclaim')
            }

            if 'backupOpts' in self._task_options:
                if 'dataOpt' in self._task_options["backupOpts"]:
                    self._task_options['backupOpts']['dataOpt'].update(_data_opt)
                else:
                    self._task_options['backupOpts']['dataOpt'] = _data_opt
            else:
                self._task_options['backupOpts'] = {
                    'dataOpt': _data_opt
                }

        self._modify_task_properties()

    @property
    def active_start_date(self) -> str:
        """
        gets the start date of the schedule
        Returns:
            (str): date in %m/%d/%Y
        """
        return SchedulePattern._time_converter(
            self._pattern['active_start_date'], '%m/%d/%Y', False)

    @active_start_date.setter
    def active_start_date(self, active_start_date: str) -> None:
        """
        sets the start date of the schedule
        Args:
            active_start_date (str): date in %m/%d/%Y
        """
        pattern_dict = dict()
        pattern_dict['freq_type'] = self.schedule_freq_type
        pattern_dict['active_start_date'] = active_start_date
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def active_start_time(self) -> str:
        """
        gets the start time of the schedule
        Returns:
            (str): time in %H/%S
        """
        return SchedulePattern._time_converter(
            self._pattern['active_start_time'], '%H:%M', False)

    @active_start_time.setter
    def active_start_time(self, active_start_time: str) -> None:
        """
        sets the start time of the schedule
        Args:
            active_start_time (str): time in %H/%S
        """
        pattern_dict = dict()
        pattern_dict['freq_type'] = self.schedule_freq_type
        pattern_dict['active_start_time'] = active_start_time
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def active_end_date(self) -> str:
        """
        gets the end date of the schedule if present
        Returns:
            (str): date in %m/%d/%Y
        """
        if "active_end_date" in self._pattern:
            if self._pattern["active_end_date"]:
                return SchedulePattern._time_converter(
                    self._pattern['active_end_date'], '%m/%d/%Y', False)
        return False

    @active_end_date.setter
    def active_end_date(self, active_start_date: str) -> None:
        """
        sets the end date for the schedule
        Args:
            active_start_date (str): date in %m/%d/%Y
        """
        pattern_dict = dict()
        pattern_dict['freq_type'] = self.schedule_freq_type
        pattern_dict['active_end_date'] = active_start_date
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def exception_dates(self) -> list:
        """
        returns a list of exception days if present
        Returns:
            (list): exception days in a schedule
        """
        if "repeatPattern" in self._pattern:
            for repeat_pattern in self._pattern["repeatPattern"]:
                if repeat_pattern.get("exception"):
                    _on_day_number = repeat_pattern.get("onDayNumber")
                    day = 1
                    exceptions = []
                    while day <= 31 and _on_day_number != 0:
                        if _on_day_number & 1 == 1:
                            exceptions.append(day)
                        _on_day_number = _on_day_number >> 1
                        day += 1
                    return exceptions
        return False

    @exception_dates.setter
    def exception_dates(self, day_list: list) -> None:
        """
        sets exception days provided as input for the schedule
        Args:
            day_list (list): exception days to set for the schedule
        """
        pattern_dict = dict()
        pattern_dict['freq_type'] = self.schedule_freq_type
        pattern_dict['exception_dates'] = day_list
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def end_after(self) -> int:
        """
        gets the maximum occurence of the schedule if present
        Returns:
            (int): end occurence
        """
        return self._pattern.get("active_end_occurence", False)

    @end_after.setter
    def end_after(self, end_after: int) -> None:
        """
        sets the end date for the schedule
        Args:
            end_after (int): number of times the schedule should run
        """
        pattern_dict = dict()
        pattern_dict['freq_type'] = self.schedule_freq_type
        pattern_dict['end_after'] = end_after
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_dict)
        self._modify_task_properties()

    @property
    def repeat_pattern(self) -> dict:
        """
        gets the repeat pattern in a schedule if present
        Returns:
            (dict): the repeat pattern
                {
                    "repeat_every": repeat_every,
                    "repeat_end": repeat_end
                    }
        """

        if self._pattern.get("freq_subday_interval", 0):
            _subday_interval = self._pattern["freq_subday_interval"]
            repeat_every = "{0}:0{1}".format(int(_subday_interval / 3600), int(
                ((_subday_interval / 60) - ((_subday_interval / 3600) * 60))))
            repeat_end = SchedulePattern._time_converter(
                self._pattern["active_end_time"], "%H:%M", utc_to_epoch=False)
            return {
                "repeat_every": repeat_every,
                "repeat_end": repeat_end
            }
        return False

    @repeat_pattern.setter
    def repeat_pattern(self, pattern_json: dict) -> None:
        """
        sets a repeat pattern for the schedule
        Args:
            pattern_json (Dict): containing the repeat every and repeat end parameters
        """
        pattern_json['freq_type'] = self.schedule_freq_type
        schedule_pattern = SchedulePattern(self._pattern)
        self._pattern = schedule_pattern.create_schedule_pattern(pattern_json)
        self._modify_task_properties()

    def run_now(self, return_multiple_jobs: bool = False) -> str:
        """
        Triggers the schedule to run immediately

        Args:
            return_multiple_jobs (bool): if set to True, return multiple jobs, default: False.

        Returns:
            job id/ Job IDs.

        Raises:
            SDKException:
                Response received is empty.
                If no job id is found.

        Usage:
            schedule.run_now()
            schedule.run_now(return_multiple_jobs=True)
        """
        request_json = {
            "TMMsg_TaskOperationReq":
                {
                    "opType": 5,
                    "subtaskEntity":
                        [
                            {
                                "_type_": 68,
                                "subtaskId": self.subtask_id,
                                "taskName": "",
                                "subtaskName": self.schedule_name,
                                "taskId": self.task_id
                            }
                        ],
                    "taskIds":
                        [
                            self.task_id
                        ]
                }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._MODIFYSCHEDULE, request_json
        )
        if response.json():
            if "jobIds" in response.json():
                if(return_multiple_jobs):
                    job_id = [int(i) for i in response.json()['jobIds']]
                else:
                    job_id = str(response.json()["jobIds"][0])

                return job_id
            else:
                raise SDKException(
                    'Response', '102', 'JobID not found in response')
        else:
            raise SDKException('Response', '102')

    def _modify_task_properties(self) -> None:
        """Modifies the task properties of the schedule.

        Raises:
            SDKException: if modification of the schedule failed.

        Usage:
            schedule._modify_task_properties()
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

                                        'subTask': self._sub_task_option,
                                        'pattern': self._pattern,
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
        self.refresh()

        if output[0]:
            return

        o_str = 'Failed to update properties of Schedule\nError: "{0}"'
        raise SDKException('Schedules', '102', o_str.format(output[2]))

    def enable(self) -> None:
        """Enable a schedule.

        Raises:
            SDKException: if failed to enable schedule, if response is empty, or if response is not success.

        Usage:
            schedule.enable()
        """
        enable_request = self._commcell_object._services['ENABLE_SCHEDULE']
        request_text = "taskId={0}".format(self.task_id)

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
                            'Schedules',
                            '102',
                            'Failed to enable Schedule\nError: "{0}"'.format(error_message))
                    else:
                        raise SDKException(
                            'Schedules', '102', "Failed to enable Schedule")
            else:
                raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def disable(self) -> None:
        """Disable a Schedule.

        Raises:
            SDKException: if failed to disable Schedule, if response is empty, or if response is not success.

        Usage:
            schedule.disable()
        """
        disable_request = self._commcell_object._services['DISABLE_SCHEDULE']

        request_text = "taskId={0}".format(self.task_id)

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
                            'Schedules',
                            '102',
                            'Failed to disable Schedule\nError: "{0}"'.format(error_message))
                    else:
                        raise SDKException(
                            'Schedules', '102', "Failed to disable Schedule")
            else:
                raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def _process_schedule_update_response(self, flag: bool, response: Any) -> Tuple[bool, str, str]:
        """Processes the response received post update request.

        Args:
            flag (bool): True or false based on response.
            response (Any): Response from modify request.

        Returns:
            Tuple[bool, str, str]:
                - bool: Based on success and failure.
                - str: Error code from response.
                - str: Error message from the response if any.

        Raises:
            SDKException: if the response is empty.

        Usage:
            flag, error_code, error_message = schedule._process_schedule_update_response(True, response)
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

        response_string = self._commcell_object._update_response_(
            response.text)
        raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Refresh the properties of the Schedule.

        Usage:
            schedule.refresh()
        """
        self._get_schedule_properties()
