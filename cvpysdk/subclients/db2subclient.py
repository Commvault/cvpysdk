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
File for operating on a Db2 Subclient

DB2Subclient is the only class defined in this file.

DB2Subclient: Derived class from Subclient Base class, representing an db2 subclient,
                        and to perform operations on that subclient

Db2Subclient:
    __init__()                          --  constructor for the class

    _get_subclient_properties()         --  gets the subclient related properties of
                                            db2 subclient

    _get_subclient_properties_json()    -- gets subclient property json for db2

    db2_use_dedupe_device()             -- getter and setter for enabling dedupe device option for db2

    db2_delete_log_files_after()        -- getter and setter for enabling delete log files after option in db2

    db2_backup_log_files()              -- getter and setter for enabling backup log files option for db2

    db2_delete_log_files_after()        -- getter and setter for enabling delete log file after option for db2

    is_backup_data_enabled()            -- getter and setter for enabling backup data option

    enable_backupdata()                 -- Method to enable backup data option at subclient level

    disable_backupdata()                -- Method to disable backup data option at subclient level

    enable_table_level()                -- Enable Table Level Browse

    enable_acs_backup()                 -- Enable DB2 ACS snap backup

"""
from __future__ import unicode_literals
from ..subclient import Subclient
from ..exception import SDKException


class DB2Subclient(Subclient):
    """
        DB2Subclient is a class to work on DB2 subclients

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Constructor for the class

        Args:
            backupset_object  (object)  -- instance of the Backupset class

            subclient_name    (str)     -- name of the subclient

            subclient_id      (str)     -- id of the subclient

        """
        super(DB2Subclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self._db2_subclient_properties = {}
        self._db2_backup_logfiles = {}
        self._db2_delete_logfiles_after = {}

    @property
    def db2_use_dedupe_device(self):
        """
            Getter to fetch dedupe device option
            Returns:
             Bool - True if dedupe_device is enabled on the subclient. Else False

        """
        return self._properties.get('db2SubclientProp', {}).get('db2UseDedupeDevice')

    @property
    def db2_delete_log_files_after(self):
        """
        Getter to fetch status of delete log files option
        Returns:
        Bool - True if delete log files option is enabled on the subclient. Else False

        """
        return self._subclient_properties.get('db2SubclientProp', {}).get('db2DeleteLogFilesAfter')

    @property
    def db2_backup_log_files(self):
        """
        Getter to fetch backup logfiles option is enabled or not
        Returns:
        Bool - True if delete log files option is enabled on the subclient. Else False

        """
        return self._subclient_properties.get('db2SubclientProp', {}).get('db2BackupLogFiles')

    @db2_backup_log_files.setter
    def db2_backup_log_files(self, value):
        """
        To enable or disable log backup option
        Args:

            value   (bool)      --  to enable or disable log backup option for db2 subclient
        """

        self._set_subclient_properties(
            "_db2_subclient_properties['db2BackupLogFiles']", value)


    @db2_delete_log_files_after.setter
    def db2_delete_log_files_after(self, value):
        """
        To enable or disable log backup option
        Args:

            value   (bool)      --  to enable or disable log backup option for db2 subclient
        """

        self._set_subclient_properties(
            "_db2_subclient_properties['db2DeleteLogFilesAfter']", value)

    @property
    def is_backup_data_enabled(self):
        """
        Getter to fetch data backup status is enabled or disabled

        Returns:

            (bool)      -   boolean value is returned based on the status of data backup option

        """

        return self._subclient_properties.get("db2SubclientProp", {}).get('db2BackupData', True)

    def enable_backupdata(self):
        """
        To enable data backup

        """

        self._set_subclient_properties("_db2_subclient_properties['db2BackupData']", True)

    def disable_backupdata(self):
        """
        To disable data backup

        """
        properties = self.properties
        properties['db2SubclientProp']["db2BackupData"] = False
        properties['db2SubclientProp']["skipLogsInBackupImage"] = 0
        properties['db2SubclientProp']["db2BackupMode"] = 0
        properties['db2SubclientProp']["db2UseDedupeDevice"] = True
        properties['db2SubclientProp']["db2DeleteLogFilesAfter"] = False
        properties['db2SubclientProp']["db2BackupLogFiles"] = True
        del properties["db2SubclientProp"]["db2BackupType"]
        self.update_properties(properties_dict=properties)

    def enable_table_level(self):
        """
        To enable table level browse

        """
        properties = self.properties
        properties['db2SubclientProp']["enableTableBrowse"] = True
        self.update_properties(properties_dict=properties)

    def enable_acs_backup(self):
        """
        To enable DB2 ACS backup
        """
        properties = self.properties
        properties['commonProperties']["snapCopyInfo"]["useDB2ACSInterface"] = True
        self.update_properties(properties_dict=properties)

    @property
    def backup_mode_online(self):
        """
                Getter to fetch online backup mode is enabled or disabled

                Returns:

                    (bool)      -   boolean value is returned based on the status of data backup option
                                    0 - online database , 1 - offline database
                """

        return self._subclient_properties.get("db2SubclientProp", {}).get('db2BackupMode', 0)

    @backup_mode_online.setter
    def backup_mode_online(self, value):
        """
        To enable or disable online backup mode

        Args:
            value (bool)    - to enable or disable online backup mode for db2 subclient

        """
        self._set_subclient_properties("_db2_subclient_properties['db2BackupMode']", value)

    def _get_subclient_properties(self):
        """Gets the subclient properties of this subclient.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        super(DB2Subclient, self)._get_subclient_properties()
        if 'db2SubclientProp' not in self._subclient_properties:
            self._subclient_properties['db2SubclientProp'] = {}
        self._db2_subclient_properties = self._subclient_properties['db2SubclientProp']
        self._db2_delete_logfiles_after = self._db2_subclient_properties.get(
            'db2DeleteLogFilesAfter')
        self._db2_backup_logfile = self._db2_subclient_properties.get('db2BackupLogFiles')
        self._subclient_properties.get("db2SubclientProp", {}).get('db2BackupData')

    def _get_subclient_properties_json(self):
        """returns subclient property json for db2
                   Returns:
                        dict - all subclient properties put inside a dict
        """
        '''subclient_json = {
            "subClientProperties":{
                "db2SubclientProp":
                    {
                        "db2BackupData": None
                    }
            }
        }'''

        subclient_json = {"subClientProperties":
                          {
                              "commonProperties": self._commonProperties,
                              "db2SubclientProp": self._db2_subclient_properties,
                              "proxyClient": self._proxyClient,
                              "subClientEntity": self._subClientEntity
                          }
                          }
        return subclient_json

    def _db2_backup_request_json(self,
                                 backup_level,
                                 **kwargs):
        """
        Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
               backup_level                     (list)  --  level of backup the user wish to run
                                                            Full / Incremental / Differential

               create_backup_copy_immediately   (bool)  --  Sybase snap job needs
                                                            this backup copy operation
                    default : False

               backup_copy_type                 (int)   --  backup copy job to be launched
                                                            based on below two options
                 default : 2,
                 possible values :
                            1 (USING_STORAGE_POLICY_RULE),
                            2( USING_LATEST_CYCLE)

            Returns:

                (dict) - JSON request to pass to the API

        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")
        create_backup_copy_immediately = kwargs.get("create_backup_copy_immediately", False)
        backup_copy_type = kwargs.get("backup_copy_type", 2)
        db2_options = dict()
        if create_backup_copy_immediately:
            sub_opt = {"dataOpt":
                       {
                           "createBackupCopyImmediately": create_backup_copy_immediately,
                           "backupCopyType": backup_copy_type
                       }
                      }
            db2_options.update(sub_opt)
        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            db2_options
        )
        return request_json

    def db2_backup(self,
                   backup_level="full",
                   **kwargs):
        """
        Performs backup on DB2 subclient

        Args:
            backup_level                            (str)   --  Level of backup.
                                                                full|incremental|differential

            create_backup_copy_immediately          (bool)  --  Sybase snap job needs
                                                                this backup copy operation
                    default : False

            backup_copy_type                        (int)   --  backup copy job to be launched
                                                                based on below two options
             default : 2,
             possible values :
                        1 (USING_STORAGE_POLICY_RULE),
                        2( USING_LATEST_CYCLE)

        Returns:
            (object) - instance of Job class

        Raises:
            SDKException:
                if backup level is incorrect

                if response is empty

                if response does not succeed

        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'incremental', 'differential']:
            raise SDKException('Subclient', '103')

        create_backup_copy_immediately = kwargs.get("create_backup_copy_immediately", False)

        if create_backup_copy_immediately:
            if backup_level != 'full':
                raise SDKException(
                    'Subclient', '102', 'Backup Copy job is not valid for Incremental or Differential')

        request_json = self._db2_backup_request_json(backup_level, **kwargs)

        backup_service = self._commcell_object._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service, request_json
        )
        return self._process_backup_response(flag, response)
