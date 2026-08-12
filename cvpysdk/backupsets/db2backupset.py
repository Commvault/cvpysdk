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

"""File for operating on a DB2 Backupset.

DB2Backupset is the only class defined in this file.

DB2Backupset:  Derived class from Backupset Base class, representing a db2 backupset,
and to perform operations on that subclient

DB2Backupset:
=============

    restore_entire_database()       --      runs the restore job for specified backupset

    restore_out_of_place()          --      runs the out of place restore for given backupset

    restore_table_level()           --      Table level restore function


DB2Backupset instance Attributes:
=================================

    **db2_db_status**       --      returns db2 database status

"""

from __future__ import unicode_literals

from ..backupset import Backupset
from typing import Any, Optional

class DB2Backupset(Backupset):
    """
    Represents a DB2 backupset and provides specialized operations for DB2 database backup and restore.

    This class extends the Backupset base class to support DB2-specific backupset management. It offers
    properties and methods to monitor database status and perform various restore operations, including
    entire database restores, out-of-place restores, and table-level restores. The class is designed to
    facilitate flexible and granular recovery scenarios for DB2 databases.

    Key Features:
        - Property to retrieve DB2 database status
        - Restore the entire DB2 database to a specified destination
        - Perform out-of-place restores to different clients, instances, or backupsets
        - Restore specific tables with support for auxiliary clients, staging paths, and authentication

    #ai-gen-doc
    """

    @property
    def db2_db_status(self) -> str:
        """Get the current status of the DB2 database.

        Returns:
            The status of the DB2 database as a string, such as "connected" or "disconnected".

        Example:
            >>> backupset = DB2Backupset(...)
            >>> status = backupset.db2_db_status  # Use dot notation for property access
            >>> print(f"DB2 database status: {status}")
            >>> # Output might be: "connected" or "disconnected"

        #ai-gen-doc
        """
        return self._properties.get('db2BackupSet', {}).get('dB2DBStatus', "")

    def restore_entire_database(
            self,
            dest_client_name: Optional[str] = None,
            dest_instance_name: Optional[str] = None,
            dest_database_name: Optional[str] = None,
            **kwargs: Any
        ):
        """Restore the entire DB2 database to the specified destination.

        This method initiates a restore operation for the DB2 database associated with this backupset.
        The database can be restored to a different client, instance, or database name as specified.
        Additional restore options can be provided via keyword arguments.

        Args:
            dest_client_name: Optional; destination client name where the database should be restored. If not provided, defaults to the source client.
            dest_instance_name: Optional; destination DB2 instance name on the destination client. If not provided, defaults to the source instance.
            dest_database_name: Optional; destination database name. If not provided, defaults to the backupset name in uppercase.
            **kwargs: Additional restore options such as:
                - recover_db (bool): Whether to recover the database after restore (default: True).
                - restore_incremental (bool): Whether to restore incremental backups (default: True).
                - restore_data (bool): Whether to restore data (default: True).
                - copy_precedence (int): Copy precedence to use for restore (default: None).
                - roll_forward (bool): Whether to roll forward the database after restore (default: True).
                - restore_logs (bool): Whether to restore logs (default: True).

        Returns:
            Job: Instance of the Job class representing the restore job.

        Raises:
            SDKException: If the restore job fails to initialize, if the response is empty, or if the response indicates failure.

        Example:
            >>> backupset = DB2Backupset(...)
            >>> # Restore to the same client and instance
            >>> job = backupset.restore_entire_database()
            >>> print(f"Restore job started: {job}")
            >>>
            >>> # Restore to a different client and instance with custom options
            >>> job = backupset.restore_entire_database(
            ...     dest_client_name="DB2Client02",
            ...     dest_instance_name="DB2Instance02",
            ...     dest_database_name="RESTORED_DB",
            ...     recover_db=True,
            ...     restore_incremental=False,
            ...     copy_precedence=2
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        self._instance_object._restore_association = self._backupset_association

        instance_object = self._instance_object
        if dest_client_name is None:
            dest_client_name = instance_object._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = instance_object.instance_name

        if dest_database_name is None:
            dest_database_name = self.backupset_name.upper()

        return self._instance_object.restore_entire_database(
            dest_client_name, dest_instance_name, dest_database_name, **kwargs)

    def restore_out_of_place(
            self,
            dest_client_name: str,
            dest_instance_name: str,
            dest_backupset_name: str,
            target_path: str,
            **kwargs: Any
    ) -> 'Job':
        """Restore DB2 data or log files to a different client, instance, or backupset.

        This method initiates an out-of-place restore operation for DB2 data or log files,
        allowing you to specify a destination client, instance, backupset, and target path.
        Advanced options such as copy precedence, time filters, redirect restore, and
        storage group/tablespace path redirection can be provided via keyword arguments.

        Args:
            dest_client_name: Name of the destination client where files will be restored.
            dest_instance_name: Name of the destination DB2 instance on the destination client.
            dest_backupset_name: Name of the destination DB2 backupset on the destination client.
            target_path: Target path for the DB restore destination.
            **kwargs: Additional advanced restore options, such as:
                - copy_precedence (int): Storage policy copy precedence.
                - from_time (str): Restore contents after this time (YYYY-MM-DD HH:MM:SS).
                - to_time (str): Restore contents before this time (YYYY-MM-DD HH:MM:SS).
                - redirect_enabled (bool): Enable redirect restore.
                - redirect_storage_group_path (dict): Redirect paths for storage groups.
                - redirect_tablespace_path (dict): Redirect paths for tablespaces.
                - destination_path (str): Destination path for restore.
                - restore_data (bool): Whether to restore data (default: True).

        Returns:
            Job: Instance representing the restore job.

        Raises:
            SDKException: If the restore job fails to initialize, response is empty, or response is not successful.

        Example:
            >>> backupset = DB2Backupset(...)
            >>> job = backupset.restore_out_of_place(
            ...     dest_client_name="DB2Client02",
            ...     dest_instance_name="DB2Instance02",
            ...     dest_backupset_name="Backupset02",
            ...     target_path="/db2/restore/target",
            ...     copy_precedence=2,
            ...     from_time="2024-05-01 00:00:00",
            ...     to_time="2024-06-01 23:59:59",
            ...     redirect_enabled=True,
            ...     redirect_storage_group_path={"SG1": "/new/path/sg1"},
            ...     restore_data=True
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        self._instance_object._restore_association = self._backupset_association

        return self._instance_object.restore_out_of_place(dest_client_name=dest_client_name,
                                                          dest_instance_name=dest_instance_name,
                                                          dest_backupset_name=dest_backupset_name,
                                                          target_path=target_path,
                                                          **kwargs)

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
            **kwargs: Any
        ):
        """Perform a DB2 table-level restore operation.

        This method initiates a table-level restore for DB2 databases, allowing you to specify 
        auxiliary and destination client details, restore paths, table paths, and authentication credentials.
        Additional restore options can be provided via keyword arguments.

        Args:
            aux_client_name: Auxiliary client name where files are to be restored.
            aux_instance_name: Auxiliary instance name for the restore operation.
            aux_backupset_name: Auxiliary backupset name for the restore.
            dest_client_name: Destination client name for the restore.
            dest_instance_name: Destination DB2 instance name on the destination client.
            dest_backupset_name: Destination DB2 backupset name on the destination client.
            target_path: Path where the database will be restored.
            staging_path: Path used for staging during restore.
            tables_path: List of table paths to restore. 
                Example (Unix): ['/+tblview+/instance_name/database_name/schema_name/table_name/**']
                Example (Windows): ["\\+tblview+\\instance_name\\database_name\\schema_name\\table_name\\**"]
            user_name: Username for authentication on the destination.
            password: Password for authentication on the destination.
            **kwargs: Additional restore options such as:
                - copy_precedence (int): Storage policy copy precedence.
                - from_time (str): Restore contents after this time (YYYY-MM-DD HH:MM:SS).
                - to_time (str): Restore contents before this time (YYYY-MM-DD HH:MM:SS).
                - rollForward (bool): Whether to perform rollforward recovery.
                - destination_path (str): Destination path for restore.
                - server_port (int): Server port for destination instance.
                - generateAuthorizationDDL (bool): Generate authorization DDL.
                - extractDDLStatements (bool): Extract DDL statements.
                - clearAuxiliary (bool): Cleanup auxiliary files after restore.
                - dropTable (bool): Drop table before import.

        Returns:
            Job: Instance of the Job class representing the restore job.

        Raises:
            SDKException: If the job initialization fails, response is empty, or response is not successful.

        Example:
            >>> tables = [
            ...     '/+tblview+/instance1/db1/schema1/table1/**',
            ...     '/+tblview+/instance1/db1/schema2/table2/**'
            ... ]
            >>> job = db2_backupset.restore_table_level(
            ...     aux_client_name='AuxClient',
            ...     aux_instance_name='AuxInstance',
            ...     aux_backupset_name='AuxBackupset',
            ...     dest_client_name='DestClient',
            ...     dest_instance_name='DestInstance',
            ...     dest_backupset_name='DestBackupset',
            ...     target_path='/db2/restore',
            ...     staging_path='/db2/staging',
            ...     tables_path=tables,
            ...     user_name='db2user',
            ...     password='password123',
            ...     copy_precedence=1,
            ...     rollForward=True
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """

        self._instance_object._restore_association = self._backupset_association

        return self._instance_object.restore_table_level(aux_client_name=aux_client_name,
                                                         aux_instance_name=aux_instance_name,
                                                         aux_backupset_name=aux_backupset_name,
                                                         dest_client_name=dest_client_name,
                                                         dest_instance_name=dest_instance_name,
                                                         dest_backupset_name=dest_backupset_name,
                                                         target_path=target_path,
                                                         staging_path=staging_path,
                                                         tables_path=tables_path,
                                                         user_name=user_name,
                                                         password=password,
                                                         **kwargs)
