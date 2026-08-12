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
    File for operating on a Dynamics 365 CRM Subclient.

MSDynamics365Subclient is the only class defined in this file.

MSDynamics365Subclient:             Derived class from O365AppsSubclient Base class, representing a
                                    Dynamics 365 subclient, and to perform operations on that subclient

MSDynamics365Subclient:

    *****************                       Methods                      *****************

    _get_subclient_properties()             --  Gets the subclient related properties of a MS Dynamics 365 subclient

    _get_subclient_properties_json()        --  get the all subclient related properties of this subclient.

    get_discovered_tables()                 --  Method to get the tables discovered from the MS Dynamics 365 CRM subclient
    get_discovered_environments()           --  Method to get the environments discovered from the Dynamics 365 CRM subclient
    _get_associated_content()               --  Method to get the content associated with a Dynamics 365 CRM subclient
    get_associated_tables()                 --  Method to get the tables associated with a Dynamics 365 CRM client
    get_associated_environments()           --  Method to get the environments associated with a Dynamics 365 CRM client
    _set_association_json()                 --  JSON to set the content association for a Dynamics 365 CRM client
    _set_content_association()              --  Method to associate some content to a Dynamics 365 CRM client...
    _table_association_info_json()          --  Private Method to create the association JSON for associating tables
                                                to a Dynamics 365 CRM client.
    set_table_associations()                --  Method to add table associations to a Dynamics 365 CRM client.
    _environment_association_info_json()    --  Method to create the association JSON for associating environments
                                                to a Dynamics 365 CRM client.
    set_environment_associations()          --  Method to add environment associations to a Dynamics 365 CRM client.
    _json_for_backup_task()                 --  Method to create the association JSON for backing up content for a Dynamics 365 subclient
    _backup_content_json()                  --  Method to fetch the metadata properties for backing up content for a Dynamics 365 subclient
    _run_backup()                           --  Method to run backup for the content of a Dynamics 365 subclient
    backup_tables()                         --  Method to run backup for the specified tables of a Dynamics 365 subclient
    backup_environments()                   --  Method to run backup for the specified environments of a Dynamics 365 subclient
    launch_client_level_full_backup()     --  Method to run client level full backup for the content of a Dynamics 365 subclient
    _restore_content_json()                 --  Restore JSON for restoring content for a Dynamics 365 subclient
    _get_restore_item_path()                --  Get the complete path of the content for running a restore job
    _prepare_restore_json()                 --  Method to prepare JSON/ Python dict for  in- place restore for the content specified.
    restore_in_place()                      --  Method to run in- place restore for the content specified.
    launch_d365_licensing()                 --  Method to launch Licensing API call.
    _get_environment_id_for_oop_restore()   --  Get the Environment ID for an environment for Out of Place Restore
    restore_out_of_place()                  --  Method to run out-of-place restore for the content specified.
    browse()                                --  Browse for the backed up content for a Dynamics 365 subclient
    _get_guid_for_path()                    --  Method to get the browse GUID corresponding to the path
    _perform_browse()                       --  Perform a browse of the backed up content
    _get_dynamics365_browse_params()        --  Default dictionary for the browse parameters for a Dynamics 365 browse query.


    *****************                       Properties                      *****************

    discovered_environments                 --  Property to get the tables discovered by the Dynamics 365 subclient.
    discovered_tables                       --  Dictionary of tables discovered by the subclient
    browse_item_type()                      --  Dynamics 365 item type

"""

import copy
import json
import time
from typing import Any, Dict, List, Optional

from ...exception import SDKException

from ..o365apps_subclient import O365AppsSubclient
from ..casubclient import CloudAppsSubclient
from ...job import Job

class MSDynamics365Subclient(O365AppsSubclient):
    """
    Represents a subclient for Microsoft Dynamics 365 within the O365 Apps backup and restore framework.

    This class extends the O365AppsSubclient to provide specialized management, backup, and restore
    operations for MS Dynamics 365 environments and tables. It offers comprehensive discovery,
    association, backup, restore, and browsing capabilities tailored to Dynamics 365 data.

    Key Features:
        - Discovery of Dynamics 365 environments and tables
        - Management of associated environments and tables for backup
        - Setting and updating associations for environments and tables
        - Full and selective backup operations for environments and tables
        - In-place and out-of-place restore operations with support for overwrite and destination selection
        - Browsing of backed-up content with support for deleted items and time-based queries
        - Licensing operations for Dynamics 365 clients
        - Access to discovered environments, tables, and browse item types via properties

    #ai-gen-doc
    """

    def __init__(self, backupset_object: object, subclient_name: str, subclient_id: int = None) -> None:
        """Initialize an MSDynamics365Subclient instance.

        Args:
            backupset_object: Instance of the backup-set class associated with this subclient.
            subclient_name: Name of the MSDynamics365 subclient.
            subclient_id: Optional; unique identifier for the subclient. If not provided, it will be determined automatically.

        Example:
            >>> backupset = BackupsetClass(commcell_object, 'BackupSetName')
            >>> subclient = MSDynamics365Subclient(backupset, 'Subclient1')
            >>> # Optionally, provide a subclient ID
            >>> subclient_with_id = MSDynamics365Subclient(backupset, 'Subclient2', subclient_id=101)

        #ai-gen-doc
        """
        super(MSDynamics365Subclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._client_object = self._instance_object._agent_object._client_object
        self._associated_tables: dict = dict()
        self._associated_environments: dict = dict()
        self._discovered_environments: dict = dict()
        self._discovered_tables: dict = dict()
        self._instance_type: int = 35
        self._app_id: int = 134
        # App ID for cloud apps
        self._Dynamics365_SET_USER_POLICY_ASSOCIATION = self._commcell_object._services['SET_USER_POLICY_ASSOCIATION']

    def _get_subclient_properties(self) -> dict:
        """Retrieve the properties specific to the MS Dynamics 365 subclient.

        Returns:
            dict: A dictionary containing the subclient-related properties for the MS Dynamics 365 subclient.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> properties = subclient._get_subclient_properties()
            >>> print(properties)
            >>> # Output will be a dictionary with subclient property details

        #ai-gen-doc
        """
        super(MSDynamics365Subclient, self)._get_subclient_properties()

    def _get_subclient_properties_json(self) -> dict:
        """Retrieve all properties related to this MSDynamics365 subclient as a dictionary.

        Returns:
            dict: A dictionary containing all subclient properties and their values.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> properties = subclient._get_subclient_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary of subclient properties

        #ai-gen-doc
        """

        return {'subClientProperties': self._subclient_properties}

    def discover_tables(self) -> dict:
        """Retrieve the tables discovered from the MS Dynamics 365 CRM subclient.

        Returns:
            dict: A dictionary containing the details of tables discovered in the subclient.

        Example:
            >>> msd_subclient = MSDynamics365Subclient()
            >>> tables = msd_subclient.discover_tables()
            >>> print(f"Discovered tables: {tables}")
            >>> # The returned dictionary contains table information for further processing

        #ai-gen-doc
        """
        self._discovered_tables = self._instance_object.discover_content(environment_discovery=False)
        return self._discovered_tables

    def discover_environments(self) -> dict:
        """Retrieve the environments discovered from the Dynamics 365 CRM subclient.

        Returns:
            dict: A dictionary containing details of the discovered Dynamics 365 environments.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> environments = subclient.discover_environments()
            >>> print(f"Discovered environments: {environments}")

        #ai-gen-doc
        """
        self._discovered_environments = self._instance_object.discover_content(environment_discovery=True)
        return self._discovered_environments

    @property
    def discovered_environments(self) -> dict:
        """Get the environments discovered by the Dynamics 365 subclient.

        This property returns a dictionary containing the environments that have been discovered
        by the Dynamics 365 subclient. If you require the most up-to-date list of environments,
        call the `refresh` method before accessing this property.

        Returns:
            dict: A dictionary of discovered environments, where keys and values represent
            environment details as provided by the subclient.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> environments = subclient.discovered_environments
            >>> print(f"Discovered environments: {environments}")
            >>> # To ensure the list is current:
            >>> subclient.refresh()
            >>> environments = subclient.discovered_environments

        #ai-gen-doc
        """
        if not bool(self._discovered_environments):
            self.discover_environments()
        return self._discovered_environments

    @property
    def discovered_tables(self) -> dict:
        """Get the tables discovered by the Dynamics 365 subclient.

        This property returns a dictionary containing the tables that have been discovered
        by the Dynamics 365 subclient. If you require the most up-to-date list of tables,
        call the `refresh` method before accessing this property.

        Returns:
            dict: A dictionary where keys are table names and values contain table details.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> tables = subclient.discovered_tables
            >>> print(f"Discovered tables: {list(tables.keys())}")
            >>> # To ensure the list is current, call subclient.refresh() before accessing

        #ai-gen-doc
        """
        if not bool(self._discovered_tables):
            self.discover_tables()
        return self._discovered_tables

    def _get_associated_content(self, is_environment: bool = False, max_retries: int = 3, retry_delay: int = 5) -> list[dict]:
        """Retrieve the content associated with a Dynamics 365 CRM subclient.

        This method fetches either the environments or tables associated with the subclient,
        depending on the value of `is_environment`. It supports retrying the fetch operation
        if the content list is initially empty.

        Args:
            is_environment: If True, retrieves associated environments; if False (default), retrieves associated tables.
            max_retries: Maximum number of retries if the content list is empty. Default is 3.
            retry_delay: Delay in seconds between retries. Default is 5.

        Returns:
            A list of dictionaries, each representing an associated environment or table.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> tables = subclient._get_associated_content()
            >>> print(f"Associated tables: {tables}")
            >>> environments = subclient._get_associated_content(is_environment=True)
            >>> print(f"Associated environments: {environments}")

        #ai-gen-doc
        """
        discover_by_type: int
        if is_environment is True:
            discover_by_type = 5
        else:
            discover_by_type = 14

        _GET_ASSOCIATED_CONTENT = self._services['USER_POLICY_ASSOCIATION']
        request_json = {
            "discoverByType": discover_by_type,
            "bIncludeDeleted": False,
            "cloudAppAssociation": {
                "subclientEntity": {
                    "subclientId": int(self.subclient_id)
                }
            }
        }

        for attempt in range(max_retries):
            flag, response = self._cvpysdk_object.make_request('POST', _GET_ASSOCIATED_CONTENT, request_json)

            if flag:
                try:
                    if response and response.json():
                        associations = response.json().get('associations', [])
                        content_list = []

                        if discover_by_type == 5:  # Environments
                            for environment in associations:
                                environment_name = environment.get("groups", {}).get("name")
                                env_dict = {
                                    "name": environment_name,
                                    "id": environment.get("groups", {}).get("id"),
                                    "userAccountInfo": environment.get("userAccountInfo", {}),
                                    "plan": environment.get("plan", {}),
                                    "is_environment": True
                                }
                                content_list.append(env_dict)

                        elif discover_by_type == 14:  # Tables
                            for table in associations:
                                table_name = table.get("userAccountInfo", {}).get("displayName")
                                table_dict = {
                                    "name": table_name,
                                    "environment_name": table.get("userAccountInfo", {}).get("ParentWebGuid", ""),
                                    "userAccountInfo": table.get("userAccountInfo", {}),
                                    "plan": table.get("plan", {}),
                                    "is_environment": False
                                }
                                content_list.append(table_dict)

                        if content_list:
                            return content_list

                        time.sleep(retry_delay)
                    else:
                        time.sleep(retry_delay)
                except ValueError as e:
                    raise SDKException('Response', '102', f"Invalid JSON response: {str(e)}")
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

        return []

    def get_associated_tables(self, refresh: bool = False) -> list[dict]:
        """Retrieve the tables associated with a Dynamics 365 CRM client.

        Args:
            refresh: If True, refreshes the dictionary contents and fetches the latest table associations.

        Returns:
            A list of dictionaries, each representing a table associated with the client.
            Each dictionary contains the following keys:
                - name: Name of the table.
                - environment_name: Name of the environment to which the table belongs.
                - plan: Dictionary with Dynamics 365 plan details used for content association.
                - is_environment: Boolean indicating if the entry is an environment (False for a table).
                - userAccountInfo: Metadata information for the table, including user and backup details.

            Example of a returned table dictionary:
                {
                    'name': 'account',
                    'environment_name': 'sample-environment-name',
                    'userAccountInfo': {
                        'aliasName': 'https://<org-url-name>.crm.dynamics.com/api/data/v9.1/account',
                        'displayName': 'Account',
                        'ParentWebGuid': 'org-environment-name',
                        'lastBackupJobRanTime': {'time': 1680000000},
                        'IdxCollectionTime': {'time': 1680000000},
                        'user': {
                            '_type_': 13,
                            'userGUID': '<table-GUID>'
                        }
                    },
                    'plan': {
                        'planName': '<PLAN-NAME>',
                        'planId': 12345
                    },
                    'is_environment': False
                }

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> tables = subclient.get_associated_tables(refresh=True)
            >>> for table in tables:
            ...     print(f"Table: {table['name']}, Environment: {table['environment_name']}")

        #ai-gen-doc
        """
        if refresh is True:
            self._associated_tables = self._get_associated_content(is_environment=False)
        return self._associated_tables

    def get_associated_environments(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """Retrieve the environments associated with a Dynamics 365 CRM client.

        Args:
            refresh: If True, fetches the latest environment associations from the server.
                If False, returns cached associations if available.

        Returns:
            A list of dictionaries, each representing an environment associated with the client.
            Each dictionary contains keys such as:
                - 'name': Name of the environment.
                - 'id': Unique identifier for the environment.
                - 'userAccountInfo': Metadata information for the environment, including user details and backup times.
                - 'plan': Dictionary with plan details ('planName', 'planId').
                - 'is_environment': Boolean indicating if the entry is an environment.

            Example:
                >>> subclient = MSDynamics365Subclient()
                >>> environments = subclient.get_associated_environments(refresh=True)
                >>> for env in environments:
                ...     print(f"Environment: {env['name']}, Plan: {env['plan']['planName']}")
                >>> # Each environment dictionary contains detailed metadata

        #ai-gen-doc
        """
        if refresh is True:
            self._associated_environments = self._get_associated_content(is_environment=True)
        return self._associated_environments

    def _set_association_json(self, is_environment: bool = False) -> dict:
        """Generate the JSON structure to set content association for a Dynamics 365 CRM client.

        Args:
            is_environment: Indicates whether the content to be associated is an environment.
                Defaults to False.

        Returns:
            A dictionary representing the content association JSON for the Dynamics 365 CRM client.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> association_json = subclient._set_association_json(is_environment=True)
            >>> print(association_json)
            # Output: {'associationType': 'environment', ...}

        #ai-gen-doc
        """
        set_content_association_json = {
                                            "LaunchAutoDiscovery": is_environment,
                                            "cloudAppAssociation": {
                                            "accountStatus": 0,
                                            "cloudAppDiscoverinfo": {
                                                "userAccounts": [
                                                ],
                                                "groups": [],
                                                "discoverByType": 14 if is_environment is False else 15
                                            },
                                            "subclientEntity": self._subClientEntity
                                            }
                                        }

        return set_content_association_json

    def _set_content_association(self, content_json: dict) -> None:
        """Associate content with a Dynamics 365 CRM client.

        This method links the provided content JSON to the Dynamics 365 CRM client,
        enabling the client to recognize and utilize the associated content.

        Args:
            content_json: A dictionary containing the association details for the content.

        Example:
            >>> content = {
            ...     "entity": "Account",
            ...     "fields": ["name", "emailaddress1"],
            ...     "filter": {"statuscode": "Active"}
            ... }
            >>> subclient._set_content_association(content)
            >>> print("Content association set successfully.")

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._Dynamics365_SET_USER_POLICY_ASSOCIATION, content_json
        )

        if flag:
            try:
                if response.json():
                    if response.json().get('resp', {}).get('errorCode', 0) != 0:
                        error_message = response.json()['errorMessage']
                        output_string = 'Failed to Create Association for a Dynamics 365 CRM client\nError: "{0}"'
                        raise SDKException(
                            'Subclient', '102', output_string.format(error_message)
                        )
                    else:
                        self.refresh()
            except ValueError:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _table_association_info_json(self, tables_list: list[tuple[str, str]]) -> list[dict]:
        """Create the association JSON metadata for associating tables to a Dynamics 365 CRM client.

        This private method generates a list of metadata dictionaries for each table-environment pair,
        which can be used to associate tables with a Dynamics 365 CRM client.

        Args:
            tables_list: A list of tuples, where each tuple contains:
                - table_name (str): The name of the table to be associated.
                - environment_name (str): The name of the environment to which the table belongs.

                Example:
                    [
                        ("account", "Production"),
                        ("contact", "Sandbox")
                    ]

        Returns:
            A list of dictionaries containing metadata information for each table association.

        Example:
            >>> tables = [("account", "Production"), ("contact", "Sandbox")]
            >>> metadata = subclient._table_association_info_json(tables)
            >>> print(metadata)
            [
                {'tableName': 'account', 'environmentName': 'Production'},
                {'tableName': 'contact', 'environmentName': 'Sandbox'}
            ]

        #ai-gen-doc
        """
        tables_info: list = list()
        _discovered_tables = self.discovered_tables
        tables_dict = {}

        if not bool(_discovered_tables):
            raise SDKException('Subclient', '101',
                               "Discovered Tables is Empty.")

        for table in _discovered_tables:
            if table["ParentWebGuid"] in tables_dict:
                tables_dict[table["ParentWebGuid"]].update({table["displayName"]: table})
            else:
                tables_dict.update({table["ParentWebGuid"]: {}})

        for table in tables_list:
            table_name, env_name = table
            if env_name in tables_dict:
                if table_name in tables_dict[env_name]:
                    tables_info.append(tables_dict[env_name][table_name])
                else:
                    raise SDKException("Subclient", "101",
                                       "Table {} not found in the environment {}".format(table_name, env_name))
            else:
                raise SDKException("Subclient", "101",
                                   "Environment {} not found in the list of discovered environments".format(env_name))

        if len(tables_info) != len(tables_list):
            raise SDKException("Subclient", "101", "All of the input tables were in the list of discovered tables")

        return tables_info

    def set_table_associations(self, tables_list: list[tuple[str, str]], plan_name: str = "") -> None:
        """Add table associations to a Dynamics 365 CRM client.

        This method associates specified tables with the Dynamics 365 CRM subclient content.
        Each table is identified by its name and the environment it belongs to.

        Args:
            tables_list: A list of tuples, where each tuple contains:
                - table_name (str): The name of the table to associate.
                - environment_name (str): The name of the environment the table belongs to.
                Example:
                    [("account", "testenv1"), ("note", "testenv2"), ("attachments", "testenv1")]
            plan_name: The name of the Dynamics 365 Plan to use for content association. Defaults to an empty string.

        Example:
            >>> tables = [("account", "testenv1"), ("note", "testenv2")]
            >>> subclient.set_table_associations(tables, plan_name="D365_Default_Plan")
            >>> print("Table associations set successfully.")

        #ai-gen-doc
        """

        plan_id = int(self._commcell_object.plans[plan_name.lower()])

        tables_info = self._table_association_info_json(tables_list=tables_list)

        _table_association_json = self._set_association_json(is_environment=False)
        _table_association_json["cloudAppAssociation"]["plan"] = {
            "planId": plan_id
        }
        _table_association_json["cloudAppAssociation"]["cloudAppDiscoverinfo"]["userAccounts"] = tables_info
        self._set_content_association(content_json=_table_association_json)

    def _environment_association_info_json(self, environments_name: list[str]) -> list[dict]:
        """Create the association JSON metadata for associating environments to a Dynamics 365 CRM client.

        Args:
            environments_name: List of environment names (as strings) to be associated with the content.

        Returns:
            A list of dictionaries containing metadata information for each environment,
            suitable for use in associating environments to the Dynamics 365 CRM client.

        Example:
            >>> env_names = ["Production", "Sandbox"]
            >>> env_info = subclient._environment_association_info_json(env_names)
            >>> print(env_info)
            [{'name': 'Production', ...}, {'name': 'Sandbox', ...}]
            # The returned list can be used for environment association operations.

        #ai-gen-doc
        """
        environments_info: list = list()
        _discovered_envs = self.discovered_environments

        if not bool(_discovered_envs):
            raise SDKException('Subclient', '101',
                               "Discovered Environments List is Empty")

        for environment in _discovered_envs:
            if environment["displayName"] in environments_name:
                _env_assoc_info = environment
                _env_assoc_info["user.userGUID"] = environment.get("user").get("userGUID")
                _env_assoc_info["rawCommonFlag"] = environment.get("commonFlags", 0)

                environments_info.append(_env_assoc_info)

        if len(environments_info) == 0:
            raise SDKException("Subclient", "101",
                               "None of the input environments were in the list of discovered environments")

        return environments_info

    def set_environment_associations(self, environments_name: list[str], plan_name: str = "") -> None:
        """Add environment associations to a Dynamics 365 CRM client.

        Associates the specified list of environment names with the content of the Dynamics 365 CRM client,
        using the provided Dynamics 365 Plan.

        Args:
            environments_name: List of environment names (as strings) to associate with the content.
                Example: ['testenv1', 'testenv2', 'testenv3']
            plan_name: Name of the Dynamics 365 Plan to use for content association. Defaults to an empty string.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> environments = ['prod_env', 'dev_env']
            >>> subclient.set_environment_associations(environments, plan_name='D365_Backup_Plan')
            >>> print("Environment associations set successfully.")

        #ai-gen-doc
        """
        environments_info: list = self._environment_association_info_json(environments_name=environments_name)

        if self._commcell_object.plans.has_plan(plan_name.lower()):
            plan_id = int(self._commcell_object.plans[plan_name.lower()])

        else:
            raise SDKException("Subclient", "101",
                               "Dynamics 365 Plan does not exist")

        _env_association_json = self._set_association_json(is_environment=True)
        _env_association_json["cloudAppAssociation"]["plan"] = {
            "planId": plan_id
        }
        _env_association_json["cloudAppAssociation"]["cloudAppDiscoverinfo"]["userAccounts"] = environments_info
        self._set_content_association(content_json=_env_association_json)

    def _json_for_backup_task(self, content_list: list, is_environment: bool = False, force_full_backup: bool = False) -> list:
        """Create the association JSON for backing up content in a Dynamics 365 subclient.

        This method generates the JSON structure required to initiate a backup task for the specified content
        in a Dynamics 365 subclient. The content can be either a list of environments or a list of tables
        (with their associated environments).

        Args:
            content_list:
                The list of content to be backed up.
                - If backing up tables: Each element should be a tuple of the form ("environment_name", "table_name").
                - If backing up environments: Each element should be a string representing the environment name.
            is_environment:
                If True, the content_list contains environment names. If False, it contains (environment, table) tuples.
            force_full_backup:
                If True, the backup will be forced as a full backup regardless of incremental settings.

        Returns:
            A list representing the JSON structure for backing up the specified content.

        Example:
            >>> # Back up specific tables
            >>> content = [("EnvA", "Table1"), ("EnvB", "Table2")]
            >>> backup_json = subclient._json_for_backup_task(content, is_environment=False)
            >>> print(backup_json)
            >>> # Back up entire environments
            >>> envs = ["EnvA", "EnvB"]
            >>> backup_json = subclient._json_for_backup_task(envs, is_environment=True, force_full_backup=True)
            >>> print(backup_json)

        #ai-gen-doc
        """
        _backup_task_json = self._backup_json('Full', False, '')
        backup_options = {
            'backupLevel': 2,  # Incremental
            'cloudAppOptions': {
            }
        }

        if len(content_list) > 0:
            _sub_client_content_json = self._backup_content_json(content_list=content_list, is_environment=is_environment)
            backup_options['cloudAppOptions']['userAccounts'] = _sub_client_content_json

        if force_full_backup is True:
            backup_options['cloudAppOptions']['forceFullBackup'] = True

        _backup_task_json['taskInfo']['subTasks'][0]['options']['backupOpts'] = backup_options
        return _backup_task_json

    def _backup_content_json(self, content_list: list, is_environment: bool = False) -> list:
        """Generate metadata JSON for backing up content in a Dynamics 365 subclient.

        This method constructs the metadata required to back up specified content for a Dynamics 365 subclient.
        The content can be either a list of tables (as tuples of environment and table names) or a list of environment names,
        depending on the value of `is_environment`.

        Args:
            content_list:
                The list of content to be backed up.
                - If backing up tables, each element should be a tuple: (environment_name, table_name).
                - If backing up environments, each element should be a string representing the environment name.
            is_environment:
                If True, the content_list contains environment names (str).
                If False, the content_list contains tuples of (environment_name, table_name).

        Returns:
            A list representing the metadata JSON required for backing up the specified content.

        Example:
            >>> # Backing up tables
            >>> content = [("Env1", "TableA"), ("Env2", "TableB")]
            >>> metadata = subclient._backup_content_json(content)
            >>> print(metadata)
            >>>
            >>> # Backing up environments
            >>> envs = ["Env1", "Env2"]
            >>> metadata = subclient._backup_content_json(envs, is_environment=True)
            >>> print(metadata)

        #ai-gen-doc
        """
        _bkp_content_json = list()

        if is_environment is True:
            for environment in self.get_associated_environments(refresh=True):
                if environment["name"] in content_list:
                    _env_bkp_info = environment["userAccountInfo"]
                    _bkp_content_json.append(_env_bkp_info)

        elif is_environment is False:
            for _table in self.get_associated_tables(refresh=True):
                _table_name, _parent_env_name = _table["name"].lower(), _table["environment_name"].lower()
                try:
                    if (_parent_env_name, _table_name) in content_list:
                        _table_bkp_info = _table["userAccountInfo"]
                        _bkp_content_json.append(_table_bkp_info)
                except TypeError:
                    raise SDKException('Subclient', '101',
                                       "For backing up tables, content list should be a list of tuples")

        return _bkp_content_json

    def _run_backup(self, backup_content: list, is_environment: bool = False, force_full_backup: bool = False) -> 'Job':
        """Run a backup job for the specified content of a Dynamics 365 subclient.

        Args:
            backup_content:
                The list of content to be backed up.
                - If backing up tables, each element should be a tuple of the form ("environment_name", "table_name").
                - If backing up environments, each element should be a string representing the environment name.
            is_environment:
                If True, the content is treated as environment names. If False, content is treated as table tuples.
            force_full_backup:
                If True, forces a full backup regardless of the backup cycle.

        Returns:
            Job: An instance of the Job class representing the initiated backup job.

        Example:
            >>> # To back up specific tables:
            >>> tables = [("EnvA", "Table1"), ("EnvB", "Table2")]
            >>> job = subclient._run_backup(tables, is_environment=False)
            >>> print(f"Backup job ID: {job.job_id}")

            >>> # To back up entire environments:
            >>> environments = ["EnvA", "EnvB"]
            >>> job = subclient._run_backup(environments, is_environment=True)
            >>> print(f"Backup job ID: {job.job_id}")

        #ai-gen-doc
        """
        _backup_json = self._json_for_backup_task(content_list=backup_content, is_environment=is_environment, force_full_backup=force_full_backup)
        backup_endpoint = self._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request("POST", backup_endpoint, _backup_json)
        return self._process_backup_response(flag, response)

    def backup_tables(self, tables_list: list[tuple[str, str]], force_full_backup: bool = False) -> 'Job':
        """Run a backup job for the specified tables of a Dynamics 365 subclient.

        Args:
            tables_list: A list of tuples specifying the tables to be backed up. Each tuple should be of the form:
                (environment_name, table_name)
                - environment_name: The name of the Dynamics 365 environment containing the table.
                - table_name: The name of the table to back up.
                Example:
                    [("testenv1", "account"), ("testenv2", "note"), ("testenv1", "attachments")]
            force_full_backup: If True, forces a full backup of the specified tables. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the backup job for the specified tables.

        Example:
            >>> tables = [("testenv1", "account"), ("testenv2", "note")]
            >>> job = subclient.backup_tables(tables)
            >>> print(f"Backup job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        return self._run_backup(backup_content=tables_list, is_environment=False, force_full_backup=force_full_backup)

    def backup_environments(self, environments_list: List[str]) -> 'Job':
        """Run a backup operation for the specified Dynamics 365 environments in this subclient.

        Args:
            environments_list: List of environment names (as strings) to be backed up.
                Example:
                    ['testenv1', 'testenv2', 'testenv3']

        Returns:
            Job: An instance of the CVPySDK.Job class representing the backup job for the specified environments.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> job = subclient.backup_environments(['testenv1', 'testenv2'])
            >>> print(f"Backup job started with ID: {job.job_id}")
            >>> # The returned Job object can be used to monitor job status and progress

        #ai-gen-doc
        """
        return self._run_backup(backup_content=environments_list, is_environment=True)

    def launch_client_level_full_backup(self) -> 'Job':
        """Run a full backup for the Dynamics 365 subclient.

        Initiates a client-level full backup operation for the Dynamics 365 subclient and returns
        a Job object representing the backup job.

        Returns:
            Job: An instance of the CVPySDK.Job class representing the initiated backup job.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> backup_job = subclient.launch_client_level_full_backup()
            >>> print(f"Backup job ID: {backup_job.job_id}")

        #ai-gen-doc
        """
        return self._run_backup(backup_content=[], is_environment=False, force_full_backup=True)

    def _restore_content_json(self) -> dict:
        """Generate the JSON payload required to restore content for a Dynamics 365 subclient.

        Returns:
            dict: A dictionary representing the JSON structure to be used for running a restore task.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> restore_json = subclient._restore_content_json()
            >>> print(restore_json)
            >>> # Use the returned JSON to initiate a restore operation

        #ai-gen-doc
        """
        _restore_task_json = {
            "taskInfo": {
                "associations": [self._subclient_properties['subClientEntity']],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 3,
                            "operationType": 1001
                        },
                        "options": {
                            "restoreOptions": {
                                "browseOption": {
                                    "timeRange": {}
                                },
                                "commonOptions": {
                                    "skip": True,
                                    "overwriteFiles": False,
                                    "unconditionalOverwrite": False
                                },
                                "destination": {
                                    "destAppId": self._app_id,
                                    "inPlace": True,
                                    "destClient": {
                                        "clientId": int(self._client_object.client_id),
                                        "clientName": self._client_object.client_name
                                    },
                                    "destPath": []
                                },
                                "fileOption": {
                                    "sourceItem": list()
                                },
                                "cloudAppsRestoreOptions": {
                                    "instanceType": self._instance_type,
                                    "d365RestoreOptions": {
                                        "restoreAllMatching": False,
                                        "restoreToDynamics365": True,
                                        "overWriteItems": False,
                                        "destLocation": "",
                                        "restoreUsingFindQuery": False
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
        return _restore_task_json

    def _get_restore_item_path(self, content_list: list, is_environment: bool = False) -> list:
        """Generate the complete restore path(s) for the specified MSDynamics365 content.

        Depending on the type of content, this method constructs the appropriate restore path(s) for use in a restore job.

        Args:
            content_list:
                If `is_environment` is True, a list of environment display names (str), all in lowercase.
                If `is_environment` is False, a list of tuples, each containing (environment_name, table_name).
                Example for tables:
                    [("testenv1", "account"), ("testenv2", "note"), ("testenv1", "attachments")]
            is_environment:
                Whether the content_list represents environments (True) or tables (False). Defaults to False.

        Returns:
            List of strings representing the complete restore path(s) for the specified content.

        Example:
            >>> # For restoring environments
            >>> env_paths = subclient._get_restore_item_path(['testenv1', 'testenv2'], is_environment=True)
            >>> print(env_paths)
            ['testenv1', 'testenv2']

            >>> # For restoring tables
            >>> table_paths = subclient._get_restore_item_path([('testenv1', 'account'), ('testenv2', 'note')])
            >>> print(table_paths)
            ['testenv1/account', 'testenv2/note']

        #ai-gen-doc
        """
        __restore_content_list = list()

        if is_environment is True:
            for environment in self.get_associated_environments(refresh=True):
                if environment["name"] in content_list:
                    _restore_id = environment["id"]
                    __restore_content_list.append(_restore_id)

        elif is_environment is False:
            for _table in self.get_associated_tables(refresh=True):
                _table_name, _parent_env_name = _table["name"].lower(), _table["environment_name"].lower()

                try:
                    if (_parent_env_name, _table_name) in content_list:
                        _id = _table.get("userAccountInfo").get("smtpAddress").split('/')
                        _table_id = _id[-1]
                        _env_id = _id[-2]
                        _restore_id = f"{_env_id}/{_table_id}"
                        __restore_content_list.append(_restore_id)

                except TypeError:
                    raise SDKException('Subclient', '101',
                                       "For restoring the tables, content list should be a list of tuples")
        __restore_content_list = list(
            map(lambda _restore_id: f"/tenant/{_restore_id}", __restore_content_list)
        )

        return __restore_content_list

    def _prepare_restore_json(
        self,
        restore_content: list,
        restore_path: list = None,
        overwrite: bool = True,
        job_id: int = None,
        is_environment: bool = False,
        is_out_of_place_restore: bool = False,
        destination_environment: str = str()
    ) -> dict:
        """Prepare the JSON (Python dict) payload for an in-place or out-of-place restore operation.

        This method constructs the restore request dictionary based on the provided content, restore paths,
        and restore options for MSDynamics365Subclient. It supports both environment-level and table-level restores,
        as well as out-of-place restores to a different environment.

        Args:
            restore_content: List of content items to restore. For environment restores, provide a list of environment
                display names (as lowercase strings). For table restores, provide a list of tuples in the form
                (environment_name, table_name).
                Example for tables:
                    [("testenv1", "account"), ("testenv2", "note"), ("testenv1", "attachments")]
            restore_path: Optional list of item paths to restore. If provided, these paths are used instead of restore_content.
                Paths are typically obtained from a browse operation.
            overwrite: Whether to overwrite existing content during restore. Defaults to True.
            job_id: Optional job ID for point-in-time restores.
            is_environment: Set to True if restoring environments; False if restoring tables. Defaults to False.
            is_out_of_place_restore: Set to True to perform an out-of-place restore to a different environment.
            destination_environment: Name of the destination environment for out-of-place restores.

        Returns:
            dict: A Python dictionary representing the restore request payload.

        Example:
            >>> # Restore specific tables to the original environment
            >>> restore_content = [("testenv1", "account"), ("testenv2", "note")]
            >>> restore_json = subclient._prepare_restore_json(restore_content)
            >>> print(restore_json)
            >>> # Restore an entire environment out-of-place
            >>> restore_content = ["testenv1"]
            >>> restore_json = subclient._prepare_restore_json(
            ...     restore_content,
            ...     is_environment=True,
            ...     is_out_of_place_restore=True,
            ...     destination_environment="prod_env"
            ... )
            >>> print(restore_json)

        #ai-gen-doc
        """
        _restore_content_json = self._restore_content_json()
        if restore_path is None:
            restore_path = self._get_restore_item_path(content_list=restore_content, is_environment=is_environment)

        _restore_content_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"][
            "sourceItem"] = restore_path

        if job_id is not None:
            _job = self._commcell_object.job_controller.get(job_id)
            _restore_content_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["browseOption"]["timeRange"][
                "toTime"] = _job.end_timestamp

        if overwrite is True:
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["commonOptions"]["overwriteFiles"] = True
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["commonOptions"][
                "skip"] = False
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["commonOptions"][
                "unconditionalOverwrite"] = True
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["cloudAppsRestoreOptions"] \
                ["d365RestoreOptions"]["overWriteItems"] = True

        if is_out_of_place_restore:
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["destination"]["destPath"] = [destination_environment]
            _instance_id = self._get_environment_id_for_oop_restore(environment_name=destination_environment)
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["cloudAppsRestoreOptions"] \
                ["d365RestoreOptions"]["destLocation"] = _instance_id
            _restore_content_json["taskInfo"]["subTasks"][0]["options"] \
                ["restoreOptions"]["destination"]["inPlace"] = False

        return _restore_content_json

    def restore_in_place(
            self,
            restore_content: Optional[list] = None,
            restore_path: Optional[list] = None,
            is_environment: bool = False,
            overwrite: bool = True,
            job_id: Optional[int] = None
        ) -> 'Job':
        """Run an in-place restore for the specified Microsoft Dynamics 365 content.

        This method initiates an in-place restore operation for the provided content or paths.
        The content to restore can be specified either as a list of environment names (for environment restores)
        or as a list of (environment_name, table_name) tuples (for table restores). Alternatively, you can provide
        a list of restore paths obtained from a browse operation.

        Args:
            restore_content:
                The content to restore. If restoring environments, provide a list of environment display names (str, lowercase).
                Example: ['testenv1', 'testenv2']
                If restoring tables, provide a list of (environment_name, table_name) tuples.
                Example: [('testenv1', 'account'), ('testenv2', 'note')]
            restore_path:
                List of item paths to restore, as returned by a browse operation. Use this instead of restore_content if available.
            is_environment:
                Set to True if restoring environments; set to False if restoring tables. Default is False.
            overwrite:
                Whether to overwrite existing content during restore. Default is True.
            job_id:
                Optional job ID for point-in-time restores.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> # Restore environments by name
            >>> job = subclient.restore_in_place(restore_content=['testenv1', 'testenv2'], is_environment=True)
            >>> print(f"Restore job started with ID: {job.job_id}")

            >>> # Restore specific tables
            >>> tables = [('testenv1', 'account'), ('testenv2', 'note')]
            >>> job = subclient.restore_in_place(restore_content=tables)
            >>> print(f"Restore job started with ID: {job.job_id}")

            >>> # Restore using paths from a browse operation
            >>> paths = ['/Dynamics365/testenv1/account', '/Dynamics365/testenv2/note']
            >>> job = subclient.restore_in_place(restore_path=paths)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        if restore_content is None and restore_path is None:
            raise SDKException("Subclient", "101", "Need to have either of restore content or restore path")

        _restore_json = self._prepare_restore_json(
            restore_content=restore_content,
            restore_path=restore_path,
            is_environment=is_environment,
            job_id=job_id,
            overwrite=overwrite,
            is_out_of_place_restore=False)

        return self._process_restore_response(_restore_json)

    def launch_d365_licensing(self, run_for_all_clients: bool = False) -> None:
        """Initiate the Dynamics 365 Licensing API call.

        This method triggers the licensing process for Dynamics 365. By default, the licensing API call
        is executed only for the current client. If `run_for_all_clients` is set to True, the licensing
        process will be launched for all clients associated with this subclient.

        Args:
            run_for_all_clients: If True, the licensing API call is executed for all clients. If False,
                it runs only for the current client. Default is False.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> # Launch licensing for the current client only
            >>> subclient.launch_d365_licensing()
            >>> # Launch licensing for all clients
            >>> subclient.launch_d365_licensing(run_for_all_clients=True)

        #ai-gen-doc
        """

        _LAUNCH_LICENSING = self._services['LAUNCH_O365_LICENSING']

        request_json = {
            "subClient": {
                "clientId": int(self._client_object.client_id)
            },
            "runForAllClients": run_for_all_clients,
            "appType": 6
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', _LAUNCH_LICENSING, request_json
        )

        if flag:
            try:
                if response.json():
                    if response.json().get('resp', {}).get('errorCode', 0) != 0:
                        error_message = response.json()['errorMessage']
                        output_string = 'Failed to Launch Licensing Thread\nError: "{0}"'
                        raise SDKException('Subclient', '102', output_string.format(error_message))
                    else:
                        self.refresh()
            except ValueError:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_environment_id_for_oop_restore(self, environment_name: str) -> str:
        """Retrieve the environment ID for a specified environment name for Out of Place Restore operations.

        Args:
            environment_name: The name of the environment for which the environment ID is required.

        Returns:
            The unique environment ID corresponding to the provided environment name.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> env_id = subclient._get_environment_id_for_oop_restore("ProductionEnv")
            >>> print(f"Environment ID: {env_id}")

        #ai-gen-doc
        """
        for environment in self.discovered_environments:
            if environment['displayName'] == environment_name:
                _env_xml = environment.get("xmlGeneric")
                _env_json = json.loads(_env_xml)
                _env_id = _env_json.get("_instanceName")
        return _env_id

    def restore_out_of_place(
            self,
            restore_content: list = None,
            restore_path: list = None,
            is_environment: bool = False,
            overwrite: bool = True,
            job_id: int = None,
            destination_environment: str = str()
        ) -> 'Job':
        """Run an out-of-place restore for the specified MSDynamics365 content.

        This method initiates an out-of-place restore operation for the provided content or paths.
        The content can be a list of environment names (as strings) or a list of (environment, table) tuples.
        Alternatively, you can specify the restore paths directly.

        Args:
            restore_content: List of content to restore. If restoring environments, provide a list of environment names as lowercase strings (e.g., ['testenv1', 'testenv2']). If restoring tables, provide a list of (environment_name, table_name) tuples (e.g., [('testenv1', 'account'), ('testenv2', 'note')]).
            restore_path: List of item paths to restore, as returned by the browse operation. Used as an alternative to restore_content.
            is_environment: Set to True if restoring environments; False if restoring tables.
            overwrite: If True, existing content at the destination will be overwritten. If False, existing content will be skipped.
            job_id: Optional job ID for point-in-time restores.
            destination_environment: Name of the destination environment for the restore.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> # Restore environments 'testenv1' and 'testenv2' to a different environment
            >>> job = subclient.restore_out_of_place(
            ...     restore_content=['testenv1', 'testenv2'],
            ...     is_environment=True,
            ...     destination_environment='prod_env'
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

            >>> # Restore specific tables to a different environment
            >>> job = subclient.restore_out_of_place(
            ...     restore_content=[('testenv1', 'account'), ('testenv2', 'note')],
            ...     is_environment=False,
            ...     destination_environment='prod_env'
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        if restore_content is None and restore_path is None:
            raise SDKException("Subclient", "101", "Need to have either of restore content or restore path")

        _restore_json = self._prepare_restore_json(
            restore_content=restore_content,
            restore_path=restore_path,
            is_environment=is_environment,
            job_id=job_id,
            overwrite=overwrite,
            is_out_of_place_restore=True,
            destination_environment=destination_environment)

        return self._process_restore_response(_restore_json)

    def browse(self,
               browse_path: Optional[list[str]] = None,
               include_deleted_items: bool = False,
               till_time: int = -1) -> dict:
        """Browse the backed up content for a Dynamics 365 subclient.

        Args:
            browse_path: Optional list specifying the path to browse within the Dynamics 365 backup.
                Example: ["environment-name", "table-name"]
            include_deleted_items: Whether to include deleted items in the browse results. Defaults to False.
            till_time: Unix timestamp for point-in-time browse. Use -1 for the latest backup.

        Returns:
            A list containing the browse results for the specified path and options.

        Example:
            >>> # Browse a specific table in an environment
            >>> results = subclient.browse(["SalesEnv", "Accounts"])
            >>> print(results)
            >>>
            >>> # Browse including deleted items
            >>> deleted_results = subclient.browse(["SalesEnv", "Accounts"], include_deleted_items=True)
            >>> print(deleted_results)
            >>>
            >>> # Point-in-time browse
            >>> point_in_time_results = subclient.browse(["SalesEnv", "Accounts"], till_time=1680307200)
            >>> print(point_in_time_results)

        #ai-gen-doc
        """
        _parent_path = str()

        _environments = self._perform_browse(parent_path=_parent_path, till_time=till_time, item_type=2,
                                             include_deleted_items=include_deleted_items)
        _browse_response = copy.deepcopy(_environments)

        if browse_path:
            _item_type: int = 3
            for path in browse_path:
                _parent_path = self._get_guid_for_path(_browse_response, path)
                if not _parent_path:
                    raise SDKException('Subclient', '101',
                                       f"Path: {path} not found in browse content: {_browse_response}")
                _browse_response = self._perform_browse(parent_path=_parent_path, till_time=till_time,
                                                        item_type=_item_type,
                                                        include_deleted_items=include_deleted_items)
                _item_type += 1

        return _browse_response

    def _get_guid_for_path(self, browse_response: dict, path: str) -> str:
        """Retrieve the GUID associated with a specific path from a browse response.

        This method extracts the GUID corresponding to the provided path from the given
        browse response dictionary. The GUID can be used in subsequent browse or data
        retrieval requests within the MSDynamics365Subclient context.

        Args:
            browse_response: The dictionary response obtained from a browse query.
            path: The path (such as a table or entity name) for which the GUID is required.

        Returns:
            The GUID string corresponding to the specified path.

        Example:
            >>> # Assume 'browse_response' is the result of a browse operation for "d365-env"
            >>> guid = subclient._get_guid_for_path(browse_response, "Accounts")
            >>> print(f"GUID for Accounts: {guid}")
            >>> # The returned GUID can be used in further browse requests

        #ai-gen-doc
        """
        guid: str = str()
        for item in browse_response:
            if item.get("appSpecific").get("d365Item").get("displayName") == path:
                guid = item.get("cvObjectGuid")
        return guid

    def _perform_browse(self, parent_path: str = str(), till_time: int = -1, item_type: int = 2,
                        include_deleted_items: bool = False):
        """
            Perform a browse of the backed up content
            Arguments:
                parent_path         (str)   --      GUID for the parent path
                include_deleted_items
                                    (bool)  --      Whether to include deleted items in the browse response
                till_time           (int)   --      Time-stamp for point in time browse
                item_type           (int)   --      Item type to be browsed
        """
        _browse_default_params = self._get_dynamics365_browse_params(item_type=item_type)

        _query_params = _browse_default_params.get("query_params")
        _file_filter = _browse_default_params.get("file_filter")
        _sort_params = _browse_default_params.get("sort_param")
        _common_filters = _browse_default_params.get("common_filters")

        if parent_path:
            _parent_path_filter = {
                "field": "PARENT_GUID",
                "intraFieldOp": 0,
                "fieldValues": {
                    "values": [
                        f"{parent_path}"
                    ]
                }
            }
            _file_filter.append(_parent_path_filter)

        if till_time != -1:
            _backup_time_filter = {
                "field": "BACKUPTIME",
                "intraFieldOp": 0,
                "fieldValues": {
                    "values": [
                        "0",
                        f"{till_time}"
                    ]
                }
            }
            _file_filter.append(_backup_time_filter)

        if include_deleted_items:
            _common_filter = {
                "groupType": 0,
                "field": "CISTATE",
                "intraFieldOp": 0,
                "fieldValues": {
                    "values": [
                        "1",
                        "3333",
                        "3334",
                        "3335"
                    ]
                }
            }
            _common_filters[0] = _common_filter

        return self.do_web_search(query_params=_query_params, file_filter=_file_filter, sort_param=_sort_params,
                                  common_filters=_common_filters)

    def _get_dynamics365_browse_params(self, item_type: int = 2) -> dict:
        """Generate the default dictionary of browse parameters for a Dynamics 365 browse query.

        Args:
            item_type: The type of item to be browsed. Defaults to 2.

        Returns:
            A dictionary containing the default parameters for performing a Dynamics 365 browse operation.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> params = subclient._get_dynamics365_browse_params(item_type=3)
            >>> print(params)
            {'itemType': 3, ...}  # Example output structure

        #ai-gen-doc
        """
        _query_params: list = [
            {
                "param": "ENABLE_MIXEDVIEW",
                "value": "true"
            },
            {
                "param": "RESPONSE_FIELD_LIST",
                "value": "D365_ENTITY_DISP_NAME,D365_ENTITY_DISP_NAME,CONTENTID,CV_OBJECT_GUID,CV_TURBO_GUID,"
                         "PARENT_GUID,AFILEID,AFILEOFFSET,COMMCELLNO,APPID,D365_ID,D365_DISPLAYNAME,"
                         "FILE_CREATEDTIME,MODIFIEDTIME,BACKUPTIME,D365_OBJECT_TYPE,D365_CONTENTHASH,D365_FLAGS,"
                         "D365_ENTITYSET_ID,D365_ENTITYSET_NAME,D365_INSTANCE_ID,D365_INSTANCE_NAME,"
                         "D365_CREATEDBY_GUID,D365_CREATEDBY_NAME,D365_MODIFIEDBY_GUID,D365_MODIFIEDBY_NAME,"
                         "D365_OWNER_GUID,D365_OWNER_NAME,DATE_DELETED,CISTATE "
            },
            {
                "param": "COLLAPSE_FIELD",
                "value": "CV_OBJECT_GUID"
            }]

        _sort_params: list = [
            {
                "sortDirection": 0,
                "sortField": "D365_DISPLAYNAME"
            }
        ]

        _common_filters: list = [
            {
                "groupType": 0,
                "field": "CISTATE",
                "intraFieldOp": 0,
                "fieldValues": {
                    "values": [
                        "1"
                    ]
                }
            },
            {
                "field": "IS_VISIBLE",
                "intraFieldOpStr": "None",
                "intraFieldOp": 0,
                "fieldValues": {
                    "isMoniker": False,
                    "isRange": False,
                    "values": [
                        "true"
                    ]
                }
            }
        ]

        _file_filter: list = [
            {
                "field": "D365_OBJECT_TYPE",
                "intraFieldOp": 0,
                "fieldValues": {
                    "values": [
                        f"{item_type}"
                    ]
                }
            }
        ]
        return {"query_params": _query_params, "file_filter": _file_filter, "sort_param": _sort_params,
                "common_filters": _common_filters}

    @property
    def browse_item_type(self) -> dict[str, int]:
        """Get the Dynamics 365 item type associated with this subclient.

        Returns:
             Dictionary mapping item type names to their integer values.

        Example:
            >>> subclient = MSDynamics365Subclient()
            >>> item_type = subclient.browse_item_type
            >>> print(f"Dynamics 365 item type: {item_type}")
        #ai-gen-doc
        """
        _browse_item_type = {"environment": 2,
                             "table": 3,
                             "record": 4}
        return _browse_item_type