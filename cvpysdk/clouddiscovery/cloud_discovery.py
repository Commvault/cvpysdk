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
Module for cloud discovery operations across different asset providers.

Classes:
    CloudDiscovery:
        Base class for cloud discovery operations.

        Methods:
            __init__()          - Initialize the CloudDiscovery instance.
            estimate_cost()     - Estimate the cost of discovered resources and protection plans.

        Properties:
            asset_provider      - Get the asset provider for this cloud discovery instance.
            connections         - Get the connections manager for this cloud discovery instance.
            resources           - Get the resources manager for this cloud discovery instance.
            credentials         - Get the credentials for this cloud discovery instance.

    AzureDiscovery:
        Azure-specific cloud discovery implementation.

        Methods:
            __init__()          - Initialize the AzureDiscovery instance.
            estimate_cost()     - Estimate the cost of discovered resources and protection plans.

        Properties:
            asset_provider      - Get the asset provider for this Azure discovery instance.

    AWSDiscovery:
        AWS-specific cloud discovery implementation.

        Methods:
            __init__()          - Initialize the AWSDiscovery instance.
            estimate_cost()     - Estimate the cost of discovered resources and protection plans.

        Properties:
            asset_provider      - Get the asset provider for this AWS discovery instance.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TYPE_CHECKING
from .constants import AssetProvider
from .connections import Connections, Connection, AWSConnections, AzureConnections
from .resources import DiscoveredResources
from ..exception import SDKException

if TYPE_CHECKING:
    from ..commcell import Commcell
    from ..credential_manager import Credentials


class CloudDiscovery(ABC):
    """Base class for cloud discovery operations.
    
    This abstract base class provides the common interface for cloud discovery
    operations across different asset providers. It manages connections, resources,
    and credential management for cloud environments.
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the CloudDiscovery instance.
        
        Args:
            commcell: The Commcell object for API operations
        """
        self._commcell = commcell
        if self.asset_provider == AssetProvider.AWS:
            self._connections = AWSConnections(commcell)
        elif self.asset_provider == AssetProvider.AZURE:
            self._connections = AzureConnections(commcell)
        else:
            raise SDKException('Discovery', '104')
        self._resources = DiscoveredResources(commcell, self.asset_provider)
        self._credentials = commcell.credentials
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_

    @property
    @abstractmethod
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for this cloud discovery instance.
        
        Returns:
            The AssetProvider enum value
        """
        pass

    @property
    def connections(self) -> Connections:
        """Get the connections manager for this cloud discovery instance.
        
        Returns:
            The Connections manager object
        """
        return self._connections

    @property
    def resources(self) -> DiscoveredResources:
        """Get the resources manager for this cloud discovery instance.
        
        Returns:
            The DiscoveredResources manager object
        """
        return self._resources

    @property
    def credentials(self) -> 'Credentials':
        """Get the credentials for this cloud discovery instance.
        
        Returns:
            The credential manager object or None
        """
        return self._credentials

    def start_discovery(self) -> int:
        """Start the discovery process for this connection.

        Returns:
            int: discovery job id

        Raises:
            SDKException:
                        Response was not success
        """
        url = self._services['START_DISCOVERY']
        flag, response = self._cvpysdk_object.make_request('POST', url=url)
        if flag:
            if response.json():
                errorcode = response.json().get('errorCode', 0)
                if errorcode == 0:
                    get_jobId = self.get_discovery_job()
                    return get_jobId
                else:
                    raise SDKException('Discovery', '101')
            raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_discovery_job(self) -> int:
        """
            Retrieve the discovery job ID for the given credential.

            Returns:
                int: The job ID of the discovery process.

            Raises:
                SDKException: If the job ID is not found or the response is invalid.
        """
        url = self._services['GET_DISCOVERY_JOB']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)
        if flag:
            if response.json():
                if response.json().get('errorCode', 0) == 0:
                    job_id = response.json().get('jobId', None)
                    if job_id:
                        return job_id
                    else:
                        raise SDKException("Discovery", "101")
            raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @abstractmethod
    def estimate_cost(self) -> Dict[str, Any]:
        """Estimate the cost of discovered resources and protection plans.

        This method should be implemented by each cloud provider to provide
        cost estimation specific to their pricing models and resource types.

        Args:
            None

        Returns:
            Dictionary containing cost estimation details. Uses Any for values
            to accommodate varying cost structures across different cloud providers
            (numeric costs, nested dictionaries, lists of cost breakdowns, etc.)

        Raises:
            NotImplementedError: Must be implemented by derived classes
        """
        pass


class AzureDiscovery(CloudDiscovery):
    """Azure cloud discovery implementation.
    
    This class provides Azure-specific cloud discovery operations including
    resource discovery, connection management, and cost estimation using
    Azure pricing models.
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the AzureDiscovery instance.
        
        Args:
            commcell: The Commcell object for API operations
        """
        super().__init__(commcell)

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for Azure discovery.
        
        Returns:
            AssetProvider.AZURE
        """
        return AssetProvider.AZURE

    def estimate_cost(self) -> Dict[str, Any]:
        """Estimate the cost of Azure resources and protection plans.

        Provides cost estimation for Azure resources including virtual machines,
        storage accounts, databases, and associated Commvault protection costs.

        Returns:
            Dictionary containing Azure cost estimation details including:
                - Resource costs by type
                - Protection plan costs
                - Total estimated monthly cost
                - Cost breakdown by region

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('webconsole', 'user', 'password')
            >>> azure_manager = AzureDiscovery(commcell)
            >>> cost_estimate = azure_manager.estimate_cost()
            >>> print(f"Total monthly cost: ${cost_estimate['total_monthly_cost']}")
            Total monthly cost: $1250.00
            >>> print(f"VM costs: ${cost_estimate['vm_costs']}")
            VM costs: $800.00

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("Azure cost estimation is not yet implemented")


class AWSDiscovery(CloudDiscovery):
    """AWS cloud discovery implementation.
    
    This class provides AWS-specific cloud discovery operations including
    resource discovery, connection management, and cost estimation using
    AWS pricing models.
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the AWSDiscovery instance.
        
        Args:
            commcell: The Commcell object for API operations
        """
        super().__init__(commcell)

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for AWS discovery.
        
        Returns:
            AssetProvider.AWS
        """
        return AssetProvider.AWS

    def estimate_cost(self) -> Dict[str, Any]:
        """Estimate the cost of AWS resources and protection plans.

        Provides cost estimation for AWS resources including EC2 instances,
        S3 storage, RDS databases, and associated Commvault protection costs.

        Returns:
            Dictionary containing AWS cost estimation details including:
                - Resource costs by type
                - Protection plan costs
                - Total estimated monthly cost
                - Cost breakdown by region

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('webconsole', 'user', 'password')
            >>> aws_manager = AWSDiscovery(commcell)
            >>> cost_estimate = aws_manager.estimate_cost()
            >>> print(f"Total monthly cost: ${cost_estimate['total_monthly_cost']}")
            Total monthly cost: $1250.50

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("AWS cost estimation is not yet implemented")
