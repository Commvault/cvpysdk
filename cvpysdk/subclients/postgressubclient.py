# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Postgres Server Subclient

PostgresSubclient is the only class defined in this file.

PostgresSubclient: Derived class from Subclient Base class, representing a HANA server subclient,
                        and to perform operations on that subclient

PostgresSubclient:
    _backup_request_json()               --  prepares the json for the backup request

    _get_subclient_properties()          --  gets the subclient  related properties of File System subclient.

    _get_subclient_properties_json()     --  gets all the subclient  related properties of File System subclient.

    content()                            --  update the content of the subclient

    log_backup_storage_policy()          --  updpates the log backup storage policy for this
                                                subclient

    backup()                             --  run a backup job for the subclient

    _get_postgres_restore_json()         --  returns the restore request json for DumpBased restore

    _get_postgres_restore_json_FS()      --  returns the restore request json for FSBased restore

    restore_postgres_server()            --  runs the restore job for postgres instance with a specified backupset and subclient

PostgresSubclient instance Attributes
=====================================

    **content**                          --  returns all the databases in the content of postgres subclient
"""
from __future__ import unicode_literals

from ..subclient import Subclients

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
        super(PostgresSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self._postgres_properties = {}

    def _backup_request_json(
            self,
            backup_level,
            backup_prefix=None):
        """
        Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                backup_level   (list)  --  level of backup the user wish to run
                        Full / Incremental / Differential
                backup_prefix   (str)   --  the prefix that the user wish to add to the backup

            Returns:
                dict - JSON request to pass to the API
        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")
        hana_options = {
            "hanaOptions": {
                "backupPrefix": str(backup_prefix)
            }
        }
        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            hana_options
        )

        return request_json

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of Postgres subclient.

        """
        super(DatabaseSubclient, self)._get_subclient_properties()
        if (self.subclient_name != "default"):
            if 'content' in self._subclient_properties:
                self._content = self._subclient_properties['content']
        else:
            self._content = None

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "impersonateUser": self._impersonateUser,
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def content(self):
        """Treats the subclient content as a property of the Subclient class."""
        content = self._content
        database_list = list()
        for database in content:
            if database.get('postgreSQLContent'):
                if database['postgreSQLContent'].get('databaseName'):
                    database_list.append(database[
                        'postgreSQLContent']['databaseName'].lstrip("/"))
        return database_list

    @content.setter
    def content(self, value):
        """Sets the content of the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update content of subclient

                    if the type of value input is not list

                    if value list is empty
        """

        raise SDKException(
            'Subclient',
            '102',
            ('Updating Postgres subclient Content is not allowed. ')
        )

    @property
    def browse(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'browse'
        ))

    @property
    def browse_in_time(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'browse_in_time'
        ))

    @property
    def find(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'find'
        ))

    @property
    def restore_in_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'restore_in_place'
        ))

    @property
    def restore_out_of_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'restore_out_of_place'
        ))

    def backup(
            self,
            backup_level="Differential",
            backup_prefix=None):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential
                    default: Differential

                backup_prefix       (str)   --  the prefix that the user wish to add to the backup
                    default: None

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'incremental', 'differential']:
            raise SDKException('Subclient', '103')

        if backup_prefix is None:
            return super(PostgresSubclient, self).backup(backup_level)

        else:
            request_json = self._backup_request_json(
                backup_level, backup_prefix)
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._commcell_object._services['CREATE_TASK'], request_json
            )
            return self._process_backup_response(flag, response)

    def _get_postgres_browse_options(self, destination_client, bkpset_name):
        self._postgres_browse_options = {
            "backupset": {
                "clientName": destination_client,
                "backupsetName": bkpset_name
            },
            "timeRange": {}
        }
        return self._postgres_browse_options

    def _get_postgres_destination(
            self, destination_client, destination_instance_name):
        self._postgres_destination = {
            "destinationInstance": {
                "clientName": destination_client,
                "instanceName": destination_instance_name,
                "appName": "PostgreSQL"
            },
            "destClient": {
                "clientName": destination_client
            }
        }
        return self._postgres_destination

    def _get_postgres_file_options(self, database_list):
        self._postgres_file_options = {
            "sourceItem": database_list
        }
        return self._postgres_file_options

    def _get_postgres_restore_options(self, bkp_set_flag):
        self._postgres_restore_options = {
            "restoreToSameServer": False,
            "tableLevelRestore": False,
            "instanceRestore": False,
            "fsBackupSetRestore": bkp_set_flag,
            "isCloneRestore": False,
            "refTime": {}
        }
        return self._postgres_restore_options

    def _get_postgres_restore_json(
            self, bkpset_name, database_list, destination_client, destination_instance_name):
        """Generates the JSON input required to run Postgres DumpBased Backupset and return the generated JSON

            Args:
                bkpset_name (str)  --  Name of the backup set
                database_list (List) -- List of databases that have t be restored
                destination_client (str) -- Name of the destination client to which the data should be restored
                destination_instance_name (str) -- Name of the desired instance in the destination client
            Returns:
                JSON  -   JSON required to run the restore job

        """
        # if bkpset_name.lower() == "fsbasedbackupset":
        #     database_list = ["/data"]

        """Generates the JSON input required to run Postgres DumpBased Backupset and return the generated JSON

            Args:
                bkpset_name (str)  --  Name of the backup set
                subclient_name (str) -- Name of the subclient
                database_list (List) -- List of databases that have t be restored
                destination_client (str) -- Name of the destination client to which the data should be restored
                destination_instance_name (str) -- Name of the desired instance in the destination client
            Returns:
                JSON  -   JSON required to run the restore job

        """
        if (bkpset_name.lower() == "fsbasedbackupset"):
            bkp_set_flag = True
        else:
            bkp_set_flag = False
        basic_postgres_options = {
            "browseOption": self._get_postgres_browse_options(destination_client, bkpset_name),
            "destination": self._get_postgres_destination(destination_client, destination_instance_name),
            "fileOption": self._get_postgres_file_options(database_list),
            "postgresRstOption": self._get_postgres_restore_options(bkp_set_flag),
            "copy_precedence": None
        }

        restore_json = self._restore_json(paths=r'/')

        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"] = basic_postgres_options
        db_options = {}
        return restore_json

    def restore_postgres_server(
            self, database_list, destination_client, destination_instance_name):
        """
        Method to restore the Postgres server

        Args:
        bkpsetName (str) -- BackupSet name
        database_list (List) -- List of databases
        destination_client (str) -- Destination Client name
        destination_instance_name (str) -- Destination Instance name

        Returns:
            object -- Job containing restore details
        """

        if destination_client is None:
            destination_client = self._properties[r"subclient"][r"instance"][r"clientName"]

        if destination_instance_name is None:
            destination_instance_name = self._properties[r"subclient"][r"instanceName"]
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        bkpset_name = self._backupset_object.backupset_name

        restore_json = self._get_postgres_restore_json(
            bkpset_name, database_list, destination_client, destination_instance_name)

        return self._process_restore_response(restore_json)

