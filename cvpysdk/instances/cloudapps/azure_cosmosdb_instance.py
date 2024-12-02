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

"""

from __future__ import unicode_literals
import time
from ..cainstance import CloudAppsInstance
from ...exception import SDKException


class AzureCosmosDBInstance(CloudAppsInstance):
    """
    Class for representing an Instance of the Azure Cosmos DB instance such as
    Azure CosmosDB Cassandra API

    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the AzureCosmosDBInstance class

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class

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

    def restore(self, restore_options):
        """
            Restores the content of this instance content

            Args:
                restore_options  : dict of keyword arguments as follows:
                    Example:
                       restore_options = {
                            'no_of_streams': no_of_stream,
                            'destination_instance': 'destination_instance_name',
                            'destination_instance_id': destination_instance_id,
                            'paths': ['path_to_restored'],
                            'cloudinstancetype': 'cloudinstancetype,
                            'backupsetname': 'backupsetname',
                            'unconditional_overwrite': True,
                            'in_place': True,
                            'sourcedatabase': 'sourcekeyspacename',
                            'destinationdatabase': 'destinationkeyspacename',
                            'srcstorageaccount': 'sourcestorageaccount',
                            'deststorageaccount': 'destinationstorageaccount'
                        }

            Returns:

                object - instance of the Job class for this restore job
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
