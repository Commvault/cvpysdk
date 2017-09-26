#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Oracle Subclient

OracleSubclient is the only class defined in this file.

OracleSubclient: Derived class from DatabaseSubclient Base class, representing an Oracle subclient,
                        and to perform operations on that subclient

OracleSubclient:

    content()                            --  update the content of the subclient

    log_backup_storage_policy()          --  updpates the log backup storage policy for this
                                                subclient

    backup()                             --  run a backup job for the subclient

"""
from __future__ import unicode_literals
from .dbsubclient import DatabaseSubclient
from ..exception import SDKException


class OracleSubclient(DatabaseSubclient):

    """
    OracleSubclient: Class to work on Oracle subclients
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        __init__: Constructor for the class
        :backupset_object:  instance of the Backupset class
        :subclient_name: name of the subclient
        :subclient_id: id of the subclient

        """
        super(OracleSubclient, self).__init__(backupset_object, subclient_name, subclient_id)

    @property
    def data_sp(self):
        """
        data_sp: Getter for data storage policy
        :returns: string

        """
        return self._commonProperties['storageDevice']['dataBackupStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self):
        """
        data_sp: Getter for log storage policy
        :returns: string

        """
        return self._commonProperties['storageDevice']['logBackupStoragePolicy']['storagePolicyName']

    @property
    def is_snap_enabled(self):
        """
        is_snap_enabled: Getter to check whether the subclient has snap enabled
        :returns: Bool

        """
        return self._commonProperties['snapCopyInfo']['isSnapBackupEnabled']

    def content(self):
        """
        content: Update the content of the subclient
        :returns: TODO

        """
        pass

    def __str__(self):
        """
        __str__: Dunder to represent the class as a string
        :returns: string

        """
        return 'Class for Oracle subclient: {}'.format(self.subclient_name)

    def __repr__(self):
        """
        __repr__: Dunder for representing the class
        :returns: string

        """
        return 'Class for Oracle subclient: {}'.format(self.subclient_name)
