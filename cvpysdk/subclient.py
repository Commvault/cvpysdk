# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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

    default_subclient()         --  returns the name of the default subclient

    all_subclients()            --  returns dict of all the subclients on commcell

    has_subclient()             --  checks if a subclient exists with the given name or not

    add()                       --  adds a new subclient to the backupset

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

    _json_task()                --  setter for task property

    _json_restore_subtask()     --  setter for sub task property

    _association_json()         --  setter for association property

    description()               --  update the description of the subclient

    content()                   --  update the content of the subclient

    enable_backup()             --  enables the backup for the subclient

    enable_trueup()             --  enables true up option for the subclient

    enable_trueup_days()        --  enables true up option and sets days for backup

    enable_backup_at_time()     --  enables backup for the subclient at the input time specified

    disble_backup()             --  disables the backup for the subclient

    backup()                    --  run a backup job for the subclient

    browse()                    --  gets the content of the backup for this subclient
    at the path specified

    browse_in_time()            --  gets the content of the backup for this subclient
    at the input path in the time range specified

    find()                      --  searches a given file/folder name in the subclient content

    restore_in_place()          --  Restores the files/folders specified in the
    input paths list to the same location

    restore_out_of_place()      --  Restores the files/folders specified in the input paths list
    to the input client, at the specified destionation location

    set_backup_nodes()          -- Set Backup Nodes for NFS Share Pseudo client's subclient.

    find_latest_job()           --  Finds the latest job for the subclient
    which includes current running job also.

    refresh()                   --  refresh the properties of the subclient


Subclient Instance Attributes:
==============================

    **snapshot_engine_name**            --  returns snapshot engine name associated
    with the subclient

    **is_default_subclient**            --  returns True if the subclient is default
    subclient else returns False

    **is_blocklevel_backup_enabled**    --  returns True if block level backup is enabled

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import math
import time

from past.builtins import basestring
from future.standard_library import install_aliases

from .job import Job
from .job import JobController
from .schedules import Schedules
from .exception import SDKException
from .schedules import SchedulePattern
from .schedules import Schedule

install_aliases()


class Subclients(object):
    """Class for getting all the subclients associated with a client."""

    def __init__(self, class_object):
        """Initialize the Subclients object for the given backupset.

            Args:
                class_object    (object)    --  instance of the Agent / Instance / Backupset class

            Returns:
                object  -   instance of the Subclients class

            Raises:
                SDKException:
                    if class object is not an instance of Agent / Instance / Backupset

        """
        from .agent import Agent
        from .instance import Instance
        from .backupset import Backupset

        self._agent_object = None
        self._instance_object = None
        self._backupset_object = None

        if isinstance(class_object, Agent):
            self._agent_object = class_object

        elif isinstance(class_object, Instance):
            self._instance_object = class_object
            self._agent_object = self._instance_object._agent_object

        elif isinstance(class_object, Backupset):
            self._backupset_object = class_object
            self._instance_object = class_object._instance_object
            self._agent_object = self._instance_object._agent_object

        else:
            raise SDKException('Subclient', '115')

        self._client_object = self._agent_object._client_object
        self._commcell_object = self._agent_object._commcell_object

        self._cvpysdk_object = self._commcell_object._cvpysdk_object
        self._services = self._commcell_object._services
        self._update_response_ = self._commcell_object._update_response_

        self._SUBCLIENTS = self._services['GET_ALL_SUBCLIENTS'] % (
            self._client_object.client_id)

        self._ADD_SUBCLIENT = self._services['ADD_SUBCLIENT']

        self._default_subclient = None

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
        from .subclients.vminstancesubclient import VMInstanceSubclient
        from .subclients.db2subclient import DB2Subclient
        from .subclients.casesubclient import CaseSubclient

        globals()['BigDataAppsSubclient'] = BigDataAppsSubclient
        globals()['FileSystemSubclient'] = FileSystemSubclient
        globals()['VirtualServerSubclient'] = VirtualServerSubclient
        globals()['CloudAppsSubclient'] = CloudAppsSubclient
        globals()['SQLServerSubclient'] = SQLServerSubclient
        globals()['NASSubclient'] = NASSubclient
        globals()['SAPHANASubclient'] = SAPHANASubclient
        globals()['OracleSubclient'] = OracleSubclient
        globals()['LNDbSubclient'] = LNDbSubclient
        globals()['LNDocSubclient'] = LNDocSubclient
        globals()['LNDmSubclient'] = LNDmSubclient
        globals()['SybaseSubclient'] = SybaseSubclient
        globals()['SAPOracleSubclient'] = SAPOracleSubclient
        globals()['ExchangeSubclient'] = ExchangeSubclient
        globals()['MYSQLSubclient'] = MYSQLSubclient
        globals()['ExchangeDatabaseSubclient'] = ExchangeDatabaseSubclient
        globals()['PostgresSubclient'] = PostgresSubclient
        globals()['DB2Subclient'] = DB2Subclient
        globals()['InformixSubclient'] = InformixSubclient
        globals()['ADSubclient'] = ADSubclient
        globals()['SharepointSubclient'] = SharepointSubclient
        globals()['VMInstanceSubclient'] = VMInstanceSubclient
        globals()['CaseSubclient'] = CaseSubclient

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        self._subclients_dict = {
            'big data apps': BigDataAppsSubclient,
            'file system': FileSystemSubclient,
            'virtual server': [VirtualServerSubclient, VMInstanceSubclient],
            'cloud apps': CloudAppsSubclient,
            'sql server': SQLServerSubclient,
            'nas': NASSubclient,        # SP11 or lower CS honors NAS as the Agent Name
            'ndmp': NASSubclient,       # SP12 and above honors NDMP as the Agent Name
            'sap hana': SAPHANASubclient,
            'oracle': OracleSubclient,
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
            'sharepoint server': SharepointSubclient
        }

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

    def __str__(self):
        """Representation string consisting of all subclients of the backupset.

            Returns:
                str - string of all the subclients of th backupset of an agent of a client
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

    def __repr__(self):
        """Representation string for the instance of the Subclients class."""
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

    def __len__(self):
        """Returns the number of the subclients associated to the Agent for the selected Client."""
        return len(self.all_subclients)

    def __getitem__(self, value):
        """Returns the name of the subclient for the given subclient ID or
            the details of the subclient for given subclient Name.

            Args:
                value   (str / int)     --  Name or ID of the subclient

            Returns:
                str     -   name of the subclient, if the subclient id was given

                dict    -   dict of details of the subclient, if subclient name was given

            Raises:
                IndexError:
                    no subclient exists with the given Name / Id

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

    def _get_subclients(self):
        """Gets all the subclients associated to the client specified by the backupset object.

            Returns:
                dict - consists of all subclients in the backupset
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
                SDKException:
                    if response is empty

                    if response is not success
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
    def all_subclients(self):
        """Returns dict of all the subclients configured on this backupset

            Retruns:
                dict    -   consists of all subclients in the backupset

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

        """
        return self._subclients

    def has_subclient(self, subclient_name):
        """Checks if a subclient exists in the commcell with the input subclient name.

            Args:
                subclient_name (str)  --  name of the subclient

            Returns:
                bool - boolean output whether the subclient exists in the backupset or not

            Raises:
                SDKException:
                    if type of the subclient name argument is not string
        """
        if not isinstance(subclient_name, basestring):
            raise SDKException('Subclient', '101')

        return self._subclients and subclient_name.lower() in self._subclients

    def add(self, subclient_name, storage_policy,
            subclient_type=None, description='', advanced_options=None,
            pre_scan_cmd=None):
        """Adds a new subclient to the backupset.

            Args:
                subclient_name      (str)   --  name of the new subclient to add

                storage_policy      (str)   --  name of the storage policy to be associated
                with the subclient

                subclient_type      (str)   --  type of subclient for sql server

                    default: None

                    Valid Values are:

                        - DATABASE

                        - FILE_FILEGROUP


                description         (str)   --  description for the subclient (optional)

                    default: ''

                advanced_options    (dict)  --  dict of additional options needed to create
                                                subclient with additional properties
                                                default : None
                    Example:
                        {
                            ondemand_subclient : True
                        }

                pre_scan_cmd        (str)   --  path to the batch file/shell script file to run
                                                before each backup of the subclient

            Returns:
                object  -   instance of the Subclient class

            Raises:
                SDKException:
                    if subclient name argument is not of type string

                    if storage policy argument is not of type string

                    if description argument is not of type string

                    if failed to create subclient

                    if response is empty

                    if response is not success

                    if subclient already exists with the given name

        """
        if not (isinstance(subclient_name, basestring) and
                isinstance(storage_policy, basestring) and
                isinstance(description, basestring)):
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

        if not self._commcell_object.storage_policies.has_policy(
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
        if pre_scan_cmd is not None:
            request_json["subClientProperties"]["commonProperties"]["prepostProcess"] = \
                {
                "runAs": 1,
                "preScanCommand": pre_scan_cmd,
            }

        if self._agent_object.agent_name == 'sql server':
            request_json['subClientProperties']['mssqlSubClientProp'] = {
                'sqlSubclientType': self._sqlsubclient_type_dict[subclient_type]
            }

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
                        'Failed to create subclient\nError: "{0}"'.format(
                            error_string)
                    )
                else:
                    subclient_id = response.json(
                    )['response']['entity']['subclientId']

                    # initialize the subclients again
                    # so the subclient object has all the subclients
                    self.refresh()

                    agent_name = self._agent_object.agent_name

                    return self._subclients_dict[agent_name](
                        self._backupset_object, subclient_name, subclient_id
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def get(self, subclient_name):
        """Returns a subclient object of the specified backupset name.

            Args:
                subclient_name (str)  --  name of the subclient

            Returns:
                object - instance of the Subclient class for the given subclient name

            Raises:
                SDKException:
                    if type of the subclient name argument is not string

                    if no subclient exists with the given name
        """
        if not isinstance(subclient_name, basestring):
            raise SDKException('Subclient', '101')
        else:
            subclient_name = subclient_name.lower()

            agent_name = self._agent_object.agent_name

            if self.has_subclient(subclient_name):
                if isinstance(self._subclients_dict[agent_name], list):
                    if self._instance_object.instance_name == "vminstance":
                        subclient = self._subclients_dict[agent_name][-1]
                    elif self._client_object.client_type and int(self._client_object.client_type) == 36:
                        # client type 36 is case manager client
                        subclient = self._subclients_dict[agent_name][-1]
                    else:
                        subclient = self._subclients_dict[agent_name][0]
                else:
                    subclient = self._subclients_dict[agent_name]

                if self._backupset_object is None:
                    self._backupset_object = self._instance_object.backupsets.get(
                        self._subclients[subclient_name]['backupset']
                    )
                return subclient(
                    self._backupset_object, subclient_name, self._subclients[subclient_name]['id']
                )

            raise SDKException(
                'Subclient', '102', 'No subclient exists with name: {0}'.format(
                    subclient_name)
            )

    def delete(self, subclient_name):
        """Deletes the subclient specified by the subclient_name from the backupset.

            Args:
                subclient_name (str)  --  name of the subclient to remove from the backupset

            Raises:
                SDKException:
                    if type of the subclient name argument is not string

                    if failed to delete subclient

                    if response is empty

                    if response is not success

                    if no subclient exists with the given name
        """
        if not isinstance(subclient_name, basestring):
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

    def refresh(self):
        """Refresh the subclients associated with the Backupset / Instance."""
        self._subclients = self._get_subclients()

    @property
    def default_subclient(self):
        """Returns the name of the default subclient for the selected Agent and Backupset."""
        return self._default_subclient


class Subclient(object):
    """Base class consisting of all the common properties and operations for a Subclient"""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialise the Subclient object.

            Args:
                backupset_object (object)  --  instance of the Backupset class

                subclient_name   (str)     --  name of the subclient

                subclient_id     (str)     --  id of the subclient
                    default: None

            Returns:
                object - instance of the Subclient class
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
            '_restore_json',
            '_impersonation_json',
            '_restore_browse_option_json',
            '_restore_common_options_json',
            '_restore_destination_json',
            '_restore_fileoption_json',
            '_json_restore_subtask'
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

        self._BROWSE = self._services['BROWSE']

        self._RESTORE = self._services['RESTORE']

        self._subclient_properties = {}
        self._content = []

        self.schedules = None
        self.refresh()

    def __getattr__(self, attribute):
        """Returns the persistent attributes"""
        if attribute in self._restore_methods:
            return getattr(self._backupset_object, attribute)

        return super(Subclient, self).__getattribute__(attribute)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Subclient class instance for Subclient: "{0}" of Backupset: "{1}"'
        return representation_string.format(
            self.subclient_name, self._backupset_object.backupset_name
        )

    def _get_subclient_id(self):
        """Gets the subclient id associated to the specified backupset name and client name.

            Returns:
                str - id associated with this subclient
        """
        subclients = Subclients(self._backupset_object)
        return subclients.get(self.subclient_name).subclient_id

    def _get_subclient_properties(self):
        """Gets the subclient properties of this subclient.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
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

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException(
                'Response',
                '101',
                self._update_response_(
                    response.text))

    def _set_subclient_properties(self, attr_name, value):
        """sets the properties of this sub client.value is updated to instance once when post call
            succeeds

            Args:
                attr_name (str) --  Name of the attribute. This should be an instance variable.
                value (str)     --  Value of the attribute. This should be an instance variable.

            Raises:
                SDKException:
                    if failed to update number properties for subclient


        """
        try:
            backup = eval('self.%s' % attr_name)        # Take backup of old value
        except (AttributeError, KeyError):
            backup = None

        exec("self.%s = %s" % (attr_name, 'value'))     # set new value

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
    def _convert_size(input_size):
        """Converts the given float size to appropriate size in B / KB / MB / GB, etc.

            Args:
                size (float)  --  float value to convert

            Returns:
                str - size converted to the specific type (B, KB, MB, GB, etc.)
        """
        if input_size == 0:
            return '0B'

        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(input_size, 1024)))
        power = math.pow(1024, i)
        size = round(input_size / power, 2)
        return '%s %s' % (size, size_name[i])

    def _process_update_response(self, flag, response):
        """Updates the subclient properties with the request provided.

            Args:
                update_request  (str)  --  update request specifying the details to update

            Returns:
                (bool, basestring, basestring):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if failed to update properties

                    if response is empty

                    if response is not success
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

    def _process_backup_response(self, flag, response):
        """Runs the Backup for a subclient with the request provided and returns the Job object.

            Args:
                update_request  (str)  --  update request specifying the details to update

            Returns:
                object - instance of the Job class for this backup job if its an immediate Job
                        instance of the Schedule class for the backup job if its a scheduled Job


            Raises:
                SDKException:
                    if job initialization failed

                    if response is empty

                    if response is not success
        """
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object,
                               response.json()['jobIds'][0])
                elif "taskId" in response.json():
                    return Schedule(self._commcell_object, schedule_id=response.json()['taskId'])
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
                     backup_level,
                     incremental_backup,
                     incremental_level,
                     advanced_options=None,
                     schedule_pattern=None):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                backup_level        (str)   --  level of backup the user wish to run

                    Full / Incremental / Differential / Synthetic_full

                incremental_backup  (bool)  --  run incremental backup

                    only applicable in case of Synthetic_full backup

                incremental_level   (str)   --  run incremental backup before/after synthetic full

                    BEFORE_SYNTH / AFTER_SYNTH

                    only applicable in case of Synthetic_full backup

                advanced_options   (dict)  --  advanced backup options to be included while
                making the request

                    default: None

            Returns:
                dict    -   JSON request to pass to the API

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
            advanced_options_dict = self._advanced_backup_options(
                advanced_options)

        if advanced_options_dict:
            request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
                advanced_options_dict
            )

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        return request_json

    def _advanced_backup_options(self, options):
        """Generates the advanced backup options dict

            Args:
                options     (dict)  --  advanced backup options that are to be included
                                            in the request

            Returns:
                (dict)  -   generated advanced options dict
        """
        return options

    @property
    def name(self):
        """Returns the Subclient display name"""
        return self._subclient_properties['subClientEntity']['subclientName']

    @property
    def _json_task(self):
        """getter for the task information in JSON"""

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
    def _json_backup_subtasks(self):
        """getter for the subtask in restore JSON . It is read only attribute"""

        _backup_subtask = {
            "subTaskType": 2,
            "operationType": 2
        }

        return _backup_subtask

    @property
    def subclient_id(self):
        """Treats the subclient id as a read-only attribute."""
        return self._subclient_id

    @property
    def subclient_name(self):
        """Treats the subclient name as a read-only attribute."""
        return self._subclient_name

    @property
    def last_backup_time(self):
        """Treats the last backup time as a read-only attribute."""
        if 'lastBackupTime' in self._commonProperties:
            if self._commonProperties['lastBackupTime'] != 0:
                _last_backup_time = time.ctime(
                    self._commonProperties['lastBackupTime']
                )
                return _last_backup_time
        return 0

    @property
    def next_backup_time(self):
        """Treats the next backup time as a read-only attribute."""
        if 'nextBackupTime' in self._commonProperties:
            if self._commonProperties['nextBackupTime'] != 0:
                _next_backup = time.ctime(
                    self._commonProperties['nextBackupTime']
                )
                return _next_backup

    @property
    def is_backup_enabled(self):
        """Treats the is backup enabled as a read-only attribute."""
        if 'enableBackup' in self._commonProperties:
            return self._commonProperties['enableBackup']

    @property
    def is_intelli_snap_enabled(self):
        """Treats the is intelli snap enabled as a read-only attribute."""
        if 'snapCopyInfo' in self._commonProperties:
            snap_copy_info = self._commonProperties.get('snapCopyInfo')
            return snap_copy_info.get('isSnapBackupEnabled')

    @property
    def is_blocklevel_backup_enabled(self):
        """returns True if block level backup is enabled else returns false"""
        return bool(self._subclient_properties.get(
            'postgreSQLSubclientProp', {}).get('isUseBlockLevelBackup', False))

    @property
    def snapshot_engine_name(self):
        """returns snapshot engine name associated with the subclient"""
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
    def is_trueup_enabled(self):
        """Treats the True up enabled as a property of the Subclient class."""
        if 'isTrueUpOptionEnabled' in self._commonProperties:
            return self._commonProperties['isTrueUpOptionEnabled']

    @property
    def is_on_demand_subclient(self):
        """Treats the on demand subclient as a read-only attribute."""
        return self._backupset_object.is_on_demand_backupset

    @property
    def description(self):
        """Treats the subclient description as a property of the Subclient class."""
        if 'description' in self._commonProperties:
            return self._commonProperties['description']

    @property
    def storage_policy(self):
        """Treats the subclient storage policy as a read-only attribute."""
        storage_device = self._commonProperties['storageDevice']
        if 'dataBackupStoragePolicy' in storage_device:
            data_backup_storage_policy = storage_device['dataBackupStoragePolicy']
            if 'storagePolicyName' in data_backup_storage_policy:
                return data_backup_storage_policy['storagePolicyName']

    @property
    def storage_ma(self):
        """Treats the subclient storage ma as a read-only attribute."""
        storage_device = self._commonProperties['storageDevice']
        if 'performanceMode' in storage_device:
            data_backup_storage_device = storage_device['performanceMode']
            data_storage_details = data_backup_storage_device["perfCRCDetails"][0]
            if 'perfMa' in data_storage_details:
                return data_storage_details['perfMa']

    @property
    def storage_ma_id(self):
        """Treats the subclient storage ma id as a read-only attribute."""
        storage_device = self._commonProperties['storageDevice']
        if 'performanceMode' in storage_device:
            data_backup_storage_device = storage_device['performanceMode']
            data_storage_details = data_backup_storage_device["perfCRCDetails"][0]
            if 'perfMaId' in data_storage_details:
                return data_storage_details['perfMaId']

    @property
    def data_readers(self):
        """Treats the data readers as a read-only attribute."""
        if 'numberOfBackupStreams' in self._commonProperties:
            return int(
                self._commonProperties['numberOfBackupStreams']
            )

    @data_readers.setter
    def data_readers(self, value):
        """Sets the count of data readers for the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update number of data readers for subclient

                    if the type of value input is not int
        """
        if isinstance(value, int):
            self._set_subclient_properties(
                "_commonProperties['numberOfBackupStreams']", value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient data readers should be an int value'
            )

    @property
    def allow_multiple_readers(self):
        """Treats the allow multiple readers as a read-only attribute."""
        if 'allowMultipleDataReaders' in self._commonProperties:
            return bool(
                self._commonProperties['allowMultipleDataReaders']
            )

    @allow_multiple_readers.setter
    def allow_multiple_readers(self, value):
        """To enable or disable allow multiple readers property
        for the subclient based on the value provided as input.

            Raises:
                SDKException:
                    if failed to update allow multiple readers for subclient

                    if the type of value input is not bool
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
    def read_buffer_size(self):
        """Treats the read buffer size as a read-only attribute."""
        if 'readBuffersize' in self._commonProperties:
            return int(
                self._commonProperties['readBuffersize']
            )

    @property
    def is_default_subclient(self):
        """Returns True if the subclient is default
        subclient else returns False"""
        return self._commonProperties.get('isDefaultSubclient')

    @read_buffer_size.setter
    def read_buffer_size(self, value):
        """Sets the read buffer size for the subclient
        as the value provided as input.
            (value in KB)

            Raises:
                SDKException:
                    if failed to update read buffer size for subclient

                    if the type of value input is not int
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
    def description(self, value):
        """Sets the description of the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update description of subclient

                    if the type of value input is not string
        """
        if isinstance(value, basestring):
            self._set_subclient_properties(
                "_commonProperties['description']", value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient description should be a string value'
            )

    @storage_policy.setter
    def storage_policy(self, value):
        """Sets the storage policy of subclient as the value provided as input.

            Args:
                value   (str)   -- Storage policy name to be assigned to subclient

            Raises:
                SDKException:
                    if storage policy name is not in string format

                    if failed to update storage policy name

        """
        if isinstance(value, basestring):
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

    def enable_backup(self):
        """Enables Backup for the subclient.

            Raises:
                SDKException:
                    if failed to enable backup of subclient
        """
        self._set_subclient_properties("_commonProperties['enableBackup']", True)

    def enable_trueup(self):
        """Setter for the TrueUp Option for a Subclient"""
        if 'isTrueUpOptionEnabled'in self._commonProperties:
            self._set_subclient_properties("_commonProperties['isTrueUpOptionEnabled']", True)

    def enable_trueup_days(self, days=30):
        """Setter for the TrueUp Option with reconcile after x days"""
        self.enable_trueup()
        self._set_subclient_properties("_commonProperties['runTrueUpJobAfterDays']", days)

    def enable_backup_at_time(self, enable_time):
        """Disables Backup if not already disabled, and enables at the time specified.

            Args:
                enable_time (str)  --  UTC time to enable the backup at, in 24 Hour format
                    format: YYYY-MM-DD HH:mm:ss

            Raises:
                SDKException:
                    if time value entered is less than the current time

                    if time value entered is not of correct format

                    if failed to enable backup

                    if response is empty

                    if response is not success
        """
        try:
            time_tuple = time.strptime(enable_time, "%Y-%m-%d %H:%M:%S")
            if time.mktime(time_tuple) < time.time():
                raise SDKException('Subclient', '108')
        except ValueError:
            raise SDKException('Subclient', '109')

        enable_backup_at_time = {
            "TimeZoneName": "(UTC) Coordinated Universal Time",
            "timeValue": enable_time
        }

        self._set_subclient_properties(
            "_commonProperties['enableBackupAtDateTime']", enable_backup_at_time
        )

    def disable_backup(self):
        """Disables Backup for the subclient.

            Raises:
                SDKException:
                    if failed to disable backup of subclient
        """
        self._set_subclient_properties(
            "_commonProperties['enableBackup']", False)

    def exclude_from_sla(self):
        """Exclude subclient from SLA.

            Raises:
                SDKException:
                    if failed to exclude the subclient from SLA
        """
        self._set_subclient_properties(
            "_commonProperties['excludeFromSLA']", True)

    def enable_intelli_snap(self, snap_engine_name, proxy_options=None):
        """Enables Intelli Snap for the subclient.

            Args:
                snap_engine_name    (str)   --  Snap Engine Name

            Raises:
                SDKException:
                    if failed to enable intelli snap for subclient
        """
        if not isinstance(snap_engine_name, basestring):
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

    def disable_intelli_snap(self):
        """Disables Intelli Snap for the subclient.

            Raises:
                SDKException:
                    if failed to disable intelli snap for subclient
        """
        self._set_subclient_properties(
            "_commonProperties['snapCopyInfo']['isSnapBackupEnabled']", False
        )

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               collect_metadata=False):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential / Synthetic_full
                    default: Incremental

                incremental_backup  (bool)  --  run incremental backup
                        only applicable in case of Synthetic_full backup
                    default: False

                incremental_level   (str)   --  run incremental backup before/after synthetic full
                        BEFORE_SYNTH / AFTER_SYNTH

                        only applicable in case of Synthetic_full backup
                    default: BEFORE_SYNTH

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'incremental',
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

    def browse(self, *args, **kwargs):
        """Browses the content of the Subclient.

            Args:
                Dictionary of browse options:
                    Example:

                        browse({
                            'path': 'c:\\\\hello',

                            'show_deleted': True,

                            'from_time': '2014-04-20 12:00:00',

                            'to_time': '2016-04-21 12:00:00'
                        })

            Kwargs:
                Keyword argument of browse options:
                    Example:

                        browse(
                            path='c:\\hello',

                            show_deleted=True,

                            from_time='2014-04-20 12:00:00',

                            to_time='2016-04-21 12:00:00'
                        )

            Returns:
                (list, dict)
                    list    -   List of only the file, folder paths from the browse response

                    dict    -   Dictionary of all the paths with additional metadata retrieved
                    from browse operation


            Refer `default_browse_options`_ for all the supported options.

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['_subclient_id'] = self._subclient_id

        return self._backupset_object.browse(options)

    def find(self, *args, **kwargs):
        """Searches a file/folder in the backed up content of the subclient,
            and returns all the files matching the filters given.

            Args:
                Dictionary of browse options:
                    Example:

                        find({
                            'file_name': '*.txt',

                            'show_deleted': True,

                            'from_time': '2014-04-20 12:00:00',

                            'to_time': '2016-04-31 12:00:00'
                        })

            Kwargs:
                Keyword argument of browse options:
                    Example:

                        find(
                            file_name='*.txt',

                            show_deleted=True,

                            'from_time': '2014-04-20 12:00:00',

                            to_time='2016-04-31 12:00:00'
                        )

            Returns:
                (list, dict)
                    list    -   List of only the file, folder paths from the browse response

                    dict    -   Dictionary of all the paths with additional metadata retrieved
                    from browse operation


            Refer `default_browse_options`_ for all the supported options.

            Additional options supported:
                file_name       (str)   --  Find files with name

                file_size_gt    (int)   --  Find files with size greater than size

                file_size_lt    (int)   --  Find files with size lesser than size

                file_size_et    (int)   --  Find files with size equal to size

            .. _default_browse_options: https://github.com/CommvaultEngg/cvpysdk/blob/master/cvpysdk/backupset.py#L565

        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['_subclient_id'] = self._subclient_id

        return self._backupset_object.find(options)

    def restore_in_place(
            self,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up
                        validate_only       : To validate data backed up for restore


                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

            Returns:
                object - instance of the Job class for this restore job if its an immediate Job
                         instance of the Schedule class for this restore job if its a scheduled Job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        self._instance_object._restore_association = self._subClientEntity

        return self._instance_object._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time,
            fs_options=fs_options,
            schedule_pattern=schedule_pattern
        )

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None,
            fs_options=None,
            schedule_pattern=None):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client                (str/object) --  either the name of the client or
                                                           the instance of the Client

                destination_path      (str)        --  full path of the restore location on client

                paths                 (list)       --  list of full paths of
                                                           files/folders to restore

                overwrite             (bool)       --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl  (bool)       --  restore data and ACL files
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)       --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time           (str)         --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                fs_options      (dict)          -- dictionary that includes all advanced options
                    options:
                        preserve_level      : preserve level option to set in restore
                        proxy_client        : proxy that needed to be used for restore
                        impersonate_user    : Impersonate user options for restore
                        impersonate_password: Impersonate password option for restore
                                                in base64 encoded form
                        all_versions        : if set to True restores all the versions of the
                                                specified file
                        versions            : list of version numbers to be backed up
                        media_agent         : Media Agent need to be used for Browse and restore
                        validate_only       : To validate data backed up for restore


                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

            Returns:
                object - instance of the Job class for this restore job if its an immediate Job
                         instance of the Schedule class for this restore job if its a scheduled Job

            Raises:
                SDKException:
                    if client is not a string or Client instance

                    if destination_path is not a string

                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        self._instance_object._restore_association = self._subClientEntity

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
            schedule_pattern=schedule_pattern
        )

    def set_backup_nodes(self, data_access_nodes):
        """Sets the the backup nodes for NFS share subclient.

            Args:
                data_access_nodes   (list)  --  the list of data access nodes to be set
                as backup nodes for NFS share subclient

            Returns:
                None    -   if the operation is successful

            Raises:
                SDKException:
                    if unable to update the backup nodes for the subclient

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
            include_active=True,
            include_finished=True,
            lookup_time=1,
            job_filter='Backup,SYNTHFULL'):
        """Finds the latest job for the subclient
            which includes current running job also.

            Args:
                include_active    (bool)    -- to indicate if
                                                active jobs should be included
                    default: True

                include_finished  (bool)    -- to indicate if finished jobs
                                                should be included
                    default: True

                lookup_time       (int)     -- get jobs executed
                                                within the number of hours
                    default: 1 Hour

                job_filter        (str)     -- to specify type of job
                    default: 'Backup,SYNTHFULL'

                    for multiple filters,
                    give the values **comma(,)** separated

                    List of Possible Values:

                            Backup

                            Restore

                            AUXCOPY

                            WORKFLOW

                            etc..

                    http://documentation.commvault.com/commvault/v11/article?p=features/rest_api/operations/get_job.htm
                        to get the complete list of filters available

            Returns:
                object  -   instance of the Job class for the latest job

            Raises:
                SDKException:
                    if any error occurred while finding the latest job.

        """
        job_controller = JobController(self._commcell_object)
        if include_active and include_finished:
            client_jobs = job_controller.all_jobs(
                client_name=self._client_object.client_name,
                lookup_time=lookup_time,
                job_filter=job_filter
            )
        elif include_active:
            client_jobs = job_controller.active_jobs(
                client_name=self._client_object.client_name,
                lookup_time=lookup_time,
                job_filter=job_filter
            )
        elif include_finished:
            client_jobs = job_controller.finished_jobs(
                client_name=self._client_object.client_name,
                lookup_time=lookup_time,
                job_filter=job_filter
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

    def refresh(self):
        """Refresh the properties of the Subclient."""
        self._get_subclient_properties()
        self.schedules = Schedules(self)

    @property
    def software_compression(self):
        """Returns the value of Software Compression settings on the Subclient."""
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
    def software_compression(self, value):
        """Sets the software compression of the subclient as the value provided as input.

            Args:
                value   (str)   --  software compression setting

                Valid values are:

                -   ON_CLIENT
                -   ON_MEDIAAGENT
                -   USE_STORAGE_POLICY_SETTINGS
                -   OFF

            Raises:
                SDKException:
                    if failed to update software compression of subclient

                    if the type of value input is not string

        """
        if isinstance(value, basestring):
            self._set_subclient_properties(
                "_commonProperties['storageDevice']['softwareCompression']", value
            )
        else:
            raise SDKException('Subclient', '101')

    @property
    def encryption_flag(self):
        """Returns the value of encryption flag settings on the Subclient."""
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
    def encryption_flag(self, value):
        """Sets the encryption Flag of the subclient as the value provided as input.

            Args:
                value   (str)   --  encryption flag value

                Valid values are:

                -   ENC_NONE
                -   ENC_MEDIA_ONLY
                -   ENC_NETWORK_AND_MEDIA
                -   ENC_NETWORK_ONLY

            Raises:
                SDKException:
                    if failed to update encryption Flag of subclient

                    if the type of value input is not string

        """

        if isinstance(value, basestring):
            self._set_subclient_properties("_commonProperties['encryptionFlag']", value)
        else:
            raise SDKException('Subclient', '101')

    @property
    def deduplication_options(self):
        """Returns the value of deduplication options settings on the Subclient."""
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
    def deduplication_options(self, enable_dedupe):
        """Enables / Disables the deduplication options of the Subclient.

            Args:
                enable_dedupe   (tuple)     --  to enable or disable deduplication

                    tuple:
                        **bool**    -   boolean flag to specify whether to
                        enable / disable deduplication

                        **str**     -   where to generate the signature at

                            Valid Values are:

                            -   ON_CLIENT
                            -   ON_MEDIA_AGENT


                    e.g.:

                        >>> subclient.deduplication_options = (False, None)

                        >>> subclient.deduplication_options = (True, "ON_CLIENT")

                        >>> subclient.deduplication_options = (True, "ON_MEDIA_AGENT")

            Raises:
                SDKException:
                    if failed to update deDuplication Options of subclient

                    if the type of value input is not correct

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
