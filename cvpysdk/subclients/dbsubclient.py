#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Database Server Subclient

DatabaseSubclient is the only class defined in this file.

DatabaseSubclient: Derived class from Subclient Base class, representing a Database server subclient,
                        and to perform operations on that subclient

DatabaseSubclient:
    

    log_backup_storage_policy()         --  updpates the log backup storage policy for this
                                                subclient


"""
from __future__ import unicode_literals

from ..subclient import Subclient
from ..exception import SDKException

class DatabaseSubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient."""

    @property
    def log_backup_storage_policy(self):
        """Treats the subclient description as a property of the Subclient class."""
        storage_device = self._subclient_properties['commonProperties']['storageDevice']

        if 'logBackupStoragePolicy' in storage_device:
            if 'storagePolicyName' in storage_device['logBackupStoragePolicy']:
                return  str(
                    storage_device['logBackupStoragePolicy']['storagePolicyName']
                )

    @log_backup_storage_policy.setter
    def log_backup_storage_policy(self, value):
        """Sets the log backup storage policy of subclient as the value provided as input.

            Args:
                value   (str)   -- Log backup Storage policy name to be assigned to subclient

            Raises:
                SDKException:
                    if failed to update log backup storage policy name

                    if log backup storage policy name is not in string format
        """
        if isinstance(value, str):
            self._set_subclient_properties("_commonProperties['storageDevice']['logBackupStoragePolicy']['storagePolicyName']",value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient log backup storage policy should be a string value'
            )
