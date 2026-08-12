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

"""File for operating on a Cloud Database Subclient.

CloudDatabaseSubclient is the only class defined in this file.

CloudDatabaseSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                        Cloud Database subclient(Amazon RDS/Redshift/DocumentDB and DynamoDB), and
                        to perform operations on that subclient

CloudDatabaseSubclient:

    _get_subclient_properties()         --  gets the properties of Cloud Database Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of Cloud Database Subclient

    content()                           --  gets the content of the subclient

    _set_content()                      --  sets the content of the subclient

    browse()                            --  Browse and returns the content of this subclient's instance backups

    restore()                           --  Restores a cloud database from the specified source and restore options

"""
from typing import Any, Dict, Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job

class CloudDatabaseSubclient(CloudAppsSubclient):
    """
    Represents a Cloud Database subclient for managing and operating on cloud database resources.

    This class extends the CloudAppsSubclient base class and provides specialized methods
    for interacting with cloud database subclients. It enables users to retrieve and set
    subclient properties, manage subclient content, browse available data, and perform
    restore operations to specified destinations.

    Key Features:
        - Retrieve subclient properties and their JSON representations
        - Set and manage subclient content
        - Property-based access and modification of subclient content
        - Browse data within the subclient
        - Restore data to a specified destination with customizable options

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> Dict[str, Any]:
        """Retrieve the properties specific to the Cloud Database subclient.

        This method fetches and returns a dictionary containing configuration details
        and settings related to the Cloud Database subclient.

        Returns:
            Dictionary containing subclient properties and their values.

        Example:
            >>> subclient = CloudDatabaseSubclient()
            >>> properties = subclient._get_subclient_properties()
            >>> print(properties)
            >>> # Output: {'property1': 'value1', 'property2': 'value2', ...}

        #ai-gen-doc
        """

        super(CloudDatabaseSubclient, self)._get_subclient_properties()

        if 'cloudDbContent' in self._subclient_properties:
            self._cloud_db_content = self._subclient_properties["cloudDbContent"]
        else:
            self._cloud_db_content = {}

    def _get_subclient_properties_json(self) -> dict:
        """Retrieve the properties JSON for the Cloud Database Subclient.

        Returns:
            dict: A dictionary containing all properties of the Cloud Database Subclient.

        Example:
            >>> subclient = CloudDatabaseSubclient()
            >>> properties = subclient._get_subclient_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary with subclient property details

        #ai-gen-doc
        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "commonProperties": self._commonProperties,
                    "cloudAppsSubClientProp": {
                        "instanceType": self._backupset_object._instance_object.ca_instance_type
                    },
                    "planEntity": {
                        "planName": self.storage_policy
                    },
                    "cloudDbContent": self._cloud_db_content
                }
        }
        return subclient_json

    def _set_content(self, content: Optional[list] = None) -> None:
        """Set the subclient content dictionary for the CloudDatabaseSubclient.

        Args:
            content: Optional list containing the subclient content items. If not provided, the content will be set to an empty or default state.

        Example:
            >>> subclient = CloudDatabaseSubclient()
            >>> subclient._set_content(['database1', 'database2'])
            >>> # The subclient content is now set to the specified databases

        #ai-gen-doc
        """
        if content is not None:
            self._cloud_db_content = {
                "children": content
            }

        self._set_subclient_properties("_cloud_db_content", self._cloud_db_content)

    @property
    def content(self) -> dict:
        """Get the cloud database content associated with this subclient.

        Returns:
            dict: A dictionary containing the content details relevant to the cloud database subclient.

        Example:
            >>> subclient = CloudDatabaseSubclient()
            >>> content_info = subclient.content
            >>> print(content_info)
            {'databaseName': 'mydb', 'instanceType': 'cloud', ...}

        #ai-gen-doc
        """
        return self._cloud_db_content

    @content.setter
    def content(self, subclient_content: list) -> None:
        """Set the content for the Cloud Database Subclient.

        This method constructs and sets the content JSON required to add or update the content
        of a Cloud Database Subclient. The provided content list is validated and used to
        generate the appropriate JSON structure for the API.

        Args:
            subclient_content: A list containing the content items to add to the subclient.

        Raises:
            SDKException: If the subclient_content is not a list or if it is empty.

        Example:
            >>> subclient = CloudDatabaseSubclient()
            >>> new_content = [{"database": "db1"}, {"database": "db2"}]
            >>> subclient.content = new_content  # Use assignment for property setter
            >>> # The subclient content is now updated with the provided databases

        #ai-gen-doc
        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of this cloud database subclient's instance.

        This method allows you to retrieve snapshot information and other details
        by specifying browse options either as positional arguments (typically a dictionary)
        or as keyword arguments.

        Args:
            *args: Optional positional arguments, typically a dictionary of browse options.
                Example:
                    {
                        'start_time': 0,
                        'end_time': 1570808875,
                        'include_aged_data': 0,
                        'copy_precedence': 0,
                    }
            **kwargs: Optional keyword arguments for browse options.
                Example:
                    start_time=0,
                    end_time=1570808875,
                    include_aged_data=0,
                    copy_precedence=0

        Returns:
            dict: The browse response JSON containing a list of snapshot information.

        Example:
            >>> # Using a dictionary as a positional argument
            >>> options = {
            ...     'start_time': 0,
            ...     'end_time': 1570808875,
            ...     'include_aged_data': 0,
            ...     'copy_precedence': 0,
            ... }
            >>> response = subclient.browse(options)
            >>> print(response)
            >>>
            >>> # Using keyword arguments
            >>> response = subclient.browse(
            ...     start_time=0,
            ...     end_time=1570808875,
            ...     include_aged_data=0,
            ...     copy_precedence=0
            ... )
            >>> print(response)

        #ai-gen-doc
        """
        return self._instance_object.browse(*args, **kwargs)

    def restore(
            self,
            destination: str,
            source: str,
            restore_options: dict
        ) -> 'Job':
        """Restore the content of this subclient's instance from a specified snapshot.

        This method initiates a restore operation for the subclient, restoring data from the given source snapshot
        to the specified destination cluster using the provided restore options.

        Args:
            destination: The name of the destination cluster to which the data will be restored.
            source: The name of the source snapshot from which to restore.
            restore_options: A dictionary containing restore options required to submit the restore request.
                Example options include:
                    - allowVersionUpgrade (bool)
                    - publicallyAccessible (bool)
                    - restoreTags (bool)
                    - enableDeletionProtection (bool)
                    - availabilityZone (str)
                    - targetParameterGroup (str)
                    - targetSubnetGroup (str)
                    - nodeType (str)
                    - targetPort (int)
                    - numberOfNodes (int)

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> restore_options = {
            ...     'allowVersionUpgrade': True,
            ...     'publicallyAccessible': True,
            ...     'restoreTags': False,
            ...     'enableDeletionProtection': False,
            ...     'availabilityZone': 'us-east-2a',
            ...     'targetParameterGroup': 'param',
            ...     'targetSubnetGroup': 'subnet',
            ...     'nodeType': 'dc-large-8',
            ...     'targetPort': 2990,
            ...     'numberOfNodes': 1
            ... }
            >>> job = subclient.restore(
            ...     destination='cluster',
            ...     source='snapshot',
            ...     restore_options=restore_options
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        return self._instance_object.restore(destination, source, restore_options)