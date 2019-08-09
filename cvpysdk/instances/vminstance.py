#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
