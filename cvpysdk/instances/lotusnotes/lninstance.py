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

"""Main file for operating on all Lotus Notes Instances.

LNInstance is the only class defined in this file.

LNInstance:
    restore_in_place()                  -- performs an in place restore

    restore_out_of_place()              -- performs an out of place restore

"""

from __future__ import unicode_literals

from ...instance import Instance
from ...exception import SDKException


class LNInstance(Instance):
    """Derived class from Instance Base class, representing an LNDOC instance,
        and to perform operations on that instance."""

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

                common_options_dict (dict)          -- dictionary for all the common options
                    options:
                        unconditionalOverwrite              :   overwrite the files during restore
                        even if they exist

                        recoverWait                         :   Specifies whether this restore
                        operation must wait until resources become available if a database recovery
                        is already taking place

                        recoverZap                          :   Specifies whether the IBM Domino
                        must change the DBIID associated with the restored database

                        recoverZapReplica                   :   Specifies whether the restore
                        operation changes the replica id of the restored database

                        recoverZapIfNecessary               :   Specifies whether the IBM Domino
                        can change the DBIID associated with the restored database if necessary

                        doNotReplayTransactLogs             :   option to skip restoring or
                        replaying logs

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        self._restore_association = self.backupsets.get(
            list(self.backupsets.all_backupsets)[0]
        )._backupset_association

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

                copy_precedence         (int)      --  copy precedence value of storage policy copy

                    default: None

                from_time           (str)          --  time to retore the contents after

                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)            --  time to retore the contents before

                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                 common_options_dict (dict)          -- dictionary for all the common options
                    options:
                        overwriteDBLinks              :   overwrite the db links

                            default: False

                        overwriteDesignDoc            :   overwrite design documents

                            default: False

                        overwriteDataDoc              :   overwrite the data documents

                            default: False

                        dbLinksOnly                   :   overwrite the db links only

                            default: False

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
        self._restore_association = self.backupsets.get(
            list(self.backupsets.all_backupsets)[0]
        )._backupset_association

        request_json = self._restore_json(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            **kwargs
        )

        return self._process_restore_response(request_json)

