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
Module for managing discovered cloud resources.

Classes:
    DiscoveredResource:
        Represents a single discovered cloud resource.

        Methods:
            __init__()              - Initialize a DiscoveredResource instance.

        Properties:
            name                    - Get the resource name.
            asset_provider          - Get the asset provider.
            workload_type           - Get the workload type (virtual machine, FileStorage, Database).
            asset_type              - Get the specific asset type (EC2, S3, EKS, DocumentDB, etc.).
            region                  - Get the cloud region.
            resource_group          - Get the resource group.
            size                    - Get the resource size specification.
            protection_status       - Get the Commvault protection status.
            protection_plan         - Get the protection plan name.
            connection              - Get the connection identifier.
            connection_type         - Get the connection type.
            last_discovered_time    - Get the last discovery timestamp.
            tags                    - Get the resource tags.
            last_backup             - Get the last backup timestamp.
            recovery_points         - Get the number of recovery points.

    DiscoveredResources:
        Manager class for handling collections of discovered cloud resources.

        Methods:
            __init__()              - Initialize the DiscoveredResources manager.
            has_resource()          - Check if a resource exists in the collection.
            filter_resources()      - Get discovered resources with optional filtering.
            assign_plan()           - Assign a protection plan to one or more resources.
            refresh()               - Refresh the resources cache by fetching latest data.
            __len__()               - Get the number of resources in the collection.

        Properties:
            resources               - Get the list of all discovered resources.
"""
import json
from typing import Dict, List, Optional, Union, TYPE_CHECKING
from datetime import datetime

from .constants import AssetProvider, WorkloadType, AssetType, AssetCVProtectionStatus, FACET_JSON, RESPONSE_FORMAT, \
    START, ROWS, QUERY, AssetCVProtectedBY, ITEM_STATE, ASSET_SUB_TYPE
from ..exception import SDKException

if TYPE_CHECKING:
    from ..commcell import Commcell


class DiscoveredResource:
    """Represents a single discovered cloud resource.
    
    This class encapsulates all the properties and metadata of a discovered
    cloud resource, including its identification, configuration, and protection status.
    """

    def __init__(
        self,
        name: str,
        asset_provider: AssetProvider,
        workload_type: WorkloadType,
        asset_type: AssetType,
        region: Optional[str] = None,
        resource_group: Optional[str] = None,
        size: Optional[str] = None,
        protection_status: AssetCVProtectionStatus = AssetCVProtectionStatus.NONE,
        protection_plan: Optional[str] = None,
        connection: Optional[str] = None,
        connection_type: Optional[str] = None,
        last_discovered_time: Optional[datetime] = None,
        tags: Optional[Dict[str, str]] = None,
        last_backup: Optional[datetime] = None,
        recovery_points: Optional[int] = None,
        protected_by: Optional[AssetCVProtectedBY] = None,
    ) -> None:
        """Initialize a DiscoveredResource instance.
        
        Args:
            name: The resource name
            asset_provider: The cloud provider type
            workload_type: The type of workload (VM, FileStorage, Database)
            asset_type: Specific asset type (EC2, S3, EKS, DocumentDB, etc.)
            region: The cloud region where resource is located
            resource_group: Resource group or organizational unit
            size: Size specification of the resource
            protection_status: Commvault protection status
            protection_plan: Associated protection plan name
            connection: Connection identifier
            connection_type: Type of connection
            last_discovered_time: When the resource was last discovered
            tags: Resource tags as key-value pairs
            last_backup: Timestamp of last backup
            recovery_points: Number of available recovery points

        Returns:
            None

        Example:
            >>> from datetime import datetime
            >>> resource = DiscoveredResource(
            ...     name="my-ec2-instance",
            ...     asset_provider=AssetProvider.AZURE,
            ...     workload_type=WorkloadType.COMPUTE,
            ...     asset_type=AssetType.AZURE_VM_SCALE_SET,
            ...     region="us-west-2",
            ...     tags={"Environment": "Production"}
            ... )
        """
        self._name = name
        self._asset_provider = asset_provider
        self._workload_type = workload_type
        self._asset_type = asset_type
        self._region = region
        self._resource_group = resource_group
        self._size = size
        self._protection_status = protection_status
        self._protection_plan = protection_plan
        self._connection = connection
        self._connection_type = connection_type
        self._last_discovered_time = last_discovered_time
        self._tags = tags or {}
        self._last_backup = last_backup
        self._recovery_points = recovery_points
        self._protected_by = protected_by


    @property
    def name(self) -> str:
        """Get the resource name.
        
        Returns:
            The resource name
        """
        return self._name

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider.
        
        Returns:
            The AssetProvider enum value
        """
        return self._asset_provider

    @property
    def workload_type(self) -> WorkloadType:
        """Get the workload type (virtual machine, FileStorage, Database).
        
        Returns:
            The WorkloadType enum value
        """
        return self._workload_type

    @property
    def asset_type(self) -> AssetType:
        """Get the specific asset type (EC2, S3, EKS, DocumentDB, etc.).
        
        Returns:
            The AssetType enum value
        """
        return self._asset_type

    @property
    def region(self) -> Optional[str]:
        """Get the cloud region.
        
        Returns:
            The region name or None
        """
        return self._region

    @property
    def resource_group(self) -> Optional[str]:
        """Get the resource group.
        
        Returns:
            The resource group name or None
        """
        return self._resource_group

    @property
    def size(self) -> Optional[str]:
        """Get the resource size specification.
        
        Returns:
            The size specification or None
        """
        return self._size

    @property
    def protection_status(self) -> AssetCVProtectionStatus:
        """Get the Commvault protection status.
        
        Returns:
            The AssetCVProtectionStatus enum value
        """
        return self._protection_status

    @property
    def protection_plan(self) -> Optional[str]:
        """Get the protection plan name.
        
        Returns:
            The protection plan name or None
        """
        return self._protection_plan

    @property
    def connection(self) -> Optional[str]:
        """Get the connection identifier.
        
        Returns:
            The connection ID or None
        """
        return self._connection

    @property
    def connection_type(self) -> Optional[str]:
        """Get the connection type.
        
        Returns:
            The connection type or None
        """
        return self._connection_type

    @property
    def last_discovered_time(self) -> Optional[datetime]:
        """Get the last discovery timestamp.
        
        Returns:
            The last discovered time or None
        """
        return self._last_discovered_time

    @property
    def tags(self) -> Dict[str, str]:
        """Get the resource tags.
        
        Returns:
            Dictionary of tag key-value pairs
        """
        return self._tags.copy()

    @property
    def last_backup(self) -> Optional[datetime]:
        """Get the last backup timestamp.
        
        Returns:
            The last backup time or None
        """
        return self._last_backup

    @property
    def recovery_points(self) -> Optional[int]:
        """Get the number of recovery points.
        
        Returns:
            The number of recovery points or None
        """
        return self._recovery_points

    @property
    def protected_by(self) -> Optional[AssetCVProtectedBY]:
        """Get the entity that protects the resource.

        Returns:
            The AssetCVProtectedBY enum value or None
        """
        return self._protected_by


class DiscoveredResources:
    """Manager class for handling collections of discovered cloud resources.
    
    This class provides methods to manage and query collections of DiscoveredResource
    objects, including resource lookup, filtering, and protection plan assignment.
    """

    def __init__(self, commcell: 'Commcell', asset_provider: AssetProvider) -> None:
        """
        Initialize the DiscoveredResources manager.

        Args:
            commcell: The Commcell object to which this resource manager belongs

        Returns:
            None: This method does not return a value as it is a constructor.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('webconsole_hostname', 'username', 'password')
            >>> discovered_resources = DiscoveredResources(commcell)
        """
        self._commcell = commcell
        self._resources: List[DiscoveredResource] = []
        self._is_loaded = False
        self._cvpysdk_object = self._commcell._cvpysdk_object
        self._services = self._commcell._services
        self._update_response_ = self._commcell._update_response_
        self._asset_provider = asset_provider

    def has_resource(self, resource_name: str,
                     workload_type: WorkloadType,
                     asset_type: AssetType) -> bool:
        """Check if a resource exists in the collection.

        Args:
            resource_name: The name of the resource to check
            asset_provider: The cloud provider type
            workload_type: The type of workload (VM, FileStorage, Database)
            asset_type: Specific asset type (EC2, S3, EKS, DocumentDB, etc.)

        Returns:
            True if resource exists, False otherwise

        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> obj = DiscoveredResources(commcell)
            >>> has_ec2_vm = obj.has_resource("my-ec2-instance", AssetProvider.AWS, WorkloadType.COMPUTE, AssetType.AMAZON_EC2_VIRTUAL_MACHINE)
        """
        raise NotImplementedError("has_resource method is not yet implemented")

    def get_resource(self, resource_name: str,
                     asset_provider: AssetProvider,
                     workload_type: WorkloadType,
                     asset_type: AssetType) -> DiscoveredResource:
        """returns a resource object for the given resource name.

        Args:
            resource_name: The name of the resource to check
            asset_provider: The cloud provider type
            workload_type: The type of workload (VM, FileStorage, Database)
            asset_type: Specific asset type (EC2, S3, EKS, DocumentDB, etc.)

        Returns:
                DiscoveredResource object for the given resource name

        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> obj = DiscoveredResources()
            >>> ec2_resource = obj.get_resource("my-ec2-instance", AssetProvider.AWS, WorkloadType.COMPUTE, AssetType.AMAZON_EC2_VIRTUAL_MACHINE)
        """
        raise NotImplementedError("get_resource method is not yet implemented")

    def filter_resources(
        self, 
        asset_provider: Optional[AssetProvider] = None,
        workload_type: Optional[WorkloadType] = None,
        asset_type: Optional[AssetType] = None,
        protection_status: Optional[AssetCVProtectionStatus] = None
    ) -> List[DiscoveredResource]:
        """Get discovered resources with optional filtering.

        Args:
            asset_provider: Filter by asset provider (optional)
            workload_type: Filter by workload type (optional)
            asset_type: Filter by asset type (optional)
            protection_status: Filter by protection status (optional)

        Returns:
            List of DiscoveredResource objects matching the filters

        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> obj = DiscoveredResources()
            >>> resources = obj.filter_resources(asset_provider=AssetProvider.AWS)
            >>> protected_resources = obj.filter_resources(protection_status=AssetCVProtectionStatus.PROTECTED)
            >>> specific_resources = obj.filter_resources(workload_type=WorkloadType.DATABASE, asset_type=AssetType.RDS)
        """
        if not self._is_loaded:
            self.refresh()

        filtered_resources = []
        for resource in self._resources:
            if asset_provider is not None and resource.asset_provider != asset_provider:
                continue
            if workload_type is not None and resource.workload_type != workload_type:
                continue
            if asset_type is not None and resource.asset_type != asset_type:
                continue
            if protection_status is not None and resource.protection_status != protection_status:
                continue
            filtered_resources.append(resource)

        return filtered_resources

    def assign_plan(self,
                    resources: Union[DiscoveredResource, List[DiscoveredResource]],
                    plan_name: str
                    ) -> bool:
        """Assign a protection plan to one or more resources.

        Args:
            resources: Single resource or list of resources to assign plan to
            plan_name: The protection plan name to assign

        Returns:
            True if plan assignment was successful, False otherwise

        Example:
            >>> # Assign plan to a single resource
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell("webconsole_hostname", "username", "password")
            >>> instance = DiscoveredResources(commcell)
            >>> resource = instance.get_resource("vm-001", AssetProvider.AWS, WorkloadType.COMPUTE, AssetType.AMAZON_EC2_VIRTUAL_MACHINE)
            >>> success = instance.assign_plan(resource, "daily-backup")
            >>> print(success)
            True

            >>> # Assign plan to multiple resources
            >>> resources = [
            ...     DiscoveredResource("vm-001", AssetProvider.AWS, WorkloadType.COMPUTE, AssetType.AMAZON_EC2_VIRTUAL_MACHINE),
            ...     DiscoveredResource("vm-002", AssetProvider.AWS, WorkloadType.COMPUTE, AssetType.AMAZON_EC2_VIRTUAL_MACHINE)
            ... ]
            >>> success = instance.assign_plan(resources, "weekly-backup")
            >>> print(success)
            True

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("assign_plan method is not yet implemented")

    def _get_resources(self) -> List[DiscoveredResource]:
        """Internal method to load resources from the backend.
        
        This is a private method that handles the actual data retrieval
        from the underlying API.

        Returns:
            List of DiscoveredResource objects
        
        Raises:
            SDKException:
                        Response was not success

        Example:
            >>> resources = self._get_resources()
        """
        url = self._services['GET_RESOURCES']
        resources = []
        start = START
        rows = ROWS

        while True:
            payload = {
                "searchParams": [
                    {"key": "q", "value": QUERY},
                    {"key": "wt", "value": RESPONSE_FORMAT},
                    {"key": "start", "value": f"{start}"},
                    {"key": "rows", "value": f"{rows}"},
                    {"key": "fq", "value": ITEM_STATE},
                    {"key": "fq", "value": ASSET_SUB_TYPE},
                    {"key": "fq", "value": f"Provider:{self._asset_provider.value}"},
                    {"key": "json.facet", "value": json.dumps(FACET_JSON)}
                ]
            }

            flag, response = self._cvpysdk_object.make_request('POST', url, payload)
            if flag:
                if response.json():
                    if not response.json().get('errorMessage', None):
                        count = response.json().get('facets', {}).get('count', 0)
                        resources_data = response.json()['response'].get('docs', [])
                        resources.extend([
                            DiscoveredResource(
                                name=resource.get('AssetName'),
                                asset_provider=self._asset_provider,
                                workload_type=WorkloadType(resource.get('WorkloadType')),
                                asset_type=AssetType(resource.get('AssetType')),
                                region=resource.get('AssetRegion'),
                                resource_group=resource.get('AssetGroup'),
                                size=resource.get('AssetSize'),
                                protection_status=AssetCVProtectionStatus(resource.get('ProtectionStatus')),
                                protection_plan=resource.get('ProtectionPlan'),
                                connection=resource.get('Connection'),
                                connection_type=resource.get('ConnectionType'),
                                last_discovered_time=datetime.fromisoformat(
                                    resource.get('LastSyncedAt')) if resource.get('LastSyncedAt') else None,
                                tags=resource.get('EntityTags', {}),
                                last_backup=datetime.fromisoformat(resource.get('LastBackup')) if resource.get(
                                    'LastBackup') else None,
                                recovery_points=resource.get('RecoveryPoints'),
                                protected_by=AssetCVProtectedBY(resource.get('ProtectedBy')[0]) if resource.get(
                                    'ProtectionStatus') == 4 and resource.get('ProtectedBy') else None
                            )
                            for resource in resources_data
                        ])
                        if start + rows >= count:
                            break
                        start += rows
                        rows = min(ROWS, count - start)
                    else:
                        raise SDKException("DISCOVERY", "103")
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))

        return resources

    def refresh(self) -> None:
        """Refresh the resources cache by fetching latest data.

        This method updates the internal resources list with
        the most recent data from the backend.

        Raises:
            SDKException:
                        Response was not success

        Example:
            >>> obj = DiscoveredResources()
            >>> obj.refresh()
        """
        self._resources = self._get_resources()

    def __len__(self) -> int:
        """Get the number of resources in the collection.
        
        Returns:
            The number of resources
        """
        if not self._is_loaded:
            self.refresh()
        return len(self._resources)

    @property
    def all_resources(self) -> List[DiscoveredResource]:
        """Get the list of all discovered resources.
        
        Returns:
            List of DiscoveredResource objects

        Example:
            >>> obj = DiscoveredResources()
            >>> all_resources = obj.resources
            >>> for resource in all_resources:
            ...     print(resource.name)
        """
        if not self._is_loaded:
            self.refresh()
        return list(self._resources)