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

    def _get_instance_properties(self):
        """Gets the properties of this instance """
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

            if 'generalCloudProperties' in cloud_apps_instance:
                self._access_node = cloud_apps_instance.get(
                    'generalCloudProperties', {}).get(
                    'proxyServers', [{}])[0].get('clientName', cloud_apps_instance.get(
                    'generalCloudProperties', {}).get('memberServers', [{}])[
                    0].get('client', {}).get('clientName'))

    @property
    def google_host_url(self):
        """
        Returns google cloud URL as read only attribute

        Returns:
            (str)     -     string representing host URL of goole cloud
        """
        return self._google_host_url

    @property
    def google_access_key(self):
        """
        Returns google cloud account access key as read only attribute

        Returns:
            (str)     -     string representing google cloud account access key
        """
        return self._google_access_key

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
    def client_name(self):
        """
        Returns client name of this instance

            Returns:
                (str) - client name as registered in the commcell

        """
        return self._properties.get('instance', {}).get('clientName')

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
        cloud_restore_json["taskInfo"]["associations"][0]["backupsetId"] =  int(self._agent_object.backupsets.get(
            'defaultBackupSet').backupset_id)

        return cloud_restore_json

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            copy_precedence=None,
            no_of_streams=2):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                no_of_streams           (int)   --  number of streams for restore
                                                    default : 2

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
            paths,
            destination_client,
            destination_instance_name,
            destination_path,
            overwrite=True,
            copy_precedence=None,
            no_of_streams=2):
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

                no_of_streams           (int)   --  number of streams for restore
                                                    default : 2

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
            no_of_streams=no_of_streams,
            restore_To_FileSystem=False)

        return self._process_restore_response(request_json)

    def restore_to_fs(
            self,
            paths,
            destination_path,
            destination_client=None,
            overwrite=True,
            copy_precedence=None,
            no_of_streams=2):
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

                no_of_streams           (int)   --  number of streams for restore
                                                    default : 2

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

        destination_appTypeId = int(self._commcell_object.clients.get(destination_client).agents.get('file system').agent_id)

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

    def _set_destination_options_json(self, value):
        """setter for cloud apps destination options in restore JSON

        Args:
            value    (dict)    --    options needed to set the cloud apps destination parameters

        Example:
            value = {
                "destination_proxy":False,
                "restore_To_FileSystem" : False
                "in_place" : False
                "destination_path" : "/test/test1"
                "destination_client" : "test_client"
                "destination_instance_name" : "test_instance"
            }

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

    def _set_common_options_json(self, value):
        """
        Setter for the Common options in restore JSON

            Args:
                value   (dict)  --  dict of common options
                                    for restore json

        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._common_options_json = {
            "overwriteFiles": True,
            "unconditionalOverwrite": value.get("overwrite", False),
            "stripLevelType": 1
        }

    def _set_proxy_credential_json(self, destination_cloud):
        """
        Method to construct the proxy credentials json for out of place restore

        Args:
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
                    "serverName": destination_cloud.get('google_cloud', {}).get('google_host_url', 'storage.googleapis.com'),
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

        if not ((isinstance(destination_client_proxy, basestring) or
                 isinstance(destination_client_proxy, Client)) and
                isinstance(destination_path, basestring) and
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
