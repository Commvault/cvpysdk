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

"""File for operating on a Pinecone Instance.

PineConeInstance is the only class defined in this file.

PineConeInstance: Derived class from CloudAppsInstance Base class, representing a
Pinecone vector database instance, and to perform operations on that instance

PineConeInstance:

    __init__()                      --  Initializes Pinecone instance object with associated
                                        agent_object, instance name and instance id

    _get_instance_properties()      --  Instance class method overwritten to add Pinecone-specific
                                        custom properties (staging path, staging credential)

PineConeInstance Attributes:

    staging_path            --  Returns the instance staging path

    staging_credential      --  Returns the staging credential name

    Common properties inherited from CloudAppsInstance:

    ca_instance_type        --  Returns the cloud apps instance type
    credential_name         --  Returns the credential name used for authentication
    plan_name               --  Returns the plan name associated with this instance
    account_name            --  Returns the account name
    proxy_client            --  Returns the proxy client name

"""
from __future__ import unicode_literals
from typing import Optional

from ..cainstance import CloudAppsInstance


class PineConeInstance(CloudAppsInstance):
    """
    Represents an instance of the Pinecone vector database service.

    Common cloud apps properties (instance type, credentials, plan, account, proxy client)
    are inherited from CloudAppsInstance. This class only adds Pinecone-specific custom
    properties parsed from WorkloadInstanceCustomProperties.
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new PineConeInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Pinecone instance.
            instance_name: The name of the Pinecone instance.
            instance_id: Optional; the unique identifier for the instance.
        """
        self._staging_path = None
        self._staging_credential = None

        super(PineConeInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve Pinecone-specific custom properties.

        Common properties (instance type, credential, plan, account, proxy client)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        This method only extracts Pinecone-specific fields from
        WorkloadInstanceCustomProperties.
        """
        super(PineConeInstance, self)._get_instance_properties()

        self._staging_path = None
        self._staging_credential = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']

            if 'customProperties' in cloud_apps_instance:
                custom_props = cloud_apps_instance.get('customProperties', {})
                name_values = custom_props.get('nameValues', [])

                for prop in name_values:
                    if prop.get('name') == 'WorkloadInstanceCustomProperties':
                        import json
                        try:
                            custom_data = json.loads(prop.get('value', '{}'))
                            self._staging_path = custom_data.get('stagingPath')
                            self._staging_credential = custom_data.get('stagingCredentialName')
                        except (json.JSONDecodeError, ValueError):
                            pass

    @property
    def staging_path(self) -> Optional[str]:
        """Get the staging path for Pinecone data operations.

        Returns:
            The staging path as a string, or None if not configured.
        """
        return self._staging_path

    @property
    def staging_credential(self) -> Optional[str]:
        """Get the staging credential name.

        Returns:
            The staging credential name as a string, or None if not configured.
        """
        return self._staging_credential