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

"""
File for operating on a MYSQL Instance.

MYSQLInstance is the only class defined in this file.

MYSQLInstance: Derived class from Instance Base class, representing an
                MYSQL instance, and to perform operations on that instance

MYSQLInstance:
==============

    _get_instance_properties()      -- method to get the properties of the instance

    _restore_json()                 -- returns the apppropriate JSON request to pass for
    Restore In-Place

    restore_in_place()              -- Restores the mysql data/log files specified in the
    input paths list to the same location

    _restore_browse_option_json()   -- setter for  browse option  property in restore

    _restore_common_options_json()  -- setter for common options property in restore

    _restore_destination_json()     -- setter for destination options property in restore

    _restore_fileoption_json()      -- setter for file option property in restore

    _restore_admin_option_json()    -- setter for admin option property in restore

    _restore_mysql_option_json()    -- setter for MySQL restore option property in restore


MYSQLInstance instance Attributes:
==================================

    **port**                            -- Returns the MySQL Server Port number

    **mysql_username**                  -- Returns the MySQL Server username

    **nt_username**                     -- Returns the MySQL Server nt username

    **config_file**                     -- Returns the MySQL Server Config File location

    **binary_directory**                -- Returns the MySQL Server Binary File location

    **version**                         -- Returns the MySQL Server version number

    **log_data_directory**              -- Returns the MySQL Server log data directory

    **log_backup_sp_details**           -- Returns the MySQL Server Log backup SP details

    **command_line_sp_details**         -- Returns the MySQL Server commandline SP details

    **autodiscovery_enabled**           -- Returns the MySQL Server auto discovery enabled flag

    **xtrabackup_bin_path**             -- Returns the MySQL Server xtrabackup bin path

    **is_xtrabackup_enabled**           -- Returns the MySQL Server xtrabackup enabled flag

    **proxy_options**                   -- Returns the MySQL Server proxy options


"""

from __future__ import unicode_literals
from ..instance import Instance
from ..exception import SDKException


class MYSQLInstance(Instance):
    """
    Class to represent a standalone MYSQL Instance
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialise the Subclient object.

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance

                    default: None

            Returns:
                object - instance of the MYSQLInstance class

        """
        self._browse_restore_json = None
        self._commonoption_restore_json = None
        self._destination_restore_json = None
        self._fileoption_restore_json = None
        self._instance = None
        self.admin_option_json = None
        self.mysql_restore_json = None
        super(MYSQLInstance, self).__init__(agent_object, instance_name, instance_id)

    @property
    def port(self):
        """Returns the MySQL Server Port number.

        Returns:
            (str)   --  MySql server port number

        """
        return self._properties.get('mySqlInstance', {}).get('port', None)

    @property
    def mysql_username(self):
        """Returns the MySQL Server username.

        Returns:
            (str)   --  MySql server SA username

        """
        return self._properties.get('mySqlInstance', {}).get('SAUser', {}).get('userName', None)

    @property
    def nt_username(self):
        """Returns the MySQL Server nt username.

        Returns:
            (str)   --  MySql server NT username

        """
        return self._properties.get('mySqlInstance', {}).get('NTUser', {}).get('userName', None)

    @property
    def config_file(self):
        """Returns the MySQL Server Config File location.

        Returns:
            (str)   --  MySql server config file location

        """
        return self._properties.get('mySqlInstance', {}).get('ConfigFile', None)

    @property
    def binary_directory(self):
        """Returns the MySQL Server Binary File location.

        Returns:
            (str)   --  MySql server binary directory

        """
        return self._properties.get('mySqlInstance', {}).get('BinaryDirectory', None)

    @property
    def version(self):
        """Returns the MySQL Server version number.

        Returns:
            (str)   --  MySql server version

        """
        return self._properties.get('mySqlInstance', {}).get('version', None)

    @property
    def log_data_directory(self):
        """Returns the MySQL Server log data directory.

        Returns:
            (str)   --  MySql server log directory path

        """
        return self._properties.get('mySqlInstance', {}).get('LogDataDirectory', None)

    @property
    def log_backup_sp_details(self):
        """Returns the MySQL Server Log backup SP details

        Returns:
            (dict)  --  MySql server log backup storage policy information

        """
        log_storage_policy_name = self._properties.get('mySqlInstance', {}).get(
            'logStoragePolicy', {}).get('storagePolicyName', None)
        log_storage_policy_id = self._properties.get('mySqlInstance', {}).get(
            'logStoragePolicy', {}).get('storagePolicyId', None)

        log_sp = {"storagePolicyName": log_storage_policy_name,
                  "storagePolicyId": log_storage_policy_id}
        return log_sp

    @property
    def command_line_sp_details(self):
        """Returns the MySQL Server commandline SP details.

        Returns:
            (dict)  --  MySql server commnadline storage policy information

        """
        cmd_storage_policy_name = self._properties.get('mySqlInstance', {}).get(
            'mysqlStorageDevice', {}).get('commandLineStoragePolicy', {}).get(
                'storagePolicyName', None)
        cmd_storage_policy_id = self._properties.get('mySqlInstance', {}).get(
            'mysqlStorageDevice', {}).get('commandLineStoragePolicy', {}).get(
                'storagePolicyId', None)

        command_sp = {"storagePolicyName": cmd_storage_policy_name,
                      "storagePolicyId": cmd_storage_policy_id}
        return command_sp

    @property
    def autodiscovery_enabled(self):
        """Returns the MySQL Server auto discovery enabled flag

        Returns:
            (bool)  --  True if auto discovery enabled
                        False if auto discovery not enabled

        """
        return self._properties.get('mySqlInstance', {}).get('EnableAutoDiscovery', False)

    @property
    def xtrabackup_bin_path(self):
        """Returns the MySQL Server xtrabackup bin path

        Returns:
            (str)   --  MySql server xtrabackup binary path

        """
        return self._properties.get(
            'mySqlInstance', {}).get(
                'xtraBackupSettings', {}).get('xtraBackupBinPath', "")

    @property
    def is_xtrabackup_enabled(self):
        """Returns the MySQL Server xtrabackup enabled flag

        Returns:
            (bool)  --  True if xtrabackup is enabled
                        False if xtrabackup is not enabled

        """
        return self._properties.get(
            'mySqlInstance', {}).get(
                'xtraBackupSettings', {}).get('enableXtraBackup', False)

    @property
    def proxy_options(self):
        """Returns the MySQL Server proxy options

        Returns:
            (dict)  --  MySql server proxy information

        """
        proxy_settings = self._properties.get('mySqlInstance', {}).get('proxySettings', {})
        proxy_opt = {
            "isUseSSL": proxy_settings.get('isUseSSL', False),
            "isProxyEnabled": proxy_settings.get('isProxyEnabled', False),
            "runBackupOnProxy": proxy_settings.get('runBackupOnProxy', False),
            "instanceId": proxy_settings.get('proxyInstance', {}).get('instanceId', None),
            "instanceName": proxy_settings.get('proxyInstance', {}).get('instanceName', None),
            "clientId": proxy_settings.get('proxyInstance', {}).get('clientId', None),
            "clientName": proxy_settings.get('proxyInstance', {}).get('clientName', None)}
        return proxy_opt

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(MYSQLInstance, self)._get_instance_properties()
        self._instance = {
            "type": 0,
            "clientName": self._agent_object._client_object.client_name,
            "clientSidePackage": True,
            "subclientName": "",
            "backupsetName": "defaultDummyBackupSet",
            "instanceName": self.instance_name,
            "appName": self._agent_object.agent_name,
            "consumeLicense": True
        }

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (list)  --  list of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API

        """
        rest_json = super(MYSQLInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        if restore_option["from_time"] is None:
            restore_option["from_time"] = {}

        if restore_option["to_time"] is None:
            restore_option["to_time"] = {}

        self._restore_admin_option_json(restore_option)
        self._restore_mysql_option_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "mySqlRstOption"] = self.mysql_restore_json
        rest_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"] = self.admin_option_json
        return rest_json

    def restore_in_place(
            self,
            path=None,
            staging=None,
            dest_client_name=None,
            dest_instance_name=None,
            data_restore=True,
            log_restore=False,
            overwrite=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            media_agent=None,
            table_level_restore=False,
            clone_env=False,
            clone_options=None,
            redirect_enabled=False,
            redirect_path=None):
        """Restores the mysql data/log files specified in the input paths list to the same location.

            Args:
                path                    (list)  --  list of database/databases to be restored

                    default: None

                staging                 (str)   --  staging location for mysql logs during restores

                    default: None

                dest_client_name        (str)   --  destination client name where files are to be
                restored

                    default: None

                dest_instance_name      (str)   --  destination mysql instance name of destination
                client

                    default: None

                data_restore            (bool)  --  for data only/data+log restore

                    default: True

                log_restore             (bool)  --  for log only/data+log restore

                    default: False

                overwrite               (bool)  --  unconditional overwrite files during restore

                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy

                    default: None

                from_time               (str)   --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time                 (str)   --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                media_agent             (str)   --  media agent associated

                    default: None

                table_level_restore     (bool)  --  Table level restore flag

                    default: False

                clone_env               (bool)  --  boolean to specify whether the database
                should be cloned or not

                    default: False

                clone_options           (dict)  --  clone restore options passed in a dict

                    default: None

                    Accepted format: {
                                        "stagingLocaion": "/gk_snap",
                                        "forceCleanup": True,
                                        "port": "5595",
                                        "libDirectory": "",
                                        "isInstanceSelected": True,
                                        "reservationPeriodS": 3600,
                                        "user": "",
                                        "binaryDirectory": "/usr/bin"

                                     }

                redirect_enabled         (bool)  --  boolean to specify if redirect restore is
                enabled

                    default: False

                redirect_path           (str)   --  Path specified in advanced restore options
                in order to perform redirect restore

                    default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        if not (isinstance(path, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        if path == []:
            raise SDKException('Instance', '104')

        if dest_client_name is None:
            dest_client_name = self._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = self.instance_name

        request_json = self._restore_json(
            paths=path,
            staging=staging,
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            data_restore=data_restore,
            log_restore=log_restore,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            media_agent=media_agent,
            table_level_restore=table_level_restore,
            clone_env=clone_env,
            clone_options=clone_options,
            redirect_enabled=redirect_enabled,
            redirect_path=redirect_path)

        return self._process_restore_response(request_json)

    def _restore_browse_option_json(self, value):
        """setter for the Browse options for restore in Json"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')
        super(MYSQLInstance, self)._restore_browse_option_json(value)
        self._browse_restore_json['backupset'] = {
            "clientName": self._agent_object._client_object.client_name,
            "backupsetName": "defaultDummyBackupSet"
        }

    def _restore_common_options_json(self, value):
        """setter for the Common options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._commonoption_restore_json = {
            "restoreToDisk": False,
            "onePassRestore": False,
            "revert": False,
            "syncRestore": False
        }

    def _restore_destination_json(self, value):
        """setter for the MySQL Destination options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = {
            "destinationInstance": {
                "clientName": value.get("dest_client_name", ""),
                "instanceName": value.get("dest_instance_name", ""),
                "appName": "MySQL"
            },
            "destClient": {
                "clientName": value.get("dest_client_name", "")
            }
        }

    def _restore_fileoption_json(self, value):
        """setter for the fileoption restore option in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._fileoption_restore_json = {
            "sourceItem": value.get("paths", [])
        }

    def _restore_admin_option_json(self, value):
        """setter for the admin restore option in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.admin_option_json = {
            "contentIndexingOption": {
                "subClientBasedAnalytics": False
            }
        }

    def _restore_mysql_option_json(self, value):
        """setter for the mysql restore option in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self.mysql_restore_json = {
            "destinationFolder": "",
            "data": value.get("data_restore", True),
            "log": value.get("log_restore", True),
            "recurringRestore": False,
            "temporaryStagingLocation": value.get("staging", ""),
            "dataStagingLocation": "",
            "logRestoreType": 0,
            "tableLevelRestore": value.get("table_level_restore", False),
            "pointofTime": False,
            "instanceRestore": True,
            "isCloneRestore": value.get("clone_env", False),
            "fromTime": value.get("from_time", {}),
            "refTime": value.get("to_time", {}),
            "destinationServer": {
                "name": ""
            }
        }
        if value.get("table_level_restore"):
            self.mysql_restore_json['dropTable'] = True
            self.mysql_restore_json['instanceRestore'] = False

        if value.get("clone_env", False):
            self.mysql_restore_json["cloneOptions"] = value.get("clone_options", "")

        if value.get("redirect_path"):
            self.mysql_restore_json["redirectEnabled"] = True
            self.mysql_restore_json["redirectItems"] = [value.get("redirect_path")]
