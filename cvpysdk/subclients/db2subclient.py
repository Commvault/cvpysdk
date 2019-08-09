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
        To enable or disable data backup

        """

        self._set_subclient_properties("_db2_subclient_properties['db2BackupData']", True)

    def disable_backupdata(self):
        """
        To enable or disable data backup

        """

        self._set_subclient_properties("_db2_subclient_properties['db2BackupData']", False)

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
