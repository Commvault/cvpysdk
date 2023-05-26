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
from .job import Job
from .client import Client
from .exception import SDKException


class CommCellMigration(object):
    """Class for representing the commcell export & import operations from commcell. """

    def __init__(self, commcell_object):
        """Initializes object of the CommCellMigration class.

            Args:
               commcell_object (object) -instance of the commcell class

            Returns:
               object - instance of the CommCellMigration class
        """

        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_
        self._commcell_name = self._commcell_object.commserv_name
        self._path_type = 0

    def commcell_export(self, export_location, client_list=None, options_dictionary=None, other_entities=None):
        """ Starts the Commcell Export job.

            Args:
                export_location     ( str )         --  Location to export generated dumps.

                client_list         ( list )        --  Contains list of clients used for export.
                    [
                        "Server_1","Client1","Client2"
                    ]

                options_dictionary  ( dict )        --  Contains options used to perform CCM Export.
                    {
                        "pathType":"Local",

                        "otherSqlInstance":True,

                        "userName":"UserName",

                        "password":"User#####",

                        "otherSqlInstance": False,

                        "sqlInstanceName":"SQLInstanceName",

                        "sqlUserName":"SQLUserName",

                        "sqlPassword":"SQLPassword",

                        "Database":"commserv",

                        "captureMediaAgents":True,
                        
                        "captureSchedules":True,

                        "captureActivityControl":True,

                        "captureOperationWindow":True,

                        "captureHolidays":True,

                        "csName": "CommservName",  # host cs for using sql instance export

                        "clientIds": [client_id1, client_id2],  # required only when exporting clients using sql instance

                        "autopickCluster":False
                    }
                
                other_entities      ( list )        --  list of other entities to be exporteddd
                    [
                        "schedule_policies",

                        "users_and_user_groups",

                        "alerts"
                    ]   

            Returns:
                CCM Export Job instance             --  returns the CCM Export job instance.

            Raises:
                SDKException:
                    if type of the input is not valid.

                    if all the required inputs are not provided.

                    if invalid inputs are passed.
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
                for client in client_list:
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

    def commcell_import(self, import_location, options_dictionary):
        """ Starts the Commcell Import job.

            Args:
                import_location     ( str )         --  Location to import the generated dumps.

                options_dictionary  ( dict )        --  Contains list of options used for CCMImport and default values.
                    {
                        "pathType": "Network",
                        "userName" : "username",
                        "password": "password",
                        "forceOverwrite": False,
                        "failIfEntityAlreadyExists": False,
                        "deleteEntitiesNotPresent": False,
                        "deleteEntitiesIfOnlyfromSource": False,
                        "forceOverwriteHolidays": False,
                        "mergeHolidays": True,
                        "forceOverwriteOperationWindow": False,
                        "mergeOperationWindow": False,
                        "forceOverwriteSchedule": False,
                        "mergeSchedules": True
                    }

            Returns:
                CCM Import Job instance             --  returns the CCM Import job instance.

            Raises:
                SDKException:
                    if type of the input is not valid.

                    if all the required inputs are not provided.

                    if invalid inputs are passed.
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

    def tape_import(self, library_id, medias_id, drive_pool_id):

        """ performs the tape import import operation for the specified tape.

            Args:
                library_id      (int)       --      tape library id.

                medias_id        (list)       --      tape id.

                drive_pool_id   (int)       --      drive pool id

            Returns:
                Tape import job instance
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
    """Class for representing the GRC feature from commcell"""

    def __init__(self, commcell_object):
        """
        Initializes the object of GlobalRepositoryCell class

        Args:
            commcell_object (Commcell)  -   Commcell class instance

        Returns:
            grc (GlobalRepositoryCell) - instance of the GlobalRepositoryCell class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._commcell_name = self._commcell_object.commserv_name

    def _get_task_details(self, task_id):
        """
        Util for getting XML of GRC schedule task (required for generating more XMLs)

        Args:
            task_id     (int)   -   id of grc schedule's task

        Returns:
            task_xml    (str)   -   xml form string with grc schedule details
            Example:
                <TMMsg_GetTaskDetailResp>
	                <taskInfo>
		                <task taskId="" taskName="" > ... </task>
                        <appGroup/>
                        <subTasks>
                            <subTask subTaskId="" subTaskType="" ...>
                            <options>
                                <backupOpts backupLevel="">
                                    <dataOpt autoCopy=""/>
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
                        </subTasks>
                    </taskInfo>
                </TMMsg_GetTaskDetailResp>
        """
        get_task_xml = f'<TMMsg_GetTaskDetailReq taskId="{task_id}"/>'
        return self._commcell_object.qoperation_execute(get_task_xml, return_xml=True)

    def _get_commcell_from_id(self, commcell_id):
        """
        Util to get registered commcell name from given commcell id

        Args:
            commcell_id (int)   -   id of commcell

        Returns:
            commcell_name   (str)   -   name of commcell
        """
        for commcell_name, commcell_data in self._commcell_object.registered_commcells.items():
            if commcell_data.get('commCell', {}).get('commCellId') == commcell_id:
                return commcell_name

    def _modify_task_props(self, podcell_properties, task_xml):
        """
        Util for modifying task properties, after grc properties are updated

        Args:
            podcell_properties  (dict)  -   the dict returned by get_podcell_properties
            task_xml    (str)           -   the xml returned for grc schedule's task info

        Returns:
            response    (dict)   -   the response from execute qoperation
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

    def _get_podcell_entities(self, podcell_name: str = None, podcell_id: int = None):
        """
        Gets the entities in podcell available for monitoring via GRC

        Args:
            podcell_name    (str)   -   name of pod cell
            podcell_id      (int)   -   id of podcell

        Returns:
            monitor_entities    (str)   -   all entities of pod cell in XML format
            Example:
                <EVGui_CCMCommCellInfo commcellName="" commcellNumber="" commcellId="">
                    <clientEntityLst clientId="" clientName="">
                        ...
                    </clientEntityLst>
                    <clientEntityLst clientId="" clientName="">
                        ...
                    </clientEntityLst>
                    <clientEntityLst clientId="" ...>
                        <appTypeEntityList ... appTypeId="">
                            <instanceList ... instanceId="">
                                <backupSetList ... backupsetId="">
                                    <subclientList ... subclientId=""/>
                                </backupSetList>
                            </instanceList>
                        </appTypeEntityList>
                    </clientEntityLst>
                    <clientComputerGrp clientGroupId="" clientGroupName=""/>
                    ...
                    <clientComputerGrp clientGroupId="" clientGroupName=""/>
                </EVGui_CCMCommCellInfo>
        """
        if podcell_id is None:
            if podcell_name is None:
                raise SDKException('GlobalRepositoryCell', '103')
            podcell_id = self._commcell_object.registered_commcells.get(podcell_name, {}) \
                .get('commCell', {}).get('commCellId')
            if podcell_id is None:
                raise SDKException('GlobalRepositoryCell', '104', f'for podcell: {podcell_name}')
        podcell_name = self._get_commcell_from_id(podcell_id)
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

    def get_clients_for_migration(self, podcell_name: str = None, podcell_id: int = None):
        """
        Gets the podcell clients that can be migrated
        
        Args:
            podcell_name    (str)   -   name of pod cell
            podcell_id      (int)   -   id of podcell
        
        Returns:
            clients_dict    (dict)  -   dict with client ID as key and client name value
            Example:
                {
                    X: "clientA",
                    Y: "clientB",
                    Z: "clienta"
                }
        """
        clients_dict = {}
        entities_xml = self._get_podcell_entities(
            podcell_name=podcell_name,
            podcell_id=podcell_id
        )
        entities_xml = ET.fromstring(entities_xml)
        for client_node in entities_xml.findall('clientEntityLst'):
            cl_id = client_node.get('clientId')
            cl_name = client_node.get('clientName')
            clients_dict[cl_id] = cl_name
        return clients_dict

    def _get_podcell_properties(self, podcell_name: str = None, podcell_id: int = None):
        """
        Gets the GRC properties of given pod cell

        Args:
            podcell_name    (str)   -   name of pod cell
            podcell_id      (int)   -   id of podcell

        Returns:
            podcell_properties  (dict)  -   different properties of pod cell in dict format with xml values
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

    def modify_monitored_clients(self, podcell_name: str = None, podcell_id: int = None, clients: list = None):
        """
        Modifies (overwrites) the monitored clients in grc properties for given podcell

        Args:
            podcell_name    (str)   -   name of pod cell
            podcell_id      (int)   -   id of podcell
            client_ids      (list)  -   list of client ids, names
                                        or Client objects (of pod cell)

        Returns:
            None
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
