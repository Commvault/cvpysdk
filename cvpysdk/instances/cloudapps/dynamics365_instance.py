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
    """Class for representing an Instance of the MSDynamics365 instance type."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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

    def _get_instance_properties_json(self):
        """Returns the instance properties json."""

        return {'instanceProperties': self._properties}

    @property
    def access_node(self):
        """Returns the name of the access node for this MS Dynamics 365 instance"""
        return self._access_node

    @property
    def idx_app_type(self) -> int:
        """Returns the App type of the MS Dynamics 365 instance"""
        return 200127

    def discover_content(self, environment_discovery: bool = False):
        """
            Run Discovery for a MS Dynamics 365 Instance
            Arguments:
                environment_discovery            (bool)--     Whether to run discovery for Dynamics 365 environments
                    If True
                        Discovery will run for Dynamics 365 environments
                    If False
                        Table level discovered content would be run
            Returns:
                discovered_content              (dict)--        Dictionary of the discovered content

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
