#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Virtual Server VMInstance Instance.

VMInstance is the only class defined in this file.

VMInstance:     Derived class from Instance  Base class, representing a
                        VMInstance, and to perform operations on that instance


VMInstance:

    __init__(
        agent_object,
        instance_name,
        instance_id)                    --  initialize object of VMInstance object
                                                associated with the Instance Instance
"""
from ..instance import Instance


class VMInstance(Instance):
    """
    Class for representing VMWare instance of the Virtual Server agent.
    """
    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Initialize the Instance object for the given Virtual Server instance.

                   Args:
                       agent_object    (object)    --  instance of the Agent class

                       instance_name   (str)       --  instance name

                       instance_id     (int)       --  instance id

        """
        super(VMInstance, self).__init__(agent_object, instance_name, instance_id)
