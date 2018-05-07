# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a MYSQL Subclient

MYSQLSubclient is the only class defined in this file.

MYSQLSubclient: Derived class from Subclient Base class, representing a MYSQL subclient,
                        and to perform operations on that subclient

MYSQLSubclient:
    __init__()                          --  constructor for the class

    _get_subclient_properties()         --  initializes the subclient related properties of
                                                 MYSQL subclient

    _get_subclient_properties_json()    --  gets all the subclient related properties of
                                                 MYSQL subclient

    content()                           --  gets the appropriate content from the Subclient

    restore_in_place()                  --  gets the restore json and pass the json for
                                                restore process
"""

from __future__ import unicode_literals

from ..subclient import Subclient
from .dbsubclient import DatabaseSubclient


class MYSQLSubclient(Subclient):
    """Derived class from Subclient Base class, representing a MYSQL subclient,
        and to perform operations on that subclient.
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialise the Subclient object.

            Args:
                backupset_object (object)  --  instance of the Backupset class

                subclient_name   (str)     --  name of the subclient

                subclient_id     (str)     --  id of the subclient
                    default: None

            Returns:
                object - instance of the MYSQLSubclient class
        """
        self.mysql_subclient_prop = None
        self.dfs_subclient_prop = None
        self.plan_entity = None
        self.cassandra_props = None
        self.analytics_subclient_prop = None
        super(MYSQLSubclient, self).__init__(backupset_object, subclient_name, subclient_id)

    def _get_subclient_properties(self):
        """Gets the subclient related properties of MYSQL subclient.

        """
        super(MYSQLSubclient, self)._get_subclient_properties()
        if 'mySqlSubclientProp' in self._subclient_properties:
            self.mysql_subclient_prop = self._subclient_properties['mySqlSubclientProp']
        if 'dfsSubclientProp' in self._subclient_properties:
            self.dfs_subclient_prop = self._subclient_properties['dfsSubclientProp']
        if 'planEntity' in self._subclient_properties:
            self.plan_entity = self._subclient_properties['planEntity']
        if 'cassandraProps' in self._subclient_properties:
            self.cassandra_props = self._subclient_properties['cassandraProps']
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']
        if 'analyticsSubclientProp' in self._subclient_properties:
            self.analytics_subclient_prop = self._subclient_properties['analyticsSubclientProp']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "mySqlSubclientProp": self.mysql_subclient_prop,
                    "subClientEntity": self._subClientEntity,
                    "dfsSubclientProp": self.dfs_subclient_prop,
                    "planEntity": self.plan_entity,
                    "cassandraProps": self.cassandra_props,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "analyticsSubclientProp": self.analytics_subclient_prop,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def content(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Returns:
                list - list of content associated with the subclient
        """
        cont = []

        # Getting the database names from subclient content details
        for path in self._content:
            for key, value in path.items():
                if key == "mySQLContent":
                    cont.append(value["databaseName"])
        return cont

    @content.setter
    def content(self, subclient_content):
        """Creates the list of content JSON to pass to the API to add/update content of a
            MYSQL Subclient.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                list - list of the appropriate JSON for an agent to send to the POST Subclient API
        """
        cont = []
        for mysql_cont in subclient_content:
            mysql_dict = {
                "mySQLContent": {
                    "databaseName": mysql_cont
                }
            }
            cont.append(mysql_dict)

        self._set_subclient_properties("_content", cont)

    def restore_in_place(
            self,
            paths,
            staging,
            dest_client_name,
            dest_instance_name,
            data_restore,
            log_restore,
            overwrite=True,
            copy_precedence=None,
            from_time=None,
            to_time=None):
        """Restores the mysql data/log files specified in the input paths list to the same location.

            Args:
                paths               (list)  --  list of database/databases to be restored

                staging             (str)   --  staging location for mysql logs during restores

                dest_client_name    (str)   --  destination client name where files are
                                                        to be restored

                dest_instance_name  (str)   --  destination mysql instance name of
                                                        destination client

                data_restore        (bool)  --  for data only/data+log restore

                log_restore         (bool)  --  for log only/data+log restore

                overwrite           (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence     (int)   --  copy precedence value of storage policy copy
                    default: None

                from_time           (str)   --  time to retore the contents after
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

                to_time             (str)   --  time to retore the contents before
                        format: YYYY-MM-DD HH:MM:SS

                    default: None

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if paths is not a list

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        self._backupset_object._instance_object._restore_association = self._subClientEntity

        return self._backupset_object._instance_object.restore_in_place(
            paths,
            staging,
            dest_client_name,
            dest_instance_name,
            data_restore,
            log_restore,
            overwrite,
            copy_precedence,
            from_time,
            to_time
        )
