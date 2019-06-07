# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Nutanix AHV Subclient.

nutanixsubclient is the only class defined in this file.

nutanixsubclient: Derived class from VirtualServerSubClient  Base class, representing a
                           nutanix AHV Subclient, and to perform operations on that Subclient

nutanixsubclient:

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                        to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()                      --  restores the VM specified by the
                                                        user to the same location
"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class nutanixsubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    nutanix  virtual server subclient,and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        self.diskExtension = ["none"]
        super(nutanixsubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def full_vm_restore_out_of_place(self,
                                     vm_to_restore=None,
                                     host=None,
                                     container=None,
                                     proxy_client=None,
                                     restore_new_name=None,
                                     overwrite=True,
                                     power_on=True,
                                     copy_precedence=0,
                                     restore_option=None):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
                    at the specified destination location.

                    Args:

                        vm_to_restore         (list)       --  provide the VM name to restore

                        host                  (str)        -- ESX host for Vm to restore

                        container             (str)        -- provide the storage account to restore

                        proxy_client          (str)        -- provide the proxy client to restore

                        restore_new_name      (str)        -- provide the new restore name
                        overwrite
                                default:False (bool)       --  overwrite the existing VM

                        poweron
                                default:False (bool)       --  power on the  restored VM


                        restore_option        (dict)       --  complete dictionary with
                                                               all advanced option
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
        # restore options
        if restore_option is None:
            restore_option = {}

        # check input parameters are correct
        if bool(restore_option):
            if not (isinstance(overwrite, bool) and
                    isinstance(power_on, bool)):
                raise SDKException('Subclient', '101')

        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            esx_host=host,
            datastore=container,
            client_name=proxy_client,
            in_place=False,
            restore_new_name=restore_new_name
        )

        # set attr for all the option in restore xml from user inputs

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 copy_precedence=0):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore          (list)      --  provide the VM name to restore

                overwrite
                        default:true   (bool)      --  overwrite the existing VM

                poweron
                        default:true   (bool)      --  power on the  restored VM

                copy_precedence        (int)       -- storage policy copy precedence
                                                      from which browse has to be performed


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        restore_option = {}
        # check mandatory input parameters are correct
        if not (isinstance(overwrite, bool) and
                isinstance(power_on, bool)):
            raise SDKException('Subclient', '101')
        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            in_place=True
        )
        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
