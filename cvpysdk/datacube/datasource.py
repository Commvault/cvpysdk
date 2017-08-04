#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Main file for performing operations on Datasources, and a single Datasource in the Datacube.

`Datasources`, and `Datasource` are 2 classes defined in this file.

Datasources:    Class for representing all the Datasources in the Datacube.

Datasource:     Class for representing a single Datasource in the Datacube.


Datasources:

    __init__(datacube_object)               --  initialise object of the Datasources class

    __str__()                               --  prints all the datasources

    __repr__()                              --  returns the string representation of this instance

    _get_datasources_from_collections()     --  gets all the datasources from a list of collections

    _get_all_datasources()                  --  gets the collections, and all datasources in it

    has_datasource()                        --  checks if a datasource exists with the given name

    get(datasource_name)                    --  returns an instance of the Datasource class,
                                                    for the input datasource name

Datasource:

    __init__(
        datacube_object,
        datasource_name,
        datasource_id=None)     --  initialise an object of Class with the given datasource name
                                        and id, and associated to the datacube

    __repr__()                  --  return the datasource name, the instance is associated with

    _get_datasource_id()        --  method to get the datasource id, if not specified in __init__

    _get_datasource_properties()--  get the properties of this datasource

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from past.builtins import basestring

from .sedstype import SEDS_TYPE_DICT

from ..exception import SDKException


class Datasources(object):
    """Class for representing all the Datasources in the Datacube."""

    def __init__(self, datacube_object):
        """Initializes an instance of the Datasources class.

            Args:
                datacube_object     (object)    --  instance of the Datacube class

            Returns:
                object  -   instance of the Datasources class
        """
        self._datacube_object = datacube_object

        self._ALL_DATASOURCES = self._datacube_object._commcell_object._services[
            'GET_ALL_DATASOURCES']

        self._datasources = self._get_all_datasources()

    def __str__(self):
        """Representation string consisting of all datasources in datacube.

            Returns:
                str - string of all the datasources associated with the datacube
        """
        representation_string = '{:^5}\t{:30}\n\n'.format('ID', 'Data Source Name')

        for datasource in self._datasources:
            sub_str = '{:^5}\t{:30}\n'.format(
                datasource['data_source_id'], datasource['data_source_name']
            )
            representation_string += sub_str

        return representation_string

    def __repr__(self):
        """Representation string for the instance of the Datasources class."""
        return "Datasources class instance for Commcell: '{0}'".format(
            self._datacube_object._commcell_object._headers['Host']
        )

    @staticmethod
    def _get_datasources_from_collections(collections):
        """Extracts all the datasources, and their details from the list of collections given,
            and returns the dictionary of all datasources.

            Args:
                collections     (list)  --  list of all collections

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single datasource

                    {
                        'data_source_1_name': {

                            'data_source_id': 21,

                            'data_source_name': '',

                            'description': '',

                            'data_source_type': '',

                            'total_count': 1234,

                            'state': 1
                        },

                        'data_source_2_name': {},

                        'data_source_3_name': {}
                        ...
                    }
        """
        datasources = {}

        for collection in collections:
            for datasource in collection['datasources']:
                datasource_dict = {}

                datasource_dict['data_source_id'] = datasource['datasourceId']
                datasource_dict['data_source_name'] = datasource['datasourceName']
                datasource_dict['description'] = datasource['description']
                datasource_dict['data_source_type'] = SEDS_TYPE_DICT[datasource['datasourceType']]
                datasource_dict['total_count'] = datasource['status']['totalcount']
                datasource_dict['state'] = datasource['status']['state']

                datasources[datasource['datasourceName']] = datasource_dict

        return datasources

    def _get_all_datasources(self):
        """Gets the list of all datasources associated with this Datacube instance.

            Returns:
                dict    -   dictionary consisting of dictionaries, where each dictionary stores the
                                details of a single datasource

                    {
                        'data_source_1_name': {

                            'data_source_id': 21,

                            'data_source_name': '',

                            'description': '',

                            'data_source_type': '',

                            'total_count': 1234,

                            'state': 1
                        },

                        'data_source_2_name': {},

                        'data_source_3_name': {}
                        ...
                    }
        """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'GET', self._ALL_DATASOURCES
        )

        if flag:
            if response.json() and 'collections' in response.json():
                collections = response.json()['collections']
                return self._get_datasources_from_collections(collections)
            else:
                raise SDKException('Datacube', '104')
        else:
            self._datacube_object._response_not_success(response)

    def has_datasource(self, datasource_name):
        """Checks if a datasource exists in the Datacube with the input datasource name.

            Args:
                datasource_name     (str)   --  name of the datasource

            Returns:
                bool    -   boolean output whether the datasource exists in the datacube or not

            Raises:
                SDKException:
                    if type of the datasource name argument is not string
        """
        if not isinstance(datasource_name, basestring):
            raise SDKException('Datacube', '101')

        return self._datasources and datasource_name.lower() in self._datasources

    def get(self, datasource_name):
        """Returns a datasource object of the specified datasource name.

            Args:
                datasource_name     (str)   --  name of the datasource

            Returns:
                object  -   instance of the Datasource class for the given datasource name

            Raises:
                SDKException:
                    if type of the datasource name argument is not string

                    if no datasource exists with the given name
        """
        if not isinstance(datasource_name, basestring):
            raise SDKException('Datacube', '101')

        datasource_name = datasource_name.lower()

        if self.has_datasource(datasource_name):
            datasource = self._datasources[datasource_name]

            return Datasource(
                self._datacube_object, datasource_name, datasource['data_source_id']
            )

        raise SDKException(
            'Datacube', '102' 'No datasource exists with the name: {0}'.format(datasource_name)
        )


class Datasource(object):
    """Class for performing operations on a single datasource"""

    def __init__(self, datacube_object, datasource_name, datasource_id=None):
        """Initialize an object of the Datasource class.

            Args:
                datacube_object     (object)    --  instance of the Datacube class

                datasource_name     (str)       --  name of the datasource

                datasource_id       (str)       --  id of the datasource
                    default: None

            Returns:
                object  -   instance of the Datasource class
        """
        self._datacube_object = datacube_object
        self._datasource_name = datasource_name.lower()

        if datasource_id is not None:
            self._datasource_id = str(datasource_id)
        else:
            self._datasource_id = self._get_datasource_id()

        self._DATASOURCE = self._datacube_object._commcell_object._services['GET_DATASOURCE'] % (
            self._datasource_id
        )

        self._properties = self._get_datasource_properties()

    def __repr__(self):
        """String representation of the instance of this class."""
        representation_string = 'Datasource class instance for Commcell: "{0}"'

        return representation_string.format(
            self._datacube_object._commcell_object._headers['Host']
        )

    def _get_datasource_id(self):
        """Gets the datasource id associated with this datasource.

            Returns:
                str     -   id associated with this datasource
        """
        datasources = Datasources(self._datacube_object)
        return datasources.get(self.datasource_name).datasource_id

    def _get_datasource_properties(self):
        """Gets the properties of this datasource.

            Returns:
                dict - dictionary consisting of the properties of this client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """
        # TODO: Populate self.properties in this method
        pass

    @property
    def datasource_id(self):
        """Returns the value of the data source id attribute."""
        return self._datasource_id

    @property
    def datasource_name(self):
        """Returns the value of the data source name attribute."""
        return self._datasource_name
