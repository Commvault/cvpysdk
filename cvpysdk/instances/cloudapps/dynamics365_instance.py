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

"""
    File for performing operations on a MS Dynamics 365 Instance.

MSDynamics365Instance is the only class defined in this file.

MSDynamics365Instance:
    Class derived from CloudAppsInstance Base class and representing a
        Dynamics 365 CRM instance,

MSDynamics365Instance:

    *****************                       Methods                      *****************

    _get_instance_properties()          --      Instance class method overwritten to fetch cloud apps
                                                    instance properties

    _get_instance_properties_json()     --      Returns the instance properties json

    discover_content()                  --      Discover content for the Dynamics 365 Instance

    *****************                       Properties                      *****************

    access_node                         --      Name of the access node that the instance is associated with

    idx_app_type                        --      Returns the App type of the MS Dynamics 365 instance
"""

from __future__ import unicode_literals
from ...exception import SDKException
from ..cainstance import CloudAppsInstance


class MSDynamics365Instance(CloudAppsInstance):
    """
    Represents an instance of the MSDynamics365 application within a cloud environment.

    This class provides mechanisms for managing and interacting with MSDynamics365 instances,
    including retrieving instance properties, accessing configuration details, and discovering
    content within specific environments. It is designed to be used as part of a cloud application
    management framework, inheriting core functionality from CloudAppsInstance.

    Key Features:
        - Retrieve instance properties in both object and JSON formats
        - Access node and application type information via properties
        - Discover content within specified environments for MSDynamics365
        - Seamless integration with cloud application management workflows

    #ai-gen-doc
    """

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the current MSDynamics365 instance.

        This method fetches the latest properties for the instance and updates the internal state.
        It should be called to ensure the instance properties are current.

        Raises:
            SDKException: If the response is empty or the response status is not successful.

        Example:
            >>> instance = MSDynamics365Instance()
            >>> instance._get_instance_properties()
            >>> # The instance properties are now updated

        #ai-gen-doc
        """
        super(MSDynamics365Instance, self)._get_instance_properties()
        # Common properties for Cloud Apps
        self._ca_instance_type = None
        self._manage_content_automatically = None
        self._auto_discovery_enabled = None
        self._auto_discovery_mode = None

        # Dynamics 365 CRM instance related properties
        self._client_id = None
        self._tenant = None
        self._access_node = None
        self._index_server = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'v2CloudAppsInstance' in cloud_apps_instance:
                d365_instance = cloud_apps_instance['v2CloudAppsInstance']

                self._manage_content_automatically = d365_instance['manageContentAutomatically']
                self._auto_discovery_enabled = d365_instance['isAutoDiscoveryEnabled']

                if 'clientId' in d365_instance:
                    self._client_id = d365_instance.get('clientId')
                    self._tenant = d365_instance.get('tenant')
                else:
                    self._client_id = d365_instance.get(
                        'azureAppList', {}).get('azureApps', [{}])[0].get('azureAppId')
                    self._tenant = d365_instance.get(
                        'azureAppList', {}).get('azureApps', [{}])[0].get('azureDirectoryId')

                if self._client_id is None:
                    raise SDKException('Instance', '102', 'Azure App has not been configured')

            if 'generalCloudProperties' in cloud_apps_instance:
                general_cloud_properties = cloud_apps_instance['generalCloudProperties']
                self._access_node = general_cloud_properties.get("memberServers", {})[0].get("client", {}).get(
                    "clientName", None)
                self._index_server = general_cloud_properties.get("indexServer", {}).get("clientName", None)

    def _get_instance_properties_json(self) -> dict:
        """Retrieve the instance properties as a JSON dictionary.

        Returns:
            dict: A dictionary containing the properties of the MSDynamics365 instance.

        Example:
            >>> instance = MSDynamics365Instance()
            >>> properties = instance._get_instance_properties_json()
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2', ...}

        #ai-gen-doc
        """

        return {'instanceProperties': self._properties}

    @property
    def access_node(self) -> str:
        """Get the name of the access node for this MS Dynamics 365 instance.

        Returns:
            The name of the access node as a string.

        Example:
            >>> instance = MSDynamics365Instance()
            >>> node_name = instance.access_node
            >>> print(f"Access node: {node_name}")

        #ai-gen-doc
        """
        return self._access_node

    @property
    def idx_app_type(self) -> int:
        """Get the application type identifier for the MS Dynamics 365 instance.

        Returns:
            int: The integer value representing the application type of this MS Dynamics 365 instance.

        Example:
            >>> msd_instance = MSDynamics365Instance()
            >>> app_type = msd_instance.idx_app_type
            >>> print(f"MS Dynamics 365 App Type: {app_type}")

        #ai-gen-doc
        """
        return 200127

    def discover_content(self, environment_discovery: bool = False) -> dict:
        """Run discovery for a Microsoft Dynamics 365 Instance.

        This method performs content discovery on the MS Dynamics 365 instance. 
        If `environment_discovery` is set to True, the discovery process will target Dynamics 365 environments.
        If set to False (default), the discovery will be performed at the table level.

        Args:
            environment_discovery: Whether to run discovery for Dynamics 365 environments (True) 
                or at the table level (False).

        Returns:
            dict: A dictionary containing the discovered content.

        Example:
            >>> msd_instance = MSDynamics365Instance()
            >>> content = msd_instance.discover_content()
            >>> print(content)
            >>> # To discover environments instead of tables:
            >>> env_content = msd_instance.discover_content(environment_discovery=True)
            >>> print(env_content)

        #ai-gen-doc
        """
        discovery_type: int
        if environment_discovery is False:
            discovery_type = 8
        else:
            discovery_type = 5

        url = self._services['GET_CLOUDAPPS_USERS'] % (
            self.instance_id, self._agent_object._client_object.client_id, discovery_type)

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', url)

        if flag:
            if response and response.json():
                discover_content = response.json()

                if discover_content.get('error', {}).get('errorCode', 0) == -304283248:
                    raise SDKException('Response', '101', discover_content)

                if 'userAccounts' in response.json():
                    _discover_content = discover_content['userAccounts']
                    return _discover_content

                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)