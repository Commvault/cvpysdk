# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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
from ...exception import SDKException


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
        self.diskextension = [".vmdk"]

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
