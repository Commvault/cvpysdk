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
        from .cloudapps.amazon_instance import AmazonRedshiftInstance
        from .cloudapps.amazon_instance import AmazonDocumentDBInstance
        from .cloudapps.amazon_instance import AmazonRDSInstance
        from .cloudapps.amazon_instance import AmazonDynamoDBInstance
        from .cloudapps.dynamics365_instance import MSDynamics365Instance
        from .cloudapps.teams_instance import TeamsInstance
        from .cloudapps.spanner_instance import GoogleSpannerInstance
        instance_type = {
            1: GoogleInstance,
            2: GoogleInstance,
            3: SalesforceInstance,
            4: AmazonRDSInstance,     # Amazon RDS Instance
            5: CloudStorageInstance,  # AmazonS3 Instance
            6: CloudStorageInstance,  # AzureBlob Instance
            # OneDrive Instance, GoogleInstance class is used for OneDrive instance too.
            7: GoogleInstance,
            14: CloudStorageInstance,  # OracleCloud Instance
            15: CloudStorageInstance,  # Openstack Instance
            20: CloudStorageInstance,  # Google Cloud Instance
            21: CloudStorageInstance,  # azure data lake gen2
            26: AmazonRedshiftInstance, # Amazon Redshift
            27: AmazonDocumentDBInstance, # Amazon Document DB
            25: CloudStorageInstance,   #AliBaba
            24: CloudStorageInstance,   #IBM
            22: AmazonDynamoDBInstance, # Amazon DynamoDB
            35: MSDynamics365Instance,   #  MS Dynamics 365 Instance
            36: TeamsInstance, # Office 365 Teams
			37: GoogleSpannerInstance # Google Cloud Spanner Instance
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
