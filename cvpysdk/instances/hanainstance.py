#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a SAP HANA Instance.

SAPHANAInstance is the only class defined in this file.

SAPHANAInstance: Derived class from Instance Base class, representing a hana server instance,
                       and to perform operations on that instance

SAPHANAInstance:
    _restore_request_json()         --  returns the restore request json

    _get_hana_restore_options()     --  returns the dict containing destination SAP HANA instance
                                            names for the given client

    _process_restore_response()      --  processes response received for Restore request

    _run_backup()                   --  runs full backup for this subclients and appends the
                                            job object to the return list

    backup()                        --  runs full backup for all subclients associated
                                            with this instance

    restore()                       --  runs the restore job for specified instance

"""
from __future__ import unicode_literals

from past.builtins import basestring

import time
import threading

from ..instance import Instance
from ..exception import SDKException
from ..job import Job


class SAPHANAInstance(Instance):
    """Derived class from Instance Base class, representing a SAP HANA instance,
        and to perform operations on that Instance."""

    def _restore_request_json(
            self,
            destination_client,
            destination_instance,
            backup_prefix=None,
            point_in_time=None,
            initialize_log_area=False,
            use_hardware_revert=False,
            clone_env=False,
            check_access=False,
            destination_instance_dir=None,
            ignore_delta_backups=False,
            backupset_name="default"):
        """Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
                destination_client          (str)       -- The HANA client where the database
                                                                should be restored

                destination_instance        (str)       -- The destination instance where the
                                                                database should be restored

                backupset_name               (str)       -- The backupset name of the instance to
                                                                be restored. If the instance
                                                                is a single DB instance then the
                                                                backupset is default by default.
                    default: default

                backup_prefix               (str)       -- The prefix of the backup job
                    default: None

                point_in_time               (str)       -- The time to which the database should
                                                                be restored to
                    default: None

                initialize_log_area         (bool)      -- Option to initialize new log area after
                                                                restore
                    default: False

                use_hardware_revert         (bool)      -- Option to do a hardware revert in
                                                                restore
                    default: False

                clone_env                   (bool)      -- Option to decide whether the database
                                                                should be cloned or not
                    default: False

                check_access                (bool)      -- Option to check access during restore
                    default: True

                destination_instance_dir      (str)       -- For snap cross instance restore or
                                                                cross machine restores requires
                                                                HANA data directory
                    default: None

                ignore_delta_backups          (bool)      -- Option to ignore delta backups during
                                                                restore
                    default: True

            Returns:
                dict - JSON request to pass to the API
        """

        self._get_hana_restore_options(destination_client)

        if destination_instance is None:
            destination_instance = self.instance_name
        else:
            if str(destination_instance) not in self.destination_instances_dict:
                raise SDKException(
                    'Instance', '102', 'No Instance exists with name: {0}'.format(
                        str(destination_instance)
                    )
                )

        destination_hana_client = str(self.destination_instances_dict[destination_instance][
            'destHANAClient'])

        if backup_prefix is None:
            backup_prefix = ""

        databases = []
        if backupset_name != "default":
            databases.append(backupset_name)

        if point_in_time is None:
            pit = {}
        else:
            if not isinstance(point_in_time, basestring):
                raise SDKException(
                    'Instance', 103
                )
            pit = {'timeValue': str(point_in_time)}

        request_json = {
            "taskInfo": {
                "associations": [{
                    "suclientName": "",
                    "clientName": str(self._agent_object._client_object.client_name),
                    "appName": str(self._agent_object.agent_name),
                    "instanceName": str(self.instance_name),
                    "backupsetName": backupset_name
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
                                "destDbName": destination_instance,
                                "destPseudoClientName": str(destination_client),
                                "ignoreDeltaBackups": ignore_delta_backups,
                                "destClientName": destination_hana_client,
                                "databases": databases,
                                "pointInTime": pit
                            },
                            "destination": {
                                "destinationInstance": {
                                    "clientName": str(destination_client),
                                    "instanceName": str(destination_instance),
                                    "appName": str(self._agent_object.agent_name)
                                },
                                "destClient": {
                                    "clientName": destination_hana_client
                                }
                            },
                            "browseOption": {
                                "backupset": {
                                    "clientName": str(self._agent_object._client_object.client_name)
                                }
                            }
                        }
                    }
                }]
            }
        }

        if destination_instance_dir is not None:
            instance_dir = {'destinationInstanceDir':destination_instance_dir}
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions'][
                'hanaOpt'].update(instance_dir)

        return request_json

    def _get_hana_restore_options(self, destination_client_name):
        """Runs the /GetDestinationsToRestore API,
            and returns the contents after parsing the response.

            Args:
                destination_client_name   (str)  --  destination client to restore to

            Returns:
                dict - dictionary consisting of the HANA destination server options

            Raises:
                SDKException:
                    if failed to get HANA clients

                    if no client exits on commcell

                    if response is empty

                    if response is not success
        """

        webservice = self._commcell_object._services['RESTORE_OPTIONS']%(
            self._agent_object.agent_id)

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            "GET",
            webservice
        )

        destination_clients_dict = {}

        if flag:
            if response.json():
                if u'genericEntityList' in response.json():
                    generic_entity_list = response.json()[u'genericEntityList']
                    for client_entity in generic_entity_list:
                        clients_dict = {
                            str(client_entity[u'clientName']).lower(): {
                                "clientId": int(client_entity[u'clientId'])
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

        webservice = self._commcell_object._services['GET_ALL_INSTANCES']%(
            destination_clients_dict[destination_client_name]['clientId'])

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            "GET", webservice)

        self.destination_instances_dict = {}

        if flag:
            if response.json():
                if 'instanceProperties' in response.json():
                    for instance in response.json()['instanceProperties']:
                        instances_dict = {
                            str(instance['instance']['instanceName']).lower(): {
                                "instanceId": int(instance['instance']['instanceId']),
                                "clientId": int(instance['instance']['clientId']),
                                "destHANAClient": str(instance['saphanaInstance'][
                                    'DBInstances'][0]['clientName'])
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

    def _process_restore_response(self, request_json):
        """Runs the CreateTask API with the request JSON provided for Restore,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if restore job failed

                    if response is empty

                    if response is not success
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', self._commcell_object._services['RESTORE'], request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    time.sleep(1)
                    return Job(self._commcell_object, response.json()['jobIds'][0])
                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Restore job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Instance', '102', o_str)
                else:
                    raise SDKException('Instance', '102', 'Failed to run the restore job')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _run_backup(self, subclient_name, return_list):
        """Triggers full backup job for the given subclient, and appends its Job object to list
            The SDKExcpetion class instance is appended to the list,
            if any exception is raised while running the backup job for the Subclient.

            Args:
                subclient_name (str)   --  name of the subclient to trigger the backup for

                return_list    (list)  --  list to append the job object to
        """
        try:
            job = self.subclients.get(subclient_name).backup('Full')
            if job:
                return_list.append(job)
        except SDKException as excp:
            return_list.append(excp)

    def backup(self):
        """Run full backup job for all subclients in this instance.

            Returns:
                list - list containing the job objects for the full backup jobs started for
                           the subclients in the backupset
        """
        return_list = []
        thread_list = []

        all_subclients = self.subclients._subclients

        if all_subclients:
            for subclient in all_subclients:
                thread = threading.Thread(
                    target=self._run_backup, args=(subclient, return_list)
                )
                thread_list.append(thread)
                thread.start()

        for thread in thread_list:
            thread.join()

        return return_list

    def restore(
            self,
            pseudo_client,
            instance,
            backup_prefix=None,
            point_in_time=None,
            initialize_log_area=False,
            use_hardware_revert=False,
            clone_env=False,
            check_access=True,
            destination_instance_dir=None,
            ignore_delta_backups=True,
            backupset_name="default"):
        """Restores the databases specified in the input paths list.

            Args:
                pseudo_client                (str)       -- The HANA client where the database
                                                                should be restored

                instance                    (str)       -- The destination instance where the
                                                                database should be restored

                backupset_name               (str)       -- The backupset name of the instance to
                                                                be restored. If the instance is a
                                                                single DB instance then the
                                                                backupset is default by default.
                    default: default

                backup_prefix               (str)       -- The prefix of the backup job
                    default: None

                point_in_time               (str)       -- The time to which the database should be
                                                                restored to
                    default: None

                initialize_log_area         (bool)      -- Option to initialize new log area after
                                                                restore
                    default: False

                use_hardware_revert         (bool)      -- Option to do a hardware revert in
                                                                restore
                    default: False

                clone_env                   (bool)      -- Option to decide whether the database
                                                                should be cloned or not
                    default: False

                check_access                (bool)      -- Option to check access during restore
                    default: True

                destination_instance_dir      (str)       -- For snap cross instance restore or
                                                                cross machine restores requires
                                                                HANA data directory
                    default: None

                ignore_delta_backups          (bool)      -- Option to ignore delta backups during
                                                                restore
                    default: True

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if instance is not a string or object

                    if response is empty

                    if response is not success
        """
        if not (isinstance(instance, str) or isinstance(instance, basestring)):
            raise SDKException('Instance', '101')

        request_json = self._restore_request_json(
            pseudo_client,
            instance,
            backup_prefix,
            point_in_time,
            initialize_log_area,
            use_hardware_revert,
            clone_env,
            check_access,
            destination_instance_dir,
            ignore_delta_backups,
            backupset_name
        )

        return self._process_restore_response(request_json)
