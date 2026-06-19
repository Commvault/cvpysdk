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

"""File for operating on a ClickHouse Instance.

ClickHouseInstance is the only class defined in this file.

ClickHouseInstance: Derived class from CloudAppsInstance Base class, representing a
ClickHouse Cloud Apps instance, and to perform operations on that instance

ClickHouseInstance:

    _get_instance_properties()  --  Instance class method overwritten to add ClickHouse-specific
                                    properties

    restore_in_place()          --  Submits an in-place restore job for the given paths

ClickHouseInstance Attributes:

    instance_type       --  Returns the ClickHouse instance type (84)
    credential_name     --  Returns the credential name
    credential_id       --  Returns the credential ID
    plan_name           --  Returns the associated plan name
    account_name        --  Returns the account name (client name)

"""
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class ClickHouseInstance(CloudAppsInstance):
    """
    Represents an instance of the ClickHouse Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account)
    are inherited from CloudAppsInstance. ClickHouse has no access node
    (has_access_node is fixed to no for all Velocity workloads).

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new ClickHouseInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this ClickHouse instance.
            instance_name: The name of the ClickHouse instance.
            instance_id: Optional; the unique identifier for the instance.
        """
        super(ClickHouseInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve ClickHouse-specific instance properties.

        Common properties (instance type, credential name/id, plan, account)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        ClickHouse has no workload-specific extra fields beyond those common ones.
        """
        super(ClickHouseInstance, self)._get_instance_properties()

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified ClickHouse database paths.

        Args:
            paths: List of database paths to restore, e.g. ["/my_db"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = clickhouse_instance.restore_in_place(paths=["/my_db"], overwrite=True)

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
