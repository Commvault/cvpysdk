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

"""Module for performing operations on Job Summary for Reports"""

from xml.etree import ElementTree
from enum import Enum
from cvpysdk.exception import SDKException


class FormatType(Enum):
    """Types of output format"""
    HTML = 1
    PDF = 6
    TEXT = 2
    XML = 12


class Report:
    """ Class for building a backup job summary report"""

    def __init__(self, commcell):
        """ Initialize the backup job summary report object """
        self.commcell = commcell
        self.__xml = """
        <?xml version="1.0" encoding="UTF-8" standalone="no" ?><TMMsg_CreateTaskReq><taskInfo>
        <task initiatedFrom="1"ownerId="1" ownerName="admin" sequenceNumber="0" taskType="1"><taskFlags disabled="0"/>
        </task><appGroup/><subTasks subTaskOperation="1"><subTask operationType="4004" subTaskType="1"/><options>
        <adminOpts><reportOption allowDynamicContent="0" excludeHiddenSubclients="0" 
        failedFilesThreshold="0" includeClientGroup="0" jobOption="0"
        showGlobalStoragePolicies="0" showHiddenStoragePolicies="0" showJobsWithFailedFailesOnly="0"><commonOpt
        dateFormat="mm/dd/yyyy" emailType="2" onCS="1" overrideDateTimeFormat="0" reportCustomName="" reportType="7715" 
        summaryOnly="0" timeFormat="hh:mm:ss am/pm"><outputFormat isNetworkDrive="0" outputType="1" textDelimiter="&#x9; 
        "/><savedTo ftpUploadLocation="Commvault Reports" isNetworkDrive="0" locationURL="" uploadAsCabinetFile="0">
        <reportSavedToClient _type_="3" clientName="" hostName=""/><ftpDetails/></savedTo>
        <locale LCID="3081" _type_="66" displayString="English-Australia" locale="en-au" localeId="0" localeName="en"/>
        </commonOpt><computerSelectionList 
        includeAll="1"/><agentList _type_="4"><flags include="1"/></agentList><mediaAgentList _type_="11"><flags 
        include="1"/></mediaAgentList><storagePolicyCopyList _type_="17" allCopies="1"/><timeRangeOption TimeZoneID="42" 
        _type_="54" toTime="86400" type="13"/><jobSummaryReport filterOnSubClientDesc="0" groupBy="2" 
        subClientDescription="" subclientFilter="0"><jobOptions isCommserveTimeZone="1" isThroughputInMB="0" 
        numberOfMostFreqErrors="0" sizeUnit="0"><backupTypes all="1" automatedSystemRecovery="0" differential="1" 
        full="1" incremental="1" syntheticFull="1"/><jobStatus all="1"/><increaseInDataSize selected="0" value="10"/>
        <decreaseInDataSize selected="0" value="10"/><retentionType basicRetention="0" extendedRetention="0" 
        manualRetention="0" retentionAll="0"/></jobOptions><rptSelections IncBackupCopyJobs="0" 
        IncBackupCopyJobsOnly="0" IncludeMediaDeletedJobs="0" agedData="0" 
        associatedEvent="0" associatedMedia="0" contentIndexingFailures="0" 
        description="1" drive="0" failedObjects="0" failureReason="1" includeArchivedPSTs="0" includeBackupFilesOnly="0" 
        includeClientDescription="0" includeDeconfiguredClients="1" includeDisabledActivityClients="1" 
        includeFailedSkippedMailboxes="0" includePerformanceJobsOnly="0" includeProtectedDatabases="0" 
        includeProtectedVMs="1" includeReferenceCopyClientMap="0" includeSnapProtectionJobsOnly="0" initializingUser="0" 
        jobAttempts="0" mediaAgents="0" numberOfHours="0" numberOfObjects="100" protectedObjects="0" 
        sizeChangePercentage="0" storagePolicy="0" stubbedFiles="0" subclientContent="0" subclientFilters="0" 
        subclientJobOpt="0"/></jobSummaryReport></reportOption></adminOpts><commonOpts/></options></subTasks></taskInfo>
        </TMMsg_CreateTaskReq>"""
        self.__root = ElementTree.fromstring(self.__xml)

    def set_format(self, format_type):
        """Sets the output format of a report

        Args:
            format_type (FormatType): Report format type

        """
        if format_type not in FormatType:
            raise Exception("Invalid format type,format should be one among the type in FormatType")
        path = self.__root.findall(".//outputFormat")
        path[0].set('outputType', '%s' % format_type.value)
        self.__xml = ElementTree.tostring(self.__root)

    def set_local_path(self, report_save_path, client_name=None):
        """ Sets the Client and the path for the report to be saved on

        Args:
            report_save_path: Report copy location of the backup job summary

            client_name: Name of the client to copy the report summary on

        """
        location = self.__root.findall(".//savedTo")
        location[0].set('locationURL', report_save_path)
        if not client_name:
            client_name = self.commcell.commserv_name
        else:
            if not self.commcell.clients.has_client(client_name):
                raise Exception(f"Client [{client_name}] does not exist")
        cname = self.__root.findall(".//reportSavedToClient")
        cname[0].set('clientName', client_name)
        self.__xml = ElementTree.tostring(self.__root)

    def export_report(self):
        """ Executes the backup job summary report

        Returns:
            str: Job ID

        """
        response = self.commcell.execute_qcommand("qoperation execute", self.__xml)
        try:
            return response.json()["jobIds"][0]
        except Exception as error:
            raise SDKException("Backupset", 102, " %s"
                               % response.json().get("errorMessage")) from error
