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

"""Main file for performing Event Viewer Operations

Events and Event are 2 classes defined in this file

Events: Class for representing all the Events associated with the commcell

Event: Class for a single Event of the commcell


Events:
    __init__(commcell_object) --  initialise object of Clients
                                  class associated with the commcell

    __str__()                 --  returns all the Events
                                  associated with the commcell

    __repr__()                --  returns the string to represent
                                  the instance of the Events class.

    events()    --  gets all the Events associated with the commcell

    get(event_id)         --  returns the Event class object of the input event id


Event:
    __init__(commcell_object)     --  initialise object of
                                      Class associated to the commcell

    __repr__()                   --  return the Event id,
                                     the instance is associated with

    _get_event_properties()      --  method to get the Event id,
                                     if not specified in __init__

    **event_code**        --  returns the event code associated to the event id
    **job_id**           --  returns the job id associated to the event id
    is_backup_disabled    -- boolean specifying if backup is disabled or not
    is_restore_disabled    -- boolean specifying if restore is disabled or not

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .exception import SDKException

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cvpysdk.commcell import Commcell


class Events(object):
    """
    Class for managing and representing Events associated with the commcell.

    This class provides an interface to interact with event data within a commcell environment.
    It allows querying for events based on specific parameters, retrieving detailed information
    about particular events, and offers string representations for easy inspection and debugging.

    Key Features:
        - Initialize with a commcell object to establish context
        - Query and retrieve lists of events using customizable parameters
        - Fetch detailed information for a specific event by event ID
        - Provides string and representation methods for user-friendly output

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize an instance of the Events class.

        Args:
            commcell_object: An instance of the Commcell class used to interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> events = Events(commcell)
            >>> print("Events object created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._events = self.events()

    def __str__(self) -> str:
        """Return a string representation of all events associated with the Commcell.

        This method provides a human-readable summary of all events managed by the Events object.

        Returns:
            A string containing details of all events associated with the Commcell.

        #ai-gen-doc
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'EventId')

        for index, event in enumerate(self._events):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, event)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self) -> str:
        """Return the string representation of the Events instance.

        This method provides a developer-friendly string that represents the current
        Events object, which can be useful for debugging and logging purposes.

        Returns:
            A string representation of the Events instance.

        #ai-gen-doc
        """
        representation_string = 'Events class instance'
        return representation_string

    def events(self, query_params_dict: dict = None, details: bool = False) -> dict:
        """Retrieve all events associated with the Commcell.

        Args:
            query_params_dict: Optional dictionary of query parameters to filter events.

            details: If True, returns complete details for each event; if False, returns only event codes.

        Returns:
            Dictionary containing all events in the Commcell. The keys are event IDs, and the values are either event codes or detailed event dictionaries, depending on the 'details' parameter.
                Example:
                    {
                        "event1_id": 1001,
                        "event2_id": {
                            "code": 1002,
                            "description": "Backup completed successfully",
                            ...
                        }
                    }

        Raises:
            SDKException: If the response is empty or not successful.

        Example:
            >>> events_obj = Events()
            >>> all_events = events_obj.events({
            >>>    "jobId": 123
            >>> })
            >>> print(f"Total events: {len(all_events)}")
            >>> # Retrieve detailed event information
            >>> detailed_events = events_obj.events(details=True)
            >>> print(detailed_events)

        #ai-gen-doc
        """
        events_request = self._commcell_object._services['GET_EVENTS']
        if query_params_dict:
            events_request = events_request + '?'
            for query_param in query_params_dict.keys():
                if events_request[-1] != '?':
                    events_request = events_request + '&'
                events_request = events_request + query_param + \
                    '=' + query_params_dict[query_param]

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', events_request)

        if flag:
            if response.json() and 'commservEvents' in response.json():
                events_dict = {}

                for dictionary in response.json()['commservEvents']:
                    event_id = dictionary['id']
                    event_code = dictionary['eventCode']
                    if details:
                        event_details = dictionary.copy()
                        del event_details['id']
                        events_dict[event_id] = event_details
                    else:
                        events_dict[event_id] = event_code

                return events_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, event_id: int) -> 'Event':
        """Retrieve an Event object by its unique event ID.

        Args:
            event_id: The unique identifier of the event to retrieve.

        Returns:
            Event: An instance of the Event class corresponding to the provided event ID.

        #ai-gen-doc
        """
        return Event(self._commcell_object, event_id)


class Event(object):
    """
    Class for managing and viewing event operations within the Event Viewer.

    This class encapsulates the properties and behaviors associated with an event,
    providing access to event details and status flags. It is initialized with a
    commcell object and an event ID, allowing retrieval and representation of event
    properties.

    Key Features:
        - Initialization with commcell object and event ID
        - String representation of the event instance
        - Retrieval of event properties
        - Access to event code via property
        - Access to associated job ID via property
        - Flags indicating if backup is disabled (is_backup_disabled)
        - Flags indicating if restore is disabled (is_restore_disabled)

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', event_id: int) -> None:
        """Initialize an instance of the Event class for a specific event.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            event_id: The unique identifier for the event to be managed or viewed.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> event = Event(commcell, 1234)
            >>> print(f"Event object created for event ID: {event_id}")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._event_id = event_id
        self._event = self._commcell_object._services['GET_EVENT'] % (
            self._event_id)
        self._get_event_properties()
        self._event_code_type_dict = {
            "BACKUP DISABLED": "318767861",
            "RESTORE DISABLED": "318767864",
        }

    def __repr__(self) -> str:
        """Return the string representation of the Event instance.

        This method provides a developer-friendly string that can be used to inspect
        the Event object in logs or interactive sessions.

        Returns:
            A string representing the Event instance.

        #ai-gen-doc
        """
        representation_string = 'Event class instance for Event: "{0}"'
        return representation_string.format(self._event_id)

    def _get_event_properties(self) -> None:
        """Retrieve the properties of this event as a dictionary.

        Returns:
            None

        Raises:
            SDKException: If the response is empty or if the response indicates a failure.

        #ai-gen-doc
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._event)

        if flag:
            if response.json() and 'commservEvents' in response.json():
                self._properties = response.json()['commservEvents'][0]

                self._eventcode = self._properties['eventCode']
                self._timeSource = self._properties['timeSource']
                self._severity = self._properties['severity']
                self._job_id = self._properties['jobId']
                self._description = self._properties['description']
                self._subsystem = self._properties['subsystem']
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def event_code(self) -> int:
        """Get the event code associated with this Event instance as a read-only attribute.

        Returns:
            The event code as an integer.

        Example:
            >>> event = Event()
            >>> code = event.event_code  # Access the event code property
            >>> print(f"Event code: {code}")

        #ai-gen-doc
        """
        return self._eventcode

    @property
    def job_id(self) -> int:
        """Get the job ID associated with this event as a read-only property.

        Returns:
            The job ID as an integer.

        Example:
            >>> event = Event()
            >>> job_identifier = event.job_id  # Access the job ID property
            >>> print(f"Job ID: {job_identifier}")

        #ai-gen-doc
        """
        return self._job_id

    @property
    def is_backup_disabled(self) -> bool:
        """Indicate whether backup is disabled based on the event type.

        Returns:
            True if the event type corresponds to a backup-disabled state, otherwise False.

        Example:
            >>> event = Event()
            >>> if event.is_backup_disabled:
            ...     print("Backup is currently disabled for this event.")
            ... else:
            ...     print("Backup is enabled for this event.")

        #ai-gen-doc
        """
        if self._event_code_type_dict["BACKUP DISABLED"] == self._eventcode:
            return True
        else:
            return False

    @property
    def is_restore_disabled(self) -> bool:
        """Indicate whether restore operations are disabled for this event type.

        Returns:
            True if restore operations are disabled for the event type, False otherwise.

        Example:
            >>> event = Event()
            >>> if event.is_restore_disabled:
            ...     print("Restore is disabled for this event type.")
            ... else:
            ...     print("Restore is allowed for this event type.")

        #ai-gen-doc
        """
        if self._event_code_type_dict["RESTORE DISABLED"] == self._eventcode:
            return True
        else:
            return False
