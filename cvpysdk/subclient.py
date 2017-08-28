#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing subclient operations.

Subclients and Subclient are 2 classes defined in this file.

Subclients: Class for representing all the subclients associated with a backupset / instance

Subclient: Base class consisting of all the common properties and operations for a Subclient


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

    _set_subclient_properties() --  sets the properties of this sub client .

    _filter_paths()             --  filters the path as per the OS, and the Agent

    _process_backup_request()   --  runs the backup request provided, and processes the response

    _browse_and_find_json()     --  returns the appropriate JSON request to pass for either
                                        Browse operation or Find operation

    _process_browse_response()  --  processes response received for both Browse and Find request

    _restore_json()             --  returns the apppropriate JSON request to pass for either
                                        Restore In-Place or Out-of-Place operation

    _json_task()                --  setter for task property

    _json_restore_subtask()     --  setter for sub task property

    _association_json()         --  setter for association property

    _impersonation_json()       --  setter for impersonation Property

    _restore_browse_option_json()-  setter for  browse option  property in restore

    _restore_commonOptions_json()-  setter for common options property in restore

    _restore_destination_json() --  setter for destination options property in restore

    _restore_fileoption_json()  -- setter for file option property in restore

    _restore_destination_json() -- setter for destination property in restore

    _restore_sharepoint_json()  -- setter for the sharepoint property in restore

    _process_restore_response() --  processes response received for the Restore request

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

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import math
import time

from past.builtins import basestring
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

        if isinstance(class_object, Instance):
            self._instance_object = class_object
        elif isinstance(class_object, Backupset):
            self._backupset_object = class_object
            self._instance_object = class_object._instance_object

            '''
            try:
                self._backupset_object = Backupset(
                    class_object._agent_object,
                    'defaultBackupSet',
                    instance_id=class_object.instance_id,
                    instance_name=class_object.instance_name
                )
            except SDKException:
                self._backupset_object = Backupset(
                    class_object._agent_object,
                    sorted(class_object.backupsets._backupsets)[0],
                    instance_id=class_object.instance_id,
                    instance_name=class_object.instance_name
                )
            '''

        self._commcell_object = self._instance_object._commcell_object

        self._SUBCLIENTS = self._commcell_object._services['GET_ALL_SUBCLIENTS'] % (
            self._instance_object._agent_object._client_object.client_id
        )

        self._ADD_SUBCLIENT = self._commcell_object._services['ADD_SUBCLIENT']

        self._subclients = self._get_subclients()

        from .subclients.fssubclient import FileSystemSubclient
        from .subclients.vssubclient import VirtualServerSubclient
        from .subclients.casubclient import CloudAppsSubclient
        from .subclients.sqlsubclient import SQLServerSubclient
        from .subclients.nassubclient import NASSubclient
        from .subclients.hanasubclient import SAPHANASubclient

        globals()['FileSystemSubclient'] = FileSystemSubclient
        globals()['VirtualServerSubclient'] = VirtualServerSubclient
        globals()['CloudAppsSubclient'] = CloudAppsSubclient
        globals()['SQLServerSubclient'] = SQLServerSubclient
        globals()['NASSubclient'] = NASSubclient
        globals()['SAPHANASubclient'] = SAPHANASubclient

        # add the agent name to this dict, and its class as the value
        # the appropriate class object will be initialized based on the agent
        self._subclients_dict = {
            'file system': FileSystemSubclient,
            'virtual server': VirtualServerSubclient,
            'cloud apps': CloudAppsSubclient,
            'sql server': SQLServerSubclient,
            'nas': NASSubclient,
            'sap hana': SAPHANASubclient
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
            sub_str = '{:^5}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\n'.format(
                index + 1,
                subclient.split('\\')[-1],
                self._subclients[subclient]['backupset'],
                self._instance_object.instance_name,
                self._instance_object._agent_object.agent_name,
                self._instance_object._agent_object._client_object.client_name
            )
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Subclients class."""
        if self._backupset_object is None:
            o_str = "Subclients class instance for Instance: '{0}'".format(
                self._instance_object.instance_name
            )
        else:
            o_str = "Subclients class instance for Backupset: '{0}', of Instance: '{1}'".format(
                self._backupset_object.backupset_name, self._instance_object.instance_name
            )

        return o_str

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
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._SUBCLIENTS
        )

        if flag:
            if response.json() and 'subClientProperties' in response.json():
                return_dict = {}

                for dictionary in response.json()['subClientProperties']:
                    backupset = dictionary['subClientEntity']['backupsetName'].lower()
                    instance = dictionary['subClientEntity']['instanceName'].lower()

                    if self._backupset_object is not None:
                        if (self._instance_object.instance_name in instance and
                                self._backupset_object.backupset_name in backupset):
                            temp_name = dictionary['subClientEntity']['subclientName'].lower()
                            temp_id = str(dictionary['subClientEntity']['subclientId']).lower()
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "backupset": backupset
                            }
                    elif self._instance_object.instance_name in instance:
                        temp_name = dictionary['subClientEntity']['subclientName'].lower()
                        temp_id = str(dictionary['subClientEntity']['subclientId']).lower()

                        if len(self._instance_object.backupsets._backupsets) > 1:
                            return_dict["{0}\\{1}".format(backupset, temp_name)] = {
                                "id": temp_id,
                                "backupset": backupset
                            }
                        else:
                            return_dict[temp_name] = {
                                "id": temp_id,
                                "backupset": backupset
                            }

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
        if not isinstance(subclient_name, basestring):
            raise SDKException('Subclient', '101')

        return self._subclients and subclient_name.lower() in self._subclients

    def add(self, subclient_name, storage_policy, description=''):
        """Adds a new subclient to the backupset.

            Args:
                subclient_name      (str)   --  name of the new subclient to add

                storage_policy      (str)   --  name of the storage policy to
                                                    associate with the subclient

                description         (str)   --  description for the subclient (optional)

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
        if not (isinstance(subclient_name, basestring) and
                isinstance(storage_policy, basestring) and
                isinstance(description, basestring)):
            raise SDKException('Subclient', '101')

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(subclient_name)
            )

        if self._backupset_object is None:
            if self._instance_object.backupsets.has_backupset('defaultBackupSet'):
                self._backupset_object = self._instance_object.backupsets.get('defaultBackupSet')
            else:
                self._backupset_object = self._instance_object.backupsets.get(
                    sorted(self._instance_object.backupsets._backupsets)[0]
                )

        if storage_policy not in self._commcell_object.storage_policies._policies:
            raise SDKException(
                'Subclient',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(storage_policy)
            )

        request_json = {
            "subClientProperties": {
                "contentOperationType": 2,
                "subClientEntity": {
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
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

            agent_name = self._instance_object._agent_object.agent_name

            if self.has_subclient(subclient_name):
                if self._backupset_object is None:
                    self._backupset_object = self._instance_object.backupsets.get(
                        self._subclients[subclient_name]['backupset']
                    )

                return self._subclients_dict[agent_name](
                    self._backupset_object, subclient_name, self._subclients[subclient_name]['id']
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
        if not isinstance(subclient_name, basestring):
            raise SDKException('Subclient', '101')
        else:
            subclient_name = subclient_name.lower()

        if self.has_subclient(subclient_name):
            delete_subclient_service = self._commcell_object._services['SUBCLIENT'] % (
                self._subclients[subclient_name]['id']
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
                            error_message = response_value['errorString']

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
        self._subclient_name = subclient_name.split('\\')[-1].lower()
        self._commcell_object = self._backupset_object._commcell_object

        if subclient_id:
            self._subclient_id = str(subclient_id)
        else:
            self._subclient_id = self._get_subclient_id()

        self._SUBCLIENT = self._commcell_object._services['SUBCLIENT'] % (self.subclient_id)

        self._BROWSE = self._commcell_object._services['BROWSE']

        self._RESTORE = self._commcell_object._services['RESTORE']

        self._subclient_properties = {}
        self._get_subclient_properties()

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

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._SUBCLIENT)

        if flag:
            if response.json() and 'subClientProperties' in response.json():
                self._subclient_properties = response.json()['subClientProperties'][0]
                if 'commonProperties' in self._subclient_properties:
                    self._commonProperties = self._subclient_properties['commonProperties']

                if 'subClientEntity' in self._subclient_properties:
                    self._subClientEntity = self._subclient_properties['subClientEntity']

                if 'proxyClient' in self._subclient_properties:

                    self._proxyClient = self._subclient_properties['proxyClient']

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _set_subclient_properties(self, attr_name, value):
        """sets the properties of this sub client.value is updated to instance once when post call
            succeeds

            Args:
                attr_name (str)  --  old value of the property. this should be instance variable.
                value (str)  --  new value of the property. this should be instance variable.

            Raises:
                SDKException:
                    if failed to update number properties for subclient


        """
        backup = None
        exec("backup = self.%s" % (attr_name))          #Take backup of old value
        exec("self.%s = %s" % (attr_name, 'value'))       #set new value

        request_json = self._get_subclient_properties_json()
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._SUBCLIENT, request_json
        )

        output = self._process_update_response(flag, response)

        if output[0]:
            return
        else:
            o_str = 'Failed to update properties of subclient\nError: "{0}"'
            exec("self.%s = %s" % (attr_name, backup)) # Restore original value from backup on failure
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
                    error_code = str(response.json()["response"][0]["errorCode"])

                    if error_code == "0":
                        return (True, "0", "")
                    else:
                        error_message = ""

                        if "errorString" in response.json()["response"][0]:
                            error_message = response.json()["response"][0]["errorString"]

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
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)


    def _filter_paths(self, paths, is_single_path=False):
        """Filters the paths based on the Operating System, and Agent.

            Args:
                paths           (list)  --  list containing paths to be filtered

                is_single_path  (bool)  --  boolean specifying whether to return a single path
                                                or the entire list

            Returns:
                list    -   if the boolean is_single_path is set to False

                str     -   if the boolean is_single_path is set to True
        """
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

        if is_single_path:
            return paths[0]
        else:
            return paths

    def _process_backup_response(self, flag, response):
        """Runs the Backup for a subclient with the request provided and returns the Job object.

            Args:
                update_request  (str)  --  update request specifying the details to update

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if job initialization failed

                    if response is empty

                    if response is not success
        """
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

    def _restore_json(
            self,
            paths,
            in_place=True,
            client=None,
            destination_path=None,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None):
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
                    "instanceName": self._backupset_object._instance_object.instance_name,
                    "instanceId": int(self._backupset_object._instance_object.instance_id),
                    "backupsetName": self._backupset_object.backupset_name,
                    "backupSetId": int(self._backupset_object.backupset_id),
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
                                "unconditionalOverwrite": overwrite,
                                "preserveLevel": 1,
                                "stripLevel": 2,
                                "stripLevelType": 0
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

        if copy_precedence:
            temp = {
                "browseOption": {
                    "mediaOption": {
                        "copyPrecedence": {
                            "copyPrecedenceApplicable": True,
                            "synchronousCopyPrecedence": copy_precedence,
                            "copyPrecedence": copy_precedence
                        }
                    }
                }
            }
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(temp)

        restore_option = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']

        if from_time and (from_time != '01/01/1970 00:00:00' and from_time != '1/1/1970 00:00:00'):
            temp = {
                "browseOption": {
                    "timeRange": {
                        "fromTimeValue": from_time
                    }
                }
            }

            if 'browseOption' in restore_option:
                if 'timeRange' in restore_option['browseOption']:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption']['timeRange'].update(temp['browseOption']['timeRange'])
                else:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption'].update(temp['browseOption'])
            else:
                request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(temp)

        if to_time and (to_time != '01/01/1970 00:00:00' and to_time != '1/1/1970 00:00:00'):
            temp = {
                "browseOption": {
                    "timeRange": {
                        "toTimeValue": to_time
                    }
                }
            }

            if 'browseOption' in restore_option:
                if 'timeRange' in restore_option['browseOption']:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption']['timeRange'].update(temp['browseOption']['timeRange'])
                else:
                    request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                        'browseOption'].update(temp['browseOption'])
            else:
                request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'].update(temp)

        return request_json

    def _backup_json(self,
                     backup_level,
                     incremental_backup,
                     incremental_level):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential / Synthetic_full

                incremental_backup  (bool)  --  run incremental backup
                        only applicable in case of Synthetic_full backup

                incremental_level   (str)   --  run incremental backup before/after synthetic full
                        BEFORE_SYNTH / AFTER_SYNTH

                        only applicable in case of Synthetic_full backup

            Returns:
                dict - JSON request to pass to the API
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

        return request_json

    def _process_restore_response(self, request_json):
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

    def _impersonation_json(self, Value):
        """setter of Impersonation Json entity of Json"""

        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._impersonation_json_ = {
            "useImpersonation": False,
            "user": {
                "userName": Value.get('username', "")
            }
        }


    def _restore_browse_option_json(self, Value):
        """setter  the Browse options for restore in Json"""

        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._browse_restore_json = {
            "listMedia": False,
            "useExactIndex": False,
            "noImage": False,
            "commCellId": 2,
            "mediaOption": {
                "mediaAgent": {
                    "mediaAgentName": ""
                },
                "library": {},
                "copyPrecedence": {
                    "copyPrecedenceApplicable": Value.get("copy_preceedence_applicable", False),
                    "copyPrecedence":Value.get("copy_preceedence", 0)
                },
                "drivePool": {}
            },
            "backupset": {
                "clientName": Value.get("client_name", ""),
                "appName": self._backupset_object._agent_object.agent_name
            },
            "timeZone": {
                "TimeZoneName": "(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi"
            },
            "timeRange": {}
        }

    def _restore_commonOptions_json(self, Value):
        """setter for  the Common options of in restore JSON"""
        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._commonoption_restore_json = {
            "systemStateBackup": False,
            "clusterDBBackedup": False,
            "powerRestore": False,
            "restoreToDisk": False,
            "offlineMiningRestore": False,
            "onePassRestore": False,
            "detectRegularExpression": True,
            "wildCard": False,
            "preserveLevel": Value.get("preserve_level", 0),
            "restoreToExchange":False,
            "stripLevel":0,
            "restoreACLs": Value.get("restore_ACL", True),
            "stripLevelType": Value.get("striplevel_type", 0),
            "unconditionalOverwrite": Value.get("unconditional_overwrite", False)
        }


    def _restore_destination_json(self, Value):
        """setter for  the destination restore option in restore JSON"""
        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._destination_restore_json = {
            "isLegalHold": False,
            "inPlace": True,
            "destPath": [Value.get("destination_path", "")],
            "destClient": {
                "clientName": Value.get("client_name", "")
            }
        }

    def _restore_fileoption_json(self, Value):
        """setter for  the fileoption restore option in restore JSON"""
        self._fileoption_restore_json = {
            "sourceItem": Value.get("source_item", []),
            "browseFilters": Value.get("browse_filters", [])
        }

    def _restore_sharepoint_json(self):
        """getter for Sharepoint restore option in JSON. it is read only attribute"""
        _sharepoint_restore_json = {
            "is90OrUpgradedClient": False
        }

        return _sharepoint_restore_json

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
    def _json_restore_subtask(self):
        """getter for the subtask in restore JSON . It is read only attribute"""

        _subtask_restore_json = {
            "subTaskType": 3,
            "operationType": 1001
        }

        return _subtask_restore_json

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
            snap_copy_info = self._commonProperties['snapCopyInfo']
            if 'isSnapBackupEnabled' in snap_copy_info:
                return bool(snap_copy_info['isSnapBackupEnabled'])

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

                    if the type of value input is not string
        """
        if isinstance(value, int):
            self._set_subclient_properties("_commonProperties['numberOfBackupStreams']", value)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient data readers should be an int value'
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
            self._set_subclient_properties("_commonProperties['description']", value)
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
                    if failed to update storage policy name

                    if storage policy name is not in string format
        """
        if isinstance(value, basestring):
            if value not in self._commcell_object.storage_policies._policies:
                raise SDKException(
                    'Subclient',
                    '102',
                    'Storage Policy: "{0}" does not exist in the Commcell'.format(value)
                )

        self._set_subclient_properties(
            "_commonProperties['storageDevice']['dataBackupStoragePolicy']['storagePolicyName']",
            value)

    def enable_backup(self):
        """Enables Backup for the subclient.

            Raises:
                SDKException:
                    if failed to enable backup of subclient
        """
        self._set_subclient_properties("_commonProperties['enableBackup']", True)

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
        self._set_subclient_properties("_commonProperties['enableBackup']", False)

    def enable_intelli_snap(self, snap_engine_name):
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

        self._set_subclient_properties("_commonProperties['snapCopyInfo']", properties_dict)

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
               collect_metadata=False,
               on_demand_input=None):
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

                on_demand_input     (str)   --  input directive file location for on
                                                    demand subclient

                        only applicable in case of on demand subclient
                    default: None

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """
        if on_demand_input is not None:
            if not isinstance(on_demand_input, basestring):
                raise SDKException('Subclient', '101')

            if not self.is_on_demand_subclient:
                raise SDKException(
                    'Subclient', '102', 'On Demand backup is not supported for this subclient'
                )

            on_demand = {
                "onDemandInputFile": on_demand_input
            }

            request_json = self._backup_json(backup_level, incremental_backup, incremental_level)

            request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(on_demand)

            backup_service = self._commcell_object._services['CREATE_TASK']

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

        else:
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

            backup_request += '&collectMetaInfo=%s'%collect_metadata

            backup_service = self._commcell_object._services['SUBCLIENT_BACKUP'] % (
                self.subclient_id, backup_request
            )

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', backup_service
            )

        return self._process_backup_response(flag, response)

    def browse(self, *args, **kwargs):
        """Browses the content of a Subclient.

            Args:
                Dictionary of browse options:
                    Example:
                        browse({
                            'path': 'c:\\hello',
                            'show_deleted': True,
                            'from_time': '2014-04-20 12:00:00',
                            'to_time': '2016-04-21 12:00:00'
                        })

                    (OR)

                Keyword argument of browse options:
                    Example:
                        browse(
                            path='c:\\hello',
                            show_deleted=True,
                            from_time='2014-04-20 12:00:00',
                            to_time='2016-04-21 12:00:00'
                        )

                Refer Backupset._default_browse_options for all the supported options

        Returns:
            list - List of only the file, folder paths from the browse response

            dict - Dictionary of all the paths with additional metadata retrieved from browse
        """
        if len(args) > 0 and type(args[0]) == dict:
            options = args[0]
        else:
            options = kwargs

        options['_subclient_id'] = self._subclient_id

        return self._backupset_object.browse(options)

    def find(self, *args, **kwargs):
        """Searches a file/folder in the subclient backup content,
            and returns all the files matching the filters given.

         Args:
            Dictionary of find options:
                Example:
                    find({
                        'file_name': '*.txt',
                        'show_deleted': True,
                        'from_time': '2014-04-20 12:00:00',
                        'to_time': '2016-04-21 12:00:00'
                    })

                (OR)

            Keyword argument of find options:
                Example:
                    find(
                        file_name='*.txt',
                        show_deleted=True,
                        from_time=2014-04-20 12:00:00,
                        to_time='2016-04-21 12:00:00'
                    )

            Refer Backupset._default_browse_options for all the supported options

            Additional options supported:
                file_name       (str)   --   Find files with name

                file_size_gt    (int)   --   Find files with size greater than size

                file_size_lt    (int)   --   Find files with size lesser than size

                file_size_et    (int)   --   Find files with size equal to size

        Returns:
            list - List of only the file, folder paths from the browse response

            dict - Dictionary of all the paths with additional metadata retrieved from browse
        """
        if len(args) > 0 and type(args[0]) == dict:
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
            to_time=None):
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

        paths = self._filter_paths(paths)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time)

        return self._process_restore_response(request_json)

    def restore_out_of_place(
            self,
            client,
            destination_path,
            paths,
            overwrite=True,
            restore_data_and_acl=True,
            copy_precedence=None,
            from_time=None,
            to_time=None):
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

        if not ((isinstance(client, basestring) or isinstance(client, Client)) and
                isinstance(destination_path, basestring) and
                isinstance(paths, list) and
                isinstance(overwrite, bool) and
                isinstance(restore_data_and_acl, bool)):
            raise SDKException('Subclient', '101')

        if isinstance(client, Client):
            client = client
        elif isinstance(client, basestring):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        paths = self._filter_paths(paths)

        destination_path = self._filter_paths([destination_path], True)

        if paths == []:
            raise SDKException('Subclient', '104')

        request_json = self._restore_json(
            paths=paths,
            in_place=False,
            client=client,
            destination_path=destination_path,
            overwrite=overwrite,
            restore_data_and_acl=restore_data_and_acl,
            copy_precedence=copy_precedence,
            from_time=from_time,
            to_time=to_time
        )

        return self._process_restore_response(request_json)
