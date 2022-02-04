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

"""

from __future__ import unicode_literals

from past.builtins import basestring

from .fssubclient import FileSystemSubclient
from ..exception import SDKException


class NASSubclient(FileSystemSubclient):
    """Derived class from Subclient Base class, representing a nas subclient,
        and to perform operations on that subclient."""
    
   
    def backup(
            self,
            backup_level="Incremental",
            incremental_backup=False,
            incremental_level='BEFORE_SYNTH', on_demand_input=None, snap_name=None):
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

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        
        if snap_name is None:
            return super(NASSubclient, self).backup(
                backup_level, incremental_backup, incremental_level, on_demand_input=on_demand_input
            )
        else:
            request_json = self._backup_json(backup_level, incremental_backup, incremental_level)

            if not isinstance(snap_name, basestring):
                raise SDKException('Subclient', '101')

            if snap_name:
                nas_options = {
                    "nasOptions": {
                        "backupFromSnap": snap_name,
                        "backupQuotas": True,
                        "backupFromSnapshot": True,
                        "backupFromSnapshotYes": True,
                        "replicationVolumeId": 0
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
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None,
            proxy_client=None,
            advanced_options=None,
            synthRestore=False):
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
                
                synthRestore (bool)     -- Advance NAS restore option SynthRestore

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
        if synthRestore == False:
            return super(NASSubclient, self).restore_in_place(
                paths,
                overwrite,
                restore_data_and_acl,
                copy_precedence,
                from_time,
                to_time,
                fs_options,
                schedule_pattern,
                proxy_client,
                advanced_options
            )
        else:
            request_json = self._restore_json(
                paths=paths,
                overwrite=overwrite,
                restore_data_and_acl=restore_data_and_acl,
                copy_precedence=copy_precedence,
                from_time=from_time,
                to_time=to_time,
                fs_options=None,
                schedule_pattern=None,
                proxy_client=None,
                advanced_options=None
            )
            
            nas_option = {
                "nasOption": {
                     "synthRestore": 1
                }
            }

            request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"].update(nas_option)

            
            return self._process_restore_response(request_json)