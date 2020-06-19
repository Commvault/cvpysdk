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
"""
File for operating on a Oracle Instance.

OracleInstance is the only class defined in this file.

OracleInstance: Derived class from Instance Base class, representing an
                            oracle instance, and to perform operations on that instance

OracleInstance:

    __init__()                          --  Constructor for the class

    restore_to_disk                     --  Performs restore to disk(app free restore)

    _get_instance_properties()          --  gets the properties of this instance

    _get_instance_properties_json()     --  gets all the instance related properties
                                            of Oracle instance

    _restore_common_options_json()      --  Setter for the Common options in restore JSON

    _restore_destination_json()         --  Setter for the Oracle destination options in restore JSON


    _get_live_sync_oracleopt_json()     --  Constructs JSON with oracle agent specific options
                                            for configuring live sync

    _live_sync_restore_json()           --  Constructs oracle live sync restore JSON
                                            by combining common and agent specific options

    create_live_sync_schedule()         --  Creates live sync schedule for the given
                                            destination oracle instance

    configure_data_masking_policy()     --  Configures data masking
                                            policy with given parameters

    get_masking_policy_id()             --  To get policy id of
                                            given data masking policy

    standalone_data_masking()           --  Launch standalone data masking
                                            job on given instance

    delete_data_masking_policy()        --  Deletes given data masking policy

    _get_browse_options                 --  To get browse options for oracle instance

    _process_browse_response            --  To process browse response

    log_stream()                        --  Getter for fetching archive log stream count

    oracle_home()                       --  Getter for $ORACLE_HOME of this instance

    version()                           --  Getter for oracle database version

    is_catalog_enabled()                --  Getter to check if catalog is enabled for backups

    catalog_user()                      --  Getter for getting catalog user

    catalog_db()                        --  Getter for catalog database name

    archive_log_dest()                  --  Getter for archivelog destination

    os_user()                           --  Getter for OS user owning oracle software

    cmd_sp()                            --  Getter for command line storage policy

    log_sp()                            --  Getter for log storage policy

    is_autobackup_on()                  --  Getter to check if autobackup is enabled

    db_user()                           --  Getter for SYS database user name

    tns_name()                          --  Getter for TNS connect string

    dbid()                              --  Getter for getting DBID of database

    restore()                           --  Performs restore on the instance
    
    _restore_db_dump_option_json()       --  setter for the oracle dbdump Restore option in restore JSON
    
    _restore_oracle_option_json()       --  setter for the oracle Restore option in restore JSON
    
    _restore_json()                     --  returns the JSON request to pass to the API as per
    the options selected by the user
    
    restore_in_place()                  --  restore for oracle logical dump

"""
from __future__ import unicode_literals
from past.builtins import basestring
from base64 import b64encode
import json
from ..exception import SDKException
from .dbinstance import DatabaseInstance



class OracleInstance(DatabaseInstance):
    """
    Class to represent a standalone Oracle Instance
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Constructor for the class

        Args:
            agent_object    -- instance of the Agent class
            instance_name   -- name of the instance
            instance_id     --  id of the instance

        """
        super(OracleInstance, self).__init__(
            agent_object, instance_name, instance_id)
        self._LIVE_SYNC = self._commcell_object._services['LIVE_SYNC']
        self._dbDump_restore_json = None
        self._oracle_restore_json = None

    def restore_to_disk(self,
                        destination_client,
                        destination_path,
                        backup_job_ids,
                        user_name,
                        password):
        """
        Perform restore to disk [Application free restore] for Oracle

            Args:
                destination_client          (str)   --  destination client name

                destination_path:           (str)   --  destination path

                backup_job_ids              (list)  --  list of backup job IDs
                                                        to be used for disk restore

                user_name                   (str)   --  impersonation user name to
                                                        restore to destination client

                password                    (str)   --  impersonation user password

            Returns:
                object -     Job containing restore details

            Raises:
                SDKException
                    if backup_job_ids not given as list of items

        """
        if not isinstance(backup_job_ids, list):
            raise SDKException('Instance', '101')
        request_json = self._get_restore_to_disk_json(destination_client,
                                                      destination_path,
                                                      backup_job_ids,
                                                      user_name,
                                                      password)
        return self._process_restore_response(request_json)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(OracleInstance, self)._get_instance_properties()
        self._instanceprop = self._properties['oracleInstance']

    def _get_instance_properties_json(self):
        """ Gets all the instance related properties of Informix instance.

           Returns:
                dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties":
                {
                    "instance": self._instance,
                    "oracleInstance": self._instanceprop
                }
        }
        return instance_json

    @property
    def log_stream(self):
        """
        Getter to fetch log stream count at instance level

            Returns:
                    int     --  log stream count atinstance level

        """
        return self._instanceprop.get("numberOfArchiveLogBackupStreams")

    @log_stream.setter
    def log_stream(self, log_stream=1):
        """
        Setter to set log stream count at instance level

            Args:
                log_stream    (int)    --  log stream count at instance level
                                           default = 1
        """
        self._set_instance_properties(
            "_instanceprop['numberOfArchiveLogBackupStreams']", log_stream)

    def _restore_common_options_json(self, value):
        """
        Setter for the Common options in restore JSON

            Args:
                value   (dict)  --  dict of common options
                                    for restore json

        """
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')
        super()._restore_common_options_json(value)
        if value.get("baseline_jobid"):
            self._commonoption_restore_json = (
                {
                    "clusterDBBackedup": value.get("clusterDBBackedup", False),
                    "restoreToDisk": value.get("restoreToDisk", False),
                    "baselineBackup": 1,
                    "baselineRefTime": value.get("baseline_ref_time", ""),
                    "isDBArchiveRestore": value.get("isDBArchiveRestore", False),
                    "baselineJobId": value.get("baseline_jobid", ""),
                    "copyToObjectStore": value.get("copyToObjectStore", False),
                    "onePassRestore": value.get("onePassRestore", False),
                    "syncRestore": value.get("syncRestore", True)
                })

    def _restore_destination_json(self, value):
        """
        Setter for the Oracle destination options in restore JSON

            Args:
                    value   (dict)  --  dict of values for destination option

        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = (
            {
                "noOfStreams": value.get("number_of_streams", 2),
                "destClient": {
                    "clientName": value.get("destination_client", "")
                              },
                "destinationInstance": {
                    "clientName": value.get("destination_client", ""),
                    "instanceName": value.get("destination_instance", ""),
                    "appName": "Oracle"
                                       }

            })

    def _get_live_sync_oracleopt_json(self):
        """
               Constructs JSON with oracle agent specific options
               for configuring live sync

        """

        self._oracle_options = {"renamePathForAllTablespaces":"",
                                "redirectAllItemsSelected": False,
                                "validate": False,
                                "ctrlRestoreFrom": True,
                                "noCatalog": True,
                                "cloneEnv":False,
                                "ctrlFileBackupType": 0,
                                "restoreControlFile": True,
                                "duplicate": False,
                                "tableViewRestore": False,
                                "osID":2,
                                "partialRestore": False,
                                "restoreStream":2,
                                "restoreSPFile": False,
                                "recover": True,
                                "oraExtendedRstOptions": 0,
                                "recoverFrom": 3,
                                "archiveLog": False,
                                "restoreData": True,
                                "restoreFrom": 3,
                                "crossmachineRestoreOptions": {
                                "onlineLogDest": ""
                                    },
                                "liveSyncOpt":{
                                    "restoreInStandby":False
                                }
                                }


    def _live_sync_restore_json(self, dest_client, dest_instance, baseline_jobid,
                                baseline_ref_time, schedule_name, source_backupset_id):
        """
               Constructs oracle live sync restore JSON by combining common
               and agent specific options

                   Args:
                       dest_client  (str)   --  The destination client name for live sync

                       dest_instance    (str)   --  The destination instance name for live sync

                       baseline_jobid   (int)   --  The jobid of the baseline backup job

                       baseline_ref_time    (int)   --  The reference time/start time
                                                        of the baseline backup

                       schedule_name    (str)   --  The name of the live sync schedule to be created

                       source_backupset_id  (int)   --  The ID of the source backupset
                                                        of source oracle instance for which
                                                        live sync needs to be configured

                    Returns:
                        (str)  --   The live sync restore JSON that is constructed
                                    using oracle and common options

        """

        restore_json = super()._restore_json(destination_client=dest_client,
                                             destination_instance=dest_instance,
                                             baseline_jobid=baseline_jobid,
                                             baseline_ref_time=baseline_ref_time,
                                             syncRestore=True,
                                             no_of_streams=2,
                                            )
        restore_option = {}
        if restore_json.get("restore_option"):
            restore_option = restore_json["restore_option"]
            for key in restore_json:
                if not key == "restore_option":
                    restore_option[key] = restore_json[key]
        else:
            restore_option.update(restore_json)

        self._get_live_sync_oracleopt_json()
        restore_json['taskInfo']['associations'][0]['subclientId'] = -1
        restore_json['taskInfo']['associations'][0]['backupsetId'] = source_backupset_id
        restore_json['taskInfo']['associations'][0]['subclientName'] = ""
        restore_json['taskInfo']['associations'][0]['backupsetName'] = ""
        restore_json['taskInfo']['associations'][0]['_type_'] = 5
        restore_json['taskInfo']['task']['taskType'] = 2
        restore_json['taskInfo']['subTasks'][0]['subTask']['operationType'] = 1007
        restore_json['taskInfo']['subTasks'][0]['subTask']['subTaskName'] = schedule_name
        restore_json['taskInfo']['subTasks'][0]['pattern'] = {
            "freq_type": 4096
        }
        destinationInstance = {
            "clientName":dest_client,
            "instanceName":dest_instance,
            "appName":"Oracle"
        }
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["destination"].update({"destinationInstance":destinationInstance})
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["oracleOpt"] = self._oracle_options
        return restore_json


    def create_live_sync_schedule(self, dest_client, dest_instance, schedule_name):
        """
               Runs full backup on source oracle instance and
               Creates live sync schdule for the given destination oracle instance

                   Args:
                       dest_client  (str)   --  The destination client name for live sync

                       dest_instance    (str)   --  The destination instance name for live sync

                       schedule_name    (str)   --  The name of the live sync schedule to be created

                   Returns:
                        (object)  --   The job object of the baseline backup that will be replicated

        """
        source_backupset_id = int(self.backupsets.get('default').backupset_id)
        subclient_obj = self.subclients.get('default')
        baseline_job_object = subclient_obj.backup(backup_level='full')
        if not baseline_job_object.wait_for_completion():
            raise SDKException('Instance', '102', baseline_job_object.delay_reason)
        baseline_ref_time = baseline_job_object.summary['jobStartTime']
        baseline_jobid = int(baseline_job_object.job_id)
        request_json = self._live_sync_restore_json(dest_client, dest_instance, baseline_jobid,
                                                    baseline_ref_time, schedule_name, source_backupset_id)
        flag, response = self._cvpysdk_object.make_request('POST', self._LIVE_SYNC, request_json)
        if flag:
            if response.json():
                if "taskId" in response.json():
                    return baseline_job_object
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    error_message = 'Live Sync configuration failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Instance', '102', error_message)
                else:
                    raise SDKException('Instance', '102', 'Failed to create schedule')
            else:
                raise SDKException('Instance', '102')
        else:
            raise SDKException('Instance', '101', self._update_response_(response.text))


    def configure_data_masking_policy(self, policy_name, table_list_of_dict):
        """Configures data masking policy with given parameters
        Args:
            policy_name         (str)   --  string representing policy name
            table_list_of_dict  list(dict)  -- list containing one dict item representing
                                                rules for single table
            Sample  list
            Tables:
                    [
                    {
                    "name":"schema_name.table_name",
                    "columns": [ {"name":"column_name", "type":"algorithm_type"},
                                "arguments":[list of strings]…]
                    }
                    ]
                    Sample :
                    [
                    {
                    "name":"HR.NUMNEW",
                    "columns":[{"name":"N1","type":0},{"name":"N2","type":2,
                    "arguments":["1000","2000"]}]
                    },
                    {
                    "name":"HR.CHANGE",
                    "columns":[{"name":"C1","type":1},{"name":"C2","type":1}]
                    }
                    ]
            schema_name , table_name, column_name: str
            Column type key in main dict takes list of dict as value :
            This list of dict represents each column name and type of algorithm
            and arguments if any for that algorithm
            arguments : list of strings

            Choose appropriate algorithm type and pass necessary arguments based
            on column type

            Algorithm       Arguments mandatory       Arguments Format        Algorithm type number

            Shuffling           NA                              NA                      0
            Numeric Range       [min, max]                  ["1000","2000"]             2
            Numeric Variance    [variance percentage]           ["50"]                  3
            FPE                 NA                              NA                      1
            Fixed String        string_to_replace           ["string_to_replace"]       4


            Supported Algorithms :

            Column Type     Algorithms Supported

            Numeric         Shuffling, FPE, Numeric Range, Numeric Variance
            Char            Shuffling , FPE , Fixed String
            Varchar         Shuffling , FPE , Fixed String

        """
        request_json = {
            "opType": 2,
            "policy": {
                "association": {"instanceId": int(self.instance_id)},
                "config": {"tables": table_list_of_dict},
                "policy": {"policyName": policy_name}
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['MASKING_POLICY'], request_json
        )
        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code != 0:
                    error_string = response.json()['errorMessage']
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while creating Data masking policy\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    return True

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text))

    def get_masking_policy_id(self, policy_name):
        """Returns policy id of given data masking policy
        Args:
            policy_name          (str)       -- data masking policy name

        Returns:
            policy_id            (int)       -- data masking policy ID

        """
        instance_id = int(self.instance_id)
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['MASKING_POLICY'])
        response_json = response.json()
        policy_list = response_json["policies"]
        policy_id = None
        for i in policy_list:
            pname = i["policy"]["policyName"]
            associated_instance_id = i["association"]["instanceId"]
            if (pname == policy_name) and (associated_instance_id == instance_id):
                policy_id = int(i["policy"]["policyId"])
                break
            else:
                continue
        return policy_id

    def delete_data_masking_policy(self, policy_name):
        """Deletes given data masking policy
        Args:
            policy_name         (str)       --  data masking policy name to be deleted

        Returns:
            bool                            -- returns true when deletion succeeds

        Raises:
            Exception

                When deletion of policy fails

                When Invalid policy name under given instance is provided
        """
        source_instance_id = int(self.instance_id)
        policy_id = self.get_masking_policy_id(policy_name)
        if policy_id is None:
            raise SDKException(
                'Instance',
                '106')

        request_json = {
            "opType": 3,
            "policy": {
                "association": {"instanceId": source_instance_id},
                "policy": {"policyId": policy_id, "policyName": policy_name}
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['MASKING_POLICY'], request_json
        )
        if flag:
            if response.json():
                error_code = response.json()['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Instance',
                        '102',
                        'Error while deleting Data masking policy\nError')
                else:
                    return True

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101',
                               self._update_response_(response.text))

    def standalone_data_masking(
            self,
            policy_name,
            destination_client=None,
            destination_instance=None):
        """Launch standalone data masking job on given instance

        Args:

            policy_name          (str)       -- data masking policy name

            destination_client   (str)       -- destination client in which destination
            instance exists

            destination_instance (str)       -- destination instance to which masking
            to be applied

        Returns:
            object -- Job containing data masking job details


        Raises:
            SDKException
                if policy ID retrieved is None

        """
        if destination_client is None:
            destination_client = self._properties['instance']['clientName']
        if destination_instance is None:
            destination_instance = self.instance_name
        destination_client_object = self._commcell_object.clients.get(
            destination_client)
        destination_agent_object = destination_client_object.agents.get(
            'oracle')
        destination_instance_object = destination_agent_object.instances.get(
            destination_instance)
        destination_instance_id = int(destination_instance_object.instance_id)
        source_instance_id = int(self.instance_id)
        policy_id = self.get_masking_policy_id(policy_name)
        if policy_id is None:
            raise SDKException(
                'Instance',
                '106')
        request_json = self._restore_json(paths=r'/')
        destination_instance_json = {
            "clientName": destination_client,
            "instanceName": destination_instance,
            "instanceId": destination_instance_id
        }
        data_masking_options = {
            "isStandalone": True,
            "enabled": True,
            "dbDMPolicy": {
                "association": {
                    "instanceId": source_instance_id},
                "policy": {
                    "policyId": policy_id,
                    "policyName": policy_name}}}
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["destination"]["destClient"]["clientName"] = destination_client
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["destination"]["destinationInstance"] = destination_instance_json
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["dbDataMaskingOptions"] = data_masking_options
        del request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"]
        return self._process_restore_response(request_json)

    def _get_oracle_restore_json(self, destination_client,
                                 instance_name, tablespaces,
                                 files, browse_option,
                                 common_options, oracle_options):
        """
        Gets the basic restore JSON from base class and modifies it for oracle

        Args:
            destination_client  (str)   --  Destination client name

            instance_name   (str)   --  instance name to restore

            tablespaces (list)  --  tablespace name list

            files   (dict)  --  fileOptions

            browse_option   (dict)  --  dict containing browse options

            common_options  (dict)  --  dict containing common options

            oracle_options  (dict)  --  dict containing other oracle options

        Returns:
            (dict) -- JSON formatted options to restore the oracle database

        Raises:
            TypeError:
                if tablespace is passed as a list
                if files is not passed as a dictionary

        """
        if not isinstance(tablespaces, list):
            raise TypeError('Expecting a list for tablespaces')
        if files is not None:
            if not isinstance(files, dict):
                raise TypeError('Expecting a dict for files')

        destination_id = int(self._commcell_object.clients.get(
            destination_client).client_id)
        tslist = ["SID: {0} Tablespace: {1}".format(
            instance_name, ts) for ts in tablespaces]
        restore_json = self._restore_json(paths=r'/')
        if common_options is not None:
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "commonOptions"] = common_options
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "oracleOpt"] = oracle_options
        if files is None:
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"] = {
                "sourceItem": tslist
            }
        else:
            restore_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]["fileOption"] = files

        if browse_option is not None:
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "browseOption"] = browse_option
        return restore_json

    def _get_browse_options(self):
        """Returns the database instance properties for browse and restore"""
        return {
            "path": "/",
            "entity": {
                "appName": self._properties['instance']['appName'],
                "instanceId": int(self.instance_id),
                "applicationId": int(self._properties['instance']['applicationId']),
                "clientId": int(self._properties['instance']['clientId']),
                "instanceName": self._properties['instance']['instanceName'],
                "clientName": self._properties['instance']['clientName']
            }
        }

    def _process_browse_response(self, request_json):
        """Runs the DBBrowse API with the request JSON provided for Browse,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                list - list containing tablespaces for the instance

            Raises:
                SDKException:
                    if browse job failed

                    if browse is empty

                    if browse is not success
        """
        if 'tablespaces' in self._instanceprop:
            return self._instanceprop['tablespaces']

        browse_service = self._commcell_object._services['ORACLE_INSTANCE_BROWSE'] % (
            self.instance_id
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', browse_service, request_json
        )

        if flag:
            response_data = json.loads(response.text)
            if response_data:
                if "oracleContent" in response_data:
                    self._instanceprop['tablespaces'] = response_data["oracleContent"]
                    return self._instanceprop['tablespaces']
                elif "errorCode" in response_data:
                    error_message = response_data['errorMessage']
                    o_str = 'Browse job failed\nError: "{0}"'.format(
                        error_message)
                    raise SDKException('Instance', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def oracle_home(self):
        """
        getter for oracle home

        Returns:
            string - string of oracle_home

        """
        return self._properties['oracleInstance']['oracleHome']

    @property
    def is_catalog_enabled(self):
        """
        Getter to check if catalog has been enabled

        Returns:
            Bool - True if catalog is enabled. Else False.

        """
        return self._properties['oracleInstance']['useCatalogConnect']

    @property
    def catalog_user(self):
        """
        Getter for catalog user

        Returns:
            string  - String containing catalog user

        Raises:
            SDKException:
                if not set

                if catalog is not enabled

        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['userName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102',
                               'Catalog user not set - {}'.format(error_str))

    @property
    def catalog_db(self):
        """
        Getter for catalog database

        Returns:
            string  - String containing catalog database

        Raises:
            SDKException:
                if not set

                if catalog is not enabled

        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102',
                               'Catalog database not set - {}'.format(error_str))

    @property
    def os_user(self):
        """
        Getter for oracle software owner

        Returns:
            string - string of oracle software owner

        """
        return self._properties['oracleInstance']['oracleUser']['userName']

    @property
    def version(self):
        """
        Getter for oracle version

        Returns:
            string - string of oracle instance version

        """
        return self._properties['version']

    @property
    def archive_log_dest(self):
        """
        Getter for the instance's archive log dest

        Returns:
            string - string for archivelog location

        """
        return self._properties['oracleInstance']['archiveLogDest']

    @property
    def cmd_sp(self):
        """
        Getter for Command Line storage policy

        Returns:
            string - string for command line storage policy

        """
        return self._properties['oracleInstance']['oracleStorageDevice'][
            'commandLineStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self):
        """
        Oracle Instance's Log Storage Poplicy

        Returns:
            string  -- string containing log storage policy

        """
        return self._properties['oracleInstance']['oracleStorageDevice'][
            'logBackupStoragePolicy']['storagePolicyName']

    @property
    def is_autobackup_on(self):
        """
        Getter to check whether autobackup is set to ON

        Returns:
            Bool - True if autobackup is set to ON. Else False.

        """
        return True if self._properties['oracleInstance']['ctrlFileAutoBackup'] == 1 else False

    @property
    def db_user(self):
        """
        Getter to get the database user used to log into the database

        Returns: Oracle database user for the instance

        """
        return self._properties['oracleInstance']['sqlConnect']['userName']

    @property
    def tns_name(self):
        """
        Getter to get the TNS Names of the database

        Returns:
            string  -- TNS name of the instance configured

        Raises:
            SDKException:
                if not set

        """
        try:
            return self._properties['oracleInstance']['sqlConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102',
                               'Instance TNS Entry not set - {}'.format(error_str))

    @property
    def dbid(self):
        """
        Getter to get the DBID of the database instance

        Returns: DBID of the oracle database

        """
        return self._properties['oracleInstance']['DBID']

    @property
    def tablespaces(self):
        """
        Getter for listing out all tablespaces for the instance

        Returns:
            list -- list containing tablespace names for the database

        """
        return [ts['tableSpace'] for ts in self.browse()]

    def browse(self, *args, **kwargs):
        """Overridden method to browse oracle database tablespaces"""
        if args and isinstance(args[0], dict):
            options = args[0]
        elif kwargs:
            options = kwargs
        else:
            options = self._get_browse_options()
        return self._process_browse_response(options)

    def backup(self, subclient_name=r"default"):
        """Uses the default subclient to backup the database

        Args:
            subclient_name (str) -- name of subclient to use
                default: default
        """
        return self.subclients.get(subclient_name).backup(r'full')

    def restore(
            self,
            files=None,
            destination_client=None,
            common_options=None,
            browse_option=None,
            oracle_options=None,
            tag=None):
        """
        Perform restore full/partial database using latest backup or backup copy

        Args:
            files               (dict)      --  fileOption for restore

            destination_client  (str)       --  destination client name

            common_options      (dict)      --  dictionary containing common options
                default:    None

            browse_option       (dict)      --  dictionary containing browse options

            oracle_options      (dict)      --  dictionary containing other oracle options
                default:    By default it restores the controlfile and datafiles from latest backup

            tag                 (str)       --  Type of the restore to be performed
                default:    None

            Example: {
            "resetLogs": 1,
            "switchDatabaseMode": True,
            "noCatalog": True,
            "restoreControlFile": True,
            "recover": True,
            "recoverFrom": 3,
            "restoreData": True,
            "restoreFrom": 3
            }

        Returns:
            object  --  Job containing restore details

        Raises:
            TypeError   --  If the oracle options is not a dict
            SDKException    --  If destination_client can't be set

        """
        if oracle_options is None:
            oracle_options = {
                "resetLogs": 1,
                "switchDatabaseMode": True,
                "noCatalog": True,
                "recover": True,
                "recoverFrom": 3,
                "restoreData": True,
                "restoreFrom": 3
            }

        if tag.lower() == 'snap':
            opt = {
                "useSnapRestore": True,
                "cleanupAuxiliary": True,
                "restoreControlFile": True,
            }
            oracle_options.update(opt)

        try:
            if destination_client is None:
                destination_client = self._properties['instance']['clientName']
        except SDKException:
            raise SDKException("Instance", "105")
        else:
            # subclient = self.subclients.get(subclient_name)
            options = self._get_oracle_restore_json(destination_client=destination_client,
                                                    instance_name=self.instance_name,
                                                    tablespaces=self.tablespaces,
                                                    files=files,
                                                    browse_option=browse_option,
                                                    common_options=common_options,
                                                    oracle_options=oracle_options)
            return self._process_restore_response(options)
            
    

    def _restore_db_dump_option_json(self,value):
        """setter for the oracle dbdump Restore option in restore JSON
            Args:
                value   (dict)  --  Dictionary of options need to be set for restore
        """
        if not isinstance(value,dict):
            raise SDKException('Instance','101')
            
        self._db_dump_restore_json = {
            "importToDatabase": True,
            "parallelism": 2,
            "restorePath": value.get("destination_path", ""),
            "overwriteTable": False,
            "enabled": True,
            "connectDetails": {
                "password": b64encode(value.get("db_password", "").encode()).decode(),
                "domainName": (self._properties.get("oracleInstance", {}).
                    get("sqlConnect", {}).get("domainName", "")),
                "userName": (self._properties.get("oracleInstance", {}).
                    get("sqlConnect", {}).get("userName", ""))
            }
        }


    def _restore_oracle_option_json(self, value):
        """setter for the oracle Restore option in restore JSON
        Args:
                value   (dict)  --  Dictionary of options need to be set for restore
        """
        if not isinstance(value,dict):
            raise SDKException('Instance','101')
            
        self._oracle_restore_json = {
            "validate": False,
            "noCatalog": False,
            "duplicateToName": "",
            "cloneEnv": False,
            "restoreControlFile": False,
            "duplicate": False,
            "tableViewRestore": False,
            "osID": 2,
            "partialRestore": False,
            "restoreStream": 2,
            "restoreSPFile": False,
            "recover": True,
            "recoverFrom": 4,
            "archiveLog": False,
            "restoreData": True,
            "restoreFrom": 0,
            "timeZone": {
                "TimeZoneName": "(UTC) Coordinated Universal Time"
            },
            "recoverTime": {},
            "sourcePaths": [
                "//**"
            ],
            "restoreTime": {}
        }
        
    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (dict)  --  Dictionary of options need to be set for restore

            Returns:
                dict             -- JSON request to pass to the API

        """
        rest_json = super(OracleInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        self._restore_db_dump_option_json(restore_option)
        self._restore_oracle_option_json(restore_option)
        rest_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["dbDumpOptions"] = self._db_dump_restore_json
        rest_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["oracleOpt"] = self._oracle_restore_json

        return rest_json

    def restore_in_place(
            self,
            db_password,
            path,
            dest_client_name,
            dest_instance_name,
            dest_path=None):
        """Restores the oracle logical dump data/log files specified in the input paths
        list to the same location.

            Args:
                
                db_password             (str)  -- password for oracle database
                
                path                    (list)  --  list of database/databases to be restored

                dest_client_name        (str)   --  destination client name where files are to be
                restored

                dest_instance_name      (str)   --  destination postgres instance name of
                destination client

                dest_path        (str)   --  destinath path for restore

                    default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        if not (isinstance(path, list) and
                isinstance(db_password, basestring)):
            raise SDKException('Instance', '101')
        if not path:
            raise SDKException('Instance','103')
        

        request_json = self._restore_json(
            db_password=db_password,
            paths=path,
            destination_client=dest_client_name,
            destination_instance=dest_instance_name,
            destination_path=dest_path)

        return self._process_restore_response(request_json)