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

"""File for operating on a DB2 Instance.

DB2Instance is the only class defined in this file.

DB2Instance:    Derived class from Instance Base class, representing a
DB2 instance, and to perform operations on that instance

DB2Instance:
============

    _restore_destination_json()     --      setter for the Db2 Destination options in restore JSON

    _db2_restore_options_json()     --      setter for  the db2 options of in restore JSON

    _restore_json()                 --      returns the JSON request to pass to the API as per
    the options selected by the user

    restore_entire_database()       --      Restores the db2 database

    restore_out_of_place()          --      runs the out of place restore for given backupset

    restore_table_level()           --      Table level restore function


DB2Instance instance Attributes:
================================
    **version**                         -- returns db2 version

    **home_directory**                  -- returns db2 home directory

    **user_name**                       -- returns db2 user name

    **data_backup_storage_policy**      -- returns data backup storage policy

    **command_line_storage_policy**     -- returns commandline storage policy

    **log_backup_storage_policy**       -- returns log backup storage policy

"""

from __future__ import unicode_literals
from base64 import b64encode

from ..exception import SDKException
from ..instance import Instance
from ..job import Job


class DB2Instance(Instance):
    """
    Represents a DB2 database instance, extending the base Instance class to provide
    specialized operations and properties for DB2 environments.

    This class offers access to key DB2 instance attributes such as version, home directory,
    username, and various storage policies. It also provides methods for performing
    comprehensive restore operations, including entire database restores, out-of-place restores,
    and table-level restores with advanced configuration options.

    Key Features:
        - Access DB2 instance properties: version, home directory, user name
        - Manage storage policies for data backup, command line, and log backup
        - Generate and handle restore destination and DB2 restore options in JSON format
        - Restore entire DB2 databases to specified destinations
        - Perform out-of-place restores to alternate locations or backup sets
        - Execute table-level restores with support for staging and table paths, and authentication

    #ai-gen-doc
    """

    @property
    def version(self) -> str:
        """Get the DB2 version associated with this instance.

        Returns:
            The DB2 version as a string.

        #ai-gen-doc
        """
        return self._properties.get('version', '')

    @property
    def home_directory(self) -> str:
        """Get the DB2 home directory path for this instance.

        Returns:
            The path to the DB2 home directory as a string.

        #ai-gen-doc
        """
        return self._properties.get('db2Instance', {}).get('homeDirectory', '')

    @property
    def user_name(self) -> str:
        """Get the DB2 username associated with this instance.

        Returns:
            The DB2 username as a string.

        #ai-gen-doc
        """
        return self._properties.get('db2Instance', {}).get('userAccount', {}).get('userName', '')

    @property
    def data_backup_storage_policy(self) -> str:
        """Get the data backup storage policy name configured at the DB2 instance level.

        Returns:
            The name of the storage policy assigned to the DB2 instance for data backups.

        #ai-gen-doc
        """
        return self._properties.get('db2Instance', {}).get(
            'DB2StorageDevice', {}).get('dataBackupStoragePolicy', {}).get('storagePolicyName', '')

    @property
    def command_line_storage_policy(self) -> str:
        """Get the command line storage policy name configured at the DB2 instance level.

        Returns:
            The name of the command line storage policy as a string.

        #ai-gen-doc
        """
        return self._properties.get('db2Instance', {}).get(
            'DB2StorageDevice', {}).get('commandLineStoragePolicy', {}).get('storagePolicyName', "")

    @property
    def log_backup_storage_policy(self) -> str:
        """Get the name of the log backup storage policy at the instance level.

        Returns:
            The name of the log backup storage policy as a string.

        #ai-gen-doc
        """
        return self._properties.get('db2Instance', {}).get(
            'DB2StorageDevice', {}).get('logBackupStoragePolicy', {}).get('storagePolicyName', "")

    def _restore_destination_json(self, value: dict) -> None:
        """Set the DB2 destination options in the restore JSON configuration.

        This method updates the restore JSON with the specified DB2 destination options.

        Args:
            value: A dictionary containing the DB2 destination options to be set in the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = {
            "destinationInstance": {
                "clientName": value.get("dest_client_name", ""),
                "instanceName": value.get("dest_instance_name", ""),
                "backupsetName": value.get("dest_backupset_name", ""),
                "appName": "DB2"
            },
            "destClient": {
                "clientName": value.get("dest_client_name", "")
            }
        }

    def _db2_restore_options_json(self, value: dict) -> dict:
        """Set the DB2 options in the restore JSON configuration.

        Args:
            value: A dictionary containing the DB2 restore options to be set.

        Returns:
            dict: The DB2 restore options dictionary

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.db2_options_restore_json = {
            "restoreType": value.get("restore_type", 0),
            "restoreLevel": value.get("restore_level", 0),
            "redirect": value.get("redirect", False),
            "rollForwardPending": value.get("rollforward_pending", False),
            "restoreArchiveLogs": value.get("restore_archive_logs", True),
            "rollForward": value.get("roll_forward", True),
            "restoreIncremental": value.get("restore_incremental", False),
            "archiveLogLSN": value.get("archivelog_lsn", False),
            "archiveLogTime": value.get("archive_log_time", False),
            "startLSN": value.get("start_lsn", False),
            "endLSN": value.get("end_lsn", False),
            "logTimeStart": value.get("logtime_start", False),
            "logTimeEnd": value.get("logtime_end", False),
            "rollForwardToEnd": value.get("roll_forward_to_end", 1),
            "useAlternateLogFile": value.get("use_alternate_logfile", False),
            "restoreData": value.get("restore_data", True),
            "restoreOnline": value.get("restore_online", False),
            "targetDb": value.get("target_db", " "),
            "targetPath": value.get("target_path", " "),
            "reportFile": value.get("report_file", " "),
            "buffers": value.get("buffers", 2),
            "bufferSize": value.get("buffer_size", 1024),
            "rollForwardDir": value.get("roll_forward_dir", " "),
            "recoverDb": value.get("recover_db", False),
            "dbHistoryFilepath": value.get("db_history_filepath", False),
            "storagePath": value.get("storage_path", False),
            "parallelism": value.get("parallelism", 0),
            "useSnapRestore": value.get("use_snap_restore", False),
            "useLatestImage": value.get("use_latest_image", True),
            "tableViewRestore": value.get("table_view_restore", False),
            "useLogTarget": value.get("use_log_target", False),
            "cloneRecovery": value.get("clone_recovery", False)
        }

        if value.get("archive_log_time", False):
            self.db2_options_restore_json["logTimeRange"] = dict()
            self.db2_options_restore_json["logTimeRange"]["fromTimeValue"] = value.get("from_time_value", 0)
            self.db2_options_restore_json["logTimeRange"]["toTimeValue"] = value.get("to_time_value", 0)

        if value.get("archivelog_lsn", False):
            self.db2_options_restore_json["startLSNNum"] = value.get("start_lsn_num", 1)
            self.db2_options_restore_json["endLSNNum"] = value.get("end_lsn_num", 1)

        return self.db2_options_restore_json

    def _restore_json(self, **kwargs) -> dict:
        """Generate the JSON request payload for a restore operation based on user-selected options.

        This method constructs and returns a dictionary representing the JSON request body
        required by the API for performing a restore, using the options provided as keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing restore options and their values.

        Returns:
            dict: The JSON request dictionary to be sent to the API for the restore operation.

        #ai-gen-doc
        """

        rest_json = super(DB2Instance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option = kwargs

        json = self._db2_restore_options_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"] = json

        return rest_json

    def restore_entire_database(
        self,
        dest_client_name: str,
        dest_instance_name: str,
        dest_database_name: str,
        **kwargs
    ) -> 'Job':
        """Restore the entire DB2 database to a specified destination.

        This method initiates a restore operation for a DB2 database, allowing you to specify
        the destination client, instance, and database name. Additional restore options can be
        provided as keyword arguments.

        Args:
            dest_client_name: The name of the destination client where the database will be restored.
            dest_instance_name: The name of the destination DB2 instance on the destination client.
            dest_database_name: The name of the destination database to restore to.
            **kwargs: Optional keyword arguments to customize the restore operation, such as:
                - restore_type (str): Type of DB2 restore. Default is "ENTIREDB".
                - recover_db (bool): Whether to recover the database after restore. Default is True.
                - restore_incremental (bool): Whether to restore incremental backups. Default is True.
                - restore_data (bool): Whether to restore data. Default is True.
                - copy_precedence (int): Copy precedence to use for restore. Default is None.
                - roll_forward (bool): Whether to roll forward the database after restore. Default is True.
                - restore_logs (bool): Whether to restore logs. Default is True.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the job initialization fails, the response is empty, or the response is not successful.

        Example:
            >>> db2_instance = DB2Instance()
            >>> job = db2_instance.restore_entire_database(
            ...     dest_client_name="db2_client",
            ...     dest_instance_name="db2_instance",
            ...     dest_database_name="restored_db",
            ...     restore_type="ENTIREDB",
            ...     recover_db=True,
            ...     restore_incremental=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        recover_db = kwargs.get("recover_db", True)
        restore_incremental = kwargs.get("restore_incremental", True)
        restore_data = kwargs.get("restore_data", True)
        copy_precedence = kwargs.get("copy_precedence", None)
        roll_forward = kwargs.get("roll_forward", True)
        restore_logs = kwargs.get("restore_logs", True)
        restore_type = kwargs.get("restore_type", 'ENTIREDB')
        start_lsn_num = kwargs.get("startLSNNum", 1)
        end_lsn_num = kwargs.get("endLSNNum", 1)
        end_lsn = kwargs.get("endLSN", False)
        start_lsn = kwargs.get("startLSN", False)
        archivelog_lsn = kwargs.get("archiveLogLSN", False)
        archive_log_time = kwargs.get("archiveLogTime", False)
        logtime_start = kwargs.get("logTimeStart", False)
        logtime_end = kwargs.get("logTimeEnd", False)
        from_time_value = kwargs.get("fromTimeValue", 0)
        to_time_value = kwargs.get("toTimeValue", 0)

        if "entiredb" in restore_type.lower():
            restore_type = 0

        request_json = self._restore_json(
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            dest_backupset_name=dest_database_name,
            target_db=dest_database_name,
            restore_type=restore_type,
            recover_db=recover_db,
            restore_incremental=restore_incremental,
            restore_data=restore_data,
            copy_precedence=copy_precedence,
            roll_forward=roll_forward,
            rollforward_pending=not roll_forward,
            restore_archive_logs=restore_logs,
            start_lsn_num=start_lsn_num,
            end_lsn_num=end_lsn_num,
            archivelog_lsn=archivelog_lsn,
            start_lsn=start_lsn,
            end_lsn=end_lsn,
            archive_log_time=archive_log_time,
            logtime_start=logtime_start,
            logtime_end=logtime_end,
            from_time_value=from_time_value,
            to_time_value=to_time_value
        )

        return self._process_restore_response(request_json)

    def restore_out_of_place(
        self,
        dest_client_name: str,
        dest_instance_name: str,
        dest_backupset_name: str,
        target_path: str,
        **kwargs: object
    ) -> 'Job':
        """Restore DB2 data or log files to a different client, instance, or backupset (out-of-place restore).

        This method initiates an out-of-place restore operation for DB2 data or log files, allowing you to restore
        to a different client, instance, or backupset than the original source. Additional restore options can be
        specified using keyword arguments.

        Args:
            dest_client_name: The name of the destination client where the files will be restored.
            dest_instance_name: The DB2 instance name on the destination client.
            dest_backupset_name: The DB2 backupset name on the destination client.
            target_path: The destination path for the DB restore.
            **kwargs: Additional optional restore parameters, such as:
                - copy_precedence (int): Storage policy copy precedence. Default is None.
                - from_time (str): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
                - to_time (str): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
                - redirect_enabled (bool): Whether redirect restore is enabled. Default is False.
                - redirect_storage_group_path (dict): Mapping of storage group names to redirect paths.
                - redirect_tablespace_path (dict): Mapping of tablespace names to redirect paths.
                - destination_path (str): Destination path for restore. Default is None.
                - restore_data (bool): Whether to restore data.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the job initialization fails, the response is empty, or the response is not successful.

        Example:
            >>> db2_instance = DB2Instance(commcell)
            >>> job = db2_instance.restore_out_of_place(
            ...     dest_client_name='db2_dest_client',
            ...     dest_instance_name='db2_dest_instance',
            ...     dest_backupset_name='db2_dest_backupset',
            ...     target_path='/db2/restore/path',
            ...     copy_precedence=1,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-01-31 23:59:59',
            ...     redirect_enabled=True,
            ...     redirect_storage_group_path={'SG1': '/new/sg1/path'},
            ...     restore_data=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        copy_precedence = kwargs.get('copy_precedence', None)
        from_time = kwargs.get('from_time', None)
        to_time = kwargs.get('to_time', None)
        redirect_enabled = kwargs.get('redirect_enabled', False)
        redirect_tablespace_path = kwargs.get('redirect_tablespace_path', None)
        redirect_storage_group_path = kwargs.get('redirect_storage_group_path', None)
        rollforward = kwargs.get('rollforward', True)
        restoreArchiveLogs = kwargs.get('restoreArchiveLogs', False)
        restore_incremental = kwargs.get('restore_incremental', True)
        restore_data = kwargs.get('restore_data', True)

        if redirect_enabled:
            if not (isinstance(redirect_tablespace_path, dict) or isinstance(redirect_tablespace_path, str)) and \
                    not isinstance(redirect_storage_group_path, dict):
                raise SDKException('Instance', '101')

        request_json = self._restore_json(
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            dest_backupset_name=dest_backupset_name,
            target_db=dest_backupset_name,
            target_path=target_path,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            redirect=redirect_enabled,
            redirect_storage_group_path=redirect_storage_group_path,
            redirect_tablespace_path=redirect_tablespace_path,
            rollforward_pending=not rollforward,
            restore_archive_logs=restoreArchiveLogs,
            roll_forward=rollforward,
            restore_incremental=restore_incremental,
            storage_path=True,
            restore_data=restore_data)

        if redirect_storage_group_path:
            storagePaths = []
            storageGroup = {"storageGroup": []}

            for name, path in redirect_storage_group_path.items():
                if isinstance(path, str):
                    storageGroup["storageGroup"].append({"groupName": name, "stoPaths": [path]})
                    storagePaths = [path]
                else:
                    storageGroup["storageGroup"].append({"groupName": name, "stoPaths": path})
                    storagePaths = [path[0]]

            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                "redirectStorageGroups"] = True
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                "storagePaths"] = storagePaths
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                "storageGroupInfo"] = storageGroup

        if redirect_tablespace_path:
            if isinstance(redirect_tablespace_path, str):
                request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                    "redirectAllPaths"] = redirect_tablespace_path
                request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                    "redirectAllTableSpacesSelected"] = True
                request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                    "redirectAllTableSpacesValue"] = redirect_tablespace_path
            else:
                redirect_info = []
                for tablespace, path in redirect_tablespace_path.items():
                    table_string = "%s\t1\t%s\t6\t25600\t1\t1" % (tablespace, path)
                    redirect_info.append(table_string)
                request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                    "redirectInfo"] = redirect_info

        return self._process_restore_response(request_json)

    def restore_table_level(
        self,
        aux_client_name: str,
        aux_instance_name: str,
        aux_backupset_name: str,
        dest_client_name: str,
        dest_instance_name: str,
        dest_backupset_name: str,
        target_path: str,
        staging_path: str,
        tables_path: list,
        user_name: str,
        password: str,
        **kwargs
    ) -> 'Job':

        """Perform a DB2 table-level restore operation.

        This method initiates a table-level restore for a DB2 database, allowing you to restore specific tables 
        from an auxiliary backupset to a destination client and instance. Additional restore options can be 
        specified using keyword arguments.

        Args:
            aux_client_name: Name of the auxiliary client where files are to be restored.
            aux_instance_name: Name of the auxiliary DB2 instance for the restore.
            aux_backupset_name: Name of the auxiliary backupset for the restore.
            dest_client_name: Name of the destination client where tables will be restored.
            dest_instance_name: Name of the destination DB2 instance.
            dest_backupset_name: Name of the destination DB2 backupset.
            target_path: Path where the database will be restored.
            staging_path: Path to use for staging during the restore process.
            tables_path: List of table paths to restore. 
                Example (Unix): ['/+tblview+/instance_name/database_name/schema_name/table_name/**']
                Example (Windows): ["\\+tblview+\\instance_name\\database_name\\schema_name\\table_name\\**"]
            user_name: Username for the destination DB2 instance.
            password: Password for the destination DB2 instance.
            **kwargs: Additional optional parameters for advanced restore options, such as:
                - src_backupset_name (str): Source backupset name.
                - copy_precedence (int): Storage policy copy precedence.
                - from_time (str): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS').
                - to_time (str): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS').
                - rollForward (bool): Whether to perform rollforward recovery (default: True).
                - destination_path (str): Destination path for restore.
                - server_port (int): Server port for the destination instance (default: 50000).
                - generateAuthorizationDDL (bool): Generate authorization DDL (default: False).
                - extractDDLStatements (bool): Extract DDL statements (default: True).
                - clearAuxiliary (bool): Cleanup auxiliary after restore (default: True).
                - dropTable (bool): Drop table for import (default: False).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the restore job fails to initialize, if the response is empty, or if the response is not successful.

        Example:
            >>> db2_instance = DB2Instance()
            >>> job = db2_instance.restore_table_level(
            ...     aux_client_name="aux_client",
            ...     aux_instance_name="AUXINST",
            ...     aux_backupset_name="AUX_BKSET",
            ...     dest_client_name="dest_client",
            ...     dest_instance_name="DESTINST",
            ...     dest_backupset_name="DEST_BKSET",
            ...     target_path="/db2/restore",
            ...     staging_path="/db2/staging",
            ...     tables_path=['/+tblview+/INST/DB/SCHEMA/TABLE/**'],
            ...     user_name="db2user",
            ...     password="db2pass",
            ...     rollForward=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        copy_precedence = kwargs.get('copy_precedence', None)
        from_time = kwargs.get('from_time', None)
        to_time = kwargs.get('to_time', None)
        rollforward = kwargs.get('rollforward', True)
        restoreArchiveLogs = kwargs.get('restoreArchiveLogs', False)

        request_json = self._restore_json(
            dest_client_name=aux_client_name,
            dest_instance_name=aux_instance_name,
            dest_backupset_name=aux_backupset_name,
            target_db=aux_backupset_name,
            target_path=target_path,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            rollforward_pending=not rollforward,
            restoreArchiveLogs=restoreArchiveLogs,
            roll_forward=rollforward,
            storage_path=True,
            table_view_restore=True)

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
            "storagePaths"] = [target_path]

        password = b64encode(password.encode()).decode()

        table_json = {
            "additionalExportParameter": kwargs.get("additionalExportParameter", ""),
            "serverPort": kwargs.get("server_port", 50000),
            "generateAuthorizationDDL": kwargs.get("generateAuthorizationDDL", False),
            "importInstance": dest_instance_name,
            "extractDDLStatements": kwargs.get("extractDDLStatements", True),
            "useAdditionalExportParameters": kwargs.get("useAdditionalExportParameters", False),
            "auxiliaryInstance": False,
            "clearAuxiliary": kwargs.get("clearAuxiliary", True),
            "importDatabase": dest_backupset_name,
            "importToWhere": 2,
            "dropTable": kwargs.get("dropTable", False),
            "stagingPath": staging_path,
            "importDbClient": {"clientName": dest_client_name},
            "importUserInfo": {"userName": user_name, "password": password}
        }

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
            "storagePaths"] = [target_path]

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
            "databaseTableRstOptions"] = table_json

        request_json['taskInfo']["subTasks"][0]["options"]["restoreOptions"][
            "browseOption"]["backupset"]["backupsetId"] = int(self.backupsets.get(aux_backupset_name).backupset_id)

        request_json['taskInfo']["subTasks"][0]["options"]["restoreOptions"][
            "browseOption"]["backupset"]["backupsetName"] = aux_backupset_name

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
            "restoreArchiveLogs"] = False

        request_json['taskInfo']["subTasks"][0]["options"]["restoreOptions"][
            "fileOption"]["filterItem"] = tables_path
        request_json['taskInfo']["subTasks"][0]["options"]["restoreOptions"][
            "fileOption"]["sourceItem"] = tables_path
        return self._process_restore_response(request_json)
