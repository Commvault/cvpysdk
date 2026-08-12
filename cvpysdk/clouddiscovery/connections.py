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
Module for managing cloud discovery connections across different asset providers.

Classes:
    Connection:
        Base class for a cloud discovery connection to a specific asset provider.

        Methods:
            __init__()              - Initialize a Connection instance.
            get_configs()           - Get all configuration name-value pairs for this connection.
            start_discovery()       - Start the discovery process for this connection.
            connection_details()    - Get connection-specific details.

        Properties:
            connection_id           - Get the connection ID for this connection.
            credential_id           - Get the credential ID for this connection.
            credential_name         - Get the credential name for this connection.
            connection_name         - Get the connection name for this connection.
            asset_provider          - Get the asset provider for this connection.

    Connections:
        Base class for managing multiple cloud discovery connections.

        Methods:
            __init__()              - Initialize the Connections manager.
            add_connection()        - Add a new connection.
            delete_connection()     - Delete an existing connection.
            get_connection()        - Get a connection by name.
            has_connection()        - Check if a connection exists.
            refresh()               - Refresh the connections cache.
            add_express_connection() - Add a new express connection.
            _get_all_connections()  - Internal method to retrieve all connections from the backend.

        Properties:
            all_connections         - Get all connections managed by this instance.

    AzureConnection:
        Represents an Azure-specific cloud discovery connection.

        Methods:
            __init__()              - Initialize an AzureConnection instance.
            connection_details()    - Get Azure-specific connection details.

        Properties:
            connection_id           - Get the Azure connection ID.
            credential_id           - Get the credential ID for this connection.
            credential_name         - Get the credential name for this connection.
            connection_name         - Get the connection name for this connection.
            asset_provider          - Get the asset provider for this connection.
            config_type()           - Get the Azure config type.

    AzureConnections:
        Manages multiple Azure cloud discovery connections.

        Methods:
            __init__()              - Initialize the AzureConnections manager.
            add_connection()        - Add a new Azure connection (express or custom).
            delete_connection()     - Delete an existing Azure connection.
            get_connection()        - Get an Azure connection by name.
            has_connection()        - Check if an Azure connection exists.
            refresh()               - Refresh the Azure connections cache.
            _get_all_connections()  - Retrieve all Azure connections from the backend.

        Properties:
            all_connections         - Get all Azure connections managed by this instance.

    AWSConnection:
        Represents an AWS-specific cloud discovery connection.

        Methods:
            __init__()              - Initialize an AWSConnection instance.
            connection_details()    - Get AWS-specific connection details.
            _get_aws_connection_details() - Get AWS-specific connection details.
            _get_aws_org_accounts() - Get all AWS organization accounts as name-value pairs.

        Properties:
            connection_id           - Get the AWS connection ID.
            credential_id           - Get the credential ID for this connection.
            credential_name         - Get the credential name for this connection.
            connection_name         - Get the connection name for this connection.
            asset_provider          - Get the asset provider for this connection.
            accounts                - Get accounts present in the connection.

    AWSConnections:
        Manages multiple AWS cloud discovery connections.

        Methods:
            __init__()              - Initialize the AWSConnections manager.
            add_connection()        - Add a new AWS cloud connection.
            delete_connection()     - Delete an existing AWS connection.
            get_connection()        - Get an AWS connection by name.
            has_connection()        - Check if an AWS connection exists.
            refresh()               - Refresh the AWS connections cache.
            aws_stack_info()        - Get AWS permissions CFT articles for a given account ID; returns List[Dict], cached per account ID.
            _get_all_connections()  - Retrieve all AWS connections from the backend.
            _get_aws_cloud_connections() - Get all AWS cloud connections as name-value pairs.
            _validate_aws_cloud_connection() - Validate AWS cloud connection for the specified account ID.
            _fetch_aws_stack_info() - Fetch the AWS permissions CFT stack info from the API.

        Properties:
            all_connections         - Get all AWS connections managed by this instance.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, TYPE_CHECKING, List, Any
from .constants import AssetProvider, AZURE_CUSTOM, AWS, AZURE, AZURE_EXPRESS, AWS_EXPRESS_CONNECTION_PAYLOAD, \
    AWS_EXPRESS_CONNECTION_PAYLOAD, AZURE_EXPRESS_CONNECTION_PAYLOAD, AWS_CONNECTION_TYPE_ORG, AzureConfigType, \
    AWS_CLOUD_CONNECTION_CRED
from .resources import DiscoveredResource
from ..exception import SDKException

if TYPE_CHECKING:
    from ..commcell import Commcell


class Connection(ABC):
    """Base class for a generic connection."""

    def __init__(self, commcell, credential_name, asset_provider):
        self._commcell = commcell
        self._credential_name = credential_name
        self._asset_provider = asset_provider

    @property
    @abstractmethod
    def connection_id(self) -> Optional[int]:
        """Get the connection ID for this connection."""
        pass

    @property
    @abstractmethod
    def credential_id(self) -> int:
        """Get the credential ID for this connection."""
        pass

    @property
    @abstractmethod
    def credential_name(self) -> str:
        """Get the credential name for this connection."""
        pass

    @property
    @abstractmethod
    def connection_name(self) -> str:
        """Get the connection name for this connection."""
        pass

    @property
    @abstractmethod
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for this connection."""
        pass


class Connections(ABC):
    """Base class for a generic connection."""

    def __init__(self, commcell: 'Commcell', asset_provider: AssetProvider = None) -> None:
        """
        Initialize the Connections manager.
        Args:
            commcell: The Commcell object to which this connection manager belongs
        """
        self._commcell = commcell
        self._asset_provider = asset_provider
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_

    @abstractmethod
    def delete_connection(self, connection_name: str) -> bool:
        """Delete an existing connection."""
        pass

    @abstractmethod
    def get_connection(self, connection_name: str) -> Optional[Connection]:
        """Get a connection by name."""
        pass

    @abstractmethod
    def has_connection(self, connection_name: str) -> bool:
        """Check if a connection exists."""
        pass

    @abstractmethod
    def refresh(self) -> None:
        """Refresh the connections cache."""
        pass

    @property
    @abstractmethod
    def all_connections(self) -> List[Connection]:
        """Get all connections managed by this instance."""
        pass

    @abstractmethod
    def add_connection(self, connection_name: str, connection_type: str,
                       **kwargs) -> Connection:
        """Add a new connection with connection-specific parameters."""
        pass


class AzureConnection(Connection):
    """Azure-specific connection."""

    def __init__(self, commcell, connection_name, connection_id, config_type=None):
        super().__init__(commcell, connection_name, AssetProvider.AZURE)
        self._commcell = commcell
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_
        self._connection_id = connection_id
        self._connection_name = connection_name
        self._credential_id = None
        self._config_type = config_type
        if config_type == AzureConfigType.CUSTOM:
            self._credential_id = self._commcell.credentials.get(connection_name).credential_id

    @property
    def connection_id(self) -> Optional[int]:
        """Get the Azure connection ID.

        Returns:
            The Azure connection ID.
        """
        return self._connection_id

    @property
    def config_type(self) -> Optional[int]:
        """Get the Azure config type.

        Returns:
            The Azure config type.
        """
        return self._config_type

    @property
    def credential_id(self) -> Optional[int]:
        """Get the credential ID for this connection.

        Returns:
            The credential ID, or None if not available for this config type.
        """
        return self._commcell.credentials.get(self._credential_name).credential_id

    @property
    def credential_name(self) -> str:
        """Get the credential name for this connection.

        Returns:
            The credential name.
        """
        return self._credential_name

    @property
    def connection_name(self) -> str:
        """Get the connection name for this connection.

        Returns:
            The connection name.
        """
        return self._connection_name

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for this connection.

        Returns:
            The AssetProvider enum value
        """
        return self._asset_provider


class AzureConnections(Connections):
    """Manages multiple Azure connections."""

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the AzureConnections instance.

        Args:
            commcell: The Commcell object for API operations
        """
        super().__init__(commcell, AssetProvider.AZURE)
        self._commcell = commcell
        self._connections: List[Connection] = []
        self._is_loaded = False
        self._asset_provider = AssetProvider.AZURE
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_
        self.refresh()

    @property
    def all_connections(self) -> list[Connection]:
        """Get all Azure connections.

        Returns:
            List of Azure connections.
        """
        return self._connections

    def get_connection(self, connection_name: str) -> AzureConnection:
        """Get an Azure connection by name.

        Args:
            connection_name (str): The name of the connection to retrieve.

        Returns:
            AzureConnection: The Azure connection object if found.

        Raises:
            SDKException: If no Azure connection exists with the given name.
        """
        for connection in self.all_connections:
            if connection.connection_name.lower() == connection_name.lower():
                return connection
        raise SDKException('Connections', '101', f"No Azure connection exists with the name: {connection_name}")

    def has_connection(self, connection_name: str) -> bool:
        """Check if an Azure connection exists for the given name.

        Args:
            connection_name (str): The name of the connection to check.

        Returns:
            bool: True if the connection exists, False otherwise.
        """
        return any(connection.connection_name.lower() == connection_name.lower() for connection in self.all_connections)

    def delete_connection(self, connection_name: str) -> bool:
        """Delete an existing Azure connection by name.

        Args:
            connection_name (str): The name of the connection to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if not isinstance(connection_name, str):
            raise SDKException('Connections', '101', "Credential name must be a string for Azure.")
        if not self.has_connection(connection_name):
            raise SDKException('Connections', '103')

        connection = self.get_connection(connection_name)
        url = self._services['RETIRE'] % connection.connection_id
        flag, response = self._cvpysdk_object.make_request('DELETE', url=url)
        if flag and response.json() and response.json().get('response', {}).get('errorCode', 0) == 0:
            self.refresh()
            return True
        raise SDKException('Connections', '102')

    def refresh(self) -> None:
        """Refresh the Azure connections cache by fetching the latest data."""
        self._connections = self._get_all_connections()

    def _get_all_connections(self) -> list[Any] | list[AzureConnection]:
        """Get all Azure cloud connections as name-value pairs.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing Azure cloud connection details.
        """
        request = self._services['GET_AZURE_CLOUD_CONNECTIONS']
        flag, response = self._cvpysdk_object.make_request('GET', request)
        if flag:
            if response.json().get('errorCode', 0) == 0:
                cloud_connections = response.json().get('cloudConnections', [])
                if not cloud_connections:
                    return []
                return [
                    AzureConnection(
                        self._commcell,
                        connection.get('displayName'),
                        connection.get('id'),
                        config_type=connection.get('configType')
                    )
                    for connection in cloud_connections
                ]
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_connection(
            self,
            connection_name: str,
            connection_type: str,
            credential_id: int,
            tenant_id: str = None,
            tenant_name: str = None,
            environment: str = "AzureCloud",
            discover_all_subscription: bool = True,
            start_discovery: bool = True,
            subscriptions: Optional[list[dict]] = None
    ) -> Connection:
        """Add a new Azure cloud connection with the specified parameters.

        Args:
            connection_name (str): Unique identifier for the connection.
            connection_type (str): Type of the connection (e.g., "Express", "Custom").
            credential_id (int): Credential ID for the Azure connection.
            tenant_id (str): Azure tenant ID.
            tenant_name (str): Azure tenant name.
            environment (str, optional): Azure environment (default: "AzureCloud").
            discover_all_subscription (bool, optional): Whether to discover all subscriptions (default: True).
            start_discovery (bool, optional): Start discovery job (default: True).
            subscriptions (Optional[list[dict]]): List of dictionaries containing subscription details

        Returns:
            Connection: The newly created Connection object.

        Example:
            >>> instance = AzureConnections(commcell)
            >>> conn = instance.add_connection(
            ...     connection_name="azure_connection_1",
            ...     connection_type="azure",
            ...     credential_id=12345,
            ...     tenant_id="2838672e-50ba-4f26-9a23-5aa12d24e499",
            ...     tenant_name="azureuser1@commvault365.onmicrosoft.com",
            ...     environment="AzureCloud",
            ...     discover_all_subscription=False,
            ...     assign_reader_role=False,
            ...     subscriptions=[{"name": "subscriptionname", "id": "11111111111111"}]
            ... )
            >>> print(conn.connection_id)
            123
        """

        payload = AZURE_EXPRESS_CONNECTION_PAYLOAD.copy()
        payload["name"] = connection_name
        payload["startDiscoveryJob"] = start_discovery
        payload["credentials"]["credentialId"] = credential_id

        payload["cloudSpecificConfiguration"]["azure"]["environment"] = environment
        if discover_all_subscription:
            payload["cloudSpecificConfiguration"]["azure"]["discoverAllSubscription"] = discover_all_subscription
        else:
            if subscriptions is None:
                raise SDKException('Connections', '101',
                                   "subscriptions parameter is required when not discovering all subscriptions.")

            payload["cloudSpecificConfiguration"]["azure"]["subscriptions"] = subscriptions

        if connection_type.lower() == AZURE_EXPRESS.lower():
            if not tenant_id or not tenant_name:
                raise SDKException('Connections', '101',
                                   "tenant_id and tenant_name are required for Express connection.")
            payload["cloudSpecificConfiguration"]["azure"]["tenantId"] = tenant_id
            payload["cloudSpecificConfiguration"]["azure"]["tenantName"] = tenant_name
        elif connection_type.lower() == AZURE_CUSTOM.lower():
            payload["cloudSpecificConfiguration"]["azure"]["isCustomConfig"] = True
        else:
            raise SDKException('Connections', '101',
                               "Invalid connection type specified. Must be 'Express' or 'Custom'.")

        url = self._services['ADD_EXPRESS_CONNECTION']
        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json() and 'id' in response.json():
                connection_id = response.json().get('id', None)
                self.refresh()
                return AzureConnection(self._commcell, connection_name, connection_id)
            else:
                raise SDKException('Connections', '107')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))


# AWS-Specific Classes
class AWSConnection(Connection):
    """AWS-specific connection."""

    def __init__(self, commcell, connection_name, connection_id):
        """Initialize an AWSConnection instance.

        Args:
            commcell: The Commcell object for API operations.
            connection_name (str): Unique display name for the connection.
            connection_id (int): The unique connection ID returned by the API.
        """
        super().__init__(commcell, connection_name, AssetProvider.AWS)
        self._connection_id = connection_id
        self._commcell = commcell
        self._credential_name = AWS_CLOUD_CONNECTION_CRED % connection_name
        self._connection_name = connection_name
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_

    @property
    def connection_id(self) -> Optional[int]:
        """Get the connection ID for this AWS connection.

        Returns:
            The connection ID if available, None otherwise.
        """
        return self._connection_id

    @property
    def credential_id(self) -> int:
        """Get the credential ID for this connection.

        Returns:
            The unique credential identifier
        """
        return self._credential_id

    @property
    def credential_name(self) -> str:
        """Get the credential Name for this connection.

        Returns:
            The credential name
        """
        return self._credential_name

    @property
    def connection_name(self) -> str:
        """Get the connection Name for this connection.

        Returns:
            The credential name
        """
        return self._connection_name

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for this connection.

        Returns:
            The AssetProvider enum value
        """
        return self._asset_provider

    @property
    def accounts(self) -> list:
        """Get accounts present in the connection.

        Returns:
            A list of accounts in the AWS connection.
        """
        if not hasattr(self, '_accounts') or not self._accounts:
            self._accounts = self._get_aws_org_accounts(self._connection_id) or []
        return self._accounts

    @property
    def connection_details(self) -> Dict[str, str]:
        """Get AWS-specific connection details.

        Returns:
            Dictionary containing AWS connection details.

        Raises:
            SDKException: If the response was not successful.

        Example:
            >>> aws_connection = AWSConnection(commcell, "my_conn", 12345)
            >>> details = aws_connection.connection_details
            >>> print(details)
            {'account_id': '123456789012', 'regions': ['us-east-1', 'us-west-2']}
        """
        return self._get_aws_connection_details(self._connection_id)

    def _get_aws_connection_details(self, connection_id) -> Dict[str, str]:
        """Get AWS-specific connection details.

        Args:
            connection_id (int): The connection ID of the AWS connection.

        Returns:
            Dict[str, str]: A dictionary containing AWS connection details.

        Raises:
            SDKException: If the response was not successful.

        Example:
            >>> aws_connection = AWSConnection(commcell)
            >>> details = aws_connection.get_aws_connection_details(12345)
            >>> print(details)
            {'account_id': '123456789012', 'regions': ['us-east-1', 'us-west-2']}
        """
        url = self._services['GET_AWS_CONNECTION_DETAILS'] % connection_id
        flag, response = self._cvpysdk_object.make_request('GET', url=url)
        if flag:
            if response.json():
                if response.json().get('errorCode', 0) == 0:
                    return response.json()
                else:
                    raise SDKException("Connections", "106")
            raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_aws_org_accounts(self, connection_id) -> Any | None:
        """Get all AWS organization accounts as name-value pairs.

            Args:
                connection_id (int): The connection ID of the AWS organization.

            Returns:
                List[Dict[str, str]]: A list of dictionaries containing account details.

            Raises:
                SDKException: If the response was not successful.

            Example:
                >>> aws_connection = AWSConnection(commcell)
                >>> accounts = aws_connection.get_aws_org_accounts(12345)
                >>> for account in accounts:
                ...     print(account['accountId'], account['accountName'])
                123456789012 Account1
                987654321098 Account2
            """
        url = self._services['GET_AWS_ORG_ACCOUNTS'] % connection_id
        flag, response = self._cvpysdk_object.make_request('GET', url=url)
        if flag:
            if response.json():
                self._accounts = response.json().get('accountDetails', [])
                if self._accounts:
                    return self._accounts
            raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))


class AWSConnections(Connections):
    """Manages multiple AWS connections."""

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the AWSConnections instance.

        Args:
            commcell: The Commcell object for API operations
        """
        super().__init__(commcell, AssetProvider.AWS)
        self._commcell = commcell
        self._connections: List[Connection] = []
        self._is_loaded = False
        self._asset_provider = AssetProvider.AWS
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_
        self._aws_stack_info: Optional[List[Dict]] = None    # cached cloudConnectionArticlesList
        self._aws_stack_info_account_id: Optional[str] = None  # account ID used for the cached response
        self.refresh()

    @property
    def all_connections(self) -> list:
        """Get all aws connections.

        Returns:
            List of AWS connections
        """
        self.refresh()
        return self._connections

    def add_connection(self, connection_name: str, account_id: str, connection_type: str,
                       regions: Optional[str] = None, accounts: Optional[list[dict]] = None,
                       discoverAllAccounts: bool = False, start_discovery: bool = True) -> AWSConnection:
        """
        Add a new AWS cloud connection with the specified parameters.

        Args:
            connection_name (str): Unique identifier for the connection.
            account_id (str): AWS account ID.
            connection_type (str): Type of AWS connection.
                Possible values:
                    - "CloudAccountLevel": Connection at the account level.
                    - "OrganizationLevel": Connection at the organization level.
            regions (str): List of AWS regions to include. | "us-east-1,ap-southeast-2"
            accounts (list[dict]): List of AWS accounts for organization-level connections. Defaults to an empty list.
            start_discovery (bool, optional): Start discovery job (default: True).
            discoverAllAccounts (bool): Whether to discover all accounts in the organization. Defaults to False.

        Returns:
            AWSConnection: The created AWS connection object.

        Example:
            connection = aws_connections.add_connection(
                connection_name="MyAWSConnection",
                account_id="123456789012",
                connection_type="CloudAccountLevel",
                regions="us-east-1,us-west-2",
                accounts= [{"accountId": "123456789012", "accountName": "Account1"},
                        {"accountId": "987654321098", "accountName": "Account2"}]
            )
        """
        payload = AWS_EXPRESS_CONNECTION_PAYLOAD.copy()
        if not self._validate_aws_cloud_connection(account_id, connection_type):
            raise SDKException('Connections', '105')
        payload["name"] = connection_name
        payload["startDiscoveryJob"] = start_discovery
        payload["connectionType"] = connection_type
        payload["cloudSpecificConfiguration"]["aws"]["regions"] = regions
        payload["cloudSpecificConfiguration"]["aws"]["iamRoleAccountId"] = account_id
        if connection_type == AWS_CONNECTION_TYPE_ORG:
            payload["cloudSpecificConfiguration"]["aws"]["organizationConfiguration"] = {
                "content": {
                    "discoverAllAccounts": discoverAllAccounts
                }
            }
            if accounts:
                payload["cloudSpecificConfiguration"]["aws"]["organizationConfiguration"]["content"][
                    "accounts"] = accounts

        url = self._services['ADD_EXPRESS_CONNECTION']
        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json() and 'id' in response.json():
                connection_id = response.json().get('id', None)
                self.refresh()
                return AWSConnection(self._commcell, connection_name, connection_id)
            else:
                raise SDKException('Connections', '107')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _validate_aws_cloud_connection(self, account_id: str, connection_type: str) -> bool:
        """Validate AWS cloud connection for the specified account ID.

            Args:
                account_id (str): The AWS account ID to validate.
                connection_type (str): The type of AWS connection.
                    - "CloudAccountLevel" for single account connections.
                    - "OrganizationLevel" for organization-level connections.

            Returns:
                bool: True if the connection is valid, raises an exception otherwise.

            Example:
                >>> aws_connection = AWSConnection(commcell)
                >>> is_valid = aws_connection.validate_aws_cloud_connection("123456789012", "CloudAccountLevel")
                >>> print(is_valid)
                True
            """

        payload = AWS_EXPRESS_CONNECTION_PAYLOAD.copy()
        payload["connectionType"] = connection_type
        payload["cloudSpecificConfiguration"]["aws"]["iamRoleAccountId"] = account_id

        url = self._services['VALIDATE_AWS_CONNECTION']
        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)
        if flag:
            if response.json().get('errorCode', 0) == 0:
                return True
            raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_connection(self, connection_name: str) -> Optional[AWSConnection]:
        """Get an AWS connection by name.

        Args:
            connection_name (str): The name of the connection to retrieve.

        Returns:
            AWSConnection: The AWS connection object if found, None otherwise.
        """
        for connection in self.all_connections:
            if connection.connection_name.lower() == connection_name.lower():
                return connection
        return None

    def has_connection(self, connection_name: str) -> bool:
        """Check if an AWS connection exists for the given name.

        Args:
            connection_name (str): The name of the connection to check.

        Returns:
            bool: True if the connection exists, False otherwise.
        """
        return any(connection.connection_name.lower() == connection_name.lower() for connection in self.all_connections)

    def delete_connection(self, connection_name: str) -> bool:
        """Delete an existing AWS connection by name.

        Args:
            connection_name (str): The name of the connection to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        connection = self.get_connection(connection_name)
        if connection:
            url = self._services['RETIRE'] % connection.connection_id
            flag, response = self._cvpysdk_object.make_request('DELETE', url=url)
            if flag and response.json().get('errorCode', 0) == 0:
                self.refresh()
                return True
            raise SDKException('Response', '102')
        raise SDKException('Response', '103')

    def refresh(self) -> None:
        """Refresh the AWS connections cache by fetching the latest data."""
        self._connections = self._get_all_connections()
        self._commcell.credentials.refresh()

    def _get_aws_cloud_connections(self) -> List[Dict[str, str]]:
        """Get all AWS cloud connections as name-value pairs.

            This method retrieves all AWS cloud connections available in the system.

            Args:
                None

            Returns:
                List[Dict[str, str]]: A list of dictionaries, where each dictionary contains details of an AWS cloud connection.

            Example:
                >>> aws_connection = AWSConnection(commcell)
                >>> connections = aws_connection.get_aws_cloud_connections()
                >>> for conn in connections:
                ...     print(conn['name'], conn['id'])
                AWS_Connection_1 12345
                AWS_Connection_2 67890
            """

        url = self._services['GET_AWS_CLOUD_CONNECTIONS']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)
        if flag:
            if response.json():
                connections = response.json().get('cloudConnections', [])
                if connections:
                    return connections
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_all_connections(self) -> List[AWSConnection]:
        """Retrieve all AWS connections from the backend.

        Returns:
            List[AWSConnection]: A list of AWS connection objects.
        """
        connections = self._get_aws_cloud_connections()
        if not connections:
            return []
        return [
            AWSConnection(
                self._commcell,
                conn.get('name'),
                conn.get('id')
            )
            for conn in connections
        ]

    def aws_stack_info(self, account_id: str) -> List[Dict]:
        """Get the AWS permissions CFT stack info for the given account ID.

        Returns the cached ``cloudConnectionArticlesList`` if already fetched for
        this account ID; otherwise calls the API, extracts the list, and caches it.

        Each article in the list contains:
            - ``cloudConnectionType`` (str): ``"CLOUD_ACCOUNT"`` or ``"ORGANIZATION"``
            - ``iamRoleArn``          (str): Full ARN of the IAM role to create/trust
            - ``externalId``          (str): External ID to embed in the trust policy
            - ``hostedInfrastructureCftUrl`` (str): CloudFormation quick-create URL
            - ``memberAccountArticles`` (dict, optional): Present only for ORGANIZATION type

        Args:
            account_id (str): The AWS account ID (12-digit) to query.

        Returns:
            List[Dict]: The ``cloudConnectionArticlesList`` from the PermissionsCFT API response.

        Raises:
            SDKException: If the API call fails, returns an unexpected response,
                          or the ``cloudConnectionArticlesList`` key is missing.

        Example:
            >>> aws_connections = AWSConnections(commcell)
            >>> articles = aws_connections.aws_stack_info('123456789012')
            >>> for article in articles:
            ...     print(article['cloudConnectionType'], article['externalId'])
            CLOUD_ACCOUNT 800AF153AAEBB9B26F818A81A0324278E037C77DB91D478A9C181AE6B4161861
            ORGANIZATION  800AF153AAEBB9B26F818A81A0324278E037C77DB91D478A9C181AE6B4161861
        """
        # Return cached value when the same account ID is requested again
        if self._aws_stack_info is not None and self._aws_stack_info_account_id == account_id:
            return self._aws_stack_info

        self._aws_stack_info = self._fetch_aws_stack_info(account_id)
        self._aws_stack_info_account_id = account_id
        return self._aws_stack_info

    def _fetch_aws_stack_info(self, aws_account_id: str) -> List[Dict]:
        """Fetch the AWS permissions CFT stack info from the API.

        Calls ``GET v4/Cloud/AWS/ExpressConfig/QuickCreateLink/PermissionsCFT?iamRoleAccountId={awsAccountId}``
        and returns the raw JSON response.

        Args:
            aws_account_id (str): The AWS account ID (12-digit) to query.

        Returns:
            List[Dict]: The ``cloudConnectionArticlesList`` from the PermissionsCFT API response.

        Raises:
            SDKException: If the API call fails or returns an unexpected response.

        Example:
            >>> aws_connections = AWSConnections(commcell)
            >>> info = aws_connections._fetch_aws_stack_info('123456789012')
            >>> print(info['cloudConnectionArticlesList'][0]['externalId'])
            800AF153AAEBB9B26F818A81A0324278E037C77DB91D478A9C181AE6B4161861
        """
        url = self._services['GET_AWS_PERMISSIONS_CFT'] % aws_account_id
        flag, response = self._cvpysdk_object.make_request('GET', url=url)
        if flag:
            if response.json():
                articles = response.json().get('cloudConnectionArticlesList')
                if articles is None:
                    raise SDKException('Connections', '108')
                return articles
            raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

