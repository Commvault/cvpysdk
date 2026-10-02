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

"""Module for Cloud Configuration (Cloud Config) SDK operations.

Classes:
    CloudConfig:
        Provides methods to interact with the Cloud Config REST APIs.

        Methods:
            create_hypervisor()             -- Create a new Cloud Config hypervisor / connection.
            get_client_details()            -- Retrieve Cloud Config client details and subclient map.
            get_discovery_subclient_id()    -- Extract the discovery subclient ID from client details.
            update_subclient()              -- Update a Cloud Config subclient (e.g., assign a plan).
            get_subclient_details()         -- Retrieve details for a Cloud Config subclient.
            create_subclient()              -- Create a new Cloud Config subclient (configuration group).
            restore_subclient()             -- Trigger a restore job for a Cloud Config subclient.
"""

from typing import Any, Dict, Optional

from .exception import SDKException
from .job import Job


class CloudConfig:
    """Provides Cloud Configuration SDK operations via v4/Cloud/CloudConfig and v4/Hypervisor APIs.

    Args:
        commcell_object (Commcell): The Commcell object to use for communication.

    Example:
        >>> cloud_config = CloudConfig(commcell)
        >>> client_id = cloud_config.create_hypervisor(payload)
        >>> details = cloud_config.get_client_details(client_id)
        >>> discovery_subclient_id = cloud_config.get_discovery_subclient_id(details)
    """

    def __init__(self, commcell_object):
        """Initialize CloudConfig with a Commcell object.

        Args:
            commcell_object (Commcell): The Commcell instance used for API communication.
        """
        self._commcell = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services

    def create_hypervisor(self, payload: Dict[str, Any]) -> int:
        """Create a new Cloud Config hypervisor (connection) via POST /v4/Hypervisor.

        Args:
            payload (dict): Request payload for hypervisor creation. Must include fields like
                ``name``, ``hypervisorType``, ``enableCloudConfigProtection``, ``credentials``,
                ``accessNodes``, ``subscriptionId``, etc.

        Returns:
            int: The client ID of the newly created hypervisor.

        Raises:
            SDKException: If the API call fails or the response is unexpected.

        Example:
            >>> payload = {
            ...     "skipCredentialValidation": False,
            ...     "useHostedInfrastructure": False,
            ...     "name": "automation-connection",
            ...     "hypervisorType": "AZURE_V2",
            ...     "enableCloudConfigProtection": True,
            ...     "credentials": {"id": 8, "name": "lalith-dev2-app-creds"},
            ...     "accessNodes": [{"id": "4", "name": "lalith-cloudconfig-proxy-lincs2", "type": 3}],
            ...     "subscriptionId": "fe424870-d00f-487e-9034-717b1845202d",
            ...     "useManagedIdentity": False,
            ...     "AzureCloudConfigAuthType": "APPLICATION"
            ... }
            >>> client_id = cloud_config.create_hypervisor(payload)
        """
        url = self._services['CREATE_CLOUD_CONFIG_HYPERVISOR']
        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json():
                resp = response.json()
                response_node = resp.get('response', {})
                error_code = response_node.get('errorCode', resp.get('errorCode', 0))
                if error_code != 0:
                    error_message = response_node.get('errorMessage') or resp.get('errorMessage', 'Unknown error')
                    raise SDKException('Response', '101', error_message)
                # POST /v4/Hypervisor returns {"response": {"hypervisorId": <id>, ...}}
                client_id = response_node.get('hypervisorId') or resp.get('hypervisorId') or resp.get('clientId')
                if client_id is None:
                    raise SDKException('Response', '102', 'hypervisorId not found in hypervisor creation response')
                return int(client_id)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_client_details(self, client_id: int) -> Dict[str, Any]:
        """Retrieve Cloud Config client details via GET /v4/Cloud/CloudConfig/Client/{clientId}.

        Args:
            client_id (int): The client ID of the hypervisor whose details are needed.

        Returns:
            dict: The full response JSON containing client details and subclient list.

        Raises:
            SDKException: If the API call fails or the response is unexpected.

        Example:
            >>> details = cloud_config.get_client_details(414)
            >>> discovery_id = cloud_config.get_discovery_subclient_id(details)
        """
        url = self._services['GET_CLOUD_CONFIG_CLIENT_DETAILS'] % client_id
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_discovery_subclient_id(self, client_details: Dict[str, Any]) -> int:
        """Extract the discovery subclient ID from the Cloud Config client details response.

        The response contains a top-level ``discoverySubclient`` object with an ``id`` field::

            {"discoverySubclient": {"name": "default", "id": 807, ...}}

        Args:
            client_details (dict): Response dict from :meth:`get_client_details`.

        Returns:
            int: The subclient ID of the discovery subclient.

        Raises:
            SDKException: If the discovery subclient ID is not found in the response.

        Example:
            >>> details = cloud_config.get_client_details(414)
            >>> disc_id = cloud_config.get_discovery_subclient_id(details)
        """
        discovery_subclient = client_details.get('discoverySubclient', {})
        subclient_id = discovery_subclient.get('id')
        if not subclient_id:
            raise SDKException(
                'Response', '102',
                'discoverySubclient.id not found in Cloud Config client details response'
            )
        return int(subclient_id)

    def update_subclient(self, subclient_id: int, payload: Dict[str, Any]) -> bool:
        """Update a Cloud Config subclient via PUT /v4/Cloud/CloudConfig/Subclient/{subclientId}.

        Typically used to assign or change the backup plan for a subclient.

        Args:
            subclient_id (int): The ID of the subclient to update.
            payload (dict): Update payload, e.g. ``{"plan": {"name": "plan-name", "id": 1}}``.

        Returns:
            bool: True if the update was successful.

        Raises:
            SDKException: If the API call fails or the response is unexpected.

        Example:
            >>> cloud_config.update_subclient(
            ...     304,
            ...     {"plan": {"name": "lalith-azure-cloud-plan1", "id": 1}}
            ... )
        """
        url = self._services['UPDATE_CLOUD_CONFIG_SUBCLIENT'] % subclient_id
        flag, response = self._cvpysdk_object.make_request('PUT', url=url, payload=payload)

        if flag:
            return True
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_subclient_details(self, subclient_id: int) -> Dict[str, Any]:
        """Retrieve details of a Cloud Config subclient via GET /v4/Cloud/CloudConfig/Subclient/{subclientId}.

        Args:
            subclient_id (int): The subclient ID to query.

        Returns:
            dict: The full response JSON containing subclient details.

        Raises:
            SDKException: If the API call fails or the response is unexpected.

        Example:
            >>> details = cloud_config.get_subclient_details(304)
        """
        url = self._services['GET_CLOUD_CONFIG_SUBCLIENT_DETAILS'] % subclient_id
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def create_subclient(self, payload: Dict[str, Any]) -> int:
        """Create a new Cloud Config subclient (configuration group) via POST /v4/Cloud/CloudConfig/Subclient.

        Args:
            payload (dict): Creation payload. Must include ``name``, ``content``,
                ``hypervisor``, and ``plan`` fields.

        Returns:
            int: The subclient ID of the newly created configuration group subclient.

        Raises:
            SDKException: If the API call fails or the response is unexpected.

        Example:
            >>> payload = {
            ...     "name": "automation-configgroup",
            ...     "content": {
            ...         "contentRuleGroups": [{
            ...             "matchRule": "ALL",
            ...             "rules": [
            ...                 {"type": "RESOURCE_GROUP", "condition": "EQUALS", "value": "open-emr"},
            ...                 {"type": "TAG_VALUE", "condition": "EQUALS", "value": "opnemr-true"}
            ...             ]
            ...         }]
            ...     },
            ...     "hypervisor": {"id": 414, "name": "automation-hyp1-2608"},
            ...     "plan": {"id": 1, "name": "lalith-azure-cloud-plan1"}
            ... }
            >>> subclient_id = cloud_config.create_subclient(payload)
        """
        url = self._services['CREATE_CLOUD_CONFIG_SUBCLIENT']
        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json():
                resp = response.json()
                response_node = resp.get('response', {})
                error_code = response_node.get('errorCode', resp.get('errorCode', 0))
                if error_code != 0:
                    error_message = response_node.get('errorMessage') or resp.get('errorMessage', 'Unknown error')
                    raise SDKException('Response', '101', error_message)
                # POST /v4/Cloud/CloudConfig/Subclient returns {"response": {"entity": {"subclientId": <id>}}}
                subclient_id = response_node.get('entity', {}).get('subclientId') or resp.get('subclientId')
                if not subclient_id:
                    raise SDKException('Response', '102', 'subclientId not found in create subclient response')
                return int(subclient_id)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def backup_subclient(self, subclient_id: int, backup_level: str = "Full") -> 'Job':
        """Trigger a backup on a Cloud Config subclient via the standard SUBCLIENT_BACKUP endpoint.

        Args:
            subclient_id (int): The subclient ID to back up.
            backup_level (str): Backup level. Supported values: ``"Full"``, ``"Incremental"``,
                ``"Differential"``, ``"Synthetic_full"``. Defaults to ``"Full"``.

        Returns:
            Job: A Job instance representing the triggered backup job.

        Raises:
            SDKException: If the API call fails or the response is unexpected.

        Example:
            >>> job = cloud_config.backup_subclient(304, backup_level="Full")
            >>> job.wait_for_completion()
        """
        backup_request = backup_level.lower()
        url = self._services['SUBCLIENT_BACKUP'] % (subclient_id, backup_request)
        flag, response = self._cvpysdk_object.make_request('POST', url=url)

        if flag:
            if response.json():
                resp = response.json()
                job_id = resp.get('jobIds', [None])[0]
                if job_id is None:
                    raise SDKException('Response', '102', 'jobId not found in backup response')
                return Job(self._commcell, int(job_id))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def restore_subclient(
        self,
        subclient_id: int,
        payload: Dict[str, Any]
    ) -> 'Job':
        """Trigger a restore job for a Cloud Config subclient via POST /v4/Cloud/CloudConfig/Subclient/{subclientId}/Restore.

        Args:
            subclient_id (int): The subclient ID to restore from.
            payload (dict): Restore payload including ``cloudConfigDestinationInfo`` with
                Azure region mapping, restore configuration, destination connection client ID,
                subclient list, and source job ID.

        Returns:
            Job: A Job instance representing the triggered restore job.

        Raises:
            SDKException: If the API call fails or the response is unexpected.

        Example:
            >>> payload = {
            ...     "cloudConfigDestinationInfo": {
            ...         "azure": {
            ...             "regionMapping": [{"sourceRegion": "eastus", "targetRegion": "southindia"}],
            ...             "restoreConfiguration": {
            ...                 "enablePrivateIpRetention": True,
            ...                 "resourceGroupMapping": [],
            ...                 "vnetMapping": [],
            ...                 "tags": [],
            ...                 "resourcePrefixConfiguration": {
            ...                     "resourceNamePrefix": "automation-recovery-prefix-",
            ...                     "applyPrefixToGloballyUniqueOnly": True
            ...                 }
            ...             }
            ...         },
            ...         "destCloudConnectionClientId": 414,
            ...         "cloudConfigSubclients": [{"id": 304, "name": "cr7-group1-0605"}]
            ...     },
            ...     "jobId": 26473
            ... }
            >>> job = cloud_config.restore_subclient(304, payload)
            >>> job.wait_for_completion()
        """
        url = self._services['RESTORE_CLOUD_CONFIG_SUBCLIENT'] % subclient_id
        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json():
                resp = response.json()
                error_code = resp.get('errorCode', 0)
                if error_code != 0:
                    error_message = resp.get('errorMessage', 'Unknown error')
                    raise SDKException('Response', '101', error_message)
                job_id = resp.get('jobId') or resp.get('jobIds', [None])[0]
                if job_id is None:
                    raise SDKException('Response', '102', 'jobId not found in restore response')
                return Job(self._commcell, int(job_id))
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_restore_metadata(self, job_id: int, client_id: int) -> Dict[str, Any]:
        """Fetch restore metadata for a Cloud Config restore job.

        Calls GET /v4/Cloud/CloudConfig/Job/{jobId}/RestoreMetadata?clientId={clientId}.

        Args:
            job_id (int): Restore job ID.
            client_id (int): Hypervisor client ID for RBAC check.

        Returns:
            dict: Restore metadata response containing fields such as
                ``recoveredCloudResourceGroupIds``.

        Raises:
            SDKException: If the API call fails or returns invalid data.
        """
        url = self._services['GET_CLOUD_CONFIG_RESTORE_METADATA'] % (job_id, client_id)
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                return response.json()
            raise SDKException('Response', '102')

        response_string = self._commcell._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def reset_restore(
        self,
        subclient_id: int,
        restore_job_id: int,
        recovered_resource_group_ids: list
    ) -> bool:
        """Reset a Cloud Config restore job and clean up recovered Azure resources.

        Calls POST /v4/Cloud/CloudConfig/Subclient/{subclientId}/Restore/{restoreJobId}/reset.

        Args:
            subclient_id (int): Cloud Config subclient ID used for restore.
            restore_job_id (int): Restore job ID.
            recovered_resource_group_ids (list): Recovered resource group IDs from restore metadata.

        Returns:
            bool: True if reset API call succeeds.

        Raises:
            SDKException: If API call fails or returns errorCode != 0.
        """
        url = self._services['RESET_CLOUD_CONFIG_SUBCLIENT_RESTORE'] % (subclient_id, restore_job_id)
        payload = {
            "azure": {
                "recoveredResourceGroupIds": recovered_resource_group_ids
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json():
                resp = response.json()
                error_code = resp.get('errorCode', 0)
                if error_code != 0:
                    error_message = resp.get('errorMessage', 'Unknown error')
                    raise SDKException('Response', '101', error_message)
                return True
            raise SDKException('Response', '102')

        response_string = self._commcell._update_response_(response.text)
        raise SDKException('Response', '101', response_string)
