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

"""File for operating on a Lotus Notes Database Agent Instance.

LNDOCInstance is the only class defined in this file.

LNDOCInstance:
    _restore_common_options_json()      --  setter for  the Common options in restore JSON

    restore_in_place()                  --  performs an in place restore of the subclient

    restore_out_of_place()              --  performs an out of place restore of the subclient

"""

from __future__ import unicode_literals

from typing import Optional, Union

from .lninstance import LNInstance
from ...exception import SDKException
from ...job import Job
from ...client import Client

class LNDOCInstance(LNInstance):
    """
    Represents an LNDOC instance, extending the LNInstance base class to provide
    specialized operations for data restoration and configuration management.

    This class offers methods to restore data either in place or out of place,
    with support for advanced options such as overwriting, restoring data and ACLs,
    specifying copy precedence, and defining time ranges for restoration. It also
    includes functionality to restore common options from a JSON value, enabling
    flexible and customizable restore operations.

    Key Features:
        - Restore common options from JSON configuration
        - In-place data and ACL restoration with overwrite and time range support
        - Out-of-place restoration to different clients or destinations
        - Fine-grained control over restore parameters and options

    #ai-gen-doc
    """

    def _restore_common_options_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing the common options to be set in the restore JSON.

        Example:
            >>> options = {
            ...     "overwrite": True,
            ...     "preserve_permissions": False
            ... }
            >>> instance._restore_common_options_json(options)
            >>> # The common options in the restore JSON are now updated with the provided values.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "overwriteDBLinks": value.get('common_options_dict').get(
                'overwriteDBLinks', False
            ),
            "overwriteDesignDoc": value.get('common_options_dict').get(
                'overwriteDesignDoc', False
            ),
            "overwriteDataDoc": value.get('common_options_dict').get(
                'overwriteDataDoc', False
            ),
            "dbLinksOnly": value.get('common_options_dict').get(
                'dbLinksOnly', False
            ),
            "onePassRestore": value.get('common_options_dict').get(
                'onePassRestore', False
            ),
            "offlineMiningRestore": value.get('common_options_dict').get(
                'offlineMiningRestore', False
            ),
            "clusterDBBackedup": value.get('common_options_dict').get(
                'clusterDBBackedup', False
            ),
            "restoreToDisk": value.get('common_options_dict').get(
                'restoreToDisk', False
            ),
            "syncRestore": value.get('common_options_dict').get(
                'syncRestore', False
            ),
            "restoreToExchange": value.get('common_options_dict').get(
                'restoreToExchange', False
            ),
            "copyToObjectStore": value.get('common_options_dict').get(
                'copyToObjectStore', False
            )
        }

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
        """Restore specified files or folders to their original location within the LNDOC instance.

        This method initiates an in-place restore operation for the provided list of file or folder paths.
        Additional options such as unconditional overwrite, restoring data and ACLs, copy precedence, and
        time filters can be specified. Advanced restore options can be passed via keyword arguments.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files will be overwritten during restore. Defaults to True.
            restore_data_and_acl: If True, both data and ACL files are restored. Defaults to True.
            copy_precedence: Optional storage policy copy precedence value. Defaults to None.
            from_time: Optional lower time boundary for restore (format: 'YYYY-MM-DD HH:MM:SS'). Defaults to None.
            to_time: Optional upper time boundary for restore (format: 'YYYY-MM-DD HH:MM:SS'). Defaults to None.
            **kwargs: Additional advanced restore options, such as:
                - unconditionalOverwrite (bool): Overwrite files even if they exist.
                - recoverWait (bool): Wait for resources if a database recovery is in progress.
                - recoverZap (bool): Change the DBIID of the restored database.
                - recoverZapReplica (bool): Change the replica ID of the restored database.
                - recoverZapIfNecessary (bool): Change DBIID if necessary.
                - doNotReplayTransactLogs (bool): Skip restoring or replaying logs.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If 'paths' is not a list, if the job fails to initialize, or if the restore response is empty or unsuccessful.

        Example:
            >>> instance = LNDOCInstance()
            >>> restore_job = instance.restore_in_place(
            ...     paths=['/data/notes/file1.nsf', '/data/notes/file2.nsf'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     unconditionalOverwrite=True
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        return super(LNDOCInstance, self).restore_in_place(
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)

    def restore_out_of_place(
            self,
            client: 'Union[str, Client]',
            destination_path: str,
            paths: list,
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: 'Optional[int]' = None,
            from_time: 'Optional[str]' = None,
            to_time: 'Optional[str]' = None,
            common_options_dict: 'Optional[dict]' = None
        ) -> 'Job':
        """Restore specified files or folders to a different client and location.

        This method restores the files and folders listed in `paths` to the specified `destination_path`
        on the given `client`. The restore can be customized with options such as overwriting existing files,
        restoring data and ACLs, specifying copy precedence, and providing additional common options.

        Args:
            client: The target client for restore. Can be either the client name (str) or a Client object.
            destination_path: Full path on the client where the data should be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional; storage policy copy precedence value to use for restore.
            from_time: Optional; restore data modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore data modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            common_options_dict: Optional; dictionary of additional restore options, such as:
                - overwriteDBLinks (bool): Overwrite database links. Default is False.
                - overwriteDesignDoc (bool): Overwrite design documents. Default is False.
                - overwriteDataDoc (bool): Overwrite data documents. Default is False.
                - dbLinksOnly (bool): Overwrite only database links. Default is False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize or complete.

        Example:
            >>> instance = LNDOCInstance()
            >>> job = instance.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location',
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'overwriteDBLinks': True}
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        return super(LNDOCInstance, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)