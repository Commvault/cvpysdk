# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Module for doing operations on an Exchange Database Agent.

This module has operations that are applicable at the Agent level for Exchange Database.

ExchangeDatabaseSubclient:
    _get_subclient_properties()         --  get the properties of the subclient, and initialize
    the basic properties

    _get_subclient_properties_json()    --  gets all the subclient properties of the
    Exchange Database subclient

    _set_content                        --  Sets the content for Exchange Database subclient

    restore_in_place()                  --  runs in-place restore for the subclient

    restore_out_of_place                --  runs out of place restore for the subclient

    set_subclient_properties()          -- sets the properties of this sub client


Attributes
----------

    **content**     --  returns the content of the Exchange Database subclient

"""

from __future__ import unicode_literals

from ...subclient import Subclient
from ...exception import SDKException


class ExchangeDatabaseSubclient(Subclient):
    """Derived class from the Subclient Base class,
        to perform operations specific to an Exchange Database Subclient."""

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of Exchange Database subclient.."""
        super(ExchangeDatabaseSubclient, self)._get_subclient_properties()

        self._content = self._subclient_properties.get('content', [])
        self._exchange_db_subclient_prop = self._subclient_properties.get(
            'exchangeDBSubClientProp', {}
        )

    def _get_subclient_properties_json(self):
        """Returns the JSON with the properties for the Subclient, that can be used for a POST
        request to update the properties of the Subclient.

           Returns:
               dict     -   all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties": {
                "subClientEntity": self._subClientEntity,
                "exchangeDBSubClientProp": self._exchange_db_subclient_prop,
                "content": self._content,
                "commonProperties": self._commonProperties,
                "contentOperationType": 1
            }
        }

        return subclient_json

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list    -   list of content added to the subclient

        """
        return self._content

    @content.setter
    def content(self, subclient_content):
        """Update the content of the subclient with the content list given by the user.

            Args:
                subclient_content   (list)  --  list of the content to add to the subclient

            Raises:
                SDKException:
                    if specified input is not a list

                    if failed to update subclient content

        """
        if isinstance(subclient_content, list) and subclient_content != []:
            self._set_content(content=subclient_content)
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient content should be a list value and not empty'
            )

    def _set_content(self, content):
        """Sets the subclient content

            Args:
                content         	(list)      --  list of subclient content

        """
        temp = []
        for item in content:
            temp.append({
                "exchangeDBContent": {
                    "databaseName": item,
                    "forceFull": True
                }
            })

        self._set_subclient_properties("_content", temp)

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                kwargs   (dict)  --  dict of options need to be set for restore

            Returns:
                dict - JSON request to pass to the API
        """
        self._instance_object._restore_association = self._subClientEntity

        restore_json = self._instance_object._restore_json(**kwargs)

        exchange_options = {
            "exchangeRestoreLogOption": 0,
            "exchangeVersion": {
                "name": "",
                "version": 15
            }
        }

        restore_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['exchangeOption'] = exchange_options

        return restore_json

    def restore_in_place(self, paths, client=None):
        """
         Run inplace restore for Exchange database subclient

         Args:
             paths      (list)   -- list of path used for inplace restore

             client     (object) -- object of client class

        Returns:
            object  -   Job class object for restore job
        """
        if client is None:
            client = self._client_object
        restore_json = self._restore_json(paths=paths, client=client)

        return self._process_restore_response(restore_json)

    def restore_out_of_place(self, client, paths):
        """
         Run out of place restore for Exchange database subclient
            Args:
                client      (str)       -- destination client on which the restore should run

                paths       (list)      -- list of path used for out of place restore

            Returns:
                object  -   Job class object for restore job
        """
        restore_json = self._restore_json(paths=paths, client=client)

        return self._process_restore_response(restore_json)

    def set_subclient_properties(self, attr_name, value):
        """"sets the properties of this sub client.value is updated to instance once when post call
            succeeds

            Args:
                attr_name (str)  --  old value of the property. this should be instance variable.
                value (str)  --  new value of the property. this should be instance variable.

        """
        self._set_subclient_properties(attr_name, value)
