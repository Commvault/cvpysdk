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
from typing import Any, Dict, List, Optional, Union
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
                     "UPDATE_SOFTWARE": 2097152,
                     "CLEANUP_OPERATION": 524288,
                     "ALL": 1048576}


class OperationWindow:
    """
    Class for managing operation window related operations.

    This class provides an interface for creating, deleting, listing, and retrieving
    operation windows. An operation window defines a specific time frame and set of
    rules for executing operations, which can be customized by specifying parameters
    such as name, date range, operations, day of the week, time intervals, and
    submission control.

    Key Features:
        - Initialization with a generic entity object for context
        - Creation of operation windows with detailed scheduling parameters
        - Deletion of operation windows by rule ID and name
        - Listing all existing operation windows
        - Retrieval of specific operation window details by rule ID and name

    #ai-gen-doc
    """

    def __init__(self, generic_entity_obj: Any):
        """Initialize an OperationWindow instance for performing operation window-related tasks.

        The OperationWindow class can be initialized with a Commcell entity object, which may be an instance of
        Commcell, Client, Agent, Instance, Backupset, Subclient, or ClientGroup. The constructor determines the
        entity type and sets up internal attributes for operation window management.

        Args:
            generic_entity_obj: Commcell entity object. This can be an instance of one of the following:
                - Commcell
                - Client
                - Agent
                - Instance
                - Backupset
                - Subclient
                - ClientGroup

        Raises:
            Exception: If an invalid entity instance is passed.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> op_window = OperationWindow(commcell)
            >>> # You can also use Client, Agent, Instance, Backupset, Subclient, or ClientGroup objects
            >>> client = Client(...)
            >>> op_window_client = OperationWindow(client)
        #ai-gen-doc
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
            name: str,
            start_date: Optional[int] = None,
            end_date: Optional[int] = None,
            operations: Optional[List[str]] = None,
            day_of_week: Optional[List[str]] = None,
            start_time: Optional[Union[int, List[int]]] = None,
            end_time: Optional[Union[int, List[int]]] = None,
            week_of_the_month: Optional[List[str]] = None,
            do_not_submit_job: bool = False
        ):
        """Create an operation window rule for the initialized Commcell entity.

        This method creates a new operation window rule, specifying when certain operations 
        are allowed or restricted for the associated Commcell entity. The rule can be customized 
        by specifying the operations, days of the week, time intervals, and other scheduling options.

        Args:
            name: Name of the operation window rule.
            start_date: Start date for the operation rule as a UNIX timestamp (seconds since Jan 1, 1970). Defaults to current date.
            end_date: End date for the operation rule as a UNIX timestamp. Defaults to 365 days from start date.
            operations: List of operation names for which the window is created. Acceptable values include:
                'FULL_DATA_MANAGEMENT', 'NON_FULL_DATA_MANAGEMENT', 'SYNTHETIC_FULL', 'DATA_RECOVERY', 'AUX_COPY',
                'DR_BACKUP', 'DATA_VERIFICATION', 'ERASE_SPARE_MEDIA', 'SHELF_MANAGEMENT', 'DELETE_DATA_BY_BROWSING',
                'DELETE_ARCHIVED_DATA', 'OFFLINE_CONTENT_INDEXING', 'ONLINE_CONTENT_INDEXING', 'SRM', 'INFORMATION_MANAGEMENT',
                'MEDIA_REFRESHING', 'DATA_ANALYTICS', 'DATA_PRUNING', 'BACKUP_COPY', 'CLEANUP_OPERATION'.
                Defaults to ['FULL_DATA_MANAGEMENT'].
            day_of_week: List of days of the week to apply the rule. Acceptable values: 'sunday', 'monday', 'tuesday', 
                'wednesday', 'thursday', 'friday', 'saturday'. Defaults to weekdays ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'].
            start_time: Start time for the "do not run" interval. Can be a single UNIX timestamp (int) for all days, or a list of timestamps (List[int]) for each day in day_of_week.
                Defaults to 28800 (8 AM).
            end_time: End time for the "do not run" interval. Can be a single UNIX timestamp (int) for all days, or a list of timestamps (List[int]) for each day in day_of_week.
                Defaults to 64800 (6 PM).
            week_of_the_month: List of weeks of the month to apply the rule. Acceptable values: 'all', 'first', 'second', 'third', 'fourth', 'last'.
                Defaults to None (applies to all weeks).
            do_not_submit_job: If True, jobs will not be submitted during the operation window.

        Returns:
            Instance containing details of the created operation window rule.

        Raises:
            SDKException: If the operation window could not be created, if the response is empty, or if the response is not successful.

        Example:
            >>> # Create an operation window for Sundays, Thursdays, and Saturdays from 8 AM to 6 PM
            >>> op_window = operation_window.create_operation_window(
            ...     name="WeekendRestriction",
            ...     day_of_week=["sunday", "thursday", "saturday"],
            ...     start_time=28800,
            ...     end_time=64800,
            ...     operations=["FULL_DATA_MANAGEMENT"]
            ... )
            >>> print(f"Created operation window: {op_window}")

            >>> # Create an operation window with different times for Monday and Friday
            >>> op_window = operation_window.create_operation_window(
            ...     name="CustomWeekdays",
            ...     day_of_week=["monday", "friday"],
            ...     start_time=[3600, 28800],
            ...     end_time=[18000, 64800],
            ...     operations=["AUX_COPY", "DATA_RECOVERY"]
            ... )
            >>> print(f"Created operation window: {op_window}")

        #ai-gen-doc
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

    def delete_operation_window(self, rule_id: Optional[int] = None, name: Optional[str] = None) -> None:
        """Delete the operation window rule by rule ID or name.

        Either the rule ID or the name must be provided to identify the operation window to delete.
        This method will raise an SDKException if deletion fails, if the response is empty, or if the response indicates an error.

        Args:
            rule_id: The integer ID of the operation window rule to delete. Optional if name is provided.
            name: The name of the operation window rule to delete. Optional if rule_id is provided.

        Raises:
            SDKException: If neither rule_id nor name is provided, if the parameters are of incorrect type,
                if the operation window could not be deleted, if the response is empty, or if the response is not successful.

        Example:
            >>> op_window = OperationWindow(...)
            >>> # Delete by rule ID
            >>> op_window.delete_operation_window(rule_id=123)
            >>> # Delete by name
            >>> op_window.delete_operation_window(name="NightlyBackupWindow")
            >>> # Either rule_id or name must be specified

        #ai-gen-doc
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

    def list_operation_window(self) -> List[Dict[str, Any]]:
        """List the operation rules configured for the associated Commcell entity.

        Returns:
            List of dictionaries, each representing an operation rule associated with the Commcell entity.
            Each rule contains details such as rule status, job submission settings, date ranges, operations,
            company information, and time-based restrictions.

        Raises:
            SDKException: If the operation rules could not be listed, if the response is empty, or if the response is not successful.

        Example:
            >>> op_window = OperationWindow(commcell_object)
            >>> rules = op_window.list_operation_window()
            >>> for rule in rules:
            ...     print(f"Rule Name: {rule['name']}, Enabled: {rule['ruleEnabled']}")
            >>> # Example output:
            >>> # Rule Name: Rule1, Enabled: True

        #ai-gen-doc
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

    def get(self, rule_id: Optional[int] = None, name: Optional[str] = None) -> 'OperationWindowDetails':
        """Retrieve the operation window rule object by rule ID or name.

        Either the rule ID or the name must be provided to identify the operation window.
        Returns an instance of OperationWindowDetails for the specified rule.

        Args:
            rule_id: Optional integer representing the rule ID of the operation window.
            name: Optional string representing the name of the operation window.

        Returns:
            OperationWindowDetails: Instance representing the requested operation window.

        Raises:
            SDKException: If neither rule_id nor name is provided, or if their types are invalid.
            Exception: If no operation window exists with the specified rule ID or name, or if multiple windows share the same name.

        Example:
            >>> op_window = OperationWindow(commcell_object)
            >>> # Retrieve by rule ID
            >>> rule_details = op_window.get(rule_id=123)
            >>> print(f"Rule ID: {rule_details.rule_id}")
            >>> # Retrieve by name
            >>> rule_details = op_window.get(name="NightlyBackupWindow")
            >>> print(f"Window Name: {rule_details.name}")

        #ai-gen-doc
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
    """
    Helper class for modifying and managing operation window details.

    This class provides an interface for accessing and updating the properties
    of an operation window, which may include scheduling parameters, entity
    identifiers, and rule configurations. It is designed to work with generic
    entity objects and rule IDs, allowing for flexible modification and retrieval
    of operation window attributes.

    Key Features:
        - Initialization with entity object, rule ID, and entity details
        - Modification of operation window parameters
        - Refreshing and retrieving rule properties
        - Property accessors and mutators for:
            - Job submission control
            - Operation window name
            - Start and end dates
            - Operations list
            - Week of the month and day of the week
            - Start and end times
            - Various entity and rule identifiers (commcell, client group, client, agent, instance, backupset, subclient)
            - Entity level

    This class is intended to be used in scenarios where operation windows need
    to be programmatically managed, such as in backup or scheduling systems.

    #ai-gen-doc
    """

    def __init__(self, generic_entity_obj: Any, rule_id: int, entity_details: Dict[str, Any]):
        """Initialize an OperationWindowDetails instance for modifying an operation window.

        Args:
            generic_entity_obj: Commcell entity object, which can be an instance of Commcell, Client, Agent, Instance, BackupSet, Subclient, or Clientgroup.
            rule_id: The rule ID of the operation window to be modified.
            entity_details: Dictionary containing details related to the entity, such as clientGroupId, clientId, applicationId, instanceId, backupsetId, subclientId, and entity_level.

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> entity_details = {
            ...     "clientGroupId": 101,
            ...     "clientId": 202,
            ...     "applicationId": 303,
            ...     "instanceId": 404,
            ...     "backupsetId": 505,
            ...     "subclientId": 606,
            ...     "entity_level": "Client"
            ... }
            >>> rule_id = 12345
            >>> op_window_details = OperationWindowDetails(commcell, rule_id, entity_details)
            >>> print(f"OperationWindowDetails initialized for rule ID: {rule_id}")

        #ai-gen-doc
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

    def modify_operation_window(self, **modify_options: Any) -> None:
        """Modify the operation window rule with the specified options.

        This method updates the operation window rule using the provided keyword arguments.
        You can customize the rule's name, date range, applicable operations, days, times, and other settings.

        Args:
            **modify_options: Arbitrary keyword arguments to specify operation window properties.
                Supported options include:
                    name (str): Name of the operation rule.
                    start_date (int): Start date as a UNIX timestamp (seconds since Jan 1, 1970). Default is current date.
                    end_date (int): End date as a UNIX timestamp. Default is 365 days from start.
                    operations (List[str]): List of operation types for the window.
                        Acceptable values include:
                            FULL_DATA_MANAGEMENT, NON_FULL_DATA_MANAGEMENT, SYNTHETIC_FULL,
                            DATA_RECOVERY, AUX_COPY, DR_BACKUP, DATA_VERIFICATION, ERASE_SPARE_MEDIA,
                            SHELF_MANAGEMENT, DELETE_DATA_BY_BROWSING, DELETE_ARCHIVED_DATA,
                            OFFLINE_CONTENT_INDEXING, ONLINE_CONTENT_INDEXING, SRM, INFORMATION_MANAGEMENT,
                            MEDIA_REFRESHING, DATA_ANALYTICS, DATA_PRUNING, BACKUP_COPY, CLEANUP_OPERATION
                    week_of_the_month (List[str]): Weeks of the month to apply the rule.
                        Acceptable values: all, first, second, third, fourth, last.
                    day_of_week (List[str]): Days of the week to apply the rule.
                        Acceptable values: sunday, monday, tuesday, wednesday, thursday, friday, saturday.
                    start_time (Union[int, List[int]]): Start time(s) as UNIX timestamp(s).
                        If a single int, applies to all days; if a list, must match day_of_week length.
                        Default is 28800 (8 AM).
                    end_time (Union[int, List[int]]): End time(s) as UNIX timestamp(s).
                        If a single int, applies to all days; if a list, must match day_of_week length.
                        Default is 86400 (6 PM).
                    do_not_submit_job (bool): Whether to prevent job submission during the window.

        Raises:
            SDKException: If the operation window could not be modified, if the response is empty,
                or if the response indicates failure.

        Example:
            >>> # Example 1: Same start/end time for multiple days
            >>> op_window.modify_operation_window(
            ...     day_of_week=["sunday", "thursday", "saturday"],
            ...     start_time=28800,
            ...     end_time=86400,
            ...     operations=["FULL_DATA_MANAGEMENT", "AUX_COPY"]
            ... )
            >>> # Example 2: Different start/end times for each day
            >>> op_window.modify_operation_window(
            ...     day_of_week=["monday", "friday"],
            ...     start_time=[3600, 28800],
            ...     end_time=[18000, 86400],
            ...     operations=["DATA_RECOVERY"]
            ... )
        #ai-gen-doc
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

    def _refresh(self) -> None:
        """Reload the properties of the operation window rule.

        This method updates the internal state of the OperationWindowDetails object
        by fetching the latest rule properties from the source.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window._refresh()
            >>> # The rule properties are now updated to reflect the latest state

        #ai-gen-doc
        """
        self._get_rule_properties()

    def _get_rule_properties(self) -> None:
        """Fetch and assign properties for the operation rule using its rule ID.

        This method retrieves the operation window rule details from the Commcell server
        and updates the instance properties such as name, start/end dates, operations,
        week of the month, day of the week, and time intervals.

        Raises:
            SDKException: If the rule cannot be retrieved or if the response contains an error.

        Example:
            >>> op_window = OperationWindowDetails(commcell_object, rule_id)
            >>> op_window._get_rule_properties()
            >>> print(f"Rule name: {op_window._name}")
            >>> print(f"Start date: {op_window._start_date}")
            >>> print(f"Operations: {op_window._operations}")
            >>> # The instance properties are now populated with rule details

        #ai-gen-doc
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
                week_of_the_month = response_json.get("dayTime", [{}])[0].get('weekOfTheMonth', [])
                if len(response_json.get("dayTime", [])) == 1:
                    start_time = response_json.get("dayTime", [{}])[0].get('startTime')
                    end_time = response_json.get("dayTime", [{}])[0].get('endTime')
                    day_of_week = response_json.get("dayTime", [{}])[0].get('dayOfWeek')
                else:
                    day_of_week = []
                    start_time = []
                    end_time = []
                    for week_day in response_json.get("dayTime", [{}]):
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
    def do_not_submit_job(self) -> bool:
        """Indicate whether jobs should not be submitted during the operation window.

        Returns:
            True if job submission is disabled during the operation window, False otherwise.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> if op_window.do_not_submit_job:
            ...     print("Job submission is disabled during this window.")
            ... else:
            ...     print("Jobs can be submitted during this window.")

        #ai-gen-doc
        """
        return self._do_not_submit_job

    @do_not_submit_job.setter
    def do_not_submit_job(self, do_not_submit_job: bool) -> None:
        """Set the 'do_not_submit_job' flag for the operation rule.

        Args:
            do_not_submit_job: Boolean value indicating whether jobs should not be submitted during the operation window.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window.do_not_submit_job = True  # Prevent job submission during the operation window
            >>> op_window.do_not_submit_job = False # Allow job submission during the operation window

        #ai-gen-doc
        """
        self.modify_operation_window(do_not_submit_job=do_not_submit_job)

    @property
    def name(self) -> str:
        """Get the name of the operation window as a read-only property.

        Returns:
            The name of the operation window as a string.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> window_name = op_window.name  # Access the name property
            >>> print(f"Operation window name: {window_name}")
        #ai-gen-doc
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the operation rule.

        Args:
            name: The new name to assign to the operation rule.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window.name = "NightlyBackupWindow"  # Use assignment for property setters
            >>> # The operation rule name is now updated to "NightlyBackupWindow"

        #ai-gen-doc
        """
        self.modify_operation_window(name=name)

    @property
    def start_date(self) -> str:
        """Get the start date for the operation window as a read-only property.

        Returns:
            The start date as a string in the format 'YYYY-MM-DD'.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> start = op_window.start_date  # Use dot notation for property access
            >>> print(f"Operation window starts on: {start}")
        #ai-gen-doc
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date: int) -> None:
        """Set the start date for the operation rule.

        Args:
            start_date: The start date for the operation rule as a UNIX timestamp (seconds since January 1, 1970).

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window.start_date = 1680307200  # Set start date to March 31, 2023
            >>> # The operation rule's start date is now updated

        #ai-gen-doc
        """
        self.modify_operation_window(start_date=start_date)

    @property
    def end_date(self) -> str:
        """Get the end date for the operation window as a read-only property.

        Returns:
            The end date of the operation window as a string.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> end = op_window.end_date  # Access the end_date property
            >>> print(f"Operation window ends on: {end}")
        #ai-gen-doc
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: int) -> None:
        """Set the end date for the operation rule.

        Args:
            end_date: The end date for the operation rule as a UNIX timestamp (seconds since January 1, 1970).

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window.end_date = 1719878400  # Set end date to a specific UNIX timestamp
            >>> # The operation rule's end date is now updated

        #ai-gen-doc
        """
        self.modify_operation_window(end_date=end_date)

    @property
    def operations(self) -> List[Dict[str, Any]]:
        """Get the list of operations associated with the operation window.

        Returns:
            List of dictionaries, each containing details about an operation.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> ops = op_window.operations  # Use dot notation for property access
            >>> print(f"Total operations: {len(ops)}")
            >>> if ops:
            >>>     print(f"First operation details: {ops[0]}")

        #ai-gen-doc
        """
        return self._operations

    @operations.setter
    def operations(self, operations: List[str]) -> None:
        """Set the operations for the operation window rule.

        Args:
            operations: List of operation names for which the operation window is created.
                Acceptable values include:
                    - FULL_DATA_MANAGEMENT
                    - NON_FULL_DATA_MANAGEMENT
                    - SYNTHETIC_FULL
                    - DATA_RECOVERY
                    - AUX_COPY
                    - DR_BACKUP
                    - DATA_VERIFICATION
                    - ERASE_SPARE_MEDIA
                    - SHELF_MANAGEMENT
                    - DELETE_DATA_BY_BROWSING
                    - DELETE_ARCHIVED_DATA
                    - OFFLINE_CONTENT_INDEXING
                    - ONLINE_CONTENT_INDEXING
                    - SRM
                    - INFORMATION_MANAGEMENT
                    - MEDIA_REFRESHING
                    - DATA_ANALYTICS
                    - DATA_PRUNING
                    - BACKUP_COPY
                    - CLEANUP_OPERATION

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window.operations = [
            ...     "FULL_DATA_MANAGEMENT",
            ...     "AUX_COPY",
            ...     "DATA_RECOVERY"
            ... ]
            >>> # The operation window will now apply to the specified operations

        #ai-gen-doc
        """
        self.modify_operation_window(operations=operations)

    @property
    def week_of_the_month(self) -> int:
        """Get the week of the month for the operation window.

        Returns:
            The week of the month as an integer (e.g., 1 for first week, 2 for second week).

        Example:
            >>> details = OperationWindowDetails(...)
            >>> week = details.week_of_the_month  # Use dot notation for property access
            >>> print(f"Operation window is set for week: {week}")

        #ai-gen-doc
        """
        return self._week_of_the_month

    @week_of_the_month.setter
    def week_of_the_month(self, week_of_the_month: List[str]) -> None:
        """Set the weeks of the month during which the operation rule applies.

        Args:
            week_of_the_month: List of week identifiers specifying when the operation rule is active.
                Acceptable values include: "all", "first", "second", "third", "fourth", "fifth".

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window.week_of_the_month = ["first", "third"]
            >>> # The operation rule will now apply on the first and third weeks of each month.

        #ai-gen-doc
        """
        self.modify_operation_window(week_of_the_month=week_of_the_month)

    @property
    def day_of_week(self) -> str:
        """Get the day of the week for the operation window.

        Returns:
            The day of the week as a string (e.g., "Monday", "Tuesday").

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> day = op_window.day_of_week  # Use dot notation for property access
            >>> print(f"Operation window is set for: {day}")

        #ai-gen-doc
        """
        return self._day_of_week

    @day_of_week.setter
    def day_of_week(self, day_of_week: List[str]) -> None:
        """Set the days of the week for the operation rule.

        Args:
            day_of_week: List of days (as strings) on which the operation rule applies.
                Acceptable values:
                    'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> op_window.day_of_week = ['monday', 'wednesday', 'friday']  # Use assignment for property setter
            >>> # The operation rule will now apply on Monday, Wednesday, and Friday

        #ai-gen-doc
        """
        self.modify_operation_window(day_of_week=day_of_week)

    @property
    def start_time(self) -> str:
        """Get the start time for the operation window as a read-only property.

        Returns:
            The start time of the operation window as a string.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> start = op_window.start_time  # Access using dot notation
            >>> print(f"Operation window starts at: {start}")
        #ai-gen-doc
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: Union[int, List[int]]) -> None:
        """Set the start time for the operation window rule.

        This setter updates the start time for the "do not run" interval in the operation window.
        The start time can be specified as a single UNIX timestamp (seconds since January 1, 1970)
        or as a list of timestamps corresponding to each weekday in the `day_of_week` list.

        Args:
            start_time: An integer UNIX timestamp for the start of the interval, or a list of
                timestamps for each weekday.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> # Set a single start time for all days
            >>> op_window.start_time = 1680307200
            >>> # Set different start times for specific weekdays
            >>> op_window.start_time = [1680307200, 1680393600, 1680480000]

        #ai-gen-doc
        """
        self.modify_operation_window(start_time=start_time)

    @property
    def end_time(self) -> str:
        """Get the end time for the operation window as a read-only property.

        Returns:
            The end time of the operation window as a string in the configured format.

        Example:
            >>> details = OperationWindowDetails(...)
            >>> end = details.end_time  # Use dot notation for property access
            >>> print(f"Operation window ends at: {end}")
        #ai-gen-doc
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: Union[int, List[int]]) -> None:
        """Set the end time for the operation window rule.

        The end time can be specified as a single UNIX timestamp (seconds since January 1, 1970) 
        or as a list of timestamps for each weekday mentioned in the day_of_week list.

        Args:
            end_time: The end time for the "do not run" interval. 
                - If an integer, sets a single end time for all applicable days.
                - If a list of integers, sets individual end times for each weekday.

        Example:
            >>> op_window = OperationWindowDetails()
            >>> # Set a single end time for all days
            >>> op_window.end_time = 1685587200
            >>> # Set different end times for specific weekdays
            >>> op_window.end_time = [1685587200, 1685673600, 1685760000]

        #ai-gen-doc
        """
        self.modify_operation_window(end_time=end_time)

    @property
    def rule_id(self) -> str:
        """Get the rule ID associated with this operation window.

        Returns:
            The rule ID as a string.

        Example:
            >>> details = OperationWindowDetails(...)
            >>> rule_id = details.rule_id  # Access the rule ID property
            >>> print(f"Rule ID: {rule_id}")

        #ai-gen-doc
        """
        return self._rule_id

    @property
    def commcell_id(self) -> int:
        """Get the Commcell ID as a read-only property.

        Returns:
            The unique identifier of the Commcell as an integer.

        Example:
            >>> details = OperationWindowDetails(...)
            >>> commcell_id = details.commcell_id  # Access the Commcell ID property
            >>> print(f"Commcell ID: {commcell_id}")

        #ai-gen-doc
        """
        return self._commcell_id

    @property
    def clientgroup_id(self) -> str:
        """Get the client group ID as a read-only property.

        Returns:
            The client group ID as a string.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> group_id = op_window.clientgroup_id  # Access via property
            >>> print(f"Client group ID: {group_id}")
        #ai-gen-doc
        """
        return self._clientgroup_id

    @property
    def client_id(self) -> str:
        """Get the client ID associated with this OperationWindowDetails instance.

        Returns:
            The client ID as a string. This property is read-only and cannot be modified directly.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> client_identifier = op_window.client_id  # Access the client ID using dot notation
            >>> print(f"Client ID: {client_identifier}")
        #ai-gen-doc
        """
        return self._client_id

    @property
    def agent_id(self) -> int:
        """Get the agent ID associated with the operation window.

        Returns:
            The agent ID as an integer.

        Example:
            >>> details = OperationWindowDetails(...)
            >>> agent_identifier = details.agent_id  # Access agent_id as a property
            >>> print(f"Agent ID: {agent_identifier}")

        #ai-gen-doc
        """
        return self._agent_id

    @property
    def instance_id(self) -> int:
        """Get the instance ID associated with this OperationWindowDetails object.

        Returns:
            The instance ID as an integer.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> instance_id = op_window.instance_id  # Use dot notation for property access
            >>> print(f"Instance ID: {instance_id}")
        #ai-gen-doc
        """
        return self._instance_id

    @property
    def backupset_id(self) -> str:
        """Get the backupset ID as a read-only property.

        Returns:
            The backupset ID as a string.

        Example:
            >>> details = OperationWindowDetails(...)
            >>> backupset_id = details.backupset_id  # Access the backupset ID property
            >>> print(f"Backupset ID: {backupset_id}")

        #ai-gen-doc
        """
        return self._backupset_id

    @property
    def subclient_id(self) -> int:
        """Get the subclient ID as a read-only property.

        Returns:
            The unique identifier of the subclient as an integer.

        Example:
            >>> details = OperationWindowDetails(...)
            >>> subclient_id = details.subclient_id  # Access via property
            >>> print(f"Subclient ID: {subclient_id}")

        #ai-gen-doc
        """
        return self._subclient_id

    @property
    def entity_level(self) -> str:
        """Get the entity level associated with the operation window details.

        This property provides read-only access to the entity level, which typically 
        indicates the scope or type of entity (such as client, subclient, or backupset) 
        for which the operation window is defined.

        Returns:
            The entity level as a string.

        Example:
            >>> op_window = OperationWindowDetails(...)
            >>> level = op_window.entity_level  # Use dot notation for property access
            >>> print(f"Entity level: {level}")
        #ai-gen-doc
        """
        return self._entity_level
