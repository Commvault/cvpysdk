#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# ---
from ..exception import SDKException
from sedstype import SEDSType


class Datasources(object):
    """ Represents a datasource in datacube """

    def __init__(self,  datacube_object):
        self._datacube_object = datacube_object

        self._ALL_DATASOURCES = self._datacube_object._commcell_object._services[
            'GET_ALL_DATASOURCES']
        self._datasources = self._get_all_datasources()

    def __str__(self):
        """Representation string consisting of all datasources in datacube.

            Returns:
                str - string of all the datasources associated with the datacube
        """
        representation_string = '{:^5}\t{:20}\n\n'.format('id', 'datasourceName')

        for datasource in self._datasources:
            sub_str = '{:^5}\t{:20}\n'.format(datasource['datasourceId'], datasource[
                'datasourceName'])
            representation_string += sub_str

        return representation_string

    def _raise_response_not_success_exception_(self, response):
        """ Helper function to raise an exception when reponse status is not 200 OK

            Args:
                 response   (object)    --  request response object
        """
        response_string = self._datacube_object._commcell_object._update_response_(response.text)
        raise SDKException('Response', '101', response_string)

    def _extract_datasources_from_collections(self, collections):
        """
            Helper function to extract datasource information from collections array
            Args:
                collections (array) --  Array of collections

            returns:
                An array of datasource objects
                [
                    {
                        datasourceName: '',
                        description: '',
                        datasourceType: '',
                        totalCount: 1234,
                        state: 1,
                        datasourceId: 21
                    },
                    {
                        datasourceName: '',
                        ...
                        ...
                    },
                    {},
                    ...
                ]
        """
        datasources = []
        for collection in collections:
            for datasource in collection['datasources']:
                datasource_dict = {}
                datasource_dict['datasourceId'] = datasource['datasourceId']
                datasource_dict['datasourceName'] = datasource['datasourceName']
                datasource_dict['description'] = datasource['description']
                datasource_dict['datasourceType'] = SEDSType.get_name_from_value(
                    datasource['datasourceType']
                )
                datasource_dict['totalcount'] = datasource['status']['totalcount']
                datasource_dict['state'] = datasource['status']['state']
                datasources.append(datasource_dict)
        return datasources

    def _get_all_datasources(self):
        """
            Gets all datasources associated with this datacube instance

            returns:

                Array of datasource objects

        """
        flag, response = self._datacube_object._commcell_object._cvpysdk_object.make_request(
            'GET', self._ALL_DATASOURCES
        )

        if flag:
            parsed_response = response.json()
            if (parsed_response and 'collections' in parsed_response):
                collections = response.json()['collections']
                return self._extract_datasources_from_collections(collections)
            else:
                raise SDKException('Datacube', '102')
        else:
            self._raise_response_not_success_exception_(response)

    def _get_cached_datasource(self, datasource_name):
        for datasource in self._datasources:
            if datasource['datasourceName'] == datasource_name:
                return datasource

        return None

    def get(self, datasource_name):
        """
        Returns a datasource from datacube that matches the supplied datasource_name
        Args:
            datasource_name (string)    --  name of the datasource


        Raises:
            SDKException:
                if type of datasource_name argument is not string

                if no datasource exists with the given name
        """

        if not isinstance(datasource_name, basestring):
            raise SDKException('Datacube', '103')
        else:
            datasource_name = datasource_name.lower()
            if(self.has_datasource(datasource_name)):
                datasource_summary = self._get_cached_datasource(datasource_name)
                return Datasource(self._datacube_object, datasource_name,
                                  datasource_summary.datasourceId)

            raise SDKException('Datacube', '104' 'No datasource exists with the name: {0}'
                               .format(datasource_name))

    def has_datasource(self, datasource_name):
        for datasource in self._datasources:
            if datasource['datasourceName'] == datasource_name:
                return True

        return False


class Datasource(object):
    """class for performing datasource operations for a specific datasource"""

    def __init__(self, datacube_object, datasource_name, datasource_id=None):
        """Initialise the Datasource class instance.

            Args:
                datacube_object (object)  --  instance of the Datacube class

                datasource_name     (str)     --  name of the datasource

                datasource_id       (str)     --  id of the datasource

            Returns:
                object - instance of the Datasource class
        """

        self._datacube_object = datacube_object
        self._datasource_name = datasource_name.lower()

        if(datasource_id):
            self._datasource_id = str(datasource_id)
        else:
            self._datasource_id = self._get_datasource_id()

        self._DATASOURCE = self._datacube_object._commcell_object._services['GET_DATASOURCE'] % (
            self._datasource_id
        )

        self._datasource_info = self._get_datasource_properties()

    def _get_datasource_properties(self):
        """Gets the properties of this datasource.

            Returns:
                dict - dictionary consisting of the properties of this client

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        #TODO: Populate self.properteis in this method
        pass

    def _get_datasource_id(self):
        #TODO: Complete this method
        pass
