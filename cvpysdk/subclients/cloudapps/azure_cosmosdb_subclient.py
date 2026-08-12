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

"""File for operating on a Azure CosmosDB Subclient.


AzureCosmosDBSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                        Azure Cosmos DB subclient(Azure CosmosDB Cassandra API, ..), and
                        to perform operations on that subclient

AzureCosmosDBSubclient:

    _get_subclient_properties()         --  gets the properties of Cloud Database Subclient

"""
from ..casubclient import CloudAppsSubclient
from ...exception import SDKException


class AzureCosmosDBSubclient(CloudAppsSubclient):
    """
    Represents an Azure Cosmos DB subclient for cloud application management.

    This class is derived from the Subclient Base class and is specifically designed
    to handle operations related to Azure Cosmos DB subclients. It provides mechanisms
    to retrieve and manage subclient properties, facilitating integration and management
    within cloud environments.

    Key Features:
        - Specialized for Azure Cosmos DB subclient operations
        - Inherits core functionality from CloudAppsSubclient
        - Provides method to retrieve subclient properties

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> dict:
        """Retrieve the properties related to the Cloud Database subclient.

        Returns:
            dict: A dictionary containing the subclient properties for the Azure Cosmos DB subclient.

        Example:
            >>> subclient = AzureCosmosDBSubclient()
            >>> properties = subclient._get_subclient_properties()
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2'}
        #ai-gen-doc
        """

        super(AzureCosmosDBSubclient, self)._get_subclient_properties()
