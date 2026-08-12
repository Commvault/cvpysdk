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

"""File for operating on a Notes Database Subclient.

LNDbSubclient is the only class defined in this file.

LNDbSubclient:  Derived class from Subclient Base class.
Represents a notes database subclient, and performs operations on that subclient

LNDbSubclient:

    _get_subclient_properties()         --  gets subclient related properties of
    Notes Database subclient.

    _get_subclient_properties_json()    --  gets all the subclient related properties of
    Notes Database subclient.

    content()                           --  get the content of the subclient

    restore_in_place()                  -- performs an in place restore of the subclient

    restore_out_of_place()              -- performs and out of place restore of the subclient

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from typing import TYPE_CHECKING
from .lnsubclient import LNSubclient
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class LNDbSubclient(LNSubclient):
    """
    LNDbSubclient is a specialized subclient class derived from LNSubclient, designed to manage and perform operations on LNDB subclients.

    This class provides methods for retrieving subclient properties, managing subclient content, and performing both in-place and out-of-place restore operations. It is intended for use in environments where granular control and restoration of LNDB subclient data is required.

    Key Features:
        - Retrieve subclient properties and their JSON representations
        - Access and modify subclient content via property methods
        - Restore data in place with options for overwriting and ACL restoration
        - Restore data out of place to different clients or destinations
        - Support for specifying restore time ranges and copy precedence

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> dict:
        """Retrieve the subclient-related properties specific to the LN DB subclient.

        Returns:
            dict: A dictionary containing the properties and configuration details of the LN DB subclient.

        Example:
            >>> subclient = LNDbSubclient()
            >>> properties = subclient._get_subclient_properties()
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2', ...}

        #ai-gen-doc
        """
        super(LNDbSubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']
        if 'proxyClient' in self._subclient_properties:
            self._proxyClient = self._subclient_properties['proxyClient']
        if 'subClientEntity' in self._subclient_properties:
            self._subClientEntity = self._subclient_properties['subClientEntity']
        if 'commonProperties' in self._subclient_properties:
            self._commonProperties = self._subclient_properties['commonProperties']

    def _get_subclient_properties_json(self) -> dict:
        """Retrieve all properties related to this subclient as a dictionary.

        Returns:
            dict: A dictionary containing all subclient properties.

        Example:
            >>> subclient = LNDbSubclient()
            >>> properties = subclient._get_subclient_properties_json()
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2', ...}

        #ai-gen-doc
        """

        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def content(self) -> list:
        """Retrieve the content items associated with this LNDbSubclient.

        Returns:
            list: A list containing the content items relevant to the subclient.

        Example:
            >>> subclient = LNDbSubclient()
            >>> content_items = subclient.content  # Access content as a property
            >>> print(f"Subclient content: {content_items}")

        #ai-gen-doc
        """
        return self._content

    @content.setter
    def content(self, subclient_content: list) -> None:
        """Set the content for the LNDB Subclient by creating a list of content JSON objects.

        This method prepares the content in the appropriate JSON format required by the API
        to add or update the content of an LNDB Subclient.

        Args:
            subclient_content: A list containing the content items to be added to the subclient.

        Example:
            >>> lndb_subclient = LNDbSubclient()
            >>> new_content = [
            ...     {"database": "SalesDB", "schema": "public"},
            ...     {"database": "HRDB", "schema": "employees"}
            ... ]
            >>> lndb_subclient.content = new_content  # Use assignment for property setter
            >>> # The subclient content is now updated with the provided list

        #ai-gen-doc
        """
        content = []
        try:
            for database in subclient_content:
                if not database or 'useClientGroupGlobalFilter' in database:
                    continue
                elif 'lotusNotesDBContent' in database:
                    content.append(database)
                else:
                    temp_content_dict = {}
                    temp_content_dict = {
                        "lotusNotesDBContent": {
                            "dbiid1": database['dbiid1'],
                            "dbiid2": database['dbiid2'],
                            "dbiid3": database['dbiid3'],
                            "dbiid4": database['dbiid4'],
                            "relativePath": database['relativePath'],
                            "databaseTitle": database['databaseTitle']
                        }
                    }
                    if temp_content_dict != {}:
                        content.append(temp_content_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        self._set_subclient_properties("_content", content)

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
        """Restore files or folders to their original location in-place.

        This method restores the specified files or folders (provided as full paths in the `paths` list)
        to their original location on the source client. You can control overwrite behavior, restore
        data and ACLs, specify copy precedence, and set time filters for the restore. Additional
        options can be provided via keyword arguments for advanced restore scenarios.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files will be unconditionally overwritten during restore. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional string specifying the start time for restore (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            to_time: Optional string specifying the end time for restore (format: 'YYYY-MM-DD HH:MM:SS'). Default is None.
            **kwargs: Additional keyword arguments for advanced restore options, such as:
                - common_options_dict (dict): Dictionary of common restore options (e.g., unconditionalOverwrite, recoverWait, disasterRecovery, etc.).
                - lndb_restore_options (dict): Dictionary of LNDb-specific restore options (e.g., disableReplication, disableBackgroundAgents).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If `paths` is not a list, if the job fails to initialize, if the response is empty, or if the response indicates failure.

        Example:
            >>> # Restore two databases in-place, overwriting existing files
            >>> job = lndb_subclient.restore_in_place(
            ...     paths=['/data/notes/mail/user1.nsf', '/data/notes/mail/user2.nsf'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-01-31 23:59:59',
            ...     common_options_dict={'unconditionalOverwrite': True},
            ...     lndb_restore_options={'disableReplication': True}
            ... )
            >>> print(f"Restore job ID: {job.job_id}")

        #ai-gen-doc
        """
        return super(LNDbSubclient, self).restore_in_place(
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

        This method restores the specified files or folders from the backup to a given client
        at the provided destination path. It supports various options such as overwriting existing files,
        restoring data and ACLs, specifying copy precedence, and filtering by time range. Additional
        options can be provided via keyword arguments for advanced restore scenarios.

        Args:
            client: The target client for the restore operation. This can be either the client name (str)
                or an instance of the Client class.
            destination_path: The full path on the destination client where the data should be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional; the copy precedence value of the storage policy copy to use.
            from_time: Optional; restore only data modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore only data modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            **kwargs: Additional keyword arguments for advanced restore options, such as:
                - common_options_dict (dict): Common restore options (e.g., unconditionalOverwrite, recoverWait, etc.).
                - lndb_restore_options (dict): LNDb-specific restore options (e.g., disableReplication).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If any of the following conditions are met:
                - The client is not a string or Client instance.
                - The destination_path is not a string.
                - The paths argument is not a list.
                - Failed to initialize the restore job.
                - The response is empty or indicates failure.

        Example:
            >>> # Restore two databases to a different client and path, overwriting existing files
            >>> job = lndb_subclient.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location/',
            ...     paths=['/data/db1.nsf', '/data/db2.nsf'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     common_options_dict={'unconditionalOverwrite': True},
            ...     lndb_restore_options={'disableReplication': True}
            ... )
            >>> print(f"Restore job ID: {job.job_id}")

        #ai-gen-doc
        """
        return super(LNDbSubclient, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)