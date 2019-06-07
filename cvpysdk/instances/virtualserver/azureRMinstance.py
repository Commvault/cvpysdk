# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Azure Resource Manager Instance.

AzureResoureceManagerInstance is the only class defined in this file.

AzureResoureceManagerInstance: Derived class from VirtualServer
                            Base class, representing a Azure Resource Manager
                            instance, and to perform operations on that
                            instance

    __init__(self, agent,_name,iid)   	 -- 	initialize object of azure RM
                                            Instance object associated with the
                                            VirtualServer Instance		

    _get_instance_properties()     --  VirtualServer Instance class method
                                        overwritten to get azure RM
                                        Specific instance properties as well

	_get_instance_properties_json()			--  get the all instance related
														properties of this subclient.

"""

from ..vsinstance import VirtualServerInstance
from ...exception import SDKException
from ...instance import Instance

class AzureRMInstance(VirtualServerInstance):

    '''
    AzureResoureceManagerInstance:

	__init__(agent_object,instance_name,instance_id)    --  initialize object
    of azure resource manager Instance object associated with
		the VirtualServer Instance
    '''

    def __init__(self, agent, name, iid):
        """Initialize the Instance object for the given Virtual Server instance.

            Args:
                class_object (agent_object,instance_name,instance_id)  --  instance of the
                                                                                Agent class,
                                                                                instance name,
                                                                                instance id

        """

        self._vendor_id = 7
        super(VirtualServerInstance, self).__init__(agent, name, iid)




    def  _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(AzureRMInstance, self)._get_instance_properties()
        self._server_name = []
        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                                                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))
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
    def server_name(self):
        """getter for the domain name in the Hyper-V json"""
        return self._server_name

    @property
    def server_host_name(self):
        """getter for the domain name in the vmware vendor json"""
        return self._server_name
    #return self._server_name
    # TODO will change with Praveen Form(jmalik)
