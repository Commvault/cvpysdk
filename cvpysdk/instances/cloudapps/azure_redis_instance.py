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

"""File for operating on an Azure Redis Instance.

AzureRedisInstance is the only class defined in this file.

AzureRedisInstance: Derived class from CloudAppsInstance Base class, representing an
Azure Redis Cloud Apps instance, and to perform operations on that instance

AzureRedisInstance:

    _get_instance_properties()  --  Instance class method overwritten to add Azure Redis-specific
                                    cloud apps instance properties

    restore_in_place()          --  Submits an in-place restore job for the given paths

AzureRedisInstance Attributes:

    instance_type       --  Returns the Azure Redis instance type (86)
    credential_name     --  Returns the credential name used for authentication
    credential_id       --  Returns the credential ID used for authentication
    plan_name           --  Returns the plan name associated with this instance
    account_name        --  Returns the account name (client name)

"""
import json
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class AzureRedisInstance(CloudAppsInstance):
    """
    Represents an instance of the Azure Redis Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account)
    are inherited from CloudAppsInstance.  This class adds Azure Redis-specific
    properties and the restore_in_place method.

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new AzureRedisInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Azure Redis instance.
            instance_name: The name of the Azure Redis instance.
            instance_id: Optional; the unique identifier for the instance.
        """
        super(AzureRedisInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve Azure Redis-specific instance properties.

        Common properties (instance type, credential name/id, plan, account, proxy client)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        This method only extracts Azure Redis-specific fields if needed.
        """
        super(AzureRedisInstance, self)._get_instance_properties()

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            general_props = cloud_apps_instance.get('generalCloudProperties', {})
            custom_props = general_props.get('customProperties', {})
            # Azure Redis specific properties can be extracted here if needed

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified Azure Redis resource group paths.

        Args:
            paths: List of resource group paths to restore, e.g. ["/resource-group-name"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = azure_redis_instance.restore_in_place(paths=["/resource-group-name"])

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
