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

"""

from ..vssubclient import VirtualServerSubclient


class OracleCloudVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a OracleCloud virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            destination_client=None,
            proxy_client=None,
            new_name=None,
            host=None,
            power_on=True,
            copy_precedence=0,
            restore_option=None):
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

                host                    (str)   --  destination host or cluster; restores to the
                                                        source VM ESX if this value is not
                                                        specified

                power_on                (bool)  --  power on the restored VM
                                                        default: True

                copy_precedence         (int)   --  copy precedence to restored from
                                                        default: 0

                restore_option          (dict)  --  dictionary with all the advanced restore
                                                        options.

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """
        if not restore_option:
            restore_option = {}

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            power_on=power_on,
            copy_preceedence=copy_precedence,
            volume_level_restore=1,
            client_name=proxy_client,
            vcenter_client=destination_client,
            esx_host=host,
            out_place=True,
            restore_new_name=new_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
