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
"""
from __future__ import unicode_literals
from ..bigdataappsinstance import BigDataAppsInstance
from ...exception import SDKException


class MongoDBInstance(BigDataAppsInstance):
    """
    Class for representing an Instance of the MongoDB  instance
    """
    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the Mongo DB class
            Args:
                agent_object    (object)  --  instance of the Agent class
                instance_name   (str)     --  name of the instance
                instance_id     (str)     --  id of the instance
                    default: None
            Returns:
                object - instance of the Instance class
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

    def restore(self, restore_options):
        """
            Restores the content of this instance content
            Args:
                restore_options : dict of keyword arguments needed to submit a MongoDB restore:
                    Example:
                       restore_options = {
                        restore_dict = {}
                            restore_dict["no_of_streams"] = 2
                            restore_dict["multinode_restore"] = True
                            restore_dict["destination_instance"] = self.client_name
                            restore_dict["destination_instance_id"] = self._instance_object.instance_id
                            restore_dict["paths"] = ["/"]
                            restore_dict["mongodb_restore"] = True
                            restore_dict["destination_client_id"] = self._client_obj.client_id
                            restore_dict["destination_client_name"] = self._client_obj.client_name
                            restore_dict["overwrite"] = True
                            restore_dict["client_type"] = 29
                            restore_dict["destination_appTypeId"] = 64
                            restore_dict["backupset_name"] = self.backupsetname
                            restore_dict["_type_"] = 5
                            restore_dict["subclient_id"] = -1
                            restore_dict["source_shard_name"] = self.replicaset
                            restore_dict["destination_shard_name"] = self.replicaset
                            restore_dict["hostname"] = self.primary_host
                            restore_dict["clientName"] = self.master_node
                            restore_dict["desthostName"] = self.primary_host
                            restore_dict["destclientName"] = self.master_node
                            restore_dict["destPortNumber"] = self.port
                            restore_dict["destDataDir"] = self.bin_path
                            restore_dict["bkpDataDir"] = self.bkp_dir_path
                            restore_dict["backupPortNumber"] = self.port
                            restore_dict["restoreDataDir"] = self.bkp_dir_path
                            restore_dict["primaryPort"] = self.port
                        }
            Returns:
                object - instance of the Job class for this restore job
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
                    {
                        "srcShardName":  restore_options.get("source_shard_name", False),
                        "destShardName": restore_options.get("destination_shard_name", False),
                        "target": {
                            "hostName": restore_options.get("hostname", False),
                            "clientName": restore_options.get("clientName", False),
                            "clientId": int(client_object_source.client_id)
                        },
                        "destHostName": restore_options.get("desthostName", False),
                        "destPortNumber": restore_options.get("destPortNumber", False),
                        "destDataDir":  restore_options.get("restoreDataDir", False),
                        "bkpSecondary": {
                            "clientName": restore_options.get("clientName", False),
                            "hostName": restore_options.get("hostname", False),
                            "clientId": int(client_object_source.client_id)
                        },
                        "bkpHostName": restore_options.get("hostname", False),
                        "bkpPortNumber": restore_options.get("backupPortNumber", False),
                        "bkpDataDir": restore_options.get("bkpDataDir", False),
                        "useDestAsSecondary": False,
                        "primaryPortNumber":restore_options.get("primaryPort", False),
                    }
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

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "distributedAppsRestoreOptions"] = distributed_restore_json
        return self._process_restore_response(request_json)
