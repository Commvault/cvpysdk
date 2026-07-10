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

"""File for operating on a HubSpot Instance.

HubSpotInstance is the only class defined in this file.

HubSpotInstance: Derived class from CloudAppsInstance Base class, representing a
HubSpot Cloud Apps instance, and to perform operations on that instance

HubSpotInstance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
                                    instance properties as well

    restore_in_place()          --  Submits an in-place restore job for the given paths

HubSpotInstance Attributes:

    instance_type       --  Returns the HubSpot instance type (98)
    credential_name     --  Returns the credential name
    credential_id       --  Returns the credential ID
    plan_name           --  Returns the associated plan name
    account_name        --  Returns the account name

"""
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class HubSpotInstance(CloudAppsInstance):
    """
    Represents an instance of the HubSpot Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account)
    are inherited from CloudAppsInstance. This class only adds the
    restore_in_place method for HubSpot-specific restore operations.

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new HubSpotInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this HubSpot instance.
            instance_name: The name of the HubSpot instance.
            instance_id: Optional; the unique identifier for the instance.
        """
        super(HubSpotInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve HubSpot-specific instance properties.

        Common properties (instance type, credential name/id, plan, account)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        HubSpot has no additional workload-specific properties beyond the common set.
        """
        super(HubSpotInstance, self)._get_instance_properties()

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified HubSpot object paths.

        Args:
            paths: List of HubSpot object paths to restore, e.g. ["/CRM", "/Marketing"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = hubspot_instance.restore_in_place(paths=["/CRM"], overwrite=True)

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
