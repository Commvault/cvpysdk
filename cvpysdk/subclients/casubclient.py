#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Cloud Apps Subclient.

CloudAppsSubclient is the only class defined in this file.

CloudAppsSubclient: Derived class from Subclient Base class, representing a
                        cloud apps subclient, and to perform operations on that subclient

CloudAppsSubclient:
    _get_subclient_content_()   --  gets the content of a cloud apps subclient

    _set_subclient_content_()   --  sets the content of a cloud apps subclient

    restore_out_of_place()      --  runs out-of-place restore for the subclient

"""

from __future__ import unicode_literals

from past.builtins import basestring

from ..exception import SDKException
from ..subclient import Subclient


class CloudAppsSubclient(Subclient):
    """Derived class from Subclient Base class, representing a CloudApps subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        for account in self._subclient_properties['content']:
            temp_account = account["cloudconnectorContent"]["includeAccounts"]

            content_dict = {
                'SMTPAddress': temp_account["contentName"],
                'display_name': temp_account["contentValue"]
            }

            content.append(content_dict)

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Cloud Apps Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        try:
            for account in subclient_content:
                temp_content_dict = {
                    "cloudconnectorContent": {
                        "includeAccounts": {
                            "contentValue": account['display_name'],
                            "contentType": 134,
                            "contentName": account['SMTPAddress']
                        }
                    }
                }

                content.append(temp_content_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        return content

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True):
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
        from ..client import Client

        if not ((isinstance(client, basestring) or isinstance(client, Client)) and
                isinstance(destination_path, basestring) and
                isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if isinstance(client, Client):
            client = client
        elif isinstance(client, basestring):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        paths = self._filter_paths(paths)

        destination_path = self._filter_paths([destination_path], True)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            in_place=False,
            client=client,
            destination_path=destination_path,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl
        )

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]['cloudAppsRestoreOptions'] = {
                "instanceType": self._backupset_object._instance_object._ca_instance_type,
                "googleRestoreOptions": {
                    "strDestUserAccount": destination_path,
                    "folderGuid": "",
                    "restoreToDifferentAccount": True,
                    "restoreToGoogle": True
                }
            }

        return self._process_restore_response(request_json)
