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
from urllib.parse import urlparse

from cvpysdk.license import LicenseDetails
from .exception import SDKException


class _Metrics(object):
    """Class for common operations in Metrics reporting
    this will be inherited by Private and Cloud metrics"""

    def __init__(self, commcell_object, isprivate):
        self._commcell_object = commcell_object
        self._isprivate = isprivate
        self._METRICS = self._commcell_object._services['METRICS']
        self._GET_METRICS = self._commcell_object._services['GET_METRICS'] % self._isprivate
        self._enable_service = True
        self._disable_service = False
        self._get_metrics_config()

    def __repr__(self):
        """Representation string for the instance of the UserGroups class."""
        if self._isprivate == 1:
            metrics_type = 'Private'
        else:
            metrics_type = 'Public'
        return "{0} Metrics class instance with config '{1}'".format(
            metrics_type,
            self._metrics_config
        )

    def _get_metrics_config(self):
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

    def refresh(self):
        """updates metrics object with the latest configuration"""
        self._get_metrics_config()

    def _update_service_state(self, service_name, state):
        for idx, service in enumerate(self._service_list):
            if service['service']['name'] == service_name:
                self._service_list[idx]['enabled'] = state
                self.services[service_name] = state

    @property
    def lastdownloadtime(self):
        """Returns last download time in unix time format"""
        return self._metrics_config['config']['scriptDownloadTime']

    @property
    def lastcollectiontime(self):
        """Returns last collection time in unix time format"""
        return self._metrics_config['config']['lastCollectionTime']

    @property
    def lastuploadtime(self):
        """Returns last upload time in unix time format"""
        return self._metrics_config['config']['lastUploadTime']

    @property
    def nextuploadtime(self):
        """Returns last Next time in unix time format"""
        return self._metrics_config['config']['nextUploadTime']

    @property
    def uploadfrequency(self):
        """Returns last Next time in unix time format"""
        return self._metrics_config['config']['uploadFrequency']

    def enable_health(self):
        """enables Health Service"""
        if self.services['Health Check'] is not True:
            self._update_service_state('Health Check', self._enable_service)

    def disable_health(self):
        """disables Health Service"""
        if self.services['Health Check'] is True:
            self._update_service_state('Health Check', self._disable_service)

    def enable_activity(self):
        """enables Activity Service"""
        if self.services['Activity'] is not True:
            self._update_service_state('Activity', self._enable_service)

    def disable_activity(self):
        """disables Activity Service"""
        if self.services['Activity'] is True:
            self._update_service_state('Activity', self._disable_service)

    def enable_audit(self):
        """enables Audit Service"""
        if self.services['Audit'] is not True:
            self._update_service_state('Audit', self._enable_service)

    def disable_audit(self):
        """disables Audit Service"""
        if self.services['Audit'] is True:
            self._update_service_state('Audit', self._disable_service)

    def enable_post_upgrade_check(self):
        """enables post_upgrade_check Service"""
        if self.services['Post Upgrade Check'] is not True:
            self._update_service_state('Post Upgrade Check', self._enable_service)

    def disables_post_upgrade_check(self):
        """disables post_upgrade_check Service"""
        if self.services['Post Upgrade Check'] is True:
            self._update_service_state('Post Upgrade Check', self._disable_service)

    def disables_chargeback(self):
        """disables post_upgrade_check Service"""
        if self.services['Charge Back'] is True:
            self._update_service_state('Charge Back', self._disable_service)

    def enable_all_services(self):
        """enables All Service"""
        for index, service in enumerate(self._service_list):
            if service['service']['name'] not in ['Post Upgrade Check', 'Upgrade Readiness']:
                self._service_list[index]['enabled'] = self._enable_service
                service_name = service['service']['name']
                self.services[service_name] = self._enable_service

    def disable_all_services(self):
        """disables All Service"""
        for index, service in enumerate(self._service_list):
            if service['service']['name'] not in ['Post Upgrade Check', 'Upgrade Readiness']:
                self._service_list[index]['enabled'] = self._disable_service
                service_name = service['service']['name']
                self.services[service_name] = self._disable_service

    def set_upload_freq(self, days=1):
        """
        updates the upload frequency
        Args:
            days (int): number of days for upload frequency, value can be between 1 to 7

        Raises:
            SDKException:
                if invalid days supplied for upload frequency

        """
        if days < 1:
            raise SDKException('Metrics', '101', 'Invalid Upload Frequency supplied')
        self._metrics_config['config']['uploadFrequency'] = days

    def set_data_collection_window(self, seconds=28800):
        """
        updates the data collection window
        Args:
            seconds: number for seconds after 12 AM
            e.g.; 28800 for 8 AM
            default; 28800

        Raises:
            SDKException:
                if window specified is below 12.05 am

        """
        if seconds < 300:  # minimum 5 minutes after 12 midnight
            raise SDKException('Metrics', '101', 'Data collection window should be above 12.05 AM')
        self._metrics_config['config']['dataCollectionTime'] = seconds

    def remove_data_collection_window(self):
        """removes data collection window"""
        self._metrics_config['config']['dataCollectionTime'] = -1

    def set_all_clientgroups(self):
        """updates metrics configuration with all client groups"""

        # sets the list to one row with client group id as -1
        self._metrics_config['config']['clientGroupList'] = [{'_type_': 28, 'clientGroupId': -1}]

    def set_clientgroups(self, clientgroup_name=None):
        """
        sets the client groups for metrics
        Args:
            clientgroup_name (list): list of client group names, None is set all client groups
            will be enabled.
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

    def enable_metrics(self):
        """enables Metrics in CommServe"""
        self._metrics_config['config']['commcellDiagUsage'] = self._enable_service

    def disable_metrics(self):
        """disables Metrics in CommServe"""
        self._metrics_config['config']['commcellDiagUsage'] = self._disable_service

    def save_config(self):
        """
        updates the configuration of Metrics
        this must be called to save the configuration changes made in this object
        Raises:
            SDKException:
                if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._METRICS, self._metrics_config
        )
        if not flag:
            raise SDKException('Response', '101', response.text)

    def upload_now(self):
        """
        Performs Upload Now operation of metrics
        Raises:
            SDKException:
                if response is not success:
        """

        self._metrics_config['config']['uploadNow'] = 1
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._METRICS, self._metrics_config
        )
        if not flag:
            raise SDKException('Response', '101', response.text)
        # reset upload now flag
        self._metrics_config['config']['uploadNow'] = 0

    def wait_for_download_completion(self, timeout=300):
        """
        Waits for Metrics collection to complete for maximum of seconds given in timeout

        Args:
            timeout (int): maximum seconds to wait
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
        raise TimeoutError(
            "Download process didn't complete after {0} seconds".format(timeout))

    def wait_for_collection_completion(self, timeout=400):
        """
        Waits for Metrics collection to complete for maximum of seconds given in timeout

        Args:
            timeout (int): maximum seconds to wait

        Raises: Timeout error if collection didn't complete within timeout period
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

    def wait_for_upload_completion(self, timeout=120):
        """
        Waits for Metrics upload to complete for maximum of seconds given in timeout

        Args:
            timeout (int): maximum seconds to wait

        Raises: Timeout error if upload didn't complete within timeout period
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

    def wait_for_uploadnow_completion(self,
                                      download_timeout=300,
                                      collection_timeout=400,
                                      upload_timeout=120):
        """
        Waits for Metrics uploadNow operation to complete, checks both collection and upload

        Args:
            download_timeout (int): maximum seconds to wait for download
            collection_timeout (int): maximum seconds to wait for collection
            upload_timeout (int): maximum seconds to wait for upload

        Raises: Timeout error if uploadNow operation didn't complete

        """
        self.wait_for_download_completion(download_timeout)
        self.wait_for_collection_completion(collection_timeout)
        self.wait_for_upload_completion(upload_timeout)

    def _get_commcell_id(self):
        """returns the hexadecimal value of commcell id"""
        license_details = LicenseDetails(self._commcell_object)
        ccid = license_details.commcell_id
        if ccid == -1:
            commcellid = 'FFFFF'
        else:
            commcellid = hex(ccid).split('x')[1].upper()
        return commcellid

    def get_uploaded_filename(self, query_id=None, last_collection_time=None):
        """
        Gets last uploaded file name

        Args:
            query_id (int): optional argument to get file name specific to a query
            last_collection_time (int): optional argument to get file name for specified last collection time

        Returns: Last uploaded file name
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

    def get_uploaded_zip_filename(self, commserv_guid, backupjob_id):
        """
        Gets last uploaded zip file name
        Args:
            query_id (int): optional argument to get file name specific to a query
        Returns : Last uploaded file name
        """
        commcellid = self._get_commcell_id()
        cs_lastcollectiontime = int(self.lastcollectiontime)
        if cs_lastcollectiontime == 0:
            raise Exception("last collection time is 0, Upload didn't complete or failed")
        file_name = "CSS" + "" + str(cs_lastcollectiontime) + "_" + str(commcellid)\
                    + "_" + str(commserv_guid) + "_" + str(backupjob_id) + ".zip"
        return file_name

class PrivateMetrics(_Metrics):
    """Class for operations in private Metrics reporting"""

    def __init__(self, commcell_object):
        """Initialize object of the UserGroups class.

                    Args:
                        commcell_object (object)  --  instance of the Commcell class
                        type -- 1 for private, 0 for public

                    Returns:
                        object - instance of the UserGroups class
        """
        _Metrics.__init__(self, commcell_object, isprivate=True)

    def _update_private_download_url(self, hostname, port, protocol):
        self._cloud['downloadURL'] = '{0}://{1}:{2}/downloads/sqlscripts/'.format(protocol,
                                                                                  hostname,
                                                                                  port)

    def _update_private_upload_url(self, hostname, port, protocol):
        self._cloud['uploadURL'] = '{0}://{1}:{2}/commandcenter/'.format(protocol, hostname, port)

    def _update_chargeback_flags(self, daily, weekly, monthly):
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
    def downloadurl(self):
        """Returns download URL of private metrics"""
        return self._metrics_config['config']['cloud']['downloadURL']

    @property
    def uploadurl(self):
        """Returns Upload URL of private metrics"""
        return self._metrics_config['config']['cloud']['uploadURL']

    @property
    def private_metrics_server_name(self):
        return urlparse(self.uploadurl).hostname

    def update_url(self, hostname, port=80, protocol='http'):
        """
        updates private Metrics URL in CommServe
        Args:
            hostname (str): Metrics server hostname
            port (int): port of webconsole
                e.g.; 80 for http and 443 for https
            protocol (str): http or https
                default: http
        """
        self._update_private_download_url(hostname, port, protocol)
        self._update_private_upload_url(hostname, port, protocol)

    def enable_chargeback(self, daily=True, weekly=False, monthly=False):
        """
        Enables Chargeback service as per the daily,weekly and Monthly arguments passes
        Args:
            daily  (bool): enables daily chargeback
            weekly (bool): enables weekly chargeback
            monthly(bool): enables Monthly chargeback

        """
        if self.services['Charge Back'] is not True:
            self._update_service_state('Charge Back', self._enable_service)
        self._update_chargeback_flags(daily, weekly, monthly)

    def enable_forwarding(self, forwarding_url):
        """
        Enables forwarding
        Args:
            forwarding_url: Webconsole url where metrics data to be forwarded
        """
        fwd_info = [{
            "httpServerURL": forwarding_url,
            "isPublic": False,
            "urlPwd": "",
            "urlUser": ""
        }]
        self._metrics_config['config']['tieringActive'] = True
        self._metrics_config['config']['HttpServerInfo']["httpServer"] = fwd_info

    def disable_forwarding(self):
        """Disables forwarding"""
        self._metrics_config['config']['tieringActive'] = False


class CloudMetrics(_Metrics):
    """Class for operations in Cloud Metrics reporting"""

    def __init__(self, commcell_object):
        """Initialize object of the UserGroups class.

                    Args:
                        commcell_object (object)  --  instance of the Commcell class

                    Returns:
                        object - instance of the UserGroups class
        """
        _Metrics.__init__(self, commcell_object, isprivate=False)

    @property
    def randomization_minutes(self):
        return self._metrics_config['config']['randomization']

    def enable_chargeback(self):
        """Enables Chargeback service"""
        if self.services['Charge Back'] is not True:
            self._update_service_state('Charge Back', self._enable_service)

    def enable_upgrade_readiness(self):
        """Enables pre upgrade readiness service"""
        if self.services['Upgrade Readiness'] is not True:
            self._update_service_state('Upgrade Readiness', self._enable_service)

    def disable_upgrade_readiness(self):
        """disables pre upgrade readiness service"""
        if self.services['Upgrade Readiness'] is True:
            self._update_service_state('Upgrade Readiness', self._disable_service)

    def enable_proactive_support(self):
        """Enables Proactive Support service"""
        if self.services['Proactive Support'] is not True:
            self._update_service_state('Proactive Support', self._enable_service)

    def disable_proactive_support(self):
        """disables Proactive Support service"""
        if self.services['Proactive Support'] is True:
            self._update_service_state('Proactive Support', self._disable_service)

    def enable_cloud_assist(self):
        """Enables Cloud Assist service and proactive support if not already enabled"""
        if self.services['Proactive Support'] is not True:
            # pro active support must be enabled to enable cloud assist
            self.enable_proactive_support()
            self._update_service_state('Cloud Assist', self._enable_service)

    def disable_cloud_assist(self):
        """disables Cloud Assist service"""
        if self.services['Cloud Assist'] is True:
            self._update_service_state('Cloud Assist', self._disable_service)

    def set_randomization_minutes(self, minutes=0):
        """
        Sets the randomization value in gxglobal param

        Args:
            minutes (int): randomization value in minutes
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
    """class for operation in localmetrics"""

    def __init__(self, commcell_object, islocalmetrics= True):
        self._commcell_object = commcell_object
        self._islocalmetrics = islocalmetrics
        self._LOCAL_METRICS = self._commcell_object._services['LOCAL_METRICS'] % self._islocalmetrics
        self._get_metrics_config()

    def _get_metrics_config(self):
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._LOCAL_METRICS
        )
        if flag:
            self._metrics_config = response.json()
            config_value = self._metrics_config['config']
            return config_value
        else:
            raise SDKException('Response', '101', response.text)

    def refresh(self):
        """updates metrics object with the latest configuration"""
        self._get_metrics_config()

    @property
    def last_upload_time(self):
        """ get last upload time"""
        return self._metrics_config['config']['lastCollectionTime']

    @property
    def nextup_load_time(self):
        """get the next upload time"""
        return self._metrics_config['config']['nextUploadTime']
