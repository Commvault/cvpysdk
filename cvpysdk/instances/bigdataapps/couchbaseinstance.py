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
""" File for operating on a couchbase instance.
CouchbaseInstance:   Derived class from BigDataAppsInstance Base class, representing a
                        Couchbase instance and to perform operations on that instance
CouchbaseInstance:
    __init__()                      --  Initializes couchbase instance object with associated
    agent_object, instance name and instance id
    restore()                       -- Submits a restore request based on restore options
"""
from __future__ import unicode_literals

from typing import TYPE_CHECKING

from ..bigdataappsinstance import BigDataAppsInstance
from ...exception import SDKException

if TYPE_CHECKING:
    from ...job import Job

class CouchbaseInstance(BigDataAppsInstance):
    """
    Represents a Couchbase database instance within a big data application environment.

    This class encapsulates the details and operations related to a Couchbase instance,
    including initialization with agent and instance metadata, and providing functionality
    to restore the instance using specified restore options.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Restore operation with customizable restore options
        - Inherits capabilities from BigDataAppsInstance for integration with big data workflows

    #ai-gen-doc
    """
    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new CouchbaseInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Couchbase instance.
            instance_name: The name of the Couchbase instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, a new instance will be created.

        Example:
            >>> agent = Agent(commcell_object, "Couchbase")
            >>> couchbase_instance = CouchbaseInstance(agent, "Couchbase_Instance1")
            >>> # With instance ID
            >>> couchbase_instance = CouchbaseInstance(agent, "Couchbase_Instance1", "12345")

        #ai-gen-doc
        """
        self._agent_object = agent_object
        self._browse_request = {}
        self._browse_url = None
        super(
            CouchbaseInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

    def restore(self, restore_options: dict) -> 'Job':
        """Restore the content of this Couchbase instance using the specified options.

        Args:
            restore_options: A dictionary containing keyword arguments required to submit a Couchbase restore job.
                Example:
                    restore_options = {
                        'no_of_streams': 4,
                        'multinode_restore': True,
                        'overwrite': True,
                        'destination_instance': 'destination_instance_name',
                        'destination_instance_id': 123,
                        'paths': ['/data/bucket1', '/data/bucket2'],
                        'destination_client_id': 456,
                        'destination_client_name': 'destination_client_name',
                        'client_type': 'Couchbase',
                        'destination_appTypeId': 789,
                        'backupset_name': 'backupset1',
                        'subclient_id': 1011,
                        'restore_items': ['bucket1', 'bucket2'],
                        'accessnodes': ['node1', 'node2']
                    }

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> restore_options = {
            ...     'no_of_streams': 2,
            ...     'overwrite': True,
            ...     'destination_instance': 'CouchbaseInstance2',
            ...     'paths': ['/data/bucket1'],
            ...     'destination_client_name': 'Client2',
            ...     'backupset_name': 'Backupset1',
            ...     'restore_items': ['bucket1'],
            ...     'accessnodes': ['node1']
            ... }
            >>> job = couchbase_instance.restore(restore_options)
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

        distributed_restore_json["stageFreeRestoreOptions"] = {
            "restoreItems": restore_options.get("restore_items")
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