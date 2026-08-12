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

"""Class to perform all the CommCell Migration operations on commcell

CommCellMigration, GlobalRepositoryCell are the only classes defined in this file.

CommCellMigration: Helper class to perform CommCell Import & Export operations.

CommCellMigration:

    __init__()                      --  initializes CommCellMigration helper object.

    commcell_export()               --  function to run CCM Export operation.

    commcell_import()               --  function to run CCM Import operation.

    tape_import()                   --  function to run tape import operation.

GlobalRepositoryCell: Helper class to perform GRC related operations

GlobalRepositoryCell:

    __init__()                      --  initializes GlobalRepositoryCell object

    get_podcell_entities()          --  gets all entities from registered podcell that can be imported

    get_podcell_properties()        --  gets all grc related properties for registered podcell

    modify_monitored_clients()      --  overwrites imported clients in podcell grc schedule

"""
import html
import xml.etree.ElementTree as ET
from base64 import b64encode
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .client import Client
from .exception import SDKException
from .job import Job

if TYPE_CHECKING:
    from .commcell import Commcell

class CommCellMigration(object):
    """
    Class for managing CommCell export and import operations.

    This class provides a comprehensive interface for handling the migration of data and configurations
    between CommCell environments. It supports exporting CommCell data, importing data back into a CommCell,
    and importing tapes into the system. The class is initialized with a CommCell object and offers flexible
    options for specifying export/import locations, client lists, and additional entities or options.

    Key Features:
        - Export CommCell data to a specified location with customizable options and client/entity selection
        - Import CommCell data from a given location with configurable options
        - Import tapes into the CommCell using library, media, and drive pool identifiers
        - Centralized management of CommCell migration tasks

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a new instance of the CommCellMigration class.

        Args:
            commcell_object: An instance of the Commcell class representing the source or target Commcell.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> migration = CommCellMigration(commcell)
            >>> print("CommCellMigration object created successfully")

        #ai-gen-doc
        """

        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_
        self._commcell_name = self._commcell_object.commserv_name
        self._path_type = 0

    def commcell_export(
        self,
        export_location: str,
        client_list: Optional[List[str]] = None,
        options_dictionary: Optional[Dict[str, Any]] = None,
        other_entities: Optional[List[str]] = None
    ) -> 'Job':
        """Start a Commcell Export job to export configuration and client data.

        This method initiates a Commcell Export job, which exports configuration data, client information,
        and other selected entities to the specified export location. You can customize the export by
        specifying a list of clients, additional export options, and other entities to include.

        Args:
            export_location: The file system path where the exported dumps will be saved.
            client_list: Optional list of client names to include in the export.
                Example: ["Server_1", "Client1", "Client2"]
            options_dictionary: Optional dictionary of export options to control export behavior.
                Example:
                    {
                        "pathType": "Local",
                        "otherSqlInstance": True,
                        "userName": "UserName",
                        "password": "...",
                        "sqlInstanceName": "SQLInstanceName",
                        "sqlUserName": "SQLUserName",
                        "sqlPassword": "...",
                        "Database": "commserv",
                        "captureMediaAgents": True,
                        "captureSchedules": True,
                        "captureActivityControl": True,
                        "captureOperationWindow": True,
                        "captureHolidays": True,
                        "csName": "CommservName",
                        "clientIds": [123, 456],
                        "autopickCluster": False
                    }
            other_entities: Optional list of additional entities to export, such as schedule policies,
                users and user groups, or alerts.
                Example: ["schedule_policies", "users_and_user_groups", "alerts"]

        Returns:
            Job: An instance representing the initiated Commcell Export job.

        Raises:
            SDKException: If input types are invalid, required inputs are missing, or invalid values are provided.

        Example:
            >>> export_options = {
            ...     "pathType": "Local",
            ...     "captureMediaAgents": True,
            ...     "captureSchedules": True
            ... }
            >>> job = commcell_migration.commcell_export(
            ...     export_location="/exports/commcell",
            ...     client_list=["ClientA", "ClientB"],
            ...     options_dictionary=export_options,
            ...     other_entities=["alerts"]
            ... )
            >>> print(f"Export job started with ID: {job.job_id}")

        #ai-gen-doc
        """

        if client_list is None and other_entities is None:
            raise SDKException('CommCellMigration', '105')

        options_dictionary = options_dictionary or {}

        path_type = options_dictionary.get("pathType", "Local")
        network_user_name = options_dictionary.get("userName", "")
        network_user_password = options_dictionary.get("password", "")
        other_sql_instance = options_dictionary.get("otherSqlInstance", False)
        sql_instance_name = options_dictionary.get("sqlInstanceName", "")
        sql_user_name = options_dictionary.get("sqlUserName", "")
        sql_password = options_dictionary.get("sqlPassword", "")
        database = options_dictionary.get("Database", "Commserv")
        capture_ma = options_dictionary.get("captureMediaAgents", True)
        capture_schedules = options_dictionary.get("captureSchedules", True)
        capture_activity_control = options_dictionary.get("captureActivityControl", True)
        capture_opw = options_dictionary.get("captureOperationWindow", True)
        capture_holidays = options_dictionary.get("captureHolidays", True)
        auto_pick_cluster = options_dictionary.get("autopickCluster", False)
        cs_name = options_dictionary.get("csName", self._commcell_name)
        client_ids = options_dictionary.get("clientIds", [])

        if not (isinstance(path_type, str)
                and isinstance(network_user_name, str)
                and isinstance(network_user_password, str)
                and isinstance(other_sql_instance, bool)
                and isinstance(sql_instance_name, str)
                and isinstance(export_location, str)
                and isinstance(sql_user_name, str)
                and isinstance(sql_password, str)
                and isinstance(database, str)
                and isinstance(capture_ma, bool)
                and isinstance(capture_schedules, bool)
                and isinstance(capture_activity_control, bool)
                and isinstance(capture_opw, bool)
                and isinstance(capture_holidays, bool)
                and isinstance(auto_pick_cluster, bool)
                and isinstance(cs_name, str)
                and isinstance(client_ids, list)):
            raise SDKException('CommCellMigration', '101')

        if path_type.lower() == 'local':
            self._path_type = 0
        elif path_type.lower() == 'network':
            self._path_type = 1
        else:
            raise SDKException('CommCellMigration', '104')

        if other_sql_instance:
            if sql_instance_name == "" or sql_user_name == "" or sql_password == "":
                raise SDKException('CommCellMigration', '103')
            sql_password = b64encode(sql_password.encode()).decode()

        common_options = {
            "otherSqlInstance": other_sql_instance,
            "pathType": self._path_type,
            "dumpFolder": export_location,
            "splitCSDB": 1,
            "sqlLinkedServer": {
                "sqlServerName": sql_instance_name,
                "sqlUserAccount": {
                    "userName": sql_user_name,
                    "password": sql_password
                }
            }
        }

        if self._path_type == 1:
            if network_user_name == "" or network_user_password == "":
                raise SDKException('CommCellMigration', '103')
            network_user_password = b64encode(network_user_password.encode()).decode()
            common_options["userAccount"] = {
                "password": network_user_password,
                "userName": network_user_name
            }

        export_json = {
            "taskInfo": {
                "task": {
                    "taskType": 1,
                    "isEditing": False,
                    "initiatedFrom": 2,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "appGroup": {
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4029
                        },
                        "options": {
                            "adminOpts": {
                                "ccmOption": {
                                    "commonOptions": common_options,
                                    "captureOptions": {
                                        "captureMediaAgents": capture_ma,
                                        "lastHours": 60,
                                        "remoteDumpDir": "",
                                        "remoteCSName": "",
                                        "captureSchedules": capture_schedules,
                                        "captureActivityControl": capture_activity_control,
                                        "captureOperationWindow": capture_opw,
                                        "captureHolidays": capture_holidays,
                                        "pruneExportedDump": False,
                                        "autopickCluster": auto_pick_cluster,
                                        "copyDumpToRemoteCS": False,
                                        "useJobResultsDirForExport": False,
                                        "captureFromDB": {
                                            "csName": cs_name,
                                            "csDbName": database
                                        },
                                        "entities": [
                                        ],
                                        "timeRange": {
                                            "_type_": 54,
                                        }
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }

        if not other_sql_instance:
            del export_json['taskInfo']['subTasks'][0]['options']['adminOpts']['ccmOption'] \
                ['captureOptions']['captureFromDB']

        sub_dict = export_json['taskInfo']['subTasks'][0]['options']['adminOpts']['ccmOption'] \
            ['captureOptions']['entities']

        if other_entities:
            for entity in other_entities:
                if entity == "schedule_policies":
                    sub_dict.append({'commCellName': self._commcell_name, "_type_": 34})

                elif entity == "users_and_user_groups":
                    sub_dict.append({'commCellName': self._commcell_name, "_type_": 36})

                elif entity == "alerts":
                    sub_dict.append({'commCellName': self._commcell_name, "_type_": 42})

        if client_list:
            if other_sql_instance:
                if not sql_instance_name \
                        or not sql_user_name \
                        or not sql_password \
                        or not client_ids:
                    raise SDKException('CommCellMigration', '106')

                for index, client in enumerate(client_list):
                    temp_dic = {'clientName': client, "clientId": client_ids[index]}
                    sub_dict.append(temp_dic)

            else:
                exportable_clients = list(self._commcell_object.grc.get_clients_for_migration(
                    podcell_id=2, podcell_guid=self._commcell_object.commserv_guid
                ).values())
                for client in client_list:
                    if not self._commcell_object.clients.has_client(client):
                        raise SDKException(
                            'CommCellMigration', '107',
                            f'Client {client} not found'
                        )
                    agents = self._commcell_object.clients.get(client).agents.all_agents
                    if not agents:
                        raise SDKException(
                            'CommCellMigration', '107',
                            f'Client {client} does not have any agents'
                        )
                    temp_dic = {'clientName': client, 'commCellName': self._commcell_name}
                    sub_dict.append(temp_dic)

        flag, response = self._cvpysdk_object.make_request('POST',
                                                           self._services['RESTORE'],
                                                           export_json)

        if flag:
            if response.json() and 'jobIds' in response.json():
                return Job(self._commcell_object, response.json()['jobIds'][0])
            elif response.json() and 'errorCode' in response.json():
                raise SDKException('CommCellMigration', '102', 'CCM Export job failed with error code : ' +
                                   str(response.json()['errorCode']))
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def commcell_import(self, import_location: str, options_dictionary: dict) -> 'Job':
        """Start a Commcell Import job using the specified import location and options.

        This method initiates the Commcell Import process, importing generated dumps from the given location
        with the provided options. The options dictionary allows customization of the import behavior, such as
        overwriting existing entities, merging schedules, and specifying authentication details.

        Args:
            import_location: The file system or network path where the generated dumps are located for import.
            options_dictionary: A dictionary containing options for the import job. Example keys include:
                - "pathType": Type of the path (e.g., "Network").
                - "userName": Username for authentication.
                - "password": Password for authentication.
                - "forceOverwrite": Whether to force overwrite existing entities.
                - "failIfEntityAlreadyExists": Fail if the entity already exists.
                - "deleteEntitiesNotPresent": Delete entities not present in the import.
                - "deleteEntitiesIfOnlyfromSource": Delete entities only if present in the source.
                - "forceOverwriteHolidays": Force overwrite holidays.
                - "mergeHolidays": Merge holidays.
                - "forceOverwriteOperationWindow": Force overwrite operation window.
                - "mergeOperationWindow": Merge operation window.
                - "forceOverwriteSchedule": Force overwrite schedule.
                - "mergeSchedules": Merge schedules.

        Returns:
            Job: An instance representing the initiated Commcell Import job.

        Raises:
            SDKException: If the input types are invalid, required inputs are missing, or invalid options are provided.

        Example:
            >>> import_options = {
            ...     "pathType": "Network",
            ...     "userName": "admin",
            ...     "password": "password123",
            ...     "forceOverwrite": True,
            ...     "mergeSchedules": True
            ... }
            >>> migration = CommCellMigration(commcell_object)
            >>> job = migration.commcell_import("/mnt/ccm_dumps", import_options)
            >>> print(f"Started import job with ID: {job.job_id}")

        #ai-gen-doc
        """
        path_type = options_dictionary.get("pathType", "Local")
        network_user_name = options_dictionary.get("userName", "")
        network_user_password = options_dictionary.get("password", "")
        force_overwrite = options_dictionary.get('forceOverwrite', False)
        fail_if_entry_already_exists = options_dictionary.get('failIfEntityAlreadyExists', False)
        delete_entities_not_present = options_dictionary.get('deleteEntitiesNotPresent', False)
        delete_only_source = options_dictionary.get('deleteEntitiesIfOnlyfromSource', False)
        fo_holidays = options_dictionary.get("forceOverwriteHolidays", False)
        merge_holidays = options_dictionary.get("mergeHolidays", True)
        fo_operation_window = options_dictionary.get("forceOverwriteOperationWindow", False)
        merge_operation_window = options_dictionary.get("mergeOperationWindow", False)
        fo_schedules = options_dictionary.get("forceOverwriteSchedule", False)
        merge_schedules = options_dictionary.get("mergeSchedules", True)

        if not (isinstance(path_type, str) and isinstance(import_location, str)):
            raise SDKException('CommCellMigration', '101')

        common_options = {
            "bRoboJob": False,
            "databaseConfiguredRemote": False,
            "pathType": self._path_type,
            "dumpFolder": import_location,
            "splitCSDB": 0
        }

        if path_type.lower() == 'local':
            self._path_type = 0
        elif path_type.lower() == 'network':
            self._path_type = 1
            common_options["userAccount"] = {
                "password": network_user_password,
                "userName": network_user_name
            }
        else:
            raise SDKException('CommCellMigration', '104')

        if self._path_type == 1:
            if network_user_name == "" or network_user_password == "":
                raise SDKException('CommCellMigration', '103')

        import_json = {
            "taskInfo": {
                "associations": [
                    {
                        "type": 0,
                        "clientSidePackage": True,
                        "consumeLicense": True
                    }
                ],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 1,
                            "operationType": 4030
                        },
                        "options": {
                            "adminOpts": {
                                "ccmOption": {
                                    "mergeOptions": {
                                        "deleteEntitiesIfOnlyfromSource": False,
                                        "forceOverwriteHolidays": fo_holidays,
                                        "reuseTapes": False,
                                        "specifyStagingPath": False,
                                        "forceOverwriteOperationWindow": fo_operation_window,
                                        "fallbackSpareGroup": "",
                                        "mergeOperationWindow": merge_operation_window,
                                        "pruneImportedDump": False,
                                        "alwaysUseFallbackDataPath": True,
                                        "deleteEntitiesNotPresent": delete_entities_not_present,
                                        "deleteEntitiesIfOnlyfromSource": delete_only_source,
                                        "forceOverwrite": force_overwrite,
                                        "mergeHolidays": merge_holidays,
                                        "forceOverwriteSchedule": fo_schedules,
                                        "fallbackDrivePool": "",
                                        "mergeActivityControl": True,
                                        "fallbackMediaAgent": "",
                                        "mergeSchedules": merge_schedules,
                                        "failIfEntityAlreadyExists": fail_if_entry_already_exists,
                                        "fallbackLibrary": "",
                                        "skipConflictMedia": False,
                                        "stagingPath": ""
                                    },
                                    "commonOptions": common_options
                                }
                            }
                        }
                    }
                ]
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST',
                                                           self._services['RESTORE'],
                                                           import_json)

        if flag:
            if response.json() and 'jobIds' in response.json():
                return Job(self._commcell_object, response.json()['jobIds'][0])
            elif response.json() and 'errorCode' in response.json():
                raise SDKException('CommCellMigration', '102', 'CCM Import job failed with error code : ' +
                                   str(response.json()['errorCode']))
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def tape_import(self, library_id: int, medias_id: list, drive_pool_id: int) -> 'Job':
        """Perform a tape import operation for the specified tape.

        Args:
            library_id: The ID of the tape library to use for the import.
            medias_id: A list of tape media IDs to be imported.
            drive_pool_id: The ID of the drive pool to use for the import operation.

        Returns:
            Job: An instance representing the initiated tape import job.

        Example:
            >>> migration = CommCellMigration()
            >>> job = migration.tape_import(library_id=5, medias_id=[101, 102], drive_pool_id=2)
            >>> print(f"Tape import job started: {job}")

        #ai-gen-doc
        """

        tape_import_json = {
            "taskInfo": {
                "associations": [
                ], "task": {
                    "ownerId": 1, "taskType": 1, "ownerName": "admin", "sequenceNumber": 0, "initiatedFrom": 1,
                    "policyType": 0, "taskId": 0, "taskFlags": {
                        "disabled": False
                    }
                }, "subTasks": [
                    {
                        "subTask": {
                            "subTaskType": 1, "operationType": 4017
                        },
                        "options": {
                            "adminOpts": {
                                "contentIndexingOption": {
                                    "subClientBasedAnalytics": False
                                }, "libraryOption": {
                                    "operation": 15, "media": [
                                    ], "library": {
                                        "libraryName": "", "_type_": 9, "libraryId": library_id
                                    }, "catalogMedia": {
                                        "fileMarkerToStart": 0, "fileMarkerToEnd": 0, "reCatalog": True,
                                        "maxNumOfDrives": 1,
                                        "spareGroupId": 0,
                                        "merge": True,
                                        "subTaskType": 2,
                                        "drivePoolEntity": {
                                            "_type_": 47, "drivePoolId": drive_pool_id
                                        }
                                    }, "mediaAgent": {
                                        "mediaAgentId": 2, "_type_": 11
                                    }
                                }
                            }, "restoreOptions": {
                                "virtualServerRstOption": {
                                    "isBlockLevelReplication": False
                                }, "commonOptions": {
                                    "syncRestore": False
                                }
                            }
                        }
                    }
                ]
            }
        }

        sub_dict = tape_import_json["taskInfo"]["subTasks"][0]["options"]["adminOpts"]["libraryOption"]["media"]

        for media in medias_id:
            temp_dict = {"_type_": 46, "mediaId": int(media), "mediaName": ""}
            sub_dict.append(temp_dict)

        flag, response = self._cvpysdk_object.make_request('POST',
                                                           self._services['RESTORE'],
                                                           tape_import_json)

        if flag:
            if response.json() and 'jobIds' in response.json():
                return Job(self._commcell_object, response.json()['jobIds'][0])
            elif response.json() and 'errorCode' in response.json():
                raise SDKException('CommCellMigration', '102', 'Tape Import job failed with error code : ' +
                                   str(response.json()['errorCode']))
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

class GlobalRepositoryCell:
    """
    Represents the Global Repository Cell (GRC) feature within a Commcell environment.

    This class provides an interface for managing and interacting with GRC-related
    entities and operations in a Commcell. It enables retrieval and modification of
    podcell properties, task details, and monitored clients, as well as facilitating
    client migration processes.

    Key Features:
        - Initialize with a Commcell object for context
        - Retrieve details of specific tasks by task ID
        - Obtain Commcell information using Commcell ID
        - Modify properties of tasks and podcells using provided configurations
        - Fetch entities and properties associated with podcells
        - Get clients eligible for migration within a podcell
        - Modify the list of monitored clients for a podcell

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a new instance of the GlobalRepositoryCell class.

        Args:
            commcell_object: An instance of the Commcell class representing the Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> grc = GlobalRepositoryCell(commcell)
            >>> print(f"GlobalRepositoryCell object created: {grc}")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._commcell_name = self._commcell_object.commserv_name

    def _get_task_details(self, task_id: int) -> str:
        """Retrieve the XML details of a Global Repository Cell (GRC) schedule task.

        This utility method fetches the XML representation of a GRC schedule task, which is 
        required for generating additional XMLs or for further processing of schedule details.

        Args:
            task_id: The unique identifier (ID) of the GRC schedule's task.

        Returns:
            A string containing the XML representation of the GRC schedule task details.

        Example:
            >>> grc_cell = GlobalRepositoryCell()
            >>> xml_details = grc_cell._get_task_details(12345)
            >>> print(xml_details)
            <TMMsg_GetTaskDetailResp>
                <taskInfo>
                    <task taskId="12345" taskName="DailyBackup"> ... </task>
                    <appGroup/>
                    <subTasks>
                        <subTask subTaskId="67890" subTaskType="Backup" ...>
                            <options>
                                <backupOpts backupLevel="Full">
                                    <dataOpt autoCopy="true"/>
                                </backupOpts>
                                <adminOpts>
                                    <ccmOption>
                                        <mergeOptions ...>
                                        <captureOptions ...>
                                            ...
                                        </captureOptions>
                                    </ccmOption>
                                </adminOpts>
                            </options>
                            <pattern ...>...</pattern>
                        </subTask>
                    </subTasks>
                </taskInfo>
            </TMMsg_GetTaskDetailResp>

        #ai-gen-doc
        """
        get_task_xml = f'<TMMsg_GetTaskDetailReq taskId="{task_id}"/>'
        return self._commcell_object.qoperation_execute(get_task_xml, return_xml=True)

    def _get_commcell_from_id(self, commcell_id: int) -> str:
        """Retrieve the registered Commcell name corresponding to the given Commcell ID.

        Args:
            commcell_id: The unique integer identifier of the Commcell.

        Returns:
            The name of the Commcell as a string.

        Example:
            >>> grc = GlobalRepositoryCell()
            >>> commcell_name = grc._get_commcell_from_id(1024)
            >>> print(f"Commcell name: {commcell_name}")

        #ai-gen-doc
        """
        for commcell_name, commcell_data in self._commcell_object.registered_commcells.items():
            if commcell_data.get('commCell', {}).get('commCellId') == commcell_id:
                return commcell_name

    def _modify_task_props(self, podcell_properties: dict, task_xml: str) -> dict:
        """Modify task properties after Global Repository Cell (GRC) properties are updated.

        This utility updates the task properties using the provided podcell properties and task XML.
        It is typically used after GRC properties have been changed to ensure the associated task
        reflects the latest configuration.

        Args:
            podcell_properties: Dictionary containing properties returned by `get_podcell_properties`.
            task_xml: XML string representing the task information for the GRC schedule.

        Returns:
            Dictionary containing the response from the qoperation execution.

        Example:
            >>> podcell_props = grc.get_podcell_properties()
            >>> task_xml = grc.get_task_xml()
            >>> response = grc._modify_task_props(podcell_props, task_xml)
            >>> print(response)
            {'status': 'success', 'taskId': 1234}

        #ai-gen-doc
        """
        grc_schedule_xml = ET.fromstring(podcell_properties['schedule_xml'])
        task_info_xml = ET.fromstring(task_xml)
        modify_task_xml = """
        <TMMsg_ModifyTaskReq>
            <taskInfo>
                <task initiatedFrom="1" ownerId="{0}" ownerName="{1}" policyType="0" sequenceNumber="0" taskId="{2}" taskType="2">
                    <taskFlags disabled="0" isEZOperation="0" isEdgeDrive="0"/>
                </task>
                <appGroup/>
                {3}
            </taskInfo>
        </TMMsg_ModifyTaskReq>
        """
        modify_task_xml = modify_task_xml.format(
            grc_schedule_xml.find('taskInfo/task').get('ownerId'),
            grc_schedule_xml.find('taskInfo/task').get('ownerName'),
            podcell_properties['task_id'],
            ET.tostring(task_info_xml.find('taskInfo/subTasks'), encoding='unicode')
        )
        return self._commcell_object.qoperation_execute(modify_task_xml)

    def _get_podcell_entities(self, podcell_name: str = None, podcell_id: int = None, podcell_guid: str = None) -> str:
        """Retrieve the entities within a specified podcell that are available for monitoring via the Global Repository Cell (GRC).

        At least one of `podcell_name`, `podcell_id`, or `podcell_guid` should be provided to identify the target podcell.
        The returned data is an XML string describing all entities (clients, groups, applications, etc.) within the podcell.

        Args:
            podcell_name: The name of the podcell to query. Optional if `podcell_id` or `podcell_guid` is provided.
            podcell_id: The unique integer ID of the podcell. Optional if `podcell_name` or `podcell_guid` is provided.
            podcell_guid: The GUID of the podcell. Optional if `podcell_name` or `podcell_id` is provided.

        Returns:
            An XML string containing all entities of the specified podcell, structured for monitoring purposes.

        Example:
            >>> grc = GlobalRepositoryCell()
            >>> xml_entities = grc._get_podcell_entities(podcell_name="PodCellA")
            >>> print(xml_entities)
            <EVGui_CCMCommCellInfo commcellName="PodCellA" commcellNumber="..." commcellId="...">
                <clientEntityLst clientId="..." clientName="...">
                    ...
                </clientEntityLst>
                <clientComputerGrp clientGroupId="..." clientGroupName="..."/>
                ...
            </EVGui_CCMCommCellInfo>

        #ai-gen-doc
        """
        if podcell_id is None:
            if podcell_name is None:
                raise SDKException('GlobalRepositoryCell', '103')
            podcell_id = self._commcell_object.registered_commcells.get(podcell_name, {}) \
                .get('commCell', {}).get('commCellId')
            if podcell_id is None:
                raise SDKException('GlobalRepositoryCell', '104', f'for podcell: {podcell_name}')
        if podcell_name is None:
            podcell_name = self._get_commcell_from_id(podcell_id)
        if podcell_guid is None:
            podcell_guid = self._commcell_object.registered_commcells[podcell_name].get('commCell', {}).get('csGUID')

        entities_xml = """
        <EVGui_GetCCMExportInfo exportMsgType="3" strCSName="{0}*{0}*8400">
            <mediaAgent _type_="3"/>
            <userInfo/>
            <commCell _type_="1" commCellId="{1}" commCellName="{0}" csGUID="{2}"/>
        </EVGui_GetCCMExportInfo>
        """
        exec_xml = entities_xml.format(podcell_name, podcell_id, podcell_guid)
        resp = self._commcell_object.qoperation_execute(exec_xml)
        return resp.get('strXmlInfo')

    def get_clients_for_migration(self, podcell_name: Optional[str] = None, podcell_id: Optional[int] = None, podcell_guid: Optional[str] = None) -> Dict[int, str]:
        """Retrieve the clients from a specified podcell that are eligible for migration.

        Args:
            podcell_name: The name of the podcell from which to retrieve clients. Optional if podcell_id or podcell_guid is provided.
            podcell_id: The unique identifier of the podcell. Optional if podcell_name or podcell_guid is provided.
            podcell_guid: The GUID of the podcell. Optional if podcell_name or podcell_id is provided.

        Returns:
            A dictionary mapping client IDs (as integers) to client names (as strings) for clients that can be migrated.

        Example:
            >>> grc = GlobalRepositoryCell()
            >>> clients = grc.get_clients_for_migration(podcell_name="PodCell1")
            >>> print(clients)
            {101: "clientA", 102: "clientB", 103: "clientC"}

        #ai-gen-doc
        """
        clients_dict = {}
        entities_xml = self._get_podcell_entities(
            podcell_name=podcell_name,
            podcell_id=podcell_id,
            podcell_guid=podcell_guid
        )
        entities_xml = ET.fromstring(entities_xml)
        for client_node in entities_xml.findall('clientEntityLst'):
            cl_id = client_node.get('clientId')
            cl_name = client_node.get('clientName')
            clients_dict[cl_id] = cl_name
        return clients_dict

    def _get_podcell_properties(self, podcell_name: Optional[str] = None, podcell_id: Optional[int] = None) -> Dict[str, Any]:
        """Retrieve the Global Repository Cell (GRC) properties for a specified pod cell.

        This method fetches various properties of a pod cell, either by its name or ID. The returned
        dictionary contains property values, which may include XML-formatted data.

        Args:
            podcell_name: Optional; The name of the pod cell to retrieve properties for.
            podcell_id: Optional; The unique identifier of the pod cell.

        Returns:
            Dictionary containing the properties of the specified pod cell, with values in XML format.

        Example:
            >>> grc = GlobalRepositoryCell()
            >>> properties = grc._get_podcell_properties(podcell_name="PodCellA")
            >>> print(properties)
            >>> # Or fetch by ID
            >>> properties = grc._get_podcell_properties(podcell_id=12345)
            >>> print(properties)

        #ai-gen-doc
        """
        # TODO: Update grc properties map
        grc_prop_map = {
            2: 'podcell_name',
            4: 'schedule_xml',
            15: 'entities_xml',
            16: 'libraries_xml',
            19: 'task_id'
        }
        if podcell_id is None:
            if podcell_name is None:
                raise SDKException('GlobalRepositoryCell', '103')
            podcell_id = self._commcell_object.registered_commcells.get(podcell_name, {}) \
                .get('commCell', {}).get('commCellId')
            if podcell_id is None:
                raise SDKException('GlobalRepositoryCell', '104', f'for podcell: {podcell_name}')
        grc_props_xml = f'<App_GetGRCCommCellPropsReq commcellId="{podcell_id}"/>'
        grc_props_response = self._commcell_object.qoperation_execute(grc_props_xml)
        podcell_properties = {
            grc_prop_map.get(prop.get('propId'), prop.get('propId')): prop.get('stringVal') or prop.get('numVal')
            for prop in grc_props_response['grcCommcellPropList']
        }
        return podcell_properties

    def modify_monitored_clients(self, podcell_name: Optional[str] = None, podcell_id: Optional[int] = None, clients: Optional[list] = None) -> None:
        """Modify (overwrite) the monitored clients in the Global Repository Cell (GRC) properties for a specified pod cell.

        This method updates the list of monitored clients for the given pod cell, replacing any existing monitored clients with the provided list.

        Args:
            podcell_name: The name of the pod cell to update. Optional if podcell_id is provided.
            podcell_id: The ID of the pod cell to update. Optional if podcell_name is provided.
            clients: A list containing client IDs, client names, or Client objects (belonging to the pod cell) to set as monitored.

        Example:
            >>> grc = GlobalRepositoryCell()
            >>> # Overwrite monitored clients using podcell name and client names
            >>> grc.modify_monitored_clients(podcell_name="PodCellA", clients=["client1", "client2"])
            >>>
            >>> # Overwrite monitored clients using podcell ID and client IDs
            >>> grc.modify_monitored_clients(podcell_id=123, clients=[101, 102, 103])
            >>>
            >>> # Overwrite monitored clients using Client objects
            >>> grc.modify_monitored_clients(podcell_name="PodCellB", clients=[client_obj1, client_obj2])

        #ai-gen-doc
        """
        if podcell_id is None:
            if podcell_name is None:
                raise SDKException('GlobalRepositoryCell', '103')
            podcell_id = self._commcell_object.registered_commcells.get(podcell_name, {}) \
                .get('commCell', {}).get('commCellId')
            if podcell_id is None:
                raise SDKException('GlobalRepositoryCell', '104', f'for podcell: {podcell_name}')

        set_grc_xml = """
            <App_SetGRCCommCellPropsReq commcellId="{0}">
                <grcCommcellProp numVal="0" propId="4" stringVal="{1}"/>
                <grcCommcellProp numVal="1" propId="1" stringVal=""/>
                <grcCommcellProp numVal="0" propId="2" stringVal="{2}"/>
                <grcCommcellProp numVal="0" propId="15" stringVal="{3}"/>
                <grcCommcellProp numVal="1" propId="8" stringVal=""/>
                <grcCommcellProp numVal="0" propId="14" stringVal=""/>
            </App_SetGRCCommCellPropsReq>
        """
        xml_header = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
        cc_props = self._get_podcell_properties(podcell_id=podcell_id)
        podcell_name = cc_props['podcell_name']
        task_xml = self._get_task_details(task_id=cc_props['task_id'])
        podcell_entities = self._get_podcell_entities(podcell_id=podcell_id)
        entities_xml = ET.fromstring(podcell_entities)
        client_ids = []
        if isinstance(clients[0], str):
            for client_node in entities_xml.findall('clientEntityLst'):
                if client_node.get('clientName') in clients:
                    client_ids.append(client_node.get('clientId'))
        elif isinstance(clients[0], int):
            client_ids = clients
        elif isinstance(clients[0], Client):
            client_ids = [int(cl.client_id) for cl in clients]

        # Generate nested XML 1 (selected clients)
        current_schedule = ET.fromstring(cc_props['schedule_xml'])
        capture_options = current_schedule.find('taskInfo/subTasks/options/adminOpts/ccmOption/captureOptions')
        # remove all <entities ...> tags
        for entity_node in capture_options.findall('entities'):
            capture_options.remove(entity_node)
        # insert <entities ...> tags for selected client_ids
        for clid in client_ids:
            capture_options.insert(0, ET.Element('entities', {'clientId': str(clid), '_type_': '3'}))
        nested_xml1 = ET.tostring(current_schedule, encoding='unicode')
        nested_xml1 = html.escape(f'{xml_header}{nested_xml1}')

        # Generate nested XML 2 (all clients in podcell)
        entities_xml = ET.fromstring(podcell_entities)
        nested_xml2 = ET.tostring(entities_xml, encoding='unicode')
        nested_xml2 = html.escape(nested_xml2)

        # Combine nested XMLs into parent XML
        final_xml = set_grc_xml.format(podcell_id, nested_xml1, podcell_name, nested_xml2)
        self._commcell_object.qoperation_execute(final_xml)
        self._modify_task_props(cc_props, task_xml)