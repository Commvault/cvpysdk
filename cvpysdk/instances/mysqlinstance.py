# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for operating on a MYSQL Instance.

MYSQLInstance is the only class defined in this file.

MYSQLInstance: Derived class from Instance Base class, representing an
                            MYSQL instance, and to perform operations on that instance

MYSQLInstance:

    port                            -- Setter for MySql Server Port number

    mysql_username                  -- Setter for SAUser username

    nt_username                     -- Setter for NTUsere username

    config_file                     -- Setter for MySql Server config file location

    binary_directory                -- Setter for MySql Server binary directory location

    version                         -- Setter for MySql Server version

    log_data_directory               -- Setter for MySql Server LogData directory location

    log_backup_sp_details           -- Setter for log backup storage policy name and id

    command_line_sp_details         -- Setter for command line storage policy name and id

    autodiscovery_enabled           -- Setter for Enable Auto Discovery Feature

    proxy_options                   -- Setter for proxy options at MySQL Instance level

    _get_instance_properties()      -- method to get the properties of the instance

    _restore_json()                 -- returns the apppropriate JSON request to pass for
                                            Restore In-Place

    restore_in_place()              -- Gets the restore json and pass the json for restore process

    _restore_browse_option_json()   -- setter for  browse option  property in restore

    _restore_common_options_json()  -- setter for common options property in restore

    _restore_destination_json()     -- setter for destination options property in restore

    _restore_fileoption_json()      -- setter for file option property in restore

    _restore_admin_option_json()    -- setter for admin option property in restore

    _restore_mysql_option_json()    -- setter for MySQL restore option property in restore


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
        """Get the MySQL Server Port number from the Instance Properties.
        """
        return self._properties['mySqlInstance']['port']

    @property
    def mysql_username(self):
        """Get the MySQL Server Port number from the Instance Properties.
        """
        return self._properties['mySqlInstance']['SAUser']['userName']

    @property
    def nt_username(self):
        """Get the MySQL Server Port number from the Instance Properties.
        """
        return self._properties['mySqlInstance']['NTUser']['userName']

    @property
    def config_file(self):
        """Get the MySQL Server Config File location from the Instance Properties.
        """
        return self._properties['mySqlInstance']['ConfigFile']

    @property
    def binary_directory(self):
        """Get the MySQL Server Binary File location from the Instance Properties.

        """
        return self._properties['mySqlInstance']['BinaryDirectory']

    @property
    def version(self):
        """Get the MySQL Server version number from the Instance Properties.

        """
        return self._properties['mySqlInstance']['version']

    @property
    def log_data_directory(self):
        """Get the MySQL Server version number from the Instance Properties.

        """
        return self._properties['mySqlInstance']['LogDataDirectory']

    @property
    def log_backup_sp_details(self):
        """Get the MySQL Server version number from the Instance Properties.

        """
        log_storage_policy_name = self._properties[
            'mySqlInstance']['logStoragePolicy']['storagePolicyName']
        log_storage_policy_id = self._properties['mySqlInstance']['logStoragePolicy'][
            'storagePolicyId']

        log_sp = {"storagePolicyName": log_storage_policy_name,
                  "storagePolicyId": log_storage_policy_id}
        return log_sp

    @property
    def command_line_sp_details(self):
        """Get the MySQL Server version number from the Instance Properties.

        """
        cmd_storage_policy_name = self._properties['mySqlInstance'][
            'mysqlStorageDevice']['commandLineStoragePolicy']['storagePolicyName']
        cmd_storage_policy_id = self._properties['mySqlInstance'][
            'mysqlStorageDevice']['commandLineStoragePolicy']['storagePolicyId']

        command_sp = {"storagePolicyName": cmd_storage_policy_name,
                      "storagePolicyId": cmd_storage_policy_id}
        return command_sp

    @property
    def autodiscovery_enabled(self):
        """Get the MySQL Server version number from the Instance Properties.

        """
        return self._properties['mySqlInstance']['EnableAutoDiscovery']

    @property
    def proxy_options(self):
        """Get the MySQL Server version number from the Instance Properties.

        """
        is_use_ssl = self._properties['mySqlInstance']['proxySettings']['isUseSSL']
        is_proxy_enabled = self._properties['mySqlInstance']['proxySettings']['isProxyEnabled']
        run_backup_on_proxy = self._properties['mySqlInstance']['proxySettings']['runBackupOnProxy']
        proxy_instance_id = self._properties['mySqlInstance']['proxySettings']['proxyInstance'][
            'instanceId']
        proxy_opt = {
            "isUseSSL": is_use_ssl,
            "isProxyEnabled": is_proxy_enabled,
            "runBackupOnProxy": run_backup_on_proxy,
            "instanceId": proxy_instance_id}
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
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["mySqlRstOption"] = self.mysql_restore_json
        rest_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"] = self.admin_option_json
        return rest_json

    def restore_in_place(
            self,
            path,
            staging,
            dest_client_name,
            dest_instance_name,
            data_restore,
            log_restore,
            overwrite=True,
            copy_precedence=None,
            from_time=None,
            to_time=None):
        """Restores the mysql data/log files specified in the input paths list to the same location.

            Args:
                path                    (list)  --  list of database/databases to be restored

                staging                 (str)   --  staging location for mysql logs during restores

                dest_client_name        (str)   --  destination client name where files are to be
                                                        restored

                dest_instance_name      (str)   --  destination mysql instance name of destination
                                                        client

                data_restore            (bool)  --  for data only/data+log restore

                log_restore             (bool)  --  for log only/data+log restore

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
            raise SDKException('Subclient', '101')

        if path == []:
            raise SDKException('Subclient', '104')

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
            to_time=to_time)

        return self._process_restore_response(request_json)

    def _restore_browse_option_json(self, value):
        """setter for the Browse options for restore in Json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._browse_restore_json = {
            "listMedia": False,
            "useExactIndex": False,
            "noImage": False,
            "commCellId": 2,
            "mediaOption": {
                "mediaAgent": {},
                "library": {},
                "copyPrecedence": {
                    "copyPrecedenceApplicable": False
                },
                "drivePool": {}
            },
            "backupset": {
                "clientName": self._agent_object._client_object.client_name,
                "backupsetName": "defaultDummyBackupSet"
            },
            "timeRange": {}
        }

    def _restore_common_options_json(self, value):
        """setter for the Common options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "restoreToDisk": False,
            "onePassRestore": False,
            "revert": False,
            "syncRestore": False
        }

    def _restore_destination_json(self, value):
        """setter for the MySQL Destination options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

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
            raise SDKException('Subclient', '101')

        self._fileoption_restore_json = {
            "sourceItem": value.get("paths", [])
        }

    def _restore_admin_option_json(self, value):
        """setter for the admin restore option in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self.admin_option_json = {
            "contentIndexingOption": {
                "subClientBasedAnalytics": False
            }
        }

    def _restore_mysql_option_json(self, value):
        """setter for the mysql restore option in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self.mysql_restore_json = {
            "destinationFolder": "",
            "data": value.get("data_restore", True),
            "log": value.get("log_restore", True),
            "recurringRestore": False,
            "temporaryStagingLocation": value.get("staging", ""),
            "dataStagingLocation": "",
            "logRestoreType": 0,
            "tableLevelRestore": False,
            "pointofTime": False,
            "instanceRestore": True,
            "isCloneRestore": False,
            "fromTime": value.get("from_time", {}),
            "refTime": value.get("to_time", {}),
            "destinationServer": {
                "name": ""
            }
        }
