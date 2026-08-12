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

"""File for operating on a Virtual Server VMware Cloud Foundation Automation Subclient.

VMwareCloudFoundationAutomationVirtualServerSubclient is the only class defined in this file.

VMwareCloudFoundationAutomationVirtualServerSubclient:   Derived class from VirtualServerSubclient Base
                                class, representing a VCF Subclient,
                                and to perform operations on that Subclient
"""

from ..vssubclient import VirtualServerSubclient


class VMwareCloudFoundationAutomationVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a VCF virtual server subclient,
       and can perform restore operations on that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given VCF virtual server subclient."""
        super(VMwareCloudFoundationAutomationVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = [".vmdk"]

        self._disk_option = {
            'Original': 0,
            'Thick Lazy Zero': 1,
            'Thin': 2,
            'Thick Eager Zero': 3
        }

        self._transport_mode = {
            'Auto': 0,
            'SAN': 1,
            'Hot Add': 2,
            'NBD': 5,
            'NBD SSL': 4
        }
