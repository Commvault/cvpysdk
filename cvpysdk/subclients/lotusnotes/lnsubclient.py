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

"""Main file for operating on any Lotus Notes Subclient.

LNSubclient is the only class defined in this file.

LNSubclient:        Class for representing all the Lotus Notes iDAs and performing
                        operations on them

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ...subclient import Subclient
from ...exception import SDKException


class LNSubclient(Subclient):
    """Derived class from Subclient Base class, representing an LN subclient,
        and to perform operations on that subclient."""

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            **kwargs):
        """Restores the files/folders specified in the input paths list to the same location.

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

            Returns:
                object  -   instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        if not (isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if kwargs.get('common_options_dict') is None:
            kwargs['common_options_dict'] = {}

        if kwargs.get('lndb_restore_options') is None:
            kwargs['lndb_restore_options'] = {}

        paths = self._filter_paths(paths)

        if paths == []:
            raise SDKException('Subclient', '104')

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        request_json = self._restore_json(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            **kwargs
        )

        return self._process_restore_response(request_json)

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            **kwargs):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore

                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files

                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy

                    default: None

                from_time           (str)       --  time to retore the contents after

                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before

                        format: YYYY-MM-DD HH:MM:SS

                    default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        if not (isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if kwargs.get('common_options_dict') is None:
            kwargs['common_options_dict'] = {}

        if kwargs.get('lndb_restore_options') is None:
            kwargs['lndb_restore_options'] = {}

        paths = self._filter_paths(paths)

        if paths == []:
            raise SDKException('Subclient', '104')

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        request_json = self._restore_json(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            in_place=False,
            **kwargs)

        return self._process_restore_response(request_json)

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               schedule_pattern=None):

        """Returns the JSON request to pass to the API as per the options selected by the user.

                    Args:
                        backup_level        (str)   --  level of backup the user wish to run

                            Full / Incremental / Differential / Synthetic_full

                        incremental_backup  (bool)  --  run incremental backup

                            only applicable in case of Synthetic_full backup

                        incremental_level   (str)   --  run incremental backup before/after
                        synthetic full

                            BEFORE_SYNTH / AFTER_SYNTH

                            only applicable in case of Synthetic_full backup

                        schedule_pattern (dict) -- scheduling options to be included for the task

                            Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                    Returns:
                        dict    -   JSON request to pass to the API

        """

        if schedule_pattern:
            request_json = self._backup_json(
                backup_level,
                incremental_backup,
                incremental_level,
                schedule_pattern=schedule_pattern)

            backup_service = self._services['CREATE_TASK']

            flag, response = self._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

        else:
            return super(LNSubclient, self).backup(
                backup_level=backup_level,
                incremental_backup=incremental_backup,
                incremental_level=incremental_level)

        return self._process_backup_response(flag, response)
