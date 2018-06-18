# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server OracleVM.

OracleVMVirtualServerSubclient is the only class defined in this file.

OracleVMVirtualServerSubclient: Derived class from VirtualServerSubClient  Base class,
                            representing a OracleVM Subclient, and
                            to perform operations on that Subclient

OracleVMVirtualServerSubclient:

    __init__(,backupset_object, subclient_name, subclient_id)--  initialize object of FusionCompute
                                                                             subclient object
                                                                                 associated with
                                                                        the VirtualServer subclient

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                     to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()              --  restores the VM specified by the
                                                    user to the same location
"""

from past.builtins import basestring
from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class OracleVMVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
           This represents a OracleVM virtual server subclient,
           and can perform restore operations on only that subclient.

        """
    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """

        super(OracleVMVirtualServerSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self.diskExtension = [".img"]

    def full_vm_restore_in_place(
            self,
            vm_to_restore=None,
            destination_client=None,
            overwrite=True,
            power_on=True,
            disk_option='Original',
            transport_mode='Auto',
            copy_precedence=0):
        """Restores the FULL Virtual machine specified in the input list
            to the location same as the actual location of the VM in VCenter.

            Args:
                vm_to_restore       (list)     --  provide the VM name to
                                                   restore
                                                   default: None

                destination_client (basestring)  -- proxy client to be used for
                                                    restore
                                                    default: proxy added in
                                                    subclient

                overwrite           (bool)     --  overwrite the existing VM
                                                   default: True

                power_on            (bool)     --  power on the  restored VM
                                                   default: True

               disk_option       (basestring) -- disk provisioning for the
                                                  restored vm
                                                  default: 0 which is equivalent
                                                  to Original

                transport_mode    (basestring) -- transport mode that need to be
                                                  used

                copy_precedence     (int)      --  copy precedence value
                                                   default: 0


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

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            volume_level_restore=1,
            client_name=destination_client,
            in_place=True,
            transport_mode=self._transport_mode.get(transport_mode.replace(" ", "").lower(),
                                                    self._transport_mode["auto"]),
            disk_option=self._get_disk_provisioning_value(disk_option),
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            restored_vm_name=None,
            disk_name_prefix=None,
            virtualization_client=None,
            destination_client=None,
            repository=None,
            overwrite=True,
            power_on=True,
            server=None,
            copy_precedence=0,
            disk_provisioning='Original'):
        """Restores the FULL Virtual machine specified in the input list
            to the provided vcenter client along with the ESX and the datastores.
            If the provided client name is none then it restores the Full Virtual
            Machine to the source client and corresponding ESX and datastore.

            Args:
                vm_to_restore     (string)  --  provide the VM name to restore
                                              {"name_of_vm_to_restore":
                                              "new_name_of_restored_vm"}
                                              default: {}
                restored_vm_name   (string)  -- name of the new VM that should
                                                restored.

                disk_name_prefix    (string) -- new name for the disks while restoring
                                                the VM

                virtualization_client   (basestring) -- name of the Oracle
                                                    virtualization
                                                    client that needs to be
                                                    restored

                destination_client    (basestring) -- name of the proxy that
                                                    should be used during
                                                    restore

                repository         (basestring) -- datastore where the
                                                  restored VM should be located
                                                  restores to the source VM
                                                  datastore if this value is
                                                  not specified

                overwrite         (bool)       -- overwrite the existing VM
                                                  default: True

                power_on          (bool)       -- power on the  restored VM
                                                  default: True

                server          (basestring) -- destination cluster or  host
                                                    restores to the source VM
                                                    esx if this value is not
                                                    specified




                copy_precedence   (int)        -- copy precedence value
                                                  default: 0

                disk_option       (basestring) -- disk provisioning for the
                                                  restored vm default: 0
                                                  which is equivalent
                                                  to Original



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

        if vm_to_restore and not isinstance(vm_to_restore, basestring):
            raise SDKException('Subclient', '101')

        if not restored_vm_name and isinstance(vm_to_restore, basestring):
            restored_vm_name = "Delete" + vm_to_restore

        if copy_precedence:
            restore_option["copy_precedence_applicable"] = True

        if restored_vm_name:
            if not (isinstance(vm_to_restore, basestring) or
                    isinstance(restored_vm_name, basestring)):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = restored_vm_name

        if vm_to_restore:
            vm_to_restore = [vm_to_restore]

        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            disk_option=self._get_disk_provisioning_value(disk_provisioning),
            restore_new_name=restored_vm_name,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            client_name=destination_client,
            vcenter_client=virtualization_client,
            esx_host=server,
            datastore=repository,
            in_place=False,
            disk_name_prefix=disk_name_prefix
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
