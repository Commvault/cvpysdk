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

"""File for operating on a SAP Oracle Instance.

SAPOracleInstance is the only class defined in this file.

SAPOracleInstance: Derived class from Instance Base class, representing a SAPOracle instance,
                       and to perform operations on that instance

SAPOracleInstance:
    __init__()                          -- Constructor for the class


    oracle_home()                       -- Getter for $ORACLE_HOME of this instance

    sapdata_home()                      -- Getter for $SAPDATA_HOME of this instance

    sapexepath()                        -- Getter for $SAPEXE of this instance

     os_user()                          -- Getter for OS user owning oracle software

    cmd_sp()                            -- Getter for command line storage policy

    log_sp()                            -- Getter for log storage policy

    db_user()                           -- Getter for SYS database user name

    saporacle_db_connectstring()        -- Getter for getting oracle database connect string

    saporacle_blocksize()               -- Getter for getting blocksize value

    saporacle_sapsecurestore()          -- Getter for getting sapsecure store option

    saporacle_archivelogbackupstreams() -- Getter for getting archivelog backup streams

    saporacle_instanceid()              -- Getter for getting InstanceId
    
    saporacle_snapbackup_enable()       -- Getter for getting Snap backup enabled or not
    
    saporacle_snapengine_name()         -- Getter for getting snap enginename

    _restore_request_json()             -- returns the restore request json

    _process_restore_response()         -- processes response received for the Restore request

    restore_in_place()                  -- runs the restore job for specified instance

    restore_outof_place()               -- runs the restore job for specified client and instance

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ..agent import Agent
from ..instance import Instance
from ..client import Client
from ..exception import SDKException


class SAPOracleInstance(Instance):
    """Derived class from Instance Base class, representing a SAPOracle instance,
        and to perform operations on that Instance."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Constructor for the class

        Args:
            agent_object    -- instance of the Agent class
            instance_name   -- name of the instance
            instance_id     --  id of the instance

        """
        super(SAPOracleInstance, self).__init__(agent_object, instance_name, instance_id)
        self._instanceprop = {}  # variable to hold instance properties to be changed

    @property
    def oracle_home(self):
        """
        getter for oracle home
        Returns:
            string - string of oracle_home
        """
        return self._properties['sapOracleInstance']['oracleHome']

    @property
    def sapdata_home(self):
        """
        getter for sapdata home
        Returns:
            string - string of sapdata_home
        """
        return self._properties['sapOracleInstance']['sapDataPath']

    @property
    def sapexepath(self):
        """
        getter for sapexepath
        Returns:
            string - string of sapexepath
        """
        return self._properties['sapOracleInstance']['sapExeFolder']

    @property
    def os_user(self):
        """
        Getter for oracle software owner
        Returns:
            string - string of oracle software owner
        """
        return self._properties['sapOracleInstance']['oracleUser']['userName']

    @property
    def cmd_sp(self):
        """
        Getter for Command Line storage policy
        Returns:
            string - string for command line storage policy
        """
        return self._properties['sapOracleInstance']['oracleStorageDevice'][
            'commandLineStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self):
        """
        Oracle Instance's Log Storage Poplicy
        Returns:
            string  -- string containing log storage policy
        """
        return self._properties['sapOracleInstance']['oracleStorageDevice'][
            'logBackupStoragePolicy']['storagePolicyName']

    @property
    def saporacle_db_user(self):
        """
        Returns: Oracle database user for the instance
        """
        return self._properties['sapOracleInstance']['sqlConnect']['userName']

    @property
    def saporacle_db_connectstring(self):
        """
        Returns: Oracle database connect string for the instance
        """
        return self._properties['sapOracleInstance']['sqlConnect']['domainName']

    @property
    def saporacle_blocksize(self):
        """
        Returns: blocksize for the instance
        """
        return self._properties['sapOracleInstance']['blockSize']

    @property
    def saporacle_sapsecurestore(self):
        """
        Returns: sapsecurestore option for the instance
        """
        return self._properties['sapOracleInstance']['useSAPSecureStore']

    @property
    def saporacle_archivelogbackupstreams(self):
        """
        Returns: archivelogbackupstreams option for the instance
        """
        return self._properties['sapOracleInstance']['numberOfArchiveLogBackupStreams']

    @property
    def saporacle_instanceid(self):
        """
        Returns: saporacle_instanceid option for the instance
        """
        return self._properties['instance']['instanceId']
    
    @property
    def saporacle_snapbackup_enable(self):
        """
        Returns: saporacle_snapbackup_enable option for the instance
        """
        return self._properties['sapOracleInstance']['snapProtectInfo']['isSnapBackupEnabled']
    
    @property
    def saporacle_snapengine_name(self):
        """
        Returns: saporacle_snapengine_name option for the instance
        """
        return self._properties['sapOracleInstance']['snapProtectInfo']['snapSelectedEngine']['snapShotEngineName']

    def _restore_saporacle_request_json(self, value):
        """Returns the JSON request to pass to the API as per the options selected by the user.

        """
        if self._restore_association is None:
            self._restore_association = self._instance
        request_json = {
            "taskInfo": {
                "associations": [self._restore_association],
                "task": self._task,
                "subTasks": [{
                    "subTask": self._restore_sub_task,
                    "options": {
                        "restoreOptions": {
                            "oracleOpt": {
                                "noCatalog": value.get("noCatalog", True),
                                "backupValidationOnly": value.get("backupValidationOnly", False),
                                "restoreData": value.get("restoreData", True),
                                "archiveLog": value.get("archiveLog", True),
                                "recover": value.get("recover", True),
                                "switchDatabaseMode": value.get("switchDatabaseMode", True),
                                "restoreStream": value.get("restoreStream", 1),
                                "restoreControlFile": value.get("restoreControlFile", True),
                                "partialRestore": value.get("partialRestore", False),
                                "openDatabase": value.get("openDatabase", True),
                                "resetLogs": value.get("resetLogs", 1),
                                "restoreTablespace": value.get("restoreTablespace", False),
                                "databaseCopy": value.get("databaseCopy", False),
                                "archiveLogBy": value.get("archiveLogBy", 'default'),
                                "recoverTime":{
                                    "time":value.get("point_in_time", 0)},
                            },
                            
                            "destination": {
                                "destinationInstance": {
                                    "clientName": value.get("destination_client"),
                                    "appName": self._agent_object.agent_name,
                                    "instanceName": value.get("destination_instance")
                                },
                                "destClient": {
                                    "clientName":value.get("destination_client")
                                }
                            },
                            "fileOption": {
                                "sourceItem": value.get("sourceItem", ["/+BROWSE+"])
                            },
                            "browseOption": {
                                "backupset": {
                                    "clientName": self._agent_object._client_object.client_name
                                },
                                "mediaOption":{
                                     "copyPrecedence": {
                                             "copyPrecedenceApplicable": value.get("copyPrecedenceApplicable", False),
                                             "copyPrecedence":value.get("copyPrecedence", 0)}}
                            }
                        }
                    }
                }]
            }
        }
        return request_json

    def restore_in_place(
            self,
            destination_client=None,
            destination_instance=None,
            sap_options=None):
        """perform inplace restore and recover  of sap oracle database
         Args:

            destination_client        (str)         --  destination client name where saporacle
                                                          client package exists if this value
                                                          not provided,it will automatically
                                                          use source backup client
            destination_instance        (str)       --  destination instance name where saporacle
                                                        client package exists if this value not
                                                         provided,it will automatically use
                                                          source backup instance
            sap_options                (dict)

                backupset_name         (str)        --  backupset name of the instance to be
                                                            restored. If the instance is a single
                                                            DB instance then the backupset name is
                                                            ``default``.
                    default: default

                restoreData               (bool)   --  RestoreData  if true mean restore data
                                                          is selected.
                                                        true - restore data selected
                                                        false - restore data unselected

                    default:true

                streams                  (int)      :  no of streams to use for restore
                    default:2

                copyPrecedence          (int)      :  copy number to use for restore
                    default:0

                archiveLog               (bool)     :  Restore archive log
                                                        true - restore archive log selected
                                                        false - restore archive log unselected
                     default: True

                recover                  (bool)     :  recover database
                                                        true - recover database selected
                                                        false - recover database unselected
                     default: True

                switchDatabaseMode       (bool)     :  switchDatabaseMode option
                                                        true - switchDatabaseMode selected
                                                        false - switchDatabaseMode unselected
                     default: True

                restoreControlFile       (bool)     :  restoreControlFile option
                                                        true - restoreControlFile selected
                                                        false - restoreControlFile unselected
                     default: True

                partialRestore       (bool)         :  partialRestore option
                                                        true - partialRestore selected
                                                        false - partialRestore unselected
                     default: False

                openDatabase       (bool)           :  openDatabase option
                                                        true - openDatabase selected
                                                        false - openDatabase unselected
                     default: True

                resetLogs       (bool)              :  resetLogs option
                                                        true - resetLogs selected
                                                        false - resetLogs unselected
                     default: True

                point_in_time            (str)      :  date to use for restore and recover  database
                                                       format: dd/MM/YYYY
                                                       gets content from 01/01/1970 if not specified
                    default: 0

                backupValidationOnly       (bool)   :  backupValidationOnly option
                                                        true - backupValidationOnly selected
                                                        false - backupValidationOnly unselected
                     default: False

                 restoreTablespace       (bool)     :  restoreTablespace option
                                                        true - restoreTablespace selected
                                                        false - restoreTablespace unselected
                     default: False

                noCatalog       (bool)              :  noCatalog option
                                                        true - noCatalog selected
                                                        false - noCatalog unselected
                     default: True

                sourceItem       (list)              :  sourceItem means browse options for
                                                         sap oracle restores
                                                        /+BROWSE+ - means both data and logs
                                                        are selected
                                                        /+BROWSE+DATA -data only selected
                                                        /+BROWSE+LOG -log only selected
                     default: /+BROWSE+
                databaseCopy       (bool)            :  databaseCopy option
                                                        true - databaseCopy selected
                                                        false - databaseCopy unselected
                     default: False

                archiveLogBy       (str)            :  for restore archive log options,
                                                        default means restore archivelogall
                                                        is selected

                     default: default

         Raises:
                SDKException:

                    if failed to browse content

                    if response is empty

                    if response is not success

                    if destination client does not exist on commcell

                    if destination instance does not exist on commcell
        """

        if sap_options is None:
            sap_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._agent_object._client_object.client_name
            

        if isinstance(destination_client, Client):
            destination_client = destination_client
            
        elif isinstance(destination_client, str):
            destination_client = Client(self._commcell_object, destination_client)
            #print(destination_client)
        else:
            raise SDKException('Instance', '101')

        dest_agent = Agent(destination_client, 'sap for oracle','61')

        # check if instance name is correct
        if destination_instance is None:
            destination_instance = self.instance_name

        if isinstance(destination_instance, Instance):
            destination_instance = destination_instance
        elif isinstance(destination_instance, str):
            destination_instance = dest_agent.instances.get(destination_instance)
        else:
            raise SDKException('Instance', '101')
        sap_options["destination_client"] = destination_client.client_name
        sap_options["destination_instance"] = destination_instance.instance_name
        #sap_options["copyPrecedence"] = sap_options.get("copyPrecedence", "0")

        # prepare and execute
        request_json = self._restore_saporacle_request_json(sap_options)
        return self._process_restore_response(request_json)
    
    
