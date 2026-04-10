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


"""
Main file for performing resource group operations in the Commcell Security Center.

ResourceGroups and ResourceGroup are the classes defined in this file.

ResourceGroups: Class for representing all the resource groups associated with a Commcell.

ResourceGroup:  Class for representing a single resource group of the Commcell.

ResourceGroups:
===============

    __init__(commcell_object)      -- initializes an instance of ResourceGroups for the specified Commcell

    __str__()                      -- returns all the resource groups associated with the Commcell

    __repr__()                     -- returns the string for the instance of the ResourceGroups class

    __len__()                      -- returns the number of resource groups associated with the Commcell

    all_resource_groups            -- returns the dict of all resource groups on the Commcell

    _get_resource_groups()         -- gets all the resource groups associated with the Commcell

    refresh()                      -- refreshes the resource groups associated with the Commcell

    has(name)       -- checks if a resource group exists with the given name

    get(name)                      -- returns the instance of the ResourceGroup class for the input resource group name

    create(name, plan_name, clients) -- creates a new resource group with the specified plan and clients

    delete(name)                   -- deletes the resource group from the Commcell

ResourceGroups Attributes
-------------------------

    **all_resource_groups**        -- returns the dict of all resource groups on the Commcell

ResourceGroup:
==============

    __init__(commcell_object, resource_group_name) -- initializes object of ResourceGroup class with the specified name

    __repr__()                     -- returns the resource group name the instance is associated with

    update_ti_plan(plan_name)      -- associates a Threat Intelligence plan with the resource group

    update_manual_associations(clients) -- updates the client associations for the resource group

ResourceGroup Attributes
------------------------

    **name**                       -- returns the name of the resource group

    **resource_group_id**          -- returns the id of the resource group

    **resource_group_name**        -- returns the name of the resource group

"""
import copy
from enum import Enum

from cvpysdk.clientgroup import ClientGroup, ClientGroups
from cvpysdk.exception import SDKException
from cvpysdk.securitycenter.constants import FQ_PARAMETERS, UPDATE_TI_PLAN_JSON, RESOURCE_GROUP_PAYLOAD_MANUAL, \
    RESOURCE_GROUP_PAYLOAD_AUTOMATIC, FL_PARAMETERS, RESOURCE_GROUP_PAYLOAD_MANUAL_UPDATE


class ResourceTypes(Enum):
    """Class to represent different FSO types(Server/ServerGroup/Project)"""
    THREAT_DETECTION = 0


class ResourceGroups():
    """Class for representing all resource groups associated with a Commcell."""

    def __init__(self, commcell_object, configtype = ResourceTypes.THREAT_DETECTION):
        """Initializes an instance of the ResourceGroups class.

        Args:
            commcell_object (object): Instance of the Commcell class.
            configtype (ResourceTypes) : Type of resource group. Default is THREAT_DETECTION

        Returns:
            object: Instance of the ResourceGroups class.
        """
        self._commcell_object = commcell_object
        self._SERVICEGROUPS = self._commcell_object._services['SERVERGROUPS_V4']
        self._update_response_ = commcell_object._update_response_
        self._resource_groups = None
        self._configtype = configtype
        self.refresh()

    def __str__(self):
        """Returns a string representation of all resource groups in the Commcell.

        Returns:
            str: String listing all resource groups for the Commcell.
        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'ResourceGroup')

        for index, resource_group_name in enumerate(self._resource_groups):
            sub_str = '{:^5}\t{:50}\n'.format(index + 1, resource_group_name)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Returns a string representation of the ResourceGroups class instance.

        Returns:
            str: String describing the ResourceGroups class instance.
        """
        return "ResourceGroups class instance for Commcell"

    def __len__(self):
        """Returns the number of resource groups associated with the Commcell.

        Returns:
            int: Number of resource groups.
        """
        return len(self.all_resource_groups)

    @property
    def all_resource_groups(self):
        """Returns a dictionary of all resource groups associated with this Commcell.

        Returns:
            dict: Dictionary of all resource groups in the Commcell.
                {
                    "resourcegroup1_name": resourcegroup1_id,
                    "resourcegroup2_name": resourcegroup2_id,
                }
        """
        return self._resource_groups

    def _get_resource_groups(self, full_response=False):
        """Fetches all resource groups associated with the Commcell.

        Args:
            full_response (bool): If True, returns the full response JSON. Default: False.

        Returns:
            dict or list: Dictionary of resource groups or full response JSON.

        Raises:
            SDKException: If response is empty or unsuccessful.
        """
        request_url = f"{self._SERVICEGROUPS}?" + FQ_PARAMETERS[self._configtype.name] + FL_PARAMETERS[self._configtype.name]
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', request_url)

        if flag:
            server_groups = {}

            if response.json() and 'serverGroups' in response.json():
                if full_response:
                    return response.json()

                name_count = {}

                for temp in response.json()['serverGroups']:
                    temp_name = temp.get('name', '').lower()
                    temp_company = temp.get('company', {}).get('name', '').lower()

                    if temp_name in name_count:
                        name_count[temp_name].add(temp_company)
                    else:
                        name_count[temp_name] = {temp_company}

                for temp in response.json()['serverGroups']:
                    temp_name = temp.get('name', '').lower()
                    temp_id = temp.get('id', '')
                    temp_company = temp.get('company', {}).get('name', '').lower()

                    if len(name_count[temp_name]) > 1:
                        unique_key = f"{temp_name}_({temp_company})"
                    else:
                        unique_key = temp_name

                    server_groups[unique_key] = temp_id

            return server_groups
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refreshes the list of resource groups associated with the Commcell."""
        self._resource_groups = self._get_resource_groups()

    def has(self, resource_group_name):
        """Checks if the specified resource group exists in the Commcell.

        Args:
            resource_group_name (str): Name of the resource group.

        Returns:
            bool: True if the resource group exists, False otherwise.

        Raises:
            SDKException: If resource_group_name is not a string.
        """
        if not isinstance(resource_group_name, str):
            raise SDKException('ResourceGroups', '101')

        return self._resource_groups and resource_group_name.lower() in self._resource_groups

    def get(self, resource_group_name):
        """Returns the ResourceGroup object for the specified resource group name.

        Args:
            resource_group_name (str): Name of the resource group.

        Returns:
            ResourceGroup: Instance of the ResourceGroup class.

        Raises:
            SDKException: If resource_group_name is not a string, or if the resource group does not exist.
        """
        if not isinstance(resource_group_name, str):
            raise SDKException('ResourceGroup', '101')
        else:
            resource_group_name = resource_group_name.lower()

            if self.has(resource_group_name):
                return ResourceGroup(
                    self._commcell_object,
                    resource_group_name,
                    self._resource_groups[resource_group_name]
                )

            raise SDKException(
                'ResourceGroups', '102', 'No resource group exists with name: {0}'.format(
                    resource_group_name))

    def create(self, resource_group_name, plan_name, clients=None, rule_group_json=None):
        """Creates a new resource group in the Commcell.

        Args:
            resource_group_name (str): Name of the new resource group.
            plan_name (str): Name of the Threat Intelligence plan to associate.
            clients (list): List of clients to add to the resource group. Default: None.
            rule_group_json (dict): JSON defining the rule group for automatic association. Default: None.
            example: {
            "match": "AND",
            "ruleGroup": [
                {
                    "match": "AND",
                    "rules": [
                        {
                            "ruleName": "CLIENT_DISPLAY_NAME",
                            "ruleValue": "m",
                            "matchCondition": "CONTAINS"
                        }
                    ]
                }
            ]
        }

        Returns:
            ResourceGroup: Instance of the created ResourceGroup class.

        Raises:
            Raises:
                SDKException:
                    if type of resource group name and description is not of type string

                    if clients argument is not of type list / string

                    if response is empty

                    if response is not success

                    if resource group already exists with the given name
        """
        if clients is None and rule_group_json is None:
            raise SDKException('ResourceGroup', '102', 'Clients list or rule group json must be provided to create a resource group')
        if not isinstance(resource_group_name, str):
            raise SDKException('ResourceGroup', '101')
        if not isinstance(plan_name, str):
            raise SDKException('ResourceGroup', '101')

        if self.has(resource_group_name):
            raise SDKException(
                'ResourceGroup', '102',
                'Resource group with name "{0}" already exists'.format(resource_group_name)
            )

        if clients is not None:
            request_json = copy.deepcopy(RESOURCE_GROUP_PAYLOAD_MANUAL)
            for client in clients:
                client = str(client)
                request_json['manualAssociation']['associatedservers'].append(
                    {"id": int(self._commcell_object.clients.get(client).client_id)}
                )
        else:
            request_json = copy.deepcopy(RESOURCE_GROUP_PAYLOAD_AUTOMATIC)
            request_json["automaticAssociation"]["serverGroupRule"] = rule_group_json

        request_json['name'] = resource_group_name
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._SERVICEGROUPS, request_json
        )

        if flag:
            response_json = response.json()
            if 'serverGroupInfo' in response_json:
                resource_group_id = response_json['serverGroupInfo'].get('id',0)
                resource_group = ResourceGroup(self._commcell_object, resource_group_name, resource_group_id)
                resource_group.update_ti_plan(plan_name)
                self._commcell_object.client_groups.refresh()
                return resource_group
            elif 'error' in response_json:
                error_code = response_json['error']['errorCode']
                if error_code != 0:
                    error_message = response_json['error']['errorMessage']
                    raise SDKException('ResourceGroup', '102', error_message)
        else:
            response_json = response.json()
            if 'error' in response_json:
                error_code = response_json['error']['errorCode']
                if error_code != 0:
                    error_message = response_json['error']['errorMessage']
                    raise SDKException('ResourceGroup', '102', error_message)

            else:
                raise SDKException('Response', '102', 'Invalid response received from server')
       

    def delete(self, resource_group_name):
        """Deletes the specified resource group from the Commcell.

        Args:
            resource_group_name (str): Name of the resource group to delete.

        Returns:
            None

        Raises:
                SDKException:
                    if type of resource group name is not of type string

                    if response is empty

                    if response is not success
        """
        self._commcell_object.client_groups.delete(resource_group_name)        
        self.refresh()

class ResourceGroup(ClientGroup):
    """Class for representing a single resource group."""

    def __init__(self, commcell_object, resource_group_name, resource_group_id=None):
        """Initializes an instance of the ResourceGroup class.

        Args:
            commcell_object (object): Instance of the Commcell class.
            resource_group_name (str): Name of the resource group.

        Returns:
            object: Instance of the ResourceGroup class.
        """
        super().__init__(commcell_object, resource_group_name)
        self._commcell_object = commcell_object
        self._resource_group_name = resource_group_name
        self._resource_group_id = resource_group_id

    def __repr__(self):
        """Returns a string representation of the ResourceGroup class instance.

        Returns:
            str: String describing the ResourceGroup class instance.
        """
        representation_string = 'ResourceGroup class instance for ResourceGroup: "{0}"'
        return representation_string.format(self._resource_group_name)

    def update_ti_plan(self, plan_name):
        """Associates a Threat Intelligence plan with the resource group.

        Args:
            plan_name (str): Name of the Threat Intelligence plan to associate.

        Returns:
            None

        Raises:
                SDKException:
                    if type of plan name is not of type string

                    if response is empty

                    if response is not success
        """
        if not isinstance(plan_name, str):
            raise SDKException('ResourceGroup', '101')

        plan_id = int(self._commcell_object.plans.get(plan_name).plan_id)
        request_json = copy.deepcopy(UPDATE_TI_PLAN_JSON)
        request_json['clientGroupDetail']['tiPlan']['planName'] = plan_name
        request_json['clientGroupDetail']['tiPlan']['planId'] = plan_id


        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENTGROUP, request_json
        )

        if flag:
            response_json = response.json()
            if 'error' in response_json:
                error_code = response_json['error']['errorCode']
                if error_code != 0:
                    error_message = response_json['error']['errorMessage']
                    raise SDKException('ResourceGroup', '102', error_message)
        else:
            response_json = response.json()
            if 'error' in response_json:
                error_code = response_json['error']['errorCode']
                if error_code != 0:
                    error_message = response_json['error']['errorMessage']
                    raise SDKException('ResourceGroup', '102', error_message)

            else:
                raise SDKException('Response', '102', 'Invalid response received from server')

    def update_manual_associations(self, clients: list) -> None:
        """Updates the client associations for the resource group.

        Args:
            clients (list): List of client names to associate with the resource group.

        Returns:
            None

        Raises:
            SDKException:
                if type of clients is not of type list

                if response is empty

                if response is not success

        Example:
        
            >>> rg = resource_groups.get('resource_group_1')
            >>> rg.update_manual_associations(['client1', 'client2'])
        """
        if not isinstance(clients, list):
            raise SDKException('ResourceGroup', '101')

        # Build the request JSON
        request_json = copy.deepcopy(RESOURCE_GROUP_PAYLOAD_MANUAL_UPDATE)
        request_json['serverGroup']['id'] = int(self._resource_group_id)
        request_json['serverGroup']['name'] = self._resource_group_name

        # Add each client to the associatedservers list
        for client in clients:
            client = str(client)
            request_json['manualAssociation']['associatedservers'].append(
                {"id": int(self._commcell_object.clients.get(client).client_id)}
            )

        # Get the ServerGroup API endpoint
        servergroup_url = self._commcell_object._services['SERVERGROUPS_V4'] + f"/{self._resource_group_id}"

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', servergroup_url, request_json
        )

        if flag:
            response_json = response.json()
            if 'errorCode' in response_json:
                error_code = response_json['errorCode']
                if error_code != 0:
                    error_message = response_json['errorMessage']
                    raise SDKException('ResourceGroup', '102', error_message)
                return
            raise SDKException('Response', '102', 'Failed to update client association to resource group')
        raise SDKException('Response', '101', self._update_response_(response.text))


