# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Class to perform all the CommCell Migration operations on commcell

CommCellMigration is the only class defined in this file.

CommCellMigration: Helper class to perform CommCell Import & Export operations.

CommCellMigration:

    __init__()                      --  initializes CommCellMigration helper object.

    commcell_export()               --  function to run CCM Export operation.

    commcell_import()               --  function to run CCM Import operation.

"""
from base64 import b64encode
from past.builtins import basestring
from .job import Job

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

    def commcell_export(self, export_location, client_list, options_dictionary=None):
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

                        "password":"UserPassword!12",

                        "sqlInstanceName":"SQLInstanceName",

                        "sqlUserName":"SQLUserName",

                        "sqlPassword":"SQLPassword",

                        "Database":"commserv",

                        "captureMediaAgents":True,

                        "autopickCluster":False
                    }

            Returns:
                CCM Export Job instance             --  returns the CCM Export job instance.

            Raises:
                SDKException:
                    if type of the input is not valid.

                    if all the required inputs are not provided.

                    if invalid inputs are passed.
        """

        path_type = options_dictionary.get("pathType", "Local")
        network_user_name = options_dictionary.get("userName", "")
        network_user_password = options_dictionary.get("password", "")
        other_sql_instance = options_dictionary.get("otherSqlInstance", False)
        sql_instance_name = options_dictionary.get("sqlInstanceName", "")
        sql_user_name = options_dictionary.get("sqlUserName", "")
        sql_password = options_dictionary.get("sqlPassword", "")
        database = options_dictionary.get("Database", "commserv")
        capture_ma = options_dictionary.get("captureMediaAgents", True)
        auto_pick_cluster = options_dictionary.get("autopickCluster", False)

        if not (isinstance(path_type, basestring)
                and isinstance(network_user_name, basestring)
                and isinstance(network_user_password, basestring)
                and isinstance(other_sql_instance, bool)
                and isinstance(sql_instance_name, basestring)
                and isinstance(export_location, basestring)
                and isinstance(sql_user_name, basestring)
                and isinstance(sql_password, basestring)
                and isinstance(database, basestring)
                and isinstance(capture_ma, bool)
                and isinstance(auto_pick_cluster, bool)):
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

        if self._path_type == 1:
            if network_user_name == "" or network_user_password == "":
                raise SDKException('CommCellMigration', '103')
            network_user_password = b64encode(network_user_password.encode()).decode()

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
                                    "commonOptions": {
                                        "otherSqlInstance": other_sql_instance,
                                        "pathType": self._path_type,
                                        "dumpFolder": export_location,
                                        "splitCSDB": 1,
                                        "userAccount": {
                                            "password": network_user_password,
                                            "userName": network_user_name
                                        },
                                        "sqlLinkedServer": {
                                            "sqlServerName": sql_instance_name,
                                            "sqlUserAccount": {
                                                "userName": sql_user_name,
                                                "password": sql_password
                                            }
                                        }
                                    },
                                    "captureOptions": {
                                        "captureMediaAgents": capture_ma,
                                        "lastHours": 60,
                                        "remoteDumpDir": "",
                                        "remoteCSName": "",
                                        "pruneExportedDump": False,
                                        "autopickCluster": auto_pick_cluster,
                                        "copyDumpToRemoteCS": False,
                                        "useJobResultsDirForExport": False,
                                        "captureFromDB": {
                                            "csName": self._commcell_name,
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

        sub_dict = export_json['taskInfo']['subTasks'][0]['options']['adminOpts']['ccmOption'] \
            ['captureOptions']['entities']

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

                options_dictionary  ( dict )        --  Contains list of options used for CCMImport.
                    {
                        "pathType":"Local",

                        "userName":"sa"

                        "password":"password"
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

        if not (isinstance(path_type, basestring) and isinstance(import_location, basestring)):
            raise SDKException('CommCellMigration', '101')

        if path_type.lower() == 'local':
            self._path_type = 0
        elif path_type.lower() == 'network':
            self._path_type = 1
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
                                        "forceOverwriteHolidays": False,
                                        "reuseTapes": False,
                                        "specifyStagingPath": False,
                                        "forceOverwriteOperationWindow": False,
                                        "fallbackSpareGroup": "",
                                        "mergeOperationWindow": False,
                                        "pruneImportedDump": False,
                                        "alwaysUseFallbackDataPath": True,
                                        "deleteEntitiesNotPresent": False,
                                        "forceOverwrite": False,
                                        "mergeHolidays": True,
                                        "forceOverwriteSchedule": False,
                                        "fallbackDrivePool": "",
                                        "mergeActivityControl": True,
                                        "fallbackMediaAgent": "",
                                        "mergeSchedules": True,
                                        "failIfEntityAlreadyExists": False,
                                        "fallbackLibrary": "",
                                        "skipConflictMedia": False,
                                        "stagingPath": ""
                                    },
                                    "commonOptions": {
                                        "bRoboJob": False,
                                        "databaseConfiguredRemote": False,
                                        "pathType": self._path_type,
                                        "dumpFolder": import_location,
                                        "splitCSDB": 0,
                                        "userAccount": {
                                            "password": network_user_password,
                                            "userName": network_user_name
                                        }
                                    }
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
