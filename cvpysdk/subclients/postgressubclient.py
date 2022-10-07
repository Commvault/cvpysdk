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

"""File for operating on a Postgres Server Subclient

PostgresSubclient is the only class defined in this file.

PostgresSubclient: Derived class from Subclient Base class, representing a HANA server subclient,
                        and to perform operations on that subclient

PostgresSubclient:
==================

    set_content()                        --  Adds/Updates/Deletes the postgresql subclient contents

    collect_object_list()                --  Sets the collect object list flag for the subclient
    as the value provided as input

    _backup_request_json()               --  prepares the json for the backup request

    _get_subclient_properties()          --  gets the subclient related properties of
    PostgreSQL subclient

    _get_subclient_properties_json()     --  gets all the subclient related properties of
    PostgreSQL subclient

    backup()                             --  Runs a backup job for the subclient of the
    level specified

    restore_postgres_server()            --  Method to restore the Postgres server


PostgresSubclient instance Attributes
=====================================

    **content**                          --  returns list of databases which are part
    of subclient content

    **collect_object_list**              --  Returns the collect object list flag of the subclient

"""
from __future__ import unicode_literals
from .dbsubclient import DatabaseSubclient
from ..exception import SDKException

class PostgresSubclient(DatabaseSubclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Constructor for the class

        Args:
            backupset_object  (object)  -- instance of the Backupset class

            subclient_name    (str)     -- name of the subclient

            subclient_id      (str)     -- id of the subclient

        """
        self._postgres_properties = {}
        self._postgres_browse_options = None
        self._postgres_destination = None
        self._postgres_file_options = None
        self._postgres_restore_options = None
        super(PostgresSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    @property
    def content(self):
        """returns list of databases which are part of subclient content"""
        self._content = None
        if not self.is_default_subclient:
            if 'content' in self._subclient_properties:
                self._content = self._subclient_properties['content']
        if not self._content is None:
            database_list = list()
            for database in self._content:
                if database.get('postgreSQLContent'):
                    if database['postgreSQLContent'].get('databaseName'):
                        database_list.append(database[
                            'postgreSQLContent']['databaseName'].lstrip("/"))
            return database_list

    def set_content(self, database_list, operation_type="OVERWRITE"):
        """ Adds/Updates/Deletes the postgresql subclient contents

            Args:

                database_list (list)  -- list of databases to be added to the subclient content

                operation_type (str)  -- Content operation to be performed

                    Accepted Values:

                        ADD         -- Adds the database list to existing content

                        OVERWRITE   -- Replaces the content with given databases

                        DELETE      -- Deletes the database from the content

            Raises:
                SDKException:
                    if database list is not a list

                    if operation type is not accepted value

                    if the database list is empty

                    if the operation is performed on default subclient

        """
        if not isinstance(database_list, list):
            raise SDKException('Subclient', '101')
        if operation_type.lower() not in ['add', 'overwrite', 'delete']:
            raise SDKException('Subclient', '102', 'Operation type not supported')
        if not database_list:
            raise SDKException('Subclient', '102', 'Cannot set empty content to a subclient')
        if self.is_default_subclient:
            raise SDKException('Subclient', '102', 'Cannot set content to the default subclient')
        operation_map = {
            'add'   :   2,
            'overwrite': 1,
            'delete':   3
            }
        properties = self._subclient_properties
        content_list = []
        for database in database_list:
            content_dict = {
                'postgreSQLContent':
                    {
                        'databaseName': f'{database}'
                    }
                }
            content_list.append(content_dict)
        properties['contentOperationType'] = operation_map[operation_type.lower()]
        properties['content'] = content_list
        self.update_properties(properties)

    @property
    def collect_object_list(self):
        """Returns the collect object list flag of the subclient.

        Returns:

            (bool)  --  True if flag is set
                        False if the flag is not set

        """
        return self._subclient_properties.get(
            'postgreSQLSubclientProp', {}).get(
                'collectObjectListDuringBackup', False)

    @collect_object_list.setter
    def collect_object_list(self, value):
        """Sets the collect object list flag for the subclient as the value provided as input.

        Args:

            value   (bool)  --  Boolean value to set as flag

            Raises:
                SDKException:
                    if failed to set collect object list flag

                    if the type of value input is not bool
        """
        if isinstance(value, bool):
            self._set_subclient_properties(
                "_subclient_properties['postgreSQLSubclientProp']['collectObjectListDuringBackup']",
                value)
        else:
            raise SDKException(
                'Subclient', '102', 'Expecting a boolean value here'
            )

    def _backup_request_json(
            self,
            backup_level,
            inc_with_data=False):
        """
        prepares the json for the backup request

            Args:
                backup_level        (list)  --  level of backup the user wish to run
                        Full / Incremental / Differential

                inc_with_data       (bool)  --  flag to determine if the incremental backup
                includes data or not

            Returns:
                dict - JSON request to pass to the API

        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")

        if "incremental" in backup_level.lower() and inc_with_data:
            request_json["taskInfo"]["subTasks"][0]["options"][
                "backupOpts"]['incrementalDataWithLogs'] = True

        return request_json

    def _get_subclient_properties(self):
        """gets the subclient related properties of PostgreSQL subclient.

        """
        super(PostgresSubclient, self)._get_subclient_properties()
        if 'postgreSQLSubclientProp' not in self._subclient_properties:
            self._subclient_properties['postgreSQLSubclientProp'] = {}
        self._postgres_properties = self._subclient_properties['postgreSQLSubclientProp']

    def _get_subclient_properties_json(self):
        """gets all the subclient related properties of PostgreSQL subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "postgreSQLSubclientProp": self._postgres_properties,
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    def backup(
            self,
            backup_level="Differential",
            inc_with_data=False):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential / Synthetic_full

                    default: Differential

                inc_with_data       (bool)  --  flag to determine if the incremental backup
                includes data or not

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success

        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'incremental', 'differential', 'synthetic_full']:
            raise SDKException('Subclient', '103')

        if not inc_with_data:
            return super(PostgresSubclient, self).backup(backup_level)
        request_json = self._backup_request_json(
            backup_level, inc_with_data)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CREATE_TASK'], request_json
        )
        return self._process_backup_response(flag, response)

    def restore_postgres_server(
            self,
            database_list=None,
            dest_client_name=None,
            dest_instance_name=None,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            clone_env=False,
            clone_options=None,
            media_agent=None,
            table_level_restore=False,
            staging_path=None,
            no_of_streams=None,
            volume_level_restore=False,
            redirect_enabled=False,
            redirect_path=None,
            **kwargs):
        """
        Method to restore the Postgres server

            Args:

                database_list               (List) -- List of databases

                dest_client_name            (str)  -- Destination Client name

                dest_instance_name          (str)  -- Destination Instance name

                copy_precedence             (int)  -- Copy precedence associted with storage

                from_time               (str)   --  time to retore the contents after
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time                 (str)   --  time to retore the contents before
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                clone_env                   (bool)  --  boolean to specify whether the database
                should be cloned or not

                    default: False

                clone_options               (dict)  --  clone restore options passed in a dict

                    default: None

                    Accepted format: {
                                        "stagingLocaion": "/gk_snap",
                                        "forceCleanup": True,
                                        "port": "5595",
                                        "libDirectory": "/opt/PostgreSQL/9.6/lib",
                                        "isInstanceSelected": True,
                                        "reservationPeriodS": 3600,
                                        "user": "postgres",
                                        "binaryDirectory": "/opt/PostgreSQL/9.6/bin"
                                     }

                media_agent             (str)   --  media agent name

                    default: None

                table_level_restore     (bool)  --  boolean to specify if the restore operation
                is table level

                    default: False

                staging_path            (str)   --  staging path location for table level restore

                    default: None

                no_of_streams           (int)   --  number of streams to be used by
                volume level restore

                    default: None

                volume_level_restore    (bool)  --  volume level restore flag

                    default: False

                redirect_enabled         (bool)  --  boolean to specify if redirect restore is
                enabled

                    default: False

                redirect_path           (str)   --  Path specified in advanced restore options
                in order to perform redirect restore

                    default: None

                revert                 (bool)  --  boolean to specify whether to do a
                                                   hardware revert in restore
                    default: False

            Returns:
                object -- Job containing restore details

        """
        backup_set_object = self._backupset_object
        instance_object = backup_set_object._instance_object
        if dest_client_name is None:
            dest_client_name = instance_object._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = instance_object.instance_name

        backupset_name = backup_set_object.backupset_name

        if backupset_name.lower() == "fsbasedbackupset":
            backupset_flag = True
            if database_list is None:
                database_list = ["/data"]
        else:
            backupset_flag = False

        instance_object._restore_association = self._subClientEntity
        return instance_object.restore_in_place(
            database_list,
            dest_client_name,
            dest_instance_name,
            backupset_name,
            backupset_flag,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            clone_env=clone_env,
            clone_options=clone_options,
            media_agent=media_agent,
            table_level_restore=table_level_restore,
            staging_path=staging_path,
            no_of_streams=no_of_streams,
            volume_level_restore=volume_level_restore,
            redirect_enabled=redirect_enabled,
            redirect_path=redirect_path,
            revert=kwargs.get("revert", False))
