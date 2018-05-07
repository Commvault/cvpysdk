#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing activity control operations

Activity Control is the only class defined in this file.

ActivityControl: Class for managing Activity Control enable/disable
                    for various entities within the comcell.

ActivityControl:
    __init__(commcell_object) -- initialise object of Class associated to the commcell

    __repr__()               --  String representation of the instance of this class.

    set()                       --  method to set activity control.

    enable_after_delay()   -- method to disable activity control and set a delay time.

    _get_activity_control_status()   -- method to get activity control status

    is_enabled()          --  boolean specifying if a given activity is enabled or not
    **reEnableTime**                --  returns the Enable back time
    **reEnableTimeZone**                --  returns the Enable back time zone

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .exception import SDKException


class ActivityControl(object):
    """Class for performing activity control operations."""

    def __init__(self, commcell_object):
        """Initialise the Activity control class instance.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the ActivityControl class
        """

        self._commcell_object = commcell_object
        self._activity_type_dict = {
            "ALL ACTIVITY": 128,
            "DATA MANAGEMENT": 1,
            "DATA RECOVERY": 2,
            "DATA AGING": 16,
            "AUX COPY": 4,
            "DATA VERIFICATION": 8192,
            "DDB ACTIVITY": 512,
            "SCHEDULER": 256,
            "OFFLINE CONTENT INDEXING": 1024,
        }
        self._get_activity_control_status()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'ActivityControl class instance'
        return representation_string

    def _request_json_(self, activity_type, enable_time):
        """Returns the JSON request to pass to the API
            as per the options selected by the user.

            Returns:
                dict - JSON request to pass to the API
        """

        request_json = {
            "commCellInfo": {
                "commCellActivityControlInfo": {
                    "activityControlOptions": [
                        {
                            "activityType": self._activity_type_dict[activity_type],
                            "enableAfterADelay": True,
                            "enableActivityType": False,
                            "dateTime": {
                                "time": enable_time}}]}}}

        return request_json

    def set(self, activity_type, action):
        """Sets activity control on Commcell.

            Args:
                activity_type (str)  --  Activity Type to be Enabled or Disabled
                Values:
                    "ALL ACTIVITY",
                    "DATA MANAGEMENT",
                    "DATA RECOVERY",
                    "DATA AGING",
                    "AUX COPY",
                    "DATA VERIFICATION",
                    "DDB ACTIVITY",
                    "SCHEDULER",
                    "OFFLINE CONTENT INDEXING",

                action (str)    --    Enable or Disable
                Values:
                    Enable
                    Disable
            Raises:
                SDKException:
                    if failed to set

                    if response is empty

                    if response is not success
        """
        set_request = self._commcell_object._services['SET_ACTIVITY_CONTROL'] % (
            str(self._activity_type_dict[activity_type]), str(action))
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', set_request
        )

        if flag:
            if response.json():
                error_code = str(response.json()['errorCode'])
                if error_code == '0':
                    self._get_activity_control_status()
                    return
                else:
                    raise SDKException(
                        'CVPySDK', '102', response.json()['errorMessage'])
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def enable_after_delay(self, activity_type, enable_time):
        """Disables activity if not already disabled
            and enables at the time specified.

            Args:
                activity_type (str)  --  Activity Type to be Enabled or Disabled
                Values:
                    "ALL ACTIVITY",
                    "DATA MANAGEMENT",
                    "DATA RECOVERY",
                    "DATA AGING",
                    "AUX COPY",
                    "DATA VERIFICATION",
                    "DDB ACTIVITY",
                    "SCHEDULER",
                    "OFFLINE CONTENT INDEXING",

                enable_time (str)-- Unix Timestamp in UTC timezone
            Raises:
                SDKException:
                    if failed to enable activity control after a time

                    if response is empty

                    if response is not success
        """
        request_json = self._request_json_(activity_type, enable_time)

        set_request = self._commcell_object._services['SET_COMMCELL_PROPERTIES']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'PUT', set_request, request_json
        )

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response'][0]['errorCode']

                if error_code == 0:
                    self._get_activity_control_status()
                    return
                elif 'errorMessage' in response.json()['response'][0]:
                    error_message = response.json(
                    )['response'][0]['errorMessage']

                    o_str = 'Failed to enable activity control \
                                after a delay\nError: "{0}"'.format(
                                    error_message)
                    raise SDKException('CVPySDK', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _get_activity_control_status(self):
        """Gets the activity control status

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        get_request = self._commcell_object._services['GET_ACTIVITY_CONTROL']
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', get_request
        )

        if flag:
            if response.json() and 'acObjects' in response.json():
                self._activity_control_properties_list = response.json()[
                    'acObjects']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def is_enabled(self, activity_type):
        """Returns True/False based on the enabled flag and also sets
                     other relevant properties for a given activity type.

            Args:
                activity_type (str)  --  Activity Type to be Enabled or Disabled
                Values:
                    "ALL ACTIVITY",
                    "DATA MANAGEMENT",
                    "DATA RECOVERY",
                    "DATA AGING",
                    "AUX COPY",
                    "DATA VERIFICATION",
                    "DDB ACTIVITY",
                    "SCHEDULER",
                    "OFFLINE CONTENT INDEXING",
        """
        self._get_activity_control_status()
        for each_activity in self._activity_control_properties_list:
            if int(each_activity['activityType']) == \
                    self._activity_type_dict[activity_type]:
                self._reEnableTime = each_activity['reEnableTime']
                self._noSchedEnable = each_activity['noSchedEnable']
                self._reenableTimeZone = each_activity['reenableTimeZone']
                return each_activity['enabled']

        o_str = 'Failed to find activity type:"{0}" in the response'.format(
            activity_type)
        raise SDKException('Client', '102', o_str)

    @property
    def reEnableTime(self):
        """Treats the reEnableTime as a read-only attribute."""
        return self._reEnableTime

    @property
    def reEnableTimeZone(self):
        """Treats the reEnableTimeZone as a read-only attribute."""
        return self._reenableTimeZone
