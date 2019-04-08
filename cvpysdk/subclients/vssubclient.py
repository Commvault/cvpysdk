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

    backup()                               --  run a backup job for the subclient

    _advanced_backup_options()              --  sets the advanced backup options

"""

import os
import re
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

        elif instance_name == hv_type.AZURE.value.lower():
            from .virtualserver.azuresubclient import AzureSubclient
            return object.__new__(AzureSubclient)

        elif instance_name == hv_type.AZURE_V2.value.lower():
            from .virtualserver.azureRMsubclient import AzureRMSubclient
            return object.__new__(AzureRMSubclient)


        elif instance_name == hv_type.FUSION_COMPUTE.value.lower():
            from .virtualserver.fusioncomputesubclient import FusionComputeVirtualServerSubclient
            return object.__new__(FusionComputeVirtualServerSubclient)

        elif instance_name == hv_type.ORACLE_VM.value.lower():
            from .virtualserver.oraclevmsubclient import OracleVMVirtualServerSubclient
            return object.__new__(OracleVMVirtualServerSubclient)

        elif instance_name == hv_type.ALIBABA_CLOUD.value.lower():
            from .virtualserver.alibabacloudsubclient import AlibabaCloudVirtualServerSubclient
            return object.__new__(AlibabaCloudVirtualServerSubclient)

        elif instance_name == hv_type.ORACLE_CLOUD.value.lower():
            from .virtualserver.oraclecloudsubclient import OracleCloudVirtualServerSubclient
            return object.__new__(OracleCloudVirtualServerSubclient)

        elif instance_name == hv_type.Azure_Stack.value.lower():
            from .virtualserver.azurestacksubclient import AzureStackSubclient
            return object.__new__(AzureStackSubclient)

        elif instance_name == hv_type.OPENSTACK.value.lower():
            from .virtualserver.openstacksubclient import OpenStackVirtualServerSubclient
            return object.__new__(OpenStackVirtualServerSubclient)

        elif instance_name == hv_type.Rhev.value.lower():
            from .virtualserver.rhevsubclient import RhevVirtualServerSubclient
            return object.__new__(RhevVirtualServerSubclient)

        elif instance_name == hv_type.AMAZON_AWS.value.lower():
            from .virtualserver.amazonsubclient import AmazonVirtualServerSubclient
            return object.__new__(AmazonVirtualServerSubclient)

        elif instance_name == hv_type.VCLOUD.value.lower():
            from .virtualserver.vcloudsubclient import VcloudVirtualServerSubclient
            return object.__new__(VcloudVirtualServerSubclient)

        elif instance_name == hv_type.Nutanix.value.lower():
            from .virtualserver.nutanixsubclient import nutanixsubclient
            return object.__new__(nutanixsubclient)

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
            '17': 'Root',
            '34': 'Tag',
            '35': 'TagCategory'
        }

        self.filter_types = {
            '1': 'Datastore',
            '2': 'Virtual Disk Name/Pattern',
            '3': 'Virtual Device Node',
            '4': 'Repository'
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
        new_name = "new_name"

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
                if 'children' in child:
                    nested_children = child['children']
                    for each_condition in nested_children:
                        display_name = each_condition['displayName']
                        content_type = VSAObjects(each_condition['type'])
                        content_type = content_type.name
                        vm_id = each_condition['name']
                        temp_dict = {
                            'equal_value': each_condition['equalsOrNotEquals'],
                            'allOrAnyChildren': each_condition['allOrAnyChildren'],
                            'id': vm_id,
                            'path': path,
                            'display_name': display_name,
                            'type': content_type
                        }
                        content.append(temp_dict)

                else:
                    display_name = child['displayName']
                    content_type = VSAObjects(child['type'])
                    content_type = content_type.name
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
        return self._proxyClient['clientName']

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

                for child in children:
                    path = child['path'] if 'path' in child else None
                    display_name = child['displayName']
                    content_type = VSAObjects(child['type'])
                    content_type = content_type.name
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
                    filter_type_id = str(child['filterType'])
                    filter_type = self.filter_types[str(child['filterType'])]
                    vm_id = child['vmGuid'] if 'vmGuid' in child else None
                    filter_name = child['filter']

                    temp_dict = {
                        'filter': filter_name,
                        'filterType': filter_type,
                        'vmGuid': vm_id,
                        'filterTypeId': filter_type_id
                    }

                    vm_diskfilter.append(temp_dict)
        else:
            vm_diskfilter = self._vmDiskFilter

        if len(vm_diskfilter) == 0:
            vm_diskfilter = None
        return vm_diskfilter

    @property
    def cbtvalue(self):
        """
        Get CBT value for given subclient. Returns status as True/False (string)

        """
        self._get_subclient_properties()
        cbt_attr = r'useChangedTrackingOnVM'
        vsasubclient_cbt_status = self._vsaSubclientProp[cbt_attr]
        return vsasubclient_cbt_status

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
                temp = {
                    'allOrAnyChildren': item.get('allOrAnyChildren', True),
                    'equalsOrNotEquals': item.get('equalsOrNotEquals', True),
                    'name': item['name'],
                    'displayName': item['display_name'],
                    'path': '',
                    'type': item['type'].value
                }
                if item['type'] == VSAObjects.VMNotes:
                    temp['value'] = item['display_name']
                    temp['displayName'] = item['display_name']
                    temp['name'] = "Notes"
                if (item['type'] ==
                        VSAObjects.VMPowerState and
                        item['state'] == 'true'):
                    temp['name'] = "PoweredState"
                    temp['value'] = 1
                    temp['displayName'] = "Powered On"
                if (item['type'] ==
                        VSAObjects.VMPowerState and
                        item['state'] == 'false'):
                    temp['name'] = "PoweredState"
                    temp['value'] = 0
                    temp['displayName'] = "Powered Off"
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

    @cbtvalue.setter
    def cbtvalue(self, value=1):
        """
        Set given value (enabled/disabled) on the subclient

        Args:
                value   (int)   - enabled(1)/disabled(0)

        Raise Exception:
                If unable to set the give CBT value

        """
        try:
            cbt_status = bool(value)
            cbt_attr = r'useChangedTrackingOnVM'
            self._set_subclient_properties("_vsaSubclientProp['useChangedTrackingOnVM']",
                                           cbt_status)
        except:
            raise SDKException('Subclient', '101')

    @property
    def live_sync(self):
        """Returns the instance of the VSALiveSync class"""
        if not self._live_sync:
            from .virtualserver.livesync.vsa_live_sync import VsaLiveSync
            self._live_sync = VsaLiveSync(self)

        return self._live_sync

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

        if not new_name:
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

        if value.get('replication_guid'):
            self._virtualserver_option_restore_json['replicationGuid'] = value['replication_guid']

    def _json_nics_advancedRestoreOptions(self, vm_to_restore, value):
        """
            Setter for nics list for advanced restore option json
        """

        nics_dict_from_browse = self.get_nics_from_browse()
        nics_list = []
        vm_nics_list = nics_dict_from_browse[vm_to_restore]

        for network_card_dict in vm_nics_list:
            _destnetwork = value.get("destination_network", network_card_dict['name'])
            if value.get('network'):
                _destnetwork = value.get('network')
            nics = {
                "subnetId": network_card_dict.get('subnetId', ""),
                "sourceNetwork": network_card_dict['name'],
                "sourceNetworkId": "",
                "networkName": "",
                "destinationNetwork": _destnetwork
            }

            nics_list.append(nics)

        return nics_list

    def _json_vmip_advanced_restore_options(self, value):
        """
            Setting IP for destination vm
        """
        vmip = []
        vm_ip = {
            "sourceIP": value.get("source_ip"),
            "sourceSubnet": value.get("source_subnet", "*.*.*.*"),
            "sourceGateway": value.get("source_gateway", "*.*.*.*"),
            "destinationIP": value.get("destination_ip"),
            "destinationSubnet": value.get("destination_subnet", "*.*.*.*"),
            "destinationGateway": value.get("destination_subnet", "*.*.*.*"),
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

        self._json_disklevel_option_restore = {
            "esxServerName": value.get("esx_server_name", ""),
            "vmFolderName": value.get("vm_folder", ""),
            "dataCenterName": value.get("data_center", ""),
            "hostOrCluster": value.get("host_cluster", ""),
            "diskOption": value.get("disk_option", 0),
            "vmName": "",
            "transportMode": value.get("transport_mode", 0),
            "passUnconditionalOverride": value.get("unconditional_overwrite", False),
            "powerOnVmAfterRestore": value.get("power_on", False),
            "registerWithFailoverCluster": value.get("add_to_failover", False),
            "userPassword": {"userName": "admin"}
        }
        if value.get('in_place'):
            self._json_disklevel_option_restore["dataStore"] = {}
        if value.get('distribute_vm_workload'):
            self._json_disklevel_option_restore["maxNumOfVMPerJob"] = value['distribute_vm_workload']

    def _json_restore_advancedRestoreOptions(self, value):
        """setter for the Virtual server restore  option in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')


        self._advanced_option_restore_json = {
            "disks": value.get("disks", []),
            "guid": value.get("guid", ""),
            "newName": value.get("new_name", ""),
            "esxHost": value.get("esx_host", ""),
            "cluster": value.get("cluster", ""),
            "name": value.get("name", ""),
            "nics": value.get("nics", []),
            "vmIPAddressOptions": value.get("vm_ip_address_options", []),
            "FolderPath": value.get("FolderPath", ""),
            "ResourcePool": value.get("ResourcePool", "")
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
            self._advanced_option_restore_json["templateName"] = value["ami"]["templateName"]
        if "iamRole" in value and value["iamRole"] is not None:
            self._advanced_option_restore_json["roleInfo"] = {
                "name": value["iamRole"]
            }
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
            subnet = nic.get('subnet')
            networkDisplayName = nic.get('networkDisplayName', "")

            nic_info = {
                'name': name,
                'label': label,
                'subnetId': subnet,
                'networkDisplayName': networkDisplayName
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
                                                    default: True

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

        return self._process_vsa_browse_response(vm_ids, browse_content)

    def disk_level_browse(self, vm_path='\\',
                          show_deleted_files=True,
                          restore_index=True,
                          from_date=0,
                          to_date=0,
                          copy_precedence=0):
        """Browses the Disks of a Virtual Machine.

            Args:
                vm_path             (str)   --  vm path to get the contents of
                    default: '\\'; returns the root of the Backup content

                show_deleted_files  (bool)  --  include deleted files in the
                                                content or not default: True

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
                                                content or not default: True

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
        _source_path = r'\\'.join([_vm_id, _folder_to_restore])

        _browse_files, _browse_files_dict = self.guest_files_browse(
            _source_path, from_date=from_date, to_date=to_date,
            copy_precedence=copy_precedence, media_agent=media_agent)

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
                           copy_precedence=0,
                           preserve_level=1,
                           unconditional_overwrite=False,
                           v2_indexing=False,
                           restore_ACL=True,
                           from_date=0,
                           to_date=0,
                           show_deleted_files=True,
                           fbr_ma=None,
                           browse_ma=""):
        """perform Guest file restore of the provided path

        Args:
            vm_name             (basestring)   --  VM from which files needs to be
                                            restored

            folder_to_restore    (basestring)  -- folder path to restore

            show_deleted_files  (bool)  --  include deleted files in the
                                            content or not
                                            default: True


            destination_path    (basestring)   --  path to restore

            copy_precedence     (int)   --  copy precedence to be used
                                                    for browsing

            from_date           (int)   --  date to get the contents after
                                            format: dd/MM/YYYY
                                            gets contents from 01/01/1970 if
                                            not specified default: 0

            to_date             (int)   --  date to get the contents before
                                            format: dd/MM/YYYY
                                            gets contents till current day
                                            if not specified default: 0

            fbr_ma              (basestring)    --  FRE MA used for browsing Unix VMs

            browse_ma            (basestring)    --  MA for browsing

            v2_indexing           (bool)         -- Restore is from child level or not

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
               (isinstance(vm_name, basestring))):
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

        elif isinstance(folder_to_restore, basestring):
            _folder_to_restore_list = []
            _folder_to_restore_list.append(folder_to_restore)
        else:
            raise SDKException('Subclient', '105')

        _file_restore_option["paths"] = []
        for _each_folder in _folder_to_restore_list:
            _file_restore_option["paths"].append(
                self._check_folder_in_browse(_vm_ids[vm_name],
                                             "%s" % _each_folder,
                                             from_date,
                                             to_date,
                                             copy_precedence,
                                             media_agent=browse_ma))

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
        _file_restore_option["copy_precedence"] = copy_precedence
        _file_restore_option["media_agent"] = browse_ma

        # prepare and execute the Json
        request_json = self._prepare_filelevel_restore_json(_file_restore_option)

        if v2_indexing:

            _vmclient_obj = self._commcell_object.clients.get(vm_name)
            _vmagent_obj = _vmclient_obj.agents.get(self._agent_object._agent_name)
            _vminstance_obj = _vmagent_obj.instances.get('VMInstance')
            _vmbackupset_obj = _vminstance_obj.backupsets.get(
                self._backupset_object._backupset_name)
            _vmsub_obj = _vmbackupset_obj.subclients.get('default')

            request_json['taskInfo']['associations'][0]['clientName'] = vm_name
            request_json['taskInfo']['associations'][0]['clientId'] = \
                _vmsub_obj._subClientEntity['clientId']
            request_json['taskInfo']['associations'][0]['instanceName'] = 'VMInstance'
            request_json['taskInfo']['associations'][0]['backupsetId'] = \
                _vmsub_obj._subClientEntity['backupsetId']
            request_json['taskInfo']['associations'][0]['instanceId'] = \
                _vmsub_obj._subClientEntity['instanceId']
            request_json['taskInfo']['associations'][0]['subclientGUID'] = \
                subclientGUID = _vmsub_obj._subClientEntity['subclientGUID']
            request_json['taskInfo']['associations'][0]['subclientName'] = 'default'
            request_json['taskInfo']['associations'][0]['subclientId'] = \
                _vmsub_obj._subClientEntity['subclientId']

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
            from_date=0,
            to_date=0):
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
        get the list of all the proxies on a selected subclient

        Returns:
            associated_proxies   (LIST)  --  returns the proxies list
        """
        associated_proxies = []
        try:
            available_subclient_proxies = self._vsaSubclientProp["proxies"]["memberServers"]
            if len(available_subclient_proxies) > 0:
                for proxy in available_subclient_proxies:
                    associated_proxies.append(proxy["client"]["clientName"])
        except KeyError:
            pass
        return associated_proxies

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
        browse_result = self.vm_files_browse()

        # vs metadata from browse result
        _metadata = browse_result[1][('\\' + vm_to_restore)]
        vs_metadata = _metadata["advanced_data"]["browseMetaData"]["virtualServerMetaData"]
        if restore_option['in_place']:
            folder_path = vs_metadata.get("inventoryPath", '')
            instanceSize = vs_metadata.get("instanceSize", '')
        else:
            folder_path = ''
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
            "\\\\" + vm_ids[vm_to_restore])

        for disk, data in disk_info_dict.items():
            ds = ""
            if "datastore" in restore_option:
                ds = restore_option["datastore"]
            if ((restore_option["in_place"]) or ("datastore" not in restore_option)):
                if "datastore" in data["advanced_data"]["browseMetaData"][
                    "virtualServerMetaData"]:
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
            _disk_dict = self._disk_dict_pattern(disk.split('\\')[-1], ds, new_name)
            if 'is_aws_proxy' in restore_option and not restore_option['is_aws_proxy']:
                _disk_dict['Datastore'] = restore_option["datastore"]
            vm_disks.append(_disk_dict)
        if not vm_disks:
            raise SDKException('Subclient', '104')
        restore_option["disks"] = vm_disks

        # prepare nics info json
        if "nics" not in restore_option:
            nics_list = self._json_nics_advancedRestoreOptions(vm_to_restore, restore_option)
            restore_option["nics"] = nics_list
            if "source_ip" in restore_option and "destination_ip" in restore_option:
                if restore_option["source_ip"] and restore_option["destination_ip"]:
                    vm_ip = self._json_vmip_advanced_restore_options(restore_option)
                    restore_option["vm_ip_address_options"] = vm_ip
            if restore_option["in_place"]:
                if "hyper" in restore_option["destination_instance"]:
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
            esx_host=restore_option.get('esx_host',vs_metadata['esxHost']),
            instanceSize=restore_option.get('instanceSize', instanceSize),
            new_name="Delete" + vm_to_restore
        )

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
        match1 = re.search('secGroupId=\"(\S*)\"', xml_str)
        match2 = re.search('secGroupName=\"(\S*)\"', xml_str)
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
        match1 = re.search('keyPairId=\"(\S*)\"', xml_str)
        match2 = re.search('keyPairName=\"(\S*)\"', xml_str)
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
        self._json_restore_volumeRstOption(restore_option)
        self._json_vcenter_instance(restore_option)

        for _each_vm_to_restore in restore_option['vm_to_restore']:
            if not restore_option["in_place"]:
                if ("restore_new_name" in restore_option and
                        restore_option["restore_new_name"] is not None):
                    restore_option["new_name"] = restore_option["restore_new_name"]
                else:
                    restore_option["new_name"] = "Delete" + _each_vm_to_restore
            else:
                restore_option["new_name"] = _each_vm_to_restore
            self.set_advanced_vm_restore_options(_each_vm_to_restore, restore_option)

        # prepare json
        request_json = self._restore_json(restore_option=restore_option)
        _virt_restore_json = self._virtualserver_option_restore_json
        _virt_restore_json["diskLevelVMRestoreOption"] = self._json_disklevel_option_restore
        _virt_restore_json["vCenterInstance"] = self._vcenter_instance_json
        _virt_restore_json["diskLevelVMRestoreOption"][
            "advancedRestoreOptions"] = self._advanced_restore_option_list
        self._advanced_restore_option_list = []
        request_json["taskInfo"]["subTasks"][0][
            "options"]["restoreOptions"]["virtualServerRstOption"] = _virt_restore_json

        request_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["volumeRstOption"] = self._volume_restore_json

        return request_json

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH',
               collect_metadata=False,
               advanced_options=None):
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

                advacnced_options       (dict)  --  advanced backup options to be included while
                                                    making the request
                    options:
                        create_backup_copy_immediately  --  Run Backup copy just after snap backup
                        backup_copy_type                --  Backup Copy level using storage policy
                                                            or subclient rule
            Returns:
                object : instance of the Job class for this backup job

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

        if advanced_options:
            request_json = self._backup_json(backup_level, incremental_backup, incremental_level,
                                             advanced_options)

            backup_service = self._commcell_object._services['CREATE_TASK']

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', backup_service, request_json
            )

        else:
            return super(VirtualServerSubclient, self).backup(backup_level=backup_level,
                                                              incremental_backup=incremental_backup,
                                                              incremental_level=incremental_level,
                                                              collect_metadata=collect_metadata)

        return self._process_backup_response(flag, response)

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
