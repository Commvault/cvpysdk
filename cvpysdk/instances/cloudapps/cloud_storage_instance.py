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

""" File for operating on a cloud storage instance.

CloudStorageInstance is the only class defined in this file.

CloudStorageInstance:   Derived class from CloudAppsInstance Base class, representing a
                        Cloud Storage instance(S3,Azure,Oraclecloud and Openstack), and to
                        perform operations on that instance

CloudStorageInstance:

    _get_instance_properties()              --  Instance class method overwritten to add cloud apps
    instance properties as well

    _generate_json()                        --  Returns the JSON request to pass to the API as per
    the options selected by the user

    restore_in_place()                      --  restores the files/folders specified in the
    input paths list to the same location.

    restore_out_of_place()                  --  restores the files/folders specified in the input
                                                paths list to the input client,
                                                at the specified destination location.

    restore_to_fs()                         --  restores the files/folders specified in the input
                                                paths list to the input fs client,
                                                at the specified destination location.

    _set_destination_options_json()         --  setter for cloud apps destination options in
    restore JSON

    _set_restore_options_json()             --  setter for cloudapps restore options in restore JSON

    _set_proxy_credential_json()            --  Method to construct the proxy credentials
                                                json for out of place restore

    restore_using_proxy()                   --  To perform restore to different cloud using
                                                proxy passing explicit credentials of destination cloud

"""
from cvpysdk.instances.cainstance import CloudAppsInstance
from cvpysdk.client import Client
from cvpysdk.exception import SDKException
from cvpysdk.job import Job

class CloudStorageInstance(CloudAppsInstance):
    """
    Represents an instance of a cloud storage application within the cloud apps framework.

    This class encapsulates the configuration, properties, and operations for managing
    a cloud storage instance. It provides access to various instance properties such as
    host URLs, access keys, account and client information, and supports multiple restore
    operations including in-place, out-of-place, file system restores, and restores using
    proxy credentials.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Retrieval of instance properties and configuration details
        - Access to cloud storage-specific properties (e.g., host URLs, access keys, account names)
        - Generation of instance configuration in JSON format
        - Multiple restore operations:
            - In-place restore
            - Out-of-place restore
            - Restore to file system
            - Restore using proxy credentials
        - Setting of destination, restore, common, and proxy credential options in JSON
        - Property accessors for various cloud storage attributes

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new CloudStorageInstance object.

        Args:
            agent_object: An instance of the Agent class associated with this cloud storage instance.
            instance_name: The name of the cloud storage instance.
            instance_id: The unique identifier for the instance. If not provided, it defaults to None.

        Example:
            >>> agent = Agent(commcell_object, "CloudApps")
            >>> cloud_instance = CloudStorageInstance(agent, "MyCloudInstance", "12345")
            >>> # The cloud_instance object is now initialized and ready for use

        #ai-gen-doc
        """
        # Common Properties
        self._ca_instance_type = None
        self._access_node = None

        # Google Cloud Properties
        self._google_host_url = None
        self._google_access_key = None
        self._google_secret_key = None

        self._host_url = None
        self._access_keyid = None
        self._secret_accesskey = None
        self._account_name = None
        self._access_key = None
        self._server_name = None
        self._username = None
        self._endpointurl = None

        self._set_cloud_destination_options_json = None
        self._set_cloud_restore_options_json = None

        super(
            CloudStorageInstance,
            self).__init__(
            agent_object,
            instance_name,
            instance_id)

    def _get_instance_properties(self) -> dict:
        """Retrieve the properties of the current cloud storage instance.

        Returns:
            dict: A dictionary containing the properties and configuration details of this cloud storage instance.

        Example:
            >>> instance = CloudStorageInstance()
            >>> properties = instance._get_instance_properties()
            >>> print(properties)
            >>> # Output will be a dictionary with instance configuration details

        #ai-gen-doc
        """
        super(CloudStorageInstance, self)._get_instance_properties()

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties.get('cloudAppsInstance', {})
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 's3Instance' in cloud_apps_instance:
                s3instance = cloud_apps_instance.get('s3Instance', {})

                self._host_url = s3instance.get('hostURL', '')
                self._access_keyid = s3instance.get('accessKeyId', '')

            if 'azureInstance' in cloud_apps_instance:
                azureinstance = cloud_apps_instance.get('azureInstance', {})

                self._host_url = azureinstance.get('hostURL', '')
                self._account_name = azureinstance.get('accountName', '')
                self._access_key = azureinstance.get('accessKey', '')

            if 'openStackInstance' in cloud_apps_instance:
                openstackinstance = cloud_apps_instance.get('openStackInstance', {})

                self._server_name = openstackinstance.get('serverName', '')
                self._username = openstackinstance.get('credentials', {}).get('userName', '')

            if 'oraCloudInstance' in cloud_apps_instance:
                oraclecloudinstance = cloud_apps_instance.get('oraCloudInstance')

                self._endpointurl = oraclecloudinstance.get('endpointURL', '')
                self._username = oraclecloudinstance.get('user', {}).get('userName', '')

            # Google Cloud Instance porperties
            if 'googleCloudInstance' in cloud_apps_instance:
                googlecloudinstance = cloud_apps_instance.get('googleCloudInstance', {})

                self._google_host_url = googlecloudinstance.get('serverName', '')
                self._google_access_key = googlecloudinstance.get('credentials', {}).get('userName', '')

            # Ali Cloud
            if 'alibabaInstance' in cloud_apps_instance:
                alibabainstance = cloud_apps_instance.get('alibabaInstance', {})

                self._host_url = alibabainstance.get('hostURL', '')
                self._access_key = alibabainstance.get('accessKey', '')

            # IBM Cloud
            if 'ibmCosInstance' in cloud_apps_instance:
                ibminstance = cloud_apps_instance.get('ibmCosInstance', {})

                self._host_url = ibminstance.get('hostURL', '')
                self._access_key = ibminstance.get('credentials', {}).get('username', '')

            # S3 Compatible
            if 's3CompatibleInstance' in cloud_apps_instance:
                s3compat_instance = cloud_apps_instance.get('s3CompatibleInstance', {})

                self._host_url = s3compat_instance.get('hostURL', '')

            if 'generalCloudProperties' in cloud_apps_instance:
                self._access_node = cloud_apps_instance.get(
                    'generalCloudProperties', {}).get(
                    'proxyServers', [{}])[0].get('clientName', cloud_apps_instance.get(
                        'generalCloudProperties', {}).get('memberServers', [{}])[
                        0].get('client', {}).get('clientName'))

    @property
    def google_host_url(self) -> str:
        """Get the Google Cloud host URL associated with this CloudStorageInstance.

        This property provides the host URL for the configured Google Cloud storage,
        allowing read-only access to the endpoint information.

        Returns:
            str: The host URL of the Google Cloud storage.

        Example:
            >>> instance = CloudStorageInstance()
            >>> url = instance.google_host_url
            >>> print(f"Google Cloud host URL: {url}")

        #ai-gen-doc
        """
        return self._google_host_url

    @property
    def google_access_key(self) -> str:
        """Get the Google Cloud account access key associated with this cloud storage instance.

        This property provides read-only access to the access key used for authenticating with Google Cloud Storage.

        Returns:
            The Google Cloud account access key as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> access_key = instance.google_access_key  # Use dot notation for property access
            >>> print(f"Google Cloud Access Key: {access_key}")

        #ai-gen-doc
        """
        return self._google_access_key

    @property
    def ca_instance_type(self) -> str:
        """Get the CloudApps instance type as a read-only attribute.

        Returns:
            The type of the CloudApps instance as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> instance_type = instance.ca_instance_type  # Use dot notation for property access
            >>> print(f"CloudApps instance type: {instance_type}")

        #ai-gen-doc
        """
        return self._ca_instance_type

    @property
    def host_url(self) -> str:
        """Get the host URL associated with this CloudStorageInstance.

        This property provides the host URL as a read-only string attribute.

        Returns:
            The host URL as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> url = instance.host_url  # Access the host URL property
            >>> print(f"Cloud storage host URL: {url}")

        #ai-gen-doc
        """
        return self._host_url

    @property
    def access_key(self) -> str:
        """Get the access key associated with this CloudStorageInstance.

        This property provides read-only access to the access key used for authentication
        with the cloud storage provider.

        Returns:
            The access key as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> key = instance.access_key  # Use dot notation to access the property
            >>> print(f"Access Key: {key}")

        #ai-gen-doc
        """
        return self._access_key

    @property
    def account_name(self) -> str:
        """Get the account name associated with this CloudStorageInstance.

        This property provides the account name as a read-only attribute.

        Returns:
            The account name as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> name = instance.account_name  # Access the account name property
            >>> print(f"Account Name: {name}")

        #ai-gen-doc
        """
        return self._account_name

    @property
    def access_keyid(self) -> str:
        """Get the access key ID associated with this cloud storage instance.

        This property provides read-only access to the access key ID used for authentication
        with the cloud storage provider.

        Returns:
            The access key ID as a string.

        Example:
            >>> cloud_instance = CloudStorageInstance()
            >>> key_id = cloud_instance.access_keyid  # Use dot notation to access the property
            >>> print(f"Access Key ID: {key_id}")

        #ai-gen-doc
        """
        return self._access_keyid

    @property
    def server_name(self) -> str:
        """Get the server name associated with this CloudStorageInstance.

        Returns:
            The server name as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> name = instance.server_name  # Access the server name property
            >>> print(f"Server name: {name}")

        #ai-gen-doc
        """
        return self._server_name

    @property
    def username(self) -> str:
        """Get the username associated with this CloudStorageInstance.

        Returns:
            The username as a string. This property is read-only.

        Example:
            >>> instance = CloudStorageInstance()
            >>> user = instance.username  # Access the username property
            >>> print(f"Cloud storage username: {user}")

        #ai-gen-doc
        """
        return self._username

    @property
    def endpointurl(self) -> str:
        """Get the endpoint URL associated with this CloudStorageInstance.

        Returns:
            The endpoint URL as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> url = instance.endpointurl  # Access the endpoint URL property
            >>> print(f"Endpoint URL: {url}")

        #ai-gen-doc
        """
        return self._endpointurl

    @property
    def client_name(self) -> str:
        """Get the client name associated with this CloudStorageInstance.

        Returns:
            The client name as registered in the Commcell.

        Example:
            >>> instance = CloudStorageInstance(commcell_object, 'Cloud_Instance')
            >>> name = instance.client_name
            >>> print(f"Client name: {name}")

        #ai-gen-doc
        """
        return self._properties.get('instance', {}).get('clientName')

    @property
    def access_node(self) -> str:
        """Get the access node associated with this CloudStorageInstance.

        Returns:
            The name of the access node as a string.

        Example:
            >>> instance = CloudStorageInstance()
            >>> node = instance.access_node  # Use dot notation to access the property
            >>> print(f"Access node: {node}")

        #ai-gen-doc
        """
        return self._access_node

    def _generate_json(self, **kwargs: dict) -> dict:
        """Generate a JSON request for the API based on user-selected options.

        This method constructs a JSON dictionary to be sent to the API, using the options
        provided as keyword arguments. The options typically correspond to restore settings
        or other configuration parameters required by the API.

        Args:
            **kwargs: Arbitrary keyword arguments representing options to be set for the restore operation.

        Returns:
            dict: A JSON-compatible dictionary to be passed to the API.

        Example:
            >>> instance = CloudStorageInstance()
            >>> json_request = instance._generate_json(restore_type='full', overwrite=True, target_path='/data/restore')
            >>> print(json_request)
            {'restore_type': 'full', 'overwrite': True, 'target_path': '/data/restore'}

        #ai-gen-doc
        """
        cloud_restore_json = super(
            CloudStorageInstance,
            self)._restore_json(
            **kwargs)
        restore_options = {}
        if kwargs.get("restore_options"):

            restore_options = kwargs["restore_options"]
            for key in kwargs:

                if not key == "restore_options":
                    restore_options[key] = kwargs[key]

        else:
            restore_options.update(kwargs)

        self._set_destination_options_json(restore_options)
        self._set_restore_options_json(restore_options)
        self._set_common_options_json(restore_options)

        cloud_restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "destination"] = self._set_cloud_destination_options_json
        cloud_restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "cloudAppsRestoreOptions"] = self._set_cloud_restore_options_json
        cloud_restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["commonOptions"] = self._common_options_json
        
        return cloud_restore_json

    def restore_in_place(
            self,
            paths: list,
            overwrite: bool = True,
            copy_precedence: int = None,
            no_of_streams: int = 2
        ) -> 'Job':
        """Restore files or folders to their original location in the cloud storage instance.

        This method restores the specified files or folders, provided as a list of full paths, 
        to their original location within the cloud storage instance. You can control whether 
        existing files are overwritten, specify a storage policy copy precedence, and set the 
        number of streams to use for the restore operation.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files will be unconditionally overwritten during restore. Default is True.
            copy_precedence: Optional; the copy precedence value of the storage policy copy to use. Default is None.
            no_of_streams: Number of streams to use for the restore operation. Default is 2.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If `paths` is not a list, if the job fails to initialize, 
                if the response is empty, or if the response indicates failure.

        Example:
            >>> cloud_instance = CloudStorageInstance(commcell)
            >>> restore_job = cloud_instance.restore_in_place(
            ...     paths=['/data/file1.txt', '/data/folder1/'],
            ...     overwrite=True,
            ...     copy_precedence=1,
            ...     no_of_streams=4
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """

        if not (isinstance(paths, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        request_json = self._generate_json(
            paths=paths,
            destination_client=self.client_name,
            destination_instance_name=self.instance_name,
            overwrite=overwrite,
            in_place=True,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=False,
            no_of_streams=no_of_streams)

        return self._process_restore_response(request_json)

    def restore_out_of_place(
            self,
            paths: list,
            destination_client: str,
            destination_instance_name: str,
            destination_path: str,
            overwrite: bool = True,
            copy_precedence: int = None,
            no_of_streams: int = 2,
            **kwargs
        ) -> 'Job':
        """Restore specified files or folders to a different client and location.

        This method restores the files or folders listed in `paths` to the specified
        destination client, instance, and path. It supports options for overwriting
        existing files, specifying storage policy copy precedence, and controlling
        the number of restore streams. Additional restore options can be provided
        via keyword arguments.

        Args:
            paths: List of full file or folder paths to restore.
            destination_client: Name of the client to restore data to.
            destination_instance_name: Name of the destination instance for the restore.
            destination_path: Target path on the destination instance where data will be restored.
            overwrite: If True, existing files at the destination will be overwritten. Defaults to True.
            copy_precedence: Storage policy copy precedence value. Defaults to None.
            no_of_streams: Number of parallel streams to use for the restore. Defaults to 2.
            **kwargs: Additional keyword arguments for advanced restore options:
                - from_time (str): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS').
                - to_time (str): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS').
                - no_image (bool): If True, restore deleted items. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If any of the following conditions occur:
                - `paths` is not a list.
                - `destination_client` is not a string or Client object.
                - `destination_path` is not a string.
                - Failed to initialize the restore job.
                - The response is empty or not successful.

        Example:
            >>> instance = CloudStorageInstance()
            >>> restore_job = instance.restore_out_of_place(
            ...     paths=['/data/file1.txt', '/data/file2.txt'],
            ...     destination_client='client02',
            ...     destination_instance_name='cloudInstance2',
            ...     destination_path='/restore/location',
            ...     overwrite=True,
            ...     copy_precedence=1,
            ...     no_of_streams=4,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     no_image=False
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """

        if not ((isinstance(destination_client, str) or
                 isinstance(destination_client, Client)) and
                isinstance(destination_instance_name, str) and
                isinstance(destination_path, str) and
                isinstance(paths, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        request_json = self._generate_json(
            paths=paths,
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            destination_path=destination_path,
            overwrite=overwrite,
            in_place=False,
            copy_precedence=copy_precedence,
            no_of_streams=no_of_streams,
            restore_To_FileSystem=False,
            **kwargs)

        return self._process_restore_response(request_json)

    def restore_to_fs(
            self,
            paths: list,
            destination_path: str,
            destination_client: str = None,
            overwrite: bool = True,
            copy_precedence: int = None,
            no_of_streams: int = 2
        ) -> 'Job':
        """Restore specified files or folders to a file system client at a given destination path.

        This method initiates a restore job for the provided list of file or folder paths, restoring them
        to the specified destination path on the target client. You can control overwrite behavior,
        copy precedence, and the number of streams used for the restore.

        Args:
            paths: List of full file or folder paths to restore.
            destination_path: Destination directory path on the target client where files/folders will be restored.
            destination_client: Name of the file system client to restore to. If None, restores to the backup or proxy client.
            overwrite: If True, existing files at the destination will be overwritten. Defaults to True.
            copy_precedence: Optional storage policy copy precedence value. If None, default precedence is used.
            no_of_streams: Number of data streams to use for the restore. Defaults to 2.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If any of the following conditions occur:
                - The client is not a string or client object.
                - The destination_path is not a string.
                - The paths argument is not a list.
                - Failed to initialize the restore job.
                - The response from the server is empty or indicates failure.

        Example:
            >>> instance = CloudStorageInstance()
            >>> restore_job = instance.restore_to_fs(
            ...     paths=['/data/file1.txt', '/data/file2.txt'],
            ...     destination_path='/restore/target/',
            ...     destination_client='client01',
            ...     overwrite=True,
            ...     copy_precedence=1,
            ...     no_of_streams=4
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """

        if not ((isinstance(destination_client, str) or
                 isinstance(destination_client, Client)) and
                isinstance(destination_path, str) and
                isinstance(paths, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        destination_appTypeId = int(
            self._commcell_object.clients.get(destination_client).agents.get('file system').agent_id)

        request_json = self._generate_json(
            paths=paths,
            destination_path=destination_path,
            destination_client=destination_client,
            overwrite=overwrite,
            in_place=False,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=True,
            no_of_streams=no_of_streams,
            destination_appTypeId=destination_appTypeId)

        return self._process_restore_response(request_json)

    def _set_destination_options_json(self, value: dict) -> None:
        """Set the cloud apps destination options in the restore JSON.

        This method updates the restore JSON with the specified destination options for cloud applications.

        Args:
            value: A dictionary containing the destination options to set for the cloud app restore operation.
                Example keys include:
                    - "destination_proxy" (bool): Whether to use a destination proxy.
                    - "restore_To_FileSystem" (bool): Whether to restore to the file system.
                    - "in_place" (bool): Whether to perform an in-place restore.
                    - "destination_path" (str): The path to restore data to.
                    - "destination_client" (str): The name of the destination client.
                    - "destination_instance_name" (str): The name of the destination instance.

        Example:
            >>> options = {
            ...     "destination_proxy": False,
            ...     "restore_To_FileSystem": False,
            ...     "in_place": False,
            ...     "destination_path": "/test/test1",
            ...     "destination_client": "test_client",
            ...     "destination_instance_name": "test_instance"
            ... }
            >>> cloud_instance._set_destination_options_json(options)

        #ai-gen-doc
        """
        proxy_option = value.get('destination_proxy', False)
        if value.get("restore_To_FileSystem"):

            self._set_cloud_destination_options_json = {
                "isLegalHold": False,
                "noOfStreams": value.get('no_of_streams', 2),
                "inPlace": value.get("in_place", ""),
                "destPath": [value.get("destination_path", "")],
                "destClient": {
                    "clientName": value.get("destination_client", "")
                }
            }

        else:

            if value.get("destination_client"):
                dest_client = value.get("destination_client", "")

            else:
                dest_client = self._agent_object._client_object.client_name

            if value.get("destination_instance_name"):
                dest_instance = value.get("destination_instance_name")

            else:
                dest_instance = self.instance_name

            regular_instance_restore_json = {
                "isLegalHold": False,
                "noOfStreams": value.get('no_of_streams', 2),
                "inPlace": value.get("in_place"),
                "destPath": [value.get("destination_path")],
                "destClient": {
                    "clientName": value.get("destination_client")
                }
            }
            if not proxy_option:
                destination_client_object = self._commcell_object.clients.get(dest_client)
                destination_agent_object = destination_client_object.agents.get('cloud apps')
                destination_instance_object = destination_agent_object.instances.get(dest_instance)
                destination_instance_details = {
                    "destinationInstance": {
                        "instanceName": value.get("destination_instance_name"),
                        "instanceId": int(destination_instance_object.instance_id)}}
                regular_instance_restore_json.update(
                    destination_instance_details)
            self._set_cloud_destination_options_json = regular_instance_restore_json

    def _set_restore_options_json(self, value: dict) -> None:
        """Set the cloud apps restore options in the restore JSON.

        This method updates the restore JSON with the specified options required for cloud apps restore operations.

        Args:
            value: A dictionary containing options to set cloud apps restore parameters.

        Example:
            >>> options = {
            ...     "restore_To_FileSystem": True
            ... }
            >>> cloud_storage_instance._set_restore_options_json(options)

        #ai-gen-doc
        """

        self._set_cloud_restore_options_json = {
            "instanceType": int(self.ca_instance_type),
            "cloudStorageRestoreOptions": {
                "restoreToFileSystem": value.get("restore_To_FileSystem"),
                "overrideCloudLogin": False,
                "restoreDestination": {
                    "instanceType": int(self.ca_instance_type)
                }
            }
        }

    def _set_common_options_json(self, value: dict) -> None:
        """Set the common options section in the restore JSON configuration.

        Args:
            value: A dictionary containing common options to be included in the restore JSON.

        Example:
            >>> common_options = {
            ...     "overwrite": True,
            ...     "preserveACL": False
            ... }
            >>> cloud_instance._set_common_options_json(common_options)
            >>> # The common options are now set for the restore operation

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._common_options_json = {
            "overwriteFiles": True,
            "unconditionalOverwrite": value.get("overwrite", False),
            "stripLevelType": 1
        }

    def _set_proxy_credential_json(self, destination_cloud: dict) -> None:
        """Construct the proxy credentials JSON for out-of-place cloud restore operations.

        This method prepares the necessary credential structure for cross-cloud restores by
        accepting a dictionary that specifies the destination cloud provider and its associated
        authentication details.

        Args:
            destination_cloud: A dictionary containing the destination cloud provider as the key,
                and a nested dictionary of credential parameters as the value.

                Example structures:
                    # For Google Cloud
                    destination_cloud = {
                        'google_cloud': {
                            'google_host_url': 'storage.googleapis.com',
                            'google_access_key': 'xxxxxx',
                            'google_secret_key': 'yyyyyy'
                        }
                    }

                    # For Amazon S3
                    destination_cloud = {
                        'amazon_s3': {
                            's3_host_url': 's3.amazonaws.com',
                            's3_access_key': 'xxxxxx',
                            's3_secret_key': 'yyyyyy'
                        }
                    }

                    # For Azure Blob
                    destination_cloud = {
                        'azure_blob': {
                            'azure_host_url': 'blob.core.windows.net',
                            'azure_account_name': 'xxxxxx',
                            'azure_access_key': 'yyyyyy'
                        }
                    }

        Example:
            >>> instance = CloudStorageInstance()
            >>> destination_cloud = {
            ...     'amazon_s3': {
            ...         's3_host_url': 's3.amazonaws.com',
            ...         's3_access_key': 'AKIA...',
            ...         's3_secret_key': 'SECRET...'
            ...     }
            ... }
            >>> instance._set_proxy_credential_json(destination_cloud)
            >>> # The proxy credentials JSON is now set for out-of-place restore

        #ai-gen-doc
        """

        if 'amazon_s3' in destination_cloud:
            self._proxy_credential_json = {
                "instanceType": 5,
                "s3Instance": {
                    "hostURL": destination_cloud.get('amazon_s3', {}).get('s3_host_url', 's3.amazonaws.com'),
                    "accessKeyId": destination_cloud.get('amazon_s3', {}).get('s3_access_key', ""),
                    "secretAccessKey": destination_cloud.get('amazon_s3', {}).get('s3_secret_key', "")
                }
            }

        elif 'google_cloud' in destination_cloud:
            self._proxy_credential_json = {
                "instanceType": 20,
                "googleCloudInstance": {
                    "serverName": destination_cloud.get('google_cloud', {}).get('google_host_url',
                                                                                'storage.googleapis.com'),
                    "credentials": {
                        "userName": destination_cloud.get('google_cloud', {}).get('google_access_key', ""),
                        "password": destination_cloud.get('google_cloud', {}).get('google_secret_key', "")
                    }
                }
            }

        elif 'azure_blob' in destination_cloud:
            self._proxy_credential_json = {
                "instanceType": 6,
                "azureInstance": {
                    "hostURL": destination_cloud.get('azure_blob', {}).get('azure_host_url', 'blob.core.windows.net'),
                    "accountName": destination_cloud.get('azure_blob', {}).get('azure_account_name', ""),
                    "accessKey": destination_cloud.get('azure_blob', {}).get('azure_access_key', "")
                }
            }

    def restore_using_proxy(
        self,
        paths: list,
        destination_client_proxy: str,
        destination_path: str,
        overwrite: bool = True,
        copy_precedence: int = None,
        destination_cloud: dict = None
    ) -> 'Job':
        """Restore files or folders to a different cloud using a proxy and explicit destination cloud credentials.

        This method initiates a restore operation to a specified cloud storage destination, using a proxy client
        with the required cloud connector package. Explicit credentials for the destination cloud must be provided.

        Args:
            paths: List of full file or folder paths to restore.
            destination_client_proxy: Name of the proxy machine with the cloud connector package installed.
            destination_path: Target location in the destination cloud instance where files will be restored.
            overwrite: If True, existing files at the destination will be unconditionally overwritten. Defaults to True.
            copy_precedence: Optional copy precedence value for the storage policy copy. Defaults to None.
            destination_cloud: Dictionary containing credentials for the destination cloud. The dictionary must
                specify exactly one supported cloud vendor and its required credentials. Example formats:

                For Google Cloud:
                    {
                        'google_cloud': {
                            'google_host_url': 'storage.googleapis.com',
                            'google_access_key': 'xxxxxx',
                            'google_secret_key': 'yyyyyy'
                        }
                    }

                For Amazon S3:
                    {
                        'amazon_s3': {
                            's3_host_url': 's3.amazonaws.com',
                            's3_access_key': 'xxxxxx',
                            's3_secret_key': 'yyyyyy'
                        }
                    }

                For Azure Blob:
                    {
                        'azure_blob': {
                            'azure_host_url': 'blob.core.windows.net',
                            'azure_account_name': 'xxxxxx',
                            'azure_access_key': 'yyyyyy'
                        }
                    }

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If any of the following conditions are met:
                - Destination cloud credentials are empty.
                - More than one vendor is specified in destination_cloud.
                - An unsupported destination cloud is chosen.
                - destination_client_proxy is not a string or Client object.
                - destination_path is not a string.
                - paths is not a list.
                - Failed to initialize the job.
                - The response is empty or not successful.

        Example:
            >>> paths = ['/data/file1.txt', '/data/file2.txt']
            >>> destination_client_proxy = 'cloud-proxy01'
            >>> destination_path = '/restore/target'
            >>> destination_cloud = {
            ...     'amazon_s3': {
            ...         's3_host_url': 's3.amazonaws.com',
            ...         's3_access_key': 'AKIA...',
            ...         's3_secret_key': 'SECRET...'
            ...     }
            ... }
            >>> job = cloud_instance.restore_using_proxy(
            ...     paths,
            ...     destination_client_proxy,
            ...     destination_path,
            ...     overwrite=True,
            ...     copy_precedence=1,
            ...     destination_cloud=destination_cloud
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        # Check if destination cloud credentials are empty
        if destination_cloud is None:
            raise SDKException(
                'Instance',
                '102',
                'Destination Cloud Credentials empty')

        if len(destination_cloud) > 1:
            raise SDKException(
                'Instance', '102', 'only one cloud vendor details can'
                                   'be passed.Multiple entries not allowed')

        cloud_vendors = ["google_cloud", "amazon_s3", "azure_blob"]
        # Check if destination cloud falls within supported cloud vendors
        cloud_vendors = ["google_cloud", "amazon_s3", "azure_blob"]
        # Check if destination cloud falls within supported cloud vendors
        dict_keys = list(destination_cloud.keys())
        if dict_keys[0] not in cloud_vendors:
            raise SDKException(
                'Instance',
                '102',
                'Unsupported destination cloud for restore')

        if not ((isinstance(destination_client_proxy, str) or
                 isinstance(destination_client_proxy, Client)) and
                isinstance(destination_path, str) and
                isinstance(paths, list) and
                isinstance(overwrite, bool)):
            raise SDKException('Instance', '101')

        request_json = self._generate_json(
            paths=paths,
            destination_proxy=True,
            destination_client=destination_client_proxy,
            destination_instance_name=None,
            destination_path=destination_path,
            overwrite=overwrite,
            in_place=False,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=False)
        self._set_proxy_credential_json(destination_cloud)
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["cloudAppsRestoreOptions"]["cloudStorageRestoreOptions"][
            "restoreDestination"] = self._proxy_credential_json
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "cloudAppsRestoreOptions"]["cloudStorageRestoreOptions"]["overrideCloudLogin"] = True
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "browseOption"]["backupset"].update({"backupsetName": "defaultBackupSet"})
        request_json["taskInfo"]["associations"][0]["backupsetName"] = "defaultBackupSet"

        return self._process_restore_response(request_json)