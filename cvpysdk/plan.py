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

Attributes
----------

    **all_plans**   --  returns the dict consisting of plans and their details


Plan
====

    __init__()                  -- initialise instance of the plan for the commcell

    __repr__()                  -- return the plan name, the instance is associated with

    _get_plan_id()              -- method to get the plan id, if not specified in __init__

    _get_plan_properties()      -- get the properties of this plan

    _update_plan_props()        -- method to update plan properties

    _get_associated_entities()  -- method to get list of entities associated to a plan

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
"""
from __future__ import unicode_literals

import copy
from enum import Enum

from .exception import SDKException

from .activateapps.constants import TargetApps, PlanConstants
from functools import reduce


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
        self._plans = None
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

                for temp in response_value:
                    temp_name = temp['plan']['planName'].lower()
                    temp_id = str(temp['plan']['planId']).lower()
                    plans[temp_name] = temp_id

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
    
    def filter_plans(self, plan_type, company_name = None):
        """
        Returns the dictionary consisting of specified type and company plans.

        Args:
            plan_type (str)      --      Type of plan ['DLO', 'Server', 'Laptop', 'Database', 'FSServer', 'FSIBMiVTL', 'Snap', 'VSAServer', 'VSAReplication', 
                                                        'ExchangeUser', 'ExchangeJournal', 'Office365', 'Dynamics365', 'DataClassification', 'Archiver']

            company_name (str)    --     To filter plans based on company. For Commcell, company_name = "". Default will return all plans

        Returns:
            dict - consists of all the plans with specified types configured on the commcell

                {
                    "plan1_name": plan1_id,

                    "plan2_name": plan2_id
                }

        Raises:
            SDKException:
                if input data type is not valid
                
                if invalid plan type is passed as parameter

                if failed to get the response
        """
        plan_type_subtype = {
                "dlo" : ("1", "16777223"),
                "server" : ("2", "33554437"),
                "laptop" : ("2", "33554439"),
                "database" : ("2", "33579013"),
                "fsserver" : ("3", "50331655"),
                "fsibmivtl" : ("3", "50331653"),
                "snap" : ("4", "67108869"),
                "vsaserver" : ("5", "83886085"),
                "vsareplication" : ("5", "83918853"),
                "exchangeuser" : ("6", "100859907"),
                "exchangejournal" : ("6", "100794372"),
                "office365" : ("6", "100859937"),
                "dynamics365" : ("6", "100794391"),
                "dataclassification" : ("7", "117506053"),
                "archiver" : ("9", "150994951")
        }
        
        if not isinstance(plan_type, str):
            raise SDKException('Plan', '101')
        elif plan_type.lower() not in plan_type_subtype:
            raise SDKException('Plan', '102', 'Invalid Plan Type Passed as Parameter')
        else:
            template_url = self._services['GET_PLANS'] % plan_type_subtype[plan_type.lower()]

            flag, response = self._cvpysdk_object.make_request('GET', template_url)

            if flag:
                result = dict()
                if 'plans' in response.json():
                    for plan in response.json()['plans']:
                        if company_name is None:
                            result[plan['plan']['planName']] = plan['plan']['planId']
                        else:
                            if plan['plan']['entityInfo']['companyName'].lower() == company_name.lower():
                                result[plan['plan']['planName']] = plan['plan']['planId'] 
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
        if not plan_sub_type == 'ExchangeUser':
            storage_pool_obj = self._commcell_object.storage_pools.get(
                storage_pool_name)
            is_dedupe = True
            if 'dedupDBDetailsList' \
                    not in storage_pool_obj._storage_pool_properties['storagePoolDetails']:
                is_dedupe = False

        request_json = self._get_plan_template(plan_sub_type, "MSP")

        request_json['plan']['summary']['rpoInMinutes'] = sla_in_minutes
        request_json['plan']['summary']['description'] = "Created from CvPySDK."
        request_json['plan']['summary']['plan']['planName'] = plan_name
        request_json['plan']['schedule']['subTasks'][1]['options']['commonOpts'][
            'automaticSchedulePattern'].update({
                'minBackupInterval': 0,
                'maxBackupIntervalMinutes': 0,
                'minSyncInterval': 0,
                'minSyncIntervalMinutes': 0
            })
        request_json['plan']['schedule']['subTasks'][1]['options']['commonOpts'][
            'automaticSchedulePattern']['ignoreOpWindowPastMaxInterval'] = True
        del request_json['plan']['schedule']['task']['taskName']
        if not plan_sub_type == 'ExchangeUser':
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
            request_json['plan']['storage']['copy'][1]['extendedFlags'] = {
                'useGlobalStoragePolicy': 1
            }
            request_json['plan']['storage']['copy'][1]['useGlobalPolicy'] = {
                "storagePolicyId": int(storage_pool_obj.storage_pool_id)
            }

        # Enable full backup schedule
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

    def refresh(self):
        """Refresh the plans associated with the Commcell."""
        self._plans = self._get_plans()

    def add_data_classification_plan(self, plan_name, index_server, target_app=TargetApps.FSO, **kwargs):
        """Adds data classification plan to the commcell

            Args:

                plan_name           (str)       --  Name of plan

                index_server        (str)       --  Index server name


                target_app          (enum)      --  Target app for this plan
                                                        cvpysdk.activateapps.constants.TargetApps

                **kwargs

                    index_content       (bool)      --  Speifies whether to index content or not to index server

                    content_analyzer    (list)      --  list of Content analyzer cloud name

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
                ca_cloud_id = self._commcell_object.content_analyzers.get(ca).cloud_id
                ca_list.append({
                    'cloudId': ca_cloud_id
                })
            request_json['plan']['eDiscoveryInfo']['contentAnalyzerCloud'] = ca_list
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
        self._ADD_USERS_TO_PLAN = self._services['ADD_USERS_TO_PLAN'] % (self.plan_id)
        self._API_SECURITY = self._services['SECURITY_ASSOCIATION']
        self._API_SECURITY_ENTITY = self._services['ENTITY_SECURITY_ASSOCIATION']

        self._properties = None
        self._sla_in_minutes = None
        self._operation_window = None
        self._full_operation_window = None
        self._plan_type = None
        self._subtype = None
        self._security_associations = {}
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
        self.refresh()

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

                    if 'storagePolicy' in self._plan_properties['storage']:
                        self._commcell_object.storage_policies.refresh()
                        self._child_policies['storagePolicy'] = self._commcell_object.storage_policies.get(
                            self._plan_properties['storage']['storagePolicy']['storagePolicyName']
                        )

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

                if 'schedule' in self._plan_properties:
                    if 'task' in self._plan_properties['schedule']:
                        self._commcell_object.schedule_policies.refresh()
                        self._child_policies['schedulePolicy'] = {
                            'data': self._commcell_object.policies.schedule_policies.get(
                                self._plan_properties['schedule']['task']['taskName']
                            )
                        }
                        if self._subtype == 33554437:
                            self._child_policies['schedulePolicy'].update({
                                'log': self._commcell_object.policies.schedule_policies.get(
                                    self._plan_properties[
                                        'database']['scheduleLog']['task']['taskName']
                                )
                            })

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

                if 'securityAssociations' in self._plan_properties:
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
    def plan_name(self, value):
        """modifies the plan name"""
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

    @property
    def storage_policy(self):
        """Treats the plan storage policy as a read-only attribute"""
        return self._child_policies['storagePolicy']

    @property
    def storage_copies(self):
        """Treats the plan storage policy as a read-only attribute"""
        return self._storage_copies

    @property
    def schedule_policies(self):
        """Treats the plan schedule policies as read-only attribute"""
        return self._child_policies['schedulePolicy']

    @property
    def addons(self):
        """Treats the plan addons as read-only attribute"""
        for addon in self._plan_properties.get('summary', {}).get('addons', []):
            self._addons.append(
                addon
            )
        return self._addons

    @property
    def subclient_policy(self):
        """Treats the plan subclient policy as a read-only attribute"""
        return self._child_policies['subclientPolicyIds']

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

    @property
    def content_indexing_props(self):
        """returns the DC plan related CI properties from Plan"""
        return self._dc_plan_props

    @property
    def properties(self):
        """Returns the configured properties for the Plan"""
        return self._plan_properties

    def refresh(self):
        """Refresh the properties of the Plan."""
        self._properties = self._get_plan_properties()

    def associate_user(self, userlist):
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
                    'sendInvite': True,
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
        self._update_plan_props(request_json)

    def edit_plan(self, **kwargs):
        """Edit plan options

                Args:

                    **kwargs for Data Classification Plan

                    index_content       (bool)      --  Speifies whether to index content or not to index server

                    content_analyzer    (list)      --  list of Content analyzer cloud name

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
                        ca_cloud_id = self._commcell_object.content_analyzers.get(ca).cloud_id
                        ca_list.append({
                            'cloudId': ca_cloud_id
                        })
                    request_json['eDiscoveryInfo'] = {
                        'contentAnalyzerCloud': ca_list}
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
    
    def update_backup_content(self, content, request_type = 'OVERWRITE'):
        """
        Args:
            content (dict)  :  dictionary with backup content details. 
            
            example: 
                content = {
                    'Windows' : {
                        'Content' : ['\\%Pictures%', '\\%Desktop%'],
                        'Exclude' : ['\\%Documents%'],
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
                    
            request_type (str)      :  Supported values 'OVERWRITE' (default), 'UPDATE', 'DELETE'. 
        }
        """
        
        update_request_type = {
            "OVERWRITE": 1,
            "UPDATE": 2,
            "DELETE": 3
        }
        
        subclients = self.policy_subclient_ids()
        
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
