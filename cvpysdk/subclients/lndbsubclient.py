# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Notes Database Subclient.

LNDbSubclient is the only class defined in this file.

LNDbSubclient:  Derived class from Subclient Base class.
Represents a notes database subclient, and performs operations on that subclient

LNDbSubclient:

    _get_subclient_properties()         --  gets subclient related properties of
    Notes Database subclient.

    _get_subclient_properties_json()    --  gets all the subclient related properties of
    Notes Database subclient.

    content()                           --  update the content of the subclient

    restore_in_place()                  -- performs an in place restore of the subclient

    restore_out_of_place()              -- performs and out of place restore of the subclient
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import json

from ..subclient import Subclient


class LNDbSubclient(Subclient):
    """Derived class from Subclient Base class, representing a LNDB subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of LN DB subclient."""
        super(LNDbSubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']
        if 'proxyClient' in self._subclient_properties:
            self._proxyClient = self._subclient_properties['proxyClient']
        if 'subClientEntity' in self._subclient_properties:
            self._subClientEntity = self._subclient_properties['subClientEntity']
        if 'commonProperties' in self._subclient_properties:
            self._commonProperties = self._subclient_properties['commonProperties']

    def _get_subclient_properties_json(self):
        """Get the all subclient related properties of this subclient.
           Returns:
                dict - all subclient properties put inside a dict
        """

        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        return self._content

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
        LNDB Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API

        """
        content = []
        try:
            for database in subclient_content:
                if 'lotusNotesDBContent' in database:
                    content.append(database)
                else:
                    temp_content_dict = {}
                    temp_content_dict = {
                        "lotusNotesDBContent": {
                            "dbiid1": database['dbiid1'],
                            "dbiid2": database['dbiid2'],
                            "dbiid3": database['dbiid3'],
                            "dbiid4": database['dbiid4'],
                            "relativePath": database['relativePath'],
                            "databaseTitle": database['databaseTitle']
                        }
                    }
                    if temp_content_dict != {}:
                        content.append(temp_content_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        self._set_subclient_properties("_content", content)

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

        if common_options_dict is None:
            common_options_dict = {}

        if lndb_restore_options is None:
            lndb_restore_options = {}

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
            fs_options=None,
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
                        preserve_level      : preserve level option to set in restore

                        proxy_client        : proxy that needed to be used for restore

                        impersonate_user    : Impersonate user options for restore

                        impersonate_password: Impersonate password option for restore
                        in base64 encoded form

                        all_versions        : if set to True restores all the versions of the
                        specified file

                        versions            : list of version numbers to be backed up

                        media_agent         : Media Agent need to be used for Browse and restore

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

        if not (isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if common_options_dict is None:
            common_options_dict = {}

        if lndb_restore_options is None:
            lndb_restore_options = {}

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
            fs_options=fs_options,
            common_options_dict=common_options_dict,
            lndb_restore_options=lndb_restore_options)

        return self._process_restore_response(request_json)
