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

"""Main file for performing Cleanroom Target specific operations.

CleanroomTargets and CleanroomTarget are 2 classes defined in this file.

CleanroomTargets:     Class for representing all the cleanroom targets

CleanroomTarget:      Class for a single cleanroom target selected, and to perform operations on that cleanroom target


cleanroomTargets:
    __init__()                   --  initialize object of CleanroomTargets class

    __str__()                   --  returns all the Cleanroom Targets

    _get_cleanroom_targets()     -- Gets all the cleanroom targets

    has_cleanroom_target()       -- Checks if a target is present in the commcell.

    get()                        --  returns the cleanroom target class object of the input target name

    refresh()                   --  refresh the targets present in the client

    get_supported_regions_smart_folder()    --  retrieves supported cloud regions from smart folder

    get_supported_regions_resource_pool()   --  retrieves supported cloud regions from resource pool

    get_supported_regions_cloud()           --  retrieves AWS cloud regions from vendor API

    get_all_supported_regions()            --  retrieves all supported regions for SW

    create()                    --  creates a cleanroom target with the specified payload

    populate_payload()        --  builds the payload with the required fields for creating a cleanroom target

cleanroomTargets Attributes
--------------------------

    **all_targets**             --  returns the dictionary consisting of all the targets that are
    present in the commcell and their information such as id and name

CleanroomTarget:
    __init__()                   --   initialize object of CleanroomTarget with the specified cleanroom target name

    _get_cleanroom_target_id()   --   method to get the cleanroom target id

    _get_cleanroom_target_properties()  --   get the properties of this recovery target

    _delete_cleanroom_target()    -- Deletes the cleanroom target

    delete()                     -- Deletes the cleanroom target

    refresh()                   --   refresh the object properties

CleanroomTarget Attributes
--------------------------

    **cleanroom_target_id**      -- Returns the id of the cleanroom target
    **cleanroom_target_name**    -- Returns the name of the cleanroom Target
    **destination_hypervisor**  -- Returns the name of destination hypervisor
    **vm_prefix**               -- Returns the prefix of the vm name
    **destination_host**        -- Returns the destination host
    **storage_account**          -- Returns the storage_account host
    **policy_type**             -- Returns the policy type
    **application_type**          -- Returns the application type
    **restore_as_managed_vm**   -- Returns the restore_as_managed_vm
    **region**                  -- Returns the region
    **expiration_time**         -- Returns the _expiration_time
    **vm_suffix**               -- Returns the vm_suffix
    **vm_prefix**               -- Returns the vm_prefix
    **access_node**             -- Returns the access_node
    **access_node_client_group** -- Returns the access_node_client_group

"""
from __future__ import absolute_import
from __future__ import unicode_literals

from typing import Dict, TYPE_CHECKING, Optional
from json.decoder import JSONDecodeError

from cvpysdk.exception import SDKException

if TYPE_CHECKING:
    from cvpysdk.commcell import Commcell

from dataclasses import dataclass

@dataclass(frozen=True)
class CleanroomSiteRegionParams:
    """
    Common parameters used by region APIs.
    """
    # Supported Regions MAPI for smart folder
    feature: Optional[int] = 18
    workload_id: Optional[int] = 15001
    region_type: Optional[int] = None

    # Cloud Regions API
    vendor: Optional[int] = None

    # V4 Regions API for resource pool
    workload_type: Optional[int] = None
    cloud_type: Optional[str] = None


class CleanroomTargets:
    """
    Manages and represents all Cleanroom targets within a Commcell environment.

    This class provides an interface for interacting with Cleanroom targets, including
    retrieving, creating, and refreshing target information. It supports checking for
    the existence of specific targets, accessing all available targets, and constructing
    payloads for target operations. Designed to work with a Commcell object, it enables
    seamless integration and management of Cleanroom resources.

    Key Features:
        - Initialization with a Commcell object
        - String representation of Cleanroom targets
        - Retrieval of all Cleanroom targets
        - Property access to all targets
        - Existence check for a specific Cleanroom target
        - Fetching details of a specific Cleanroom target
        - Refreshing the Cleanroom targets list
        - Creation of new Cleanroom targets using payloads
        - Payload population for target operations

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a new instance of the CleanroomTargets class.

        Args:
            commcell_object: An instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> cleanroom_targets = CleanroomTargets(commcell)
            >>> print("CleanroomTargets object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._RECOVERY_TARGETS_API = self._services['GET_ALL_RECOVERY_TARGETS']
        self._TARGET_URL = self._services['CREATE_RUNBOOK_TARGET']
        self._GET_ALL_REGIONS_API = f"{self._services['GET_REGIONS']}&useDefaultLocaleId=true"
        self._SUPPORTED_REGIONS_MAPI = self._services['GET_SUPPORTED_REGIONS_MAPI']
        self._CLOUD_REGIONS_API = self._services['GET_CLOUD_REGIONS']
        self._RESOURCE_POOL_REGIONS_API = (
            f"{self._services['REGIONS']}?workloadId=%s&type=%s"
        )
        self._CLEANROOM_SITE_URL = self._services['CLEANROOM_SITE']

        self._SITE_VENDOR_REGION_PARAMS = {
            'AMAZON': CleanroomSiteRegionParams(region_type=2, vendor=4, workload_type=0, cloud_type='AWS'),
            'AZURE_V2': CleanroomSiteRegionParams(region_type=1, vendor =7, workload_type=0, cloud_type='AZURE')
        }
        self._cleanroom_targets = None
        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all cleanroom targets.

        This method provides a human-readable string that lists all targets managed by the CleanroomTargets instance.

        Returns:
            A string containing the details of all targets.

        Example:
            >>> targets = CleanroomTargets()
            >>> print(str(targets))
            Target1, Target2, Target3

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'CleanroomTargets')

        for index, cleanroom_target in enumerate(self._cleanroom_targets):
            sub_str = '{:^5}\t{:20}\n'.format(
                index + 1,
                cleanroom_target
            )
            representation_string += sub_str

        return representation_string.strip()

    def _get_cleanroom_targets(self) -> dict:
        """Retrieve all cleanroom targets associated with the client.

        Returns:
            dict: A dictionary mapping target names to their corresponding IDs.
                Example:
                    {
                        "target1_name": target1_id,
                        "target2_name": target2_id
                    }

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> targets = cleanroom_targets._get_cleanroom_targets()
            >>> print(targets)
            {'FinanceDB': 101, 'HRDocs': 102}

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGETS_API)
        if flag:
            if response.json() and 'recoveryTargets' in response.json():
                cleanroom_target_dict = {}
                for cleanroomTarget in response.json()['recoveryTargets']:
                    if cleanroomTarget['applicationType'] == "CLEAN_ROOM":
                        temp_name = cleanroomTarget['name'].lower()
                        cleanroom_target_dict[temp_name] = str(cleanroomTarget['id'])

                return cleanroom_target_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_targets(self) -> Dict[str, int]:
        """Get a dictionary of all cleanroom targets.

        Returns:
            Dict[str, int]: A dictionary mapping each target's name to its unique ID.

            Example output:
                {
                    "target1_name": 101,
                    "target2_name": 102
                }

        Example:
            >>> targets = cleanroom_targets.all_targets
            >>> print(targets)
            {'target1_name': 101, 'target2_name': 102}
            >>> # Access a specific target's ID
            >>> target_id = targets.get('target1_name')
            >>> print(f"Target ID: {target_id}")

        #ai-gen-doc
        """
        return self._cleanroom_targets

    def has_cleanroom_target(self, target_name: str) -> bool:
        """Check if a cleanroom target with the specified name exists in the Commcell.

        Args:
            target_name: The name of the cleanroom target to check.

        Returns:
            True if the target exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the type of the target_name argument is not a string.

        Example:
            >>> targets = CleanroomTargets(commcell_object)
            >>> exists = targets.has_cleanroom_target("TargetA")
            >>> print(f"TargetA exists: {exists}")

        #ai-gen-doc
        """
        if not isinstance(target_name, str):
            raise SDKException('Target', '101')

        return self._cleanroom_targets and target_name.lower() in self._cleanroom_targets

    def get(self, cleanroom_target_name: str) -> 'CleanroomTarget':
        """Retrieve a target object by its name.

        Args:
            cleanroom_target_name: The name of the cleanroom target to retrieve.

        Returns:
            An instance of the target class corresponding to the specified target name.

        Raises:
            SDKException: If the provided target name is not a string or if no target exists with the given name.

        Example:
            >>> targets = CleanroomTargets()
            >>> target = targets.get("TargetA")
            >>> print(f"Retrieved target: {target}")

        #ai-gen-doc
        """
        if not isinstance(cleanroom_target_name, str):
            raise SDKException('Target', '101')
        else:
            cleanroom_target_name = cleanroom_target_name.lower()

            if self.has_cleanroom_target(cleanroom_target_name):
                return CleanroomTarget(
                    self._commcell_object, cleanroom_target_name, self.all_targets[cleanroom_target_name])

            raise SDKException('RecoveryTarget', '102', 'No target exists with name: {0}'.format(cleanroom_target_name))

    def refresh(self) -> None:
        """Reload the cleanroom targets to ensure the latest information is available.

        This method refreshes the internal state of the CleanroomTargets object, updating its data
        to reflect any recent changes in the cleanroom targets.

        Example:
            >>> targets = CleanroomTargets()
            >>> targets.refresh()
            >>> print("Cleanroom targets have been refreshed.")

        #ai-gen-doc
        """
        self._cleanroom_targets = self._get_cleanroom_targets()

    def get_supported_regions_smart_folder(self, vendor: str) -> dict:
        """Return supported regions for the vendor from Smart Folder config (MAPI)."""

        params = getattr(self, '_SITE_VENDOR_REGION_PARAMS', {}).get(vendor.upper())
        if not params:
            raise SDKException('CleanroomSite', '101', f'Unsupported vendor: {vendor}')

        if params.feature is None or params.region_type is None:
            raise SDKException('CleanroomSite', '101', f'Missing feature/region_type for vendor: {vendor}')

        api_url = self._SUPPORTED_REGIONS_MAPI % (params.feature, params.region_type)
        flag, response = self._cvpysdk_object.make_request('GET', api_url)

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        try:
            response_json = response.json()
            return (response_json or {}).get('data', {}).get('regions', []) or []
        except JSONDecodeError:
            raise SDKException('Response', '102', 'Invalid JSON response received from the server.')

    def get_supported_regions_resource_pool(self, vendor: str) -> dict:
        """Return supported regions for the vendor from Resource Pool (V4 Regions) endpoint."""

        params = getattr(self, '_SITE_VENDOR_REGION_PARAMS', {}).get(vendor.upper())
        if not params:
            raise SDKException('CleanroomSite', '101', f'Unsupported vendor: {vendor}')

        if params.workload_id is None or not params.cloud_type:
            raise SDKException('CleanroomSite', '101', f'Missing workload_id/cloud_type for vendor: {vendor}')

        api_url = self._RESOURCE_POOL_REGIONS_API % (params.workload_id, params.cloud_type)
        flag, response = self._cvpysdk_object.make_request('GET', api_url)

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        try:
            response_json = response.json()
            return (response_json or {}).get('regions', []) or []
        except JSONDecodeError:
            raise SDKException('Response', '102', 'Invalid JSON response received from the server.')

    def get_supported_regions_cloud(self, vendor: str) -> dict:
        """Return supported regions for the vendor from Cloud/Regions endpoint."""

        params = getattr(self, '_SITE_VENDOR_REGION_PARAMS', {}).get(vendor.upper())
        if not params:
            raise SDKException('CleanroomSite', '101', f'Unsupported vendor: {vendor}')

        if params.vendor is None:
            raise SDKException('CleanroomSite', '101', f'Missing vendor id for vendor: {vendor}')

        api_url = self._CLOUD_REGIONS_API % (params.vendor,)
        flag, response = self._cvpysdk_object.make_request('GET', api_url)

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        try:
            response_json = response.json()
            return (response_json or {}).get('regions', []) or []
        except JSONDecodeError:
            raise SDKException('Response', '102', 'Invalid JSON response received from the server.')

    def get_all_supported_regions(self, vendor: str) -> list[dict]:
        """Return all supported regions for SW."""

        params = getattr(self, '_SITE_VENDOR_REGION_PARAMS', {}).get(vendor.upper())
        if not params:
            raise SDKException('CleanroomSite', '101', f'Unsupported vendor: {vendor!r}')

        if not params.region_type:
            raise SDKException('CleanroomSite', '101', f'Missing type for vendor: {vendor!r}')

        api_url = self._GET_ALL_REGIONS_API % params.region_type
        flag, response = self._cvpysdk_object.make_request('GET', api_url)

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        try:
            response_json = response.json()
            return (response_json or {}).get('regions', []) or []
        except JSONDecodeError:
            raise SDKException('Response', '102', 'Invalid JSON response received from the server.')

    def create(self, payload: dict = dict()) -> dict:
        """Create a new cleanroom target with the specified payload.

        Args:
            payload: Dictionary containing the parameters required to create the cleanroom target.
                Example payload:
                    {
                        "name": "target_name",
                        "description": "Target description",
                        ...
                    }

        Returns:
            dict: Response from the API containing details of the created target, such as:
                {
                    "id": 1234567890,
                    "name": "target_name"
                }

        Raises:
            SDKException: If the payload is not a dictionary, if the API response is empty, or if the API response indicates failure.

        Example:
            >>> targets = CleanroomTargets()
            >>> payload = {"name": "MyTarget", "description": "Test target"}
            >>> response = targets.create(payload)
            >>> print(response)
            {'id': 1234567890, 'name': 'MyTarget'}

        #ai-gen-doc
        """
        if not isinstance(payload, dict):
            raise SDKException('RecoveryTarget', '101', 'Payload must be a dictionary')
        flag, response = self._cvpysdk_object.make_request('POST', self._TARGET_URL, payload=payload)

        if flag:
            try:
                response_json = response.json()
                if not response_json:
                    raise ValueError('Response', '102', 'Empty response received from the server')

                if "id" in response_json:
                    return response_json
                else:
                    raise KeyError('Response', '102', 'Target ID not found in the response')
            except JSONDecodeError:
                raise ValueError('Response', '102', 'Invalid response received from the server.')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def populate_payload(self, target: dict, region: dict, node: dict = None) -> dict:
        """Build the payload with the required fields for creating a cleanroom target.

        This method constructs and returns a payload dictionary for cleanroom target creation,
        using the provided target, region, and optionally access node details.

        Args:
            target: Dictionary containing target details. Must include required fields depending on the use case.
            region: Dictionary containing region details to be included in the payload.
            node: Optional dictionary with access node details. Required when specifying a new access node.

        Returns:
            A dictionary representing the populated payload for cleanroom target creation.

        Raises:
            SDKException: If the target input is empty or if the target name is not a string.

        Example:
            >>> target = {
            ...     "target_name": "Cleanroom_Target",
            ...     "target_vendor": "AZURE_V2",
            ...     "credentials_id": 1234567890,
            ...     "credentials_name": "Azure_Credentials",
            ...     "subscription_id": "<subscription_id>",
            ... }
            >>> region = {
            ...     "guid": "eastus (Commcell)",
            ...     "name": "US East"
            ... }
            >>> node = {
            ...     "access_node_id": 1234567890,
            ...     "access_node_type": 3
            ... }
            >>> payload = cleanroom_targets.populate_payload(target, region, node)
            >>> print(payload)
            #ai-gen-doc
        """
        if not isinstance(target['target_name'], str):
            raise SDKException('RecoveryTarget', '101', 'Missing or invalid target name')
        api_payload = {
                            "options": {
                            "region": region if region else {},
                            "accessNode": {}
                            }
                        }
        #Populate the payload with access node details
        if node.get('access_node_id') is not None:  #Using existing access node or access node group
            access_node_entity = {
                "id": node.get('access_node_id', 0),
                "name": node.get('access_node_name', 'string'),
                "type": node.get('access_node_type', 3)
            }
            api_payload['options']['accessNode'].update(access_node_entity)
        if not target:
            raise SDKException('RecoveryTarget', '101', 'Target payload cannot be empty')
        elif target.get('target_id') is not None and target.get('target_id') > 0 :  #Using existing target
            target_entity = {
                "entity": {
                "id": target.get('target_id', 0),
                "name": target.get('target_name', 'string')
                }
            }
            api_payload.update(target_entity)
        else:
            options = {
                        "vendor": target.get('target_vendor', 'AZURE_V2')
                    }
            api_payload['options'].update(options)
            if target.get("target_id") == 0 or target.get("target_id") == "":
                if target.get("hypervisor_id") is not None:  # Using existing hypervisor to create new target
                    existing_hypervisor = {
                        "hypervisor": {
                            "entity": {
                                "id": target.get('hypervisor_id', 0),
                                "name": target.get('hypervisor_name', 'string')
                            }
                        }
                    }
                    access_node_entity = {
                        "id": 0,
                        "type": 28
                    }
                    api_payload['options'].update(existing_hypervisor)
                    api_payload['options']['accessNode'].update(access_node_entity)
                elif target.get("credentials_id") is not None:  #Using existing credentials to create new hypervisor for the target
                    new_hypervisor = {
                        "hypervisor": {
                            "optionsAzure": {
                                "credentials": {
                                    "id": target.get('credentials_id', 0),
                                    "name": target.get('credentials_name', 'string')
                                },
                            "skipCredentialValidation": False,
                            "subscriptionId": target.get('subscription_id', '<subscription_id>'),
                            "useManagedIdentity": False
                            }
                        }
                    }
                    options.update(new_hypervisor)
                    api_payload['options'].update(options)
        return api_payload

    def create_cleanroom_site(self, payload: dict) -> dict:
        """Create a cleanroom site via POST ``Cleanroom/Site``.

        Args:
            payload: Full POST request body dict (as expected by the API).

        Returns:
            dict: API response, e.g. ``{'id': 1234, 'name': 'MySite'}``.

        Raises:
            SDKException: On non-200 API response or invalid JSON.
        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._CLEANROOM_SITE_URL, payload=payload
        )
        if flag:
            try:
                response_json = response.json()
                if not response_json:
                    raise SDKException('Response', '102', 'Empty response received from server')
                return response_json
            except JSONDecodeError:
                raise SDKException('Response', '102', 'Invalid JSON response received from server')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def delete_cleanroom_site(self, target_id) -> bool:
        """Delete a cleanroom site by its numeric target ID.

        Uses ``DELETE V4/RecoveryTarget/{id}``.

        Args:
            target_id: Integer or string ID of the cleanroom target to delete.

        Returns:
            bool: ``True`` on success.

        Raises:
            SDKException: If the DELETE request fails.
        """
        delete_url = self._services['GET_RECOVERY_TARGET'] % str(target_id)
        flag, response = self._cvpysdk_object.make_request('DELETE', delete_url)
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))
        return True


class CleanroomTarget:
    """
    Class for managing and performing operations on cleanroom targets.

    The CleanroomTarget class provides a comprehensive interface for handling cleanroom target entities,
    including creation, deletion, property management, and configuration of various infrastructure and
    security settings. It exposes numerous properties for accessing and modifying target attributes such as
    instance details, network configuration, security groups, storage accounts, and more.

    Key Features:
        - Initialization with commcell object, target name, and target ID
        - Retrieval and management of cleanroom target ID and properties
        - Deletion of cleanroom targets
        - Setting and accessing policy types
        - Extensive property accessors for:
            - Target instance and application type
            - Hypervisor and access node details
            - Security user names and client groups
            - VM naming conventions (prefix/suffix)
            - Storage account, region, and availability zone
            - Network, security group, and resource group configuration
            - Public IP, VM size, and bastion deployment options
            - Custom image and infrastructure network settings
            - NAT gateway, public IP settings, and server groups
            - IAM role, encryption key, instance and volume types
            - Network subnet, key pair, and other security settings
        - Refreshing target properties
        - Deleting cleanroom targets

    This class is intended for use in environments where secure, isolated target management is required,
    providing fine-grained control over infrastructure and security parameters.

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', cleanroom_target_name: str, cleanroom_target_id: str = None) -> None:
        """Initialize a new instance of the CleanroomTarget class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            cleanroom_target_name: The name of the cleanroom target.
            cleanroom_target_id: Optional; the unique identifier for the cleanroom target. If not provided, it may be set later.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> target = CleanroomTarget(commcell, 'TargetA', '12345')
            >>> # The CleanroomTarget instance is now initialized and ready for use

        #ai-gen-doc
        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._cleanroom_target_name = cleanroom_target_name.lower()

        if cleanroom_target_id:
            # Use the target id mentioned in the arguments
            self._cleanroom_target_id = str(cleanroom_target_id)
        else:
            # Get the target id if target id is not provided
            self._cleanroom_target_id = self._get_cleanroom_target_id()
        self._RECOVERY_TARGET_API = self._services['GET_RECOVERY_TARGET'] % self._cleanroom_target_id
        self._RUNBOOK_TARGET_API = self._services['GET_RUNBOOK_TARGET'] % self._cleanroom_target_id
        self._EDIT_RUNBOOK_TARGET_API = self._services['EDIT_RUNBOOK_TARGET_API'] % self._cleanroom_target_id
        self._cleanroom_target_properties = None

        self._policy_type = None
        self._application_type = None
        self._destination_hypervisor = None
        self._access_node = None
        self._access_node_client_group = None
        self._instance = None
        self._users = []
        self._user_groups = []
        self._vm_prefix = ''
        self._vm_suffix = ''
        self._expiration_time = None

        self._region = None
        self._availability_zone = None
        self._storage_account = None
        self._resource_group = None
        self._restore_as_managed_vm = None
        self._infra_server_group_name = None
        self._infra_server_group_id = None

        self._maxNoOfAccessNodes = None
        self._infra_security_group = None
        self._infra_vpc = None
        self._infra_virtual_network = None
        self._natGatewayPublicIPSettings = None
        self._infraPublicIPprefix = None
        self._infraPublicIP = None
        self._infra_resourceGroup = None
        self._infra_vm_size = None
        self._custom_images = None
        self._networkAddressSpace = None
        self._deployBastion = None
        self._recovery_SecurityRules = None
        self._infra_SecurityRules = None

        self._instance_type = None
        self._encryption_key = None
        self._key_pair = None
        self._iam_role = None
        self._volume_type = None
        self._network_subnet = None
        self._security_group = None

        self._esx_server = None
        self._datastore = None
        self._destination_network = None
        self._resource_pool = None
        self._folder_path = None
        self._storage_policy_name = None
        self.refresh()

    def _get_cleanroom_target_id(self) -> str:
        """Retrieve the unique identifier associated with this cleanroom target.

        Returns:
            The target ID as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> target_id = target._get_cleanroom_target_id()
            >>> print(f"Target ID: {target_id}")

        #ai-gen-doc
        """
        target = CleanroomTargets(self._commcell_object)
        return target.all_targets[self._cleanroom_target_name]

    def _delete_cleanroom_target(self) -> None:
        """Delete the cleanroom target associated with this object.

        This method removes the cleanroom target from the system. If the deletion is unsuccessful,
        an SDKException is raised.

        Raises:
            SDKException: If the response indicates the deletion was not successful.

        Example:
            >>> target = CleanroomTarget()
            >>> target._delete_cleanroom_target()
            >>> print("Cleanroom target deleted successfully.")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('DELETE', self._RECOVERY_TARGET_API)
        if flag:
            return flag
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_policy_type(self, policy_type: str) -> None:
        """Set the policy type for the CleanroomTarget instance.

        Args:
            policy_type: The type of policy to assign (e.g., "retention", "access").

        Example:
            >>> target = CleanroomTarget()
            >>> target._set_policy_type("retention")
            >>> # The policy type is now set to "retention" for this target

        #ai-gen-doc
        """
        if policy_type == "AMAZON":
            self._policy_type = 1
        elif policy_type == "MICROSOFT":
            self._policy_type = 2
        elif policy_type == "AZURE_V2":
            self._policy_type = 7
        elif policy_type in ["VMW_BACKUP_LABTEMPLATE", "VMW_LIVEMOUNT"]:
            self._policy_type = 13
        elif policy_type == "VMW":
            self._policy_type = 0
        else:
            self._policy_type = -1

    def edit_cleanroom_target_custom_image(self, image_info, infra_vm_size):
        """Edits the cleanroom target to add or update custom images.

        Args:
            image_info: Dictionary or list of dictionaries containing custom image details.
                Single image format:
                    {
                        'imageGUID': '/subscriptions/.../resourceGroups/.../images/imageName',
                        'imageName': 'DisplayName',
                        'operatingSystem': 'UNIX' or 'WINDOWS'
                    }
            infra_vm_size: VM size identifier to set for infrastructure; when None,
                the existing VM size setting is left unchanged.

        Raises:
            SDKException: If the API request fails or returns invalid data.

        Example:
            >>> target = CleanroomTarget(commcell, 'target_name')
            >>> image = {
            ...     'imageGUID': '/subscriptions/abc/resourceGroups/rg/images/myImage',
            ...     'imageName': 'myImage - [x64] [Gen2] [Linux] [Generalized]',
            ...     'operatingSystem': 'UNIX'
            ... }
            >>> target.edit_cleanroom_target_custom_image(image, infra_vm_size)
        """
        # Get current target configuration
        flag, response = self._cvpysdk_object.make_request('GET', self._RUNBOOK_TARGET_API)
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        if not response.json():
            raise SDKException('Response', '102', 'Empty response received from server')

        target_payload = response.json()

        # Ensure infrastructure and advancedSettings exist in payload
        if 'infrastructure' not in target_payload:
            target_payload['infrastructure'] = {}
        if 'advancedSettings' not in target_payload['infrastructure']:
            target_payload['infrastructure']['advancedSettings'] = {}

        # Process image_info - convert single image to list
        if isinstance(image_info, dict):
            custom_images = [image_info]
        elif isinstance(image_info, list):
            custom_images = image_info
        else:
            raise SDKException('RecoveryTarget', '101', 'image_info must be a dictionary or list')

        # Validate custom image format
        for image in custom_images:
            if not all(key in image for key in ['imageGUID', 'imageName', 'operatingSystem']):
                raise SDKException(
                    'RecoveryTarget', '101',
                    'Each custom image must contain imageGUID, imageName, and operatingSystem'
                )
            if image['operatingSystem'] not in ['UNIX', 'WINDOWS']:
                raise SDKException(
                    'RecoveryTarget', '101',
                    'operatingSystem must be either UNIX or WINDOWS'
                )

        # Update custom images in payload
        target_payload['infrastructure']['advancedSettings']['customImages'] = custom_images
        # Only set vmSize when provided to avoid clearing existing value unintentionally
        if infra_vm_size is not None:
            target_payload['infrastructure']['advancedSettings']['vmSize'] = infra_vm_size

        # Make PUT request to update target
        flag, response = self._cvpysdk_object.make_request(
            'PUT',
            self._EDIT_RUNBOOK_TARGET_API,
            payload=target_payload
        )

        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        # Refresh target properties after update
        self.refresh()

    def _get_cleanroom_target_properties(self) -> dict:
        """Retrieve the properties of the cleanroom target.

        This method fetches and returns the configuration properties associated with the current cleanroom target.

        Returns:
            dict: A dictionary containing the cleanroom target's properties.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> target = CleanroomTarget()
            >>> properties = target._get_cleanroom_target_properties()
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2'}

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RUNBOOK_TARGET_API)
        flag_old, response_old = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGET_API)

        if flag and flag_old:
            if response.json():
                self._cleanroom_target_properties = response.json()
                self._application_type = (
                    self._cleanroom_target_properties.get("general", {}).get("target", {}).get("applicationType", ""))
                self._destination_hypervisor = (
                    self._cleanroom_target_properties.get("general", {}).get("hypervisor", {}).get("name", ""))
                self._vm_suffix = (
                    self._cleanroom_target_properties.get("general", {}).get("entityDisplayName", {}).get("suffix", ""))
                self._vm_prefix = (
                    self._cleanroom_target_properties.get("general", {}).get("entityDisplayName", {}).get("prefix", ""))
                access_node = self._cleanroom_target_properties.get("general", {}).get("accessNode", {})
                node_type = access_node.get("type", "")

                self._access_node = (
                    "Automatic"
                    if node_type == "Automatic"
                    else {
                        "type": node_type,
                        "name": access_node.get("name", ""),
                        "id": access_node.get("id", "")
                    }
                    if node_type in ("Client", "Group")
                    else None
                )
                self._users = (
                    self._cleanroom_target_properties.get("general", {}).get('security', {}).get('users', []))
                self._user_groups = (
                    self._cleanroom_target_properties.get("general", {}).get('securityOptions', {}).get('userGroups',
                                                                                                        []))
                self._instance = (
                    self._cleanroom_target_properties.get("general", {}).get("target", {}).get("vendor", ""))
                self._set_policy_type(self._instance)
                self._is_automatic_site = (
                    self._cleanroom_target_properties.get("general", {}).get("deployCleanroomResources", {}).get("isEnabled", False)
                )
                if response_old.json():
                    self._cleanroom_old_target_properties = response_old.json()
                    if self.policy_type == 1:
                        self._region = (self._cleanroom_old_target_properties.get('cloudDestinationOptions', {})
                                        .get('region', {})
                                        .get('name', ''))
                        self._availability_zone = (
                            self._cleanroom_old_target_properties.get('cloudDestinationOptions', {})
                                .get('availabilityZone', ''))
                        self._iam_role = (self._cleanroom_old_target_properties.get('destinationOptions', {})
                                          .get('iamRole', {}).get('name', ''))
                        self._encryption_key = (self._cleanroom_old_target_properties.get('cloudDestinationOptions', {})
                                                .get('encryptionKey', {}).get('name', ''))

                        # Get the first instance type, or None if not defined or empty
                        self._instance_type = (
                                self._cleanroom_old_target_properties.get('cloudDestinationOptions', {})
                                .get('instanceTypes') or [None]
                        )[0]
                        self._security_group = (self._cleanroom_old_target_properties.get('securityOptions', {})
                                                .get('securityGroups', [{}])[0]
                                                .get('name', ''))
                        self._network_subnet = (self._cleanroom_old_target_properties.get('networkOptions', {})
                                                .get('networkCard', {})
                                                .get('network', ''))
                        self._volume_type = (self._cleanroom_old_target_properties.get('cloudDestinationOptions', {})
                                             .get('volumeType', {}))
                        self._key_pair = (self._cleanroom_old_target_properties.get('cloudDestinationOptions', {})
                                          .get('keyPair', ''))

                # Parse new AWS properties from recovery section
                if self._policy_type == 1:
                    self._region = (self._cleanroom_target_properties.get('recovery', {})
                                    .get('region', {}).get('guid', ''))
                    self._availability_zone = (self._cleanroom_target_properties.get('recovery', {})
                                               .get('availabilityZone', {}).get('guid', ''))
                    self._key_pair = (self._cleanroom_target_properties.get('recovery', {})
                                      .get('keyPair', {}).get('name', ''))
                    self._iam_role = (self._cleanroom_target_properties.get('recovery', {})
                                      .get('iamRole', {}).get('name', ''))
                    self._encryption_key = (self._cleanroom_target_properties.get('recovery', {})
                                            .get('encryptionKey', {}).get('name', ''))
                    self._volume_type = (self._cleanroom_target_properties.get('recovery', {})
                                         .get('volumeType', ''))
                    self._vpc = (self._cleanroom_target_properties.get('recovery', {})
                                 .get('vpc', {}).get('name', ''))
                    self._security_groups = (self._cleanroom_target_properties.get('recovery', {})
                                             .get('securityGroups', []))
                    self._instance_type = (self._cleanroom_target_properties.get('recovery', {})
                                           .get('instanceType', {}).get('guid', ''))
                    self._create_public_ip = (self._cleanroom_target_properties.get('recovery', {})
                                              .get('createPublicIPAddress', False))

                    # Infrastructure network settings
                    self._maxNoOfAccessNodes = (self._cleanroom_target_properties.get('infrastructure', {})
                                                .get('maxNoOfAccessNodes', ''))
                    self._infra_vpc = (self._cleanroom_target_properties.get('infrastructure', {})
                                                   .get('networkSettings', {}).get('vpc', {})
                                                   .get('name', ''))
                    self._infra_virtual_network = (self._cleanroom_target_properties.get('infrastructure', {})
                                                   .get('networkSettings', {}).get('virtualNetwork', {})
                                                   .get('name', ''))
                    self._infra_security_groups = (self._cleanroom_target_properties.get('infrastructure', {})
                                                   .get('networkSettings', {}).get('securityGroups', []))
                    self._infra_create_public_ip = (self._cleanroom_target_properties.get('infrastructure', {})
                                                    .get('networkSettings', {}).get('infrastructurePublicIPSettings', {})
                                                    .get('createPublicIPAddress', False))

                    # Infrastructure network topology settings
                    self._workload_server_group = (self._cleanroom_target_properties.get('infrastructure', {})
                                                   .get('networkTopologySettings', {}).get('workloadServerGroup', {})
                                                   .get('name', ''))
                    self._infra_server_group_name = (self._cleanroom_target_properties.get('infrastructure', {})
                                                     .get('networkTopologySettings', {}).get('infrastructureServerGroup', {})
                                                     .get('name', ''))
                    self._infra_network_gateway = (self._cleanroom_target_properties.get('infrastructure', {})
                                                   .get('networkTopologySettings', {}).get('infrastructureNetworkGateway', ''))

                    # Infrastructure advanced settings
                    self._infra_iam_role = (self._cleanroom_target_properties.get('infrastructure', {})
                                            .get('advancedSettings', {}).get('iamRole', {}).get('guid', ''))
                    self._infra_vm_size = (self._cleanroom_target_properties.get('infrastructure', {})
                                           .get('advancedSettings', {}).get('vmSize', {}).get('guid', ''))
                    self._custom_images = (self._cleanroom_target_properties.get('infrastructure', {})
                                           .get('advancedSettings', {}).get('customImages', []))

                    # Advanced network address space
                    self._networkAddressSpace = (self._cleanroom_target_properties.get('advanced', {})
                                                 .get('networkAddressSpace', {}))
                    self._endpointSubnet = (self._cleanroom_target_properties.get('advanced', {})
                                            .get('networkAddressSpace', {}).get('endpointSubnet', ''))
                    self._publicSubnet = (self._cleanroom_target_properties.get('advanced', {})
                                          .get('networkAddressSpace', {}).get('publicSubnet', ''))

                    # Security group rules
                    self._recovery_SecurityRules = (self._cleanroom_target_properties.get('advanced', {})
                                                    .get('securityGroupRules', {}).get('recoveredEntity', []))
                    self._infra_SecurityRules = (self._cleanroom_target_properties.get('advanced', {})
                                                 .get('securityGroupRules', {}).get('infrastructure', []))

                if self._policy_type == 7:
                    self._region = (self._cleanroom_target_properties.get('recovery', {})
                                    .get('region', {})
                                    .get('guid', ''))
                    self._availability_zone = (self._cleanroom_target_properties.get('recovery', {})
                                               .get('availabilityZone', {}).get('guid', ''))
                    self._storage_account = (self._cleanroom_target_properties.get("recovery", {})
                                             .get("storageAccount", {}).get("guid", ''))

                    self._vm_size = (self._cleanroom_target_properties.get('recovery', {}).get("vmSize", {})
                                     .get("guid"))
                    self._disk_type = (self._cleanroom_target_properties.get('recovery', {})
                                       .get('storageType').get('guid', ''))
                    self._virtual_network = (self._cleanroom_target_properties.get('recovery', {})
                                             .get('virtualNetwork', {})
                                             .get('name', ''))
                    self._security_group = (self._cleanroom_target_properties.get('recovery', {})
                                            .get('securityGroup', {})
                                            .get('name', ''))
                    self._resource_group = (self._cleanroom_target_properties.get('recovery', {})
                                            .get('resourceGroup', {})
                                            .get('guid', ''))
                    self._create_public_ip = (self._cleanroom_target_properties.get('recovery', {})
                                              .get('createPublicIPAddress'))
                    # infrastructure network settings
                    self._maxNoOfAccessNodes = (self._cleanroom_target_properties.get('infrastructure', {})
                                                .get('maxNoOfAccessNodes', ''))
                    self._infra_virtual_network = (self._cleanroom_target_properties.get('infrastructure', {})
                                                   .get('networkSettings', {}).get('virtualNetwork', {})
                                                   .get('name', ''))
                    self._infra_security_group = (self._cleanroom_target_properties.get('infrastructure', {})
                                                  .get('networkSettings', {}).get('securityGroup', {})
                                                  .get('name', ''))
                    self._natGatewayPublicIPSettings = (self._cleanroom_target_properties.get('infrastructure', {})
                                                        .get('networkSettings', {}).get("natGatewayPublicIPSettings",
                                                                                        {})
                                                        .get('ipPrefix', {}).get('guid', ""))
                    self._infraPublicIPprefix = (self._cleanroom_target_properties.get('infrastructure', {})
                                                 .get('networkSettings', {}).get("infrastructurePublicIPSettings", {})
                                                 .get('ipPrefix', {}).get('guid', ""))
                    self._infraPublicIP = (self._cleanroom_target_properties.get('infrastructure', {})
                                           .get('networkSettings', {}).get("infrastructurePublicIPSettings", {})
                                           .get('createPublicIPAddress', ""))
                    # infrastructure advanced settings

                    self._infra_server_group_name = (self._cleanroom_target_properties.get('infrastructure', {})
                                                     .get('networkTopologySettings', {}).get('infrastructureServerGroup', {})
                                                     .get('name', ''))
                    self._infra_resourceGroup = (self._cleanroom_target_properties.get('infrastructure', {})
                                                 .get('advancedSettings', {}).get('resourceGroup', {}).get('name', ''))
                    self._infra_vm_size = (self._cleanroom_target_properties.get('infrastructure', {})
                                          .get('advancedSettings', {}).get("vmSize", {}).get('guid', ""))
                    self._custom_images = (self._cleanroom_target_properties.get('infrastructure', {})
                                          .get('advancedSettings', {}).get("customImages", [{}]))

                    # advanced settings

                    self._networkAddressSpace = (
                        self._cleanroom_target_properties.get('advanced', {}).get("networkAddressSpace", {}))
                    self._deployBastion = (self._cleanroom_target_properties.get('advanced', {})
                                           .get("networkAddressSpace", {}).get("deploySecureConnection", ""))
                    self._recovery_SecurityRules = (self._cleanroom_target_properties.get('advanced', {})
                                                    .get("securityGroupRules", {}).get("recoveredEntity", [{}]))
                    self._infra_SecurityRules = (self._cleanroom_target_properties.get('advanced', {})
                                                 .get("securityGroupRules", {}).get("infrastructure", [{}]))
                self._infra_server_group_id = (self._cleanroom_target_properties.get('infrastructure', {})
                                               .get('networkTopologySettings', {}).get('infrastructureServerGroup', {})
                                               .get('id'))

                if self._policy_type == 0:
                    recovery = self._cleanroom_target_properties.get('recovery', {})
                    self._esx_server = recovery.get('esxServer', {}).get('name', '')
                    self._datastore = recovery.get('dataStore', {}).get('name', '')
                    self._destination_network = recovery.get('destinationNetwork', {}).get('name', '')
                    self._resource_pool = recovery.get('resourcePool', {}).get('name', '')
                    self._folder_path = recovery.get('folderPath', {}).get('name', '')
                    self._storage_policy_name = recovery.get('storagePolicy', {}).get('name', '')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def cleanroom_target_id(self) -> str:
        """Get the unique identifier of the cleanroom target.

        Returns:
            The ID of the cleanroom target as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> target_id = target.cleanroom_target_id  # Access the property
            >>> print(f"Cleanroom Target ID: {target_id}")

        #ai-gen-doc
        """
        return self._cleanroom_target_id

    @property
    def cleanroom_target_name(self) -> str:
        """Get the display name of the cleanroom target.

        Returns:
            The display name of the cleanroom target as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> name = target.cleanroom_target_name  # Use dot notation for property access
            >>> print(f"Cleanroom target name: {name}")

        #ai-gen-doc
        """
        return self._cleanroom_target_name

    @property
    def policy_type(self) -> str:
        """Get the policy type ID associated with this cleanroom target.

        The policy type ID indicates the platform for which the cleanroom target is configured:
            1  - AWS
            2  - Microsoft Hyper-V
            7  - Azure
            13 - VMware

        Returns:
            The policy type ID as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> policy_id = target.policy_type
            >>> print(f"Policy type ID: {policy_id}")
            >>> # Output might be: Policy type ID: 1

        #ai-gen-doc
        """
        return self._policy_type

    @property
    def target_instance(self) -> str:
        """Get the name of the target instance for this CleanroomTarget.

        Returns:
            The target instance name as a string. Possible values include:
                - "Instance1"
                - "Instance2"
                - "Instance3"

        Example:
            >>> cleanroom_target = CleanroomTarget()
            >>> instance = cleanroom_target.target_instance  # Access the target instance property
            >>> print(f"Target instance: {instance}")

        #ai-gen-doc
        """
        return self._instance

    @property
    def application_type(self) -> str:
        """Get the name of the application type for this CleanroomTarget.

        Returns:
            The application type as a string. Possible values:
                - "0": Replication type
                - "1": Regular type

        Example:
            >>> target = CleanroomTarget()
            >>> app_type = target.application_type
            >>> print(f"Application type: {app_type}")
            # Output might be "0" for Replication type or "1" for Regular type

        #ai-gen-doc
        """
        return self._application_type

    @property
    def destination_hypervisor(self) -> str:
        """Get the client name of the destination hypervisor.

        Returns:
            The client name of the destination hypervisor as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> hypervisor_name = target.destination_hypervisor  # Use dot notation for property access
            >>> print(f"Destination hypervisor: {hypervisor_name}")

        #ai-gen-doc
        """
        return self._destination_hypervisor

    @property
    def access_node(self) -> str:
        """Get the client name of the access node (proxy) for the cleanroom target.

        Returns:
            The client name of the access node or proxy as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> node_name = target.access_node
            >>> print(f"Access node: {node_name}")

        #ai-gen-doc
        """
        return self._access_node

    @property
    def access_node_client_group(self) -> str:
        """Get the client group name set on the access node field of the cleanroom target.

        Returns:
            The name of the client group configured as the access node for this cleanroom target.

        Example:
            >>> target = CleanroomTarget()
            >>> group_name = target.access_node_client_group  # Use dot notation for property access
            >>> print(f"Access node client group: {group_name}")

        #ai-gen-doc
        """
        return self._access_node_client_group

    @property
    def security_user_names(self) -> list:
        """Get the list of user names used for ownership of the hypervisor and virtual machines.

        Returns:
            list: A list of strings representing the user names associated with the ownership of the hypervisor and VMs.

        Example:
            >>> target = CleanroomTarget()
            >>> user_names = target.security_user_names
            >>> print(user_names)
            ['admin', 'backup_user', 'vm_owner']

        #ai-gen-doc
        """
        return [user['userName'] for user in self._users]

    @property
    def vm_prefix(self) -> str:
        """Get the prefix to be used for the destination VM name.

        Returns:
            The string prefix that will be added to the destination VM's name.

        Example:
            >>> target = CleanroomTarget()
            >>> prefix = target.vm_prefix
            >>> print(f"VMs will be created with prefix: {prefix}")

        #ai-gen-doc
        """
        return self._vm_prefix

    @property
    def vm_suffix(self) -> str:
        """Get the suffix to be appended to the destination VM name.

        Returns:
            The suffix string that will be added to the destination VM's name.

        Example:
            >>> target = CleanroomTarget()
            >>> suffix = target.vm_suffix  # Use dot notation for property access
            >>> print(f"VM name suffix: {suffix}")

        #ai-gen-doc
        """
        return self._vm_suffix

    @property
    def is_automatic_site(self) -> bool:
        """Get the status of the resource provisioning option for this CleanroomTarget
        Returns:
            The status of the resource provisioning option,
            if create new returns True if it is manually managed returns False
        Example:
            >>> target = CleanroomTarget()
            >>> deploy_status = target.is_automatic_site
            >>> print(f"Deploy cleanroom resources: {deploy_status}")
        #ai-gen-doc
        """
        return self._is_automatic_site

    @property
    def storage_account(self) -> str:
        """Get the Azure storage account name used for VM storage deployment.

        Returns:
            The name of the Azure storage account as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> account_name = target.storage_account
            >>> print(f"Storage account: {account_name}")

        #ai-gen-doc
        """
        return self._storage_account

    @property
    def region(self) -> str:
        """Get the Azure cleanroom target region for the destination VM.

        Returns:
            The region name as a string where the cleanroom target VM will be deployed in Azure.

        Example:
            >>> target = CleanroomTarget()
            >>> azure_region = target.region
            >>> print(f"Cleanroom target region: {azure_region}")

        #ai-gen-doc
        """
        return self._region

    @property
    def availability_zone(self) -> str:
        """Get the cleanroom target availability zone for the destination VM in Azure.

        Returns:
            The availability zone as a string for the cleanroom target in Azure.

        Example:
            >>> target = CleanroomTarget()
            >>> zone = target.availability_zone
            >>> print(f"Availability Zone: {zone}")

        #ai-gen-doc
        """
        return self._availability_zone

    @property
    def virtual_network(self) -> str:
        """Get the cleanroom target virtual network for the destination VM in Azure.

        Returns:
            The name or identifier of the Azure virtual network associated with the cleanroom target.

        Example:
            >>> target = CleanroomTarget()
            >>> vnet = target.virtual_network
            >>> print(f"Cleanroom target virtual network: {vnet}")

        #ai-gen-doc
        """
        return self._virtual_network

    @property
    def security_group(self) -> str:
        """Get the security group associated with the cleanroom target for the destination VM in Azure.

        Returns:
            The name or identifier of the Azure security group assigned to the cleanroom target's destination VM.

        Example:
            >>> target = CleanroomTarget()
            >>> sg = target.security_group
            >>> print(f"Security group: {sg}")

        #ai-gen-doc
        """
        return self._security_group

    @property
    def resource_group(self) -> str:
        """Get the Azure resource group name for the cleanroom target destination VM.

        Returns:
            The name of the Azure resource group as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> group = target.resource_group
            >>> print(f"Resource group: {group}")

        #ai-gen-doc
        """
        return self._resource_group

    @property
    def create_public_ip(self) -> str:
        """Get the public IP group name created for the destination VM in Azure.

        Returns:
            The name of the public IP group associated with the cleanroom target for the destination virtual machine.

        Example:
            >>> target = CleanroomTarget()
            >>> public_ip_group = target.create_public_ip
            >>> print(f"Public IP group: {public_ip_group}")

        #ai-gen-doc
        """
        return self._create_public_ip

    @property
    def vm_size(self) -> str:
        """Get the Azure VM size for the cleanroom target destination VM.

        Returns:
            The VM size as a string, representing the Azure VM size configured for the cleanroom target.

        Example:
            >>> target = CleanroomTarget()
            >>> size = target.vm_size
            >>> print(f"Cleanroom target VM size: {size}")

        #ai-gen-doc
        """
        return self._vm_size

    @property
    def deployBastion(self) -> bool:
        """Indicate whether the deploy bastion feature is enabled for this CleanroomTarget.

        Returns:
            True if deploy bastion is enabled; False otherwise.

        Example:
            >>> target = CleanroomTarget()
            >>> if target.deployBastion:
            ...     print("Deploy bastion is enabled.")
            ... else:
            ...     print("Deploy bastion is disabled.")

        #ai-gen-doc
        """
        return self._deployBastion

    @property
    def custom_image(self) -> list:
        """Get the list of custom images configured for the cleanroom target.

        Returns:
            list: A list containing the custom images set on the target.

        Example:
            >>> target = CleanroomTarget()
            >>> images = target.custom_image
            >>> print(f"Custom images: {images}")

        #ai-gen-doc
        """
        return self._custom_images

    @property
    def infra_virtual_network(self) -> str:
        """Get the name of the infrastructure virtual network associated with this CleanroomTarget.

        Returns:
            The name of the infra virtual network as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> network_name = target.infra_virtual_network  # Use dot notation for property access
            >>> print(f"Infrastructure virtual network: {network_name}")

        #ai-gen-doc
        """
        return self._infra_virtual_network

    @property
    def infra_security_group(self) -> str:
        """Get the name of the infrastructure security group associated with this cleanroom target.

        Returns:
            The name of the infra security group as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> group_name = target.infra_security_group
            >>> print(f"Infrastructure security group: {group_name}")

        #ai-gen-doc
        """
        return self._infra_security_group

    @property
    def natGatewayPublicIPSettings(self) -> dict:
        """Get the NAT gateway public IP settings for the cleanroom target.

        Returns:
            dict: A dictionary containing the NAT gateway public IP configuration details.

        Example:
            >>> target = CleanroomTarget()
            >>> nat_settings = target.natGatewayPublicIPSettings
            >>> print(nat_settings)
            {'publicIP': '203.0.113.42', 'allocationMethod': 'Static'}

        #ai-gen-doc
        """
        return self._natGatewayPublicIPSettings

    @property
    def infraPublicIPprefix(self) -> str:
        """Get the public IP prefix associated with the cleanroom infrastructure.

        Returns:
            The public IP prefix as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> ip_prefix = target.infraPublicIPprefix
            >>> print(f"Infrastructure public IP prefix: {ip_prefix}")

        #ai-gen-doc
        """
        return self._infraPublicIPprefix

    @property
    def infrapublicip(self) -> bool:
        """Indicate whether public IP creation is enabled for the infrastructure.

        Returns:
            bool: True if creating a public IP is enabled for the infrastructure, False otherwise.

        Example:
            >>> target = CleanroomTarget()
            >>> if target.infrapublicip:
            ...     print("Public IP creation is enabled for Infra")
            ... else:
            ...     print("Public IP creation is not enabled for Infra")

        #ai-gen-doc
        """
        return self._infraPublicIP

    @property
    def infra_server_group(self) -> str:
        """Get the server group used for autoscale operations.

        Returns:
            The name of the server group that will be utilized in autoscale scenarios.

        Example:
            >>> target = CleanroomTarget()
            >>> group_name = target.infra_server_group
            >>> print(f"Autoscale server group: {group_name}")

        #ai-gen-doc
        """
        return self._infra_server_group_name

    @property
    def infra_server_group_id(self) -> int:
        """Get the ID of the infrastructure server group used for autoscale operations.

        Returns:
            The ID of the infrastructure server group

        Example:
            >>> target = CleanroomTarget()
            >>> group_id = target.infra_server_group_id
            >>> print(f"Infrastructure server group ID: {group_id}")

        #ai-gen-doc
        """
        return self._infra_server_group_id

    @property
    def infra_resource_group(self) -> str:
        """Get the name of the resource group where the autoscale node will be created.

        Returns:
            The name of the resource group as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> group_name = target.infra_resource_group
            >>> print(f"Autoscale node will be created in: {group_name}")

        #ai-gen-doc
        """
        return self._infra_resourceGroup

    @property
    def infra_vm_size(self) -> str:
        """Get the name of the virtual machine size used for infrastructure.

        Returns:
            str: The name of the VM size configured for infrastructure purposes.

        Example:
            >>> target = CleanroomTarget()
            >>> vm_size = target.infra_vm_size  # Use dot notation for property access
            >>> print(f"Infrastructure VM size: {vm_size}")

        #ai-gen-doc
        """
        return self._infra_vm_size

    @property
    def networkAddressSpace(self) -> dict:
        """Get the address space configuration for the virtual network and its subnets.

        Returns:
            dict: A dictionary containing address space details for the vnet and subnets,
            including recovery entity, infrastructure, and bastion subnets.

        Example:
            >>> target = CleanroomTarget()
            >>> address_space = target.networkAddressSpace
            >>> print(address_space)
            {'vnet': '10.0.0.0/16', 'recovery_entity': '10.0.1.0/24', 'infra': '10.0.2.0/24', 'bastion': '10.0.3.0/24'}

        #ai-gen-doc
        """
        return self._networkAddressSpace

    @property
    def iam_role(self) -> str:
        """Get the IAM role name used for the cleanroom Recovery Group.

        Returns:
            The IAM role name as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> role_name = target.iam_role  # Access the IAM role property
            >>> print(f"IAM Role: {role_name}")
        #ai-gen-doc
        """
        return self._iam_role

    @property
    def encryption_key(self) -> str:
        """Get the name of the encryption key used for the cleanroom Recovery Group.

        Returns:
            The name of the encryption key as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> key_name = target.encryption_key
            >>> print(f"Encryption key name: {key_name}")

        #ai-gen-doc
        """
        return self._encryption_key

    @property
    def instance_type(self) -> str:
        """Get the instance type of the cleanroom Recovery Group.

        Returns:
            The instance type as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> print(target.instance_type)
            >>> # Output might be: 'EC2', 'VMware', etc.

        #ai-gen-doc
        """
        return self._instance_type

    @property
    def volume_type(self) -> str:
        """Get the volume type of the cleanroom Recovery Group.

        Returns:
            The volume type as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> vtype = target.volume_type
            >>> print(f"Volume type: {vtype}")

        #ai-gen-doc
        """
        return self._volume_type

    @property
    def network_subnet(self) -> str:
        """Get the network subnet associated with the cleanroom Recovery Group.

        Returns:
            The network subnet as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> subnet = target.network_subnet
            >>> print(f"Cleanroom network subnet: {subnet}")

        #ai-gen-doc
        """
        return self._network_subnet

    @property
    def key_pair(self) -> str:
        """Get the name of the key pair used for the cleanroom Recovery Group.

        Returns:
            The key pair name as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> key_name = target.key_pair  # Access the key pair property
            >>> print(f"Key pair name: {key_name}")

        #ai-gen-doc
        """
        return self._key_pair

    @property
    def esx_server(self) -> str:
        """Get the ESX server name for the VMware cleanroom target."""
        return self._esx_server

    @property
    def datastore(self) -> str:
        """Get the datastore name for the VMware cleanroom target."""
        return self._datastore

    @property
    def destination_network(self) -> str:
        """Get the destination network name for the VMware cleanroom target."""
        return self._destination_network

    @property
    def resource_pool(self) -> str:
        """Get the resource pool name for the VMware cleanroom target."""
        return self._resource_pool

    @property
    def folder_path(self) -> str:
        """Get the VM folder path for the VMware cleanroom target."""
        return self._folder_path

    @property
    def storage_policy_name(self) -> str:
        """Get the storage policy name for the VMware cleanroom target."""
        return self._storage_policy_name

    @property
    def vpc(self) -> str:
        """Get the AWS VPC name for the cleanroom target.

        Returns:
            The VPC name as a string for AWS cleanroom target.

        Example:
            >>> target = CleanroomTarget()
            >>> vpc_name = target.vpc
            >>> print(f"VPC: {vpc_name}")

        #ai-gen-doc
        """
        return getattr(self, '_vpc', None)

    @property
    def security_groups(self) -> list:
        """Get the list of AWS security groups for the cleanroom target.

        Returns:
            List of security groups for AWS cleanroom target.

        Example:
            >>> target = CleanroomTarget()
            >>> sgs = target.security_groups
            >>> print(f"Security groups: {sgs}")

        #ai-gen-doc
        """
        return getattr(self, '_security_groups', [])

    @property
    def workload_server_group(self) -> str:
        """Get the AWS workload server group name for the cleanroom target.

        Returns:
            The workload server group name as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> wsg = target.workload_server_group
            >>> print(f"Workload server group: {wsg}")

        #ai-gen-doc
        """
        return getattr(self, '_workload_server_group', None)

    @property
    def infra_network_gateway(self) -> str:
        """Get the AWS infrastructure network gateway for the cleanroom target.

        Returns:
            The infrastructure network gateway as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> gateway = target.infra_network_gateway
            >>> print(f"Infrastructure network gateway: {gateway}")

        #ai-gen-doc
        """
        return getattr(self, '_infra_network_gateway', '')

    @property
    def infra_iam_role(self) -> str:
        """Get the AWS infrastructure IAM role for the cleanroom target.

        Returns:
            The infrastructure IAM role as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> role = target.infra_iam_role
            >>> print(f"Infrastructure IAM role: {role}")

        #ai-gen-doc
        """
        return getattr(self, '_infra_iam_role', None)

    @property
    def infra_security_groups(self) -> list:
        """Get the list of AWS infrastructure security groups for the cleanroom target.

        Returns:
            List of infrastructure security groups.

        Example:
            >>> target = CleanroomTarget()
            >>> infra_sgs = target.infra_security_groups
            >>> print(f"Infrastructure security groups: {infra_sgs}")

        #ai-gen-doc
        """
        return getattr(self, '_infra_security_groups', [])

    @property
    def infra_create_public_ip(self) -> bool:
        """Get whether to create public IP for AWS infrastructure.

        Returns:
            Boolean indicating if public IP should be created for infrastructure.

        Example:
            >>> target = CleanroomTarget()
            >>> create_ip = target.infra_create_public_ip
            >>> print(f"Create infrastructure public IP: {create_ip}")

        #ai-gen-doc
        """
        return getattr(self, '_infra_create_public_ip', False)

    @property
    def infra_vpc(self) -> str:
        """Get the AWS infrastructure VPC name for the cleanroom target.

        Returns:
            The infrastructure VPC name as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> infra_vpc_name = target.infra_vpc
            >>> print(f"Infrastructure VPC: {infra_vpc_name}")

        #ai-gen-doc
        """
        return getattr(self, '_infra_vpc', None)

    @property
    def endpoint_subnet(self) -> str:
        """Get the AWS endpoint subnet for the cleanroom target.

        Returns:
            The endpoint subnet CIDR as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> subnet = target.endpoint_subnet
            >>> print(f"Endpoint subnet: {subnet}")

        #ai-gen-doc
        """
        return getattr(self, '_endpointSubnet', '')

    @property
    def public_subnet(self) -> str:
        """Get the AWS public subnet for the cleanroom target.

        Returns:
            The public subnet CIDR as a string.

        Example:
            >>> target = CleanroomTarget()
            >>> subnet = target.public_subnet
            >>> print(f"Public subnet: {subnet}")

        #ai-gen-doc
        """
        return getattr(self, '_publicSubnet', '')

    def edit_cleanroom_site(self, edit_fields: dict) -> dict:
        """Edit this cleanroom site via ``PUT Cleanroom/Target/{id}``.

        Fetches the current configuration, applies *edit_fields* for
        the appropriate vendor (determined by :attr:`policy_type`), then
        PUTs the updated payload back.  Calls :meth:`refresh` afterwards.

        Common keys (all vendors):
            - ``name``   (str)  -- New display name for the site.
            - ``suffix`` (str)  -- New VM display-name suffix.

        VMware-specific keys (policy_type == 0):
            - ``destination_network`` (dict) ``{name, guid, type}``
            - ``resource_pool``       (dict) ``{name, guid, type}``
            - ``folder_path``         (dict) ``{name, guid, type}``
            - ``storage_policy``      (dict) ``{name, type}``

        Azure-specific keys (policy_type == 7):
            - ``region``           (dict) ``{guid, name, type}``
            - ``storage_account``  (dict) ``{guid, name}``
            - ``virtual_network``  (dict) ``{guid, name}``
            - ``security_group``   (dict) ``{guid, name}``
            - ``resource_group``   (dict) ``{guid, name}``
            - ``vm_size``          (dict) ``{guid, name}``
            - ``availability_zone`` (dict) ``{guid, name}``

        AWS-specific keys (policy_type == 1):
            - ``region``           (dict) ``{guid, name}``
            - ``vpc``              (dict) ``{guid, name}``
            - ``security_groups``  (list)
            - ``instance_type``    (dict) ``{guid, name}``
            - ``volume_type``      (str)
            - ``key_pair``         (dict) ``{name}``
            - ``iam_role``         (dict) ``{guid, name}``
            - ``encryption_key``   (dict) ``{guid, name}``
            - ``availability_zone`` (dict) ``{guid, name}``

        Args:
            edit_fields: Dict of fields to change.

        Returns:
            dict: API response body (may be empty for 204 responses).

        Raises:
            SDKException: If the GET or PUT request fails.
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RUNBOOK_TARGET_API)
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))
        if not response.json():
            raise SDKException('Response', '102', 'Empty response received from server')

        payload = response.json()

        # --- Common fields (all vendors) ---
        if 'name' in edit_fields:
            payload.setdefault('general', {}).setdefault('target', {})['name'] = edit_fields['name']
            self._cleanroom_target_name = edit_fields['name'].lower()

        if 'suffix' in edit_fields:
            payload.setdefault('general', {}).setdefault('entityDisplayName', {})['suffix'] = edit_fields['suffix']

        recovery = payload.setdefault('recovery', {})

        # --- VMware (policy_type == 0) ---
        if self._policy_type == 0:
            if 'destination_network' in edit_fields:
                recovery['destinationNetwork'] = edit_fields['destination_network']
            if 'resource_pool' in edit_fields:
                recovery['resourcePool'] = edit_fields['resource_pool']
            if 'folder_path' in edit_fields:
                recovery['folderPath'] = edit_fields['folder_path']
            if 'storage_policy' in edit_fields:
                recovery['storagePolicy'] = edit_fields['storage_policy']

        # --- Azure (policy_type == 7) ---
        elif self._policy_type == 7:
            if 'region' in edit_fields:
                recovery['region'] = edit_fields['region']
            if 'storage_account' in edit_fields:
                recovery['storageAccount'] = edit_fields['storage_account']
            if 'virtual_network' in edit_fields:
                recovery['virtualNetwork'] = edit_fields['virtual_network']
            if 'security_group' in edit_fields:
                recovery['securityGroup'] = edit_fields['security_group']
            if 'resource_group' in edit_fields:
                recovery['resourceGroup'] = edit_fields['resource_group']
            if 'vm_size' in edit_fields:
                recovery['vmSize'] = edit_fields['vm_size']
            if 'availability_zone' in edit_fields:
                recovery['availabilityZone'] = edit_fields['availability_zone']

        # --- AWS (policy_type == 1) ---
        elif self._policy_type == 1:
            if 'region' in edit_fields:
                recovery['region'] = edit_fields['region']
            if 'vpc' in edit_fields:
                recovery['vpc'] = edit_fields['vpc']
            if 'security_groups' in edit_fields:
                recovery['securityGroups'] = edit_fields['security_groups']
            if 'instance_type' in edit_fields:
                recovery['instanceType'] = edit_fields['instance_type']
            if 'volume_type' in edit_fields:
                recovery['volumeType'] = edit_fields['volume_type']
            if 'key_pair' in edit_fields:
                recovery['keyPair'] = edit_fields['key_pair']
            if 'iam_role' in edit_fields:
                recovery['iamRole'] = edit_fields['iam_role']
            if 'encryption_key' in edit_fields:
                recovery['encryptionKey'] = edit_fields['encryption_key']
            if 'availability_zone' in edit_fields:
                recovery['availabilityZone'] = edit_fields['availability_zone']

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._EDIT_RUNBOOK_TARGET_API, payload=payload
        )
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        self.refresh()
        try:
            return response.json() if response.text else {}
        except JSONDecodeError:
            return {}

    def refresh(self) -> None:
        """Reload the properties of the cleanroom target.

        This method updates the cleanroom target's properties to reflect the latest state,
        ensuring that any changes made externally are incorporated.

        Example:
            >>> target = CleanroomTarget()
            >>> target.refresh()
            >>> print("Cleanroom target properties refreshed.")

        #ai-gen-doc
        """
        self._get_cleanroom_target_properties()

    def delete(self) -> bool:
        """Delete the Cleanroom Target.

        This method attempts to delete the Cleanroom Target associated with this instance.
        It returns True if the deletion was successful, or False otherwise.

        Returns:
            bool: True if the Cleanroom Target was deleted successfully, False otherwise.

        Example:
            >>> target = CleanroomTarget()
            >>> success = target.delete()
            >>> print(f"Target deleted: {success}")

        #ai-gen-doc
        """
        return self._delete_cleanroom_target()
