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
from ..subclient import Subclient as subclient
from typing import Any, Optional, List, Dict, Union, Tuple

class VSBackupset(Backupset):
    """
    Represents a Virtual Server (VS) backupset, derived from the Backupset base class.

    This class provides specialized operations for managing and interacting with VS backupsets,
    including browsing backup content, handling subclients, and applying filters for virtual machines
    and disks. It also supports configuration and management of index servers associated with the backupset.

    Key Features:
        - Creation of VS backupset instances with custom parameters
        - Browsing backupset content
        - Processing browse responses with customizable options
        - Access to hidden subclient information
        - Management of index server properties
        - Application of VM filters to control backup content
        - Application of VM disk filters for granular backup selection

    #ai-gen-doc
    """

    def __new__(cls, instance_object: Any, backupset_name: str, backupset_id: Optional[str] = None) -> Any:
        """Create a new VSBackupset instance based on the provided instance object.

        This method dynamically determines the appropriate backupset class to instantiate
        based on the type and name of the given instance_object. If a matching backupset
    class is found, an instance of that class is created; otherwise, a generic VSBackupset
        instance is returned.

        Args:
        instance_object: The instance object representing the virtual server environment.
        backupset_name: The name of the backupset as a string.
        backupset_id: Optional identifier for the backupset.

        Returns:
        An instance of the appropriate backupset class, or a generic VSBackupset instance
        if no specific class is found.

        Example:
        >>> instance = VirtualServerInstance(...)
        >>> backupset = VSBackupset(instance, "DailyBackup", backupset_id="12345")
        >>> print(type(backupset))
        >>> # The returned object will be of the correct backupset subclass based on the instance

        #ai-gen-doc
        """
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

    @property
    def hidden_subclient(self) -> 'subclient':
        """Get the hidden subclient object associated with this VSBackupset.

        This property creates and returns the hidden subclient if it does not already exist.
        The hidden subclient is typically used for internal backup operations and is not visible in standard subclient listings.

        Returns:
            subclient: The hidden subclient object for this backupset.

        Example:
            >>> vs_backupset = VSBackupset(...)
            >>> hidden_sc = vs_backupset.hidden_subclient  # Use dot notation for property access
            >>> print(f"Hidden subclient: {hidden_sc}")
            >>> # The returned subclient object can be used for further backup operations

        #ai-gen-doc
        """
        if not self._hidden_subclient:
            hidden_subclient_service = self._commcell_object._services['VSA_HIDDEN_SUBCLIENT'] % (
                self._client_object.client_name, self.backupset_name)
            flag, response = self._commcell_object._cvpysdk_object.make_request(
                "GET", hidden_subclient_service)
            if flag:
                if response.json():
                    hidden_subclient_id = response.json().get('subclientId')
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
            self._hidden_subclient = subclient(self, 'Do Not Backup', hidden_subclient_id)
        return self._hidden_subclient

    def browse(self, *args: Any, **kwargs: Any) -> Tuple[List[str], Dict[str, Any]]:
        """Browse the content of the backupset using specified options.

        This method allows you to retrieve file and folder paths from the backupset, 
        along with additional metadata. You can specify browse options either as a 
        dictionary or as keyword arguments.

        Args:
            *args: Optional positional argument containing a dictionary of browse options.
                Example:
                    >>> backupset.browse({
                    ...     'path': 'c:\\hello',
                    ...     'show_deleted': True,
                    ...     'from_time': '2014-04-20 12:00:00',
                    ...     'to_time': '2016-04-21 12:00:00'
                    ... })

            **kwargs: Optional keyword arguments for browse options.
                Example:
                    >>> backupset.browse(
                    ...     path='c:\\hello',
                    ...     show_deleted=True,
                    ...     from_time='2014-04-20 12:00:00',
                    ...     to_time='2016-04-21 12:00:00'
                    ... )

        Returns:
            A tuple containing:
                - List of file and folder paths from the browse response.
                - Dictionary with all paths and additional metadata retrieved from the browse operation.

        Example:
            >>> # Using a dictionary of options
            >>> file_list, metadata = backupset.browse({
            ...     'path': '/data',
            ...     'show_deleted': False,
            ...     'from_time': '2023-01-01 00:00:00',
            ...     'to_time': '2023-12-31 23:59:59'
            ... })
            >>> print(file_list)
            >>> print(metadata)

            >>> # Using keyword arguments
            >>> file_list, metadata = backupset.browse(
            ...     path='/data',
            ...     show_deleted=True
            ... )
            >>> print(file_list)
            >>> print(metadata)
        #ai-gen-doc
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['retry_count'] = 0
        return self._do_browse(options)

    def _process_browse_response(self, flag: bool, response: Any, options: Dict[str, Any]) -> Union[List[str], Tuple[List[str], Dict[str, Any]]]:
        """Process the browse response and retrieve file or folder paths with metadata.

        This method analyzes the browse response from the server and extracts a list of file or folder paths,
        along with a dictionary containing metadata for each path. It handles error scenarios, retries if necessary,
        and supports options such as showing deleted items.

        Args:
            flag: Boolean indicating whether the response was successful.
            response: The response object received from the server (should support .json()).
            options: Dictionary of browse options, such as retry count and operation type.

        Returns:
            A tuple containing:
                - List of file or folder paths extracted from the browse response.
                - Dictionary mapping each path to its metadata (name, size, type, backup time, etc.).

            In certain cases, may return an empty list and dictionary if no items are found.

        Raises:
            SDKException: If browsing/searching for content fails, the response is empty, or the response indicates failure.

        Example:
            >>> options = {'retry_count': 0, 'operation': 'browse', 'path': 'C:\\Data'}
            >>> flag = True  # Assume the response was successful
            >>> response = server.get_browse_response()  # Should be a response object with .json()
            >>> paths, metadata = backupset._process_browse_response(flag, response, options)
            >>> print(f"Found {len(paths)} items")
            >>> for path in paths:
            ...     print(f"Path: {path}, Metadata: {metadata[path]}")
        #ai-gen-doc
        """
        paths_dict = {}
        paths = []
        result_set = None
        browse_result = None
        error_message = None
        options['retry_count'] = options['retry_count'] + 1
        show_deleted = options.get('show_deleted', False)

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
                        if not isinstance(response_json['browseResponses'][0]['messages'], list):
                            response_json['browseResponses'][0]['messages'] = [
                                response_json['browseResponses'][0]['messages']]
                        message = response_json['browseResponses'][0]['messages'][0]
                        error_message = message['errorMessage']
                        if error_message == 'Please note that this is a live browse operation. Live browse operations can take some time before the results appear in the browse window.':
                            return [], {}
                        raise SDKException('Backupset', '102', str(error_message))

                    else:
                        return [], {}

                if not result_set:
                    raise SDKException('Backupset', '108', "Failed to browse for subclient backup content")

                if 'all_versions' in options['operation']:
                    return self._process_browse_all_versions_response(result_set,options)

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

                    if 'backupTime' in result['advancedData'] and int(result['advancedData']['backupTime']) > 0:
                        bkp_time = time.localtime(int(result['advancedData']['backupTime']))
                        bkp_time = time.strftime('%d/%m/%Y %H:%M:%S', bkp_time)
                    else:
                        bkp_time = None

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
                        
                    if show_deleted and 'deleted' in result.get('flags'):
                        deleted = True if result['flags'].get('deleted') in (True, '1') else False
                    else:
                        deleted = None

                    paths_dict[path] = {
                        'name': name,
                        'snap_display_name': snap_display_name,
                        'size': size,
                        'modified_time': mod_time,
                        'type': file_or_folder,
                        'backup_time': bkp_time,
                        'advanced_data': result['advancedData'],
                        'deleted': deleted
                    }

                    paths.append(path)

                return paths, paths_dict

        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def index_server(self) -> Optional['Client']:
        """Get the index server client configured for this backupset.

        Returns:
            Client instance representing the index server if set, or None if no index server is configured.

        Example:
            >>> backupset = VSBackupset(commcell_object, ...)
            >>> index_server_client = backupset.index_server  # Use dot notation for property access
            >>> if index_server_client:
            >>>     print(f"Index server client name: {index_server_client.client_name}")
            >>> else:
            >>>     print("No index server is configured for this backupset.")

        #ai-gen-doc
        """

        client_name = None

        if 'indexSettings' in self._properties:
            if 'currentIndexServer' in self._properties['indexSettings']:
                client_name = self._properties['indexSettings']['currentIndexServer']['clientName']

        if client_name is not None:
            return Client(self._commcell_object, client_name=client_name)

        return None

    @index_server.setter
    def index_server(self, value: 'Client') -> None:
        """Set the index server client for the backupset.

        This property setter assigns a Client object as the index server for the backupset.
        The provided client must be a qualified index server client; otherwise, an exception is raised.

        Args:
            value: Client object representing the index server to assign.

        Raises:
            SDKException: If the provided client is not a valid Client object,
                or if the client is not a qualified index server.

        Example:
            >>> index_server_client = Client(...)
            >>> backupset = VSBackupset(...)
            >>> backupset.index_server = index_server_client  # Use assignment for property setters
            >>> # The index server for the backupset is now set

        #ai-gen-doc
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

    @property
    def vm_filter(self) -> List[Any]:
        """Get the VM filters set at the backupset level.

        Returns:
            List containing the content associated as filters with the backupset.

        Example:
            >>> backupset = VSBackupset(...)
            >>> filters = backupset.vm_filter  # Use dot notation for property access
            >>> print(f"VM filters: {filters}")
            >>> # The returned list contains all VM filter criteria for this backupset

        #ai-gen-doc
        """

        return self.hidden_subclient.content

    @vm_filter.setter
    def vm_filter(self, content: List[Dict[str, Any]]) -> None:
        """Set the VM filter content for the backupset.

        This setter updates the VM filter of the backupset by providing a list of filter criteria.
        Each filter should be represented as a dictionary containing the filter's name and type.

        Args:
            content: A list of dictionaries, where each dictionary specifies a filter with 'name' and 'type' keys.

        Example:
            >>> filters = [
            ...     {'name': 'VM01', 'type': 'VirtualMachine'},
            ...     {'name': 'Production', 'type': 'Tag'}
            ... ]
            >>> backupset = VSBackupset(...)
            >>> backupset.vm_filter = filters  # Use assignment for property setters
            >>> # The VM filter content is now updated for the backupset

        #ai-gen-doc
        """
        self.hidden_subclient.content = content
        self.hidden_subclient.refresh()

    @property
    def vm_disk_filter(self) -> List[Any]:
        """Get the VM disk filters configured at the backupset level.

        Returns:
            List containing the disk filter content associated with the backupset.

        Example:
            >>> backupset = VSBackupset(...)
            >>> disk_filters = backupset.vm_disk_filter  # Use dot notation for property access
            >>> print(f"Disk filters: {disk_filters}")
            >>> # The returned list contains all disk filters set for this backupset

        #ai-gen-doc
        """
        return self.hidden_subclient.vm_diskfilter

    @vm_disk_filter.setter
    def vm_disk_filter(self, vm_diskfilter: List[Any]) -> None:
        """Set the disk filter list for the VM backupset.

        This setter updates the disk filter content for the backupset by passing the provided
        list of disk filters to the underlying subclient and refreshing its state.

        Args:
            vm_diskfilter: List of disk filters to add to the backupset. Each item should represent
                a disk filter configuration as required by the backupset API.

        Example:
            >>> disk_filters = [
            ...     {"diskName": "Hard disk 1", "exclude": True},
            ...     {"diskName": "Hard disk 2", "exclude": False}
            ... ]
            >>> vs_backupset = VSBackupset(...)
            >>> vs_backupset.vm_disk_filter = disk_filters  # Use assignment for property setter
            >>> # The disk filter list is now updated for the backupset

        #ai-gen-doc
        """
        self.hidden_subclient.vm_diskfilter = vm_diskfilter
        self.hidden_subclient.refresh()
