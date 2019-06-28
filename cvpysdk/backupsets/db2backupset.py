# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a DB2 Backupset.

DB2Backupset is the only class defined in this file.

DB2Backupset:  Derived class from Backupset Base class, representing a db2 backupset,
and to perform operations on that subclient

DB2Backupset:
=============

    restore_entire_database()       --      runs the restore job for specified backupset


DB2Backupset instance Attributes:
=================================

    **db2_db_status**       --      returns db2 database status

"""

from __future__ import unicode_literals

from ..backupset import Backupset


class DB2Backupset(Backupset):
    """Derived class from Backupset Base class, representing a db2 backupset,
        and to perform operations on that backupset."""

    @property
    def db2_db_status(self):
        """
        returns db2 database status

        Returns:
            (str) -- Status of db as connected or disconnected

        """
        return self._properties.get('db2BackupSet', {}).get('dB2DBStatus', "")

    def restore_entire_database(
            self,
            dest_client_name=None,
            dest_instance_name=None,
            dest_database_name=None,
            recover_db=True,
            restore_incremental=True

    ):
        """Restores the db2 databases specified in the input paths list to the same location.

            Args:
                dest_client_name        (str)   --  destination client name where db need to be
                restored

                dest_instance_name      (str)   --  destination db2 instance name of destination
                client

                dest_database_name      (str)   --  destination database name

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
        self._instance_object._restore_association = self._backupset_association

        instance_object = self._instance_object
        if dest_client_name is None:
            dest_client_name = instance_object._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = instance_object.instance_name

        if dest_database_name is None:
            dest_database_name = self.backupset_name.upper()

        return self._instance_object.restore_entire_database(
            dest_client_name, dest_instance_name, dest_database_name,
            recover_db=recover_db, restore_incremental=restore_incremental)
