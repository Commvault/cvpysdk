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
    """
    Represents a SAP Oracle instance, extending the base Instance class to provide
    specialized operations and properties for managing SAP Oracle environments.

    This class encapsulates configuration details and operational methods specific
    to SAP Oracle instances, including access to key paths, user information,
    and SAP Oracle-specific settings. It also provides mechanisms for restoring
    SAP Oracle instances, both through internal request generation and in-place
    restoration operations.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Properties for accessing Oracle home, SAP data home, SAP executable path, and OS user
        - Properties for command and log service providers
        - Access to SAP Oracle database user, connect string, block size, and secure store
        - Properties for archive log backup streams, instance ID, snapshot backup enablement, and snap engine name
        - Internal method for generating SAP Oracle restore request JSON
        - Method for performing in-place restore operations with custom SAP options

    #ai-gen-doc
    """

    def __init__(self, agent_object: Agent, instance_name: str, instance_id: int = None) -> None:
        """Initialize a SAPOracleInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this SAP Oracle instance.
            instance_name: The name of the SAP Oracle instance.
            instance_id: Optional; the unique identifier for the SAP Oracle instance.

        #ai-gen-doc
        """
        super(SAPOracleInstance, self).__init__(agent_object, instance_name, instance_id)
        self._instanceprop = {}  # variable to hold instance properties to be changed

    @property
    def oracle_home(self) -> str:
        """Get the Oracle home directory path for the SAP Oracle instance.

        Returns:
            The Oracle home directory as a string.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['oracleHome']

    @property
    def sapdata_home(self) -> str:
        """Get the SAPDATA home directory path for the SAP Oracle instance.

        Returns:
            The path to the SAPDATA home directory as a string.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['sapDataPath']

    @property
    def sapexepath(self) -> str:
        """Get the SAP executable path (sapexepath) for the SAP Oracle instance.

        Returns:
            The SAP executable path as a string.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['sapExeFolder']

    @property
    def os_user(self) -> str:
        """Get the Oracle software owner username for this SAP Oracle instance.

        Returns:
            The username of the Oracle software owner as a string.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['oracleUser']['userName']

    @property
    def cmd_sp(self) -> str:
        """Get the command line storage policy string for the SAP Oracle instance.

        Returns:
            The storage policy string used for command line operations.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['oracleStorageDevice'][
            'commandLineStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self) -> str:
        """Get the log storage policy associated with the Oracle instance.

        Returns:
            The name of the log storage policy as a string.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['oracleStorageDevice'][
            'logBackupStoragePolicy']['storagePolicyName']

    @property
    def saporacle_db_user(self) -> str:
        """Get the Oracle database user associated with this SAP Oracle instance.

        Returns:
            The Oracle database user name as a string.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['sqlConnect']['userName']

    @property
    def saporacle_db_connectstring(self) -> str:
        """Get the Oracle database connect string for this SAP Oracle instance.

        Returns:
            The Oracle database connect string associated with the instance.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['sqlConnect']['domainName']

    @property
    def saporacle_blocksize(self) -> int:
        """Get the block size configured for the SAP Oracle instance.

        Returns:
            The block size value for the instance as an integer.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['blockSize']

    @property
    def saporacle_sapsecurestore(self) -> str:
        """Get the SAP Secure Store option configured for this SAP Oracle instance.

        Returns:
            str: The SAP Secure Store option value for the instance.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['useSAPSecureStore']

    @property
    def saporacle_archivelogbackupstreams(self) -> int:
        """Get the number of archive log backup streams configured for the SAP Oracle instance.

        Returns:
            int: The number of backup streams used for archiving logs in this SAP Oracle instance.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['numberOfArchiveLogBackupStreams']

    @property
    def saporacle_instanceid(self) -> int:
        """Get the SAP Oracle instance ID option for this instance.

        Returns:
            The SAP Oracle instance ID as an integer.

        #ai-gen-doc
        """
        return self._properties['instance']['instanceId']
    
    @property
    def saporacle_snapbackup_enable(self) -> bool:
        """Get the status of the SAP Oracle SnapBackup enable option for this instance.

        Returns:
            bool: True if SnapBackup is enabled for the SAP Oracle instance, False otherwise.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['snapProtectInfo']['isSnapBackupEnabled']
    
    @property
    def saporacle_snapengine_name(self) -> str:
        """Get the Snap Engine name option for the SAP Oracle instance.

        Returns:
            The Snap Engine name configured for this SAP Oracle instance as a string.

        #ai-gen-doc
        """
        return self._properties['sapOracleInstance']['snapProtectInfo']['snapSelectedEngine']['snapShotEngineName']

    def _restore_saporacle_request_json(self, value: dict) -> dict:
        """Generate the JSON request payload for SAP Oracle restore operations.

        This method constructs and returns a JSON dictionary formatted according to the options
        specified by the user, suitable for submission to the SAP Oracle restore API.

        Args:
            value: A dictionary containing user-selected restore options and parameters.

        Returns:
            A dictionary representing the JSON request payload for the SAP Oracle restore API.

        #ai-gen-doc
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
        destination_client: str = None,
        destination_instance: str = None,
        sap_options: dict = None
    ) -> None:
        """Perform an in-place restore and recovery of a SAP Oracle database.

        This method restores and recovers a SAP Oracle database on the original or specified destination client and instance.
        The restore operation can be customized using the `sap_options` dictionary to control various restore and recovery parameters.

        Args:
            destination_client: The name of the destination client where the SAP Oracle client package exists.
                If not provided, the source backup client will be used.
            destination_instance: The name of the destination SAP Oracle instance.
                If not provided, the source backup instance will be used.
            sap_options: Dictionary of SAP Oracle restore options. Supported keys include:
                - backupset_name (str): Name of the backupset to restore. Default is "default".
                - restoreData (bool): Whether to restore data. Default is True.
                - streams (int): Number of streams to use for restore. Default is 2.
                - copyPrecedence (int): Copy number to use for restore. Default is 0.
                - archiveLog (bool): Whether to restore archive logs. Default is True.
                - recover (bool): Whether to recover the database. Default is True.
                - switchDatabaseMode (bool): Whether to switch database mode. Default is True.
                - restoreControlFile (bool): Whether to restore the control file. Default is True.
                - partialRestore (bool): Whether to perform a partial restore. Default is False.
                - openDatabase (bool): Whether to open the database after restore. Default is True.
                - resetLogs (bool): Whether to reset logs after restore. Default is True.
                - point_in_time (str): Point-in-time for restore in "dd/MM/YYYY" format. Default is "0" (from 01/01/1970).
                - backupValidationOnly (bool): Whether to perform backup validation only. Default is False.
                - restoreTablespace (bool): Whether to restore tablespace. Default is False.
                - noCatalog (bool): Whether to use no catalog. Default is True.
                - sourceItem (list): Browse options for SAP Oracle restores (e.g., ['/+BROWSE+']).
                - databaseCopy (bool): Whether to perform a database copy. Default is False.
                - archiveLogBy (str): Archive log restore option. Default is "default".

        Raises:
            SDKException: If the restore operation fails due to:
                - Failed to browse content
                - Empty response from the server
                - Unsuccessful response from the server
                - Destination client does not exist on Commcell
                - Destination instance does not exist on Commcell

        Example:
            >>> sap_instance = SAPOracleInstance()
            >>> sap_instance.restore_in_place(
            ...     destination_client="prod-db-server",
            ...     destination_instance="ORCL",
            ...     sap_options={
            ...         "backupset_name": "default",
            ...         "restoreData": True,
            ...         "streams": 4,
            ...         "archiveLog": True,
            ...         "recover": True,
            ...         "point_in_time": "15/03/2024"
            ...     }
            ... )
            >>> print("Restore operation initiated successfully.")

        #ai-gen-doc
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
        else:
            raise SDKException('Instance', '101')

        dest_agent = Agent(destination_client, 'sap for oracle', '61')

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
        # sap_options["copyPrecedence"] = sap_options.get("copyPrecedence", "0")

        # prepare and execute
        request_json = self._restore_saporacle_request_json(sap_options)
        return self._process_restore_response(request_json)
