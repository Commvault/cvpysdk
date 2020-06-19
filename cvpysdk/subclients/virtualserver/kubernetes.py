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

"""File for operating on a Virtual Server Kubernetes Subclient.

KubernetesVirtualServerSubclient is the only class defined in this file.

Class: KubernetesVirtualServerSubclient:    Derived class from VirtualServerSubClient Base
                                            class,representing a Kubernetes Subclient,
                                            and to perform operations on that Subclient

    KubernetesVirtualServerSubclient:

        __init__(
            backupset_object,
            subclient_name,
            subclient_id)           --  initialize object of Kubernetes subclient class,
                                        associated with the VirtualServer subclient

        full_vm_restore_in_place()  --  restores the pod specified by the user to
                                        the same location

        full_vm_restore_out_of_place() -- restores the pod specified to the provided
                                          Kubernetes psuedoclient

        _prepare_kubernetes_restore_json() -- Restore json prep method for kubernetes

        _json_restore_volumeRstOption()  -- Restores json for volumeRstOptions

        set_advanced_vm_restore_options() -- Advanced VM restore options

        _json_restore_virtualServerRstOption() -- json for VirtualServerRst options for Kubernetes.


Class: ApplicationGroups:                Derived class from Subclients Base
                                            class,representing a Kubernetes ApplicationGroups,
                                            and to perform operations on that ApplicationGroups

    ApplicationGroups:

        __init__(class_object)           --  initialize object of Kubernetes subclient class,
                                            associated with the VirtualServer subclient

        create_application_group()       --       creates application group


"""

from cvpysdk.subclients.vssubclient import VirtualServerSubclient
from cvpysdk.virtualmachinepolicies import VirtualMachinePolicy
from past.builtins import basestring
from ...exception import SDKException
from ...subclient import Subclients


class KubernetesVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a VMWare virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        super(KubernetesVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.disk_extension = [".vmdk"]

        self._disk_option = {
            'Original': 0,
            'Thick Lazy Zero': 1,
            'Thin': 2,
            'Thick Eager Zero': 3
        }

        self._transport_mode = {
            'Auto': 0,
            'SAN': 1,
            'Hot Add': 2,
            'NBD': 5,
            'NBD SSL': 4
        }

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore,
            restored_vm_name=None,
            vcenter_client=None,
            esx_host=None,
            datastore=None,
            datacenter=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            transport_mode='Auto',
            proxy_client=None,
            source_ip=None,
            destination_ip=None,
            network=None
    ):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore            (str)    --  VM that is to be restored

                restored_vm_name         (str)    --  new name of vm. If nothing is passed,
                                                      'delete' is appended to the original vm name

                vcenter_client           (str)    --  name of the vcenter client where the VM
                                                      should be restored.

                esx_host                (str)    --  destination esx host. Restores to the source
                                                      VM esx if this value is not specified

                datastore               (str)    --  datastore where the restored VM should be
                                                      located. Restores to the source VM datastore
                                                      if this value is not specified

                overwrite               (bool)    --  overwrite the existing VM
                                                      default: True

                power_on                (bool)    --  power on the  restored VM
                                                      default: True

                copy_precedence          (int)    --  copy precedence value
                                                      default: 0

                disk_option              (str)    --  disk provisioning for the  restored vm
                                                      Options for input are: 'Original',
                                                      'Thick Lazy Zero', 'Thin', 'Thick Eager Zero'
                                                      default: 'Original'

                transport_mode            (str)    --  transport mode to be used for the restore.
                                                      Options for input are: 'Auto', 'SAN',
                                                      'Hot Add', 'NBD', 'NBD SSL'
                                                      default: Auto

                proxy_client              (str)    --  destination proxy client

                source_ip                 (str)    --  IP of the source VM

                destination_ip            (str)    --  IP of the destination VM

                network                   (str)    --  Network of the detination vm

            Returns:
                object - instance of the Job class for this restore job


            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        restore_option = {}

        # check mandatory input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, basestring):
            raise SDKException('Subclient', '101')

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client'] = proxy_client

        if restored_vm_name:
            if not(isinstance(vm_to_restore, basestring) or
                   isinstance(restored_vm_name, basestring)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_vm_name

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        restore_option_copy = restore_option.copy()

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=vcenter_client,
            datastore=datastore,
            esx_host=esx_host,
            datacenter=datacenter,
            esx_server=None,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            disk_option=self._disk_option[disk_option],
            transport_mode=self._transport_mode[transport_mode],
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            source_item=[],
            source_ip=source_ip,
            destination_ip=destination_ip,
            network=network
        )

        request_json = self._prepare_kubernetes_restore_json(restore_option)
        return self._process_restore_response(request_json)


    def _prepare_kubernetes_restore_json(self, restore_option):
        """
        Prepare Full VM restore Json with all getters

        Args:
            restore_option - dictionary with all VM restore options

        value:
            restore_option:

                preserve_level           (bool)   - set the preserve level in restore

                unconditional_overwrite  (bool)  - unconditionally overwrite the disk
                                                    in the restore path

                destination_path          (str)- path where the disk needs to be
                                                 restored

                client_name               (str)  - client where the disk needs to be
                                                   restored

                destination_vendor         (str) - vendor id of the Hypervisor

                destination_disktype       (str) - type of disk needs to be restored
                                                   like VHDX,VHD,VMDK

                source_item                 (str)- GUID of VM from which disk needs to
                                                   be restored
                                                   eg:
                                                   \\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

                copy_precedence_applicable  (bool)- True if needs copy_precedence to
                                                    be honoured else False

                copy_precedence            (int) - the copy id from which browse and
                                                   restore needs to be performed

                power_on                    (bool) - power on the VM after restore

                add_to_failover             (bool) - Register the VM to Failover Cluster

                datastore                   (str) - Datastore where the VM needs to be
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
                guid                    (str)    - GUID of the VM needs to be restored
                new_name                (str)    - New name for the VM to be restored
                esx_host                (str)    - esx_host or client name where it need
                                                     to be restored
                name                    (str)    - name of the VM to be restored

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

        return request_json

    def _json_restore_volumeRstOption(self, value):
        """setter for  the Volume restore option for in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        return{
            "volumeLeveRestore": False,
            "volumeLevelRestoreType": value.get("volume_level_restore", 0)
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
            "isBlockLevelReplication": value.get("block_level", False),
            "datacenter": value.get("datacenter", "")
        }

        if value.get('replication_guid'):
            self._virtualserver_option_restore_json['replicationGuid'] = value['replication_guid']

    def set_advanced_vm_restore_options(self, vm_to_restore, restore_option):
        """
        set the advanced restore options for all vm in restore
        param

            vm_to_restore               - Name of the VM to restore

            restore_option              - restore options that need to be set for advanced restore option

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
            instance_size = vs_metadata.get("instanceSize", '')
        else:
            folder_path = ''
            instance_size = ''
        if restore_option.get('resourcePoolPath'):
            restore_option['resourcePoolPath'] = vs_metadata['resourcePoolPath']
        if restore_option.get('datacenter'):
            restore_option['datacenter'] = restore_option.get('datacenter')
        if restore_option.get('terminationProtected'):
            restore_option['terminationProtected'] = vs_metadata.get('terminationProtected', '')
        if restore_option.get('iamRole'):
            restore_option['iamRole'] = vs_metadata.get('role', '')
        if restore_option.get('securityGroups'):
            _security_groups = self._find_security_groups(vs_metadata['networkSecurityGroups'])
            restore_option['securityGroups'] = _security_groups
        if restore_option.get('keyPairList'):
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

        if "datastore" in restore_option:
            ds = restore_option["datastore"]
        new_name = vm_to_restore
        diskpattern = "automation`Deployment`{0}.yaml".format(vm_to_restore)
        _disk_dict = self._disk_dict_pattern(diskpattern, ds, new_name)
        if 'is_aws_proxy' in restore_option and not restore_option['is_aws_proxy']:
            _disk_dict['Datastore'] = restore_option["datastore"]
        vm_disks.append(_disk_dict)
        if not vm_disks:
            raise SDKException('Subclient', '104')
        restore_option["disks"] = vm_disks

        self._set_restore_inputs(
            restore_option,
            disks=vm_disks,
            esx_host=restore_option.get('esx_host') or vs_metadata['esxHost'],
            instance_size=restore_option.get('instanceSize', instance_size),
            new_name=restore_option.get('new_name', "Delete" + vm_to_restore)
        )

        temp_dict = self._json_restore_advancedRestoreOptions(restore_option)
        self._advanced_restore_option_list.append(temp_dict)

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            transport_mode='Auto',
            proxy_client=None):
        """Restores the FULL Virtual machine specified in the input list
            to the location same as the actual location of the VM in VCenter.

            Args:
                vm_to_restore         (list)        --  provide the VM name to restore
                                                        default: None

                overwrite             (bool)        --  overwrite the existing VM
                                                        default: True

                power_on              (bool)        --  power on the  restored VM
                                                        default: True

                copy_precedence       (int)         --  copy precedence value
                                                        default: 0

                disk_option           (basestring)  --  disk provisioning for the restored vm
                                                        Options for input are: 'Original',
                                                        'Thick Lazy Zero', 'Thin',
                                                        'Thick Eager Zero'
                                                        default: Original

                transport_mode        (basestring)  --  transport mode to be used for
                                                        the restore.
                                                        Options for input are: 'Auto', 'SAN',
                                                        ''Hot Add', NBD', 'NBD SSL'
                                                        default: Auto

                proxy_client          (basestring)  --  proxy client to be used for restore
                                                        default: proxy added in subclient


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        restore_option = {}
        # check input parameters are correct
        if vm_to_restore and not isinstance(vm_to_restore, basestring):
            raise SDKException('Subclient', '101')
        disk_option_value = self._disk_option[disk_option]
        transport_mode_value = self._transport_mode[transport_mode]
        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        if proxy_client is not None:
            restore_option['client'] = proxy_client

        restore_option_copy = restore_option.copy()

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            in_place=True,
            esx_server_name="",
            volume_level_restore=1,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            disk_option=disk_option_value,
            transport_mode=transport_mode_value,
            copy_precedence=copy_precedence
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)


class ApplicationGroups(Subclients):

    ''' Class to create Kubernetes Application groups
        Derived from Subclients class
    Args:
        class_object  of Backupset class
     '''

    def __init__(self, class_object):

        super(ApplicationGroups, self).__init__(class_object)

    def create_application_group(self,
                                 content,
                                 plan_name,
                                 subclient_name="automation"):

        """Create application / Kubernetes Subclient.

            Args:
                client_id               (str)    --  Client id

                content                 (str)    --  Subclient content

                plan_name                 (str)    --  Plan name

                subclient_name          (str)    --  Subclient name you want to create Subclient

        """
        flag, get_pods = self._cvpysdk_object.make_request('GET', self._services['GET_VM_BROWSE']
                                                           % (int(self._client_object.client_id)))
        temp_str = get_pods.content.decode("utf-8")
        list_temp = temp_str.split(',')
        plan_id = ''
        mylist = []
        for element in list_temp:
            if content in element:
                list_strguid = element.split(':')
                mylist.append((list_strguid[1]).replace('"', ''))

        plan_id = int(self._commcell_object.plans[str(plan_name.lower())])

        app_create_json = {
            "subClientProperties": {
                "vmContentOperationType": 2,
                "vmContent": {
                    "children": [
                        {
                            "equalsOrNotEquals": True,
                            "displayName": mylist[0],
                            "allOrAnyChildren": True,
                            "type": 5,
                            "name": mylist[1]
                        }
                    ]
                },
                "subClientEntity": {
                    "clientId": int(self._client_object.client_id),
                    "appName": "Virtual Server",
                    "applicationId": 106,
                    "subclientName": subclient_name
                },
                "planEntity": {
                    "planId": int(plan_id)
                },
                "commonProperties": {
                    "enableBackup": True,
                    "numberOfBackupStreams": 5,
                    "isSnapbackupEnabled": True,
                    "snapCopyInfo": {
                        "transportModeForVMWare": 0,
                        "isSnapBackupEnabled": False
                    }
                },
                "vsaSubclientProp": {
                    "autoDetectVMOwner": False,
                    "quiesceGuestFileSystemAndApplications": True
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST', self._services['ADD_SUBCLIENT'],
                                                           app_create_json)
        if flag == False:
            raise SDKException('Response', '101', self._update_response_(response.text))

