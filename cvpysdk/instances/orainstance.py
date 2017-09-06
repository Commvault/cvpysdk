#!/usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Oracle Instance.

OracleInstance is the only class defined in this file.

OracleInstance: Derived class from Instance Base class, representing an
                            oracle instance, and to perform operations on that instance


"""
from __future__ import unicode_literals

from ..instance import Instance
from ..client import Client
from ..exception import SDKException
from .. import constants


class OracleInstance(Instance):

    """
    OracleInstance: Class to represent an Oracle Instance
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        __init__: Constructor for the class
        :agent_object: instance of the Agent class
        :instance_name: name of the instance
        :instance_id: id of the instance

        """
        super(OracleInstance, self).__init__(agent_object, instance_name, instance_id)

    @property
    def oracle_home(self):
        """
        oracle_home: getter for oracle home
        :returns: string

        """
        return self._properties['oracleInstance']['oracleHome']

    @property
    def user(self):
        """
        user: Getter for oracle user
        :returns: string

        """
        return self._properties['oracleInstance']['oracleUser']['userName']

    @property
    def version(self):
        """
        version: Getter for oracle version
        :returns: string

        """
        return self._properties['version']

    @property
    def archive_log_dest(self):
        """
        archive_log_dest: Getter for the instance's archive log dest
        :returns: string

        """
        return self._properties['oracleInstance']['archiveLogDest']

    @property
    def cmd_sp(self):
        """
        cmd_sp: Getter for Command Line storage policy
        :returns: string

        """
        return self._properties['oracleInstance']['oracleStorageDevice']['commandLineStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self):
        """
        log_sp: Oracle Instance's Log Storage Poplicy
        :returns: string

        """
        return self._properties['oracleInstance']['oracleStorageDevice']['logBackupStoragePolicy']['storagePolicyName']
        
    @property
    def autobackup_on(self):
        """
        autobackup_on: Getter to check whether autobackup is set to ON
        :returns: Bool

        """
        return True if self._properties['oracleInstance']['ctrlFileAutoBackup'] == 1 else Fase

    def _restore_request_json(self, arg1):
        """
         _restore_request_json: Returns the JSON request to pass to the API as per the options selected by the user.

        :arg1: TODO
        :returns: JSON formatted dict

        """
        pass


    def _process_restore_response(self, arg1):
        """
        _process_restore_response: Runs the CreateTask API with the request JSON provided for Restore and returns the contents after parsing the response.

        :arg1: TODO
        :returns: JSON formatted dict

        """
        pass


    def _get_oracle_restore_options(self, arg1):
        """
        _get_oracle_restore_options: Runs the Oracle Restoreoptions API with the request JSON provided,
            and returns the contents after parsing the response.

        :arg1: TODO
        :returns: JSON formatted dict

        """
        pass


    def _run_backup(self, arg1):
        """
        _run_backup: Triggers full backup job for the given subclient, and appends its Job object to list
            The SDKExcpetion class instance is appended to the list,
            if any exception is raised while running the backup job for the Subclient.

        :arg1: TODO
        :returns: JSON formatted dict

        """
        pass


    def _process_browse_request(self, arg1):
        """
        _process_browse_request: Runs the SQL Instance Browse API with the request JSON provided for the operation
            specified, and returns the contents after parsing the response.

        :arg1: TODO
        :returns: JSON formatted dict

        """
        pass


    def backup(self, arg1):
        """
        backup: Run full backup job for all subclients in this instance.

        :arg1: TODO
        :returns: list containing the job objects for the full backup jobs started for the subclients in the backupset

        """
        pass


    def restore(self, arg1):
        """
        restore: Restores the databases specified in the input paths list.

        :arg1: TODO
        :returns: object - instance of the Job class for this restore job

        """
        pass


    def __str__(self):
        """
        __str__: Dunder to represent the class as string
        :returns: string

        """
        return r'Instance: {} Subclients: {}'.format(self._instance_name, self.subclients)


    def __repr__(self):
        """
        __repr__: Dunder to represent the class as string
        :returns: string

        """
        pass
