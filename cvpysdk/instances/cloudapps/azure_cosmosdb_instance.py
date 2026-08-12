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

""" File for operating on a cloud database instance.

AzureCosmosDBInstance:   Derived class from CloudAppsInstance Base class, representing a
                        Azure Cosmos DB instance( Azure CosmosDB Cassandra API, ..), and to
                        perform operations on that instance

AzureCosmosDBInstance:

    __init__()                      --  Initializes Azure Cosmos DB instance object with associated
    agent_object, instance name and instance id

    _get_instance_properties()      --  Retrieves cloud database related instance properties

    restore()                       -- Submits a restore request based on restore options
    restore_mongodbapi()            -- Submits a restore request for Cosmos MongoDB API based on restore options

"""

from __future__ import unicode_literals
import time
from typing import TYPE_CHECKING

from ..cainstance import CloudAppsInstance
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class AzureCosmosDBInstance(CloudAppsInstance):
    """
    Represents an instance of Azure Cosmos DB, including support for APIs such as
    Azure CosmosDB Cassandra API.

    This class provides functionality to initialize and manage a specific Azure Cosmos DB
    instance within a cloud application environment. It allows for the restoration of
    database instances using customizable restore options.

    Key Features:
        - Initialization of Azure Cosmos DB instance with agent, name, and ID
        - Restoration of database instance using specified restore options
        - Designed for integration with cloud application management workflows

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize an AzureCosmosDBInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Azure Cosmos DB instance.
            instance_name: The name of the Azure Cosmos DB instance.
            instance_id: Optional; the unique identifier for the instance. Defaults to None.

        Example:
            >>> agent = Agent(commcell_object, "AzureCosmosDB")
            >>> cosmos_instance = AzureCosmosDBInstance(agent, "MyCosmosDBInstance")
            >>> # Optionally, provide an instance ID
            >>> cosmos_instance_with_id = AzureCosmosDBInstance(agent, "MyCosmosDBInstance", "12345")

        #ai-gen-doc
        """
        self._agent_object = agent_object
        self._ca_instance_type = None
        self._browse_request = {}
        self._browse_url = None

        super(
            AzureCosmosDBInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

    def restore(self, restore_options: dict) -> 'Job':
        """Restore the content of this Azure Cosmos DB instance.

        This method initiates a restore operation for the instance using the specified options.

        Args:
            restore_options: Dictionary containing restore parameters. Supported keys include:
                - 'no_of_streams' (int): Number of streams to use for the restore.
                - 'destination_instance' (str): Name of the destination instance.
                - 'destination_instance_id' (int): ID of the destination instance.
                - 'paths' (list of str): List of paths to restore.
                - 'cloudinstancetype' (str): Cloud instance type.
                - 'backupsetname' (str): Name of the backup set.
                - 'unconditional_overwrite' (bool): Whether to overwrite existing data.
                - 'in_place' (bool): Whether to perform an in-place restore.
                - 'sourcedatabase' (str): Name of the source database.
                - 'destinationdatabase' (str): Name of the destination database.
                - 'srcstorageaccount' (str): Source storage account.
                - 'deststorageaccount' (str): Destination storage account.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> restore_options = {
            ...     'no_of_streams': 4,
            ...     'destination_instance': 'CosmosDBInstance2',
            ...     'destination_instance_id': 12345,
            ...     'paths': ['/dbs/mydb/colls/mycoll'],
            ...     'cloudinstancetype': 'Standard',
            ...     'backupsetname': 'DailyBackup',
            ...     'unconditional_overwrite': True,
            ...     'in_place': False,
            ...     'sourcedatabase': 'mydb',
            ...     'destinationdatabase': 'mydb_restored',
            ...     'srcstorageaccount': 'sourceaccount',
            ...     'deststorageaccount': 'destaccount'
            ... }
            >>> job = azure_cosmosdb_instance.restore(restore_options)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not (isinstance(restore_options, dict)):
            raise SDKException('Instance', '101')
        request_json = self._restore_json(restore_option=restore_options)

        request_json["taskInfo"]["associations"][0]["_type_"] = "INSTANCE_ENTITY"
        request_json["taskInfo"]["associations"][0]["cloudInstanceType"] = restore_options["cloudinstancetype"]
        request_json["taskInfo"]["associations"][0]["backupsetName"] = restore_options["backupsetname"]
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]

        cloud_app_restore_options = {
            "azureDbRestoreOptions": {
                "overwrite": restore_options["unconditional_overwrite"],
                "restoreEntity": [
                ]
            },
            "instanceType": restore_options["cloudinstancetype"]
        }

        if "CASSANDRA" in restore_options["cloudinstancetype"]:
            if restore_options.get("tempWriteThroughput", 0):
                cloud_app_restore_options["azureDbRestoreOptions"]["tempWriteThroughput"] = restore_options["tempWriteThroughput"]
            cloud_app_restore_options["azureDbRestoreOptions"]["restoreEntity"] = [
                {
                    "srcEntity": {
                        "databaseName": restore_options["sourcedatabase"],
                        "storageAccountName": restore_options["srcstorageaccount"]},
                    "destEntity": {
                        "databaseName": restore_options["destinatinodatabase"],
                        "storageAccountName": restore_options["deststorageaccount"]}}]

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = cloud_app_restore_options

        return self._process_restore_response(request_json)

    def restore_mongodbapi(self, restore_options: dict) -> 'Job':

        """
        Restores a MongoDB instance.

        This method initiates a restore operation for the instance using the specified options.

        Args:
            restore_options: Dictionary containing restore parameters. Supported keys include:
                - 'no_of_streams' (int): Number of streams to use for the restore.
                - 'destination_instance' (str): Name of the destination instance.
                - 'destination_instance_id' (int): ID of the destination instance.
                - 'cloudinstancetype' (str): Cloud instance type.
                - 'backupsetname' (str): Name of the backup set.
                - 'unconditional_overwrite' (bool): Whether to overwrite existing data.
                - 'sourcedatabase' (str): Name of the source database.
                - 'destination_database' (str): Name of the destination database.
                - 'srcstorageaccount' (str): Source storage account.
                - 'deststorageaccount' (str): Destination storage account.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> restore_options = {
            ...     'no_of_streams': 4,
            ...     'destination_instance': 'CosmosDBInstance2',
            ...     'destination_instance_id': 12345,
            ...     'cloudinstancetype': 'Standard',
            ...     'backupsetname': 'DailyBackup',
            ...     'unconditional_overwrite': True,
            ...     'sourcedatabase': 'mydb',
            ...     'destination_database': 'mydb_restored',
            ...     'srcstorageaccount': 'sourceaccount',
            ...     'deststorageaccount': 'destaccount'
            ... }
            >>> job = azure_cosmosdb_instance.restore_mongodbapi(restore_options)
            >>> print(f"Restore job started with ID: {job.job_id}")

        """
        request_json = self._restore_json(restore_option=restore_options)
        cloud_app_restore_options = {
            "azureDbRestoreOptions": {
                "overwrite": restore_options["unconditional_overwrite"],
                "restoreEntity": [
                ]
            },
            "instanceType": restore_options["cloudinstancetype"]
        }
        if restore_options.get("tempWriteThroughput", 0):
            cloud_app_restore_options["azureDbRestoreOptions"]["tempWriteThroughput"] = restore_options["tempWriteThroughput"]
        cloud_app_restore_options["azureDbRestoreOptions"]["restoreEntity"] = [
            {
                "srcEntity": {
                    "databaseName": restore_options["sourcedatabase"],
                    "storageAccountName": restore_options["srcstorageaccount"]},
                "destEntity": {
                    "databaseName": restore_options["destination_database"],
                    "storageAccountName": restore_options["deststorageaccount"]}}]

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = cloud_app_restore_options
        request_json["taskInfo"]["associations"][0]["_type_"] = "INSTANCE_ENTITY"
        request_json["taskInfo"]["associations"][0]["cloudInstanceType"] = restore_options["cloudinstancetype"]
        request_json["taskInfo"]["associations"][0]["backupsetName"] = restore_options["backupsetname"]
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"] = {"sourceItem": [
            "/" + restore_options["srcstorageaccount"] + "/" +restore_options["sourcedatabase"]]}
        mongodb_destination_options = {
            "destClient": {
                "clientId": restore_options["client_id"],
                "clientName": restore_options["client_name"]
                },
            "destinationInstance":{
                "clientId": restore_options["client_id"],
                "clientName": restore_options["client_name"],
                "applicationId": 134,
                "appName": "Cloud Apps",
                "instanceId": int(restore_options["destination_instance_id"]),
                "instanceName": restore_options["destination_instance"]
            },
            "noOfStreams": restore_options["no_of_streams"]
        }
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["destination"] = mongodb_destination_options

        return self._process_restore_response(request_json)

