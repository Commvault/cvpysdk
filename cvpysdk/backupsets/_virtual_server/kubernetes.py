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
from cvpysdk.backupsets.vsbackupset import VSBackupset
from cvpysdk.exception import SDKException
from ...subclients.virtualserver.kubernetes import ApplicationGroups

class KubernetesBackupset(VSBackupset):

    def __init__(self, instance_object, backupset_name, backupset_id=None):
        """Initialise the backupset object."""
        self._blr_pair_details = None
        super().__init__(instance_object, backupset_name, backupset_id)
        self._application_groups = None

    def refresh(self):
        """Refresh the properties of the Backupset."""
        super().refresh()
        self._application_groups = None


    @property
    def application_groups(self):
        """"""
        if self._application_groups is None:
            self._application_groups = ApplicationGroups(self)
        return self._application_groups
