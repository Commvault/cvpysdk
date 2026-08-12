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
    _commonoption_restore_json          --  setter for  the Common options in restore JSON

    restore_in_place()                  --  performs an in place restore of the subclient

    restore_out_of_place()              --  performs an out of place restore of the subclient

"""

from __future__ import unicode_literals

from typing import TYPE_CHECKING

from .lninstance import LNInstance
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class LNDMInstance(LNInstance):
    """
    Represents an LNDOC instance, derived from the LNInstance base class.

    This class provides specialized operations for managing and restoring data
    within an LNDOC instance. It includes methods for restoring data both in place
    and out of place, as well as handling common restore options in JSON format.

    Key Features:
        - Restore data in place with customizable options such as overwrite, ACL restoration, copy precedence, and time range selection.
        - Restore data out of place to a specified client and destination path, with similar customization options.
        - Manage and process common restore options using JSON input for flexible configuration.

    #ai-gen-doc
    """

    def _commonoption_restore_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing the common options to be set in the restore JSON.

        Example:
            >>> instance = LNDMInstance()
            >>> common_options = {
            ...     "overwrite": True,
            ...     "preserve_permissions": False
            ... }
            >>> instance._commonoption_restore_json(common_options)
            >>> # The common options are now set in the restore JSON

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "append": value.get('common_options_dict').get(
                'append', False
            ),
            "skip": value.get('common_options_dict').get(
                'skip', False
            ),
            "unconditionalOverwrite": value.get('common_options_dict').get(
                'unconditionalOverwrite', True
            ),
            "restoreOnlyStubExists": value.get('common_options_dict').get(
                'restoreOnlyStubExists', False
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
            "recoverToRecoveredItemsFolder": value.get('common_options_dict').get(
                'recoverToRecoveredItemsFolder', False
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
            common_options_dict: dict = None
        ) -> 'Job':
        """Restore files or folders to their original location (in-place restore).

        This method restores the specified files or folders, as provided in the `paths` list, 
        to their original location on the client. You can control overwrite behavior, 
        data and ACL restoration, copy precedence, time range, and additional restore options.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, unconditionally overwrite existing files during restore. Default is True.
            restore_data_and_acl: If True, restore both data and ACLs. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional lower bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper bound for restore time range (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            common_options_dict: Optional dictionary of additional restore options. Supported keys include:
                - 'append': Append documents to the database (default: False)
                - 'skip': Skip if already present (default: False)
                - 'unconditionalOverwrite': Overwrite the documents (default: False)
                - 'restoreOnlyStubExists': Restore only if it is a stub (default: False)

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If `paths` is not a list, if the job fails to initialize, 
                if the response is empty, or if the response indicates failure.

        Example:
            >>> instance = LNDMInstance()
            >>> restore_job = instance.restore_in_place(
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'skip': True}
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        return super(LNDMInstance, self).restore_in_place(
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
            common_options_dict: dict = None
        ) -> 'Job':
        """Restore specified files or folders to a different client and destination path.

        This method restores the files or folders listed in `paths` to the specified `destination_path`
        on the given `client`. The restore can be customized with options such as overwriting existing files,
        restoring data and ACLs, specifying copy precedence, time filters, and additional common options.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: Full path on the client where data will be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional lower time boundary for restore (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper time boundary for restore (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            common_options_dict: Optional dictionary of additional restore options. Supported keys include:
                - 'append': Append documents to the database (default: False)
                - 'skip': Skip if already present (default: False)
                - 'unconditionalOverwrite': Overwrite the documents (default: False)
                - 'restoreOnlyStubExists': Restore only if it is a stub (default: False)

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize.

        Example:
            >>> # Restore files to a different client and path
            >>> job = lndm_instance.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location',
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'skip': True}
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        return super(LNDMInstance, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)