#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ?2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Constants for SDK Operations.

HyperVisorType:
        Enum class for Instance Names

"""


from enum import Enum

class HyperVisorType(Enum):
    """ Maps the Instance Hypervisor  Name for general Names """
    VIRTUAL_CENTER = "VMware"
    MS_VIRTUAL_SERVER = "hyper-v"
    AZURE = "Azure"
    AZURE_V2  = "Azure Resource Manager"