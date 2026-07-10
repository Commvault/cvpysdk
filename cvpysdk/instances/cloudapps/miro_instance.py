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

"""File for operating on a Miro Instance.

MiroInstance is the only class defined in this file.

MiroInstance:  Derived class from CloudAppsInstance Base class, representing a
               Miro Cloud Apps instance, and to perform operations on that instance

MiroInstance:

    _get_instance_properties()  --  Instance class method overwritten to add Miro-specific
                                    cloud apps instance properties

    restore_in_place()          --  Submits an in-place restore job for the given paths

MiroInstance Attributes:

    instance_type       --  Returns the Miro instance type (104)
    credential_name     --  Returns the credential name used for authentication
    credential_id       --  Returns the credential ID used for authentication
    plan_name           --  Returns the plan name associated with this instance
    account_name        --  Returns the account name (client name)
"""

from typing import List, Optional

from ..cainstance import CloudAppsInstance


class MiroInstance(CloudAppsInstance):
    """
    Represents an instance of the Miro Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account)
    are inherited from CloudAppsInstance.  This class only adds Miro-specific
    parsing and the restore_in_place method.

    #ai-gen-doc
    """

    def __init__(
        self,
        agent_object: object,
        instance_name: str,
        instance_id: str = None,
    ) -> None:
        """
        Initialize a new MiroInstance object.

        All private fields are set to ``None`` before the parent ``__init__``
        so that ``_get_instance_properties()`` starts from a clean state.

        Args:
            agent_object: Instance of the Agent class associated with this Miro instance.
            instance_name (str): The name of the Miro instance.
            instance_id (str): Optional unique identifier for the instance.

        #ai-gen-doc
        """
        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        super(MiroInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """
        Retrieve Miro-specific instance properties.

        Delegates common parsing (instance type, credentials, plan, account)
        to the parent ``CloudAppsInstance._get_instance_properties()``.
        Resets all private fields to ``None`` before re-parsing.

        #ai-gen-doc
        """
        super(MiroInstance, self)._get_instance_properties()

        # Reset all fields before re-parsing
        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._plan_name = None
        self._account_name = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance.get('instanceType')

            general_props = cloud_apps_instance.get('generalCloudProperties', {})
            cred = general_props.get('credentials', {})
            self._credential_name = cred.get('credentialName')
            self._credential_id = cred.get('credentialId')

        if 'planEntity' in self._properties:
            self._plan_name = self._properties['planEntity'].get('planName')

        if 'instance' in self._properties:
            self._account_name = self._properties['instance'].get('clientName')

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def instance_type(self) -> Optional[int]:
        """
        Return the Miro instance type integer (104).

        Returns:
            int: The cloud apps instance type for Miro.

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def credential_name(self) -> Optional[str]:
        """
        Return the credential name used for Miro authentication.

        Returns:
            str: The credential entity name, or None if not set.

        #ai-gen-doc
        """
        return self._credential_name

    @property
    def credential_id(self) -> Optional[int]:
        """
        Return the credential ID used for Miro authentication.

        Returns:
            int: The credential entity ID, or None if not set.

        #ai-gen-doc
        """
        return self._credential_id

    @property
    def plan_name(self) -> Optional[str]:
        """
        Return the plan name associated with this Miro instance.

        Returns:
            str: The plan name, or None if not set.

        #ai-gen-doc
        """
        return self._plan_name

    @property
    def account_name(self) -> Optional[str]:
        """
        Return the account name (Commvault client name) for this Miro instance.

        Returns:
            str: The client/account name, or None if not set.

        #ai-gen-doc
        """
        return self._account_name

    # ------------------------------------------------------------------
    # Restore
    # ------------------------------------------------------------------

    def restore_in_place(
        self,
        paths: List[str],
        overwrite: bool = True,
        copy_precedence: int = 0,
        **kwargs,
    ):
        """
        Submit an in-place restore job for the specified Miro board paths.

        Args:
            paths (List[str]): List of board paths to restore,
                               e.g. ["/BoardName__cvbid12<encodedId>"].
            overwrite (bool): Whether to overwrite existing data during restore.
                              Defaults to True.
            copy_precedence (int): Copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to ``_restore_in_place``.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = miro_instance.restore_in_place(
            ...     paths=["/MyBoard__cvbid12uXjVHO0_AJU="], overwrite=True
            ... )

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs,
        )
