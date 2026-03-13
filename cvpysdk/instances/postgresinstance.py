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

"""File for operating on a POSTGRESQL Instance.

PostgreSQLInstance is the only class defined in this file.

PostgreSQLInstance: Derived class from Instance Base class, representing a postgres server instance,
                       and to perform operations on that instance

PostgreSQLInstance:
===================

    _get_instance_properties()           --     Gets the properties of this instance

    _get_instance_properties_json()      --     Gets all the instance related properties of
    PostgreSQL instance.

    _restore_json()                      --     returns the JSON request to pass to the API as per
    the options selected by the user

    _restore_common_options_json()       --     setter for the common options in restore JSON

    _restore_destination_json()          --     setter for the Destination options in restore JSON

    _restore_postgres_option_json()      --     setter for the postgres restore option
    in restore JSONRe

    restore_in_place()                   --     Restores the postgres data/log files
    specified in the input paths list to the same location

    change_sa_password()                 --     Changes postgresql user password

PostgreSQLInstance instance Attributes
======================================

    **postgres_bin_directory**           --  returns the postgres bin directory of postgres server

    **postgres_lib_directory**           --  returns the lib directory of postgres server

    **postgres_archive_log_directory**   --  returns the postgres archive log directory
    of postgres server

    **log_storage_policy**               --  returns the log storage policy for the instance

    **postgres_server_user_name**        --  returns the postgres server user name
    of postgres server

    **postgres_server_port_number**      --  returns the postgres server port number
    of postgres server

    **maintenance_database**             --  returns the maintenance database associated
    with postgres server

    **postgres_version**                 --  returns the postgres server version

    **standby_instance_name**            --  Returns the standby instance name

    **standby_instance_id**              --  Returns the standby instance id

    **use_master_for_log_backup**        --  Returns True if master is used for log backup

    **use_master_for_data_backup**       --  Returns True if master is used for data backup

    **archive_delete**                   --  Returns True if archive delete is enabled for instance

    **postgres_ssl_status**              --  Returns True/False based on if ssl is enabled or not

    **postgres_ssl_ca_file**             --  Returns SSL CA file path

    **postgres_ssl_key_file**            --  Returns SSL key file path

    **postgres_ssl_cert_file**           --  Returns SSL cert file path

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode

from ..instance import Instance
from ..exception import SDKException
from ..job import Job

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class PostgreSQLInstance(Instance):
    """
    Represents a PostgreSQL database instance, extending the base Instance class.

    This class provides comprehensive management and operational capabilities for
    PostgreSQL instances, including configuration, backup, restore, and security
    operations. It exposes properties for accessing and modifying key PostgreSQL
    instance attributes such as binary and library directories, archive log
    directories, server user and port information, SSL configuration, standby
    settings, and storage policies.

    Additionally, the class offers methods for retrieving and manipulating
    instance properties, handling restore operations with various options, and
    managing security aspects like changing the superuser password.

    Key Features:
        - Access to PostgreSQL binary, library, and archive log directories
        - Management of log storage policies
        - Retrieval and configuration of server user, port, and maintenance database
        - PostgreSQL version and SSL configuration management
        - Standby instance support and status checks
        - Control over log and data backup sources (master/standby)
        - Archive log deletion management
        - Secure password change for the superuser account
        - Retrieval of instance properties in both object and JSON formats
        - Flexible restore operations, including in-place and advanced options

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int) -> None:
        """Initialize a PostgreSQLInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this PostgreSQL instance.
            instance_name: The name of the PostgreSQL instance.
            instance_id: The unique identifier for the PostgreSQL instance.

        #ai-gen-doc
        """
        super(
            PostgreSQLInstance,
            self).__init__(
            agent_object,
            instance_name,
            instance_id)
        self.backup_object = None
        self.backupset_object = None
        self.sub_client_object = None
        self.postgres_restore_json = None
        self._postgres_restore_options = None
        self._destination_restore_json = None

    @property
    def postgres_bin_directory(self) -> str:
        """Get the bin directory path of the PostgreSQL server.

        Returns:
            The absolute path to the PostgreSQL server's bin directory as a string.

        #ai-gen-doc
        """
        if self._properties['postGreSQLInstance']['BinaryDirectory']:
            return self._properties['postGreSQLInstance']['BinaryDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Binary directory.")

    @property
    def postgres_lib_directory(self) -> str:
        """Get the library directory path of the PostgreSQL server.

        Returns:
            The absolute path to the PostgreSQL server's library (lib) directory as a string.

        #ai-gen-doc
        """
        if self._properties['postGreSQLInstance']['LibDirectory']:
            return self._properties['postGreSQLInstance']['LibDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Lib directory.")

    @property
    def postgres_archive_log_directory(self) -> str:
        """Get the archive log directory path of the PostgreSQL server.

        Returns:
            The file system path to the PostgreSQL server's archive log directory as a string.

        #ai-gen-doc
        """
        if self._properties['postGreSQLInstance']['ArchiveLogDirectory']:
            return self._properties['postGreSQLInstance']['ArchiveLogDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Archive log directory.")

    @property
    def log_storage_policy(self) -> Optional[str]:
        """Get the log storage policy associated with this PostgreSQL instance.

        Returns:
            The name of the log storage policy as a string, or None if no policy is set.

        #ai-gen-doc
        """
        return self._properties.get('postGreSQLInstance', {}).get('logStoragePolicy', {}).get('storagePolicyName', None)

    @log_storage_policy.setter
    def log_storage_policy(self, value: str) -> None:
        """Set the log storage policy for the PostgreSQL instance.

        Args:
            value: The name of the storage policy to assign for log backups.

        #ai-gen-doc
        """
        if not isinstance(value, str):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['logStoragePolicy'] = {}
        properties['postGreSQLInstance']['logStoragePolicy']['storagePolicyName'] = value
        self.update_properties(properties)

    @property
    def postgres_server_user_name(self) -> str:
        """Get the username of the PostgreSQL server.

        Returns:
            The username used to connect to the PostgreSQL server as a string.

        #ai-gen-doc
        """
        if self.credentials:
            return self._commcell_object.credentials.get(self.credentials)._credential_properties.get("userName")
        else:
            if self._properties['postGreSQLInstance']['SAUser']['userName']:
                return self._properties['postGreSQLInstance']['SAUser']['userName']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Server name.")

    @property
    def postgres_server_port_number(self) -> str:
        """Get the port number associated with the PostgreSQL server.

        Returns:
            The port number used by the PostgreSQL server as a string.

        #ai-gen-doc
        """
        if self._properties['postGreSQLInstance']['port']:
            return self._properties['postGreSQLInstance']['port']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the port Number.")

    @property
    def maintenance_database(self) -> str:
        """Get the maintenance database associated with the PostgreSQL server.

        Returns:
            The name of the maintenance database as a string.

        #ai-gen-doc
        """
        if self._properties['postGreSQLInstance'].get('MaintainenceDB'):
            return self._properties['postGreSQLInstance']['MaintainenceDB']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch maintenance database.")

    @property
    def postgres_version(self) -> str:
        """Get the PostgreSQL server version for this instance.

        Returns:
            The version of the PostgreSQL server as a string.

        #ai-gen-doc
        """
        if self._properties.get('version'):
            return self._properties['version']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch postgres version.")

    @property
    def archive_delete(self) -> bool:
        """Check if archive delete is enabled for the PostgreSQL instance.

        Returns:
            True if archive delete is enabled; False otherwise.

        #ai-gen-doc
        """
        return self._properties.get('postGreSQLInstance', {}).get('ArchiveDelete', False)

    @archive_delete.setter
    def archive_delete(self, value: bool) -> None:
        """Set the archive delete property for the PostgreSQL instance.

        This setter enables or disables the archive delete feature for the instance.

        Args:
            value: Set to True to enable archive delete, or False to disable it.

        #ai-gen-doc
        """
        if not isinstance(value, bool):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['ArchiveDelete'] = value
        self.update_properties(properties)

    @property
    def standby_instance_name(self) -> Optional[str]:
        """Get the name of the standby PostgreSQL instance.

        Returns:
            The name of the standby instance as a string.

        #ai-gen-doc
        """
        if self.is_standby_enabled:
            return self._properties.get('postGreSQLInstance', {}).get(
                'standbyOptions', {}).get('standbyInstance', {}).get('instanceName', "")

        return None

    @property
    def standby_instance_id(self) -> Optional[str]:
        """Get the standby instance ID for the PostgreSQL instance.

        Returns:
            The standby instance ID as a string.

        #ai-gen-doc
        """
        if self.is_standby_enabled:
            return self._properties.get('postGreSQLInstance', {}).get(
                'standbyOptions', {}).get('standbyInstance', {}).get('instanceId', "")

        return None

    @property
    def is_standby_enabled(self) -> bool:
        """Check if standby mode is enabled for the PostgreSQL instance.

        Returns:
            True if standby mode is enabled; False otherwise.

        #ai-gen-doc
        """
        return self._properties.get('postGreSQLInstance', {}).get('standbyOptions', {}).get('isStandbyEnabled', False)

    @property
    def use_master_for_log_backup(self) -> bool:
        """Indicate whether the master database is used for log backup operations.

        Returns:
            True if the master database is configured to be used for log backup; False otherwise.

        #ai-gen-doc
        """
        return self._properties.get('postGreSQLInstance', {}).get('standbyOptions', {}).get('useMasterForLogBkp', False)

    @use_master_for_log_backup.setter
    def use_master_for_log_backup(self, value: bool) -> None:
        """Set whether to use the master server for log backup in standby mode.

        Args:
            value: Set to True to enable using the master server for log backup; False to disable.

        #ai-gen-doc
        """
        if not isinstance(value, bool):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['standbyOptions']['useMasterForLogBkp'] = value
        self.update_properties(properties)

    @property
    def use_master_for_data_backup(self) -> bool:
        """Indicate whether the master server is used for data backup.

        Returns:
            True if the master server is configured to be used for data backup; otherwise, False.

        #ai-gen-doc
        """
        return self._properties.get('postGreSQLInstance', {}).get(
            'standbyOptions', {}).get('useMasterForDataBkp', False)

    @use_master_for_data_backup.setter
    def use_master_for_data_backup(self, value: bool) -> None:
        """Set the property to use the master server for data backup in a PostgreSQL standby configuration.

        Args:
            value: Set to True to enable using the master server for data backup; set to False to disable.

        #ai-gen-doc
        """
        if not isinstance(value, bool):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['standbyOptions']['useMasterForDataBkp'] = value
        self.update_properties(properties)

    @property
    def postgres_ssl_status(self) -> bool:
        """Check whether SSL is enabled for the PostgreSQL instance.

        Returns:
            True if SSL is enabled for the PostgreSQL instance, False otherwise.

        #ai-gen-doc
        """
        return self._properties.get("postGreSQLInstance", {}).get("sslOpt", {}).get("sslEnabled", False)

    @property
    def postgres_ssl_ca_file(self) -> str:
        """Get the file path to the SSL CA certificate used by the PostgreSQL instance.

        Returns:
            The file path to the SSL CA (Certificate Authority) file as a string.

        #ai-gen-doc
        """
        return self._properties.get("postGreSQLInstance", {}).get("sslOpt", {}).get("sslCa", "")

    @property
    def postgres_ssl_key_file(self) -> str:
        """Get the file path to the PostgreSQL SSL key file.

        Returns:
            The full path to the SSL key file used by the PostgreSQL instance.

        #ai-gen-doc
        """
        return self._properties.get("postGreSQLInstance", {}).get("sslOpt", {}).get("sslKey", "")

    @property
    def postgres_ssl_cert_file(self) -> str:
        """Get the file path to the PostgreSQL SSL certificate.

        Returns:
            The file system path to the SSL certificate used by the PostgreSQL instance.

        #ai-gen-doc
        """
        return self._properties.get("postGreSQLInstance", {}).get("sslOpt", {}).get("sslCert", "")

    def change_sa_password(self, value: str) -> None:
        """Change the password for the PostgreSQL user (SA user).

        Args:
            value: The new password to set for the PostgreSQL user.

        #ai-gen-doc
        """
        if not isinstance(value, str):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['SAUser']['password'] = b64encode(value.encode()).decode()
        self.update_properties(properties)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this PostgreSQL instance.

        This method fetches the latest properties for the PostgreSQL instance from the Commcell
        and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response from the Commcell is empty or indicates a failure.

        #ai-gen-doc
        """
        super(PostgreSQLInstance, self)._get_instance_properties()
        self._postgresql_instance = self._properties['postGreSQLInstance']

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all properties related to the PostgreSQL instance as a dictionary.

        Returns:
            dict: A dictionary containing all instance properties for the PostgreSQL instance.

        #ai-gen-doc
        """
        instance_json = {
            "instanceProperties":
                {
                    "instance": self._instance,
                    "postGreSQLInstance": self._postgresql_instance
                }
        }
        return instance_json

    def _restore_json(self, **kwargs) -> dict:
        """Generate the JSON request payload for a restore operation based on user-selected options.

        This method constructs a dictionary representing the JSON request to be sent to the API,
        using the provided keyword arguments to specify restore options.

        Args:
            **kwargs: Arbitrary keyword arguments representing restore options. Each key-value pair
                corresponds to a specific restore parameter required by the API.

        Returns:
            dict: The JSON request dictionary to be passed to the API for the restore operation.

        #ai-gen-doc
        """
        rest_json = super(PostgreSQLInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        self._restore_postgres_option_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["postgresRstOption"] = self.postgres_restore_json
        return rest_json

    def _restore_common_options_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing the common options to be set in the restore JSON.

        #ai-gen-doc
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')
        super(PostgreSQLInstance, self)._restore_common_options_json(value)
        if value.get("baseline_jobid"):
            self._commonoption_restore_json = {
                "clusterDBBackedup": False,
                "restoreToDisk": False,
                "baselineBackup": 1,
                "baselineRefTime": value.get("baseline_ref_time", ""),
                "baselineJobId": value.get("baseline_jobid", ""),
                "copyToObjectStore": False,
                "onePassRestore": False,
                "syncRestore": value.get("sync_restore", True)
            }

    def _restore_destination_json(self, value: dict) -> None:
        """Set the destination options in the restore JSON configuration.

        This method updates the restore JSON with the specified destination options.

        Args:
            value: Dictionary containing the destination options to be set for the restore operation.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        if value.get("restore_to_disk"):
            return super(PostgreSQLInstance, self)._restore_destination_json(value)

        else:
            self._destination_restore_json = {
                "destinationInstance": {
                    "clientName": value.get("dest_client_name", ""),
                    "instanceName": value.get("dest_instance_name", ""),
                    "appName": self._agent_object.agent_name
                },
                "destClient": {
                    "clientName": value.get("dest_client_name", "")
                }
            }

    def _restore_postgres_option_json(self, value: dict) -> None:
        """Set the restore options in the PostgreSQL restore JSON.

        Args:
            value: Dictionary containing the options to be set for the restore operation.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.postgres_restore_json = self._postgres_restore_options = {
            "restoreToSameServer": False,
            "tableLevelRestore": value.get("table_level_restore", False),
            "instanceRestore": False,
            "fsBackupSetRestore": value.get("backupset_flag", ""),
            "isCloneRestore": value.get("clone_env", False),
            "refTime": {}
        }

        if value.get("clone_env", False):
            self.postgres_restore_json["cloneOptions"] = value.get("clone_options", "")

        if value.get("to_time"):
            time_value = {"timevalue": value.get("to_time", "")}
            self.postgres_restore_json["refTime"] = time_value
            self.postgres_restore_json["fromTime"] = time_value
            self.postgres_restore_json["pointOfTime"] = time_value

        if value.get("table_level_restore"):
            self.postgres_restore_json["stagingPath"] = value.get("staging_path", "")
            self.postgres_restore_json["auxilaryMap"] = []
            database_list = []
            for table_path in value.get("paths"):
                database_list.append(table_path.split('/')[1])
            database_list = set(database_list)
            for database_name in database_list:
                self.postgres_restore_json["auxilaryMap"].append({"sourceDB": database_name})

        if value.get("redirect_path"):
            self.postgres_restore_json["redirectEnabled"] = True
            self.postgres_restore_json["redirectItems"] = [value.get("redirect_path")]

        if value.get("restore_to_disk"):
            self.postgres_restore_json["fsBackupSetRestore"] = False

    def restore_in_place(
        self,
        path: list,
        dest_client_name: str,
        dest_instance_name: str,
        backupset_name: str,
        backupset_flag: bool,
        overwrite: bool = True,
        copy_precedence: int = None,
        from_time: str = None,
        to_time: str = None,
        clone_env: bool = False,
        clone_options: dict = None,
        media_agent: str = None,
        table_level_restore: bool = False,
        staging_path: str = None,
        no_of_streams: int = None,
        volume_level_restore: bool = False,
        redirect_enabled: bool = False,
        redirect_path: str = None,
        restore_to_disk: bool = False,
        restore_to_disk_job: int = None,
        destination_path: str = None,
        revert: bool = False
    ) -> 'Job':
        """Restore PostgreSQL data or log files in place to their original location.

        This method restores the specified PostgreSQL databases or files to the same location on the destination client and instance.
        It supports various restore options such as cloning, table-level restore, volume-level restore, redirect restore, and restore to disk.

        Args:
            path: List of database names or file paths to be restored.
            dest_client_name: Name of the destination client where the data will be restored.
            dest_instance_name: Name of the destination PostgreSQL instance.
            backupset_name: Name of the backupset to restore from.
            backupset_flag: Flag indicating if the backup is file system-based.
            overwrite: If True, files will be unconditionally overwritten during restore. Default is True.
            copy_precedence: Copy precedence value of the storage policy copy. Default is None.
            from_time: Restore data backed up after this time (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Restore data backed up before this time (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            clone_env: If True, the database will be cloned. Default is False.
            clone_options: Dictionary of clone restore options. Example:
                {
                    "stagingLocaion": "/gk_snap",
                    "forceCleanup": True,
                    "port": "5595",
                    "libDirectory": "/opt/PostgreSQL/9.6/lib",
                    "isInstanceSelected": True,
                    "reservationPeriodS": 3600,
                    "user": "postgres",
                    "binaryDirectory": "/opt/PostgreSQL/9.6/bin"
                }
                Default is None.
            media_agent: Name of the media agent to use for the restore. Default is None.
            table_level_restore: If True, perform a table-level restore. Default is False.
            staging_path: Staging path location for table-level restore. Default is None.
            no_of_streams: Number of streams to use for volume-level restore. Default is None.
            volume_level_restore: If True, perform a volume-level restore. Default is False.
            redirect_enabled: If True, enable redirect restore. Default is False.
            redirect_path: Path to redirect the restore to. Default is None.
            restore_to_disk: If True, restore to disk instead of the original location. Default is False.
            restore_to_disk_job: Backup job ID to restore to disk. Default is None.
            destination_path: Destination path for the restore. Default is None.
            revert: If True, perform a hardware revert during restore. Default is False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the path is not a list, if the job fails to initialize, if the response is empty, or if the response is not successful.

        #ai-gen-doc
        """
        if not (isinstance(path, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        if not path:
            raise SDKException('Instance', '104')

        if not no_of_streams:
            no_of_streams = 1

        index_free_restore = False
        if restore_to_disk:
            index_free_restore = True

        request_json = self._restore_json(
            paths=path,
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            backupset_name=backupset_name,
            backupset_flag=backupset_flag,
            copy_precedence=copy_precedence,
            overwrite=overwrite,
            from_time=from_time,
            to_time=to_time,
            clone_env=clone_env,
            clone_options=clone_options,
            media_agent=media_agent,
            table_level_restore=table_level_restore,
            staging_path=staging_path,
            no_of_streams=no_of_streams,
            volume_level_restore=volume_level_restore,
            redirect_enabled=redirect_enabled,
            redirect_path=redirect_path,
            restore_to_disk=restore_to_disk,
            index_free_restore=index_free_restore,
            destination_path=destination_path,
            restore_jobs=restore_to_disk_job)

        if volume_level_restore:
            request_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['destination']["noOfStreams"] = no_of_streams

        if restore_to_disk:
            request_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['destination']["destPath"] = [destination_path]

        if revert:
            request_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['commonOptions']["revert"] = revert
        return self._process_restore_response(request_json)
