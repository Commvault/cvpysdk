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

"""File for operating on a Google Instance.

MSDynamics365Instance is the only class defined in this file.

MSDynamics365Instance: Derived class from CloudAppsInstance Base class, representing a
Dynamics 365 CRM instance,

MSDynamics365Instance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
    instance properties as well

    _get_instance_properties_json()      --  Returns the instance properties json

"""

from __future__ import unicode_literals
from past.builtins import basestring
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
        # Common properties for Google and OneDrive
        self._ca_instance_type = None
        self._manage_content_automatically = None
        self._auto_discovery_enabled = None
        self._auto_discovery_mode = None
        self._proxy_client = None

        # Dynamics 365 CRM instance related properties
        self._client_id = None
        self._tenant = None
        self.__proxy_client = None
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
                self._proxy_client = general_cloud_properties.get("memberServers",{})[0].get("client",{}).get("clientName",{})
                self._index_server = general_cloud_properties.get("indexServer",{}).get("clientName","")

    def _get_instance_properties_json(self):
        """Returns the instance properties json."""

        return {'instanceProperties': self._properties}

    @property
    def proxy_client(self):
        """Returns the proxy client name to this instance"""
        return self._proxy_client