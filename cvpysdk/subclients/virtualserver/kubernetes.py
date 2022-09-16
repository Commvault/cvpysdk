﻿# -*- coding: utf-8 -*-

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

KubernetesVirtualServerSubclient and ApplicationGroups are the only class defined in this file.

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

        disk_restore()                  --  Function to restore disk.

        enable_intelli_snap()           --  Enables Intellisnap on subclient

        guest_file_restore()            --  Restore the files and folders to file system destionation
                                            or to target PVC

        guest_files_browse()            --  Browse files in a application at any point in time

        namespace_restore_in_place()    --  Perform a namespace level restore in-place

        namespace_restore_out_of_place()--  Perform a namespace level restore out-of-place


Class: ApplicationGroups:                Derived class from Subclients Base
                                            class,representing a Kubernetes ApplicationGroups,
                                            and to perform operations on that ApplicationGroups

    ApplicationGroups:

        __init__(class_object)           --  initialize object of Kubernetes subclient class,
                                            associated with the VirtualServer subclient

        browse()                         -- Browse cluster for namespace, applications, volumes, or labels

        get_children_node()              -- Construct the json object for content and filter

        create_application_group()       --       creates application group


"""

import copy
from cvpysdk.subclients.vssubclient import VirtualServerSubclient
from cvpysdk.virtualmachinepolicies import VirtualMachinePolicy
from ...exception import SDKException
from ...subclient import Subclients


class KubernetesVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a Kubernetes virtual server subclient,
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
        self.diskExtension = [".yaml"]

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

    def full_app_restore_out_of_place(
            self,
            apps_to_restore,
            restore_namespace,
            restored_app_name=None,
            kubernetes_client=None,
            storage_class=None,
            overwrite=True,
            copy_precedence=0,
            proxy_client=None,
    ):
        """Restores the FULL Application specified in the input list
            to the provided Kubernetes client at the specified namespace with storage class.
            If the provided client name is none then it restores the Full Application
            to the source Kubernetes client and corresponding namespace and storage class.

            Args:
                apps_to_restore         (list)  --  List of Applications that is to be restored

                restored_app_name       (dict)  --  Dictionary mapping new name of Applications

                kubernetes_client       (str)   --  Name of the Kubernetes client where the Application should be restored
                                                    Restores to the source Kubernetes client if this value is not specified

                storage_class           (str)   --  Storage class for the PVC to be restored with.
                                                    Uses source storage class if not specified.

                restore_namespace       (str)   --  Target namespace where Applications are to be restored

                overwrite               (bool)  --  overwrite the existing Applications if exists
                                                    default: True

                copy_precedence          (int)  --  copy precedence value
                                                      default: 0

                proxy_client              (str)    --  destination proxy client

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
        if apps_to_restore and not isinstance(apps_to_restore, list):
            raise SDKException('Subclient', '101')

        # populating proxy client. It assumes the proxy controller added in instance
        # properties if not specified
        if proxy_client is not None:
            restore_option['client'] = proxy_client

        if restored_app_name:
            if not(isinstance(apps_to_restore, list) or
                   isinstance(restored_app_name, dict)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_app_name

        if not kubernetes_client:
            kubernetes_client = self._client_object.client_name

        restore_option_copy = restore_option.copy()

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=kubernetes_client,
            datastore=storage_class,
            esx_host=kubernetes_client,
            datacenter=restore_namespace,
            unconditional_overwrite=overwrite,
            vm_to_restore=self._set_vm_to_restore(apps_to_restore),
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            source_item=[]
        )

        request_json = self._prepare_kubernetes_restore_json(restore_option)
        return self._process_restore_response(request_json)


    def _prepare_kubernetes_restore_json(self, restore_option):
        """
        Prepare Full Application restore Json with all getters

        Args:
            restore_option - dictionary with all Application restore options

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

                source_item                 (str)- GUID of Application from which disk needs to
                                                   be restored
                                                   eg:
                                                   \\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

                copy_precedence_applicable  (bool)- True if needs copy_precedence to
                                                    be honoured else False

                copy_precedence            (int) - the copy id from which browse and
                                                   restore needs to be performed

                datastore                   (str) - Storage class which the Application PVC needs to be
                                                    restored with

                disks   (list of dict)      - list with dict for each disk in Application
                                                eg: [{
                                                        name:"pvc-1"
                                                        datastore:"storageclass-1"
                                                    }
                                                    {
                                                        name:"pvc-2"
                                                        datastore:"storageclass-2"
                                                    }
                                                ]
                guid                    (str)    - GUID of the Application needs to be restored

                new_name                (str)    - New name for the Application to be restored

                esx_host                (str)    - client name where Application need to be restored

                name                    (str)    - name of the Application to be restored

        returns:
              request_json        -complete json for perfomring Full Application Restore
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

        _new_name_dict = restore_option.get('restore_new_name', {})
        for _each_vm_to_restore in restore_option['vm_to_restore']:
            restore_option["new_name"] = _new_name_dict.get(_each_vm_to_restore, _each_vm_to_restore)
            namespace_app_map = restore_option.get('namespace_app_map', {})
            datacenter = restore_option.get('datacenter', None)

            if not namespace_app_map:
                # FOR : Full Application Restores Restores
                # If namespace_app_map is not passed the it is a full application restore
                # so 'datacenter' should be passed. Nothing to do here
                pass

            elif _each_vm_to_restore in namespace_app_map:
                # FOR : Namespace Level Restore
                # If _each_vm_to_restore is in namespace_app_map which means it's an application
                # and not a namespace, so we need to pass 'datacenter' to advanced restore options

                app_ns = namespace_app_map.get(_each_vm_to_restore)

                # Getting the target namespace if restoring to a new namespace name
                target_ns = _new_name_dict[app_ns]
                restore_option['datacenter'] = target_ns
            else:
                # FOR : Namespace Level Restore
                # If it's a namespace, then there is no 'datacenter' needed so pop it
                if 'datacenter' in restore_option:
                    restore_option.pop('datacenter')
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
            "endUserVMRestore": value.get("end_user_vm_restore", False)     # Required by Kubernetes Disk Level Restore
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

        if "datacenter" in value:   # Required for Kubernetes Disk Level Restore
            self._advanced_option_restore_json['datacenter'] = value["datacenter"]

        if value.get('block_level'):
            self._advanced_option_restore_json["blrRecoveryOpts"] = \
                self._json_restore_blrRecoveryOpts(value)

        temp_dict = copy.deepcopy(self._advanced_option_restore_json)
        return temp_dict

    def _get_app_pvc(self, application_id):
        """Get the dictionary of PVCs in the applications with storage class info

            Args:

                application_id      (str)       --  Application GUID to get PVC

            Returns:

                List of dicts with PVC information
        """
        app_disks, disk_metadata = self.browse('\\' + application_id)
        pvc_path_list = [disk for disk in app_disks if disk.split('.')[-1] != 'yaml']

        pvc_list = []

        for pvc in pvc_path_list:
            temp_dict = {}
            pvc_metadata = disk_metadata[pvc]
            vs_metadata = pvc_metadata['advanced_data']['browseMetaData']['virtualServerMetaData']
            temp_dict['name'] = pvc_metadata['name']
            temp_dict['storageclass'] = vs_metadata['datastore']
            pvc_list.append(temp_dict)

        return pvc_list

    def set_advanced_vm_restore_options(self, vm_to_restore, restore_option):
        """
        set the advanced restore options for all vm in restore
        param

            vm_to_restore               - Name of the Application to restore

            restore_option              - restore options that need to be set for advanced restore option

            power_on                    - power on the Application after restore

            add_to_failover             - Register the Application to Failover Cluster

            datastore                   - Datastore where the Application needs to be restored

            disks   (list of dict)      - list with dict for each disk in Application
                                            eg: [{
                                                        name:"pvc-1"
                                                        datastore:"storageclass-1"
                                                    }
                                                    {
                                                        name:"pvc-2"
                                                        datastore:"storageclass-2"
                                                    }
                                                ]
            guid                        - GUID of the Application needs to be restored

            new_name                    - New name for the Application to be restored

            esx_host                    - client name where it need to be restored

            name                        - name of the Application to be restored

        """

        # Set the new name for the restored Application.
        # If new_name is not given, it restores the Application with same name
        # with suffix Delete.
        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        browse_result = self.vm_files_browse()
        application_id = vm_ids[vm_to_restore]

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
        restore_option['paths'].append("\\" + application_id)
        restore_option['name'] = vm_to_restore
        restore_option['guid'] = application_id
        restore_option["FolderPath"] = folder_path
        restore_option["ResourcePool"] = "/"

        # populate restore disk and datastore
        vm_disks = []
        new_name = vm_to_restore

        storage_class_map = restore_option.get('storage_class_map', None)

        # To populate disk list for each app in case of namespace restore
        if storage_class_map:
            pvc_list = self._get_app_pvc(application_id)
            for pvc in pvc_list:
                storageclass_name = pvc['storageclass']
                pvc_name = pvc['name']

                # If 'datastore' is passed then it's full app restore, else
                # it is namespace level restore.
                # Namespace level restore can be passed with storage class mapping
                if storageclass_name in storage_class_map:
                    storageclass_name = storage_class_map[storageclass_name]
                _disk_dict = self._disk_dict_pattern(pvc_name, storageclass_name, pvc_name)
                vm_disks.append(_disk_dict)

        restore_option["disks"] = vm_disks

        self._set_restore_inputs(
            restore_option,
            esx_host=restore_option.get('esx_host') or vs_metadata['esxHost'],
            instance_size=restore_option.get('instanceSize', instance_size),
            new_name=restore_option.get('new_name', "Delete" + vm_to_restore)
        )

        temp_dict = self._json_restore_advancedRestoreOptions(restore_option)
        self._advanced_restore_option_list.append(temp_dict)

    def full_app_restore_in_place(
            self,
            apps_to_restore=None,
            overwrite=True,
            copy_precedence=0,
            proxy_client=None):
        """Restores the FULL Application specified in the input list
            to the location same as the actual location of the Application in Kubernetes cluster.

            Args:
                apps_to_restore     (list)      --  List of applications to restore

                overwrite           (bool)      --  overwrite the existing Applications if exists
                                                    default: True

                copy_precedence     (int)       --  copy precedence value
                                                    default: 0

                proxy_client        (str)       --  proxy client to be used for restore
                                                    default: proxy added in application group/cluster

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
        if apps_to_restore and not isinstance(apps_to_restore, list):
            raise SDKException('Subclient', '101')
        if copy_precedence:
            restore_option['copy_precedence_applicable'] = True

        if proxy_client is not None:
            restore_option['client'] = proxy_client

        kubernetes_host = self._client_object.client_name

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(apps_to_restore),
            in_place=True,
            esx_host=kubernetes_host,
            volume_level_restore=1,
            unconditional_overwrite=overwrite,
            copy_precedence=copy_precedence
        )

        request_json = self._prepare_kubernetes_inplace_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def _prepare_kubernetes_inplace_restore_json(self, restore_option):
        """
        Prepare Full Application restore in-place Json with all getters

        Args:
            restore_option - dictionary with all Application restore options

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

                source_item                 (str)- GUID of Application from which disk needs to
                                                   be restored
                                                   eg:
                                                   \\5F9FA60C-0A89-4BD9-9D02-C5ACB42745EA

                copy_precedence_applicable  (bool)- True if needs copy_precedence to
                                                    be honoured else False

                copy_precedence            (int) - the copy id from which browse and
                                                   restore needs to be performed

                datastore                   (str) - Storage class which the Application PVC needs to be
                                                    restored with

                disks   (list of dict)      - list with dict for each disk in Application
                                                eg: [{
                                                        name:"pvc-1"
                                                        datastore:"storageclass-1"
                                                    }
                                                    {
                                                        name:"pvc-2"
                                                        datastore:"storageclass-2"
                                                    }
                                                ]
                guid                    (str)    - GUID of the Application needs to be restored

                new_name                (str)    - New name for the Application to be restored

                esx_host                (str)    - client name where Application need to be restored

                name                    (str)    - name of the Application to be restored

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

        if restore_option.get('copy_precedence'):
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
                if 'disk_type' in restore_option:
                    restore_option['restoreAsManagedVM'] = restore_option['disk_type'][_each_vm_to_restore]
                if ("restore_new_name" in restore_option and
                        restore_option["restore_new_name"] is not None):
                    restore_option["new_name"] = restore_option["restore_new_name"] + _each_vm_to_restore
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
        return request_json

    def disk_restore(self,
                     application_name,
                     destination_path,
                     disk_name=None,
                     proxy_client=None,
                     **kwargs):
        """Restores the disk specified in the input paths list to the same location

            Args:
                application_name             (str)    --  Name of the Application added in subclient content
                                                        whose  disk is selected for restore

                destination_path        (str)    --  Staging (destination) path to restore the
                                                        disk.

                disk_name                 (list)    --  name of the disk which has to be restored
                                                        (only yaml files permitted - enter full
                                                        name of the disk)
                                                        default: None
                proxy_client        (str)    --  Destination proxy client to be used
                                                        default: None

            Kwargs:

                Allows parameters to modify disk restore --

                copy_precedence            (int)    --  SP copy precedence from which browse has to

                media_agent         (str)   -- MA needs to use for disk browse
                    default :Storage policy MA

                snap_proxy          (str)   -- proxy need to be used for disk
                                                    restores from snap
                    default :proxy in instance or subclient

                disk_extension      (str)   -- Extension of disk file (Default: '.yaml')

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not passed in proper expected format

                    if response is empty

                    if response is not success
        """

        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _disk_restore_option = {}

        copy_precedence = kwargs.get("copy_precedence", 0)
        disk_extn = kwargs.get("disk_extension", '.yaml')
        unconditional_overwrite = kwargs.get('unconditional_overwrite', False)
        show_deleted_files = kwargs.get('show_deleted_files', False)

        # Volume level restore values -
        # 4 - Manifest Restore
        volume_level_restore = kwargs.get("volume_level_restore", 4)

        if not disk_name:
            disk_name = []
        else:
            disk_extn = self._get_disk_extension(disk_name)

        # check if inputs are correct
        if not (isinstance(application_name, str) and
                isinstance(destination_path, str) and
                isinstance(disk_name, list)):
            raise SDKException('Subclient', '101')

        if copy_precedence:
            _disk_restore_option['copy_precedence_applicable'] = True

        # fetching all disks from the vm
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + vm_ids[application_name])

        # Filter out disks with specified extension from disk list
        disk_list = list(filter(lambda name: self._get_disk_extension([name]) == disk_extn, disk_list))
        disk_info_dict = { disk : disk_info_dict[disk] for disk in disk_list }

        if not disk_name:  # if disk names are not provided, restore all disks
            for each_disk_path in disk_list:
                disk_name.append(each_disk_path.split('\\')[-1])

        else:  # else, check if the given application has a disk with the list of disks in disk_name.
            for each_disk in disk_name:
                # disk path has GUID in case of files, and application name in case of manifests
                each_disk_path = "\\" + \
                                 (vm_ids[application_name] if volume_level_restore != 4 else application_name) + \
                                 "\\" + each_disk.split("\\")[-1]
                if each_disk_path not in disk_list:
                    raise SDKException('Subclient', '111')

        _disk_restore_option["destination_vendor"] = \
            self._backupset_object._instance_object._vendor_id

        if proxy_client is not None:
            _disk_restore_option['client'] = proxy_client
        else:
            _disk_restore_option['client'] = self._backupset_object._instance_object.co_ordinator

        # set Source item List
        src_item_list = []
        for each_disk in disk_name:
            src_item_list.append("\\" + vm_ids[application_name] + "\\" + each_disk.split("\\")[-1])

        _disk_restore_option['paths'] = src_item_list
        _disk_restore_option['unconditional_overwrite'] = unconditional_overwrite
        _disk_restore_option['show_deleted_files'] = show_deleted_files

        # Populate volume level restore options
        _disk_restore_option['volume_level_restore'] = volume_level_restore

        self._set_restore_inputs(
            _disk_restore_option,
            in_place=False,
            copy_precedence=copy_precedence,
            destination_path=destination_path,
            paths=src_item_list
        )

        request_json = self._prepare_disk_restore_json(_disk_restore_option)
        return self._process_restore_response(request_json)

    def enable_intelli_snap(self, snap_engine_name=None, proxy_options=None, snapshot_engine_id =None):
        """Enables Intelli Snap for the subclient.

            Args:
                snap_engine_name    (str)   --  Snap Engine Name

                proxy_options       (str)    -- to set proxy for Kubernetes

                snapshot_engine_id   (int)   -- Snapshot engine id

            Raises:
                SDKException:
                    if failed to enable intelli snap for subclient
        """
        if snapshot_engine_id is None:
            snapshot_engine_id = 82

        properties_dict = {
            "isSnapBackupEnabled": True,
            "snapToTapeSelectedEngine": {
                "snapShotEngineId": snapshot_engine_id,
                "snapShotEngineName": snap_engine_name
            }
        }
        if proxy_options is not None:
            if "snap_proxy" in proxy_options:
                properties_dict["snapToTapeProxyToUse"] = {
                    "clientName": proxy_options["snap_proxy"]
                }

            if "backupcopy_proxy" in proxy_options:
                properties_dict["useSeparateProxyForSnapToTape"] = True
                properties_dict["separateProxyForSnapToTape"] = {
                    "clientName": proxy_options["backupcopy_proxy"]
                }

            if "use_source_if_proxy_unreachable" in proxy_options:
                properties_dict["snapToTapeProxyToUseSource"] = True

        self._set_subclient_properties(
            "_commonProperties['snapCopyInfo']", properties_dict)

    def guest_file_restore(self,
                           application_name,
                           destination_path,
                           volume_level_restore,
                           disk_name=None,
                           proxy_client=None,
                           restore_list=None,
                           restore_pvc_guid=None,
                           **kwargs):
        """perform Guest file restore of the provided path

        Args:
            application_name_name   (str)   --  Name of the source application
            destination_path        (str)   --  Path at the destination to restore at
            volume_level_restore    (str)   --  Flag to denote volume_level_restore
                                                Accepted values -
                                                6 for restore to PVC
                                                7 for FS Destination restore
            disk_name               (str)   --  Name of the source PVC
            proxy_client            (str)   --  Access node for restore
            restore_list            (str)   --  List of files or folders to restore. Contains Full path
                                                of files or folders relative to PVC mount point.
                                                Eg. if /tmp is the mount point with files or folder /tmp/folder1/file1,
                                                restore list should have format 'folder1/file1'
            restore_pvc_guid        (str)   --  strGUID of the target PVC

        Kwargs:
            copy_precedence         (int)   --  To set copy precedence for restore
            disk_extension          (str)   --  Extention of the disk
            unconditional_overwrite (int)   --  To set unconditional overwrite for restore
            show_deleted_files      (bool)  --  Whether to show deleted files in browse
            in_place                (bool)  --  If restore job is inplace

        Raises:
            SDK Exception if
                -inputs are not of correct type as per definition

                -invalid volume_level_restore passed
        """
        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _guest_file_rst_options = {}
        _advanced_restore_options = {}

        copy_precedence = kwargs.get("copy_precedence", 0)
        disk_extn = kwargs.get("disk_extension", '')
        overwrite = kwargs.get("unconditional_overwrite", 1)
        unconditional_overwrite = kwargs.get('unconditional_overwrite', False)
        show_deleted_files = kwargs.get('show_deleted_files', False)
        in_place = kwargs.get('in_place', False)

        # check if inputs are correct
        if not (isinstance(application_name, str) and
                isinstance(destination_path, str) and
                isinstance(disk_name, str)):
            raise SDKException('Subclient', '101')
        if volume_level_restore not in [6, 7]:
            raise SDKException("Subclient", "102", "Invalid volume level restore type passed")

        if copy_precedence:
            _guest_file_rst_options['copy_precedence_applicable'] = True

        # fetching all disks from the application
        disk_list, disk_info_dict = self.disk_level_browse(
            "\\" + vm_ids[application_name])

        # Filter out disks with specified extension from disk list
        disk_list = list(filter(lambda name: self._get_disk_extension([name]) == disk_extn, disk_list))
        disk_info_dict = {disk: disk_info_dict[disk] for disk in disk_list}

        _guest_file_rst_options["destination_vendor"] = \
            self._backupset_object._instance_object._vendor_id

        if proxy_client is not None:
            _guest_file_rst_options['client'] = proxy_client
        else:
            _guest_file_rst_options['client'] = self._backupset_object._instance_object.co_ordinator

        # set Source item List
        src_item_list = []
        for each_item in restore_list:
            item = "\\".join(each_item.split('/'))
            src_item_list.append( "\\" + vm_ids[application_name] + "\\" + disk_name + "\\" + item)

        _guest_file_rst_options['paths'] = src_item_list

        if volume_level_restore == 6:

            if in_place:
                restore_pvc_guid = "{}`PersistentVolumeClaim`{}".format(
                    vm_ids[application_name].split('`')[0], disk_name
                )
                new_name = disk_name

            else:
                new_name = restore_pvc_guid.split('`')[-2]
                _advanced_restore_options['datacenter'] = "none"

            new_guid = restore_pvc_guid

        else:

            new_guid = "{}`PersistentVolumeClaim`{}".format(
                vm_ids[application_name].split('`')[0], disk_name
            )
            new_name = disk_name

        _guest_file_rst_options['in_place'] = in_place
        _guest_file_rst_options['volume_level_restore'] = volume_level_restore
        _guest_file_rst_options['unconditional_overwrite'] = unconditional_overwrite
        _guest_file_rst_options['show_deleted_files'] = show_deleted_files

        _advanced_restore_options['new_guid'] = new_guid
        _advanced_restore_options['new_name'] = new_name
        _advanced_restore_options['name'] = disk_name
        _advanced_restore_options['guid'] = vm_ids[application_name]
        _advanced_restore_options['end_user_vm_restore'] = True

        # set advanced restore options disks
        _disk_dict = self._disk_dict_pattern(disk_name, "")
        _advanced_restore_options['disks'] = [_disk_dict]

        advanced_options_dict = self._json_restore_advancedRestoreOptions(_advanced_restore_options)
        self._advanced_restore_option_list.append(advanced_options_dict)

        self._set_restore_inputs(
            _guest_file_rst_options,
            in_place=False,
            copy_precedence=copy_precedence,
            destination_path=destination_path,
            paths=src_item_list
        )

        request_json = self._prepare_disk_restore_json(_guest_file_rst_options)

        # Populate the advancedRestoreOptions section
        self._virtualserver_option_restore_json["diskLevelVMRestoreOption"][
            "advancedRestoreOptions"] = self._advanced_restore_option_list
        self._advanced_restore_option_list = []

        return self._process_restore_response(request_json)

    def guest_files_browse(
            self,
            application_path='\\',
            show_deleted_files=False,
            restore_index=True,
            from_date=0,
            to_date=0,
            copy_precedence=0,
            media_agent=""):
        """Browses the Files and Folders inside a Virtual Machine in the time
           range specified.

            Args:
                application_path    (str)   --  folder path to get the contents
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
            vm_files_browse=False, media_agent=media_agent)

    def _get_apps_in_namespace(self, namespaces):
        """Get the list of applications to be restored with the namespace level restore

            Args:
                namespaces      (list)  -   List of namespaces

            Returns:

                  list of applictations to be restored with namespaces
        """

        apps_to_restore = []
        namespace_app_dict = {}
        app, app_dict = self.browse()
        for app_path, metadata in app_dict.items():
            app_name = metadata['name']
            app_id = metadata['snap_display_name']
            app_ns = app_id.split('`')[0]
            app_type = app_id.split('`')[1]
            if app_type != 'Namespace' and app_ns in namespaces:
                apps_to_restore.append(app_name)
                namespace_app_dict[app_name] = app_ns

        return apps_to_restore, namespace_app_dict

    def namespace_restore_out_of_place(
            self,
            namespace_to_restore,
            target_namespace_name={},
            target_cluster_name=None,
            storage_class_map=None,
            overwrite=True,
            copy_precedence=0,
            proxy_client=None
    ):
        """Perform a namespace-level restore out-of-place

            Args:

                namespace_to_restore        (list)  --  List of namespaces to restore

                target_namespace_name       (dict)  --  Target namespace name to perform restore at
                                                        Eg. {'namespace1': 'namespace1-rst'}

                target_cluster_name         (str)   --  Name of the target cluster to restore at

                storage_class_map           (dict)  --  Mapping of storage classes for transformation
                                                        Eg. {'rook-ceph-block' : 'azurefile'}

                overwrite                   (bool)  --  Overwrite the existing namespace
                                                        Default: true

                copy_precedence             (int)   --  Copy preceedence value

                proxy_client                (str)   --  Name of the proxy client to launch restore
                                                        Default : None (Automatic)
            Returns:

                object - instance of the Job class for this restore job

            Raises:

                SDKException:

                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        restore_options = {}

        # Check mandatory input parameters are correct
        if namespace_to_restore and not type(namespace_to_restore) is list:
            raise SDKException('Subclient', '101')

        # Populating proxy client. It automatically fetches proxy controller from subclient/instance level
        # property if not specified
        if proxy_client is not None:
            restore_options['client'] = proxy_client

        restore_new_name = {}
        apps_to_restore = []

        if not type(target_namespace_name) is dict:
            raise SDKException('Subclient', '101')
        for ns in namespace_to_restore:
            if ns not in target_namespace_name:
                target_namespace_name[ns] = ns
        restore_new_name.update(target_namespace_name)

        namespace_apps, namespace_app_map = self._get_apps_in_namespace(namespace_to_restore)
        apps_to_restore.extend(namespace_apps)

        for app in apps_to_restore:
            restore_new_name[app] = app
        apps_to_restore.extend(namespace_to_restore)

        restore_options['restore_new_name'] = restore_new_name
        restore_options['namespace_app_map'] = namespace_app_map

        if not target_cluster_name:
            target_cluster_name = self._client_object.client_name

        self._set_restore_inputs(
            restore_options,
            in_place=False,
            vcenter_client=target_cluster_name,
            esx_host=target_cluster_name,
            esx_server=None,
            unconditional_overwrite=overwrite,
            power_on=True,
            vm_to_restore=self._set_vm_to_restore(apps_to_restore),
            disk_option=self._disk_option['Original'],
            transport_mode=self._transport_mode['Auto'],
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            source_item=[],
            source_ip=None,
            destination_ip=None,
            network=None,
            storage_class_map=storage_class_map
        )

        request_json = self._prepare_kubernetes_restore_json(restore_options)
        return self._process_restore_response(request_json)

    def namespace_restore_in_place(
            self,
            namespace_to_restore,
            overwrite=True,
            copy_precedence=0,
            proxy_client=None
    ):
        """Perform a namespace-level restore in-place

            Args:

                namespace_to_restore        (list)  --  List of namespaces to restore

                overwrite                   (bool)  --  Overwrite the existing namespace
                                                        Default: true

                copy_precedence             (int)   --  Copy preceedence value

                proxy_client                (str)   --  Name of the proxy client to launch restore
                                                        Default : None (Automatic)
            Returns:

                object - instance of the Job class for this restore job

            Raises:

                SDKException:

                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        restore_options = {}

        # Check mandatory input parameters are correct
        if namespace_to_restore and not type(namespace_to_restore) is list:
            raise SDKException('Subclient', '101')

        # Populating proxy client. It automatically fetches proxy controller from subclient/instance level
        # property if not specified
        if proxy_client is not None:
            restore_options['client'] = proxy_client

        apps_to_restore = []

        namespace_apps, namespace_app_map = self._get_apps_in_namespace(namespace_to_restore)
        apps_to_restore.extend(namespace_apps)
        apps_to_restore.extend(namespace_to_restore)

        client_name = self._client_object.client_name
        self._set_restore_inputs(
            restore_options,
            vm_to_restore=self._set_vm_to_restore(apps_to_restore),
            in_place=True,
            esx_host=client_name,
            esx_server_name="",
            volume_level_restore=1,
            unconditional_overwrite=overwrite,
            disk_option=self._disk_option['Original'],
            transport_mode=self._transport_mode['Auto'],
            copy_precedence=copy_precedence
        )

        request_json = self._prepare_kubernetes_inplace_restore_json(restore_options)
        return self._process_restore_response(request_json)


class ApplicationGroups(Subclients):

    ''' Class to create Kubernetes Application groups
        Derived from Subclients class
    Args:
        class_object  of Backupset class
     '''

    def __init__(self, class_object):

        super(ApplicationGroups, self).__init__(class_object)

    def __do_browse(self, browse_type="Applications", namespace=None, ns_guid=None):
        """Do GET browse request based on the browse type
            Args:
                browse_type     (str)   --  Type of browse (mandatory if namespace is not None)
                                            Accepted values - Namespaces, Applications, Volumes, Labels
                namespace       (str)   --  Namespace to browse

                ns_guid         (str)   --  Namespace GUID of namespace to browse
        """

        browse_type_dict = {
            "Namespaces": "GET_K8S_NS_BROWSE",
            "Applications": "GET_K8S_APP_BROWSE",
            "Volumes": "GET_K8S_VOLUME_BROWSE",
            "Labels": "GET_K8S_LABEL_BROWSE"
        }

        if not (namespace and ns_guid):
            service = browse_type_dict["Namespaces"]
            parameters = int(self._client_object.client_id)
        else:
            service = browse_type_dict[browse_type]
            parameters = (namespace, ns_guid, int(self._client_object.client_id))

        flag, get_browse = self._cvpysdk_object.make_request(
            'GET', self._services[service] % parameters
        )

        if flag:
            if get_browse and get_browse.json():
                browse_json = get_browse.json()
                if not 'inventoryInfo' in browse_json:
                    raise SDKException(
                        'Subclient',
                        '102',
                        "Failed to browse cluster content\nContent returned does not have inventoryInfo"
                    )
                else:
                    return browse_json['inventoryInfo']
            else:
                raise SDKException(
                    'Subclient',
                    '102',
                    'Failed to browse cluster content\nInvalid response'
                )
        else:
            try:
                # If browse fails then append raise HTTP exception to get error reason
                get_browse.raise_for_status()
            except Exception as exp:
                raise SDKException(
                    'Subclient',
                    '102',
                    f'Failed to browse cluster content\nError: "{exp}"'
                )

    def __get_children_json(self, app_name, app_type, browse_type, browse_response=None, selector=False):
        """Private method to return the json object for the application
            Args:
                app_name    (str)   --  Name of the application
                app_type    (str)   --  Application type (FOLDER/VM/Selector)
                browse_type (str)   --  Browse type of application
                browse_response (str)   --  Browse response from discovery
                selector    (str)   --  If content is a label selector
        """

        # JSON format is different in case of applications and selectors
        if selector:
            if browse_type == "Applications":
                # Casting Applications to Application since `Applications` is not recognized for selectors
                browse_type = "Application"
            if browse_type not in ['Application', 'Namespaces', 'Volumes']:
                raise SDKException(
                    'Subclient',
                    '102',
                    'Invalid browse type for Selector.'
                )

            return {
                "equalsOrNotEquals": True,
                "displayName": f"{browse_type}:{app_name}",
                "value": f"{browse_type}:{app_name}",
                "allOrAnyChildren": True,
                "type": app_type,
                "name": app_type
            }

        else:
            for app_item in browse_response:
                # Iterate over each application in browse response to get strGUID of selected app
                if app_item['name'] == app_name:
                    if browse_type == "Volumes" and app_type == "FOLDER":
                        app_item['strGUID'].replace('Namespace', 'Volumes')
                    return {
                            "equalsOrNotEquals": True,
                            "displayName": app_item['name'],
                            "allOrAnyChildren": True,
                            "type": app_type,
                            "name": app_item['strGUID']
                    }
            else:
                # If for loop completes without returning, then app does not exist in browse
                raise SDKException(
                    'Subclient',
                    '102',
                    f'Searched element [{app_name}] not found in browse.'
                )

    def get_children_node(self, content):
        """Construct and return the json object for content
            Args:
                content     (list)      --  Content to parse and construct json object
                                            Check create_application_group for usage.
        """

        # List of accepted browse types for application and selector
        app_browse_list = ['Applications', 'Labels', 'Volumes']
        selector_browse_list = ['Applications', 'Application', 'Namespaces', 'Volumes']

        if not type(content) is list:
            raise SDKException('Subclient', '101', 'Invalid data type for content.')

        children = []
        for item in content:
            if not type(item) is str:
                raise SDKException('Subclient', '101', 'Invalid data type for content.')

            # Split first `:` to get content type (Application or Selector).
            if item.find(':') < 0:
                item = 'Application:' + item
            content_type, content_item = item.split(':', 1)

            # Split second `:` to get Browse type and app value
            if content_item.find(':') < 0:
                content_item = 'Applications:' + content_item
            browse_type, app = content_item.split(':')

            # Format check
            if (content_type == 'Selector' and browse_type not in selector_browse_list) or \
                (content_type == 'Application' and browse_type not in app_browse_list):
                raise SDKException('Subclient', '101', 'Invalid string format for content.')

            browse_response = ""
            app_type = ""
            selector = False

            if content_type == 'Selector':
                app_type = "Selector"
                browse_response=None
                app_name = app
                selector = True

            elif content_type == 'Application':
                app_split = app.split('/')
                app_name = app_split[-1]
                if len(app_split) > 1:

                    # If split length is > 1, then fetch browse response of application
                    browse_response = self.browse(browse_type=browse_type, namespace=app_split[0])
                    app_type = "VM"
                else:

                    # If split length = 1, then fetch browse response of namespace
                    browse_response = self.browse(browse_type="Namespaces")
                    app_type = "FOLDER"
            else:
                raise SDKException('Subclient', '101', 'Invalid content type.')

            children.append(self.__get_children_json(
                    app_name=app_name,
                    app_type=app_type,
                    browse_type=browse_type,
                    browse_response=browse_response,
                    selector=selector
                )
            )

        return children

    def browse(self, browse_type='Namespaces', namespace=None):
        """Browse cluster content
            Args:
                browse_type     (str)   --  Browse type to perform
                                            Accepted values - Namespaces, Appilcations, Volumes, Labels
                namespace       (str)   --  Namespace to browse in
        """

        if browse_type not in ["Namespaces", "Applications", "Volumes", "Labels"]:
            raise SDKException(
                'Subclient',
                '101',
                f'Invalid value passed for browse_type [{browse_type}]'
            )

        all_namespaces = self.__do_browse(browse_type="Namespaces")

        # If namespace is not passed, or browse_type is Namespaces, return browse response from namespaces
        if browse_type == "Namespaces" or not namespace:
            return all_namespaces

        ns_guid = ""
        for ns in all_namespaces:
            if ns['name'] == namespace:
                ns_guid = ns['strGUID']
                break
        else:
            raise SDKException(
                'Subclient',
                '102',
                f"Could not fetch namespace GUID for namespace [{namespace}]"
            )

        # Encoding ` characters for URL
        ns_guid = ns_guid.replace('`', '%60')

        return self.__do_browse(browse_type=browse_type, namespace=namespace, ns_guid=ns_guid)

    def create_application_group(self,
                                 content,
                                 plan_name=None,
                                 filter=None,
                                 subclient_name="automation"):

        """Create application / Kubernetes Subclient.

            Args:
                client_id               (str)       --  Client id

                content                 (list)      --  Subclient content. Format 'ContentType:BrowseType:namespace/app'
                                                        Should be a list of strings with above format.

                                                        Valid ContentType -
                                                            Application, Selector.
                                                            If not specified, default is 'Application'
                                                        Valid BrowseType for Application ContentType -
                                                            Applications, Volumes, Labels
                                                            If not specified, default is 'Applications'
                                                        Valid BrowseType for Selector ContentType -
                                                            Application, Applications, Volumes, Namespaces
                                                            If not specified, default is 'Namespaces'

                                                        Examples -
                                                            1. ns001 --  Format : namespace
                                                            2. ns001/app001 --  Format : namespace/app
                                                            3. Volumes:ns001/pvc001 --  Format : BrowseType:namespace/app
                                                            4. Selector:Namespaces:app=demo -n ns004 --  Format : ContentType:BrowseType:namespace
                                                            5. ['Application:Volumes:nsvol/vol001', 'nsvol02/app1']
                                                            ...

                plan_name               (str)       --  Plan name

                filter                  (list)      --  filter for subclient content.
                                                        See 'content' for format and examples

                subclient_name          (str)       --  Subclient name you want to create Subclient

        """

        content_children = []
        filter_children = []

        # Get the json objects for content and filters
        content_children.extend(self.get_children_node(content))
        if filter:
            filter_children.extend(self.get_children_node(filter))

        plan_id = int(self._commcell_object.plans[str(plan_name.lower())])

        app_create_json = {
            "subClientProperties": {
                "vmContentOperationType": 'ADD',
                "vmContent": {
                    "children": content_children
                },
                "subClientEntity": {
                    "clientId": int(self._client_object.client_id),
                    "appName": "Virtual Server",
                    "applicationId": 106,
                    "subclientName": subclient_name
                },
                "planEntity": {
                    "planId": plan_id
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

        if filter:
            # If filter is passed for subclient, additional flags are added to create subclient json
            app_create_json['subClientProperties']['vmFilterOperationType'] = 'ADD'
            app_create_json['subClientProperties']['vmDiskFilterOperationType'] = 'ADD'
            app_create_json['subClientProperties']['vmFilter'] = { 'children' : filter_children}

        flag, response = self._cvpysdk_object.make_request('POST', self._services['ADD_SUBCLIENT'],
                                                           app_create_json)
        if flag == False:
            raise SDKException('Response', '101', self._update_response_(response.text))
