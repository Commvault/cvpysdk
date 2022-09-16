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
from ..casubclient import CloudAppsSubclient
from ...exception import SDKException


class CloudStorageSubclient(CloudAppsSubclient):
    """ Derived class from Subclient Base class, representing a Cloud Storage subclient,
        and to perform operations on that subclient. """

    def _get_subclient_properties(self):
        """ Gets the subclient related properties of Cloud Storage subclient. """
        super(CloudStorageSubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

    def _get_subclient_properties_json(self):
        """ Gets the properties JSON of Cloud Storage Subclient.

           Returns:
                dict - all subclient properties put inside a dict

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

    def _set_content(self,
                     content=None):
        """ Sets the subclient content

            Args:
                content         (list)      --  list of subclient content

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
    def content(self):
        """ Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient

        """
        content = []

        for path in self._content:
            if 'path' in path:
                content.append(path["path"])

        return content

    @content.setter
    def content(self, subclient_content):
        """ Creates the list of content JSON to pass to the API to add/update content of a
            Cloud Storage Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API

            Raises :
                SDKException : if the subclient content is not a list value and if it is empty

        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            copy_precedence=None,
            no_of_streams=2):
        """ Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders
                     to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                no_of_streams           (int)   --  number of streams for restore
                                                    default : 2

            Returns:
                object - instance of the Job class for this restore job

        """

        self._instance_object._restore_association = self._subClientEntity

        return self._instance_object.restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            no_of_streams=no_of_streams)

    def restore_out_of_place(
            self,
            paths,
            destination_client,
            destination_instance_name,
            destination_path,
            overwrite=True,
            copy_precedence=None,
            no_of_streams=2,
            **kwargs):

        """ Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                paths                    (list)  --  list of full paths of files/folders to restore

                destination_client       (str)   --  name of the client to which the files are
                    to be restored.
                    default: None for in place restores

                destination_instance_name(str)   --  name of the instance to which the files are
                    to be restored.
                    default: None for in place restores

                destination_path         (str)   --  location where the files are to be restored
                    in the destination instance.

                overwrite                (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence          (int)   --  copy precedence value of storage policy copy
                    default: None

                no_of_streams           (int)   --  number of streams for restore
                                                    default : 2

                kwargs                  (dict)  -- dict of keyword arguments as follows

                    from_time           (str)   --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS
                        default: None

                    to_time             (str)   --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS
                        default: None

                    no_image            (bool)  --  restore deleted items
                        default: False

            Returns:
                object - instance of the Job class for this restore job

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
            paths,
            destination_path,
            destination_client=None,
            overwrite=True,
            copy_precedence=None,
            no_of_streams=2):
        """ Restores the files/folders specified in the input paths list to the fs client

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                destination_path        (str)   --  location where the files are to be restored
                    in the destination instance.

                destination_client      (str)   --  name of the fs client to which the files
                    are to be restored.
                    default: None for restores to backup or proxy client.

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                no_of_streams           (int)   --  number of streams for restore
                                                    default : 2

            Returns:
                object - instance of the Job class for this restore job

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

    def restore_using_proxy(self,
                            paths,
                            destination_client_proxy,
                            destination_path,
                            overwrite=True,
                            copy_precedence=None,
                            destination_cloud=None):
        """
        To perform restore to different cloud using
        proxy passing explicit credentials of destination cloud

        Args:
            destination_client_proxy (str)          --  name of proxy machine having cloud connector package

            paths                    (list)         --  list of full paths of files/folders to restore

            destination_path         (str)          --  location where the files are to be restored
                                                        in the destination instance.

            overwrite                (bool)         --  unconditional overwrite files during restore
                                                        default: True

            copy_precedence          (int)          --  copy precedence value of storage policy copy
                                                        default: None


            destination_cloud        (dict(dict))  --     dict of dict representing cross cloud credentials

            Sample dict(dict) :

            destination_cloud = {
                                    'google_cloud': {
                                                        'google_host_url':'storage.googleapis.com',
                                                        'google_access_key':'xxxxxx',
                                                        'google_secret_key':'yyyyyy'
                                                    }
                                }

            destination_cloud = {
                                    'amazon_s3':    {
                                                        's3_host_url':'s3.amazonaws.com',
                                                        's3_access_key':'xxxxxx',
                                                        's3_secret_key':'yyyyyy'
                                                    }
                                }
            destination_cloud = {
                                    'azure_blob':   {
                                                        'azure_host_url':'blob.core.windows.net',
                                                        'azure_account_name':'xxxxxx',
                                                        'azure_access_key':'yyyyyy'
                                                    }
                                }

        Returns:
                object - instance of the Job class for this restore job

        Raises:
            SDKException:

                    if destination cloud credentials empty

                    if destination cloud has more than one vendor details

                    if unsupported destination cloud for restore is chosen

                    if client is not a string or Client object

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        self._instance_object._restore_association = self._subClientEntity

        return self._instance_object.restore_using_proxy(paths=paths,
                                                         destination_client_proxy=destination_client_proxy,
                                                         destination_path=destination_path,
                                                         overwrite=overwrite,
                                                         copy_precedence=copy_precedence,
                                                         destination_cloud=destination_cloud
                                                         )
