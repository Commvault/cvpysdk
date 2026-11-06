# -*- coding: utf-8 -*-
# ————————————————————————–
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
# ————————————————————————–

"""File for operating on a Power Apps instance.

PowerAppsInstance is the only class defined in this file.

PowerAppsInstance: Derived class from CloudAppsInstance Base class, representing Power Platform Power Apps.

PowerAppsInstance:
    _get_instance_properties()      --  Gets the properties of this machine.
    _get_instance_properties_json() --  Returns the instance properties json.
    update_instance()               --  Update Instance properties.

"""

from __future__ import unicode_literals

from ...exception import SDKException
from ..cainstance import CloudAppsInstance


class PowerAppsInstance(CloudAppsInstance):
    """
    Represents an instance of Power Platform Power Apps within a cloud application environment.

    This class provides management capabilities for Power Apps instances, including property retrieval,
    configuration updates, and access node validation.

    #ai-gen-doc
    """

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of this Power Apps instance.

        This method fetches the current configuration and properties for the PowerAppsInstance
        from the Commcell server. It updates the instance's internal state with the latest
        information. If the response from the server is empty, unsuccessful, or if the access
        node is not configured, an SDKException is raised.

        Raises:
            SDKException: If the response is empty, not successful, or if the access node is not configured.

        Example:
            >>> powerapps_instance = PowerAppsInstance(commcell_object, instance_name)
            >>> powerapps_instance._get_instance_properties()
            >>> # The instance properties are now refreshed and available for use

        #ai-gen-doc
        """
        super(PowerAppsInstance, self)._get_instance_properties()

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
            dict: A dictionary containing the properties of the Power Apps instance.

        Example:
            >>> powerapps_instance = PowerAppsInstance()
            >>> properties = powerapps_instance._get_instance_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary with instance property details

        #ai-gen-doc
        """

        return {'instanceProperties': self._properties}

    def update_instance(self, request_json: dict) -> dict:
        """Update the properties of the Power Apps instance.

        Args:
            request_json: A dictionary containing the instance properties to update.

        Returns:
            dict: The response from the update request, typically containing status and details of the operation.

        Raises:
            SDKException: If the update fails, the response is empty, or the response indicates failure.

        Example:
            >>> update_data = {
            ...     "instanceProperties": {
            ...         "description": "Updated Power Apps instance",
            ...         "isActive": True
            ...     }
            ... }
            >>> response = powerapps_instance.update_instance(update_data)
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
                error_message = response.json().get('errorMessage',"")
                raise SDKException('Subclient', '102', f"Update failed, error message : {error_message}")

            raise SDKException('Response', '102')

        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)
