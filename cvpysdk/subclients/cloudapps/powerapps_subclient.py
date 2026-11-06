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

"""File for operating on a Power Apps subclient.

PowerAppsSubclient is the only class defined in this file.

PowerAppsSubclient: Derived class from Subclient Base class, representing a Platform Power Apps subclient,
and to perform operations on that subclient.

PowerAppsSubclient:
    _json_subclient_entity()    --  Get subclientEntity json for Power Apps association operation
"""

from __future__ import unicode_literals
from copy import copy

from ..casubclient import CloudAppsSubclient
from ..cloudapps.powerapps_constants import PowerAppsConstants as const


class PowerAppsSubclient(CloudAppsSubclient):
    """
    Represents a Power Platform Power Apps subclient for managing backup and association operations.

    This class extends the CloudAppsSubclient to provide specialized functionality for Power Apps.

    #ai-gen-doc
    """

    def _json_subclient_entity(self) -> dict:
        """Generate the subclientEntity JSON for Power Apps association operations.

        Returns:
            dict: A dictionary representing the subclientEntity JSON required for Power Apps association operations.

        Example:
            >>> powerapps_subclient = PowerAppsSubclient()
            >>> subclient_entity_json = powerapps_subclient._json_subclient_entity()
            >>> print(subclient_entity_json)
            # Output will be a dictionary suitable for Power Apps association API calls

        #ai-gen-doc
        """
        subclient_entity_json = copy(const.ADD_SUBCLIENT_ENTITY_JSON)
        subclient_entity_json['instanceId'] = int(self._instance_object.instance_id)
        subclient_entity_json['subclientId'] = int(self._subclient_id)
        subclient_entity_json['clientId'] = int(self._client_object.client_id)
        subclient_entity_json['applicationId'] = int(self._subClientEntity['applicationId'])
        return subclient_entity_json