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

"""Main file for performing client group operations.

ClientGroups and ClientGroup are the classes defined in this file.

ClientGroups: Class for representing all the client groups associated with a commcell

ClientGroup:  Class for representing a single Client Group of the commcell

ClientGroups:
=============

    __init__(commcell_object)  -- initialise instance of the ClientGroups associated with
    the specified commcell

    __str__()                  -- returns all the client groups associated with the Commcell

    __repr__()                 -- returns the string for the instance of the ClientGroups class

    __len__()                  -- returns the number of client groups associated with the Commcell

    __getitem__()              -- returns the name of the client group for the given client group
    Id or the details for the given client group name

    _get_clientgroups()        -- gets all the clientgroups associated with the commcell specified

    _valid_clients()           -- returns the list of all the valid clients,
    from the list of clients provided

    _get_fl_paramters()        -- Returns the fl parameters to be passed in the mongodb caching api call

    _get_sort_parameters()     -- Returns the sort parameters to be passed in the mongodb caching api call

    _get_fq_parameters()       -- Returns the fq parameters based on the fq list passed

    get_client_groups_cache()  -- Gets all the client groups present in CommcellEntityCache DB.


    has_clientgroup()          -- checks if a client group exists with the given name or not

    create_smart_rule()        -- Create rules required for smart client group creation
    based on input parameters

    merge_smart_rules()        -- Merge multiple rules into (SCG) rule to create smart client group

    _create_scope_dict()       -- Creates Scope Dictionary needed for Smart Client group association

    add(clientgroup_name)      -- adds a new client group to the commcell

    get(clientgroup_name)      -- returns the instance of the ClientGroup class,
    for the the input client group name

    delete(clientgroup_name)   -- deletes the client group from the commcell

    refresh()                  -- refresh the client groups associated with the commcell

ClientGroups Attributes
-----------------------

    **all_clientgroups**         -- returns the dict of all the clientgroups on the commcell

    **all_clientgroups_cache**   -- Returns dict of all the client groups and their info present in
    CommcellEntityCache in mongoDB

    **all_client_groups_prop**   -- Returns complete GET API response

ClientGroup:
============

    __init__(commcell_object,
             clientgroup_name,
             clientgroup_id=None)  -- initialise object of ClientGroup class with the specified
    client group name and id

    __repr__()                     -- return the client group name, the instance is associated with

    _get_clientgroup_id()          -- method to get the clientgroup id, if not specified

    _get_clientgroup_properties()  -- get the properties of this clientgroup

    _initialize_clientgroup_properties() --  initializes the properties of this ClientGroup

    _request_json_()               -- returns the appropriate JSON to pass for enabling/disabling
    an activity

    _process_update_request()      -- processes the clientgroup update API call

    _update()                      -- updates the client group properties

    _add_or_remove_clients()       -- adds/removes clients to/from a ClientGroup

    enable_backup_at_time()        -- enables backup for the client group at the time specified

    enable_backup()                -- enables the backup flag

    disable_backup()               -- disables the backup flag

    enable_restore_at_time()       -- enables restore for the client group at the time specified

    enable_restore()               -- enables the restore flag

    disable_restore()              -- disables the restore flag

    enable_data_aging_at_time()    -- enables data aging for the client group at the time specified

    enable_data_aging()            -- enables the data aging flag

    disable_data_aging()           -- disables the data aging flag

    add_clients()                  -- adds the valid clients to client group

    remove_clients()               -- removes the valid clients from client group

    remove_all_clients()           -- removes all the associated clients from client group

    network()                      -- returns Network class object

    push_network_config()          -- performs a push network configuration on client group

    refresh()                      -- refresh the properties of the client group

    push_servicepack_and_hotfixes() -- triggers installation of service pack and hotfixes

    repair_software()               -- triggers Repair software on the client group

    update_properties()             -- to update the client group properties

    add_additional_setting()        -- adds registry key to client group property

    delete_additional_setting()     -- Delete registry key from client group property

    is_auto_discover_enabled()      -- gets the autodiscover option for the Organization

    enable_auto_discover()          -- enables  autodiscover option at client group level

    disable_auto_discover()         -- disables  autodiscover option at client group level

    refresh_clients()               -- force refreshes clients in a client group

    add_http_proxy()                -- adds http proxy settings to client group

    remove_http_proxy()             -- removes http proxy settings from client group

ClientGroup Attributes
-----------------------

    Following attributes are available for an instance of the ClientGroup class:

        **name**                       --      returns the name of client group
        
        **clientgroup_id**             --      returns the id of client group
        
        **clientgroup_name**           --      returns the name of client group
        
        **description**                --      returns the description of client group
        
        **associated_clients**         --      returns the associated clients of client group
        
        **is_backup_enabled**          --      returns the backup activity status of client group
        
        **is_restore_enabled**         --      returns the restore activity status of client group
        
        **is_data_aging_enabled**      --      returns the data aging activity status of client group
        
        **is_smart_client_group**      --      returns true if client group is a smart client group
        
        **is_auto_discover_enabled**   --      returns the auto discover status of client group
        
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import time
import copy
from typing import Dict, List, Optional, Union

from .additional_settings import AdditionalSettings
from .exception import SDKException
from .network import Network
from .network_throttle import NetworkThrottle
from .deployment.install import Install
from .job import Job


class ClientGroups(object):
    """
    Manages all client groups associated with a Commcell.

    The ClientGroups class provides a comprehensive interface for interacting with client groups
    within a Commcell environment. It supports operations such as adding, retrieving, deleting,
    and refreshing client groups, as well as advanced management features like smart rule creation
    and merging, client validation, and caching mechanisms.

    Key Features:
        - Add new client groups with specified clients
        - Retrieve client group details by name
        - Delete existing client groups
        - Refresh the client group list from the Commcell
        - Access all client groups and cached client groups via properties
        - Check for the existence of a client group by name
        - Create and merge smart rules for dynamic client group management
        - Validate clients and manage filtering, sorting, and query parameters
        - Internal utilities for scope and parameter management

    This class is intended to be used as part of the Commcell management suite, providing
    efficient and flexible client group operations.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a new instance of the ClientGroups class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> client_groups = ClientGroups(commcell)
            >>> print("ClientGroups object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._CLIENTGROUPS = self._commcell_object._services['CLIENTGROUPS']

        self._clientgroups = None
        self._clientgroups_cache = None
        self._all_client_groups_prop = None
        self.filter_query_count = 0
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all client groups in the Commcell.

        This method provides a human-readable summary of all client groups managed by the Commcell,
        typically listing their names or key details in a single string.

        Returns:
            A string containing information about all client groups in the Commcell.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> print(str(client_groups))
            ClientGroup1, ClientGroup2, ClientGroup3
        #ai-gen-doc
        """
        representation_string = "{:^5}\t{:^50}\n\n".format('S. No.', 'ClientGroup')

        for index, clientgroup_name in enumerate(self._clientgroups):
            sub_str = '{:^5}\t{:50}\n'.format(index + 1, clientgroup_name)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return a string representation of the ClientGroups instance.

        This method provides a human-readable summary of all client groups 
        associated with the Commcell, which is useful for debugging and logging.

        Returns:
            A string listing all client groups associated with the Commcell.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> print(repr(client_groups))
            >>> # Output: "<ClientGroups: [Group1, Group2, Group3]>"

        #ai-gen-doc
        """
        return "ClientGroups class instance for Commcell"

    def __len__(self) -> int:
        """Return the number of client groups associated with the Commcell.

        Returns:
            The total count of client groups as an integer.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> num_groups = len(client_groups)
            >>> print(f"Total client groups: {num_groups}")
        #ai-gen-doc
        """
        return len(self.all_clientgroups)

    def __getitem__(self, value: Union[str, int]) -> Union[str, dict]:
        """Retrieve client group information by name or ID.

        If a client group ID (int) is provided, returns the name of the client group.
        If a client group name (str) is provided, returns a dictionary with details of the client group.

        Args:
            value: The name (str) or ID (int) of the client group to retrieve.

        Returns:
            str: The name of the client group if an ID was provided.
            dict: A dictionary containing details of the client group if a name was provided.

        Raises:
            IndexError: If no client group exists with the given name or ID.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> # Get client group details by name
            >>> group_details = client_groups["Finance"]
            >>> print(group_details)
            {'clientGroupId': 5, 'clientGroupName': 'Finance', ...}

            >>> # Get client group name by ID
            >>> group_name = client_groups[5]
            >>> print(group_name)
            'Finance'

        #ai-gen-doc
        """
        value = str(value)

        if value in self.all_clientgroups:
            return self.all_clientgroups[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_clientgroups.items())
                )[0][0]
            except IndexError:
                raise IndexError('No client group exists with the given Name / Id')

    def _get_clientgroups(self, full_response: bool = False) -> dict:
        """Retrieve all client groups associated with the Commcell.

        Args:
            full_response: If True, returns the complete response from the Commcell API. 
                If False, returns a simplified dictionary mapping client group names to their IDs.

        Returns:
            dict: A dictionary containing all client groups of the Commcell. 
            The keys are client group names, and the values are their corresponding IDs.
            Example:
                {
                    "clientgroup1_name": clientgroup1_id,
                    "clientgroup2_name": clientgroup2_id,
                }

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> client_groups = client_groups_obj._get_clientgroups()
            >>> print(client_groups)
            {'Finance_Group': 101, 'IT_Group': 102}
            >>> # To get the full response:
            >>> full_resp = client_groups_obj._get_clientgroups(full_response=True)
            >>> print(full_resp)

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._CLIENTGROUPS
        )

        if flag:
            if response.json() and 'groups' in response.json():
                if full_response:
                    return response.json()
                clientgroups_dict = {}

                name_count = {}

                for client_group in response.json()['groups']:
                    temp_name = client_group['name'].lower()
                    temp_company = \
                        client_group.get('clientGroup', {}).get('entityInfo', {}).get('companyName', '').lower()

                    if temp_name in name_count:
                        name_count[temp_name].add(temp_company)
                    else:
                        name_count[temp_name] = {temp_company}

                for client_group in response.json()['groups']:
                    temp_name = client_group['name'].lower()
                    temp_id = str(client_group['Id']).lower()
                    temp_company = \
                        client_group.get('clientGroup', {}).get('entityInfo', {}).get('companyName', '').lower()

                    if len(name_count[temp_name]) > 1:
                        unique_key = f"{temp_name}_({temp_company})"
                    else:
                        unique_key = temp_name

                    clientgroups_dict[unique_key] = temp_id

                return clientgroups_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _valid_clients(self, clients_list: list) -> list:
        """Filter and return only the valid clients from the provided clients list.

        Args:
            clients_list: List of client names or client objects to be added to the client group.

        Returns:
            A list containing the names of all valid clients found in the input clients_list.

        Raises:
            SDKException: If the clients_list argument is not of type list.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> input_clients = ['client1', 'client2', 'invalid_client']
            >>> valid_clients = client_groups._valid_clients(input_clients)
            >>> print(valid_clients)
            ['client1', 'client2']

        #ai-gen-doc
        """
        if not isinstance(clients_list, list):
            raise SDKException('ClientGroup', '101')

        clients = []

        for client in clients_list:
            if isinstance(client, str):
                client = client.strip().lower()

                if self._commcell_object.clients.has_client(client):
                    clients.append(client)

        return clients

    def _get_fl_parameters(self, fl: Optional[list] = None) -> str:
        """Generate the 'fl' parameter string for use in MongoDB caching API calls.

        Args:
            fl: Optional list of column names to include in the API request. If None, a default set of columns may be used.

        Returns:
            A string representing the 'fl' parameter to be passed in the MongoDB caching API call.

        Example:
            >>> client_groups = ClientGroups()
            >>> fl_param = client_groups._get_fl_parameters(['name', 'status', 'id'])
            >>> print(fl_param)
            name,status,id

        #ai-gen-doc
        """
        self.valid_columns = {
            'name': 'name',
            'id': 'groups.Id',
            'association': 'groups.groupAssocType',
            'companyName': 'groups.clientGroup.entityInfo.companyName',
            'tags': 'tags'
        }
        default_columns = 'name'

        if fl:
            if all(col in self.valid_columns for col in fl):
                fl_parameters = f"&fl={default_columns},{','.join(self.valid_columns[column] for column in fl)}"
            else:
                raise SDKException('ClientGroup', '102', 'Invalid column name passed')
        else:
            fl_parameters = "&fl=groups.clientGroup,groups.discoverRulesInfo,groups.groupAssocType,groups.Id," \
                            "groups.name,groups.isCompanySmartClientGroup"

        return fl_parameters

    def _get_sort_parameters(self, sort: Optional[list] = None) -> str:
        """Generate the sort parameter string for use in MongoDB caching API calls.

        Args:
            sort: Optional list containing the column name and sort order.
                The list should have two elements:
                    - The first element is the column name to sort by (str).
                    - The second element is the sort type: 1 for ascending, -1 for descending (int or str).
                Example: ['name', '1']

        Returns:
            A string representing the sort parameters to be used in the API call.

        Example:
            >>> client_groups = ClientGroups()
            >>> sort_param = client_groups._get_sort_parameters(['name', '1'])
            >>> print(sort_param)
            "name:1"
            >>> # This string can be passed to the MongoDB caching API for sorting results

        #ai-gen-doc
        """
        sort_type = str(sort[1])
        col = sort[0]
        if col in self.valid_columns.keys() and sort_type in ['1', '-1']:
            sort_parameter = '&sort=' + self.valid_columns[col] + ':' + sort_type
        else:
            raise SDKException('ClientGroup', '102', 'Invalid column name passed')
        return sort_parameter

    def _get_fq_parameters(self, fq: Optional[list] = None) -> str:
        """Generate the FQ (filter query) parameter string from the provided list.

        Args:
            fq: Optional list of filter conditions, where each element is a list containing
                [columnName, condition, value]. For example:
                [['name', 'contains', 'test'], ['association', 'eq', 'Manual']]

        Returns:
            A string representing the FQ parameters suitable for use in API queries.

        Example:
            >>> fq_list = [['name', 'contains', 'test'], ['association', 'eq', 'Manual']]
            >>> fq_param = client_groups._get_fq_parameters(fq_list)
            >>> print(fq_param)
            # Output might be: "name:contains:test;association:eq:Manual"

        #ai-gen-doc
        """
        conditions = {"contains", "notContain", "eq", "neq"}
        params = [
            "&fq=groups.isCompanySmartClientGroup:eq:false",
            "&fq=groups.clientGroup.clientGroupName:neq:Index Servers"
        ]

        for column, condition, *value in fq or []:
            if column not in self.valid_columns:
                raise SDKException('ClientGroup', '102', 'Invalid column name passed')

            # Handle 'tags' column separately
            if column == "tags" and condition == "contains":
                params.append(f"&tags={value[0]}")
            elif condition in conditions:
                params.append(f"&fq={self.valid_columns[column]}:{condition.lower()}:{value[0]}")
            elif condition == "isEmpty" and not value:
                params.append(f"&fq={self.valid_columns[column]}:in:null,")
            else:
                raise SDKException('ClientGroup', '102', 'Invalid condition passed')

        return "".join(params)

    def get_client_groups_cache(self, hard: bool = False, **kwargs: dict) -> dict:
        """Retrieve all client groups from the CommcellEntityCache database.

        This method fetches client group information from the CommcellEntityCache DB, with options to customize
        the returned data using various filters and parameters.

        Args:
            hard: If True, performs a hard refresh on the client groups cache to ensure the latest data is retrieved.
            **kwargs: Optional keyword arguments to refine the query:
                - fl (list): List of column names to include in the response (default: None).
                - sort (list): Specifies sorting as ['columnName', '1'] for ascending or ['columnName', '-1'] for descending (default: None).
                - limit (list): Specifies the start and limit for pagination, e.g., ['0', '100'] (default: ['0', '100']).
                - search (str): String to search within the commcell entity cache (default: None).
                - fq (list): List of filters, each as [columnName, condition, value], e.g., [['name', 'contains', 'test']] (default: None).

        Returns:
            dict: A dictionary containing the properties and details of all client groups matching the query.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> # Retrieve all client groups with default settings
            >>> groups = client_groups.get_client_groups_cache()
            >>> print(groups)
            >>> # Retrieve client groups with specific columns and a search filter
            >>> groups_filtered = client_groups.get_client_groups_cache(
            ...     fl=['name', 'description'],
            ...     search='production'
            ... )
            >>> print(groups_filtered)

        #ai-gen-doc
        """
        # computing params
        fl_parameters = self._get_fl_parameters(kwargs.get('fl', None))
        fq_parameters = self._get_fq_parameters(kwargs.get('fq', None))
        limit = kwargs.get('limit', None)
        limit_parameters = f'start={limit[0]}&limit={limit[1]}' if limit else ''
        hard_refresh = '&hardRefresh=true' if hard else ''
        sort_parameters = self._get_sort_parameters(kwargs.get('sort', None)) if kwargs.get('sort', None) else ''

        # Search operation can only be performed on limited columns, so filtering out the columns on which search works
        searchable_columns = ["name","association",'companyName']
        search_parameter = (f'&search={",".join(self.valid_columns[col] for col in searchable_columns)}:contains:'
                            f'{kwargs.get("search", None)}') if kwargs.get('search', None) else ''

        params = [
            limit_parameters,
            sort_parameters,
            fl_parameters,
            hard_refresh,
            search_parameter,
            fq_parameters
        ]
        request_url = f"{self._CLIENTGROUPS}?" + "".join(params)
        flag, response = self._commcell_object._cvpysdk_object.make_request("GET", request_url)
        if not flag:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        client_group_cache = {}
        if response.json() and 'groups' in response.json():
            self.filter_query_count = response.json().get('filterQueryCount', 0)
            for group in response.json()['groups']:
                name = group.get('name')
                company_name = None
                client_group_config = {
                    'name': name,
                    'id': group.get('Id'),
                    'association': group.get('groupAssocType'),
                }
                if 'clientGroup' in group:
                    if 'companyName' in group.get('clientGroup', {}).get('entityInfo', {}):
                        company_name = group.get('clientGroup', {}).get('entityInfo', {}).get('companyName')
                        client_group_config['companyName'] = company_name
                    if 'tags' in group.get('clientGroup', {}):
                        client_group_config['tags'] = group.get('clientGroup', {}).get('tags')

                # Ensure unique key
                unique_name = name
                if name in client_group_cache and company_name:
                    unique_name = f"{name}_{company_name}"

                client_group_cache[unique_name] = client_group_config

            return client_group_cache
        else:
            raise SDKException('Response', '102')

    @property
    def all_clientgroups(self) -> Dict[str, int]:
        """Get a dictionary of all client groups associated with this Commcell.

        Returns:
            Dict[str, int]: A dictionary mapping client group names to their corresponding IDs.
                Example format:
                    {
                        "clientgroup1_name": 123,
                        "clientgroup2_name": 456,
                    }

        Example:
            >>> client_groups = client_groups_obj.all_clientgroups
            >>> print(client_groups)
            {'Finance_Group': 101, 'HR_Group': 102}
            >>> # Access a specific client group ID
            >>> finance_id = client_groups['Finance_Group']
            >>> print(f"Finance group ID: {finance_id}")

        #ai-gen-doc
        """
        return self._clientgroups

    @property
    def all_clientgroups_cache(self) -> dict:
        """Get a dictionary of all client groups and their information from the CommcellEntityCache in MongoDB.

        The returned dictionary contains the names of all client groups as keys, with each value being a dictionary
        of details for that client group, including its ID, association type, company, and tags.

        Returns:
            dict: A dictionary where each key is a client group name and the value is a dictionary with the following structure:
                {
                    "id": <clientgroup_id>,
                    "association": <association_type>,
                    "company": <company_name>,
                    "tags": <tags>
                }

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> all_groups = client_groups.all_clientgroups_cache
            >>> for group_name, group_info in all_groups.items():
            ...     print(f"Group: {group_name}, ID: {group_info['id']}, Company: {group_info['company']}")

        #ai-gen-doc
        """
        if not self._clientgroups_cache:
            self._clientgroups_cache = self.get_client_groups_cache()
        return self._clientgroups_cache

    def has_clientgroup(self, clientgroup_name: str) -> bool:
        """Check if a client group with the specified name exists in the Commcell.

        Args:
            clientgroup_name: The name of the client group to check for existence.

        Returns:
            True if the client group exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the clientgroup_name argument is not a string.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> exists = client_groups.has_clientgroup("DatabaseAdmins")
            >>> print(f"Client group exists: {exists}")
            # Output: Client group exists: True

        #ai-gen-doc
        """
        if not isinstance(clientgroup_name, str):
            raise SDKException('ClientGroup', '101')

        return self._clientgroups and clientgroup_name.lower() in self._clientgroups

    def create_smart_rule(self,
                          filter_rule: str = 'OS Type',
                          filter_condition: str = 'equal to',
                          filter_value: str = 'Windows',
                          value: str = '1') -> dict:
        """Create a smart rule dictionary for client group creation based on specified filter parameters.

        This method prepares a rule definition used for smart client group creation, allowing you to specify
        the rule type, condition, value, and additional parameters. The returned dictionary can be used
        when creating or updating smart client groups.

        Args:
            filter_rule: The rule selection criterion (e.g., 'OS Type').
            filter_condition: The filter condition to apply (e.g., 'equal to').
            filter_value: The value to match for the rule criterion (e.g., 'Windows').
            value: The value required to create the rule (typically a string representation of a number).

        Returns:
            dict: A dictionary representing the smart rule, structured as:
                {
                    "rule": {
                        "filterID": 100,
                        "secValue": "Windows",
                        "propID": 8,
                        "propType": 4,
                        "value": "1"
                    }
                }

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> rule = client_groups.create_smart_rule(
            ...     filter_rule='OS Type',
            ...     filter_condition='equal to',
            ...     filter_value='Windows',
            ...     value='1'
            ... )
            >>> print(rule)
            {'rule': {'filterID': 100, 'secValue': 'Windows', 'propID': 8, 'propType': 4, 'value': '1'}}

        #ai-gen-doc
        """

        filter_dict = {
            'equal to': 100,
            'not equal': 101,
            'any in selection': 108,
            'not in selection': 109,
            'is true': 1,
            'is false': 2,
            'contains': 10,
            'starts with': 14,
            'ends with': 15,
            'does not contain': 11,
            }
        prop_id_dict = {
            'Name': 1,
            'Client': 2,
            'Agents Installed': 3,
            'Associated Client Group': 4,
            'Timezone': 5,
            'Hostname': 6,
            'Client Version': 7,
            'OS Type': 8,
            'Package Installed': 9,
            'Client offline (days)': 10,
            'User as client owner': 11,
            'Local user group as client owner': 12,
            'External group as client owner': 13,
            'Associated library name': 14,
            'OS Version': 15,
            'Product Version': 16,
            'Client Version Same as CS Version': 17,
            'Days since client created': 18,
            'Days since last backup': 19,
            'SnapBackup clients': 20,
            'Clients with attached storages': 21,
            'Case manager hold clients': 22,
            'MediaAgents for clients in group': 23,
            'Client acts as proxy': 24,
            'Backup activity enabled': 25,
            'Restore activity enabled': 26,
            'Client online (days)': 27,
            'Inactive AD user as client owner': 28,
            'Client excluded from SLA report': 29,
            'Client uses storage policy': 30,
            'Client is not ready': 31,
            'Associated Storage Policy': 32,
            'MediaAgent has Lucene Index Roles': 33,
            'Client associated with plan': 34,
            'Client by Schedule Interval': 35,
            'Client needs Updates': 36,
            'Subclient Name': 37,
            'CommCell Psuedo Client': 38,
            'Client Description': 39,
            'Clients discovered using VSA Subclient': 40,
            'Clients with no Archive Data': 41,
            'User Client Provider Associations': 42,
            'User Group Client Provider Associations': 43,
            'Company Client Provider Associations': 44,
            'Clients Meet SLA': 45,
            'Index Servers': 46,
            'Clients with OnePass enabled': 49,
            'Clients by Role': 50,
            'Clients by Permission': 51,
            'User description contains': 52,
            'User Group description contains': 53,
            'Content Analyzer Cloud': 54,
            'Company Installed Client Associations': 55,
            'Client Online in Last 30 Days': 56,
            'Clients With Subclients Having Associated Storage Policy': 60,
            'Clients With Improperly Deconfigured Subclients': 61,
            'Strikes count': 62,
            'Clients With Backup Schedule': 63,
            'Clients With Long Running Jobs': 64,
            'Clients With Synthetic Full Backup N Days': 67,
            'MediaAgents for clients in group list': 70,
            'Associated Client Group List': 71,
            'Timezone List': 72,
            'MediaAgent has Lucene Index Role List': 73,
            'Associated Storage Policy List': 74,
            'Timezone Region List': 75,
            'Clients With Encryption': 80,
            'Client CIDR Address Range': 81,
            'HAC Cluster': 85,
            'Client Display Name': 116,
            'Clients associated to any company': 158,
            'VMs not in any Subclient Content': 166,
            'Pseudo Clients': 115,
            }
        ptype_dict = {
            'Name': 2,
            'Client': 4,
            'Agents Installed': 6,
            'Associated Client Group': 4,
            'Timezone': 4,
            'Hostname': 2,
            'Client Version': 4,
            'OS Type': 4,
            'Package Installed': 6,
            'Client offline (days)': 3,
            'User as client owner': 2,
            'Local user group as client owner': 2,
            'External group as client owner': 2,
            'Associated library name': 2,
            'OS Version': 2,
            'Product Version': 2,
            'Client Version Same as CS Version': 1,
            'Days since client created': 3,
            'Days since last backup': 3,
            'SnapBackup clients': 1,
            'Clients with attached storages': 1,
            'Case manager hold clients': 1,
            'MediaAgents for clients in group': 2,
            'Client acts as proxy': 1,
            'Backup activity enabled': 1,
            'Restore activity enabled': 1,
            'Client online (days)': 3,
            'Inactive AD user as client owner': 1,
            'Client excluded from SLA report': 1,
            'Client uses storage policy': 2,
            'Client is not ready': 1,
            'Associated Storage Policy': 4,
            'MediaAgent has Lucene Index Roles': 4,
            'Client associated with plan': 2,
            'Client by Schedule Interval': 4,
            'Client needs Updates': 1,
            'Subclient Name': 2,
            'CommCell Psuedo Client': 1,
            'Client Description': 2,
            'Clients discovered using VSA Subclient': 6,
            'Clients with no Archive Data': 1,
            'User Client Provider Associations': 2,
            'User Group Client Provider Associations': 2,
            'Company Client Provider Associations': 4,
            'Clients Meet SLA': 4,
            'Index Servers': 1,
            'Clients with OnePass enabled': 1,
            'Clients by Role': 4,
            'Clients by Permission': 4,
            'User description contains': 2,
            'User Group description contains': 2,
            'Content Analyzer Cloud': 1,
            'Company Installed Client Associations': 4,
            'Client Online in Last 30 Days': 1,
            'Clients With Subclients Having Associated Storage Policy': 1,
            'Clients With Improperly Deconfigured Subclients': 1,
            'Strikes count': 3,
            'Clients With Backup Schedule': 1,
            'Clients With Long Running Jobs': 3,
            'Clients With Synthetic Full Backup N Days': 3,
            'MediaAgents for clients in group list': 7,
            'Associated Client Group List': 7,
            'Timezone List': 7,
            'MediaAgent has Lucene Index Role List': 7,
            'Associated Storage Policy List': 7,
            'Timezone Region List': 7,
            'Clients With Encryption': 1,
            'Client CIDR Address Range': 10,
            'HAC Cluster': 1,
            'Client Display Name': 2,
            'Clients associated to any company': 1,
            'VMs not in any Subclient Content': 1,
            'Pseudo Clients': 1,
            }

        rule_mk = {
            "rule": {
                "filterID": filter_dict[filter_condition],
                "secValue": filter_value,
                "propID": prop_id_dict[filter_rule],
                "propType": ptype_dict[filter_rule],
                "value": value
            }
            }

        return rule_mk

    def merge_smart_rules(self, rule_list: list, op_value: str = 'all', scg_op: str = 'all') -> dict:
        """Merge multiple smart rules into a single rule group for creating a smart client group.

        Args:
            rule_list: List of smart rule dictionaries to be merged into a rule group.
            op_value: Logical condition to apply between individual smart rules within the group.
                Valid values include 'all', 'any', or 'not any'. Default is 'all'.
            scg_op: Logical condition to apply between smart rule groups at the group level.
                Valid values include 'all', 'any', or 'not any'. Default is 'all'.

        Returns:
            A dictionary representing the merged smart client group rule, suitable for use in smart client group creation.

        Example:
            >>> rules = [
            ...     {"type": "OS", "value": "Windows"},
            ...     {"type": "Location", "value": "DataCenter1"}
            ... ]
            >>> merged_rule = client_groups.merge_smart_rules(rules, op_value='all', scg_op='any')
            >>> print(merged_rule)
            {'op': 'any', 'rules': [{'op': 'all', 'rules': [{'type': 'OS', 'value': 'Windows'}, {'type': 'Location', 'value': 'DataCenter1'}]}]}

        #ai-gen-doc
        """

        op_dict = {
            'all': 0,
            'any': 1,
            'not any': 2
        }
        scg_rule = {
            "op": op_dict[scg_op],
            "rules": [
            ]
        }
        rules_dict = {
            "rule": {
                "op": op_dict[op_value],
                "rules": [
                ]
            }
        }

        for each_rule in rule_list:
            rules_dict["rule"]["rules"].append(each_rule)

        scg_rule["rules"].append(rules_dict)
        return scg_rule

    def _create_scope_dict(self, client_scope: str, value: str = None) -> dict:
        """Create a dictionary representing the client scope for a smart client group.

        This method constructs a dictionary with the necessary data for the specified client scope,
        which is used when configuring smart client groups.

        Args:
            client_scope: The type of client scope to use. Accepted values include:
                - "Clients in this Commcell"
                - "Clients of Companies"
                - "Clients of User"
                - "Clients of User Groups"
            value: The value to select for the client scope dropdown. This is required for all
                client scopes except "Clients in this Commcell", where the value is automatically
                set to the CommServe name.

        Returns:
            dict: A dictionary containing the client scope data required for the smart client group.

        Example:
            >>> client_groups = ClientGroups()
            >>> scope_dict = client_groups._create_scope_dict("Clients of Companies", value="CompanyA")
            >>> print(scope_dict)
            {'clientScope': 'Clients of Companies', 'value': 'CompanyA'}

            >>> # For "Clients in this Commcell", value is set automatically
            >>> scope_dict = client_groups._create_scope_dict("Clients in this Commcell")
            >>> print(scope_dict)
            {'clientScope': 'Clients in this Commcell', 'value': 'CommServeName'}

        Note:
            The 'value' parameter is not required when client_scope is "Clients in this Commcell".
            In this case, the value is automatically set to the CommServe name.

        #ai-gen-doc
        """
        scgscope = {
            "entity": {}
        }
        if client_scope.lower() == 'clients in this commcell':
            scgscope["entity"] = {
                "commCellName": self._commcell_object.commserv_name,
                "_type_": 1
            }
        elif client_scope.lower() == 'clients of companies' and value is not None:
            scgscope["entity"] = {
                "providerDomainName": value,
                "_type_": 61
            }
        elif client_scope.lower() == 'clients of user' and value is not None:
            scgscope["entity"] = {
                "userName": value,
                "_type_": 13
            }
        elif client_scope.lower() == 'clients of user group' and value is not None:
            scgscope["entity"] = {
                "userGroupName": value,
                "_type_": 15
            }
        return scgscope

    def add(self, clientgroup_name: str, clients: list = [], **kwargs) -> 'ClientGroup':
        """Add a new Client Group to the Commcell.

        Creates a new client group with the specified name and adds the provided clients to it.
        Additional configuration options can be set using keyword arguments.

        Args:
            clientgroup_name: The name of the new client group to add.
            clients: A list of client names or a comma-separated string of client names to be added to the group.
                Defaults to an empty list.
            **kwargs: Optional keyword arguments for additional configuration. Supported keys include:
                - clientgroup_description (str): Description of the client group. Default is "".
                - enable_backup (bool): Enable or disable backup. Default is True.
                - enable_restore (bool): Enable or disable restore. Default is True.
                - enable_data_aging (bool): Enable or disable data aging. Default is True.
                - scg_rule (dict): Rule required to create a smart client group.
                - client_scope (str): Client scope for the Smart Client Group.
                - client_scope_value (str): Client scope value for a particular scope.

        Returns:
            ClientGroup: An instance of the created ClientGroup.

        Raises:
            SDKException: If the client group name or description is not a string,
                if the clients argument is not a list or string,
                if the response is empty or unsuccessful,
                or if a client group with the given name already exists.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> new_group = client_groups.add(
            ...     clientgroup_name="FinanceDept",
            ...     clients=["client1", "client2"],
            ...     clientgroup_description="Finance department servers",
            ...     enable_backup=True
            ... )
            >>> print(f"Created client group: {new_group}")

        #ai-gen-doc
        """
        if not (isinstance(clientgroup_name, str) and
                isinstance(kwargs.get('clientgroup_description', ''), str)):
            raise SDKException('ClientGroup', '101')

        if not self.has_clientgroup(clientgroup_name):
            if isinstance(clients, list):
                clients = self._valid_clients(clients)
            elif isinstance(clients, str):
                clients = self._valid_clients(clients.split(','))
            else:
                raise SDKException('ClientGroup', '101')

            clients_list = []

            for client in clients:
                clients_list.append({'clientName': client})

            smart_client_group = bool(kwargs.get('scg_rule'))
            if kwargs.get('scg_rule') is None:
                kwargs['scg_rule'] = {}

            request_json = {
                "clientGroupOperationType": 1,
                "clientGroupDetail": {
                    "description": kwargs.get('clientgroup_description', ''),
                    "isSmartClientGroup": smart_client_group,
                    "scgRule": kwargs.get('scg_rule'),
                    "clientGroup": {
                        "clientGroupName": clientgroup_name
                    },
                    "associatedClients": clients_list
                }
            }

            scg_scope = None
            if kwargs.get("client_scope") is not None:
                # Check if value is there or not
                if kwargs.get("client_scope").lower() == "clients in this commcell":
                    scg_scope = [self._create_scope_dict(kwargs.get("client_scope"))]
                else:
                    if kwargs.get("client_scope_value") is not None:
                        scg_scope = [self._create_scope_dict(kwargs.get("client_scope"), kwargs.get("client_scope_value"))]
                    else:
                        raise SDKException('ClientGroup', '102',
                                           "Client Scope {0} requires a value".format(kwargs.get("client_scope")))

            if scg_scope is not None:
                request_json["clientGroupDetail"]["scgScope"] = scg_scope

            if kwargs.get("enable_backup") or kwargs.get("enable_data_aging") or kwargs.get("enable_restore"):
                client_group_activity_control = {
                        "activityControlOptions": [
                            {
                                "activityType": 1,
                                "enableAfterADelay": False,
                                "enableActivityType": kwargs.get('enable_backup', True)
                            }, {
                                "activityType": 16,
                                "enableAfterADelay": False,
                                "enableActivityType": kwargs.get('enable_data_aging', True)
                            }, {
                                "activityType": 2,
                                "enableAfterADelay": False,
                                "enableActivityType": kwargs.get('enable_restore', True)
                            }
                        ]
                    }
                request_json["clientGroupDetail"]["clientGroupActivityControl"] = client_group_activity_control

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._CLIENTGROUPS, request_json
            )

            if flag:
                if response.json():
                    error_message = None

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']
                        o_str = 'Failed to create new ClientGroup\nError:"{0}"'.format(
                            error_message
                        )
                        raise SDKException('ClientGroup', '102', o_str)
                    elif 'clientGroupDetail' in response.json():
                        self.refresh()
                        clientgroup_id = response.json()['clientGroupDetail'][
                            'clientGroup']['clientGroupId']

                        return ClientGroup(
                            self._commcell_object, clientgroup_name, clientgroup_id
                        )
                    else:
                        o_str = 'Failed to create new ClientGroup'
                        raise SDKException('ClientGroup', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'ClientGroup', '102', 'Client Group "{0}" already exists.'.format(clientgroup_name)
            )

    def get(self, clientgroup_name: str) -> 'ClientGroup':
        """Retrieve a ClientGroup object by its name.

        Args:
            clientgroup_name: The name of the client group to retrieve.

        Returns:
            ClientGroup: An instance of the ClientGroup class corresponding to the specified name.

        Raises:
            SDKException: If the client group name is not a string or if no client group exists with the given name.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> group = client_groups.get("Finance_Group")
            >>> print(f"Retrieved client group: {group}")

        #ai-gen-doc
        """
        if not isinstance(clientgroup_name, str):
            raise SDKException('ClientGroup', '101')
        else:
            clientgroup_name = clientgroup_name.lower()

            if self.has_clientgroup(clientgroup_name):
                return ClientGroup(
                    self._commcell_object, clientgroup_name, self._clientgroups[clientgroup_name]
                )

            raise SDKException(
                'ClientGroup',
                '102',
                'No ClientGroup exists with name: {0}'.format(clientgroup_name)
            )

    def delete(self, clientgroup_name: str) -> None:
        """Delete a client group from the Commcell.

        Removes the specified client group by name from the Commcell environment.

        Args:
            clientgroup_name: The name of the client group to delete.

        Raises:
            SDKException: If the client group name is not a string, if the response is empty,
                if the deletion fails, or if no client group exists with the given name.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> client_groups.delete("TestClientGroup")
            >>> print("Client group deleted successfully.")

        #ai-gen-doc
        """

        if not isinstance(clientgroup_name, str):
            raise SDKException('ClientGroup', '101')
        else:
            clientgroup_name = clientgroup_name.lower()

            if self.has_clientgroup(clientgroup_name):
                clientgroup_id = self._clientgroups[clientgroup_name]

                delete_clientgroup_service = self._commcell_object._services['CLIENTGROUP']

                flag, response = self._commcell_object._cvpysdk_object.make_request(
                    'DELETE', delete_clientgroup_service % clientgroup_id
                )

                if flag:
                    if response.json():
                        if 'errorCode' in response.json():
                            error_code = str(response.json()['errorCode'])
                            error_message = response.json()['errorMessage']

                            if error_code == '0':
                                # initialize the clientgroups again
                                # so the clientgroups object has all the client groups
                                self.refresh()
                            else:
                                o_str = 'Failed to delete ClientGroup\nError: "{0}"'.format(
                                    error_message
                                )
                                raise SDKException('ClientGroup', '102', o_str)
                        else:
                            raise SDKException('Response', '102')
                    else:
                        raise SDKException('Response', '102')
                else:
                    response_string = self._commcell_object._update_response_(response.text)
                    raise SDKException('Response', '101', response_string)
            else:
                raise SDKException(
                    'ClientGroup',
                    '102',
                    'No ClientGroup exists with name: "{0}"'.format(clientgroup_name)
                )

    def refresh(self, **kwargs: dict) -> None:
        """Refresh the list of client groups on this Commcell.

        This method updates the internal cache of client groups, optionally using MongoDB as the data source
        or performing a hard refresh of the cache.

        Keyword Args:
            mongodb (bool, optional): If True, fetch the client groups cache from MongoDB. Defaults to False.
            hard (bool, optional): If True, perform a hard refresh of the MongoDB cache for this entity. Defaults to False.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> client_groups.refresh()  # Standard refresh
            >>> client_groups.refresh(mongodb=True)  # Refresh using MongoDB cache
            >>> client_groups.refresh(hard=True)  # Perform a hard refresh

        #ai-gen-doc
        """
        mongodb = kwargs.get('mongodb', False)
        hard = kwargs.get('hard', False)

        self._clientgroups = self._get_clientgroups()
        if mongodb:
            self._clientgroups_cache = self.get_client_groups_cache(hard=hard)

    @property
    def all_client_groups_prop(self) -> list[dict]:
        """Get the complete GET API response for all client groups.

        Returns:
            list[dict]: A list of dictionaries containing the full API response data for all client groups.

        Example:
            >>> client_groups = ClientGroups(commcell_object)
            >>> all_groups = client_groups.all_client_groups_prop
            >>> print(f"Total client groups: {len(all_groups)}")
            >>> # Access details of the first client group
            >>> if all_groups:
            >>>     print(all_groups[0])

        #ai-gen-doc
        """
        self._all_client_groups_prop = self._get_clientgroups(full_response=True).get("groups",[])
        return self._all_client_groups_prop


class ClientGroup(object):
    """
    Manages operations and properties for a specific ClientGroup within a CommCell environment.

    The ClientGroup class provides a comprehensive interface for managing client groups, including
    configuration, client association, backup and restore operations, data aging, network settings,
    and additional settings. It allows for dynamic updates to group properties, client membership,
    and operational controls such as enabling/disabling backup, restore, and data aging features.
    The class also supports advanced features like auto-discovery, company association changes,
    network configuration pushes, and software maintenance tasks.

    Key Features:
        - Initialization and representation of client group objects
        - Retrieval and management of client group properties and IDs
        - Dynamic update of client group name, description, and associated clients
        - Add, remove, or overwrite clients in the group
        - Enable/disable backup, restore, and data aging operations (immediate or scheduled)
        - Manage network settings and throttling for the client group
        - Push network configurations, service packs, and hotfixes to clients
        - Repair client software with authentication and reboot options
        - Update client group properties and additional settings
        - Enable/disable auto-discovery for client group membership
        - Refresh client group and associated clients' information
        - Change the company association of the client group
        - Access to various properties such as name, ID, description, associated clients,
          backup/restore/data aging status, smart group status, company name, network settings,
          client group filters, and additional settings

    This class is intended for use in environments where centralized management of client groups
    is required, providing robust methods for configuration, maintenance, and operational control.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, clientgroup_name: str, clientgroup_id: str = None) -> None:
        """Initialize a ClientGroup instance.

        Args:
            commcell_object: An instance of the Commcell class representing the connected Commcell environment.
            clientgroup_name: The name of the client group to manage.
            clientgroup_id: Optional; the unique identifier of the client group. If not provided, it may be determined automatically.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> client_group = ClientGroup(commcell, 'Finance_Group')
            >>> # Optionally, specify the client group ID
            >>> client_group_with_id = ClientGroup(commcell, 'Finance_Group', clientgroup_id='12345')

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._clientgroup_name = clientgroup_name.lower()

        if clientgroup_id:
            # Use the client group id provided in the arguments
            self._clientgroup_id = str(clientgroup_id)
        else:
            # Get the id associated with this client group
            self._clientgroup_id = self._get_clientgroup_id()

        self._CLIENTGROUP = self._commcell_object._services['CLIENTGROUP'] % (self.clientgroup_id)

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._properties = None
        self._description = None
        self._is_backup_enabled = None
        self._is_restore_enabled = None
        self._is_data_aging_enabled = None
        self._is_smart_client_group = None
        self._company_name = None
        self._additional_settings = None

        self.refresh()

    def __repr__(self) -> str:
        """Return a string representation of the ClientGroup instance.

        This method provides a human-readable string that describes the current ClientGroup object,
        which is useful for debugging and logging purposes.

        Returns:
            A string containing details about this ClientGroup instance.

        Example:
            >>> group = ClientGroup(...)
            >>> print(repr(group))
            >>> # Output: <ClientGroup name='MyGroup' id=123>

        #ai-gen-doc
        """
        representation_string = 'ClientGroup class instance for ClientGroup: "{0}"'
        return representation_string.format(self.clientgroup_name)

    def _get_clientgroup_id(self) -> str:
        """Retrieve the unique identifier (ID) associated with this client group.

        Returns:
            The client group ID as a string.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> group_id = client_group._get_clientgroup_id()
            >>> print(f"Client group ID: {group_id}")

        #ai-gen-doc
        """
        clientgroups = ClientGroups(self._commcell_object)
        return clientgroups.get(self.clientgroup_name).clientgroup_id

    def _get_clientgroup_properties(self) -> dict:
        """Retrieve the properties of the current client group.

        Returns:
            dict: A dictionary containing the properties of this client group.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> properties = client_group._get_clientgroup_properties()
            >>> print(properties)
            >>> # Output will be a dictionary with client group details

        #ai-gen-doc
        """

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._CLIENTGROUP
        )

        if flag:
            if response.json() and 'clientGroupDetail' in response.json():
                return response.json()['clientGroupDetail']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_clientgroup_properties(self) -> None:
        """Initialize the common properties for the client group.

        This method sets up the default or required properties for the client group instance.
        It is typically called internally during the creation or refresh of a client group object.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group._initialize_clientgroup_properties()
            >>> # The client group properties are now initialized and ready for use

        #ai-gen-doc
        """
        clientgroup_props = self._get_clientgroup_properties()
        self._properties = clientgroup_props

        if 'clientGroupName' in clientgroup_props['clientGroup']:
            self._clientgroup_name = clientgroup_props['clientGroup']['clientGroupName'].lower()
        else:
            raise SDKException(
                'ClientGroup', '102', 'Client Group name is not specified in the response'
            )

        self._description = None

        if 'description' in clientgroup_props:
            self._description = clientgroup_props['description']

        self._associated_clients = []

        if 'associatedClients' in clientgroup_props:
            for client in clientgroup_props['associatedClients']:
                self._associated_clients.append(client['clientName'])

        self._is_smart_client_group = self._properties['isSmartClientGroup']
        self._is_backup_enabled = False
        self._is_restore_enabled = False
        self._is_data_aging_enabled = False

        if 'clientGroupActivityControl' in clientgroup_props:
            cg_activity_control = clientgroup_props['clientGroupActivityControl']

            if 'activityControlOptions' in cg_activity_control:
                for control_options in cg_activity_control['activityControlOptions']:
                    if control_options['activityType'] == 1:
                        self._is_backup_enabled = control_options['enableActivityType']
                    elif control_options['activityType'] == 2:
                        self._is_restore_enabled = control_options['enableActivityType']
                    elif control_options['activityType'] == 16:
                        self._is_data_aging_enabled = control_options['enableActivityType']

        self._company_name = clientgroup_props.get('securityAssociations', {}).get('tagWithCompany', {}).get('providerDomainName')

    def _request_json_(self, option: str, enable: bool = True, enable_time: str = None, **kwargs: dict) -> dict:
        """Generate the JSON request payload for the API based on the selected operation option.

        Args:
            option: The operation for which to generate the API request (e.g., "Backup", "Restore", "Data Aging").
            enable: Whether to enable the specified option in the request. Defaults to True.
            enable_time: Optional time (as a string) to schedule the operation. If None, the operation is immediate.
            **kwargs: Additional keyword arguments for the request. Common keys include:
                - timezone (str): The timezone to use for the operation. Use the TIMEZONES dict from constants.py.
                  For Linux CommServer, provide time in GMT timezone.

        Returns:
            dict: The JSON request dictionary to be sent to the API.

        Example:
            >>> # Generate a backup request in GMT timezone
            >>> request = client_group._request_json_(
            ...     option="Backup",
            ...     enable=True,
            ...     enable_time="2023-06-01T10:00:00",
            ...     timezone="GMT"
            ... )
            >>> print(request)
            {'operation': 'Backup', 'enable': True, 'enableTime': '2023-06-01T10:00:00', 'timezone': 'GMT'}

        #ai-gen-doc
        """
        options_dict = {
            "Backup": 1,
            "Restore": 2,
            "Data Aging": 16
        }

        request_json1 = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "clientGroupActivityControl": {
                    "activityControlOptions": [{
                        "activityType": options_dict[option],
                        "enableAfterADelay": False,
                        "enableActivityType": enable
                    }]
                },
                "clientGroup": {
                    "newName": self.name
                }
            }
        }

        request_json2 = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "clientGroupActivityControl": {
                    "activityControlOptions": [{
                        "activityType": options_dict[option],
                        "enableAfterADelay": True,
                        "enableActivityType": False,
                        "dateTime": {
                            "TimeZoneName": kwargs.get("timezone", self._commcell_object.default_timezone),
                            "timeValue": enable_time
                        }
                    }]
                },
                "clientGroup": {
                    "newName": self.name
                }
            }
        }

        if enable_time:
            return request_json2
        else:
            return request_json1

    def _process_update_request(self, request_json: dict) -> tuple[str, str]:
        """Execute the ClientGroup update API request.

        Sends the provided request JSON as a payload to update the client group, and returns
        the error code and error message from the API response.

        Args:
            request_json: Dictionary containing the request payload for the update operation.

        Returns:
            A tuple containing:
                - error_code (str): The error code received in the response.
                - error_message (str): The error message received in the response.

        Raises:
            SDKException: If the response is empty or the update operation is not successful.

        Example:
            >>> request_payload = {"clientGroupId": 123, "newName": "UpdatedGroup"}
            >>> error_code, error_message = client_group._process_update_request(request_payload)
            >>> print(f"Error code: {error_code}, Message: {error_message}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLIENTGROUP, request_json
        )

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])

                if 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']
                else:
                    error_message = ""

                self.refresh()
                return error_code, error_message
            raise SDKException('Response', '102')
        response_string = self._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _update(
            self,
            clientgroup_name: str,
            clientgroup_description: str,
            associated_clients: 'Optional[Union[str, List[str]]]' = None,
            operation_type: str = "NONE"
        ) -> None:
        """Update the properties of this client group.

        This method updates the client group with a new name, description, and optionally modifies
        the associated clients based on the specified operation type.

        Args:
            clientgroup_name: The new name to assign to the client group.
            clientgroup_description: The description for the client group.
            associated_clients: A comma-separated string of client names or a list of client names
                to be added, removed, or overwritten in the client group. If None, no client association changes are made.
            operation_type: The operation to perform on associated clients. Valid values are:
                "NONE", "OVERWRITE", "ADD", "DELETE", "CLEAR". Default is "NONE".

        Raises:
            SDKException: If the update response is empty or not successful.

        Example:
            >>> client_group = ClientGroup()
            >>> client_group._update(
            ...     clientgroup_name="NewGroupName",
            ...     clientgroup_description="Updated description",
            ...     associated_clients=["client1", "client2"],
            ...     operation_type="ADD"
            ... )
            >>> print("Client group updated successfully.")

        #ai-gen-doc
        """
        clients_list = []

        associated_clients_op_types = {
            "NONE": 0,
            "OVERWRITE": 1,
            "ADD": 2,
            "DELETE": 3,
            "CLEAR": 4
        }

        for client in associated_clients:
            clients_list.append({'clientName': client})

        request_json = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "description": clientgroup_description,
                "clientGroup": {
                    "newName": clientgroup_name
                },
                "associatedClientsOperationType": associated_clients_op_types[operation_type],
                "associatedClients": clients_list
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CLIENTGROUP, request_json
        )

        self.refresh()

        if flag:
            if response.json():

                error_message = response.json()['errorMessage']
                error_code = str(response.json()['errorCode'])

                if error_code == '0':
                    return (True, "0", "")
                else:
                    return (False, error_code, error_message)

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _add_or_remove_clients(self, clients: Union[str, list], operation_type: str) -> None:
        """Add or remove clients to or from the ClientGroup.

        This method allows you to add, overwrite, or delete clients in the client group by specifying
        the operation type and the clients to be affected. The clients parameter can be either a 
        comma-separated string of client names or a list of client names.

        Args:
            clients: A comma-separated string or a list of client names to be added, overwritten, or removed.
            operation_type: The type of operation to perform. Valid values are 'ADD', 'OVERWRITE', or 'DELETE'.

        Raises:
            SDKException: If clients is not a string or list, if no valid clients are found, or if the operation fails.

        Example:
            >>> client_group = ClientGroup()
            >>> # Add clients using a list
            >>> client_group._add_or_remove_clients(['client1', 'client2'], 'ADD')
            >>> # Remove clients using a comma-separated string
            >>> client_group._add_or_remove_clients('client3,client4', 'DELETE')

        #ai-gen-doc
        """
        if isinstance(clients, (str, list)):
            clientgroups_object = ClientGroups(self._commcell_object)

            if isinstance(clients, list):
                validated_clients_list = clientgroups_object._valid_clients(clients)
            elif isinstance(clients, str):
                validated_clients_list = clientgroups_object._valid_clients(clients.split(','))

            if operation_type in ['ADD', 'OVERWRITE']:
                for client in validated_clients_list:
                    if client in self._associated_clients:
                        validated_clients_list.remove(client)

            if not validated_clients_list:
                raise SDKException('ClientGroup', '102', 'No valid clients were found')

            output = self._update(
                clientgroup_name=self.name,
                clientgroup_description=self.description,
                associated_clients=validated_clients_list,
                operation_type=operation_type
            )

            exception_message_dict = {
                'ADD': 'Failed to add clients to the ClientGroup\nError: "{0}"',
                'OVERWRITE': 'Failed to add clients to the ClientGroup\nError: "{0}"',
                'DELETE': 'Failed to remove clients from the ClientGroup\nError: "{0}"'
            }

            if output[0]:
                return
            else:
                o_str = exception_message_dict[operation_type]
                raise SDKException('ClientGroup', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'ClientGroup', '102', 'Client\'s name should be a list or string value'
            )

    @property
    def properties(self) -> dict:
        """Get the properties of the client group.

        Returns:
            dict: A dictionary containing the properties and configuration details of the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> group_props = client_group.properties
            >>> print(group_props)
            {'clientGroupId': 123, 'clientGroupName': 'MyClientGroup', ...}

        #ai-gen-doc
        """
        return copy.deepcopy(self._properties)

    @property
    def name(self) -> str:
        """Get the display name of the client group.

        Returns:
            The display name of the client group as a string.

        Example:
            >>> client_group = ClientGroup(commcell_object, group_id)
            >>> group_name = client_group.name  # Use dot notation for property access
            >>> print(f"Client group name: {group_name}")

        #ai-gen-doc
        """
        return self._properties['clientGroup']['clientGroupName']

    @property
    def clientgroup_id(self) -> int:
        """Get the unique identifier (ID) of the client group.

        This property provides read-only access to the client group's ID.

        Returns:
            int: The unique ID of the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> group_id = client_group.clientgroup_id
            >>> print(f"Client group ID: {group_id}")

        #ai-gen-doc
        """
        return self._clientgroup_id

    @property
    def clientgroup_name(self) -> str:
        """Get the name of the client group as a read-only property.

        Returns:
            The name of the client group as a string.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'WebServers')
            >>> name = client_group.clientgroup_name  # Access the client group name
            >>> print(f"Client group name: {name}")

        #ai-gen-doc
        """
        return self._clientgroup_name

    @property
    def description(self) -> str:
        """Get the description of the client group as a read-only property.

        Returns:
            The description of the client group as a string.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> desc = client_group.description  # Access the description property
            >>> print(f"Client group description: {desc}")

        #ai-gen-doc
        """
        return self._description

    @property
    def associated_clients(self) -> List[str]:
        """Get the list of clients associated with this ClientGroup as a read-only property.

        Returns:
            List of client names that are members of the ClientGroup.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'Finance_Group')
            >>> clients = client_group.associated_clients  # Access as a property
            >>> for client in clients:
            ...     print(f"Client name: {client}")

        #ai-gen-doc
        """
        return self._associated_clients

    @property
    def is_backup_enabled(self) -> bool:
        """Indicate whether backup is enabled for this client group.

        Returns:
            True if backup is enabled for the client group, False otherwise.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> if client_group.is_backup_enabled:
            ...     print("Backup is enabled for this client group.")
            ... else:
            ...     print("Backup is not enabled for this client group.")

        #ai-gen-doc
        """
        return self._is_backup_enabled

    @property
    def is_restore_enabled(self) -> bool:
        """Indicate whether restore operations are enabled for this client group.

        Returns:
            True if restore is enabled for the client group, False otherwise.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> if client_group.is_restore_enabled:
            ...     print("Restore is enabled for this client group.")
            ... else:
            ...     print("Restore is not enabled for this client group.")

        #ai-gen-doc
        """
        return self._is_restore_enabled

    @property
    def is_data_aging_enabled(self) -> bool:
        """Indicate whether data aging is enabled for this client group.

        Returns:
            bool: True if data aging is enabled for the client group, False otherwise.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> if client_group.is_data_aging_enabled:
            ...     print("Data aging is enabled for this client group.")
            ... else:
            ...     print("Data aging is not enabled for this client group.")

        #ai-gen-doc
        """
        return self._is_data_aging_enabled

    @property
    def is_smart_client_group(self) -> bool:
        """Check if the client group is a smart client group.

        Returns:
            True if the client group is a smart client group, False otherwise.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> if client_group.is_smart_client_group:
            ...     print("This is a smart client group.")
            ... else:
            ...     print("This is a regular client group.")

        #ai-gen-doc
        """
        return self._is_smart_client_group

    @property
    def company_name(self) -> str:
        """Get the name of the company to which this client group belongs.

        Returns:
            The company name as a string.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> company = client_group.company_name
            >>> print(f"Client group belongs to company: {company}")

        #ai-gen-doc
        """
        return self._company_name
    
    @property
    def network(self) -> 'Network':
        """Get the Network object associated with this ClientGroup.

        Returns:
            Network: An instance of the Network class for managing network-related configurations of the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> network_obj = client_group.network  # Access the Network property
            >>> print(f"Network object: {network_obj}")

        #ai-gen-doc
        """
        if self._networkprop is None:
            self._networkprop = Network(self)

        return self._networkprop

    @property
    def network_throttle(self) -> 'NetworkThrottle':
        """Get the NetworkThrottle object associated with this ClientGroup.

        Returns:
            NetworkThrottle: An instance for managing network throttling settings for the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> throttle = client_group.network_throttle  # Access the NetworkThrottle property
            >>> print(f"Network throttle object: {throttle}")
            >>> # Use the returned NetworkThrottle object to configure throttling as needed

        #ai-gen-doc
        """
        if self._network_throttle is None:
            self._network_throttle = NetworkThrottle(self)

        return self._network_throttle

    @property
    def client_group_filter(self) -> dict:
        """Get the filters associated with this client group.

        Returns:
            dict: A dictionary containing the client group filters.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> filters = client_group.client_group_filter
            >>> print(filters)
            >>> # Output: {'filterType': 'OS', 'filterValue': 'Windows'}

        #ai-gen-doc
        """
        client_group_filters = {}

        os_type_map = {
            1: 'windows_filters',
            2: 'unix_filters'
        }

        for filters_root in self._properties['globalFiltersInfo']['globalFiltersInfoList']:
            client_group_filters[os_type_map[filters_root['operatingSystemType']]] = filters_root.get(
                'globalFilters', {}).get('filters', [])

        return client_group_filters

    @property
    def is_auto_discover_enabled(self) -> bool:
        """Check if auto-discover is enabled for the client group.

        Returns:
            True if the auto-discover property is enabled for this client group, False otherwise.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> if client_group.is_auto_discover_enabled:
            ...     print("Auto-discover is enabled for this client group.")
            ... else:
            ...     print("Auto-discover is not enabled.")

        #ai-gen-doc
        """
        return self._properties.get('enableAutoDiscovery', False)

    @client_group_filter.setter
    def client_group_filter(self, filters: dict) -> None:
        """Set the server group filters for the client group.

        Args:
            filters: A dictionary specifying the filters to apply to the client group.

        Example:
            >>> group = ClientGroup()
            >>> group.client_group_filter = {"os_type": "Windows", "location": "DataCenter1"}
            >>> # The client group will now use the specified filters

        #ai-gen-doc
        """
        request_json = {}
        request_json['clientGroupDetail'] = self._properties
        filters_root = request_json['clientGroupDetail']['globalFiltersInfo']['globalFiltersInfoList']

        for var in filters_root:
            if var['operatingSystemType'] == 1:
                var['globalFilters'] = {
                    'filters': filters.get('windows_filters', var['globalFilters'].get(
                        'filters', []))
                }
            if var['operatingSystemType'] == 2:
                var['globalFilters'] = {
                    'filters': filters.get('unix_filters', var['globalFilters'].get(
                        'filters', []))
                }
            var['globalFilters']['opType'] = 1
        request_json['clientGroupOperationType'] = 2

        self._process_update_request(request_json)
        self.refresh()

    def enable_backup(self) -> None:
        """Enable backup operations for this ClientGroup.

        This method activates backup functionality for the client group, allowing 
        backup jobs to be performed on all clients within the group.

        Raises:
            SDKException: If the backup enable operation fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'Finance_Group')
            >>> client_group.enable_backup()
            >>> print("Backup enabled for the client group.")

        #ai-gen-doc
        """
        request_json = self._request_json_('Backup')

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_backup_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Backup'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_backup_at_time(self, enable_time: str, **kwargs: dict) -> None:
        """Schedule backup enablement at a specified UTC time for the client group.

        This method disables backup if it is not already disabled, and then schedules 
        backup to be enabled at the specified UTC time. The time must be provided in 
        24-hour format: 'YYYY-MM-DD HH:mm:ss'. An optional timezone can be specified 
        using the 'timezone' keyword argument.

        Args:
            enable_time: The UTC time to enable backup, in 'YYYY-MM-DD HH:mm:ss' format.
            **kwargs: Optional keyword arguments.
                - timezone (str): The timezone to use for the operation. Refer to the TIMEZONES 
                  dictionary in constants.py for valid values.

        Raises:
            SDKException: If the provided time is earlier than the current time, 
                if the time format is incorrect, or if enabling backup fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.enable_backup_at_time(
            ...     '2024-07-01 22:00:00',
            ...     timezone='Asia/Kolkata'
            ... )
            >>> print("Backup will be enabled at the specified time.")

        #ai-gen-doc
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('ClientGroup', '103')
        except ValueError:
            raise SDKException('ClientGroup', '104')

        request_json = self._request_json_('Backup', False, enable_time, **kwargs)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            return
        else:
            if error_message:
                o_str = 'Failed to enable Backup\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Backup'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_backup(self) -> None:
        """Disable backup operations for this ClientGroup.

        This method disables all backup activities associated with the current ClientGroup instance.
        If the operation fails, an SDKException is raised.

        Raises:
            SDKException: If the backup could not be disabled for the ClientGroup.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'Finance_Group')
            >>> client_group.disable_backup()
            >>> print("Backup disabled for the client group.")

        #ai-gen-doc
        """
        request_json = self._request_json_('Backup', False)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_backup_enabled = False
            return
        else:
            if error_message:
                o_str = 'Failed to disable Backup\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to diable Backup'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_restore(self) -> None:
        """Enable restore functionality for this ClientGroup.

        This method activates the restore capability for the current ClientGroup instance.
        If the operation fails, an SDKException is raised.

        Raises:
            SDKException: If the restore enable operation fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.enable_restore()
            >>> print("Restore enabled for the client group.")

        #ai-gen-doc
        """
        request_json = self._request_json_('Restore')

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_restore_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Restore'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_restore_at_time(self, enable_time: str, **kwargs: dict) -> None:
        """Schedule restore enablement at a specified UTC time for the client group.

        This method disables restore access if it is not already disabled, and then schedules
        restore access to be enabled at the specified UTC time. The time must be provided in
        24-hour format: 'YYYY-MM-DD HH:mm:ss'. An optional timezone can be specified using the
        'timezone' keyword argument.

        Args:
            enable_time: The UTC time at which to enable restore access, in 'YYYY-MM-DD HH:mm:ss' format.
            **kwargs: Optional keyword arguments.
                - timezone (str): The timezone to use for the operation. Refer to the TIMEZONES
                  dictionary in constants.py for valid values.

        Raises:
            SDKException: If the provided time is earlier than the current time, if the time format
                is incorrect, or if enabling restore fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> # Schedule restore enablement for 2024-07-01 15:00:00 UTC
            >>> client_group.enable_restore_at_time('2024-07-01 15:00:00', timezone='America/New_York')

        #ai-gen-doc
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('ClientGroup', '103')
        except ValueError:
            raise SDKException('ClientGroup', '104')

        request_json = self._request_json_('Restore', False, enable_time, **kwargs)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            return
        else:
            if error_message:
                o_str = 'Failed to enable Restore\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Restore'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_restore(self) -> None:
        """Disable restore operations for this ClientGroup.

        This method disables the ability to perform restore operations for all clients within the client group.
        If the operation fails, an SDKException is raised.

        Raises:
            SDKException: If the restore disable operation fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'Finance_Group')
            >>> client_group.disable_restore()
            >>> print("Restore operations have been disabled for the client group.")

        #ai-gen-doc
        """
        request_json = self._request_json_('Restore', False)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_restore_enabled = False
            return
        else:
            if error_message:
                o_str = 'Failed to disable Restore\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to disable Restore'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_data_aging(self) -> None:
        """Enable Data Aging for this ClientGroup.

        This method enables the Data Aging feature for the current ClientGroup instance.
        Data Aging is used to remove aged or obsolete data based on retention policies.

        Raises:
            SDKException: If enabling data aging fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.enable_data_aging()
            >>> print("Data Aging enabled for the client group.")

        #ai-gen-doc
        """
        request_json = self._request_json_('Data Aging')

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_data_aging_enabled = True
            return
        else:
            if error_message:
                o_str = 'Failed to enable Data Aging\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Data Aging'

            raise SDKException('ClientGroup', '102', o_str)

    def enable_data_aging_at_time(self, enable_time: str, **kwargs: dict) -> None:
        """Schedule Data Aging to be enabled at a specified UTC time.

        This method disables Data Aging if it is currently enabled, and then schedules it to be enabled 
        at the provided UTC time. The time must be specified in 24-hour format as 'YYYY-MM-DD HH:mm:ss'.

        Args:
            enable_time: The UTC time at which to enable Data Aging, in the format 'YYYY-MM-DD HH:mm:ss'.
            **kwargs: Optional keyword arguments.
                - timezone (str): The timezone to use for the operation. 
                  Refer to the TIMEZONES dictionary in constants.py for valid values.

        Raises:
            SDKException: If the provided time is earlier than the current time, 
                if the time format is incorrect, or if enabling Data Aging fails.

        Example:
            >>> group = ClientGroup()
            >>> group.enable_data_aging_at_time('2024-07-01 23:00:00', timezone='America/New_York')
            >>> print("Data Aging will be enabled at the specified time.")

        #ai-gen-doc
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('ClientGroup', '103')
        except ValueError:
            raise SDKException('ClientGroup', '104')

        request_json = self._request_json_('Data Aging', False, enable_time, **kwargs)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            return
        else:
            if error_message:
                o_str = 'Failed to enable Data Aging\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable Data Aging'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_data_aging(self) -> None:
        """Disable Data Aging for this ClientGroup.

        This method disables the Data Aging feature for the current ClientGroup instance.
        Data Aging is a process that removes aged data based on retention rules.

        Raises:
            SDKException: If the operation to disable data aging fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.disable_data_aging()
            >>> print("Data Aging has been disabled for the client group.")

        #ai-gen-doc
        """
        request_json = self._request_json_('Data Aging', False)

        error_code, error_message = self._process_update_request(request_json)

        if error_code == '0':
            self._is_data_aging_enabled = False
            return
        else:
            if error_message:
                o_str = 'Failed to disable Data Aging\nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to disable Data Aging'

            raise SDKException('ClientGroup', '102', o_str)

    @clientgroup_name.setter
    def clientgroup_name(self, value: str) -> None:
        """Set the name of the client group.

        Args:
            value: The new name to assign to the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'OldName')
            >>> client_group.clientgroup_name = 'NewGroupName'  # Use assignment for property setter
            >>> # The client group name is now updated to 'NewGroupName'

        #ai-gen-doc
        """
        if isinstance(value, str):
            output = self._update(
                clientgroup_name=value,
                clientgroup_description=self.description,
                associated_clients=self._associated_clients
            )

            if output[0]:
                return
            else:
                o_str = 'Failed to update the ClientGroup name\nError: "{0}"'
                raise SDKException('ClientGroup', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'ClientGroup', '102', 'Clientgroup name should be a string value'
            )

    @description.setter
    def description(self, value: str) -> None:
        """Set the description of the client group.

        Args:
            value: The new description to assign to the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.description = "This group contains all production servers."
            >>> # The client group's description is now updated

        #ai-gen-doc
        """
        if isinstance(value, str):
            output = self._update(
                clientgroup_name=self.name,
                clientgroup_description=value,
                associated_clients=self._associated_clients
            )

            if output[0]:
                return
            else:
                o_str = 'Failed to update the ClientGroup description\nError: "{0}"'
                raise SDKException('ClientGroup', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'ClientGroup', '102', 'Clientgroup description should be a string value'
            )

    def add_clients(self, clients: Union[str, List[str]], overwrite: bool = False) -> None:
        """Add clients to the ClientGroup.

        This method adds one or more clients to the client group. The clients can be specified
        as a comma-separated string of client names or as a list of client names. If the
        `overwrite` flag is set to True, any existing clients in the group will be removed
        before adding the new clients.

        Args:
            clients: A comma-separated string of client names or a list of client names to add to the group.
            overwrite: If True, removes all existing clients from the group before adding the new clients.
                Defaults to False.

        Raises:
            SDKException: If `clients` is not a string or list, if no valid clients are found,
                or if the operation fails to add clients to the client group.

        Example:
            >>> client_group = ClientGroup()
            >>> # Add a single client by name
            >>> client_group.add_clients('client1')
            >>> # Add multiple clients using a comma-separated string
            >>> client_group.add_clients('client1,client2,client3')
            >>> # Add multiple clients using a list
            >>> client_group.add_clients(['client1', 'client2'])
            >>> # Overwrite existing clients with a new list
            >>> client_group.add_clients(['client4', 'client5'], overwrite=True)

        #ai-gen-doc
        """
        if overwrite is True:
            return self._add_or_remove_clients(clients, 'OVERWRITE')
        else:
            return self._add_or_remove_clients(clients, 'ADD')

    def remove_clients(self, clients: Union[str, list]) -> None:
        """Remove one or more clients from the ClientGroup.

        Args:
            clients: A comma-separated string of client names or a list of client names to be removed from the client group.

        Raises:
            SDKException: If 'clients' is not a string or list, if no valid clients are found, or if removal fails.

        Example:
            >>> client_group = ClientGroup()
            >>> # Remove clients using a comma-separated string
            >>> client_group.remove_clients("client1,client2")
            >>> # Remove clients using a list
            >>> client_group.remove_clients(["client3", "client4"])
            >>> print("Clients removed from the group successfully.")

        #ai-gen-doc
        """
        return self._add_or_remove_clients(clients, 'DELETE')

    def remove_all_clients(self) -> None:
        """Remove all clients associated with this client group.

        This method clears all clients from the client group. If the operation fails,
        an SDKException is raised.

        Raises:
            SDKException: If the method fails to remove all clients from the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.remove_all_clients()
            >>> print("All clients have been removed from the client group.")

        #ai-gen-doc
        """
        output = self._update(
            clientgroup_name=self.name,
            clientgroup_description=self.description,
            associated_clients=self._associated_clients,
            operation_type="CLEAR"
        )

        if output[0]:
            return
        else:
            o_str = 'Failed to remove clients from the ClientGroup\nError: "{0}"'
            raise SDKException('ClientGroup', '102', o_str.format(output[2]))

    def push_network_config(self) -> None:
        """Push the network configuration to all clients in the client group.

        This method initiates a network configuration push operation for the entire client group.
        It is typically used to update network settings across multiple clients managed by the group.

        Raises:
            SDKException: If the input data is invalid, the response is empty, or the response indicates failure.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.push_network_config()
            >>> print("Network configuration push initiated for the client group.")

        #ai-gen-doc
        """

        xml_execute_command = """
                        <App_PushFirewallConfigurationRequest>
                        <entity clientGroupName="{0}"/>
                        </App_PushFirewallConfigurationRequest>
            """.format(self.clientgroup_name)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['EXECUTE_QCOMMAND'], xml_execute_command
        )

        if flag:
            if response.json():
                error_code = -1
                error_message = ""
                if 'entityResponse' in response.json():
                    error_code = response.json()['entityResponse'][0]['errorCode']

                    if 'errorMessage' in response.json():
                        error_message = response.json()['errorMessage']

                elif 'errorMessage' in response.json():
                    error_message = response.json()['errorMessage']

                    if 'errorCode' in response.json():
                        error_code = response.json()['errorCode']

                if error_code != 0:
                    raise SDKException('ClientGroup', '102', error_message)

            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def push_servicepack_and_hotfix(
            self,
            reboot_client: bool = False,
            run_db_maintenance: bool = True
        ) -> 'Job':
        """Trigger the installation of service packs and hotfixes on all clients in the group.

        This method initiates a job to push the latest service pack and hotfix updates to all clients 
        within the client group. You can optionally specify whether to reboot the clients after installation 
        and whether to run database maintenance as part of the process.

        Args:
            reboot_client: If True, the client machines will be rebooted after the installation.
                Defaults to False.
            run_db_maintenance: If True, database maintenance will be performed during the update.
                Defaults to True.

        Returns:
            Job: An instance of the Job class representing the download and installation job.

        Raises:
            SDKException: If the download job fails, the response is empty, the response is not successful,
                or if another download job is already running.

        Note:
            This method cannot be used for revision upgrades; it is intended only for service pack and hotfix installations.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'WebServers')
            >>> job = client_group.push_servicepack_and_hotfix(reboot_client=True, run_db_maintenance=False)
            >>> print(f"Job ID: {job.job_id}")

        #ai-gen-doc
        """
        install = Install(self._commcell_object)
        return install.push_servicepack_and_hotfix(
            client_computer_groups=[self.name],
            reboot_client=reboot_client,
            run_db_maintenance=run_db_maintenance)

    def repair_software(
            self,
            username: str = None,
            password: str = None,
            reboot_client: bool = False
        ) -> 'Job':
        """Trigger a repair of the software on all clients in the client group.

        This method initiates a repair operation for the software installed on the client group.
        Optionally, you can provide credentials for the target machines and specify whether the
        clients should be rebooted after the repair.

        Args:
            username: The username to use for re-installing features on the client machines. If not provided, the default credentials are used.
            password: The base64-encoded password corresponding to the username. If not provided, the default credentials are used.
            reboot_client: Whether to reboot the clients in the group after the repair operation. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the repair job.

        Raises:
            SDKException: If the install job fails, the response is empty, or the response indicates failure.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'WebServers')
            >>> job = client_group.repair_software(username='admin', password='cGFzc3dvcmQ=', reboot_client=True)
            >>> print(f"Repair job started with Job ID: {job.job_id}")

        #ai-gen-doc
        """
        install = Install(self._commcell_object)
        return install.repair_software(
            client_group=self.name,
            username=username,
            password=password,
            reboot_client=reboot_client
        )

    def update_properties(self, properties_dict: dict) -> None:
        """Update the properties of the client group.

        This method updates the client group properties using the provided dictionary.
        You can obtain a deep copy of the current properties using `self.properties`,
        modify the desired fields, and then pass the updated dictionary to this method.

        Args:
            properties_dict: A dictionary containing the client group properties to update.

        Raises:
            SDKException: If the update fails, the response is empty, or the response code is not as expected.

        Example:
            >>> # Get a deep copy of current properties
            >>> props = client_group.properties
            >>> # Modify a property
            >>> props['clientGroup']['description'] = "Updated description"
            >>> # Update the client group with new properties
            >>> client_group.update_properties(props)

        #ai-gen-doc
        """
        request_json = {
            "clientGroupOperationType": 2,
            "clientGroupDetail": {
                "clientGroup": {
                    "clientGroupName": self.name
                }
            }
        }

        request_json['clientGroupDetail'].update(properties_dict)
        error_code, error_message = self._process_update_request(request_json)

        if error_code != '0':
            raise SDKException(
                'ClientGroup', '102', 'Failed to update client group property\nError: "{0}"'.format(error_message)
            )

    def add_additional_setting(
            self,
            category: str = None,
            key_name: str = None,
            data_type: str = None,
            value: str = None,
            comment: str = None,
            enabled: int = 1
        ) -> None:
        """Add an additional registry key setting to the client group property.

        This method allows you to add a custom registry key (additional setting) to the client group,
        which can be used to configure advanced or custom behaviors for all clients in the group.

        Args:
            category: The category under which the registry key will be added.
            key_name: The name of the registry key to add.
            data_type: The data type of the registry key. Accepted values are:
                'BOOLEAN', 'INTEGER', 'STRING', 'MULTISTRING', 'ENCRYPTED'.
            value: The value to assign to the registry key.
            comment: Optional comment describing the additional setting.
            enabled: Set to 1 to enable the additional setting, or 0 to disable it. Default is 1.

        Raises:
            SDKException: If the additional setting could not be added, if the response is empty,
                or if the response code is not as expected.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.add_additional_setting(
            ...     category='Network',
            ...     key_name='EnableCustomPort',
            ...     data_type='BOOLEAN',
            ...     value='True',
            ...     comment='Enable custom port for all clients in group',
            ...     enabled=1
            ... )
            >>> print("Additional setting added successfully.")

        #ai-gen-doc
        """

        properties_dict = {
            "registryKeys": [{"deleted": 0,
                              "hidden": False,
                              "relativepath": category,
                              "keyName": key_name,
                              "isInheritedFromClientGroup": False,
                              "comment": comment,
                              "type": data_type,
                              "value": value,
                              "enabled": enabled}]
        }

        self.update_properties(properties_dict)

    def delete_additional_setting(
            self,
            category: str = None,
            key_name: str = None
        ) -> None:
        """Delete a registry key from the client group property.

        This method removes a specified registry key from the client group's additional settings,
        based on the provided category and key name.

        Args:
            category: The category under which the registry key is stored.
            key_name: The name of the registry key to delete.

        Raises:
            SDKException: If the deletion fails, the response is empty, or the response code is not as expected.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.delete_additional_setting(category='Network', key_name='EnableIPv6')
            >>> print("Registry key deleted successfully.")

        #ai-gen-doc
        """

        properties_dict = {
            "registryKeys": [{"deleted": 1,
                              "relativepath": category,
                              "keyName": key_name}]
        }

        self.update_properties(properties_dict)

    def enable_auto_discover(self) -> None:
        """Enable autodiscover functionality at the ClientGroup level.

        This method activates the autodiscover feature for the client group, allowing automatic detection and addition of clients as per the group configuration.

        Raises:
            SDKException: If enabling autodiscover fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.enable_auto_discover()
            >>> print("Autodiscover enabled for the client group.")

        #ai-gen-doc
        """
        request_json = {
            "clientGroupOperationType": 2,
            'clientGroupDetail': {
                    'enableAutoDiscovery': True,
                    "clientGroup": {
                            "clientGroupName": self.clientgroup_name
            }
        }
        }
        error_code, error_message = self._process_update_request(request_json)
        if error_code != '0':
            if error_message:
                o_str = 'Failed to enable autodiscover \nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to enable autodiscover'

            raise SDKException('ClientGroup', '102', o_str)

    def disable_auto_discover(self) -> None:
        """Disable autodiscover functionality at the ClientGroup level.

        This method turns off the autodiscover feature for the current ClientGroup instance.
        If the operation fails, an SDKException is raised.

        Raises:
            SDKException: If the autodiscover feature could not be disabled.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.disable_auto_discover()
            >>> print("Autodiscover has been disabled for the client group.")

        #ai-gen-doc
        """
        request_json = {
            "clientGroupOperationType": 2,
            'clientGroupDetail': {
                    'enableAutoDiscovery': False,
                    "clientGroup": {
                            "clientGroupName": self.clientgroup_name
            }
        }
        }
        error_code, error_message = self._process_update_request(request_json)
        if error_code != '0':
            if error_message:
                o_str = 'Failed to Disable autodiscover \nError: "{0}"'.format(error_message)
            else:
                o_str = 'Failed to Disable autodiscover'

            raise SDKException('ClientGroup', '102', o_str)

    def refresh(self) -> None:
        """Reload the properties of the ClientGroup to reflect the latest state.

        This method updates the ClientGroup instance with the most current information,
        ensuring that any changes made externally are reflected in the object.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> client_group.refresh()
            >>> print("ClientGroup properties refreshed successfully")

        #ai-gen-doc
        """
        self._initialize_clientgroup_properties()
        self._networkprop = Network(self)
        self._network_throttle = None
        self._additional_settings = None

    def refresh_clients(self) -> None:
        """Reload the list of clients associated with this client group.

        This method refreshes the internal client list, ensuring that any changes 
        to the group membership are reflected in the current object.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'Finance_Group')
            >>> client_group.refresh_clients()
            >>> print("Client group members refreshed successfully")

        #ai-gen-doc
        """
        refresh_client_api = self._services['SERVERGROUPS_V4'] + f"/{self._clientgroup_id}/Refresh"

        flag, response = self._cvpysdk_object.make_request("PUT", refresh_client_api)

        if not flag:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        response_json = response.json()
        if not response_json:
            raise SDKException('Response', '102')

        error_code = response_json.get("errorCode")
        error_message = response_json.get("errorMessage")

        if error_code:
            raise SDKException("ClientGroup", '102', error_message)

        self.refresh()

    def change_company(self, target_company_name: str) -> None:
        """Change the company association for the client group and all its clients.

        This method migrates the client group and all clients belonging to it to the specified target company.

        Args:
            target_company_name: The name of the company to which the client group and its clients will be migrated.

        Raises:
            SDKException: If the response from the operation is empty or indicates failure.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'Finance_Group')
            >>> client_group.change_company('NewCompanyName')
            >>> print("Client group and its clients have been migrated to the new company.")

        #ai-gen-doc
        """
        if target_company_name.lower() == 'commcell':
            company_id = 0
        else:
            company_id = int(self._commcell_object.organizations.get(target_company_name).organization_id)

        request_json = {
            "entities": [
                {
                    "name": self._clientgroup_name,
                    "clientGroupId": int(self._clientgroup_id),
                    "_type_": 28
                }
            ]
        }

        req_url = self._services['ORGANIZATION_ASSOCIATION'] % company_id
        flag, response = self._cvpysdk_object.make_request('PUT', req_url, request_json)

        if flag:
            if response.json():
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    raise SDKException('Organization', '110', 'Error: {0}'.format(response.json()['errorMessage']))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        self.refresh()

    def add_http_proxy(self, use_client_os_proxy_settings=False, proxy_server="", proxy_port=0,
                       use_authentication=False, use_with_network_topology=False,
                       proxy_credential_name=None, proxy_credential_id=None, proxy_bypass_list="") -> None:
        """Add an HTTP proxy configuration to the client group

        Args:
            use_client_os_proxy_settings (bool): Use the client OS proxy settings.

            proxy_server (str): The proxy server address.

            proxy_port (int): The proxy server port.

            use_authentication (bool): Use authentication for the proxy.

            use_with_network_topology (bool): Use the proxy with network topology.

            proxy_credential_name (str): The name of the proxy credential.

            proxy_credential_id (int): The ID of the proxy credential.

            proxy_bypass_list (str): Comma-separated list of addresses to bypass the proxy.

        """

        proxy_type = "GLOBAL" if use_client_os_proxy_settings else "EXPLICIT"

        if proxy_type == "EXPLICIT":
            if not proxy_server or not isinstance(proxy_server, str):
                raise SDKException( 'ClientGroup', 102,
                    "proxy_server is required and must be a non-empty string when using EXPLICIT proxy."
                )
            if not isinstance(proxy_port, int) or not (1 <= proxy_port <= 65535):
                raise SDKException( 'ClientGroup', 102,
                    "proxy_port must be an integer between 1 and 65535 when using EXPLICIT proxy."
                )

        request_json = {
            "entity": {
                "clientGroupId": int(self.clientgroup_id)
            },
            "httpProxy": {
                "server": proxy_server,
                "port": proxy_port,
                "useForNetworkRoutes": use_with_network_topology,
                "proxyBypassList": proxy_bypass_list,
                "configureHTTPProxy": True,
                "useAuthentication": use_authentication,
                "proxyType": proxy_type
            }
        }

        if proxy_credential_id and proxy_credential_name:
            request_json["httpProxy"]["credentials"] = {
                "credentialId": proxy_credential_id,
                "credentialName": proxy_credential_name
            }
        else:
            request_json["httpProxy"]["selectedCredential"] = None


        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['HTTP_PROXY'], request_json
        )

        if flag:
            if response.json():
                error_code = -1
                error_message ="Failed to add HTTP proxy configuration to the client group."
                if 'errorCode' in response.json():
                        error_code = response.json()['errorCode']
                if error_code != 0:
                    raise SDKException('ClientGroup', '102', error_message)

            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def remove_http_proxy(self) -> None:
        """Remove the HTTP proxy configuration from the client group."""

        request_json = {
            "entity": {
                "clientGroupId": int(self.clientgroup_id)
            },
            "httpProxy": {
                "configureHTTPProxy": False
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['HTTP_PROXY'], request_json
        )

        if flag:
            if response.json():
                error_code = -1
                error_message = "Failed to remove HTTP proxy configuration to the client group."
                if 'errorCode' in response.json():
                    error_code = response.json()['errorCode']
                if error_code != 0:
                    raise SDKException('ClientGroup', '102', error_message)

            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
        
    @property
    def additional_settings(self) -> dict:
        """Get the additional settings associated with this client group.

        Returns:
            dict: A dictionary containing additional configuration settings for the client group.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> settings = client_group.additional_settings
            >>> print(settings)
            {'setting1': 'value1', 'setting2': 'value2'}

        #ai-gen-doc
        """
        if self._additional_settings is None:
            self._additional_settings = AdditionalSettings(self)
        return self._additional_settings

    def get_power_management(self) -> dict:
        """Retrieve the current cloud VM power management configuration for this client group.

        Returns:
            dict: The ``powerManagementInfo`` dictionary from the API response, containing
            fields such as ``isPowerManagementEnabled``, ``isPowerMgmtAllowed``,
            ``isPowerMgmtSupported``, ``isPowerMgmtAllowedCheck``, and
            ``selectedCloudController``.

        Raises:
            SDKException: If the response is empty or the request fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> info = client_group.get_power_management()
            >>> print(info)
            {'isPowerManagementEnabled': True, 'isPowerMgmtAllowed': True, ...}
        """
        get_url = self._services['CLIENTGROUP_CLOUD_POWER_MGMT_GET'] % self.clientgroup_id
        flag, response = self._cvpysdk_object.make_request('GET', get_url)

        if not flag:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        if not response.json():
            raise SDKException('Response', '102')

        return response.json().get('powerManagementInfo', {})

    def set_power_management(self, cloud_controller_client: str, enable: bool = False) -> None:
        """Enable or disable cloud VM power management for this client group.

        Calls :meth:`get_power_management` to fetch the current ``isPowerMgmtAllowed``,
        ``isPowerMgmtSupported``, and ``isPowerMgmtAllowedCheck`` values, then issues
        a PUT request updating only ``isPowerManagementEnabled``.

        Args:
            cloud_controller_client: Name of the cloud controller client (hypervisor) to
                associate with power management.
            enable: ``True`` to enable power management, ``False`` to disable it.
                Defaults to ``False``.

        Raises:
            SDKException: If the client does not exist, or if the GET/PUT request fails.

        Example:
            >>> client_group = ClientGroup(commcell_object, 'MyClientGroup')
            >>> # Enable power management
            >>> client_group.set_power_management('TestGroup-Target-Hypervisor', enable=True)
            >>> # Disable power management
            >>> client_group.set_power_management('TestGroup-Target-Hypervisor', enable=False)
        """
        cloud_client = self._commcell_object.clients.get(cloud_controller_client)
        cloud_client_id = int(cloud_client.client_id)

        power_info = self.get_power_management()

        request_json = {
            "cgId": int(self.clientgroup_id),
            "powerManagementInfo": {
                "isPowerManagementEnabled": enable,
                "isPowerMgmtAllowed": power_info.get('isPowerMgmtAllowed', True),
                "isPowerMgmtSupported": power_info.get('isPowerMgmtSupported', True),
                "isPowerMgmtAllowedCheck": power_info.get('isPowerMgmtAllowedCheck', True),
                "selectedCloudController": {
                    "clientId": cloud_client_id,
                    "clientName": cloud_controller_client
                }
            }
        }

        put_url = self._services['CLIENTGROUP_CLOUD_POWER_MGMT']
        flag, response = self._cvpysdk_object.make_request('PUT', put_url, request_json)

        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    error_message = response.json().get('errorMessage', 'Failed to update power management.')
                    raise SDKException('ClientGroup', '102', error_message)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
