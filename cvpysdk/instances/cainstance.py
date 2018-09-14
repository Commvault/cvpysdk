# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Cloud Apps Instance.

CloudAppsInstance is the only class defined in this file.

CloudAppsInstance:  Derived class from Instance Base class, representing a
cloud apps instance, and to perform operations on that instance

**Note:** GoogleInstance class is used for OneDrive as well.

CloudAppsInstance:

    __new__()   --  Method to create object based on specific cloud apps instance type


Usage
=====

To add a new Instance for Cloud Apps agent, please follow these steps:

    1. Add the module for the new instance type under the location:
        **/cvpysdk/instances/cloudapps**,
        with the module name **<new instance type>_instance.py**
        (e.g. "google_instance.py", "salesforce_instance.py")

    #. Create a class for your instance type and inherit the CloudAppsInstance class.

    #. Add the import statement inside the __new__ method.
        **NOTE:** If you add the import statement at the top,
        it'll cause cyclic import, and the call will fail

    #. After adding the import statement:
        - In the **instance_type** dict
            - Add the cloud apps instance type as the key, and the class as its value

"""

from __future__ import unicode_literals

from ..instance import Instance
from ..exception import SDKException


class CloudAppsInstance(Instance):
    """Class for representing an Instance of the Cloud Apps agent."""

    def __new__(cls, agent_object, instance_name, instance_id):
        from .cloudapps.google_instance import GoogleInstance
        from .cloudapps.salesforce_instance import SalesforceInstance
        from .cloudapps.cloud_storage_instance import CloudStorageInstance

        instance_type = {
            1: GoogleInstance,
            2: GoogleInstance,
            3: SalesforceInstance,
            5: CloudStorageInstance,  # AmazonS3 Instance
            6: CloudStorageInstance,  # AzureBlob Instance
            # OneDrive Instance, GoogleInstance class is used for OneDrive instance too.
            7: GoogleInstance,
            14: CloudStorageInstance,  # OracleCloud Instance
            15: CloudStorageInstance,  # Openstack Instance
        }

        commcell_object = agent_object._commcell_object
        instance_service = 'Instance/{0}'.format(instance_id)

        response = commcell_object.request('GET', instance_service)

        if response.json() and "instanceProperties" in response.json():
            properties = response.json()["instanceProperties"][0]
        else:
            raise SDKException('Instance', '105')

        cloud_apps_instance_type = properties['cloudAppsInstance']['instanceType']

        return object.__new__(instance_type[cloud_apps_instance_type])
