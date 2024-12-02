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
    """ Derived class from Subclient Base class, representing a Azure Cosmos DB subclient,
            and to perform operations on that subclient. """

    def _get_subclient_properties(self):
        """ Gets the subclient related properties of Cloud Database subclient. """

        super(AzureCosmosDBSubclient, self)._get_subclient_properties()


