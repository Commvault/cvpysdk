# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Google Instance.

GoogleInstance is the only class defined in this file.

GoogleInstance:     Derived class from CloudAppsInstance Base class, representing a
                        Google (GMail/GDrive) instance, and to perform operations on that instance

GoogleInstance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
                                        instance properties as well

"""

from __future__ import unicode_literals

from ..cainstance import CloudAppsInstance


class GoogleInstance(CloudAppsInstance):
    """Class for representing an Instance of the GMail/Gdrive instance type."""

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(GoogleInstance, self)._get_instance_properties()

        self._ca_instance_type = None
        self._manage_content_automatically = None
        self._auto_discovery_enabled = None
        self._app_email_id = None
        self._google_admin_id = None
        self._service_account_key_file = None
        self._app_client_id = None
        self._proxy_client = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 'gInstance' in cloud_apps_instance:
                ginstance = cloud_apps_instance['gInstance']

                self._manage_content_automatically = ginstance['manageContentAutomatically']
                self._auto_discovery_enabled = ginstance['isAutoDiscoveryEnabled']
                self._app_email_id = ginstance['appEmailId']
                self._google_admin_id = ginstance['emailId']
                self._service_account_key_file = ginstance['appKey']
                self._app_client_id = ginstance['appClientId']

            if 'generalCloudProperties' in cloud_apps_instance:
                self._proxy_client = cloud_apps_instance[
                    'generalCloudProperties']['proxyServers'][0]['clientName']

    @property
    def ca_instance_type(self):
        """Treats the CloudApps instance type as a read-only attribute."""
        if self._ca_instance_type == 1:
            return 'GMAIL'
        elif self._ca_instance_type == 2:
            return 'GDRIVE'
        else:
            return self._ca_instance_type

    @property
    def manage_content_automatically(self):
        """Treats the CloudApps Manage Content Automatically property as a read-only attribute."""
        return self._manage_content_automatically

    @property
    def auto_discovery_status(self):
        """Treats the Auto discovery property as a read-only attribute."""
        return self._auto_discovery_enabled

    @property
    def app_email_id(self):
        """Treats the service account mail id as a read-only attribute."""
        return self._app_email_id

    @property
    def google_admin_id(self):
        """Treats the Google admin mail id as a read-only attribute."""
        return self._google_admin_id

    @property
    def key_file_path(self):
        """Treats the service account key file path as a read-only attribute."""
        return self._service_account_key_file

    @property
    def google_client_id(self):
        """Treats the service account client id as a read-only attribute."""
        return self._app_client_id

    @property
    def proxy_client(self):
        """Treats the proxy client name to this instance as a read-only attribute."""
        return self._proxy_client
