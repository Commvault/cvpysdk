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

"""File for operating on a Cloud Apps Subclient.

CloudAppsSubclient is the only class defined in this file.

CloudAppsSubclient: Derived class from Subclient Base class, representing a
cloud apps subclient, and to perform operations on that subclient.

Note: GoogleSubclient class is used for OneDrive subclient too.

CloudAppsSubclient:

    __new__()   --  Method to create object based on specific cloud apps instance type

"""

from __future__ import unicode_literals

from ..subclient import Subclient
from ..exception import SDKException


class CloudAppsSubclient(Subclient):
    """Class for representing a subclient of the Cloud Apps agent."""

    def __new__(cls, backupset_object, subclient_name, subclient_id=None):
        from .cloudapps.salesforce_subclient import SalesforceSubclient
        from .cloudapps.google_subclient import GoogleSubclient
        from .cloudapps.cloud_storage_subclient import CloudStorageSubclient

        instance_types = {
            1: GoogleSubclient,
            2: GoogleSubclient,
            3: SalesforceSubclient,
            5: CloudStorageSubclient,  # AmazonS3 Subclient
            6: CloudStorageSubclient,  # AzureBlob Subclient
            7: GoogleSubclient,  # OneDrive Subclient. GoogleSuclient class is used for OneDrive too
            14: CloudStorageSubclient,  # OracleCloud Subclient
            15: CloudStorageSubclient,  # Openstack Subclient
        }

        cloud_apps_instance_type = backupset_object._instance_object._properties[
            'cloudAppsInstance']['instanceType']

        if cloud_apps_instance_type in instance_types:
            instance_type = instance_types[cloud_apps_instance_type]
        else:
            raise SDKException('Subclient', '112')

        return object.__new__(instance_type)
