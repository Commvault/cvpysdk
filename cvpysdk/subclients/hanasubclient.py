#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a HANA Server Subclient.

HANAServerSubclient is the only class defined in this file.

HANAServerSubclient: Derived class from Subclient Base class, representing a HANA server subclient,
                        and to perform operations on that subclient

HANAServerSubclient:

    _backup_request_json()              --  prepares the json for the backup request

    _get_subclient_content_()           --  gets the content of a HANA server subclient

    _initialize_subclient_properties()  --  initializes additional properties of this subclient

    content()                           --  update the content of the subclient

    log_backup_storage_policy()         --  updpates the log backup storage policy for this
                                                subclient

    backup()                            --  run a backup job for the subclient

"""
from __future__ import unicode_literals

from past.builtins import basestring

from ..subclient import Subclient
from ..exception import SDKException


class SAPHANASubclient(Subclient):
    """Derived class from Subclient Base class, representing a file system subclient,
        and to perform operations on that subclient."""

    def _backup_request_json(self, backup_level, backup_prefix):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                backup_level    (list)  --  level of backup the user wish to run
                        Full / Incremental / Differential

                backup_prefix   (str)   --  the prefix that the user wish to add to the backup

            Returns:
                dict    -   JSON request to pass to the API
        """
        request_json = {
            "taskInfo": {
                "associations": [{
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "instanceName": self._backupset_object._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": self.subclient_name
                }],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 1
                },
                "subTasks": [{
                    "subTask": {
                        "subTaskType": 2,
                        "operationType": 2
                    },
                    "options": {
                        "backupOpts": {
                            "backupLevel": backup_level,
                            "hanaOptions": {
                                "backupPrefix": backup_prefix
                            }
                        }
                    }
                }]
            }
        }

        return request_json

    def _get_subclient_content_(self):
        """Gets the appropriate content from the Subclient relevant to the user.

            Args:
                subclient_properties (dict)  --  dictionary contatining the properties of
                                                     subclient

            Returns:
                list - list of content associated with the subclient
        """
        contents = []

        if 'content' in self._subclient_properties:
            subclient_content = self._subclient_properties['content']
        else:
            subclient_content = []

        contents.append(subclient_content)

        return contents

    def _initialize_subclient_properties(self):
        """Initializes properties of this subclient"""
        super(SAPHANASubclient, self)._initialize_subclient_properties()

        self._log_backup_storage_policy = None

        storage_device = self._subclient_properties['commonProperties']['storageDevice']

        if 'logBackupStoragePolicy' in storage_device:
            if 'storagePolicyName' in storage_device['logBackupStoragePolicy']:
                self._log_backup_storage_policy = str(
                    storage_device['logBackupStoragePolicy']['storagePolicyName']
                )

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
            'Subclient', '102', 'Updating the content of a SAP HANA subclient is not permitted.'
        )

    @property
    def browse(self):
        raise AttributeError("'{0}' object has no attribute '{1}'".format(
            self.__class__.__name__,
            'browse'
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

    @property
    def log_backup_storage_policy(self):
        """Treats the subclient description as a property of the Subclient class."""
        return self._log_backup_storage_policy

    @log_backup_storage_policy.setter
    def log_backup_storage_policy(self, value):
        """Sets the log backup storage policy of subclient as the value provided as input.

            Args:
                value   (str)   -- Log backup Storage policy name to be assigned to subclient

            Raises:
                SDKException:
                    if failed to update log backup storage policy name

                    if log backup storage policy name is not in string format
        """
        if isinstance(value, basestring):
            if value not in self._commcell_object.storage_policies._policies:
                raise SDKException(
                    'Subclient',
                    '102',
                    'Storage Policy: "{0}" does not exist in the Commcell'.format(value)
                )

            properties_dict = {
                "storageDevice": {
                    "logBackupStoragePolicy": {
                        "storagePolicyName": value
                    }
                }
            }

            request_json = self._update_subclient_props_json(properties_dict)

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._SUBCLIENT, request_json
            )

            output = self._process_update_response(flag, response)

            if output[0]:
                return
            else:
                o_str = ('Failed to update the log backup storage policy of the Subclient'
                         '\nError: "{0}"')
                raise SDKException('Subclient', '102', o_str.format(output[2]))
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient log backup storage policy should be a string value'
            )

    def backup(self, backup_level="Differential", backup_prefix=None):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Differential
                    default: Differential

                backup_prefix       (str)   --  the prefix that the user wish to add to the backup
                    default: None

            Returns:
                object  -   instance of the Job class for this backup job

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

        else:
            request_json = self._backup_request_json(backup_level, backup_prefix)

            flag, response = self._commcell_object._cvpysdk_object.make_request(
                'POST', self._commcell_object._services['CREATE_TASK'], request_json
            )

            return self._process_backup_response(flag, response)
