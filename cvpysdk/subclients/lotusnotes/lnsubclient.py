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

"""Main file for operating on any Lotus Notes Subclient.

LNSubclient is the only class defined in this file.

LNSubclient:        Class for representing all the Lotus Notes iDAs and performing
                        operations on them

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ...subclient import Subclient
from ...exception import SDKException
from ...job import Job

class LNSubclient(Subclient):
    """
    LNSubclient is a specialized subclass of the Subclient base class, designed to manage
    and perform operations specific to LN subclients within a backup and restore framework.

    This class provides methods for executing backup operations and restoring data either
    in place or to alternate locations. It supports granular control over backup levels,
    incremental backups, scheduling, and restoration parameters such as overwrite options,
    access control lists (ACLs), and time-based data selection.

    Key Features:
        - In-place restoration of data with options for overwriting and ACL restoration
        - Out-of-place restoration to different clients or destinations
        - Flexible backup operations supporting full, incremental, and scheduled backups
        - Time-based data selection for restore operations
        - Integration with copy precedence for restore and backup management

    #ai-gen-doc
    """

    def restore_in_place(
            self,
            paths: list,
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: int = None,
            from_time: str = None,
            to_time: str = None,
            **kwargs
        ) -> 'Job':
        """Restore files or folders to their original location within the same client.

        This method initiates an in-place restore operation for the specified files or folders.
        The restore can optionally overwrite existing files and restore both data and ACLs.
        You can also specify a storage policy copy precedence and a time range for the restore.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs are restored. Default is True.
            copy_precedence: Optional; storage policy copy precedence to use for the restore.
            from_time: Optional; restore contents modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore contents modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            **kwargs: Additional keyword arguments for advanced restore options.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If 'paths' is not a list, if the job fails to initialize, 
                or if the restore response is empty or unsuccessful.

        Example:
            >>> subclient = LNSubclient()
            >>> restore_job = subclient.restore_in_place(
            ...     paths=['/user/docs/report.docx', '/user/photos/'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59'
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        if not (isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if kwargs.get('common_options_dict') is None:
            kwargs['common_options_dict'] = {}

        if kwargs.get('lndb_restore_options') is None:
            kwargs['lndb_restore_options'] = {}

        paths = self._filter_paths(paths)

        if paths == []:
            raise SDKException('Subclient', '104')

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        request_json = self._restore_json(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            **kwargs
        )

        return self._process_restore_response(request_json)

    def restore_out_of_place(
            self,
            client: object,
            destination_path: str,
            paths: list,
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: int = None,
            from_time: str = None,
            to_time: str = None,
            **kwargs
        ) -> 'Job':
        """Restore files or folders to a different client and location.

        This method restores the specified files or folders from backup to a given destination path
        on the specified client. The restore can be performed with options to overwrite existing files,
        restore data and ACLs, specify copy precedence, and filter by time range.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: The full path on the destination client where data will be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional; copy precedence value for the storage policy copy.
            from_time: Optional; restore contents modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore contents modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            **kwargs: Additional keyword arguments for advanced restore options.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize.

        Example:
            >>> # Restore files to a different client and location
            >>> job = subclient.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location',
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        if not (isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if kwargs.get('common_options_dict') is None:
            kwargs['common_options_dict'] = {}

        if kwargs.get('lndb_restore_options') is None:
            kwargs['lndb_restore_options'] = {}

        paths = self._filter_paths(paths)

        if paths == []:
            raise SDKException('Subclient', '104')

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        request_json = self._restore_json(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            in_place=False,
            **kwargs)

        return self._process_restore_response(request_json)

    def backup(self,
               backup_level: str = "Incremental",
               incremental_backup: bool = False,
               incremental_level: str = 'BEFORE_SYNTH',
               schedule_pattern: dict = None) -> dict:
        """Generate the JSON request for a backup operation with the specified options.

        This method constructs and returns a JSON request payload to be used with the API,
        based on the backup options provided by the user.

        Args:
            backup_level: The level of backup to perform. Supported values are:
                "Full", "Incremental", "Differential", "Synthetic_full".
                Defaults to "Incremental".
            incremental_backup: Whether to run an incremental backup as part of a synthetic full backup.
                Only applicable when backup_level is "Synthetic_full". Defaults to False.
            incremental_level: Specifies when to run the incremental backup relative to the synthetic full.
                Supported values are "BEFORE_SYNTH" or "AFTER_SYNTH".
                Only applicable when backup_level is "Synthetic_full". Defaults to "BEFORE_SYNTH".
            schedule_pattern: A dictionary specifying scheduling options for the backup task.
                Refer to the documentation for `schedules.schedulePattern.createSchedule()` for details
                on the expected format.

        Returns:
            dict: The JSON request payload to be passed to the API for initiating the backup.

        Example:
            >>> subclient = LNSubclient()
            >>> backup_request = subclient.backup(
            ...     backup_level="Synthetic_full",
            ...     incremental_backup=True,
            ...     incremental_level="AFTER_SYNTH",
            ...     schedule_pattern={"pattern": "Daily"}
            ... )
            >>> print(backup_request)
            # The returned dictionary can be used to trigger a backup via the API.

        #ai-gen-doc
        """

        if schedule_pattern:
            request_json = self._backup_json(
                backup_level,
                incremental_backup,
                incremental_level,
                schedule_pattern=schedule_pattern)

            backup_service = self._services['CREATE_TASK']

            flag, response = self._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

        else:
            return super(LNSubclient, self).backup(
                backup_level=backup_level,
                incremental_backup=incremental_backup,
                incremental_level=incremental_level)

        return self._process_backup_response(flag, response)