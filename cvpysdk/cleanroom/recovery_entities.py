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

from enum import Enum
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING

from cvpysdk.exception import SDKException
from cvpysdk.cleanroom.recoveryjob import RecoveryJob

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
    'AMAZON': 'Amazon Web Services',
    'VMW': 'VMware'
}

RecoveryDestinationVendor = {
    7 : 'azure',
    1 : 'amazon',
    0 : 'vmw',
}

class RecoveryStatus(Enum):
    """
    Enumeration representing various recovery statuses.

    This class is used to define and manage distinct recovery states within an application,
    providing a clear and type-safe way to handle status values. As an Enum, it ensures
    that only predefined recovery statuses are used, improving code reliability and readability.

    Key Features:
        - Defines recovery status values as enumeration members
        - Facilitates type-safe status management
        - Improves code clarity and maintainability

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
    RECOVERED_WITH_THREATS = 10

class RecoveryReadiness(Enum):
    """
    Enumeration representing different levels or states of recovery readiness.

    This class is intended to be used for categorizing or identifying
    the readiness status in recovery-related workflows or systems.
    As an Enum, it provides a set of constant values for use in
    decision-making, status reporting, or configuration.

    Key Features:
        - Defines recovery readiness states as enumeration members
        - Facilitates clear and type-safe status representation
        - Useful for workflow control and reporting

    #ai-gen-doc
    """
    NO_STATUS = 0
    NONE = 0
    NOT_READY = 1
    READY = 2

class RecoveryStatusNotReadyCategory(Enum):
    """
    Enumeration for recovery status categories indicating 'not ready' states.

    This Enum class is used to represent various categories or reasons why a recovery
    status may be considered 'not ready'. It provides a structured way to classify
    and handle different 'not ready' conditions in recovery processes.

    Key Features:
        - Defines distinct 'not ready' recovery status categories
        - Enables clear and type-safe handling of recovery states
        - Facilitates categorization and management of recovery readiness

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

class ValidationStatus(Enum):
    """
    Enumeration representing various validation statuses.

    This class is intended to define a set of constant values that represent
    the possible outcomes or states of a validation process. It can be used
    to standardize validation status reporting across different components
    of an application.

    Key Features:
        - Provides a clear and type-safe way to represent validation statuses
        - Facilitates consistent status handling in validation workflows
        - Inherits from Python's Enum for easy integration and usage

    #ai-gen-doc
    """
    NONE = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILED = 3
    WARNING = 4

class RecoveryEntities:
    """
    Manages and interacts with recovery entities within a recovery group.

    This class provides an interface to access and verify the existence of recovery entities
    associated with a specific recovery group and commcell object. It is designed to facilitate
    entity management operations such as retrieval and existence checks.

    Key Features:
        - Initialization with a recovery group and commcell object
        - Retrieval of recovery entities by entity ID
        - Verification of entity existence by entity ID

    #ai-gen-doc
    """

    def __init__(self, recovery_group: object, commcell_object: 'Commcell') -> None:
        """Initialize the RecoveryEntities manager for a specific recovery group.

        Args:
            recovery_group: The recovery group object to manage.
            commcell_object: The Commcell connection object used for operations.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> recovery_entities = RecoveryEntities(recovery_group, commcell)
            >>> print("RecoveryEntities manager initialized for FinanceGroup")

        #ai-gen-doc
        """
        self._recovery_group_object = recovery_group # gets the recovery group object
        self._commcell_object = commcell_object # gets commcell object

    def get(self, entity_id: int) -> object:
        """Retrieve the recovery entity object for the specified entity ID.

        Args:
            entity_id: The unique integer ID of the recovery entity to retrieve.

        Returns:
            An instance of the recovery entity corresponding to the given entity ID.

        Raises:
            SDKException: If a recovery group does not exist with the specified name,
                or if a recovery entity does not exist with the given ID.

        Example:
            >>> recovery_entities = RecoveryEntities()
            >>> entity = recovery_entities.get(1234)
            >>> print(f"Retrieved entity: {entity}")

        #ai-gen-doc
        """
        entity_id = int(entity_id)
        if self._recovery_group_object.recovery_group_name:
            if self.entity_exists(entity_id):
                return RecoveryEntity(self._commcell_object, self._recovery_group_object,
                                      entity_id)
            raise SDKException('RecoveryEnity', '102',
                               'No recovery entity exists with id: {0}'.format(entity_id))
        raise SDKException('RecoveryGroup', '102',
                               'Recovery group name is empty: {0}'.format(self._recovery_group_object.recovery_group_name))


    def entity_exists(self, entity_id: int) -> bool:
        """Check if a recovery entity with the specified ID exists.

        Args:
            entity_id: The unique identifier of the recovery entity to check.

        Returns:
            True if the entity exists, False otherwise.

        Example:
            >>> recovery_entities = RecoveryEntities()
            >>> exists = recovery_entities.entity_exists(12345)
            >>> print(f"Entity exists: {exists}")

        #ai-gen-doc
        """
        for entity in self._recovery_group_object.entities:
            if entity['id'] == entity_id:
                return True
        return False

class RecoveryEntity:
    """
    Represents a recovery entity within a recovery group, providing access to its properties,
    status, and configuration, as well as methods to manage and refresh its state.

    This class is designed to interact with recovery entities in a CommCell environment,
    allowing users to retrieve detailed information about the entity, its source and destination
    virtual machines, recovery options, validation results, and job history. It also provides
    mechanisms to refresh the entity's data and access its configuration.

    Key Features:
        - Initialization with CommCell and recovery group context
        - Access to entity properties such as IDs, source/destination VMs, clients, agents, instances, and subclients
        - Retrieval of recovery options and configuration details
        - Monitoring of entity readiness, recovery, and validation status
        - Access to validation results and recovery point details
        - Retrieval of last recovery and restore job information
        - Access to parent recovery group and workload details
        - Method to refresh entity data and update properties

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', recovery_group_object: object, recovery_entity_id: int) -> None:
        """Initialize a new instance of the RecoveryEntity class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            recovery_group_object: The recovery group object associated with this recovery entity.
            recovery_entity_id: The unique identifier for the recovery entity.

        Example:
            >>> commcell = Commcell('hostname', 'username', 'password')
            >>> recovery_group = RecoveryGroup(commcell)
            >>> entity = RecoveryEntity(commcell, recovery_group, 12345)
            >>> print(f"Created RecoveryEntity with ID: {entity.recovery_entity_id}")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._recovery_group =recovery_group_object
        self._recovery_target = self._commcell_object.cleanroom_targets.get(self._recovery_group.target_name)
        self._recovery_entity_id = recovery_entity_id

        self._source_vm = None
        self._destination_vm = None
        self._last_recovery_job = None
        self._last_restore_job = None
        self._parent = None
        self._recovery_readiness_status = None
        self._recovery_status = None
        self._validation_status = None
        self._validation_results = None
        self._recovery_point = None
        self._workload = None
        self._source_client_object = None
        self._source_agent_object = None
        self._source_instance_object = None
        self._source_subclient_object = None
        self._destination_client_object = None
        self._destination_agent_object = None
        self._destination_instance_object = None

        self._recovery_config_dict = None
        self._recovery_image = None

        self._properties = None

        self._RECOVERY_ENTITY_URL = commcell_object._services['RECOVERY_ENTITY'] % self._recovery_entity_id
        self.refresh()


    def _get_entity_recovery_options(self) -> dict:
        """Retrieve the recovery options for the recovery entity.

        This method fetches the recovery options associated with the current recovery entity.
        It is intended for internal use to obtain configuration or operational parameters
        required for recovery operations.

        Returns:
            dict: A dictionary containing the recovery options for the entity.

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> options = recovery_entity._get_entity_recovery_options()
            >>> print("Recovery options:", options)

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_ENTITY_URL)

        if flag:
            try:
                # Attempt to decode the JSON response
                response_data = response.json()

                if not response_data:
                    raise SDKException('Response', '102', 'Response contains no data.')

                # If data is present, process the response
                self._properties = response_data
                self._source_vm = self._properties['name']
                self._destination_vm = self._properties['destinationName']
                self._parent = self._properties.get('vmGroup', '')
                self._destination_proxy_client_object = 'Automatic' if self._recovery_target.access_node == 'Automatic' else self._commcell_object.clients.get(
                self._recovery_target.access_node['name']) if self._recovery_target.access_node[
                                                                      'type'] == 'Client' else None

                if self._properties['recoveryStatusNotReadyCategory'] != 0:
                    """In this case readiness status is Not Ready"""
                    self._recovery_readiness_status = RecoveryStatusNotReadyCategory(self._properties['recoveryStatusNotReadyCategory']).name
                else:
                    self._recovery_readiness_status = RecoveryReadiness.READY.name
                self._last_recovery_job = self._properties['lastRecoveryJobId']
                if self._last_recovery_job != 0:
                    recovery_job = RecoveryJob(self._commcell_object, self._last_recovery_job)
                    phases = recovery_job.get_phases().get(self._source_vm, [])
                    for phase in phases:
                        if phase.get('phase_name').name == 'RESTORE_VM' and phase.get('job_id'):
                            self._last_restore_job = phase.get('job_id')
                self._recovery_status = RecoveryStatus(self._properties['recoveryStatus']).name
                self._validation_status = ValidationStatus(self._properties['validationStatus']).name
                # validation results are available for only threat scan/windows defender enabled recovery jobs
                if 'validationResults' in self._properties.keys():
                    validation_results = self._properties.get('validationResults', {})
                    self._validation_results = {
                        'output': validation_results[0].get('output'),
                        'failureReason': validation_results[0].get('failureReason'),
                        'name': validation_results[0].get('name'),
                        'validationStatus':validation_results[0].get('validationStatus'),
                        'threatInfo': validation_results[0].get('threatInfo')
                    }
                else:
                    pass
                recovery_point_details = self._properties.get('recoveryPointDetails', {})
                self._recovery_point = {
                        'entityRecoveryPointCategory': recovery_point_details.get('entityRecoveryPointCategory'),
                        'entityRecoveryPoint': recovery_point_details.get('entityRecoveryPoint'),
                        'inheritedFrom': recovery_point_details.get('inheritedFrom')
                    }
                self._workload = WORKLOADS[self._properties['workload']]
                self._source_client = self._properties['client']['name']
                self._source_agent = WORKLOADS[self._properties['workload']]
                self._source_instance = self._properties['instance']['name']
                self._source_subclient = self._properties['vmGroup']['name']
                self._destination_client = self._recovery_target.destination_hypervisor
                self._destination_agent = WORKLOADS[self._properties['workload']]
                self._destination_instance = INSTANCES[self._recovery_target.target_instance]
                """Returns a dict of all entities restore options"""
                self._recovery_config_dict = {
                     self._properties['name']: self._properties['recoveryConfiguration']['configuration'][RecoveryDestinationVendor[self._recovery_target.policy_type]]
                }
                self._recovery_image = self._properties.get('recoveryConfiguration', {}).get('imageDetails', {}).get('vmTemplate', {}).get('name')

            except JSONDecodeError:
                raise SDKException('Response', '101', 'Failed to decode JSON from the response.')
            except KeyError as e:
                raise SDKException('Response', '101', f'Missing expected key in the response: {str(e)}')

        # If the request was unsuccessful, raise an exception
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    @property
    def commcell(self) -> 'Commcell':
        """Get the Commcell object associated with this RecoveryEntity.

        Returns:
            Commcell: The Commcell instance linked to this recovery entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> cc = entity.commcell  # Access the associated Commcell object
            >>> print(f"Connected to Commcell: {cc}")

        #ai-gen-doc
        """
        return self._commcell_object

    @property
    def entity_id(self) -> int:
        """Get the unique identifier of the recovery entity.

        Returns:
            int: The entity ID associated with this RecoveryEntity instance.

        Example:
            >>> recovery_entity = RecoveryEntity()
            >>> eid = recovery_entity.entity_id  # Use dot notation for property access
            >>> print(f"Entity ID: {eid}")
        #ai-gen-doc
        """
        return self._recovery_entity_id

    @property
    def source_vm(self) -> str:
        """Get the name of the source virtual machine entity.

        Returns:
            The name of the source VM as a string.

        Example:
            >>> recovery_entity = RecoveryEntity()
            >>> vm_name = recovery_entity.source_vm  # Use dot notation for property access
            >>> print(f"Source VM: {vm_name}")

        #ai-gen-doc
        """
        return self._source_vm

    @property
    def destination_vm(self) -> str:
        """Get the name of the destination entity (VM) for the recovery operation.

        Returns:
            The name of the destination virtual machine as a string.

        Example:
            >>> recovery_entity = RecoveryEntity()
            >>> dest_vm_name = recovery_entity.destination_vm
            >>> print(f"Destination VM: {dest_vm_name}")

        #ai-gen-doc
        """
        return self._destination_vm

    @property
    def recovery_group_name(self) -> str:
        """Get the name of the recovery group associated with this entity.

        Returns:
            The name of the recovery group as a string.

        Example:
            >>> entity = RecoveryEntity()
            >>> group_name = entity.recovery_group_name  # Use dot notation for property access
            >>> print(f"Recovery group: {group_name}")
        #ai-gen-doc
        """
        return self._recovery_group.recovery_group_name

    @property
    def recovery_target_name(self) -> str:
        """Get the name of the recovery target associated with this entity.

        Returns:
            The name of the recovery target as a string.

        Example:
            >>> entity = RecoveryEntity()
            >>> target_name = entity.recovery_target_name
            >>> print(f"Recovery target: {target_name}")

        #ai-gen-doc
        """
        return self._recovery_target.cleanroom_target_name

    @property
    def entity_readiness_status(self) -> str:
        """Get the readiness state of the recovery entity.

        Returns:
            The readiness status of the entity as a string.

        Example:
            >>> entity = RecoveryEntity()
            >>> status = entity.entity_readiness_status  # Use dot notation for property
            >>> print(f"Entity readiness status: {status}")

        #ai-gen-doc
        """
        return self._recovery_readiness_status

    @property
    def entity_recovery_status(self) -> str:
        """Get the recovery status of the entity.

        Returns:
            str: The current recovery status of the entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> status = entity.entity_recovery_status  # Use dot notation for property access
            >>> print(f"Entity recovery status: {status}")

        #ai-gen-doc
        """
        return self._recovery_status

    @property
    def validation_status(self) -> str:
        """Get the validation status of the recovery entity.

        Returns:
            The current validation status of the entity as a string.

        Example:
            >>> entity = RecoveryEntity()
            >>> status = entity.validation_status  # Use dot notation for property access
            >>> print(f"Validation status: {status}")

        #ai-gen-doc
        """
        return self._validation_status

    @property
    def validation_results(self) -> dict:
        """Get the validation results of the recovery entity.

        Returns:
            dict: A dictionary containing the validation results for this entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> results = entity.validation_results  # Access validation results as a property
            >>> print(results)
            {'status': 'valid', 'details': 'All checks passed'}

        #ai-gen-doc
        """
        return self._validation_results

    @property
    def recoveryPointDetails(self) -> dict:
        """Get the details of the recovery point as a dictionary.

        Returns:
            dict: A dictionary containing information about the recovery point.

        Example:
            >>> entity = RecoveryEntity()
            >>> details = entity.recoveryPointDetails  # Access recovery point details as a property
            >>> print(details)
            {'recovery_point_id': 123, 'timestamp': '2023-12-01T10:00:00Z', ...}

        #ai-gen-doc
        """
        return self._recovery_point

    @property
    def lastRecoveryJob(self) -> int:
        """Get the most recent recovery job associated with this RecoveryEntity.

        Returns:
            int: The ID of the last recovery job performed for this entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> last_job = entity.lastRecoveryJob  # Access the property to get the last recovery job
            >>> print(f"Last recovery job ID: {last_job}")

        #ai-gen-doc
        """
        return self._last_recovery_job

    @property
    def lastRestoreJob(self) -> int:
        """Get the most recent restore job ID associated with this RecoveryEntity.

        Returns:
            int: The ID of the last restore job performed for this recovery entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> last_job = entity.lastRestoreJob
            >>> print(f"Last restore job ID: {last_job}")

        #ai-gen-doc
        """
        return self._last_restore_job

    @property
    def parent(self) -> str:
        """Get the VM group associated with the source recovery entity.

        Returns:
            str: The name of the VM group to which this recovery entity belongs.

        Example:
            >>> entity = RecoveryEntity()
            >>> vm_group = entity.parent  # Access the parent VM group using the property
            >>> print(f"Parent VM group: {vm_group}")

        #ai-gen-doc
        """
        return self._parent

    @property
    def workload(self) -> str:
        """Get the workload type of the source entity.

        Returns:
            The workload of the source entity as a string.

        Example:
            >>> entity = RecoveryEntity()
            >>> print(entity.workload)  # Use dot notation to access the workload property
            'Exchange'
        #ai-gen-doc
        """
        return self._workload

    def all_properties(self) -> dict:
        """Retrieve all properties associated with this recovery entity.

        Returns:
            dict: A dictionary containing all properties of the entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> properties = entity.all_properties()
            >>> print(properties)
            >>> # Output: {'property1': value1, 'property2': value2, ...}

        #ai-gen-doc
        """
        return self._properties

    @property
    def recovery_config_dict(self) -> dict:
        """Get the dictionary of recovery options for this recovery entity.

        Returns:
            dict: A dictionary containing recovery configuration options specific to the entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> config = entity.recovery_config_dict
            >>> print(config)
            {'option1': 'value1', 'option2': 'value2'}

        #ai-gen-doc
        """
        return self._recovery_config_dict

    @property
    def recovery_image(self) -> str:
        """Get the recovery image associated with this recovery entity.

        Returns:
            str: The name of the recovery image used for this entity.

        Example:
            >>> entity = RecoveryEntity()
            >>> image = entity.recovery_image
            >>> print(f"Recovery image: {image}")

        #ai-gen-doc
        """
        return self._recovery_image


    @property
    def check_entity_id(self) -> bool:
        """Check if the recovery group exists and contains the specified entity.

        Returns:
            True if the recovery group exists and includes the entity, False otherwise.

        Example:
            >>> entity = RecoveryEntity()
            >>> exists = entity.check_entity_id
            >>> print(f"Entity exists in recovery group: {exists}")

        #ai-gen-doc
        """
        if self._recovery_group.recovery_group_name is not None:
            if self._properties['id'] == self._recovery_entity_id:
                return True
            else:
                return False

    @property
    def source_client(self) -> str:
        """Get the source client name for this recovery entity.

        Returns:
            The name of the source client as a string.

        Example:
            >>> recovery_entity = RecoveryEntity()
            >>> src_client = recovery_entity.source_client
            >>> print(f"Source client: {src_client}")

        #ai-gen-doc
        """
        return self._source_client

    @property
    def source_agent(self) -> str:
        """Get the source agent workload type for the recovery entity.

        This property returns the type of workload associated with the recovery entity,
        such as 'VM' for virtual machines or 'Files' for file-based workloads.

        Returns:
            str: The source agent workload type (e.g., 'VM', 'Files').

        Example:
            >>> entity = RecoveryEntity()
            >>> agent_type = entity.source_agent
            >>> print(f"Source agent: {agent_type}")
            Source agent: VM

        #ai-gen-doc
        """
        return self._source_agent

    @property
    def source_instance(self) -> str:
        """Get the source instance type for the recovery entity.

        This property returns the type of the source instance, such as 'Azure', 'AWS', etc., 
        associated with the recovery entity.

        Returns:
            The source instance type as a string (e.g., 'Azure', 'AWS').

        Example:
            >>> entity = RecoveryEntity()
            >>> instance_type = entity.source_instance
            >>> print(f"Source instance type: {instance_type}")

        #ai-gen-doc
        """
        return self._source_instance

    @property
    def source_subclient(self) -> str:
        """Get the source subclient name for this recovery entity.

        Returns:
            The name of the source subclient as a string.

        Example:
            >>> recovery_entity = RecoveryEntity()
            >>> subclient = recovery_entity.source_subclient
            >>> print(f"Source subclient: {subclient}")

        #ai-gen-doc
        """
        return self._source_subclient

    @property
    def destination_client(self) -> str:
        """Get the destination client Hypervisor Client for this recovery entity.

        Returns:
            The name of the destination client Hypervisor Client as a string.

        Example:
            >>> entity = RecoveryEntity()
            >>> dest_client = entity.destination_client
            >>> print(f"Destination client: {dest_client}")

        #ai-gen-doc
        """
        return self._destination_client

    @property
    def destination_agent(self) -> str:
        """Get the destination agent for the recovery entity.

        This property returns the name of the destination agent associated with the recovery entity,
        which could be a workload type such as VM or Files.

        Returns:
            The name of the destination agent as a string.

        Example:
            >>> entity = RecoveryEntity()
            >>> agent = entity.destination_agent  # Use dot notation for property access
            >>> print(f"Destination agent: {agent}")

        #ai-gen-doc
        """
        return self._destination_agent

    @property
    def destination_instance(self) -> str:
        """Get the destination instance associated with the recovery entity.

        This property returns the name or identifier of the destination instance,
        such as an Azure or AWS instance, to which the recovery entity is targeted.

        Returns:
            The destination instance as a string (e.g., 'Azure', 'AWS').

        Example:
            >>> entity = RecoveryEntity()
            >>> dest_instance = entity.destination_instance
            >>> print(f"Destination instance: {dest_instance}")

        #ai-gen-doc
        """
        return self._destination_instance

    def refresh(self) -> None:
        """Reload the properties of the live sync entity.

        This method updates the internal state of the RecoveryEntity instance to reflect 
        the latest properties and configuration from the source system.

        Example:
            >>> entity = RecoveryEntity()
            >>> entity.refresh()
            >>> print("Live sync properties refreshed successfully")

        #ai-gen-doc
        """
        self._get_entity_recovery_options()
