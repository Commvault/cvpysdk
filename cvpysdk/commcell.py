#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2017 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on Commcell via REST API.

Commcell is the main class for the CVPySDK python package.

Commcell: Initializes a connection to the commcell and is a wrapper for the entire commcell ops.

Commcell:
    __init__(webconsole_hostname,
             commcell_username,
             commcell_password)  --  initialise object of the Commcell class

    __repr__()                   --  return the name of the commcell, user is connected to,
                                        along with the user name of the connected user

    __enter__()                  --  returns the current instance, using the "with" context manager

    __exit__()                   --  logs out the user associated with the current instance

    _attribs_()                  --  initializes the objects of the classes given in the input list

    _init_attrib_()              --  initializes the object of the class given as input and stores
                                        in the given input dictionary with class name as key

    _update_response_()          --  returns only the relevant response for the response received
                                        from the server

    _remove_attribs_()           --  removes all the attributs associated with the commcell
                                        object upon logout

    _get_commserv_name()         --  returns the commserv name

    _qoperation_execute()        --  runs the qoperation execute rest api on specified input xml

    logout()                     --  logs out the user associated with the current instance

    request()                    --  runs an input HTTP request on the API specified,
                                        and returns its response

    send_mail()                  --  sends an email to the specified user

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import getpass
import socket

from base64 import b64encode

from requests.exceptions import SSLError
from requests.exceptions import Timeout

# ConnectionError is a built-in exception, do not override it
from requests.exceptions import ConnectionError as RequestsConnectionError


from .services import get_services
from .cvpysdk import CVPySDK
from .client import Clients
from .alert import Alerts
from .storage import MediaAgents
from .storage import DiskLibraries
from .storage import StoragePolicies
from .storage import SchedulePolicies
from .usergroup import UserGroups
from .workflow import WorkFlow
from .exception import SDKException
from .clientgroup import ClientGroups
from .globalfilter import GlobalFilters
from .datacube.datacube import Datacube
from .plan import Plans
from .job import JobController


USER_LOGGED_OUT_MESSAGE = 'User Logged Out. Please initialize the Commcell object again.'
"""str:     Message to be returned to the user, when trying the get the value of an attribute
                of the Commcell class, after the user was logged out.
"""


class Commcell(object):
    """Class for establishing a session to the Commcell via Commvault REST API."""

    def __init__(self, webconsole_hostname, commcell_username, commcell_password=None):
        """Initialize the Commcell object with the values required for doing the api operations.

            Args:
                webconsole_hostname  (str)  --  webconsole host name/ip; webclient.company.com

                commcell_username    (str)  --  username of the user to log in to commcell console

                commcell_password    (str)  --  plain text password to log in to commcell console
                    default: None

            Returns:
                object - instance of this class

            Raises:
                SDKException:
                    if the web service is down or not reachable

                    if no token is received upon log in
        """
        web_service = [
            r'https://{0}/webconsole/api/'.format(webconsole_hostname),
            r'http://{0}/webconsole/api/'.format(webconsole_hostname)
        ]

        self._user = commcell_username

        self._headers = {
            'Host': webconsole_hostname,
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authtoken': None
        }

        self._device_id = socket.getfqdn()

        if commcell_password is None:
            commcell_password = getpass.getpass('Please enter the Commcell Password: ')

        if isinstance(commcell_password, dict):
            self._password = commcell_password
        else:
            # encodes the plain text password using base64 encoding
            self._password = b64encode(commcell_password.encode()).decode()

        self._cvpysdk_object = CVPySDK(self)

        # Checks if the service is running or not
        for service in web_service:
            self._web_service = service
            try:
                if self._cvpysdk_object._is_valid_service():
                    break
            except (RequestsConnectionError, SSLError, Timeout):
                continue
        else:
            raise SDKException('Commcell', '101')

        # Initialize all the services with this commcell service
        self._services = get_services(self._web_service)

        if isinstance(commcell_password, dict):
            if self._password['Authtoken'].startswith('QSDK '):
                self._headers['Authtoken'] = self._password['Authtoken']
            else:
                self._headers['Authtoken'] = '{0}{1}'.format('QSDK ', self._password['Authtoken'])
        else:
            # Login to the commcell with the credentials provided
            # and store the token in the headers
            self._headers['Authtoken'] = self._cvpysdk_object._login()

        if not self._headers['Authtoken']:
            raise SDKException('Commcell', '102')

        self._commserv_name = self._get_commserv_name()

        self._clients = None
        self._media_agents = None
        self._workflows = None
        self._alerts = None
        self._disk_libraries = None
        self._storage_policies = None
        self._schedule_policies = None
        self._user_groups = None
        self._client_groups = None
        self._global_filters = None
        self._datacube = None
        self._plans = None
        self._job_controller = None

        del self._password

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string about the details of the Commcell class instance
        """
        representation_string = 'Commcell class instance of Commcell: "{0}", for User: "{1}"'
        return representation_string.format(self.webconsole_hostname, self._user)

    def __enter__(self):
        """Returns the current instance.

            Returns:
                object - the initialized instance referred by self
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Logs out the user associated with the current instance."""
        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def _update_response_(self, input_string):
        """Returns only the relevant response from the response received from the server.

            Args:
                input_string (str)  --  input string to retrieve the relevant response from

            Returns:
                str - final response to be used
        """
        if '<title>' in input_string and '</title>' in input_string:
            response_string = input_string.split("<title>")[1]
            response_string = response_string.split("</title>")[0]
            return response_string

        return input_string

    def _remove_attribs_(self):
        """Removes all the attributes associated with the instance of this class."""
        del self._clients
        del self._media_agents
        del self._workflows
        del self._alerts
        del self._disk_libraries
        del self._storage_policies
        del self._schedule_policies
        del self._user_groups
        del self._client_groups
        del self._global_filters
        del self._datacube
        del self._plans
        del self._job_controller

        del self._web_service
        del self._cvpysdk_object
        del self._device_id
        del self._services
        del self

    def _get_commserv_name(self):
        """Returns the name of the CommServ, the commcell is connected to.

            Returns:
                str     -   name of the CommServ

            Raises:
                SDKException:
                    if failed to get commserv name

                    if response received is empty

                    if response is not success
        """
        request_url = self._services['COMMSERV']

        flag, response = self._cvpysdk_object.make_request('GET', request_url)

        if flag:
            if response.json():
                if 'commcell' in response.json() and 'commCellName' in response.json()['commcell']:
                    return response.json()['commcell']['commCellName']
                else:
                    raise SDKException('Commcell', '103')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _qoperation_execute(self, request_xml):
        """Makes a qoperation execute rest api call

            Args:
                request_xml     (str)   --  request xml that is to be passed

            Returns:
                (dict)  -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def commserv_name(self):
        """Returns the value of the CommServ name attribute."""
        return self._commserv_name

    @property
    def webconsole_hostname(self):
        """Returns the value of the host name of the webconsole used to connect to the Commcell."""
        return self._headers['Host']

    @property
    def device_id(self):
        """Returns the value of the Device ID attribute."""
        try:
            return self._device_id
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def clients(self):
        """Returns the instance of the Clients class."""
        try:
            if self._clients is None:
                self._clients = Clients(self)

            return self._clients
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def media_agents(self):
        """Returns the instance of the MediaAgents class."""
        try:
            if self._media_agents is None:
                self._media_agents = MediaAgents(self)

            return self._media_agents
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def workflows(self):
        """Returns the instance of the Workflow class."""
        try:
            if self._workflows is None:
                self._workflows = WorkFlow(self)

            return self._workflows
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def alerts(self):
        """Returns the instance of the Alerts class."""
        try:
            if self._alerts is None:
                self._alerts = Alerts(self)

            return self._alerts
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def disk_libraries(self):
        """Returns the instance of the DiskLibraries class."""
        try:
            if self._disk_libraries is None:
                self._disk_libraries = DiskLibraries(self)

            return self._disk_libraries
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def storage_policies(self):
        """Returns the instance of the StoragePolicies class."""
        try:
            if self._storage_policies is None:
                self._storage_policies = StoragePolicies(self)

            return self._storage_policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def schedule_policies(self):
        """Returns the instance of the SchedulePolicies class."""
        try:
            if self._schedule_policies is None:
                self._schedule_policies = SchedulePolicies(self)

            return self._schedule_policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def user_groups(self):
        """Returns the instance of the UserGroups class."""
        try:
            if self._user_groups is None:
                self._user_groups = UserGroups(self)

            return self._user_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def client_groups(self):
        """Returns the instance of the ClientGroups class."""
        try:
            if self._client_groups is None:
                self._client_groups = ClientGroups(self)

            return self._client_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def global_filters(self):
        """Returns the instance of the GlobalFilters class."""
        try:
            if self._global_filters is None:
                self._global_filters = GlobalFilters(self)

            return self._global_filters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def datacube(self):
        """Returns the instance of the Datacube class."""
        try:
            if self._datacube is None:
                self._datacube = Datacube(self)

            return self._datacube
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def plans(self):
        """Returns the instance of the Plans class."""
        try:
            if self._plans is None:
                self._plans = Plans(self)

            return self._plans
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    @property
    def job_controller(self):
        """Returns the instance of the Jobs class."""
        try:
            if self._job_controller is None:
                self._job_controller = JobController(self)

            return self._job_controller
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE
        except SDKException:
            return None

    def logout(self):
        """Logs out the user associated with the current instance."""
        if self._headers['Authtoken'] is None:
            return 'User already logged out.'

        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def request(self, request_type, request_url, request_body=None):
        """Runs the request of the type specified on the request URL, with the body passed
            in the arguments.

            Args:
                request_type (str)   --  type of HTTP request to run on the Commcell
                    e.g.; POST, GET, PUT, DELETE

                request_url  (str)   --  API name to run the request on with params, if any
                    e.g.; Backupset, Agent, Client, Client/{clientId}, ..., etc.

                request_body (dict)  --  JSON request body to pass along with the request
                    default: None

            Returns:
                object - the response received from the server
        """
        request_url = self._web_service + request_url

        _, response = self._cvpysdk_object.make_request(
            request_type.upper(), request_url, request_body
        )

        return response

    def send_mail(self, to_address, subject, body=''):
        """Sends a mail to the specified email address from the email asscoiated to this user

            Args:
                to_address      (str)   --  to address to whom the mail is to be sent

                subject         (str)   --  subject of the email that is to be sent to the user

                body            (str)   --  email body that is to be sent to the user

            Raises:
                SDKException:
                    if failed to send an email to specified user

                    if response is empty

                    if response is not success
        """
        # encode the body if that contains special characters
        import html
        body = html.escape(body)

        send_email_request = """
        <App_SendEmailReq>
            <toEmail>{0}</toEmail>
            <subject>{1}</subject>
            <body>{2}</body>
        </App_SendEmailReq>""".format(to_address, subject, body)

        response_json = self._qoperation_execute(send_email_request)

        if 'errorCode' in response_json and response_json['errorCode'] != 0:
            raise SDKException('Commcell', '104')
