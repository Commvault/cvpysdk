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

"""File for operating on a Virtual Server Vcloud Subclient.

VcloudVirtualServerSubclient is the only class defined in this file.

VcloudVirtualServerSubclient:   Derived class from VirtualServerSubClient Base
                                class,representing a Vcloud Subclient,
                                and to perform operations on that Subclient

VcloudVirtualServerSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of Vcloud subclient class,
                                    associated with the VirtualServer subclient

"""

from ..vssubclient import VirtualServerSubclient


class VcloudVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a Vcloud virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """

        super(VcloudVirtualServerSubclient, self).__init__(
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
