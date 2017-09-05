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
    _backup_request_json()               --  prepares the json for the backup request

    _get_subclient_properties()          --  gets the subclient  related properties of File System subclient.

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

    def __init__(self):
        """
        __init__: Constructor for the class

        """
        DatabaseSubclient.__init__(self)
        self._data_backup_storage_policy = None
        self._log_backup_storage_policy = None

    @property
    def data_backup_storage_policy(self):
        """
        data_backup_storage_policy: Getter for data storage policy
        :returns: string

        """
        return self._data_backup_storage_policy

    @data_backup_storage_policy.setter
    def data_backup_storage_policy(self, data_sp):
        """
        data_backup_storage_policy: Setter for data storage policy

        :data_sp: Storage Policy to be set for Oracle Data

        """
        pass

    @property
    def log_backup_storage_policy(self):
        """
        log_backup_storage_policy: Getter for log storage policy

        :returns: string

        """
        return self._log_backup_storage_policy

    @log_backup_storage_policy.setter
    def log_backup_storage_policy(self, log_sp):
        """
        log_backup_storage_policy: Setter for log storage policy
        :log_sp: Log storage policy

        """
        pass

    def _backup_request_json(self):
        """
        _backup_request_json: Prepares backup request
        :returns: JSON representation of backup request

        """
        pass

    def _get_subclient_properties(self):
        """
        _get_subclient_properties: Gets the subclient  related properties for an instance
        :returns: TODO

        """
        pass

    def content(self):
        """
        content: Update the content of the subclient
        :returns: TODO

        """
        pass
