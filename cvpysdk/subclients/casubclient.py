# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

        instance_types = {
            1: GoogleSubclient,
            2: GoogleSubclient,
            3: SalesforceSubclient,
            7: GoogleSubclient  # OneDrive Subclient. GoogleSuclient class is used for OneDrive too
        }

        cloud_apps_instance_type = backupset_object._instance_object._properties[
            'cloudAppsInstance']['instanceType']

        if cloud_apps_instance_type in instance_types:
            instance_type = instance_types[cloud_apps_instance_type]
        else:
            raise SDKException('Subclient', '112')

        return object.__new__(instance_type)
