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
File for operating with the a Big Data Apps Instance.

BigDataAppsInstance is the only class defined in this file.

BigDataAppsInstance:    Derived class from Instance Base class, representing a
bigdata apps instance, and to perform operations on that instance

BigDataAppsInstance
===================

    __new__()   --  Method to create object based on specific bigdatapps instance type

"""
from ..instance import Instance
from ..exception import SDKException

class BigDataAppsInstance(Instance):
    """
    Class for representing an Instance of the BigDataApps agent
    """
    def __new__(cls, agent_object, instance_name, instance_id):
        """
        Method for object creation based on cluster type of BigdataApps

        Args:
            agent_object    (object)    -- Object associated with the agent

            instance_name   (str)       --  Name associated with the instance object

            instance_id     (int)       --  Id associated with the instance object

        Returns:
            object          (obj)       --  Object associated with the BigDataApps instance

        """
        from cvpysdk.instances.splunkinstance import SplunkInstance
        instance_types = {
            16: SplunkInstance
        }

        commcell_object = agent_object._commcell_object
        instance_service = 'Instance/{0}'.format(instance_id)

        response = commcell_object.request('GET', instance_service)

        if response.json() and "instanceProperties" in response.json():
            properties = response.json()["instanceProperties"][0]
        else:
            raise SDKException('Instance', '105')

        bigdata_apps_cluster_type = properties \
            ["distributedClusterInstance"]["clusterType"]

        if bigdata_apps_cluster_type in instance_types.keys():
            instance_type = instance_types[bigdata_apps_cluster_type]
            return object.__new__(instance_type)

        return object.__new__(cls)
