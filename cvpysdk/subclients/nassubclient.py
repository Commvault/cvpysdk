#!/usr/bin/env python
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

"""File for operating on a NAS Subclient

NASSubclient is the only class defined in this file.

NASSubclient: Derived class from Subclient Base class, representing a nas subclient,
                        and to perform operations on that subclient

NASSubclient:
    _get_subclient_properties()          --  gets the subclient  related properties of NAS subclient.
    
    _get_subclient_properties_json()     --  gets all the subclient  related properties of NAS subclient.
    
    content()                            --  update the content of the subclient

    filter_content()                    --  update the filter content of the subclient

    content()                           --  update the content of the subclient

    backup()                            --  run a backup job for the subclient
    
    restore_in_place()                  -- run a restore in place for the subclient
    
    restore_out_of_place()                  -- run a restore out of place for the subclient

"""

from __future__ import unicode_literals

from .fssubclient import FileSystemSubclient
from ..exception import SDKException


class NASSubclient(FileSystemSubclient):
    """Derived class from Subclient Base class, representing a nas subclient,
        and to perform operations on that subclient."""
    
   
    def backup(
            self,
            backup_level="Incremental",
            incremental_backup=False,
            incremental_level='BEFORE_SYNTH',
            on_demand_input=None,
            snap_name=None,
            backup_external_links=0,
            backup_offline_data=False,
            block_backup=False,
            volume_based_backup=False):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential / Synthetic_full
                    default: Incremental

                incremental_backup  (bool)  --  run incremental backup
                        only applicable in case of Synthetic_full backup
                    default: False

                incremental_level   (str)   --  run incremental backup before/after synthetic full
                        BEFORE_SYNTH / AFTER_SYNTH

                        only applicable in case of Synthetic_full backup
                    default: BEFORE_SYNTH

                on_demand_input     (str)   --  input file location for on demand backupset
                    default: None

                snap_name   (str)   --  input for snap_name

		        backup_external_links	(int)	--	input for advanced option backup external links

                backup_offline_data   (bool)  --  input for advanced NAS backup option backupOfflineData

                block_backup (bool) -- input for advanced NAS backup option blockBackup

                volume_based_backup   (bool)  --  input for advanced NAS backup option volumeBasedBackup

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        request_json = self._backup_json(
            backup_level,
            incremental_backup,
            incremental_level,
            on_demand_input)

        nas_options = {
            "nasOptions": {
                "blockBackup": True if block_backup else False,
                "backupFromSnap": snap_name if snap_name is not None else "",
                "backupOfflineData": True if backup_offline_data else False,
                "backupQuotas": True,
                "backupFromSnapshot": True,
                "backupFromSnapshotYes": True,
                "backupExternalLinks": backup_external_links,
                "replicationVolumeId": 0,
                "volumeBasedBackup": True if volume_based_backup else False
            }
        }

        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            nas_options
        )

        bakup_service = self._commcell_object._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', bakup_service, request_json
        )

        return self._process_backup_response(flag, response)

    def restore_in_place(
            self,
            paths,
            overwrite=None,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None,
            proxy_client=None,
            advanced_options=None,
            synth_restore=False,
            DAR=None,
            noRecursive=None
            ):
        """Runs a restore job for the subclient .

            Args:
                            paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: None

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up
                        validate_only       : To validate data backed up for restore


                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                proxy_client    (str)          -- Proxy client used during FS under NAS operations

                advanced_options    (dict)  -- Advanced restore options
                
                synth_restore (bool)     -- Advance NAS restore option SynthRestore

                DAR (bool)     -- Advance NAS restore option DAR

                noRecursive (bool)     -- Advance NAS restore option Recursive

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Returns:
                object - instance of the Job class for this restore job if its an immediate Job
                         instance of the Schedule class for this restore job if its a scheduled Job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
                
        """
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        request_json = self._restore_json(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            schedule_pattern=None,
            proxy_client=None,
            advanced_options=None
        )

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['unconditionalOverwrite'] = True
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['stripLevel'] = 0
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['preserveLevel'] = 1
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['stripLevelType'] = 0

        if fs_options:
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['browseOption']['liveBrowse'] = True

        nas_option = {
            "nasOption": {
                "synthRestore": 1 if synth_restore is True else 2,
                "useDirectAccess": 0 if DAR is True else 1,
                "noRecursive": False if noRecursive is False else True,
                "overwrite": True if overwrite is True else False
            }
        }

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"].update(nas_option)

        return self._process_restore_response(request_json)
        
    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=None,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None,
            proxy_client=None,
            advanced_options=None,
            synth_restore=False,
            DAR=None,
            noRecursive=None
            ):
        """Runs a restore job for the subclient .

            Args:
                            paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up
                        validate_only       : To validate data backed up for restore


                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                proxy_client    (str)          -- Proxy client used during FS under NAS operations

                advanced_options    (dict)  -- Advanced restore options
                
                synth_restore (bool)     -- Advance NAS restore option SynthRestore

                DAR (bool)     -- Advance NAS restore option DAR

                noRecursive (bool)     -- Advance NAS restore option Recursive

                    Options:

                        job_description (str)   --  Restore job description

                        timezone        (str)   --  Timezone to be used for restore

                            **Note** make use of TIMEZONES dict in constants.py to pass timezone

            Returns:
                object - instance of the Job class for this restore job if its an immediate Job
                         instance of the Schedule class for this restore job if its a scheduled Job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
                
        """
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        request_json = self._restore_json(
            client=client,
            destPath=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            schedule_pattern=None,
            proxy_client=None,
            advanced_options=None
        )

        destination_options = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].get('destination', {})
        destination_options['destPath'] = destination_options.get('destPath', [''])
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination']['destPath'][0] = destination_path
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination']['inPlace'] = False

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['unconditionalOverwrite'] = True
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['stripLevel'] = 2
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['preserveLevel'] = 1
        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['commonOptions']['stripLevelType'] = 0

        if fs_options:
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['browseOption']['liveBrowse'] = True

        nas_option = {
            "nasOption": {
                "synthRestore": 1 if synth_restore is True else 2,
                "useDirectAccess": 0 if DAR is True else 1,
                "noRecursive": False if noRecursive is False else True,
                "overwrite": True if overwrite is True else False
            }
        }

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(nas_option)

        return self._process_restore_response(request_json)