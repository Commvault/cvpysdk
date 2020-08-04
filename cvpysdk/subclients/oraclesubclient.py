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
File for operating on a Oracle Subclient

OracleSubclient is the only class defined in this file.

OracleSubclient: Derived class from DatabaseSubclient Base class, representing an Oracle subclient,
                        and to perform operations on that subclient

OracleSubclient:
    __init__()                          --  constructor for the class

    _get_subclient_properties()         --  gets the subclient related properties of
                                            Oracle subclient

    _get_subclient_properties_json()    --  returns subclient property json for oracle

    data()                              --  Getter and Setter for enabling data mode in oracle

    selective_online_full()             --  Getter and Setter to enable selective online option

    set_backupcopy_interface()          --  Setter for the backupcopy interface

    data_stream()                       --  Getter and Setter for data stream

    backup()                            --  Performs backup database

    restore()                           --  Performs restore databases
    
    restore_in_place()                  --  Performs restore for oracle logical dump

    backup_archive_log()                --  Getter ans Setter for enaling/disabling
                                            archive log mode

    archive_files_per_bfs()             --  Getter and Setter for archive files per BFS

    data_sp()                           --  Getters and setters for data storage policy

    _get_oracle_restore_json            --  To get restore JSON for an oracle instance

    _oracle_backup_json                 --  Get backup JSON for oracle instance

    is_snapenabled()                    --  Check if intellisnap has been enabled in the subclient

"""
from __future__ import unicode_literals
from .dbsubclient import DatabaseSubclient
from ..exception import SDKException
from ..constants import InstanceBackupType


class OracleSubclient(DatabaseSubclient):
    """
    OracleSubclient is a class to work on Oracle subclients

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Constructor for the class

        Args:
            backupset_object  (object)  -- instance of the Backupset class
            subclient_name    (str)     -- name of the subclient
            subclient_id      (str)     -- id of the subclient
        """
        super(OracleSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self._get_subclient_properties()
        #self._oracle_properties = {}

    def _oracle_backup_json(
            self,
            backup_level="full",
            schedule_pattern=None):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level            (str)   --  level of backup the user wish to run
                                                    Full / Incremental

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

            Returns:
                dict    -- dict containing request JSON

        """
        oracle_options = {
            "oracleOptions": {}
        }
        request_json = self._backup_json(
            backup_level,
            False,
            "BEFORE_SYNTH",
            schedule_pattern=schedule_pattern
        )

        # Add option to run RMAN cumulatives
        oracle_options["oracleOptions"]["cumulative"] = True

        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            oracle_options
        )
        return request_json

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of Oracle subclient.
        """
        if not bool(self._subclient_properties):
            super(OracleSubclient, self)._get_subclient_properties()
        self._oracle_subclient_properties = self._subclient_properties.get("oracleSubclientProp")

    def _get_subclient_properties_json(self):
        """returns subclient property json for oracle
           Returns:
                dict - all subclient properties put inside a dict
        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "commonProperties": self._commonProperties,
                    "oracleSubclientProp": self._oracle_subclient_properties,
                }
        }
        return subclient_json

    def set_prop_for_orcle_subclient(self, storage_policy, snap_engine=None, archivefilebfs=32):
        """Updates the subclient properties.

            Args:

                storage_policy      (str)   --  name of the storage policy to be associated
                with the subclient

                snap_engine         (str)   --  Snap Engine to be set for subclient (optional)

                    default: None

            Raises:
                SDKException:
                    if storage policy argument is not of type string

                    if failed to update subclient

                    if response is empty

                    if response is not success

        """
        if not archivefilebfs and (self.archive_files_per_bfs == '0'):
            self.archive_files_per_bfs = 32
        else:
            self.archive_files_per_bfs = archivefilebfs

        self.data_stream = 2

        self.storage_policy = storage_policy
        if snap_engine:
            self.enable_intelli_snap(snap_engine)

    @property
    def data(self):
        """
        Getter to fetch if data enabled in oracle subclient or not

            Returns:
                bool     --  True if data is enabled on the subclient. Else False

        """
        return self._oracle_subclient_properties.get("data")

    @data.setter
    def data(self, data):
        """
        Enables  data for oracle subclient

            Args:
                data      (bool) --   True if data to be enabled on the subclient. Else False
        """
        self._set_subclient_properties(
            "_oracle_subclient_properties['data']", data)

    @property
    def backup_archive_log(self):
        """
        Getter to fetch if archive log backup enabled or not

            Returns:
                    bool     --  True if archivelog is enabled on the subclient. Else False

        """
        return self._oracle_subclient_properties.get("backupArchiveLog")

    @backup_archive_log.setter
    def backup_archive_log(self, backup_archive_log):
        """
        Setter to enable backup archive log in oracle subclient

            Args:
                backup_archive_log    (bool)    --  True if archive log to be enabled
                                                    on the subclient.Else False
        """
        self._set_subclient_properties(
            "_oracle_subclient_properties['backupArchiveLog']", backup_archive_log)

    @property
    def selective_online_full(self):
        """
        Getter to fetch if selective online full enabled or not

            Returns:
                    bool     --  True if selective online is enabled on the subclient. Else False

        """
        return self._oracle_subclient_properties.get("selectiveOnlineFull")

    @selective_online_full.setter
    def selective_online_full(self, selective_online_full):
        """
        Setter to enable backup archive log in oracle subclient

            Args:
                selective_online_full    (bool)    --  True if selective online to be enabled
                                                        on the subclient.Else False
        """
        self.backup_archive_log = True
        self._set_subclient_properties(
            "_oracle_subclient_properties['selectiveOnlineFull']", selective_online_full)

    @property
    def archive_files_per_bfs(self):
        """
        Getter to fetch archive files per BFS

            Returns:
                    (int)    --     value for archive files per BFS
        """
        return self._oracle_subclient_properties.get("archiveFilesPerBFS")

    @archive_files_per_bfs.setter
    def archive_files_per_bfs(self, archive_files_per_bfs=32):
        """
        Setter to set parameter  archive files per BFS

            Args:
               archive_files_per_bfs    (int)    --     value for archive files per BFS
                                                        default : 32
        """
        self._set_subclient_properties(
            "_oracle_subclient_properties['archiveFilesPerBFS']", archive_files_per_bfs)

    @property
    def data_stream(self):
        """
        Getter to fetch data stream count

            Returns:
                    int     --  data backup stream count at subclient level

        """
        return self._oracle_subclient_properties.get("dataThresholdStreams")

    @data_stream.setter
    def data_stream(self, data_stream=1):
        """
        Setter to set data backup stream count at subclient level

            Args:
                data_stream    (int)    --  data backup stream count at subclient level
                                            default = 1
        """
        self._set_subclient_properties(
            "_oracle_subclient_properties['dataThresholdStreams']", data_stream)

    @property
    def data_sp(self):
        """
        Getter for data storage policy

        Returns:
            string - string representing data storage policy
        """
        return self._commonProperties['storageDevice'][
            'dataBackupStoragePolicy']['storagePolicyName']

    @property
    def is_table_browse_enabled(self):
        """
        Getter to check whether the subclient has table browse enabled

        Returns:
            Bool - True if table browse is enabled on the subclient. Else False
        """
        # return self._oracle_subclient_properties['enableTableBrowse']
        return self._subclient_properties['oracleSubclientProp']['enableTableBrowse']

    @property
    def is_snapenabled(self):
        """
        Getter to check whether the subclient has snap enabled

        Returns:
            Bool - True if snap is enabled on the subclient. Else False

        """
        return self._subclient_properties['commonProperties']['snapCopyInfo']['isSnapBackupEnabled']

    def enable_table_browse(self):
        """
        Enables Table Browse for the subclient.

        Raises:
            SDKException:
                if failed to enable tablebrowse for subclient

        """

        self._set_subclient_properties("_oracle_subclient_properties['enableTableBrowse']", True)

    def disable_table_browse(self):
        """Disables Table Browse for the subclient.
            Raises:
                SDKException:
                        if failed to disable tablebrowse for subclient
        """

        self._set_subclient_properties(
            "_oracle_subclient_properties['enableTableBrowse']", False
        )

    def set_backupcopy_interface(self, interface):
        """Sets the backup copy interafce for the subclient.

            Args:
                interface (str) -- type of the backup copy interface

            Raises:
                SDKException:
                    if failed to disable intelli snap for subclient
        """

        if interface in self._backupcopy_interfaces:
            interface = self._backupcopy_interfaces[interface]
            self._commonProperties['snapCopyInfo']['backupCopyInterface'] = interface
        else:
            raise SDKException("Subclient", "101")

    @property
    def find(self, *args, **kwargs):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__, 'find'))

    def backup(
            self,
            backup_level=InstanceBackupType.FULL.value,
            cumulative=False,
            schedule_pattern=None):
        """

        Args:

            backup_level            (str)   --  level of backup the user wish to run
                                                Full / Incremental
                                                    default: Full

            cumulative (Bool) -- True if cumulative backup is required
                                    default: False

            schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

        Returns:
            object - instance of the Job class for this backup job if its an immediate Job

                     instance of the Schedule class for the backup job if its a scheduled Job

        Raises:
            SDKException:
                if backup level is incorrect

                if response is empty

                if response does not succeed

        """
        if backup_level not in ['full', 'incremental']:
            raise SDKException(r'Subclient', r'103')

        if not (cumulative or schedule_pattern):
            return super(OracleSubclient, self).backup(backup_level)

        if cumulative:
            backup_level = InstanceBackupType.CUMULATIVE.value
        request_json = self._oracle_backup_json(
            backup_level,
            schedule_pattern
        )
        backup_service = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service, request_json
        )
        return self._process_backup_response(flag, response)

    def inline_backupcopy(self, backup_level=InstanceBackupType.FULL.value):
        """Performs inline backupcopy on an oracle subclient

        Args:
            backup_level (str)  -- Level of backup. Can be full or incremental
                default: full

        Returns:
            object -- instance of Job class

        Raises:
            SDKException:
                if backup level is incorrect

                if response is empty

                if response does not succeed

        """
        if backup_level not in ['full', 'incremental']:
            raise SDKException(r'Subclient', r'103')

        backupcopy_level = 1

        backup_opts = {
            "dataOpt": {
                "skipCatalogPhaseForSnapBackup": True,
                "createBackupCopyImmediately": True,
                "useCatalogServer": True,
                "followMountPoints": True,
                "enableIndexCheckPointing": True,
                "backupCopyType": 2,
                "enforceTransactionLogUsage": True,
                "skipConsistencyCheck": False,
                "collectVMGranularRecoveryMetadataForBkpCopy": False,
                "createNewIndex": False,
                "verifySynthFull": True
            }
        }

        request_json = self._backup_json(
            backupcopy_level,
            incremental_backup=False,
            incremental_level=backupcopy_level,
            advanced_options=backup_opts,
            schedule_pattern=None)

        backup_service = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service, request_json
        )
        return self._process_backup_response(flag, response)

    def restore(
            self,
            files=None,
            destination_client=None,
            common_options=None,
            browse_option=None,
            oracle_options=None, tag=None):
        """Performs restore the entire/partial database using latest backup/backupcopy

        Args:
            files               (dict) -- dictionary containing file options
                default -- None

            destination_client  (str) -- destination client name
                default -- None

            common_options      (dict) -- common options to be passed on for restore
                default -- None

            browse_option       (dict) -- dictionary containing browse options

            oracle_options      (dict) -- dictionary containing other oracle options
                default -- By default it restores the controlfile and datafiles
                                from latest backup

            tag                 (str)  --  Type of the restore to be performed
                default:    None

                Example: {
                            "resetLogs": 1,
                            "switchDatabaseMode": True,
                            "noCatalog": True,
                            "restoreControlFile": True,
                            "recover": True,
                            "recoverFrom": 3,
                            "restoreData": True,
                            "restoreFrom": 3

                        }

        Returns:
            object -- Job containing restore details
        """
        return self._backupset_object._instance_object.restore(files, destination_client,
                                                               common_options, browse_option,
                                                               oracle_options, tag)

    def restore_in_place(
            self,
            db_password=None,
            database_list=None,
            dest_client_name=None,
            dest_instance_name=None,
            destination_path=None):
        """
        Method to restore the logical dump 

            Args:
                
                db_password             (str)  -- password for oracle database
                                    
                database_list           (List) -- List of databases

                dest_client_name        (str)  -- Destination Client name

                dest_instance_name      (str)  -- Destination Instance name

                destination_path        (str)   --  destination path for restore

                    default: None

            Returns:
                object -- Job containing restore details

        """
        instance_object = self._instance_object
        if dest_client_name is None:
            dest_client_name = instance_object._agent_object._client_object.client_name

        if dest_instance_name is None:
            dest_instance_name = instance_object.instance_name

        instance_object._restore_association = self._subclient_properties["subClientEntity"]
        
        return instance_object.restore_in_place(
            db_password,
            database_list,
            dest_client_name,
            dest_instance_name,
            dest_path=destination_path)
