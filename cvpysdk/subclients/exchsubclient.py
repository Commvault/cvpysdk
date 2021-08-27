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

"""File for operating on an Exchange Subclient.

ExchangeSubclient is the only class defined in this file.

ExchangeSubclient:  Derived class from Subclient Base class,  representing an Exchange Mailbox
Agent subclient, and to perform operations on that subclient.

ExchangeSubclient:

    __new__()   --  Method to create object based on the backupset name


"""

from __future__ import unicode_literals

from past.builtins import basestring

from ..client import Client
from ..subclient import Subclient
from ..exception import SDKException


class ExchangeSubclient(Subclient):
    """Derived class from Subclient Base class, representing an Exchange subclient,
        and to perform operations on that subclient.
    """

    def __new__(cls, backupset_object, subclient_name, subclient_id=None):
        """Decides which subclient object needs to be created"""
        from .exchange.usermailbox_subclient import UsermailboxSubclient
        from .exchange.journalmailbox_subclient import JournalMailboxSubclient
        from .exchange.contentstoremailbox_subclient import ContentStoreMailboxSubclient
        backupset_types = {
            "user mailbox": UsermailboxSubclient,
            "journal mailbox": JournalMailboxSubclient,
            "contentstore mailbox": ContentStoreMailboxSubclient
        }

        backupset_name = backupset_object.backupset_name

        if backupset_name in backupset_types:
            subclient_type = backupset_types[backupset_name]
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient for this instance type is not yet implemented'
            )

        return object.__new__(subclient_type)

    @staticmethod
    def _get_client_dict(client_object):
        """Returns the client dict for the client object to be appended to member server.

            Args:
                client_object   (object)    --  instance of the Client class

            Returns:
                dict    -   dictionary for a single client to be associated
        """
        client_dict = {
            "client": {
                "clientName": client_object.client_name,
                "clientId": int(client_object.client_id),
                "_type_": 3
            }
        }

        return client_dict

    def _member_servers(self, clients_list):
        """Returns the proxy clients to be associated .

            Args:
                clients_list (list)    --  list of the clients to associated

            Returns:
                list - list consisting of all member servers to be associated

            Raises:
                SDKException:
                    if type of clients list argument is not list

        """
        if not isinstance(clients_list, list):
            raise SDKException('Subclient', '101')

        member_servers = []

        for client in clients_list:
            if isinstance(client, basestring):
                client = client.strip().lower()

                if self._commcell_object.clients.has_client(client):
                    temp_client = self._commcell_object.clients.get(client)

                    if temp_client.agents.has_agent('exchange mailbox (classic)'):
                        client_dict = self._get_client_dict(temp_client)
                        member_servers.append(client_dict)

                    del temp_client
            elif isinstance(client, Client):
                if client.agents.has_agent('exchange mailbox (classic)'):
                    client_dict = self._get_client_dict(client)
                    member_servers.append(client_dict)

        return member_servers

    def _content_indexing_option_json(self):
        """Getter for  the content indexing options of ContentIndexing JSON"""

        self._content_indexing_option_json_ = {
            "reanalyze": False,
            "selectInactiveMailboxes": False,
            "fileAnalytics": False,
            "subClientBasedAnalytics": False
        }

    def _media_option_json(self, value):
        """Setter for  the media options of ContentIndexing JSON

            Args:
                value   (dict)  --  media option need to be included

            Returns:
                (dict)  -       generated media options JSON

        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._media_option_json_ = {
            "pickFailedItems": value.get("pick_failed_items"),
            "pickFailedItemsOnly": value.get("pick_only_failed_items"),
            "auxcopyJobOption": {
                "maxNumberOfStreams": value.get("streams"),
                "allCopies": True,
                "useMaximumStreams": False,
                "proxies": value.get("proxies")
            }
        }

    def _json_backupset(self):
        """Getter for the Exchange Mailbox backupset option in restore json"""

        self._exchange_backupset_json = {
            "clientName": self._client_object.client_name,
            "backupsetName": self._backupset_object.backupset_name
        }

    def _json_restore_exchange_restore_option(self, value):
        """
            setter for  the Exchange Mailbox in place restore  option in restore json

            Args:
                value   (dict)  --  restore option need to be included

            Returns:
                (dict)  -       generated exchange restore options JSON
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._exchange_option_restore_json = {
            "exchangeRestoreChoice": 1,
            "exchangeRestoreDrive": 1,
            "isJournalReport": value.get("journal_report", False),
            "pstFilePath": "",
            "targetMailBox": value.get("target_mailbox",None)
        }

    def _json_restore_exchange_common_option(self, value):
        """
           Prepare exchange mailbox in place restore common options in restore json

            Args:
                value   (dict)  --  restore common options need to be included

            Returns:
                (dict)  -       generated exchange restore common options JSON
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._exchange_common_option_restore_json = {
            "clusterDBBackedup": False,
            "restoreToDisk": False,
            "restoreDataInsteadOfStub": True,
            "offlineMiningRestore": False,
            "browse": True,
            "skip": False,
            "restoreOnlyStubExists": False,
            "truncateBody": value.get("truncate_body", False),
            "restoreAsStubs": value.get("restore_as_stubs", False),
            "copyToObjectStore": False,
            "onePassRestore": False,
            "collectMsgsLargerThan": value.get("collect_msgs_larger_than", 1024),
            "collectMsgsDaysAfter": value.get("collect_msgs_days_after", 30),
            "unconditionalOverwrite": True,
            "syncRestore": False,
            "leaveMessageBody": value.get("leave_message_body", False),
            "collectMsgWithAttach": value.get("collect_msg_with_attach", False),
            "truncateBodyToBytes": value.get("truncate_body_to_bytes", 0),
            "recoverToRecoveredItemsFolder": False,
            "append": False
        }

        return self._exchange_common_option_restore_json

    def _json_out_of_place_destination_option(self, value):
        """setter for  the Exchange Mailbox out of place restore
        option in restore json

            Args:
                value   (dict)  --  restore option need to be included

            Returns:
                (dict)  -       generated exchange restore options JSON

        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._out_of_place_destination_json = {
            "inPlace": False,
            "destPath": [value.get("destination_path")],
            "destClient": {
                "clientId": int(self._client_object.client_id),
                "clientName": self._client_object.client_name
            },
        }

    def _json_disk_restore_exchange_restore_option(self, value):
        """Setter for  the Exchange Mailbox Disk restore option
        in restore json

            Args:
                value   (dict)  --  restore option need to be included

            Returns:
                (dict)  -       generated exchange restore options JSON

        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._exchange_disk_option_restore_json = {
            "exchangeRestoreChoice": 3,
            "exchangeRestoreDrive": 1,
            "diskFilePath": value.get("destination_path"),
            "isJournalReport": value.get("journal_report", False),
            "pstFilePath": ""
        }

    def _json_pst_restore_exchange_restore_option(self, value):
        """Setter for  the Exchange Mailbox PST restore option in restore json
            Args:
                value   (dict)  --  restore option need to be included

            Returns:
                (dict)  -       generated exchange restore options JSON

        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._exchange_pst_option_restore_json = {
            "exchangeRestoreChoice": 2,
            "exchangeRestoreDrive": 1,
            "isJournalReport": value.get("journal_report", False),
            "pstFilePath": value.get("destination_path"),
            "pstRestoreOption": value.get("limit_pst_size", 0),
            "pstSize": value.get("pst_size", 2048)
        }

    @property
    def _json_content_indexing_subtasks(self):
        """Getter for the contentindexing subtask in restore JSON.
        It is read only attribute"""

        _subtask_restore_json = {
            "subTaskType": 1,
            "operationType": 5020
        }

        return _subtask_restore_json

    def _prepare_pst_restore_json(self, _pst_restore_option=None):
        """
        Prepare PST retsore Json with all getters

        Args:
            _pst_restore_option - dictionary with all PST restore options

            value:
                paths                   (list)  --  list of paths of mailboxes/folders to restore

                destination_client              --  client where the mailboxes needs to be restored
                destination_path                --  PST path where the mailboxes needs to be
                                                    restored
                unconditional_overwrite (bool)  --  unconditional overwrite files during restore
                    default: True
                journal_report          (bool)  --  Journal report is true for journal and
                                                    contentStore Mailbox
                    default: False

        returns:
            request_json   -- complete json for performing PST Restore options
        """

        if _pst_restore_option is None:
            _pst_restore_option = {}

        paths = self._filter_paths(_pst_restore_option['paths'])
        self._json_pst_restore_exchange_restore_option(_pst_restore_option)
        self._json_backupset()

        _pst_restore_option['paths'] = paths

        # set the setters
        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_pst_restore_option)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions'][
                'exchangeOption'] = self._exchange_pst_option_restore_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["browseOption"]['backupset'] = self._exchange_backupset_json

        return request_json

    def _prepare_disk_restore_json(self, _disk_restore_option):
        """
        Prepare disk retsore Json with all getters

        Args:
            _disk_restore_option - dictionary with all disk restore options

            value:
                paths                   (list)  --  list of paths of mailboxes/folders to restore

                destination_client              --  client where the mailboxes needs to be restored
                destination_path                --  path where the mailboxes needs to be restored
                unconditional_overwrite (bool)  --  unconditional overwrite files during restore
                    default: True
                journal_report          (bool)  --  Journal report is true for journal and
                                                    contentStore Mailbox
                    default: False


        returns:
            request_json        -complete json for performing disk Restore options
        """

        if _disk_restore_option is None:
            _disk_restore_option = {}

        paths = self._filter_paths(_disk_restore_option['paths'])
        self._json_disk_restore_exchange_restore_option(_disk_restore_option)
        self._json_backupset()
        _disk_restore_option['paths'] = paths

        # set the setters
        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_disk_restore_option)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions'][
                'exchangeOption'] = self._exchange_disk_option_restore_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["browseOption"]['backupset'] = self._exchange_backupset_json

        return request_json

    def _prepare_out_of_place_restore_json(self, _restore_option):
        """
        Prepare out of place retsore Json with all getters

        Args:
            _restore_option - dictionary with all out of place restore options

            value:
                paths                   (list)  --  list of paths of mailboxes/folders to restore

                destination_client              --  client where the mailboxes needs to be restored
                destination_path                --  path where the mailboxes needs to be restored
                unconditional_overwrite (bool)  --  unconditional overwrite files during restore
                    default: True
                journal_report          (bool)  --  Journal report is true for journal and
                                                    contentStore Mailbox
                    default: False


        returns:
            request_json        -  complete json for performing disk Restore options

        """

        if _restore_option is None:
            _restore_option = {}

        paths = self._filter_paths(_restore_option['paths'])
        self._json_restore_exchange_restore_option(_restore_option)
        self._json_out_of_place_destination_option(_restore_option)
        self._json_backupset()
        _restore_option['paths'] = paths

        # set the setters
        self._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_restore_option)

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions'][
                'exchangeOption'] = self._exchange_option_restore_json

        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions'][
                'destination'] = self._out_of_place_destination_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["browseOption"]['backupset'] = self._exchange_backupset_json

        return request_json

    def _cleanup_json(self):
        """Returns the JSON request to pass to the API as per the options selected by the user.
            Returns:
                dict - JSON request to pass to the API

        """
        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": self._json_backup_subtasks,
                        "options": {
                            "backupOpts": {
                                "backupLevel": 15
                            }
                        }
                    }
                ]
            }
        }

        return request_json

    def cleanup(self):
        """Runs a cleanup job for the subclient .

            Returns:
                object - instance of the Job class for this backup job

        """

        request_json = self._cleanup_json()
        return self._process_restore_response(request_json)

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            journal_report=False,
            restore_as_stub=None,
            recovery_point_id=None):
        """Restores the mailboxes/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of paths of mailboxes/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True
                journal_report          (bool)  --  Journal report is true for journal and
                                                        contentStore Mailbox
                    default: False

                restore_as_stub         (dict)  --  setters for common options

                recovery_point_id       (int)   --  ID of the recovery point to which the mailbox is to be restored to
                    Default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        restore_option = {}
        if paths == []:
            raise SDKException('Subclient', '104')
        restore_option['journal_report'] = journal_report

        paths = self._filter_paths(paths)
        self._json_restore_exchange_restore_option(restore_option)
        self._json_backupset()
        restore_option['unconditional_overwrite'] = overwrite
        restore_option['paths'] = paths

        request_json = self._restore_json(restore_option=restore_option)
        request_json['taskInfo']['associations'][0]['subclientName'] = self.subclient_name
        request_json['taskInfo']['associations'][0][
            'backupsetName'] = self._backupset_object.backupset_name
        request_json['taskInfo']['subTasks'][0][
            'options']['restoreOptions']['exchangeOption'] = self._exchange_option_restore_json
        if restore_as_stub:
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'commonOptions'] = self._json_restore_exchange_common_option(restore_as_stub)

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["browseOption"]['backupset'] = self._exchange_backupset_json

        if recovery_point_id is not None:
            request_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]['exchangeOption']["recoveryPointId"] = recovery_point_id

        return self._process_restore_response(request_json)

    def out_of_place_restore(
            self,
            paths,
            destination_path,
            overwrite=True,
            journal_report=False):
        """Restores the mailboxes/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of paths of mailboxes/folders to restore
                destination_client              --  client where the mailboxes needs to be restored
                destination_path                --  path where the mailboxes needs to be restored

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True
                journal_report          (bool)  --  Journal report is true for journal and
                                                    contentStore Mailbox
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

        restore_option = {}
        if paths == []:
            raise SDKException('Subclient', '104')
        restore_option['journal_report'] = journal_report
        restore_option['unconditional_overwrite'] = overwrite
        restore_option['paths'] = paths
        # restore_option['client'] = destination_client
        restore_option['destination_path'] = destination_path
        oop_target_mailbox = destination_path.split(chr(18))[0].split("\\MB\\")[1]
        restore_option['target_mailbox'] = oop_target_mailbox
        request_json = self._prepare_out_of_place_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def disk_restore(
            self,
            paths,
            destination_client,
            destination_path,
            overwrite=True,
            journal_report=False):
        """Restores the mailboxes/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of paths of mailboxes/folders to restore
                destination_client              --  client where the mailboxes needs to be restored
                destination_path                --  path where the mailboxes needs to be restored

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True
                journal_report          (bool)  --  Journal report is true for journal and
                                                    contentStore Mailbox
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

        restore_option = {}
        if paths == []:
            raise SDKException('Subclient', '104')
        restore_option['journal_report'] = journal_report
        restore_option['unconditional_overwrite'] = overwrite
        restore_option['paths'] = paths
        restore_option['client'] = destination_client
        restore_option['destination_path'] = destination_path

        request_json = self._prepare_disk_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def pst_restore(
            self,
            paths,
            destination_client,
            pst_path,
            overwrite=True,
            journal_report=False):
        """Restores the Mailbox/Emails specified in the input paths list to the PST PATH location.

            Args:
                paths                   (list)  --  list of paths of mailboxes/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True
                journal_report          (bool)  --  Journal report is true for journal and
                                                    contentStore Mailbox
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

        restore_option = {}
        if paths == []:
            raise SDKException('Subclient', '104')
        restore_option['journal_report'] = journal_report
        restore_option['unconditional_overwrite'] = overwrite
        restore_option['paths'] = paths
        restore_option['client'] = destination_client
        restore_option['destination_path'] = pst_path

        request_json = self._prepare_pst_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def pst_ingestion(self):
        """Runs a backup job for the subclient of the level specified.
            Returns:
                object - instance of the Job class for this backup job

        """

        payload_dict = {
            "taskInfo":{
                "associations":[self._subClientEntity],
                "task": self.get_pst_task_json(),
                "subTasks":[{
                    "subTaskOperation":1,
                    "subTask":{
                        "subTaskType":2,
                        "operationType":5024
                    },
                    "options":{
                        "backupOpts":self.get_pst_backup_opt_json(),
                        "adminOpts":{
                            "contentIndexingOption":{
                                "subClientBasedAnalytics":False
                            }
                        },
                        "restoreOptions":{
                            "virtualServerRstOption":{
                                "isBlockLevelReplication":False
                            }
                        }
                    }
                }]
            }
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._commcell_object._services["RESTORE"], payload_dict)

        return self._process_backup_response(flag, response)

    def subclient_content_indexing(self,
                                   pick_failed_items=False,
                                   pick_only_failed_items=False,
                                   streams=4,
                                   proxies=None):
        """Run content Indexing on Subclient .

            Args:
               pick_failed_items
                        default:False   (bool)  --  Pick fail items during Content Indexing

                pick_only_failed_items  (bool)  --  Pick only fail items items during Content
                                                    Indeixng
                    default: False

                streams                 (int)   --  Streams for Content Indexing job

                    default: 4

                proxies                 (list) --  provide the proxies to run CI
                    default: None

            Returns:
                object - instance of the Job class for this ContentIndexing job

        """
        # check if inputs are correct

        ci_option = {}
        if not (isinstance(pick_failed_items, bool) and
                isinstance(pick_only_failed_items, bool)):
            raise SDKException('Subclient', '101')

        ci_option['pick_failed_items'] = pick_failed_items
        ci_option['pick_only_failed_items'] = pick_only_failed_items
        ci_option['streams'] = streams
        if proxies is None:
            ci_option['proxies'] = {}
        else:
            member_servers = self._member_servers(proxies)
            ci_option['proxies'] = {
                "memberServers": member_servers
            }

        self._media_option_json(ci_option)
        self._content_indexing_option_json()
        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": self._json_content_indexing_subtasks,
                        "options": {
                            "backupOpts": {
                                "mediaOpt": self._media_option_json_
                            },
                            "adminOpts": {
                                "contentIndexingOption": self._content_indexing_option_json_
                            },
                            "restoreOptions": {
                                "virtualServerRstOption": {
                                    "isBlockLevelReplication": False
                                },
                                "browseOption": {
                                    "backupset": {}
                                }
                            }
                        }
                    }
                ]
            }
        }

        return self._process_restore_response(request_json)

    def get_pst_task_json(self):
        """Get task json for pst ingestion job

            Returns:
                 Pst task json
        """
        task_json = {
            "ownerId": self._commcell_object.users.all_users[
                self._commcell_object.commcell_username],
            "taskType": 1,
            "ownerName": self._commcell_object.commcell_username,
            "sequenceNumber": 0,
            "initiatedFrom": 1,
            "policyType": 0,
            "taskId": 0,
            "taskFlags": {
                "isEZOperation": False, "disabled": False
            }
        }
        return task_json

    def get_pst_backup_opt_json(self):
        """Get backup options json for pst ingestion job

            Returns:
                 Pst backup options json
        """
        backup_opt_json = {
            "truncateLogsOnSource": False,
            "sybaseSkipFullafterLogBkp": False,
            "notSynthesizeFullFromPrevBackup": False,
            "backupLevel": 2,
            "incLevel": 1,
            "adHocBackup": False,
            "runIncrementalBackup": False,
            "isSpHasInLineCopy": False,
            "runSILOBackup": False,
            "doNotTruncateLog": False,
            "exchOnePassOptions": {
                "proxies": {}
            },
            "dataOpt": self.get_pst_data_opt_json(),
            "mediaOpt": {}
        }
        return backup_opt_json

    def get_pst_data_opt_json(self):
        """Get data options json for pst ingestion job

            Returns:
                 Pst data options json
        """
        data_json = {
            "skipCatalogPhaseForSnapBackup": True,
            "useCatalogServer": False,
            "followMountPoints": True,
            "enforceTransactionLogUsage": False,
            "skipConsistencyCheck": False,
            "createNewIndex": False
        }
        return data_json
