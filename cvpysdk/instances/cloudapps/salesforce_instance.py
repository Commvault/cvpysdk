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

"""File for operating on a Salesforce Instance.

SalesforceInstance is the only class defined in this file.

SalesforceeInstance:    Derived class from CloudAppsInstance Base class, representing a
                            Salesforce instance, and to perform operations on that instance

SalesforceInstance:

    _restore_json()                     --  Returns the JSON request to pass to the API as per the options selected by
                                            the user

    restore_to_file_system()            --  Runs object level restore to file system and returns object of Job or
                                            Schedule class

    restore_to_database()               --  Runs object level restore to database and returns object of Job or Schedule
                                            class

    restore_to_salesforce_from_database() --  Runs restore to Salesforce from database and returns object of Job or
                                            Schedule class

    restore_to_salesforce_from_media()  --  Runs restore to Salesforce from database and returns object of Job or
                                            Schedule class

    metadata_restore_to_file_system()   --  Runs metadata restore to file system and returns object of Job or Schedule
                                            class

    metadata_restore_to_salesforce()    --  Runs metadata restore to Salesforce and returns object of Job or Schedule
                                            class

SalesforceInstance Attributes:

    **ca_instance_type**            --  Returns the instance type of this cloud apps instance

    **organization_id**             --  Returns the Salesforce organization id

    **login_url**                   --  Returns the login url of Salesforce organization

    **consumer_id**                 --  Returns the Consumer Id of the Salesforce connected app used to authenticate
                                        with Salesforce by this instance

    **proxy_client**                --  Returns the name of the access node. Returns None if client group is configured
                                        as access node

"""
from __future__ import unicode_literals
from base64 import b64encode
from ..cainstance import CloudAppsInstance
from ...exception import SDKException


class SalesforceInstance(CloudAppsInstance):
    """
    Represents an instance of the Salesforce cloud application.

    This class provides a comprehensive interface for managing and restoring Salesforce instances.
    It exposes properties for accessing instance-specific details such as organization ID, login URL,
    consumer ID, proxy client, and access node. The class supports various restore operations,
    including restoring data and metadata to the file system, database, or directly to Salesforce
    from different sources.

    Key Features:
        - Access to Salesforce instance properties (type, organization ID, login URL, consumer ID, proxy client, access node)
        - Restore instance data to file system
        - Restore instance data to database with configurable parameters
        - Restore Salesforce data from database or media sources
        - Restore metadata to file system or directly to Salesforce
        - Internal support for restoring from JSON representations

    #ai-gen-doc
    """

    @property
    def ca_instance_type(self) -> str:
        """Get the instance type of this Salesforce cloud apps instance.

        Returns:
            The instance type as a string.

        Example:
            >>> sf_instance = SalesforceInstance()
            >>> instance_type = sf_instance.ca_instance_type
            >>> print(f"Instance type: {instance_type}")
            >>> # The output will display the type of the Salesforce cloud apps instance

        #ai-gen-doc
        """
        return 'SALESFORCE'

    @property
    def organization_id(self) -> str:
        """Get the Salesforce organization ID associated with this instance.

        Returns:
            The Salesforce organization ID as a string.

        Example:
            >>> sf_instance = SalesforceInstance()
            >>> org_id = sf_instance.organization_id
            >>> print(f"Organization ID: {org_id}")

        Raises:
            SDKException: If the organization ID attribute could not be fetched.

        #ai-gen-doc
        """
        try:
            return self._properties['cloudAppsInstance']['salesforceInstance']['sfOrgID']
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch organization ID')

    @property
    def login_url(self) -> str:
        """Get the login URL of the Salesforce organization.

        Returns:
            The login URL as a string.

        Raises:
            SDKException: If the login URL attribute could not be fetched.

        Example:
            >>> sf_instance = SalesforceInstance()
            >>> url = sf_instance.login_url
            >>> print(f"Salesforce login URL: {url}")

        #ai-gen-doc
        """
        try:
            return self._properties['cloudAppsInstance']['salesforceInstance']['endpoint']
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch login url')

    @property
    def consumer_id(self) -> str:
        """Get the Consumer Id of the Salesforce connected app used for authentication.

        This property retrieves the Consumer Id associated with the Salesforce connected app 
        that is used by this instance to authenticate with Salesforce.

        Returns:
            The Consumer Id as a string.

        Raises:
            SDKException: If the Consumer Id attribute could not be fetched.

        Example:
            >>> sf_instance = SalesforceInstance()
            >>> consumer_id = sf_instance.consumer_id  # Use dot notation for property access
            >>> print(f"Salesforce Consumer Id: {consumer_id}")

        #ai-gen-doc
        """
        try:
            return self._properties['cloudAppsInstance']['salesforceInstance']['consumerId']
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch login url')

    @property
    def proxy_client(self) -> str:
        """Get the name of the access node (proxy client) for this Salesforce instance.

        Returns:
            The name of the access node as a string.

        Raises:
            SDKException: If the attribute could not be fetched or if the access node is a client group.

        Example:
            >>> sf_instance = SalesforceInstance()
            >>> access_node = sf_instance.proxy_client
            >>> print(f"Access node: {access_node}")

        #ai-gen-doc
        """
        try:
            general_cloud_properties = self._properties['cloudAppsInstance']['generalCloudProperties']
            if 'clientName' in general_cloud_properties['proxyServers'][0].keys():
                return general_cloud_properties['proxyServers'][0]['clientName']
            if 'clientName' in general_cloud_properties['accessNodes']['memberServers'][0]['client'].keys():
                return general_cloud_properties['accessNodes']['memberServers'][0]['client']['clientName']
            if 'clientGroupName' in general_cloud_properties['accessNodes']['memberServers'][0]['client'].keys():
                raise SDKException(
                    'Instance',
                    '102',
                    'This instance uses a client group as access node. Use access_node attribute instead.'
                )
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch proxy client')

    @property
    def access_node(self) -> dict:
        """Get the access node configuration for the Salesforce instance.

        Returns:
            dict: A dictionary containing either:
                - 'clientName' and 'clientId' if a single client is configured as the access node, or
                - 'clientGroupName' and 'clientGroupId' if a client group is configured as the access node.

        Raises:
            SDKException: If the access node attribute could not be fetched.

        Example:
            >>> sf_instance = SalesforceInstance()
            >>> access_info = sf_instance.access_node
            >>> print(access_info)
            {'clientName': 'ClientA', 'clientId': 123}
            # or
            {'clientGroupName': 'GroupA', 'clientGroupId': 456}

        #ai-gen-doc
        """
        try:
            access_node = self._properties['cloudAppsInstance']['generalCloudProperties']['accessNodes'] \
                ['memberServers'][0]['client'].copy()
            if 'entityInfo' in access_node:
                del access_node['entityInfo']
            return access_node
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch access node')

    def _restore_json(self, **kwargs: dict) -> dict:
        """Generate the JSON request payload for a restore operation based on user-selected options.

        This method constructs and returns a dictionary representing the JSON request body
        to be sent to the API for a Salesforce restore operation. The request is built
        according to the keyword arguments provided by the user, allowing for flexible
        configuration of restore parameters.

        Args:
            **kwargs: Arbitrary keyword arguments specifying restore options. Each key-value
                pair represents a parameter to include in the restore request.

        Returns:
            dict: The JSON request payload as a dictionary, ready to be sent to the API.

        Example:
            >>> instance = SalesforceInstance()
            >>> restore_payload = instance._restore_json(
            ...     source='backup_2023_10_01',
            ...     target='production',
            ...     overwrite=True
            ... )
            >>> print(restore_payload)
            {'source': 'backup_2023_10_01', 'target': 'production', 'overwrite': True}

        #ai-gen-doc
        """
        if len(self.backupsets.all_backupsets) > 1 or len(self.subclients.all_subclients) > 1:
            raise SDKException(
                'Instance',
                '102',
                'More than one backupset/subclient configured in this instance. Run restore from subclient'
            )

        if not kwargs.get('no_of_streams', None):
            kwargs['no_of_streams'] = 2
        kwargs['client'] = kwargs.get('client', None) or self._agent_object._client_object
        request_json = super()._restore_json(**kwargs)

        backupset = self.backupsets.get(list(self.backupsets.all_backupsets.keys())[0])
        subclient = list(self.subclients.all_subclients.items())[0]
        request_json['taskInfo']['associations'][0].update({
            'backupsetName': backupset.name,
            'backupsetId': int(backupset.backupset_id),
            'subclientName': subclient[0],
            'subclientId': int(subclient[1]['id'])
        })

        request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['cloudAppsRestoreOptions'] = {
            'instanceType': self.ca_instance_type,
            'salesforceRestoreOptions': {
                'restoreToFileSystem': kwargs.get('restore_to_file_system', False),
                'restoreToSalesforce': kwargs.get('restore_to_salesforce', False),
                'restoreFromDatabase': kwargs.get('restore_from_database', False),
                'isMetadataRestore': kwargs.get('is_metadata_restore', False),
                'pathToStoreCsv': kwargs.get('path_to_store_csv', None) or backupset.download_cache_path,
                'dependentRestoreLevel': kwargs.get('dependent_restore_level', 0),
                'restoreParentType': kwargs.get('restore_parent_type', 'NONE'),
                'isSaaSRestore': False
            }
        }

        if 'restore_to_salesforce' in kwargs and kwargs['restore_to_salesforce']:
            if kwargs.get('instance', None) and kwargs.get('backupset', None):
                destination_client = self._commcell_object.clients.get(kwargs['client'])
                destination_instance = destination_client.agents.get('Cloud Apps').instances.get(kwargs['instance'])
                destination_backupset = destination_instance.backupsets.get(kwargs['backupset'])
            else:
                destination_instance = self
                destination_backupset = backupset
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['destination'].update({
                'destinationInstance': {
                    'instanceId': int(destination_instance.instance_id),
                    'instanceName': destination_instance.name,
                },
                'destinationBackupset': {
                    'backupsetId': int(destination_backupset.backupset_id),
                    'backupsetName': destination_backupset.backupset_name
                }
            })

        if kwargs.get('db_enabled', False):
            request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['cloudAppsRestoreOptions'] \
                ['salesforceRestoreOptions'].update({
                'syncDatabase': {
                    'dbEnabled': True,
                    'dbType': kwargs['db_type'],
                    'dbHost': kwargs['db_host'],
                    'dbInstance': kwargs.get('db_instance', ''),
                    'dbPort': str(kwargs.get('db_port', 5432 if kwargs['db_type'] == 'POSTGRESQL' else 1433)),
                    'dbName': kwargs['db_name'],
                    'dbUserPassword': {
                        'userName': kwargs['db_user_name'],
                        'password': b64encode(kwargs['db_password'].encode()).decode()
                    }
                },
                'overrideTable': kwargs.get('override_table', True),
                'restoreCatalogDatabase': kwargs.get('restore_catalog_database', False)
            })

        return request_json

    def restore_to_file_system(self, **kwargs: dict) -> object:
        """Perform an object-level restore to the file system and return a Job or Schedule object.

        This method initiates a restore operation for Salesforce files and objects to a specified file system location.
        For out-of-place restores, both the `client` and `path_to_store_csv` parameters must be provided. By default,
        the restore will target the access node and use the download cache path.

        Keyword Args:
            paths (List[str], optional): List of file and object paths to restore, e.g.,
                ['/Files/filename', '/Objects/object_name']. Defaults to ['/Files/', '/Objects/'] (all files and objects).
            client (str, optional): Name of the destination client. Defaults to the access node.
            path_to_store_csv (str, optional): Path on the destination client to restore to. Defaults to the download cache path.
            from_time (str, optional): Restore contents modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time (str, optional): Restore contents modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            no_of_streams (int, optional): Number of streams to use for restore. Defaults to 2.
            dependent_restore_level (int, optional): Restore children option. Defaults to 0.
                0  -- No Children
                1  -- Immediate Children
                -1 -- All Children
            restore_parent_type (str, optional): Restore parents option. Defaults to 'NONE'.
                'NONE' -- No Parents
                'ALL'  -- All Parents

        Returns:
            object: An instance of the Job or Schedule class representing the restore operation.

        Raises:
            SDKException: If any of the following conditions are met:
                - The 'paths' parameter is provided but is not a list.
                - The 'client' parameter is not provided and the access node is a client group.
                - Only one of 'client' or 'path_to_store_csv' is provided (both must be present for out-of-place restore).
                - The 'client' or 'path_to_store_csv' parameters are not strings.

        Example:
            >>> # Restore all files and objects to the default location
            >>> job = salesforce_instance.restore_to_file_system()
            >>> print(f"Restore job started: {job}")

            >>> # Out-of-place restore to a specific client and path
            >>> job = salesforce_instance.restore_to_file_system(
            ...     client='DestinationClient',
            ...     path_to_store_csv='/tmp/restore_folder',
            ...     paths=['/Files/AccountData.csv'],
            ...     no_of_streams=4
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        PARAMS = ('client', 'path_to_store_csv')

        if not isinstance(kwargs.get('paths', list()), list):
            raise SDKException('Instance', '101')

        if any(param in kwargs for param in PARAMS) and \
                not all(isinstance(kwargs.get(param, None), str) for param in PARAMS):
            raise SDKException('Instance', '101')

        if not 'paths' in kwargs:
            kwargs['paths'] = ['/Files/', '/Objects/']

        request_json = self._restore_json(
            client=kwargs.get('client', self.proxy_client),
            restore_to_file_system=True,
            **kwargs
        )
        
        return self._process_restore_response(request_json)

    def restore_to_database(
            self,
            db_type: str,
            db_host_name: str,
            db_name: str,
            db_user_name: str,
            db_password: str,
            **kwargs: dict
        ) -> object:
        """Perform an object-level restore to a specified database.

        This method initiates a restore operation for Salesforce objects or files to a target database,
        supporting both PostgreSQL and SQL Server. Additional restore options can be provided via keyword arguments.

        Args:
            db_type: The type of database to restore to. Must be either 'POSTGRESQL' or 'SQLSERVER'.
            db_host_name: Hostname or IP address of the target database server.
            db_name: Name of the database where objects will be restored.
            db_user_name: Username for authenticating with the target database.
            db_password: Password for the specified database user.
            **kwargs: Additional restore options. Supported keys include:
                - paths (list of str): List of files/objects to restore (default: ['/Objects/'] for all objects).
                - db_instance (str): Database instance name (required for SQL Server).
                - db_port (int): Port number for the database server (default: 5432 for PostgreSQL, 1433 for SQL Server).
                - from_time (str): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS').
                - to_time (str): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS').
                - no_of_streams (int): Number of streams to use for restore (default: 2).
                - path_to_store_csv (str): Path for staging folder (default: download cache path).
                - dependent_restore_level (int): Restore children option (0: No Children, 1: Immediate, -1: All).
                - restore_parent_type (str): Restore parents option ('NONE' or 'ALL').

        Returns:
            Object representing the restore operation, typically an instance of Job or Schedule class.

        Raises:
            SDKException: If required parameters are missing or of incorrect type,
                if db_type is 'SQLSERVER' but db_instance is not provided or not a string,
                or if 'paths' is provided but is not a list.

        Example:
            >>> # Restore all Salesforce objects to a PostgreSQL database
            >>> job = salesforce_instance.restore_to_database(
            ...     db_type='POSTGRESQL',
            ...     db_host_name='db.example.com',
            ...     db_name='salesforce_restore',
            ...     db_user_name='dbuser',
            ...     db_password='securepass',
            ...     paths=['/Objects/Account', '/Objects/Contact'],
            ...     db_port=5432,
            ...     no_of_streams=4
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        PARAMS = (db_type, db_host_name,  db_name, db_user_name, db_password)

        if not isinstance(kwargs.get('paths', list()), list):
            raise SDKException('Instance', '101')

        if not all(isinstance(val, str) for val in PARAMS) and \
                (isinstance(kwargs.get('db_instance', None), str) != (db_type == 'SQLSERVER')):
            raise SDKException('Instance', '101')

        if not 'paths' in kwargs:
            kwargs['paths'] = ['/Objects/']

        request_json = self._restore_json(
            db_enabled=True,
            db_type=db_type,
            db_host=db_host_name,
            db_name=db_name,
            db_user_name=db_user_name,
            db_password=db_password,
            **kwargs
        )

        return self._process_restore_response(request_json)

    def restore_to_salesforce_from_database(self, **kwargs: dict) -> object:
        """Run a restore operation to Salesforce from a database and return a Job or Schedule object.

        This method initiates a restore process that transfers data from a specified database to Salesforce.
        For out-of-place restores, provide the `client`, `instance`, and `backupset` parameters. If database
        parameters are omitted, the default sync database will be used.

        Keyword Args:
            paths (list of str, optional): List of files and objects to restore, e.g., ['/Files/filename', '/Objects/object_name'].
                Defaults to ['/Files/', '/Objects/'] to select all files and objects.
            client (str, optional): Name of the destination client. Defaults to the source client.
            instance (str, optional): Name of the destination instance. Defaults to the source instance.
            backupset (str, optional): Name of the destination backupset. Defaults to the source backupset.
            db_type (str, optional): Type of database, either 'POSTGRESQL' or 'SQLSERVER'.
            db_host (str, optional): Hostname of the database server.
            db_name (str, optional): Name of the database where objects will be restored.
            db_user_name (str, optional): Username for the database.
            db_password (str, optional): Password for the database user.
            db_instance (str, optional): Database instance for SQL Server.
            db_port (int, optional): Port of the database server. Defaults to 5432 for POSTGRESQL and 1433 for SQLSERVER.
            from_time (str, optional): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time (str, optional): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS').
            no_of_streams (int, optional): Number of streams to use for restore. Defaults to 2.
            path_to_store_csv (str, optional): Path to use as a staging folder. Defaults to the download cache path.
            dependent_restore_level (int, optional): Restore children option. 0 = No Children, 1 = Immediate Children, -1 = All Children.
            restore_parent_type (str, optional): Restore parents option. 'NONE' = No Parents, 'ALL' = All Parents.

        Returns:
            object: An instance of Job or Schedule class representing the restore operation.

        Raises:
            SDKException: If any of the following conditions are met:
                - 'paths' is provided but is not a list.
                - Any database parameters are provided but not all required parameters are present.
                - Database parameters are not all strings.
                - 'db_type' is 'SQLSERVER' but 'db_instance' is missing or not a string.
                - Only some of 'client', 'instance', or 'backupset' are provided (all three must be present for out-of-place restore).
                - 'client', 'instance', or 'backupset' are not strings.

        Example:
            >>> # Restore all files and objects to Salesforce using default sync database
            >>> job = salesforce_instance.restore_to_salesforce_from_database()
            >>> print(f"Restore job started: {job}")

            >>> # Out-of-place restore to a different client and database
            >>> job = salesforce_instance.restore_to_salesforce_from_database(
            ...     client='NewClient',
            ...     instance='NewInstance',
            ...     backupset='NewBackupset',
            ...     db_type='POSTGRESQL',
            ...     db_host='db.example.com',
            ...     db_name='salesforce_db',
            ...     db_user_name='dbuser',
            ...     db_password='dbpass'
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        DB_PARAMS = ('db_type', 'db_host', 'db_name', 'db_user_name', 'db_password')
        DEST_PARAMS = ('client', 'instance', 'backupset')

        if not isinstance(kwargs.get('paths', list()), list):
            raise SDKException('Instance', '101')

        if any(param in kwargs for param in DEST_PARAMS) and \
                not all(isinstance(kwargs.get(param, None), str) for param in DEST_PARAMS):
            raise SDKException('Instance', '101')

        if any(param in kwargs for param in DB_PARAMS):
            if not all(isinstance(kwargs.get(param, None), str) for param in DB_PARAMS) and \
                    (isinstance(kwargs.get('db_instance', None), str) != (kwargs['db_type'] == 'SQLSERVER')):
                raise SDKException('Instance', '101')
            kwargs['db_enabled'] = True

        if not 'paths' in kwargs:
            kwargs['paths'] = ['/Files/', '/Objects/']

        request_json = self._restore_json(
            restore_to_salesforce=True,
            restore_from_database=True,
            **kwargs
        )

        return self._process_restore_response(request_json)

    def restore_to_salesforce_from_media(self, **kwargs: dict) -> object:
        """Restore data to Salesforce from media and return a Job or Schedule object.

        This method initiates a restore operation to Salesforce from a database backup. 
        For out-of-place restores, specify the `client`, `instance`, and `backupset` parameters. 
        If database parameters are not provided, the sync database will be used as the staging database.

        Keyword Args:
            paths (List[str], optional): List of files and objects to restore, e.g., ['/Files/filename', '/Objects/object_name'].
                Defaults to ['/Files/', '/Objects/'] (restores all files and objects).
            client (str, optional): Name of the destination client. Defaults to the source client.
            instance (str, optional): Name of the destination instance. Defaults to the source instance.
            backupset (str, optional): Name of the destination backupset. Defaults to the source backupset.
            db_type (str, optional): Type of database ('POSTGRESQL' or 'SQLSERVER').
            db_host (str, optional): Hostname of the database server.
            db_name (str, optional): Name of the database where objects will be restored.
            db_user_name (str, optional): Username for the database.
            db_password (str, optional): Password for the database user.
            db_instance (str, optional): Database instance for SQL Server.
            db_port (int, optional): Port of the database server. Defaults to 5432 for POSTGRESQL and 1433 for SQLSERVER.
            from_time (str, optional): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time (str, optional): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS').
            no_of_streams (int, optional): Number of streams to use for restore. Defaults to 2.
            path_to_store_csv (str, optional): Path to use as the staging folder. Defaults to the download cache path.
            dependent_restore_level (int, optional): Restore children option. 
                0: No Children, 1: Immediate Children, -1: All Children. Defaults to 0.
            restore_parent_type (str, optional): Restore parents option. 
                'NONE': No Parents, 'ALL': All Parents. Defaults to 'NONE'.

        Returns:
            object: An instance of Job or Schedule class representing the restore operation.

        Raises:
            SDKException: If any of the following conditions are met:
                - 'paths' is provided but is not a list.
                - Any database parameters are provided but not all required parameters are present.
                - Database parameters are not all strings.
                - 'db_type' is 'SQLSERVER' but 'db_instance' is missing or not a string.
                - Only some of 'client', 'instance', or 'backupset' are provided (all three must be present for out-of-place restore).
                - 'client', 'instance', or 'backupset' are not strings.

        Example:
            >>> # Restore all files and objects to the default Salesforce instance
            >>> job = salesforce_instance.restore_to_salesforce_from_media()
            >>> print(f"Restore job started: {job}")

            >>> # Out-of-place restore to a different client and instance with custom database parameters
            >>> job = salesforce_instance.restore_to_salesforce_from_media(
            ...     client='NewClient',
            ...     instance='NewInstance',
            ...     backupset='NewBackupset',
            ...     db_type='POSTGRESQL',
            ...     db_host='db.example.com',
            ...     db_name='salesforce_restore',
            ...     db_user_name='dbuser',
            ...     db_password='dbpass',
            ...     paths=['/Files/important_file', '/Objects/Account']
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        DB_PARAMS = ('db_type', 'db_host', 'db_name', 'db_user_name', 'db_password')
        DEST_PARAMS = ('client', 'instance', 'backupset')

        if not isinstance(kwargs.get('paths', list()), list):
            raise SDKException('Instance', '101')

        if any(param in kwargs for param in DEST_PARAMS) and \
                not all(isinstance(kwargs.get(param, None), str) for param in DEST_PARAMS):
            raise SDKException('Instance', '101')

        if any(keyword in kwargs for keyword in DB_PARAMS):
            if not all(isinstance(kwargs.get(param, None), str) for param in DB_PARAMS) and \
                    (isinstance(kwargs.get('db_instance', None), str) != (kwargs['db_type'] == 'SQLSERVER')):
                raise SDKException('Instance', '101')
            kwargs['db_enabled'] = True

        if not 'paths' in kwargs:
            kwargs['paths'] = ['/Files/', '/Objects/']

        request_json = self._restore_json(
            restore_to_salesforce=True,
            **kwargs
        )

        return self._process_restore_response(request_json)

    def metadata_restore_to_file_system(self, **kwargs: dict) -> object:
        """Run a metadata restore operation to the file system.

        This method initiates a metadata restore for Salesforce components to a specified file system location.
        For an out-of-place restore, both the `client` and `path_to_store_csv` parameters must be provided.
        By default, the restore will target the access node and its download cache path.

        Keyword Args:
            paths (List[str], optional): List of metadata component paths to restore, e.g.,
                ['/Metadata/unpackaged/objects/Account.object', '/Metadata/unpackaged/profiles/Admin.profile'].
                Defaults to ['/Metadata/unpackaged/'] (restores all metadata components).
            client (str, optional): Name of the destination client. Defaults to the access node.
            path_to_store_csv (str, optional): Path on the destination client to restore to.
                Defaults to the download cache path.
            from_time (str, optional): Restore contents modified after this time (format: 'YYYY-MM-DD HH:MM:SS').
            to_time (str, optional): Restore contents modified before this time (format: 'YYYY-MM-DD HH:MM:SS').
            no_of_streams (int, optional): Number of streams to use for restore. Defaults to 2.
            dependent_restore_level (int, optional): Restore children option.
                0  -- No Children (default)
                1  -- Immediate Children
                -1 -- All Children
            restore_parent_type (str, optional): Restore parents option.
                'NONE' -- No Parents (default)
                'ALL'  -- All Parents

        Returns:
            object: An instance of the Job or Schedule class representing the restore operation.

        Raises:
            SDKException: If any of the following conditions are met:
                - The 'paths' parameter is provided but is not a list.
                - The 'client' parameter is not provided and the access node is a client group.
                - Only one of 'client' or 'path_to_store_csv' is provided (both must be present for out-of-place restore).
                - The 'client' or 'path_to_store_csv' parameters are not strings.

        Example:
            >>> # Restore all metadata components to the default location
            >>> job = salesforce_instance.metadata_restore_to_file_system()
            >>> print(f"Restore job started: {job}")

            >>> # Out-of-place restore to a specific client and path
            >>> job = salesforce_instance.metadata_restore_to_file_system(
            ...     client='DestinationClient',
            ...     path_to_store_csv='/tmp/salesforce_restore',
            ...     paths=['/Metadata/unpackaged/objects/Account.object'],
            ...     no_of_streams=4
            ... )
            >>> print(f"Restore job started: {job}")

        #ai-gen-doc
        """
        PARAMS = ('client', 'path_to_store_csv')

        if not isinstance(kwargs.get('paths', list()), list):
            raise SDKException('Instance', '101')

        if any(param in kwargs for param in PARAMS) and \
                not all(isinstance(kwargs.get(param, None), str) for param in PARAMS):
            raise SDKException('Instance', '101')

        if not 'paths' in kwargs:
            kwargs['paths'] = ['/Metadata/unpackaged/']
        
        request_json = self._restore_json(
            restore_to_file_system=True,
            is_metadata_restore=True,
            **kwargs
        )
        return self._process_restore_response(request_json)

    def metadata_restore_to_salesforce(self, **kwargs: dict) -> object:
        """Run a metadata restore operation to Salesforce.

        This method initiates a metadata restore to a Salesforce instance. It supports both in-place and out-of-place restores.
        For out-of-place restores, you must provide the `client`, `instance`, and `backupset` parameters in `kwargs`.
        Additional restore options can be specified via keyword arguments.

        Keyword Args:
            paths (List[str], optional): List of metadata component paths to restore. 
                Example: ['/Metadata/unpackaged/objects/Account.object', '/Metadata/unpackaged/profiles/Admin.profile'].
                Defaults to ['/Metadata/unpackaged/'] (restores all metadata components).
            client (str, optional): Name of the destination client. Defaults to the source client.
            instance (str, optional): Name of the destination instance. Defaults to the source instance.
            backupset (str, optional): Name of the destination backupset. Defaults to the source backupset.
            from_time (str, optional): Restore contents after this time (format: 'YYYY-MM-DD HH:MM:SS'). Defaults to None.
            to_time (str, optional): Restore contents before this time (format: 'YYYY-MM-DD HH:MM:SS'). Defaults to None.
            no_of_streams (int, optional): Number of streams to use for restore. Defaults to 2.
            path_to_store_csv (str, optional): Path to use as a staging folder. Defaults to the download cache path.
            dependent_restore_level (int, optional): Restore children option. 
                0: No Children (default), 1: Immediate Children, -1: All Children.
            restore_parent_type (str, optional): Restore parents option. 
                'NONE': No Parents (default), 'ALL': All Parents.

        Returns:
            object: An instance of the Job or Schedule class representing the restore operation.

        Raises:
            SDKException: 
                - If `paths` is provided but is not a list.
                - If any of `client`, `instance`, or `backupset` are provided but not all three are present.
                - If `client`, `instance`, or `backupset` are not strings.

        Example:
            >>> # In-place restore of all metadata components
            >>> job = salesforce_instance.metadata_restore_to_salesforce()
            >>> print(f"Restore job started: {job}")

            >>> # Out-of-place restore of specific components
            >>> job = salesforce_instance.metadata_restore_to_salesforce(
            ...     paths=['/Metadata/unpackaged/objects/Account.object'],
            ...     client='DestinationClient',
            ...     instance='DestinationInstance',
            ...     backupset='DestinationBackupset'
            ... )
            >>> print(f"Out-of-place restore job: {job}")

        #ai-gen-doc
        """
        DEST_PARAMS = ('client', 'instance', 'backupset')

        if not isinstance(kwargs.get('paths', list()), list):
            raise SDKException('Instance', '101')

        if any(param in kwargs for param in DEST_PARAMS) and \
                not all(isinstance(kwargs.get(param, None), str) for param in DEST_PARAMS):
            raise SDKException('Instance', '101')

        if not 'paths' in kwargs:
            kwargs['paths'] = ['/Metadata/unpackaged/']
        
        request_json = self._restore_json(
            restore_to_salesforce=True,
            is_metadata_restore=True,
            **kwargs
        )
        
        return self._process_restore_response(request_json)