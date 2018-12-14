# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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
