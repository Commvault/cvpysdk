# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing storage related operations on the commcell.

This file has all the classes related to Schedule Policy operations.

SchedulePolicies: Class for representing all the Schedule Policies associated to the commcell.


SchedulePolicies:
    __init__(commcell_object)    --  initialize the SchedulePolicies instance for the commcell

    __str__()                    --  returns all the schedule policies associated with the commcell

    __repr__()                   --  returns a string for instance of the SchedulePolicies class

    _get_policies()              --  gets all the schedule policies of the commcell

    all_schedule_policies()      --  returns the dict of all the schedule policies on commcell

    has_policy(policy_name)      --  checks if a schedule policy exists with the given name

    refresh()                    --  refresh the schedule policies associated with the commcell


"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode

from past.builtins import basestring
from future.standard_library import install_aliases

from ..exception import SDKException
from ..job import Job

install_aliases()


class SchedulePolicies(object):
    """Class for getting all the schedule policies associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the SchedulePolicies class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the SchedulePolicies class
        """
        self._commcell_object = commcell_object
        self._POLICY = self._commcell_object._services['SCHEDULE_POLICY']

        self._policies = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all schedule policies of the commcell.

            Returns:
                str - string of all the schedule policies associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'Schedule Policy')

        for index, policy in enumerate(self._policies):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, policy)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Representation string for the instance of the SchedulePolicies class."""
        return "SchedulePolicies class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_policies(self):
        """Gets all the schedule policies associated to the commcell specified by commcell object.

            Returns:
                dict - consists of all schedule policies of the commcell
                    {
                         "schedule_policy1_name": schedule_policy1_id,
                         "schedule_policy2_name": schedule_policy2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request('GET', self._POLICY)

        if flag:
            if response.json() and 'taskDetail' in response.json():
                policies = response.json()['taskDetail']
                policies_dict = {}

                for policy in policies:
                    temp_name = policy['task']['taskName'].lower()
                    temp_id = str(policy['task']['taskId']).lower()
                    policies_dict[temp_name] = temp_id

                return policies_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_schedule_policies(self):
        """Returns the schedule policies on this commcell

            dict - consists of all schedule policies of the commcell
                    {
                         "schedule_policy1_name": schedule_policy1_id,
                         "schedule_policy2_name": schedule_policy2_id
                    }
        """
        return self._policies

    def has_policy(self, policy_name):
        """Checks if a schedule policy exists in the commcell with the input schedule policy name.

            Args:
                policy_name (str)  --  name of the schedule policy

            Returns:
                bool - boolean output whether the schedule policy exists in the commcell or not

            Raises:
                SDKException:
                    if type of the schedule policy name argument is not string
        """
        if not isinstance(policy_name, basestring):
            raise SDKException('Storage', '101')

        return self._policies and policy_name.lower() in self._policies

    def refresh(self):
        """Refresh the Schedule Policies associated with the Commcell."""
        self._policies = self._get_policies()
