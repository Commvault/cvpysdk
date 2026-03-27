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
File for operating on a Oracle Instance.

OracleInstance is the only class defined in this file.

OracleInstance: Derived class from Instance Base class, representing an
                            oracle instance, and to perform operations on that instance

OracleInstance:

    __init__()                          --  Constructor for the class

    restore_to_disk                     --  Performs restore to disk(app free restore)

    _get_instance_properties()          --  gets the properties of this instance

    _get_instance_properties_json()     --  gets all the instance related properties
                                            of Oracle instance

    _restore_common_options_json()      --  Setter for the Common options in restore JSON

    _restore_destination_json()         --  Setter for the Oracle destination options in restore JSON


    _get_live_sync_oracleopt_json()     --  Constructs JSON with oracle agent specific options
                                            for configuring live sync

    _live_sync_restore_json()           --  Constructs oracle live sync restore JSON
                                            by combining common and agent specific options

    create_live_sync_schedule()         --  Creates live sync schedule for the given
                                            destination oracle instance

    configure_data_masking_policy()     --  Configures data masking
                                            policy with given parameters

    get_masking_policy_id()             --  To get policy id of
                                            given data masking policy

    standalone_data_masking()           --  Launch standalone data masking
                                            job on given instance

    delete_data_masking_policy()        --  Deletes given data masking policy

    _get_browse_options                 --  To get browse options for oracle instance

    _process_browse_response            --  To process browse response

    log_stream()                        --  Getter for fetching archive log stream count

    oracle_home()                       --  Getter for $ORACLE_HOME of this instance

    version()                           --  Getter for oracle database version

    is_catalog_enabled()                --  Getter to check if catalog is enabled for backups

    catalog_user()                      --  Getter for getting catalog user

    catalog_db()                        --  Getter for catalog database name

    archive_log_dest()                  --  Getter for archivelog destination

    os_user()                           --  Getter for OS user owning oracle software

    cmd_sp()                            --  Getter for command line storage policy

    log_sp()                            --  Getter for log storage policy

    is_autobackup_on()                  --  Getter to check if autobackup is enabled

    db_user()                           --  Getter for SYS database user name

    tns_name()                          --  Getter for TNS connect string

    dbid()                              --  Getter for getting DBID of database

    restore()                           --  Performs restore on the instance
    
    _restore_db_dump_option_json()       --  setter for the oracle dbdump Restore option in restore JSON
    
    _restore_oracle_option_json()       --  setter for the oracle Restore option in restore JSON
    
    _restore_json()                     --  returns the JSON request to pass to the API as per
    the options selected by the user
    
    restore_in_place()                  --  restore for oracle logical dump

"""
from __future__ import unicode_literals
from base64 import b64encode
import json

from ..exception import SDKException
from ..job import Job
from .dbinstance import DatabaseInstance

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class OracleInstance(DatabaseInstance):
    """
    Represents a standalone Oracle database instance with advanced management capabilities.

    This class provides a comprehensive interface for managing Oracle database instances,
    including backup, restore, data masking, live sync, and property management operations.
    It is designed to interact with agent objects and supports both disk-based and in-place
    restore operations, as well as live synchronization and data masking policy configuration.

    Key Features:
        - Initialization and configuration of Oracle instances
        - Backup operations for subclients
        - Restore operations to disk and in-place, with support for advanced options
        - Live sync restore and schedule creation for Oracle databases
        - Data masking policy management: configure, retrieve, delete, and apply policies
        - Property accessors for Oracle instance attributes (e.g., oracle_home, version, db_user, tns_name)
        - Browsing and processing of database objects and responses
        - Support for RAC stream allocation and advanced restore options
        - Management of catalog and archive log destinations

    This class is intended for use in environments requiring robust Oracle database management,
    automation of backup and restore workflows, and enforcement of data masking policies.

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int = None) -> None:
        """Initialize an OracleInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Oracle instance.
            instance_name: The name of the Oracle instance.
            instance_id: Optional; the unique identifier for the Oracle instance.

        #ai-gen-doc
        """
        super(OracleInstance, self).__init__(
            agent_object, instance_name, instance_id)
        self._LIVE_SYNC = self._commcell_object._services['LIVE_SYNC']
        self._dbDump_restore_json = None
        self._oracle_restore_json = None

    def restore_to_disk(self,
                        destination_client: str,
                        destination_path: str,
                        backup_job_ids: list,
                        user_name: str,
                        password: str) -> 'Job':
        """Perform an application-free restore of Oracle data to disk.

        This method restores Oracle backup data to a specified path on a destination client
        using the provided backup job IDs. The operation is performed using impersonation
        credentials for the destination client.

        Args:
            destination_client: The name of the destination client where data will be restored.
            destination_path: The full path on the destination client where the data will be restored.
            backup_job_ids: List of backup job IDs to use for the disk restore.
            user_name: The impersonation username for the destination client.
            password: The impersonation user password for the destination client.

        Returns:
            Job: An object containing details of the restore job.

        Raises:
            SDKException: If backup_job_ids is not provided as a list.

        Example:
            >>> oracle_instance = OracleInstance()
            >>> job = oracle_instance.restore_to_disk(
            ...     destination_client="dbserver01",
            ...     destination_path="/restore/oracle",
            ...     backup_job_ids=[12345, 12346],
            ...     user_name="oracle_user",
            ...     password="secure_password"
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not isinstance(backup_job_ids, list):
            raise SDKException('Instance', '101')

        request_json = self._get_restore_to_disk_json(
            destination_client,
            destination_path,
            backup_job_ids,
            user_name,
            password
        )

        return self._process_restore_response(request_json)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Oracle instance.

        This method fetches the latest configuration and status properties for the Oracle instance
        from the Commcell server and updates the instance's internal state accordingly.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        #ai-gen-doc
        """
        super(OracleInstance, self)._get_instance_properties()
        self._instanceprop = self._properties['oracleInstance']

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all properties related to the Oracle instance as a dictionary.

        Returns:
            dict: A dictionary containing all instance properties for the Oracle instance.

        #ai-gen-doc
        """
        instance_json = {
            "instanceProperties":
                {
                    "instance": self._instance,
                    "oracleInstance": self._instanceprop
                }
        }
        return instance_json

    @property
    def log_stream(self) -> int:
        """Get the log stream count at the Oracle instance level.

        Returns:
            The number of log streams configured for this Oracle instance.

        #ai-gen-doc
        """
        return self._instanceprop.get("numberOfArchiveLogBackupStreams")

    @log_stream.setter
    def log_stream(self, log_stream: int = 1) -> None:
        """Set the log stream count at the Oracle instance level.

        Args:
            log_stream: The number of log streams to set for the instance. Defaults to 1.

        #ai-gen-doc
        """
        self._set_instance_properties("_instanceprop['numberOfArchiveLogBackupStreams']", log_stream)

    def _restore_common_options_json(self, value: dict) -> None:
        """Set the common options for the restore JSON configuration.

        Args:
            value: A dictionary containing common options to be included in the restore JSON.

        #ai-gen-doc
        """
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')
        super()._restore_common_options_json(value)
        if value.get("baseline_jobid"):
            self._commonoption_restore_json = ({
                "clusterDBBackedup": value.get("clusterDBBackedup", False),
                "restoreToDisk": value.get("restoreToDisk", False),
                "baselineBackup": 1,
                "baselineRefTime": value.get("baseline_ref_time", ""),
                "isDBArchiveRestore": value.get("isDBArchiveRestore", False),
                "baselineJobId": value.get("baseline_jobid", ""),
                "copyToObjectStore": value.get("copyToObjectStore", False),
                "onePassRestore": value.get("onePassRestore", False),
                "syncRestore": value.get("syncRestore", True)
            })

    def _restore_destination_json(self, value: dict) -> None:
        """Set the Oracle destination options in the restore JSON.

        Args:
            value: A dictionary containing the destination options for the Oracle restore operation.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = ({
            "noOfStreams": value.get("number_of_streams", 2),
            "destClient": {
                "clientName": value.get("destination_client", "")
            },
            "destinationInstance": {
                "clientName": value.get("destination_client", ""),
                "instanceName": value.get("destination_instance", ""),
                "appName": value.get("app_name", "Oracle")
            }
        })

    def _get_live_sync_oracleopt_json(self, **kwargs: dict) -> None:
        """Construct a JSON dictionary with Oracle agent-specific options for configuring live sync.

        This method generates a JSON structure containing options required for live sync operations
        specific to Oracle agents. The options are provided as keyword arguments.

        Keyword Args:
            redirect_path (str): Path on the destination client to which tablespaces and datafiles
                should be redirected.

        Returns:
            None

        #ai-gen-doc
        """

        self._oracle_options = {
            "renamePathForAllTablespaces": "",
            "redirectAllItemsSelected": False,
            "validate": False,
            "ctrlRestoreFrom": True,
            "noCatalog": True,
            "cloneEnv": False,
            "ctrlFileBackupType": 0,
            "restoreControlFile": True,
            "duplicate": False,
            "tableViewRestore": False,
            "osID": 2,
            "partialRestore": False,
            "restoreStream": 2,
            "restoreSPFile": False,
            "recover": True,
            "oraExtendedRstOptions": 0,
            "recoverFrom": 3,
            "archiveLog": False,
            "restoreData": True,
            "restoreFrom": 3,
            "crossmachineRestoreOptions": {
                "onlineLogDest": ""
            },
            "liveSyncOpt": {
                "restoreInStandby": False
            }
        }
        if kwargs.get('redirect_path', None) is not None:
            self._oracle_options.update({
                "renamePathForAllTablespaces": kwargs.get('redirect_path'),
                "redirectAllItemsSelected": True,
                "redirectItemsPresent": True
            })

    def _live_sync_restore_json(
            self,
            dest_client: str,
            dest_instance: str,
            baseline_jobid: int,
            baseline_ref_time: int,
            schedule_name: str,
            source_backupset_id: int,
            **kwargs: dict
    ) -> str:
        """Construct the Oracle Live Sync restore JSON payload.

        This method combines common and Oracle agent-specific options to generate
        the JSON required for configuring a Live Sync restore operation.

        Args:
            dest_client: The destination client name for the Live Sync operation.
            dest_instance: The destination Oracle instance name for Live Sync.
            baseline_jobid: The job ID of the baseline backup job.
            baseline_ref_time: The reference or start time of the baseline backup (as a Unix timestamp).
            schedule_name: The name of the Live Sync schedule to be created.
            source_backupset_id: The ID of the source backupset from the source Oracle instance.
            **kwargs: Additional keyword arguments for advanced options.
                Supported keys:
                    - redirect_path (str): Path on the destination client to redirect tablespaces and datafiles.

        Returns:
            The constructed Live Sync restore JSON string containing all required options.

        Example:
            >>> json_payload = oracle_instance._live_sync_restore_json(
            ...     dest_client="ora_dest_client",
            ...     dest_instance="ora_dest_instance",
            ...     baseline_jobid=12345,
            ...     baseline_ref_time=1680000000,
            ...     schedule_name="DailyLiveSync",
            ...     source_backupset_id=6789,
            ...     redirect_path="/oracle/datafiles"
            ... )
            >>> print(json_payload)
            # The output is a JSON string ready for use in Live Sync configuration.

        #ai-gen-doc
        """

        restore_json = super()._restore_json(
            destination_client=dest_client,
            destination_instance=dest_instance,
            baseline_jobid=baseline_jobid,
            baseline_ref_time=baseline_ref_time,
            syncRestore=True,
            no_of_streams=2,
        )

        restore_option = {}
        if restore_json.get("restore_option"):
            restore_option = restore_json["restore_option"]
            for key in restore_json:
                if not key == "restore_option":
                    restore_option[key] = restore_json[key]
        else:
            restore_option.update(restore_json)

        self._get_live_sync_oracleopt_json(**kwargs)
        restore_json['taskInfo']['associations'][0]['subclientId'] = -1
        restore_json['taskInfo']['associations'][0]['backupsetId'] = source_backupset_id
        restore_json['taskInfo']['associations'][0]['subclientName'] = ""
        restore_json['taskInfo']['associations'][0]['backupsetName'] = ""
        restore_json['taskInfo']['associations'][0]['_type_'] = 5
        restore_json['taskInfo']['task']['taskType'] = 2
        restore_json['taskInfo']['subTasks'][0]['subTask']['operationType'] = 1007
        restore_json['taskInfo']['subTasks'][0]['subTask']['subTaskName'] = schedule_name
        restore_json['taskInfo']['subTasks'][0]['pattern'] = {
            "freq_type": 4096
        }
        destinationInstance = {
            "clientName": dest_client,
            "instanceName": dest_instance,
            "appName": "Oracle"
        }
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["destination"].update({"destinationInstance": destinationInstance})
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["oracleOpt"] = self._oracle_options

        return restore_json

    def create_live_sync_schedule(self, dest_client: str, dest_instance: str, schedule_name: str, **kwargs) -> 'Job':
        """Run a full backup on the source Oracle instance and create a live sync schedule
        for the specified destination Oracle instance.

        This method initiates a baseline backup on the source Oracle instance and sets up a live sync schedule
        to replicate data to the destination instance.

        Additional options can be provided via keyword arguments, such as redirecting tablespaces and datafiles
        to a specific path on the destination client.

        Args:
            dest_client: The name of the destination client for live sync.
            dest_instance: The name of the destination Oracle instance for live sync.
            schedule_name: The name to assign to the live sync schedule.
            **kwargs: Optional keyword arguments. Supported keys include:
                - redirect_path (str): Path on the destination client to redirect tablespaces and datafiles.

        Returns:
            The job object representing the baseline backup that will be replicated.

        Example:
            >>> oracle_instance = OracleInstance()
            >>> job = oracle_instance.create_live_sync_schedule(
            ...     dest_client="DestClient01",
            ...     dest_instance="DestInstance01",
            ...     schedule_name="DailyLiveSync",
            ...     redirect_path="/mnt/oracle/data"
            ... )
            >>> print(f"Live sync schedule created. Baseline job ID: {job.job_id}")

        #ai-gen-doc
        """
        source_backupset_id = int(self.backupsets.get('default').backupset_id)
        subclient_obj = self.subclients.get('default')
        baseline_job_object = subclient_obj.backup(backup_level='full')
        if not baseline_job_object.wait_for_completion():
            raise SDKException('Instance', '102', baseline_job_object.delay_reason)
        baseline_ref_time = baseline_job_object.summary['jobStartTime']
        baseline_jobid = int(baseline_job_object.job_id)
        request_json = self._live_sync_restore_json(dest_client, dest_instance, baseline_jobid,
                                                    baseline_ref_time, schedule_name,
                                                    source_backupset_id, **kwargs)
        flag, response = self._cvpysdk_object.make_request('POST', self._LIVE_SYNC, request_json)
        if flag:
            if response.json():
                if "taskId" in response.json():
                    return baseline_job_object
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    error_message = 'Live Sync configuration failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Instance', '102', error_message)
                else:
                    raise SDKException('Instance', '102', 'Failed to create schedule')
            else:
                raise SDKException('Instance', '102')
        else:
            raise SDKException('Instance', '101', self._update_response_(response.text))

    def configure_data_masking_policy(self, policy_name: str, table_list_of_dict: list[dict]) -> bool:
        """Configure a data masking policy for Oracle tables with specified rules.

        This method sets up a data masking policy using the provided policy name and a list of table masking rules.
        Each table rule specifies the table name and a list of columns, where each column defines the masking algorithm
        and any required arguments.

        Args:
            policy_name: The name of the data masking policy to configure.
            table_list_of_dict: A list of dictionaries, each representing a table and its masking rules.
                Each dictionary should have the following structure:
                    {
                        "name": "schema_name.table_name",
                        "columns": [
                            {
                                "name": "column_name",
                                "type": algorithm_type_number,
                                "arguments": [list of strings, optional]
                            },
                            ...
                        ]
                    }
                - "name": Fully qualified table name (schema and table).
                - "columns": List of column masking rules.
                    - "name": Name of the column to mask.
                    - "type": Algorithm type number (see below).
                    - "arguments": List of strings with algorithm arguments (if required).

        Returns:
            bool - After successfully configuring the data masking policy

        Supported algorithm types and arguments:
            - Shuffling (0): No arguments required.
            - FPE (1): No arguments required.
            - Numeric Range (2): Arguments: [min, max] as strings, e.g., ["1000", "2000"].
            - Numeric Variance (3): Arguments: [variance percentage] as string, e.g., ["50"].
            - Fixed String (4): Arguments: [string_to_replace], e.g., ["MASKED"].

        Supported algorithms by column type:
            - Numeric: Shuffling, FPE, Numeric Range, Numeric Variance
            - Char: Shuffling, FPE, Fixed String
            - Varchar: Shuffling, FPE, Fixed String

        #ai-gen-doc
        """
        request_json = {
            "opType": 2,
            "policy": {
                "association": {"instanceId": int(self.instance_id)},
                "config": {"tables": table_list_of_dict},
                "policy": {"policyName": policy_name}
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['MASKING_POLICY'], request_json
        )
        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code != 0:
                    error_string = response.json()['errorMessage']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating Data masking policy\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    return True

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_masking_policy_id(self, policy_name: str) -> int:
        """Retrieve the policy ID for a specified data masking policy by name.

        Args:
            policy_name: The name of the data masking policy whose ID is to be retrieved.

        Returns:
            The integer ID corresponding to the specified data masking policy.

        #ai-gen-doc
        """
        instance_id = int(self.instance_id)
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['MASKING_POLICY'])
        response_json = response.json()
        policy_list = response_json["policies"]
        policy_id = None
        for i in policy_list:
            pname = i["policy"]["policyName"]
            associated_instance_id = i["association"]["instanceId"]
            if (pname == policy_name) and (associated_instance_id == instance_id):
                policy_id = int(i["policy"]["policyId"])
                break
            else:
                continue
        return policy_id

    def delete_data_masking_policy(self, policy_name: str) -> bool:
        """Delete a specified data masking policy from the Oracle instance.

        Args:
            policy_name: The name of the data masking policy to be deleted.

        Returns:
            True if the policy was successfully deleted, False otherwise.

        Raises:
            Exception: If the deletion fails or if an invalid policy name is provided.

        #ai-gen-doc
        """
        source_instance_id = int(self.instance_id)
        policy_id = self.get_masking_policy_id(policy_name)
        if policy_id is None:
            raise SDKException(
                'Instance',
                '106')

        request_json = {
            "opType": 3,
            "policy": {
                "association": {"instanceId": source_instance_id},
                "policy": {"policyId": policy_id, "policyName": policy_name}
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['MASKING_POLICY'], request_json
        )
        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while deleting Data masking policy\nError')
                else:
                    return True

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def standalone_data_masking(
            self,
            policy_name: str,
            destination_client: str = None,
            destination_instance: str = None
    ) -> object:
        """Launch a standalone data masking job on the specified Oracle instance.

        This method initiates a data masking job using the provided data masking policy.
        Optionally, you can specify a destination client and destination instance where
        the masking should be applied.

        Args:
            policy_name: The name of the data masking policy to use.
            destination_client: (Optional) The name of the destination client where the destination instance exists.
            destination_instance: (Optional) The name of the destination instance to which masking will be applied.

        Returns:
            An object representing the Job containing details of the data masking operation.

        Raises:
            SDKException: If the policy ID retrieved is None.

        Example:
            >>> oracle_instance = OracleInstance()
            >>> job = oracle_instance.standalone_data_masking(
            ...     policy_name="MaskingPolicy1",
            ...     destination_client="ProdClient",
            ...     destination_instance="ProdInstance"
            ... )
            >>> print(f"Data masking job started: {job}")

        #ai-gen-doc
        """
        if destination_client is None:
            destination_client = self._properties['instance']['clientName']
        if destination_instance is None:
            destination_instance = self.instance_name
        destination_client_object = self._commcell_object.clients.get(
            destination_client)
        destination_agent_object = destination_client_object.agents.get(
            'oracle')
        destination_instance_object = destination_agent_object.instances.get(
            destination_instance)
        destination_instance_id = int(destination_instance_object.instance_id)
        source_instance_id = int(self.instance_id)
        policy_id = self.get_masking_policy_id(policy_name)
        if policy_id is None:
            raise SDKException(
                'Instance',
                '106')
        request_json = self._restore_json(paths=r'/')
        destination_instance_json = {
            "clientName": destination_client,
            "instanceName": destination_instance,
            "instanceId": destination_instance_id
        }
        data_masking_options = {
            "isStandalone": True,
            "enabled": True,
            "dbDMPolicy": {
                "association": {
                    "instanceId": source_instance_id},
                "policy": {
                    "policyId": policy_id,
                    "policyName": policy_name}}}
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["destination"]["destClient"]["clientName"] = destination_client
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["destination"]["destinationInstance"] = destination_instance_json
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["dbDataMaskingOptions"] = data_masking_options
        del request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"]
        return self._process_restore_response(request_json)

    def _get_oracle_restore_json(
            self,
            destination_client: str,
            instance_name: str,
            tablespaces: list,
            files: dict,
            browse_option: dict,
            common_options: dict,
            oracle_options: dict,
            destination: dict = None
    ) -> dict:
        """Generate and modify the restore JSON for Oracle database restores.

        This method retrieves the base restore JSON and customizes it for Oracle-specific restore operations,
        including tablespace and file options, browse and common options, and Oracle-specific settings.

        Args:
            destination_client: Name of the destination client where the restore will be performed.
            instance_name: Name of the Oracle instance to restore.
            tablespaces: List of tablespace names to be restored.
            files: Dictionary specifying file options for the restore.
            browse_option: Dictionary containing browse options for the restore operation.
            common_options: Dictionary containing common restore options.
            oracle_options: Dictionary containing additional Oracle-specific restore options.
            destination: Optional; dictionary specifying destination client and instance names. Defaults to None.

        Returns:
            dict: JSON-formatted dictionary containing all options required to restore the Oracle database.

        Raises:
            SDKException: If tablespaces is not a list or if files is not a dictionary.

        Example:
            >>> restore_json = oracle_instance._get_oracle_restore_json(
            ...     destination_client="ora_client",
            ...     instance_name="orcl",
            ...     tablespaces=["USERS", "SYSTEM"],
            ...     files={"datafile": "/path/to/datafile"},
            ...     browse_option={"backupset": "full"},
            ...     common_options={"overwrite": True},
            ...     oracle_options={"restoreControlFile": True},
            ...     destination={"client": "ora_client", "instance": "orcl"}
            ... )
            >>> print(restore_json)
            {'destination': {'client': 'ora_client', 'instance': 'orcl'}, ...}

        #ai-gen-doc
        """
        if not isinstance(tablespaces, list):
            raise SDKException(
                'Instance',
                '101', 'Expecting a list for tablespaces')
        if files is not None:
            if not isinstance(files, dict):
                raise SDKException(
                    'Instance',
                    '101', 'Expecting a dict for files')

        destination_id = int(self._commcell_object.clients.get(
            destination_client).client_id)
        tslist = ["SID: {0} Tablespace: {1}".format(
            instance_name, ts) for ts in tablespaces]
        restore_json = self._restore_json(paths=r'/')
        if common_options is not None:
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "commonOptions"] = common_options
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "oracleOpt"] = oracle_options
        if destination:
            if not isinstance(destination, dict):
                raise SDKException(
                    'Instance',
                    '101', 'Expecting a dict for destination details')
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["destination"] = destination
        if files is None:
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"] = {
                "sourceItem": tslist
            }
        else:
            restore_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]["fileOption"] = files

        if browse_option is not None:
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "browseOption"] = browse_option
        return restore_json

    def _get_browse_options(self) -> dict:
        """Retrieve the database instance properties required for browse and restore operations.

        Returns:
            dict: A dictionary containing the properties and options used for browsing and restoring the Oracle database instance.

        #ai-gen-doc
        """
        return {
            "path": "/",
            "entity": {
                "appName": self._properties['instance']['appName'],
                "instanceId": int(self.instance_id),
                "applicationId": int(self._properties['instance']['applicationId']),
                "clientId": int(self._properties['instance']['clientId']),
                "instanceName": self._properties['instance']['instanceName'],
                "clientName": self._properties['instance']['clientName']
            }
        }

    def _process_browse_response(self, request_json: dict, use_cache: bool = True) -> list:
        """Process the response from the DBBrowse API using the provided request JSON.

        This method sends the given JSON request to the DBBrowse API, parses the response,
        and returns a list of tablespaces for the Oracle instance.

        Args:
            request_json: Dictionary containing the JSON request to be sent to the DBBrowse API.
            use_cache: Whether to use cached tablespaces or not.

        Returns:
            A list containing tablespaces for the Oracle instance.

        Raises:
            SDKException: If the browse job fails, the response is empty, or the browse operation is not successful.

        Example:
            >>> instance = OracleInstance()
            >>> request = {"operation": "browse", "parameters": {...}}
            >>> tablespaces = instance._process_browse_response(request)
            >>> print(f"Tablespaces: {tablespaces}")

        #ai-gen-doc
        """
        if use_cache and 'tablespaces' in self._instanceprop:
            return self._instanceprop['tablespaces']

        browse_service = self._commcell_object._services['ORACLE_INSTANCE_BROWSE'] % (
            self.instance_id
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', browse_service, request_json
        )

        if flag:
            response_data = json.loads(response.text)
            if response_data:
                if "oracleContent" in response_data:
                    self._instanceprop['tablespaces'] = response_data["oracleContent"]
                    return self._instanceprop['tablespaces']
                elif "errorCode" in response_data:
                    error_message = response_data['errorMessage']
                    o_str = 'Browse job failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Instance', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def oracle_home(self) -> str:
        """Get the Oracle home directory path for this Oracle instance.

        Returns:
            The Oracle home directory as a string.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['oracleHome']

    @property
    def is_catalog_enabled(self) -> bool:
        """Check if the Oracle catalog is enabled for this instance.

        Returns:
            True if the catalog is enabled; otherwise, False.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['useCatalogConnect']

    @property
    def catalog_user(self) -> str:
        """Get the catalog user associated with this Oracle instance.

        Returns:
            The catalog user as a string.

        Raises:
            SDKException: If the catalog user is not set or if catalog is not enabled.

        #ai-gen-doc
        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['userName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102', 'Catalog user not set - {}'.format(error_str))

    @property
    def catalog_db(self) -> str:
        """Get the name of the catalog database associated with this Oracle instance.

        Returns:
            The name of the catalog database as a string.

        Raises:
            SDKException: If the catalog database is not set or if cataloging is not enabled.

        #ai-gen-doc
        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102', 'Catalog database not set - {}'.format(error_str))

    @property
    def os_user(self) -> str:
        """Get the Oracle software owner username for this instance.

        Returns:
            The username of the Oracle software owner as a string.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['oracleUser']['userName']

    @property
    def version(self) -> str:
        """Get the version string of the Oracle instance.

        Returns:
            The version of the Oracle instance as a string.

        #ai-gen-doc
        """
        return self._properties['version']

    @property
    def archive_log_dest(self) -> str:
        """Get the archive log destination for the Oracle instance.

        Returns:
            The file system path or location where archive logs are stored for this Oracle instance.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['archiveLogDest']

    @property
    def cmd_sp(self) -> str:
        """Get the command line storage policy string for the Oracle instance.

        Returns:
            str: The command line storage policy string associated with this Oracle instance.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['oracleStorageDevice'][
            'commandLineStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self) -> str:
        """Get the log storage policy name for the Oracle instance.

        Returns:
            The name of the log storage policy as a string.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['oracleStorageDevice'][
            'logBackupStoragePolicy']['storagePolicyName']

    @property
    def is_autobackup_on(self) -> bool:
        """Check if autobackup is enabled for the Oracle instance.

        Returns:
            True if autobackup is set to ON, otherwise False.

        #ai-gen-doc
        """
        return True if self._properties['oracleInstance']['ctrlFileAutoBackup'] == 1 else False

    @property
    def db_user(self) -> str:
        """Get the Oracle database user used to log into the database for this instance.

        Returns:
            The Oracle database username as a string.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['sqlConnect']['userName']

    @property
    def tns_name(self) -> str:
        """Get the TNS (Transparent Network Substrate) name of the Oracle database instance.

        Returns:
            The TNS name of the instance as a string.

        Raises:
            SDKException: If the TNS name is not set for the instance.

        #ai-gen-doc
        """
        try:
            return self._properties['oracleInstance']['sqlConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102', 'Instance TNS Entry not set - {}'.format(error_str))

    @property
    def dbid(self) -> int:
        """Get the DB ID (Database Identifier) of the Oracle database instance.

        Returns:
            int: The DB ID of the Oracle database.

        #ai-gen-doc
        """
        return self._properties['oracleInstance']['DBID']

    @property
    def tablespaces(self) -> list:
        """Get a list of all tablespace names for the Oracle database instance.

        Returns:
            list: A list containing the names of all tablespaces in the database.

        #ai-gen-doc
        """
        tablespaces = []
        browse_response = self.browse()
        if browse_response:
            for db in browse_response:
                if 'tablespace' in db:
                    tablespaces.append(db['tablespace'])

                # In the case of CDB, we may have to browse through each
                # individual database (PDB) to fetch all the tablespaces
                elif 'database' in db:
                    options = self._get_browse_options()
                    options['path'] = f"/{db['database']}"
                    tablespaces.extend(self.browse(use_cache=False, **options))
        return tablespaces


    def browse(self, *args: Any, **kwargs: Any) -> Any:
        """Browse Oracle database tablespaces.

        This method allows browsing of Oracle database tablespaces associated with the instance.
        The arguments and keyword arguments can be used to specify browse options such as 
        filters, levels, or specific tablespaces.

        Args:
            *args: Positional arguments for browse options.
            **kwargs: Keyword arguments for browse options.

        Returns:
            The result of the browse operation, which may include tablespace details or metadata.

        #ai-gen-doc
        """
        use_cache = kwargs.pop('use_cache', True)
        if args and isinstance(args[0], dict):
            options = args[0]
        elif kwargs:
            options = kwargs
        else:
            options = self._get_browse_options()
        return self._process_browse_response(options, use_cache)

    def backup(self, subclient_name: str = "default") -> None:
        """Initiate a backup operation for the Oracle database using the specified subclient.

        Args:
            subclient_name: The name of the subclient to use for the backup operation. 
                Defaults to "default" if not specified.

        #ai-gen-doc
        """
        return self.subclients.get(subclient_name).backup(r'full')

    def restore(
        self,
        files: dict = None,
        destination_client: str = None,
        common_options: dict = None,
        browse_option: dict = None,
        oracle_options: dict = None,
        tag: str = None,
        destination_instance: str = None,
        streams: int = 2
    ) -> 'Job':
        """Perform a full or partial Oracle database restore using the latest backup or a backup copy.

        This method initiates a restore operation for an Oracle database, allowing for both full and partial restores.
        You can specify various options such as files to restore, destination client, restore options, and the number of streams.

        Args:
            files: Dictionary specifying file options for the restore operation.
            destination_client: Name of the destination client where the database will be restored.
            common_options: Dictionary containing common restore options. Defaults to None.
            browse_option: Dictionary containing browse options for the restore.
            tag: Type of the restore to be performed. Defaults to None.
            destination_instance: Name of the destination Oracle instance. If None, an in-place restore is performed.
            streams: Number of streams to use for the restore operation. Defaults to 2.
            oracle_options: Dictionary containing Oracle-specific restore options. If not provided, the controlfile and
                datafiles are restored from the latest backup by default.
                Example:
                    {
                        "resetLogs": 1,
                        "switchDatabaseMode": True,
                        "noCatalog": True,
                        "restoreControlFile": True,
                        "recover": True,
                        "recoverFrom": 3,
                        "restoreData": True,
                        "restoreFrom": 3
                    }

        Returns:
            object: A Job object containing details of the initiated restore operation.

        Raises:
            SDKException: If Oracle options or destination client cannot be set.

        Example:
            >>> oracle_instance = OracleInstance()
            >>> restore_job = oracle_instance.restore(
            ...     files={"datafiles": ["/u01/oradata/mydb/data01.dbf"]},
            ...     destination_client="dbserver02",
            ...     oracle_options={
            ...         "resetLogs": 1,
            ...         "restoreControlFile": True,
            ...         "recover": True
            ...     },
            ...     streams=4
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        options = {
            "resetLogs": 1,
            "switchDatabaseMode": True,
            "noCatalog": True,
            "recover": True,
            "recoverFrom": 3,
            "restoreData": True,
            "restoreFrom": 3
        }
        if oracle_options is None:
            oracle_options = {}
        options.update(oracle_options)
        oracle_options = options.copy()

        if tag and tag.lower() == 'snap':
            opt = {
                "useSnapRestore": True,
                "cleanupAuxiliary": True,
                "restoreControlFile": True,
            }
            for key, val in opt.items():
                oracle_options.setdefault(key, val)

        try:
            if destination_client is None or destination_instance is None:
                destination_client = self._properties['instance']['clientName']
                destination_instance = self._properties['instance']['instanceName']
            destination = {
                "destination_client": destination_client,
                "destination_instance": destination_instance
            }
            if tag and tag.lower() == "rac":
                stream_allocation = self._get_rac_stream_allocation(
                    destination_client, destination_instance, streams)
                oracle_options.update(stream_allocation)
                destination["app_name"] = "Oracle RAC"
            self._restore_destination_json(destination)
        except SDKException:
            raise SDKException("Instance", "105")
        else:
            # subclient = self.subclients.get(subclient_name)
            if destination_client and destination_instance:
                options = self._get_oracle_restore_json(destination_client=destination_client,
                                                        destination=self._destination_restore_json,
                                                        instance_name=self.instance_name,
                                                        tablespaces=self.tablespaces,
                                                        files=files,
                                                        browse_option=browse_option,
                                                        common_options=common_options,
                                                        oracle_options=oracle_options)
            else:
                options = self._get_oracle_restore_json(destination_client=destination_client,
                                                        instance_name=self.instance_name,
                                                        tablespaces=self.tablespaces,
                                                        files=files,
                                                        browse_option=browse_option,
                                                        common_options=common_options,
                                                        oracle_options=oracle_options)
            return self._process_restore_response(options)

    def _get_rac_stream_allocation(self, destination_client: str, destination_instance: str, streams: int) -> dict:
        """Populate the RAC stream allocation settings for Oracle restore options.

        This method sets the number of streams to be used for restoring data to a specific
        destination client and RAC (Real Application Cluster) instance in Oracle environments.

        Args:
            destination_client: The name of the destination client where the restore will occur.
            destination_instance: The name of the destination RAC instance for the restore.
            streams: The number of streams to allocate for the restore operation.

        Example:
            >>> oracle_instance = OracleInstance()
            >>> oracle_instance._get_rac_stream_allocation(
            ...     destination_client="rac_node1",
            ...     destination_instance="orcl1",
            ...     streams=4
            ... )
            >>> # The RAC stream allocation is now set for the specified client and instance.

        #ai-gen-doc
        """
        destination_client_obj = self._commcell_object.clients.get(destination_client)
        destination_instance_obj = destination_client_obj.agents.get("Oracle RAC").instances.get(destination_instance)
        rac_stream_allocation = {"racDataStreamAllcation": []}
        for node in destination_instance_obj.properties['oracleRACInstance']['racDBInstance']:
            rac_stream_allocation["racDataStreamAllcation"].append(f"{node['racDbInstanceId']} {streams}")
        return rac_stream_allocation

    def _restore_db_dump_option_json(self, value: dict) -> None:
        """Set the Oracle database dump restore options in the restore JSON.

        Args:
            value: Dictionary containing the options to be set for the Oracle database dump restore operation.

        #ai-gen-doc
        """
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._db_dump_restore_json = {
            "importToDatabase": True,
            "parallelism": 2,
            "restorePath": value.get("destination_path", ""),
            "overwriteTable": False,
            "enabled": True,
            "connectDetails": {
                "password": b64encode(value.get("db_password", "").encode()).decode(),
                "domainName": (self._properties.get("oracleInstance", {}).
                               get("sqlConnect", {}).get("domainName", "")),
                "userName": (self._properties.get("oracleInstance", {}).
                             get("sqlConnect", {}).get("userName", ""))
            }
        }

    def _restore_oracle_option_json(self, value: dict) -> None:
        """Set Oracle restore options in the restore JSON configuration.

        Args:
            value: A dictionary containing the Oracle restore options to be set.

        #ai-gen-doc
        """
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._oracle_restore_json = {
            "validate": False,
            "noCatalog": False,
            "duplicateToName": "",
            "cloneEnv": False,
            "restoreControlFile": False,
            "duplicate": False,
            "tableViewRestore": False,
            "osID": 2,
            "partialRestore": False,
            "restoreStream": 2,
            "restoreSPFile": False,
            "recover": True,
            "recoverFrom": 4,
            "archiveLog": False,
            "restoreData": True,
            "restoreFrom": 0,
            "timeZone": {
                "TimeZoneName": "(UTC) Coordinated Universal Time"
            },
            "recoverTime": {},
            "sourcePaths": [
                "//**"
            ],
            "restoreTime": {}
        }

        if value.get("restore_oracle_options_type") == "restore_archivelogs_norecover":
            self._oracle_restore_json = {
                "resetLogs": 0,
                "backupValidationOnly": False,
                "threadId": 1,
                "deviceType": 0,
                "restoreFailover": True,
                "resetDatabase": False,
                "noCatalog": True,
                "ctrlRestoreFrom": False,
                "controlFilePath": "",
                "specifyControlFileTime": False,
                "restoreDataTag": False,
                "useEndLSN": False,
                "useStartLSN": False,
                "restoreTablespace": False,
                "archiveLogBy": 1,
                "ctrlFileBackupType": 0,
                "restoreControlFile": False,
                "restoreInstanceLog": False,
                "duplicate": False,
                "startLSNNum": "",
                "checkReadOnly": False,
                "osID": 2,
                "specifyControlFile": False,
                "setDBId": False,
                "partialRestore": False,
                "restoreStream": 2,
                "specifySPFile": False,
                "restoreSPFile": False,
                "recover": False,
                "recoverFrom": 4,
                "archiveLog": True,
                "endLSNNum": "",
                "autoDetectDevice": True,
                "useEndLog": False,
                "isDeviceTypeSelected": False,
                "useStartLog": True,
                "logTarget": "",
                "restoreData": False,
                "restoreFrom": 0,
                "duplicateToSkipReadOnly": False
            }
            if value.get("start_lsn", None):
                self._oracle_restore_json["useStartLSN"] = True
                self._oracle_restore_json["startLSNNum"] = value.get("start_lsn")
            if value.get("end_lsn", None):
                self._oracle_restore_json["useEndLSN"] = True
                self._oracle_restore_json["endLSNNum"] = value.get("end_lsn")
            if value.get("log_dest", None):
                self._oracle_restore_json["logTarget"] = value.get("log_dest")

    def _restore_json(self, **kwargs) -> dict:
        """Generate the JSON request payload for the restore API based on user-selected options.

        This method constructs a dictionary representing the JSON request body required by the restore API,
        using the options provided as keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments representing restore options. Each key-value pair
                corresponds to a specific restore parameter.

        Returns:
            dict: The JSON request dictionary to be sent to the API.

        #ai-gen-doc
        """
        rest_json = super(OracleInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        self._restore_db_dump_option_json(restore_option)
        self._restore_oracle_option_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["dbDumpOptions"] = self._db_dump_restore_json
        rest_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["oracleOpt"] = self._oracle_restore_json

        return rest_json

    def restore_in_place(
        self,
        db_password: str,
        path: list,
        dest_client_name: str,
        dest_instance_name: str,
        dest_path: str = None,
        restore_oracle_options_type: str = None,
        start_lsn: str = None,
        end_lsn: str = None,
        log_dest: str = None
    ) -> 'Job':
        """Restore Oracle logical dump data or log files to their original location.

        This method restores the specified Oracle database or log files, as provided in the `path` list,
        to the same location on the destination client and instance. Additional options such as destination
        path, restore options type, LSN range, and log destination can be specified for advanced restore scenarios.

        Args:
            db_password: Password for the Oracle database.
            path: List of database or log file paths to be restored.
            dest_client_name: Name of the destination client where files will be restored.
            dest_instance_name: Name of the destination Oracle instance on the destination client.
            dest_path: Optional; destination path for the restore operation. Defaults to None.
            restore_oracle_options_type: Optional; type of Oracle restore options to use. Defaults to None.
            start_lsn: Optional; starting Log Sequence Number for log restore. Defaults to None.
            end_lsn: Optional; ending Log Sequence Number for log restore. Defaults to None.
            log_dest: Optional; destination for log files during restore. Defaults to None.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If `path` is not a list, if the job fails to initialize, if the response is empty,
                or if the response indicates failure.

        Example:
            >>> oracle_instance = OracleInstance()
            >>> job = oracle_instance.restore_in_place(
            ...     db_password="oracle_pwd",
            ...     path=["/backup/db1.dmp", "/backup/db2.dmp"],
            ...     dest_client_name="oracle_client",
            ...     dest_instance_name="orcl",
            ...     dest_path="/oracle/restore",
            ...     restore_oracle_options_type="FULL",
            ...     start_lsn="1000",
            ...     end_lsn="2000",
            ...     log_dest="/oracle/logs"
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not (isinstance(path, list) and
                isinstance(db_password, str)):
            raise SDKException('Instance', '101')
        if not path:
            raise SDKException('Instance', '103')

        request_json = self._restore_json(
            db_password=db_password,
            paths=path,
            destination_client=dest_client_name,
            destination_instance=dest_instance_name,
            destination_path=dest_path,
            restore_oracle_options_type=restore_oracle_options_type,
            start_lsn=start_lsn, end_lsn=end_lsn,
            log_dest=log_dest)

        return self._process_restore_response(request_json)
