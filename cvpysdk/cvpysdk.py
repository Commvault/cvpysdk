#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Helper file for session operations.

CVPySDK: Class for common operations for the CS, as well as the python package

CVPySDK:
    __init__(commcell_object)   --  initialise object of the CVPySDK class and bind to the commcell
    _is_valid_service_()        --  checks if the service is valid and running or not
    _login_()                   --  sign in the user to the commcell with the credentials provided
    _logout_()                  --  sign out the current logged in user from the commcell,
                                        and end the session
    make_request()              --  run the http request specified on the URL/WebService provided,
                                        and return the flag specifying success/fail, and response

"""

from __future__ import absolute_import

import requests

try:
    # Python 2 import
    import httplib as httplib
except ImportError:
    # Python 3 import
    import http.client as httplib

from .exception import SDKException


class CVPySDK(object):
    """Helper class for login, and logout operations.

        Also contains method for performing request of all types.
    """

    def __init__(self, commcell_object):
        """Initialize the CVPySDK object for running various operations.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the CVPySDK class
        """
        self._commcell_object = commcell_object

    def _is_valid_service_(self):
        """Checks if the service url is a valid url or not.

            Returns:
                True - if the service url is valid
                False - if the service url is invalid

            Raises:
                Error returned by the requests package
        """
        try:
            response = requests.get(self._commcell_object._commcell_service)

            # Valid service if the status code is 200 and response is True
            return response.status_code == httplib.OK and response.ok
        except requests.exceptions.ConnectionError as con_err:
            raise con_err

    def _login_(self):
        """Posts a login request to the server

            Returns:
                tuple - (token, user_GUID), when response is success

            Raises:
                SDKException:
                    if login failed
                    if response is empty
                    if response is not success
                Error returned by the requests package
        """
        try:
            json_login_request = {
                "mode": 4,
                "username": self._commcell_object._user,
                "password": self._commcell_object._password
            }

            flag, response = self.make_request(
                'POST', self._commcell_object._services.LOGIN, json_login_request
            )

            if flag:
                if response.json():
                    if "userName" in response.json() and "token" in response.json():
                        return str(response.json()['token']), str(response.json()['userGUID'])
                    else:
                        error_message = response.json()['errList'][0]['errLogMessage']
                        err_msg = 'Login Failed\nError: "{0}"'.format(error_message)
                        raise SDKException('CVPySDK', '101', err_msg)
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('CVPySDK', '101')
        except requests.exceptions.ConnectionError as con_err:
            raise con_err.message

    def _logout_(self):
        """Posts a logout request to the server

            Returns:
                str - response string from server upon logout success
        """
        flag, response = self.make_request('POST', self._commcell_object._services.LOGOUT)

        if flag:
            self._commcell_object._headers['Authtoken'] = None
            if response.status_code == httplib.OK:
                return response.text
            else:
                return 'Failed to logout the user'
        else:
            return 'User already logged out'

    def make_request(self, method, url, payload=None, attempts=0):
        """Makes the request of the type specified in the argument 'method'

            Args:
                method    (str)         --  http operation to perform, e.g.; GET, POST, PUT, DELETE
                url       (str)         --  the web url or service to run the HTTP request on
                payload   (dict / str)  --  data to be passed along with the request
                    default: None
                attempts  (int)         --  number of attempts made with the same request
                    default: 0

            Returns:
                tuple:
                    (True, response) - in case of success
                    (False, response) - in case of failure

            Raises:
                SDKException:
                    if the method passed is incorrect / not supported
                    if the number of attempts exceed 3
                Error returned by the requests package
        """
        try:
            headers = self._commcell_object._headers

            if method == 'POST':
                if isinstance(payload, dict):
                    response = requests.post(url, headers=headers, json=payload)
                else:
                    response = requests.post(url, headers=headers, data=payload)
            elif method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=payload)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise SDKException('CVPySDK', '102', 'HTTP method {} not supported'.format(method))

            if response.status_code == httplib.UNAUTHORIZED and headers['Authtoken'] is not None:
                if attempts < 3:
                    self._commcell_object._headers['Authtoken'], _ = self._login_()
                    return self.make_request(method, url, payload, attempts + 1)
                else:
                    # Raise max attempts exception, if attempts exceeds 3
                    raise SDKException('CVPySDK', '103')

            if response.status_code == httplib.OK and response.ok:
                return (True, response)
            else:
                return (False, response)
        except requests.exceptions.ConnectionError as con_err:
            raise con_err.message
