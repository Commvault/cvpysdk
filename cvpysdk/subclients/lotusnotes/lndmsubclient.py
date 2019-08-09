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

"""File for operating on a Domino Mailbox Archiver Subclient.

LNDmSubclient is the only class defined in this file.

LNDmSubclient:  Derived class from Subclient Base class.
Represents a domino mailbox archiver subclient, and performs operations on that subclient

LNDmSubclient:

    restore_in_place()                  -- performs an in place restore of the subclient

    restore_out_of_place()              -- performs and out of place restore of the subclient

    backup()                            --  run a backup job for the subclient
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .lnsubclient import LNSubclient
from ...exception import SDKException


class LNDmSubclient(LNSubclient):
    """Derived class from LNSubclient Base class, representing a LNDM subclient,
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

                common_options_dict (dict)          -- dictionary for all the common options
                    options:
                        append                      :   append documents to the database

                            default: False

                        skip                        :   skip if already present

                            default: False

                        unconditionalOverwrite      :   overwrite the documents

                            default: False

                        restoreOnlyStubExists       :   restore only if it is a stub

                            default: False

            Returns:
                object  -   instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        return super(LNDmSubclient, self).restore_in_place(
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)

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

                common_options_dict (dict)          -- dictionary for all the common options
                    options:
                        append                      :   append documents to the database

                            default: False

                        skip                        :   skip if already present

                            default: False

                        unconditionalOverwrite      :   overwrite the documents

                            default: False

                        restoreOnlyStubExists       :   restore only if it is a stub

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
        return super(LNDmSubclient, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)
