#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Main File for performing   Sybase Subclient Operations

SybaseSubclient is the only class defined in this file.

SybaseSubclient: Derived class from DatabaseSubclient Base class, representing an Sybase subclient,
                        and to perform operations on that subclient

SybaseSubclient:

    __init__()                          -- initialise object of sybase subclient object associated
                                            with the specified instance

    _get_subclient_properties           -- get the all subclient related properties of this subclient

    _sybase_backup_request_json         -- Returns the JSON request to pass to the API as per the options selected by the user

    content()                           -- update the content of the sybase  subclient

    backup()                            -- Run a backup job for the subclient


"""
from __future__ import unicode_literals
from .dbsubclient import DatabaseSubclient
from ..exception import SDKException


class SybaseSubclient(DatabaseSubclient):
    """
    Base class consisting of all the common properties and operations for a Sybase Subclient
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize Sybase Subclient Object

        Args:
            backupset_object  (object)  -- instance of the Backupset class

            subclient_name    (str)     -- name of the subclient

            subclient_id      (str)     -- id of the subclient

        Returns :
            object - instance of the Sybase Subclient class
        """
        super(SybaseSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)
        self._sybase_properties = {}

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of Sybase subclient"""

        super(SybaseSubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        return {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }

    def _sybase_backup_request_json(
            self,
            backup_level,
            donottruncatelog=False, sybaseskipfullafterlogbkp=False):
        """
        Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
               backup_level   (list)  --  level of backup the user wish to run
                        Full / Incremental / Differential

               donottruncatelog (bool) -- Sybase truncate log option for incremental backup

               sybaseskipfullafterlogbkp (bool) -- Sybase backup option for incremental

            Returns:
                dict - JSON request to pass to the API
        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")
        sybase_options = {
            "doNotTruncateLog": donottruncatelog,
            "sybaseSkipFullafterLogBkp": sybaseskipfullafterlogbkp
        }
        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            sybase_options
        )
        return request_json

    @property
    def content(self):
        """Treats the subclient content as a property of the Subclient class."""
        subclient_content = self._content
        sybase_dblist = []
        for item in subclient_content:
            sybase_server_dict = item
            dbname = sybase_server_dict['sybaseContent']['databaseName']
            sybase_dblist.append(dbname)

        return sybase_dblist

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add a new Sybase Subclient
            with the content passed in subclient content.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        content_new = []
        for dbname in subclient_content:
            sybase_server_dict = {"sybaseContent": {"databaseName": dbname}}
            content_new.append(sybase_server_dict)
        self._set_subclient_properties("_content", content_new)

    def backup(self, backup_level=r'full', donottruncatelog=False, sybaseskipfullafterlogbkp=False):
        """

        Args:
            backup_level (str)  -- Level of backup. Can be full, incremental or differential
             default: full

        Returns:
            object -- instance of Job class

        Raises:
            SDKException:
                if backup level is incorrect

                if response is empty

                if response does not succeed

        """
        if backup_level.lower() not in ['full', 'incremental', 'differential']:
            raise SDKException(r'Subclient', r'103')

        if backup_level.lower() == 'incremental':
            donottruncatelog = donottruncatelog
            sybaseskipfullafterlogbkp = sybaseskipfullafterlogbkp
        else:
            donottruncatelog = False
            sybaseskipfullafterlogbkp = False

        request_json = self._sybase_backup_request_json(
            backup_level.lower(), donottruncatelog, sybaseskipfullafterlogbkp)

        backup_service = self._commcell_object._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service, request_json
        )
        return self._process_backup_response(flag, response)
