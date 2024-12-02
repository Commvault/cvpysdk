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

"""Main file for performing plan operations.

Plans,PlanTypes and Plan are the classes defined in this file.

Plans: Class for representing all the plans in the commcell

PlanTypes : Class for representing plan types

Plan: Class for representing a single plan of the commcell

Plans
=====

    __init__(commcell_object)   --  initialise object of plans class of the commcell

    __str__()                   --  returns all the plans associated with the commcell

    __repr__()                  --  returns the string for the instance of the plans class

    __len__()                   --  returns the number of plans added to the Commcell

    __getitem__()               --  returns the name of the plan for the given plan Id
    or the details for the given plan name

    _get_plans()                --  gets all the plans associated with the commcell specified

    _get_plan_template()        --  gets the Plan subtype's JSON template

    add()                       --  adds a new Plan to the CommCell

    has_plan()                  --  checks if a plan exists with the given name or not

    get()                       --  returns the instance of the Plans class

    delete()                    --  deletes the plan from the commcell

    refresh()                   --  refresh the plans associated with the commcell

    add_data_classification_plan()-  Adds data classification plan to the commcell

    get_supported_solutions()   --  returns the supported solutions for plans

    add_exchange_plan()         --  Adds a new exchange plan to the commcell

    create_server_plan()        --  creates a new server plan to the commcell

    _get_fl_parameters()        --  Returns the fl parameters to be passed in the mongodb caching api call

    _get_sort_parameters()      --  Returns the sort parameters to be passed in the mongodb caching api call

    _get_fq_parameters()        --  Returns the fq parameters based on the fq list passed

    get_plans_cache()           --  Returns plan cache in response
    
Attributes
----------

    **all_plans**   --  returns the dict consisting of plans and their details

    **all_plans_cache** --  Returns the dictionary consisting of all the plans cache present in mongoDB


Plan
====

    __init__()                  -- initialise instance of the plan for the commcell

    __repr__()                  -- return the plan name, the instance is associated with

    _get_plan_id()              -- method to get the plan id, if not specified in __init__

    _get_plan_properties()      -- get the properties of this plan

    _update_plan_props()        -- method to update plan properties

    _get_associated_entities()  -- method to get list of entities associated to a plan

    _enable_content_indexing_o365_plan() --method to enable content indexing for O365 plan

    derive_and_add()            -- add new plan by deriving from the parent Plan object

    plan_name                   --  returns the name of the plan

    plan_id                     --  returns the ID of the plan

    refresh()                   --  refresh the properties of the plan

    associate_user()            --  associates users to the plan

    modify_schedule()           --  modifies the RPO schedules of the plan

    add_storage_copy()          --  adds a storage pool as a copy to the plan

    disable_full_schedule()     --  disables the full schedule of a plan

    share()                     --  shares plan with given user by associating given role

    schedule()                  --  create/delete schedule on DC Plan

    edit_plan()                 --  edit plan options
    
    update_security_associations() -- to update security associations of a plan

    get_plan_properties()       --  method to get the properties of the plan fetched via v4 API
    
    get_storage_copy_details()  --  method to get storage copy details

    get_storage_copy_id()       --  method to get storage copy id

    add_copy()                  --  method to add a copy to the plan

    edit_copy()                 --  method to edit a copy of the plan

    delete_copy()               --  method to delete a copy from the plan

    add_region()                --  method to add a region to the plan

    remove_region()             --  method to remove a region from the plan

    get_schedule_properties()   --  method to get the schedule properties of the plan

    add_schedule()              --  method to add a schedule to the plan

    edit_schedule()             --  method to edit a schedule of the plan

    delete_schedule()           --  method to delete a schedule from the plan

    edit_snapshot_options()     --  method to edit snapshot options of the plan

    update_backup_content()     --  method to update backup content of the plan

    enable_data_aging()         --  Enable data aging for the copy of the plan

Plan Attributes
----------------
    **plan_id**                 --  returns the id of the plan

    **plan_name**               --  returns the name of the plan

    **sla_in_minutes**          --  returns the SLA/RPO of the plan

    **plan_type**               --  returns the type of the plan

    **subtype**                 --  returns the subtype of the plan

    **override_entities**       --  returns the override restrictions of the plan

    **storage_policy**          --  returns the storage policy of the plan

    **schedule_policies**       --  returns the schedule policy of the plan

    **subclient_policy**        --  returns the subclient policy of the plan

    **associated_entities**     --  returns all the backup entities associated with the plan

    **operation_window**        --  returns the incremental operation window set by the plan

    **full_operation_window**   --  returns the full operation window set by the plan

    **associated_entities**     --  returns all the entities associated with the plan

    **content_indexing_props**  --  returns the DC plan related properties from the plan

    **region_id**               --  Returns the Backup destination region id

    **company**                 --  Returns the company of the plan

    **resources**               --  Returns the resources stored in storage resource pool
    
    **applicable_solutions**    --  returns applicable solutions configured on server plan

    **data_schedule_policy**    --  returns the data schedule policy of the plan

    **log_schedule_policy**     --  returns the log schedule policy of the plan

    **snap_schedule_policy**    --  returns the snap schedule policy of the plan

    **content_indexing**        --  returns the status of content indexing of O365 plan

"""
from __future__ import unicode_literals

import copy
from enum import Enum

from .exception import SDKException
from .security.security_association import SecurityAssociation
from .activateapps.constants import TargetApps, PlanConstants
from functools import reduce
from typing import List, Tuple, Dict, Union

class PlanTypes(Enum):
    """Class Enum to represent different plan types"""
    Any = 0
    DLO = 1
    MSP = 2
    FS = 3
    SNAP = 4
    VSA = 5
    EXCHANGE = 6
    DC = 7
    EDISCOVERY = 8
    ARCHIVER = 9

class _PayloadGeneratorPlanV4:
    """Class to provide payload for creating/modifying server plans using V4 API."""

    def __init__(self, commcell):
        """Initialize the _PayloadGeneratorPlanV4 class instance"""
        self.__commcell = commcell

    def get_copy_payload(self, copy_details: dict, is_aux_copy: bool=False) -> dict:
        """
            Method to get single copy details payload based on the provided configuration.

            Args:
                - copy_details (dict): Configuration for the copy.
                Should contain the following keys:
                    - 'storage_name' (str): Name of the storage.
                    - 'retentionPeriodDays' (int): Retention days for the copy (Default: 30 days)
                    - 'backupDestinationName' (str): Name of the copy (Default: 'Primary')
                    - 'region_name' (str, optional): Name of the region
                    - 'storageTemplateTags' (dict): To indentify storage based on tags (Needed only for Global Plans)

                Note: Additional properties can be sent in the input to update the payload with the same exact key names.
                    
                - is_aux_copy (bool, optional): Indicates if the copy is an aux copy. Default: False
                    
            Returns:
                dict: Copy details as a dictionary.
        """
        # validate the input
        if 'storageTemplateTags' not in copy_details and 'storage_name' not in copy_details:
            raise SDKException('Plan', '102', 'Storage details is required for copy configuration.')
        
        temp_dict = copy_details.copy() # make a copy of the input to avoid modifying the original input

        payload = {
            "backupDestinationName": copy_details.get("backupDestinationName", "Primary"),
            "retentionPeriodDays": copy_details.get("retentionPeriodDays", 30),
            "useExtendedRetentionRules": False,
            "overrideRetentionSettings": True,
            "backupStartTime": -1,
        }

        # If storage_name is provided, update the payload with storage details
        if 'storage_name' in copy_details:
            storage_pool = self.__commcell.storage_pools.get(copy_details["storage_name"])
            payload['storagePool'] = {
                "id": int(storage_pool.storage_pool_id),
                "name": storage_pool.storage_pool_name
            }
            payload['storageType'] = storage_pool.storage_pool_properties['storagePoolDetails']['libraryList'][0]['model'].upper()

        # Add aux copy specific properties
        if is_aux_copy:
            payload["backupsToCopy"] = copy_details.get("backupsToCopy", "All_JOBS")

        # Add region if available
        if region_name := copy_details.get("region_name"):
            payload["region"] = {"id": int(self.__commcell.regions.get(region_name).region_id)}

            # remove the keys that are already set and doesnot match payload keys
            temp_dict.pop('region_name')

        # If the input as advanced properties like extended retention or others, update the payload
        payload = self.update_payload(original_payload=payload, update_info_dict=temp_dict)

        return payload

    def get_backupdestinations_payload(self, destinations_config: List[dict]) -> list:
        """
            Method to get the payload for multiple copies based on the provided configuration.

            Args:
                - destinations_config (list): List of dictionaries representing copy configurations.
                Each dictionary should contain the following keys:
                    - 'storage_name' (str): Name of the storage.
                    - 'retentionPeriodDays' (int): Retention days for the copy (Default: 30 days)
                    - 'backupDestinationName' (str): Name of the copy (Default: 'Primary')
                    - 'region_name' (str, optional): Name of the region

                Note: Additional properties can be sent in the input to update the payload with the same exact key names.

            Returns:
                dict: Backup destinations payload as a dictionary.
            """
        backup_destinations = []

        # primary copy
        copy_details = self.get_copy_payload(destinations_config[0], is_aux_copy=False)
        backup_destinations.append(copy_details)

        # aux copies
        for copy_config in destinations_config[1:]:
            copy_details = self.get_copy_payload(copy_config, is_aux_copy=True)
            backup_destinations.append(copy_details)

        return backup_destinations

    def get_schedule_payload(self, schedule_details: Dict) -> Dict:
        """
        Method to get the payload for a single schedule based on the provided configuration.

        Args:
            - backupType (str): Type of backup schedule
            - scheduleOperation (str): Operation to perform on the schedule. (Default: ADD)
            - forDatabasesOnly (bool): Indicates if the schedule is for databases only (Default: False)

            For scheduleOperation = MODIFY / DELETE:
            - scheduleId (int): ID of the schedule
            - policyId (int): ID of the policy

            Note: Additional properties can be sent in the input to update the payload with the same exact key names. Get the path and key names from the API documentation or Command Center equivalent API.

        Returns:
            dict: Schedule details as a dictionary.
        """
        # Validate the input
        if 'backupType' not in schedule_details:
            raise SDKException('Plan', '102', 'backupType is required for schedule configuration.')

        operation_type = schedule_details.get('scheduleOperation', 'ADD')
        if operation_type in ['MODIFY', 'DELETE']:
            if 'scheduleId' not in schedule_details or 'policyId' not in schedule_details:
                raise SDKException('Plan', '102', 'scheduleId and policyId are required for MODIFY / DELETE operations.')

        payload = {}
        backup_type = schedule_details['backupType']
        is_transaction_log = backup_type == "TRANSACTIONLOG"

        # Set default values for the payload
        if is_transaction_log:
            payload['schedulePattern'] = {
                "scheduleFrequencyType": "AUTOMATIC",
                "maxBackupIntervalInMins": 240
            }
            payload['scheduleOption'] = {
                "useDiskCacheForLogBackups": False,
                "commitFrequencyInHours": 8,
                "logsDiskUtilizationPercent": 80,
                "logFilesThreshold": 50
            }
            payload['forDatabasesOnly'] = True
        else:
            payload['schedulePattern'] = {
                "scheduleFrequencyType": "DAILY",
                "startTime": 75600,
                "frequency": 1
            }
            payload['forDatabasesOnly'] = False

        payload['scheduleOperation'] = operation_type

        # Update the payload with the provided input details
        # This will override the default values
        # This will also set advanced properties for schedule if provided in the input
        payload = self.update_payload(original_payload=payload, update_info_dict=schedule_details)
        
        return payload

    def get_rpo_payload(self, schedules: List[dict]) -> dict:
        """
            Method to get the payload for multiple schedules based on the provided configuration

            Args:
                - backupType (str): Type of backup
                - scheduleOperation (str): Operation to perform on the schedule. (Default: ADD)
                - forDatabasesOnly (bool): Indicates if the schedule is for databases only (Default: False)

                Note: Additional properties can be sent in the input to update the payload with the same exact key names.

            Returns:
                dict: Full schedule payload as a dictionary.
        """
        schedules_payload = []

        for schedule_config in schedules:
            schedule_details = self.get_schedule_payload(schedule_config)
            schedules_payload.append(schedule_details)

        return {"schedules": schedules_payload}

    def get_create_server_plan_payload(self, plan_name: str, backup_destinations: List[dict], schedules: List[dict], **additional_params) -> dict:
        """
            Method to get a payload for creating a server plan.

            Args:
                - plan_name (str): Name of the backup plan.
                - backup_destinations (list): List of dictionaries representing backup destinations.
                - schedules (list): List of dictionaries representing backup schedules.

                - additional_params (dict): Additional parameters for the plan. Include:
                - rpo_backup_window (list, optional): Backup window for RPO schedules.
                - full_backup_window (list, optional): Backup window for full backup schedules.
                - enable_backup_copy (bool, optional): Enable backup copy.
                - backup_copy_rpo_mins (int, optional): RPO for backup copy in minutes.
                - snap_retention_days (int, optional): Retention period in days.
                - snap_recovery_points (int, optional): Snap recovery point.

            Returns:
                dict: Payload for creating a backup plan.
            """
        plan_payload = {
            "planName": plan_name,
            "backupDestinations": self.get_backupdestinations_payload(backup_destinations),
            "rpo": {
                "backupFrequency": self.get_rpo_payload(schedules),
                "backupWindow": additional_params.get("rpo_backup_window", []),
                "fullBackupWindow": additional_params.get("full_backup_window", [])
            },
            "snapshotOptions": {
                "enableBackupCopy": additional_params.get("enable_backup_copy", True),
                "backupCopyRPOMins": additional_params.get("backup_copy_rpo_mins", 240)
            }
        }

        if snap_recovery_points := additional_params.get("snap_recovery_points"):
            plan_payload["snapshotOptions"]["snapRecoveryPoints"] = snap_recovery_points
            plan_payload["snapshotOptions"]["retentionRuleType"] = 'SNAP_RECOVERY_POINTS'
        else:
            plan_payload["snapshotOptions"]["retentionPeriodDays"] = additional_params.get("snap_retention_days", 30)
            plan_payload["snapshotOptions"]["retentionRuleType"] = 'RETENTION_PERIOD'

        return plan_payload

    def update_payload(self, original_payload, update_info_dict) -> Dict:
        """
        Recursively update the original dictionary with the values from the update dictionary.

        This function handles nested dictionaries, allowing for updates at different levels of depth.

        Args:
            original_payload (dict): The original dictionary to be updated.
            update_info_dict (dict): The dictionary containing values for update.

        Returns:
            dict: The updated dictionary.

        Example:
            >>> original = {'a': 1, 'b': {'c': 2, 'd': 3}}
            >>> update = {'b': {'d': 4}, 'e': 5}
            >>> updated = update_payload(original, update)
            >>> print(updated)
            {'a': 1, 'b': {'c': 2, 'd': 4}, 'e': 5}
        """
        for key, value in update_info_dict.items():
            if isinstance(value, dict):
                original_payload[key] = self.update_payload(original_payload.get(key, {}), value)
            else:
                original_payload[key] = value
        return original_payload

class Plans(object):
    """Class for representing all the plans in the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of Plans class.

            Args:
                commcell_object (object)  -- instance of the Commcell class

            Returns:
                object - instance of Plans class
        """

        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._PLANS = self._services['PLANS']
        self._V4_PLANS = self._services['V4_SERVER_PLANS']
        self._V4_GLOBAL_PLANS = self._services['V4_GLOBAL_SERVER_PLANS']
        self._plans = None
        self._plans_cache = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all plans of the Commcell.

            Returns:
                str - string of all the plans for a commcell
        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'Plan')

        for index, plan in enumerate(self._plans):
            sub_str = '{:^5}\t{:30}\n'.format(index + 1, plan)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Plans class."""
        return "Plans class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the plans added to the Commcell."""
        return len(self.all_plans)

    def __getitem__(self, value):
        """Returns the name of the plan for the given plan ID or
            the details of the plan for given plan Name.

            Args:
                value   (str / int)     --  Name or ID of the plan

            Returns:
                str     -   name of the plan, if the plan id was given

                dict    -   dict of details of the plan, if plan name was given

            Raises:
                IndexError:
                    no plan exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_plans:
            return self.all_plans[value]
        else:
            try:
                return list(filter(lambda x: x[1]['id'] == value, self.all_plans.items()))[0][0]
            except IndexError:
                raise IndexError('No plan exists with the given Name / Id')

    def _get_plans(self):
        """Gets all the plans associated with the commcell

            Returns:
                dict - consists of all plans in the commcell
                    {
                        "plan1_name": plan1_id,
                        "plan2_name": plan2_id
                    }

                Raises:
                    SDKException:
                        if response is empty

                        if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._PLANS)

        if flag:
            plans = {}

            if response.json() and 'plans' in response.json():
                response_value = response.json()['plans']

                name_count = {}

                for temp in response_value:
                    temp_name = temp.get('plan', {}).get('planName', '').lower()
                    temp_company = temp.get('plan', {}).get('entityInfo', {}).get('companyName', '').lower()

                    if temp_name in name_count:
                        name_count[temp_name].add(temp_company)
                    else:
                        name_count[temp_name] = {temp_company}

                for temp in response_value:
                    temp_name = temp.get('plan', {}).get('planName', '').lower()
                    temp_id = str(temp['plan']['planId']).lower()
                    temp_company = temp.get('plan', {}).get('entityInfo', {}).get('companyName', '').lower()

                    if len(name_count[temp_name]) > 1:
                        unique_key = f"{temp_name}_({temp_company})"
                    else:
                        unique_key = temp_name

                    plans[unique_key] = temp_id

            return plans
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_plan_template(self, plan_sub_type, plan_type="MSP"):
        """Gets the Plan subtype's JSON template.

            Args:
                plan_sub_type    (str)   --  Sub-type of plan to add

                    "Server"    -   Server Plans

                    "FSServer"  -   File System Plans

                    "Laptop"    -   Laptop Plans


                plan_type       (str)   --  Type of plan to add

                    default: "MSP"

            Returns:
                str     -   JSON string of the Plan's template

            Raises:
                SDKException:
                    if type or subtype of the plan does not exist

                    if there is a failure in getting the template

        """
        if not (isinstance(plan_sub_type, str) and
                isinstance(plan_type, str)):
            raise SDKException('Plan', '101')
        else:
            template_url = self._services['GET_PLAN_TEMPLATE'] % (plan_type, plan_sub_type)

            flag, response = self._cvpysdk_object.make_request('GET', template_url)

            if flag:
                if response.json() and 'plan' in response.json():
                    return response.json()
                else:
                    raise SDKException('Plan', '102', 'Failed to get Plan template')
            else:
                response_string = self._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

    def _get_fl_parameters(self, fl: list = None) -> str:
        """
        Returns the fl parameters to be passed in the mongodb caching api call

        Args:
            fl    (list)  --   list of columns to be passed in API request

        Returns:
            fl_parameters(str) -- fl parameter string
        """
        self.valid_columns = {
            'planName': 'plans.plan.planName',
            'planId': 'plans.plan.planId',
            'planType': 'plans.subtype',
            'numAssocEntities': 'plans.numAssocEntities',
            'rpoInMinutes': 'plans.rpoInMinutes',
            'numCopies': 'plans.numCopies',
            'planStatusFlag': 'plans.planStatusFlag',
            'storage': 'plans.storageResourcePoolMaps.resources.resourcePool',
            'company': 'plans.plan.entityInfo.companyName',
            'tags': 'tags'
        }
        default_columns = 'plans.plan.planName,plans.plan.planId'

        if fl:
            if all(col in self.valid_columns for col in fl):
                fl_parameters = f"&fl={default_columns},{','.join(self.valid_columns[column] for column in fl)}"
            else:
                raise SDKException('Plan', '102', 'Invalid column name passed')
        else:
            fl_parameters = f"&fl={default_columns},{','.join(column for column in self.valid_columns.values())}"

        return fl_parameters

    def _get_sort_parameters(self, sort: list = None) -> str:
        """
        Returns the sort parameters to be passed in the mongodb caching api call

        Args:
            sort  (list)  --   contains the name of the column on which sorting will be performed and type of sort
                                valid sor type -- 1 for ascending and -1 for descending
                                e.g. sort = ['connectName','1']

        Returns:
            sort_parameters(str) -- sort parameter string
        """
        sort_type = str(sort[1])
        col = sort[0]
        if col in self.valid_columns.keys() and sort_type in ['1', '-1']:
            sort_parameter = '&sort=' + self.valid_columns[col] + ':' + sort_type
        else:
            raise SDKException('Plan', '102', 'Invalid column name passed')
        return sort_parameter

    def _get_fq_parameters(self, fq: list = None) -> str:
        """
        Returns the fq parameters based on the fq list passed
        Args:
             fq     (list) --   contains the columnName, condition and value
                    e.g. fq = [['planName','contains', test'],['numAssocEntities','between', '0-1']]

        Returns:
            fq_parameters(str) -- fq parameter string
        """
        conditions = ['contains', 'notContain', 'eq', 'neq', 'gt', 'lt']
        params = [""]
        if fq:

            for param in fq:
                if param[0] in self.valid_columns.keys():
                    if param[0] == 'tags' and param[1] =='contains':
                        params.append(f"&tags={param[2]}")
                    elif param[1] in conditions:
                        params.append(f"&fq={self.valid_columns[param[0]]}:{param[1].lower()}:{param[2]}")
                    elif param[1] == 'isEmpty' and len(param) == 2:
                        params.append(f"&fq={self.valid_columns[param[0]]}:in:null,")
                    elif param[1] == 'between' and '-' in param[2]:
                        ranges = param[2].split('-')
                        params.append(f"&fq={self.valid_columns[param[0]]}:gteq:{ranges[0]}")
                        params.append(f"&fq={self.valid_columns[param[0]]}:lteq:{ranges[1]}")
                    else:
                        raise SDKException('Plan', '102', 'Invalid condition passed')
                else:
                    raise SDKException('Plan', '102', 'Invalid column Name passed')
        if params:
            return "".join(params)

    def get_plans_cache(self, hard: bool = False, **kwargs) -> dict:
        """
        Returns plan cache in response.

        Args:
            hard  (bool)    --   Flag to perform hard refresh on plans cache.
            **kwargs (dict):
                fl (list)   --   List of columns to return in response (default: None).
                sort (list) --   Contains the name of the column on which sorting will be performed and type of sort.
                                       Valid sort type: 1 for ascending and -1 for descending
                                       e.g. sort = ['columnName', '1'] (default: None).
                limit (list)--   Contains the start and limit parameter value.
                                        Default ['0', '100'].
                search (str)--   Contains the string to search in the commcell entity cache (default: None).
                fq (list)   --   Contains the columnName, condition, and value.
                                        e.g. fq = [['planName', 'contains', 'test'],
                                        ['numAssocEntities', 'between', '0-1']] (default: None).
                enum (bool) --   Flag to return enums in the response (default: True).

        Returns:
            dict: Dictionary of all the properties present in response.
        """
        headers = self._commcell_object._headers.copy()
        if kwargs.get('enum', True):
            headers['EnumNames'] = "True"

        fl_parameters = self._get_fl_parameters(kwargs.get('fl', None))
        fq_parameters = self._get_fq_parameters(kwargs.get('fq', None))
        limit = kwargs.get('limit', ['0', '100'])
        limit_parameters = f'start={limit[0]}&limit={limit[1]}'
        hard_refresh = '&hardRefresh=true' if hard else ''
        sort_parameters = self._get_sort_parameters(kwargs.get('sort', None)) if kwargs.get('sort', None) else ''
        search_parameter = f'&search={",".join(self.valid_columns.values())}:contains:{kwargs.get("search", None)}' if kwargs.get(
            'search', None) else ''

        request_url = (
                self._PLANS + "?" + limit_parameters + sort_parameters + fl_parameters + fq_parameters +
                hard_refresh + search_parameter
        )
        flag, response = self._cvpysdk_object.make_request("GET", request_url, headers=headers)

        if not flag:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        plans_summary = {}
        if response.json() and 'plans' in response.json():
            for plan in response.json()['plans']:
                name = plan.get("plan", {}).get("planName", None)
                plan_config = {
                    'planId': plan.get('plan', {}).get('planId', None),
                    'planType': plan.get('subtype'),
                    'numCopies': plan.get('numCopies'),
                    'numAssocEntities': plan.get('numAssocEntities'),
                    'rpoInMinutes': plan.get('rpoInMinutes'),
                    'planStatusFlag': plan.get('planStatusFlag'),
                    'company': plan.get('plan', {}).get('entityInfo', {}).get('companyName', None)
                }
                if 'storageResourcePoolMaps' in plan and 'resources' in plan.get('storageResourcePoolMaps', {})[0]:
                    plan_config['storage'] = [
                        resource.get('resourcePool', {}).get('resourcePoolName')
                        for resource in plan.get('storageResourcePoolMaps', {})[0].get('resources')
                    ]
                if 'tags' in plan.get('plan'):
                    plan_config['tags'] = plan.get('plan', None).get('tags')
                plan_config = {key: value for key, value in plan_config.items() if value is not None}
                plans_summary[name] = plan_config

            return plans_summary
        else:
            raise SDKException("Plan", "102", "Failed to get plans summary")

    @property
    def all_plans(self):
        """Returns the dictionary consisting of all the plans added to the Commcell.

            dict - consists of all the plans configured on the commcell

                {
                    "plan1_name": plan1_id,

                    "plan2_name": plan2_id
                }

        """
        return self._plans

    @property
    def all_plans_cache(self):
        """Returns the dictionary consisting of all the plans cache present in mongoDB

                    dict - consists of all the plans configured on the commcell

                        {
                        "plan1_name":
                         {
                         id : <plan's id>,
                         Type : <type of plan>,
                         subtype : <sub type of plan>,
                         status: <status of the plan>,
                         numCopies: <number of copies>,
                         numAssocEntities: <associated Entities Count>,
                         RPO: <rpo in minutes>,
                         planStatusFlag: <status of plan>,
                         company: <name of the company plan belongs to>
                         },

                        "plan2_name":
                         {
                         id : <plan's id>,
                         Type : <type of plan>,
                         subtype : <sub type of plan>,
                         status: <status of the plan>,
                         numCopies: <number of copies>,
                         numAssocEntities: <associated Entities Count>,
                         RPO: <rpo in minutes>,
                         planStatusFlag: <status of plan>,
                         company: <name of the company plan belongs to>
                         },
                    }

                """
        return self._plans_cache
    
    def filter_plans(self, plan_type, company_name=None):
        """
        Returns the dictionary consisting of specified type and company plans.

        Args:
            plan_type (str)      --      Type of plan ['DLO', 'Server', 'Laptop', 'Database', 'FSServer', 'FSIBMiVTL', 'Snap', 'VSAServer', 'VSAReplication', 
                                                        'ExchangeUser', 'ExchangeJournal', 'Office365', 'Dynamics365', 'DataClassification', 'Archiver']
            company_name (str)    --     To filter plans based on the company. For Commcell, company_name = 'Commcell'. Default will return all plans

        Returns:
            dict - consists of all the plans with specified types configured on the commcell
                {
                    "plan1_name": plan1_id,
                    "plan2_name": plan2_id
                }

        Raises:
            SDKException:
                if input data type is not valid
                if an invalid plan type is passed as a parameter
                if failed to get the response
        """
        if not isinstance(plan_type, str):
            raise SDKException('Plan', '101')
        
        plan_type_lower = plan_type.lower()
        
        if plan_type_lower not in ["dlo", "server", "laptop", "database", "fsserver", "fsibmivtl", "snap", 
                                    "vsaserver", "vsareplication", "exchangeuser", "exchangejournal", 
                                    "office365", "dynamics365", "dataclassification", "archiver"]:
            raise SDKException('Plan', '102', 'Invalid Plan Type Passed as Parameter')

        params = f"fq=plans.subtype%3Ain%3A{plan_type}&fl=plans.plan.planId%2Cplans.plan.planName%2Cplans.subtype%2Cplans.type"

        if company_name:
            company_id = (
                self._commcell_object.organizations.get(company_name).organization_id 
                if company_name != 'Commcell' else 0
            )
            params += f"&fq=companyId%3Aeq%3A{company_id}"

        template_url = self._services['PLAN_SUMMARY'] % params

        flag, response = self._cvpysdk_object.make_request('GET', template_url)

        if flag:
            result = dict()
            if 'plans' in response.json():
                for plan in response.json()['plans']:
                    result[plan['plan']['name']] = plan['plan']['id']
            return result
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_plan(self, plan_name):
        """Checks if a plan exists in the commcell with the input plan name.

            Args:
                plan_name   (str)   --  name of the plan

            Returns:
                bool    -   boolean output whether the plan exists in the commcell or not

            Raises:
                SDKException:
                    if type of the plan name argument is not string

        """
        if not isinstance(plan_name, str):
            raise SDKException('Plan', '101')

        return self._plans and plan_name.lower() in self._plans

    def get(self, plan_name):
        """Returns a plan object of the specified plan name.

            Args:
                plan_name (str)  --  name of the plan

            Returns:
                object - instance of the Plan class for the the given plan name

            Raises:
                SDKException:
                    if type of the plan name argument is not string

                    if no plan exists with the given name
        """
        if not isinstance(plan_name, str):
            raise SDKException('Plan', '101')
        else:
            plan_name = plan_name.lower()

            if self.has_plan(plan_name):
                return Plan(
                    self._commcell_object,
                    plan_name,
                    self._plans[plan_name]
                )

            raise SDKException(
                'Plan', '102', 'No plan exists with name: {0}'.format(
                    plan_name)
            )

    def delete(self, plan_name):
        """Deletes the plan from the commcell.

            Args:
                plan_name (str)  --  name of the plan to remove from the commcell

            Raises:
                SDKException:
                    if type of the plan name argument is not string

                    if failed to delete plan

                    if response is empty

                    if response is not success

                    if no plan exists with the given name
        """
        if not isinstance(plan_name, str):
            raise SDKException('Plan', '101')
        else:
            plan_name = plan_name.lower()

            if self.has_plan(plan_name):
                plan_id = self._plans[plan_name]

                delete_plan = self._services['DELETE_PLAN'] % (plan_id)

                flag, response = self._cvpysdk_object.make_request('DELETE', delete_plan)

                error_code = 0

                if flag:
                    if 'error' in response.json():
                        if isinstance(response.json()['error'], list):
                            error_code = response.json()['error'][0]['status']['errorCode']
                        else:
                            error_code = response.json()['errorCode']

                    if error_code != 0:
                        o_str = 'Failed to delete plan'
                        if isinstance(response.json()['error'], list):
                            error_message = response.json()['error'][0]['status']['errorMessage']
                        else:
                            error_message = response.json()['errorMessage']
                        o_str += '\nError: "{0}"'.format(error_message)
                        raise SDKException('Plan', '102', o_str)
                    else:
                        # initialize the plan again
                        # so the plan object has all the plan
                        self.refresh()
                else:
                    response_string = self._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'Plan',
                    '102',
                    'No plan exists with name: {0}'.format(plan_name)
                )

    def add_exchange_plan(self, plan_name: str, plan_sub_type: str = 'ExchangeUser', **kwargs):
        """Adds a new exchange plan to the commcell.

            Args:
                plan_name           (str)   --  name of the new plan to add

                plan_sub_type       (str)   --  Type of plan to add - ExchangeUser or ExchangeJournal
                    Default: ExchangeUser

                kwargs              (dict)  --  Optional parameters for creating a plan
                    Accepted Values:
                        retain_msgs_received_time           (int)   -- Retain messages based on received time
                        retain_msgs_deletion_time           (int)   -- Retain messages based on deletion time
                        enable_cleanup_archive_mailbox      (bool)  -- Enable cleanup on archive mailbox
                        cleanup_msg_older_than              (int)   -- Cleanup messages older than
                        cleanup_msg_larger_than             (int)   -- Cleanup messages larger than
                        enable_content_search               (bool)  -- Enable content indexing
                        enable_archive_on_archive_mailbox   (bool)  -- Enable archive on archived mailbox
                        create_stubs                        (bool)  -- Create stubs during cleanup
                        prune_stubs                         (bool)  -- Prune stubs during cleanup
                        prune_msgs                          (bool)  -- Prune messages during cleanup
                        number_of_days_src_pruning          (int)   -- Number of days for source pruning
                        include_msgs_older_than             (int)   -- Include messages older than for archiving
                        include_msgs_larger_than            (int)   -- Inlcude messages larger than for archiving

            Returns:
                Plan object of the created plan

            Raises:
                SDKException:
                    if input parameters are incorrect

                    if Plan already exists

                    if error in creating the plan

        """
        if plan_sub_type not in ['ExchangeUser', 'ExchangeJournal']:
            raise SDKException('Plan', '101', "Plan subtype should be ExchangeUser or ExchangeJournal.")
        elif self.has_plan(plan_name):
                raise SDKException('Plan', '102', 'Plan "{0}" already exists'.format(plan_name))
        request_json = self._get_plan_template(plan_sub_type)
        request_json['plan']['summary']['plan']['planName'] = plan_name
        exch_retention = request_json['plan']['exchange']['mbRetention']['detail']['emailPolicy']['retentionPolicy']
        exch_retention['numOfDaysForMediaPruning'] = kwargs.get('retain_msgs_received_time', -1)
        if plan_sub_type == 'ExchangeUser':
            exch_arch = request_json['plan']['exchange']['mbArchiving']['detail']['emailPolicy']['archivePolicy']
            exch_cleanup = request_json['plan']['exchange']['mbCleanup']['detail']['emailPolicy']['cleanupPolicy']
            exch_cleanup['excludeFolderFilter']['folderPatternsSelected'].remove('Drafts')
            exch_cleanup['excludeFolderFilter']['folderPatternsAvailable'].append('Drafts')
            exch_cleanup['archiveMailbox'] = kwargs.get('enable_cleanup_archive_mailbox', False)
            exch_cleanup['collectMsgsDaysAfter'] = kwargs.get('cleanup_msg_older_than', 0)
            exch_cleanup['collectMsgsLargerThan'] = kwargs.get('cleanup_msg_larger_than', 0)
            exch_cleanup['skipUnreadMsgs'] = kwargs.get('skip_unread_msgs', False)
            exch_cleanup['collectMsgWithAttach'] = kwargs.get('collect_msg_with_attach', False)
            exch_cleanup['createStubs'] = kwargs.get('create_stubs', True)
            exch_cleanup['pruneStubs'] = kwargs.get('prune_stubs', False)
            exch_cleanup['pruneMsgs'] = kwargs.get('prune_msgs', False)
            exch_cleanup['numOfDaysForSourcePruning'] = kwargs.get('number_of_days_src_pruning', 0)
            exch_arch['backupDeletedItemRetention'] = kwargs.get('backup_deleted_item_retention', False)
            if 'includeDiscoveryHoldsFolder' in kwargs:
                exch_arch['includeDiscoveryHoldsFolder'] = kwargs.get('include_discovery_holds_folder')
            if 'includePurgesFolder' in kwargs:
                exch_arch['includePurgesFolder'] = kwargs.get('include_purges_folder')
            if 'includeVersionsFolder' in kwargs:
                exch_arch['includeVersionsFolder'] = kwargs.get('include_versions_folder')
            exch_arch['includeOnlyMsgsWithAttachemts'] = kwargs.get('include_only_msgs_with_attachemts', False)
            exch_arch['includeMsgsOlderThan'] = kwargs.get('include_msgs_older_than', 0)
            exch_arch['includeMsgsLargerThan'] = kwargs.get('include_msgs_larger_than', 0)
            exch_arch['archiveMailbox'] = kwargs.get('enable_archive_on_archive_mailbox', False)
            if 'retain_msgs_deletion_time' in kwargs and kwargs.get('retain_msgs_deletion_time') > 0:
                exch_retention['type'] = 1
                exch_retention['numOfDaysForMediaPruning'] = kwargs.get('retain_msgs_deletion_time', 0)
        else:
            exch_arch = request_json['plan']['exchange']['mbJournal']['detail']['emailPolicy']['journalPolicy']
        exch_arch['contentIndexProps']['enableContentIndex'] = kwargs.get('enable_content_search', False)

        headers = self._commcell_object._headers.copy()
        headers['LookupNames'] = 'False'

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._PLANS, request_json, headers=headers
        )

        if flag:
            if response.json():
                response_value = response.json()
                error_message = None
                error_code = None

                if 'errors' in response_value:
                    error_code = response_value['errors'][0]['status']['errorCode']
                    error_message = response_value['errors'][0]['status']['errorMessage']

                if error_code > 1:
                    o_str = 'Failed to create new Plan\nError: "{0}"'.format(
                        error_message
                    )
                    raise SDKException('Plan', '102', o_str)

                if 'plan' in response_value:
                    plan_name = response_value['plan']['summary']['plan']['planName']

                    self.refresh()
                    self._commcell_object.storage_policies.refresh()
                    return self.get(plan_name)
                else:
                    o_str = ('Failed to create new plan due to error code: "{0}"\n'
                             'Please check the documentation for '
                             'more details on the error').format(error_code)

                    raise SDKException('Plan', '102', o_str)
            else:
                raise SDKException('Response', 102)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def create_server_plan(
        self, plan_name: str, backup_destinations: Union[List[dict], dict], schedules: Union[List[dict], dict]=None, **additional_params
    ) -> object:
        """
            Method to create a server plan using V4 API

            Args:
                plan_name (str)             --  Name of the plan to create

                backup_destinations (list/dict)  --  List of dictionaries representing backup destinations.
                Each dictionary should contain the following keys:
                    - 'storage_name' (str): Name of the storage.
                    - 'retentionPeriodDays' (int): Retention days for the copy (Default: 30 days)
                    - 'backupDestinationName' (str): Name of the copy (Default: 'Primary')
                    - 'region_name' (str, optional): Name of the region
                    To create elastic plans, region_name should be specified for all the copies

                Examples:
                # specify just storage and rest use default values
                {"storage_name": "Backup Storage"}

                # specify storage name and retention period 
                {"storage_name": "Backup Storage", "retentionPeriodDays": 30}

                # create plan with aux copies
                [
                    {"storage_name": "Backup Storage 1"},
                    {"storage_name": "Backup Storage 2", "backupDestinationName": "Aux Copy 1"},
                ]

                # create elastic plan
                {"storage_name": "Backup Storage", "region_name": "asia"}

                # create elastic plan with multiple regions and multiple copies in each region
                [
                    {"storage_name": "Backup Storage 1", "region_name": "asia"},
                    {"storage_name": "Backup Storage 2", "region_name": "asia", "backupDestinationName": "Aux Copy Name"},
                    {"storage_name": "Backup Storage 3", "region_name": "africa"},
                    {"storage_name": "Backup Storage 4", "region_name": "africa", "backupDestinationName": "Aux Copy Name"}
                ]

                Note: Additional properties can be sent in the input to update the payload with the same exact key names. Refer API documentation for more details or use Command Center equivalent API.
                    
                schedules (list or dict, optional)  --  List of dictionaries representing backup schedules.
                Each dictionary should contain the following keys:
                    - backupType (str): Type of backup schedule
                    - forDatabasesOnly (bool): Indicates if the schedule is for databases only (Default: False)
                    - Additional properties to update the default schedule details.

                Examples:

                # create plan with default schedules
                None

                # create plan with no schedules
                []

                # create plan with schedules based on backup type and rest use default values
                {"backupType": "INCREMENTAL"}
                {"backupType": "FULL"}
                {"backupType": "TRANSACTIONLOG"}

                # specify agents for schedules
                {"backupType": "INCREMENTAL", "forDatabasesOnly": False}
                {"backupType": "FULL", "forDatabasesOnly": True}

                # create plan with multiple schedules
                [
                    {"backupType": "INCREMENTAL"},
                    {"backupType": "FULL", "forDatabasesOnly": True},
                    {"backupType": "TRANSACTIONLOG"}
                ]

                # advance properties for schedules
                {"backupType": "TRANSACTIONLOG", "scheduleOption": {"useDiskCacheForLogBackups": True}}

                # specify pattern and start time for schedule
                {
                    "backupType": "INCREMENTAL",
                    "schedulePattern": {
                        "scheduleFrequencyType": "DAILY",
                        "startTime": 75600,
                        "frequency": 1
                    }
                }

                Note: Additional properties can be sent in the input to update the payload with the same exact key names. Refer API documentation for more details or use Command Center equivalent API.
                    
                additional_params (dict)    --  Additional parameters for creating a plan
                    Accepted Values:
                        rpo_backup_window (list, optional): Backup window for RPO schedules.
                        full_backup_window (list, optional): Backup window for full backup schedules.
                        enable_backup_copy (bool, optional): Enable backup copy.
                        backup_copy_rpo_mins (int, optional): RPO for backup copy in minutes.
                        snap_retention_days (int, optional): Retention period in days.
                        snap_recovery_points (int, optional): Snap recovery point.
                        gcm_options (dict, optional): Global Configuration Manager options
                            commcells (list): List of commcell IDs to apply the plan (If not specified, applies to all commcells)

                        For Global Plans, backup_destinations input should be in the following format:

                        Example #1: For Single Copy
                            backup_destinations = {
                                "storageTemplateTags": [
                                    {
                                        "name": "Tag Name",
                                        "value": "Tag Value"
                                    }
                                ]
                            }

                        Example #2: For Multiple Copies
                        backup_destinations = [
                            {
                                'storageTemplateTags': [
                                    {
                                        'name': 'Tag Name 1', 
                                        'value': 'Tag Value 1'
                                    }
                                ]
                            }, 
                            {
                                'backupDestinationName': 'Aux Copy Name', 
                                'storageTemplateTags': [
                                    {
                                        'name': 'Tag Name 2', 
                                        'value': 'Tag Value 2'
                                    }
                                ]
                            }
                        ]

        """
        if schedules is None:
            schedules = [
                {'backupType': 'INCREMENTAL'},
                {'backupType': 'TRANSACTIONLOG'},
            ] # default schedules

        if isinstance(backup_destinations, dict):
            backup_destinations = [backup_destinations]

        if isinstance(schedules, dict):
            schedules = [schedules]

        request_json = _PayloadGeneratorPlanV4(self._commcell_object).get_create_server_plan_payload(
            plan_name, backup_destinations, schedules, **additional_params
        )

        if gcm_options := additional_params.get('gcm_options'):
            service_commcell_ids = gcm_options.get('commcells', [])  # [{'id': 1}, {'id': 2}]
            apply_on_all_commcells = False if service_commcell_ids else True
            request_json = {
            "globalConfigInfo": {
                "commcells": service_commcell_ids,
                "scope": "",
                "scopeFilterQuery": "",
                "applyOnAllCommCells": apply_on_all_commcells
            },
            "plan": request_json
            }

        endpoint = self._V4_GLOBAL_PLANS if gcm_options else self._V4_PLANS
        flag, response = self._cvpysdk_object.make_request('POST', endpoint, request_json)

        if flag:
            if response.json():
                response_value = response.json()
                if 'errors' in response_value:
                    error_message = response_value.get('errors', [{}])[0].get('errorMessage')
                    error_code = response_value.get('errors', [{}])[0].get('errorCode', 0)
                else:
                    error_message = response_value.get('errorMessage')
                    error_code = response_value.get('errorCode', 0)

                # corner case condition
                if error_code == 587207454:
                    raise SDKException('Plan', '102', f'Successfully created plan {response_value["plan"]["name"]} '
                                                      f'with error: {error_message}')
                if error_code != 0:
                    raise SDKException('Plan', '102', f'Failed to create new V4 Server Plan\nError: "{error_message}"')
                
                plan_name = response_value['plan']['name']

                self.refresh()
                self._commcell_object.policies.refresh()

                # refresh storage policies and schedule policies, if refreshing policies is not enough
                # self._commcell_object.storage_policies.refresh()
                # self._commcell_object.schedule_policies.refresh()

                return self.get(plan_name)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add(self,
            plan_name,
            plan_sub_type,
            storage_pool_name=None,
            sla_in_minutes=1440,
            override_entities=None):
        """Adds a new Plan to the CommCell.

        Args:
            plan_name           (str)   --  name of the new plan to add

            plan_sub_type       (str)   --  Type of plan to add

                "Server"    -   Server Plans

                "FSServer"  -   File System Plans

                "Laptop"    -   Laptop Plans

                "ExchangeUser"  -   Exchange Mailbox Plan


            storage_pool_name   (str)   --  name of the storage pool to be used for the plan

            sla_in_minutes      (int)   --  Backup SLA in hours

                default: 1440

            override_entities   (dict)  --  Specify the entities with respective
                                            inheritance values.

                default: None

                    {
                        'privateEntities': [1, 4],

                        'enforcedEntities': [256, 512, 1024]
                    }
                    - where,
                            privateEntities are set when respective entity overriding is required
                            enforcedEntities are set when respective entity overriding is not
                            allowed
                            left blank if overriding is optional

                    - entity IDs,
                            1    - Storage
                            4    - RPO/Schedules
                            256  - Windows content
                            512  - Unix content
                            1024 - Mac content

        Returns:
            object  -   instance of the Plan class created by this method

        Raises:
            SDKException:
                if input parameters are incorrect

                if Plan already exists

        """
        if not (isinstance(plan_name, str) and
                isinstance(plan_sub_type, str)):
            raise SDKException('Plan', '101')
        else:
            if self.has_plan(plan_name):
                raise SDKException(
                    'Plan', '102', 'Plan "{0}" already exists'.format(plan_name)
                )
        storage_pool_obj = self._commcell_object.storage_pools.get(
            storage_pool_name)
        is_dedupe = True
        if 'dedupDBDetailsList' not in storage_pool_obj._storage_pool_properties['storagePoolDetails']:
            is_dedupe = False

        request_json = self._get_plan_template(plan_sub_type, "MSP")
        if plan_sub_type == "Laptop":
            del request_json['plan']['laptop']['accessPolicies']
            
        request_json['plan']['summary']['rpoInMinutes'] = sla_in_minutes
        request_json['plan']['summary']['description'] = "Created from CvPySDK."
        request_json['plan']['summary']['plan']['planName'] = plan_name

        template_schedules = [schedule['subTask']['subTaskName'] for schedule in request_json['plan']['schedule']['subTasks']]
        if 'Synthetic Fulls' in template_schedules:
            synth_full_index = template_schedules.index('Synthetic Fulls')
            request_json['plan']['schedule']['subTasks'][synth_full_index]['options']['commonOpts'][
                'automaticSchedulePattern'].update({
                    'minBackupInterval': 0,
                    'maxBackupIntervalMinutes': 0,
                    'minSyncInterval': 0,
                    'minSyncIntervalMinutes': 0
                })
            request_json['plan']['schedule']['subTasks'][synth_full_index]['options']['commonOpts'][
                'automaticSchedulePattern']['ignoreOpWindowPastMaxInterval'] = True
        del request_json['plan']['schedule']['task']['taskName']
        request_json['plan']['storage']['copy'][0]['useGlobalPolicy'] = {
            "storagePolicyId": int(storage_pool_obj.storage_pool_id)
        }
        if is_dedupe:
            request_json['plan']['storage']['copy'][0]['dedupeFlags'][
                'useGlobalDedupStore'] = 1
        else:
            del request_json['plan']['storage']['copy'][0]['storagePolicyFlags']
            del request_json['plan']['storage']['copy'][0]['dedupeFlags'][
                'enableDeduplication']
            del request_json['plan']['storage']['copy'][0]['dedupeFlags'][
                'enableClientSideDedup']
            del request_json['plan']['storage']['copy'][0]['DDBPartitionInfo']
            request_json['plan']['storage']['copy'][0]['extendedFlags'] = {
                'useGlobalStoragePolicy': 1
                }

        # Configurations for database and snap addons
        if plan_sub_type == "Server" and 'database' in request_json['plan']:
            request_json['plan']['database']['storageLog']['copy'][0]['dedupeFlags'][
                'useGlobalDedupStore'] = 1
            request_json['plan']['database']['storageLog']['copy'][0].pop(
                'DDBPartitionInfo', None
            )
            request_json['plan']['database']['storageLog']['copy'][0]['dedupeFlags'][
                'useGlobalPolicy'] = {
                    "storagePolicyId": int(storage_pool_obj.storage_pool_id)
                }
            
            # From SP36, snap copy wont be created by default during plan creation or present in the template
            if len(request_json['plan']['storage']['copy']) > 1:
                request_json['plan']['storage']['copy'][1]['extendedFlags'] = {
                    'useGlobalStoragePolicy': 1
                }
                request_json['plan']['storage']['copy'][1]['useGlobalPolicy'] = {
                    "storagePolicyId": int(storage_pool_obj.storage_pool_id)
                }

        # Enable full backup schedule
        if plan_sub_type != "Laptop":
            for subtask in request_json['plan']['schedule']['subTasks']:
                if 'flags' in subtask['subTask'] and subtask['subTask']['flags'] == 65536:
                    import copy
                    full_schedule = copy.deepcopy(subtask)
                    del copy
                    full_schedule['subTask'].update({
                        'subTaskName': 'Full backup schedule',
                        'flags': 4194304
                    })
                    full_schedule['pattern'].update({
                        'freq_type': 4,
                        'freq_interval': 1,
                        'name': 'Full backup schedule',
                        'active_end_time': 0
                    })
                    full_schedule['options']['backupOpts']['backupLevel'] = 'FULL'
                    request_json['plan']['schedule']['subTasks'].append(full_schedule)
                    break

        if isinstance(override_entities, dict):
            request_json['plan']['summary']['restrictions'] = 0
            request_json['plan']['inheritance'] = {
                'isSealed': False
            }

            if 'enforcedEntities' in override_entities:
                request_json['plan']['inheritance']['enforcedEntities'] = override_entities[
                    'enforcedEntities']

            if 'privateEntities' in override_entities:
                request_json['plan']['inheritance']['privateEntities'] = override_entities[
                    'privateEntities']
        else:
            request_json['plan']['summary']['restrictions'] = 1
            request_json['plan']['inheritance'] = {
                'isSealed': True
            }

        headers = self._commcell_object._headers.copy()
        headers['LookupNames'] = 'False'

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._PLANS, request_json, headers=headers
        )

        if flag:
            if response.json():
                response_value = response.json()
                error_message = None
                error_code = None

                if 'errors' in response_value:
                    error_code = response_value['errors'][0]['status']['errorCode']
                    error_message = response_value['errors'][0]['status']['errorMessage']

                if error_code > 1:
                    o_str = 'Failed to create new Plan\nError: "{0}"'.format(
                        error_message
                    )
                    raise SDKException('Plan', '102', o_str)

                if 'plan' in response_value:
                    plan_name = response_value['plan']['summary']['plan']['planName']

                    # initialize the plans again
                    # so that the plans object has all the plans
                    self.refresh()
                    # with plan delete storage policy associated might be deleted
                    # initialize storage policy again
                    self._commcell_object.storage_policies.refresh()

                    return self.get(plan_name)
                else:
                    o_str = ('Failed to create new plan due to error code: "{0}"\n'
                             'Please check the documentation for '
                             'more details on the error').format(error_code)

                    raise SDKException('Plan', '102', o_str)
            else:
                raise SDKException('Response', 102)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_eligible_plans(self, entities):
        """Returns dict of plans that are eligible for the specified entities

            Args:
                entities    (dict)  - dictionary containing entities as keys and
                                        their respective IDs as values
                    {
                        'clientId': id,
                        'appId': id,
                        'backupsetId': id
                    }

            Returns:
                dict                - dict of eligible plans

            Raises:
                SDKException:
                    if there is an error in the response
        """
        query = ''
        for i in entities:
            query += '{0}={1}&'.format(i, entities[i])
        requset_url = self._services['ELIGIBLE_PLANS'] % query[0:-1]
        flag, response = self._cvpysdk_object.make_request('GET', requset_url)
        del query

        if flag:
            plans = {}

            if response.json() and 'plans' in response.json():
                response_value = response.json()['plans']

                for temp in response_value:
                    temp_name = temp['plan']['planName'].lower()
                    temp_id = str(temp['plan']['planId']).lower()
                    plans[temp_name] = temp_id

            return plans
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_supported_solutions(self):
        """Method to get supported solutions for plans"""
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._services['PLAN_SUPPORTED_SOLUTIONS']
        )

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))
        
        if response.json() and 'id' in response.json():
            return {solution['name']: solution['id'] for solution in response.json()['id']}
        else:
            raise SDKException('Response', '102')
        
    def refresh(self, **kwargs):
        """
        Refresh the list of plans on this commcell.

            Args:
                **kwargs (dict):
                    mongodb (bool)  -- Flag to fetch plans cache from MongoDB (default: False).
                    hard (bool)     -- Flag to hard refresh MongoDB cache for this entity (default: False).
        """
        mongodb = kwargs.get('mongodb', False)
        hard = kwargs.get('hard', False)

        self._plans = self._get_plans()
        if mongodb:
            self._plans_cache = self.get_plans_cache(hard=hard)

    def add_data_classification_plan(self, plan_name, index_server, target_app=TargetApps.FSO, **kwargs):
        """Adds data classification plan to the commcell

            Args:

                plan_name           (str)       --  Name of plan

                index_server        (str)       --  Index server name


                target_app          (enum)      --  Target app for this plan
                                                        cvpysdk.activateapps.constants.TargetApps

                **kwargs

                    index_content       (bool)      --  Speifies whether to index content or not to index server

                    content_analyzer    (list)      --  list of Content analyzer client name

                    entity_list         (list)      --  list of entities which needs to be extracted

                    classifier_list     (list)      --  list of classifier which needs to be classified

                    enable_ocr          (bool)      --  specifies whether OCR is enabled or not

                    ocr_language        (int)       --  Language to be used when doing OCR
                                                            Default : English (Value-1)

                     Supported Languages:

                                    ENGLISH = 1,
                                    HEBREW = 2,
                                    SPANISH = 3,
                                    FRENCH = 4,
                                    ITALIAN = 5,
                                    DANISH = 6

                    include_docs        (str)       --  Include documents type separated by comma

                    exclude_path        (list)      --  List of paths which needs to be excluded

                    min_doc_size        (int)       --  Minimum document size in MB

                    max_doc_size        (int)       --  Maximum document size in MB

            Returns:

                object  - Plan object

            Raises:

                SDKException:

                        if input is not valid

                        if failed to create plan

                        if failed to find entities/classifier details

        """
        extraction_policy_list = []
        if not (isinstance(plan_name, str) and
                isinstance(index_server, str)):
            raise SDKException('Plan', '101')
        request_json = self._get_plan_template("DataClassification", "MSP")
        request_json['plan']['summary']['description'] = "DC Plan Created from CvPySDK."
        request_json['plan']['summary']['plan']['planName'] = plan_name
        request_json['plan']['options'] = {
            "enableThreatAnalysis": False,
            "targetApps": [
                target_app.value
            ]
        }
        index_server_client_id = self._commcell_object.index_servers.get(index_server).index_server_client_id
        request_json['plan']['eDiscoveryInfo']['analyticsIndexServer'] = {
            'clientId': index_server_client_id
        }
        if target_app.value == TargetApps.FSO.value:
            del request_json['plan']['ciPolicy']['detail']['ciPolicy']['filters']
            request_json['plan']['ciPolicy']['detail']['ciPolicy']['opType'] = PlanConstants.INDEXING_ONLY_METADATA
        elif target_app.value == TargetApps.SDG.value:
            if 'content_analyzer' not in kwargs:
                raise SDKException('Plan', '103')
            ca_list = []
            for ca in kwargs.get('content_analyzer', []):
                ca_client_id = self._commcell_object.content_analyzers.get(ca).client_id
                ca_list.append({
                    'clientId': ca_client_id
                })
            request_json['plan']['eDiscoveryInfo']['contentAnalyzerClient'] = ca_list
            if 'entity_list' not in kwargs and 'classifier_list' not in kwargs:
                raise SDKException('Plan', '104')
            activate_obj = self._commcell_object.activate
            if 'entity_list' in kwargs or 'classifier_list' in kwargs:
                entity_mgr_obj = activate_obj.entity_manager()
                # classifier is also an activate entity with type alone different so append this to entity list itself
                entity_list = []
                for entity in kwargs.get('entity_list', []):
                    entity_list.append(entity)
                for entity in kwargs.get('classifier_list', []):
                    entity_list.append(entity)
                for entity in entity_list:
                    entity_obj = entity_mgr_obj.get(entity)
                    extraction_policy_list.append(entity_obj.container_details)

            request_json['plan']['eePolicy']['policyType'] = 3
            request_json['plan']['eePolicy']['flags'] = 8
            request_json['plan']['eePolicy']['detail'] = {
                "eePolicy": {
                    "copyPrecedence": 0,
                    "extractionPolicyType": 6,  # container entities
                    "extractionPolicy": {
                        "extractionPolicyList": extraction_policy_list
                    }

                }
            }
            if 'index_content' in kwargs:
                request_json['plan']['ciPolicy']['detail']['ciPolicy']['opType'] = kwargs.get(
                    'index_content', PlanConstants.INDEXING_METADATA_AND_CONTENT)
            if 'enable_ocr' in kwargs:
                request_json['plan']['ciPolicy']['detail']['ciPolicy']['enableImageExtraction'] = kwargs.get(
                    'enable_ocr', False)
                request_json['plan']['ciPolicy']['detail']['ciPolicy']['ocrLanguages'] = [kwargs.get('ocr_language', 1)]
            if 'include_docs' in kwargs:
                request_json['plan']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters']['includeDocTypes'] = kwargs.get(
                    'include_docs', PlanConstants.DEFAULT_INCLUDE_DOC_TYPES)
            if 'min_doc_size' in kwargs:
                request_json['plan']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters']['minDocSize'] = kwargs.get(
                    'min_doc_size', PlanConstants.DEFAULT_MIN_DOC_SIZE)
            if 'max_doc_size' in kwargs:
                request_json['plan']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters'][
                    'maxDocSize'] = kwargs.get('max_doc_size', PlanConstants.DEFAULT_MAX_DOC_SIZE)
            if 'exclude_path' in kwargs:
                request_json['plan']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters'][
                    'excludePaths'] = kwargs.get('exclude_path', PlanConstants.DEFAULT_EXCLUDE_LIST)

        headers = self._commcell_object._headers.copy()
        headers['LookupNames'] = 'False'

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._PLANS, request_json, headers=headers
        )

        if flag:
            if response.json():
                response_value = response.json()
                error_message = None
                error_code = None

                if 'errors' in response_value:
                    error_code = response_value['errors'][0]['status']['errorCode']
                    error_message = response_value['errors'][0]['status']['errorMessage']

                if error_code > 1:
                    o_str = 'Failed to create new Plan\nError: "{0}"'.format(
                        error_message
                    )
                    raise SDKException('Plan', '102', o_str)

                if 'plan' in response_value:
                    plan_name = response_value['plan']['summary']['plan']['planName']
                    # initialize the plans again
                    self.refresh()

                    return self.get(plan_name)
                else:
                    o_str = ('Failed to create new plan due to error code: "{0}"\n'
                             'Please check the documentation for '
                             'more details on the error').format(error_code)

                    raise SDKException('Plan', '102', o_str)
            else:
                raise SDKException('Response', 102)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_plans_summary(self) -> dict:

        """Returns plan summary in response

        Returns:
            list - plans summary

        **NOTE - THE FUNCTION WOULD BE DEPRECATED IN SP40 AS GET_PLANS_CACHE() WILL RETURN THE SIMILAR RESPONSE**
        """
        params = "fl=plans.missingEntities%2Cplans.numAssocEntities%2Cplans.numCopies%2Cplans.parent" \
                 "%2Cplans.permissions%2Cplans.plan.planId%2Cplans.plan.planName%2Cplans.planStatusFlag%2Cplans.restrictions%2C" \
                 "plans.rpoInMinutes%2Cplans.subtype%2Cplans.type%2Cplans.targetApps%2Cplans.storageResourcePoolMaps.resources.resourcePool" \
                 "&hardRefresh=true"
        request_url = self._services['PLAN_SUMMARY'] % params

        flags,response = self._cvpysdk_object.make_request('GET',request_url)

        if flags:
            if response.json():
                plans_summary = {entry.get("plan", {}).get("name", None): entry.get("associatedEntities", None)
                                 for entry in response.json()["plans"]}
                return plans_summary
            else:
                raise SDKException("Plan", "102", "Failed to get plans summary")
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def add_office365_plan(self, plan_name)->None:
        """
        Creates Office 365 plan
        Args:
            plan_name (str) : name of the plan to be created
        """
        if not isinstance(plan_name, str):
            raise SDKException('Plan','102','Plan name should be passed as String')
        plan_sub_type = "Office365"
        plan_type = "EXCHANGE"
        office365_plan_template = self._get_plan_template(plan_type=plan_type,plan_sub_type=plan_sub_type)
        office365_plan_template["plan"]["summary"]["plan"]["planName"] = plan_name
        flag, response = self._cvpysdk_object.make_request("POST", self._PLANS ,office365_plan_template)
        if flag:
            if response:
                if response.status_code == 200:
                    self.refresh()
                elif response.status_code == 400:
                    raise SDKException("Plan","102","Bad request")
                elif response.status_code == 401:
                    raise SDKException("Plan", "102", "User is unauthorized to perform create operation")
            else:
                raise SDKException("Plan","102","Response received is empty")
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


class Plan(object):
    """Class for performing operations for a specific Plan."""

    def __init__(self, commcell_object, plan_name, plan_id=None):
        """Initialize the Plan class instance.

            Args:
                commcell_object     (object)  --  instance of the Commcell class

                plan_name           (str)     --  name of the plan

                plan_id             (str)     --  id of the plan
                    default: None

            Returns:
                object - instance of the Plan class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._plan_name = plan_name.lower()
        self._plan_properties = None

        if plan_id:
            self._plan_id = str(plan_id)
        else:
            self._plan_id = self._get_plan_id()

        self._PLAN = self._services['PLAN'] % (self.plan_id)
        self._V4_PLAN = self._services['V4_SERVER_PLAN'] % (self.plan_id)
        self._PLAN_RPO = self._services['SERVER_PLAN_RPO'] % (self.plan_id)
        self._ADD_USERS_TO_PLAN = self._services['ADD_USERS_TO_PLAN'] % (self.plan_id)
        self._API_SECURITY = self._services['SECURITY_ASSOCIATION']
        self._API_SECURITY_ENTITY = self._services['ENTITY_SECURITY_ASSOCIATION']
        self._SERVER_PLAN_BACKUP_DESTINATION = self._services['V4_SERVER_PLAN_BACKUP_DESTINATION'] % (self.plan_id)

        self._properties = None
        self._sla_in_minutes = None
        self._operation_window = None
        self._full_operation_window = None
        self._plan_type = None
        self._subtype = None
        self._security_associations = {}
        self._provider_domain_name = None
        self._resources = None
        self._storage_pool = None
        self._child_policies = {
            'storagePolicy': None,
            'schedulePolicy': {},
            'subclientPolicyIds': []
        }
        self._storage_copies = {}
        self._user_group = None
        self._client_group = None
        self._override_entities = None
        self._parent_plan_name = None
        self._addons = []
        self._associated_entities = {}
        self._dc_plan_props = {}
        self._plan_entity_type = 158
        self._region_id = []
        self._applicable_solutions = []
        self._v4_plan_properties = {}
        self.refresh()
        self.plan_v4_helper = _PayloadGeneratorPlanV4(commcell=self._commcell_object)
        self._data_schedule_policy = None
        self._log_schedule_policy = None
        self._snap_schedule_policy = None

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Plan class instance for plan: "{0}", of Commcell: "{1}"'

        return representation_string.format(
            self._plan_name, self._commcell_object.commserv_name
        )

    def _get_plan_id(self):
        """Gets the plan id associated with this plan.

            Returns:
                str - id associated with this plan
        """
        plans = Plans(self._commcell_object)
        return plans.get(self.plan_name).plan_id

    def _get_v4_plan_properties(self) -> Dict:
        """Gets the properties of this plan from V4 API

            Returns:
                dict - dictionary consisting of the properties of this plan

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._V4_PLAN)

        if flag:
            if response.json():
                self._v4_plan_properties = response.json()
                return self._v4_plan_properties
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_plan_properties(self):
        """Gets the plan properties of this plan.

            Returns:
                dict - dictionary consisting of the properties of this plan

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        plan_properties_url = '{0}?propertyLevel=30'.format(self._PLAN)
        flag, response = self._cvpysdk_object.make_request('GET', plan_properties_url)

        if flag:
            if response.json() and 'plan' in response.json():
                self._plan_properties = response.json()['plan']

                if 'planName' in self._plan_properties['summary']['plan']:
                    self._plan_name = self._plan_properties['summary']['plan']['planName'].lower()

                if 'slaInMinutes' in self._plan_properties['summary']:
                    self._sla_in_minutes = self._plan_properties['summary']['slaInMinutes']

                if 'type' in self._plan_properties['summary']:
                    self._plan_type = self._plan_properties['summary']['type']

                if 'subtype' in self._plan_properties['summary']:
                    self._subtype = self._plan_properties['summary']['subtype']

                if 'storage' in self._plan_properties:
                    if 'copy' in self._plan_properties['storage']:
                        for copy in self._plan_properties['storage']['copy']:
                            if 'useGlobalPolicy' in copy:
                                storage_pool_name = copy['useGlobalPolicy']['storagePolicyName'].lower()
                            else:
                                storage_pool_name = copy['library']['libraryName'].lower()
                            self._storage_copies[copy['StoragePolicyCopy']['copyName']] = {
                                'storagePool': storage_pool_name,
                                'retainBackupDataForDays': copy[
                                    'retentionRules']['retainBackupDataForDays'],
                                'isDefault': False,
                                'isSnapCopy': False,
                            }
                            if 'extendedRetentionRuleOne' in copy['retentionRules']:
                                self._storage_copies[
                                    copy['StoragePolicyCopy']['copyName']]['extendedRetention'] = (
                                        1,
                                        True,
                                        copy['retentionRules']['extendedRetentionRuleOne']['rule'],
                                        copy['retentionRules']['extendedRetentionRuleOne']['endDays'],
                                        copy['retentionRules']['extendedRetentionRuleOne']['graceDays']
                                    ) 
                            if copy['isDefault'] == 1:
                                self._storage_copies[
                                    copy['StoragePolicyCopy']['copyName']]['isDefault'] = True

                            if copy['isSnapCopy'] == 1:
                                self._storage_copies[
                                    copy['StoragePolicyCopy']['copyName']]['isSnapCopy'] = True

                if self._subtype == 33554439:
                    if 'clientGroup' in self._plan_properties['autoCreatedEntities']:
                        self._commcell_object.client_groups.refresh()
                        self._client_group = self._commcell_object.client_groups.get(
                            self._plan_properties['autoCreatedEntities']['clientGroup'][
                                'clientGroupName']
                        )

                    if 'localUserGroup' in self._plan_properties['autoCreatedEntities']:
                        self._user_group = self._plan_properties['autoCreatedEntities'][
                            'localUserGroup']['userGroupName']

                if self._plan_properties['operationWindow']['ruleId'] != 0:
                    self._operation_window = self._plan_properties['operationWindow']
                else:
                    self._operation_window = None

                if self._plan_properties['fullOperationWindow']['ruleId'] != 0:
                    self._full_operation_window = self._plan_properties['fullOperationWindow']
                else:
                    self._full_operation_window = None

                if 'laptop' in self._plan_properties:
                    if 'backupContent' in self._plan_properties['laptop']['content']:
                        self._child_policies['subclientPolicyIds'].clear()
                        for ida in self._plan_properties['laptop']['content']['backupContent']:
                            if ida['subClientPolicy'].get('backupSetEntity'):
                                self._child_policies['subclientPolicyIds'].append(
                                    ida['subClientPolicy']['backupSetEntity']['backupsetId']
                                )

                if ('inheritance' in self._plan_properties and
                        not self._plan_properties['inheritance']['isSealed']):
                    temp_dict = self._plan_properties['inheritance']
                    del temp_dict['isSealed']
                    if 'enforcedEntities' not in temp_dict:
                        temp_dict['enforcedEntities'] = []
                    if 'privateEntities' not in temp_dict:
                        temp_dict['privateEntities'] = []
                    self._override_entities = temp_dict

                if 'parent' in self._plan_properties['summary']:
                    self._parent_plan_name = self._plan_properties['summary']['parent']['planName']

                if 'eePolicy' in self._plan_properties:
                    extraction_policy = self._plan_properties['eePolicy']
                    if 'policyEntity' in extraction_policy:
                        self._dc_plan_props['eePolicyId'] = extraction_policy['policyEntity']['policyId']
                    if 'detail' in extraction_policy:
                        self._dc_plan_props['eePolicy'] = extraction_policy['detail']['eePolicy']

                if 'ciPolicy' in self._plan_properties:
                    ci_policy = self._plan_properties['ciPolicy']
                    if 'policyEntity' in ci_policy:
                        self._dc_plan_props['ciPolicyId'] = ci_policy['policyEntity']['policyId']
                    if 'detail' in ci_policy:
                        self._dc_plan_props['ciPolicy'] = ci_policy['detail']['ciPolicy']

                if 'eDiscoveryInfo' in self._plan_properties:
                    if 'analyticsIndexServer' in self._plan_properties['eDiscoveryInfo']:
                        self._dc_plan_props['analyticsIndexServer'] = self._plan_properties['eDiscoveryInfo']['analyticsIndexServer']

                if 'options' in self._plan_properties:
                    plan_options = self._plan_properties['options']
                    if 'targetApps' in plan_options:
                        self._dc_plan_props['targetApps'] = plan_options['targetApps']

                    if 'supportedWorkloads' in plan_options:
                        self._applicable_solutions = [soln['solutionName'] for soln in plan_options['supportedWorkloads'].get('solutions', [])]

                if 'securityAssociations' in self._plan_properties:
                    self._security_associations = {}
                    for association in self._plan_properties['securityAssociations'].get('associations', []):
                        temp_key = None
                        if 'externalGroupName' in association['userOrGroup'][0]:
                            temp_key = '{0}\\{1}'.format(
                                    association['userOrGroup'][0]['providerDomainName'],
                                    association['userOrGroup'][0]['externalGroupName']
                                )
                        elif 'userGroupName' in association['userOrGroup'][0]:
                            temp_key = association['userOrGroup'][0]['userGroupName']
                        else:
                            temp_key = association['userOrGroup'][0]['userName']
                        if 'role' in association['properties']:
                            if temp_key in self._security_associations:
                                self._security_associations[temp_key].append(
                                    association['properties']['role']['roleName']
                                )
                            else:
                                self._security_associations[temp_key] = [association['properties']['role']['roleName']]
                    if 'tagWithCompany' in self._plan_properties.get('securityAssociations'):
                        self._provider_domain_name = self._plan_properties.get('securityAssociations', {}).\
                            get('tagWithCompany', {}).get('providerDomainName')

                if "storageRules" in self._plan_properties:
                    self._region_id = [x["regions"]["region"][0]["regionId"]
                                       for x in self._plan_properties["storageRules"]["rules"]]

                if 'storageResourcePoolMap' in self._plan_properties:
                    self._resources = self._plan_properties.get('storageResourcePoolMap', {})[0].get('resources')

                self._get_associated_entities()

                return self._plan_properties
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def derive_and_add(self,
                       plan_name,
                       storage_pool_name=None,
                       sla_in_minutes=None,
                       override_entities=None):
        """Derives the base plan based on the the inheritance properties to created a derived plan

            Args:
                plan_name           (str)        --  name of the new plan to add

                storage_pool_name   (str)   --  name of the storage pool to be used for the plan
                    default: None   :   when the name is left to default, it inherits the base plan
                                        storage pool if overriding is optional/not allowed

                sla_in_minutes        (int)        --  Backup SLA in hours
                    default: None   :   when the SLA is left to default, it inherits the base plan
                                        SLA if overriding is optional/not allowed

                override_entities   (dict)  --  Specify the entities with respective overriding.

                    default: None

                        {
                            'privateEntities': [1, 4],

                            'enforcedEntities': [256, 512, 1024]
                        }
                        - where,
                                privateEntities are set when respective entity overriding is must
                                enforcedEntities are set when respective entity overriding is
                                not allowed
                                left blank if overriding is optional

                        - entity IDs,
                                1    - Storage
                                4    - SLA/Schedules
                                256  - Windows content
                                512  - Unix content
                                1024 - Mac content


        Returns:
            object - instance of the Plan class created by this method

        Raises:
            SDKException:
                if plan name is in incorrect format

                if plan already exists

                if neccessary arguments are not passed

                if inheritance rules are not followed

        """
        if not isinstance(plan_name, str):
            raise SDKException('Plan', '101', 'Plan name must be string value')
        else:
            if self._commcell_object.plans.has_plan(plan_name):
                raise SDKException(
                    'Plan', '102', 'Plan "{0}" already exists'.format(
                        plan_name)
                )
        if self._override_entities is not None:
            request_json = self._commcell_object.plans._get_plan_template(
                str(self._subtype), "MSP")

            request_json['plan']['summary']['description'] = "Created from CvPySDK."
            request_json['plan']['summary']['plan']['planName'] = plan_name
            request_json['plan']['summary']['parent'] = {
                'planId': int(self._plan_id)
            }

            is_dedupe = True
            if storage_pool_name is not None:
                storage_pool_obj = self._commcell_object.storage_pools.get(
                    storage_pool_name
                )
                if 'dedupDBDetailsList' \
                        not in storage_pool_obj._storage_pool_properties['storagePoolDetails']:
                    is_dedupe = False
                storage_pool_id = int(storage_pool_obj.storage_pool_id)
                if is_dedupe:
                    request_json['plan']['storage']['copy'][0]['dedupeFlags'][
                        'useGlobalDedupStore'] = 1
                else:
                    del request_json['plan']['storage']['copy'][0]['storagePolicyFlags']
                    del request_json['plan']['storage']['copy'][0]['dedupeFlags'][
                        'enableDeduplication']
                    del request_json['plan']['storage']['copy'][0]['dedupeFlags'][
                        'enableClientSideDedup']
                    del request_json['plan']['storage']['copy'][0]['DDBPartitionInfo']
                    request_json['plan']['storage']['copy'][0]['extendedFlags'] = {
                        'useGlobalStoragePolicy': 1
                    }
            else:
                storage_pool_id = None

            if 1 in self._override_entities['enforcedEntities']:
                if storage_pool_id is None:
                    request_json['plan']['storage'] = {
                        "storagePolicyId": self.storage_policy.storage_policy_id
                    }
                    snap_copy_id = self.storage_policy.storage_policy_id
                else:
                    raise SDKException(
                        'Plan', '102', 'Storage is enforced by base plan, cannot be overridden')
            elif 1 in self._override_entities['privateEntities']:
                if storage_pool_id is not None:
                    request_json['plan']['storage']['copy'][0]['useGlobalPolicy'] = {
                        "storagePolicyId": storage_pool_id
                    }
                    snap_copy_id = storage_pool_id
                else:
                    raise SDKException('Plan', '102', 'Storage must be input')
            else:
                if storage_pool_id is not None:
                    request_json['plan']['storage']['copy'][0]['useGlobalPolicy'] = {
                        "storagePolicyId": storage_pool_id
                    }
                    snap_copy_id = storage_pool_id
                else:
                    request_json['plan']['storage'] = {
                        "storagePolicyId": self.storage_policy.storage_policy_id
                    }
                    snap_copy_id = self.storage_policy.storage_policy_id

            if 4 in self._override_entities['enforcedEntities']:
                if sla_in_minutes is None:
                    request_json['plan']['summary']['slaInMinutes'] = self._sla_in_minutes
                else:
                    raise SDKException(
                        'Plan', '102', 'SLA is enforced by base plan, cannot be overridden')
            elif 4 in self._override_entities['privateEntities']:
                if sla_in_minutes is not None:
                    request_json['plan']['summary']['slaInMinutes'] = sla_in_minutes
                else:
                    raise SDKException('Plan', '102', 'SLA must be input')
            else:
                if sla_in_minutes is not None:
                    request_json['plan']['summary']['slaInMinutes'] = sla_in_minutes
                else:
                    request_json['plan']['summary']['slaInMinutes'] = self._sla_in_minutes

            if isinstance(override_entities, dict):
                request_json['plan']['summary']['restrictions'] = 0
                request_json['plan']['inheritance'] = {
                    'isSealed': False
                }
                for entity in self._override_entities['enforcedEntities']:
                    from functools import reduce
                    if override_entities and entity in reduce(
                            lambda i, j: i + j, override_entities.values()):
                        raise SDKException(
                            'Plan', '102', 'Override not allowed')
                if 'enforcedEntities' in override_entities:
                    request_json['plan']['inheritance']['enforcedEntities'] = (
                        override_entities['enforcedEntities']
                    )
                if 'privateEntities' in override_entities:
                    request_json['plan']['inheritance']['privateEntities'] = (
                        override_entities['privateEntities']
                    )
            else:
                request_json['plan']['summary']['restrictions'] = 1
                request_json['plan']['inheritance'] = {
                    'isSealed': True
                }

            if sla_in_minutes is not None:
                request_json['plan']['definesSchedule'] = {
                    'definesEntity': True
                }
            else:
                request_json['plan']['definesSchedule'] = {
                    'definesEntity': False
                }

            if isinstance(self._override_entities, dict):
                if (4 not in
                        self._override_entities['enforcedEntities'] +
                        self._override_entities['privateEntities']):
                    request_json['plan']['definesSchedule']['overrideEntity'] = 0
                elif 4 in self._override_entities['enforcedEntities']:
                    request_json['plan']['definesSchedule']['overrideEntity'] = 2
                elif 4 in self._override_entities['privateEntities']:
                    request_json['plan']['definesSchedule']['overrideEntity'] = 1

            if storage_pool_id is not None:
                request_json['plan']['definesStorage'] = {
                    'definesEntity': True
                }
            else:
                request_json['plan']['definesStorage'] = {
                    'definesEntity': False
                }

            if isinstance(self._override_entities, dict):
                if (1 not in
                        self._override_entities['enforcedEntities'] +
                        self._override_entities['privateEntities']):
                    request_json['plan']['definesStorage']['overrideEntity'] = 0
                elif 1 in self._override_entities['enforcedEntities']:
                    request_json['plan']['definesStorage']['overrideEntity'] = 2
                elif 1 in self._override_entities['privateEntities']:
                    request_json['plan']['definesStorage']['overrideEntity'] = 1

            if self._subtype != 33554437:
                temp_defines_key = {
                    'definesEntity': False
                }
                if isinstance(self._override_entities, dict):
                    if (not all(entity in
                                self._override_entities['enforcedEntities'] +
                                self._override_entities['privateEntities']
                                for entity in [256, 512, 1024])):
                        temp_defines_key['overrideEntity'] = 0
                    elif all(entity in self._override_entities['enforcedEntities']
                             for entity in [256, 512, 1024]):
                        temp_defines_key['overrideEntity'] = 2
                    elif all(entity in self._override_entities['privateEntities']
                             for entity in [256, 512, 1024]):
                        temp_defines_key['overrideEntity'] = 1
                request_json['plan']['laptop']['content']['definesSubclientLin'] = temp_defines_key
                request_json['plan']['laptop']['content']['definesSubclientMac'] = temp_defines_key
                request_json['plan']['laptop']['content']['definesSubclientWin'] = temp_defines_key

            if self._subtype == 33554437 and 'snap' in self.addons and 'copy' \
                    in request_json['plan']['storage']:
                request_json['plan']['storage']['copy'][1]['useGlobalPolicy'] = {
                    'storagePolicyId': snap_copy_id
                }
                request_json['plan']['storage']['copy'][1]['extendedFlags'] = {
                    'useGlobalStoragePolicy': 1
                }

            add_plan_service = self._commcell_object.plans._PLANS
            headers = self._commcell_object._headers.copy()
            headers['LookupNames'] = 'False'

            flag, response = self._cvpysdk_object.make_request(
                'POST', add_plan_service, request_json, headers=headers
            )

            if flag:
                if response.json():
                    response_value = response.json()
                    error_message = None
                    error_code = None

                    if 'errors' in response_value:
                        error_code = response_value['errors'][0]['status']['errorCode']
                        error_message = response_value['errors'][0]['status']['errorMessage']

                    # error_codes 0 - OK, 1 - plan without storage, 84 - restricted plan
                    if error_code not in [0, 1, 84]:
                        o_str = 'Failed to create new Plan\nError: "{0}"'.format(
                            error_message
                        )
                        raise SDKException('Plan', '102', o_str)

                    if 'plan' in response_value:
                        plan_name = response_value['plan']['summary']['plan']['planName']

                        # initialize the plans again
                        # so that the plans object has all the plans
                        self._commcell_object.plans.refresh()

                        return self._commcell_object.plans.get(plan_name)
                    else:
                        o_str = ('Failed to create new plan due to error code: "{0}"\n'
                                 'Please check the documentation for '
                                 'more details on the error').format(error_code)

                        raise SDKException('Plan', '102', o_str)
                else:
                    raise SDKException('Response', 102)
            else:
                response_string = self._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException('Plan', '102', 'Inheritance disabled for plan')

    def modify_schedule(self, schedule_json, is_full_schedule=False):
        """Modifies the incremental RPO schedule pattern of the plan with the given schedule json

            Args:
            schedule_json (dict) -- {
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
            is_full_schedule (bool) --  Pass True if he schedule to be modified is the full backup schedule
        """
        if is_full_schedule:
            try:
                schedule_id = list(filter(
                    lambda st: st['subTask']['flags'] == 4194304, self.schedule_policies['data']._subtasks
                ))[0]['subTask']['subTaskId']
            except IndexError:
                raise IndexError('Full backup schedule not enabled')
        else:
            schedule_id = list(filter(
                lambda st: st['subTask']['flags'] == 65536, self.schedule_policies['data']._subtasks
            ))[0]['subTask']['subTaskId']
        self.schedule_policies['data'].modify_schedule(
            schedule_json,
            schedule_id=schedule_id
        )
        self.refresh()

    def __handle_response(self, flag: bool, response: object, custom_error_message: str=None):
        """Handles the response received from the server

        Args:
            flag (bool)                 --  boolean specifying whether the request was successful or not

            response (Response Object)  --  response received from the server

            custom_error_message (str)  --  custom error message to be used in case of failure

        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        if flag:
            if response.json():
                response_value = response.json()
                error_info = response_value.get('error', response_value)
                error_message = error_info.get('errorMessage', '')
                error_code = error_info.get('errorCode', 0)

                if error_code != 0:
                    if custom_error_message:
                        error_message = custom_error_message + '\nError: "{0}"'.format(error_message)
                    raise SDKException('Plan', '102', error_message)
                
                self.refresh()

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_plan_properties(self) -> Dict:
        """
        Method to get the properties of this plan fetched from v4 API.
        
        Returns:
            Dict: A dictionary containing the properties of the plan fetched from the v4 API.
        """
        return self._v4_plan_properties

    def get_storage_copy_details(self, copy_name: str, region_name: str = None) -> Dict:
        """Method to get the storage copy details of the given copy name and region name

        Args:
            copy_name (str): Name of the copy
            region_name (str, optional): Name of the region

        Returns:
            dict: Dictionary consisting of the properties of the given copy name
        """
        backup_destinations = self._v4_plan_properties.get('backupDestinations', [])

        # Filter by region name
        if region_name:
            backup_destinations = list(filter(lambda item: item.get('region', {}).get("name") == region_name, backup_destinations))

        # Filter by copy name
        if copy_name:
            backup_destinations = list(filter(lambda item: item.get('planBackupDestination', {}).get("name") == copy_name, backup_destinations))

        if not backup_destinations:
            raise SDKException('Plan', '102', f'No copy found with name: [{copy_name}] and region: [{region_name}]')

        if len(backup_destinations) > 1:
            raise SDKException('Plan', '102', f'Multiple copies found with name: [{copy_name}] and region: [{region_name}]')
        
        copy_details = next(iter(backup_destinations), None)
        
        return copy.deepcopy(copy_details) # return a deep copy to avoid modifying the original properties

    def get_storage_copy_id(self, copy_name: str, region_name: str = None) -> int:
        """Gets the storage copy id of the given copy name

        Args:
            copy_name (str): Name of the copy
            region_name (str, optional): Name of the region

        Returns:
            int: Storage copy id of the given copy name
        """
        copy_details = self.get_storage_copy_details(copy_name, region_name)
        return copy_details.get('planBackupDestination', {}).get('id', 0) if copy_details else 0

    def add_copy(self, copy_name: str, storage_pool: str, retention: int=30, extended_retention: dict=None, region: str=None) -> None:
        """
            Method to add an aux copy to the plan

            Args:
                copy_name   (str)   -   name of the copy that is being added
                storage_pool (str)  -   name of the storage pool that is to be used for the copy
                retention   (int)   -   retention period in days for the copy
                extended_retention (dict)  -   extended retention rules of a copy
                region      (str)   -   region name to which copy needs to be added

            Returns:
                None

            Raises:
                SDKException:
                -   if failed to add new copy to the plan
        """
        copy_details = {
            "backupDestinationName": copy_name,
            "storage_name": storage_pool,
            "retentionPeriodDays": retention
        }

        if extended_retention:
            copy_details['useExtendedRetentionRules'] = True
            copy_details["extendedRetentionRules"] = extended_retention

        request_json = {
            'destinations': [self.plan_v4_helper.get_copy_payload(copy_details, is_aux_copy=True)]
        }
        # during add copy, region should be specified as the separate blob
        if region:
            request_json['region'] = {"id": int(self._commcell_object.regions.get(region).region_id)}

        flag, response = self._cvpysdk_object.make_request('POST', self._SERVER_PLAN_BACKUP_DESTINATION, request_json)

        self.__handle_response(flag, response, custom_error_message=f'Failed to add new copy to the plan : [{self.plan_name}]')

    def edit_copy(self, copy_name: str, new_retention_days: int = None, new_recovery_points: int = None, new_extended_retention: dict = None, current_region_name: str = None) -> None:
        """
        Method to edit a copy settings

        Args:
            copy_name (str): name of the copy that is being edited
            new_retention_days (int): new retention period in days for the copy
            new_recovery_points (int): new recovery points for the snap copy
            new_extended_retention (dict): new extended retention rules of a copy
            current_region_name (str): name of the region from which the copy needs to be edited

            Example:
                new_extended_retention =  {
                "firstExtendedRetentionRule": {
                    "isInfiniteRetention": False,
                    "type": "WEEKLY_FULLS",
                    "retentionPeriodDays": 90
                }
        }
        """
        copy_details = self.get_storage_copy_details(copy_name, current_region_name)
        copy_id = self.get_storage_copy_id(copy_name, current_region_name)
        is_snap_copy = copy_details.get('isSnapCopy', False)

        # input validation
        if new_retention_days is not None and new_recovery_points is not None:
            raise SDKException('Plan', '102', 'Both retention days and recovery points cannot be set at the same time')

        if new_recovery_points and not is_snap_copy:
            raise SDKException('Plan', '102', 'Recovery points can be set only for snap copy')

        # copy the old details to the required payload first
        required_props = ['retentionPeriodDays', 'retentionRuleType', 'useExtendedRetentionRules', 'extendedRetentionRules']
        new_retention_rules = {key: copy_details[key] for key in required_props if key in copy_details}

        # update the payload based on the input
        if new_retention_days is not None:
            new_retention_rules.update({'retentionPeriodDays': new_retention_days, 'retentionRuleType': "RETENTION_PERIOD"})

        if new_recovery_points is not None:
            new_retention_rules.update({'retentionPeriodDays': new_recovery_points, 'retentionRuleType': "SNAP_RECOVERY_POINTS"})

        if new_extended_retention:
            new_retention_rules.update({'useExtendedRetentionRules': True, 'extendedRetentionRules': new_extended_retention})

        # special property that needs to be sent during edit
        new_retention_rules['fullBackupTypesToBeRetained'] = 'FIRST'

        request_json = {'retentionRules': new_retention_rules}

        flag, response = self._cvpysdk_object.make_request('PUT', self._services['V5_SERVER_PLAN_COPY'] % (self.plan_id, copy_id), request_json)

        self.__handle_response(flag, response, custom_error_message=f'Failed to edit copy settings for the plan : [{self.plan_name}] Copy: [{copy_name}] Region: [{current_region_name}]')

    def delete_copy(self, copy_name: str, region_name: str=None) -> None:
        """
        Method to remove a copy from the plan

        Args:
            copy_name (str)   -   name of the copy to be removed
            region_name (str) -   name of the region from which the copy needs to be removed

        Returns:
            None

        Raises:
            SDKException:
                -   if failed to remove the copy from the plan
        """
        copy_id = self.get_storage_copy_id(copy_name, region_name)

        flag, response = self._cvpysdk_object.make_request('DELETE', self._services['V4_SERVER_PLAN_COPY'] % (self.plan_id, copy_id))

        self.__handle_response(flag, response, custom_error_message=f'Failed to remove copy from the plan: [{self.plan_name}]')

    def add_region(self, region_name: str) -> None:
        """
        Method to add a region to the plan

        Args:
            region_name (str)   -   name of the region that is being added

        Returns:
            None

        Raises:
            SDKException:
                -   if failed to add new region to the plan
        """
        region_id = self._commcell_object.regions.get(region_name).region_id

        request_json = {
            "regionToConfigure": {
                "id": int(region_id)
            }
        }

        flag, response = self._cvpysdk_object.make_request('PUT', self._V4_PLAN, request_json)

        self.__handle_response(flag, response, custom_error_message=f'Failed to add new region to the plan : [{self.plan_name}]')

    def remove_region(self, region_name: str) -> None:
        """
        Method to remove a region from the plan

        Args:
            region_name (str)   -   name of the region that is being removed

        Returns:
            None

        Raises:
            SDKException:
                -   if failed to remove the region from the plan
        """
        region_id = self._commcell_object.regions.get(region_name).region_id

        flag, response = self._cvpysdk_object.make_request('DELETE', self._services['SERVER_PLAN_REGIONS'] % (self.plan_id, region_id))

        self.__handle_response(flag, response, custom_error_message=f'Failed to remove region from the plan: [{self.plan_name}]')

    def get_schedule_properties(self, schedule_filter: dict) -> dict:
        """
        Method to get the schedule properties of the plan

        Args:
            schedule_filter (dict) - dictionary containing the filter criteria for the schedule

            Example for schedule filter:

            # select the full backup schedule
                {"backupType": "FULL"}

            # select the schedule where backup type is incremental and schedule is applicable to all agents
            {"backupType": "INCREMENTAL", "forDatabasesOnly": False}

        Returns:
            dict - schedule properties of the plan

        Raises:
            SDKException:
                - if no schedule is found with the provided filter
                - if multiple schedules are found with the provided filter
        """
        schedules = self._v4_plan_properties['rpo']['backupFrequency']['schedules']
        filtered_schedules = [schedule for schedule in schedules if all(schedule.get(key) == value for key, value in schedule_filter.items())]

        if not filtered_schedules:
            raise SDKException('Plan', '102', f'No schedule found with the provided filter: {schedule_filter} for plan: [{self.plan_name}]')
        
        if len(filtered_schedules) > 1:
            raise SDKException('Plan', '102', f'Multiple schedules found with the provided filter: {schedule_filter} for plan: [{self.plan_name}]')

        return copy.deepcopy(filtered_schedules[0]) # return a deep copy to avoid modifying the original schedule properties

    def add_schedule(self, schedule_options: dict) -> None:
        """
        Method to add a new schedule to the plan

        Args:
            schedule_options (dict) - schedule options to be added (backupType is mandatory)

            Note: To prepare advanced schedule options, refer to the API documentation or Command Center equivalent API

            Example:

            # create schedule based on backup type and rest use default values
            {"backupType": "INCREMENTAL"}
            {"backupType": "TRANSACTIONLOG"}

            # create schedule with advanced properties
            {
                "backupType": "FULL", 
                "schedulePattern": {
                    "scheduleFrequencyType": "DAILY",
                    "startTime": 75600,
                    "frequency": 1
                    }
            }

            # specify agents for schedules
            {"backupType": "INCREMENTAL", "forDatabasesOnly": False}
            {"backupType": "FULL", "forDatabasesOnly": True}

            # advance properties for schedules
            {"backupType": "TRANSACTIONLOG", "scheduleOption": {"useDiskCacheForLogBackups": True}}

        Returns:
            None

        Raises:
            SDKException:
                - if failed to add the schedule to the plan
        """
        schedule_payload = self.plan_v4_helper.get_schedule_payload(schedule_options)
        
        payload = {
            "backupFrequency": {
                "schedules": [schedule_payload]
            }
        }
        flag, response = self._cvpysdk_object.make_request('PUT', self._PLAN_RPO, payload)

        self.__handle_response(flag, response, custom_error_message=f'Failed to add new schedule to the plan: [{self.plan_name}]')    

    def edit_schedule(self, schedule_options: dict, schedule_filter: dict) -> None:
        """
        Method to edit the schedule options of the plan

        Args:
            schedule_options (dict) - schedule options to be edited
            schedule_filter (dict)  - schedule for which the options are to be edited

            Refer to the add_schedule method for the format of the schedule options

            Refer to the get_schedule_properties method for the format of the schedule filter

        Returns:
            None

        Raises:
            SDKException:
                - if failed to edit the schedule options of the plan
        """
        schedule_payload = self.get_schedule_properties(schedule_filter)

        schedule_payload['scheduleOperation'] = 'MODIFY'
        # update the payload with the new provided options
        schedule_payload = self.plan_v4_helper.update_payload(schedule_payload, schedule_options)

        payload = {
            "backupFrequency": {
                "schedules": [schedule_payload]
            }
        }

        flag, response = self._cvpysdk_object.make_request('PUT', self._PLAN_RPO, payload)

        self.__handle_response(flag, response, custom_error_message=f'Failed to edit schedule options for the plan: [{self.plan_name}]')

    def delete_schedule(self, schedule_filter: dict) -> None:
        """
        Method to delete the schedule from the plan

        Args:
            schedule_filter (dict)  - schedule to be deleted

            Refer to the get_schedule_properties method for the format of the schedule filter

        Returns:
            None

        Raises:
            SDKException:
                - if failed to edit the schedule options of the plan
        """
        schedule_payload = self.get_schedule_properties(schedule_filter)
        schedule_payload['scheduleOperation'] = 'DELETE'

        payload = {
            "backupFrequency": {
                "schedules": [schedule_payload]
            }
        }

        flag, response = self._cvpysdk_object.make_request('PUT', self._PLAN_RPO, payload)

        self.__handle_response(flag, response, custom_error_message=f'Failed to delete schedule from the plan: [{self.plan_name}]')

    def edit_snapshot_options(self, enable_backup_copy:bool=True, backup_copy_rpo: int=None) -> None:
        """
        Method to edit the snapshot options of the plan

        Args:
            enable_backup_copy (bool)   -   enable backup copy for the plan

            backup_copy_rpo (int)       -   backup copy RPO for the plan

        Returns:
            None

        Raises:
            SDKException:
                -   if failed to edit the snapshot options of the plan
        """
        request_json = {
            "snapshotOptions": {
                "enableBackupCopy": enable_backup_copy
            }
        }

        if backup_copy_rpo:
            request_json["snapshotOptions"]["backupCopyRPOMins"] = backup_copy_rpo

        flag, response = self._cvpysdk_object.make_request('PUT', self._V4_PLAN, request_json)

        self.__handle_response(flag, response, custom_error_message=f'Failed to edit snapshot settings for the plan : [{self.plan_name}]')

    def add_storage_copy(self, copy_name, storage_pool, retention=30, extended_retention=None):
        """Add a storage copy as backup destination to this plan
            Args:
                copy_name   (str)   -   name of the copy that is being added

                storage_pool (str)  -   name of the storage pool for the copy to be added

                retention   (int)   -   retention period in days for the copy

                extended_retention (tuple)  -   extended retention rules of a copy
                                                Example: [1, True, "EXTENDED_ALLFULL", 0, 0]
            Returns:
                dict    -   dictionary of all copies of this plan
        """
        if isinstance(copy_name, str) and isinstance(storage_pool, str):
            if not self.storage_policy.has_copy(copy_name):
                self.storage_policy.create_secondary_copy(
                    copy_name,
                    global_policy=storage_pool
                )
                self.storage_policy.get_copy(copy_name).copy_retention = (retention, 0, 0)
                if extended_retention:
                    self.storage_policy.get_copy(
                        copy_name).extended_retention_rules = extended_retention
                self.refresh()
                return self.storage_copies
            else:
                err_msg = f'Storage Policy copy "{copy_name}" already exists.'
                raise SDKException('Storage', '102', err_msg)
        else:
            raise SDKException(
                'Plan', '102', 'Copy name and storage pool name must be a string.'
            )

    def disable_full_schedule(self):
        """Disable the full backup schedule of the plan"""
        try:
            self.schedule_policies['data'].delete_schedule(schedule_id=list(filter(
                lambda st: st['subTask']['flags'] == 4194304, self.schedule_policies['data']._subtasks
            ))[0]['subTask']['subTaskId'])
        except IndexError:
            raise IndexError('Full backup schedule not enabled')

    def edit_association(self, entities, new_plan=None):
        """Reassociates or dissociates the entities from this plan
            Args:
                entities    (list)  --  list containing entity objects whose plan association must be edited
                                        Eg: [
                                            {
                                                "clientName": "client",
                                                "subclientName": "subclient",
                                                "backupsetName": "backupset",
                                                "appName": "app"
                                            }
                                        ]

                new_plan    (str)   --  new plan to which the associated entities must be reassociated with

            Raises:
                SDKException
                    if plan not found
        """
        req_json = {
            'plan': {
                'planName': self.plan_name
            },
            'entities': entities
        }
        if new_plan is not None:
            if self._commcell_object.plans.has_plan(new_plan):
                req_json.update({
                    'planOperationType': 'OVERWRITE',
                    'newPlan': {
                        'planName': new_plan
                    }
                })
            else:
                SDKException('Plan', '102', 'No plan exists with name: {0}'.format(
                    new_plan)
                )
        else:
            req_json.update({
                'planOperationType': 'DELETE'
            })
        req_url = self._services['ASSOCIATED_ENTITIES'] % (self._plan_id)
        flag, response = self._cvpysdk_object.make_request(
            'PUT', req_url, req_json
        )

        if flag:
            if 'response' in response.json():
                error_code = str(response.json()["response"][0]["errorCode"])

                if error_code == "0":
                    self.refresh()
                    return
            else:
                error_message = str(response.json()["errorMessage"])
                o_str = 'Failed to edit plan associated entities\nError: "{0}"'
                raise SDKException('Plan', '102', o_str.format(error_message))
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _update_plan_props(self, props):
        """Updates the properties of the plan

            Args:
                props   (dict)  --  dictionary containing the properties to be updated
                                    {
                                        'planName': 'NewName'
                                    }

            Raises:
                SDKException
                    if there is failure in updating the plan
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._PLAN, props
        )
        if flag:
            if response.json():
                error_code = str(response.json()["errors"][0]["status"]["errorCode"])
                error_message = str(response.json()["errors"][0]["status"]["errorMessage"])

                if error_code == "0":
                    self.refresh()
                    return (True, error_code)
                else:
                    return (False, error_code, error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_associated_entities(self):
        """Gets all the backup entities associated with the plan.

            Returns:
                dict - dictionary containing list of entities that are
                       associated with the plan.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        request_url = self._services['ASSOCIATED_ENTITIES'] % (self._plan_id)
        flag, response = self._cvpysdk_object.make_request(
            'GET', request_url
        )

        if flag:
            if response.json() and 'entities' in response.json():
                self._associated_entities = response.json()['entities']
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def plan_id(self):
        """Treats the plan id as a read-only attribute."""
        return self._plan_id

    @property
    def plan_name(self):
        """Treats the plan name as a read-only attribute."""
        return self._plan_name

    @plan_name.setter
    def plan_name(self, value: str):
        """modifies the plan name"""
        # use v4 API for server plans
        if self.subtype == 33554437:
            req_json = {
                "newName": value
            }

            flag, response = self._cvpysdk_object.make_request('PUT', self._V4_PLAN, req_json)

            self.__handle_response(flag, response, custom_error_message=f'Failed to update the plan name: [{self._plan_name}]')
            return

        if isinstance(value, str):
            req_json = {
                'summary': {
                    'plan': {
                        'planName': value
                    }
                }
            }
            resp = self._update_plan_props(req_json)

            if resp[0]:
                return
            else:
                o_str = 'Failed to update the plan name\nError: "{0}"'
                raise SDKException('Plan', '102', o_str.format(resp[2]))
        else:
            raise SDKException(
                'Plan', '102', 'Plan name must be a string value'
            )

    @property
    def sla_in_minutes(self):
        """Treats the plan SLA/RPO as a read-only attribute."""
        return self._sla_in_minutes

    @sla_in_minutes.setter
    def sla_in_minutes(self, value):
        """Modifies the plan SLA/RPO"""
        if isinstance(value, int):
            req_json = {
                'summary': {
                    'slaInMinutes': value
                }
            }
            resp = self._update_plan_props(req_json)

            if resp[0]:
                return
            else:
                o_str = 'Failed to update the plan SLA\nError: "{0}"'
                raise SDKException('Plan', '102', o_str.format(resp[2]))
        else:
            raise SDKException(
                'Plan', '102', 'Plan SLA must be an int value'
            )

    @property
    def operation_window(self):
        """Treats the plan incremental operation window as a read-only attribute"""
        return self._operation_window

    @operation_window.setter
    def operation_window(self, value):
        """Modifies the incremental operation window of the plan

            Args:
                value   (list)    --  list of time slots for setting the backup window

                value   (None)      --  set value to None to clear the operation window

            Raises:
                SDKException:
                    if the input is incorrect

                    if the operation window configuration fails
        """
        if isinstance(value, list):
            req_json = {
                "operationWindow": {
                    "operations": [
                        2,
                        4
                    ],
                    "dayTime": value
                }
            }
            resp = self._update_plan_props(req_json)
            if resp[0]:
                self.refresh()
                return
            else:
                o_str = 'Failed to update the operation window\nError: "{0}"'
                raise SDKException('Plan', '102', o_str.format(resp[2]))
        elif value is None:
            self._commcell_object.operation_window.delete_operation_window(
                rule_id=self._operation_window['ruleId']
            )
            self.refresh()
            return
        else:
            raise SDKException(
                'Plan', '102', 'Plan operation window must be a list value or None'
            )

    @property
    def full_operation_window(self):
        """Treats the plan full backup operation window as a read-only attribute"""
        return self._full_operation_window

    @full_operation_window.setter
    def full_operation_window(self, value):
        """Modifies the full backup operation window of the plan

            Args:
                value   (list)    --  list of time slots for setting the backup window

                value   (None)      --  set value to None to clear the operation window

            Raises:
                SDKException:
                    if the input is incorrect

                    if the operation window configuration fails
        """
        if isinstance(value, list):
            req_json = {
                "operationWindow": {
                    "operations": [
                        1,
                    ],
                    "dayTime": value
                }
            }
            resp = self._update_plan_props(req_json)
            if resp[0]:
                self.refresh()
                return
            else:
                o_str = 'Failed to update the full operation window\nError: "{0}"'
                raise SDKException('Plan', '102', o_str.format(resp[2]))
        elif value is None:
            self._commcell_object.operation_window.delete_operation_window(
                rule_id=self._full_operation_window['ruleId']
            )
            self.refresh()
            return
        else:
            raise SDKException(
                'Plan', '102', 'Plan full operation window must be a list value or None'
            )

    @property
    def plan_type(self):
        """Treats the plan type as a read-only attribute."""
        return self._plan_type

    @property
    def subtype(self):
        """Treats the plan subtype as a read-only attribute."""
        return self._subtype

    @property
    def override_entities(self):
        """Treats the plan override_entities as a read-only attribute."""
        return self._override_entities

    @override_entities.setter
    def override_entities(self, value):
        """Sets the override restrictions for the plan"""
        req_json = {
            "inheritance": {
                "isSealed": False,
                "enforcedEntitiesOperationType": 1,
                "privateEntitiesOperationType": 1
            }
        }
        if isinstance(value, dict):
            req_json['inheritance'].update(value)
            resp = self._update_plan_props(req_json)
            if resp[0]:
                return
            else:
                o_str = 'Failed to update the plan override restrictions\nError: "{0}"'
                raise SDKException('Plan', '102', o_str.format(resp[2]))
        else:
            raise SDKException(
                'Plan', '102', 'Override restrictions must be defined in a dict'
            )

    def __set_storage_policy(self):
        """Method to set the storage policy of the plan"""
        self._commcell_object.storage_policies.refresh()
        storage_policy_name = self._plan_properties.get('storage', {}).get('storagePolicy', {}).get('storagePolicyName')
        if storage_policy_name and self._commcell_object.storage_policies.has_policy(storage_policy_name):
            self._child_policies['storagePolicy'] = self._commcell_object.storage_policies.get(storage_policy_name)
        else:
            raise SDKException('Plan', '102', f'Failed to fetch storage policy: {storage_policy_name}')

    @property
    def storage_policy(self):
        """Treats the plan storage policy as a read-only attribute"""
        if not self._child_policies.get('storagePolicy'):
            self.__set_storage_policy()

        return self._child_policies.get('storagePolicy')

    @property
    def storage_copies(self):
        """Treats the plan storage policy as a read-only attribute"""
        return self._storage_copies

    def __set_schedule_policies(self):
        """Sets the schedule policies for the plan"""
        self._commcell_object.schedule_policies.refresh()
        data_schedule_policy_exists = self._plan_properties.get('schedule', {}).get('task', {}).get('taskName')
        log_schedule_policy_exists = self._plan_properties.get('database', {}).get('scheduleLog', {}).get('task', {}).get('taskName')
        snap_schedule_policy_exists = self._plan_properties.get('snapInfo', {}).get('snapTask', {}).get('task', {}).get('taskName')

        if data_schedule_policy_exists:
            self._child_policies['schedulePolicy']['data'] = self.data_schedule_policy

        if log_schedule_policy_exists:
            self._child_policies['schedulePolicy']['log'] = self.log_schedule_policy

        if snap_schedule_policy_exists:
            self._child_policies['schedulePolicy']['snap'] = self.snap_schedule_policy

    @property
    def schedule_policies(self):
        """Treats the plan schedule policies as read-only attribute"""
        if not self._child_policies.get('schedulePolicy'):
            self.__set_schedule_policies()

        return self._child_policies.get('schedulePolicy')

    def __get_schedule_policy(self, policy_type: str) -> object:
        """
        Returns the schedule policy object of the given policy type

        Args:
            policy_type (str)  --  type of schedule policy to be fetched
                            Eg: 'data', 'log', 'snap'

        Returns:
            object  --  schedule policy object
        """
        policy_name = ''
        policy_type = policy_type.lower()

        if policy_type == 'data':
            policy_name = self._plan_properties.get('schedule', {}).get('task', {}).get('taskName', '')
        elif policy_type == 'log':
            policy_name = self._plan_properties.get('database', {}).get('scheduleLog', {}).get('task', {}).get('taskName', '')
        elif policy_type == 'snap':
            policy_name = self._plan_properties.get('snapInfo', {}).get('snapTask', {}).get('task', {}).get('taskName', '')
        else:
            raise SDKException('Plan', '102', 'Invalid schedule policy type')

        schedule_policies = self._commcell_object.schedule_policies

        if not schedule_policies.has_policy(policy_name):
            raise SDKException('Plan', '102', 'Failed to fetch schedule policies')

        return schedule_policies.get(policy_name)

    @property
    def data_schedule_policy(self) -> object:
        """
            Treats the plan data scheduler policy as read-only attribute

            Returns:
                object  -   data schedule policy object
        """
        if not self._data_schedule_policy:
            self._data_schedule_policy = self.__get_schedule_policy('data')
        return self._data_schedule_policy

    @property
    def log_schedule_policy(self) -> object:
        """
            Treats the plan log schedule policy as read-only attribute

            Returns:
                object  -   log schedule policy object
        """
        if not self._log_schedule_policy:
            self._log_schedule_policy = self.__get_schedule_policy('log')
        return self._log_schedule_policy

    @property
    def snap_schedule_policy(self) -> object:
        """
            Treats the plan snap schedule policy as read-only attribute

            Returns:
                object  -   snap schedule policy object
        """
        if not self._snap_schedule_policy:
            self._snap_schedule_policy = self.__get_schedule_policy('snap')
        return self._snap_schedule_policy

    @property
    def addons(self):
        """Treats the plan addons as read-only attribute"""
        for addon in self._plan_properties.get('summary', {}).get('addons', []):
            self._addons.append(
                addon
            )
        return self._addons

    def __set_subclient_policy_ids(self):
        """Sets the subclient policy ids for the plan"""
        backup_content = self._plan_properties.get('laptop', {}).get('content', {}).get('backupContent', [])

        self._child_policies['subclientPolicyIds'] = [
            ida['subClientPolicy']['backupSetEntity']['backupsetId']
            for ida in backup_content
            if ida.get('subClientPolicy', {}).get('backupSetEntity', {}).get('backupsetId')
        ]

    @property
    def subclient_policy(self):
        """Treats the plan subclient policy as a read-only attribute"""
        if not self._child_policies.get('subclientPolicyIds'):
            self.__set_subclient_policy_ids()

        return self._child_policies.get('subclientPolicyIds')

    @property
    def associated_entities(self):
        """getter for the backup entities associated with the plan"""
        return self._associated_entities

    @property
    def parent_plan(self):
        """getter for the parent plan of a derived plan"""
        return self._commcell_object.plans.get(self._parent_plan_name)

    @property
    def security_associations(self):
        """getter for the plan's security associations
            Eg:
                {
                    'sample_user_group_name': 'role_name'
                }
        """
        return self._security_associations

    def update_security_associations(self, associations_list, is_user = True, request_type = None, external_group = False):
        """
        Adds the security association on the plan object

        Args:
            associations_list   (list)  --  list of users to be associated
                Example:
                    associations_list = [
                        {
                            'user_name': user1,
                            'role_name': role1
                        },
                        {
                            'user_name': user2,
                            'role_name': role2
                        }
                    ]
 
            is_user (bool)           --    True or False. set is_user = False, If associations_list made up of user groups
            request_type (str)      --    eg : 'OVERWRITE' or 'UPDATE' or 'DELETE', Default will be OVERWRITE operation
            external_group (bool)    --    True or False, set external_group = True. If Security associations is being done on External User Groups

        Raises:
            SDKException:
                if association is not of List type
        """
        if not isinstance(associations_list, list):
            raise SDKException('Plan', '102')

        SecurityAssociation(self._commcell_object, self)._add_security_association(associations_list, 
                                        is_user, request_type, external_group)

    @property
    def content_indexing_props(self):
        """returns the DC plan related CI properties from Plan"""
        return self._dc_plan_props

    @property
    def content_indexing(self):
        """Returns the Content Indexing status of O365 plan"""
        try:
            ci_status = (self.properties.get("office365Info",{})
                         .get("o365Exchange",{})
                         .get("mbArchiving", {})
                         .get("detail", {})
                         .get("emailPolicy", {})
                         .get("archivePolicy", {})
                         .get("contentIndexProps", {})
                         .get("enableContentIndex", {}))
        except:
            ci_status= None
        return ci_status

    @content_indexing.setter
    def content_indexing(self, value: bool):
        """Sets content indexing value for O365 plan"""
        self._enable_content_indexing_o365_plan(value)


    @property
    def properties(self):
        """Returns the configured properties for the Plan"""
        return self._plan_properties

    @property
    def region_id(self):
        """Returns the Backup destination region id"""
        return self._region_id

    @property
    def company(self) -> str:
        """
        Returns the company of the plan

        return:
            str --  company's domain name
        """
        return self._provider_domain_name

    @property
    def resources(self) -> list:
        """
        Returns the resources stored in storage resource pool

        return:
            list --  plan's resources
        """
        return self._resources

    def refresh(self):
        """Refresh the properties of the Plan."""
        self._properties = self._get_plan_properties()

        # fetch v4 properties for server plans
        if self.subtype == 33554437:
            self._v4_plan_properties = self._get_v4_plan_properties()

        # lazy loading of properties
        self._data_schedule_policy = None
        self._log_schedule_policy = None
        self._snap_schedule_policy = None
        self._child_policies = {
            'storagePolicy': None,
            'schedulePolicy': {},
            'subclientPolicyIds': []
        } # reset to constructor state

    def associate_user(self, userlist, send_invite=True):
        """associates the users to the plan.
            # TODO: Need to handle user groups.

           Arguments:
                userlist(list) - list of users to be associated to the plans.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        users_list = []

        for user in userlist:
            if self._commcell_object.users.has_user(user):
                temp = self._commcell_object.users.get(user)

                temp_dict = {
                    'sendInvite': send_invite,
                    'user': {
                        'userName': temp.user_name,
                        'userId': int(temp.user_id)
                    }
                }

                users_list.append(temp_dict)

        request_json = {
            "userOperationType": 1,
            "users": users_list
        }

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._ADD_USERS_TO_PLAN, request_json
        )

        if flag:
            if response.json() and 'errors' in response.json():
                for error in response.json()["errors"]:
                    error_code = error["status"]["errorCode"]

                    if error_code == 0:
                        pass
                    else:
                        o_str = 'Failed to add users with error code: "{0}"'
                        raise SDKException('Plan', '102', o_str.format(error_code))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def share(self, user_or_group_name, role_name, is_user=True, ops_type=1):
        """Shares plan with given user or group by associating with given role

                Args:

                    user_or_group_name      (str)       --  User or Group name to which we are sharing

                    role_name               (str)       --  Role name which needs to associated with

                    ops_type                (int)       --  Operation type

                                                            Default : 1 (Add)

                                                            Supported : 1 (Add)
                                                                        3 (Delete)

                Returns:

                    None

                Raises:

                    SDKException:

                            if input is not valid

                            if failed to do sharing

                            if user/group/role not exists on commcell

                            if failed to get exisitng association details

        """
        if not isinstance(user_or_group_name, str) or not isinstance(role_name, str):
            raise SDKException('Plan', '101')
        if ops_type not in [1, 3]:
            raise SDKException('Plan', '102', "Sharing operation type provided is not supported")
        if is_user:
            if not self._commcell_object.users.has_user(user_or_group_name):
                raise SDKException('Plan', '102', "User doesn't exists in the commcell")
        if not self._commcell_object.roles.has_role(role_name=role_name):
            raise SDKException('Plan', '102', "Role doesn't exists in the commcell")
        request_json = copy.deepcopy(PlanConstants.PLAN_SHARE_REQUEST_JSON)
        association_response = None
        if ops_type == 1 and len(self.security_associations) > 1:
            association_request_json = copy.deepcopy(PlanConstants.PLAN_SHARE_REQUEST_JSON)
            del association_request_json['securityAssociations']
            association_request_json['entityAssociated']['entity'][0]['entityId'] = int(self._plan_id)
            flag, response = self._cvpysdk_object.make_request(
                'GET', self._API_SECURITY_ENTITY %
                (self._plan_entity_type, int(
                    self._plan_id)), association_request_json)
            if flag:
                if response.json() and 'securityAssociations' in response.json():
                    association_response = response.json(
                    )['securityAssociations'][0]['securityAssociations']['associations']
                else:
                    raise SDKException('Plan', '102', 'Failed to get existing security associations')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

        external_user = False
        if '\\' in user_or_group_name:
            external_user = True
        if is_user:
            user_obj = self._commcell_object.users.get(user_or_group_name)
            user_id = user_obj.user_id
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userId'] = int(user_id)
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = 13
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userName'] = user_or_group_name
        elif external_user:
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['groupId'] = 0
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = 62
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0][
                'externalGroupName'] = user_or_group_name
        else:
            grp_obj = self._commcell_object.user_groups.get(user_or_group_name)
            grp_id = grp_obj.user_group_id
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['userGroupId'] = int(grp_id)
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0]['_type_'] = 15
            request_json['securityAssociations']['associations'][0]['userOrGroup'][0][
                'userGroupName'] = user_or_group_name

        request_json['entityAssociated']['entity'][0]['entityId'] = int(self._plan_id)
        request_json['securityAssociations']['associationsOperationType'] = ops_type
        role_obj = self._commcell_object.roles.get(role_name)
        request_json['securityAssociations']['associations'][0]['properties']['role']['roleId'] = role_obj.role_id
        request_json['securityAssociations']['associations'][0]['properties']['role']['roleName'] = role_obj.role_name

        # Associate existing associations to the request
        if ops_type == 1 and len(self.security_associations) > 1:
            request_json['securityAssociations']['associations'].extend(association_response)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_SECURITY, request_json
        )
        if flag:
            if response.json() and 'response' in response.json():
                response_json = response.json()['response'][0]
                error_code = response_json['errorCode']
                if error_code != 0:
                    error_message = response_json['errorString']
                    raise SDKException(
                        'Plan',
                        '102', error_message)
                self.refresh()
            else:
                raise SDKException('Plan', '105')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def schedule(self, schedule_name, pattern_json, ops_type=2):
        """Creates or modifies the schedule associated with plan

                Args:

                    schedule_name       (str)       --  Schedule name

                    pattern_json        (dict)      --  Schedule pattern dict (Refer to Create_schedule_pattern in schedule.py)

                    ops_type            (int)       --  Operation type

                                                            Default : 2 (Add)

                                                            Supported : 2 (Add/Modify)

                Raises:

                      SDKException:

                            if input is not valid

                            if failed to create/modify schedule

                            if plan is not of type Data classification plan

        """
        if not isinstance(schedule_name, str) or not isinstance(pattern_json, dict):
            raise SDKException('Plan', '101')
        if self.plan_type not in [PlanTypes.DC.value]:
            raise SDKException('Plan', '102', "Add/Modify Schedule is supported only for DC Plan via CvpySDK")
        if ops_type not in [2]:
            raise SDKException('Plan', '102', "Schedule operation type provided is not supported")
        request_json = copy.deepcopy(PlanConstants.PLAN_SCHEDULE_REQUEST_JSON[self.plan_type])
        request_json['summary']['plan']['planId'] = int(self.plan_id)
        request_json['schedule']['associations'][0]['entityId'] = int(self.plan_id)
        request_json['schedule']['task']['taskName'] = f"Cvpysdk created Schedule policy for plan - {self.plan_name}"
        request_json['schedule']['subTasks'][0]['subTask'][
            'subTaskName'] = schedule_name
        request_json['schedule']['subTasks'][0]['pattern'] = pattern_json
        request_json['schedule']['subTasks'][0]['options']['adminOpts']['contentIndexingOption']['operationType'] = ops_type
        if self._dc_plan_props['targetApps'][0] == TargetApps.FS.value:
            request_json['schedule']['subTasks'][0]['subTask']['operationType'] = 5022
        self._update_plan_props(request_json)

    def edit_plan(self, **kwargs):
        """Edit plan options

                Args:

                    **kwargs for Data Classification Plan

                    index_content       (bool)      --  Speifies whether to index content or not to index server

                    content_analyzer    (list)      --  list of Content analyzer client name

                    entity_list         (list)      --  list of entities which needs to be extracted

                    classifier_list     (list)      --  list of classifier which needs to be classified

                    enable_ocr          (bool)      --  specifies whether OCR is enabled or not

                    ocr_language        (int)       --  Language to be used when doing OCR
                                                            Default : English (Value-1)

                     Supported Languages:

                                    ENGLISH = 1,
                                    HEBREW = 2,
                                    SPANISH = 3,
                                    FRENCH = 4,
                                    ITALIAN = 5,
                                    DANISH = 6

                    include_docs        (str)       --  Include documents type separated by comma

                    exclude_path        (list)      --  List of paths which needs to be excluded

                    min_doc_size        (int)       --  Minimum document size in MB

                    max_doc_size        (int)       --  Maximum document size in MB
        """
        if self.plan_type != PlanTypes.DC.value:
            raise SDKException('Plan', '102', "Function Not supported for this plan type")
        extraction_policy_list = []
        request_json = None
        if self.plan_type == PlanTypes.DC.value:
            request_json = copy.deepcopy(PlanConstants.PLAN_UPDATE_REQUEST_JSON[self.plan_type])
            request_json['summary']['plan']['planId'] = int(self.plan_id)
            if TargetApps.SDG.value in self.content_indexing_props['targetApps']:
                request_json['eePolicyInfo']['eePolicy']['detail']['eePolicy'] = self.content_indexing_props['eePolicy']
                request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy'] = self.content_indexing_props['ciPolicy']
                activate_obj = self._commcell_object.activate
                if 'content_analyzer' in kwargs:
                    ca_list = []
                    for ca in kwargs.get('content_analyzer', []):
                        ca_client_id = self._commcell_object.content_analyzers.get(ca).client_id
                        ca_list.append({
                            'clientId': ca_client_id
                        })
                    request_json['eDiscoveryInfo'] = {
                        'contentAnalyzerClient': ca_list}
                if 'entity_list' in kwargs or 'classifier_list' in kwargs:
                    entity_mgr_obj = activate_obj.entity_manager()
                    # classifier is also an activate entity with type alone different so
                    # append this to entity list itself
                    entity_list = []
                    for entity in kwargs.get('entity_list', []):
                        entity_list.append(entity)
                    for entity in kwargs.get('classifier_list', []):
                        entity_list.append(entity)
                    for entity in entity_list:
                        entity_obj = entity_mgr_obj.get(entity)
                        extraction_policy_list.append(entity_obj.container_details)
                    request_json['eePolicyInfo']['eePolicy']['detail']['eePolicy']['extractionPolicy']['extractionPolicyList'] = extraction_policy_list

                if 'enable_ocr' in kwargs:
                    request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['enableImageExtraction'] = kwargs.get(
                        'enable_ocr', False)
                    request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['ocrLanguages'] = [
                        kwargs.get('ocr_language', 1)]
                if 'include_docs' in kwargs:
                    request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters']['includeDocTypes'] = kwargs.get(
                        'include_docs', PlanConstants.DEFAULT_INCLUDE_DOC_TYPES)
                if 'min_doc_size' in kwargs:
                    request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters']['minDocSize'] = kwargs.get(
                        'min_doc_size', PlanConstants.DEFAULT_MIN_DOC_SIZE)
                if 'max_doc_size' in kwargs:
                    request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters'][
                        'maxDocSize'] = kwargs.get('max_doc_size', PlanConstants.DEFAULT_MAX_DOC_SIZE)
                if 'exclude_path' in kwargs:
                    request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters'][
                        'excludePaths'] = kwargs.get('exclude_path', PlanConstants.DEFAULT_EXCLUDE_LIST)
                if 'index_content' in kwargs:
                    request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['opType'] = kwargs.get(
                        'index_content', PlanConstants.INDEXING_METADATA_AND_CONTENT)
            elif TargetApps.FSO.value in self.content_indexing_props['targetApps']:
                # currently we dont have any thing to update in DC plan for FSO app so throw exception
                raise SDKException('Plan', '102', 'No attributes to Edit for DC Plan with TargetApps as : FSO')
        self._update_plan_props(request_json)

    def _enable_content_indexing_o365_plan(self, value):
        """Enable CI for O365 plan

            Args:
                value (bool)  --- specifies whether to content index or not

            Returns:
                None
        """
        request_json = copy.deepcopy(PlanConstants.PLAN_UPDATE_REQUEST_JSON[self.plan_type])

        request_json['summary']['plan']['planName'] = self.plan_name
        request_json['summary']['plan']['planId'] = int(self.plan_id)
        o365_arch = request_json['office365Info']['o365Exchange']['mbArchiving']['detail']['emailPolicy']
        o365_arch['archivePolicy']['contentIndexProps']['enableContentIndex'] = value

        o365_cloud = request_json['office365Info']['o365CloudOffice']['caBackup']['detail']['cloudAppPolicy'][
            'backupPolicy']
        o365_cloud['onedrivebackupPolicy']['enableContentIndex'] = value
        o365_cloud['spbackupPolicy']['enableContentIndex'] = value
        o365_cloud['teamsbackupPolicy']['enableContentIndex'] = value

        request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters'][
            'includeDocTypes'] = PlanConstants.DEFAULT_INCLUDE_DOC_TYPES
        request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters'][
            'minDocSize'] = PlanConstants.DEFAULT_MIN_DOC_SIZE

        request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy']['filters']['fileFilters'][
            'maxDocSize'] = PlanConstants.DEFAULT_MAX_DOC_SIZE
        request_json['ciPolicyInfo']['ciPolicy']['detail']['ciPolicy'][
            'opType'] = PlanConstants.INDEXING_METADATA_AND_CONTENT
        request_json['ciPolicy'] = request_json['ciPolicyInfo']['ciPolicy']

        self._update_plan_props(request_json)

    def policy_subclient_ids(self):
        """Returns Policy subclient IDs of the plan
        
        Returns:
            dict : OS and its associated subclient ID
        
        example:
            {
                'Windows' : windows_subclient_policy_subclient_id,
                'Linux' : linux_subclient_policy_subclient_id,
                'Mac' : mac_subclient_policy_subclient_id
            }
        
        """
        result = dict()
        for backupset_id in self.subclient_policy:
            url = self._commcell_object._services['ADD_SUBCLIENT'] + '?clientId=2&applicationId=1030&backupsetid=' + str(backupset_id)

            flag, response = self._commcell_object._cvpysdk_object.make_request('GET', url)
            if flag:
                if response.json() and 'subClientProperties' in response.json():
                    subclient_id = response.json()['subClientProperties'][0]['subClientEntity']['subclientId']
                    backupset_name = response.json()['subClientProperties'][0]['subClientEntity']['backupsetName']
                    os = backupset_name.split()[-3]
                    result[os] = subclient_id
                else:
                    raise SDKException('Plan', 102, 'Failed to get subclient Ids.')
            else:
                raise SDKException('Plan', 102, response.text)
            
        return result
    
    def __update_content_policy(self, content):
        """
        Args:
            content (dict)  :  dictionary with backup content details. 
            
            example:
                content = {
                    "windowsIncludedPaths": ["Desktop"],
                    "windowsExcludedPaths": ["Music"],
                    "windowsFilterToExcludePaths": ["Videos"],
                    "unixIncludedPaths": ["Desktop"],
                    "unixExcludedPaths": ["Music"],
                    "unixFilterToExcludePaths": ["Videos"],
                    "macIncludedPaths": ["Desktop"],
                    "macExcludedPaths": ["Music"],
                    "macFilterToExcludePaths": ["Videos"],
                    "backupSystemState": True,
                    "useVSSForSystemState": True,
                    "backupSystemStateOnlyWithFullBackup": False
                }

            For unix and mac, replace key name with respective os name, **IncludedPaths, **ExcludedPaths, **FilterToExcludePaths

        """
        
        request_json = {
            'backupContent' : content
        }

        request_url = self._commcell_object._services['V4_SERVER_PLAN'] % self.plan_id

        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', request_url, request_json)

        self.__handle_response(flag, response, f'Failed to update backup content for Plan: {self.plan_name}')

    def __map_content_to_new_format(self, content):
        """
            Method to map old content format to new format (if we need to update the content policy of plan)
            
            Note: We cannot remove the old format as it is still can be used to modify the content of plans created before SP32. So mapping old content to new ones as needed.
        """
        result = {
            "windowsIncludedPaths": [],
            "windowsExcludedPaths": [],
            "windowsFilterToExcludePaths": [],
            "unixIncludedPaths": [],
            "unixExcludedPaths": [],
            "unixFilterToExcludePaths": [],
            "macIncludedPaths": [],
            "macExcludedPaths": [],
            "macFilterToExcludePaths": [],
            "backupSystemState": True,
            "useVSSForSystemState": True,
            "backupSystemStateOnlyWithFullBackup": False
        }

        if 'Linux' in content:
            content['Unix'] = content.pop('Linux')

        for os, data in content.items():
            included_paths_key = f"{os.lower()}IncludedPaths"
            excluded_paths_key = f"{os.lower()}ExcludedPaths"
            filter_to_exclude_paths_key = f"{os.lower()}FilterToExcludePaths"

            if 'Content' in data:
                result[included_paths_key] = [path.split('%')[-2] for path in data['Content']]

            if 'Exclude' in data:
                result[excluded_paths_key] = [path.split('%')[-2] for path in data['Exclude']]

            if 'Except' in data:
                result[filter_to_exclude_paths_key] = [path.split('%')[-2] for path in data['Except']]

            if os == 'Windows':
                result['backupSystemState'] = data.get('Backup System State', True)
                result['useVSSForSystemState'] = data.get('useVSSForSystemState', True)
                result['backupSystemStateOnlyWithFullBackup'] = data.get('backupSystemStateOnlyWithFullBackup', False)

        return result
    
    def update_backup_content(self, content, request_type = 'OVERWRITE'):
        """
        Args:
            content (dict)  :  dictionary with backup content details. 
            
            example: 
                content = {
                    'Windows' : {
                        'Content' : ['\\%Pictures%', '\\%Desktop%'],
                        'Exclude' : ['\\%Documents%'],
                        'Except' : ['\\%Documents%'],
                        'Backup System State' : True
                    },
                    'Linux' : {
                        'Content' : ['/%Pictures%'],
                        'Exclude' : ['/%Documents%']
                    },
                    'Mac' : {
                        'Content' : ['/%Pictures%'],
                        'Exclude' : ['/%Documents%']
                    }
                }
                    
            request_type (str)      :  Supported values 'OVERWRITE' (default), 'UPDATE', 'DELETE'. 

            For plans created from SP32, Please use below format of content
            example:
                content = {
                    "windowsIncludedPaths": ["Desktop"],
                    "windowsExcludedPaths": ["Music"],
                    "windowsFilterToExcludePaths": ["Videos"],
                    "backupSystemState": True,
                    "useVSSForSystemState": True,
                    "backupSystemStateOnlyWithFullBackup": False
                }

            For unix and mac, replace key name with respective os name, **IncludedPaths, **ExcludedPaths, **FilterToExcludePaths
        """
        
        update_request_type = {
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3
        }
        
        subclients = self.policy_subclient_ids()

        if not subclients:
            if 'Windows' in content or 'Linux' in content or 'Mac' in content:
                content = self.__map_content_to_new_format(content)
            self.__update_content_policy(content)
            return
        
        for os, value in content.items():
            request_json = {
                "subClientProperties": {
                    "fsExcludeFilterOperationType": update_request_type.get(request_type, 1),
                    "fsContentOperationType" : update_request_type.get(request_type, 1)
                }
            }
            
            request_url = self._commcell_object._services['SUBCLIENT'] % subclients[os]
            
            contents = list()
            for key, val in value.items():
                if key.lower() == 'content':
                    for path in val: contents.append({"path" : path})
                if key.lower() == 'exclude':
                    for path in val: contents.append({"excludePath" : path})
                if os == 'Windows' and key == 'Backup System State':
                    request_json['subClientProperties']['fsSubClientProp'] = {'backupSystemState' : val}
                    
            if contents:
                request_json['subClientProperties']['content'] = contents
            
            flag, response = self._commcell_object._cvpysdk_object.make_request('POST', request_url, request_json)
                
            if flag:
                if response.json() and 'response' in response.json():
                    errorCode = response.json()['response'][0].get('errorCode')
                    if errorCode:
                        raise SDKException('Plan', 102, 'Failed to Change Content of Plan.')
                else:
                    raise SDKException('Plan', 102, 'Failed to get subclient Ids.')
            else:
                raise SDKException('Plan', 102, response.text)

    def enable_data_aging(self, plan_copy_id: int, is_enable=True):

        """Method is used to enable/disable the data aging for the plan copy

            Args:
                plan_copy_id(int)      :   copy_id of the plan

                is_enable(bool)       :   value whether to be unable or disable the data aging

                                      example: true = enable
                                               false = disable
            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        payload = {
            "retentionRules": {
                "enableDataAging": is_enable
            }
        }

        api_url = self._services['ENABLE_DATA_AGING'] % (self._plan_id, plan_copy_id)
        flag, response = self._cvpysdk_object.make_request(method='PUT',
                                                           url=api_url, payload=payload)
        if not flag:
            raise SDKException('Response', '101',
                               self._commcell_object._update_response_(response.text))
        if not response:
            raise SDKException('Response', '102',
                               self._commcell_object._update_response_(response.text))

    @property
    def applicable_solutions(self):
        """Method to read applicable solutions"""
        return self._applicable_solutions

    @applicable_solutions.setter
    def applicable_solutions(self, solutions: list = list()):
        """Method to update applicable solutions of plan
        
        Args:
            solutions (list) : List of Applicable Solutions
            
            example: 
                ["File Servers", "Databases"] : FS and DB will be set as a applicable solutions
                [] : Passing empty list will reset applicable solutions to ALL
            
        """
        request_url  = self._commcell_object._services['APPLICABLE_SOLNS_ENABLE' if solutions else 'APPLICABLE_SOLNS_DISABLE'] % self.plan_id
        
        if solutions:
            supported_solutions =  self._commcell_object.plans.get_supported_solutions()
            request_json = {"solutions": [{"id": supported_solutions[soln_name], "name": soln_name} for soln_name in solutions]}
        else:
            request_json = None
                    
        flag, response = self._commcell_object._cvpysdk_object.make_request('PUT', request_url, request_json)
        
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))
        
        if not response.json() or response.json()['errorCode']:
            raise SDKException('Plan', 102, 'Failed to update Applicable Solutions for Plan')
                
        self.refresh()
