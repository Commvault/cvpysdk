#!/usr/bin/env python
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

from typing import Any, Dict

from .exception import SDKException

class ActivityControl(object):
    """
    Class for managing and controlling activity operations within a CommCell environment.

    The ActivityControl class provides an interface to perform various activity control operations,
    such as enabling, disabling, and scheduling activities with specific actions and time delays.
    It allows querying the status of activities, checking if an activity is enabled, and accessing
    properties related to re-enabling activities, including the time and time zone settings.

    Key Features:
        - Initialize with a CommCell object for context-specific activity control
        - Set activity actions (enable/disable) for specified activity types
        - Enable activities after a specified delay
        - Generate request JSON for activity control operations
        - Retrieve current activity control status
        - Check if a particular activity type is enabled
        - Access re-enable time and time zone properties

    #ai-gen-doc
    """

    def __init__(self, commcell_object) -> None:
        """Initialize an ActivityControl instance for managing activity controls in the Commcell.

        Args:
            commcell_object: Instance of the Commcell class representing the connected Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell(command_center_hostname, username, password)
            >>> activity_control = ActivityControl(commcell)
            >>> # The ActivityControl object can now be used to manage activity controls

        #ai-gen-doc
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

    def __repr__(self) -> str:
        """Return a string representation of the ActivityControl instance.

        Returns:
            A string indicating that this object is an instance of the ActivityControl class.

        Example:
            >>> activity_control = ActivityControl(...)
            >>> print(repr(activity_control))
            ActivityControl class instance

        #ai-gen-doc
        """
        representation_string = 'ActivityControl class instance'
        return representation_string

    def _request_json_(self, activity_type: str, enable_time: int) -> Dict[str, Any]:
        """Generate the JSON request payload for activity control API operations.

        Constructs a JSON dictionary based on the specified activity type and enable time,
        suitable for passing to the activity control API.

        Args:
            activity_type: The type of activity to control (e.g., 'Backup', 'Restore').
            enable_time: The time (as an integer, typically a Unix timestamp) when the activity should be enabled.

        Returns:
            Dictionary representing the JSON request to be sent to the API.

        Example:
            >>> activity_control = ActivityControl()
            >>> request_payload = activity_control._request_json_('Backup', 1712345678)
            >>> print(request_payload)
            {
                "commCellInfo": {
                    "commCellActivityControlInfo": {
                        "activityControlOptions": [
                            {
                                "activityType": ...,
                                "enableAfterADelay": True,
                                "enableActivityType": False,
                                "dateTime": {
                                    "time": 1712345678
                                }
                            }
                        ]
                    }
                }
            }
        #ai-gen-doc
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

    def set(self, activity_type: str, action: str) -> None:
        """Set the activity control status for a specific activity type on the Commcell.

        This method enables or disables a specified activity type on the Commcell, such as data management,
        data recovery, or scheduler activities.

        Args:
            activity_type: The type of activity to be enabled or disabled. Valid values include:
                "ALL ACTIVITY", "DATA MANAGEMENT", "DATA RECOVERY", "DATA AGING", "AUX COPY",
                "DATA VERIFICATION", "DDB ACTIVITY", "SCHEDULER", "OFFLINE CONTENT INDEXING".
            action: The action to perform on the activity type. Valid values are "Enable" or "Disable".

        Raises:
            SDKException: If the activity control could not be set, if the response is empty,
                or if the response indicates failure.

        Example:
            >>> activity_control = ActivityControl(commcell_object)
            >>> activity_control.set("DATA MANAGEMENT", "Enable")
            >>> # This will enable data management activity on the Commcell

        #ai-gen-doc
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

    def enable_after_delay(self, activity_type: str, enable_time: str) -> None:
        """Disable the specified activity if not already disabled, and enable it at the given time.

        This method schedules the enabling of a Commcell activity after a specified delay, using a Unix timestamp in UTC.
        If the activity is not already disabled, it will be disabled first, then enabled at the provided time.

        Args:
            activity_type: The type of activity to be enabled or disabled. Valid values include:
                "ALL ACTIVITY", "DATA MANAGEMENT", "DATA RECOVERY", "DATA AGING", "AUX COPY",
                "DATA VERIFICATION", "DDB ACTIVITY", "SCHEDULER", "OFFLINE CONTENT INDEXING".
            enable_time: The Unix timestamp (as a string) in UTC timezone when the activity should be enabled.

        Raises:
            SDKException: If enabling the activity control after the specified time fails,
                if the response is empty, or if the response indicates failure.

        Example:
            >>> activity_control = ActivityControl(commcell_object)
            >>> # Schedule enabling 'DATA MANAGEMENT' activity at a specific UTC timestamp
            >>> activity_control.enable_after_delay("DATA MANAGEMENT", "1712345678")
            >>> print("Activity scheduled for enablement after delay.")
        #ai-gen-doc
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

    def _get_activity_control_status(self) -> None:
        """Retrieve and update the activity control status for the Commcell.

        This method sends a GET request to the Commcell to obtain the current activity control status.
        The retrieved status is stored in the internal activity control properties list.

        Raises:
            SDKException: If the response from the Commcell is empty or indicates a failure.

        Example:
            >>> activity_control = ActivityControl(commcell_object)
            >>> activity_control._get_activity_control_status()
            >>> # The activity control properties are now updated internally

        #ai-gen-doc
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

    def is_enabled(self, activity_type: str) -> bool:
        """Check if a specific activity type is enabled and update related properties.

        This method verifies whether the specified activity type is currently enabled.
        It also updates internal properties such as re-enable time, scheduling status,
        and time zone for the activity. If the activity type is not found, an SDKException
        is raised.

        Args:
            activity_type: The name of the activity type to check. Supported values include:
                - "ALL ACTIVITY"
                - "DATA MANAGEMENT"
                - "DATA RECOVERY"
                - "DATA AGING"
                - "AUX COPY"
                - "DATA VERIFICATION"
                - "DDB ACTIVITY"
                - "SCHEDULER"
                - "OFFLINE CONTENT INDEXING"

        Returns:
            True if the activity type is enabled, False otherwise.

        Raises:
            SDKException: If the specified activity type is not found.

        Example:
            >>> activity_control = ActivityControl(...)
            >>> is_data_management_enabled = activity_control.is_enabled("DATA MANAGEMENT")
            >>> print(f"Data Management Enabled: {is_data_management_enabled}")
            >>> # Internal properties such as reEnableTime and noSchedEnable are updated after this call

        #ai-gen-doc
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
    def reEnableTime(self) -> str:
        """Get the reEnableTime value as a read-only property.

        Returns:
            The reEnableTime value as a string, representing the time when the activity can be re-enabled.

        Example:
            >>> activity_control = ActivityControl(...)
            >>> time = activity_control.reEnableTime  # Use dot notation for property access
            >>> print(f"Re-enable time: {time}")

        #ai-gen-doc
        """
        return self._reEnableTime

    @property
    def reEnableTimeZone(self) -> bool:
        """Get the value of the reEnableTimeZone attribute.

        This property provides read-only access to the reEnableTimeZone flag, which indicates
        whether the time zone re-enablement feature is active for the current ActivityControl instance.

        Returns:
            True if time zone re-enablement is enabled, False otherwise.

        Example:
            >>> activity_control = ActivityControl(...)
            >>> is_enabled = activity_control.reEnableTimeZone  # Use dot notation for property access
            >>> print(f"Time zone re-enablement enabled: {is_enabled}")

        #ai-gen-doc
        """
        return self._reenableTimeZone
