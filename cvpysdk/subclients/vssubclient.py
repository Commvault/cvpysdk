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
    _get_subclient_content_()               --  gets the content of a virtual server subclient

    _set_subclient_content_()               --  sets the content of a virtual server subclient

    _get_vm_ids_and_names_dict()            --  creates and returns 2 dictionaries, along with the 
                                                    vm path

    _parse_vm_path()                        --  parses the path provided by user,
                                                    and replaces the VM Display Name with the VM ID
    
    _restore_virtualServerRstOption_json    --  setter for Virtualserver property in restore
    
    _restore_diskLevelVMRestoreOption_json  -- setter for diskLevel restore property in restore
    
    _restore_advancedRestoreOptions_json    -- setter for advanced restore property in restore
    
    _restore_volumeRstOption_json           -- setter for Volume restore property in restore

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


class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def __new__(self, backupset_object, subclient_name, subclient_id=None):
        """Decides which instance object needs to be created"""

        hv_type = constants.HyperVisorType
        if(backupset_object._instance_object.instance_name == hv_type.MS_VIRTUAL_SERVER):
            from virtualserver.hypervsubclient import HyperVVirtualServerSubclient
            return object.__new__(HyperVVirtualServerSubclient)

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (backupset_object,subclient_name,subclient_id)  --  instance of the 
                                                                                    backupset class, 
                                                                                    subclient name,
                                                                                    subclient id

        """

        super(VirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = [".vhd", ".avhd", ".avhdx", ".vhdx", ".vmdk"]
        self._vm_names_browse = []
        self._vm_ids_browse = {}

    def _restore_virtualServerRstOption_json(self, Value):
        """setter for  the Virtual server restore  option in restore json"""

        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._virtualserver_option_restore_json = {
            "isDiskBrowse": Value.get("disk_browse", True),
            "isFileBrowse": Value.get("file_browse", False),
            "isVolumeBrowse": False,
            "viewType": "DEFAULT",
            "isBlockLevelReplication": False
        }

    def _restore_diskLevelVMRestoreOption_json(self, Value):
        """setter for  the disk Level VM Restore Option    in restore json"""

        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._disklevel_option_restore_json = {
            "vmFolderName": Value.get("vm_folder", ""),
            "dataCenterName": Value.get("data_center", ""),
            "hostOrCluster": Value.get("host_cluster", ""),
            "diskOption": Value.get("disk_option", 0),
            "vmName": "",
            "transportMode": Value.get("transport_mode", 0),
            "passUnconditionalOverride": Value.get("unconditional_overwrite", False),
            "powerOnVmAfterRestore": Value.get("power_on", False),
            "registerWithFailoverCluster": Value.get("add_to_failover", False),
            "userPassword": {"userName": "admin"},
            "dataStore": {}
        }

    def _restore_advancedRestoreOptions_json(self, Value):
        """setter for the Virtual server restore  option in restore json"""

        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._advanced_option_restore_json = {
            "Datastore": Value.get("datastore", ""),
            "DestinationPath": Value.get("destination_path", ""),
            "disks": Value.get("disks", []),
            "guid": Value.get("guid", ""),
            "newName": Value.get("new_name", ""),
            "esxHost": Value.get("esxhost", ""),
            "name": Value.get("name", "")
        }

    def _restore_volumeRstOption_json(self, Value):
        """setter for  the Volume restore option for in restore json"""

        if not isinstance(Value, dict):
            raise SDKException('Subclient', '101')

        self._volume_restore_json = {
            "destinationVendor": Value.get("destination_vendor", 0),
            "volumeLeveRestore": False,
            "volumeLevelRestoreType": 0,
            "destinationDiskType": Value.get("destination_disktype", 0)
        }

    def _get_subclient_content_(self):
        """Gets the appropriate content from the Subclient relevant to the user.

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
            subclient_content = self._subclient_properties['vmContent']

            if 'children' in subclient_content:
                children = subclient_content['children']

                for child in children:
                    path = str(child['path']) if 'path' in child else None
                    display_name = str(child['displayName'])
                    content_type = content_types[str(child['type'])]
                    vm_id = str(child['name'])

                    temp_dict = {
                        'id': vm_id,
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
                    'name': temp_dict['id'],
                    'displayName': temp_dict['display_name'],
                    'path': temp_dict['path'],
                    'type': content_types[temp_dict['type']]
                }

                content.append(virtual_server_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        vs_subclient_content = {
            "children": content
        }

        return vs_subclient_content

    def _get_vm_ids_and_names_dict(self):
        """Parses through the subclient content and creates 2 dictionaries.

            Returns:
                dict    -   dictionary consisting of VM ID as Key and VM Display Name as Value

                dict    -   dictionary consisting of VM Display Name as Key and VM ID as Value
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
        if(self._vm_names_browse == []):
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
                vm_ids          (dict)      --  dictionary with VM ID as Key and VM Name as Value

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
                vm_names            (dict)      --  dictionary with VM Name as Key, VM ID as Value

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

    def browse(self, vm_path='\\', show_deleted_files=True, vm_disk_browse=False):
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
            vm_path, show_deleted_files, vm_disk_browse, True
        )

        return self._process_vsa_browse_response(vm_ids, browse_content)

    def browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=True,
            restore_index=True,
            vm_disk_browse=False,
            from_date=None,
            to_date=None):
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
            vm_path, show_deleted_files, restore_index, vm_disk_browse, from_date, to_date, True
        )

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
            if(any(path.lower().endswith(Ext) for Ext in self.diskExtension)):
                paths_list.append(path)

        paths_dict = {}

        for path in browse_content[1]:
            if(any(path.lower().endswith(Ext) for Ext in self.diskExtension)):
                paths_dict[path] = browse_content[1][path]

        if paths_list and paths_dict:
            return paths_list, paths_dict
        else:
            raise SDKException('Subclient', '111')

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
            vm_path, show_deleted_files, restore_index, False, from_date, to_date
        )

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
            if(_browse_folder_name == _restore_folder_name):
                source_item = _path
                break

        if (source_item is None):
            raise SDKException('SubClient', '111')

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
        if (not(isinstance(destination_path, str)) and
            (isinstance(vm_name, str)) and
                (isinstance(folder_to_restore, str))):
            raise SDKException('Subclient', '105')

        if(not(vm_name in _vm_names)):
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
        self._restore_destination_json(_file_restore_option)

        # preocess the folder to restore for browse
        if (isinstance(folder_to_restore, list)):
            _folder_to_restore_list = folder_to_restore

        else:
            _folder_to_restore_list = []
            _folder_to_restore_list.append(folder_to_restore)

        _file_restore_option["source_item"] = []
        for _each_folder in _folder_to_restore_list:
            _file_restore_option["source_item"].append(
                self._check_folder_in_browse(_vm_ids[vm_name], "%s" % _each_folder, from_date, to_date))

        self._restore_fileoption_json(_file_restore_option)

        # set the browse options
        _file_restore_option["disk_browse"] = False
        _file_restore_option["file_browse"] = True
        self._restore_virtualServerRstOption_json(_file_restore_option)

        # set the common file level restore options
        _file_restore_option["striplevel_type"] = "PRESERVE_LEVEL"
        _file_restore_option["preserve_level"] = preserve_level
        _file_restore_option["unconditional_overwrite"] = unconditional_overwrite
        _file_restore_option["restore_ACL"] = restore_ACL
        self._restore_commonOptions_json(_file_restore_option)

        # set the browse option
        _file_restore_option["copy_precedence_applicable"] = True
        _file_restore_option["copy_precedence"] = copy_preceedence
        self._restore_browse_option_json(_file_restore_option)

        # set the rest setters
        self._impersonation_json(_file_restore_option)
        self._restore_virtualServerRstOption_json(_file_restore_option)
        self._restore_volumeRstOption_json(_file_restore_option)

        # prepare and execute the Json
        request_json = self._prepare_filelevel_restore_json()

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
            _vol_restore_type   (str)   -- Value of Volume restore type parameter of the XML
            _dest_disk_type     (str)   -- Value of destiantion Disk Type parameter of the XML
        """

        if _src_disk_extn.lower() == ".vhdx":
            if(_dest_disk_extn.lower() == "vhd"):
                _vol_restore_type = "VIRTUAL_HARD_DISKS"
                _dest_disk_type = "VHD_DYNAMIC"

            elif(_dest_disk_extn.lower() == "vmdk"):
                _vol_restore_type = "VMDK_FILES"
                _dest_disk_type = "VMDK_VCB4"

            else:
                raise SDKException('Subclient', '101')

        elif (_src_disk_extn.lower() == ".vmdk"):
            if(_dest_disk_extn.lower() == "vhd"):
                _vol_restore_type = "VIRTUAL_HARD_DISKS"
                _dest_disk_type = "VHD_DYNAMIC"

            elif(_dest_disk_extn.lower() == "vhdx"):
                _vol_restore_type = "VIRTUAL_HARD_DISKS"
                _dest_disk_type = "VHDX_DYNAMIC"

            else:
                raise SDKException('Subclient', '101')

        else:
            raise SDKException('Subclient', '101')

        return _vol_restore_type, _dest_disk_type

    def _prepare_filelevel_restore_json(self):
        """
        prepares the  file level restore json from getters 
        """

        request_json = {
            "taskInfo": {
                "associations": [self._association_json()],
                "task": self._task_json(),
                "subTasks": [
                    {
                        "subTask": self._restore_subtask_json(),
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

    def _prepare_disk_restore_json(self):
        """
        Prepare disk retsore Json with all getters
        """

        _virt_restore_json = self._virtualserver_option_restore_json
        _virt_restore_json["diskLevelVMRestoreOption"] = self._disklevel_option_restore_json

        request_json = {
            "taskInfo": {
                "associations": [self._association_json()],
                "task": self._task_json(),
                "subTasks": [
                    {
                        "subTask": self._restore_subtask_json(),
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

    def _restore_out_of_place(
            self,
            restore_option_dict=False):
        """Restores the VM Guest files/folders specified in the input paths list to the client,
            at the specified destionation location.

            Args:
                restore_option_dict    (dict)     --  complete dictionary with all advanced optio
                    default: False

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        # populate basic information of browse
        browse_result = self.vm_files_browse()

        # create client Object if needed
        if(isinstance(restore_option_dict['esxServerName'], None)):
            restore_option_dict['esxServerName'] = self._backupset_object._agent_object._client_object.client_name

        if isinstance(restore_option_dict['esxServerName'], Client):
            client = restore_option_dict['esxServerName']
        elif isinstance(restore_option_dict['esxServerName'], str):
            client = Client(self._commcell_object, client)
        else:
            raise SDKException('Subclient', '105')

        # populate the Esx Host default if None
        for vm_to_restore in restore_option_dict['VMstoRestore']:
            if(isinstance(restore_option_dict[vm_to_restore]['esxHost'], None)):
                vs_metadata = browse_result[1]['\\' + vm_to_restore][-1]
                restore_option_dict[vm_to_restore]['esxHost'] = vs_metadata['esxHost']

            if(isinstance(restore_option_dict[vm_to_restore]['newName'], None)):
                restore_option_dict[vm_to_restore]['newName'] = "Delete" + vm_to_restore

        #request_json = self._prepare_fullvm_restore_json(restore_option_dict)

        #return self._process_restore_response(request_json)
