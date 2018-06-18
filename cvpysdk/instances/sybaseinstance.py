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

    sybase_blocksize()              -- returns integer of  block size for given sybase instance

    sybase_configfile()             -- returns string of sybase_configfile for given sybase instance

    sybase_sharedmemory_directory() -- returns string of sybase_memory_directory
                                       for given sybase instance

    restore_sybase_server()         -- Method to perform restore full sybase server

    restore_database()              -- Method to restore individual databases

"""


from __future__ import unicode_literals
import datetime
from ..instance import Instance
from ..exception import SDKException


class SybaseInstance(Instance):
    """
    Class to represent a standalone Sybase Instance
    """

    def __init__(self, agent_object, instance_name, instance_id=None):
        """
        Initializes the object of Sybase Instance class

        Args:
            agent_object (object)   -- instance of the Agent class

            instance_name (str)  -- name of the instance

            instance_id (str)    --  id of the instance
                default None
        Returns :
            object - instance of the Sybase Instance class

        """
        super(SybaseInstance, self).__init__(
            agent_object, instance_name, instance_id)
        self._instanceprop = {}  # instance variable to hold instance properties

    @property
    def sybase_home(self):
        """
        Getter for sybase home

        Returns:
            string - string of sybase_home

        """
        return self._properties['sybaseInstance']['sybaseHome']

    @property
    def sybase_instance_name(self):
        """
        Getter for sybase instance name with actual case without any conversion

        Returns:
            string - string of sybase_instance_name

        """
        return self._properties["instance"]["instanceName"]

    @property
    def is_discovery_enabled(self):
        """
        Getter to check if autodiscovery  has been enabled

        Returns:
            Bool - True if autodiscovery is enabled. Else False.

        """
        return self._properties['sybaseInstance']['enableAutoDiscovery']

    @property
    def localadmin_user(self):
        """
        Getter for local admin user

        Returns:
            string - string of Local admin user

        """
        return self._properties['sybaseInstance']['localAdministrator']['userName']

    @property
    def sa_user(self):
        """
        Getter for sa username

        Returns:
            string - string of sa username

        """
        return self._properties['sybaseInstance']['saUser']['userName']

    @property
    def version(self):
        """
        Getter for sybase version

        Returns:
            string - string of sybase instance version

        """
        return self._properties['version']

    @property
    def backup_server(self):
        """
        Getter for backup_server

        Returns:
            string - string of backup_server

        """
        return self._properties['sybaseInstance']['backupServer']

    @property
    def sybase_ocs(self):
        """
        Getter for sybase_ocs

        Returns:
            string - string of sybase_ocs

        """
        return self._properties['sybaseInstance']['sybaseOCS']

    @property
    def sybase_ase(self):
        """
        Getter for sybase_ase

        Returns:
            string - string of sybase_ase

        """
        return self._properties['sybaseInstance']['sybaseASE']

    @property
    def sybase_blocksize(self):
        """
        Getter for sybase_blocksize

        Returns:
            Integer - Int of sybase_blocksize

        """
        return self._properties['sybaseInstance']['sybaseBlockSize']

    @property
    def sybase_configfile(self):
        """
        Getter for sybase_configfile

        Returns:
            string - string of sybase_configfile

        """
        return self._properties['sybaseInstance']['configFile']

    @property
    def sybase_sharedmemory_directory(self):
        """
        Getter for sybase_sharedmemory_directory

        Returns:
            string - string of sybase_sharedmemory_directory

        """
        return self._properties['sybaseInstance']['sharedMemoryDirectory']

    @property
    def client_name(self):
        """
        Getter for getting client name of this instance

        Returns:
            string -- client name as registered in the commcell

        """
        return self._properties[r"instance"][r"clientName"]

    def _get_sybase_restore_base_json(self,
                                      destination_client,
                                      destination_instance_name,
                                      pointintime=False,
                                      instance_restore=False,
                                      timevalue=None,
                                      sybasecreatedevice=False,
                                      renamedatabases=False,
                                      copy_precedence=0):
        """
        Method to return basic sybase restore JSON based on given combination of parameters

        Args:

            destination_client_name   (str)    -- sybase destination client for restore

            destination_instance_name  (str)  -- sybase destination instance for restore

            pointintime  (bool)                -- determines pointintime based restore or not

            instance_restore  (bool)           -- determines if its single database or
                                                 complete sybase server restore

            timevalue  (str)                  -- for pointintime based restore
                                              format: YYYY-MM-DD HH:MM:SS

            sybasecreatedevice  (bool)         -- determines whether to createdevice for
                                                 sybase database restore

            renamedatabases (bool)            -- determines whether renamedatabase option
                                                 chosen for given database restore

            copy_precedence         (int)     --  copy precedence value of storage policy copy
                    default: 0


        Return :

            returns base sybase restore json

        """
        copy_precedence_applicable = False
        if copy_precedence is not None:
            copy_precedence_applicable = True
        if instance_restore is not True:
            pointintime = True
            if timevalue is None:
                current_time = datetime.datetime.now()
                current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                timevalue = current_time
        else:
            if (timevalue is None) and (pointintime is True):
                current_time = datetime.datetime.now()
                current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                timevalue = current_time
        syb_db = []
        basic_sybase_options = {
            "browseOption": {
                "timeRange": {
                    "toTimeValue": timevalue
                },
                "mediaOption": {
                    "copyPrecedence": {
                        "copyPrecedenceApplicable": copy_precedence_applicable,
                        "copyPrecedence": copy_precedence
                    }
                }
            },
            "destination": {
                "destClient": {
                    "clientName": destination_client
                },
                "destinationInstance": {
                    "instanceName": destination_instance_name,
                    "appName": "Sybase",
                    "clientName": destination_client

                }
            },
            "sybaseRstOption": {
                "sybaseRecoverType": "STATE_RECOVER",
                "pointofTime": pointintime,
                "destinationServer": {
                    "name": destination_instance_name
                },
                "pointInTime": {
                    "timeValue": timevalue
                },
                "instanceRestore": instance_restore,
                "renameDatabases": renamedatabases,
                "restoreType": "POINT_IN_TIME",
                "sybaseDatabase": syb_db
            },
            "commonOptions": {
                "sybaseCreateDevices": sybasecreatedevice
            }
        }

        return basic_sybase_options

    def _db_option(self, database_list, renamedatabases, sybasecreatedevice, device_options):
        """
        Method to construct  db option for each databases in db list

        Args :
            database_list  (list)  --list of databases opted for restore

            sybasecreatedevice  (bool)         -- determines whether to createdevice
                                                 for sybase database restore

            renamedatabases  (bool)           -- determines whether renamedatabase option
                                                 chosen for given database restore

            device_options  (dict(dict))   -- list of dict for each database with
                                                 device rename and database rename options

        returns :
            list of db_options to be added to restore_json

        """
        db_options = []
        for dbname in database_list:
            if device_options is None:
                db_json = self._get_single_database_json(dbname=dbname)
            else:
                if dbname in device_options.keys():
                    dev_opt = device_options[dbname]
                    db_json = self._get_single_database_json(
                        dbname, dev_opt, renamedatabases, sybasecreatedevice)
                else:
                    db_json = self._get_single_database_json(dbname=dbname)
            db_options.append(db_json)

        return db_options

    def _get_sybase_restore_json(self,
                                 destination_client,
                                 destination_instance_name,
                                 database_list,
                                 timevalue=None,
                                 sybasecreatedevice=False,
                                 renamedatabases=False,
                                 device_options=None,
                                 copy_precedence=0):
        """Method to construct sybase restore JSON for individual Database restore

        Args :

            destination_client_name  (str)    -- sybase destination client for restore

            destination_instance_name  (str)  -- sybase destination instance for restore

            database_list (list)              -- list of sybase databases to be restored

            timevalue (str)                   -- for pointintime based restore
                                              format: YYYY-MM-DD HH:MM:SS

            sybasecreatedevice (bool)         -- determines whether to createdevice
                                                 for sybase database restore

            renamedatabases (bool)            -- determines whether renamedatabase option
                                                 chosen for given database restore

            device_options  (dict(dict))      -- dict of dict for each database with
                                                 device rename and database rename options

            copy_precedence         (int)     --  copy precedence value of storage policy copy
                    default: 0


        Returns :

                return restore JSON for individual Sybase database restore

        """
        instance_restore = False
        pointintime = True
        # Check to perform renamedatabase/create device
        if (sybasecreatedevice is False) and (renamedatabases is False):
            device_options = None

        basic_sybase_options = self._get_sybase_restore_base_json(
            destination_client,
            destination_instance_name,
            pointintime,
            instance_restore,
            timevalue,
            sybasecreatedevice,
            renamedatabases,
            copy_precedence
        )
        restore_json = self._restore_json(paths=r'/')
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"] = basic_sybase_options
        db_options = self._db_option(
            database_list, renamedatabases, sybasecreatedevice, device_options
        )
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "sybaseRstOption"]["sybaseDatabase"] = db_options
        return restore_json

    def _get_sybase_full_restore_json(self,
                                      destination_client,
                                      destination_instance_name,
                                      pointintime=False,
                                      timevalue=None,
                                      sybasecreatedevice=True,
                                      renamedatabases=False,
                                      device_options=None,
                                      copy_precedence=0):
        """Method to create JSON for Full server restore

        Args :

            destination_client_name  (str)    -- sybase destination client for restore

            destination_instance_name  (str)  -- sybase destination instance for restore

            pointintime (bool)                -- determines pointintime based restore or not

            timevalue (str)                   -- for pointintime based restore
                                                format: YYYY-MM-DD HH:MM:SS

            sybasecreatedevice (bool)         -- determines whether to createdevice
                                                 for sybase database restore

            renamedatabases (bool)            -- determines whether renamedatabase option
                                                 chosen for given database restore

            device_options : (dict(dict))     -- dict of dict for each database with
                                                 device rename and database rename options

            copy_precedence         (int)     --  copy precedence value of storage policy copy
                    default: 0

        Returns :

                return restore JSON for Full sybase server restore

        """

        instance_restore = True
        basic_sybase_options = self._get_sybase_restore_base_json(
            destination_client,
            destination_instance_name,
            pointintime,
            instance_restore,
            timevalue,
            sybasecreatedevice,
            renamedatabases,
            copy_precedence)
        restore_json = self._restore_json(paths=r'/')
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"] = basic_sybase_options
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
            database_list, renamedatabases, sybasecreatedevice, device_options)
        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"][
            "sybaseRstOption"]["sybaseDatabase"] = db_options
        return restore_json

    def _get_single_database_json(
            self,
            dbname,
            device_options=None,
            renamedatabases=False,
            sybasecreatedevice=False):
        """
            Method to construct database JSON for individual Sybase databases with create device and rename database parameters

            Args :

                dbname (str)                      -- Database name opted for restore

                device_options : (dict(dict))       -- dict of dict for given database with device rename and database rename option

                sybasecreatedevice (bool)         -- determines whether to createdevice for sybase database restore

                renamedatabases : (bool)            -- determines whether renamedatabase option chosen for given database restore
            Returns :

                Individual Database option with restore [ for rename and create device ]

        """
        sybase_db_details = None
        databasechain = "0:0" + ":" + dbname + ":0"
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
            if sybasecreatedevice is True:
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
            if renamedatabases is True:
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

            data_device = subclientid + ":" + dbid + ":" + datadevid + ":" + datadevicename + \
                ":" + newdatadevicename + ":" + newdatadevicepath + \
                ":" + size + ":" + newdatabasename
            log_device = subclientid + ":" + dbid + ":" + logdevid + ":" + logdevicename + \
                ":" + newlogdevicename + ":" + newlogdevicepath + \
                ":" + size + ":" + newdatabasename
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
        Method to get all databases for the speicfied Sybase Server instance
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
                              pointintime=False,
                              timevalue=None,
                              renamedatabases=False,
                              device_options=None,
                              copy_precedence=0):
        """
        Method to restore the entire sybase server

        Args:

            destination_client_name  (str)   -- sybase destination client for restore

            destination_instance_name  (str) -- sybase destination instance for restore

            pointintime (bool)               -- determines pointintime based restore or not

            timevalue (str)                  -- for pointintime based restore
                                              format: YYYY-MM-DD HH:MM:SS

            sybasecreatedevice (bool)        -- determines whether to createdevice for sybase database restore

            renamedatabases (bool)           -- determines whether renamedatabase option chosen for given database restore

            device_options (dict(dict))      -- dict of dict for each database with device rename and database rename options

            copy_precedence         (int)    --  copy precedence value of storage policy copy
                    default: 0
        Note :

        Also This is dict  of dict having sourcedatabasename as Key and set of another dict options
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

            object -- Job containing restore details
        """

        if destination_client is None:
            destination_client = self.client_name

        if destination_instance_name is None:
            destination_instance_name = self.instance_name

        sybasecreatedevice = True
        request_json = self._get_sybase_full_restore_json(
            destination_client,
            destination_instance_name,
            pointintime,
            timevalue,
            sybasecreatedevice,
            renamedatabases,
            device_options, copy_precedence)

        # subclient_object = self.subclients.get('default')
        return self._process_restore_response(request_json)

    def restore_database(self,
                         destination_client=None,
                         destination_instance_name=None,
                         database_list=None,
                         timevalue=None,
                         sybasecreatedevice=False,
                         renamedatabases=False,
                         device_options=None,
                         copy_precedence=0):
        """

        Method to restore the individual databases

        Args:

            destination_client_name  (str)    -- sybase destination client for restore

            destination_instance_name  (str)  -- sybase destination instance for restore

            database_list (list)              -- list of sybase databases to be restored

            timevalue (str)                   -- for pointintime based restore
                                              format: YYYY-MM-DD HH:MM:SS

            sybasecreatedevice (bool)         -- determines whether to createdevice for sybase database restore

            renamedatabases (bool)            -- determines whether renamedatabase option chosen for given database restore

            device_options (dict(dict))       -- dict of dict for each database with device rename and database rename options

            copy_precedence         (int)     --  copy precedence value of storage policy copy
                    default: 0
        Note :

        Also This is dict  of dict having sourcedatabasename as Key and set of another dict options
        as value corresponding to that source Database.

        Also if you wouldn't want to pass value for particular option , mark it none


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
            object -- Job containing restore details


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
            sybasecreatedevice,
            renamedatabases,
            device_options,
            copy_precedence)
        # subclient_object = self.subclients.get('default')
        return self._process_restore_response(request_json)
