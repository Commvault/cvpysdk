# -*- coding: utf-8 -*-
# ————————————————————————–
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
# ————————————————————————–

"""File for operating on a power Platform Power Bi subclient

PowerBISubclient is the only class defined in this file.

PowerBISubclient: Derived class from Subclient Base class, representing a Platform Power Bi subclient,
and to perform operations on that subclient

PowerBISubclient:
    _json_subclient_entity()    --  Get subclientEntity json for power bi association operation
"""

from __future__ import unicode_literals
import base64
from copy import copy, deepcopy
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from ...exception import SDKException
from ..casubclient import CloudAppsSubclient
from ..cloudapps.powerbi_constants import PowerBiConstants as const


class PowerBISubclient(CloudAppsSubclient):
    """
    Represents a Platform Power Bi subclient for managing backup, restore, and content operations.

    This class extends the CloudAppsSubclient to provide specialized functionality for Power Bi
    within the Power Platform suite. It enables discovery, backup, restore, and management of Power Bi data,
    including Power Bi associations, content handling, and advanced restore options.

    #ai-gen-doc
    """

    def _json_subclient_entity(self) -> dict:
        """Generate the subclientEntity JSON for Power Bi association operations.

        Returns:
            dict: A dictionary representing the subclientEntity JSON required for Power Bi association operations.

        Example:
            >>> powerbi_subclient = PowerBISubclient()
            >>> subclient_entity_json = powerbi_subclient._json_subclient_entity()
            >>> print(subclient_entity_json)
            # Output will be a dictionary suitable for Power Bi association API calls

        #ai-gen-doc
        """
        subclient_entity_json = copy(const.ADD_SUBCLIENT_ENTITY_JSON)
        subclient_entity_json['instanceId'] = int(self._instance_object.instance_id)
        subclient_entity_json['subclientId'] = int(self._subclient_id)
        subclient_entity_json['clientId'] = int(self._client_object.client_id)
        subclient_entity_json['applicationId'] = int(self._subClientEntity['applicationId'])
        return subclient_entity_json