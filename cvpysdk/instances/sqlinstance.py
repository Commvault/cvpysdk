# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

    backup()                        --  runs full backup for all subclients associated
                                            with this instance

    browse()                        --  gets the content of the backup for this instance

    browse_in_time()                --  gets the content of the backup for this instance
                                            in the time range specified

    restore()                       --  runs the restore job for specified

    restore_to_destination_server() --  restores the database on destination server

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

    def _process_browse_request(self, browse_request):
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

    def browse(self):
        """Gets the list of the backed up databases for this instance.

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

        return self._process_browse_request(browse_request)

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
                "overrideHigherLevelSettings":{
                    "overrideGlobalAuthentication": enabled,
                    "useLocalSystemAccount": True
                }
            }
        elif enable and username is not None:
            if password is not None:
                impersonate_json = {
                    "overrideHigherLevelSettings":{
                        "overrideGlobalAuthentication": enabled,
                        "useLocalSystemAccount": False,
                        "userAccount":{
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
                "overrideHigherLevelSettings":{
                    "overrideGlobalAuthentication": enable,
                    "useLocalSystemAccount": False
                }
            }

        self._set_instance_properties("_mssql_instance_prop", impersonate_json)
