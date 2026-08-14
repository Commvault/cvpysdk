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

"""File for operating on a Klaviyo Instance.

KlaviyoInstance is the only class defined in this file.

KlaviyoInstance: Derived class from CloudAppsInstance Base class, representing a
Klaviyo Cloud Apps instance, and to perform operations on that instance

KlaviyoInstance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
                                    instance properties as well

    restore_in_place()          --  Submits an in-place restore job

KlaviyoInstance Attributes:

    instance_type       --  Returns the Klaviyo instance type (90)
    credential_name     --  Returns the credential name
    credential_id       --  Returns the credential ID
    plan_name           --  Returns the associated plan name
    account_name        --  Returns the account name

"""
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class KlaviyoInstance(CloudAppsInstance):
    """
    Represents an instance of the Klaviyo Cloud Apps service.

    This class extends the CloudAppsInstance base class and provides specialized methods
    for interacting with Klaviyo instances.

    Key Features:
        - Retrieve instance properties including credentials, plan, and account details
        - Submit in-place restore jobs for backed-up Klaviyo data
        - Property-based access to instance configuration

    Common properties inherited from CloudAppsInstance:
        - ca_instance_type: Returns the cloud apps instance type (90 for Klaviyo)
        - credential_name: Returns the credential name used for authentication
        - credential_id: Returns the credential ID used for authentication
        - plan_name: Returns the plan name associated with this instance
        - account_name: Returns the account name (client name)

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new KlaviyoInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Klaviyo instance.
            instance_name: The name of the Klaviyo instance.
            instance_id: Optional; the unique identifier for the instance.

        #ai-gen-doc
        """
        # Initialize all private fields to None before calling super()
        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        super(KlaviyoInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve Klaviyo-specific instance properties.

        Parses the instance properties response to extract Klaviyo-specific configuration
        including credential details, plan information, and account name.

        Common properties (instance type, credential name/id, plan, account) are parsed
        from the API response and stored as private attributes.

        #ai-gen-doc
        """
        super(KlaviyoInstance, self)._get_instance_properties()

        # Reset all fields
        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            general_props = cloud_apps_instance.get('generalCloudProperties', {})

            # Parse instance type
            self._ca_instance_type = cloud_apps_instance.get('instanceType')

            # Parse credential details
            credentials = general_props.get('credentials', {})
            self._credential_name = credentials.get('userName')
            self._credential_id = credentials.get('credentialId')

        # Parse plan information
        if 'planEntity' in self._properties:
            plan_entity = self._properties['planEntity']
            self._plan_name = plan_entity.get('planName')

        # Parse account name
        if 'instance' in self._properties:
            instance_info = self._properties['instance']
            self._account_name = instance_info.get('clientName')

    @property
    def instance_type(self) -> Optional[int]:
        """Get the Klaviyo instance type.

        Returns:
            int: The instance type identifier (90 for Klaviyo), or None if not set.

        Example:
            >>> print(klaviyo_instance.instance_type)
            90

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def credential_name(self) -> Optional[str]:
        """Get the credential name used for authentication.

        Returns:
            str: The credential name, or None if not configured.

        Example:
            >>> print(klaviyo_instance.credential_name)
            'klaviyo_29june_3'

        #ai-gen-doc
        """
        return self._credential_name

    @property
    def credential_id(self) -> Optional[int]:
        """Get the credential ID used for authentication.

        Returns:
            int: The credential ID, or None if not configured.

        Example:
            >>> print(klaviyo_instance.credential_id)
            34

        #ai-gen-doc
        """
        return self._credential_id

    @property
    def plan_name(self) -> Optional[str]:
        """Get the plan name associated with this instance.

        Returns:
            str: The plan name, or None if not configured.

        Example:
            >>> print(klaviyo_instance.plan_name)
            'DataVaultPlan'

        #ai-gen-doc
        """
        return self._plan_name

    @property
    def account_name(self) -> Optional[str]:
        """Get the account name (client name) for this instance.

        Returns:
            str: The account name, or None if not configured.

        Example:
            >>> print(klaviyo_instance.account_name)
            'klaviyo_29june_3'

        #ai-gen-doc
        """
        return self._account_name

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified Klaviyo content paths.

        Restores backed-up Klaviyo data (profiles, lists, and other configured content)
        to the original location.

        Args:
            paths: List of content paths to restore, e.g. ["/profiles", "/lists"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = klaviyo_instance.restore_in_place(paths=["/profiles"], overwrite=True)

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
