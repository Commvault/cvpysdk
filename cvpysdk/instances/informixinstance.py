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


class InformixInstance(Instance):
    """
    Class to represent a standalone Informix Instance
    """

    def __init__(self, agent_object, instance_name, instance_id):
        """Initialize object of the Instances class.

            Args:
                agent_object (object)  --  instance of the Agent class

                instance_name          --   Name of the instance

                instance_id            --   ID of the instance

            Returns:
                object - instance of the Instances class

        """
        self._instance = None
        self._destination_restore_json = None
        self.informix_restore_json = None
        self._informix_instance = None
        super(InformixInstance, self).__init__(agent_object, instance_name, instance_id)

    @property
    def informix_directory(self):
        """ Returns the informix directory path of informix server """
        return self._properties['informixInstance'].get('informixDir', None)

    @property
    def informix_user(self):
        """ Returns the informix username """
        return self._properties['informixInstance']['informixUser'].get('userName', None)

    @property
    def on_config_file(self):
        """ Returns the on config file name of informix server. """
        return self._properties['informixInstance'].get('onConfigFile', None)

    @property
    def sql_host_file(self):
        """ Returns the sql host file path of informix server. """
        return self._properties['informixInstance'].get('sqlHostfile', None)

    @property
    def log_storage_policy_name(self):
        """ Returns the log backup storage policy name """
        return self._properties['informixInstance']['informixStorageDevice'][
            'logBackupStoragePolicy'].get('storagePolicyName', None)

    @log_storage_policy_name.setter
    def log_storage_policy_name(self, storage_policy):
        """ Setter for informix instance log_storage_policy name

            Args:

                storage_policy (str)  -- storage_policy_name

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
    def log_storage_policy_id(self):
        """ Returns the log backup storage policy id """
        return self._properties['informixInstance']['informixStorageDevice'][
            'logBackupStoragePolicy'].get('storagePolicyId', None)

    @property
    def command_line_sp_name(self):
        """ Returns command line storage policy name """
        return self._properties['informixInstance']['informixStorageDevice'][
            'commandLineStoragePolicy'].get('storagePolicyName', None)

    @command_line_sp_name.setter
    def command_line_sp_name(self, storage_policy):
        """ Setter for informix instance command_line_sp name

            Args:

                storage_policy (str)  -- storage_policy_name

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
    def command_line_sp_id(self):
        """ Returns command line storage policy id """
        return self._properties['informixInstance']['informixStorageDevice'][
            'commandLineStoragePolicy'].get('storagePolicyId', None)

    def _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(InformixInstance, self)._get_instance_properties()
        self._informix_instance = self._properties['informixInstance']

    def _get_instance_properties_json(self):
        """ Gets all the instance related properties of Informix instance.

           Returns:
                dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties":
                {
                    "instance": self._instance,
                    "informixInstance": self._informix_instance
                }
        }
        return instance_json

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the
        options selected by the user

            Args:
                kwargs   (list)  --  list of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API

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
            path,
            restore_type="ENTIRE INSTANCE",
            copy_precedence=None,
            physical_restore=True,
            logical_restore=True,
            restore_option_type="NORMAL",
            to_time=None,
            upto_log=None):
        """Restores the informix data/log files specified in the input\
                paths list to the same location.

            Args:

                path                (list)  --  List of dbspaces to be restored

                restore_type        (str)   --  Restore type for informix instance

                copy_precedence     (int)   --  Copy precedence associted with storage
                policy

                physical_restore    (bool)  --  Physical restore flag

                logical_restore     (bool)  --  Logical restore flag

                    Accepted Values:

                        ENTIRE INSTANCE/WHOLE SYSTEM

                restore_option_type (str)   -- Restore option type for Informix instance

                    Accepted values:

                        NORMAL/POINT_IN_TIME/UPTO_LOGICAL_LOG

                to_time             (str)   -- time range to perform point in time restore

                    Accepted Format:

                        YYYY-MM-DD HH:MM:SS

                upto_log            (int)   -- logical log number to perform restore
                upto that log

            Returns:

                object - instance of the Job class for this restore job

            Raises:

                SDKException:

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        if not isinstance(path, list):
            raise SDKException('Instance', '101')

        if path == []:
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
            path,
            dest_client_name,
            dest_instance_name,
            restore_type="ENTIRE INSTANCE",
            copy_precedence=None,
            physical_restore=True,
            logical_restore=True):
        """Restores the informix data/log files specified in the input\
                paths list to the different location.

            Args:

                path                (list)  --  List of dbspaces to be restored

                dest_client_name    (str)   --  Name of the destination client

                dest_instance_name  (str)   --  name of destination instance

                restore_type        (str)   --  Restore type for informix instance

                copy_precedence     (int)   --  Copy precedence associted with storage
                policy

                physical_restore    (bool)  --  Physical restore flag

                logical_restore     (bool)  --  Logical restore flag

                    Accepted Values:

                        ENTIRE INSTANCE/WHOLE SYSTEM

            Returns:

                object - instance of the Job class for this restore job

            Raises:

                SDKException:

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        if not isinstance(path, list):
            raise SDKException('Instance', '101')

        if path == []:
            raise SDKException('Instance', '104')

        restore_types_dict = {
            "ENTIRE INSTANCE":1,
            "WHOLE SYSTEM":2
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

    def _restore_informix_option_json(self, value):
        """setter for the Informix option in restore JSON"""

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

    def _restore_destination_option_json(self, value):
        """setter for  the destination restore option in restore JSON"""
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
