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

"""File for operating on Azure object storage instances.

ObjectStorageAzureBase:         Base class with shared GRP discovery operations and common
                                Azure storage properties.

AzureBlobStorageInstance:        Azure Blob Storage instance (instance type 6).

AzureDataLakeStorageInstance:   Azure Data Lake Storage Gen2 instance (instance type 21).

AzureBlobDiscoveryInstance:     Azure Blob Discovery GRP instance (instance type 45).

AzureFilesStorageInstance:     Azure Files Storage instance.

ObjectStorageAzureBase:

    update_discovery_grp_rules()    --  Update discovery rules on the GRP instance.

    run_discovery()                 --  Trigger discovery on the GRP instance.

"""

from typing import Any, Optional

from .cloud_storage_instance import CloudStorageInstance
from ...exception import SDKException


class ObjectStorageAzureBase(CloudStorageInstance):
    """Base class for all Azure object storage instances.

    Provides shared Azure storage properties and operations such as
    discovery rule management and discovery execution for GRP instances.
    Child classes set their specific endpoint URL suffix.
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize ObjectStorageAzureBase.

        Args:
            agent_object: The agent object associated with this instance.
            instance_name: The name of the instance.
            instance_id: Optional unique identifier for the instance.
        """
        super(ObjectStorageAzureBase, self).__init__(
            agent_object, instance_name, instance_id
        )
        self.url = ""

    def update_discovery_grp_rules(
            self,
            plan_name,
            rule_display_name='All storage accounts',
            rule_type=1000,
            rule_value='',
            match_type=1
        ):
        """Update discovery rules on this Azure Blob Discovery GRP instance.

        Step 2 of the GRP-based Azure Blob instance creation workflow.

        Args:
            plan_name: Plan name to associate with rule.
            rule_display_name: Display name for the rule (default: 'All storage accounts').
            rule_type: Rule type for discovery matching:
                    - 1000: Discover all storage accounts.
                    - 2: Match storage account by name.
            rule_value: Value to match (empty for 'all', or account name for type 2).
            match_type: Match type (1=contains).

        Raises:
            SDKException: On API failure.
        """
        plan_id = None
        plan_name_resolved = plan_name.strip()
        if self._commcell_object.plans.has_plan(plan_name_resolved):
            plan_obj = self._commcell_object.plans.get(plan_name_resolved)
            plan_id = int(plan_obj.plan_id)
        else:
            raise SDKException(
                'Instance', '102',
                f'Plan "{plan_name_resolved}" not found on CommCell'
            )

        request_json = {
            'instanceProperties': {
                'instance': {
                    'clientName': self._agent_object._client_object.client_name,
                    'clientId': int(self._agent_object._client_object.client_id),
                    'instanceName': self.instance_name,
                    'instanceId': int(self.instance_id),
                    'applicationId': 134,
                    '_type_': 5,
                },
                'cloudAppsInstance': {
                    'instanceType': 45,
                    'azureResourceDiscoveryInstance': {
                        'crdInstanceType': {
                            'discoveryTarget': {
                                'targetInstanceType': 6,
                                'targetAppType': 134
                            }
                        },
                        'discoveryRules': {
                            'rules': [{
                                'matchCriteria': 1,
                                'discoveryTargetType': {
                                    'targetInstanceType': 6,
                                    'targetAppType': 134
                                },
                                'region': {},
                                'ruleGroups': [{
                                    'matchCriteria': 1,
                                    'ruleEntities': [{
                                        'planEntity': {
                                            'planId': plan_id,
                                            'planName': plan_name_resolved
                                        },
                                        'ruleDefinition': {
                                            'displayName': rule_display_name,
                                            'type': int(rule_type),
                                            'value': rule_value,
                                            'matchType': int(match_type)
                                        }
                                    }]
                                }]
                            }]
                        },
                        'disableBackupForItemsNoLongerMatching': False
                    },
                    'generalCloudProperties': {
                        'memberServers': []
                    },
                    'objectStorageInstance': {}
                },
                'planEntity': {
                    'planId': plan_id
                }
            },
            'useResourcePoolInfo': False
        }

        instance_url = self._commcell_object._services['INSTANCE'] % self.instance_id
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', instance_url, request_json
        )

        if flag:
            response_data = response.json() if response.text else {}
            if isinstance(response_data, list):
                response_data = response_data[0] if response_data else {}
            if not isinstance(response_data, dict):
                return
            resp_inner = response_data.get('response', {})
            if isinstance(resp_inner, list):
                resp_inner = resp_inner[0] if resp_inner else {}
            if not isinstance(resp_inner, dict):
                resp_inner = {}
            error_code = response_data.get('errorCode', resp_inner.get('errorCode', 0))
            if error_code != 0:
                error_string = response_data.get('errorMessage', resp_inner.get('errorString', ''))
                raise SDKException('Instance', '102',
                                   f'Error updating GRP rules\nError: "{error_string}"')
            return
        raise SDKException('Response', '101', self._update_response_(response.text))

    def run_discovery(self):
        """Trigger discovery on this Azure Blob Discovery GRP instance.

        Step 3 of the GRP-based Azure Blob instance creation workflow.
        This triggers a discovery job that auto-creates Azure Blob storage instances.

        Returns:
            str: Job ID of the discovery task (or None if not returned).

        Raises:
            SDKException: On API failure.
        """
        request_json = {
            'taskInfo': {
                'associations': [{
                    'clientId': int(self._agent_object._client_object.client_id),
                    'clientName': self._agent_object._client_object.client_name,
                    'instanceId': int(self.instance_id),
                    'instanceName': self.instance_name,
                    'applicationId': 134,
                    'appName': 'Cloud Apps',
                    'displayName': self._agent_object._client_object.client_name,
                    'entityInfo': {
                        'companyId': 0,
                        'companyName': 'Commcell',
                        'multiCommcellId': 0
                    }
                }],
                'subTasks': [{
                    'subTask': {
                        'operationType': 4048,
                        'subTaskType': 1
                    },
                    'options': {}
                }],
                'task': {
                    'taskType': 1
                }
            }
        }

        create_task_url = self._commcell_object._services['CREATE_TASK']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', create_task_url, request_json
        )

        if flag:
            response_data = response.json() if response.text else {}
            if isinstance(response_data, list):
                response_data = response_data[0] if response_data else {}
            error_code = response_data.get('errorCode', 0)
            if error_code != 0:
                error_message = response_data.get('errorMessage', '')
                raise SDKException('Instance', '102',
                                   f'Discovery failed\nError: "{error_message}"')
            job_id = response_data.get('jobIds', [None])
            if isinstance(job_id, list) and job_id:
                job_id = job_id[0]
            elif not isinstance(job_id, (str, int)):
                job_id = response_data.get('taskId')
            return str(job_id) if job_id else None
        raise SDKException('Response', '101', self._update_response_(response.text))


class AzureBlobStorageInstance(ObjectStorageAzureBase):
    """Represents an Azure Blob Storage instance (instance type 6)."""

    def __init__(
            self,
            agent_object: Any,
            instance_name: str,
            instance_id: Optional[int] = None
        ) -> None:
        """Initialize an Azure Blob Storage instance.

        Args:
            agent_object: Agent object that owns this instance.
            instance_name: Name of the Azure Blob storage instance.
            instance_id: Optional instance ID when known.

        Returns:
            None

        Example:
            >>> instance = AzureBlobStorageInstance(agent_obj, 'azure_blob_inst', 101)
            >>> instance.url
            'blob.core.windows.net'
        """
        super(AzureBlobStorageInstance, self).__init__(
            agent_object, instance_name, instance_id
        )
        self.url = "blob.core.windows.net"


class AzureDataLakeStorageInstance(ObjectStorageAzureBase):
    """Represents an Azure Data Lake Storage Gen2 instance (instance type 21)."""

    def __init__(
            self,
            agent_object: Any,
            instance_name: str,
            instance_id: Optional[int] = None
        ) -> None:
        """Initialize an Azure Data Lake Storage Gen2 instance.

        Args:
            agent_object: Agent object that owns this instance.
            instance_name: Name of the Azure Data Lake Gen2 instance.
            instance_id: Optional instance ID when known.

        Returns:
            None

        Example:
            >>> instance = AzureDataLakeStorageInstance(agent_obj, 'adls_gen2_inst', 202)
            >>> instance.url
            'dfs.core.windows.net'
        """
        super(AzureDataLakeStorageInstance, self).__init__(
            agent_object, instance_name, instance_id
        )
        self.url = "dfs.core.windows.net"


class AzureBlobDiscoveryInstance(ObjectStorageAzureBase):
    """Represents an Azure Blob Discovery GRP instance (instance type 45)."""


class AzureFilesStorageInstance(ObjectStorageAzureBase):
    """Represents an Azure Files Storage instance."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        super(AzureFilesStorageInstance, self).__init__(
            agent_object, instance_name, instance_id
        )
        self.url = "file.core.windows.net"
