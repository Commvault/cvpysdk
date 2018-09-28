# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a SAP HANA Instance.

SAPHANAInstance is the only class defined in this file.

SAPHANAInstance: Derived class from Instance Base class, representing a hana server instance,
                       and to perform operations on that instance

SAPHANAInstance:

    sps_version()                   --  returns the SPS version of the instance

    instance_number()               --  returns the instance number of SAP HANA

    sql_location_directory()        --  returns the SQL location directory of the Instance

    instance_db_username()          --  returns the db username of the instance

    db_instance_client()            --  returns the SAP HANA client associated with the instance

    hdb_user_storekey()             --  returns the HDB user store key if its set

    _restore_request_json()         --  returns the restore request json

    _get_hana_restore_options()     --  returns the dict containing destination SAP HANA instance
                                            names for the given client

    restore()                       --  runs the restore job for specified instance

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import threading

from past.builtins import basestring

from ..instance import Instance
from ..exception import SDKException


class SAPHANAInstance(Instance):
    """Derived class from Instance Base class, representing a SAP HANA instance,
        and to perform operations on that Instance."""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initialize the subclient object

        Args:
            agent_object    (object):       instance of the agent class

            instance_name   (basestring):   name of the instance

            instance_id     (int):          ID of the instance

        """
        super(SAPHANAInstance, self).__init__(agent_object, instance_name, instance_id)
        self.destination_instances_dict = {}

    @property
    def sps_version(self):
        """
        Returns the sps version of the HANA instance

        Returns:
            sps version
        """
        return self._properties['saphanaInstance']['spsVersion']

    @property
    def instance_number(self):
        """
        Returns the instance number of the HANA instance

        Returns:
            instance number
        """
        return self._properties['saphanaInstance']['dbInstanceNumber']

    @property
    def sql_location_directory(self):
        """
        Returns the isql location directory of the HANA instance

        Returns:
            SQL location directory
        """
        return self._properties['saphanaInstance']['hdbsqlLocationDirectory']

    @property
    def instance_db_username(self):
        """
        Returns the username of the HANA instance database

        Returns:
            instance db username
        """
        return self._properties['saphanaInstance']['dbUser']['userName']

    @property
    def db_instance_client(self):
        """
        Returns the client name of the HANA instance

        Returns:
            db instance client name
        """
        return self._properties['saphanaInstance']['DBInstances'][0]

    @property
    def hdb_user_storekey(self):
        """
        Returns the hdb user store key of the HANA instance

        Returns:
            hdb user store key
        """
        return self._properties['saphanaInstance']['hdbuserstorekey']

    def _restore_request_json(
            self,
            destination_client,
            destination_instance,
            backupset_name="default",
            backup_prefix=None,
            point_in_time=None,
            initialize_log_area=False,
            use_hardware_revert=False,
            clone_env=False,
            check_access=False,
            destination_instance_dir=None,
            ignore_delta_backups=False):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                destination_client          (str)   --  HANA client to restore the database at

                destination_instance        (str)   --  destination instance to restore the db at

                backupset_name              (str)   --  backupset name of the instance to be
                                                            restored. If the instance is a single
                                                            DB instance then the backupset name is
                                                            ``default``.
                    default: default

                backup_prefix               (str)   --  prefix of the backup job
                    default: None

                point_in_time               (str)   --  time to which db should be restored to
                    default: None

                initialize_log_area         (bool)  --  boolean to specify whether to initialize
                                                            the new log area after restore
                    default: False

                use_hardware_revert         (bool)  --  boolean to specify whether to do a
                                                            hardware revert in restore
                    default: False

                clone_env                   (bool)  --  boolean to specify whether the database
                                                            should be cloned or not
                    default: False

                check_access                (bool)  --  check access during restore or not
                    default: True

                destination_instance_dir    (str)   --  HANA data directory for snap cross instance
                                                            restore or cross machine restores
                    default: None

                ignore_delta_backups        (bool)  --  whether to ignore delta backups during
                                                            restore or not
                    default: True

            Returns:
                dict    -   JSON request to pass to the API

        """
        self._get_hana_restore_options(destination_client)

        if destination_instance is None:
            destination_instance = self.instance_name
        else:
            if destination_instance not in self.destination_instances_dict:
                raise SDKException(
                    'Instance', '102', 'No Instance exists with name: {0}'.format(
                        destination_instance
                    )
                )

        destination_hana_client = self.destination_instances_dict[destination_instance][
            'destHANAClient']

        if backup_prefix is None:
            backup_prefix = ""

        databases = []

        if backupset_name != "default":
            databases.append(backupset_name)

        if point_in_time is None:
            recover_time = 0
            point_in_time = {}
        else:
            if not isinstance(point_in_time, basestring):
                raise SDKException('Instance', 103)

            point_in_time = {
                'time': int(point_in_time)
            }
            recover_time = 1

        request_json = {
            "taskInfo": {
                "associations": [{
                    "clientName": self._agent_object._client_object.client_name,
                    "appName": self._agent_object.agent_name,
                    "instanceName": self.instance_name.upper(),
                    "backupsetName": backupset_name,
                    "suclientName": ""
                }],
                "task": {
                    "initiatedFrom": 1,
                    "taskType": 1
                },
                "subTasks": [{
                    "subTask": {
                        "subTaskType": 3,
                        "operationType": 1001
                    },
                    "options": {
                        "restoreOptions": {
                            "hanaOpt": {
                                "initializeLogArea": initialize_log_area,
                                "useHardwareRevert": use_hardware_revert,
                                "cloneEnv": clone_env,
                                "checkAccess": check_access,
                                "backupPrefix": backup_prefix,
                                "destDbName": destination_instance.upper(),
                                "destPseudoClientName": str(destination_client),
                                "ignoreDeltaBackups": ignore_delta_backups,
                                "destClientName": destination_hana_client,
                                "databases": databases,
                                "recoverTime": recover_time,
                                "pointInTime": point_in_time
                            },
                            "destination": {
                                "destinationInstance": {
                                    "clientName": destination_client,
                                    "appName": self._agent_object.agent_name,
                                    "instanceName": destination_instance
                                },
                                "destClient": {
                                    "clientName": destination_hana_client
                                }
                            },
                            "browseOption": {
                                "backupset": {
                                    "clientName": self._agent_object._client_object.client_name
                                }
                            }
                        }
                    }
                }]
            }
        }

        if destination_instance_dir is not None:
            instance_dir = {
                'destinationInstanceDir': destination_instance_dir
            }

            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'hanaOpt'].update(instance_dir)

        return request_json

    def _get_hana_restore_options(self, destination_client_name):
        """Runs the /GetDestinationsToRestore API,
            and returns the contents after parsing the response.

            Args:
                destination_client_name     (str)   --  destination client to restore to

            Returns:
                dict    -   dictionary consisting of the HANA destination server options

            Raises:
                SDKException:
                    if failed to get HANA clients

                    if no client exits on commcell

                    if response is empty

                    if response is not success

        """
        webservice = self._commcell_object._services['RESTORE_OPTIONS'] % (
            self._agent_object.agent_id
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request("GET", webservice)

        destination_clients_dict = {}

        if flag:
            if response.json():
                if 'genericEntityList' in response.json():
                    generic_entity_list = response.json()['genericEntityList']

                    for client_entity in generic_entity_list:
                        clients_dict = {
                            client_entity['clientName'].lower(): {
                                "clientId": client_entity['clientId']
                            }
                        }
                        destination_clients_dict.update(clients_dict)
                elif 'error' in response.json():
                    if 'errorMessage' in response.json()['error']:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Client', '102', error_message)
                    else:
                        raise SDKException('Client', '102', 'No client exists on commcell')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        webservice = self._commcell_object._services['GET_ALL_INSTANCES'] % (
            destination_clients_dict[destination_client_name]['clientId']
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request("GET", webservice)

        if flag:
            if response.json():
                if 'instanceProperties' in response.json():
                    for instance in response.json()['instanceProperties']:
                        instances_dict = {
                            instance['instance']['instanceName'].lower(): {
                                "clientId": instance['instance']['clientId'],
                                "instanceId": instance['instance']['instanceId'],
                                "destHANAClient": instance['saphanaInstance'][
                                    'DBInstances'][0]['clientName']
                            }
                        }
                        self.destination_instances_dict.update(instances_dict)
                elif 'error' in response.json():
                    if 'errorMessage' in response.json()['error']:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Instance', '102', error_message)
                    else:
                        raise SDKException('Instance', '102', 'No Instance exists on commcell')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def restore(
            self,
            pseudo_client,
            instance,
            backupset_name="default",
            backup_prefix=None,
            point_in_time=None,
            initialize_log_area=False,
            use_hardware_revert=False,
            clone_env=False,
            check_access=True,
            destination_instance_dir=None,
            ignore_delta_backups=True):
        """Restores the databases specified in the input paths list.

            Args:
                pseudo_client               (str)   --  HANA client to restore the database at

                instance                    (str)   --  destination instance to restore the db at

                backupset_name              (str)   --  backupset name of the instance to be
                                                            restored. If the instance is a single
                                                            DB instance then the backupset name is
                                                            ``default``.
                    default: default

                backup_prefix               (str)   --  prefix of the backup job
                    default: None

                point_in_time               (str)   --  time to which db should be restored to
                    default: None

                initialize_log_area         (bool)  --  boolean to specify whether to initialize
                                                            the new log area after restore
                    default: False

                use_hardware_revert         (bool)  --  boolean to specify whether to do a
                                                            hardware revert in restore
                    default: False

                clone_env                   (bool)  --  boolean to specify whether the database
                                                            should be cloned or not
                    default: False

                check_access                (bool)  --  check access during restore or not
                    default: True

                destination_instance_dir    (str)   --  HANA data directory for snap cross instance
                                                            restore or cross machine restores
                    default: None

                ignore_delta_backups        (bool)  --  whether to ignore delta backups during
                                                            restore or not
                    default: True

            Returns:
                object  -   instance of the Job class for this restore job

            Raises:
                SDKException:
                    if instance is not a string or object

                    if response is empty

                    if response is not success

        """
        if not isinstance(instance, (basestring, Instance)):
            raise SDKException('Instance', '101')

        request_json = self._restore_request_json(
            pseudo_client,
            instance,
            backupset_name,
            backup_prefix,
            point_in_time,
            initialize_log_area,
            use_hardware_revert,
            clone_env,
            check_access,
            destination_instance_dir,
            ignore_delta_backups
        )

        return self._process_restore_response(request_json)
