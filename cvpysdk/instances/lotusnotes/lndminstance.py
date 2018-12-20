# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Lotus Notes Database Agent Instance.

LNDOCInstance is the only class defined in this file.

LNDOCInstance:
    _commonoption_restore_json          --  setter for  the Common options in restore JSON

    restore_in_place()                  --  performs an in place restore of the subclient

    restore_out_of_place()              --  performs an out of place restore of the subclient

"""

from __future__ import unicode_literals

from .lninstance import LNInstance
from ...exception import SDKException


class LNDMInstance(LNInstance):
    """Derived class from LNInstance Base class, representing an LNDOC instance,
        and to perform operations on that instance."""

    def _commonoption_restore_json(self, value):
        """setter for  the Common options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "append": value.get('common_options_dict').get(
                'append', False
            ),
            "skip": value.get('common_options_dict').get(
                'skip', False
            ),
            "unconditionalOverwrite": value.get('common_options_dict').get(
                'unconditionalOverwrite', True
            ),
            "restoreOnlyStubExists": value.get('common_options_dict').get(
                'restoreOnlyStubExists', False
            ),
            "onePassRestore": value.get('common_options_dict').get(
                'onePassRestore', False
            ),
            "offlineMiningRestore": value.get('common_options_dict').get(
                'offlineMiningRestore', False
            ),
            "clusterDBBackedup": value.get('common_options_dict').get(
                'clusterDBBackedup', False
            ),
            "recoverToRecoveredItemsFolder": value.get('common_options_dict').get(
                'recoverToRecoveredItemsFolder', False
            ),
            "restoreToDisk": value.get('common_options_dict').get(
                'restoreToDisk', False
            ),
            "syncRestore": value.get('common_options_dict').get(
                'syncRestore', False
            ),
            "restoreToExchange": value.get('common_options_dict').get(
                'restoreToExchange', False
            ),
            "copyToObjectStore": value.get('common_options_dict').get(
                'copyToObjectStore', False
            )
        }

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            common_options_dict=None):
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
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        return super(LNDMInstance, self).restore_in_place(
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
            common_options_dict=None):
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
        return super(LNDMInstance, self).restore_out_of_place(
            client,
            destination_path,
            paths,
            overwrite,
            restore_data_and_acl,
            copy_precedence,
            from_time,
            to_time,
            **kwargs)

