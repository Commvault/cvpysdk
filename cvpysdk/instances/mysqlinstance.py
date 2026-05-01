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

"""
File for operating on a MYSQL Instance.

MYSQLInstance is the only class defined in this file.

MYSQLInstance: Derived class from Instance Base class, representing an
                MYSQL instance, and to perform operations on that instance

MYSQLInstance:
==============

    _get_instance_properties()      -- method to get the properties of the instance

    _restore_json()                 -- returns the apppropriate JSON request to pass for
    Restore In-Place

    restore_in_place()              -- Restores the mysql data/log files specified in the
    input paths list to the same location

    restore_out_of_place()          -- method to perform out of place restore of MySQL data/log/recurring files to the
    destination client.

    _restore_browse_option_json()   -- setter for  browse option  property in restore

    _restore_common_options_json()  -- setter for common options property in restore

    _restore_destination_json()     -- setter for destination options property in restore

    _restore_fileoption_json()      -- setter for file option property in restore

    _restore_admin_option_json()    -- setter for admin option property in restore

    _restore_mysql_option_json()    -- setter for MySQL restore option property in restore


MYSQLInstance instance Attributes:
==================================

    **port**                            -- Returns the MySQL Server Port number

    **mysql_username**                  -- Returns the MySQL Server username

    **nt_username**                     -- Returns the MySQL Server nt username

    **config_file**                     -- Returns the MySQL Server Config File location

    **binary_directory**                -- Returns the MySQL Server Binary File location

    **version**                         -- Returns the MySQL Server version number

    **log_data_directory**              -- Returns the MySQL Server log data directory

    **log_backup_sp_details**           -- Returns the MySQL Server Log backup SP details

    **command_line_sp_details**         -- Returns the MySQL Server commandline SP details

    **autodiscovery_enabled**           -- Returns the MySQL Server auto discovery enabled flag

    **xtrabackup_bin_path**             -- Returns the MySQL Server xtrabackup bin path

    **is_xtrabackup_enabled**           -- Returns the MySQL Server xtrabackup enabled flag

    **proxy_options**                   -- Returns the MySQL Server proxy options

    **mysql_enterprise_backup_binary_path** --  Returns the MySQL Enterprise backup binary path
    details

    **no_lock_status**                  --  Returns the No Lock check box status for MySQL Instance

    **ssl_enabled**                     --  Returns(boolean) True/False based on SSL status

"""

from __future__ import unicode_literals

from ..instance import Instance
from ..exception import SDKException
from ..job import Job

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class MYSQLInstance(Instance):
    """
    Represents a standalone MySQL instance with comprehensive management and restore capabilities.

    This class encapsulates the configuration, properties, and operational controls for a MySQL database instance.
    It provides access to key instance attributes such as port, usernames, configuration files, binary directories,
    version information, and backup/restore options. The class supports both in-place and out-of-place restore operations,
    including advanced options for table-level restores, cloning environments, and redirecting restore paths.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Access to instance properties: port, MySQL/NT usernames, config file, binary directory, version, log directories
        - Backup and restore details: log backup SP, command line SP, xtrabackup, MySQL Enterprise Backup
        - Autodiscovery enablement and management
        - Proxy options and SSL enablement
        - No-lock status management
        - Methods for retrieving instance properties and restoring from JSON configurations
        - In-place and out-of-place restore operations with extensive customization options
        - Support for table-level restore, cloning, redirection, and recurring restores
        - Internal methods for handling restore options and administrative settings

    This class is intended for use in environments where robust management and restoration of MySQL instances is required,
    providing a programmatic interface for both configuration and operational tasks.

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int = None) -> None:
        """Initialize a MYSQLInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this MySQL instance.
            instance_name: The name of the MySQL instance.
            instance_id: The unique identifier for the MySQL instance. Defaults to None.

        #ai-gen-doc
        """
        self._browse_restore_json = None
        self._commonoption_restore_json = None
        self._destination_restore_json = None
        self._fileoption_restore_json = None
        self._instance = None
        self.admin_option_json = None
        self.mysql_restore_json = None
        super(MYSQLInstance, self).__init__(agent_object, instance_name, instance_id)

    @property
    def port(self) -> str:
        """Get the MySQL Server port number for this instance.

        Returns:
            The port number used by the MySQL Server as a string.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('port', None)

    @property
    def mysql_username(self) -> str:
        """Get the MySQL Server username associated with this instance.

        Returns:
            The MySQL server SA (System Administrator) username as a string.

        #ai-gen-doc
        """
        if self.credentials:
            credential_obj = self._commcell_object.credentials.get(self.credentials)
            if credential_obj:
                return credential_obj._credential_properties.get('userName')
        return self._properties.get('mySqlInstance', {}).get('SAUser', {}).get('userName', None)

    @property
    def nt_username(self) -> str:
        """Get the MySQL Server NT username associated with this instance.

        Returns:
            The NT username used for MySQL Server authentication as a string.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('NTUser', {}).get('userName', None)

    @property
    def config_file(self) -> str:
        """Get the location of the MySQL server configuration file.

        Returns:
            The file path to the MySQL server's configuration file as a string.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('ConfigFile', None)

    @property
    def binary_directory(self) -> str:
        """Get the MySQL Server binary file directory location.

        Returns:
            The file system path to the MySQL server's binary directory as a string.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('BinaryDirectory', None)

    @property
    def version(self) -> str:
        """Get the MySQL Server version number for this instance.

        Returns:
            The version number of the MySQL server as a string.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('version', None)

    @property
    def log_data_directory(self) -> str:
        """Get the MySQL Server log data directory path.

        Returns:
            The file system path to the MySQL server's log data directory as a string.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('LogDataDirectory', None)

    @property
    def log_backup_sp_details(self) -> dict:
        """Get the MySQL Server log backup storage policy details.

        Returns:
            dict: A dictionary containing information about the storage policy used for MySQL Server log backups.

        #ai-gen-doc
        """
        log_storage_policy_name = self._properties.get('mySqlInstance', {}).get(
            'logStoragePolicy', {}).get('storagePolicyName', None)
        log_storage_policy_id = self._properties.get('mySqlInstance', {}).get(
            'logStoragePolicy', {}).get('storagePolicyId', None)

        log_sp = {"storagePolicyName": log_storage_policy_name,
                  "storagePolicyId": log_storage_policy_id}
        return log_sp

    @property
    def command_line_sp_details(self) -> dict:
        """Get the MySQL Server command-line storage policy details.

        Returns:
            dict: A dictionary containing information about the MySQL server's command-line storage policy.

        #ai-gen-doc
        """
        cmd_storage_policy_name = self._properties.get('mySqlInstance', {}).get(
            'mysqlStorageDevice', {}).get('commandLineStoragePolicy', {}).get(
            'storagePolicyName', None)
        cmd_storage_policy_id = self._properties.get('mySqlInstance', {}).get(
            'mysqlStorageDevice', {}).get('commandLineStoragePolicy', {}).get(
            'storagePolicyId', None)

        command_sp = {"storagePolicyName": cmd_storage_policy_name,
                      "storagePolicyId": cmd_storage_policy_id}
        return command_sp

    @property
    def autodiscovery_enabled(self) -> bool:
        """Indicate whether MySQL Server auto discovery is enabled for this instance.

        Returns:
            True if auto discovery is enabled; False otherwise.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('EnableAutoDiscovery', False)

    @autodiscovery_enabled.setter
    def autodiscovery_enabled(self, value: bool) -> None:
        """Set the auto discovery attribute for the MYSQL instance.

        Args:
            value: Boolean value to enable (True) or disable (False) auto discovery.

        #ai-gen-doc
        """
        properties = self._properties
        update = {
            "EnableAutoDiscovery": value
        }
        properties['mySqlInstance'] = update
        self.update_properties(properties)

    @property
    def xtrabackup_bin_path(self) -> str:
        """Get the path to the MySQL server xtrabackup binary.

        Returns:
            The file system path to the xtrabackup binary used by the MySQL server.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('xtraBackupSettings', {}).get('xtraBackupBinPath', "")

    @property
    def is_xtrabackup_enabled(self) -> bool:
        """Check if xtrabackup is enabled for the MySQL Server instance.

        Returns:
            True if xtrabackup is enabled; False otherwise.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('xtraBackupSettings', {}).get('enableXtraBackup', False)

    @property
    def proxy_options(self) -> dict:
        """Get the MySQL Server proxy options for this instance.

        Returns:
            dict: A dictionary containing MySQL server proxy information, such as proxy host, port, and authentication details.

        #ai-gen-doc
        """
        proxy_settings = self._properties.get('mySqlInstance', {}).get('proxySettings', {})
        proxy_opt = {
            "isUseSSL": proxy_settings.get('isUseSSL', False),
            "isProxyEnabled": proxy_settings.get('isProxyEnabled', False),
            "runBackupOnProxy": proxy_settings.get('runBackupOnProxy', False),
            "instanceId": proxy_settings.get('proxyInstance', {}).get('instanceId', None),
            "instanceName": proxy_settings.get('proxyInstance', {}).get('instanceName', None),
            "clientId": proxy_settings.get('proxyInstance', {}).get('clientId', None),
            "clientName": proxy_settings.get('proxyInstance', {}).get('clientName', None)}
        return proxy_opt

    @property
    def mysql_enterprise_backup_binary_path(self) -> dict:
        """Get the MySQL Enterprise backup binary path details.

        Returns:
            dict: A dictionary containing details about the MySQL Enterprise backup binary path.

        #ai-gen-doc
        """
        meb_settings = self._properties.get('mySqlInstance', {}).get('mebSettings', {})
        return meb_settings

    @mysql_enterprise_backup_binary_path.setter
    def mysql_enterprise_backup_binary_path(self, value: str) -> None:
        """Set the MySQL Enterprise backup binary path for the instance.

        Args:
            value: The file system path to the MySQL Enterprise backup binary to be set for this MySQL instance.

        #ai-gen-doc
        """
        if not isinstance(value, str):
            raise SDKException('Instance', '101')
        properties = self._properties
        meb_bin_path_update = {
            "enableMEB": False if value == '' else True,
            "mebBinPath": value
        }
        properties['mySqlInstance']['mebSettings'] = meb_bin_path_update
        self.update_properties(properties)

    @property
    def no_lock_status(self) -> bool:
        """Get the status of the 'No Lock' checkbox in the MySQL instance.

        Returns:
            True if the 'No Lock' checkbox is enabled, False if it is disabled.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('EnableNoLocking', False)

    @no_lock_status.setter
    def no_lock_status(self, value: bool) -> None:
        """Set the No Lock property for the MySQL Instance.

        Args:
            value: Set to True to enable the No Lock property, or False to disable it.

        #ai-gen-doc
        """
        if not isinstance(value, bool):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['mySqlInstance']['EnableNoLocking'] = value
        self.update_properties(properties)

    @property
    def ssl_enabled(self) -> bool:
        """Check if SSL is enabled for the MySQL instance.

        Returns:
            True if SSL is enabled for the MySQL instance, False otherwise.

        #ai-gen-doc
        """
        return self._properties.get('mySqlInstance', {}).get('sslEnabled', False)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this MySQL instance.

        This method fetches the current configuration and properties for the MySQL instance
        associated with this object. It updates the instance's internal state with the latest
        information from the Commcell.

        Raises:
            SDKException: If the response from the Commcell is empty or indicates a failure.

        #ai-gen-doc
        """
        super(MYSQLInstance, self)._get_instance_properties()
        self._instance = {
            "type": 0,
            "clientName": self._agent_object._client_object.client_name,
            "clientSidePackage": True,
            "subclientName": "",
            "backupsetName": "defaultDummyBackupSet",
            "instanceName": self.instance_name,
            "appName": self._agent_object.agent_name,
            "consumeLicense": True
        }

    def _restore_json(self, **kwargs) -> dict:
        """Generate the JSON request payload for a restore operation based on user-selected options.

        This method constructs and returns a dictionary representing the JSON request
        to be sent to the API for a restore operation. The options for the restore
        are provided as keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing restore options and their values.

        Returns:
            dict: The JSON request dictionary to be passed to the API.

        #ai-gen-doc
        """
        rest_json = super(MYSQLInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        if restore_option["from_time"] is None:
            restore_option["from_time"] = {}

        if restore_option["to_time"] is None:
            restore_option["to_time"] = {}

        self._restore_admin_option_json(restore_option)
        self._restore_mysql_option_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "mySqlRstOption"] = self.mysql_restore_json
        rest_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"] = self.admin_option_json
        return rest_json

    def restore_in_place(
        self,
        path: Optional[list] = None,
        staging: Optional[str] = None,
        dest_client_name: Optional[str] = None,
        dest_instance_name: Optional[str] = None,
        data_restore: bool = True,
        log_restore: bool = False,
        overwrite: bool = True,
        copy_precedence: Optional[int] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        media_agent: Optional[str] = None,
        table_level_restore: bool = False,
        clone_env: bool = False,
        clone_options: Optional[dict] = None,
        redirect_enabled: bool = False,
        redirect_path: Optional[str] = None,
        browse_jobid: Optional[int] = None
    ) -> 'Job':
        """Restore MySQL data and/or log files to their original location (in-place restore).

        This method restores the specified MySQL databases or tables to the same location on the source or destination client.
        It supports options for data-only, log-only, or combined restores, as well as advanced features like table-level restore,
        cloning, and redirect restore.

        Args:
            path: List of databases or tables to restore. If None, restores all available.
            staging: Optional staging location for MySQL logs during restore.
            dest_client_name: Name of the destination client for the restore. If None, uses the source client.
            dest_instance_name: Name of the destination MySQL instance. If None, uses the source instance.
            data_restore: If True, performs data or data+log restore. Default is True.
            log_restore: If True, performs log or data+log restore. Default is False.
            overwrite: If True, unconditionally overwrites files during restore. Default is True.
            copy_precedence: Storage policy copy precedence value. If None, uses default.
            from_time: Restore data after this time (format: 'YYYY-MM-DD HH:MM:SS'). If None, restores from earliest.
            to_time: Restore data before this time (format: 'YYYY-MM-DD HH:MM:SS'). If None, restores up to latest.
            media_agent: Name of the media agent to use for the restore. If None, uses default.
            table_level_restore: If True, enables table-level restore. Default is False.
            clone_env: If True, clones the database environment. Default is False.
            clone_options: Dictionary of clone restore options. Example:
                {
                    "stagingLocaion": "/gk_snap",
                    "forceCleanup": True,
                    "port": "5595",
                    "libDirectory": "",
                    "isInstanceSelected": True,
                    "reservationPeriodS": 3600,
                    "user": "",
                    "binaryDirectory": "/usr/bin"
                }
            redirect_enabled: If True, enables redirect restore. Default is False.
            redirect_path: Path to use for redirect restore if enabled.
            browse_jobid: Job ID to browse and restore from. If None, uses latest available.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the path argument is not a list, if the job fails to initialize,
                if the response is empty, or if the restore operation is unsuccessful.

        #ai-gen-doc
        """
        if not (isinstance(path, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        if not path:
            raise SDKException('Instance', '104')

        if dest_client_name is None:
            dest_client_name = self._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = self.instance_name

        request_json = self._restore_json(
            paths=path,
            staging=staging,
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            data_restore=data_restore,
            log_restore=log_restore,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            media_agent=media_agent,
            table_level_restore=table_level_restore,
            clone_env=clone_env,
            clone_options=clone_options,
            redirect_enabled=redirect_enabled,
            redirect_path=redirect_path,
            browse_jobid=browse_jobid)

        return self._process_restore_response(request_json)

    def restore_out_of_place(
        self,
        path: Optional[list] = None,
        staging: Optional[str] = None,
        dest_client_name: Optional[str] = None,
        dest_instance_name: Optional[str] = None,
        data_restore: bool = True,
        log_restore: bool = False,
        overwrite: bool = True,
        copy_precedence: Optional[int] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        media_agent: Optional[str] = None,
        table_level_restore: bool = False,
        clone_env: bool = False,
        clone_options: Optional[dict] = None,
        redirect_enabled: bool = False,
        redirect_path: Optional[str] = None,
        browse_jobid: Optional[int] = None,
        recurringRestore: bool = False
    ) -> 'Job':
        """Perform an out-of-place restore of MySQL data, logs, or recurring files to a specified destination client and instance.

        This method allows you to restore MySQL databases or tables to a different client or instance, with options for data/log restore, table-level restore, cloning, and advanced restore settings.

        Args:
            path: List of database or table names to be restored. If None, restores all available.
            staging: Staging location for MySQL logs during restore operations.
            dest_client_name: Name of the destination client where the data will be restored.
            dest_instance_name: Name of the destination MySQL instance on the destination client.
            data_restore: If True, performs data or data+log restore. Defaults to True.
            log_restore: If True, performs log or data+log restore. Defaults to False.
            overwrite: If True, existing files at the destination will be overwritten. Defaults to True.
            copy_precedence: Storage policy copy precedence value to use for restore.
            from_time: Restore data backed up after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Restore data backed up before this time (format: 'YYYY-MM-DD HH:MM:SS').
            media_agent: Name of the MediaAgent to use for the restore.
            table_level_restore: If True, enables table-level restore. Defaults to False.
            clone_env: If True, clones the database environment. Defaults to False.
            clone_options: Dictionary of additional clone restore options.
            redirect_enabled: If True, enables redirect restore. Defaults to False.
            redirect_path: Path to redirect the restore to, used with redirect_enabled.
            browse_jobid: Job ID to browse and restore from a specific backup job.
            recurringRestore: If True, enables recurring restore. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the path is not a list, if job initialization fails, if destination client or instance name is empty, or if the restore response is empty or unsuccessful.

        #ai-gen-doc
        """
        if not (isinstance(path, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        if not path:
            raise SDKException('Instance', '104')

        if dest_client_name is None:
            raise SDKException('Client', '102',
                               "The destination client name is missing. "
                               "Please provide a valid destination client name to proceed")

        if dest_instance_name is None:
            raise SDKException('Instance', '102',
                               "The destination Instance name is missing. "
                               "Please provide a valid destination Instance name to proceed")

        request_json = self._restore_json(
            paths=path,
            staging=staging,
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            data_restore=data_restore,
            log_restore=log_restore,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            media_agent=media_agent,
            table_level_restore=table_level_restore,
            clone_env=clone_env,
            clone_options=clone_options,
            redirect_enabled=redirect_enabled,
            redirect_path=redirect_path,
            browse_jobid=browse_jobid,
            recurringRestore=recurringRestore)

        return self._process_restore_response(request_json)

    def _restore_browse_option_json(self, value: dict) -> None:
        """Set the browse options for restore operations in JSON format.

        Args:
            value: A dictionary containing the browse options to be used during restore.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        super(MYSQLInstance, self)._restore_browse_option_json(value)

        self._browse_restore_json['backupset'] = {
            "clientName": self._agent_object._client_object.client_name,
            "backupsetName": "defaultDummyBackupSet"
        }

        if value.get("browse_jobid"):
            self._browse_restore_json['browseJobId'] = value.get("browse_jobid")

        if value.get("from_time") and value.get("to_time"):
            self._browse_restore_json["timeRange"] = {
                "fromTime": value.get("from_time"),
                "toTime": value.get("to_time")
            }

    def _restore_common_options_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing the common options to be set in the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._commonoption_restore_json = {
            "restoreToDisk": False,
            "onePassRestore": False,
            "revert": False,
            "syncRestore": False
        }

    def _restore_destination_json(self, value: dict) -> None:
        """Set the MySQL destination options in the restore JSON configuration.

        Args:
            value: A dictionary containing the MySQL destination options to be set in the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = {
            "destinationInstance": {
                "clientName": value.get("dest_client_name", ""),
                "instanceName": value.get("dest_instance_name", ""),
                "appName": "MySQL"
            },
            "destClient": {
                "clientName": value.get("dest_client_name", "")
            }
        }

    def _restore_fileoption_json(self, value: dict) -> None:
        """Set the file option for the restore operation in the restore JSON.

        Args:
            value: A dictionary containing file option settings to be applied to the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._fileoption_restore_json = {
            "sourceItem": value.get("paths", [])
        }

    def _restore_admin_option_json(self, value: dict) -> None:
        """Set the admin restore option in the restore JSON configuration.

        Args:
            value: A dictionary containing the admin restore options to be set in the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.admin_option_json = {
            "contentIndexingOption": {
                "subClientBasedAnalytics": False
            }
        }

    def _restore_mysql_option_json(self, value: dict) -> None:
        """Set the MySQL restore options in the restore JSON configuration.

        Args:
            value: A dictionary containing MySQL restore options to be set in the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.mysql_restore_json = {
            "destinationFolder": "",
            "data": value.get("data_restore", True),
            "log": value.get("log_restore", True),
            "recurringRestore": value.get("recurringRestore", False),
            "temporaryStagingLocation": value.get("staging", ""),
            "dataStagingLocation": "",
            "logRestoreType": 0,
            "tableLevelRestore": value.get("table_level_restore", False),
            "pointofTime": True if value.get("to_time") else False,
            "instanceRestore": True,
            "isCloneRestore": value.get("clone_env", False),
            "fromTime": value.get("from_time", {}),
            "refTime": value.get("to_time", {}),
            "destinationServer": {
                "name": ""
            }
        }
        if value.get("table_level_restore"):
            self.mysql_restore_json['dropTable'] = True
            self.mysql_restore_json['instanceRestore'] = False

        if value.get("clone_env", False):
            self.mysql_restore_json["cloneOptions"] = value.get("clone_options", "")

        if value.get("redirect_path"):
            self.mysql_restore_json["redirectEnabled"] = True
            self.mysql_restore_json["redirectItems"] = [value.get("redirect_path")]

        if value.get("from_time"):
            self.mysql_restore_json["fromTime"] = {"time": value.get("to_time")}

        if value.get("to_time"):
            self.mysql_restore_json["refTime"] = {"time": value.get("to_time")}

        if value.get("to_time"):
            self.mysql_restore_json["pointInTime"] = {"time": value.get("to_time")}

        if value.get("dest_instance_name"):
            self.mysql_restore_json["destinationServer"] = {"name": value.get("dest_instance_name")}
