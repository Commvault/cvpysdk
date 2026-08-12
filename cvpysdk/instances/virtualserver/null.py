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
from cvpysdk.exception import SDKException
from cvpysdk.instances.vsinstance import VirtualServerInstance


class NullSubclient(VirtualServerInstance):
    """
    A specialized subclient class representing a null or placeholder subclient for virtual server instances.

    This class is intended to serve as a base or default implementation for subclients that do not require
    specific backup or restore operations. It is initialized with an agent object, instance name, and instance ID,
    and inherits from the VirtualServerInstance class.

    Key Features:
        - Acts as a placeholder or default subclient for virtual server instances
        - Initialization with agent object, instance name, and instance ID
        - Inherits core functionality from VirtualServerInstance

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: int = None) -> None:
        """Initialize a NullSubclient instance.

        Args:
            agent_object: The agent object associated with this subclient.
            instance_name: The name of the instance for the subclient.
            instance_id: Optional; the unique identifier for the instance. Defaults to None.

        Example:
            >>> agent = Agent()
            >>> null_subclient = NullSubclient(agent, "TestInstance", 101)
            >>> print(f"NullSubclient created for instance: {null_subclient}")

        #ai-gen-doc
        """
        raise SDKException('Instance', '102',
                           'Instance: "{0}" is not yet supported'.
                           format(instance_name))
