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

"""Main file for operating on all Lotus Notes Instances.

LNInstance is the only class defined in this file.

LNInstance:
    restore_in_place()                  -- performs an in place restore

    restore_out_of_place()              -- performs an out of place restore

"""

from __future__ import unicode_literals

from typing import TYPE_CHECKING

from ...instance import Instance
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class LNInstance(Instance):
    """
    Represents an LNDOC instance, extending the Instance base class to provide specialized
    operations for data restoration.

    This class offers methods to perform both in-place and out-of-place restore operations
    on LNDOC instances. It allows users to restore data and access control lists (ACLs)
    from specified paths, with options to overwrite existing data, set copy precedence,
    and define restore time ranges. Out-of-place restores enable restoration to different
    clients and destination paths.

    Key Features:
        - In-place restore of data and ACLs from specified paths
        - Out-of-place restore to alternate clients and destinations
        - Overwrite control for existing data during restore
        - Support for copy precedence and time range selection

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
        """Restore files or folders to their original location within the LNInstance.

        This method restores the specified files or folders, as provided in the `paths` list, 
        to their original location on the source client. Various options allow you to control 
        overwrite behavior, data and ACL restoration, copy precedence, and time-based filtering. 
        Additional restore options can be provided via keyword arguments.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs are restored. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional string in 'YYYY-MM-DD HH:MM:SS' format to restore items modified after this time.
            to_time: Optional string in 'YYYY-MM-DD HH:MM:SS' format to restore items modified before this time.
            **kwargs: Additional restore options, such as:
                - common_options_dict (dict): Dictionary of advanced restore options, e.g.:
                    - unconditionalOverwrite (bool)
                    - recoverWait (bool)
                    - recoverZap (bool)
                    - recoverZapReplica (bool)
                    - recoverZapIfNecessary (bool)
                    - doNotReplayTransactLogs (bool)

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If `paths` is not a list, if the job fails to initialize, 
                or if the restore response is empty or unsuccessful.

        Example:
            >>> ln_instance = LNInstance()
            >>> restore_job = ln_instance.restore_in_place(
            ...     paths=['/data/mail1.nsf', '/data/mail2.nsf'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'unconditionalOverwrite': True}
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        self._restore_association = self.backupsets.get(
            list(self.backupsets.all_backupsets)[0]
        )._backupset_association

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
        """Restore files or folders to a different client and destination path.

        This method restores the specified files or folders from backup to a given client at the provided
        destination path. You can control overwrite behavior, restore data and ACLs, specify copy precedence,
        and filter restore content by time range. Additional restore options can be provided via keyword arguments.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object instance.
            destination_path: Full path on the target client where data will be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs are restored. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional lower bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            **kwargs: Additional restore options as keyword arguments. Common options include:
                - overwriteDBLinks (bool): Overwrite database links. Default is False.
                - overwriteDesignDoc (bool): Overwrite design documents. Default is False.
                - overwriteDataDoc (bool): Overwrite data documents. Default is False.
                - dbLinksOnly (bool): Overwrite only database links. Default is False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize or complete.

        Example:
            >>> # Restore files to a different client and path
            >>> job = ln_instance.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location',
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     overwriteDBLinks=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        self._restore_association = self.backupsets.get(
            list(self.backupsets.all_backupsets)[0]
        )._backupset_association

        request_json = self._restore_json(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            **kwargs
        )

        return self._process_restore_response(request_json)