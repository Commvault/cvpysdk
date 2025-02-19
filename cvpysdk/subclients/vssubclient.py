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

"""File for operating on a Virtual Server Subclient.

VirualServerSubclient is the only class defined in this file.

VirtualServerSubclient: Derived class from the Subclient Base class, representing a
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

    _full_vm_restore_update_json_for_v2     -- modifies the restore json as per v2
                                                subclient details and returns it

    backup()                               --  run a backup job for the subclient

    _advanced_backup_options()              --  sets the advanced backup options

    update_properties()                       --  child method to add vsa specific properties to update properties

    index_server                            --  Property to get/set the indexserver client for the subclient

To add a new Virtual Subclient,  create a class in a new module under virtualserver sub package


The new module which is created has to named in the following manner:
1. Name the module with the name of the Virtual Server without special characters
2.Spaces alone must be replaced with underscores('_')

For eg:

    The Virtual Server 'Red Hat Virtualization' is named as 'red_hat_virtualization.py'

    The Virtual Server 'Hyper-V' is named as 'hyperv.py'

"""

import os
import re
from enum import Enum
import copy
import xml.etree.ElementTree as ET
from importlib import import_module
from inspect import getmembers, isclass, isabstract

import xmltodict

from cvpysdk.plan import Plans
from ..exception import SDKException
from ..client import Client
from ..subclient import Subclient
from ..constants import VSAObjects, HypervisorType, VsInstanceType


class VirtualServerSubclient(Subclient):
    """Derived class from Subclient Base class, representing a virtual server subclient,
        and to perform operations on that subclient."""

    def __new__(cls, backupset_object, subclient_name, subclient_id=None):
        """Decides which instance object needs to be created"""

        instance_name = VsInstanceType.VSINSTANCE_TYPE[backupset_object._instance_object._vsinstancetype]

        try:
            subclient_module = import_module("cvpysdk.subclients.virtualserver.{}".format(instance_name))
        except ImportError:
            subclient_module = import_module("cvpysdk.subclients.virtualserver.null")

        classes = getmembers(subclient_module, lambda m: isclass(m) and not isabstract(m))

        for name, _class in classes:
            if issubclass(_class, VirtualServerSubclient) and _class.__module__.rsplit(".", 1)[-1] == instance_name:
                return object.__new__(_class)

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
            '16': 'UnprotectedVMs',
            '17': 'Root',
            '34': 'Tag',
            '35': 'TagCategory'
        }

        self.filter_types = {
            '1': 'Datastore',
            '2': 'Virtual Disk Name/Pattern',
            '3': 'Virtual Device Node',
            '4': 'Container',
            '5': 'Disk Label',
            '6': 'Disk Type',
            '9': 'Disk Tag Name/Value',
            '10':'Repository'
        }

        self._disk_option = {
            'original': 0,
            'thicklazyzero': 1,
            'thin': 2,
            'thickeagerzero': 3
        }

        self._transport_mode = {
            'auto': 0,
            'san': 1,
            'hotadd': 2,
            'nbd': 5,
            'nbdssl': 4
        }

        self._vm_names_browse = []
        self._vm_ids_browse = {}
        self._advanced_restore_option_list = []
        self._live_sync = None

    class disk_pattern(Enum):
        """
        stores the disk pattern of all hypervisors
        """
        name = "name"
        datastore = "Datastore"
        new_name = "newName"

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
            content = self._get_content_list(children)
        return content

    @property
    def subclient_proxy(self):
        """
            Gets the List of proxies at the Subclient

            Returns:
                    list         (list) :    Proxies at the subclient
        """
        return self._get_subclient_proxies()

    @property
    def instance_proxy(self):
        """
        Gets the proxy at instance level

        Returns:
                string          (string) :      Proxy at instane
        """
        return self._proxyClient.get('clientName', None)

    @property
    def vm_filter(self):
        """Gets the appropriate filter from the Subclient relevant to the user.

            Returns:
                list - list of filter associated with the subclient
        """
        vm_filter = []
        if self._vmFilter:
            subclient_filter = self._vmFilter
            if 'children' in subclient_filter:
                children = subclient_filter['children']
                vm_filter = self._get_content_list(children)
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
                    filter_type_id = str(child['filterType'])
                    filter_type = self.filter_types[str(child['filterType'])]
                    vm_id = child['vmGuid'] if 'vmGuid' in child else None
                    filter_name = child['filter']
                    value = child['value']

                    temp_dict = {
                        'filter': filter_name,
                        'filterType': filter_type,
                        'vmGuid': vm_id,
                        'filterTypeId': filter_type_id,
                        'value':value
                    }

                    vm_diskfilter.append(temp_dict)
        else:
            vm_diskfilter = self._vmDiskFilter

        if len(vm_diskfilter) == 0:
            vm_diskfilter = None
        return vm_diskfilter

    @property
    def metadata(self):
        """
            Get if collect files/metadata value for given subclient.
            Returns status as True/False (string)
            Default: False for subclient which doesnt have the property
        """
        collectdetails = r'collectFileDetails'
        if collectdetails in self._vsaSubclientProp:
            vsasubclient_collect_details = self._vsaSubclientProp[collectdetails]
        else:
            vsasubclient_collect_details = False
        return vsasubclient_collect_details

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
                        subclient_content = [{'allOrAnyChildren': True, 'content': [
                            {'equal_value': True, 'allOrAnyChildren': True, 'display_name': '*abc*', 'type': 'VMName'},
                            {'equal_value': False, 'allOrAnyChildren': True, 'display_name': 'xyz', 'type': 'VMName'}]},
                                      {'allOrAnyChildren': False, 'content': [
                                          {'equal_value': True, 'allOrAnyChildren': True, 'display_name': '*12*',
                                           'type': 'VMName'},
                                          {'equal_value': True, 'allOrAnyChildren': True, 'display_name': '*34*',
                                           'type': 'VMName'}]}]
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
            for entity in subclient_content:
                virtual_server_dict = dict()
                if not isinstance(entity, dict):
                    entity = {'content': entity}
                elif 'content' not in entity:
                    entity = {'content': entity}
                virtual_server_dict['allOrAnyChildren'] = entity.get('allOrAnyChildren', True)
                virtual_server_dict['children'] = []

                def add_childrens(item, multiple_rule=False):
                    """
                    add contents in the hierarchy
                    Args:
                        item                (dict)  :   content's current item to be added
                        multiple_rule       (bool)  :   If multiple rule present or not

                    """
                    temp = {
                        'allOrAnyChildren': item.get('allOrAnyChildren', True),
                        'equalsOrNotEquals': item.get('equal_value', True),
                        'name': item.get('name', ""),
                        'displayName': item.get('display_name', ''),
                        'path': '',
                        'type': item['type'] if (
                                isinstance(item['type'], int) or isinstance(item['type'], str)) else
                        item['type'].value
                    }
                    if item['type'] == VSAObjects.VMNotes:
                        temp['value'] = item['display_name']
                        temp['displayName'] = item['display_name']
                        temp['name'] = "Notes"
                    if (item['type'] ==
                            VSAObjects.VMPowerState and
                            item['state'] == 'true'):
                        temp['name'] = "PoweredState"
                        temp['value'] = "1"
                        temp['displayName'] = "Powered On"
                    if (item['type'] ==
                            VSAObjects.VMPowerState and
                            item['state'] == 'false'):
                        temp['name'] = "PoweredState"
                        temp['value'] = "0"
                        temp['displayName'] = "Powered Off"
                    if multiple_rule:
                        virtual_server_dict.get('children').append(temp)
                    else:
                        content.append(temp)
                if not isinstance(entity, list):
                    entity = [entity]
                if len(entity[0]['content']) == 1 or isinstance(entity[0]['content'], dict):
                    if isinstance(entity[0]['content'], list):
                        add_childrens(entity[0]['content'][0])
                    else:
                        add_childrens(entity[0]['content'])
                else:
                    for items in entity:
                        for item in items['content']:
                            add_childrens(item, True)
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
                if temp_dict.get('filterTypeId'):
                    filter_type_id = temp_dict['filterTypeId']
                else:
                    filter_type_id = \
                        list(filter(lambda x: self.filter_types[x].lower() == temp_dict['filtertype'].lower(),
                                    self.filter_types))[
                            0]

                virtual_server_dict = {
                    'filter': temp_dict['filter'],
                    'filterType': filter_type_id,
                    'vmGuid': temp_dict.get('vmGuid')
                }

                vm_diskfilter.append(virtual_server_dict)

        except KeyError as err:
            raise SDKException('Subclient', '102',
                               '{} not given in content'.format(err))

        vs_diskfilter_content = {
            "filters": vm_diskfilter
        }
        self._set_subclient_properties("_vmDiskFilter", vs_diskfilter_content)

    @property
    def live_sync(self):
        """Returns the instance of the VSALiveSync class"""
        if not self._live_sync:
            from .virtualserver.livesync.vsa_live_sync import VsaLiveSync
            self._live_sync = VsaLiveSync(self)

        return self._live_sync

    @property
    def index_server(self):
        """Returns the index server client set for the subclient. None if no Index Server is set"""

        if 'indexSettings' not in self._commonProperties:
            return None

        index_settings = self._commonProperties['indexSettings']
        index_server = None

        if ('currentIndexServer' in index_settings and
                'clientName' in index_settings['currentIndexServer']):
            index_server = index_settings['currentIndexServer']['clientName']

        if index_server is None:
            return None

        return self._commcell_object.clients.get(index_server)

    @index_server.setter
    def index_server(self, value):
        """Sets the index server client for the backupset

            Args:
                value   (object)    --  The index server client object to set

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        if not isinstance(value, Client):
            raise SDKException('Subclient', '121')

        index_server_name = value.client_name

        self._set_subclient_properties(
            "_commonProperties['indexSettings']['currentIndexServer']['clientName']",
            index_server_name)

    def _get_disk_provisioning_value(self, provisioningType):
        """
         Returns the provisioning code for the selected type

        Args:
                provisioningType  (String) - Disk provisioning type

        return: (int) - diskProvisionValue

        """
        # Defaults to "original"
        disk_provision_value = 0
        provisioningType = provisioningType.replace(" ", "").lower()
        if provisioningType in self._disk_option:
            disk_provision_value = self._disk_option[provisioningType]
        return disk_provision_value

    @metadata.setter
    def metadata(self, value=True):
        """
        Set given value of collectFileDetails/metadata (True/false) on the subclient

        Args:
                value   (str)    True/False

        """
        collectdetails = r'collectFileDetails'
        if collectdetails in self._vsaSubclientProp:
            self._set_subclient_properties("_vsaSubclientProp['collectFileDetails']", value)

    @property
    def cbtvalue(self):
        """
        Get CBT value for given subclient.

        Returns:
            (Boolean)    True/False

        """
        return self._subclient_properties.get('vsaSubclientProp', {}).get("useChangedTrackingOnVM", False)


    @cbtvalue.setter
    def cbtvalue(self, value):
        """
        Set CBT value for given subclient

        Args:
            value   (Boolean)   True/False

        """
        update_properties = self.properties
        update_properties["vsaSubclientProp"]['useChangedTrackingOnVM'] = value
        self.update_properties(update_properties)

    def update_properties(self, properties_dict):
        """
        child method to add any specific attributes for vsa
        Args:
            properties_dict         (dict):     dict of all propterties of subclient
        """
        properties_dict.update({
            "vmFilterOperationType": "OVERWRITE",
            "vmContentOperationType": "OVERWRITE",
            "vmDiskFilterOperationType": "OVERWRITE"
        })
        super().update_properties(properties_dict)

    def _get_content_list(self, children):
        """
        Gets the content in list format
        Args:
            children                            (list):     Content if the subclient

        Returns:
            content_list                        (list):     Content of the subclient
        """

        content_list = []
        for child in children:
            path = child['path'] if 'path' in child else None
            allOrAnyChildren = child['allOrAnyChildren'] if 'allOrAnyChildren' in child else None
            _temp_list = []
            _temp_dict = {}
            if 'children' in child:
                nested_children = child['children']
                for each_condition in nested_children:
                    display_name = each_condition['displayName']
                    content_type = VSAObjects(each_condition['type']).name
                    vm_id = '' if each_condition.get('name', '') in display_name else each_condition.get('name', '')
                    temp_dict = {
                        'equal_value': each_condition.get('equalsOrNotEquals', True),
                        'allOrAnyChildren': each_condition.get('allOrAnyChildren', True),
                        'id': vm_id,
                        'path': path,
                        'display_name': display_name,
                        'type': content_type
                    }
                    _temp_list.append(temp_dict)
                _temp_dict['allOrAnyChildren'] = allOrAnyChildren
                _temp_dict['content'] = _temp_list
                content_list.append(_temp_dict)
            else:
                display_name = child['displayName']
                content_type = VSAObjects(child['type']).name
                vm_id = child.get('name', '')
                temp_dict = {
                    'equal_value': child['equalsOrNotEquals'],
                    'allOrAnyChildren': child.get('allOrAnyChildren', True),
                    'id': vm_id,
                    'path': path,
                    'display_name': display_name,
                    'type': content_type
                }
                content_list.append(temp_dict)
        return content_list

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of Virtual server subclient.

        """

        self._vmDiskFilter = None
        self._vmFilter = None
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

    def _disk_dict_pattern(self, name, datastore, new_name=None):
        """
        set the disk dictionary of the hypervisor

        Args:
                name            (str)       --  name of the disk

                datastore       (str)       --  datastore where the disk has to be restored

                new_name        (str)       --  new name of the disk

            Returns:

                disk dictionary(dict)       -- Dictionary with key name, new name , datastore
                                                and corresponding
        """

        if not new_name and not self._instance_object.instance_name == HypervisorType.GOOGLE_CLOUD.value.lower():
            new_name = name
        temp_disk_dict = {}
        temp_disk_dict[self.disk_pattern.name.value] = name
        temp_disk_dict[self.disk_pattern.datastore.value] = datastore
        temp_disk_dict[self.disk_pattern.new_name.value] = new_name
        return temp_disk_dict

    def _json_vcenter_instance(self, value):
        """ Setter for vcenter_instance JSON """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._virtualserver_option_restore_json["vCenterInstance"] = {
            "clientName": value.get("destination_client_name", ""),
            "instanceName": value.get("destination_instance", ""),
            "appName": value.get("appName", "Virtual Server")
        }

        if value.get("destination_instance_id") and value.get("destination_client_id"):
            self._virtualserver_option_restore_json["vCenterInstance"].update(
                {"instanceId": value.get("destination_instance_id", 0),
                 "clientId": value.get("destination_client_id", 0)}
            )

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
            "isBlockLevelReplication": value.get("block_level", False)
        }

        if value.get('run_security_scan'):
            self._virtualserver_option_restore_json['securityScanOptions'] = {
                "runSecurityScan": value.get("run_security_scan", False)
            }

        if value.get('replication_guid'):
            self._virtualserver_option_restore_json['replicationGuid'] = value['replication_guid']

    def _json_restore_virtualServerRstOption_filelevelrestoreoption(self, value):
        """
            setter for  the File level restore option for agent less restore option in restore json
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        return {
            "serverName": value.get("server_name", ''),
            "vmGuid": value.get("vm_guid", ''),
            "vmName": value.get("vm_name", '')
        }

    def _json_restore_guest_password(self, value):
        """
            setter for vm credentials for agentless restore option in restore json
        """
        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        return {
            "userName": value.get("user_name", ''),
            "password": value.get("password", '')
        }

    def _json_nics_advancedRestoreOptions(self, vm_to_restore, value):
        """
            Setter for nics list for advanced restore option json
        """

        nics_dict_from_browse = self.get_nics_from_browse(copy_precedence=value.get('copy_precedence', 0))
        nics_list = []
        vm_nics_list = nics_dict_from_browse[vm_to_restore]
        for network_card_dict in vm_nics_list:
            if self._instance_object.instance_name == HypervisorType.GOOGLE_CLOUD.value.lower():
                current_project = network_card_dict.get('subnetId').split('/')[6]
                if value.get('project_id') is not None:
                    network_card_dict['subnetId'] = value.get('subnetwork_nic')
                    network_card_dict['sourceNetwork'] = value.get('networks_nic')
                    network_card_dict['publicIPaddress'] = value.get('publicIPaddress')
                    network_card_dict['privateIPaddress'] = value.get('privateIPaddress')

            _destnetwork = value.get("destination_network",
                                     value.get('network',
                                               network_card_dict['name']))

            nics = {
                "subnetId": network_card_dict.get('subnetId', ""),
                "sourceNetwork": network_card_dict['name'],
                "sourceNetworkId": network_card_dict.get('sourceNetwork', ""),
                "name": (network_card_dict.get('sourceNetwork',
                                               "") + _destnetwork) if self._instance_object.instance_name ==
                                                                      HypervisorType.GOOGLE_CLOUD.value.lower() and _destnetwork else
                network_card_dict['label'],
                "publicIPaddress": network_card_dict.get("publicIPaddress",""),
                "privateIPaddress": network_card_dict.get("privateIPaddress",""),
                "networkName": _destnetwork if _destnetwork else '',
                "destinationNetwork": _destnetwork if _destnetwork else network_card_dict['name']
            }

            # setting nics for azureRM instance
            if value.get('destination_instance').lower() == HypervisorType.AZURE_V2.value.lower():
                if value.get('subnet_id'):
                    nics["subnetId"] = value.get('subnet_id')
                    nics["networkName"] = value.get('subnet_id').split('/')[0]
                    nics["networkDisplayName"] = nics["networkName"] + '\\' + value.get('subnet_id').split('/')[-1]
                elif "networkDisplayName" in value and 'networkrsg' in value and 'destsubid' in value:
                    nics["networkDisplayName"] = value["networkDisplayName"]
                    nics["networkName"] = value["networkDisplayName"].split('\\')[0]
                    modify_nics = value.get('subnetId', nics['subnetId']).split('/')
                    modify_nics[8] = nics["networkName"]
                    modify_nics[4] = value['networkrsg']
                    modify_nics[2] = value['destsubid']
                    modify_nics[10] = value["networkDisplayName"].split('\\')[1]
                    final_nics = ""
                    for each_info in modify_nics[1:]:
                        final_nics = final_nics + '/' + each_info
                    nics["subnetId"] = final_nics
                    name = ''
                    for each_info in modify_nics[1:9]:
                        name = name + '/' + each_info
                    nics["name"] = name

            nics_list.append(nics)

        return nics_list

    def _json_vmip_advanced_restore_options(self, value):
        """
            Setting IP for destination vm
        """
        vmip = []
        _asterisk = "*.*.*.*"
        vm_ip = {
            "sourceIP": value.get("source_ip"),
            "sourceSubnet": value["source_subnet"] if value.get("source_subnet") else _asterisk,
            "sourceGateway": value["source_gateway"] if value.get("source_gateway") else _asterisk,
            "destinationIP": value.get("destination_ip"),
            "destinationSubnet": value["destination_subnet"] if value.get("destination_subnet") else _asterisk,
            "destinationGateway": value["destination_gateway"] if value.get("destination_gateway") else _asterisk,
            "primaryDNS": value.get("primary_dns", ""),
            "alternateDNS": value.get("alternate_dns", ""),
            "primaryWins": value.get("primare_wins", ""),
            "altenameWins": value.get("alternate_wins", ""),
            "useDhcp": False
        }
        vmip.append(vm_ip)
        return vmip

    def _json_restore_diskLevelVMRestoreOption(self, value):
        """setter for  the disk Level VM Restore Option    in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')
        vcenter_userpwd = ''
        if 'vmware' in self._instance_object.instance_name:
            vcenter_userpwd = self._instance_object._user_name

        json_disklevel_option_restore = {
            "esxServerName": value.get("esx_server", ""),
            "vmFolderName": value.get("vm_folder", ""),
            "dataCenterName": value.get("data_center", ""),
            "hostOrCluster": value.get("host_cluster", ""),
            "diskOption": value.get("disk_option", 0),
            "vmName": "",
            "transportMode": value.get("transport_mode", 0),
            "passUnconditionalOverride": value.get("unconditional_overwrite", False),
            "powerOnVmAfterRestore": value.get("power_on", False),
            "registerWithFailoverCluster": value.get("add_to_failover", False),
            "userPassword": {"userName": vcenter_userpwd or "admin"},
            "redirectWritesToDatastore": value.get("redirectWritesToDatastore", ""),
            "delayMigrationMinutes": value.get("delayMigrationMinutes", 0)
        }
        if value['in_place']:
            json_disklevel_option_restore["dataStore"] = {}
        if value.get('distribute_vm_workload'):
            json_disklevel_option_restore["maxNumOfVMPerJob"] = value['distribute_vm_workload']

        self._virtualserver_option_restore_json["diskLevelVMRestoreOption"] = json_disklevel_option_restore

    def _json_restore_attach_diskLevelVMRestoreOption(self, value):
        """setter for the attach disk Level VM Restore Option in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        json_disklevel_option_restore = {
            "esxServerName": value.get("esxHost", ""),
            "diskOption": value.get("disk_option", 0),
            "passUnconditionalOverride": value.get("unconditional_overwrite", False),
            "powerOnVmAfterRestore": value.get("power_on", False),
            "transportMode": value.get("transport_mode", 0),
            "userPassword": {"userName": value.get("userName",""),"password": value.get("password","")}
        }
        self._virtualserver_option_restore_json["diskLevelVMRestoreOption"] = json_disklevel_option_restore

    def _json_restore_advancedRestoreOptions(self, value):
        """setter for the Virtual server restore  option in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._advanced_option_restore_json = {
            "disks": value.get("disks", []),
            "guid": value.get("guid", ""),
            "newGuid": value.get("new_guid", ""),
            "newName": value.get("new_name", ""),
            "esxHost": value.get("esx_host", ""),
            "projectId": value.get("project_id", ""),
            "cluster": value.get("cluster", ""),
            "name": value.get("name", ""),
            "nics": value.get("nics", []),
            "vmIPAddressOptions": value.get("vm_ip_address_options", []),
            "FolderPath": value.get("FolderPath", ""),
            "resourcePoolPath": value.get("ResourcePool", ""),
            "volumeType": value.get("volumeType", "Auto"),
            "vmCustomMetadata": value.get("vmCustomMetadata",[])
        }

        value_dict = {
            "createPublicIP": ["createPublicIP", ["createPublicIP", ""]],
            "restoreAsManagedVM": ["restoreAsManagedVM", ["restoreAsManagedVM", ""]],
            "destination_os_name": ["osName", ["destination_os_name", "AUTO"]],
            "resourcePoolPath": ["resourcePoolPath", ["resourcePoolPath", ""]],
            "datacenter": ["datacenter", ["datacenter", ""]],
            "terminationProtected": ["terminationProtected", ["terminationProtected", False]],
            "securityGroups": ["securityGroups", ["securityGroups", ""]],
            "keyPairList": ["keyPairList", ["keyPairList", ""]]
        }

        for key in value_dict:
            if key in value:
                inner_key = value_dict[key][0]
                val1, val2 = value_dict[key][1][0], value_dict[key][1][1]
                self._advanced_option_restore_json[inner_key] = value.get(val1, val2)

        if "vmSize" in value:
            val1, val2 = ("instanceSize", "") if not value["vmSize"] else ("vmSize", "vmSize")
            self._advanced_option_restore_json["vmSize"] = value.get(val1, val2)
        if "ami" in value and value["ami"] is not None:
            self._advanced_option_restore_json["templateId"] = value["ami"]["templateId"]
            if value.get('ami', {}).get('templateName'):
                self._advanced_option_restore_json["templateName"] = value["ami"]["templateName"]
        if "iamRole" in value and value["iamRole"] is not None:
            self._advanced_option_restore_json["roleInfo"] = {
                "name": value["iamRole"]
            }
        if value.get("serviceAccount", {}).get("email"):
            self._advanced_option_restore_json["roleInfo"] = {
                "email": value.get("serviceAccount").get("email"),
                "name": value.get("serviceAccount").get("displayName"),
                "id": value.get("serviceAccount").get("uniqueId")
            }
        if self._instance_object.instance_name == 'openstack':
            if "securityGroups" in value and value["securityGroups"] is not None:
                self._advanced_option_restore_json["securityGroups"] = [{"groupName": value["securityGroups"]}]
        if "destComputerName" in value and value["destComputerName"] is not None:
            self._advanced_option_restore_json["destComputerName"] = value["destComputerName"]
        if "destComputerUserName" in value and value["destComputerUserName"] is not None:
            self._advanced_option_restore_json["destComputerUserName"] = value["destComputerUserName"]
        if "instanceAdminPassword" in value and value["instanceAdminPassword"] is not None:
            self._advanced_option_restore_json["instanceAdminPassword"] = value["instanceAdminPassword"]

        if self.disk_pattern.datastore.value == "DestinationPath":
            self._advanced_option_restore_json["DestinationPath"] = value.get("datastore", "")

        else:
            self._advanced_option_restore_json["Datastore"] = value.get("datastore", "")

        if value.get('block_level'):
            self._advanced_option_restore_json["blrRecoveryOpts"] = \
                self._json_restore_blrRecoveryOpts(value)

        temp_dict = copy.deepcopy(self._advanced_option_restore_json)
        return temp_dict

    def _json_restore_blrRecoveryOpts(self, value):
        """ setter for blr recovery options in block level json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        return {
            "recoveryType": value.get("recovery_type", 1),
            "granularV2": {
                "ccrpInterval": value.get("ccrp_interval", 300),
                "acrpInterval": value.get("acrp_interval", 0),
                "maxRpInterval": value.get("max_RpInterval", 21600),
                "rpMergeDelay": value.get("rp_merge_delay", 172800),
                "rpRetention": value.get("rp_retention", 604800),
                "maxRpStoreOfflineTime": value.get("max_RpStore_OfflineTime", 0),
                "useOffPeakSchedule": value.get("use_OffPeak_Schedule", 0),
                "rpStoreId": value.get("rpstore_id", ""),
                "rpStoreName": value.get("rpstore_name", "")
            }
        }

    def _json_restore_volumeRstOption(self, value):
        """setter for  the Volume restore option for in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        return{
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

        def _assign_vm_name_id(contents, _vm_ids, _vm_names):
            for _content in contents:
                if _content.get('content'):
                    _vm_ids, _vm_names = _assign_vm_name_id(_content['content'], _vm_ids, _vm_names)
                    continue
                if _content['type'].lower() in ('vm', 'virtual machine'):
                    _vm_ids[_content['id']] = _content['display_name']
                    _vm_names[_content['display_name']] = _content['id']
                else:
                    _vm_ids = {}
                    _vm_names = {}
                    break
            return _vm_ids, _vm_names
        return _assign_vm_name_id(self.content, vm_ids, vm_names)

    def _get_vm_ids_and_names_dict_from_browse(self):
        """Parses through the Browse content and get the VMs Backed up

            returns :
                vm_names    (list)  -- returns list of VMs backed up
                vm_ids      (dict)  -- returns id list of VMs backed up
        """

        _vm_ids, _vm_names = self._get_vm_ids_and_names_dict()
        if not self._vm_names_browse:
            paths, paths_dict = self.browse()
            if not _vm_names:
                for key, val in paths_dict.items():
                    _vm_names[val['name']] = val['snap_display_name']
            for _each_path in paths_dict:
                _vm_id = _each_path.split("\\")[1]
                self._vm_names_browse.append(_vm_id)
                self._vm_ids_browse[_vm_id] = _vm_names[_vm_id]

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
               show_deleted_files=False,
               vm_disk_browse=False,
               vm_files_browse=False,
               operation='browse',
               copy_precedence=0,
               **kwargs
               ):
        """Gets the content of the backup for this subclient at the path
           specified.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not default: False

                vm_disk_browse      (bool)  --  browse virtual machine files
                                                e.g.; .vmdk files, etc.
                                                only applicable when browsing
                                                content inside a guest virtual
                                                machine
                                                default: False

                vm_files_browse      (bool)  -- browse files and folders
                                                default: True

                operation            (str)   -- Type of operation, browser of find

                copy_precedence      (int)   -- The copy precedence to do the operation from

            Kwargs(optional)

                live_browse           (bool)   -- set to True to get live browse content
                                                    even though file indexing is enabled

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

        if operation == 'find':
            # Return all VMs browse content for find operation
            vm_path_list = []
            browse_content_dict = {}
            if not vm_names:
                _vm_ids, vm_names = self._get_vm_ids_and_names_dict_from_browse()
            vm_paths = ['\\' + vm_id for vm_id in vm_names.values()]
            for vm_path in vm_paths:
                vm_path = self._parse_vm_path(vm_names, vm_path)
                browse_content = super(VirtualServerSubclient, self).browse(
                    show_deleted_files, vm_disk_browse, True, path=vm_path,
                    vs_file_browse=vm_files_browse, operation=operation,
                    copy_precedence=copy_precedence
                )
                vm_path_list += browse_content[0]
                browse_content_dict.update(browse_content[1])
            browse_content = (vm_path_list, browse_content_dict)

        else:
            vm_path = self._parse_vm_path(vm_names, vm_path)
            browse_content = super(VirtualServerSubclient, self).browse(
                show_deleted_files, vm_disk_browse, True, path=vm_path,
                vs_file_browse=vm_files_browse, operation=operation, **kwargs
            )

        if not vm_ids:
            for key, val in browse_content[1].items():
                vm_ids[val['snap_display_name']] = val['name']
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
        if not isinstance(input_xml, str):
            raise SDKException("Subclient", "101")

        root = ET.fromstring(input_xml)

        nic_list = []

        for nic in root.findall('nic'):
            name = nic.get('name')
            label = nic.get('label')
            subnet = nic.get('subnet')
            networkDisplayName = nic.get('networkDisplayName', "")
            sourceNetwork = nic.get('id',"")

            nic_info = {
                'name': name,
                'label': label,
                'subnetId': subnet,
                'networkDisplayName': networkDisplayName,
                'sourceNetwork': sourceNetwork
            }
            nic_list.append(nic_info)

        return nic_list

    def get_nics_from_browse(self, copy_precedence=0):
        """
            Browses the vm to get the nics info xml, gets the nics info using
            the parse_nics_xml method and prepares the dict for nics json

            Args:
                copy_precedence     (int)   --  The copy precedence to do browse from

            Returns:
                dict:   --   dict with key as vm_name and the value as the
                             nics info for that vm

        """

        path, path_dict = self.browse(vm_disk_browse=True, copy_precedence=copy_precedence)

        nics_dict = {}
        nics = ""

        # Added for v2.1
        for vmpath in path:
            result = path_dict[vmpath]
            if ('browseMetaData' not in result['advanced_data']) or \
                    ('virtualServerMetaData' not in result['advanced_data']['browseMetaData']) or \
                    ('nics' not in result['advanced_data']['browseMetaData']['virtualServerMetaData']):
                path, path_dict = self.browse(vm_disk_browse=True, operation='find', copy_precedence=copy_precedence)
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
            show_deleted_files=False,
            restore_index=True,
            vm_disk_browse=False,
            from_date=0,
            to_date=0,
            copy_precedence=0,
            vm_files_browse=False,
            media_agent=""):
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
                                                    default: False

                    restore_index       (bool)  --  restore index if it is not
                                                    cached  default: True

                    vm_disk_browse      (bool)  --  browse the VM disks or not
                                                    default: False

                    from_date           (int)   --  date to get the contents
                                                    after
                                                    format: dd/MM/YYYY
                                                    gets contents from
                                                    01/01/1970 if not specified
                                                    default: 0

                    to_date             (int)  --   date to get the contents
                                                    before
                                                    format: dd/MM/YYYY
                                                    gets contents till current
                                                    day if not specified
                                                    default: 0

                    copy_precedence     (int)   --  copy precedence to be used
                                                    for browsing

                    media_agent         (str)   --  Browse MA via with Browse has to happen.
                                                    It can be MA different than Storage Policy MA

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
            show_deleted=show_deleted_files, restore_index=restore_index,
            vm_disk_browse=vm_disk_browse,
            from_time=from_date, to_time=to_date, copy_precedence=copy_precedence,
            path=vm_path, vs_file_browse=vm_files_browse, media_agent=media_agent)
        if not vm_ids:
            for key, val in browse_content[1].items():
                vm_ids[val['snap_display_name']] = val['name']
        return self._process_vsa_browse_response(vm_ids, browse_content)

    def disk_level_browse(self, vm_path='\\',
                          show_deleted_files=False,
                          restore_index=True,
                          from_date=0,
                          to_date=0,
                          copy_precedence=0):
        """Browses the Disks of a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not default: False

                restore_index  (bool)  --       Restore index or not.
                                                default: True

                from_date           (int)   --  date to get the contents after
                                                format: dd/MM/YYYY
                                                gets contents from 01/01/1970
                                                if not specified
                                                default: 0

                to_date             (int)  --  date to get the contents before
                                               format: dd/MM/YYYY
                                               gets contents till current day
                                               if not specified
                                               default: 0

                copy_precedence     (int)   --  copy precedence to be used
                                                    for browsing

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
            vm_path, show_deleted_files, restore_index, True, from_date, to_date, copy_precedence
        )

        paths_list = []
        for path in browse_content[0]:
            if any(path.lower().endswith(Ext) for Ext in self.diskExtension):
                paths_list.append(path)

            elif os.path.splitext(path)[1] == "" and "none" in self.diskExtension:
                paths_list.append(path)

        paths_dict = {}

        for path in browse_content[1]:
            if any(path.lower().endswith(Ext) for Ext in self.diskExtension):
                paths_dict[path] = browse_content[1][path]
            elif os.path.splitext(path)[1] == "" and "none" in self.diskExtension:
                # assuming it as Fusion compute kind of hypervisors
                paths_dict[path] = browse_content[1][path]

        if paths_list and paths_dict:
            return paths_list, paths_dict
        else:
            raise SDKException('Subclient', '113')

    def guest_files_browse(
            self,
            vm_path='\\',
            show_deleted_files=False,
            restore_index=True,
            from_date=0,
            to_date=0,
            copy_precedence=0,
            media_agent=""):
        """Browses the Files and Folders inside a Virtual Machine in the time
           range specified.

            Args:
                vm_path             (str)   --  folder path to get the contents
                                                of
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not default: False

                restore_index       (bool)  --  restore index if it is not cached
                                                default: True

                from_date           (int)   --  date to get the contents after
                                                format: dd/MM/YYYY

                                                gets contents from 01/01/1970
                                                if not specified
                                                default: 0

                to_date             (int)  --  date to get the contents before
                                               format: dd/MM/YYYY

                                               gets contents till current day
                                               if not specified
                                               default: 0

                copy_precedence     (int)   --  copy precedence to be used
                                                    for browsing

                media_agent         (str)   --  Browse MA via with Browse has to happen.
                                                It can be MA different than Storage Policy MA

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
            vm_path, show_deleted_files, restore_index, False, from_date, to_date, copy_precedence,
            vm_files_browse=True, media_agent=media_agent)

    def _check_folder_in_browse(
            self,
            _vm_id,
            _folder_to_restore,
            from_date,
            to_date,
            copy_precedence,
            media_agent):
        """
        Check if the particular folder is present in browse of the subclient
        in particular VM

        args:
            _vm_id      (str)     -- VM id from which folder has to be restored

            _folder_to_restore (str)     -- folder path which has to be restored

            from_date           (int)   --  date to get the contents after
                                                format: dd/MM/YYYY

                                                gets contents from 01/01/1970
                                                if not specified
                                                default: 0

            to_date             (int)  --  date to get the contents before
                                               format: dd/MM/YYYY

                                               gets contents till current day
                                               if not specified
                                               default: 0

            copy_precedence     (int)   --  copy precedence to be used
                                                    for browsing

            media_agent         (str)   --  Browse MA via with Browse has to hapeen .
                                                    It can be MA different than Storage Policy MA

        exception:
            raise exception
                if folder is not present in browse
        """

        source_item = None

        _folder_to_restore = _folder_to_restore.replace(":", "")
        _restore_folder_name = _folder_to_restore.split("\\")[-1]
        _folder_to_restore = _folder_to_restore.replace("\\" + _restore_folder_name, "")
        _source_path = '\\'.join([_vm_id, _folder_to_restore])

        _browse_files, _browse_files_dict = self.guest_files_browse(
            _source_path, from_date=from_date, to_date=to_date,
            copy_precedence=copy_precedence, media_agent=media_agent)

        for _path in _browse_files_dict:
            _browse_folder_name = _path.split("\\")[-1]
            if _browse_folder_name == _restore_folder_name:
                source_item = '\\'.join([_source_path, _restore_folder_name])
                source_item = '\\' + source_item
                break

        if source_item is None:
            raise SDKException('Subclient', '102', 'Browse failure: Folder not found in browse')

        return source_item

    def guest_file_restore(self, *args, **kwargs):
        """perform Guest file restore of the provided path

        Args:
            options     (dict)  --  dictionary of guest file restores options

        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs
        vm_name = options.get('vm_name', None)
        folder_to_restore = options.get('folder_to_restore', None)
        destination_client = options.get('destination_client', None)
        destination_path = options.get('destination_path', None)
        copy_precedence = options.get('copy_precedence', 0)
        preserve_level = options.get('preserve_level', 1)
        unconditional_overwrite = options.get('unconditional_overwrite', False)
        restore_ACL = options.get('restore_ACL', True)
        from_date = options.get('from_date', 0)
        to_date = options.get('to_date', 0)
        show_deleted_files = options.get('show_deleted_files', False)
        fbr_ma = options.get('fbr_ma', None)
        browse_ma = options.get('browse_ma', "")
        agentless = options.get('agentless', "")
        in_place = options.get('in_place', False)

        _vm_names, _vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _file_restore_option = {}
        _verify_path = options.get('verify_path', True)

        # check if inputs are correct
        if not(isinstance(destination_path, str) and
               (isinstance(vm_name, str))):
            raise SDKException('Subclient', '105')

        if vm_name not in _vm_names:
            raise SDKException('Subclient', '111')

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._instance_object.co_ordinator

        if fbr_ma:
            _file_restore_option["proxy_client"] = fbr_ma

        _file_restore_option["client"] = destination_client
        _file_restore_option["destination_path"] = destination_path

        # process the folder to restore for browse
        if isinstance(folder_to_restore, list):
            _folder_to_restore_list = folder_to_restore

        elif isinstance(folder_to_restore, str):
            _folder_to_restore_list = []
            _folder_to_restore_list.append(folder_to_restore)
        else:
            raise SDKException('Subclient', '105')

        _file_restore_option["paths"] = []
        for _each_folder in _folder_to_restore_list:
            # check_folder_in_browse modifies path (removes colon) and verifies in browse results.
            # The modified path does not work for windows VM when file indexing is enabled
            # Set `verify_path` to False to skip this verification and use the restore path as is

            if _verify_path:
                _restore_item_path = self._check_folder_in_browse(
                    _vm_ids[vm_name],
                    "%s" % _each_folder,
                    from_date,
                    to_date,
                    copy_precedence,
                    media_agent=browse_ma
                )
            else:
                # Converting native path to VM path
                # C:\folder1 => \<vm_guid>\C:\folder1
                # /folder1/folder2 => \<vm_guid>\folder1\folder2

                _item_path = _each_folder.replace('/', '\\')
                _item_path = _item_path[1:] if _item_path[0] == '\\' else _item_path
                _restore_item_path = '\\'.join(['', _vm_ids[vm_name], _item_path])

            _file_restore_option["paths"].append(_restore_item_path)

        # set the browse options
        _file_restore_option["disk_browse"] = False
        _file_restore_option["file_browse"] = True
        _file_restore_option["from_time"] = from_date
        _file_restore_option["to_time"] = to_date

        # set the common file level restore options
        _file_restore_option["striplevel_type"] = "PRESERVE_LEVEL"
        _file_restore_option["preserve_level"] = preserve_level
        _file_restore_option["unconditional_overwrite"] = unconditional_overwrite
        _file_restore_option["restore_ACL"] = restore_ACL
        _file_restore_option["in_place"] = in_place

        # set the browse option
        _file_restore_option["copy_precedence_applicable"] = True
        _file_restore_option["copy_precedence"] = copy_precedence
        _file_restore_option["media_agent"] = browse_ma

        # set agentless options
        if agentless:
            _file_restore_option["server_name"] = agentless['vserver']
            _file_restore_option["vm_guid"] = agentless['vm_guid']
            _file_restore_option["vm_name"] = agentless['vm_name']
            _file_restore_option["user_name"] = agentless['vm_user']
            _file_restore_option["password"] = agentless['vm_pass']
            _file_restore_option["agentless"] = True

        # prepare and execute the Json
        request_json = self._prepare_filelevel_restore_json(_file_restore_option)
        return self._process_restore_response(request_json)

    def vm_files_browse(self, vm_path='\\', show_deleted_files=False, operation='browse', copy_precedence=0):
        """Browses the Files and Folders of a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not
                                                default: False

                operation           (str)   --  The type of operation to perform (browse/find)

                copy_precedence     (int)   --  The copy precedence to do browse from

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
        return self.browse(vm_path, show_deleted_files, True, operation=operation, copy_precedence=copy_precedence)

    def vm_files_browse_in_time(
            self,
            vm_path='\\',
            show_deleted_files=False,
            restore_index=True,
            from_date=0,
            to_date=0):
        """Browses the Files and Folders of a Virtual Machine in the time range
           specified.

            Args:
                vm_path             (str)   --  folder path to get the contents
                                                default: '\\';
                                                returns the root of the Backup
                                                content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not
                                                default: False

                restore_index       (bool)  --  restore index if it is not
                                                cached
                                                default: True

                from_date           (int)   --  date to get the contents after
                                                format: dd/MM/YYYY
                                                gets contents from 01/01/1970
                                                if not specified
                                                default: 0

                to_date             (int)  --   date to get the contents before
                                                format: dd/MM/YYYY
                                                gets contents till current day
                                                if not specified
                                                default: 0

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

    def reinitialize_vm_names_browse(self):
        self._vm_names_browse = []
        self._get_vm_ids_and_names_dict_from_browse()

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
            src_disk_extn   (str)   --  source disk extension of the disk
            dest_disk_extn  (str)   --  Extension to which disk is converted

        return
            _vol_restore_type   (str)   -- value of Volume restore type
                                           parameter of the XML
            _dest_disk_type     (str)   -- value of destination Disk Type
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
            if not isinstance(vm_to_restore, list):
                vm_to_restore = [vm_to_restore]
            for each_vm in vm_to_restore:
                _temp_res_list.append(each_vm)

        vm_to_restore = list(set(self._vm_names_browse) & set(_temp_res_list))

        if not vm_to_restore:
            raise SDKException('Subclient', '104')

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

    def _get_subclient_proxies(self):
        """
        Get the list of all the proxies on a selected subclient

        Returns:
            associated_proxies   (List)  --  returns the proxies list
        """
        associated_proxies = []
        try:
            available_subclient_proxies = self._vsaSubclientProp["proxies"]["memberServers"]
            if len(available_subclient_proxies) > 0:
                for client in available_subclient_proxies:
                    if 'clientName' in client['client']:
                        associated_proxies.append(client["client"]["clientName"])
                    elif 'clientGroupName' in client['client']:
                        client_group = self._commcell_object.client_groups.get(client["client"]["clientGroupName"])
                        associated_proxies.extend(client_group.associated_clients)
        except KeyError:
            pass
        return list(dict.fromkeys(associated_proxies))

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
            restore_option["destination_client_id"] = int(client.client_id)
            agent = client.agents.get('Virtual Server')
            instancekeys = next(iter(agent.instances._instances))
            instance = agent.instances.get(instancekeys)
            restore_option["destination_instance"] = instance.instance_name
            restore_option["destination_instance_id"] = int(instance.instance_id)

        if (("esx_server" not in restore_option) or
                (restore_option["esx_server"] is None)):
            restore_option["esx_server"] = instance.server_host_name[0]

        if (("client_name" not in restore_option) or
                (restore_option["client_name"] is None)):
            subclient_proxy_list = self._get_subclient_proxies()

            if len(subclient_proxy_list) > 0:
                restore_option["client"] = subclient_proxy_list[0]
            else:
                restore_option["client"] = instance.co_ordinator
        else:
            restore_option["client"] = restore_option["client_name"]

    def _set_vm_conversion_defaults(self, vcenter_client, restore_option):
        """
        set all the VMconversion changews need to be performed
        Args:
            vcenter_client: Client Name to which it has to be converted

            restore_option: dictinoary where parameter needs to be set

        Returns:
            subclient :     (obj)   : object for the subclient class of virtual client
            raise exception:
             if client does not exist

        """

        client = self._commcell_object.clients.get(vcenter_client)
        agent = client.agents.get('Virtual Server')
        instancekeys = next(iter(agent.instances._instances))
        instance = agent.instances.get(instancekeys)
        backupsetkeys = next(iter(instance.backupsets._backupsets))
        backupset = instance.backupsets.get(backupsetkeys)
        sckeys = next(iter(backupset.subclients._subclients))
        subclient = backupset.subclients.get(sckeys)

        # populating all defaults
        esx_server = instance.server_host_name[0]
        self.disk_pattern = subclient.disk_pattern
        restore_option["destination_vendor"] = instance._vendor_id
        restore_option["backupset_client_name"] = client.client_name

        if not subclient:
            raise SDKException('Subclient', '104')

        return subclient

    def set_advanced_vm_restore_options(self, vm_to_restore, restore_option):
        """
        set the advanced restore options for all vm in restore
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
        copy_precedence = restore_option.get('copy_precedence', 0)
        browse_result = self.vm_files_browse(copy_precedence=copy_precedence)

        # vs metadata from browse result
        _metadata = browse_result[1][('\\' + vm_to_restore)]

        if ('browseMetaData' not in _metadata['advanced_data']) or \
                ('virtualServerMetaData' not in _metadata['advanced_data']['browseMetaData']) or \
                ('nics' not in _metadata['advanced_data']['browseMetaData']['virtualServerMetaData']):
            browse_result = self.vm_files_browse(operation='find', copy_precedence=copy_precedence)
            _metadata = browse_result[1][('\\' + vm_to_restore)]

        vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]
        if restore_option['in_place']:
            folder_path = vs_metadata.get("inventoryPath", '')
            instanceSize = vs_metadata.get("instanceSize", '')
        else:
            folder_path = restore_option['folder_path'] if restore_option.get('folder_path') else ''
            instanceSize = ''

        if 'resourcePoolPath' in restore_option and restore_option['resourcePoolPath'] is None:
            restore_option['resourcePoolPath'] = vs_metadata['resourcePoolPath']
        if 'datacenter' in restore_option and restore_option['datacenter'] is None:
            restore_option['datacenter'] = vs_metadata.get('dataCenter', '')
        if ('terminationProtected' in restore_option and
                restore_option['terminationProtected'] is None):
            restore_option['terminationProtected'] = vs_metadata.get('terminationProtected', '')
        if 'iamRole' in restore_option and restore_option['iamRole'] is None:
            restore_option['iamRole'] = vs_metadata.get('role', '')
        if 'securityGroups' in restore_option and restore_option['securityGroups'] is None:
            _security_groups = self._find_security_groups(vs_metadata['networkSecurityGroups'])
            restore_option['securityGroups'] = _security_groups
        if 'keyPairList' in restore_option and restore_option['keyPairList'] is None:
            _keypair_list = self._find_keypair_list(vs_metadata['loginKeyPairs'])
            restore_option['keyPairList'] = _keypair_list

        # populate restore source item
        restore_option['paths'].append("\\" + vm_ids[vm_to_restore])
        restore_option['name'] = vm_to_restore
        restore_option['guid'] = vm_ids[vm_to_restore]
        restore_option["FolderPath"] = folder_path
        restore_option["ResourcePool"] = "/"

        # populate restore disk and datastore
        vm_disks = []
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\\\" + vm_ids[vm_to_restore], copy_precedence=copy_precedence)

        for disk, data in disk_info_dict.items():
            ds = ""
            if "datastore" in restore_option:
                ds = restore_option["datastore"]
            if restore_option[
                "in_place"] or "datastore" not in restore_option or not restore_option.get(
                    'datastore'):
                if "datastore" in data["advanced_data"]["browseMetaData"]["virtualServerMetaData"]:
                    restore_option["datastore"] = data["advanced_data"]["browseMetaData"][
                        "virtualServerMetaData"]["datastore"]
                    ds = restore_option["datastore"]
                elif "esxHost" in vs_metadata and "is_aws_proxy" in restore_option:
                    if restore_option.get("availability_zone") is not None:
                        ds = restore_option.get("availability_zone")
                    else:
                        ds = vs_metadata["esxHost"]
            new_name_prefix = restore_option.get("disk_name_prefix")
            new_name = data["name"] if new_name_prefix is None \
                else new_name_prefix + "_" + data["name"]
            if self._instance_object.instance_name == HypervisorType.GOOGLE_CLOUD.value.lower():
                new_name = ""
                if data["advanced_data"]["browseMetaData"]["virtualServerMetaData"].get('replicaZones', False):
                    replicaZones = restore_option.get("replicaZones")
            if restore_option['destination_instance'].lower() in [HypervisorType.VIRTUAL_CENTER.value.lower(),
                                                                  HypervisorType.AZURE_V2.value.lower()]:
                _disk_dict = self._disk_dict_pattern(data['snap_display_name'], ds, new_name)
            else:
                _disk_dict = self._disk_dict_pattern(disk.split('\\')[-1], ds, new_name)
            if 'is_aws_proxy' in restore_option and not restore_option['is_aws_proxy']:
                _disk_dict['Datastore'] = restore_option["datastore"]
            vm_disks.append(_disk_dict)
        if not vm_disks:
            raise SDKException('Subclient', '104')
        restore_option["disks"] = vm_disks

        # prepare nics info json
        if "nics" not in restore_option or \
                self._instance_object.instance_name == HypervisorType.GOOGLE_CLOUD.value.lower():
            nics_list = self._json_nics_advancedRestoreOptions(vm_to_restore, restore_option)
            restore_option["nics"] = nics_list
            if restore_option.get('source_ip') and restore_option.get('destination_ip'):
                vm_ip = self._json_vmip_advanced_restore_options(restore_option)
                restore_option["vm_ip_address_options"] = vm_ip
            if restore_option["in_place"]:
                if "hyper" in restore_option["destination_instance"].lower():
                    restore_option["client_name"] = vs_metadata['esxHost']
                    restore_option["esx_server"] = vs_metadata['esxHost']
                elif 'Red' in restore_option["destination_instance"]:
                    restore_option["esxHost"] = vs_metadata['clusterName']
                    restore_option["cluster"] = vs_metadata['clusterName']
                    vs_metadata["esxHost"] = vs_metadata['clusterName']

        # populate VM Specific values
        self._set_restore_inputs(
            restore_option,
            disks=vm_disks,
            esx_host=restore_option.get('esx_host') or vs_metadata['esxHost'],
            instanceSize=restore_option.get('instanceSize', instanceSize),
            new_name=restore_option.get('new_name', "del" + vm_to_restore)
        )

        temp_dict = self._json_restore_advancedRestoreOptions(restore_option)
        self._advanced_restore_option_list.append(temp_dict)

    def set_advanced_attach_disk_restore_options(self, vm_to_restore, restore_option):
        """
        set the advanced restore options for all vm in restore
        :param

        vm_to_restore : Name of the VM where disks will be restored
        restore_option: restore options that need to be set for advanced restore option

            datastore                   - Datastore where the disks needs to be restored

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
        _ = self.vm_files_browse()
        # populate restore source item
        restore_option['name'] = vm_to_restore
        restore_option['guid'] = vm_ids[vm_to_restore]
        restore_option["FolderPath"] = ''
        restore_option["ResourcePool"] = "/"

        # populate restore disk and datastore
        vm_disks = []
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\\\" + vm_ids[vm_to_restore])

        for disk, data in disk_info_dict.items():
            ds = ""
            if "datastore" in restore_option:
                ds = restore_option["datastore"]
            new_name_prefix = restore_option.get("disk_name_prefix")
            if self._instance_object.instance_name != 'openstack':
                new_name = data["snap_display_name"].replace("/", "_").replace(" ", "_")
                new_name = "del_" + new_name if new_name_prefix is None \
                    else new_name_prefix + "_" + new_name
            else:
                new_name = data["name"]
            _disk_dict = self._disk_dict_pattern(data['snap_display_name'], ds, new_name)
            vm_disks.append(_disk_dict)
        if not vm_disks:
            raise SDKException('Subclient', '104')
        restore_option["disks"] = vm_disks

        # populate VM Specific values
        self._set_restore_inputs(
            restore_option,
            disks=vm_disks,
            esx_host=restore_option.get('esx'),
            new_name=restore_option.get('newName', vm_to_restore),
            new_guid=restore_option.get('newGUID', restore_option.get('guid')),
            datastore=restore_option.get('datastore'))

        temp_dict = self._json_restore_advancedRestoreOptions(restore_option)
        self._advanced_restore_option_list.append(temp_dict)

    @staticmethod
    def _find_security_groups(xml_str):
        """
        sets the security group json from the input xml
        Args:
             xml_str            (str)  --  xml from which we want to retrieve security group info
        Returns:
             security_group    (dict)  -- security group dict
        """
        match1 = re.search(r'secGroupId=\"(\S*)\"', xml_str)
        match2 = re.search(r'secGroupName=\"(\S*)\"', xml_str)
        security_group = [
            {
                "groupId": match1.group(1),
                "groupName": match2.group(1)
            }
        ]
        return security_group

    @staticmethod
    def _find_keypair_list(xml_str):
        """
        sets the keypair list json from the input xml
        Args:
             xml_str            (str)  --  xml from which we want to retrieve keypair list info
        Returns:
             keypair_list	(dict) -- keypair list dict
        """
        match1 = re.search(r'keyPairId=\"(\S*)\"', xml_str)
        match2 = re.search(r'keyPairName=\"(\S*)\"', xml_str)
        keypair_list = [
            {
                "keyId": match1.group(1),
                "keyName": match2.group(1)
            }
        ]
        return keypair_list

    def amazon_defaults(self, vm_to_restore, restore_option):
        """
               set all the VMconversion changes need to be performed
               specfic to Amazon
               Args:
                   vm_to_restore  (str)  :  content of destination subclient object

                   restore_option (dict) :  dictionary with all VM restore options

        """

        browse_result = self.vm_files_browse()
        # vs metadata from browse result
        _metadata = browse_result[1][('\\' + vm_to_restore)]
        if ('browseMetaData' not in _metadata['advanced_data']) or \
                ('virtualServerMetaData' not in _metadata['advanced_data']['browseMetaData']) or \
                ('nics' not in _metadata['advanced_data']['browseMetaData']['virtualServerMetaData']):
            browse_result = self.vm_files_browse(operation='find')
            _metadata = browse_result[1][('\\' + vm_to_restore)]
        vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]

        restore_option['resourcePoolPath'] = vs_metadata['resourcePoolPath']
        restore_option['datacenter'] = vs_metadata.get('dataCenter', '')
        restore_option['terminationProtected'] = vs_metadata.get('terminationProtected', '')
        restore_option['iamRole'] = vs_metadata.get('role', '')
        _security_groups = self._find_security_groups(vs_metadata['networkSecurityGroups'])
        restore_option['securityGroups'] = _security_groups
        _keypair_list = self._find_keypair_list(vs_metadata['loginKeyPairs'])
        restore_option['keyPairList'] = _keypair_list
        restore_option['esx_host'] = vs_metadata.get('esxHost', '')
        restore_option['datastore'] = vs_metadata.get('datastore', '')

        nics_list = self._json_nics_advancedRestoreOptions(vm_to_restore, restore_option)
        restore_option["nics"] = nics_list

        return restore_option

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

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["virtualServerRstOption"] = self._virtualserver_option_restore_json

        if _file_restore_option.get('agentless'):
            request_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]["virtualServerRstOption"][
                "fileLevelVMRestoreOption"] = \
                self._json_restore_virtualServerRstOption_filelevelrestoreoption(_file_restore_option)
            request_json["taskInfo"]["subTasks"][0]["options"][
                "restoreOptions"]["virtualServerRstOption"]["fileLevelVMRestoreOption"][
                "guestUserPassword"] = self._json_restore_guest_password(_file_restore_option)

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["volumeRstOption"] = self._json_restore_volumeRstOption(_file_restore_option)

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

                copy_precedence_applicable  - True if needs copy_precedence to be honored else
                                                        False

                copy_precedence            - the copy id from which browse and
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

        request_json["taskInfo"]["subTasks"][0][
            "options"]["restoreOptions"]["virtualServerRstOption"] = self._virtualserver_option_restore_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["volumeRstOption"] = self._json_restore_volumeRstOption(_disk_restore_option)

        return request_json

    def _prepare_attach_disk_restore_json(self, _disk_restore_option=None):
        """
        Prepare attach disk retsore Json with all getters

        Args:
            _disk_restore_option - dictionary with all attach disk restore options

            value:
                destination_path            - path where the disk needs to be restored

                client_name                 - client where the disk needs to be restored

                destination_vendor          - vendor id of the Hypervisor

                paths                 - GUID of VM from which disk needs to be restored
                                                eg:\\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

                copy_precedence_applicable  - True if needs copy_precedence to be honored else
                                                        False

                copy_precedence            - the copy id from which browse and
                                                                restore needs to be performed

        returns:
            request_json        -complete json for performing disk Restore options

        """

        if _disk_restore_option is None:
            _disk_restore_option = {}

        # set the setters
        self._backupset_object._instance_object._restore_association = self._subClientEntity
        request_json = self._restore_json(restore_option=_disk_restore_option)
        self._set_restore_defaults(_disk_restore_option)
        self._json_restore_virtualServerRstOption(_disk_restore_option)
        self._json_vcenter_instance(_disk_restore_option)
        self._json_restore_attach_diskLevelVMRestoreOption(_disk_restore_option)
        self.set_advanced_attach_disk_restore_options(_disk_restore_option['vm_to_restore'], _disk_restore_option)
        self._virtualserver_option_restore_json["diskLevelVMRestoreOption"][
            "advancedRestoreOptions"] = self._advanced_restore_option_list
        self._advanced_restore_option_list = []
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "virtualServerRstOption"] = self._virtualserver_option_restore_json
        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["volumeRstOption"] = self._json_restore_volumeRstOption(_disk_restore_option)
        if _disk_restore_option.get('new_instance'):
            request_json = self._update_attach_disk_restore_new_instance(request_json, _disk_restore_option)
        return request_json

    @staticmethod
    def _update_attach_disk_restore_new_instance(json_to_be_edited, _disk_restore_option):
        """
        Updates teh Json for attach disk restore as a new instance

        Args:
            json_to_be_edited               (dict): Request json to be edited

            _disk_restore_option:           (dict): Attach dsik restore options

        Returns:
            json_to_be_edited               (dict): Dictionary after its edited

        """
        json_to_be_edited['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'virtualServerRstOption']['diskLevelVMRestoreOption']['powerOnVmAfterRestore'] = True
        adv_options = json_to_be_edited['taskInfo']['subTasks'][0]['options']['restoreOptions'][
            'virtualServerRstOption']['diskLevelVMRestoreOption']['advancedRestoreOptions'][0]
        del adv_options['newGuid']
        del adv_options['nics'][0]['destinationNetwork']
        _nic2 = adv_options['nics'][0].copy()
        adv_options['nics'].append(_nic2)
        adv_options['nics'][1]['networkName'] = 'New Network Interface'
        _region = adv_options['esxHost']
        for disks in adv_options['disks']:
            disks['availabilityZone'] = _region
        adv_options['guestOperatingSystemId'] = _disk_restore_option.get('os_id', 0)
        return json_to_be_edited

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

            copy_precedence_applicable  - True if needs copy_precedence to
                                          be honoured else False

            copy_precedence            - the copy id from which browse and
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

        if "destination_vendor" not in restore_option:
            restore_option["destination_vendor"] = \
                self._backupset_object._instance_object._vendor_id

        if restore_option['copy_precedence']:
            restore_option['copy_precedence_applicable'] = True

        # set all the restore defaults
        self._set_restore_defaults(restore_option)

        # set the setters
        self._backupset_object._instance_object._restore_association = self._subClientEntity
        self._json_restore_virtualServerRstOption(restore_option)
        self._json_restore_diskLevelVMRestoreOption(restore_option)
        self._json_vcenter_instance(restore_option)

        for _each_vm_to_restore in restore_option['vm_to_restore']:
            if not restore_option["in_place"]:
                if 'disk_type' in restore_option and restore_option['disk_type']:
                    restore_option['restoreAsManagedVM'] = restore_option['disk_type'][
                        _each_vm_to_restore]
                if ("restore_new_name" in restore_option and
                        restore_option["restore_new_name"] is not None):
                    if len(restore_option['vm_to_restore']) == 1:
                        restore_option["new_name"] = restore_option["restore_new_name"]
                    else:
                        restore_option["new_name"] = restore_option[
                                                         "restore_new_name"] + _each_vm_to_restore
                else:
                    restore_option["new_name"] = "del" + _each_vm_to_restore
            else:
                restore_option["new_name"] = _each_vm_to_restore
            self.set_advanced_vm_restore_options(_each_vm_to_restore, restore_option)

        # prepare json
        request_json = self._restore_json(restore_option=restore_option)
        self._virtualserver_option_restore_json["diskLevelVMRestoreOption"][
            "advancedRestoreOptions"] = self._advanced_restore_option_list
        self._advanced_restore_option_list = []
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "virtualServerRstOption"] = self._virtualserver_option_restore_json
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "volumeRstOption"] = self._json_restore_volumeRstOption(
            restore_option)
        if restore_option.get('v2_details') and len(restore_option.get('vm_to_restore', '')) <= 1:
            request_json = self._full_vm_restore_update_json_for_v2(request_json, restore_option.get('v2_details'))

        return request_json

    @staticmethod
    def _full_vm_restore_update_json_for_v2(json_to_be_edited, v2_details):
        """
        Update the final request JSON to match wth the v2 vm
        Args:
            json_to_be_edited               (dict): Final restore JSON for the restore without v2 subclient details

            v2_details                      (dict): v2 vm subclient details
                                   eg: {
                                            'clientName': 'vm_client1',
                                            'instanceName': 'VMInstance',
                                            'displayName': 'vm_client1',
                                            'backupsetId': 12,
                                            'instanceId': 2,
                                            'subclientId': 123,
                                            'clientId': 1234,
                                            'appName': 'Virtual Server',
                                            'backupsetName': 'defaultBackupSet',
                                            'applicationId': 106,
                                            'subclientName': 'default'
                                        }

        Returns:
            json_to_be_edited        -complete json for performing Full VM Restore
                                        options with v2 subclient details

        """
        json_to_be_edited['taskInfo']['associations'][0]['clientName'] = v2_details.get('clientName')
        json_to_be_edited['taskInfo']['associations'][0]['clientId'] = v2_details.get('clientId')
        json_to_be_edited['taskInfo']['associations'][0]['instanceName'] = v2_details.get('instanceName')
        json_to_be_edited['taskInfo']['associations'][0]['instanceId'] = v2_details.get('instanceId')
        json_to_be_edited['taskInfo']['associations'][0]['displayName'] = v2_details.get('displayName')
        json_to_be_edited['taskInfo']['associations'][0]['backupsetName'] = v2_details.get('backupsetName')
        json_to_be_edited['taskInfo']['associations'][0]['backupsetId'] = v2_details.get('backupsetId')
        json_to_be_edited['taskInfo']['associations'][0]['subclientName'] = v2_details.get('subclientName')
        json_to_be_edited['taskInfo']['associations'][0]['subclientId'] = v2_details.get('subclientId')
        json_to_be_edited['taskInfo']['subTasks'][0]['options']['restoreOptions']['browseOption']['backupset'][
            'clientName'] = v2_details.get('clientName')
        del json_to_be_edited['taskInfo']['associations'][0]['subclientGUID']
        return json_to_be_edited

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               collect_metadata=False,
               advanced_options=None,
               schedule_pattern=None):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level            (str)   --  level of backup the user wish to run
                                                    Full / Incremental / Differential /
                                                    Synthetic_full

                incremental_backup      (bool)  --  run incremental backup
                                                    only applicable in case of Synthetic_full backup

                incremental_level       (str)   --  run incremental backup before/after synthetic full
                                                    BEFORE_SYNTH / AFTER_SYNTH
                                                    only applicable in case of Synthetic_full backup

                collect_metadata        (bool)  --  Collect Meta data for the backup

                advanced_options       (dict)  --  advanced backup options to be included while
                                                    making the request
                    options:
                        create_backup_copy_immediately  --  Run Backup copy just after snap backup
                        backup_copy_type                --  Backup Copy level using storage policy
                                                            or subclient rule

                schedule_pattern (dict) -- scheduling options to be included for the task

                        Please refer schedules.schedulePattern.createSchedule()
                                                                    doc for the types of Jsons

            Returns:
                object - instance of the Job class for this backup job if its an immediate Job

                         instance of the Schedule class for the backup job if its a scheduled Job

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

        if advanced_options or schedule_pattern:
            request_json = self._backup_json(
                backup_level=backup_level,
                incremental_backup=incremental_backup,
                incremental_level=incremental_level,
                advanced_options=advanced_options,
                schedule_pattern=schedule_pattern
            )

            backup_service = self._commcell_object._services['CREATE_TASK']

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

            return self._process_backup_response(flag, response)

        else:
            return super(VirtualServerSubclient, self).backup(backup_level=backup_level,
                                                              incremental_backup=incremental_backup,
                                                              incremental_level=incremental_level,
                                                              collect_metadata=collect_metadata)

    def _advanced_backup_options(self, options):
        """Generates the advanced backup options dict

            Args:
                options         (dict)  --  advanced backup options that are to be included
                                            in the request
                    create_backup_copy_immediately  --  Run Backup copy just after snap backup
                    backup_copy_type                --  Backup Copy level using storage policy
                                                        or subclient rule

            Returns:
            (dict)                      --  generated advanced options dict
        """
        final_dict = super(VirtualServerSubclient, self)._advanced_backup_options(options)

        if 'create_backup_copy_immediately' in options:
            final_dict['dataOpt'] = {
                'createBackupCopyImmediately': options.get('create_backup_copy_immediately', False),
                'backupCopyType': options.get('backup_copy_type', 'USING_STORAGE_POLICY_RULE')
            }

        return final_dict

    def _prepare_blr_json(self, restore_option):

        if "destination_vendor" not in restore_option:
            restore_option["destination_vendor"] = self._backupset_object._instance_object._vendor_id

        # set all the restore defaults
        self._set_restore_defaults(restore_option)

        # Restore Options
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        self._json_restore_virtualServerRstOption(restore_option)

        # Virtual Server RST option
        self._allocation_policy_json(restore_option)
        self._json_restore_diskLevelVMRestoreOption(restore_option)
        self._json_vcenter_instance(restore_option)
        _vm_browse_path_nodes_json = list()
        # Disk Level  VM Restore Options
        self._json_restore_default_restore_settings(restore_option)
        new_name = restore_option["new_name"]
        for _each_vm_to_restore in restore_option['vm_to_restore']:
            if restore_option["prefix"] == 1:
                restore_option["new_name"] = "{}{}".format(new_name, _each_vm_to_restore)
            else:
                restore_option["new_name"] = "{}{}".format(_each_vm_to_restore, new_name)
            self._set_advanced_vm_restore_options_blr(_each_vm_to_restore, restore_option)
            _vm_browse_path_nodes_json.append(self._vm_browse_path_nodes())
        self._virtualserver_option_restore_json["diskLevelVMRestoreOption"]["advancedRestoreOptions"] = self._advanced_restore_option_list[0]

        # prepare json
        request_json = self._restore_json(restore_option=restore_option)
        request_json["taskInfo"]["subTasks"][0]["options"]["vmBrowsePathNodes"] = _vm_browse_path_nodes_json
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["virtualServerRstOption"] = self._virtualserver_option_restore_json
        request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["volumeRstOption"] = self._json_restore_volumeRstOption(
            restore_option)
        request_json["taskInfo"]["subTasks"][0]["subTask"]["operationType"] = 1007
        request_json["taskInfo"]["associations"][0]["_type_"] = 6

        self._advanced_restore_option_list = list()
        request_json["TMMsg_TaskInfo"] = request_json["taskInfo"]
        del request_json["taskInfo"]
        return request_json

    def _vm_browse_path_nodes(self):
        return {
            "browsePath": self._advanced_restore_option_list[-1]["name"],
            "vmGUID": self._advanced_restore_option_list[-1]["guid"],
            "esxHost": self._advanced_restore_option_list[-1]["esxHost"],
            "datastore": self._advanced_restore_option_list[-1]["Datastore"],
            "resourcePoolPath": self._advanced_restore_option_list[-1]["resourcePoolPath"],
            "vmDataStore": self._advanced_restore_option_list[-1]["Datastore"],
            "vmEsxHost": self._advanced_restore_option_list[-1]["esxHost"],
            "vmeResourcePoolPath": self._advanced_restore_option_list[-1]["resourcePoolPath"],
            "isMetadataAvaiable": "0"
        }

    def _json_restore_default_restore_settings(self, restore_option):
        """setter for  the default restore settings in block level json"""

        if not isinstance(restore_option, dict):
            raise SDKException('Subclient', '101')

        self._virtualserver_option_restore_json["diskLevelVMRestoreOption"]["defaultRestoreSettings"] = {
            "esxHost": restore_option["esx_host"],
            "Datastore": restore_option.get("datastore", ""),
            "resourcePoolPath": restore_option.get("resource_pool", "/"),
            "blrRecoveryOpts": self._json_restore_blrRecoveryOpts(restore_option)
        }

    def _allocation_policy_json(self, restore_option):
        self._virtualserver_option_restore_json["allocationPolicy"] = {
            "flags": "",
            "instanceEntity": {
                "flags": ""
            },
            "policyType": "0",
            "region": {
                "flags": ""
            },
            "vmAllocPolicyId": restore_option["target_id"],
            "vmAllocPolicyName": restore_option["target_name"]
        }

    def _prepare_blr_xml(self, restore_option):
        request_json = self._prepare_blr_json(restore_option)

        xml_string = xmltodict.unparse(request_json)
        plans = Plans(self._commcell_object)

        return (
            """<?xml version="1.0" encoding="UTF-8"?><EVGui_SetVMBlockLevelReplicationReq subclientId="{5}" opType="3">
            <blockLevelReplicationTaskXML><![CDATA[{0}]]></blockLevelReplicationTaskXML>
            <subClientProperties>
            <subClientEntity clientId="{1}" applicationId="106" instanceId="{2}" backupsetId="{3}"/>
            <planEntity planId="{4}"/>
            </subClientProperties>
            </EVGui_SetVMBlockLevelReplicationReq>
        """.format(
                xml_string,
                self._client_object.client_id,
                self._instance_object.instance_id,
                self._backupset_object.backupset_id,
                plans.all_plans[restore_option["plan_name"].lower()],
                self._subclient_id))

    def _set_advanced_vm_restore_options_blr(self, vm_to_restore, restore_option):
        """set the advanced restore options for all vm in restore

        vm_to_restore : Name of the VM to restore

        restore_option: restore options that need to be set for advanced restore option

        """

        vm_names, vm_ids = self._get_vm_ids_and_names_dict()

        # populate restore source item
        restore_option['name'] = vm_to_restore
        restore_option['guid'] = vm_ids[vm_to_restore]
        restore_option['paths'].append("\\" + vm_ids[vm_to_restore])
        restore_option["resourcePoolPath"] = "/"

        restore_option["nics"] = {
            "sourceNetwork": restore_option["source_network"],
            "destinationNetwork": restore_option["destination_network"]
        }
        temp_dict = self._json_restore_advancedRestoreOptions(restore_option)
        self._advanced_restore_option_list.append(temp_dict)

    def _prepare_preview_json(self):
        """Prepares the JSON for previewing subclient contents

        Returns:
            JSON - for previewing subclient contents

        """
        return(
            {
                "appId": {
                    "subclientId": int(self.subclient_id),
                    "clientId": int(self._client_object.client_id),
                    "instanceId": int(self._instance_object.instance_id),
                    "backupsetId": int(self._backupset_object.backupset_id),
                    "apptypeId": int(self._agent_object.agent_id)
                },
                "filterEntity": self._vmFilter,
                "contentEntity": self._vmContent
            }
        )

    def _parse_preview_vms(self, subclient_vm_list):
        """Parses the vm list from the preview vm response

        Returns:
            _vm_list        (list)  - List of the vms as the subclient content
        """
        _vm_list = []
        for vm in subclient_vm_list:
            _vm_list.append(vm['name'])
        return _vm_list

    def preview_content(self):
        """
        Preview the subclient and get the content

        Returns:
            list       - List of the vms as the subclient content

        """
        preview = self._commcell_object._services['PREVIEW']
        preview_json = self._prepare_preview_json()

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', preview, preview_json
        )
        if flag and 'scList' in response.json():
            return self._parse_preview_vms(response.json()['scList'])
        else:
            raise SDKException(
                'Subclient',
                '102',
                self._update_response_(
                    response.text))

    @property
    def quiesce_file_system(self):
        """
            Gets the quiesce value set for the vsa subclient

        Returns:
            (Boolean)    True/False
        """
        quiesce_file_system = r'quiesceGuestFileSystemAndApplications'
        return self._vsaSubclientProp.get(quiesce_file_system)

    @quiesce_file_system.setter
    def quiesce_file_system(self, value):
        """
        Sets the quiesce value for the vsa subclient

        Args:
            value   (Boolean)   True/False

        """
        update_properties = self.properties
        update_properties['vsaSubclientProp']['quiesceGuestFileSystemAndApplications'] = value
        self.update_properties(update_properties)