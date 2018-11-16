# -*- coding: utf-8 -*-
# ————————————————————————–
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# ————————————————————————–

"""File for operating on a SQL Server Subclient

SQLServerSubclient is the only class defined in this file.

SQLServerSubclient: Derived class from Subclient Base class, representing a sql server subclient,
and to perform operations on that subclient

SQLServerSubclient:
    
    _get_subclient_properties()         --  gets the subclient  related properties of SQL subclient.
    
    _get_subclient_properties_json()    --  gets all the subclient  related properties of SQL subclient.

    content()                           --  sets the content of the subclient.

    log_backup_storage_policy()         --  updates the log backup storage policy for this subclient.

    backup()                            --  run a backup job for the subclient.

    update_content()                    --  add, delete, overwrite the sql server subclient contents.

"""

from __future__ import unicode_literals

from .dbsubclient import DatabaseSubclient
from ..exception import SDKException


class SQLServerSubclient(DatabaseSubclient):
    """Derived class from Subclient Base class, representing a sql server subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of SQL Server subclient.           
           
        """
        super(DatabaseSubclient,self)._get_subclient_properties()

        self._mssql_subclient_prop = self._subclient_properties.get('mssqlSubClientProp', {})
        self._content = self._subclient_properties.get('content', {})
        self._is_file_group_subclient = self._mssql_subclient_prop.get('sqlSubclientType', False) == 2
    
    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.        
           
           Returns:
                dict - all subclient properties put inside a dict
           
        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "mssqlSubClientProp": self._mssql_subclient_prop,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

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
            return []

        database_name = None
        content_list = []

        if 'mssqlFFGDBName' in self._subclient_properties['mssqlSubClientProp']:
            database_name = self._subclient_properties['mssqlSubClientProp']['mssqlFFGDBName']

        for content in subclient_content:
            if 'mssqlDbContent' in content:
                content_list.append(content["mssqlDbContent"]["databaseName"])
            elif 'mssqlFGContent' in content:
                content_list.append(content['mssqlFGContent']['databaseName'])

        if self._is_file_group_subclient:
            contents.append(database_name)
            contents.append(content_list)
        else:
            contents = content_list

        return contents

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add a new sql server Subclient
            with the content passed in subclient content.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        if self._is_file_group_subclient:
            err_message = 'Content addition is not supported for FILE/ FILE GROUP subclient.'
            'Please use Commcell Console to update the content.'
            raise SDKException('Subclient', '102', err_message)
        else:
            for database_name in subclient_content:
                sql_server_dict = {
                    "mssqlDbContent": {
                        "databaseName": database_name
                    }
                }
                content.append(sql_server_dict)

        self._set_subclient_properties("_content", content)
    
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

    @property
    def mssql_subclient_prop(self):
        """ getter for sql server subclient properties """
        return self._mssql_subclient_prop

    @mssql_subclient_prop.setter
    def mssql_subclient_prop(self, value):
        """

            Args:
                value (list)  --  list of the category and properties to update on the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        category, prop = value

        if self._is_file_group_subclient:
            err_message = 'Updating properties is not supported for FILE/ FILE GROUP subclient.'
            'Please use Commcell Console to update the subclient.'
            raise SDKException('Subclient', '102', err_message)

        self._set_subclient_properties(category, prop)

    def update_content(self, subclient_content, action):
        """Updates the sql server subclient contents with supplied content list.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient
                
                action (int)  --   action to perform on subclient
                1: OVERWRITE, 2: ADD, 3: DELETE

            Returns:
                list - list of the appropriate JSON to send to the POST Subclient API
        """
        request_json = self._get_subclient_properties_json()
        content_list = []

        if self._is_file_group_subclient:
            err_message = 'Content modification is not supported for FILE/ FILE GROUP subclient.'
            'Please use Commcell Console to update the content.'
            raise SDKException('Subclient', '102', err_message)
        else:
            for database_name in subclient_content:
                sql_server_dict = {
                    "mssqlDbContent": {
                        "databaseName": database_name
                    }
                }
                content_list.append(sql_server_dict)
        request_json['subClientProperties']['content'] = content_list

        content_op_dict = {
            "contentOperationType": action
        }
        request_json['subClientProperties'].update(content_op_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._SUBCLIENT, request_json
        )

        output = self._process_update_response(flag, response)

        if output[0]:
            return
        else:
            o_str = 'Failed to update content of subclient\nError: "{0}"'
            raise SDKException('Subclient', '102', o_str.format(output[2]))
