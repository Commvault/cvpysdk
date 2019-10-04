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

     select_local_drive(client_name)             --  Selects local drive as report generation
                                                     location for specified client

     select_network_share()                      --  select network share as location

     set_report_copy_location(report_save_path)  --  sets report copy location to specified path

     set_report_custom_name(name)                --  sets custom report name

      run_report()                               --  Generates the report

BackupJobSummary:

    __init__(commcell_object)                   --  Initialize the backup job summary report object

"""

from enum import Enum
from cvpysdk.exception import SDKException


class FormatType(Enum):
    """Types of output format"""
    HTML = 1
    PDF = 6
    TEXT = 2
    XML = 12


class Report:
    """Operations on classic report"""

    def __init__(self, commcell):
        """ Initialize the report object """
        self._commcell = commcell
        self._request_json = {}
        self._cvpysdk_commcell_object = commcell._cvpysdk_object
        self._services = commcell._services
        self._report_extension = FormatType.HTML.name
        self._backup_job_summary_report = None

    @property
    def backup_job_summary(self):
        """Returns object of backup job summary report"""
        if self._backup_job_summary_report is None:
            self._backup_job_summary_report = BackupJobSummary(self._commcell)
        return self._backup_job_summary_report

    def set_format(self, format_type):
        """Sets the output format of a report
        Args:
            format_type (FormatType): set file extension using Enum class FormatType
        """
        for each_format_type in FormatType:
            if each_format_type.name == format_type:
                self._report_extension = each_format_type.name
                self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']\
                ['reportOption']['commonOpt']['outputFormat']['outputType'] = \
                    str(each_format_type.value)
                return
        raise Exception("Invalid format type,format should be one among the type in FormatType")

    def select_local_drive(self, client_name=None):
        """Select local drive
        Args:
            client_name(String)        --       Name of the client
        """
        if not client_name:
            client_name = self._commcell.commserv_name
        else:
            if not self._commcell.clients.has_client(client_name):
                raise Exception(f"Client [{client_name}] does not exist")
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption']\
        ['commonOpt']['savedTo']['reportSavedToClient']['clientName'] = client_name

    def select_network_share(self):
        """Select network share"""
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption']\
            ['commonOpt']['savedTo']['isNetworkDrive'] = 1

    def set_report_copy_location(self, report_save_path):
        """ Sets the path of report
        Args:
            report_save_path (String)   --      Report copy location of the report
        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption']\
            ['commonOpt']['savedTo']['locationURL'] = report_save_path

    def set_report_custom_name(self, name):
        """ Sets report custom name
        Args:
            name(String)               --       Custom name of the report
        """
        self._request_json['taskInfo']['subTasks'][0]['options']['adminOpts']['reportOption']\
        ['commonOpt']['reportCustomName'] = (name + "." + self._report_extension)

    def run_report(self):
        """ Executes the report
        Returns:
            str: Job ID
        """
        flag, response = self._cvpysdk_commcell_object.make_request('POST',
                                                                    self._services['CREATE_TASK'],
                                                                    self._request_json)
        try:
            return response.json()['jobIds'][0]
        except Exception:
            raise SDKException("RunReportError", '101', response.json()["errorMessage"])


class BackupJobSummary(Report):
    """Operations on backup job summary report"""
    def __init__(self, commcell_object):
        """ Initialize the backup job summary report object """
        super().__init__(commcell_object)
        self._request_json = {
            "taskInfo": {
                "task": {
                    "ownerId": 1,
                    "taskType": 1,
                    "ownerName": "admin",
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
                                        "includeAll": True
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
                                        }
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
