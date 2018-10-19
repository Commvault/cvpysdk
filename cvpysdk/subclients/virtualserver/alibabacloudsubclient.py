# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server AlibabaCloud Subclient.

AlibabaCloudVirtualServerSubclient is the only class defined in this file.

AlibabaCloudVirtualServerSubclient: Derived class from VirtualServerSubClient  Base class,
                            representing a AlibabaCloud Subclient, and
                            to perform operations on that Subclient

AlibabaCloudVirtualServerSubclient:

    full_vm_restore_out_of_place()  --  restores the VM specified in to the specified client,
                                        at the specified destination location

"""

from past.builtins import basestring
from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class AlibabaCloudVirtualServerSubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient Base class.
       This represents a AlibabaCloud virtual server subclient,
       and can perform restore operations on only that subclient.

    """

    def full_vm_restore_out_of_place(
            self,
            vm_to_restore=None,
            destination_client=None,
            proxy_client=None,
            new_name=None,
            availability_zone=None,
            instance_type=None,
            network=None,
            security_groups=None,
            power_on=True,
            overwrite=False,
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

                availability_zone       (str)   --  the availability zone to which the instances
                                                    has to be restored.

                        Note: You can restore the instances only to the same availability zone
                                as the proxy resides

                instance_type           (str)   --  the shape / size of the instance

                network                 (str)   --  the network to which the restore instance has
                                                    to be attached

                security_groups         (list)  --  the security groups to which the restored
                                                    instances need to be attached

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

        if bool(restore_option):
            if not (isinstance(overwrite, bool) and
                    isinstance(power_on, bool)):
                raise SDKException('Subclient', '101')

        if new_name:
            if not isinstance(new_name, basestring):
                raise SDKException('Subclient', '101')
            restore_option['restore_new_name'] = new_name

        if network:
            restore_option['destination_network'] = network.split("\\")[0]

        if instance_type:
            restore_option['instanceSize'] = instance_type

        if security_groups:
            restore_option['security'] = security_groups

        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            client_name=proxy_client,
            vcenter_client=destination_client,
            esx_host=availability_zone,
            in_place=False,
            restore_new_name=new_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)
