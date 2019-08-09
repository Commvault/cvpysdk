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

"""File for operating on a Virtual Server VMInstance Subclient.

VMInstanceSubclient is the only class defined in this file.

VMInstanceSubclient:   Derived class from Subclient Base
                                class,representing a VMInstance Subclien

VMInstanceSubclient:

    __init__(
        backupset_object,
        subclient_name,
        subclient_id)           --  initialize object of vminstance subclient class,
                                    associated with the VirtualServer subclient
"""

from ..subclient import Subclient


class VMInstanceSubclient(Subclient):
    """
    Derived class from Subclient Base class.
    This represents a VMInstance virtual server subclient
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Initialize the Instance object for the given Virtual Server instance.

           Args:
               backupset_object    (object)  --  instance of the Backupset class

               subclient_name   (str)        --  subclient name

               subclient     (int)           --  subclient id

        """
        super(VMInstanceSubclient, self).__init__(backupset_object, subclient_name, subclient_id)
