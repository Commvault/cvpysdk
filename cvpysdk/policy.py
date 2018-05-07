# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on all types of Policies associated with the Commcell.

Policies:   Class for representing all types of Policies associated with the Commcell

"""

from __future__ import unicode_literals

from .exception import SDKException

from .policies.configuration_policies import ConfigurationPolicies


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
        return "Policies class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def refresh(self):
        """Refresh all the Policies associated with the Commcell."""
        self._configuration_policies = None

    @property
    def configuration_policies(self):
        """Returns the instance of the ConfigurationPolicies class."""
        try:
            if self._configuration_policies is None:
                self._configuration_policies = ConfigurationPolicies(self._commcell_object)

            return self._configuration_policies
        except SDKException:
            return None
