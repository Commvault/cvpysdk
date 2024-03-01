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

"""File for handling all the exceptions for the CVPySDK python package.

EXCEPTION_DICT:
    A python dictionary for holding all the exception messages for a specific event or class.

    Any exceptions to be raised from the SDK in a module should be added to this dictionary.

    where,

        -   the key is the module name or the class name where the exception is raised

        -   the value is a dictionary:

            -   key is a unique ID to identify the exception message

            -   value is the exception message

|

SDKException:
    Class inheriting the "Exception" Base class for raising
    a specific exception for the CVPySDK python package.

    The user should create an instance of the SDKException class:

        **SDKException(exception_module, exception_id, exception_message)**

        where,

            -   exception_module:   the module in which the exception is being raised

                -   key in the EXCEPTION_DICT

            -   exception_id:       unique ID which identifies the message for the Exception

            -   exception_message:  additional message to the exception

                -   only applicable if the user wishes to provide an additional message to the
                    exception along with the message already present as the value for the
                    exception_module - exception_id pair

    Example:

        **raise SDKException('CVPySDK', '101')**

        will raise the exception as:

            SDKException: Failed to Login with the credentials provided

        and, **raise SDKException('CVPySDK', '101', 'Please check the credentials')**

        will raise:

            SDKException: Failed to Login with the credentials provided

            Please check the credentials

        where the user given message is appended to the original message joined by new line

"""

from __future__ import absolute_import
from __future__ import unicode_literals

# Common dictionary for all exceptions among the python package
EXCEPTION_DICT = {
    'Response': {
        '101': 'Response was not success',
        '102': 'Response received is empty',
        '500': 'Unable to perform the requested method'
    },
    'Commcell': {
        '101': 'Commcell is not reachable. Please check the commcell name and services again',
        '102': 'Credentials not received. Please try again.',
        '103': 'Failed to get the CommServ details',
        '104': 'Failed to send an email to specified user',
        '105': 'Failed to run the Data Aging job',
        '106': 'Failed to get the SAML token',
        '107': 'Data type of the input(s) is not valid',
        '108': ''
    },
    'CVPySDK': {
        '101': 'Failed to Login with the credentials provided',
        '102': '',
        '103': 'Reached the maximum attempts limit',
        '104': 'This session has expired. Please login again',
        '105': 'Script Type is not valid',
        '106': 'The token has expired. Please login again',
        '107': 'No mapping exists for the given token for any user'
    },
    'DisasterRecovery': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Client': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Time Value should be greater than current time',
        '104': 'Time Value entered is not of correct format',
        '105': 'Script Type is not supported',
        '106': 'Failed to get the instance',
        '107': 'Service Restart timed out',
        '108': 'Failed to get the log directory',
        '109': 'Operation is not supported for this Client'
    },
    'Agent': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Time Value should be greater than current time',
        '104': 'Time Value entered is not of correct format'
    },
    'Backupset': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Class object should be an instance of Agent / Instance class',
        '104': 'Invalid pruning type. Valid inputs "days_based" or "cycles_based".',
        '105': 'Invalid days/cycles value. Please provide an integer value >= 2.',
        '106': 'IndexServer value should be a client object'
    },
    'Instance': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Input date is incorrect',
        '104': 'File/Folder(s) to restore list is empty',
        '105': 'Could not fetch instance property',
        '106': 'Invalid policy name under given instance. Validate the policy name',
        '107': 'Unsupported auto discovery mode provided.'
               'Valid values are REGEX and GROUP',
        '108': 'Invalid FREL client'
    },
    'Subclient': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Backup Level not identified. Please check the backup level again',
        '104': 'File/Folder(s) to restore list is empty',
        '105': 'Type of client should either be the Client class instance or string',
        '106': 'Input date is incorrect',
        '107': 'End Date should be greater than the Start Date',
        '108': 'Time Value should be greater than current time',
        '109': 'Time Value entered is not of correct format',
        '110': 'No data found at the path specified',
        '111': 'No File/Folder matched the input value',
        '112': 'Method Not Implemented',
        '113': 'Type of instance should either be the Instance class instance or string',
        '114': 'Type of backupset should either be the Backupset class instance or string',
        '115': 'Class object should be an instance of Agent / Instance / Backupset class',
        '116': 'Auto discovery values should be a list',
        '117': 'Auto discovery is disabled at instance level',
        '118': 'Failed to run the backup copy job',
        '119': 'Invalid pruning type. Valid inputs "days_based" or "cycles_based".',
        '120': 'Invalid days/cycles value. Please provide an integer value greater than 0.',
        '121': 'IndexServer value should be a client object',
        '122': 'In-Place restore is not supported with multiple source paths'
    },
    'Job': {
        '101': 'Incorrect JobId',
        '102': '',
        '103': 'No job exists with the specified Job ID',
        '104': 'No records found for this Job',
        '105': 'Failed to get the Job Details',
        '106': 'Unexpected response received from server',
        '107': 'Job Info Type not passed from AdvancedJobDetailType enum',
        '108': 'Data type of input(s) is not valid'
    },
    'Storage': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Type of media agent should either be the MediaAgent class instance or string',
        '104': 'Type of library should either be the DiskLibrary class instance or string',
        '105': 'No storage policies exist for this user',
        '106': 'Failed to run the backup copy job',
        '107': 'Failed to run the deferred catalog job',
        '108': 'Failed to run the DDB move job',
        '109': 'Failed to run the DDB verification job',
        '110': 'Input data is not correct',
        "111": 'Failed to update copy property',
        "112": 'Failed to run DDB Reconstruction job',
        "113": 'Failed to run DDB space reclaimation job'
    },
    'Schedules': {
        '101': 'Invalid Class object passed as argument to the Schedules class',
        '102': 'Data type of the input(s) is not valid',
        '103': 'Invalid operation type passed to Schedules class',
        '104': 'Provided Option cannot be updated',
        '105': 'Could not find the provided schedule name/id',
        '106': ''
    },
    'ClientGroup': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Time Value should be greater than current time',
        '104': 'Time Value entered is not of correct format'
    },
    'UserGroup': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Domain': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Alert': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Workflow': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Input is not valid XML / file path',
        '104': 'No Workflow exists with the given name',
        '105': 'Failed to set workflow properties'
    },
    'Datacube': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to get the list of analytics engines',
        '104': 'Failed to get the datasources'
    },
    'ContentAnalyzer': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to get ContentAnalyzer cloud details'
    },
    'ActivateEntity': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to get entity regex details from commcell',
        '104': 'Unable to create regex entity in the commcell',
        '105': 'Unable to delete regex entity in the commcell',
        '106': 'Unable to modify regex entity in the commcell',
        '107': 'Failed to get entity container details from commcell'
    },
    'Classifier': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to get classifier details from commcell',
        '104': 'Unable to create classifier in the commcell',
        '105': 'Unable to delete classifier in the commcell',
        '106': 'Unable to modify classifier in the commcell',
        '107': 'Training model data zip file not exists in given path',
        '108': 'Model Data Training failed on this classifier',
        '109': 'Cancel Training failed on this classifier'
    },
    'Tags': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to get TagSet details from commcell',
        '104': 'Unable to create TagSet in the commcell',
        '105': 'Unable to modify TagSet in the commcell',
        '106': 'Unable to find given tag name in this tagset',
        '107': 'Unable to do TagSet security association in the commcell'
    },
    'EntityManager': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'GlobalFilter': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Plan': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Content Analyzer input is missing',
        '104': 'Please provide either entity list or classifier list in input',
        '105': 'Failed to share plan with user or group'
    },
    'Inventory': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to fetch inventories details from commcell',
        '104': 'Failed to fetch inventory properties from commcell',
        '105': 'Failed to create an Inventory',
        '106': 'Unable to find inventory in commcell',
        '107': 'Failed to Delete an Inventory',
        '108': 'Failed to add asset to Inventory',
        '109': 'Unable to find asset in the Inventory',
        '110': 'Failed to delete asset from Inventory',
        '111': 'Failed to share Inventory'


    },
    'EdiscoveryClients': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to start crawl job',
        '104': 'Failed to get job history',
        '105': 'Failed to get job status',
        '106': 'Failed to get Ediscovery clients',
        '107': 'Unable to get display names for associated data sources in this client',
        '108': 'Data source doesnt exists on this client',
        '109': 'Failed to share ediscovery client with user/group',
        '110': 'Failed to fetch data source properties',
        '111': 'Failed to delete data source',
        '112': 'Failed to perform search',
        '113': 'Failed to perform export',
        '114': 'Failed to perform export status check',
        '115': 'Failed to create data source',
        '116': 'Failed to perform review actions on documents',
        '117': 'Failed to get Ediscovery projects',
        '118': 'Failed to get Ediscovery project properties',
        '119': 'Failed to add Ediscovery client',
        '120': 'Failed to delete Ediscovery client',
    },
    'FileStorageOptimization': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to find given Server name in FSO',
        '104': 'Failed to find data source in FSO Server',
        '105': 'Failed to start collection job at server level',
        '106': "Failed to find server group name in FSO",
        '107': 'Failed to start collection job at server group level',

    },
    'SensitiveDataGovernance': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to find given project name in SDG',
    },
    'RequestManager': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failed to get requests details from commcell',
        '104': 'Failed to get request properties',
        '105': 'Unable to find given request',
        '106': 'Failed to delete request',
        '107': 'Failed to add request',
        '108': 'Failed to configure request',
        '109': 'Failed to mark review as complete as it has non-reviewed documents',
        '110': 'Failed to request approval as review is not in completed state'
    },
    'ComplianceSearch': {
        '101': 'Provided user or user group name does not exist',
        '102': 'Invalid permission name provided',
        '103': 'Export not found under the export set',
        '104': 'Export deletion failed with error',
        '105': 'Failed to get the export set with provided export set name',
        '106': 'Export Set not found'
    },
    'Salesforce': {
        '101': 'Neither Sync Database enabled nor user provided database details for restore',
        '102': ''
    },
    'Metrics': {
        '101': 'Invalid input(s) specified'
    },
    'InternetOptions': {
        '101': 'Invalid input(s) specified'
    },
    'Virtual Machine': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'User': {
        '101': 'Data type of input(s) is not valid',
        '102': '',
        '103': 'User with same name already exists'
    },
    'Role': {
        '101': 'Data type of input(s) is not valid',
        '102': ''
    },
    'Security': {
        '101': 'Data type of input(s) is not valid',
        '102': ''
    },
    'Credential': {
        '101': 'Data type of input(s) is not valid',
        '102': ''
    },
    'DownloadCenter': {
        '101': 'Response received is not a proper XML. Please check the XML',
        '102': '',
        '103': 'Category does not exist at Download Center',
        '104': 'Category already exists at Download Center',
        '105': 'Sub Category already exists for the given Category at Download Center',
        '106': 'Package does not exist at Download Center. Please check the name again',
        '107': 'Failed to download the package',
        '108': 'Category does not exists at Download Center',
        '109': 'Sub Category does not exists at Download Center',
        '110': 'Multiple platforms available. Please specify the platform',
        '111': ('Multiple download types available for this platform. '
                'Please specify the download type'),
        '112': 'Package is not available for the given platform',
        '113': 'Package is not available for the given download type',
        '114': 'Package already exists with the given name',
        '115': 'Version is not available on Download Center',
        '116': 'Platform is not supported on Download Center',
        '117': 'Download Type is not supported on Download Center',
        '118': 'File is not a valid README file',
        '119': 'Failed to upload the package'
    },
    'Organization': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'No organization exists with the given name',
        '104': 'Failed to delete the organization',
        '105': 'Email address is not valid',
        '106': 'Organization already exists',
        '107': 'Failed to add organization',
        '108': 'Failed to enable Auth Code Generation for the Organization',
        '109': 'Failed to disable Auth Code Generation for the Organization',
        '110': 'Failed to update the properties of the Organization',
        '111': ('Plan is not associated with the organization. '
                'Add plan to the Organization, and then set it as the default'),
        '112': 'Failed to activate organization',
        '113': 'Failed to deactivate organization',
        '114': 'Input is not provided in expected manner'
    },
    'RemoteOrganization': {
        '101': 'Failed to update organization operators remotely',
        '102': 'Failed to activate organization remotely',
        '103': 'Failed to deactivate organization remotely',
        '104': 'Failed to update organization tags remotely',
        '105': 'Data type of the input(s) is not valid',
        '106': '',
        '107': 'Email address is not valid',
        '108': 'Organization already exists',
        '109': 'Failed to add organization remotely',
        '110': 'No organization exists with the given name in workloads or idp'
    },
    'StoragePool': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'No storage pool exists with the given name',
    },
    'Monitoring': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'ReplicationPairs': {
        '101': 'Failed to get replication pairs information',
        '102': 'Invalid response received for replication pairs',
        '103': 'Replication Pair not found'
    },
    'BLRPairs': {
        '101': 'Data type of the input(s) is not valid',
        '102': 'BLR Pair not found',
        '103': 'RPStore not found'
    },
    'ReplicationGroup': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'FailoverGroup': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Failover group does not exist'
    },
    'ConfigurationPolicies': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Snap': {
        '102': 'Failed to run the job for Snap Operation',
        '103': 'Failed to update Snap Configs'
    },
    'OperationWindow': {
        '101': 'Failed to create a operation window',
        '102': '',
        '103': 'Failed to delete the operation window',
        '104': 'Failed to list operation windows',
        '105': 'Failed to modify a operation window',
        '106': 'Data type of the input(s) is not valid'
    },
    'IdentityManagement': {
        '101': 'Failed to retreive apps',
        '102': 'App not found',
        '103': 'Failed to configure identity app',
        '104': 'Failed to delete identity app',
        '105': 'Failed to modify identity app',
        '106': 'Failed to get redirect url of user'
    },
    'CommCellMigration': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Please specify all the required inputs',
        '104': 'Please give appropriate input(s)',
        '105': 'Both Clients list and Other Entities list cannot be none',
        '106': 'Incorrect SQL credentials provied',
        '107': 'Given client is not available for export'
    },
    'GlobalRepositoryCell': {
        '101': 'Data type of the input(s) is not valid',
        '102': '',
        '103': 'Podcell ID and Podcell name both cannot be None',
        '104': 'Unable to lookup Podcell ID'
    },
    'NetworkTopology': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Certificates': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'Download': {
        '101': 'Failed to execute the download Job',
        '102': 'service_pack version argument is missing in the method call'
    },
    'Install': {
        '101': 'Insufficient parameters are given',
        '102': 'Invalid client name is given',
        '103': 'Invalid client group name is given',
        '104': 'Installation failed please check the logs',
        '105': 'please provide the features to be installed',
        '106': 'please provide the client details',
        '107': 'Failed to execute Install job'
    },
    'StorageArray': {
        '101': 'Array already exist',
        '102': 'Failed to add array',
        '103': 'Failed to delete array'
    },
    'NameChange': {
        '101': 'Client hostname not provided',
        '102': 'Commcell hostname not provided',
        '103': 'Old domain name not provided',
        '104': 'New domain name not provided',
        '105': 'Client ID list not provided'
    },
    'CommcellRegistration': {
        '101': 'Failed to register commcell',
        '102': '',
        '103': 'Failed to unregister commcell',
        '104': 'Datatype of the input is not valid',
        '105': 'Failed to reach remote commcell.',
        '106': 'Failed to authenticate remote commcell. Invalid user name and password.',
        '107': 'Insufficient permissions'
    },
    'LiveSync': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'BackupNetworkPairs': {
        '101': '',
    },
    'Uninstall': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'IndexServers': {
        '101': 'Data type of the input(s) is not valid',
        '102': 'Index Server not found',
        '103': 'Invalid role name',
        '104': '',
        '105': 'Unsupported backup level specified. Please check',
        '106': 'Storage policy is not associated with subclient. Please associate',
        '107': 'Backup is not enabled for client/subclient',
        '108': 'Client name not specified for solr cloud restore',
        '109': 'Provide the Index Server Node name for browse to work',
        '110': 'Multiple roles found, Unix Index Server Browse works for only 1 role at a time.',
        '111': 'Failed to delete docs in the core'
    },
    'HACClusters': {
        '101': 'Data type of the input(s) is not valid',
        '102': 'HAC not found',
        '103': 'HAC zKeeper node not found',
    },
    'IndexPools': {
        '101': 'Data type of the input(s) is not valid',
        '102': 'Index pool not found',
        '103': 'Index pool node not found',
    },
    'Metallic': {
        '101': 'Data type of the input(s) is not valid',
        '102': ''
    },
    'KeyManagementServer': {
        '101': 'Data type of the input(s) is not valid',
        '102': 'Key Management Server not found',
        '103': 'Key Management Server type is not valid',
        '104': 'Key Management Server type not found',
        '105': 'Invalid key provider authentication type',
        '106': 'Invalid KMS name',
        '107': 'Key list is missing for Bring Your Own Key'
    },
    'Region': {
        '101': 'Entity type not found.',
        '102': ''
    }
}


class SDKException(Exception):
    """Exception class for raising exception specific to a module."""

    def __init__(self, exception_module, exception_id, exception_message=""):
        """Initialize the SDKException class instance for the exception.

            Args:
                exception_module  (str)  --  name of the module where the exception was raised

                exception_id      (str)  --  id of the exception specific to the exception_module

                exception_message (str)  --  additional message about the exception

            Returns:
                object  -   instance of the SDKException class of type Exception

        """
        exception_id = str(exception_id)

        self.exception_module = exception_module
        self.exception_id = exception_id
        self.exception_message = EXCEPTION_DICT[exception_module][exception_id]

        if exception_message:
            if self.exception_message:
                self.exception_message = '\n'.join([self.exception_message, exception_message])
            else:
                self.exception_message = exception_message

        Exception.__init__(self, self.exception_message)
