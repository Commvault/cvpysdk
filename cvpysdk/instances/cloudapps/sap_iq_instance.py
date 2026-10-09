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

"""File for operating on a SAP IQ Instance.

SapIqInstance is the only class defined in this file.

SapIqInstance: Derived class from CloudAppsInstance Base class, representing a
SAP IQ Cloud Apps instance (Cloud Apps instance type 107), and to perform
operations on that instance

SapIqInstance:

    _get_instance_properties()  --  Instance class method overwritten to add SAP IQ-specific
                                    properties (access node and workload custom properties)

    restore_in_place()          --  Submits an in-place restore job for the given paths

SapIqInstance Attributes:

    access_node         --  Returns the SAP IQ access node client name

    database_name       --  Returns the protected SAP IQ database name

    engine_name         --  Returns the SAP IQ server engine name

    port                --  Returns the SAP IQ server port

    util_port           --  Returns the SAP IQ utility database port

    iq_dir              --  Returns the SAP IQ installation directory on the access node

    Common properties inherited from CloudAppsInstance:

    ca_instance_type    --  Returns the cloud apps instance type
    credential_name     --  Returns the credential name used for authentication
    credential_id       --  Returns the credential ID used for authentication
    plan_name           --  Returns the plan name associated with this instance
    account_name        --  Returns the account name (client name)
    proxy_client        --  Returns the proxy client name

"""
import json
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class SapIqInstance(CloudAppsInstance):
    """
    Represents an instance of the SAP IQ Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account, proxy client)
    are inherited from CloudAppsInstance. This class adds the SAP IQ access node and the
    fields stored in the ``WorkloadInstanceCustomProperties`` custom property.

    #ai-gen-doc
    """

    CUSTOM_PROPERTIES_NAME = 'WorkloadInstanceCustomProperties'

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new SapIqInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this SAP IQ instance.
            instance_name: The name of the SAP IQ instance.
            instance_id: Optional; the unique identifier for the instance.

        Example:
            >>> instance = agent.instances.get('my_iq_db')

        #ai-gen-doc
        """
        self._access_node = None
        self._database_name = None
        self._engine_name = None
        self._port = None
        self._util_port = None
        self._iq_dir = None

        super(SapIqInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve SAP IQ-specific instance properties.

        Common properties are parsed by CloudAppsInstance._get_instance_properties().
        This method extracts the access node and the SAP IQ custom properties.

        #ai-gen-doc
        """
        super(SapIqInstance, self)._get_instance_properties()

        self._access_node = None
        self._database_name = None
        self._engine_name = None
        self._port = None
        self._util_port = None
        self._iq_dir = None

        general_props = self._properties.get('cloudAppsInstance', {}).get(
            'generalCloudProperties', {}
        )

        member_servers = general_props.get('accessNodes', {}).get('memberServers', [])
        if member_servers:
            client_info = member_servers[0].get('client', {})
            self._access_node = (
                client_info.get('clientName') or client_info.get('clientGroupName')
            )

        for name_value in general_props.get('customProperties', {}).get('nameValues', []):
            if name_value.get('name') != self.CUSTOM_PROPERTIES_NAME:
                continue
            try:
                custom_props = json.loads(name_value.get('value') or '{}')
            except (TypeError, ValueError):
                custom_props = {}
            self._database_name = custom_props.get('databaseName')
            self._engine_name = custom_props.get('engineName')
            self._port = custom_props.get('port')
            self._util_port = custom_props.get('utilPort')
            self._iq_dir = custom_props.get('iqDir')

    @property
    def access_node(self) -> Optional[str]:
        """Get the access node client or client group name for this SAP IQ instance.

        Returns:
            The access node name, or None if not configured.

        Example:
            >>> instance.access_node
            'sykbiq2'

        #ai-gen-doc
        """
        return self._access_node

    @property
    def database_name(self) -> Optional[str]:
        """Get the SAP IQ database protected by this instance.

        Returns:
            The database name, or None if not configured.

        Example:
            >>> instance.database_name
            'test_database_for_mcp'

        #ai-gen-doc
        """
        return self._database_name

    @property
    def engine_name(self) -> Optional[str]:
        """Get the SAP IQ server engine name.

        Returns:
            The engine name, or None if not configured.

        Example:
            >>> instance.engine_name
            'sykbiq2_test'

        #ai-gen-doc
        """
        return self._engine_name

    @property
    def port(self) -> Optional[int]:
        """Get the SAP IQ server port.

        Returns:
            The server port, or None if not configured.

        Example:
            >>> instance.port
            2638

        #ai-gen-doc
        """
        return self._port

    @property
    def util_port(self) -> Optional[int]:
        """Get the SAP IQ utility database port.

        Returns:
            The utility port, or None if not configured.

        Example:
            >>> instance.util_port
            19638

        #ai-gen-doc
        """
        return self._util_port

    @property
    def iq_dir(self) -> Optional[str]:
        """Get the SAP IQ installation directory on the access node.

        Returns:
            The installation directory, or None if not configured.

        Example:
            >>> instance.iq_dir
            '/opt/sap'

        #ai-gen-doc
        """
        return self._iq_dir

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified SAP IQ database paths.

        Args:
            paths: List of database paths to restore, e.g. ["/my_iq_db"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        Example:
            >>> job = sap_iq_instance.restore_in_place(paths=["/my_iq_db"], overwrite=True)

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
