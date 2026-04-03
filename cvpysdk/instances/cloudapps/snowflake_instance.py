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

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
                                    instance properties as well

    restore_in_place()          --  Submits an in-place restore job for the given paths

SnowflakeInstance Attributes:

    instance_type       --  Returns the Snowflake instance type (61)

    credential_name     --  Returns the credential name used for Snowflake authentication

    credential_id       --  Returns the credential ID used for Snowflake authentication

    access_node         --  Returns the access node client or client group name

    plan_name           --  Returns the plan name associated with this instance

    account_name        --  Returns the Snowflake account name (client name)

"""
from typing import List, Optional

from ...exception import SDKException
from ..cainstance import CloudAppsInstance


class SnowflakeInstance(CloudAppsInstance):
    """
    Represents an instance of the Snowflake Cloud Apps service.

    This class provides an interface for managing and interacting with a Snowflake instance.
    It exposes properties to access key attributes such as the instance type, credentials,
    access node, plan, account name, and optional staging path.

    Key Features:
        - Access to the Snowflake instance type via `instance_type`
        - Retrieve authentication credentials with `credential_name` and `credential_id`
        - Obtain the access node (client or client group) using `access_node`
        - Get the associated plan name with `plan_name`
        - Retrieve the Snowflake account name with `account_name`
        - Internal method for fetching and updating instance properties

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new SnowflakeInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Snowflake instance.
            instance_name: The name of the Snowflake instance.
            instance_id: Optional; the unique identifier for the instance.

        Example:
            >>> agent = Agent(commcell_object, 'cloud apps')
            >>> snowflake_instance = SnowflakeInstance(agent, 'MySnowflakeInstance')

        #ai-gen-doc
        """
        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._access_node = None
        self._plan_name = None
        self._account_name = None

        super(SnowflakeInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the current Snowflake instance.

        Parses the cloudAppsInstance block from the instance properties response and
        extracts Snowflake-specific configuration including credentials, access nodes,
        plan details, and account information.

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> instance = SnowflakeInstance(agent_object, 'SnowflakeInstance')
            >>> instance._get_instance_properties()
            >>> print(instance.credential_name)

        #ai-gen-doc
        """
        super(SnowflakeInstance, self)._get_instance_properties()

        self._ca_instance_type = None
        self._credential_name = None
        self._credential_id = None
        self._access_node = None
        self._plan_name = None
        self._account_name = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance.get('instanceType')

            general_props = cloud_apps_instance.get('generalCloudProperties', {})

            # Snowflake credential (credentialId / credentialName)
            if 'credentials' in general_props:
                creds = general_props['credentials']
                self._credential_name = creds.get('credentialName')
                self._credential_id = creds.get('credentialId')

            # Access node — can be a client or a client group
            member_servers = general_props.get('accessNodes', {}).get('memberServers', [])
            if member_servers:
                client_info = member_servers[0].get('client', {})
                self._access_node = (
                    client_info.get('clientName') or
                    client_info.get('clientGroupName')
                )

        # Plan info
        plan = self._properties.get('planEntity', {})
        self._plan_name = plan.get('planName')

        # Account name equals the client name for Snowflake instances
        instance_info = self._properties.get('instance', {})
        self._account_name = instance_info.get('clientName')

    @property
    def instance_type(self) -> Optional[int]:
        """Get the Snowflake instance type identifier.

        Returns:
            The instance type as an integer (61), or None if not set.

        Example:
            >>> print(snowflake_instance.instance_type)
            61

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def credential_name(self) -> Optional[str]:
        """Get the credential name used for Snowflake authentication.

        Returns:
            The credential name as a string, or None if not configured.

        Example:
            >>> print(snowflake_instance.credential_name)
            'my-snowflake-credential'

        #ai-gen-doc
        """
        return self._credential_name

    @property
    def credential_id(self) -> Optional[int]:
        """Get the credential ID used for Snowflake authentication.

        Returns:
            The credential ID as an integer, or None if not configured.

        Example:
            >>> print(snowflake_instance.credential_id)
            24

        #ai-gen-doc
        """
        return self._credential_id

    @property
    def access_node(self) -> Optional[str]:
        """Get the access node client or client group name for this Snowflake instance.

        Returns:
            The access node name as a string (client name or client group name),
            or None if not configured.

        Example:
            >>> print(snowflake_instance.access_node)
            'ritwiz-snowflake-test-server-group'

        #ai-gen-doc
        """
        return self._access_node

    @property
    def plan_name(self) -> Optional[str]:
        """Get the plan name associated with this Snowflake instance.

        Returns:
            The plan name as a string, or None if not configured.

        Example:
            >>> print(snowflake_instance.plan_name)
            'ritwiz-aws-agp-non-dedupe'

        #ai-gen-doc
        """
        return self._plan_name

    @property
    def account_name(self) -> Optional[str]:
        """Get the Snowflake account name (Commvault client name for this instance).

        Returns:
            The account name as a string, or None if not configured.

        Example:
            >>> print(snowflake_instance.account_name)
            'basic-acc1-non-dedeupe-aws'

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
