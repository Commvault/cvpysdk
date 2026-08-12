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

"""File for operating on a PowerBI Instance.
PowerBIInstance is the only class defined in this file.

PowerBIInstance: Derived class from CloudAppsInstance Base class, representing Power Platform Power Bi.

PowerBIInstance:
    _get_instance_properties()      --  Gets the properties of this machine.
    _get_instance_properties_json() --  Returns the instance properties json.
    update_instance()               --  Update Instance properties.

"""

from __future__ import unicode_literals
import time

from ...exception import SDKException
from ..cainstance import CloudAppsInstance
from ...job import Job

class PowerBIInstance(CloudAppsInstance):
    """
    Represents an instance of Power Platform Power Bi within a cloud application environment.

    This class provides comprehensive management and operational capabilities for Power Platform Power Bi instances,
    including property retrieval, discovery, restoration, and instance updates. It is designed to facilitate
    backup, recovery, and configuration tasks for Power Bi environments in cloud-based infrastructures.

    Key Features:
        - Retrieve instance properties and their JSON representations
        - Update Power Bi instance configuration using JSON requests

    #ai-gen-doc
    """

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Power Bi Instance.

        This method fetches the current configuration and properties for the PowerBiInstance
        from the Commcell server. It updates the instance's internal state with the latest
        information. If the response from the server is empty, unsuccessful, or if the access
        node is not configured, an SDKException is raised.

        Raises:
            SDKException: If the response is empty, not successful, or if the access node is not configured.

        Example:
            >>> powerbi_instance = PowerBIInstance(commcell_object, instance_name)
            >>> powerbi_instance._get_instance_properties()
            >>> # The instance properties are now refreshed and available for use

        #ai-gen-doc
        """
        super(PowerBIInstance, self)._get_instance_properties()

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

    def _get_instance_properties_json(self) -> dict:
        """Retrieve the instance properties as a JSON dictionary.

        Returns:
            dict: A dictionary containing the properties of the PowerBi instance.

        Example:
            >>> powerbi_instance = PowerBIInstance()
            >>> properties = powerbi_instance._get_instance_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary with instance property details

        #ai-gen-doc
        """

        return {'instanceProperties': self._properties}

    def update_instance(self, request_json: dict) -> dict:
        """Update the properties of the Power Bi instance.

        Args:
            request_json: A dictionary containing the instance properties to update.

        Returns:
            dict: The response from the update request, typically containing status and details of the operation.

        Raises:
            SDKException: If the update fails, the response is empty, or the response indicates failure.

        Example:
            >>> update_data = {
            ...     "instanceProperties": {
            ...         "description": "Updated PowerBi instance",
            ...         "isActive": True
            ...     }
            ... }
            >>> response = powerbi_instance.update_instance(update_data)
            >>> print(response)
            {'status': 'success', 'details': {...}}

        #ai-gen-doc
        """

        url = self._services['INSTANCE_PROPERTIES'] % (self.instance_id)
        flag, response = self._cvpysdk_object.make_request('POST', url, request_json)
        if response.json():

            if 'processinginstructioninfo' in response.json():
                return response.json()

            elif "errorCode" in response.json():
                error_message = response.json()['errorMessage']
                raise SDKException('Subclient', '102', f"Update failed, error message : {error_message}")

            raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)