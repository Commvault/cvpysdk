# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

from past.builtins import basestring

from ...exception import SDKException

from ..exchsubclient import ExchangeSubclient
from ...client import Client


class ContentStoreMailboxSubclient(ExchangeSubclient):
    """Derived class from ExchangeSubclient Base class.

        This represents a contentstoremailbox subclient,
        and can perform discover and restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given ContentStoreMailbox Subclient.

            Args:
                backupset_object    (object)    --  instance of the backupset class

                subclient_name      (str)       --  subclient name

                subclient_id        (int)       --  subclient id

        """
        super(
            ContentStoreMailboxSubclient,
            self).__init__(backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._client_object = self._instance_object._agent_object._client_object
        self._SET_EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'SET_EMAIL_POLICY_ASSOCIATIONS']

        self.refresh()

    def _get_content_store_assocaitions(self):
        """Gets the appropriate content store associations from the Subclient.

            Returns:
                list    -   list of content store mailbox associated with the subclient

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
    def _get_client_dict(client_object):
        """Returns the client dict for the client object to be appended to member server.

            Args:
                client_object   (object)    --  instance of the Client class

            Returns:
                dict    -   dictionary for a single client to be associated
        """
        client_dict = {
            "clientName": client_object.client_name,
            "clientId": int(client_object.client_id),
        }

        return client_dict

    def _content_store_servers(self, clients_list):
        """Returns the proxy clients to be associated .

            Args:
                clients_list (list)    --  list of the clients to associated

            Returns:
                list - list consisting of all member servers to be associated

            Raises:
                SDKException:
                    if type of clients list argument is not list
        """
        if not isinstance(clients_list, list):
            raise SDKException('Subclient', '101')

        content_store_servers = []

        for client in clients_list:
            if isinstance(client, basestring):
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
    def content_store_mailboxes(self):
        """"Returns the list of discovered users for the UserMailbox subclient."""
        return self._content_store_mailboxes

    def set_contentstore_assocaition(self, subclient_content):
        """Create User assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the Users to add to the subclient

                    subclient_content = {

                        'mailboxNames' : ["AutoCi2"],,

                        'contentStoreClients' : [shindex],

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy'
                    }

        """
        users = []

        if not isinstance(subclient_content, dict):
            raise SDKException('Subclient', '101')

        from ...policies.configuration_policies import ConfigurationPolicy

        if not (isinstance(subclient_content[
                'journal_policy'], (ConfigurationPolicy, basestring)) and
                isinstance(subclient_content[
                    'retention_policy'], (ConfigurationPolicy, basestring)) and
                isinstance(subclient_content['mailboxNames'], list)):
            raise SDKException('Subclient', '101')

        if isinstance(subclient_content['journal_policy'], ConfigurationPolicy):
            journal_policy = subclient_content['journal_policy']
        elif isinstance(subclient_content['journal_policy'], basestring):
            journal_policy = ConfigurationPolicy(
                self._commcell_object, subclient_content['journal_policy'])

        if isinstance(subclient_content['retention_policy'], ConfigurationPolicy):
            retention_policy = subclient_content['retention_policy']
        elif isinstance(subclient_content['retention_policy'], basestring):
            retention_policy = ConfigurationPolicy(
                self._commcell_object, subclient_content['retention_policy'])
        content_store_server = self._content_store_servers(
            subclient_content['contentStoreClients'])

        try:

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

    def refresh(self):
        """Refresh the User Mailbox Subclient."""
        self._get_subclient_properties()
        self._content_store_mailboxes = self._get_content_store_assocaitions()
