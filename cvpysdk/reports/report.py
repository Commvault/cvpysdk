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

"""Module for performing operations on classic Reports.

Report              :  Class for selecting different options on report and generate the report.
BackupJobSummary    :  Generate backup job summary report.
FormatType          :  Use this Enum class to provide different file extension.


Report:

     __init__(commcell_object)                   --  Initialize the Report instance for the
                                                     commcell

     backup_job_summary()                        --  Returns backup job summary instance

     set_format(format_type)                     --  sets specified file extension for the report
                                                     to be generated

     select_local_drive(report_copy_location, client_name) --  Selects local drive as report generation
                                                     location for specified client

     select_network_share()                      --  select network share as location

     set_report_custom_name(name)                --  sets custom report name

     run_report()                                --  Generates the report


BackupJobSummary:

    __init__(commcell_object)                   --  Initialize the backup job summary report object

     select_protected_objects()                  --  Select protected object option

     set_last_hours(hours)                       --  Jobs to be included since n hours

     set_last_days(hours)                        --  Jobs to be included since n days

     select_computers(clients, client_groups)    --  select specific clients and clientgroups


"""

from enum import Enum
from cvpysdk.exception import SDKException
from typing import Optional, List


class FormatType(Enum):
    """Types of output format

    Attributes:
        HTML (int): Represents HTML format with value 1.
        PDF (int): Represents PDF format with value 6.
        TEXT (int): Represents TEXT format with value 2.
        XML (int): Represents XML format with value 12.
    """
    HTML = 1
    PDF = 6
    TEXT = 2
    XML = 12


class Report:
    """Operations on classic report

    Attributes:
        _commcell (Commcell): Commcell object associated with the report.
        _request_json (dict): JSON request to be sent to the CommServe.
        _cvpysdk_commcell_object (CVPySDK): CVPySDK commcell object.
        _services (dict): Dictionary of Commvault services.
        _report_extension (str): Report file extension. Defaults to HTML.
        _backup_job_summary_report (BackupJobSummary): Instance of BackupJobSummary report.
    """

    def __init__(self, commcell):
        """ Initialize the report object

        Args:
            commcell (Commcell): the commcell object
        """
        self._commcell = commcell
        self._request_json = {}
        self._cvpysdk_commcell_object = commcell._cvpysdk_object
        self._services = commcell._services
        self._report_extension = FormatType.HTML.name
        self._backup_job_summary_report = None

    @property
    def backup_job_summary(self) -> "BackupJobSummary":
        """Returns object of backup job summary report

        Returns:
            BackupJobSummary: Instance of the BackupJobSummary class.

        Usage:
            >>> report = Report(commcell_object)
            >>> backup_job_summary = report.backup_job_summary
        """
        if self._backup_job_summary_report is None:
            self._backup_job_summary_report = BackupJobSummary(self._commcell)
        return self._backup_job_summary_report

    def set_format(self, format_type: FormatType) -> None:
        """Sets the output format of a report

        Args:
            format_type (FormatType): set file extension using Enum class FormatType

        Raises:
            Exception: if format_type is not a valid FormatType

        Usage:
            >>> report = Report(commcell_object)
            >>> report.set_format(FormatType.PDF)
        """
        for each_format_type in FormatType:
            if each_format_type.name == format_type.name:
                self._report_extension = each_format_type.name
                self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']\
                ['reportOption']['commonOpt']['outputFormat']['outputType'] = \
                    str(each_format_type.value)
                return
        raise Exception("Invalid format type,format should be one among the type in FormatType")

    def select_local_drive(self, report_copy_location: str, client_name: Optional[str] = None) -> None:
        """Select local drive

        Args:
            report_copy_location (str): location where report need to be saved
            client_name          (str): Name of the client, defaults to CommServe name if None

        Raises:
            Exception: if client_name does not exist

        Usage:
            >>> report = Report(commcell_object)
            >>> report.select_local_drive(report_copy_location='C:\\reports', client_name='client1')
            >>> report.select_local_drive(report_copy_location='C:\\reports')
        """
        if not client_name:
            client_name = self._commcell.commserv_name
        else:
            if not self._commcell.clients.has_client(client_name):
                raise Exception(f"Client [{client_name}] does not exist")
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption']\
        ['commonOpt']['savedTo']['reportSavedToClient']['clientName'] = client_name

        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['commonOpt']['savedTo']['locationURL'] = report_copy_location

    def select_network_share(self) -> None:
        """Select network share

        Usage:
            >>> report = Report(commcell_object)
            >>> report.select_network_share()
        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption']\
            ['commonOpt']['savedTo']['isNetworkDrive'] = 1

    def set_report_custom_name(self, name: str) -> None:
        """ Sets report custom name

        Args:
            name (str): Custom name of the report

        Usage:
            >>> report = Report(commcell_object)
            >>> report.set_report_custom_name(name='MyReport')
        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption']\
        ['commonOpt']['reportCustomName'] = (name + "." + self._report_extension)

    def run_report(self) -> str:
        """ Executes the report

        Returns:
            str: Job ID

        Raises:
            SDKException: if the report execution fails

        Usage:
            >>> report = Report(commcell_object)
            >>> job_id = report.run_report()
        """
        flag, response = self._cvpysdk_commcell_object.make_request('POST',
                                                                    self._services['CREATE_TASK'],
                                                                    self._request_json)
        try:
            return response.json()['jobIds'][0]
        except Exception:
            raise SDKException("RunReportError", '101', response.json()["errorMessage"])


class BackupJobSummary(Report):
    """Operations on backup job summary report

    Attributes:
        _request_json (dict): JSON request for the backup job summary report.
    """
    def __init__(self, commcell_object):
        """ Initialize the backup job summary report object

        Args:
            commcell_object (Commcell): Commcell object.
        """
        super().__init__(commcell_object)
        self._request_json = {
            "taskInfo": {
                "task": {
                    "ownerId": 1,
                    "taskType": 1,
                    "ownerName": commcell_object.commcell_username,
                    "sequenceNumber": 0,
                    "initiatedFrom": 1,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "appGroup": {},
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4004
                        },
                        "options": {
                            "adminOpts": {
                                "reportOption": {
                                    "includeClientGroup": False,
                                    "showHiddenStoragePolicies": False,
                                    "showJobsWithFailedFailesOnly": False,
                                    "showGlobalStoragePolicies": False,
                                    "allowDynamicContent": False,
                                    "jobOption": False,
                                    "excludeHiddenSubclients": False,
                                    "failedFilesThreshold": 0,
                                    "mediaAgentList": [
                                        {
                                            "_type_": 11,
                                            "flags": {
                                                "include": True
                                            }
                                        }
                                    ],
                                    "storagePolicyCopyList": [
                                        {
                                            "_type_": 17,
                                            "allCopies": True
                                        }
                                    ],
                                    "commonOpt": {
                                        "dateFormat": "mm/dd/yyyy",
                                        "overrideDateTimeFormat": 0,
                                        "reportType": 7715,
                                        "summaryOnly": False,
                                        "reportCustomName": "",
                                        "emailType": 2,
                                        "timeFormat": "hh:mm:ss am/pm",
                                        "onCS": True,
                                        "savedTo": {
                                            "locationURL": "",
                                            "ftpUploadLocation": "Commvault Reports",
                                            "uploadAsCabinetFile": False,
                                            "isNetworkDrive": False,
                                            "reportSavedToClient": {
                                                "hostName": "",
                                                "clientName": "",
                                                "_type_": 3
                                            },
                                            "ftpDetails": {}
                                        },
                                        "locale": {
                                            "_type_": 66,
                                            "LCID": 3081,
                                            "displayString": "English-Australia",
                                            "locale": "en-au",
                                            "localeName": "en",
                                            "localeId": 0
                                        },
                                        "outputFormat": {
                                            "textDelimiter": "\t",
                                            "outputType": 1,
                                            "isNetworkDrive": False
                                        }
                                    },
                                    "computerSelectionList": {
                                        "includeAll": True,
                                        "clientGroupList": [
                                        ],
                                        "clientList": [
                                        ]

                                    },
                                    "jobSummaryReport": {
                                        "subClientDescription": "",
                                        "subclientFilter": False,
                                        "filterOnSubClientDesc": False,
                                        "groupBy": 2,
                                        "rptSelections": {
                                            "includeSnapProtectionJobsOnly": False,
                                            "includeArchivedPSTs": False,
                                            "includeProtectedDatabases": False,
                                            "includeClientDescription": False,
                                            "includeBackupFilesOnly": False,
                                            "description": True,
                                            "stubbedFiles": False,
                                            "includeFailedSkippedMailboxes": False,
                                            "includeDisabledActivityClients": True,
                                            "sizeChangePercentage": False,
                                            "jobAttempts": False,
                                            "includePerformanceJobsOnly": False,
                                            "includeReferenceCopyClientMap": False,
                                            "subclientContent": False,
                                            "failedObjects": False,
                                            "includeProtectedVMs": True,
                                            "associatedEvent": False,
                                            "mediaAgents": False,
                                            "agedData": False,
                                            "IncBackupCopyJobsOnly": False,
                                            "subclientFilters": False,
                                            "protectedObjects": False,
                                            "IncBackupCopyJobs": False,
                                            "contentIndexingFailures": False,
                                            "subclientJobOpt": 0,
                                            "associatedMedia": False,
                                            "storagePolicy": False,
                                            "numberOfHours": 0,
                                            "initializingUser": False,
                                            "includeDeconfiguredClients": True,
                                            "numberOfObjects": 100,
                                            "failureReason": True,
                                            "IncludeMediaDeletedJobs": False,
                                            "drive": False
                                        },
                                        "jobOptions": {
                                            "numberOfMostFreqErrors": 0,
                                            "sizeUnit": 0,
                                            "isThroughputInMB": False,
                                            "isCommserveTimeZone": True,
                                            "retentionType": {
                                                "basicRetention": False,
                                                "manualRetention": False,
                                                "extendedRetention": False,
                                                "retentionAll": False
                                            },
                                            "backupTypes": {
                                                "all": True,
                                                "syntheticFull": True,
                                                "automatedSystemRecovery": False,
                                                "incremental": True,
                                                "full": True,
                                                "differential": True
                                            },
                                            "jobStatus": {
                                                "all": True
                                            },
                                            "increaseInDataSize": {
                                                "value": 10,
                                                "selected": False
                                            },
                                            "decreaseInDataSize": {
                                                "value": 10,
                                                "selected": False
                                            }
                                        }
                                    },
                                    "agentList": [
                                        {
                                            "_type_": 4,
                                            "flags": {
                                                "include": True
                                            }
                                        }
                                    ],
                                    "timeRangeOption": {
                                        "type": 13,
                                        "_type_": 54,
                                        "TimeZoneID": 42,
                                        "toTime": 86400
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }

    def select_protected_objects(self) -> None:
        """select protected objects

        Usage:
            >>> backup_job_summary = BackupJobSummary(commcell_object)
            >>> backup_job_summary.select_protected_objects()
        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['jobSummaryReport']['rptSelections']['protectedObjects'] = True

    def __set_include_all(self, status: bool = True) -> None:
        """
        Set include all computers true/false if any client/client group are getting selected
        Args:
                status     (Boolean)    --  Set True to include all the clients otherwise set false

        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['computerSelectionList']['includeAll'] = status

    def __select_client_groups(self, client_groups: list) -> None:
        """
        Select client groups
        Args:
                client_groups     (List)    --  list of clientgroups
        """
        client_group_list_dict = []
        for each_client_group in client_groups:
            client_group_list_dict.append({"clientGroupName": each_client_group})
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['computerSelectionList']['clientGroupList'] = client_group_list_dict

    def __select_clients(self, client_list: list) -> None:
        """
        Select client clients
         Args:
                client_list     (List)    --  list of clients
        """
        client_list_dict = []
        for each_client in client_list:
            client_list_dict.append({"clientName": each_client})
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['computerSelectionList']['clientList'] = client_list_dict

    def set_last_hours(self, number_of_hours: int = 24) -> None:
        """
        Set time range to generate report since n number of hours
        Args:
                number_of_hours     (Int)    --  number of hours
        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['timeRangeOption']['type'] = 13
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['timeRangeOption']['toTimeValue'] = str(number_of_hours)

    def set_last_days(self, number_of_days: int = 24) -> None:
        """
        Set time range to generate report since n number of days
        Args:
                number_of_hours     (Int)    --  number of hours
        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['timeRangeOption']['type'] = 11
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption'] \
            ['timeRangeOption']['toTimeValue'] = str(number_of_days)

    def select_computers(self, clients: Optional[List[str]] = None, client_groups: Optional[List[str]] = None) -> None:
        """
        Select clients and client groups for generating the report
        Args:
                clients       (List): List of clients
                client_groups (List): List of client groups

        Usage:
            >>> backup_job_summary = BackupJobSummary(commcell_object)
            >>> backup_job_summary.select_computers(clients=['client1', 'client2'], client_groups=['group1', 'group2'])
            >>> backup_job_summary.select_computers(clients=['client1'])
            >>> backup_job_summary.select_computers(client_groups=['group1'])
        """
        self.__set_include_all(status=False)
        if clients:
            self.__select_clients(clients)
        if client_groups:
            self.__select_client_groups(client_groups)
