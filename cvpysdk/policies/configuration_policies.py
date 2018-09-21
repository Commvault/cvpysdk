# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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


ConfigurationPolicies:

    __init__(commcell_object)   --  initialize the ConfigurationPolicies instance for the Commcell

    __str__()                   --  returns all the ConfigurationPolicies policies associated
    with the Commcell

    __repr__()                  --  returns a string for the instance of the
    ConfigurationPolicies class

    _get_policies()             --  gets all the Configuration policies of the Commcell

    has_policy(policy_name)     --  checks if a Configuration policy exists with the
    given name in a particular instance

    get(policy_name)            --  returns a ConfigurationPolicy object of the
    specified Configuration policy name

    add(policy_object)          --  adds a new Configuration policy to the
    ConfigurationPolicies instance, and returns an object of corresponding policy_type

    delete(policy_name)         --  removes the specified Configuration policy from the Commcell

    get_policy_object()         --  get the policy object based on policy type


"""

from __future__ import unicode_literals

from past.builtins import basestring

from ..exception import SDKException


class ConfigurationPolicies(object):
    """Class for getting all the Configuration policies associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the ConfigurationPolicies class.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the ConfigurationPolicies class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._POLICY = self._services['GET_CONFIGURATION_POLICIES']
        self._policies = None
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of the ConfigurationPolicies class."""
        return "ConfigurationPolicies class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_policies(self):
        """Gets all the Configuration policies associated to the
            commcell specified by commcell object.

            Returns:
                dict    -   consists of all Configuration policies of the commcell

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

    def has_policy(self, policy_name):
        """Checks if a Configuration policy exists in the commcell with
            the input Configuration policy name.

            Args:
                policy_name     (str)   --  name of the Configuration policy

            Returns:
                bool    -   boolean output whether the Configuration policy exists in the commcell
                or not

            Raises:
                SDKException:
                    if type of the configuration policy name argument is not string

        """
        if not isinstance(policy_name, basestring):
            raise SDKException('ConfigurationPolicies', '101')

        return self._policies and policy_name.lower() in self._policies

    def _get_policy_id(self, policy_name):

        if not isinstance(policy_name, basestring):
            raise SDKException('ConfigurationPolicies', '101')
        if policy_name.lower() in self._policies:
            return self._policies[policy_name.lower()][0]

    def get(self, configuration_policy_name, policy_type):
        """Returns a ConfigurationPolicy object of the specified Configuration policy name.

            Args:
                configuration_policy_name     (str)   --  name of the configuration policy
                policy_type                    (str)   --  type of the policy

            Returns:
                object - instance of the ConfigurationPolicy class for the given policy name

            Raises:
                SDKException:
                    if type of the Configuration policy name argument is not string

                    if no Configuration policy exists with the given name
        """
        if not isinstance(configuration_policy_name, basestring):
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

    def get_policy_object(self, policy_type, configuration_policy_name):
        """Get a  Policy object based on policy type

            Args:
                policy_type                 (str)   --  type of policy to create the object of

                    Valid values are:

                        - Archive

                        - Cleanup

                        - Retention

                        - Journal

                configuration_policy_name   (str)   --  name of the configuration Policy

            Returns:
                object  -   instance of the appropriate Policy class


        """

        policy_types = {
            "Archive": ArchivePolicy,
            "Journal": JournalPolicy,
            "Cleanup": CleanupPolicy,
            "Retention": RetentionPolicy
        }

        try:
            return policy_types[policy_type](self._commcell_object, configuration_policy_name)
        except KeyError:
            raise SDKException(
                'ConfigurationPolicies',
                '102',
                'Policy Type {} is not supported'.format(policy_type)
            )

    def delete(self, configuration_policy_name):
        """Deletes a Configuration policy from the commcell.

            Args:
                configuration_policy_name (str)  --  name of the configuration policy to delete

            Raises:
                SDKException:
                    if type of the configuration policy name argument is not string

                    if failed to delete configuration policy

                    if response is empty

                    if response is not success
        """
        if not isinstance(configuration_policy_name, basestring):
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
                except ValueError:
                    if response.text:
                        self.refresh()
                        return response.text.strip()
                    else:
                        raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'ConfigurationPolicies', '102', 'No policy exists with name: {0}'.format(
                    configuration_policy_name)
            )

    def add_policy(self, policy_object):
        """Adds a new Configuration Policy to the Commcell.

            Args:
                policy_object(object)         --  policy onject based on type
                                                    of policy
            Raises:
                SDKException:
                    if failed to create configuration policy

                    if response is empty

                    if response is not success
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
                    self._policies = self._get_policies()
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

    def refresh(self):
        """Refresh the Virtual Machine policies."""
        self._policies = self._get_policies()


class ConfigurationPolicy(object):

    """Class for representing a single Configuration Policy. Contains method definitions for
        common operations among all Configuration Policies"""

    def __init__(self, commcell_object, configuration_policy_name, configuration_policy_id=None):
        """
        Initialize object of the ConfigurationPolicy class.
            Args:
                commcell_object    (object)  --  instance of the Commcell class
                configuration_policy_name     (str)     --
                configuration_policy_id       (int)     --
            Returns:
                object - instance of the ConfigurationPolicies class
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
    def configuration_policy_id(self):
        """Treats the configuration policy id as a read-only attribute."""
        return self._configuration_policy_id

    @property
    def configuration_policy_name(self):
        """Treats the configuration policy name as a read-only attribute."""
        return self._configuration_policy_name

    def _get_configuration_policy_id(self):
        """Gets the Configuration policy id asscoiated with the Configuration policy"""

        configuration_policies = ConfigurationPolicies(self._commcell_object)
        return configuration_policies._get_policies()[self._configuration_policy_name.lower()][0]


class ArchivePolicy():
    """Class for performing Archive policy operations for a specific archive policy"""

    def __init__(self, commcell_object, archive_policy_name):
        """Initialise the Archive Policy class instance."""
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
    def name(self):
        """Treats the name as a read-only attribute."""
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of the policy"""
        self._name = name

    @property
    def email_policy_type(self):
        """Treats the email_policy_type as a read-only attribute."""
        return self._email_policy_type

    @property
    def archive_mailbox(self):
        """Treats the archive_mailbox as a read-only attribute."""
        return self._archive_mailbox

    @archive_mailbox.setter
    def archive_mailbox(self, archive_mailbox):
        """Enable/Disable archive_mailbox option for policy"""
        self._archive_mailbox = archive_mailbox

    @property
    def backup_deleted_item_retention(self):
        """Treats the backup_deleted_item_retention as a read-only attribute."""
        return self._backup_deleted_item_retention

    @backup_deleted_item_retention.setter
    def backup_deleted_item_retention(self, backup_deleted_item_retention):
        """Enable/Disable backup deleted item retention"""
        self._backup_deleted_item_retention = backup_deleted_item_retention

    @property
    def backup_stubs(self):
        """Treats the backup_stubs as a read-only attribute."""
        return self._backup_stubs

    @backup_stubs.setter
    def backup_stubs(self, backup_stubs):
        """Sets backup stubs option on policy"""
        self._backup_stubs = backup_stubs

    @property
    def disabled_mailbox(self):
        """Treats the disabled_mailbox as a read-only attribute."""
        return self._disabled_mailbox

    @disabled_mailbox.setter
    def disabled_mailbox(self, disabled_mailbox):
        """Enable/Disable disable mailbox on policy"""
        self._disabled_mailbox = disabled_mailbox

    @property
    def enable_mailbox_quota(self):
        """Treats the enable_mailbox_quota as a read-only attribute."""
        return self._enable_mailbox_quota

    @enable_mailbox_quota.setter
    def enable_mailbox_quota(self, enable_mailbox_quota):
        """Sets the mailbox quota value"""
        self._enable_mailbox_quota = enable_mailbox_quota

    @property
    def include_messages_larger_than(self):
        """Treats the include_messages_larger_than as a read-only attribute."""
        return self._include_messages_larger_than

    @include_messages_larger_than.setter
    def include_messages_larger_than(self, include_messages_larger_than):
        """Sets the message rule include message larger than"""
        self._include_messages_larger_than = include_messages_larger_than

    @property
    def include_messages_older_than(self):
        """Treats the include_messages_older_than as a read-only attribute."""
        return self._include_messages_older_than

    @include_messages_older_than.setter
    def include_messages_older_than(self, include_messages_older_than):
        """Sets the message rule include messages older than"""
        self._include_messages_older_than = include_messages_older_than

    @property
    def include_messages_with_attachements(self):
        """Treats the include_messages_with_attachements as a read-only attribute."""
        return self._include_messages_with_attachements

    @include_messages_with_attachements.setter
    def include_messages_with_attachements(self, include_messages_with_attachements):
        """Sets the message rule include messages with attachments"""
        self._include_messages_with_attachements = include_messages_with_attachements

    @property
    def primary_mailbox(self):
        """Treats the primary_mailbox as a read-only attribute."""
        return self._primary_mailbox

    @primary_mailbox.setter
    def primary_mailbox(self, primary_mailbox):
        """Enable/Disable primary mailbox on policy """
        self._primary_mailbox = primary_mailbox

    @property
    def skip_mailboxes_exceeded_quota(self):
        """Treats the skip_mailboxes_exceeded_quota as a read-only attribute."""
        return self._skip_mailboxes_exceeded_quota

    @skip_mailboxes_exceeded_quota.setter
    def skip_mailboxes_exceeded_quota(self, skip_mailboxes_exceeded_quota):
        """Sets the mailbox exceeded quota value"""
        self._skip_mailboxes_exceeded_quota = skip_mailboxes_exceeded_quota

    @property
    def include_discovery_holds_folder(self):
        """Treats the include_discovery_holds_folder as a read-only attribute."""
        return self._include_discovery_holds_folder

    @include_discovery_holds_folder.setter
    def include_discovery_holds_folder(self, include_discovery_holds_folder):
        """Enable/Disable disocvery hold folder"""
        self._include_discovery_holds_folder = include_discovery_holds_folder

    @property
    def include_purges_folder(self):
        """Treats the include_purges_folder as a read-only attribute."""
        return self._include_purges_folder

    @include_purges_folder.setter
    def include_purges_folder(self, include_purges_folder):
        """Enable/Disable Purges folder"""
        self._include_purges_folder = include_purges_folder

    @property
    def include_version_folder(self):
        """Treats the include_version_folder as a read-only attribute."""
        return self._include_version_folder

    @include_version_folder.setter
    def include_version_folder(self, include_version_folder):
        """Enable/Disable versions folder"""
        self._include_version_folder = include_version_folder

    @property
    def save_conversation_meta_data(self):
        """Treats the save_conversation_meta_data as a read-only attribute."""
        return self._save_conversation_meta_data

    @save_conversation_meta_data.setter
    def save_conversation_meta_data(self, save_conversation_meta_data):
        """sets the save conversation meta data"""
        self._save_conversation_meta_data = save_conversation_meta_data

    @property
    def include_categories(self):
        """Treats the include_categories as a read-only attribute."""
        return self._include_categories

    @include_categories.setter
    def include_categories(self, include_categories):
        """sets the include categories option on policy"""
        self._include_categories = include_categories

    @property
    def include_folder_filter(self):
        """Treats the include_folder_filter as a read-only attribute."""
        return self._include_folder_filter

    @include_folder_filter.setter
    def include_folder_filter(self, include_folder_filter):
        """sets include folder filter on policy"""
        self._include_folder_filter = include_folder_filter

    @property
    def exclude_folder_filter(self):
        """Treats the exclude_folder_filter as a read-only attribute."""
        return self._exclude_folder_filter

    @exclude_folder_filter.setter
    def exclude_folder_filter(self, exclude_folder_filter):
        """sets exclude folder filter on policy"""
        self._exclude_folder_filter = exclude_folder_filter

    @property
    def exclude_message_class_filter(self):
        """Treats the exclude_message_class_filter as a read-only attribute."""
        return self._exclude_message_class_filter

    @exclude_message_class_filter.setter
    def exclude_message_class_filter(self, exclude_message_class_filter):
        """sets message class filters on policy"""
        self._exclude_message_class_filter = exclude_message_class_filter

    @property
    def content_index_behind_alert(self):
        """Treats the content_index_behind_alert as a read-only attribute."""
        return self._content_index_behind_alert

    @content_index_behind_alert.setter
    def content_index_behind_alert(self, content_index_behind_alert):
        """sets content index alert"""
        self._content_index_behind_alert = content_index_behind_alert

    @property
    def content_index_data_over(self):
        """Treats the content_index_data_over as a read-only attribute."""
        return self._content_index_data_over

    @content_index_data_over.setter
    def content_index_data_over(self, content_index_data_over):
        """sets content Index data over value"""
        self._content_index_data_over = content_index_data_over

    @property
    def deferred_days(self):
        """Treats the deferred_days as a read-only attribute."""
        return self._deferred_days

    @deferred_days.setter
    def deferred_days(self, deferred_days):
        """sets deferred days"""
        self._deferred_days = deferred_days

    @property
    def enable_content_index(self):
        """Treats the enable_content_index as a read-only attribute."""
        return self._enable_content_index

    @enable_content_index.setter
    def enable_content_index(self, enable_content_index):
        """Enable/Disable ContentIndex"""
        self._enable_content_index = enable_content_index

    @property
    def enable_deferred_days(self):
        """Treats the enable_deferred_days as a read-only attribute."""
        return self._enable_deferred_days

    @enable_deferred_days.setter
    def enable_deferred_days(self, enable_deferred_days):
        """Enable/Disable deferred days"""
        self._enable_deferred_days = enable_deferred_days

    @property
    def enable_preview_generation(self):
        """Treats the enable_preview_generation as a read-only attribute."""
        return self._enable_preview_generation

    @enable_preview_generation.setter
    def enable_preview_generation(self, enable_preview_generation):
        """Enable/Disable preview generation"""
        self._enable_preview_generation = enable_preview_generation

    @property
    def jobs_older_than(self):
        """Treats the jobs_older_than as a read-only attribute."""
        return self._jobs_older_than

    @jobs_older_than.setter
    def jobs_older_than(self, jobs_older_than):
        """sets job older than value"""
        self._jobs_older_than = jobs_older_than

    @property
    def retention_days_for_ci(self):
        """Treats the retention_days_for_ci as a read-only attribute."""
        return self._retention_days_for_ci

    @retention_days_for_ci.setter
    def retention_days_for_ci(self, retention_days_for_ci):
        """sets retention for ContentIndex"""
        self._retention_days_for_ci = retention_days_for_ci

    @property
    def start_time(self):
        """Treats the start_time as a read-only attribute."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """sets start time"""
        self._start_time = start_time

    @property
    def synchronize_on(self):
        """Treats the synchronize_on as a read-only attribute."""
        return self._synchronize_on

    @synchronize_on.setter
    def synchronize_on(self, synchronize_on):
        """sets synchronize on for ContentIndex"""
        self._synchronize_on = synchronize_on

    @property
    def path(self):
        """Treats the path as a read-only attribute."""
        return self._path

    @path.setter
    def path(self, path):
        """sets previewpath for ContentIndex"""
        self._path = path

    @property
    def username(self):
        """Treats the username as a read-only attribute."""
        return self._username

    @username.setter
    def username(self, username):
        """sets username for ContentIndex"""
        self._username = username

    @property
    def password(self):
        """Treats the password as a read-only attribute."""
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def _initialize_policy_json(self):
        """
            sets values for creating the add policy json
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

    """Class for performing Journal policy operations for a specific journal policy"""

    def __init__(self, commcell_object, journal_policy_name):
        """Initialise the Journal Policy class instance."""

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
    def name(self):
        """Treats the name as a read-only attribute."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email_policy_type(self):
        """Treats the email_policy_type as a read-only attribute."""
        return self._email_policy_type

    @property
    def complete_job_mapi_error(self):
        """Treats the complete_job_mapi_error as a read-only attribute."""
        return self._complete_job_mapi_error

    @complete_job_mapi_error.setter
    def complete_job_mapi_error(self, complete_job_mapi_error):
        self._complete_job_mapi_error = complete_job_mapi_error

    @property
    def delete_archived_messages(self):
        """Treats the delete_archived_messages as a read-only attribute."""
        return self._delete_archived_messages

    @delete_archived_messages.setter
    def delete_archived_messages(self, delete_archived_messages):
        self._delete_archived_messages = delete_archived_messages

    @property
    def job_hours_run(self):
        """Treats the job_hours_run as a read-only attribute."""
        return self._job_hours_run

    @job_hours_run.setter
    def job_hours_run(self, job_hours_run):
        self._job_hours_run = job_hours_run

    @property
    def job_messages_protected(self):
        """Treats the job_messages_protected as a read-only attribute."""
        return self._job_messages_protected

    @job_messages_protected.setter
    def job_messages_protected(self, job_messages_protected):
        self._job_messages_protected = job_messages_protected

    @property
    def include_folder_filter(self):
        """Treats the include_folder_filter as a read-only attribute."""
        return self._include_folder_filter

    @include_folder_filter.setter
    def include_folder_filter(self, include_folder_filter):
        self._include_folder_filter = include_folder_filter

    @property
    def exclude_folder_filter(self):
        """Treats the exclude_folder_filter as a read-only attribute."""
        return self._exclude_folder_filter

    @exclude_folder_filter.setter
    def exclude_folder_filter(self, exclude_folder_filter):
        self._exclude_folder_filter = exclude_folder_filter

    @property
    def exclude_message_class_filter(self):
        """Treats the exclude_message_class_filter as a read-only attribute."""
        return self._exclude_message_class_filter

    @exclude_message_class_filter.setter
    def exclude_message_class_filter(self, exclude_message_class_filter):
        self._exclude_message_class_filter = exclude_message_class_filter

    @property
    def content_index_behind_alert(self):
        """Treats the content_index_behind_alert as a read-only attribute."""
        return self._content_index_behind_alert

    @content_index_behind_alert.setter
    def content_index_behind_alert(self, content_index_behind_alert):
        self._content_index_behind_alert = content_index_behind_alert

    @property
    def content_index_data_over(self):
        """Treats the content_index_data_over as a read-only attribute."""
        return self._content_index_data_over

    @content_index_data_over.setter
    def content_index_data_over(self, content_index_data_over):
        self._content_index_data_over = content_index_data_over

    @property
    def deferred_days(self):
        """Treats the deferred_days as a read-only attribute."""
        return self._deferred_days

    @deferred_days.setter
    def deferred_days(self, deferred_days):
        self._deferred_days = deferred_days

    @property
    def enable_content_index(self):
        """Treats the enable_content_index as a read-only attribute."""
        return self._enable_content_index

    @enable_content_index.setter
    def enable_content_index(self, enable_content_index):
        self._enable_content_index = enable_content_index

    @property
    def enable_deferred_days(self):
        """Treats the enable_deferred_days as a read-only attribute."""
        return self._enable_deferred_days

    @enable_deferred_days.setter
    def enable_deferred_days(self, enable_deferred_days):
        self._enable_deferred_days = enable_deferred_days

    @property
    def enable_preview_generation(self):
        """Treats the enable_preview_generation as a read-only attribute."""
        return self.enable_preview_generation

    @enable_preview_generation.setter
    def enable_preview_generation(self, enable_preview_generation):
        self._enable_preview_generation = enable_preview_generation

    @property
    def jobs_older_than(self):
        """Treats the jobs_older_than as a read-only attribute."""
        return self._jobs_older_than

    @jobs_older_than.setter
    def jobs_older_than(self, jobs_older_than):
        self._jobs_older_than = jobs_older_than

    @property
    def retention_days_for_ci(self):
        """Treats the retention_days_for_ci as a read-only attribute."""
        return self._retention_days_for_ci

    @retention_days_for_ci.setter
    def retention_days_for_ci(self, retention_days_for_ci):
        self._retention_days_for_ci = retention_days_for_ci

    @property
    def start_time(self):
        """Treats the start_time as a read-only attribute."""
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def synchronize_on(self):
        """Treats the synchronize_on as a read-only attribute."""
        return self._synchronize_on

    @synchronize_on.setter
    def synchronize_on(self, synchronize_on):
        self._synchronize_on = synchronize_on

    @property
    def path(self):
        """Treats the path as a read-only attribute."""
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def username(self):
        """Treats the username as a read-only attribute."""
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        """Treats the password as a read-only attribute."""
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def _initialize_policy_json(self):
        """
            sets values for creating the add policy json
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

    """Class for performing Cleanup policy operations for a specific cleanup policy"""

    def __init__(self, commcell_object, cleanup_policy_name):
        """Initialise the cleanup Policy class instance."""

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
    def name(self):
        """Treats the name as a read-only attribute."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email_policy_type(self):
        """Treats the email_policy_type as a read-only attribute."""
        return self._email_policy_type

    @property
    def add_recall_link(self):
        """Treats the add_recall_link as a read-only attribute."""
        return self._add_recall_link

    @add_recall_link.setter
    def add_recall_link(self, add_recall_link):
        self._add_recall_link = add_recall_link

    @property
    def archive_if_size(self):
        """Treats the archive_if_size as a read-only attribute."""
        return self._archive_if_size

    @archive_if_size.setter
    def archive_if_size(self, archive_if_size):
        self._archive_if_size = archive_if_size

    @property
    def archive_mailbox(self):
        """Treats the archive_mailbox as a read-only attribute."""
        return self._archive_mailbox

    @archive_mailbox.setter
    def archive_mailbox(self, archive_mailbox):
        self._archive_mailbox = archive_mailbox

    @property
    def collect_messages_with_attachments(self):
        """Treats the collect_messages_with_attachments as a read-only attribute."""
        return self._collect_messages_with_attachments

    @collect_messages_with_attachments.setter
    def collect_messages_with_attachments(self, collect_messages_with_attachments):
        self._collect_messages_with_attachments = collect_messages_with_attachments

    @property
    def collect_messages_days_after(self):
        """Treats the collect_messages_days_after as a read-only attribute."""
        return self._collect_messages_days_after

    @collect_messages_days_after.setter
    def collect_messages_days_after(self, collect_messages_days_after):
        self._collect_messages_days_after = collect_messages_days_after

    @property
    def collect_messages_larger_than(self):
        """Treats the collect_messages_larger_than as a read-only attribute."""
        return self._collect_messages_larger_than

    @collect_messages_larger_than.setter
    def collect_messages_larger_than(self, collect_messages_larger_than):
        self._collect_messages_larger_than = collect_messages_larger_than

    @property
    def create_stubs(self):
        """Treats the create_stubs as a read-only attribute."""
        return self._create_stubs

    @create_stubs.setter
    def create_stubs(self, create_stubs):
        self._create_stubs = create_stubs

    @property
    def disabled_mailbox(self):
        """Treats the disabled_mailbox as a read-only attribute."""
        return self._disabled_mailbox

    @disabled_mailbox.setter
    def disabled_mailbox(self, disabled_mailbox):
        self._disabled_mailbox = disabled_mailbox

    @property
    def enable_message_rules(self):
        """Treats the enable_message_rules as a read-only attribute."""
        return self._enable_message_rules

    @enable_message_rules.setter
    def enable_message_rules(self, enable_message_rules):
        self._enable_message_rules = enable_message_rules

    @property
    def leave_message_body(self):
        """Treats the leave_message_body as a read-only attribute."""
        return self._leave_message_body

    @leave_message_body.setter
    def leave_message_body(self, leave_message_body):
        self._leave_message_body = leave_message_body

    @property
    def mailbox_quota(self):
        """Treats the mailbox_quota as a read-only attribute."""
        return self._mailbox_quota

    @mailbox_quota.setter
    def mailbox_quota(self, mailbox_quota):
        self._mailbox_quota = mailbox_quota

    @property
    def number_of_days_for_source_pruning(self):
        """Treats the number_of_days_for_source_pruning as a read-only attribute."""
        return self._number_of_days_for_source_pruning

    @number_of_days_for_source_pruning.setter
    def number_of_days_for_source_pruning(self, number_of_days_for_source_pruning):
        self._number_of_days_for_source_pruning = number_of_days_for_source_pruning

    @property
    def primary_mailbox(self):
        """Treats the primary_mailbox as a read-only attribute."""
        return self._primary_mailbox

    @primary_mailbox.setter
    def primary_mailbox(self, primary_mailbox):
        self._primary_mailbox = primary_mailbox

    @property
    def prune_erased_messages_or_stubs(self):
        """Treats the prune_erased_messages_or_stubs as a read-only attribute."""
        return self._prune_erased_messages_or_stubs

    @prune_erased_messages_or_stubs.setter
    def prune_erased_messages_or_stubs(self, prune_erased_messages_or_stubs):
        self._prune_erased_messages_or_stubs = prune_erased_messages_or_stubs

    @property
    def prune_messages(self):
        """Treats the prune_messages as a read-only attribute."""
        return self._prune_messages

    @prune_messages.setter
    def prune_messages(self, prune_messages):
        self._prune_messages = prune_messages

    @property
    def prune_stubs(self):
        """Treats the prune_stubs as a read-only attribute."""
        return self._prune_stubs

    @prune_stubs.setter
    def prune_stubs(self, prune_stubs):
        self._prune_stubs = prune_stubs

    @property
    def skip_unread_messages(self):
        """Treats the skip_unread_messages as a read-only attribute."""
        return self._skip_unread_messages

    @skip_unread_messages.setter
    def skip_unread_messages(self, skip_unread_messages):
        self._skip_unread_messages = skip_unread_messages

    @property
    def stop_archive_if_size(self):
        """Treats the stop_archive_if_size as a read-only attribute."""
        return self._stop_archive_if_size

    @stop_archive_if_size.setter
    def stop_archive_if_size(self, stop_archive_if_size):
        self._stop_archive_if_size = stop_archive_if_size

    @property
    def truncate_body(self):
        """Treats the truncate_body as a read-only attribute."""
        return self._truncate_body

    @truncate_body.setter
    def truncate_body(self, truncate_body):
        self._truncate_body = truncate_body

    @property
    def truncate_body_to_bytes(self):
        """Treats the truncate_body_to_bytes as a read-only attribute."""
        return self._truncate_body_to_bytes

    @truncate_body_to_bytes.setter
    def truncate_body_to_bytes(self, truncate_body_to_bytes):
        self._truncate_body_to_bytes = truncate_body_to_bytes

    @property
    def used_disk_space(self):
        """Treats the used_disk_space as a read-only attribute."""
        return self._used_disk_space

    @used_disk_space.setter
    def path(self, used_disk_space):
        self._used_disk_space = used_disk_space

    @property
    def used_disk_space_value(self):
        """Treats the used_disk_space_value as a read-only attribute."""
        return self._used_disk_space_value

    @used_disk_space_value.setter
    def used_disk_space_value(self, used_disk_space_value):
        self._used_disk_space_value = used_disk_space_value

    @property
    def include_folder_filter(self):
        """Treats the include_folder_filter as a read-only attribute."""
        return self._include_folder_filter

    @include_folder_filter.setter
    def include_folder_filter(self, include_folder_filter):
        self._include_folder_filter = include_folder_filter

    @property
    def exclude_folder_filter(self):
        """Treats the exclude_folder_filter as a read-only attribute."""
        return self._exclude_folder_filter

    @exclude_folder_filter.setter
    def exclude_folder_filter(self, exclude_folder_filter):
        self._exclude_folder_filter = exclude_folder_filter

    @property
    def exclude_message_class_filter(self):
        """Treats the exclude_message_class_filter as a read-only attribute."""
        return self._exclude_message_class_filter

    @exclude_message_class_filter.setter
    def exclude_message_class_filter(self, exclude_message_class_filter):
        self._exclude_message_class_filter = exclude_message_class_filter

    def _initialize_policy_json(self):
        """
            sets values for creating the add policy json
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
    """Class for performing Retention policy operations for a specific retention policy"""

    def __init__(self, commcell_object, retention_policy_name):
        """Initialise the Rentention Policy class instance."""

        self._commcell_object = commcell_object
        self._name = retention_policy_name
        self._email_policy_type = 3
        self._number_of_days_for_media_pruning = -1

    @property
    def name(self):
        """Treats the name as a read-only attribute."""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email_policy_type(self):
        """Treats the email_policy_type as a read-only attribute."""
        return self._email_policy_type

    @property
    def days_for_media_pruning(self):
        """Treats the number_of_days_for_media_pruning as a read-only attribute."""
        return self._number_of_days_for_media_pruning

    @days_for_media_pruning.setter
    def days_for_media_pruning(self, days_for_media_pruning):
        self._number_of_days_for_media_pruning = days_for_media_pruning

    def _initialize_policy_json(self):
        """
            sets values for creating the add policy json
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
                            "numOfDaysForMediaPruning": self.days_for_media_pruning
                        }
                    }
                },
                "policyEntity": {
                    "policyName": self.name
                }
            }
        }

        return policy_json
