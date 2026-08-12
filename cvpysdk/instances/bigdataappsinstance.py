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
File for operating with Big Data Apps Instance.

BigDataAppsInstance is the only class defined in this file.

BigDataAppsInstance:    Derived class from Instance Base class, representing a
bigdata apps instance, and to perform operations on that instance

BigDataAppsInstance
===================

    __new__()   --  Method to create object based on specific bigdatapps instance type

"""
from ..instance import Instance
from ..exception import SDKException

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class BigDataAppsInstance(Instance):
    """
    Represents an instance of the BigDataApps agent.

    This class is designed to encapsulate the creation and management of a BigDataApps agent instance,
    providing a structured way to associate an agent object with a unique instance name and identifier.

    Key Features:
        - Instantiates a BigDataApps agent instance using agent object, name, and ID
        - Ensures proper initialization and association of instance metadata
        - Inherits from the base Instance class for extended functionality

    #ai-gen-doc
    """
    def __new__(cls, agent_object: 'Agent', instance_name: str, instance_id: int) -> object:
        """Create a new BigDataAppsInstance object based on the cluster type.

        This method is responsible for instantiating the appropriate subclass of BigDataAppsInstance
        depending on the cluster type associated with the provided agent object, instance name, and instance ID.

        Args:
            agent_object: The agent object associated with the BigDataApps instance.
            instance_name: The name of the instance to be created.
            instance_id: The unique identifier for the instance.

        Returns:
            An object representing the BigDataApps instance, which may be a specific subclass
            depending on the cluster type.

        Example:
            >>> instance = BigDataAppsInstance(agent_object, "HadoopCluster01", 101)
            >>> print(f"Created instance: {instance}")
            >>> # The returned object will be of the appropriate subclass for the cluster type

        #ai-gen-doc
        """
        from cvpysdk.instances.splunkinstance import SplunkInstance
        from cvpysdk.instances.bigdataapps.mongodbinstance import MongoDBInstance
        from cvpysdk.instances.bigdataapps.yugabyteinstance import YugabyteInstance
        from cvpysdk.instances.bigdataapps.couchbaseinstance import CouchbaseInstance
        instance_types = {
            16: SplunkInstance,
            17: CouchbaseInstance,
            19: YugabyteInstance,
            8: MongoDBInstance
        }

        commcell_object = agent_object._commcell_object
        instance_service = 'Instance/{0}'.format(instance_id)

        response = commcell_object.request('GET', instance_service)

        if response.json() and "instanceProperties" in response.json():
            properties = response.json()["instanceProperties"][0]
        else:
            raise SDKException('Instance', '105')

        bigdata_apps_cluster_type = properties.get('distributedClusterInstance', {}).get('clusterType', -1)

        if bigdata_apps_cluster_type in instance_types.keys():
            instance_type = instance_types[bigdata_apps_cluster_type]
            return object.__new__(instance_type)

        return object.__new__(cls)
