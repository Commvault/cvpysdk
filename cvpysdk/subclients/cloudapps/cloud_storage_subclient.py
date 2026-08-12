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

"""File for operating on a Cloud Storage Subclient.

CloudStorageSubclient is the only class defined in this file.

CloudStorageSubclient:  Derived class from CloudAppsSubclient Base class, representing a
                        Cloud Storage subclient(S3,Azure,Oraclecloud and Openstack), and
                        to perform operations on that subclient

CloudStorageSubclient:

    _get_subclient_properties()         --  gets the properties of Cloud Storage Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of Cloud Storage Subclient

    content()                           --  gets the content of the subclient

    _set_content()                      --  sets the content of the subclient

    restore_in_place()                  --  Restores the files/folders specified in the
    input paths list to the same location

    restore_out_of_place()              --  Restores the files/folders specified in the
    input paths list to the input client, at the specified destination location

    restore_to_fs()                     --  Restores the files/folders specified in the
    input paths list to the input fs client, at the specified destination location.

    restore_using_proxy()               --  To perform restore to different cloud using
                                            proxy passing explicit credentials of destination cloud

"""
from typing import Optional

from ..casubclient import CloudAppsSubclient
from ...exception import SDKException
from ...job import Job

class CloudStorageSubclient(CloudAppsSubclient):
    """
    Represents a Cloud Storage subclient for managing and performing operations on cloud-based data.

    This class extends the CloudAppsSubclient base class and provides specialized methods for
    handling cloud storage subclient properties, content management, and various restore operations.
    It is designed to facilitate backup, recovery, and content configuration tasks for cloud storage
    environments.

    Key Features:
        - Retrieve subclient properties and properties in JSON format
        - Manage subclient content with getter and setter methods
        - Restore data in place within the original location
        - Restore data out of place to a different client, instance, or path
        - Restore data to a file system destination
        - Restore data using a proxy to a cloud destination
        - Support for overwrite options, copy precedence, and stream configuration during restore operations

    #ai-gen-doc
    """

    def _get_subclient_properties(self) -> dict:
        """Retrieve the properties specific to the Cloud Storage subclient.

        Returns:
            dict: A dictionary containing the subclient-related properties for the Cloud Storage subclient.

        Example:
            >>> properties = cloud_storage_subclient._get_subclient_properties()
            >>> print(properties)
            >>> # Output will be a dictionary with subclient property details

        #ai-gen-doc
        """
        super(CloudStorageSubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

    def _get_subclient_properties_json(self) -> dict:
        """Retrieve the properties JSON for the Cloud Storage Subclient.

        Returns:
            dict: A dictionary containing all properties of the Cloud Storage Subclient.

        Example:
            >>> subclient = CloudStorageSubclient()
            >>> properties = subclient._get_subclient_properties_json()
            >>> print(properties)
            >>> # Output will be a dictionary with subclient configuration details

        #ai-gen-doc
        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "cloudAppsSubClientProp": {
                        "instanceType": self._backupset_object._instance_object.ca_instance_type
                    },
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    def _set_content(self, content: Optional[list] = None) -> None:
        """Set the content for the cloud storage subclient.

        This method assigns the specified content list to the subclient, defining which data or objects
        are included in backup or restore operations.

        Args:
            content: Optional list specifying the subclient content. If not provided, the content will be set to an empty list or default value.

        Example:
            >>> subclient = CloudStorageSubclient()
            >>> subclient._set_content(['bucket1/folderA', 'bucket2/folderB'])
            >>> # The subclient content is now set to the specified cloud storage paths

        #ai-gen-doc
        """
        if content is None:
            content = self.content

        update_content = []
        for path in content:
            cloud_dict = {
                "path": path
            }
            update_content.append(cloud_dict)

        self._set_subclient_properties("_content", update_content)

    @property
    def content(self) -> list:
        """Retrieve the content associated with the CloudStorageSubclient.

        Returns:
            list: A list containing the content items relevant to the subclient.

        Example:
            >>> subclient = CloudStorageSubclient()
            >>> content_list = subclient.content
            >>> print(f"Subclient content: {content_list}")

        #ai-gen-doc
        """
        content = []

        for path in self._content:
            if 'path' in path:
                content.append(path["path"])

        return content

    @content.setter
    def content(self, subclient_content: list) -> None:
        """Set the content for the Cloud Storage Subclient.

        This setter creates and assigns the list of content JSON objects required to add or update
        the content of a Cloud Storage Subclient. The provided list should contain the content items
        to be managed by the subclient.

        Args:
            subclient_content: A list containing the content items to add to the subclient.

        Raises:
            SDKException: If the subclient_content is not a list or if it is empty.

        Example:
            >>> cloud_subclient = CloudStorageSubclient()
            >>> new_content = ['bucket1/folderA', 'bucket2/folderB']
            >>> cloud_subclient.content = new_content  # Use assignment for property setter
            >>> # The subclient content is now updated with the specified items

        #ai-gen-doc
        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def restore_in_place(
            self,
            paths: list,
            overwrite: bool = True,
            copy_precedence: int = None,
            no_of_streams: int = 2
        ) -> 'Job':
        """Restore the specified files or folders to their original location in the cloud storage subclient.

        Args:
            paths: List of full file or folder paths to restore in place.
            overwrite: If True, existing files at the destination will be overwritten. Defaults to True.
            copy_precedence: Optional storage policy copy precedence value to use for the restore. If None, the default copy is used.
            no_of_streams: Number of parallel streams to use for the restore operation. Defaults to 2.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> subclient = CloudStorageSubclient(commcell_object, client_name, instance_name, backupset_name, subclient_name)
            >>> restore_paths = ["/data/file1.txt", "/data/folder1/"]
            >>> job = subclient.restore_in_place(restore_paths, overwrite=True, copy_precedence=1, no_of_streams=4)
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        self._instance_object._restore_association = self._subClientEntity

        return self._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            no_of_streams=no_of_streams)

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
        `destination_client` and `destination_instance_name` at the given `destination_path`.
        The restore operation can be customized with options such as overwriting existing files,
        specifying copy precedence, and setting the number of streams. Additional restore
        options can be provided via keyword arguments.

        Args:
            paths: List of full file or folder paths to restore.
            destination_client: Name of the client to which the data will be restored.
            destination_instance_name: Name of the instance on the destination client.
            destination_path: Path on the destination instance where data will be restored.
            overwrite: If True, existing files at the destination will be overwritten. Defaults to True.
            copy_precedence: Optional; storage policy copy precedence value. Defaults to None.
            no_of_streams: Number of streams to use for the restore. Defaults to 2.
            **kwargs: Additional keyword arguments for advanced restore options:
                - from_time (str): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS').
                - to_time (str): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS').
                - no_image (bool): If True, restore deleted items. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> subclient = CloudStorageSubclient()
            >>> job = subclient.restore_out_of_place(
            ...     paths=['/data/file1.txt', '/data/file2.txt'],
            ...     destination_client='client2',
            ...     destination_instance_name='instanceB',
            ...     destination_path='/restore/location',
            ...     overwrite=True,
            ...     copy_precedence=1,
            ...     no_of_streams=4,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     no_image=False
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        self._instance_object._restore_association = self._subClientEntity

        return self._instance_object.restore_out_of_place(
            paths=paths,
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            destination_path=destination_path,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            no_of_streams=no_of_streams,
            **kwargs)

    def restore_to_fs(
            self,
            paths: list,
            destination_path: str,
            destination_client: str = None,
            overwrite: bool = True,
            copy_precedence: int = None,
            no_of_streams: int = 2
        ) -> 'Job':
        """Restore specified files or folders from cloud storage to a file system client.

        This method initiates a restore job to copy the given files or folders from cloud storage
        to the specified destination path on a file system client. You can control overwrite behavior,
        copy precedence, and the number of restore streams.

        Args:
            paths: List of full file or folder paths to restore from cloud storage.
            destination_path: The target directory path on the destination client where files/folders will be restored.
            destination_client: Name of the file system client to restore to. If None, restores to the backup or proxy client.
            overwrite: If True, existing files at the destination will be overwritten. Defaults to True.
            copy_precedence: Optional storage policy copy precedence value. If None, the default precedence is used.
            no_of_streams: Number of parallel streams to use for the restore operation. Defaults to 2.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Example:
            >>> subclient = CloudStorageSubclient()
            >>> restore_job = subclient.restore_to_fs(
            ...     paths=['/cloud/data/file1.txt', '/cloud/data/folder/'],
            ...     destination_path='/mnt/restore/',
            ...     destination_client='FSClient01',
            ...     overwrite=True,
            ...     copy_precedence=1,
            ...     no_of_streams=4
            ... )
            >>> print(f"Restore job started with ID: {restore_job.job_id}")

        #ai-gen-doc
        """

        self._instance_object._restore_association = self._subClientEntity

        if destination_client is None:
            destination_client = self._instance_object.backup_client

        return self._instance_object.restore_to_fs(
            paths=paths,
            destination_path=destination_path,
            destination_client=destination_client,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            no_of_streams=no_of_streams)

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

        This method allows you to restore specified files or folders to a different cloud storage provider
        by routing the restore through a proxy machine with the cloud connector package installed.
        You must provide the destination cloud credentials explicitly in the `destination_cloud` parameter.

        Args:
            paths: List of full file or folder paths to restore.
            destination_client_proxy: Name of the proxy machine with the cloud connector package.
            destination_path: Target location in the destination cloud where files will be restored.
            overwrite: If True, existing files at the destination will be overwritten. Defaults to True.
            copy_precedence: Optional copy precedence value for the storage policy copy.
            destination_cloud: Dictionary containing credentials for the destination cloud provider.
                The dictionary should have a single key for the cloud vendor (e.g., 'google_cloud', 'amazon_s3', 'azure_blob'),
                with a nested dictionary of required credentials. Example:

                destination_cloud = {
                    'google_cloud': {
                        'google_host_url': 'storage.googleapis.com',
                        'google_access_key': 'xxxxxx',
                        'google_secret_key': 'yyyyyy'
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
            >>> restore_paths = ['/data/file1.txt', '/data/file2.txt']
            >>> proxy = 'cloud-proxy01'
            >>> dest_path = '/restore/target/'
            >>> dest_cloud = {
            ...     'amazon_s3': {
            ...         's3_host_url': 's3.amazonaws.com',
            ...         's3_access_key': 'AKIAxxxxxx',
            ...         's3_secret_key': 'yyyyyyyy'
            ...     }
            ... }
            >>> job = subclient.restore_using_proxy(
            ...     paths=restore_paths,
            ...     destination_client_proxy=proxy,
            ...     destination_path=dest_path,
            ...     overwrite=True,
            ...     destination_cloud=dest_cloud
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        self._instance_object._restore_association = self._subClientEntity

        return self._instance_object.restore_using_proxy(paths=paths,
                                                         destination_client_proxy=destination_client_proxy,
                                                         destination_path=destination_path,
                                                         overwrite=overwrite,
                                                         copy_precedence=copy_precedence,
                                                         destination_cloud=destination_cloud
                                                         )