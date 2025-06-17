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

"""File for operating on all types of Policies associated with the Commcell.

Policies:   Class for representing all types of Policies associated with the Commcell

"""

from __future__ import unicode_literals

from .exception import SDKException

from .policies.configuration_policies import ConfigurationPolicies
from .policies.storage_policies import StoragePolicies
from .policies.schedule_policies import SchedulePolicies


class Policies:
    """Class for getting all the all the policies associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Policies class.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the Policies class

        """
        self._commcell_object = commcell_object
        self.refresh()

    def __repr__(self):
        """Representation string for the instance of the Policies class."""
        return "Policies class instance for Commcell"

    def refresh(self):
        """Refresh all the Policies associated with the Commcell."""
        self._configuration_policies = None
        self._storage_policies = None
        self._schedule_policies = None

    @property
    def configuration_policies(self):
        """Returns the instance of the ConfigurationPolicies class."""
        if self._configuration_policies is None:
            self._configuration_policies = ConfigurationPolicies(self._commcell_object)

        return self._configuration_policies


    @property
    def storage_policies(self):
        """Returns the instance of the StoragePolicies class."""
        if self._storage_policies is None:
            self._storage_policies = StoragePolicies(self._commcell_object)

        return self._storage_policies


    @property
    def schedule_policies(self):
        """Returns the instance of the SchedulePolicies class."""
        if self._schedule_policies is None:
            self._schedule_policies = SchedulePolicies(self._commcell_object)

        return self._schedule_policies
