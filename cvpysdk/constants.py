#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright �2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Helper file to maintain all the constants used in the SDK

HypervisorType  -       Enum which maintains the list of all the hypervisors supported by SDK

AppIDAType      -       Enum which maintains the list of all the IDA type values

"""

from enum import Enum


class HypervisorType(Enum):
    """Class to maintain all the hypervisor related constants"""
    VIRTUAL_CENTER = "VMware"
    MS_VIRTUAL_SERVER = "Hyper-V"
    AZURE = "Azure"
    AZURE_V2 = "Azure Resource Manager"


class AppIDAType(Enum):
    """Class to maintain all the app ida constants"""
    WINDOWS_FILE_SYSTEM = 33
    LINUX_FILE_SYSTEM = 29
