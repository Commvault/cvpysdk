#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# ---

"""
    Main file for performing Datacube related operations

    The class 'Datacube' is defined here

    Datacube:
    __init__(commcell_object)    --  initialise object of the Datacube class
    _attribs_()                  --  initializes the objects of the classes given in the input list

    _init_attrib_()              --  initializes the object of the class given as input and stores
                                        in the given input dictionary with class name as key

"""
from threading import Thread

try:
    # Python 2 import
    from Queue import Queue
except ImportError:
    # Python 3 import
    from queue import Queue

from .exception import SDKException
from .datasource import Datasources


class Datacube(object):

    """ Represents a datacube running on the commcell """

    def __init__(self, commcell_object):
        """Initialize object of the Datacube class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Datacube class
        """
        self._commcell_object = commcell_object

        # APIs
        self._ANALYTICS_ENGINES = self._commcell_object._services['GET_ANALYTICS_ENGINES']
        self._ALL_DATASOURCES = self._commcell_object._services['GET_ALL_DATASOURCES']

        # API results
        self.analytics_engines = self._get_analytics_engines()

        datacube_sdk_classes = [
            Datasources
        ]

        datacube_sdk_dict = self._attribs_(datacube_sdk_classes)

        self.datasources = datacube_sdk_dict[Datasources]

    def __str__(self):
        """Representation string consisting of all datacube of the commcell.

            Returns:
                str - string of all the clients associated with the commcell

            TODO: Do this
        """
        print("yet to do")

    def _raise_response_not_success_exception_(self, response):
        """ Helper function to raise an exception when reponse status is not 200 OK
            Args:
                 response   (object)    --  request response object
        """
        response_string = self._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _get_analytics_engines(self):
        """Gets all the analytics engines associated with the datacube

            Returns:
                dict - consists of all clients in the commcell
                    {
                         "listOfCIServer": [] //array of analytics engines
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request\
        ('GET', self._ANALYTICS_ENGINES)

        if flag:
            parsed_response = response.json()
            if(parsed_response and 'listOfCIServer' in parsed_response):
                return response.json()['listOfCIServer']
            else:
                raise SDKException('Datacube', '101')
        else:
            self._raise_response_not_success_exception_(response)

    def _attribs_(self, datacube_sdk_classes):
        """Initializes the objects of the classes in the datacube_sdk_classes list given as input.

            Args:
                datacube_sdk_classes (list)  --  list containing the classes to initialize the
                object of

            Returns:
                dict - dict consisting of the class name as key and the class object as its value
        """
        datacube_sdk_dict = {}

        self._queue = Queue()

        for datacube_sdk_class in datacube_sdk_classes:
            thread = Thread(target=self._init_attrib_, args=(datacube_sdk_class,
                                                             datacube_sdk_dict))
            self._queue.put(thread)
            thread.start()

        self._queue.join()

        return datacube_sdk_dict

    def _init_attrib_(self, datacube_sdk_class, datacube_sdk_dict):
        """Initializes the object of the datacube_sdk_class given as input, and stores it
            with the class name as the key to the datacube_sdk_dict.

            Args:
                datacube_sdk_class (class)  --  sdk class to initialize the object of

                datacube_sdk_dict  (dict)   --  dict to store the class object as value,
                                        with the class name as key
        """
        try:
            datacube_sdk_dict[datacube_sdk_class] = datacube_sdk_class(self)
        except SDKException:
            datacube_sdk_dict[datacube_sdk_class] = None
        finally:
            self._queue.task_done()
