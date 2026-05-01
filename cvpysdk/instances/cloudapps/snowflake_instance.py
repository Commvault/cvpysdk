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

"""File for operating on a Snowflake Instance.

SnowflakeInstance is the only class defined in this file.

SnowflakeInstance: Derived class from CloudAppsInstance Base class, representing a
Snowflake Cloud Apps instance, and to perform operations on that instance

SnowflakeInstance:

    _get_instance_properties()  --  Instance class method overwritten to add Snowflake-specific
                                    properties (access node)

    restore_in_place()          --  Submits an in-place restore job for the given paths

SnowflakeInstance Attributes:

    access_node         --  Returns the access node client or client group name

    Common properties inherited from CloudAppsInstance:

    ca_instance_type    --  Returns the cloud apps instance type
    credential_name     --  Returns the credential name used for authentication
    credential_id       --  Returns the credential ID used for authentication
    plan_name           --  Returns the plan name associated with this instance
    account_name        --  Returns the account name (client name)
    proxy_client        --  Returns the proxy client name

"""
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class SnowflakeInstance(CloudAppsInstance):
    """
    Represents an instance of the Snowflake Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account, proxy client)
    are inherited from CloudAppsInstance. This class only adds Snowflake-specific
    properties (access node) and the restore_in_place method.
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new SnowflakeInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Snowflake instance.
            instance_name: The name of the Snowflake instance.
            instance_id: Optional; the unique identifier for the instance.
        """
        self._access_node = None

        super(SnowflakeInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve Snowflake-specific instance properties.

        Common properties (instance type, credential name/id, plan, account, proxy client)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        This method only extracts Snowflake-specific fields (access node).
        """
        super(SnowflakeInstance, self)._get_instance_properties()

        self._access_node = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            general_props = cloud_apps_instance.get('generalCloudProperties', {})

            # Access node — can be a client or a client group
            member_servers = general_props.get('accessNodes', {}).get('memberServers', [])
            if member_servers:
                client_info = member_servers[0].get('client', {})
                self._access_node = (
                    client_info.get('clientName') or
                    client_info.get('clientGroupName')
                )

    @property
    def access_node(self) -> Optional[str]:
        """Get the access node client or client group name for this Snowflake instance.

        Returns:
            The access node name as a string, or None if not configured.
        """
        return self._access_node

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified Snowflake database paths.

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
            >>> job = snowflake_instance.restore_in_place(paths=["/MY_DB"], overwrite=True)

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
