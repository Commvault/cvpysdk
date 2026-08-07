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

"""File for operating on a GCPFirestore Instance.

GCPFirestoreInstance is the only class defined in this file.

GCPFirestoreInstance:  Derived class from CloudAppsInstance Base class, representing a
GCPFirestore Cloud Apps instance, and to perform operations on that instance

GCPFirestoreInstance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
                                    instance properties as well

    restore_in_place()          --  Submits an in-place restore job

GCPFirestoreInstance Attributes:

    instance_type       --  Returns the GCPFirestore instance type (89)
    credential_name     --  Returns the credential name
    credential_id       --  Returns the credential ID
    plan_name           --  Returns the associated plan name
    account_name        --  Returns the account name

"""
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class GCPFirestoreInstance(CloudAppsInstance):
    """
    Represents an instance of the GCPFirestore Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account, proxy client)
    are inherited from CloudAppsInstance. This class adds GCPFirestore-specific
    properties and the restore_in_place method.

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new GCPFirestoreInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this GCPFirestore instance.
            instance_name: The name of the GCPFirestore instance.
            instance_id: Optional; the unique identifier for the instance.

        #ai-gen-doc
        """
        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        super(GCPFirestoreInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve GCPFirestore-specific instance properties.

        Common properties (instance type, credential name/id, plan, account, proxy client)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        This method extracts GCPFirestore-specific fields if any.

        #ai-gen-doc
        """
        super(GCPFirestoreInstance, self)._get_instance_properties()

        # Reset all private fields
        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        # Parse cloud apps instance properties
        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance.get('instanceType')

            if 'generalCloudProperties' in cloud_apps_instance:
                general_props = cloud_apps_instance['generalCloudProperties']

                # Credential
                if 'credentials' in general_props:
                    creds = general_props['credentials']
                    self._credential_name = creds.get('credentialName')
                    self._credential_id = creds.get('credentialId')

        # Plan
        plan = self._properties.get('planEntity', {})
        self._plan_name = plan.get('planName')

        # Account name (client name)
        instance_info = self._properties.get('instance', {})
        self._account_name = instance_info.get('clientName')

    @property
    def instance_type(self) -> Optional[int]:
        """Get the GCPFirestore instance type.

        Returns:
            The instance type integer (89), or None if not set.

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def credential_name(self) -> Optional[str]:
        """Get the credential name for this GCPFirestore instance.

        Returns:
            The credential name as a string, or None if not configured.

        #ai-gen-doc
        """
        return self._credential_name

    @property
    def credential_id(self) -> Optional[int]:
        """Get the credential ID for this GCPFirestore instance.

        Returns:
            The credential ID as an integer, or None if not configured.

        #ai-gen-doc
        """
        return self._credential_id

    @property
    def plan_name(self) -> Optional[str]:
        """Get the plan name associated with this GCPFirestore instance.

        Returns:
            The plan name as a string, or None if not configured.

        #ai-gen-doc
        """
        return self._plan_name

    @property
    def account_name(self) -> Optional[str]:
        """Get the account name for this GCPFirestore instance.

        Returns:
            The account name as a string, or None if not configured.

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
        """Submit an in-place restore job for the specified GCPFirestore database paths.

        Args:
            paths: List of database paths to restore, e.g. ["/MY_DB"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = gcp_firestore_instance.restore_in_place(paths=["/MY_DB"], overwrite=True)

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
