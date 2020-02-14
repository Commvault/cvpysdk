#!/usr/bin/env python
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

"""File for operating on a Database Server Subclient

DatabaseSubclient is the only class defined in this file.

DatabaseSubclient: Derived class from Subclient Base class, representing a Database server subclient,
                        and to perform operations on that subclient

DatabaseSubclient:
    

    log_backup_storage_policy()         --  updpates the log backup storage policy for this
                                                subclient


"""
from __future__ import unicode_literals
from past.builtins import basestring

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
        if isinstance(value, basestring):
            value = value.lower()

            if not self._commcell_object.storage_policies.has_policy(value):
                raise SDKException(
                    'Subclient',
                    '102',
                    'Storage Policy: "{0}" does not exist in the Commcell'.format(value)
                )

            self._set_subclient_properties(
                "_commonProperties['storageDevice']['logBackupStoragePolicy']",
                {
                    "storagePolicyName": value,
                    "storagePolicyId": int(
                        self._commcell_object.storage_policies.all_storage_policies[value]
                    )
                }
            )
        else:
            raise SDKException('Subclient', '101')

