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

"""
File for operating on a Informix Instance.

InformixInstance is the only class defined in this file.

InformixInstance: Derived class from Instance Base class, representing an
                    Informix instance, and to perform operations on that instance

InformixInstance:
=================

    __init__()                          -- initialize object of the Instances class

    _get_instance_properties()          -- gets the properties of this instance

    _get_instance_properties_json()     -- gets all the instance related properties
    of Informix instance

    _restore_json()                     -- returns the JSON request to pass to the API as
    per the options selected by the user

    restore_in_place()                  -- restores the informix data/log files specified in
    the input paths list to the same location

    restore_out_of_place()              -- restores the informix data/log files specified in
    the input paths list to the different location

    _restore_informix_option_json()     -- setter for the Informix option in restore JSON

    _restore_destination_option_json()  -- setter for  the destination restore option
    in restore JSON


InformixInstance instance Attributes
------------------------------------

    **informix_directory**          --  returns the informix directory path of informix server

    **informix_user**               --  returns the informix username

    **credentials**                 --  returns instance credentials

    **on_config_file**              --  returns the on config file name of informix server

    **sql_host_file**               --  returns the sql host file path of informix server

    **log_storage_policy_name**     --  returns the log backup storage policy name

    **log_storage_policy_id**       --  returns the log backup storage policy id

    **command_line_sp_name**        --  returns command line storage policy name

    **command_line_sp_id**          --  returns command line storage policy id

"""

from __future__ import unicode_literals

from ..instance import Instance
from ..exception import SDKException

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent
    from ..job import Job


class InformixInstance(Instance):
    """
    Represents a standalone Informix database instance within a managed environment.

    This class provides comprehensive management and configuration capabilities for Informix instances,
    including access to instance properties, configuration files, user credentials, and storage policies.
    It supports both in-place and out-of-place restore operations, allowing flexible recovery options.
    The class exposes several properties for accessing key Informix configuration details and storage policy information.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Access to Informix directory, user, credentials, ONCONFIG file, and SQLHOSTS file via properties
        - Retrieval and management of log storage policy and command line storage policy (name and ID)
        - Internal methods for fetching instance properties and generating JSON representations
        - Restore operations:
            - In-place restore with customizable options (path, restore type, copy precedence, physical/logical restore, time-based restore)
            - Out-of-place restore to different client or instance
        - Generation of restore option JSON for Informix and destination settings

    #ai-gen-doc
    """

    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int) -> None:
        """Initialize an InformixInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Informix instance.
            instance_name: The name of the Informix instance.
            instance_id: The unique identifier for the Informix instance.

        #ai-gen-doc
        """
        self._instance = None
        self._destination_restore_json = None
        self.informix_restore_json = None
        self._informix_instance = None
        super(InformixInstance, self).__init__(agent_object, instance_name, instance_id)

    @property
    def informix_directory(self) -> str:
        """Get the Informix directory path of the Informix server.

        Returns:
            The directory path as a string where the Informix server is installed.

        #ai-gen-doc
        """
        return self._properties['informixInstance'].get('informixDir', None)

    @property
    def informix_user(self) -> str:
        """Get the Informix database username associated with this instance.

        Returns:
            The Informix username as a string.

        #ai-gen-doc
        """

        # windows instance will have credentials associated with it, linux will just have username in instance prop
        if self.credentials:
            return self._commcell_object.credentials.get(self.credentials)._credential_properties.get("userName")

        return self._properties['informixInstance']['informixUser'].get('userName', None)

    @property
    def credentials(self) -> str:
        """Get the name of the credential associated with the Informix instance.

        Returns:
            The name of the credential as a string.

        #ai-gen-doc
        """
        return self._properties[
            'informixInstance']['informixUser'].get('savedCredential', {}).get('credentialName', None)

    @property
    def on_config_file(self) -> str:
        """Get the ONCONFIG file name for the Informix server instance.

        Returns:
            The name of the ONCONFIG configuration file as a string.

        #ai-gen-doc
        """
        return self._properties['informixInstance'].get('onConfigFile', None)

    @property
    def sql_host_file(self) -> str:
        """Get the SQL host file path of the Informix server.

        Returns:
            The file system path to the SQL host file used by the Informix server.

        #ai-gen-doc
        """
        return self._properties['informixInstance'].get('sqlHostfile', None)

    @property
    def log_storage_policy_name(self) -> str:
        """Get the name of the storage policy used for log backups.

        Returns:
            The name of the log backup storage policy as a string.

        #ai-gen-doc
        """
        return self._properties['informixInstance']['informixStorageDevice'][
            'logBackupStoragePolicy'].get('storagePolicyName', None)

    @log_storage_policy_name.setter
    def log_storage_policy_name(self, storage_policy: str) -> None:
        """Set the log storage policy name for the Informix instance.

        Args:
            storage_policy: The name of the storage policy to be set for Informix instance logs.

        #ai-gen-doc
        """
        content = self._informix_instance['informixStorageDevice']
        content['logBackupStoragePolicy'] = {
            'storagePolicyName': storage_policy
        }
        content = {
            'informixStorageDevice': content
        }
        self._set_instance_properties('_informix_instance', content)

    @property
    def log_storage_policy_id(self) -> int:
        """Get the storage policy ID used for Informix log backups.

        Returns:
            The integer ID of the storage policy assigned for log backups.

        #ai-gen-doc
        """
        return self._properties['informixInstance']['informixStorageDevice'][
            'logBackupStoragePolicy'].get('storagePolicyId', None)

    @property
    def command_line_sp_name(self) -> str:
        """Get the name of the command line storage policy associated with this Informix instance.

        Returns:
            The storage policy name as a string.

        #ai-gen-doc
        """
        return self._properties['informixInstance']['informixStorageDevice'][
            'commandLineStoragePolicy'].get('storagePolicyName', None)

    @command_line_sp_name.setter
    def command_line_sp_name(self, storage_policy: str) -> None:
        """Set the storage policy name for the Informix instance command line.

        Args:
            storage_policy: The name of the storage policy to assign to the Informix instance.

        #ai-gen-doc
        """
        content = self._informix_instance['informixStorageDevice']
        content['commandLineStoragePolicy'] = {
            'storagePolicyName': storage_policy
        }
        content = {
            'informixStorageDevice': content
        }
        self._set_instance_properties('_informix_instance', content)

    @property
    def command_line_sp_id(self) -> int:
        """Get the storage policy ID used for command line operations in the Informix instance.

        Returns:
            The storage policy ID as an integer.

        #ai-gen-doc
        """
        return self._properties['informixInstance']['informixStorageDevice'][
            'commandLineStoragePolicy'].get('storagePolicyId', None)

    def _get_instance_properties(self) -> None:
        """Retrieve and update the properties of the current Informix instance.

        This method fetches the latest properties for the Informix instance from the Commcell server.
        It updates the instance's internal state with the retrieved properties.

        Raises:
            SDKException: If the response from the server is empty or indicates a failure.

        #ai-gen-doc
        """
        super(InformixInstance, self)._get_instance_properties()
        self._informix_instance = self._properties['informixInstance']

    def _get_instance_properties_json(self) -> dict:
        """Retrieve all properties related to the Informix instance as a dictionary.

        Returns:
            dict: A dictionary containing all instance properties for the Informix instance.

        #ai-gen-doc
        """
        instance_json = {
            "instanceProperties":
                {
                    "instance": self._instance,
                    "informixInstance": self._informix_instance
                }
        }
        return instance_json

    def _restore_json(self, **kwargs) -> dict:
        """Generate the JSON request payload for the restore API based on user-selected options.

        This method constructs a dictionary representing the JSON request body required by the API,
        using the provided keyword arguments to specify restore options.

        Args:
            **kwargs: Arbitrary keyword arguments representing restore options and their values.

        Returns:
            dict: The JSON request dictionary to be sent to the API.

        #ai-gen-doc
        """
        rest_json = super(InformixInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        self._restore_informix_option_json(restore_option)
        if restore_option.get('out_of_place'):
            self._restore_destination_option_json(restore_option)
            rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "destination"] = self._destination_restore_json
        rest_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "informixOption"] = self.informix_restore_json
        return rest_json

    def restore_in_place(
        self,
        path: list,
        restore_type: str = "ENTIRE INSTANCE",
        copy_precedence: int = None,
        physical_restore: bool = True,
        logical_restore: bool = True,
        restore_option_type: str = "NORMAL",
        to_time: str = None,
        upto_log: int = None
    ) -> 'Job':
        """Restore Informix data or log files in-place to their original locations.

        This method initiates an in-place restore operation for the specified Informix dbspaces or log files.
        You can perform a full instance restore, a point-in-time restore, or restore up to a specific logical log.

        Args:
            path: List of dbspaces (as strings) to be restored.
            restore_type: Type of restore operation. Common values include "ENTIRE INSTANCE" or "WHOLE SYSTEM".
            copy_precedence: Optional copy precedence associated with the storage policy.
            physical_restore: If True, performs a physical restore.
            logical_restore: If True, performs a logical restore.
            restore_option_type: Restore option type. Accepted values are "NORMAL", "POINT_IN_TIME", or "UPTO_LOGICAL_LOG".
            to_time: Optional point-in-time (format: "YYYY-MM-DD HH:MM:SS") for point-in-time restore.
            upto_log: Optional logical log number to restore up to.

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If the path is not a list, if the job fails to initialize, if the response is empty, or if the response is not successful.

        Example:
            >>> dbspaces = ['rootdbs', 'datadbs']
            >>> job = informix_instance.restore_in_place(
            ...     path=dbspaces,
            ...     restore_type="ENTIRE INSTANCE",
            ...     physical_restore=True,
            ...     logical_restore=True
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not isinstance(path, list):
            raise SDKException('Instance', '101')

        if not path:
            raise SDKException('Instance', '104')

        restore_types_dict = {
            "ENTIRE INSTANCE":1,
            "WHOLE SYSTEM":2
        }

        restore_option_type_dict = {
            "NORMAL": 0,
            "POINT_IN_TIME": 1,
            "UPTO_LOGICAL_LOG": 2
        }

        request_json = self._restore_json(
            paths=path,
            restore_type=restore_types_dict[restore_type.upper()],
            copy_precedence=copy_precedence,
            physical_restore=physical_restore,
            logical_restore=logical_restore,
            restore_option_type=restore_option_type_dict[restore_option_type.upper()],
            to_time=to_time,
            upto_log=upto_log)
        return self._process_restore_response(request_json)

    def restore_out_of_place(
        self,
        path: list,
        dest_client_name: str,
        dest_instance_name: str,
        restore_type: str = "ENTIRE INSTANCE",
        copy_precedence: int = None,
        physical_restore: bool = True,
        logical_restore: bool = True
    ) -> 'Job':
        """Restore Informix data or log files to a different client or instance (out-of-place restore).

        This method initiates an out-of-place restore operation for the specified Informix dbspaces,
        allowing you to restore data to a different client and/or instance. You can control the type
        of restore (physical/logical), specify copy precedence, and select the restore type.

        Args:
            path: List of dbspaces to be restored.
            dest_client_name: Name of the destination client where data will be restored.
            dest_instance_name: Name of the destination Informix instance.
            restore_type: Type of restore operation. Common values are "ENTIRE INSTANCE" or "WHOLE SYSTEM".
            copy_precedence: Optional; copy precedence associated with the storage policy.
            physical_restore: Whether to perform a physical restore (default is True).
            logical_restore: Whether to perform a logical restore (default is True).

        Returns:
            Job: An instance of the Job class representing the restore job.

        Raises:
            SDKException: If `path` is not a list, if the job fails to initialize, or if the restore response is empty or unsuccessful.

        Example:
            >>> dbspaces = ['dbspace1', 'dbspace2']
            >>> job = informix_instance.restore_out_of_place(
            ...     path=dbspaces,
            ...     dest_client_name='DestinationClient',
            ...     dest_instance_name='DestInstance',
            ...     restore_type='ENTIRE INSTANCE',
            ...     copy_precedence=1,
            ...     physical_restore=True,
            ...     logical_restore=False
            ... )
            >>> print(f"Restore job started with ID: {job.job_id}")

        #ai-gen-doc
        """
        if not isinstance(path, list):
            raise SDKException('Instance', '101')

        if not path:
            raise SDKException('Instance', '104')

        restore_types_dict = {
            "ENTIRE INSTANCE": 1,
            "WHOLE SYSTEM": 2
        }

        request_json = self._restore_json(
            paths=path,
            restore_type=restore_types_dict[restore_type.upper()],
            copy_precedence=copy_precedence,
            physical_restore=physical_restore,
            logical_restore=logical_restore,
            dest_client_name=dest_client_name,
            dest_instance_name=dest_instance_name,
            out_of_place=True)
        return self._process_restore_response(request_json)

    def _restore_informix_option_json(self, value: dict) -> None:
        """Set the Informix-specific options in the restore JSON configuration.

        Args:
            value: A dictionary containing Informix restore options to be set in the restore JSON.

        #ai-gen-doc
        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')
        restore_time_dict = {}
        if value.get('to_time'):
            restore_time_dict['timeValue'] = value.get('to_time')
        last_log_number = 0
        if value.get('upto_log'):
            last_log_number = value.get('upto_log')
        self.informix_restore_json = {
            "restoreOnConfigFile": True,
            "informixRestoreOptionType": value.get("restore_option_type", 0),
            "numRestoreStreams": 2,
            "restoreEmergencyBootFile": True,
            "informixRestoreType": value.get("restore_type", ""),
            "logicalLogNumber": last_log_number,
            "physical": value.get("physical_restore", ""),
            "logical": value.get("logical_restore", ""),
            "restoreTime": restore_time_dict,
            "timeZone": {
                "TimeZoneName": "(UTC) Coordinated Universal Time"
            }
        }

    def _restore_destination_option_json(self, value: dict) -> None:
        """Set the destination restore option in the restore JSON configuration.

        Args:
            value: A dictionary containing the destination restore options to be set in the restore JSON.

        #ai-gen-doc
        """
        instance_id = ""
        if value.get("dest_client_name") and value.get("dest_instance_name"):
            instance_id = self._commcell_object.clients.get(
                value.get("dest_client_name")).agents.get(
                    'informix').instances.all_instances[value.get("dest_instance_name")]
        if not isinstance(value, dict):
            raise SDKException('Instance', '101')
        self._destination_restore_json = {
            "destClient": {
                "clientName": value.get("dest_client_name", ""),
            },
            "destinationInstance": {
                "instanceName": value.get("dest_instance_name", ""),
                "instanceId": int(instance_id)
            }
        }
