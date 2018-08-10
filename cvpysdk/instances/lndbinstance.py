# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Lotus Notes Database Agent Instance.

LNDBInstance is the only class defined in this file.

LNDBInstance:
    restore_in_place()                  -- performs an in place restore of the subclient

    restore_out_of_place()              -- performs an out of place restore of the subclient

"""

from __future__ import unicode_literals

from ..instance import Instance


class LNDBInstance(Instance):
    """Derived class from Instance Base class, representing an LNDB instance,
        and to perform operations on that instance."""

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            common_options_dict=None,
            lndb_restore_options=None):
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


                    Disaster Recovery special options:
                        skipErrorsAndContinue               :   enables a data recovery operation
                        to continue despite media errors
                        
                        disasterRecovery                    :   run disaster recovery

                lndb_restore_options    (dict)          -- dictionary for all options specific
                to an lndb restore
                    options:
                        disableReplication      :   disable relpication on database

                        disableBackgroundAgents :   disable background agents

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
            common_options_dict=common_options_dict,
            lndb_restore_options=lndb_restore_options
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
            common_options_dict=None,
            lndb_restore_options=None):
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


                    Disaster Recovery special options:
                        skipErrorsAndContinue               :   enables a data recovery operation
                        to continue despite media errors
                        
                        disasterRecovery                    :   run disaster recovery

                lndb_restore_options    (dict)          -- dictionary for all options specific
                to an lndb restore
                    options:
                        disableReplication      :   disable relpication on database

                        disableBackgroundAgents :   disable background agents

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
            common_options_dict=common_options_dict,
            lndb_restore_options=lndb_restore_options
        )

        return self._process_restore_response(request_json)

    def _restore_common_options_json(self, value):
        """setter for  the Common options of in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "doNotReplayTransactLogs": value.get('common_options_dict').get(
                'doNotReplayTransactLogs', False
            ),
            "clusterDBBackedup": value.get('common_options_dict').get(
                'clusterDBBackedup', False
            ),
            "recoverWait": value.get('common_options_dict').get(
                'recoverWait', False
            ),
            "restoreToDisk": value.get('common_options_dict').get(
                'restoreToDisk', False
            ),
            "offlineMiningRestore": value.get('common_options_dict').get(
                'offlineMiningRestore', False
            ),
            "restoreToExchange": value.get('common_options_dict').get(
                'restoreToExchange', False
            ),
            "recoverZapIfNecessary": value.get('common_options_dict').get(
                'recoverZapIfNecessary', False
            ),
            "recoverZapReplica": value.get('common_options_dict').get(
                'recoverZapReplica', False
            ),
            "copyToObjectStore": value.get('common_options_dict').get(
                'copyToObjectStore', False
            ),
            "onePassRestore": value.get('common_options_dict').get(
                'onePassRestore', False
            ),
            "recoverZap": value.get('common_options_dict').get(
                'recoverZap', False
            ),
            "recoverRefreshBackup": value.get('common_options_dict').get(
                'recoverRefreshBackup', False
            ),
            "unconditionalOverwrite": value.get('common_options_dict').get(
                'unconditionalOverwrite', False
            ),
            "syncRestore": value.get('common_options_dict').get(
                'syncRestore', False
            ),
            "recoverPointInTime": value.get('common_options_dict').get(
                'recoverPointInTime', False
            )
        }

        if value.get('common_options_dict').get('disasterRecovery'):
            self._commonoption_restore_json.update({
                "restoreDeviceFilesAsRegularFiles": value.get('common_options_dict').get(
                    'restoreDeviceFilesAsRegularFiles', False
                ),
                "isFromBrowseBackup": value.get('common_options_dict').get(
                    'isFromBrowseBackup', False
                ),
                "ignoreNamespaceRequirements": value.get('common_options_dict').get(
                    'ignoreNamespaceRequirements', False
                ),
                "restoreSpaceRestrictions": value.get('common_options_dict').get(
                    'restoreSpaceRestrictions', False
                ),
                "skipErrorsAndContinue": value.get('common_options_dict').get(
                    'skipErrorsAndContinue', False
                ),
                "recoverAllProtectedMails": value.get('common_options_dict').get(
                    'recoverAllProtectedMails', False
                ),
                "validateOnly": value.get('common_options_dict').get(
                    'validateOnly', False
                ),
                "revert": value.get('common_options_dict').get(
                    'revert', False
                ),
                "disasterRecovery": value.get('common_options_dict').get(
                    'disasterRecovery', True
                ),
                "detectRegularExpression": value.get('common_options_dict').get(
                    'detectRegularExpression', True
                ),
            })

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

                   Args:
                       kwargs   (list)  --  list of options need to be set for restore

                   Returns:
                       dict - JSON request to pass to the API
               """
        restore_json = super(LNDBInstance, self)._restore_json(**kwargs)

        restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'lotusNotesDBRestoreOption'] = {
            "disableReplication": kwargs.get('lndb_restore_options').get('disableReplication', False),
            "disableBackgroundAgents": kwargs.get('lndb_restore_options').get('disableBackgroundAgents', False)
        }

        if kwargs.get('common_options_dict').get('disasterRecovery'):
            restore_json['taskInfo']['subTasks'][0]['options']['commonOpts'] = {
                'jobDescription': '',
                'startUpOpts': {
                    'startInSuspendedState': False,
                    'useDefaultPriority': True,
                    'priority': 166
                }
            }
            restore_json['taskInfo']['subTasks'][0]['options']['backupOpts'] = {
                'backupLevel': 2
            }
            restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'browseOption']['mediaOption']['copyPrecedence'] = {
                'copyPrecedence': 0,
                'synchronousCopyPrecedence': 1,
                'copyPrecedenceApplicable': False
            }
        return restore_json
