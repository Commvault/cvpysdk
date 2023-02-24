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



User Mailbox Subclient Instance Attributes:
==============================

    discover_users                          --  Dictionary of users discovered
    discover_databases                      --  Dictionary of databases discovered
    adgroups                                --  Dictionary of discovered AD Groups
    o365groups                              --  Dictionary of discovered Office 365 Groups
"""

from __future__ import unicode_literals

from ...exception import SDKException

from ..exchsubclient import ExchangeSubclient

from ...subclient import Subclients

from ...backupset import Backupsets

import time


class UsermailboxSubclient(ExchangeSubclient):
    """Derived class from ExchangeSubclient Base class.

        This represents a usermailbox subclient,
        and can perform discover and restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given UserMailbox Subclient.

            Args:
                backupset_object    (object)    --  instance of the backupset class

                subclient_name      (str)       --  subclient name

                subclient_id        (int)       --  subclient id

        """
        super(UsermailboxSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

        self._instance_object = backupset_object._instance_object
        self._client_object = self._instance_object._agent_object._client_object
        self._SET_EMAIL_POLICY_ASSOCIATIONS = self._commcell_object._services[
            'SET_EMAIL_POLICY_ASSOCIATIONS']

        self.refresh()

    def _policy_json(self, configuration_policy, policy_type):
        """Creates policy Json based on configuration_policy name
        and policy_type

            Args:
                configuration_policy (str/object)  --  configuration policy name or
                object of congiguration policy class
                policy_type   (int)                --  configuration policy type

            Returns:
                list - list of the appropriate JSON for an agent to send to
                       the POST Subclient API
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

    def _association_json(self, subclient_content, is_o365group=False):
        """Constructs association json to create assocaition in UserMailbox Subclient.

            Args:
                subclient_content (dict)  --  dict of the Users to add to the subclient
                                             (dict of only policies in case of Office 365 groups)
                subclient_content = {

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy'
                    }


            Returns:
                dict -- Association JSON request to pass to the API
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

    def _association_json_with_plan(self, plan_details):
        """Constructs association json with plan to create association in UserMailbox Subclient.
        
            Args: plan_details = {
                    'plan_name': Plan Name,
                    'plan_id': int or None (Optional)
                    }
                 Returns:
                    dict -- Association JSON request to pass to the API
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

    def _association_mailboxes_json(self, mailbox_alias_names):
        """
            Args:
                mailbox_alias_names(list): alias names of the mailboxes to backup
                    Example:
                        ['aj', 'tkumar']
            Returns:
                mailboxes_json(list): Required details of mailboxes to backup
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

    def _task_json_for_backup(self, mailbox_alias_names):
        """
        Args:
            mailbox_alias_names(list): alias names of the mailboxes to backup
                Sample Values
                    ['aj', 'tkumar']
        Returns:
            task_json(dict): Task json required to pass to the API
        """
        task_json = self._backup_json('Full', False, '')
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

    def _set_association_request(self, associations_json):
        """
            Runs the emailAssociation POST API to set association

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

    def _update_association_request(self, associations_json):
        """Runs the EmailAssocaition PUT API to update association

            Args:
                associations_json  (dict)  -- request json sent as payload

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

    def _get_discover_users(self, use_without_refresh_url=False, retry_attempts=0):
        """Gets the discovered users from the Subclient .

            Args:
                use_without_refresh_url (boolean)   -   discovery without refresh cache

                retry_attempts(int)                 - retry for discovery

            Returns:
                list    -   list of discovered users associated with the subclient

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
                    time.sleep(10)  # the results might take some time depending on domains
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

    def _get_discover_database(self):
        """Gets the discovered databases from the Subclient .

            Returns:
                list    -   list of discovered databases associated with the subclient

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

    def _get_discover_adgroups(self):
        """Gets the discovered adgroups from the Subclient .

            Returns:
                list    -   list of discovered adgroups associated with the subclient

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

    def _get_user_assocaitions(self):
        """Gets the appropriate users associations from the Subclient.

            Returns:
                list    -   list of users and groups associated with the subclient

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
                    archive_policy = None
                    cleanup_policy = None
                    retention_policy = None
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
                    if 'emailPolicies' in child['policies']:
                        for policy in child['policies']['emailPolicies']:
                            if policy['detail'].get('emailPolicy', {}).get('emailPolicyType') == 1:
                                archive_policy = str(policy['policyEntity']['policyName'])
                            elif policy['detail'].get('emailPolicy', {}).get('emailPolicyType') == 2:
                                cleanup_policy = str(policy['policyEntity']['policyName'])
                            elif policy['detail'].get('emailPolicy', {}).get('emailPolicyType') == 3:
                                retention_policy = str(policy['policyEntity']['policyName'])
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
                        'archive_policy': archive_policy,
                        'cleanup_policy': cleanup_policy,
                        'retention_policy': retention_policy,
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

    def _get_database_associations(self):
        """Gets the appropriate database association from the Subclient.

            Returns:
                list    -   list of database associated with the subclient

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

    def _get_adgroup_assocaitions(self):
        """Gets the appropriate adgroup assocaitions from the Subclient.

            Returns:
                list    -   list of adgroups associated with the subclient

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
                    archive_policy = None
                    cleanup_policy = None
                    retention_policy = None
                    adgroup_name = str(child['adGroupsInfo']['adGroupName'])
                    is_auto_discover_user = str(child['additionalOptions']['enableAutoDiscovery'])

                    for policy in child['policies']['emailPolicies']:
                        if policy['detail']['emailPolicy']['emailPolicyType'] == 1:
                            archive_policy = str(policy['policyEntity']['policyName'])
                        elif policy['detail']['emailPolicy']['emailPolicyType'] == 2:
                            cleanup_policy = str(policy['policyEntity']['policyName'])
                        elif policy['detail']['emailPolicy']['emailPolicyType'] == 3:
                            retention_policy = str(policy['policyEntity']['policyName'])

                    temp_dict = {
                        'adgroup_name': adgroup_name,
                        'is_auto_discover_user': is_auto_discover_user,
                        'archive_policy': archive_policy,
                        'cleanup_policy': cleanup_policy,
                        'retention_policy': retention_policy
                    }

                    adgroups.append(temp_dict)

        return adgroups

    def _backup_generic_items_json(self, subclient_content):
        """
            Create the JSON for Backing Up the Generic Items of any Exchange Online Client

            Args:
                subclient_content   (list)  List having dictionary of items to be backed up

                subclient_content = [
                    {
                    "associationName" : "All Public Folders",
                    "associationType":12
                    },
                    {
                    "associationName" : "All Users",
                    "associationType":12
                    }
                ]

            Returns:
                The JSON to create a backup task
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
    def discover_users(self):
        """"Returns the list of discovered users for the UserMailbox subclient."""
        return self._discover_users

    @property
    def discover_databases(self):
        """Returns the list of discovered databases for the UserMailbox subclient."""
        return self._discover_databases

    @property
    def discover_adgroups(self):
        """Returns the list of discovered AD groups for the UserMailbox subclient."""
        return self._discover_adgroups

    @property
    def users(self):
        """Returns the list of users associated with UserMailbox subclient."""
        return self._users

    @property
    def databases(self):
        """Returns the list of databases associated with the UserMailbox subclient."""
        return self._databases

    @property
    def adgroups(self):
        """Returns the list of AD groups associated with the UserMailbox subclient."""
        return self._adgroups

    @property
    def o365groups(self):
        """Returns the list of discovered O365 groups for the UserMailbox subclient."""
        return self._o365groups

    def set_user_assocaition(self, subclient_content, use_policies=True):
        """Create User assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the Users to add to the subclient

                    subclient_content = {

                        'mailboxNames' : ["AutoCi2"],,

                        -- if use_policies is True --

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy'

                        -- if use_policies is False --

                        'plan_name': 'Exchange Plan Name',

                        'plan_id': int or None (Optional)
                        --
                    }

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

    def set_pst_association(self, subclient_content):
        """Create PST assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the pst to add to the subclient

                    subclient_content = {

                        'pstTaskName' : "Task Name for PST",

                        'folders' : ['list of folders'] //If pst ingestion by folder location,
                        'fsContent': Dictionary of client, backupset, subclient
                        Ex: {'client1':{'backupset1':[subclient1], 'backupset2':None},
                            'client2': None}
                        This would add subclient1, all subclients under backupset2 and
                        all backupsets under client2 to the association

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

    def set_fs_association_for_pst(self, association):
        """Helper method to create pst association for PST Ingestion by FS
            Args:
                association(dict) -- Dictionary of client, backupset, subclient
                                    Ex: {'client1':{'backupset1':[subclient1], 'backupset2':None},
                                        'client2': None}
                                    This would add subclient1, all subclients under backupset2 and
                                    all backupsets under client2 to the association
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

    def set_database_assocaition(self, subclient_content):
        """Create Database assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the databases to add to the subclient

                    subclient_content = {

                        'databaseNames' : ["SGDB-1"],

                        'is_auto_discover_user' : True,

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy',
                    }
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
        _assocaition_json_ = self._association_json(subclient_content)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_assocaition_json_)

    def set_adgroup_associations(self, subclient_content):
        """Create Ad groups assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the adgroups to add to the subclient

                    subclient_content = {

                        'adGroupNames' : ["_Man5_Man5_"],

                        'is_auto_discover_user' : True,

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy',
                    }

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
        _assocaition_json_ = self._association_json(subclient_content)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_assocaition_json_)

    def set_o365group_asscoiations(self, subclient_content):
        """Create O365 Group association for UserMailboxSubclient.
            Args:
                subclient_content   (dict)  --  dict of the policies to associate

                    subclient_content = {

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy'
                    }
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
        _assocaition_json_ = self._association_json(subclient_content, True)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_assocaition_json_)

    def delete_user_assocaition(self, subclient_content, use_policies=True):
        """delete User assocaition for UserMailboxSubclient.
            Args:
                subclient_content   (dict)  --  dict of the Users to delete from subclient
                    subclient_content = {
                        'mailboxNames' : ["AutoCi2"],
                        -- if use_policies is True --
                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy'
                        --
                        -- if use_policies is False --
                        'plan_name': Plan Name,
                        'plan_id': int or None (Optional)
                        --
                    }
                use_policies (bool) -- If True uses policies else uses Plan
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
                            # "msExchRecipientTypeDetails": mb_item['msExchRecipientTypeDetails'],
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

    def delete_o365group_association(self, subclient_content):
        """delete O365 group association for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the Users to delete from subclient

                    subclient_content = {

                        'mailboxNames' : ["AutoCi2"],

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy'
                    }

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

    def delete_database_assocaition(self, subclient_content):
        """Deletes Database assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the databases to delete from subclient

                    subclient_content = {

                        'databaseNames' : ["SGDB-1"],

                        'is_auto_discover_user' : True,

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy',
                    }
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
        _assocaition_json_ = self._association_json(subclient_content)
        _assocaition_json_["emailAssociation"]["emailStatus"] = 1
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._update_association_request(_assocaition_json_)

    def delete_adgroup_assocaition(self, subclient_content):
        """Deletes Ad groups assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the adgroups to delete from subclient

                    subclient_content = {

                        'adGroupNames' : ["_Man5_Man5_"],

                        'is_auto_discover_user' : True,

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy',
                    }

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
        _assocaition_json_ = self._association_json(subclient_content)
        _assocaition_json_["emailAssociation"]["emailStatus"] = 1
        _assocaition_json_["emailAssociation"]["advanceOptions"]["enableAutoDiscovery"] = subclient_content[
            "is_auto_discover_user"]
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_assocaition_json_)

    def enable_allusers_associations(self, subclient_content):
        """Enable all users assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the policies which needs to be
                assigned to all user assocaitions

                    subclient_content = {

                        'is_auto_discover_user' : True

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy',
                    }

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
        _assocaition_json_ = self._association_json(subclient_content)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_assocaition_json_)

    def disable_allusers_associations(self):
        """Disables alluser assocaition for UserMailboxSubclient."""
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
        _assocaition_json_ = self._association_json(subclient_content)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        _assocaition_json_["emailAssociation"]["emailStatus"] = 2
        self._set_association_request(_assocaition_json_)

    def enable_auto_discover_association(self, association_name, plan_name):
        """Enable all users assocaition for UserMailboxSubclient.

                    Args:
                        association_name  (str)  --  Type of auto discover association
                            Valid Values:
                                "All Users"
                                "All O365 Mailboxes"
                                "All Public Folders"

                        plan_name  (str)  --  Name of the plan to associate with users/groups


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

    def delete_auto_discover_association(self, association_name, subclient_content, use_policies=True):
        """
            Delete all users association for UserMailboxSubclient.

                    Args:
                        association_name  (str)  --  Type of auto discover association
                            Valid Values:
                                "All Users"
                                "All O365 Mailboxes"
                                "All Public Folders"

                        subclient_content (dict) - containing the information of users/groups

                            if use_policies is True

                                subclient_content={
                                    "is_auto_dicover_user" (bool): True
                                    "archive_policy" (obj): Archive Policy object
                                    "cleanup_policy" (obj): Cleanup Policy Object
                                    "retention_policy" (obj): Retention Policy Object
                                }

                            if use_policies is False

                                subclient_content={
                                    "is_auto_discover_user" (bool): True,
                                    "plan_name" (str): Name of the exchange plan
                                }


        """
        if not (isinstance(subclient_content, dict)):
            raise SDKException("Subclient", "101")

        association_dict = {"all users": 8,
                            "all o365 group mailboxes": 11,
                            "all public folders": 12
                            }

        if association_name.lower() not in association_dict:
            raise SDKException("Subclient", "102", "Invalid Association Name supplied")

        if use_policies == True:
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

    def enable_ews_support(self, service_url):
        """This function provides support for EWS protocol to backup on-prem mailboxes
            Args:
                service_url (string) -- EWS Connection URL for your exchange server
            Returns: None
        """
        self.agentproperties = self._agent_object.properties
        self.agentproperties["onePassProperties"]["onePassProp"]["ewsDetails"]["bUseEWS"] = True
        self.agentproperties["onePassProperties"]["onePassProp"]["ewsDetails"]["ewsConnectionUrl"] = service_url
        self._agent_object.update_properties(self.agentproperties)

    def browse_mailboxes(self, retry_attempts=0):
        """
        This function returns the mailboxes available for OOP restore
        return: dictionary containing mailbox info
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

    def backup_generic_items(self, subclient_content):
        """
            Backups the Generic Items for any Exchange Online Client
            GGeneric Items:
                All Public Folders/ All O365 Group ailboxes/ All Users

            Args:
                subclient_content   (list)  List having dictionary of items to be backed up

                subclient_content = [
                    {
                    "associationName" : "All Public Folders",
                    "associationType":12
                    },
                    {
                    "associationName" : "All Users",
                    "associationType":12
                    }
                ]
        """
        task_dict = self._backup_generic_items_json(subclient_content=subclient_content)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._services['CREATE_TASK'], task_dict
        )

        return self._process_backup_response(flag, response)

    def backup_mailboxes(self, mailbox_alias_names):
        """
        Backup specific mailboxes.
        Args:
            mailbox_alias_names(list): alias names of all the mailboxes to backup
                Sample Values:
                    ['aj', 'tkumar']
        Returns:
            job(Job): instance of job class for the backup job
        """
        task_json = self._task_json_for_backup(mailbox_alias_names)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)

    def create_recovery_point(self, mailbox_prop, job=None, job_id=None):
        """
            Method to create a recovery point

            Arguments:
                mailbox_prop        (dict)--    Dictionary of mailbox properties for which the Recovery point is to be created
                Sample:
                {
                    'mailbox_smtp' : name of the mailbox for which recovery point is to be created
                    'mailbox_guid': GUID of the mailbox
                    'index_server': Name of the index server to be used to create index on
                }
                job                 (object)--  Backup Job to which restore point has to be created
                job_id              (int)--     Backup Job ID to which restore point is to be created

                Either pass the job object or the job_id

            Returns:
                res_dict            (dict)--    Dictionary of Response
                Format:
                {
                    'rercovery_point_id' : ID of the recovery point created,
                    'recovery_point_job_id': Job ID for recovery point creation JOB
                }
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

    def refresh(self):
        """Refresh the User Mailbox Subclient."""
        self._get_subclient_properties()
        self._discover_users = self._get_discover_users()
        self._discover_databases = self._get_discover_database()
        self._discover_adgroups = self._get_discover_adgroups()
        self._users, self._o365groups = self._get_user_assocaitions()
        self._databases = self._get_database_associations()
        self._adgroups = self._get_adgroup_assocaitions()
