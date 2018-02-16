# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing plan operations.

Plans and Plan are the classes defined in this file.

Plans: Class for representing all the plans in the commcell

Plan: Class for representing a single plan of the commcell

Plans:
    __init__(commcell_object)   --  initialise object of plans class of the commcell

    __str__()                   --  returns all the plans associated with the commcell

    __repr__()                  --  returns the string for the instance of the plans class

    _get_plans()                --  gets all the plans associated with the commcell specified

    _get_plan_template()        --  gets the Plan subtype's JSON template

    add()                       --  adds a new Plan to the CommCell

    has_plan()                  --  checks if a plan exists with the given name or not

    get()                       --  returns the instance of the Plans class

    delete()                    --  deletes the plan from the commcell

    refresh()                   --  refresh the plans associated with the commcell


Plan:
    __init__()                  -- initialise instance of the plan for the commcell

    __repr__()                  -- return the plan name, the instance is associated with

    _get_plan_id()              -- method to get the plan id, if not specified in __init__

    _get_plan_properties()      -- get the properties of this plan

    plan_name                   --  returns the name of the plan

    plan_id                     --  returns the ID of the plan

    refresh()                   --  refresh the properties of the plan

    associate_user()            --  associates users to the plan


"""

from __future__ import unicode_literals

from past.builtins import basestring

from .exception import SDKException
from .clientgroup import ClientGroup
from .usergroup import UserGroup


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
                plan_subType    (str)   --  Sub-type of plan to add

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

        """
        if not (isinstance(plan_sub_type, basestring) and
                isinstance(plan_type, basestring)):
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
        if not isinstance(plan_name, basestring):
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
        if not isinstance(plan_name, basestring):
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
        if not isinstance(plan_name, basestring):
            raise SDKException('Plan', '101')
        else:
            plan_name = plan_name.lower()

            if self.has_plan(plan_name):
                plan_id = self._plans[plan_name]

                delete_plan = self._services['DELETE_PLAN'] % (plan_id)

                flag, response = self._cvpysdk_object.make_request('DELETE', delete_plan)

                error_code = -1

                if flag:
                    if 'errorCode' in response.json():
                        error_code = response.json()['errorCode']

                    if error_code != 0:
                        o_str = 'Failed to delete plan'
                        error_message = response.json()['errorMessage']
                        if error_message:
                            o_str += '\nError: "{0}"'.format(error_message)
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
            storage_pool_name,
            sla_in_minutes=240,
            override_entities=None):
        """Adds a new Plan to the CommCell.

        Args:
            plan_name           (str)   --  name of the new plan to add

            plan_sub_type       (str)   --  Type of plan to add

                "Server"    -   Server Plans

                "FSServer"  -   File System Plans

                "Laptop"    -   Laptop Plans


            storage_pool_name   (str)   --  name of the storage pool to be used for the plan

            sla_in_minutes      (int)   --  Backup SLA in hours

                default: 240

            override_entities   (dict)  --  Specify the entities with respective overriding.

                default: None

                    {
                        'private': [1, 4, 256, 512, 1024],

                        'enforced': []
                    }


        Returns:
            object  -   instance of the Plan class created by this method

        Raises:
            SDKException:

        """
        if not (isinstance(plan_name, basestring) and
                isinstance(plan_sub_type, basestring) and
                isinstance(storage_pool_name, basestring)):
            raise SDKException('Plan', '101')
        else:
            if self.has_plan(plan_name):
                raise SDKException(
                    'Plan', '102', 'Plan "{0}" already exists'.format(plan_name)
                )

        storage_pool_id = int(self._commcell_object.storage_pools.get(storage_pool_name))

        request_json = self._get_plan_template(plan_sub_type, "MSP")

        request_json['plan']['summary']['slaInMinutes'] = sla_in_minutes
        request_json['plan']['summary']['description'] = "Created from CvPySDK."
        request_json['plan']['summary']['plan']['planName'] = plan_name
        request_json['plan']['storage']['copy'][0]['dedupeFlags']['useGlobalDedupStore'] = 1
        request_json['plan']['storage']['copy'][0]['useGlobalPolicy'] = {
            "storagePolicyId": storage_pool_id
        }

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

                if 'errorCode' in response_value:
                    error_code = response_value['errorCode']

                if 'errorMessage' in response_value:
                    error_message = response_value['errorMessage']

                if error_message:
                    o_str = 'Failed to create new Plan\nError: "{0}"'.format(
                        error_message
                    )
                    raise SDKException('Plan', '102', o_str)

                if 'plan' in response_value:
                    plan_name = response_value['plan']['summary']['plan']['planName']

                    # initialize the plans again
                    # so that the plans object has all the plans
                    self.refresh()

                    return self.get(plan_name)
                else:
                    o_str = ('Failed to create new plan due to error code: "{0}"\n'
                             'Please check the documentation for '
                             'more details on the error').format(error_code)

                    raise SDKException('Backupset', '102', o_str)
            else:
                raise SDKException('Response', 102)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the plans associated with the Commcell."""
        self._plans = self._get_plans()


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

        if plan_id:
            self._plan_id = str(plan_id)
        else:
            self._plan_id = self._get_plan_id()

        self._PLAN = self._services['PLAN'] % (self.plan_id)
        self._ADD_USERS_TO_PLAN = self._services['ADD_USERS_TO_PLAN'] % (self.plan_id)

        self._properties = None
        self._sla_in_minutes = None
        self._plan_type = None
        self._subtype = None
        self._permissions = []
        self._storage_pool = None
        self._child_policies = {
            'storagePolicyId': None,
            'schedulePolicyId': None,
            'subclientPolicyIds': []
        }
        self._user_group = None
        self._client_group = None
        self._override_entities = None
        self._parent_plan_id = None
        # self._security_associations = {}

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
        plan_properties_url = '{0}?propertyLevel=20'.format(self._PLAN)
        flag, response = self._cvpysdk_object.make_request('GET', plan_properties_url)

        if flag:
            if response.json() and 'plan' in response.json():
                plan_properties = response.json()['plan']

                if 'slaInMinutes' in plan_properties['summary']:
                    self._sla_in_minutes = plan_properties['summary']['slaInMinutes']

                if 'type' in plan_properties['summary']:
                    self._plan_type = plan_properties['summary']['type']

                if 'subtype' in plan_properties['summary']:
                    self._subtype = plan_properties['summary']['subtype']

                if 'useGlobalPolicy' in plan_properties['storage']['copy'][0]:
                    self._storage_pool = plan_properties['storage']['copy'][0]['useGlobalPolicy']

                if self._subtype == 33554439:
                    if 'clientGroup' in plan_properties['autoCreatedEntities']:
                        self._client_group = ClientGroup(
                            self._commcell_object,
                            plan_properties['autoCreatedEntities']['clientGroup'][
                                'clientGroupName']
                        )

                    if 'localUserGroup' in plan_properties['autoCreatedEntities']:
                        self._user_group = UserGroup(
                            self._commcell_object,
                            plan_properties['autoCreatedEntities']['localUserGroup'][
                                'userGroupName']
                        )

                if 'storagePolicy' in plan_properties['storage']:
                    self._child_policies['storagePolicyId'] = plan_properties['storage'][
                        'storagePolicy']['storagePolicyId']

                if 'task' in plan_properties['schedule']:
                    self._child_policies['schedulePolicyId'] = plan_properties['schedule'][
                        'task']['taskId']

                if self._subtype != 33554437:
                    if 'backupContent' in plan_properties['laptop']['content']:
                        for ida in plan_properties['laptop']['content']['backupContent']:
                            self._child_policies['subclientPolicyIds'].append(
                                ida['subClientPolicy']['backupSetEntity']['backupsetId']
                            )

                if ('inheritance' in plan_properties and
                        not plan_properties['inheritance']['isSealed']):
                    temp_dict = plan_properties['inheritance']
                    del temp_dict['isSealed']
                    self._override_entities = temp_dict

                if 'parent' in plan_properties['summary']:
                    self._parent_plan_id = plan_properties['summary']['parent']['planId']

                return plan_properties
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def plan_id(self):
        """Treats the plan id as a read-only attribute."""
        return self._plan_id

    @property
    def plan_name(self):
        """Treats the plan name as a read-only attribute."""
        return self._plan_name

    @property
    def sla_in_minutes(self):
        """Treats the plan SLA as a read-only attribute."""
        return self._sla_in_minutes

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
