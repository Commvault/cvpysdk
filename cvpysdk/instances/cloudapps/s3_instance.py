# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Amazon S3 Instance.

S3Instance is the only class defined in this file.

S3Instance:     Derived class from CloudAppsInstance Base class, representing a
                        Amazon S3 instance, and to perform operations on that instance

S3Instance:

    _get_instance_properties()  --  Instance class method overwritten to add cloud apps
                                        instance properties as well

"""

from __future__ import unicode_literals
from base64 import b64encode
from past.builtins import basestring
from cvpysdk.instances.cainstance import CloudAppsInstance
from cvpysdk.agent import Agent
from cvpysdk.instance import Instance
from cvpysdk.client import Client

class S3Instance(CloudAppsInstance):
    """Class for representing an Instance of the Amazon S3 instance type."""

    def _get_instance_properties(self):
        """Gets the properties of this instance"""
        super(S3Instance, self)._get_instance_properties()

        self._ca_instance_type = None
        self._host_url = None
        self._access_keyID = None
        self._secret_accesskey = None
        self._backup_client = None

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 's3Instance' in cloud_apps_instance:
                s3instance = cloud_apps_instance['s3Instance']

                self._host_url = s3instance['hostURL']
                self._access_keyID = s3instance['accessKeyId']
                self._secret_accesskey = s3instance['secretAccessKey']

            if 'generalCloudProperties' in cloud_apps_instance:
                self._backup_client = cloud_apps_instance[
                    'generalCloudProperties']['proxyServers'][0]['clientName']

    @property
    def ca_instance_type(self):
        """Treats the CloudApps instance type as a read-only attribute."""
        return self._ca_instance_type

    @property
    def host_url(self):
        """Treats the CloudApps host URL property as a read-only attribute."""
        return self._host_url

    @property
    def access_keyID(self):
        """Treats the acess key ID property as a read-only attribute."""
        return self._access_keyID

    @property
    def secret_accesskey(self):
        """Treats the secret access key as a read-only attribute."""
        return self._secret_accesskey

    @property
    def backup_client(self):
        """Treats the proxy client name to this instance as a read-only attribute."""
        return self._backup_client
