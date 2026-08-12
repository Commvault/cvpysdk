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

"""File for operating on a Salesforce Backupset.

SalesforceBackupset is the only class defined in this file.

SalesforceBackuset:     Derived class from CloudAppsBackupset Base class, representing a
                            salesforce backupset, and to perform operations on that backupset

SalesforceBackupset:
     __init__()                      --    Backupset class method overwritten to add salesforce
                                               browse options in default browse options

    _get_backupset_properties()      --    Backupset class method overwritten to add salesforce
                                               backupset properties as well

    _prepare_browse_json()           --    Backupset class method overwritten to add salesforce
                                               browse option

    download_cache_path()            --    Fetches download cache path from backupset

    mutual_auth_path()               --    Fetches mutual auth path from backupset

    salesforce_user_name()           --    Fetches salesforce user name from backupset

    is_sync_db_enabled()             --    Determines sync database enabled or not on backupset

    sync_db_type()                   --    Fetches sync database type from backupset

    sync_db_host()                   --    Fetches sync database host name from backupset

    sync_db_instance()               --    Fetches ssync database instance name from backupset

    sync_db_name()                   --    Fetches sync database name from backupset

    sync_db_port()                   --    Fetches sync database port number from backupset

    sync_db_user_name()              --    Fetches sync database user name from backupset

"""

from __future__ import unicode_literals

from ..cabackupset import CloudAppsBackupset
from typing import Dict, Any, Optional

class SalesforceBackupset(CloudAppsBackupset):
    """
    Represents a Salesforce backupset, extending the CloudAppsBackupset base class.

    This class provides specialized functionality for managing Salesforce backupsets,
    including operations for retrieving backupset properties, preparing browse requests,
    and handling Salesforce-specific configuration options. It exposes several properties
    related to Salesforce user credentials, mutual authentication, and synchronization
    database settings, enabling fine-grained control and monitoring of backupset operations.

    Key Features:
        - Initialization with instance object, backupset name, and backupset ID
        - Retrieval of backupset properties
        - Preparation of browse JSON requests with customizable options
        - Access to download cache and mutual authentication paths
        - Management of Salesforce user credentials
        - Configuration and status of synchronization database (sync DB)
        - Properties for sync DB type, host, instance, name, port, and user name
        - Ability to set mutual authentication path

    #ai-gen-doc
    """

    def __init__(self, instance_object: object, backupset_name: str, backupset_id: Optional[int] = None) -> None:
        """Initialize a SalesforceBackupset instance for the specified Salesforce environment.

        Args:
            instance_object: Instance of the Instance class representing the Salesforce environment.
            backupset_name: Name of the backupset as a string.
            backupset_id: Optional integer ID of the backupset.

        Example:
            >>> instance = Instance(...)
            >>> backupset = SalesforceBackupset(instance, "Salesforce_Backupset", backupset_id=123)
            >>> print(f"Backupset created: {backupset}")

        #ai-gen-doc
        """
        self._download_cache_path = None
        self._mutual_auth_path = None
        self._user_name = None
        self._api_token = None
        self._sync_db_enabled = None
        self._sync_db_type = None
        self._sync_db_host = None
        self._sync_db_instance = None
        self._sync_db_name = None
        self._sync_db_port = None
        self._sync_db_user_name = None
        self._sync_db_user_password = None

        super(SalesforceBackupset, self).__init__(instance_object, backupset_name, backupset_id)

        salesforce_browse_options = {
            '_browse_view_name_list': ['TBLVIEW', 'FILEVIEW']
        }

        self._default_browse_options.update(salesforce_browse_options)

    def _get_backupset_properties(self) -> None:
        """Retrieve and set the properties for this Salesforce backupset.

        This method fetches backupset properties from the internal data structure and updates
        relevant attributes such as cache path, mutual authentication path, user credentials,
        and sync database configuration.

        Raises:
            SDKException: If the response containing backupset properties is empty or unsuccessful.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> backupset._get_backupset_properties()
            >>> print(backupset._download_cache_path)
            >>> print(backupset._user_name)
            >>> print(backupset._sync_db_enabled)
            >>> # Access other backupset properties as needed

        #ai-gen-doc
        """
        super(SalesforceBackupset, self)._get_backupset_properties()

        if 'cloudAppsBackupset' in self._properties:
            cloud_apps_backupset = self._properties['cloudAppsBackupset']
            if 'salesforceBackupSet' in cloud_apps_backupset:
                sfbackupset = cloud_apps_backupset['salesforceBackupSet']
                if 'downloadCachePath' in sfbackupset:
                    self._download_cache_path = sfbackupset['downloadCachePath']
                self._mutual_auth_path = sfbackupset.get('mutualAuthPath', '')
                if 'userName' in sfbackupset['userPassword']:
                    self._user_name = sfbackupset['userPassword']['userName']
                if 'syncDatabase' in sfbackupset:
                    self._sync_db_enabled = sfbackupset['syncDatabase'].get('dbEnabled', False)
                if self._sync_db_enabled:
                    if 'dbType' in sfbackupset['syncDatabase']:
                        self._sync_db_type = sfbackupset['syncDatabase']['dbType']
                    if 'dbHost' in sfbackupset['syncDatabase']:
                        self._sync_db_host = sfbackupset['syncDatabase']['dbHost']
                    if 'dbInstance' in sfbackupset['syncDatabase']:
                        self._sync_db_instance = sfbackupset['syncDatabase']['dbInstance']
                    if 'dbName' in sfbackupset['syncDatabase']:
                        self._sync_db_name = sfbackupset['syncDatabase']['dbName']
                    if 'dbPort' in sfbackupset['syncDatabase']:
                        self._sync_db_port = sfbackupset['syncDatabase']['dbPort']
                    if 'userName' in sfbackupset['syncDatabase']['dbUserPassword']:
                        self._sync_db_user_name = sfbackupset[
                            'syncDatabase']['dbUserPassword']['userName']
                    if 'password' in sfbackupset['syncDatabase']['dbUserPassword']:
                        self._sync_db_user_password = sfbackupset[
                            'syncDatabase']['dbUserPassword']['password']

    def _prepare_browse_json(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the JSON object for a Salesforce browse request.

        This method constructs and returns a JSON object containing the necessary
        parameters for performing a browse operation on Salesforce backup data.
        It augments the base browse JSON with Salesforce-specific view options.

        Args:
            options: Dictionary containing browse options, including
                '_browse_view_name_list' for specifying Salesforce browse views.

        Returns:
            Dictionary representing the JSON object for the browse request.

        Example:
            >>> options = {
            ...     '_browse_view_name_list': ['Account', 'Contact'],
            ...     'other_option': 'value'
            ... }
            >>> backupset = SalesforceBackupset(...)
            >>> browse_json = backupset._prepare_browse_json(options)
            >>> print(browse_json)
            {'advOptions': {'browseViewNameList': ['Account', 'Contact']}, ...}

        #ai-gen-doc
        """
        request_json = super(SalesforceBackupset, self)._prepare_browse_json(options)
        salesforce_browse_view = {
            'browseViewNameList': options['_browse_view_name_list']
        }
        request_json['advOptions'].update(salesforce_browse_view)
        return request_json

    @property
    def download_cache_path(self) -> str:
        """Get the path to the download cache for Salesforce backups.

        Returns:
            The file system path to the download cache as a string.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> cache_path = backupset.download_cache_path  # Use dot notation for properties
            >>> print(f"Download cache path: {cache_path}")

        #ai-gen-doc
        """
        return self._download_cache_path

    @property
    def mutual_auth_path(self) -> str:
        """Get the mutual authentication download cache path.

        Returns:
            The file system path as a string where mutual authentication cache is stored.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> cache_path = backupset.mutual_auth_path  # Use dot notation for property access
            >>> print(f"Mutual authentication cache path: {cache_path}")

        #ai-gen-doc
        """
        return self._mutual_auth_path

    @property
    def salesforce_user_name(self) -> str:
        """Get the Salesforce user name associated with this backupset.

        Returns:
            The Salesforce user name as a string.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> user_name = backupset.salesforce_user_name  # Use dot notation for property access
            >>> print(f"Salesforce user: {user_name}")
        #ai-gen-doc
        """
        return self._user_name

    @property
    def is_sync_db_enabled(self) -> bool:
        """Indicate whether the sync database feature is enabled for this Salesforce backupset.

        Returns:
            True if sync database is enabled, False otherwise.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> if backupset.is_sync_db_enabled:
            ...     print("Sync DB is enabled for this backupset.")
            ... else:
            ...     print("Sync DB is not enabled.")
        #ai-gen-doc
        """
        return self._sync_db_enabled

    @property
    def sync_db_type(self) -> str:
        """Get the type of the synchronization database used for Salesforce backups.

        Returns:
            The sync database type as a string.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> db_type = backupset.sync_db_type  # Use dot notation for property access
            >>> print(f"Sync database type: {db_type}")

        #ai-gen-doc
        """
        return self._sync_db_type

    @property
    def sync_db_host(self) -> str:
        """Get the hostname of the sync database used for Salesforce backup operations.

        Returns:
            The sync database hostname as a string.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> hostname = backupset.sync_db_host  # Use dot notation for property access
            >>> print(f"Sync DB Host: {hostname}")
        #ai-gen-doc
        """
        return self._sync_db_host

    @property
    def sync_db_instance(self) -> str:
        """Get the name of the sync database instance for this Salesforce backupset.

        Returns:
            The sync database instance name as a string.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> db_instance_name = backupset.sync_db_instance  # Use dot notation for property access
            >>> print(f"Sync DB instance: {db_instance_name}")
        #ai-gen-doc
        """
        return self._sync_db_instance

    @property
    def sync_db_name(self) -> str:
        """Get the name of the synchronization database for the Salesforce backupset.

        Returns:
            The sync database name as a string.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> db_name = backupset.sync_db_name  # Use dot notation for property access
            >>> print(f"Sync database name: {db_name}")
        #ai-gen-doc
        """
        return self._sync_db_name

    @property
    def sync_db_port(self) -> int:
        """Get the port number used for the sync database connection.

        Returns:
            The sync database port number as an integer.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> port = backupset.sync_db_port  # Use dot notation for property access
            >>> print(f"Sync DB port: {port}")

        #ai-gen-doc
        """
        return self._sync_db_port

    @property
    def sync_db_user_name(self) -> str:
        """Get the username used for database synchronization in Salesforce backupset.

        Returns:
            The sync database username as a string.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> username = backupset.sync_db_user_name  # Use dot notation for property access
            >>> print(f"Sync DB username: {username}")
            >>> # The returned username can be used for authentication or auditing purposes

        #ai-gen-doc
        """
        return self._sync_db_user_name

    @mutual_auth_path.setter
    def mutual_auth_path(self, value: str) -> None:
        """Set the mutual authentication certificate path for the Salesforce backupset.

        This property setter updates the path to the mutual authentication certificate 
        used by the access node for secure communication.

        Args:
            value: The file system path to the mutual authentication certificate on the access node.

        Example:
            >>> backupset = SalesforceBackupset(...)
            >>> backupset.mutual_auth_path = "/etc/certs/salesforce_mutual_auth.pem"
            >>> # The mutual authentication path is now updated for the backupset

        #ai-gen-doc
        """
        if self.mutual_auth_path != value:
            if self.is_sync_db_enabled:
                del self._properties['cloudAppsBackupset']['salesforceBackupSet']['syncDatabase']['dbUserPassword'][
                    'password']
            self._properties['cloudAppsBackupset']['salesforceBackupSet']['mutualAuthPath'] = value
            self.update_properties(self._properties)
