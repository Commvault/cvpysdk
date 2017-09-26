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
    
    _get_subclient_properties()          --  gets the subclient  related properties of SQL subclient.
    
    _get_subclient_properties_json()     --  gets all the subclient  related properties of SQL subclient.

    _initialize_subclient_properties()  --  initializes additional properties of this subclient

    content()                           --  update the content of the subclient

    log_backup_storage_policy()         --  updates the log backup storage policy for this
                                                subclient

    backup()                            --  run a backup job for the subclient

"""

from __future__ import unicode_literals

from .dbsubclient import DatabaseSubclient
from ..exception import SDKException


class SQLServerSubclient(DatabaseSubclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient."""

    @property
    def content(self):
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
            database_name = self._subclient_properties['mssqlSubClientProp']['mssqlFFGDBName']

        for content in subclient_content:
            if 'mssqlDbContent' in content:
                content_list.append(content["mssqlDbContent"]["databaseName"])
            elif 'mssqlFGContent' in content:
                self._is_file_group_subclient = True
                content_list.append(content['mssqlFGContent']['databaseName'])

        if self._is_file_group_subclient:
            contents.append(database_name)
            contents.append(content_list)
        else:
            contents = content_list

        return contents

    @content.setter
    def content(self, subclient_content):
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

        self._set_subclient_properties("_content",content)

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.           
           
        """
        super(DatabaseSubclient,self)._get_subclient_properties()
        if 'impersonateUser' in self._subclient_properties:
            self._impersonateUser = self._subclient_properties['impersonateUser']
        if 'fsSubClientProp' in self._subclient_properties:
            self._fsSubClientProp = self._subclient_properties['fsSubClientProp']
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']
    
    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.        
           
           Returns:
                dict - all subclient properties put inside a dict
           
        """
        subclient_json = {
            "subClientProperties":
                {
                    "impersonateUser": self._impersonateUser,
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json
    
    
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

        backup_service = self._commcell_object._services['SUBCLIENT_BACKUP'] % (
            self.subclient_id, backup_level
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service
        )

        return self._process_backup_response(flag, response)
