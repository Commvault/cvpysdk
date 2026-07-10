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

"""File for operating on a GCP Memorystore Instance.

GcpMemorystoreInstance is the only class defined in this file.

GcpMemorystoreInstance: Derived class from CloudAppsInstance Base class, representing a
GCP Memorystore Cloud Apps instance, and to perform operations on that instance

GcpMemorystoreInstance:

    _get_instance_properties()  --  Instance class method overwritten to add GCP Memorystore-specific
                                    cloud apps instance properties

    restore_in_place()          --  Submits an in-place restore job for the given paths

GcpMemorystoreInstance Attributes:

    instance_type       --  Returns the GCP Memorystore instance type (82)
    credential_name     --  Returns the credential name used for authentication
    credential_id       --  Returns the credential ID used for authentication
    plan_name           --  Returns the plan name associated with this instance
    account_name        --  Returns the account name (client name)
    engine_type         --  Returns the engine type (e.g., 'redis')

"""
import json
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class GcpMemorystoreInstance(CloudAppsInstance):
    """
    Represents an instance of the GCP Memorystore Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account)
    are inherited from CloudAppsInstance.  This class adds GCP Memorystore-specific
    properties (engine_type) and the restore_in_place method.

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new GcpMemorystoreInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this GCP Memorystore instance.
            instance_name: The name of the GCP Memorystore instance.
            instance_id: Optional; the unique identifier for the instance.
        """
        self._engine_type = None

        super(GcpMemorystoreInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve GCP Memorystore-specific instance properties.

        Common properties (instance type, credential name/id, plan, account, proxy client)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        This method only extracts GCP Memorystore-specific fields (engine_type).
        """
        super(GcpMemorystoreInstance, self)._get_instance_properties()

        self._engine_type = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            general_props = cloud_apps_instance.get('generalCloudProperties', {})
            custom_props = general_props.get('customProperties', {})
            name_values = custom_props.get('nameValues', [])

            for nv in name_values:
                if nv.get('name') == 'WorkloadInstanceCustomProperties':
                    try:
                        props = json.loads(nv.get('value', '{}'))
                        self._engine_type = props.get('engine_type')
                    except (ValueError, TypeError):
                        pass

    @property
    def engine_type(self) -> Optional[str]:
        """Get the Memorystore engine type (e.g., 'redis').

        Returns:
            The engine type string, or None if not configured.

        #ai-gen-doc
        """
        return self._engine_type

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified GCP Memorystore region paths.

        Args:
            paths: List of region paths to restore, e.g. ["/us-central1"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = gcp_memorystore_instance.restore_in_place(paths=["/us-central1"])

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
