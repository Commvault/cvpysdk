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
from typing import TYPE_CHECKING

from .policies.configuration_policies import ConfigurationPolicies
from .policies.storage_policies import StoragePolicies
from .policies.schedule_policies import SchedulePolicies

if TYPE_CHECKING:
    from .commcell import Commcell


class Policies:
    """Class for getting all the policies associated with the commcell.

    Description:
        This class provides access to different types of policies associated with the Commcell,
        such as configuration policies, storage policies, and schedule policies.

    Attributes:
        _commcell_object (object): Instance of the Commcell class.
        _configuration_policies (ConfigurationPolicies): Instance of ConfigurationPolicies class.
        _storage_policies (StoragePolicies): Instance of StoragePolicies class.
        _schedule_policies (SchedulePolicies): Instance of SchedulePolicies class.

    Usage:
        >>> policies = Policies(commcell_object)

    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize object of the Policies class.

        Args:
            commcell_object (object): Instance of the Commcell class.

        Returns:
            None

        """
        self._commcell_object = commcell_object
        self._configuration_policies = None
        self._storage_policies = None
        self._schedule_policies = None
        self.refresh()

    def __repr__(self) -> str:
        """Representation string for the instance of the Policies class.

        Returns:
            str: String representation of the Policies class instance.

        """
        return "Policies class instance for Commcell"

    def refresh(self) -> None:
        """Refresh all the Policies associated with the Commcell.

        Returns:
            None

        """
        self._configuration_policies = None
        self._storage_policies = None
        self._schedule_policies = None

    @property
    def configuration_policies(self) -> ConfigurationPolicies:
        """Returns the instance of the ConfigurationPolicies class.

        Returns:
            ConfigurationPolicies: Instance of the ConfigurationPolicies class.

        Usage:
            >>> config_policies = policies.configuration_policies

        """
        if self._configuration_policies is None:
            self._configuration_policies = ConfigurationPolicies(
                self._commcell_object)

        return self._configuration_policies

    @property
    def storage_policies(self) -> StoragePolicies:
        """Returns the instance of the StoragePolicies class.

        Returns:
            StoragePolicies: Instance of the StoragePolicies class.

        Usage:
            >>> storage_policies = policies.storage_policies

        """
        if self._storage_policies is None:
            self._storage_policies = StoragePolicies(self._commcell_object)

        return self._storage_policies

    @property
    def schedule_policies(self) -> SchedulePolicies:
        """Returns the instance of the SchedulePolicies class.

        Returns:
            SchedulePolicies: Instance of the SchedulePolicies class.

        Usage:
            >>> schedule_policies = policies.schedule_policies

        """
        if self._schedule_policies is None:
            self._schedule_policies = SchedulePolicies(self._commcell_object)

        return self._schedule_policies
