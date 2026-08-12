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
""" File for operating on a MongoDB instance.
MongoDBInstance :   Derived class from BigDataAppsInstance Base class, representing a
                        MongoDBInstance instance and to perform operations on that instance
MongoDBInstance:
    __init__()                      --  Initializes MongoDB instance object with associated
    agent_object, instance name and instance id
    restore()                       -- Submits a restore request based on restore options
    restore_collection()            -- collection based restore.
    get_restore_json_for_out_of_place() -- Get restore JSON for out-of-place restore
    restore_out_of_place()          -- Out-of-place restore for MongoDB instance
    discover_mongodb_nodes()        -- Runs machine calss discovery
    refresh_mongo_instance()        -- Refresh mongoDB call by yaking machine response as input

"""
from __future__ import unicode_literals

from typing import Any, Dict

from ..bigdataappsinstance import BigDataAppsInstance
from ...exception import SDKException
from ...job import Job

class MongoDBInstance(BigDataAppsInstance):
    """
    Represents an instance of a MongoDB database within a big data application environment.

    This class provides functionality to manage and interact with MongoDB instances,
    including initialization with agent and instance details, and performing restore
    operations at both the database and collection levels.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Restore entire MongoDB instance using customizable restore options
        - Restore specific MongoDB collections with targeted restore options

    #ai-gen-doc
    """
    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a MongoDBInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this MongoDB instance.
            instance_name: The name of the MongoDB instance.
            instance_id: Optional; the unique identifier for the MongoDB instance. Defaults to None.

        Example:
            >>> agent = Agent(commcell_object, "MongoDB")
            >>> mongo_instance = MongoDBInstance(agent, "MongoInstance1")
            >>> # Optionally, provide an instance ID
            >>> mongo_instance_with_id = MongoDBInstance(agent, "MongoInstance2", "12345")

        #ai-gen-doc
        """
        self._agent_object = agent_object
        self._browse_request = {}
        self._browse_url = None
        super(
            MongoDBInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

    def restore(self, restore_options: Dict[str, Any]) -> 'Job':
        """Restore the content of this MongoDB instance using the specified options.

        Args:
            restore_options: Dictionary of keyword arguments required to submit a MongoDB restore job.
                The dictionary should include keys such as:
                    - "no_of_streams": Number of streams to use for restore (int)
                    - "multinode_restore": Whether to perform a multinode restore (bool)
                    - "destination_instance": Name of the destination instance (str)
                    - "destination_instance_id": ID of the destination instance (int)
                    - "paths": List of paths to restore (list of str)
                    - "mongodb_restore": Flag to indicate MongoDB restore (bool)
                    - "destination_client_id": ID of the destination client (int)
                    - "destination_client_name": Name of the destination client (str)
                    - "overwrite": Whether to overwrite existing data (bool)
                    - "client_type": Type of client (int)
                    - "destination_appTypeId": Application type ID for destination (int)
                    - "backupset_name": Name of the backup set (str)
                    - "_type_": Type identifier (int)
                    - "subclient_id": Subclient ID (int)
                    - "source_shard_name": Name of the source shard (str)
                    - "destination_shard_name": Name of the destination shard (str)
                    - "hostname": Hostname for restore (str)
                    - "clientName": Client name for restore (str)
                    - "desthostName": Destination host name (str)
                    - "destclientName": Destination client name (str)
                    - "destPortNumber": Destination port number (int)
                    - "destDataDir": Destination data directory (str)
                    - "bkpDataDir": Backup data directory (str)
                    - "backupPortNumber": Backup port number (int)
                    - "restoreDataDir": Restore data directory (str)
                    - "primaryPort": Primary port number (int)
                    - "clusterConfig": Cluster configuration data (Any)

        Returns:
            Job: An instance of the Job class representing the submitted restore job.

        Example:
            >>> restore_options = {
            ...     "no_of_streams": 2,
            ...     "multinode_restore": True,
            ...     "destination_instance": "MongoDB_Instance_01",
            ...     "destination_instance_id": 123,
            ...     "paths": ["/"],
            ...     "mongodb_restore": True,
            ...     "destination_client_id": 456,
            ...     "destination_client_name": "MongoDB_Client_01",
            ...     "overwrite": True,
            ...     "client_type": 29,
            ...     "destination_appTypeId": 64,
            ...     "backupset_name": "DailyBackupSet",
            ...     "_type_": 5,
            ...     "subclient_id": -1,
            ...     "source_shard_name": "shard01",
            ...     "destination_shard_name": "shard01",
            ...     "hostname": "mongo-primary.example.com",
            ...     "clientName": "mongo-master",
            ...     "desthostName": "mongo-primary.example.com",
            ...     "destclientName": "mongo-master",
            ...     "destPortNumber": 27017,
            ...     "destDataDir": "/data/db",
            ...     "bkpDataDir": "/backup/db",
            ...     "backupPortNumber": 27017,
            ...     "restoreDataDir": "/backup/db",
            ...     "primaryPort": 27017,
            ...     "clusterConfig": {"replicaSet": "rs0"}
            ... }
            >>> job = mongodb_instance.restore(restore_options)
            >>> print(f"Restore job submitted: {job}")
            >>> # The returned Job object can be used to monitor restore progress

        #ai-gen-doc
        """
        if not (isinstance(restore_options, dict)):
            raise SDKException('Instance', '101')
        request_json = self._restore_json(restore_option=restore_options)

        request_json["taskInfo"]["associations"][0]["subclientId"] = restore_options.get(
            "subclient_id", -1)
        request_json["taskInfo"]["associations"][0]["backupsetName"] = restore_options.get(
            "backupset_name")
        request_json["taskInfo"]["associations"][0]["_type_"] = restore_options.get(
            "_type_")

        distributed_restore_json = {
            "distributedRestore": True,
        }


        client_object_source = self._commcell_object.clients.get(restore_options['clientName'])
        client_object_destination = self._commcell_object.clients.get(restore_options['destclientName'])

        distributed_restore_json["mongoDBRestoreOptions"] = {
                "destShardList": [
                ],
                "restoreFilesOnly": False,
                "recover": True,
                "pointInTimeToEndOfBackup": True,
                "latestOpLogSync": True,
                "latestEndOfBackup": True,
                "isGranularRecovery": False,
                "autoDBShutDown": True,
                "isInplaceRestore": True
            }

        if restore_options.get("clusterConfig"):
            for host_info in restore_options.get("clusterConfig"):
                shard_name = host_info.get("replSet", "")
                hostname = host_info.get("host", "")
                port = int(host_info.get("port", ""))
                clientname = host_info.get("clientname", "")
                clientid = int(host_info.get("clientid", ""))
                dbpath =  host_info.get("dbpath", "")

                shard_entry = {
                    "srcShardName": shard_name,
                    "destShardName": shard_name,
                    "target": {
                        "hostName": hostname,
                        "clientName": clientname,
                        "clientId": clientid
                    },
                    "destHostName": hostname,
                    "destPortNumber": port,
                    "destDataDir": dbpath,
                    "bkpSecondary": {
                        "clientName": clientname,
                        "hostName": hostname,
                        "clientId": clientid
                    },
                    "bkpHostName": hostname,
                    "bkpPortNumber": port,
                    "bkpDataDir": dbpath,
                    "useDestAsSecondary": False,
                    "primaryPortNumber": port
                }

                distributed_restore_json["mongoDBRestoreOptions"]["destShardList"].append(shard_entry)

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "distributedAppsRestoreOptions"] = distributed_restore_json
        return self._process_restore_response(request_json)
    
    def get_restore_json_for_out_of_place(self, restore_options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the JSON payload for an out-of-place restore operation based on the provided restore options.

        Args:
            restore_options: Dictionary of keyword arguments required to submit a MongoDB restore job.
                The dictionary should include keys such as:
                    "subclient_id": ID of the subclient (int),
                    "backupset_id": ID of the backupset (int),

                    "src_client_id": ID of the source client (int),
                    "src_client_name": Name of the source client (str),
                    "src_instance_id": ID of the source instance (int),
                    "src_instance_name": Name of the source instance (str),
                    "src_shard_name": Name of the source shard (str),
                    "src_host_name": Hostname of the source (str),
                    "src_port": Port number of the source (int),
                    "src_dbpath": Database path of the source (str),
                    "src_client_id_secondary": ID of the secondary source client (int),

                    "dest_client_id": ID of the destination client (int),
                    "dest_client_name": Name of the destination client (str),
                    "dest_instance_id": ID of the destination instance (int),
                    "dest_instance_name": Name of the destination instance (str),
                    "dest_cluster_config": Configuration of the destination cluster (dict),

                    "recover": recover_db,
                    "auto_db_shutdown": auto_restore

        Returns:
            dict: Returns a dictionary representing the JSON payload for the restore operation, which can be used to submit an out-of-place restore job.

        """

        request_json = {
            "taskInfo": {
                "associations": [
                    {
                        "subclientId": int(restore_options.get("subclient_id", -1)),
                        "applicationId": 64,
                        "clientName": restore_options.get("src_instance_name"),
                        "backupsetId": int(restore_options.get("backupset_id")),
                        "instanceId": int(restore_options.get("src_instance_id")),
                        "clientId": int(restore_options.get("src_client_id")),
                        "commCellId": 2,
                        "_type_": 5
                    }
                ],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": "RESTORE",
                            "operationType": "RESTORE"
                        },
                        "options": {
                            "restoreOptions": {
                                "commonOptions": {
                                    "unconditionalOverwrite": False
                                },
                                "browseOption": {
                                    "commCellId": 2,
                                    "backupset": {
                                        "backupsetId": int(restore_options.get("backupset_id")),
                                        "clientId": int(restore_options.get("src_client_id")),
                                    },
                                    "timeRange": {}
                                },
                                "destination": {
                                    "noOfStreams": 2,
                                    "destClient": {
                                        "clientId": int(restore_options.get("dest_client_id")),
                                        "clientName": restore_options.get("dest_instance_name")
                                    },
                                    "destinationInstance": {
                                        "clientId": int(restore_options.get("dest_client_id")),
                                        "clientName": restore_options.get("dest_instance_name"),
                                        "applicationId": 64,
                                        "appName": "Big Data Apps",
                                        "instanceId": int(restore_options.get("dest_instance_id")),
                                        "instanceName": restore_options.get("dest_instance_name")
                                    }
                                },
                                "fileOption": {
                                    "sourceItem": [
                                        "/"
                                    ]
                                },
                                "distributedAppsRestoreOptions": {
                                    "distributedRestore": True,
                                    "mongoDBRestoreOptions": {
                                        "destShardList": [],
                                        "destGranularEntityList": [],
                                        "recover": restore_options.get("recover", True),
                                        "latestOpLogSync": True,
                                        "pointInTimeToEndOfBackup": True,
                                        "latestEndOfBackup": True,
                                        "isGranularRecovery": False,
                                        "autoDBShutDown": restore_options.get("auto_db_shutdown", True)
                                    }
                                },
                                "qrOption": {
                                    "destAppTypeId": 64
                                }
                            },
                            "commonOpts": {
                                "notifyUserOnJobCompletion": True,
                            }
                        }
                    }
                ]
            }
        }

        if restore_options.get("dest_cluster_config"):
            for host_info in restore_options.get("dest_cluster_config"):
                shard_name = host_info.get("replSet", "")
                hostname = host_info.get("host", "")
                port = int(host_info.get("port", ""))
                clientname = host_info.get("clientname", "")
                clientid = int(host_info.get("clientid", ""))
                dbpath =  host_info.get("dbpath", "")

                shard_entry = {
                    "srcShardName": restore_options.get("src_shard_name"),
                    "destShardName": shard_name,
                    "target": {
                        "hostName": hostname,
                        "clientName": clientname,
                        "clientId": int(clientid)
                    },
                    "destHostName": hostname,
                    "destPortNumber": int(port),
                    "destDataDir": dbpath,
                    "bkpSecondary": {
                        "clientName": restore_options.get("src_client_name"),
                        "hostName": restore_options.get("src_hostname"),
                        "clientId": int(restore_options.get("src_client_id_secondary"))
                    },
                    "bkpHostName": restore_options.get("src_hostname"),
                    "bkpPortNumber": int(restore_options.get("src_port")),
                    "bkpDataDir": restore_options.get("src_dbpath"),
                    "useDestAsSecondary": False,
                    "primaryPortNumber": int(restore_options.get("src_port"))
                }

                request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                    "distributedAppsRestoreOptions"]["mongoDBRestoreOptions"]["destShardList"].append(shard_entry)


        return request_json
    
    def restore_out_of_place(self, restore_options: Dict[str, Any]) -> 'Job':
        """
        Restore the content of this MongoDB instance to a different location using the specified options.

        Args:
            restore_options: Dictionary of keyword arguments required to submit a MongoDB restore job.
                The dictionary should include keys such as:
                    "subclient_id": ID of the subclient (int),
                    "backupset_id": ID of the backupset (int),

                    "src_client_id": ID of the source client (int),
                    "src_client_name": Name of the source client (str),
                    "src_instance_id": ID of the source instance (int),
                    "src_instance_name": Name of the source instance (str),
                    "src_shard_name": Name of the source shard (str),
                    "src_host_name": Hostname of the source (str),
                    "src_port": Port number of the source (int),
                    "src_dbpath": Database path of the source (str),
                    "src_client_id_secondary": ID of the secondary source client (int),

                    "dest_client_id": ID of the destination client (int),
                    "dest_client_name": Name of the destination client (str),
                    "dest_instance_id": ID of the destination instance (int),
                    "dest_instance_name": Name of the destination instance (str),
                    "dest_cluster_config": Configuration of the destination cluster (dict),

                    "recover": recover_db,
                    "auto_db_shutdown": auto_restore

        Returns:
            Job: An instance of the Job class representing the submitted restore job.
        """
        if not (isinstance(restore_options, dict)):
            raise SDKException('Instance', '101')
        
        request_json = self.get_restore_json_for_out_of_place(restore_options)

        return self._process_restore_response(request_json)

    def restore_collection(self, restore_options: dict) -> 'Job':
        """Restore the content of this MongoDB instance for an in-place collection restore.

        Args:
            restore_options: A dictionary containing the required options for the MongoDB restore job.
                The dictionary should include keys such as:
                    - "no_of_streams": int, number of streams to use for restore
                    - "multinode_restore": bool, whether to use multinode restore
                    - "destination_instance": str, name of the destination instance
                    - "destination_instance_id": int, ID of the destination instance
                    - "paths": list, list of collection paths to restore
                    - "mongodb_restore": bool, set to True for MongoDB restore
                    - "destination_client_id": int, ID of the destination client
                    - "destination_client_name": str, name of the destination client
                    - "overwrite": bool, whether to overwrite existing data
                    - "client_type": int, client type identifier
                    - "destination_appTypeId": int, application type ID for destination
                    - "backupset_name": str, name of the backup set
                    - "_type_": int, type identifier
                    - "subclient_id": int, ID of the subclient
                    - "source_shard_name": str, name of the source shard
                    - "destination_shard_name": str, name of the destination shard
                    - "hostname": str, host name for restore
                    - "clientName": str, client name for restore
                    - "desthostName": str, destination host name
                    - "destclientName": str, destination client name
                    - "destPortNumber": int, destination port number
                    - "destDataDir": str, destination data directory
                    - "bkpDataDir": str, backup data directory
                    - "backupPortNumber": int, backup port number
                    - "restoreDataDir": str, restore data directory
                    - "primaryPort": int, primary port number

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> restore_options = {
            ...     "no_of_streams": 2,
            ...     "multinode_restore": True,
            ...     "destination_instance": "MongoDB_Instance1",
            ...     "destination_instance_id": 101,
            ...     "paths": ["/"],
            ...     "mongodb_restore": True,
            ...     "destination_client_id": 201,
            ...     "destination_client_name": "MongoDB_Client1",
            ...     "overwrite": True,
            ...     "client_type": 29,
            ...     "destination_appTypeId": 64,
            ...     "backupset_name": "defaultBackupSet",
            ...     "_type_": 5,
            ...     "subclient_id": 301,
            ...     "source_shard_name": "shard1",
            ...     "destination_shard_name": "shard1",
            ...     "hostname": "mongo-primary",
            ...     "clientName": "mongo-master",
            ...     "desthostName": "mongo-primary",
            ...     "destclientName": "mongo-master",
            ...     "destPortNumber": 27017,
            ...     "destDataDir": "/data/db",
            ...     "bkpDataDir": "/backup/db",
            ...     "backupPortNumber": 27017,
            ...     "restoreDataDir": "/backup/db",
            ...     "primaryPort": 27017
            ... }
            >>> job = mongodb_instance.restore_collection(restore_options)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not (isinstance(restore_options, dict)):
            raise SDKException('Instance', '101')
        request_json = self._restore_json(restore_option=restore_options)

        request_json["taskInfo"]["associations"][0]["subclientId"] = restore_options.get(
            "subclient_id", )
        request_json["taskInfo"]["associations"][0]["backupsetName"] = restore_options.get(
            "backupset_name")
        request_json["taskInfo"]["associations"][0]["_type_"] = restore_options.get(
            "_type_")
        distributed_restore_json = {
            "distributedRestore": True,
        }
        client_object_source = self._commcell_object.clients.get(restore_options['clientName'])
        client_object_destination = self._commcell_object.clients.get(restore_options['destclientName'])
        distributed_restore_json["mongoDBRestoreOptions"] = {
                "destShardList": [],
                "destGranularEntityList": [
                    {
                        "srcDbName": restore_options.get("source_db_name", False),
                        "destDbName": restore_options.get("restore_db_name", False),
                        "isDbEntity": True,
                        "destCollectionName": ""
                    }
                ],
                "restoreFilesOnly": False,
                "recover": True,
                "pointInTimeToEndOfBackup": True,
                "latestOpLogSync": True,
                "latestEndOfBackup": True,
                "isGranularRecovery": True
            }
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "distributedAppsRestoreOptions"] = distributed_restore_json
        return self._process_restore_response(request_json)

    def discover_mongo_nodes(self, options: dict):
        """
        Discovers MongoDB member nodes associated with instance

        Args:
            options (dict): Dictionary with all required arguments.

            Required keys:
                instance_id         (int)   --  Instance ID of MongoDB instance
                master_node         (str)   --  Master of MongoDB Instance
                master_hostname     (str)   --  Hostname of master node
                master_client_id    (int)   --  Client ID of master Node
                port                (int)   --  Port where mongos / mongod services are running
                bin_path            (str)   --  Binary path for MongoDB installation
                db_user             (str)   --  Database user
                os_user             (str)   --  OS user to contact and run command
                db_credential_id    (int)   --  Database credential ID
                ssl_credential_id   (int)   --  SSL credential ID

        Returns:
            tuple: (flag, response) received from Discover API
        """

        required = [
            "instance_id", "master_node", "master_hostname", "master_client_id",
            "port", "bin_path", "os_user", "db_credential_id", "ssl_credential_id"
        ]

        # check for missing keys
        missing = [key for key in required if key not in options or options[key] in (None, "")]
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")

        # build request payload
        request_json = {
            "distAppsProperties": {
                "clusterType": 8,  # MongoDB cluster type
                "subclient": {
                    "instanceId": options["instance_id"]
                },
                "clusterConfig": {
                    "mdbConfig": {
                        "mdbServerType": "STATUS_UNKNOWN",
                        "masterNode": {
                            "hostName": options["master_hostname"],
                            "osUser": options["os_user"],
                            "portNumber": options["port"],
                            "binPath": options["bin_path"],
                            "client": {
                                "clientId": options["master_client_id"],
                                "clientName": options["master_node"]
                            }
                        },
                        "sslCMCredInfo": {
                            "credentialId": options["ssl_credential_id"],
                            "credentialName": ""
                        },
                        "authCMCredInfo": {
                            "credentialId": options["db_credential_id"],
                            "credentialName": ""
                        }
                    }
                }
            },
            "path": "/",
            "foldersOnly": True,
            "clientEntity": {
                "clientId": options["master_client_id"]
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST',
            self._services['MACHINE_BROWSE'] % (options["master_client_id"]),
            request_json
        )

        return flag, response
        

    def refresh_mongo_instance(self, options: dict):
        """
        Refreshes a MongoDB instance configuration with new cluster details.

        Args:
            options (dict): Dictionary containing required arguments.

            Required keys:
                config (dict): Response JSON from MachineBrowse containing updated
                               MongoDB configuration.
                               Expected format:
                                   {
                                       "browseItems": [
                                           {
                                               "mdbItem": {
                                                   "mdbConfig": { ... }
                                               }
                                           }
                                       ]
                                   }
                instance_id (int): ID of the MongoDB instance to refresh.

        Returns:
            dict: Updated instance JSON if successful.

        Raises:
            ValueError: If required keys are missing or config format is invalid.
            Exception: If fetching or updating the instance properties fails.
        """

        # Step 1: Validate required keys
        required = ["config", "instance_id"]
        missing = [key for key in required if key not in options or options[key] in (None, "")]
        if missing:
            raise ValueError(f"Missing required parameters: {missing}")

        config = options["config"]
        instance_id = options["instance_id"]

        # Step 2: Fetch current instance properties
        flag, inst_response = self._cvpysdk_object.make_request(
            'GET',
            self._services['INSTANCE'] % (instance_id)
        )
        if not flag:
            raise Exception("Failed to get instance properties")

        instance_json = inst_response.json()

        # Step 3: Extract new mdbConfig from MachineBrowse response
        try:
            new_mdb_config = config['browseItems'][0]['mdbItem']['mdbConfig']
        except (KeyError, IndexError, TypeError):
            raise ValueError("Invalid config format. 'browseItems[0].mdbItem.mdbConfig' not found.")

        props = instance_json.get('instanceProperties')
        if isinstance(props, list):
            props = props[0]  # Take the first element if wrapped in a list

        # Step 4: Preserve critical values from old mdbConfig
        old_mdb_config = props['distributedClusterInstance']['clusterConfig']['mdbConfig']
        for key in ("sslCMCredInfo", "authCMCredInfo", "masterNode"):
            if key in old_mdb_config:
                new_mdb_config[key] = old_mdb_config[key]

        # Step 5: Replace mdbConfig in instance JSON
        props['distributedClusterInstance']['clusterConfig']['mdbConfig'] = new_mdb_config
        request_json = {"instanceProperties": props}

        # Step 6: Submit updated config
        flag, update_response = self._cvpysdk_object.make_request(
            'POST',
            self._services['INSTANCE'] % (instance_id),
            request_json
        )
        if not flag:
            raise Exception(f"Update Failed: {update_response.text}")

        return update_response.json()


