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

"""File for operating on a SAP HANA Backupset.

HANABackupset is the only class defined in this file.

HANABackupset:  Derived class from Backupset Base class, representing a SAP HANA backupset,
                    and to perform operations on that subclient

HANABackupset:

    restore()       --      runs the restore job for specified backupset

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

from ..backupset import Backupset
from ..exception import SDKException


class HANABackupset(Backupset):
    """Derived class from Backupset Base class, representing a SAP HANA backupset,
        and to perform operations on that backupset.
    """

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
                pseudo_client               (str)   --  HANA client to restore the database at

                instance                    (str)   --  destination instance to restore the db at

                backup_prefix               (str)   --  prefix of the backup job
                    default: None

                point_in_time               (str)   --  time to which db should be restored to
                    default: None

                initialize_log_area         (bool)  --  boolean to specify whether to initialize
                                                            the new log area after restore
                    default: False

                use_hardware_revert         (bool)  --  boolean to specify whether to do a
                                                            hardware revert in restore
                    default: False

                clone_env                   (bool)  --  boolean to specify whether the database
                                                            should be cloned or not
                    default: False

                check_access                (bool)  --  check access during restore or not
                    default: True

                destination_instance_dir    (str)   --  HANA data directory for snap cross instance
                                                            restore or cross machine restores
                    default: None

                ignore_delta_backups        (bool)  --  whether to ignore delta backups during
                                                            restore or not
                    default: True

            Returns:
                object  -   instance of the Job class for this restore job

            Raises:
                SDKException:
                    if instance is not a string or object

                    if response is empty

                    if response is not success

        """
        from ..instance import Instance

        if not isinstance(instance, (basestring, Instance)):
            raise SDKException('Backupset', '101')

        request_json = self._instance_object._restore_request_json(
            pseudo_client,
            instance,
            self.backupset_name,
            backup_prefix,
            point_in_time,
            initialize_log_area,
            use_hardware_revert,
            clone_env,
            check_access,
            destination_instance_dir,
            ignore_delta_backups
        )

        return self._instance_object._process_restore_response(request_json)
