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
    """Class for representing an Instance of the Salesforce instance type."""

    @property
    def ca_instance_type(self):
        """
        Returns the instance type of this cloud apps instance

        Returns:
            (str): Instance Type
        """
        return 'SALESFORCE'

    @property
    def organization_id(self):
        """
        Returns the Salesforce organization id

        Returns:
            (str): Organization Id

        Raises:
            SDKException: if attribute could not be fetched
        """
        try:
            return self._properties['cloudAppsInstance']['salesforceInstance']['sfOrgID']
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch organization ID')

    @property
    def login_url(self):
        """
        Returns the login url of Salesforce organization

        Returns:
            (str): Login URL

        Raises:
            SDKException: if attribute could not be fetched
        """
        try:
            return self._properties['cloudAppsInstance']['salesforceInstance']['endpoint']
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch login url')

    @property
    def consumer_id(self):
        """
        Returns the Consumer Id of the Salesforce connected app used to authenticate with Salesforce by this instance

        Returns:
            (str): Consumer Id

        Raises:
            SDKException: if attribute could not be fetched
        """
        try:
            return self._properties['cloudAppsInstance']['salesforceInstance']['consumerId']
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch login url')

    @property
    def proxy_client(self):
        """
        Returns the name of the access node.

        Returns:
            (str): Access Node

        Raises:
            SDKException:
                if attribute could not be fetched

                if access node is a client group
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
    def access_node(self):
        """
        Returns a dictionary containing clientName and clientId or clientGroupName and clientGroupId depending on
        whether a single client or a client group is configured as access node.

        Returns:
            (dict): Dictionary containing access node name and id

        Raises:
            SDKException: if attribute could not be fetched
        """
        try:
            access_node = self._properties['cloudAppsInstance']['generalCloudProperties']['accessNodes'] \
                ['memberServers'][0]['client'].copy()
            if 'entityInfo' in access_node:
                del access_node['entityInfo']
            return access_node
        except KeyError:
            raise SDKException('Instance', '105', 'Could not fetch access node')

    def _restore_json(self, **kwargs):
        """
        Returns the JSON request to pass to the API as per the options selected by the user

        Args:
            **kwargs (dict): Dict of named parameters to set for restore

        Returns:
            (dict): Request JSON
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

    def restore_to_file_system(self, **kwargs):
        """
        Runs object level restore to file system and returns object of Job or Schedule class. For out of place restore,
        pass both client and path_to_store_csv parameters. By default, will restore to access node and download cache
        path.

        Args:
            **kwargs (dict): Restore options including
                {
                    paths (list[str]): List of files and objects to restore like
                                ['/Files/filename', '/Objects/object_name']
                                (Default is ['/Files/', '/Objects/'] which selects all files and objects for restore),

                    client (str): Name of destination client (Default is access node),

                    path_to_store_csv (str): path on destination client to restore to (Default is download cache path),

                    from_time (str): time to restore contents after like YYYY-MM-DD HH:MM:SS (Default is None),

                    to_time (str): time to restore contents before like YYYY-MM-DD HH:MM:SS (Default is None),

                    no_of_streams (int): Number of streams to use for restore (Default is 2),

                    dependent_restore_level (int): restore children option (Default is 0)
                                                    0  -- No Children
                                                    1  -- Immediate Children
                                                    -1 -- All Children,

                    restore_parent_type (str): restore parents option (Default is 'NONE')
                                                    'NONE' -- No Parents
                                                    'ALL'  -- All Parents
                }

        Returns:
            object: Object of Job or Schedule class

        Raises:
            SDKException:
                if paths is given but is not a list
    
                if client parameter is not given and the access node configured with this instance is a client group
                
                if either client or path_to_store_csv is given but not both are present
                
                if client or path_to_store_csv are not strings
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
            db_type,
            db_host_name,
            db_name,
            db_user_name,
            db_password,
            **kwargs
        ):
        """
        Runs object level restore to database and returns object of Job or Schedule class

        Args:
            db_type (str): Type of database out of 'POSTGRESQL' or 'SQLSERVER'

            db_host_name (str): Hostname of database server

            db_name (str): Database name where objects will be restored

            db_user_name (str): Username of database user

            db_password (str): Password of database user

            **kwargs (dict): Other restore options including
                {
                    paths (list[str]): List of files and objects to restore like
                                ['/Files/filename', '/Objects/object_name']
                                (Default is ['/Objects/'] which selects all objects for restore),

                    db_instance (str): Database instance for SQL Server,

                    db_port (int): Port of database server (Default is 5432 for POSTGRESQL and 1433 for SQLSERVER),

                    from_time (str): time to restore contents after like YYYY-MM-DD HH:MM:SS (Default is None),

                    to_time (str): time to restore contents before like YYYY-MM-DD HH:MM:SS (Default is None),

                    no_of_streams (int): Number of streams to use for restore (Default is 2),

                    path_to_store_csv (str): path to use as staging folder (Default is download cache path),

                    dependent_restore_level (int): restore children option (Default is 0)
                                                    0  -- No Children
                                                    1  -- Immediate Children
                                                    -1 -- All Children,

                    restore_parent_type (str): restore parents option (Default is 'NONE')
                                                    'NONE' -- No Parents
                                                    'ALL'  -- All Parents
                }

        Returns:
            object: Object of Job or Schedule class

        Raises:
            SDKException:
                if required parameters are not of the correct type

                if db_type is 'SQLSERVER' but db_instance is not given/ is not a string

                if paths is given but is not a list
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

    def restore_to_salesforce_from_database(self, **kwargs):
        """
        Runs restore to Salesforce from database and returns object of Job or Schedule class. For out of place restore,
        pass the client, instance and backupset parameters. If database parameters are not passed, sync db will be used.

        Args:
            **kwargs (dict): Other restore options including
                {
                    paths (list[str]): List of files and objects to restore like
                                ['/Files/filename', '/Objects/object_name']
                                (Default is ['/Files/', '/Objects/'] which selects all files and objects for restore),

                    client (str): Name of destination client (Default is source client),

                    instance (str): Name of destination instance (Default is source instance),

                    backupset (str): Name of destination backupset (Default is source backupset),

                    db_type (str): Type of database out of 'POSTGRESQL' or 'SQLSERVER',

                    db_host (str): Hostname of database server,

                    db_name (str): Database name where objects will be restored,

                    db_user_name (str): Username of database user,

                    db_password (str): Password of database user,

                    db_instance (str): Database instance for SQL Server,

                    db_port (int): Port of database server (Default is 5432 for POSTGRESQL and 1433 for SQLSERVER),

                    from_time (str): time to restore contents after like YYYY-MM-DD HH:MM:SS (Default is None),

                    to_time (str): time to restore contents before like YYYY-MM-DD HH:MM:SS (Default is None),

                    no_of_streams (int): Number of streams to use for restore (Default is 2),

                    path_to_store_csv (str): path to use as staging folder (Default is download cache path),

                    dependent_restore_level (int): restore children option (Default is 0)
                                                    0  -- No Children
                                                    1  -- Immediate Children
                                                    -1 -- All Children,

                    restore_parent_type (str): restore parents option (Default is 'NONE')
                                                    'NONE' -- No Parents
                                                    'ALL'  -- All Parents
                }

        Returns:
            object: Object of Job or Schedule class

        Raises:
            SDKException:
                if paths is given but is not a list

                if any database parameters are given but not all are present

                if database parameters are not all strings

                if db_type is 'SQLSERVER' but db_instance is not given/ is not a string

                if either client, instance or backupset are given but not all three are present

                if client, instance and backupset are not strings
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

    def restore_to_salesforce_from_media(self, **kwargs):
        """
        Runs restore to Salesforce from database and returns object of Job or Schedule class. For out of place restore,
        pass the client, instance and backupset parameters. If database parameters are not passed, sync db will be used
        as staging db.

        Args:
            **kwargs (dict): Other restore options including
                {
                    paths (list[str]): List of files and objects to restore like
                                ['/Files/filename', '/Objects/object_name']
                                (Default is ['/Files/', '/Objects/'] which selects all files and objects for restore),

                    client (str): Name of destination client (Default is source client),

                    instance (str): Name of destination instance (Default is source instance),

                    backupset (str): Name of destination backupset (Default is source backupset),

                    db_type (str): Type of database out of 'POSTGRESQL' or 'SQLSERVER',

                    db_host (str): Hostname of database server,

                    db_name (str): Database name where objects will be restored,

                    db_user_name (str): Username of database user,

                    db_password (str): Password of database user,

                    db_instance (str): Database instance for SQL Server,

                    db_port (int): Port of database server (Default is 5432 for POSTGRESQL and 1433 for SQLSERVER),

                    from_time (str): time to restore contents after like YYYY-MM-DD HH:MM:SS (Default is None),

                    to_time (str): time to restore contents before like YYYY-MM-DD HH:MM:SS (Default is None),

                    no_of_streams (int): Number of streams to use for restore (Default is 2),

                    path_to_store_csv (str): path to use as staging folder (Default is download cache path),

                    dependent_restore_level (int): restore children option (Default is 0)
                                                    0  -- No Children
                                                    1  -- Immediate Children
                                                    -1 -- All Children,

                    restore_parent_type (str): restore parents option (Default is 'NONE')
                                                    'NONE' -- No Parents
                                                    'ALL'  -- All Parents
                }

        Returns:
            object: Object of Job or Schedule class

        Raises:
            SDKException:
                if paths is given but is not a list

                if any database parameters are given but not all are present

                if database parameters are not all strings

                if db_type is 'SQLSERVER' but db_instance is not given/ is not a string

                if either client, instance or backupset are given but not all three are present

                if client, instance and backupset are not strings
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

    def metadata_restore_to_file_system(self, **kwargs):
        """
        Runs metadata restore to file system and returns object of Job or Schedule class. For out of place restore,
        pass both client and path_to_store_csv parameters. By default, will restore to access node and download cache
        path.

        Args:
            **kwargs (dict): Other restore options including
                {                    
                    paths (list[str]): List of metadata components to restore like
                                ['/Metadata/unpackaged/objects/Account.object',
                                 '/Metadata/unpackaged/profiles/Admin.profile']
                                (Default is ['/Metadata/unpackaged/'] which selects all metdata components for restore),
                                
                    client (str): Name of destination client (Default is access node),
                    
                    path_to_store_csv (str): path on destination client to restore to (Default is download cache path),
                    
                    from_time (str): time to restore contents after like YYYY-MM-DD HH:MM:SS (Default is None),
                    
                    to_time (str): time to restore contents before like YYYY-MM-DD HH:MM:SS (Default is None),
                    
                    no_of_streams (int): Number of streams to use for restore (Default is 2),
                    
                    dependent_restore_level (int): restore children option (Default is 0)
                                                    0  -- No Children
                                                    1  -- Immediate Children
                                                    -1 -- All Children,
                                                    
                    restore_parent_type (str): restore parents option (Default is 'NONE')
                                                    'NONE' -- No Parents
                                                    'ALL'  -- All Parents
                }

        Returns:
            object: Object of Job or Schedule class

        Raises:
            SDKException:
                if paths is given but is not a list
    
                if client parameter is not given and the access node configured with this instance is a client group
                
                if either client or path_to_store_csv is given but not both are present
                
                if client or path_to_store_csv are not strings
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

    def metadata_restore_to_salesforce(self, **kwargs):
        """
        Runs metadata restore to Salesforce and returns object of Job or Schedule class. For out of place restore,
        pass client, instance and backupset parameters.

        Args:
            **kwargs (dict): Other restore options including
                {
                    paths (list[str]): List of metadata components to restore like
                                ['/Metadata/unpackaged/objects/Account.object',
                                 '/Metadata/unpackaged/profiles/Admin.profile']
                                (Default is ['/Metadata/unpackaged/'] which selects all metdata components for restore),
                                
                    client (str): Name of destination client (Default is source client),
                    
                    instance (str): Name of destination instance (Default is source instance),
                    
                    backupset (str): Name of destination backupset (Default is source backupset),
                    
                    from_time (str): time to restore contents after like YYYY-MM-DD HH:MM:SS (Default is None),
                    
                    to_time (str): time to restore contents before like YYYY-MM-DD HH:MM:SS (Default is None),
                    
                    no_of_streams (int): Number of streams to use for restore (Default is 2),
                    
                    path_to_store_csv (str): path to use as staging folder (Default is download cache path),
                    
                    dependent_restore_level (int): restore children option (Default is 0)
                                                    0  -- No Children
                                                    1  -- Immediate Children
                                                    -1 -- All Children,
                                                    
                    restore_parent_type (str): restore parents option (Default is 'NONE')
                                                    'NONE' -- No Parents
                                                    'ALL'  -- All Parents
                }

        Returns:
            object: Object of Job or Schedule class

        Raises:
            SDKException:
                if paths is given but is not a list
                
                if either client, instance or backupset are given but not all three are present

                if client, instance and backupset are not strings
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
