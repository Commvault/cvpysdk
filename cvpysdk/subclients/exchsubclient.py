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

    _prepare_attachment_json() -- Method to prepare the requestJSON for attachment restore

    _get_attachment() -- Method to get the content of the attachment

    _get_attachment_preview() -- Method to get the preview content of all the attachments in the attachment list

    preview_backedup_file -- Method to get the preview content of the mail

    _get_ad_group_backup_task_json -- Get AD Group back task json

    ad_group_backup -- Run AD Group backup

    _get_ad_group_backup_subtask_json -- Gets the subtask json for ad group backup

    _get_ad_group_backup_options_json -- Gets the option json for ad group backup

    _get_ad_group_backup_backupoptions_json -- Gets the backup option json for ad group backup


"""

from __future__ import unicode_literals
import re
from ..client import Client
from ..subclient import Subclient
from ..exception import SDKException
from .exchange.constants import JobOptionKeys, JobOptionValues, JobOptionIntegers, ExchangeConstants



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
            if isinstance(client, str):
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

    def _json_job_option_items(self, value):
        """
        Generates JSON for job options.
        Args:
            value (dict): Dictionary containing job options.
        Returns:
            dict: JSON representation of job options.
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        additional_options = []
        message_exist = value.get("if_message_exists", JobOptionValues.SKIP.value)
        stub_rehydration = value.get('stub_rehydration', JobOptionValues.DISABLED.value)
        include_deleted_items = value.get('include_deleted_items', JobOptionValues.DISABLED.value)
        match_destination_user = value.get('match_destination_user', JobOptionValues.DISABLED.value)
        stub_rehydration_option = value.get('stub_rehydration_option',
                                            JobOptionValues.RECOVER_STUBS.value)
        email_level_reporting = value.get('email_level_reporting', JobOptionValues.DISABLED.value)
        old_link = value.get('old_recall_link', None)
        new_link = value.get('new_recall_link', None)

        self._job_option_items_json = [
            {"option": JobOptionKeys.RESTORE_DESTINATION.value, "value": JobOptionValues.EXCHANGE.value},
            {"option": JobOptionKeys.DESTINATION.value, "value": JobOptionValues.ORIGINAL_LOCATION.value},
            {"option": JobOptionKeys.IF_MESSAGE_EXISTS.value, "value": message_exist},
            {"option": JobOptionKeys.INCLUDE_DELETED_ITEMS.value, "value": include_deleted_items},
            {"option": JobOptionKeys.MATCH_DESTINATION_USER.value, "value": match_destination_user},
            {"option": JobOptionKeys.STUB_REHYDRATION.value, "value": stub_rehydration},
        ]

        if stub_rehydration != JobOptionValues.DISABLED.value:
            if stub_rehydration_option == JobOptionValues.RECOVER_STUBS.value:
                additional_options = []
            elif stub_rehydration_option == JobOptionValues.STUB_REPORTING.value:
                additional_options = [
                    {"option": JobOptionKeys.MAILBOX_LEVEL_REPORTING.value, "value": JobOptionValues.ENABLED.value},
                    {"option": JobOptionKeys.EMAIL_LEVEL_REPORTING.value, "value": email_level_reporting},
                ]
            elif stub_rehydration_option == JobOptionValues.UPDATE_RECALL_LINK.value:
                additional_options = [
                    {"option": JobOptionKeys.OLD_RECALL_LINK.value, "value": old_link},
                    {"option": JobOptionKeys.NEW_RECALL_LINK.value, "value": new_link},
                ]

        if additional_options:
            self._job_option_items_json.extend(additional_options)

        self._job_option_items_json.append({
            "option": JobOptionKeys.STUB_REHYDRATION_OPTION.value,
            "value": stub_rehydration_option
        })

        return self._job_option_items_json

    def _exchange_option_restore_json_rehydration(self, value):
        """
        Generates JSON for Exchange restore rehydration options.
        Args:
            value (dict): Dictionary containing rehydration options.
        Returns:
            dict: JSON representation of rehydration options.
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        mapping = {
            JobOptionValues.RECOVER_STUBS.value: JobOptionIntegers.RECOVER_STUBS.value,
            JobOptionValues.STUB_REPORTING.value: JobOptionIntegers.STUB_REPORTING.value,
            JobOptionValues.UPDATE_RECALL_LINK.value: JobOptionIntegers.UPDATE_RECALL_LINK.value
        }

        stub_rehydration_option = mapping.get(
            value.get('stub_rehydration_option', JobOptionValues.RECOVER_STUBS.value)
        )

        email_level_reporting = value.get('email_level_reporting', JobOptionValues.DISABLED.value)
        old_link = value.get('old_recall_link', None)
        new_link = value.get('new_recall_link', None)

        base = {
            JobOptionKeys.STUB_REHYDRATION.value: True,
            JobOptionKeys.STUB_REHYDRATION_OPTION.value: stub_rehydration_option
        }

        additional_options = {}
        if stub_rehydration_option == JobOptionIntegers.RECOVER_STUBS.value:
            additional_options = {}
        elif stub_rehydration_option == JobOptionIntegers.STUB_REPORTING.value:
            additional_options = {
                "stubReportOption": {
                    "messageLevelReport": email_level_reporting == JobOptionValues.ENABLED.value,
                    "mailboxLevelReport": True
                }
            }
        elif stub_rehydration_option == JobOptionIntegers.UPDATE_RECALL_LINK.value:
            additional_options = {
                "stubOldRecallLink": old_link,
                "stubRecallLink": new_link
            }

        base.update(additional_options)

        self._json_exchange_options = {
            JobOptionKeys.EXCHANGE_RESTORE_CHOICE.value: JobOptionIntegers.EXCHANGE_RESTORE_CHOICE.value,
            JobOptionKeys.EXCHANGE_RESTORE_DRIVE.value: JobOptionIntegers.EXCHANGE_RESTORE_DRIVE.value,
            JobOptionKeys.IS_JOURNAL_REPORT.value: value.get("journal_report", False),
            JobOptionKeys.PST_FILE_PATH.value: "",
            JobOptionKeys.TARGET_MAILBOX.value: value.get("target_mailbox", None),
            JobOptionKeys.STUB_REHYDRATION.value: base
        }

        return self._json_exchange_options

    def _browse_filter_xml(self, value):
        """
        Generates an XML query for browsing with a filter.
        Args:
            value (dict): Dictionary containing the filter value with the key 'keyword'.
        Returns:
            str: XML query string for the filter.
        """
        xml_query = f"""<?xml version='1.0' encoding='UTF-8'?>
        <databrowse_Query type="0" queryId="0" isFacet="1">
            <whereClause connector="0">
                <criteria field="29">
                    <values val="{value["keyword"]}"/>
                </criteria>
            </whereClause>
        </databrowse_Query>"""
        return xml_query

    def _request_json_search_in_restore(self, filters):
        """
        Generates a JSON request for searching within a restore operation.
        Args:
            filters (dict): Dictionary containing the search filter parameters.
                               Expected keys are 'keyword' and 'appID'.
        Returns:
            dict: JSON request for the search operation.
        """
        req_json = ExchangeConstants.SEARCH_IN_RESTORE_PAYLOAD
        req_json["advSearchGrp"]["cvSearchKeyword"]["keyword"] = filters.get("keyword", "")
        req_json["advSearchGrp"]["galaxyFilter"][0]["appIdList"] = filters.get("appID", [])
        return req_json

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
            recovery_point_id=None,
            **kwargs):
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

                **kwargs:
                Expected:
                stub_rehydration        (dict)  --  stub rules to rehydrate items during restore
                    Default: None

                filters                  (dict)  --  filter values for find and restore
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

        stub_rehydration = kwargs.get("stub_rehydration")
        if stub_rehydration:
            request_json['taskInfo']['subTasks'][0]['options']['commonOpts'][
                'jobOptionItems'] = self._json_job_option_items(stub_rehydration)
            request_json['taskInfo']['subTasks'][0][
                'options']['restoreOptions']['exchangeOption'] = self._exchange_option_restore_json_rehydration(stub_rehydration)

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["browseOption"]['backupset'] = self._exchange_backupset_json

        if recovery_point_id is not None:
            request_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]['exchangeOption']["recoveryPointId"] = recovery_point_id

        filters = kwargs.get("filters")
        if filters:
            if (filters.get("restore_all_matching")):
                request_json["taskInfo"]["subTasks"][0]["options"][
                    "restoreOptions"]["exchangeOption"]["restoreAllMatching"] = filters.get("restore_all_matching",
                                                                                           False)
                request_json["taskInfo"]["subTasks"][0]["options"][
                    "restoreOptions"]["fileOption"]["browseFilters"] = [self._browse_filter_xml(filters)]
            if (filters.get("restore_selected_items")):
                req = self._request_json_search_in_restore(filters)
                result = self._process_search_response(req)
                request_json["taskInfo"]["subTasks"][0]["options"][
                    "restoreOptions"]["fileOption"]["sourceItem"] = result

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

    def _prepare_attachment_json(self, metadata, attachment_id):
        """Prepare the JSON for the attachment files with the options provided.
            Args:
                metadata    (dict)  --  metadata of the mail
                attachment_id(str)  --  attachment id of the file
            Returns:
                dict - JSON request to pass to the API

        """

        request_json = {
            "filters": [
                {
                    "field": "CLIENT_ID",
                    "fieldValues": {
                        "values": [
                            str(self._get_client_dict(self._client_object)["client"]["clientId"])
                        ]
                    }
                },
                {
                    "field": "SUBCLIENT_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["subclient"]["applicationId"])
                        ]
                    }
                },
                {
                    "field": "APP_TYPE",
                    "fieldValues": {
                        "values": [
                            "137"
                        ]
                    }
                },
                {
                    "field": "CONTENTID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["browseMetaData"]["indexing"]["objectGUID"])
                        ]
                    }
                },
                {
                    "field": "ATTACHMENTID",
                    "fieldValues": {
                        "values": [
                            attachment_id
                        ]
                    }
                },
                {
                    "field": "CV_TURBO_GUID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["browseMetaData"]["indexing"]["objectGUID"])
                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["archiveFileId"])
                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_OFFSET",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["offset"])
                        ]
                    }
                },
                {
                    "field": "COMMCELL_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["advConfig"]["browseAdvancedConfigResp"][
                                    "commcellNumber"])
                        ]
                    }
                },
                {
                    "field": "ITEM_SIZE",
                    "fieldValues": {
                        "values": [
                            str(metadata["size"])
                        ]
                    }
                }
            ]
        }
        return request_json

    def _get_attachment(self,metadata,attachmentId):
        """Get the content of the attachment file with the options provided.
            Args:
                metadata    (dict)  --  metadata of the mail
                attachmentId(str)  --  attachment id of the file
            Returns:
                str - content of the attachment file (html content)
        """

        request_json = self._prepare_attachment_json(metadata,attachmentId)
        self._GET_VARIOUS_PREVIEW = self._services['GET_VARIOUS_PREVIEW']
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._GET_VARIOUS_PREVIEW, request_json)

        if flag:
            return response.text
        else:
            raise SDKException('Subclient', '102', self._update_response_(response.text))


    def _get_attachment_preview(self, attachments, metadata):
        """
        Get the preview content of all the attachments in the attachment list
        Args:
            attachments (list)  --  list of attachments
            metadata    (dict)  --  metadata of the mail

        Returns:
            dict - dictionary with attachment name as key and content as value

        """
        attachments_preview = {}
        pattern = re.compile(r'attId=([^&]+)')
        for attachment in attachments:
            match = pattern.search(attachment['ciPreviewLink']).group(1)
            attachments_preview[attachment['name']] = self._get_attachment(metadata, match)
        return attachments_preview

    def preview_backedup_file(self, file_path):
        """Gets the preview content for the subclient.

            Params:
                file_path (str)  --  path of the file for which preview is needed

            Returns:
                html   (str)   --  html content of the preview

            Raises:
                SDKException:
                    if file is not found

                    if response is empty

                    if response is not success
        """
        self._GET_PREVIEW_CONTENT = self._services['GET_PREVIEW']
        metadata = self._get_preview_metadata(file_path)
        if metadata is None:
            raise SDKException('Subclient', '123')

        if metadata["type"] != "File":
            raise SDKException('Subclient', '124')

        if metadata["size"] == 0:
            raise SDKException('Subclient', '125')

        if metadata["size"] > 20 * 1024 * 1024:
            raise SDKException('Subclient', '126')
        request_json = {
            "filters": [
                {
                    "field": "CLIENT_ID",
                    "fieldValues": {
                        "values": [
                            str(self._get_client_dict(self._client_object)["client"]["clientId"])
                        ]
                    }
                },
                {
                    "field": "SUBCLIENT_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["subclient"]["applicationId"])
                        ]
                    }
                },
                {
                    "field": "CONTENTID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["browseMetaData"]["indexing"]["objectGUID"])
                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["archiveFileId"])
                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_OFFSET",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["offset"])
                        ]
                    }
                },
                {
                    "field": "COMMCELL_NUMBER",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["advConfig"]["browseAdvancedConfigResp"][
                                            "commcellNumber"])
                        ]
                    }
                },
                {
                    "field": "ITEM_SIZE",
                    "fieldValues": {
                        "values": [
                            str(metadata["size"])
                        ]
                    }
                },
                {
                    "field": "ITEM_PATH",
                    "fieldValues": {
                        "values": [
                            file_path
                        ]
                    }
                }
            ]
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._GET_PREVIEW_CONTENT, request_json)

        if flag:
            if "Preview not available" not in response.text:
                response =  response.json()
            else:
                raise SDKException('Subclient', '127')
        else:
            raise SDKException('Subclient', '102', self._update_response_(response.text))

        result = ""
        attachments = response["attachments"]
        del response["attachments"]
        for key in response:
            result += key + " : " + str(response[key]) + "\n"
        # If mail has attachments we add the content of the attachments
        if len (attachments) != 0:
            attachments_preview = self._get_attachment_preview(attachments, metadata)
            result += "Attachments:\n"
            for file in attachments_preview:
                result += file + " : " + attachments_preview[file] + "\n"
        return result

    @staticmethod
    def _get_ad_group_backup_common_opt_json(ad_group_name):
        """
            Gets the common options json for ad group backup
            Args:
                ad_group_name(str):     Name of ad group
            Return:
                Common options for da group backup
        """
        return {
            "notifyUserOnJobCompletion": False,
            "jobMetadata": [
                {
                    "selectedItems": [
                        {
                            "itemName": ad_group_name,
                            "itemType": "AD group"
                        }
                    ],
                    "jobOptionItems": [
                        {
                            "option": "Total running time",
                            "value": "Disabled"
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def _get_ad_group_backup_backupoptions_json(ad_group_name):
        """
            Gets the backup options json for ad group backup
            Args:
                ad_group_name(str):     Name of ad group
            Returns:
                Backup options json for ad group backup
        """
        return {
            "backupLevel": 2,
            "incLevel": 1,
            "exchOnePassOptions": {
                "adGroups": [
                    {
                        "adGroupName": ad_group_name
                    }
                ]
            },
            "dataOpt": {
                "useCatalogServer": False,
                "followMountPoints": True,
                "enforceTransactionLogUsage": False,
                "skipConsistencyCheck": True,
                "createNewIndex": False
            }
        }

    @staticmethod
    def _get_ad_group_backup_options_json(ad_group_name):
        """
            Get options json for ad group backup
            Args:
                ad_group_name(str):     Name of ad group
            Returns:
                options json for ad group backup
        """
        return {
            "backupOpts": ExchangeSubclient._get_ad_group_backup_backupoptions_json(ad_group_name),
            "commonOpts": ExchangeSubclient._get_ad_group_backup_common_opt_json(ad_group_name)
        }

    @staticmethod
    def _get_ad_group_backup_subtask_json(ad_group_name):
        """
            Gets the subtask json for ad group backup
            Args:
                ad_group_name(str):     Name of ad group
            Returns:
                Sub task json for ad group backup
        """
        sub_task_json = [{
            "subTask": {
              "subTaskType": 2,
              "operationType": 2
            },
            "options": ExchangeSubclient._get_ad_group_backup_options_json(ad_group_name)
        }]
        return sub_task_json

    def _get_ad_group_backup_task_json(self, ad_group_name):
        """
            Gets the task json for ad group backup
            Args:
                ad_group_name(str):     Name of ad group
            Returns:
                Task json for ad group backup
        """
        task_json = {
            "associations": [self._subClientEntity],
            "task": {"taskType": 1},
            "subTasks": ExchangeSubclient._get_ad_group_backup_subtask_json(ad_group_name)
        }
        return task_json
    
    def ad_group_backup(self, ad_group_name):
        """
            Run backup of AD Group
            Args:
                ad_group_name(str):     Name of ad group
            Returns:
                Processed job
        """
        task_json = self._get_ad_group_backup_task_json(ad_group_name)
        create_task = self._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task, task_json
        )
        return self._process_backup_response(flag, response)
