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

    _recoverypoint_request_json()   -- returns a json to be sent to server to create
                                            a recovery point

    get_recovery_points()         --    lists all the recovery points

    _process_recovery_point_request() --  starts the recovery point job and process
                                                the response

    backup()                        --  runs full backup for all subclients associated
                                            with this instance

    browse()                        --  gets the content of the backup for this instance

    browse_in_time()                --  gets the content of the backup for this instance
                                            in the time range specified

    restore()                       --  runs the restore job for specified

    restore_to_destination_server() --  restores the database on destination server

    create_recovery_point()         --  creates a recovery point on destination server

    table_level_restore()           --  starts the table level restore job

    _table_level_restore_request_json() --  returns a json to be sent to the server for
                                            table level restore job

"""

from __future__ import unicode_literals

import re
import time
import datetime
import threading
from base64 import b64encode

from ..instance import Instance
from ..exception import SDKException
from ..job import Job
from ..constants import SQLDefines


class SQLServerInstance(Instance):
    """Derived class from Instance Base class, representing a SQL Server instance,
        and to perform operations on that Instance."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        super(SQLServerInstance, self)._get_instance_properties()

        self._mssql_instance_prop = self._properties.get('mssqlInstance', {})

    def _get_instance_properties_json(self):
        """get the all instance related properties of this instance.

           Returns:
                dict - all subclient properties put inside a dict

        """
        instance_json = {
            "instanceProperties":
                {
                    "instance": self._instance,
                    "instanceActivityControl": self._instanceActivityControl,
                    "mssqlInstance": self._mssql_instance_prop,
                    "contentOperationType": 1
                }
        }
        return instance_json

    def _restore_request_json(
            self,
            content_to_restore,
            restore_path=None,
            drop_connections_to_databse=False,
            overwrite=True,
            destination_instance=None,
            to_time=None,
            sql_restore_type=SQLDefines.DATABASE_RESTORE,
            sql_recover_type=SQLDefines.STATE_RECOVER,
            undo_path=None,
            restricted_user=None
    ):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                content_to_restore (list): databases list to restore

                restore_path (list, optional): list of dicts for restore paths of database files

                drop_connections_to_databse (bool, optional): drop connections to database during restore

                overwrite (bool, optional): overwrite database on restore

                destination_instance (str): restore databases to this sql instance

                to_time (str, optional): restore to time

                sql_restore_type (str, optional): type of sql restore state
                (DATABASE_RESTORE, STEP_RESTORE, RECOVER_ONLY)

                sql_recover_type (str, optional): type of sql restore state
                (STATE_RECOVER, STATE_NORECOVER, STATE_STANDBY)

                undo_path (str, optional): file path for undo path for sql server standby restore

                restricted_user (bool, optional): Restore database in restricted user mode

            Returns:
                dict - JSON request to pass to the API
        """

        self._get_sql_restore_options(content_to_restore)

        if destination_instance is None:
            destination_instance = (self.instance_name).lower()
        else:
            if destination_instance not in self.destination_instances_dict:
                raise SDKException(
                    'Instance',
                    '102',
                    'No Instance exists with name: {0}'.format(destination_instance)
                )

        destination_client_id = int(
            self.destination_instances_dict[destination_instance]['clientId']
        )

        destination_instance_id = int(
            self.destination_instances_dict[destination_instance]['instanceId']
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
                                "restoreSource": content_to_restore
                            },
                            "commonOptions": {
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
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'sqlServerRstOption'].update(restore_path_dict)

        if restricted_user is not None:
            restricted_user_dict = {
                "dbOnly":
                    restricted_user
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'sqlServerRstOption'].update(restricted_user_dict)

        if to_time is not None:
            to_time_dict = {
                "browseOption": {
                    "timeRange": {
                        "toTimeValue": to_time
                    }
                }
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(to_time_dict)

        return request_json

    def _process_restore_response(self, request_json):
        """Runs the CreateTask API with the request JSON provided for Restore,
            and returns the contents after parsing the response.

            Args:
                request_json (dict):  JSON request to run for the API

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if restore job failed

                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['RESTORE'], request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    time.sleep(1)
                    return Job(self._commcell_object, response.json()['jobIds'][0])
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

    def _get_sql_restore_options(self, content_to_restore):
        """Runs the SQL/Restoreoptions API with the request JSON provided,
            and returns the contents after parsing the response.

            Args:
                content_to_restore (list):  Databases list to restore

            Returns:
                dict - dictionary consisting of the sql destination server options

            Raises:
                SDKException:
                    if failed to get SQL instances

                    if no instance exits on commcell

                    if response is empty

                    if response is not success
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

    def _run_backup(self, subclient_name, return_list):
        """Triggers full backup job for the given subclient, and appends its Job object to list
            The SDKExcpetion class instance is appended to the list,
            if any exception is raised while running the backup job for the Subclient.

            Args:
                subclient_name (str):  Name of the subclient to trigger the backup for

                return_list (list):  List to append the job object to
        """
        try:
            job = self.subclients.get(subclient_name).backup('Full')
            if job:
                return_list.append(job)
        except SDKException as excp:
            return_list.append(excp)

    def _process_browse_request(self, browse_request, get_full_details=False):
        """Runs the SQL Instance Browse API with the request JSON provided for the operation
            specified, and returns the contents after parsing the response.

            Args:
                browse_request (dict):  JSON request to be sent to Server

            Returns:
                list - list of all databases

                dict - database names along with details like backup created time
                           and database version

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
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

    def backup(self):
        """Run full backup job for all subclients in this instance.

            Returns:
                list - list containing the job objects for the full backup jobs started for
                           the subclients in the backupset
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

    def browse(self, get_full_details=False):
        """Gets the list of the backed up databases for this instance.
            Args:
                get_full_details (bool) - if True returns dict with all databases
                            with last full backupjob details, default false
            Returns:
                list - list of all databases

                dict - database names along with details like backup created time
                           and database version

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        browse_request = self._commcell_object._services['INSTANCE_BROWSE'] % (
            self._agent_object._client_object.client_id, "SQL", self.instance_id
        )

        return self._process_browse_request(browse_request, get_full_details=get_full_details)

    def browse_in_time(self, from_date=None, to_date=None):
        """Gets the list of the backed up databases for this instance in the given time frame.

            Args:
                from_date (str): date to get the contents after.  Format: dd/MM/YYYY
                Gets contents from 01/01/1970 if not specified.  Defaults to None.

                to_date (str): date to get the contents before.  Format: dd/MM/YYYY
                Gets contents till current day if not specified.  Defaults to None.

            Returns:
                list - list of all databases

                dict - database names along with details like backup created timen
                           and database version

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        if from_date and (from_date != '01/01/1970' and from_date != '1/1/1970'):
            temp = from_date.split('/')
            if (len(temp) == 3 and
                    0 < int(temp[0]) < 32 and
                    0 < int(temp[1]) < 13 and
                    int(temp[2]) > 1969 and
                    (re.search(r'\d\d/\d\d/\d\d\d\d', from_date) or
                     re.search(r'\d/\d/\d\d\d\d', from_date))):
                from_date = int(time.mktime(time.strptime(from_date, '%d/%m/%Y')))
            else:
                raise SDKException('Instance', '103')
        else:
            from_date = 0

        if to_date and (to_date != '01/01/1970' and to_date != '1/1/1970'):
            temp = to_date.split('/')
            if (len(temp) == 3 and
                    0 < int(temp[0]) < 32 and
                    0 < int(temp[1]) < 13 and
                    int(temp[2]) > 1969 and
                    (re.search(r'\d\d/\d\d/\d\d\d\d', to_date) or
                     re.search(r'\d/\d/\d\d\d\d', to_date))):
                today = time.strftime('%d/%m/%Y')
                if today == to_date:
                    to_date = int(time.time())
                else:
                    to_date = int(time.mktime(time.strptime(to_date, '%d/%m/%Y')))
            else:
                raise SDKException('Instance', '103')
        else:
            to_date = int(time.time())

        browse_request = self._commcell_object._services['INSTANCE_BROWSE'] % (
            self._agent_object._client_object.client_id, "SQL", self.instance_id
        )

        browse_request += '?fromTime={0}&toTime={1}'.format(from_date, to_date)

        return self._process_browse_request(browse_request)

    def get_recovery_points(self):
        """
        lists all the recovery points.

        returns:
            object (list) - list of all the recovery points and clones
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

    def _recoverypoint_request_json(self,
                                    dbname,
                                    expire_days=1,
                                    recovery_point_name=None,
                                    point_in_time=0,
                                    destination_instance=None,
                                    snap=False
                                    ):
        """
            creates and returns a request json for the recovery point creation

            Args:
                dbname (str) -- database to be restored

                expire_days (int)   -- days for which the database will be restored
                        default 1,. 1 day
                recovery_point_name (str)  -- name of the recovery point to be created
                        default None. creates a db with db_name + <timestamp>

                point_in_time   (timestamp) -- unix time for the point in time recovery point creation
                        default 0.  performs restore to last backup

                destination_instance (str)  -- name of the destination instance in which recovery point is to be
                                                created.
                                default None. creates in the same instance

                snap    (bool)      -- If the recovery point to be created is for snap setup
                            default False
            returns:
                request_json (Dict) --   request json for create recovery points
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
            'GET', self._commcell_object._services["SQL_DATABASE_DETAILS"] %(self.instance_id, db_id), None
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
            "queries": [
                {
                    "type": 0,
                    "queryId": "0"
                }
            ],
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

    def _process_recovery_point_request(self, request_json):
        """
            process the create recovery job browse request
            Args:
                request_json (dict):  JSON request to run for the API

            Returns:
                object (Job) - instance of the Job class for this restore job

                recovery point Id (int) : id to uniquely access the recovery point

                dbname (str) - name of the db that is created.

            Raises:
                SDKException:
                    if restore job failed

                    if response is empty

                    if response is not success

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

    def create_recovery_point(self,
                              database_name,
                              new_database_name=None,
                              destination_instance=None,
                              expire_days=1,
                              snap=False
                              ):
        """stats a granular restore or recovery point job and creates a on demand restore of a database

        agrs:
            database_name (str) :   Name of the database for granular restore

            new_database_name (str) :   Name of the newly created database database
                    default: None   creates a database with original dbname+ <TIMESTAMP>

            destination_instance (str):  Destination server(instance) name.
                    default None .creates a database in the same instance

            expire_days (int) :    days for which the database will be available
                    default 1 day.

            snap (bool)     : create recovery point for the snap setup
                    dafault False

        returns:
             object (Job) : instance of the Job class for this restore job

             recovery point Id (int) : id to uniquely access the recovery point

            recovery_point_name (str) : name of the database created

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

    def table_level_restore(self,
                            src_db_name,
                            tables_to_restore,
                            destination_db_name,
                            rp_name,
                            include_child_tables,
                            include_parent_tables):
        """Starts a table level restore

        Args:

            src_db_name(str) : Name of the source database

            tables_to_restore(list) : List of tables to restore

            destination_db_name(str) : Destination database name

            rp_name(str) : Name of recovery point

            include_child_tables(bool) : Includes all child tables in restore.

            include_parent_tables(bool) : Includes all parent tables in restore.

        Returns:

            job : Instance of Job class for this restore job"""

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

    def _table_level_restore_request_json(self,
                                          src_db,
                                          tables_to_restore,
                                          destination_db,
                                          rp_name,
                                          include_child_tables,
                                          include_parent_tables):
        """Creates and returns a request json for table level restore

        Args:
            src_db(str) : Name of the source database

            tables_to_restore(list) : List of tables to restore

            destination_db(str) : Destination database name

            rp_name(str) : Name of the corresponding recovery point

            include_child_tables(bool) : Includes all child tables in restore.

            include_parent_tables(bool) : Includes all parent tables in restore.

        Returns:

            request_json(dict) : Request json for table level restore"""

        client_name = self._agent_object._client_object.client_name
        client_id = int(self._agent_object._client_object.client_id)
        instance_name = self.instance_name
        instance_id = int(self.instance_id)

        source_item = []
        for table in tables_to_restore:
            source_item.append('/' + table)

        request_json = {
            "taskInfo": {
                "associations": [
                    {
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
                    }
                ],
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

    def restore(
            self,
            content_to_restore,
            drop_connections_to_databse=False,
            overwrite=True,
            restore_path=None,
            to_time=None,
            sql_restore_type=SQLDefines.DATABASE_RESTORE,
            sql_recover_type=SQLDefines.STATE_RECOVER,
            undo_path=None,
            restricted_user=None,
            destination_instance=None
    ):
        """Restores the databases specified in the input paths list.

            Args:
                content_to_restore (list):  List of databases to restore.

                drop_connections_to_databse (bool):  Drop connections to database.  Defaults to False.

                overwrite (bool):  Unconditional overwrite files during restore.  Defaults to True.

                restore_path (str):  Existing path on disk to restore.  Defaults to None.

                to_time (str):  Restore to time.  Defaults to None.

                sql_recover_type (str):  Type of sql recovery state. (STATE_RECOVER, STATE_NORECOVER, STATE_STANDBY)
                Defaults to STATE_RECOVER.

                sql_restore_type (str):  Type of sql restore state.  (DATABASE_RESTORE, STEP_RESTORE, RECOVER_ONLY)
                Defaults to DATABASE_RESTORE.

                undo_path (str):  File path for undo path for sql standby restores.  Defaults to None.

                restricted_user (bool):  Restore database in restricted user mode.  Defaults to None.

                destination_instance (str):  Destination instance to restore too.  Defaults to None.

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if content_to_restore is not a list

                    if response is empty

                    if response is not success
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
            destination_instance=destination_instance
        )

        return self._process_restore_response(request_json)

    def restore_to_destination_server(
            self,
            content_to_restore,
            destination_server,
            drop_connections_to_databse=False,
            overwrite=True,
            restore_path=None):
        """Restores the databases specified in the input paths list.

            Args:
                content_to_restore (list):  List of databases to restore.

                destination_server (str):  Destination server(instance) name.

                drop_connections_to_databse (bool): Drop connections to database.  Defaults to False.

                overwrite (bool):  Unconditional overwrite files during restore.  Defaults to True.

                restore_path (str):  Existing path on disk to restore.  Default to None.

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if content_to_restore is not a list

                    if response is empty

                    if response is not success
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

    @property
    def mssql_instance_prop(self):
        """ getter for sql server instance properties """
        return self._mssql_instance_prop

    @mssql_instance_prop.setter
    def mssql_instance_prop(self, value):
        """Setter for SQL server instance properties

            Args:
                value (list)  --  list of the category and properties to update on the instance

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Instance API
        """
        category, prop = value

        self._set_instance_properties(category, prop)

    def vss_option(self, value):
        """Enables or disables VSS option on SQL instance

            Args:
                value (bool)  --  Boolean value whether to set VSS option on or off

        """

        request_json = {
            "useVss": value
        }

        self._set_instance_properties("_mssql_instance_prop", request_json)

    def vdi_timeout(self, value):
        """Sets the SQL VDI timeout value on SQL instance

            Args:
                value (int)  --  value of vdi timeout for sql vdi operations

        """

        request_json = {
            "vDITimeOut": value
        }

        self._set_instance_properties("_mssql_instance_prop", request_json)

    def impersonation(self, enable, username=None, password=None):
        """Sets impersonation on SQL instance with local system account or provided user account.

            Args:
                enable (bool)  --  boolean value whether to set impersonation

                username (str, optional)   --  user to set for impersonation.
                Defaults to local system account if enabled is True and username not provided.

                password (str, optional)   --  password of user account

        """

        if enable and username is None:
            impersonate_json = {
                "overrideHigherLevelSettings": {
                    "overrideGlobalAuthentication": enable,
                    "useLocalSystemAccount": True
                }
            }
        elif enable and username is not None:
            if password is not None:
                impersonate_json = {
                    "overrideHigherLevelSettings": {
                        "overrideGlobalAuthentication": enable,
                        "useLocalSystemAccount": False,
                        "userAccount": {
                            "userName": username,
                            "password": b64encode(password.encode()).decode()
                        }
                    }
                }
            else:
                raise SDKException(
                    'Instance',
                    '102',
                    'Please provide password to set impersonation for user [{0}]'.format(username)
                )
        else:
            impersonate_json = {
                "overrideHigherLevelSettings": {
                    "overrideGlobalAuthentication": enable,
                    "useLocalSystemAccount": False
                }
            }

        self._set_instance_properties("_mssql_instance_prop", impersonate_json)
