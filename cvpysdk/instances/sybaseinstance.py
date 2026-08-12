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
File for operating on a Sybase Instance.

SybaseInstance is the only class defined in this file.
SybaseInstance: Derived class from Instance Base class, representing a
                sybase instance, and to perform operations on that instance

SybaseInstance:

    __init__()                      -- initialise object of Sybase  Instance associated with
                                       the specified agent

    _get_sybase_restore_json()      -- Private Method to construct restore JSON for
                                       individual database restore

    _get_sybase_full_restore_json() -- Private Method to construct
                                       restore JSON for fullserver restore

    _get_single_database_json()     -- Private Method to construct
                                       restore JSON for individual database restore

    _get_server_content()           -- Private Method to construct restore JSON for
                                       individual database when we have rename device options


    _restore_common_options_json()  -- setter for common options property in restore

    _restore_destination_json()     -- setter for destination options property in restore

    _restore_sybase_option_json()   -- setter for Sybase restore option property in restore

    _primary_node_properties()      --  Returns Primary Node Properties of sybase hadr instance

    sybase_home()                   -- returns string of sybase_home Property of Sybase instance

    sybase_instance_name()          -- returns sybase instance name without any case change

    is_discovery_enabled()          -- returns bool value of autodiscovery option
                                       at given sybase instance level

    localadmin_user()               -- returns string of localadmin_user of given sybase instance

    sa_user()                       -- returns string of sybase sa_user of given sybase instance

    version()                       -- returns string of given sybase server version

    backup_server()                 -- returns string of backup_server for given sybase instance

    sybase_ocs()                    -- returns string of sybase_ocs for given sybase instance

    sybase_ase()                    -- returns string of sybase_ase for given sybase  instance

    sybase_blocksize()              -- returns integer of block
                                       size for given sybase instance

    sybase_configfile()             -- returns string of sybase_configfile
                                       for given sybase instance

    sybase_sharedmemory_directory() -- returns string of sybase_memory_directory
                                       for given sybase instance

    restore_sybase_server()         -- Performs full sybase server restore

    restore_database()              -- Performs individual databases restore

    restore_to_disk()               -- Perform restore to disk [Application free restore] for sybase

    get_node_properties()           --  Returns properties of all sybase hadr nodes or for given node id

"""

from __future__ import unicode_literals
import datetime

from ..exception import SDKException
from .dbinstance import DatabaseInstance

from typing import TYPE_CHECKING, Dict, List, Optional
if TYPE_CHECKING:
    from ..agent import Agent


class SybaseInstance(DatabaseInstance):
    """
    Represents a standalone Sybase database instance within a managed environment.

    This class provides comprehensive management and restoration capabilities for Sybase
    database instances. It exposes properties to access key configuration details such as
    Sybase home directory, instance name, version, users, backup server, and HADR (High
    Availability Disaster Recovery) settings. The class also includes methods for retrieving
    node properties, generating restore configuration JSONs, and performing various types of
    Sybase database and server restores, including full, single database, and disk-based
    restores.

    Key Features:
        - Access to Sybase instance configuration and metadata via properties
        - Support for HADR and primary node identification
        - Methods to retrieve node and server content properties
        - Generation of restore configuration JSONs for different restore scenarios
        - Restoration of Sybase servers and databases to specified destinations
        - Disk-based restore operations with authentication support
        - Fine-grained control over restore options such as point-in-time, device options,
          database renaming, and copy precedence

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int = None) -> None:
        """Initialize a SybaseInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Sybase instance.
            instance_name: The name of the Sybase instance.
            instance_id: Optional; the unique identifier for the Sybase instance. Defaults to None.

        #ai-gen-doc
        """
        self._sybase_restore_json = None
        self._commonoption_restore_json = None
        self._destination_restore_json = None
        super(SybaseInstance, self).__init__(agent_object, instance_name, instance_id)
        self._is_hadr = len(self._properties.get('sybaseClusterInstance', {})) > 0
        self._instanceprop = {}  # instance variable to hold instance properties
        self._nodes = self.get_node_properties()
        self._primarynodeprop = self._primary_node_properties()

    @property
    def sybase_home(self) -> str:
        """Get the Sybase home directory path for this SybaseInstance.

        Returns:
            The Sybase home directory as a string.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('sybaseHome')
        return self._properties.get('sybaseInstance', {}).get('sybaseHome')

    @property
    def sybase_instance_name(self) -> str:
        """Get the Sybase instance name with its original case preserved.

        Returns:
            The Sybase instance name as a string, maintaining the actual case as configured.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('backupServer')[:-3]
        return self._properties.get('instance', {}).get('instanceName')

    @property
    def is_discovery_enabled(self) -> bool:
        """Check if autodiscovery is enabled for the Sybase instance.

        Returns:
            True if autodiscovery is enabled; False otherwise.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('enableAutoDiscovery')
        return self._properties.get('sybaseInstance', {}).get('enableAutoDiscovery')

    @property
    def localadmin_user(self) -> str:
        """Get the local admin user for the Sybase instance.

        Returns:
            The username of the local admin as a string.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('localAdministrator', {}).get('userName')
        return self._properties.get('sybaseInstance', {}).get('localAdministrator', {}).get('userName')

    @property
    def sa_user(self) -> str:
        """Get the 'sa' (system administrator) username for the Sybase instance.

        Returns:
            The 'sa' username as a string.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('saUser', {}).get('userName')
        return self._properties.get('sybaseInstance', {}).get('saUser', {}).get('userName')

    @property
    def version(self) -> str:
        """Get the Sybase version associated with this instance.

        Returns:
            The Sybase version as a string.

        #ai-gen-doc
        """
        return self._properties.get('version')

    @property
    def backup_server(self) -> str:
        """Get the name of the backup server associated with this Sybase instance.

        Returns:
            The name of the backup server as a string.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('backupServer')
        return self._properties.get('sybaseInstance', {}).get('backupServer')

    @property
    def sybase_ocs(self) -> str:
        """Get the Sybase Open Client/Server (OCS) version string for this Sybase instance.

        Returns:
            The Sybase OCS version as a string.


        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('sybaseOCS')
        return self._properties.get('sybaseInstance', {}).get('sybaseOCS')

    @property
    def sybase_ase(self) -> str:
        """Get the string representation for Sybase ASE.

        Returns:
            str: A string representing the Sybase ASE instance.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('sybaseASE')
        return self._properties.get('sybaseInstance', {}).get('sybaseASE')

    @property
    def sybase_blocksize(self) -> int:
        """Get the Sybase block size value for this instance.

        Returns:
            The block size value as an integer.

        #ai-gen-doc
        """
        return self._properties.get('sybaseInstance', {}).get('sybaseBlockSize')

    @property
    def sybase_configfile(self) -> str:
        """Get the Sybase configuration file path for this instance.

        Returns:
            The file path to the Sybase configuration file as a string.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('configFile')
        return self._properties.get('sybaseInstance', {}).get('configFile')

    @property
    def sybase_sharedmemory_directory(self) -> str:
        """Get the Sybase shared memory directory path for this instance.

        Returns:
            The directory path as a string where Sybase shared memory is stored.

        #ai-gen-doc
        """
        if self.is_hadr:
            return self._primarynodeprop.get('sybaseProps', {}).get('sharedMemoryDirectory')
        return self._properties.get('sybaseInstance', {}).get('sharedMemoryDirectory')

    @property
    def is_hadr(self) -> bool:
        """Check if the current Sybase instance is configured as HADR (High Availability Disaster Recovery).

        Returns:
            True if the instance is an HADR-enabled Sybase instance, otherwise False.

        #ai-gen-doc
        """
        return self._is_hadr

    @property
    def hadr_primarynode_id(self) -> Optional[str]:
        """Get the Sybase HADR primary node ID for this instance.

        Returns:
            The primary node ID as a string if the instance is configured for HADR.


        #ai-gen-doc
        """
        if self.is_hadr:
            return self._properties.get('sybaseClusterInstance', {}).get('primaryNodeId')
        return None

    @property
    def client_name(self) -> str:
        """Get the client name associated with this Sybase instance.

        Returns:
            The client name as registered in the Commcell.

        #ai-gen-doc
        """
        return self._properties.get('instance', {}).get('clientName')

    def _primary_node_properties(self) -> dict:
        """Retrieve the primary node properties for the Sybase instance.

        Returns:
            dict: A dictionary containing the properties of the primary node.

        #ai-gen-doc
        """
        if self.is_hadr:
            nodes = self._properties.get('sybaseClusterInstance').get('nodes')
            for node in nodes:
                if node.get('physicalClient', {}).get('clientId') == self.hadr_primarynode_id:
                    return node

    def get_node_properties(self, clientId: Optional[str] = None) -> dict:
        """Retrieve node properties for a specific client or all nodes.

        Args:
            clientId: Optional; The client ID as a string. If provided, returns the node properties for the specified client.
                If not provided, returns properties for all nodes.

        Returns:
            A dictionary containing node properties. If clientId is specified, returns properties for that client;
            otherwise, returns properties for all nodes.

        Example:
            >>> instance = SybaseInstance()
            >>> # Get properties for a specific client
            >>> node_props = instance.get_node_properties(clientId="1234")
            >>> print(node_props)
            >>> # Get properties for all nodes
            >>> all_node_props = instance.get_node_properties()
            >>> print(all_node_props)

        #ai-gen-doc
        """
        if self.is_hadr:
            nodes = self._properties.get('sybaseClusterInstance').get('nodes')
            if clientId:
                for node in nodes:
                    if node.get('physicalClient', {}).get('clientId') == int(clientId):
                        return node
            return nodes

    def _restore_common_options_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing common options to be included in the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._commonoption_restore_json = {
            "indexFreeRestore": value.get("index_free_restore", False),
            "restoreToDisk": value.get("restore_to_disk", False),
            "sybaseCreateDevices": value.get("sybase_create_device", False)
        }

    def _restore_destination_json(self, value: dict) -> None:
        """Set the Sybase destination options in the restore JSON.

        Args:
            value: A dictionary containing the destination options for the Sybase restore operation.

        Example:
            >>> destination_options = {
            ...     "server": "sybase_server",
            ...     "database": "target_db",
            ...     "user": "db_user"
            ... }
            >>> sybase_instance._restore_destination_json(destination_options)
            >>> # The destination options are now set for the restore operation

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = {
            "destinationInstance": {
                "clientName": value.get("destination_client", ""),
                "instanceName": value.get("destination_instance_name", ""),
                "appName": "Sybase"
            },
            "destClient": {
                "clientName": value.get("destination_client", "")
            },
            "destPath": [value.get("destination_path", "")]
        }

    def _restore_sybase_option_json(self, value: dict) -> None:
        """Set the Sybase restore options in the restore JSON configuration.

        Args:
            value: A dictionary containing key-value pairs for Sybase restore options.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')
        if value.get("to_time") is None:
            time_dict = {}
        else:
            time_dict = {
                "timeValue": value.get("to_time", "")
            }
        self._sybase_restore_json = {
            "sybaseRecoverType": "STATE_RECOVER",
            "pointofTime": value.get("point_in_time", ""),
            "destinationServer": {
                "name": value.get("destination_instance_name", "")
            },
            "pointInTime": time_dict,
            "instanceRestore": value.get("instance_restore", ""),
            "renameDatabases": value.get("rename_databases", ""),
            "restoreType": "POINT_IN_TIME",
            "sybaseDatabase": value.get("syb_db", "")
        }

    def _restore_json(self, **kwargs) -> dict:
        """Construct the JSON request payload for a restore operation based on user-selected options.

        This method generates a dictionary representing the JSON request to be sent to the API,
        using the provided keyword arguments to specify restore options.

        Args:
            **kwargs: Arbitrary keyword arguments representing restore options and their values.

        Returns:
            dict: The JSON request dictionary to be passed to the API for the restore operation.


        #ai-gen-doc
        """
        restore_json = super(SybaseInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        self._restore_sybase_option_json(restore_option)
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["sybaseRstOption"] = self._sybase_restore_json
        return restore_json

    def _get_sybase_restore_base_json(
        self,
        destination_client: str,
        destination_instance_name: str,
        point_in_time: bool = False,
        instance_restore: bool = False,
        timevalue: str = None,
        sybase_create_device: bool = False,
        rename_databases: bool = False,
        copy_precedence: int = 0
    ) -> dict:
        """Generate the base JSON structure for a Sybase restore operation.

        This method constructs a dictionary representing the base configuration for a Sybase restore,
        based on the provided parameters such as destination client, instance name, restore type,
        point-in-time recovery, and additional restore options.

        Args:
            destination_client: The name of the Sybase destination client for the restore.
            destination_instance_name: The name of the Sybase destination instance for the restore.
            point_in_time: Whether to perform a point-in-time restore. Defaults to False.
            instance_restore: Whether to restore the entire Sybase server (True) or a single database (False). Defaults to False.
            timevalue: The point-in-time value for the restore in 'YYYY-MM-DD HH:MM:SS' format. Used if point_in_time is True.
            sybase_create_device: Whether to create a new device for the Sybase database restore. Defaults to False.
            rename_databases: Whether to rename the database(s) during restore. Defaults to False.
            copy_precedence: The copy precedence value of the storage policy. Defaults to 0.

        Returns:
            dict: A dictionary containing the base Sybase restore JSON configuration.

        Example:
            >>> instance = SybaseInstance()
            >>> restore_json = instance._get_sybase_restore_base_json(
            ...     destination_client="sybase_client",
            ...     destination_instance_name="sybase_instance",
            ...     point_in_time=True,
            ...     timevalue="2023-12-01 10:00:00",
            ...     sybase_create_device=True,
            ...     rename_databases=False,
            ...     copy_precedence=1
            ... )
            >>> print(restore_json)
            # The output will be a dictionary with the specified restore configuration.

        #ai-gen-doc
        """
        copy_precedence_applicable = False
        if copy_precedence is not None:
            copy_precedence_applicable = True
        if instance_restore is not True:
            point_in_time = True
            if timevalue is None:
                current_time = datetime.datetime.utcnow()
                current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                timevalue = current_time
        else:
            if (timevalue is None) and (point_in_time is True):
                current_time = datetime.datetime.utcnow()
                current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                timevalue = current_time
        syb_db = []
        basic_sybase_options = self._restore_json(
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            point_in_time=point_in_time,
            instance_restore=instance_restore,
            to_time=timevalue,
            from_time=None,
            sybase_create_device=sybase_create_device,
            rename_databases=rename_databases,
            copy_precedence=copy_precedence,
            copy_precedence_applicable=copy_precedence_applicable,
            syb_db=syb_db)

        return basic_sybase_options

    def _db_option(
        self,
        database_list: set,
        rename_databases: bool,
        sybase_create_device: bool,
        device_options: dict
    ) -> List[dict]:
        """Construct database options for each database in the provided list.

        This method generates a dictionary of options for each database specified in `database_list`,
        incorporating settings for renaming databases and creating devices during a Sybase database restore.
        The `device_options` parameter allows for specifying device and database rename options for each database.

        Args:
            database_list: Set of dictionary database names to be restored.
            rename_databases: Whether to enable the rename database option for the restore.
            sybase_create_device: Whether to create a new device for the Sybase database restore.
            device_options: Dictionary containing device and database rename options for each database.

        Returns:
            Dictionary containing the constructed database options to be added to the restore JSON.

        Example:
            >>> db_list = ['db1', 'db2']
            >>> rename = True
            >>> create_device = False
            >>> dev_opts = {
            ...     'db1': {'device_rename': 'dev1_new', 'db_rename': 'db1_new'},
            ...     'db2': {'device_rename': 'dev2_new', 'db_rename': 'db2_new'}
            ... }
            >>> db_options = sybase_instance._db_option(db_list, rename, create_device, dev_opts)
            >>> print(db_options)
            {'db1': {'device_rename': 'dev1_new', 'db_rename': 'db1_new', ...}, ...}

        #ai-gen-doc
        """
        db_options = []
        for dbname in database_list:
            if device_options is None:
                db_json = self._get_single_database_json(dbname=dbname)
            else:
                if dbname in device_options.keys():
                    dev_opt = device_options[dbname]
                    db_json = self._get_single_database_json(
                        dbname, dev_opt, rename_databases, sybase_create_device)
                else:
                    db_json = self._get_single_database_json(dbname=dbname)
            db_options.append(db_json)
        return db_options

    def _get_sybase_restore_json(
        self,
        destination_client: str,
        destination_instance_name: str,
        database_list: set,
        timevalue: str = None,
        sybase_create_device: bool = False,
        rename_databases: bool = False,
        device_options: dict = None,
        copy_precedence: int = 0
    ) -> dict:
        """Construct the restore JSON payload for an individual Sybase database restore operation.

        This method generates the required JSON structure to initiate a Sybase database restore,
        supporting options such as point-in-time restore, device creation, database renaming,
        and custom device options.

        Args:
            destination_client: The name of the Sybase destination client for the restore.
            destination_instance_name: The name of the Sybase destination instance for the restore.
            database_list: Set of database names to be restored.
            timevalue: Optional. Point-in-time restore value in the format 'YYYY-MM-DD HH:MM:SS'.
            sybase_create_device: Whether to create a new device for the Sybase database restore.
            rename_databases: Whether to enable the rename database option during restore.
            device_options: Optional. Dictionary of device and database rename options for each database.
            copy_precedence: Copy precedence of the storage policy to use for the restore.

        Returns:
            dict: The constructed JSON payload for the Sybase database restore operation.

        Example:
            >>> restore_json = sybase_instance._get_sybase_restore_json(
            ...     destination_client="sybase_client",
            ...     destination_instance_name="sybase_instance",
            ...     database_list=["db1", "db2"],
            ...     timevalue="2023-12-01 10:00:00",
            ...     sybase_create_device=True,
            ...     rename_databases=True,
            ...     device_options={"db1": {"device": "dev1", "rename": "db1_new"}},
            ...     copy_precedence=1
            ... )
            >>> print(restore_json)
            # The returned dictionary can be used to submit a Sybase restore request.

        #ai-gen-doc
        """
        instance_restore = False
        point_in_time = True
        # Check to perform renamedatabase/create device
        if (sybase_create_device is False) and (rename_databases is False):
            device_options = None

        restore_json = self._get_sybase_restore_base_json(
            destination_client,
            destination_instance_name,
            point_in_time,
            instance_restore,
            timevalue,
            sybase_create_device,
            rename_databases,
            copy_precedence
        )

        db_options = self._db_option(
            database_list, rename_databases, sybase_create_device, device_options
        )
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "sybaseRstOption"]["sybaseDatabase"] = db_options
        return restore_json

    def _get_sybase_full_restore_json(
        self,
        destination_client: str,
        destination_instance_name: str,
        point_in_time: bool = False,
        timevalue: str = None,
        sybase_create_device: bool = True,
        rename_databases: bool = False,
        device_options: dict = None,
        copy_precedence: int = 0
    ) -> dict:
        """Create the JSON payload for a full Sybase server restore operation.

        This method constructs the required JSON structure for performing a full Sybase server restore,
        including options for point-in-time restore, device creation, database renaming, and device options.

        Args:
            destination_client: The name of the Sybase destination client for the restore.
            destination_instance_name: The name of the Sybase destination instance for the restore.
            point_in_time: Whether to perform a point-in-time restore. Defaults to False.
            timevalue: The point-in-time value for the restore in 'YYYY-MM-DD HH:MM:SS' format. Used only if point_in_time is True.
            sybase_create_device: Whether to create devices for the Sybase database restore. Defaults to True.
            rename_databases: Whether to enable the rename database option during restore. Defaults to False.
            device_options: A dictionary of dictionaries specifying device and database rename options for each database. Defaults to None.
            copy_precedence: The copy precedence of the storage policy to use for the restore. Defaults to 0.

        Returns:
            dict: The JSON payload required for a full Sybase server restore operation.

        Example:
            >>> restore_json = sybase_instance._get_sybase_full_restore_json(
            ...     destination_client="sybase_client",
            ...     destination_instance_name="sybase_instance",
            ...     point_in_time=True,
            ...     timevalue="2023-12-01 10:00:00",
            ...     sybase_create_device=True,
            ...     rename_databases=False,
            ...     device_options={"db1": {"device": "dev1", "rename": "db1_new"}},
            ...     copy_precedence=1
            ... )
            >>> print(restore_json)
            # The output will be a dictionary representing the restore JSON payload.

        #ai-gen-doc
        """

        instance_restore = True
        restore_json = self._get_sybase_restore_base_json(
            destination_client,
            destination_instance_name,
            point_in_time,
            instance_restore,
            timevalue,
            sybase_create_device,
            rename_databases,
            copy_precedence)
        db_options = []
        dblist = self._get_server_content()
        device_options_keys = []
        if device_options is not None:
            for key in device_options.keys():
                device_options_keys.append(str(key))

        if not dblist:
            raise SDKException(
                'Instance', '102', 'Database contents of Sybase server is empty'
            )

        database_list = dblist
        db_options = self._db_option(database_list, rename_databases, sybase_create_device, device_options)
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "sybaseRstOption"]["sybaseDatabase"] = db_options
        return restore_json

    def _get_single_database_json(
        self,
        dbname: str,
        device_options: Optional[dict] = None,
        rename_databases: bool = False,
        sybase_create_device: bool = False
    ) -> dict:
        """Construct the JSON payload for restoring a single Sybase database.

        This method generates a dictionary representing the restore options for an individual
        Sybase database, including options for device creation and database renaming.

        Args:
            dbname: The name of the Sybase database to be restored.
            device_options: Optional dictionary containing device and database rename options
                for the specified database. The structure should be a dictionary of dictionaries,
                where each key is a device or database name and the value is its options.
            rename_databases: Whether to enable the rename database option for the restore.
            sybase_create_device: Whether to enable the create device option for the restore.

        Returns:
            A dictionary representing the restore options for the specified database,
            including settings for device creation and renaming as applicable.

        Example:
            >>> instance = SybaseInstance()
            >>> db_json = instance._get_single_database_json(
            ...     dbname="mydb",
            ...     device_options={"mydb": {"device": "dev1", "rename": "mydb_new"}},
            ...     rename_databases=True,
            ...     sybase_create_device=True
            ... )

        #ai-gen-doc
        """
        sybase_db_details = None
        databasechain = "0:0:{0}:0".format(dbname)
        dbchain_list = []
        dbchain_list.append(databasechain)
        subclientid = "0"
        dbid = "0"
        datadevid = "0"
        logdevid = "0"
        size = "0"
        device = []
        sybase_db_details = {
            "databaseId": {"name": dbname},
            "associatedSubClientId": 0,
            "databaseChain": dbchain_list
        }
        if device_options is not None:
            if sybase_create_device:
                for key1, value1 in device_options.items():
                    if device_options[key1] is None:
                        if key1 == "newdatabasename":
                            device_options[key1] = None
                        else:
                            device_options[key1] = "0"
            else:
                for key1, value1 in device_options.items():
                    if key1 == "newdatabasename":
                        continue
                    else:
                        device_options[key1] = "0"

            datadevicename = device_options["datadevicename"]
            newdatadevicename = device_options["newdatadevicename"]
            newdatadevicepath = device_options["newdatadevicepath"]
            logdevicename = device_options["logdevicename"]
            newlogdevicename = device_options["newlogdevicename"]
            newlogdevicepath = device_options["newlogdevicepath"]
            if rename_databases:
                if device_options["newdatabasename"] is None:
                    newdatabasename = dbname
                else:
                    newdatabasename = device_options["newdatabasename"]
            else:
                device_options["newdatabasename"] = dbname

            # Check to find given device is system device

            system_databases = ['master', 'model', 'sybsystemprocs',
                                'sybsystemdb', 'tempdb', 'sybmgmtdb', 'dbccdb', 'sybsecurity']
            if dbname in system_databases:
                newdatadevicename = "0"
                newlogdevicename = "0"
                newdatabasename = dbname

            data_device = "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}".format(
                subclientid,
                dbid,
                datadevid,
                datadevicename,
                newdatadevicename,
                newdatadevicepath,
                size,
                newdatabasename
            )

            log_device = "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}".format(
                subclientid,
                dbid,
                logdevid,
                logdevicename,
                newlogdevicename,
                newlogdevicepath,
                size,
                newdatabasename
            )

            device.append(data_device)
            device.append(log_device)
            sybase_db_details = {
                "databaseId": {"name": dbname},
                "associatedSubClientId": 0,
                "databaseChain": dbchain_list,
                "devices": device
            }

        return sybase_db_details

    def _get_server_content(self) -> set:
        """Retrieve all databases available for the specified Sybase Server instance.

        Returns:
            Set of database names available as server content.

        #ai-gen-doc
        """
        subclient_dict = self.subclients._get_subclients()
        subclient_list = []
        db_list = []
        for key in subclient_dict.keys():
            subclient_list.append(str(key))
        for sub in subclient_list:
            sub_obj = self.subclients.get(sub)
            content = sub_obj.content
            for eachdb in content:
                db_list.append(eachdb)
        db_list = set(db_list)
        return db_list

    def restore_sybase_server(
        self,
        destination_client: Optional[str] = None,
        destination_instance_name: Optional[str] = None,
        point_in_time: bool = False,
        timevalue: Optional[str] = None,
        rename_databases: bool = False,
        device_options: Optional[Dict[str, Dict[str, Optional[str]]]] = None,
        copy_precedence: int = 0
    ) -> object:
        """Perform a full Sybase server restore operation.

        This method initiates a full restore of a Sybase server, with options to restore to a different client or instance,
        perform a point-in-time restore, rename databases, and specify device options for each database.

        Args:
            destination_client: The name of the Sybase destination client for the restore. If None, restores to the source client.
            destination_instance_name: The name of the Sybase destination instance for the restore. If None, restores to the source instance.
            point_in_time: Whether to perform a point-in-time restore. Defaults to False.
            timevalue: The point-in-time value for the restore, in the format 'YYYY-MM-DD HH:MM:SS'. Required if point_in_time is True.
            rename_databases: Whether to rename databases during the restore. Defaults to False.
            copy_precedence: The copy to restore the data from
            device_options: A dictionary mapping source database names to their device and rename options. 
                Each value is a dictionary with keys such as:
                    - "datadevicename"
                    - "newdatadevicename"
                    - "newdatadevicepath"
                    - "logdevicename"
                    - "newlogdevicename"
                    - "newlogdevicepath"
                    - "newdatabasename"
                If a particular option is not needed, set its value to None.
                Example:
                    device_options = {
                        "db1": {
                            "datadevicename": "testdata",
                            "newdatadevicename": "testdatanew",
                            "newdatadevicepath": "/opt/sap/data/testdatanew.dat",
                            "logdevicename": "testlog",
                            "newlogdevicename": "testlognew",
                            "newlogdevicepath": "/opt/sap/data/testlognew.dat",
                            "newdatabasename": "db1new"
                        },
                        "model": {
                            "datadevicename": None,
                            "newdatadevicename": None,
                            "newdatadevicepath": None,
                            "logdevicename": None,
                            "newlogdevicename": None,
                            "newlogdevicepath": None,
                            "newdatabasename": "modelnew"
                        }
                    }
                Note: Devices corresponding to system databases cannot be renamed.
            copy_precedence: The copy precedence of the storage policy to use for the restore. Defaults to 0.

        Returns:
            object: A Job object containing details of the restore operation.

        Example:
            >>> device_opts = {
            ...     "db1": {
            ...         "datadevicename": "testdata",
            ...         "newdatadevicename": "testdatanew",
            ...         "newdatadevicepath": "/opt/sap/data/testdatanew.dat",
            ...         "logdevicename": "testlog",
            ...         "newlogdevicename": "testlognew",
            ...         "newlogdevicepath": "/opt/sap/data/testlognew.dat",
            ...         "newdatabasename": "db1new"
            ...     }
            ... }
            >>> job = sybase_instance.restore_sybase_server(
            ...     destination_client="sybase_dest_client",
            ...     destination_instance_name="SYBASE_DEST",
            ...     point_in_time=True,
            ...     timevalue="2023-12-01 10:00:00",
            ...     rename_databases=True,
            ...     device_options=device_opts,
            ...     copy_precedence=1
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        if destination_client is None:
            destination_client = self.client_name

        if destination_instance_name is None:
            destination_instance_name = self.instance_name

        sybase_create_device = True
        request_json = self._get_sybase_full_restore_json(
            destination_client,
            destination_instance_name,
            point_in_time,
            timevalue,
            sybase_create_device,
            rename_databases,
            device_options,
            copy_precedence)

        return self._process_restore_response(request_json)

    def restore_database(
        self,
        destination_client: str = None,
        destination_instance_name: str = None,
        database_list: set = None,
        timevalue: str = None,
        sybase_create_device: bool = False,
        rename_databases: bool = False,
        device_options: dict = None,
        copy_precedence: int = 0
    ) -> object:
        """Perform an individual Sybase database restore operation.

        This method restores one or more Sybase databases to a specified destination client and instance.
        It supports options for point-in-time restore, device creation, renaming databases, and advanced
        device configuration through the `device_options` parameter.

        Args:
            destination_client: The name of the destination client for the restore. Defaults to None.
            destination_instance_name: The name of the destination Sybase instance for the restore. Defaults to None.
            database_list: Set of database names to restore. Must not be empty.
            timevalue: Point-in-time for restore in the format 'YYYY-MM-DD HH:MM:SS'. Defaults to None.
            sybase_create_device: Whether to create devices for the database restore. Defaults to False.
            rename_databases: Whether to rename databases during restore. Defaults to False.
            copy_precedence: Copy precedence of the storage policy to use for restore. Defaults to 0.
            device_options: Dictionary of dictionaries specifying device and database rename options for each source database.
                The outer dictionary key is the source database name, and the value is a dictionary of options.
                If a particular option is not required, set its value to None.

                Example:
                    device_options = {
                        "db1": {
                            "datadevicename": "testdata",
                            "newdatadevicename": "testdatanew",
                            "newdatadevicepath": "/opt/sap/data/testdatanew.dat",
                            "logdevicename": "testlog",
                            "newlogdevicename": "testlognew",
                            "newlogdevicepath": "/opt/sap/data/testlognew.dat",
                            "newdatabasename": "db1new"
                        },
                        "db2": {
                            "datadevicename": None,
                            "newdatadevicename": None,
                            "newdatadevicepath": "/opt/sap/data/testdatanew.dat",
                            "logdevicename": "testlog",
                            "newlogdevicename": "testlognew",
                            "newlogdevicepath": "/opt/sap/data/testlognew.dat",
                            "newdatabasename": None
                        }
                    }

        Returns:
            object: A Job object containing details of the restore operation.

        Raises:
            SDKException: If `database_list` is empty.

        Example:
            >>> instance = SybaseInstance()
            >>> job = instance.restore_database(
            ...     destination_client="sybase_client",
            ...     destination_instance_name="SYBASE_INST",
            ...     database_list={"db1", "db2"},
            ...     timevalue="2023-10-01 12:00:00",
            ...     sybase_create_device=True,
            ...     rename_databases=True,
            ...     device_options={
            ...         "db1": {
            ...             "datadevicename": "testdata",
            ...             "newdatadevicename": "testdatanew",
            ...             "newdatadevicepath": "/opt/sap/data/testdatanew.dat",
            ...             "logdevicename": "testlog",
            ...             "newlogdevicename": "testlognew",
            ...             "newlogdevicepath": "/opt/sap/data/testlognew.dat",
            ...             "newdatabasename": "db1new"
            ...         }
            ...     },
            ...     copy_precedence=1
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if destination_client is None:
            destination_client = self.client_name

        if destination_instance_name is None:
            destination_instance_name = self.instance_name

        if database_list is None:
            raise SDKException('Instance', r'102', 'Restore Database List cannot be empty')

        request_json = self._get_sybase_restore_json(
            destination_client,
            destination_instance_name,
            database_list,
            timevalue,
            sybase_create_device,
            rename_databases,
            device_options,
            copy_precedence)

        return self._process_restore_response(request_json)

    def restore_to_disk(
        self,
        destination_client: str,
        destination_path: str,
        backup_job_ids: list,
        user_name: str,
        password: str
    ) -> object:
        """Perform an application-free restore to disk for a Sybase instance.

        This method restores Sybase backup data to a specified path on a destination client
        using the provided backup job IDs. The operation is performed using impersonation
        credentials for the destination client.

        Args:
            destination_client: The name of the destination client where the data will be restored.
            destination_path: The full path on the destination client where the data should be restored.
            backup_job_ids: List of backup job IDs to use for the disk restore.
            user_name: The impersonation username for the destination client.
            password: The impersonation user password for the destination client.

        Returns:
            An object representing the Job containing restore details.

        Raises:
            SDKException: If backup_job_ids is not provided as a list.

        Example:
            >>> sybase_instance = SybaseInstance()
            >>> job = sybase_instance.restore_to_disk(
            ...     destination_client="client01",
            ...     destination_path="/restore/location",
            ...     backup_job_ids=[1234, 5678],
            ...     user_name="restore_user",
            ...     password="secure_password"
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not isinstance(backup_job_ids, list):
            raise SDKException('Instance', '101')
        request_json = self._get_restore_to_disk_json(
            destination_client,
            destination_path,
            backup_job_ids,
            user_name,
            password
        )
        del request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["sybaseRstOption"]
        return self._process_restore_response(request_json)
