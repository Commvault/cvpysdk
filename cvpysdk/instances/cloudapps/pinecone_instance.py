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

"""File for operating on a Pinecone Instance.

PineConeInstance is the only class defined in this file.

PineConeInstance: Derived class from CloudAppsInstance Base class, representing a
Pinecone vector database instance, and to perform operations on that instance

PineConeInstance:

    __init__()                      --  Initializes Pinecone instance object with associated
                                        agent_object, instance name and instance id

    _get_instance_properties()      --  Instance class method overwritten to add cloud apps
                                        instance properties as well

PineConeInstance Attributes:

    instance_type           --  Returns the Pinecone instance type

    credential_name         --  Returns the credential name used for Pinecone authentication

    staging_path            --  Returns the instance staging path

    staging_credential      --  Returns the staging credential name

    account_name            --  Returns the Pinecone account name

    plan_name               --  Returns the plan name associated with this instance

    proxy_client            --  Returns the proxy client name for this instance

"""
from __future__ import unicode_literals
from typing import Optional

from ...exception import SDKException
from ..cainstance import CloudAppsInstance


class PineConeInstance(CloudAppsInstance):
    """
    Represents an instance of the Pinecone vector database service.

    This class provides an interface for managing and interacting with a Pinecone instance.
    It exposes properties to access key attributes such as the instance type, credentials,
    staging paths, account information, and associated plans. Internal methods allow retrieval
    of instance-specific properties for configuration and management.

    Key Features:
        - Access to the type of Pinecone instance via `instance_type`
        - Retrieve authentication credentials with `credential_name`
        - Obtain the staging path for data operations using `staging_path`
        - Access staging credentials via `staging_credential`
        - Retrieve the Pinecone account name with `account_name`
        - Get the associated plan name with `plan_name`
        - Access the proxy client for communication with the Pinecone instance using `proxy_client`
        - Internal method for fetching and updating instance properties

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new PineConeInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Pinecone instance.
            instance_name: The name of the Pinecone instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, 
                        it will be determined automatically.

        Example:
            >>> agent = Agent(commcell_object, 'cloud apps')
            >>> pinecone_instance = PineConeInstance(agent, 'MyPineconeInstance')
            >>> # Optionally, provide an instance ID
            >>> pinecone_instance_with_id = PineConeInstance(agent, 'MyPineconeInstance', '12345')

        #ai-gen-doc
        """
        self._ca_instance_type = None
        self._credential_name = None
        self._staging_path = None
        self._staging_credential = None
        self._account_name = None
        self._plan_name = None
        self._proxy_client = None

        super(PineConeInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the current Pinecone instance.

        This method fetches the latest properties for the instance and updates the internal state.
        It extracts Pinecone-specific configuration including credentials, staging paths, account
        information, and plan details from the cloud apps instance properties.

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> instance = PineConeInstance(agent_object, 'PineconeInstance_123')
            >>> instance._get_instance_properties()
            >>> # The instance properties are now updated internally
            >>> print(f"Instance type: {instance.instance_type}")
            >>> print(f"Staging path: {instance.staging_path}")

        #ai-gen-doc
        """
        super(PineConeInstance, self)._get_instance_properties()

        # Reset properties
        self._ca_instance_type = None
        self._credential_name = None
        self._staging_path = None
        self._staging_credential = None
        self._account_name = None
        self._plan_name = None
        self._proxy_client = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance.get('instanceType')

            # Extract general cloud properties
            if 'generalCloudProperties' in cloud_apps_instance:
                general_props = cloud_apps_instance['generalCloudProperties']
                
                # Get proxy client information
                if 'proxyServers' in general_props:
                    proxy_servers = general_props.get('proxyServers', [])
                    if proxy_servers:
                        self._proxy_client = proxy_servers[0].get('clientName')

            # Extract custom properties for Pinecone
            if 'customProperties' in cloud_apps_instance:
                custom_props = cloud_apps_instance.get('customProperties', {})
                name_values = custom_props.get('nameValues', [])
                
                for prop in name_values:
                    if prop.get('name') == 'WorkloadInstanceCustomProperties':
                        import json
                        try:
                            custom_data = json.loads(prop.get('value', '{}'))
                            self._staging_path = custom_data.get('stagingPath')
                            self._staging_credential = custom_data.get('stagingCredentialName')
                        except (json.JSONDecodeError, ValueError):
                            pass

        # Extract credential information
        if 'securityAssociations' in self._properties:
            security_assocs = self._properties.get('securityAssociations', {})
            if 'associations' in security_assocs:
                associations = security_assocs.get('associations', [])
                if associations:
                    credentials = associations[0].get('userOrGroup', {})
                    self._credential_name = credentials.get('userName')

        # Extract plan information
        if 'planEntity' in self._properties:
            plan = self._properties.get('planEntity', {})
            self._plan_name = plan.get('planName')

        # Extract account name from instance properties
        if 'instance' in self._properties:
            instance_info = self._properties.get('instance', {})
            self._account_name = instance_info.get('clientName')

    @property
    def instance_type(self) -> Optional[int]:
        """Get the Pinecone instance type identifier.

        Returns:
            The Pinecone instance type as an integer, or None if not set.

        Example:
            >>> pinecone_instance = PineConeInstance(agent, 'MyPinecone')
            >>> instance_type = pinecone_instance.instance_type
            >>> print(f"Instance type: {instance_type}")

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def credential_name(self) -> Optional[str]:
        """Get the credential name used for Pinecone authentication.

        Returns:
            The credential name as a string, or None if not configured.

        Example:
            >>> pinecone_instance = PineConeInstance(agent, 'MyPinecone')
            >>> cred_name = pinecone_instance.credential_name
            >>> print(f"Credential: {cred_name}")

        #ai-gen-doc
        """
        return self._credential_name

    @property
    def staging_path(self) -> Optional[str]:
        """Get the staging path for Pinecone data operations.

        Returns:
            The staging path as a string, or None if not configured.

        Example:
            >>> pinecone_instance = PineConeInstance(agent, 'MyPinecone')
            >>> path = pinecone_instance.staging_path
            >>> print(f"Staging path: {path}")

        #ai-gen-doc
        """
        return self._staging_path

    @property
    def staging_credential(self) -> Optional[str]:
        """Get the staging credential name.

        Returns:
            The staging credential name as a string, or None if not configured.

        Example:
            >>> pinecone_instance = PineConeInstance(agent, 'MyPinecone')
            >>> staging_cred = pinecone_instance.staging_credential
            >>> print(f"Staging credential: {staging_cred}")

        #ai-gen-doc
        """
        return self._staging_credential

    @property
    def account_name(self) -> Optional[str]:
        """Get the Pinecone account name.

        Returns:
            The account name as a string, or None if not configured.

        Example:
            >>> pinecone_instance = PineConeInstance(agent, 'MyPinecone')
            >>> account = pinecone_instance.account_name
            >>> print(f"Account: {account}")

        #ai-gen-doc
        """
        return self._account_name

    @property
    def plan_name(self) -> Optional[str]:
        """Get the plan name associated with this Pinecone instance.

        Returns:
            The plan name as a string, or None if not configured.

        Example:
            >>> pinecone_instance = PineConeInstance(agent, 'MyPinecone')
            >>> plan = pinecone_instance.plan_name
            >>> print(f"Plan: {plan}")

        #ai-gen-doc
        """
        return self._plan_name

    @property
    def proxy_client(self) -> Optional[str]:
        """Get the proxy client name for this Pinecone instance.

        Returns:
            The proxy client name as a string, or None if not configured.

        Example:
            >>> pinecone_instance = PineConeInstance(agent, 'MyPinecone')
            >>> proxy = pinecone_instance.proxy_client
            >>> print(f"Proxy client: {proxy}")

        #ai-gen-doc
        """
        return self._proxy_client
