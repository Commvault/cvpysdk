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

"""File for operating on a Teams Instance.
TeamsInstance is the only class defined in this file.

TeamsInstance: Derived class from CloudAppsInstance Base class, representing Office 365 Teams.

TeamsInstance:
    _get_instance_properties        --  Gets the properties of this machine.
    _get_instance_properties_json   --  Returns the instance properties json.

"""

from __future__ import unicode_literals
from past.builtins import basestring
from ...exception import SDKException
from ..cainstance import CloudAppsInstance


class TeamsInstance(CloudAppsInstance):
    """Class for representing an Instance of Office 365 Teams."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.
            Args:
                None

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty.
                    if response is not success.
                    if access node is not configured.

        """
        super(TeamsInstance, self)._get_instance_properties()

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

    def _get_instance_properties_json(self):
        """Returns the instance properties json.
            Returns:
                dict    --  Dictionary of the instance properties.

        """

        return {'instanceProperties': self._properties}

