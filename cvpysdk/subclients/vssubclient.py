#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Subclient.

VirualServerSubclient is the only class defined in this file.

VirtualServerSubclient: Derived class from Subclient Base class, representing a
                            virtual server subclient, and to perform operations on that subclient

VirtualServerSubclient:
    __get_subclient_properties()          --  gets the subclient  related properties of
                                                                            VSA subclient.

    _get_subclient_properties_json()     --  gets all the subclient  related properties of
                                                                            VSA subclient.

    _get_vm_ids_and_names_dict()            --  creates and returns 2 dictionaries, along with the
                                                    vm path

    _parse_vm_path()                        --  parses the path provided by user,
                                                    and replaces the VM Display Name with the VM ID

    _json_restore_virtualServerRstOption    --  setter for Virtualserver property in restore

    _json_restore_diskLevelVMRestoreOption  -- setter for diskLevel restore property in restore

    _json_restore_advancedRestoreOptions    -- setter for advanced restore property in restore

    _json_restore_volumeRstOption           -- setter for Volume restore property in restore

    _process_vsa_browse_response()          --  processes the browse response received from server,
                                                    and replaces the vm id with the vm name

    _process_restore_request()              --  processes the Restore Request and replaces the VM
                                                    display name with their ID before passing
                                                        to the API

    _get_disk_Extension()                   --  Gets the Extension of disk provided

    _get_conversion_disk_Type()             -- For source Disk gets the Disk that can be converted
                                                    to and set its destination Vendor

    _prepare_filelevel_restore_json()       -- internal Method can be used by subclasses for
                                                    file level restore Json

    _prepare_disk_restore_json              -- internal Method can be used by subclasses for
                                                    disk level restore Json

    _check_folder_in_browse                 -- Internal Method to check folder is in
                                                    browse from subclient

    browse()                                --  gets the content of the backup for this subclient
                                                    at the vm path specified

    disk_level_browse()                     --  browses the Disks of a Virtual Machine

    guest_files_browse()                    --  browses the Files and Folders
                                                    inside a Virtual Machine


    vm_files_browse()                       --  browses the Files and Folders
                                                    of a Virtual Machine

    vm_files_browse_in_time()               --  browses the Files and Folders of a Virtual Machine
                                            in the time range specified

    restore_out_of_place()                  --  restores the VM Guest Files specified in
                                                    the paths list to the client, at the
                                                        specified destionation location

    full_vm_restore_in_place()              --  restores the VM specified by the
                                                    user to the same location

"""

import os

from ..exception import SDKException
from ..subclient import Subclient
from ..client import Client
from .. import constants
from past.builtins import basestring


class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def __new__(self, backupset_object, subclient_name, subclient_id=None):
        """Decides which instance object needs to be created"""

        hv_type = constants.HypervisorType
        if backupset_object._instance_object.instance_name == hv_type.MS_VIRTUAL_SERVER.value.lower():
            from .virtualserver.hypervsubclient import HyperVVirtualServerSubclient
            return object.__new__(HyperVVirtualServerSubclient)


    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (backupset_object,subclient_name,subclient_id)  --  instance of the
                                                                                    backupset class,
                                                                                    subclient name,
                                                                                    subclient id

        """
        self.content_types = {
            '1': 'Host',
            '2': 'Resource Pool',
            '4': 'Datacenter',
            '9': 'Virtual Machine',
            '16': 'All unprotected VMs',
            '17': 'Root'
        }
        super(VirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = [".vhd", ".avhd", ".avhdx", ".vhdx", ".vmdk"]
        self._vm_names_browse = []
        self._vm_ids_browse = {}
        self._advanced_restore_option_list = []

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        content = []
        subclient_content = self._vmContent

        if 'children' in subclient_content:
            children = subclient_content['children']

            for child in children:
                path = str(child['path']) if 'path' in child else None
                display_name = str(child['displayName'])
                content_type = self.content_types[str(child['type'])]
                vm_id = str(child['name'])

                temp_dict = {
                    'equal_value': child['equalsOrNotEquals'],
                    'allOrAnyChildren': child['allOrAnyChildren'],
                    'id': vm_id,
                    'path': path,
                    'display_name': display_name,
                    'type': content_type
                }

                content.append(temp_dict)

        return content

    @property
    def vm_filter(self):
        """Gets the appropriate filter from the Subclient relevant to the user.

            Returns:
                list - list of filter associated with the subclient
        """
        vm_filter = []

        if not self._vmFilter is None:
            subclient_filter = self._vmFilter

            if 'children' in subclient_filter:
                children = subclient_filter['children']

                for child in children:
                    path = str(child['path']) if 'path' in child else None
                    display_name = str(child['displayName'])
                    content_type = self.content_types[str(child['type'])]
                    vm_id = str(child['name'])

                    temp_dict = {
                        'id': vm_id,
                        'path': path,
                        'display_name': display_name,
                        'type': content_type,
                        'equal_value': child['allOrAnyChildren']
                    }

                    vm_filter.append(temp_dict)

        else:
            vm_filter = self._vmFilter

        return vm_filter

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            Virtual Server Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content = []

        try:
            for temp_dict in subclient_content:
                content_type = [types for types, name in self.content_types.items()
                                if name == temp_dict['type']]

                virtual_server_dict = {
                    'allOrAnyChildren': True,
                    'equalsOrNotEquals': True,
                    'name': temp_dict['id'],
                    'displayName': temp_dict['display_name'],
                    'path': temp_dict['path'],
                    'type': content_type[0]
                }

                content.append(virtual_server_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        vs_subclient_content = {
            "children": content
        }
        self._set_subclient_properties("_vmContent", vs_subclient_content)

    @vm_filter.setter
    def vm_filter(self, subclient_filter):
        """Creates the list of Filter JSON to pass to the API to add/update content of a
            Virtual Server Subclient.

            Args:
                subclient_filter (list)  --  list of the filter to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        vm_filter = []

        try:
            for temp_dict in subclient_filter:
                for type_id, type_name in self.content_types.items():
                    if type_name == temp_dict['type']:
                        content_type_id = type_id
                        break

                virtual_server_dict = {
                    'allOrAnyChildren': True,
                    'equalsOrNotEquals': temp_dict["equal_value"],
                    'name': temp_dict['id'],
                    'displayName': temp_dict['display_name'],
                    'path': temp_dict['path'],
                    'type': content_type_id
                }

                vm_filter.append(virtual_server_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102',
                               '{} not given in content'.format(err))

        vs_filter_content = {
            "children": vm_filter
        }
        self._set_subclient_content("_vmFilter", vs_filter_content)

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.

        """

        self._vmDiskFilter = None
        self._vmFilter = None

        if not bool(self._subclient_properties):
            super(VirtualServerSubclient, self)._get_subclient_properties()

        if 'vmContent' in self._subclient_properties:
            self._vmContent = self._subclient_properties['vmContent']
        if 'vmDiskFilter' in self._subclient_properties:
            self._vmDiskFilter = self._subclient_properties['vmDiskFilter']
        if 'vmFilter' in self._subclient_properties:
            self._vmFilter = self._subclient_properties['vmBackupInfo']
        if 'vmBackupInfo' in self._subclient_properties:
            self._vmBackupInfo = self._subclient_properties['vmBackupInfo']
        if 'vsaSubclientProp' in self._subclient_properties:
            self._vsaSubclientProp = self._subclient_properties['vsaSubclientProp']

    def _get_subclient_content_(self):
        """
        Returns the subclient content from property. Base class Abstract method implementation

        return:
            VM content  (dict)  -- Dictionary of VM Content with all details

        """
        return self.content

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "vmContent": self._vmContent,
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "vmDiskFilter": self._vmDiskFilter,
                    "vmBackupInfo": self._vmBackupInfo,
                    "vsaSubclientProp": self._vsaSubclientProp,
                    #"content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    def _set_default_client(self, client):
        """
        Set the default client values for VSA and create object for client

        Args:
            Client  (str)   -- client name if given

        Raise Exception:
            if the client is not part of CS

        """

        if client is None:
            client = self._backupset_object._instance_object.co_ordinator

        if isinstance(client, Client):
            client = client
        elif isinstance(client, str):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        return client

    def _json_restore_virtualServerRstOption(self, value):
        """setter for  the Virtual server restore  option in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._virtualserver_option_restore_json = {
            "isDiskBrowse": value.get("disk_browse", True),
            "isFileBrowse": value.get("file_browse", False),
            "isVolumeBrowse": False,
            "viewType": "DEFAULT",
            "isBlockLevelReplication": False
        }

    def _json_restore_diskLevelVMRestoreOption(self, value):
        """setter for  the disk Level VM Restore Option    in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._json_disklevel_option_restore = {
            "vmFolderName": value.get("vm_folder", ""),
            "dataCenterName": value.get("data_center", ""),
            "hostOrCluster": value.get("host_cluster", ""),
            "diskOption": value.get("disk_option", 0),
            "vmName": "",
            "transportMode": value.get("transport_mode", 0),
            "passUnconditionalOverride": value.get("unconditional_overwrite", False),
            "powerOnVmAfterRestore": value.get("power_on", False),
            "registerWithFailoverCluster": value.get("add_to_failover", False),
            "userPassword": {"userName": "admin"},
            "dataStore": {}
        }

    def _json_restore_advancedRestoreOptions(self, value):
        """setter for the Virtual server restore  option in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._advanced_option_restore_json = {
            "Datastore": value.get("datastore", ""),
            "DestinationPath": value.get("destination_path", ""),
            "disks": value.get("disks", []),
            "guid": value.get("guid", ""),
            "newName": value.get("new_name", ""),
            "esxHost": value.get("esx_host", ""),
            "name": value.get("name", "")
        }

    def _advanced_restore_option(self, value):
        """
        populate the advanced restore option list with the dict passed
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._advanced_restore_option_list.append(value)

    def _json_restore_volumeRstOption(self, value):
        """setter for  the Volume restore option for in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._volume_restore_json = {
            "destinationVendor": value.get("destination_vendor", 0),
            "volumeLeveRestore": False,
            "volumeLevelRestoreType": value.get("volume_level_restore", 0),
            "destinationDiskType": value.get("destination_disktype", 0)
        }

    def _get_vm_ids_and_names_dict(self):
        """Parses through the subclient content and creates 2 dictionaries.

            Returns:
                dict    -   dictionary consisting of VM ID as Key and VM Display Name as value

                dict    -   dictionary consisting of VM Display Name as Key and VM ID as value
        """
        vm_ids = {}
        vm_names = {}

        for content in self.content:
            vm_ids[content['id']] = content['display_name']
            vm_names[content['display_name']] = content['id']

        return vm_ids, vm_names

    def _get_vm_ids_and_names_dict_from_browse(self):
        """Parses through the Browse content and get the VMs Backed up

            returns :
                vm_names    (list)  -- returns list of VMs backed up
                vm_ids      (dict)  -- returns id list of VMs backed up
        """

        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict()
        if self._vm_names_browse == []:
            paths, paths_dict = self.browse()

            for _each_path in paths_dict:
                _vm_id = _each_path.split("\\")[1]
                self._vm_names_browse.append(_vm_id)
                self._vm_ids_browse[_vm_id] = _vm_ids[_vm_id]

        return self._vm_names_browse, self._vm_ids_browse

    def _parse_vm_path(self, vm_names, vm_path):
        """Parses the path provided by user, and replaces the VM Display Name with the VM ID.

            Returns:
                str     -   string of path to run browse for
        """
        if vm_path not in ['\\', '']:
            if not vm_path.startswith('\\'):
                vm_path = '\\' + vm_path

            vm_path_list = vm_path.split('\\')

            for vm_name in vm_names:
                if vm_name in vm_path_list[1]:
                    vm_path = vm_path.replace(vm_path_list[1], vm_names[vm_name])
                    break

        return vm_path

    def _process_vsa_browse_response(self, vm_ids, browse_content):
        """Processes the Browse response and replaces the VM ID with their display name before
            returning to user.

            Args:
                vm_ids          (dict)      --  dictionary with VM ID as Key and VM Name as value

                browse_content  (tuple)     --  browse response received from server

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time
        """
        for index, path in enumerate(browse_content[0]):
            if vm_ids:
                for vm_id in vm_ids:
                    if vm_id in path:
                        browse_content[0][index] = path.replace(vm_id, vm_ids[vm_id])

        temp_dict = {}

        for path in browse_content[1]:
            if vm_ids:
                for vm_id in vm_ids:
                    if vm_id in path:
                        temp_dict[path.replace(vm_id, vm_ids[vm_id])] = browse_content[1][path]

        return browse_content[0], temp_dict

    def _process_restore_request(self, vm_names, restore_content):
        """Processes the Restore Request and replaces the VM display name with their ID before
            passing to the API.

            Args:
                vm_names            (dict)      --  dictionary with VM Name as Key, VM ID as value

                restore_content     (tuple)    --  content to restore specified by user

            Returns:
                list - list of all folders or files with their full paths inside the input path
        """
        for index, path in enumerate(restore_content):
            if vm_names:
                for vm_name in vm_names:
                    if vm_name in path:
                        restore_content[index] = path.replace(vm_name, vm_names[vm_name])

        return restore_content

    def browse(self, vm_path='\\',
               show_deleted_files=True,
               vm_disk_browse=False,
               vm_files_browse=False):
        """Gets the content of the backup for this subclient at the path specified.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

                vm_disk_browse      (bool)  --  browse virtual machine files
                                                    e.g.; .vmdk files, etc.
                    only applicable when browsing content inside a guest virtual machine
                    default: False

                vm_file_browse      (bool)  --  browse files and folders
                    default: True

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        vm_ids, vm_names = self._get_vm_ids_and_names_dict()

        vm_path = self._parse_vm_path(vm_names, vm_path)

        browse_content = super(VirtualServerSubclient, self).browse(
            vm_path, show_deleted_files, vm_disk_browse, True, vs_file_browse=vm_files_browse
        )

        return self._process_vsa_browse_response(vm_ids, browse_content)

    def browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            vm_disk_browse=False,
            from_date=None,
            to_date=None,
            vm_files_browse=False):
        """Gets the content of the backup for this subclient
            at the path specified in the time range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents of
                    default: '\\'; returns the root of the Backup content

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
        vm_ids, vm_names = self._get_vm_ids_and_names_dict()

        vm_path = self._parse_vm_path(vm_names, vm_path)

        browse_content = super(VirtualServerSubclient, self).browse(
            show_deleted_files, restore_index, vm_disk_browse, from_date, to_date, True,
            path=vm_path, vm_disk_browse=vm_disk_browse, vs_file_browse=vm_files_browse)

        return self._process_vsa_browse_response(vm_ids, browse_content)

    def disk_level_browse(self, vm_path='\\',
                          show_deleted_files=True,
                          restore_index=True,
                          from_date=None,
                          to_date=None):
        """Browses the Disks of a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
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
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        browse_content = self.browse_in_time(
            vm_path, show_deleted_files, restore_index, True, from_date, to_date
        )

        paths_list = []

        for path in browse_content[0]:
            if any(path.lower().endswith(Ext) for Ext in self.diskExtension):
                paths_list.append(path)

        paths_dict = {}

        for path in browse_content[1]:
            if any(path.lower().endswith(Ext) for Ext in self.diskExtension):
                paths_dict[path] = browse_content[1][path]

        if paths_list and paths_dict:
            return paths_list, paths_dict
        else:
            raise SDKException('Subclient', '113')

    def guest_files_browse(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            from_date=None,
            to_date=None):
        """Browses the Files and Folders inside a Virtual Machine in the time range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents of
                    default: '\\'; returns the root of the Backup content

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
        return self.browse_in_time(
            vm_path, show_deleted_files, restore_index, False, from_date, to_date,
            vm_files_browse=True)

    def _check_folder_in_browse(
            self,
            _vm_id,
            _folder_to_restore,
            from_date,
            to_date):
        """
        Check if the particular folder is present in browse of the subclient in particular VM

        args:
            _vm_id      (str)      -- VM id from which folder has to be restored

            folder_path     (str)   -- folder path whioch has to be restored

        exception:
            raise exception
                if folder is not present in browse
        """

        source_item = None

        _folder_to_restore = _folder_to_restore.replace(":", "")
        _restore_folder_name = _folder_to_restore.split("\\")[-1]
        _folder_to_restore = _folder_to_restore.replace("\\" + _restore_folder_name, "")
        _source_path = "\\\\" + _vm_id + "\\" + _folder_to_restore

        _browse_files, _browse_files_dict = self.guest_files_browse(
            _source_path, from_date=from_date, to_date=to_date)

        for _path in _browse_files_dict:
            _browse_folder_name = _path.split("\\")[-1]
            if _browse_folder_name == _restore_folder_name:
                source_item = _path
                break

        if source_item is None:
            raise SDKException('SubClient', '113')

        return _source_path

    def guest_file_restore(self,
                           vm_name=None,
                           folder_to_restore=None,
                           destination_client=None,
                           destination_path=None,
                           copy_preceedence=0,
                           preserve_level=1,
                           restore_ACL=True,
                           unconditional_overwrite=False,
                           from_date=None,
                           to_date=None,
                           show_deleted_files=True):
        """perform Guest file restore of the provided path

        Args:
            vm_name             (str)   --  VM from which files needs to be restored

            folder_to_restore    (str)   --  folder path to restore

            show_deleted_files  (bool)  --  include deleted files in the content or not
                default: True


            destination_path    (str)   -- path to restore

            from_date           (str)   --  date to get the contents after
                    format: dd/MM/YYYY

                    gets contents from 01/01/1970 if not specified
                default: None

            to_date             (str)  --  date to get the contents before
                    format: dd/MM/YYYY

                    gets contents till current day if not specified
                default: None

         Raises:
                SDKException:
                    if from date value is incorrect

                    if to date value is incorrect

                    if to date is less than from date

                    if failed to browse content

                    if response is empty

                    if response is not success
        """

        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _file_restore_option = {}

        # check if inputs are correct
        if not(isinstance(destination_path, str) and
               (isinstance(vm_name, str)) and
                (isinstance(folder_to_restore, str))):
            raise SDKException('Subclient', '105')

        if not(vm_name in _vm_names):
            raise SDKException('Subclient', '111')

        # check if client name is correct
        if(destination_client is None):
            destination_client = self._backupset_object._instance_object.co_ordinator

        if isinstance(destination_client, Client):
            client = destination_client
        elif isinstance(destination_client, str):
            client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        _file_restore_option["client_name"] = client.client_name
        _file_restore_option["destination_path"] = destination_path

        # process the folder to restore for browse
        if isinstance(folder_to_restore, list):
            _folder_to_restore_list = folder_to_restore

        else:
            _folder_to_restore_list = []
            _folder_to_restore_list.append(folder_to_restore)

        _file_restore_option["source_item"] = []
        for _each_folder in _folder_to_restore_list:
            _file_restore_option["source_item"].append(
                self._check_folder_in_browse(_vm_ids[vm_name], "%s" %
                                             _each_folder, from_date, to_date))

        # set the browse options
        _file_restore_option["disk_browse"] = False
        _file_restore_option["file_browse"] = True

        # set the common file level restore options
        _file_restore_option["striplevel_type"] = "PRESERVE_LEVEL"
        _file_restore_option["preserve_level"] = preserve_level
        _file_restore_option["unconditional_overwrite"] = unconditional_overwrite
        _file_restore_option["restore_ACL"] = restore_ACL

        # set the browse option
        _file_restore_option["copy_precedence_applicable"] = True
        _file_restore_option["copy_precedence"] = copy_preceedence

        # prepare and execute the Json
        request_json = self._prepare_filelevel_restore_json(_file_restore_option)

        return self._process_restore_response(request_json)

    def vm_files_browse(self, vm_path='\\', show_deleted_files=True):
        """Browses the Files and Folders of a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the content or not
                    default: True

            Returns:
                list - list of all folders or files with their full paths inside the input path

                dict - path along with the details like name, file/folder, size, modification time

            Raises:
                SDKException:
                    if failed to browse content

                    if response is empty

                    if response is not success
        """
        return self.browse(vm_path, show_deleted_files, True)

    def vm_files_browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            from_date=None,
            to_date=None):
        """Browses the Files and Folders of a Virtual Machine in the time range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents of
                    default: '\\'; returns the root of the Backup content

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
        return self.browse_in_time(
            vm_path, show_deleted_files, restore_index, True, from_date, to_date
        )

    def _get_disk_Extension(self, disk_list):
        """
        get the Extension of all disk in the list

        Args:
            disk_list   (LIST)  -- get the disk List

        return:
            extn_list   (LIST)  --  returns the Extension List of the disk list
        """

        _extn_list = []
        for each_disk in disk_list:
            _disk_name, _extn_name = os.path.splitext(each_disk)
            _extn_list.append(_extn_name)

        _extn_list = list(set(_extn_list))

        if(len(_extn_list) > 1):
            return _extn_list
        else:
            return _extn_list[0]

    def _get_conversion_disk_Type(self, _src_disk_extn, _dest_disk_extn):
        """
        return volume restore type and destiantion disk Type

        Args:
            src_disk_extn   (str)   --  source disk extension of the disk
            dest_disk_extn  (str)   --  Extension to which disk is converted

        return
            _vol_restore_type   (str)   -- value of Volume restore type parameter of the XML
            _dest_disk_type     (str)   -- value of destination Disk Type parameter of the XML
        """

        disk_conversion = {
            "vhdx": {"vhd": ("VIRTUAL_HARD_DISKS", "VHD_DYNAMIC"),
                     "vmdk": ("VMDK_FILES", "VMDK_VCB4")
                     },
            "vmdk": {"vhd": ("VIRTUAL_HARD_DISKS", "VHD_DYNAMIC"),
                     "vhdx": ("VIRTUAL_HARD_DISKS", "VHDX_DYNAMIC")
                     }
        }
        _src_disk_extn = _src_disk_extn.lower().strip(".")
        _dest_disk_extn = _dest_disk_extn.lower().strip(".")

        return disk_conversion[_src_disk_extn][_dest_disk_extn]

    def _set_vm_to_restore(self, vm_to_restore=None, restore_option={}):
        """
        check whether the VMs provided for restore is backued up else assume
                            Vm_to_restore with default

        Args:
            vm_to_restore   (list)      -- list of Vm to restore

            restore_option  (dict)      -- dict with all restore options

        return:
            vm_to_restore   (list)      -- Final list of Vm need to be restored

        """

        if not self._vm_names_browse:
            self._get_vm_ids_and_names_dict_from_browse()

        # set vms to restore
        _temp_res_list = []
        if vm_to_restore is None:
            vm_to_restore = restore_option.get("vm_to_restore", self._vm_ids_browse.keys())
            _temp_res_list = vm_to_restore

        else:
            _temp_res_list.append(vm_to_restore)

        vm_to_restore = list(set(self._vm_names_browse) & set(_temp_res_list))

        if not vm_to_restore:
            raise SDKException('Subclient', 104)

        return vm_to_restore

    def _set_advanced_attributes(self, restore_option, **kwargs):
        """
        set all the advanced properties of the subclient restore

        Args:
            restore_option  (dict)  -- restore option dictionary where advanced
                                            properties to be appended

            **kwargs                --  Keyword arguments with key as property name
                                            and its value
        """
        restore_option.update(kwargs)
        restore_option["destination_vendor"] = \
            self._backupset_object._instance_object._vendor_id

    def _set_vm_attributes(self, restore_option, **kwargs):
        """
        set all the advanced properties of the subclient restore for VM

        Args:
            restore_option  (dict)  -- restore option dictionary where advanced
                                            properties to be appended

            **kwargs                --  Keyword arguments with key as property name
                                            and its value
        """
        restore_option.update(kwargs)

    def _prepare_filelevel_restore_json(self, _file_restore_option):
        """
        prepares the  file level restore json from getters
        """

        self._restore_destination_json(_file_restore_option)
        self._restore_fileoption_json(_file_restore_option)
        self._json_restore_virtualServerRstOption(_file_restore_option)
        self._restore_commonOptions_json(_file_restore_option)
        self._restore_browse_option_json(_file_restore_option)
        self._impersonation_json(_file_restore_option)
        self._json_restore_virtualServerRstOption(_file_restore_option)
        self._json_restore_volumeRstOption(_file_restore_option)

        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTask": self._json_restore_subtask,
                        "options": {
                            "restoreOptions": {
                                "impersonation": self._impersonation_json_,
                                "virtualServerRstOption": self._virtualserver_option_restore_json,
                                "volumeRstOption": self._volume_restore_json,
                                "browseOption": self._browse_restore_json,
                                "commonOptions": self._commonoption_restore_json,
                                "destination": self._destination_restore_json,
                                "fileOption": self._fileoption_restore_json,
                                "sharePointRstOption": self._restore_sharepoint_json()
                            }
                        }
                    }]
            }
        }
        return request_json

    def _prepare_disk_restore_json(self, _disk_restore_option=None):
        """
        Prepare disk retsore Json with all getters

        Args:
            _disk_restore_option - dictionary with all disk restore options

            value:
                preserve_level              -  set the preserve level in restore
                unconditional_overwrite     - unconditionally overwrite the disk
                                                    in the restore path

                destination_path            - path where the disk needs to be restored
                client_name                 - client where the disk needs to be restored

                destination_vendor          - vendor id of the Hypervisor
                destination_disktype        - type of disk needs to be restored like VHDX,VHD,VMDK
                source_item                 - GUID of VM from which disk needs to be restored
                                                eg:\\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

                copy_precedence_applicable  - True if needs copy_preceedence to be honored else False
                copy_preceedence            - the copy id from which browse and 
                                                                restore needs to be performed

        returns:
            request_json        -complete json for performing disk Restore options

        """

        if _disk_restore_option is None:
            _disk_restore_option = {}

        # set the  setters for Json
        self._restore_commonOptions_json(_disk_restore_option)
        self._restore_destination_json(_disk_restore_option)
        self._json_restore_volumeRstOption(_disk_restore_option)
        self._restore_fileoption_json(_disk_restore_option)
        self._impersonation_json(_disk_restore_option)
        self._restore_browse_option_json(_disk_restore_option)
        self._json_restore_virtualServerRstOption(_disk_restore_option)
        self._json_restore_diskLevelVMRestoreOption(_disk_restore_option)

        _virt_restore_json = self._virtualserver_option_restore_json
        _virt_restore_json["diskLevelVMRestoreOption"] = self._json_disklevel_option_restore

        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTask": self._json_restore_subtask,
                        "options": {
                            "restoreOptions": {
                                "impersonation": self._impersonation_json_,
                                "virtualServerRstOption": self._virtualserver_option_restore_json,
                                "volumeRstOption": self._volume_restore_json,
                                "browseOption": self._browse_restore_json,
                                "commonOptions": self._commonoption_restore_json,
                                "destination": self._destination_restore_json,
                                "fileOption": self._fileoption_restore_json,
                                "sharePointRstOption": self._restore_sharepoint_json()
                            }
                        }
                    }]
            }
        }
        return request_json

    def _prepare_fullvm_restore_json(self, restore_option=None):
        """
        Prepare Full VM restore Json with all getters

        Args:
        restore_option - dictionary with all VM restore options

        value:
            preserve_level              -  set the preserve level in restore
            unconditional_overwrite     - unconditionally overwrite the disk
                                                in the restore path

            destination_path            - path where the disk needs to be restored
            client_name                 - client where the disk needs to be restored

            destination_vendor          - vendor id of the Hypervisor
            destination_disktype        - type of disk needs to be restored like VHDX,VHD,VMDK
            source_item                 - GUID of VM from which disk needs to be restored
                                            eg:\\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

            copy_precedence_applicable  - True if needs copy_preceedence to be honoured else False
            copy_preceedence            - the copy id from which browse and 
                                                            restore needs to be performed

            power_on                    - power on the VM after restore
            add_to_failover             - Register the VM to Failover Cluster
            datastore                   - Datastore where the VM needs to be restored

            disks   (list of dict)      - list with dict for each disk in VM
                                            eg: [{
                                                    name:"disk1.vmdk"
                                                    datastore:"local"
                                                }
                                                {
                                                    name:"disk2.vmdk"
                                                    datastore:"local1"
                                                }
                                            ]
            guid                        - GUID of the VM needs to be restored
            new_name                    - New name for the VM to be restored
            esx_host                    - esx_host or client name where it need to be restored
            name                        - name of the VM to be restored

        returns:
            request_json        -complete json for perfomring Full VM Restore options

        """

        if restore_option is None:
            restore_option = {}

        # set the setters
        self._restore_commonOptions_json(restore_option)
        self._impersonation_json(restore_option)
        self._json_restore_volumeRstOption(restore_option)
        self._restore_commonOptions_json(restore_option)
        self._restore_browse_option_json(restore_option)
        self._restore_destination_json(restore_option)
        self._json_restore_diskLevelVMRestoreOption(restore_option)
        self._json_restore_virtualServerRstOption(restore_option)
        self._restore_fileoption_json(restore_option)

        _virt_restore_json = self._virtualserver_option_restore_json
        _virt_restore_json["diskLevelVMRestoreOption"] = self._json_disklevel_option_restore
        _virt_restore_json["diskLevelVMRestoreOption"][
                                "advancedRestoreOptions"] = self._advanced_restore_option_list

        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [
                    {
                        "subTask": self._json_restore_subtask,
                        "options": {
                            "restoreOptions": {
                                "impersonation": self._impersonation_json_,
                                "virtualServerRstOption": self._virtualserver_option_restore_json,
                                "volumeRstOption": self._volume_restore_json,
                                "browseOption": self._browse_restore_json,
                                "commonOptions": self._commonoption_restore_json,
                                "destination": self._destination_restore_json,
                                "fileOption": self._fileoption_restore_json,
                                "sharePointRstOption": self._restore_sharepoint_json()
                            }
                        }
                    }]
            }
        }
        return request_json
