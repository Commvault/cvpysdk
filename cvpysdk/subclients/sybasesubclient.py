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

    is_snapenabled()                    -- Check if intellisnap has been enabled in the subclient and sets it accordingly

    snap_engine()                       -- updates snap_engine for sybase subclient

    snap_proxy()                        -- updates proxy name from sybase snap operation

    use_dump_based_backup_copy()        -- updates the use of dump based method for backup copy

    dump_based_backup_copy_option()     -- updates subtype of dump based operation

    configured_instance()               -- updates configured instance name for dump based backup copy type 1

    auxiliary_sybase_server()           -- updates custom instance properties for dump based backup copy type 2

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

        if 'snapCopyInfo' in self._commonProperties:
            self._snapCopyInfo = self._commonProperties['snapCopyInfo']

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
                    "contentOperationType": 1,
                    "snapCopyInfo": self._snapCopyInfo
                }
        }

    def _sybase_backup_request_json(
            self,
            backup_level,
            donottruncatelog=False, sybaseskipfullafterlogbkp=False, createbackupcopyimmediately=False, backupcopytype=2):
        """
        Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
               backup_level   (list)  --  level of backup the user wish to run
                        Full / Incremental / Differential

               donottruncatelog (bool) -- Sybase truncate log option for incremental backup

               sybaseskipfullafterlogbkp (bool) -- Sybase backup option for incremental

               createbackupcopyimmediately(bool)  -- Sybase snap job needs this backup copy operation

               backupcopytype(int)            --   backup copy job to be launched based on below two options
                default : 2, possible values : 1 (USING_STORAGE_POLICY_RULE), 2( USING_LATEST_CYCLE)

            Returns:
                dict - JSON request to pass to the API
        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")
        sybase_options = {
            "doNotTruncateLog": donottruncatelog,
            "sybaseSkipFullafterLogBkp": sybaseskipfullafterlogbkp
        }

        if createbackupcopyimmediately is True:
            sub_opt = {"dataOpt":
                       {
                           "createBackupCopyImmediately": createbackupcopyimmediately,
                           "backupCopyType": backupcopytype
                       }
                       }
            sybase_options.update(sub_opt)

        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            sybase_options
        )
        return request_json

    @property
    def is_snapenabled(self):
        """
        Getter to check whether the subclient has snap enabled
        Returns:
            Bool - True if snap is enabled on the subclient. Else False
        """
        return self._snapCopyInfo['isSnapBackupEnabled']

    @is_snapenabled.setter
    def is_snapenabled(self, value):
        """Method to set is snap enabled to true or false
        Args:
            value           (bool) --   to enable snap at subclient level or not
        """
        self._set_subclient_properties(
            "_snapCopyInfo['isSnapBackupEnabled']", value)

    @property
    def snap_engine(self):
        """
        Getter to fetch snap_engine
        Returns:
            str     --  name of snap engine at subclient level

        """
        return self._snapCopyInfo['snapToTapeSelectedEngine']['snapShotEngineName']

    @snap_engine.setter
    def snap_engine(self, engine_name):
        """Method to set snap engine name
        Args:
            engine_name           (str) --   snap engine name
        """
        self._set_subclient_properties(
            "_snapCopyInfo['snapToTapeSelectedEngine']['snapShotEngineName']", engine_name)

    @property
    def snap_proxy(self):
        """
        Getter to snap_proxy if set any
        Returns:
            str     --  name of proxy client used for intellisnap operation

        """
        return self._snapCopyInfo['snapToTapeProxyToUse']['clientName']

    @snap_proxy.setter
    def snap_proxy(self, proxy_name):
        """Method to set snap proxy name
        Args:
            proxy_name           (str) --   snap proxy name
        """
        self._set_subclient_properties(
            "_snapCopyInfo['snapToTapeProxyToUse']['clientName']", proxy_name)

    @property
    def use_dump_based_backup_copy(self):
        """
        Getter to status of dumpbased backup copy
        Returns:
            bool     --  checks if dump based backup copy is enabled or not

        """
        return self._snapCopyInfo['useDumpBasedBackupCopy']

    @use_dump_based_backup_copy.setter
    def use_dump_based_backup_copy(self, dump_based):
        """Method to enable dump based backup copy
        Args:
            dump_based           (bool) --   set true  to enable dump based backup copy option
        """
        self._set_subclient_properties(
            "_snapCopyInfo['useDumpBasedBackupCopy']", dump_based)

    @property
    def dump_based_backup_copy_option(self):
        """
        Getter to fetch dumpbased backup copy option : 1(configured instance), 2(custom new instance)
        Returns:
            int     --  returns 1 or 2 based type of sybase instance configured

        """
        return self._snapCopyInfo['dumpBasedBackupCopyOption']

    @dump_based_backup_copy_option.setter
    def dump_based_backup_copy_option(self, dump_based_backup_copy_option):
        """Method to enable dump based backup copy
        Args:
            dump_based_backup_copy_option      (int) --   set 1(configured instance), 2(custom new instance)
        """
        self._set_subclient_properties(
            "_snapCopyInfo['dumpBasedBackupCopyOption']", dump_based_backup_copy_option)

    @property
    def configured_instance(self):
        """Getter to fetch configured isntance name if dump based backup copy option is 2
        Returns:
            (str)       --      string of configured instance if dump based backup option is 1

        Raises:
            SDK Exception
                if dump based backup copy not enabled

                if dump based copy option is not 1
        """
        if (self._snapCopyInfo['useDumpBasedBackupCopy']):
            if (self._snapCopyInfo['dumpBasedBackupCopyOption'] == 1):
                return self._snapCopyInfo['configuredSybaseInstance']['instanceName']
            else:
                raise SDKException(
                    'Subclient', '102', "Invalid dump based copy option set. cannot get this parameter")
        else:
            raise SDKException('Subclient', '102',
                               "Dump based parameter is not available")

    @configured_instance.setter
    def configured_instance(self, instance_name):
        """Setter for configured instance name for dump based backup copy option
        Args:
            instance_name       (str) --    string of instance name to be used for dump based backup copy
        """

        self._set_subclient_properties(
            "_snapCopyInfo['configuredSybaseInstance']['instanceName']", str(instance_name))

    @property
    def auxiliary_sybase_server(self):
        """Getter to fetch custom instance properties if dump based copy option is 2
        Returns:
            dict        --  dict of four properties : sybase_home, sybase_ase, sybase_ocs, sybase_user for custom instance
        Raises:
            SDK Exception
                if dump based backup copy not enabled

                if dump based copy option is not 2
        """

        if self.use_dump_based_backup_copy:
            if self.dump_based_backup_copy_option == 2:
                auxiliary_sybase_server = {
                    'sybaseHome': self._snapCopyInfo['sybaseHome'],
                    'sybaseASE': self._snapCopyInfo['sybaseASE'],
                    'sybaseOCS': self._snapCopyInfo['sybaseOCS'],
                    'sybaseUser': self._snapCopyInfo['sybaseUser']['userName']
                }
                return auxiliary_sybase_server
            else:
                raise SDKException(
                    'Subclient', '102', "Invalid dump based copy option set. cannot get this parameter")
        else:
            raise SDKException('Subclient', '102',
                               "dump based parameter is not available")

    @auxiliary_sybase_server.setter
    def auxiliary_sybase_server(self, instance_properties):
        """Setter  custom instance properties if dump based copy option is 2
        Args:
            instance_properties     (dict)       --  dict of four properties : sybase_home, sybase_ase, sybase_ocs, sybase_user for custom instance

            Sample dict:
            instance_properties = {
                        'sybaseHome':sybase_home,
                        'sybaseASE':sybase_ase,
                        'sybaseOCS':sybase_ocs,
                        'sybaseUser':sybase_user
                }
        Raises:
            SDK Exception

                if None value in instance_properties
        """
        if None in instance_properties.values():
            raise SDKException(
                'Instance', '102', "One of the sybase custom instance parameter is None so cannot proceed")
        self._set_subclient_properties(
            "_snapCopyInfo['sybaseHome']", str(instance_properties['sybaseHome']))
        self._set_subclient_properties(
            "_snapCopyInfo['sybaseASE']", str(instance_properties['sybaseASE']))
        self._set_subclient_properties(
            "_snapCopyInfo['sybaseOCS']", str(instance_properties['sybaseOCS']))
        self._set_subclient_properties("_snapCopyInfo['sybaseUser']['userName']", str(
            instance_properties['sybaseUser']))

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

    def backup(self, backup_level=r'full', donottruncatelog=False, sybaseskipfullafterlogbkp=False, createbackupcopyimmediately=False, backupcopytype=2):
        """

        Args:
            backup_level (str)  -- Level of backup. Can be full, incremental or differential
             default: full

            donottruncatelog (bool) -- Sybase truncate log option for incremental backup

            sybaseskipfullafterlogbkp (bool) -- Sybase backup option for incremental

            createbackupcopyimmediately(bool)  -- Sybase snap job needs this backup copy operation

            backupcopytype(int)            --   backup copy job to be launched based on below two options
                default : 2, possible values : 1 (USING_STORAGE_POLICY_RULE), 2( USING_LATEST_CYCLE)

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

        if createbackupcopyimmediately is True:
            if backup_level.lower() == 'incremental':
                raise SDKException(
                    'Subclient', '102', 'Backup Copy job is not valid for Transaction Log Backup ')

        request_json = self._sybase_backup_request_json(
            backup_level.lower(), donottruncatelog, sybaseskipfullafterlogbkp, createbackupcopyimmediately, backupcopytype)

        backup_service = self._commcell_object._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service, request_json
        )
        return self._process_backup_response(flag, response)
