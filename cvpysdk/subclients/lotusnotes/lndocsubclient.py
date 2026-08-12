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

"""File for operating on a Notes Document Subclient.

LNDocSubclient is the only class defined in this file.

LNDocSubclient:  Derived class from LNSubclient Base class.
Represents a notes document subclient, and performs operations on that subclient

LNDocSubclient:
    restore_in_place()          --  performs an in place restore of the subclient

    restore_out_of_place()      --  performs and out of place restore of the subclient

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from typing import Any, List, Optional, TYPE_CHECKING, Union

from .lnsubclient import LNSubclient
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job
    from ...client import Client

class LNDocSubclient(LNSubclient):
    """
    Represents a specialized LNDOC subclient for performing data restoration operations.

    This class extends the LNSubclient base class to provide functionality for restoring
    data either in place or out of place. It is designed to manage LNDOC subclient-specific
    restoration tasks, including handling file paths, overwrite options, access control lists,
    copy precedence, and time-based restoration filters.

    Key Features:
        - Restore data in place to the original location with customizable options
        - Restore data out of place to a different client or destination path
        - Support for overwriting existing data during restore
        - Ability to restore both data and associated ACLs
        - Specify copy precedence for restoration
        - Filter restoration by time range

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
        """Restore files or folders to their original location within the LNDocSubclient.

        This method initiates an in-place restore operation for the specified files or folders.
        You can control overwrite behavior, restore data and ACLs, specify copy precedence,
        and limit the restore to a specific time range. Additional restore options can be
        provided via keyword arguments.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files will be overwritten during restore. Default is True.
            restore_data_and_acl: If True, both data and ACL files are restored. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional lower bound for restore time window (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional upper bound for restore time window (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            **kwargs: Additional restore options, such as:
                - common_options_dict (dict): Dictionary of common restore options, e.g.:
                    - unconditionalOverwrite
                    - recoverWait
                    - recoverZap
                    - recoverZapReplica
                    - recoverZapIfNecessary
                    - doNotReplayTransactLogs
                    - skipErrorsAndContinue
                    - disasterRecovery

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If 'paths' is not a list, if the job fails to initialize,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> subclient = LNDocSubclient()
            >>> restore_job = subclient.restore_in_place(
            ...     paths=['/data/notesdb1.nsf', '/data/notesdb2.nsf'],
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
        return super(LNDocSubclient, self).restore_in_place(
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)

    def restore_out_of_place(
            self,
            client: Union[str, 'Client'],
            destination_path: str,
            paths: List[str],
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: Optional[int] = None,
            from_time: Optional[str] = None,
            to_time: Optional[str] = None,
            **kwargs: Any
        ) -> 'Job':
        """Restore files or folders out-of-place to a specified client and destination path.

        This method restores the files and folders listed in `paths` to the given `client` at the 
        specified `destination_path`. You can control overwrite behavior, restore ACLs, set copy 
        precedence, and filter restore data by time range. Additional options can be provided via 
        keyword arguments, such as common_options_dict for advanced restore settings.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: Full path on the client where data will be restored.
            paths: List of full file/folder paths to restore.
            overwrite: If True, files at the destination will be overwritten unconditionally. Default is True.
            restore_data_and_acl: If True, both data and ACL files will be restored. Default is True.
            copy_precedence: Optional copy precedence value for storage policy copy.
            from_time: Optional start time (format: 'YYYY-MM-DD HH:MM:SS') to restore contents after.
            to_time: Optional end time (format: 'YYYY-MM-DD HH:MM:SS') to restore contents before.
            **kwargs: Additional restore options, such as:
                common_options_dict (dict): Dictionary of advanced options:
                    - overwriteDBLinks (bool): Overwrite database links. Default: False.
                    - overwriteDesignDoc (bool): Overwrite design documents. Default: False.
                    - overwriteDataDoc (bool): Overwrite data documents. Default: False.
                    - dbLinksOnly (bool): Overwrite only database links. Default: False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize or execute.

        Example:
            >>> # Restore files to a different client and location
            >>> paths_to_restore = ['/data/docs/file1.nsf', '/data/docs/file2.nsf']
            >>> job = subclient.restore_out_of_place(
            ...     client='TargetClient01',
            ...     destination_path='/restore/location/',
            ...     paths=paths_to_restore,
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={
            ...         'overwriteDBLinks': True,
            ...         'overwriteDesignDoc': False
            ...     }
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        return super(LNDocSubclient, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)