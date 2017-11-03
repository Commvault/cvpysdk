#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for operating on a Oracle Instance.

OracleInstance is the only class defined in this file.

OracleInstance: Derived class from Instance Base class, representing an
                            oracle instance, and to perform operations on that instance

OracleInstance:

    __init__()              -- Constructor for the class

    oracle_home()           -- Getter for $ORACLE_HOME of this instance

    version()               -- Getter for oracle database version

    is_catalog_enabled()    -- Getter to check if catalog is enabled for backups

    catalog_user()          -- Getter for getting catalog user

    catalog_db()            -- Getter for catalog database name

    archive_log_dest()      -- Getter for archivelog destination

    os_user()               -- Getter for OS user owning oracle software

    cmd_sp()                -- Getter for command line storage policy

    log_sp()                -- Getter for log storage policy

    is_autobackup_on()      -- Getter to check if autobackup is enabled

    db_user()               -- Getter for SYS database user name

    tns_name()              -- Getter for TNS connect string

    dbid()                  -- Getter for getting DBID of database

    delete()                -- Method to delete the instance from the Commserve

"""
from __future__ import unicode_literals

from ..instance import Instance
# from ..client import Client
from ..exception import SDKException


class OracleInstance(Instance):
    """
    Class to represent a standalone Oracle Instance
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Constructor for the class

        Args:
            agent_object    -- instance of the Agent class
            instance_name   -- name of the instance
            instance_id     --  id of the instance

        """
        super(OracleInstance, self).__init__(agent_object, instance_name, instance_id)
        self._instanceprop = {}  # variable to hold instance properties to be changed

    @property
    def oracle_home(self):
        """
        getter for oracle home

        Returns:
            string - string of oracle_home

        """
        return self._properties['oracleInstance']['oracleHome']

    @property
    def is_catalog_enabled(self):
        """
        Getter to check if catalog has been enabled

        Returns:
            Bool - True if catalog is enabled. Else False.

        """
        return self._properties['oracleInstance']['useCatalogConnect']

    @property
    def catalog_user(self):
        """
        Getter for catalog user

        Returns:
            string  - String containing catalog user

        Raises:
            SDKException:
                if not set

                if catalog is not enabled

        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['userName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102', 'Catalog user not set - {}'.format(error_str))

    @property
    def catalog_db(self):
        """
        Getter for catalog database

        Returns:
            string  - String containing catalog database

        Raises:
            SDKException:
                if not set

                if catalog is not enabled

        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102',
                               'Catalog database not set - {}'.format(error_str))

    @property
    def os_user(self):
        """
        Getter for oracle software owner

        Returns:
            string - string of oracle software owner

        """
        return self._properties['oracleInstance']['oracleUser']['userName']

    @property
    def version(self):
        """
        Getter for oracle version

        Returns:
            string - string of oracle instance version

        """
        return self._properties['version']

    @property
    def archive_log_dest(self):
        """
        Getter for the instance's archive log dest

        Returns:
            string - string for archivelog location

        """
        return self._properties['oracleInstance']['archiveLogDest']

    @property
    def cmd_sp(self):
        """
        Getter for Command Line storage policy

        Returns:
            string - string for command line storage policy

        """
        return self._properties['oracleInstance']['oracleStorageDevice']\
            ['commandLineStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self):
        """
        Oracle Instance's Log Storage Poplicy

        Returns:
            string  -- string containing log storage policy

        """
        return self._properties['oracleInstance']['oracleStorageDevice']\
        ['logBackupStoragePolicy']['storagePolicyName']

    @property
    def is_autobackup_on(self):
        """
        Getter to check whether autobackup is set to ON

        Returns:
            Bool - True if autobackup is set to ON. Else False.

        """
        return True if self._properties['oracleInstance']['ctrlFileAutoBackup'] == 1 else False

    @property
    def db_user(self):
        """

        Returns: Oracle database user for the instance

        """
        return self._properties['oracleInstance']['sqlConnect']['userName']

    @property
    def tns_name(self):
        """

        Returns:
            string  -- TNS name of the instance configured

        Raises:
            SDKException:
                if not set

        """
        try:
            return self._properties['oracleInstance']['sqlConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102',
                               'Instance TNS Entry not set - {}'.format(error_str))

    @property
    def dbid(self):
        """

        Returns: DBID of the oracle database

        """
        return self._properties['oracleInstance']['DBID']
