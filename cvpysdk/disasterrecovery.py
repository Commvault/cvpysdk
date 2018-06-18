# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Class to perform all the disaster recovery operations on commcell

DisasterRecovery is the only class defined in this file

DisasterRecovery: Helper class to perform DR operations

DisasterRecovery:

    __init__()                    --  initializes DR helper object

    disaster_recovery_backup()    --  function to run DR backup

    _process_drbackup_response()  -- process the disaster recovery backup request

    restore_out_of_place()        -- function to run DR restore operation

    drbackupwithjson()            -- Run DR backup with JSON including clients with
                                     sendlogfiles.

    _generatedrbackupjson()       -- Generate JSON corresponds to DR backup job

    _process_createtask_response()-- Runs the CreateTask API with the request JSON
                                     provided for DR backup.

    _filter_paths()               -- Filters the paths based on the Operating System and Agent.

"""


from cvpysdk.job import Job
from cvpysdk.exception import SDKException
from cvpysdk.client import Client


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
        self.iscompressionenabled = True
        self._RESTORE = self.commcell._services['RESTORE']
        self.backuptype = "full"
        self._CREATE_TASK = self.commcell._services['CREATE_TASK']
        self.ishistorydb = True
        self.isworkflowdb = True
        self._client_list = None
        self.advbackup = False

    @property
    def client_list(self):
        """Treats the client_list as a read-only attribute."""
        return self._client_list

    @client_list.setter
    def client_list(self, value):
        """Treats the client_list as a read-only attribute."""
        self._client_list = value

    @property
    def iscompression_enabled(self):
        """Treats the iscompressionenabled as a read-only attribute."""
        return self.iscompressionenabled

    @iscompression_enabled.setter
    def iscompression_enabled(self, value):
        """Treats the iscompressionenabled as a read-only attribute."""
        self.iscompressionenabled = value

    @property
    def backup_type(self):
        """Treats the backup_type as a read-only attribute."""
        return self.backuptype

    @backup_type.setter
    def backup_type(self, value):
        """Treats the backup_type as a read-only attribute."""
        self.backuptype = value

    def disaster_recovery_backup(self):
        """Runs a DR job for Commserv

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / / Differential
                    default: Full


            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """

        if self.backuptype.lower() not in ['full', 'differential']:
            raise SDKException('Response', '103')
        backuptypes = {"full": 1, "differential": 3}
        if self.advbackup:
            self.backuptype = backuptypes[self.backuptype.lower()]
            return self._advanced_dr_backup()
        else:
            dr_service = self.commcell._services['DRBACKUP']
            request_json = {"isCompressionEnabled": self.iscompression_enabled,
                            "jobType": 1, "backupType": backuptypes[self.backuptype.lower()]}
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
                elif "errorCode" in response.json():
                    o_str = 'Initializing backup failed\nError: "{0}"'.format(
                        response.json()['errorMessage']
                    )
                    raise SDKException('Response', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
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
            fs_options=None):
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
        if not ((isinstance(client, str) or isinstance(client, Client)) and
                isinstance(destination_path, str)and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Response', '101')

        if fs_options is None:
            fs_options = {}

        if isinstance(client, Client):
            client = client
        elif isinstance(client, str):
            client = Client(self.commcell, client)
        else:
            raise SDKException('Response', '105')
        drpath = self.path + "\\CommserveDR"
        destination_path = self._filter_paths([destination_path], True)
        drpath = [self._filter_paths([drpath], True)]
        if drpath == []:
            raise SDKException('Response', '104')

        #client_obj = self.commcell.clients.get(self.commcell.commserv_name)
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
            fs_options=fs_options)

    def _advanced_dr_backup(self):
        """Runs a DR job with JSON input

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / / Differential / Synthetic_full
                    default: Full


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
                "initiatedFrom": "COMMANDLINE"
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

            self._droptions = {
                "drbackupType": self.backuptype, "dbName": "commserv",
                "backupHistoryDataBase": self.ishistorydb,
                "backupWFEngineDataBase": self.isworkflowdb,
                "enableDatabasesBackupCompression": self.iscompression_enabled,
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
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'DR backup job failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Response', '102', o_str)
                else:
                    raise SDKException(
                        'Response', '102', 'Failed to run the DR backup job')
            else:
                raise SDKException('Response', '102')
        else:
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
        else:
            return paths
