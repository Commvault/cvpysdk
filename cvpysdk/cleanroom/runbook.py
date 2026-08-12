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

Runbook:   Class for creating a cleanroom recovery group and target using the new simplified runbook API

"""
from json.decoder import JSONDecodeError
from cvpysdk.exception import SDKException
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cvpysdk.commcell import Commcell


class Runbook:
    """
    Class to perform actions on a cleanroom runbook.

    This class provides an interface for managing and executing operations on a cleanroom runbook,
    leveraging a commcell object for communication and orchestration. It supports creation of runbooks,
    payload population for specific entities, and exposes recovery group identification.

    Key Features:
        - Initialization with a commcell object for backend operations
        - Creation of runbooks using customizable payloads
        - Property access to recovery group ID for identification and tracking
        - Payload population for entities, targets, regions, and nodes to facilitate runbook execution

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a new instance of the Runbook class.

        Args:
            commcell_object: An instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> runbook = Runbook(commcell)
            >>> print("Runbook instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._recovery_group_id = None
        self._RUNBOOK_URL = commcell_object._services['CREATE_CLEANROOM_RUNBOOK']    

    def create(self, payload: dict = dict()) -> dict:
        """Create a cleanroom runbook with the specified payload.

        Args:
            payload: Dictionary containing the parameters required to create the runbook.

        Returns:
            dict: The response from the API containing details of the created runbook.
            Example response:
                {
                    "recoveryGroup": {
                        "id": 1234567890,
                        "name": "runbook_name"
                    }
                }

        Raises:
            SDKException: If the payload is empty, the API response is empty, or the API response indicates failure.

        Example:
            >>> runbook = Runbook()
            >>> payload = {
            ...     "recoveryGroup": {
            ...         "name": "MyRunbook",
            ...         "description": "Automated recovery workflow"
            ...     }
            ... }
            >>> response = runbook.create(payload)
            >>> print(response["recoveryGroup"]["id"])
            1234567890

        #ai-gen-doc
        """
        if not payload:
            raise SDKException('RecoveryGroup', '101', 'Payload cannot be empty')
        flag, response = self._cvpysdk_object.make_request('POST', self._RUNBOOK_URL, payload=payload)
        
        if flag:
            try:
                response_json = response.json()
                if not response_json:
                    raise ValueError('Response', '102', 'Empty response received from the server')
                
                if "recoveryGroup" in response_json and "id" in response_json['recoveryGroup']:
                        self._recovery_group_id = response_json['recoveryGroup']['id']
                        return response_json
                else:
                    raise KeyError('Response', '102', 'Recovery group ID not found in the response')
            except JSONDecodeError:
                raise ValueError('Response', '102', 'Invalid response received from the server.')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
            
    @property
    def recovery_group_id(self) -> int:
        """Get the recovery group ID associated with this runbook.

        The recovery group ID is initialized when the runbook is created and uniquely identifies
        the recovery group for this runbook instance.

        Returns:
            The integer ID of the recovery group.

        Example:
            >>> runbook = Runbook()
            >>> group_id = runbook.recovery_group_id
            >>> print(f"Recovery Group ID: {group_id}")
        #ai-gen-doc
        """
        if self._recovery_group_id is not None:
            return int(self._recovery_group_id)
        return None

    def populate_payload(self, entities: dict, target: dict, region: dict, node: dict = None) -> dict:
        """Build the payload required for creating a runbook.

        This method constructs and returns a payload dictionary containing the necessary fields for runbook creation,
        based on the provided entities, target, region, and optionally, access node details.

        Args:
            entities: Dictionary containing the entities to be included in the runbook. This should include a "name" key
                and an "entities" list, where each entity dictionary specifies details such as instance, client, backupset,
                workload type, and execution order.
            target: Dictionary specifying the target environment for the runbook. The format varies depending on whether
                an existing target, a new target with an existing hypervisor, or a new target with credentials is used.
            region: Dictionary containing region details, such as "guid" and "name".
            node: Optional dictionary specifying access node details, such as "access_node_id" and "access_node_type".
                This is required only when not using an existing target or hypervisor.

        Returns:
            dict: The fully populated payload dictionary ready for runbook creation.

        Raises:
            SDKException: If the entities input is empty, if an invalid workload type is provided, or if the target input is empty.

        Example:
            >>> entities = {
            ...     "name": "Runbook with existing target",
            ...     "entities": [
            ...         {
            ...             "instance_id": 1,
            ...             "instance_name": "DefaultInstanceName",
            ...             "client_id": 2,
            ...             "client_name": "devcs3",
            ...             "backupset_id": 3,
            ...             "backupset_name": "defaultBackupSet",
            ...             "subclient_id": 14,
            ...             "subclient_name": "small file",
            ...             "workload": "FILES",
            ...             "execution_order": 2
            ...         },
            ...         {
            ...             "instance_id": 6,
            ...             "instance_name": "Amazon Web Services",
            ...             "client_id": 10,
            ...             "client_name": "AWS",
            ...             "backupset_id": 14,
            ...             "backupset_name": "defaultBackupSet",
            ...             "vm_group_id": 18,
            ...             "vm_guid": "i-0d485455929da6c11",
            ...             "vm_name": "WindowsTestVM1",
            ...             "source_vendor": "AMAZON",
            ...             "workload": "VM",
            ...             "execution_order": 1
            ...         }
            ...     ]
            ... }
            >>> target = {
            ...     "target_id": 1234567890,
            ...     "target_name": "Cleanroom_Target",
            ...     "target_vendor": "AZURE_V2"
            ... }
            >>> region = {
            ...     "guid": "eastus (Commcell)",
            ...     "name": "US East"
            ... }
            >>> node = {
            ...     "access_node_id": 1234567890,
            ...     "access_node_type": 3
            ... }
            >>> payload = runbook.populate_payload(entities, target, region, node)
            >>> print(payload)
            # The returned payload can be used for runbook creation.

        #ai-gen-doc
        """
        if not isinstance(entities['name'], str):
            raise SDKException('RecoveryGroup', '101', 'Missing or invalid Runbook name')
        api_payload = {
                        "name": entities.get('name', 'cleanroom_runbook'),
                        "target": {
                            "options": {
                            "region": region if region else {},
                            "accessNode": {}
                            }
                        },
                        "entities": [
                        ],
                        "advancedOptions": {
                            "postRecoveryActions": [
                            {
                                "scriptCredentials": {},
                                "guestCredentials": {}
                            }
                            ],
                            "delayBetweenPriorityMachines": 0,
                            "continueOnFailure": False,
                            "recoveryExpirationOptions": {
                            "enableExpirationOption": True,
                            "daysToExpire": 7,
                            "isRescuedCommServe": True,
                            "expirationTime": 0
                            }
                        }
                    }

        #Populate the payload with list of entities
        if not entities or not entities.get('entities'):
            raise SDKException('RecoveryGroup', '101', 'Payload cannot be empty')
        else:
            for item in entities['entities']:
                workload = None
                if item['workload'] == 'VM':
                    workload = 8
                elif item['workload'] == 'FILES':
                    workload = 9
                else:
                    raise SDKException('RecoveryGroup', '101', 'Invalid workload type provided in payload')
                entity = {
                    "instance": {
                        "id": item.get('instance_id', 0),
                        "name": item.get("instance_name", "string")
                    },
                    "backupSet": {
                        "id": item.get('backupset_id', 0),
                        "name": item.get("backupset_name", "string")
                    },
                    "client": {
                        "id": item.get('hypervisor_id', 0) if item.get('hypervisor_id') else item.get('client_id', 0),
                        "name": item.get("hypervisor_name", "string") if item.get('hypervisor_name') else item.get('client_name', "string"),
                    },
                    "workload": workload,
                    "executionOrder": {
                        "priority": item.get('execution_order', 0)
                    },
                    "recoveryPointDetails": {
                        "inheritedFrom": "RECOVERY_GROUP",
                        "entityRecoveryPoint": 0,
                        "entityRecoveryPointCategory": "LATEST"
                    }              
                }
                if workload == 8:  # VM workload
                    vm_info = {
                        "vmGroup": {
                            "id": item.get("vm_group_id", 0)
                        },
                        "virtualMachine": {
                            "GUID": item.get("vm_guid", "<vm_guid>"),
                            "name": item.get("vm_name", "string")
                        },
                        "sourceVendor": item.get("source_vendor", "VMW")
                    }
                    entity.update(vm_info)
                elif workload == 9:  # FILES workload
                    file_info = {
                        "subclient": {
                            "id": item.get("subclient_id", 0),
                            "name": item.get("subclient_name", "string")
                        }
                    }
                    entity.update(file_info)
                api_payload['entities'].append(entity)
        #Populate the payload with target details
        #Populate the payload with access node details
        if node.get('access_node_id') is not None:  #Using existing access node or access node group
            access_node_entity = {
                "id": node.get('access_node_id', 0),
                "name": node.get('access_node_name', 'string'),
                "type": node.get('access_node_type', 3)
            }
            api_payload['target']['options']['accessNode'].update(access_node_entity)
        if not target:
            raise SDKException('RecoveryGroup', '101', 'Target payload cannot be empty')
        elif target.get('target_id') is not None and target.get('target_id') > 0 :  #Using existing target
            target_entity = {
                "entity": {
                "id": target.get('target_id', 0),
                "name": target.get('target_name', 'string')
                }
            }
            api_payload['target'].update(target_entity)
        else:
            options = {
                        "vendor": target.get('target_vendor', 'AZURE_V2')
                    }
            api_payload['target']['options'].update(options) 
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
                    api_payload['target']['options'].update(existing_hypervisor)
                    api_payload['target']['options']['accessNode'].update(access_node_entity)
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
                    api_payload['target']['options'].update(options)
        return api_payload
