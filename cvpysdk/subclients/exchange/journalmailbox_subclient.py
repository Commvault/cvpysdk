# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

from past.builtins import basestring

from ...exception import SDKException
from ..exchsubclient import ExchangeSubclient


class JournalMailboxSubclient(ExchangeSubclient):
    """Derived class from ExchangeSubclient Base class.

        This represents a JournalMailbox subclient,
        and can perform discover and restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given JournalMailbox Subclient.

            Args:
                backupset_object    (object)    --  instance of the backupset class

                subclient_name      (str)       --  subclient name

                subclient_id        (int)       --  subclient id

        """
        super(JournalMailboxSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._discover_journal_users = None
        self._client_object = self._instance_object._agent_object._client_object
        self._SET_EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'SET_EMAIL_POLICY_ASSOCIATIONS']

        self.refresh()

    def _get_discover_journal_users(self):
        """Gets the discovered users from the Subclient .

            Returns:
                list    -   list of discovered users associated with the subclient

        """
        self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY'] % (
            int(self._backupset_object.backupset_id), 'Journal Mailbox')

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._DISCOVERY)

        if flag:
            discover_content = response.json()
            if 'discoverInfo' in discover_content.keys():

                if 'mailBoxes' in discover_content['discoverInfo']:
                    self._discover_journal_users = discover_content['discoverInfo']['mailBoxes']

            return self._discover_journal_users

        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_journal_user_assocaitions(self):
        """Gets the appropriate journal users associations from the Subclient.

            Returns:
                list    -   list of users associated with the subclient

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
                        'retention_policy': retention_policy
                    }

                    users.append(temp_dict)

        return users

    def _set_association_request(self, associations_json):
        """Runs the emailAssociation as API to set association

            Args:
                associations_json    (dict)  -- request json sent as payload

            Returns:
                (str, str):
                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
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
    def discover_journal_users(self):
        """"Returns the list of discovered journal users for the JournalMailbox subclient."""
        return self._discover_journal_users

    @property
    def journal_users(self):
        """Returns the list of journal users associated with JournalMailbox subclient."""
        return self._journal_users

    def set_journal_user_assocaition(self, subclient_content):
        """Create Journal assocaition for JournalMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the Users to add to the subclient

                    subclient_content = {

                        'mailboxNames' : ["AutoCi2"],

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
                    "mailBoxes": users
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

        self._set_association_request(associations_json)

    def set_pst_assocaition(self, subclient_content):
        """Create PST assocaition for JournalMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the pst to add to the subclient

                    subclient_content = {

                            'pstTaskName' : "Task Name for PST",

                            'folders' : ['list of folders'],

                            'pstOwnerManagement' : {

                                'defaultOwner': "default owner if no owner is determined",

                                'pstDestFolder': "ingest psts under this folder",

                                'usePSTNameToCreateChild': Boolean
                            }
                        }

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
            _assocaition_json_ = {
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

    def refresh(self):
        """Refresh the Journal Mailbox Subclient."""
        self._get_subclient_properties()
        self._discover_journal_users = self._get_discover_journal_users()
        self._journal_users = self._get_journal_user_assocaitions()
