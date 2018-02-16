# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
File for operating on a Oracle Instance.

OracleInstance is the only class defined in this file.

OracleInstance: Derived class from Instance Base class, representing an
                            oracle instance, and to perform operations on that instance

OracleInstance:

    __init__()                  -- Constructor for the class

    _get_browse_options         -- Method to get browse options for oracle instance

    _process_browse_response    -- Method to process browse response

    oracle_home()               -- Getter for $ORACLE_HOME of this instance

    version()                   -- Getter for oracle database version

    is_catalog_enabled()        -- Getter to check if catalog is enabled for backups

    catalog_user()              -- Getter for getting catalog user

    catalog_db()                -- Getter for catalog database name

    archive_log_dest()          -- Getter for archivelog destination

    os_user()                   -- Getter for OS user owning oracle software

    cmd_sp()                    -- Getter for command line storage policy

    log_sp()                    -- Getter for log storage policy

    is_autobackup_on()          -- Getter to check if autobackup is enabled

    db_user()                   -- Getter for SYS database user name

    tns_name()                  -- Getter for TNS connect string

    dbid()                      -- Getter for getting DBID of database

    restore()                   -- Method to restore the instance

"""
from __future__ import unicode_literals

import json

from ..instance import Instance
from ..exception import SDKException


class OracleInstance(Instance):
    """
    Class to represent a standalone Oracle Instance
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Constructor for the class

        Args:
            agent_object    -- instance of the Agent class
            instance_name   -- name of the instance
            instance_id     --  id of the instance

        """
        super(OracleInstance, self).__init__(agent_object, instance_name, instance_id)
        self._instanceprop = {}  # instance variable to hold instance properties

    def _get_oracle_restore_json(self, destination_client,
                                 instance_name, tablespaces,
                                 common_options, oracle_options):
        """
        Gets the basic restore JSON from base class and modifies it for oracle

        Returns: dict -- JSON formatted options to restore the oracle database

        Args:
            destination_client (str) -- Destination client name
            instance_name (str) -- instance name to restore
            tablespaces (list) -- tablespace name list
            common_options (dict) --  dict containing common options
            oracle_options (dict) --  dict containing other oracle options

        """
        if not isinstance(tablespaces, list):
            raise TypeError('Expecting a list for tablespaces')
        destination_id = int(self._commcell_object.clients.get(
            destination_client).client_id)
        tslist = ["SID: {0} Tablespace: {1}".format(instance_name, ts) for ts in tablespaces]
        restore_json = self._restore_json(paths=r'/')
        if common_options is not None:
            restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
                "commonOptions"] = common_options
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["oracleOpt"] = oracle_options
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["fileOption"] = {
            "sourceItem": tslist
        }
        return restore_json

    def _get_browse_options(self):
        """Method to return the database instance properties for browse and restore"""
        return {
            "path": "/",
            "entity": {
                "appName": self._properties['instance']['appName'],
                "instanceId": int(self.instance_id),
                "applicationId": int(self._properties['instance']['applicationId']),
                "clientId": int(self._properties['instance']['clientId']),
                "instanceName": self._properties['instance']['instanceName'],
                "clientName": self._properties['instance']['clientName']
            }
        }

    def _process_browse_response(self, request_json):
        """Runs the DBBrowse API with the request JSON provided for Browse,
            and returns the contents after parsing the response.

            Args:
                request_json    (dict)  --  JSON request to run for the API

            Returns:
                list - list containing tablespaces for the instance

            Raises:
                SDKException:
                    if browse job failed

                    if browse is empty

                    if browse is not success
        """
        if 'tablespaces' in self._instanceprop:
            return self._instanceprop['tablespaces']

        browse_service = self._commcell_object._services['ORACLE_INSTANCE_BROWSE'] % (
            self.instance_id
        )

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', browse_service, request_json
        )

        if flag:
            response_data = json.loads(response.text)
            if response_data:
                if "oracleContent" in response_data:
                    self._instanceprop['tablespaces'] = response_data["oracleContent"]
                    return self._instanceprop['tablespaces']
                elif "errorCode" in response_data:
                    error_message = response_data['errorMessage']
                    o_str = 'Browse job failed\nError: "{0}"'.format(error_message)
                    raise SDKException('Instance', '102', o_str)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def oracle_home(self):
        """
        getter for oracle home

        Returns:
            string - string of oracle_home

        """
        return self._properties['oracleInstance']['oracleHome']

    @property
    def is_catalog_enabled(self):
        """
        Getter to check if catalog has been enabled

        Returns:
            Bool - True if catalog is enabled. Else False.

        """
        return self._properties['oracleInstance']['useCatalogConnect']

    @property
    def catalog_user(self):
        """
        Getter for catalog user

        Returns:
            string  - String containing catalog user

        Raises:
            SDKException:
                if not set

                if catalog is not enabled

        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['userName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102', 'Catalog user not set - {}'.format(error_str))

    @property
    def catalog_db(self):
        """
        Getter for catalog database

        Returns:
            string  - String containing catalog database

        Raises:
            SDKException:
                if not set

                if catalog is not enabled

        """
        if not self.is_catalog_enabled:
            raise SDKException('Instance', r'102', 'Catalog is not enabled.')
        try:
            return self._properties['oracleInstance']['catalogConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102',
                               'Catalog database not set - {}'.format(error_str))

    @property
    def os_user(self):
        """
        Getter for oracle software owner

        Returns:
            string - string of oracle software owner

        """
        return self._properties['oracleInstance']['oracleUser']['userName']

    @property
    def version(self):
        """
        Getter for oracle version

        Returns:
            string - string of oracle instance version

        """
        return self._properties['version']

    @property
    def archive_log_dest(self):
        """
        Getter for the instance's archive log dest

        Returns:
            string - string for archivelog location

        """
        return self._properties['oracleInstance']['archiveLogDest']

    @property
    def cmd_sp(self):
        """
        Getter for Command Line storage policy

        Returns:
            string - string for command line storage policy

        """
        return self._properties['oracleInstance']['oracleStorageDevice'][
            'commandLineStoragePolicy']['storagePolicyName']

    @property
    def log_sp(self):
        """
        Oracle Instance's Log Storage Poplicy

        Returns:
            string  -- string containing log storage policy

        """
        return self._properties['oracleInstance']['oracleStorageDevice'][
            'logBackupStoragePolicy']['storagePolicyName']

    @property
    def is_autobackup_on(self):
        """
        Getter to check whether autobackup is set to ON

        Returns:
            Bool - True if autobackup is set to ON. Else False.

        """
        return True if self._properties['oracleInstance']['ctrlFileAutoBackup'] == 1 else False

    @property
    def db_user(self):
        """
        Getter to get the database user used to log into the database

        Returns: Oracle database user for the instance

        """
        return self._properties['oracleInstance']['sqlConnect']['userName']

    @property
    def tns_name(self):
        """
        Getter to get the TNS Names of the database

        Returns:
            string  -- TNS name of the instance configured

        Raises:
            SDKException:
                if not set

        """
        try:
            return self._properties['oracleInstance']['sqlConnect']['domainName']
        except KeyError as error_str:
            raise SDKException('Instance', r'102',
                               'Instance TNS Entry not set - {}'.format(error_str))

    @property
    def dbid(self):
        """
        Getter to get the DBID of the database instance

        Returns: DBID of the oracle database

        """
        return self._properties['oracleInstance']['DBID']

    @property
    def tablespaces(self):
        """
        Getter for listing out all tablespaces for the instance

        Returns:
            list -- list containing tablespace names for the database

        """
        return [ts['tableSpace'] for ts in self.browse()]

    def browse(self, *args, **kwargs):
        """Overridden method to browse oracle database tablespaces"""
        if args and isinstance(args[0], dict):
            options = args[0]
        elif kwargs:
            options = kwargs
        else:
            options = self._get_browse_options()
        return self._process_browse_response(options)

    def backup(self, subclient_name=r"default"):
        """Uses the default subclient to backup the database

        Args:
            subclient_name (str) -- name of subclient to use
                default: default
        """
        return self.subclients.get(subclient_name).backup(r'full')

    def restore(self, destination_client=None, common_options = None, oracle_options=None):
        """
        Method to restore the entire database using latest backup

        Args:
            destination_client (str) -- destination client name
            common_options(dict): dictionary containing common options
                default -- None
            oracle_options (dict): dictionary containing other oracle options
                default -- By default it restores the controlfile and datafiles
                                from latest backup
                Example: {
                            "resetLogs": 1,
                            "switchDatabaseMode": True,
                            "noCatalog": True,
                            "restoreControlFile": True,
                            "recover": True,
                            "recoverFrom": 3,
                            "restoreData": True,
                            "restoreFrom": 3
                        }
        Returns:
            object -- Job containing restore details
        """
        if oracle_options is None:
            oracle_options = {
                "resetLogs": 1,
                "switchDatabaseMode": True,
                "noCatalog": True,
                "restoreControlFile": True,
                "recover": True,
                "recoverFrom": 3,
                "restoreData": True,
                "restoreFrom": 3
            }

        if not isinstance(oracle_options, dict):
            raise TypeError('Expecting a dict for oracle_options')

        try:
            if destination_client is None:
                destination_client = self._properties['instance']['clientName']
        except SDKException:
            raise
        else:
            # subclient = self.subclients.get(subclient_name)
            options = self._get_oracle_restore_json(destination_client=destination_client,
                                                    instance_name=self.instance_name,
                                                    tablespaces=self.tablespaces,
                                                    common_options=common_options,
                                                    oracle_options=oracle_options)
            return self._process_restore_response(options)
