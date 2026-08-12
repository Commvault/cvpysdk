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
"""File for operating on an AD agent Backupset.

adbackupset is the only class defined in this file.

Class:

    ADBackupset:  Derived class from Backuset Base class, representing a
                            AD agent backupset, and to perform operations on that backupset

    AdBackupset:

        check_subclient()   --  Method to check existing subclient. if not, create new one
Usage
=====


Limitation:
 * current , update subclient content failed. this is limitation in sp12.will tyr in sp13

"""

from __future__ import unicode_literals

from ..backupset import Backupset
from ..exception import SDKException
from typing import Any, Optional, List


class ADBackupset(Backupset):
    """
    AD agent backupset class for managing Active Directory backupsets.

    This class provides specialized functionality for handling backupsets
    related to Active Directory agents. It includes methods to verify and
    manage subclients within a backupset, ensuring that subclient configurations
    such as name, storage policy, and content are properly set up or updated.
    The class also supports deletion of existing subclients as needed.

    Key Features:
        - Verification and management of subclients within an AD backupset
        - Configuration of subclient properties including name, storage policy, and content
        - Support for deletion of existing subclients during setup
        - Inherits core backupset management capabilities

    #ai-gen-doc
    """

    def check_subclient(self,
                        backupset_ins: Any,
                        subclientname: str,
                        storagepolicy: Optional[str] = None,
                        subclientcontent: Optional[List[str]] = None,
                        deleteexist: bool = False) -> Any:
        """Check if the specified subclient exists, and create a new one if not found.

        This method verifies the existence of a subclient within the provided backupset instance.
        If the subclient does not exist, it creates a new subclient with the specified storage policy
        and content. Optionally, it can delete the existing subclient if requested.

        Args:
            backupset_ins: The backupset instance containing subclients.
            subclientname: Name of the subclient to check or create.
            storagepolicy: Optional name of the storage policy to assign to the new subclient.
            subclientcontent: Optional list of content paths for the subclient. Each element should be a path string.
            deleteexist: If True, deletes the existing subclient before creating a new one.

        Returns:
            The Subclient instance corresponding to the specified subclient name.

        Example:
            >>> backupset = Backupset(...)
            >>> subclient = ad_backupset.check_subclient(
            ...     backupset_ins=backupset,
            ...     subclientname="AD_Subclient",
            ...     storagepolicy="DefaultPolicy",
            ...     subclientcontent=["/AD/Users", "/AD/Groups"],
            ...     deleteexist=True
            ... )
            >>> print(f"Subclient created: {subclient}")

        #ai-gen-doc
        """
        # add detail for the parameters
        subclients = backupset_ins.subclients
        if subclients.has_subclient(subclientname):
            subclient_ins = subclients.get(subclientname)
            if deleteexist:
                backupset_ins.delete(subclientname)
        else:
            if storagepolicy is None:
                raise SDKException("Subclient", 102, "No storage policy is defined")
            else:
                subclients.add(subclientname, storagepolicy)
                sc_ins = backupset_ins.subclients.get(subclientname)
                content = []
                for entry in subclientcontent:
                    entrydict = {"path" : ",{0}".format(entry)}
                    content.append(entrydict)
                sc_ins._set_subclient_properties("content", content)
                subclient_ins = sc_ins
        return subclient_ins
