# -*- coding: utf-8 -*-
#
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
#
"""
Main file for performing Cleanroom recovery operations

RecoveryGroups:     Class for representing all the recovery groups

RecoveryGroup:      Class for a single recovery group selected, and to perform operations on that recovery group

"""
from enum import Enum
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from cvpysdk.exception import SDKException

from cvpysdk.cleanroom.target import CleanroomTarget

from .recovery_entities import RecoveryEntities

if TYPE_CHECKING:
    from cvpysdk.commcell import Commcell

WORKLOADS = {
    0: "GENERIC",
    1: "O365",
    2: "SALESFORCE",
    3: "EXCHANGE",
    4: "SHAREPOINT",
    5: "ONEDRIVE",
    6: "TEAMS",
    7: "DYNAMICS_365",
    8: "VIRTUAL SERVER",
    9: "FILE SYSTEM"
}

INSTANCES = {
    'AZURE_V2': 'Azure Resource Manager',
    'AMAZON': 'Amazon Web Services'
}

class RecoveryGroups:
    """
    Manages and represents all cleanroom recovery groups within a CommCell environment.

    This class provides an interface to interact with recovery groups, allowing users to
    query, retrieve, and refresh group information. It supports checking for the existence
    of specific recovery groups, accessing all available groups, and obtaining details
    about individual groups.

    Key Features:
        - Initialization with a CommCell object for context
        - Property to access all recovery groups
        - Check for the existence of a recovery group by name
        - Retrieve details of a specific recovery group
        - Refresh the recovery group information from the source
        - String representation of the recovery groups collection
        - Internal method to fetch recovery group data

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a RecoveryGroups object with the specified Commcell connection.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', '<password>')
            >>> recovery_groups = RecoveryGroups(commcell)
            >>> print("RecoveryGroups object initialized successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object

        self._RECOVERY_GROUPS_URL = commcell_object._services['ALL_RECOVERY_GROUPS']
        self._recovery_groups = None

        self.refresh()

    @property
    def all_groups(self) -> Dict[str, int]:
        """Get a dictionary of all recovery groups and their corresponding IDs.

        Returns:
            Dict[str, int]: A dictionary where each key is the name of a recovery group,
            and each value is the group's unique ID.

        Example:
            >>> recovery_groups = RecoveryGroups(commcell_object)
            >>> groups = recovery_groups.all_groups
            >>> print(groups)
            {'FinanceGroup': 101, 'HRGroup': 102}

        #ai-gen-doc
        """
        return self._recovery_groups

    def has_recovery_group(self, recovery_group_name: str) -> bool:
        """Check if a recovery group with the specified name exists in the Commcell.

        Args:
            recovery_group_name: The name of the recovery group to check.

        Returns:
            True if the recovery group exists in the Commcell, False otherwise.

        Raises:
            SDKException: If the provided recovery_group_name is not a string.

        Example:
            >>> rg = RecoveryGroups(commcell_object)
            >>> exists = rg.has_recovery_group("Finance_Recovery_Group")
            >>> print(f"Recovery group exists: {exists}")
            # Output: Recovery group exists: True

        #ai-gen-doc
        """
        if not isinstance(recovery_group_name, str):
            raise SDKException('RecoveryGroup', '101')

        return self._recovery_groups and recovery_group_name in self._recovery_groups

    def get(self, recovery_group_name: str) -> 'RecoveryGroup':
        """Retrieve a recovery group object by its name.

        Args:
            recovery_group_name: The name of the recovery group to retrieve.

        Returns:
            An instance of the recovery group class corresponding to the specified group name.

        Raises:
            SDKException: If the group name is not a string or if no group exists with the given name.

        Example:
            >>> recovery_groups = RecoveryGroups()
            >>> group = recovery_groups.get("Finance_Backup_Group")
            >>> print(f"Retrieved group: {group}")

        #ai-gen-doc
        """
        if not isinstance(recovery_group_name, str):
            raise SDKException('RecoveryGroup', '101')
        else:
            if self.has_recovery_group(recovery_group_name):
                return RecoveryGroup(
                    self._commcell_object,
                    recovery_group_name,
                    self.all_groups[recovery_group_name]
                )

            raise SDKException('RecoveryGroup', '102',
                               'No recovery group exists with name: {0}'.format(recovery_group_name))

    def refresh(self) -> None:
        """Reload the recovery group information from the Commcell.

        This method refreshes the internal state of the RecoveryGroups object, ensuring that
        any changes to recovery groups on the Commcell are reflected in this instance.

        Example:
            >>> recovery_groups = RecoveryGroups(commcell_object)
            >>> recovery_groups.refresh()
            >>> print("Recovery groups have been refreshed.")

        #ai-gen-doc
        """
        self._recovery_groups = self._get_recovery_groups()

    def __str__(self) -> str:
        """Return a string representation of all recovery groups.

        This method provides a human-readable string that lists all recovery groups
        managed by this RecoveryGroups instance.

        Returns:
            A string containing the names or details of all recovery groups.

        Example:
            >>> recovery_groups = RecoveryGroups(commcell_object)
            >>> print(str(recovery_groups))
            RecoveryGroup1, RecoveryGroup2, RecoveryGroup3

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'RecoveryGroup')

        for index, group in enumerate(self._recovery_groups):
            sub_str = '{:^5}\t{:20}\n'.format(
                index + 1,
                group
            )
            representation_string += sub_str

        return representation_string.strip()

    def _get_recovery_groups(self) -> dict:
        """Retrieve all recovery groups associated with the client.

        Returns:
            dict: A dictionary mapping recovery group names to their corresponding IDs.
                Example:
                    {
                        "group1_name": group1_id,
                        "group2_name": group2_id
                    }

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> recovery_groups = recovery_groups_obj._get_recovery_groups()
            >>> print(recovery_groups)
            {'FinanceGroup': 101, 'HRGroup': 102}

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_GROUPS_URL)

        if flag:
            try:
                json_resp = response.json()

                group_name_id_dict = {group['name']: group['id'] for group in json_resp['recoveryGroups']}

                return group_name_id_dict
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))


class RecoveryStatus(Enum):
    """
    Enumeration representing various recovery statuses.

    This class defines a set of constant values to indicate the status of a recovery process.
    It is intended to be used wherever recovery states need to be tracked or communicated,
    providing a clear and type-safe way to represent different recovery outcomes.

    Key Features:
        - Enumerates recovery status values
        - Ensures type safety and clarity in status representation
        - Facilitates consistent usage of recovery states across the codebase

    #ai-gen-doc
    """
    NO_STATUS = 0
    NONE = 0
    NOT_READY = 1
    READY = 2
    RECOVERED = 3
    FAILED = 4
    RECOVERED_WITH_ERRORS = 5
    IN_PROGRESS = 6
    CLEANED_UP = 7
    MARK_AS_FAILED = 8
    CLEANUP_FAILED = 9

class RecoveryStatusNotReadyCategory(Enum):
    """
    Enumeration for recovery status categories indicating 'not ready' states.

    This Enum class is used to represent various categories or reasons why a recovery
    process may be considered 'not ready'. It provides a structured way to classify
    and handle different 'not ready' statuses within recovery workflows.

    Key Features:
        - Defines distinct 'not ready' recovery status categories
        - Facilitates clear status management in recovery processes
        - Enables type-safe usage of recovery status categories

    #ai-gen-doc
    """
    NONE = 0
    INVALID_VM_NAME = 1
    INVALID_COPY = 2
    MARK_AS_FAILED = 4
    V1_INDEXING_NOT_SUPPORTED = 16
    INVALID_SMART_FOLDER = 8
    LAST_BACKUP_OUTDATED = 32
    LAST_BACKUP_NOT_READY = 64
    MANAGED_IDENTITY_ENABLED = 128
    AUTOSCALING_DISABLED = 256

class RecoveryGroup:
    """
    Class for managing and performing operations on a recovery group.

    The RecoveryGroup class provides a comprehensive interface for interacting with
    recovery groups, including accessing their properties, managing associated entities,
    and performing recovery actions. It supports threat scanning, Windows Defender scanning,
    and cleanup operations for recovered entities. The class also allows validation of
    new recovery targets and hypervisors, and provides access to related resources such as
    security groups, virtual networks, resource groups, and storage accounts.

    Key Features:
        - Initialization with commcell object, recovery group name, and ID
        - Access to recovery group properties (ID, name, target name, entities, etc.)
        - Management of recovery entities and their statuses
        - Threat scan and Windows Defender scan enablement checks
        - Power-off option for destination VMs post-recovery
        - Entity recovery operations (recover all, recover specific entities)
        - Threat count retrieval for entities
        - Refresh and update recovery group properties
        - Validation of new recovery targets and hypervisors
        - Cleanup of recovered entities
        - Deletion of recovery group

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', recovery_group_name: str, recovery_group_id: Optional[str] = None) -> None:
        """Initialize a RecoveryGroup instance.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            recovery_group_name: The name of the recovery group to manage.
            recovery_group_id: Optional; the unique identifier of the recovery group. If not provided, it may be determined automatically.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> recovery_group = RecoveryGroup(commcell, 'Finance_Recovery_Group')
            >>> # With a specific recovery group ID
            >>> recovery_group = RecoveryGroup(commcell, 'Finance_Recovery_Group', recovery_group_id='12345')

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self.recovery_group_name = recovery_group_name
        if recovery_group_id is not None:
            self._recovery_group_id = str(recovery_group_id)
        else:
            # get id from RecoveryGroups class
            self._recovery_group_id = RecoveryGroups(commcell_object).all_groups[recovery_group_name]
        self._RECOVERY_GROUP_URL = commcell_object._services['RECOVERY_GROUP'] % self._recovery_group_id
        self._RECOVER_URL = commcell_object._services['RECOVERY_GROUP_RECOVER'] % self._recovery_group_id
        self._RECOVERY_GROUP_THREATS_COUNT = commcell_object._services['RECOVERY_GROUP_THREATS_COUNT'] % self._recovery_group_id

        # will be set when refresh is called
        self._properties = None
        self.refresh()
        self._recovery_entities = RecoveryEntities(self, self._commcell_object)
        self._recovery_target = CleanroomTarget(self._commcell_object, self.target_name)

    @property
    def recovery_entities(self) -> 'RecoveryEntities':
        """Get the RecoveryEntities manager associated with this RecoveryGroup.

        This property provides access to the RecoveryEntities manager, which can be used to create and manage individual RecoveryEntity objects within the recovery group.

        Returns:
            RecoveryEntities: The manager object for handling RecoveryEntity instances.

        Example:
            >>> recovery_group = RecoveryGroup(commcell_object, group_id)
            >>> entities_manager = recovery_group.recovery_entities
            >>> print(f"RecoveryEntities manager: {entities_manager}")
            >>> # Use entities_manager to create or manage RecoveryEntity objects

        #ai-gen-doc
        """
        return self._recovery_entities

    @property
    def id(self) -> int:
        """Get the unique identifier of the recovery group.

        Returns:
            The recovery group ID as an integer.

        Example:
            >>> rg = RecoveryGroup()
            >>> group_id = rg.id  # Access the recovery group ID using the property
            >>> print(f"Recovery Group ID: {group_id}")

        #ai-gen-doc
        """
        return int(self._recovery_group_id)

    @property
    def name(self) -> str:
        """Get the name of the recovery group.

        Returns:
            The name of this RecoveryGroup as a string.

        Example:
            >>> rg = RecoveryGroup()
            >>> group_name = rg.name  # Access the name property
            >>> print(f"Recovery group name: {group_name}")

        #ai-gen-doc
        """
        return self.recovery_group_name

    @property
    def target_name(self) -> str:
        """Get the name of the target associated with this RecoveryGroup.

        Returns:
            The target name as a string.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> name = recovery_group.target_name
            >>> print(f"Target name: {name}")

        #ai-gen-doc
        """
        return self.entities[0]['target']['name']

    @property
    def is_rescued_cs(self):
        """Check if the recovery group is a rescued cleanroom.

        Returns:
            True if the recovery group is a rescued cleanroom, False otherwise.

        Example:
            >>> rg = RecoveryGroup()
            >>> if rg.is_Rescued_cs:
            ...     print("This recovery group is a rescued cleanroom.")
            ... else:
            ...     print("This recovery group is not a rescued cleanroom.")

        #ai-gen-doc
        """
        return self._properties['recoveryGroup']['recoveryExpirationOptions']['isRescuedCommServe']

    @property
    def entities(self) -> List[Dict[str, Any]]:
        """Get all entity properties in the recovery group.

        Returns:
            A list of dictionaries, each containing the properties of an entity within the recovery group.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> entity_list = recovery_group.entities
            >>> print(f"Number of entities: {len(entity_list)}")
            >>> for entity in entity_list:
            ...     print(entity)

        #ai-gen-doc
        """
        return self._properties['entities']

    @property
    def entities_list(self) -> list:
        """Get the list of all entities in the recovery group.

        Returns:
            list: A list containing all entities that are part of this recovery group.

        Example:
            >>> rg = RecoveryGroup()
            >>> entities = rg.entities_list  # Use dot notation to access the property
            >>> print(f"Entities in the recovery group: {entities}")

        #ai-gen-doc
        """
        entity_list = []
        for entity in self.entities:
            entity_list.append(entity['name'])
        return entity_list

    @property
    def entities_id(self) -> List[int]:
        """Get the list of entity IDs in the recovery group.

        Returns:
            List[int]: A list containing the IDs of all entities that are part of this recovery group.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> entity_ids = recovery_group.entities_id
            >>> print(f"Entity IDs in the group: {entity_ids}")

        #ai-gen-doc
        """
        entity_list_id = []
        for entity in self.entities:
            entity_list_id.append(entity['id'])
        return entity_list_id

    @property
    def vendor_type(self) -> str:
        """Detect the cloud vendor type from the recovery configuration.

        Returns:
            'azure' if Azure configuration is present, 'amazon' if AWS configuration is present.

        Example:
            >>> rg = RecoveryGroup()
            >>> vendor = rg.vendor_type
            >>> print(f"Vendor: {vendor}")

        #ai-gen-doc
        """
        config = self.entities[0]['recoveryConfiguration']['configuration']
        if 'azure' in config:
            return 'azure'
        elif 'amazon' in config:
            return 'amazon'
        else:
            raise SDKException('RecoveryGroup', '102', 'Unknown vendor type in recovery configuration')

    @property
    def security_group(self) -> str:
        """Get the name of the security group associated with this recovery group.

        Returns:
            The security group name/id as a string for Azure, or list of security groups for AWS.

        Example:
            >>> rg = RecoveryGroup()
            >>> group_name = rg.security_group
            >>> print(f"Security group: {group_name}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        config = self.entities[0]['recoveryConfiguration']['configuration'][vendor]

        if vendor == 'azure':
            return config['overrideReplicationOptions']['securityGroup']['id']
        elif vendor == 'amazon':
            return config['overrideReplicationOptions'].get('securityGroups', [])

    @property
    def virtual_network(self) -> str:
        """Get the name of the virtual network associated with this recovery group.

        Returns:
            The name of the virtual network as a string (Azure VNet or AWS VPC/Subnet).

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> vnet_name = recovery_group.virtual_network
            >>> print(f"Virtual Network: {vnet_name}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        config = self.entities[0]['recoveryConfiguration']['configuration'][vendor]

        if vendor == 'azure':
            return config['overrideReplicationOptions']['virtualNetwork']['networkName']
        elif vendor == 'amazon':
            return config['overrideReplicationOptions']['network'].get('name', '')

    @property
    def resource_group(self) -> str:
        """Get the Azure resource group name associated with this RecoveryGroup.

        Returns:
            The name of the Azure resource group as a string, or None for AWS.

        Example:
            >>> rg = RecoveryGroup()
            >>> group_name = rg.resource_group
            >>> print(f"Resource group: {group_name}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'azure':
            return self.entities[0]['recoveryConfiguration']['configuration']['azure']['resourceGroup']
        elif vendor == 'amazon':
            return None  # AWS doesn't have resource groups

    @property
    def storage_account(self) -> str:
        """Get the Azure storage account name used for deploying the VM's storage.

        Returns:
            The name of the Azure storage account as a string, or None for AWS.

        Example:
            >>> rg = RecoveryGroup()
            >>> account_name = rg.storage_account
            >>> print(f"Storage account: {account_name}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'azure':
            return self.entities[0]['recoveryConfiguration']['configuration']['azure']['storageAccount']
        elif vendor == 'amazon':
            return None  # AWS doesn't use storage accounts

    @property
    def instance_type(self) -> str:
        """Get the AWS instance type for the recovery group.

        Returns:
            The AWS instance type as a string, or None for Azure.

        Example:
            >>> rg = RecoveryGroup()
            >>> instance = rg.instance_type
            >>> print(f"Instance type: {instance}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'amazon':
            return self.entities[0]['recoveryConfiguration']['configuration']['amazon'].get('instanceType')
        return None

    @property
    def datacenter(self) -> str:
        """Get the AWS datacenter/region for the recovery group.

        Returns:
            The AWS datacenter/region as a string, or None for Azure.

        Example:
            >>> rg = RecoveryGroup()
            >>> dc = rg.datacenter
            >>> print(f"Datacenter: {dc}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'amazon':
            return self.entities[0]['recoveryConfiguration']['configuration']['amazon'].get('datacenter')
        return None

    @property
    def availability_zone(self) -> str:
        """Get the AWS availability zone for the recovery group.

        Returns:
            The AWS availability zone as a string, or None for Azure.

        Example:
            >>> rg = RecoveryGroup()
            >>> az = rg.availability_zone
            >>> print(f"Availability zone: {az}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'amazon':
            return self.entities[0]['recoveryConfiguration']['configuration']['amazon'].get('availabilityZone')
        return None

    @property
    def subnet_id(self) -> str:
        """Get the subnet ID for the recovery group.

        Returns:
            The subnet ID as a string (Azure subnet_id or AWS subnetId).

        Example:
            >>> rg = RecoveryGroup()
            >>> subnet = rg.subnet_id
            >>> print(f"Subnet ID: {subnet}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        config = self.entities[0]['recoveryConfiguration']['configuration'][vendor]

        if vendor == 'azure':
            return config['overrideReplicationOptions']['virtualNetwork'].get('subnetId', '')
        elif vendor == 'amazon':
            return config['overrideReplicationOptions']['network'].get('subnetId', '')

    @property
    def iam_role(self) -> dict:
        """Get the AWS IAM role for the recovery group.

        Returns:
            The IAM role dictionary, or None for Azure.

        Example:
            >>> rg = RecoveryGroup()
            >>> role = rg.iam_role
            >>> print(f"IAM role: {role}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'amazon':
            return self.entities[0]['recoveryConfiguration']['configuration']['amazon']['overrideReplicationOptions'].get('IAMRole', {})
        return None

    @property
    def key_pair(self) -> str:
        """Get the AWS key pair for the recovery group.

        Returns:
            The AWS key pair name as a string, or None for Azure.

        Example:
            >>> rg = RecoveryGroup()
            >>> kp = rg.key_pair
            >>> print(f"Key pair: {kp}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'amazon':
            return self.entities[0]['recoveryConfiguration']['configuration']['amazon']['overrideReplicationOptions'].get('keyPair')
        return None

    @property
    def encryption_key(self) -> str:
        """Get the AWS encryption key for the recovery group.

        Returns:
            The AWS encryption key as a string, or None for Azure.

        Example:
            >>> rg = RecoveryGroup()
            >>> key = rg.encryption_key
            >>> print(f"Encryption key: {key}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'amazon':
            return self.entities[0]['recoveryConfiguration']['configuration']['amazon']['overrideReplicationOptions'].get('encryptionKey')
        return None

    @property
    def volume_type(self) -> str:
        """Get the AWS volume type for the recovery group.

        Returns:
            The AWS volume type as a string, or None for Azure.

        Example:
            >>> rg = RecoveryGroup()
            >>> vol_type = rg.volume_type
            >>> print(f"Volume type: {vol_type}")

        #ai-gen-doc
        """
        vendor = self.vendor_type
        if vendor == 'amazon':
            return self.entities[0]['recoveryConfiguration']['configuration']['amazon']['overrideReplicationOptions'].get('volumeType', '')
        return None

    @property
    def get_new_target_name(self) -> str:
        """Get the generated target name for the recovery group created using custom configuration.

        Returns:
            The name of the target created for the recovery group as a string.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> target_name = recovery_group.get_new_target_name
            >>> print(f"New target name: {target_name}")

        #ai-gen-doc
        """
        return f'{self.recovery_group_name}-Site'

    @property
    def get_new_hypervisor_name(self) -> str:
        """Get the name of the newly created hypervisor for the recovery group.

        This property returns the name of the hypervisor that was created as part of the recovery group setup using a custom configuration.

        Returns:
            The name of the created hypervisor as a string.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> hypervisor_name = recovery_group.get_new_hypervisor_name
            >>> print(f"New hypervisor name: {hypervisor_name}")

        #ai-gen-doc
        """
        return f'{self.get_new_target_name}-Hypervisor'

    @property
    def is_threatscan_enabled(self) -> bool:
        """Check if threat scan is enabled at the recovery group level.

        Returns:
            True if the threat scan property is enabled for this recovery group, False otherwise.

        Example:
            >>> rg = RecoveryGroup()
            >>> if rg.is_threatscan_enabled:
            ...     print("Threat scan is enabled for this recovery group.")
            ... else:
            ...     print("Threat scan is not enabled for this recovery group.")

        #ai-gen-doc
        """
        return self._properties['recoveryGroup']['threatScan']['enableThreatScan']

    @property
    def is_windefender_enabled(self) -> bool:
        """Check if Windows Defender is enabled at the recovery group level.

        Returns:
            True if the Windows Defender property is enabled for this recovery group, False otherwise.

        Example:
            >>> rg = RecoveryGroup()
            >>> if rg.is_windefender_enabled:
            ...     print("Windows Defender is enabled for this recovery group.")
            ... else:
            ...     print("Windows Defender is not enabled for this recovery group.")

        #ai-gen-doc
        """
        return self._properties['recoveryGroup']['threatScan']['enableWindowsDefenderScan']

    @property
    def powerOffDestinationVMPostRecovery(self) -> bool:
        """Indicate whether the power off/on option is enabled for the destination VM after recovery.

        Returns:
            bool: True if the destination VM will be powered off (and/or on) post recovery; False otherwise.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> is_power_off_enabled = recovery_group.powerOffDestinationVMPostRecovery
            >>> print(f"Power off/on post recovery enabled: {is_power_off_enabled}")

        #ai-gen-doc
        """
        return self._properties['recoveryGroup']['powerOffDestinationVMPostRecoveryAndValidation']

    # ---------------------------- DESTINATION ----------------------------

    @property
    def destination_client_object(self):
        """Returns cvpysdk destination hypervisor client object"""
        destination_client = self._recovery_target.destination_hypervisor
        self._destination_client_object = self._commcell_object.clients.get(destination_client)
        return self._destination_client_object

    def destination_agent_object(self, workload):
        """Returns cvpysdk destination agent(workload) object"""
        destination_agent = WORKLOADS[workload]
        self._destination_agent_object = self.destination_client_object.agents.get(destination_agent)
        return self._destination_agent_object

    def destination_instance_object(self, workload):
        """Returns cvpysdk destination instance object"""
        destination_instance = INSTANCES[self._recovery_target.target_instance]
        self._destination_instance_object = self.destination_agent_object(workload).instances.get(
            destination_instance)
        return self._destination_instance_object

    @property
    def is_post_recovery_actions_configured(self) -> bool:
        """Check if post recovery actions are configured at the recovery group level.

        Returns:
            True if one or more post recovery actions are configured, False otherwise.

        Example:
            >>> rg = RecoveryGroup()
            >>> if rg.is_post_recovery_actions_configured:
            ...     print("Post recovery actions are configured.")
            ... else:
            ...     print("No post recovery actions configured.")

        #ai-gen-doc
        """
        post_actions = self._properties['recoveryGroup'].get('postRecoveryActions', [])
        return bool(post_actions)  # True if list is non-empty


    @property
    def autoscale_enabled(self):
        """Returns boolean if autoscale enabled or not"""
        return self._properties['recoveryGroup']['useAutoScale']

    def _recover_entities(self, entity_ids: list, threat_scan: bool = False, win_defender_scan: bool = False) -> int:
        """Send a request to recover all entities with the specified IDs.

        This method initiates the recovery process for the provided entity IDs. Optionally, security scans
        such as threat scan and Windows Defender scan can be performed on the restored virtual machines.

        Args:
            entity_ids: A list of entity IDs to be recovered.
            threat_scan: If True, runs a security scan on the restored VMs. Defaults to False.
            win_defender_scan: If True, runs a Windows Defender scan on the restored VMs. Defaults to False.

        Returns:
            The job ID (int) of the initiated recovery operation.

        Raises:
            SDKException: If the response is empty or the recovery request is not successful.

        Example:
            >>> group = RecoveryGroup()
            >>> job_id = group._recover_entities([101, 102, 103], threat_scan=True)
            >>> print(f"Recovery job started with ID: {job_id}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('POST', self._RECOVER_URL, payload={
            'recoveryGroup': {
                'id': self.id
            },
            'entities': [{'id': e_id} for e_id in entity_ids],
            'threatScan': {
                'enableThreatScan': threat_scan if not self.is_threatscan_enabled else self.is_threatscan_enabled,
                'enableWindowsDefenderScan': win_defender_scan if not self.is_windefender_enabled else self.is_windefender_enabled
            }
        })

        if flag:
            try:
                return response.json()['jobId']
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102', 'Job id not found in response')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def get_threats_count(self) -> int:
        """Retrieve the total number of threats detected for the recovery group.

        This method sends a request to obtain the overall threats count associated with the recovery group.

        Returns:
            The number of threats detected for the recovery group as an integer.

        Raises:
            SDKException: If the response is empty or the request is not successful.

        Example:
            >>> rg = RecoveryGroup()
            >>> threat_count = rg.get_threats_count()
            >>> print(f"Total threats detected: {threat_count}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_GROUP_THREATS_COUNT)

        if flag:
            try:
                return response.json()['KPI'][0]["threatCount"]
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102', 'Threat count not found in response')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def recover_all(self, threat_scan: bool = False, win_defender_scan: bool = False) -> int:
        """Initiate recovery for all entities in the recovery group.

        This method sends a request to recover all entities associated with the recovery group.
        Optional threat scanning and Windows Defender scanning can be enabled during the recovery process.

        Args:
            threat_scan: If True, perform a threat scan as part of the recovery. Defaults to False.
            win_defender_scan: If True, perform a Windows Defender scan during recovery. Defaults to False.

        Returns:
            The job ID (int) of the initiated recovery operation.

        Raises:
            SDKException: If the response is empty or the recovery request is unsuccessful.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> job_id = recovery_group.recover_all(threat_scan=True, win_defender_scan=False)
            >>> print(f"Recovery job started with ID: {job_id}")

        #ai-gen-doc
        """
        eligible_entities = [entity['id'] for entity in self.entities if
                             entity['recoveryStatus'] not in [RecoveryStatus.NOT_READY.value,
                                                              RecoveryStatus.IN_PROGRESS.value] and
                     (not win_defender_scan or (win_defender_scan and entity['osType'] == 0))]

        return self._recover_entities(eligible_entities, threat_scan, win_defender_scan)

    def refresh(self) -> None:
        """Reload the recovery group information to ensure the latest state is reflected.

        This method refreshes the internal data of the recovery group, updating it with the most current information from the source.

        Example:
            >>> rg = RecoveryGroup()
            >>> rg.refresh()  # Updates the recovery group with the latest data

        #ai-gen-doc
        """
        self._properties = self._get_recovery_group_properties()

    def _get_recovery_group_properties(self) -> dict:
        """Retrieve the properties of the recovery group.

        Returns:
            dict: A dictionary containing the properties of the recovery group.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> properties = recovery_group._get_recovery_group_properties()
            >>> print(properties)
            >>> # The returned dictionary contains key-value pairs describing the recovery group

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_GROUP_URL)

        if flag:
            try:
                return response.json()
            except JSONDecodeError:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def delete(self) -> None:
        """Send a request to delete the replication group associated with this RecoveryGroup instance.

        This method initiates the deletion process for the replication group. If the deletion fails
        or the response is empty, an SDKException is raised.

        Raises:
            SDKException: If the response from the deletion request is empty or indicates failure.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> recovery_group.delete()
            >>> print("Replication group deleted successfully.")

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request('DELETE', self._RECOVERY_GROUP_URL)

        if flag:
            try:
                return response.json()
            except JSONDecodeError:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def get_entity_status(self) -> dict:
        """Retrieve the recovery status and readiness category for all entities in the recovery group.

        Returns:
            dict: A dictionary mapping each entity name to its recovery status and not-ready category.
            The structure is typically:
                {
                    "entity_name_1": {"status": "Ready", "not_ready_category": None},
                    "entity_name_2": {"status": "Not Ready", "not_ready_category": "Network Issue"},
                    ...
                }

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> status_info = recovery_group.get_entity_status()
            >>> for entity, info in status_info.items():
            ...     print(f"{entity}: Status={info['status']}, Not Ready Category={info['not_ready_category']}")

        #ai-gen-doc
        """
        status_map = {}
        for entity in self.entities:
            if 'name' not in entity:
                continue  # Skip entities without a name

            status_map[entity['name']] = {
                'recoveryStatus': entity.get('recoveryStatus', None),
                'recoveryStatusNotReadyCategory': entity.get('recoveryStatusNotReadyCategory', None)
            }
        return status_map

    def validate_new_recovery_target_exists(self) -> bool:
        """Check if a newly created recovery target (via custom configuration) exists with the correct name.

        Returns:
            bool: True if the recovery target exists and matches the expected name, False otherwise.

        Example:
            >>> rg = RecoveryGroup()
            >>> exists = rg.validate_new_recovery_target_exists()
            >>> print(f"Recovery target exists: {exists}")

        #ai-gen-doc
        """
        observed_target = self.target_name
        expected_target = self.get_new_target_name

        return observed_target == expected_target

    def validate_new_hypervisor_exists(self) -> bool:
        """Check if the newly created hypervisor via custom configuration exists with the correct name.

        Returns:
            bool: True if the new hypervisor exists and has the correct name, False otherwise.

        Example:
            >>> rg = RecoveryGroup()
            >>> exists = rg.validate_new_hypervisor_exists()
            >>> print(f"Hypervisor exists: {exists}")

        #ai-gen-doc
        """
        observed_hypervisor = self._recovery_target.destination_hypervisor
        expected_hypervisor = self.get_new_hypervisor_name

        return observed_hypervisor == expected_hypervisor

    def cleanup_recovered_entities(self) -> int:
        """Perform cleanup of all recovered entities in the recovery group.

        This method initiates a cleanup operation for all entities that have been recovered
        within the recovery group. It returns the job ID associated with the cleanup process.

        Returns:
            int: The job ID of the initiated cleanup job.

        Raises:
            SDKException: If the response from the cleanup operation is empty or unsuccessful.

        Example:
            >>> recovery_group = RecoveryGroup()
            >>> job_id = recovery_group.cleanup_recovered_entities()
            >>> print(f"Cleanup job started with Job ID: {job_id}")

        #ai-gen-doc
        """
        entity_ids = self.entities_id
        group_id = self.id

        if not entity_ids:
            raise SDKException('RecoveryGroup', '101', 'entity_ids cannot be empty')

        payload = {
            "recoveryGroup": {"id": group_id},
            "entities": [{"id": eid} for eid in entity_ids]
        }
        flag, response = self._cvpysdk_object.make_request(
            'POST',
            self._commcell_object._services['CLEANUP_RECOVERY_GROUP'],
            payload
        )
        if flag:
            try:
                return response.json()['jobId']
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102', 'Job id not found in response')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    @property
    def crr_resources(self) -> List[Dict]:
        """Return the list of CRR resources for this recovery group.

        Returns:
            list: The raw list of resource dicts from ``crrResourcesInfo.resources``,
            each containing ``resourceId``, ``resourceStatus``, ``resourceType``,
            ``resourceURL``, ``scope``, and ``resourceInfo`` (with ``name`` and ``guid``).

        Example:
            >>> for r in recovery_group.crr_resources:
            ...     print(r['resourceInfo']['name'], r['resourceStatus'])
        """
        return (
            self._properties
            .get('recoveryGroup', {})
            .get('crrResourcesInfo', {})
            .get('resources', [])
        )
