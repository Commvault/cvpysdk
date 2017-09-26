#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Azure Resource Manager Instance.

AzureResoureceManagerInstance is the only class defined in this file.

AzureResoureceManagerInstance: Derived class from VirtualServer  Base class, representing a
                           Azure Resource Manager instance, and to perform operations on that instance

AzureResoureceManagerInstance:

	__init__(agent_object,instance_name,instance_id)    --  initialize object of azure resource manager Instance object associated with
																the VirtualServer Instance


"""

from ..vsinstance import VirtualServerInstance
from ...exception import SDKException
from ...instance import Instance

class AzureRMInstance(VirtualServerInstance):
    
    def __init__(self, agent, name, iid):
        super(VirtualServerInstance, self).__init__(agent, name, iid)
        
    