# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Salesforce Backupset.

SalesforceBackupset is the only class defined in this file.

SalesforceBackuset:     Derived class from CloudAppsBackupset Base class, representing a
                            salesforce backupset, and to perform operations on that backupset

SalesforceBackupset:
     __init__()                      --    Backupset class method overwritten to add salesforce
                                               browse options in default browse options

    _get_backupset_properties()      --    Backupset class method overwritten to add salesforce
                                               backupset properties as well

    _prepare_browse_json()           --    Backupset class method overwritten to add salesforce
                                               browse option

    download_cache_path()            --    Fetches download cache path from backupset

    salesforce_user_name()           --    Fetches salesforce user name from backupset

    is_sync_db_enabled()             --    Determines sync database enabled or not on backupset

    sync_db_type()                   --    Fetches sync database type from backupset

    sync_db_host()                   --    Fetches sync database host name from backupset

    sync_db_instance()               --    Fetches ssync database instance name from backupset

    sync_db_name()                   --    Fetches sync database name from backupset

    sync_db_port()                   --    Fetches sync database port number from backupset

    sync_db_user_name()              --    Fetches sync database user name from backupset

"""

from __future__ import unicode_literals

from ..cabackupset import CloudAppsBackupset


class SalesforceBackupset(CloudAppsBackupset):
    """Derived class from CloudAppsBackupset Base class, representing a
        salesforce backupset, and to perform operations on that backupset.
    """

    def __init__(self, instance_object, backupset_name, backupset_id=None):
        """Initlializes instance of the Backupset class for the Salesforce instance.

            Args:
                instance_object     (object)    --  instance of the Instance class

                backupset_name      (str)       --  name of backupset

                backupset_id        (int)       --  id of backupset

            Returns:
                object - instance of the SalesforceBackupset class

        """
        self._download_cache_path = None
        self._user_name = None
        self._api_token = None
        self._sync_db_enabled = None
        self._sync_db_type = None
        self._sync_db_host = None
        self._sync_db_instance = None
        self._sync_db_name = None
        self._sync_db_port = None
        self._sync_db_user_name = None
        self._sync_db_user_password = None

        super(SalesforceBackupset, self).__init__(instance_object, backupset_name, backupset_id)

        salesforce_browse_options = {
            '_browse_view_name_list': ['TBLVIEW', 'FILEVIEW']
        }

        self._default_browse_options.update(salesforce_browse_options)

    def _get_backupset_properties(self):
        """Gets the properties of this backupset.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(SalesforceBackupset, self)._get_backupset_properties()

        if 'cloudAppsBackupset' in self._properties:
            cloud_apps_backupset = self._properties['cloudAppsBackupset']
            if 'salesforceBackupSet' in cloud_apps_backupset:
                sfbackupset = cloud_apps_backupset['salesforceBackupSet']
                if 'downloadCachePath' in sfbackupset:
                    self._download_cache_path = sfbackupset['downloadCachePath']
                if 'userName' in sfbackupset['userPassword']:
                    self._user_name = sfbackupset['userPassword']['userName']
                if 'syncDatabase' in sfbackupset:
                    self._sync_db_enabled = sfbackupset['syncDatabase']['dbEnabled']
                if self._sync_db_enabled:
                    if 'dbType' in sfbackupset['syncDatabase']:
                        self._sync_db_type = sfbackupset['syncDatabase']['dbType']
                    if 'dbHost' in sfbackupset['syncDatabase']:
                        self._sync_db_host = sfbackupset['syncDatabase']['dbHost']
                    if 'dbInstance' in sfbackupset['syncDatabase']:
                        self._sync_db_instance = sfbackupset['syncDatabase']['dbInstance']
                    if 'dbName' in sfbackupset['syncDatabase']:
                        self._sync_db_name = sfbackupset['syncDatabase']['dbName']
                    if 'dbPort' in sfbackupset['syncDatabase']:
                        self._sync_db_port = sfbackupset['syncDatabase']['dbPort']
                    if 'userName' in sfbackupset['syncDatabase']['dbUserPassword']:
                        self._sync_db_user_name = sfbackupset[
                            'syncDatabase']['dbUserPassword']['userName']
                    if 'dbUserPassword' in sfbackupset['syncDatabase']['dbUserPassword']:
                        self._sync_db_user_password = sfbackupset[
                            'syncDatabase']['dbUserPassword']['password']

    def _prepare_browse_json(self, options):
        """Prepares the JSON object for the browse request.

             Args:
                options     (dict)  --  the browse options dictionary

            Returns:
                dict - A JSON object for the browse response

        """
        request_json = super(SalesforceBackupset, self)._prepare_browse_json(options)
        salesforce_browse_view = {
            'browseViewNameList': options['_browse_view_name_list']
        }
        request_json['advOptions'].update(salesforce_browse_view)
        return request_json

    @property
    def download_cache_path(self):
        """getter for download cache path"""
        return self._download_cache_path

    @property
    def salesforce_user_name(self):
        """getter for salesforce user name"""
        return self._user_name

    @property
    def is_sync_db_enabled(self):
        """lets the user know whether sync db enabled or not"""
        return self._sync_db_enabled

    @property
    def sync_db_type(self):
        """getter for the sync database type"""
        return self._sync_db_type

    @property
    def sync_db_host(self):
        """getter for the sync database hostname"""
        return self._sync_db_host

    @property
    def sync_db_instance(self):
        """getter for the sync database instance name"""
        return self._sync_db_instance

    @property
    def sync_db_name(self):
        """getter for the sync database name"""
        return self._sync_db_name

    @property
    def sync_db_port(self):
        """getter for the sync database port number"""
        return self._sync_db_port

    @property
    def sync_db_user_name(self):
        """getter for the sync database user name"""
        return self._sync_db_user_name
