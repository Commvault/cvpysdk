# -*- coding: utf-8 -*-
# ————————————————————————–
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# ————————————————————————–

"""File for operating on a Sharepoint Subclient

SharepointSubclient is the only class defined in this file.

SharepointSubclient: Derived class from Subclient Base class, representing a sharepoint subclient,
and to perform operations on that subclient

SharepointSubclient:

    _get_subclient_properties()         --  gets the subclient related properties of the Sharepoint subclient.

    _get_subclient_properties_json()    --  gets all the subclient related properties of the Sharepoint subclient.

    _process_restore_response           --  processes response received for the restore request.

    _restore_request_json               --  returns the JSON request to pass to the API as per the options.

    sharepoint_subclient_prop()         --  initializes additional properties of this subclient.

    content()                           --  sets the content of the subclient.

    restore()                           --  restores the databases specified in the input paths list.

"""

from __future__ import unicode_literals
from base64 import b64encode
from ..subclient import Subclient
from ..exception import SDKException
from ..constants import SQLDefines
from ..constants import SharepointDefines


class SharepointSubclient(Subclient):
    """Derived class from Subclient Base class, representing a Sharepoint subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient related properties of the Sharepoint subclient.

        """
        super(SharepointSubclient, self)._get_subclient_properties()

        self._sharepoint_subclient_prop = self._subclient_properties.get('sharepointsubclientprop', {})
        self._content = self._subclient_properties.get('content', {})

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "sharepointsubclientprop": self._sharepoint_subclient_prop,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def sharepoint_subclient_prop(self):
        """ getter for sql server subclient properties """
        return self._sharepoint_subclient_prop

    @sharepoint_subclient_prop.setter
    def sharepoint_subclient_prop(self, value):
        """

            Args:
                value (list)  --  list of the category and properties to update on the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        category, prop = value

        self._set_subclient_properties(category, prop)

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """

        subclient_content = self._content

        content_list = []

        for content in subclient_content:
            if 'spContentPath' in content:
                content_list.append(content["spContentPath"])

        return content_list

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add a new Sharepoint server Subclient
            with the content passed in subclient content.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

        """
        content = []

        for webapp in subclient_content:
            sp_server_dict = {
                "spContentPath": webapp
            }
            content.append(sp_server_dict)

        self._set_subclient_properties("_content", content)

    def restore(
            self,
            content_to_restore,
            database_client,
            spsetup_list,
            overwrite=True
    ):
        """Restores the Sharepoint content specified in the input paths list.

            Args:
                content_to_restore (list):  Content to restore.

                database_client (str): Name of Sharepoint SQL server back-end client.

                spsetup_list (dict): Dictionary of the Sharepoint setup configuration.

                overwrite (bool):  Unconditional overwrite files during restore.  Defaults to True.

                to_time (str):  Restore to time.  Defaults to None.


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if content_to_restore is not a list

                    if response is empty

                    if response is not success
        """
        if not isinstance(content_to_restore, list):
            raise SDKException('Subclient', '101')

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        request_json = self._sharepoint_restore_options_json(
            content_to_restore,
            database_client,
            spsetup_list,
            overwrite=overwrite
        )

        return self._process_restore_response(request_json)

    def _sharepoint_restore_options_json(
            self,
            content,
            database_client,
            spsetup_list,
            destination_client=None,
            overwrite=None
    ):
        """Constructs JSON for Sharepoint restore options based on restore request
            and returns the constructed json.

            Args:
                content (list):  List of Sharepoint content to restore.

                database_client (str): Name of Sharepoint SQL server back-end client.

                spsetup_list (dict): Dictionary of the Sharepoint setup configuration.

                destination_client (str): Restore destination Sharepoint client.

                overwrite (bool):  Unconditional overwrite files during restore.  Defaults to True.

            Returns:
                dict: dictionary consisting of the Sharepoint Server options.
        """
        client_name = self._client_object._client_name

        request_json = self._restore_json(
            client=client_name
        )

        if destination_client is None:
            destination_client = client_name

        common_options = {
            "allVersion": True,
            "erExSpdbPathRestore": True
        }
        destination = {
            "inPlace": True, # TODO check if in-place/oop.. will do this when we implement oop testcase
            "destClient": {
                "clientName": destination_client
            },
            "destinationInstance": {
                "clientName": destination_client,
                "instanceName": "defaultInstance",
                "appName": self._agent_object.agent_name
            }
        }
        sql_restore_options = {
            "sqlRecoverType": SQLDefines.STATE_RECOVER,
            "dropConnectionsToDatabase": True,
            "overWrite": overwrite,
            "sqlRestoreType": SQLDefines.DATABASE_RESTORE
        }
        sharepoint_restore_option = {
            "configContentDatabase": True,
            "isSharePointRBS": False,
            "restoreSqlDBTO": False,
            "is90OrUpgradedClient": False,
            "restoreSqlDBtoLocation": "",
            "fetchSqlDatabases": True,
            "spRestoreToDisk": {
                "restoreToDisk": False
            }
        }
        sharepoint_db_restore_option = {
            "restoreType": "SameConfiguration",
            "restoreDatabaseOption": "RESTORE_ALL",
            "rbsOptions": {
                "sqlSource": {
                    "clientName": database_client
                },
                "sqlDestination": {
                    "destClient": {
                        "clientName": database_client
                    }
                }
            }
        }

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']\
            ['browseOption']['backupset']["backupsetName"] = self._backupset_object._backupset_name
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["sqlServerRstOption"] = sql_restore_options
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["sharePointDBRestoreOption"] = sharepoint_db_restore_option
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["commonOptions"].update(common_options)
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["destination"].update(destination)
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["sharePointRstOption"].update(sharepoint_restore_option)


        content_json = {}
        source_items = []
        database_list = []
        for item in content:
            item = item.split("\\")[2]
            for sp_dict in spsetup_list:
                if sp_dict["application_pool"].lower() == item.lower():
                    database_name = sp_dict["content_database"]
                    database_server = sp_dict["database_server"]
                    web_application = sp_dict["web_application"]
                    username = sp_dict["credentials"]["username"]
                    password = b64encode(sp_dict["credentials"]["password"].encode()).decode()

                    source_items.append(
                        SharepointDefines.CONTENT_WEBAPP.format(item)
                    )
                    source_items.append(
                        SharepointDefines.CONTENT_DB.format(item, database_name)
                    )

                    database_list.append(database_name)

                    content_json = {
                        "SharePointMetaData": [{
                            "newDirectoryName": "",
                            "newDatabaseServerName": database_server,
                            "sourceItem":
                                SharepointDefines.CONTENT_DB.format(item, database_name),
                            "newDatabaseName": database_name,
                            "sharePointMetaDataType": "SPContentDatabase"
                        }, {
                            "sourceItem":
                                SharepointDefines.CONTENT_WEBAPP.format(item),
                            "newWebApplicationURL": web_application,
                            "newWebApplicationName": item,
                            "sharePointMetaDataType": "SPWebApplication",
                            "credentials": {
                                "userName": username,
                                "password": password
                                }
                        }]
                    }
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["fileOption"]["sourceItem"] = source_items
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["sqlServerRstOption"]["database"] = database_list
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["sqlServerRstOption"]["restoreSource"] = database_list
        request_json['taskInfo']['subTasks'][0]['options']["restoreOptions"]\
            ["sharePointDBRestoreOption"].update(content_json)

        return request_json
