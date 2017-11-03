#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for operating on a Oracle Subclient

OracleSubclient is the only class defined in this file.

OracleSubclient: Derived class from DatabaseSubclient Base class, representing an Oracle subclient,
                        and to perform operations on that subclient

OracleSubclient:
    __init__()                          -- constructor for the class

    data_sp()                           -- Getters and setters for data storage policy

    is_snapenabled()                    -- Check if intellisnap has been enabled in the subclient

"""
from __future__ import unicode_literals
from .dbsubclient import DatabaseSubclient


# from ..exception import SDKException


class OracleSubclient(DatabaseSubclient):
    """
    OracleSubclient is a class to work on Oracle subclients
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Constructor for the class

        Args:
            backupset_object  (object)  -- instance of the Backupset class
            subclient_name    (str)     -- name of the subclient
            subclient_id      (str)     -- id of the subclient
        """
        super(OracleSubclient, self).__init__(backupset_object, subclient_name, subclient_id)
        self._subclientprop = {}    # variable to hold subclient properties to be changed

    @property
    def data_sp(self):
        """
        Getter for data storage policy

        Returns:
            string - string representing data storage policy
        """
        return self._commonProperties['storageDevice']\
            ['dataBackupStoragePolicy']['storagePolicyName']

    @property
    def is_snapenabled(self):
        """
        Getter to check whether the subclient has snap enabled

        Returns:
            Bool - True if snap is enabled on the subclient. Else False
        """
        return self._commonProperties['snapCopyInfo']['isSnapBackupEnabled']
