#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on Commcell via REST API.

Commcell is the main class for the CVPySDK python package.

Commcell: Initializes a connection to the commcell and is a wrapper for the entire commcell ops.

Commcell:
    __init__(commcell_name,
             port=81,
             commcell_username,
             commcell_password)  --  initialise object of the Commcell class
    __enter__()                  --  returns the current instance, using the "with" context manager
    __exit__()                   --  logs out the user associated with the current instance
    __del__()                    --  logs out the user associated with the current instance
    __repr__()                   --  return the name of the commcell, user is connected to,
                                        along with the user name of the connected user.
    _update_response_()          --  returns only the relevant response for the response received
                                        from the server.
    _remove_attribs_()           --  removes all the attributs associated with the commcell
                                        object upon logout.
    logout()                     --  logs out the user associated with the current instance

"""

import base64

from services import ApiLibrary
from cvpysdk import CVPySDK
from client import Clients
from alert import Alerts
from storage import MediaAgents
from storage import DiskLibraries
from storage import StoragePolicies
from exception import SDKException


class Commcell(object):
    """Class for creating a session to the commcell via rest api."""

    def __init__(self, commcell_name, commcell_username='', commcell_password='', port=81):
        """Initialize the Commcell object with the values required for doing the api operations.

            Args:
                commcell_name (str) - name of the server; name@domain.com
                port (int) - port, the server is reachable at
                    default: 81
                commcell_username (str) - username of the user to log in to commserver
                    default: ''
                commcell_password (str) - plain text / base64 encrypted password to log in
                    default: ''

            Returns:
                object - instance of this class

            Raises:
                SDKException:
                    if the web service is down or not reachable
                    if not token is received upon log in
        """
        self._commcell_service = r'http://{0}:{1}/SearchSvc/CVWebService.svc/'
        self._commcell_service = self._commcell_service.format(commcell_name, port)

        self._user = commcell_username

        try:
            # Checks if the password is base 64 encoded or not
            base64.decodestring(commcell_password)
            self._password = commcell_password
        except:
            # encodes the plain text password using base64 encoding
            self._password = base64.b64encode(commcell_password)

        self._headers = {
            'Host': commcell_name,
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authtoken': None
        }

        self._cvpysdk_object = CVPySDK(self)

        # Checks if the service is running or not
        if not self._cvpysdk_object._is_valid_service_():
            self._commcell_service = r'http://{0}/webconsole/api/'.format(commcell_name)
            if not self._cvpysdk_object._is_valid_service_():
                raise SDKException('Commcell', '101')

        # Initialize all the services with this commcell service
        self._services = ApiLibrary(self._commcell_service)

        # Login to the commcell with the credentials provided and store the token in the headers.
        self._headers['Authtoken'], self.__user_guid = self._cvpysdk_object._login_()

        if not self._headers['Authtoken']:
            raise SDKException('CVPySDK', '101')

        commcell_entities = [
            Clients(self),
            Alerts(self),
            MediaAgents(self),
            DiskLibraries(self),
            StoragePolicies(self)
        ]

        self.clients, self.alerts, \
            self.media_agents, self.disk_libraries, self.storage_policies = commcell_entities

    def __enter__(self):
        """Returns the current instance.

            Returns:
                object - the initialized instance referred by self
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Logs out the user associated with the current instance."""
        print self._cvpysdk_object._logout_()
        self._remove_attribs_()

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string about the details of the Commcell class instance
        """
        representation_string = 'Commcell instance for Commcell: "{0}", for User: "{1}"'
        return representation_string.format(self._headers['Host'], self._user)

    def _update_response_(self, input_string):
        """Returns only the relevant response from the response received from the server.

            Args:
                input_string (str) - input string to retrieve the relevant response from

            Returns:
                str - final response to be used
        """
        if '<title>' in input_string and '</title>' in input_string:
            response_string = str(input_string).split("<title>")[1]
            response_string = response_string.split("</title>")[0]
            return response_string
        else:
            return input_string

    def _remove_attribs_(self):
        """Removes all the attributes associated with the instance of this class."""
        del self.clients
        del self.disk_libraries
        del self.media_agents
        del self.storage_policies
        del self.__user_guid
        del self._commcell_service
        del self._cvpysdk_object
        del self._password
        del self._services
        del self

    def logout(self):
        """Logs out the user associated with the current instance."""
        if self._headers['Authtoken'] is None:
            print 'User already logged out.'
        else:
            print self._cvpysdk_object._logout_()
            self._remove_attribs_()
