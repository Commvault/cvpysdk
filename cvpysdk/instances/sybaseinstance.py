# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
File for operating on a Sybase Instance.

SybaseInstance is the only class defined in this file.
SybaseInstance: Derived class from Instance Base class, representing an
                            sybase instance, and to perform operations on that instance

SybaseInstance:

    __init__()                      -- initialise object of Sybase  Instance associated with
                                       the specified agent

    _get_sybase_restore_json()      -- Private Method to construct restore JSON for
                                       individual database restore

    _get_sybase_full_restore_json() -- Private Method to construct
                                       restore JSON for fullserver restore

    _get_single_database_json()     -- Private Method to construct
                                       restore JSON for individual database restore

    _get_server_content()           -- Private Method to construct restore JSON for
                                       individual database when we have rename device options


    _restore_common_options_json()  -- setter for common options property in restore

    _restore_destination_json()     -- setter for destination options property in restore

    _restore_sybase_option_json()   -- setter for Sybase restore option property in restore

    sybase_home()                   -- returns string of sybase_home Property of Sybase instance

    sybase_instance_name()          -- returns sybase instance name without any case change

    is_discovery_enabled()          -- returns bool value of autodiscovery option
                                       at given sybase instance level

    localadmin_user()               -- returns string of localadmin_user of given sybase instance

    sa_user()                       -- returns string of sybase sa_user of given sybase instance

    version()                       -- returns string of given sybase server version

    backup_server()                 -- returns string of backup_server for given sybase instance

    sybase_ocs()                    -- returns string of sybase_ocs for given sybase instance

    sybase_ase()                    -- returns string of sybase_ase for given sybase  instance

    sybase_blocksize()              -- returns integer of block
                                       size for given sybase instance

    sybase_configfile()             -- returns string of sybase_configfile
                                       for given sybase instance

    sybase_sharedmemory_directory() -- returns string of sybase_memory_directory
                                       for given sybase instance

    restore_sybase_server()         -- Performs full sybase server restore

    restore_database()              -- Performs individual databases restore

    restore_to_disk()               -- Perform restore to disk [Application free restore] for sybase

"""


from __future__ import unicode_literals
import datetime
from .dbinstance import DatabaseInstance
from ..exception import SDKException


class SybaseInstance(DatabaseInstance):
    """
    Class to represent a standalone Sybase Instance
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Initializes the object of Sybase Instance class

            Args:
                agent_object    (object) --     instance of the Agent class

                instance_name   (str)    --     name of the instance

                instance_id     (str)    --     id of the instance
                                                default None

            Returns :
                (object) - instance of the Sybase Instance class

        """
        self._sybase_restore_json = None
        self._commonoption_restore_json = None
        self._destination_restore_json = None
        super(SybaseInstance, self).__init__(
            agent_object, instance_name, instance_id)
        self._instanceprop = {}  # instance variable to hold instance properties


    @property
    def sybase_home(self):
        """
        Returns sybase home

            Returns:
                (str) - string representing sybase home

        """
        return self._properties.get('sybaseInstance', {}).get('sybaseHome')

    @property
    def sybase_instance_name(self):
        """
        Returns sybase instance name with actual case without any conversion

            Returns:
                (str) - string representing sybase instance name

        """
        return self._properties.get('instance', {}).get('instanceName')

    @property
    def is_discovery_enabled(self):
        """
        Returns autodiscovery enable status

            Returns:
                bool - boolean value beased on autodiscovery enable status.

                    True  - returns True if autodiscovery is enabled

                    False - returns False if autodiscosvery is not enabled

        """
        return self._properties.get('sybaseInstance', {}).get('enableAutoDiscovery')

    @property
    def localadmin_user(self):
        """
        Returns for local admin user

            Returns:
                (str) - string representing local admin user

        """
        return self._properties.get('sybaseInstance', {}).get('localAdministrator', {}).get('userName')

    @property
    def sa_user(self):
        """
        Returns for sa username

            Returns:
                (str) - string representing sa username

        """
        return self._properties.get('sybaseInstance', {}).get('saUser', {}).get('userName')

    @property
    def version(self):
        """
        Returns for sybase version

            Returns:
                (str) - string representing sybase version

        """
        return self._properties.get('version')

    @property
    def backup_server(self):
        """
        Returns for backup server

            Returns:
                (str) - string representing backup server

        """
        return self._properties.get('sybaseInstance', {}).get('backupServer')

    @property
    def sybase_ocs(self):
        """
        Returns for sybase ocs

            Returns:
                (str) - string representing sybase OCS

        """
        return self._properties.get('sybaseInstance', {}).get('sybaseOCS')

    @property
    def sybase_ase(self):
        """
        Returns for sybase ase

            Returns:
                (str) - string representing sybase ASE

        """
        return self._properties.get('sybaseInstance', {}).get('sybaseASE')

    @property
    def sybase_blocksize(self):
        """
        Returns for sybase blocksize

            Returns:
                (int) - integer representing block size value

        """
        return self._properties.get('sybaseInstance', {}).get('sybaseBlockSize')

    @property
    def sybase_configfile(self):
        """
        Returns for sybase configfile

            Returns:
                (str) - string representing sybase config file

        """
        return self._properties.get('sybaseInstance', {}).get('configFile')

    @property
    def sybase_sharedmemory_directory(self):
        """
        Returns for sybase shared memory directory

            Returns:
                (str)  -    string representing sybase
                            sybase shared memory directory

        """
        return self._properties.get('sybaseInstance', {}).get('sharedMemoryDirectory')

    @property
    def client_name(self):
        """
        Returns client name of this instance

            Returns:
                (str) - client name as registered in the commcell

        """
        return self._properties.get('instance', {}).get('clientName')

    def _restore_common_options_json(self, value):
        """
        Setter for the Common options in restore JSON

            Args:
                value   (dict)  --  dict of common options
                                    for restore json

        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._commonoption_restore_json = {
            "indexFreeRestore": value.get("index_free_restore", False),
            "restoreToDisk": value.get("restore_to_disk", False),
            "sybaseCreateDevices": value.get("sybase_create_device", False)
        }

    def _restore_destination_json(self, value):
        """
        Setter for the Sybase Destination options in restore JSON

            Args:
                    value   (dict)  --  dict of values for destination option

        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')

        self._destination_restore_json = {
            "destinationInstance": {
                "clientName": value.get("destination_client", ""),
                "instanceName": value.get("destination_instance_name", ""),
                "appName": "Sybase"
            },
            "destClient": {
                "clientName": value.get("destination_client", "")
            },
            "destPath": [value.get("destination_path", "")]
        }

    def _restore_sybase_option_json(self, value):
        """
        Setter for the sybase restore option in restore JSON

            Args:
                value   (dict)  --  dict of values for sybase option

        """

        if not isinstance(value, dict):
            raise SDKException('Instance', '101')
        if value.get("to_time") is None:
            time_dict = {}
        else:
            time_dict = {
                "timeValue":value.get("to_time", "")
            }
        self._sybase_restore_json = {
            "sybaseRecoverType": "STATE_RECOVER",
            "pointofTime": value.get("point_in_time", ""),
            "destinationServer": {
                "name": value.get("destination_instance_name", "")
            },
            "pointInTime": time_dict,
            "instanceRestore": value.get("instance_restore", ""),
            "renameDatabases": value.get("rename_databases", ""),
            "restoreType": "POINT_IN_TIME",
            "sybaseDatabase": value.get("syb_db", "")
        }

    def _restore_json(self, **kwargs):
        """
        Returns the JSON request to pass to the API as per the options selected by the user.

                Args:
                    kwargs   (list)  --  list of options need to be set for restore

                Returns:
                   (dict) - JSON request to pass to the API

        """
        restore_json = super(SybaseInstance, self)._restore_json(**kwargs)
        restore_option = {}
        if kwargs.get("restore_option"):
            restore_option = kwargs["restore_option"]
            for key in kwargs:
                if not key == "restore_option":
                    restore_option[key] = kwargs[key]
        else:
            restore_option.update(kwargs)

        self._restore_sybase_option_json(restore_option)
        restore_json["taskInfo"]["subTasks"][0]["options"][
            "restoreOptions"]["sybaseRstOption"] = self._sybase_restore_json
        return restore_json

    def _get_sybase_restore_base_json(self,
                                      destination_client,
                                      destination_instance_name,
                                      point_in_time=False,
                                      instance_restore=False,
                                      timevalue=None,
                                      sybase_create_device=False,
                                      rename_databases=False,
                                      copy_precedence=0):
        """
        Returns basic sybase restore JSON based on given combination of parameters

            Args:
                destination_client_name    (str)    -- sybase destination client for restore

                destination_instance_name  (str)    -- sybase destination instance for restore

                point_in_time              (bool)   -- determines point_in_time based restore or not
                                                       default : False

                instance_restore           (bool)   -- determines if its single database or
                                                       complete sybase server restore
                                                       default : False

                timevalue                  (str)    -- for point_in_time based restore
                                                       format: YYYY-MM-DD HH:MM:SS
                                                       default : None

                sybase_create_device       (bool)   -- determines whether to createdevice for
                                                       sybase database restore
                                                       default : False

                rename_databases           (bool)   -- determines whether renamedatabase option
                                                       chosen for given database restore
                                                       default : False

                copy_precedence            (int)    -- copy precedence value of storage policy
                                                       default: 0


            Return:
                (dict)  -    returns base sybase restore json

        """
        copy_precedence_applicable = False
        if copy_precedence is not None:
            copy_precedence_applicable = True
        if instance_restore is not True:
            point_in_time = True
            if timevalue is None:
                current_time = datetime.datetime.utcnow()
                current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                timevalue = current_time
        else:
            if (timevalue is None) and (point_in_time is True):
                current_time = datetime.datetime.utcnow()
                current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                timevalue = current_time
        syb_db = []
        basic_sybase_options = self._restore_json(
            destination_client=destination_client,
            destination_instance_name=destination_instance_name,
            point_in_time=point_in_time,
            instance_restore=instance_restore,
            to_time=timevalue,
            from_time=None,
            sybase_create_device=sybase_create_device,
            rename_databases=rename_databases,
            copy_precedence=copy_precedence,
            copy_precedence_applicable=copy_precedence_applicable,
            syb_db=syb_db)

        return basic_sybase_options

    def _db_option(self,
                   database_list,
                   rename_databases,
                   sybase_create_device,
                   device_options):
        """
        Constructs  database option for
        each databases in database list

            Args:
                database_list           (list)          --  list of databases opted for restore

                sybase_create_device    (bool)          --  determines whether to createdevice
                                                            for sybase database restore

                rename_databases        (bool)          --  determines whether renamedatabase option
                                                            chosen for given database restore

                device_options          (dict(dict))    --  list of dict for each database with
                                                            device rename and database
                                                            rename options

            Returns:
                (dict)    -     list of db_options to
                                be added to restore_json

        """
        db_options = []
        for dbname in database_list:
            if device_options is None:
                db_json = self._get_single_database_json(dbname=dbname)
            else:
                if dbname in device_options.keys():
                    dev_opt = device_options[dbname]
                    db_json = self._get_single_database_json(
                        dbname, dev_opt, rename_databases, sybase_create_device)
                else:
                    db_json = self._get_single_database_json(dbname=dbname)
            db_options.append(db_json)
        return db_options

    def _get_sybase_restore_json(self,
                                 destination_client,
                                 destination_instance_name,
                                 database_list,
                                 timevalue=None,
                                 sybase_create_device=False,
                                 rename_databases=False,
                                 device_options=None,
                                 copy_precedence=0):
        """
        Constructs sybase restore JSON for individual Database restore

            Args:
                destination_client_name         (str)           --  sybase destination client
                                                                    for restore

                destination_instance_name       (str)           --  sybase destination instance
                                                                    for restore

                database_list                   (list)          --  list of databases for restore

                timevalue                       (str)           --  for point_in_time based restore
                                                                    format: YYYY-MM-DD HH:MM:SS
                                                                    default : None

                sybase_create_device            (bool)          --  determines whether to
                                                                    createdevice
                                                                    for sybase database restore
                                                                    default : False

                rename_databases                (bool)          --  determines whether
                                                                    renamedatabase option
                                                                    enabled or not
                                                                    default : False

                device_options                  (dict(dict))    --  dict of dict for each
                                                                    database with device
                                                                    and database rename options
                                                                    default : None

                copy_precedence                 (int)           --  copy precedence of
                                                                    storage policy
                                                                    default: 0

            Returns:
                    (dict)    -   return restore JSON for individual Sybase database restored

        """
        instance_restore = False
        point_in_time = True
        # Check to perform renamedatabase/create device
        if (sybase_create_device is False) and (rename_databases is False):
            device_options = None

        restore_json = self._get_sybase_restore_base_json(
            destination_client,
            destination_instance_name,
            point_in_time,
            instance_restore,
            timevalue,
            sybase_create_device,
            rename_databases,
            copy_precedence
        )

        db_options = self._db_option(
            database_list, rename_databases, sybase_create_device, device_options
        )
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "sybaseRstOption"]["sybaseDatabase"] = db_options
        return restore_json

    def _get_sybase_full_restore_json(self,
                                      destination_client,
                                      destination_instance_name,
                                      point_in_time=False,
                                      timevalue=None,
                                      sybase_create_device=True,
                                      rename_databases=False,
                                      device_options=None,
                                      copy_precedence=0):
        """
        Creates JSON for Full server restore

            Args:
                destination_client_name         (str)           --  sybase destination client
                                                                    for restore

                destination_instance_name       (str)           --  sybase destination instance
                                                                    for restore

                point_in_time                   (bool)          --  determines point_in_time
                                                                    restore or not
                                                                    default : False

                timevalue                       (str)           --  for point_in_time based restore
                                                                    format: YYYY-MM-DD HH:MM:SS
                                                                    default : None

                sybase_create_device            (bool)          --  determines whether to
                                                                    createdevice
                                                                    for sybase database restore
                                                                    default : True

                rename_databases                (bool)          --  determines whether
                                                                    renamedatabase option
                                                                    enabled or not
                                                                    default : False

                device_options                  (dict(dict))    --  dict of dict for each
                                                                    database with device
                                                                    and database
                                                                    rename options
                                                                    default : None

                copy_precedence                 (int)           --  copy precedence of
                                                                    storage policy
                                                                    default: 0

            Returns:
                    (dict) -   return restore JSON for Full sybase server restore

        """

        instance_restore = True
        restore_json = self._get_sybase_restore_base_json(
            destination_client,
            destination_instance_name,
            point_in_time,
            instance_restore,
            timevalue,
            sybase_create_device,
            rename_databases,
            copy_precedence)
        db_options = []
        dblist = self._get_server_content()
        device_options_keys = []
        if device_options is not None:
            for key in device_options.keys():
                device_options_keys.append(str(key))

        if not dblist:
            raise SDKException(
                'Instance', '102', 'Database contents of Sybase server is empty'
            )

        database_list = dblist
        db_options = self._db_option(
            database_list, rename_databases, sybase_create_device, device_options)
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "sybaseRstOption"]["sybaseDatabase"] = db_options
        return restore_json

    def _get_single_database_json(self,
                                  dbname,
                                  device_options=None,
                                  rename_databases=False,
                                  sybase_create_device=False):
        """
        Constructs database JSON for individual
        Sybase databases with create device and rename database parameters

            Args:
                dbname                  (str)              --   Database name opted for restore

                device_options          (dict(dict))       --   dict of dict for given database
                                                                with device and database
                                                                rename option


                sybase_create_device    (bool)             --   determines whether to createdevice
                                                                for sybase database restore

                rename_databases        (bool)             --   determines whether renamedatabase
                                                                option chosen for given
                                                                database restore
            Returns:
                (dict)    -     Individual Database option with restore[
                                for rename and create device]

        """
        sybase_db_details = None
        databasechain = "0:0:{0}:0".format(dbname)
        dbchain_list = []
        dbchain_list.append(databasechain)
        subclientid = "0"
        dbid = "0"
        datadevid = "0"
        logdevid = "0"
        size = "0"
        device = []
        sybase_db_details = {
            "databaseId": {"name": dbname},
            "associatedSubClientId": 0,
            "databaseChain": dbchain_list
        }
        if device_options is not None:
            if sybase_create_device:
                for key1, value1 in device_options.items():
                    if device_options[key1] is None:
                        if key1 == "newdatabasename":
                            device_options[key1] = None
                        else:
                            device_options[key1] = "0"
            else:
                for key1, value1 in device_options.items():
                    if key1 == "newdatabasename":
                        continue
                    else:
                        device_options[key1] = "0"

            datadevicename = device_options["datadevicename"]
            newdatadevicename = device_options["newdatadevicename"]
            newdatadevicepath = device_options["newdatadevicepath"]
            logdevicename = device_options["logdevicename"]
            newlogdevicename = device_options["newlogdevicename"]
            newlogdevicepath = device_options["newlogdevicepath"]
            if rename_databases:
                if device_options["newdatabasename"] is None:
                    newdatabasename = dbname
                else:
                    newdatabasename = device_options["newdatabasename"]
            else:
                device_options["newdatabasename"] = dbname

            # Check to find given device is system device

            system_databases = ['master', 'model', 'sybsystemprocs',
                                'sybsystemdb', 'tempdb', 'sybmgmtdb', 'dbccdb', 'sybsecurity']
            if dbname in system_databases:
                newdatadevicename = "0"
                newlogdevicename = "0"
                newdatabasename = dbname
            data_device = "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}".format(subclientid,
                                                                   dbid,
                                                                   datadevid,
                                                                   datadevicename,
                                                                   newdatadevicename,
                                                                   newdatadevicepath,
                                                                   size,
                                                                   newdatabasename)

            log_device = "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}".format(subclientid,
                                                                  dbid,
                                                                  logdevid,
                                                                  logdevicename,
                                                                  newlogdevicename,
                                                                  newlogdevicepath,
                                                                  size,
                                                                  newdatabasename)

            device.append(data_device)
            device.append(log_device)
            sybase_db_details = {
                "databaseId": {"name": dbname},
                "associatedSubClientId": 0,
                "databaseChain": dbchain_list,
                "devices": device
            }

        return sybase_db_details

    def _get_server_content(self):
        """
        To get all databases for the speicfied Sybase Server instance

        Returns:
            (list)      -       list of databases available as server content

        """
        subclient_dict = self.subclients._get_subclients()
        subclient_list = []
        db_list = []
        for key in subclient_dict.keys():
            subclient_list.append(str(key))
        for sub in subclient_list:
            sub_obj = self.subclients.get(sub)
            content = sub_obj.content
            for eachdb in content:
                db_list.append(eachdb)
        db_list = set(db_list)
        return db_list

    def restore_sybase_server(self,
                              destination_client=None,
                              destination_instance_name=None,
                              point_in_time=False,
                              timevalue=None,
                              rename_databases=False,
                              device_options=None,
                              copy_precedence=0):
        """
        Performs Full sybase server restore

            Args:
                destination_client_name     (str)               --  sybase destination client
                                                                    for restore
                                                                    default : None

                destination_instance_name   (str)               --  sybase destination instance
                                                                    for restore
                                                                    default : None

                point_in_time               (bool)              --  determines point_in_time
                                                                    restore or not
                                                                    default:False

                timevalue                   (str)               --  for point_in_time based restore
                                                                    format: YYYY-MM-DD HH:MM:SS
                                                                    default : None


                rename_databases            (bool)              --  determines whether
                                                                    renamedatabase option chosen
                                                                    default:False


                device_options              (dict(dict))        --  dict of dict for each database
                                                                    with device and database
                                                                    rename options
                                                                    default : None

                copy_precedence             (int)               --  copy precedence of storage
                                                                    policy
                                                                    default: 0

            Note:

            Also This is dict  of dict having sourcedatabasenamead
            Key and set of another dict options
            as value corresponding to that source Database.

            Also if you wouldn't want to pass value for particular option , mark it none

            Dict format : "sourceDBname":"dict options"

                    Example: device_options = {}
                        "db1":
                            {
                                        "datadevicename":"testdata",

                                        "newdatadevicename":"testdatanew",

                                        "newdatadevicepath":"/opt/sap/data/testdatanew.dat",

                                        "logdevicename":"testlog",

                                        "newlogdevicename":"testlognew",

                                        "newlogdevicepath":"/opt/sap/data/testlognew.dat",

                                        "newdatabasename": "db1new"

                            },

                        "model":
                            {
                                        "datadevicename":None,

                                        "newdatadevicename":None,

                                        "newdatadevicepath":None,

                                        "logdevicename":None,

                                        "newlogdevicename":None,

                                        "newlogdevicepath":None,

                                        "newdatabasename": "modelnew"

                            }

                    }

            Note : Devices corresponding to System database cannot be renamed

            Returns:
                (object)    -     Job containing restore details

        """

        if destination_client is None:
            destination_client = self.client_name

        if destination_instance_name is None:
            destination_instance_name = self.instance_name

        sybase_create_device = True
        request_json = self._get_sybase_full_restore_json(
            destination_client,
            destination_instance_name,
            point_in_time,
            timevalue,
            sybase_create_device,
            rename_databases,
            device_options,
            copy_precedence)

        return self._process_restore_response(request_json)

    def restore_database(self,
                         destination_client=None,
                         destination_instance_name=None,
                         database_list=None,
                         timevalue=None,
                         sybase_create_device=False,
                         rename_databases=False,
                         device_options=None,
                         copy_precedence=0):
        """
        Performs individual database restores

            Args:

                destination_client_name     (str)               --  destination client for restore
                                                                    default : None

                destination_instance_name   (str)               --  destination instance
                                                                    for restore
                                                                    default : None

                database_list               (list)              --  list of databases for restore

                timevalue                   (str)               --  for point_in_time based restore
                                                                    format: YYYY-MM-DD HH:MM:SS
                                                                    default : None

                sybase_create_device        (bool)              --  determines whether to create
                                                                    device for database restore
                                                                    default:False

                rename_databases            (bool)              --  determines whether
                                                                    renamedatabase option chosen
                                                                    default:False

                device_options              (dict(dict))        --  dict of dict for each database
                                                                    with device and database
                                                                    rename options
                                                                    default : None

                copy_precedence             (int)               --  copy precedence of storage
                                                                    policy
                                                                    default: 0
            Note :

            Also This is dict  of dict having sourcedatabasename
            as Key and set of another dict options
            as value corresponding to that source Database.

            Also if you wouldn't want to pass
            value for particular option , mark it none


                    Example: device_options = {
                        "db1":
                            {
                                        "datadevicename":"testdata",

                                        "newdatadevicename":"testdatanew",

                                        "newdatadevicepath":"/opt/sap/data/testdatanew.dat",

                                        "logdevicename":"testlog",

                                        "newlogdevicename":"testlognew",

                                        "newlogdevicepath":"/opt/sap/data/testlognew.dat",

                                        "newdatabasename": "db1new"
                            },
                        "db2":
                        {
                                        "datadevicename":None,

                                        "newdatadevicename":None,

                                        "newdatadevicepath":"/opt/sap/data/testdatanew.dat",

                                        "logdevicename":"testlog",

                                        "newlogdevicename":"testlognew",

                                        "newlogdevicepath":"/opt/sap/data/testlognew.dat",

                                        "newdatabasename": None
                        }

                    }


            Returns:
                (object)    -     Job containing restore details

            Raises:
                SDKException
                    if databaselist is empty

        """
        if destination_client is None:
            destination_client = self.client_name

        if destination_instance_name is None:
            destination_instance_name = self.instance_name

        if database_list is None:
            raise SDKException('Instance', r'102',
                               'Restore Database List cannot be empty')

        request_json = self._get_sybase_restore_json(
            destination_client,
            destination_instance_name,
            database_list,
            timevalue,
            sybase_create_device,
            rename_databases,
            device_options,
            copy_precedence)

        return self._process_restore_response(request_json)

    def restore_to_disk(self,
                        destination_client,
                        destination_path,
                        backup_job_ids,
                        user_name,
                        password):
        """
        Perform restore to disk [Application free restore] for sybase

            Args:
                destination_client          (str)   --  destination client name

                destination_path:           (str)   --  destination path

                backup_job_ids              (list)  --  list of backup job IDs
                                                        to be used for disk restore

                user_name                   (str)   --  impersonation user name to
                                                        restore to destination client

                password                    (str)   --  impersonation user password

            Returns:
                (object)    -     Job containing restore details

            Raises:
                SDKException
                    if backup_job_ids not given as list of items

        """
        if not isinstance(backup_job_ids, list):
            raise SDKException('Instance', '101')
        request_json = self._get_restore_to_disk_json(destination_client,
                                                      destination_path,
                                                      backup_job_ids,
                                                      user_name,
                                                      password)
        del request_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["sybaseRstOption"]
        return self._process_restore_response(request_json)
