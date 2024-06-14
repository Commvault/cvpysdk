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
    """Class for representing an Instance of Amazon RDS"""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the AmazonRDSInstance class

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class

        """
        super(
            AmazonRDSInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

        self._browse_url = self._services['CLOUD_DATABASE_BROWSE']

    def _process_browse_response(self, flag, response):
        """ Process browse request response

            Args:

                flag -- indicates whether the rest API request is successful

                response -- response returned if the request was successful.

            Returns:

                dict    - The snapshot list JSON response received from the browse request

                Exception - If the browse request failed
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

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

             Args:
                kwargs   (list)  --  list of options need to be set for restore

                Ex: For RDS Instance Cluster Restore following are the possible options
                    {
                        destination : 'instance/cluster',
                        source : 'snapshot',
                        options :   {
                                        'archFileId': 123
                                        'isMultiAZ' : true,
                                        'publicallyAccess' : true,
                                        'copyTagsToSnapshot' : false,
                                        'enableDeletionProtection': false,
                                        'targetParameterGroupName': 'param',
                                        'targetSubnetGroup': 'subnet',
                                        'targetDBInstanceClass': 'dc-large-8',
                                        'targetPort': 2990
                                    }
                    }

            Returns:
                dict - JSON request to pass to the API
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
    """Class for representing an Instance of the Amazon Redshift"""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the AmazonRedshiftInstance class

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class

        """
        super(
            AmazonRedshiftInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

        self._browse_url = self._services['CLOUD_DATABASE_BROWSE']

    def _process_browse_response(self, flag, response):
        """ Process browse request response

            Args:

                flag -- indicates whether the rest API request is successful

                response -- response returned if the request was successful.

            Returns:

                dict    - The snapshot list JSON response received from the browse request

                Exception - If the browse request failed
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

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

             Args:
                kwargs   (list)  --  list of options need to be set for restore

                Ex: For Redshift Instance Cluster Restore following are the possible options
                    {
                        destination : 'cluster',
                        source : 'snapshot',
                        options :   {
                                        'allowVersionUpgrade' : true,
                                        'publicallyAccessible' : true,
                                        'restoreTags' : false,
                                        'enableDeletionProtection': false,
                                        'availabilityZone': 'us-east-2a',
                                        'targetParameterGroup': 'param',
                                        'targetSubnetGroup': 'subnet',
                                        'nodeType': 'dc-large-8',
                                        'targetPort': 2990,
                                        'numberOfNodes': 1
                                    }
                    }

            Returns:
                dict - JSON request to pass to the API
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
    """Class for representing an Instance of the Amazon DocumentDB"""

    def __init__(self, agent_object, instance_name, instance_id=None):
        """Initializes the object of the AmazonDocumentDBInstance class

            Args:
                agent_object    (object)  --  instance of the Agent class

                instance_name   (str)     --  name of the instance

                instance_id     (str)     --  id of the instance
                    default: None

            Returns:
                object - instance of the Instance class

        """
        super(
            AmazonDocumentDBInstance,
            self).__init__(
                agent_object,
                instance_name,
                instance_id)

        self._browse_url = self._services['CLOUD_DATABASE_BROWSE']

    def _process_browse_response(self, flag, response):
        """ Process browse request response

            Args:

                flag -- indicates whether the rest API request is successful

                response -- response returned if the request was successful.

            Returns:

                dict    - The snapshot list JSON response received from the browse request

                Exception - If the browse request failed
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

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

             Args:
                kwargs   (list)  --  list of options need to be set for restore

                Ex: For DocumentDB Instance Cluster Restore following are the possible options
                    {
                        destination : 'cluster',
                        source : 'snapshot',
                        options :   {
                                        'restoreTags' : false,
                                        'enableDeletionProtection': false,
                                        'availabilityZone': 'us-east-2a',
                                        'targetSubnetGroup': 'subnet',
                                        'targetInstanceClass': 'dc-large-8',
                                        'targetPort': 2990,
                                        'numberOfNodes': 1
                                    }
                    }

            Returns:
                dict - JSON request to pass to the API
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
    """Class for representing an Instance of the Amazon DynamoDB"""

    def _restore_json(self, **kwargs):
        """Returns the JSON request to pass to the API as per the options selected by the user.

             Args:
                kwargs   (list)  --  list of options need to be set for restore

                For DynamoDB Instance Cluster Restore following are the required parameters
                        destination : "",
                        source : "",
                        options = {
                            'paths':  (list of strings)
                            'table_map': (list of dicts)
                            'adjust_write_capacity': (int)
                            'destination_client': (string))
                            'destination_instance': string
                    }

                    }
                Example:
                        destination : "",
                        source : "",
                        options :   {
                                    'paths': ['/us-east-1/table_1'],
                                    'table_map': [{
                                    'srcTable':{'name': 'table_1', 'region':'us-east-1'},
                                    'destTable':{'name': 'table_2', 'region': 'us-east-2'}
                                    }]
                                    'adjust_write_capacity': 100,
                                    'destination_client': 'client1',
                                    'destination_instance': 'DynamoDB'
                                    }
            Returns:
                dict - JSON request to pass to the API
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