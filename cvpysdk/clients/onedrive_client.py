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

"""
OneDriveClient class is defined in this file.

OneDriveClient:     Class for a single OneDrive for Business client (v2) of the commcell

OneDriveClient
=======

_get_subclient() --  Returns the sub-client object for OneDrive for Business client (v2)

backup_all_users_in_client() -- Run backup for all users present in OneDrive for Business client (v2)

in_place_restore()  --  Run an inplace restore of specified users for OneDrive for business client (v2)

out_of_place_restore()  --  Run an out-of-place restore of specified users for OneDrive for business client (v2)

disk_restore()  --  Runs disk restore of specified users for OneDrive for business client (v2)

modify_server_plan()  --  Method to Modify Server Plan Associated to Client

modify_job_results_directory()  --  Method to modify job results directory

run_trueup_for_whole_client()  --  Method to run TrueUp for whole client

read_trueup_items_for_whole_client()  --  Method to read data from TrueUp API for whole client

extract_last_sync_missing_items() --  Extract LastSyncMissingItems values from JSON data for TrueUp API

restore_to_azure_blob() -- Runs restore to azure blob for specified users on OneDrive for business client

"""


from typing import Any, List, Optional

from ..client import Client, SDKException
from cvpysdk.commcell import Commcell
from cvpysdk.job import Job

class OneDriveClient(Client):
    """
    OneDriveClient provides comprehensive management and data protection operations for OneDrive clients.

    This class enables backup, restore, and configuration management for OneDrive users within a client.
    It supports various restore scenarios including in-place, out-of-place, disk-based, and Azure Blob restores.
    Additionally, it allows modification of server plans and job results directories, and facilitates true-up operations
    to ensure data consistency across the client.

    Key Features:
        - Initialization with commcell object, client name, and client ID
        - Retrieval of subclient information
        - Execution and reading of true-up operations for the whole client
        - Backup of all users in the client
        - In-place and out-of-place restore operations for selected users
        - Disk restore to specified clients and paths with optional file permission skipping
        - Restore data directly to Azure Blob storage
        - Modification of server plans for migration or upgrade scenarios
        - Update of job results directory for shared environments

    #ai-gen-doc
    """
    def __init__(self, commcell_object: 'Commcell', client_name: str, client_id: Optional[str] = None) -> None:
        """Initialize a OneDriveClient instance for managing OneDrive operations.

        Args:
            commcell_object: Instance of the Commcell class representing the Commcell connection.
            client_name: Name of the OneDrive client as a string.
            client_id: Optional string representing the client ID. If not provided, defaults to None.

        Example:
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> onedrive_client = OneDriveClient(commcell, "OneDriveClient01", client_id="12345")
            >>> # The OneDriveClient object can now be used for OneDrive operations

        #ai-gen-doc
        """
        super(OneDriveClient, self).__init__(
            commcell_object, client_name, client_id)

    def _get_subclient(self) -> Any:
        """Retrieve the subclient object for the OneDrive for Business client.

        This method navigates through the Commcell object hierarchy to obtain the
        subclient associated with the default OneDrive backupset.

        Returns:
            The subclient object for the OneDrive for Business client.

        Example:
            >>> onedrive_client = OneDriveClient(commcell_object, client_name)
            >>> subclient = onedrive_client._get_subclient()
            >>> print(f"Subclient object: {subclient}")
            >>> # The returned subclient object can be used for backup and restore operations

        #ai-gen-doc
        """
        _client = self._commcell_object.clients.get(self.client_name)
        _agent = _client.agents.get('Cloud Apps')
        _instance = _agent.instances.get('OneDrive')
        _backupset = _instance.backupsets.get('defaultbackupset')
        _subclient = _backupset.subclients.get('default')
        return _subclient

    def run_trueup_for_whole_client(self) -> None:
        """Run the TrueUp operation for the entire OneDrive client.

        This method initiates a TrueUp process for the whole client, ensuring that
        the backup data is synchronized and up-to-date. If the TrueUp operation fails,
        an SDKException is raised with details about the error.

        Raises:
            SDKException: If the TrueUp operation fails for the client.

        Example:
            >>> onedrive_client = OneDriveClient(...)
            >>> onedrive_client.run_trueup_for_whole_client()
            >>> print("TrueUp operation completed successfully")
            # If the operation fails, an SDKException will be raised with error details.

        #ai-gen-doc
        """
        base_url = self._commcell_object.webconsole_hostname
        url = self._services['RUN_TRUEUP'].format(base_url)
        trueup_json = {
            "processinginstructioninfo": {
                "formatFlags": {
                    "skipIdToNameConversion": True
                }
            },
            "isEnterprise": True,
            "discoverySentTypes": [
                20
            ],
            "subclientDetails": {
                "instanceId": 7,  # Used for unique verification of Agent Type, not the same as the instanceId generated by the CommServe
                "subclientName": "default",
                "clientId": int(self.client_id),
                "applicationId": 134,
                "instanceName": "OneDrive",
                "backupsetName": "defaultBackupSet"
            }
        }
        flag, response = self._cvpysdk_object.make_request(method='POST',
                                                           url=url, payload=trueup_json)
        if flag:
            if response.json() and 'errorCode' in response.json():
                error_code = response.json().get('errorCode')
                if error_code != 0:
                    error_message = response.json().get('errorMessage')
                    output_string = f'Failed to run trueup with \nError: {error_message}'
                    raise SDKException('Response', '101', output_string)
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text))

    def read_trueup_items_for_whole_client(self) -> int:
        """Read the number of items from the TrueUp API for the entire client.

        This method queries the TrueUp API for the current client and returns the total number of items
        reported as missing during the last synchronization. If the API call fails, an SDKException is raised.

        Returns:
            int: The total number of items in the TrueUp response.

        Raises:
            SDKException: If an error occurs while reading the TrueUp response.

        Example:
            >>> client = OneDriveClient(...)
            >>> num_items = client.read_trueup_items_for_whole_client()
            >>> print(f"Number of TrueUp items: {num_items}")
        #ai-gen-doc
        """

        def extract_last_sync_missing_items(json_data):
            """Extract LastSyncMissingItems values from JSON data

            Args:
                json_data (dict) : JSON data from TrueUp API

            Returns:
                last_sync_missing_items (list) : List of LastSyncMissingItems values from TrueUp API
            """
            last_sync_missing_items = []
            rows = json_data.get('rows', [])

            for row in rows:
                row_data = row.get('row', [])
                if len(row_data) >= 6:  # Ensure there are enough elements
                    last_sync_missing_items.append(int(row_data[5]))
            return last_sync_missing_items

        subclient_id = self._get_subclient().subclient_id
        client_id = self._client_id
        base_url = self._commcell_object.webconsole_hostname
        url = self._services['READ_TRUEUP_RESULTS_CLIENT'].format(base_url)
        url = url % (subclient_id, client_id)
        flag, response = self._cvpysdk_object.make_request(
            method='GET', url=url)
        if flag:
            last_sync_missing_items = extract_last_sync_missing_items(
                response.json())
            num_of_items = sum(last_sync_missing_items)
            return num_of_items
        else:
            raise (
                SDKException('Response', '101', f'Error occurred while reading TrueUp response \nError: {response.text}'))

    def backup_all_users_in_client(self) -> 'Job':
        """Run an incremental backup for all users present in the OneDrive client.

        This method initiates a backup operation for every user associated with the current OneDrive client instance.
        The backup is performed at the incremental level, capturing only changes since the last backup.

        Returns:
            Job: Instance of the Job class representing the initiated backup job.

        Example:
            >>> onedrive_client = OneDriveClient(...)
            >>> backup_job = onedrive_client.backup_all_users_in_client()
            >>> print(f"Backup job started: {backup_job}")
            >>> # The returned Job object can be used to monitor backup progress

        #ai-gen-doc
        """
        _subclient_object = self._get_subclient()
        return _subclient_object.backup(backup_level='INCREMENTAL')

    def in_place_restore(self, users: List[str], **kwargs: Any):
        """Run an in-place restore for specified OneDrive for Business users.

        This method initiates an in-place restore operation for the provided list of user SMTP addresses.
        Additional restore options can be specified using keyword arguments.

        Args:
            users: List of SMTP addresses (strings) representing the users to restore.
            **kwargs: Additional restore options.
                overwrite (bool, optional): If True, files are unconditionally overwritten during restore (default: False).
                restore_as_copy (bool, optional): If True, files are restored as copies (default: False).
                skip_file_permissions (bool, optional): If True, file permissions are not restored (default: False).

        Returns:
            An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input types are incorrect, job initialization fails, response is empty, or response is not successful.

        Example:
            >>> client = OneDriveClient(...)
            >>> users = ['user1@domain.com', 'user2@domain.com']
            >>> job = client.in_place_restore(users, overwrite=True, restore_as_copy=False)
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        _subclient_object = self._get_subclient()
        restore_job = _subclient_object.in_place_restore_onedrive_for_business_client(
            users, **kwargs)
        return restore_job

    def out_of_place_restore(self, users: List[str], destination_path: str, **kwargs: Any):
        """Run an out-of-place restore for specified OneDrive for Business users.

        This method initiates a restore operation for the given list of users, restoring their OneDrive data
        to the specified destination user. Additional restore options can be provided via keyword arguments.

        Args:
            users: List of SMTP addresses representing the users whose data will be restored.
            destination_path: SMTP address of the destination user where data will be restored.
            **kwargs: Additional restore options.
                overwrite (bool): If True, files will be unconditionally overwritten during restore (default: False).
                restore_as_copy (bool): If True, files will be restored as copies (default: False).
                skip_file_permissions (bool): If True, file permissions will not be restored (default: False).

        Returns:
            Job: Instance representing the restore job.

        Raises:
            SDKException: If input types are incorrect, job initialization fails, response is empty, or response is not successful.

        Example:
            >>> users = ['user1@domain.com', 'user2@domain.com']
            >>> destination = 'restoreuser@domain.com'
            >>> job = onedrive_client.out_of_place_restore(
            ...     users, destination, overwrite=True, restore_as_copy=False
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        _subclient_object = self._get_subclient()
        restore_job = _subclient_object.out_of_place_restore_onedrive_for_business_client(
            users, destination_path, **kwargs)
        return restore_job

    def disk_restore(self,
                     users: List[str],
                     destination_client: str,
                     destination_path: str,
                     skip_file_permissions: bool = False) -> 'Job':
        """Run a disk restore for specified OneDrive for Business users.

        This method initiates a disk restore operation for the given list of users, restoring their OneDrive data to the specified destination client and path. Optionally, file permissions can be skipped during the restore.

        Args:
            users: List of SMTP addresses representing the users to restore.
            destination_client: Name of the client where the users' data will be restored.
            destination_path: Destination folder path on the target client.
            skip_file_permissions: If True, file permissions will not be restored. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input types are incorrect, job initialization fails, or the restore response is empty or unsuccessful.

        Example:
            >>> users = ['user1@domain.com', 'user2@domain.com']
            >>> client = 'TargetClient01'
            >>> path = 'C:/RestoredData/OneDrive'
            >>> job = onedrive_client.disk_restore(users, client, path, skip_file_permissions=True)
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        _subclient_object = self._get_subclient()
        restore_job = _subclient_object.disk_restore_onedrive_for_business_client(users,
                                                                                  destination_client,
                                                                                  destination_path,
                                                                                  skip_file_permissions=skip_file_permissions)
        return restore_job

    def restore_to_azure_blob(self, users: List[str], blob_name: str) -> 'Job':
        """Restore OneDrive data for specified users to an Azure Blob storage.

        Args:
            users: List of SMTP addresses representing the users whose OneDrive data will be restored.
            blob_name: Name of the Azure Blob credential to which the restore will be performed.

        Returns:
            Job: A Job object representing the restore operation.

        Example:
            >>> users = ['user1@domain.com', 'user2@domain.com']
            >>> blob_name = 'AzureBlobCredential'
            >>> client = OneDriveClient(...)
            >>> restore_job = client.restore_to_azure_blob(users, blob_name)
            >>> print(f"Restore job started: {restore_job}")

        #ai-gen-doc
        """
        _subclient_object = self._get_subclient()
        restore_job = _subclient_object.restore_user_to_azure_blob(users, blob_name)
        return restore_job

    def modify_server_plan(self, old_plan: str, new_plan: str) -> None:
        """Modify the server plan associated with this OneDrive client.

        This method updates the server plan for the client by replacing the existing plan with a new one.

        Args:
            old_plan: The name of the existing server plan to be replaced.
            new_plan: The name of the new server plan to associate with the client.

        Example:
            >>> client = OneDriveClient(...)
            >>> client.modify_server_plan('OldServerPlan', 'NewServerPlan')
            >>> print("Server plan updated successfully")

        #ai-gen-doc
        """

        from ..plan import Plan
        entities = [{
            "clientName": self.client_name
        }]
        self.plan_obj = Plan(self._commcell_object, old_plan)
        self.plan_obj.edit_association(entities, new_plan)

    def modify_job_results_directory(self, modified_shared_jr_directory: str) -> None:
        """Modify the job results directory for the OneDrive client.

        Args:
            modified_shared_jr_directory: The new path for the job results directory as a string.

        Example:
            >>> client = OneDriveClient(...)
            >>> client.modify_job_results_directory('/mnt/shared/job_results')
            >>> # The job results directory is now updated to the specified path

        #ai-gen-doc
        """
        jr_update_dict = {
            "client": {
                "jobResulsDir": {
                    "path": modified_shared_jr_directory
                }
            }
        }

        self.update_properties(properties_dict=jr_update_dict)
