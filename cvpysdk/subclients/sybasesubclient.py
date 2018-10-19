# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Main File for performing Sybase Subclient Operations

SybaseSubclient is the only class defined in this file.

SybaseSubclient :       Derived class from DatabaseSubclient Base class,
                        representing an Sybase subclient,
                        and to perform operations on that subclient

SybaseSubclient:

    __init__()                          --  initialise object of sybase
                                            subclient object associated
                                            with the specified instance

    _get_subclient_properties           --  get the all subclient related
                                            properties of this subclient

    _sybase_backup_request_json         --  Returns the JSON request to pass to
                                            the API as per the options selected by the user

    is_snapenabled()                    --  Check if intellisnap has been enabled
                                            in the subclient and sets it accordingly

    snap_engine()                       --  updates snap_engine for sybase subclient

    snap_proxy()                        --  updates proxy name from sybase snap operation

    use_dump_based_backup_copy()        --  updates the use of dump based method for backup copy

    dump_based_backup_copy_option()     --  updates subtype of dump based operation

    configured_instance()               --  updates configured instance name
                                            for dump based backup copy type 1

    auxiliary_sybase_server()           --  updates custom instance properties
                                            for dump based backup copy type 2

    content()                           --  update the content of
                                            the sybase  subclient

    backup()                            --  Run a backup job for the subclient


"""
from __future__ import unicode_literals
from ..subclient import Subclient
from ..exception import SDKException


class SybaseSubclient(Subclient):
    """
    Base class consisting of all the common properties and operations for a Sybase Subclient
    """

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """
        Initialize Sybase Subclient Object

        Args:
            backupset_object  (object)  --  instance of the Backupset class

            subclient_name    (str)     --  name of the subclient

            subclient_id      (str)     --  id of the subclient
                                            default : None


        Returns :
            (object) - instance of the Sybase Subclient class

        """
        self._sybase_properties = {}
        self._snap_copy_info = None
        super(SybaseSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def _get_subclient_properties(self):
        """
        Gets the subclient related properties of Sybase subclient
        """

        super(SybaseSubclient, self)._get_subclient_properties()
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

        self._snap_copy_info = self._commonProperties.get('snapCopyInfo')

    def _get_subclient_properties_json(self):
        """
        Get the all subclient related properties of this subclient.

           Returns:
                (dict) - all subclient properties put inside a dict

        """
        return {
            "subClientProperties":
                {
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1,
                    "snapCopyInfo": self._snap_copy_info
                }
        }

    def _sybase_backup_request_json(self,
                                    backup_level,
                                    do_not_truncate_log=False,
                                    sybase_skip_full_after_logbkp=False,
                                    create_backup_copy_immediately=False,
                                    backup_copy_type=2,
                                    directive_file=None):
        """
        Returns the JSON request to pass to the API as per the options selected by the user.

            Args:
               backup_level                     (list)  --  level of backup the user wish to run
                                                            Full / Incremental / Differential

               do_not_truncate_log              (bool)  --  Sybase truncate log option
                                                            for incremental backup
                                                            default : False

               sybase_skip_full_after_logbkp    (bool)  --  Sybase backup option for incremental
                                                            default : False

               create_backup_copy_immediately   (bool)  --  Sybase snap job needs
                                                            this backup copy operation
                                                            default : False

               backup_copy_type                 (int)   --  backup copy job to be launched
                                                            based on below two options
                                                            default : 2, possible values :
                                                            1 (USING_STORAGE_POLICY_RULE),
                                                            2( USING_LATEST_CYCLE)

               directive_file                   (str)   --  inputfile for ondemand backup
                                                            containing database list
                                                            default : None

            Returns:

                (dict) - JSON request to pass to the API

        """
        request_json = self._backup_json(backup_level, False, "BEFORE_SYNTH")
        sybase_options = {
            "doNotTruncateLog": do_not_truncate_log,
            "sybaseSkipFullafterLogBkp": sybase_skip_full_after_logbkp
        }

        if create_backup_copy_immediately:
            sub_opt = {"dataOpt":
                       {
                           "createBackupCopyImmediately": create_backup_copy_immediately,
                           "backupCopyType": backup_copy_type
                       }
                      }
            sybase_options.update(sub_opt)
        if self._commonProperties.get("onDemandSubClient", False):
            on_demand_input = {"onDemandInputFile":directive_file}
            sybase_options.update(on_demand_input)

        request_json["taskInfo"]["subTasks"][0]["options"]["backupOpts"].update(
            sybase_options
        )
        return request_json


    @property
    def is_snapenabled(self):
        """
        Getter to check whether the subclient has snap enabled

        Returns:
            (bool)  -    boolean value based on snap
                         status at subclient level

                True    -  returns Truee if snap is enabled on the subclient
                False   -  returns False if snap is not
                            enabled at subclient level

        """
        return self._snap_copy_info.get("isSnapBackupEnabled", False)

    @is_snapenabled.setter
    def is_snapenabled(self, value):
        """
        To set is snap enabled to true or false

        Args:
            value           (bool) --   to enable snap at subclient level or not

        """
        self._set_subclient_properties(
            "_snap_copy_info['isSnapBackupEnabled']", value)

    @property
    def snap_engine(self):
        """
        Getter to fetch snap_engine

        Returns:
            (str)     -  name of snap engine at subclient level

        """
        return self._snap_copy_info.get('snapToTapeSelectedEngine', {}).get('snapShotEngineName')

    @snap_engine.setter
    def snap_engine(self, engine_name):
        """
        To set snap engine name

        Args:
            engine_name           (str) --      name of snap engine
                                                for intellisnap

        """
        self._set_subclient_properties(
            "_snap_copy_info['snapToTapeSelectedEngine']['snapShotEngineName']", engine_name)

    @property
    def snap_proxy(self):
        """
        Getter to snap_proxy if set any

        Returns:
            (str)     --    name of proxy client used
                            for intellisnap operation

        """
        return self._snap_copy_info.get('snapToTapeProxyToUse', {}).get('clientName')

    @snap_proxy.setter
    def snap_proxy(self, proxy_name):
        """
        Setter for snap proxy name

        Args:
            proxy_name           (str) --   snap proxy name

        """
        self._set_subclient_properties(
            "_snap_copy_info['snapToTapeProxyToUse']['clientName']", proxy_name)

    @property
    def use_dump_based_backup_copy(self):
        """
        Getter to status of dumpbased backup copy

        Returns:
            (bool)     -    checks if dump based backup
                            copy is enabled or not

        """
        return self._snap_copy_info.get('useDumpBasedBackupCopy')

    @use_dump_based_backup_copy.setter
    def use_dump_based_backup_copy(self, dump_based):
        """
        To enable dump based backup copy

        Args:
            dump_based      (bool)     --      set true  to enable dump
                                               based backup copy option

        """
        self._set_subclient_properties(
            "_snap_copy_info['useDumpBasedBackupCopy']", dump_based)

    @property
    def dump_based_backup_copy_option(self):
        """
        Getter to fetch dumpbased backup copy option :
        1(configured instance), 2(custom new instance)

        Returns:
            (int)     -  returns 1 or 2 based type of sybase instance configured

        """
        return self._snap_copy_info.get("dumpBasedBackupCopyOption")

    @dump_based_backup_copy_option.setter
    def dump_based_backup_copy_option(self, dump_based_backup_copy_option):
        """
        Enable dump based backup copy

        Args:
            dump_based_backup_copy_option      (int) --  set 1(configured instance),
                                                             2(custom new instance)
        """
        self._set_subclient_properties(
            "_snap_copy_info['dumpBasedBackupCopyOption']", dump_based_backup_copy_option)

    @property
    def configured_instance(self):
        """
        Getter to fetch configured instance
        name if dump based backup copy option is 2
        Returns:
            (str)       -       string of configured instance
                                if dump based backup option is 1

        Raises:
            SDK Exception
                if dump based backup copy not enabled

                if dump based copy option is not 1

        """
        if self._snap_copy_info.get('useDumpBasedBackupCopy'):
            if self._snap_copy_info.get('dumpBasedBackupCopyOption') == 1:
                return self._snap_copy_info['configuredSybaseInstance']['instanceName']
            else:
                raise SDKException(
                    'Subclient', '102', "Invalid dump based copy option")
        else:
            raise SDKException('Subclient', '102',
                               "Dump based parameter is not available")

    @configured_instance.setter
    def configured_instance(self, instance_name):
        """
        Setter for configured instance
        name for dump based backup copy option

        Args:
            instance_name       (str) --    string of instance name
                                            to be used for dump based backup copy

        """

        self._set_subclient_properties(
            "_snap_copy_info['configuredSybaseInstance']['instanceName']", instance_name)

    @property
    def auxiliary_sybase_server(self):
        """
        Getter to fetch custom instance properties if dump based copy option is 2

        Returns:
            (dict)       -  dict of four properties
                            for custom instance
        Raises:
            SDK Exception
                if dump based backup copy not enabled

                if dump based copy option is not 2

        """

        if self.use_dump_based_backup_copy:
            if self.dump_based_backup_copy_option == 2:
                auxiliary_sybase_server = {
                    'sybaseHome': self._snap_copy_info.get('sybaseHome'),
                    'sybaseASE': self._snap_copy_info.get('sybaseASE'),
                    'sybaseOCS': self._snap_copy_info.get('sybaseOCS'),
                    'sybaseUser': self._snap_copy_info.get('sybaseUser', {}).get('userName')
                }
                return auxiliary_sybase_server
            else:
                raise SDKException(
                    'Subclient', '102', "Invalid dump based copy option set")
        else:
            raise SDKException('Subclient', '102',
                               "dump based parameter is not available")

    @auxiliary_sybase_server.setter
    def auxiliary_sybase_server(self, instance_properties):
        """
        Setter  custom instance properties if dump based copy option is 2

        Args:
            instance_properties     (dict)       --  dict of four properties
                                                     for custom instance

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
                'Instance', '102', "One of the sybase custom instance parameter is None. Exiting")
        self._set_subclient_properties(
            "_snap_copy_info['sybaseHome']", instance_properties['sybaseHome'])
        self._set_subclient_properties(
            "_snap_copy_info['sybaseASE']", instance_properties['sybaseASE'])
        self._set_subclient_properties(
            "_snap_copy_info['sybaseOCS']", instance_properties['sybaseOCS'])
        self._set_subclient_properties("_snap_copy_info['sybaseUser']['userName']",
                                       instance_properties['sybaseUser'])

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
        """
        Creates the list of content JSON to pass to the API to add a new Sybase Subclient
        with the content passed in subclient content.

            Args:
                subclient_content (list)  --  list of the content to add to the subclient

            Returns:
                (list) -    list of the appropriate JSON
                            for an agent to send to the POST Subclient API

        """
        content_new = []
        for dbname in subclient_content:
            sybase_server_dict = {"sybaseContent": {"databaseName": dbname}}
            content_new.append(sybase_server_dict)
        self._set_subclient_properties("_content", content_new)

    def backup(self,
               backup_level=r'full',
               do_not_truncate_log=False,
               sybase_skip_full_after_logbkp=False,
               create_backup_copy_immediately=False,
               backup_copy_type=2,
               directive_file=None):
        """
        Performs backup on sybase subclient

        Args:
            backup_level                            (str)   --  Level of backup.
                                                                full|incremental|differential
                                                                default: full

            do_not_truncate_log                     (bool)  --  Sybase truncate log option
                                                                for incremental backup
                                                                default : False

            sybase_skip_full_after_logbkp           (bool)  --  Sybase backup option for incremental
                                                                default : False

            create_backup_copy_immediately          (bool)  --  Sybase snap job needs
                                                                this backup copy operation
                                                                default : False

            backup_copy_type                        (int)   --  backup copy job to be launched
                                                                based on below two options
                                                                default : 2, possible values :
                                                                1 (USING_STORAGE_POLICY_RULE),
                                                                2( USING_LATEST_CYCLE)

            directive_file                          (str)   --  input file for ondemand backup
                                                                containing database list
                                                                default : None

        Returns:
            (object) - instance of Job class

        Raises:
            SDKException:
                if backup level is incorrect

                if response is empty

                if response does not succeed

        """
        if backup_level.lower() not in ['full', 'incremental', 'differential']:
            raise SDKException(r'Subclient', r'103')

        if backup_level.lower() == 'incremental':
            do_not_truncate_log = do_not_truncate_log
            sybase_skip_full_after_logbkp = sybase_skip_full_after_logbkp
        else:
            do_not_truncate_log = False
            sybase_skip_full_after_logbkp = False

        if create_backup_copy_immediately:
            if backup_level.lower() == 'incremental':
                raise SDKException(
                    'Subclient', '102', 'Backup Copy job is not valid for Transaction Log Backup ')

        request_json = self._sybase_backup_request_json(backup_level.lower(),
                                                        do_not_truncate_log,
                                                        sybase_skip_full_after_logbkp,
                                                        create_backup_copy_immediately,
                                                        backup_copy_type,
                                                        directive_file)

        backup_service = self._commcell_object._services['CREATE_TASK']

        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'POST', backup_service, request_json
        )
        return self._process_backup_response(flag, response)
