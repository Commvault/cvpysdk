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

LNDBInstance is the only class defined in this file.

LNDBInstance:
    restore_in_place()                  --  performs an in place restore of the subclient

    restore_out_of_place()              --  performs an out of place restore of the subclient

    _restore_common_options_json()      --  setter for  the Common options in restore JSON

    _restore_json()                     --  returns the JSON request to pass to the API
    as per the options selected by the user

"""

from __future__ import unicode_literals

from typing import TYPE_CHECKING

from .lninstance import LNInstance
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class LNDBInstance(LNInstance):
    """
    Represents a Logical Node Database (LNDB) instance, extending the LNInstance base class.

    This class provides specialized operations for managing and restoring LNDB instances.
    It includes methods for restoring configuration options from JSON, as well as performing
    both in-place and out-of-place restore operations. The class is designed to facilitate
    data recovery and migration scenarios for LNDB instances, supporting granular control
    over restore parameters such as overwrite behavior, access control restoration, copy precedence,
    and time-based filtering.

    Key Features:
        - Restore common options from JSON configuration
        - Restore LNDB instance state from JSON
        - Perform in-place restore operations with customizable options
        - Perform out-of-place restore operations to different clients or destinations
        - Support for advanced restore parameters including overwrite, ACLs, copy precedence, and time range

    #ai-gen-doc
    """

    def _restore_common_options_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing the common options to be set in the restore JSON.

        Example:
            >>> options = {
            ...     "overwrite": True,
            ...     "preservePaths": False
            ... }
            >>> instance._restore_common_options_json(options)
            >>> # The common options in the restore JSON are now updated with the provided values

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "doNotReplayTransactLogs": value.get('common_options_dict').get(
                'doNotReplayTransactLogs', False
            ),
            "clusterDBBackedup": value.get('common_options_dict').get(
                'clusterDBBackedup', False
            ),
            "recoverWait": value.get('common_options_dict').get(
                'recoverWait', False
            ),
            "restoreToDisk": value.get('common_options_dict').get(
                'restoreToDisk', False
            ),
            "offlineMiningRestore": value.get('common_options_dict').get(
                'offlineMiningRestore', False
            ),
            "restoreToExchange": value.get('common_options_dict').get(
                'restoreToExchange', False
            ),
            "recoverZapIfNecessary": value.get('common_options_dict').get(
                'recoverZapIfNecessary', False
            ),
            "recoverZapReplica": value.get('common_options_dict').get(
                'recoverZapReplica', False
            ),
            "copyToObjectStore": value.get('common_options_dict').get(
                'copyToObjectStore', False
            ),
            "onePassRestore": value.get('common_options_dict').get(
                'onePassRestore', False
            ),
            "recoverZap": value.get('common_options_dict').get(
                'recoverZap', False
            ),
            "recoverRefreshBackup": value.get('common_options_dict').get(
                'recoverRefreshBackup', False
            ),
            "unconditionalOverwrite": value.get('common_options_dict').get(
                'unconditionalOverwrite', False
            ),
            "syncRestore": value.get('common_options_dict').get(
                'syncRestore', False
            ),
            "recoverPointInTime": value.get('common_options_dict').get(
                'recoverPointInTime', False
            )
        }

        if value.get('common_options_dict').get('disasterRecovery'):
            self._commonoption_restore_json.update({
                "restoreDeviceFilesAsRegularFiles": value.get('common_options_dict').get(
                    'restoreDeviceFilesAsRegularFiles', False
                ),
                "isFromBrowseBackup": value.get('common_options_dict').get(
                    'isFromBrowseBackup', False
                ),
                "ignoreNamespaceRequirements": value.get('common_options_dict').get(
                    'ignoreNamespaceRequirements', False
                ),
                "restoreSpaceRestrictions": value.get('common_options_dict').get(
                    'restoreSpaceRestrictions', False
                ),
                "skipErrorsAndContinue": value.get('common_options_dict').get(
                    'skipErrorsAndContinue', False
                ),
                "recoverAllProtectedMails": value.get('common_options_dict').get(
                    'recoverAllProtectedMails', False
                ),
                "validateOnly": value.get('common_options_dict').get(
                    'validateOnly', False
                ),
                "revert": value.get('common_options_dict').get(
                    'revert', False
                ),
                "disasterRecovery": value.get('common_options_dict').get(
                    'disasterRecovery', True
                ),
                "detectRegularExpression": value.get('common_options_dict').get(
                    'detectRegularExpression', True
                ),
            })

    def _restore_json(self, **kwargs: dict) -> dict:
        """Generate the JSON request payload for a restore operation based on user-selected options.

        This method constructs and returns a dictionary representing the JSON request body
        required by the API for performing a restore, using the options provided as keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing restore options and their values.

        Returns:
            dict: The JSON request dictionary to be sent to the API for the restore operation.

        Example:
            >>> instance = LNDBInstance()
            >>> restore_payload = instance._restore_json(source_path='/data', dest_path='/restore', overwrite=True)
            >>> print(restore_payload)
            {'source_path': '/data', 'dest_path': '/restore', 'overwrite': True}

        #ai-gen-doc
        """
        restore_json = super(LNDBInstance, self)._restore_json(**kwargs)

        restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'lotusNotesDBRestoreOption'] = {
                "disableReplication": kwargs.get('lndb_restore_options').get(
                    'disableReplication', False
                ),
                "disableBackgroundAgents": kwargs.get('lndb_restore_options').get(
                    'disableBackgroundAgents', False
                )
            }

        if kwargs.get('common_options_dict').get('disasterRecovery'):
            restore_json['taskInfo']['subTasks'][0]['options']['commonOpts'] = {
                'jobDescription': '',
                'startUpOpts': {
                    'startInSuspendedState': False,
                    'useDefaultPriority': True,
                    'priority': 166
                }
            }
            restore_json['taskInfo']['subTasks'][0]['options']['backupOpts'] = {
                'backupLevel': 2
            }
            restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'browseOption']['mediaOption']['copyPrecedence'] = {
                    'copyPrecedence': 0,
                    'synchronousCopyPrecedence': 1,
                    'copyPrecedenceApplicable': False
                }
        return restore_json

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
        """Restore files or folders to their original location within the LNDB instance.

        This method initiates an in-place restore operation for the specified files or folders.
        Additional options can be provided via keyword arguments to customize the restore behavior.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files will be unconditionally overwritten during restore. Default is True.
            restore_data_and_acl: If True, both data and ACL files are restored. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional lower bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            **kwargs: Additional restore options, such as:
                - common_options_dict (dict): Dictionary of common restore options (e.g., unconditionalOverwrite, recoverWait, disasterRecovery, etc.).
                - lndb_restore_options (dict): Dictionary of LNDB-specific restore options (e.g., disableReplication, disableBackgroundAgents).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If 'paths' is not a list, if the job fails to initialize, or if the restore response is empty or unsuccessful.

        Example:
            >>> lndb_instance = LNDBInstance()
            >>> restore_job = lndb_instance.restore_in_place(
            ...     paths=['/data/notes/db1.nsf', '/data/notes/db2.nsf'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'unconditionalOverwrite': True},
            ...     lndb_restore_options={'disableReplication': True}
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        return super(LNDBInstance, self).restore_in_place(
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)

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

        This method restores the specified files or folders (provided in the `paths` list) to the given
        `destination_path` on the specified `client`. The restore can be customized with options such as
        overwriting existing files, restoring data and ACLs, copy precedence, and time filters. Additional
        options can be provided via keyword arguments for advanced restore scenarios.

        Args:
            client: The target client for the restore. Can be either the client name (str) or a Client object.
            destination_path: The full path on the target client where the data will be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional; the copy precedence value of the storage policy copy to use.
            from_time: Optional; restore data modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore data modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            **kwargs: Additional restore options, such as:
                - common_options_dict (dict): Common restore options (e.g., unconditionalOverwrite, recoverWait, etc.).
                - lndb_restore_options (dict): LNDB-specific restore options (e.g., disableReplication).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize.

        Example:
            >>> # Restore files to a different client and path
            >>> job = lndb_instance.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location',
            ...     paths=['/data/file1.nsf', '/data/file2.nsf'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'unconditionalOverwrite': True},
            ...     lndb_restore_options={'disableReplication': True}
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        return super(LNDBInstance, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)