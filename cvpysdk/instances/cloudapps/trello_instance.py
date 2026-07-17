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

"""File for operating on a Trello Instance.

TrelloInstance is the only class defined in this file.

TrelloInstance: Derived class from CloudAppsInstance Base class, representing a
Trello Cloud Apps instance, and to perform operations on that instance

TrelloInstance:

    _get_instance_properties()  --  Instance class method overwritten to parse
                                    Trello-specific custom properties

    restore_in_place()          --  Submits an in-place restore job for the given paths

"""
from typing import Any, List, Optional

from ..cainstance import CloudAppsInstance


class TrelloInstance(CloudAppsInstance):
    """Represents an instance of the Trello Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account, proxy client)
    are inherited from CloudAppsInstance. This class adds optional Trello-specific
    properties parsed from customProperties when available.

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new TrelloInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Trello instance.
            instance_name: The name of the Trello instance.
            instance_id: Optional unique identifier for the instance.
        """
        self._tenant_name = None
        super(TrelloInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self) -> None:
        """Retrieve Trello-specific custom properties.

        Parses the common cloud apps fields via parent implementation and then
        extracts workload-specific keys from customProperties when present.
        """
        super(TrelloInstance, self)._get_instance_properties()
        self._tenant_name = None

        cloud_apps_instance = self._properties.get('cloudAppsInstance', {})
        custom_props = cloud_apps_instance.get('customProperties', {})
        name_values = custom_props.get('nameValues', [])
        for item in name_values:
            if item.get('name') == 'tenantName':
                self._tenant_name = item.get('value')

    @property
    def tenant_name(self) -> Optional[str]:
        """Get the tenant name configured for this Trello instance.

        Returns:
            str | None: Tenant/workspace name when available.

        #ai-gen-doc
        """
        return self._tenant_name

    def restore_in_place(
        self,
        paths: List[str],
        overwrite: bool = True,
        copy_precedence: int = 0,
        **kwargs: Any
    ):
        """Submit an in-place restore job for the specified Trello paths.

        Args:
            paths: List of paths/items to restore.
            overwrite: Whether to overwrite existing data. Defaults to True.
            copy_precedence: Copy precedence to use. Defaults to 0.
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
