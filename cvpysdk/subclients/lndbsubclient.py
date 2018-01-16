# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Notes Database Subclient.

LNDbSubclient is the only class defined in this file.

LNDbSubclient:  Derived class from Subclient Base class.
                    Represents a notes database subclient,
                    and performs operations on that subclient

LNDbSubclient:

    _get_subclient_properties()          --  gets subclient related properties of
                                                    Notes Database subclient.

    _get_subclient_properties_json()     --  gets all the subclient related properties of
                                                    Notes Database subclient.

    content()                            --  update the content of the subclient

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
        # print(self._subclient_properties)
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

    # # @content.setter
    # def content(self, subclient_content):
    #     """
    #
    #     Creates the list of content JSON to pass to the API to add/update content of a
    #         LNDB Subclient.
    #
    #         Args:
    #             subclient_content (list)  --  list of the content to add to the subclient
    #
    #         Returns:
    #             list - list of the appropriate JSON for an agent to send to the POST Subclient API
    #
    #     """
    #     content = []
    #
    #     try:
    #         for database in subclient_content:
    #             print(database)
    #             print(type(database))
    #             # temp_content_dict = {
    #             #     "lotusNotesDBContent": {
    #             #             "dbiid1"        : database['dbiid1'],
    #             #             "dbiid2"        : database['dbiid2'],
    #             #             "dbiid3"        : database['dbiid3'],
    #             #             "dbiid4"        : database['dbiid4'],
    #             #             "relativePath"  : database['relativePath'],
    #             #             "databaseTitle" : database['databaseTitle'],
    #             #         }
    #             # }
    #             content.append(database)
    #     except KeyError as err:
    #         raise SDKException('Subclient', '102', '{} not given in content'.format(err))
    #
    #     self._set_subclient_properties("_content", content)

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

        request_json = self._restore_json(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time
        )

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["commonOptions"] = {
                "doNotReplayTransactLogs": common_options_dict.get('doNotReplayTransactLogs', False),
                "clusterDBBackedup": common_options_dict.get('clusterDBBackedup', False),
                "recoverWait": common_options_dict.get('recoverWait', False),
                "restoreToDisk": common_options_dict.get('restoreToDisk', False),
                "offlineMiningRestore": common_options_dict.get('offlineMiningRestore', False),
                "restoreToExchange": common_options_dict.get('restoreToExchange', False),
                "recoverZapIfNecessary": common_options_dict.get('recoverZapIfNecessary', False),
                "recoverZapReplica": common_options_dict.get('recoverZapReplica', False),
                "onePassRestore": common_options_dict.get('onePassRestore', False),
                "recoverZap": common_options_dict.get('recoverZap', False),
                "recoverRefreshBackup": common_options_dict.get('recoverRefreshBackup', False),
                "unconditionalOverwrite": common_options_dict.get('unconditionalOverwrite', False),
                "syncRestore": common_options_dict.get('syncRestore', False),
                "recoverPointInTime": common_options_dict.get('recoverPointInTime', False),
            }

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["lotusNotesDBRestoreOption"] = {
            "disableReplication": lndb_restore_options.get('disableReplication', False),
            "disableBackgroundAgents": lndb_restore_options.get('disableBackgroundAgents', False)
        }

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"] = {"sourceItem": ["\\"]}
        with open(r'C:/lndb_restore.json', 'w') as f:
            f.write(json.dumps(request_json))
        print(request_json)
        return self._process_restore_response(request_json)
