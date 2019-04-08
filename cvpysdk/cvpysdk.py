# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# pylint: disable=R1705

"""Helper file for session operations.

This file is used to perform Authentication for the user on the Commcell.

    #.  Check if the web server and service is valid and running

    #.  Perform Login operation to the Commcell using the credentials provided by the user

    #.  Store the Authtoken received after Login REST API call to use for the entire session

    #.  Renew Authtoken if credentials were given by the user during Commcell object
        initialization, and the current token has expired

    #.  Logout the current user from the Commcell, and disconnect the API session

    #.  Common method to be used in the entire SDK to perform REST API call on the Web Server


CVPySDK:

    __init__(commcell_object)   --  initialise object of the CVPySDK class and bind to the commcell

    _is_valid_service()         --  checks if the service is valid and running or not

    _login()                    --  sign in the user to the commcell with the credentials provided

    _renew_login_token()        --  renews the Authtoken for the currently logged in user

    _logout()                   --  sign out the current logged in user from the commcell,
    and ends the session

    _request()                  --  executes the request on the server and return the Response

    who_am_i()                  --  Fetches the username of the user to whom authtoken is mapped

    make_request()              --  run the http request specified on the URL/WebService provided,
    and return the flag specifying success/fail, and response

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from xml.parsers.expat import ExpatError

import requests
import xmltodict

try:
    # Python 2 import
    import httplib
except ImportError:
    # Python 3 import
    import http.client as httplib

from .exception import SDKException


class CVPySDK(object):
    """Helper class for login, and logout operations.

        Also contains common method for running all HTTP requests.
    """

    def __init__(self, commcell_object, certificate_path=None):
        """Initialize the CVPySDK object for running various operations.

            Args:
                commcell_object     (object)    --  instance of the Commcell class


                certificate_path        (str)   --  path of the CA_BUNDLE or directory with
                certificates of trusted CAs (including trusted self-signed certificates)

                    default: None

            Returns:
                object  -   instance of the CVPySDK class

        """
        self._commcell_object = commcell_object
        self._certificate_path = certificate_path

    def _is_valid_service(self):
        """Checks if the service url is a valid url or not.

            Returns:
                True    -   if the service url is valid

                False   -   if the service url is invalid

            Raises:
                requests Connection Error:
                    requests.exceptions.ConnectionError

                requests Timeout Error:
                    requests.exceptions.Timeout

        """
        try:
            response = self._request(
                method='GET',
                url=self._commcell_object._web_service,
                timeout=184
            )

            # Valid service if the status code is 200 and response is True
            return response.status_code == httplib.OK and response.ok
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            raise error

    def _login(self):
        """Posts a login request to the server.

            Returns:
                str     -   Authtoken received from the WebServer upon successfull login

            Raises:
                SDKException:
                    if login failed

                    if response is empty

                    if response is not success

                requests Connection Error:
                    requests.exceptions.ConnectionError

        """
        try:
            if isinstance(self._commcell_object._password, dict):
                raise SDKException('CVPySDK', '104')

            json_login_request = {
                "mode": 4,
                "username": self._commcell_object._user,
                "password": self._commcell_object._password,
                "deviceId": self._commcell_object.device_id
            }

            flag, response = self.make_request(
                'POST', self._commcell_object._services['LOGIN'], json_login_request
            )

            if flag:
                if response.json():
                    if "userName" in response.json() and "token" in response.json():
                        return response.json()['token']
                    else:
                        error_message = response.json()['errList'][0]['errLogMessage']
                        err_msg = 'Error: "{0}"'.format(error_message)
                        raise SDKException('CVPySDK', '101', err_msg)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        except requests.exceptions.ConnectionError as con_err:
            raise con_err

    def _renew_login_token(self):
        """Posts a Renew Login Token request to the server.

            Returns:
                str     -   new token received from the WebServer

            Raises:
                SDKException:
                    if token renew failed

                    if response is empty

                    if response is not success

                requests Connection Error:
                    requests.exceptions.ConnectionError

        """
        try:
            if self._commcell_object._is_saml_login:
                raise SDKException('CVPySDK', '106')

            token_renew_request = {
                "sessionId": self._commcell_object._headers['Authtoken'],
                "deviceId": self._commcell_object.device_id
            }

            flag, response = self.make_request(
                'POST', self._commcell_object._services['RENEW_LOGIN_TOKEN'], token_renew_request
            )

            if flag:
                if response.json():
                    if "token" in response.json():
                        return response.json()['token']
                    else:
                        error_message = response.json()['error']['errLogMessage']
                        err_msg = 'Error: "{0}"'.format(error_message)
                        raise SDKException('CVPySDK', '101', err_msg)
                else:
                    raise SDKException('Response', '102')
            else:
                response_string = self._commcell_object._update_response_(response.text)
                raise SDKException('Response', '101', response_string)
        except requests.exceptions.ConnectionError as con_err:
            raise con_err

    def _logout(self):
        """Posts a logout request to the server.

            Returns:
                str     -   response string from server upon logout success

        """
        flag, response = self.make_request('POST', self._commcell_object._services['LOGOUT'])

        if flag:
            self._commcell_object._headers['Authtoken'] = None

            if response.status_code == httplib.OK:
                return response.text
            else:
                return 'Failed to logout the user'
        else:
            return 'User already logged out'

    def _request(self, **kwargs):
        """Executes the request on the Server with the given parameters.

            If the certificate path is given and the Web Service starts with **https**,
            it adds the **verify** parameter to the request, and passes the certificate path as
            its value.

            Args:
                **kwargs    --  dict of keyword arguments, same as accepted by the

                    **requests.request** method

            Returns:
                object  -   **requests.Response** class instance, as received from calling the
                **requests.request** method

        """
        if self._certificate_path and self._commcell_object._web_service.startswith('https'):
            return requests.request(verify=self._certificate_path, **kwargs)

        return requests.request(**kwargs)

    def who_am_i(self, authtoken=None):
        """Get the username of the user, to whom the Authtoken belongs to.

            Args:
                authtoken   (str)   --  QSDK or SAML authentication token

            Returns:
                str     -   username of the user respective to the token

            Raises:
                SDKException:
                    if no user mapping found

        """
        temp_headers = self._commcell_object._headers.copy()

        if authtoken:
            temp_headers['Authtoken'] = authtoken

        flag, response = self.make_request(
            'POST', self._commcell_object._services['WHO_AM_I'], headers=temp_headers
        )

        if flag:
            user_dict = xmltodict.parse(response.content)

            if 'CvEntities_ProcessingInstructionInfo' in user_dict:
                return user_dict['CvEntities_ProcessingInstructionInfo']['user']['@userName']
            else:
                raise SDKException('CVPySDK', '107')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def make_request(
            self,
            method,
            url,
            payload=None,
            attempts=0,
            headers=None,
            stream=False,
            files=None):
        """Makes the request of the type specified in the argument 'method'.

            Args:
                method      (str)           --  HTTP operation to perform

                    e.g.:

                    -   GET

                    -   POST

                    -   PUT

                    -   DELETE

                url         (str)           --  the web url or service to run the HTTP request on


                payload     (dict / str)    --  data to be passed along with the request

                    default: None


                attempts    (int)           --  number of attempts made with the same request

                    default: 0


                headers     (dict)          --  dict of request headers for the request

                        if not specified we use default headers

                    default: None


                stream      (bool)          --  boolean specifying whether the request should get
                data via stream or normal get

                    default: False


                files       (dict)          --  file to upload in the form of

                        {
                            'file': open('report.txt', 'rb')
                        }

                    default: None

            Returns:
                tuple:
                    (True, response)    -   in case of success

                    (False, response)   -   in case of failure

            Raises:
                SDKException:
                    if the method passed is incorrect / not supported

                    if the number of attempts exceed 3

                requests Connection Error:
                    requests.exceptions.ConnectionError

        """
        try:
            if headers is None:
                headers = self._commcell_object._headers.copy()

            if method == 'POST':
                if isinstance(payload, (dict, list)):
                    if files is not None:
                        response = self._request(method=method, url=url, files=files, data=payload)
                    else:
                        response = self._request(
                            method=method, url=url, headers=headers, json=payload, stream=stream
                        )
                else:
                    try:
                        # call encode on the payload in case the characters in the payload
                        # are not encoded, and to encode the string payload to bytes
                        payload = payload.encode()
                    except AttributeError:
                        # pass silently if payload is alredy encoded in bytes
                        pass

                    if 'Content-type' in headers:
                        try:
                            if payload is not None:
                                xmltodict.parse(payload)
                            headers['Content-type'] = 'application/xml'
                        except ExpatError:
                            headers['Content-type'] = 'text/plain'

                    response = self._request(
                        method=method, url=url, headers=headers, data=payload, stream=stream
                    )
            elif method == 'GET':
                response = self._request(method=method, url=url, headers=headers, stream=stream)
            elif method == 'PUT':
                response = self._request(method=method, url=url, headers=headers, json=payload)
            elif method == 'DELETE':
                response = self._request(method=method, url=url, headers=headers)
            else:
                raise SDKException('CVPySDK', '102', 'HTTP method {} not supported'.format(method))

            if response.status_code == httplib.UNAUTHORIZED and headers['Authtoken'] is not None:
                if attempts < 3:
                    self._commcell_object._headers['Authtoken'] = self._renew_login_token()
                    return self.make_request(method, url, payload, attempts + 1)
                else:
                    # Raise max attempts exception, if attempts exceeds 3
                    raise SDKException('CVPySDK', '103')

            if response.status_code == httplib.OK and response.ok:
                return (True, response)
            else:
                return (False, response)
        except requests.exceptions.ConnectionError as con_err:
            raise con_err
