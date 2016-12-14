#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing sublcient operations.

Subclients and Subclient are 2 classes defined in this file.

Subclients: Class for representing all the subclients associated with a backupset

Subclient: Class for representing a single subclient, and to perform operations on that subclient


Subclients:
    __init__(backupset_object)  --  initialise object of subclients object associated with
                                        the specified backup set.
    __str__()                   --  returns all the subclients associated with the backupset
    __repr__()                  --  returns the string for the instance of the Subclients class
    _get_subclients()           --  gets all the subclients associated with the backupset specified
    has_subclient()             --  checks if a subclient exists with the given name or not
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
    backup()                    --  run a backup job for the subclient
    browse()                    --  gets the content of the backup for this subclient
                                        at the path specified
    browse_in_time()            --  gets the content of the backup for this subclient
                                        at the input path in the time range specified
    restore_in_place()          --  Restores the files/folders specified in the
                                        input paths list to the same location
    restore_out_of_place()      --  Restores the files/folders specified in the input paths list
                                        to the input client, at the specified destionation location
"""

import re
import math
import time
import urllib

from job import Job
from schedules import Schedules
from exception import SDKException


class Subclients(object):
    """Class for getting all the subclients associated with a client."""

    def __init__(self, backupset_object):
        """Initialize the Sublcients object for the given backupset.

            Args:
                backupset_object (object)  --  instance of the Backupset class

            Returns:
                object - instance of the Subclients class
        """
        self._backupset_object = backupset_object
        self._commcell_object = self._backupset_object._commcell_object

        self._ALL_SUBCLIENTS = self._commcell_object._services.GET_ALL_SUBCLIENTS % (
            self._backupset_object._agent_object._client_object.client_id)

        self._subclients = self._get_subclients()

    def __str__(self):
        """Representation string consisting of all subclients of the backupset.

            Returns:
                str - string of all the subclients of th backupset of an agent of a client
        """
        representation_string = '{:^5}\t{:^20}\t{:^20}\t{:^20}\t{:^20}\n\n'.format(
            'S. No.', 'Subclient', 'Backupset', 'Agent', 'Client')

        for index, subclient in enumerate(self._subclients):
            sub_str = '{:^5}\t{:20}\t{:20}\t{:20}\t{:20}\n'.format(
                index + 1,
                subclient,
                self._backupset_object.backupset_name,
                self._backupset_object._agent_object.agent_name,
                self._backupset_object._agent_object._client_object.client_name)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the Subclients class."""
        return "Subclients class instance for Backupset: '{0}'".format(
            self._backupset_object.backupset_name)

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
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET',
                                                                            self._ALL_SUBCLIENTS)

        if flag:
            if response.json() and 'subClientProperties' in response.json():
                return_dict = {}

                for dictionary in response.json()['subClientProperties']:
                    backupset = str(dictionary['subClientEntity']['backupsetName']).lower()

                    if self._backupset_object.backupset_name in backupset:
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

            if self.has_subclient(subclient_name):
                return Subclient(self._backupset_object,
                                 subclient_name,
                                 self._subclients[subclient_name])

            raise SDKException('Subclient',
                               '102',
                               'No subclient exists with name: {0}'.format(subclient_name))

    def delete(self, subclient_name):
        """Deletes the subclient specified by the subclient_name from the backupset.

            Args:
                subclient_name (str)  --  name of the subclient to remove from the backupset

            Returns:
                None

            Raises:
                SDKException:
                    if type of the subclient name argument is not string
                    if response is empty
                    if response is not success
                    if no subclient exists with the given name
        """
        if not isinstance(subclient_name, str):
            raise SDKException('Subclient', '101')
        else:
            subclient_name = str(subclient_name).lower()

        if self.has_subclient(subclient_name):
            delete_subclient_service = self._commcell_object._services.SUBCLIENT % \
                (self._subclients[subclient_name])

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'DELETE', delete_subclient_service)

            if flag:
                if response.json():
                    if 'response' in response.json():
                        response_value = response.json()['response'][0]
                        error_code = str(response_value['errorCode'])
                        error_message = None

                        if 'errorString' in response_value:
                            error_message = str(response_value['errorString'])

                        if error_message:
                            o_str = 'Failed to delete subclient with error code: "{0}", error: "{1}"'
                            print o_str.format(error_code, error_message)
                        else:
                            if error_code is '0':
                                print "Sub Client {0} deleted successfully".format(subclient_name)

                                # initialize the subclients again
                                # so the subclient object has all the subclients
                                self._subclients = self._get_subclients()
                            else:
                                o_str = 'Failed to delete subclient with error code: "{0}"'
                                print o_str.format(error_code)
                                print 'Please check the documentation for more details on the error'
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        else:
            raise SDKException('Subclient',
                               '102',
                               'No subclient exists with name: {0}'.format(subclient_name))


class Subclient(object):
    """Class for performing backupset operations for a specific backupset."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialise the Subclient object.

            Args:
                backupset_object (object)  --  instance of the Backupset class
                subclient_name (str)       --  name of the subclient
                subclient_id (str)         --  id of the subclient
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
        self.properties = self._get_subclient_properties()
        self._BACKUP = None

        self._BROWSE = self._commcell_object._services.BROWSE
        self._RESTORE = self._commcell_object._services.RESTORE

        self.schedules = Schedules(self)

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Subclient class instance for Subclient: "{0}" of Backupset: "{1}"'
        return representation_string.format(
            self.subclient_name, self._backupset_object.backupset_name)

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
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @staticmethod
    def _convert_size(input_size):
        """Converts the given float size to appropriate size in KB / MB / GB, etc.

            Args:
                size (float)  --  float value to convert

            Returns:
                str - size converted to the specific type (B, KB, MB, GB, etc.)
        """
        if input_size == 0:
            return '0B'
        size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(input_size, 1024)))
        power = math.pow(1024, i)
        size = round(input_size / power, 2)
        return '%s %s' % (size, size_name[i])

    @property
    def subclient_id(self):
        """Treats the subclient id as a read-only attribute."""
        return self._subclient_id

    @property
    def subclient_name(self):
        """Treats the subclient name as a read-only attribute."""
        return self._subclient_name

    def backup(
            self,
            backup_level="Incremental",
            incremental_backup=False,
            incremental_level='BEFORE_SYNTH'):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level (str)         --  level of backup the user wish to run
                        Full / Incremental / Synthetic_full
                    default: Incremental

                incremental_backup (bool)  --  run incremental backup
                        only applicable in case of Synthetic_full backup
                    default: False

                incremental_level (str)    --  run incremental backup before / after synthetic full
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
        if backup_level not in ['full', 'incremental', 'synthetic_full']:
            raise SDKException('Subclient', '103')

        self._BACKUP = self._commcell_object._services.SUBCLIENT_BACKUP % (
            self.subclient_id, backup_level)

        if backup_level == 'synthetic_full':
            if incremental_backup:
                self._BACKUP += '&runIncrementalBackup=True'
                self._BACKUP += '&incLevel=%s' % (incremental_level.lower())
            else:
                self._BACKUP += '&runIncrementalBackup=False'

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            self._BACKUP)
        if flag:
            if response.json():
                if "jobIds" in response.json():
                    print '{0} Backup job started for subclient: "{1}" with job id: "{2}"'.format(
                        str(backup_level).capitalize(),
                        self.subclient_name,
                        response.json()['jobIds'][0])

                    time.sleep(1)
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    o_str = "Initializing backup failed with error code: %s" % \
                        (response.json()['errorCode'])
                    o_str += "\nError message: %s" % (response.json()['errorMessage'])
                    raise SDKException('Subclient', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def browse(self, path, show_deleted_files=False, vm_file_browse=False, vm_disk_browse=False):
        """Gets the content of the backup for this subclient at the path specified.

            Args:
                path (str)                  --  folder path to get the contents of
                show_deleted_files (bool)   --  include deleted files in the content or not
                    default: False
                vm_file_browse (bool)       --  browse files and folders inside
                                                    a guest virtual machine
                    only applicable when browsing content inside a guest virtual machine
                    default: False
                vm_disk_browse (bool)       --  browse virtual machine files
                                                    e.g.; .vmdk files, etc.
                    only applicable when browsing content inside a guest virtual machine
                    default: False

            Returns:
                list - list of all folders or files with their full paths inside the input path
                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if response is empty
                    if response is not success
        """
        web_service = self._SUBCLIENT + '/Browse?'
        encode_dict = {
            'path': path,
            'showDeletedFiles': show_deleted_files,
            'vsFileBrowse': vm_file_browse,
            'vsDiskBrowse': vm_disk_browse
        }

        web_service += urllib.urlencode(encode_dict)

        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', web_service)

        if flag:
            if response.json() and 'browseResponses' in response.json():
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

                        # convert bits to bytes and then pass to convert_size
                        size = self._convert_size(float(result['size']) / 8.0)

                        temp = {
                            path: [name, file_or_folder, size, mod_time]
                        }

                        paths.append(path)
                        full_result.append(temp)

                    return paths, full_result
                elif 'aggrResultSet' in browse_result:
                    aggr_result_set = browse_result['aggrResultSet']
                    if aggr_result_set[0]['count'] == 0:
                        print 'No data found at the path specified.'
                else:
                    print 'Did not get the expected data'
                    print response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def browse_in_time(self,
                       path,
                       show_deleted_files=True,
                       restore_index=True,
                       from_date=None,
                       to_date=None):
        """Gets the content of the backup for this subclient
            at the path specified in the time range specified.

            Args:
                path (str)                  --  folder path to get the contents of
                show_deleted_files (bool)   --  include deleted files in the content or not
                    default: True
                restore_index (bool)        --  restore index if it is not cached
                    default: True
                from_date (str)             --  date to get the contents after
                        format: dd/MM/YYYY
                        gets contents from 01/01/1970 if not specified
                    default: None
                to_date (str)               --  date to get the contents before
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

        request_json = {
            "opType": 0,
            "queries": [
                {
                    "type": 0,
                    "queryId": "dataQuery",
                    "dataParam": {
                        "sortParam": {
                            "ascending": False,
                            "sortBy": [0]
                        }
                    }
                }
            ],
            "mode": {
                "mode": 2
            },
            "paths": [
                {
                    "path": path
                }
            ],
            "options": {
                "showDeletedFiles": show_deleted_files,
                "restoreIndex": restore_index
            },
            "entity": {
                "subclientId": int(self.subclient_id),
                "applicationId": int(self._backupset_object._agent_object.agent_id),
                "clientName": self._backupset_object._agent_object._client_object.client_name,
                "backupsetId": int(self._backupset_object.backupset_id),
                "instanceId": int(self._backupset_object._instance_id),
                "clientId": int(self._backupset_object._agent_object._client_object.client_id)
            },
            "timeRange": {
                "fromTime": from_date,
                "toTime": to_date
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            self._BROWSE,
                                                                            request_json)

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

                            # convert bits to bytes and then pass to convert_size
                            size = self._convert_size(float(result['size']) / 8.0)

                            temp = {
                                path: [name, file_or_folder, size, mod_time]
                            }

                            paths.append(path)
                            full_result.append(temp)

                        return paths, full_result
                    else:
                        print 'No data found at the path specified.'
                elif 'messages' in response.json()['browseResponses'][0]:
                    message = response.json()['browseResponses'][0]['messages'][0]
                    error_code = message['errorCode']
                    error_message = message['errorMessage']

                    print "Failed to browse for subclient backup content with error code: %s" % (error_code)
                    print "Error message: %s" % (error_message)
                else:
                    print 'No data found at the path specified.'
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def restore_in_place(self,
                         paths,
                         overwrite=True,
                         restore_deleted_files=True,
                         restore_data_and_acl=True):
        """Restores the files/folders specified in the input paths list to the same location.

            Args:
                paths (list)                    --  list of full paths of files/folders to restore
                overwrite (bool)                --  unconditional overwrite files during restore
                    default: True
                restore_deleted_files (bool)    --  restore files that have been deleted on media
                    default: True
                restore_data_and_acl (bool)     --  restore data and ACL files
                    default: True

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list
                    if response is empty
                    if response is not success
        """
        if not isinstance(paths, list):
            raise SDKException('Subclient', '102', '"paths" should be of "list" type')

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
            paths[index] = path

        request_json = {
            "mode": 2,
            "serviceType": 1,
            "userInfo": {
                "userGuid": self._commcell_object._Commcell__user_guid
            },
            "advanced": {
                "restoreDataAndACL": restore_data_and_acl,
                "restoreDeletedFiles": restore_deleted_files,
                "unconditionalOverwrite": overwrite
            },
            "header": {
                "destination": {
                    "clientId": int(self._backupset_object._agent_object._client_object.client_id),
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "inPlace": True
                },
                "filePaths": paths,
                "srcContent": {
                    "subclientId": int(self.subclient_id),
                    "clientId": int(self._backupset_object._agent_object._client_object.client_id),
                    "instanceId": int(self._backupset_object._instance_id),
                    "backupSetId": int(self._backupset_object.backupset_id),
                    "appTypeId": int(self._backupset_object._agent_object.agent_id)
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            self._RESTORE,
                                                                            request_json)

        if flag:
            if response.json():
                if "jobId" in response.json():
                    print 'Restore job started for subclient: "{0}" with job id: "{1}"'.format(
                        self.subclient_name,
                        response.json()['jobId']
                    )

                    time.sleep(1)
                    return Job(self._commcell_object, response.json()['jobId'])
                elif "errList" in response.json():
                    error_code = response.json()['errList'][0]['errorCode']
                    error_message = response.json()['errList'][0]['errLogMessage']

                    o_str = "Restore job failed with error code: %s" % (error_code)
                    o_str += "\nError message: %s" % (error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def restore_out_of_place(self,
                             client,
                             destination_path,
                             paths,
                             overwrite=True,
                             restore_deleted_files=True,
                             restore_data_and_acl=True):
        """Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                client (str/object)             --  either the name of the client or
                                                        the instance of the Client
                destination_path (str)          --  full path of the restore location on client
                paths (list)                    --  list of full paths of files/folders to restore
                overwrite (bool)                --  unconditional overwrite files during restore
                    default: True
                restore_deleted_files (bool)    --  restore files that have been deleted on media
                    default: True
                restore_data_and_acl (bool)     --  restore data and ACL files
                    default: True

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if client is not a string or Client instance
                    if destination_path is not a string
                    if paths is not a list
                    if response is empty
                    if response is not success
        """
        from client import Client

        if not ((isinstance(client, str) or isinstance(client, Client)) and
                isinstance(destination_path, str) and
                isinstance(paths, list)):
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

        request_json = {
            "mode": 2,
            "serviceType": 1,
            "userInfo": {
                "userGuid": self._commcell_object._Commcell__user_guid
            },
            "advanced": {
                "restoreDataAndACL": restore_data_and_acl,
                "restoreDeletedFiles": restore_deleted_files,
                "unconditionalOverwrite": overwrite
            },
            "header": {
                "destination": {
                    "clientId": int(client.client_id),
                    "clientName": client.client_name,
                    "inPlace": False,
                    "destPath": [destination_path]
                },
                "filePaths": paths,
                "srcContent": {
                    "subclientId": int(self.subclient_id),
                    "clientId": int(self._backupset_object._agent_object._client_object.client_id),
                    "instanceId": int(self._backupset_object._instance_id),
                    "backupSetId": int(self._backupset_object.backupset_id),
                    "appTypeId": int(self._backupset_object._agent_object.agent_id)
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request('POST',
                                                                            self._RESTORE,
                                                                            request_json)

        if flag:
            if response.json():
                if "jobId" in response.json():
                    print 'Restore job started for subclient: "{0}" with job id: "{1}"'.format(
                        self.subclient_name,
                        response.json()['jobId']
                    )

                    time.sleep(1)
                    return Job(self._commcell_object, response.json()['jobId'])
                elif "errorList" in response.json():
                    error_code = response.json()['errorList'][0]['errorCode']
                    error_message = response.json()['errorList'][0]['errLogMessage']

                    o_str = "Restore job failed with error code: %s" % (error_code)
                    o_str += "\nError message: %s" % (error_message)
                    raise SDKException('Subclient', '102', o_str)
                else:
                    raise SDKException('Subclient', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
