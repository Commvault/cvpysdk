# -*- coding: utf-8 -*-
# pylint: disable=W0212,W0201
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

"""main file for performing disaster recovery operations on commcell

DisasterRecovery                :   Class for performing DR backup with various options.

DisasterRecoveryManagement      :   Class for performing disaster recovery management operations.

DisasterRecovery:
=================

    __init__()                    --    initializes DisasterRecovery class object

    reset_to_defaults()           --    resets the properties to default values

    disaster_recovery_backup()    --    function to run DR backup

    _process_drbackup_response()  --    process the disaster recovery backup request

    restore_out_of_place()        --    function to run DR restore operation

    _advanced_dr_backup()         --    includes advance dr backup options

    _generatedrbackupjson()       --    Generate JSON corresponds to DR backup job

    _process_createtask_response()--    Runs the CreateTask API with the request JSON
                                        provided for DR backup.

    _filter_paths()               --    Filters the paths based on the Operating System and Agent.


DisasterRecovery Attributes
==========================

    **backuptype**                --    set or get backup type
    **is_compression_enabled**    --    set or get compression property
    **is_history_db_enabled**     --    set or get history db property
    **is_workflow_db_enabled**    --    set or get workflow db property
    **is_appstudio_db_enabled**   --    set or get appstudio db property
    **is_cvcloud_db_enabled**     --    set or get cvcloud db property
    **is_dm2_db_enabled**         --    set or get dm2db property
    **client_list**               --    set or get client list property.

DisasterRecoveryManagement:
==========================

    __init__()                          --   initializes DisasterRecoveryManagement class object

    _get_dr_properties()                --   Executes get request on server and retrives the dr settings

    _set_dr_properties()                --   Executes post request on server and sets the dr settings

    refresh()                           --   retrives the latest dr settings

    set_local_dr_path                   --   sets the local dr path

    set_network_dr_path                 --   sets the unc path

    upload_metdata_to_commvault_cloud   --   sets ths account to be used for commvault cloud backup.

    upload_metdata_to_cloud_library     --   sets the libarary to be used for cloud backup.

    impersonate_user                    --   account to be used for execution of pre/post scripts

    use_impersonate_user                --  gets the setting use_impersonate_user

DisasterRecoveryManagement Attributes:
=====================================

    **number_of_metadata**                  --  set or get number of metadata to be retained property
    **use_vss**                             --  set or get use vss property
    **wild_card_settings**                  --  set or get wild card settings property
    **backup_metadata_folder**              --  get backup metadata folder property
    **upload_backup_metadata_to_cloud**     --  get upload backup metadata to cloud property
    **upload_backup_metadata_to_cloud_lib** --  get upload backup metadata to cloud lib.
    **dr_storage_policy**                   --  set or get dr storage policy property
    **pre_scan_process**                    --  set or get pre scan process
    **post_scan_process**                   --  set or get post scan process
    **pre_backup_process**                  --  set or get pre backup process
    **post_backup_process**                 --  set or get post backup process
    **run_post_scan_process**               --  set or get run post scan process
    **run_post_backup_process**             --  set or get run post backup process

"""

from base64 import b64encode
from past.builtins import basestring
from cvpysdk.policies.storage_policies import StoragePolicy
from .job import Job
from .exception import SDKException
from .client import Client


class DisasterRecovery(object):
    """Class to perform all the disaster recovery operations on commcell"""

    def __init__(self, commcell):
        """Initializes DisasterRecovery object

            Args:
                commcell    (object)    --  instance of commcell

        """
        self.commcell = commcell
        self.client = Client(self.commcell, self.commcell.commserv_name)
        self.path = self.client.install_directory
        self._RESTORE = self.commcell._services['RESTORE']
        self._CREATE_TASK = self.commcell._services['CREATE_TASK']
        self.advbackup = False
        self.reset_to_defaults()

    def reset_to_defaults(self):
        """
        Resets the instance variables to default values

            Returns:
                 None
        """
        self._backup_type = "full"
        self._is_compression_enabled = True
        self._is_history_db_enabled = True
        self._is_workflow_db_enabled = True
        self._is_appstudio_db_enabled = True
        self._is_cvcloud_db_enabled = True
        self._is_dm2_db_enabled = True
        self._client_list = None
        self.advanced_job_options = None

    def disaster_recovery_backup(self):
        """Runs a DR job for Commserv

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """

        if self._backup_type.lower() not in ['full', 'differential']:
            raise SDKException('Response', '103')
        backuptypes = {"full": 1, "differential": 3}
        if self.advbackup:
            self._backup_type = backuptypes[self._backup_type.lower()]
            return self._advanced_dr_backup()
        dr_service = self.commcell._services['DRBACKUP']
        request_json = {"isCompressionEnabled": self._is_compression_enabled,
                        "jobType": 1, "backupType": backuptypes[self.backup_type.lower()]}
        flag, response = self.commcell._cvpysdk_object.make_request(
            'POST', dr_service, request_json
        )
        return self._process_drbackup_response(flag, response)

    def _process_drbackup_response(self, flag, response):
        """DR Backup response will be processed.

            Args:
                flag, response  (str)  --  results of DR backup JSON request

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if job initialization failed

                    if response is empty

                    if response is not success
        """
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self.commcell, response.json()['jobIds'][0])
                if "errorCode" in response.json():
                    o_str = 'Initializing backup failed\nError: "{0}"'.format(
                        response.json()['errorMessage']
                    )
                    raise SDKException('Response', '102', o_str)
            raise SDKException('Response', '102')
        response_string = self.commcell._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def restore_out_of_place(
            self,
            client,
            destination_path,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            restore_jobs=[]):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                                                           the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                                                           files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        preserve_level      : preserve level option to set in restore
                        proxy_client        : proxy that needed to be used for restore
                        impersonate_user    : Impersonate user options for restore
                        impersonate_password: Impersonate password option for restore
                                                in base64 encoded form
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up

                restore_jobs    (list)      --  list of jobs to be restored if the job is index free restore

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        if not ((isinstance(client, (basestring, Client))
                 and isinstance(destination_path, basestring)
                 and isinstance(overwrite, bool) and isinstance(restore_data_and_acl, bool))):
            raise SDKException('Response', '101')

        if fs_options is None:
            fs_options = {}

        if isinstance(client, Client):
            client = client
        elif isinstance(client, basestring):
            client = Client(self.commcell, client)
        else:
            raise SDKException('Response', '105')
        drpath = self.path + "\\CommserveDR"
        destination_path = self._filter_paths([destination_path], True)
        drpath = [self._filter_paths([drpath], True)]
        if not drpath:
            raise SDKException('Response', '104')
        agent_obj = client.agents.get("File System")
        instance_obj = agent_obj.instances.get("DefaultInstanceName")

        instance_obj._restore_association = {
            "type": "0",
            "backupsetName": "DR-BackupSet",
            "instanceName": "DefaultInstanceName",
            "appName": "CommServe Management",
            "clientName": self.commcell.commserv_name,
            "consumeLicense": True,
            "clientSidePackage": True,
            "subclientName": ""
        }
        return instance_obj._restore_out_of_place(
            client,
            destination_path,
            paths=drpath,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            restore_jobs=restore_jobs)

    def _advanced_dr_backup(self):
        """Runs a DR job with JSON input

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        request_json = self._generatedrbackupjson()
        return self._process_createtask_response(request_json)

    def _generatedrbackupjson(self):
        """
        Generate JSON corresponds to DR backup job
        """
        try:
            self._task = {
                "taskFlags": {"disabled": False},
                "policyType": "DATA_PROTECTION",
                "taskType": "IMMEDIATE",
                "initiatedFrom": 1
            }
            self._subtask = {
                "subTaskType": "ADMIN",
                "operationType": "DRBACKUP"
            }
            clientdict = []
            if self._client_list is not None:
                for client in self._client_list:
                    client = {
                        "type": 0,
                        "clientName": client,
                        "clientSidePackage": True,
                        "consumeLicense": True}
                    clientdict.append(client)

            common_opts = None
            if self.advanced_job_options:
                common_opts = {
                    "startUpOpts": {
                        "priority": self.advanced_job_options.get("priority", 66),
                        "startInSuspendedState": self.advanced_job_options.get("start_in_suspended_state", False),
                        "startWhenActivityIsLow": self.advanced_job_options.get("start_when_activity_is_low", False),
                        "useDefaultPriority": self.advanced_job_options.get("use_default_priority", True)
                    },
                    "jobRetryOpts": {
                        "runningTime": {
                            "enableTotalRunningTime": self.advanced_job_options.get(
                                "enable_total_running_time", False),
                            "totalRunningTime": self.advanced_job_options.get("total_running_time", 3600)
                        },
                        "enableNumberOfRetries": self.advanced_job_options.get("enable_number_of_retries", False),
                        "killRunningJobWhenTotalRunningTimeExpires": self.advanced_job_options.get(
                            "kill_running_job_when_total_running_time_expires", False),
                        "numberOfRetries": self.advanced_job_options.get("number_of_retries", 0)
                    },
                    "jobDescription": self.advanced_job_options.get("job_description", "")
                }

            self._droptions = {
                "drbackupType": self._backuptype, "dbName": "commserv",
                "backupHistoryDataBase": self.is_history_db_enabled,
                "backupWFEngineDataBase": self.is_workflow_db_enabled,
                "backupAppStudioDataBase": self.is_appstudio_db_enabled,
                "backupCVCloudDataBase": self.is_cvcloud_db_enabled,
                "backupDM2DataBase": self.is_dm2_db_enabled,
                "enableDatabasesBackupCompression": self.is_compression_enabled,
                "client": clientdict

            }

            request_json = {
                "taskInfo":
                {
                    "task": self._task,
                    "subTasks":
                    [{
                        "subTaskOperation": 1,
                        "subTask": self._subtask,
                        "options":
                        {
                            "adminOpts":
                            {
                                "drBackupOption": self._droptions,
                                "contentIndexingOption":
                                {
                                    "subClientBasedAnalytics": False
                                }
                            },
                            "restoreOptions":
                            {
                                "virtualServerRstOption":
                                {
                                    "isBlockLevelReplication": False
                                }
                            }
                        }
                    }
                    ]
                }
            }

            if self.advanced_job_options:
                request_json["taskInfo"]["subTasks"][0]["options"]["commonOpts"] = common_opts

            return request_json
        except Exception as err:
            raise SDKException('Response', '101', err)

    def _process_createtask_response(self, request_json):
        """Runs the CreateTask API with the request JSON provided for DR backup,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if restore job failed

                    if response is empty

                    if response is not success
        """
        flag, response = self.commcell._cvpysdk_object.make_request(
            'POST', self._CREATE_TASK, request_json
        )
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self.commcell, response.json()['jobIds'][0])
                if "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'DR backup job failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Response', '102', o_str)
                raise SDKException(
                    'Response', '102', 'Failed to run the DR backup job')
            raise SDKException('Response', '102')
        response_string = self.commcell._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _filter_paths(self, paths, is_single_path=False):
        """Filters the paths based on the Operating System, and Agent.

            Args:
                paths           (list)  --  list containing paths to be filtered

                is_single_path  (bool)  --  boolean specifying whether to return a single path
                                                or the entire list

            Returns:
                list    -   if the boolean is_single_path is set to False

                str     -   if the boolean is_single_path is set to True
        """
        for index, path in enumerate(paths):

            path = path.strip('\\').strip('/')
            if path:
                path = path.replace('/', '\\')
            else:
                path = '\\'

            paths[index] = path

        if is_single_path:
            return paths[0]
        return paths

    @property
    def client_list(self):
        """Treats the client_list as a read-only attribute."""
        return self._client_list

    @client_list.setter
    def client_list(self, value):
        """Treats the client_list as a read-only attribute."""
        if isinstance(value, list):
            self._client_list = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_compression_enabled(self):
        """Treats the iscompressionenabled as a read-only attribute."""
        return self._is_compression_enabled

    @is_compression_enabled.setter
    def is_compression_enabled(self, value):
        """Treats the iscompressionenabled as a read-only attribute."""
        if isinstance(value, bool):
            self._is_compression_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def backup_type(self):
        """Treats the backup_type as a read-only attribute."""
        return self._backuptype

    @backup_type.setter
    def backup_type(self, value):
        """Treats the backup_type as a read-only attribute."""
        if isinstance(value, basestring):
            self._backuptype = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_history_db_enabled(self):
        """Treats the historydb as a read-only attribute."""
        return self._is_history_db_enabled

    @is_history_db_enabled.setter
    def is_history_db_enabled(self, value):
        """sets the value of ishistorydb

            Args:
                value   (bool)      --  True/False
         """
        if isinstance(value, bool):
            self._is_history_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_workflow_db_enabled(self):
        """Treats the workflowdb as a read-only attribute."""
        return self._is_workflow_db_enabled

    @is_workflow_db_enabled.setter
    def is_workflow_db_enabled(self, value):
        """
        sets the value of isworkflowdb

            Args:
                value   (bool)      --  True/False
         """
        if isinstance(value, bool):
            self._is_workflow_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_appstudio_db_enabled(self):
        """Treats the workflowdb as a read-only attribute."""
        return self._is_appstudio_db_enabled

    @is_appstudio_db_enabled.setter
    def is_appstudio_db_enabled(self, value):
        """
        sets the value of isappstudiodb

            Args:
                value   (bool)      --  True/False
         """
        if isinstance(value, bool):
            self._is_appstudio_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_cvcloud_db_enabled(self):
        """Treats the cvclouddb as a read-only attribute."""
        return self._is_cvcloud_db_enabled

    @is_cvcloud_db_enabled.setter
    def is_cvcloud_db_enabled(self, value):
        """
        sets the value of iscvclouddb

            Args:
                value   (bool)      --  True/False
         """
        if isinstance(value, bool):
            self._is_cvcloud_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def is_dm2_db_enabled(self):
        """Treats the dm2db as a read-only attribute."""
        return self._is_dm2_db_enabled

    @is_dm2_db_enabled.setter
    def is_dm2_db_enabled(self, value):
        """
        sets the value of isdm2db

            Args:
                value   (bool)      --  True/False
         """
        if isinstance(value, bool):
            self._is_dm2_db_enabled = value
        else:
            raise SDKException('DisasterRecovery', '101')


class DisasterRecoveryManagement(object):
    """Class to perform all the disaster recovery management operations on commcell"""

    def __init__(self, commcell):
        """Initializes DisasterRecoveryManagement object

            Args:
            commcell    (object)    --  instance of commcell

        """
        self._commcell = commcell
        self._service = commcell._services.get('DISASTER_RECOVERY_PROPERTIES')
        self._cvpysdk_object = commcell._cvpysdk_object
        self.refresh()

    def _get_dr_properties(self):
        """
        Executes a request on the server to get the settings of disaster recovery Backup.

            Returns:
                None

            Raises:
                SDKException
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(method='GET', url=self._service)
        if flag:
            if response and response.json():
                self._settings_dict = response.json()
                if self._settings_dict.get('errorCode', 0) != 0:
                    raise SDKException('Job', '102', 'Failed to get dr management properties. \nError: {0}'.format(
                        self._settings_dict.get('errorMessage', '')))
                if 'drBackupInfo' in self._settings_dict:
                    self._prepost_settings = self._settings_dict.get('drBackupInfo').get('prePostProcessSettings', {})
                    self._export_settings = self._settings_dict.get('drBackupInfo').get('exportSettings', {})
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _set_dr_properties(self):
        """
        Executes a request on the server, to set the dr settings.

         Returns:
               None
         Raises:
              SDKException:
                    if given inputs are invalid.

        """

        flag, response = self._cvpysdk_object.make_request(method='POST', url=self._service,
                                                           payload=self._settings_dict)
        if flag:
            if response and response.json():
                if int(response.json().get('processinginstructioninfo').get('attributes')[0].get('value', 0)) != 0:
                    if not response.json().get('response', {}):
                        raise SDKException('DisasterRecovery', '102',
                                           'Failed to set dr properties, Received errorcode: {0}'.format(
                                               response.json().get(
                                                   'processinginstructioninfo').get('attributes')[0].get('value')))
                    if response.json().get('response')[0].get('errorCode') != 0:
                        raise SDKException('DisasterRecovery', '102', 'Failed to set dr properties. Error: {0}'.format(
                            response.json().get('response')[0].get('errorString')
                        ))
                self.refresh()
        else:
            raise SDKException('Response', '102')

    def refresh(self):
        """
        refreshs the dr settings associated with commcell.

        Returns:
            None
        """
        self._prepost_settings = None
        self._export_settings = None
        self._get_dr_properties()

    def set_local_dr_path(self, path):
        """
        Sets local DR path

            Args:
                 path       (str)       --         local path.

            Returns:
                None
        """
        if isinstance(path, basestring):
            self._export_settings['backupMetadataFolder'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def set_network_dr_path(self, path, username, password):
        """
        Sets network DR path

            Args:
                 path       (str)       --      UNC path.

                 username   (str)       --      username with admin privileges of the remote machine.

                 password   (str)       --      password.

            Returns:
                None
        """
        if isinstance(path, basestring) and isinstance(username, basestring) and isinstance(password, basestring):
            self._export_settings['backupMetadataFolder'] = path
            self._export_settings['networkUserAccount']['userName'] = username
            self._export_settings['networkUserAccount']['password'] = b64encode(password.encode()).decode()
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def upload_metdata_to_commvault_cloud(self, flag, username=None, password=None):
        """
        Enable/Disable upload metadata to commvault cloud setting.

            Args:
                 flag       (bool)      --      True/False.

                 username   (str)       --      username of the commvault cloud.

                 password   (str)       --      password of the commvault cloud.

            Returns:
                 None
        """
        if isinstance(flag, bool):
            self._export_settings['uploadBackupMetadataToCloud'] = flag
            if flag:
                if isinstance(username, basestring) and isinstance(password, basestring):
                    self._export_settings['cloudCredentials']['userName'] = username
                    self._export_settings['cloudCredentials']['password'] = b64encode(password.encode()).decode()
                else:
                    raise SDKException('DisasterRecovery', '101')
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def upload_metdata_to_cloud_library(self, flag, libraryname=None):
        """
        Enable/Disable upload metadata to cloud library

            Args:
                 flag       (bool)      --      True/False.

                 libraryname   (str)    --      Third party cloud library name.

            Returns:
                None
        """
        if isinstance(flag, bool):
            self._export_settings['uploadBackupMetadataToCloudLib'] = flag
            if flag:
                if isinstance(libraryname, basestring):
                    self._export_settings['cloudLibrary']['libraryName'] = libraryname
                else:
                    raise SDKException('DisasterRecovery', '101')
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    def impersonate_user(self, flag, username, password):
        """
        Enable/Disable Impersonate user option for pre/post scripts.

            Args:
                flag        (bool)      --  True/False.

                username    (str)       --  username with admin privileges.

                password    (str)       --  password for the account.

            Returns:
                None
        """
        if isinstance(flag, bool):
            self._prepost_settings['useImpersonateUser'] = flag
            if flag:
                if isinstance(username, basestring) and isinstance(password, basestring):
                    self._prepost_settings['impersonateUser']['userName'] = username
                    self._prepost_settings['impersonateUser']['password'] = b64encode(password.encode()).decode()
                else:
                    raise SDKException('DisasterRecovery', '101')
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def use_impersonate_user(self):
        """
        gets the impersonate user(True/False)

            Returns:
                  True/False
        """
        return self._prepost_settings.get('useImpersonateUser')

    @property
    def number_of_metadata(self):
        """
         gets the value, Number of metadata folders to be retained.

            Returns:
                number of metadata     (int)
        """
        return self._export_settings.get('numberOfMetadata')

    @number_of_metadata.setter
    def number_of_metadata(self, value):
        """
        Sets the value, Number of metadata folders to be retained.

            Args:
                value       (int)       --      number of metadata folders to be retained.

            Returns:
                None
        """
        if isinstance(value, int):
            self._export_settings['numberOfMetadata'] = value
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def use_vss(self):
        """
        gets the value, use vss()

            Returns:
                True/False
        """
        return self._export_settings.get('isUseVSS')

    @use_vss.setter
    def use_vss(self, flag):
        """
        sets the value, use vss

            Args:
                 flag   (bool)      --      True/Flase

            Returns:
                None
        """
        if isinstance(flag, bool):
            self._export_settings['isUseVSS'] = flag
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def wild_card_settings(self):
        """
        gets the wild card settings

            Returns:
                (str)       --     client logs that are to be backed up
        """
        return self._export_settings.get('wildCardSetting')

    @wild_card_settings.setter
    def wild_card_settings(self, logs):
        """
        sets the wild card setting

            Args:
                 logs    (list)      --      log file names

            Returns:
                  None
        """
        mandatory = "cvd;SIDBPrune;SIDBEngine;CVMA"
        if isinstance(logs, list):
            temp = ''
            for log in logs:
                temp = temp + ';' + log
        else:
            raise Exception('Pass log names in list')
        self._export_settings['wildCardSetting'] = mandatory + temp
        self._set_dr_properties()

    @property
    def backup_metadata_folder(self):
        """
        gets the backup metadata folder

            Returns:
                 (str)      --      Backup metadata folder
        """
        return self._export_settings.get('backupMetadataFolder')

    @property
    def upload_backup_metadata_to_cloud(self):
        """
        gets the upload backup metadata to cloud setting

            Returns:
                 True/False
        """
        return self._export_settings.get('uploadBackupMetadataToCloud')

    @property
    def upload_backup_metadata_to_cloud_lib(self):
        """
        gets the upload metadata to cloud lib

            Returns:
                True/False
        """
        return self._export_settings.get('uploadBackupMetadataToCloudLib')

    @property
    def dr_storage_policy(self):
        """
        gets the storage policy name, that is being used for DR backups

            Returns:
                (str)       --      Name of the storage policy
        """
        return self._export_settings.get('storagePolicy').get('storagePolicyName')

    @dr_storage_policy.setter
    def dr_storage_policy(self, storage_policy_object):
        """
        sets the storage policy for DR jobs

            Args:
                storage_policy_object       (object)        --      object of the storage policy

            Returns:
                None
        """
        if isinstance(storage_policy_object, StoragePolicy):        # add str
            self._export_settings['storagePolicy']['storagePolicyName'] = storage_policy_object.name
            self._export_settings['storagePolicy']['storagePolicyId'] = int(storage_policy_object.storage_policy_id)
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def pre_scan_process(self):
        """
        gets the script path of the pre scan process

            Returns:
                (str)       --      script path
        """
        return self._prepost_settings.get('preScanProcess')

    @pre_scan_process.setter
    def pre_scan_process(self, path):
        """
        sets the pre scan process.

            Args:
                 path   (str)      --   path of the pre scan script

            Returns:
                None
        """
        if isinstance(path, basestring):
            self._prepost_settings['preScanProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def post_scan_process(self):
        """
        gets the script path of the post scan process

            Returns:
                (str)       --      script path
        """
        return self._prepost_settings.get('postScanProcess')

    @post_scan_process.setter
    def post_scan_process(self, path):
        """
         sets the post scan process.

            Args:
                 path   (str)      --   path of the post scan script

            Returns:
                None
        """
        if isinstance(path, basestring):
            self._prepost_settings['postScanProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def pre_backup_process(self):
        """
        gets the script path of the pre backup process

            Returns:
                (str)       --      script path
        """
        return self._prepost_settings.get('preBackupProcess')

    @pre_backup_process.setter
    def pre_backup_process(self, path):
        """
         sets the pre backup process.

            Args:
                 path   (str)      --   path of the pre backup script

            Returns:
                None
        """
        if isinstance(path, basestring):
            self._prepost_settings['preBackupProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def post_backup_process(self):
        """
        gets the script path of the post backup process

            Returns:
                (str)       --      script path
        """
        return self._prepost_settings.get('postBackupProcess')

    @post_backup_process.setter
    def post_backup_process(self, path):
        """
         sets the post backup process.

            Args:
                 path   (str)      --   path of the post backup script

            Returns:
                None
        """
        if isinstance(path, basestring):
            self._prepost_settings['postBackupProcess'] = path
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def run_post_scan_process(self):
        """
        gets the value, run post scan process

            Returns:
                 True/False
        """
        return self._prepost_settings.get('runPostScanProcess')

    @run_post_scan_process.setter
    def run_post_scan_process(self, flag):
        """
        sets the value, run post scan process

            Args:
                 flag      (bool)   --      True/False

            Returns:
                None
        """
        if isinstance(flag, bool):
            self._prepost_settings['runPostScanProcess'] = flag
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')

    @property
    def run_post_backup_process(self):
        """
         gets the value, run post backup process

            Returns:
                 True/False
        """
        return self._prepost_settings.get('runPostBackupProcess')

    @run_post_backup_process.setter
    def run_post_backup_process(self, flag):
        """
        sets the value, run post backup process

            Args:
                 flag      (bool)   --      True/False

            Returns:
                None
        """
        if isinstance(flag, bool):
            self._prepost_settings['runPostBackupProcess'] = flag
            self._set_dr_properties()
        else:
            raise SDKException('DisasterRecovery', '101')
