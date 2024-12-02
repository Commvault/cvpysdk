# -*- coding: utf-8 -*-
# pylint: disable=R1705, R0205

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
"""
File for Azure AD sublcient related operation

Class:
    AzureAdSubclient:    class to handle Azure Ad subclient instnace and operation
"""

from __future__ import unicode_literals
from ..subclient import Subclient


class AzureAdSubclient(Subclient):
    """
        Class for Azure AD subclient related operation
        overwrite common in place restore function
    """

    def restore_in_place(self, **kwargs):
        """ restore azure AD objects with new index
            Args:
                kwargs    dict    additional dict passed for restore.
                                need pass additional azure AD option in restore_options
                                azureADOption" : {"restoreAllMatching": False,
                                                  "restoreMembership" : True,
                                                  "newUserDefaultPassword": "",
                                                  "items": restore_items}}}
        """
        self._instance_object._restore_association = self._subClientEntity
        return self._instance_object._restore_in_place(**kwargs)
