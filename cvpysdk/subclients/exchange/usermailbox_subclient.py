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

"""File for operating on a UserMailbox Subclient.

UsermailboxSubclient is the only class defined in this file.

UsermailboxSubclient:       Derived class from ExchangeMailboxSubclient Base class, representing a
                            UserMailbox subclient, and to perform operations on that subclient

UsermailboxSubclient:
======================

    _get_subclient_properties()         --  gets the properties of UserMailbox Subclient
    _get_subclient_properties_json()    --  gets the properties JSON of UserMailbox Subclient
    _get_discover_adgroups()            --  Get the discovered AD Groups
    _get_discover_users()               --  Get the discovered users
    _association_json_with_plan()       --  Create the Association JSON for
                                            associations using Exchange Plan
    _association_mailboxes_json()       --  Association for particular mailboxes
    _task_json_for_backup()             --  JSON for backup task for Exchange User mailbox Subclient
    _backup_generic_items_json()        --  JSON to backup generic items
    _search_user()                      --  Searches for the user in the discovered users list

Content Association Methods:
==============================

    set_user_assocaition()              --  Set exchange users association
    set_pst_association()               --  Create PST association for UserMailboxSubclient
    set_fs_association_for_pst()        --  Helper method to create pst association for
                                            PST Ingestion by FS association
    set_adgroup_associations()          --  Create Association for ADGroups
    set_o365group_asscoiations()        --  Create O365 group association

    delete_user_assocaition()           --  Delete User Association from content
    delete_o365group_association()      --  Delete Office 365 Group Association
    delete_database_assocaition()       --  Delete Exchange DB Association
    delete_adgroup_assocaition          --  Delete association for an AD Group


    enable_allusers_association()       --  Enable association for all mailboxes
    disable_allusers_association()      --  Disable All Users Association

    enable_auto_discover_association    --  Enable Association for Auto Discovered Content
                                            viz. All Public Folders/
                                                All Mailboxes/
                                                All Group Mailboxes
    delete_auto_discover_association    --  Delete Association for Auto Discovered Content
                                           `viz. All Public Folders/
                                                All Mailboxes/
                                                All Group Mailboxes
    enable_ews_support()                --  Enables EWS Support for backup for ON_PREM Mailboxes

Browse/ Restore/ Backup Methods:
==============================

    browse_mailboxes()                  --  Backup specific mailboxes
    backup_generic_items()              --  Backup Generic Items
                                            viz. All Public Folders/
                                                All User Mailboxes/
                                                All Group Mailboxes
    backup_mailboxes()                  --  Backup selected mailboxes
    restore_in_place()                  --  runs in-place restore for the subclient
    create_recovery_point()             --  Create a recovery point for a mailbox
    restore_in_place_syntex()           --  runs an in-place restore for the Syntex client
    find_mailbox()                      --  Performs search operation of a mailbox in browse



User Mailbox Subclient Instance Attributes:
==============================

    discover_users                          --  Dictionary of users discovered
    discover_databases                      --  Dictionary of databases discovered
    adgroups                                --  Dictionary of discovered AD Groups
    o365groups                              --  Dictionary of discovered Office 365 Groups
"""

from __future__ import unicode_literals

import datetime
import time
from typing import Any, Dict, List, Optional, Union, Tuple

from ...exception import SDKException
from ...job import Job
from ..exchsubclient import ExchangeSubclient
from .constants import ExchangeConstants

class UsermailboxSubclient(ExchangeSubclient):
    """
    UsermailboxSubclient provides management and operations for user mailbox subclients
    within an Exchange backup environment.

    This class extends the ExchangeSubclient base class to support discovery, association,
    backup, and restore operations specifically for user mailboxes, databases, Active Directory groups,
    and Office 365 groups. It offers a comprehensive interface for configuring policies, managing
    associations, performing mailbox searches, and handling backup and restore tasks.

    Key Features:
        - Initialization and configuration of user mailbox subclients
        - Policy and association management for mailboxes, databases, AD groups, and O365 groups
        - Discovery of users, databases, AD groups, and O365 groups
        - Search and browse capabilities for mailboxes and users
        - Backup operations for mailboxes and generic items
        - Restore operations including in-place restore and recovery point creation
        - Enable/disable associations and auto-discover features
        - Support for EWS (Exchange Web Services)
        - Refresh and update subclient state

    Properties:
        - discover_users: Provides discovered user mailboxes
        - discover_databases: Provides discovered databases
        - discover_adgroups: Provides discovered AD groups
        - users: Returns associated users
        - databases: Returns associated databases
        - adgroups: Returns associated AD groups
        - o365groups: Returns associated Office 365 groups

    #ai-gen-doc
    """

    def __init__(self, backupset_object: object, subclient_name: str, subclient_id: int = None) -> None:
        """Initialize a UsermailboxSubclient instance for the specified UserMailbox subclient.

        Args:
            backupset_object: Instance of the backupset class associated with this subclient.
            subclient_name: Name of the UserMailbox subclient.
            subclient_id: Optional; ID of the subclient. If not provided, it will be determined automatically.

        Example:
            >>> backupset = Backupset(commcell_object, 'Exchange', 'UserMailbox')
            >>> subclient = UsermailboxSubclient(backupset, 'MailboxSubclient1')
            >>> print(f"Subclient created: {subclient}")

        #ai-gen-doc
        """
        super(UsermailboxSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._client_object = self._instance_object._agent_object._client_object
        self._SET_EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'SET_EMAIL_POLICY_ASSOCIATIONS']
        self._SEARCH = (self._commcell_object._services['EMAIL_DISCOVERY'] %
                        (int(self._backupset_object.backupset_id), 'User'))

        self.refresh()

    def _policy_json(self, configuration_policy: Union[str, object], policy_type: int) -> dict[
        str, int | dict[str, int] | dict[str, dict[str, int]] | dict[str, int | Any]]:
        """Generate a policy JSON structure based on the configuration policy and type.

        This method creates a JSON payload suitable for sending to the POST Subclient API,
        using either the name of a configuration policy or an instance of a configuration policy class,
        along with the specified policy type.

        Args:
            configuration_policy: The configuration policy, specified either as a string (policy name)
                or as an object representing the configuration policy.
            policy_type: The type of configuration policy as an integer.

        Returns:
            A list containing the JSON structure appropriate for the agent to send to the POST Subclient API.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> # Using policy name
            >>> json_payload = subclient._policy_json("DefaultPolicy", 1)
            >>> print(json_payload)
            >>> # Using policy object
            >>> policy_obj = ConfigurationPolicy("CustomPolicy")
            >>> json_payload = subclient._policy_json(policy_obj, 2)
            >>> print(json_payload)

        #ai-gen-doc
        """

        from ...policies.configuration_policies import ConfigurationPolicy
        if not (isinstance(configuration_policy, (str, ConfigurationPolicy))):
            raise SDKException('Subclient', '101')

        if isinstance(configuration_policy, str):
            configuration_policy = ConfigurationPolicy(
                self._commcell_object, configuration_policy)

        policy_json = {
            "policyType": 1,
            "flags": 0,
            "agentType": {
                "appTypeId": 137
            },
            "detail": {
                "emailPolicy": {
                    "emailPolicyType": policy_type
                }
            },
            "policyEntity": {
                "policyId": int(configuration_policy.configuration_policy_id),
                "policyName": configuration_policy.configuration_policy_name
            }
        }

        return policy_json

    def _association_json(self, subclient_content: dict, is_o365group: bool = False) -> dict:
        """Construct the association JSON for creating an association in a UserMailbox Subclient.

        Args:
            subclient_content: Dictionary containing the users or policies to add to the subclient.
                For regular user mailboxes, this should include user and policy information.
                For Office 365 groups, this should include only policy information.
                Example:
                    {
                        'archive_policy': "CIPLAN Archiving policy",
                        'cleanup_policy': 'CIPLAN Clean-up policy',
                        'retention_policy': 'CIPLAN Retention policy'
                    }
            is_o365group: If True, indicates the association is for an Office 365 group. Defaults to False.

        Returns:
            Dictionary representing the association JSON request to be passed to the API.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> content = {
            ...     'archive_policy': "CIPLAN Archiving policy",
            ...     'cleanup_policy': 'CIPLAN Clean-up policy',
            ...     'retention_policy': 'CIPLAN Retention policy'
            ... }
            >>> association_json = subclient._association_json(content)
            >>> print(association_json)
            # Output will be a dictionary formatted for the API association request

        #ai-gen-doc
        """
        policy_types = {
            "archive_policy": 1,
            "cleanup_policy": 2,
            "retention_policy": 3
        }

        email_policies = []

        if 'archive_policy' in subclient_content:
            email_policies.append(self._policy_json(subclient_content.get(
                'archive_policy'), policy_types['archive_policy']))
        if 'cleanup_policy' in subclient_content:
            email_policies.append(self._policy_json(subclient_content.get(
                'cleanup_policy'), policy_types['cleanup_policy']))
        if 'retention_policy' in subclient_content:
            email_policies.append(self._policy_json(subclient_content.get(
                'retention_policy'), policy_types['retention_policy']))

        associations_json = {
            "emailAssociation": {
                "advanceOptions": {
                    "enableAutoDiscovery": subclient_content.get("is_auto_discover_user",
                                                                 is_o365group)
                },
                "subclientEntity": self._subClientEntity,
                "policies": {
                    "emailPolicies": email_policies
                }
            }
        }

        return associations_json

    def _association_json_with_plan(self, plan_details: Dict[str, Any]) -> dict:
        """Construct the association JSON payload with plan details for UserMailbox Subclient.

        This method prepares a dictionary representing the association request,
        which can be used to associate a UserMailbox Subclient with a specific plan.

        Args:
            plan_details: A dictionary containing plan information.
                Expected keys:
                    - 'plan_name' (str): The name of the plan.
                    - 'plan_id' (Optional[int]): The ID of the plan, or None if not specified.

        Returns:
            dict: The association JSON request payload to be sent to the API.

        Example:
            >>> plan_info = {'plan_name': 'ExchangePlan', 'plan_id': 1234}
            >>> assoc_json = subclient._association_json_with_plan(plan_info)
            >>> print(assoc_json)
            {'plan': {'planName': 'ExchangePlan', 'planId': 1234}}
        #ai-gen-doc
        """

        try:
            if not self._commcell_object.plans.has_plan(plan_details['plan_name']):
                raise SDKException('Subclient', '102',
                                   'Plan Name {} not found'.format(plan_details['plan_name']))
            if 'plan_id' not in plan_details or plan_details['plan_id'] is None:
                plan_id = self._commcell_object.plans[plan_details['plan_name'].lower()]
            else:
                plan_id = plan_details['plan_id']

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        plan_details = {
            'planId': int(plan_id)
        }

        association_json = {
            "emailAssociation": {
                "subclientEntity": self._subClientEntity,
                "plan": plan_details
            }
        }
        return association_json

    def _association_mailboxes_json(self, mailbox_alias_names: list) -> list:
        """Generate the JSON structure for associating mailboxes by alias names.

        Args:
            mailbox_alias_names: A list of mailbox alias names to be included for backup.
                Example:
                    ['aj', 'tkumar']

        Returns:
            A list containing the required details of the mailboxes to be backed up, formatted as JSON-compatible dictionaries.

        Example:
            >>> mailbox_aliases = ['aj', 'tkumar']
            >>> mailboxes_json = subclient._association_mailboxes_json(mailbox_aliases)
            >>> print(mailboxes_json)
            [{'aliasName': 'aj'}, {'aliasName': 'tkumar'}]

        #ai-gen-doc
        """
        mailboxes_json = []
        mailbox_alias_names = set(mailbox_alias_names)
        associated_mailboxes = self._users + self._o365groups

        for user in associated_mailboxes:
            if user['alias_name'] in mailbox_alias_names:
                mailbox_info = {
                    "aliasName": user["alias_name"],
                    "mailBoxType": user['mailbox_type'],
                    "databaseName": user['database_name'],
                    "displayName": user['display_name'],
                    "smtpAddress": user['smtp_address'],
                    "isAutoDiscoveredUser": True if user['is_auto_discover_user'].lower() == 'true' else False,
                    "msExchRecipientTypeDetails": user['mailbox_type'],
                    "exchangeVersion": user['exchange_version'],
                    "exchangeServer": user['exchange_server'],
                    "lastArchiveJobRanTime": user['last_archive_job_ran_time'],
                    "user": {
                        "userGUID": user['user_guid']
                    }
                }
                mailboxes_json.append(mailbox_info)
        return mailboxes_json

    def _task_json_for_backup(self, mailbox_alias_names: list, **kwargs: dict) -> dict:
        """Generate the task JSON required for backing up specified mailboxes.

        Args:
            mailbox_alias_names: List of alias names for the mailboxes to be backed up.
                Example:
                    ['aj', 'tkumar']
            **kwargs: Additional parameters for the backup task.
                items_selection_option (str): Item Selection Option (e.g., "7" for selecting recently backed up entities).

        Returns:
            dict: The task JSON dictionary to be passed to the backup API.

        Example:
            >>> mailbox_aliases = ['aj', 'tkumar']
            >>> task_json = subclient._task_json_for_backup(mailbox_aliases, items_selection_option="7")
            >>> print(task_json)
            # The returned dictionary can be used as the payload for the backup API.

        #ai-gen-doc
        """
        common_backup_options = None
        items_selection_option = kwargs.get('items_selection_option', '')
        if items_selection_option != '':
            common_backup_options = {'itemsSelectionOption': items_selection_option}
        task_json = self._backup_json(backup_level='INCREMENTAL', incremental_backup=False,incremental_level='BEFORE_SYNTH',common_backup_options=common_backup_options)
        if mailbox_alias_names != None:
            associated_mailboxes_json = self._association_mailboxes_json(mailbox_alias_names)
            backup_options = {
                'backupLevel': 2,  # Incremental
                'incLevel': 1,
                'exchOnePassOptions': {
                    'mailBoxes': associated_mailboxes_json
                }
            }
            data_options = {
                "useCatalogServer": False,
                "followMountPoints": True,
                "enforceTransactionLogUsage": False,
                "skipConsistencyCheck": True,
                "createNewIndex": False
            }
            task_json['taskInfo']['subTasks'][0]['options']['backupOpts'] = backup_options
            task_json['taskInfo']['subTasks'][0]['options']['dataOpt'] = data_options
        return task_json

    def _set_association_request(self, associations_json: dict) -> tuple[str, str]:
        """Send a POST request to the emailAssociation API to set mailbox associations.

        Args:
            associations_json: Dictionary containing the request payload for the association.

        Returns:
            A tuple containing:
                - error code received in the response (str)
                - error message received (str)

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> associations = {
            ...     "mailboxList": ["user1@example.com", "user2@example.com"],
            ...     "operationType": 1
            ... }
            >>> error_code, error_message = subclient._set_association_request(associations)
            >>> print(f"Error code: {error_code}, Message: {error_message}")

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._SET_EMAIL_POLICY_ASSOCIATIONS, associations_json
        )

        if flag:
            try:
                if response.json():
                    if response.json()['resp']['errorCode'] != 0:
                        error_message = response.json()['errorMessage']
                        output_string = 'Failed to create assocaition\nError: "{0}"'
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

    def _update_association_request(self, associations_json: dict) -> tuple[str, str]:
        """Update mailbox associations using the EmailAssociation PUT API.

        This method sends a PUT request to update mailbox associations with the provided JSON payload.
        It returns the error code and error message from the API response.

        Args:
            associations_json: Dictionary containing the request payload for updating associations.

        Returns:
            A tuple containing:
                str: The error code received in the response.
                str: The error message received.

        Raises:
            SDKException: If the response is empty or the API call is not successful.

        Example:
            >>> payload = {
            ...     "associations": [
            ...         {"mailboxName": "user1@example.com", "action": "add"},
            ...         {"mailboxName": "user2@example.com", "action": "remove"}
            ...     ]
            ... }
            >>> error_code, error_message = subclient._update_association_request(payload)
            >>> print(f"Error code: {error_code}, Message: {error_message}")

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._SET_EMAIL_POLICY_ASSOCIATIONS, associations_json
        )

        if flag:
            try:
                if response.json():
                    if response.json()['resp']['errorCode'] != 0:
                        error_message = response.json()['errorMessage']
                        output_string = 'Failed to create assocaition\nError: "{0}"'
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

    def _get_discover_users(self, use_without_refresh_url: bool = False, retry_attempts: int = 0) -> list:
        """Retrieve the list of discovered users associated with the subclient.

        Args:
            use_without_refresh_url: If True, performs discovery without refreshing the cache.
            retry_attempts: Number of retry attempts for the discovery operation.

        Returns:
            list: A list of discovered users associated with the subclient.

        Example:
            >>> users = subclient._get_discover_users()
            >>> print(f"Discovered users: {users}")
            >>> # To perform discovery without refreshing cache and with retries:
            >>> users = subclient._get_discover_users(use_without_refresh_url=True, retry_attempts=2)

        #ai-gen-doc
        """
        self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY'] % (
            int(self._backupset_object.backupset_id), 'User'
        )

        if use_without_refresh_url:
            self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY_WITHOUT_REFRESH'] % (
                int(self._backupset_object.backupset_id), 'User'
            )
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._DISCOVERY)

        if flag:
            if response and response.json():
                discover_content = response.json()

                _error_code = discover_content.get('resp', {}).get('errorCode', 0)
                if _error_code == 469762468 or _error_code == 469762470:
                    # if discover_content.get('resp', {}).get('errorCode', 0) == 469762468:
                    time.sleep(60)  # the results might take some time depending on domains
                    if retry_attempts > 10:
                        raise SDKException('Subclient', '102', 'Failed to perform discovery.')

                    return self._get_discover_users(use_without_refresh_url=True,
                                                    retry_attempts=retry_attempts + 1)

                if 'discoverInfo' in discover_content.keys():
                    if 'mailBoxes' in discover_content['discoverInfo']:
                        self._discover_users = discover_content['discoverInfo']['mailBoxes']

                        return self._discover_users
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _search_user(self, user: str, retry_attempts: int = 0) -> list:
        """Search for a user in the discovered users list.

        Args:
            user: The alias name or SMTP address of the user to search for.
            retry_attempts: The number of retry attempts to perform if the search fails. Defaults to 0.

        Returns:
            A list of discovered users matching the search criteria.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> matching_users = subclient._search_user('john.doe@example.com')
            >>> print(matching_users)
            ['john.doe@example.com', 'jdoe@example.com']

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', f"{self._SEARCH}&search={user}")

        if flag:
            if response and response.json():
                search_content = response.json()

                _error_code = search_content.get('resp', {}).get('errorCode', 0)
                if _error_code == 469762468 or _error_code == 469762470:
                    # if search_content.get('resp', {}).get('errorCode', 0) == 469762468:
                    time.sleep(10)  # the results might take some time depending on domains
                    if retry_attempts > 10:
                        raise SDKException('Subclient', '102', 'Failed to perform search and discovery.')
                    return self._search_user(user, retry_attempts=retry_attempts + 1)

                return search_content.get('discoverInfo', {}).get('mailBoxes', [])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_discover_database(self) -> list:
        """Retrieve the list of discovered databases associated with the subclient.

        Returns:
            list: A list containing the names or identifiers of databases discovered for this subclient.

        Example:
            >>> databases = subclient._get_discover_database()
            >>> print(f"Discovered databases: {databases}")

        #ai-gen-doc
        """
        self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY'] % (
            int(self._backupset_object.backupset_id), 'Database'
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._DISCOVERY)

        if flag:
            discover_content = response.json()
            if 'discoverInfo' in discover_content.keys():
                if 'databases' in discover_content['discoverInfo']:
                    discover_content = discover_content['discoverInfo']['databases']
                return discover_content

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_discover_adgroups(self) -> list:
        """Retrieve the list of discovered Active Directory groups associated with the subclient.

        Returns:
            list: A list containing the discovered AD groups for this subclient.

        Example:
            >>> adgroups = subclient._get_discover_adgroups()
            >>> print(f"Discovered AD groups: {adgroups}")

        #ai-gen-doc
        """
        self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY'] % (
            int(self._backupset_object.backupset_id), 'AD Group'
        )
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._DISCOVERY)

        if flag:
            discover_content = response.json()
            if 'discoverInfo' in discover_content.keys():

                if 'adGroups' in discover_content['discoverInfo']:
                    discover_content = discover_content['discoverInfo']['adGroups']

                return discover_content

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_user_assocaitions(self) -> tuple[
        list[dict[str | Any, str | None | Any]], list[dict[str | Any, str | None | Any]]]:
        """Retrieve the list of users and groups associated with the subclient.

        Returns:
            list: A list containing the users and groups that are currently associated with this subclient.

        Example:
            >>> associations = subclient._get_user_assocaitions()
            >>> print(f"Associated users/groups: {associations}")

        #ai-gen-doc
        """
        users = []
        groups = []

        self._EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
                                              'GET_EMAIL_POLICY_ASSOCIATIONS'] % (self.subclient_id, 'User')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._EMAIL_POLICY_ASSOCIATIONS
        )

        if flag:
            subclient_content = response.json()

            if 'associations' in subclient_content:
                children = subclient_content['associations']

                for child in children:
                    plan_name = None
                    plan_id = None
                    display_name = str(child['userMailBoxInfo']['displayName'])
                    alias_name = str(child['userMailBoxInfo']['aliasName'])
                    smtp_address = str(child['userMailBoxInfo']['smtpAdrress'])
                    database_name = str(child['userMailBoxInfo']['databaseName'])
                    exchange_server = str(child['userMailBoxInfo']['exchangeServer'])
                    user_guid = str(child['userMailBoxInfo']['user']['userGUID'])
                    is_auto_discover_user = str(child['userMailBoxInfo']['isAutoDiscoveredUser'])
                    mailbox_type = int(child['userMailBoxInfo']['msExchRecipientTypeDetails'])
                    exchange_version = int(child['userMailBoxInfo']['exchangeVersion'])
                    last_archive_job_ran_time = child['userMailBoxInfo']['lastArchiveJobRanTime']

                    if 'plan' in child:
                        plan_name = child.get('plan').get('planName')
                        plan_id = child.get('plan').get('planId')

                    temp_dict = {
                        'display_name': display_name,
                        'alias_name': alias_name,
                        'smtp_address': smtp_address,
                        'database_name': database_name,
                        'exchange_server': exchange_server,
                        'user_guid': user_guid,
                        'is_auto_discover_user': is_auto_discover_user,
                        'plan_name': plan_name,
                        'plan_id': plan_id,
                        'mailbox_type': mailbox_type,
                        'exchange_version': exchange_version,
                        'last_archive_job_ran_time': last_archive_job_ran_time
                    }
                    if int(child['userMailBoxInfo']['msExchRecipientTypeDetails']) == 36:
                        groups.append(temp_dict)
                    else:
                        users.append(temp_dict)

        return users, groups

    def _get_database_associations(self) -> list:
        """Retrieve the list of databases associated with this subclient.

        Returns:
            list: A list containing the names or identifiers of databases associated with the subclient.

        Example:
            >>> associations = subclient._get_database_associations()
            >>> print(f"Databases associated with subclient: {associations}")

        #ai-gen-doc
        """
        databases = []

        self._EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
                                              'GET_EMAIL_POLICY_ASSOCIATIONS'] % (self.subclient_id, 'Database')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._EMAIL_POLICY_ASSOCIATIONS
        )

        if flag:
            subclient_content = response.json()

            if 'associations' in subclient_content:
                children = subclient_content['associations']

                for child in children:
                    database_name = str(child['databaseInfo']['databaseName'])
                    exchange_server = str(child['databaseInfo']['exchangeServer'])
                    archive_policy = None
                    cleanup_policy = None
                    retention_policy = None
                    is_auto_discover_user = str(child['additionalOptions']['enableAutoDiscovery'])

                    for policy in child['policies']['emailPolicies']:
                        if policy['detail']['emailPolicy']['emailPolicyType'] == 1:
                            archive_policy = str(policy['policyEntity']['policyName'])
                        elif policy['detail']['emailPolicy']['emailPolicyType'] == 2:
                            cleanup_policy = str(policy['policyEntity']['policyName'])
                        elif policy['detail']['emailPolicy']['emailPolicyType'] == 3:
                            retention_policy = str(policy['policyEntity']['policyName'])

                    temp_dict = {
                        'database_name': database_name,
                        'exchange_server': exchange_server,
                        'is_auto_discover_user': is_auto_discover_user,
                        'archive_policy': archive_policy,
                        'cleanup_policy': cleanup_policy,
                        'retention_policy': retention_policy
                    }

                    databases.append(temp_dict)

        return databases

    def _get_adgroup_assocaitions(self) -> list:
        """Retrieve the list of Active Directory groups associated with this subclient.

        Returns:
            list: A list containing the names or identifiers of AD groups linked to the subclient.

        Example:
            >>> adgroups = subclient._get_adgroup_assocaitions()
            >>> print(f"Associated AD groups: {adgroups}")

        #ai-gen-doc
        """
        adgroups = []

        self._EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
                                              'GET_EMAIL_POLICY_ASSOCIATIONS'] % (self.subclient_id, 'AD Group')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._EMAIL_POLICY_ASSOCIATIONS
        )

        if flag:
            subclient_content = response.json()

            if 'associations' in subclient_content:
                children = subclient_content['associations']

                for child in children:
                    planName = None
                    planId = None
                    adgroup_name = str(child['adGroupsInfo']['adGroupName'])
                    is_auto_discover_user = str(child['additionalOptions']['enableAutoDiscovery'])

                    if 'plan' in child:
                        planName = child['plan']['planName']
                        planId = child['plan']['planId']
                    else:
                        raise Exception('Plan details are not available')

                    temp_dict = {
                        'adgroup_name': adgroup_name,
                        'is_auto_discover_user': is_auto_discover_user,
                        'planName': planName,
                        'planId': planId
                    }

                    adgroups.append(temp_dict)

        return adgroups

    def _backup_generic_items_json(self, subclient_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate the JSON payload for backing up generic items in an Exchange Online client.

        Args:
            subclient_content: A list of dictionaries, each specifying an item to be backed up.
                Each dictionary should contain:
                    - "associationName": The name of the item or group (e.g., "All Public Folders").
                    - "associationType": The type identifier for the association (e.g., 12).

                Example:
                    subclient_content = [
                        {
                            "associationName": "All Public Folders",
                            "associationType": 12
                        },
                        {
                            "associationName": "All Users",
                            "associationType": 12
                        }
                    ]

        Returns:
            A dictionary representing the JSON payload required to create a backup task for the specified items.

        Example:
            >>> subclient_content = [
            ...     {"associationName": "All Public Folders", "associationType": 12},
            ...     {"associationName": "All Users", "associationType": 12}
            ... ]
            >>> backup_json = usermailbox_subclient._backup_generic_items_json(subclient_content)
            >>> print(backup_json)
            >>> # The returned dictionary can be used to initiate a backup task

        #ai-gen-doc
        """

        task_dict = {
            "taskInfo": {
                "associations": [
                    self._subClientEntity
                ],
                "task": {
                    "taskType": 1
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 2,
                            "operationType": 2
                        },
                        "options": {
                            "backupOpts": {
                                "backupLevel": 1,
                                "incLevel": 1,
                                "exchOnePassOptions": {
                                    "genericAssociations": [
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }
        task_dict["taskInfo"]["subTasks"][0]["options"]["backupOpts"]["exchOnePassOptions"][
            "genericAssociations"] = subclient_content
        return task_dict

    @property
    def discover_users(self) -> list:
        """Get the list of discovered users for the UserMailbox subclient.

        Returns:
            list: A list containing the discovered user mailboxes associated with this subclient.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> users = subclient.discover_users
            >>> print(f"Discovered users: {users}")
            >>> # The returned list contains user mailbox identifiers or details

        #ai-gen-doc
        """
        return self._discover_users

    @property
    def discover_databases(self) -> List[Dict[str, Any]]:
        """Get the list of discovered databases for the UserMailbox subclient.

        Returns:
            List of dictionaries, each containing details about a discovered database.

        Example:
            >>> subclient = UsermailboxSubclient(commcell_object, subclient_name)
            >>> databases = subclient.discover_databases  # Use dot notation for property
            >>> print(f"Discovered {len(databases)} databases")
            >>> # Access details of the first database
            >>> if databases:
            >>>     first_db = databases[0]
            >>>     print(f"First database details: {first_db}")

        #ai-gen-doc
        """
        return self._discover_databases

    @property
    def discover_adgroups(self) -> list:
        """Get the list of discovered Active Directory (AD) groups for the UserMailbox subclient.

        Returns:
            list: A list containing the names or identifiers of discovered AD groups associated with this UserMailbox subclient.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> ad_groups = subclient.discover_adgroups
            >>> print(f"Discovered AD groups: {ad_groups}")
            >>> # Use the returned list to process or display AD group information

        #ai-gen-doc
        """
        return self._discover_adgroups

    @property
    def users(self) -> list:
        """Get the list of users associated with the UserMailbox subclient.

        Returns:
            list: A list containing the users linked to this UserMailbox subclient.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> user_list = subclient.users
            >>> print(f"Number of users: {len(user_list)}")
            >>> for user in user_list:
            >>>     print(user)
        #ai-gen-doc
        """
        return self._users

    @property
    def databases(self) -> List[str]:
        """Get the list of databases associated with the UserMailbox subclient.

        Returns:
            List of database names as strings that are linked to this UserMailbox subclient.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> db_list = subclient.databases  # Use dot notation for property access
            >>> print(f"Databases: {db_list}")
            >>> # Output might be: Databases: ['DB1', 'DB2', 'DB3']

        #ai-gen-doc
        """
        return self._databases

    @property
    def adgroups(self) -> List[str]:
        """Get the list of Active Directory (AD) groups associated with the UserMailbox subclient.

        Returns:
            List of AD group names as strings that are linked to this UserMailbox subclient.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> ad_group_list = subclient.adgroups  # Use dot notation for property access
            >>> print(f"Associated AD groups: {ad_group_list}")

        #ai-gen-doc
        """
        return self._adgroups

    @property
    def o365groups(self) -> list:
        """Get the list of discovered O365 groups for the UserMailbox subclient.

        Returns:
            list: A list containing the discovered O365 groups associated with this UserMailbox subclient.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> groups = subclient.o365groups
            >>> print(f"Discovered O365 groups: {groups}")

        #ai-gen-doc
        """
        return self._o365groups

    def set_user_assocaition(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Create user association for the UserMailboxSubclient.

        This method associates users with the UserMailboxSubclient, allowing you to specify either policy-based
        or plan-based associations depending on the value of `use_policies`.

        Args:
            subclient_content: Dictionary containing user and policy/plan information. The structure should be:
                {
                    'mailboxNames': List of mailbox user names to add (e.g., ["AutoCi2"]),
                    # If use_policies is True:
                    'archive_policy': Name of the archiving policy (str),
                    'cleanup_policy': Name of the clean-up policy (str),
                    'retention_policy': Name of the retention policy (str),
                    # If use_policies is False:
                    'plan_name': Name of the Exchange plan (str),
                    'plan_id': Optional plan ID (int or None)
                }
            use_policies: If True, associates users using policies; if False, uses plan-based association. Defaults to True.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> # Using policies
            >>> content = {
            ...     'mailboxNames': ['user1', 'user2'],
            ...     'archive_policy': 'ArchivePolicy1',
            ...     'cleanup_policy': 'CleanupPolicy1',
            ...     'retention_policy': 'RetentionPolicy1'
            ... }
            >>> subclient.set_user_assocaition(content, use_policies=True)
            >>>
            >>> # Using plan
            >>> content = {
            ...     'mailboxNames': ['user3'],
            ...     'plan_name': 'ExchangePlanA',
            ...     'plan_id': 123
            ... }
            >>> subclient.set_user_assocaition(content, use_policies=False)

        #ai-gen-doc
        """
        users = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        if not (isinstance(subclient_content['mailboxNames'], list)):
            raise SDKException('Subclient', '101')

        try:
            discover_users = self.discover_users

            for mailbox_item in subclient_content['mailboxNames']:

                for mb_item in discover_users:

                    if mailbox_item.lower() == mb_item['aliasName'].lower() or \
                            mailbox_item.lower() == mb_item['smtpAdrress'].lower():
                        mailbox_dict = {
                            'smtpAdrress': mb_item['smtpAdrress'],
                            'aliasName': mb_item['aliasName'],
                            'mailBoxType': mb_item['mailBoxType'],
                            'displayName': mb_item['displayName'],
                            'exchangeServer': mb_item['exchangeServer'],
                            'isAutoDiscoveredUser': mb_item['isAutoDiscoveredUser'],
                            "associated": False,
                            'databaseName': mb_item['databaseName'],
                            "exchangeVersion": mb_item['exchangeVersion'],
                            "licensingStatus": mb_item['licensingStatus'],
                            # "msExchRecipientTypeDetails": mb_item['msExchRecipientTypeDetails'],
                            'user': {
                                '_type_': 13,
                                'userGUID': mb_item['user']['userGUID']
                            }
                        }
                        users.append(mailbox_dict)
                        break

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        if len(users) != len(subclient_content['mailboxNames']):
            to_search_user = [s_user for s_user in subclient_content['mailboxNames']
                              if not any(s_user == f_user['smtpAdrress'] for f_user in users)]
            for mailbox_item in to_search_user:
                search_users = self._search_user(mailbox_item)
                if len(search_users) != 0:
                    users.append(search_users[0])

        discover_info = {
            "discoverByType": 1,
            "mailBoxes": users
        }
        if use_policies:
            _association_json_ = self._association_json(subclient_content)
        else:
            _association_json_ = self._association_json_with_plan(subclient_content)
        _association_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_association_json_)

    def set_pst_association(self, subclient_content: dict) -> None:
        """Create a PST association for the UserMailboxSubclient.

        This method associates PST (Personal Storage Table) files with the UserMailboxSubclient
        by specifying the PST ingestion task details, folder locations, file system content, and
        owner management options.

        Args:
            subclient_content: A dictionary containing the PST association details. The expected structure is:
                {
                    'pstTaskName': str,  # Name for the PST ingestion task
                    'folders': List[str],  # List of folder paths for PST ingestion (optional)
                    'fsContent': dict,  # Mapping of client, backupset, and subclient associations
                    'pstOwnerManagement': {
                        'defaultOwner': str,  # Default owner if no owner is determined
                        'pstDestFolder': str,  # Destination folder for ingested PSTs
                        'usePSTNameToCreateChild': bool  # Whether to use PST name to create child folders
                    }
                }

        Example:
            >>> subclient_content = {
            ...     'pstTaskName': 'PST Ingestion Task',
            ...     'folders': ['/pst_files/folder1', '/pst_files/folder2'],
            ...     'fsContent': {
            ...         'client1': {'backupset1': ['subclient1'], 'backupset2': None},
            ...         'client2': None
            ...     },
            ...     'pstOwnerManagement': {
            ...         'defaultOwner': 'user@example.com',
            ...         'pstDestFolder': '/ingested_psts',
            ...         'usePSTNameToCreateChild': True
            ...     }
            ... }
            >>> subclient.set_pst_association(subclient_content)
            >>> print("PST association created successfully.")

        #ai-gen-doc
        """
        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        try:
            if 'ownerSelectionOrder' not in subclient_content['pstOwnerManagement']:
                subclient_content['pstOwnerManagement']['ownerSelectionOrder'] = [4, 1, 3]
            if 'createPstDestFolder' not in subclient_content['pstOwnerManagement']:
                subclient_content['pstOwnerManagement']['createPstDestFolder'] = True
            if 'pstDestFolder' not in subclient_content['pstOwnerManagement']:
                subclient_content['pstOwnerManagement']['pstDestFolder'] = (f'Archived From '
                                                                            f'Automation')

            pst_dict = {
                'pstTaskName': subclient_content['pstTaskName'],
                'taskType': 1,
                'pstOwnerManagement': {
                    'adProperty': "",
                    'startingFolderPath': "",
                    'pstStubsAction': 1,
                    'managePSTStubs': False,
                    'mergeintoMailBox': True,
                    'pstOwnerBasedOnACL': True,
                    'pstOwnerBasedOnLaptop': False,
                    'usePSTNameToCreateChildForNoOwner': True,
                    'createPstDestFolder':
                        subclient_content["pstOwnerManagement"]["createPstDestFolder"],
                    'orphanFolder': subclient_content['pstOwnerManagement']['defaultOwner'],
                    'pstDestFolder': subclient_content['pstOwnerManagement']['pstDestFolder'],
                    'usePSTNameToCreateChild':
                        subclient_content['pstOwnerManagement']['usePSTNameToCreateChild'],
                    'ownerSelectionOrder':
                        subclient_content["pstOwnerManagement"]["ownerSelectionOrder"]
                }
            }
            if 'folders' in subclient_content:
                pst_dict['folders'] = subclient_content['folders']
            elif 'fsContent' in subclient_content:
                pst_dict['associations'] = self.set_fs_association_for_pst(
                    subclient_content['fsContent'])
                pst_dict['taskType'] = 0
            subclient_entity = {"_type_": 7, "subclientId": int(self._subclient_id)}
            discover_info = {
                'discoverByType': 9,
                'pstIngestion': pst_dict
            }
            _assocaition_json_ = {
                "emailAssociation":
                    {
                        "emailDiscoverinfo": discover_info,
                        "subclientEntity": subclient_entity
                    }
            }
            self._set_association_request(_assocaition_json_)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

    def set_fs_association_for_pst(self, association: dict) -> list[
        dict[str, int | Any] | dict[str, int | str | Any] | dict[str, int | Any]]:
        """Create a PST association for PST Ingestion by File System (FS).

        This helper method sets up associations between clients, backupsets, and subclients
        for PST ingestion. The `association` dictionary should map client names to either:
          - a dictionary of backupset names to lists of subclient names (or None for all subclients),
          - or None to include all backupsets and subclients under the client.

        Example:
            >>> association = {
            ...     'client1': {
            ...         'backupset1': ['subclient1'],
            ...         'backupset2': None
            ...     },
            ...     'client2': None
            ... }
            >>> subclient.set_fs_association_for_pst(association)
            >>> # This will associate 'subclient1' under 'backupset1', all subclients under 'backupset2',
            >>> # and all backupsets/subclients under 'client2' for PST ingestion.

        Args:
            association: Dictionary specifying the client, backupset, and subclient associations for PST ingestion.

        #ai-gen-doc
        """
        assoc_list = []
        client_dict, backupset_dict, sub_dict = dict(), dict(), dict()
        _type_id = {"client": 3, "subclient": 7, "backupset": 6, "apptype": 4}
        for client_name, backupsets in association.items():
            client_name = client_name.lower()
            client_obj = self._commcell_object.clients.get(client_name)

            client_dict = {"commCellId": int(self._commcell_object._id),
                           "commcellName": self._commcell_object.commserv_name,
                           "clientName": client_name,
                           "clientId": int(client_obj.client_id)
                           }
            agent = client_obj.agents.get("file system")

            if backupsets:
                for backupset_name, subclients in backupsets.items():
                    backupset_name = backupset_name.lower()
                    backupset_obj = agent.backupsets.get(backupset_name)
                    if not backupset_obj:
                        raise SDKException('Subclient', '102', "Backupset {0} not present in "
                                                               "".format(backupset_name))
                    backupset_dict = {"backupsetName": backupset_obj.name,
                                      "appName": "File System",
                                      "applicationId": int(agent.agent_id),
                                      "backupsetId": int(backupset_obj.backupset_id),
                                      "_type_": _type_id["backupset"]
                                      }
                    backupset_dict.update(client_dict)
                    for subclient_name in subclients:
                        if subclient_name.lower() not in backupset_obj.subclients.all_subclients:
                            raise SDKException('Subclient', '102',
                                               "Subclient %s not present in backupset %s" %
                                               (str(subclient_name), str(backupset_name)))
                        subclient_name = subclient_name.lower()
                        sub_dict = {"subclientId": int(backupset_obj.subclients.all_subclients[
                                                           subclient_name]['id']),
                                    "subclientName": subclient_name}
                        sub_dict.update(backupset_dict)
                        sub_dict["_type_"] = _type_id["subclient"]
                        assoc_list.append(sub_dict)
                    if not subclients:
                        assoc_list.append(backupset_dict)
            else:
                client_dict["_type_"] = _type_id["client"]
                assoc_list.append(client_dict)
        return assoc_list

    def set_database_assocaition(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Create a database association for the UserMailboxSubclient.

        This method associates databases with the UserMailboxSubclient using either policy-based
        or plan-based configuration, depending on the provided parameters.

        Args:
            subclient_content: Dictionary specifying the databases and association details.
                For policy-based association:
                    {
                        'databaseNames': [list of database names as strings],
                        'is_auto_discover_user': True,
                        'archive_policy': "Archiving policy name",
                        'cleanup_policy': "Clean-up policy name",
                        'retention_policy': "Retention policy name"
                    }
                For plan-based association:
                    {
                        'is_auto_discover_user': True,
                        'plan_name': "Name of the plan",
                        'plan_id': (optional) ID of the plan as string or int
                    }
            use_policies: If True, uses policy-based association; if False, uses plan-based association.

        Example:
            >>> # Policy-based association
            >>> content = {
            ...     'databaseNames': ['DB1', 'DB2'],
            ...     'is_auto_discover_user': True,
            ...     'archive_policy': 'CIPLAN Archiving policy',
            ...     'cleanup_policy': 'CIPLAN Clean-up policy',
            ...     'retention_policy': 'CIPLAN Retention policy'
            ... }
            >>> subclient.set_database_assocaition(content, use_policies=True)

            >>> # Plan-based association
            >>> content = {
            ...     'is_auto_discover_user': True,
            ...     'plan_name': 'Exchange Plan',
            ...     'plan_id': 12345
            ... }
            >>> subclient.set_database_assocaition(content, use_policies=False)

        #ai-gen-doc
        """
        databases = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        if not (isinstance(subclient_content['databaseNames'], list) and
                isinstance(subclient_content['is_auto_discover_user'], bool)):
            raise SDKException('Subclient', '101')

        try:
            discover_databases = self.discover_databases

            for database_item in subclient_content['databaseNames']:

                for db_item in discover_databases:

                    if database_item.lower() == db_item['databaseName'].lower():
                        database_dict = {
                            'exchangeServer': db_item['exchangeServer'],
                            "associated": False,
                            'databaseName': db_item['databaseName'],
                        }
                        databases.append(database_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        discover_info = {
            "discoverByType": 2,
            "databases": databases
        }
        if use_policies:
            _association_json_ = self._association_json(subclient_content)
        else:
            _association_json_ = self._association_json_with_plan(subclient_content)
            _association_json_["emailAssociation"]["advanceOptions"] = {
                "enableAutoDiscovery": subclient_content.get("is_auto_discover_user", False)
            }
        _association_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_association_json_)

    def set_adgroup_associations(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Associate Active Directory (AD) groups with the UserMailboxSubclient.

        This method creates associations between AD groups and the UserMailboxSubclient,
        allowing you to manage mailbox content based on group membership. The association
        can be configured to use policies or plans, depending on the `use_policies` flag.

        Args:
            subclient_content: Dictionary containing AD group association details.
                When `use_policies` is True, the dictionary should include:
                    - 'adGroupNames': List of AD group names to associate.
                    - 'is_auto_discover_user': Boolean indicating if auto-discovery is enabled.
                    - 'archive_policy': Name of the archiving policy.
                    - 'cleanup_policy': Name of the clean-up policy.
                    - 'retention_policy': Name of the retention policy.
                When `use_policies` is False, the dictionary should include:
                    - 'plan_name': Name of the Exchange plan.
                    - 'is_auto_discover_user': Boolean indicating if auto-discovery is enabled.
                    - 'plan_id': Integer plan ID or None (optional).
            use_policies: If True, use policy-based association. If False, use plan-based association. Defaults to True.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> adgroup_content = {
            ...     'adGroupNames': ['HR_Group', 'Finance_Group'],
            ...     'is_auto_discover_user': True,
            ...     'archive_policy': 'Default Archive',
            ...     'cleanup_policy': 'Default Cleanup',
            ...     'retention_policy': 'Default Retention'
            ... }
            >>> subclient.set_adgroup_associations(adgroup_content)
            >>> # For plan-based association:
            >>> plan_content = {
            ...     'plan_name': 'Exchange_Plan_01',
            ...     'is_auto_discover_user': True,
            ...     'plan_id': 1234
            ... }
            >>> subclient.set_adgroup_associations(plan_content, use_policies=False)

        #ai-gen-doc
        """
        adgroups = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        if not (isinstance(subclient_content['adGroupNames'], list) and
                isinstance(subclient_content['is_auto_discover_user'], bool)):
            raise SDKException('Subclient', '101')

        try:
            discover_adgroups = self.discover_adgroups

            for adgroup_item in subclient_content['adGroupNames']:

                for ad_item in discover_adgroups:

                    if adgroup_item.lower() == ad_item['adGroupName'].lower():
                        adgroup_dict = {
                            'adGroupName': ad_item['adGroupName'],
                        }
                        adgroups.append(adgroup_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        discover_info = {
            "discoverByType": 3,
            "adGroups": adgroups
        }
        if use_policies:
            _assocaition_json_ = self._association_json(subclient_content)
        else:
            _assocaition_json_ = self._association_json_with_plan(subclient_content)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        _assocaition_json_["emailAssociation"].update({"emailStatus": 0})
        _assocaition_json_["emailAssociation"].update({"advanceOptions": {
            "enableAutoDiscovery": subclient_content["is_auto_discover_user"]
        }})
        self._set_association_request(_assocaition_json_)

    def set_o365group_asscoiations(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Create O365 Group associations for the UserMailboxSubclient.

        Associates the specified archive, cleanup, and retention policies with the O365 Group
        for this UserMailboxSubclient.

        Args:
            subclient_content: Dictionary containing the policies to associate. The expected keys are:
                - 'archive_policy': Name of the archiving policy (str).
                - 'cleanup_policy': Name of the clean-up policy (str).
                - 'retention_policy': Name of the retention policy (str).

                Example:
                    subclient_content = {
                        'archive_policy': "CIPLAN Archiving policy",
                        'cleanup_policy': "CIPLAN Clean-up policy",
                        'retention_policy': "CIPLAN Retention policy"
                    }
            use_policies: If True, use policy-based association. If False, use plan-based association. Defaults to True.

        Example:
            >>> subclient_content = {
                    'is_auto_discover_user': True,
            ...     'archive_policy': "CIPLAN Archiving policy",
            ...     'cleanup_policy': "CIPLAN Clean-up policy",
            ...     'retention_policy': "CIPLAN Retention policy"
            ... }
            >>> subclient.set_adgroup_associations(subclient_content)

            >>> # For plan-based association:
            >>> plan_content = {
            ...     'plan_name': 'Exchange_Plan_01',
            ...     'is_auto_discover_user': True,
            ...     'plan_id': 1234
            ... }
            >>> subclient.set_adgroup_associations(plan_content, use_policies=False)

        #ai-gen-doc
        """
        discover_info = {
            "discoverByType": 11,
            "genericAssociations": [
                {
                    "associationName": "All O365 Group Mailboxes",
                    "associationType": 11
                }
            ]
        }
        if use_policies:
            _assocaition_json_ = self._association_json(subclient_content)
        else:
            _assocaition_json_ = self._association_json_with_plan(subclient_content)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        _assocaition_json_["emailAssociation"].update({"advanceOptions": {
            "enableAutoDiscovery": subclient_content.get("is_auto_discover_user", True)
        }})
        self._set_association_request(_assocaition_json_)

    def delete_user_assocaition(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Delete user associations from a UserMailboxSubclient.

        This method removes specified user mailboxes from the subclient, either by using policies or a plan,
        depending on the value of `use_policies`.

        Args:
            subclient_content: Dictionary specifying the users and associated policy or plan information.
                Example structure:
                    {
                        'mailboxNames': ["user1@domain.com", "user2@domain.com"],
                        # If use_policies is True:
                        'archive_policy': "CIPLAN Archiving policy",
                        'cleanup_policy': "CIPLAN Clean-up policy",
                        'retention_policy': "CIPLAN Retention policy"
                        # If use_policies is False:
                        'plan_name': "Plan Name",
                        'plan_id': 123  # Optional
                    }
            use_policies: If True, uses policy-based association; if False, uses plan-based association.

        Example:
            >>> subclient_content = {
            ...     'mailboxNames': ["alice@company.com", "bob@company.com"],
            ...     'archive_policy': "Default Archive Policy",
            ...     'cleanup_policy': "Default Cleanup Policy",
            ...     'retention_policy': "Default Retention Policy"
            ... }
            >>> subclient.delete_user_assocaition(subclient_content, use_policies=True)

            >>> subclient_content = {
            ...     'mailboxNames': ["carol@company.com"],
            ...     'plan_name': "UserMailboxPlan",
            ...     'plan_id': 456
            ... }
            >>> subclient.delete_user_assocaition(subclient_content, use_policies=False)

        #ai-gen-doc
        """
        users = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        if not (isinstance(subclient_content['mailboxNames'], list)):
            raise SDKException('Subclient', '101')

        try:
            discover_users = self.discover_users

            for mailbox_item in subclient_content['mailboxNames']:

                for mb_item in discover_users:

                    if mailbox_item.lower() == mb_item['aliasName'].lower():
                        mailbox_dict = {
                            'smtpAdrress': mb_item['smtpAdrress'],
                            'aliasName': mb_item['aliasName'],
                            'mailBoxType': mb_item['mailBoxType'],
                            'displayName': mb_item['displayName'],
                            'exchangeServer': mb_item['exchangeServer'],
                            'isAutoDiscoveredUser': mb_item['isAutoDiscoveredUser'],
                            "associated": False,
                            'databaseName': mb_item['databaseName'],
                            "exchangeVersion": mb_item['exchangeVersion'],
                            "exchangeServer": mb_item['exchangeServer'],
                            'user': {
                                '_type_': 13,
                                'userGUID': mb_item['user']['userGUID']
                            }
                        }
                        users.append(mailbox_dict)
                        break

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))
        discover_info = {
            "discoverByType": 1,
            "mailBoxes": users
        }
        if use_policies:
            _association_json_ = self._association_json(subclient_content)
        else:
            _association_json_ = self._association_json_with_plan(subclient_content)
        _association_json_["emailAssociation"]["emailStatus"] = 1
        _association_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._update_association_request(_association_json_)

    def delete_o365group_association(self, subclient_content: dict) -> None:
        """Delete the association of O365 groups from a UserMailboxSubclient.

        Removes specified users and their associated policies from the subclient.

        Args:
            subclient_content: Dictionary containing details of the users and policies to remove from the subclient.
                Example format:
                    {
                        'mailboxNames': ["AutoCi2"],
                        'archive_policy': "CIPLAN Archiving policy",
                        'cleanup_policy': "CIPLAN Clean-up policy",
                        'retention_policy': "CIPLAN Retention policy"
                    }

        Example:
            >>> subclient_content = {
            ...     'mailboxNames': ["AutoCi2"],
            ...     'archive_policy': "CIPLAN Archiving policy",
            ...     'cleanup_policy': "CIPLAN Clean-up policy",
            ...     'retention_policy': "CIPLAN Retention policy"
            ... }
            >>> subclient.delete_o365group_association(subclient_content)
            >>> print("O365 group association deleted successfully.")

        #ai-gen-doc
        """
        groups = []
        try:
            for mb_item in self.o365groups:
                mailbox_dict = {
                    'smtpAdrress': mb_item['smtp_address'],
                    'aliasName': mb_item['alias_name'],
                    'mailBoxType': 1,
                    'displayName': mb_item['display_name'],
                    'exchangeServer': "",
                    'isAutoDiscoveredUser': mb_item['is_auto_discover_user'].lower() == 'true',
                    'msExchRecipientTypeDetails': 36,
                    "associated": False,
                    'databaseName': mb_item['database_name'],
                    'user': {
                        '_type_': 13,
                        'userGUID': mb_item['user_guid']
                    }
                }
                groups.append(mailbox_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        discover_info = {
            "discoverByType": 1,
            "mailBoxes": groups
        }
        _assocaition_json_ = self._association_json(subclient_content, True)
        _assocaition_json_["emailAssociation"]["emailStatus"] = 1
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._update_association_request(_assocaition_json_)

    def delete_database_assocaition(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Delete database associations for a UserMailboxSubclient.

        This method removes specified database associations from the subclient, either using policies or plans,
        based on the provided parameters.

        Args:
            subclient_content: Dictionary specifying the databases and associated policies or plans to delete.
                For policy-based deletion:
                    {
                        'databaseNames': [list of database names as strings],
                        'archive_policy': 'Archiving policy name',
                        'cleanup_policy': 'Clean-up policy name',
                        'retention_policy': 'Retention policy name'
                    }
                For plan-based deletion:
                    {
                        'is_auto_discover_user': True,
                        'plan_name': 'Name of the plan',
                        'plan_id': 'Optional plan ID'
                    }
            use_policies: If True, uses policy-based deletion; if False, uses plan-based deletion.

        Example:
            >>> # Delete databases using policy
            >>> subclient_content = {
            ...     'databaseNames': ['DB1', 'DB2'],
            ...     'archive_policy': 'ArchivePolicy1',
            ...     'cleanup_policy': 'CleanupPolicy1',
            ...     'retention_policy': 'RetentionPolicy1'
            ... }
            >>> subclient.delete_database_assocaition(subclient_content, use_policies=True)
            >>>
            >>> # Delete databases using plan
            >>> subclient_content = {
            ...     'is_auto_discover_user': True,
            ...     'plan_name': 'MailboxPlanA',
            ...     'plan_id': '12345'
            ... }
            >>> subclient.delete_database_assocaition(subclient_content, use_policies=False)

        #ai-gen-doc
        """
        databases = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        if not (isinstance(subclient_content['databaseNames'], list) and
                isinstance(subclient_content['is_auto_discover_user'], bool)):
            raise SDKException('Subclient', '101')

        try:
            discover_databases = self.discover_databases

            for database_item in subclient_content['databaseNames']:

                for db_item in discover_databases:

                    if database_item.lower() == db_item['databaseName'].lower():
                        database_dict = {
                            'exchangeServer': db_item['exchangeServer'],
                            "associated": False,
                            'databaseName': db_item['databaseName'],
                        }
                        databases.append(database_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        discover_info = {
            "discoverByType": 2,
            "databases": databases
        }

        if use_policies:
            _association_json_ = self._association_json(subclient_content)
        else:
            _association_json_ = self._association_json_with_plan(subclient_content)

        _association_json_["emailAssociation"]["emailStatus"] = 1
        _association_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._update_association_request(_association_json_)

    def delete_adgroup_assocaition(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Delete Active Directory (AD) group associations from a UserMailboxSubclient.

        This method removes specified AD groups from the subclient's content, either using policies or plans
        based on the provided parameters.

        Args:
            subclient_content: Dictionary specifying the AD groups and related policy or plan information to delete.
                Example structure for policy-based deletion:
                    {
                        'adGroupNames': ["ADGroup1", "ADGroup2"],
                        'is_auto_discover_user': True,
                        'archive_policy': "CIPLAN Archiving policy",
                        'cleanup_policy': "CIPLAN Clean-up policy",
                        'retention_policy': "CIPLAN Retention policy"
                    }
                Example structure for plan-based deletion:
                    {
                        'is_auto_discover_user': True,
                        'plan_name': "Exchange Plan Name",
                        'plan_id': 123  # Optional, can be int or None
                    }
            use_policies: If True, use policy-based deletion; if False, use plan-based deletion.

        Example:
            >>> subclient_content = {
            ...     'adGroupNames': ["FinanceGroup", "HRGroup"],
            ...     'is_auto_discover_user': True,
            ...     'archive_policy': "Finance Archive Policy",
            ...     'cleanup_policy': "Finance Cleanup Policy",
            ...     'retention_policy': "Finance Retention Policy"
            ... }
            >>> subclient.delete_adgroup_assocaition(subclient_content)
            >>>
            >>> # For plan-based deletion:
            >>> plan_content = {
            ...     'is_auto_discover_user': True,
            ...     'plan_name': "Exchange Plan",
            ...     'plan_id': 456
            ... }
            >>> subclient.delete_adgroup_assocaition(plan_content, use_policies=False)

        #ai-gen-doc
        """
        adgroups = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        if not (isinstance(subclient_content['adGroupNames'], list) and
                isinstance(subclient_content['is_auto_discover_user'], bool)):
            raise SDKException('Subclient', '101')

        try:
            discover_adgroups = self.discover_adgroups

            for adgroup_item in subclient_content['adGroupNames']:

                for ad_item in discover_adgroups:

                    if adgroup_item.lower() == ad_item['adGroupName'].lower():
                        adgroup_dict = {
                            "associated": False,
                            'adGroupName': ad_item['adGroupName'],
                        }
                        adgroups.append(adgroup_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        discover_info = {
            "discoverByType": 3,
            "adGroups": adgroups
        }
        if use_policies:
            _assocaition_json_ = self._association_json(subclient_content)
        else:
            _assocaition_json_ = self._association_json_with_plan(subclient_content)
        _assocaition_json_["emailAssociation"]["emailStatus"] = 1
        _assocaition_json_["emailAssociation"]["enableAutoDiscovery"] = subclient_content[
            "is_auto_discover_user"]
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_assocaition_json_)

    def enable_allusers_associations(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Enable all users association for the UserMailboxSubclient.

        This method assigns specified policies or plans to all user associations within the subclient.
        The `subclient_content` parameter should be a dictionary specifying either policy details or plan details.

        Args:
            subclient_content: Dictionary containing the configuration for user associations.
                For policy-based association:
                    {
                        'is_auto_discover_user': True,
                        'archive_policy': "CIPLAN Archiving policy",
                        'cleanup_policy': "CIPLAN Clean-up policy",
                        'retention_policy': "CIPLAN Retention policy"
                    }
                For plan-based association:
                    {
                        'is_auto_discover_user': True,
                        'plan_name': "Name of plan",
                        'plan_id': "Optional plan ID"
                    }
            use_policies: If True, use policy-based association; if False, use plan-based association.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> # Using policies
            >>> policy_content = {
            ...     'is_auto_discover_user': True,
            ...     'archive_policy': "CIPLAN Archiving policy",
            ...     'cleanup_policy': "CIPLAN Clean-up policy",
            ...     'retention_policy': "CIPLAN Retention policy"
            ... }
            >>> subclient.enable_allusers_associations(policy_content, use_policies=True)
            >>>
            >>> # Using a plan
            >>> plan_content = {
            ...     'is_auto_discover_user': True,
            ...     'plan_name': "UserMailbox Plan"
            ... }
            >>> subclient.enable_allusers_associations(plan_content, use_policies=False)

        #ai-gen-doc
        """

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        discover_info = {
            "discoverByType": 8,
            "genericAssociations": [
                {
                    "associationName": "All Users",
                    "associationType": 8
                }
            ]
        }
        if use_policies:
            _association_json_ = self._association_json(subclient_content)
        else:
            _association_json_ = self._association_json_with_plan(plan_details=subclient_content)
        _association_json_['emailAssociation']['advanceOptions'] = {"enableAutoDiscovery": True}
        _association_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_association_json_)

    def disable_allusers_associations(self, use_policies: bool = True, plan_details: Optional[Dict[str, Any]] = None) -> None:
        """Disable all-user associations for the UserMailboxSubclient.

        This method disables the association of all users with the UserMailboxSubclient.
        You can choose to use either policies or plans for the operation.

        Args:
            use_policies: If True, disables associations using policies. If False, uses plans.
            plan_details: Optional dictionary containing plan information.
                Example: {"plan_name": "BackupPlan", "plan_id": 123}

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> # Disable all-user associations using policies
            >>> subclient.disable_allusers_associations(use_policies=True)
            >>>
            >>> # Disable all-user associations using a specific plan
            >>> plan_info = {"plan_name": "ExchangeBackup", "plan_id": 456}
            >>> subclient.disable_allusers_associations(use_policies=False, plan_details=plan_info)

        #ai-gen-doc
        """
        subclient_content = {
            'is_auto_discover_user': True
        }
        discover_info = {
            "discoverByType": 8,
            "genericAssociations": [
                {
                    "associationName": "All Users",
                    "associationType": 8
                }
            ]
        }

        if use_policies:
            _association_json_ = self._association_json(subclient_content)
        else:
            _association_json_ = self._association_json_with_plan(plan_details=plan_details)

        _association_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        _association_json_["emailAssociation"]["emailStatus"] = 2
        _association_json_['emailAssociation']['advanceOptions'] = {"enableAutoDiscovery": True}
        self._set_association_request(_association_json_)

    def enable_auto_discover_association(self, association_name: str, plan_name: str) -> None:
        """Enable auto-discover association for all users in the UserMailboxSubclient.

        This method configures the subclient to automatically associate users or groups
        based on the specified association type and plan.

        Args:
            association_name: The type of auto-discover association to enable.
                Valid values include:
                    - "All Users"
                    - "All O365 Mailboxes"
                    - "All Public Folders"
            plan_name: The name of the plan to associate with the discovered users or groups.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> subclient.enable_auto_discover_association("All Users", "DefaultPlan")
            >>> print("Auto-discover association enabled for all users with DefaultPlan.")

        #ai-gen-doc
        """
        plan = self._commcell_object.plans.get(plan_name)

        association_dict = {"All Users": 8,
                            "All Office365 Groups": 11,
                            "All Public Folders": 12
                            }

        _association_json = {
            "emailAssociation": {
                "emailStatus": 0,
                "advanceOptions": {
                    "enableAutoDiscovery": True
                },
                "subclientEntity": self._subClientEntity,
                "emailDiscoverinfo": {
                    "discoverByType": association_dict[association_name],
                    "genericAssociations": [
                        {
                            "associationName": association_name,
                            "associationType": association_dict[association_name]
                        }
                    ]
                },
                "plan": {
                    "planId": int(plan.plan_id)
                }
            }
        }
        self._set_association_request(_association_json)

    def delete_auto_discover_association(self, association_name: str, subclient_content: dict, use_policies: bool = True) -> None:
        """Delete all user associations for the UserMailboxSubclient based on auto discover association type.

        This method removes associations for users or groups from the UserMailboxSubclient, using either policies or plans
        depending on the value of `use_policies`. The `subclient_content` dictionary should contain relevant information
        about the users/groups and associated policies or plans.

        Args:
            association_name: The type of auto discover association to delete.
                Valid values:
                    - "All Users"
                    - "All O365 Mailboxes"
                    - "All Public Folders"
            subclient_content: Dictionary containing information about users/groups and their associated policies or plans.
                If use_policies is True:
                    {
                        "is_auto_discover_user": bool,
                        "archive_policy": object,
                        "cleanup_policy": object,
                        "retention_policy": object
                    }
                If use_policies is False:
                    {
                        "is_auto_discover_user": bool,
                        "plan_name": str,
                        "plan_id": Optional[str]
                    }
            use_policies: If True, uses policy objects for association; if False, uses plan information.

        Example:
            >>> subclient_content = {
            ...     "is_auto_discover_user": True,
            ...     "archive_policy": archive_policy_obj,
            ...     "cleanup_policy": cleanup_policy_obj,
            ...     "retention_policy": retention_policy_obj
            ... }
            >>> subclient.delete_auto_discover_association("All Users", subclient_content, use_policies=True)
            >>>
            >>> subclient_content = {
            ...     "is_auto_discover_user": True,
            ...     "plan_name": "ExchangePlan",
            ...     "plan_id": "12345"
            ... }
            >>> subclient.delete_auto_discover_association("All O365 Mailboxes", subclient_content, use_policies=False)

        #ai-gen-doc
        """
        if not (isinstance(subclient_content, dict)):
            raise SDKException("Subclient", "101")

        association_dict = {"all users": 8,
                            "all o365 group mailboxes": 11,
                            "all public folders": 12
                            }

        if association_name.lower() not in association_dict:
            raise SDKException("Subclient", "102", "Invalid Association Name supplied")

        if use_policies:
            _association_json_ = self._association_json(subclient_content)
        else:
            planobject = self._commcell_object.plans.get(subclient_content["plan_name"])
            _association_json_ = self._association_json_with_plan(plan_details=planobject)

        discover_info = {
            "discoverByType": association_dict[association_name.lower()],
            "genericAssociations": [
                {
                    "associationName": association_name,
                    "associationType": association_dict[association_name.lower()]
                }
            ]
        }
        _association_json_["emailAssociation"]["advanceOptions"]["enableAutoDiscovery"] = True
        _association_json_["emailAssociation"]["emailStatus"] = 1
        _association_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_association_json_)

    def enable_ews_support(self, service_url: str) -> None:
        """Enable EWS (Exchange Web Services) protocol support for backing up on-premises mailboxes.

        Args:
            service_url: The EWS connection URL for your Exchange server.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> subclient.enable_ews_support("https://exchange.example.com/EWS/Exchange.asmx")
            >>> print("EWS support enabled for the subclient.")

        #ai-gen-doc
        """
        self.agentproperties = self._agent_object.properties
        self.agentproperties["onePassProperties"]["onePassProp"]["ewsDetails"]["bUseEWS"] = True
        self.agentproperties["onePassProperties"]["onePassProp"]["ewsDetails"]["ewsConnectionUrl"] = service_url
        self._agent_object.update_properties(self.agentproperties)

    def browse_mailboxes(self, retry_attempts: int = 0) -> dict:
        """Retrieve the mailboxes available for Out-of-Place (OOP) restore.

        Args:
            retry_attempts: Number of times to retry the mailbox retrieval in case of failure. Defaults to 0.

        Returns:
            dict: A dictionary containing information about the available mailboxes for OOP restore.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> mailboxes = subclient.browse_mailboxes(retry_attempts=2)
            >>> print(f"Number of mailboxes found: {len(mailboxes)}")
            >>> # Access mailbox details
            >>> for mailbox_id, mailbox_info in mailboxes.items():
            ...     print(f"Mailbox ID: {mailbox_id}, Info: {mailbox_info}")

        #ai-gen-doc
        """
        BROWSE_MAILBOXES = self._commcell_object._services['EMAIL_DISCOVERY_WITHOUT_REFRESH'] % (
            int(self._backupset_object.backupset_id), 'User'
        )
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', BROWSE_MAILBOXES)
        if flag:
            if response and response.json():
                discover_content = response.json()
                if discover_content.get('resp', {}).get('errorCode', 0) == 469762468:
                    time.sleep(10)
                    if retry_attempts > 10:
                        raise SDKException('Subclient', '102', 'Failed to perform browse operation.')
                    return self.browse_mailboxes(retry_attempts + 1)
                if 'discoverInfo' in discover_content.keys():
                    if 'mailBoxes' in discover_content['discoverInfo']:
                        mailboxes = discover_content["discoverInfo"]["mailBoxes"]
                        return mailboxes
            else:
                raise SDKException("Response", "102")
        else:
            response_string = self.commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def backup_generic_items(self, subclient_content: list[dict]) -> None:
        """Backup generic items for an Exchange Online client.

        This method initiates a backup of generic items such as all public folders, all O365 group mailboxes, or all users
        for the specified Exchange Online client. The items to be backed up are specified in the `subclient_content` list,
        where each item is a dictionary describing the association name and type.

        Args:
            subclient_content: A list of dictionaries, each specifying an item to be backed up. Each dictionary should have:
                - "associationName": The name of the association (e.g., "All Public Folders", "All Users").
                - "associationType": The type of association as an integer.

                Example:
                    [
                        {
                            "associationName": "All Public Folders",
                            "associationType": 12
                        },
                        {
                            "associationName": "All Users",
                            "associationType": 12
                        }
                    ]

        Example:
            >>> subclient_content = [
            ...     {"associationName": "All Public Folders", "associationType": 12},
            ...     {"associationName": "All Users", "associationType": 12}
            ... ]
            >>> subclient.backup_generic_items(subclient_content)
            >>> print("Backup of generic items initiated successfully.")

        #ai-gen-doc
        """
        task_dict = self._backup_generic_items_json(subclient_content=subclient_content)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['CREATE_TASK'], task_dict
        )

        return self._process_backup_response(flag, response)

    def backup_mailboxes(self, mailbox_alias_names: Optional[list] = None, **kwargs: dict) -> 'Job':
        """Initiate a backup job for specific mailboxes by their alias names.

        Args:
            mailbox_alias_names: Optional list of alias names for the mailboxes to back up.
                Example:
                    ['aj', 'tkumar']
            **kwargs: Additional keyword arguments for backup customization.
                items_selection_option (str): Item Selection Option (e.g., "7" for selecting recently backed up entities).

        Returns:
            Job: An instance of the Job class representing the initiated backup job.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> job = subclient.backup_mailboxes(mailbox_alias_names=['aj', 'tkumar'], items_selection_option="7")
            >>> print(f"Backup job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        task_json = self._task_json_for_backup(mailbox_alias_names, **kwargs)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)

    def create_recovery_point(self, mailbox_prop: Dict[str, Any], job: Optional['Job'] = None, job_id: Optional[int] = None) -> Dict[str, Any]:
        """Create a recovery point for a specified mailbox.

        This method initiates the creation of a recovery point for a mailbox using the provided mailbox properties.
        You must specify either a backup job object or a backup job ID to associate the recovery point with a specific backup job.

        Args:
            mailbox_prop: Dictionary containing mailbox properties required for recovery point creation.
                Example:
                    {
                        'mailbox_smtp': 'user@example.com',
                        'mailbox_guid': '1234-5678-90ab-cdef',
                        'index_server': 'IndexServer01'
                    }
            job: Optional; Job object representing the backup job to associate with the recovery point.
            job_id: Optional; Integer ID of the backup job to associate with the recovery point.

        Returns:
            Dictionary containing the response details of the recovery point creation.
            Example format:
                {
                    'recovery_point_id': 12345,
                    'recovery_point_job_id': 67890
                }

        Example:
            >>> mailbox_props = {
            ...     'mailbox_smtp': 'user@example.com',
            ...     'mailbox_guid': '1234-5678-90ab-cdef',
            ...     'index_server': 'IndexServer01'
            ... }
            >>> # Using job object
            >>> result = subclient.create_recovery_point(mailbox_props, job=backup_job)
            >>> print(result)
            >>> # Using job ID
            >>> result = subclient.create_recovery_point(mailbox_props, job_id=67890)
            >>> print(result)

        #ai-gen-doc
        """

        if (job == None and job_id == None):
            raise Exception("At least one value out of job or job_id should be passed")

        if (job == None and type(job_id) == int):
            job = self._commcell_object.job_controller.get(job_id)

        index_server = self._commcell_object.clients.get(mailbox_prop['index_server'])
        index_server_id = index_server.client_id

        recovery_point_dict = {
            "opType": 0,
            "advOptions": {
                "advConfig": {
                    "browseAdvancedConfigReq": {
                        "additionalFlags": [
                            {
                                "flagType": 13,
                                "value": "{}".format(index_server_id),
                                "key": "RecoveryPointIndexServer"
                            }
                        ]
                    },
                    "applicationMining": {
                        "appType": 137,
                        "isApplicationMiningReq": True,
                        "browseInitReq": {
                            "bCreateRecoveryPoint": True,
                            "jobId": int(job.job_id),
                            "pointInTimeRange": {
                                "fromTime": int(job.start_timestamp),
                                "toTime": int(job.end_timestamp)
                            },
                            "mbxInfo": [
                                {
                                    "smtpAdrress": mailbox_prop['mailbox_smtp'],
                                    "mbxGUIDs": mailbox_prop['mailbox_guid']
                                }
                            ]
                        }
                    }
                }
            },
            "paths": [
                {
                    "path": "\\MB\\{%s}" % mailbox_prop['mailbox_guid']
                }
            ],
            "entity": {
                "subclientId": int(self.subclient_id),
                "backupsetId": int(self._backupset_object.backupset_id),
                "clientId": int(self._client_object.client_id)
            },
            "timeRange": {
                "fromTime": 0,
                "toTime": int(job.start_timestamp)
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['BROWSE'], recovery_point_dict
        )

        if flag:
            if response and response.json():
                browse_response = response.json()

                if 'browseResponses' in browse_response.keys():
                    recovery_point_job_id = browse_response.get('browseResponses', [{}])[0].get('browseResult', {}).get(
                        'advConfig', {}).get(
                        'applicationMining', {}).get('browseInitResp', {}).get('recoveryPointJobID')

                    recovery_point_id = browse_response.get('browseResponses', [{}])[0].get('browseResult', {}).get(
                        'advConfig', {}).get(
                        'applicationMining', {}).get('browseInitResp', {}).get('recoveryPointID', {})

                    res_dict = {
                        'recovery_point_job_id': recovery_point_job_id,
                        'recovery_point_id': recovery_point_id
                    }
                    return res_dict
                else:
                    raise SDKException('Response', '102', response.json)
            else:
                raise SDKException('Response', '102', response.json)
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Reload the User Mailbox Subclient information from the server.

        This method refreshes the state of the UsermailboxSubclient instance, ensuring that
        any changes made on the server are reflected in the local object.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> subclient.refresh()
            >>> print("Subclient information refreshed successfully")

        #ai-gen-doc
        """
        self._get_subclient_properties()
        self._discover_users = self._get_discover_users()
        self._discover_databases = self._get_discover_database()
        self._discover_adgroups = self._get_discover_adgroups()
        self._users, self._o365groups = self._get_user_assocaitions()
        self._databases = self._get_database_associations()
        self._adgroups = self._get_adgroup_assocaitions()

    def restore_in_place_syntex(self, **kwargs: dict) -> 'Job':
        """Run an in-place restore job on the specified Syntex Exchange pseudo client.

        This method initiates an in-place restore operation for the given mailboxes or folders
        on a Syntex Exchange pseudo client. The paths to restore should be provided as a list
        using the 'paths' keyword argument.

        Keyword Args:
            paths (list): List of mailbox or folder paths to restore.

        Returns:
            Job: The Job object representing the initiated restore job.

        Raises:
            SDKException: If 'paths' is not a list, if the job fails to initialize, or if the response is empty.

        Example:
            >>> paths_to_restore = ['/Mailbox1/Inbox', '/Mailbox2/Sent Items']
            >>> job = subclient.restore_in_place_syntex(paths=paths_to_restore)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        paths = kwargs.get('paths', [])
        paths = self._filter_paths(paths)
        self._json_restore_exchange_restore_option({})
        self._json_backupset()
        restore_option = {"paths": paths}

        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=restore_option)
        request_json['taskInfo']['associations'][0]['subclientName'] = self.subclient_name
        request_json['taskInfo']['associations'][0][
            'backupsetName'] = self._backupset_object.backupset_name
        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions']['exchangeOption'] = self._exchange_option_restore_json
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["browseOption"]['backupset'] = self._exchange_backupset_json

        mailboxes = self.browse_mailboxes()
        mailbox_details = {}
        for path in paths:
            mailbox_details[path] = next((mailbox for mailbox in mailboxes if mailbox['aliasName'] == path), None)
        syntex_restore_items = []

        for key, value in mailbox_details.items():
            syntex_restore_items.append({
                "displayName": value["displayName"],
                "guid": value["user"]["userGUID"],
                "rawId": value["user"]["userGUID"],
                "restoreType": 1
            })

        # Get the current time in UTC
        current_time = datetime.datetime.now(datetime.timezone.utc)
        current_timestamp = int(current_time.timestamp())
        current_iso_format = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = {}
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"][
            "msSyntexRestoreOptions"] = {
            "msSyntexRestoreItems": {
                "listMsSyntexRestoreItems": syntex_restore_items
            },
            "restoreDate": {
                "time": current_timestamp,
                "timeValue": current_iso_format
            },
            "restorePointId": "",
            "restoreType": 1,
            "useFastRestorePoint": False
        }

        return self._process_restore_response(request_json)

    @staticmethod
    def _find_mailbox_query_params(query_params: Optional[dict] = None) -> list[dict[str, Any] | dict[str, Any]]:
        """Generate the query parameters for a find mailbox request.

        Args:
            query_params: Optional dictionary containing key-value pairs to include in the query.
                If None, default parameters will be used.

        Returns:
            A dictionary representing the JSON query parameters for the find mailbox request.

        Example:
            >>> params = UsermailboxSubclient._find_mailbox_query_params({'mailboxName': 'john.doe'})
            >>> print(params)
            {'mailboxName': 'john.doe'}

        #ai-gen-doc
        """
        final_params = []
        default_params = ExchangeConstants.FIND_MBX_QUERY_DEFAULT_PARAMS
        if query_params:
            for param, value in query_params.items():
                if param in default_params:
                    default_params.pop(value)
                final_params.append({"param": param, "value": value})
        for param, value in default_params.items():
            final_params.append({"param": param, "value": value})
        return final_params

    @staticmethod
    def _find_mailbox_facets(facets: Optional[List[str]] = None) -> list[dict[str, str | Any] | dict[str, Any]]:
        """Generate facet requests for a mailbox search query.

        Args:
            facets: Optional list of strings specifying the mailbox facets to include in the query.
                If None, no facets are included.

        Returns:
            Dictionary representing the JSON structure for the mailbox facets query.

        Example:
            >>> facets = ['Sender', 'Recipient', 'Date']
            >>> query_json = UsermailboxSubclient._find_mailbox_facets(facets)
            >>> print(query_json)
            >>> # Output will be a dictionary suitable for use in a mailbox search request

        #ai-gen-doc
        """
        final_params = []
        default_facet = ExchangeConstants.FIND_MBX_DEFAULT_FACET

        for facet in facets:
            if facet in default_facet:
                default_facet.remove(facet)
            final_params.append({"name": facet})
        for facet in default_facet:
            final_params.append({"name": facet})
        return final_params

    def find_mailbox(self, mailbox_smtp: str, **kwargs: dict) -> dict:
        """Perform a find operation to locate a mailbox by its SMTP address.

        Args:
            mailbox_smtp: The SMTP address of the mailbox to search for.
            **kwargs: Optional keyword arguments to customize the find operation.

        Returns:
            A dictionary containing the response JSON for the find mailbox operation.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> result = subclient.find_mailbox('user@example.com')
            >>> print(result)
            {'mailbox': {'smtp': 'user@example.com', 'status': 'found', ...}}

        #ai-gen-doc
        """

        data = ExchangeConstants.FIND_MAILBOX_REQUEST_DATA

        data["advSearchGrp"]["emailFilter"][0]["filter"]["filters"].append(
            {
                "field": "CUSTODIAN",
                "intraFieldOp": 0,
                "fieldValues": {
                    "values": [
                        mailbox_smtp
                    ]
                }
            }
        )
        data["advSearchGrp"]["galaxyFilter"][0]["appIdList"] = [int(self.subclient_id)]
        data["facetRequests"]["facetRequest"] = UsermailboxSubclient._find_mailbox_facets(
            kwargs.get("facets_params", None))
        data["searchProcessingInfo"]["pageSize"] = int(kwargs.get("page_size", 100))
        data["searchProcessingInfo"]["queryParams"] = UsermailboxSubclient._find_mailbox_query_params(
            kwargs.get("query_params", None))

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['DO_WEB_SEARCH'], data
        )
        if flag:
            if response and response.json():
                return response.json()
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_live_update_job_json(self) -> dict:
        """Create JSON structure for a live update job task.

        Returns:
            dict: A dictionary containing the task JSON structure for triggering a live update job.

        Example:
            >>> subclient = UsermailboxSubclient()
            >>> task_json = subclient._get_live_update_job_json()
            >>> print(task_json)
        """
        task_json = {
            "taskInfo": {
                "taskOperation": 1,
                "associations": [
                    {
                        "subclientId": int(self.subclient_id),
                        "entityType": 7,
                        "_SubclType_": 0,
                        "_type_": 7
                    }
                ],
                "task": {
                    "isEZOperation": False,
                    "description": "",
                    "ownerId": 1,
                    "runUserId": 1,
                    "taskType": 1,
                    "ownerName": "",
                    "alertName": "",
                    "sequenceNumber": 0,
                    "isEditing": False,
                    "GUID": "",
                    "isFromCommNetBrowserRootNode": False,
                    "initiatedFrom": 3,
                    "policyType": 0,
                    "associatedObjects": 0,
                    "taskName": ""
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskOrder": 0,
                            "subTaskType": 2,
                            "flags": 0,
                            "operationType": 5027,
                            "subTaskId": 1
                        }
                    }
                ]
            }
        }
        return task_json

    def live_update_job(self) -> None:
        """Trigger a live update job for the UserMailbox subclient.

         This method initiates a live update job to refresh and synchronize the subclient's
         mailbox content with the latest changes from the Exchange server.

         Raises:
             SDKException: If the response status code is not 200 or if the API request fails.

         Example:
             >>> subclient = UsermailboxSubclient()
             >>> subclient.live_update_job()
             >>> print("Live update job triggered successfully.")


        #ai-gen-doc
        """
        task_json = self._get_live_update_job_json()
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json)
        if flag:
            if not response.status_code == 200:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))