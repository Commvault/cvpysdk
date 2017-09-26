#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ?2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server VMware Instance.

VMwareInstance is the only class defined in this file.

VMwareInstance: Derived class from VirtualServer  Base class, representing a
                           VMware instance, and to perform operations on that instance

VMwareInstance:

	__init__(agent_object,instance_name,instance_id)    --  initialize object of vmware Instance object associated with
																the VirtualServer Instance

    _get_instance_properties()  						--  VirtualServer Instance class method overwritten to get vmware Specific
                                                            instance properties as well

	_get_instance_properties_json(self)                 --  get the all instance(vmware) related properties of this subclient

"""

from ..vsinstance import VirtualServerInstance
from ...exception import SDKException
from ...instance import Instance

class VMwareInstance(VirtualServerInstance):

    def __init__(self, agent, name, iid):
        super(VirtualServerInstance, self).__init__(agent, name, iid)

    def  _get_instance_properties(self):
        """Gets the properties of this instance.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
                    
        """
        super(VMwareInstance, self)._get_instance_properties()
   
        if "vmwareVendor" in self._properties:
            self._vmwarvendor = self._virtualserverinstance[2]


    def _get_instance_properties_json(self):
        """get the all instance related properties of this subclient.        
           
           Returns:
                dict - all instance properties put inside a dict
           
        """
        instance_json = {
                            "instanceProperties":
                                {
                                    "isDeleted": False,
                                    "instance": self._instance,
                                    "instanceActivityControl": self._instanceActivityControl,
                                    "virtualServerInstance": {
                                        "vsInstanceType": self._virtualserverinstance['vsInstanceType'],
                                        "associatedClients": self._virtualserverinstance['associatedClients'],
                                        "vmwareVendor": self._virtualserverinstance['vmwareVendor']
                                    }
                                }
                        }
        return instance_json

    @property
    def _domain_name(self):
        """getter for the domain name in the vmware vendor json"""
        return self._vmwarvendor["domainName"]

    @property
    def _user_name(self):
        """getter for the username from the vmware vendor json"""
        return self._vmwarvendor["userName"]
    