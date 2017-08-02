#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a SAP HANA Backupset

HANABackupset is the only class defined in this file.

HANABackupset: Derived class from Backupset Base class, representing a SAP HANA backupset,
                        and to perform operations on that subclient

HANABackupset:
    _get_backupset_properties()     --  gets the properties of this subclient

    restore()                       --  runs the restore job for specified backupset

"""

from __future__ import unicode_literals

from ..backupset import Backupset
from ..exception import SDKException


class HANABackupset(Backupset):
    """Derived class from Backupset Base class, representing a SAP HANA backupset,
        and to perform operations on that backupset."""

    def _get_backupset_properties(self):
        """Derived class from Backupset Base class, representing a SAP HANA backupset,
            and to perform operations on that backupset."""
        super(HANABackupset, self)._get_backupset_properties()

    def restore(
            self,
            pseudo_client,
            instance,
            backup_prefix=None,
            point_in_time=None,
            initialize_log_area=False,
            use_hardware_revert=False,
            clone_env=False,
            check_access=True,
            destination_instance_dir=None,
            ignore_delta_backups=True):
        """Restores the databases specified in the input paths list.

            Args:
                pseudo_client                (str)       -- The HANA client where the database
                                                                should be restored

                instance                     (str)       -- The destination instance where the
                                                                database should be restored

                backup_prefix                (str)       -- The prefix of the backup job
                    default: None

                point_in_time                (str)       -- The time to which the database
                                                                should be restored to
                    default: None

                initialize_log_area           (bool)      -- Option to initialize new log area after
                                                                restore
                    default: False

                use_hardware_revert           (bool)      -- Option to do a hardware revert in
                                                                restore
                    default: False

                clone_env                    (bool)      -- Option to decide whether the database
                                                                should be cloned or not
                    default: False

                check_access                 (bool)      -- Option to check access during restore
                    default: True

                destination_instance_dir      (str)       -- For snap cross instance restore or
                                                                cross machine restores requires
                                                                HANA data directory
                    default: None

                ignore_delta_backups          (bool)      -- Option to ignore delta backups during
                                                                restore
                    default: True

                    default: default

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if instance is not a string or object

                    if response is empty

                    if response is not success
        """
        from ..instance import Instance

        if not (isinstance(instance, str) or isinstance(instance, basestring)):
            raise SDKException('Instance', '101')

        request_json = self._instance_object._restore_request_json(
            pseudo_client,
            instance,
            backup_prefix,
            point_in_time,
            initialize_log_area,
            use_hardware_revert,
            clone_env,
            check_access,
            destination_instance_dir,
            ignore_delta_backups,
            self.backupset_name
        )

        return self._instance_object._process_restore_response(request_json)
        