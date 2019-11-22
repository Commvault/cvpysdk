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

UsermailboxSubclient:   Derived class from ExchangeMailboxSubclient Base class, representing a
                            UserMailbox subclient, and to perform operations on that subclient

UsermailboxSubclient:

    _get_subclient_properties()         --  gets the properties of UserMailbox Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of UserMailbox Subclient

    users()                             --  creates users association for subclient

    Databases()                         --  creates Db association for  the subclient

    Adgroups()                          --  creates Adgroup association for subclient

    restore_in_place()                  --  runs in-place restore for the subclient

    set_pst_association()               --  Create PST assocaition for UserMailboxSubclient

    set_fs_association_for_pst()        --  Helper method to create pst association for
                                            PST Ingestion by FS association
"""


from __future__ import unicode_literals

from past.builtins import basestring

from ...exception import SDKException

from ..exchsubclient import ExchangeSubclient

from ...subclient import Subclients

from ...backupset import Backupsets


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
        if not (isinstance(configuration_policy, (basestring, ConfigurationPolicy))):
            raise SDKException('Subclient', '101')

        if isinstance(configuration_policy, basestring):
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

    def _association_json(self, subclient_content):
        """Constructs association json to create assocaition in UserMailbox Subclient.

            Args:
                subclient_content (dict)  --  dict of the Users to add to the subclient

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
                    "enableAutoDiscovery": subclient_content.get("is_auto_discover_user", False)
                },
                "subclientEntity": self._subClientEntity,
                "policies": {
                    "emailPolicies": email_policies
                }
            }
        }

        return associations_json

    def _set_association_request(self, associations_json):
        """Runs the emailAssociation ass API to set association

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

    def _get_discover_users(self):
        """Gets the discovered users from the Subclient .

            Returns:
                list    -   list of discovered users associated with the subclient

        """
        self._DISCOVERY = self._commcell_object._services['EMAIL_DISCOVERY'] % (
            int(self._backupset_object.backupset_id), 'User'
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._DISCOVERY)

        if flag:
            discover_content = response.json()
            if 'discoverInfo' in discover_content.keys():

                if 'mailBoxes' in discover_content['discoverInfo']:
                    self._discover_users = discover_content['discoverInfo']['mailBoxes']

                return self._discover_users

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
                list    -   list of users associated with the subclient

        """
        users = []

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
                        'plan_id': plan_id
                    }

                    users.append(temp_dict)

        return users

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

    def set_user_assocaition(self, subclient_content):
        """Create User assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the Users to add to the subclient

                    subclient_content = {

                        'mailboxNames' : ["AutoCi2"],,

                        'archive_policy' : "CIPLAN Archiving policy",

                        'cleanup_policy' : 'CIPLAN Clean-up policy',

                        'retention_policy': 'CIPLAN Retention policy'
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
                            'user': {
                                '_type_': 13,
                                'userGUID': mb_item['user']['userGUID']
                            }
                        }
                        users.append(mailbox_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        discover_info = {
            "discoverByType": 1,
            "mailBoxes": users
        }

        _assocaition_json_ = self._association_json(subclient_content)
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._set_association_request(_assocaition_json_)

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
                    'pstStubsAction':1,
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
                pst_dict['taskType'] = 0;
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
                        raise SDKException('Subclient','102',"Backupset {0} not present in file "
                                                             "system agent".format(backupset_name))
                    backupset_dict = {"backupsetName": backupset_obj.name,
                                      "appName": "File System",
                                      "applicationId": int(agent.agent_id),
                                      "backupsetId": int(backupset_obj.backupset_id),
                                      "_type_": _type_id["backupset"]
                                      }
                    backupset_dict.update(client_dict)
                    for subclient_name in subclients:
                        if subclient_name not in backupset_obj.subclients.all_subclients:
                            raise SDKException('Subclient','102',
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

    def delete_user_assocaition(self, subclient_content):
        """delete User assocaition for UserMailboxSubclient.

            Args:
                subclient_content   (dict)  --  dict of the Users to delete from subclient

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
                            'user': {
                                '_type_': 13,
                                'userGUID': mb_item['user']['userGUID']
                            }
                        }
                        users.append(mailbox_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        discover_info = {
            "discoverByType": 1,
            "mailBoxes": users
        }

        _assocaition_json_ = self._association_json(subclient_content)
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
        _assocaition_json_["emailAssociation"]["emailDiscoverinfo"] = discover_info
        self._update_association_request(_assocaition_json_)

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

    def refresh(self):
        """Refresh the User Mailbox Subclient."""
        self._get_subclient_properties()
        self._discover_users = self._get_discover_users()
        self._discover_databases = self._get_discover_database()
        self._discover_adgroups = self._get_discover_adgroups()
        self._users = self._get_user_assocaitions()
        self._databases = self._get_database_associations()
        self._adgroups = self._get_adgroup_assocaitions()
