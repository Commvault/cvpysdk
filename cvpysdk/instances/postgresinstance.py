# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a POSTGRESQL Instance.

PostgreSQLInstance is the only class defined in this file.

PostgreSQLInstance: Derived class from Instance Base class, representing a postgres server instance,
                       and to perform operations on that instance

PostgreSQLInstance:

    _get_postgres_restore_json()    --  returns the restore request json for FSBased restore


    restore_postgres_server()       --  runs the restore job for postgres instance

PostgreSQLInstance instance Attributes
==================================

    **postgres_bin_directory**           --  returns the `postgres_bin_directory` of postgres server

    **postgres_archive_log_directory**   --  returns the `postgres_archive_log_directory`
                                                of postgres server

    **postgres_server_user_name**        --  returns the `postgres_server_user_name`
                                                of postgres server

    **postgres_server_port_number**      --  returns the `postgres_server_port_number`
                                                of postgres server

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
        self.cvpysdk_object = self._commcell_object._cvpysdk_object
        self.services = self._commcell_object._services

    def _get_postgres_restore_json(
            self,
            destination_client,
            destination_instance_name):
        """Generates the JSON input required to run Postgres FS
                Based Backupset and return the generated JSON

            Args:
                destination_client          (str) -- Name of the destination client to which
                                                        the data should be restored
                destination_instance_name   (str) -- Name of the desired instance in the
                                                        destination client
            Returns:
                JSON  -   JSON required to run the restore job

        """
        basic_postgres_options = {
            "browseOption": {
                "backupset": {
                    "clientName": destination_client,
                    "backupsetName": "FSBasedBackupSet"
                },
                "timeZone": {
                    "TimeZoneName": "(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi"
                },
                "timeRange": {}
            },
            "commonOptions": {
                "clusterDBBackedup": False,
                "restoreToDisk": False,
                "onePassRestore": False,
                "syncRestore": False
            },
            "destination": {
                "destinationInstance": {
                    "clientName": destination_client,
                    "instanceName": destination_instance_name,
                    "appName": "PostgreSQL"
                },
                "destClient": {
                    "clientName": destination_client
                }
            },
            "fileOption": {
                "sourceItem": [
                    "/data"
                ]
            },
            "postgresRstOption": {
                "pointInTime": False,
                "restoreToSameServer": False,
                "tableLevelRestore": False,
                "instanceRestore": False,
                "fsBackupSetRestore": True,
                "startServer": True,
                "isCloneRestore": False,
                "fromTime": {},
                "refTime": {}
            }
        }

        restore_json = self._restore_json(paths=r'/')

        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"] = basic_postgres_options

        return restore_json

    def restore_postgres_server(
            self,
            destination_client,
            destination_instance_name):
        """
        Method to restore the Postgres server

        Args:
        destination_client (str) -- Destination Client name

        destination_instance_name (str) -- Destination Instance name

        Returns:
            object -- Job containing restore details
        """

        if destination_client is None:
            destination_client = self._properties[r"instance"][r"clientName"]

        if destination_instance_name is None:
            destination_instance_name = self.instance_name
        request_json = self._get_postgres_restore_json(
            destination_client, destination_instance_name)

        return self._process_restore_response(request_json)

    @property
    def postgres_bin_directory(self):
        """Returns the bin directory of postgres server"""
        if self._properties['postGreSQLInstance']['BinaryDirectory']:
            return self._properties['postGreSQLInstance']['BinaryDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Binary directory.")

    @property
    def postgres_archive_log_directory(self):
        """Returns the archive log directory of postgres server"""
        if self._properties['postGreSQLInstance']['ArchiveLogDirectory']:
            return self._properties['postGreSQLInstance']['ArchiveLogDirectory']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Archive log directory.")

    @property
    def postgres_server_user_name(self):
        """Returns the username of postgres server"""
        if self._properties['postGreSQLInstance']['SAUser']['userName']:
            return self._properties['postGreSQLInstance']['SAUser']['userName']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the Server name.")

    @property
    def postgres_server_port_number(self):
        """Returns the port number associated with postgres server"""
        if self._properties['postGreSQLInstance']['port']:
            return self._properties['postGreSQLInstance']['port']
        raise SDKException(
            'Instance',
            '105',
            "Could not fetch the port Number.")
