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



    _restore_json_cloud()          --  returns the appropriate JSON request to pass for in place,
    out of place and restores to file system.

    _restore_in_place_cloud()      --  restores the files/folders specified in the
    input paths list to the same location.

    _restore_out_of_place_cloud()  --  restores the files/folders specified in the input paths
    list to the input client, at the specified destination location.

    _restore_to_fs_cloud()         --  restores the files/folders specified in the input paths
    list to the input fs client, at the specified destination location.

    _restore_browse_option_json()   --  setter for  browse option  property in restore

    _restore_commonOptions_json()   --  setter for common options property in restore

    _restore_destination_json()     --  setter for destination options property in restore

    _restore_fileoption_json()      -- setter for file option property in restore

    _restore_cloudappsoption_json_cloud  -- setter for cloud apps restore option in restore
"""

from __future__ import unicode_literals
from past.builtins import basestring
from cvpysdk.instance import Instance
from cvpysdk.exception import SDKException
from cvpysdk.client import Client


class CloudAppsInstance(Instance):
    """Class for representing an Instance of the Cloud Apps agent."""

    def __new__(cls, agent_object, instance_name, instance_id):
        from .cloudapps.google_instance import GoogleInstance
        from .cloudapps.s3_instance import S3Instance

        instance_type = {
            1: GoogleInstance,
            2: GoogleInstance,
            5: S3Instance
        }

        commcell_object = agent_object._commcell_object
        instance_service = 'Instance/{0}'.format(instance_id)

        response = commcell_object.request('GET', instance_service)

        if response.json() and "instanceProperties" in response.json():
            properties = response.json()["instanceProperties"][0]
        else:
            raise SDKException('Instance', '102', 'Failed to get the properties of the Instance')

        cloud_apps_instance_type = properties['cloudAppsInstance']['instanceType']

        return object.__new__(instance_type[cloud_apps_instance_type])

    def _restore_json(
            self,
            **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (list)  --  list of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API
        """

        restore_option_cloud = {}
        if kwargs.get("restore_option_cloud"):
            restore_option_cloud = kwargs["restore_option_cloud"]
            for key in kwargs:
                if not key == "restore_option_cloud":
                    restore_option_cloud[key] = kwargs[key]
        else:
            restore_option_cloud.update(kwargs)

        if self._restore_association is None:
            self._restore_association = self._instance

        self._restore_browse_option_json_cloud(restore_option_cloud)
        self._restore_common_options_json_cloud(restore_option_cloud)
        self._restore_destination_json_cloud(restore_option_cloud)
        self._restore_fileoption_json_cloud(restore_option_cloud)
        self._restore_cloudappsoption_json_cloud(restore_option_cloud)

        request_json_cloud = {
            "taskInfo": {
                "associations": [self._restore_association],
                "task": self._task,
                "subTasks": [{
                    "subTaskOperation": 1,
                    "subTask": self._restore_sub_task,
                    "options": {
                        "restoreOptions": {

                            "browseOption": self._destination_restore_json_cloud,
                            "commonOptions": self._commonoption_restore_json_cloud,
                            "destination": self._destination_restore_json_cloud,
                            "fileOption": self._fileoption_restore_json_cloud,
                            "cloudAppsRestoreOptions": self._cloudappsoption_restore_json_cloud
                        }
                    }
                }]
            }
        }

        return request_json_cloud

    def _restore_in_place(
            self,
            paths,
            destination_client=None,
            destination_instance_name=None,
            overwrite=True,
            in_place=True,
            copy_precedence=None,
            restore_To_FileSystem=False):
        """Restores the files/folders specified in the input paths list to the same location.
            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                destination_client      (str)   --  name of the client to which the files are
                    to be restored.
                    default: None for in place restores

                destination_instance_name(str)  --  name of the instance to which the files
                    are to be restored.
                    default: None for in place restores

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                in_place                (bool)  --  denotes whether it's an inplace restore or not
                    default: True for in place restores

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                restore_To_FileSystem   (bool)  --  denotes whether it's a restore to fs or not

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
                isinstance(overwrite, bool) and
                isinstance(in_place, bool) and
                isinstance(restore_To_FileSystem, bool)):

            raise SDKException('Subclient', '101')

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json_cloud = self._restore_json(
            paths=paths,
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            overwrite=overwrite,
            in_place=in_place,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=restore_To_FileSystem)

        return self._process_restore_response(request_json_cloud)

    def _restore_out_of_place(
            self,
            paths,
            destination_client,
            destination_instance_name,
            destination_path,
            overwrite=True,
            in_place=False,
            copy_precedence=None,
            restore_To_FileSystem=False
    ):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                destination_client      (str)   --  name of the client to which the files
                    are to be restored.
                    default: None for in place restores

                destination_instance_name(str)  --  name of the instance to which the files
                    are to be restored.
                    default: None for in place restores

                destination_path         (str)  --  location where the files are to be restored
                    in the destination instance.

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                in_place                (bool)  --  denotes whether it's an inplace restore or not
                    default: False for out of place restores

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                restore_To_FileSystem   (bool)  --  denotes whether it's a restore to fs or not
                    default: False for restores other than restores to FS

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

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
                isinstance(overwrite, bool) and
                isinstance(in_place, bool) and
                isinstance(restore_To_FileSystem, bool)):

            raise SDKException('Subclient', '101')

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json_cloud = self._restore_json(
            paths=paths,
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            destination_path=destination_path,
            overwrite=overwrite,
            in_place=in_place,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=restore_To_FileSystem
        )

        return self._process_restore_response(request_json_cloud)

    def _restore_to_fs(
            self,
            paths,
            destination_path,
            destination_client=None,
            overwrite=True,
            in_place=False,
            copy_precedence=None,
            restore_To_FileSystem=True
    ):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                destination_path         (str)  --  location where the files are to be restored
                    in the destination instance.

                destination_client      (str)   --  name of the fs client to which the files
                    are to be restored.
                    default: None for restores to backup or proxy client.

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                in_place                (bool)  --  denotes whether it's an inplace restore or not
                    default: False for out of place restores

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                restore_To_FileSystem   (bool)  --  denotes whether it's a restore to fs or not
                    default: True for restores to FS

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance

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
                isinstance(overwrite, bool) and
                isinstance(in_place, bool) and
                isinstance(restore_To_FileSystem, bool)):

            raise SDKException('Subclient', '101')

        request_json_cloud = self._restore_json(
            paths=paths,
            destination_path=destination_path,
            destination_client=destination_client,
            overwrite=overwrite,
            in_place=in_place,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=restore_To_FileSystem
        )

        return self._process_restore_response(request_json_cloud)

    def _restore_browse_option_json_cloud(self, value):
        """setter  the Browse options for restore in Json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        if "copy_precedence" in value:
            value["copy_precedence_applicable"] = True

        time_range_dict = {}
        if value.get('from_time'):
            time_range_dict['fromTimeValue'] = value.get('from_time')

        if value.get('to_time'):
            time_range_dict['toTimeValue'] = value.get('to_time')

        self._browse_restore_json_cloud = {
            "listMedia": False,
            "useExactIndex": False,
            "noImage": False,
            "commCellId": 2,
            "mediaOption": {
                "mediaAgent": {
                    "mediaAgentName": value.get("media_agent", "")
                },
                "library": {},
                "copyPrecedence": {
                    "copyPrecedenceApplicable": value.get("copy_precedence_applicable", False),
                    "copyPrecedence": value.get("copy_precedence", 0)
                },
                "drivePool": {}
            },
            "backupset": {
                "clientName": value.get("destination_client", ""),
                "appName": self._agent_object.agent_name
            },
            "timeZone": {
                "TimeZoneName": "(UTC) Coordinated Universal Time",
            },
            "timeRange": time_range_dict
        }

    def _restore_common_options_json_cloud(self, value):
        """setter for  the Common options in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json_cloud = {
            "systemStateBackup": False,
            "clusterDBBackedup": False,
            "powerRestore": False,
            "restoreToDisk": False,
            "offlineMiningRestore": False,
            "preserveLevel": value.get("preserve_level", 1),
            "stripLevelType": value.get("striplevel_type", 1),
            "stripLevel": value.get("strip_level", 0),
            "overwriteFiles": True,
            "copyToObjectStore": False,
            "onePassRestore": False,
            "doNotOverwriteFileOnDisk": False,
            "unconditionalOverwrite": value.get("unconditional_overwrite", False),
            "syncRestore": False,
            "detectRegularExpression": True,
            "wildCard": False
        }

    def _restore_destination_json_cloud(self, value):
        """setter for  the destination restore option in restore JSON"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        if value.get("restore_To_FileSystem") is False:

            if value.get("destination_client") is None:
                dest_client = self._agent_object._client_object.client_name

            else:
                dest_client = value.get("destination_client", "")

            if value.get("destination_instance_name") is None:
                dest_instance = self.instance_name

            else:
                dest_instance = value.get("destination_instance_name", "")

            dclient = self._commcell_object.clients.get(dest_client)
            dagent = dclient.agents.get('Cloud Apps')
            dinstance = dagent.instances.get(dest_instance)

            self._destination_restore_json_cloud = {
                "isLegalHold": False,
                "inPlace": value.get("in_place", ""),
                "destPath": [value.get("destination_path", "")],
                "destClient": {
                    "clientName": value.get("destination_client", ""),
                    "clientId": int(dclient.client_id)

                },
                "destinationInstance": {
                    "instanceName": value.get("destination_instance_name", ""),
                    "instanceId": int(dinstance.instance_id)
                }
            }

        else:

            self._destination_restore_json_cloud = {
                "isLegalHold": False,
                "inPlace": value.get("in_place", ""),
                "destPath": [value.get("destination_path", "")],
                "destClient": {
                    "clientName": value.get("destination_client", "")
                }
            }

    def _restore_fileoption_json_cloud(self, value):
        """setter for  the fileoption restore option in restore JSON"""

        self._fileoption_restore_json_cloud = {
            "sourceItem": value.get("paths", [])

        }

    def _restore_cloudappsoption_json_cloud(self, value):
        """setter for the cloudapps restore option in restore JSON"""

        self._cloudappsoption_restore_json_cloud = {
            "instanceType": int(self.ca_instance_type),
            "cloudStorageRestoreOptions": {
                "restoreToFileSystem": value.get("restore_To_FileSystem", ""),
                "overrideCloudLogin": False,
                "restoreDestination": {
                    "instanceType": int(self.ca_instance_type)
                }
            }
        }

    def restore_instance(
            self,
            paths,
            destination_client=None,
            destination_instance_name=None,
            overwrite=True,
            in_place=True,
            copy_precedence=None,
            restore_To_FileSystem=False):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                destination_client      (str)   --  name of the client to which the files
                    are to be restored.
                    default: None for in place restores

                destination_instance_name(str)  --  name of the instance to which the files
                    are to be restored.
                    default: None for in place restores

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                in_place                (bool)  --  denotes whether it's an inplace restore or not
                    default: True for in place restores

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                restore_To_FileSystem   (bool)  --  denotes whether it's a restore to fs or not

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
                isinstance(overwrite, bool) and
                isinstance(in_place, bool) and
                isinstance(restore_To_FileSystem, bool)):

            raise SDKException('Subclient', '101')

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json_cloud = self._restore_json_cloud(
            paths=paths,
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            overwrite=overwrite,
            in_place=in_place,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=restore_To_FileSystem)

        return self._process_restore_response(request_json_cloud)
