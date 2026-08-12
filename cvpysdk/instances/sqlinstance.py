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

"""File for operating on a SQL Server Instance.

SQLServerInstance is the only class defined in this file.

SQLServerInstance: Derived class from Instance Base class, representing a sql server instance,
                       and to perform operations on that instance

SQLServerInstance:

    _get_instance_properties()      --  gets the instance related properties of SQL instance.

    _get_instance_properties_json() --  gets all the instance related properties of SQL instance.

    _restore_request_json()         --  returns the restore request json

    _process_restore_response()     --  processes response received for the Restore request

    _get_sql_restore_options()      --  returns the dict containing destination sql server names

    _run_backup()                   --  runs full backup for this subclients and appends the
    job object to the return list

    _process_browse_request()       --  processes response received for Browse request

    _recoverypoint_request_json()   --  returns a json to be sent to server to create
    a recovery point

    _get_database_list()            --  gets list of databases and its properties

    _process_recovery_point_request() --  starts the recovery point job and process
    the response

    _table_level_restore_request_json() --  returns a json to be sent to the server for
    table level restore job

    _get_ag_groups()    --  gets available Availability Groups from the primary replica and returns it

    _get_ag_group_replicas()    --  gets replicas list from the Availability Group and returns it

    get_recovery_points()           --  lists all the recovery points

    backup()                        --  runs full backup for all subclients associated
    with this instance

    browse()                        --  gets the content of the backup for this instance

    browse_in_time()                --  gets the content of the backup for this instance
    in the time range specified

    restore()                       --  runs the restore job for specified

    restore_to_destination_server() --  restores the database on destination server

    create_recovery_point()         --  creates a recovery point on destination server

    table_level_restore()           --  starts the table level restore job

    mssql_instance_prop()       --  sets instance properties for the mssql instance

    vss_option()        --  enables or disables VSS option on SQL instance

    vdi_timeout()       --  sets the SQL VDI timeout value on SQL instance

    impersonation()     --  sets impersonation on SQL instance with local system account or provided credentials

    create_sql_ag()     --  creates a new SQL Availability Group client and instance

    database_details()  --  gets the database details

SQLServerInstance Attributes:

    mssql_instance_prop     --  returns the mssql instance properties

    ag_group_name           --  returns the Availability Group Name

    ag_primary_replica      --  returns the Availability Group Primary Replica

    ag_replicas_list        --  returns the Availability Group Replicas List

    ag_listener_list        --  returns the Availability Group Listener List

    database_list           --  returns the list of protected databases

"""

import datetime
import re
import threading
import time

from typing import Any, Dict, List, Optional, Union

from ..constants import SQLDefines
from ..exception import SDKException
from ..instance import Instance
from ..job import Job
from ..schedules import Schedules
from ..schedules import Schedule
from ..schedules import SchedulePattern


class SQLServerInstance(Instance):
    """
    Represents a SQL Server instance, extending the base Instance class to provide
    comprehensive management and operational capabilities for SQL Server environments.

    This class offers a wide range of methods and properties to interact with SQL Server
    instances, including management of Always On Availability Groups (AG), backup and restore
    operations, database browsing, recovery point management, and table-level restores.
    It also provides access to instance and database properties, and supports advanced
    configuration options such as VSS, VDI timeouts, and impersonation.

    Key Features:
        - Access to AG group names, primary replicas, replicas list, and listener list
        - Retrieval and management of database lists and instance properties
        - Backup operations for SQL Server databases and subclients
        - Flexible restore operations, including point-in-time, overwrite, and destination server restores
        - Table-level restore capabilities with options for child and parent tables
        - Recovery point creation and management
        - Browsing of databases and data within specific time ranges
        - Configuration of VSS options, VDI timeouts, and impersonation credentials
        - Creation and management of SQL Always On Availability Groups
        - Detailed retrieval of database information

    #ai-gen-doc
    """

    @property
    def ag_group_name(self) -> str:
        """Get the name of the Availability Group associated with this SQL Server instance.

        Returns:
            The Availability Group name as a string.

        #ai-gen-doc
        """
        return self._ag_group_name

    @property
    def ag_primary_replica(self) -> str:
        """Get the name of the Availability Group Primary Replica for this SQL Server instance.

        Returns:
            The name of the primary replica server as a string.

        #ai-gen-doc
        """
        return self._ag_primary_replica

    @property
    def ag_replicas_list(self) -> list:
        """Get the list of Availability Group Replicas for the SQL Server instance.

        Returns:
            list: A list containing information about each Availability Group Replica associated with this SQL Server instance.

        #ai-gen-doc
        """
        return self._ag_replicas_list

    @property
    def ag_listener_list(self) -> list:
        """Get the list of Availability Group Listeners for the SQL Server instance.

        Returns:
            list: A list containing the names or details of Availability Group Listeners associated with this SQL Server instance.

        #ai-gen-doc
        """
        return self._ag_listener_list

    @property
    def database_list(self) -> List[Dict]:
        """Get the list of protected databases for this SQL Server instance.

        Returns:
            List of dictionary of database names (as strings) that are currently protected.

        #ai-gen-doc
        """
        return self._get_database_list()

    @property
    def mssql_instance_prop(self) -> dict:
        """Get the properties of the SQL Server instance.

        Returns:
            dict: A dictionary containing the properties of the SQL Server instance.

        #ai-gen-doc
        """
        return self._mssql_instance_prop

    @mssql_instance_prop.setter
    def mssql_instance_prop(self, value: list) -> None:
        """Set the SQL Server instance properties.

        This setter updates the SQL Server instance properties with the provided list of categories and properties.
        The input should be a list specifying the categories and their corresponding properties to update on the instance.

        Args:
            value: A list containing the categories and properties to update for the SQL Server instance.

        #ai-gen-doc
        """
        category, prop = value

        self._set_instance_properties(category, prop)

    def _get_instance_properties(self) -> None:
        """Retrieve the properties of the current SQL Server instance.

        This method fetches and returns a dictionary containing the configuration
        and status properties for the SQL Server instance associated with this object.

        Returns:
            None

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        #ai-gen-doc
        """

        super(SQLServerInstance, self)._get_instance_properties()

        self._ag_group_name = None
        self._ag_primary_replica = None
        self._ag_replicas_list = []
        self._ag_group_listener_list = []

        self._mssql_instance_prop = self._properties.get('mssqlInstance', {})

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services['INSTANCE'] % self._instance_id + "?propertyLevel=20"
        )

        if flag:
            if response.json():
                self._mssql_instance_prop = response.json()['instanceProperties'][0]['mssqlInstance']

        if 'agProperties' in self._mssql_instance_prop:
            self._ag_group_name = self.mssql_instance_prop.get(
                'agProperties', {}).get('availabilityGroup', {}).get('name')
            self._ag_primary_replica = self.mssql_instance_prop.get(
                'agProperties', {}).get('availabilityGroup', {}).get('primaryReplicaServerName')

            listener_list_tmp = []
            listener_list = self.mssql_instance_prop.get(
                'agProperties', {}).get('availabilityGroup', {}).get('SQLAvailabilityGroupListenerList', {})
            for listener in listener_list:
                listener_list_tmp.append(listener['availabilityGroupListenerName'])
            self._ag_listener_list = listener_list_tmp

            replica_list_tmp = []
            replica_list = self.mssql_instance_prop.get('agProperties', {}).get('SQLAvailabilityReplicasList', {})
            if replica_list:
                for replica in replica_list['SQLAvailabilityReplicasList']:
                    replica_dict = {
                        "serverName": replica['name'],
                        "clientId": replica['replicaClient']['clientId'],
                        "clientName": replica['replicaClient']['clientName']
                    }
                    replica_list_tmp.append(replica_dict)
                self._ag_replicas_list = replica_list_tmp

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all instance-related properties for this SQL Server instance.

        Returns:
            dict: A dictionary containing all subclient properties associated with this instance.

        #ai-gen-doc
        """
        instance_json = {
            "instanceProperties": {
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "mssqlInstance": self._mssql_instance_prop,
                "contentOperationType": 1
            }
        }
        return instance_json

    def _get_database_list(self) -> Optional[List[Dict]]:
        """Retrieve a list of SQL Server databases with their IDs and last backup times.

        Returns:
            List of dictionary where each key is a database name, and the value is another
            dictionary containing the database ID and the last backup time.

        Raises:
            SDKException: If the response from the server is empty.

        #ai-gen-doc
        """
        databases_details = []
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services['SQL_DATABASE_LIST'] %int(self.instance_id), None
        )
        if flag:
            response_json = response.json()
            if "SqlDatabase" in response_json:
                for database in response_json['SqlDatabase']:
                    database_name = database['dbName']
                    database_id = database['dbId']
                    backup_time = datetime.datetime.fromtimestamp(
                        int(database['bkpTime'])
                    ).strftime('%d-%m-%Y %H:%M:%S')

                    temp = {
                        database_name: [database_id, backup_time]
                    }

                    databases_details.append(temp)
                return databases_details
            return None
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _restore_request_json(
        self,
        content_to_restore: list,
        restore_path: Optional[list] = None,
        drop_connections_to_databse: bool = False,
        overwrite: bool = True,
        destination_instance: Optional[str] = None,
        to_time: Optional[Union[int, str]] = None,
        sql_restore_type: str = None,
        sql_recover_type: str = None,
        undo_path: Optional[str] = None,
        restricted_user: Optional[bool] = None,
        **kwargs: Any
    ) -> dict:
        """Construct the JSON request payload for a SQL Server restore operation.

        This method generates the appropriate JSON structure required by the API to perform
        a SQL Server database restore, based on the provided options and parameters.

        Args:
            content_to_restore: List of database names to restore.
            restore_path: Optional list of dictionaries specifying restore paths for database files.
            drop_connections_to_databse: If True, drops connections to the database during restore.
            overwrite: If True, overwrites the database during restore.
            destination_instance: Optional SQL instance name to restore databases to.
            to_time: Optional restore time as an integer (timestamp) or string ('yyyy-MM-dd HH:mm:ss').
            sql_restore_type: Type of SQL restore operation (e.g., 'DATABASE_RESTORE', 'STEP_RESTORE', 'RECOVER_ONLY').
            sql_recover_type: Type of SQL recovery state (e.g., 'STATE_RECOVER', 'STATE_NORECOVER', 'STATE_STANDBY').
            undo_path: Optional file path for undo during standby restore.
            restricted_user: If True, restores the database in restricted user mode.
            **kwargs: Additional keyword arguments:
                - point_in_time: Optional integer time value for point-in-time restore.
                - schedule_pattern: Optional dictionary specifying a schedule pattern for the restore.
                - hardware_revert: Optional bool indicating hardware revert restore.
                - log_shipping: Optional bool to restore log backups in standby or no recovery state.

        Returns:
            dict: JSON request payload to be sent to the API for the restore operation.

        Example:
            >>> restore_json = sql_instance._restore_request_json(
            ...     content_to_restore=['SalesDB', 'HRDB'],
            ...     restore_path=[{'db': 'SalesDB', 'path': '/data/sales.mdf'}],
            ...     drop_connections_to_databse=True,
            ...     overwrite=True,
            ...     destination_instance='SQLPROD01',
            ...     to_time='2023-06-01 12:00:00',
            ...     sql_restore_type='DATABASE_RESTORE',
            ...     sql_recover_type='STATE_RECOVER',
            ...     undo_path=None,
            ...     restricted_user=False,
            ...     point_in_time=1685611200,
            ...     schedule_pattern={'type': 'daily', 'time': '02:00'},
            ...     hardware_revert=False,
            ...     log_shipping=True
            ... )
            >>> print(restore_json)
            >>> # The returned dictionary can be sent to the API for restore

        #ai-gen-doc
        """

        self._get_sql_restore_options(content_to_restore)

        if destination_instance is None:
            destination_instance = self.instance_name.lower()

        if destination_instance not in self.destination_instances_dict:
            raise SDKException(
                'Instance',
                '102',
                'SQL Instance [{0}] not suitable for restore destination or does not exist.'.format(
                    destination_instance)
            )

        destination_client_id = int(
            self.destination_instances_dict[destination_instance]['clientId']
        )

        destination_instance_id = int(
            self.destination_instances_dict[destination_instance]['instanceId']
        )

        point_in_time = kwargs.get('point_in_time', None)
        schedule_pattern = kwargs.get('schedule_pattern', None)
        hardware_revert = kwargs.get('hardware_revert', False)
        log_shipping = (
                kwargs.get('log_shipping', False) and
                       (sql_recover_type == SQLDefines.STATE_STANDBY or sql_recover_type == SQLDefines.STATE_NORECOVER)
        )

        request_json = {
            "taskInfo": {
                "associations": [{
                    "clientName": self._agent_object._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self.instance_name
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
                            "sqlServerRstOption": {
                                "sqlRecoverType": sql_recover_type,
                                "dropConnectionsToDatabase": drop_connections_to_databse,
                                "overWrite": overwrite,
                                "sqlRestoreType": sql_restore_type,
                                "database": content_to_restore,
                                "restoreSource": content_to_restore,
                                "logShippingOnly": log_shipping
                            },
                            "commonOptions": {
                                "revert": hardware_revert
                            },
                            "destination": {
                                "destinationInstance": {
                                    "clientId": destination_client_id,
                                    "instanceName": destination_instance,
                                    "instanceId": destination_instance_id
                                },
                                "destClient": {
                                    "clientId": destination_client_id
                                }
                            },
                            "browseOption": {
                                "timeZone": {
                                    "TimeZoneName": self._agent_object._client_object.timezone
                                }
                            }
                        }
                    }
                }]
            }
        }

        if sql_recover_type == SQLDefines.STATE_STANDBY:
            if undo_path is not None:
                undo_path_dict = {
                    "fileOption": {
                        "mapFiles": {
                            "renameFilesSuffix": undo_path
                        }
                    }
                }
                request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(undo_path_dict)
            else:
                raise SDKException('Instance', '102', 'Failed to set Undo Path for Standby Restore.')

        if restore_path is not None:
            restore_path_dict = {
                "device":
                    restore_path
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['sqlServerRstOption']\
                .update(restore_path_dict)

        if restricted_user is not None:
            restricted_user_dict = {
                "dbOnly":
                    restricted_user
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['sqlServerRstOption']\
                .update(restricted_user_dict)

        if point_in_time:
            to_time = point_in_time
            pit_dict = {
                "pointOfTimeRst": True,
                "pointInTime": {
                    "time": point_in_time
                }
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['sqlServerRstOption']\
                .update(pit_dict)

        if to_time is not None:
            to_time_type = "toTimeValue"
            if isinstance(to_time, int):
                to_time_type = "toTime"
            to_time_dict = {
                "timeRange": {
                    to_time_type: to_time
                }
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['browseOption'].update(to_time_dict)

        if schedule_pattern is not None:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        return request_json

    def _process_restore_response(self, request_json: dict) -> Union['Job', 'Schedule']:
        """Execute the CreateTask API for a restore operation and process the response.

        This method sends the provided JSON request to the CreateTask API to initiate a restore job.
        It parses the API response and returns an instance of the Job class representing the restore job.

        Args:
            request_json: Dictionary containing the JSON request payload for the restore API.

        Returns:
            Job: An instance of the Job class representing the initiated restore job.

        Raises:
            SDKException: If the restore job fails, the response is empty, or the response indicates failure.

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['RESTORE'], request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    time.sleep(1)
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Instance', '102', o_str)
                else:
                    raise SDKException('Instance', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_sql_restore_options(self, content_to_restore: list) -> dict:
        """Retrieve SQL Server restore options using the provided database list.

        This method sends a request to the SQL/Restoreoptions API with the specified
        databases to restore, parses the response, and returns the SQL destination
        server options as a dictionary.

        Args:
            content_to_restore: List of databases to restore.

        Returns:
            Dictionary containing the SQL destination server options.

        Raises:
            SDKException: If the API call fails, no SQL instance exists on the Commcell,
                the response is empty, or the response indicates failure.

        #ai-gen-doc
        """
        contents_dict = []

        for content in content_to_restore:
            database_dict = {
                "databaseName": content
            }
            contents_dict.append(database_dict)

        request_json = {
            "restoreDbType": 0,
            "sourceInstanceId": int(self.instance_id),
            "selectedDatabases": contents_dict
        }

        webservice = self._commcell_object._services['SQL_RESTORE_OPTIONS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            "POST", webservice, request_json
        )

        self.destination_instances_dict = {}

        if flag:
            if response.json():
                if 'sqlDestinationInstances' in response.json():
                    for instance in response.json()['sqlDestinationInstances']:
                        instances_dict = {
                            instance['genericEntity']['instanceName'].lower(): {
                                "instanceId": int(instance['genericEntity']['instanceId']),
                                "clientId": int(instance['genericEntity']['clientId'])
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
        return response.json()

    def _run_backup(self, subclient_name: str, return_list: list) -> None:
        """Trigger a full backup job for the specified subclient and append the resulting Job object to a list.

        If an exception occurs while running the backup job for the subclient, an instance of the SDKException class
        is appended to the provided list instead.

        Args:
            subclient_name: The name of the subclient for which to trigger the backup.
            return_list: The list to which the resulting Job object or SDKException instance will be appended.

        #ai-gen-doc
        """
        try:
            job = self.subclients.get(subclient_name).backup('Full')
            if job:
                return_list.append(job)
        except SDKException as excp:
            return_list.append(excp)

    def _process_browse_request(self, browse_request: dict, get_full_details: bool = False) -> (list, list):
        """Execute the SQL Instance Browse API with the provided request and parse the response.

        This method sends a JSON request to the server to browse SQL instance contents and returns
        the parsed results. Depending on the operation and the `get_full_details` flag, the response
        may include a list of database names or a dictionary with detailed information such as
        backup creation time and database version.

        Args:
            browse_request: The JSON request dictionary to be sent to the server for browsing.
            get_full_details: If True, returns detailed information for each database; otherwise,
                returns a simple list of database names. Defaults to False.

        Returns:
            list: A list of all database names if `get_full_details` is False.
            dict: A dictionary mapping database names to their details (e.g., backup created time,
                database version) if `get_full_details` is True.

        Raises:
            SDKException: If the server response is empty or indicates a failure.

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request("GET", browse_request)

        full_result = []
        databases = []

        if flag:
            if response.json():
                if 'sqlDatabase' in response.json():
                    # returns whole dict if requested
                    if get_full_details:
                        return response.json()["sqlDatabase"]

                    for database in response.json()['sqlDatabase']:

                        database_name = database['databaseName']

                        created_time = datetime.datetime.fromtimestamp(
                            int(database['createdTime'])
                        ).strftime('%d-%m-%Y %H:%M:%S')

                        version = database['version']

                        temp = {
                            database_name: [created_time, version]
                        }

                        databases.append(database_name)
                        full_result.append(temp)

                return databases, full_result
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _recoverypoint_request_json(
        self,
        dbname: str,
        expire_days: int = 1,
        recovery_point_name: Optional[str] = None,
        point_in_time: int = 0,
        destination_instance: Optional[str] = None,
        snap: bool = False
    ) -> Dict[str, Any]:
        """Create and return a request JSON for SQL Server recovery point creation.

        This method constructs the request payload required to create a recovery point for a specified SQL Server database.
        The recovery point can be customized with an expiration period, a custom name, a specific point-in-time, a destination instance, and an option for snapshot setup.

        Args:
            dbname: Name of the database for which the recovery point is to be created.
            expire_days: Number of days the recovery point will be retained. Defaults to 1 day.
            recovery_point_name: Optional custom name for the recovery point. If not provided, a name is generated using the database name and a timestamp.
            point_in_time: Unix timestamp for point-in-time recovery. Defaults to 0, which restores to the last backup.
            destination_instance: Optional name of the destination SQL Server instance where the recovery point will be created. If None, uses the current instance.
            snap: Whether the recovery point is for a snapshot setup. Defaults to False.

        Returns:
            Dictionary representing the request JSON for creating the recovery point.

        #ai-gen-doc
        """

        if recovery_point_name is None:
            timestamp = datetime.datetime.timestamp(datetime.datetime.now())
            recovery_point_name = dbname + str(int(timestamp))

        instance = self
        if destination_instance != self.instance_name:
            instance = SQLServerInstance(self._agent_object, destination_instance)

        # fetching db details
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services["SQL_DATABASES"] % dbname, None
        )
        if flag:
            response = response.json()
            db_id = response["SqlDatabase"][0]["dbId"]
        else:
            raise SDKException('Response', 102, "failed to fetch db details")

        # fetching full database details
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services["SQL_DATABASE_DETAILS"] % (self.instance_id, db_id), None
        )
        if flag:
            response = response.json()
            db_details = response["SqlDatabase"][0]
        else:
            raise SDKException('Response', 102, "failed to fetch db details")

        fullbackup_job = db_details["fBkpJob"]
        if fullbackup_job is None:
            raise Exception("failed to get last full backup job details")

        job = self._commcell_object.job_controller.get(fullbackup_job)

        # retrieving the physical paths and logical file names
        restore_options = self._get_sql_restore_options([dbname])
        physical_files = []
        logical_files = []
        for files in restore_options["sqlDbdeviceItem"]:
            physical_files.append(files["fileName"])
            logical_files.append(files["logicalFileName"])

        request_json = {
            "opType": 0,
            "session": {},
            "queries": [{
                "type": 0,
                "queryId": "0"
            }],
            "mode": {
                "mode": 3
            },
            "advOptions": {
                "copyPrecedence": 0,
                "advConfig": {
                    "extendedConfig": {
                        "browseAdvConfigLiveBrowse": {
                            "useISCSIMount": False
                        }
                    },
                    "applicationMining": {
                        "appType": 81,
                        "agentVersion": 0,
                        "isApplicationMiningReq": True,
                        "browseInitReq": {
                            "database": dbname,
                            "bCreateRecoveryPoint": True,
                            "destDatabase": recovery_point_name,
                            "appMinType": 2 if not snap else 0,
                            "expireDays": expire_days,
                            "instance": {
                                "clientId": instance.properties["instance"]["clientId"],
                                "instanceName": instance.instance_name,
                                "instanceId": int(instance.instance_id),
                                "applicationId": 81
                            },
                            "miningJobs": [fullbackup_job],
                            "client": {
                                "clientId": self.properties["instance"]["clientId"]
                            },
                            "phyfileRename": physical_files,
                            "logfileRename": logical_files,
                        }
                    }
                }
            },
            "ma": {
                "clientId": self.properties["instance"]["clientId"]
            },
            "options": {
                "instantSend": True,
                "skipIndexRestore": False
            },
            "entity": {
                "drivePoolId": 0,
                "subclientId": job.details["jobDetail"]["generalInfo"]["subclient"]["subclientId"],
                "applicationId": 81,
                "libraryId": job.details["jobDetail"]["generalInfo"]["mediaLibrary"]["libraryId"],
                "backupsetId": job.details["jobDetail"]["generalInfo"]["subclient"]["backupsetId"],
                "instanceId": int(self.instance_id),
                "clientId": self.properties["instance"]["clientId"]
            },
            "timeRange": {
                "fromTime": 0,
                "toTime": point_in_time
            }
        }

        return request_json

    def _process_recovery_point_request(self, request_json: dict) -> tuple:
        """Process the create recovery job browse request for SQL Server.

        This method sends a recovery point creation request using the provided JSON payload,
        and returns the resulting Job object, the unique recovery point ID, and the name of the created database.

        Args:
            request_json: Dictionary containing the JSON request to be sent to the API for recovery point creation.

        Returns:
            tuple: A tuple containing:
                - Job: An instance of the Job class representing the restore job.
                - int: The unique recovery point ID.
                - str: The name of the database that is created.

        Raises:
            SDKException: If the restore job fails, the response is empty, or the response indicates failure.

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['BROWSE'], request_json
        )

        if flag:
            response_json = response.json()
            if response_json:
                if "browseResponses" in response_json:
                    d = response_json['browseResponses'][0]["browseResult"]["advConfig"]["applicationMining"]["browseInitResp"]
                    try:
                        return Job(self._commcell_object, d["recoveryPointJobID"]), d["recoveryPointID"], d["edbPath"]
                    except Exception as msg:
                        # server code 102 response is empty or doesn't contain required parameters
                        raise SDKException('Instance', 102, msg)

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'create recovery point job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Instance', '102', o_str)
                else:
                    raise SDKException('Instance', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _table_level_restore_request_json(
        self,
        src_db: str,
        tables_to_restore: list,
        destination_db: str,
        rp_name: str,
        include_child_tables: bool,
        include_parent_tables: bool
    ) -> dict:
        """Create and return a request JSON for performing a table-level restore in SQL Server.

        Args:
            src_db: Name of the source database from which tables will be restored.
            tables_to_restore: List of table names to restore from the source database.
            destination_db: Name of the destination database where tables will be restored.
            rp_name: Name of the recovery point to use for the restore operation.
            include_child_tables: If True, include all child tables related to the selected tables in the restore.
            include_parent_tables: If True, include all parent tables related to the selected tables in the restore.

        Returns:
            A dictionary representing the request JSON for the table-level restore operation.

        Example:
            >>> request_json = instance._table_level_restore_request_json(
            ...     src_db="SalesDB",
            ...     tables_to_restore=["Orders", "Customers"],
            ...     destination_db="SalesDB_Restore",
            ...     rp_name="RP_2023_10_01",
            ...     include_child_tables=True,
            ...     include_parent_tables=False
            ... )
            >>> print(request_json)
            # The returned dictionary can be used to initiate a table-level restore request.

        #ai-gen-doc
        """

        client_name = self._agent_object._client_object.client_name
        client_id = int(self._agent_object._client_object.client_id)
        instance_name = self.instance_name
        instance_id = int(self.instance_id)

        source_item = []
        for table in tables_to_restore:
            source_item.append('/' + table)

        request_json = {
            "taskInfo": {
                "associations": [{
                    "subclientId": -1,
                    "copyId": 0,
                    "applicationId": 81,
                    "clientName": client_name,
                    "backupsetId": -1,
                    "instanceId": instance_id,
                    "clientId": client_id,
                    "instanceName": instance_name,
                    "_type_": 5,
                    "appName": self._agent_object.agent_name
                }],
                "task": {
                    "ownerId": 1,
                    "taskType": 1,
                    "ownerName": "admin",
                    "sequenceNumber": 0,
                    "initiatedFrom": 1,
                    "policyType": 0,
                    "taskId": 0,
                    "taskFlags": {
                        "isEZOperation": False,
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 3,
                            "operationType": 1001
                        },
                        "options": {
                            "adminOpts": {
                                "contentIndexingOption": {
                                    "subClientBasedAnalytics": False
                                }
                            },
                            "restoreOptions": {
                                "virtualServerRstOption": {
                                    "isBlockLevelReplication": False
                                },
                                "sqlServerRstOption": {
                                    "cloneEnv": False,
                                    "ffgRestore": False,
                                    "cloneResrvTimePeriod": 0,
                                    "vSSBackup": False,
                                },
                                "dbArchiveRestoreOptions": {
                                    "restoreAllDependentTables": include_child_tables,
                                    "isTableLevelRestore": True,
                                    "destDatabaseName": destination_db,
                                    "restoreToSourceDatabase": True,
                                    "restoreToHistoryDatabase": False,
                                    "restoreAllParentTables": include_parent_tables,
                                    "databaseName": {
                                        "clientId": client_id,
                                        "instanceName": instance_name,
                                        "instanceId": instance_id,
                                        "applicationId": 81
                                    },
                                    "sqlArchiveOptions": {
                                        "sourceDBName": src_db,
                                        "sourceDatabaseInfo": {
                                            "dbName": rp_name,
                                            "instance": {
                                                "clientId": client_id,
                                                "instanceName": instance_name,
                                                "instanceId": instance_id,
                                                "applicationId": 81
                                            }
                                        }
                                    }
                                },
                                "browseOption": {
                                    "listMedia": False,
                                    "useExactIndex": False,
                                    "noImage": True,
                                    "commCellId": self._commcell_object.commcell_id,
                                    "mediaOption": {
                                        "useISCSIMount": False,
                                        "mediaAgent": {
                                            "mediaAgentId": 0,
                                            "_type_": 11
                                        },
                                        "library": {
                                            "_type_": 9,
                                            "libraryId": 0
                                        },
                                        "copyPrecedence": {
                                            "copyPrecedenceApplicable": False
                                        },
                                        "drivePool": {
                                            "_type_": 47,
                                            "drivePoolId": 0
                                        }
                                    },
                                    "backupset": {
                                        "backupsetId": -1,
                                        "clientId": client_id
                                    },
                                    "timeRange": {}
                                },
                                "commonOptions": {
                                    "clusterDBBackedup": False,
                                    "restoreToDisk": False,
                                    "isDBArchiveRestore": True,
                                    "copyToObjectStore": False,
                                    "onePassRestore": False,
                                    "syncRestore": False
                                },
                                "destination": {
                                    "destClient": {
                                        "clientId": client_id,
                                        "clientName": client_name
                                    }
                                },
                                "fileOption": {
                                    "sourceItem": source_item,
                                    "browseFilters": [
                                        "<?xml version='1.0' encoding='UTF-8'?>"
                                        "<databrowse_Query type=\"0\" queryId=\"0\" />"
                                    ]
                                },
                                "dbDataMaskingOptions": {
                                    "isStandalone": False
                                }
                            },
                            "commonOpts": {
                                "notifyUserOnJobCompletion": False,
                                "perfJobOpts": {
                                    "rstPerfJobOpts": {
                                        "mediaReadSpeed": False,
                                        "pipelineTransmittingSpeed": False
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
        return request_json

    def _get_ag_groups(self) -> dict:
        """Retrieve available Availability Groups from the primary replica.

        Returns:
            dict: A dictionary containing SQL destination server options for the available Availability Groups.

        Raises:
            SDKException: If a specified Availability Group name does not exist for this SQL Server instance.

        #ai-gen-doc
        """

        instance_id = int(self.instance_id)
        client_id = int(self.properties['instance']['clientId'])

        webservice = self._commcell_object._services['SQL_AG_GROUPS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            "GET", webservice % (client_id, instance_id)
        )

        if flag:
            if response.json():
                if 'SQLAvailabilityGroupList' in response.json():
                    return response.json()['SQLAvailabilityGroupList']
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Instance', '102', 'No Availability Groups exist for given primary replica '
                                                      'or SQL services are down on target server.')

    def _get_ag_group_replicas(self, ag_group_name: str) -> dict:
        """Retrieve the list of replicas for a specified SQL Server Availability Group.

        Args:
            ag_group_name: The name of the Availability Group for which to fetch replica information.

        Returns:
            A dictionary containing details of the replicas associated with the specified SQL AG group.

        Raises:
            SDKException: If no replicas exist for the given Availability Group.

        #ai-gen-doc
        """

        instance_id = int(self.instance_id)
        client_id = int(self.properties['instance']['clientId'])

        webservice = self._commcell_object._services['SQL_AG_GROUP_REPLICAS']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            "GET", webservice %(client_id, instance_id, ag_group_name)
        )

        if flag:
            if response.json():
                if 'SQLAvailabilityReplicasList' in response.json():
                    return response.json()
                else:
                    raise SDKException('Instance', '102', 'No replicas exist for given Availability Group '
                                                          'or SQL services are down on target server.')
            else:
                raise SDKException('Response', '102')

    def backup(self) -> List['Job']:
        """Run a full backup job for all subclients in this SQL Server instance.

        This method initiates full backup jobs for each subclient within the backupset 
        associated with this SQL Server instance. It returns a list of job objects 
        representing the backup jobs that were started.

        Returns:
            List[Job]: A list containing Job objects for each subclient's full backup job.

        #ai-gen-doc
        """
        return_list = []
        thread_list = []

        all_subclients = self.subclients._subclients

        if all_subclients:
            for subclient in all_subclients:
                thread = threading.Thread(
                    target=self._run_backup, args=(subclient, return_list)
                )
                thread_list.append(thread)
                thread.start()

        for thread in thread_list:
            thread.join()

        return return_list

    def browse(self, get_full_details: bool = False) -> Union[list, dict]:
        """Retrieve the list of backed up databases for this SQL Server instance.

        Args:
            get_full_details: If True, returns a dictionary with all databases and their last full backup job details.
                If False (default), returns a simple list of all database names.

        Returns:
            list: A list of all backed up database names if get_full_details is False.
            dict: A dictionary mapping database names to details such as backup creation time and database version if get_full_details is True.

        Raises:
            SDKException: If the response is empty or the response indicates failure.

        Example:
            >>> instance = SQLServerInstance()
            >>> # Get a simple list of backed up databases
            >>> db_list = instance.browse()
            >>> print(db_list)
            ['Database1', 'Database2', 'Database3']

            >>> # Get detailed information about each backed up database
            >>> db_details = instance.browse(get_full_details=True)
            >>> print(db_details)
            {
                'Database1': {'last_backup_time': '2023-12-01 10:00:00', 'version': '15.0'},
                'Database2': {'last_backup_time': '2023-12-02 12:30:00', 'version': '14.0'}
            }

        #ai-gen-doc
        """
        browse_request = self._commcell_object._services['INSTANCE_BROWSE'] % (
            self._agent_object._client_object.client_id, "SQL", self.instance_id
        )

        return self._process_browse_request(browse_request, get_full_details=get_full_details)

    def browse_in_time(
        self,
        from_date: Optional[Union[str, int]] = None,
        to_date: Optional[Union[str, int]] = None,
        full_details: Optional[bool] = None
    ) -> Union[List[str], Dict[str, Any]]:
        """Retrieve a list of backed up databases for this SQL Server instance within a specified time frame.

        Args:
            from_date: The start date/time for browsing backups. Accepts a string in the format 'dd/MM/YYYY', 
                'dd/MM/YYYY HH:MM:SS', or an integer timestamp. If not specified, defaults to 01/01/1970.
            to_date: The end date/time for browsing backups. Accepts a string in the format 'dd/MM/YYYY', 
                'dd/MM/YYYY HH:MM:SS', or an integer timestamp. If not specified, defaults to the current date.
            full_details: If True, returns detailed information for each database, including backup creation time 
                and database version. If False or None, returns only the list of database names.

        Returns:
            If full_details is False or None:
                List of database names (str) that have backups in the specified time frame.
            If full_details is True:
                Dictionary mapping database names (str) to their details (such as backup creation time and version).

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> # Get all backed up databases from 01/01/2023 to 31/01/2023
            >>> db_list = sql_instance.browse_in_time(from_date='01/01/2023', to_date='31/01/2023')
            >>> print(db_list)
            >>> 
            >>> # Get detailed backup information for all databases in the last week
            >>> import time
            >>> one_week_ago = int(time.time()) - 7*24*60*60
            >>> db_details = sql_instance.browse_in_time(from_date=one_week_ago, full_details=True)
            >>> for db, details in db_details.items():
            >>>     print(f"{db}: {details}")

        #ai-gen-doc
        """
        regex_date = r"\d{1,2}/\d{1,2}/\d{4}"
        regex_datetime = regex_date + r"\s+\d{2}:\d{2}:\d{2}"
        if not isinstance(from_date, int):
            if from_date and bool(re.search(regex_datetime, from_date)):
                from_date = int(time.mktime(time.strptime(from_date, '%d/%m/%Y %H:%M:%S' )))
            elif from_date and bool(re.search(regex_date, from_date)):
                from_date = int(time.mktime(time.strptime(from_date, '%d/%m/%Y')))
            else:
                from_date = 0
        if not isinstance(to_date, int):
            if to_date and bool(re.search(regex_datetime, to_date)):
                to_date = int(time.mktime(time.strptime(to_date, '%d/%m/%Y %H:%M:%S')))
            elif to_date and bool(re.search(regex_date, to_date)):
                to_date = int(time.mktime(time.strptime(to_date, '%d/%m/%Y')))
            else:
                to_date = int(time.time())

        browse_request = self._commcell_object._services['INSTANCE_BROWSE'] % (
            self._agent_object._client_object.client_id, "SQL", self.instance_id
        )

        browse_request += '?fromTime={0}&toTime={1}'.format(from_date, to_date)

        return self._process_browse_request(browse_request, full_details)

    def restore(
        self,
        content_to_restore: list,
        drop_connections_to_databse: bool = False,
        overwrite: bool = True,
        restore_path: str = None,
        to_time: 'Union[int, str, None]' = None,
        sql_restore_type: str = SQLDefines.DATABASE_RESTORE,
        sql_recover_type: str = SQLDefines.STATE_RECOVER,
        undo_path: str = None,
        restricted_user: bool = None,
        destination_instance: str = None,
        **kwargs
    ) -> 'Union[Job, Schedule]':
        """Restore the specified SQL Server databases from backup.

        This method initiates a restore operation for the provided list of databases, with options to control
        overwrite behavior, restore paths, recovery state, and advanced SQL Server restore settings.

        Args:
            content_to_restore: List of database names to restore.
            drop_connections_to_databse: If True, drops existing connections to the database before restore. Defaults to False.
            overwrite: If True, unconditionally overwrites existing files during restore. Defaults to True.
            restore_path: Optional. Path on disk where the database should be restored. Defaults to None.
            to_time: Optional. Point-in-time to restore to, as an integer timestamp or string in 'yyyy-MM-dd HH:mm:ss' format.
            sql_restore_type: Optional. Type of SQL restore operation (e.g., 'DATABASE_RESTORE', 'STEP_RESTORE', 'RECOVER_ONLY').
            sql_recover_type: Optional. SQL recovery state after restore (e.g., 'STATE_RECOVER', 'STATE_NORECOVER', 'STATE_STANDBY').
            undo_path: Optional. File path for undo file (used in standby restores).
            restricted_user: Optional. If True, restores the database in restricted user mode.
            destination_instance: Optional. Name of the destination SQL Server instance for the restore.

        Keyword Args:
            point_in_time: Optional[int]. Time value to use for point-in-time restore.
            schedule_pattern: Optional[dict]. Schedule pattern for scheduling the restore job.
            hardware_revert: Optional[bool]. If True, performs a hardware revert. Defaults to False.
            log_shipping: Optional[bool]. If True, restores log backups in standby or no recovery state.

        Returns:
            Job: Instance of the Job class representing the restore job.
            Schedule: Instance of the Schedule class if the restore is scheduled.

        Raises:
            SDKException: If content_to_restore is not a list, or if the restore response is empty or unsuccessful.

        Example:
            >>> # Restore a single database with default options
            >>> job = sql_instance.restore(['MyDatabase'])
            >>> print(f"Restore job started: {job}")

            >>> # Restore multiple databases to a specific path and point in time
            >>> job = sql_instance.restore(
            ...     ['DB1', 'DB2'],
            ...     restore_path='D:\\SQLRestores',
            ...     to_time='2023-12-01 10:00:00'
            ... )
            >>> print(f"Restore job started: {job}")

            >>> # Schedule a restore job with a custom schedule pattern
            >>> schedule_pattern = {'freq_type': 'daily', 'active_start_time': '02:00'}
            >>> schedule = sql_instance.restore(
            ...     ['MyDatabase'],
            ...     schedule_pattern=schedule_pattern
            ... )
            >>> print(f"Scheduled restore: {schedule}")

        #ai-gen-doc
        """
        if not isinstance(content_to_restore, list):
            raise SDKException('Instance', '101')

        if destination_instance is not None:
            destination_instance = destination_instance.lower()

        request_json = self._restore_request_json(
            content_to_restore,
            drop_connections_to_databse=drop_connections_to_databse,
            overwrite=overwrite,
            restore_path=restore_path,
            to_time=to_time,
            sql_restore_type=sql_restore_type,
            sql_recover_type=sql_recover_type,
            undo_path=undo_path,
            restricted_user=restricted_user,
            destination_instance=destination_instance,
            **kwargs
        )

        return self._process_restore_response(request_json)

    def restore_to_destination_server(
        self,
        content_to_restore: list,
        destination_server: str,
        drop_connections_to_databse: bool = False,
        overwrite: bool = True,
        restore_path: str = None
    ) -> 'Job':
        """Restore specified SQL Server databases to a destination server.

        This method initiates a restore operation for the given list of databases, allowing you to specify
        the destination server, whether to drop existing connections, whether to overwrite existing files,
        and an optional restore path.

        Args:
            content_to_restore: List of database names to restore.
            destination_server: Name of the destination SQL Server instance.
            drop_connections_to_databse: If True, drops active connections to the database before restore. Defaults to False.
            overwrite: If True, unconditionally overwrites files during restore. Defaults to True.
            restore_path: Optional. Path on disk where the databases should be restored. If None, uses default location.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If content_to_restore is not a list, if the response is empty, or if the restore operation fails.

        Example:
            >>> databases = ['SalesDB', 'HRDB']
            >>> job = sql_instance.restore_to_destination_server(
            ...     content_to_restore=databases,
            ...     destination_server='SQLServer02\\Instance1',
            ...     drop_connections_to_databse=True,
            ...     overwrite=True,
            ...     restore_path='D:\\SQLRestores'
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not isinstance(content_to_restore, list):
            raise SDKException('Instance', '101')

        request_json = self._restore_request_json(
            content_to_restore,
            drop_connections_to_databse=drop_connections_to_databse,
            overwrite=overwrite,
            restore_path=restore_path,
            destination_instance=destination_server
        )

        return self._process_restore_response(request_json)

    def get_recovery_points(self) -> tuple:
        """List all recovery points and clones for the SQL Server instance.

        Returns:
            tuple: A list containing all recovery points and clones associated with the SQL Server instance.

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services["SQL_CLONES"], None
        )
        if flag:
            response_json = response.json()
            if "rpObjectList" in response_json:
                return response_json["total"], response_json["rpObjectList"]
            return 0, None
        raise SDKException('Response', '102', "failed to get recovery points")

    def create_recovery_point(
        self,
        database_name: str,
        new_database_name: Optional[str] = None,
        destination_instance: Optional[str] = None,
        expire_days: int = 1,
        snap: bool = False
    ) -> tuple:
        """Start a granular restore or recovery point job and create an on-demand restore of a SQL Server database.

        This method initiates a restore or recovery point job for the specified database, optionally creating a new database
        with a custom name and/or on a different SQL Server instance. The recovery point will be available for the specified
        number of days. Optionally, a recovery point can be created for a snapshot setup.

        Args:
            database_name: Name of the database to perform granular restore or recovery point creation.
            new_database_name: Name for the newly created database. If None, a name is generated using the original database name and a timestamp.
            destination_instance: Name of the destination SQL Server instance. If None, the database is restored to the same instance.
            expire_days: Number of days the recovery point will be available. Default is 1 day.
            snap: Whether to create a recovery point for a snapshot setup. Default is False.

        Returns:
            A tuple containing:
                - Job: An instance of the Job class representing the restore job.
                - int: The unique recovery point ID.
                - str: The name of the created recovery point database.

        Example:
            >>> # Create a recovery point for 'SalesDB' and restore as 'SalesDB_Restore' on the same instance
            >>> job, recovery_point_id, recovery_db_name = sql_instance.create_recovery_point(
            ...     database_name='SalesDB',
            ...     new_database_name='SalesDB_Restore',
            ...     expire_days=3
            ... )
            >>> print(f"Job ID: {job}, Recovery Point ID: {recovery_point_id}, Database Name: {recovery_db_name}")

        #ai-gen-doc
        """
        # write a wrapper over this to allow creating more than one recovery points at a time is neccessary
        if not isinstance(database_name, str):
            raise SDKException('Instance', '101')

        if destination_instance is None:
            destination_instance = self.instance_name
        else:
            destination_instance = destination_instance.lower()

        recoverypoint_request = self._recoverypoint_request_json(
            database_name,
            expire_days=expire_days,
            recovery_point_name=new_database_name,
            destination_instance=destination_instance,
            snap=snap
        )
        return self._process_recovery_point_request(recoverypoint_request)

    def table_level_restore(
        self,
        src_db_name: str,
        tables_to_restore: list,
        destination_db_name: str,
        rp_name: str,
        include_child_tables: bool,
        include_parent_tables: bool
    ) -> 'Job':
        """Initiate a table-level restore operation for a SQL Server database.

        This method starts a restore job to recover specific tables from a source database to a destination database,
        using a specified recovery point. You can choose to include related child and/or parent tables in the restore.

        Args:
            src_db_name: Name of the source SQL Server database from which tables will be restored.
            tables_to_restore: List of table names to restore from the source database.
            destination_db_name: Name of the destination database where tables will be restored.
            rp_name: Name of the recovery point to use for the restore operation.
            include_child_tables: If True, includes all child tables related to the specified tables in the restore.
            include_parent_tables: If True, includes all parent tables related to the specified tables in the restore.

        Returns:
            Job: An instance of the Job class representing the initiated restore job.

        Example:
            >>> instance = SQLServerInstance()
            >>> job = instance.table_level_restore(
            ...     src_db_name="SalesDB",
            ...     tables_to_restore=["Orders", "Customers"],
            ...     destination_db_name="SalesDB_Restore",
            ...     rp_name="RP_2023_10_01",
            ...     include_child_tables=True,
            ...     include_parent_tables=False
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        if not (isinstance(src_db_name, str)
                or isinstance(tables_to_restore, list)
                or isinstance(destination_db_name, str)):
            raise SDKException('Instance', '101')

        request_json = self._table_level_restore_request_json(
            src_db_name,
            tables_to_restore,
            destination_db_name,
            rp_name,
            include_child_tables,
            include_parent_tables
        )

        return self._process_restore_response(request_json)

    def vss_option(self, value: bool) -> None:
        """Enable or disable the VSS (Volume Shadow Copy Service) option on the SQL Server instance.

        Args:
            value: Set to True to enable VSS option, or False to disable it.

        #ai-gen-doc
        """

        request_json = {
            "useVss": value
        }

        self._set_instance_properties("_mssql_instance_prop", request_json)

    def vdi_timeout(self, value: int) -> None:
        """Set the SQL VDI (Virtual Device Interface) timeout value for the SQL Server instance.

        This method configures the timeout duration (in seconds) for SQL VDI operations on the instance.

        Args:
            value: The timeout value in seconds to be set for SQL VDI operations.

        #ai-gen-doc
        """

        request_json = {
            "vDITimeOut": value
        }

        self._set_instance_properties("_mssql_instance_prop", request_json)

    def impersonation(self, enable: bool, credentials: Optional[str] = None) -> None:
        """Enable or disable impersonation on the SQL Server instance.

        This method sets impersonation for the SQL Server instance using either the local system account 
        or the provided credentials. If impersonation is enabled and no credentials are specified, 
        the local system account will be used by default.

        Args:
            enable: Set to True to enable impersonation, or False to disable it.
            credentials: Optional. The name of the credentials to use for impersonation. If not provided 
                and impersonation is enabled, the local system account will be used.

        Example:
            >>> sql_instance = SQLServerInstance()
            >>> # Enable impersonation using the local system account
            >>> sql_instance.impersonation(True)
            >>> # Enable impersonation using specific credentials
            >>> sql_instance.impersonation(True, credentials="sql_admin_creds")
            >>> # Disable impersonation
            >>> sql_instance.impersonation(False)

        #ai-gen-doc
        """

        if enable and credentials is None:
            impersonate_json = {
                "overrideHigherLevelSettings": {
                    "overrideGlobalAuthentication": True,
                    "useLocalSystemAccount": True
                }
            }
        elif enable and credentials is not None:
            impersonate_json = {
                "overrideHigherLevelSettings": {
                    "overrideGlobalAuthentication": True,
                    "useLocalSystemAccount": False
                },
                "MSSQLCredentialinfo": {
                    "credentialName": credentials
                }
            }
        else:
            impersonate_json = {
                "overrideHigherLevelSettings": {
                    "overrideGlobalAuthentication": True,
                    "useLocalSystemAccount": False
                }
            }

        self._set_instance_properties("_mssql_instance_prop", impersonate_json)

    def create_sql_ag(self, client_name: str, ag_group_name: str, credentials: Optional[str] = None) -> 'Instance':
        """Create a new SQL Availability Group (AG) client and instance.

        This method provisions a new SQL AG client and its associated instance using the specified client name 
        and availability group name. Optionally, impersonation credentials can be provided.

        Args:
            client_name: The name to assign to the new Availability Group client.
            ag_group_name: The name of the Availability Group to create.
            credentials: Optional. The name of the credentials to use for impersonation. If not provided, 
                no impersonation is used.

        Returns:
            Instance: An instance of the Instance class representing the newly created Availability Group.

        Raises:
            SDKException: If the Availability Group for the given primary replica does not exist,
                if the Availability Group client or instance fails to be created,
                or if the specified credentials for impersonation do not exist.

        #ai-gen-doc
        """
        # If credentials passed, verify it exists
        if credentials:
            if not credentials in self._commcell_object.credentials.all_credentials:
                raise SDKException(
                    'Credential', '102', 'Credential name provided does not exist in the commcell.'
                )

        # Get the available AG groups configured on SQL Instance
        ag_groups_resp = self._get_ag_groups()

        # Verify the provided AG group exists from available AG groups on primary replica
        if not any(ag['name'] == ag_group_name for ag in ag_groups_resp):
            raise SDKException(
                'Instance', '102', 'Availability Group with provided name does not exist for given replica.'
            )
        for ag_group in ag_groups_resp:
            if ag_group['name'].lower() == ag_group_name.lower():
                ag_group_endpointURL = ag_group['endpointURL']
                ag_group_backupPref = ag_group['backupPreference']
                ag_primary_replica_server = ag_group['primaryReplicaServerName']

                ag_group_listener_list = []
                if 'SQLAvailabilityGroupListenerList' in ag_group:
                    for listener in ag_group['SQLAvailabilityGroupListenerList']:
                        listener_details = {
                            'availabilityGroupListenerName': listener['availabilityGroupListenerName']
                        }
                        ag_group_listener_list.append(listener_details)

        # Get the replicas from the provided AG group
        ag_group_replicas_resp = self._get_ag_group_replicas(ag_group_name)

        request_json = {
            "App_CreatePseudoClientRequest": {
                "clientInfo": {
                    "clientType": 20,
                    "mssqlagClientProperties": {
                        "SQLServerInstance": {
                            "clientId": int(self.properties['instance']['clientId']),
                            "instanceId": int(self.instance_id)
                        },
                        "availabilityGroup": {
                            "name": ag_group_name,
                            "primaryReplicaServerName": ag_primary_replica_server,
                            "backupPreference": ag_group_backupPref,
                            "endpointURL": ag_group_endpointURL
                        },
                        "SQLAvailabilityReplicasList": ag_group_replicas_resp,
                    },
                },
                "entity": {
                    "clientName": client_name
                }
            }
        }
        if ag_group_listener_list:
            request_json['App_CreatePseudoClientRequest']['clientInfo']['mssqlagClientProperties']\
            ['availabilityGroup']['SQLAvailabilityGroupListenerList'] = ag_group_listener_list

        webservice = self._commcell_object._services['EXECUTE_QCOMMAND']

        flag, response = self._cvpysdk_object.make_request(
            'POST', webservice, request_json)

        if flag:
            if response.json():
                if 'response' in response.json():
                    error_code = response.json()['response']['errorCode']

                    if error_code != 0:
                        error_string = response.json()['response']['errorString']
                        o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                        raise SDKException('Client', '102', o_str)
                    else:
                        self._commcell_object.refresh()

                        # Get newly created AG instance
                        ag_client = self._commcell_object.clients.get(
                            response.json()['response']['entity']['clientName']
                        )
                        agent = ag_client.agents.get(self._agent_object.agent_name)
                        if ag_group_listener_list:
                            ag_instance_name = ag_group_listener_list[0]['availabilityGroupListenerName'] \
                                               + '/' + ag_group_name
                        else:
                            ag_instance_name = ag_group_name
                        ag_instance = agent.instances.get(ag_instance_name)
                        if credentials is not None:
                            ag_instance.impersonation(True, credentials)

                        return ag_instance
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to create client\nError: "{0}"'.format(error_string)

                    raise SDKException('Client', '102', o_str)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def database_details(self, database_name: str) -> Optional[dict]:
        """Retrieve detailed information for a specific SQL Server database.

        Args:
            database_name: The name of the database for which details are to be retrieved.

        Returns:
            A dictionary containing the details of the specified database, such as configuration, status, and other relevant properties.

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._commcell_object._services['SQL_DATABASE'] %(self.instance_id, database_name), None
        )
        if flag:
            response_json = response.json()
            if 'SqlDatabase' in response_json:
                for database in response_json['SqlDatabase']:
                    if database_name == database['dbName']:
                        return database
            return None
        raise SDKException('Response', '102', "Failed to get the database details")
