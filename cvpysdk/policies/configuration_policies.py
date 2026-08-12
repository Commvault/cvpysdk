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

"""Main file for performing Configuration Policies related related operations on the commcell.

ConfigurationPolicies:  Class for representing all the Configuration Policies associated
                            with the Commcell

ConfigurationPolicy:    Class for representing a single Configuration Policy. Contains
                            method definitions for common methods among all Configuration Policies

ArchivePolicy:          Class for representing a single Archive Policy associated with
                            the Commcell; inherits ConfigurationPolicy

JournalPolicy:          Class for representing a single Journal Policy associated with
                            the Commcell; inherits ConfigurationPolicy

CleanupPolicy:          Class for representing a single Cleanup Policy associated with
                            the Commcell; inherits ConfigurationPolicy

RetentionPolicy:        Class for representing a single Retention Policy associated with
                            the Commcell; inherits ConfigurationPolicy

ContentIndexingPolicy:  Class for representing a single Content Indexing Policy associated with
                            the Commcell; inherits ConfigurationPolicy


ConfigurationPolicies:

    __init__(commcell_object)   --  initialize the ConfigurationPolicies instance for the Commcell

    __str__()                   --  returns all the ConfigurationPolicies policies associated
    with the Commcell

    __repr__()                  --  returns a string for the instance of the
    ConfigurationPolicies class

    _get_policies()             --  gets all the Configuration policies of the Commcell

    _get_ci_policies()          --  gets all the CI configuration policies of the Commcell

    has_policy(policy_name)     --  checks if a Configuration policy exists with the
    given name in a particular instance

    get(policy_name)            --  returns a ConfigurationPolicy object of the
    specified Configuration policy name

    add(policy_object)          --  adds a new Configuration policy to the
    ConfigurationPolicies instance, and returns an object of corresponding policy_type

    delete(policy_name)         --  removes the specified Configuration policy from the Commcell

    get_policy_object()         --  get the policy object based on policy type

    run_content_indexing()      --  runs a Content indexing job for the CI policy


ContentIndexingPolicy:

    __init__()                  --  initializes the ContentIndexingPolicy instance for the given policy name

    _initialize_policy_json()   --  creates a JSON payload for the Content Indexing Policy

ContentIndexingPolicy Attributes:

    **name**                    --  name of the Content Indexing policy

    **include_doc_types**       --  list of all the file types to be included while Content Indexing

    **index_server_name**       --  index server name to be used for Content Indexing

    **data_access_node**        --  data access node's client name

    **min_doc_size**            --  minimum documents size in MB

    **max_doc_size**            --  maximum documents size in MB

    **exclude_paths**           --  list of all the paths to be excluded from Content Indexing


"""

from __future__ import unicode_literals
from typing import TYPE_CHECKING, Optional, List, Union

from ..exception import SDKException
from ..job import Job

if TYPE_CHECKING:
    from ..commcell import Commcell

class ConfigurationPolicies(object):
    """Class for getting all the Configuration policies associated with the commcell.

    Attributes:
        _commcell_object (object): Instance of the Commcell class.
        _cvpysdk_object (object): Instance of the CVPySDK class.
        _services (dict): Dictionary of service URLs.
        _update_response_ (method): Method to update the response string.
        _POLICY (str): Service URL for getting configuration policies.
        _POLICY_FS (str): Service URL for getting file system policies.
        _CREATE_TASK (str): Service URL for creating tasks.
        _policies (dict): Dictionary of configuration policies.
        _ci_policies (dict): Dictionary of content indexing policies.

    Usage:
        >>> commcell = Commcell('localhost', 'user', 'password')
        >>> config_policies = ConfigurationPolicies(commcell)
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize object of the ConfigurationPolicies class.

        Args:
            commcell_object (object): Instance of the Commcell class.

        Returns:
            None

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._POLICY = self._services['GET_CONFIGURATION_POLICIES']
        self._POLICY_FS = self._services['GET_CONFIGURATION_POLICIES_FS']
        self._CREATE_TASK = self._services['CREATE_TASK']
        self._policies = None
        self._ci_policies = None
        self.refresh()

    def __repr__(self) -> str:
        """Representation string for the instance of the ConfigurationPolicies class.

        Returns:
            str: String representation of the class instance.
        """
        return "ConfigurationPolicies class instance for Commcell"

    def _get_policies(self) -> dict:
        """Gets all the Configuration policies associated to the
            commcell specified by commcell object.

            Returns:
                dict: Consists of all Configuration policies of the commcell

                    {
                        "configuration_policy1_name": configuration_policy1_id,

                        "configuration_policy2_name": configuration_policy2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._POLICY)

        if flag:
            if response.json() and 'policies' in response.json():
                policies = response.json()['policies']

                if policies == []:
                    return {}

                policies_dict = {}

                for policy in policies:
                    temp_name = policy['policyEntity']['policyName'].lower()
                    temp_id = str(policy['policyEntity']['policyId']).lower()
                    temp_policytype = str(policy['detail']['emailPolicy']
                                          ['emailPolicyType']).lower()
                    policies_dict[temp_name] = [temp_id, temp_policytype]

                return policies_dict
            else:
                return {}
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def has_policy(self, policy_name: str) -> bool:
        """Checks if a Configuration policy exists in the commcell with
            the input Configuration policy name.

            Args:
                policy_name (str): Name of the Configuration policy

            Returns:
                bool: Boolean output whether the Configuration policy exists in the commcell
                or not

            Raises:
                SDKException:
                    if type of the configuration policy name argument is not string

        """
        if not isinstance(policy_name, str):
            raise SDKException('ConfigurationPolicies', '101')

        return (self._policies and policy_name.lower() in self._policies) or \
               (self._ci_policies and policy_name.lower() in self._ci_policies)

    def _get_ci_policies(self) -> dict:
        """Gets all the Content Indexing policies associated to the commcell specified by commcell object.

            Returns:
                 dict: Consists of all Configuration policies of the commcell
                            {
                                "ci_policy1_name": [ci_policy1_id, ci_policy_type],

                                "ci_policy2_name": [ci_policy2_id, ci_policy_type]
                            }

            Raises:
                SDKException:
                        if response is empty

                        if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._POLICY_FS)

        if flag:
            policies_dict = {}
            if response.json() and 'policies' in response.json():
                policies = response.json()['policies']
                for policy in policies:
                    temp_name = policy['policyEntity']['policyName'].lower()
                    temp_id = str(policy['policyEntity']['policyId']).lower()
                    temp_policy_type = str(policy['detail']['filePolicy']
                                          ['filePolicyType']).lower()
                    policies_dict[temp_name] = [temp_id, temp_policy_type]
            return policies_dict
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_policy_id(self, policy_name: str) -> str:
        """Returns the policy ID for the given policy name.

        Args:
            policy_name (str): Name of the policy.

        Returns:
            str: The policy ID.

        Raises:
            SDKException: If the policy name is not a string.
        """
        if not isinstance(policy_name, str):
            raise SDKException('ConfigurationPolicies', '101')
        if policy_name.lower() in self._policies:
            return self._policies[policy_name.lower()][0]
        if policy_name.lower() in self._ci_policies:
            return self._ci_policies[policy_name.lower()][0]

    def get(self, configuration_policy_name: str, policy_type: str) -> 'ConfigurationPolicy':
        """Returns a ConfigurationPolicy object of the specified Configuration policy name.

        Args:
            configuration_policy_name (str): Name of the configuration policy.
            policy_type             (str): Type of the policy.

        Returns:
            object: Instance of the ConfigurationPolicy class for the given policy name.

        Raises:
            SDKException:
                if type of the Configuration policy name argument is not string

                if no Configuration policy exists with the given name

        Usage:
            >>> commcell = Commcell('localhost', 'user', 'password')
            >>> config_policies = ConfigurationPolicies(commcell)
            >>> policy = config_policies.get('MyPolicy', 'Archive')
        """
        if not isinstance(configuration_policy_name, str):
            raise SDKException('ConfigurationPolicies', '101')

        if self.has_policy(configuration_policy_name):
            return ConfigurationPolicy(
                self._commcell_object, configuration_policy_name, self._get_policy_id(
                    configuration_policy_name)
            )

        else:
            raise SDKException(
                'ConfigurationPolicies', '102', 'No policy exists with name: {0}'.format(
                    configuration_policy_name)
            )

    def get_policy_object(self, policy_type: str, configuration_policy_name: str) -> Union['ArchivePolicy', 'JournalPolicy', 'CleanupPolicy', 'RetentionPolicy', 'ContentIndexingPolicy']:
        """Get a Policy object based on policy type

            Args:
                policy_type                 (str)   --  type of policy to create the object of

                    Valid values are:

                        - Archive

                        - Cleanup

                        - Retention

                        - Journal

                        - Content Indexing

                configuration_policy_name   (str)   --  name of the configuration Policy

            Returns:
                Union[ArchivePolicy, JournalPolicy, CleanupPolicy, RetentionPolicy, ContentIndexingPolicy]: instance of the appropriate Policy class

            Raises:
                SDKException:
                    If the policy type is not supported.

            Usage:
                >>> commcell = Commcell('localhost', 'user', 'password')
                >>> config_policies = ConfigurationPolicies(commcell)
                >>> archive_policy = config_policies.get_policy_object('Archive', 'MyArchivePolicy')
        """

        policy_types = {
            "Archive": ArchivePolicy,
            "Journal": JournalPolicy,
            "Cleanup": CleanupPolicy,
            "Retention": RetentionPolicy,
            "ContentIndexing": ContentIndexingPolicy
        }

        try:
            return policy_types[policy_type](self._commcell_object, configuration_policy_name)
        except KeyError as e:
            raise SDKException(
                'ConfigurationPolicies',
                '102',
                'Policy Type {} is not supported'.format(policy_type)
            ) from e

    def run_content_indexing(self, ci_policy_name: str) -> 'Job':
        """Runs Content indexing job from the CI policy level

            Args:
                ci_policy_name (str): Content indexing policy name

            Returns:
                Job: Job class object for the CI Job

            Raises:
                SDKException:
                    No CI policy exists     -   if given policy name does not exist
                    Failed to run CI job    -   if CI job failed to start
                    Response was not success
                    Response received is empty

            Usage:
                >>> commcell = Commcell('localhost', 'user', 'password')
                >>> config_policies = ConfigurationPolicies(commcell)
                >>> job = config_policies.run_content_indexing('MyCIPolicy')
        """
        if not self.has_policy(ci_policy_name):
            raise SDKException('ConfigurationPolicies', '102', f'No CI policy exists with name: {ci_policy_name}')
        request_json = {
            "taskInfo": {
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 1,
                    "policyType": 0,
                    "taskId": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 5022
                        },
                        "options": {
                            "adminOpts": {
                                "contentIndexingOption": {
                                    "fileAnalytics": False,
                                    "subClientBasedAnalytics": False
                                },
                                "contentIndexingPolicyOption": {
                                    "policyId": int(self._get_policy_id(ci_policy_name)),
                                    "policyName": ci_policy_name,
                                    "policyDetailType": 5,
                                    "policyType": 2
                                }
                            }
                        }
                    }
                ]
            }
        }
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._CREATE_TASK, request_json)
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Content Index job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('ConfigurationPolicies', '102', o_str)
                raise SDKException('ConfigurationPolicies', '102', 'Failed to run the content indexing job')
            raise SDKException('Response', '102')
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def delete(self, configuration_policy_name: str) -> None:
        """Deletes a Configuration policy from the commcell.

        Args:
            configuration_policy_name (str): Name of the configuration policy to delete

        Raises:
            SDKException:
                if type of the configuration policy name argument is not string

                if failed to delete configuration policy

                if response is empty

                if response is not success

        Usage:
            >>> commcell = Commcell('localhost', 'user', 'password')
            >>> config_policies = ConfigurationPolicies(commcell)
            >>> config_policies.delete('MyPolicy')
        """
        if not isinstance(configuration_policy_name, str):
            raise SDKException('ConfigurationPolicies', '101')

        if self.has_policy(configuration_policy_name):
            policy_delete_service = self._services['DELETE_CONFIGURATION_POLICY'] % (
                str(self._get_policy_id(configuration_policy_name)))

            flag, response = self._cvpysdk_object.make_request(
                'DELETE', policy_delete_service
            )

            if flag:
                try:
                    if response.json():
                        if response.json()['errorCode'] != 0:
                            error_message = response.json()['errorMessage']
                            o_str = 'Failed to delete Configuration policy\nError: "{0}"'

                            raise SDKException(
                                'ConfigurationPolicies', '102', o_str.format(error_message))
                except ValueError as e:
                    if response.text:
                        self.refresh()
                        return response.text.strip()
                    else:
                        raise SDKException('Response', '102') from e
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'ConfigurationPolicies', '102', 'No policy exists with name: {0}'.format(
                    configuration_policy_name)
            )

    def add_policy(self, policy_object: object) -> 'ConfigurationPolicy':
        """Adds a new Configuration Policy to the Commcell.

        Args:
            policy_object (object): Policy object based on type of policy

        Returns:
            ConfigurationPolicy: The created ConfigurationPolicy object.

        Raises:
            SDKException:
                if failed to create configuration policy

                if response is empty

                if response is not success

        Usage:
            >>> commcell = Commcell('localhost', 'user', 'password')
            >>> config_policies = ConfigurationPolicies(commcell)
            >>> archive_policy = ArchivePolicy(commcell, 'MyNewPolicy')
            >>> new_policy = config_policies.add_policy(archive_policy)
        """

        json = policy_object._initialize_policy_json()
        configuration_policy_name = policy_object.name.lower()

        create_configuration_policy = self._services['CREATE_CONFIGURATION_POLICIES']

        flag, response = self._cvpysdk_object.make_request(
            'POST', create_configuration_policy, json
        )

        if flag:
            if response.json():
                if 'policy' in response.json():
                    # initialize the policies again
                    # so the policies object has all the policies
                    self.refresh()
                    return ConfigurationPolicy(
                        self._commcell_object, configuration_policy_name,
                        self._get_policy_id(configuration_policy_name)
                    )
                elif 'error' in response.json():
                    error_message = response.json()['error']['errorMessage']
                    o_str = 'Failed to create Configuration policy\nError: "{0}"'

                    raise SDKException('ConfigurationPolicies', '102', o_str.format(error_message))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self) -> None:
        """Refresh the Virtual Machine policies.

        Returns:
            None
        """
        self._policies = self._get_policies()
        self._ci_policies = self._get_ci_policies()

class ConfigurationPolicy(object):
    """Class for representing a single Configuration Policy.
    Contains method definitions for common operations among all Configuration Policies.

    Attributes:
        _configuration_policy_name (str): The name of the configuration policy.
        _commcell_object (Commcell): Instance of the Commcell class.
        _cvpysdk_object (CVPySDK): Instance of the CVPySDK class.
        _services (dict): Dictionary of Commvault services.
        _update_response_ (method): Method to update response.
        _configuration_policy_id (str): The ID of the configuration policy.
        _CONGIGURATION_POLICY (str): API service endpoint for the configuration policy.

    Usage:
        # Initialize a ConfigurationPolicy object
        config_policy = ConfigurationPolicy(commcell_object, 'MyPolicy')
    """

    def __init__(self, commcell_object: 'Commcell', configuration_policy_name: str, configuration_policy_id: int = None) -> None:
        """Initialize object of the ConfigurationPolicy class.

        Args:
            commcell_object (object): Instance of the Commcell class.
            configuration_policy_name (str): Name of the configuration policy.
            configuration_policy_id (int, optional): ID of the configuration policy. Defaults to None.

        Raises:
            Exception: if failed to initialize the ConfigurationPolicy object.
        """

        self._configuration_policy_name = configuration_policy_name
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        if configuration_policy_id:
            self._configuration_policy_id = str(configuration_policy_id)
        else:
            self._configuration_policy_id = self._get_configuration_policy_id()

        self._CONGIGURATION_POLICY = self._services['GET_CONFIGURATION_POLICY'] % (
            self._configuration_policy_id
        )

    @property
    def configuration_policy_id(self) -> str:
        """Treats the configuration policy id as a read-only attribute.

        Returns:
            str: The ID of the configuration policy.

        Usage:
            policy_id = config_policy.configuration_policy_id
        """
        return self._configuration_policy_id

    @property
    def configuration_policy_name(self) -> str:
        """Treats the configuration policy name as a read-only attribute.

        Returns:
            str: The name of the configuration policy.

        Usage:
            policy_name = config_policy.configuration_policy_name
        """
        return self._configuration_policy_name

    def _get_configuration_policy_id(self) -> str:
        """Gets the Configuration policy id asscoiated with the Configuration policy

        Returns:
            str: The ID of the configuration policy.

        Usage:
            policy_id = config_policy._get_configuration_policy_id()
        """

        configuration_policies = ConfigurationPolicies(self._commcell_object)
        return configuration_policies._get_policy_id(self._configuration_policy_name)

class ArchivePolicy():
    """Class for performing Archive policy operations for a specific archive policy

    Attributes:
        _commcell_object: Commcell object associated with this archive policy.
        _name (str): Name of the archive policy.
        _email_policy_type (int): Type of the email policy (default: 1).
        _archive_mailbox (bool): Flag indicating if archive mailbox is enabled (default: False).
        _backup_deleted_item_retention (bool): Flag indicating if backup deleted item retention is enabled (default: False).
        _backup_stubs (bool): Flag indicating if backup stubs is enabled (default: False).
        _disabled_mailbox (bool): Flag indicating if disabled mailbox is enabled (default: True).
        _enable_mailbox_quota (bool): Flag indicating if mailbox quota is enabled (default: False).
        _include_messages_larger_than (int): Size in KB for including messages larger than this value (default: 0).
        _include_messages_older_than (int): Number of days for including messages older than this value (default: 0).
        _include_messages_with_attachements (bool): Flag indicating if messages with attachments should be included (default: False).
        _primary_mailbox (bool): Flag indicating if primary mailbox is enabled (default: True).
        _include_discovery_holds_folder (bool): Flag indicating if discovery holds folder should be included (default: False).
        _include_purges_folder (bool): Flag indicating if purges folder should be included (default: False).
        _include_version_folder (bool): Flag indicating if version folder should be included (default: False).
        _save_conversation_meta_data (bool): Flag indicating if conversation metadata should be saved (default: False).
        _include_categories (bool): Flag indicating if categories should be included (default: False).
        _skip_mailboxes_exceeded_quota (int): Size in KB for skipping mailboxes exceeding this quota (default: 10240).
        _include_folder_filter (str): Comma-separated list of folders to include (default: "Deleted Items,Drafts,Inbox,Sent Items").
        _exclude_folder_filter (str): Comma-separated list of folders to exclude (default: "Deleted Items,Drafts,Inbox,Sent Items,Junk Mail,Sync Issues").
        _exclude_message_class_filter (str): Comma-separated list of message classes to exclude (default: "Appointments,Contacts,Schedules,Tasks").
        _content_index_behind_alert (bool): Flag indicating if content index behind alert is enabled (default: False).
        _content_index_data_over (int): Size in GB for content index data over alert (default: 0).
        _deferred_days (int): Number of deferred days for content indexing (default: 0).
        _enable_content_index (bool): Flag indicating if content index is enabled (default: False).
        _enable_deferred_days (bool): Flag indicating if deferred days is enabled (default: False).
        _enable_preview_generation (bool): Flag indicating if preview generation is enabled (default: False).
        _jobs_older_than (int): Number of days for jobs older than this value (default: 0).
        _retention_days_for_ci (int): Number of retention days for content index (default: -1).
        _start_time (int): Start time for content indexing (default: 0).
        _synchronize_on (bool): Flag indicating if synchronization is enabled (default: False).
        _path (str): Path for content index preview (default: "").
        _username (str): Username for content index preview (default: "").
        _password (str): Password for content index preview (default: "").
    """

    def __init__(self, commcell_object: 'Commcell', archive_policy_name: str) -> None:
        """Initialise the Archive Policy class instance.

        Args:
            commcell_object: Commcell object.
            archive_policy_name (str): Name of the archive policy.
        """
        self._commcell_object = commcell_object

        self._name = archive_policy_name
        self._email_policy_type = 1
        self._archive_mailbox = False
        self._backup_deleted_item_retention = False
        self._backup_stubs = False
        self._disabled_mailbox = True
        self._enable_mailbox_quota = False
        self._include_messages_larger_than = 0
        self._include_messages_older_than = 0
        self._include_messages_with_attachements = False
        self._primary_mailbox = True
        self._include_discovery_holds_folder = False
        self._include_purges_folder = False
        self._include_version_folder = False
        self._save_conversation_meta_data = False
        self._include_categories = False
        self._skip_mailboxes_exceeded_quota = 10240
        self._include_folder_filter = "Deleted Items,Drafts,Inbox,Sent Items"
        self._exclude_folder_filter = "Deleted Items,Drafts,Inbox,Sent Items,Junk Mail,Sync Issues"
        self._exclude_message_class_filter = "Appointments,Contacts,Schedules,Tasks"
        self._content_index_behind_alert = False
        self._content_index_data_over = 0
        self._deferred_days = 0
        self._enable_content_index = False
        self._enable_deferred_days = False
        self._enable_preview_generation = False
        self._jobs_older_than = 0
        self._retention_days_for_ci = -1
        self._start_time = 0
        self._synchronize_on = False
        self._path = ""
        self._username = ""
        self._password = ""
        # self._initialize_archive_policy_properties()

    @property
    def name(self) -> str:
        """Treats the name as a read-only attribute.

        Returns:
            str: The name of the archive policy.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the policy

        Args:
            name (str): The new name for the archive policy.
        """
        self._name = name

    @property
    def email_policy_type(self) -> int:
        """Treats the email_policy_type as a read-only attribute.

        Returns:
            int: The email policy type.
        """
        return self._email_policy_type

    @property
    def archive_mailbox(self) -> bool:
        """Treats the archive_mailbox as a read-only attribute.

        Returns:
            bool: True if archive mailbox is enabled, False otherwise.
        """
        return self._archive_mailbox

    @archive_mailbox.setter
    def archive_mailbox(self, archive_mailbox: bool) -> None:
        """Enable/Disable archive_mailbox option for policy

        Args:
            archive_mailbox (bool): True to enable archive mailbox, False to disable.
        """
        self._archive_mailbox = archive_mailbox

    @property
    def backup_deleted_item_retention(self) -> bool:
        """Treats the backup_deleted_item_retention as a read-only attribute.

        Returns:
            bool: True if backup deleted item retention is enabled, False otherwise.
        """
        return self._backup_deleted_item_retention

    @backup_deleted_item_retention.setter
    def backup_deleted_item_retention(self, backup_deleted_item_retention: bool) -> None:
        """Enable/Disable backup deleted item retention

        Args:
            backup_deleted_item_retention (bool): True to enable, False to disable.
        """
        self._backup_deleted_item_retention = backup_deleted_item_retention

    @property
    def backup_stubs(self) -> bool:
        """Treats the backup_stubs as a read-only attribute.

        Returns:
            bool: True if backup stubs is enabled, False otherwise.
        """
        return self._backup_stubs

    @backup_stubs.setter
    def backup_stubs(self, backup_stubs: bool) -> None:
        """Sets backup stubs option on policy

        Args:
            backup_stubs (bool): True to enable backup stubs, False to disable.
        """
        self._backup_stubs = backup_stubs

    @property
    def disabled_mailbox(self) -> bool:
        """Treats the disabled_mailbox as a read-only attribute.

        Returns:
            bool: True if disabled mailbox is enabled, False otherwise.
        """
        return self._disabled_mailbox

    @disabled_mailbox.setter
    def disabled_mailbox(self, disabled_mailbox: bool) -> None:
        """Enable/Disable disable mailbox on policy

        Args:
            disabled_mailbox (bool): True to disable mailbox, False to enable.
        """
        self._disabled_mailbox = disabled_mailbox

    @property
    def enable_mailbox_quota(self) -> bool:
        """Treats the enable_mailbox_quota as a read-only attribute.

        Returns:
            bool: True if mailbox quota is enabled, False otherwise.
        """
        return self._enable_mailbox_quota

    @enable_mailbox_quota.setter
    def enable_mailbox_quota(self, enable_mailbox_quota: bool) -> None:
        """Sets the mailbox quota value

        Args:
            enable_mailbox_quota (bool): True to enable mailbox quota, False to disable.
        """
        self._enable_mailbox_quota = enable_mailbox_quota

    @property
    def include_messages_larger_than(self) -> int:
        """Treats the include_messages_larger_than as a read-only attribute.

        Returns:
            int: The size in KB for including messages larger than this value.
        """
        return self._include_messages_larger_than

    @include_messages_larger_than.setter
    def include_messages_larger_than(self, include_messages_larger_than: int) -> None:
        """Sets the message rule include message larger than

        Args:
            include_messages_larger_than (int): Size in KB.
        """
        self._include_messages_larger_than = include_messages_larger_than

    @property
    def include_messages_older_than(self) -> int:
        """Treats the include_messages_older_than as a read-only attribute.

        Returns:
            int: The number of days for including messages older than this value.
        """
        return self._include_messages_older_than

    @include_messages_older_than.setter
    def include_messages_older_than(self, include_messages_older_than: int) -> None:
        """Sets the message rule include messages older than

        Args:
            include_messages_older_than (int): Number of days.
        """
        self._include_messages_older_than = include_messages_older_than

    @property
    def include_messages_with_attachements(self) -> bool:
        """Treats the include_messages_with_attachements as a read-only attribute.

        Returns:
            bool: True if messages with attachments should be included, False otherwise.
        """
        return self._include_messages_with_attachements

    @include_messages_with_attachements.setter
    def include_messages_with_attachements(self, include_messages_with_attachements: bool) -> None:
        """Sets the message rule include messages with attachments

        Args:
            include_messages_with_attachements (bool): True to include, False to exclude.
        """
        self._include_messages_with_attachements = include_messages_with_attachements

    @property
    def primary_mailbox(self) -> bool:
        """Treats the primary_mailbox as a read-only attribute.

        Returns:
            bool: True if primary mailbox is enabled, False otherwise.
        """
        return self._primary_mailbox

    @primary_mailbox.setter
    def primary_mailbox(self, primary_mailbox: bool) -> None:
        """Enable/Disable primary mailbox on policy

        Args:
            primary_mailbox (bool): True to enable, False to disable.
        """
        self._primary_mailbox = primary_mailbox

    @property
    def skip_mailboxes_exceeded_quota(self) -> int:
        """Treats the skip_mailboxes_exceeded_quota as a read-only attribute.

        Returns:
            int: The size in KB for skipping mailboxes exceeding this quota.
        """
        return self._skip_mailboxes_exceeded_quota

    @skip_mailboxes_exceeded_quota.setter
    def skip_mailboxes_exceeded_quota(self, skip_mailboxes_exceeded_quota: int) -> None:
        """Sets the mailbox exceeded quota value

        Args:
            skip_mailboxes_exceeded_quota (int): Size in KB.
        """
        self._skip_mailboxes_exceeded_quota = skip_mailboxes_exceeded_quota

    @property
    def include_discovery_holds_folder(self) -> bool:
        """Treats the include_discovery_holds_folder as a read-only attribute.

        Returns:
            bool: True if discovery holds folder should be included, False otherwise.
        """
        return self._include_discovery_holds_folder

    @include_discovery_holds_folder.setter
    def include_discovery_holds_folder(self, include_discovery_holds_folder: bool) -> None:
        """Enable/Disable disocvery hold folder

        Args:
            include_discovery_holds_folder (bool): True to include, False to exclude.
        """
        self._include_discovery_holds_folder = include_discovery_holds_folder

    @property
    def include_purges_folder(self) -> bool:
        """Treats the include_purges_folder as a read-only attribute.

        Returns:
            bool: True if purges folder should be included, False otherwise.
        """
        return self._include_purges_folder

    @include_purges_folder.setter
    def include_purges_folder(self, include_purges_folder: bool) -> None:
        """Enable/Disable Purges folder

        Args:
            include_purges_folder (bool): True to include, False to exclude.
        """
        self._include_purges_folder = include_purges_folder

    @property
    def include_version_folder(self) -> bool:
        """Treats the include_version_folder as a read-only attribute.

        Returns:
            bool: True if versions folder should be included, False otherwise.
        """
        return self._include_version_folder

    @include_version_folder.setter
    def include_version_folder(self, include_version_folder: bool) -> None:
        """Enable/Disable versions folder

        Args:
            include_version_folder (bool): True to include, False to exclude.
        """
        self._include_version_folder = include_version_folder

    @property
    def save_conversation_meta_data(self) -> bool:
        """Treats the save_conversation_meta_data as a read-only attribute.

        Returns:
            bool: True if conversation metadata should be saved, False otherwise.
        """
        return self._save_conversation_meta_data

    @save_conversation_meta_data.setter
    def save_conversation_meta_data(self, save_conversation_meta_data: bool) -> None:
        """sets the save conversation meta data

        Args:
            save_conversation_meta_data (bool): True to save, False otherwise.
        """
        self._save_conversation_meta_data = save_conversation_meta_data

    @property
    def include_categories(self) -> bool:
        """Treats the include_categories as a read-only attribute.

        Returns:
            bool: True if categories should be included, False otherwise.
        """
        return self._include_categories

    @include_categories.setter
    def include_categories(self, include_categories: bool) -> None:
        """sets the include categories option on policy

        Args:
            include_categories (bool): True to include, False otherwise.
        """
        self._include_categories = include_categories

    @property
    def include_folder_filter(self) -> str:
        """Treats the include_folder_filter as a read-only attribute.

        Returns:
            str: Comma-separated list of folders to include.
        """
        return self._include_folder_filter

    @include_folder_filter.setter
    def include_folder_filter(self, include_folder_filter: str) -> None:
        """sets include folder filter on policy

        Args:
            include_folder_filter (str): Comma-separated list of folders.
        """
        self._include_folder_filter = include_folder_filter

    @property
    def exclude_folder_filter(self) -> str:
        """Treats the exclude_folder_filter as a read-only attribute.

        Returns:
            str: Comma-separated list of folders to exclude.
        """
        return self._exclude_folder_filter

    @exclude_folder_filter.setter
    def exclude_folder_filter(self, exclude_folder_filter: str) -> None:
        """sets exclude folder filter on policy

        Args:
            exclude_folder_filter (str): Comma-separated list of folders.
        """
        self._exclude_folder_filter = exclude_folder_filter

    @property
    def exclude_message_class_filter(self) -> str:
        """Treats the exclude_message_class_filter as a read-only attribute.

        Returns:
            str: Comma-separated list of message classes to exclude.
        """
        return self._exclude_message_class_filter

    @exclude_message_class_filter.setter
    def exclude_message_class_filter(self, exclude_message_class_filter: str) -> None:
        """sets message class filters on policy

        Args:
            exclude_message_class_filter (str): Comma-separated list of message classes.
        """
        self._exclude_message_class_filter = exclude_message_class_filter

    @property
    def content_index_behind_alert(self) -> bool:
        """Treats the content_index_behind_alert as a read-only attribute.

        Returns:
            bool: True if content index behind alert is enabled, False otherwise.
        """
        return self._content_index_behind_alert

    @content_index_behind_alert.setter
    def content_index_behind_alert(self, content_index_behind_alert: bool) -> None:
        """sets content index alert

        Args:
            content_index_behind_alert (bool): True to enable, False to disable.
        """
        self._content_index_behind_alert = content_index_behind_alert

    @property
    def content_index_data_over(self) -> int:
        """Treats the content_index_data_over as a read-only attribute.

        Returns:
            int: The size in GB for content index data over alert.
        """
        return self._content_index_data_over

    @content_index_data_over.setter
    def content_index_data_over(self, content_index_data_over: int) -> None:
        """sets content Index data over value

        Args:
            content_index_data_over (int): Size in GB.
        """
        self._content_index_data_over = content_index_data_over

    @property
    def deferred_days(self) -> int:
        """Treats the deferred_days as a read-only attribute.

        Returns:
            int: The number of deferred days for content indexing.
        """
        return self._deferred_days

    @deferred_days.setter
    def deferred_days(self, deferred_days: int) -> None:
        """sets deferred days

        Args:
            deferred_days (int): Number of days.
        """
        self._deferred_days = deferred_days

    @property
    def enable_content_index(self) -> bool:
        """Treats the enable_content_index as a read-only attribute.

        Returns:
            bool: True if content index is enabled, False otherwise.
        """
        return self._enable_content_index

    @enable_content_index.setter
    def enable_content_index(self, enable_content_index: bool) -> None:
        """Enable/Disable ContentIndex

        Args:
            enable_content_index (bool): True to enable, False to disable.
        """
        self._enable_content_index = enable_content_index

    @property
    def enable_deferred_days(self) -> bool:
        """Treats the enable_deferred_days as a read-only attribute.

        Returns:
            bool: True if deferred days is enabled, False otherwise.
        """
        return self._enable_deferred_days

    @enable_deferred_days.setter
    def enable_deferred_days(self, enable_deferred_days: bool) -> None:
        """Enable/Disable deferred days

        Args:
            enable_deferred_days (bool): True to enable, False to disable.
        """
        self._enable_deferred_days = enable_deferred_days

    @property
    def enable_preview_generation(self) -> bool:
        """Treats the enable_preview_generation as a read-only attribute.

        Returns:
            bool: True if preview generation is enabled, False otherwise.
        """
        return self._enable_preview_generation

    @enable_preview_generation.setter
    def enable_preview_generation(self, enable_preview_generation: bool) -> None:
        """Enable/Disable preview generation

        Args:
            enable_preview_generation (bool): True to enable, False to disable.
        """
        self._enable_preview_generation = enable_preview_generation

    @property
    def jobs_older_than(self) -> int:
        """Treats the jobs_older_than as a read-only attribute.

        Returns:
            int: The number of days for jobs older than this value.
        """
        return self._jobs_older_than

    @jobs_older_than.setter
    def jobs_older_than(self, jobs_older_than: int) -> None:
        """sets job older than value

        Args:
            jobs_older_than (int): Number of days.
        """
        self._jobs_older_than = jobs_older_than

    @property
    def retention_days_for_ci(self) -> int:
        """Treats the retention_days_for_ci as a read-only attribute.

        Returns:
            int: The number of retention days for content index.
        """
        return self._retention_days_for_ci

    @retention_days_for_ci.setter
    def retention_days_for_ci(self, retention_days_for_ci: int) -> None:
        """sets retention for ContentIndex

        Args:
            retention_days_for_ci (int): Number of days.
        """
        self._retention_days_for_ci = retention_days_for_ci

    @property
    def start_time(self) -> int:
        """Treats the start_time as a read-only attribute.

        Returns:
            int: The start time for content indexing.
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: int) -> None:
        """sets start time

        Args:
            start_time (int): Start time.
        """
        self._start_time = start_time

    @property
    def synchronize_on(self) -> bool:
        """Treats the synchronize_on as a read-only attribute.

        Returns:
            bool: True if synchronization is enabled, False otherwise.
        """
        return self._synchronize_on

    @synchronize_on.setter
    def synchronize_on(self, synchronize_on: bool) -> None:
        """sets synchronize on for ContentIndex

        Args:
            synchronize_on (bool): True to enable, False to disable.
        """
        self._synchronize_on = synchronize_on

    @property
    def path(self) -> str:
        """Treats the path as a read-only attribute.

        Returns:
            str: The path for content index preview.
        """
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        """sets previewpath for ContentIndex

        Args:
            path (str): Path for content index preview.
        """
        self._path = path

    @property
    def username(self) -> str:
        """Treats the username as a read-only attribute.

        Returns:
            str: The username for content index preview.
        """
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        """sets username for ContentIndex

        Args:
            username (str): Username for content index preview.
        """
        self._username = username

    @property
    def password(self) -> str:
        """Treats the password as a read-only attribute.

        Returns:
            str: The password for content index preview.
        """
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        """sets password for ContentIndex

        Args:
            password (str): Password for content index preview.
        """
        self._password = password

    def _initialize_policy_json(self) -> dict:
        """
            sets values for creating the add policy json

        Returns:
            dict: The policy JSON.
        """

        policy_json = {
            "policy": {
                "policyType": 1,
                "agentType": {
                    "appTypeId": 137
                },
                "detail": {
                    "emailPolicy": {
                        "emailPolicyType": 1,
                        "archivePolicy": {
                            "includeMsgsLargerThan": self._include_messages_larger_than,
                            "skipMailBoxesExceededQuota": self._skip_mailboxes_exceeded_quota,
                            "backupDeletedItemRetention": self._backup_deleted_item_retention,
                            "primaryMailbox": self._primary_mailbox,
                            "includeMsgsOlderThan": self._include_messages_older_than,
                            "archiveMailbox": self._archive_mailbox,
                            "disabledMailbox": self._disabled_mailbox,
                            "backupStubs": self._backup_stubs,
                            "enableMailBoxQuota": self._enable_mailbox_quota,
                            "includeOnlyMsgsWithAttachemts": self._include_messages_with_attachements,
                            "includeDiscoveryHoldsFolder": self._include_discovery_holds_folder,
                            "includePurgesFolder": self._include_purges_folder,
                            "includeVersionsFolder": self._include_version_folder,
                            "saveConversationMetaData": self._save_conversation_meta_data,
                            "includeCategories": self._include_categories,
                            "includeFolderFilter": {
                                "folderPatternsAvailable": [
                                    "Deleted Items",
                                    "Drafts",
                                    "Inbox",
                                    "Sent Items"
                                ]
                            },
                            "excludeFolderFilter": {
                                "folderPatternsSelected": [
                                    "Junk Mail",
                                    "Sync Issues"
                                ],
                                "folderPatternsAvailable": [
                                    "Deleted Items",
                                    "Drafts",
                                    "Inbox",
                                    "Sent Items"
                                ]
                            },
                            "contentIndexProps": {
                                "enableContentIndex": self._enable_content_index,
                                "contentIndexBehindAlert": self._content_index_behind_alert,
                                "synchronizeOn": self._synchronize_on,
                                "contentIndexDataOver": self._content_index_data_over,
                                "retentionDaysForCI": self._retention_days_for_ci,
                                "startTime": self._start_time,
                                "jobsOlderThan": self._jobs_older_than,
                                "enablePreviewGeneration": self._enable_preview_generation,
                                "deferredDays": self._deferred_days,
                                "enableDeferredDays": self._enable_deferred_days,
                                "pattern": [
                                    {}
                                ],
                                "previewPathDir": {
                                    "path": self._path,
                                    "userAccount": {
                                        "userName": self._username,
                                        "password": self._password
                                    }
                                }
                            },
                            "excludeMessageClassFilter": {
                                "folderPatternsAvailable": [
                                    "Appointments",
                                    "Contacts",
                                    "Schedules",
                                    "Tasks"
                                ]
                            }
                        }
                    }
                },
                "policyEntity": {
                    "policyName": self._name
                }
            }
        }

        return policy_json

class JournalPolicy():
    """Class for performing Journal policy operations for a specific journal policy.

    Attributes:
        _commcell_object (Commcell): Commcell object associated with the journal policy.
        _name (str): Name of the journal policy.
        _commserver (Commcell): Commcell object (duplicate of _commcell_object).
        _email_policy_type (int): Type of email policy (default: 4).
        _complete_job_mapi_error (int): Flag for complete job MAPI error (default: 0).
        _delete_archived_messages (bool): Flag to delete archived messages (default: True).
        _job_hours_run (int): Number of hours a job has run (default: 0).
        _job_messages_protected (int): Number of messages protected by a job (default: 1).
        _include_folder_filter (str): Filter for included folders (default: "Deleted Items,Drafts,Inbox,Sent Items").
        _exclude_folder_filter (str): Filter for excluded folders (default: "Deleted Items,Drafts,Inbox,Sent Items,Junk Mail,Sync Issues").
        _exclude_message_class_filter (str): Filter for excluded message classes (default: "Appointments,Contacts,Schedules,Tasks").
        _content_index_behind_alert (bool): Flag for content index behind alert (default: False).
        _content_index_data_over (int): Content index data over value (default: 0).
        _deferred_days (int): Number of deferred days (default: 0).
        _enable_content_index (bool): Flag to enable content index (default: False).
        _enable_deferred_days (bool): Flag to enable deferred days (default: False).
        _enable_preview_generation (bool): Flag to enable preview generation (default: False).
        _jobs_older_than (int): Number of days jobs older than (default: 0).
        _retention_days_for_ci (int): Retention days for content index (default: -1).
        _start_time (int): Start time (default: 0).
        _synchronize_on (bool): Flag to synchronize on (default: False).
        _path (str): Path for preview generation (default: "").
        _username (str): Username for preview generation path (default: "").
        _password (str): Password for preview generation path (default: "").

    Usage:
        >>> journal_policy = JournalPolicy(commcell_object, 'MyJournalPolicy')
    """

    def __init__(self, commcell_object: 'Commcell', journal_policy_name: str) -> None:
        """Initialise the Journal Policy class instance.

        Args:
            commcell_object (Commcell):  Commcell object for the commcell.
            journal_policy_name (str):  Name of the journal policy.
        """

        self._commcell_object = commcell_object

        self._name = journal_policy_name
        self._commserver = commcell_object
        self._email_policy_type = 4
        self._complete_job_mapi_error = 0
        self._delete_archived_messages = True
        self._job_hours_run = 0
        self._job_messages_protected = 1
        self._include_folder_filter = "Deleted Items,Drafts,Inbox,Sent Items"
        self._exclude_folder_filter = "Deleted Items,Drafts,Inbox,Sent Items,Junk Mail,Sync Issues"
        self._exclude_message_class_filter = "Appointments,Contacts,Schedules,Tasks"
        self._content_index_behind_alert = False
        self._content_index_data_over = 0
        self._deferred_days = 0
        self._enable_content_index = False
        self._enable_deferred_days = False
        self._enable_preview_generation = False
        self._jobs_older_than = 0
        self._retention_days_for_ci = -1
        self._start_time = 0
        self._synchronize_on = False
        self._path = ""
        self._username = ""
        self._password = ""

    @property
    def name(self) -> str:
        """Treats the name as a read-only attribute.

        Returns:
            str: The name of the journal policy.

        Usage:
            >>> name = journal_policy.name
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def email_policy_type(self) -> int:
        """Treats the email_policy_type as a read-only attribute.

        Returns:
            int: The email policy type.

        Usage:
            >>> email_policy_type = journal_policy.email_policy_type
        """
        return self._email_policy_type

    @property
    def complete_job_mapi_error(self) -> int:
        """Treats the complete_job_mapi_error as a read-only attribute.

        Returns:
            int: The complete job MAPI error.

        Usage:
            >>> complete_job_mapi_error = journal_policy.complete_job_mapi_error
        """
        return self._complete_job_mapi_error

    @complete_job_mapi_error.setter
    def complete_job_mapi_error(self, complete_job_mapi_error: int) -> None:
        self._complete_job_mapi_error = complete_job_mapi_error

    @property
    def delete_archived_messages(self) -> bool:
        """Treats the delete_archived_messages as a read-only attribute.

        Returns:
            bool: Whether to delete archived messages.

        Usage:
            >>> delete_archived_messages = journal_policy.delete_archived_messages
        """
        return self._delete_archived_messages

    @delete_archived_messages.setter
    def delete_archived_messages(self, delete_archived_messages: bool) -> None:
        """Sets the delete archived messages option.
        
        Args:
            delete_archived_messages (bool): True to delete archived messages, False otherwise.

        Usage:
            >>> journal_policy.delete_archived_messages = True    
        """
        self._delete_archived_messages = delete_archived_messages

    @property
    def job_hours_run(self) -> int:
        """Treats the job_hours_run as a read-only attribute.

        Returns:
            int: The job hours run.

        Usage:
            >>> job_hours_run = journal_policy.job_hours_run
        """
        return self._job_hours_run

    @job_hours_run.setter
    def job_hours_run(self, job_hours_run: int) -> None:
        """Sets the job hours run.

        Args:
            job_hours_run (int): The number of hours a job has run.

        Usage:
            >>> journal_policy.job_hours_run = 5
        """
        self._job_hours_run = job_hours_run

    @property
    def job_messages_protected(self) -> int:
        """Treats the job_messages_protected as a read-only attribute.

        Returns:
            int: The job messages protected.

        Usage:
            >>> job_messages_protected = journal_policy.job_messages_protected
        """
        return self._job_messages_protected

    @job_messages_protected.setter
    def job_messages_protected(self, job_messages_protected: int) -> None:
        """Sets the job messages protected.
        
        Args:
            job_messages_protected (int): The number of messages protected by a job.

        Usage:
            >>> journal_policy.job_messages_protected = 10
        """
        self._job_messages_protected = job_messages_protected

    @property
    def include_folder_filter(self) -> str:
        """Treats the include_folder_filter as a read-only attribute.

        Returns:
            str: The include folder filter.

        Usage:
            >>> include_folder_filter = journal_policy.include_folder_filter
        """
        return self._include_folder_filter

    @include_folder_filter.setter
    def include_folder_filter(self, include_folder_filter: str) -> None:
        """Sets the include folder filter.

        Args:
            include_folder_filter (str): The include folder filter.

        Usage:
            >>> journal_policy.include_folder_filter = "Inbox"
        """
        self._include_folder_filter = include_folder_filter

    @property
    def exclude_folder_filter(self) -> str:
        """Treats the exclude_folder_filter as a read-only attribute.

        Returns:
            str: The exclude folder filter.

        Usage:
            >>> exclude_folder_filter = journal_policy.exclude_folder_filter
        """
        return self._exclude_folder_filter

    @exclude_folder_filter.setter
    def exclude_folder_filter(self, exclude_folder_filter: str) -> None:
        """Sets the exclude folder filter.

        Args:
            exclude_folder_filter (str): The exclude folder filter.

        Usage:
            >>> journal_policy.exclude_folder_filter = "Spam"
        """
        self._exclude_folder_filter = exclude_folder_filter

    @property
    def exclude_message_class_filter(self) -> str:
        """Treats the exclude_message_class_filter as a read-only attribute.

        Returns:
            str: The exclude message class filter.

        Usage:
            >>> exclude_message_class_filter = journal_policy.exclude_message_class_filter
        """
        return self._exclude_message_class_filter

    @exclude_message_class_filter.setter
    def exclude_message_class_filter(self, exclude_message_class_filter: str) -> None:
        """Sets the exclude message class filter.

        Args:
            exclude_message_class_filter (str): The exclude message class filter.

        Usage:
            >>> journal_policy.exclude_message_class_filter = "Tasks"
        """
        self._exclude_message_class_filter = exclude_message_class_filter

    @property
    def content_index_behind_alert(self) -> bool:
        """Treats the content_index_behind_alert as a read-only attribute.

        Returns:
            bool: Whether content index is behind alert.

        Usage:
            >>> content_index_behind_alert = journal_policy.content_index_behind_alert
        """
        return self._content_index_behind_alert

    @content_index_behind_alert.setter
    def content_index_behind_alert(self, content_index_behind_alert: bool) -> None:
        """Sets the content index behind alert.

        Args:
            content_index_behind_alert (bool): Whether content index is behind alert.

        Usage:
            >>> journal_policy.content_index_behind_alert = True
        """
        self._content_index_behind_alert = content_index_behind_alert

    @property
    def content_index_data_over(self) -> int:
        """Treats the content_index_data_over as a read-only attribute.

        Returns:
            int: The content index data over value.

        Usage:
            >>> content_index_data_over = journal_policy.content_index_data_over
        """
        return self._content_index_data_over

    @content_index_data_over.setter
    def content_index_data_over(self, content_index_data_over: int) -> None:
        """Sets the content index data over value.

        Args:
            content_index_data_over (int): The content index data over value.

        Usage:
            >>> journal_policy.content_index_data_over = 100
        """
        self._content_index_data_over = content_index_data_over

    @property
    def deferred_days(self) -> int:
        """Treats the deferred_days as a read-only attribute.

        Returns:
            int: The number of deferred days.

        Usage:
            >>> deferred_days = journal_policy.deferred_days
        """
        return self._deferred_days

    @deferred_days.setter
    def deferred_days(self, deferred_days: int) -> None:
        """Sets the number of deferred days.

        Args:
            deferred_days (int): The number of deferred days.

        Usage:
            >>> journal_policy.deferred_days = 5
        """
        self._deferred_days = deferred_days

    @property
    def enable_content_index(self) -> bool:
        """Treats the enable_content_index as a read-only attribute.

        Returns:
            bool: Whether content index is enabled.

        Usage:
            >>> enable_content_index = journal_policy.enable_content_index
        """
        return self._enable_content_index

    @enable_content_index.setter
    def enable_content_index(self, enable_content_index: bool) -> None:
        """Enable/Disable ContentIndex
        
        Args:
            enable_content_index (bool): True to enable, False to disable.

        Usage:
            >>> journal_policy.enable_content_index = True        
        """
        self._enable_content_index = enable_content_index

    @property
    def enable_deferred_days(self) -> bool:
        """Treats the enable_deferred_days as a read-only attribute.

        Returns:
            bool: Whether deferred days are enabled.

        Usage:
            >>> enable_deferred_days = journal_policy.enable_deferred_days
        """
        return self._enable_deferred_days

    @enable_deferred_days.setter
    def enable_deferred_days(self, enable_deferred_days: bool) -> None:
        """Enable/Disable deferred days
        
        Args:
            enable_deferred_days (bool): True to enable, False to disable.

        Usage:
            >>> journal_policy.enable_deferred_days = True        
        """
        self._enable_deferred_days = enable_deferred_days

    @property
    def enable_preview_generation(self) -> bool:
        """Treats the enable_preview_generation as a read-only attribute.

        Returns:
            bool: Whether preview generation is enabled.

        Usage:
            >>> enable_preview_generation = journal_policy.enable_preview_generation
        """
        return self._enable_preview_generation

    @enable_preview_generation.setter
    def enable_preview_generation(self, enable_preview_generation: bool) -> None:
        """Enable/Disable preview generation
        
        Args:
            enable_preview_generation (bool): True to enable, False to disable.

        Usage:
            >>> journal_policy.enable_preview_generation = True        
        """
        self._enable_preview_generation = enable_preview_generation

    @property
    def jobs_older_than(self) -> int:
        """Treats the jobs_older_than as a read-only attribute.

        Returns:
            int: The number of days jobs older than.

        Usage:
            >>> jobs_older_than = journal_policy.jobs_older_than
        """
        return self._jobs_older_than

    @jobs_older_than.setter
    def jobs_older_than(self, jobs_older_than: int) -> None:
        """Sets the number of days for jobs older than this value
        
        Args:
            jobs_older_than (int): Number of days.

        Usage:
            >>> journal_policy.jobs_older_than = 30        
        """
        self._jobs_older_than = jobs_older_than

    @property
    def retention_days_for_ci(self) -> int:
        """Treats the retention_days_for_ci as a read-only attribute.

        Returns:
            int: The retention days for content index.

        Usage:
            >>> retention_days_for_ci = journal_policy.retention_days_for_ci
        """
        return self._retention_days_for_ci

    @retention_days_for_ci.setter
    def retention_days_for_ci(self, retention_days_for_ci: int) -> None:
        """Sets the retention days for content index
        
        Args:
            retention_days_for_ci (int): Number of retention days.

        Usage:
            >>> journal_policy.retention_days_for_ci = 365        
        """
        self._retention_days_for_ci = retention_days_for_ci

    @property
    def start_time(self) -> int:
        """Treats the start_time as a read-only attribute.

        Returns:
            int: The start time.

        Usage:
            >>> start_time = journal_policy.start_time
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: int) -> None:
        """Sets the start time for content indexing
        
        Args:
            start_time (int): Start time value.

        Usage:
            >>> journal_policy.start_time = 8        
        """
        self._start_time = start_time

    @property
    def synchronize_on(self) -> bool:
        """Treats the synchronize_on as a read-only attribute.

        Returns:
            bool: Whether synchronize on is enabled.

        Usage:
            >>> synchronize_on = journal_policy.synchronize_on
        """
        return self._synchronize_on

    @synchronize_on.setter
    def synchronize_on(self, synchronize_on: bool) -> None:
        """Enable/Disable synchronization for content indexing
        
        Args:
            synchronize_on (bool): True to enable, False to disable.

        Usage:
            >>> journal_policy.synchronize_on = True        
        """
        self._synchronize_on = synchronize_on

    @property
    def path(self) -> str:
        """Treats the path as a read-only attribute.

        Returns:
            str: The path for preview generation.

        Usage:
            >>> path = journal_policy.path
        """
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        """Sets the path for preview generation
        
        Args:
            path (str): The file system path for preview generation.

        Usage:
            >>> journal_policy.path = "/path/to/preview"        
        """
        self._path = path

    @property
    def username(self) -> str:
        """Treats the username as a read-only attribute.

        Returns:
            str: The username for preview generation path.

        Usage:
            >>> username = journal_policy.username
        """
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        """Sets the username for preview generation path access
        
        Args:
            username (str): Username for accessing the preview path.

        Usage:
            >>> journal_policy.username = "admin"        
        """
        self._username = username

    @property
    def password(self) -> str:
        """Treats the password as a read-only attribute.

        Returns:
            str: The password for preview generation path.

        Usage:
            >>> password = journal_policy.password
        """
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        """Sets the password for preview generation path access
        
        Args:
            password (str): Password for accessing the preview path.

        Usage:
            >>> journal_policy.password = "secure_password"        
        """
        self._password = password

    def _initialize_policy_json(self) -> dict:
        """sets values for creating the add policy json

        Returns:
            dict: The policy JSON.

        Usage:
            >>> policy_json = journal_policy._initialize_policy_json()
        """
        policy_json = {
            "policy": {
                "policyType": 1,
                "agentType": {
                    "appTypeId": 137
                },
                "detail": {
                    "emailPolicy": {
                        "emailPolicyType": 4,
                        "journalPolicy": {
                            "deleteArchivedMessages": self._delete_archived_messages,
                            "contentIndexProps": {
                                "enableContentIndex": self._enable_content_index,
                                "contentIndexBehindAlert": self.content_index_behind_alert,
                                "synchronizeOn": self._synchronize_on,
                                "contentIndexDataOver": self._content_index_data_over,
                                "retentionDaysForCI": -self._retention_days_for_ci,
                                "startTime": self._start_time,
                                "jobsOlderThan": self._jobs_older_than,
                                "enablePreviewGeneration": self._enable_preview_generation,
                                "deferredDays": self._deferred_days,
                                "enableDeferredDays": self._enable_deferred_days,
                                "pattern": [
                                    {}
                                ],
                                "previewPathDir": {
                                    "path": self._path,
                                    "userAccount": {
                                        "userName": self._username,
                                        "password": self._password

                                    }
                                }
                            },
                            "excludeMessageClassFilter": {
                                "folderPatternsAvailable": [
                                    "Appointments",
                                    "Contacts",
                                    "Schedules",
                                    "Tasks"
                                ]
                            },
                            "includeFolderFilter": {
                                "folderPatternsAvailable": [
                                    "Deleted Items",
                                    "Drafts",
                                    "Inbox",
                                    "Sent Items"
                                ]
                            },
                            "excludeFolderFilter": {
                                "folderPatternsSelected": [
                                    "Junk Mail",
                                    "Sync Issues"
                                ],
                                "folderPatternsAvailable": [
                                    "Deleted Items",
                                    "Drafts",
                                    "Inbox",
                                    "Sent Items"
                                ]
                            }
                        }
                    }
                },
                "policyEntity": {
                    "policyName": self._name
                }
            }
        }

        return policy_json

class CleanupPolicy():
    """Class for performing Cleanup policy operations for a specific cleanup policy

    Attributes:
        _commcell_object: Commcell object associated with the cleanup policy.
        _name (str): Name of the cleanup policy.
        _email_policy_type (int): Type of email policy (default: 2).
        _add_recall_link (bool): Whether to add a recall link (default: True).
        _archive_if_size (int): Size to archive if (default: 90).
        _archive_mailbox (bool): Whether to archive the mailbox (default: False).
        _collect_messages_with_attachments (bool): Whether to collect messages with attachments (default: False).
        _collect_messages_days_after (int): Number of days after which to collect messages (default: 0).
        _collect_messages_larger_than (int): Size larger than which to collect messages (default: 0).
        _create_stubs (bool): Whether to create stubs (default: True).
        _disabled_mailbox (bool): Whether the mailbox is disabled (default: True).
        _enable_message_rules (bool): Whether to enable message rules (default: True).
        _leave_message_body (bool): Whether to leave the message body (default: True).
        _mailbox_quota (bool): Whether to apply mailbox quota (default: False).
        _number_of_days_for_source_pruning (int): Number of days for source pruning (default: 730).
        _primary_mailbox (bool): Whether it is the primary mailbox (default: True).
        _prune_erased_messages_or_stubs (bool): Whether to prune erased messages or stubs (default: False).
        _prune_messages (bool): Whether to prune messages (default: False).
        _prune_stubs (bool): Whether to prune stubs (default: False).
        _skip_unread_messages (bool): Whether to skip unread messages (default: False).
        _stop_archive_if_size (int): Size to stop archiving if (default: 75).
        _truncate_body (bool): Whether to truncate the body (default: False).
        _truncate_body_to_bytes (int): Number of bytes to truncate the body to (default: 1024).
        _used_disk_space (bool): Whether to consider used disk space (default: False).
        _used_disk_space_value (int): Used disk space value (default: 50).
        _include_folder_filter (str): Filter for including folders (default: "Deleted Items,Drafts,Inbox,Sent Items").
        _exclude_folder_filter (str): Filter for excluding folders (default: "Deleted Items,Drafts,Inbox,Sent Items,Junk Mail,Sync Issues").
        _exclude_message_class_filter (str): Filter for excluding message classes (default: "Appointments,Contacts,Schedules,Tasks").
    
    Usage:
        >>> cleanup_policy = CleanupPolicy(commcell_object, 'MyCleanupPolicy')
    """

    def __init__(self, commcell_object: 'Commcell', cleanup_policy_name: str) -> None:
        """Initialise the cleanup Policy class instance.

        Args:
            commcell_object: Commcell object associated with the cleanup policy.
            cleanup_policy_name (str): Name of the cleanup policy.
        """
        self._commcell_object = commcell_object
        self._name = cleanup_policy_name
        self._email_policy_type = 2
        self._add_recall_link = True
        self._archive_if_size = 90
        self._archive_mailbox = False
        self._collect_messages_with_attachments = False
        self._collect_messages_days_after = 0
        self._collect_messages_larger_than = 0
        self._create_stubs = True
        self._disabled_mailbox = True
        self._enable_message_rules = True
        self._leave_message_body = True
        self._mailbox_quota = False
        self._number_of_days_for_source_pruning = 730
        self._primary_mailbox = True
        self._prune_erased_messages_or_stubs = False
        self._prune_messages = False
        self._prune_stubs = False
        self._skip_unread_messages = False
        self._stop_archive_if_size = 75
        self._truncate_body = False
        self._truncate_body_to_bytes = 1024
        self._used_disk_space = False
        self._used_disk_space_value = 50
        self._include_folder_filter = "Deleted Items,Drafts,Inbox,Sent Items"
        self._exclude_folder_filter = "Deleted Items,Drafts,Inbox,Sent Items,Junk Mail,Sync Issues"
        self._exclude_message_class_filter = "Appointments,Contacts,Schedules,Tasks"

    @property
    def name(self) -> str:
        """Treats the name as a read-only attribute.

        Returns:
            str: The name of the cleanup policy.

        Usage:
            >>> cleanup_policy = CleanupPolicy(commcell_object, 'MyCleanupPolicy')
            >>> cleanup_policy.name
            'MyCleanupPolicy'
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the cleanup policy.

        Args:
            name (str): The new name for the cleanup policy.
            
        Usage:
            >>> cleanup_policy.name = 'NewCleanupPolicy'
        """
        self._name = name

    @property
    def email_policy_type(self) -> int:
        """Treats the email_policy_type as a read-only attribute.

        Returns:
            int: The email policy type.
        """
        return self._email_policy_type

    @property
    def add_recall_link(self) -> bool:
        """Treats the add_recall_link as a read-only attribute.

        Returns:
            bool: Whether the add recall link is enabled.
        """
        return self._add_recall_link

    @add_recall_link.setter
    def add_recall_link(self, add_recall_link: bool) -> None:
        """Enable/Disable add recall link option
        
        Args:
            add_recall_link (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.add_recall_link = True        
        """
        self._add_recall_link = add_recall_link

    @property
    def archive_if_size(self) -> int:
        """Treats the archive_if_size as a read-only attribute.

        Returns:
            int: The archive if size value.
        """
        return self._archive_if_size

    @archive_if_size.setter
    def archive_if_size(self, archive_if_size: int) -> None:
        """Sets the archive if size value
        
        Args:
            archive_if_size (int): Size threshold for archiving.

        Usage:
            >>> cleanup_policy.archive_if_size = 90        
        """
        self._archive_if_size = archive_if_size

    @property
    def archive_mailbox(self) -> bool:
        """Treats the archive_mailbox as a read-only attribute.

        Returns:
            bool: Whether the archive mailbox is enabled.
        """
        return self._archive_mailbox

    @archive_mailbox.setter
    def archive_mailbox(self, archive_mailbox: bool) -> None:
        """Enable/Disable archive mailbox option
        
        Args:
            archive_mailbox (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.archive_mailbox = True        
        """
        self._archive_mailbox = archive_mailbox

    @property
    def collect_messages_with_attachments(self) -> bool:
        """Treats the collect_messages_with_attachments as a read-only attribute.

        Returns:
            bool: Whether collecting messages with attachments is enabled.
        """
        return self._collect_messages_with_attachments

    @collect_messages_with_attachments.setter
    def collect_messages_with_attachments(self, collect_messages_with_attachments: bool) -> None:
        """Enable/Disable collecting messages with attachments
        
        Args:
            collect_messages_with_attachments (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.collect_messages_with_attachments = True        
        """
        self._collect_messages_with_attachments = collect_messages_with_attachments

    @property
    def collect_messages_days_after(self) -> int:
        """Treats the collect_messages_days_after as a read-only attribute.

        Returns:
            int: The number of days after which to collect messages.
        """
        return self._collect_messages_days_after

    @collect_messages_days_after.setter
    def collect_messages_days_after(self, collect_messages_days_after: int) -> None:
        """Sets the number of days after which to collect messages
        
        Args:
            collect_messages_days_after (int): Number of days.

        Usage:
            >>> cleanup_policy.collect_messages_days_after = 30        
        """
        self._collect_messages_days_after = collect_messages_days_after

    @property
    def collect_messages_larger_than(self) -> int:
        """Treats the collect_messages_larger_than as a read-only attribute.

        Returns:
            int: The size larger than which to collect messages.
        """
        return self._collect_messages_larger_than

    @collect_messages_larger_than.setter
    def collect_messages_larger_than(self, collect_messages_larger_than: int) -> None:
        """Sets the size threshold for collecting messages
        
        Args:
            collect_messages_larger_than (int): Size threshold in KB.

        Usage:
            >>> cleanup_policy.collect_messages_larger_than = 1024        
        """
        self._collect_messages_larger_than = collect_messages_larger_than

    @property
    def create_stubs(self) -> bool:
        """Treats the create_stubs as a read-only attribute.

        Returns:
            bool: Whether creating stubs is enabled.
        """
        return self._create_stubs

    @create_stubs.setter
    def create_stubs(self, create_stubs: bool) -> None:
        """Enable/Disable creating stubs
        
        Args:
            create_stubs (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.create_stubs = True        
        """
        self._create_stubs = create_stubs

    @property
    def disabled_mailbox(self) -> bool:
        """Treats the disabled_mailbox as a read-only attribute.

        Returns:
            bool: Whether the mailbox is disabled.
        """
        return self._disabled_mailbox

    @disabled_mailbox.setter
    def disabled_mailbox(self, disabled_mailbox: bool) -> None:
        """Enable/Disable disabled mailbox option
        
        Args:
            disabled_mailbox (bool): True to disable mailbox, False to enable.

        Usage:
            >>> cleanup_policy.disabled_mailbox = True        
        """
        self._disabled_mailbox = disabled_mailbox

    @property
    def enable_message_rules(self) -> bool:
        """Treats the enable_message_rules as a read-only attribute.

        Returns:
            bool: Whether enabling message rules is enabled.
        """
        return self._enable_message_rules

    @enable_message_rules.setter
    def enable_message_rules(self, enable_message_rules: bool) -> None:
        """Enable/Disable message rules
        
        Args:
            enable_message_rules (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.enable_message_rules = True        
        """
        self._enable_message_rules = enable_message_rules

    @property
    def leave_message_body(self) -> bool:
        """Treats the leave_message_body as a read-only attribute.

        Returns:
            bool: Whether leaving the message body is enabled.
        """
        return self._leave_message_body

    @leave_message_body.setter
    def leave_message_body(self, leave_message_body: bool) -> None:
        """Enable/Disable leaving the message body
        
        Args:
            leave_message_body (bool): True to leave message body, False otherwise.

        Usage:
            >>> cleanup_policy.leave_message_body = True        
        """
        self._leave_message_body = leave_message_body

    @property
    def mailbox_quota(self) -> bool:
        """Treats the mailbox_quota as a read-only attribute.

        Returns:
            bool: Whether mailbox quota is enabled.
        """
        return self._mailbox_quota

    @mailbox_quota.setter
    def mailbox_quota(self, mailbox_quota: bool) -> None:
        """Enable/Disable mailbox quota
        
        Args:
            mailbox_quota (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.mailbox_quota = True        
        """
        self._mailbox_quota = mailbox_quota

    @property
    def number_of_days_for_source_pruning(self) -> int:
        """Treats the number_of_days_for_source_pruning as a read-only attribute.

        Returns:
            int: The number of days for source pruning.
        """
        return self._number_of_days_for_source_pruning

    @number_of_days_for_source_pruning.setter
    def number_of_days_for_source_pruning(self, number_of_days_for_source_pruning: int) -> None:
        """Sets the number of days for source pruning
        
        Args:
            number_of_days_for_source_pruning (int): Number of days.

        Usage:
            >>> cleanup_policy.number_of_days_for_source_pruning = 730        
        """
        self._number_of_days_for_source_pruning = number_of_days_for_source_pruning

    @property
    def primary_mailbox(self) -> bool:
        """Treats the primary_mailbox as a read-only attribute.

        Returns:
            bool: Whether it is the primary mailbox.
        """
        return self._primary_mailbox

    @primary_mailbox.setter
    def primary_mailbox(self, primary_mailbox: bool) -> None:
        """Enable/Disable primary mailbox
        
        Args:
            primary_mailbox (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.primary_mailbox = True        
        """
        self._primary_mailbox = primary_mailbox

    @property
    def prune_erased_messages_or_stubs(self) -> bool:
        """Treats the prune_erased_messages_or_stubs as a read-only attribute.

        Returns:
            bool: Whether pruning erased messages or stubs is enabled.
        """
        return self._prune_erased_messages_or_stubs

    @prune_erased_messages_or_stubs.setter
    def prune_erased_messages_or_stubs(self, prune_erased_messages_or_stubs: bool) -> None:
        """Enable/Disable pruning erased messages or stubs
        
        Args:
            prune_erased_messages_or_stubs (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.prune_erased_messages_or_stubs = True        
        """
        self._prune_erased_messages_or_stubs = prune_erased_messages_or_stubs

    @property
    def prune_messages(self) -> bool:
        """Treats the prune_messages as a read-only attribute.

        Returns:
            bool: Whether pruning messages is enabled.
        """
        return self._prune_messages

    @prune_messages.setter
    def prune_messages(self, prune_messages: bool) -> None:
        """Enable/Disable pruning messages
        
        Args:
            prune_messages (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.prune_messages = True        
        """
        self._prune_messages = prune_messages

    @property
    def prune_stubs(self) -> bool:
        """Treats the prune_stubs as a read-only attribute.

        Returns:
            bool: Whether pruning stubs is enabled.
        """
        return self._prune_stubs

    @prune_stubs.setter
    def prune_stubs(self, prune_stubs: bool) -> None:
        """Enable/Disable pruning stubs
        
        Args:
            prune_stubs (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.prune_stubs = True        
        """
        self._prune_stubs = prune_stubs

    @property
    def skip_unread_messages(self) -> bool:
        """Treats the skip_unread_messages as a read-only attribute.

        Returns:
            bool: Whether skipping unread messages is enabled.
        """
        return self._skip_unread_messages

    @skip_unread_messages.setter
    def skip_unread_messages(self, skip_unread_messages: bool) -> None:
        """Enable/Disable skipping unread messages
        
        Args:
            skip_unread_messages (bool): True to skip unread messages, False otherwise.

        Usage:
            >>> cleanup_policy.skip_unread_messages = True        
        """
        self._skip_unread_messages = skip_unread_messages

    @property
    def stop_archive_if_size(self) -> int:
        """Treats the stop_archive_if_size as a read-only attribute.

        Returns:
            int: The size to stop archiving if.
        """
        return self._stop_archive_if_size

    @stop_archive_if_size.setter
    def stop_archive_if_size(self, stop_archive_if_size: int) -> None:
        """Sets the size threshold to stop archiving
        
        Args:
            stop_archive_if_size (int): Size threshold to stop archiving.

        Usage:
            >>> cleanup_policy.stop_archive_if_size = 75        
        """
        self._stop_archive_if_size = stop_archive_if_size

    @property
    def truncate_body(self) -> bool:
        """Treats the truncate_body as a read-only attribute.

        Returns:
            bool: Whether truncating the body is enabled.
        """
        return self._truncate_body

    @truncate_body.setter
    def truncate_body(self, truncate_body: bool) -> None:
        """Enable/Disable body truncation
        
        Args:
            truncate_body (bool): True to enable truncation, False to disable.

        Usage:
            >>> cleanup_policy.truncate_body = True        
        """
        self._truncate_body = truncate_body

    @property
    def truncate_body_to_bytes(self) -> int:
        """Treats the truncate_body_to_bytes as a read-only attribute.

        Returns:
            int: The number of bytes to truncate the body to.
        """
        return self._truncate_body_to_bytes

    @truncate_body_to_bytes.setter
    def truncate_body_to_bytes(self, truncate_body_to_bytes: int) -> None:
        """Sets the number of bytes to truncate the body to
        
        Args:
            truncate_body_to_bytes (int): Number of bytes for truncation.

        Usage:
            >>> cleanup_policy.truncate_body_to_bytes = 1024        
        """
        self._truncate_body_to_bytes = truncate_body_to_bytes

    @property
    def used_disk_space(self) -> bool:
        """Treats the used_disk_space as a read-only attribute.

        Returns:
            bool: Whether considering used disk space is enabled.
        """
        return self._used_disk_space

    @used_disk_space.setter
    def used_disk_space(self, used_disk_space: bool) -> None:
        """Enable/Disable considering used disk space
        
        Args:
            used_disk_space (bool): True to enable, False to disable.

        Usage:
            >>> cleanup_policy.used_disk_space = True        
        """
        self._used_disk_space = used_disk_space

    @property
    def used_disk_space_value(self) -> int:
        """Treats the used_disk_space_value as a read-only attribute.

        Returns:
            int: The used disk space value.
        """
        return self._used_disk_space_value

    @used_disk_space_value.setter
    def used_disk_space_value(self, used_disk_space_value: int) -> None:
        """Sets the used disk space value threshold
        
        Args:
            used_disk_space_value (int): Disk space threshold value.

        Usage:
            >>> cleanup_policy.used_disk_space_value = 50        
        """
        self._used_disk_space_value = used_disk_space_value

    @property
    def include_folder_filter(self) -> str:
        """Treats the include_folder_filter as a read-only attribute.

        Returns:
            str: The filter for including folders.
        """
        return self._include_folder_filter

    @include_folder_filter.setter
    def include_folder_filter(self, include_folder_filter: str) -> None:
        """Sets the filter for including folders
        
        Args:
            include_folder_filter (str): Comma-separated list of folders to include.

        Usage:
            >>> cleanup_policy.include_folder_filter = "Inbox,Sent Items"        
        """
        self._include_folder_filter = include_folder_filter

    @property
    def exclude_folder_filter(self) -> str:
        """Treats the exclude_folder_filter as a read-only attribute.

        Returns:
            str: The filter for excluding folders.
        """
        return self._exclude_folder_filter

    @exclude_folder_filter.setter
    def exclude_folder_filter(self, exclude_folder_filter: str) -> None:
        """Sets the filter for excluding folders
        
        Args:
            exclude_folder_filter (str): Comma-separated list of folders to exclude.

        Usage:
            >>> cleanup_policy.exclude_folder_filter = "Junk Mail,Spam"        
        """
        self._exclude_folder_filter = exclude_folder_filter

    @property
    def exclude_message_class_filter(self) -> str:
        """Treats the exclude_message_class_filter as a read-only attribute.

        Returns:
            str: The filter for excluding message classes.
        """
        return self._exclude_message_class_filter

    @exclude_message_class_filter.setter
    def exclude_message_class_filter(self, exclude_message_class_filter: str) -> None:
        """Sets the filter for excluding message classes
        
        Args:
            exclude_message_class_filter (str): Comma-separated list of message classes to exclude.

        Usage:
            >>> cleanup_policy.exclude_message_class_filter = "Appointments,Tasks"        
        """
        self._exclude_message_class_filter = exclude_message_class_filter

    def _initialize_policy_json(self) -> dict:
        """
            sets values for creating the add policy json

        Returns:
            dict: The policy JSON.
        """

        policy_json = {
            "policy": {
                "policyType": 1,
                "agentType": {
                    "appTypeId": 137
                },
                "detail": {
                    "emailPolicy": {
                        "emailPolicyType": 2,
                        "cleanupPolicy": {
                            "usedDiskSpace": self._used_disk_space,
                            "createStubs": self._create_stubs,
                            "usedDiskSpaceValue": self._used_disk_space_value,
                            "pruneMsgs": self._prune_messages,
                            "primaryMailbox": self._primary_mailbox,
                            "disabledMailbox": self._disabled_mailbox,
                            "pruneErasedMsgsOrStubs": self._prune_erased_messages_or_stubs,
                            "collectMsgsDaysAfter": self._collect_messages_days_after,
                            "numOfDaysForSourcePruning": self._number_of_days_for_source_pruning,
                            "collectMsgsLargerThan": self._collect_messages_larger_than,
                            "skipUnreadMsgs": self._skip_unread_messages,
                            "collectMsgWithAttach": self._collect_messages_with_attachments,
                            "leaveMsgBody": self._leave_message_body,
                            "mailboxQuota": self.mailbox_quota,
                            "truncateBody": self._truncate_body,
                            "pruneStubs": self._prune_stubs,
                            "enableMessageRules": self._enable_message_rules,
                            "archiveMailbox": self._archive_mailbox,
                            "archiveIfSize": self._archive_if_size,
                            "truncateBodyToBytes": self._truncate_body_to_bytes,
                            "addRecallLink": self._add_recall_link,
                            "stopArchiveIfSize": self._stop_archive_if_size,
                            "excludeMessageClassFilter": {
                                "folderPatternsAvailable": [
                                    "Appointments",
                                    "Contacts",
                                    "Schedules",
                                    "Tasks"
                                ]
                            },
                            "includeFolderFilter": {
                                "folderPatternsAvailable": [
                                    "Deleted Items",
                                    "Drafts",
                                    "Inbox",
                                    "Sent Items"
                                ]
                            },
                            "excludeFolderFilter": {
                                "folderPatternsSelected": [
                                    "Junk Mail",
                                    "Sync Issues"
                                ],
                                "folderPatternsAvailable": [
                                    "Deleted Items",
                                    "Drafts",
                                    "Inbox",
                                    "Sent Items"
                                ]
                            }
                        }
                    }
                },
                "policyEntity": {
                    "policyName": self._name
                }
            }
        }

        return policy_json

class RetentionPolicy():
    """Class for performing Retention policy operations for a specific retention policy.

    Attributes:
        _commcell_object: Commcell object associated with the retention policy.
        _name (str): Name of the retention policy.
        _email_policy_type (int): Type of email policy (default: 3).
        _number_of_days_for_media_pruning (int): Number of days for media pruning (default: -1).
        _retention_type (int): Type of retention (default: 0).
        _exchange_folder_retention (bool): Flag indicating if exchange folder retention is enabled (default: False).
        _exchange_retention_tags (bool): Flag indicating if exchange retention tags are enabled (default: False).

    Usage:
        rp = RetentionPolicy(commcell_object, 'MyRetentionPolicy')
    """

    def __init__(self, commcell_object: 'Commcell', retention_policy_name: str) -> None:
        """Initialise the Retention Policy class instance.

        Args:
            commcell_object: Commcell object associated with the retention policy.
            retention_policy_name (str): Name of the retention policy.
        """

        self._commcell_object = commcell_object
        self._name = retention_policy_name
        self._email_policy_type = 3
        self._number_of_days_for_media_pruning = -1
        self._retention_type = 0
        self._exchange_folder_retention = False
        self._exchange_retention_tags = False

    @property
    def name(self) -> str:
        """Treats the name as a read-only attribute.

        Returns:
            str: The name of the retention policy.

        Usage:
            name = retention_policy.name
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the name of the retention policy.

        Args:
            name (str): The new name for the retention policy.

        Usage:
            retention_policy.name = "NewRetentionPolicyName"
        """
        self._name = name

    @property
    def email_policy_type(self) -> int:
        """Treats the email_policy_type as a read-only attribute.

        Returns:
            int: The email policy type.

        Usage:
            email_type = retention_policy.email_policy_type
        """
        return self._email_policy_type

    @property
    def days_for_media_pruning(self) -> int:
        """Treats the number_of_days_for_media_pruning as a read-only attribute.

        Returns:
            int: The number of days for media pruning.

        Usage:
            days = retention_policy.days_for_media_pruning
        """
        return self._number_of_days_for_media_pruning

    @days_for_media_pruning.setter
    def days_for_media_pruning(self, days_for_media_pruning: int) -> None:
        """Sets the number of days for media pruning
        
        Args:
            days_for_media_pruning (int): Number of days for media pruning.

        Usage:
            >>> retention_policy.days_for_media_pruning = 30        
        """
        self._number_of_days_for_media_pruning = days_for_media_pruning

    @property
    def retention_type(self) -> int:
        """Treats the retention_type as a read-only attribute.

        Returns:
            int: The retention type.

        Usage:
            retention_type = retention_policy.retention_type
        """
        return self._retention_type

    @retention_type.setter
    def retention_type(self, retention_type: int) -> None:
        """Sets the retention type
        
        Args:
            retention_type (int): The retention type value.

        Usage:
            >>> retention_policy.retention_type = 1        
        """
        self._retention_type = retention_type

    @property
    def exchange_folder_retention(self) -> bool:
        """Treats the exchange_folder_retention as a read-only attribute.

        Returns:
            bool: True if exchange folder retention is enabled, False otherwise.

        Usage:
            exchange_folder_retention = retention_policy.exchange_folder_retention
        """
        return self._exchange_folder_retention

    @exchange_folder_retention.setter
    def exchange_folder_retention(self, exchange_folder_retention: bool) -> None:
        """Enable/Disable exchange folder retention
        
        Args:
            exchange_folder_retention (bool): True to enable, False to disable.

        Usage:
            >>> retention_policy.exchange_folder_retention = True        
        """
        self._exchange_folder_retention = exchange_folder_retention

    @property
    def exchange_retention_tags(self) -> bool:
        """Treats the exchange_retention_tags as a read-only attribute.

        Returns:
            bool: True if exchange retention tags are enabled, False otherwise.

        Usage:
            exchange_retention_tags = retention_policy.exchange_retention_tags
        """
        return self._exchange_retention_tags

    @exchange_retention_tags.setter
    def exchange_retention_tags(self, exchange_retention_tags: bool) -> None:
        """Enable/Disable exchange retention tags
        
        Args:
            exchange_retention_tags (bool): True to enable, False to disable.

        Usage:
            >>> retention_policy.exchange_retention_tags = False        
        """
        self._exchange_retention_tags = exchange_retention_tags

    def _initialize_policy_json(self) -> dict:
        """Sets values for creating the add policy json.

        Returns:
            dict: A dictionary containing the JSON structure for the retention policy.
        """
        policy_json = {
            "policy": {
                "policyType": 1,
                "agentType": {
                    "appTypeId": 137
                },
                "detail": {
                    "emailPolicy": {
                        "emailPolicyType": 3,
                        "retentionPolicy": {
                            "numOfDaysForMediaPruning": self.days_for_media_pruning,
                            "type": self.retention_type,
                            "advanceRetentionOption": {
                                "bExchangeFoldersRetention": self.exchange_folder_retention,
                                "bExchangeRetentionTags": self.exchange_retention_tags
                            }
                        }
                    }
                },
                "policyEntity": {
                    "policyName": self.name
                }
            }
        }

        return policy_json

class ContentIndexingPolicy():
    """Class for performing Content Indexing policy operations for a specific CI policy.

    Attributes:
        _commcell_object: CommCell object associated with this policy.
        _name (str): Name of the Content Indexing policy.
        _file_policy_type (int): Type of the file policy (default: 5).
        _includeDocTypes (str): Comma-separated string of document types to include.
        _index_server_name (Optional[str]): Name of the index server.
        _data_access_node (Optional[str]): Name of the data access node.
        _exclude_paths (List[str]): List of paths to exclude from indexing.
        _min_doc_size (int): Minimum document size to index (in MB).
        _max_doc_size (int): Maximum document size to index (in MB).

    Usage:
        >>> ci_policy = ContentIndexingPolicy(commcell_object, 'MyCIPolicy')
    """

    def __init__(self, commcell_object: 'Commcell', ci_policy_name: str) -> None:
        """Initialise the Content indexing Policy class instance.

        Args:
            commcell_object: The CommCell object.
            ci_policy_name (str): The name of the Content Indexing policy.
        """
        self._commcell_object = commcell_object
        self._name = ci_policy_name
        self._file_policy_type = 5
        self._includeDocTypes = "*.bmp,*.csv,*.doc,*.docx,*.dot,*.eml,*.htm,*.html,*.jpeg,*.jpg," \
                                "*.log,*.msg,*.odg,*.odp,*.ods,*.odt,*.pages,*.pdf,*.png,*.ppt," \
                                "*.pptx,*.rtf,*.txt,*.xls,*.xlsx,*.xmind,*.xml"
        self._index_server_name: Optional[str] = None
        self._data_access_node: Optional[str] = None
        self._exclude_paths: List[str] = ["C:\\Program Files", "C:\\Program Files (x86)", "C:\\Windows"]
        self._min_doc_size = 0
        self._max_doc_size = 50

    @property
    def name(self) -> str:
        """Treats the name as a read-only attribute.

        Returns:
            str: The name of the Content Indexing policy.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the name of the Content Indexing policy
        
        Args:
            value (str): The new name for the policy.

        Usage:
            >>> ci_policy.name = "NewPolicyName"        
        """
        self._name = value

    @property
    def include_doc_types(self) -> str:
        """Treats the include_doc_types as a read-only attribute.

        Returns:
            str: The comma-separated string of included document types.
        """
        return self._includeDocTypes

    @include_doc_types.setter
    def include_doc_types(self, value: str) -> None:
        """Sets the included document types for content indexing
        
        Args:
            value (str): Comma-separated string of document types to include.

        Usage:
            >>> ci_policy.include_doc_types = "*.pdf,*.doc,*.txt"        
        """
        self._includeDocTypes = value

    @property
    def index_server_name(self) -> Optional[str]:
        """Treats the index_server_name as a read-only attribute.

        Returns:
            Optional[str]: The name of the index server.
        """
        return self._index_server_name

    @index_server_name.setter
    def index_server_name(self, value: str) -> None:
        """Sets the index server name for content indexing
        
        Args:
            value (str): The name of the index server.

        Usage:
            >>> ci_policy.index_server_name = "IndexServer1"        
        """
        self._index_server_name = value

    @property
    def data_access_node(self) -> Optional[str]:
        """Treats the data_access_node as a read-only attribute.

        Returns:
            Optional[str]: The name of the data access node.
        """
        return self._data_access_node

    @data_access_node.setter
    def data_access_node(self, value: str) -> None:
        """Sets the data access node for content indexing
        
        Args:
            value (str): The name of the data access node.

        Usage:
            >>> ci_policy.data_access_node = "DataAccessNode1"        
        """
        self._data_access_node = value

    @property
    def min_doc_size(self) -> int:
        """Treats the min_doc_size as a read-only attribute.

        Returns:
            int: The minimum document size to index (in MB).
        """
        return self._min_doc_size

    @min_doc_size.setter
    def min_doc_size(self, value: int) -> None:
        """Sets the minimum document size for content indexing
        
        Args:
            value (int): Minimum document size in MB.

        Usage:
            >>> ci_policy.min_doc_size = 0        
        """
        self._min_doc_size = value

    @property
    def max_doc_size(self) -> int:
        """Treats the max_doc_size as a read-only attribute.

        Returns:
            int: The maximum document size to index (in MB).
        """
        return self._max_doc_size

    @max_doc_size.setter
    def max_doc_size(self, value: int) -> None:
        """Sets the maximum document size for content indexing
        
        Args:
            value (int): Maximum document size in MB.

        Usage:
            >>> ci_policy.max_doc_size = 50        
        """
        self._max_doc_size = value

    @property
    def exclude_paths(self) -> List[str]:
        """Treats the exclude_paths as a read-only attribute.

        Returns:
            List[str]: The list of paths to exclude from indexing.
        """
        return self._exclude_paths

    @exclude_paths.setter
    def exclude_paths(self, value: List[str]) -> None:
        """Sets the paths to exclude from content indexing
        
        Args:
            value (List[str]): List of paths to exclude from indexing.

        Usage:
            >>> ci_policy.exclude_paths = ["C:\\Temp", "C:\\Windows"]        
        """
        self._exclude_paths = value

    def _initialize_policy_json(self) -> dict:
        """Sets values for creating the add policy json.

        Raises:
            SDKException: If any of the required attributes are not of the correct type.

        Returns:
            dict: The JSON representation of the Content Indexing policy.

        Usage:
            >>> policy_json = self._initialize_policy_json()
        """
        if not isinstance(self._index_server_name, str) or not isinstance(self._data_access_node, str) \
            or not isinstance(self._exclude_paths, list) or not isinstance(self._includeDocTypes, str) \
                or not isinstance(self._name, str) or not isinstance(self._min_doc_size, int) \
                or not isinstance(self._max_doc_size, int):
            raise SDKException('ConfigurationPolicies', '101')
        policy_json = {
            "policy": {
                "policyType": 2,
                "flags": 0,
                "agentType": {
                    "appTypeId": 33
                },
                "detail": {
                    "filePolicy": {
                        "filePolicyType": self._file_policy_type,
                        "contentIndexingPolicy": {
                            "includeDocTypes": self._includeDocTypes,
                            "copyPrecedence": 1,
                            "minDocSize": self._min_doc_size,
                            "searchEngineId": int(self._commcell_object.index_servers.
                                                  get(self._index_server_name).index_server_client_id),
                            "contentIndexVersionsAfterNumberOfDays": -1,
                            "maxDocSize": self._max_doc_size,
                            "globalFilterFlag": 0,
                            "excludePaths": self._exclude_paths,
                            "dataAccessNodes": {
                                "numberOfStreams": 0,
                                "dataAccessNodes": [
                                    {
                                        "clientName": self._data_access_node,
                                        "clientId": int(self._commcell_object.clients.
                                                        get(self._data_access_node).client_id),
                                        "_type_": 3
                                    }
                                ]
                            }
                        }
                    }
                },
                "policyEntity": {
                    "policyName": self._name
                }
            }
        }
        return policy_json
