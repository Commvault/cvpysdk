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

"""File for operating on a Salesforce Instance.

SalesforceInstance is the only class defined in this file.

SalesforceeInstance:    Derived class from CloudAppsInstance Base class, representing a
                            Salesforce instance, and to perform operations on that instance

SalesforceInstance:

    _get_instance_properties()      --    Instance class method overwritten to add cloud apps
                                            instance properties as well

    ca_instance_type()              --

    organization_id()               --    Fetches salesforce organization id defined in instance

    login_url()                     --    Fetches salesforce login url defined in instance

    consumer_id()                   --    Fetches salesforce consumer if defined in instance

    proxy_client()                  --    Fetches backup client used for the instance

"""

from __future__ import unicode_literals

from ..cainstance import CloudAppsInstance


class SalesforceInstance(CloudAppsInstance):
    """Class for representing an Instance of the Salesforce instance type."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize the object of the SalesforceInstance class.

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class
        """
        self._ca_instance_type = None
        self._proxy_client = None
        self._login_url = None
        self._org_id = None
        self._consumer_secret = None
        self._consumer_id = None

        super(SalesforceInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(SalesforceInstance, self)._get_instance_properties()

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'salesforceInstance' in cloud_apps_instance:
                sfinstance = cloud_apps_instance['salesforceInstance']
                if 'endpoint' in sfinstance:
                    self._login_url = sfinstance['endpoint']
                if 'sfOrgID' in sfinstance:
                    self._org_id = sfinstance['sfOrgID']
                if 'consumerId' in sfinstance:
                    self._consumer_id = sfinstance['consumerId']

            if 'generalCloudProperties' in cloud_apps_instance:
                self._proxy_client = cloud_apps_instance[
                    'generalCloudProperties']['proxyServers'][0]['clientName']

    @property
    def ca_instance_type(self):
        """Treats the CloudApps instance type as a read-only attribute."""
        if self._ca_instance_type == 3:
            return 'SALESFORCE'

        return self._ca_instance_type

    @property
    def organization_id(self):
        """gets the salesforce organization id"""
        return self._org_id

    @property
    def login_url(self):
        """gets the salesforce login url"""
        return self._login_url

    @property
    def consumer_id(self):
        """gets the salesforce consumer id."""
        return self._consumer_id

    @property
    def proxy_client(self):
        """gets the backup client."""
        return self._proxy_client
