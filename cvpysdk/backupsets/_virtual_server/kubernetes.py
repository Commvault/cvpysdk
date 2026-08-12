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

"""File for operating on a Virtual Server Kubernetes Backupset.

KubernetesBackupset is the only class defined in this file.

KubernetesBackupset:               Derived class from Virtual server Backupset Base
                                    class,representing a Kubernetes Backupset ,
                                    and to perform operations on that Backupset

KubernetesBackupset:

    __init__(
        instance_object,
        backupset_name,
        backupset_id)           --  initialize object of Kubernetes backupset class,
                                    associated with the VirtualServer subclient

    refresh ()                    --  refresh the Backupset associated with the agent

    application_groups()        --   Apllication groups property

"""
from enum import Enum
from json import JSONDecodeError
from typing import *
from cvpysdk.backupsets.vsbackupset import VSBackupset
from cvpysdk.exception import SDKException
from ...subclients.virtualserver.kubernetes import ApplicationGroups


class KubernetesBackupset(VSBackupset):
    """
    Represents a Kubernetes Backupset, derived from the Virtual Server Backupset base class.

    This class provides an interface for managing and performing operations on Kubernetes backupsets,
    including initialization, refreshing backupset data, and accessing application groups associated
    with the backupset.

    Attributes:
        _blr_pair_details (dict): Stores BLR (Block Level Replication) pair details for the backupset.
        _application_groups (ApplicationGroups): Manages application groups within the Kubernetes backupset.

    Usage:
        k8s_backupset = KubernetesBackupset(instance_object, 'default')

    Key Features:
        - Initialization of Kubernetes backupset with instance object, name, and ID
        - Refreshing backupset data to ensure up-to-date information
        - Access to application groups via a property for managing group operations

    #ai-gen-doc
    """

    def __init__(self, instance_object: object, backupset_name: str, backupset_id: Optional[str] = None) -> None:
        """Initialize a KubernetesBackupset object for managing backup operations.

        Args:
            instance_object: Object representing the Virtual Server instance associated with the backupset.
            backupset_name: Name of the backupset as a string.
            backupset_id: Optional string representing the unique ID of the backupset. If not provided, a default value is used.

        Example:
            >>> instance = VirtualServerInstance(...)
            >>> backupset = KubernetesBackupset(instance, "K8s_Backupset", backupset_id="12345")
            >>> # The backupset object can now be used for backup management tasks

        #ai-gen-doc
        """
        self._blr_pair_details = None
        super().__init__(instance_object, backupset_name, backupset_id)
        self._application_groups = None

    def refresh(self) -> None:
        """Reload the properties of the KubernetesBackupset object.

        This method refreshes the backupset's internal state, ensuring that 
        the latest properties and application group information are retrieved.
        Cached data is cleared and will be reloaded on subsequent access.

        Example:
            >>> backupset = KubernetesBackupset(...)
            >>> backupset.refresh()  # Updates backupset properties and clears cached application groups
            >>> print("Backupset properties refreshed successfully")

        #ai-gen-doc
        """
        super().refresh()
        self._application_groups = None

    @property
    def application_groups(self) -> 'ApplicationGroups':
        """Get the ApplicationGroups object associated with this Kubernetes backupset.

        Returns:
            ApplicationGroups: An instance for managing application groups within the backupset.

        Example:
            >>> k8s_backupset = KubernetesBackupset(...)
            >>> app_groups = k8s_backupset.application_groups  # Use dot notation for property access
            >>> print(f"Application groups object: {app_groups}")
            >>> # The returned ApplicationGroups object can be used for further group management

        #ai-gen-doc
        """
        if self._application_groups is None:
            self._application_groups = ApplicationGroups(self)
        return self._application_groups
