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

""" File for operating on a cloud database instance.

CloudDatabaseInstance is the only class defined in this file.

CloudDatabaseInstance:   Derived class from CloudAppsInstance Base class, representing a
                        Cloud Database instance( Amazon RDS,Redshift,DocumentDB and DynamoDB), and to
                        perform operations on that instance

CloudDatabaseInstance:

    __init__()                      --  Initializes cloud database instance object with associated
    agent_object, instance name and instance id

    _get_instance_properties()      --  Retrieves cloud database related instance properties

    _browse_request_json()          --  Retrieves and sets browse request json based on browse options

    _process_browse_response()      --  Process the response received from browse request

    browse()                        --  Browse and returns the contents of this instance backup

    restore()                       -- Submits a restore request based on restore options

"""

from __future__ import unicode_literals
import time
from typing import Any, Dict

from ..cainstance import CloudAppsInstance
from ...exception import SDKException
from ...job import Job

class CloudDatabaseInstance(CloudAppsInstance):
    """
    Represents an instance of a cloud database service, such as Amazon RDS, Redshift, DocumentDB, DynamoDB, or Cloud Spanner.

    This class provides an interface for managing and interacting with cloud database instances within a cloud application environment.
    It supports operations such as browsing database contents, restoring data, and retrieving instance properties. The class is designed
    to be used as part of a larger cloud management framework, enabling seamless integration and automation of database management tasks.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Retrieval of instance properties
        - Access to and modification of browse request JSON payloads
        - Processing of browse responses
        - Browsing of database contents
        - Restoration of data to specified destinations with customizable options
        - Property for accessing the cloud application instance type

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new CloudDatabaseInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this cloud database instance.
            instance_name: The name of the cloud database instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, it will be determined automatically.

        Example:
            >>> agent = Agent(commcell_object, 'CloudDBAgent')
            >>> cloud_db_instance = CloudDatabaseInstance(agent, 'MyCloudDBInstance')
            >>> # Optionally, provide an instance ID
            >>> cloud_db_instance_with_id = CloudDatabaseInstance(agent, 'MyCloudDBInstance', '12345')

        #ai-gen-doc
        """

        self._ca_instance_type = None
        self._browse_request = {}
        self._browse_url = None

        super(
            CloudDatabaseInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

    def _get_instance_properties(self) -> dict:
        """Retrieve the properties of the current cloud database instance.

        Returns:
            dict: A dictionary containing the properties and configuration details of this cloud database instance.

        Example:
            >>> instance = CloudDatabaseInstance()
            >>> properties = instance._get_instance_properties()
            >>> print(properties)
            {'instanceName': 'CloudDB01', 'status': 'Active', ...}
        #ai-gen-doc
        """
        super(CloudDatabaseInstance, self)._get_instance_properties()
        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

    @property
    def ca_instance_type(self) -> str:
        """Get the CloudApps instance type for this cloud database instance.

        This property provides the type of the CloudApps instance as a read-only string attribute.

        Returns:
            The CloudApps instance type as a string.

        Example:
            >>> cloud_db_instance = CloudDatabaseInstance()
            >>> instance_type = cloud_db_instance.ca_instance_type
            >>> print(f"CloudApps instance type: {instance_type}")

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def _browse_request_json(self) -> dict:
        """Get the browse request JSON for the CloudApps instance.

        Returns:
            dict: The JSON structure required to perform a browse operation on the CloudApps instance.

        Example:
            >>> instance = CloudDatabaseInstance()
            >>> browse_json = instance._browse_request_json
            >>> print(browse_json)
            >>> # Use the returned JSON to initiate a browse request

        #ai-gen-doc
        """
        return self._browse_request

    @_browse_request_json.setter
    def _browse_request_json(self, value: Dict[str, Any]) -> None:
        """Set the CloudApps instance browse request JSON options.

        This setter method configures the browse request JSON for the CloudDatabaseInstance
        based on the provided options dictionary.

        Args:
            value: A dictionary containing browse options for the CloudApps instance.
                Example:
                    {
                        'start_time': 0,
                        'end_time': 1570808875,
                        'include_aged_data': 0,
                        'copy_precedence': 0,
                    }

        Example:
            >>> options = {
            ...     'start_time': 0,
            ...     'end_time': 1570808875,
            ...     'include_aged_data': 0,
            ...     'copy_precedence': 0,
            ... }
            >>> instance = CloudDatabaseInstance()
            >>> instance._browse_request_json = options  # Use assignment for property setter

        #ai-gen-doc
        """
        start_time = value.get('start_time', 0)
        end_time = value.get('end_time', int(time.time()))
        include_aged_data = value.get('include_aged_data', 0)
        copy_precedence = value.get('copy_precedence', 0)
        self._browse_request = {
            "entity": {
                "instanceId": int(self.instance_id)
            },
            "copyPresedence": copy_precedence,
            "includeAgedData": include_aged_data,
            "startTime": start_time,
            "endTime": end_time
        }

    def _process_browse_response(self, flag: bool, response: dict) -> dict:
        """Process the response from a browse request.

        This method evaluates the result of a browse operation, typically performed via a REST API call.
        If the request was successful (flag is True), it returns the JSON response dictionary.
        If the request failed, an exception is raised.

        Args:
            flag: Indicates whether the REST API request was successful (True) or not (False).
            response: The response dictionary returned if the request was successful.

        Returns:
            dict: The JSON response received from the browse request.

        Raises:
            Exception: If the browse request failed (flag is False).

        Example:
            >>> instance = CloudDatabaseInstance()
            >>> try:
            ...     result = instance._process_browse_response(True, {"data": "sample"})
            ...     print(result)
            ... except Exception as e:
            ...     print(f"Browse failed: {e}")

        #ai-gen-doc
        """
        if flag:
            return response.json()

        o_str = 'Failed to browse content of this instance backups.\nError: "{0}"'
        raise SDKException('Subclient', '102', o_str.format(response))

    def browse(self, *args: Any, **kwargs: Any) -> dict:
        """Browse the content of the cloud database instance.

        This method allows you to browse the contents of a cloud database instance by specifying
        browse options either as positional arguments (typically a dictionary) or as keyword arguments.

        Args:
            *args: Optional positional arguments, typically a dictionary containing browse options such as:
                - 'start_time': The start time for the browse operation (epoch timestamp).
                - 'end_time': The end time for the browse operation (epoch timestamp).
                - 'include_aged_data': Whether to include aged data (0 or 1).
                - 'copy_precedence': The copy precedence value.
            **kwargs: Optional keyword arguments for browse options. Keys correspond to browse parameters.

        Returns:
            dict: The JSON response from the browse operation, containing the results of the browse.

        Example:
            >>> # Using a dictionary as a positional argument
            >>> options = {
            ...     'start_time': 0,
            ...     'end_time': 1570808875,
            ...     'include_aged_data': 0,
            ...     'copy_precedence': 0,
            ... }
            >>> response = cloud_db_instance.browse(options)
            >>> print(response)

            >>> # Using keyword arguments
            >>> response = cloud_db_instance.browse(
            ...     start_time=0,
            ...     end_time=1570808875,
            ...     include_aged_data=0,
            ...     copy_precedence=0
            ... )
            >>> print(response)

        #ai-gen-doc
        """

        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        self._browse_request_json = options
        flag, response = self._cvpysdk_object.make_request('POST', self._browse_url, self._browse_request)
        return self._process_browse_response(flag, response)

    def restore(self, destination: str, source: str, options: dict) -> 'Job':
        """Restore the content of this cloud database instance from a specified snapshot.

        Args:
            destination: The name of the destination cluster to restore to.
            source: The name of the source snapshot to restore from.
            options: A dictionary of restore options required to submit the restore request.
                Example options for restoring an Amazon Redshift instance cluster from a snapshot:
                    {
                        'allowVersionUpgrade': True,
                        'publicallyAccessible': True,
                        'restoreTags': False,
                        'enableDeletionProtection': False,
                        'availabilityZone': 'us-east-2a',
                        'targetParameterGroup': 'param',
                        'targetSubnetGroup': 'subnet',
                        'nodeType': 'dc-large-8',
                        'targetPort': 2990,
                        'numberOfNodes': 1
                    }

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
            >>> job = cloud_db_instance.restore(
            ...     destination='target_cluster',
            ...     source='snapshot_2023_01_01',
            ...     options=restore_options
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        if not (isinstance(source, str) or
                isinstance(destination, str) or
                isinstance(options, dict)):
            raise SDKException('Instance', '101')
        request_json = self._restore_json(destination=destination, source=source, options=options)
        return self._process_restore_response(request_json)