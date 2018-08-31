# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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
    """Derived class from Backupset Base class, representing a **NAS / NDMP** backupset,
        and to perform operations on that backupset.

    """

    def _get_backupset_properties(self):
        """Derived class from Backupset Base class, representing a nas backupset,
            and to perform operations on that backupset."""
        super(NASBackupset, self)._get_backupset_properties()

        self._is_image_backupset = False

        if 'fsBackupSet' in self._properties:
            if 'netAppImageBackup' in self._properties['fsBackupSet']:
                self._is_image_backupset = bool(
                    self._properties['fsBackupSet']['netAppImageBackup']
                )

    @property
    def is_image_backupset(self):
        """Treats is_image_backupset as a read-only property"""
        return self._is_image_backupset

    def set_image_backupset(self):
        """Sets the backupset represented by this Backupset class instance as the image backupset
            if it is not the image backupset.

            Raises:
                SDKException:
                    if failed to set this as the image backupset

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
