# -*- coding: utf-8 -*-
# pylint: disable=W0212,W0201
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

"""main file for performing disaster recovery operations on commcell

DisasterRecovery                :   Class for performing DR backup with various options.

DisasterRecoveryManagement      :   Class for performing disaster recovery management operations.

DisasterRecovery:
=================

    __init__()                    --    initializes DisasterRecovery class object

    reset_to_defaults()           --    resets the properties to default values

    disaster_recovery_backup()    --    function to run DR backup

    _process_drbackup_response()  --    process the disaster recovery backup request

    has_dr_copy()                 --    check if a specific DR backup copy is configured

    get_dr_copies()               --    get a list of all DR backup copies configured on the CommServe server

    add_dr_copy()                 --    add a DR backup copy to the CommServe server with the specified storage pool and retention settings.

    delete_dr_copy()              --    delete a DR backup copy from the CommServe server.

    restore_out_of_place()        --    function to run DR restore operation

    _advanced_dr_backup()         --    includes advance dr backup options

    _generatedrbackupjson()       --    Generate JSON corresponds to DR backup job

    _process_createtask_response()--    Runs the CreateTask API with the request JSON
                                        provided for DR backup.

    _filter_paths()               --    Filters the paths based on the Operating System and Agent.


DisasterRecovery Attributes
==========================

    **backuptype**                --    set or get backup type
    **is_compression_enabled**    --    set or get compression property
    **is_history_db_enabled**     --    set or get history db property
    **is_workflow_db_enabled**    --    set or get workflow db property
    **is_appstudio_db_enabled**   --    set or get appstudio db property
    **is_cvcloud_db_enabled**     --    set or get cvcloud db property
    **is_dm2_db_enabled**         --    set or get dm2db property
    **client_list**               --    set or get client list property.

DisasterRecoveryManagement:
==========================

    __init__()                          --   initializes DisasterRecoveryManagement class object

    _get_dr_properties()                --   Executes get request on server and retrives the dr settings

    _set_dr_properties()                --   Executes post request on server and sets the dr settings

    refresh()                           --   retrives the latest dr settings

    set_local_dr_path                   --   sets the local dr path

    set_network_dr_path                 --   sets the unc path

    upload_metdata_to_commvault_cloud   --   sets ths account to be used for commvault cloud backup.

    upload_metdata_to_cloud_library     --   sets the libarary to be used for cloud backup.

    impersonate_user                    --   account to be used for execution of pre/post scripts

    use_impersonate_user                --  gets the setting use_impersonate_user

DisasterRecoveryManagement Attributes:
=====================================

    **number_of_metadata**                  --  set or get number of metadata to be retained property
    **use_vss**                             --  set or get use vss property
    **wild_card_settings**                  --  set or get wild card settings property
    **backup_metadata_folder**              --  get backup metadata folder property
    **upload_backup_metadata_to_cloud**     --  get upload backup metadata to cloud property
    **upload_backup_metadata_to_cloud_lib** --  get upload backup metadata to cloud lib.
    **dr_storage_policy**                   --  set or get dr storage policy property
    **pre_scan_process**                    --  set or get pre scan process
    **post_scan_process**                   --  set or get post scan process
    **pre_backup_process**                  --  set or get pre backup process
    **post_backup_process**                 --  set or get post backup process
    **run_post_scan_process**               --  set or get run post scan process
    **run_post_backup_process**             --  set or get run post backup process

"""
from base64 import b64encode

from cvpysdk.policies.storage_policies import StoragePolicy, StoragePolicyCopy
from cvpysdk.storage import DiskLibrary
from .job import Job
from .exception import SDKException
from .client import Client
from .constants import AppIDAType
from .storage_pool import StorageType, StoragePoolType

from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
if TYPE_CHECKING:
    import requests
    from cvpysdk.commcell import Commcell


class DisasterRecovery(object):
    """
    DisasterRecovery class for managing disaster recovery operations on a CommCell.

    This class provides a comprehensive interface for performing disaster recovery tasks,
    including backup, restore, and configuration management. It supports both standard and
    advanced disaster recovery backups, out-of-place restores, and resetting configurations
    to default states. The class also offers various properties to manage and query backup
    settings, client lists, and database options relevant to disaster recovery.

    Key Features:
        - Perform disaster recovery backups (standard and advanced)
        - Restore data out-of-place with flexible options
        - Reset disaster recovery settings to defaults
        - Process backup and task responses
        - Generate disaster recovery backup JSON configurations
        - Filter paths for backup and restore operations
        - Manage client lists and backup types
        - Enable or disable compression and various database options
        - Access disaster recovery management properties

    #ai-gen-doc
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize a DisasterRecovery object with the given Commcell instance.

        Args:
            commcell: An instance of the Commcell class representing the connection to the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> dr = DisasterRecovery(commcell)
            >>> print("DisasterRecovery object initialized successfully")
        #ai-gen-doc
        """
        self.commcell = commcell
        self.client = Client(self.commcell, self.commcell.commserv_name)
        self.path = self.client.install_directory
        self._RESTORE = self.commcell._services['RESTORE']
        self._CREATE_TASK = self.commcell._services['CREATE_TASK']
        self._V4_DRBACKUP_BACKUP_DESTINATIONS = self.commcell._services['V4_DRBACKUP_BACKUP_DESTINATIONS']
        self._V4_DRBACKUP_BACKUP_DESTINATION_DELETE = self.commcell._services['V4_DRBACKUP_BACKUP_DESTINATION_DELETE']
        self._V4_DRBACKUP_STORAGE_POLICY = self.commcell._services['V4_DRBACKUP_STORAGE_POLICY']
        self.advbackup = False
        self._disaster_recovery_management = None
        self.reset_to_defaults()

    def reset_to_defaults(self) -> None:
        """Reset all instance variables of the DisasterRecovery object to their default values.

        This method restores the internal state of the DisasterRecovery instance, clearing any custom settings
        or modifications and returning all variables to their initial default values.

        #ai-gen-doc
        """
        self._backup_type = "full"
        self._is_compression_enabled = True
        self._is_history_db_enabled = True
        self._is_workflow_db_enabled = True
        self._is_appstudio_db_enabled = True
        self._is_cvcloud_db_enabled = True
        self._is_dm2_db_enabled = True
        self._client_list = None
        self.advanced_job_options = None

    def disaster_recovery_backup(self) -> Job:
        """Initiate a Disaster Recovery (DR) backup job for the CommServe server.

        This method starts a DR backup job, which is essential for protecting the CommServe database and configuration.
        The returned Job object can be used to monitor the status and progress of the backup operation.

        Returns:
            Job: An instance of the Job class representing the initiated DR backup job.

        Raises:
            SDKException: If the backup level specified is incorrect, if the response is empty, or if the response indicates failure.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr_job = dr.disaster_recovery_backup()
            >>> print(f"Started DR backup job with ID: {dr_job.job_id}")

        #ai-gen-doc
        """

        if self._backup_type.lower() not in ['full', 'differential']:
            raise SDKException('Response', '103')
        backuptypes = {"full": 1, "differential": 3}
        if self.advbackup:
            self._backup_type = backuptypes[self._backup_type.lower()]
            return self._advanced_dr_backup()
        dr_service = self.commcell._services['DRBACKUP']
        request_json = {"isCompressionEnabled": self._is_compression_enabled,
                        "jobType": 1, "backupType": backuptypes[self.backup_type.lower()]}
        flag, response = self.commcell._cvpysdk_object.make_request(
            'POST', dr_service, request_json
        )
        return self._process_drbackup_response(flag, response)

    def _process_drbackup_response(self, flag: str, response: 'requests.Response') -> Job:
        """Process the response from a Disaster Recovery (DR) backup operation.

        This method handles the results of a DR backup JSON request, validates the response,
        and returns a Job instance representing the initiated restore job.

        Args:
            flag: The result flag from the DR backup JSON request.
            response: The response string from the DR backup JSON request.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If job initialization fails, if the response is empty, or if the response indicates failure.

        #ai-gen-doc
        """
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self.commcell, response.json()['jobIds'][0])
                if "errorCode" in response.json():
                    o_str = 'Initializing backup failed\nError: "{0}"'.format(
                        response.json()['errorMessage']
                    )
                    raise SDKException('Response', '102', o_str)
            raise SDKException('Response', '102')
        response_string = self.commcell._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def restore_out_of_place(
            self,
            client: Union[str, Client],
            destination_path: str,
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: Optional[int] = None,
            from_time: Optional[str] = None,
            to_time: Optional[str] = None,
            fs_options: Optional[Dict[str, Any]] = None,
            restore_jobs: Optional[List[int]] = None
        ) -> Job:
        """Restore files or folders out-of-place to a specified client and destination path.

        This method initiates a restore operation for the given client, restoring the selected
        files or folders to the specified destination path. Advanced options such as overwrite,
        ACL restoration, copy precedence, time filters, and file system options can be configured.

        Args:
            client: The target client for restore. Can be the client name (str) or a Client object.
            destination_path: Full path on the client where data will be restored.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs will be restored. Default is True.
            copy_precedence: Optional copy precedence value for storage policy copy.
            from_time: Optional start time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional end time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            fs_options: Optional dictionary of advanced file system restore options, such as:
                - preserve_level: Level of folder structure to preserve.
                - proxy_client: Proxy client to use for restore.
                - impersonate_user: User to impersonate during restore.
                - impersonate_password: Base64-encoded password for impersonation.
                - all_versions: If True, restores all versions of the specified file.
                - versions: List of version numbers to restore.
            restore_jobs: Optional list of job IDs to restore (for index-free restore).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize.

        Example:
            >>> dr = DisasterRecovery()
            >>> job = dr.restore_out_of_place(
            ...     client='Client01',
            ...     destination_path='/restore/location',
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     copy_precedence=2,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-01-31 23:59:59',
            ...     fs_options={'preserve_level': 2, 'proxy_client': 'Proxy01'},
            ...     restore_jobs=[12345, 12346]
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not ((isinstance(client, (str, Client))
                 and isinstance(destination_path, str)
                 and isinstance(overwrite, bool) and isinstance(restore_data_and_acl, bool))):
            raise SDKException('Response', '101')

        if fs_options is None:
            fs_options = {}

        if isinstance(client, Client):
            client = client
        elif isinstance(client, str):
            client = Client(self.commcell, client)
        else:
            raise SDKException('Response', '105')

        agent_obj = client.agents.get("File System")
        drpath = self.path + "\\CommserveDR"
        destination_path = self._filter_paths([destination_path], True, agent_id=agent_obj.agent_id)
        drpath = [self._filter_paths([drpath], True, agent_id=agent_obj.agent_id)]
        if not drpath:
            raise SDKException('Response', '104')
        instance_obj = agent_obj.instances.get("DefaultInstanceName")

        instance_obj._restore_association = {
            "type": "0",
            "backupsetName": "DR-BackupSet",
            "instanceName": "DefaultInstanceName",
            "appName": "CommServe Management",
            "clientName": self.commcell.commserv_name,
            "consumeLicense": True,
            "clientSidePackage": True,
            "subclientName": ""
        }
        return instance_obj._restore_out_of_place(
            client,
            destination_path,
            paths=drpath,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            restore_jobs=restore_jobs)

    def get_dr_copies(self):
        """Get a mapping of the storage policies and DR backup copies configured on the CommServe server."""
        flag, response = self.commcell._cvpysdk_object.make_request('GET', self._V4_DRBACKUP_BACKUP_DESTINATIONS)
        if flag:
            if response.json():
                backup_destinations = response.json().get('backupdestinations', [])
            else:
                response_string = self.commcell._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException('DisasterRecovery', '102', 'Failed to retrieve DR backup copies')
        
        flag, response = self.commcell._cvpysdk_object.make_request('GET', self._V4_DRBACKUP_STORAGE_POLICY)
        if flag:
            if response.json():
                storage_policy_name = response.json().get('name', '')
            else:
                response_string = self.commcell._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException('DisasterRecovery', '102', 'Failed to retrieve storage policies for DR backup copies')
        
        # Extract name and copy id from each backup destination
        processed_destinations = []
        for destination in backup_destinations:
            if 'planBackupDestination' in destination:
                copy_name = destination['planBackupDestination'].get('name')
                copy_id = destination['planBackupDestination'].get('id')
                if copy_name and copy_id:
                    processed_destinations.append({copy_name: copy_id})
        
        dr_copies = {'StoragePolicy': storage_policy_name, 'BackupDestinations': processed_destinations}
        return dr_copies

    def has_dr_copy(self, copy_name) -> bool:
        """Check if a specific DR backup copy is configured on the CommServe server.
        
        Args:
        
            copy_name: The name of the DR backup copy to check for existence."""
        
        copies = self.get_dr_copies()
        return any(copy_name in destination for destination in copies['BackupDestinations'])

    def add_dr_copy(self, copy_name: str, storage_pool: str, retention: int=0, extended_retention: dict=None) -> 'StoragePolicyCopy':
        """Add a DR backup copy to the CommServe server with the specified storage pool and retention settings.

        This method creates a new DR backup copy using the provided parameters, allowing for additional redundancy
        and protection of the CommServe database. The copy will be associated with the specified storage pool and
        configured with the given retention settings.

        Args:
            copy_name: The name for the new DR backup copy.
            storage_pool: The name of the storage pool where the DR backup copy will be stored.
            retention: Retention period in days for the DR backup copy. Default is 0 (no retention).
            extended_retention: Optional dictionary specifying extended retention rules for the DR backup copy. 

        Raises:
            SDKException: If input parameters are invalid or if adding the DR backup copy fails.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.add_dr_copy(
            ...     copy_name='DR_Copy_01',
            ...     storage_pool='StoragePool01',
            ...     retention=30,
            ...     extended_retention={
            ...     "firstExtendedRetentionRule": {
                    "isInfiniteRetention": False,
                    "type": "WEEKLY_FULLS",
                    "retentionPeriodDays": 90
                    },
            ...     "secondExtendedRetentionRule": {
                    "type": "MONTHLY_FULLS",
                    "retentionPeriodDays": 365,
                    "isInfiniteRetention": False
                    },
            ...     "thirdExtendedRetentionRule": {
                    "type": "YEARLY_FULLS",
                    "retentionPeriodDays": 1825,
                    "isInfiniteRetention": False
                }
            }
            >>> print("DR backup copy added successfully")

        #ai-gen-doc
        """
        #Make changes for defaults if its Tape pool
        copy_payload = {"backupDestinationName": copy_name, "overrideRetentionSettings": True, "backupStartTime": -1, "useExtendedRetentionRules": False}
        storage_pool_obj = self.commcell.storage_pools.get(storage_pool)
        copy_payload['storagePool'] = {"id": int(storage_pool_obj.storage_pool_id), "name": storage_pool_obj.storage_pool_name}
        if storage_pool_obj.storage_type == StorageType.TAPE.value:
            copy_payload['storagePool']['type'] = StoragePoolType.SECONDARY_COPY.value #To fetch maxstreamNums from the pool to inherit in copy
            if retention: # If retention is provided, use it
                copy_payload['retentionPeriodDays'] = retention
            else:
                copy_payload.update({'overrideRetentionSettings': False})
                copy_payload['retentionPeriodDays'] = storage_pool_obj.get_copy().copy_retention['days']  # Default retention -> inherit from tape pools
            copy_payload['backupsToCopy'] = "MONTHLY_FULLS" # Default backups to copy for tape pools
            copy_payload['fullBackupTypesToCopy'] = "LAST"  # Default full backup types to copy for tape pools
        else:
            if retention:
                copy_payload['retentionPeriodDays'] = retention
            else:
                copy_payload['retentionPeriodDays'] = 30  # Default retention for non-tape pools
        if storage_pool_obj.is_worm_storage_lock_enabled: #copies inhering worm pools should not be overriding pool retention
            if 'retentionPeriodDays' in copy_payload:
                del copy_payload['retentionPeriodDays']
            copy_payload.update({'overrideRetentionSettings': False})
        if extended_retention:
            if (storage_pool_obj.storage_type == StorageType.TAPE.value or storage_pool_obj.is_worm_storage_lock_enabled) and retention is None:
                raise SDKException('Plan', '102', 'Retention period days must be specified when adding extended retention rules for Tape storage pool')
            copy_payload.update({'useExtendedRetentionRules': True})
            copy_payload.update({"extendedRetentionRules": extended_retention})

        request_json = {
            'destinations': [copy_payload]
        }
        flag, response = self.commcell._cvpysdk_object.make_request('POST', self._V4_DRBACKUP_BACKUP_DESTINATIONS, request_json)

        dr_copies = self.get_dr_copies()
        storage_policy = dr_copies['StoragePolicy']
        if flag:
            if response.json():
                response_json = response.json()
                if "planBackupDestination" in response_json and len(response_json['planBackupDestination']) > 0:
                    return StoragePolicyCopy(self.commcell, storage_policy, response_json['planBackupDestination'][0]['name'])
                if "errorCode" in response_json and response_json['errorCode'] != 0:
                    error_message = response_json['errorMessage']
                    o_str = 'Adding DR backup copy failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Response', '102', o_str)
            else:
                response_string = self.commcell._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
            
    def delete_dr_copy(self, copy: Union[str, StoragePolicyCopy, int]) -> None:
        """Delete a DR backup copy from the CommServe server.

        This method removes the specified DR backup copy, which can help manage storage resources and maintain
        an organized set of backup copies. The copy to be deleted can be identified by its name or by providing
        a StoragePolicyCopy object.

        Args:
            copy: The DR backup copy to delete. Can be the copy name (str) or a StoragePolicyCopy object.

        Raises:
            SDKException: If the specified copy does not exist or if the deletion operation fails.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.delete_dr_copy('DR_Copy_01')
            >>> print("DR backup copy deleted successfully")

        #ai-gen-doc
        """
        dr_copies = self.get_dr_copies()
        storage_policy = dr_copies['StoragePolicy']
        if isinstance(copy, StoragePolicyCopy):
            copy_id = copy.copy_id
        elif isinstance(copy, str):
            copy_id = StoragePolicyCopy(self.commcell, storage_policy, copy).copy_id
        elif isinstance(copy, int):
            copy_id = copy
        else:
            raise SDKException('DisasterRecovery', '101')

        flag, response = self.commcell._cvpysdk_object.make_request('DELETE', self._V4_DRBACKUP_BACKUP_DESTINATION_DELETE % copy_id)

        if flag:
            if response.json():
                response_json = response.json()
                if "errorCode" in response_json and response_json['errorCode'] != 0:
                    error_message = response_json['errorMessage']
                    o_str = 'Deleting DR backup copy failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Response', '102', o_str)
            else:
                response_string = self.commcell._update_response_(response.text)
                raise SDKException('Response', '101', response_string)

    def _advanced_dr_backup(self) -> Job:
        """Run an advanced Disaster Recovery (DR) backup job using JSON input.

        This method initiates a DR backup job and returns an instance of the Job class representing the backup operation.

        Returns:
            Job: An instance of the Job class for the initiated backup job.

        Raises:
            SDKException: If the backup level specified is incorrect, if the response is empty, or if the response indicates failure.

        #ai-gen-doc
        """
        request_json = self._generatedrbackupjson()
        return self._process_createtask_response(request_json)

    def _generatedrbackupjson(self) -> dict:
        """Generate a JSON dictionary corresponding to a Disaster Recovery (DR) backup job.

        Returns:
            dict: A dictionary representing the DR backup job in JSON format.

        #ai-gen-doc
        """
        try:
            self._task = {
                "taskFlags": {"disabled": False},
                "policyType": "DATA_PROTECTION",
                "taskType": "IMMEDIATE",
                "initiatedFrom": 1
            }
            self._subtask = {
                "subTaskType": "ADMIN",
                "operationType": "DRBACKUP"
            }
            clientdict = []
            if self._client_list is not None:
                for client in self._client_list:
                    client = {
                        "type": 0,
                        "clientName": client,
                        "clientSidePackage": True,
                        "consumeLicense": True}
                    clientdict.append(client)

            common_opts = None
            if self.advanced_job_options:
                common_opts = {
                    "startUpOpts": {
                        "priority": self.advanced_job_options.get("priority", 66),
                        "startInSuspendedState": self.advanced_job_options.get("start_in_suspended_state", False),
                        "startWhenActivityIsLow": self.advanced_job_options.get("start_when_activity_is_low", False),
                        "useDefaultPriority": self.advanced_job_options.get("use_default_priority", True)
                    },
                    "jobRetryOpts": {
                        "runningTime": {
                            "enableTotalRunningTime": self.advanced_job_options.get(
                                "enable_total_running_time", False),
                            "totalRunningTime": self.advanced_job_options.get("total_running_time", 3600)
                        },
                        "enableNumberOfRetries": self.advanced_job_options.get("enable_number_of_retries", False),
                        "killRunningJobWhenTotalRunningTimeExpires": self.advanced_job_options.get(
                            "kill_running_job_when_total_running_time_expires", False),
                        "numberOfRetries": self.advanced_job_options.get("number_of_retries", 0)
                    },
                    "jobDescription": self.advanced_job_options.get("job_description", "")
                }

            self._droptions = {
                "drbackupType": self._backup_type, "dbName": "commserv",
                "backupHistoryDataBase": self.is_history_db_enabled,
                "backupWFEngineDataBase": self.is_workflow_db_enabled,
                "backupAppStudioDataBase": self.is_appstudio_db_enabled,
                "backupCVCloudDataBase": self.is_cvcloud_db_enabled,
                "backupDM2DataBase": self.is_dm2_db_enabled,
                "enableDatabasesBackupCompression": self.is_compression_enabled,
                "client": clientdict

            }

            request_json = {
                "taskInfo":
                {
                    "task": self._task,
                    "subTasks":
                    [{
                        "subTaskOperation": 1,
                        "subTask": self._subtask,
                        "options":
                        {
                            "adminOpts":
                            {
                                "drBackupOption": self._droptions,
                                "contentIndexingOption":
                                {
                                    "subClientBasedAnalytics": False
                                }
                            },
                            "restoreOptions":
                            {
                                "virtualServerRstOption":
                                {
                                    "isBlockLevelReplication": False
                                }
                            }
                        }
                    }
                    ]
                }
            }

            if self.advanced_job_options:
                request_json["taskInfo"]["subTasks"][0]["options"]["commonOpts"] = common_opts

            return request_json
        except Exception as err:
            raise SDKException('Response', '101', err)

    def _process_createtask_response(self, request_json: dict) -> Job:
        """Execute the CreateTask API for DR backup and parse the response.

        This method sends the provided JSON request to the CreateTask API for disaster recovery backup,
        processes the response, and returns a Job object representing the restore job.

        Args:
            request_json: Dictionary containing the JSON request payload for the CreateTask API.

        Returns:
            Job: An instance of the Job class representing the initiated restore job.

        Raises:
            SDKException: If the restore job fails, the response is empty, or the response indicates failure.

        #ai-gen-doc
        """
        flag, response = self.commcell._cvpysdk_object.make_request(
            'POST', self._CREATE_TASK, request_json
        )
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self.commcell, response.json()['jobIds'][0])
                if "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'DR backup job failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Response', '102', o_str)
                raise SDKException(
                    'Response', '102', 'Failed to run the DR backup job')
            raise SDKException('Response', '102')
        response_string = self.commcell._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _filter_paths(self, paths: list, is_single_path: bool = False, agent_id: str = None) -> Union[list, str]:
        """Filter the provided paths based on the operating system and agent.

        Args:
            paths: List of file or directory paths to be filtered.
            is_single_path: If True, return only a single filtered path as a string. If False, return a list of filtered paths.
            agent_id: Optional file system agent ID used for filtering.

        Returns:
            list: A list of filtered paths if is_single_path is False.
            str: A single filtered path if is_single_path is True.

        Example:
            >>> dr = DisasterRecovery()
            >>> filtered_list = dr._filter_paths(['/data', '/backup'], is_single_path=False)
            >>> print(filtered_list)
            ['/data', '/backup']
            >>> single_path = dr._filter_paths(['/data', '/backup'], is_single_path=True)
            >>> print(single_path)
            '/data'

        #ai-gen-doc
        """
        for index, path in enumerate(paths):
            # "if" condition is default i.e. if client is not provided
            if agent_id is None or int(agent_id) == AppIDAType.WINDOWS_FILE_SYSTEM.value:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('/', '\\')
                else:
                    path = '\\'
            elif int(agent_id) == AppIDAType.LINUX_FILE_SYSTEM.value:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('\\', '/')
                else:
                    path = '\\'
                path = '/' + path
            paths[index] = path

        if is_single_path:
            return paths[0]
        return paths

    @property
    def client_list(self) -> list:
        """Get the list of clients associated with the DisasterRecovery instance as a read-only property.

        Returns:
            list: A list containing the client names or client objects managed by this DisasterRecovery instance.

        Example:
            >>> dr = DisasterRecovery()
            >>> clients = dr.client_list  # Access the client list property
            >>> print(f"Number of clients: {len(clients)}")
            >>> for client in clients:
            ...     print(client)
        #ai-gen-doc
        """
        return self._client_list

    @client_list.setter
    def client_list(self, value: list) -> None:
        """Attempting to set the client_list attribute is not allowed.

        Args:
            value: The value attempted to be assigned to client_list (ignored).

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.client_list = ['ClientA', 'ClientB']  # This will not change the client_list

        #ai-gen-doc
        """
        if isinstance(value, list):
            self._client_list = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_compression_enabled(self) -> bool:
        """Indicate whether compression is enabled for disaster recovery operations.

        Returns:
            bool: True if compression is enabled, False otherwise.

        Example:
            >>> dr = DisasterRecovery()
            >>> if dr.is_compression_enabled:
            ...     print("Compression is enabled for disaster recovery.")
            ... else:
            ...     print("Compression is not enabled for disaster recovery.")

        #ai-gen-doc
        """
        return self._is_compression_enabled

    @is_compression_enabled.setter
    def is_compression_enabled(self, value: bool) -> None:
        """Attempt to set the is_compression_enabled property.

        Note:
            This property is read-only and cannot be set directly. 
            Any attempt to assign a value to this property will have no effect.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.is_compression_enabled = True  # This will not change the property value

        #ai-gen-doc
        """
        if isinstance(value, bool):
            self._is_compression_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def backup_type(self) -> str:
        """Get the backup type for the DisasterRecovery instance as a read-only property.

        Returns:
            The backup type as a string.

        Example:
            >>> dr = DisasterRecovery()
            >>> current_type = dr.backup_type  # Access the backup type property
            >>> print(f'Disaster Recovery backup type: {current_type}')
        #ai-gen-doc
        """
        return self._backup_type

    @backup_type.setter
    def backup_type(self, value: str) -> None:
        """Attempting to set the backup_type attribute is not allowed.

        This property is read-only and cannot be modified directly. Any attempt to set
        the backup_type will be ignored or may raise an exception, depending on implementation.

        Args:
            value: The attempted value for backup_type (ignored).

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.backup_type = "Full"  # This will not change the backup_type attribute

        #ai-gen-doc
        """
        if isinstance(value, str):
            self._backup_type = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_history_db_enabled(self) -> bool:
        """Indicate whether the history database is enabled for disaster recovery.

        Returns:
            bool: True if the history database is enabled, False otherwise.

        Example:
            >>> dr = DisasterRecovery()
            >>> if dr.is_history_db_enabled:
            ...     print("History database is enabled for disaster recovery.")
            ... else:
            ...     print("History database is not enabled.")

        #ai-gen-doc
        """
        return self._is_history_db_enabled

    @is_history_db_enabled.setter
    def is_history_db_enabled(self, value: bool) -> None:
        """Set the value indicating whether the history database is enabled.

        Args:
            value: Set to True to enable the history database, or False to disable it.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.is_history_db_enabled = True  # Enable the history database
            >>> dr.is_history_db_enabled = False  # Disable the history database

        #ai-gen-doc
        """
        if isinstance(value, bool):
            self._is_history_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_workflow_db_enabled(self) -> bool:
        """Indicate whether the Workflow Database (workflowdb) is enabled for disaster recovery.

        Returns:
            bool: True if the workflowdb is enabled; False otherwise.

        Example:
            >>> dr = DisasterRecovery(commcell_object)
            >>> if dr.is_workflow_db_enabled:
            ...     print("Workflow DB is enabled for disaster recovery.")
            ... else:
            ...     print("Workflow DB is not enabled.")

        #ai-gen-doc
        """
        return self._is_workflow_db_enabled

    @is_workflow_db_enabled.setter
    def is_workflow_db_enabled(self, value: bool) -> None:
        """Set the workflow database enabled status for disaster recovery.

        Args:
            value: Set to True to enable the workflow database, or False to disable it.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.is_workflow_db_enabled = True  # Enable the workflow database
            >>> dr.is_workflow_db_enabled = False  # Disable the workflow database

        #ai-gen-doc
        """
        if isinstance(value, bool):
            self._is_workflow_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_appstudio_db_enabled(self) -> bool:
        """Indicate whether the AppStudio workflow database is enabled.

        This property provides a read-only boolean value that specifies if the AppStudio workflow database 
        feature is currently enabled in the DisasterRecovery configuration.

        Returns:
            True if the AppStudio workflow database is enabled; False otherwise.

        Example:
            >>> dr = DisasterRecovery(commcell_object)
            >>> if dr.is_appstudio_db_enabled:
            ...     print("AppStudio workflow database is enabled.")
            ... else:
            ...     print("AppStudio workflow database is not enabled.")

        #ai-gen-doc
        """
        return self._is_appstudio_db_enabled

    @is_appstudio_db_enabled.setter
    def is_appstudio_db_enabled(self, value: bool) -> None:
        """Set the AppStudio database enabled status for disaster recovery.

        Args:
            value: Boolean value indicating whether the AppStudio database is enabled (True) or disabled (False).

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.is_appstudio_db_enabled = True  # Enable AppStudio database
            >>> dr.is_appstudio_db_enabled = False  # Disable AppStudio database

        #ai-gen-doc
        """
        if isinstance(value, bool):
            self._is_appstudio_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_cvcloud_db_enabled(self) -> bool:
        """Indicate whether the cvclouddb feature is enabled.

        This property provides a read-only boolean value that specifies if the cvclouddb 
        (Commvault Cloud Database) is currently enabled for disaster recovery operations.

        Returns:
            True if cvclouddb is enabled; False otherwise.

        Example:
            >>> dr = DisasterRecovery()
            >>> if dr.is_cvcloud_db_enabled:
            ...     print("cvclouddb is enabled for disaster recovery.")
            ... else:
            ...     print("cvclouddb is not enabled.")

        #ai-gen-doc
        """
        return self._is_cvcloud_db_enabled

    @is_cvcloud_db_enabled.setter
    def is_cvcloud_db_enabled(self, value: bool) -> None:
        """Set the value indicating whether the CVCloud database is enabled.

        Args:
            value: True to enable the CVCloud database, or False to disable it.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.is_cvcloud_db_enabled = True  # Enable the CVCloud database
            >>> dr.is_cvcloud_db_enabled = False  # Disable the CVCloud database

        #ai-gen-doc
        """
        if isinstance(value, bool):
            self._is_cvcloud_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_dm2_db_enabled(self) -> bool:
        """Indicate whether the DM2 database is enabled for disaster recovery.

        This property provides a read-only boolean value that specifies if the DM2 database 
        feature is currently enabled in the disaster recovery configuration.

        Returns:
            True if the DM2 database is enabled; False otherwise.

        Example:
            >>> dr = DisasterRecovery()
            >>> if dr.is_dm2_db_enabled:
            ...     print("DM2 database is enabled for disaster recovery.")
            ... else:
            ...     print("DM2 database is not enabled.")

        #ai-gen-doc
        """
        return self._is_dm2_db_enabled

    @is_dm2_db_enabled.setter
    def is_dm2_db_enabled(self, value: bool) -> None:
        """Set the value indicating whether DM2 database is enabled for disaster recovery.

        Args:
            value: True to enable DM2 database, False to disable it.

        Example:
            >>> dr = DisasterRecovery()
            >>> dr.is_dm2_db_enabled = True  # Enable DM2 database
            >>> dr.is_dm2_db_enabled = False  # Disable DM2 database

        #ai-gen-doc
        """
        if isinstance(value, bool):
            self._is_dm2_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def disaster_recovery_management(self) -> 'DisasterRecoveryManagement':
        """Get the DisasterRecoveryManagement instance associated with this DisasterRecovery object.

        Returns:
            DisasterRecoveryManagement: An instance for managing disaster recovery operations.

        Example:
            >>> dr = DisasterRecovery(commcell_object)
            >>> dr_management = dr.disaster_recovery_management  # Access the property
            >>> print(f"Disaster Recovery Management object: {dr_management}")
            >>> # The returned DisasterRecoveryManagement object can be used for further disaster recovery tasks

        #ai-gen-doc
        """
        if self._disaster_recovery_management is None:
            self._disaster_recovery_management = DisasterRecoveryManagement(self.commcell)
        return self._disaster_recovery_management


class DisasterRecoveryManagement(object):
    """
    DisasterRecoveryManagement provides a comprehensive interface for managing disaster recovery operations on a CommCell.

    This class enables configuration, monitoring, and execution of disaster recovery processes, including backup metadata management, cloud integration, storage policy assignment, and process automation. It supports both local and network disaster recovery paths, cloud region management, and user impersonation for secure operations.

    Key Features:
        - Retrieve and set disaster recovery properties
        - Manage disaster recovery backup options
        - Configure and refresh disaster recovery settings
        - Set local and network disaster recovery paths with credential support
        - Upload metadata to Commvault Cloud and cloud libraries
        - Manage cloud regions and enable/disable cloud uploads
        - Impersonate users for secure operations
        - Access and modify properties such as region, number of metadata, VSS usage, wild card settings, backup metadata folder, and storage policy
        - Configure pre/post scan and backup processes, with options to run them automatically

    Usage:
        Instantiate with a CommCell object to perform disaster recovery management tasks, including property configuration, cloud integration, and process automation.

    #ai-gen-doc
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize a DisasterRecoveryManagement object.

        Args:
            commcell: An instance of the Commcell class representing the Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> drm = DisasterRecoveryManagement(commcell)
            >>> print("DisasterRecoveryManagement object created successfully")

        #ai-gen-doc
        """
        self._commcell = commcell
        self.services = self._commcell._services
        self._service = self.services['DISASTER_RECOVERY_PROPERTIES']
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self.refresh()

    def _get_dr_properties(self) -> None:
        """Retrieve the disaster recovery backup settings from the server.

        This method sends a request to the server to obtain the current configuration
        and properties related to disaster recovery backup. It updates the internal
        state of the DisasterRecoveryManagement object with the retrieved settings.

        Raises:
            SDKException: If the server response is empty or indicates a failure.

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(method='GET', url=self._service)
        if flag:
            if response and response.json():
                self._settings_dict = response.json()
                if self._settings_dict.get('errorCode', 0) != 0:
                    raise SDKException('Job', '102', 'Failed to get dr management properties. \nError: {0}'.format(
                        self._settings_dict.get('errorMessage', '')))
                if 'drBackupInfo' in self._settings_dict:
                    self._prepost_settings = self._settings_dict.get('drBackupInfo').get('prePostProcessSettings', {})
                    self._export_settings = self._settings_dict.get('drBackupInfo').get('exportSettings', {})
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _set_dr_properties(self) -> None:
        """Send a request to the server to configure disaster recovery (DR) settings.

        This method updates the DR properties on the server. It should be called after
        setting the desired DR configuration parameters on the DisasterRecoveryManagement object.

        Raises:
            SDKException: If the provided inputs for DR settings are invalid.

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request(method='POST', url=self._service,
                                                           payload=self._settings_dict)
        if flag:
            if response and response.json():
                if response.json().get('response') and response.json().get('response')[0].get('errorCode') != 0:
                    raise SDKException('DisasterRecovery', '102', 'Failed to set dr properties. Error: {0}'.format(
                        response.json().get('response')[0].get('errorString')
                    ))
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def _get_drbackup_options(self) -> dict:
        """Retrieve the disaster recovery (DR) backup options as a dictionary.

        Returns:
            dict: A dictionary containing the DR backup configuration options.

        Example:
            >>> dr_mgmt = DisasterRecoveryManagement()
            >>> dr_options = dr_mgmt._get_drbackup_options()
            >>> print(dr_options)
            {'backup_frequency': 'daily', 'retention_days': 30, ...}
        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            method='GET',
            url=self.services['DISASTER_RECOVERY_OPTIONS']
        )
        if flag:
            if response and response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def get_cloud_regions(self) -> dict:
        """Retrieve the available disaster recovery (DR) backup cloud regions.

        Returns:
            dict: A dictionary containing the default DR region and a list of available regions.
                Example structure:
                    {
                        "defaultRegion": "southindia",
                        "regions": [
                            {
                                "regionCode": "eastus2",
                                "displayName": "East US 2"
                            },
                            {
                                "regionCode": "southindia",
                                "displayName": "(Asia Pacific) South India"
                            }
                        ]
                    }

        Example:
            >>> dr_mgmt = DisasterRecoveryManagement()
            >>> regions_info = dr_mgmt.get_cloud_regions()
            >>> print(f"Default region: {regions_info['defaultRegion']}")
            >>> for region in regions_info['regions']:
            ...     print(f"Region code: {region['regionCode']}, Name: {region['displayName']}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            method='GET',
            url=self.services['DRBACKUP_REGIONS']
        )
        if flag:
            if response and response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def _set_commvault_cloud_upload(self, flag: bool, region: Optional[str] = None) -> None:
        """Set the disaster recovery (DR) settings for Commvault Cloud upload.

        This method sends a request to the server to enable or disable Commvault Cloud upload for DR backups.
        Optionally, a specific region can be selected for the DR backup upload. If no region is provided,
        the default region will be used.

        Args:
            flag: Set to True to enable Commvault Cloud upload, or False to disable it.
            region: Optional; the region to which the DR backup should be uploaded. If None, the default region is used.

        Raises:
            SDKException: If the provided inputs are invalid.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm._set_commvault_cloud_upload(True, region="us-east-1")
            >>> # Enables Commvault Cloud upload for DR backups to the 'us-east-1' region
            >>>
            >>> drm._set_commvault_cloud_upload(False)
            >>> # Disables Commvault Cloud upload for DR backups

        #ai-gen-doc
        """
        current_options = self._get_drbackup_options()
        current_options['properties']['uploadBackupMetadataToCloud'] = flag
        if flag:
            current_options['properties']['region'] = region if region else self.get_cloud_regions()['defaultRegion']

        flag, response = self._cvpysdk_object.make_request(
                                    method='POST',
                                    url=self.services['DISASTER_RECOVERY_OPTIONS'],
                                    payload=current_options
                                )
        if flag:
            if response and response.json():
                if response.json().get('errorCode') != 0:
                    raise SDKException('DisasterRecovery', '102', 'Failed to set dr properties. Error: {0}'.format(
                        response.json().get('errorMessage')
                    ))
                self.refresh()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def refresh(self) -> None:
        """Refresh the disaster recovery (DR) settings associated with the Commcell.

        This method reloads the DR configuration, ensuring that the latest settings 
        from the Commcell are applied.

        #ai-gen-doc
        """
        self._prepost_settings = None
        self._export_settings = None
        self._get_dr_properties()

    def set_local_dr_path(self, path: str) -> None:
        """Set the local Disaster Recovery (DR) path.

        This method configures the local path where Disaster Recovery files will be stored.

        Args:
            path: The local filesystem path to be used for Disaster Recovery storage.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.set_local_dr_path('/var/commvault/dr')
            >>> print("Local DR path set successfully")

        #ai-gen-doc
        """
        if isinstance(path, str):
            self._export_settings['backupMetadataFolder'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def set_network_dr_path(self, path: str, credential_name: str) -> None:
        """Set the network Disaster Recovery (DR) path using a specified credential.

        This method configures the UNC (Universal Naming Convention) path for network-based disaster recovery
        and associates it with a credential for authentication.

        Args:
            path: The UNC path to be used for network DR (e.g., '\\\\server\\share\\dr').
            credential_name: The name of the credential to use for accessing the specified UNC path.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.set_network_dr_path('\\\\backupserver\\drshare', 'DR_Credential')
            >>> print("Network DR path set successfully.")

        #ai-gen-doc
        """
        if isinstance(path, str) and isinstance(credential_name, str):
            self._export_settings['backupMetadataFolder'] = path
            dr_backup_credential = {
                "credentialId": self._commcell.credentials.get(credential_name).credential_id,
                "credentialName": credential_name
            }
            self._export_settings['drBackupCredential'] = dr_backup_credential
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def upload_metdata_to_commvault_cloud(self, flag: bool, username: str = None, password: str = None, region: str = None) -> None:
        """Enable or disable the upload of metadata to Commvault Cloud.

        This method configures whether disaster recovery (DR) metadata should be uploaded to Commvault Cloud.
        Optionally, you can specify the cloud account credentials and the region for the upload.

        Args:
            flag: Set to True to enable metadata upload, or False to disable it.
            username: (Optional) Username for the Commvault Cloud account.
            password: (Optional) Password for the Commvault Cloud account.
            region: (Optional) Cloud region to upload the DR backup metadata. If None, the default region is used.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.upload_metdata_to_commvault_cloud(
            ...     flag=True,
            ...     username="cloud_user",
            ...     password="secure_password",
            ...     region="us-east-1"
            ... )
            >>> # This enables metadata upload to Commvault Cloud in the specified region.

            >>> drm.upload_metdata_to_commvault_cloud(flag=False)
            >>> # This disables metadata upload to Commvault Cloud.

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            self._export_settings['uploadBackupMetadataToCloud'] = flag
            if flag:
                if region and isinstance(region, str):
                    self._export_settings['region'] = region
                else:
                    raise SDKException('DisasterRecovery', '101')
                if isinstance(username, str) and isinstance(password, str):
                    self._export_settings['cloudCredentials']['userName'] = username
                    self._export_settings['cloudCredentials']['password'] = b64encode(password.encode()).decode()
                else:
                    raise SDKException('DisasterRecovery', '101')
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def upload_metdata_to_cloud_library(self, flag: bool, libraryname: object = None) -> None:
        """Enable or disable the upload of metadata to a cloud library.

        This method allows you to control whether metadata is uploaded to a specified third-party cloud library.
        You can enable or disable this feature by setting the `flag` parameter.

        Args:
            flag: Set to True to enable metadata upload, or False to disable it.
            libraryname: The name of the third-party cloud library as a string, or a disklibrary object. If not specified, the default library is used.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.upload_metdata_to_cloud_library(True, libraryname="MyCloudLibrary")
            >>> # Disables metadata upload for the default library
            >>> drm.upload_metdata_to_cloud_library(False)

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            self._export_settings['uploadBackupMetadataToCloudLib'] = flag
            if flag:
                if isinstance(libraryname, str):
                    cloud_lib_obj = DiskLibrary(self._commcell, library_name=libraryname)
                elif isinstance(libraryname, DiskLibrary):
                    cloud_lib_obj = libraryname
                else:
                    raise SDKException('DisasterRecovery', '101')
                self._export_settings['cloudLibrary']['libraryName'] = cloud_lib_obj.name
                self._export_settings['cloudLibrary']['libraryId'] = int(cloud_lib_obj.library_id)
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def impersonate_user(self, flag: bool, username: str, password: str) -> None:
        """Enable or disable the impersonate user option for pre/post scripts.

        This method allows you to enable or disable the impersonation of a user with administrative privileges
        when running pre/post scripts in disaster recovery operations.

        Args:
            flag: Set to True to enable impersonation, or False to disable it.
            username: The username of the account with administrative privileges to impersonate.
            password: The password for the specified administrative account.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.impersonate_user(True, "admin_user", "secure_password")
            >>> # Impersonation is now enabled for pre/post scripts

            >>> drm.impersonate_user(False, "admin_user", "secure_password")
            >>> # Impersonation is now disabled for pre/post scripts

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            self._prepost_settings['useImpersonateUser'] = flag
            if flag:
                if isinstance(username, str) and isinstance(password, str):
                    self._prepost_settings['impersonateUser']['userName'] = username
                    self._prepost_settings['impersonateUser']['password'] = b64encode(password.encode()).decode()
                else:
                    raise SDKException('DisasterRecovery', '101')
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def use_impersonate_user(self) -> bool:
        """Indicate whether the impersonate user feature is enabled.

        Returns:
            True if impersonate user is enabled; False otherwise.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> if drm.use_impersonate_user:
            ...     print("Impersonate user is enabled.")
            ... else:
            ...     print("Impersonate user is disabled.")

        #ai-gen-doc
        """
        return self._prepost_settings.get('useImpersonateUser')

    @property
    def region(self) -> str:
        """Get the current region configured for uploading Disaster Recovery (DR) backups.

        Returns:
            The name of the region as a string where DR backups are uploaded.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> current_region = drm.region
            >>> print(f"DR backups are uploaded to region: {current_region}")

        #ai-gen-doc
        """
        return self._get_drbackup_options()['properties']['region']

    @property
    def number_of_metadata(self) -> int:
        """Get the number of metadata folders to be retained.

        Returns:
            The number of metadata folders (as an integer) that are configured to be retained.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> num_metadata = drm.number_of_metadata
            >>> print(f"Number of metadata folders to retain: {num_metadata}")

        #ai-gen-doc
        """
        return self._export_settings.get('numberOfMetadata')

    @number_of_metadata.setter
    def number_of_metadata(self, value: int) -> None:
        """Set the number of metadata folders to be retained for disaster recovery.

        Args:
            value: The number of metadata folders to retain.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.number_of_metadata = 5  # Retain 5 metadata folders

        #ai-gen-doc
        """
        if isinstance(value, int):
            self._export_settings['numberOfMetadata'] = value
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def use_vss(self) -> bool:
        """Indicate whether VSS (Volume Shadow Copy Service) is enabled for disaster recovery operations.

        Returns:
            bool: True if VSS is enabled, False otherwise.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> if drm.use_vss:
            ...     print("VSS is enabled for disaster recovery.")
            ... else:
            ...     print("VSS is not enabled for disaster recovery.")

        #ai-gen-doc
        """
        return self._export_settings.get('isUseVSS')

    @use_vss.setter
    def use_vss(self, flag: bool) -> None:
        """Set the 'use_vss' flag for disaster recovery operations.

        Args:
            flag: Boolean value indicating whether to enable (True) or disable (False) the use of VSS (Volume Shadow Copy Service).

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.use_vss = True  # Enable VSS
            >>> drm.use_vss = False  # Disable VSS

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            self._export_settings['isUseVSS'] = flag
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def wild_card_settings(self) -> str:
        """Get the wild card settings for client logs to be backed up.

        Returns:
            A string representing the client log wild card settings that determine which logs are included in the backup.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> settings = drm.wild_card_settings
            >>> print(f"Wild card settings: {settings}")

        #ai-gen-doc
        """
        return self._export_settings.get('wildCardSetting')

    @wild_card_settings.setter
    def wild_card_settings(self, logs: list) -> None:
        """Set the wild card settings for log file names.

        Args:
            logs: A list of log file names to be used as wild card settings.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.wild_card_settings = ['log1.txt', 'log2.txt']
            >>> # The wild card settings are now updated with the specified log files

        #ai-gen-doc
        """
        mandatory = "cvd;SIDBPrune;SIDBEngine;CVMA"
        if isinstance(logs, list):
            temp = ''
            for log in logs:
                temp = temp + ';' + log
        else:
            raise Exception('Pass log names in list')
        self._export_settings['wildCardSetting'] = mandatory + temp
        self._set_dr_properties()

    @property
    def backup_metadata_folder(self) -> str:
        """Get the path to the backup metadata folder.

        Returns:
            The path to the backup metadata folder as a string.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> metadata_path = drm.backup_metadata_folder  # Use dot notation for property access
            >>> print(f"Backup metadata folder: {metadata_path}")

        #ai-gen-doc
        """
        return self._export_settings.get('backupMetadataFolder')

    @property
    def upload_backup_metadata_to_cloud(self) -> bool:
        """Get the current setting for uploading backup metadata to the cloud.

        Returns:
            True if the upload backup metadata to cloud option is enabled, False otherwise.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> is_enabled = drm.upload_backup_metadata_to_cloud
            >>> print(f"Upload backup metadata to cloud enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._export_settings.get('uploadBackupMetadataToCloud')

    @property
    def upload_backup_metadata_to_cloud_lib(self) -> bool:
        """Check if backup metadata upload to the cloud library is enabled.

        Returns:
            True if uploading backup metadata to the cloud library is enabled, False otherwise.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> is_enabled = drm.upload_backup_metadata_to_cloud_lib
            >>> print(f"Upload to cloud library enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._export_settings.get('uploadBackupMetadataToCloudLib')

    @property
    def dr_storage_policy(self) -> str:
        """Get the name of the storage policy used for Disaster Recovery (DR) backups.

        Returns:
            The name of the storage policy configured for DR backups.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> storage_policy_name = drm.dr_storage_policy
            >>> print(f"DR Storage Policy: {storage_policy_name}")

        #ai-gen-doc
        """
        return self._export_settings.get('storagePolicy').get('storagePolicyName')

    @dr_storage_policy.setter
    def dr_storage_policy(self, storage_policy_object: StoragePolicy) -> None:
        """Set the storage policy to be used for Disaster Recovery (DR) jobs.

        Args:
            storage_policy_object: An object representing the storage policy to assign for DR jobs.

        #ai-gen-doc
        """
        if isinstance(storage_policy_object, StoragePolicy):        # add str
            self._export_settings['storagePolicy']['storagePolicyName'] = storage_policy_object.name
            self._export_settings['storagePolicy']['storagePolicyId'] = int(storage_policy_object.storage_policy_id)
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def pre_scan_process(self) -> str:
        """Get the script path for the pre-scan process.

        Returns:
            The file system path to the script used for the pre-scan process as a string.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> script_path = drm.pre_scan_process
            >>> print(f"Pre-scan script path: {script_path}")

        #ai-gen-doc
        """
        return self._prepost_settings.get('preScanProcess')

    @pre_scan_process.setter
    def pre_scan_process(self, path: str) -> None:
        """Set the path for the pre-scan process script.

        Args:
            path: The file system path to the pre-scan script to be used during disaster recovery operations.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.pre_scan_process = "/opt/scripts/pre_scan.sh"
            >>> # The pre-scan process is now set to the specified script path

        #ai-gen-doc
        """
        if isinstance(path, str):
            self._prepost_settings['preScanProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def post_scan_process(self) -> str:
        """Get the script path configured for the post scan process.

        Returns:
            The file system path to the script that is executed after the scan process completes.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> post_scan_script = drm.post_scan_process
            >>> print(f"Post scan script path: {post_scan_script}")

        #ai-gen-doc
        """
        return self._prepost_settings.get('postScanProcess')

    @post_scan_process.setter
    def post_scan_process(self, path: str) -> None:
        """Set the path for the post scan process script.

        Args:
            path: The file system path to the post scan script to be executed after the scan process.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.post_scan_process = "/opt/scripts/post_scan.sh"
            >>> # The post scan process script is now set to the specified path

        #ai-gen-doc
        """
        if isinstance(path, str):
            self._prepost_settings['postScanProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def pre_backup_process(self) -> str:
        """Get the script path of the pre-backup process.

        Returns:
            The file system path to the script that is executed before the backup process begins.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> pre_script = drm.pre_backup_process
            >>> print(f"Pre-backup script path: {pre_script}")

        #ai-gen-doc
        """
        return self._prepost_settings.get('preBackupProcess')

    @pre_backup_process.setter
    def pre_backup_process(self, path: str) -> None:
        """Set the path for the pre-backup process script.

        Args:
            path: The file system path to the pre-backup script to be executed before backup operations.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.pre_backup_process = "/opt/scripts/pre_backup.sh"
            >>> # The pre-backup process is now set to the specified script path

        #ai-gen-doc
        """
        if isinstance(path, str):
            self._prepost_settings['preBackupProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def post_backup_process(self) -> str:
        """Get the script path configured for the post-backup process.

        Returns:
            The file system path to the script that is executed after a backup completes.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> script_path = drm.post_backup_process
            >>> print(f"Post-backup script path: {script_path}")

        #ai-gen-doc
        """
        return self._prepost_settings.get('postBackupProcess')

    @post_backup_process.setter
    def post_backup_process(self, path: str) -> None:
        """Set the path for the post-backup process script.

        This setter assigns the file system path to the script that should be executed after a backup operation completes.

        Args:
            path: The file system path to the post-backup script.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.post_backup_process = "/opt/scripts/post_backup.sh"
            >>> # The post-backup process is now set to execute the specified script after backups

        #ai-gen-doc
        """
        if isinstance(path, str):
            self._prepost_settings['postBackupProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def run_post_scan_process(self) -> bool:
        """Get the current setting for running the post scan process.

        Returns:
            bool: True if the post scan process is enabled, False otherwise.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> if drm.run_post_scan_process:
            ...     print("Post scan process is enabled.")
            ... else:
            ...     print("Post scan process is disabled.")

        #ai-gen-doc
        """
        return self._prepost_settings.get('runPostScanProcess')

    @run_post_scan_process.setter
    def run_post_scan_process(self, flag: bool) -> None:
        """Set the flag to enable or disable the post scan process.

        Args:
            flag: A boolean value indicating whether to run the post scan process (True) or not (False).

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.run_post_scan_process = True  # Enable post scan process
            >>> drm.run_post_scan_process = False  # Disable post scan process

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            self._prepost_settings['runPostScanProcess'] = flag
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def run_post_backup_process(self) -> bool:
        """Get the current setting for running the post-backup process.

        Returns:
            bool: True if the post-backup process is enabled, False otherwise.

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> if drm.run_post_backup_process:
            ...     print("Post-backup process is enabled.")
            ... else:
            ...     print("Post-backup process is disabled.")

        #ai-gen-doc
        """
        return self._prepost_settings.get('runPostBackupProcess')

    @run_post_backup_process.setter
    def run_post_backup_process(self, flag: bool) -> None:
        """Set the flag to enable or disable the post-backup process.

        Args:
            flag: A boolean value indicating whether to run the post-backup process (True) or not (False).

        Example:
            >>> drm = DisasterRecoveryManagement()
            >>> drm.run_post_backup_process = True  # Enable post-backup process
            >>> drm.run_post_backup_process = False  # Disable post-backup process

        #ai-gen-doc
        """
        if isinstance(flag, bool):
            self._prepost_settings['runPostBackupProcess'] = flag
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')