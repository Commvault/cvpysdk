# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations related to Datacube APIs.

The class `Datacube` is defined here in this file,
that will directly interact with all the Datacube APIs.


Datacube:

    __init__(commcell_object)   --  initialise object of the Datacube class

    __repr__()                  --  returns the string representation of an instance of this class

    _response_not_success()     --  parses through the exception response, and raises SDKException

    _get_analytics_engines()    --  returns the list of all Content Indexing (CI) Servers

    datasources()               --  returns an instance of the Datasources class

    get_jdbc_drivers()          --  gets the list all jdbc_drivers associated with the datacube.

    refresh()                   --  refresh the datasources associated with the Datacube Engine

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

from .datasource import Datasources

from ..exception import SDKException


USER_LOGGED_OUT_MESSAGE = 'User Logged Out. Please initialize the Commcell object again.'
"""str:     Message to be returned to the user, when trying the get the value of an attribute
of the Commcell class, after the user was logged out.

"""


class Datacube(object):

    """ Represents a datacube running on the commcell """

    def __init__(self, commcell_object):
        """Initialize an instance of the Datacube class.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the Datacube class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._ANALYTICS_ENGINES = self._services['GET_ANALYTICS_ENGINES']
        self._ALL_DATASOURCES = self._services['GET_ALL_DATASOURCES']
        self._GET_JDBC_DRIVERS = None

        self._analytics_engines = self._get_analytics_engines()
        self._datasources = None

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str     -   string consisting of the details of the instance of this class

        """
        o_str = "Datacube class instance for CommServ '{0}'".format(
            self._commcell_object.commserv_name
        )

        return o_str

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_analytics_engines(self):
        """Gets the list all the analytics engines associated with the datacube.

            Returns:
                dict    -   consists of all clients in the commcell
                    {
                        "listOfCIServer": []    # array of analytics engines
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._ANALYTICS_ENGINES)

        if flag:
            if response.json() and 'listOfCIServer' in response.json():
                return response.json()['listOfCIServer']
            else:
                raise SDKException('Datacube', '103')
        else:
            self._response_not_success(response)

    @property
    def analytics_engines(self):
        """Returns the value of the analytics engines attributes."""
        return self._analytics_engines

    @property
    def datasources(self):
        """Returns the instance of the Datasources class."""
        try:
            if self._datasources is None:
                self._datasources = Datasources(self)

            return self._datasources
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def get_jdbc_drivers(self, analytics_engine):
        """Gets the list all jdbc_drivers associated with the datacube.

            Args:
                analytics_engine (str) -- client name of analytics_engine

            Returns:
                list    -   consists of all jdbc_drivers in the datacube

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        if not isinstance(analytics_engine, basestring):
            raise SDKException('Datacube', '101')

        engine_index = (
            self.analytics_engines.index(engine)
            for engine in self.analytics_engines
            if engine["clientName"] == analytics_engine
        ).next()

        self._GET_JDBC_DRIVERS = self._services['GET_JDBC_DRIVERS'] % (
            self.analytics_engines[engine_index]["cloudID"]
        )

        flag, response = self._cvpysdk_object.make_request('GET', self._GET_JDBC_DRIVERS)

        if flag:
            if response.json() and 'drivers' in response.json():
                return response.json()['drivers']
            else:
                raise SDKException('Datacube', '103')
        else:
            self._response_not_success(response)

    def refresh(self):
        """Refresh the datasources associated to the Datacube Engine."""
        self._datasources = None
