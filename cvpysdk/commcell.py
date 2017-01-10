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
             commcell_username,
             commcell_password,
             port=81)            --  initialise object of the Commcell class
    __repr__()                   --  return the name of the commcell, user is connected to,
                                        along with the user name of the connected user
    __enter__()                  --  returns the current instance, using the "with" context manager
    __exit__()                   --  logs out the user associated with the current instance
    _attribs_()                  --  initializes the objects of the classes given in the input list
    _init_attrib_()              --  initializes the object of the class given as input and stores
                                        in the given input dictionary with class name as key
    _update_response_()          --  returns only the relevant response for the response received
                                        from the server.
    _remove_attribs_()           --  removes all the attributs associated with the commcell
                                        object upon logout.
    logout()                     --  logs out the user associated with the current instance
    request()                    --  runs a input HTTP request on the API specified,
                                        and returns its response

"""

from base64 import b64encode
from Queue import Queue
from threading import Thread

from services import ApiLibrary
from cvpysdk import CVPySDK
from client import Clients
from alert import Alerts
from storage import MediaAgents
from storage import DiskLibraries
from storage import StoragePolicies
from storage import SchedulePolicies
from usergroup import UserGroups
from workflow import WorkFlow
from exception import SDKException


class Commcell(object):
    """Class for creating a session to the commcell via rest api."""

    def __init__(self, commcell_name, commcell_username='', commcell_password='', port=81):
        """Initialize the Commcell object with the values required for doing the api operations.

            Args:
                commcell_name (str)      --  name of the server; name@domain.com
                commcell_username (str)  --  username of the user to log in to webconsole
                    default: ''
                commcell_password (str)  --  plain text password to log in to webconsole
                    default: ''
                port (int)               --  port, the server is reachable at
                    default: 81

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

        # encodes the plain text password using base64 encoding
        self._password = b64encode(commcell_password)

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

        sdk_classes = [Clients, Alerts, MediaAgents, DiskLibraries, StoragePolicies,
                       SchedulePolicies, UserGroups, WorkFlow]

        sdk_dict = self._attribs_(sdk_classes)

        self.clients = sdk_dict[Clients]
        self.alerts = sdk_dict[Alerts]
        self.media_agents = sdk_dict[MediaAgents]
        self.disk_libraries = sdk_dict[DiskLibraries]
        self.storage_policies = sdk_dict[StoragePolicies]
        self.schedule_policies = sdk_dict[SchedulePolicies]
        self.user_groups = sdk_dict[UserGroups]
        self.workflows = sdk_dict[WorkFlow]

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string about the details of the Commcell class instance
        """
        representation_string = 'Commcell class instance of Commcell: "{0}", for User: "{1}"'
        return representation_string.format(self._headers['Host'], self._user)

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

    def _attribs_(self, sdk_classes):
        """Initializes the objects of the classes in the sdk_classes list given as input.

            Args:
                sdk_classes (list)  --  list containing the classes to initialize the object of

            Returns:
                dict - dict consisting of the class name as key and the class object as its value
        """
        sdk_dict = {}

        self._queue = Queue()

        for sdk_class in sdk_classes:
            thread = Thread(target=self._init_attrib_, args=(sdk_class, sdk_dict))
            thread.start()
            self._queue.put(thread)

        self._queue.join()

        return sdk_dict

    def _init_attrib_(self, sdk_class, sdk_dict):
        """Initializes the object of the sdk_class given as input, and stores it
            with the class name as the key to the sdk_dict.

            Args:
                sdk_class (class)  --  sdk class to initialize the object of
                sdk_dict  (dict)   --  dict to store the class object as value,
                                        with the class name as key
        """
        sdk_dict[sdk_class] = sdk_class(self)
        self._queue.task_done()

    def _update_response_(self, input_string):
        """Returns only the relevant response from the response received from the server.

            Args:
                input_string (str)  --  input string to retrieve the relevant response from

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
        del self.alerts
        del self.media_agents
        del self.disk_libraries
        del self.storage_policies
        del self.schedule_policies
        del self.user_groups
        del self.workflows
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

    def request(self, request_type, request_url, request_body=None):
        """Runs the request of the type specified on the request URL, with the body passed
            in the arguments.

            Args:
                request_type (str)  --  type of HTTP request to run on the Commcell
                    e.g.; POST, GET, PUT, DELETE

                request_url (str)   --  API name to run the request on with params, if any
                    e.g.; Backupset, Agent, Client, Client/{clientId}, ..., etc.

                request_body (dict) --  JSON request body to pass along with the request
                    default: None

            Returns:
                object - the response received from the server
        """
        request_url = self._commcell_service + request_url
        flag, response = self._cvpysdk_object.make_request(request_type.upper(),
                                                           request_url,
                                                           request_body)

        return response
