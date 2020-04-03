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

"""File for operating on a Sharepoint Backupset.

SPBackupset is the only class defined in this file.

SPBackupset:  Derived class from Backupset Base class, representing a sharepoint backupset,
and to perform operations on that subclient

SPBackupset:
=============

    azure_storage_details()      --  updates azure storage details in sharepoint backupset properties

"""

from __future__ import unicode_literals

from ..backupset import Backupset


class SharepointBackupset(Backupset):
    """Derived class from Backupset Base class, representing a sharepoint backupset,
        and to perform operations on that backupset."""

    @property
    def azure_storage_details(self):
        """
        Returns azure storage details associated with backupset

        Returns:
            azure_storage_account_information  (dict)  -- dictionary of azure storage account details

        """
        backupset_properties = self.properties
        azure_storage_account_information = None
        accounts = backupset_properties["sharepointBackupSet"]["spOffice365BackupSetProp"]["serviceAccounts"]\
            ["accounts"]
        for account in accounts:
            if account.get("serviceType", -1) == 52:
                azure_storage_account_information = account
        return azure_storage_account_information

    @azure_storage_details.setter
    def azure_storage_details(self, azure_storage_account_information):
        """Updates azure storage details in sharepoint backupset properties

            Args:

                    azure_storage_account_information (dict)--  information of azure account
                                                        azure_storage_account_information : {
                                                            "serviceType": 52,
                                                            "userAccount": {
                                                                "password": azure_secret,
                                                                "userName": azure_username
                                                            }
                                                        }

        """
        backupset_properties = self.properties
        backupset_properties["sharepointBackupSet"]["spOffice365BackupSetProp"]["serviceAccounts"]["accounts"].append(
            azure_storage_account_information)
        backupset_properties["commonBackupSet"]["isDefaultBackupSet"] = False
        backupset_properties["sharepointBackupSet"]["spOffice365BackupSetProp"]["additionalCredentials"] = {}
        backupset_properties["backupSetEntity"]["flags"] = {}
        self.update_properties(backupset_properties)
