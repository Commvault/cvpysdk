# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a DB2 Instance.

DB2Instance is the only class defined in this file.

DB2Instance:    Derived class from Instance Base class, representing a
                           DB2 instance, and to perform operations on that instance

DB2Instance:

    _get_instance_properties()      --      Instance class method overwritten to add cloud apps
                                            instance properties as well

    version()                       --      getter method for db2 version

    home_directory()                --      Getter for db2 home directory

    user_account()                  --      Getter for db2 user account name

    data_backup_storage_policy()    --      Getter for sp name configured for data backup

    command_line_storage_policy()   --      Getter for cli backup sp name

    log_backup_storgae_policy()     --      Getter for log backup sp name

    _restore_entire_database()      --      Performs restore for entire database level

"""
from __future__ import unicode_literals
from ..instance import Instance
from ..exception import SDKException


class DB2Instance(Instance):

    @property
    def version(self):
        """Getter for db2 version

        Returns:
            db2 version value in string

        """
        return self._properties.get('version')

    @property
    def home_directory(self):
        """
        getter for db2 home

        Returns:
            string - string of db2_home

        """
        return self._properties.get('db2Instance',{}).get('homeDirectory')

    @property
    def user_account(self):
        """
                Getter for db2 user

                Returns:
                    string  - String containing db2 user
        """
        return self._properties.get('DB2Instance',{}).get('userAccount')

    @property
    def data_backup_storage_policy(self):
        """ Getter for data storagepolicy from instance level

            Returns:
                Storage policy name from db2 instance level

        """
        return self._properties['db2Instance']['db2StorageDevice'][
            'dataBackupStoragePolicy'].get('storagePolicyName')

    @property
    def command_line_storage_policy(self):
        """Getter for commandline sp defined at db2 instance level
            Returns:
                Command line sp name from db2 instance level
        """
        return self._properties['DB2Instance']['DB2StorageDevice'][
            'commandLineStoragePolicy'].get('storagePolicyName')

    @property
    def log_backup_storgae_policy(self):
        """
        Getter for log backup storage policy defined at instance level
            Returns:
                 Log backup SP name from instance level
        """
        return self._properties['DB2Instance']['DB2StorageDevice'][
            'logBackupStoragePolicy'].get('storagePolicyName')

    def _restore_destination_json(self, value):
        """setter for the Db2 Destination options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._destination_restore_json = {
            "destinationInstance": {
                "clientName": value.get("dest_client_name", ""),
                "instanceName": value.get("dest_instance_name", ""),
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
            raise SDKException('Subclient', '101')

        self.db2_options_restore_json = {
            "restoreType": value.get("restore_type", "ENTIREDB"),
            "redirect": value.get("redirect", False),
            "restoreArchiveLogs": value.get("restore_archive_logs", False),
            "rollForward": value.get("roll_forward", True),
            "restoreIncramental": value.get("restore_incremental", False),
            "rollForwardToEnd": value.get("roll_forward_to_end", "TO_END"),
            "restoreData": value.get("restore_data", True),
            "restoreOnline": value.get("restore_online", False),
            "targetDb": value.get("target_db", " "),
            "targetPath": value.get("target_path", " "),
            "reportFile": value.get("report_file", " "),
            "buffers": value.get("buffers", 2),
            "bufferSize": value.get("buffer_size", 1024),
            "rollForwardDir": value.get("roll_forward_dir", " "),
            "historyFilePath": value.get("history_file_path", " "),
            "recoverDb": value.get("recover_db", True),
            "dbHistoryFilepath": value.get("db_history_filepath", False),
            "storagePath": value.get("storage_path", False),
            "parallelism": value.get("parallelism", 0),
            "useSnapRestore": value.get("use_snap_restore", False),
            "useLatestImage": value.get("use_latest_image", True),
            "tableViewRestore": value.get("table_view_restore", False),
            "cloneRecovery": value.get("clone_recovery", False),
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

        self._db2_restore_options_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["db2Option"] = self._db2_restore_options_json(restore_option)
        return rest_json

    def restore_entire_database(
            self,
            dest_client_name=None,
            dest_instance_name=None,
            dest_database_name=None,
            db2_options=None

    ):
        """Restores the db2 database specified in the input paths list.

            Args:

                dest_client_name        (str)   --  destination client name

                dest_instance_name      (str)   --  destination db2 instance name of destination on destination client

                dest_database_name      (str)    -- destination database name

                db2_options             (dict)    -- db2 restore options like rollforward to end of logs

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        restore_option = {}

        if db2_options is None:
            db2_options = {}

        if dest_client_name is None:
            dest_client_name = self._agent_object._client_object.client_name
        if dest_instance_name is None:
            dest_instance_name = self.instance_name.upper()


        restore_option["dest_client_name"] = dest_client_name
        restore_option["dest_instance_name"] = dest_instance_name
        restore_option["dest_backupset_name"] = dest_database_name
        restore_option["target_db"] = dest_database_name
        restore_option["client_name"] = self._agent_object._client_object.client_name
        restore_option["copy_precedence_applicable"] = True
        restore_option["copy_precedence"] = db2_options.get("copy_precedence", 0)
        restore_option["from_time"] = db2_options.get("from_time", 0)
        restore_option["to_time"] = db2_options.get("to_time", 0)

        request_json = self._restore_json(**restore_option)

        return self._process_restore_response(request_json)
