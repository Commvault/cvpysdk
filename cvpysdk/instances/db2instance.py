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

"""File for operating on a DB2 Instance.

DB2Instance is the only class defined in this file.

DB2Instance:    Derived class from Instance Base class, representing a
DB2 instance, and to perform operations on that instance

DB2Instance:
============

    _restore_destination_json()     --      setter for the Db2 Destination options in restore JSON

    _db2_restore_options_json()     --      setter for  the db2 options of in restore JSON

    _restore_json()                 --      returns the JSON request to pass to the API as per
    the options selected by the user

    restore_entire_database()       --      Restores the db2 database

    restore_out_of_place()          --      runs the out of place restore for given backupset


DB2Instance instance Attributes:
================================
    **version**                         -- returns db2 version

    **home_directory**                  -- returns db2 home directory

    **user_name**                       -- returns db2 user name

    **data_backup_storage_policy**      -- returns data backup storage policy

    **command_line_storage_policy**     -- returns commandline storage policy

    **log_backup_storage_policy**       -- returns log backup storage policy

"""
from __future__ import unicode_literals
from ..instance import Instance
from ..exception import SDKException


class DB2Instance(Instance):
    """ Derived class from Instance Base class, representing a DB2 instance,
        and to perform operations on that Instance."""

    @property
    def version(self):
        """returns db2 version

        Returns:
            (str) -- db2 version value in string

        """
        return self._properties.get('version', "")

    @property
    def home_directory(self):
        """
        returns db2 home directory

        Returns:
            (str) - string of db2_home

        """
        return self._properties.get('db2Instance', {}).get('homeDirectory', "")

    @property
    def user_name(self):
        """
                returns db2 user name

                Returns:
                    (str)  - String containing db2 user

        """
        return self._properties.get(
            'db2Instance', {}).get('userAccount', {}).get('userName', "")

    @property
    def data_backup_storage_policy(self):
        """ returns data backup storage policy

            Returns:
                (str) -- Storage policy name from db2 instance level

        """
        return self._properties.get('db2Instance', {}).get(
            'DB2StorageDevice', {}).get('dataBackupStoragePolicy', {}).get('storagePolicyName', "")

    @property
    def command_line_storage_policy(self):
        """returns commandline storage policy

            Returns:
                (str)  --  Command line sp name from db2 instance level

        """
        return self._properties.get('db2Instance', {}).get(
            'DB2StorageDevice', {}).get('commandLineStoragePolicy', {}).get('storagePolicyName', "")

    @property
    def log_backup_storage_policy(self):
        """
        returns log backup storage policy

            Returns:
                (str)  -- Log backup SP name from instance level

        """
        return self._properties.get('db2Instance', {}).get(
            'DB2StorageDevice', {}).get('logBackupStoragePolicy', {}).get('storagePolicyName', "")

    def _restore_destination_json(self, value):
        """setter for the Db2 Destination options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = {
            "destinationInstance": {
                "clientName": value.get("dest_client_name", ""),
                "instanceName": value.get("dest_instance_name", ""),
                "backupsetName": value.get("dest_backupset_name", ""),
                "appName": "DB2"
            },
            "destClient": {
                "clientName": value.get("dest_client_name", "")
            }
        }

    def _db2_restore_options_json(self, value):
        """setter for  the db2 options of in restore JSON
            Args:
                value (dict) -- Dictionary of options need to be set for restore

        """
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.db2_options_restore_json = {
            "restoreType": value.get("restore_type", 0),
            "restoreLevel": value.get("restore_level", 0),
            "redirect": value.get("redirect", False),
            "rollForwardPending": value.get("rollforward_pending", False),
            "restoreArchiveLogs": value.get("restore_archive_logs", True),
            "rollForward": value.get("roll_forward", True),
            "restoreIncremental": value.get("restore_incremental", False),
            "archiveLogLSN": value.get("archivelog_lsn", False),
            "archiveLogTime": value.get("archive_log_time", False),
            "startLSN": value.get("start_lsn", False),
            "endLSN": value.get("end_lsn", False),
            "logTimeStart": value.get("logtime_start", False),
            "logTimeEnd": value.get("logtime_end", False),
            "rollForwardToEnd": value.get("roll_forward_to_end", 1),
            "useAlternateLogFile": value.get("use_alternate_logfile", False),
            "restoreData": value.get("restore_data", True),
            "restoreOnline": value.get("restore_online", False),
            "targetDb": value.get("target_db", " "),
            "targetPath": value.get("target_path", " "),
            "reportFile": value.get("report_file", " "),
            "buffers": value.get("buffers", 2),
            "bufferSize": value.get("buffer_size", 1024),
            "rollForwardDir": value.get("roll_forward_dir", " "),
            "recoverDb": value.get("recover_db", False),
            "dbHistoryFilepath": value.get("db_history_filepath", False),
            "storagePath": value.get("storage_path", False),
            "parallelism": value.get("parallelism", 0),
            "useSnapRestore": value.get("use_snap_restore", False),
            "useLatestImage": value.get("use_latest_image", True),
            "tableViewRestore": value.get("table_view_restore", False),
            "useLogTarget": value.get("use_log_target", False),
            "cloneRecovery": value.get("clone_recovery", False)
        }

        return self.db2_options_restore_json

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (dict)  --  list of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API

        """
        rest_json = super(DB2Instance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option = kwargs

        json = self._db2_restore_options_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"] = json
        return rest_json

    def restore_entire_database(
            self,
            dest_client_name,
            dest_instance_name,
            dest_backupset_name,
            restore_type='ENTIREDB',
            recover_db=True,
            restore_incremental=True,

    ):
        """Restores the db2 database

            Args:

                dest_client_name        (str)   --  destination client name

                dest_instance_name      (str)   --  destination db2 instance name of
                destination on destination client

                dest_database_name      (str)   -- destination database name

                restore_type            (str)   -- db2 restore type

                    default: "ENTIREDB"

                recover_db              (bool)  -- recover database flag

                    default: True

                restore_incremental     (bool)  -- Restore incremental flag

                    default: True

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        if "entiredb" in restore_type.lower():
            restore_type = 0

        request_json = self._restore_json(
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            dest_backupset_name=dest_backupset_name,
            target_db=dest_backupset_name,
            restore_type=restore_type,
            recover_db=recover_db,
            restore_incremental=restore_incremental,
        )
        request_json['taskInfo']["subTasks"][0]["options"]["restoreOptions"][
            "browseOption"]["backupset"]["backupsetName"] = dest_backupset_name

        return self._process_restore_response(request_json)

    def restore_out_of_place(
            self,
            dest_client_name,
            dest_instance_name,
            dest_backupset_name,
            target_path,
            **kwargs):
        """Restores the DB2 data/log files specified in the input paths
        list to the same location.

            Args:
                dest_client_name        (str)   --  destination client name where files are to be
                restored

                dest_instance_name      (str)   --  destination db2 instance name of
                destination client

                dest_backupset_name     (str)   --  destination db2 backupset name of
                destination client

                target_path             (str)   --  Destination DB restore path

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time               (str)   --  time to retore the contents after
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time                 (str)   --  time to retore the contents before
                    format: YYYY-MM-DD HH:MM:SS

                    default: None

                redirect_enabled         (bool)  --  boolean to specify if redirect restore is
                enabled

                    default: False

                redirect_storage_group_path           (dict)   --  Path specified for each storage group
                in advanced restore options in order to perform redirect restore
                    format: {'Storage Group Name': 'Redirect Path'}

                    default: None

                 redirect_tablespace_path           (dict)   --  Path specified for each tablespace in advanced
                 restore options in order to perform redirect restore
                    format: {'Tablespace name': 'Redirect Path'}

                    default: None

                destination_path        (str)   --  destinath path for restore
                    default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        copy_precedence = kwargs.get('copy_precedence', None)
        from_time = kwargs.get('from_time', None)
        to_time = kwargs.get('to_time', None)
        redirect_enabled = kwargs.get('redirect_enabled', False)
        redirect_tablespace_path = kwargs.get('redirect_tablespace_path', None)
        redirect_storage_group_path = kwargs.get('redirect_storage_group_path', None)
        rollforward = kwargs.get('rollforward', True)
        restoreArchiveLogs = kwargs.get('restoreArchiveLogs', False)
        restore_incremental = kwargs.get('restore_incremental', True)

        if redirect_enabled:
            if not isinstance(redirect_tablespace_path, dict) and \
                    not isinstance(redirect_storage_group_path, dict):
                raise SDKException('Instance', '101')

        request_json = self._restore_json(
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            dest_backupset_name=dest_backupset_name,
            target_db=dest_backupset_name,
            target_path=target_path,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            redirect=redirect_enabled,
            redirect_storage_group_path=redirect_storage_group_path,
            redirect_tablespace_path=redirect_tablespace_path,
            rollforward_pending=rollforward,
            restoreArchiveLogs=restoreArchiveLogs,
            roll_forward=rollforward,
            restore_incremental=restore_incremental,
            storage_path=True)

        if redirect_storage_group_path:
            storagePaths = []
            storageGroup = {"storageGroup": []}

            for name, path in redirect_storage_group_path.items():
                storagePaths.append(path)
                if isinstance(path, str):
                    storageGroup["storageGroup"].append({"groupName": name, "stoPaths": [path]})
                else:
                    storageGroup["storageGroup"].append({"groupName": name, "stoPaths": path})

            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                "storagePaths"] = storagePaths
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                "storageGroupInfo"] = storageGroup

        if redirect_tablespace_path:
            redirect_info = []
            for tablespace, path in redirect_tablespace_path.items():
                table_string = "%s\t1\t%s\t6\t25600\t1\t1" % (tablespace, path)
                redirect_info.append(table_string)
            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"][
                "redirectInfo"] = redirect_info

        request_json['taskInfo']["subTasks"][0]["options"]["restoreOptions"][
            "browseOption"]["backupset"]["backupsetName"] = dest_backupset_name

        return self._process_restore_response(request_json)

