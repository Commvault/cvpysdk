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

"""File for operating on a Hadoop instance.

HadoopInstance: Derived class from BigDataAppsInstance base class, representing a
Hadoop instance and to perform operations on that instance.
    __init__()                      --  Initializes hadoop instance object with associated
        agent_object, instance name and instance id
    restore()                       -- Submits a restore request based on restore options
"""

from __future__ import unicode_literals

from typing import TYPE_CHECKING

from ...exception import SDKException
from ..bigdataappsinstance import BigDataAppsInstance

if TYPE_CHECKING:
    from ...job import Job


class HadoopInstance(BigDataAppsInstance):
    """Represents a Hadoop instance in Big Data Apps."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes Hadoop instance object with associated agent object, name and id."""
        self._agent_object = agent_object
        self._browse_request = {}
        self._browse_url = None
        super(HadoopInstance, self).__init__(agent_object, instance_name, instance_id)