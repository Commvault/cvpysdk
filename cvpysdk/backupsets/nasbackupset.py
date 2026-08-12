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

"""Module for performing operations on a Backupset for the **NAS / NDMP** Agent.

NASBackupset is the only class defined in this file.

NASBackupset: Derived class from Backupset Base class, representing a **NAS / NDMP** backupset,
and to perform operations on that subclient

NASBackupset:

    _get_backupset_properties()     --  gets the properties of this subclient

    set_image_backupset()           --  sets this backupset as image backupset

"""

from __future__ import unicode_literals

from .fsbackupset import FSBackupset
from ..exception import SDKException


class NASBackupset(FSBackupset):
    """
    Represents a NAS/NDMP backupset, derived from the Backupset base class.

    This class provides specialized functionality for managing NAS (Network Attached Storage)
    and NDMP (Network Data Management Protocol) backupsets. It enables users to perform
    operations specific to NAS backupsets, including retrieving backupset properties and
    managing image backupset settings.

    Key Features:
        - Retrieve NAS/NDMP backupset properties
        - Check if the backupset is configured as an image backupset
        - Set the backupset as an image backupset

    #ai-gen-doc
    """

    def _get_backupset_properties(self) -> None:
        """Retrieve and set NAS backupset-specific properties.

        This method overrides the base class implementation to extract NAS-specific
        backupset properties, such as determining if the backupset is configured for
        NetApp image backup. It updates internal state based on the backupset's configuration.

        Example:
            >>> nas_backupset = NASBackupset(...)
            >>> nas_backupset._get_backupset_properties()
            >>> print(nas_backupset._is_image_backupset)
            >>> # The _is_image_backupset attribute will reflect whether NetApp image backup is enabled

        #ai-gen-doc
        """
        super(NASBackupset, self)._get_backupset_properties()

        self._is_image_backupset = False

        if 'fsBackupSet' in self._properties:
            if 'netAppImageBackup' in self._properties['fsBackupSet']:
                self._is_image_backupset = bool(
                    self._properties['fsBackupSet']['netAppImageBackup']
                )

    @property
    def is_image_backupset(self) -> bool:
        """Indicate whether this NAS backupset is configured as an image backupset.

        Returns:
            True if the backupset is an image backupset, False otherwise.

        Example:
            >>> backupset = NASBackupset(...)
            >>> if backupset.is_image_backupset:
            ...     print("This is an image backupset.")
            ... else:
            ...     print("This is a file-level backupset.")

        #ai-gen-doc
        """
        return self._is_image_backupset

    def set_image_backupset(self) -> None:
        """Set this backupset as the image backupset if it is not already configured as such.

        This method updates the backupset properties to enable image backup functionality.
        If the backupset is already set as an image backupset, no action is taken.

        Raises:
            SDKException: If the operation fails to set this backupset as the image backupset.

        Example:
            >>> backupset = NASBackupset(...)
            >>> backupset.set_image_backupset()
            >>> print("Backupset is now configured for image backup.")

        #ai-gen-doc
        """
        if self.is_image_backupset is False:
            request_json = {
                "association": {
                    "entity": [{
                        "clientName":
                            self._instance_object._agent_object._client_object.client_name,
                        "appName": self._instance_object._agent_object.agent_name,
                        "instanceName": self._instance_object.instance_name,
                        "backupsetName": self.backupset_name
                    }]
                },
                "backupsetProperties": {
                    "fsBackupSet": {
                        "netAppImageBackup": True
                    }
                }
            }

            output = self._process_update_reponse(request_json)

            if output[0]:
                return
            else:
                o_str = 'Failed to set the backupset as Image backupset\nError: "{0}"'
                raise SDKException('Backupset', '102', o_str.format(output[2]))
