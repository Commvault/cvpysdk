# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright  Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Azure Stack Instance.

AzureStackInstance is the only class defined in this file.

AzureStackInstance:         Derived class from VirtualServer
                            Base class, representing a Azure Stack
                            instance, and to perform operations on that
                            instance

    __init__(self, agent,_name,iid)   	 -- initialize object of azure Stack
                                            Instance object associated with the
                                            VirtualServer Instance

    _get_instance_properties()           -- VirtualServer Instance class method
                                            overwritten to get azure Stack
                                            Specific instance properties as well

	_get_instance_properties_json()		 -- get the all instance related
											properties of this subclient.

"""

from ..vsinstance import VirtualServerInstance


class AzureStackInstance(VirtualServerInstance):
    """Class for representing Azure stack instance of the Virtual Server agent"""

    def __init__(self, agent, name, iid):

        """ Initialize the Instance object for the given Virtual Server instance

            Args:
                agent               (object)    --  the instance of the agent class

                name                (str)       --  the name of the instance

                iid                 (int)       --  the instance id

        """
	self._vendor_id = 403
        self._subscriptionid = None
        self._applicationid = None
        self._server_name = []
        super(AzureStackInstance, self).__init__(agent, name, iid)


    def  _get_instance_properties(self):
        """
        Get the properties of this instance

        Raise:
            SDK Exception:
                if response is not empty
                if response is not success
        """

        super(AzureStackInstance, self)._get_instance_properties()

        if "vmwareVendor" in self._virtualserverinstance:
            self._subscriptionid = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['domainName']

            self._applicationid = self._virtualserverinstance['vmwareVendor'][
                'virtualCenter']['userName']

        if 'virtualServerInstance' in self._properties:
            _member_servers = self._properties["virtualServerInstance"] \
                                                ["associatedClients"]["memberServers"]
            for _each_client in _member_servers:
                client = _each_client['client']
                if 'clientName' in client.keys():
                    self._server_name.append(str(client['clientName']))



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
                    "vsInstanceType":  self._vendor_id,
                    "associatedClients": self._virtualserverinstance['associatedClients'],
                    "vmwareVendor": {}
                    }
                       }
               }
        return instance_json


    @property
    def server_host_name(self):
        """return the associated clients with the instance"""
        return self._server_name

    @property
    def subscriptionid(self):
        """
        returns the subcriptionID of the instance

        """
        return self._subscriptionid

    @property
    def applicationid(self):
        """
        returns the applciationID of the instance
        """
        return self._applicationid
