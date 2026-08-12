# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
    enable_files                              --  Enables files option on subclient content

    disable_files                             --  Disables files option on subclient content

    enable_metadata                           --  Enables metadata option on subclient content

    disable_metadata                          --  Disables metadata option on subclient content

    enable_archived_deleted                   --  Enables backup archived and deleted option on subclient content

    disable_archived_deleted                  --  Disables backup archived and deleted  option on subclient content

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
from typing import Any, Dict, List, Optional

from ..casubclient import CloudAppsSubclient

from ...agent import Agent
from ...backupsets.cloudapps.salesforce_backupset import SalesforceBackupset
from ...client import Client
from ...exception import SDKException
from ...instance import Instance


class SalesforceSubclient(CloudAppsSubclient):
    """
    SalesforceSubclient provides specialized management and restore operations for Salesforce data
    within the CloudAppsSubclient framework.

    This class enables users to interact with Salesforce subclients, retrieve and manage their properties,
    and perform advanced restore operations to various destinations including file systems, databases,
    and Salesforce instances. It offers granular control over the inclusion of files, metadata, and archived/deleted items,
    as well as utilities for browsing and validating objects for restore.

    Key Features:
        - Initialization and configuration of Salesforce subclient instances
        - Retrieval of subclient properties and their JSON representations
        - Properties for accessing objects, files, metadata, and archived/deleted items
        - Enable/disable management for files, metadata, and archived/deleted items
        - Object validation within browse data for restore operations
        - Preparation of restore options and destination configurations for Salesforce
        - Restore capabilities:
            - Restore to file system
            - Restore to database
            - Restore to Salesforce from database or media
            - Metadata restore to Salesforce
        - Internal utilities for preparing restore JSON payloads

    This class is intended for use in environments where Salesforce data protection and recovery
    are managed through the CloudAppsSubclient infrastructure.

    #ai-gen-doc
    """

    def __init__(self, backupset_object: object, subclient_name: str, subclient_id: str = None) -> None:
        """Initialize a SalesforceSubclient instance.

        Args:
            backupset_object: Instance of the Backupset class associated with this subclient.
            subclient_name: Name of the Salesforce subclient.
            subclient_id: Optional; unique identifier for the subclient. If not provided, a new subclient may be created.

        Example:
            >>> backupset = Backupset(commcell_object, 'SalesforceBackupset')
            >>> subclient = SalesforceSubclient(backupset, 'DailySalesforceSubclient')
            >>> # Optionally, specify an existing subclient ID
            >>> subclient_with_id = SalesforceSubclient(backupset, 'ExistingSubclient', subclient_id='12345')

        #ai-gen-doc
        """
        self.cloud_apps_subclient_prop = {}
        self._files = None
        self._metadata = None
        self._archived_deleted = None
        self._objects = None
        super(SalesforceSubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def _get_subclient_properties(self) -> None:
        """Retrieve and update the properties of this Salesforce subclient.

        This method fetches the latest properties for the subclient from the backend service
        and updates the internal state accordingly.

        Raises:
            SDKException: If the response from the backend is empty or indicates a failure.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient._get_subclient_properties()
            >>> print("Subclient properties refreshed successfully")

        #ai-gen-doc
        """
        super(SalesforceSubclient, self)._get_subclient_properties()

        if 'cloudAppsSubClientProp' in self._subclient_properties:
            self._cloud_apps_subclient_prop = self._subclient_properties['cloudAppsSubClientProp']
            if 'salesforceSubclient' in self._cloud_apps_subclient_prop:
                sfsubclient = self._cloud_apps_subclient_prop['salesforceSubclient']
                self._objects = sfsubclient.get('backupSfObjects')
                self._files = sfsubclient.get('backupFileObjects')
                self._metadata = sfsubclient.get('backupSFMetadata')
                self._archived_deleted = sfsubclient.get('backupArchivedandDeletedRecs')

    def _get_subclient_properties_json(self) -> dict:
        """Retrieve all properties related to this Salesforce subclient.

        Returns:
            dict: A dictionary containing all subclient properties.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> properties = subclient._get_subclient_properties_json()
            >>> print(properties)
            {'property1': 'value1', 'property2': 'value2', ...}

        #ai-gen-doc
        """
        subclient_json = {
            "subClientProperties": {
                "proxyClient": self._proxyClient,
                "subClientEntity": self._subClientEntity,
                "cloudAppsSubClientProp": self._cloud_apps_subclient_prop,
                "commonProperties": self._commonProperties,
                "contentOperationType": 1
            }
        }

        return subclient_json

    @property
    def objects(self) -> dict:
        """Get the Salesforce files option for this subclient.

        Returns:
            dict: A dictionary containing the Salesforce files option details for the subclient.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> files_option = subclient.objects
            >>> print(files_option)
            {'option1': 'value1', 'option2': 'value2'}

        #ai-gen-doc
        """
        return self._objects

    @property
    def files(self) -> dict:
        """Get the Salesforce files option settings for this subclient.

        Returns:
            dict: A dictionary containing the Salesforce files option configuration.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> files_option = subclient.files
            >>> print(files_option)
            {'include_files': True, 'max_file_size': 1048576}

        #ai-gen-doc
        """
        return self._files

    @property
    def metadata(self) -> dict:
        """Get the Salesforce metadata options for this subclient.

        Returns:
            dict: A dictionary containing the Salesforce metadata configuration options.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> metadata_options = subclient.metadata  # Use dot notation for property access
            >>> print(metadata_options)
            >>> # Output might include metadata settings such as object types, fields, etc.

        #ai-gen-doc
        """
        return self._metadata

    @property
    def archived_deleted(self) -> Any:
        """Get the archived and deleted Salesforce backup data for this subclient.

        Returns:
            The archived and deleted data associated with the Salesforce backup. The exact type depends on the implementation.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> archived_data = subclient.archived_deleted
            >>> print(archived_data)
            >>> # Use the returned data for further processing or analysis

        #ai-gen-doc
        """
        return self._archived_data

    def enable_files(self) -> None:
        """Enable the files option on the subclient content.

        This method activates the files option for the Salesforce subclient, allowing file-level operations on the subclient's content.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient.enable_files()
            >>> print("Files option enabled for the subclient.")

        #ai-gen-doc
        """
        if not self.files:
            self._set_subclient_properties("_subclient_properties['cloudAppsSubClientProp']\
                                           ['salesforceSubclient']['backupFileObjects']", True)

    def enable_metadata(self) -> None:
        """Enable the metadata option for the subclient content.

        This method activates the metadata option on the subclient, allowing metadata to be included
        in backup operations for Salesforce data.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient.enable_metadata()
            >>> print("Metadata option enabled for the subclient.")

        #ai-gen-doc
        """
        if not self.metadata:
            self._set_subclient_properties("_subclient_properties['cloudAppsSubClientProp']\
                                           ['salesforceSubclient']['backupSFMetadata']", True)

    def enable_archived_deleted(self) -> None:
        """Enable the backup of archived and deleted items on the subclient content.

        This method configures the subclient to include archived and deleted Salesforce data in backup operations.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient.enable_archived_deleted()
            >>> print("Archived and deleted items backup enabled for subclient.")
        #ai-gen-doc
        """
        if self.archived_deleted:
            self._set_subclient_properties("_subclient_properties['cloudAppsSubClientProp']\
                                           ['salesforceSubclient']['backupArchivedandDeletedRecs']", False)

    def disable_files(self) -> None:
        """Disable the files option on the subclient content.

        This method disables the files option for the current Salesforce subclient,
        preventing files from being included in the subclient's content.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient.disable_files()
            >>> print("Files option disabled for the subclient.")
        #ai-gen-doc
        """
        if self.files:
            self._set_subclient_properties("_subclient_properties['cloudAppsSubClientProp']\
                                           ['salesforceSubclient']['backupFileObjects']", False)

    def disable_metadata(self) -> None:
        """Disable the metadata option on the subclient content.

        This method disables the metadata option for the Salesforce subclient,
        preventing metadata from being included in backup operations.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient.disable_metadata()
            >>> print("Metadata option disabled for the subclient.")
        #ai-gen-doc
        """
        if self.metadata:
            self._set_subclient_properties("_subclient_properties['cloudAppsSubClientProp']\
                                           ['salesforceSubclient']['backupSFMetadata']", False)

    def disable_archived_deleted(self) -> None:
        """Disable the backup of archived and deleted records for the subclient content.

        This method turns off the option to include archived and deleted records in the backup
        for the Salesforce subclient. Use this when you want to exclude such records from future backups.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient.disable_archived_deleted()
            >>> print("Archived and deleted records will no longer be backed up.")
        #ai-gen-doc
        """
        if not self.archived_deleted:
            self._set_subclient_properties("_subclient_properties['cloudAppsSubClientProp']\
                                           ['salesforceSubclient']['backupArchivedandDeletedRecs']", True)

    def check_object_in_browse(self, object_to_restore: str, browse_data: list) -> None:
        """Check if a specific object is present in the subclient's browse data.

        This method verifies whether the specified object (such as a folder or file path)
        exists within the provided browse data list for the subclient. If the object is
        not found, an SDKException is raised.

        Args:
            object_to_restore: The path of the object (e.g., folder or file) to check for in the browse data.
            browse_data: List of objects returned from the subclient's browse response.

        Raises:
            SDKException: If the specified object is not present in the browse result.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> browse_result = subclient.browse()
            >>> subclient.check_object_in_browse('Accounts', browse_result)
            >>> # If 'Accounts' is not present, an SDKException will be raised.

        #ai-gen-doc
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

    def _restore_salesforce_options_json(self, value: dict) -> None:
        """Set the Salesforce restore options in the restore JSON configuration.

        This method assigns the provided dictionary of Salesforce restore options to the internal restore JSON structure.
        The input must be a dictionary; otherwise, an SDKException will be raised.

        Args:
            value: A dictionary containing Salesforce restore options to be set.

        Raises:
            SDKException: If the input value is not a dictionary.

        Example:
            >>> options = {
            ...     "restoreType": "Full",
            ...     "includeAttachments": True
            ... }
            >>> subclient._restore_salesforce_options_json(options)
            >>> # The Salesforce restore options are now set in the restore JSON

        #ai-gen-doc
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
                    "dbHost": value.get("db_host_name", ''),
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

    def _restore_salesforce_destination_json(self, value: dict) -> None:
        """Set the Salesforce destination restore options in the restore JSON.

        This method updates the restore JSON with the provided Salesforce destination options.

        Args:
            value: A dictionary containing Salesforce destination restore options.

        Raises:
            SDKException: If the input value is not a dictionary.

        Example:
            >>> options = {
            ...     "destinationOrg": "TargetOrg",
            ...     "restoreType": "Full"
            ... }
            >>> subclient._restore_salesforce_destination_json(options)
            >>> # The restore JSON is now updated with the specified destination options

        #ai-gen-doc
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
            objects_to_restore: Optional[List[str]] = None,
            destination_client: Optional[str] = None,
            sf_options: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Perform a restore of Salesforce data to the file system at the specified path.

        This method restores selected Salesforce objects to a staging path on the specified destination client.
        If no destination client is provided, the source backup client is used by default. Additional restore
        options can be specified using the `sf_options` dictionary.

        Args:
            objects_to_restore: Optional list of Salesforce object names to restore. If not provided, all available objects may be restored.
            destination_client: Optional name of the destination client where the Cloud Connector package exists. If not specified, the source backup client is used.
            sf_options: Optional dictionary of restore options. Supported keys include:
                - destination_path (str): Staging path for restored Salesforce data. Defaults to the download cache path from the source if not specified.
                - dependent_level (int): Level of child objects to restore. 0 = no children, 1 = immediate children, -1 = all children. Default is 0.
                - streams (int): Number of streams to use for restore. Default is 2.
                - copy_precedence (int): Copy number to use for restore. Default is 0.
                - from_time (str): Restore contents after this date (format: dd/MM/YYYY). Defaults to 01/01/1970 if not specified.
                - to_time (str): Restore contents before this date (format: dd/MM/YYYY). Defaults to the latest if not specified.
                - show_deleted_files (bool): Whether to include deleted files in the restore. Default is True.

        Returns:
            The result of the restore operation. The return type may vary depending on the implementation.

        Raises:
            SDKException: If any of the following conditions occur:
                - The 'from_time' value is incorrect.
                - The 'to_time' value is incorrect.
                - 'to_time' is earlier than 'from_time'.
                - Failed to browse content.
                - The response is empty or not successful.
                - The destination client does not exist on the Commcell.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> restore_options = {
            ...     "destination_path": "/tmp/sf_restore",
            ...     "dependent_level": 1,
            ...     "streams": 4,
            ...     "from_time": "01/01/2023",
            ...     "to_time": "31/01/2023",
            ...     "show_deleted_files": False
            ... }
            >>> result = subclient.restore_to_file_system(
            ...     objects_to_restore=["Account", "Contact"],
            ...     destination_client="client01",
            ...     sf_options=restore_options
            ... )
            >>> print("Restore result:", result)

        #ai-gen-doc
        """

        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._instance_object.proxy_client

        if isinstance(destination_client, Client):
            client = destination_client
        elif isinstance(destination_client, str):
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
            objects_to_restore_list = [objects_to_restore]

        file_restore_option["paths"] = []
        browse_files, _ = self.browse(
            path='/Objects',
            from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0)
        )

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["paths"].append(
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
            objects_to_restore: Optional[List[str]] = None,
            destination_client: Optional[str] = None,
            sf_options: Optional[Dict[str, Any]] = None
    ) -> None:
        """Perform a Salesforce restore operation to a database.

        This method restores specified Salesforce objects to a target database using the provided options.
        The destination client must have the Cloud Connector package installed. If not specified, the source
        backup client is used by default. Database connection and restore options are provided via the
        `sf_options` dictionary.

        Args:
            objects_to_restore: Optional list of Salesforce object names to restore. If not provided, all available objects may be restored.
            destination_client: Optional name of the destination client where the Cloud Connector package exists. If not provided, the source backup client is used.
            sf_options: Optional dictionary of Salesforce restore options, which may include:
                - destination_path (str): Staging path for Salesforce restore data. Defaults to the source's download cache path if not specified.
                - db_type (str): Database type (e.g., "SQLSERVER"). Defaults to "SQLSERVER".
                - db_host_name (str): Database hostname (e.g., "dbhost.company.com").
                - db_instance (str): Database instance name (if applicable).
                - db_name (str): Name of the target database for import.
                - db_port (str): Database connection port. Defaults to "1433".
                - db_user_name (str): Database username with read/write permissions.
                - db_user_password (str): Database user password.
                - overrirde_table (bool): Whether to override tables in the database. Defaults to True.
                - dependent_level (int): Level of dependent object restore (0: no children, 1: immediate children, -1: all children). Defaults to 0.
                - streams (int): Number of streams to use for restore. Defaults to 2.
                - copy_precedence (int): Copy number to use for restore. Defaults to 0.
                - from_date (str): Restore contents after this date (format: "dd/MM/YYYY"). Defaults to "01/01/1970" if not specified.
                - to_date (str): Restore contents before this date (format: "dd/MM/YYYY"). Defaults to current day if not specified.
                - show_deleted_files (bool): Whether to include deleted files in the restore. Defaults to True.

        Raises:
            SDKException: If any of the following conditions occur:
                - The from_date value is incorrect.
                - The to_date value is incorrect.
                - The to_date is earlier than from_date.
                - Failed to browse content.
                - The response is empty or not successful.
                - The destination client does not exist on the Commcell.
                - Not all required database details are provided.

        Example:
            >>> sf_subclient = SalesforceSubclient()
            >>> restore_options = {
            ...     "db_type": "SQLSERVER",
            ...     "db_host_name": "dbhost.company.com",
            ...     "db_name": "SalesforceRestoreDB",
            ...     "db_user_name": "dbadmin",
            ...     "db_user_password": "password123",
            ...     "overrirde_table": True,
            ...     "streams": 4
            ... }
            >>> sf_subclient.restore_to_database(
            ...     objects_to_restore=["Account", "Contact"],
            ...     destination_client="Client01",
            ...     sf_options=restore_options
            ... )
            >>> print("Restore to database initiated successfully.")

        #ai-gen-doc
        """
        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._instance_object.proxy_client

        if isinstance(destination_client, Client):
            dest_client = destination_client
        elif isinstance(destination_client, str):
            dest_client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        if not ('db_host_name' in sf_options and
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
            objects_to_restore_list = [objects_to_restore]

        file_restore_option["paths"] = []
        browse_files, _ = self.browse(
            path='/Objects',
            from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0)
        )

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["paths"].append(
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
        file_restore_option["db_host_name"] = sf_options.get("db_host_name", "")
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
            objects_to_restore: Optional[List[str]] = None,
            destination_client: Optional[str] = None,
            destination_instance: Optional[str] = None,
            destination_backupset: Optional[str] = None,
            sf_options: Optional[Dict[str, Any]] = None
    ) -> None:
        """Perform a restore operation to Salesforce from a database backup.

        This method restores specified Salesforce objects from a database backup to a Salesforce environment.
        You can specify the objects to restore, the destination client, instance, and backupset, as well as
        various Salesforce and database options via the `sf_options` dictionary.

        Args:
            objects_to_restore: Optional list of Salesforce object names to restore. If not provided, all available objects may be restored.
            destination_client: Optional name of the destination pseudo client. If not specified, the source client is used.
            destination_instance: Optional name of the destination instance. If not specified, the source instance is used.
            destination_backupset: Optional name of the destination backupset. If not specified, the source backupset is used.
            sf_options: Optional dictionary of Salesforce and database restore options. Supported keys include:
                - destination_path (str): Staging path for Salesforce restore data.
                - db_type (str): Database type (default: "SQLSERVER").
                - db_host_name (str): Database hostname (e.g., "dbhost.company.com").
                - db_instance (str): Database instance name (if applicable).
                - db_name (str): Database name where data will be imported.
                - db_port (str): Database connection port (default: "1433").
                - db_user_name (str): Database username (requires read/write permissions).
                - db_user_password (str): Database user password.
                - overrirde_table (bool): Whether to override tables in the database (default: True).
                - dependent_level (int): Restore children based on selected level (0: none, 1: immediate, -1: all; default: 0).
                - streams (int): Number of streams to use for restore (default: 2).
                - copy_precedence (int): Copy number to use for restore (default: 0).
                - from_time (str): Restore contents after this date ("dd/MM/YYYY"; default: None).
                - to_time (str): Restore contents before this date ("dd/MM/YYYY"; default: None).
                - show_deleted_files (bool): Include deleted files in the restore (default: True).

        Raises:
            SDKException: If any of the following conditions occur:
                - The from date value is incorrect.
                - The to date value is incorrect.
                - The to date is earlier than the from date.
                - Failed to browse content.
                - The response is empty or not successful.
                - The destination client, instance, or backupset does not exist.
                - SyncDB is not enabled and database details are not provided.

        Example:
            >>> sf_subclient = SalesforceSubclient()
            >>> sf_subclient.restore_to_salesforce_from_database(
            ...     objects_to_restore=['Account', 'Contact'],
            ...     destination_client='SalesforceClient01',
            ...     destination_instance='SF_Instance1',
            ...     destination_backupset='SF_Backupset1',
            ...     sf_options={
            ...         'destination_path': '/tmp/sf_restore',
            ...         'db_type': 'SQLSERVER',
            ...         'db_host_name': 'dbhost.company.com',
            ...         'db_name': 'salesforce_db',
            ...         'db_user_name': 'dbuser',
            ...         'db_user_password': 'password',
            ...         'overrirde_table': True,
            ...         'dependent_level': 1,
            ...         'streams': 4,
            ...         'from_time': '01/01/2023',
            ...         'to_time': '31/01/2023',
            ...         'show_deleted_files': False
            ...     }
            ... )
            >>> print("Restore to Salesforce from database initiated successfully.")

        #ai-gen-doc
        """
        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._agent_object._client_object

        if isinstance(destination_client, Client):
            dest_client = destination_client
        elif isinstance(destination_client, str):
            dest_client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        dest_agent = Agent(dest_client, 'Cloud Apps', '134')

        # check if instance name is correct
        if destination_instance is None:
            destination_instance = self._backupset_object._instance_object

        if isinstance(destination_instance, Instance):
            dest_instance = destination_instance
        elif isinstance(destination_instance, str):
            dest_instance = dest_agent.instances.get(destination_instance)
        else:
            raise SDKException('Subclient', '113')

        # check if backupset name is correct
        if destination_backupset is None:
            destination_backupset = self._backupset_object

        if isinstance(destination_backupset, SalesforceBackupset):
            dest_backupset = destination_backupset
        elif isinstance(destination_backupset, str):
            dest_backupset = SalesforceBackupset(dest_instance, destination_backupset)
        else:
            raise SDKException('Subclient', '114')

        if not self._backupset_object.is_sync_db_enabled:
            if not (
                    'db_host_name' in sf_options and 'db_instance' in sf_options and
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
            objects_to_restore_list = [objects_to_restore]

        file_restore_option["paths"] = []
        browse_files, _ = self.browse(
            path='/Objects', from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0))

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["paths"].append(
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
        if self._backupset_object.is_sync_db_enabled or ('db_host_name' in sf_options):
            if self._backupset_object.sync_db_type is None:
                dbtype = 'SQLSERVER'
            else:
                dbtype = self._backupset_object.sync_db_type
            file_restore_option["db_type"] = sf_options.get("db_type", dbtype)
            file_restore_option["db_host_name"] = sf_options.get(
                "db_host_name", self._backupset_object.sync_db_host
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
            objects_to_restore: Optional[str] = None,
            destination_client: Optional[str] = None,
            destination_instance: Optional[str] = None,
            destination_backupset: Optional[str] = None,
            sf_options: Optional[dict] = None
    ) -> None:
        """Perform a restore operation to Salesforce from media.

        This method restores specified Salesforce objects from backup media to a Salesforce environment.
        You can specify the destination client, instance, and backupset, or allow the system to use the source values by default.
        Additional Salesforce restore options can be provided via the `sf_options` dictionary.

        Args:
            objects_to_restore: A string representing the list of Salesforce objects to restore.
            destination_client: The name of the destination pseudo client. If not provided, the source client is used.
            destination_instance: The name of the destination instance. If not provided, the source instance is used.
            destination_backupset: The name of the destination backupset. If not provided, the source backupset is used.
            sf_options: A dictionary of Salesforce restore options, which may include:
                - destination_path (str): Staging path for Salesforce restore data.
                - db_type (str): Database type (default: 'SQLSERVER').
                - db_host_name (str): Database hostname (e.g., 'dbhost.company.com').
                - db_instance (str): Database instance name.
                - db_name (str): Database name for data import.
                - db_port (str): Database connection port (default: '1433').
                - db_user_name (str): Database username (requires read/write permissions).
                - db_user_password (str): Database user password.
                - overrirde_table (bool): Whether to override tables in the database (default: True).
                - dependent_level (int): Restore children based on level (0: none, 1: immediate, -1: all; default: 0).
                - streams (int): Number of streams to use for restore (default: 2).
                - copy_precedence (int): Copy number to use for restore (default: 0).
                - from_time (str): Restore contents after this date (format: 'dd/MM/YYYY'; default: None).
                - to_time (str): Restore contents before this date (format: 'dd/MM/YYYY'; default: None).
                - show_deleted_files (bool): Include deleted files in the restore (default: True).

        Raises:
            SDKException: If any of the following conditions occur:
                - The 'from_time' value is incorrect.
                - The 'to_time' value is incorrect.
                - The 'to_time' is earlier than 'from_time'.
                - Failed to browse content.
                - The response is empty or not successful.
                - The destination client, instance, or backupset does not exist.
                - Staging database details are not provided.

        Example:
            >>> sf_subclient = SalesforceSubclient()
            >>> sf_subclient.restore_to_salesforce_from_media(
            ...     objects_to_restore="Account,Contact",
            ...     destination_client="SalesforceClient01",
            ...     destination_instance="SalesforceInstance01",
            ...     destination_backupset="SalesforceBackupset01",
            ...     sf_options={
            ...         "destination_path": "/tmp/sf_restore",
            ...         "db_type": "SQLSERVER",
            ...         "db_host_name": "dbhost.company.com",
            ...         "db_name": "salesforce_db",
            ...         "db_user_name": "dbuser",
            ...         "db_user_password": "password",
            ...         "overrirde_table": True,
            ...         "dependent_level": 0,
            ...         "streams": 2,
            ...         "copy_precedence": 0,
            ...         "from_time": "01/01/2023",
            ...         "to_time": "31/12/2023",
            ...         "show_deleted_files": True
            ...     }
            ... )
            >>> print("Restore to Salesforce from media initiated successfully.")

        #ai-gen-doc
        """

        file_restore_option = {}

        if sf_options is None:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._agent_object._client_object

        if isinstance(destination_client, Client):
            dest_client = destination_client
        elif isinstance(destination_client, str):
            dest_client = Client(self._commcell_object, destination_client)
        else:
            raise SDKException('Subclient', '105')

        dest_agent = Agent(dest_client, 'Cloud Apps')

        # check if instance name is correct
        if destination_instance is None:
            destination_instance = self._backupset_object._instance_object

        if isinstance(destination_instance, Instance):
            dest_instance = destination_instance
        elif isinstance(destination_instance, str):
            dest_instance = dest_agent.instances.get(destination_instance)
        else:
            raise SDKException('Subclient', '113')

        # check if backupset name is correct
        if destination_backupset is None:
            destination_backupset = self._backupset_object

        if isinstance(destination_backupset, SalesforceBackupset):
            dest_backupset = destination_backupset
        elif isinstance(destination_backupset, str):
            dest_backupset = SalesforceBackupset(dest_instance, destination_backupset)
        else:
            raise SDKException('Subclient', '114')

        if not ('db_host_name' in sf_options and
                'db_instance' in sf_options and
                'db_name' in sf_options and
                'db_user_name' in sf_options and
                'db_user_password' in sf_options):
            raise SDKException('Salesforce', '101')

        file_restore_option["dest_client_name"] = dest_client.client_name
        file_restore_option["dest_instance_name"] = dest_instance.instance_name
        file_restore_option["dest_backupset_name"] = dest_backupset.backupset_name

        self._restore_salesforce_destination_json(file_restore_option)

        # process the objects to restore
        if isinstance(objects_to_restore, list):
            objects_to_restore_list = objects_to_restore

        else:
            objects_to_restore_list = [objects_to_restore]

        file_restore_option["paths"] = []
        browse_files, _ = self.browse(
            path='/Objects',
            from_time=sf_options.get("from_time", 0),
            to_time=sf_options.get("to_time", 0)
        )

        for each_object in objects_to_restore_list:
            if each_object.find('/Files') < 0:
                file_restore_option["paths"].append(
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
        file_restore_option["db_host_name"] = sf_options.get("db_host_name", "")
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

    def metadata_restore_to_salesforce(
            self,
            metadata_list: Optional[list] = None,
            destination_client: Optional[str] = None,
            destination_instance: Optional[str] = None,
            destination_backupset: Optional[str] = None,
            **sf_options: object
    ) -> None:
        """Perform a metadata restore to Salesforce from backup media.

        This method restores specified Salesforce metadata components from backup media to a Salesforce environment.
        You can specify the destination client, instance, and backupset, or allow the system to use the source values.
        Additional Salesforce restore options can be provided as keyword arguments.

        Args:
            metadata_list: Optional list of metadata component paths to restore (e.g., ["folder/component.type"]).
            destination_client: Optional name of the destination pseudo client. If not provided, the source client is used.
            destination_instance: Optional name of the destination instance. If not provided, the source instance is used.
            destination_backupset: Optional name of the destination backupset. If not provided, the source backupset is used.
            **sf_options: Additional Salesforce restore options, such as:
                - destination_path (str): Staging path for Salesforce restore data.
                - streams (int): Number of streams to use for restore (default: 2).
                - copy_precedence (int): Copy number to use for restore (default: 0).
                - from_time (str): Restore contents after this date (format: dd/MM/YYYY, default: 01/01/1970).
                - to_time (str): Restore contents before this date (format: dd/MM/YYYY, default: current day).
                - show_deleted_files (bool): Whether to include deleted files in the restore (default: True).

        Raises:
            SDKException: If any of the following conditions occur:
                - The from date value is incorrect.
                - The to date value is incorrect.
                - The to date is earlier than the from date.
                - Failed to browse content.
                - The response is empty or not successful.
                - The destination client, instance, or backupset does not exist.

        Example:
            >>> subclient = SalesforceSubclient()
            >>> subclient.metadata_restore_to_salesforce(
            ...     metadata_list=["src/Account.object", "src/Contact.object"],
            ...     destination_client="SalesforceClient01",
            ...     destination_instance="InstanceA",
            ...     destination_backupset="Backupset1",
            ...     destination_path="/tmp/sf_restore",
            ...     streams=4,
            ...     from_time="01/01/2023",
            ...     to_time="31/01/2023",
            ...     show_deleted_files=False
            ... )
            >>> print("Metadata restore initiated successfully.")

        #ai-gen-doc
        """

        file_restore_option = {}

        if not sf_options:
            sf_options = {}

        # check if client name is correct
        if destination_client is None:
            destination_client = self._backupset_object._agent_object._client_object

        if isinstance(destination_client, Client):
            dest_client = destination_client
        elif isinstance(destination_client, str):
            dest_client = self._commcell_object.clients.get(destination_client)
        else:
            raise SDKException('Subclient', '105')

        dest_agent = Agent(dest_client, 'Cloud Apps')

        # check if instance name is correct
        if destination_instance is None:
            destination_instance = self._backupset_object._instance_object

        if isinstance(destination_instance, Instance):
            dest_instance = destination_instance
        elif isinstance(destination_instance, str):
            dest_instance = dest_agent.instances.get(destination_instance)
        else:
            raise SDKException('Subclient', '113')

        # check if backupset name is correct
        if destination_backupset is None:
            destination_backupset = self._backupset_object

        if isinstance(destination_backupset, SalesforceBackupset):
            dest_backupset = destination_backupset
        elif isinstance(destination_backupset, str):
            dest_backupset = SalesforceBackupset(dest_instance, destination_backupset)
        else:
            raise SDKException('Subclient', '114')

        file_restore_option["dest_client_name"] = dest_client.client_name
        file_restore_option["dest_instance_name"] = dest_instance.instance_name
        file_restore_option["dest_backupset_name"] = dest_backupset.backupset_name

        self._restore_salesforce_destination_json(file_restore_option)

        file_restore_option["paths"] = [f"/Metadata/unpackaged/{metadata_path}" for metadata_path in metadata_list]

        # set the salesforce options
        file_restore_option["staging_path"] = sf_options.get(
            "destination_path", dest_backupset.download_cache_path
        )
        file_restore_option["dependent_level"] = sf_options.get("dependent_level", 0)
        file_restore_option["streams"] = sf_options.get("streams", 2)
        file_restore_option["to_fs"] = False
        file_restore_option["to_cloud"] = True
        file_restore_option["from_database"] = False
        file_restore_option["is_metadata"] = True

        # set the browse option
        file_restore_option["client_name"] = self._backupset_object._agent_object._client_object.client_name
        file_restore_option["copy_precedence_applicable"] = True
        file_restore_option["copy_precedence"] = sf_options.get("copy_precedence", 0)
        file_restore_option["from_time"] = sf_options.get("from_time", 0)
        file_restore_option["to_time"] = sf_options.get("to_time", 0)

        # prepare and execute the Json
        request_json = self._prepare_salesforce_restore_json(file_restore_option)

        return self._process_restore_response(request_json)

    def _prepare_salesforce_restore_json(self, file_restore_option: dict) -> dict:
        """Prepare the Salesforce restore JSON payload using the provided file restore options.

        This method constructs a JSON dictionary required for initiating a Salesforce restore operation,
        based on the options specified in the `file_restore_option` parameter.

        Args:
            file_restore_option: A dictionary containing options and parameters for the Salesforce file restore.

        Returns:
            A dictionary representing the Salesforce restore JSON payload.

        Example:
            >>> restore_options = {
            ...     "object_name": "Account",
            ...     "restore_type": "Full",
            ...     "target_org": "TargetOrgName"
            ... }
            >>> payload = subclient._prepare_salesforce_restore_json(restore_options)
            >>> print(payload)
            {'object_name': 'Account', 'restore_type': 'Full', 'target_org': 'TargetOrgName'}

        #ai-gen-doc
        """
        self._restore_fileoption_json(file_restore_option)
        self._restore_salesforce_options_json(file_restore_option)
        self._restore_browse_option_json(file_restore_option)
        self._impersonation_json(file_restore_option)
        self._restore_common_options_json(file_restore_option)

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
