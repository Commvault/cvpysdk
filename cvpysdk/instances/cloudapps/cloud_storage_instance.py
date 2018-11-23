# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

""" File for operating on a cloud storage instance.

CloudStorageInstance is the only class defined in this file.

CloudStorageInstance:   Derived class from CloudAppsInstance Base class, representing a
                        Cloud Storage instance(S3,Azure,Oraclecloud and Openstack), and to
                        perform operations on that instance

CloudStorageInstance:

    _get_instance_properties()            --  Instance class method overwritten to add cloud apps
    instance properties as well

    _generate_json()                      --  Returns the JSON request to pass to the API as per
    the options selected by the user

    _restore_in_place()                   --  restores the files/folders specified in the
    input paths list to the same location.

    _restore_out_of_place()               --  restores the files/folders specified in the input
    paths list to the input client, at the specified destination location.

    _restore_to_fs()                      --  restores the files/folders specified in the input
    paths list to the input fs client, at the specified destination location.

    _set_destination_options_json()       --  setter for cloud apps destination options in
    restore JSON

    _set_restore_options_json()           --  setter for cloudapps restore options in restore JSON

"""
from past.builtins import basestring
from cvpysdk.instances.cainstance import CloudAppsInstance
from cvpysdk.client import Client
from cvpysdk.exception import SDKException


class CloudStorageInstance(CloudAppsInstance):
    """Class for representing an Instance of the cloud storage instance type."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the CloudStorageInstance class.

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class

        """

        self._ca_instance_type = None
        self._host_url = None
        self._access_keyid = None
        self._secret_accesskey = None
        self._account_name = None
        self._access_key = None
        self._server_name = None
        self._username = None
        self._endpointurl = None
        self._access_node = None
        self._set_cloud_destination_options_json = None
        self._set_cloud_restore_options_json = None

        super(CloudStorageInstance, self).__init__(agent_object, instance_name, instance_id)

    def _get_instance_properties(self):
        """Gets the properties of this instance"""
        super(CloudStorageInstance, self)._get_instance_properties()

        if 'cloudAppsInstance' in self._properties:
            cloud_apps_instance = self._properties['cloudAppsInstance']
            self._ca_instance_type = cloud_apps_instance['instanceType']

            if 's3Instance' in cloud_apps_instance:
                s3instance = cloud_apps_instance['s3Instance']

                self._host_url = s3instance['hostURL']
                self._access_keyid = s3instance['accessKeyId']
                self._secret_accesskey = s3instance['secretAccessKey']

            if 'azureInstance' in cloud_apps_instance:
                azureinstance = cloud_apps_instance['azureInstance']

                self._host_url = azureinstance['hostURL']
                self._account_name = azureinstance['accountName']
                self._access_key = azureinstance['accessKey']

            if 'openStackInstance' in cloud_apps_instance:

                self._server_name = cloud_apps_instance['openStackInstance']['serverName']
                self._username = cloud_apps_instance['openStackInstance']['credentials'][
                    'userName']

            if 'oraCloudInstance' in cloud_apps_instance:
                oraclecloudinstance = cloud_apps_instance['oraCloudInstance']

                self._endpointurl = oraclecloudinstance['endpointURL']
                self._username = oraclecloudinstance['user']['userName']

            if 'generalCloudProperties' in cloud_apps_instance:
                self._access_node = cloud_apps_instance[
                    'generalCloudProperties']['proxyServers'][0]['clientName']

    @property
    def ca_instance_type(self):
        """Returns the CloudApps instance type as a read-only attribute."""
        return self._ca_instance_type

    @property
    def host_url(self):
        """Returns the host URL property as a read-only attribute."""
        return self._host_url

    @property
    def access_key(self):
        """Returns the access key property as a read-only attribute."""
        return self._access_key

    @property
    def account_name(self):
        """Returns the account name as a read-only attribute."""
        return self._account_name

    @property
    def access_keyid(self):
        """Returns the access key ID property as a read-only attribute."""
        return self._access_keyid

    @property
    def secret_accesskey(self):
        """Returns the secret access key as a read-only attribute."""
        return self._secret_accesskey

    @property
    def server_name(self):
        """Returns the server name property as a read-only attribute."""
        return self._server_name

    @property
    def username(self):
        """Returns the username property as a read-only attribute."""
        return self._username

    @property
    def endpointurl(self):
        """Returns the endpoint URL property as a read-only attribute."""
        return self._endpointurl

    @property
    def access_node(self):
        """Returns the access node of this instance as a read-only attribute."""
        return self._access_node

    def _generate_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (list)  --  list of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API

        """
        cloud_restore_json = super(CloudStorageInstance, self)._restore_json(**kwargs)
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

        cloud_restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["destination"] = self._set_cloud_destination_options_json
        cloud_restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["cloudAppsRestoreOptions"] = self._set_cloud_restore_options_json
        cloud_restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["commonOptions"] = {
                "stripLevelType": 1
            }

        return cloud_restore_json

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            copy_precedence=None):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        if not (isinstance(paths, list) and
                isinstance(overwrite, bool)):

            raise SDKException('Instance', '101')

        request_json = self._generate_json(
            paths=paths,
            destination_client=None,
            destination_instance_name=None,
            overwrite=overwrite,
            in_place=True,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=False)

        return self._process_restore_response(request_json)

    def restore_out_of_place(
            self,
            paths,
            destination_client,
            destination_instance_name,
            destination_path,
            overwrite=True,
            copy_precedence=None):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destination location.

            Args:
                paths                    (list)  --  list of full paths of files/folders to restore

                destination_client       (str)   --  name of the client to which the files
                    are to be restored.

                destination_instance_name(str)   --  name of the instance to which the files
                    are to be restored.

                destination_path         (str)   --  location where the files are to be restored
                    in the destination instance.

                overwrite                (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence          (int)   --  copy precedence value of storage policy copy
                    default: None


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client object

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        if not ((isinstance(destination_client, basestring) or
                 isinstance(destination_client, Client)) and
                isinstance(destination_instance_name, basestring) and
                isinstance(destination_path, basestring) and
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
            restore_To_FileSystem=False)

        return self._process_restore_response(request_json)

    def restore_to_fs(
            self,
            paths,
            destination_path,
            destination_client=None,
            overwrite=True,
            copy_precedence=None):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destination location.

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

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or client object

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        if not ((isinstance(destination_client, basestring) or
                 isinstance(destination_client, Client)) and
                isinstance(destination_path, basestring) and
                isinstance(paths, list) and
                isinstance(overwrite, bool)):

            raise SDKException('Instance', '101')

        request_json = self._generate_json(
            paths=paths,
            destination_path=destination_path,
            destination_client=destination_client,
            overwrite=overwrite,
            in_place=False,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=True)

        return self._process_restore_response(request_json)

    def _set_destination_options_json(self, value):
        """setter for cloud apps destination options in restore JSON

        Args:
            value    (dict)    --    options needed to set the cloud apps destination parameters

        Example:
            value = {
                "restore_To_FileSystem" : False
                "in_place" : False
                "destination_path" : "/test/test1"
                "destination_client" : "test_client"
                "destination_instance_name" : "test_instance"
            }

        """
        if value.get("restore_To_FileSystem"):

            self._set_cloud_destination_options_json = {
                "isLegalHold": False,
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

            dclient = self._commcell_object.clients.get(dest_client)
            dagent = dclient.agents.get('Cloud Apps')
            dinstance = dagent.instances.get(dest_instance)

            self._set_cloud_destination_options_json = {
                "isLegalHold": False,
                "inPlace": value.get("in_place"),
                "destPath": [value.get("destination_path")],
                "destClient": {
                    "clientName": value.get("destination_client"),
                    "clientId": int(dclient.client_id)
                },

                "destinationInstance": {
                    "instanceName": value.get("destination_instance_name"),
                    "instanceId": int(dinstance.instance_id)
                }
            }

    def _set_restore_options_json(self, value):
        """setter for cloudapps restore options in restore JSON

        Args:
            value    (dict)    --    options needed to set the cloud apps restore parameters

        Example:
            value = {
                "restore_To_FileSystem": True
                }

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
