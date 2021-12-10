# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server OracleCloud Subclient.

OracleCloudeVirtualServerSubclient is the only class defined in this file.

OracleCloudVirtualServerSubclient: Derived class from VirtualServerSubClient  Base class,
                            representing a OracleCloud Subclient, and
                            to perform operations on that Subclient

OracleCloudVirtualServerSubclient:

    full_vm_restore_out_of_place()  --  restores the VM specified in to the specified client,
                                        at the specified destination location

    full_vm_restore_in_place()  --  restores the VM specified in to the source client,

"""
import time
from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class OCIVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a OracleCloud virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        super(OCIVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = ["none"]
        self.vm_obj = None
        self.source_vm_details = None
        self.hvobj = None

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            destination_client=None,
            proxy_client=None,
            new_name='AutomationRestored_'+str(int(time.time())),
            copy_preceedence=0,
            power_on=True,
            source_vm_details=None,
            restore_option=None,
            indexing_v2=True,
            **kwargs):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore           (list)  --  list of all VMs to restore

                destination_client      (str)   --  name of the pseudo client where VM should be
                                                        restored

                proxy_client            (str)   --  the proxy to be used for restore

                new_name                (str)   --  new name to be given to the restored VM

                power_on                (bool)  --  power on the restored VM
                                                        default: True

                copy_precedence         (int)   --  copy precedence to restored from
                                                        default: 0

                restore_option          (dict)  --  dictionary with all the advanced restore
                                                        options.

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_out_of_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        #self.hvobj = hvobj
        #self.vm_obj = self.hvobj.get_vm_property(vm_to_restore)
        #vm_ip = self.hvobj['oci_vm_ip'],
        #vm_guid = self.hvobj['oci_vm_guid'],
        #vm_guidip = self.hvobj['oci_vm_ip'],
        copy_precedence = 0
        self.source_vm_details = source_vm_details
        if not restore_option:
            restore_option = {}
        restore_option["v2_details"] = kwargs.get("v2_details", None)
    # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(),
            power_on=True,
            copy_precedence=copy_precedence,
            indexing_v2=indexing_v2,
            restore_new_name=new_name,
            esx_server=self._instance_object._server_name[0],
            in_place=False,
            source_ip=self.source_vm_details['source_ip'],
            destination_ip=None,
            restoreToDefaultHost=False,
            destination_vendor=0,
            destination_disktype=0,
            useVcloudCredentials=True
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 source_vm_details=None,
                                 vm_to_restore=None,
                                 proxy_client=None,
                                 overwrite=True,
                                 power_on=True,
                                 copy_precedence=0,
                                 indexing_v2= True,
                                 **kwargs):

        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore         (list)       --  provide the VM name to restore

                overwrite
                        default:true   (bool)      --  overwrite the existing VM

                proxy_client            (str)   --  the proxy to be used for restore

                power_on
                        default:true   (bool)      --  power on the  restored VM

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_out_of_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success


        """
        self.source_vm_details = source_vm_details
        #self.hvobj = hvobj
        #self.vm_obj = self.hvobj.get_vm_property(vm_to_restore)
        restore_option = {"v2_details": kwargs.get("v2_details", None)}
    # check mandatory input parameters are correct
        if not (isinstance(overwrite, bool) and
                isinstance(power_on, bool)):
            raise SDKException('Subclient', '101')
        # set attr for all the option in restore xml from user inputs
        #copy_precedence = 0
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(),
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            out_place=False,
            in_place=True,
            power_on=True,
            indexing_v2=indexing_v2,
            esx_server=self._instance_object._server_name[0],
            source_ip=self.source_vm_details['source_ip'],
            destination_ip=None,
            restoreToDefaultHost=False,
            useVcloudCredentials=True,
            unconditional_overwrite=False,
            noImage=True,
            isFromBrowseBackup=True
        )
        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def set_advanced_vm_restore_options(self, vm_to_restore, restore_option):
        """
        set the advanced restore options for all vm in restore
        :param

        vm_to_restore : Name of the VM to restore
        restore_option: restore options that need to be set for advanced restore option

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

        # populate restore source item
        restore_option['paths'].append("\\" + vm_ids[vm_to_restore])
        restore_option['name'] = vm_to_restore
        restore_option['guid'] = self.source_vm_details['guid']#self.vm_obj['guid']
        restore_option["FolderPath"] = folder_path
        restore_option["ResourcePool"] = "/"

        # populate restore disk and datastore
        vm_disks = []
        disk_list, disk_info_dict = self.disk_level_browse("\\\\" + vm_ids[vm_to_restore])

        for disk, data in disk_info_dict.items():
            if ((restore_option["in_place"]) or ("datastore" not in restore_option)):
                restore_option["datastore"] = data["advanced_data"]["browseMetaData"][
                                             "virtualServerMetaData"]["datastore"]
                restore_option['vmSize'] = self.source_vm_details['vmSize']
            _disk_dict = self._disk_dict_pattern(disk.split('\\')[-1], restore_option["datastore"])
            vm_disks.append(_disk_dict)
        if not vm_disks:
            raise SDKException('Subclient', 104)
        restore_option["disks"] = vm_disks

        # prepare nics info json
        nics_list = self._json_nics_advancedRestoreOptions(vm_to_restore, restore_option)

        restore_option["nics"] = nics_list
        if restore_option["source_ip"] and restore_option["destination_ip"]:
            vm_ip = self._json_vmip_advanced_restore_options(restore_option)
            restore_option["vm_ip_address_options"] = vm_ip
        if restore_option["in_place"]:
            restore_option['createPublicIP'] = False
            if "hyper" in restore_option["destination_instance"]:
                restore_option["client_name"] = vs_metadata['esxHost']
                restore_option["esx_server"] = vs_metadata['esxHost']
        else:
            restore_option['createPublicIP'] = True
        # populate VM Specific values
        self._set_restore_inputs(
            restore_option,
            disks=vm_disks,
            esx_host=vs_metadata['esxHost'],
            instanceSize=self.source_vm_details['vmSize'],
            createPublicIP=True,
            vmSize=self.source_vm_details['vmSize'],
            new_name="Delete" + vm_to_restore
        )

        temp_dict = self._json_restore_advancedRestoreOptions(restore_option)
        self._advanced_restore_option_list.append(temp_dict)


    def _json_nics_advancedRestoreOptions(self, vm_to_restore, value):
        """
            Setter for nics list for advanced restore option json

        """

        #nics_dict_from_browse = self.get_nics_from_browse()
        nics_list = []
        #vm_nics_list = nics_dict_from_browse[vm_to_restore]

        for key, val in self.source_vm_details['vcn'].items():
            nics = {
                "subnetId": val['subnet_id'],
                "sourceNetwork": val['display_name'],
                "sourceNetworkId": val['subnet_id'],
                "name": val['network_id'],
                "networkName": val['display_name'],
                "networkDisplayName": val['network_id'],
                "destinationNetwork": val['subnet_id']
            }

            nics_list.append(nics)

        return nics_list
    

    def _json_restore_volumeRstOption(self, value):
        """setter for  the Volume restore option for in restore json"""

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._volume_restore_json = {
            "volumeLeveRestore": False,
            "volumeLevelRestoreType": value.get("volume_level_restore", 1)
        }

    def _json_vcenter_instance(self, value):
        """ Setter for vcenter_instance JSON """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')


        self._vcenter_instance_json = {
            "clientName": value.get("destination_client_name", ""),
            "instanceName": value.get("destination_instance", "")
        }
