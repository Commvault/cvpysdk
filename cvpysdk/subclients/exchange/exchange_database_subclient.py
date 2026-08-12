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

"""Module for doing operations on an Exchange Database Agent.

This module has operations that are applicable at the Agent level for Exchange Database.

ExchangeDatabaseSubclient:
    _get_subclient_properties()         --  get the properties of the subclient, and initialize
    the basic properties

    _get_subclient_properties_json()    --  gets all the subclient properties of the
    Exchange Database subclient

    _set_content                        --  Sets the content for Exchange Database subclient

    restore_in_place()                  --  runs in-place restore for the subclient

    restore_out_of_place                --  runs out of place restore for the subclient

    set_subclient_properties()          -- sets the properties of this sub client

    create_recovery_point()             --  create recovery point for a database

    get_session()                       -- Get the session ids for a database

    get_mailbox_tags()                  -- Get the mailboxtags for mailboxes

    run_restore_messages()              -- run livebrowse restore


Attributes
----------

    **content**     --  returns the content of the Exchange Database subclient

"""

from __future__ import unicode_literals

from typing import Any

from ...subclient import Subclient
from ...exception import SDKException
from ...job import Job

from requests import Response


class ExchangeDatabaseSubclient(Subclient):
    """
    Specialized subclient class for managing Exchange Database operations.

    This class extends the Subclient base class to provide functionality
    specific to Exchange Database subclients, including property management,
    content handling, and advanced restore operations. It supports both
    in-place and out-of-place restores, recovery point creation, session
    management, mailbox tag retrieval, and message restoration.

    Key Features:
        - Retrieve and manage subclient properties and content
        - Set Exchange Database-specific subclient properties
        - Generate and handle subclient property JSON representations
        - Perform in-place and out-of-place restore operations for Exchange databases
        - Create recovery points for Exchange databases with configurable expiry
        - Manage restore sessions and retrieve mailbox tags
        - Restore messages using session and mailbox tag information

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> dict:
        """Retrieve the properties related to the Exchange Database subclient.

        Returns:
            dict: A dictionary containing the subclient properties specific to the Exchange Database subclient.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> properties = subclient._get_subclient_properties()
            >>> print(properties)
            >>> # Output will be a dictionary with subclient property details

        #ai-gen-doc
        """
        super(ExchangeDatabaseSubclient, self)._get_subclient_properties()

        self._content = self._subclient_properties.get('content', [])
        self._exchange_db_subclient_prop = self._subclient_properties.get(
            'exchangeDBSubClientProp', {}
        )

    def _get_subclient_properties_json(self) -> dict:
        """Generate a JSON-compatible dictionary of the subclient's properties.

        This method prepares all relevant subclient properties in a dictionary format,
        suitable for use in a POST request to update the subclient's configuration.

        Returns:
            dict: A dictionary containing all subclient properties.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> properties_json = subclient._get_subclient_properties_json()
            >>> # Use properties_json in a POST request to update subclient settings

        #ai-gen-doc
        """
        subclient_json = {
            "subClientProperties": {
                "subClientEntity": self._subClientEntity,
                "exchangeDBSubClientProp": self._exchange_db_subclient_prop,
                "content": self._content,
                "commonProperties": self._commonProperties,
                "contentOperationType": 1
            }
        }

        return subclient_json

    @property
    def content(self) -> list:
        """Retrieve the list of content items added to the Exchange Database Subclient.

        Returns:
            list: A list containing the content items currently associated with the subclient.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> content_list = subclient.content
            >>> print(f"Subclient content: {content_list}")

        #ai-gen-doc
        """
        return self._content

    @content.setter
    def content(self, subclient_content: list) -> None:
        """Set the content of the subclient with the provided list.

        Updates the subclient's content to match the specified list. The input must be a list,
        and each item in the list should represent a content item to be added to the subclient.

        Args:
            subclient_content: A list containing the content items to set for the subclient.

        Raises:
            SDKException: If the input is not a list or if updating the subclient content fails.

        Example:
            >>> new_content = ['Mailbox Database 1', 'Mailbox Database 2']
            >>> subclient.content = new_content  # Use assignment for property setter
            >>> print("Subclient content updated successfully")

        #ai-gen-doc
        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def _set_content(self, content: list) -> None:
        """Set the content for the Exchange Database subclient.

        Args:
            content: A list containing the subclient content items to be set.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> subclient._set_content(['MailboxDB1', 'MailboxDB2'])
            >>> # The subclient content is now set to the specified databases

        #ai-gen-doc
        """
        temp = []
        for item in content:
            temp.append(
                {
                    "exchangeDBContent": {
                        "databaseName": item,
                        "forceFull": True
                    }
                }
            )

        self._set_subclient_properties("_content", temp)

    def set_exchangedb_subclient_prop(self, key: str, value: object) -> None:
        """Set a property for the Exchange Database subclient.

        This method allows you to update a specific property of the Exchange Database subclient
        by specifying the property key and the value to assign.

        Args:
            key: The name of the property to be changed.
            value: The value to set for the specified property.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> subclient.set_exchangedb_subclient_prop('retentionDays', 30)
            >>> subclient.set_exchangedb_subclient_prop('enableCircularLogging', True)

        #ai-gen-doc
        """
        self._set_subclient_properties(
            "_exchange_db_subclient_prop['{0}']".format(str(key)),
            value
        )

    def _restore_json(self, **kwargs: Any) -> dict:
        """Generate the JSON request payload for the restore API based on user-selected options.

        This method constructs a dictionary representing the restore request, using the provided keyword arguments
        to set specific restore options.

        Args:
            **kwargs: Arbitrary keyword arguments specifying restore options. Each key-value pair represents
                an option to be included in the restore request.

        Returns:
            dict: The JSON request dictionary to be sent to the API.

        Example:
            >>> options = {
            ...     "database_name": "ExchangeDB1",
            ...     "restore_type": "in_place",
            ...     "overwrite": True
            ... }
            >>> json_request = subclient._restore_json(**options)
            >>> print(json_request)
            {'database_name': 'ExchangeDB1', 'restore_type': 'in_place', 'overwrite': True}

        #ai-gen-doc
        """
        self._instance_object._restore_association = self._subClientEntity

        restore_json = self._instance_object._restore_json(**kwargs)

        exchange_options = {
            "exchangeRestoreLogOption": 0,
            "exchangeVersion": {
                "name": "",
                "version": 15
            }
        }

        restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['exchangeOption'] = exchange_options

        return restore_json

    def restore_in_place(self, paths: list, client: object = None) -> object:
        """Perform an in-place restore for the Exchange database subclient.

        This method initiates an in-place restore operation for the specified Exchange database paths.
        Optionally, a specific client object can be provided to target the restore.

        Args:
            paths: List of database paths to restore in place.
            client: Optional; the client object representing the target client for the restore.

        Returns:
            An object representing the Job for the restore operation.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> restore_paths = [r'C:\\ExchangeDB1', r'C:\\ExchangeDB2']
            >>> job = subclient.restore_in_place(restore_paths)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if client is None:
            client = self._client_object
        restore_json = self._restore_json(paths=paths, client=client)

        return self._process_restore_response(restore_json)

    def restore_out_of_place(self, client: str, paths: list) -> 'Job':
        """Run an out-of-place restore for an Exchange database subclient.

        This method initiates a restore operation where the selected Exchange database(s)
        are restored to a different client (destination) than the original source.

        Args:
            client: The name of the destination client where the restore should be performed.
            paths: A list of database paths to be restored out of place.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> restore_job = subclient.restore_out_of_place('DestinationClient', ['/db1', '/db2'])
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """
        restore_json = self._restore_json(paths=paths, client=client)

        return self._process_restore_response(restore_json)

    def create_recovery_point(self, db_name: str, media_agent: str, expiry_days: int = 5) -> int:
        """Create a recovery point for a specified Exchange database.

        This method initiates a job to create a recovery point for the given database
        using the specified media agent. The recovery point will be retained for the
        specified number of days.

        Args:
            db_name: The name of the Exchange database for which to create the recovery point.
            media_agent: The name of the media agent to use for creating the recovery point.
            expiry_days: The number of days to retain the recovery point. Defaults to 5.

        Returns:
            The job ID of the initiated recovery point creation job.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> job_id = subclient.create_recovery_point('MailboxDB01', 'MediaAgent01', expiry_days=7)
            >>> print(f"Recovery point creation job started with ID: {job_id}")

        #ai-gen-doc
        """
        options = {
            'path': db_name,
            'media_agent': media_agent.split('.')[0],
            'subclientId': int(self.subclient_id)
        }

        options = self._backupset_object._prepare_browse_options(options)
        request_json = self._backupset_object._prepare_browse_json(options)

        request_json['advOptions'] = {
            "advConfig": {
                "applicationMining": {
                    "browseInitReq": {
                        "appMinType": 2,
                        "bCreateRecoveryPoint": True,
                        "expireDays": expiry_days
                    },
                    "isApplicationMiningReq": True,
                    "appType": int(self._agent_object._agent_id)
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)

        if flag:
            if response and response.json():
                response = response.json()
                response = response['browseResponses'][0]
                job_id = response['browseResult']['advConfig']['applicationMining']['browseInitResp']['recoveryPointJobID']
                job = Job(self._commcell_object, job_id)
                job.wait_for_completion()
                return job
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')

    def get_session(self, path: str, media_agent: str, edb_paths: dict, recovery_point_ids: dict) -> dict:
        """Retrieve session IDs for a recovery point in an Exchange database.

        Args:
            path: The name of the Exchange database.
            media_agent: The name of the media agent to use for creating the recovery point.
            edb_paths: A dictionary mapping EDB paths to their corresponding job IDs.
            recovery_point_ids: A dictionary mapping job IDs to recovery point IDs (e.g., {97297: 834, 97298: 835}).

        Returns:
            dict: A dictionary containing session IDs associated with the specified recovery points.

        Example:
            >>> subclient = ExchangeDatabaseSubclient()
            >>> edb_paths = {'/db1/edb': 12345, '/db2/edb': 12346}
            >>> recovery_points = {12345: 67890, 12346: 67891}
            >>> sessions = subclient.get_session('MailboxDB01', 'MediaAgent01', edb_paths, recovery_points)
            >>> print(sessions)
            {'/db1/edb': 555, '/db2/edb': 556}

        #ai-gen-doc
        """
        session_ids = {}
        for jobid, edb_path in edb_paths.items():
            options = {
                'path': path,
                'media_agent': media_agent.split('.')[0],
                'subclientId': int(self.subclient_id)
            }
            options = self._backupset_object._prepare_browse_options(options)
            request_json = self._backupset_object._prepare_browse_json(options)
            request_json['session'] = {
            }
            request_json['advOptions'] = {
                "advConfig": {
                    "applicationMining": {
                        "isApplicationMiningReq": True,
                        "appType": int(self._agent_object._agent_id),
                        "browseInitReq": {
                            "bCreateRecoveryPoint": False,
                            "recoveryPointID": recovery_point_ids[jobid],
                            "appMinType": 0,
                            "edbPath": edb_path
                        }
                    }
                }
            }

            flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)

            if flag:
                if response and response.json():
                    response = response.json()
                    response = response['browseResponses'][0]
                    edb = response['browseResult']['advConfig']['applicationMining']['browseInitResp']['edbPath']
                    session_ids[edb] = response['session']['sessionId']
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101')

        return session_ids

    def get_mailbox_tags(self, path: str, media_agent: str, edb_paths: dict, session_ids: dict) -> dict:
        """Retrieve mailbox tags for a recovery point in an Exchange database.

        Args:
            path: The name of the Exchange database.
            media_agent: The name of the media agent to use for creating the recovery point.
            edb_paths: A dictionary mapping EDB file paths to their corresponding job IDs.
            session_ids: A dictionary containing session IDs of recovery point jobs.

        Returns:
            A dictionary where each key is a mailbox identifier and the value is a list or set of associated tags.

        Example:
            >>> edb_paths = {'C:\\ExchangeDB\\db1.edb': 12345}
            >>> session_ids = {'session1': 67890}
            >>> tags = subclient.get_mailbox_tags('DB1', 'MediaAgent01', edb_paths, session_ids)
            >>> print(tags)
            {'mailbox1': ['tag1', 'tag2'], 'mailbox2': ['tag3']}

        #ai-gen-doc
        """
        mailbox_tags = {}
        for jobid, edb_path in edb_paths.items():
            options = {
                'path': path,
                'media_agent': media_agent.split('.')[0],
                'subclientId': int(self.subclient_id)
            }
            options = self._backupset_object._prepare_browse_options(options)
            request_json = self._backupset_object._prepare_browse_json(options)
            request_json['session'] = {
                'sessionId': session_ids[edb_path]
            }
            request_json['advOptions'] = {
                "advConfig": {
                    "applicationMining": {
                        "isApplicationMiningReq": True,
                        "appType": int(self._agent_object._agent_id),
                        "browseReq": {
                            "exMiningReq": {
                                "miningLevel": 0,
                                "edbPath": edb_path
                            }
                        }
                    }
                }
            }
            flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)
            if flag:
                if response and response.json():
                    response = response.json()
                    response = response['browseResponses'][0]
                    response = response['browseResult']['dataResultSet'][0]
                    db_name = response['advancedData']['advConfig']['applicationMining']['browseResp']['exMiningRsp'][
                        'edbPath']
                    mailbox_tags[db_name] = \
                    response['advancedData']['advConfig']['applicationMining']['browseResp']['exMiningRsp'][
                        'mailboxTag']
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101')

        return mailbox_tags

    def run_restore_messages(
            self,
            path: str,
            media_agent: str,
            oop_path: str,
            session_id: dict,
            edb_path: dict,
            mailbox_tags: dict
    ) -> 'Response':
        """Run a restore operation to recover messages from a backup.

        This method initiates a recovery point job for a specified Exchange database backup,
        restoring messages for the given mailbox tags to a PST file at the specified output path.

        Args:
            path: The name of the Exchange database to restore from.
            media_agent: The name of the media agent to use for the recovery point job.
            oop_path: The output path where the PST file will be created.
            session_id: A dictionary containing session IDs of recovery point jobs.
            edb_path: A dictionary mapping EDB paths to their corresponding job IDs.
            mailbox_tags: A dictionary specifying mailbox tags for which the restore should be performed.

        Returns:
            Response: The response object containing the result of the restore operation.

        Example:
            >>> response = subclient.run_restore_messages(
            ...     path="MailboxDB01",
            ...     media_agent="MediaAgent1",
            ...     oop_path="C:/Restores/Output.pst",
            ...     session_id={"job1": 12345},
            ...     edb_path={"edb1": "C:/EDB/edb1.edb"},
            ...     mailbox_tags={"mailbox1": "tag1"}
            ... )
            >>> print(response)
            >>> # The response object contains details about the restore job

        #ai-gen-doc
        """
        options = {
            'path': path,
            'media_agent': media_agent,
            'subclientId': int(self.subclient_id)
        }
        options = self._backupset_object._prepare_browse_options(options)
        request_json = self._backupset_object._prepare_browse_json(options)

        request_json['session'] = {
            'sessionId': session_id
        }
        request_json['advOptions'] = {
            "advConfig": {
                "applicationMining": {
                    "appType": int(self._agent_object._agent_id),
                    "isApplicationMiningReq": True,
                    "browseReq": {
                        "exRestoreReq": {
                            "restoreType": 0,
                            "edbPath": edb_path,
                            "mailboxTag": mailbox_tags,
                            "destLocation": oop_path,
                            "restoreDestType": 0
                        }
                    },
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._BROWSE, request_json)

        if flag:
            if response and response.json():
                response = response.json()
                return response
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101')
