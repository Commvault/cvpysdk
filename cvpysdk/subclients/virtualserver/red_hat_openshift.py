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

"""File for operating on a Virtual Server OpenShift Subclient.

OpenshiftSubclient is the only class defined in this file.

OpenshiftSubclient: Derived class from VirtualServerSubClient  Base class,
                            representing a Openshift Subclient, and
                            to perform operations on that Subclient

OpenshiftSubclient:

    full_vm_restore_in_place()      --  restores the VM specified by the user to
                                            the same location
    full_vm_restore_out_of_place()  --  restores the VM specified in to the specified client,
                                        at the specified destination location

"""

from past.builtins import basestring
from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class OpenshiftSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a OpenShift virtual server subclient,
       and can perform restore operations on only that subclient.

    """
    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """

        super(OpenshiftSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)