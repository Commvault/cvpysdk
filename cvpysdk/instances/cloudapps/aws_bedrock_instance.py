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

"""File for operating on an AWS Bedrock Instance.

AwsBedrockInstance is the only class defined in this file.

AwsBedrockInstance: Derived class from CloudAppsInstance Base class, representing an
AWS Bedrock Cloud Apps instance, and to perform operations on that instance.

AwsBedrockInstance:

    _get_instance_properties()  --  Instance class method overwritten to add AWS Bedrock-specific
                                    properties (access node)

    restore_in_place()          --  Submits an in-place restore job for the given paths

AwsBedrockInstance Attributes:

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


class AwsBedrockInstance(CloudAppsInstance):
    """Represents an instance of the AWS Bedrock Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account, proxy client)
    are inherited from CloudAppsInstance. This class adds AWS Bedrock-specific
    properties (access node) and the restore_in_place method.

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new AwsBedrockInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this AWS Bedrock instance.
            instance_name: The name of the AWS Bedrock instance.
            instance_id: Optional; the unique identifier for the instance.

        #ai-gen-doc
        """
        self._access_node = None

        super(AwsBedrockInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve AWS Bedrock-specific instance properties.

        Common properties are parsed by CloudAppsInstance._get_instance_properties().
        This method only extracts AWS Bedrock-specific fields (access node).

        #ai-gen-doc
        """
        super(AwsBedrockInstance, self)._get_instance_properties()

        self._access_node = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            general_props = cloud_apps_instance.get('generalCloudProperties', {})

            member_servers = general_props.get('accessNodes', {}).get('memberServers', [])
            if member_servers:
                client_info = member_servers[0].get('client', {})
                self._access_node = (
                    client_info.get('clientName') or
                    client_info.get('clientGroupName')
                )

    @property
    def access_node(self) -> Optional[str]:
        """Get the access node client or client group name for this AWS Bedrock instance.

        Returns:
            str: Access node name if configured, otherwise None.

        #ai-gen-doc
        """
        return self._access_node

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified AWS Bedrock paths.

        Args:
            paths: List of paths to restore.
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0.
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
