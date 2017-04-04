#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a SQL Server Subclient

SQLServerSubclient is the only class defined in this file.

SQLServerSubclient: Derived class from Subclient Base class, representing a sql server subclient,
                        and to perform operations on that subclient

SQLServerSubclient:
    _get_subclient_content_()           --  gets the content of a sql server subclient

    _set_subclient_content_()           --  sets the content of a sql server subclient

    _initialize_subclient_properties()  --  initializes additional properties of this subclient

    content                             --  update the content of the subclient

    log_backup_storage_policy           --  updpates the log backup storage policy for this
                                                subclient

    backup()                            --  run a backup job for the subclient

"""

from ..subclient import Subclient
from ..exception import SDKException


class SQLServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of
                                                     subclient

            Returns:
                list - list of content associated with the subclient
        """
        contents = []

        if 'content' in self._subclient_properties:
            subclient_content = self._subclient_properties['content']
        else:
            subclient_content = []

        database_name = None
        content_list = []

        if 'mssqlFFGDBName' in self._subclient_properties['mssqlSubClientProp']:
            database_name = str(self._subclient_properties['mssqlSubClientProp']['mssqlFFGDBName'])

        for content in subclient_content:
            if 'mssqlDbContent' in content:
                content_list.append(str(content["mssqlDbContent"]["databaseName"]))
            elif 'mssqlFGContent' in content:
                self._is_file_group_subclient = True
                content_list.append(str(content['mssqlFGContent']['databaseName']))

        if self._is_file_group_subclient:
            contents.append(database_name)
            contents.append(content_list)
        else:
            contents = content_list

        return contents

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add a new File System Subclient
            with the content passed in subclient content.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        if self._is_file_group_subclient:
            for file_group in subclient_content[1]:
                sql_server_dict = {
                    "mssqlFGContent": {
                        "databaseName": file_group
                    }
                }
                content.append(sql_server_dict)
        else:
            for database_name in subclient_content:
                sql_server_dict = {
                    "mssqlDbContent": {
                        "databaseName": database_name
                    }
                }
                content.append(sql_server_dict)

        return content

    def _initialize_subclient_properties(self):
        """Initializes properties of this subclient"""
        self._is_file_group_subclient = False

        super(SQLServerSubclient, self)._initialize_subclient_properties()

        self._log_backup_storage_policy = None

        storage_device = self._subclient_properties['commonProperties']['storageDevice']

        if 'logBackupStoragePolicy' in storage_device:
            self._log_backup_storage_policy = str(
                storage_device['logBackupStoragePolicy']['storagePolicyName']
            )

    @property
    def content(self):
        """Treats the subclient content as a property of the Subclient class."""
        return self._content

    @content.setter
    def content(self, value):
        """Sets the content of the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if self._is_file_group_subclient:
            raise SDKException(
                'Subclient',
                '102',
                ('Updating File/File Group Content is not allowed. '
                 'Please use Commcell Console to update content.')
            )

        if isinstance(value, list) and value != []:
            output = self._update(self.description, value, self.is_backup_enabled)

            if output[0]:
                return
            else:
                o_str = 'Failed to update the content of the subclient\nError: "{0}"'
                raise SDKException('Subclient', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    @property
    def browse(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'browse'
        ))

    @property
    def browse_in_time(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'browse_in_time'
        ))

    @property
    def find(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'find'
        ))

    @property
    def restore_in_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'restore_in_place'
        ))

    @property
    def restore_out_of_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'restore_out_of_place'
        ))

    @property
    def log_backup_storage_policy(self):
        """Treats the subclient description as a property of the Subclient class."""
        return self._log_backup_storage_policy

    @log_backup_storage_policy.setter
    def log_backup_storage_policy(self, value):
        """Sets the log backup storage policy of subclient as the value provided as input.

            Args:
                value   (str)   -- Log backup Storage policy name to be assigned to subclient

            Raises:
                SDKException:
                    if failed to update log backup storage policy name

                    if log backup storage policy name is not in string format
        """
        if isinstance(value, str):
            output = self._update(
                self.description,
                self.content,
                storage_policy=self._storage_policy,
                log_backup_storage_policy=value
            )

            if output[0]:
                return
            else:
                o_str = ('Failed to update the log backup storage policy of the Subclient'
                         '\nError: "{0}"')
                raise SDKException('Subclient', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient log backup storage policy should be a string value'
            )

    def backup(
            self,
            backup_level="Differential"):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level    (str)   --  level of backup the user wish to run
                        Full / Transaction_Log / Differential
                    default: Differential

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'transaction_log', 'differential']:
            raise SDKException('Subclient', '103')

        return self._process_backup_request(backup_level)
