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
""" File for operating on a yugabyte instance.
YugabyteInstance:   Derived class from BigDataAppsInstance Base class, representing a
                        YugabyteDB instance, and to perform operations on that instance
YugabyteInstance:
    __init__()                      --  Initializes YugabyteDB instance object with associated
    agent_object, instance name and instance id
    restore()                       -- Submits a restore request based on restore options
"""
from __future__ import unicode_literals
import time
from ..bigdataappsinstance import BigDataAppsInstance
from ...exception import SDKException


class YugabyteInstance(BigDataAppsInstance):
    """
    Class for representing an Instance of the yugabyte instance
    """
    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the YugabyteInstance class
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
            YugabyteInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

    def restore(self, restore_options):
        """
            Restores the content of this instance content
            Args:
                restore_options : dict of keyword arguments needed to submit a yugabytedb restore:

                    Example:
                       restore_options = {
                            'no_of_streams': no_of_stream,
                            'multinode_restore': multinode_restore,
                            'destination_instance': 'destination_instance_name',
                            'destination_instance_id': destination_instance_id,
                            'paths': ['paths_to_be_restored'],
                            'destination_client_id': 'destination_client_id,
                            'destination_client_name': 'destination_client_name',
                            'client_type': client_type,
                            'destination_appTypeId': destination_appTypeId,
                            'backupset_name': 'backupset_name',
                            'sql_fromtable': 'sql_fromtable',
                            'cql_fromtable': 'cql_fromtable',
                            'sql_totable': 'sql_totable',
                            'cql_totable': 'cql_totable',
                            'accessnodes': ['accessnodes'],
                            'kms_config': 'kms_config',
                            'kmsconfigUUID': 'kmsconfigUUID
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

        distributed_restore_json = {
            "distributedRestore": True,
        }

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = {
            "instanceType": "AMAZON_S3"
        }
        distributed_restore_json["noSQLGenericRestoreOptions"] = {
            "tableMap": [
                {
                    "fromTable": restore_options.get("sql_fromtable"),
                    "toTable": restore_options.get("sql_totable")
                },
                {
                    "fromTable": restore_options.get("cql_fromtable"),
                    "toTable": restore_options.get("cql_totable")
                }
            ]
        }
        distributed_restore_json["yugabyteDBRestoreOptions"] = {
            "kmsConfigName": restore_options.get("kms_config"),
            "kmsConfigUUID": restore_options.get("kmsconfigUUID")
        }
        distributed_restore_json["clientType"] = restore_options.get("client_type")
        distributed_restore_json["isMultiNodeRestore"] = True
        access_nodes = []
        for node in restore_options.get("accessnodes"):
            client_object = self._commcell_object.clients.get(node)
            client_id = int(client_object.client_id)
            access_node = {
                "clientId": client_id,
                "clientName": client_object.client_name
            }
            access_nodes.append(access_node)
        distributed_restore_json["dataAccessNodes"] = {
            "dataAccessNodes": access_nodes
        }

        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "distributedAppsRestoreOptions"] = distributed_restore_json
        return self._process_restore_response(request_json)
