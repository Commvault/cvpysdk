# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server AzureStack Subclient.

AzureStackSubclient is the only class defined in this file.

AzureStackSubclient: Derived class from VirtualServerSubClient  Base class, representing a
                           AzureStack Subclient, and to perform operations on that Subclient

AzureStackSubclient:

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                        to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()                      --  restores the VM specified by the
                                                        user to the same location
"""

from ..vssubclient import VirtualServerSubclient
from .azure_resource_manager import AzureRMSubclient


class AzureStackSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    AzureStack virtual server subclient,and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        self.diskExtension = [".vhd", ".avhd"]
        super(AzureStackSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def full_vm_restore_out_of_place(self,
                                     vm_to_restore=None,
                                     resource_group=None,
                                     storage_account=None,
                                     proxy_client=None,
                                     restore_new_name=None,
                                     overwrite=False,
                                     power_on=False,
                                     instance_size=None,
                                     public_ip=True,
                                     restore_as_managed=True,
                                     copy_precedence=0,
                                     restore_option=None):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            at the specified destination location.

            Args:

                vm_to_restore         (list)       --  provide the VM name to restore

                resource_group        (str)        -- provide the resource group to restore

                storage_account       (str)        -- provide the storage account to restore

                proxy_client          (str)        -- provide the proxy client to restore

                restore_new_name      (str)        -- provide the new restore name

                instance_size         (str)        -- provide the instance size of the restore VM

                createPublicIP
                        default:True   (bool)      --  creates the Public IP of the new VM

                restoreAsManagedVM
                        default:False   (bool)      --  new VM will be restored as unmanaged VM


                overwrite
                        default:False   (bool)      --  overwrite the existing VM

                poweron
                        default:False   (bool)      --  power on the  restored VM


                restore_option      (dict)     --  complete dictionary with all advanced optio
                    default: {}

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if destination_path is not a string

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        AzureRMSubclient.full_vm_restore_out_of_place(
            self, vm_to_restore, resource_group, storage_account,
            proxy_client, restore_new_name, restore_option, overwrite, power_on,
            instance_size, public_ip, restore_as_managed,
            copy_precedence)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 public_ip=True,
                                 restore_as_managed=False,
                                 copy_precedence=0):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore         (list)       --  provide the VM name to restore

                createPublicIP
                        default:True   (bool)      --  creates the Public IP of the new VM

                restoreAsManagedVM
                        default:False   (bool)      --  new VM will be restored as unmanaged VM

                overwrite
                        default:true   (bool)      --  overwrite the existing VM

                poweron
                        default:true   (bool)      --  power on the  restored VM


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """

        AzureRMSubclient.full_vm_restore_in_place(
            self, overwrite, power_on,
            public_ip, restore_as_managed, copy_precedence)
