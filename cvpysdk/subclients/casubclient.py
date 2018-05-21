# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Cloud Apps Subclient.

CloudAppsSubclient is the only class defined in this file.

CloudAppsSubclient: Derived class from Subclient Base class, representing a
                        cloud apps subclient, and to perform operations on that subclient

CloudAppsSubclient:

    __new__()   --  Method to create object based on specific cloud apps instance type


    restore_in_place()        --     Restores the files/folders specified in the
    input paths list to the same location

    restore_out_of_place()    --     Restores the files/folders specified in the input paths list
    to the input client, at the specified destination location

    restore_to_fs()           --     Restores the files/folders specified in the input paths
    list to the input fs client, at the specified destination location.

    backup()                  --     Runs backup for S3 subclient

    add_subclient()           --     Adds a new subclient to the cloud apps instance

"""

from __future__ import unicode_literals

from ..subclient import Subclient
from ..exception import SDKException
from past.builtins import basestring


class CloudAppsSubclient(Subclient):
    """Class for representing a subclient of the Cloud Apps agent."""

    def __new__(cls, backupset_object, subclient_name, subclient_id=None):
        from .cloudapps.google_subclient import GoogleSubclient
        from .cloudapps.s3_subclient import S3Subclient

        instance_types = {
            1: GoogleSubclient,
            2: GoogleSubclient,
            5: S3Subclient
        }

        cloud_apps_instance_type = backupset_object._instance_object._properties[
            'cloudAppsInstance']['instanceType']

        if cloud_apps_instance_type in instance_types:
            instance_type = instance_types[cloud_apps_instance_type]
        else:
            raise SDKException(
                'Subclient', '102', 'Subclient for this instance type is not yet implemented'
            )

        return object.__new__(instance_type)

    def restore_in_place(self, paths, overwrite=True, copy_precedence=None):
        """
            Restores the files/folders specified in the input paths list to the same location.

            Args:
                 paths                   (list)  --  list of full paths of files/folders to restore

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

            Returns:
                object - instance of the Job class for this restore job
        """

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        return self._backupset_object._instance_object._restore_in_place(
            paths=paths,
            destination_client=None,
            destination_instance_name=None,
            overwrite=overwrite,
            in_place=True,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=False
        )

    def restore_out_of_place(
            self,
            paths,
            destination_client,
            destination_instance_name,
            destination_path,
            overwrite=True,
            copy_precedence=None):
        """
            Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                destination_client      (str)   --  name of the client to which the files are
                    to be restored.
                    default: None for in place restores

                destination_instance_name(str)  --  name of the instance to which the files are
                    to be restored.
                    default: None for in place restores

                destination_path         (str)  --  location where the files are to be restored
                    in the destination instance.

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

            Returns:
                object - instance of the Job class for this restore job

        """

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        return self._backupset_object._instance_object._restore_out_of_place(
            paths=paths,
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            destination_path=destination_path,
            overwrite=overwrite,
            in_place=False,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=False
        )

    def restore_to_fs(
            self,
            paths,
            destination_path,
            destination_client=None,
            overwrite=True,
            copy_precedence=None):
        """
            Restores the files/folders specified in the input paths list to the input client,
            at the specified destionation location.

            Args:
                paths                   (list)  --  list of full paths of files/folders to restore

                destination_path         (str)  --  location where the files are to be restored
                    in the destination instance.

                destination_client      (str)   --  name of the fs client to which the files
                    are to be restored.
                    default: None for restores to backup or proxy client.

                overwrite               (bool)  --  unconditional overwrite files during restore
                    default: True

                copy_precedence         (int)   --  copy precedence value of storage policy copy
                    default: None

            Returns:
                object - instance of the Job class for this restore job

            """

        self._backupset_object._instance_object._restore_association = self._subClientEntity

        if destination_client is None:
            destination_client = self._backupset_object._instance_object.backup_client

        return self._backupset_object._instance_object._restore_to_fs(
            paths=paths,
            destination_path=destination_path,
            destination_client=destination_client,
            overwrite=overwrite,
            in_place=False,
            copy_precedence=copy_precedence,
            restore_To_FileSystem=True)

    def backup(self,
               backup_level="Incremental",
               incremental_backup=False,
               incremental_level='BEFORE_SYNTH'
              ):
        """Runs a backup job for the subclient of the level specified.

            Args:
                backup_level        (str)   --  level of backup the user wish to run
                        Full / Incremental / Synthetic_full
                    default: Incremental

                incremental_backup  (bool)  --  run incremental backup
                        only applicable in case of Synthetic_full backup
                    default: False

                incremental_level   (str)   --  run incremental backup before/after synthetic full
                        BEFORE_SYNTH / AFTER_SYNTH

                        only applicable in case of Synthetic_full backup
                    default: BEFORE_SYNTH

                on_demand_input     (str)   --  input directive file location for on
                                                    demand subclient

                        only applicable in case of on demand subclient
                    default: None

                advacnced_options   (dict)  --  advanced backup options to be included while
                                                    making the request
                        default: None

                        options:
                            directive_file          :   path to the directive file
                            adhoc_backup            :   if set triggers the adhoc backup job
                            adhoc_backup_contents   :   sets the contents for adhoc backup

            Returns:
                object - instance of the Job class for this backup job

            Raises:
                SDKException:
                    if backup level specified is not correct

                    if response is empty

                    if response is not success
        """

        return super(CloudAppsSubclient, self).backup(backup_level=backup_level,
                                                      incremental_backup=incremental_backup,
                                                      incremental_level=incremental_level)

    def add_subclient(self, subclient_name, content, storage_policy, description=''):
        """Adds a new subclient to the instance.

            Args:
                subclient_name      (str)   --  name of the new subclient to add

                storage_policy      (str)   --  name of the storage policy to
                                                    associate with the subclient

                description         (str)   --  description for the subclient (optional)

            Returns:
                object - instance of the Subclient class

            Raises:
                SDKException:
                    if subclient name argument is not of type string

                    if storage policy argument is not of type string

                    if description argument is not of type string

                    if failed to create subclient

                    if response is empty

                    if response is not success

                    if subclient already exists with the given name
        """
        if not (isinstance(subclient_name, basestring) and
                isinstance(storage_policy, basestring) and
                isinstance(description, basestring)):
            raise SDKException('Subclient', '101')

        if self.has_subclient(subclient_name):
            raise SDKException(
                'Subclient', '102', 'Subclient "{0}" already exists.'.format(subclient_name)
            )

        if self._backupset_object is None:
            if self._instance_object.backupsets.has_backupset('defaultBackupSet'):
                self._backupset_object = self._instance_object.backupsets.get('defaultBackupSet')
            else:
                self._backupset_object = self._instance_object.backupsets.get(
                    sorted(self._instance_object.backupsets._backupsets)[0]
                )

        if not self._commcell_object.storage_policies.has_policy(storage_policy):
            raise SDKException(
                'Subclient',
                '102',
                'Storage Policy: "{0}" does not exist in the Commcell'.format(storage_policy)
            )

        request_json = {
            "subClientProperties": {
                "contentOperationType": 2,
                "subClientEntity": {
                    "clientName": self._backupset_object._agent_object._client_object.client_name,
                    "appName": self._backupset_object._agent_object.agent_name,
                    "instanceName": self._instance_object.instance_name,
                    "backupsetName": self._backupset_object.backupset_name,
                    "subclientName": subclient_name
                },
                "cloudAppsSubClientProp": {
                    "instanceType": int(self.Instance_id)
                },
                "content": content,
                "commonProperties": {
                    "description": description,
                    "enableBackup": True,
                    "storageDevice": {
                        "dataBackupStoragePolicy": {
                            "storagePolicyName": storage_policy
                        }
                    }
                }
            }
        }

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._ADD_SUBCLIENT, request_json
        )

        if flag:
            if response.json() and 'response' in response.json():
                error_code = response.json()['response']['errorCode']

                if error_code != 0:
                    error_string = response.json()['response']['errorString']
                    raise SDKException(
                        'Subclient',
                        '102',
                        'Failed to create subclient\nError: "{0}"'.format(error_string)
                    )
                else:
                    subclient_id = response.json()['response']['entity']['subclientId']

                    # initialize the subclients again
                    # so the subclient object has all the subclients
                    self.refresh()

                    agent_name = self._backupset_object._agent_object.agent_name

                    return self._subclients_dict[agent_name](
                        self._backupset_object, subclient_name, subclient_id
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)
