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

from ..backupset import Backupset
from ..exception import SDKException
from typing import Union, Optional

class HANABackupset(Backupset):
    """
    Represents a SAP HANA backupset, extending the Backupset base class.

    This class provides specialized functionality for managing SAP HANA backupsets,
    including performing restore operations with various configuration options.
    It is designed to facilitate backupset management and restoration tasks
    specific to SAP HANA environments.

    Key Features:
        - Restore SAP HANA backupsets to specified instances and directories
        - Support for point-in-time restores
        - Options to initialize log area and use hardware revert
        - Ability to clone environments and check access during restore
        - Configurable destination instance directory and delta backup handling

    #ai-gen-doc
    """

    def restore(
            self,
            pseudo_client: str,
            instance: Union[str, 'Instance'],
            backup_prefix: Optional[str] = None,
            point_in_time: Optional[str] = None,
            initialize_log_area: bool = False,
            use_hardware_revert: bool = False,
            clone_env: bool = False,
            check_access: bool = True,
            destination_instance_dir: Optional[str] = None,
            ignore_delta_backups: bool = True
        ) -> 'Job':
        """Restore HANA databases to a specified client and instance.

        This method initiates a restore operation for HANA databases, allowing customization of restore options such as point-in-time recovery, hardware revert, cloning, and log area initialization.

        Args:
            pseudo_client: Name of the HANA client where the database will be restored.
            instance: Destination instance for the restore operation. Can be a string or an Instance object.
            backup_prefix: Optional prefix of the backup job to restore from.
            point_in_time: Optional timestamp to restore the database to a specific point in time.
            initialize_log_area: Whether to initialize the new log area after restore. Default is False.
            use_hardware_revert: Whether to perform a hardware revert during restore. Default is False.
            clone_env: Whether to clone the database environment during restore. Default is False.
            check_access: Whether to check access permissions during restore. Default is True.
            destination_instance_dir: Optional HANA data directory for cross-instance or cross-machine restores.
            ignore_delta_backups: Whether to ignore delta backups during restore. Default is True.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the instance parameter is not a string or Instance object, or if the restore response is empty or unsuccessful.

        Example:
            >>> # Restore a HANA database to a specific client and instance
            >>> backupset = HANABackupset(...)
            >>> job = backupset.restore(
            ...     pseudo_client="hana_client1",
            ...     instance="hana_instance1",
            ...     backup_prefix="daily_backup",
            ...     point_in_time="2024-06-01 12:00:00",
            ...     initialize_log_area=True,
            ...     use_hardware_revert=False,
            ...     clone_env=False,
            ...     check_access=True,
            ...     destination_instance_dir="/hana/data",
            ...     ignore_delta_backups=True
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        from ..instance import Instance

        if not isinstance(instance, (str, Instance)):
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
