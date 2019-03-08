# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

    _default_db2_subclient_props()    --  returns subclient property json for db2

    data()                              --  Getter and Setter for enabling data mode in db2

    db2_use_dedupe_device               -- getter and setter for enabling dedupe device option for db2

    db2_delete_log_files_after          -- getter and setter for enabling delete log files after option in db2

    db2_backup_log_files                -- getter and setter for enabling backup log files option for db2

"""
from __future__ import unicode_literals
from ..subclient import Subclient
from ..exception import SDKException


class DB2Subclient(Subclient):
    """
        DB2Subclient is a class to work on DB2 subclients

    """

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
        return  self._properties.get('db2SubclientProp',{}).get('db2DeleteLogFilesAfter')

    @property
    def data(self):
        """
        Getter to fetch if data enabled in oracle subclient or not

            Returns:
                bool     --  True if data is enabled on the subclient. Else False

        """
        return self._db2_subclient_properties.get("data")

    @property
    def db2_backup_log_files(self):
        """
        Getter to fetch backup logfiles option is enabled or not
        Returns:
        Bool - True if delete log files option is enabled on the subclient. Else False

        """
        return self._properties.get('db2SubclientProp', {}).get('db2BackupLogFiles')

    def _get_subclient_properties(self):
        """Gets the subclient properties of this subclient.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        super(DB2Subclient, self)._get_subclient_properties()


        self._db2_subclient_properties = self._subclient_properties.get('db2SubclientProp',
                                                                            self._default_db2_subclient_props())

    def _default_db2_subclient_props(self):
        """returns subclient property json for db2
                   Returns:
                        dict - all subclient properties put inside a dict
        """
        db2_properties = {

            "db2SubclientProperties": {
                "db2BackupData": True,
                "db2BackupType": None,
                "db2BackupMode": 0,
                "db2NumberofBuffer": 2,
                "db2BufferSize": 1024,
                "db2Parallelism": 0,
                "db2UseCompression": False,
                "db2BackupLogFiles": True,
                "db2DeleteLogFilesAfter": False,
                "db2DisableSwitchCurrentLog": None,
                "numberOfBackupStreams": None
            }
        }
        return db2_properties
