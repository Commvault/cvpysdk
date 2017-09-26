#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server Amazon Instance.

AmazonInstance is the only class defined in this file.

AmazonInstance: Derived class from VirtualServer  Base class, representing a
                           Amazon instance, and to perform operations on that instance

AmazonInstance:

	__init__(agent_object,instance_name,instance_id)    --  initialize object of amazon Instance object associated with
																the VirtualServer Instance


"""

from ..vsinstance import VirtualServerInstance
from ...exception import SDKException
from ...instance import Instance

class AmazonInstance(VirtualServerInstance):
    
    def __init__(self, agent, name, iid):
        super(VirtualServerInstance, self).__init__(agent, name, iid)
        

    