#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Constants for specifying the Hyper Visor Type for Virtual Server agents.

All supported hyper visors must be added to the HyperVisor class of type Enum.

HyperVisorType:     Enum class for Instance Names

"""

from enum import Enum


class HyperVisor(Enum):
    """Class for mapping the Instance Name of a Virtual Server Agent Client to a general name."""

    VIRTUAL_CENTER = "VMware"
    MS_VIRTUAL_SERVER = "hyper-v"
    AZURE = "Azure"
    AZURE_V2 = "Azure Resource Manager"
