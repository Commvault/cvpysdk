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

"""File for operating on a Domino Mailbox Archiver Subclient.

LNDmSubclient is the only class defined in this file.

LNDmSubclient:  Derived class from Subclient Base class.
Represents a domino mailbox archiver subclient, and performs operations on that subclient

LNDmSubclient:

    restore_in_place()                  -- performs an in place restore of the subclient

    restore_out_of_place()              -- performs and out of place restore of the subclient

    backup()                            --  run a backup job for the subclient
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from typing import TYPE_CHECKING

from .lnsubclient import LNSubclient
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class LNDmSubclient(LNSubclient):
    """
    Represents a LNDM subclient, derived from the LNSubclient base class.

    This class provides specialized operations for managing and restoring data
    associated with a LNDM subclient. It supports both in-place and out-of-place
    restore functionalities, allowing users to recover data to its original location
    or to a different client and destination path.

    Key Features:
        - In-place restore: Restore files and directories to their original locations
        - Out-of-place restore: Restore files and directories to a different client and path
        - Options for overwriting existing data and restoring data with ACLs
        - Support for specifying copy precedence and time ranges for restore operations

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
        """Restore specified files or folders to their original location (in-place restore).

        This method initiates an in-place restore operation for the provided list of file or folder paths.
        You can control overwrite behavior, restore data and ACLs, specify storage policy copy precedence,
        and set time filters for the restore. Additional common options can be passed as keyword arguments.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, unconditionally overwrite existing files during restore. Default is True.
            restore_data_and_acl: If True, restore both data and ACL files. Default is True.
            copy_precedence: Optional; storage policy copy precedence value. Default is None.
            from_time: Optional; restore contents modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore contents modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            **kwargs: Additional common restore options as keyword arguments. For example:
                - append (bool): Append documents to the database.
                - skip (bool): Skip if already present.
                - unconditionalOverwrite (bool): Overwrite the documents.
                - restoreOnlyStubExists (bool): Restore only if it is a stub.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If 'paths' is not a list, if the job fails to initialize, or if the restore response is empty or unsuccessful.

        Example:
            >>> subclient = LNDmSubclient()
            >>> restore_job = subclient.restore_in_place(
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     skip=True
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        return super(LNDmSubclient, self).restore_in_place(
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
        """Restore specified files or folders to a different client and destination path.

        This method restores the files or folders listed in `paths` to the specified `destination_path`
        on the given `client`. The restore can be customized with options such as overwriting existing
        files, restoring data and ACLs, specifying copy precedence, and filtering by time range.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: Full path on the target client where data will be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs are restored. Default is True.
            copy_precedence: Optional; storage policy copy precedence value. Default is None.
            from_time: Optional; restore data modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore data modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            **kwargs: Additional restore options, such as:
                - common_options_dict (dict): Dictionary of common restore options, e.g.:
                    - append (bool): Append documents to the database.
                    - skip (bool): Skip if already present.
                    - unconditionalOverwrite (bool): Overwrite the documents.
                    - restoreOnlyStubExists (bool): Restore only if it is a stub.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize.

        Example:
            >>> # Restore files to a different client and path
            >>> job = subclient.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location',
            ...     paths=['/data/file1.txt', '/data/file2.txt'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'skip': False, 'unconditionalOverwrite': True}
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        return super(LNDmSubclient, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)