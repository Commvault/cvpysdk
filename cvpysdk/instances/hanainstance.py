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

"""File for operating on a SAP HANA Instance.

SAPHANAInstance is the only class defined in this file.

SAPHANAInstance: Derived class from Instance Base class, representing a hana server instance,
                       and to perform operations on that instance

SAPHANAInstance:

    sps_version()                   --  returns the SPS version of the instance

    instance_number()               --  returns the instance number of SAP HANA

    sql_location_directory()        --  returns the SQL location directory of the Instance

    instance_db_username()          --  returns the db username of the instance

    db_instance_client()            --  returns the SAP HANA client associated with the instance

    hdb_user_storekey()             --  returns the HDB user store key if its set

    _restore_request_json()         --  returns the restore request json

    _get_hana_restore_options()     --  returns the dict containing destination SAP HANA instance
                                            names for the given client

    restore()                       --  runs the restore job for specified instance

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ..instance import Instance
from ..exception import SDKException
from ..job import Job

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class SAPHANAInstance(Instance):
    """
    Represents a SAP HANA instance and provides operations for instance management and restoration.

    This class is derived from the Instance base class and is specifically designed to handle SAP HANA
    database instances. It encapsulates instance-specific properties such as SPS version, instance number,
    SQL location directory, database username, client information, and HDB user store key. The class also
    provides methods for generating restore request payloads, retrieving restore options, and performing
    restore operations on SAP HANA instances.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Access to SAP HANA instance properties (SPS version, instance number, SQL directory, DB username, client, user store key)
        - Generation of restore request JSON for SAP HANA instance recovery
        - Retrieval of restore options for a given destination client
        - Execution of restore operations with advanced options (point-in-time restore, log area initialization, hardware revert, clone environment, access checks, stream management, catalog time, and more)

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int = None) -> None:
        """Initialize a SAPHANAInstance object.

        Args:
            agent_object: Instance of the agent class associated with this SAP HANA instance.
            instance_name: The name of the SAP HANA instance.
            instance_id: Optional; the unique integer ID of the SAP HANA instance. Defaults to None.

        #ai-gen-doc
        """
        super(SAPHANAInstance, self).__init__(agent_object, instance_name, instance_id)
        self.destination_instances_dict = {}

    @property
    def sps_version(self) -> str:
        """Get the SPS (Support Package Stack) version of the HANA instance.

        Returns:
            str: The SPS version string of the HANA instance.

        #ai-gen-doc
        """
        return self._properties['saphanaInstance']['spsVersion']

    @property
    def instance_number(self) -> int:
        """Get the instance number of the HANA instance.

        Returns:
            The instance number as an integer.

        #ai-gen-doc
        """
        return self._properties['saphanaInstance']['dbInstanceNumber']

    @property
    def sql_location_directory(self) -> str:
        """Get the isql location directory of the HANA instance.

        Returns:
            The file system path to the isql location directory for this SAP HANA instance.

        #ai-gen-doc
        """
        return self._properties['saphanaInstance']['hdbsqlLocationDirectory']

    @property
    def instance_db_username(self) -> str:
        """Get the username of the HANA instance database.

        Returns:
            The username associated with the HANA instance database as a string.

        #ai-gen-doc
        """
        return self._properties['saphanaInstance']['dbUser']['userName']

    @property
    def db_instance_client(self) -> str:
        """Get the client name associated with the HANA database instance.

        Returns:
            The client name of the HANA instance as a string.

        #ai-gen-doc
        """
        return self._properties['saphanaInstance']['DBInstances'][0]

    @property
    def hdb_user_storekey(self) -> str:
        """Get the HDB user store key associated with the SAP HANA instance.

        Returns:
            The HDB user store key as a string.

        #ai-gen-doc
        """
        return self._properties['saphanaInstance']['hdbuserstorekey']

    def _restore_request_json(
        self,
        destination_client: str,
        destination_instance: str,
        backupset_name: str = "default",
        backup_prefix: Optional[str] = None,
        point_in_time: Optional[str] = None,
        initialize_log_area: bool = False,
        use_hardware_revert: bool = False,
        clone_env: bool = False,
        check_access: bool = False,
        destination_instance_dir: Optional[str] = None,
        ignore_delta_backups: bool = False,
        no_of_streams: int = 2,
        catalog_time: Optional[str] = None
    ) -> dict:
        """Construct the JSON request payload for a SAP HANA restore operation.

        This method generates a dictionary representing the restore request, 
        based on the provided options and parameters. The resulting JSON can 
        be sent to the API to initiate a restore operation for a SAP HANA instance.

        Args:
            destination_client: The HANA client where the database will be restored.
            destination_instance: The destination instance for the database restore.
            backupset_name: Name of the backupset to restore. For single DB instances, use "default".
            backup_prefix: Optional prefix of the backup job to restore.
            point_in_time: Optional point-in-time (as a string) to which the database should be restored.
            initialize_log_area: Whether to initialize the new log area after restore.
            use_hardware_revert: Whether to perform a hardware revert during restore.
            clone_env: Whether to clone the database environment during restore.
            check_access: Whether to check access permissions during restore.
            destination_instance_dir: Optional HANA data directory for cross-instance or cross-machine restores.
            ignore_delta_backups: Whether to ignore delta backups during restore.
            no_of_streams: Number of streams to use for the restore operation.
            catalog_time: Optional catalog time to use for the restore.

        Returns:
            dict: The JSON request payload to be sent to the API for the restore operation.

        Example:
            >>> restore_json = saphana_instance._restore_request_json(
            ...     destination_client="hana_client01",
            ...     destination_instance="HDB00",
            ...     backupset_name="default",
            ...     backup_prefix="backup_2023_01_01",
            ...     point_in_time="2023-01-01 12:00:00",
            ...     initialize_log_area=True,
            ...     use_hardware_revert=False,
            ...     clone_env=False,
            ...     check_access=True,
            ...     destination_instance_dir="/hana/data/HDB00",
            ...     ignore_delta_backups=False,
            ...     no_of_streams=4,
            ...     catalog_time=None
            ... )
            >>> print(restore_json)
            # The printed dictionary can be sent as a JSON payload to the restore API.

        #ai-gen-doc
        """
        self._get_hana_restore_options(destination_client)

        if destination_instance is None:
            destination_instance = self.instance_name
        else:
            if destination_instance not in self.destination_instances_dict:
                raise SDKException(
                    'Instance', '102', 'No Instance exists with name: {0}'.format(
                        destination_instance
                    )
                )

        destination_hana_client = self.destination_instances_dict[destination_instance][
            'destHANAClient']

        if backup_prefix is None:
            backup_prefix = ""

        databases = []

        if backupset_name != "default":
            databases.append(backupset_name)

        if point_in_time is None:
            recover_time = 0
            point_in_time = {}
        else:
            if not isinstance(point_in_time, str):
                raise SDKException('Instance', 103)

            point_in_time = {
                'time': int(point_in_time)
            }
            recover_time = 1

        request_json = {
            "taskInfo": {
                "associations": [{
                    "clientName": self._agent_object._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self.instance_name.upper(),
                    "backupsetName": backupset_name,
                    "suclientName": ""
                }],
                "task": {
                    "initiatedFrom": 1,
                    "taskType": 1
                },
                "subTasks": [{
                    "subTask": {
                        "subTaskType": 3,
                        "operationType": 1001
                    },
                    "options": {
                        "restoreOptions": {
                            "hanaOpt": {
                                "initializeLogArea": initialize_log_area,
                                "useHardwareRevert": use_hardware_revert,
                                "cloneEnv": clone_env,
                                "checkAccess": check_access,
                                "backupPrefix": backup_prefix,
                                "destDbName": destination_instance.upper(),
                                "destPseudoClientName": str(destination_client),
                                "ignoreDeltaBackups": ignore_delta_backups,
                                "destClientName": destination_hana_client,
                                "databases": databases,
                                "recoverTime": recover_time,
                                "pointInTime": point_in_time
                            },
                            "destination": {
                                "destinationInstance": {
                                    "clientName": destination_client,
                                    "appName": self._agent_object.agent_name,
                                    "instanceName": destination_instance
                                },
                                "destClient": {
                                    "clientName": destination_hana_client
                                },
                                "noOfStreams": no_of_streams
                            },
                            "browseOption": {
                                "backupset": {
                                    "clientName": self._agent_object._client_object.client_name
                                }
                            }
                        }
                    }
                }]
            }
        }
        if catalog_time:
            if not isinstance(catalog_time, str):
                raise SDKException('Instance', 103)
            catalog_time = {
                'time': int(catalog_time)
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'hanaOpt']['catalogPointInTime'] = catalog_time
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'hanaOpt']['catalogRecoverTime'] = 1

        if destination_instance_dir is not None:
            instance_dir = {
                'destinationInstanceDir': destination_instance_dir
            }

            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'hanaOpt'].update(instance_dir)

        return request_json

    def _get_hana_restore_options(self, destination_client_name: str) -> None:
        """Retrieve HANA destination server options for restore operations.

        This method calls the /GetDestinationsToRestore API to obtain available HANA destination 
        server options for the specified destination client. The response is parsed and returned 
        as a dictionary.

        Args:
            destination_client_name: The name of the destination client to which the restore will be performed.

        Returns:
            None

        Raises:
            SDKException: If the API call fails, if no client exists on the Commcell, 
                if the response is empty, or if the response indicates failure.

        #ai-gen-doc
        """
        webservice = self._commcell_object._services['RESTORE_OPTIONS'] % (
            self._agent_object.agent_id
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request("GET", webservice)

        destination_clients_dict = {}

        if flag:
            if response.json():
                if 'genericEntityList' in response.json():
                    generic_entity_list = response.json()['genericEntityList']

                    for client_entity in generic_entity_list:
                        clients_dict = {
                            client_entity['clientName'].lower(): {
                                "clientId": client_entity['clientId']
                            }
                        }
                        destination_clients_dict.update(clients_dict)
                elif 'error' in response.json():
                    if 'errorMessage' in response.json()['error']:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Client', '102', error_message)
                    else:
                        raise SDKException('Client', '102', 'No client exists on commcell')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        webservice = self._commcell_object._services['GET_ALL_INSTANCES'] % (
            destination_clients_dict[destination_client_name]['clientId']
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request("GET", webservice)

        if flag:
            if response.json():
                if 'instanceProperties' in response.json():
                    for instance in response.json()['instanceProperties']:
                        instances_dict = {
                            instance['instance']['instanceName'].lower(): {
                                "clientId": instance['instance']['clientId'],
                                "instanceId": instance['instance']['instanceId'],
                                "destHANAClient": instance['saphanaInstance'][
                                    'DBInstances'][0]['clientName']
                            }
                        }
                        self.destination_instances_dict.update(instances_dict)
                elif 'error' in response.json():
                    if 'errorMessage' in response.json()['error']:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Instance', '102', error_message)
                    else:
                        raise SDKException('Instance', '102', 'No Instance exists on commcell')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def restore(
        self,
        pseudo_client: str,
        instance: str,
        backupset_name: str = "default",
        backup_prefix: Optional[str] = None,
        point_in_time: Optional[str] = None,
        initialize_log_area: bool = False,
        use_hardware_revert: bool = False,
        clone_env: bool = False,
        check_access: bool = True,
        destination_instance_dir: Optional[str] = None,
        ignore_delta_backups: bool = True,
        no_of_streams: int = 2,
        catalog_time: Optional[str] = None
    ) -> 'Job':
        """Restore SAP HANA databases to a specified client and instance.

        This method initiates a restore operation for SAP HANA databases, allowing for various restore options such as point-in-time recovery, hardware revert, cloning, and more.

        Args:
            pseudo_client: The name of the HANA client where the database will be restored.
            instance: The destination instance name for the database restore.
            backupset_name: The backupset name of the instance to be restored. For single DB instances, use "default".
            backup_prefix: Optional prefix of the backup job to restore from.
            point_in_time: Optional point-in-time (as a string) to which the database should be restored.
            initialize_log_area: Whether to initialize the new log area after restore. Defaults to False.
            use_hardware_revert: Whether to perform a hardware revert during restore. Defaults to False.
            clone_env: Whether to clone the database environment during restore. Defaults to False.
            check_access: Whether to check access during restore. Defaults to True.
            destination_instance_dir: Optional HANA data directory for cross-instance or cross-machine restores.
            ignore_delta_backups: Whether to ignore delta backups during restore. Defaults to True.
            no_of_streams: Number of streams to use for the restore operation. Defaults to 2.
            catalog_time: Optional catalog time to use for the restore.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the instance parameter is not a string or object, if the response is empty, or if the response is not successful.

        Example:
            >>> job = saphana_instance.restore(
            ...     pseudo_client="hana_client1",
            ...     instance="HDB00",
            ...     backupset_name="default",
            ...     point_in_time="2023-05-01 12:00:00",
            ...     initialize_log_area=True,
            ...     no_of_streams=4
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not isinstance(instance, (str, Instance)):
            raise SDKException('Instance', '101')

        request_json = self._restore_request_json(
            pseudo_client,
            instance,
            backupset_name,
            backup_prefix,
            point_in_time,
            initialize_log_area,
            use_hardware_revert,
            clone_env,
            check_access,
            destination_instance_dir,
            ignore_delta_backups,
            no_of_streams,
            catalog_time
        )

        return self._process_restore_response(request_json)
