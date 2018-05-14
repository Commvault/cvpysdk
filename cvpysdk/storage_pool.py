# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for doing operations on an Storage Pools.

This module has classes defined for doing operations for Storage Pools:

    #. Get the Id for the given Storage Pool


StoragePools
============

    __init__(commcell_object)   --  initializes object of the StoragePools class associated
    with the commcell

    __str__()                   --  returns all the storage pools associated with the commcell

    __repr__()                  --  returns the string representation of an instance of this class

    __len__()                   --  returns the number of storage pools added to the Commcell

    __getitem__()               --  returns the name of the storage pool for the given storage
    pool Id or the details for the given storage pool name

    _get_storage_pools()        --  returns all storage pools added to the commcell

    has_storage_pool()          --  checks whether the storage pool  with given name exists or not

    get()                       --  returns id of the storage pool for the specified input name

    refresh()                   --  refresh the list of storage pools associated with the commcell


Attributes
----------

    **all_storage_pools**   --  returns dict of all the storage pools on commcell


# TODO: check with MM API team to get the response in JSON


"""

import xmltodict

from .exception import SDKException


class StoragePools:
    """Class for doing operations on Storage Pools, like get storage poo ID."""

    def __init__(self, commcell_object):
        """Initializes instance of the StoragePools class to perform operations on a storage pool.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the StoragePools class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._storage_pools_api = self._services['STORAGE_POOL']
        self._storage_pools = None

        self.refresh()

    def __str__(self):
        """Representation string consisting of all storage pools present in the Commcell.

            Returns:
                str     -   string of all the storage pools associated with the commcell

        """
        representation_string = '{:^5}\t{:^40}\n\n'.format('S. No.', 'Storage Pool')

        for index, storage_pool in enumerate(self._storage_pools):
            sub_str = '{:^5}\t{:40}\n'.format(index + 1, storage_pool)
            representation_string += sub_str

        return representation_string.strip()

    def __repr__(self):
        """Returns the string representation of an instance of this class."""
        return "StoragePools class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def __len__(self):
        """Returns the number of the storage pools added to the Commcell."""
        return len(self.all_storage_pools)

    def __getitem__(self, value):
        """Returns the name of the storage pool for the given storage pool ID or
            the details of the storage pool for given storage pool Name.

            Args:
                value   (str / int)     --  Name or ID of the storage pool

            Returns:
                str     -   name of the storage pool, if the storage pool id was given

                dict    -   dict of details of the storage pool, if storage pool name was given

            Raises:
                IndexError:
                    no storage pool exists with the given Name / Id

        """
        value = str(value)

        if value in self.all_storage_pools:
            return self.all_storage_pools[value]
        else:
            try:
                return list(
                    filter(lambda x: x[1]['id'] == value, self.all_storage_pools.items())
                )[0][0]
            except IndexError:
                raise IndexError('No storage pool exists with the given Name / Id')

    def _get_storage_pools(self):
        """Gets all the storage pools associated with the Commcell environment.

            Returns:
                dict    -   consists of all storage pools added to the commcell

                    {
                        "storage_pool1_name": storage_pool1_id,

                        "storage_pool2_name": storage_pool2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        headers = self._commcell_object._headers.copy()
        headers['Accept'] = 'application/xml'

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._storage_pools_api, headers=headers
        )

        if flag:
            storage_pools = {}

            response = xmltodict.parse(response.text)['Api_GetStoragePoolListResp']

            storage_pool_list = response['storagePoolList']

            if not isinstance(storage_pool_list, list):
                storage_pool_list = [storage_pool_list]

            if response:
                for pool in storage_pool_list:
                    name = pool['storagePoolEntity']['@storagePoolName'].lower()
                    storage_pool_id = pool['storagePoolEntity']['@storagePoolId']

                    storage_pools[name] = storage_pool_id

            return storage_pools
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def all_storage_pools(self):
        """Returns dict of all the storage pools on this commcell

            dict    -   consists of all storage pools added to the commcell

                {

                    "storage_pool1_name": storage_pool1_id,

                    "storage_pool2_name": storage_pool2_id
                }

        """
        return self._storage_pools

    def has_storage_pool(self, name):
        """Checks if a storage pool exists in the Commcell with the input storage pool name.

            Args:
                name    (str)   --  name of the storage pool

            Returns:
                bool    -   boolean output whether the storage pool exists in the commcell or not

        """
        return self._storage_pools and name.lower() in self._storage_pools

    def get(self, name):
        """Returns the id of the storage pool for the given storage pool name.

            Args:
                name    (str)   --  name of the storage pool to get the id of

            Returns:
                str     -   id of the storage pool for the given storage pool name

            Raises:
                SDKException:
                    if no storage pool exists with the given name

        """
        name = name.lower()

        if self.has_storage_pool(name):
            return self._storage_pools[name]
        else:
            raise SDKException('StoragePool', '103')

    def refresh(self):
        """Refresh the list of storage pools associated to the Commcell."""
        self._storage_pools = self._get_storage_pools()
