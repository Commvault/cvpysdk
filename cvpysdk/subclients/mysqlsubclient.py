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

"""File for operating on a MYSQL Subclient

MYSQLSubclient is the only class defined in this file.

MYSQLSubclient: Derived class from Subclient Base class, representing a MYSQL subclient,
                        and to perform operations on that subclient

MYSQLSubclient:
    __init__()                          --  constructor for the class

    is_failover_to_production()         --  Sets the isFailOverToProduction flag for the
    subclient as the value provided as input

    _backup_request_json()              --  prepares the json for the backup request

    _get_subclient_properties()         --  Gets the subclient related properties of MYSQL subclient

    _get_subclient_properties_json()    --  get the all subclient related properties of this
    subclient

    content()                           --  Creates the list of content JSON to pass to the API to
    add/update content of a MYSQL Subclient

    backup()                            --  Runs a backup job for the subclient of the level
    specified

    restore_in_place()                  --  Restores the mysql data/log files specified in
    the input paths list to the same location


MYSQLSubclient instance Attributes:
===================================

    **is_blocklevel_backup_enabled**    --  Returns True if block level backup is
    enabled else returns false

    **is_proxy_enabled**                --  Returns True if proxy is enabled in the subclient

    **is_failover_to_production**       --  Returns the isFailOverToProduction flag of the subclient

    **content**                         --  Returns the appropriate content from
    the Subclient relevant to the user

"""

from __future__ import unicode_literals
from ..subclient import Subclient
from ..exception import SDKException


class MYSQLSubclient(Subclient):
    """Derived class from Subclient Base class, representing a MYSQL subclient,
        and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialise the Subclient object.

            Args:
                backupset_object (object)  --  instance of the Backupset class

                subclient_name   (str)     --  name of the subclient

                subclient_id     (str)     --  id of the subclient
                    default: None

            Returns:
                object - instance of the MYSQLSubclient class

        """
        self.mysql_subclient_prop = None
        self.dfs_subclient_prop = None
        self.plan_entity = None
        self.cassandra_props = None
        self.analytics_subclient_prop = None
        super(MYSQLSubclient, self).__init__(backupset_object, subclient_name, subclient_id)

    @property
    def is_blocklevel_backup_enabled(self):
        """returns True if block level backup is enabled else returns false

        Returns:
            (bool) - boolean value based on blocklevel enable status

                    True if block level is enabled
                    False if block level is not enabled

        """
        return bool(self._subclient_properties.get(
            'mySqlSubclientProp', {}).get('isUseBlockLevelBackup', False))

    @property
    def is_proxy_enabled(self):
        """Returns True if proxy is enabled in the subclient

        Returns:
            (bool) - boolean value based on proxy enable status

                    True if proxy is enabled
                    False if proxy is not enabled

        """
        return self._subclient_properties.get(
            'mySqlSubclientProp', {}).get('proxySettings', {}).get(
                'isProxyEnabled', False)

    @property
    def is_failover_to_production(self):
        """Returns the isFailOverToProduction flag of the subclient.

        Returns:

            (bool)  --  True if flag is set
                        False if the flag is not set

        """
        return self._subclient_properties.get(
            'mySqlSubclientProp', {}).get(
                'proxySettings', {}).get('isFailOverToProduction', False)

    @is_failover_to_production.setter
    def is_failover_to_production(self, value):
        """Sets the isFailOverToProduction flag for the subclient as the value provided as input.

        Args:

            value   (bool)  --  Boolean value to set as flag

            Raises:
                SDKException:
                    if failed to set isFailOverToProduction flag

                    if the type of value input is not bool
        """
        if isinstance(value, bool):
            self._set_subclient_properties(
                "_subclient_properties['mySqlSubclientProp']\
                ['proxySettings']['isFailOverToProduction']",
                value)
        else:
            raise SDKException(
                'Subclient', '102', 'Expecting a boolean value here'
            )

    def _backup_request_json(
            self,
            backup_level,
            inc_with_data=False,
            truncate_logs_on_source=False,
            do_not_truncate_logs=False):
        """
        prepares the json for the backup request

            Args:
                backup_level            (list)  --  level of backup the user wish to run

                    Accepted Values:
                        Full / Incremental / Differential

                inc_with_data           (bool)  --  flag to determine if the incremental backup
                includes data or not

                truncate_logs_on_source (bool)  --  flag to determine if the logs to be
                truncated on master client

                    default: False

                do_not_truncate_logs    (bool)  --  flag to determine if the proxy logs
                needs to be truncated or not

                    default: False

            Returns:
                dict - JSON request to pass to the API

        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")

        backup_options = {
            "truncateLogsOnSource":truncate_logs_on_source,
            "sybaseSkipFullafterLogBkp":False,
            "notSynthesizeFullFromPrevBackup":False,
            "incrementalDataWithLogs":inc_with_data,
            "backupLevel":backup_level,
            "incLevel":"NONE",
            "adHocBackup":False,
            "runIncrementalBackup":False,
            "doNotTruncateLog":do_not_truncate_logs,
            "dataOpt":{
                "skipCatalogPhaseForSnapBackup":True,
                "createBackupCopyImmediately":True,
                "useCatalogServer":True,
                "followMountPoints":False,
                "enforceTransactionLogUsage":False,
                "skipConsistencyCheck":False,
                "createNewIndex":False
            },
            "mediaOpt":{

            }
        }
        request_json["taskInfo"]["subTasks"][0]["options"][
            "backupOpts"] = backup_options

        return request_json

    def _get_subclient_properties(self):
        """Gets the subclient related properties of MYSQL subclient"""
        super(MYSQLSubclient, self)._get_subclient_properties()
        if 'mySqlSubclientProp' in self._subclient_properties:
            self.mysql_subclient_prop = self._subclient_properties['mySqlSubclientProp']
        if 'dfsSubclientProp' in self._subclient_properties:
            self.dfs_subclient_prop = self._subclient_properties['dfsSubclientProp']
        if 'planEntity' in self._subclient_properties:
            self.plan_entity = self._subclient_properties['planEntity']
        if 'cassandraProps' in self._subclient_properties:
            self.cassandra_props = self._subclient_properties['cassandraProps']
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']
        if 'analyticsSubclientProp' in self._subclient_properties:
            self.analytics_subclient_prop = self._subclient_properties['analyticsSubclientProp']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "mySqlSubclientProp": self.mysql_subclient_prop,
                    "subClientEntity": self._subClientEntity,
                    "dfsSubclientProp": self.dfs_subclient_prop,
                    "planEntity": self.plan_entity,
                    "cassandraProps": self.cassandra_props,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "analyticsSubclientProp": self.analytics_subclient_prop,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def content(self):
        """Returns the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient

        """
        cont = []

        # Getting the database names from subclient content details
        for path in self._content:
            for key, value in path.items():
                if key == "mySQLContent":
                    cont.append(value["databaseName"])
        return cont

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            MYSQL Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API

        """
        cont = []
        for mysql_cont in subclient_content:
            mysql_dict = {
                "mySQLContent": {
                    "databaseName": mysql_cont
                }
            }
            cont.append(mysql_dict)

        self._set_subclient_properties("_content", cont)


    def backup(
            self,
            backup_level="Differential",
            inc_with_data=False,
            truncate_logs_on_source=False,
            do_not_truncate_logs=False):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential / Synthetic_full

                    default: Differential

                inc_with_data       (bool)  --  flag to determine if the incremental backup
                includes data or not

                truncate_logs_on_source (bool)  --  flag to determine if the logs to be
                truncated on master client

                    default: False

                do_not_truncate_logs    (bool)  --  flag to determine if the proxy logs
                needs to be truncated or not

                    default: False

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success

        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'incremental', 'differential', 'synthetic_full']:
            raise SDKException('Subclient', '103')

        if not (inc_with_data or truncate_logs_on_source or do_not_truncate_logs):
            return super(MYSQLSubclient, self).backup(backup_level)
        request_json = self._backup_request_json(
            backup_level,
            inc_with_data,
            truncate_logs_on_source=truncate_logs_on_source,
            do_not_truncate_logs=do_not_truncate_logs)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CREATE_TASK'], request_json
        )
        return self._process_backup_response(flag, response)

    def restore_in_place(
            self,
            paths=None,
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
                paths               (list)  --  list of database/databases to be restored

                staging             (str)   --  staging location for mysql logs during restores

                dest_client_name    (str)   --  destination client name where files are
                                                        to be restored

                dest_instance_name  (str)   --  destination mysql instance name of
                                                        destination client

                data_restore        (bool)  --  for data only/data+log restore

                log_restore         (bool)  --  for log only/data+log restore

                overwrite           (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence     (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)   --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time             (str)   --  time to retore the contents before
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
        if not (isinstance(paths, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Subclient', '101')

        if paths == []:
            raise SDKException('Subclient', '104')

        instance_object = self._backupset_object._instance_object
        if dest_client_name is None:
            dest_client_name = instance_object._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = instance_object.instance_name
        instance_object._restore_association = self._subClientEntity

        return instance_object.restore_in_place(
            path=paths,
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
            redirect_path=redirect_path
        )
