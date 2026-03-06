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

"""Main file for performing operations on scale targets configured in the Commserv.

`ScaleTargets`, 'ScaleTargetType' and `ScaleTarget` are 3 classes defined in this file.

ScaleTargets:    Class for representing all the Scale Targets configured in the Commserv.

ScaleTarget:     Class for representing a single Scale Target in the Commcell.

ScaleTargetType: Enum class for representing different types of scale targets.


ScaleTargets:

    __init__(commcell_object)           --  initialise object of the ScaleTargets class

    _response_not_success()             --  parses through the exception response, and raises SDKException

    refresh()                           --  refresh the scale targets associated with the commcell

    get()                               --  Returns an instance of ScaleTarget class for the given scale target name

    get_properties()                    --  Returns the properties for the given scale target name

    _get_all_scale_targets()            --  Returns dict consisting all scale targets associated with commcell

    _get_scale_target_details_from_response()  --  parses scale target details from API response

    has()                               --  Checks whether given scale target exists in commcell or not

    add()                               --  Adds a new scale target to the commcell

    delete()                            --  Deletes a scale target from the commcell


ScaleTarget:

    __init__()                          --  initialize an object of ScaleTarget Class with the given scale target
                                                name and associated to the commcell

    refresh()                           --  refresh the properties of the scale target

    _get_scale_target_properties()      --  Gets all the details of associated scale target

    edit()                              --  Edit specific properties of the scale target

    has_region()                        --  Checks if a specific region is configured in the scale target or not


ScaleTarget Attributes
-----------------

    **scale_target_id**     --  returns the scale target id

    **scale_target_name**   --  returns the name of the scale target

    **description**         --  returns the description of the scale target

    **type**                --  returns the type of the scale target

    **max_computes_spawned** --  returns the max computes that can be spawned

    **use_public_ips**      --  returns whether public IPs are used

    **auth_type**           --  returns the authentication type

    **compute_tags**        --  returns the compute tags

    **azure_target_details** --  returns the Azure-specific target details

    **access_nodes**        --  returns the access nodes list

    **credential_entity**   --  returns the credential entity details

    **region_specific_info_list** --  returns the list of region-specific information for the scale target

"""
from enum import Enum
from .exception import SDKException


class ScaleTargetType(Enum):
    """Enum for Scale Target types."""
    NONE = 0
    AZURE_VM = 1
    AMAZON_VM = 2
    GCP_VM = 3
    AZURE_KEDA = 4


class ScaleTargets(object):
    """
    Manages and represents all Scale Targets within a CommCell environment.

    This class provides an interface for interacting with Scale Target clients,
    retrieving their properties, and managing their lifecycle within the CommCell.
    It supports operations such as fetching all available Scale Targets, checking
    for the existence of specific targets, refreshing the target list, and obtaining
    detailed properties for individual targets.

    Key Features:
        - Initialization with a CommCell object for context
        - Retrieve properties of a specific Scale Target
        - Fetch all Scale Targets present in the CommCell
        - Parse scale target information from API responses
        - Refresh the list of Scale Targets to reflect current state
        - Get a Scale Target by name
        - Check if a specific Scale Target exists
        - Internal response validation for API interactions

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize a new instance of the ScaleTargets class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> scale_targets = ScaleTargets(commcell)
            >>> print("ScaleTargets instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._scale_targets = None
        self._api_get_scale_targets = self._services['GET_SCALE_TARGETS']
        self.refresh()

    def _response_not_success(self, response: object) -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object, typically 
        returned from an API request using the `requests` Python package. If the response 
        status code is not 200, an exception is raised to indicate the request was not successful.

        Args:
            response: The response object received from an API request (e.g., a `requests.Response` instance).

        Example:
            >>> response = requests.get('https://api.example.com/data')
            >>> scale_targets = ScaleTargets()
            >>> scale_targets._response_not_success(response)
            # Raises an exception if the response status code is not 200

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_properties(self, scale_target_name: str) -> dict:
        """Retrieve the properties of a specified scale target.

        Args:
            scale_target_name: The name of the scale target whose properties are to be fetched.

        Returns:
            A dictionary containing the properties for the given scale target name.

        Example:
            >>> scale_targets = ScaleTargets()
            >>> properties = scale_targets.get_properties("FS_AutoscaleDemo")
            >>> print(properties)
            {'scaleTargetName': 'FS_AutoscaleDemo', 'scaleTargetId': 1, ...}

        #ai-gen-doc
        """
        return self._scale_targets[scale_target_name.lower()]

    def _get_all_scale_targets(self) -> dict:
        """Retrieve the list of all scale targets associated with this Commcell.

        Returns:
            dict: A dictionary containing scale target details. Each scale target is represented
            as a dictionary with keys such as "scaleTargetName", "scaleTargetId", "type", and "description".

            Example response structure:
                {
                    "scaleTargetName_1": {
                        "scaleTargetName": "FS_AutoscaleDemo",
                        "scaleTargetId": 1,
                        "type": 1,
                        "description": ""
                    },
                    "scaleTargetName_2": {
                        "scaleTargetName": "LeastAppPermission",
                        "scaleTargetId": 4,
                        "type": 1,
                        "description": ""
                    }
                }

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> scale_targets = ScaleTargets()._get_all_scale_targets()
            >>> for target_name, target_info in scale_targets.items():
            ...     print(f"Target: {target_info['scaleTargetName']}, ID: {target_info['scaleTargetId']}")

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._api_get_scale_targets
        )
        if flag:
            if response.json() and 'basicDetails' in response.json():
                return self._get_scale_target_details_from_response(response.json())
            raise SDKException('ScaleTarget', '103')
        self._response_not_success(response)

    @staticmethod
    def _get_scale_target_details_from_response(response: dict) -> dict:
        """Extract all scale targets and their details from the API response.

        This static method processes the provided API response and returns a dictionary
        where each key represents a scale target name (lowercase), and the corresponding 
        value is a dictionary containing the details of that target.

        Args:
            response: Dictionary containing the API response with 'basicDetails' key.

        Returns:
            Dictionary mapping scale target names (lowercase) to their detail dictionaries.

        Example:
            >>> response = {
            ...     'basicDetails': [
            ...         {'type': 1, 'description': '', 'entity': {'scaleTargetName': 'Target1', 'scaleTargetId': 1}},
            ...         {'type': 1, 'description': '', 'entity': {'scaleTargetName': 'Target2', 'scaleTargetId': 2}}
            ...     ]
            ... }
            >>> targets = ScaleTargets._get_scale_target_details_from_response(response)
            >>> print(targets)
            {'target1': {...}, 'target2': {...}}

        #ai-gen-doc
        """
        _scale_targets = {}
        for scale_target in response.get('basicDetails', []):
            entity = scale_target.get('entity', {})
            target_dict = {}
            target_dict['scaleTargetName'] = entity.get('scaleTargetName', "")
            target_dict['scaleTargetId'] = entity.get('scaleTargetId', 0)
            target_dict['type'] = scale_target.get('type', 0)
            target_dict['description'] = scale_target.get('description', "")
            _scale_targets[entity.get('scaleTargetName', "").lower()] = target_dict
        return _scale_targets

    def refresh(self) -> None:
        """Reload the scale targets associated with the Commcell.

        This method refreshes the internal state of the ScaleTargets object, ensuring that 
        any changes to the scale targets on the Commcell are reflected in this instance.

        Example:
            >>> scale_targets = ScaleTargets(commcell_object)
            >>> scale_targets.refresh()  # Updates the list of scale targets from the Commcell
            >>> print("Scale targets refreshed successfully")

        #ai-gen-doc
        """
        self._scale_targets = self._get_all_scale_targets()

    def get(self, scale_target_name: str) -> 'ScaleTarget':
        """Retrieve a ScaleTarget object for the specified scale target name.

        Args:
            scale_target_name: The name of the Scale Target for which to retrieve the ScaleTarget object.

        Returns:
            ScaleTarget: An instance of the ScaleTarget class corresponding to the given scale target name.

        Raises:
            SDKException: If the response is empty, the response is not successful, or if the scale_target_name is not a string.

        Example:
            >>> scale_targets = ScaleTargets()
            >>> target = scale_targets.get("FS_AutoscaleDemo")
            >>> print(f"Retrieved ScaleTarget: {target.scale_target_name}")

        #ai-gen-doc
        """
        if not isinstance(scale_target_name, str):
            raise SDKException('ScaleTarget', '101')

        if self.has(scale_target_name):
            return ScaleTarget(self._commcell_object, scale_target_name)
        raise SDKException('ScaleTarget', '102', "Unable to get ScaleTarget class object for given scale target name")

    def has(self, scale_target_name: str) -> bool:
        """Check if a scale target exists in the Commcell by name.

        Args:
            scale_target_name: The name of the scale target to check.

        Returns:
            True if the scale target exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the scale_target_name argument is not a string.

        Example:
            >>> scale_targets = ScaleTargets(commcell_object)
            >>> exists = scale_targets.has("FS_AutoscaleDemo")
            >>> print(f"Scale target exists: {exists}")
            # Output: Scale target exists: True

        #ai-gen-doc
        """
        if not isinstance(scale_target_name, str):
            raise SDKException('ScaleTarget', '101')

        return self._scale_targets and scale_target_name.lower() in map(str.lower, self._scale_targets)

    def add(self,
            scale_target_name: str,
            subscription_id: str,
            scale_manager_client_name: str,
            app_credential_name: str,
            resource_group_name: str,
            scale_target_type: ScaleTargetType = ScaleTargetType.AZURE_VM,
            **kwargs) -> 'ScaleTarget':
        """Add a new scale target to the Commcell.

        Args:
            scale_target_name: Name of the scale target to be created.
            subscription_id: Azure subscription ID.
            scale_manager_client_name: Name of the scale manager client.
            app_credential_name: Name of the application credential.
            resource_group_name: Azure resource group name.
            scale_target_type: Type of scale target (default: AZURE_VM).
            **kwargs: Additional optional parameters such as:
                - max_computes_spawned: Maximum computes to spawn (default: 50)
                - description: Description of the scale target
                - use_public_ips: Whether to use public IPs (default: False)
                - compute_tags: List of compute tags (default: [])
                - auth_type: Authentication type (default: 0)
                - fallback_scale_manager_client_name: Fallback scale manager client name
                - regions_config: List of region configurations, each containing:
                    - region: Region name (e.g., "eastus2")
                    - virtual_network_id: Virtual network resource ID
                    - virtual_network_name: Virtual network name
                    - subnet_id: Subnet resource ID
                    - subnet_name: Subnet name
                    - storage_account_id: Storage account resource ID
                    - storage_account_name: Storage account name

        Returns:
            ScaleTarget: An instance of the newly created ScaleTarget.

        Raises:
            SDKException: If the add operation fails or input validation fails.

        Example:
            >>> scale_targets = ScaleTargets(commcell_object)
            >>> regions_config = [
            ...     {
            ...         "region": "eastus2",
            ...         "virtual_network_id": "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Network/virtualNetworks/vnet",
            ...         "virtual_network_name": "my-vnet",
            ...         "subnet_id": "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Network/virtualNetworks/vnet/subnets/default",
            ...         "subnet_name": "default",
            ...         "storage_account_id": "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/storage",
            ...         "storage_account_name": "storage"
            ...     }
            ... ]
            >>> new_target = scale_targets.add(
            ...     scale_target_name="MyScaleTarget",
            ...     subscription_id="4e621aa1-91cf-48c4-88fe-4eea77276df6",
            ...     scale_manager_client_name="yarascalemgr",
            ...     app_credential_name="AutoScaleApp",
            ...     resource_group_name="my_resource_group",
            ...     max_computes_spawned=100,
            ...     regions_config=regions_config
            ... )
            >>> print(f"Created: {new_target.scale_target_name}")

        #ai-gen-doc
        """
        if not isinstance(scale_target_name, str):
            raise SDKException('ScaleTarget', '101')

        # Get scale manager client details
        scale_manager_client = self._commcell_object.clients.get(scale_manager_client_name)
        
        # Get fallback scale manager client details (only if specified, otherwise leave empty)
        fallback_scale_manager_name = kwargs.get('fallback_scale_manager_client_name', '')
        fallback_scale_manager_id = 0
        if fallback_scale_manager_name:
            fallback_scale_manager_client = self._commcell_object.clients.get(fallback_scale_manager_name)
            fallback_scale_manager_id = int(fallback_scale_manager_client.client_id)
        
        # Get credential details
        credentials = self._commcell_object.credentials.get(app_credential_name)

        # Build region-specific info list from regions_config
        region_specific_info_list = []
        regions_config = kwargs.get('regions_config', [])
        for region_config in regions_config:
            region_info = {
                "region": region_config.get('region', ""),
                "virtualNetworkDetails": {
                    "id": region_config.get('virtual_network_id', ""),
                    "name": region_config.get('virtual_network_name', "")
                },
                "subnetDetails": {
                    "id": region_config.get('subnet_id', ""),
                    "name": region_config.get('subnet_name', "")
                },
                "storageAccountDetails": {
                    "id": region_config.get('storage_account_id', ""),
                    "name": region_config.get('storage_account_name', "")
                }
            }
            region_specific_info_list.append(region_info)

        # Build the payload
        payload = {
            "maxComputesSpawned": kwargs.get('max_computes_spawned', 50),
            "use_public_ips": kwargs.get('use_public_ips', False),
            "description": kwargs.get('description', ""),
            "type": scale_target_type.value if isinstance(scale_target_type, ScaleTargetType) else scale_target_type,
            "authType": kwargs.get('auth_type', 0),
            "entity": {
                "scaleTargetName": scale_target_name
            },
            "accessNodes": [
                {              
                    "clientId": int(scale_manager_client.client_id),
                    "name": scale_manager_client_name,
                    "_type_": 3
                }
            ],
            "computeTags": kwargs.get('compute_tags', []),
            "credEntity": {
                "credentialId": int(credentials.credential_id),
                "credentialName": app_credential_name
            },
            "fallbackScalemanagerId": {
                "entity": {
                    "clientName": fallback_scale_manager_name,
                    "clientId": fallback_scale_manager_id,
                    "_type_": 3
                },
                "type": 3
            },
            "azureTargetDetails": {
                "subscriptionDetails": {
                    "id": subscription_id
                },
                "resourceGroupDetails": {
                    "name": resource_group_name
                },
                "regionSpecificInfoList": region_specific_info_list
            }
        }

        
        # Make API call
        api_endpoint = self._services['CREATE_SCALE_TARGET']
        flag, response = self._cvpysdk_object.make_request(
            'POST',
            api_endpoint,
            payload
        )
        if flag:
            if response.json() and 'entity' in response.json():
                self.refresh()
                return ScaleTarget(self._commcell_object, scale_target_name)
            raise SDKException('ScaleTarget', '104')
        self._response_not_success(response)

    def delete(self, scale_target_name: str) -> None:
        """Delete a scale target from the Commcell.

        Args:
            scale_target_name: Name of the scale target to be deleted.

        Raises:
            SDKException: If the scale target does not exist or deletion fails.

        Example:
            >>> scale_targets = ScaleTargets(commcell_object)
            >>> scale_targets.delete("MyScaleTarget")
            >>> print("Scale target deleted successfully")

        #ai-gen-doc
        """
        if not isinstance(scale_target_name, str):
            raise SDKException('ScaleTarget', '101')

        if not self.has(scale_target_name):
            raise SDKException('ScaleTarget', '102', f"Scale target '{scale_target_name}' not found")

        # Get scale target ID
        scale_target_properties = self.get_properties(scale_target_name)
        scale_target_id = scale_target_properties.get('scaleTargetId')

        # Make API call
        api_endpoint = self._services['DELETE_SCALE_TARGET'] % scale_target_id
        flag, response = self._cvpysdk_object.make_request(
            'DELETE',
            api_endpoint
        )

        if flag:
            if response.json():
                response_data = response.json()
                # Check for error code 0 (success)
                if response_data.get('errorCode') == 0:
                    self.refresh()
                    return
                raise SDKException('ScaleTarget', '102', response_data.get('errorMessage', 'Failed to delete scale target'))
            raise SDKException('ScaleTarget', '105')
        self._response_not_success(response)


class ScaleTarget(object):
    """
    ScaleTarget provides an interface for managing and interacting with a single scale target.

    This class allows users to initialize a scale target, retrieve its detailed properties,
    access scale target-specific identifiers and configurations, and refresh the target's state. 
    It is designed to work with a commcell object and a specified scale target name, facilitating 
    operations related to auto-scaling and compute resource management.

    Key Features:
        - Initialization with commcell object and scale target name
        - Retrieval of scale target properties and configurations
        - Access to scale target ID, name, compute limits, and Azure details
        - Access to authentication and credential information
        - Access to compute tags and access nodes
        - Ability to refresh and update the target's state

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object, scale_target_name: str) -> None:
        """Initialize a ScaleTarget object for a specific scale target.

        Args:
            commcell_object: An instance of the Commcell class representing the Commcell connection.
            scale_target_name: The name of the scale target.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> target = ScaleTarget(commcell, 'FS_AutoscaleDemo')
            >>> print("ScaleTarget object created for target:", target.scale_target_name)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._scale_target_name = scale_target_name
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        
        # Initialize properties
        self._scale_target_id = None
        self._description = None
        self._type = None
        self._max_computes_spawned = None
        self._use_public_ips = None
        self._auth_type = None
        self._compute_tags = None
        self._azure_target_details = None
        self._access_nodes = None
        self._credential_entity = None
        self._fallback_scale_manager_id = None
        
        self._api_get_scale_target = self._services['GET_SCALE_TARGET']
        self.refresh()

    def _get_scale_target_properties(self) -> None:
        """Retrieve detailed properties for this scale target from the Commcell.

        This method gathers and updates all configuration properties for this scale target,
        including compute limits, authentication details, Azure configurations, access nodes,
        and credential information.

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> target = ScaleTarget(commcell_object, 'FS_AutoscaleDemo')
            >>> target._get_scale_target_properties()
            >>> print("Scale target properties refreshed.")

        #ai-gen-doc
        """
        # Get scale target ID from basic details
        basic_details = self._commcell_object.scale_targets.get_properties(self._scale_target_name)
        self._scale_target_id = basic_details.get('scaleTargetId')
        
        # Make API call to get detailed properties
        flag, response = self._cvpysdk_object.make_request(
            'GET', 
            self._api_get_scale_target % (self._scale_target_id))
        
        if flag:
            if response.json():
                response_data = response.json()
                self._description = response_data.get('description', "")
                self._type = response_data.get('type', 0)
                self._max_computes_spawned = response_data.get('maxComputesSpawned', 0)
                self._use_public_ips = response_data.get('use_public_ips', False)
                self._auth_type = response_data.get('authType', 0)
                self._compute_tags = response_data.get('computeTags', [])
                self._azure_target_details = response_data.get('azureTargetDetails', {})
                self._access_nodes = response_data.get('accessNodes', [])
                self._credential_entity = response_data.get('credEntity', {})
                self._fallback_scale_manager_id = response_data.get('fallbackScalemanagerId', {
                    "entity": {
                        "clientName": "",
                        "clientId": 0,
                        "_type_": 3
                    },
                    "type": 3
                })
            else:
                raise SDKException('ScaleTarget', '103')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def scale_target_id(self) -> int:
        """Get the ID of the Scale Target.

        Returns:
            The integer value representing the Scale Target ID.

        Example:
            >>> target = ScaleTarget(commcell_object, 'FS_AutoscaleDemo')
            >>> target_id = target.scale_target_id
            >>> print(f"Scale Target ID: {target_id}")

        #ai-gen-doc
        """
        return int(self._scale_target_id)

    @property
    def scale_target_name(self) -> str:
        """Get the name of the Scale Target.

        Returns:
            The Scale Target name as a string.

        Example:
            >>> target = ScaleTarget(commcell_object, 'FS_AutoscaleDemo')
            >>> name = target.scale_target_name
            >>> print(f"Scale Target Name: {name}")

        #ai-gen-doc
        """
        return self._scale_target_name

    @property
    def description(self) -> str:
        """Get the description of the Scale Target.

        Returns:
            The Scale Target description as a string.

        Example:
            >>> target = ScaleTarget()
            >>> desc = target.description
            >>> print(f"Description: {desc}")

        #ai-gen-doc
        """
        return self._description

    @property
    def type(self) -> ScaleTargetType:
        """Get the type of the Scale Target.

        Returns:
            The Scale Target type as a ScaleTargetType enum value.

        Example:
            >>> target = ScaleTarget()
            >>> target_type = target.type
            >>> print(f"Type: {target_type}")
            >>> if target_type == ScaleTargetType.AZURE_VM:
            ...     print("This is an Azure VM scale target")

        #ai-gen-doc
        """
        try:
            return ScaleTargetType(int(self._type))
        except ValueError:
            return ScaleTargetType.NONE

    @property
    def max_computes_spawned(self) -> int:
        """Get the maximum number of computes that can be spawned.

        Returns:
            The maximum number of compute instances as an integer.

        Example:
            >>> target = ScaleTarget()
            >>> max_computes = target.max_computes_spawned
            >>> print(f"Max Computes: {max_computes}")

        #ai-gen-doc
        """
        return int(self._max_computes_spawned)

    @property
    def use_public_ips(self) -> bool:
        """Get whether public IPs are used for the Scale Target.

        Returns:
            Boolean value indicating if public IPs are used.

        Example:
            >>> target = ScaleTarget()
            >>> use_public = target.use_public_ips
            >>> print(f"Use Public IPs: {use_public}")

        #ai-gen-doc
        """
        return self._use_public_ips

    @property
    def auth_type(self) -> int:
        """Get the authentication type for the Scale Target.

        Returns:
            The authentication type as an integer.

        Example:
            >>> target = ScaleTarget()
            >>> auth = target.auth_type
            >>> print(f"Auth Type: {auth}")

        #ai-gen-doc
        """
        return int(self._auth_type)

    @property
    def compute_tags(self) -> list:
        """Get the compute tags associated with the Scale Target.

        Returns:
            A list of compute tag dictionaries with 'key' and 'value' pairs.

        Example:
            >>> target = ScaleTarget()
            >>> tags = target.compute_tags
            >>> print(f"Compute Tags: {tags}")

        #ai-gen-doc
        """
        return self._compute_tags

    @property
    def azure_target_details(self) -> dict:
        """Get the Azure-specific target details.

        Returns:
            A dictionary containing Azure configuration details including resource groups,
            subscriptions, regions, subnets, virtual networks, and storage accounts.

        Example:
            >>> target = ScaleTarget()
            >>> azure_details = target.azure_target_details
            >>> print(f"Azure Details: {azure_details}")

        #ai-gen-doc
        """
        return self._azure_target_details

    @property
    def access_nodes(self) -> list:
        """Get the list of access nodes for the Scale Target.

        Returns:
            A list of access node dictionaries containing clientId, name, and _type_ information.

        Example:
            >>> target = ScaleTarget()
            >>> nodes = target.access_nodes
            >>> print(f"Access Nodes: {nodes}")

        #ai-gen-doc
        """
        return self._access_nodes

    @property
    def credential_entity(self) -> dict:
        """Get the credential entity details for the Scale Target.

        Returns:
            A dictionary containing credentialId and credentialName.

        Example:
            >>> target = ScaleTarget()
            >>> creds = target.credential_entity
            >>> print(f"Credential Entity: {creds}")

        #ai-gen-doc
        """
        return self._credential_entity

    @property
    def region_specific_info_list(self) -> list:
        """Get the list of region-specific information for the Scale Target.

        Returns:
            A list of region configuration dictionaries, each containing region name,
            virtual network details, subnet details, and storage account details.

        Example:
            >>> target = ScaleTarget()
            >>> regions = target.region_specific_info_list
            >>> print(f"Configured Regions: {[r.get('region') for r in regions]}")

        #ai-gen-doc
        """
        return self._azure_target_details.get('regionSpecificInfoList', [])

    def has_region(self, region_name: str) -> bool:
        """Check if a specific region is configured in the Scale Target.

        Args:
            region_name: The name of the region to check (e.g., 'eastus2', 'westus').

        Returns:
            True if the region is configured in regionSpecificInfoList, False otherwise.

        Raises:
            SDKException: If region_name is not a string.

        Example:
            >>> target = ScaleTarget()
            >>> if target.has_region('eastus2'):
            ...     print("Region eastus2 is configured")
            >>> else:
            ...     print("Region eastus2 is not configured")

        #ai-gen-doc
        """
        if not isinstance(region_name, str):
            raise SDKException('ScaleTarget', '101', "Region name must be a string")
        
        region_list = self.region_specific_info_list
        configured_regions = [r.get('region', '').lower() for r in region_list]
        return region_name.lower() in configured_regions

    def edit(self, **kwargs) -> None:
        """Edit an existing scale target with the specified parameters.

        This method allows updating specific properties of a scale target. Only the properties
        provided in kwargs will be updated; all other properties will retain their current values.
        After a successful update, the scale target object is automatically refreshed to reflect
        the changes.

        Args:
            **kwargs: Optional parameters to update, including:
                - scale_target_name: Name of the scale target (default: current name)
                - description: Description of the scale target
                - max_computes_spawned: Maximum computes to spawn (default: current value)
                - use_public_ips: Whether to use public IPs (default: current value)
                - auth_type: Authentication type (default: current value)
                - compute_tags: List of compute tags (default: current value)
                - app_credential_name: Name of the application credential to update (optional)
                - access_node_names: List of access node client names to update. Each client will be fetched 
                    and added as an access node with clientId and name
                - fallback_scale_manager_client_name: Name of the fallback scale manager client to update (optional)
                - regions_config: List of region configurations. Behavior controlled by region_action parameter.
                    Each region object should contain:
                    - region: Region name (e.g., "eastus2")
                    - virtual_network_id: Virtual network resource ID
                    - virtual_network_name: Virtual network name
                    - subnet_id: Subnet resource ID
                    - subnet_name: Subnet name
                    - storage_account_id: Storage account resource ID
                    - storage_account_name: Storage account name
                - region_action: Action to perform with regions_config. Options:
                    - 'replace': Replace all regions with provided regions_config (default)
                    - 'add': Add provided regions to existing regions
                    - 'remove': Remove specified regions by region name from existing regions

        Raises:
            SDKException: If the edit operation fails or input validation fails.

        Example:
            >>> target = ScaleTarget(commcell_object, 'FS_AutoscaleDemo')
            >>> target.edit(
            ...     description="Updated description",
            ...     max_computes_spawned=100
            ... )
            >>> print(f"Updated description: {target.description}")
            
            >>> # Rename scale target
            >>> target.edit(scale_target_name="FS_AutoscaleDemo_New")
            >>> print(f"New name: {target.scale_target_name}")
            
            >>> # Replace all regions
            >>> regions_config = [
            ...     {
            ...         "region": "westus2",
            ...         "virtual_network_id": "/subscriptions/xxx/...",
            ...         "virtual_network_name": "new-vnet",
            ...         "subnet_id": "/subscriptions/xxx/...",
            ...         "subnet_name": "new-subnet",
            ...         "storage_account_id": "/subscriptions/xxx/...",
            ...         "storage_account_name": "newstorage"
            ...     }
            ... ]
            >>> target.edit(regions_config=regions_config, region_action='replace')
            
            >>> # Add new regions to existing ones
            >>> target.edit(regions_config=regions_config, region_action='add')
            
            >>> # Remove specific regions by name
            >>> regions_to_remove = [{"region": "eastus2"}]
            >>> target.edit(regions_config=regions_to_remove, region_action='remove')
            
            >>> # Update access nodes
            >>> target.edit(access_node_names=['yarascalemgr1', 'yarascalemgr2'])
            
            >>> # Update fallback scale manager
            >>> target.edit(fallback_scale_manager_client_name='fallback_scalemgr')

        #ai-gen-doc
        """
        # Update scale target name if provided
        scale_target_name = kwargs.get('scale_target_name', self._scale_target_name)
        if scale_target_name != self._scale_target_name:
            self._scale_target_name = scale_target_name
        
        # Update credential entity if app_credential_name is provided
        credential_entity = self._credential_entity
        if 'app_credential_name' in kwargs:
            app_credential_name = kwargs.get('app_credential_name')
            credentials = self._commcell_object.credentials.get(app_credential_name)
            credential_entity = {
                "credentialId": credentials.credential_id,
                "credentialName": app_credential_name
            }
        
        # Update access nodes if access_node_names is provided
        access_nodes = self._access_nodes
        if 'access_node_names' in kwargs:
            access_node_names = kwargs.get('access_node_names', [])
            access_nodes = []
            for node_name in access_node_names:
                access_node_client = self._commcell_object.clients.get(node_name)
                access_node = {
                    "clientId": int(access_node_client.client_id),
                    "name": node_name,
                    "_type_": 3
                }
                access_nodes.append(access_node)
        
        # Update fallback scale manager if fallback_scale_manager_client_name is provided
        fallback_scale_manager_id = self._fallback_scale_manager_id
        if 'fallback_scale_manager_client_name' in kwargs:
            fallback_scale_manager_name = kwargs.get('fallback_scale_manager_client_name', '')
            if fallback_scale_manager_name:
                fallback_scale_manager_client = self._commcell_object.clients.get(fallback_scale_manager_name)
                fallback_scale_manager_id = {
                    "entity": {
                        "clientName": fallback_scale_manager_name,
                        "clientId": int(fallback_scale_manager_client.client_id),
                        "_type_": 3
                    },
                    "type": 3
                }
            else:
                # If empty string is provided, clear the fallback manager
                fallback_scale_manager_id = {
                    "entity": {
                        "clientName": "",
                        "clientId": 0,
                        "_type_": 3
                    },
                    "type": 3
                }
        
        # Build region-specific info list if regions_config is provided
        azure_target_details = self._azure_target_details.copy()
        
        if 'regions_config' in kwargs:
            regions_config = kwargs.get('regions_config', [])
            region_action = kwargs.get('region_action', 'replace').lower()
            current_regions = azure_target_details.get('regionSpecificInfoList', [])
            region_specific_info_list = []
            
            if region_action == 'replace':
                # Replace all regions with new ones
                for region_config in regions_config:
                    region_info = {
                        "region": region_config.get('region', ""),
                        "virtualNetworkDetails": {
                            "id": region_config.get('virtual_network_id', ""),
                            "name": region_config.get('virtual_network_name', "")
                        },
                        "subnetDetails": {
                            "id": region_config.get('subnet_id', ""),
                            "name": region_config.get('subnet_name', "")
                        },
                        "storageAccountDetails": {
                            "id": region_config.get('storage_account_id', ""),
                            "name": region_config.get('storage_account_name', "")
                        }
                    }
                    region_specific_info_list.append(region_info)
            
            elif region_action == 'add':
                # Add new regions to existing ones
                region_specific_info_list = current_regions.copy()
                existing_region_names = {r.get('region') for r in current_regions}
                
                for region_config in regions_config:
                    region_name = region_config.get('region', "")
                    # Only add if region doesn't already exist
                    if region_name not in existing_region_names:
                        region_info = {
                            "region": region_name,
                            "virtualNetworkDetails": {
                                "id": region_config.get('virtual_network_id', ""),
                                "name": region_config.get('virtual_network_name', "")
                            },
                            "subnetDetails": {
                                "id": region_config.get('subnet_id', ""),
                                "name": region_config.get('subnet_name', "")
                            },
                            "storageAccountDetails": {
                                "id": region_config.get('storage_account_id', ""),
                                "name": region_config.get('storage_account_name', "")
                            }
                        }
                        region_specific_info_list.append(region_info)
            
            elif region_action == 'remove':
                # Remove specified regions by region name
                regions_to_remove = {r.get('region') for r in regions_config}
                region_specific_info_list = [
                    r for r in current_regions 
                    if r.get('region') not in regions_to_remove
                ]
            
            azure_target_details['regionSpecificInfoList'] = region_specific_info_list
        
        # Build the complete payload using current values + updates
        payload = {
            "description": kwargs.get('description', self._description),
            "type": self._type,
            "maxComputesSpawned": kwargs.get('max_computes_spawned', self._max_computes_spawned),
            "use_public_ips": kwargs.get('use_public_ips', self._use_public_ips),
            "authType": kwargs.get('auth_type', self._auth_type),
            "entity": {
                "scaleTargetName": scale_target_name,
                "scaleTargetId": int(self._scale_target_id),
            },
            "accessNodes": access_nodes,
            "computeTags": kwargs.get('compute_tags', self._compute_tags),
            "credEntity": credential_entity,
            "fallbackScalemanagerId": fallback_scale_manager_id,
            "azureTargetDetails": azure_target_details
        }        

        # Make API call
        api_endpoint = self._services['UPDATE_SCALE_TARGET'] % self._scale_target_id
        flag, response = self._cvpysdk_object.make_request(
            'POST',
            api_endpoint,
            payload
        )

        if flag:
            if response.json():
                response_data = response.json()
                # Check for error code 0 (success)
                if response_data.get('errorCode') == 0:
                    if 'scale_target_name' in kwargs:
                        self._commcell_object.scale_targets.refresh()  # Refresh the scale targets list in Commcell object if name was changed
                    self.refresh()
                    return
                raise SDKException('ScaleTarget', '102', response_data.get('errorMessage', 'Failed to update scale target'))
            raise SDKException('ScaleTarget', '106')
        raise SDKException('Response', '101', self._update_response_(response.text))

    def refresh(self) -> None:
        """Reload the scale target details associated with this Commcell.

        This method refreshes the internal state of the ScaleTarget object, ensuring that 
        any changes made to the scale target configuration on the Commcell are reflected 
        in this instance.

        Example:
            >>> target = ScaleTarget(commcell_object, 'FS_AutoscaleDemo')
            >>> target.refresh()  # Updates the scale target details from the Commcell
            >>> print("Scale target details refreshed.")

        #ai-gen-doc
        """
        self._get_scale_target_properties()
