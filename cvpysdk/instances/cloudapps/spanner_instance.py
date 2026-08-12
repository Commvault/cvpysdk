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

"""File for operating on a Google Cloud Spanner Instance.

GoogleSpannerInstance is the only class defined in this file.

GoogleSpannerInstance: Derived class from CloudAppsInstance Base class, representing a
Google Cloud Spanner instance, and to perform operations on that instance

GoogleSpannerInstance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
    instance properties as well

GoogleSpannerInstance Attributes:

    instance_type           --  Returns the GoogleSpannerInstance instance type

    spanner_instance_id     --  Returns the cloud service account client id

    proxy_client            --  Returns the proxy client name to this instance

    staging_path            --  Returns the instance staging path

    project_id              --  Returns the cloud spanner project id

"""
from ...exception import SDKException
from ..cainstance import CloudAppsInstance


class GoogleSpannerInstance(CloudAppsInstance):
    """
    Represents an instance of the Google Cloud Spanner service.

    This class provides an interface for managing and interacting with a Google Cloud Spanner instance.
    It exposes properties to access key attributes such as the instance type, Spanner instance ID,
    proxy client, staging path, and project ID. Internal methods allow retrieval of instance-specific
    properties for further configuration or inspection.

    Key Features:
        - Access to the type of Spanner instance via `instance_type`
        - Retrieve the unique Spanner instance ID with `spanner_instance_id`
        - Obtain the proxy client for communication with the Spanner instance using `proxy_client`
        - Access the staging path for temporary data or operations via `staging_path`
        - Retrieve the associated Google Cloud project ID with `project_id`
        - Internal method for fetching instance properties

    #ai-gen-doc
    """

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the current Google Spanner instance.

        This method fetches the latest properties for the instance and updates the internal state.
        It raises an SDKException if the response from the server is empty or unsuccessful.

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> instance = GoogleSpannerInstance(commcell_object, instance_name)
            >>> instance._get_instance_properties()
            >>> # The instance properties are now updated internally

        #ai-gen-doc
        """
        super(GoogleSpannerInstance, self)._get_instance_properties()
        self._ca_instance_type = None
        self._proxy_client = None

        self._google_instance_id = None
        self._staging_path = None
        self._project_id = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'generalCloudProperties' in cloud_apps_instance:
                if 'proxyServers' in cloud_apps_instance['generalCloudProperties']:
                    self._proxy_client = cloud_apps_instance.get(
                        'generalCloudProperties', {}).get('proxyServers', [{}])[0].get('clientName')
                else:
                    if 'clientName' in cloud_apps_instance.get(
                        'generalCloudProperties', {}).get('memberServers', [{}])[0].get('client'):
                        self._proxy_client = cloud_apps_instance.get('generalCloudProperties', {}).get(
                            'memberServers', [{}])[0].get('client', {}).get('clientName')
                    else:
                        self._proxy_client = cloud_apps_instance.get('generalCloudProperties', {}).get(
                            'memberServers', [{}])[0].get('client', {}).get('clientGroupName')

                if self._proxy_client is None:
                    raise SDKException('Instance', '102', 'Access Node has not been configured')

            if 'cloudSpannerInstance' in cloud_apps_instance:
                self._google_instance_id = cloud_apps_instance.get(
                    'cloudSpannerInstance', {}).get('instanceId')
                self._staging_path = cloud_apps_instance.get(
                    'cloudSpannerInstance', {}).get('cloudStagingPath')
                self._project_id = cloud_apps_instance.get(
                    'cloudSpannerInstance', {}).get('projectId')

    @property
    def instance_type(self) -> int:
        """Get the instance type of the CloudAppsInstance.

        Returns:
            int: The instance type identifier for the CloudAppsInstance.

        Example:
            >>> spanner_instance = GoogleSpannerInstance()
            >>> inst_type = spanner_instance.instance_type
            >>> print(f"Instance type: {inst_type}")

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def spanner_instance_id(self) -> str:
        """Get the Google service account instance ID for this Spanner instance.

        Returns:
            The instance ID as a string.

        Example:
            >>> spanner_instance = GoogleSpannerInstance()
            >>> instance_id = spanner_instance.spanner_instance_id
            >>> print(f"Spanner Instance ID: {instance_id}")

        #ai-gen-doc
        """
        return self._google_instance_id

    @property
    def proxy_client(self) -> str:
        """Get the proxy client name associated with this Google Spanner instance.

        Returns:
            str: The name of the proxy client linked to the cloud account for this instance.

        Example:
            >>> instance = GoogleSpannerInstance()
            >>> proxy_name = instance.proxy_client
            >>> print(f"Proxy client name: {proxy_name}")

        #ai-gen-doc
        """
        return self._proxy_client

    @property
    def staging_path(self) -> str:
        """Get the Cloud Spanner instance staging path.

        Returns:
            The staging path for the Cloud Spanner instance as a string.

        Example:
            >>> instance = GoogleSpannerInstance()
            >>> path = instance.staging_path  # Use dot notation for property access
            >>> print(f"Staging path: {path}")

        #ai-gen-doc
        """
        return self._staging_path

    @property
    def project_id(self) -> str:
        """Get the Google Cloud Spanner project ID associated with this instance.

        Returns:
            The project ID as a string.

        Example:
            >>> instance = GoogleSpannerInstance()
            >>> project_id = instance.project_id  # Use dot notation for property access
            >>> print(f"Cloud Spanner project ID: {project_id}")

        #ai-gen-doc
        """
        return self._project_id
