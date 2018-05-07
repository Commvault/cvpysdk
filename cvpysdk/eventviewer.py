#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
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


class Events(object):
    """Class for representing Events associated with the commcell."""

    def __init__(self, commcell_object):
        """Initialize object of the Events class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Events class
        """
        self._commcell_object = commcell_object
        self._events = self.events()

    def __str__(self):
        """Representation string consisting of all events of the commcell.

            Returns:
                str - string of all the events associated with the commcell
        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'EventId')

        for index, event in enumerate(self._events):
            sub_str = '{:^5}\t{:20}\n'.format(index + 1, event)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Events class instance'
        return representation_string

    def events(self, query_params_dict={}):
        """Gets all the events associated with the commcell

            Args:
                query_params_dict (dict)  --  Query Params Dict
                    Example:
                        {
                            "jobId": 123,
                        }
            Returns:
                dict - consists of all events in the commcell
                    {
                         "event1_id": event1_code,
                         "event2_id": event2_code
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
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
                    events_dict[event_id] = event_code

                return events_dict
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def get(self, event_id):
        """Returns an event object

            Args:
                event_id (str)  --  Id of the Event

            Returns:
                object - instance of the Event class for the given Event Id
        """
        return Event(self._commcell_object, event_id)


class Event(object):
    """Class for Event Viewer operations."""

    def __init__(self, commcell_object, event_id):
        """Initialize the Event Viewer class instance.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Event class
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

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Event class instance for Event: "{0}"'
        return representation_string.format(self._event_id)

    def _get_event_properties(self):
        """Gets the event properties of this event.

            Returns:
                dict - dictionary consisting of the properties of this event

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
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
    def event_code(self):
        """Treats the event code as a read-only attribute."""
        return self._eventcode

    @property
    def job_id(self):
        """Treats the job id as a read-only attribute."""
        return self._job_id

    @property
    def is_backup_disabled(self):
        """Returns True/False based on the event type"""
        if self._event_code_type_dict["BACKUP DISABLED"] == self._eventcode:
            return True
        else:
            return False

    @property
    def is_restore_disabled(self):
        """Returns True/False based on the event type"""
        if self._event_code_type_dict["RESTORE DISABLED"] == self._eventcode:
            return True
        else:
            return False
