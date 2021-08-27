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

"""File for operating on a Dynamics 365 CRM Subclient.

MSDynamics365Subclient is the only class defined in this file.

MSDynamics365Subclient:    Derived class from CloudAppsSubclient Base class, representing a
                            Dynamics 365 subclient, and to perform operations on that subclient

MSDynamics365Subclient:

    _get_subclient_properties()         --  gets the properties of Google Subclient

    _get_subclient_properties_json()    --  gets the properties JSON of Google Subclient

"""

from ...exception import SDKException

from ..casubclient import CloudAppsSubclient

class MSDynamics365Subclient(CloudAppsSubclient):
    """Derived class from CloudAppsSubclient Base class, representing a MSDynamics365 subclient"""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of a Dynamics 365 subclient.."""
        super(MSDynamics365Subclient, self)._get_subclient_properties()

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """

        return {'subClientProperties': self._subclient_properties}
