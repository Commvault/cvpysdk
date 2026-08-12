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
from typing import Optional, Dict, Any

class SharepointBackupset(Backupset):
    """
    Represents a SharePoint backupset, extending the Backupset base class.

    This class is designed to manage and perform operations specific to SharePoint backupsets,
    including support for both SharePoint Online and integration with Azure storage accounts.
    It provides properties to determine the type of SharePoint instance and to access Azure storage details,
    as well as methods to handle Azure storage account information.

    Key Features:
        - Identification of SharePoint Online instances
        - Access to Azure storage account details
        - Management of Azure storage account information for backup operations

    #ai-gen-doc
    """

    @property
    def is_sharepoint_online_instance(self) -> bool:
        """Check if the backupset is a SharePoint Online instance.

        Returns:
            True if the backupset name corresponds to a SharePoint Online instance, False otherwise.

        Example:
            >>> backupset = SharepointBackupset(...)
            >>> if backupset.is_sharepoint_online_instance:
            ...     print("This is a SharePoint Online backupset.")
            ... else:
            ...     print("This is not a SharePoint Online backupset.")

        #ai-gen-doc
        """
        return self.backupset_name == "sharepoint online"

    @property
    def azure_storage_details(self) -> Optional[Dict[str, Any]]:
        """Get the Azure storage account details associated with this SharePoint backupset.

        Returns:
            Optional[Dict[str, Any]]: Dictionary containing Azure storage account information if available,
            otherwise None.

        Example:
            >>> backupset = SharepointBackupset(...)
            >>> azure_details = backupset.azure_storage_details  # Use dot notation for property access
            >>> if azure_details:
            ...     print(f"Azure Storage Account: {azure_details.get('accountName')}")
            ... else:
            ...     print("No Azure storage account details found for this backupset.")

        #ai-gen-doc
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
    def azure_storage_details(self, azure_storage_account_information: Dict[str, Any]) -> None:
        """Update Azure storage account details in the SharePoint backupset properties.

        Args:
            azure_storage_account_information: Dictionary containing Azure account information.
                Example format:
                    {
                        "serviceType": 52,
                        "userAccount": {
                            "password": azure_secret,
                            "userName": azure_username
                        }
                    }

        Example:
            >>> azure_info = {
            ...     "serviceType": 52,
            ...     "userAccount": {
            ...         "password": "my_azure_secret",
            ...         "userName": "my_azure_username"
            ...     }
            ... }
            >>> backupset = SharepointBackupset(...)
            >>> backupset.azure_storage_details = azure_info  # Use assignment for property setter
            >>> # Azure storage details are now updated in the backupset properties

        #ai-gen-doc
        """
        backupset_properties = self.properties
        backupset_properties["sharepointBackupSet"]["spOffice365BackupSetProp"]["serviceAccounts"]["accounts"].append(
            azure_storage_account_information)
        backupset_properties["commonBackupSet"]["isDefaultBackupSet"] = False
        backupset_properties["sharepointBackupSet"]["spOffice365BackupSetProp"]["additionalCredentials"] = {}
        backupset_properties["backupSetEntity"]["flags"] = {}
        self.update_properties(backupset_properties)
