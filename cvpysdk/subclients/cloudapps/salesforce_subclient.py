# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for operating on a Salesforce Subclient.

SalesforceSubclient is the only class defined in this file.

SalesforceSubclient:     Derived class from CloudAppsSubclient Base class, representing a
                            salesforce subclient, and to perform operations on that subclient

SalesforceSubclient:

    _get_subclient_properties()               --  Subclient class method overwritten to add
                                                      salesforce subclient properties as well

    _get_subclient_properties_json()          --  gets all the subclient  related properties of
                                                      salesforce subclient.

    browse()                                  --  Browses the salesforce content

    _check_object_in_browse()                 --  internal method to check the object exists
                                                      in browse content

    _restore_salesforce_options_json()        --  internal method for salesforce options json

    _restore_salesforce_destination_json()    --  internal method for salesforce destination option
                                                      json

    restore_to_file_system()                  --  restores the selected content to filesystem

    restore_to_database()                     --  restores the selected content to database

    restore_to_salesforce_from_database()     --  restores the selected content to salesforce from
                                                      database

    restore_to_salesforce_from_media()        --  restores the selected content to salesforce from
                                                      media

    _prepare_salesforce_restore_json()        --  internal method which prepares entire restore
                                                      json for salesforce

"""

from __future__ import unicode_literals

from base64 import b64encode
from past.builtins import basestring

from ..casubclient import CloudAppsSubclient

from ...client import Client
from ...agent import Agent
from ...instance import Instance
from ...backupsets.cloudapps.salesforce_backupset import SalesforceBackupset
from ...exception import SDKException


class SalesforceSubclient(CloudAppsSubclient):
    """Derived class from CloudAppsSubclient Base class, representing a Salesforce subclient,
        and to perform operations on that subclient."""

    def _get_subclient_properties(self):
        """Gets the properties of this subclient.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        super(SalesforceSubclient, self)._get_subclient_properties()

        if 'CloudAppsSubclientProp' in self._subclient_properties:
            self._cloud_apps_subclient_prop = self._subclient_properties['CloudAppsSubclientProp']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.

           Returns:
                dict - all subclient properties put inside a dict

        """
        subclient_json = {
            "subClientProperties": {
                "proxyClient": self._proxyClient,
                "subClientEntity": self._subClientEntity,
                "CloudAppsSubclientProp": self._cloud_apps_subclient_prop,
                "commonProperties": self._commonProperties,
                "contentOperationType": 1
            }
        }

        return subclient_json

    def check_object_in_browse(self, object_to_restore, browse_data):
        """Check if the particular object is present in browse of the subclient

            Args:
                _object_to_restore     (str)   --  folder path whioch has to be restored

                _browse_data           (str)   --  list of objects from browse response

            Raises:
                SDKException:
                    if object is not present in browse result

        """
        source_item = None

        if (object_to_restore.find("/Objects") < 0 and
                object_to_restore.find("/") < 0 and
                object_to_restore.find("/Files") < 0):
            restore_object_name = "/Objects/" + object_to_restore
        else:
            restore_object_name = object_to_restore

        for path in browse_data:
            if path.find(restore_object_name) >= 0:
                source_item = path
                break

        if source_item is None:
            raise SDKException('Subclient', '113')

        return restore_object_name

    def _restore_salesforce_options_json(self, value):
        """setter for the salesforce restore  options in restore json
            Raises:
                SDKException:
                    if input value is not dictionary
        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._salesforce_restore_option_json = {
            "instanceType": 'SALESFORCE',
            "salesforceRestoreOptions": {
                "restoreToFileSystem": value.get("to_fs", True),
                "pathToStoreCsv": value.get("staging_path", '/tmp/'),
                "dependentRestoreLevel": value.get("dependent_level", 0),
                "isMetadataRestore": value.get("is_metadata", False),
                "restoreToSalesforce": value.get("to_cloud", False),
                "restoreFromDatabase": value.get("from_database", False),
                "overrideTable": value.get("override_table", True),
                "syncDatabase": {
                    "dbEnabled": value.get("db_enabled", False),
                    "dbType": value.get("db_type", 'SQLSERVER'),
                    "dbHost": value.get("db_host", ''),
                    "dbPort": value.get("db_port", '1433'),
                    "dbName": value.get("db_name", ''),
                    "dbInstance": value.get("db_instance", ''),
                    "dbUserPassword": {
                        "userName": value.get("db_user_name", ''),
                        "password": value.get("db_user_password", '')
                    },

                }

            }
        }

    def _restore_salesforce_destination_json(self, value):
        """setter for  the salesforce destination restore option in restore JSON
            Raises:
                SDKException:
                    if input value is not dictionary
        """

        if not isinstance(value, dict):
            raise SDKException('Subclient', '101')

        self._destination_restore_json = {
            "destClient": {
                "clientName": value.get("dest_client_name", "")
            },
            "destinationInstance": {
                "instanceName": value.get("dest_instance_name", ""),
                "appName": 'Cloud Apps',
                "clientName": value.get("dest_client_name", "")
            },
            "destinationBackupset": {
                "backupsetName": value.get("dest_backupset_name", ""),
                "instanceName": value.get("dest_instance_name", ""),
                "appName": 'Cloud Apps',
                "clientName": value.get("dest_client_name", "")
            },
            "noOfStreams": value.get("streams", 2)
        }

    def restore_to_file_system(
            self,
            objects_to_restore=None,
            destination_client=None,
            sf_options=None):
        """perform restore to file system to the provided path

        Args:
            objects_to_restore  (str)   --  list of objects to restore

            destination_client  (str)   --  destination client name where cloud connector
                                                package exists if this value not provided,
                                                it will automatically use source backup client

            sf_options          (dict)

                destination_path    (str)   :   staging path for salesforce restore data.
                                                    if this value is not provided, uses download
                                                    cache path from source

                dependent_level     (int)   :   restore children based on selected level.
                                                    0   -   no Children
                                                    1   -   immediate children
                                                    -1  -   All children
                    default: 0

                streams             (int)   :   no of streams to use for restore
                    default: 2

                copy_precedence     (int)   :   copy number to use for restore
                    default: 0

                from_time           (str)   :   date to get the contents after
                                                    format: dd/MM/YYYY
                                                    gets content from 01/01/1970 if not specified
                    default: 0

                to_time             (str)   :   date to get the contents before
                                                    format: dd/MM/YYYY
                                                    gets content till latest if not specified
                    default: 0

                show_deleted_files  (bool)  :   include deleted files in the content or not
                    default: True

         Raises:
                SDKException:
                    if from time value is incorrect

                    if to time value is incorrect

                    if to time is less than from time

                    if failed to browse content

                    if response is empty

                    if response is not success

                    if destination client does not exist on commcell

        """

        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._instance_object.proxy_client

        if isinstance(destination_client, Client):
            client = destination_client
        elif isinstance(destination_client, basestring):
            client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        file_restore_option["client_name"] = client.client_name
        file_restore_option["destination_path"] = sf_options.get(
            "destination_path", self._backupset_object.download_cache_path
        )

        self._restore_destination_json(file_restore_option)

        # process the objects to restore
        if isinstance(objects_to_restore, list):
            objects_to_restore_list = objects_to_restore

        else:
            objects_to_restore_list = []
            objects_to_restore_list.append(objects_to_restore)

        file_restore_option["source_item"] = []
        browse_files, _ = self.browse(
            path='/Objects',
            from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0)
        )

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["source_item"].append(
                    self.check_object_in_browse("%s" % each_object, browse_files)
                )

        # set the salesforce options
        file_restore_option["staging_path"] = sf_options.get(
            "destination_path",
            self._backupset_object.download_cache_path
        )
        file_restore_option["dependent_level"] = sf_options.get("dependent_level", 0)
        file_restore_option["to_fs"] = True
        file_restore_option["streams"] = sf_options.get("streams", 2)

        # set the browse option
        file_restore_option["copy_precedence_applicable"] = True
        file_restore_option["copy_precedence"] = sf_options.get("copy_precedence", 0)

        # prepare and execute the Json
        request_json = self._prepare_salesforce_restore_json(file_restore_option)

        return self._process_restore_response(request_json)

    def restore_to_database(
            self,
            objects_to_restore=None,
            destination_client=None,
            sf_options=None):
        """perform Restore to  Database

        Args:
            objects_to_restore  (str)   --  list of objects to restore

            destination_client  (str)   --  destination clientname where cloud connector package
                                                exists. if this value not provided, it will
                                                automatically use source backup client

            sf_options          (dict)

                destination_path    (str)   :   staging path for salesforce restore data.
                                                    if this value is not provided, it will
                                                    automatically use download cache path
                                                    from source

                db_type             (str)   :   database type. if database details does not
                                                    provided, it will use syncdb database
                                                    for restore
                    default: SQLSERVER

                db_host             (str)   :   database hostname (ex:dbhost.company.com)

                db_instance         (str)   :   database instance name
                                                    (provide if applicable for that database type)

                db_name             (str)   :   database database name
                                                    (it is where data will be imported)

                db_port             (str)   :   database connection port
                    default: 1433

                db_user_name        (str)   :   database username
                                                    (it should have read/write permissions on db)

                db_user_password    (str)   :   database user password

                overrirde_table     (bool)  :   overrides the tables on  database
                    default: True

                dependent_level     (int)   :   restore dependent object based on selected level.
                                                    0   -   no Children
                                                    1   -   immediate children
                                                   -1   -   All children
                    default: 0

                streams             (int)   :   no of streams to use for restore
                    default: 2

                copy_precedence     (int)   :   copy number to use for restore
                    default: 0

                from_date           (str)   :   date to get the contents after
                                                    format: dd/MM/YYYY
                                                    gets contents from 01/01/1970 if not specified
                    default: 0

                to_date             (str)   :   date to get the contents before
                                                    format: dd/MM/YYYY
                                                    gets contents till current day if not specified
                    default: 0

                show_deleted_files  (bool)  :   include deleted files in the content or not
                    default: True

        Raises:
            SDKException:
                if from time value is incorrect

                if to time value is incorrect

                if to time is less than from time

                if failed to browse content

                if response is empty

                if response is not success

                if destination client does not exist on commcell

                if all the database details not provided

        """
        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._instance_object.proxy_client

        if isinstance(destination_client, Client):
            dest_client = destination_client
        elif isinstance(destination_client, basestring):
            dest_client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        if not ('db_host' in sf_options and
                'db_instance' in sf_options and
                'db_name' in sf_options and
                'db_user_name' in sf_options and
                'db_user_password' in sf_options):
            raise SDKException('Salesforce', '101')

        # set the destination client
        file_restore_option["client_name"] = dest_client.client_name
        file_restore_option["destination_path"] = sf_options.get(
            "destination_path", self._backupset_object.download_cache_path
        )

        self._restore_destination_json(file_restore_option)

        # process the objects to restore
        if isinstance(objects_to_restore, list):
            objects_to_restore_list = objects_to_restore

        else:
            objects_to_restore_list = []
            objects_to_restore_list.append(objects_to_restore)

        file_restore_option["source_item"] = []
        browse_files, _ = self.browse(
            path='/Objects',
            from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0)
        )

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["source_item"].append(
                    self.check_object_in_browse("%s" % each_object, browse_files)
                )

        # set the salesforce options
        file_restore_option["staging_path"] = sf_options.get(
            "destination_path", self._backupset_object.download_cache_path
        )
        file_restore_option["dependent_level"] = sf_options.get("dependent_level", 0)
        file_restore_option["streams"] = sf_options.get("streams", 2)
        file_restore_option["to_fs"] = False
        file_restore_option["db_enabled"] = True
        file_restore_option["db_type"] = sf_options.get("db_type", 'SQLSERVER')
        file_restore_option["db_host"] = sf_options.get("db_host", "")
        file_restore_option["db_instance"] = sf_options.get("db_instance", "")
        file_restore_option["db_name"] = sf_options.get("db_name", "autorestoredb")
        file_restore_option["db_port"] = sf_options.get("db_port", '1433')
        file_restore_option["db_user_name"] = sf_options.get("db_user_name", 'sa')
        db_base64_password = b64encode(sf_options['db_user_password'].encode()).decode()
        file_restore_option["db_user_password"] = db_base64_password
        file_restore_option["override_table"] = sf_options.get("override_table", True)

        # set the browse option
        file_restore_option["copy_precedence_applicable"] = True
        file_restore_option["copy_precedence"] = sf_options.get("copy_precedence", 0)
        file_restore_option["from_time"] = sf_options.get("from_time", 0)
        file_restore_option["to_time"] = sf_options.get("to_time", 0)

        # prepare and execute the Json
        request_json = self._prepare_salesforce_restore_json(file_restore_option)

        return self._process_restore_response(request_json)

    def restore_to_salesforce_from_database(
            self,
            objects_to_restore=None,
            destination_client=None,
            destination_instance=None,
            destination_backupset=None,
            sf_options=None):
        """perform Restore to Salesforce from Database

        Args:
            objects_to_restore      (str)   --  list of objects to restore

            destination_client      (str)   --  destination pseudo client name.
                                                    if this value not provided, it will
                                                    automatically select source client

            destination_instance    (str)   --  destination instance name.
                                                    if this value not provided, it will
                                                    automatically select source instance name

            destination_backupset   (str)   --  destination backupset name.
                                                    if this value not provided, it will
                                                    automatically select source backupset
            sf_options              (dict)

                destination_path    (str)   :   staging path for salesforce restore data

                db_type             (str)   :   database type. if database details does not
                                                    provided, it will use syncdb database
                                                    for restore
                    default: SQLSERVER

                db_host             (str)   :   database hostname (ex:dbhost.company.com)

                db_instance         (str)   :   database instance name
                                                    (provide if applicable for that database type)

                db_name             (str)   :   database database name
                                                    (it is where data will be imported)

                db_port             (str)   :   database connection port
                    default: 1433

                db_user_name        (str)   :   database username
                                                    (read/write permissions needed on db)

                db_user_password    (str)   :   database user password

                overrirde_table     (bool)  :   overrides the tables on  database
                    default: True

                dependent_level     (int)   :   restore children based on selected level.
                                                    0   -   no Children
                                                    1   -   immediate children
                                                    -1  -   All children
                    default: 0

                streams             (int)   :   no of streams to use for restore
                    default: 2

                copy_precedence     (int)   :   copy number to use for restore
                    default: 0

                from_time           (str)   :   date to get the contents after
                                                    format: dd/MM/YYYY
                                                    gets contents from 01/01/1970 if not specified
                    default: None

                to_time             (str)   :   date to get the contents before
                                                    format: dd/MM/YYYY
                                                    gets contents till current day if not specified
                    default: None

                show_deleted_files  (bool)  :   include deleted files in the content or not
                    default: True

        Raises:
            SDKException:
                if from date value is incorrect

                if to date value is incorrect

                if to date is less than from date

                if failed to browse content

                if response is empty

                if response is not success

                if destination client does not exist

                if destination instance does not exist

                if destination backupset does not exist

                if syncdb is not enabled and user not provided the database details

        """
        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._agent_object._client_object

        if isinstance(destination_client, Client):
            dest_client = destination_client
        elif isinstance(destination_client, basestring):
            dest_client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        dest_agent = Agent(dest_client, 'Cloud Apps')

        # check if instance name is correct
        if destination_instance is None:
            destination_instance = self._backupset_object._instance_object

        if isinstance(destination_instance, Instance):
            dest_instance = destination_instance
        elif isinstance(destination_instance, basestring):
            dest_instance = dest_agent.instances.get(destination_instance)
        else:
            raise SDKException('Subclient', '113')

        # check if backupset name is correct
        if destination_backupset is None:
            destination_backupset = self._backupset_object

        if isinstance(destination_backupset, SalesforceBackupset):
            dest_backupset = destination_backupset
        elif isinstance(destination_backupset, basestring):
            dest_backupset = SalesforceBackupset(dest_instance, destination_backupset)
        else:
            raise SDKException('Subclient', '114')

        if not self._backupset_object.is_sync_db_enabled:
            if not (
                    'db_host' in sf_options and 'db_instance' in sf_options and
                    'db_name' in sf_options and 'db_user_name' in sf_options and
                    'db_user_password' in sf_options):
                raise SDKException('Salesforce', '101')

        # set salesforce destination client
        file_restore_option["dest_client_name"] = dest_client.client_name
        file_restore_option["dest_instance_name"] = dest_instance.instance_name
        file_restore_option["dest_backupset_name"] = dest_backupset.backupset_name

        self._restore_salesforce_destination_json(file_restore_option)

        # process the objects to restore
        if isinstance(objects_to_restore, list):
            objects_to_restore_list = objects_to_restore

        else:
            objects_to_restore_list = []
            objects_to_restore_list.append(objects_to_restore)

        file_restore_option["source_item"] = []
        browse_files, _ = self.browse(
            path='/Objects', from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0))

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["source_item"].append(
                    self.check_object_in_browse(
                        "%s" %
                        each_object,
                        browse_files))

        # set the salesforce options
        file_restore_option["staging_path"] = sf_options.get(
            "destination_path",
            dest_backupset.download_cache_path)
        file_restore_option["dependent_level"] = sf_options.get("dependent_level", 0)
        file_restore_option["streams"] = sf_options.get("streams", 2)
        file_restore_option["to_fs"] = False
        file_restore_option["to_cloud"] = True
        file_restore_option["from_database"] = True
        file_restore_option["db_enabled"] = True
        if (self._backupset_object.is_sync_db_enabled) or ('db_host' in sf_options):
            if self._backupset_object.sync_db_type is None:
                dbtype = 'SQLSERVER'
            else:
                dbtype = self._backupset_object.is_sync_db_enabled
            file_restore_option["db_type"] = sf_options.get("db_type", dbtype)
            file_restore_option["db_host"] = sf_options.get(
                "db_host", self._backupset_object.sync_db_host
            )
            file_restore_option["db_instance"] = sf_options.get(
                "db_instance", self._backupset_object.sync_db_instance
            )
            file_restore_option["db_name"] = sf_options.get(
                "db_name", self._backupset_object.sync_db_name
            )
            file_restore_option["db_port"] = sf_options.get(
                "db_port", self._backupset_object.sync_db_port
            )
            file_restore_option["db_user_name"] = sf_options.get(
                "db_user_name", self._backupset_object.sync_db_user_name
            )

            if 'db_user_password' in sf_options:
                sf_options['_db_base64_password'] = b64encode(
                    sf_options['db_user_password'].encode()).decode()

            file_restore_option["db_user_password"] = sf_options.get(
                "_db_base64_password",
                self._backupset_object._sync_db_user_password)
        else:
            raise SDKException('Salesforce', '101')

        file_restore_option["override_table"] = sf_options.get("override_table", True)

        # set the browse option
        file_restore_option["client_name"] = self._backupset_object._agent_object._client_object.client_name
        file_restore_option["copy_precedence_applicable"] = True
        file_restore_option["copy_precedence"] = sf_options.get("copy_precedence", 0)
        file_restore_option["from_time"] = sf_options.get("from_time", 0)
        file_restore_option["to_time"] = sf_options.get("to_time", 0)

        # prepare and execute the Json
        request_json = self._prepare_salesforce_restore_json(file_restore_option)

        return self._process_restore_response(request_json)

    def restore_to_salesforce_from_media(
            self,
            objects_to_restore=None,
            destination_client=None,
            destination_instance=None,
            destination_backupset=None,
            sf_options=None):
        """perform Restore to Salesforce from Media.

        Args:
            objects_to_restore      (str)   --  list of objects to restore

            destination_client      (str)   --  destination pseudo client name.
                                                    if this value not provided, it will
                                                    automatically select source client

            destination_instance    (str)   --  destination instance name.
                                                    if this value not provided, it will
                                                    automatically select source instance name

            destination_backupset   (str)   --  destination backupset name.
                                                    if this value not provided, it will
                                                    automatically select source backupset
            sf_options              (dict)

                destination_path    (str)   :   staging path for salesforce restore data

                db_type             (str)   :   database type. if database details does not
                                                    provided, it will use syncdb database
                                                    for restore
                    default: SQLSERVER

                db_host             (str)   :   database hostname (ex:dbhost.company.com)

                db_instance         (str)   :   database instance name
                                                    (provide if applicable for that database type)

                db_name             (str)   :   database database name
                                                    (it is where data will be imported)

                db_port             (str)   :   database connection port
                    default: 1433

                db_user_name        (str)   :   database username
                                                    (read/write permissions needed on db)

                db_user_password    (str)   :   database user password

                overrirde_table     (bool)  :   overrides the tables on  database
                    default: True

                dependent_level     (int)   :   restore children based on selected level.
                                                    0   -   no Children
                                                    1   -   immediate children
                                                    -1  -   All children
                    default: 0

                streams             (int)   :   no of streams to use for restore
                    default: 2

                copy_precedence     (int)   :   copy number to use for restore
                    default: 0

                from_time           (str)   :   date to get the contents after
                                                    format: dd/MM/YYYY
                                                    gets contents from 01/01/1970 if not specified
                    default: None

                to_time             (str)   :   date to get the contents before
                                                    format: dd/MM/YYYY
                                                    gets contents till current day if not specified
                    default: None

                show_deleted_files  (bool)  :   include deleted files in the content or not
                    default: True

        Raises:
                SDKException:
                    if from date value is incorrect

                    if to date value is incorrect

                    if to date is less than from date

                    if failed to browse content

                    if response is empty

                    if response is not success

                    if destination client does not exist

                    if destination instance does not exist

                    if destination backupset does not exist

                    if user does not provide staging database details

        """

        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._agent_object._client_object

        if isinstance(destination_client, Client):
            dest_client = destination_client
        elif isinstance(destination_client, basestring):
            dest_client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        dest_agent = Agent(dest_client, 'Cloud Apps')

        # check if instance name is correct
        if destination_instance is None:
            destination_instance = self._backupset_object._instance_object

        if isinstance(destination_instance, Instance):
            dest_instance = destination_instance
        elif isinstance(destination_instance, basestring):
            dest_instance = dest_agent.instances.get(destination_instance)
        else:
            raise SDKException('Subclient', '113')

        # check if backupset name is correct
        if destination_backupset is None:
            destination_backupset = self._backupset_object

        if isinstance(destination_backupset, SalesforceBackupset):
            dest_backupset = destination_backupset
        elif isinstance(destination_backupset, basestring):
            dest_backupset = SalesforceBackupset(dest_instance, destination_backupset)
        else:
            raise SDKException('Subclient', '114')

        if not ('db_host' in sf_options and
                'db_instance' in sf_options and
                'db_name' in sf_options and
                'db_user_name' in sf_options and
                'db_user_password' in sf_options):
            raise SDKException('Salesforce', '101')

        file_restore_option["dest_client_name"] = dest_client.client_name
        file_restore_option["dest_instance_name"] = dest_instance.instance_name
        file_restore_option["dest_backupset_name"] = dest_backupset.backupset_name

        self. _restore_salesforce_destination_json(file_restore_option)

        # process the objects to restore
        if isinstance(objects_to_restore, list):
            objects_to_restore_list = objects_to_restore

        else:
            objects_to_restore_list = []
            objects_to_restore_list.append(objects_to_restore)

        file_restore_option["source_item"] = []
        browse_files, _ = self.browse(
            path='/Objects',
            from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0)
        )

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["source_item"].append(
                    self.check_object_in_browse("%s" % each_object, browse_files)
                )

        # set the salesforce options
        file_restore_option["staging_path"] = sf_options.get(
            "destination_path", dest_backupset.download_cache_path
        )
        file_restore_option["dependent_level"] = sf_options.get("dependent_level", 0)
        file_restore_option["streams"] = sf_options.get("streams", 2)
        file_restore_option["to_fs"] = False
        file_restore_option["to_cloud"] = True
        file_restore_option["from_database"] = False
        file_restore_option["db_enabled"] = True
        file_restore_option["db_type"] = sf_options.get("db_type", 'SQLSERVER')
        file_restore_option["db_host"] = sf_options.get("db_host", "")
        file_restore_option["db_instance"] = sf_options.get("db_instance", "")
        file_restore_option["db_name"] = sf_options.get("db_name", 'autorestoredb')
        file_restore_option["db_port"] = sf_options.get("db_port", '1433')
        file_restore_option["db_user_name"] = sf_options.get("db_user_name", 'sa')
        db_base64_password = b64encode(sf_options['db_user_password'].encode()).decode()
        file_restore_option["db_user_password"] = db_base64_password
        file_restore_option["override_table"] = sf_options.get("override_table", True)

        # set the browse option
        file_restore_option["client_name"] = self._backupset_object._agent_object._client_object.client_name
        file_restore_option["copy_precedence_applicable"] = True
        file_restore_option["copy_precedence"] = sf_options.get("copy_precedence", 0)
        file_restore_option["from_time"] = sf_options.get("from_time", 0)
        file_restore_option["to_time"] = sf_options.get("to_time", 0)

        # prepare and execute the Json
        request_json = self._prepare_salesforce_restore_json(file_restore_option)

        return self._process_restore_response(request_json)

    def _prepare_salesforce_restore_json(self, file_restore_option):
        """prepares the  salesforce restore json from getters."""
        self._restore_fileoption_json(file_restore_option)
        self._restore_salesforce_options_json(file_restore_option)
        self._restore_browse_option_json(file_restore_option)
        self._impersonation_json(file_restore_option)
        self._restore_commonOptions_json(file_restore_option)

        request_json = {
            "taskInfo": {
                "associations": [self._subClientEntity],
                "task": self._json_task,
                "subTasks": [{
                    "subTask": self._json_restore_subtask,
                    "options": {
                        "restoreOptions": {
                            "impersonation": self._impersonation_json_,
                            "cloudAppsRestoreOptions": self._salesforce_restore_option_json,
                            "browseOption": self._browse_restore_json,
                            "commonOptions": self._commonoption_restore_json,
                            "destination": self._destination_restore_json,
                            "fileOption": self._fileoption_restore_json,

                        }
                    }
                }]
            }
        }

        return request_json
