# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for performing Operation Window related operations on given Commcell entity.

OperationWindow: Class for performing Operation Window related operations on given Commcell entity.

OperationWindow:

    __init__()                          --  initialize instance of the OperationWindow class

    create_operation_window()           --  Creates a Operation rule on the given commcell instance

    delete_operation_window()           --  deletes a Operation rule on the commcell instance

    list_operation_window()             --  Lists all the operation rule associated with given commcell entity

        Example with client instance:
            from cvpysdk.commcell import Commcell
            commcell = Commcell(<CS>, username, password)
            client = commcell.clients.get(<client Name>)
            from cvpysdk.operation_window import OperationWindow
            client_operation_window = OperationWindow(client)
            rule_id = client_operation_window.create_operation_window("operation window example on clientLevel")
            client_operation_window.list_operation_window()
            client_operation_window.delete_operation_window(rule_id)

"""

from __future__ import absolute_import

import time
from datetime import timedelta

from .exception import SDKException
from .client import Client
from .agent import Agent
from .instance import Instance
from .backupset import Backupset
from .subclient import Subclient


class OperationWindow(object):
    """Class for representing all operation window related operations"""

    def __init__(self, generic_entity_obj):
        """Initialize the OperationWindow class instance for performing OperationWindow related operations.

            Args:
                generic_entity_obj     (object)    --  Commcell entity object
                    Expected value : commcell/Client/Agent/Instance/BackupSet/Subclient Instance

            Returns:
                object  -   instance of the OperationWindow class

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

        self.client_id = 0
        self.agent_id = 0
        self.instance_id = 0
        self.backupset_id = 0
        self.subclient_id = 0
        self.entity_type = ''
        self.entity_id = ''

        # we will derive all the entity id's based on the input entity type
        if isinstance(generic_entity_obj, Commcell):
            pass
        elif isinstance(generic_entity_obj, Client):
            self.client_id = generic_entity_obj.client_id
            self.entity_type = "clientId"
            self.entity_id = self.client_id
        elif isinstance(generic_entity_obj, Agent):
            self.client_id = generic_entity_obj._client_object.client_id
            self.agent_id = generic_entity_obj.agent_id
            self.entity_type = "applicationId"
            self.entity_id = self.agent_id
        elif isinstance(generic_entity_obj, Instance):
            self.client_id = generic_entity_obj._agent_object._client_object.client_id
            self.agent_id = generic_entity_obj._agent_object.agent_id
            self.instance_id = generic_entity_obj.instance_id
            self.entity_type = "instanceId"
            self.entity_id = self.instance_id
        elif isinstance(generic_entity_obj, Backupset):
            self.client_id = generic_entity_obj._instance_object._agent_object._client_object.client_id
            self.agent_id = generic_entity_obj._instance_object._agent_object.agent_id
            self.instance_id = generic_entity_obj._instance_object.instance_id
            self.backupset_id = generic_entity_obj.backupset_id
            self.entity_type = "backupsetId"
            self.entity_id = self.backupset_id
        elif isinstance(generic_entity_obj, Subclient):
            self.client_id =  \
                generic_entity_obj._backupset_object._instance_object._agent_object._client_object.client_id
            self.agent_id = generic_entity_obj._backupset_object._instance_object._agent_object.agent_id
            self.instance_id = generic_entity_obj._backupset_object._instance_object.instance_id
            self.backupset_id = generic_entity_obj._backupset_object.backupset_id
            self.subclient_id = generic_entity_obj.subclient_id
            self.entity_type = "subclientId"
            self.entity_id = self.subclient_id
        else:
            raise SDKException('Response', '101', "Invalid instance passed")

        # append the entity type and entity id to end of list operation window REST API.
        # For commcell it will empty string
        self.connect_string = self._list_operation_window.split('?')[0] + '?' + \
                              self.entity_type + "=" + self.entity_id

    def create_operation_window(
            self,
            name,
            start_date=None,
            end_date=None,
            operations=None,
            day_of_week=None,
            start_time=None,
            end_time=None,
            client_group_name=None):
        """ Creates operation rule on the initialized commcell instance

            Args:
                name          (str)   --  Name of the Operation rule

                start_date    (int)   -- The start date for the operation rule.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - current date

                end_date      (int)   -- The end date for the operation rule.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 365 days

                operations   (list)   -- The operations the operation rule applies to
                    Acceptable Values:
                        FULL_DATA_MANAGEMENT/NON_FULL_DATA_MANAGEMENT/SYNTHETIC_FULL/
                        DATA_RECOVERY/AUX_COPY/ER_BACKUP/ARCHIVE_CHECK/TAPE_ERASE/
                        SHELF_MANAGEMENT/DELETE_DATA_BY_BROWSING/DELETE_ARCHIVED_DATA/
                        OFFLINE_CONTENT_INDEXING/ONLINE_CONTENT_INDEXING/SRM/INFOMGMT/
                        MEDIA_REFRESHING/DATA_ANALYTICS/DATA_PRUNING/BACKUP_COPY/STUBBING

                day_of_week (list)    -- List of days of the week on which the operation rule applies to
                    Acceptable Values:
                        sunday/ monday/ tuesday/ wednesday/ thursday/ friday/ saturday

                    default- Weekdays

                start_time  (int)     -- The start time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 28800 (8 AM)

                end_time    (int)     -- The end time for the "do not run" interval.
                    Valid values are UNIX-style timestamps (seconds since January 1, 1970).
                    default - 86400 (6 PM)

                client_group_name   (str)  -- Name of client group

            Returns:
                Returns the rule Id (system-generated ID assigned to the operation rule created)

            Raises:
                SDKException:
                    if the Operation window could not be created

                    if response is empty

                    if response is not success

        """
        day_of_week_mapping = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        operation_mapping = {
            "FULL_DATA_MANAGEMENT": 1,
            "NON_FULL_DATA_MANAGEMENT": 2,
            "SYNTHETIC_FULL": 4,
            "DATA_RECOVERY": 8,
            "AUX_COPY": 16,
            "ER_BACKUP": 32,
            "ARCHIVE_CHECK": 64,
            "TAPE_ERASE": 128,
            "SHELF_MANAGEMENT": 256,
            "DELETE_DATA_BY_BROWSING": 512,
            "DELETE_ARCHIVED_DATA": 1024,
            "OFFLINE_CONTENT_INDEXING": 2048,
            "ONLINE_CONTENT_INDEXING": 4096,
            "SRM": 8192,
            "INFOMGMT": 16384,
            "MEDIA_REFRESHING": 32768,
            "DATA_ANALYTICS": 65536,
            "DATA_PRUNING": 131072,
            "BACKUP_COPY": 262144,
            "STUBBING": 524288}

        if start_date is None:
            start_date = int(time.time())
        if end_date is None:
            end_date = int(time.time()) + int(timedelta(days=365).total_seconds())
        if start_time is None:
            start_time = int(timedelta(hours=8).total_seconds())
        if end_time is None:
            end_time = int(timedelta(hours=18).total_seconds())

        operations_list = []
        if operations is None:
            operations_list = [operation_mapping["FULL_DATA_MANAGEMENT"]]
        else:
            for operation in operations:
                if operation not in operation_mapping:
                    response_string = "Invalid input %s for operation is passed" % operation
                    raise SDKException('OperationWindow', '101', response_string)
                operations_list.append(operation_mapping[operation.upper()])

        day_of_week_list = []
        if day_of_week is None:
            day_of_week_list = [1, 2, 3, 4, 5]  # defaults to weekdays
        else:
            for day in day_of_week:
                if day.lower() not in day_of_week_mapping:
                    response_string = "Invalid input value %s for day_of_week" % day
                    raise SDKException('OperationWindow', '101', response_string)
                day_of_week_list.append(day_of_week_mapping.index(day.lower()))

        client_group_id = 0
        client_groups = self._commcell_object.client_groups
        if not client_group_name is None:
            client_group_id = client_groups.all_clientgroups[client_group_name]

        payload = {
            "operationWindow": {
                "ruleEnabled": True,
                "startDate": start_date,
                "endDate": end_date,
                "name": name,
                "operations": operations_list,
                "dayTime": [{
                    "startTime": start_time,
                    "endTime": end_time,
                    "dayOfWeek": day_of_week_list
                }]
            },
            "entity": {
                "clientGroupId": client_group_id,
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
                error_code = response.json()["error"]['errorCode']
                if int(error_code) == 0:
                    return int(response.json()['operationWindow']['ruleId'])
                else:
                    raise SDKException(
                        'OperationWindow', '101', response.json()["error"]['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response(
                response.text)
            raise SDKException('Response', '101', response_string)

    def delete_operation_window(self, rule_id):
        """Deletes the operation rule associated with given rule Id.

            Args:
                rule_id       (int)   --  Rule Id of the operation window returned in create request

            Raises:
                SDKException:
                    if the Operation window could not be deleted

                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._operation_window + '/' + str(rule_id))
        if flag:
            if response.json():
                error_code = response.json()["error"]['errorCode']
                if int(error_code):
                    raise SDKException(
                        'OperationWindow', '103', response.json()["error"]['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response(
                response.text)
            raise SDKException('Response', '101', response_string)

    def list_operation_window(self):
        """Lists the operation rules for the associated commcell entity.

            Returns:
                Returns the List of operation rules (dictionary) associated with given commcell entity

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
                error_code = response.json()["error"]['errorCode']
                if int(error_code) == 0:
                    return response.json()['operationWindow']
                else:
                    raise SDKException(
                        'OperationWindow', '104', response.json()["error"]['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response(
                response.text)
            raise SDKException('Response', '101', response_string)
