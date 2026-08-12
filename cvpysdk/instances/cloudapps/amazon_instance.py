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

""" File for operating on a amazon instances.

AmazonRDSInstance, AmazonRedshiftInstance, AmazonDocumentDBInstance, AmazonDynamoDBInstance
are the classes defined in this file.

AmazonRDSInstance:  Derived class from CloudDatabaseInstance Base class, representing a Cloud Database instance of
                    type Amazon RDS and to perform operations on that instance

AmazonRDSInstance:

    __init__()                      --  Initializes amazon rds instance object with associated
    agent_object, instance name and instance id

    _process_browse_request()       --  Process the response received from browse request

    _restore_json()                 -- Generates Restore json with restore options


AmazonRedshiftInstance:   Derived class from CloudDatabaseInstance Base class, representing a
                        Cloud Database instance of type Amazon Redshift and to
                        perform operations on that instance

AmazonRedshiftInstance:

    __init__()                      --  Initializes amazon redshift instance object with associated
    agent_object, instance name and instance id

    _process_browse_request()       --  Process the response received from browse request

    _restore_json()                 -- Generates Restore json with restore options


AmazonDocumentDBInstance: Derived class from CloudDatabaseInstance Base class, representing a
                            Cloud Database instance of type Amazon DocumentDB and to perform
                            operations on that instance

AmazonDocumentDBInstance

    __init__()                      -- Initializes amazon documentdb instance object with associated
    agent_object, instance name and instance id

    _process_browse_request()       --  Process the response received from browse request

    _restore_json()                 -- Generates Restore json with restore options

AmazonDynamoDBInstance: Derived class from CloudDatabaseInstance Base class, representing a
                        Cloud Database instance of type Amazon DynamoDB and to
                        perform operations on that instance

AmazonDynamoDBInstance:

    _restore_json()                 -- Generates Restore json with restore option
"""

from __future__ import unicode_literals
from .cloud_database_instance import CloudDatabaseInstance
from ...exception import SDKException


class AmazonRDSInstance(CloudDatabaseInstance):
    """
    Represents an instance of Amazon RDS within a cloud database management context.

    This class provides functionality for managing and interacting with Amazon RDS instances,
    including initialization with agent and instance details, processing browse responses,
    and generating restore configurations in JSON format.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Processing of browse responses for RDS instance operations
        - Generation of restore configuration in JSON format

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize an AmazonRDSInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Amazon RDS instance.
            instance_name: The name of the Amazon RDS instance.
            instance_id: Optional; the unique identifier of the Amazon RDS instance. Defaults to None.

        Example:
            >>> agent = Agent(commcell_object, "AmazonRDS")
            >>> rds_instance = AmazonRDSInstance(agent, "my_rds_instance", "rds-123456")
            >>> print(f"Amazon RDS Instance created: {rds_instance}")

        #ai-gen-doc
        """
        super(
            AmazonRDSInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

        self._browse_url = self._services['CLOUD_DATABASE_BROWSE']

    def _process_browse_response(self, flag: bool, response: dict) -> dict:
        """Process the response from a browse request for Amazon RDS snapshots.

        Args:
            flag: Indicates whether the REST API request was successful (True) or not (False).
            response: The response dictionary returned if the request was successful.

        Returns:
            dict: The JSON response containing the snapshot list from the browse request.

        Raises:
            Exception: If the browse request failed (i.e., flag is False).

        Example:
            >>> instance = AmazonRDSInstance()
            >>> result = instance._process_browse_response(True, {"snapshots": [...]})
            >>> print(result)
            {'snapshots': [...]}

        #ai-gen-doc
        """
        if flag:
            if response.json() and 'snapList' in response.json():
                snapshot_list = response.json()['snapList']
            else:
                raise SDKException(
                    'Instance',
                    '102',
                    "Incorrect response from browse.\nResponse : {0}".format(
                        response.json()))
        else:
            o_str = 'Failed to browse content of this instance backups.\nError: "{0}"'
            raise SDKException('Instance', '102', o_str.format(response))
        return snapshot_list

    def _restore_json(self, **kwargs: dict) -> dict:
        """Generate the JSON request payload for the API based on user-selected restore options.

        This method constructs a dictionary representing the restore request, using the provided keyword arguments
        to specify restore parameters such as destination, source, and additional options.

        Example:
            >>> restore_json = rds_instance._restore_json(
            ...     destination='instance/cluster',
            ...     source='snapshot',
            ...     options={
            ...         'archFileId': 123,
            ...         'isMultiAZ': True,
            ...         'publicallyAccess': True,
            ...         'copyTagsToSnapshot': False,
            ...         'enableDeletionProtection': False,
            ...         'targetParameterGroupName': 'param',
            ...         'targetSubnetGroup': 'subnet',
            ...         'targetDBInstanceClass': 'dc-large-8',
            ...         'targetPort': 2990
            ...     }
            ... )
            >>> print(restore_json)
            {'destination': 'instance/cluster', 'source': 'snapshot', 'options': {...}}

        Returns:
            dict: The JSON request dictionary to be sent to the API for restore operations.

        #ai-gen-doc
        """
        restore_json = super(
            AmazonRDSInstance,
            self)._restore_json(**kwargs)

        restore_options = {}
        if kwargs.get("restore_options"):
            restore_options = kwargs["restore_options"]
            for key in kwargs:
                if not key == "restore_options":
                    restore_options[key] = kwargs[key]
        else:
            restore_options.update(kwargs)

        # Populate Redshift restore options
        rds_restore_json = {
            "rdsRestoreOptions": {
                "sourceSnap": {
                    "snapShotName": restore_options['source']
                },
                "targetDbName": restore_options['destination']
            }
        }

        rds_restore_json['rdsRestoreOptions']['isMultiAZ'] = \
            restore_options.get('options', {}).get('isMultiAZ', False)

        rds_restore_json['rdsRestoreOptions']['publicallyAccess'] = \
            restore_options.get('options', {}).get('publicallyAccess', True)

        rds_restore_json['rdsRestoreOptions']['copyTagsToSnapshot'] = \
            restore_options.get('options', {}).get('copyTagsToSnapshot', False)

        rds_restore_json['rdsRestoreOptions']['enableDeletionProtection'] = \
            restore_options.get('options', {}).get('enableDeletionProtection', False)

        rds_restore_json['rdsRestoreOptions']['targetParameterGroupName'] = \
            restore_options.get('options', {}).get('targetParameterGroupName', '')

        rds_restore_json['rdsRestoreOptions']['targetSecurityGroupValue'] = \
            restore_options.get('options', {}).get('targetSubnetGroup', '')

        rds_restore_json['rdsRestoreOptions']['targetDBInstanceClass'] = \
            restore_options.get('options', {}).get('targetDBInstanceClass', '')

        rds_restore_json['rdsRestoreOptions']['targetPort'] = \
            restore_options.get('options', {}).get('targetPort', 0)

        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = \
            rds_restore_json

        return restore_json


class AmazonRedshiftInstance(CloudDatabaseInstance):
    """
    Represents an instance of Amazon Redshift within a cloud database management context.

    This class provides functionality for managing and interacting with Amazon Redshift instances,
    including initialization with agent and instance details, processing browse responses, and
    handling restore operations in JSON format.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Processing of browse responses for Redshift instance operations
        - Handling and generation of restore operations in JSON format

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize an AmazonRedshiftInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this Redshift instance.
            instance_name: The name of the Amazon Redshift instance.
            instance_id: Optional; the unique identifier for the instance. Defaults to None.

        Example:
            >>> agent = Agent(commcell_object, "AmazonRedshift")
            >>> redshift_instance = AmazonRedshiftInstance(agent, "Redshift-Prod", "12345")
            >>> # If instance_id is not known, it can be omitted
            >>> redshift_instance = AmazonRedshiftInstance(agent, "Redshift-Dev")

        #ai-gen-doc
        """
        super(
            AmazonRedshiftInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

        self._browse_url = self._services['CLOUD_DATABASE_BROWSE']

    def _process_browse_response(self, flag: bool, response: dict) -> dict:
        """Process the response from a browse request to Amazon Redshift.

        Args:
            flag: Indicates whether the REST API request was successful (True) or not (False).
            response: The response dictionary returned if the request was successful.

        Returns:
            dict: The JSON response containing the snapshot list from the browse request.

        Example:
            >>> instance = AmazonRedshiftInstance()
            >>> response = instance._process_browse_response(True, {"snapshots": [...]})
            >>> print(response)
            {'snapshots': [...]}

        #ai-gen-doc
        """
        if flag:
            if response.json() and 'snapList' in response.json():
                snapshot_list = response.json()['snapList']
            else:
                raise SDKException(
                    'Instance',
                    '102',
                    "Incorrect response from browse.\nResponse : {0}".format(
                        response.json()))
        else:
            o_str = 'Failed to browse content of this instance backups.\nError: "{0}"'
            raise SDKException('Instance', '102', o_str.format(response))
        return snapshot_list

    def _restore_json(self, **kwargs: dict) -> dict:
        """Generate the JSON request payload for restoring an Amazon Redshift instance.

        This method constructs a JSON dictionary based on the provided keyword arguments,
        which specify the restore options selected by the user. The resulting JSON can be
        passed directly to the API for initiating a restore operation.

        Keyword Args:
            kwargs: Arbitrary keyword arguments representing restore options. These should
                match the expected structure for Redshift instance cluster restore. For example:

                {
                    "destination": "cluster",
                    "source": "snapshot",
                    "options": {
                        "allowVersionUpgrade": True,
                        "publicallyAccessible": True,
                        "restoreTags": False,
                        "enableDeletionProtection": False,
                        "availabilityZone": "us-east-2a",
                        "targetParameterGroup": "param",
                        "targetSubnetGroup": "subnet",
                        "nodeType": "dc-large-8",
                        "targetPort": 2990,
                        "numberOfNodes": 1
                    }
                }

        Returns:
            dict: The JSON request dictionary to be sent to the API for restore operations.

        Example:
            >>> instance = AmazonRedshiftInstance()
            >>> restore_json = instance._restore_json(
            ...     destination="cluster",
            ...     source="snapshot",
            ...     options={
            ...         "allowVersionUpgrade": True,
            ...         "publicallyAccessible": True,
            ...         "restoreTags": False,
            ...         "enableDeletionProtection": False,
            ...         "availabilityZone": "us-east-2a",
            ...         "targetParameterGroup": "param",
            ...         "targetSubnetGroup": "subnet",
            ...         "nodeType": "dc-large-8",
            ...         "targetPort": 2990,
            ...         "numberOfNodes": 1
            ...     }
            ... )
            >>> print(restore_json)
            {'destination': 'cluster', 'source': 'snapshot', 'options': {...}}

        #ai-gen-doc
        """
        restore_json = super(
            AmazonRedshiftInstance,
            self)._restore_json(**kwargs)

        restore_options = {}
        if kwargs.get("restore_options"):
            restore_options = kwargs["restore_options"]
            for key in kwargs:
                if not key == "restore_options":
                    restore_options[key] = kwargs[key]
        else:
            restore_options.update(kwargs)

        # Populate Redshift restore options
        redshift_restore_json = {
            "redshiftRestoreOption": {
                "targetInstanceId": restore_options['destination'],
                "restoreSnapshotId": restore_options['source']
            }
        }

        redshift_restore_json['redshiftRestoreOption']['allowVersionUpgrade'] = \
            restore_options.get('options', {}).get('allowVersionUpgrade', True)

        redshift_restore_json['redshiftRestoreOption']['publicallyAccessible'] = \
            restore_options.get('options', {}).get('publicallyAccessible', True)

        redshift_restore_json['redshiftRestoreOption']['restoreTags'] = \
            restore_options.get('options', {}).get('restoreTags', False)

        redshift_restore_json['redshiftRestoreOption']['enableDeletionProtection'] = \
            restore_options.get('options', {}).get('enableDeletionProtection', False)

        redshift_restore_json['redshiftRestoreOption']['availabilityZone'] = \
            restore_options.get('options', {}).get('availabilityZone', '')

        redshift_restore_json['redshiftRestoreOption']['targetParameterGroupName'] = \
            restore_options.get('options', {}).get('targetParameterGroupName', '')

        redshift_restore_json['redshiftRestoreOption']['targetSubnetGroup'] = \
            restore_options.get('options', {}).get('targetSubnetGroup', '')

        redshift_restore_json['redshiftRestoreOption']['nodeType'] = \
            restore_options.get('options', {}).get('nodeType', '')

        redshift_restore_json['redshiftRestoreOption']['targetPort'] = \
            restore_options.get('options', {}).get('targetPort', 0)

        redshift_restore_json['redshiftRestoreOption']['numberOfNodes'] = \
            restore_options.get('options', {}).get('numberOfNodes', 1)

        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = \
            redshift_restore_json

        return restore_json


class AmazonDocumentDBInstance(CloudDatabaseInstance):
    """
    Represents an instance of Amazon DocumentDB within a cloud database management context.

    This class encapsulates the properties and behaviors associated with an Amazon DocumentDB instance,
    providing mechanisms for initialization, processing browse responses, and restoring instance data
    in JSON format. It is designed to be used as part of a larger cloud database management system,
    inheriting core functionality from the CloudDatabaseInstance base class.

    Key Features:
        - Initialization with agent object, instance name, and instance ID
        - Processing of browse responses for instance data management
        - Restoration of instance state from JSON data

    #ai-gen-doc
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize an AmazonDocumentDBInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this DocumentDB instance.
            instance_name: The name of the Amazon DocumentDB instance.
            instance_id: Optional; the unique identifier for the instance. Defaults to None.

        Example:
            >>> agent = Agent(commcell_object, "AmazonDocumentDB")
            >>> docdb_instance = AmazonDocumentDBInstance(agent, "myDocDBInstance", "12345")
            >>> # The docdb_instance object is now initialized and ready for use

        #ai-gen-doc
        """
        super(
            AmazonDocumentDBInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

        self._browse_url = self._services['CLOUD_DATABASE_BROWSE']

    def _process_browse_response(self, flag: bool, response: dict) -> dict:
        """Process the response from a browse request for Amazon DocumentDB snapshots.

        Args:
            flag: Indicates whether the REST API request was successful (True) or not (False).
            response: The response dictionary returned if the request was successful.

        Returns:
            dict: The JSON response containing the snapshot list from the browse request.

        Raises:
            Exception: If the browse request failed (i.e., flag is False).

        Example:
            >>> instance = AmazonDocumentDBInstance()
            >>> response = instance._process_browse_response(True, {"snapshots": [...]})
            >>> print(response)
            {'snapshots': [...]}

        #ai-gen-doc
        """
        if flag:
            if response.json() and 'snapList' in response.json():
                snapshot_list = response.json()['snapList']
            else:
                raise SDKException(
                    'Instance',
                    '102',
                    "Incorrect response from browse.\nResponse : {0}".format(
                        response.json()))
        else:
            o_str = 'Failed to browse content of this instance backups.\nError: "{0}"'
            raise SDKException('Instance', '102', o_str.format(response))
        return snapshot_list

    def _restore_json(self, **kwargs: dict) -> dict:
        """Generate the JSON request payload for restoring an Amazon DocumentDB instance.

        This method constructs a JSON dictionary based on the options provided via keyword arguments.
        The generated JSON can be used as the request body for the restore API.

        Keyword Args:
            kwargs: Key-value pairs specifying restore options. Typical options include:
                - destination (str): The restore destination, e.g., 'cluster'.
                - source (str): The restore source, e.g., 'snapshot'.
                - options (dict): Additional restore parameters, such as:
                    - restoreTags (bool): Whether to restore tags.
                    - enableDeletionProtection (bool): Enable deletion protection.
                    - availabilityZone (str): Target availability zone.
                    - targetSubnetGroup (str): Subnet group for the target.
                    - targetInstanceClass (str): Instance class for the target.
                    - targetPort (int): Port number for the target.
                    - numberOfNodes (int): Number of nodes to restore.

        Returns:
            dict: The JSON request payload to be sent to the API.

        Example:
            >>> restore_json = docdb_instance._restore_json(
            ...     destination='cluster',
            ...     source='snapshot',
            ...     options={
            ...         'restoreTags': False,
            ...         'enableDeletionProtection': False,
            ...         'availabilityZone': 'us-east-2a',
            ...         'targetSubnetGroup': 'subnet',
            ...         'targetInstanceClass': 'dc-large-8',
            ...         'targetPort': 2990,
            ...         'numberOfNodes': 1
            ...     }
            ... )
            >>> print(restore_json)
            {'destination': 'cluster', 'source': 'snapshot', 'options': {'restoreTags': False, 'enableDeletionProtection': False, 'availabilityZone': 'us-east-2a', 'targetSubnetGroup': 'subnet', 'targetInstanceClass': 'dc-large-8', 'targetPort': 2990, 'numberOfNodes': 1}}

        #ai-gen-doc
        """
        restore_json = super(
            AmazonDocumentDBInstance,
            self)._restore_json(**kwargs)

        restore_options = {}
        if kwargs.get("restore_options"):
            restore_options = kwargs["restore_options"]
            for key in kwargs:
                if not key == "restore_options":
                    restore_options[key] = kwargs[key]
        else:
            restore_options.update(kwargs)

        # Populate DocumentDB restore options
        documentdb_restore_option = {
            "documentDBRestoreOptions": {
                "targetInstanceId": restore_options['destination'],
                "restoreSnapshotId": restore_options['source']
            }
        }

        documentdb_restore_option['documentDBRestoreOptions']['restoreTags'] = \
            restore_options.get('options', {}).get('restoreTags', False)

        documentdb_restore_option['documentDBRestoreOptions']['enableDeletionProtection'] = \
            restore_options.get('options', {}).get('enableDeletionProtection', False)

        documentdb_restore_option['documentDBRestoreOptions']['availabilityZone'] = \
            restore_options.get('options', {}).get('availabilityZone', '')

        documentdb_restore_option['documentDBRestoreOptions']['targetSubnetGroup'] = \
            restore_options.get('options', {}).get('targetSubnetGroup', '')

        documentdb_restore_option['documentDBRestoreOptions']['targetInstanceClass'] = \
            restore_options.get('options', {}).get('targetInstanceClass', '')

        documentdb_restore_option['documentDBRestoreOptions']['targetPort'] = \
            restore_options.get('options', {}).get('targetPort', 0)

        documentdb_restore_option['documentDBRestoreOptions']['numberOfNodes'] = \
            restore_options.get('options', {}).get('numberOfNodes', 1)

        restore_json["taskInfo"]["subTasks"][0]["options"]["restoreOptions"]["cloudAppsRestoreOptions"] = \
            documentdb_restore_option

        return restore_json

class AmazonDynamoDBInstance(CloudDatabaseInstance):
    """
    Represents an instance of Amazon DynamoDB within a cloud database management context.

    This class provides the foundational structure for managing and interacting with
    Amazon DynamoDB instances. It includes internal mechanisms for restoring instance
    state from JSON representations, facilitating persistence and recovery operations.

    Key Features:
        - Representation of Amazon DynamoDB instances
        - Support for restoring instance state from JSON data

    #ai-gen-doc
    """

    def _restore_json(self, **kwargs: dict) -> dict:
        """Construct the JSON request payload for a DynamoDB instance restore operation.

        This method generates the JSON structure required by the API based on the options 
        provided by the user for restoring a DynamoDB instance. The options should include 
        details such as destination, source, and restore-specific parameters.

        Common required parameters for DynamoDB instance cluster restore:
            - destination (str): The destination for the restore.
            - source (str): The source from which to restore.
            - options (dict): Additional restore options, such as:
                - 'paths' (list of str): List of table paths to restore.
                - 'table_map' (list of dict): Mapping of source to destination tables.
                - 'adjust_write_capacity' (int): Write capacity units to set.
                - 'destination_client' (str): Name of the destination client.
                - 'destination_instance' (str): Name of the destination DynamoDB instance.

        Example:
            >>> restore_payload = instance._restore_json(
            ...     destination="",
            ...     source="",
            ...     options={
            ...         'paths': ['/us-east-1/table_1'],
            ...         'table_map': [{
            ...             'srcTable': {'name': 'table_1', 'region': 'us-east-1'},
            ...             'destTable': {'name': 'table_2', 'region': 'us-east-2'}
            ...         }],
            ...         'adjust_write_capacity': 100,
            ...         'destination_client': 'client1',
            ...         'destination_instance': 'DynamoDB'
            ...     }
            ... )
            >>> print(restore_payload)
            {'destination': '', 'source': '', 'options': {...}}

        Returns:
            dict: The JSON request payload to be sent to the API for restore.

        #ai-gen-doc
        """
        restore_json = super(
            AmazonDynamoDBInstance,
            self)._restore_json(**kwargs)

        restore_options = {}
        if kwargs.get('options'):
            restore_options = kwargs['options']
            for key in kwargs:
                if not key == 'options':
                    restore_options[key] = kwargs[key]
        else:
            restore_options.update(kwargs)

        source_backupset_id = int(self.backupsets.all_backupsets['defaultbackupset']['id'])
        dynamodb_restore_option = {
            "dynamoDbRestoreOptions": {
                'tempWriteThroughput': restore_options.get('adjust_write_capacity', ''),
                'overwrite': restore_options.get('overwrite', False),
                'destinationTableList': restore_options.get('table_map', [])
            }
        }
        destination_restore_json = (
            {
                "noOfStreams": restore_options.get("number_of_streams", 2),
                "destClient": {
                    "clientName": restore_options.get("destination_client", "")
                },
                "destinationInstance": {
                    "clientName": restore_options.get("destination_client", ""),
                    "instanceName": restore_options.get("destination_instance", ""),
                    "appName": self._instance['appName']
                }

            })
        restore_json['taskInfo']['associations'][0]['backupsetId'] = source_backupset_id
        restore_json['taskInfo']['subTasks'][0]['options'][
            "restoreOptions"]["destination"] = destination_restore_json
        restore_json['taskInfo']['subTasks'][0]['options'][
            'restoreOptions']['cloudAppsRestoreOptions'] = dynamodb_restore_option
        restore_json['taskInfo']['subTasks'][0]['options'][
            'restoreOptions']['fileOption']['sourceItem'] = restore_options.get("paths", "")
        restore_json['taskInfo']['subTasks'][0]['options'][
            'restoreOptions']['cloudAppsRestoreOptions']['instanceType'] = 22

        return restore_json