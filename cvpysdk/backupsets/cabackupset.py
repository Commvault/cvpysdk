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

"""File for operating on a Cloud Apps Backupset.

CloudAppsBackupset is the only class defined in this file.

CloudAppsBackupset:  Derived class from Backuset Base class, representing a
                        cloud apps backupset, and to perform operations on that backupset

CloudAppsBackupset:

    __new__()   --  Method to create object based on specific cloud apps instance type


Usage
=====

To add a new Backupset for Cloud Apps agent, please follow these steps:

    1. Add the module for the new instance type under the location:
        **/cvpysdk/backupsets/cloudapps**,
        with the module name **<new instance type>_backupset.py**
        (e.g. "salesforce_backupset.py")

    #. Create a class for your instance type and inherit the CloudAppsBackupset class.

    #. Add the import statement inside the __new__ method.
        **NOTE:** If you add the import statement at the top,
        it'll cause cyclic import, and the call will fail

    #. After adding the import statement:
        - In the **instance_type** dict
            - Add the cloud apps instance type as the key, and the class as its value

"""

from __future__ import unicode_literals

from ..backupset import Backupset


class CloudAppsBackupset(Backupset):
    """Class for representing a Backupset of the Cloud Apps agent."""

    def __new__(cls, instance_object, backupset_name, backupset_id=None):

        from .cloudapps.salesforce_backupset import SalesforceBackupset

        instance_types = {
            3: SalesforceBackupset
        }

        cloud_apps_instance_type = instance_object._properties['cloudAppsInstance']['instanceType']

        if cloud_apps_instance_type in instance_types:
            instance_type = instance_types[cloud_apps_instance_type]
        else:
            instance_type = cls

        return object.__new__(instance_type)
