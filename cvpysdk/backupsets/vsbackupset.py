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

"""Module for performing operations on a Backupset for the **Virtual Server** Agent.

VSBackupset is the only class defined in this file.

VSBackupset:

    browse()                        -- browse the content of the backupset
    _process_browse_response()      -- retrieves the items from browse response

    To add a new Virtual Backupset, create a class in a new module under _virtual_server sub package


The new module which is created has to named in the following manner:
1. Name the module with the name of the Virtual Server without special characters
2.Spaces alone must be replaced with underscores('_')

For eg:

    The Virtual Server 'Red Hat Virtualization' is named as 'red_hat_virtualization.py'

    The Virtual Server 'Hyper-V' is named as 'hyperv.py'
"""

from __future__ import unicode_literals

import re
import time
from importlib import import_module
from inspect import isabstract, isclass, getmembers

from ..backupset import Backupset
from ..client import Client
from ..exception import SDKException


class VSBackupset(Backupset):
    """Derived class from Backupset Base class, representing a vs backupset,
            and to perform operations on that backupset."""

    def __new__(cls, instance_object, backupset_name, backupset_id=None):
        """Decides which instance object needs to be created"""
        instance_name = instance_object.instance_name
        instance_name = re.sub('[^A-Za-z0-9_]+', '', instance_name.replace(" ", "_"))

        try:
            backupset_module = import_module("cvpysdk.backupsets._virtual_server.{}".format(instance_name))
        except ImportError:
            return object.__new__(cls)

        classes = getmembers(backupset_module, lambda m: isclass(m) and not isabstract(m))

        for name, _class in classes:
            if issubclass(_class, Backupset) and _class.__module__.rsplit(".", 1)[-1] == instance_name:
                return object.__new__(_class)

    def browse(self, *args, **kwargs):
        """Browses the content of the Backupset.

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
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['retry_count'] = 0
        return self._do_browse(options)

    def _process_browse_response(self, flag, response, options):
        """Retrieves the items from browse response.

                Args:
                    flag        (bool)  --  boolean, whether the response was success or not

                    response    (dict)  --  JSON response received for the request from the Server

                    options     (dict)  --  The browse options dictionary

                Returns:
                    list - List of only the file / folder paths from the browse response

                    dict - Dictionary of all the paths with additional metadata retrieved from browse

                Raises:
                    SDKException:
                        if failed to browse/search for content

                        if response is empty

                        if response is not success
                """
        paths_dict = {}
        paths = []
        result_set = None
        browse_result = None
        error_message = None
        options['retry_count'] = options['retry_count'] + 1

        if flag:
            response_json = response.json()
            if response_json and 'browseResponses' in response_json:
                _browse_responses = response_json['browseResponses']
                if not isinstance(_browse_responses, list):
                    _browse_responses = [_browse_responses]
                for browse_response in _browse_responses:
                    resp_type = browse_response['respType']
                    if 'messages' in browse_response:
                        # checking if it is not a list, then converting it to list
                        if not isinstance(browse_response['messages'], list):
                            browse_response['messages'] = [browse_response['messages']]
                        message = browse_response['messages'][0]
                        error_message = message['errorMessage']
                        if resp_type == 2 or resp_type == 3 and 'No items found in the index, possibly index is being rebuilt' in \
                                error_message:
                            if options['retry_count'] <= 3:
                                time.sleep(180)
                                return self._do_browse(options)
                            else:
                                err = "Maximum browse attemps exhausted. Browse did not give full results"
                                raise Exception(err)
                    if "browseResult" in browse_response:
                        browse_result = browse_response['browseResult']
                        if 'dataResultSet' in browse_result:
                            result_set = browse_result['dataResultSet']
                            if not isinstance(result_set, list):
                                result_set = [result_set]
                            break
                if not browse_result:
                    if not isinstance(response_json['browseResponses'], list):
                        response_json['browseResponses'] = [response_json['browseResponses']]
                    if 'messages' in response_json['browseResponses'][0]:
                        if not isinstance(response_json['browseResponses'][0]['messages'],list):
                            response_json['browseResponses'][0]['messages'] = [response_json['browseResponses'][0]['messages']]
                        message = response_json['browseResponses'][0]['messages'][0]
                        error_message = message['errorMessage']
                        if error_message == 'Please note that this is a live browse operation. Live browse operations can take some time before the results appear in the browse window.':
                            return [], {}
                        raise SDKException('Backupset', '102', str(error_message))

                    else:
                        return [], {}

                if not result_set:
                    raise SDKException('Backupset', '110', "Failed to browse for subclient backup content")

                if 'all_versions' in options['operation']:
                    return self._process_browse_all_versions_response(result_set)

                for result in result_set:
                    name = result.get('displayName')
                    snap_display_name = result.get('name')

                    if 'path' in result:
                        path = result['path']
                    else:
                        path = '\\'.join([options['path'], name])

                    if 'modificationTime' in result and int(result['modificationTime']) > 0:
                        mod_time = time.localtime(int(result['modificationTime']))
                        mod_time = time.strftime('%d/%m/%Y %H:%M:%S', mod_time)
                    else:
                        mod_time = None

                    if 'file' in result['flags']:
                        if result['flags']['file'] is True or result['flags']['file'] == "1":
                            file_or_folder = 'File'
                        else:
                            file_or_folder = 'Folder'
                    else:
                        file_or_folder = 'Folder'

                    if 'size' in result:
                        size = result['size']
                    else:
                        size = None

                    paths_dict[path] = {
                        'name': name,
                        'snap_display_name': snap_display_name,
                        'size': size,
                        'modified_time': mod_time,
                        'type': file_or_folder,
                        'advanced_data': result['advancedData']
                    }

                    paths.append(path)

                return paths, paths_dict

        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def index_server(self):
        """Returns the index server client set for the backupset"""

        client_name = None

        if 'indexSettings' in self._properties:
            if 'currentIndexServer' in self._properties['indexSettings']:
                client_name = self._properties['indexSettings']['currentIndexServer']['clientName']

        if client_name is not None:
            return Client(self._commcell_object, client_name=client_name)

        return None

    @index_server.setter
    def index_server(self, value):
        """Sets index server client for the backupset. Property value should be a client object

            Args:

                value     (obj)    --  The cvpysdk client object of the index server client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        if not isinstance(value, Client):
            raise SDKException('Backupset', '106')

        properties = self._properties
        index_server_id = int(value.client_id)
        index_server_name = value.client_name

        if 'indexSettings' in properties:
            qualified_index_servers = []
            if 'qualifyingIndexServers' in properties['indexSettings']:
                for index_server in properties['indexSettings']['qualifyingIndexServers']:
                    qualified_index_servers.append(index_server['clientId'])

            if index_server_id in qualified_index_servers:
                properties['indexSettings']['currentIndexServer'] = {
                    'clientId': index_server_id,
                    'clientName': index_server_name
                }
            else:
                raise SDKException(
                    'Backupset', '102', '{0} is not a qualified IndexServer client'.format(
                        index_server_name))
        else:
            properties['indexSettings'] = {
                'currentIndexServer': {
                    'clientId': index_server_id,
                    'clientName': index_server_name
                }
            }

        request_json = {
            'backupsetProperties': properties
        }

        self._process_update_reponse(request_json)
