# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Fusion Compute Instance.

FusionComputeInstance is the only class defined in this file.

FusionComputeInstance: Derived class from VirtualServer  Base class, representing a
                           Fusion Compute instance, and to perform operations on that instance

HyperVInstance:

    __init__(agent_object,instance_name,instance_id)    -- initialize object of FusionCompute
                                                                Instance object associated with the
                                                                        VirtualServer Instance


    _get_instance_properties()                          --  VirtualServer Instance class method
                                                            overwritten to get Fusion Compute
                                                            Specific instance properties as well

    _set_instance_properties()                          --  Fusion Compute Instance class method
                                                                to set Fusion Compute
                                                                Specific instance properties


"""


from ..vsinstance import VirtualServerInstance

class FusionComputeInstance(VirtualServerInstance):
    """Class for representing an Hyper-V of the Virtual Server agent."""

    def __init__(self, agent, instance_name, instance_id=None):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (agent_object,instance_name,instance_id)  --  instance of the
                                                                                Agent class,
                                                                                instance name,
                                                                                instance id

        """
	self._vendor_id = 14
        super(FusionComputeInstance, self).__init__(agent, instance_name, instance_id)     
        self._server_name = None




    def  _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(FusionComputeInstance, self)._get_instance_properties()
        # waiting for praveen form


    def _get_instance_properties_json(self):
        """get the all instance related properties of this subclient.

          Returns:
               dict - all instance properties put inside a dict

        """
        instance_json = {
            "instanceProperties":{
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "virtualServerInstance": {
                    "vsInstanceType": self._vendor_id,
                    "associatedClients": self._virtualserverinstance['associatedClients'],
                    "vmwareVendor": {}
                    }
            }
        }
        return instance_json


    @property
    def server_host_name(self):
        """return the Fusion compute VRM  associated with the PseudoClient"""
        #return self._server_name
        # TODO will change with Praveen Form(rsn)
        return ["172.24.20.146"]
        #for now to move on hard coed it
