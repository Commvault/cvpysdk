# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a HANA Server Subclient

HANAServerSubclient is the only class defined in this file.

HANAServerSubclient: Derived class from Subclient Base class, representing a HANA server subclient,
                        and to perform operations on that subclient

HANAServerSubclient:
    _backup_request_json()               --  prepares the json for the backup request

    _get_subclient_properties()          --  gets the subclient  related properties of
                                                SAP HANA subclient.

    backup()                             --  run a backup job for the subclient

"""
from __future__ import unicode_literals
from .dbsubclient import DatabaseSubclient
from ..exception import SDKException


class SAPHANASubclient(DatabaseSubclient):
    """Derived class from Subclient Base class, representing a SAP HANA subclient,
        and to perform operations on that subclient."""

    def _backup_request_json(
            self,
            backup_level,
            backup_prefix=None):
        """
        Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                backup_level   (list)  --  level of backup the user wish to run
                        Full / Incremental / Differential
                backup_prefix   (str)   --  the prefix that the user wish to add to the backup

            Returns:
                dict - JSON request to pass to the API
        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")
        hana_options = {
            "hanaOptions": {
                "backupPrefix": str(backup_prefix)
            }
        }
        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(hana_options)

        return request_json

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of SAP HANA subclient."""
        super(SAPHANASubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

    @property
    def content(self):
        """Treats the subclient content as a property of the Subclient class."""
        return self._content

    @content.setter
    def content(self, value):
        """Sets the content of the subclient as the value provided as input.

            Raises:
                SDKException:
                    if failed to update content of subclient

                    if the type of value input is not list

                    if value list is empty
        """
        raise SDKException(
            'Subclient',
            '102',
            ('Updating SAP HANA subclient Content is not allowed. ')
            )

    @property
    def browse(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'browse'
        ))

    @property
    def browse_in_time(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'browse_in_time'
        ))

    @property
    def find(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'find'
        ))

    @property
    def restore_in_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'restore_in_place'
        ))

    @property
    def restore_out_of_place(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'restore_out_of_place'
        ))

    def backup(
            self,
            backup_level="Differential",
            backup_prefix=None):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential
                    default: Differential

                backup_prefix       (str)   --  the prefix that the user wish to add to the backup
                    default: None

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success

        """
        backup_level = backup_level.lower()

        if backup_level not in ['full', 'incremental', 'differential']:
            raise SDKException('Subclient', '103')

        if backup_prefix is None:
            return super(SAPHANASubclient, self).backup(backup_level)

        request_json = self._backup_request_json(backup_level, backup_prefix)
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['CREATE_TASK'], request_json
        )
        return self._process_backup_response(flag, response)
