# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Subclient.

VirualServerSubclient is the only class defined in this file.

VirtualServerSubclient: Derived class from Subclient Base class, representing a
                            virtual server subclient, and to perform operations
                            on that subclient

VirtualServerSubclient:
    __get_subclient_properties()      --  gets the subclient  related
                                          properties of VSA subclient.

    _get_subclient_properties_json()  --  gets all the subclient  related
                                          properties of VSA subclient.

    _get_vm_ids_and_names_dict()      --  creates and returns 2 dictionaries,
                                          along with the vm path

    _parse_vm_path()                  --  parses the path provided by user,
                                          and replaces the VM Display Name with
                                          the VM ID

    _json_restore_virtualServerRstOption    -- setter for Virtualserver
                                               property in restore

    _json_restore_diskLevelVMRestoreOption  -- setter for diskLevel restore
                                               property in restore

    _json_restore_advancedRestoreOptions    -- setter for advanced restore
                                               property in restore

    _json_restore_volumeRstOption           -- setter for Volume restore
                                               property in restore

    _json_vcenter_instance                  -- setter for vcenter instance
                                               json in restore

    _json_nics_advancedRestoreOptions       -- Setter for nics list for
                                               advanced restore option json

    _process_vsa_browse_response()          -- processes the browse response
                                               received from server,and
                                               replaces the vm id with the vm
                                               name

    _process_restore_request()              -- processes the Restore Request
                                               and replaces the VM
                                               display name with their ID
                                               before passing to the API

    _get_disk_Extension()                   -- Gets the Extension of disk
                                               provided

    _get_conversion_disk_Type()             -- For source Disk gets the Disk
                                               that can be converted to and
                                               set its destination Vendor

    _prepare_filelevel_restore_json()       -- internal Method can be used by
                                               subclasses for file level
                                               restore Json

    _prepare_disk_restore_json              -- internal Method can be used by
                                               subclasses for disk level
                                               restore Json

    _check_folder_in_browse                 -- Internal Method to check folder
                                               is in browse from subclient

    browse()                                -- gets the content of the backup
                                               for this subclient at the vm
                                               path specified

    parse_nics_xml()                        -- gets the list of nics for a VM

    get_nics_from_browse()                  -- Browses the vm to get the nics
                                               info xml, gets the nics info
                                               using the parse_nics_xml method
                                               and prepares the dict for nics
                                               json

    disk_level_browse()                     -- browses the Disks of a Virtual
                                               Machine

    guest_files_browse()                    -- browses the Files and Folders
                                               inside a Virtual Machine


    vm_files_browse()                       -- browses the Files and Folders
                                               of a Virtual Machine

    vm_files_browse_in_time()               -- browses the Files and Folders
                                               of a Virtual Machine in the time
                                               range specified

    restore_out_of_place()                  -- restores the VM Guest Files
                                               specified in the paths list to
                                               the client, at the
                                               specified destionation location

    full_vm_restore_in_place()              -- restores the VM specified by the
                                               user to the same location

"""

import os
from enum import Enum
import copy
import xml.etree.ElementTree as ET

from past.builtins import basestring

from ..exception import SDKException
from ..subclient import Subclient
from ..client import Client
from .. import constants
from ..constants import VSAObjects



class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def __new__(cls, backupset_object, subclient_name, subclient_id=None):
        """Decides which instance object needs to be created"""
        hv_type = constants.HypervisorType
        instance_name = backupset_object._instance_object.instance_name

        if instance_name == hv_type.MS_VIRTUAL_SERVER.value.lower():
            from .virtualserver.hypervsubclient import HyperVVirtualServerSubclient
            return object.__new__(HyperVVirtualServerSubclient)

        elif instance_name == hv_type.VIRTUAL_CENTER.value.lower():
            from .virtualserver.vmwaresubclient import VMWareVirtualServerSubclient
            return object.__new__(VMWareVirtualServerSubclient)

        elif instance_name == hv_type.FUSION_COMPUTE.value.lower():
            from .virtualserver.fusioncomputesubclient import FusionComputeVirtualServerSubclient
            return object.__new__(FusionComputeVirtualServerSubclient)

        else:
            raise SDKException(
                'Subclient',
                '102',
                'Subclient for Instance: "{0}" is not yet supported'.format(instance_name)
            )

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                backupset_object    (object)    --  instance of the backupset class

                subclient_name      (str)       --  subclient name

                subclient_id        (int)       --  subclient id

        """
        super(VirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id
        )

        self.content_types = {
            '1': 'Host',
            '2': 'Resource Pool',
            '4': 'Datacenter',
            '9': 'Virtual Machine',
            '16': 'All unprotected VMs',
            '17': 'Root'
        }

        self.filter_types = {
            '1': 'Datastore',
            '2': 'Virtual Disk Name/Pattern',
            '3': 'Virtual Device Node'
        }
        self.diskExtension = [".vhd", ".avhd", ".avhdx", ".vhdx", ".vmdk"]
        self._vm_names_browse = []
        self._vm_ids_browse = {}
        self._advanced_restore_option_list = []

    class disk_pattern(Enum):
        """
        stores the disk pattern of all hypervisors
        """
        name = "name"
        datastore = "Datastore"

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
                path = child['path'] if 'path' in child else None
                display_name = child['displayName']
                content_type = self.content_types[str(child['type'])]
                vm_id = child['name']

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

        if not self._vmFilter:
            subclient_filter = self._vmFilter

            if 'children' in subclient_filter:
                children = subclient_filter['children']

                for child in children:
                    path = child['path'] if 'path' in child else None
                    display_name = child['displayName']
                    content_type = self.content_types[str(child['type'])]
                    vm_id = child['name']

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

    @property
    def vm_diskfilter(self):
        """Gets the appropriate Diskfilter from the Subclient relevant to the user.

            Returns:
                list - list of Diskfilter associated with the subclient

        """
        vm_diskfilter = []
        if self._vmDiskFilter is not None:
            subclient_diskfilter = self._vmDiskFilter

            if 'filters' in subclient_diskfilter:
                filters = subclient_diskfilter['filters']

                for child in filters:
                    filter_type = self.filter_types[str(child['filterType'])]
                    vm_id = child['vmGuid'] if 'vmGuid' in child else None
                    filter_name = child['filter']

                    temp_dict = {
                        'filter': filter_name,
                        'filterType': filter_type,
                        'vmGuid': vm_id
                    }

                    vm_diskfilter.append(temp_dict)

        else:
            vm_diskfilter = self._vmDiskFilter

        return vm_diskfilter

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update
           content of a Virtual Server Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the
                subclient list should contain name and type
                (like VSAObjects.VMName, VSAObjects.DATASTORE )
                example:[
                            {
                            'type' : VSAObjects.VMNotes,
                            'display_name' : 'removed',
                            }
                        ]

                for Advance user:
                        where we need to have multiple constraints for a single
                        rule.
                        list should contain minimum 2 parameters (name, type,
                        true/False for equalsOrNotEquals) for a single
                        constraint
                        for power on/off, we need to specify one more
                        parameter i.e., true -on, false -off(as state variable)
                        example:
                        subclient_content = [
                            [
                                {
                                'type' : VSAObjects.VMName,
                                'display_name' : 'VM*'
                                }
                            ],
                            [
                                {
                                  'type' : VSAObjects.VMNotes,
                                  'display_name' : 'removed',
                                },
                                {
                                  'type' : VSAObjects.VMPowerState,
                                  'state': 'false',
                                }
                            ]
                        ]



            Returns:
                list - list of the appropriate JSON for an agent to send to the
                       POST Subclient API
        """
        content = []
        try:
            for item in subclient_content:
                virtual_server_dict = {}
                virtual_server_dict['allOrAnyChildren'] = True
                child = []
                for content_dict in item:
                    temp = {
                        'allOrAnyChildren': content_dict.get('allOrAnyChildren', True),
                        'equalsOrNotEquals': content_dict.get('equalsOrNotEquals', True),
                        'name': '',
                        'displayName': content_dict['display_name'],
                        'path': '',
                        'type': content_dict['type'].value
                    }
                    if content_dict['type'] == VSAObjects.VMNotes:
                        temp['value'] = content_dict['display_name']
                        temp['displayName'] = content_dict['display_name']
                        temp['name'] = "Notes"
                    if (content_dict['type'] ==
                            VSAObjects.VMPowerState and
                            content_dict['state'] == 'true'):
                        temp['name'] = "PoweredState"
                        temp['value'] = 1
                        temp['displayName'] = "Powered On"
                    if (content_dict['type'] ==
                            VSAObjects.VMPowerState and
                            content_dict['state'] == 'false'):
                        temp['name'] = "PoweredState"
                        temp['value'] = 0
                        temp['displayName'] = "Powered Off"
                    child.append(temp)
                if len(item) > 1:
                    virtual_server_dict['path'] = ''
                    virtual_server_dict['children'] = child
                else:
                    virtual_server_dict.update(temp)
                content.append(virtual_server_dict)
        except KeyError as err:
            raise SDKException('Subclient', '102', '{} not given in content'.format(err))

        vs_subclient_content = {
            "children": content
        }

        self._set_subclient_properties("_vmContent", vs_subclient_content)

    @vm_filter.setter
    def vm_filter(self, subclient_filter):
        """Creates the list of Filter JSON to pass to the API to update the
           VM_filter of a Virtual Server Subclient. i.e. it works in overwrite
           mode

            Args:
                subclient_filter (list)  --  list of the filter to add to the
                                             subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the
                       POST Subclient API
        """
        vm_filter = []

        try:
            for temp_dict in subclient_filter:
                content_type_id = ""
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
        self._set_subclient_properties("_vmFilter", vs_filter_content)

    @vm_diskfilter.setter
    def vm_diskfilter(self, subclient_diskfilter):
        """Creates the list of Disk Filter JSON to pass to the API to update
           the Disk_filter of a Virtual Server Subclient. i.e. it works in
           overwrite mode

            Args:
                subclient_diskfilter (list)  --  list of the Disk filter to add
                                                 to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to
                       the POST Subclient API
        """
        vm_diskfilter = []

        try:
            for temp_dict in subclient_diskfilter:
                for type_id, type_name in self.filter_types.items():
                    if type_name == temp_dict['type']:
                        filter_type_id = type_id
                        break

                virtual_server_dict = {
                    'filter': temp_dict['filter'],
                    'filterType': filter_type_id,
                    'vmGuid': temp_dict['vmGuid']
                }

                vm_diskfilter.append(virtual_server_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102',
                               '{} not given in content'.format(err))

        vs_diskfilter_content = {
            "filters": vm_diskfilter
        }
        self._set_subclient_properties("_vmDiskFilter", vs_diskfilter_content)

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
            self._vmFilter = self._subclient_properties['vmFilter']
        if 'vmBackupInfo' in self._subclient_properties:
            self._vmBackupInfo = self._subclient_properties['vmBackupInfo']
        if 'vsaSubclientProp' in self._subclient_properties:
            self._vsaSubclientProp = self._subclient_properties['vsaSubclientProp']

    def _get_subclient_content_(self):
        """
        Returns the subclient content from property. Base class Abstract method
        implementation

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
                    "vmFilter": self._vmFilter,
                    "vmBackupInfo": self._vmBackupInfo,
                    "vsaSubclientProp": self._vsaSubclientProp,
                    # "content": self._content,
                    "commonProperties": self._commonProperties,
                    "vmContentOperationType": 1,
                    "vmDiskFilterOperationType": 1,
                    "vmFilterOperationType": 1
                }
        }
        return subclient_json

    def _disk_dict_pattern(self, name, datastore):
        """
        set the disk dictionary of the hyperviosr
        :param name:  name of the disk
        :param datastore: destiantion path of the disk needs to be restored
        :return:  disk dictionary
        """

        temp_disk_dict = {}
        temp_disk_dict[self.disk_pattern.name.value] = name
        temp_disk_dict[self.disk_pattern.datastore.value] = datastore
        return temp_disk_dict

    def _json_vcenter_instance(self, value):
        """ Setter for vcenter_instance JSON """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')


        self._vcenter_instance_json = {
            "clientName": value.get("destination_client_name", ""),
            "instanceName": value.get("destination_instance", ""),
            "appName": value.get("appName", "Virtual Server")
        }

    def _json_restore_virtualServerRstOption(self, value):
        """
            setter for  the Virtual server restore  option in restore json
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._virtualserver_option_restore_json = {
            "isDiskBrowse": value.get("disk_browse", True),
            "isFileBrowse": value.get("file_browse", False),
            "isVolumeBrowse": False,
            "isVirtualLab": value.get("virtual_lab", False),
            "esxServer": value.get("esx_server", ""),
            "isAttachToNewVM": value.get("attach_to_new_vm", False),
            "viewType": "DEFAULT",
            "isBlockLevelReplication": False
        }

    def _json_nics_advancedRestoreOptions(self, vm_to_restore):
        """
            Setter for nics list for advanced restore option json
        """
        nics_dict_from_browse = self.get_nics_from_browse()

        nics_list = []

        vm_nics_list = nics_dict_from_browse[vm_to_restore]

        for network_card_dict in vm_nics_list:
            nics = {
                "subnetId": "",
                "sourceNetwork": network_card_dict['name'],
                "sourceNetworkId": "",
                "networkName": "",
                "destinationNetwork": network_card_dict['name']
            }

            nics_list.append(nics)

        return nics_list

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
            "disks": value.get("disks", []),
            "guid": value.get("guid", ""),
            "newName": value.get("new_name", ""),
            "esxHost": value.get("esx_host", ""),
            "name": value.get("name", ""),
            "nics":value.get("nics", "")
        }

        if self.disk_pattern.datastore.value == "DestinationPath":
            self._advanced_option_restore_json["DestinationPath"] = value.get("datastore", "")

        else:
            self._advanced_option_restore_json["Datastore"] = value.get("datastore", "")

        temp_dict = copy.deepcopy(self._advanced_option_restore_json)
        return temp_dict


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
                dict    -   dictionary consisting of VM ID as Key and VM
                            Display Name as value

                dict    -   dictionary consisting of VM Display Name as Key and
                            VM ID as value
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
        if not self._vm_names_browse:
            paths, paths_dict = self.browse()

            for _each_path in paths_dict:
                _vm_id = _each_path.split("\\")[1]
                self._vm_names_browse.append(_vm_id)
                self._vm_ids_browse[_vm_id] = _vm_ids[_vm_id]

        return self._vm_names_browse, self._vm_ids_browse

    def _parse_vm_path(self, vm_names, vm_path):
        """Parses the path provided by user, and replaces the VM Display Name
           with the VM ID.

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
        """Processes the Browse response and replaces the VM ID with their
        display name before returning to user.

            Args:
                vm_ids          (dict)      --  dictionary with VM ID as Key
                                                and VM Name as value

                browse_content  (tuple)     --  browse response received from
                                                server

            Returns:
                list - list of all folders or files with their full
                       paths inside the input path

                dict - path along with the details like name, file/folder,
                       size, modification time
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
        """Processes the Restore Request and replaces the VM display name with
           their ID before passing to the API.

            Args:
                vm_names            (dict)      --  dictionary with VM Name as
                                                    Key, VM ID as value

                restore_content     (tuple)    --  content to restore specified
                                                   by user

            Returns:
                list - list of all folders or files with their full paths
                       inside the input path
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
        """Gets the content of the backup for this subclient at the path
           specified.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not default: True

                vm_disk_browse      (bool)  --  browse virtual machine files
                                                e.g.; .vmdk files, etc.
                                                only applicable when browsing
                                                content inside a guest virtual
                                                machine
                                                default: False

                vm_files_browse      (bool)  -- browse files and folders
                                                default: True

            Returns:
                list - list of all folders or files with their full paths
                       inside the input path

                dict - path along with the details like name, file/folder,
                       size, modification time

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

    def parse_nics_xml(self, input_xml):
        """
            Gets the content of the backup for this subclient at the path
            specified.

            Args:
                input_xml : --   nics info xml per vm to parse the nics name
                                 and label

            Returns:
                nic_list:   --    list of all Nics for a VM

            Raise:
                SDKException:
                    if input parameter is not proper


        """
        if not isinstance(input_xml, basestring):
            raise SDKException("Subclient", "101")

        root = ET.fromstring(input_xml)

        nic_list = []

        for nic in root.findall('nic'):
            name = nic.get('name')
            label = nic.get('label')

            nic_info = {
                'name': name,
                'label': label
            }
            nic_list.append(nic_info)

        return nic_list

    def get_nics_from_browse(self):
        """
            Browses the vm to get the nics info xml, gets the nics info using
            the parse_nics_xml method and prepares the dict for nics json


            Returns:
                dict:   --   dict with key as vm_name and the value as the
                             nics info for that vm

        """

        path, path_dict = self.browse(vm_disk_browse=True)

        nics_dict = {}
        nics = ""
        for vmpath in path:
            result = path_dict[vmpath]
            name = ""
            if 'name' in result:
                name = result['name']
            if 'advanced_data' in result:
                advanced_data = result['advanced_data']

                if 'browseMetaData' in advanced_data:
                    browse_meta_data = advanced_data['browseMetaData']

                    if 'virtualServerMetaData' in browse_meta_data:
                        virtual_server_metadata = browse_meta_data['virtualServerMetaData']

                        if 'nics' in virtual_server_metadata:
                            nics = virtual_server_metadata['nics']

            nics_dict[name] = self.parse_nics_xml(nics)

        return nics_dict

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
                    vm_path             (str)   --  folder path to get the
                                                    contents of
                                                    default: '\\'
                                                    returns the root of the
                                                    Backup content

                    show_deleted_files  (bool)  --  include deleted files in
                                                    the content or not
                                                    default: True

                    restore_index       (bool)  --  restore index if it is not
                                                    cached  default: True

                    vm_disk_browse      (bool)  --  browse the VM disks or not
                                                    default: False

                    from_date           (str)   --  date to get the contents
                                                    after
                                                    format: dd/MM/YYYY
                                                    gets contents from
                                                    01/01/1970 if not specified
                                                    default: None

                    to_date             (str)  --   date to get the contents
                                                    before
                                                    format: dd/MM/YYYY
                                                    gets contents till current
                                                    day if not specified
                                                    default: None

                Returns:
                    list - list of all folders or files with their full paths
                           inside the input path

                    dict - path along with the details like name, file/folder,
                           size, modification time

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

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not default: True


                from_date           (str)   --  date to get the contents after
                                                format: dd/MM/YYYY
                                                gets contents from 01/01/1970
                                                if not specified
                                                default: None

                to_date             (str)  --  date to get the contents before
                                               format: dd/MM/YYYY
                                               gets contents till current day
                                               if not specified
                                               default: None

            Returns:
                list - list of all folders or files with their full paths
                       inside the input path

                dict - path along with the details like name, file/folder,
                       size, modification time

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

            elif os.path.splitext(path)[1] == "":
                paths_list.append(path)

        paths_dict = {}

        for path in browse_content[1]:
            if any(path.lower().endswith(Ext) for Ext in self.diskExtension):
                paths_dict[path] = browse_content[1][path]
            elif os.path.splitext(path)[1] == "":
                # assuming it as Fusion compute kind of hypervisors
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
        """Browses the Files and Folders inside a Virtual Machine in the time
           range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents
                                                of
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not default: True

                restore_index       (bool)  --  restore index if it is not cached
                                                default: True

                from_date           (str)   --  date to get the contents after
                                                format: dd/MM/YYYY

                                                gets contents from 01/01/1970
                                                if not specified
                                                default: None

                to_date             (str)  --  date to get the contents before
                                               format: dd/MM/YYYY

                                               gets contents till current day
                                               if not specified
                                               default: None

            Returns:
                list - list of all folders or files with their full paths
                       inside the input path

                dict - path along with the details like name, file/folder,
                       size, modification time

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
        Check if the particular folder is present in browse of the subclient
        in particular VM

        args:
            _vm_id      (str)     -- VM id from which folder has to be restored

            folder_path (str)     -- folder path which has to be restored

        exception:
            raise exception
                if folder is not present in browse
        """

        source_item = None

        _folder_to_restore = _folder_to_restore.replace(":", "")
        _restore_folder_name = _folder_to_restore.split("\\")[-1]
        _folder_to_restore = _folder_to_restore.replace("\\" + _restore_folder_name, "")
        _source_path = r'\\'.join([_vm_id, _folder_to_restore])

        _browse_files, _browse_files_dict = self.guest_files_browse(
            _source_path, from_date=from_date, to_date=to_date)

        for _path in _browse_files_dict:
            _browse_folder_name = _path.split("\\")[-1]
            if _browse_folder_name == _restore_folder_name:
                source_item = r'\\'.join([_source_path, _restore_folder_name])
                break

        if source_item is None:
            raise SDKException('Subclient', '113')

        return source_item

    def guest_file_restore(self,
                           vm_name=None,
                           folder_to_restore=None,
                           destination_client=None,
                           destination_path=None,
                           copy_preceedence=0,
                           preserve_level=1,
                           unconditional_overwrite=False,
                           restore_ACL=True,
                           from_date=None,
                           to_date=None,
                           show_deleted_files=True):
        """perform Guest file restore of the provided path

        Args:
            vm_name             (basestring)   --  VM from which files needs to be
                                            restored

            folder_to_restore    (basestring)  -- folder path to restore

            show_deleted_files  (bool)  --  include deleted files in the
                                            content or not
                                            default: True


            destination_path    (basestring)   --  path to restore

            from_date           (basestring)   --  date to get the contents after
                                            format: dd/MM/YYYY
                                            gets contents from 01/01/1970 if
                                            not specified default: None

            to_date             (basestring)   --  date to get the contents before
                                            format: dd/MM/YYYY
                                            gets contents till current day
                                            if not specified default: None

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
        if not(isinstance(destination_path, basestring) and
               (isinstance(vm_name, basestring)) and
               (isinstance(folder_to_restore, basestring))):
            raise SDKException('Subclient', '105')

        if vm_name not in _vm_names:
            raise SDKException('Subclient', '111')

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._instance_object.co_ordinator

        if isinstance(destination_client, Client):
            client = destination_client
        elif isinstance(destination_client, basestring):
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

        _file_restore_option["paths"] = []
        for _each_folder in _folder_to_restore_list:
            _file_restore_option["paths"].append(
                self._check_folder_in_browse(_vm_ids[vm_name],
                                             "%s" %_each_folder,
                                             from_date,
                                             to_date))

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
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not
                                                default: True

            Returns:
                list - list of all folders or files with their full paths
                       inside the input path

                dict - path along with the details like name, file/folder,
                       size, modification time

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
        """Browses the Files and Folders of a Virtual Machine in the time range
           specified.

            Args:
                vm_path             (basestring)   --  folder path to get the contents
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not
                                                default: True

                restore_index       (bool)  --  restore index if it is not
                                                cached
                                                default: True

                from_date           (basestring)   --  date to get the contents after
                                                format: dd/MM/YYYY
                                                gets contents from 01/01/1970
                                                if not specified
                                                default: None

                to_date             (basestring)  --   date to get the contents before
                                                format: dd/MM/YYYY
                                                gets contents till current day
                                                if not specified
                                                default: None

            Returns:
                list - list of all folders or files with their full paths
                       inside the input path

                dict - path along with the details like name, file/folder,
                       size, modification time

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

    def _get_disk_extension(self, disk_list):
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

        if len(_extn_list) > 1:
            return _extn_list
        else:
            return _extn_list[0]

    def _get_conversion_disk_Type(self, _src_disk_extn, _dest_disk_extn):
        """
        return volume restore type and destination disk Type

        Args:
            src_disk_extn   (basestring)   --  source disk extension of the disk
            dest_disk_extn  (basestring)   --  Extension to which disk is converted

        return
            _vol_restore_type   (basestring)   -- value of Volume restore type
                                           parameter of the XML
            _dest_disk_type     (basestring)   -- value of destination Disk Type
                                           parameter of the XML
        """

        disk_conversion = {
            "vhdx": {
                "vhd": ("VIRTUAL_HARD_DISKS", "VHD_DYNAMIC"),
                "vmdk": ("VMDK_FILES", "VMDK_VCB4")
            },
            "vmdk": {
                "vhd": ("VIRTUAL_HARD_DISKS", "VHD_DYNAMIC"),
                "vhdx": ("VIRTUAL_HARD_DISKS", "VHDX_DYNAMIC")
            }
        }
        _src_disk_extn = _src_disk_extn.lower().strip(".")
        _dest_disk_extn = _dest_disk_extn.lower().strip(".")

        return disk_conversion[_src_disk_extn][_dest_disk_extn]

    def _set_vm_to_restore(self, vm_to_restore=None, restore_option=None):
        """
        check whether the VMs provided for restore is backued up else assume
                            Vm_to_restore with default

        Args:
            vm_to_restore   (list)      -- list of Vm to restore

            restore_option  (dict)      -- dict with all restore options

        return:
            vm_to_restore   (list)      -- Final list of Vm need to be restored

        """
        if restore_option is None:
            restore_option = {}

        if not self._vm_names_browse:
            self._get_vm_ids_and_names_dict_from_browse()

        # set vms to restore
        if not vm_to_restore:
            vm_to_restore = restore_option.get("vm_to_restore", self._vm_ids_browse)
            _temp_res_list = vm_to_restore

        else:
            _temp_res_list = []
            _temp_res_list.append(vm_to_restore)

        vm_to_restore = list(set(self._vm_names_browse) & set(_temp_res_list))

        if not vm_to_restore:
            raise SDKException('Subclient', 104)

        return vm_to_restore

    def _set_restore_inputs(self, restore_option, **kwargs):
        """
        set all the advanced properties of the subclient restore

        Args:
            restore_option  (dict)  -- restore option dictionary where advanced
                                            properties to be appended

            **kwargs                --  Keyword arguments with key as property name
                                            and its value
        """
        for key in kwargs:
            if key not in restore_option or restore_option[key] is None:
                restore_option[key] = kwargs[key]

    def _set_restore_defaults(self, restore_option):
        """
        :param restore_option:  dict with all restore input values
        """

        if (("vcenter_client" not in restore_option) or (
                restore_option["vcenter_client"] is None)):
            instance_dict = self._backupset_object._instance_object._properties['instance']
            restore_option["destination_client_name"] = instance_dict["clientName"]
            restore_option["destination_instance"] = instance_dict["instanceName"]
            instance = self._backupset_object._instance_object

        else:
            client = self._commcell_object.clients.get(restore_option["vcenter_client"])
            restore_option["destination_client_name"] = restore_option["vcenter_client"]
            agent = client.agents.get('Virtual Server')
            instancekeys = next(iter(agent.instances._instances))
            instance = agent.instances.get(instancekeys)
            restore_option["destination_instance"] = instance.instance_name

        restore_option["esx_server"] = instance.server_host_name[0]

        if (("client_name" not in restore_option) or
                (restore_option["client_name"] is None)):
            restore_option["client_name"] = instance.co_ordinator
        else:
            restore_option["client_name"] = restore_option["proxy_client"]

    def set_advanced_vm_restore_options(self, vm_to_restore, restore_option):
        """
        set tje advanced restore options for all vm in restore
        :param

        vm_to_restore : Name of the VM to restore
        restore_option: restore options that need to be set for advanced restore option

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
        """


        # Set the new name for the restored VM.
        # If new_name is not given, it restores the VM with same name
        # with suffix Delete.
        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        browse_result = self.vm_files_browse()

        # vs metadata from browse result
        _metadata = browse_result[1][('\\' + vm_to_restore)]
        vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]

        # populate restore source item
        restore_option['paths'].append("\\" + vm_ids[vm_to_restore])
        restore_option['name'] = vm_to_restore
        restore_option['guid'] = vm_ids[vm_to_restore]


        # populate restore disk and datastore
        vm_disks = []
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\\\" + vm_ids[vm_to_restore])

        for disk, data in disk_info_dict.items():

            self._set_restore_inputs(restore_option,
                                     datastore=data["advanced_data"]["browseMetaData"][
                                         "virtualServerMetaData"]["datastore"])

            _disk_dict = self._disk_dict_pattern(disk.split('\\')[-1], restore_option["datastore"])

            vm_disks.append(_disk_dict)

        restore_option["disks"] = vm_disks

        if not vm_disks:
            raise SDKException('Subclient', 104)

        # prepare nics info json
        nics_list = self._json_nics_advancedRestoreOptions(vm_to_restore)
        restore_option["nics"] = nics_list

        # populate VM Specific values
        self._set_restore_inputs(
            restore_option,
            disks=vm_disks,
            esx_host=vs_metadata['esxHost'],
            new_name="Delete" + vm_to_restore
        )

        temp_dict = self._json_restore_advancedRestoreOptions(restore_option)
        self._advanced_restore_option_list.append(temp_dict)

    def _prepare_filelevel_restore_json(self, _file_restore_option):
        """
        prepares the  file level restore json from getters
        """


        if _file_restore_option is None:
            _file_restore_option = {}

        # set the setters
        self._backupset_object._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_file_restore_option)
        self._json_restore_virtualServerRstOption(_file_restore_option)
        self._json_restore_volumeRstOption(_file_restore_option)

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["virtualServerRstOption"] = self._virtualserver_option_restore_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["volumeRstOption"] = self._volume_restore_json

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
                paths                 - GUID of VM from which disk needs to be restored
                                                eg:\\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

                copy_precedence_applicable  - True if needs copy_preceedence to be honored else
                                                        False

                copy_preceedence            - the copy id from which browse and
                                                                restore needs to be performed

        returns:
            request_json        -complete json for performing disk Restore options

        """

        if _disk_restore_option is None:
            _disk_restore_option = {}


        # set the setters
        self._backupset_object._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_disk_restore_option)
        self._json_restore_virtualServerRstOption(_disk_restore_option)
        self._json_restore_diskLevelVMRestoreOption(_disk_restore_option)

        _virt_restore_json = self._virtualserver_option_restore_json
        _virt_restore_json["diskLevelVMRestoreOption"] = self._json_disklevel_option_restore
        self._json_restore_volumeRstOption(_disk_restore_option)

        request_json["taskInfo"]["subTasks"][0][
            "options"]["restoreOptions"]["virtualServerRstOption"] = _virt_restore_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["volumeRstOption"] = self._volume_restore_json

        return request_json

    def _prepare_fullvm_restore_json(self, restore_option=None):
        """
        Prepare Full VM restore Json with all getters

        Args:
            restore_option - dictionary with all VM restore options

        value:
            preserve_level              - set the preserve level in restore

            unconditional_overwrite     - unconditionally overwrite the disk
                                          in the restore path

            destination_path            - path where the disk needs to be
                                          restored

            client_name                 - client where the disk needs to be
                                          restored

            destination_vendor          - vendor id of the Hypervisor

            destination_disktype        - type of disk needs to be restored
                                          like VHDX,VHD,VMDK

            source_item                 - GUID of VM from which disk needs to
                                          be restored
                                          eg:
                                          \\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

            copy_precedence_applicable  - True if needs copy_preceedence to
                                          be honoured else False

            copy_preceedence            - the copy id from which browse and
                                          restore needs to be performed

            power_on                    - power on the VM after restore

            add_to_failover             - Register the VM to Failover Cluster

            datastore                   - Datastore where the VM needs to be
                                          restored

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
            esx_host                    - esx_host or client name where it need
                                          to be restored
            name                        - name of the VM to be restored

        returns:
              request_json        -complete json for perfomring Full VM Restore
                                   options

        """

        if restore_option is None:
            restore_option = {}
        restore_option['paths'] = []
        restore_option["destination_vendor"] = \
            self._backupset_object._instance_object._vendor_id

        #set all the restore defaults
        self._set_restore_defaults(restore_option)

        # set the setters
        self._backupset_object._instance_object._restore_association = self._subClientEntity
        self._json_restore_virtualServerRstOption(restore_option)
        self._json_restore_diskLevelVMRestoreOption(restore_option)
        self._json_restore_volumeRstOption(restore_option)
        self._json_vcenter_instance(restore_option)

        for _each_vm_to_restore in restore_option['vm_to_restore']:
            if restore_option["out_place"]:
                restore_option["new_name"] = restore_option["restore_new_name"]
            else:
                restore_option["new_name"] = _each_vm_to_restore
            self.set_advanced_vm_restore_options(_each_vm_to_restore, restore_option)

        #prepare json
        request_json = self._restore_json(restore_option=restore_option)
        _virt_restore_json = self._virtualserver_option_restore_json
        _virt_restore_json["diskLevelVMRestoreOption"] = self._json_disklevel_option_restore
        _virt_restore_json["vCenterInstance"] = self._vcenter_instance_json
        _virt_restore_json["diskLevelVMRestoreOption"][
            "advancedRestoreOptions"] = self._advanced_restore_option_list

        request_json["taskInfo"]["subTasks"][0][
            "options"]["restoreOptions"]["virtualServerRstOption"] = _virt_restore_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["volumeRstOption"] = self._volume_restore_json

        return request_json
