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

"""File for operating on a ContentStoreMailbox Subclient.

ContentStoreMailboxSubclient is the only class defined in this file.

ContentStoreMailboxSubclient:   Derived class from ExchangeMailboxSubclient Base class,
                                representing a ContentStoreMailbox subclient, and to
                                perform operations on that subclient

JournalMailboxSubclient:

    _get_subclient_properties()         --  gets the properties of UserMailbox Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of UserMailbox Subclient

    users()                             --  creates users association for subclient

    Databases()                         --  creates Db association for  the subclient

    Adgroups()                          --  creates Adgroup association for subclient

    restore_in_place()                  --  runs in-place restore for the subclient

"""

from __future__ import unicode_literals

from ...exception import SDKException

from ..exchsubclient import ExchangeSubclient
from ...client import Client


class ContentStoreMailboxSubclient(ExchangeSubclient):
    """
    Specialized subclient class for managing Content Store Mailbox operations within Exchange environments.

    This class extends the ExchangeSubclient base class to provide targeted functionality for
    content store mailbox subclients. It enables discovery, association management, and restoration
    operations specific to content store mailboxes. The class is designed to interact with backup sets,
    manage mailbox associations, and refresh subclient data as needed.

    Key Features:
        - Initialization with backup set, subclient name, and subclient ID
        - Retrieval of content store associations
        - Generation of client dictionaries for mailbox management
        - Identification and management of content store servers from client lists
        - Property access to content store mailboxes
        - Setting content store associations with support for policy usage
        - Refreshing subclient data to ensure up-to-date information

    #ai-gen-doc
    """

    def __init__(self, backupset_object: object, subclient_name: str, subclient_id: int = None) -> None:
        """Initialize a ContentStoreMailboxSubclient instance.

        Args:
            backupset_object: Instance of the backupset class associated with this subclient.
            subclient_name: The name of the ContentStoreMailbox subclient.
            subclient_id: Optional; the unique identifier for the subclient. If not provided, it will be determined automatically.

        Example:
            >>> backupset = Backupset(commcell_object, 'ExchangeBackupset')
            >>> subclient = ContentStoreMailboxSubclient(backupset, 'MailboxSubclient1')
            >>> print(f"Subclient created: {subclient}")

        #ai-gen-doc
        """
        super(
            ContentStoreMailboxSubclient,
            self).__init__(backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._client_object = self._instance_object._agent_object._client_object
        self._SET_EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'SET_EMAIL_POLICY_ASSOCIATIONS']

        self.refresh()

    def _get_content_store_assocaitions(self) -> list:
        """Retrieve the list of content store mailboxes associated with the subclient.

        Returns:
            list: A list containing the content store mailboxes associated with this subclient.

        Example:
            >>> subclient = ContentStoreMailboxSubclient()
            >>> associations = subclient._get_content_store_assocaitions()
            >>> print(f"Associated mailboxes: {associations}")

        #ai-gen-doc
        """
        users = []

        self._EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'GET_EMAIL_POLICY_ASSOCIATIONS'] % (self.subclient_id, 'ContentStore Mailbox')

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
                    display_name = str(child['contentStoreMailbox']['displayName'])
                    smtp_address = str(child['contentStoreMailbox']['smtpAdrress'])
                    user_guid = str(child['contentStoreMailbox']['user']['userGUID'])
                    is_auto_discover_user = str(
                        child['contentStoreMailbox']['isAutoDiscoveredUser'])
                    for policy in child['policies']['emailPolicies']:
                        if policy['detail'].get('emailPolicy', {}).get('emailPolicyType') == 4:
                            journal_policy = str(policy['policyEntity']['policyName'])
                        elif policy['detail'].get('emailPolicy', {}).get('emailPolicyType') == 3:
                            retention_policy = str(policy['policyEntity']['policyName'])

                    temp_dict = {
                        'display_name': display_name,
                        'smtp_address': smtp_address,
                        'user_guid': user_guid,
                        'is_auto_discover_user': is_auto_discover_user,
                        'journal_policy': journal_policy,
                        'retention_policy': retention_policy
                    }

                    users.append(temp_dict)

        return users

    @staticmethod
    def _get_client_dict(client_object: object) -> dict:
        """Generate a dictionary representation for a given client object.

        This static method creates a dictionary for the provided client object,
        which can be used to associate the client with a member server.

        Args:
            client_object: An instance of the Client class to be converted into a dictionary.

        Returns:
            dict: A dictionary containing information about the specified client.

        Example:
            >>> client = Client('client_name')
            >>> client_dict = ContentStoreMailboxSubclient._get_client_dict(client)
            >>> print(client_dict)
            {'clientName': 'client_name', ...}

        #ai-gen-doc
        """
        client_dict = {
            "clientName": client_object.client_name,
            "clientId": int(client_object.client_id),
        }

        return client_dict

    def _content_store_servers(self, clients_list: list) -> list:
        """Return the list of proxy clients (member servers) to be associated.

        Args:
            clients_list: List of client names or client objects to be associated as proxy clients.

        Returns:
            List containing all member servers to be associated as proxy clients.

        Raises:
            SDKException: If the provided clients_list argument is not of type list.

        Example:
            >>> subclient = ContentStoreMailboxSubclient()
            >>> servers = subclient._content_store_servers(['ClientA', 'ClientB'])
            >>> print(servers)
            ['ClientA', 'ClientB']

        #ai-gen-doc
        """
        if not isinstance(clients_list, list):
            raise SDKException('Subclient', '101')

        content_store_servers = []

        for client in clients_list:
            if isinstance(client, str):
                client = client.strip().lower()

                if self._commcell_object.clients.has_client(client):
                    temp_client = self._commcell_object.clients.get(client)

                    if temp_client.agents.has_agent('exchange mailbox (classic)'):
                        client_dict = self._get_client_dict(temp_client)
                        content_store_client_dict = {
                            "isActive": True,
                            "client": client_dict
                        }
                        content_store_servers.append(content_store_client_dict)

                    del temp_client
            elif isinstance(client, Client):
                if client.agents.has_agent('exchange mailbox (classic)'):
                    client_dict = self._get_client_dict(client)
                    content_store_client_dict = {
                        "isActive": True,
                        "client": client_dict
                    }
                    content_store_servers.append(content_store_client_dict)

        return content_store_servers

    @property
    def content_store_mailboxes(self) -> list:
        """Get the list of discovered users for the UserMailbox subclient.

        Returns:
            list: A list containing the discovered user mailboxes associated with this subclient.

        Example:
            >>> subclient = ContentStoreMailboxSubclient()
            >>> users = subclient.content_store_mailboxes
            >>> print(f"Discovered users: {users}")

        #ai-gen-doc
        """
        return self._content_store_mailboxes

    def set_contentstore_assocaition(self, subclient_content: dict, use_policies: bool = True) -> None:
        """Associate users with a UserMailboxSubclient using either policies or a plan.

        This method creates associations for user mailboxes in a ContentStoreMailboxSubclient.
        The association can be configured using either archiving, cleanup, and retention policies,
        or by specifying a plan, depending on the value of `use_policies`.

        Args:
            subclient_content: Dictionary containing user and association details. The structure should be:
                {
                    'mailboxNames': List of mailbox aliases (list of str),
                    'contentStoreClients': List of Content Store client names (list of str),
                    # If use_policies is True:
                    'archive_policy': Name of the archiving policy (str),
                    'cleanup_policy': Name of the cleanup policy (str),
                    'retention_policy': Name of the retention policy (str),
                    # If use_policies is False:
                    'plan_name': Name of the plan (str),
                    'plan_id': Optional plan ID (int or None)
                }
            use_policies: If True, uses the specified policies for association. If False, uses the specified plan.

        Example:
            >>> subclient_content = {
            ...     'mailboxNames': ['user1@domain.com', 'user2@domain.com'],
            ...     'contentStoreClients': ['CSClient1'],
            ...     'archive_policy': 'ArchivePolicy1',
            ...     'cleanup_policy': 'CleanupPolicy1',
            ...     'retention_policy': 'RetentionPolicy1'
            ... }
            >>> subclient.set_contentstore_assocaition(subclient_content, use_policies=True)
            >>>
            >>> # Using a plan instead of policies
            >>> subclient_content = {
            ...     'mailboxNames': ['user3@domain.com'],
            ...     'contentStoreClients': ['CSClient2'],
            ...     'plan_name': 'MailboxPlanA',
            ...     'plan_id': 123
            ... }
            >>> subclient.set_contentstore_assocaition(subclient_content, use_policies=False)

        #ai-gen-doc
        """
        users = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')
        try:
            content_store_server = self._content_store_servers(
                subclient_content['contentStoreClients'])

            for mailbox_item in subclient_content['mailboxNames']:
                mailbox_dict = {
                    'smtpAdrress': mailbox_item['smtpAdrress'],
                    'mailBoxType': 3,
                    'displayName': mailbox_item['displayName'],
                    'contentStoreClients': content_store_server

                }
                users.append(mailbox_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        if use_policies:
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
            associations_json = {
                "emailAssociation": {
                    "advanceOptions": {},
                    "subclientEntity": self._subClientEntity,
                    "emailDiscoverinfo": {
                        "discoverByType": 6,
                        "contentStoreMailboxes": users
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
                                    "policyId": int(retention_policy._configuration_policy_id),
                                    "policyName": retention_policy._configuration_policy_name
                                }
                            }
                        ]
                    }
                }
            }

        else:
            if 'plan_name' not in subclient_content:
                raise SDKException('Subclient', '102', "'plan_name' not given in content")

            if not self._commcell_object.plans.has_plan(subclient_content['plan_name']):
                raise SDKException('Subclient', '102',
                                   'Plan Name {} not found'.format(subclient_content['plan_name']))
            if 'plan_id' not in subclient_content or subclient_content['plan_id'] is None:
                plan_id = self._commcell_object.plans[subclient_content['plan_name'].lower()]
            else:
                plan_id = subclient_content['plan_id']

            associations_json = {
                "emailAssociation": {
                    "advanceOptions": {"enableAutoDiscovery": False},
                    "subclientEntity": self._subClientEntity,
                    "emailDiscoverinfo": {
                        "discoverByType": 6,
                        "contentStoreMailboxes": users
                    },
                    "emailStatus": 0,
                    "plan": {"planId": int(plan_id)}
                }
            }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', self._SET_EMAIL_POLICY_ASSOCIATIONS, associations_json
        )

        if flag:
            try:
                if response.json():
                    if response.json()['resp']['errorCode'] != 0:
                        error_message = response.json()['errorMessage']
                        output_string = 'Failed to create user assocaition\nError: "{0}"'
                        raise SDKException(
                            'Exchange Mailbox', '102', output_string.format(error_message)
                        )
                    else:
                        self.refresh()
            except ValueError:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Reload the state of the User Mailbox Subclient.

        This method refreshes the internal data and state of the User Mailbox Subclient,
        ensuring that any changes made externally are reflected in the current instance.

        Example:
            >>> subclient = ContentStoreMailboxSubclient()
            >>> subclient.refresh()
            >>> print("Subclient state refreshed successfully")

        #ai-gen-doc
        """
        self._get_subclient_properties()
        self._content_store_mailboxes = self._get_content_store_assocaitions()