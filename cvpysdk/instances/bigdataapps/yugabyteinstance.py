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
from typing import TYPE_CHECKING

from ..bigdataappsinstance import BigDataAppsInstance
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class YugabyteInstance(BigDataAppsInstance):
    """
    Represents an instance of a Yugabyte database within a big data application environment.

    This class encapsulates the details and operations related to a Yugabyte instance,
    including initialization with agent and instance metadata, and restoration of the
    instance using specified restore options.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Restoration of the Yugabyte instance using customizable restore options
        - Inherits capabilities from BigDataAppsInstance for integration with big data applications

    #ai-gen-doc
    """
    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new YugabyteInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Yugabyte instance.
            instance_name: The name of the Yugabyte instance.
            instance_id: Optional; the unique identifier for the instance. Defaults to None.

        Example:
            >>> agent = Agent(commcell_object, "Yugabyte")
            >>> yugabyte_instance = YugabyteInstance(agent, "YB_Instance1")
            >>> # With instance ID
            >>> yugabyte_instance_with_id = YugabyteInstance(agent, "YB_Instance2", "12345")

        #ai-gen-doc
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

    def restore(self, restore_options: dict) -> 'Job':
        """Restore the content of this Yugabyte instance using the specified options.

        Args:
            restore_options: Dictionary containing keyword arguments required to submit a YugabyteDB restore job.
                Common keys include:
                    - 'no_of_streams': Number of streams to use for restore.
                    - 'multinode_restore': Boolean indicating if multinode restore is enabled.
                    - 'destination_instance': Name of the destination instance.
                    - 'destination_instance_id': ID of the destination instance.
                    - 'paths': List of paths to be restored.
                    - 'destination_client_id': ID of the destination client.
                    - 'destination_client_name': Name of the destination client.
                    - 'client_type': Type of the client.
                    - 'destination_appTypeId': Application type ID for the destination.
                    - 'backupset_name': Name of the backup set.
                    - 'sql_fromtable': Source SQL table name.
                    - 'cql_fromtable': Source CQL table name.
                    - 'sql_totable': Target SQL table name.
                    - 'cql_totable': Target CQL table name.
                    - 'accessnodes': List of access nodes.
                    - 'kms_config': KMS configuration.
                    - 'kmsconfigUUID': UUID for the KMS configuration.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> restore_options = {
            ...     'no_of_streams': 4,
            ...     'multinode_restore': True,
            ...     'destination_instance': 'yb_instance_dest',
            ...     'destination_instance_id': 12345,
            ...     'paths': ['/data/backup1', '/data/backup2'],
            ...     'destination_client_id': 67890,
            ...     'destination_client_name': 'yb_client_dest',
            ...     'client_type': 1,
            ...     'destination_appTypeId': 1001,
            ...     'backupset_name': 'daily_backup',
            ...     'sql_fromtable': 'public.table1',
            ...     'cql_fromtable': 'keyspace1.table2',
            ...     'sql_totable': 'public.table1_restored',
            ...     'cql_totable': 'keyspace1.table2_restored',
            ...     'accessnodes': ['node1', 'node2'],
            ...     'kms_config': 'default_kms',
            ...     'kmsconfigUUID': 'abc123-uuid'
            ... }
            >>> job = yugabyte_instance.restore(restore_options)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
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