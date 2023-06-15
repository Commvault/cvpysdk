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

"""File for performing Operation Window related operations on given Commcell entity.

OperationWindow and OperationWindowDetails are 2 classes defined in this class.

OperationWindow: Class for performing Operation Window related operations on given Commcell entity.

OperationWindowDetails: Class for modifying an existing operation window


OperationWindow:
===============

    __init__()                          --  Initialize instance of the OperationWindow class

    create_operation_window()           --  Creates a Operation rule on the given commcell entity

    delete_operation_window()           --  Deletes a Operation rule on the commcell entity(Using rule_id/name)

    list_operation_window()             --  Lists all the operation rule associated with given commcell entity

    get()                               --  Returns instance of OperationWindowDetails class(Using rule_id/name)

OperationWindowDetails:
======================

    __init__()                          --  Initialize instance of OperationWindowDetails class

    modify_operation_window()           --  Modifies a Operation window

    _refresh()                          --  Refreshes the properties of a rule


    _get_rule_properties()              -- Assigns the properties of an operation by getting the rule using rule id


OperationWindowDetails Instance Attributes:
==========================================
    **name**                            --  Returns/Modifies the name of the operation window

    **start_date**                      --  Returns/Modifies the start date of the operation window

    **end_date**                        --  Returns/Modifies the end date of the operation window

    **operations**                      --  Returns/Modifies the operations of the operation window

    **day_of_week**                     --  Returns/Modifies the day of week of the operation window

    **start_time**                      --  Returns/Modifies the start time of the operation window

    **end_time**                        --  Returns/Modifies the end time of the operation window

    **rule_id**                         --  Returns rule id of the operation window

    **commcell_id**                     --  Returns commcell id of the entity object

    **clientgroup_id**                  --  Returns client group id of the entity object

    **client_id**                       --  Returns client id of the entity object

    **agent_id**                        --  Returns agent id of the entity object

    **instance_id**                     --  Returns instance id of the entity object

    **backupset_id**                    --  Returns backupset id of the entity object

    **subclient_id**                    --  Returns subclient id of the entity object

    **entity_level**                    --  Returns entity level of the entity object

Example with client entity:
        from cvpysdk.commcell import Commcell
        commcell = Commcell(<CS>, username, password)
        client = commcell.clients.get(<client Name>)
        from cvpysdk.operation_window import OperationWindow
        client_operation_window = OperationWindow(client)
        client_operation_window.list_operation_window()
        client_operation_window_details = client_operation_window.create_operation_window(name="operation
                                                                                        window example on clientLevel")
        client_operation_window.delete_operation_window(rule_id=client_operation_window_details.rule_id)
        client_operation_window_details = client_operation_window.get(rule_id=client_operation_window_details.rule_id)
        client_operation_window_details.modify_operation_window(name="Modified operation window example on clientLevel")

Example for modifying a rule:
        client_operation_window = OperationWindow(client)
        rules = client_operation_window.list_operation_window()
        ruleId = rules[0]['ruleId']
        client_operation_window_details = OperationWindowDetails(client, ruleId, client_operation_window.entity_details)
        # You can use get(OperationWindow) method to modify a rule too.
        client_operation_window_details.modify_operation_window(name="Modified operation window example on clientLevel")
"""

from __future__ import absolute_import
import time
import datetime
import calendar
from datetime import timedelta
from .exception import SDKException
from .clientgroup import ClientGroup
from .client import Client
from .agent import Agent
from .instance import Instance
from .backupset import Backupset
from .subclient import Subclient

DAY_OF_WEEK_MAPPING = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
WEEK_OF_THE_MONTH_MAPPING = {"all": 32,
                             "first": 1,
                             "second": 2,
                             "third": 4,
                             "fourth": 8,
                             "last": 16}
OPERATION_MAPPING = {"FULL_DATA_MANAGEMENT": 1,
                     "NON_FULL_DATA_MANAGEMENT": 2,
                     "SYNTHETIC_FULL": 4,
                     "DATA_RECOVERY": 8,
                     "AUX_COPY": 16,
                     "DR_BACKUP": 32,
                     "DATA_VERIFICATION": 64,
                     "ERASE_SPARE_MEDIA": 128,
                     "SHELF_MANAGEMENT": 256,
                     "DELETE_DATA_BY_BROWSING": 512,
                     "DELETE_ARCHIVED_DATA": 1024,
                     "OFFLINE_CONTENT_INDEXING": 2048,
                     "ONLINE_CONTENT_INDEXING": 4096,
                     "SRM": 8192,
                     "INFORMATION_MANAGEMENT": 16384,
                     "MEDIA_REFRESHING": 32768,
                     "DATA_ANALYTICS": 65536,
                     "DATA_PRUNING": 131072,
                     "BACKUP_COPY": 262144,
                     "CLEANUP_OPERATION": 524288,
                     "ALL": 1048576}


class OperationWindow:
    """Class for representing all operation window related operations"""

    def __init__(self, generic_entity_obj):
        """Initialize the OperationWindow class instance for
           performing Operation Window related operations.

            Args:
                generic_entity_obj     (object)    --  Commcell entity object
                    Expected value : commcell/Client/Agent/Instance/BackupSet/Subclient/Clientgroup Instance

            Returns:
                object  -   instance of the OperationWindow class

            Raises:
                Exception:
                    If invalid instance is passed
        """
        # imports inside the __init__ method definition to avoid cyclic imports
        from .commcell import Commcell

        if isinstance(generic_entity_obj, Commcell):
            self._commcell_object = generic_entity_obj
        else:
            self._commcell_object = generic_entity_obj._commcell_object

        self._commcell_services = self._commcell_object._services
        self._operation_window = self._commcell_services['OPERATION_WINDOW']
        self._list_operation_window = self._commcell_services['LIST_OPERATION_WINDOW']
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._update_response = self._commcell_object._update_response_

        self.clientgroup_id = 0
        self.client_id = 0
        self.agent_id = 0
        self.instance_id = 0
        self.backupset_id = 0
        self.subclient_id = 0
        self.entity_type = ''
        self.entity_id = ''
        self.entity_details = dict()

        self.generic_entity_obj = generic_entity_obj

        # we will derive all the entity id's based on the input entity type
        if isinstance(generic_entity_obj, Commcell):
            self.entity_details["entity_level"] = "commserv"
        elif isinstance(generic_entity_obj, ClientGroup):
            self.clientgroup_id = generic_entity_obj.clientgroup_id
            self.entity_type = "clientgroupId"
            self.entity_id = self.clientgroup_id
            self.entity_details["entity_level"] = self.entity_type[:-2]
        elif isinstance(generic_entity_obj, Client):
            self.client_id = generic_entity_obj.client_id
            self.entity_type = "clientId"
            self.entity_id = self.client_id
            self.entity_details["entity_level"] = self.entity_type[:-2]
        elif isinstance(generic_entity_obj, Agent):
            self.client_id = generic_entity_obj._client_object.client_id
            self.agent_id = generic_entity_obj.agent_id
            self.entity_type = "applicationId"
            self.entity_id = self.agent_id
            self.entity_details["entity_level"] = "agent"
        elif isinstance(generic_entity_obj, Instance):
            self.client_id = generic_entity_obj._agent_object._client_object.client_id
            self.agent_id = generic_entity_obj._agent_object.agent_id
            self.instance_id = generic_entity_obj.instance_id
            self.entity_type = "instanceId"
            self.entity_id = self.instance_id
            self.entity_details["entity_level"] = self.entity_type[:-2]
        elif isinstance(generic_entity_obj, Backupset):
            self.client_id = generic_entity_obj._instance_object._agent_object. \
                _client_object.client_id
            self.agent_id = generic_entity_obj._instance_object._agent_object.agent_id
            self.instance_id = generic_entity_obj._instance_object.instance_id
            self.backupset_id = generic_entity_obj.backupset_id
            self.entity_type = "backupsetId"
            self.entity_id = self.backupset_id
            self.entity_details["entity_level"] = self.entity_type[:-2]
        elif isinstance(generic_entity_obj, Subclient):
            self.client_id = generic_entity_obj._backupset_object._instance_object. \
                _agent_object._client_object.client_id
            self.agent_id = generic_entity_obj._backupset_object. \
                _instance_object._agent_object.agent_id
            self.instance_id = generic_entity_obj._backupset_object._instance_object.instance_id
            self.backupset_id = generic_entity_obj._backupset_object.backupset_id
            self.subclient_id = generic_entity_obj.subclient_id
            self.entity_type = "subclientId"
            self.entity_id = self.subclient_id
            self.entity_details["entity_level"] = self.entity_type[:-2]
        else:
            raise SDKException('Response', '101', "Invalid instance passed")

        self.entity_details.update({"clientGroupId": self.clientgroup_id,
                                    "clientId": self.client_id,
                                    "applicationId": self.agent_id,
                                    "instanceId": self.instance_id,
                                    "backupsetId": self.backupset_id,
                                    "subclientId": self.subclient_id})

        # append the entity type and entity id to end of list operation window REST API.
        # For commcell it will empty string
        self.connect_string = self._list_operation_window.split('?')[0] + '?' + self.entity_type + "=" + self.entity_id

    def create_operation_window(
            self,
            name,
            start_date=None,
            end_date=None,
            operations=None,
            day_of_week=None,
            start_time=None,
            end_time=None,
            week_of_the_month=None,
            do_not_submit_job=False):
        """ Creates operation rule on the initialized commcell entity

            Args:
                name          (str)   --  Name of the Operation rule

                start_date    (int)   -- The start date for the operation rule.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - current date

                end_date      (int)   -- The end date for the operation rule.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 365 days

                operations (list)         --   List of operations for which the operation
                                               window is created

                    Acceptable Values:
                        FULL_DATA_MANAGEMENT/NON_FULL_DATA_MANAGEMENT/SYNTHETIC_FULL/
                        DATA_RECOVERY/AUX_COPY/DR_BACKUP/DATA_VERIFICATION/ERASE_SPARE_MEDIA/
                        SHELF_MANAGEMENT/DELETE_DATA_BY_BROWSING/DELETE_ARCHIVED_DATA/
                        OFFLINE_CONTENT_INDEXING/ONLINE_CONTENT_INDEXING/SRM/INFORMATION_MANAGEMENT/
                        MEDIA_REFRESHING/DATA_ANALYTICS/DATA_PRUNING/BACKUP_COPY/CLEANUP_OPERATION

                week_of_the_month(list)     -- List of week of the month on which the operation rule applies to
                        Acceptable Values:
                            all/first/second/third/fourth/last

                            default - None

                day_of_week (list)    -- List of days of the week on which the operation rule applies to
                    Acceptable Values:
                        sunday/ monday/ tuesday/ wednesday/ thursday/ friday/ saturday

                    default- Weekdays

                start_time  (int)     -- The start time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 28800 (8 AM)
                    Must specify one timestamp for start time for all the weekdays, otherwise
                    make a list for each weekday mentioned in the day_of_week list.

                start_time (list)    -- The list of start timestamps for each weekday mentioned
                    in the day_of_week list.

                end_time    (int)     -- The end time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 86400 (6 PM)
                    Must specify one timestamp for end time for all the weekdays, otherwise
                    make a list for each weekday mentioned in the day_of_week list.

                end_time   (list)    -- The list of end timestamps for each weekday mentioned
                    in the day_of_week list.

                Example:
                    1. day_of_week : ["sunday", "thursday", "saturday"]
                       start_time  : 28800
                       end_time    : 86400
                       The above inputs specify that for all the three days mentioned, start_time and end_time of
                       operation window would be same
                    2. day_of_week : ["monday","friday"]
                       start_time  : [3600, 28800]
                       end_time    : [18000, 86400]
                       The above input specify that on monday operation window starts at 3600 and ends at 18000 whereas
                       on friday, the operation window starts at 28800 and ends at 86400

                do_not_submit_job   (bool) -- doNotSubmitJob of the operation rule

            Returns:
                Returns the instance of created Operation window details

            Raises:
                SDKException:
                    if the Operation window could not be created

                    if response is empty

                    if response is not success

        """
        if start_date is None:
            start_date = int(calendar.timegm(datetime.date.today().timetuple()))
        if end_date is None:
            end_date = start_date
        if start_time is None:
            start_time = int(timedelta(hours=8).total_seconds())
        if end_time is None:
            end_time = int(timedelta(hours=18).total_seconds())

        operations_list = []
        if operations is None:
            operations_list = [OPERATION_MAPPING["FULL_DATA_MANAGEMENT"]]
        else:
            for operation in operations:
                if operation not in OPERATION_MAPPING:
                    response_string = "Invalid input %s for operation is passed" % operation
                    raise SDKException('OperationWindow', '102', response_string)
                operations_list.append(OPERATION_MAPPING[operation.upper()])

        day_of_week_list = []
        if day_of_week is None:
            day_of_week_list = [1, 2, 3, 4, 5]      # defaults to weekdays
        else:
            for day in day_of_week:
                if day.lower() not in DAY_OF_WEEK_MAPPING:
                    response_string = "Invalid input value %s for day_of_week" % day
                    raise SDKException('OperationWindow', '102', response_string)
                day_of_week_list.append(DAY_OF_WEEK_MAPPING.index(day.lower()))

        week_of_the_month_list = []
        if week_of_the_month:
            for week in week_of_the_month:
                if week.lower() not in WEEK_OF_THE_MONTH_MAPPING:
                    response_string = "Invalid input %s for week_of_the_month" % week
                    raise SDKException('OperationWindow', '102', response_string)
                week_of_the_month_list.append(WEEK_OF_THE_MONTH_MAPPING[week.lower()])

        daytime_list = []
        num_of_days = len(day_of_week_list)
        if isinstance(start_time, int) and isinstance(end_time, int):
            daytime_list.append(
                {
                    "startTime": start_time,
                    "endTime": end_time,
                    "weekOfTheMonth": week_of_the_month_list,
                    "dayOfWeek": day_of_week_list
                }
            )
        elif isinstance(start_time, list) and isinstance(end_time, list):
            if not(num_of_days == len(start_time) == len(end_time)):
                response_string = "did not specify start time and end time for all the given week days"
                raise SDKException('OperationWindow', '102', response_string)
            for week_day in range(num_of_days):
                daytime_list.append(
                    {
                        "startTime": start_time[week_day],
                        "endTime": end_time[week_day],
                        "weekOfTheMonth": week_of_the_month_list,
                        "dayOfWeek": [day_of_week_list[week_day]]
                    }
                )
        else:
            response_string = "Both start_time and end_time should be of same type."
            raise SDKException('OperationWindow', '102', response_string)

        payload = {
            "operationWindow": {
                "ruleEnabled": True,
                "doNotSubmitJob": do_not_submit_job,
                "startDate": start_date,
                "endDate": end_date,
                "name": name,
                "operations": operations_list,
                "dayTime": daytime_list
            },
            "entity": {
                "clientGroupId": int(self.clientgroup_id),
                "clientId": int(self.client_id),
                "applicationId": int(self.agent_id),
                "instanceId": int(self.instance_id),
                "backupsetId": int(self.backupset_id),
                "subclientId": int(self.subclient_id)
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._operation_window, payload=payload)
        if flag:
            if response.json():
                error_code = response.json().get("error", {}).get('errorCode')
                if int(error_code) == 0:
                    return self.get(rule_id=int(response.json().get('operationWindow', {}).get('ruleId')))
                raise SDKException('OperationWindow', '101')
            raise SDKException('Response', '102')
        response_string = self._update_response(response.text)
        raise SDKException('Response', '102', response_string)

    def delete_operation_window(self, rule_id=None, name=None):
        """Deletes the operation rule associated with given rule Id/Name.

            Args:
                rule_id       (int)   --  Rule Id of the operation window

                name           (str)   --  Name of the operation window

            Raises:
                SDKException:
                    if the Operation window could not be deleted

                    if response is empty

                    if response is not success

        """

        if not name and not rule_id:
            raise SDKException(
                'OperationWindow',
                '102',
                'Either Name or Rule Id is needed')

        if name and not isinstance(name, str) or rule_id and not isinstance(rule_id, int):
            raise SDKException('OperationWindow', '106')

        if name:
            rule_id = self.get(name=name).rule_id

        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._operation_window + '/' + str(rule_id))
        if flag:
            if response.json():
                error_code = response.json().get("error", {}).get('errorCode')
                if int(error_code):
                    raise SDKException('OperationWindow', '103')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response(
                response.text)
            raise SDKException('Response', '102', response_string)

    def list_operation_window(self):
        """Lists the operation rules for the associated commcell entity.

            Returns:
                Returns the List of operation rules (dictionary) associated with given commcell entity

                Example --

                    [{'ruleEnabled': True,
                      'doNotSubmitJob': False,
                      'endDate': 0,
                      'level': 0,
                      'name': 'Rule1',
                      'ruleId': 1,
                      'startDate': 0,
                      'operations': ['FULL_DATA_MANAGEMENT', 'NON_FULL_DATA_MANAGEMENT'],
                      'company': {'_type_': 61,
                                  'providerId': 0,
                                  'providerDomainName': ''},
                      'dayTime': [{'startTime': 28800,
                                   'endTime': 64800,
                                   'weekOfTheMonth': ['first','third'],
                                   'dayOfWeek': ['sunday','monday']}]}
                    ]

            Raises:
                SDKException:
                    if the Operation rules could not be Listed

                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self.connect_string)
        if flag:
            if response.json():
                error_code = response.json().get("error", {}).get('errorCode')
                if int(error_code) == 0:
                    list_of_rules = response.json().get("operationWindow")
                    operation_reverse_mapping = {value: key for key, value in OPERATION_MAPPING.items()}
                    wotm_reverse_mapping = {value: key for key, value in WEEK_OF_THE_MONTH_MAPPING.items()}
                    if list_of_rules is not None:
                        for operation_rule in list_of_rules:
                            operations = operation_rule.get("operations")
                            if operations is not None:
                                operation_rule["operations"] = [operation_reverse_mapping[operation] for operation in
                                                                operations]
                            day_time_list = operation_rule.get("dayTime", [])
                            for day_time in day_time_list:
                                if day_time.get("weekOfTheMonth"): # if we have weekOfTheMonth, we replace it with name.
                                    day_time['weekOfTheMonth'] = [wotm_reverse_mapping[week] for week in day_time.get("weekOfTheMonth")]

                                if day_time.get("dayTime"): # if we have dayTime, we replace it with name.
                                    day_time['dayTime'] = [DAY_OF_WEEK_MAPPING[day] for day in day_time['dayTime']]
                            operation_rule['dayTime'] = day_time_list
                    return list_of_rules
                raise SDKException('OperationWindow', '104')
            raise SDKException('Response', '102')
        response_string = self._update_response(response.text)
        raise SDKException('Response', '102', response_string)

    def get(self, rule_id=None, name=None):
        """Returns the operation rule object for a given rule

         Args:
            rule_id               (int)   --  Rule Id of an operation Window

            name                  (str)   --  Name of the operation window

         Returns:
                object - instance of the OperationWindowDetails class
                            for the given operation window name/rule
         Raises:
                SDKException:
                    if type of the operation window name argument is not string

                    if no operation window exists with such name
        """
        if not name and not rule_id:
            raise SDKException(
                'OperationWindow',
                '102',
                'Either Name or Rule Id is needed')

        if name and not isinstance(name, str) or rule_id and not isinstance(rule_id, int):
            raise SDKException('OperationWindow', '106')

        list_of_rules = self.list_operation_window()
        if rule_id:
            for operation_rule in list_of_rules:
                if operation_rule.get("ruleId") == rule_id:
                    return OperationWindowDetails(self.generic_entity_obj, rule_id, self.entity_details)
            raise Exception("No such operation window with rule id as {0} exists".format(rule_id))
        if name:
            rules = [operation_rule.get("ruleId") for operation_rule in list_of_rules
                     if operation_rule.get("name") == name]
            if not rules:
                raise Exception("No such operation window with name as {0} exists".format(name))
            if len(rules) == 1:
                return OperationWindowDetails(self.generic_entity_obj, rules[0], self.entity_details)
            raise Exception("More than one operation window are named as {0} exists".format(name))


class OperationWindowDetails:
    """Helper class for modifying operation window"""

    def __init__(self, generic_entity_obj, rule_id, entity_details):
        """
        Initialize the OperationWindowDetails class instance for
           modifying OperationWindow.

            Args:
                generic_entity_obj     (object)    --  Commcell entity object
                    Expected value : commcell/Client/Agent/Instance/BackupSet/Subclient/Clientgroup Entity

                rule_id (int)   -- Rule id of the operation window to be modified

                entity_details -- Details related to the entity

            Usually gets initialized from OperationWindow class

            Returns:
                object  -   instance of the OperationWindowDetails class
        """
        from .commcell import Commcell
        if isinstance(generic_entity_obj, Commcell):
            self._commcell_object = generic_entity_obj
        else:
            self._commcell_object = generic_entity_obj._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._update_response = self._commcell_object._update_response_
        self._commcell_services = self._commcell_object._services
        self._operation_window = self._commcell_services['OPERATION_WINDOW']

        self._rule_id = rule_id
        self._name = None
        self._start_date = None
        self._end_date = None
        self._operations = None
        self._week_of_the_month = None
        self._day_of_week = None
        self._start_time = None
        self._end_time = None
        self._do_not_submit_job = False

        self._commcell_id = self._commcell_object.commcell_id
        self._clientgroup_id = entity_details["clientGroupId"]
        self._client_id = entity_details["clientId"]
        self._agent_id = entity_details["applicationId"]
        self._instance_id = entity_details["instanceId"]
        self._backupset_id = entity_details["backupsetId"]
        self._subclient_id = entity_details["subclientId"]
        self._entity_level = entity_details["entity_level"]

        self._refresh()

    def modify_operation_window(self, **modify_options):
        """Modifies the Operation rule.

            Args:
                modify_options(dict)  -- Arbitrary keyword arguments.

                modify_options Args:
                    name          (str)   --  Name of the Operation rule

                    start_date    (int)   -- The start date for the operation rule.
                        Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                        default - current date

                    end_date      (int)   -- The end date for the operation rule.
                        Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                        default - 365 days

                    operations (list)         --   List of operations for which the operation
                                                   window is created

                        Acceptable Values:
                            FULL_DATA_MANAGEMENT/NON_FULL_DATA_MANAGEMENT/SYNTHETIC_FULL/
                            DATA_RECOVERY/AUX_COPY/DR_BACKUP/DATA_VERIFICATION/ERASE_SPARE_MEDIA/
                            SHELF_MANAGEMENT/DELETE_DATA_BY_BROWSING/DELETE_ARCHIVED_DATA/
                            OFFLINE_CONTENT_INDEXING/ONLINE_CONTENT_INDEXING/SRM/INFORMATION_MANAGEMENT/
                            MEDIA_REFRESHING/DATA_ANALYTICS/DATA_PRUNING/BACKUP_COPY/CLEANUP_OPERATION

                    week_of_the_month(list)     -- List of week of the month on which the operation rule applies to
                        Acceptable Values:
                            all/first/second/third/fourth/last

                            default - None

                    day_of_week (list)    -- List of days of the week on which the operation rule applies to
                        Acceptable Values:
                            sunday/ monday/ tuesday/ wednesday/ thursday/ friday/ saturday

                        default- Weekdays

                    start_time  (int)     -- The start time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 28800 (8 AM)
                    Must specify one timestamp for start time for all the weekdays, otherwise
                    make a list for each weekday mentioned in the day_of_week list.

                start_time (list)    -- The list of start timestamps for each weekday mentioned
                    in the day_of_week list.

                end_time    (int)     -- The end time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 86400 (6 PM)
                    Must specify one timestamp for end time for all the weekdays, otherwise
                    make a list for each weekday mentioned in the day_of_week list.

                end_time   (list)    -- The list of end timestamps for each weekday mentioned
                    in the day_of_week list.

                Example:
                    1. day_of_week : ["sunday", "thursday", "saturday"]
                       start_time  : 28800
                       end_time    : 86400
                       The above inputs specify that for all the three days mentioned, start_time and end_time of
                       operation window would be same
                    2. day_of_week : ["monday","friday"]
                       start_time  : [3600, 28800]
                       end_time    : [18000, 86400]
                       The above input specify that on monday operation window starts at 3600 and ends at 18000 whereas
                       on friday, the operation window starts at 28800 and ends at 86400

                    do_not_submit_job   (bool)  -- doNotSubmitJob of the operation rule

            Raises:
                SDKException:
                    if the Operation window could not be Modified

                    if response is empty

                    if response is not success


        """
        start_date = modify_options.get("start_date", self.start_date)
        end_date = modify_options.get("end_date", self.end_date)
        start_time = modify_options.get("start_time", self.start_time)
        end_time = modify_options.get("end_time", self.end_time)
        name = modify_options.get("name", self.name)
        operations = modify_options.get("operations", self.operations)
        week_of_the_month = modify_options.get("week_of_the_month", self.week_of_the_month)
        day_of_week = modify_options.get("day_of_week", self.day_of_week)
        do_not_submit_job = modify_options.get("do_not_submit_job", self.do_not_submit_job)

        if not operations:
            # Empty list can be passed
            operations_list = operations
        else:
            operations_list = [OPERATION_MAPPING[operation.upper()] for operation in operations]

        week_of_the_month_list = []
        if week_of_the_month:
            week_of_the_month_list = [WEEK_OF_THE_MONTH_MAPPING[week.lower()] for week in week_of_the_month]

        day_of_week_list = [DAY_OF_WEEK_MAPPING.index(day.lower()) for day in day_of_week]
        daytime_list = []
        num_of_days = len(day_of_week_list)
        if isinstance(start_time, int) and isinstance(end_time, int):
            daytime_list.append(
                {
                    "startTime": start_time,
                    "endTime": end_time,
                    "weekOfTheMonth": week_of_the_month_list,
                    "dayOfWeek": day_of_week_list
                }
            )
        elif isinstance(start_time, list) and isinstance(end_time, list):
            if not (num_of_days == len(start_time) == len(end_time)):
                response_string = "did not specify start time and end time for all the given week days"
                raise SDKException('OperationWindow', '102', response_string)
            for week_day in range(num_of_days):
                daytime_list.append(
                    {
                        "startTime": start_time[week_day],
                        "endTime": end_time[week_day],
                        "weekOfTheMonth": week_of_the_month_list,
                        "dayOfWeek": [day_of_week_list[week_day]]
                    }
                )
        else:
            response_string = "Both start_time and end_time should be of same type."
            raise SDKException('OperationWindow', '102', response_string)
        payload = {
            "operationWindow": {
                "ruleEnabled": True,
                "doNotSubmitJob": do_not_submit_job,
                "startDate": start_date,
                "endDate": end_date,
                "name": name,
                "ruleId": int(self.rule_id),
                "operations": operations_list,
                "dayTime": daytime_list
            },
            "entity": {
                "clientGroupId": int(self._clientgroup_id),
                "clientId": int(self._client_id),
                "applicationId": int(self._agent_id),
                "instanceId": int(self._instance_id),
                "backupsetId": int(self._backupset_id),
                "subclientId": int(self._subclient_id)
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._operation_window, payload=payload)
        if flag:
            if response.json():
                error_code = response.json().get("error", {}).get('errorCode')
                if int(error_code) == 0:
                    int(response.json().get('operationWindow', {}).get('ruleId'))
                    self._refresh()
                else:
                    raise SDKException('OperationWindow', '105')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response(response.text)
            raise SDKException('Response', '101', response_string)

    def _refresh(self):
        """Refreshes the properties of a rule"""
        self._get_rule_properties()

    def _get_rule_properties(self):
        """
        Assigns the properties of an operation rule by getting the rule using rule id
        """
        xml = "<Api_GetOperationWindowReq><ruleId>" + str(self.rule_id) + "</ruleId></Api_GetOperationWindowReq>"
        response_json = self._commcell_object._qoperation_execute(xml)
        if response_json:
            error_code = response_json.get("error", {}).get('errorCode')
            if int(error_code) == 0:
                response_json = response_json.get('operationWindow', {})[0]
                self._do_not_submit_job = response_json.get('doNotSubmitJob')
                self._name = response_json.get('name')
                self._start_date = response_json.get('startDate')
                self._end_date = response_json.get('endDate')
                operations = response_json.get('operations')
                operation_reverse_mapping = {value: key for key, value in OPERATION_MAPPING.items()}
                self._operations = [operation_reverse_mapping[operation] for operation in operations]
                week_of_the_month = response_json.get("dayTime")[0].get('weekOfTheMonth', [])
                if len(response_json.get("dayTime", [])) == 1:
                    start_time = response_json.get("dayTime")[0]['startTime']
                    end_time = response_json.get("dayTime")[0]['endTime']
                    day_of_week = response_json.get("dayTime")[0]['dayOfWeek']
                else:
                    day_of_week = []
                    start_time = []
                    end_time = []
                    for week_day in response_json.get("dayTime", []):
                        if week_day.get("dayOfWeek"):
                            day_of_week.append(week_day.get("dayOfWeek")[0])
                        if week_day.get("startTime") is not None:
                            start_time.append(week_day.get("startTime"))
                        if week_day.get("endTime") is not None:
                            end_time.append(week_day.get("endTime"))
                wotm_reverse_mapping = {value: key for key, value in WEEK_OF_THE_MONTH_MAPPING.items()}
                self._week_of_the_month = [wotm_reverse_mapping[week] for week in week_of_the_month]
                self._day_of_week = [DAY_OF_WEEK_MAPPING[day] for day in day_of_week]
                self._start_time = start_time
                self._end_time = end_time
            else:
                raise SDKException('OperationWindow', '102',
                                   response_json.get("error", {}).get('errorMessage'))
        else:
            raise SDKException('Response', '102')

    @property
    def do_not_submit_job(self):
        """Treats do_not_submit_job as a read-only attribute."""
        return self._do_not_submit_job

    @do_not_submit_job.setter
    def do_not_submit_job(self, do_not_submit_job):
        """
        Modifies do_not_submit_job of the operation rule
        Args:
             do_not_submit_job: (bool) -- do_not_submit_job of the operation rule to be modified"""
        self.modify_operation_window(do_not_submit_job=do_not_submit_job)

    @property
    def name(self):
        """Treats name as a read-only attribute."""
        return self._name

    @name.setter
    def name(self, name):
        """
        Modifies the name of the operation rule
        Args:
             name: (str) --Name of the operation rule to be modified
        """
        self.modify_operation_window(name=name)

    @property
    def start_date(self):
        """Treats start_date as a read-only attribute."""
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Modifies the start_date of the operation rule
        Args:
            start_date: (int) --The start date for the operation rule.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
        Returns: None
        """
        self.modify_operation_window(start_date=start_date)

    @property
    def end_date(self):
        """Treats end_date as a read-only attribute."""
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Modifies the end_date of the operation rule
        Args:
            end_date: (int)   -- The end date for the operation rule.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
        Returns: None
        """
        self.modify_operation_window(end_date=end_date)

    @property
    def operations(self):
        """Treats opearations as a read-only attribute."""
        return self._operations

    @operations.setter
    def operations(self, operations):
        """
        Modifies the operations of the operation rule
        Args:
            operations: (list)         --   List of operations for which the operation
                                               window is created
                    Acceptable Values:
                        FULL_DATA_MANAGEMENT/NON_FULL_DATA_MANAGEMENT/SYNTHETIC_FULL/
                        DATA_RECOVERY/AUX_COPY/DR_BACKUP/DATA_VERIFICATION/ERASE_SPARE_MEDIA/
                        SHELF_MANAGEMENT/DELETE_DATA_BY_BROWSING/DELETE_ARCHIVED_DATA/
                        OFFLINE_CONTENT_INDEXING/ONLINE_CONTENT_INDEXING/SRM/INFORMATION_MANAGEMENT/
                        MEDIA_REFRESHING/DATA_ANALYTICS/DATA_PRUNING/BACKUP_COPY/CLEANUP_OPERATION

        Returns: None
        """
        self.modify_operation_window(operations=operations)

    @property
    def week_of_the_month(self):
        """Treats week_of_the_month as a read-only attribute."""
        return self._week_of_the_month

    @week_of_the_month.setter
    def week_of_the_month(self, week_of_the_month):
        """
        Modifies the week_of_the_month of the operation rule
        Args:
            week_of_the_month: (list)         --   List of week of the month on which the operation rule applies to
                     Acceptable Values:
                            all/first/second/third/fourth/fifth
        Returns: None
        """
        self.modify_operation_window(week_of_the_month=week_of_the_month)

    @property
    def day_of_week(self):
        """Treats day_of_week as a read-only attribute."""
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, day_of_week):
        """
        Modifies the day_of_week of the operation rule
        Args:
            day_of_week: (list)    -- List of days of the week on which the operation rule applies to
                    Acceptable Values:
                        sunday/ monday/ tuesday/ wednesday/ thursday/ friday/ saturday
        Returns: None
        """
        self.modify_operation_window(day_of_week=day_of_week)

    @property
    def start_time(self):
        """Treats start_time as a read-only attribute."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Modifies the start_time of the operation rule
        Args:
            start_time: (int)     -- The start time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                        (list)    -- The list of start timestamps for each weekday mentioned
                    in the day_of_week list.
        Returns: None
        """
        self.modify_operation_window(start_time=start_time)

    @property
    def end_time(self):
        """Treats end_time as a read-only attribute."""
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Modifies the end_time of the operation rule
        Args:
            end_time: (int)     -- The end time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                      (list)    -- The list of end timestamps for each weekday mentioned
                    in the day_of_week list.
        Returns: None
        """
        self.modify_operation_window(end_time=end_time)

    @property
    def rule_id(self):
        """Treats rule_id as read-only attribute"""
        return self._rule_id

    @property
    def commcell_id(self):
        """Treats the commcell id as a read-only attribute."""
        return self._commcell_id

    @property
    def clientgroup_id(self):
        """Treats the client group id as a read-only attribute."""
        return self._clientgroup_id

    @property
    def client_id(self):
        """Treats the client id as a read-only attribute."""
        return self._client_id

    @property
    def agent_id(self):
        """Treats the agent id as a read-only attribute."""
        return self._agent_id

    @property
    def instance_id(self):
        """Treats the instance id as a read-only attribute."""
        return self._instance_id

    @property
    def backupset_id(self):
        """Treats the backupset id as a read-only attribute."""
        return self._backupset_id

    @property
    def subclient_id(self):
        """Treats the sub client id as a read-only attribute."""
        return self._subclient_id

    @property
    def entity_level(self):
        """Treats the entity level as a read-only attribute."""
        return self._entity_level
