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
    """Class for representing an Instance of the Google Cloud Spanner instance type."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

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
    def instance_type(self):
        """
            Returns:

                 int:   CloudAppsInstance instance type

        """
        return self._ca_instance_type

    @property
    def spanner_instance_id(self):
        """
            Returns:

                 str:   Google service account instance id

        """
        return self._google_instance_id

    @property
    def proxy_client(self):
        """
            Returns the proxy client name to this instance

                str:    Client name of proxy associated to cloud account

        """
        return self._proxy_client

    @property
    def staging_path(self):
        """
            Returns the instance staging path

                str:    Cloud spanner staging path of instance

        """
        return self._staging_path

    @property
    def project_id(self):
        """
            Returns the cloud project id

                str:    Cloud spanner project id
        """
        return self._project_id
