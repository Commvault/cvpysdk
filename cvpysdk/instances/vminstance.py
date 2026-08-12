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

VMInstance:     Derived class from Instance  Base class, representing a VMInstance,
                and to perform operations on that instance

VMInstance:
    __init__()                    --  initialize object of VMInstance object associated with the Instance
"""
from ..instance import Instance

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..agent import Agent


class VMInstance(Instance):
    """
    Represents a VMWare instance managed by the Virtual Server agent.

    This class encapsulates the details and management of a VMWare instance,
    providing an interface for initializing and handling VMWare-specific
    virtual server instances within the broader backup or virtualization
    management framework.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Specialized for VMWare virtual server environments
        - Inherits core functionality from the base Instance class

    #ai-gen-doc
    """
    def __init__(self, agent_object: 'Agent', instance_name: str, instance_id: int = None) -> None:
        """Initialize a VMInstance object for the specified Virtual Server instance.

        Args:
            agent_object: An instance of the Agent class representing the associated agent.
            instance_name: The name of the virtual server instance.
            instance_id: Optional; the unique identifier for the instance. If not provided, it may be determined automatically.

        #ai-gen-doc
        """
        super(VMInstance, self).__init__(agent_object, instance_name, instance_id)
