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
        Module for operating on a Big Data Apps Subclient

        BigDataAppsSubclient:

            __init__()                  --  Just inializes all properties related to its super class

            set_data_access_nodes(data_access_nodes) -- adds the passed json object as data access
                                                        nodes for this subclient.

"""

from __future__ import unicode_literals
from ..subclients.fssubclient import FileSystemSubclient
from ..exception import SDKException


class BigDataAppsSubclient(FileSystemSubclient):
    """
        Derived class from FileSystemSubclient. Can perform fs subclient operations.
    """
    def __new__(cls, backupset_object, subclient_name, subclient_id=None):
        """
        Object creation function for BigDataAppsSubclient which returns appropiate
        sub class object based on cluster type

        Args:
            backupset_object    (obj)   --  Backupset object associated with the
            subclient

            subclient_name      (str)   --  Subclient name

            subclient_id        (int)   --  Subclient Id

        Returns:
            object              (obj)   --  Object associated with the Bigdatapps subclient

        """
        from ..subclients.splunksubclient import SplunkSubclient
        from ..subclients.index_server_subclient import IndexServerSubclient
        cluster_types = {
            16: SplunkSubclient,
            6: IndexServerSubclient
        }

        bigdata_apps_cluster_type = backupset_object._instance_object.properties. \
            get('distributedClusterInstance', {}).get('clusterType', -1)

        if bigdata_apps_cluster_type in cluster_types.keys():
            cluster_type = cluster_types[bigdata_apps_cluster_type]
            return object.__new__(cluster_type)

        return object.__new__(cls)

    def set_data_access_nodes(self, data_access_nodes):
        """
            Sets the Data Access Nodes for the distributed apps subclient.
            Args :

                data_access_nodes (list) : Sets the list of client nodes passed as
                                            data access node for this distributed apps
                                            subclient

            Raise SDK Exception :

                If unable to set data access nodes property of the subclient.

        """

        data_access_nodes_client_json = []
        for access_node in data_access_nodes:
            data_access_nodes_client_json.append({"clientName": access_node})

        data_access_nodes_json = {
            "dataAccessNodes": data_access_nodes_client_json
        }

        request_json = {
            "subClientProperties": {
                "dfsSubclientProp": {
                    "distributedDataAccessNodes": data_access_nodes_json
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._SUBCLIENT, request_json)

        output = self._process_update_response(flag, response)

        if output[0]:
            return

        o_str = 'Failed to update properties of subclient\nError: "{0}"'
        raise SDKException('Subclient', '102', o_str.format(output[2]))
