# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

"""File for operating on a SQL Server Subclient

SQLServerSubclient is the only class defined in this file.

SQLServerSubclient: Derived class from Subclient Base class, representing a sql server subclient,
and to perform operations on that subclient

SQLServerSubclient:

    _get_subclient_properties()         --  gets the subclient related properties of SQL subclient.

    _get_subclient_properties_json()    --  gets all the subclient related properties of SQL subclient.

    content()                           --  sets the content of the subclient.

    log_backup_storage_policy()         --  updates the log backup storage policy for this subclient.

    backup()                            --  run a backup job for the subclient.

    update_content()                    --  add, delete, overwrite the sql server subclient contents.

    blocklevel_backup_option            --  setter for block level backup option on SQL subclient

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
        super(DatabaseSubclient, self)._get_subclient_properties()

        self._mssql_subclient_prop = self._subclient_properties.get('mssqlSubClientProp', {})
        self._content = self._subclient_properties.get('content', {})
        self._is_file_group_subclient = self._mssql_subclient_prop.get('sqlSubclientType', False) == 2

    def _get_subclient_properties_json(self):
        """Get the all subclient related properties of this subclient.

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
            backup_level="Differential",
            data_options=[],
            schedule_pattern=None
    ):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level    (str)   --  level of backup the user wish to run
                        Full / Transaction_Log / Differential
                    default: Differential

                data_options    (list)  --  List of options to be enabled on backup

                The accepted string values are:
                    * start_log_backup_after_successfull_backup
                    * copy_only
                    * allow_diff_backup_on_read_only
                    * partial_sql_backup
                    * tail_log_backup
                    * use_sql_compression
                    * checksum
                    * continue_after_error

                    default: []

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

            Returns:
                object - instance of the Job class for this backup job if its an immediate Job

                         instance of the Schedule class for the backup job if its a scheduled Job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        advanced_options = {}
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'transaction_log', 'differential']:
            raise SDKException('Subclient', '103')

        if data_options or schedule_pattern:
            if data_options:
                invalid_full_data_opts = ['tail_log_backup', 'allow_diff_backup_on_read_only']
                invalid_transaction_log_data_opts = [
                    'start_log_backup_after_successfull_backup',
                    'allow_diff_backup_on_read_only',
                    'copy_only']
                invalid_differential_data_opts = ['tail_log_backup', 'copy_only']

                if 'checksum' in data_options and 'use_sql_compression' in data_options:
                    raise ValueError("checksum or use_sql_compression can be enabled , but not both")
                if backup_level == 'full' and any(option in data_options for option in invalid_full_data_opts):
                    raise ValueError("{0} are not applicable for full backup".format(invalid_full_data_opts))
                elif backup_level == 'transaction_log' and any(option in data_options
                                                               for option in invalid_transaction_log_data_opts):
                    raise ValueError("{0} are not applicable for Transaction log backup".format(
                        invalid_transaction_log_data_opts))
                elif backup_level == 'differential' and any(option in data_options
                                                            for option in invalid_differential_data_opts):
                    raise ValueError("{0} are not applicable for full backup".format(invalid_differential_data_opts))

                advanced_options["dataOpt"] = {
                    "enableIndexCheckPointing": False,
                    "verifySynthFull": True,
                    "startLogBackupAfterSuccessfullBackup":
                        "start_log_backup_after_successfull_backup" in data_options,
                    "tailLogBackup": "tail_log_backup" in data_options,
                    "partailSqlBkp": "partial_sql_backup" in data_options,
                    "useSqlCompression": "use_sql_compression" in data_options,
                    "useCatalogServer": False,
                    "enforceTransactionLogUsage": False,
                    "copyOnly": "copy_only" in data_options,
                    "skipConsistencyCheck": False,
                    "skipCatalogPhaseForSnapBackup": True,
                    "runIntegrityCheck": False,
                    "checksum": "checksum" in data_options,
                    "continueaftererror": "continue_after_error" in data_options,
                    "allowDiffBackupOnReadOnly": "allow_diff_backup_on_read_only" in data_options
                }

            request_json = self._backup_json(
                backup_level,
                False,
                "BEFORE_SYNTH",
                advanced_options,
                schedule_pattern
            )

            backup_service = self._services['CREATE_TASK']

            flag, response = self._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

            return self._process_backup_response(flag, response)

        return super(SQLServerSubclient, self).backup(
            backup_level=backup_level,
        )

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

    @property
    def blocklevel_backup_option(self):
        """returns True if block level backup is enabled else returns false

            Returns:
                bool - boolean value based on blocklevel enable status

                    True if block level is enabled
                    False if block level is not enabled

        """
        return bool(
            self._subclient_properties.get(
                'mssqlSubClientProp', {}).get('useBlockLevelBackupWithOptimizedRecovery', False))

    @blocklevel_backup_option.setter
    def blocklevel_backup_option(self, value):
        """Enables or disables block level option on SQL subclient

            Args:
                value (bool)  --  Boolean value whether to set block level option on or off

        """

        if self._is_file_group_subclient:
            err_message = 'Updating properties is not supported for FILE/ FILE GROUP subclient.'
            'Please use Commcell Console to update the subclient.'
            raise SDKException('Subclient', '102', err_message)

        self._set_subclient_properties("_mssql_subclient_prop['useBlockLevelBackupWithOptimizedRecovery']", value)
