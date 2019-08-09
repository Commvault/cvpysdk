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
