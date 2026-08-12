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

"""Main file for performing subclient operations.

Subclients and Subclient are 2 classes defined in this file.

Subclients: Class for representing all the subclients associated with a backupset / instance

Subclient: Base class consisting of all the common properties and operations for a Subclient


Subclients:
===========
    __init__(class_object)      --  initialise object of subclients object associated with
    the specified backup set/instance.

    __str__()                   --  returns all the subclients associated with the backupset

    __repr__()                  --  returns the string for the instance of the Subclients class

    __len__()                   --  returns the number of subclients associated with the Agent
    for the selected Client

    __getitem__()               --  returns the name of the subclient for the given subclient Id
    or the details for the given subclient name

    _get_subclients()           --  gets all the subclients associated with the backupset specified

    _process_add_request()      --  to post the add client request

    default_subclient()         --  returns the name of the default subclient

    all_subclients()            --  returns dict of all the subclients on commcell

    has_subclient()             --  checks if a subclient exists with the given name or not

    add()                       --  adds a new subclient to the backupset

    add_oracle_logical_dump_subclient()  --  add subclient for oracle logical dump

    add_postgresql_subclient()  --  Adds a new postgresql subclient to the backupset.

     add_mysql_subclient()  --  Adds a new mysql subclient to the instance.

    add_virtual_server_subclient()  -- adds a new virtual server subclient to the backupset

    add_onedrive_subclient()   --  adds a new onedrive subclient to the instance

    get(subclient_name)         --  returns the subclient object of the input subclient name

    delete(subclient_name)      --  deletes the subclient (subclient name) from the backupset

    refresh()                   --  refresh the subclients associated with the Backupset / Instance


Subclient:
==========
    __init__()                  --  initialise instance of the Subclient class,
    associated to the specified backupset

    __getattr__()               --  provides access to restore helper methods

    __repr__()                  --  return the subclient name, the instance is associated with

    _get_subclient_id()         --  method to get subclient id, if not specified in __init__ method

    _get_subclient_properties() --  get the properties of this subclient

    _set_subclient_properties() --  sets the properties of this sub client .

    _process_backup_request()   --  runs the backup request provided, and processes the response

    _browse_and_find_json()     --  returns the appropriate JSON request to pass for either
    Browse operation or Find operation

    _process_browse_response()  --  processes response received for both Browse and Find request

    _common_backup_options()    --  Generates the advanced job options dict

    _json_task()                --  setter for task property

    _json_restore_subtask()     --  setter for sub task property

    _association_json()         --  setter for association property

    _get_preview_metadata()     --  gets the preview metadata for the file

    _get_preview()              --  gets the preview for the file
    browse_Cosmos_Content()     --  Browse Cosmos Account content to validate Backup Account exists
    _restore_atlas_option_json()--  Creates Restore JSON for atlas and runs restore

    update_atlas_instance()     --  Update Atlas subclient

    update_properties()         --  To update the subclient properties

    description()               --  update the description of the subclient

    content()                   --  update the content of the subclient

    enable_backup()             --  enables the backup for the subclient

    enable_trueup()             --  enables true up option for the subclient

    enable_trueup_days()        --  enables true up option and sets days for backup

    enable_backup_at_time()     --  enables backup for the subclient at the input time specified

    disable_backup()             --  disables the backup for the subclient

    set_proxy_for_snap()        --  method to set Use proxy option for intellisnap subclient

    unset_proxy_for_snap()      --  method to unset Use proxy option for intellisnap subclient

    set_proxy_for_backup_copy() --  method to set separate proxy server for backup copy for intelliSnap subclient

    unset_proxy_for_backup_copy() --  method to unset separate proxy server for backup copy for intelliSnap subclient

    backup()                    --  run a backup job for the subclient

    browse()                    --  gets the content of the backup for this subclient
    at the path specified

    browse_in_time()            --  gets the content of the backup for this subclient
    at the input path in the time range specified

    find()                      --  searches a given file/folder name in the subclient content

    list_media()                --  List media required to browse and restore backed up data from the backupset

    restore_in_place()          --  Restores the files/folders specified in the
    input paths list to the same location

    restore_out_of_place()      --  Restores the files/folders specified in the input paths list
    to the input client, at the specified destionation location

    set_backup_nodes()          -- Set Backup Nodes for NFS Share Pseudo client's subclient.

    find_latest_job()           --  Finds the latest job for the subclient
    which includes current running job also.

    run_content_indexing()      -- Runs CI for subclient

    refresh()                   --  refresh the properties of the subclient


Subclient Instance Attributes:
==============================

    **properties**                      --  returns the properties of the subclient

    **name**                            --  returns the name of the subclient

    **display_name**                    --  returns the display name of the subclient

    **description**                     --  returns the description of the subclient

    **snapshot_engine_name**            --  returns snapshot engine name associated
    with the subclient

    **is_default_subclient**            --  returns True if the subclient is default
    subclient else returns False

    **is_blocklevel_backup_enabled**    --  returns True if block level backup is enabled

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy
import math
import time
from typing import Any, Dict, List, Optional, Union

from .exception import SDKException
from .job import Job
from .job import JobController
from .schedules import SchedulePattern
from .schedules import Schedules
from .additional_settings import AdditionalSettings

class Subclients(object):
    """
    Manages and interacts with all subclients associated with a client.

    The Subclients class provides a comprehensive interface for managing subclients,
    including retrieval, addition, deletion, and inspection of subclient objects.
    It supports various subclient types such as Oracle Logical Dump, PostgreSQL,
    MySQL, Virtual Server, and OneDrive, allowing for flexible and extensible
    subclient management within a client context.

    Key Features:
        - Retrieve all subclients or a specific subclient by name
        - Add new subclients with detailed configuration options
        - Support for specialized subclient types (Oracle Logical Dump, PostgreSQL, MySQL, Virtual Server, OneDrive)
        - Delete existing subclients
        - Check for the existence of a subclient by name
        - Access the default subclient and all subclients via properties
        - Refresh the subclient list to reflect current state
        - Iterable and indexable interface for subclient collections
        - String representation and length support for easy inspection

    #ai-gen-doc
    """

    def __init__(self, class_object: object) -> None:
        """Initialize a Subclients object for the specified backupset context.

        Args:
            class_object: An instance of the Agent, Instance, or Backupset class that this Subclients object will be associated with.

        Raises:
            SDKException: If the provided class_object is not an instance of Agent, Instance, or Backupset.

        Example:
            >>> agent = Agent(commcell_object, "File System")
            >>> subclients = Subclients(agent)
            >>> print(type(subclients))
            <class 'Subclients'>

        #ai-gen-doc
        """
        from .agent import Agent
        from .instance import Instance
        from .backupset import Backupset

        self._agent_object = None
        self._instance_object = None
        self._backupset_object = None
        self._url_param = ''

        if isinstance(class_object, Agent):
            self._agent_object = class_object
            self._url_param += self._agent_object.agent_id

        elif isinstance(class_object, Instance):
            self._instance_object = class_object
            self._agent_object = self._instance_object._agent_object
            self._url_param += '{0}&instanceId={1}'.format(
                self._agent_object.agent_id, self._instance_object.instance_id
            )

        elif isinstance(class_object, Backupset):
            self._backupset_object = class_object
            self._instance_object = class_object._instance_object
            self._agent_object = self._instance_object._agent_object
            self._url_param += self._agent_object.agent_id
            self._url_param += '&backupsetId={0}'.format(
                self._backupset_object.backupset_id
            )
        else:
            raise SDKException('Subclient', '115')

        self._client_object = self._agent_object._client_object
        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._SUBCLIENTS = self._services['GET_ALL_SUBCLIENTS'] % (
            self._client_object.client_id, self._url_param
        )

        self._ADD_SUBCLIENT = self._services['ADD_SUBCLIENT']

        self._default_subclient = None

        # sql server subclient type dict
        self._sqlsubclient_type_dict = {
            'DATABASE': 1,
            'FILE_FILEGROUP': 2,
        }

        # this will work only for `Exchange Database` Agent, as only an object of
        # ExchangeDatabaseAgent class has these attributes
        if self._instance_object is None and hasattr(
                self._agent_object, '_instance_object'):
            self._instance_object = self._agent_object._instance_object

        if self._backupset_object is None and hasattr(
                self._agent_object, '_backupset_object'):
            self._backupset_object = self._agent_object._backupset_object

        self.refresh()

    def __str__(self) -> str:
        """Return a string representation of all subclients in the backupset.

        This method provides a human-readable summary listing all subclients 
        associated with the backupset for an agent of a client.

        Returns:
            A string containing the names or details of all subclients in the backupset.

        Example:
            >>> subclients = Subclients()
            >>> print(str(subclients))
            Subclient1
            Subclient2
            Subclient3

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Subclient', 'Backupset', 'Instance', 'Agent', 'Client'
        )

        for index, subclient in enumerate(self._subclients):
            sub_str = '{:^5}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\n'.format(
                index + 1,
                subclient.split('\\')[-1],
                self._subclients[subclient]['backupset'],
                self._instance_object.instance_name,
                self._agent_object.agent_name,
                self._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the Subclients instance.

        This method provides a developer-friendly string that represents the current
        Subclients object, useful for debugging and logging purposes.

        Returns:
            A string representation of the Subclients instance.

        Example:
            >>> subclients = Subclients()
            >>> print(repr(subclients))
            <Subclients object at 0x7f8b2c1d2e80>
        #ai-gen-doc
        """
        if self._backupset_object is not None:
            o_str = (
                'Subclients class instance for Backupset: "{0}", '
                'of Instance: "{1}", for Agent: "{2}"'
            ).format(
                self._backupset_object.backupset_name,
                self._instance_object.instance_name,
                self._agent_object.agent_name
            )
        elif self._instance_object is not None:
            o_str = 'Subclients class instance for Instance: "{0}", of Agent: "{1}"'.format(
                self._instance_object.instance_name,
                self._agent_object.agent_name
            )
        else:
            o_str = 'Subclients class instance for Agent: "{0}"'.format(
                self._agent_object.agent_name
            )

        return o_str

    def __len__(self) -> int:
        """Get the number of subclients associated with the Agent for the selected Client.

        Returns:
            The total count of subclients as an integer.

        Example:
            >>> subclients = Subclients()
            >>> count = len(subclients)
            >>> print(f"Number of subclients: {count}")
        #ai-gen-doc
        """
        return len(self.all_subclients)

    def __getitem__(self, value: 'Union[str, int]') -> 'Union[str, dict]':
        """Retrieve subclient information by name or ID.

        If a subclient ID (int) is provided, returns the name of the corresponding subclient.
        If a subclient name (str) is provided, returns a dictionary containing the subclient's details.

        Args:
            value: The name (str) or ID (int) of the subclient to retrieve.

        Returns:
            str: The name of the subclient if an ID was provided.
            dict: A dictionary of subclient details if a name was provided.

        Raises:
            IndexError: If no subclient exists with the given name or ID.

        Example:
            >>> subclients = Subclients()
            >>> # Get subclient details by name
            >>> details = subclients["DailyBackup"]
            >>> print(details)
            {'id': 5, 'name': 'DailyBackup', 'status': 'Active'}
            >>> # Get subclient name by ID
            >>> name = subclients[5]
            >>> print(name)
            'DailyBackup'

        #ai-gen-doc
        """
        value = str(value)

        if value in self.all_subclients:
            return self.all_subclients[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_subclients.items())
                )[0][0]
            except IndexError:
                raise IndexError('No subclient exists with the given Name / Id')

    def _get_subclients(self) -> dict:
        """Retrieve all subclients associated with the client specified by the backupset object.

        Returns:
            dict: A dictionary containing all subclients in the backupset. Each key is a subclient name,
            and the value is a dictionary with subclient details, such as ID and backupset.
            Example structure:
                {
                    "subclient1_name": {
                        "id": subclient1_id,
                        "backupset": backupset
                    },
                    "subclient2_name": {
                        "id": subclient2_id,
                        "backupset": backupset
                    }
                }

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        Example:
            >>> subclients = subclients_obj._get_subclients()
            >>> for name, details in subclients.items():
            ...     print(f"Subclient: {name}, ID: {details['id']}, Backupset: {details['backupset']}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._SUBCLIENTS)

        if flag:
            if response.json() and 'subClientProperties' in response.json():
                return_dict = {}

                for dictionary in response.json()['subClientProperties']:
                    # store the agent, instance, and backupset name for the current subclient
                    # the API call returns the subclients for all Agents, so we need to filter
                    # them out based on the Agent / Instance / Backupset that had been selected
                    # by the user earlier
                    agent = dictionary['subClientEntity']['appName'].lower()
                    instance = dictionary['subClientEntity']['instanceName'].lower(
                    )
                    backupset = dictionary['subClientEntity']['backupsetName'].lower(
                    )

                    # filter subclients for all entities: Agent, Instance, and Backupset
                    # as the instance of the Backupset class was passed for Subclients instance
                    # creation
                    if self._backupset_object is not None:
                        if (self._backupset_object.backupset_name in backupset and
                                self._instance_object.instance_name in instance and
                                self._agent_object.agent_name in agent):
                            temp_name = dictionary['subClientEntity']['subclientName'].lower(
                            )
                            temp_id = str(
                                dictionary['subClientEntity']['subclientId']).lower()

                            return_dict[temp_name] = {
                                "id": temp_id,
                                "backupset": backupset
                            }

                            if dictionary['commonProperties'].get(
                                    'isDefaultSubclient'):
                                self._default_subclient = temp_name

                    elif self._instance_object is not None:
                        if (self._instance_object.instance_name in instance and
                                self._agent_object.agent_name in agent):
                            temp_name = dictionary['subClientEntity']['subclientName'].lower(
                            )
                            temp_id = str(
                                dictionary['subClientEntity']['subclientId']).lower()

                            if len(
                                    self._instance_object.backupsets.all_backupsets) > 1:
                                temp_name = "{0}\\{1}".format(
                                    backupset, temp_name)

                            return_dict[temp_name] = {
                                "id": temp_id,
                                "backupset": backupset
                            }

                            if dictionary['commonProperties'].get(
                                    'isDefaultSubclient'):
                                self._default_subclient = temp_name

                    elif self._agent_object is not None:
                        if self._agent_object.agent_name in agent:
                            temp_name = dictionary['subClientEntity']['subclientName'].lower(
                            )
                            temp_id = str(
                                dictionary['subClientEntity']['subclientId']).lower()

                            if len(self._agent_object.instances.all_instances) > 1:
                                if len(
                                        self._instance_object.backupsets.all_backupsets) > 1:
                                    temp_name = "{0}\\{1}\\{2}".format(
                                        instance, backupset, temp_name
                                    )
                                else:
                                    temp_name = "{0}\\{1}".format(
                                        instance, temp_name)
                            else:
                                if len(
                                        self._instance_object.backupsets.all_backupsets) > 1:
                                    temp_name = "{0}\\{1}".format(
                                        backupset, temp_name)

                            return_dict[temp_name] = {
                                "id": temp_id,
                                "backupset": backupset
                            }

                            if dictionary['commonProperties'].get(
                                    'isDefaultSubclient'):
                                self._default_subclient = temp_name

                return return_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    @property
    def all_subclients(self) -> dict:
        """Get a dictionary of all subclients configured on this backupset.

        Returns:
            dict: A dictionary where each key is a subclient name and the value is a dictionary 
            containing the subclient's ID and associated backupset. The structure is as follows:

                {
                    "subclient1_name": {
                        "id": subclient1_id,
                        "backupset": backupset
                    },
                    "subclient2_name": {
                        "id": subclient2_id,
                        "backupset": backupset
                    }
                }

        Example:
            >>> subclients = Subclients(backupset_object)
            >>> all_subclients = subclients.all_subclients
            >>> for name, details in all_subclients.items():
            ...     print(f"Subclient: {name}, ID: {details['id']}, Backupset: {details['backupset']}")

        #ai-gen-doc
        """
        return self._subclients

    def has_subclient(self, subclient_name: str) -> bool:
        """Check if a subclient with the specified name exists in the Commcell.

        Args:
            subclient_name: The name of the subclient to check for existence.

        Returns:
            True if the subclient exists in the backupset, False otherwise.

        Raises:
            SDKException: If the type of the subclient_name argument is not a string.

        Example:
            >>> subclients = Subclients()
            >>> exists = subclients.has_subclient("default")
            >>> print(f"Subclient exists: {exists}")
            # Output: Subclient exists: True

        #ai-gen-doc
        """
        if not isinstance(subclient_name, str):
            raise SDKException('Subclient', '101')

        return self._subclients and subclient_name.lower() in self._subclients

    def _process_add_request(self, request_json: dict) -> 'Subclient':
        """Send a request to add a new subclient and return the resulting Subclient instance.

        Args:
            request_json: Dictionary containing the payload for the add subclient request.

        Returns:
            Subclient: An instance of the Subclient class representing the newly created subclient.

        Example:
            >>> subclients = Subclients()
            >>> payload = {
            ...     "subClientProperties": {
            ...         "subClientEntity": {
            ...             "clientName": "Client1",
            ...             "appName": "File System",
            ...             "instanceName": "DefaultInstanceName",
            ...             "backupsetName": "default"
            ...         },
            ...         "commonProperties": {
            ...             "description": "New subclient"
            ...         }
            ...     }
            ... }
            >>> new_subclient = subclients._process_add_request(payload)
            >>> print(f"Created subclient: {new_subclient}")

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._ADD_SUBCLIENT, request_json
        )

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Subclient',
                        '102',
                        'Failed to create subclient\nError: "{0}"'.format(error_string)
                    )
                else:
                    # initialize the subclients again so the subclient object has all the subclients
                    self.refresh()

                    subclient_name = request_json['subClientProperties']['subClientEntity']['subclientName']

                    return self.get(subclient_name)

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add(self, subclient_name: str, storage_policy: Optional[str] = None,
            subclient_type: Optional[str] = None, description: str = '',
            advanced_options: Optional[Dict[str, Any]] = None,
            pre_scan_cmd: Optional[str] = None) -> 'Subclient':
        """Add a new subclient to the backupset.

        This method creates a new subclient with the specified name and optional properties,
        such as storage policy, subclient type, description, advanced options, and a pre-scan command.

        Args:
            subclient_name: Name of the new subclient to add.
            storage_policy: Name of the storage policy to associate with the subclient. Defaults to None.
            subclient_type: Type of subclient for SQL Server. Valid values are "DATABASE" or "FILE_FILEGROUP". Defaults to None.
            description: Optional description for the subclient. Defaults to an empty string.
            advanced_options: Dictionary of additional options for subclient creation. Example: {"ondemand_subclient": True}. Defaults to None.
            pre_scan_cmd: Path to a batch file or shell script to run before each backup of the subclient. Defaults to None.

        Returns:
            Subclient: An instance of the Subclient class representing the newly created subclient.

        Raises:
            SDKException: If any of the following conditions occur:
                - subclient_name, storage_policy, or description is not of type string
                - Failed to create subclient
                - Response is empty or not successful
                - Subclient already exists with the given name

        Example:
            >>> subclients = Subclients(backupset_object)
            >>> new_subclient = subclients.add(
            ...     subclient_name="FinanceDB",
            ...     storage_policy="DailyBackupPolicy",
            ...     subclient_type="DATABASE",
            ...     description="Finance database backups",
            ...     advanced_options={"ondemand_subclient": True},
            ...     pre_scan_cmd="/scripts/pre_backup.sh"
            ... )
            >>> print(f"Created subclient: {new_subclient}")

        #ai-gen-doc
        """
        if not (isinstance(subclient_name, str) and
                isinstance(description, str)):
            raise SDKException('Subclient', '101')

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(
                    subclient_name)
            )

        if self._backupset_object is None:
            if self._instance_object.backupsets.has_backupset(
                    'defaultBackupSet'):
                self._backupset_object = self._instance_object.backupsets.get(
                    'defaultBackupSet')
            else:
                self._backupset_object = self._instance_object.backupsets.get(
                    sorted(self._instance_object.backupsets.all_backupsets)[0]
                )

        if storage_policy and not self._commcell_object.storage_policies.has_policy(
                storage_policy):
            raise SDKException(
                'Subclient',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    storage_policy)
            )

        if advanced_options:
            if advanced_options.get("ondemand_subclient", False):
                ondemand_value = advanced_options.get("ondemand_subclient")
            else:
                ondemand_value = False
        else:
            ondemand_value = False

        request_json = {
            "subClientProperties": {
                "contentOperationType": 2,
                "subClientEntity": {
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": subclient_name
                },
                "commonProperties": {
                    "description": description,
                    "enableBackup": True,
                    "onDemandSubClient": ondemand_value,
                    "storageDevice": {
                        "dataBackupStoragePolicy": {
                            "storagePolicyName": storage_policy
                        }
                    },
                }
            }
        }

        if storage_policy is None:
            del request_json["subClientProperties"]["commonProperties"]["storageDevice"]

        if pre_scan_cmd is not None:
            request_json["subClientProperties"]["commonProperties"]["prepostProcess"] = {
                "runAs": 1,
                "preScanCommand": pre_scan_cmd
            }

        if self._agent_object.agent_name == 'sql server':
            request_json['subClientProperties']['mssqlSubClientProp'] = {
                'sqlSubclientType': self._sqlsubclient_type_dict[subclient_type]
            }

        return self._process_add_request(request_json)

    def add_oracle_logical_dump_subclient(
            self,
            subclient_name: str,
            storage_policy: str,
            dump_dir: str,
            full_mode: bool,
            credential_name: str = "",
            schema_value: Optional[list] = None
        ) -> 'Subclient':
        """Add a subclient for Oracle logical dump backup.

        This method creates a subclient for Oracle logical dump in either full mode or schema mode:
        - For full mode: set `full_mode` to True and leave `schema_value` as None.
        - For schema mode: set `full_mode` to False and provide a list of schema names in `schema_value`.

        Args:
            subclient_name: Name of the subclient for logical dump.
            storage_policy: Storage policy to associate with the subclient.
            dump_dir: Directory path where dumps will be stored.
            full_mode: If True, creates a subclient in full mode; if False, creates in schema mode.
            credential_name: Name of the saved credential in the Commvault credential store for the Oracle database connection.
            schema_value: List of schema names for schema mode subclient. Should be None for full mode.

        Returns:
            Subclient: An instance of the Subclient class representing the newly created subclient.

        Raises:
            SDKException: If any of the following conditions occur:
                - subclient_name is not a string
                - storage_policy is not a string
                - subclient_name already exists
                - storage_policy does not exist

        Example:
            >>> # Create a full mode Oracle logical dump subclient
            >>> subclient = subclients.add_oracle_logical_dump_subclient(
            ...     subclient_name="FullDumpSubclient",
            ...     storage_policy="OracleStoragePolicy",
            ...     dump_dir="/oracle/dumps",
            ...     full_mode=True,
            ...     credential_name="oracle-cred"
            ... )
            >>> print(f"Created subclient: {subclient}")

            >>> # Create a schema mode Oracle logical dump subclient
            >>> subclient = subclients.add_oracle_logical_dump_subclient(
            ...     subclient_name="SchemaDumpSubclient",
            ...     storage_policy="OracleStoragePolicy",
            ...     dump_dir="/oracle/dumps",
            ...     full_mode=False,
            ...     credential_name="oracle-cred",
            ...     schema_value=["HR", "FINANCE"]
            ... )
            >>> print(f"Created schema mode subclient: {subclient}")

        #ai-gen-doc
        """
        if not (isinstance(subclient_name, str) and
                isinstance(storage_policy, str) and
                isinstance(dump_dir, str) and
                isinstance(full_mode, bool)):
            raise SDKException('Subclient', '101')
        if (full_mode == False and not
        isinstance(schema_value, list)):
            raise SDKException('Subclient', '101')

        credential_id = self._commcell_object.credentials.get(credential_name).credential_id

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(
                    subclient_name)
            )

        if self._backupset_object is None:
            if self._instance_object.backupsets.has_backupset(
                    'defaultBackupSet'):
                self._backupset_object = self._instance_object.backupsets.get(
                    'defaultBackupSet')
            else:
                self._backupset_object = self._instance_object.backupsets.get(
                    sorted(self._instance_object.backupsets.all_backupsets)[0]
                )

        if not self._commcell_object.storage_policies.has_policy(
                storage_policy):
            raise SDKException(
                'Subclient',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    storage_policy)
            )

        request_json = {
            "subClientProperties": {
                "subClientEntity": {
                    "clientName": self._client_object.client_name,
                    "instanceName": self._instance_object.instance_name,
                    "appName": self._agent_object.agent_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": subclient_name
                },
                "oracleSubclientProp": {
                    "data": False,
                    "archiveDelete": False,
                    "useSQLConntect": False,
                    "dbSubclientType": 2,
                    "mergeIncImageCopies": False,
                    "selectiveOnlineFull": False,
                    "protectBackupRecoveryArea": False,
                    "selectArchiveLogDestForBackup": False,
                    "backupSPFile": False,
                    "backupControlFile": False,
                    "backupArchiveLog": False,
                    "validate": False,
                },
                "commonProperties": {
                    "snapCopyInfo": {
                        "useSeparateProxyForSnapToTape": False,
                        "checkProxyForSQLIntegrity": False,
                        "snapToTapeProxyToUseSource": False,
                        "isSnapBackupEnabled": False,
                        "IsOracleSposDriverEnabled": False,
                        "isRMANEnableForTapeMovement": False
                    },
                    "dbDumpConfig": {
                        "fullMode": True,
                        "database": "",
                        "dumpDir": dump_dir,
                        "parallelism": 2,
                        "overrideInstanceUser": True,
                        "dbConnectCredential": {
                            "credentialId": credential_id,
                            "credentialName": credential_name
                        }
                    },
                    "storageDevice": {
                        "dataBackupStoragePolicy": {
                            "storagePolicyName": storage_policy
                        },
                        "deDuplicationOptions": {
                            "enableDeduplication": True
                        }
                    }
                }
            }
        }

        if (full_mode == False):
            request_json["subClientProperties"]["commonProperties"]["dbDumpConfig"]["fullMode"] = False
            request_json["subClientProperties"]["commonProperties"]["dbDumpConfig"]["schema"] = schema_value

        return self._process_add_request(request_json)

    def add_postgresql_subclient(
            self,
            subclient_name: str,
            storage_policy: str,
            contents: list,
            no_of_streams: int = 1,
            collect_object_list: bool = False
        ) -> 'Subclient':
        """Add a new PostgreSQL subclient to the backup set.

        This method creates a new PostgreSQL subclient with the specified name, associates it with a storage policy,
        and assigns the provided list of databases as its content. You can also specify the number of backup streams
        and whether to enable the collection of the object list for the subclient.

        Args:
            subclient_name: Name of the new subclient to add.
            storage_policy: Name of the storage policy to associate with the subclient.
            contents: List of databases to be included as subclient content.
            no_of_streams: Number of backup streams to use. Defaults to 1.
            collect_object_list: Whether to enable collection of the object list for the subclient. Defaults to False.

        Returns:
            Subclient: An instance of the created Subclient.

        Raises:
            SDKException: If any of the following conditions occur:
                - subclient_name is not a string
                - storage_policy is not a string
                - contents is not a list or is an empty list
                - Failed to create the subclient
                - Response is empty or not successful
                - A subclient with the given name already exists

        Example:
            >>> subclients = Subclients(backupset_object)
            >>> db_list = ['postgres', 'mydb']
            >>> subclient = subclients.add_postgresql_subclient(
            ...     subclient_name='FinanceDBs',
            ...     storage_policy='GoldPolicy',
            ...     contents=db_list,
            ...     no_of_streams=2,
            ...     collect_object_list=True
            ... )
            >>> print(f"Created subclient: {subclient}")

        #ai-gen-doc
        """
        if not (isinstance(subclient_name, str) and
                isinstance(storage_policy, str) and
                isinstance(contents, list)):
            raise SDKException('Subclient', '101')

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(
                    subclient_name)
            )

        if not self._commcell_object.storage_policies.has_policy(
                storage_policy):
            raise SDKException(
                'Subclient',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    storage_policy)
            )

        if not contents:
            raise SDKException(
                'Subclient',
                '102',
                'Content list cannot be empty'
            )

        content_list = []
        for content in contents:
            content_list.append({"postgreSQLContent": {"databaseName": content}})

        request_json = {
            "subClientProperties": {
                "contentOperationType": 2,
                "subClientEntity": {
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": subclient_name
                },
                "commonProperties": {
                    "storageDevice": {
                        "dataBackupStoragePolicy": {
                            "storagePolicyName": storage_policy
                        }
                    },
                },
                "postgreSQLSubclientProp": {
                    "numberOfBackupStreams": no_of_streams,
                    "collectObjectListDuringBackup": collect_object_list
                },
                "content": content_list
            }
        }

        return self._process_add_request(request_json)

    def add_mysql_subclient(
            self,
            subclient_name: str,
            storage_policy: str,
            contents: list,
            **kwargs: dict
    ) -> 'Subclient':
        """Add a new MySQL subclient to the instance.

        This method creates a new MySQL subclient with the specified name, associates it with a storage policy,
        and sets the provided database list as its content. Additional configuration options can be provided
        via keyword arguments.

        Args:
            subclient_name: Name of the new subclient to add.
            storage_policy: Name of the storage policy to associate with the subclient.
            contents: List of databases to be included as subclient content.
            **kwargs: Optional keyword arguments for advanced configuration:
                - no_of_backup_streams (int): Number of backup streams to use (default: 1).
                - no_of_log_backup_streams (int): Number of transaction log backup streams (default: 1).
                - full_instance_xtrabackup (bool): Set to True to use XtraBackup for the subclient (default: False).

        Returns:
            Subclient: An instance of the Subclient class representing the newly created MySQL subclient.

        Raises:
            SDKException: If any of the following conditions occur:
                - subclient_name is not a string
                - storage_policy is not a string
                - contents is not a list or is an empty list
                - Failed to create the subclient
                - Response is empty or not successful
                - A subclient with the given name already exists

        Example:
            >>> subclients = Subclients(instance_object)
            >>> mysql_subclient = subclients.add_mysql_subclient(
            ...     subclient_name="MySQL_DB_Backup",
            ...     storage_policy="GoldPolicy",
            ...     contents=["db1", "db2"],
            ...     no_of_backup_streams=2,
            ...     full_instance_xtrabackup=True
            ... )
            >>> print(f"Created subclient: {mysql_subclient}")

        #ai-gen-doc
        """
        if not (isinstance(subclient_name, str) and
                isinstance(storage_policy, str) and
                isinstance(contents, list)):
            raise SDKException('Subclient', '101')

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(
                    subclient_name)
            )

        if not self._commcell_object.storage_policies.has_policy(
                storage_policy):
            raise SDKException(
                'Subclient',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(
                    storage_policy)
            )

        if not contents:
            raise SDKException(
                'Subclient',
                '102',
                'Content list cannot be empty'
            )

        content_list = []
        for content in contents:
            content_list.append({"mySQLContent": {"databaseName": content}})

        request_json = {
            "subClientProperties": {
                "contentOperationType": 2,
                "subClientEntity": {
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": "defaultDummyBackupSet",
                    "subclientName": subclient_name
                },
                "commonProperties": {
                    "storageDevice": {
                        "dataBackupStoragePolicy": {
                            "storagePolicyName": storage_policy
                        }
                    },
                },
                "mySqlSubclientProp": {
                    "numberOfBackupStreams": kwargs.get('no_of_backup_streams', 1),
                    "numberOfTransactionLogStreams": kwargs.get('no_of_log_backup_streams', 1),
                    "fullInstanceXtraBackup": kwargs.get('full_instance_xtrabackup', False)
                },
                "content": content_list
            }
        }

        return self._process_add_request(request_json)

    def add_virtual_server_subclient(
            self,
            subclient_name: str,
            subclient_content: list,
            **kwargs: dict
    ) -> 'Subclient':
        """Add a new virtual server subclient to the backupset.

        This method creates a new virtual server subclient with the specified name and content.
        Additional options such as plan, storage policy, and description can be provided as keyword arguments.

        Args:
            subclient_name: The name of the subclient to be created.
            subclient_content: A list defining the content to be added to the subclient. The structure should use
                VSAObjects Enum values for the 'type' field. See examples below for typical usage.
            **kwargs: Optional keyword arguments:
                - plan_name (str): Plan to associate with the subclient.
                - storage_policy (str): Storage policy to associate with the subclient.
                - description (str): Description for the subclient (default: '').

        Returns:
            Subclient: An instance of the created Subclient.

        Raises:
            SDKException: If any of the following occur:
                - subclient_name is not a string
                - storage_policy is not a string
                - description is not a string
                - failed to create subclient
                - response is empty or not successful
                - a subclient with the given name already exists

        Example:
            >>> subclient_content = [{
            ...     'equal_value': True,
            ...     'allOrAnyChildren': True,
            ...     'id': '',
            ...     'path': '',
            ...     'display_name': 'sample1',
            ...     'type': VSAObjects.VMName
            ... }]
            >>> subclient = subclients.add_virtual_server_subclient(
            ...     subclient_name="MyVMSubclient",
            ...     subclient_content=subclient_content,
            ...     storage_policy="GoldPolicy",
            ...     description="Subclient for VM backups"
            ... )
            >>> print(f"Created subclient: {subclient}")

        #ai-gen-doc
        """
        if not (isinstance(subclient_name, str) and
                isinstance(subclient_content, list)):
            raise SDKException('Subclient', '101')

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(
                    subclient_name)
            )

        if self._backupset_object is None:
            if self._instance_object.backupsets.has_backupset(
                    'defaultBackupSet'):
                self._backupset_object = self._instance_object.backupsets.get(
                    'defaultBackupSet')
            else:
                self._backupset_object = self._instance_object.backupsets.get(
                    sorted(self._instance_object.backupsets.all_backupsets)[0]
                )

        content = []

        def set_content(item_content):
            """
            create content dictionary
            Args:
                item_content            (dict):     Dict of content details

                Example:
                    {
                        'equal_value': True,
                        'allOrAnyChildren': True,
                        'display_name': 'sample1',
                        'type':  < VSAObjects.VMName: 10 >
                    }

            Returns:

            """
            return {
                "equalsOrNotEquals": item_content.get('equal_value', True),
                "name": item_content.get('id', ''),
                "displayName": item_content.get('display_name', ''),
                "path": item_content.get('path', ''),
                "allOrAnyChildren": item.get('allOrAnyChildren', True),
                "type": item_content['type'] if isinstance(item_content['type'], int) else item_content['type'].value
            }

        for item in subclient_content:
            _temp_list = []
            _temp_dict = {}
            allOrAnyChildren = item.get('allOrAnyChildren', None)
            if 'content' in item:
                nested_content = item['content']
                for each_condition in nested_content:
                    temp_dict = set_content(each_condition)
                    _temp_list.append(temp_dict)
                _temp_dict['allOrAnyChildren'] = allOrAnyChildren
                _temp_dict['children'] = _temp_list
                content.append(_temp_dict)
            else:
                temp_dict = set_content(item)
                content.append(temp_dict)

        request_json = {
            "subClientProperties": {
                "vmContentOperationType": 2,
                "vmContent": {
                    "children": content
                },
                "subClientEntity": {
                    "clientName": self._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": subclient_name
                },
                "commonProperties": {
                    "description": kwargs.get('description'),
                    "enableBackup": True
                }
            }
        }

        if kwargs.get("customSnapshotResourceGroup"):
            request_json["subClientProperties"]["vsaSubclientProp"] = \
                {"customSnapshotResourceGroup": kwargs.get("customSnapshotResourceGroup")}

        if kwargs.get('plan_name'):
            if not self._commcell_object.plans.has_plan(kwargs['plan_name']):
                raise SDKException(
                    'Subclient',
                    '102',
                    'Plan: "{0}" does not exist in the Commcell'.format(kwargs['plan_name'])
                )
            request_json['subClientProperties']['planEntity'] = {
                "planName": kwargs['plan_name']
            }

        elif kwargs.get('storage_policy'):
            if not self._commcell_object.storage_policies.has_policy(kwargs.get('storage_policy')):
                raise SDKException(
                    'Subclient',
                    '102',
                    'Storage Policy: "{0}" does not exist in the Commcell'.format(kwargs.get('storage_policy'))
                )
            request_json['subClientProperties']['commonProperties']['storageDevice'] = {
                "dataBackupStoragePolicy": {
                    "storagePolicyName": kwargs.get('storage_policy')
                }
            }
        else:
            raise SDKException('Subclient', '102', 'Either Plan or Storage policy should be given as input')

        return self._process_add_request(request_json)

    def add_onedrive_subclient(self, subclient_name: str, server_plan: str) -> 'Subclient':
        """Add a new OneDrive subclient to the backup set.

        Creates a new subclient with the specified name and associates it with the given server plan.

        Args:
            subclient_name: The name of the new subclient to add.
            server_plan: The name of the server plan to associate with the subclient.

        Returns:
            Subclient: An instance of the Subclient class representing the newly created subclient.

        Raises:
            SDKException: If any of the following conditions occur:
                - The subclient name is not a string.
                - The server plan is not a string.
                - Failed to create the subclient.
                - The response is empty or not successful.
                - A subclient with the given name already exists.
                - The specified server plan does not exist.

        Example:
            >>> subclients = Subclients(backupset_object)
            >>> new_subclient = subclients.add_onedrive_subclient("FinanceDept", "OneDriveServerPlan")
            >>> print(f"Created subclient: {new_subclient}")

        #ai-gen-doc
        """

        if not (isinstance(subclient_name, str) and
                isinstance(server_plan, str)):
            raise SDKException('Subclient', '101')

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(
                    subclient_name)
            )

        if self._backupset_object is None:
            if self._instance_object.backupsets.has_backupset(
                    self._instance_object.backupsets.default_backup_set):
                self._backupset_object = self._instance_object.backupsets.get(
                    self._instance_object.backupsets.default_backup_set)
            else:
                self._backupset_object = self._instance_object.backupsets.get(
                    sorted(self._instance_object.backupsets.all_backupsets)[0]
                )

        if self._commcell_object.plans.has_plan(server_plan):
            server_plan_object = self._commcell_object.plans.get(server_plan)
            server_plan_id = int(server_plan_object.plan_id)
        else:
            raise SDKException('Plan', '102', 'Provide Valid Plan Name')

        request_json = {
            "subClientProperties": {
                "subClientEntity": {
                    "clientName": self._client_object.client_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetId": int(self._backupset_object.backupset_id),
                    "instanceId": int(self._instance_object.instance_id),
                    "clientId": int(self._client_object.client_id),
                    "appName": self._agent_object.agent_name,
                    "applicationId": 134,
                    "subclientName": subclient_name
                },
                "planEntity": {
                    "planId": server_plan_id
                },
                "cloudAppsSubClientProp": {
                    "instanceType": 7,
                    "oneDriveSubclient": {
                        "enableOneNote": False,
                        "isEnterprise": True
                    }
                },
                "cloudconnectorSubclientProp": {
                    "isAutoDiscoveryEnabled": False
                },
                "commonProperties": {
                    "enableBackup": True
                }
            }
        }

        return self._process_add_request(request_json)

    def get(self, subclient_name: str) -> 'Subclient':
        """Retrieve a Subclient object by its name.

        Args:
            subclient_name: The name of the subclient to retrieve.

        Returns:
            Subclient: An instance of the Subclient class corresponding to the specified subclient name.

        Raises:
            SDKException: If the subclient_name is not a string or if no subclient exists with the given name.

        Example:
            >>> subclients = Subclients()
            >>> subclient = subclients.get("default")
            >>> print(f"Subclient name: {subclient.name}")

        #ai-gen-doc
        """
        if not isinstance(subclient_name, str):
            raise SDKException('Subclient', '101')
        else:
            subclient_name = subclient_name.lower()

            if self.has_subclient(subclient_name):

                if self._backupset_object is None:
                    self._backupset_object = self._instance_object.backupsets.get(
                        self._subclients[subclient_name]['backupset']
                    )
                return Subclient(
                    self._backupset_object, subclient_name, self._subclients[subclient_name]['id']
                )

            raise SDKException(
                'Subclient', '102', 'No subclient exists with name: {0}'.format(
                    subclient_name)
            )

    def delete(self, subclient_name: str) -> None:
        """Delete a subclient from the backupset by its name.

        Removes the specified subclient from the backupset. If the subclient does not exist,
        or if the deletion fails, an SDKException is raised.

        Args:
            subclient_name: The name of the subclient to remove from the backupset.

        Raises:
            SDKException: If the subclient name is not a string, if the subclient does not exist,
                if the deletion fails, if the response is empty, or if the response indicates failure.

        Example:
            >>> subclients = Subclients()
            >>> subclients.delete("DailyBackupSubclient")
            >>> print("Subclient deleted successfully.")

        #ai-gen-doc
        """
        if not isinstance(subclient_name, str):
            raise SDKException('Subclient', '101')
        else:
            subclient_name = subclient_name.lower()

        if self.has_subclient(subclient_name):
            delete_subclient_service = self._services['SUBCLIENT'] % (
                self._subclients[subclient_name]['id']
            )

            flag, response = self._cvpysdk_object.make_request(
                'DELETE', delete_subclient_service)

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = response_value['errorString']

                        if error_message:
                            o_str = 'Failed to delete subclient\nError: "{0}"'
                            raise SDKException(
                                'Subclient', '102', o_str.format(error_message))
                        else:
                            if error_code == '0':
                                # initialize the subclients again
                                # so the subclient object has all the
                                # subclients
                                self.refresh()
                            else:
                                o_str = ('Failed to delete subclient with Error Code: "{0}"\n'
                                         'Please check the documentation for '
                                         'more details on the error')
                                raise SDKException(
                                    'Subclient', '102', o_str.format(error_code))
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException(
                    'Response', '101', self._update_response_(
                        response.text))
        else:
            raise SDKException(
                'Subclient', '102', 'No subclient exists with name: {0}'.format(
                    subclient_name)
            )

    def refresh(self) -> None:
        """Reload the subclients associated with the Backupset or Instance.

        This method refreshes the internal cache of subclients, ensuring that any changes 
        made on the Commcell are reflected in the current object. Use this method to 
        update the subclient list after adding, removing, or modifying subclients.

        Example:
            >>> subclients = Subclients(backupset_object)
            >>> subclients.refresh()  # Refresh the subclient list to reflect latest changes
            >>> print("Subclients refreshed successfully")

        #ai-gen-doc
        """
        self._subclients = self._get_subclients()

    @property
    def default_subclient(self) -> str:
        """Get the name of the default subclient for the selected Agent and Backupset.

        Returns:
            The name of the default subclient as a string.

        Example:
            >>> subclients = Subclients()
            >>> default_name = subclients.default_subclient
            >>> print(f"Default subclient name: {default_name}")

        #ai-gen-doc
        """
        return self._default_subclient


class Subclient(object):
    """
    Base class for managing Subclient entities within a backup and restore framework.

    The Subclient class encapsulates all common properties and operations required for
    handling subclients, including configuration, backup, restore, and property management.
    It provides a comprehensive interface for interacting with subclient objects, enabling
    advanced backup options, scheduling, and metadata management.

    Key Features:
        - Initialization and representation of subclient objects
        - Dynamic attribute access and property management
        - Backup operations with support for advanced and common options
        - Restore operations (in-place and out-of-place) with granular control
        - Scheduling and enabling/disabling backup features
        - IntelliSnap and TrueUp feature management
        - Proxy and storage policy configuration
        - Browsing, finding, and listing media associated with subclients
        - Content indexing and job management
        - Data reader and buffer size configuration
        - Encryption, deduplication, and compression settings
        - Metadata preview and retrieval
        - Refresh and update of subclient properties

    This class is intended to be used as a foundational component for more specialized
    subclient implementations, providing a robust set of tools for backup and restore
    operations in enterprise environments.

    #ai-gen-doc
    """

    def __new__(cls, backupset_object: object, subclient_name: str, subclient_id: str = None) -> 'Subclient':
        """Create a new instance of the Subclient class.

        This method is responsible for constructing a new Subclient object associated with a specific backupset.
        It allows specifying the subclient's name and optionally its unique identifier.

        Args:
            backupset_object: The backupset object to which this subclient belongs.
            subclient_name: The name of the subclient to be created.
            subclient_id: Optional; the unique identifier for the subclient. If not provided, a new ID may be generated.

        Returns:
            Subclient: A new instance of the Subclient class.

        Example:
            >>> subclient = Subclient(backupset_object, "DailyBackup", "12345")
            >>> print(f"Subclient created: {subclient}")

        #ai-gen-doc
        """
        from .subclients.fssubclient import FileSystemSubclient
        from .subclients.bigdataappssubclient import BigDataAppsSubclient
        from .subclients.vssubclient import VirtualServerSubclient
        from .subclients.casubclient import CloudAppsSubclient
        from .subclients.sqlsubclient import SQLServerSubclient
        from .subclients.nassubclient import NASSubclient
        from .subclients.hanasubclient import SAPHANASubclient
        from .subclients.oraclesubclient import OracleSubclient
        from .subclients.lotusnotes.lndbsubclient import LNDbSubclient
        from .subclients.lotusnotes.lndocsubclient import LNDocSubclient
        from .subclients.lotusnotes.lndmsubclient import LNDmSubclient
        from .subclients.sybasesubclient import SybaseSubclient
        from .subclients.saporaclesubclient import SAPOracleSubclient
        from .subclients.exchsubclient import ExchangeSubclient
        from .subclients.mysqlsubclient import MYSQLSubclient
        from .subclients.exchange.exchange_database_subclient import ExchangeDatabaseSubclient
        from .subclients.postgressubclient import PostgresSubclient
        from .subclients.informixsubclient import InformixSubclient
        from .subclients.adsubclient import ADSubclient
        from .subclients.sharepointsubclient import SharepointSubclient
        from .subclients.sharepointsubclient import SharepointV1Subclient
        from .subclients.vminstancesubclient import VMInstanceSubclient
        from .subclients.db2subclient import DB2Subclient
        from .subclients.casesubclient import CaseSubclient
        from .subclients.aadsubclient import AzureAdSubclient

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        _subclients_dict = {
            'big data apps': BigDataAppsSubclient,
            'file system': FileSystemSubclient,
            'virtual server': [VirtualServerSubclient, VMInstanceSubclient],
            'cloud apps': CloudAppsSubclient,
            'sql server': SQLServerSubclient,
            'nas': NASSubclient,  # SP11 or lower CS honors NAS as the Agent Name
            'ndmp': NASSubclient,  # SP12 and above honors NDMP as the Agent Name
            'sap hana': SAPHANASubclient,
            'oracle': OracleSubclient,
            'oracle rac': OracleSubclient,
            'notes database': LNDbSubclient,
            'notes document': LNDocSubclient,
            'domino mailbox archiver': LNDmSubclient,
            'sybase': SybaseSubclient,
            'sap for oracle': SAPOracleSubclient,
            "exchange mailbox": [ExchangeSubclient, CaseSubclient],
            'mysql': MYSQLSubclient,
            'exchange database': ExchangeDatabaseSubclient,
            'postgresql': PostgresSubclient,
            'db2': DB2Subclient,
            'informix': InformixSubclient,
            'active directory': ADSubclient,
            'sharepoint server': [SharepointV1Subclient, SharepointSubclient],
            "azure ad": AzureAdSubclient
        }

        agent_object = backupset_object._agent_object
        instance_object = backupset_object._instance_object
        client_object = agent_object._client_object

        agent_name = agent_object.agent_name.lower()

        if isinstance(_subclients_dict.get(agent_name), list):
            if instance_object.instance_name == "vminstance":
                _class = _subclients_dict[agent_name][-1]
            elif client_object.client_type and int(client_object.client_type) == 36:
                # client type 36 is case manager client
                _class = _subclients_dict[agent_name][-1]
            elif int(agent_object.agent_id) == 78 and client_object.client_type:
                # agent id 78 is sharepoint client
                _class = _subclients_dict[agent_name][-1]
            else:
                _class = _subclients_dict[agent_name][0]
        else:
            _class = _subclients_dict.get(agent_name, cls)

        if _class.__new__ == cls.__new__:
            return object.__new__(_class)
        return _class.__new__(_class, backupset_object, subclient_name, subclient_id)

    def __init__(self, backupset_object: object, subclient_name: str, subclient_id: str = None) -> None:
        """Initialize a Subclient object.

        Args:
            backupset_object: Instance of the Backupset class to which this subclient belongs.
            subclient_name: Name of the subclient.
            subclient_id: Optional; ID of the subclient. If not provided, it will be determined automatically.

        Example:
            >>> backupset = Backupset(client_object, 'defaultBackupSet')
            >>> subclient = Subclient(backupset, 'default')
            >>> print(f"Subclient created: {subclient}")

        #ai-gen-doc
        """
        self._backupset_object = backupset_object
        self._subclient_name = subclient_name.split('\\')[-1].lower()

        self._commcell_object = self._backupset_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._instance_object = self._backupset_object._instance_object
        self._agent_object = self._backupset_object._agent_object
        self._client_object = self._agent_object._client_object

        self._restore_methods = [
            '_process_restore_response',
            '_filter_paths',
            '_process_search_response',
            '_restore_json',
            '_impersonation_json',
            '_restore_browse_option_json',
            '_restore_common_options_json',
            '_restore_destination_json',
            '_restore_fileoption_json',
            '_json_restore_subtask'
        ]

        self._restore_options_json = [
            '_impersonation_json_',
            '_browse_restore_json',
            '_destination_restore_json',
            '_commonoption_restore_json',
            '_fileoption_restore_json',

        ]

        self._backupcopy_interfaces = {
            'FILESYSTEM': 1,
            'RMAN': 2,
            'VOLUME': 3
        }

        if subclient_id:
            self._subclient_id = str(subclient_id)
        else:
            self._subclient_id = self._get_subclient_id()

        self._SUBCLIENT = self._services['SUBCLIENT'] % (self.subclient_id)
        self._CLOUD_CONTENT_BROWSE = self._services['CLOUD_CONTENT_BROWSE']

        self._BROWSE = self._services['BROWSE']

        self._RESTORE = self._services['RESTORE']

        self._PREVIEW_CONTENT = self._services['GET_DOC_PREVIEW']
        self._DOBROWSE = self._services['BROWSE']

        self._subclient_properties = {}
        self._content = []
        self._additional_settings = None

        self.schedules = None
        self.refresh()

    def __getattr__(self, attribute: str) -> object:
        """Retrieve the value of a persistent attribute for the Subclient instance.

        Args:
            attribute: The name of the attribute to retrieve.

        Returns:
            The value of the requested persistent attribute.

        Example:
            >>> value = subclient.__getattr__('backupset_name')
            >>> print(f"Backupset name: {value}")

        #ai-gen-doc
        """
        if attribute in self._restore_methods:
            return getattr(self._backupset_object, attribute)
        if attribute in self._restore_options_json:
            return getattr(self._backupset_object, attribute)

        return super(Subclient, self).__getattribute__(attribute)

    def __repr__(self) -> str:
        """Return the string representation of the Subclient instance.

        This method provides a developer-friendly string that represents the current Subclient object,
        which is useful for debugging and logging purposes.

        Returns:
            A string representation of the Subclient instance.

        Example:
            >>> subclient = Subclient()
            >>> print(repr(subclient))
            <Subclient object at 0x7f8b2c1d2e80>

        #ai-gen-doc
        """
        representation_string = 'Subclient class instance for Subclient: "{0}" of Backupset: "{1}"'
        return representation_string.format(
            self.subclient_name, self._backupset_object.backupset_name
        )

    def _get_subclient_id(self) -> str:
        """Retrieve the subclient ID associated with the specified backupset and client.

        Returns:
            The unique identifier (ID) of this subclient as a string.

        Example:
            >>> subclient = Subclient()
            >>> subclient_id = subclient._get_subclient_id()
            >>> print(f"Subclient ID: {subclient_id}")

        #ai-gen-doc
        """
        subclients = Subclients(self._backupset_object)
        return subclients.get(self.subclient_name).subclient_id

    def _get_subclient_properties(self) -> None:
        """Retrieve and update the properties of this subclient from the Commcell.

        This method fetches the latest subclient properties and updates the internal state
        of the Subclient object. It should be called to ensure the object reflects the most
        current configuration from the Commcell.

        Raises:
            SDKException: If the response from the Commcell is empty or indicates a failure.

        Example:
            >>> subclient = Subclient()
            >>> subclient._get_subclient_properties()
            >>> # The subclient object now has updated properties from the Commcell

        #ai-gen-doc
        """

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._SUBCLIENT)

        if flag:
            if response.json() and 'subClientProperties' in response.json():
                self._subclient_properties = response.json()[
                    'subClientProperties'][0]

                if 'commonProperties' in self._subclient_properties:
                    self._commonProperties = self._subclient_properties['commonProperties']

                if 'subClientEntity' in self._subclient_properties:
                    self._subClientEntity = self._subclient_properties['subClientEntity']

                if 'proxyClient' in self._subclient_properties:
                    self._proxyClient = self._subclient_properties['proxyClient']

                if 'planEntity' in self._subclient_properties:
                    self._planEntity = self._subclient_properties['planEntity']

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def _set_subclient_properties(self, attr_name: str, value: str) -> None:
        """Set a property of the subclient and update its value upon a successful POST call.

        This method updates the specified attribute of the subclient instance with the provided value.
        The change is applied to the instance only if the update operation succeeds.

        Args:
            attr_name: The name of the subclient attribute to update. This should correspond to an instance variable.
            value: The new value to assign to the specified attribute.

        Raises:
            SDKException: If the update operation fails to set the subclient property.

        Example:
            >>> subclient._set_subclient_properties('description', 'Updated subclient description')
            >>> # The 'description' attribute of the subclient is now updated if the operation succeeds.

        #ai-gen-doc
        """
        try:
            backup = eval('self.%s' % attr_name)  # Take backup of old value
        except (AttributeError, KeyError):
            backup = None

        exec("self.%s = %s" % (attr_name, 'value'))  # set new value

        request_json = self._get_subclient_properties_json()

        flag, response = self._cvpysdk_object.make_request('POST', self._SUBCLIENT, request_json)

        output = self._process_update_response(flag, response)

        if output[0]:
            return
        else:
            o_str = 'Failed to update properties of subclient\nError: "{0}"'

            # Restore original value from backup on failure
            exec("self.%s = %s" % (attr_name, backup))

            raise SDKException('Subclient', '102', o_str.format(output[2]))

    @staticmethod
    def _convert_size(input_size: float) -> str:
        """Convert a numeric size value to a human-readable string with appropriate units.

        This method takes a size value (in bytes) and converts it to a string representation
        using the most suitable unit (B, KB, MB, GB, etc.), making it easier to read and interpret.

        Args:
            input_size: The size value in bytes as a float.

        Returns:
            A string representing the size in the most appropriate unit (e.g., '512 B', '1.5 MB').

        Example:
            >>> Subclient._convert_size(1024)
            '1.0 KB'
            >>> Subclient._convert_size(1048576)
            '1.0 MB'
            >>> Subclient._convert_size(123)
            '123.0 B'

        #ai-gen-doc
        """
        if input_size == 0:
            return '0B'

        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(input_size, 1024)))
        power = math.pow(1024, i)
        size = round(input_size / power, 2)
        return '%s %s' % (size, size_name[i])

    def _process_update_response(self, flag: bool, response: dict) -> tuple:
        """Process the response from a subclient property update request.

        This method evaluates the response received after attempting to update subclient properties.
        It returns a tuple containing the success status, error code, and error message.

        Args:
            flag: Boolean indicating whether the update request was successful.
            response: Dictionary containing the response details from the update request.

        Returns:
            A tuple of (success_flag, error_code, error_message):
                success_flag (bool): True if the update was successful, False otherwise.
                error_code (str): Error code received in the response, if any.
                error_message (str): Error message received in the response, if any.

        Raises:
            SDKException: If the update fails, the response is empty, or the response indicates failure.

        Example:
            >>> success, error_code, error_msg = subclient._process_update_response(True, {"errorCode": "0", "errorMessage": ""})
            >>> print(f"Success: {success}, Error Code: {error_code}, Error Message: {error_msg}")
            >>> # Use the returned values to handle update results

        #ai-gen-doc
        """
        if flag:
            if response.json():
                if "response" in response.json():
                    error_code = str(
                        response.json()["response"][0]["errorCode"])

                    if error_code == "0":
                        return (True, "0", "")
                    else:
                        error_message = ""

                        if "errorString" in response.json()["response"][0]:
                            error_message = response.json(
                            )["response"][0]["errorString"]

                        if error_message:
                            return (False, error_code, error_message)
                        else:
                            return (False, error_code, "")
                elif "errorCode" in response.json():
                    error_code = str(response.json()['errorCode'])
                    error_message = response.json()['errorMessage']

                    if error_code == "0":
                        return (True, "0", "")

                    if error_message:
                        return (False, error_code, error_message)
                    else:
                        return (False, error_code, "")
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def _process_backup_response(self, flag: str, response: dict) -> object:
        """Process the backup response for a subclient and return the corresponding job or schedule object.

        This method handles the response from a backup request for a subclient. Depending on the type of job,
        it returns either a Job object (for immediate jobs) or a Schedule object (for scheduled jobs).

        Args:
            flag: A string indicating the type of backup operation or job.
            response: The response dictionary received from the backup request.

        Returns:
            An instance of the Job class if the backup is an immediate job, or an instance of the Schedule class
            if the backup is a scheduled job.

        Raises:
            SDKException: If job initialization fails, if the response is empty, or if the response indicates failure.

        Example:
            >>> job_or_schedule = subclient._process_backup_response('IMMEDIATE', backup_response)
            >>> print(f"Received object: {job_or_schedule}")
            >>> # The returned object can be a Job or Schedule instance depending on the backup type

        #ai-gen-doc
        """
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    if len(response.json()['jobIds']) == 1:
                        return Job(self._commcell_object,
                                   response.json()['jobIds'][0])
                    else:
                        joblist = []
                        for jobids in response.json()['jobIds']:
                            joblist.append(Job(self._commcell_object, jobids))
                        return joblist
                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])
                elif "errorCode" in response.json():
                    o_str = 'Initializing backup failed\nError: "{0}"'.format(
                        response.json()['errorMessage']
                    )
                    raise SDKException('Subclient', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def _backup_json(self,
                     backup_level: str,
                     incremental_backup: bool,
                     incremental_level: str,
                     advanced_options: Optional[Dict[str, Any]] = None,
                     schedule_pattern: Optional[Dict[str, Any]] = None,
                     common_backup_options: Optional[Dict[str, Any]] = None
                     ) -> Dict[str, Any]:
        """Construct the JSON request payload for a backup operation based on user-selected options.

        Args:
            backup_level: The level of backup to perform. Valid values include:
                "Full", "Incremental", "Differential", "Synthetic_full".
            incremental_backup: Whether to run an incremental backup. Only applicable for "Synthetic_full" backups.
            incremental_level: Specifies when to run the incremental backup relative to the synthetic full.
                Valid values: "BEFORE_SYNTH", "AFTER_SYNTH". Only applicable for "Synthetic_full" backups.
            advanced_options: Optional dictionary of advanced backup options to include in the request.
            schedule_pattern: Optional dictionary specifying the schedule pattern for the backup.
            common_backup_options: Optional dictionary of advanced job options to include in the request.

        Returns:
            Dictionary representing the JSON request to be sent to the API for the backup operation.

        Example:
            >>> subclient = Subclient()
            >>> backup_json = subclient._backup_json(
            ...     backup_level="Synthetic_full",
            ...     incremental_backup=True,
            ...     incremental_level="BEFORE_SYNTH",
            ...     advanced_options={"option1": "value1"},
            ...     schedule_pattern={"pattern": "daily"},
            ...     common_backup_options={"jobOption": "fast"}
            ... )
            >>> print(backup_json)
            >>> # The returned dictionary can be used to initiate a backup via the API

        #ai-gen-doc
        """

        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": self._json_backup_subtasks,
                        "options": {
                            "backupOpts": {
                                "backupLevel": backup_level,
                                "incLevel": incremental_level,
                                "runIncrementalBackup": incremental_backup
                            }
                        }
                    }
                ]
            }
        }

        advanced_options_dict = {}

        if advanced_options:
            if advanced_options.get('impersonate_gui'):
                request_json['taskInfo']['task']['initiatedFrom'] = 1
            advanced_options_dict = self._advanced_backup_options(
                advanced_options)

        if advanced_options_dict:
            request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
                advanced_options_dict
            )

        advance_job_option_dict = {}

        if common_backup_options:
            advance_job_option_dict = self._common_backup_options(
                common_backup_options)

        if advance_job_option_dict:
            request_json["taskInfo"]["subTasks"][0]["options"]["commonOpts"] = advance_job_option_dict

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        return request_json

    def _common_backup_options(self, options: dict) -> dict:
        """Generate the advanced job options dictionary for backup operations.

        Args:
            options: A dictionary containing advanced job options to be included in the backup request.

        Returns:
            A dictionary representing the generated advanced job options for the backup job.

        Example:
            >>> subclient = Subclient()
            >>> advanced_options = {
            ...     "priority": "high",
            ...     "throttle": True
            ... }
            >>> job_options = subclient._common_backup_options(advanced_options)
            >>> print(job_options)
            {'priority': 'high', 'throttle': True}

        #ai-gen-doc
        """
        return options

    def _advanced_backup_options(self, options: dict) -> dict:
        """Generate the advanced backup options dictionary for a backup request.

        Args:
            options: A dictionary containing advanced backup options to be included in the request.

        Returns:
            A dictionary representing the generated advanced backup options, ready to be used in a backup request.

        Example:
            >>> subclient = Subclient()
            >>> options = {
            ...     "encryption": True,
            ...     "priority": 5,
            ...     "backupLevel": "FULL"
            ... }
            >>> advanced_options = subclient._advanced_backup_options(options)
            >>> print(advanced_options)
            {'encryption': True, 'priority': 5, 'backupLevel': 'FULL'}

        #ai-gen-doc
        """
        return options

    def _process_index_delete_response(self, flag: bool, response: object) -> 'Job':
        """Process the response for an index delete job and return the corresponding Job object.

        This method handles the response from an index delete request for a subclient. It validates the response,
        initiates the Job object for the index delete operation, and returns it for further tracking or management.

        Args:
            flag: Boolean flag indicating whether to initiate the index delete job.
            response: The response object received after making the index delete request.

        Returns:
            Job: An instance of the Job class representing the index delete job.

        Raises:
            SDKException: If job initialization fails, the response is empty, or the response indicates failure.

        Example:
            >>> job = subclient._process_index_delete_response(True, response)
            >>> print(f"Index delete job ID: {job.job_id}")
            >>> # Use the returned Job object to monitor job status or retrieve job details

        #ai-gen-doc
        """
        if flag:
            if response.json():
                if "resp" in response.json():
                    error_code = response.json()['resp']['errorCode']
                    if error_code != 0:
                        error_string = response.json().get('response', {}).get('errorString', str())
                        o_str = 'Failed to Delete Documents\nError: "{0}"'.format(error_string)
                        raise SDKException('Subclient', '102', o_str)
                elif 'errorMessage' in response.json():
                    error_string = response.json()['errorMessage']
                    o_str = 'Failed to Delete Documents\nError: "{0}"'.format(error_string)
                    raise SDKException('Subclient', '102', o_str)
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()["jobIds"][0])
            return None
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def browse_Cosmos_Content(self, update_dict: dict):
        """
        Does a cloud content browse to validate the Backup Account exists
        """
        browse_json = {
            "instanceType": 51,
            "clientEntity":
                {
                    "clientId": update_dict["clientId"],
                    "clientName": update_dict["clientName"]
                },
            "appId":
                {
                    "clientName": update_dict["clientName"],
                    "clientId": update_dict["clientId"],
                    "instanceId": update_dict["instanceId"],
                    "applicationId": 134
                },
            "browseTargetType": {}
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._CLOUD_CONTENT_BROWSE, browse_json)
        if flag:
            return response.json()
        else:
            raise SDKException('Subclient','102','Browse Failed')

    def _restore_atlas_option_json(self, restore_dict: dict) :
        """Setter for Atlas restore option in restore JSON. and launching restore job"""

        # Before running restore we need to browse for backed up Data to get cluster path

        entity_json = {
            "backupsetId": restore_dict["backupsetId"],
            "instanceId": restore_dict["instanceId"],
            "subclientId": restore_dict["subclientId"],
            "clientId": restore_dict["clientId"],
            "applicationId": 134
        }

        browse_json = {
            "opType": 0,
            "queries": [
                {
                    "type": 0,
                    "queryId": "0"
                }
            ],
            "paths": [
                {
                    "path": "/"
                }
            ],
            "timeRange": {
                "toTime": 0
            },
            "entity": entity_json
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._DOBROWSE, browse_json)
        response = response.json()
        result = response['browseResponses'][0]['browseResult']['dataResultSet'][0]
        if 'displayName' not in result or 'displayPath' not in result:
            raise SDKException('Response', '102')
        display_name = result['displayName']
        display_path = result['displayPath']

        restore_json = {
            "taskInfo": {
                "associations": [entity_json],
                "task": {"taskType": 1},
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 3,
                            "operationType": 1001
                        },
                        "options": {
                            "restoreOptions": {
                                "browseOption": {
                                    "commCellId": 2,
                                    "timeRange": {
                                        "fromTime": 0,
                                        "toTime": 0
                                    }
                                },
                                "destination": {
                                    "destClient": entity_json,
                                    "destinationInstance": entity_json
                                },
                                "fileOption": {
                                    "sourceItem": [display_path]

                                },
                                "commonOptions": {},
                                "jobIds": [],
                                "cloudAppsRestoreOptions": {
                                    "instanceType": 40,
                                    "mongoDBAtlasRestoreOptions": {
                                        "targetClusterNamesList": [display_name],
                                        "isOutOfPlaceRestore": False,
                                        "isRestoreToLatest": True,
                                        "isRestoreToPIT": False,
                                        "sourceProjectAppId": restore_dict["subclientId"]
                                    }
                                }
                            }
                        }
                    }
                ]
            }}

        flag, response = self._cvpysdk_object.make_request('POST', self._RESTORE, restore_json)

        self._restore_association = None

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])

                elif "taskId" in response.json():
                    return Schedules(self._commcell_object).get(task_id=response.json()['taskId'])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def update_atlas_instance(self, update_dict: dict) -> None:
        """
        updates the property of Subclient using the provided dictionary
        for atlas we need an additional step to browse path of provided cluster and
        this needs to be updated in subclient property
        """

        browse_json = {
            "instanceType": 40,
            "clientEntity": {
                "clientId": update_dict["clientId"],
                "clientName": update_dict["clientName"],
            },
            "appId": {
                "clientName":update_dict["clientName"],
                "clientId": update_dict["clientId"],
                "instanceId": update_dict["instanceId"],
                "applicationId": 134
            },
            "browseTargetType": {}
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._CLOUD_CONTENT_BROWSE, browse_json)
        if not flag:
            raise SDKException ('Response','101',self._update_response_(response.text))
        response= response.json()
        org_name = response ["cloudDBEntity"]["children"][0]["name"]
        project_name = update_dict["AtlasProjectName"]
        browse_json["browsePath"] = f"{org_name}/{project_name}"

        flag, response = self._cvpysdk_object.make_request('POST', self._CLOUD_CONTENT_BROWSE, browse_json)
        if not flag:
            raise SDKException ('Response','101',self._update_response_(response.text))
        response= response.json()
        path = response["cloudDBEntity"]["children"][0]["path"]

        properties_dict = {
            "cloudAppsSubClientProp": {
                "instanceType": 4
            },
            "cloudDbContent": {
                "children": [
                    {
                        "allOrAnyChildren": True,
                        "displayName": update_dict["AtlasClusterName"],
                        "name": update_dict["AtlasClusterName"],
                        "path": path,
                        "negation": False,
                        "type": 48,
                        "value": f"{org_name}/{project_name}/{update_dict['AtlasClusterName']}"
                    }
                ]
            },
            "cloudDbFilter": {
            },
            "commonProperties": {
                "numberOfBackupStreams": 2
            }
        }

        self.update_properties(properties_dict)

    def update_properties(self, properties_dict: dict) -> None:
        """Update the properties of the subclient using the provided dictionary.

        This method updates the subclient's configuration by applying the changes specified
        in the `properties_dict`. To modify subclient properties safely, obtain a deep copy
        of the current properties using `self.properties`, update the desired fields, and
        then pass the modified dictionary to this method.

        Args:
            properties_dict: A dictionary containing the subclient properties to update.

        Raises:
            SDKException: If the update operation fails, the response is empty, or the response
                code is not as expected.

        Example:
            >>> # Get a deep copy of current properties
            >>> props = subclient.properties
            >>> # Modify a property
            >>> props['commonProperties']['description'] = "Updated description"
            >>> # Update the subclient with new properties
            >>> subclient.update_properties(props)

        #ai-gen-doc
        """
        request_json = {
            "subClientProperties": {}
        }

        request_json['subClientProperties'].update(properties_dict)

        # check if subclient name is updated in the request
        # if subclient name is updated set the newName field in the request
        if properties_dict.get('subClientEntity', {}).get('subclientName') and properties_dict.get(
                'subClientEntity', {}).get('subclientName') != self._subClientEntity.get('subclientName'):
            request_json['newName'] = properties_dict.get('subClientEntity', {}).get('subclientName')
        flag, response = self._cvpysdk_object.make_request('POST', self._SUBCLIENT, request_json)
        status, _, error_string = self._process_update_response(flag, response)
        self.refresh()

        if not status:
            raise SDKException('Subclient', '102', 'Failed to update subclient properties\nError: "{}"'.format(
                error_string))

    @property
    def properties(self) -> dict:
        """Get the properties of the subclient.

        Returns:
            dict: A dictionary containing the subclient's properties and configuration details.

        Example:
            >>> subclient = Subclient()
            >>> props = subclient.properties
            >>> print(props)
            {'subclientName': 'default', 'backupSetName': 'BackupSet1', ...}

        #ai-gen-doc
        """
        return copy.deepcopy(self._subclient_properties)

    @property
    def name(self) -> str:
        """Get the display name of the Subclient.

        Returns:
            The display name of the Subclient as a string.

        Example:
            >>> subclient = Subclient()
            >>> display_name = subclient.name  # Use dot notation for property access
            >>> print(f"Subclient name: {display_name}")

        #ai-gen-doc
        """
        return self._subclient_properties['subClientEntity']['subclientName']

    @property
    def display_name(self) -> str:
        """Get the display name of the Subclient.

        Returns:
            The display name of the Subclient as a string.

        Example:
            >>> subclient = Subclient()
            >>> name = subclient.display_name  # Use dot notation for property access
            >>> print(f"Subclient display name: {name}")

        #ai-gen-doc
        """
        return self.name

    @property
    def subclient_guid(self) -> str:
        """Get the unique GUID (Globally Unique Identifier) of the subclient.

        Returns:
            str: The GUID associated with this subclient.

        Example:
            >>> subclient = Subclient()
            >>> guid = subclient.subclient_guid  # Use dot notation for property access
            >>> print(f"Subclient GUID: {guid}")

        #ai-gen-doc
        """
        return self._subclient_properties.get('subClientEntity', {}).get('subclientGUID')

    @display_name.setter
    def display_name(self, display_name: str) -> None:
        """Set the display name for the subclient.

        Args:
            display_name: The new display name to assign to the subclient.

        Example:
            >>> subclient.display_name = "Critical Data Subclient"
            >>> # The subclient's display name is now set to "Critical Data Subclient"
        #ai-gen-doc
        """
        update_properties = self.properties
        update_properties['subClientEntity']['subclientName'] = display_name
        self.update_properties(update_properties)

    @name.setter
    def name(self, name: str) -> None:
        """Set the name for the subclient.

        Args:
            name: The new name to assign to the subclient.

        Example:
            >>> subclient = Subclient()
            >>> subclient.name = "NewSubclientName"  # Use assignment to set the name
            >>> print(subclient.name)
            NewSubclientName

        #ai-gen-doc
        """
        self.display_name = name

    @property
    def _json_task(self) -> dict:
        """Get the task information for this subclient in JSON format.

        Returns:
            dict: A dictionary containing the task information in JSON format.

        Example:
            >>> subclient = Subclient()
            >>> task_json = subclient._json_task
            >>> print(task_json)
            >>> # The output will be a dictionary representing the subclient's task details.

        #ai-gen-doc
        """

        _taks_option_json = {
            "initiatedFrom": 2,
            "taskType": 1,
            "policyType": 0,
            "taskFlags": {
                "disabled": False
            }
        }

        return _taks_option_json

    @property
    def _json_backup_subtasks(self) -> dict:
        """Get the backup subtask information for use in restore JSON.

        This property provides a read-only dictionary containing the subtask details 
        required for backup operations in the restore JSON format.

        Returns:
            dict: A dictionary representing the backup subtask information.

        Example:
            >>> subclient = Subclient()
            >>> subtasks = subclient._json_backup_subtasks
            >>> print(subtasks)
            {'subtaskName': 'Backup', 'subtaskType': 1, ...}

        #ai-gen-doc
        """

        _backup_subtask = {
            "subTaskType": 2,
            "operationType": 2
        }

        return _backup_subtask

    @property
    def subclient_id(self) -> int:
        """Get the unique identifier of the subclient as a read-only property.

        Returns:
            The subclient's unique ID as an integer.

        Example:
            >>> subclient = Subclient()
            >>> subclient_id = subclient.subclient_id  # Access the subclient ID property
            >>> print(f"Subclient ID: {subclient_id}")

        #ai-gen-doc
        """
        return self._subclient_id

    @property
    def subclient_name(self) -> str:
        """Get the name of the subclient as a read-only property.

        Returns:
            The name of the subclient as a string.

        Example:
            >>> subclient = Subclient()
            >>> name = subclient.subclient_name  # Access the subclient name property
            >>> print(f"Subclient name: {name}")
            >>> # The subclient_name property is read-only and cannot be modified directly

        #ai-gen-doc
        """
        return self._subclient_name

    @property
    def last_backup_time(self) -> str:
        """Get the last backup time for this subclient as a read-only property.

        Returns:
            The last backup time as a string, typically in a standard date-time format.

        Example:
            >>> subclient = Subclient()
            >>> last_time = subclient.last_backup_time  # Access as a property
            >>> print(f"Last backup was at: {last_time}")

        #ai-gen-doc
        """
        if 'lastBackupTime' in self._commonProperties:
            if self._commonProperties['lastBackupTime'] != 0:
                _last_backup_time = time.ctime(
                    self._commonProperties['lastBackupTime']
                )
                return _last_backup_time
        return 0

    @property
    def next_backup_time(self) -> str:
        """Get the scheduled time for the next backup as a read-only property.

        Returns:
            str: The next scheduled backup time in string format.

        Example:
            >>> subclient = Subclient()
            >>> next_time = subclient.next_backup_time  # Access as a property
            >>> print(f"Next backup is scheduled at: {next_time}")

        #ai-gen-doc
        """
        if 'nextBackupTime' in self._commonProperties:
            if self._commonProperties['nextBackupTime'] != 0:
                _next_backup = time.ctime(
                    self._commonProperties['nextBackupTime']
                )
                return _next_backup

    @property
    def is_backup_enabled(self) -> bool:
        """Indicate whether backup is enabled for this subclient.

        Returns:
            True if backup is enabled for the subclient, False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> if subclient.is_backup_enabled:
            ...     print("Backup is enabled for this subclient.")
            ... else:
            ...     print("Backup is not enabled for this subclient.")

        #ai-gen-doc
        """
        if 'enableBackup' in self._commonProperties:
            return self._commonProperties['enableBackup']

    @property
    def is_intelli_snap_enabled(self) -> bool:
        """Indicate whether IntelliSnap is enabled for this subclient.

        Returns:
            bool: True if IntelliSnap is enabled, False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> if subclient.is_intelli_snap_enabled:
            ...     print("IntelliSnap is enabled for this subclient.")
            ... else:
            ...     print("IntelliSnap is not enabled for this subclient.")

        #ai-gen-doc
        """
        if 'snapCopyInfo' in self._commonProperties:
            snap_copy_info = self._commonProperties.get('snapCopyInfo')
            return snap_copy_info.get('isSnapBackupEnabled')

    @property
    def is_blocklevel_backup_enabled(self) -> bool:
        """Check if block-level backup is enabled for this subclient.

        Returns:
            True if block-level backup is enabled; False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> if subclient.is_blocklevel_backup_enabled:
            ...     print("Block-level backup is enabled.")
            ... else:
            ...     print("Block-level backup is not enabled.")

        #ai-gen-doc
        """
        return bool(self._subclient_properties.get(
            'postgreSQLSubclientProp', {}).get('isUseBlockLevelBackup', False))

    @property
    def snapshot_engine_name(self) -> str:
        """Get the snapshot engine name associated with this subclient.

        Returns:
            The name of the snapshot engine configured for the subclient.

        Example:
            >>> subclient = Subclient()
            >>> engine_name = subclient.snapshot_engine_name  # Use dot notation for property
            >>> print(f"Snapshot engine: {engine_name}")

        #ai-gen-doc
        """
        if self.is_intelli_snap_enabled:
            if 'snapCopyInfo' in self._commonProperties:
                snap_copy_info = self._commonProperties.get('snapCopyInfo', "")
                if 'snapToTapeSelectedEngine' in snap_copy_info:
                    if 'snapShotEngineName' in snap_copy_info.get('snapToTapeSelectedEngine', ""):
                        return snap_copy_info['snapToTapeSelectedEngine'].get(
                            'snapShotEngineName', "")
        raise SDKException(
            'Subclient',
            '102',
            'Cannot fetch snap engine name.')

    @property
    def is_trueup_enabled(self) -> bool:
        """Indicate whether the TrueUp feature is enabled for this Subclient.

        Returns:
            bool: True if TrueUp is enabled for the subclient, False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> if subclient.is_trueup_enabled:
            ...     print("TrueUp is enabled for this subclient.")
            ... else:
            ...     print("TrueUp is not enabled for this subclient.")

        #ai-gen-doc
        """
        if 'isTrueUpOptionEnabled' in self._commonProperties:
            return self._commonProperties['isTrueUpOptionEnabled']

    @property
    def is_on_demand_subclient(self) -> bool:
        """Indicate whether this subclient is an on-demand subclient.

        This property provides a read-only boolean value that specifies if the subclient 
        is configured as an on-demand subclient.

        Returns:
            True if the subclient is on-demand; False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> if subclient.is_on_demand_subclient:
            ...     print("This is an on-demand subclient.")
            ... else:
            ...     print("This is a regular subclient.")

        #ai-gen-doc
        """
        return self._backupset_object.is_on_demand_backupset

    @property
    def description(self) -> str:
        """Get the description of the subclient.

        This property allows you to access the description associated with the subclient instance.

        Returns:
            The description of the subclient as a string.

        Example:
            >>> subclient = Subclient()
            >>> desc = subclient.description  # Access the description property
            >>> print(f"Subclient description: {desc}")

        #ai-gen-doc
        """
        if 'description' in self._commonProperties:
            return self._commonProperties['description']

    @property
    def storage_policy(self) -> str:
        """Get the storage policy associated with this subclient as a read-only property.

        Returns:
            The name of the storage policy assigned to the subclient.

        Example:
            >>> subclient = Subclient(commcell_object, client_name, agent_name, instance_name, backupset_name, subclient_name)
            >>> policy_name = subclient.storage_policy  # Access storage policy using property
            >>> print(f"Storage policy for subclient: {policy_name}")

        #ai-gen-doc
        """
        storage_device = self._commonProperties['storageDevice']
        if 'dataBackupStoragePolicy' in storage_device:
            data_backup_storage_policy = storage_device['dataBackupStoragePolicy']
            if 'storagePolicyName' in data_backup_storage_policy:
                return data_backup_storage_policy['storagePolicyName']

    @property
    def storage_ma(self) -> str:
        """Get the storage media agent (MA) associated with this subclient as a read-only property.

        Returns:
            The name of the storage media agent (MA) assigned to the subclient.

        Example:
            >>> subclient = Subclient()
            >>> ma_name = subclient.storage_ma  # Access the storage MA as a property
            >>> print(f"Storage Media Agent: {ma_name}")
        #ai-gen-doc
        """
        storage_device = self._commonProperties['storageDevice']
        if 'performanceMode' in storage_device:
            data_backup_storage_device = storage_device['performanceMode']
            data_storage_details = data_backup_storage_device["perfCRCDetails"][0]
            if 'perfMa' in data_storage_details:
                return data_storage_details['perfMa']

    @property
    def storage_ma_id(self) -> int:
        """Get the storage media agent ID associated with this subclient.

        This property provides read-only access to the storage media agent (MA) ID 
        for the subclient, which uniquely identifies the media agent used for storage operations.

        Returns:
            The storage media agent ID as an integer.

        Example:
            >>> subclient = Subclient()
            >>> ma_id = subclient.storage_ma_id  # Access the storage MA ID using dot notation
            >>> print(f"Storage Media Agent ID: {ma_id}")

        #ai-gen-doc
        """
        storage_device = self._commonProperties['storageDevice']
        if 'performanceMode' in storage_device:
            data_backup_storage_device = storage_device['performanceMode']
            data_storage_details = data_backup_storage_device["perfCRCDetails"][0]
            if 'perfMaId' in data_storage_details:
                return data_storage_details['perfMaId']

    @property
    def data_readers(self) -> int:
        """Get the number of data readers configured for this subclient.

        Returns:
            The number of data readers as an integer.

        Example:
            >>> subclient = Subclient()
            >>> readers = subclient.data_readers  # Access as a property
            >>> print(f"Number of data readers: {readers}")

        #ai-gen-doc
        """
        if 'numberOfBackupStreams' in self._commonProperties:
            return int(
                self._commonProperties['numberOfBackupStreams']
            )

    @data_readers.setter
    def data_readers(self, value: int) -> None:
        """Set the number of data readers for the subclient.

        Updates the count of data readers assigned to this subclient. The value must be an integer.

        Args:
            value: The desired number of data readers to assign to the subclient.

        Raises:
            SDKException: If the update fails or if the provided value is not an integer.

        Example:
            >>> subclient = Subclient()
            >>> subclient.data_readers = 4  # Set the number of data readers to 4
            >>> # The subclient now uses 4 data readers for operations

        #ai-gen-doc
        """
        if isinstance(value, int):
            self._set_subclient_properties(
                "_commonProperties['numberOfBackupStreams']", value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient data readers should be an int value'
            )

    @property
    def allow_multiple_readers(self) -> bool:
        """Indicate whether multiple readers are allowed for this Subclient.

        This property provides read-only access to the setting that determines if multiple readers 
        can access the Subclient simultaneously, which may improve backup performance in certain scenarios.

        Returns:
            True if multiple readers are allowed; False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> if subclient.allow_multiple_readers:
            ...     print("Multiple readers are enabled for this Subclient.")
            ... else:
            ...     print("Multiple readers are not enabled.")

        #ai-gen-doc
        """
        if 'allowMultipleDataReaders' in self._commonProperties:
            return bool(
                self._commonProperties['allowMultipleDataReaders']
            )

    @allow_multiple_readers.setter
    def allow_multiple_readers(self, value: bool) -> None:
        """Enable or disable the 'allow multiple readers' property for the subclient.

        This property controls whether multiple data readers are allowed for the subclient.
        Set to True to enable multiple readers, or False to disable.

        Args:
            value: Boolean indicating whether to allow multiple readers (True) or not (False).

        Raises:
            SDKException: If the update fails or if the input value is not of type bool.

        Example:
            >>> subclient = Subclient()
            >>> subclient.allow_multiple_readers = True  # Enable multiple readers
            >>> subclient.allow_multiple_readers = False  # Disable multiple readers

        #ai-gen-doc
        """
        # Has to be initialized for new subclient as attribute is not present
        # default value is False
        if 'allowMultipleDataReaders' not in self._commonProperties:
            self._commonProperties['allowMultipleDataReaders'] = False

        if isinstance(value, bool):
            self._set_subclient_properties(
                "_commonProperties['allowMultipleDataReaders']",
                value)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient allow multple readers should be a bool value'
            )

    @property
    def read_buffer_size(self) -> int:
        """Get the read buffer size for the subclient as a read-only attribute.

        Returns:
            The read buffer size in bytes as an integer.

        Example:
            >>> subclient = Subclient()
            >>> buffer_size = subclient.read_buffer_size  # Access as a property
            >>> print(f"Read buffer size: {buffer_size} bytes")
        #ai-gen-doc
        """
        if 'readBuffersize' in self._commonProperties:
            return int(
                self._commonProperties['readBuffersize']
            )

    @property
    def is_default_subclient(self) -> bool:
        """Check if this subclient is the default subclient.

        Returns:
            True if the subclient is the default subclient, otherwise False.

        Example:
            >>> subclient = Subclient()
            >>> if subclient.is_default_subclient:
            ...     print("This is the default subclient.")
            ... else:
            ...     print("This is not the default subclient.")

        #ai-gen-doc
        """
        return self._commonProperties.get('isDefaultSubclient')

    @read_buffer_size.setter
    def read_buffer_size(self, value: int) -> None:
        """Set the read buffer size for the subclient.

        This property setter updates the read buffer size for the subclient to the specified value in kilobytes (KB).

        Args:
            value: The new read buffer size in KB. Must be an integer.

        Raises:
            SDKException: If the update fails or if the provided value is not an integer.

        Example:
            >>> subclient.read_buffer_size = 8192  # Set read buffer size to 8192 KB
            >>> print("Read buffer size updated successfully.")

        #ai-gen-doc
        """
        # Has to be initialized for new subclient as attribute is not present
        # default value is 0
        if 'readBuffersize' not in self._commonProperties:
            self._commonProperties['readBuffersize'] = 0

        if isinstance(value, int):
            self._set_subclient_properties(
                "_commonProperties['readBuffersize']",
                value)
        else:
            raise SDKException(
                'Subclient', '102',
                'Subclient read buffer size should be an int value'
            )

    @description.setter
    def description(self, value: str) -> None:
        """Set the description of the subclient.

        Updates the subclient's description to the specified string value.

        Args:
            value: The new description to assign to the subclient.

        Raises:
            SDKException: If the description update fails or if the input value is not a string.

        Example:
            >>> subclient = Subclient()
            >>> subclient.description = "This subclient handles daily backups."
            >>> # The subclient's description is now updated

        #ai-gen-doc
        """
        if isinstance(value, str):
            self._set_subclient_properties(
                "_commonProperties['description']", value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient description should be a string value'
            )

    @storage_policy.setter
    def storage_policy(self, value: str) -> None:
        """Set the storage policy for the subclient.

        Assigns the specified storage policy name to the subclient. The value must be a string
        representing the name of an existing storage policy.

        Args:
            value: The name of the storage policy to assign to the subclient.

        Raises:
            SDKException: If the provided storage policy name is not a string, or if the update fails.

        Example:
            >>> subclient = Subclient()
            >>> subclient.storage_policy = "WeeklyBackupPolicy"  # Use assignment for property setter
            >>> # The subclient's storage policy is now set to "WeeklyBackupPolicy"

        #ai-gen-doc
        """
        if isinstance(value, str):
            value = value.lower()

            if not self._commcell_object.storage_policies.has_policy(value):
                raise SDKException(
                    'Subclient',
                    '102',
                    'Storage Policy: "{0}" does not exist in the Commcell'.format(value)
                )

            self._set_subclient_properties(
                "_commonProperties['storageDevice']['dataBackupStoragePolicy']",
                {
                    "storagePolicyName": value,
                    "storagePolicyId": int(
                        self._commcell_object.storage_policies.all_storage_policies[value]
                    )
                }
            )
        else:
            raise SDKException('Subclient', '101')

    def enable_backup(self) -> None:
        """Enable backup operations for the subclient.

        This method activates backup functionality for the subclient, allowing it to participate in scheduled or manual backup jobs.

        Raises:
            SDKException: If enabling backup for the subclient fails.

        Example:
            >>> subclient = Subclient()
            >>> subclient.enable_backup()
            >>> print("Backup enabled for the subclient.")

        #ai-gen-doc
        """
        self._set_subclient_properties("_commonProperties['enableBackup']", True)

    def enable_trueup(self) -> None:
        """Enable the TrueUp option for this Subclient.

        This method activates the TrueUp feature, which ensures that backup data is accurately tracked and managed for the Subclient.

        Example:
            >>> subclient = Subclient()
            >>> subclient.enable_trueup()
            >>> print("TrueUp option enabled for the subclient.")

        #ai-gen-doc
        """
        if 'isTrueUpOptionEnabled' in self._commonProperties:
            self._set_subclient_properties("_commonProperties['isTrueUpOptionEnabled']", True)

    def enable_trueup_days(self, days: int = 30) -> None:
        """Enable the TrueUp option and set the number of days for reconciliation.

        This method configures the TrueUp feature for the subclient, specifying 
        the number of days after which reconciliation should occur.

        Args:
            days: The number of days after which the TrueUp reconciliation is performed. 
                Defaults to 30.

        Example:
            >>> subclient = Subclient()
            >>> subclient.enable_trueup_days(45)
            >>> # The TrueUp option is now enabled with reconciliation set for every 45 days.

        #ai-gen-doc
        """
        self.enable_trueup()
        self._set_subclient_properties("_commonProperties['runTrueUpJobAfterDays']", days)

    def enable_backup_at_time(self, enable_time: str) -> None:
        """Schedule the subclient to enable backup at a specified UTC time.

        This method disables backup if it is not already disabled, and then schedules 
        the backup to be enabled at the provided UTC time. The time must be specified 
        in 24-hour format as 'YYYY-MM-DD HH:mm:ss'.

        Note:
            For Linux CommServer environments, provide the time in GMT timezone.

        Args:
            enable_time: The UTC time at which to enable backup, in the format 'YYYY-MM-DD HH:mm:ss'.

        Raises:
            SDKException: If the provided time is earlier than the current time.
            SDKException: If the time format is incorrect.
            SDKException: If enabling backup fails.
            SDKException: If the response is empty or not successful.

        Example:
            >>> subclient = Subclient()
            >>> subclient.enable_backup_at_time('2024-07-01 22:30:00')
            >>> print("Backup will be enabled at the specified time.")

        #ai-gen-doc
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('Subclient', '108')
        except ValueError:
            raise SDKException('Subclient', '109')

        enable_backup_at_time = {
            "TimeZoneName": self._commcell_object.default_timezone,
            "timeValue": enable_time
        }

        self._set_subclient_properties(
            "_commonProperties['enableBackupAtDateTime']", enable_backup_at_time
        )

    def disable_backup(self) -> None:
        """Disable backup operations for the subclient.

        This method disables backup functionality for the current subclient instance.
        If the operation fails, an SDKException is raised.

        Raises:
            SDKException: If the backup could not be disabled for the subclient.

        Example:
            >>> subclient = Subclient()
            >>> subclient.disable_backup()
            >>> print("Backup has been disabled for the subclient.")

        #ai-gen-doc
        """
        self._set_subclient_properties(
            "_commonProperties['enableBackup']", False)

    def exclude_from_sla(self) -> None:
        """Exclude this subclient from Service Level Agreement (SLA) compliance.

        This method marks the subclient so that it is not considered for SLA compliance checks.

        Raises:
            SDKException: If the operation to exclude the subclient from SLA fails.

        Example:
            >>> subclient = Subclient()
            >>> subclient.exclude_from_sla()
            >>> print("Subclient successfully excluded from SLA compliance.")

        #ai-gen-doc
        """
        self._set_subclient_properties(
            "_commonProperties['excludeFromSLA']", True)

    def enable_intelli_snap(self, snap_engine_name: str, proxy_options: Optional[dict] = None) -> None:
        """Enable IntelliSnap for the subclient using the specified snap engine.

        Args:
            snap_engine_name: The name of the snap engine to use for IntelliSnap operations.
            proxy_options: Optional dictionary containing proxy configuration options for the snap engine.

        Raises:
            SDKException: If enabling IntelliSnap for the subclient fails.

        Example:
            >>> subclient = Subclient()
            >>> subclient.enable_intelli_snap('VSA_SnapEngine')
            >>> # Optionally, specify proxy options
            >>> proxy_cfg = {'proxyHost': 'proxy01', 'proxyPort': 8080}
            >>> subclient.enable_intelli_snap('VSA_SnapEngine', proxy_options=proxy_cfg)

        #ai-gen-doc
        """
        if not isinstance(snap_engine_name, str):
            raise SDKException("Subclient", "101")

        properties_dict = {
            "isSnapBackupEnabled": True,
            "snapToTapeSelectedEngine": {
                "snapShotEngineName": snap_engine_name
            }
        }

        if proxy_options is not None:
            if "snap_proxy" in proxy_options:
                properties_dict["snapToTapeProxyToUse"] = {
                    "clientName": proxy_options["snap_proxy"]
                }

            if "backupcopy_proxy" in proxy_options:
                properties_dict["useSeparateProxyForSnapToTape"] = True
                properties_dict["separateProxyForSnapToTape"] = {
                    "clientName": proxy_options["backupcopy_proxy"]
                }

            if "use_source_if_proxy_unreachable" in proxy_options:
                properties_dict["snapToTapeProxyToUseSource"] = True

        self._set_subclient_properties(
            "_commonProperties['snapCopyInfo']", properties_dict)

    def disable_intelli_snap(self) -> None:
        """Disable IntelliSnap for the subclient.

        This method disables the IntelliSnap feature for the current subclient instance.
        IntelliSnap provides snapshot-based backup capabilities, and disabling it will
        revert the subclient to standard backup operations.

        Raises:
            SDKException: If the operation to disable IntelliSnap fails.

        Example:
            >>> subclient = Subclient()
            >>> subclient.disable_intelli_snap()
            >>> print("IntelliSnap has been disabled for the subclient.")

        #ai-gen-doc
        """
        self._set_subclient_properties(
            "_commonProperties['snapCopyInfo']['isSnapBackupEnabled']", False
        )

    def set_proxy_for_snap(self, proxy_name: str) -> None:
        """Set the proxy to be used for IntelliSnap operations on the subclient.

        This method configures the specified proxy server for use with IntelliSnap backups
        on the current subclient.

        Args:
            proxy_name: The name of the proxy server to be used for IntelliSnap operations.

        Example:
            >>> subclient = Subclient()
            >>> subclient.set_proxy_for_snap("ProxyServer01")
            >>> print("Proxy for IntelliSnap set successfully.")

        #ai-gen-doc
        """
        if not isinstance(proxy_name, str):
            raise SDKException("Subclient", "101")

        properties_dict = {
            "clientName": proxy_name
        }

        update_properties = self.properties
        update_properties['commonProperties']['snapCopyInfo']['snapToTapeProxyToUse'] = properties_dict
        self.update_properties(update_properties)

    def unset_proxy_for_snap(self) -> None:
        """Unset the 'Use proxy' option for an IntelliSnap subclient.

        This method disables the proxy setting for the IntelliSnap subclient, ensuring that
        backup operations do not use a proxy server.

        Example:
            >>> subclient = Subclient()
            >>> subclient.unset_proxy_for_snap()
            >>> print("Proxy for IntelliSnap has been unset.")

        #ai-gen-doc
        """

        properties_dict = {
            "clientId": 0
        }
        update_properties = self.properties
        update_properties['commonProperties']['snapCopyInfo']['snapToTapeProxyToUse'] = properties_dict
        self.update_properties(update_properties)

    def set_proxy_for_backup_copy(self, proxy_name):
        """ method to set separate proxy server for backup copy for IntelliSnap subclient

        Args:
            proxy_name(str) -- Name of the proxy to be used

        """
        if not isinstance(proxy_name, str):
            raise SDKException("Subclient", "101")

        properties_dict = {
            "clientName": proxy_name
        }

        update_properties = self.properties
        update_properties['commonProperties']['snapCopyInfo']['separateProxyForSnapToTape'] = properties_dict
        self.update_properties(update_properties)

    def unset_proxy_for_backup_copy(self):
        """ method to unset separate proxy server for backup copy for IntelliSnap subclient """

        properties_dict = {
            "clientId": 0
        }
        update_properties = self.properties
        update_properties['commonProperties']['snapCopyInfo']['separateProxyForSnapToTape'] = properties_dict
        self.update_properties(update_properties)

    def backup(self,
               backup_level: str = "Incremental",
               incremental_backup: bool = False,
               incremental_level: str = 'BEFORE_SYNTH',
               collect_metadata: bool = False) -> 'Job':
        """Run a backup job for the subclient at the specified backup level.

        This method initiates a backup operation for the subclient, allowing you to specify the backup level 
        and additional options for synthetic full backups.

        Args:
            backup_level: The level of backup to run. Supported values are:
                "Full", "Incremental", "Differential", "Synthetic_full".
                Defaults to "Incremental".
            incremental_backup: Whether to run an incremental backup as part of a synthetic full backup.
                Only applicable when backup_level is "Synthetic_full". Defaults to False.
            incremental_level: When to run the incremental backup relative to the synthetic full.
                Supported values: "BEFORE_SYNTH", "AFTER_SYNTH".
                Only applicable when backup_level is "Synthetic_full". Defaults to "BEFORE_SYNTH".
            collect_metadata: Whether to collect metadata during the backup. Defaults to False.

        Returns:
            Job: An instance of the Job class representing the initiated backup job.

        Raises:
            SDKException: If the specified backup level is invalid, or if the backup job fails to start.

        Example:
            >>> subclient = Subclient()
            >>> job = subclient.backup(backup_level="Full")
            >>> print(f"Backup job started with ID: {job.job_id}")

            >>> # Run a synthetic full backup with incremental before synth
            >>> job = subclient.backup(backup_level="Synthetic_full", incremental_backup=True, incremental_level="BEFORE_SYNTH")
            >>> print(f"Synthetic full backup job ID: {job.job_id}")

        #ai-gen-doc
        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'incremental', 'transaction_log',
                                'differential', 'synthetic_full']:
            raise SDKException('Subclient', '103')

        backup_request = backup_level

        if backup_level == 'synthetic_full':
            if incremental_backup:
                backup_request += '&runIncrementalBackup=True'
                backup_request += '&incrementalLevel=%s' % (
                    incremental_level.lower())
            else:
                backup_request += '&runIncrementalBackup=False'

        backup_request += '&collectMetaInfo=%s' % collect_metadata

        backup_service = self._services['SUBCLIENT_BACKUP'] % (
            self.subclient_id, backup_request)

        flag, response = self._cvpysdk_object.make_request(
            'POST', backup_service)

        return self._process_backup_response(flag, response)

    def get_ma_associated_storagepolicy(self) -> List[str]:
        """Retrieve the list of Media Agents associated with the storage policy for this subclient.

        Returns:
            List of Media Agent names associated with the storage policy.

        Raises:
            Exception: If unable to retrieve the Media Agent names.

        Example:
            >>> subclient = Subclient()
            >>> ma_list = subclient.get_ma_associated_storagepolicy()
            >>> print(f"Media Agents: {ma_list}")

        #ai-gen-doc
        """
        storage = self._subclient_properties['commonProperties']['storageDevice']
        if 'performanceMode' in storage:
            data_backup_storage_device = storage['performanceMode']["perfCRCDetails"]
            malist = []
            for each_ma in data_backup_storage_device:
                malist.append(each_ma['perfMa'])
            return malist

    def browse(self, *args: Any, **kwargs: Any) -> tuple[list, dict]:
        """Browse the content of the Subclient.

        This method allows you to explore the files and folders protected by the Subclient.
        You can specify browse options either as a single dictionary argument or as keyword arguments.
        The method returns a tuple containing a list of file/folder paths and a dictionary with detailed metadata.

        You can refer to the supported browse options in the `default_browse_options` documentation:
        https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        Examples:
            # Using a dictionary of browse options
            >>> result = subclient.browse({
            ...     'path': 'c:\\hello',
            ...     'show_deleted': True,
            ...     'from_time': '2014-04-20 12:00:00',
            ...     'to_time': '2016-04-21 12:00:00'
            ... })
            >>> file_list, metadata = result
            >>> print(file_list)
            >>> print(metadata)

            # Using keyword arguments for browse options
            >>> file_list, metadata = subclient.browse(
            ...     path='c:\\hello',
            ...     show_deleted=True,
            ...     from_time='2014-04-20 12:00:00',
            ...     to_time='2016-04-21 12:00:00'
            ... )
            >>> print(file_list)
            >>> print(metadata)

        Returns:
            tuple[list, dict]: 
                - list: List of file and folder paths from the browse response.
                - dict: Dictionary containing all paths with additional metadata from the browse operation.

        #ai-gen-doc
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['_subclient_id'] = kwargs.get('subclient_id', self._subclient_id)

        return self._backupset_object.browse(options)

    def find(self, *args: Any, **kwargs: Any) -> tuple[list, dict]:
        """Search for files or folders in the backed up content of the subclient.

        This method allows you to search for files and folders that match specified filters 
        within the subclient's backup content. You can provide search criteria either as a 
        dictionary of browse options or as keyword arguments.

        Supported options include:
            - file_name (str): Pattern to match file names (e.g., '*.txt').
            - show_deleted (bool): Whether to include deleted files in the results.
            - from_time (str): Start time for the search range (format: 'YYYY-MM-DD HH:MM:SS').
            - to_time (str): End time for the search range (format: 'YYYY-MM-DD HH:MM:SS').
            - file_size_gt (int): Find files with size greater than the specified value (in bytes).
            - file_size_lt (int): Find files with size less than the specified value (in bytes).
            - file_size_et (int): Find files with size equal to the specified value (in bytes).

        For a complete list of supported options, refer to the 
        `default_browse_options`_ documentation.

        Args:
            *args: Optional positional arguments. Typically, a single dictionary of browse options.
            **kwargs: Optional keyword arguments specifying browse options.

        Returns:
            tuple[list, dict]: 
                - A list of file and folder paths matching the search criteria.
                - A dictionary containing all matched paths with additional metadata from the browse operation.

        Example:
            >>> # Using a dictionary of browse options
            >>> results, metadata = subclient.find({
            ...     'file_name': '*.txt',
            ...     'show_deleted': True,
            ...     'from_time': '2022-01-01 00:00:00',
            ...     'to_time': '2022-12-31 23:59:59'
            ... })
            >>> print(f"Found {len(results)} .txt files")

            >>> # Using keyword arguments
            >>> results, metadata = subclient.find(
            ...     file_name='report_*.csv',
            ...     file_size_gt=1024,
            ...     show_deleted=False
            ... )
            >>> for path in results:
            ...     print(path)

        .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        #ai-gen-doc
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['_subclient_id'] = self._subclient_id

        return self._backupset_object.find(options)

    def list_media(self, *args: Any, **kwargs: Any) -> Union[List[Any], Dict[str, Any]]:
        """List the media required to browse and restore backed up data from the subclient.

        This method retrieves a list of all media needed for browsing and restoring data, 
        based on the provided options. Options can be supplied either as a single dictionary 
        argument or as keyword arguments.

        Args:
            *args: Optional positional arguments. Typically, a single dictionary containing 
                browse options such as 'path', 'show_deleted', 'from_time', and 'to_time'.
            **kwargs: Optional keyword arguments specifying browse options directly.

        Returns:
            Union[List[Any], Dict[str, Any]]: 
                - A list of all media required for the specified options.
                - A dictionary containing the total size of the media.

        Raises:
            SDKException: If the media listing fails or the response is not successful.

        Example:
            >>> # Using a dictionary of options
            >>> media_list, media_size = subclient.list_media({
            ...     'path': 'c:\\hello',
            ...     'show_deleted': True,
            ...     'from_time': '2020-04-20 12:00:00',
            ...     'to_time': '2021-04-19 12:00:00'
            ... })
            >>> print(f"Media required: {media_list}")
            >>> print(f"Total media size: {media_size}")

            >>> # Using keyword arguments
            >>> media_list, media_size = subclient.list_media(
            ...     path='c:\\hello',
            ...     show_deleted=True,
            ...     from_time='2020-04-20 12:00:00',
            ...     to_time='2021-04-19 12:00:00'
            ... )
            >>> print(f"Media required: {media_list}")
            >>> print(f"Total media size: {media_size}")

        Note:
            Refer to `_default_browse_options` in backupset.py for all supported options.

        #ai-gen-doc
        """

        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['_subclient_id'] = self._subclient_id

        return self._backupset_object.list_media(options)

    def restore_in_place(
            self,
            paths: list,
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: int = None,
            from_time: str = None,
            to_time: str = None,
            fs_options: dict = None,
            schedule_pattern: dict = None,
            proxy_client: str = None,
            advanced_options: dict = None
        ) -> object:
        """Restore files or folders to their original location on the client.

        This method restores the specified files or folders (provided in the `paths` list) to their original location
        on the client. You can control overwrite behavior, restore ACLs, specify copy precedence, set time filters,
        and provide advanced restore options. The restore can be performed immediately or scheduled for later execution.

        Args:
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs are restored. Default is True.
            copy_precedence: Optional storage policy copy precedence value. Default is None.
            from_time: Optional string specifying the start time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional string specifying the end time for restore (format: 'YYYY-MM-DD HH:MM:SS').
            fs_options: Optional dictionary of advanced file system restore options, such as:
                - all_versions (bool): Restore all versions of the specified file.
                - versions (list): List of version numbers to restore.
                - validate_only (bool): Validate data for restore without performing the restore.
            schedule_pattern: Optional dictionary specifying scheduling options for the restore job.
                Refer to `schedules.schedulePattern.createSchedule()` documentation for details.
            proxy_client: Optional string specifying the proxy client to use during NAS operations.
            advanced_options: Optional dictionary of advanced restore options, such as:
                - job_description (str): Description for the restore job.
                - timezone (str): Timezone to use for the restore. Use the TIMEZONES dict in constants.py.

        Returns:
            object: An instance of the Job class if the restore is immediate, or an instance of the Schedule class if the restore is scheduled.

        Raises:
            SDKException: If `paths` is not a list, if the job fails to initialize, if the response is empty, or if the response is not successful.

        Example:
            >>> subclient = Subclient()
            >>> restore_job = subclient.restore_in_place(
            ...     paths=['/data/file1.txt', '/data/folder2'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True,
            ...     from_time='2023-01-01 00:00:00',
            ...     to_time='2023-12-31 23:59:59',
            ...     fs_options={'all_versions': True},
            ...     advanced_options={'job_description': 'Restore job for year-end'}
            ... )
            >>> print(f"Restore job started: {restore_job}")

        #ai-gen-doc
        """
        self._instance_object._restore_association = self._subClientEntity

        if fs_options is None or not fs_options:
            fs_options = {}
            fs_options['no_of_streams'] = 10
        elif 'no_of_streams' not in fs_options:
            fs_options['no_of_streams'] = 10

        return self._instance_object._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            schedule_pattern=schedule_pattern,
            proxy_client=proxy_client,
            advanced_options=advanced_options
        )

    def restore_out_of_place(
            self,
            client: object,
            destination_path: str,
            paths: list,
            overwrite: bool = True,
            restore_data_and_acl: bool = True,
            copy_precedence: int = None,
            from_time: str = None,
            to_time: str = None,
            fs_options: dict = None,
            schedule_pattern: dict = None,
            proxy_client: str = None,
            advanced_options: dict = None
        ) -> object:
        """Restore specified files or folders to a different client and destination path.

        This method restores the files or folders listed in `paths` to the specified `destination_path`
        on the given `client`. It supports various options such as overwriting existing files, restoring
        data and ACLs, specifying copy precedence, time filters, advanced file system options, scheduling,
        proxy client, and additional advanced restore options.

        Args:
            client: The target client for restore. Can be a client name (str) or a Client object.
            destination_path: Full path on the destination client where data will be restored.
            paths: List of full file or folder paths to restore.
            overwrite: If True, existing files at the destination will be overwritten. Default is True.
            restore_data_and_acl: If True, both data and ACLs are restored. Default is True.
            copy_precedence: Optional; copy precedence value for storage policy copy.
            from_time: Optional; restore data backed up after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time: Optional; restore data backed up before this time (format: 'YYYY-MM-DD HH:MM:SS').
            fs_options: Optional; dictionary of advanced file system restore options (e.g., preserve_level, proxy_client, impersonate_user, all_versions, versions, media_agent, validate_only).
            schedule_pattern: Optional; dictionary specifying scheduling options for the restore job.
            proxy_client: Optional; proxy client name to use during restore (for NAS operations).
            advanced_options: Optional; dictionary of advanced restore options (e.g., job_description, timezone).

        Returns:
            object: An instance of the Job class if the restore is immediate, or an instance of the Schedule class if the restore is scheduled.

        Raises:
            SDKException: If input parameters are invalid or if the restore job fails to initialize or execute.

        Example:
            >>> # Restore files to a different client and path
            >>> subclient = Subclient()
            >>> job = subclient.restore_out_of_place(
            ...     client='TargetClient',
            ...     destination_path='/restore/location/',
            ...     paths=['/data/file1.txt', '/data/file2.txt'],
            ...     overwrite=True,
            ...     restore_data_and_acl=True
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        self._instance_object._restore_association = self._subClientEntity

        if fs_options and 'proxy_client' in fs_options:
            proxy_client = fs_options['proxy_client']

        # restore to use default 10 streams
        if fs_options is None or not fs_options:
            fs_options = {}
            fs_options['no_of_streams'] = 10
        elif 'no_of_streams' not in fs_options:
            fs_options['no_of_streams'] = 10

        return self._instance_object._restore_out_of_place(
            client=client,
            destination_path=destination_path,
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            schedule_pattern=schedule_pattern,
            proxy_client=proxy_client,
            advanced_options=advanced_options
        )

    def set_backup_nodes(self, data_access_nodes: list) -> None:
        """Set the backup nodes for an NFS share subclient.

        This method assigns the specified list of data access nodes as backup nodes for the NFS share subclient.

        Args:
            data_access_nodes: A list of data access node names or identifiers to be set as backup nodes.

        Example:
            >>> subclient = Subclient()
            >>> nodes = ['node1', 'node2', 'node3']
            >>> subclient.set_backup_nodes(nodes)
            >>> print("Backup nodes updated successfully.")

        Raises:
            SDKException: If unable to update the backup nodes for the subclient.

        #ai-gen-doc
        """
        data_access_nodes_json = []
        for access_node in data_access_nodes:
            data_access_nodes_json.append({"clientName": access_node})

        request_json = {
            "subClientProperties": {
                "fsSubClientProp": {
                    "backupConfiguration": {
                        "backupDataAccessNodes": data_access_nodes_json
                    }
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request('POST', self._SUBCLIENT, request_json)

        output = self._process_update_response(flag, response)

        if output[0]:
            return
        else:
            o_str = 'Failed to update properties of subclient\nError: "{0}"'
            raise SDKException('Subclient', '102', o_str.format(output[2]))

    def find_latest_job(
            self,
            include_active: bool = True,
            include_finished: bool = True,
            lookup_time: int = 1,
            job_filter: str = 'Backup,SYNTHFULL'
        ) -> 'Job':
        """Find the latest job for the subclient, including currently running jobs.

        This method retrieves the most recent job associated with the subclient, 
        optionally including active (running) and/or finished jobs, filtered by job type 
        and limited to jobs executed within a specified time window.

        Args:
            include_active: Whether to include active (currently running) jobs. Defaults to True.
            include_finished: Whether to include finished (completed) jobs. Defaults to True.
            lookup_time: The number of hours in the past to look for jobs. Defaults to 1 (last hour).
            job_filter: Comma-separated string specifying job types to include (e.g., 'Backup,SYNTHFULL').
                For a full list of possible job types, refer to:
                http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm

        Returns:
            Job: An instance of the Job class representing the latest job found for the subclient.

        Raises:
            SDKException: If an error occurs while finding the latest job.

        Example:
            >>> # Find the latest backup or synthetic full job in the last hour (default)
            >>> latest_job = subclient.find_latest_job()
            >>> print(f"Latest job ID: {latest_job.job_id}")
            >>>
            >>> # Find the latest restore job in the last 4 hours, including only finished jobs
            >>> latest_restore = subclient.find_latest_job(
            ...     include_active=False,
            ...     include_finished=True,
            ...     lookup_time=4,
            ...     job_filter='Restore'
            ... )
            >>> print(f"Latest restore job ID: {latest_restore.job_id}")

        #ai-gen-doc
        """
        job_controller = JobController(self._commcell_object)
        entity_dict = {
            "subclientId": int(self.subclient_id)
        }
        if include_active and include_finished:
            client_jobs = job_controller.all_jobs(
                client_name=self._client_object.client_name,
                lookup_time=lookup_time,
                job_filter=job_filter,
                entity=entity_dict
            )
        elif include_active:
            client_jobs = job_controller.active_jobs(
                client_name=self._client_object.client_name,
                lookup_time=lookup_time,
                job_filter=job_filter,
                entity=entity_dict
            )
        elif include_finished:
            client_jobs = job_controller.finished_jobs(
                client_name=self._client_object.client_name,
                lookup_time=lookup_time,
                job_filter=job_filter,
                entity=entity_dict
            )
        else:
            raise SDKException(
                'Subclient',
                '102',
                "Either active or finished job must be included"
            )

        latest_jobid = 0
        for job in client_jobs:
            if client_jobs[job]['subclient_id'] == int(self._subclient_id):
                if int(job) > latest_jobid:
                    latest_jobid = int(job)

        if latest_jobid == 0:
            raise SDKException('Subclient', '102', "No jobs found")

        return Job(self._commcell_object, latest_jobid)

    def run_content_indexing(self,
                            pick_failed_items: bool = False,
                            pick_only_failed_items: bool = False,
                            streams: int = 4,
                            proxies: Optional[list] = None) -> 'Job':
        """Run a content indexing job on the subclient.

        This method initiates a content indexing operation for the subclient, allowing you to specify
        whether to include failed items, only failed items, the number of streams, and optional proxies.

        Args:
            pick_failed_items: If True, include failed items from previous jobs in the content indexing operation. Default is False.
            pick_only_failed_items: If True, only failed items from previous jobs are included in the content indexing operation. Default is False.
            streams: The number of streams to use for the content indexing job. Default is 4.
            proxies: Optional list of proxies to use for running the content indexing job. Default is None.

        Returns:
            Job: An instance of the Job class representing the initiated content indexing job.

        Example:
            >>> # Run content indexing with default settings
            >>> job = subclient.run_content_indexing()
            >>> print(f"Started content indexing job: {job}")

            >>> # Run content indexing with custom streams and proxies
            >>> job = subclient.run_content_indexing(streams=8, proxies=['proxy1', 'proxy2'])
            >>> print(f"Started content indexing job with proxies: {job}")

        #ai-gen-doc
        """
        if not (isinstance(pick_failed_items, bool) and
                isinstance(pick_only_failed_items, bool)):
            raise SDKException('Subclient', '101')

        if proxies is None:
            proxies = {}

        self._media_option_json = {
            "pickFailedItems": pick_failed_items,
            "pickFailedItemsOnly": pick_only_failed_items,
            "auxcopyJobOption": {
                "maxNumberOfStreams": streams,
                "allCopies": True,
                "useMaximumStreams": False,
                "proxies": proxies
            }
        }

        self._content_indexing_option_json= {
            "reanalyze": False,
            "fileAnalytics": False,
            "subClientBasedAnalytics": False
        }
        self._subtask_restore_json = {
            "subTaskType": 1,
            "operationType": 5020
        }

        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": self._subtask_restore_json,
                        "options": {
                            "backupOpts": {
                                "mediaOpt": self._media_option_json
                            },
                            "adminOpts": {
                                "contentIndexingOption": self._content_indexing_option_json
                            },
                            "restoreOptions": {
                                "virtualServerRstOption": {
                                    "isBlockLevelReplication": False
                                },
                                "browseOption": {
                                    "backupset": {}
                                }
                            }
                        }
                    }
                ]
            }
        }

        return self._process_restore_response(request_json)

    def refresh(self) -> None:
        """Reload the properties of the Subclient to reflect the latest state.

        This method updates the Subclient's internal properties by fetching the most recent
        information from the Commcell or associated data source. Use this method if you suspect
        that the Subclient's configuration has changed outside of the current object instance.

        Example:
            >>> subclient = Subclient()
            >>> subclient.refresh()
            >>> print("Subclient properties refreshed successfully")

        #ai-gen-doc
        """
        self._get_subclient_properties()
        self.schedules = Schedules(self)

    @property
    def software_compression(self) -> bool:
        """Get the current status of software compression for the Subclient.

        Returns:
            bool: True if software compression is enabled, False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> is_enabled = subclient.software_compression
            >>> print(f"Software compression enabled: {is_enabled}")

        #ai-gen-doc
        """
        mapping = {
            0: 'ON_CLIENT',
            1: 'ON_MEDIAAGENT',
            2: 'USE_STORAGE_POLICY_SETTINGS',
            4: 'OFF'
        }

        try:
            return mapping[self._commonProperties['storageDevice']['softwareCompression']]
        except KeyError:
            return self._commonProperties['storageDevice']['softwareCompression']

    @software_compression.setter
    def software_compression(self, value: str) -> None:
        """Set the software compression setting for the subclient.

        Args:
            value: The desired software compression setting. Valid values are:
                - "ON_CLIENT"
                - "ON_MEDIAAGENT"
                - "USE_STORAGE_POLICY_SETTINGS"
                - "OFF"

        Raises:
            SDKException: If the update fails or if the input value is not a string.

        Example:
            >>> subclient.software_compression = "ON_CLIENT"
            >>> # The software compression for the subclient is now set to "ON_CLIENT"

        #ai-gen-doc
        """
        if isinstance(value, str):
            self._set_subclient_properties(
                "_commonProperties['storageDevice']['softwareCompression']", value
            )
        else:
            raise SDKException('Subclient', '101')

    @property
    def network_agent(self) -> bool:
        """Get the status of the network agents setting for the Subclient.

        Returns:
            bool: True if network agents are enabled for the Subclient, False otherwise.

        Example:
            >>> subclient = Subclient()
            >>> is_enabled = subclient.network_agent  # Use dot notation for property access
            >>> print(f"Network agents enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._commonProperties['storageDevice']['networkAgents']

    @network_agent.setter
    def network_agent(self, value: int) -> None:
        """Set the number of network agents for the subclient.

        Args:
            value: The number of network agents to assign to the subclient. Must be an integer.

        Raises:
            SDKException: If updating the network agents fails, or if the provided value is not an integer.

        Example:
            >>> subclient = Subclient()
            >>> subclient.network_agent = 4  # Sets the number of network agents to 4
            >>> print("Network agents updated successfully.")

        #ai-gen-doc
        """

        if isinstance(value, int):
            self._set_subclient_properties("_commonProperties['storageDevice']['networkAgents']", value)
        else:
            raise SDKException('Subclient', '101')

    @property
    def encryption_flag(self) -> int:
        """Get the encryption flag setting for the Subclient.

        Returns:
            int: The current value of the encryption flag for this Subclient.

        Example:
            >>> subclient = Subclient()
            >>> flag = subclient.encryption_flag
            >>> print(f"Encryption flag value: {flag}")

        #ai-gen-doc
        """
        mapping = {
            0: 'ENC_NONE',
            1: 'ENC_MEDIA_ONLY',
            2: 'ENC_NETWORK_AND_MEDIA',
            3: 'ENC_NETWORK_ONLY'
        }

        try:
            return mapping[self._commonProperties['encryptionFlag']]
        except KeyError:
            return self._commonProperties['encryptionFlag']

    @encryption_flag.setter
    def encryption_flag(self, value: str) -> None:
        """Set the encryption flag for the subclient.

        This setter updates the encryption flag of the subclient to the specified value.
        Valid values for the encryption flag are:
            - ENC_NONE
            - ENC_MEDIA_ONLY
            - ENC_NETWORK_AND_MEDIA
            - ENC_NETWORK_ONLY

        Args:
            value: The encryption flag value to set. Must be one of the valid values listed above.

        Raises:
            SDKException: If the encryption flag update fails or if the input value is not a string.

        Example:
            >>> subclient = Subclient()
            >>> subclient.encryption_flag = "ENC_NETWORK_AND_MEDIA"  # Use assignment for property setter
            >>> print("Encryption flag updated successfully")

        #ai-gen-doc
        """

        if isinstance(value, str):
            self._set_subclient_properties("_commonProperties['encryptionFlag']", value)
        else:
            raise SDKException('Subclient', '101')

    @property
    def deduplication_options(self) -> dict:
        """Get the deduplication options settings for this Subclient.

        Returns:
            dict: A dictionary containing the deduplication options configured for the Subclient.

        Example:
            >>> subclient = Subclient(commcell_object, client_name, agent_name, instance_name, backupset_name, subclient_name)
            >>> dedup_options = subclient.deduplication_options  # Use dot notation for property access
            >>> print("Deduplication options:", dedup_options)
            >>> # The returned dictionary contains deduplication settings such as mode, thresholds, and other relevant options

        #ai-gen-doc
        """
        mapping_dedupe = {
            0: False,
            1: True,
        }
        mapping_signature = {
            1: "ON_CLIENT",
            2: "ON_MEDIA_AGENT"
        }

        dedupe_options = self._commonProperties['storageDevice']['deDuplicationOptions']

        if "enableDeduplication" in dedupe_options:
            if dedupe_options['enableDeduplication'] == 0:
                return mapping_dedupe[dedupe_options['enableDeduplication']]
            else:
                if 'generateSignature' in dedupe_options:
                    try:
                        return mapping_signature[dedupe_options['generateSignature']]
                    except KeyError:
                        return dedupe_options['generateSignature']

    @deduplication_options.setter
    def deduplication_options(self, enable_dedupe: tuple) -> None:
        """Enable or disable deduplication options for the Subclient.

        Args:
            enable_dedupe: A tuple specifying deduplication settings.
                - The first element (bool): Set to True to enable deduplication, False to disable.
                - The second element (str or None): Specifies where to generate the signature.
                    Valid values are:
                        - "ON_CLIENT"
                        - "ON_MEDIA_AGENT"
                    Use None if not applicable.

        Raises:
            SDKException: If updating deduplication options fails or if the input type is incorrect.

        Example:
            >>> subclient.deduplication_options = (False, None)
            >>> subclient.deduplication_options = (True, "ON_CLIENT")
            >>> subclient.deduplication_options = (True, "ON_MEDIA_AGENT")

        #ai-gen-doc
        """
        if enable_dedupe[0] is True:
            if enable_dedupe[1] is not None:
                self._set_subclient_properties(
                    "_commonProperties['storageDevice']['deDuplicationOptions']",
                    {
                        "enableDeduplication": enable_dedupe[0],
                        "generateSignature": enable_dedupe[1]
                    }
                )
            else:
                raise SDKException('Subclient', '102', "Input data is not correct")
        else:
            self._set_subclient_properties(
                "_commonProperties['storageDevice']['deDuplicationOptions']",
                {
                    "enableDeduplication": enable_dedupe[0],
                }
            )

    @property
    def plan(self) -> Optional[str]:
        """Get the name of the plan associated with this subclient.

        Returns:
            The name of the plan as a string if a plan is associated, or None if no plan is set.

        Example:
            >>> subclient = Subclient()
            >>> plan_name = subclient.plan  # Use dot notation for property access
            >>> if plan_name:
            >>>     print(f"Subclient is associated with plan: {plan_name}")
            >>> else:
            >>>     print("No plan is associated with this subclient.")

        #ai-gen-doc
        """

        if 'planEntity' in self._subclient_properties:
            planEntity = self._subclient_properties['planEntity']

            if bool(planEntity) and 'planName' in planEntity:
                return planEntity['planName']
            else:
                return None
        else:
            raise SDKException('Subclient', '112')

    @plan.setter
    def plan(self, value: 'Union[object, str, None]') -> None:
        """Associate or remove a plan from the subclient.

        This setter allows you to associate a plan with the subclient by providing either a Plan object,
        the name of the plan as a string, or remove the association by setting the value to None.

        Args:
            value: The plan to associate with the subclient. This can be:
                - A Plan object to associate with the subclient.
                - A string representing the name of the plan to associate.
                - None to remove any existing plan association.

        Raises:
            SDKException: If the input type is incorrect or if the plan association fails.

        Example:
            >>> subclient = Subclient()
            >>> plan_obj = Plan('DailyBackup')
            >>> subclient.plan = plan_obj  # Associate using a Plan object
            >>> subclient.plan = "WeeklyBackup"  # Associate using a plan name
            >>> subclient.plan = None  # Remove plan association

        #ai-gen-doc
        """
        from .plan import Plan
        if isinstance(value, Plan):
            if self._commcell_object.plans.has_plan(value.plan_name):
                self.update_properties({
                    'planEntity': {
                        'planName': value.plan_name
                    },
                    "useContentFromPlan": True
                })
            else:
                raise SDKException('Subclient', '102', 'Plan does not exist')
        elif isinstance(value, str):
            if self._commcell_object.plans.has_plan(value):
                self.update_properties({
                    'planEntity': {
                        'planName': value
                    },
                    "useContentFromPlan": True
                })
            else:
                raise SDKException('Subclient', '102', 'Plan does not exist')
                
        elif value is None:
            self.update_properties({
                'removePlanAssociation': True
            })
        else:
            raise SDKException('Subclient', '101')

    @property
    def additional_settings(self) -> AdditionalSettings:
        """Returns the AdditionalSettings instance for managing additional settings on this subclient.

        This property provides access to the AdditionalSettings API for the subclient entity,
        allowing you to add, edit, delete, and retrieve additional settings specific to this subclient.

        Returns:
            AdditionalSettings: An instance of the AdditionalSettings class for this subclient.

        Example:
            >>> subclient = self.agent.instances.get("instance_name").backupsets.get("backupset_name").subclients.get("subclient_name")
            >>> subclient.additional_settings.add_additional_setting(
            ...     key_name="",
            ...     category="",
            ...     data_type="",
            ...     value="",
            ...     comment="",
            ...     enabled=True
            ... )
        """
        try:
            self._additional_settings = AdditionalSettings(self)
        except Exception as e:
            raise SDKException('Subclient', '102', 
                'Failed to initialize AdditionalSettings: "{0}"'.format(str(e)))
        return self._additional_settings

    def _get_preview_metadata(self, file_path: str) -> Optional[dict]:
        """Retrieve the preview metadata for a specified file in the subclient.

        Args:
            file_path: The path to the file for which preview metadata is required.

        Returns:
            A dictionary containing the metadata content of the preview if the file is found.
            Returns None if the specified file does not exist.

        Example:
            >>> subclient = Subclient()
            >>> metadata = subclient._get_preview_metadata('/data/documents/report.pdf')
            >>> if metadata is not None:
            ...     print("Preview metadata:", metadata)
            ... else:
            ...     print("File not found or no metadata available.")

        #ai-gen-doc
        """

        paths, data = self.find()

        for path in paths:
            if path.lower() == file_path.lower():
                return data[path]
        else:
            return None

    def _get_preview(self, file_path: str) -> str:
        """Retrieve the HTML preview content for a specified file in the subclient.

        Args:
            file_path: The path to the file for which the preview content is to be retrieved.

        Returns:
            The HTML content of the file preview as a string.

        Raises:
            SDKException: If the file is not found, the response is empty, or the response is not successful.

        Example:
            >>> subclient = Subclient()
            >>> html_content = subclient._get_preview('/documents/report.pdf')
            >>> print(html_content)
            # The output will be the HTML preview of the specified file.

        #ai-gen-doc
        """
        metadata = self._get_preview_metadata(file_path)
        if metadata is None:
            raise SDKException('Subclient', '123')

        if metadata["type"] != "File":
            raise SDKException('Subclient', '124')

        if metadata["size"] == 0:
            raise SDKException('Subclient', '125')

        if metadata["size"] > 20 * 1024 * 1024:
            raise SDKException('Subclient', '126')

        request_json = {
            "filters": [
                {
                    "field": "CONTENTID",
                    "fieldValues": {
                        "values": [

                        ]
                    }
                },
                {
                    "field": "COMMCELL_NUMBER",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["advConfig"]["browseAdvancedConfigResp"][
                                    "commcellNumber"])
                        ]
                    }
                },
                {
                    "field": "CLIENT_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["sourceCommServer"]["commCellId"])
                        ]
                    }
                },
                {
                    "field": "SUBCLIENT_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["subclient"]["applicationId"])
                        ]
                    }
                },
                {
                    "field": "MODIFIED_TIME",
                    "fieldValues": {
                        "values": [
                            metadata["modified_time"]
                        ]
                    }
                },
                {
                    "field": "ITEM_PATH",
                    "fieldValues": {
                        "values": [
                            file_path
                        ]
                    }
                },
                {
                    "field": "ITEM_SIZE",
                    "fieldValues": {
                        "values": [
                            str(metadata["size"])
                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_ID",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["archiveFileId"])
                        ]
                    }
                },
                {
                    "field": "ARCHIVE_FILE_OFFSET",
                    "fieldValues": {
                        "values": [
                            str(metadata["advanced_data"]["offset"])
                        ]
                    }
                }
            ]
        }

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._PREVIEW_CONTENT, request_json)

        if flag:
            if "Preview not available" not in response.text:
                return response.text
            else:
                raise SDKException('Subclient', '127')
        else:
            raise SDKException('Subclient', '102', self._update_response_(response.text))