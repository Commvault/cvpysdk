#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing sublcient operations.

Subclients, Subclient, FileSystemSubclient, VirtualServerSubclient,
and CloudAppsSubclient are 5 classes defined in this file.

Subclients: Class for representing all the subclients associated with a backupset

Subclient: Base class consisting of all the common properties and operations for a Subclient

FileSystemSubclient: Derived class from Subclient Base class, representing a file system subclient,
                        and to perform operations on that subclient

VirtualServerSubclient: Derived class from Subclient Base class, representing a
                            virtual server subclient, and to perform operations on that subclient

CloudAppsSubclient: Derived class from Subclient Base class, representing a
                            cloud apps subclient, and to perform operations on that subclient

Subclients:
    __init__(class_object)      --  initialise object of subclients object associated with
                                        the specified backup set/instance.

    __str__()                   --  returns all the subclients associated with the backupset

    __repr__()                  --  returns the string for the instance of the Subclients class

    _get_subclients()           --  gets all the subclients associated with the backupset specified

    has_subclient()             --  checks if a subclient exists with the given name or not

    add()                       --  adds a new subclient to the backupset

    get(subclient_name)         --  returns the subclient object of the input subclient name

    delete(subclient_name)      --  deletes the subclient (subclient name) from the backupset


Subclient:
    __init__(backupset_object,
             subclient_name,
             subclient_id)      --  initialise instance of the Subclient class,
                                        associated to the specified backupset

    __repr__()                  --  return the subclient name, the instance is associated with

    _get_subclient_id()         --  method to get subclient id, if not specified in __init__ method

    _get_subclient_properties() --  get the properties of this subclient

    _initialize_subclient_properties() --  initializes the properties of this subclient

    _browse_and_find_json()     --  returns the appropriate JSON request to pass for either
                                        Browse operation or Find operation

    _process_browse_request()   --  processes response received for both Browse and Find request

    _restore_json()             --  returns the apppropriate JSON request to pass for either
                                        Restore In-Place or Out-of-Place operation

    _process_restore_request()  --  processes response received for the Restore request

    description()               --  update the description of the subclient

    content()                   --  update the content of the subclient

    enable_backup()             --  enables the backup for the subclient

    enable_backup_at_time()     --  enables backup for the subclient at the input time specified

    disble_backup()             --  disbles the backup for the subclient

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


FileSystemSubclient:
    _get_subclient_content_()   --  gets the content of a file system subclient

    _set_subclient_content_()   --  sets the content of a file system subclient


VirtualServerSubclient:
    _get_subclient_content_()   --  gets the content of a virtual server subclient

    _set_subclient_content_()   --  sets the content of a virtual server subclient


CloudAppsSubclient:
    _get_subclient_content_()   --  gets the content of a cloud apps subclient

    _set_subclient_content_()   --  sets the content of a cloud apps subclient

"""

from __future__ import absolute_import

import re
import math
import time

from future.standard_library import install_aliases

from .job import Job
from .schedules import Schedules
from .exception import SDKException

install_aliases()


class Subclients(object):
    """Class for getting all the subclients associated with a client."""

    def __init__(self, class_object):
        """Initialize the Sublcients object for the given backupset.

            Args:
                class_object (object)  --  instance of the Backupset/Instance class

            Returns:
                object - instance of the Subclients class
        """
        from .instance import Instance
        from .backupset import Backupset

        self._backupset_object = None
        self._instance_object = None

        if isinstance(class_object, Backupset):
            self._backupset_object = class_object
        elif isinstance(class_object, Instance):
            self._instance_object = class_object
            self._backupset_object = Backupset(
                class_object._agent_object,
                'defaultBackupSet',
                instance_id=class_object.instance_id,
                instance_name=class_object.instance_name
            )

        self._commcell_object = self._backupset_object._commcell_object

        self._SUBCLIENTS = self._commcell_object._services.GET_ALL_SUBCLIENTS % (
            self._backupset_object._agent_object._client_object.client_id
        )

        self._ADD_SUBCLIENT = self._commcell_object._services.ADD_SUBCLIENT

        self._subclients = self._get_subclients()

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        self._subclients_dict = {
            'file system': FileSystemSubclient,
            'virtual server': VirtualServerSubclient,
            'cloud apps': CloudAppsSubclient
        }

    def __str__(self):
        """Representation string consisting of all subclients of the backupset.

            Returns:
                str - string of all the subclients of th backupset of an agent of a client
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Subclient', 'Backupset', 'Instance', 'Agent', 'Client'
        )

        for index, subclient in enumerate(self._subclients):
            sub_str = '{:^5}\t{:20}\t{:20}\t{:^20}\t{:20}\t{:20}\n'.format(
                index + 1,
                subclient,
                self._backupset_object.backupset_name,
                self._backupset_object._instance_name,
                self._backupset_object._agent_object.agent_name,
                self._backupset_object._agent_object._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Subclients class."""
        return "Subclients class instance for Backupset: '{0}', of Instance: '{1}'".format(
            self._backupset_object.backupset_name, self._backupset_object._instance_name
        )

    def _get_subclients(self):
        """Gets all the subclients associated to the client specified by the backupset object.

            Returns:
                dict - consists of all subclients in the backupset
                    {
                         "subclient1_name": subclient1_id,
                         "subclient2_name": subclient2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._SUBCLIENTS
        )

        if flag:
            if response.json() and 'subClientProperties' in response.json():
                return_dict = {}

                for dictionary in response.json()['subClientProperties']:
                    backupset = str(dictionary['subClientEntity']['backupsetName']).lower()
                    instance = str(dictionary['subClientEntity']['instanceName']).lower()

                    if self._instance_object is not None:
                        if (self._instance_object.instance_name in instance and
                                self._backupset_object.backupset_name in backupset):
                            temp_name = str(dictionary['subClientEntity']['subclientName']).lower()
                            temp_id = str(dictionary['subClientEntity']['subclientId']).lower()
                            return_dict[temp_name] = temp_id
                    elif self._backupset_object.backupset_name in backupset:
                        temp_name = str(dictionary['subClientEntity']['subclientName']).lower()
                        temp_id = str(dictionary['subClientEntity']['subclientId']).lower()
                        return_dict[temp_name] = temp_id

                return return_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

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
        if not isinstance(subclient_name, str):
            raise SDKException('Subclient', '101')

        return self._subclients and str(subclient_name).lower() in self._subclients

    def add(self, subclient_name, storage_policy, description=''):
        """Adds a new subclient to the backupset.

            Args:
                subclient_name  (str)   --  name of the new subclient to add

                storage_policy  (str)   --  name of the storage policy to associate with subclient

                description     (str)   --  description for the subclient (optional)

            Returns:
                object - instance of the Subclient class

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
        if not (isinstance(subclient_name, str) and
                isinstance(storage_policy, str) and
                isinstance(description, str)):
            raise SDKException('Subclient', '101')

        if not self.has_subclient(subclient_name):
            request_json = {
                "subClientProperties": {
                    "contentOperationType": 2,
                    "subClientEntity": {
                        "clientName": self._backupset_object._agent_object._client_object.client_name,
                        "appName": self._backupset_object._agent_object.agent_name,
                        "backupsetName": self._backupset_object.backupset_name,
                        "instanceName": self._backupset_object._instance_name,
                        "subclientName": subclient_name
                    },
                    "commonProperties": {
                        "description": description,
                        "enableBackup": True,
                        "storageDevice": {
                            "dataBackupStoragePolicy": {
                                "storagePolicyName": storage_policy
                            }
                        }
                    }
                }
            }

            flag, response = self._commcell_object._cvpysdk_object.make_request(
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
                        subclient_id = response.json()['response']['entity']['subclientId']

                        # initialize the subclients again
                        # so the subclient object has all the subclients
                        self._subclients = self._get_subclients()

                        agent_name = self._backupset_object._agent_object.agent_name

                        return self._subclients_dict[agent_name](
                            self._backupset_object, subclient_name, subclient_id
                        )
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(subclient_name)
            )

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
        if not isinstance(subclient_name, str):
            raise SDKException('Subclient', '101')
        else:
            subclient_name = str(subclient_name).lower()

            agent_name = self._backupset_object._agent_object.agent_name

            if self.has_subclient(subclient_name):
                return self._subclients_dict[agent_name](
                    self._backupset_object, subclient_name, self._subclients[subclient_name]
                )

            raise SDKException(
                'Subclient', '102', 'No subclient exists with name: {0}'.format(subclient_name)
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
        if not isinstance(subclient_name, str):
            raise SDKException('Subclient', '101')
        else:
            subclient_name = str(subclient_name).lower()

        if self.has_subclient(subclient_name):
            delete_subclient_service = self._commcell_object._services.SUBCLIENT % (
                self._subclients[subclient_name]
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', delete_subclient_service
            )

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = str(response_value['errorString'])

                        if error_message:
                            o_str = 'Failed to delete subclient\nError: "{0}"'
                            raise SDKException('Subclient', '102', o_str.format(error_message))
                        else:
                            if error_code == '0':
                                # initialize the subclients again
                                # so the subclient object has all the subclients
                                self._subclients = self._get_subclients()
                            else:
                                o_str = ('Failed to delete subclient with Error Code: "{0}"\n'
                                         'Please check the documentation for '
                                         'more details on the error')
                                raise SDKException('Subclient', '102', o_str.format(error_code))
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException(
                'Subclient', '102', 'No subclient exists with name: {0}'.format(subclient_name)
            )


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
        self._subclient_name = str(subclient_name).lower()
        self._commcell_object = self._backupset_object._commcell_object

        if subclient_id:
            self._subclient_id = str(subclient_id)
        else:
            self._subclient_id = self._get_subclient_id()

        self._SUBCLIENT = self._commcell_object._services.SUBCLIENT % (self.subclient_id)
        self._BACKUP = None

        self._BROWSE = self._commcell_object._services.BROWSE
        self._RESTORE = self._commcell_object._services.RESTORE

        self._initialize_subclient_properties()

        self.schedules = Schedules(self)

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

            Returns:
                dict - dictionary consisting of the properties of this subclient

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._SUBCLIENT)

        if flag:
            if response.json() and 'subClientProperties' in response.json():
                return response.json()['subClientProperties'][0]
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    # Abstract method to be overridden
    # Raises `Method Not Implemented` Exception if not implemented
    def _get_subclient_content_(self, subclient_content):
        raise SDKException('Subclient', '112')

    # Abstract method to be overridden
    # Raises `Method Not Implemented` Exception if not implemented
    def _set_subclient_content_(self, subclient_content):
        raise SDKException('Subclient', '112')

    def _initialize_subclient_properties(self):
        """Initializes the common properties for the subclient."""
        self._subclient_properties = self._get_subclient_properties()

        if 'description' in self._subclient_properties['commonProperties']:
            self._description = str(self._subclient_properties['commonProperties']['description'])
        else:
            self._description = None

        if 'lastBackupTime' in self._subclient_properties['commonProperties']:
            if self._subclient_properties['commonProperties']['nextBackupTime'] == 0:
                self._last_backup_time = None
            else:
                self._last_backup_time = time.ctime(
                    self._subclient_properties['commonProperties']['lastBackupTime']
                )
        else:
            self._last_backup_time = None

        if 'onDemandSubClient' in self._subclient_properties['commonProperties']:
            self._on_demand_subclient = self._subclient_properties[
                'commonProperties']['onDemandSubClient']
        else:
            self._on_demand_subclient = False

        if 'nextBackupTime' in self._subclient_properties['commonProperties']:
            if self._subclient_properties['commonProperties']['nextBackupTime'] == 0:
                self._next_backup = None
            else:
                self._next_backup = time.ctime(
                    self._subclient_properties['commonProperties']['nextBackupTime']
                )
        else:
            self._next_backup = None

        if 'enableBackup' in self._subclient_properties['commonProperties']:
            self._is_backup_enabled = self._subclient_properties[
                'commonProperties']['enableBackup']
        else:
            self._is_backup_enabled = False

        self._content = self._get_subclient_content_(self._subclient_properties)

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

    def _update(self, subclient_description, subclient_content, backup=True, enable_time=None):
        """Updates the properties of the subclient.

            Args:
                subclient_description (str)     --  description of the subclient

                subclient_content     (list)    --  content of the subclient

                backup                (bool)    --  enable backup or not

                enable_time           (str)     --  time to re-enable the activity at

            Returns:
                (bool, str, str):
                    bool -  flag specifies whether success / failure

                    str  -  error code received in the response

                    str  -  error message received

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        request_json1 = {
            "association": {
                "entity": [{
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "instanceName": self._backupset_object._instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": self.subclient_name
                }]
            }, "subClientProperties": {
                "contentOperationType": 1,
                "subClientEntity": {
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "instanceName": self._backupset_object._instance_name,
                    "subclientName": self.subclient_name
                },
                "content": self._set_subclient_content_(subclient_content),
                "commonProperties": {
                    "description": subclient_description,
                    "enableBackup": backup
                }
            }
        }

        request_json2 = {
            "association": {
                "entity": [{
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "instanceName": self._backupset_object._instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": self.subclient_name
                }]
            }, "subClientProperties": {
                "contentOperationType": 1,
                "subClientEntity": {
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "instanceName": self._backupset_object._instance_name,
                    "subclientName": self.subclient_name
                },
                "content": self._set_subclient_content_(subclient_content),
                "commonProperties": {
                    "description": subclient_description,
                    "enableBackup": False,
                    "enableBackupAfterDelay": True,
                    "enableBackupAtDateTime": {
                        "TimeZoneName": "(UTC) Coordinated Universal Time",
                        "timeValue": enable_time
                    }
                }
            }
        }

        if enable_time is None:
            request_json = request_json1
        else:
            request_json = request_json2

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._SUBCLIENT, request_json
        )

        self._initialize_subclient_properties()

        if flag:
            if response.json() and "response" in response.json():
                error_code = str(response.json()["response"][0]["errorCode"])

                if error_code == "0":
                    return (True, "0", "")
                else:
                    error_string = ""

                    if "errorString" in response.json()["response"][0]:
                        error_string = response.json()["response"][0]["errorString"]

                    if error_string:
                        return (False, error_code, error_string)
                    else:
                        return (False, error_code, "")
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _process_backup_request(self, backup_request):
        """Runs the Backup for a subclient with the request provided and returns the Job object.

            Args:
                backup_request  (str)  --  backup request specifying the backup level,
                                               to run for the subclient

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if job initialization failed

                    if response is empty

                    if response is not success
        """
        self._BACKUP = self._commcell_object._services.SUBCLIENT_BACKUP % (
            self.subclient_id, backup_request
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST', self._BACKUP)

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    o_str = 'Initializing backup failed\nError: "{0}"'.format(
                        response.json()['errorMessage']
                    )
                    raise SDKException('Subclient', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _browse_and_find_json(
            self,
            option,
            path='\\**\\*',
            file_or_folder_name=None,
            show_deleted_files=True,
            restore_index=True,
            from_date=0,
            to_date=time.time()):
        """Returns the JSON request to pass to the DoBrowse API,
            as per the options selected by the user.

            Args:
                option (str)  --  string option for which to run the API for
                    e.g.; Browse / Find

            Returns:
                dict - JSON request to pass to the API
        """
        options_dict = {
            "Browse": 0,
            "Find": 1
        }

        request_json = {
            "opType": options_dict[option],
            "mode": {
                "mode": 2
            },
            "paths": [{
                "path": path
            }],
            "options": {
                "showDeletedFiles": show_deleted_files,
                "restoreIndex": restore_index
            },
            "entity": {
                "clientName": self._backupset_object._agent_object._client_object.client_name,
                "clientId": int(self._backupset_object._agent_object._client_object.client_id),
                "applicationId": int(self._backupset_object._agent_object.agent_id),
                "instanceId": int(self._backupset_object._instance_id),
                "backupsetId": int(self._backupset_object.backupset_id),
                "subclientId": int(self.subclient_id)
            },
            "timeRange": {
                "fromTime": int(from_date),
                "toTime": int(to_date)
            },
            "queries": [{
                "type": 0,
                "queryId": "dataQuery",
                "dataParam": {
                    "sortParam": {
                        "ascending": False,
                        "sortBy": [0]
                    }
                }
            }]
        }

        if option == 'Find':
            request_json['queries'][0]['whereClause'] = [{
                "connector": 0,
                "criteria": {
                    "field": "FileName",
                    "values": [file_or_folder_name]
                }
            }]

        return request_json

    def _process_browse_request(self, option, flag, response):
        """Runs the DoBrowse API with the request JSON provided for the operation specified,
            and returns the contents after parsing the response.

            Args:
                option      (str)   --  string option for which to process the response for
                    e.g.; Browse / Find

                flag        (bool)  --  boolean to specify whether the response was success or not

                response    (dict)  --  JSON response received for the request from the Server

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse/search for content

                    if response is empty

                    if response is not success
        """
        options_dict = {
            "Browse": ('110', 'Failed to browse for subclient backup content\nError: "{0}"'),
            "Find": ('111', 'Failed to Search\nError: "{0}"')
        }

        exception_code = options_dict[option][0]
        exception_message = options_dict[option][1]

        if flag:
            if response.json() and 'browseResponses' in response.json():
                if 'browseResult' in response.json()['browseResponses'][0]:
                    browse_result = response.json()['browseResponses'][0]['browseResult']

                    if 'dataResultSet' in browse_result:
                        result_set = browse_result['dataResultSet']
                        full_result = []
                        paths = []

                        for result in result_set:
                            name = str(result['displayName'])
                            path = str(result['path'])
                            mod_time = time.localtime(result['modificationTime'])
                            mod_time = time.strftime('%d/%m/%Y %H:%M:%S', mod_time)

                            if 'file' in result['flags']:
                                file_or_folder = 'File'
                            else:
                                file_or_folder = 'Folder'

                            # gets the size in human readable format
                            size = self._convert_size(float(result['size']))

                            temp = {
                                path: [name, file_or_folder, size, mod_time]
                            }

                            paths.append(path)
                            full_result.append(temp)

                        return paths, full_result
                    else:
                        raise SDKException('Subclient', exception_code)
                elif 'messages' in response.json()['browseResponses'][0]:
                    message = response.json()['browseResponses'][0]['messages'][0]
                    error_message = message['errorMessage']

                    o_str = exception_message
                    raise SDKException('Subclient', '102', o_str.format(error_message))
                else:
                    raise SDKException('Subclient', exception_code)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _restore_json(
            self,
            paths,
            in_place=True,
            client=None,
            destination_path=None,
            overwrite=True,
            restore_data_and_acl=True):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                paths   (list)  --  list of full paths of files/folders to restore

            Returns:
                dict - JSON request to pass to the API
        """
        if client is None and destination_path is None:
            client_id = int(self._backupset_object._agent_object._client_object.client_id)
            client_name = self._backupset_object._agent_object._client_object.client_name
        else:
            client_id = int(client.client_id)
            client_name = client.client_name

        request_json = {
            "taskInfo": {
                "associations": [{
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "clientId": int(self._backupset_object._agent_object._client_object.client_id),
                    "appName": self._backupset_object._agent_object.agent_name,
                    "appTypeId": int(self._backupset_object._agent_object.agent_id),
                    "backupsetName": self._backupset_object.backupset_name,
                    "backupSetId": int(self._backupset_object.backupset_id),
                    "instanceName": self._backupset_object._instance_name,
                    "instanceId": int(self._backupset_object._instance_id),
                    "subclientName": self.subclient_name,
                    "subclientId": int(self.subclient_id),
                }],
                "task": {
                    "initiatedFrom": 2,
                    "taskType": 1,
                    "policyType": 0,
                    "taskFlags": {
                        "disabled": False
                    }
                },
                "subTasks": [{
                    "subTaskOperation": 1,
                    "subTask": {
                        "subTaskType": 3,
                        "operationType": 1001
                    },
                    "options": {
                        "restoreOptions": {
                            "commonOptions": {
                                "unconditionalOverwrite": overwrite
                            },
                            "destination": {
                                "inPlace": in_place,
                                "destClient": {
                                    "clientId": client_id,
                                    "clientName": client_name,
                                }
                            },
                            "fileOption": {
                                "sourceItem": paths
                            }
                        }
                    }
                }]
            }
        }

        if restore_data_and_acl:
            request_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]["restoreACLsType"] = 3

        if destination_path is not None:
            request_json['taskInfo']["subTasks"][0]["options"][
                "restoreOptions"]["destination"]["destPath"] = [destination_path]

        return request_json

    def _process_restore_request(self, request_json):
        """Runs the CreateTask API with the request JSON provided for Restore,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if restore job failed

                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._RESTORE, request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']

                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def subclient_id(self):
        """Treats the subclient id as a read-only attribute."""
        return self._subclient_id

    @property
    def subclient_name(self):
        """Treats the subclient name as a read-only attribute."""
        return self._subclient_name

    @property
    def on_demand_subclient(self):
        """Treats the on demand subclient as a read-only attribute."""
        return self._on_demand_subclient

    @property
    def last_backup_time(self):
        """Treats the last backup time as a read-only attribute."""
        return self._last_backup_time

    @property
    def next_backup_time(self):
        """Treats the next backup time as a read-only attribute."""
        return self._next_backup

    @property
    def is_backup_enabled(self):
        """Treats the is backup enabled as a read-only attribute."""
        return self._is_backup_enabled

    @property
    def description(self):
        """Treats the subclient description as a property of the Subclient class."""
        return self._description

    @property
    def content(self):
        """Treats the subclient content as a property of the Subclient class."""
        return self._content

    @description.setter
    def description(self, value):
        """Sets the description of the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update description of subclient

                    if the type of value input is not string
        """
        if isinstance(value, str):
            output = self._update(value, self.content, self.is_backup_enabled)

            if output[0]:
                return
            else:
                o_str = 'Failed to update the description of the subclient\nError: "{0}"'
                raise SDKException('Subclient', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient description should be a string value'
            )

    @content.setter
    def content(self, value):
        """Sets the content of the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        if isinstance(value, list) and value != []:
            output = self._update(self.description, value, self.is_backup_enabled)

            if output[0]:
                return
            else:
                o_str = 'Failed to update the content of the subclient\nError: "{0}"'
                raise SDKException('Subclient', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def enable_backup(self):
        """Enables Backup for the subclient.

            Raises:
                SDKException:
                    if failed to enable backup of subclient
        """
        output = self._update(self.description, self.content, True)

        if output[0]:
            return
        else:
            o_str = 'Failed to enable backup for the subclient\nError: "{0}"'
            raise SDKException('Subclient', '102', o_str.format(output[2]))

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

        output = self._update(self.description, self.content, False, enable_time)

        if output[0]:
            return
        else:
            o_str = 'Failed to enable backup for the subclient\nError: "{0}"'
            raise SDKException('Subclient', '102', o_str.format(output[2]))

    def disable_backup(self):
        """Disables Backup for the subclient.

            Raises:
                SDKException:
                    if failed to disable backup of subclient
        """
        output = self._update(self.description, self.content, False)

        if output[0]:
            return
        else:
            o_str = 'Failed to disable backup for the subclient\nError: "{0}"'
            raise SDKException('Subclient', '102', o_str.format(output[2]))

    def backup(
            self,
            backup_level="Incremental",
            incremental_backup=False,
            incremental_level='BEFORE_SYNTH'):
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

        if backup_level not in ['full', 'incremental', 'differential', 'synthetic_full']:
            raise SDKException('Subclient', '103')

        backup_request = backup_level

        if backup_level == 'synthetic_full':
            if incremental_backup:
                backup_request += '&runIncrementalBackup=True'
                backup_request += '&incLevel=%s' % (incremental_level.lower())
            else:
                backup_request += '&runIncrementalBackup=False'

        return self._process_backup_request(backup_request)

    def browse(self,
               path='',
               show_deleted_files=False,
               vm_file_browse=False,
               vm_disk_browse=False):
        """Gets the content of the backup for this subclient at the path specified.

            Args:
                path                (str)   --  folder path to get the contents of
                    default: ''; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: False

                vm_file_browse      (bool)  --  browse files and folders inside
                                                    a guest virtual machine
                    only applicable when browsing content inside a guest virtual machine
                    default: False

                vm_disk_browse      (bool)  --  browse virtual machine files
                                                    e.g.; .vmdk files, etc.
                    only applicable when browsing content inside a guest virtual machine
                    default: False

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        from urllib.parse import urlencode

        web_service = self._SUBCLIENT + '/Browse?'
        encode_dict = {
            'path': path,
            'showDeletedFiles': show_deleted_files,
            'vsFileBrowse': vm_file_browse,
            'vsDiskBrowse': vm_disk_browse,
            'mode': 2
        }

        web_service += urlencode(encode_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', web_service)

        return self._process_browse_request('Browse', flag, response)

    def browse_in_time(self,
                       path='',
                       show_deleted_files=True,
                       restore_index=True,
                       from_date=None,
                       to_date=None):
        """Gets the content of the backup for this subclient
            at the path specified in the time range specified.

            Args:
                path                (str)   --  folder path to get the contents of
                    default: ''; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

                restore_index       (bool)  --  restore index if it is not cached
                    default: True

                from_date           (str)   --  date to get the contents after
                        format: dd/MM/YYYY

                        gets contents from 01/01/1970 if not specified
                    default: None

                to_date             (str)  --  date to get the contents before
                        format: dd/MM/YYYY

                        gets contents till current day if not specified
                    default: None

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if from date value is incorrect

                    if to date value is incorrect

                    if to date is less than from date

                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        if from_date and (from_date != '01/01/1970' and from_date != '1/1/1970'):
            temp = from_date.split('/')
            if (len(temp) == 3 and
                    0 < int(temp[0]) < 32 and
                    0 < int(temp[1]) < 13 and
                    int(temp[2]) > 1969 and
                    (re.search(r'\d\d/\d\d/\d\d\d\d', from_date) or
                     re.search(r'\d/\d/\d\d\d\d', from_date))):
                from_date = int(time.mktime(time.strptime(from_date, '%d/%m/%Y')))
            else:
                raise SDKException('Subclient', '106')
        else:
            from_date = 0

        if to_date and (to_date != '01/01/1970' and to_date != '1/1/1970'):
            temp = to_date.split('/')
            if (len(temp) == 3 and
                    0 < int(temp[0]) < 32 and
                    0 < int(temp[1]) < 13 and
                    int(temp[2]) > 1969 and
                    (re.search(r'\d\d/\d\d/\d\d\d\d', to_date) or
                     re.search(r'\d/\d/\d\d\d\d', to_date))):
                today = time.strftime('%d/%m/%Y')
                if today == to_date:
                    to_date = int(time.time())
                else:
                    to_date = int(time.mktime(time.strptime(to_date, '%d/%m/%Y')))
            else:
                raise SDKException('Subclient', '106')
        else:
            to_date = int(time.time())

        if to_date < from_date:
            raise SDKException('Subclient', '107')

        if int(self._backupset_object._agent_object.agent_id) == 33:
            path = path.strip('\\').strip('/')
            if path:
                path = path.replace('/', '\\')
            else:
                path = '\\'
        elif int(self._backupset_object._agent_object.agent_id) == 29:
            path = path.strip('\\').strip('/')
            if path:
                path = path.replace('\\', '/')
            else:
                path = '\\'

            path = '/' + path

        request_json = self._browse_and_find_json(
            option='Browse',
            path=path,
            show_deleted_files=show_deleted_files,
            restore_index=restore_index,
            from_date=from_date,
            to_date=to_date
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._BROWSE, request_json
        )

        return self._process_browse_request('Browse', flag, response)

    def find(self,
             file_or_folder_name,
             show_deleted_files=True,
             restore_index=True):
        """Searches a file/folder in the subclient backup content,
            and returns all the files matching the file name given.

            Args:
                file_or_folder_name (str)   --  name of the file or folder to search

                show_deleted_files  (bool)  --  include deleted files in the search or not
                    default: True

                restore_index       (bool)  --  restore index if it is not cached
                    default: True

            Returns:
                list - list of all files or folders with their full paths matching the name

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to search file/folder

                    if response is empty

                    if response is not success
        """
        request_json = self._browse_and_find_json(
            option='Find',
            file_or_folder_name=file_or_folder_name,
            show_deleted_files=show_deleted_files,
            restore_index=restore_index
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._BROWSE, request_json
        )

        return self._process_browse_request('Find', flag, response)

    def restore_in_place(self, paths, overwrite=True, restore_data_and_acl=True):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                restore_data_and_acl    (bool)  --  restore data and ACL files
                    default: True

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
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        for index, path in enumerate(paths):
            if int(self._backupset_object._agent_object.agent_id) == 33:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('/', '\\')
                else:
                    path = '\\'
            elif int(self._backupset_object._agent_object.agent_id) == 29:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('\\', '/')
                else:
                    path = '\\'
                path = '/' + path

            paths[index] = path

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths, overwrite=overwrite, restore_data_and_acl=restore_data_and_acl
        )

        return self._process_restore_request(request_json)

    def restore_out_of_place(self,
                             client,
                             destination_path,
                             paths,
                             overwrite=True,
                             restore_data_and_acl=True):
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
        from .client import Client

        if not ((isinstance(client, str) or isinstance(client, Client)) and
                isinstance(destination_path, str) and
                isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if isinstance(client, Client):
            client = client
        elif isinstance(client, str):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        for index, path in enumerate(paths):
            if int(self._backupset_object._agent_object.agent_id) == 33:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('/', '\\')
                else:
                    path = '\\'
            elif int(self._backupset_object._agent_object.agent_id) == 29:
                path = path.strip('\\').strip('/')
                if path:
                    path = path.replace('\\', '/')
                else:
                    path = '\\'
                path = '/' + path

            paths[index] = path

        if int(self._backupset_object._agent_object.agent_id) == 33:
            destination_path = destination_path.strip('\\').strip('/')
            if destination_path:
                destination_path = destination_path.replace('/', '\\')
            else:
                destination_path = '\\'
        elif int(self._backupset_object._agent_object.agent_id) == 29:
            destination_path = destination_path.strip('\\').strip('/')
            if destination_path:
                destination_path = destination_path.replace('\\', '/')
            else:
                destination_path = '\\'

            destination_path = '/' + destination_path

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            in_place=False,
            client=client,
            destination_path=destination_path,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl
        )

        return self._process_restore_request(request_json)


class FileSystemSubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self, subclient_properties):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of subclient

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        if 'content' in self._subclient_properties:
            subclient_content = subclient_properties['content']

            for path in subclient_content:
                content.append(str(path["path"]))

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            File System Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        for path in subclient_content:
            file_system_dict = {
                "path": path
            }
            content.append(file_system_dict)

        return content


class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self, subclient_properties):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of subclient

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        content_types = {
            '1': 'Host',
            '2': 'Resource Pool',
            '4': 'Datacenter',
            '9': 'Virtual Machine',
            '16': 'All unprotected VMs',
            '17': 'Root'
        }

        if 'vmContent' in self._subclient_properties:
            subclient_content = subclient_properties['vmContent']

            if 'children' in subclient_content:
                children = subclient_content['children']

                for child in children:
                    path = str(child['path']) if 'path' in child else None
                    display_name = str(child['displayName'])
                    content_type = content_types[str(child['type'])]

                    temp_dict = {
                        'path': path,
                        'display_name': display_name,
                        'type': content_type
                    }

                    content.append(temp_dict)

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Virtual Server Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        content_types = {
            'Host': '1',
            'Root': '17',
            'Datacenter': '4',
            'Resource Pool': '2',
            'Virtual Machine': '9',
            'All unprotected VMs': '16'
        }

        try:
            for temp_dict in subclient_content:
                virtual_server_dict = {
                    'allOrAnyChildren': True,
                    'equalsOrNotEquals': True,
                    'displayName': temp_dict['display_name'],
                    'path': temp_dict['path'],
                    'type': content_types[temp_dict['type']]
                }

                content.append(virtual_server_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        return content


class CloudAppsSubclient(Subclient):
    """Derived class from Subclient Base class, representing a CloudApps subclient,
        and to perform operations on that subclient."""

    def _get_subclient_content_(self, subclient_properties):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of subclient

            Returns:
                list - list of content associated with the subclient
        """
        content = []

        for account in subclient_properties['content']:
            temp_account = account["cloudconnectorContent"]["includeAccounts"]

            content_dict = {
                'SMTPAddress': temp_account["contentName"],
                'display_name': temp_account["contentValue"]
            }

            content.append(content_dict)

        return content

    def _set_subclient_content_(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Cloud Apps Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        try:
            for account in subclient_content:
                temp_content_dict = {
                    "cloudconnectorContent": {
                        "includeAccounts": {
                            "contentValue": account['display_name'],
                            "contentType": 134,
                            "contentName": account['SMTPAddress']
                        }
                    }
                }
                content.append(temp_content_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        return content
