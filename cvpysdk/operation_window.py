# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for performing Operation Window related operations on Commcell.

OperationWindow:   Class for creation,deletion and listing of operation windows

OperationWindow:

    __init__(commcell_object)           --  initialize instance of the OperationWindow class

    create_operation_window()           --  Creates a Operation window

    delete_operation_window()           --  deletes a Operation Window from the commcell

    list_operation_window()             --  Lists all the operation window associted with a client

"""

from __future__ import absolute_import
import time
from .exception import SDKException
from .client import Client
from .agent import Agent
from .instance import Instance
from .backupset import Backupset
from .subclient import Subclient


class OperationWindow(object):
    """Class for representing all workflows of a commcell."""

    def __init__(self, generic_entity_obj):
        """Initialize the OperationWindow class instance for
           performing OperationWindow related operations.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

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
        """Creates the OperationWindow with the Operation Window name given as input,
           for a particular client given as input and returns its Rule id.

            Args:
                name              (str)   --  Name of the Operation Window

                start_date/end_date (str) --  Timestamp value for the start and end date
                                              of operation window. If default values are passed,
                                              this will create a operation window for the
                                              period of one year starting from the present date.

                operations (list)         --   List of operations for which the operation
                                               window is created

                    Acceptable Values:

                        FULL_DATA_PROTECTION/NON_FULL_DATA_PROTECTION/SYNTHETIC_FULL/
                        DATA_RECOVERY/AUX_COPY/ER_BACKUP/ARCHIVE_CHECK/TAPE_ERASE/
                        SHELF_MANAGEMENT/ERASE_BACKUP_DATA/ERASE_MIGRATED_DATA/
                        OFFLINE_CONTENT_INDEXING/ONLINE_CONTENT_INDEXING/SRM/INFOMGMT/
                        MEDIA_REFRESHING/DATA_ANALYTICS/DATA_PRUNING/BACKUP_COPY/STUBBING

                day_of_week  (list)      --   List of days on which the operation window is active

                    Acceptable Values:

                        sunday/ monday/ tuesday/ wednesday/ thursday/ friday/ saturday

                start_time/end_time (str)  -- Time period in which the operation window is active.
                                               If the defauilt values are passed, it will create a
                                               operation window from 12AM - 11:59PM

                client_group_name   (str)  -- Name of client group

            Returns:
                Returns the rule Id of created Operation window

            Raises:
                SDKException:
                    if the Operation window could not be created

                    if response is empty

                    if response is not success

        """
        day_of_week_mapping = {
            "sunday": 0,
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6}
        operation_mapping = {
            "FULL_DATA_PROTECTION": 1,
            "NON_FULL_DATA_PROTECTION": 2,
            "SYNTHETIC_FULL": 4,
            "DATA_RECOVERY": 8,
            "AUX_COPY": 16,
            "ER_BACKUP": 32,
            "ARCHIVE_CHECK": 64,
            "TAPE_ERASE": 128,
            "SHELF_MANAGEMENT": 256,
            "ERASE_BACKUP_DATA": 512,
            "ERASE_MIGRATED_DATA": 1024,
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
            end_date = int(time.time()) + 31556926
        if start_time is None:
            start_time = 0
        if end_time is None:
            end_time = 86340

        operations_list = []
        if operations is None:
            operations_list = [1]
        else:
            for i in operations:
                operations_list.append(operation_mapping[i.upper()])

        day_of_week_list = []
        if day_of_week is None:
            day_of_week_list = [0, 1, 2, 3, 4, 5, 6]
        else:
            for i in day_of_week:
                day_of_week_list.append(day_of_week_mapping[i.lower()])

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
                    return response.json()['operationWindow']['ruleId']
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
        """Deletes the OperationWindow with the rule Id given as input.

            Args:
                rule_id       (int)   --  Rule Id of the operation window

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
                if int(error_code) != 0:
                    raise SDKException(
                        'OperationWindow', '103', response.json()["error"]['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response(
                response.text)
            raise SDKException('Response', '101', response_string)

    def list_operation_window(self):
        """Lists the OperationWindows for the client Id given as input.

            Args:
               None

            Returns:
                Returns the List of operation window created for a given client

            Raises:
                SDKException:
                    if the Operation windows could not be Listed

                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self.connect_string)
        if flag:
            if response.json():
                error_code = response.json()["error"]['errorCode']
                if int(error_code) == 0:
                    return response.json()
                else:
                    raise SDKException(
                        'OperationWindow', '104', response.json()["error"]['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response(
                response.text)
            raise SDKException('Response', '101', response_string)
