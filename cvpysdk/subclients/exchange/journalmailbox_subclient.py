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

"""File for operating on a JournalMailbox Subclient.

JournalMailboxSubclient is the only class defined in this file.

JournalMailboxSubclient:   Derived class from ExchangeMailboxSubclient Base class, representing a
                            JournalMailbox subclient, and to perform operations on that subclient

JournalMailboxSubclient:

    users()                             --  creates users association for subclient

    restore_in_place()                  --  runs in-place restore for the subclient

"""

from __future__ import unicode_literals

from typing import List

from ...exception import SDKException
from ..exchsubclient import ExchangeSubclient
import time

class JournalMailboxSubclient(ExchangeSubclient):
    """
    Specialized subclient class for managing Journal Mailbox operations in Exchange environments.

    This class extends the ExchangeSubclient base class to provide functionality specific to
    Journal Mailbox subclients. It enables discovery, association, and restoration operations
    for journal users, as well as management of user associations and PST associations.

    Key Features:
        - Initialization with backup set, subclient name, and subclient ID
        - Discovery of journal users with support for refresh and retry mechanisms
        - Retrieval and management of journal user associations
        - Setting associations using JSON payloads and plan details
        - Properties for accessing discovered journal users and current journal users
        - Methods to set journal user and PST associations, optionally using policies
        - Refresh capability to update subclient state

    Intended Usage:
        Use this class to automate and manage Journal Mailbox subclient operations, including
        user discovery, association management, and restoration tasks within an Exchange backup set.

    #ai-gen-doc
    """

    def __init__(self, backupset_object: object, subclient_name: str, subclient_id: int = None) -> None:
        """Initialize a JournalMailboxSubclient instance.

        Args:
            backupset_object: Instance of the backupset class associated with this subclient.
            subclient_name: Name of the JournalMailbox subclient.
            subclient_id: Optional; unique identifier for the subclient. If not provided, it will be determined automatically.

        Example:
            >>> backupset = Backupset(commcell_object, 'Exchange', 'BackupSet1')
            >>> subclient = JournalMailboxSubclient(backupset, 'JournalSubclient01', subclient_id=123)
            >>> print(f"Subclient '{subclient_name}' initialized successfully.")

        #ai-gen-doc
        """
        super(JournalMailboxSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._discover_journal_users = None
        self._client_object = self._instance_object._agent_object._client_object
        self._SET_EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'SET_EMAIL_POLICY_ASSOCIATIONS']

        self.refresh()

    def _get_discover_journal_users(self, use_without_refresh_url: bool = False, retry_attempts: int = 0) -> list:
        """Retrieve the list of discovered users associated with the journal mailbox subclient.

        Args:
            use_without_refresh_url: If True, performs discovery without refreshing the cache.
            retry_attempts: Number of retry attempts for the discovery operation.

        Returns:
            list: A list of discovered users associated with the subclient.

        Example:
            >>> users = subclient._get_discover_journal_users(use_without_refresh_url=True, retry_attempts=2)
            >>> print(f"Discovered users: {users}")

        #ai-gen-doc
        """
        self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY'] % (
            int(self._backupset_object.backupset_id), 'Journal Mailbox')

        if use_without_refresh_url:
            self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY_WITHOUT_REFRESH'] % (
                int(self._backupset_object.backupset_id), 'Journal Mailbox'
            )

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._DISCOVERY)

        if flag:
            if response and response.json():
                discover_content = response.json()
                _error_code = discover_content.get('resp', {}).get('errorCode', 0)
                if _error_code == 469762468 or _error_code == 469762470:
                    time.sleep(60) # the results might take some time depending on domains
                    if retry_attempts > 10:
                        raise SDKException('Subclient', '102', 'Failed to perform discovery.')

                    return self._get_discover_journal_users(use_without_refresh_url=True ,
                                                            retry_attempts=retry_attempts + 1)

                if 'discoverInfo' in discover_content.keys():

                    if 'mailBoxes' in discover_content['discoverInfo']:
                        self._discover_journal_users = discover_content['discoverInfo']['mailBoxes']

                        return self._discover_journal_users
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_journal_user_assocaitions(self) -> List[str]:
        """Retrieve the list of journal user associations for this Subclient.

        Returns:
            List of user names (as strings) associated with the subclient for journaling purposes.

        Example:
            >>> subclient = JournalMailboxSubclient()
            >>> user_list = subclient._get_journal_user_assocaitions()
            >>> print(f"Associated users: {user_list}")
            >>> # Output might be: ['user1@example.com', 'user2@example.com']

        #ai-gen-doc
        """
        users = []
        self._EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'GET_EMAIL_POLICY_ASSOCIATIONS'] % (self.subclient_id, 'Journal Mailbox')

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._EMAIL_POLICY_ASSOCIATIONS
        )

        if flag:
            subclient_content = response.json()

            if 'associations' in subclient_content:
                children = subclient_content['associations']

                for child in children:
                    journal_policy = None
                    retention_policy = None
                    display_name = str(child['userMailBoxInfo']['displayName'])
                    alias_name = str(child['userMailBoxInfo']['aliasName'])
                    smtp_address = str(child['userMailBoxInfo']['smtpAdrress'])
                    database_name = str(child['userMailBoxInfo']['databaseName'])
                    exchange_server = str(child['userMailBoxInfo']['exchangeServer'])
                    user_guid = str(child['userMailBoxInfo']['user']['userGUID'])
                    is_auto_discover_user = str(child['userMailBoxInfo']['isAutoDiscoveredUser'])

                    for policy in child['policies']['emailPolicies']:
                        if policy['detail'].get('emailPolicy', {}).get('emailPolicyType') == 4:
                            journal_policy = str(policy['policyEntity']['policyName'])
                        elif policy['detail'].get('emailPolicy', {}).get('emailPolicyType') == 3:
                            retention_policy = str(policy['policyEntity']['policyName'])

                    temp_dict = {
                        'display_name': display_name,
                        'alias_name': alias_name,
                        'smtp_address': smtp_address,
                        'database_name': database_name,
                        'exchange_server': exchange_server,
                        'user_guid': user_guid,
                        'is_auto_discover_user': is_auto_discover_user,
                        'journal_policy': journal_policy,
                        'retention_policy': retention_policy,
                    }
                    if child['plan'].get('planName', None):
                        temp_dict['plan']= child['plan']['planName']

                    users.append(temp_dict)

        return users

    def _set_association_request(self, associations_json: dict) -> tuple[str, str]:
        """Send an email association request using the provided JSON payload.

        This method runs the emailAssociation API to set associations for the JournalMailboxSubclient.
        It returns the error code and error message received in the response.

        Args:
            associations_json: Dictionary containing the request payload for the association API.

        Returns:
            A tuple containing:
                str: The error code received in the response.
                str: The error message received in the response.

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> payload = {"mailboxIds": [123, 456], "associationType": "user"}
            >>> error_code, error_message = subclient._set_association_request(payload)
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

    @property
    def discover_journal_users(self) -> list:
        """Get the list of discovered journal users for the JournalMailbox subclient.

        Returns:
            list: A list containing the discovered journal users associated with this JournalMailbox subclient.

        Example:
            >>> subclient = JournalMailboxSubclient()
            >>> users = subclient.discover_journal_users  # Use dot notation for property access
            >>> print(f"Discovered users: {users}")

        #ai-gen-doc
        """
        return self._discover_journal_users

    @property
    def journal_users(self) -> List[str]:
        """Get the list of journal users associated with the JournalMailbox subclient.

        Returns:
            List of strings representing the email addresses or usernames of journal users.

        Example:
            >>> subclient = JournalMailboxSubclient()
            >>> users = subclient.journal_users  # Use dot notation for property access
            >>> print(f"Journal users: {users}")
            >>> # Output might be: ['user1@example.com', 'user2@example.com']

        #ai-gen-doc
        """
        return self._journal_users

    def _association_json(self, subclient_content: dict) -> dict:
        """Construct the association JSON payload for creating an association in a UserMailbox Subclient.

        This method generates a dictionary representing the association configuration,
        typically including archiving, cleanup, and retention policies for the subclient.
        The input should be a dictionary specifying the relevant policies or users.

        Args:
            subclient_content: Dictionary containing the users or policies to associate with the subclient.
                For example:
                    {
                        'archive_policy': "CIPLAN Archiving policy",
                        'cleanup_policy': "CIPLAN Clean-up policy",
                        'retention_policy': "CIPLAN Retention policy"
                    }

        Returns:
            Dictionary representing the association JSON request to be passed to the API.

        Example:
            >>> subclient = JournalMailboxSubclient()
            >>> content = {
            ...     'archive_policy': "CIPLAN Archiving policy",
            ...     'cleanup_policy': "CIPLAN Clean-up policy",
            ...     'retention_policy': "CIPLAN Retention policy"
            ... }
            >>> association_json = subclient._association_json(content)
            >>> print(association_json)
            # Output will be a dictionary suitable for the API request

        #ai-gen-doc
        """
        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        from ...policies.configuration_policies import ConfigurationPolicy

        if not (isinstance(subclient_content[
                'journal_policy'], (ConfigurationPolicy, str)) and
                isinstance(subclient_content[
                    'retention_policy'], (ConfigurationPolicy, str)) and
                isinstance(subclient_content['mailboxNames'], list)):
            raise SDKException('Subclient', '101')

        if isinstance(subclient_content['journal_policy'], ConfigurationPolicy):
            journal_policy = subclient_content['journal_policy']
        elif isinstance(subclient_content['journal_policy'], str):
            journal_policy = ConfigurationPolicy(
                self._commcell_object, subclient_content['journal_policy'])

        if isinstance(subclient_content['retention_policy'], ConfigurationPolicy):
            retention_policy = subclient_content['retention_policy']
        elif isinstance(subclient_content['retention_policy'], str):
            retention_policy = ConfigurationPolicy(
                self._commcell_object, subclient_content['retention_policy'])

        try:
            discover_journal_users = self.discover_journal_users

            for mailbox_item in subclient_content['mailboxNames']:

                for mb_item in discover_journal_users:

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
                            'user': {
                                '_type_': 13,
                                'userGUID': mb_item['user']['userGUID']
                            }
                        }
                        users.append(mailbox_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        associations_json = {
            "emailAssociation": {
                "advanceOptions": {},
                "subclientEntity": self._subClientEntity,
                "emailDiscoverinfo": {
                    "discoverByType": 5,
                    "mailBoxes": None
                },
                "policies": {
                    "emailPolicies": [
                        {
                            "policyType": 1,
                            "flags": 0,
                            "agentType": {
                                "appTypeId": 137
                            },
                            "detail": {
                                "emailPolicy": {
                                    "emailPolicyType": 4
                                }
                            },
                            "policyEntity": {
                                "policyId": int(journal_policy.configuration_policy_id),
                                "policyName": journal_policy.configuration_policy_name
                            }

                        },
                        {
                            "policyType": 1,
                            "flags": 0,
                            "agentType": {
                                "appTypeId": 137
                            },
                            "detail": {
                                "emailPolicy": {
                                    "emailPolicyType": 3
                                }
                            },
                            "policyEntity": {
                                "policyId": int(retention_policy.configuration_policy_id),
                                "policyName": retention_policy.configuration_policy_name
                            }
                        }
                    ]
                }
            }
        }

        return associations_json

    def _association_json_with_plan(self, plan_details: dict) -> dict:
        """Construct the association JSON payload using the provided plan details for creating an association in a UserMailbox Subclient.

        Args:
            plan_details: A dictionary containing plan information. Expected keys:
                - 'plan_name' (str): The name of the plan.
                - 'plan_id' (Optional[int]): The ID of the plan, or None if not specified.

        Returns:
            dict: The association JSON request payload to be sent to the API.

        Example:
            >>> plan_info = {'plan_name': 'ExchangePlan', 'plan_id': 1234}
            >>> assoc_json = subclient._association_json_with_plan(plan_info)
            >>> print(assoc_json)
            # Output will be a dictionary formatted for the API association request

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

    def set_journal_user_assocaition(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Create a journal association for the JournalMailboxSubclient.

        This method associates users or mailboxes with the JournalMailboxSubclient, using either policies or plans
        based on the `use_policies` flag. The association details are provided in the `subclient_content` dictionary.

        Args:
            subclient_content: Dictionary containing details of the users or mailboxes to associate. The expected keys are:
                - 'mailboxNames': List of mailbox names to add (e.g., ["AutoCi2"]).
                - 'archive_policy': Name of the archive policy to use.
                - 'cleanup_policy': Name of the cleanup policy to use.
                - 'retention_policy': Name of the retention policy to use.
                - If `use_policies` is False, also include:
                    - 'plan_name': Name of the Exchange plan.
                    - 'plan_id': Integer plan ID or None (optional).
            use_policies: If True, use policies for association; if False, use plans.
                Defaults to True.

        Example:
            >>> subclient_content = {
            ...     'mailboxNames': ['user1@example.com', 'user2@example.com'],
            ...     'archive_policy': 'Corporate Archive Policy',
            ...     'cleanup_policy': 'Corporate Cleanup Policy',
            ...     'retention_policy': 'Corporate Retention Policy'
            ... }
            >>> subclient.set_journal_user_assocaition(subclient_content)
            >>>
            >>> # Using plans instead of policies
            >>> subclient_content = {
            ...     'mailboxNames': ['user3@example.com'],
            ...     'plan_name': 'Exchange Plan Name',
            ...     'plan_id': 12345
            ... }
            >>> subclient.set_journal_user_assocaition(subclient_content, use_policies=False)

        #ai-gen-doc
        """
        users = []



        try:
            discover_journal_users = self.discover_journal_users

            for mailbox_item in subclient_content['mailboxNames']:

                for mb_item in discover_journal_users:

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
                            'user': {
                                '_type_': 13,
                                'userGUID': mb_item['user']['userGUID']
                            }
                        }
                        users.append(mailbox_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        if use_policies:
            _association_json_ = self._association_json(subclient_content)
            _association_json_["emailAssociation"]["emailDiscoverinfo"]["mailBoxes"] = users
        else:
            _association_json_ = self._association_json_with_plan(subclient_content)
            _association_json_["emailAssociation"]["emailDiscoverinfo"] = {"discoverByType":5, "mailBoxes" : users}
        self._set_association_request(_association_json_)

    def set_pst_assocaition(self, subclient_content: dict) -> None:
        """Create a PST association for the JournalMailboxSubclient.

        This method associates a PST (Personal Storage Table) with the JournalMailboxSubclient
        by specifying the PST task name, folders to include, and owner management options.

        Args:
            subclient_content: Dictionary containing PST association details. The expected format is:
                {
                    'pstTaskName': str,  # Name for the PST task
                    'folders': list,     # List of folder names to include
                    'pstOwnerManagement': {
                        'defaultOwner': str,            # Default owner if no owner is determined
                        'pstDestFolder': str,           # Destination folder for ingested PSTs
                        'usePSTNameToCreateChild': bool # Whether to use PST name to create a child folder
                    }
                }

        Example:
            >>> subclient_content = {
            ...     'pstTaskName': "Import PST Task",
            ...     'folders': ["Inbox", "Sent Items"],
            ...     'pstOwnerManagement': {
            ...         'defaultOwner': "user@example.com",
            ...         'pstDestFolder': "ImportedPSTs",
            ...         'usePSTNameToCreateChild': True
            ...     }
            ... }
            >>> subclient.set_pst_assocaition(subclient_content)
            >>> print("PST association created successfully.")

        #ai-gen-doc
        """
        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        try:

            if 'createPstDestFolder' not in subclient_content['pstOwnerManagement']:
                subclient_content['pstOwnerManagement']['createPstDestFolder'] = True
            if 'pstDestFolder' not in subclient_content['pstOwnerManagement']:
                subclient_content['pstOwnerManagement']['pstDestFolder'] = (f'Archived From '
                                                                            f'Automation')

            pst_dict = {
                'pstTaskName': subclient_content['pstTaskName'],
                'taskType': 1,
                'folders': subclient_content['folders'],
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
                }
            }

            subclient_entity = {"_type_": 7, "subclientId": int(self._subclient_id)}
            discover_info = {
                'discoverByType': 9,
                'pstIngestion': pst_dict
            }
            _associations_json = {
                "emailAssociation":
                    {
                        "emailDiscoverinfo": discover_info,
                        "subclientEntity": subclient_entity
                    }
            }

            self._set_association_request(_associations_json)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))
        except Exception as excp:
            raise excp

    def refresh(self) -> None:
        """Reload the Journal Mailbox Subclient information.

        This method refreshes the internal state of the JournalMailboxSubclient instance,
        ensuring that any changes made externally are reflected in the object.

        Example:
            >>> subclient = JournalMailboxSubclient()
            >>> subclient.refresh()  # Updates the subclient's information from the source
            >>> print("Subclient refreshed successfully")
        #ai-gen-doc
        """
        self._get_subclient_properties()
        self._discover_journal_users = self._get_discover_journal_users()
        self._journal_users = self._get_journal_user_assocaitions()
