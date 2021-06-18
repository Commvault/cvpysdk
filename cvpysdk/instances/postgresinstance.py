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

"""File for operating on a POSTGRESQL Instance.

PostgreSQLInstance is the only class defined in this file.

PostgreSQLInstance: Derived class from Instance Base class, representing a postgres server instance,
                       and to perform operations on that instance

PostgreSQLInstance:
===================

    _get_instance_properties()           --     Gets the properties of this instance

    _get_instance_properties_json()      --     Gets all the instance related properties of
    PostgreSQL instance.

    _restore_json()                      --     returns the JSON request to pass to the API as per
    the options selected by the user

    _restore_common_options_json()       --     setter for the common options in restore JSON

    _restore_destination_json()          --     setter for the Destination options in restore JSON

    _restore_postgres_option_json()      --     setter for the postgres restore option
    in restore JSONRe

    restore_in_place()                   --     Restores the postgres data/log files
    specified in the input paths list to the same location

PostgreSQLInstance instance Attributes
======================================

    **postgres_bin_directory**           --  returns the postgres bin directory of postgres server

    **postgres_lib_directory**           --  returns the lib directory of postgres server

    **postgres_archive_log_directory**   --  returns the postgres archive log directory
    of postgres server

    **postgres_server_user_name**        --  returns the postgres server user name
    of postgres server

    **postgres_server_port_number**      --  returns the postgres server port number
    of postgres server

    **maintenance_database**             --  returns the maintenance database associated
    with postgres server

    **postgres_version**                 --  returns the postgres server version

    **standby_instance_name**            --  Returns the standby instance name

    **standby_instance_id**              --  Returns the standby instance id

    **use_master_for_log_backup**        --  Returns True if master is used for log backup

    **use_master_for_data_backup**       --  Returns True if master is used for data backup

    **archive_delete**                   --  Returns True if archive delete is enabled for instance

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ..instance import Instance
from ..exception import SDKException


class PostgreSQLInstance(Instance):
    """Derived class from Instance Base class, representing a POSTGRESQL instance,
        and to perform operations on that Instance."""

    def __init__(self, agent_object, instance_name, instance_id):
        """Initialize object of the Instances class.

            Args:
                agent_object (object)  --  instance of the Agent class

            Returns:
                object - instance of the Instances class

        """
        super(
            PostgreSQLInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)
        self.backup_object = None
        self.backupset_object = None
        self.sub_client_object = None
        self.postgres_restore_json = None
        self._postgres_restore_options = None
        self._destination_restore_json = None


    @property
    def postgres_bin_directory(self):
        """Returns the bin directory of postgres server

            Return Type: str

        """
        if self._properties['postGreSQLInstance']['BinaryDirectory']:
            return self._properties['postGreSQLInstance']['BinaryDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Binary directory.")

    @property
    def postgres_lib_directory(self):
        """Returns the lib directory of postgres server

            Return Type: str

        """
        if self._properties['postGreSQLInstance']['LibDirectory']:
            return self._properties['postGreSQLInstance']['LibDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Lib directory.")

    @property
    def postgres_archive_log_directory(self):
        """Returns the archive log directory of postgres server

            Return Type: str

        """
        if self._properties['postGreSQLInstance']['ArchiveLogDirectory']:
            return self._properties['postGreSQLInstance']['ArchiveLogDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Archive log directory.")

    @property
    def postgres_server_user_name(self):
        """Returns the username of postgres server

            Return Type: str

        """
        if self._properties['postGreSQLInstance']['SAUser']['userName']:
            return self._properties['postGreSQLInstance']['SAUser']['userName']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Server name.")

    @property
    def postgres_server_port_number(self):
        """Returns the port number associated with postgres server

            Return Type: str

        """
        if self._properties['postGreSQLInstance']['port']:
            return self._properties['postGreSQLInstance']['port']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the port Number.")

    @property
    def maintenance_database(self):
        """Returns the maintenance database associated with postgres server

            Return Type: str

        """
        if self._properties['postGreSQLInstance'].get('MaintainenceDB'):
            return self._properties['postGreSQLInstance']['MaintainenceDB']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch maintenance database.")

    @property
    def postgres_version(self):
        """Returns the postgres server version

            Return Type: str

        """
        if self._properties.get('version'):
            return self._properties['version']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch postgres version.")

    @property
    def archive_delete(self):
        """Returns True if archive delete enabled. False if not

            Return Type: bool

        """
        return self._properties.get('postGreSQLInstance', {}).get('ArchiveDelete', False)

    @archive_delete.setter
    def archive_delete(self, value):
        """ Setter for archive delete instance property

            Args:

                value (bool)  -- True to enable archive delete

        """
        if not isinstance(value, bool):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['ArchiveDelete'] = value
        self.update_properties(properties)

    @property
    def standby_instance_name(self):
        """Returns the standby instance name

            Return Type: str

        """
        if self.is_standby_enabled:
            return self._properties.get('postGreSQLInstance', {}).get('standbyOptions', {}).get('standbyInstance', {}).get('instanceName', {})
        return None

    @property
    def standby_instance_id(self):
        """Returns the standby instance id

            Return Type: str

        """
        if self.is_standby_enabled:
            return self._properties.get('postGreSQLInstance', {}).get('standbyOptions', {}).get('standbyInstance', {}).get('instanceId', {})
        return None

    @property
    def is_standby_enabled(self):
        """Returns True if standby enabled. False if not

            Return Type: bool

        """
        return self._properties.get('postGreSQLInstance', {}).get('standbyOptions', {}).get('isStandbyEnabled', False)

    @property
    def use_master_for_log_backup(self):
        """ Returns True if master is used for log backup

            Return Type: bool

        """
        return self._properties.get('postGreSQLInstance', {}).get('standbyOptions', {}).get('useMasterForLogBkp', False)

    @use_master_for_log_backup.setter
    def use_master_for_log_backup(self, value):
        """ Setter for user master for log backup standby property

            Args:

                value (bool)  -- True to use master for log backup

        """
        if not isinstance(value, bool):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['standbyOptions']['useMasterForLogBkp'] = value
        self.update_properties(properties)

    @property
    def use_master_for_data_backup(self):
        """ Returns True if master is used for data backup

            Return Type: bool

        """
        return self._properties.get('postGreSQLInstance', {}).get('standbyOptions', {}).get('useMasterForDataBkp', False)

    @use_master_for_data_backup.setter
    def use_master_for_data_backup(self, value):
        """ Setter for user master for data backup standby property

            Args:

                value (bool)  -- True to use master for data backup

        """
        if not isinstance(value, bool):
            raise SDKException('Instance', '101')
        properties = self._properties
        properties['postGreSQLInstance']['standbyOptions']['useMasterForDataBkp'] = value
        self.update_properties(properties)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(PostgreSQLInstance, self)._get_instance_properties()
        self._postgresql_instance = self._properties['postGreSQLInstance']

    def _get_instance_properties_json(self):
        """ Gets all the instance related properties of PostgreSQL instance.

           Returns:
                dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties":
                {
                    "instance": self._instance,
                    "postGreSQLInstance": self._postgresql_instance
                }
        }
        return instance_json

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (dict)  --  Dictionary of options need to be set for restore

            Returns:
                dict             -- JSON request to pass to the API

        """
        rest_json = super(PostgreSQLInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        self._restore_postgres_option_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["postgresRstOption"] = self.postgres_restore_json
        return rest_json

    def _restore_common_options_json(self, value):
        """setter for  the Common options of in restore JSON"""
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')
        super(PostgreSQLInstance, self)._restore_common_options_json(value)
        if value.get("baseline_jobid"):
            self._commonoption_restore_json = {
                "clusterDBBackedup":False,
                "restoreToDisk":False,
                "baselineBackup":1,
                "baselineRefTime": value.get("baseline_ref_time", ""),
                "baselineJobId":value.get("baseline_jobid", ""),
                "copyToObjectStore":False,
                "onePassRestore":False,
                "syncRestore":value.get("sync_restore", True)
            }

    def _restore_destination_json(self, value):
        """setter for the Destination options in restore JSON

            Args:
                value   (dict)  --  Dictionary of options need to be set for restore

        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        if value.get("restore_to_disk"):
            return super(PostgreSQLInstance, self)._restore_destination_json(value)

        else:
            self._destination_restore_json = {
                "destinationInstance": {
                    "clientName": value.get("dest_client_name", ""),
                    "instanceName": value.get("dest_instance_name", ""),
                    "appName": self._agent_object.agent_name
                },
                "destClient": {
                    "clientName": value.get("dest_client_name", "")
                }
            }

    def _restore_postgres_option_json(self, value):
        """setter for the restore option in restore JSON

            Args:
                value   (dict)  --  Dictionary of options need to be set for restore

        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.postgres_restore_json = self._postgres_restore_options = {
            "restoreToSameServer": False,
            "tableLevelRestore": value.get("table_level_restore", False),
            "instanceRestore": False,
            "fsBackupSetRestore": value.get("backupset_flag", ""),
            "isCloneRestore": value.get("clone_env", False),
            "refTime": {}
        }

        if value.get("clone_env", False):
            self.postgres_restore_json["cloneOptions"] = value.get("clone_options", "")

        if value.get("to_time"):
            time_value = {"timevalue": value.get("to_time", "")}
            self.postgres_restore_json["refTime"] = time_value
            self.postgres_restore_json["fromTime"] = time_value
            self.postgres_restore_json["pointOfTime"] = time_value

        if value.get("table_level_restore"):
            self.postgres_restore_json["stagingPath"] = value.get("staging_path", "")
            self.postgres_restore_json["auxilaryMap"] = []
            database_list = []
            for table_path in value.get("paths"):
                database_list.append(table_path.split('/')[1])
            database_list = set(database_list)
            for database_name in database_list:
                self.postgres_restore_json["auxilaryMap"].append({"sourceDB": database_name})

        if value.get("redirect_path"):
            self.postgres_restore_json["redirectEnabled"] = True
            self.postgres_restore_json["redirectItems"] = [value.get("redirect_path")]

        if value.get("restore_to_disk"):
            self.postgres_restore_json["fsBackupSetRestore"] = False

    def restore_in_place(
            self,
            path,
            dest_client_name,
            dest_instance_name,
            backupset_name,
            backupset_flag,
            overwrite=True,
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
            restore_to_disk=False,
            restore_to_disk_job=None,
            destination_path=None):
        """Restores the postgres data/log files specified in the input paths
        list to the same location.

            Args:
                path                    (list)  --  list of database/databases to be restored

                dest_client_name        (str)   --  destination client name where files are to be
                restored

                dest_instance_name      (str)   --  destination postgres instance name of
                destination client

                backupset_name          (str)   --  destination postgres backupset name of
                destination client

                backupset_flag          (bool)  --  flag to indicate fsbased backup

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time               (str)   --  time to retore the contents after
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time                 (str)   --  time to retore the contents before
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                clone_env               (bool)  --  boolean to specify whether the database
                should be cloned or not

                    default: False

                clone_options           (dict)  --  clone restore options passed in a dict

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

                restore_to_disk         (bool)  --  restore to disk flag

                    default: False

                restore_to_disk_job     (int)   --  backup job id to restore to disk

                    default: None

                destination_path        (str)   --  destinath path for restore

                    default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        if not (isinstance(path, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        if not path:
            raise SDKException('Instance', '104')

        if not no_of_streams:
            no_of_streams = 1

        index_free_restore = False
        if restore_to_disk:
            index_free_restore = True

        request_json = self._restore_json(
            paths=path,
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            backupset_name=backupset_name,
            backupset_flag=backupset_flag,
            copy_precedence=copy_precedence,
            overwrite=overwrite,
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
            restore_to_disk=restore_to_disk,
            index_free_restore=index_free_restore,
            destination_path=destination_path,
            restore_jobs=restore_to_disk_job)

        if volume_level_restore:
            request_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['destination']["noOfStreams"] = no_of_streams

        if restore_to_disk:
            request_json['taskInfo']['subTasks'][0]['options'][
                'restoreOptions']['destination']["destPath"] = [destination_path]

        return self._process_restore_response(request_json)
