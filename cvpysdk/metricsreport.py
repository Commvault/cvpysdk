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

"""File for performing Metrics operations.

_Metrics        : Class for representing all common operations on Metrics Reporting
PrivateMetrics  : Class for representing Private Metrics and performing operations on it.
PublicMetrics   : Class for representing Public Metrics and performing operations on it.

use method save_config() or upload_now() to save the updated configurations.

Metrics:
    __init__(Commcell_object, isprivate)--  initialise with object of CommCell and flag to
                                            specificy metrics Type

    __repr__()                   --  returns the string to represent the instance of the
                                            Metrics class
    enable_health()              --  enables Health service

    disable_health()             --  disables Health service

    enable_activity()            --  enables Activity service

    disable_activity()           --  disables Activity service

    enable_audit()               --  enables Audit service

    disable_audit()              --  disables Audit service

    disable_chargeback()         --  disables Chargeback service

    enable_post_upgrade_check()  -- enables enable_post_upgrade_check Service

    enable_all_services()        -- enables All Service in metrics

    disable_all_services()       -- disables All Service

    enable_metrics()             -- enables Metrics Service

    disable_metrics()            -- disables Metrics Service in CommServe

    set_upload_freq()            --  updates the upload frequency

    set_data_collection_window   -- updates the data collection window

    remove_data_collection_window-- removes data collection window

    set_all_clientgroup()        -- updates metrics configuration with all client groups

    set_clientgroups()           -- sets the client groups for metrics

    save_config()                -- updates the configuration of Metrics, this must be
                                    called to save the configuration changes made in this object

    upload_now()                 -- Performs Upload Now operation of metrics

    wait_for_download_completion()-- waits for metrics download operation to complete

    wait_for_collection_completion-- waits for metrics collection operation to complete

    wait_for_upload_completion()  -- waits for metrics upload operation to complete

    wait_for_uploadnow_completion()-- waits for complete metrics operation to complete

    get_possible_uploaded_filenames-- gives the possible names for the uploaded files

    refresh()                      -- refresh the properties and config of the Metrics Server
    get_uploaded_filename()        -- Gets last uploaded file name
    get_uploaded_zip_filename()    -- Gets last uploaded zip file name
PrivateMetrics:
    __init__(Commcell_object)   --  initialise with object of CommCell

    update_url(hostname)        --  Updates Metrics URL for download and upload

    enable_chargeback(daily, weekly, monthly)
                                --  enables chargeback service

PublicMetrics:
    __init__(Commcell_object)   --  initialise with object of CommCell

    enable_chargeback()         --  enables chargeback service

    enable_upgrade_readiness()  -- Enables pre upgrade readiness service

    disable_upgrade_readiness() -- disables pre upgrade readiness service

    enable_proactive_support()  -- Enables Proactive Support service

    disable_proactive_support() -- disables Proactive Support service

    enable_cloud_assist()       -- Enables Cloud Assist service

    disable_cloud_assist()      -- disables Cloud Assist service

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from time import sleep
from typing import List, Optional
from urllib.parse import urlparse

from cvpysdk.license import LicenseDetails

from Web.Common.exceptions import CVTestStepFailure
from .exception import SDKException

class _Metrics(object):
    """
    Base class for common operations in Metrics reporting.

    This class provides a comprehensive set of methods and properties for managing,
    configuring, and monitoring metrics reporting services. It is designed to be
    inherited by both Private and Cloud metrics classes, offering a unified interface
    for metrics configuration, service state management, data collection, upload
    scheduling, and health/activity/audit controls.

    Key Features:
        - Metrics configuration retrieval and refresh
        - Service state management (enable/disable health, activity, audit, post-upgrade check, chargeback, etc.)
        - Upload frequency and data collection window configuration
        - Client group management for metrics reporting
        - Enable/disable all metrics services
        - Manual and scheduled metrics upload operations
        - Wait mechanisms for download, collection, and upload completion with timeout support
        - Access to key metrics properties (last download/collection/upload times, next upload time, upload frequency)
        - Retrieval of uploaded file and zip filenames for reporting
        - Saving and updating metrics configuration

    This class is intended for internal use as a base for more specialized metrics
    reporting classes, providing essential building blocks for metrics management
    in both private and cloud environments.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, isprivate: bool) -> None:
        """Initialize the _Metrics object with a Commcell connection and privacy setting.

        Args:
            commcell_object: The Commcell object representing the connection to the Commcell environment.
            isprivate: Boolean flag indicating whether the metrics are private.

        Example:
            >>> metrics = _Metrics(commcell_object, isprivate=True)
            >>> print("Metrics object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._isprivate = isprivate
        self._METRICS = self._commcell_object._services['METRICS']
        self._GET_METRICS = self._commcell_object._services['GET_METRICS'] % self._isprivate
        self._enable_service = True
        self._disable_service = False
        self._get_metrics_config()

    def __repr__(self) -> str:
        """Return the string representation of the _Metrics instance.

        This method provides a developer-friendly string that represents the current
        _Metrics object, useful for debugging and logging purposes.

        Returns:
            A string representation of the _Metrics instance.

        Example:
            >>> metrics = _Metrics()
            >>> print(repr(metrics))
            <_Metrics object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """
        if self._isprivate == 1:
            metrics_type = 'Private'
        else:
            metrics_type = 'Public'
        return "{0} Metrics class instance with config '{1}'".format(
            metrics_type,
            self._metrics_config
        )

    def _get_metrics_config(self) -> dict:
        """Retrieve the configuration settings for metrics.

        Returns:
            dict: A dictionary containing the current metrics configuration.

        Example:
            >>> metrics = _Metrics()
            >>> config = metrics._get_metrics_config()
            >>> print(config)
            {'enabled': True, 'interval': 60, 'retention': 30}

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._GET_METRICS
        )
        if flag:
            self._metrics_config = response.json()
            self._metrics_config.update({'isPrivateCloud': bool(self._isprivate == 1)})
            if self._metrics_config and 'config' in self._metrics_config:
                # get services
                self.services = {}
                self._cloud = self._metrics_config['config']['cloud']
                self._service_list = self._cloud['serviceList']
                for service in self._service_list:
                    service_name = service['service']['name']
                    status = service['enabled']
                    self.services[service_name] = status
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', response.text)

    def refresh(self) -> None:
        """Update the metrics object with the latest configuration.

        This method refreshes the internal state of the metrics object to ensure it reflects
        the most current configuration data.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.refresh()
            >>> print("Metrics configuration updated successfully")

        #ai-gen-doc
        """
        self._get_metrics_config()

    def _update_service_state(self, service_name: str, state: str) -> None:
        """Update the state of a specified service in the metrics system.

        Args:
            service_name: The name of the service whose state is being updated.
            state: The new state to assign to the service (e.g., 'running', 'stopped', 'error').

        Example:
            >>> metrics = _Metrics()
            >>> metrics._update_service_state('BackupService', 'running')
            >>> # The state of 'BackupService' is now set to 'running' in the metrics system

        #ai-gen-doc
        """
        for idx, service in enumerate(self._service_list):
            if service['service']['name'] == service_name:
                self._service_list[idx]['enabled'] = state
                self.services[service_name] = state

    @property
    def lastdownloadtime(self) -> int:
        """Get the last download time in Unix time format.

        Returns:
            The last download time as an integer representing seconds since the Unix epoch.

        Example:
            >>> metrics = _Metrics()
            >>> last_time = metrics.lastdownloadtime
            >>> print(f"Last download time (Unix timestamp): {last_time}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['scriptDownloadTime']

    @property
    def lastcollectiontime(self) -> int:
        """Get the last collection time in Unix time format.

        Returns:
            The last collection time as an integer representing seconds since the Unix epoch.

        Example:
            >>> metrics = _Metrics()
            >>> last_time = metrics.lastcollectiontime
            >>> print(f"Last collection time (Unix timestamp): {last_time}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['lastCollectionTime']

    @property
    def lastuploadtime(self) -> int:
        """Get the last upload time in Unix time format.

        Returns:
            The last upload time as an integer representing seconds since the Unix epoch.

        Example:
            >>> metrics = _Metrics()
            >>> last_time = metrics.lastuploadtime
            >>> print(f"Last upload time (Unix timestamp): {last_time}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['lastUploadTime']

    @property
    def nextuploadtime(self) -> int:
        """Get the next upload time in Unix timestamp format.

        Returns:
            The next scheduled upload time as an integer Unix timestamp.

        Example:
            >>> metrics = _Metrics()
            >>> next_time = metrics.nextuploadtime  # Use dot notation for property access
            >>> print(f"Next upload time (Unix timestamp): {next_time}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['nextUploadTime']

    @property
    def uploadfrequency(self) -> int:
        """Get the next upload time in Unix time format.

        Returns:
            The next scheduled upload time as a Unix timestamp (seconds since epoch).

        Example:
            >>> metrics = _Metrics()
            >>> next_upload = metrics.uploadfrequency
            >>> print(f"Next upload scheduled at: {next_upload}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['uploadFrequency']

    def enable_health(self) -> None:
        """Enable the Health Service for metrics monitoring.

        This method activates the Health Service, allowing the system to collect and report health-related metrics.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.enable_health()
            >>> print("Health Service enabled successfully")

        #ai-gen-doc
        """
        if self.services['Health Check'] is not True:
            self._update_service_state('Health Check', self._enable_service)

    def disable_health(self) -> None:
        """Disable the Health Service for this metrics instance.

        This method turns off the Health Service monitoring functionality associated with the metrics object.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.disable_health()
            >>> print("Health Service has been disabled.")
        #ai-gen-doc
        """
        if self.services['Health Check'] is True:
            self._update_service_state('Health Check', self._disable_service)

    def enable_activity(self) -> None:
        """Enable the Activity Service for metrics collection.

        This method activates the Activity Service, allowing the system to start collecting and reporting activity metrics.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.enable_activity()
            >>> print("Activity Service enabled for metrics collection.")

        #ai-gen-doc
        """
        if self.services['Activity'] is not True:
            self._update_service_state('Activity', self._enable_service)

    def disable_activity(self) -> None:
        """Disable the Activity Service for metrics.

        This method disables the Activity Service, preventing further activity tracking or metric collection.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.disable_activity()
            >>> print("Activity Service has been disabled.")

        #ai-gen-doc
        """
        if self.services['Activity'] is True:
            self._update_service_state('Activity', self._disable_service)

    def enable_audit(self) -> None:
        """Enable the Audit Service for metrics collection.

        This method activates the Audit Service, allowing the system to track and record audit-related events.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.enable_audit()
            >>> print("Audit Service enabled successfully")

        #ai-gen-doc
        """
        if self.services['Audit'] is not True:
            self._update_service_state('Audit', self._enable_service)

    def disable_audit(self) -> None:
        """Disable the Audit Service for the current metrics context.

        This method turns off auditing, preventing further audit logs from being generated
        or collected for the associated metrics.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.disable_audit()
            >>> print("Audit service has been disabled for metrics.")
        #ai-gen-doc
        """
        if self.services['Audit'] is True:
            self._update_service_state('Audit', self._disable_service)

    def enable_post_upgrade_check(self) -> None:
        """Enable the post-upgrade check service.

        This method activates the post-upgrade check service, which can be used to verify 
        system integrity or configuration after an upgrade process.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.enable_post_upgrade_check()
            >>> print("Post-upgrade check service enabled.")

        #ai-gen-doc
        """
        if self.services['Post Upgrade Check'] is not True:
            self._update_service_state('Post Upgrade Check', self._enable_service)

    def disables_post_upgrade_check(self) -> None:
        """Disable the post-upgrade check service.

        This method disables the post-upgrade check service, preventing it from running after an upgrade operation.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.disables_post_upgrade_check()
            >>> print("Post-upgrade check service has been disabled.")

        #ai-gen-doc
        """
        if self.services['Post Upgrade Check'] is True:
            self._update_service_state('Post Upgrade Check', self._disable_service)

    def disables_chargeback(self) -> None:
        """Disable the chargeback feature in the metrics service.

        This method disables the chargeback functionality, which may be used for tracking or billing purposes within the metrics service.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.disables_chargeback()
            >>> print("Chargeback feature disabled.")
        #ai-gen-doc
        """
        if self.services['Charge Back'] is True:
            self._update_service_state('Charge Back', self._disable_service)

    def enable_all_services(self) -> None:
        """Enable all available metric services.

        This method activates all metric services managed by the _Metrics class.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.enable_all_services()
            >>> print("All metric services have been enabled.")

        #ai-gen-doc
        """
        for index, service in enumerate(self._service_list):
            if service['service']['name'] not in ['Post Upgrade Check', 'Upgrade Readiness']:
                self._service_list[index]['enabled'] = self._enable_service
                service_name = service['service']['name']
                self.services[service_name] = self._enable_service

    def disable_all_services(self) -> None:
        """Disable all metric services managed by this instance.

        This method disables all services associated with the metrics system.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.disable_all_services()
            >>> print("All metric services have been disabled.")

        #ai-gen-doc
        """
        for index, service in enumerate(self._service_list):
            if service['service']['name'] not in ['Post Upgrade Check', 'Upgrade Readiness']:
                self._service_list[index]['enabled'] = self._disable_service
                service_name = service['service']['name']
                self.services[service_name] = self._disable_service

    def set_upload_freq(self, days: int = 1) -> None:
        """Update the upload frequency for metrics data.

        Args:
            days: The number of days to set as the upload frequency. Must be an integer between 1 and 7.

        Raises:
            SDKException: If an invalid value for days is supplied (not in the range 1 to 7).

        Example:
            >>> metrics = _Metrics()
            >>> metrics.set_upload_freq(3)
            >>> # The upload frequency is now set to every 3 days

        #ai-gen-doc
        """
        if days < 1:
            raise SDKException('Metrics', '101', 'Invalid Upload Frequency supplied')
        self._metrics_config['config']['uploadFrequency'] = days

    def set_data_collection_window(self, seconds: int = 28800) -> None:
        """Update the data collection window for metrics collection.

        This method sets the start time for data collection, specified as the number of seconds after 12:00 AM.
        For example, 28800 seconds corresponds to 8:00 AM. The default value is 28800 seconds.

        Args:
            seconds: The number of seconds after 12:00 AM to begin data collection. Must be at least 300 seconds (12:05 AM).

        Raises:
            SDKException: If the specified window is below 12:05 AM (less than 300 seconds).

        Example:
            >>> metrics = _Metrics()
            >>> metrics.set_data_collection_window(32400)  # Sets window to 9:00 AM
            >>> metrics.set_data_collection_window()       # Uses default of 8:00 AM

        #ai-gen-doc
        """
        if seconds < 300:  # minimum 5 minutes after 12 midnight
            raise SDKException('Metrics', '101', 'Data collection window should be above 12.05 AM')
        self._metrics_config['config']['dataCollectionTime'] = seconds

    def remove_data_collection_window(self) -> None:
        """Remove the data collection window configuration from the metrics object.

        This method deletes any existing data collection window settings, reverting to default behavior.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.remove_data_collection_window()
            >>> print("Data collection window removed successfully")

        #ai-gen-doc
        """
        self._metrics_config['config']['dataCollectionTime'] = -1

    def set_all_clientgroups(self) -> None:
        """Update the metrics configuration to include all client groups.

        This method refreshes the metrics settings so that all available client groups 
        are included in the configuration. Use this when you want metrics to apply 
        universally across all client groups managed by the system.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.set_all_clientgroups()
            >>> print("Metrics configuration updated to include all client groups.")

        #ai-gen-doc
        """

        # sets the list to one row with client group id as -1
        self._metrics_config['config']['clientGroupList'] = [{'_type_': 28, 'clientGroupId': -1}]

    def set_clientgroups(self, clientgroup_name: Optional[List[str]] = None) -> None:
        """Set the client groups to be used for metrics collection.

        If no client group names are provided, all available client groups will be enabled for metrics.

        Args:
            clientgroup_name: Optional list of client group names to enable for metrics. 
                If None, all client groups will be enabled.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.set_clientgroups(['GroupA', 'GroupB'])
            >>> # Only 'GroupA' and 'GroupB' will be enabled for metrics
            >>> metrics.set_clientgroups()
            >>> # All client groups will be enabled for metrics

        #ai-gen-doc
        """
        if clientgroup_name is None:
            self.set_all_clientgroups()
        else:
            self._metrics_config['config']['clientGroupList'] = []
            clientgroup = self._metrics_config['config']['clientGroupList']
            for each_client_grp in clientgroup_name:
                cg_id = self._commcell_object.client_groups.get(each_client_grp).clientgroup_id
                clientgroup.append(
                    {'_type_': 28, 'clientGroupId': int(cg_id), 'clientGroupName': each_client_grp}
                )

    def enable_metrics(self) -> None:
        """Enable the Metrics feature in the CommServe environment.

        This method activates Metrics collection and reporting capabilities within the CommServe.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.enable_metrics()
            >>> print("Metrics have been enabled in CommServe.")
        #ai-gen-doc
        """
        self._metrics_config['config']['commcellDiagUsage'] = self._enable_service

    def disable_metrics(self) -> None:
        """Disable the Metrics feature in the CommServe environment.

        This method turns off the Metrics functionality, preventing the collection and reporting
        of metrics data within the CommServe system.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.disable_metrics()
            >>> print("Metrics have been disabled in CommServe.")

        #ai-gen-doc
        """
        self._metrics_config['config']['commcellDiagUsage'] = self._disable_service

    def save_config(self) -> None:
        """Save the current configuration changes for the Metrics object.

        This method updates the Metrics configuration with any changes made to the object.
        It must be called after making modifications to ensure that the changes are persisted.

        Raises:
            SDKException: If the configuration update response is not successful.

        Example:
            >>> metrics = _Metrics()
            >>> # Make configuration changes to the metrics object
            >>> metrics.save_config()  # Persist the changes to the configuration

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._METRICS, self._metrics_config
        )
        if not flag:
            raise SDKException('Response', '101', response.text)

    def upload_now(self) -> None:
        """Trigger an immediate upload of metrics data.

        This method initiates the "Upload Now" operation for metrics, sending the latest metrics data to the configured destination.

        Raises:
            SDKException: If the upload operation does not complete successfully.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.upload_now()
            >>> print("Metrics upload initiated successfully.")

        #ai-gen-doc
        """

        self._metrics_config['config']['uploadNow'] = 1
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._METRICS, self._metrics_config
        )
        if not flag:
            raise SDKException('Response', '101', response.text)
        # reset upload now flag
        self._metrics_config['config']['uploadNow'] = 0

    def wait_for_download_completion(self, timeout: int = 300) -> None:
        """Wait for the Metrics collection download to complete, up to the specified timeout.

        This method blocks execution until the Metrics collection process finishes or the timeout 
        (in seconds) is reached.

        Args:
            timeout: Maximum number of seconds to wait for the download to complete. Defaults to 300 seconds.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.wait_for_download_completion(timeout=600)
            >>> print("Metrics download completed or timed out.")

        #ai-gen-doc
        """
        self.refresh()
        time_limit = timeout
        while time_limit > 0:
            if self.lastdownloadtime > 0:
                return True
            else:
                sleep(30)
                time_limit -= 30
                self.refresh()
        raise CVTestStepFailure("Download process didn't complete after {0} seconds".format(timeout))

    def wait_for_collection_completion(self, timeout: int = 400) -> None:
        """Wait for the metrics collection process to complete within a specified timeout period.

        This method blocks execution until the metrics collection is finished or the specified
        timeout (in seconds) is reached.

        Args:
            timeout: The maximum number of seconds to wait for the collection to complete. Defaults to 400 seconds.

        Raises:
            TimeoutError: If the metrics collection does not complete within the specified timeout period.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.wait_for_collection_completion(timeout=300)
            >>> print("Metrics collection completed successfully.")

        #ai-gen-doc
        """
        self.refresh()
        timelimit = timeout
        while timelimit > 0:
            if self.lastcollectiontime > 0:
                return True
            else:
                sleep(30)
                timelimit -= 30
                self.refresh()
        raise TimeoutError("Collection process didn't complete after {0} seconds".format(timeout))

    def wait_for_upload_completion(self, timeout: int = 120) -> None:
        """Wait for the Metrics upload process to complete within a specified timeout period.

        This method blocks execution until the Metrics upload is finished or the timeout is reached.

        Args:
            timeout: The maximum number of seconds to wait for the upload to complete. Defaults to 120 seconds.

        Raises:
            TimeoutError: If the upload does not complete within the specified timeout period.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.wait_for_upload_completion(timeout=180)
            >>> print("Upload completed successfully.")

        #ai-gen-doc
        """
        self.refresh()
        timelimit = timeout
        while timelimit > 0:
            if self.lastuploadtime >= self.lastcollectiontime and self.lastuploadtime > 0:
                return True
            else:
                sleep(30)
                timelimit -= 30
                self.refresh()
        raise TimeoutError("Upload process didn't complete after {0} seconds".format(timeout))

    def wait_for_uploadnow_completion(self, download_timeout: int = 300, collection_timeout: int = 400, upload_timeout: int = 120) -> None:
        """Wait for the Metrics uploadNow operation to complete, including both collection and upload phases.

        This method blocks execution until the Metrics uploadNow process has finished, or until the specified timeouts are reached for each phase.

        Args:
            download_timeout: Maximum number of seconds to wait for the download phase to complete. Default is 300 seconds.
            collection_timeout: Maximum number of seconds to wait for the collection phase to complete. Default is 400 seconds.
            upload_timeout: Maximum number of seconds to wait for the upload phase to complete. Default is 120 seconds.

        Raises:
            TimeoutError: If the uploadNow operation does not complete within the specified timeouts.

        Example:
            >>> metrics = _Metrics()
            >>> metrics.wait_for_uploadnow_completion(download_timeout=200, collection_timeout=300, upload_timeout=100)
            >>> print("UploadNow operation completed successfully.")

        #ai-gen-doc
        """
        self.wait_for_download_completion(download_timeout)
        self.wait_for_collection_completion(collection_timeout)
        self.wait_for_upload_completion(upload_timeout)

    def _get_commcell_id(self) -> str:
        """Retrieve the hexadecimal representation of the Commcell ID.

        Returns:
            The Commcell ID as a hexadecimal string.

        Example:
            >>> metrics = _Metrics()
            >>> hex_id = metrics._get_commcell_id()
            >>> print(f"Commcell ID (hex): {hex_id}")

        #ai-gen-doc
        """
        license_details = LicenseDetails(self._commcell_object)
        ccid = license_details.commcell_id
        if ccid == -1:
            commcellid = 'FFFFF'
        else:
            commcellid = hex(ccid).split('x')[1].upper()
        return commcellid

    def get_uploaded_filename(self, query_id: Optional[int] = None, last_collection_time: Optional[int] = None) -> str:
        """Retrieve the name of the last uploaded file.

        This method returns the filename of the most recently uploaded file. Optionally, you can specify a query ID
        to get the filename associated with a particular query, or provide a last collection time to get the filename
        for a specific collection timestamp.

        Args:
            query_id: Optional; The ID of the query to filter the uploaded file name.
            last_collection_time: Optional; The timestamp of the last collection to filter the uploaded file name.

        Returns:
            The name of the last uploaded file as a string.

        Example:
            >>> metrics = _Metrics()
            >>> filename = metrics.get_uploaded_filename()
            >>> print(f"Last uploaded file: {filename}")
            >>>
            >>> # With query_id
            >>> filename = metrics.get_uploaded_filename(query_id=123)
            >>> print(f"File for query 123: {filename}")
            >>>
            >>> # With last_collection_time
            >>> filename = metrics.get_uploaded_filename(last_collection_time=1680000000)
            >>> print(f"File for collection time 1680000000: {filename}")

        #ai-gen-doc
        """

        commcellid = self._get_commcell_id()
        if last_collection_time is None:
            cs_lastcollectiontime = int(self.lastcollectiontime)
        else:
            cs_lastcollectiontime = last_collection_time
        if cs_lastcollectiontime == 0:
            raise Exception("last collection time is 0, Upload didn't complete or failed")
        if query_id is None:
            file_name = "CSS" + "" + str(cs_lastcollectiontime) + "_" + str(commcellid) + ".xml"
        else:
            file_name = "CSS" + "" + str(cs_lastcollectiontime) + "_" + str(
                commcellid) + "_" + str(query_id) + ".xml"
        return file_name

    def get_uploaded_zip_filename(self, commserv_guid: str, backupjob_id: int) -> str:
        """Retrieve the name of the last uploaded zip file for a given CommServe and backup job.

        Args:
            commserv_guid: The GUID of the CommServe for which the zip file was uploaded.
            backupjob_id: The ID of the backup job associated with the uploaded zip file.

        Returns:
            The filename of the last uploaded zip file as a string.

        Example:
            >>> metrics = _Metrics()
            >>> filename = metrics.get_uploaded_zip_filename("1234-5678-90ab-cdef", 101)
            >>> print(f"Last uploaded zip file: {filename}")

        #ai-gen-doc
        """
        commcellid = self._get_commcell_id()
        cs_lastcollectiontime = int(self.lastcollectiontime)
        if cs_lastcollectiontime == 0:
            raise Exception("last collection time is 0, Upload didn't complete or failed")
        file_name = "CSS" + "" + str(cs_lastcollectiontime) + "_" + str(commcellid)\
                    + "_" + str(commserv_guid) + "_" + str(backupjob_id) + ".zip"
        return file_name

class PrivateMetrics(_Metrics):
    """
    Handles operations related to private metrics reporting within the system.

    This class provides an interface for managing private metrics, including
    configuration of download and upload URLs, chargeback settings, and forwarding
    options. It exposes properties to access current metrics server information and
    supports enabling or disabling forwarding and chargeback features.

    Key Features:
        - Initialize with a CommCell object for context
        - Update private download and upload URLs with specified host, port, and protocol
        - Access current download and upload URLs via properties
        - Retrieve the private metrics server name
        - Update URLs for metrics reporting
        - Enable chargeback with daily, weekly, and monthly flags
        - Enable or disable forwarding to a specified URL

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize an instance of the PrivateMetrics class.

        Args:
            commcell_object: An instance of the Commcell class used to establish a connection.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> private_metrics = PrivateMetrics(commcell)
            >>> print("PrivateMetrics object created successfully")

        #ai-gen-doc
        """
        _Metrics.__init__(self, commcell_object, isprivate=True)

    def _update_private_download_url(self, hostname: str, port: int, protocol: str) -> None:
        """Update the private download URL using the specified hostname, port, and protocol.

        Args:
            hostname: The hostname to be used in the download URL.
            port: The port number to be used in the download URL.
            protocol: The protocol (e.g., 'http', 'https') to be used in the download URL.

        Example:
            >>> metrics = PrivateMetrics()
            >>> metrics._update_private_download_url('example.com', 8080, 'https')
            >>> # The private download URL is now updated with the new parameters

        #ai-gen-doc
        """
        self._cloud['downloadURL'] = '{0}://{1}:{2}/downloads/sqlscripts/'.format(protocol,
                                                                                  hostname,
                                                                                  port)

    def _update_private_upload_url(self, hostname: str, port: int, protocol: str) -> None:
        """Update the private upload URL using the specified hostname, port, and protocol.

        Args:
            hostname: The hostname to use for constructing the upload URL.
            port: The port number to use for the upload URL.
            protocol: The protocol to use (e.g., 'http', 'https') for the upload URL.

        Example:
            >>> metrics = PrivateMetrics()
            >>> metrics._update_private_upload_url('example.com', 8080, 'https')
            >>> # The private upload URL is now updated with the new settings

        #ai-gen-doc
        """
        self._cloud['uploadURL'] = '{0}://{1}:{2}/commandcenter/'.format(protocol, hostname, port)

    def _update_chargeback_flags(self, daily: bool, weekly: bool, monthly: bool) -> None:
        """Update the chargeback flags for daily, weekly, and monthly metrics.

        Args:
            daily: Set to True to enable daily chargeback metrics, False to disable.
            weekly: Set to True to enable weekly chargeback metrics, False to disable.
            monthly: Set to True to enable monthly chargeback metrics, False to disable.

        Example:
            >>> metrics = PrivateMetrics()
            >>> metrics._update_chargeback_flags(daily=True, weekly=False, monthly=True)
            >>> # This will enable daily and monthly chargeback metrics, and disable weekly.

        #ai-gen-doc
        """
        flags = 0
        if daily:
            flags = flags | 4
        if weekly:
            flags = flags | 8
        if monthly:
            flags = flags | 16
        for service in self._service_list:
            if service['service']['name'] == 'Charge Back':
                service['flags'] = flags

    @property
    def downloadurl(self) -> str:
        """Get the download URL for private metrics.

        Returns:
            The URL as a string that can be used to download private metrics data.

        Example:
            >>> metrics = PrivateMetrics()
            >>> url = metrics.downloadurl  # Use dot notation to access the property
            >>> print(f"Download URL: {url}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['cloud']['downloadURL']

    @property
    def uploadurl(self) -> str:
        """Get the upload URL for private metrics.

        Returns:
            str: The URL endpoint used for uploading private metrics.

        Example:
            >>> metrics = PrivateMetrics()
            >>> url = metrics.uploadurl  # Use dot notation to access the property
            >>> print(f"Upload URL: {url}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['cloud']['uploadURL']

    @property
    def private_metrics_server_name(self) -> str:
        """Get the name of the private metrics server associated with this instance.

        Returns:
            The name of the private metrics server as a string.

        Example:
            >>> metrics = PrivateMetrics()
            >>> server_name = metrics.private_metrics_server_name
            >>> print(f"Private Metrics Server: {server_name}")

        #ai-gen-doc
        """
        return urlparse(self.uploadurl).hostname

    def update_url(self, hostname: str, port: int = 80, protocol: str = 'http') -> None:
        """Update the private Metrics URL in the CommServe configuration.

        This method sets the URL used by the CommServe to communicate with the private Metrics server,
        based on the provided hostname, port, and protocol.

        Args:
            hostname: The hostname or IP address of the Metrics server.
            port: The port number for the web console (default is 80 for HTTP, 443 for HTTPS).
            protocol: The protocol to use for the connection ('http' or 'https'). Default is 'http'.

        Example:
            >>> metrics = PrivateMetrics()
            >>> metrics.update_url('metrics.example.com', port=443, protocol='https')
            >>> # The CommServe will now use https://metrics.example.com:443 as the Metrics URL

        #ai-gen-doc
        """
        self._update_private_download_url(hostname, port, protocol)
        self._update_private_upload_url(hostname, port, protocol)

    def enable_chargeback(self, daily: bool = True, weekly: bool = False, monthly: bool = False) -> None:
        """Enable the Chargeback service with daily, weekly, and/or monthly options.

        This method activates the Chargeback service according to the specified frequency flags.
        You can enable any combination of daily, weekly, and monthly chargeback reporting.

        Args:
            daily: If True, enables daily chargeback reporting. Default is True.
            weekly: If True, enables weekly chargeback reporting. Default is False.
            monthly: If True, enables monthly chargeback reporting. Default is False.

        Example:
            >>> metrics = PrivateMetrics()
            >>> metrics.enable_chargeback(daily=True, weekly=True, monthly=False)
            >>> # This enables daily and weekly chargeback reporting

            >>> metrics.enable_chargeback(monthly=True)
            >>> # This enables only monthly chargeback reporting

        #ai-gen-doc
        """
        if self.services['Charge Back'] is not True:
            self._update_service_state('Charge Back', self._enable_service)
        self._update_chargeback_flags(daily, weekly, monthly)

    def enable_forwarding(self, forwarding_url: str) -> None:
        """Enable forwarding of metrics data to a specified Webconsole URL.

        Args:
            forwarding_url: The Webconsole URL to which metrics data should be forwarded.

        Example:
            >>> metrics = PrivateMetrics()
            >>> metrics.enable_forwarding("https://webconsole.example.com/metrics")
            >>> print("Forwarding enabled to the specified Webconsole URL")

        #ai-gen-doc
        """
        fwd_info = [{
            "httpServerURL": forwarding_url,
            "isPublic": False,
            "urlPwd": "",
            "urlUser": ""
        }]
        self._metrics_config['config']['tieringActive'] = True
        self._metrics_config['config']['HttpServerInfo']["httpServer"] = fwd_info

    def disable_forwarding(self) -> None:
        """Disable the forwarding of private metrics.

        This method stops the forwarding of private metrics data, preventing it from being sent to external systems or services.

        Example:
            >>> metrics = PrivateMetrics()
            >>> metrics.disable_forwarding()
            >>> print("Forwarding disabled for private metrics.")

        #ai-gen-doc
        """
        self._metrics_config['config']['tieringActive'] = False


class CloudMetrics(_Metrics):
    """
    CloudMetrics provides a suite of operations for managing and reporting cloud metrics.

    This class enables the configuration and control of various cloud metrics features,
    including chargeback, upgrade readiness, proactive support, and cloud assist functionalities.
    It also allows for the management of randomization settings to optimize reporting intervals.

    Key Features:
        - Enable or disable chargeback reporting
        - Enable or disable upgrade readiness monitoring
        - Enable or disable proactive support features
        - Enable or disable cloud assist capabilities
        - Configure randomization minutes for metrics reporting
        - Access randomization settings via property

    Inherits from:
        _Metrics

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a CloudMetrics object with the given Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> cloud_metrics = CloudMetrics(commcell)
            >>> print("CloudMetrics object initialized successfully")

        #ai-gen-doc
        """
        _Metrics.__init__(self, commcell_object, isprivate=False)

    @property
    def randomization_minutes(self) -> int:
        """Get the number of randomization minutes configured for cloud metrics.

        Returns:
            int: The number of minutes used for randomizing cloud metrics operations.

        Example:
            >>> metrics = CloudMetrics()
            >>> minutes = metrics.randomization_minutes
            >>> print(f"Randomization minutes: {minutes}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['randomization']

    def enable_chargeback(self) -> None:
        """Enable the Chargeback service for cloud metrics.

        This method activates the Chargeback service, allowing for tracking and reporting of resource usage and associated costs.

        Example:
            >>> cloud_metrics = CloudMetrics()
            >>> cloud_metrics.enable_chargeback()
            >>> print("Chargeback service enabled successfully.")

        #ai-gen-doc
        """
        if self.services['Charge Back'] is not True:
            self._update_service_state('Charge Back', self._enable_service)

    def enable_upgrade_readiness(self) -> None:
        """Enable the pre-upgrade readiness service for cloud metrics.

        This method activates the pre-upgrade readiness service, which helps ensure that the environment is prepared for an upgrade.

        Example:
            >>> cloud_metrics = CloudMetrics()
            >>> cloud_metrics.enable_upgrade_readiness()
            >>> print("Pre-upgrade readiness service enabled.")

        #ai-gen-doc
        """
        if self.services['Upgrade Readiness'] is not True:
            self._update_service_state('Upgrade Readiness', self._enable_service)

    def disable_upgrade_readiness(self) -> None:
        """Disable the pre-upgrade readiness service for the cloud metrics environment.

        This method turns off the pre-upgrade readiness checks, which may be used to prepare 
        the environment for upgrades or maintenance.

        Example:
            >>> metrics = CloudMetrics()
            >>> metrics.disable_upgrade_readiness()
            >>> print("Upgrade readiness service has been disabled.")

        #ai-gen-doc
        """
        if self.services['Upgrade Readiness'] is True:
            self._update_service_state('Upgrade Readiness', self._disable_service)

    def enable_proactive_support(self) -> None:
        """Enable the Proactive Support service for the cloud metrics system.

        This method activates the Proactive Support feature, which may provide enhanced monitoring 
        and support capabilities for your cloud environment.

        Example:
            >>> metrics = CloudMetrics()
            >>> metrics.enable_proactive_support()
            >>> print("Proactive Support has been enabled.")

        #ai-gen-doc
        """
        if self.services['Proactive Support'] is not True:
            self._update_service_state('Proactive Support', self._enable_service)

    def disable_proactive_support(self) -> None:
        """Disable the Proactive Support service for the current CloudMetrics instance.

        This method turns off the Proactive Support service, preventing it from collecting
        or sending diagnostic data to the support team.

        Example:
            >>> metrics = CloudMetrics()
            >>> metrics.disable_proactive_support()
            >>> print("Proactive Support has been disabled.")

        #ai-gen-doc
        """
        if self.services['Proactive Support'] is True:
            self._update_service_state('Proactive Support', self._disable_service)

    def enable_cloud_assist(self) -> None:
        """Enable the Cloud Assist service and proactive support if not already enabled.

        This method activates the Cloud Assist service, which may include enabling proactive support features
        for your cloud environment. If Cloud Assist is already enabled, this method has no effect.

        Example:
            >>> metrics = CloudMetrics()
            >>> metrics.enable_cloud_assist()
            >>> print("Cloud Assist service is now enabled.")

        #ai-gen-doc
        """
        if self.services['Proactive Support'] is not True:
            # pro active support must be enabled to enable cloud assist
            self.enable_proactive_support()
            self._update_service_state('Cloud Assist', self._enable_service)

    def disable_cloud_assist(self) -> None:
        """Disable the Cloud Assist service for this CloudMetrics instance.

        This method turns off the Cloud Assist service, preventing it from collecting or sending metrics data to the cloud.

        Example:
            >>> metrics = CloudMetrics()
            >>> metrics.disable_cloud_assist()
            >>> print("Cloud Assist service has been disabled.")

        #ai-gen-doc
        """
        if self.services['Cloud Assist'] is True:
            self._update_service_state('Cloud Assist', self._disable_service)

    def set_randomization_minutes(self, minutes: int = 0) -> None:
        """Set the randomization value (in minutes) in the gxglobal parameter.

        This method updates the randomization setting, which may be used to stagger scheduled operations 
        to avoid simultaneous execution.

        Args:
            minutes: The randomization value in minutes to set. Defaults to 0 (no randomization).

        Example:
            >>> metrics = CloudMetrics()
            >>> metrics.set_randomization_minutes(15)
            >>> # The randomization value is now set to 15 minutes

        #ai-gen-doc
        """
        qcommand = self._commcell_object._services['QCOMMAND']
        qoperation = ('qoperation execscript -sn SetKeyIntoGlobalParamTbl.sql '
                      '-si CommservSurveyRandomizationEnabled -si y -si {0}'.format(minutes))

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', qcommand, qoperation
        )
        if not flag:
            raise SDKException('Response', '101', response.text)


class LocalMetrics:
    """
    Class for managing and operating on local metrics configurations.

    The LocalMetrics class provides functionality to interact with and manage
    local metrics within a system. It allows for initialization with a commcell
    object, retrieval and refresh of metrics configuration, and provides
    properties to access the last and next upload times for metrics data.

    Key Features:
        - Initialize with commcell object and local metrics flag
        - Retrieve current metrics configuration
        - Refresh metrics configuration data
        - Access last upload time of metrics
        - Access next scheduled upload time of metrics

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, islocalmetrics: bool = True) -> None:
        """Initialize the LocalMetrics object with a Commcell connection.

        Args:
            commcell_object: The Commcell instance to associate with this LocalMetrics object.
            islocalmetrics: Indicates whether to use local metrics. Defaults to True.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> local_metrics = LocalMetrics(commcell)
            >>> # To specify not using local metrics:
            >>> local_metrics = LocalMetrics(commcell, islocalmetrics=False)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._islocalmetrics = islocalmetrics
        self._LOCAL_METRICS = self._commcell_object._services['LOCAL_METRICS'] % self._islocalmetrics
        self._get_metrics_config()

    def _get_metrics_config(self) -> dict:
        """Retrieve the configuration settings for local metrics.

        Returns:
            dict: A dictionary containing the configuration parameters for local metrics.

        Example:
            >>> metrics = LocalMetrics()
            >>> config = metrics._get_metrics_config()
            >>> print(config)
            {'enabled': True, 'interval': 60, ...}

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._LOCAL_METRICS
        )
        if flag:
            self._metrics_config = response.json()
            config_value = self._metrics_config['config']
            return config_value
        else:
            raise SDKException('Response', '101', response.text)

    def refresh(self) -> None:
        """Update the metrics object with the latest configuration.

        This method refreshes the internal state of the metrics object to ensure it reflects
        the most recent configuration settings.

        Example:
            >>> metrics = LocalMetrics()
            >>> metrics.refresh()
            >>> print("Metrics configuration updated.")

        #ai-gen-doc
        """
        self._get_metrics_config()

    @property
    def last_upload_time(self) -> Optional[str]:
        """Get the timestamp of the last metrics upload.

        Returns:
            The last upload time as a string in ISO 8601 format, or None if no upload has occurred.

        Example:
            >>> metrics = LocalMetrics()
            >>> last_time = metrics.last_upload_time  # Use dot notation for property access
            >>> print(f"Last upload time: {last_time}")
            >>> # Output might be: "2024-06-01T12:34:56Z" or None if never uploaded

        #ai-gen-doc
        """
        return self._metrics_config['config']['lastCollectionTime']

    @property
    def nextup_load_time(self) -> float:
        """Get the scheduled time for the next upload operation.

        Returns:
            The timestamp (as a float, typically in seconds since the epoch) representing when the next upload is scheduled.

        Example:
            >>> metrics = LocalMetrics()
            >>> next_time = metrics.nextup_load_time
            >>> print(f"Next upload scheduled at: {next_time}")

        #ai-gen-doc
        """
        return self._metrics_config['config']['nextUploadTime']