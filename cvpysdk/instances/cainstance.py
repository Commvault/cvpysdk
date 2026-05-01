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

"""File for operating on Cloud Apps Instance.

CloudAppsInstance is the only class defined in this file.

CloudAppsInstance:  Derived class from Instance Base class, representing a
cloud apps instance, and to perform operations on that instance

**Note:** GoogleInstance class is used for OneDrive as well.

CloudAppsInstance:

    __new__()   --  Method to create object based on specific cloud apps instance type


Usage
=====

To add a new Instance for Cloud Apps agent, please follow these steps:

    1. Add the module for the new instance type under the location:
        **/cvpysdk/instances/cloudapps**,
        with the module name **<new instance type>_instance.py**
        (e.g. "google_instance.py", "salesforce_instance.py")

    #. Create a class for your instance type and inherit the CloudAppsInstance class.

    #. Add the import statement inside the __new__ method.
        **NOTE:** If you add the import statement at the top,
        it'll cause cyclic import, and the call will fail

    #. After adding the import statement:
        - In the **instance_type** dict
            - Add the cloud apps instance type as the key, and the class as its value

"""

from __future__ import unicode_literals

from ..instance import Instance
from ..exception import SDKException

from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class CloudAppsInstance(Instance):
    """
    Represents an instance of the Cloud Apps agent.

    This class is responsible for encapsulating the details of a Cloud Apps agent instance,
    including its association with a specific agent object, instance name, and instance ID.
    It provides a specialized constructor for creating new Cloud Apps agent instances.

    Common cloud apps properties (instance type, proxy client, credential, plan, account)
    are parsed here so that derived classes only need to handle workload-specific properties.

    #ai-gen-doc
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize a CloudAppsInstance object.

        Args:
            agent_object: The agent object associated with this instance.
            instance_name: The name of the cloud application instance.
            instance_id: Optional unique identifier for the instance.
        """
        self._ca_instance_type = None
        self._proxy_client = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        super(CloudAppsInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self):
        """Retrieve and parse common cloud apps instance properties.

        Extracts instance type, proxy client, credential, plan, and account
        from the instance properties response. Derived classes should call
        super()._get_instance_properties() and then parse workload-specific
        properties (e.g. custom properties).
        """
        super(CloudAppsInstance, self)._get_instance_properties()

        self._ca_instance_type = None
        self._proxy_client = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance.get('instanceType')

            if 'generalCloudProperties' in cloud_apps_instance:
                general_props = cloud_apps_instance['generalCloudProperties']

                # Proxy client
                proxy_servers = general_props.get('proxyServers', [])
                if proxy_servers:
                    self._proxy_client = proxy_servers[0].get('clientName')

                # Credential
                if 'credentials' in general_props:
                    creds = general_props['credentials']
                    self._credential_name = creds.get('credentialName')
                    self._credential_id = creds.get('credentialId')

        # Plan
        plan = self._properties.get('planEntity', {})
        self._plan_name = plan.get('planName')

        # Account name (client name)
        instance_info = self._properties.get('instance', {})
        self._account_name = instance_info.get('clientName')

    @property
    def ca_instance_type(self):
        """Returns the cloud apps instance type."""
        return self._ca_instance_type

    @property
    def proxy_client(self) -> Optional[str]:
        """Returns the proxy client name for this instance."""
        return self._proxy_client

    @property
    def credential_name(self) -> Optional[str]:
        """Returns the credential name used for authentication."""
        return self._credential_name

    @property
    def credential_id(self) -> Optional[int]:
        """Returns the credential ID used for authentication."""
        return self._credential_id

    @property
    def plan_name(self) -> Optional[str]:
        """Returns the plan name associated with this instance."""
        return self._plan_name

    @property
    def account_name(self) -> Optional[str]:
        """Returns the account name (client name) for this instance."""
        return self._account_name

    def __new__(cls, agent_object: 'Agent', instance_name: str, instance_id: int) -> object:
        """Create and return a new instance of the CloudAppsInstance class.

        Args:
            agent_object: The agent object associated with this instance.
            instance_name: The name of the cloud application instance.
            instance_id: The unique identifier for the instance.

        Returns:
            A new CloudAppsInstance object.

        Example:
            >>> instance = CloudAppsInstance(agent_object, "MyCloudApp", 101)
            >>> print(instance)
            <CloudAppsInstance object at 0x...>

        #ai-gen-doc
        """
        from .cloudapps.google_instance import GoogleInstance
        from .cloudapps.salesforce_instance import SalesforceInstance
        from .cloudapps.cloud_storage_instance import CloudStorageInstance
        from .cloudapps.amazon_instance import AmazonRedshiftInstance
        from .cloudapps.amazon_instance import AmazonDocumentDBInstance
        from .cloudapps.amazon_instance import AmazonRDSInstance
        from .cloudapps.amazon_instance import AmazonDynamoDBInstance
        from .cloudapps.dynamics365_instance import MSDynamics365Instance
        from .cloudapps.teams_instance import TeamsInstance
        from .cloudapps.spanner_instance import GoogleSpannerInstance
        from .cloudapps.onedrive_instance import OneDriveInstance
        from .cloudapps.azure_cosmosdb_instance import AzureCosmosDBInstance
        from .cloudapps.powerbi_instance import PowerBIInstance
        from .cloudapps.cloud_database_instance import CloudDatabaseInstance
        from .cloudapps.pinecone_instance import PineConeInstance
        from .cloudapps.snowflake_instance import SnowflakeInstance

        instance_type = {
            1: GoogleInstance,
            2: GoogleInstance,
            3: SalesforceInstance,
            4: AmazonRDSInstance,  # Amazon RDS Instance
            5: CloudStorageInstance,  # AmazonS3 Instance
            6: CloudStorageInstance,  # AzureBlob Instance
            7: OneDriveInstance,  # OneDrive Instance
            14: CloudStorageInstance,  # OracleCloud Instance
            15: CloudStorageInstance,  # Openstack Instance
            20: CloudStorageInstance,  # Google Cloud Instance
            21: CloudStorageInstance,  # azure data lake gen2
            26: AmazonRedshiftInstance,  # Amazon Redshift
            27: AmazonDocumentDBInstance,  # Amazon Document DB
            25: CloudStorageInstance,  # AliBaba
            24: CloudStorageInstance,  # IBM
            22: AmazonDynamoDBInstance,  # Amazon DynamoDB
            35: MSDynamics365Instance,  # MS Dynamics 365 Instance
            36: TeamsInstance,  # Office 365 Teams
            37: GoogleSpannerInstance,  # Google Cloud Spanner Instance
            40: CloudDatabaseInstance,  # MongoDB Atlas
            44: AzureCosmosDBInstance,  # Azure Cosmos DB Cloud Apps Instance
            51: AzureCosmosDBInstance,   # Azure Cosmos DB MongoDBAPI Instance
            56: CloudStorageInstance,  # S3 Compatible Instance
            58: PineConeInstance,  # PineCone Instance
            60: PowerBIInstance,     # Power Platform PowerBi Instance
            61: SnowflakeInstance   # Snowflake Instance
        }

        commcell_object = agent_object._commcell_object
        instance_service = 'Instance/{0}'.format(instance_id)

        response = commcell_object.request('GET', instance_service)

        if response.json() and "instanceProperties" in response.json():
            properties = response.json()["instanceProperties"][0]
        else:
            raise SDKException('Instance', '105')

        cloud_apps_instance_type = properties['cloudAppsInstance']['instanceType']

        return object.__new__(instance_type[cloud_apps_instance_type])
