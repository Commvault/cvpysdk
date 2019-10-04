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

from ...subclient import Subclient
from ...exception import SDKException
from ...job import Job

class ExchangeDatabaseSubclient(Subclient):
    """Derived class from the Subclient Base class,
        to perform operations specific to an Exchange Database Subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of Exchange Database subclient.."""
        super(ExchangeDatabaseSubclient, self)._get_subclient_properties()

        self._content = self._subclient_properties.get('content', [])
        self._exchange_db_subclient_prop = self._subclient_properties.get(
            'exchangeDBSubClientProp', {}
        )

    def _get_subclient_properties_json(self):
        """Returns the JSON with the properties for the Subclient, that can be used for a POST
        request to update the properties of the Subclient.

           Returns:
               dict     -   all subclient properties put inside a dict

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
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list    -   list of content added to the subclient

        """
        return self._content

    @content.setter
    def content(self, subclient_content):
        """Update the content of the subclient with the content list given by the user.

            Args:
                subclient_content   (list)  --  list of the content to add to the subclient

            Raises:
                SDKException:
                    if specified input is not a list

                    if failed to update subclient content

        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def _set_content(self, content):
        """Sets the subclient content

            Args:
                content         	(list)      --  list of subclient content

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

    def set_exchangedb_subclient_prop(self, key, value):
        """Sets the exchange DB sublcient properties

            Args:
                key         	(str)       --  property to be changed

                value           (obj)       --  value to be set

        """
        self._set_subclient_properties(
            "_exchange_db_subclient_prop['{0}']".format(str(key)),
            value
        )


    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (dict)  --  dict of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API
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

    def restore_in_place(self, paths, client=None):
        """
         Run inplace restore for Exchange database subclient

         Args:
             paths      (list)   -- list of path used for inplace restore

             client     (object) -- object of client class

        Returns:
            object  -   Job class object for restore job
        """
        if client is None:
            client = self._client_object
        restore_json = self._restore_json(paths=paths, client=client)

        return self._process_restore_response(restore_json)

    def restore_out_of_place(self, client, paths):
        """
         Run out of place restore for Exchange database subclient
            Args:
                client      (str)       -- destination client on which the restore should run

                paths       (list)      -- list of path used for out of place restore

            Returns:
                object  -   Job class object for restore job
        """
        restore_json = self._restore_json(paths=paths, client=client)

        return self._process_restore_response(restore_json)

    def create_recovery_point(self, db_name, media_agent, expiry_days=5):
        """"
        Run a create recovery point job on a backup

            Args:
                db_name            (str)   --  database name

                media_agent        (str)   --  media agent name to create recovery point on

                expiry_days         (int)   --  no of days to keep the recovery point
                                                default : 5

            Returns:
                job     - Job id of recovery point
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


    def get_session(self, path, media_agent, edb_paths, recovery_point_ids):
        """"
        Get session ids for a recovery point

            Args:
                path            (str)   --  database name

                media_agent     (str)   --  media agent name to create recovery point on

                edb_paths       (dict)   --  edb paths with job Ids
                ex: {97297: '\\\\SPVM\\sc_4701_job_97296_1563312295\\1563312295\\Microsoft Information
                Store\\AUTODBx_spvm.VAYU.COMMVAULT.COM\\EDBFILES\\AUTODBx_spvm.VAYU.COMMVAULT.COM.edb
                ', 97298: '\\\\MSE-2013\\sc_4701_job_97296_1563312333\\1563312333\\Microsoft Information St
                ore\\AUTODBx_MSE-2013.VAYU.COMMVAULT.COM\\EDBFILES\\AUTODBx_MSE-2013.VAYU.COMMVAULT.COM.edb'}

                recovery_point_ids (dict)   --  ids of recovery point jobs
                ex: {97297: 834, 97298: 835}
            Returns:
                Sessionids     - dictionary of sessionids
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
                if response and response.json() :
                    response = response.json()
                    response = response['browseResponses'][0]
                    edb = response['browseResult']['advConfig']['applicationMining']['browseInitResp']['edbPath']
                    session_ids[edb] = response['session']['sessionId']
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101')

        return session_ids


    def get_mailbox_tags(self, path, media_agent, edb_paths, session_ids):
        """"
        Get the mailbox tags for a recovery point

            Args:
                path            (str)   --  database name

                media_agent     (str)   --  media agent name to create recovery point on

                edb_paths       (dict)   --  edb paths with job Ids

                session_ids      (dict)   --  sessionIDs of recovery point jobs

            Returns:
                mailboxTags     - dictionary of mailboxes and their tags
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
                    db_name = response['advancedData']['advConfig']['applicationMining']['browseResp']['exMiningRsp']['edbPath']
                    mailbox_tags[db_name] = response['advancedData']['advConfig']['applicationMining']['browseResp']['exMiningRsp']['mailboxTag']
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101')

        return mailbox_tags

    def run_restore_messages(self, path, media_agent, oop_path,
                             session_id, edb_path, mailbox_tags):
        """"
        Run a create recovery point job on a backup

            Args:
                path            (str)   --  database name

                media_agent              (str)   --  media agent name to create recovery point on

                oop_path        (str)   --  path for pst restore

                edb_path       (dict)   --  edb paths with job Ids

                session_id      (dict)   --  sessionIDs of recovery point jobs

                mailbox_tags    (dict)  --  mailbox tags for which restore has to run

            Returns:
                Response
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

