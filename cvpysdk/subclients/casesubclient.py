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

"""File for operating on an CaseManger Subclient.

CaseMangerSubclient is the only class defined in this file.

CaseMangerSubclient:  Derived class from Subclient Base class, representing an Exchange Mailbox
Agent subclient, and to perform operations on that subclient.

CaseMangerSubclient:

    __new__()   --  Method to create object based on the backupset name

"""

from __future__ import unicode_literals

from cvpysdk.subclient import Subclient
from cvpysdk.exception import SDKException


class CaseSubclient(Subclient):
    """Derived class from Subclient Base class, representing an Case Manger subclient,
        and to perform operations on that subclient.

    """

    def _case_definition_request(self, defination_json):
        """Runs the case defination ass API to add definition for case

            Args:
                defination_json    (dict)  -- request json sent as payload

            Returns:
                (str, str):
                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        _CASE_DEFINITION = self._commcell_object._services['CASEDEFINITION']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', _CASE_DEFINITION, defination_json
        )

        if flag:
            try:
                if response.json():
                    if 'cmDef' not in response.json():
                        error_message = response.json()['errorMessage']
                        output_string = 'Failed to add defination\nError: "{0}"'
                        raise SDKException(
                            'Subclient', '102', output_string.format(error_message)
                        )
                    else:
                        self.refresh()
            except ValueError:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def json_hold_info(self):
        """Getter for the hold_info JSON."""

        hold_type_dict = {
            'user mailbox': 1,
            'journal mailbox': 2,
            'contentstore mailbox': 3
        }
        self._hold_info_ = [
            {
                "subclientId": int(self.subclient_id),
                "holdName": self._backupset_object.backupset_name,
                "appName": "Exchange Mailbox",
                "holdType": hold_type_dict[self._backupset_object.backupset_name.lower()]
            },
        ]
        return self._hold_info_

    @property
    def json_search_request(self):
        """Getter for the search request JSON."""

        self._search_request_ = {
            "advSearchGrp": {
                'emailFilter': self._filter_list
            },
            "searchProcessingInfo": {
                "queryParams": [
                    {
                        "param": "LANGUAGE",
                        "value": "ENGLISH"
                    }
                ]
            }
        }

        return self._search_request_

    @property
    def json_index_copy_options(self):
        """Getter for the index copy options JSON."""

        self._index_copy_option_json_ = {
            "adminOpts": {
                "caseMgrOptions": {
                    "type": 1
                }
            },
        }

        return self._index_copy_option_json_

    @property
    def json_data_copy_subtasks(self):
        """Getter for the data copy subtask JSON."""

        self._subtask_data_copy_json_ = {
            "subTaskType": 2,
            "operationType": 2
        }

        return self._subtask_data_copy_json_

    @property
    def json_data_copy_options(self):
        """Getter for the data copy options JSON."""

        self._data_copy_option_json_ = {
            "backupOpts": {
                "caseMgrOptions": {
                    "type": 2
                }
            },
        }

        return self._data_copy_option_json_

    @property
    def json_index_copy_subtasks(self):
        """Getter for the index copy subtask in JSON"""

        self._subtask_index_copy_json_ = {
            "subTaskType": 1,
            "operationType": 5023
        }

        return self._subtask_index_copy_json_

    @property
    def json_content_indexing_subtasks(self):
        """Getter for the contentindexing subtask JSON"""

        self._subtask_content_indexing_json_ = {

            "subTaskType": 1,
            "operationType": 5020
        }

        return self._subtask_content_indexing_json_

    @property
    def json_media_options(self):
        """Getter for the contentindexing media options JSON."""

        self._media_options_json_ = {
            "auxcopyJobOption": {
                "maxNumberOfStreams": 6,
                "allCopies": True,
                "useMaximumStreams": False,
            }
        }

        return self._media_options_json_

    def _index_copy_json(self):
        """Prepare Index copy Job Json with all getters

        returns:
            request_json   -- completed json for performing index copy

        """
        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTask": self.json_index_copy_subtasks,
                        "options": self.json_index_copy_options
                    }
                ]
            }
        }

        return request_json

    def _data_copy_json(self):
        """Prepare data copy Job Json with all getters

        returns:
            request_json   -- completed json for performing Data copy

        """
        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {

                        "subTask": self.json_data_copy_subtasks,
                        "options": self.json_data_copy_options

                    }
                ]
            }
        }

        return request_json

    def _prepare_email_filter_list(self, options):
        """Prepare Email filter list
            Args:
                options  (dict)  --  filter options for case

        """

        filers_list = []
        for item in options.get('filters'):

            filter_json = {
                "field": item.get('field'),
                "intraFieldOp": item.get('intraFieldOp', 0),
                "fieldValues": {
                    "values": item.get('values', [])
                }
            }
            filers_list.append(filter_json)

        self._filter_list = [
            {
                "interGroupOP": options.get('interGroupOP', 2),
                "filter": {
                    "interFilterOP": options.get('interGroupOP', 2),
                    "filters": filers_list
                }
            }
        ]

    def index_copy(self):
        """Runs a Index Copy job for the subclient .

            Returns:
                object - instance of the Job class for this index copy job

        """

        request_json = self._index_copy_json()
        return self._process_restore_response(request_json)

    def data_copy(self):
        """Runs a data copy job for the subclient .

            Returns:
                object - instance of the Job class for this data copy job

        """

        request_json = self._data_copy_json()
        return self._process_restore_response(request_json)

    def content_indexing(self):
        """Run content Indexing on Subclient .

            Returns:
                object - instance of the Job class for this ContentIndexing job

        """

        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTask": self.json_content_indexing_subtasks,
                        "options": {
                            "backupOpts": {
                                "mediaOpt": self.json_media_options
                            }
                        }
                    }
                ]
            }
        }

        return self._process_restore_response(request_json)

    def add_definition(self, definition_name, custodian_info, email_filters=None):
        """Add definition for UserMailboxSubclient.

            Args:
                custodian_info   (dict)  --  list of users info to the case subclient

                custodian_info = [

                    {
                      "smtp": "ee2@testexch.commvault.com",
                      "name": "ee2",
                      "guid": "1b690719-72af-4d13-9ce0-577962cd165d"

                    },

                    {
                      "smtp": "ee15@testexch.commvault.com",
                      "name": "ee15",
                      "guid": "86139703-b8e7-41b9-824f-47f3f4b0dde1"

                    }

                  ]

        """

        if not isinstance(custodian_info, list):
            raise SDKException('Subclient', '101')

        try:
            self._filter_list = []
            if email_filters:
                self._prepare_email_filter_list(email_filters)
            self.custodian_info = []

            for mailbox_item in custodian_info:
                custodian_dict = {
                    'smtp': mailbox_item['smtp'],
                    'name': mailbox_item['name'],
                    'guid': mailbox_item['guid'],
                    'isGroup': 0

                }
                self.custodian_info.append(custodian_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))
        definition_json = {
            "mode": 1,
            "cmDef": {
                "caseId": int(self._client_object.client_id),
                "name": definition_name,
                "ownerId": 274,
                "defXml": {
                    "holdInfo": self.json_hold_info,
                    "custodianInfo": self.custodian_info,
                    "searchReq": self.json_search_request
                }
            }

        }

        self._case_definition_request(definition_json)
